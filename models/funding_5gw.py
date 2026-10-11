"""5 GW build funding model, 2027-2030: the author's workbook, ported and reconciled.

Source: models/source/NBIS_5GW_Funding_Model.xlsx (sheets "Debt Equity" and
"Depreciation"). compute() reproduces every formula in that workbook; cell
references are in the comments. On each run the script checks its output against
the values Excel saved in the workbook and stops if they differ, so the port
cannot drift from the spreadsheet.

The script then applies four reconciliation steps, one at a time, so each
change's effect on the 2030 outputs is visible (see notes/2026-10-funding-model-review.md):
  1. Opening balance sheet at year-end 2026, pro forma (the workbook opens 2027
     with June 30 cash, debt and shares and skips H2 2026).
  2. Pricing at contract rates: $12M ARR per MW instead of a $20-25M floor.
  3. Cash sweep: operating cash funds capex before new capital is raised.
  4. Accounting: depreciation on non-GPU and existing assets; EPS and the issue
     price use modeled shares and cash.

Writes models/output/funding_5gw.md, funding_5gw.csv (every step, every year) and
funding_sensitivity.csv (the reconciled model across a grid of ARR per MW).
Run from the repo root:  python models/funding_5gw.py   (standard library only)
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nebius_scenarios as scen  # noqa: E402  (H2 2026 bridge uses the base case)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "models" / "output"
YEARS = [2027, 2028, 2029, 2030]

# --- Workbook inputs, as received ($B unless noted) ------------------------
WORKBOOK = {
    "gw_open": 0.4,                        # B4  active GW, labeled Jun'26 A
    "gw_added": [1.15, 1.15, 1.15, 1.15],  # C5:F5
    "arr_per_mw_open": 20.0,               # B7  $M
    "arr_per_mw": [22.0, 25.0, 25.0, 25.0],  # C7:F7  "floor"
    "margin": [0.5, 0.5, 0.5, 0.5],        # C10:F10  EBITDA margin
    "cash_conversion": [0.70, 0.77, 0.79, 0.80],  # C14:F14
    "equity_slice": 0.20,                  # B64  straight equity, % of capex
    "prepay_rate": 0.45,                   # B65  prepayments, % of capex
    "program_capex": 270.0,                # B66  total 2027-30 capex
    "ebitda_to_capex": 0.15,               # B67  share of EBITDA applied to capex
    "secured_cap": 0.25,                   # B68  secured debt cap, % of capex
    "ev_ebitda": 9.5,                      # B69  drives the equity issue price
    "secured_rate": 0.075,                 # B70
    "convert_coupon": 0.01,                # B71
    "conversion_premium": 0.40,            # B55
    "debt_open": 8.5457,                   # B82  all convertible notes
    "secured_open": 0.0,                   # B83
    "cash_open": 8.0421,                   # B84
    "shares_open": 271.855,                # B85  M shares
    "gpu_share": 0.64,                     # Depreciation!B5
    "gpu_life": 5,                         # Depreciation!B6  years
    "salvage": 0.0,                        # Depreciation!B7
    "tax_rate": 0.22,                      # Depreciation!B8
    "pe": 20.0,                            # Depreciation!B39
    "eps_shares_bn": 0.3522,               # Depreciation!D38:G38 hardcoded divisor
    # Not in the workbook; zero / off reproduces it exactly.
    "nongpu_life": None,                   # years; None = non-GPU capex never depreciated
    "legacy_depreciation": 0.0,            # $B per year on assets in place at YE26
    "cash_in_equity_value": False,         # add opening cash in the EV -> equity bridge (row 78)
    "eps_on_model_shares": False,          # EPS on modeled diluted shares, not the hardcode
}

# Cached values Excel saved in the workbook (data_only read of the .xlsx).
WORKBOOK_EXPECTED = {
    "arr": [34.1, 67.5, 96.25, 125.0], "revenue": [21.05, 50.8, 81.875, 110.625],
    "ebitda": [10.525, 25.4, 40.9375, 55.3125], "interest": [0.085457, 1.4027945, 2.6978195, 3.96953825],
    "secured": [16.875, 16.875, 16.875, 15.328125], "converts": [5.17125, 2.94, 0.609375, 0.0],
    "equity": [13.5, 13.5, 13.5, 13.5], "debt_close": [30.59195, 50.40695, 67.891325, 83.21945],
    "cash_close": [13.745393, 28.0905985, 51.592779, 83.57636575],
    "issue_price": [336.3623990730352, 675.367348396931, 1019.639458419166, 1325.4685387494708],
    "shares_close": [311.99028277002424, 331.97940429336103, 345.219378372954, 355.40445603065285],
    "shares_diluted": [322.9717420834892, 346.07028251045614, 359.73714067495666, 369.9222183326555],
    "depreciation": [8.64, 17.28, 25.92, 34.56],
    "net_income": [1.4036435399999985, 5.239420289999998, 9.609350789999999, 13.090710164999999],
    "eps": [3.98535928449744, 14.876264310051102, 27.283789863713796, 37.1683991056218],
    "pe_price": [79.7071856899488, 297.525286201022, 545.675797274276, 743.367982112436],
}

# --- Reconciliation inputs --------------------------------------------------
# H2 2026 bridge from June 30 to December 31, 2026 ($B). Financing is filed or
# company-announced; operating flows come from the base case of nebius_scenarios.py.
JUL_SECURED_LOAN = 0.775        # [F2 F-34]
AUG_CONVERTS_FACE = 5.0         # [PR]
AUG_CONVERTS_NET = 4.94         # [S]
EXCHANGED_PRINCIPAL = 0.8       # [PR] Aug 2026 exchange of older notes for shares
EXCHANGE_SHARES = 15.8          # M [PR]
NVIDIA_WARRANTS = 21.065936     # M, pre-funded, $0.0001 exercise [F2 F-31]
CONVERTS_PRINCIPAL_JUN30 = 10.0418  # accreted principal [F2 F-28]
PPE_NET_JUN30 = 13.0452         # [F2 F-2]
CONTRACT_ARR_PER_MW = 12.0      # $M/MW/yr: author's 5-year tier; Microsoft deal implies $11.6-12.9M
NONGPU_LIFE = 20                # years, buildings, power and cooling (author assumption)
END_GW = 5.0                    # workbook's end point (B4 + SUM(C5:F5))


def h2_2026():
    act = scen.load_actuals()
    rows = [r for r in scen.run("base", scen.SCENARIOS["base"], act) if r["quarter"].startswith("2026")]
    return {k: sum(r[k] for r in rows) / 1000 for k in ("capex", "prepayments", "group_ebitda")}


def compute(p):
    """Mirror of the workbook. Lists are indexed 0..3 for 2027..2030."""
    o = {k: [] for k in ("gw", "arr", "revenue", "ebitda", "capex", "prepay", "opcash", "interest",
                          "ebitda_applied", "secured", "converts", "equity", "surplus", "retained",
                          "debt_open", "debt_close", "cash_close", "issue_price", "new_shares",
                          "shares_close", "potential", "shares_diluted")}
    gw_prev, arr_prev = p["gw_open"], p["gw_open"] * p["arr_per_mw_open"]   # B4, B6
    debt, cash, shares = p["debt_open"], p["cash_open"], p["shares_open"]   # C33, C45, C51
    cum_sec = cum_conv = cum_potential = 0.0
    total_added = sum(p["gw_added"])                                          # G5
    for i in range(4):
        gw = gw_prev + p["gw_added"][i]                                       # row 4
        arr = gw * p["arr_per_mw"][i]                                         # row 6
        rev = (arr_prev + arr) / 2                                            # row 8
        ebitda = rev * p["margin"][i]                                         # row 9
        capex = p["program_capex"] * p["gw_added"][i] / total_added           # row 11
        prepay = capex * p["prepay_rate"]                                     # row 12
        opcash = ebitda * p["cash_conversion"][i]                             # row 13
        interest = ((cum_sec + p["secured_open"]) * p["secured_rate"]         # row 38
                    + (cum_conv + p["debt_open"] - p["secured_open"]) * p["convert_coupon"])  # row 39
        net = opcash - interest                                               # row 16
        applied = min(p["ebitda_to_capex"] * ebitda, net)                     # row 17
        equity = p["equity_slice"] * capex                                    # row 20
        secured = max(0.0, min(capex - prepay - applied - equity, capex * p["secured_cap"]))  # row 18
        converts = max(0.0, capex - prepay - applied - equity - secured)      # row 19
        surplus = prepay + applied + secured + converts + equity - capex      # row 21
        retained = net - applied                                              # row 27
        # Valuation block rows 75-79: issue price from same-year EBITDA x multiple.
        equity_value = ebitda * p["ev_ebitda"] - debt + (cash if p["cash_in_equity_value"] else 0.0)
        price = equity_value * 1000 / shares if shares else 0.0
        new = equity * 1000 / price if price else 0.0                         # row 53
        conv_price = price * (1 + p["conversion_premium"])                    # row 58
        potential = converts * 1000 / conv_price if conv_price else 0.0       # row 59
        cum_sec += secured
        cum_conv += converts
        cum_potential += potential
        for k, v in (("gw", gw), ("arr", arr), ("revenue", rev), ("ebitda", ebitda), ("capex", capex),
                     ("prepay", prepay), ("opcash", opcash), ("interest", interest),
                     ("ebitda_applied", applied), ("secured", secured), ("converts", converts),
                     ("equity", equity), ("surplus", surplus), ("retained", retained),
                     ("debt_open", debt), ("issue_price", price), ("new_shares", new), ("potential", potential)):
            o[k].append(v)
        debt += secured + converts                                            # row 35
        cash += retained + surplus                                            # row 48
        shares += new                                                         # row 23
        o["debt_close"].append(debt)
        o["cash_close"].append(cash)
        o["shares_close"].append(shares)
        o["shares_diluted"].append(shares + cum_potential)                    # row 60
        gw_prev, arr_prev = gw, arr

    # Depreciation sheet: straight-line by vintage, GPU share of capex only.
    gpu = [c * p["gpu_share"] for c in o["capex"]]
    nongpu = [c - g for c, g in zip(o["capex"], gpu)]
    o["depreciation"], o["ebit"], o["net_income"], o["eps"], o["pe_price"] = [], [], [], [], []
    for i, year in enumerate(YEARS):
        dep = sum(gpu[v] * (1 - p["salvage"]) / p["gpu_life"]
                  for v in range(4) if YEARS[v] <= year <= YEARS[v] + p["gpu_life"] - 1)
        if p["nongpu_life"]:
            dep += sum(nongpu[v] / p["nongpu_life"] for v in range(i + 1))
        dep += p["legacy_depreciation"]
        ebit = o["ebitda"][i] - dep                                            # row 32
        ebt = ebit - o["interest"][i]                                          # row 34
        ni = ebt - max(0.0, ebt) * p["tax_rate"]                               # rows 35-36
        eps_shares = o["shares_diluted"][i] / 1000 if p["eps_on_model_shares"] else p["eps_shares_bn"]
        eps = ni / eps_shares                                                  # row 38
        for k, v in (("depreciation", dep), ("ebit", ebit), ("net_income", ni), ("eps", eps), ("pe_price", eps * p["pe"])):
            o[k].append(v)
    o["external"] = [s + c + e for s, c, e in zip(o["secured"], o["converts"], o["equity"])]
    o["dilution"] = [d / p["shares_open"] - 1 for d in o["shares_diluted"]]   # row 61
    return o


def check_against_workbook(o):
    bad = []
    for key, want in WORKBOOK_EXPECTED.items():
        for year, got, exp in zip(YEARS, o[key], want):
            if abs(got - exp) > 1e-6 * max(1.0, abs(exp)):
                bad.append(f"{key} {year}: model {got:.6f} vs workbook {exp:.6f}")
    if bad:
        raise SystemExit("Port no longer matches the workbook:\n  " + "\n  ".join(bad))


def at_price(p, arr_per_mw):
    """Flat ARR per MW, holding year-end 2026 ARR, the 5 GW end point and capex per MW fixed."""
    arr_ye26 = WORKBOOK["gw_open"] * WORKBOOK["arr_per_mw_open"]            # B6 = $8B, the guide midpoint
    capex_per_gw = WORKBOOK["program_capex"] / sum(WORKBOOK["gw_added"])     # $58.7B per GW
    gw_ye26 = arr_ye26 / arr_per_mw
    return dict(p, gw_open=gw_ye26, gw_added=[(END_GW - gw_ye26) / 4] * 4, arr_per_mw_open=arr_per_mw,
                arr_per_mw=[arr_per_mw] * 4, program_capex=capex_per_gw * (END_GW - gw_ye26))


def breakeven_price(p):
    """ARR per MW at which 2030 net income is zero (bisection)."""
    lo, hi = 1.0, 60.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if compute(at_price(p, mid))["net_income"][3] < 0 else (lo, mid)
    return (lo + hi) / 2


SENSITIVITY_PRICES = [
    (7.4, "Q4 2025 observed ($1.25B ARR / ~170 MW)"),
    (8.5, "repo base case (guidance-implied)"),
    (12.0, "5-year contracts (Microsoft ~$11.6-12.9M)"),
    (16.0, ""),
    (20.0, "workbook opening"),
    (25.0, "workbook 2028-30 floor"),
]


DISCOUNT_RATE = 0.12      # annual, for discounting 2030 value back to today (author assumption)
YEARS_TO_2030 = 4.2       # mid-October 2026 to December 2030
EXIT_MULTIPLES = (6.0, 9.5)  # EV / 2030 EBITDA: 6x for a business earning below its depreciation; 9.5x is the workbook's B69


def value_per_share(o, multiple):
    """2030 equity value per fully diluted share, and its present value today."""
    equity = o["ebitda"][3] * multiple - o["debt_close"][3] + o["cash_close"][3]
    v2030 = equity * 1000 / o["shares_diluted"][3]
    return v2030, v2030 / (1 + DISCOUNT_RATE) ** YEARS_TO_2030


def implied_price_per_mw(p, multiple, share_price):
    """ARR per MW at which the discounted 2030 value equals today's share price (bisection)."""
    lo, hi = 1.0, 60.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if value_per_share(compute(at_price(p, mid)), multiple)[1] < share_price else (lo, mid)
    return (lo + hi) / 2


