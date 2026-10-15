"""Debt structure for the 5 GW build: fund each kind of contract with the cheapest capital it can carry.

Nebius.MD (the author's running notes, folded into research/nebius-initiation.md section 7)
prices capacity in three tiers: short-term and auction deals at $40-50M of annual revenue
per MW, core 1-3 year deals at $20-25M, and 5-year hyperscaler deals at ~$12M. Today the
build is funded mostly with customer prepayments, unsecured converts and equity, whatever
the contract behind the capacity. This model splits the funding by tier instead:

  A. Contract-backed GPU term loans for investment-grade 5-year contracts
     (the July 2026 MUFG facility: SOFR + 2.50%, secured by GPUs and an IG contract).
  B. Delayed-draw term loans for 1-3 year contracts, tenor matched to the contract
     (CoreWeave's non-IG DDTLs: SOFR + 4.50-5.50%).
  C. Sale-leaseback of the powered shell (buildings, power, cooling) to infrastructure
     capital, which then rents it back (Meta/Blue Owl Hyperion, QTS/Microsoft).
  D. Equity and converts only for what lenders won't fund: the equity slice, reserve
     accounts and short-term/auction capacity.

For each tier it computes, per MW: sources and uses, debt sized to a minimum DSCR, the
equity check, equity IRR over the GPU's life, and the contract price needed for a 12%
equity return. It compares this with today's funding (prepayments plus equity and converts,
shell owned). Then it scales both to the 2027-2030 build in the reconciled funding model
and writes an annual debt schedule.

Writes models/output/debt_structure.md and debt_structure.csv.
Run from the repo root:  python models/debt_structure.py   (standard library only)
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import funding_5gw as fm          # noqa: E402  capex per MW, GPU share, reconciled build, YE26 shares
import nebius_scenarios as scen   # noqa: E402  share price

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "models" / "output"

# --- Cost and operating inputs -------------------------------------------
CAPEX_PER_MW = fm.WORKBOOK["program_capex"] / sum(fm.WORKBOOK["gw_added"])  # $58.7M, workbook B66 / G5
GPU_SHARE = fm.WORKBOOK["gpu_share"]                                         # 64%, Depreciation!B5
GPU_CAPEX = CAPEX_PER_MW * GPU_SHARE
SHELL_CAPEX = CAPEX_PER_MW - GPU_CAPEX


def gpu_economics():
    with open(ROOT / "data" / "gpu_economics.csv", newline="", encoding="utf-8") as f:
        return {r["gpu"]: r for r in csv.DictReader(f)}


_B200 = gpu_economics()["B200"]
GPUS_PER_MW = GPU_CAPEX * 1e6 / (float(_B200["server_cost"]) / int(_B200["gpus_per_server"]))
OPEX_PER_MW = GPUS_PER_MW * float(_B200["power_ops_per_yr"]) / 1e6  # $M/MW/yr, power and site operations
SOFR = float(_B200["interest_rate"]) - 0.025                          # 3.88%; the file stores SOFR + 2.50%

GPU_LIFE = fm.WORKBOOK["gpu_life"]   # 5 years: every vintage is evaluated over this horizon
GPU_RESIDUAL = 0.15                  # GPU resale/re-use value at year 5, share of cost (author assumption)
RECONTRACT_ARR = 12.0                # $M/MW once a short contract ends: scarcity pricing assumed gone
SHELL_LIFE = fm.NONGPU_LIFE          # 20 years
COST_OF_EQUITY = fm.DISCOUNT_RATE    # 12%, the repo's discount rate

# --- Structure inputs ----------------------------------------------------
ADVANCE_CAP = 0.95        # debt + prepayment <= 95% of GPU capex (IREN: financing + Microsoft prepayment = 95%)
SHELL_RENT_YIELD = 0.08   # annual rent / shell cost on a sale-leaseback; Hyperion ~6.6%, QTS 7.23% with
                          # hyperscaler tenants, so ~8% for Nebius as an unrated tenant (assumption)
DSRA_MONTHS = 6           # debt service reserve, funded at close, released at maturity

TIERS = {
    "hyperscaler": {
        "label": "Hyperscaler, 5-year", "who": "Microsoft, Meta (investment grade)",
        "arr": 12.0, "term": 5, "prepay": 0.20,
        "tranche": "A. Contract-backed GPU term loan", "rate": SOFR + 0.025, "dscr": 1.25,
        "rate_basis": "SOFR + 2.50% (Nebius/MUFG, July 2026)",
    },
    "mid": {
        "label": "Core, 1–3 year", "who": "AI labs, enterprises (mostly unrated)",
        "arr": 22.5, "term": 3, "prepay": 0.10,
        "tranche": "B. Delayed-draw term loan, tenor = contract", "rate": 0.1044, "dscr": 1.35,
        "rate_basis": "SOFR + 5.50% at 97, 10.44% yield (CoreWeave DDTL 5.5, Aug 2026)",
    },
    "short": {
        "label": "Short-term and auction", "who": "Spot and premium buyers",
        "arr": 40.0, "term": 1, "prepay": 0.0,
        "tranche": "D. Equity / converts (no term debt on uncontracted cash flow)", "rate": None, "dscr": None,
        "rate_basis": "—",
    },
}

MIXES = [  # share of new MW by tier: hyperscaler, mid, short
    ("all_hyperscaler", "All hyperscaler (reconciled funding model)", (1.0, 0.0, 0.0)),
    ("base", "Base mix", (0.60, 0.30, 0.10)),
    ("core_heavy", "Core-heavy", (0.40, 0.45, 0.15)),
]
SENSITIVITY = [  # (label, overrides) for the hyperscaler tier
    ("Base inputs", {}),
    ("Power and operations $3.0M per MW (vs $1.87M)", {"opex": 3.0}),
    ("Project margin 50%, the AI cloud segment's (opex $6.0M per MW)", {"opex": 6.0}),
    ("GPU residual 0% (vs 15%)", {"residual": 0.0}),
    ("GPU residual 30%", {"residual": 0.30}),
    ("Shell rent yield 9.5% (vs 8%)", {"rent_yield": 0.095}),
    ("GPU loan at SOFR + 5.50% instead of + 2.50%", {"rate": SOFR + 0.055}),
    ("Prepayment 10% of contract value (vs 20%)", {"prepay_share": 0.10}),
    ("Prepayment 44% of contract value (the workbook's 45% of capex)", {"prepay_share": 0.44}),
]
IG_CONTRACTED = 40.0  # $B of IG contracted revenue Nebius cited as available to finance (July 2026)


# --- Finance helpers -------------------------------------------------------
def annuity_factor(rate, years):
    return (1 - (1 + rate) ** -years) / rate


def npv(rate, flows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def irr(flows):
    lo, hi = -0.99, 5.0
    if npv(lo + 1e-9, flows) * npv(hi, flows) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if npv(mid, flows) > 0 else (lo, mid)
    return (lo + hi) / 2


def vintage(tier, structure, arr=None, opex=None, residual=None, rent_yield=None, rate=None, prepay_share=None):
    """One MW built at t=0 and run for GPU_LIFE years. structure: 'current' or 'proposed'.

    current:  prepayment, then equity/converts for the rest; Nebius owns the shell.
    proposed: prepayment, a GPU loan sized to the contract (tenor = contract), the shell sold
              and leased back, equity for the remainder plus the reserve account.
    """
    t = TIERS[tier]
    arr = t["arr"] if arr is None else arr
    opex = OPEX_PER_MW if opex is None else opex
    residual = GPU_RESIDUAL if residual is None else residual
    rent_yield = SHELL_RENT_YIELD if rent_yield is None else rent_yield
    term = t["term"]
    prepay = (t["prepay"] if prepay_share is None else prepay_share) * arr * term
    # Year-by-year cash EBITDA: the contract, then re-contracting at RECONTRACT_ARR.
    rev = [arr if y < term else RECONTRACT_ARR for y in range(GPU_LIFE)]
    cash_ebitda = [r - opex - (prepay / term if y < term else 0.0) for y, r in enumerate(rev)]
    proposed = structure == "proposed"
    rent = SHELL_CAPEX * rent_yield if proposed else 0.0
    cfads = [c - rent for c in cash_ebitda]
    debt = ds = dsra = 0.0
    rate = (t["rate"] if rate is None else rate) if proposed and t["rate"] else None
    if rate:
        af = annuity_factor(rate, term)
        contract_cfads = min(cfads[:term])
        debt = max(0.0, min(contract_cfads / t["dscr"] * af, ADVANCE_CAP * GPU_CAPEX - prepay))
        ds = debt / af
        dsra = ds * DSRA_MONTHS / 12
    shell_sale = SHELL_CAPEX if proposed else 0.0
    equity = CAPEX_PER_MW - prepay - debt - shell_sale + dsra
    flows = [-equity] + [cfads[y] - (ds if y < term else 0.0) for y in range(GPU_LIFE)]
    flows[term] += dsra                                                   # reserve released at maturity
    flows[-1] += GPU_CAPEX * residual
    if not proposed:
        flows[-1] += SHELL_CAPEX * (1 - GPU_LIFE / SHELL_LIFE)             # shell book value kept
    # Cost of capital on the $58.7M: prepayment free, debt at its rate, lease at its yield, equity at 12%.
    wacc = (debt * (rate or 0) + shell_sale * rent_yield + equity * COST_OF_EQUITY) / CAPEX_PER_MW
    return {
        "tier": tier, "structure": structure, "arr": arr, "capex": CAPEX_PER_MW, "prepay": prepay,
        "debt": debt, "shell_sale": shell_sale, "equity": equity, "dsra": dsra, "rent": rent,
        "ebitda": arr - opex, "cfads": cfads[0], "debt_service": ds,
        "dscr": cfads[0] / ds if ds else None, "rate": rate, "wacc": wacc,
        "irr": irr(flows), "npv": npv(COST_OF_EQUITY, flows), "flows": flows,
    }


def required_arr(tier, structure, **over):
    """Contract price per MW at which the equity NPV at 12% is zero (bisection)."""
    lo, hi = 1.0, 80.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if vintage(tier, structure, mid, **over)["npv"] < 0 else (lo, mid)
    return (lo + hi) / 2


# --- Program: the 2027-2030 build -----------------------------------------
def build_plan():
    """GW added per year in the reconciled funding model (step 2 onwards: $12M per MW, ending at 5 GW)."""
    s2 = [s for k, _, _, s in fm.steps() if k == "contract_price"][0]
    return s2["gw_added"], s2["shares_open"]


def program(mix, structure):
    gw_added, _ = build_plan()
    total_gw = sum(gw_added)
    out = {k: 0.0 for k in ("capex", "prepay", "debt", "shell_sale", "equity", "dsra", "rent", "ig_tcv", "ebitda")}
    for share, tier in zip(mix, TIERS):
        v = vintage(tier, structure)
        gw = total_gw * share
        for k in ("capex", "prepay", "debt", "shell_sale", "equity", "dsra", "rent", "ebitda"):
            out[k] += v[k] * gw          # $M per MW x GW = $B
        if tier == "hyperscaler":
            out["ig_tcv"] += TIERS[tier]["arr"] * TIERS[tier]["term"] * gw
    out["gw"] = total_gw
    return out


def schedule(mix):
    """Annual secured-debt schedule, proposed structure. A vintage is built and drawn in year y,
    earns from y+1 and amortizes over its contract. $B."""
    gw_added, _ = build_plan()
    years = list(range(fm.YEARS[0], fm.YEARS[-1] + max(t["term"] for t in TIERS.values()) + 1))
    rows = {y: {"drawn": 0.0, "interest": 0.0, "principal": 0.0, "cfads": 0.0, "rent": 0.0, "closing": 0.0}
            for y in years}
    for i, build_year in enumerate(fm.YEARS):
        for share, tier in zip(mix, TIERS):
            gw = gw_added[i] * share
            v = vintage(tier, "proposed")
            t = TIERS[tier]
            bal = v["debt"] * gw
            rows[build_year]["drawn"] += bal
            for k in range(GPU_LIFE):
                y = build_year + 1 + k
                if y not in rows:
                    continue
                rows[y]["rent"] += v["rent"] * gw
                rev = t["arr"] if k < t["term"] else RECONTRACT_ARR
                prepay_release = v["prepay"] / t["term"] if k < t["term"] else 0.0
                rows[y]["cfads"] += (rev - OPEX_PER_MW - prepay_release - v["rent"]) * gw
                if k < t["term"] and bal > 0:
                    interest = bal * t["rate"]
                    principal = v["debt_service"] * gw - interest
                    rows[y]["interest"] += interest
                    rows[y]["principal"] += principal
                    bal -= principal
    closing = 0.0
    for y in years:
        r = rows[y]
        closing += r["drawn"] - r["principal"]
        r["closing"] = max(0.0, closing)
        r["debt_service"] = r["interest"] + r["principal"]
        r["dscr"] = r["cfads"] / r["debt_service"] if r["debt_service"] else None
    return years, rows


# --- Output ------------------------------------------------------------------
def m(x, d=1):
    return f"${x:,.{d}f}M"


def b(x, d=1):
    return f"${x:,.{d}f}B"


def pct(x):
    return "n/m" if x is None else f"{x:.1%}"


TERM_SHEET = [
    ("Borrower", "One ring-fenced subsidiary per contract or site pool (template: Nebius Compute II, LLC / Oy)",
     "Ring-fenced subsidiary per contract pool", "Infrastructure partner's JV / property company", "Nebius Group N.V."),
    ("Collateral", "GPUs, assignment of the customer contract, project accounts", "GPUs, contracts, accounts",
     "The land, building and power equipment", "Unsecured"),
    ("Tenor", "Equal to the contract (5 years); fully amortizing", "Equal to the contract (1–3 years); fully amortizing",
     "15–20 year lease, renewal options", "2030–2034 (existing notes)"),
    ("Sizing", f"Lower of {TIERS['hyperscaler']['dscr']:.2f}x DSCR on contract cash flow and "
     f"{ADVANCE_CAP:.0%} of GPU cost less prepayment", f"Lower of {TIERS['mid']['dscr']:.2f}x DSCR and the same "
     f"{ADVANCE_CAP:.0%} cap", "100% of shell cost", "Residual"),
    ("Pricing", TIERS["hyperscaler"]["rate_basis"], TIERS["mid"]["rate_basis"],
     f"~{SHELL_RENT_YIELD:.0%} rent yield (assumption; Hyperion ~6.6%, QTS 7.23%)",
     "0.50% (2030) / 4.50% (2034) coupons, 40–45% conversion premium (Aug 2026)"),
    ("Covenants", f"Min DSCR, {DSRA_MONTHS}-month debt service reserve, distribution lock-up below 1.15x, parent liquidity",
     "Same, plus a cash sweep if the contract isn't renewed 6 months before maturity",
     "Rent ranks ahead of GPU debt at the site; Nebius parent guarantee", "None beyond indenture"),
    ("Precedents", "Nebius $775M (Jul 2026); CoreWeave DDTL 4.0, SOFR + 2.25%, A3; IREN $3.6B at ~5.9%",
     "CoreWeave DDTL 5.0 (SOFR + 4.50%) and 5.5 (SOFR + 5.50%)", "Meta/Blue Owl Hyperion (80/20, A+); QTS $3.9B at 7.23%",
     "Nebius converts, Mar and Aug 2026"),
]


def write_markdown():
    tiers = list(TIERS)
    cur = {k: vintage(k, "current") for k in tiers}
    pro = {k: vintage(k, "proposed") for k in tiers}
    gw_added, shares_ye26 = build_plan()
    price = scen.VALUATION["price"]
    L = [
        "# Debt Structure for the 5 GW Build",
        "",
        "*Generated by `models/debt_structure.py`. Do not edit by hand. The argument is in "
        "[`research/debt-structure.md`](../../research/debt-structure.md).*",
        "",
        "> Not investment advice. A mechanical model: every output follows from the inputs listed here.",
        "",
        "## Inputs",
        "",
        "| Input | Value | Source |",
        "|---|---|---|",
        f"| Capex per MW | {m(CAPEX_PER_MW)} (GPUs {m(GPU_CAPEX)}, shell {m(SHELL_CAPEX)}) | Author's workbook, $270B / 4.6 GW, 64% GPUs |",
        f"| Power and site operations | {m(OPEX_PER_MW, 2)} per MW a year | `data/gpu_economics.csv`: B200 $2,800 per GPU a year × {GPUS_PER_MW:,.0f} GPUs per MW (GPU capex ÷ $56,250 per GPU) |",
        f"| SOFR | {SOFR:.2%} | `data/gpu_economics.csv` |",
        f"| GPU life, residual value | {GPU_LIFE} years, {GPU_RESIDUAL:.0%} of cost | Workbook life; residual is an assumption |",
        f"| Price after a short contract ends | {m(RECONTRACT_ARR)} per MW | Assumption: scarcity pricing gone, back to the 5-year rate |",
        f"| Cost of equity | {COST_OF_EQUITY:.0%} | Repo discount rate |",
        f"| Debt + prepayment cap | {ADVANCE_CAP:.0%} of GPU cost | IREN/Microsoft financing |",
        f"| Shell sale-leaseback rent | {SHELL_RENT_YIELD:.0%} of shell cost a year | Assumption, see term sheet |",
        "",
        "| Tier | Customers | Price per MW a year | Contract | Prepayment (share of contract value) | Tranche |",
        "|---|---|---|---|---|---|",
    ]
    for k in tiers:
        t = TIERS[k]
        L.append(f"| {t['label']} | {t['who']} | {m(t['arr'])} | {t['term']} yr | {t['prepay']:.0%} | {t['tranche']} |")
    L += ["", "Prices are the author's tiers in Nebius.MD and initiation note §7.3: short-term $40–50M (low end used), "
          "core $20–25M (midpoint), 5-year hyperscaler ~$12M (Microsoft's Vineland deal implies $11.6–12.9M).", ""]

    L += ["## Per MW: sources and uses", "",
          "Current = prepayment, then equity or converts for the rest, with the shell owned. "
          "Proposed = prepayment, a GPU loan sized to the contract, the shell sold and leased back, then equity.", "",
          "| $M per MW | " + " | ".join(f"{TIERS[k]['label']}, current | {TIERS[k]['label']}, proposed" for k in tiers) + " |",
          "|---" * (1 + 2 * len(tiers)) + "|"]
    rows = [
        ("Capex", lambda v: m(v["capex"])),
        ("Customer prepayment", lambda v: m(v["prepay"])),
        ("Secured GPU loan", lambda v: m(v["debt"])),
        ("Shell sale-leaseback", lambda v: m(v["shell_sale"])),
        ("Debt service reserve (a use)", lambda v: m(v["dsra"])),
        ("**Nebius equity / converts**", lambda v: f"**{m(v['equity'])}**"),
        ("EBITDA, contract years", lambda v: m(v["ebitda"])),
        ("Shell rent", lambda v: m(v["rent"])),
        ("Cash available for debt service, year 1", lambda v: m(v["cfads"])),
        ("Debt service", lambda v: m(v["debt_service"])),
        ("DSCR", lambda v: f"{v['dscr']:.2f}x" if v["dscr"] else "—"),
        ("Loan rate", lambda v: pct(v["rate"]) if v["rate"] else "—"),
        ("Cost of capital on the capex", lambda v: pct(v["wacc"])),
        ("Equity IRR over 5 years", lambda v: pct(v["irr"])),
        ("Equity NPV at 12%", lambda v: m(v["npv"])),
    ]
    for name, fn in rows:
        L.append(f"| {name} | " + " | ".join(f"{fn(cur[k])} | {fn(pro[k])}" for k in tiers) + " |")

    L += ["", "## Price per MW needed for a 12% equity return", "",
          "The contract price at which equity NPV at 12% is zero. This is what cheaper financing buys: the same "
          "build works at a lower price.", "",
          "| Tier | Current structure | Proposed structure | Difference | Tier price |", "|---|---|---|---|---|"]
    for k in tiers:
        rc, rp = required_arr(k, "current"), required_arr(k, "proposed")
        L.append(f"| {TIERS[k]['label']} | {m(rc)} | {m(rp)} | {m(rp - rc)} | {m(TIERS[k]['arr'])} |")

    L += ["", "## Sensitivity: the hyperscaler tier", "",
          "One input changed at a time. The 5-year tier is the one that matters: it is most of the build and the "
          "only tier priced close to its cost.", "",
          "| Change | Needed price, current | Needed price, proposed | Equity per MW, proposed | Equity IRR at $12M, proposed |",
          "|---|---|---|---|---|"]
    for label, over in SENSITIVITY:
        v = vintage("hyperscaler", "proposed", **over)
        L.append(f"| {label} | {m(required_arr('hyperscaler', 'current', **over))} | "
                 f"{m(required_arr('hyperscaler', 'proposed', **over))} | {m(v['equity'])} | {pct(v['irr'])} |")
    L += ["", "**Read this first:** the model sizes debt on *project* cash flow (contract revenue less power and site "
          "operations), as a lender does. The AI cloud segment's 50% EBITDA margin also carries the platform, R&D, sales "
          "and leased-site rent, which stay at the parent. If 50% were the project margin, no financing structure makes "
          "a $12M contract work, which is the funding model review's finding."]

    L += ["", f"## The 2027–2030 build: {sum(gw_added):.2f} GW", "",
          f"GW added per year from the reconciled funding model ({', '.join(f'{g:.2f}' for g in gw_added)}). "
          f"Shares are counted at **${price:.2f}** ({scen.VALUATION['price_date']}); "
          f"dilution is against {shares_ye26:.1f}M year-end 2026 shares. Equity here is before operating cash flow, which in the "
          "funding model pays for part of the build in later years.", "",
          "| $B, 2027–30 | " + " | ".join(f"{label}, current | {label}, proposed" for _, label, _ in MIXES) + " |",
          "|---" * (1 + 2 * len(MIXES)) + "|"]
    progs = [(program(mix, "current"), program(mix, "proposed")) for _, _, mix in MIXES]
    prow = [
        ("Capex", lambda p: b(p["capex"])),
        ("Customer prepayments", lambda p: b(p["prepay"])),
        ("Secured GPU loans", lambda p: b(p["debt"])),
        ("Shell sale-leasebacks", lambda p: b(p["shell_sale"])),
        ("**Nebius equity / converts**", lambda p: f"**{b(p['equity'])}**"),
        ("Shares at today's price (M)", lambda p: f"{p['equity'] * 1000 / price:,.0f}"),
        ("Dilution", lambda p: f"{p['equity'] * 1000 / price / shares_ye26:+.0%}"),
        ("Shell rent at full build, a year", lambda p: b(p["rent"])),
        ("IG contract value to be signed", lambda p: b(p["ig_tcv"])),
    ]
    for name, fn in prow:
        L.append(f"| {name} | " + " | ".join(f"{fn(c)} | {fn(p)}" for c, p in progs) + " |")
    base_pro = program(MIXES[1][2], "proposed")
    L += ["", f"**Debt follows contracts.** Tranche A can only be drawn against signed investment-grade contracts. "
          f"Nebius cited ~${IG_CONTRACTED:.0f}B of IG contracted revenue available to finance in July 2026; at "
          f"{m(TIERS['hyperscaler']['arr'] * TIERS['hyperscaler']['term'])} of contract value per MW that covers "
          f"~{IG_CONTRACTED / (TIERS['hyperscaler']['arr'] * TIERS['hyperscaler']['term']):.2f} GW. "
          f"The base mix needs {b(base_pro['ig_tcv'])}.",
          "",
          "**Prepayments are set per contract, not per dollar of capex.** Deferred revenue was $6.0B against $37.5B of RPO "
          "at June 30 (16% of contract value); IREN's Microsoft prepayment was ~20%. The workbook's 45% of capex equals "
          "~44% of a 5-year hyperscaler contract, which no customer has paid so far (see the sensitivity)."]

    years, rows_s = schedule(MIXES[1][2])
    L += ["", "## Secured debt schedule, base mix, proposed structure ($B)", "",
          "A vintage is built and drawn in its build year, earns from the next year, and amortizes over its contract. "
          "Cash available for debt service covers every vintage in operation, after shell rent. A site's rent is counted "
          "while its first GPUs run; after year 5 the 20-year lease is carried by the GPU refresh, which needs its own "
          "contract and tranche and is not modeled.", "",
          "| | " + " | ".join(str(y) for y in years) + " |", "|---" * (len(years) + 1) + "|"]
    for name, key, f in (("Drawn", "drawn", "{:.1f}"), ("Interest", "interest", "{:.1f}"),
                         ("Principal", "principal", "{:.1f}"), ("Closing secured debt", "closing", "{:.1f}"),
                         ("Shell rent", "rent", "{:.1f}"), ("Cash available for debt service", "cfads", "{:.1f}")):
        L.append(f"| {name} | " + " | ".join(f.format(rows_s[y][key]) for y in years) + " |")
    L.append("| DSCR | " + " | ".join(f"{rows_s[y]['dscr']:.2f}x" if rows_s[y]["dscr"] else "—" for y in years) + " |")

    L += ["", "## Term sheet", "",
          "| | A. Contract-backed GPU loan | B. Core-contract DDTL | C. Shell sale-leaseback | D. Corporate converts / equity |",
          "|---|---|---|---|---|"]
    for row in TERM_SHEET:
        L.append("| " + " | ".join(row) + " |")
    L += ["", "**Cash waterfall in each borrower:** customer receipts → power and site operations → shell rent → "
          "senior interest and principal → reserve top-up → distributions to Nebius only above 1.15x DSCR."]
    (OUT / "debt_structure.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return cur, pro, progs


def write_csv(cur, pro, progs):
    with open(OUT / "debt_structure.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["section", "case", "structure", "metric", "value"])
        for structure, vs in (("current", cur), ("proposed", pro)):
            for tier, v in vs.items():
                for k in ("arr", "prepay", "debt", "shell_sale", "dsra", "equity", "ebitda", "rent", "cfads",
                          "debt_service", "dscr", "rate", "wacc", "irr", "npv"):
                    w.writerow(["per_mw", tier, structure, k, "" if v[k] is None else round(v[k], 4)])
                w.writerow(["per_mw", tier, structure, "required_arr", round(required_arr(tier, structure), 4)])
        for (key, _, _), (c, p) in zip(MIXES, progs):
            for structure, prog in (("current", c), ("proposed", p)):
                for k in ("gw", "capex", "prepay", "debt", "shell_sale", "equity", "rent", "ig_tcv"):
                    w.writerow(["program", key, structure, k, round(prog[k], 4)])
        years, rows = schedule(MIXES[1][2])
        for y in years:
            for k in ("drawn", "interest", "principal", "closing", "rent", "cfads", "dscr"):
                v = rows[y][k]
                w.writerow(["schedule", f"base_{y}", "proposed", k, "" if v is None else round(v, 4)])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cur, pro, progs = write_markdown()
    write_csv(cur, pro, progs)
    for k in TIERS:
        c, p = cur[k], pro[k]
        print(f"{TIERS[k]['label']:24} equity/MW {m(c['equity']):>8} -> {m(p['equity']):>8}   "
              f"IRR {pct(c['irr']):>7} -> {pct(p['irr']):>7}   needed price {m(required_arr(k, 'current')):>8} -> "
              f"{m(required_arr(k, 'proposed')):>8}")
    for (_, label, _), (c, p) in zip(MIXES, progs):
        print(f"{label:44} equity {b(c['equity']):>8} -> {b(p['equity']):>8}   secured debt {b(p['debt']):>7}")


if __name__ == "__main__":
    main()
