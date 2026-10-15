"""Nebius financing: what was raised in 2025-2026, and a frame for funding 2026-2030.

Part 1 reads data/financing_history.csv (every financing since June 2025, from the 6-K
filings) and totals it by instrument and period, then lists what is still outstanding.

Part 2 is the plan, built to be filled in step by step:
  - 2026: capex at the guidance midpoint, with H1 actuals and the financing done since.
  - 2027-2030: $270B of capex; customer prepayments fund 45% of it (taken as given).
  - The remaining 55% is left open. For reference, it is split the way Nebius funded
    itself outside prepayments in 2025-2026.

Writes models/output/financing_plan.md and financing_plan.csv.
Run from the repo root:  python models/financing_plan.py   (standard library only)
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nebius_scenarios as scen  # noqa: E402  share price

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "models" / "output"

# --- Plan inputs ($B) --------------------------------------------------------
CAPEX_2026_GUIDE = (20.0, 25.0)      # Q2 2026 guidance [PR]
CAPEX_2027_30 = 270.0                # program total, 2027-2030
PHASING = [0.25, 0.25, 0.25, 0.25]   # share of the program in each year
PREPAY_SHARE = 0.45                  # customer prepayments as a share of capex (given)
PLAN_YEARS = [2027, 2028, 2029, 2030]

# Instruments that fund the rest. None = not decided yet.
REMAINING_MIX = {"operating_cash": None, "secured_debt": None, "convertible": None, "equity": None, "leases": None}

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
          "| Instrument | 2025–26 share | 2027–30 at that share | Shares (M) | Decided |", "|---|---|---|---|---|"]
    labels = {"convertible": "Convertible notes", "equity": "Equity (offerings, ATM, warrants)", "secured_debt": "Secured debt"}
    for k in ("convertible", "equity", "secured_debt"):
        amt = gap * mix.get(k, 0.0)
        if k == "equity":
            sh = f"{amt * 1000 / price:,.0f}"
        elif k == "convertible":
            sh = f"{amt * 1000 / (price * (1 + CONVERT_PREMIUM)):,.0f} if converted"
        else:
            sh = "—"
        decided = "—" if REMAINING_MIX.get(k) is None else f"{REMAINING_MIX[k]:.0%}"
        L.append(f"| {labels[k]} | {mix.get(k, 0):.0%} | {b(amt)} | {sh} | {decided} |")
    L += ["| Operating cash flow | — | — | — | — |", "| Leases (sites someone else builds) | — | — | — | — |",
          "", "**Open choices:**",
          "1. **Operating cash flow.** How much of EBITDA goes to capex after interest and tax? That depends on price per MW "
          "(see the 5 GW funding model).",
          "2. **Secured debt.** Scale the July MUFG template to the investment-grade contracts (~$40B cited in July)?",
          "3. **Converts vs. equity.** Keep converts at ~two-thirds of outside money, or move to ATM equity and secured debt?",
          "4. **Leases.** Keep leasing data centers ($12.1B signed so far)? If so, part of the $270B never shows up as capex.",
          "5. **Does the $270B include the shell and power?** That decides whether leases reduce the capex number."]
    (OUT / "financing_plan.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return t, out, prow, mix


def write_csv(t, out, prow, mix):
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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t, out, prow, mix = write(load())
    write_csv(t, out, prow, mix)
    for r in prow:
        print(f"{r['year']}  capex {b(r['capex']):>7}  prepay {b(r['prepay']):>7}  raised {b(r['raised']):>6}  left {b(r['remaining']):>7}")


if __name__ == "__main__":
    main()
