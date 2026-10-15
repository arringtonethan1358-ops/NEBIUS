# Review: the author's 5 GW funding model

*Reviewed October 11, 2026. Workbook: [`models/source/NBIS_5GW_Funding_Model.xlsx`](../models/source/NBIS_5GW_Funding_Model.xlsx). Code port and reconciliation: [`models/funding_5gw.py`](../models/funding_5gw.py), with output in [`models/output/funding_5gw.md`](../models/output/funding_5gw.md).*

> Not investment advice.

## What the workbook does

The workbook asks how Nebius pays for building out to 5 GW of live capacity from 2027 to 2030. It assumes:

- capacity: 0.4 GW in June 2026, plus 1.15 GW a year
- revenue: $20–25M of ARR per MW
- cost: $270B of capex, about $58.7M per MW
- margins: 50% EBITDA, with 70–80% of EBITDA turning into cash

The funding stack:

- customer prepayments cover 45% of capex
- 15% of EBITDA goes to capex
- straight equity covers 20% of capex
- secured debt covers up to 25% of capex
- convertible notes fill the rest

The equity issue price comes from the same year's EBITDA × 9.5, less debt. A second sheet depreciates the GPU share of capex (64%) over 5 years, deducts interest and 22% tax, and puts the result on 20x EPS.

**As received, the 2030 results are:**

| Item | 2030 value |
|---|---|
| ARR | $125B |
| Net income | $13.1B |
| EPS | $37.17 |
| Price at 20x EPS | **$743** |
| Dilution | 36% |
| Closing cash | $83.6B |

## Port check

`models/funding_5gw.py` reproduces every formula. On each run it compares 64 cells against the values Excel saved in the workbook, and stops if any of them differ. All 64 match, so the reconciliation below starts from exactly what the workbook computes.

## Findings, most important first

### 1. The price per MW carries the whole result, and the $20–25M "floor" is the mid-term tier, not the hyperscaler rate

`Debt Equity!B7:F7` sets ARR per MW at $20M today and $22–25M from 2027. Applying that rate to all 5 GW is the most aggressive input in the model:

- **It is the 1–3-year tier.** In the author's own tier table (`research/nebius-initiation.md` §7.3), $20–25M is the *mid-term* rate. Five-year hyperscaler contracts are ~$12M. The 5 GW build is mostly hyperscaler capacity (Microsoft, Meta), so most of it should price near $12M.
- **The only contract with a known MW count is $11.6–12.9M per MW a year.** That is Microsoft's $17.4–19.4B over 5 years on ~300 MW at Vineland *(derived)*. [S] [N]
- **Observed ARR per MW has been lower still.** It was ~$7.4M at Q4 2025 ($1.25B ARR [S] on ~170 MW active [PR]). Guidance pairs $7–9B of year-end ARR with 0.8–1.0 GW connected, i.e. $7–11M.
- **The opening point is a year-end figure, not June.** `B4 × B7` = 0.4 GW × $20M = **$8B**, labelled "Jun'26 A". Actual June ARR was **$3.0B** [PR]. $8B is the midpoint of the *year-end* 2026 guide, so the workbook effectively starts in December 2026 but labels that point June.

**Effect** (step 2 in the output, $12M per MW, same $8B opening ARR, still ending at 5 GW):

| | Workbook | Step 2, at $12M per MW |
|---|---|---|
| 2030 ARR | $125B | $60B |
| 2027–30 EBITDA | $132B | $68B |
| 2030 net income | $13.1B | **−$9.7B** |

### 2. At contract prices, the GPUs don't earn back their cost on a 5-year life

This follows from the workbook's own capex and depreciation inputs:

| Per MW, per year | Amount |
|---|---|
| GPU depreciation ($58.7M × 64% ÷ 5 years) | **$7.5M** |
| EBITDA at $12M of ARR and a 50% margin | **$6.0M** |

Non-GPU assets and interest come on top. **Break-even ARR per MW for 2030 net income**, reconciled model:

| Capex per MW | 5-year GPU life | 6-year GPU life |
|---|---|---|
| $58.7M (workbook) | $20.6M | $17.9M |
| $50M | $17.6M | $15.2M |
| $45M | $15.8M | $13.7M |

Every cell is above the ~$12M five-year contract rate.

This is the strongest bear argument in the repo, and it comes from the bull model's own inputs. It only holds if the price and the capex are quoted per the **same kind of MW**:
- If the $12M is per IT MW and capex is per grid MW, the comparison overstates the problem by roughly the PUE (1.2–1.3x).
- That is one more reason to get the MW basis answered on the Q3 call (watch-list item 12).

### 3. The model raises outside capital while holding $84B of cash

`B67` sends only 15% of EBITDA to capex. Rows 27 and 46 then put the rest of operating cash into the cash balance. Meanwhile `B64` issues equity for 20% of capex every year regardless.

By 2030 the model has:
- raised **$128.7B** of debt and equity
- built up **$83.6B** of cash