def steps():
    """Cumulative reconciliation steps: (key, label, what changed, inputs)."""
    h2 = h2_2026()
    s0 = dict(WORKBOOK)
    s1 = dict(s0,
              debt_open=CONVERTS_PRINCIPAL_JUN30 - EXCHANGED_PRINCIPAL + AUG_CONVERTS_FACE + JUL_SECURED_LOAN,
              secured_open=JUL_SECURED_LOAN,
              cash_open=s0["cash_open"] + JUL_SECURED_LOAN + AUG_CONVERTS_NET
              + h2["prepayments"] + h2["group_ebitda"] - h2["capex"],
              shares_open=s0["shares_open"] + NVIDIA_WARRANTS + EXCHANGE_SHARES)
    s2 = at_price(s1, CONTRACT_ARR_PER_MW)
    gw_ye26, added = s2["gw_open"], s2["gw_added"][0]
    s3 = dict(s2, ebitda_to_capex=1.0)
    ppe_ye26 = PPE_NET_JUN30 + h2["capex"]
    legacy = ppe_ye26 * (s0["gpu_share"] / s0["gpu_life"] + (1 - s0["gpu_share"]) / NONGPU_LIFE)
    s4 = dict(s3, nongpu_life=NONGPU_LIFE, legacy_depreciation=legacy,
              cash_in_equity_value=True, eps_on_model_shares=True)
    return [
        ("workbook", "Workbook as received", "Reproduces every formula; checked against Excel's saved values.", s0),
        ("ye26_open", "1. Open at year-end 2026",
         f"Opening cash ${s1['cash_open']:.1f}B (June 30 + July loan + August converts + base-case H2 prepayments and EBITDA − H2 capex); "
         f"debt ${s1['debt_open']:.1f}B at principal, of which ${JUL_SECURED_LOAN}B secured; "
         f"{s1['shares_open']:.1f}M shares incl. NVIDIA's pre-funded warrants and the August exchange shares.", s1),
        ("contract_price", "2. Price at contract rates",
         f"${CONTRACT_ARR_PER_MW:.0f}M ARR per MW throughout. Same $8B year-end 2026 ARR, so {gw_ye26:.2f} GW live at YE26 "
         f"and {added:.2f} GW added a year to reach {END_GW:.0f} GW; capex kept at ${s2['program_capex'] / (END_GW - gw_ye26):.1f}M per MW "
         f"(${s2['program_capex']:.0f}B program).", s2),
        ("cash_sweep", "3. Cash sweep", "All operating cash after interest goes to capex (B67 = 100%) before secured debt, converts or equity.", s3),
        ("accounting", "4. Accounting fixes",
         f"Non-GPU capex depreciated over {NONGPU_LIFE} years; ${legacy:.1f}B a year on assets in place at YE26 "
         f"(${ppe_ye26:.1f}B, same GPU/non-GPU split); opening cash added to equity value for the issue price; "
         "EPS on modeled diluted shares instead of a fixed 352.2M.", s4),
    ]


