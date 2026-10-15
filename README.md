# NEBIUS
This is a repo about Nebius, and helps provide alpha to readers 

Independent research on **Nebius Group (NASDAQ: NBIS)**, the AI cloud and GPU infrastructure company.

## The call in one page

*As of October 11, 2026. Share price $221.33. Not investment advice.*

**The question that matters is price per megawatt, not capacity.** Nebius guides to 5 GW of contracted power and $7–9B of ARR by year-end 2026. What it doesn't disclose is how much revenue each megawatt earns, and that one number decides the outcome:

| What it takes | ARR per MW | Source |
|---|---|---|
| Today's share price | **~$11–15M** | 9.5x vs. 6x EBITDA, [funding model](models/output/funding_5gw.md) |
| GPUs earn back their cost on a 5-year life | **~$20M** | Same model, at $58.7M of capex per MW |
| Microsoft's 5-year deal (the only contract with a disclosed MW count) | **~$12M** | Derived |

So the stock is roughly fairly priced if investors keep valuing Nebius on EBITDA. It is expensive if they start valuing it on earnings, because GPU depreciation outruns EBITDA at contract prices.

| | |
|---|---|
| **Where it is** | Q2 revenue $582M (+454% YoY), AI cloud EBITDA margin 50%, ARR $3.0B, backlog (RPO) $37.5B |
| **The strain** | Q2 free cash flow −$3.4B. Converts worth $20.8B vs. $8.5B on the books. ~38M new shares or equivalents in H1. Three customers are 59% of revenue |
| **The bull case** | On-demand prices up again on October 1, auctions clearing at record prices, and a software layer (Tavily, ClarifAI, Eigen AI) that could keep customers once GPU scarcity fades |
| **What settles it** | The Q3 report (November 10–11): ARR per active MW, the mix of new contracts, 2027 capex per MW. The 10 predictions written down in advance are in the [scorecard](research/scorecard.md) |
| **Valuation** | EV $68.5–76.6B, 9.0–10.0x base-case year-end 2026 ARR, vs. ~4–5x for CoreWeave |

Read next: the [call note](research/call-note.md) (one page), then the [initiation note](research/nebius-initiation.md) (full research).

## Start here

- **[Initiation note](research/nebius-initiation.md):** business overview, financial trajectory, capacity build-out, funding, pricing power and the software-layer thesis, bull and bear cases, valuation framework, and what to watch next quarter.
- **[Peer comparison](research/peer-comparison.md):** Nebius vs. CoreWeave vs. IREN on growth, backlog, capex intensity, funding and pricing.
- **[Call note](research/call-note.md):** the one-page argument above, with the arithmetic and what would change it.
- **[Prediction scorecard](research/scorecard.md):** dated calls for each quarter, scored after the report.
- **[Scenario model](models/output/scenarios.md):** 2026–2027 bear, base and bull paths for ARR, revenue, EBITDA, capex and the funding gap.
- **[5 GW funding model](models/output/funding_5gw.md):** the author's 2027–2030 funding workbook, ported to code and reconciled to the filings step by step, with a price-per-MW sensitivity. [Review](notes/2026-10-funding-model-review.md).
- **[Debt structure](research/debt-structure.md):** a cheaper way to fund the build. Each contract tier in Nebius.MD gets its own tranche: contract-backed GPU loans, matched-tenor term loans, and shell sale-leasebacks. Cuts equity per contracted MW about 6x. [Model output](models/output/debt_structure.md).
- **[Dashboard](https://claude.ai/artifact/VctArcL8X2pdPxmKpKs1Yb):** headline numbers, ARR scenarios, cash flow, capacity pipeline, valuation, site list, and a GPU economics calculator. Private until shared.

## Layout

| Folder | Contents |
|---|---|
| `research/` | Long-form theses and deep dives |
| `earnings/` | One note per quarter (copy `earnings/TEMPLATE.md`). Next up: [`2026-Q3.md`](earnings/2026-Q3.md), a pre-earnings draft with the bars Q3 must clear |
| `data/` | `nebius_kpis.csv`: tracked KPIs, each row with a source and a source-quality label. `mw_pipeline.csv` and `contracted_sites.csv`: the author's capacity estimates by stage and site. `gpu_economics.csv`: per-GPU assumptions behind the calculator |
| `notes/` | Working drafts and running theses, not yet polished. [`news-log.md`](notes/news-log.md) is filled by the weekly news check. Includes the author's [October 2026 report draft](notes/2026-10-nebius-report-draft.md) and its [fact-check](notes/2026-10-report-review.md), and the [funding model review](notes/2026-10-funding-model-review.md) |
| `scripts/` | `validate_kpis.py` checks the KPI dataset's schema and sourcing rules. It runs automatically on every pull request |
| `models/` | `nebius_scenarios.py`: bear, base, bull and author's-pipeline model through 2027, built from `data/`, with EV multiples at the current share price. `funding_5gw.py`: the author's 5 GW workbook (`source/NBIS_5GW_Funding_Model.xlsx`) ported to code, checked cell by cell against it, then reconciled. `debt_structure.py`: tiered debt structure, per MW and for the 2027–2030 build, with a debt schedule and term sheet. Output is in [`models/output/`](models/output/). CI fails if any output is stale |

## Automation

- **Weekly news check (Mondays, 13:55 UTC):** searches for Nebius and peer news and opens a pull request adding material items to `notes/news-log.md`.
- **Q3 2026 earnings (Nov 10, 16:00 UTC):** fills in `earnings/2026-Q3.md`, scores the Q3 predictions in `research/scorecard.md`, and opens a pull request.
- **CI on every pull request:** validates the KPI file and checks that the model output is current.

## Sourcing rules

1. Every number gets a citation.
2. Label each source: `filing` (6-K/20-F financial statements, with page), `filing_derived` (arithmetic on filed numbers), `primary_linked` (company release or letter), `secondary` (press, analysts), or `author_notes` (our own notes, not yet independently confirmed).
3. Replace secondary figures with primary ones whenever possible.
4. Before committing data changes, run `python scripts/validate_kpis.py`, `python models/nebius_scenarios.py`, `python models/funding_5gw.py` and `python models/debt_structure.py`, and commit the regenerated `models/output/`.

---

*Not investment advice. For educational purposes only.*
