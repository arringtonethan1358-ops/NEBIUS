"""Nebius financing: what was raised in 2025-2026, and a frame for funding 2026-2030.

Part 1 reads data/financing_history.csv (every financing since June 2025, from the 6-K
filings) and totals it by instrument and period, then lists what is still outstanding.

Part 2 is the plan, built to be filled in step by step:
  - 2026: capex at the guidance midpoint, with H1 actuals and the financing done since.
  - 2027-2030: $270B of capex; customer prepayments fund 45% of it (taken as given).
  - For reference, the remaining 55% split the way Nebius funded itself outside
    prepayments in 2025-2026.

Part 3 is the revised plan for 2027-2029, year by year: operating cash, leases, secured
GPU loans and a loan on the GPUs already installed come first; equity and converts fill
whatever is left, keeping year-end cash above a floor. It tracks interest, loan
repayments, lease rent, debt outstanding, leverage and new shares.

Writes models/output/financing_plan.md and financing_plan.csv.
Run from the repo root:  python models/financing_plan.py   (standard library only)
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import funding_5gw as fm          # noqa: E402  EBITDA path and year-end 2026 cash
import nebius_scenarios as scen  # noqa: E402  share price

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "models" / "output"

# --- Plan inputs ($B) --------------------------------------------------------
CAPEX_2026_GUIDE = (20.0, 25.0)      # Q2 2026 guidance [PR]
CAPEX_2027_30 = 270.0                # program total, 2027-2030
PHASING = [0.25, 0.25, 0.25, 0.25]   # share of the program in each year
PREPAY_SHARE = 0.45                  # customer prepayments as a share of capex (given)
PLAN_YEARS = [2027, 2028, 2029, 2030]

# --- Revised plan inputs, 2027-2029 ($B unless noted) ------------------------
REVISED_YEARS = [2027, 2028, 2029]
OPCASH_SHARE = 0.60          # cash from operations before interest, as a share of EBITDA (after tax,
                             # working capital and the already-prepaid part of revenue)
LEASE_FUNDED = 8.0           # data center capex paid for by landlords (build-to-suit) each year
LEASE_RENT_YIELD = 0.08      # rent a year on lease-funded capex, starting the year after
GPU_SHARE = 0.64             # GPUs and servers as a share of capex (author's workbook)
SECURED_SHARE_OF_GPU = 0.30  # new GPU loans as a share of GPU capex; investment-grade contracts only
SECURED_RATE = 0.0638        # SOFR 3.88% + 2.50%, the July 2026 MUFG terms
SECURED_TERM = 5             # years; repaid in equal parts starting the year after drawing
EXISTING_GPU_LOAN = 5.0      # 2027 loan against the ~$11B of GPUs installed by mid-2026, less the $775M used
MIN_CASH = 10.0              # floor on year-end cash
EQUITY_SHARE_OF_RAISE = 0.50 # equity (ATM) share of the money raised from investors; the rest is converts
ATM_COST = 0.0125            # ATM commission
NEW_CONVERT_COUPON = 0.025   # coupon on new converts (recent deals: 0.50%-4.50%)
MUFG_LOAN = 0.775            # existing secured loan, due October 2030
SHARES_YE26 = 308.7          # M: Class A + B, NVIDIA warrants and the August exchange shares

PERIODS = [("2025", "2025-01-01", "2025-12-31"), ("H1 2026", "2026-01-01", "2026-06-30"),
           ("Jul–Oct 2026", "2026-07-01", "2026-10-15")]
FLOW_ROWS = [  # (category, label) for money raised
    ("prepayment", "Customer prepayments (increase in deferred revenue)"),
    ("convertible", "Convertible notes"),
    ("equity_offering", "Public share offering"),
    ("atm", "ATM share sales"),
    ("warrant", "NVIDIA pre-funded warrants"),
    ("other_equity", "Share option exercises"),
    ("secured_debt", "Secured term loan"),
    ("subsidiary", "Avride SAFEs (subsidiary)"),
]
EXTERNAL = ("convertible", "equity_offering", "atm", "warrant", "other_equity", "secured_debt")
EQUITY = ("equity_offering", "atm", "warrant", "other_equity")
CONVERT_PREMIUM = 0.40               # typical recent conversion premium, for share equivalents only


def load():
    with open(ROOT / "data" / "financing_history.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["amount"] = float(r["amount_usd_mn"])
    return rows


def totals(rows):
    """{period: {category: $M}} for money raised and capex."""
    t = {p: defaultdict(float) for p, _, _ in PERIODS}
    for r in rows:
        for p, start, end in PERIODS:
            if start <= r["date"] <= end:
                t[p][r["category"]] += r["amount"]
    return t


def outstanding(rows):
    """Convertible series net of exchanges, plus secured debt."""
    series = {}
    for r in rows:
        if r["category"] in ("convertible", "exchange", "secured_debt"):
            key = r["series"]
            s = series.setdefault(key, {"series": key, "kind": r["category"], "principal": 0.0, "accreted": 0.0,
                                        "coupon": float(r["coupon"] or 0), "maturity": r["maturity"],
                                        "conversion_price": float(r["conversion_price"] or 0)})
            s["principal"] += r["amount"]
            s["accreted"] += float(r["accreted_usd_mn"] or 0)
    out = [s for s in series.values() if s["kind"] != "exchange" and s["principal"] > 0]
    for s in out:
        s["shares"] = s["principal"] / s["conversion_price"] if s["conversion_price"] else 0.0
        s["coupon_cost"] = s["principal"] * s["coupon"]
    return sorted(out, key=lambda s: s["maturity"])


def reference_mix(t):
    """Share of 2025-2026 money raised outside prepayments, by instrument group."""
    agg = defaultdict(float)
    for p in t.values():
        for cat in EXTERNAL:
            group = "equity" if cat in EQUITY else cat
            agg[group] += p[cat]
    total = sum(agg.values())
    return {k: v / total for k, v in agg.items()}, total


def plan(t):
    h1 = t["H1 2026"]
    capex_26 = sum(CAPEX_2026_GUIDE) / 2
    h2_capex = capex_26 - h1["capex"] / 1000
    rows = [{
        "year": 2026, "capex": capex_26,
        "prepay": h1["prepayment"] / 1000 + PREPAY_SHARE * h2_capex,
        "raised": sum(t[p][c] for p in ("H1 2026", "Jul–Oct 2026") for c in EXTERNAL) / 1000,
    }]
    for y, w in zip(PLAN_YEARS, PHASING):
        capex = CAPEX_2027_30 * w
        rows.append({"year": y, "capex": capex, "prepay": capex * PREPAY_SHARE, "raised": 0.0})
    for r in rows:
        r["remaining"] = r["capex"] - r["prepay"] - r["raised"]
    return rows, h2_capex


def m(x):
    return f"−${-x:,.0f}M" if x < 0 else f"${x:,.0f}M"


def b(x, d=1):
    return f"−${-x:,.{d}f}B" if x < 0 else f"${x:,.{d}f}B"


def pct_coupon(c):
    return f"{c * 100:g}%"


def write(rows):
    t = totals(rows)
    out = outstanding(rows)
    mix, mix_base = reference_mix(t)
    prow, h2_capex = plan(t)
    price = scen.VALUATION["price"]
    periods = [p for p, _, _ in PERIODS]
    L = ["# Nebius Financing: 2025–2026 Actuals and the 2026–2030 Plan", "",
         "*Generated by `models/financing_plan.py` from [`data/financing_history.csv`](../../data/financing_history.csv). "
         "Do not edit by hand.*", "",
         "> Not investment advice. 2025 and H1 2026 figures are from the 6-K filings; the August 2026 converts are from press "
         "coverage of the closing. Each row's source is in the data file.", "",
         "## 1. What Nebius raised", "",
         "| $M | " + " | ".join(periods) + " | Total |", "|---" * (len(periods) + 2) + "|"]
    for cat, label in FLOW_ROWS:
        vals = [t[p][cat] for p in periods]
        L.append(f"| {label} | " + " | ".join(m(v) if v else "—" for v in vals) + f" | {m(sum(vals))} |")
    ext = [sum(t[p][c] for c in EXTERNAL) for p in periods]
    capex = [t[p]["capex"] for p in periods]
    pre = [t[p]["prepayment"] for p in periods]
    L.append("| **Raised from investors and lenders** | " + " | ".join(f"**{m(v)}**" for v in ext) + f" | **{m(sum(ext))}** |")
    L.append("| Capex | " + " | ".join(m(v) if v else "not yet reported" for v in capex) + f" | {m(sum(capex))} |")
    L.append("| Prepayments as a share of capex | " + " | ".join(f"{p / c:.0%}" if c else "—" for p, c in zip(pre, capex))
             + f" | {sum(pre) / sum(capex):.0%} |")
    L += ["", "Not counted above:",
          "- **Note exchange (August 2026):** $800M of the June 2025 notes swapped for ~15.8M shares. No cash.",
          "- **Leases:** operating lease liabilities rose from $845M (December 2025) to $1,625M (June 2026). On top of that, "
          "**$12.1B of signed leases, mainly data centers, haven't started yet** (undiscounted, 2026–2027 start, up to 12 years). "
          "This is how Nebius gets sites without paying for the buildings. [Q2-2026 6-K F-24]",
          "- **Q4 2024:** $700M of equity sold, before this window (Q4-2025 6-K cash flow comparatives).", ""]

    L += ["## 2. Every transaction", "", "| Date | Instrument | Series / terms | $M | Shares (M) | Source |", "|---|---|---|---|---|---|"]
    for r in rows:
        if r["category"] in ("capex", "prepayment", "program", "lease", "lease_commitment"):
            continue
        shares = f"{float(r['shares_mn']):.1f}" if r["shares_mn"] else "—"
        if r["category"] == "convertible":
            shares += " if converted"
        L.append(f"| {r['date']} | {r['instrument']} | {r['series']} | {m(r['amount'])} | {shares} | {r['source_quality']} |")

    L += ["", "## 3. What's outstanding after August 2026", "",
          "| Series | Matures | Coupon | Principal | At maturity (accreted) | Conversion price | Shares if converted (M) | Annual coupon |",
          "|---|---|---|---|---|---|---|---|"]
    for s in out:
        conv = f"${s['conversion_price']:.2f}" if s["conversion_price"] else "—"
        acc = m(s["accreted"]) if s["accreted"] else ("n/a" if s["kind"] == "convertible" else "—")
        name = s["series"] if s["kind"] == "convertible" else f"Secured term loan ({s['series']})"
        shares = f"{s['shares']:.1f}" if s["shares"] else "—"
        L.append(f"| {name} | {s['maturity']} | {pct_coupon(s['coupon'])} | {m(s['principal'])} | {acc} | {conv} | "
                 f"{shares} | {m(s['coupon_cost'])} |")
    conv = [s for s in out if s["kind"] == "convertible"]
    L.append(f"| **Total** | | | **{m(sum(s['principal'] for s in out))}** | | | "
             f"**{sum(s['shares'] for s in conv):.1f}** | **{m(sum(s['coupon_cost'] for s in out))}** |")
    L += ["", f"- **Converts:** {m(sum(s['principal'] for s in conv))} of original principal across {len(conv)} series, all unsecured. "
          f"If all convert, that's ~{sum(s['shares'] for s in conv):.0f}M shares, on top of the 21.1M NVIDIA warrant shares. "
          "Several series accrete, so more is owed at maturity than was borrowed (shown where filed).",
          "- **Secured:** the $775M MUFG loan is the only secured debt.",
          "- **Coupons:** cash coupon is about "
          f"{m(sum(s['coupon_cost'] for s in out))} a year. Most of the converts' cost is the accretion and the conversion shares, not the coupon.", ""]

    L += ["## 4. The plan, 2026–2030", "",
          f"- **2026:** capex at the ${CAPEX_2026_GUIDE[0]:.0f}–{CAPEX_2026_GUIDE[1]:.0f}B guidance midpoint. H1 is actual "
          f"(${t['H1 2026']['capex'] / 1000:.1f}B of capex, ${t['H1 2026']['prepayment'] / 1000:.1f}B of prepayments); "
          f"H2 assumes prepayments fund {PREPAY_SHARE:.0%} of the remaining {b(h2_capex)}. "
          "\"Already raised\" is the money from investors and lenders this year to date. The 2026 surplus leaves out "
          "the $3.7B of cash Nebius started the year with, H2 operating costs and acquisitions ($252M in H1).",
          f"- **2027–2030:** {b(CAPEX_2027_30, 0)} of capex, spread {', '.join(f'{w:.0%}' for w in PHASING)}. "
          f"Prepayments fund {PREPAY_SHARE:.0%}.", "",
          "| $B | " + " | ".join(str(r["year"]) for r in prow) + " | 2027–30 |", "|---" * (len(prow) + 2) + "|"]
    fut = prow[1:]
    for label, key in (("Capex", "capex"), (f"Customer prepayments ({PREPAY_SHARE:.0%})", "prepay"),
                       ("Already raised", "raised"), ("**Left to fund (− = surplus)**", "remaining")):
        cells = [b(r[key]) for r in prow]
        tot = b(sum(r[key] for r in fut))
        if key == "remaining":
            cells, tot = [f"**{c}**" for c in cells], f"**{tot}**"
        L.append(f"| {label} | " + " | ".join(cells) + f" | {tot} |")
    gap = sum(r["remaining"] for r in fut)

    L += ["", f"### How the remaining {b(gap)} gets funded (2027–2030): to decide", "",
          f"Reference only: the split if Nebius keeps funding itself the way it did outside prepayments in 2025–2026 "
          f"({m(mix_base)} raised). Shares are at ${price:.2f} for equity and at a {CONVERT_PREMIUM:.0%} conversion premium "
          "for converts.", "",
          "| Instrument | 2025–26 share | 2027–30 at that share | Shares (M) |", "|---|---|---|---|"]
    labels = {"convertible": "Convertible notes", "equity": "Equity (offerings, ATM, warrants)", "secured_debt": "Secured debt"}
    for k in ("convertible", "equity", "secured_debt"):
        amt = gap * mix.get(k, 0.0)
        if k == "equity":
            sh = f"{amt * 1000 / price:,.0f}"
        elif k == "convertible":
            sh = f"{amt * 1000 / (price * (1 + CONVERT_PREMIUM)):,.0f} if converted"
        else:
            sh = "—"
        L.append(f"| {labels[k]} | {mix.get(k, 0):.0%} | {b(amt)} | {sh} |")
    L += ["", "This ignores operating cash. The revised plan below uses it."]
    rp = revised_plan(out)
    L += write_revised(rp, price)
    (OUT / "financing_plan.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return t, out, prow, mix, rp


def revised_plan(out):
    """Year-by-year sources and uses for 2027-2029. Equity and converts are the plug."""
    final = fm.steps()[-1][3]
    ebitda = fm.compute(final)["ebitda"]                    # reconciled model, $12M ARR per MW
    cash = fm.steps()[1][3]["cash_open"]                    # pro forma year-end 2026
    existing_coupons = sum(s["coupon_cost"] for s in out if s["kind"] == "convertible") / 1000
    existing_converts = sum(s["principal"] for s in out if s["kind"] == "convertible") / 1000
    tranches, conv_new, leased, shares_atm, shares_conv = [], 0.0, 0.0, 0.0, 0.0
    rows = []
    for i, y in enumerate(REVISED_YEARS):
        capex = CAPEX_2027_30 * PHASING[i]
        prepay = capex * PREPAY_SHARE
        opcash = OPCASH_SHARE * ebitda[i]
        rent = leased * LEASE_RENT_YIELD
        new_gpu_loans = SECURED_SHARE_OF_GPU * GPU_SHARE * capex
        legacy_loan = EXISTING_GPU_LOAN if i == 0 else 0.0
        drawn = new_gpu_loans + legacy_loan
        sec_open = sum(a - a * min(max(y - 1 - s, 0), SECURED_TERM) / SECURED_TERM for a, s in tranches)
        principal = sum(a / SECURED_TERM for a, s in tranches if s < y <= s + SECURED_TERM)
        interest = ((sec_open + MUFG_LOAN) * SECURED_RATE + drawn * SECURED_RATE / 2
                    + existing_coupons + conv_new * NEW_CONVERT_COUPON)
        before = cash + prepay + opcash + LEASE_FUNDED + drawn - capex - rent - interest - principal
        raised = max(0.0, MIN_CASH - before)
        equity, converts = raised * EQUITY_SHARE_OF_RAISE, raised * (1 - EQUITY_SHARE_OF_RAISE)
        price = scen.VALUATION["price"]
        shares_atm += equity * 1000 / (1 - ATM_COST) / price
        shares_conv += converts * 1000 / (price * (1 + CONVERT_PREMIUM))
        cash = before + raised
        tranches.append((drawn, y))
        conv_new += converts
        leased += LEASE_FUNDED
        sec_close = sec_open + drawn - principal
        rows.append({
            "year": y, "capex": capex, "prepay": prepay, "opcash": opcash, "lease": LEASE_FUNDED,
            "gpu_loans": new_gpu_loans, "legacy_loan": legacy_loan, "equity": equity, "converts": converts,
            "interest": interest, "principal": principal, "rent": rent, "cash": cash, "ebitda": ebitda[i],
            "secured_close": sec_close + MUFG_LOAN, "leased": leased,
            "converts_close": existing_converts - (0.1 if y >= 2029 else 0.0) + conv_new,  # Jun 2029 notes convert
            "shares_atm": shares_atm, "shares_conv": shares_conv,
        })
    return rows


def write_revised(rp, price):
    years = [r["year"] for r in rp]
    head = "| $B | " + " | ".join(str(y) for y in years) + " | 3 years |"
    sep = "|---" * (len(years) + 2) + "|"

    def line(label, key, total=True, fmt=lambda v: f"{v:,.1f}", bold=False):
        cells = [fmt(r[key]) for r in rp]
        tot = fmt(sum(r[key] for r in rp)) if total else ""
        if bold:
            label, cells, tot = f"**{label}**", [f"**{c}**" for c in cells], (f"**{tot}**" if tot else "")
        return f"| {label} | " + " | ".join(cells) + f" | {tot} |"

    last = rp[-1]
    L = ["", "## 5. Revised plan, 2027–2029", "",
         "Equity and converts fill whatever the other sources leave, keeping year-end cash at or above the floor. "
         "Everything else follows the inputs below; change them in `models/financing_plan.py`.", "",
         "| Input | Value |", "|---|---|",
         f"| Capex | {b(CAPEX_2027_30 * PHASING[0])} a year (the $270B frame) |",
         f"| Customer prepayments | {PREPAY_SHARE:.0%} of capex |",
         f"| Operating cash before interest | {OPCASH_SHARE:.0%} of EBITDA (EBITDA from the reconciled 5 GW model, $12M ARR per MW) |",
         f"| Lease-funded data centers | {b(LEASE_FUNDED)} a year, rent {LEASE_RENT_YIELD:.0%} a year from the next year |",
         f"| New GPU loans | {SECURED_SHARE_OF_GPU:.0%} of GPU capex (GPUs = {GPU_SHARE:.0%} of capex), investment-grade contracts only |",
         f"| Loan on GPUs already installed | {b(EXISTING_GPU_LOAN)} in 2027, against ~$11B of GPUs |",
         f"| Secured loan terms | {SECURED_RATE:.2%} (SOFR + 2.50%), repaid over {SECURED_TERM} years from the year after drawing |",
         f"| Minimum year-end cash | {b(MIN_CASH)} |",
         f"| Money from investors | {EQUITY_SHARE_OF_RAISE:.0%} ATM equity at ${price:.2f}, {1 - EQUITY_SHARE_OF_RAISE:.0%} converts "
         f"at a {CONVERT_PREMIUM:.0%} premium, {NEW_CONVERT_COUPON:.1%} coupon |",
         "", "### Sources and uses", "", head, sep,
         "| *Uses* | | | | |",
         line("Capex", "capex"), line("Interest (all debt)", "interest"), line("Secured loan repayments", "principal"),
         line("Rent on lease-funded data centers", "rent"),
         "| *Sources* | | | | |",
         line(f"Customer prepayments ({PREPAY_SHARE:.0%})", "prepay"),
         line(f"Operating cash ({OPCASH_SHARE:.0%} of EBITDA)", "opcash"),
         line("Lease-funded data centers", "lease"),
         line("New GPU loans (contracted capacity)", "gpu_loans"),
         line("Loan on GPUs already installed", "legacy_loan"),
         line("ATM equity", "equity", bold=True), line("Convertible notes", "converts", bold=True),
         line("Year-end cash", "cash", total=False),
         "", "### Capital stack at year-end", "", head, sep,
         line("Secured debt outstanding (incl. the $775M MUFG loan)", "secured_close", total=False),
         line("Convertible notes outstanding (principal)", "converts_close", total=False),
         line("Lease-funded data centers, cumulative", "leased", total=False),
         line("EBITDA", "ebitda", total=False)]
    L.append("| Secured debt / EBITDA | " + " | ".join(f"{r['secured_close'] / r['ebitda']:.1f}x" for r in rp) + " | |")
    L.append("| EBITDA / interest | " + " | ".join(f"{r['ebitda'] / r['interest']:.1f}x" for r in rp) + " | |")
    existing_conv_shares = 68.6
    total_new = last["shares_atm"] + last["shares_conv"]
    L += ["", "### Shares", "",
          "| M shares | End of 2029 |", "|---|---|",
          f"| Year-end 2026 (incl. NVIDIA warrants and exchange shares) | {SHARES_YE26:.1f} |",
          f"| New ATM shares | {last['shares_atm']:.1f} |",
          f"| New converts, if converted | {last['shares_conv']:.1f} |",
          f"| **New shares from this plan** | **{total_new:.1f} ({total_new / SHARES_YE26:+.0%})** |",
          f"| Existing converts, if converted | {existing_conv_shares:.1f} |",
          f"| Fully diluted | {SHARES_YE26 + total_new + existing_conv_shares:.1f} |",
          "", "**Read before using:**",
          "- **Price per MW drives everything.** EBITDA is the reconciled model's $12M ARR per MW path. Higher contract prices "
          "raise operating cash and how much the GPUs can borrow, and cut the equity needed.",
          f"- **Shares are priced at today's ${price:.2f}.** A higher share price means fewer shares for the same money, a lower one more.",
          "- **The rent is a cost the EBITDA path doesn't include,** so it's taken out separately here.",
          "- **The $100M of 2029 notes** convert at $51.45, far below today's price, so they're assumed to convert into ~1.9M "
          "shares, not be repaid in cash.",
          "- **2030 is still open:** the last $67.5B of the $270B, plus $5.0B of converts and the MUFG loan due that year."]
    return L


def write_csv(t, out, prow, mix, rp):
    with open(OUT / "financing_plan.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["section", "key", "metric", "value"])
        for p, _, _ in PERIODS:
            for cat, v in sorted(t[p].items()):
                w.writerow(["raised_usd_mn", p, cat, round(v, 2)])
        for s in out:
            for k in ("principal", "accreted", "coupon", "conversion_price", "shares", "coupon_cost"):
                w.writerow(["outstanding", s["series"], k, round(s[k], 4)])
        for r in prow:
            for k in ("capex", "prepay", "raised", "remaining"):
                w.writerow(["plan_usd_bn", r["year"], k, round(r[k], 4)])
        for k, v in sorted(mix.items()):
            w.writerow(["reference_mix", "2025-2026", k, round(v, 4)])
        for r in rp:
            for k, v in r.items():
                if k != "year":
                    w.writerow(["revised_plan_usd_bn", r["year"], k, round(v, 4)])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t, out, prow, mix, rp = write(load())
    write_csv(t, out, prow, mix, rp)
    for r in rp:
        print(f"{r['year']}  GPU loans {b(r['gpu_loans'] + r['legacy_loan']):>7}  equity {b(r['equity']):>6}  "
              f"converts {b(r['converts']):>6}  interest {b(r['interest']):>6}  cash {b(r['cash']):>6}")


if __name__ == "__main__":
    main()