def fmt(x, unit="B", d=1):
    return f"${x:,.{d}f}{unit}"


METRICS = [
    ("2030 ARR", lambda o: fmt(o["arr"][3])),
    ("2027–30 revenue", lambda o: fmt(sum(o["revenue"]))),
    ("2027–30 EBITDA", lambda o: fmt(sum(o["ebitda"]))),
    ("2027–30 capex", lambda o: fmt(sum(o["capex"]))),
    ("External capital raised", lambda o: fmt(sum(o["external"]))),
    ("  of which new equity", lambda o: fmt(sum(o["equity"]))),
    ("2030 closing debt", lambda o: fmt(o["debt_close"][3])),
    ("2030 closing cash", lambda o: fmt(o["cash_close"][3])),
    ("2030 shares, fully diluted for new converts (M)", lambda o: f"{o['shares_diluted'][3]:,.0f}"),
    ("Dilution vs opening shares", lambda o: f"{o['dilution'][3]:+.0%}"),
    ("2027 equity issue price", lambda o: fmt(o["issue_price"][0], "", 0)),
    ("2030 net income", lambda o: fmt(o["net_income"][3])),
    ("2030 EPS", lambda o: fmt(o["eps"][3], "", 2)),
    ("2030 price at 20x EPS", lambda o: fmt(o["pe_price"][3], "", 0) if o["eps"][3] > 0 else "n/m (loss)"),
]


