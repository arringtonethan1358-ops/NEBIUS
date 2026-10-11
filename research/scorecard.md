# Prediction Scorecard

This page holds the repo's calls, written down **before** each report and scored afterwards, so readers can judge the research on its record. The git history timestamps every entry.

**Rules**
- Predictions are written down before the report and are not edited afterwards. A wrong call stays on the page.
- Each one is scored **Hit**, **Miss**, or **n/d** (not disclosed). A non-disclosure is recorded but not counted either way.
- A range is a hit if the reported number lands inside it, including the endpoints.

> Not investment advice.

## Q3 2026 (report expected November 10–11, 2026)

*Recorded October 11, 2026, at a share price of $221.33.*

**Sources of the numbers:**
- **Model:** the base case of [`models/nebius_scenarios.py`](../models/nebius_scenarios.py).
- **Bars:** from [`earnings/2026-Q3.md`](../earnings/2026-Q3.md).
- **Main call:** in [`call-note.md`](call-note.md).

| # | Prediction | Model / bar | Actual | Result |
|---|---|---|---|---|
| 1 | AI cloud **ARR at September 30: $4.2–5.5B**. Below the straight-line path to the year-end guide ($5.0–6.0B), because the Microsoft ramp is weighted to Q4 | Base $4.86B; author's pipeline $4.18B | | |
| 2 | **Group revenue: $0.85–1.05B** | Base $930M; straight-line bar $1.0–1.2B | | |
| 3 | **Group adjusted EBITDA margin: 39–46%** | Base 44%; full-year guide ~40%; H2 implied ~41% | | |
| 4 | Full-year 2026 guidance for **revenue ($3.0–3.4B) and year-end ARR ($7–9B) reaffirmed, not raised** | — | | |
| 5 | **Capex: $5.9–8.4B** for the quarter | Base $7.2B; guide-implied bar | | |
| 6 | **Deferred revenue rises $1.5–4.0B** in the quarter (prepayments rebound from Q2's +$1.2B) | Base ~$3.6B gross prepayments | | |
| 7 | **Depreciation and amortization above $300M** (Q2: $259.7M) as equipment goes into service | — | | |
| 8 | **ARR per active MW ≤ $13M**, if Nebius discloses active MW. This is the main call: the ~$12M contract rate, not the $20–25M mid-term tier | Call note | | |
| 9 | New contracts disclosed in the quarter are **mostly hyperscaler / multi-year**, not 1–3-year deals at $20M+ per MW | Call note | | |
| 10 | **Top-3 customers still above 50%** of revenue (Q2: 59%) | — | | |

**Score:** _to be filled after the report._

### How the main call is scored

The call is right if #8 is a hit, or #8 is n/d and #9 is a hit. It is wrong if:
- active-MW disclosure puts ARR per MW at **$18M or more**, on a basis comparable to capex, or
- Nebius says most new capacity is signed at mid-term rates.

Anything in between is recorded as *unresolved* and carried to Q4.
