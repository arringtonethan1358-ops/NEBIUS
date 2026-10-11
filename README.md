# NEBIUS
This is a repo about Nebius, and helps provide alpha to readers 

Independent research on **Nebius Group (NASDAQ: NBIS)**, the AI cloud and GPU infrastructure company.

## Start here

- **[Initiation note](research/nebius-initiation.md):** business overview, financial trajectory, capacity build-out, funding, pricing power and the software-layer thesis, bull and bear cases, valuation framework, and what to watch next quarter.
- **[Peer comparison](research/peer-comparison.md):** Nebius vs. CoreWeave vs. IREN on growth, backlog, capex intensity, funding and pricing.
- **[Scenario model](models/output/scenarios.md):** 2026–2027 bear, base and bull paths for ARR, revenue, EBITDA, capex and the funding gap.
- **[Dashboard](https://claude.ai/artifact/VctArcL8X2pdPxmKpKs1Yb):** headline numbers, ARR scenarios, cash flow, capacity pipeline, valuation, site list, and a GPU economics calculator. Private until shared.

## Layout

| Folder | Contents |
|---|---|
| `research/` | Long-form theses and deep dives |
| `earnings/` | One note per quarter (copy `earnings/TEMPLATE.md`). Next up: [`2026-Q3.md`](earnings/2026-Q3.md), a pre-earnings draft with the bars Q3 must clear |
| `data/` | `nebius_kpis.csv`: tracked KPIs, each row with a source and a source-quality label. `mw_pipeline.csv` and `contracted_sites.csv`: the author's capacity estimates by stage and site. `gpu_economics.csv`: per-GPU assumptions behind the calculator |
| `notes/` | Working drafts and running theses, not yet polished. [`news-log.md`](notes/news-log.md) is filled by the weekly news check. Includes the author's [October 2026 report draft](notes/2026-10-nebius-report-draft.md) and its [fact-check](notes/2026-10-report-review.md) |
| `scripts/` | `validate_kpis.py` checks the KPI dataset's schema and sourcing rules. It runs automatically on every pull request |
| `models/` | `nebius_scenarios.py`: bear, base, bull and author's-pipeline model through 2027, built from `data/`, with EV multiples at the current share price. Output is in [`models/output/scenarios.md`](models/output/scenarios.md). CI fails if the output is stale |

## Automation

- **Weekly news check (Mondays, 13:55 UTC):** searches for Nebius and peer news and opens a pull request adding material items to `notes/news-log.md`.
- **Q3 2026 earnings (Nov 10, 16:00 UTC):** fills in `earnings/2026-Q3.md` and opens a pull request.
- **CI on every pull request:** validates the KPI file and checks that the model output is current.

## Sourcing rules

1. Every number gets a citation.
2. Label each source: `filing` (6-K/20-F financial statements, with page), `filing_derived` (arithmetic on filed numbers), `primary_linked` (company release or letter), `secondary` (press, analysts), or `author_notes` (our own notes, not yet independently confirmed).
3. Replace secondary figures with primary ones whenever possible.
4. Before committing data changes, run `python scripts/validate_kpis.py` and `python models/nebius_scenarios.py`, and commit the regenerated `models/output/`.

---

*Not investment advice. For educational purposes only.*