No company would do both. Sweeping operating cash into capex first (step 3) cuts outside capital by **$35.8B** in the reconciled case and leaves closing cash at about the opening level. The workbook lacks a minimum-cash input, which would be the right control here.

### 4. The balance sheet starts in June, but the ARR starts in December

The model rolls straight from June 30 into 2027, so July–December 2026 is missing.

| Item | Workbook (June 30) | Year-end 2026, pro forma |
|---|---|---|
| Cash | $8.0B | ~$8.4B |
| Debt | $8.5B (carrying value) | ~$15.8B at principal, of which $0.775B secured |
| Shares | 271.9M | ~308.7M |

Missing from H2 2026:
- ~$14.4B of capex
- ~$7.2B of prepayments
- the $775M secured loan (July)
- the $5.75B of converts (August; $5.0B priced plus $750M of options)
- the $0.8B note exchange

`B83` (secured debt) is 0, but the July loan is secured. Step 1 fixes the opening balances. Debt is measured at principal ($10.04B accreted [F2 F-28]), because that is what accrues interest and gets repaid, rather than the $8.5B carrying value.

### 5. The share count leaves out shares that already exist

- **`B85` = 271.855M** is Class A + B only.
  - It excludes NVIDIA's **21.07M pre-funded warrants**: exercise price $0.0001, economically already shares. [F2 F-31]
  - It also excludes the ~15.8M August exchange shares. [PR]
- **Rows 60–61** dilute only for *new* converts. The existing converts (fair value **$20.8B** [F2 F-29], deep in the money) are left out entirely, so "cumulative dilution vs Jun-2026" understates the true fully diluted count. The port matches the workbook on this; the existing converts' conversion terms aren't in `data/` yet.
- **`Depreciation!D38:G38`** divides by a hardcoded **0.3522B** shares for every year. The model's own share count is 312M in 2027 and 370M fully diluted in 2030, so 2027 EPS is understated and 2030 EPS overstated. Step 4 uses the modeled count.

### 6. Depreciation covers only the GPUs bought in 2027–2030

The `Depreciation` sheet depreciates 64% of new capex. Not covered:
- **The other 36% (~$97B):** buildings, power, cooling. Never depreciated.
- **Assets already in place at year-end 2026:** ~$27B, made up of June PP&E of $13.0B [F2 F-2] plus H2 capex.

Step 4 adds:
- 20-year lives on non-GPU capex
- ~$4.0B a year on the existing base, using the same 64/36 split

Q2 D&A was $259.7M for the quarter [F2 F-3] and will step up as the $7.8B of equipment not yet in service goes live.

### 7. Smaller items

- **The issue price ignores cash** (`C78 = EV − opening debt`). With the workbook's cash pile this materially understates the price. Step 4 adds opening cash.
- **Two valuations in one file disagree by 1.8x.** EV/EBITDA at 9.5x implies a **$1,325** 2030 issue price (`F79`). 20x EPS implies **$743** (`Depreciation!G39`). The share count and the exit value should come from one method.
- **The issue price is circular in substance.** It uses the same year's full EBITDA, so the 2027 equity is priced on 2027 results before they exist. Prior-year or forward-12-month EBITDA at the time of issue would be more realistic.
- **Interest is understated in build years.** Interest runs on opening balances, so debt raised during 2027 pays none until 2028. 2027 interest is $0.09B on $22B of new debt.
- **No cost for the rest of the group.** EBITDA = revenue × 50%, with no cost for Avride, TripleTen or corporate (~−$0.2B a year at Q2 rates).
- **Tax isn't in the cash flow.** It is computed on the `Depreciation` sheet but never deducted from cash.
- **Wrong row references in labels:** `A15` says "row 39" but uses row 40. `A52` says "see row 63" but means row 79.

## Reconciled result

Each step stacks on the previous one. Details are in `models/output/funding_5gw.md`.

| 2030 | Workbook | 1. YE26 open | 2. $12M per MW | 3. Cash sweep | 4. Accounting |
|---|---|---|---|---|---|
| ARR | $125B | $125B | $60B | $60B | $60B |
| Outside capital, 2027–30 | $128.7B | $128.7B | $129.7B | $93.9B | $93.9B |
| Closing cash | $83.6B | $83.5B | $43.0B | $8.4B | $8.4B |
| Shares, diluted for new converts | 370M | 427M | 556M | 506M | 485M |
| Net income | $13.1B | $13.0B | −$9.7B | −$8.9B | −$17.4B |

## What would make the workbook's numbers right

Any one of these, if shown in the filings, moves the result back toward the workbook's case:

1. **Price:** Nebius discloses ARR per MW near $20M on a basis that matches capex, or shows that the 5 GW mix leans to mid-term and short-term contracts rather than 5-year hyperscaler deals.
2. **Capex:** all-in capex well below $45M per MW.
3. **GPU life:** a longer depreciation life, backed by the H100 data (initiation note §7.4). A 6-year life lowers break-even by about $2.7M per MW.

The Q3 call can settle the first. See [`research/call-note.md`](../research/call-note.md).
