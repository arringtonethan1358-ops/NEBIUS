"""Bear / base / bull scenario model for Nebius, Q3 2026 through Q4 2027.

Reads actuals from data/nebius_kpis.csv and writes:
  models/output/scenarios.md   tables for each scenario plus the guidance check
  models/output/scenarios.csv  quarterly rows for every scenario
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
SCENARIOS = {
    "bear": {
        "gw_ye26": 0.8, "gw_ye27": 1.5,        # 2027 build slips below the >1 GW/yr plan
        "arr_per_mw": 7.5,                      # $M; pricing gains fade
        "ai_margin_q4_27": 0.45,                # AI cloud adj. EBITDA margin by Q4 2027
        "capex_per_mw_27": 32.0,                # $M per MW added in 2027
        "prepay_share": 0.35,                   # share of capex funded by customer prepayments
    },
    "base": {
        "gw_ye26": 0.9, "gw_ye27": 1.9,
        "arr_per_mw": 8.5,
        "ai_margin_q4_27": 0.52,
        "capex_per_mw_27": 30.0,
        "prepay_share": 0.50,
    },
    "bull": {
        "gw_ye26": 1.0, "gw_ye27": 2.2,
        "arr_per_mw": 9.5,                      # Oct 2026 price increases stick
        "ai_margin_q4_27": 0.57,
        "capex_per_mw_27": 28.0,
        "prepay_share": 0.55,
    },
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
        "| | Bear | Base | Bull |",
        "|---|---|---|---|",
    ]
    labels = [
        ("gw_ye26", "Connected GW, end of 2026", "{:.1f}"),
        ("gw_ye27", "Connected GW, end of 2027", "{:.1f}"),
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
        "| | Bear | Base | Bull |",
        "|---|---|---|---|",
    ]
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

    lines += ["", "### 2026 guidance check", "", "| | Bear | Base | Bull | Guidance |", "|---|---|---|---|---|"]
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
        "| Share price | " + " | ".join(s.title() for s in SCENARIOS) + " |",
        "|---|---|---|---|",
    ]
    for p in SHARED["share_prices"]:
        lines.append(f"| ${p:,.0f} | " + " | ".join(
            f"{max(t[s][1]['funding_gap'], 0) / p:,.0f}M" for s in SCENARIOS) + " |")

    lines += ["", "## ARR paths", "", "![ARR at quarter end by scenario](arr.svg)", "",
              "## Quarterly detail ($M unless noted)", ""]
    for s in SCENARIOS:
        lines += [f"**{s.title()}**", "",
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


def write_svg(results, act):
    labels = ["2026-Q1", "2026-Q2"] + QUARTERS
    series = {s: [act["arr_q1"], act["arr_q2"]] + [r["arr_end_bn"] for r in results[s]] for s in SCENARIOS}
    colors = {"bear": "#d9534f", "base": "#5b7fbf", "bull": "#3a9a5b"}
    w, h, left, right, top, bottom = 640, 320, 48, 90, 20, 40
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
    for s, vals in series.items():
        pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{colors[s]}" stroke-width="2.5"/>')
        out.append(f'<text x="{x(len(vals) - 1) + 6:.1f}" y="{y(vals[-1]) + 4:.1f}" fill="{colors[s]}">{s.title()} ${vals[-1]:.1f}B</text>')
    out.append("</svg>")
    (OUT / "arr.svg").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    act = load_actuals()
    results = {s: run(s, a, act) for s, a in SCENARIOS.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    write_markdown(results, act)
    write_csv(results)
    write_svg(results, act)
    for s in SCENARIOS:
        y26, y27 = year_totals(results[s], "2026", act), year_totals(results[s], "2027", act)
        print(f"{s:5} 2026 rev {fmt_bn(y26['group_revenue'])} ARR ${y26['arr_ye']:.2f}B | "
              f"2027 rev {fmt_bn(y27['group_revenue'])} EBITDA {fmt_bn(y27['group_ebitda'])} gap {fmt_bn(y27['funding_gap'])}")


if __name__ == "__main__":
    main()