def write_markdown(results):
    keys = [k for k, *_ in results]
    lines = [
        "# 5 GW Funding Model: Workbook vs. Reconciled",
        "",
        "*Generated by `models/funding_5gw.py` from `models/source/NBIS_5GW_Funding_Model.xlsx`. Do not edit by hand.*",
        "",
        "> Not investment advice. A mechanical model: every output follows from the inputs listed here.",
        "",
        "The first column reproduces the author's workbook exactly (the script stops if any of "
        f"{sum(len(v) for v in WORKBOOK_EXPECTED.values())} checked cells drift from Excel's saved values). "
        "Each later column adds one change on top of the previous one. "
        "The review is in [`notes/2026-10-funding-model-review.md`](../../notes/2026-10-funding-model-review.md).",
        "",
        "## 2030 outcome, step by step",
        "",
        "| | " + " | ".join(label for _, label, _, _ in [(k, l, w, o) for k, l, w, o in results]) + " |",
        "|---" * (len(results) + 1) + "|",
    ]
    for name, fn in METRICS:
        lines.append(f"| {name} | " + " | ".join(fn(o) for *_, o in results) + " |")
    lines += ["", "## What each step changes", ""]
    for _, label, what, _ in results:
        lines.append(f"- **{label}.** {what}")
    final = steps()[-1][3]
    lines += ["", "## Sensitivity: price per MW", "",
              "Reconciled model (step 4) at a flat ARR per MW. Year-end 2026 ARR stays at $8B, the build still ends at 5 GW, "
              "and capex stays at $58.7M per MW, so a lower price means more GW already live at YE26 and less left to build.", "",
              "| ARR per MW | Basis | 2030 ARR | 2030 EBITDA | 2030 net income, 5-yr GPU life | 2030 net income, 6-yr GPU life | Dilution vs YE26 shares |",
              "|---|---|---|---|---|---|---|"]
    for price, basis in SENSITIVITY_PRICES:
        o5, o6 = compute(at_price(final, price)), compute(at_price(dict(final, gpu_life=6), price))
        lines.append(f"| ${price:.1f}M | {basis} | {fmt(o5['arr'][3])} | {fmt(o5['ebitda'][3])} | "
                     f"{fmt(o5['net_income'][3])} | {fmt(o6['net_income'][3])} | {o5['dilution'][3]:+.0%} |")
    be5, be6 = breakeven_price(final), breakeven_price(dict(final, gpu_life=6))
    lines += ["", f"**Break-even:** 2030 net income turns positive at about **${be5:.1f}M of ARR per MW** with 5-year GPU lives "
              f"(${be6:.1f}M with 6-year lives). At $58.7M of capex per MW, 64% of it GPUs, a 5-year life costs "
              f"${58.7 * 0.64 / 5:.1f}M per MW a year in GPU depreciation alone, while a 50% margin on $12M of ARR earns $6.0M of EBITDA."]
    price = scen.VALUATION["price"]
    lines += ["", "## What today's share price implies", "",
              f"Value per fully diluted share in 2030 = (2030 EBITDA × multiple − debt + cash) ÷ shares, discounted to today at "
              f"{DISCOUNT_RATE:.0%} a year over {YEARS_TO_2030} years. Reconciled model (step 4). "
              "Existing converts are counted as debt at principal; if they convert instead, shares rise and debt falls, which lowers "
              "per-share value when the stock is above the conversion price. ClickHouse and other stakes (~$5 a share) are excluded. "
              f"Compare with **${price:.2f}** ({scen.VALUATION['price_date']}).", "",
              "| ARR per MW | " + " | ".join(f"2030 value at {m:g}x | Today at {m:g}x" for m in EXIT_MULTIPLES) + " |",
              "|---" * (1 + 2 * len(EXIT_MULTIPLES)) + "|"]
    for mw_price, _ in SENSITIVITY_PRICES:
        o = compute(at_price(final, mw_price))
        cells = []
        for m in EXIT_MULTIPLES:
            v, pv = value_per_share(o, m)
            cells += [fmt(v, "", 0), fmt(pv, "", 0)]
        lines.append(f"| ${mw_price:.1f}M | " + " | ".join(cells) + " |")
    implied = ", ".join(f"**${implied_price_per_mw(final, m, price):.1f}M** at {m:g}x" for m in EXIT_MULTIPLES)
    lines += ["", f"**Implied ARR per MW at ${price:.2f}:** {implied}."]
    for key, label, _, o in (results[0], results[-1]):
        lines += ["", f"## Annual detail: {label} ($B unless noted)", "",
                  "| | " + " | ".join(str(y) for y in YEARS) + " |", "|---" * 5 + "|"]
        rows = [("Live GW (year-end)", "gw", "{:.2f}"), ("ARR (year-end)", "arr", "{:.1f}"),
                ("Revenue", "revenue", "{:.1f}"), ("EBITDA", "ebitda", "{:.1f}"), ("Capex", "capex", "{:.1f}"),
                ("Prepayments", "prepay", "{:.1f}"), ("Operating cash applied to capex", "ebitda_applied", "{:.1f}"),
                ("Secured debt", "secured", "{:.1f}"), ("Convertible notes", "converts", "{:.1f}"),
                ("New equity", "equity", "{:.1f}"), ("Cash interest", "interest", "{:.2f}"),
                ("Closing debt", "debt_close", "{:.1f}"), ("Closing cash", "cash_close", "{:.1f}"),
                ("Equity issue price ($)", "issue_price", "{:,.0f}"), ("Shares, fully diluted (M)", "shares_diluted", "{:,.0f}"),
                ("Depreciation", "depreciation", "{:.1f}"), ("Net income", "net_income", "{:.1f}"), ("EPS ($)", "eps", "{:.2f}")]
        for name, k, f in rows:
            lines.append(f"| {name} | " + " | ".join(f.format(v) for v in o[k]) + " |")
    (OUT / "funding_5gw.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(results):
    fields = ["step", "year", "gw", "arr", "revenue", "ebitda", "capex", "prepay", "ebitda_applied", "secured",
              "converts", "equity", "external", "interest", "debt_close", "cash_close", "issue_price",
              "shares_diluted", "dilution", "depreciation", "net_income", "eps", "pe_price"]
    with open(OUT / "funding_5gw.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for key, _, _, o in results:
            for i, year in enumerate(YEARS):
                w.writerow([key, year] + [round(o[k][i], 4) for k in fields[2:]])


def write_sensitivity_csv(final):
    """Reconciled model at a grid of ARR per MW, plus the labelled reference, break-even and implied points."""
    price = scen.VALUATION["price"]
    points = [("reference", basis or f"${p:.0f}M", p) for p, basis in SENSITIVITY_PRICES]
    points += [("grid", "", float(p)) for p in range(6, 27) if float(p) not in {x for x, _ in SENSITIVITY_PRICES}]
    points += [("breakeven", "Break-even, 5-year GPU life", breakeven_price(final)),
               ("breakeven", "Break-even, 6-year GPU life", breakeven_price(dict(final, gpu_life=6)))]
    points += [("implied", f"Implied by ${price:.2f} at {m:g}x EBITDA", implied_price_per_mw(final, m, price))
               for m in EXIT_MULTIPLES]
    fields = ["kind", "label", "arr_per_mw", "arr_2030", "ebitda_2030", "net_income_2030_5y", "net_income_2030_6y",
              "dilution", "value_2030_6x", "value_today_6x", "value_2030_9_5x", "value_today_9_5x"]
    with open(OUT / "funding_sensitivity.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for kind, label, mw in sorted(points, key=lambda x: x[2]):
            o5, o6 = compute(at_price(final, mw)), compute(at_price(dict(final, gpu_life=6), mw))
            (v6, pv6), (v9, pv9) = (value_per_share(o5, m) for m in EXIT_MULTIPLES)
            w.writerow([kind, label] + [round(x, 4) + 0.0 for x in (mw, o5["arr"][3], o5["ebitda"][3], o5["net_income"][3],
                                                               o6["net_income"][3], o5["dilution"][3], v6, pv6, v9, pv9)])


def main():
    results = []
    for key, label, what, inputs in steps():
        o = compute(inputs)
        if key == "workbook":
            check_against_workbook(o)
        results.append((key, label, what, o))
    OUT.mkdir(parents=True, exist_ok=True)
    write_markdown(results)
    write_csv(results)
    write_sensitivity_csv(steps()[-1][3])
    for key, label, _, o in results:
        print(f"{label:28} 2030 ARR {fmt(o['arr'][3]):>8}  external {fmt(sum(o['external'])):>8}  "
              f"cash {fmt(o['cash_close'][3]):>7}  diluted {o['shares_diluted'][3]:5.0f}M  EPS {fmt(o['eps'][3], '', 2):>7}")


if __name__ == "__main__":
    main()
