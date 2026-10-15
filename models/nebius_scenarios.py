"""Bear / base / bull scenario model for Nebius, Q3 2026 through Q4 2027.

Reads actuals from data/nebius_kpis.csv and writes:
  models/output/scenarios.md   tables for each scenario plus the guidance check
  models/output/scenarios.csv  quarterly rows for every scenario
  models/output/summary.csv    one row per scenario: annual totals and EV multiples
  models/output/arr.svg        ARR paths by scenario

Run from the repo root:  python models/nebius_scenarios.py
Standard library only. All assumptions live in SCENARIOS and SHARED below;
change them there and re-run.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KPIS = ROOT / "data" / "nebius_kpis.csv"
OUT = ROOT / "models" / "output"

# --- Assumptions -----------------------------------------------------------
# ARR is driven by connected capacity x ARR per MW. 2026 guidance pairs
# $7-9B year-end ARR with 0.8-1.0 GW connected, i.e. ~$7-11M ARR per MW.
# Capex per MW added uses the author's all-in estimate of $50-60M per MW
# (data center + GPUs + networking); see notes/2026-10-nebius-report-draft.md.
SCENARIOS = {
    "bear": {
        "label": "Bear",
        "gw_ye26": 0.8, "gw_ye27": 1.5,        # 2027 build slips below the >1 GW/yr plan
        "arr_per_mw": 7.5,                      # $M; pricing gains fade
        "ai_margin_q4_27": 0.45,                # AI cloud adj. EBITDA margin by Q4 2027
        "capex_per_mw_27": 60.0,                # $M per MW added in 2027 (all-in)
        "prepay_share": 0.35,                   # share of capex funded by customer prepayments
    },
    "base": {
        "label": "Base",
        "gw_ye26": 0.9, "gw_ye27": 1.9,
        "arr_per_mw": 8.5,
        "ai_margin_q4_27": 0.52,
        "capex_per_mw_27": 55.0,
        "prepay_share": 0.50,
    },
    "bull": {
        "label": "Bull",
        "gw_ye26": 1.0, "gw_ye27": 2.2,
        "arr_per_mw": 9.5,                      # Oct 2026 price increases stick
        "ai_margin_q4_27": 0.57,
        "capex_per_mw_27": 50.0,
        "prepay_share": 0.55,
    },
    # Author's site-level pipeline (notes/2026-10-nebius-report-draft.md):
    # ~240 MW active + 0.3-0.6 GW finishing by YE26; +0.5-0.8 GW in 2027.
    # Uses the base case's pricing and margins so only capacity differs.
    "author": {
        "label": "Author's pipeline",
        "gw_ye26": 0.7, "gw_ye27": 1.35,
        "arr_per_mw": 8.5,
        "ai_margin_q4_27": 0.52,
        "capex_per_mw_27": 55.0,
        "prepay_share": 0.50,
    },
}
# Market inputs for valuation. Price: NBIS close on 2026-10-09 (Robinhood / Yahoo Finance).
# Balance sheet: June 30, 2026 (Q2 6-K), pro forma for the July secured facility and
# the August converts and note exchange; ignores Q3 operating cash flow and capex.
VALUATION = {
    "price": 221.33,
    "price_date": "2026-10-09 close",
    "shares_outstanding": 271.855218,   # M, Class A + B, Jun 30 [F2 F-5]
    "nvidia_warrants": 21.065936,       # M, pre-funded [F2 F-31]
    "exchange_shares": 15.8,            # M, Aug 2026 note exchange [PR]
    "cash_jun30": 9_098.1,              # $M incl. restricted cash [F2 F-7]
    "aug_converts_net": 5_681.0,        # $M net proceeds, Aug 2026: gross x 98.8% (net/gross of the earlier $4.94B / $5.0B estimate)
    "aug_converts_face": 5_750.0,       # $M, $5.0B priced + $750M options exercised in full [PR closing, Aug 24 2026]
    "secured_facility": 775.0,          # $M, Jul 2026 [F2 F-34]
    "converts_accreted": 10_041.8,      # $M principal at maturity, Jun 30 [F2 F-28]
    "converts_fair_value": 20_823.7,    # $M, Jun 30 [F2 F-29]
    "exchanged_principal": 800.0,       # $M original principal exchanged for shares, Aug 2026 [PR]
}
SHARED = {
    "capex_2026": 22_500.0,          # $M, midpoint of $20-25B guidance
    "q3_share_of_h2_arr_add": 0.4,   # H2 2026 ramp is back-end loaded (Microsoft ramps Q3-Q4)
    "non_ai_revenue_q": 7.4,         # $M per quarter: TripleTen + Avride - eliminations (Q2 2026)
    "other_segments_ebitda_q": -49.5,  # $M per quarter: Avride + TripleTen (Q2 2026)
    "share_prices": (150.0, 225.0, 300.0),  # $ per share, for the dilution sensitivity
}
GUIDE_2026 = {"revenue": (3_000.0, 3_400.0), "arr_ye": (7.0, 9.0), "margin": 0.40}
QUARTERS = ["2026-Q3", "2026-Q4", "2027-Q1", "2027-Q2", "2027-Q3", "2027-Q4"]


def load_actuals():
    vals = {}
    with open(KPIS, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                vals[(row["period"], row["metric"])] = float(row["value"])
            except ValueError:
                pass  # ranges such as guidance
    need = {
        "arr_q1": ("2026-Q1", "ai_arr"), "arr_q2": ("2026-Q2", "ai_arr"),
        "ai_rev_q2": ("2026-Q2", "ai_revenue"), "ai_ebitda_q2": ("2026-Q2", "ai_adj_ebitda"),
        "rev_q1": ("2026-Q1", "group_revenue"), "rev_q2": ("2026-Q2", "group_revenue"),
        "ebitda_q1": ("2026-Q1", "group_adj_ebitda"), "ebitda_q2": ("2026-Q2", "group_adj_ebitda"),
        "capex_q1": ("2026-Q1", "capex"), "capex_q2": ("2026-Q2", "capex"),
        "prepay_q1": ("2026-Q1", "deferred_revenue_change_cf"),
        "prepay_q2": ("2026-Q2", "deferred_revenue_change_cf"),
    }
    missing = [k for k, key in need.items() if key not in vals]
    if missing:
        raise SystemExit(f"missing actuals in {KPIS}: {missing}")
    return {k: vals[key] for k, key in need.items()}


def run(name, a, act):
    # Calibrate quarterly revenue to the ARR it implies: Q2 AI revenue / average Q1-Q2 ARR / 4.
    k = act["ai_rev_q2"] / ((act["arr_q1"] + act["arr_q2"]) / 2 * 1000 / 4)
    arr_ye26 = a["gw_ye26"] * a["arr_per_mw"]
    arr_ye27 = a["gw_ye27"] * a["arr_per_mw"]
    arr_q3 = act["arr_q2"] + SHARED["q3_share_of_h2_arr_add"] * (arr_ye26 - act["arr_q2"])
    step27 = (arr_ye27 - arr_ye26) / 4
    arr_end = [arr_q3, arr_ye26] + [arr_ye26 + step27 * i for i in range(1, 5)]

    m0 = act["ai_ebitda_q2"] / act["ai_rev_q2"]
    capex_h2_q = (SHARED["capex_2026"] - act["capex_q1"] - act["capex_q2"]) / 2
    capex_27_q = (a["gw_ye27"] - a["gw_ye26"]) * 1000 * a["capex_per_mw_27"] / 4

    rows, prev = [], act["arr_q2"]
    for i, q in enumerate(QUARTERS):
        ai_rev = k * (prev + arr_end[i]) / 2 * 1000 / 4
        margin = m0 + (a["ai_margin_q4_27"] - m0) * (i + 1) / len(QUARTERS)
        ai_ebitda = ai_rev * margin
        capex = capex_h2_q if q.startswith("2026") else capex_27_q
        prepay = capex * a["prepay_share"]
        group_ebitda = ai_ebitda + SHARED["other_segments_ebitda_q"]
        rows.append({
            "scenario": name, "quarter": q, "arr_end_bn": arr_end[i],
            "ai_revenue": ai_rev, "group_revenue": ai_rev + SHARED["non_ai_revenue_q"],
            "ai_margin": margin, "group_ebitda": group_ebitda, "capex": capex,
            "prepayments": prepay, "funding_gap": capex - prepay - group_ebitda,
        })
        prev = arr_end[i]
    return rows


def year_totals(rows, year, act):
    r = [x for x in rows if x["quarter"].startswith(year)]
    t = {f: sum(x[f] for x in r) for f in ("group_revenue", "group_ebitda", "capex", "prepayments", "funding_gap")}
    if year == "2026":  # add H1 actuals
        t["group_revenue"] += act["rev_q1"] + act["rev_q2"]
        t["group_ebitda"] += act["ebitda_q1"] + act["ebitda_q2"]
        t["capex"] += act["capex_q1"] + act["capex_q2"]
        t["prepayments"] += act["prepay_q1"] + act["prepay_q2"]
        t["funding_gap"] = t["capex"] - t["prepayments"] - t["group_ebitda"]
    t["arr_ye"] = r[-1]["arr_end_bn"]
    t["margin"] = t["group_ebitda"] / t["group_revenue"]
    return t


def fmt_bn(x):
    return f"${x / 1000:,.2f}B"


def header(first=""):
    names = [SCENARIOS[s]["label"] for s in SCENARIOS]
    return [f"| {first} | " + " | ".join(names) + " |", "|---" * (len(names) + 1) + "|"]


def enterprise_value():
    v = VALUATION
    cash = v["cash_jun30"] + v["aug_converts_net"] + v["secured_facility"]
    shares_lo = v["shares_outstanding"] + v["nvidia_warrants"] + v["exchange_shares"]
    debt_lo = v["converts_accreted"] - v["exchanged_principal"] + v["aug_converts_face"] + v["secured_facility"]
    shares_hi = v["shares_outstanding"] + v["nvidia_warrants"]
    debt_hi = v["converts_fair_value"] + v["aug_converts_face"] + v["secured_facility"]
    return v["price"] * shares_lo + debt_lo - cash, v["price"] * shares_hi + debt_hi - cash


def valuation(t):
    v = VALUATION
    cash = v["cash_jun30"] + v["aug_converts_net"] + v["secured_facility"]
    # Low: converts as debt at accreted principal; exchange shares counted.
    shares_lo = v["shares_outstanding"] + v["nvidia_warrants"] + v["exchange_shares"]
    debt_lo = v["converts_accreted"] - v["exchanged_principal"] + v["aug_converts_face"] + v["secured_facility"]
    ev_lo = v["price"] * shares_lo + debt_lo - cash
    # High: converts at June 30 fair value (prices in their conversion value); pre-exchange share count.
    shares_hi = v["shares_outstanding"] + v["nvidia_warrants"]
    debt_hi = v["converts_fair_value"] + v["aug_converts_face"] + v["secured_facility"]
    ev_hi = v["price"] * shares_hi + debt_hi - cash
    lines = [
        "", "## Valuation at the current share price", "",
        f"Share price **${v['price']:.2f}** ({v['price_date']}). Balance sheet as of June 30, 2026, pro forma for the July secured facility "
        "and the August converts and note exchange, ignoring Q3 cash burn. The two EV methods bracket how to treat the in-the-money converts:", "",
        "| | Low EV | High EV |", "|---|---|---|",
        f"| Converts treated as | debt at accreted principal; exchange shares counted | debt at June 30 fair value (includes conversion value) |",
        f"| Shares (M, incl. NVIDIA warrants) | {shares_lo:,.1f} | {shares_hi:,.1f} |",
        f"| Equity value | {fmt_bn(v['price'] * shares_lo)} | {fmt_bn(v['price'] * shares_hi)} |",
        f"| + Debt | {fmt_bn(debt_lo)} | {fmt_bn(debt_hi)} |",
        f"| − Cash (pro forma) | {fmt_bn(cash)} | {fmt_bn(cash)} |",
        f"| **Enterprise value** | **{fmt_bn(ev_lo)}** | **{fmt_bn(ev_hi)}** |",
        "", "**Implied multiples (low–high EV):**", "",
    ] + header()
    def mult(fn):
        return " | ".join(f"{ev_lo / fn(t[s]):.1f}–{ev_hi / fn(t[s]):.1f}x" for s in SCENARIOS)
    lines.append("| EV / 2026 year-end ARR | " + mult(lambda y: y[0]["arr_ye"] * 1000) + " |")
    lines.append("| EV / 2027 year-end ARR | " + mult(lambda y: y[1]["arr_ye"] * 1000) + " |")
    lines.append("| EV / 2027 adj. EBITDA | " + mult(lambda y: y[1]["group_ebitda"]) + " |")
    lines += ["",
        "For reference, CoreWeave's EV is roughly $80–93B: a ~$45B market cap plus ~$35B of debt and leases as of Q1, before cash; "
        "one data provider's EV/EBITDA implies ~$93B. Against its $18.5–19.5B year-end 2026 ARR target, that is **~4–5x EV / 2026 ARR**. "
        "All CoreWeave figures are secondary; see `research/peer-comparison.md`.",
    ]
    return lines


def write_markdown(results, act):
    lines = [
        "# Nebius Scenario Model: Output",
        "",
        "*Generated by `models/nebius_scenarios.py` from `data/nebius_kpis.csv`. Do not edit by hand; change the assumptions in the script and re-run.*",
        "",
        "> Not investment advice. This is a mechanical scenario model: every output follows from the assumptions table, not from a forecast of what Nebius will report.",
        "",
        "## Assumptions",
        "",
    ] + header()
    labels = [
        ("gw_ye26", "Live GW at end of 2026 (company 'connected' basis)", "{:.2f}"),
        ("gw_ye27", "Live GW at end of 2027", "{:.2f}"),
        ("arr_per_mw", "Year-end ARR per connected MW ($M)", "{:.1f}"),
        ("ai_margin_q4_27", "AI cloud adj. EBITDA margin by Q4 2027", "{:.0%}"),
        ("capex_per_mw_27", "2027 capex per MW added ($M)", "{:.0f}"),
        ("prepay_share", "Share of capex funded by prepayments", "{:.0%}"),
    ]
    for key, label, f in labels:
        lines.append(f"| {label} | " + " | ".join(f.format(SCENARIOS[s][key]) for s in SCENARIOS) + " |")
    lines += [
        "",
        f"Shared assumptions: 2026 capex at the guidance midpoint ({fmt_bn(SHARED['capex_2026'])}); "
        f"{SHARED['q3_share_of_h2_arr_add']:.0%} of the H2 2026 ARR increase lands by September; "
        "Avride and TripleTen held at Q2 2026 run-rates. "
        "Quarterly revenue = average of opening and closing ARR / 4, scaled by the Q2 2026 ratio of AI revenue to ARR.",
        "",
        "**Funding gap** = capex − customer prepayments − adjusted EBITDA. It is a rough measure of outside capital needed: "
        "it ignores interest, taxes and working capital (which make it larger) and existing cash (which covers part of it). "
        "2026 figures include H1 actuals.",
        "",
        "## Results",
        "",
    ] + header()
    t = {s: (year_totals(results[s], "2026", act), year_totals(results[s], "2027", act)) for s in SCENARIOS}
    def row(label, fn):
        lines.append(f"| {label} | " + " | ".join(fn(t[s]) for s in SCENARIOS) + " |")
    row("**2026** group revenue", lambda y: fmt_bn(y[0]["group_revenue"]))
    row("2026 year-end ARR", lambda y: f"${y[0]['arr_ye']:.2f}B")
    row("2026 group adj. EBITDA (margin)", lambda y: f"{fmt_bn(y[0]['group_ebitda'])} ({y[0]['margin']:.0%})")
    row("2026 capex", lambda y: fmt_bn(y[0]["capex"]))
    row("2026 funding gap (capex − prepayments − EBITDA)", lambda y: fmt_bn(y[0]["funding_gap"]))
    row("**2027** group revenue", lambda y: fmt_bn(y[1]["group_revenue"]))
    row("2027 year-end ARR", lambda y: f"${y[1]['arr_ye']:.2f}B")
    row("2027 group adj. EBITDA (margin)", lambda y: f"{fmt_bn(y[1]['group_ebitda'])} ({y[1]['margin']:.0%})")
    row("2027 capex", lambda y: fmt_bn(y[1]["capex"]))
    row("2027 prepayments", lambda y: fmt_bn(y[1]["prepayments"]))
    row("2027 funding gap", lambda y: fmt_bn(y[1]["funding_gap"]))

    h = header()
    lines += ["", "### 2026 guidance check", "", h[0] + " Guidance |", h[1] + "---|"]
    lo, hi = GUIDE_2026["revenue"]
    lines.append("| Revenue | " + " | ".join(fmt_bn(t[s][0]["group_revenue"]) for s in SCENARIOS)
                 + f" | {fmt_bn(lo)}–{fmt_bn(hi)} |")
    lo, hi = GUIDE_2026["arr_ye"]
    lines.append("| Year-end ARR | " + " | ".join(f"${t[s][0]['arr_ye']:.2f}B" for s in SCENARIOS)
                 + f" | ${lo:.0f}–{hi:.0f}B |")
    lines.append("| Adj. EBITDA margin | " + " | ".join(f"{t[s][0]['margin']:.0%}" for s in SCENARIOS)
                 + f" | ~{GUIDE_2026['margin']:.0%} |")

    lines += [
        "",
        "### What the 2027 funding gap means in shares",
        "",
        "New shares needed to fund the 2027 gap entirely with equity (in millions), at different share prices. "
        "For scale: 271.9M shares were outstanding on June 30, 2026, plus 21.1M NVIDIA pre-funded warrants. "
        "In practice part of the gap is funded with debt and convertibles, and the ~$9.1B of cash and restricted cash on hand (June 30, 2026) absorbs some of it first.",
        "",
    ] + header("Share price")
    for p in SHARED["share_prices"]:
        lines.append(f"| ${p:,.0f} | " + " | ".join(
            f"{max(t[s][1]['funding_gap'], 0) / p:,.0f}M" for s in SCENARIOS) + " |")

    lines += valuation(t)
    lines += ["", "## ARR paths", "", "![ARR at quarter end by scenario](arr.svg)", "",
              "## Quarterly detail ($M unless noted)", ""]
    for s in SCENARIOS:
        lines += [f"**{SCENARIOS[s]['label']}**", "",
                  "| Quarter | ARR end ($B) | Group revenue | AI margin | Group adj. EBITDA | Capex | Prepayments | Funding gap |",
                  "|---|---|---|---|---|---|---|---|"]
        for r in results[s]:
            lines.append(f"| {r['quarter']} | {r['arr_end_bn']:.2f} | {r['group_revenue']:,.0f} | {r['ai_margin']:.0%} | "
                         f"{r['group_ebitda']:,.0f} | {r['capex']:,.0f} | {r['prepayments']:,.0f} | {r['funding_gap']:,.0f} |")
        lines.append("")
    (OUT / "scenarios.md").write_text("\n".join(lines), encoding="utf-8")


def write_csv(results):
    fields = list(next(iter(results.values()))[0].keys())
    with open(OUT / "scenarios.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for rows in results.values():
            for r in rows:
                w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})


def write_summary(results, act):
    """One row per scenario: annual totals and EV multiples (feeds the dashboard)."""
    ev_lo, ev_hi = enterprise_value()
    fields = ["scenario", "label", "rev_2026", "arr_ye26", "ebitda_2026", "margin_2026", "rev_2027", "arr_ye27",
              "ebitda_2027", "margin_2027", "capex_2027", "gap_2027", "ev_low", "ev_high",
              "ev_arr26_low", "ev_arr26_high", "ev_ebitda27_low", "ev_ebitda27_high"]
    with open(OUT / "summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for s in SCENARIOS:
            y26, y27 = year_totals(results[s], "2026", act), year_totals(results[s], "2027", act)
            row = [s, SCENARIOS[s]["label"], y26["group_revenue"], y26["arr_ye"], y26["group_ebitda"], y26["margin"],
                   y27["group_revenue"], y27["arr_ye"], y27["group_ebitda"], y27["margin"], y27["capex"], y27["funding_gap"],
                   ev_lo, ev_hi, ev_lo / (y26["arr_ye"] * 1000), ev_hi / (y26["arr_ye"] * 1000),
                   ev_lo / y27["group_ebitda"], ev_hi / y27["group_ebitda"]]
            w.writerow([round(x, 4) if isinstance(x, float) else x for x in row])


def write_svg(results, act):
    labels = ["2026-Q1", "2026-Q2"] + QUARTERS
    series = {s: [act["arr_q1"], act["arr_q2"]] + [r["arr_end_bn"] for r in results[s]] for s in SCENARIOS}
    colors = {"bear": "#d9534f", "base": "#5b7fbf", "bull": "#3a9a5b", "author": "#9b6bd1"}
    w, h, left, right, top, bottom = 680, 320, 48, 150, 20, 40
    ymax = max(max(v) for v in series.values()) * 1.1
    x = lambda i: left + i * (w - left - right) / (len(labels) - 1)
    y = lambda v: top + (h - top - bottom) * (1 - v / ymax)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="sans-serif" font-size="11">',
           f'<title>Nebius ARR at quarter end by scenario ($B)</title>']
    for t in range(0, int(ymax) + 1, 5):
        out.append(f'<line x1="{left}" x2="{w - right}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="#888" stroke-opacity="0.3"/>')
        out.append(f'<text x="{left - 6}" y="{y(t) + 4:.1f}" text-anchor="end" fill="#888">${t}B</text>')
    for i, lab in enumerate(labels):
        out.append(f'<text x="{x(i):.1f}" y="{h - bottom + 16}" text-anchor="middle" fill="#888">{lab.replace("20", "", 1)}</text>')
    out.append(f'<line x1="{x(1):.1f}" x2="{x(1):.1f}" y1="{top}" y2="{h - bottom}" stroke="#888" stroke-dasharray="3 3"/>')
    out.append(f'<text x="{x(1) + 4:.1f}" y="{top + 10}" fill="#888">actual | scenario</text>')
    label_y, last = {}, None
    for s in sorted(series, key=lambda k: -series[k][-1]):  # top to bottom, keep labels 13px apart
        ly = y(series[s][-1]) + 4
        if last is not None and ly - last < 13:
            ly = last + 13
        label_y[s], last = ly, ly
    for s, vals in series.items():
        pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
        dash = ' stroke-dasharray="6 3"' if s == "author" else ""
        out.append(f'<polyline points="{pts}" fill="none" stroke="{colors[s]}" stroke-width="2.5"{dash}/>')
        out.append(f'<text x="{x(len(vals) - 1) + 6:.1f}" y="{label_y[s]:.1f}" fill="{colors[s]}">{SCENARIOS[s]["label"]} ${vals[-1]:.1f}B</text>')
    out.append("</svg>")
    (OUT / "arr.svg").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    act = load_actuals()
    results = {s: run(s, a, act) for s, a in SCENARIOS.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    write_markdown(results, act)
    write_csv(results)
    write_summary(results, act)
    write_svg(results, act)
    for s in SCENARIOS:
        y26, y27 = year_totals(results[s], "2026", act), year_totals(results[s], "2027", act)
        print(f"{s:6} 2026 rev {fmt_bn(y26['group_revenue'])} ARR ${y26['arr_ye']:.2f}B | "
              f"2027 rev {fmt_bn(y27['group_revenue'])} EBITDA {fmt_bn(y27['group_ebitda'])} gap {fmt_bn(y27['funding_gap'])}")


if __name__ == "__main__":
    main()
