"""Nebius financing: what was raised in 2025-2026, and a frame for funding 2026-2030.

Part 1 reads data/financing_history.csv (every financing since June 2025, from the 6-K
filings) and totals it by instrument and period, then lists what is still outstanding.

Part 2 is the plan, built to be filled in step by step:
  - 2026: capex at the guidance midpoint, with H1 actuals and the financing done since.
  - 2027-2030: $270B of capex; customer prepayments fund 45% of it (taken as given).
  - For reference, the remaining 55% split the way Nebius funded itself outside
    prepayments in 2025-2026.

Part 3 is the revised plan for 2027-2030, year by year: operating cash, leases, secured
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

# --- Revised plan inputs, 2027-2030 ($B unless noted) ------------------------
REVISED_YEARS = [2027, 2028, 2029, 2030]
OPCASH_SHARE = 0.60          # cash from operations before interest, as a share of EBITDA (after tax,
                             # working capital and the already-prepaid part of revenue)
LEASE_FUNDED = 8.0           # data center capex paid for by landlords (build-to-suit) each year
LEASE_RENT_YIELD = 0.08      # rent a year on lease-funded capex, starting the year after
GPU_SHARE = 0.64             # GPUs and servers as a share of capex (author's workbook)
SECURED_SHARE_OF_GPU = 0.30  # new GPU loans as a share of GPU capex; investment-grade contracts only
SECURED_RATE = 0.0638        # SOFR 3.88% + 2.50%, the July 2026 MUFG terms
SECURED_TERM = 5             # years; repaid in equal parts starting the year after drawing
EXISTING_GPU_LOAN = 5.0      # 2027 loan against the ~$11B of GPUs installed by mid-2026, less the $775M used
EXISTING_GPU_VALUE = 11.0    # GPUs and servers installed or being installed at June 30, 2026, net [Q2-2026 6-K F-23]
LEGACY_TERM = 3              # years: those GPUs are 1-2 years into a 5-year life, so a shorter loan
MIN_CASH = 10.0              # floor on year-end cash
EQUITY_SHARE_OF_RAISE = 0.50 # equity (ATM) share of the money raised from investors; the rest is converts
ATM_COST = 0.0125            # ATM commission
NEW_CONVERT_COUPON = 0.025   # coupon on new converts (recent deals: 0.50%-4.50%)
NEW_CONVERT_TERM = 5         # years to maturity for new converts
MUFG_LOAN = 0.775            # existing secured loan, repaid in cash October 2030
AUG_2030_ACCRETION = 344.81 / 313.46  # 0.50% notes due Aug 2030 repay ~110% (effective vs. initial conversion price)
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


def debt_ledger(out):
    """Existing debt at year-end 2026, one entry per instrument."""
    price = scen.VALUATION["price"]
    led = [{"name": "MUFG secured loan (SOFR + 2.50%)", "kind": "secured_existing", "amount": MUFG_LOAN, "drawn": 2026,
            "rate": SECURED_RATE, "bullet": 2030, "cash_at_maturity": MUFG_LOAN}]
    for sr in out:
        if sr["kind"] != "convertible":
            continue
        year = int(sr["maturity"][:4])
        converts = sr["conversion_price"] < price                     # in the money today -> shares
        accreted = sr["accreted"] / 1000 if sr["accreted"] else sr["principal"] / 1000 * (
            AUG_2030_ACCRETION if sr["series"].startswith("0.50%") else 1.0)
        led.append({"name": f"Convert, {sr['series']}", "kind": "convert_existing", "amount": sr["principal"] / 1000,
                    "drawn": 2025, "rate": sr["coupon"], "bullet": year, "conversion_price": sr["conversion_price"],
                    "cash_at_maturity": 0.0 if converts else accreted, "settles": "shares" if converts else "cash"})
    return led


def balance(d, y):
    """Principal outstanding at the end of year y."""
    if y < d["drawn"]:
        return 0.0
    if "term" in d:                                                    # amortizing loan
        paid = min(max(y - d["drawn"], 0), d["term"])
        return d["amount"] * (1 - paid / d["term"])
    return d["amount"] if y < d["bullet"] else 0.0


def interest_in(d, y):
    if y < d["drawn"]:
        return 0.0
    if y == d["drawn"]:
        return d["amount"] * d["rate"] / 2                             # drawn mid-year
    if "bullet" in d and y == d["bullet"]:
        return d["amount"] * d["rate"] / 2                             # repaid or converted mid-year
    return balance(d, y - 1) * d["rate"]


def repaid_in(d, y):
    """Cash principal paid in year y (conversions into shares cost no cash)."""
    if "term" in d:
        return d["amount"] / d["term"] if d["drawn"] < y <= d["drawn"] + d["term"] else 0.0
    return d.get("cash_at_maturity", d["amount"]) if y == d["bullet"] else 0.0


def revised_plan(out):
    """Year by year, 2027-2030. Equity and converts are the plug that keeps cash at the floor."""
    final = fm.steps()[-1][3]
    ebitda = fm.compute(final)["ebitda"]                    # reconciled model, $12M ARR per MW
    cash = fm.steps()[1][3]["cash_open"]                    # pro forma year-end 2026
    price = scen.VALUATION["price"]
    led = debt_ledger(out)
    leased, rows = 0.0, []
    for i, y in enumerate(REVISED_YEARS):
        capex = CAPEX_2027_30 * PHASING[i]
        prepay, opcash = capex * PREPAY_SHARE, OPCASH_SHARE * ebitda[i]
        rent = leased * LEASE_RENT_YIELD
        led.append({"name": f"GPU loan, {y} vintage", "kind": "secured_new", "amount": SECURED_SHARE_OF_GPU * GPU_SHARE * capex,
                    "drawn": y, "rate": SECURED_RATE, "term": SECURED_TERM})
        if i == 0 and EXISTING_GPU_LOAN:
            led.append({"name": "Loan on GPUs already installed", "kind": "secured_legacy", "amount": EXISTING_GPU_LOAN,
                        "drawn": y, "rate": SECURED_RATE, "term": LEGACY_TERM})
        drawn = sum(d["amount"] for d in led if d["drawn"] == y)
        interest = sum(interest_in(d, y) for d in led)
        repaid = sum(repaid_in(d, y) for d in led)
        before = cash + prepay + opcash + LEASE_FUNDED + drawn - capex - rent - interest - repaid
        # New converts pay half a year's coupon in the year they're issued, so solve for the raise that
        # still leaves cash exactly at the floor.
        conv_share = 1 - EQUITY_SHARE_OF_RAISE
        raised = max(0.0, (MIN_CASH - before) / (1 - conv_share * NEW_CONVERT_COUPON / 2))
        equity, converts = raised * EQUITY_SHARE_OF_RAISE, raised * conv_share
        if converts:
            conv = {"name": f"Convert, {y} issue", "kind": "convert_new", "amount": converts, "drawn": y,
                    "rate": NEW_CONVERT_COUPON, "bullet": y + NEW_CONVERT_TERM,
                    "conversion_price": price * (1 + CONVERT_PREMIUM)}
            led.append(conv)
            interest += interest_in(conv, y)
        cash = before + raised - (interest_in(conv, y) if converts else 0.0)
        leased += LEASE_FUNDED
        atm_gross = equity / (1 - ATM_COST)
        rows.append({
            "year": y, "capex": capex, "prepay": prepay, "opcash": opcash, "lease": LEASE_FUNDED, "rent": rent,
            "gpu_loans": sum(d["amount"] for d in led if d["kind"] == "secured_new" and d["drawn"] == y),
            "legacy_loan": EXISTING_GPU_LOAN if i == 0 else 0.0,
            "equity": equity, "atm_gross": atm_gross, "atm_fee": atm_gross - equity, "atm_shares": atm_gross * 1000 / price,
            "converts": converts, "interest": interest, "repaid": repaid, "cash": cash, "ebitda": ebitda[i],
        })
    return rows, led


def write_revised(plan_out, price):
    rp, led = plan_out
    years = [r["year"] for r in rp]
    yrs = " | ".join(str(y) for y in years)
    n = len(years)

    def table(rows_, total=True, first="$B", dec=1):
        L = [f"| {first} | {yrs} |" + (" Total |" if total else ""), "|---" * (n + 1 + (1 if total else 0)) + "|"]
        for label, vals, bold in rows_:
            cells = [f"{v:,.{dec}f}" if round(v, dec) else "—" for v in vals]
            tot = f"{sum(vals):,.{dec}f}" if total else None
            if bold:
                label, cells = f"**{label}**", [f"**{c}**" for c in cells]
                tot = f"**{tot}**" if tot else None
            L.append(f"| {label} | " + " | ".join(cells) + (f" | {tot} |" if total else " |"))
        return L

    pick = lambda kind: [d for d in led if d["kind"] == kind]
    L = ["", f"## 5. Money to raise, {years[0]}–{years[-1]}", ""]
    raise_rows = [("New GPU loans (contracted capacity)", [r["gpu_loans"] for r in rp], False),
                  ("Loan on GPUs already installed", [r["legacy_loan"] for r in rp], False),
                  ("ATM equity (net)", [r["equity"] for r in rp], False),
                  ("Convertible notes", [r["converts"] for r in rp], False)]
    raise_rows.append(("Total to raise", [sum(v[i] for _, v, _ in raise_rows) for i in range(n)], True))
    L += table(raise_rows)

    # --- Convertible notes
    new_conv = pick("convert_new")
    L += ["", "### Convertible notes to issue", "",
          "| Issue | Amount | Coupon | Conversion price | Matures | Shares if converted (M) | Coupon a year |",
          "|---|---|---|---|---|---|---|"]
    for d in new_conv:
        L.append(f"| {d['drawn']} | {b(d['amount'])} | {pct_coupon(d['rate'])} | ${d['conversion_price']:.2f} "
                 f"({CONVERT_PREMIUM:.0%} over ${price:.2f}) | {d['bullet']} | {d['amount'] * 1000 / d['conversion_price']:.1f} | "
                 f"{b(d['amount'] * d['rate'], 2)} |")
    tc = sum(d["amount"] for d in new_conv)
    L.append(f"| **Total** | **{b(tc)}** | | | | **{sum(d['amount'] * 1000 / d['conversion_price'] for d in new_conv):.1f}** | "
             f"**{b(sum(d['amount'] * d['rate'] for d in new_conv), 2)}** |")
    L += ["", "Unsecured, like the existing eight series. If the stock is above the conversion price at maturity they "
          "become shares; if not, Nebius repays them in cash."]

    # --- ATM
    L += ["", "### ATM equity", "",
          "| | " + yrs + " | Total |", "|---" * (n + 2) + "|"]
    for label, key, f in (("Net proceeds ($B)", "equity", "{:,.1f}"), ("Gross sales ($B)", "atm_gross", "{:,.1f}"),
                          ("Commission at 1.25% ($B)", "atm_fee", "{:,.2f}"), ("Shares sold (M)", "atm_shares", "{:,.1f}")):
        vals = [r[key] for r in rp]
        L.append(f"| {label} | " + " | ".join(f.format(v) for v in vals) + f" | {f.format(sum(vals))} |")
    L += ["", f"Shares priced at today's ${price:.2f}. The current program has ~12.3M shares left, about ${12.27 * price / 1000:.1f}B, "
          "so 2027 needs a new program on top of it."]

    # --- Loan on GPUs already installed
    leg = pick("secured_legacy")
    if leg:
        d = leg[0]
        L += ["", "### Loan on GPUs already installed", "",
              f"- **Amount:** {b(d['amount'])}, drawn {d['drawn']}, against the ~{b(EXISTING_GPU_VALUE, 0)} of GPUs and servers "
              "on the books at June 30, 2026. Part of that already backs the $775M MUFG loan; on the ~$10B left, "
              f"{b(d['amount'])} is a ~{d['amount'] / (EXISTING_GPU_VALUE - MUFG_LOAN):.0%} advance.",
              f"- **Rate:** {d['rate']:.2%} (SOFR 3.88% + 2.50%, the MUFG terms), floating.",
              f"- **Repayment:** equal parts over {d['term']} years from {d['drawn'] + 1}. Shorter than the new loans, because "
              "these GPUs are already 1–2 years old.",
              "- **Collateral:** the installed GPUs and the customer contracts they serve.", ""]
        L += table([("Drawn", [d["amount"] if y == d["drawn"] else 0.0 for y in years], False),
                    ("Repaid", [repaid_in(d, y) for y in years], False),
                    ("Interest", [interest_in(d, y) for y in years], False),
                    ("Balance at year-end", [balance(d, y) for y in years], True)], total=False, dec=2)

    # --- New GPU loans
    new_sec = pick("secured_new")
    L += ["", "### New GPU loans (contracted capacity)", "",
          f"- **Size:** {SECURED_SHARE_OF_GPU:.0%} of each year's GPU capex (GPUs are {GPU_SHARE:.0%} of capex), only on capacity "
          "with a signed investment-grade contract.",
          f"- **Rate:** {SECURED_RATE:.2%} (SOFR + 2.50%), floating.",
          f"- **Repayment:** equal parts over {SECURED_TERM} years, starting the year after each draw.",
          "- **Structure:** one ring-fenced subsidiary per contract, like the July 2026 MUFG loan.", "",
          "Balance at year-end by vintage ($B):", ""]
    L += table([(d["name"].replace("GPU loan, ", "").replace(" vintage", " loans"), [balance(d, y) for y in years], False)
                for d in new_sec] +
               [("Total balance", [sum(balance(d, y) for d in new_sec) for y in years], True)], total=False)
    L += [""]
    L += table([("Drawn", [sum(d["amount"] for d in new_sec if d["drawn"] == y) for y in years], False),
                ("Repaid", [sum(repaid_in(d, y) for d in new_sec) for y in years], False),
                ("Interest", [sum(interest_in(d, y) for d in new_sec) for y in years], False)], dec=2)

    # --- All debt
    groups = [("MUFG secured loan", "secured_existing"), ("Loan on GPUs already installed", "secured_legacy"),
              ("New GPU loans", "secured_new"), ("Existing converts (8 series)", "convert_existing"),
              ("New converts", "convert_new")]
    L += ["", "## 6. Debt", "", "### Outstanding at year-end ($B principal)", "",
          f"| | 2026 | {yrs} |", "|---" * (n + 2) + "|"]
    for label, kind in groups:
        vals = [sum(balance(d, y) for d in pick(kind)) for y in [2026] + years]
        L.append(f"| {label} | " + " | ".join(f"{v:,.1f}" if v else "—" for v in vals) + " |")
    sec = [sum(balance(d, y) for d in led if d["kind"].startswith("secured")) for y in [2026] + years]
    unsec = [sum(balance(d, y) for d in led if d["kind"].startswith("convert")) for y in [2026] + years]
    L.append("| Secured | " + " | ".join(f"{v:,.1f}" for v in sec) + " |")
    L.append("| Unsecured | " + " | ".join(f"{v:,.1f}" for v in unsec) + " |")
    L.append("| **Total debt** | " + " | ".join(f"**{a + c:,.1f}**" for a, c in zip(sec, unsec)) + " |")
    L.append("| Secured / EBITDA | — | " + " | ".join(f"{sec[i + 1] / r['ebitda']:.1f}x" for i, r in enumerate(rp)) + " |")
    L.append("| Total debt / EBITDA | — | " + " | ".join(f"{(sec[i + 1] + unsec[i + 1]) / r['ebitda']:.1f}x" for i, r in enumerate(rp)) + " |")

    L += ["", "### Interest by instrument ($B)", ""]
    L += table([(label, [sum(interest_in(d, y) for d in pick(kind)) for y in years], False) for label, kind in groups] +
               [("Total interest", [sum(interest_in(d, y) for d in led) for y in years], True)], dec=2)
    L.append("| EBITDA / interest | " + " | ".join(f"{r['ebitda'] / sum(interest_in(d, r['year']) for d in led):.1f}x" for r in rp) + " | |")

    L += ["", "### Principal paid in cash ($B)", ""]
    L += table([(label, [sum(repaid_in(d, y) for d in pick(kind)) for y in years], False) for label, kind in groups] +
               [("Total", [sum(repaid_in(d, y) for d in led) for y in years], True)], dec=2)
    L += ["", "Converts that are in the money at maturity turn into shares and cost no cash: the June 2029 notes "
          "($51.45) and September 2030 notes ($138.75). The August 2030 notes convert at $313.46, above today's price, "
          f"so they're repaid in cash at ~{AUG_2030_ACCRETION:.0%} of principal."]

    after = defaultdict(lambda: [0.0, 0.0])
    last = years[-1]
    for d in led:
        if "term" in d:
            for y in range(last + 1, d["drawn"] + d["term"] + 1):
                after[y][0] += d["amount"] / d["term"]
        elif d["bullet"] > last:
            after[d["bullet"]][1] += d["amount"]
    L += ["", f"### Due after {last} ($B principal)", "", "| Year | Secured repayments | Converts maturing |", "|---|---|---|"]
    for y in sorted(after):
        L.append(f"| {y} | {after[y][0]:,.1f} | {after[y][1]:,.1f} |" if after[y][1] else f"| {y} | {after[y][0]:,.1f} | — |")
    L.append(f"| **Total** | **{sum(v[0] for v in after.values()):,.1f}** | **{sum(v[1] for v in after.values()):,.1f}** |")
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
        rows_, led = rp
        for r in rows_:
            for k, v in r.items():
                if k != "year":
                    w.writerow(["revised_plan_usd_bn", r["year"], k, round(v, 4)])
        for d in led:
            for y in [2026] + REVISED_YEARS:
                w.writerow(["debt_balance_usd_bn", f"{d['name']} | {y}", d["kind"], round(balance(d, y), 4)])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t, out, prow, mix, rp = write(load())
    write_csv(t, out, prow, mix, rp)
    for r in rp[0]:
        print(f"{r['year']}  GPU loans {b(r['gpu_loans'] + r['legacy_loan']):>7}  equity {b(r['equity']):>6}  "
              f"converts {b(r['converts']):>6}  interest {b(r['interest']):>6}  cash {b(r['cash']):>6}")


if __name__ == "__main__":
    main()
