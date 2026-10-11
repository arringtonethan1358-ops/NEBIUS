# Nebius (NBIS): The Stock Needs ~$11–15M per MW. The Build Needs $20M.

*Call note, October 11, 2026. Share price $221.33 (October 9 close). Not investment advice.*

## The call

The debate on Nebius is usually framed as capacity: can it bring 5 GW online? We think the real question is **price per megawatt**, which shows up nowhere in the guidance. A rough guide to the numbers:

| What it takes | ARR per MW |
|---|---|
| Justify today's share price | **~$11–15M** |
| GPUs earn back their cost on a 5-year life | **~$20M** |
| The only contract with a disclosed MW count (Microsoft) | **~$12M** |

So the stock is fairly priced if the market keeps valuing Nebius on EBITDA, and expensive if it starts valuing it on earnings. The Q3 report on November 10–11 is the first chance to find out which.

## The arithmetic

The model is [`models/funding_5gw.py`](../models/funding_5gw.py), our port of the author's 5 GW funding workbook. It is reconciled to the filings, and every step is shown in [`models/output/funding_5gw.md`](../models/output/funding_5gw.md).

The setup:
- Year-end 2026 ARR stays at the $8B guidance midpoint.
- The build ends at 5 GW in 2030.
- Capex is $58.7M per MW, the workbook's own figure.

Only the price per MW changes from row to row:

| ARR per MW | 2030 ARR | 2030 net income | Value today at 6x EBITDA | Value today at 9.5x |
|---|---|---|---|---|
| $8.5M (guidance-implied) | $42.5B | −$23.0B | $64 | $140 |
| **$12M (5-year contracts)** | **$60B** | **−$17.4B** | **$141** | **$261** |
| $16M | $80B | −$9.7B | $246 | $419 |
| $20M (workbook opening) | $100B | −$1.3B | $360 | $590 |
| $25M (workbook 2028–30) | $125B | $7.2B | $510 | $812 |

The 2030 value is discounted to today at 12% a year. At **$221.33**, the market is pricing:
- **~$10.9M per MW** if it keeps paying 9.5x EBITDA
- **~$15.1M** if it pays 6x

**The catch is depreciation.** Per MW, a year:

| Item | Amount |
|---|---|
| GPU depreciation ($58.7M × 64% GPUs ÷ 5 years) | **$7.5M** |
| EBITDA at $12M of ARR and a 50% margin | **$6.0M** |

Non-GPU assets and interest come on top. At contract prices the build grows EBITDA and loses money.

| GPU life | 2030 break-even ARR per MW |
|---|---|
| 5 years | **~$20.6M** |
| 6 years | ~$17.9M |
| 6 years, with capex cut to $45M per MW | ~$13.7M |

Even the last case is above $12M.

## Why $12M, not $20M

**For ~$12M or less:**
- Microsoft: $17.4–19.4B over 5 years on ~300 MW = **$11.6–12.9M per MW per year** *(derived)*. It is the only deal with a disclosed MW count.
- Q4 2025: ~$1.25B ARR on ~170 MW active = **~$7.4M** per MW.
- Guidance: $7–9B of year-end ARR on 0.8–1.0 GW connected = **$7–11M**.
- Mix: the 5 GW build is mostly hyperscaler capacity, which signs 5-year contracts.

**For $20M or more:**
- On-demand list prices rose again on October 1 (B300 up ~56% year to date).
- The first capacity auction cleared 15% above any price Nebius had charged before.
- The author's tier table puts mid-term (1–3-year) deals at $20–25M.
- Nebius is holding back 2027 capacity, expecting higher prices.

All of this is real, but it describes the *short- and mid-term* book. That book is the minority of a 5 GW build anchored by hyperscalers.

## What would change our mind

1. **A disclosed price basis.** Nebius says its per-MW prices are quoted per IT MW while capex is per grid MW. A PUE of 1.2–1.3 shrinks the gap by that much.
2. **A mix that stays mid-term.** New contracts for the 2027 capacity it is holding back sign at $20M+ for 1–3 years, rather than at hyperscaler rates.
3. **Cheaper builds.** All-in capex comes in well below $45M per MW.
4. **Longer GPU lives** that the market accepts. Our H100 work (initiation note §7.4) suggests old GPUs stay profitable longer than 5 years.

## What Q3 will tell us

The [scorecard](scorecard.md) writes down, before the report, the thresholds that would confirm or break this call. The most important:

| Disclosure | Supports the call | Breaks it |
|---|---|---|
| ARR per active MW at September 30 | ≤ $13M | ≥ $18M on a basis comparable to capex |
| Pricing on contracts signed in Q3 | Hyperscaler-weighted | Mostly mid-term at $20M+ |
| Capex per MW guidance for 2027 | ≥ $50M | ≤ $40M |
| D&A in the quarter | Rising faster than revenue | Flat as capacity goes live |

## Risks to the call

- **Upside:** scarcity lasts through 2028. Every renewal reprices higher and the 5-year tier never dominates the mix.
- **Downside beyond our numbers:**
  - The fully diluted count here excludes conversion of the existing converts ($20.8B fair value).
  - Three customers are 59% of revenue.
  - Site delays push the revenue later while the financing still dilutes on schedule.

Sources: Q1 and Q2 2026 Form 6-K, Exhibit 99.2; company releases; author's notes. Each figure is tagged in [`research/nebius-initiation.md`](nebius-initiation.md), and the workbook review is in [`notes/2026-10-funding-model-review.md`](../notes/2026-10-funding-model-review.md).
