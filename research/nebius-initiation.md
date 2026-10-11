# Nebius Group (NASDAQ: NBIS) — Initiation Note

*As of 2026-10-11. Latest reported quarter: Q2 2026 (reported 2026-08-12). Next catalyst: Q3 2026 results (expected mid-November 2026).*

> **Not investment advice.** This is independent research for educational purposes. Every figure carries a source tag; see [Sources](#sources).

**Source tags:**
- **[F2]** Q2 2026 Form 6-K, Exhibit 99.2 (unaudited financial statements). Page numbers are given as F-x.
- **[F1]** Q1 2026 Form 6-K (filed 2026-05-20), Exhibit 99.2.
- **[PR]** company press release or shareholder letter, read via excerpts.
- **[S]** secondary (press, analysts).
- **[N]** the author's own running notes and thesis (merged from `Nebius.MD`).
- **(derived)** our arithmetic on filed numbers.

---

## TL;DR

- **What it is:** a neocloud. Nebius builds GPU data centers and rents AI compute through its own cloud platform. AI cloud was **$574.9M of $582.3M Q2 revenue (~99%)**. [F2 F-3, F-33]
- **Where it is:** Q2 revenue **+454% YoY**. AI cloud adjusted EBITDA was **$285.7M (50% margin)**, and group adjusted EBITDA was **$236.2M (41%)**. [F2 F-33] ARR was **$3.0B** at June-end. [PR]
- **Visibility:** remaining performance obligations (RPO, contracted revenue not yet recognized) were **$37.5B**, up from $33.6B in March. 36% of it is due within 24 months. [F2 F-19] [F1]
- **2026 guidance (reaffirmed in August):**
  - $3.0–3.4B revenue
  - **$7–9B year-end ARR**
  - ~40% adjusted EBITDA margin
  - **$20–25B capex**
  - 5 GW of contracted power by year-end [PR]
- **Pricing power:** on-demand GPU list prices rose another **~17–21% on Oct 1** (B300 up ~56% year to date). Memory rose **+41%**. The first capacity auction cleared 15% above any price Nebius had ever charged. [N] [S]
- **The debate:** the backlog is real. Against it:
  - **Burn:** Q2 free cash flow was **–$3.4B** (derived).
  - **Converts:** the convertible notes carry a **$20.8B fair value vs. $8.5B on the books**. [F2 F-29]
  - **Equity:** ~38M new shares or share equivalents in H1 alone. [F2 F-5, F-31]
  - **Concentration:** three customers are **59%** of revenue. [F2 F-17]
- **Our framing:** the stock is a bet on turning **$7.8B of not-yet-in-service equipment** and 5 GW of contracted power into revenue on schedule. The open question is how much of that gets funded by customer prepayments rather than new shares.
- **The longer-term thesis** (§7): GPU scarcity wins customers today, but software on top of the GPU keeps them. Nebius is using scarcity pricing to fund a push up the stack (Tavily, ClarifAI, Eigen AI). The winners will own everything from chip to token. [N]

---

## 1. Business overview

| Segment | What it does | Q2 2026 revenue | Q2 2026 adj. EBITDA |
|---|---|---|---|
| **Nebius AI cloud** | GPU clusters, in-house servers, AI cloud platform, inference and training tools; data centers in Finland (owned), leased/co-located, and greenfield | $574.9M | **$285.7M** |
| **Avride** | Autonomous vehicles and delivery robots | $1.0M | $(40.1)M |
| **TripleTen** | Edtech / tech re-skilling | $10.0M | $(9.4)M |
| Eliminations | | $(3.6)M | |
| **Group** | | **$582.3M** | **$236.2M** |

Source: [F2 F-33].

**How customers buy compute [N]:**
- **Bare metal:** the whole physical GPU server, with no virtualization layer.
- **Managed Kubernetes or Slurm clusters:** Nebius runs the orchestration, networking and storage.
- **Serverless and managed inference (Token Factory):** sold to dev teams and individual developers, priced per token rather than per GPU-hour.

Revenue isn't broken out by these tiers. GPUs are NVIDIA only (H100, H200, B200, B300, GB200 and GB300 NVL72, L40S), with Vera Rubin NVL72 to come. See [`notes/2026-10-nebius-report-draft.md`](../notes/2026-10-nebius-report-draft.md).

**Equity stakes (not consolidated):** [F2 F-9, F-21]
- **ClickHouse:** minority stake, carried at **$1,517.7M**. It was written up by $780.6M after ClickHouse's January 2026 Series D, a $400M raise Nebius did not join. That non-cash gain is the whole reason Q1 GAAP net income was positive. Ownership % is not disclosed in the 6-K.
- **Toloka:** **minority** stake (49% voting interest since May 2025). The preferred shares are carried at $86.5M.

**H1 2026 acquisitions:** [F2 F-9, F-25] [F1 F-30]
- **Tavily:** search API for AI agents.
- **ClarifAI:** core team plus a $75M patent portfolio.
- **Eigen AI:** inference, model compression and fine-tuning. Closed June 10, 2026. Most of the money went to keeping the team, not buying the company: [F2 F-15/16]
  - purchase price $331.4M: ~1.4M shares worth $298.7M plus $32.7M cash
  - retention $549.2M: ~2.4M shares worth $508.1M plus $41.1M cash, vesting over 4 years and booked as compensation (~62% of total value)
- **Inferize (October 2026, after the period):** cuts the time it takes to load and scale models for inference. It is being folded into Token Factory. Terms weren't disclosed; press estimates $100–150M. [S]

Together these added **$605.6M of goodwill**. Nebius is buying software and inference talent to move up the stack from bare-metal GPU rental.

---

## 2. Financial trajectory

| $M | Q2 2025 | Q1 2026 | Q2 2026 | H1 2026 |
|---|---|---|---|---|
| Revenue | 105.1 | 399.0 *(derived)* | **582.3** | 981.3 |
| — AI cloud revenue | 93.7 | 389.7 *(derived)* | **574.9** | 964.6 |
| AI cloud adj. EBITDA | 9.5 | 174.0 *(derived)* | **285.7** | 459.7 |
| — margin | 10% | 45% | **50%** | 48% |
| Group adj. EBITDA | (21.0) | 129.5 *(derived)* | **236.2** | 365.7 |
| — margin | n/m | 32% | **41%** | 37% |
| Depreciation & amortization | 75.2 | 212.0 *(derived)* | 259.7 | 471.7 |
| Share-based compensation | 14.7 | 35.3 | 102.5 | 137.8 |
| Loss from operations | (111.2) | (128.0) *(derived)* | **(175.9)** | (303.9) |
| Net income / (loss) | 584.4 ¹ | 621.2 ² | **(190.4)** | 430.8 |
| Diluted EPS | $2.38 | — | **$(0.68)** | $1.53 |
| Diluted shares (weighted, M) | 247.3 | — | 280.4 | 302.6 |

Sources: [F2 F-3, F-33]. Q1 figures are H1 minus Q2. ¹ Includes a $597.4M ClickHouse revaluation gain and Toloka discontinued operations. ² Includes the $780.6M ClickHouse gain. [F1]

**ARR (company metric, not in the financial statements):** $1.25B (December 2025) → $1.9B (March) → **$3.0B (June)**. [PR] [S]

**GAAP bridge for Q2 2026 (filed):** [F2 F-34]

| $M | |
|---|---|
| Adjusted EBITDA | 236.2 |
| Depreciation and amortization | (259.7) |
| Share-based compensation | (102.5) |
| Acquisition costs | (49.9) |
| **Operating loss** | **(175.9)** |
| Net interest | (95.0) |
| Other income, equity-method income and tax | +80.5 |
| **Net loss** | **(190.4)** |

**Read-through:**
1. **Operating leverage is real.** The AI cloud margin went from 10% to 45% to 50% in four quarters. [F2]
2. **SBC jumped 3x quarter over quarter** ($35M → $103M), mostly from acquisition-related awards. Watch whether it settles back down.
3. **Depreciation is about to step up.** **$7.84B of PP&E is "assets not yet in use"**, 55% of gross PP&E. [F2 F-23] When it goes into service, quarterly D&A could roughly double from $260M, pushing GAAP further negative even as EBITDA grows.
4. **The second-half ARR ramp** from $3.0B to $7–9B is the key test. A cross-check: RPO due in the next 24 months is ~$13.5B (36% × $37.5B), or **~$6.7B per year** from contracted backlog alone (derived). That supports the low end of the ARR guide before any new deals.

---

## 3. Cash flow and funding: where the stress is

| $M | Q1 2026 | Q2 2026 | H1 2026 |
|---|---|---|---|
| Operating cash flow | 2,258.0 | **2,246.1** *(derived)* | 4,504.1 |
| — of which deferred revenue increase (prepayments) | 3,198.0 | **1,197.0** *(derived)* | 4,395.0 |
| Capex (PP&E + intangibles) | (2,472.9) | **(5,657.4)** *(derived)* | (8,130.3) |
| **Free cash flow** *(derived)* | **(214.9)** | **(3,411.3)** | **(3,626.2)** |
| Convertible notes, net | 4,293.7 | — | 4,293.7 |
| NVIDIA pre-funded warrants | 2,000.0 | — | 2,000.0 |
| ATM share sales, net | — | 2,811.1 | 2,811.1 |

Sources: [F2 F-7] [F1 cash flow statement].

**What the filings show:**
1. **Prepayments funded 54% of H1 capex** (4,397.7 / 8,130.3, derived). That matches management's 50–60% claim. [F2 F-19] [S]
2. **Q2 prepayment inflows fell by ~$2B** quarter over quarter, while capex more than doubled. Free cash flow went from roughly breakeven to **–$3.4B in one quarter**. The ATM ($2.8B) filled the gap. The $775M secured facility (July) and $5.0B of converts (August) came next. [F2 F-34] [PR]
3. **Deferred revenue has reached $5.98B**, up from $1.58B in December. Customers have prepaid about 10 quarters of current revenue. [F2 F-2, F-19]

**Balance sheet, June 30, 2026:** [F2 F-2, F-17, F-18, F-28]

| $M | Dec 31, 2025 | Mar 31, 2026 | Jun 30, 2026 |
|---|---|---|---|
| Cash and equivalents | 3,678.1 | 9,298.2 | **8,042.1** |
| Restricted cash | 43.5 | 328.7 *(derived)* | **1,056.0** |
| PP&E, net | 5,553.3 | — | **13,045.2** |
| Deferred revenue (total) | 1,577.5 | 4,778.1 | **5,975.2** |
| Convertible debt, carrying value | 4,103.2 | 8,432.0 | **8,499.0** |
| Convertible debt, accreted principal at maturity | 4,836.8 | — | **10,041.8** |
| Convertible debt, **fair value** | — | — | **20,823.7** |
| Total equity | 4,594.0 | 7,241.9 | 10,340.5 |

---

## 4. Share count and dilution

| Item | Shares (M) | Source |
|---|---|---|
| Class A + B shares outstanding, June 30, 2026 | **271.9** | [F2 F-2, F-5] |
| NVIDIA pre-funded warrants (exercise price $0.0001; already in basic EPS) | 21.1 | [F2 F-31] |
| ATM sold in Q2 at a $223.60 average (12.27M more available) | 12.7 *(already in outstanding)* | [F2 F-32] |
| Eigen AI acquisition | 3.8 *(already in outstanding)* | [F2 F-5] |
| March 2026 converts, at initial conversion rates (~$183 and ~$180 per share) | ~23.9 *(derived)* | [F2 F-27] |
| 2025 converts ($4.16B original principal) | *conversion rates not in these 6-Ks; see the 20-F* | |
| August 2026: $800M of 2029/2031 notes exchanged for shares | ~15.8 | [PR] |
| August 2026: $5.0B of new converts | *terms in the pricing release* | [PR] |

**Key point:** the converts' fair value (**$20.8B**) is 2.5x their carrying value. The market prices them as equity, not debt. When you value Nebius, count the conversion shares in the share base rather than treating the notes as debt. NVIDIA's March 2026 warrants were priced at **~$94.94 per share** ($2,000M / 21.07M shares, derived).

---

## 5. Customers and backlog

**Customers at 10% or more of revenue:** [F2 F-17]

| Customer | Q2 2025 | Q2 2026 | H1 2026 |
|---|---|---|---|
| Customer A | 39% | <10% | <10% |
| Customer B | 15% | <10% | <10% |
| Customer C | <10% | **24%** | 26% |
| Customer D | <10% | **21%** | 21% |
| Customer E | <10% | **14%** | <10% |

- **The top of the customer base turned over completely in a year.** Last year's two biggest customers are both now under 10%, and three new ones make up 59%. The filings don't name them. Press reporting identifies Microsoft and Meta as the two largest. [S]
- **Contracts reported in press (not in the 6-Ks):**
  - Microsoft: ~$17.4–19.4B (September 2025). [S]
  - Meta: ~$3B (November 2025), plus a larger multi-year deal reported at ~$27B. The size is **unverified**. [S]
- **Receivables are concentrated too:** Customer E holds 29% of accounts receivable and Customer D 16%. [F2 F-17]

**RPO:** [F2 F-19] [F1]

| | Mar 31, 2026 | Jun 30, 2026 |
|---|---|---|
| Total RPO | $33.6B | **$37.5B** |
| Due within 24 months | 29% | **36%** |
| Due in months 25–48 | 39% | 40% |
| Due after 48 months | 32% | 24% |

All of it belongs to the AI cloud segment. The shift toward near-term recognition is a good sign: more of the backlog becomes revenue sooner.

---

## 6. Capacity and power

| Metric | Value | Source |
|---|---|---|
| Active power, end of 2025 | ~170 MW | [PR] |
| Contracted power target, end of 2026 | **5 GW** (raised from 4 GW) | [PR] |
| Connected power target, end of 2026 | 800 MW – 1 GW, fully active in 1H 2027 | [S] |
| Build pace from 2027 | >1 GW per year | [S] |
| Fixed power and energy commitments | ~$540M per year in 2027–2030; $3.1B thereafter | [F2 F-26] |
| Bloom Energy fuel cells (May 2026) | ~250 MW guaranteed, 10-year terms, up to $2.6B in fees | [F1 F-30] |
| Long-lived assets in the US | $9.0B of $15.0B total | [F2 F-34] |
| Capex supplier concentration | three suppliers | [F2 F-17] |

**The author's MW pipeline, by stage and site [N]:** *(estimates, October 2026; not disclosed by the company; see the [review](../notes/2026-10-report-review.md))*

| Stage | Estimate | Detail |
|---|---|---|
| Active (earning revenue) | **200–275 MW** | Vineland NJ 100–150; Mäntsälä FI 75; London, Iceland, Israel, Paris, Kansas City and Minnesota 45–50 combined |
| Connected (powered, not yet billing) | 0–50 MW | Turns into active within months, so it never piles up. **This is not the company's definition**: its 0.8–1.0 GW "connected" target also includes capacity the author counts as active or under construction |
| Under construction | **~1 GW** (0.8–1.3) | 0.3–0.6 GW finishing by YE26 (leased sites plus Birmingham phase 1); 0.5–0.8 GW for 2027 (first phases of Missouri and Pennsylvania, plus Meta's second deal) |
| Contracted, not started | 3.1–3.8 GW of the 5 GW target | Pennsylvania construction isn't confirmed |
| Contracted by site | **~4.05 GW** | US owned 2.7 GW (Missouri up to 1.2 GW, likely ~0.8; Pennsylvania 1.2; Birmingham 0.3). US leased 0.47 GW (Vineland 300, Oklahoma 100+, Kansas City 40, Minnesota ~31 MW). Europe 0.8 GW (Lappeenranta 310, Béthune 240, Finland 145, UK 65, Estonia 22, Spain 18 MW). Israel 0.08 GW (Beit Shemesh 58, Masmiyya 22 MW) |

About 94% of contracted capacity hasn't come online yet. Site risks to watch:
- **Birmingham:** a Humane Society lawsuit challenges the substation and switching station, even though the city says no zoning approval was needed. [S]
- **Béthune:** the first phase missed its summer target, per the author. [N]
- **Vineland:** the 250 MW Bloom fuel cell installation. [F1 F-30]

---

## 7. Pricing power and the software layer

*Merged from the author's running notes (`Nebius.MD`; thesis added 2026-09-20, pricing logged 2026-09-22). Tag: **[N]**.*

### 7.1 Thesis: value add on top of the accelerator [N]

The hyperscalers didn't just build businesses renting out CPU compute. They built extremely valuable products around data, networking, security, storage, etc. We're now building around AI accelerators, but the playbook of building value add software on top is the same.

Turns out GPUs are really good for running AI models. That is why inference engines, which take a trained model and compute and produce intelligent tokens that can do real work, have become the first piece of this software stack. But, there is so much more to build than just this!

Training helps you turn compute into better models that produce more valuable tokens. Routing helps you pick the right model to generate those tokens at the right cost and quality. Security monitoring helps you check what's going into and coming out of those models. Then there's agent observability, context management, sandboxing, etc. All of these things will be part of the new AI stack and the opportunity is much bigger than just serving a model.

This definitely isn't a winner-take-all market, whether we're talking about open models vs. the frontier or the players within each category. Customers want choice, flexibility, and access to the fundamental building blocks to create their own systems.

Constrained GPU supply will actually act like a regularizer and draw this fight out longer. Customers are looking for both compute capacity AND value add on top of it. When someone doesn't have capacity, you go somewhere else. That means more players get exposure to customers and the opportunity to address value add.

Getting a customer because you have available GPUs is different from keeping them because your software is better. In the limit, the value add on top of the GPU will win out. The companies that do the best job building that software AND verticalize the fastest to own everything from chip to token will take the lion's share. It's important to be building for that now, even when the immediate customer need is just more compute.

**Takeaways:**

- **The CPU-cloud playbook repeats on accelerators.** Raw rental is the entry point; the durable margin sits in the software layer built on top (data, networking, security, storage → now training, routing, security monitoring, agent observability, context management, sandboxing).
- **Inference is the first layer, not the last.** Serving a model is the smallest slice of the eventual stack.
- **Not winner-take-all.** Customers demand choice and building blocks across both open and frontier models.
- **Scarce GPUs extend the game.** Capacity shortages push customers to shop around, which hands more players a shot at proving out their value add.
- **Acquisition ≠ retention.** Available GPUs win the customer; better software keeps them.
- **Verticalize chip → token.** The share goes to whoever pairs the best software with the fastest path to owning the full stack — and that has to be built now, while customers are still only asking for more compute.

**What the filings say about this thesis:**
- **Nebius is already buying the layers above inference.** In H1 2026 it acquired Tavily (search for AI agents), ClarifAI's inference and orchestration team and patents ($75M), and Eigen AI (inference, compression and fine-tuning). These deals added **$605.6M of goodwill**. [F2 F-2, F-9] [F1 F-30]
- **It already owns everything from data center to token.** That runs from its owned Finland data center and in-house server designs through to its own cloud platform. [F2 F-9]
- **The filings can't yet tell software from rental.** Revenue is reported as one AI cloud line, so the share of revenue from software is invisible. Ask for that split (see §11).

### 7.2 On-demand GPU price increase, effective Oct 1, 2026 [N] [S]

Nebius notified customers on 2026-09-17 of its second on-demand price increase this year. Per-GPU-hour list rates:

| Instance | Old | New | Change |
| --- | --- | --- | --- |
| NVIDIA H100 | $3.85 | $4.50 | ~+17% |
| NVIDIA H200 | $4.50 | $5.40 | ~+20% |
| NVIDIA B200 | $7.15 | $8.50 | ~+19% |
| NVIDIA B300 | $7.85 | $9.50 | ~+21% |

Non-GPU resources went up more:

- **AMD EPYC Genoa CPU-only instances:** ~+25%
- **Memory:** ~+41%
- **Unchanged:** RTX PRO 6000 and L40S. Multi-month reservations of large clusters can get discounts. [S]

**Context:** [N]
- **Second increase this year.** The May round averaged ~29% on on-demand capacity. Together, the two rounds put the B300 up **~56% year to date** ($6.09 → $7.85 → $9.50). *(One press report calls it the second increase "in three months"; the ~56% cumulative B300 figure matches.)* [S]
- **Stated reason:** a Nebius spokesperson said, "Demand for computing capacity to train and run AI models is surging."
- **Market reaction:** NBIS jumped ~9–11% on the announcement (Thursday, September 17).
- **Live price discovery:**
  - Nebius's first capacity auction cleared **15% above the highest price it had ever charged** for Blackwell-generation chips, and ~20% above Blackwell pipeline pricing.
  - Short-duration premium contracts are pricing at **$40–50M per MW**, vs. **$20–25M per MW** on core 1–3 year deals (see §7.3).
  - CEO Arkady Volozh said the company could "sell today our entire 2027 capacity" at current terms.
  - The Q2 group adjusted EBITDA margin was 41%, matching the filing's $236.2M on $582.3M. [F2 F-33]

**Read-through:** [N]
- **The regularizer is real, and it's priced.** Constrained supply isn't just drawing the fight out — it's letting Nebius reprice the same silicon twice in five months without losing the customer. That's the "getting a customer because you have available GPUs" phase paying cash today.
- **Raising list price on H100s is a supply statement, not a demand statement.** Last-gen Hopper repricing +17% means even the older fleet is sold out. Watch whether H100 rates hold once B300/Rubin capacity lands at scale — that's the first honest test of pricing power vs. scarcity rent.
- **Memory +41% > GPU +~20% is the tell.** The bottleneck is spreading past the accelerator to the rest of the box. That is the same "data, networking, storage" surface the hyperscalers monetized, showing up as a pricing lever before it shows up as a product.
- **Auction > list price.** The auction clearing 15% over the highest price ever charged says list rates are trailing the market. Expect a third hike, or expect more revenue to shift to auctioned/short-duration contracts at 2x the $/MW of core deals.
- **The risk to underwrite.** Price hikes are the easy revenue. They are also the part a competitor with free capacity can undercut tomorrow. The thesis above still holds: this buys time to build the software layer that makes the customer stay when someone else has GPUs at $7.85.

**Sizing (derived, with caveats):**
- **The increase mostly affects on-demand revenue.** Most revenue sits in long-term contracts with fixed pricing (the $37.5B RPO). The ~+20% list increase therefore lands mainly on the on-demand and short-term slice, which the filings don't disclose separately.
- **Margins benefit almost fully.** A price increase on hardware that's already deployed carries close to 100% incremental margin. Even a modest on-demand share could lift the AI cloud segment's 50% adjusted EBITDA margin. [F2 F-33]
- **Short-term pricing will show up in new contracts.** Premium short-duration deals at $40–50M per MW are 2x the 1–3 year deals. A rising share of them should appear as RPO growing faster than contracted MW.

### 7.3 Pricing per MW by contract length [N]

| Contract type | Annual revenue per MW | Notes |
|---|---|---|
| Short-term / premium | ~$40M (up to $40–50M) | Auctions cleared above list price [N] [S] |
| Mid-term (1–3 years) | **$20–25M** | Q2 2026 floor; roughly 2x 2026 base pricing. Nebius is holding back 2027 capacity, expecting higher prices [N] |
| Long-term (5 years, hyperscaler) | ~$12M | Cross-check: Microsoft's $17.4–19.4B over 5 years on ~300 MW at Vineland is **$11.6–12.9M per MW per year** *(derived)* [S] [N] |

**Correction:** an earlier version of this note guessed that "$ per MW" meant total contract value. The Microsoft cross-check shows it is **annual revenue per MW**.

**Open question for Q3:** even the 5-year tier is above the ~$7–11M of ARR per *connected* MW implied by 2026 guidance ($7–9B on 0.8–1.0 GW). One of three things explains it:
- guidance is conservative
- prices are quoted per IT MW rather than per grid MW (a PUE of 1.2–1.3 closes most of the gap)
- part of the connected capacity isn't billing yet

The scenario model uses the guidance-implied figure, so it's conservative if the tier prices are the right basis.

### 7.4 GPU unit economics: does the chip earn its keep? [N]

Per GPU, per year, at 70% utilization. Server costs: H100 ~$285K and B200 ~$450K per 8-GPU server. Power is at $0.08/kWh. Debt service is at the secured-facility rate (SOFR 3.88% + 2.50% ≈ 6.4%) [F2 F-34].

| | H100 (paid off) | B200 (new, debt-financed) |
|---|---|---|
| Price per GPU-hour assumed | $2.77 | $4.20 |
| Revenue at 70% utilization | ~$17.0K | **~$25.8K** *(corrected from $36.8K, which assumed 100%)* |
| Power and operations | ~$2.0K | ~$2.8K |
| Debt service | — | ~$14.8K |
| **Net per year** | **~$15K** | **~$8.2K** |
| Break-even utilization | — | ~48% |

While the debt is outstanding, a paid-off older GPU out-earns a new financed one. **Equilibrium:** a new financed B200 only matches a paid-off H100 running at 70% when it runs at **~89% utilization**, or rents for **~$5.31 an hour** at 70% *(derived)*. October's on-demand list prices ($8.50 B200, $4.50 H100) are well above that, so for now scarcity pricing keeps new chips past equilibrium. On top of that, software gains (compression, batching, speculative decoding: Eigen AI, Inferize) raise tokens per second on older chips every year. Together that sets a floor under older GPUs' economic life and supports a longer depreciation schedule. Full detail and open items are in the [review](../notes/2026-10-report-review.md).

---

## 8. Bull case

1. **Contracted, prepaid demand.** $37.5B RPO and $6.0B of customer cash already received. Customers are funding about half of the build-out. [F2]
2. **Margins are scaling.** AI cloud reached a 50% adjusted EBITDA margin in Q2, up from 10% a year earlier. [F2]
3. **A wave of capacity is about to go live.** $7.8B of equipment is installed or awaiting installation. [F2]
4. **NVIDIA is a shareholder.** It bought $2B of warrants in March 2026. [F2]
5. **Hidden assets.** ClickHouse ($1.5B book value at the last round mark), Toloka and Avride sit outside the AI-cloud multiple.
6. **Pricing power.** Two on-demand price increases this year (B300 ~+56% year to date), and an auction that cleared above the highest price ever charged. Premium short-term deals at $40–50M per MW, ~2x 1–3 year deals. [N] [S]
7. **Moving up the stack.** H1 acquisitions in inference, orchestration and agent search are the start of the software layer that turns renters into sticky customers. [N] [F2]

## 9. Bear case

1. **The funding gap is widening.** Q2 free cash flow was –$3.4B, and prepayments fell ~$2B quarter over quarter. Each new GW needs more converts or equity. [F2]
2. **Dilution.** ~38M shares or share equivalents were issued in H1 (21.1M NVIDIA warrants, 12.7M ATM, 3.8M for the Eigen acquisition). Add ~24M+ potential shares from the March converts, plus the 2025 and August 2026 notes. [F2]
3. **Concentration.** Three customers are 59% of revenue, and the receivables are just as concentrated. [F2]
4. **GAAP losses will widen.** Depreciation on $7.8B of new assets, plus ~$119M of quarterly interest expense. [F2]
5. **Fixed commitments.** ~$540M per year in power obligations, plus Bloom, whether or not GPUs are rented. [F2] [F1]
6. **Avride burns cash.** –$40M adjusted EBITDA per quarter on $1M of revenue, partly funded by outside SAFEs ($178M liability). [F2 F-18, F-33]
7. **Scarcity rent, not pricing power.** Price increases are the easy revenue, and a competitor with spare capacity can undercut them. The first real test is whether H100 rates hold once B300 and Rubin capacity arrives at scale. [N]
8. **Site execution.** About 94% of contracted MW isn't live yet. Specific risks: the Birmingham lawsuit, Béthune permitting, and Pennsylvania construction not yet confirmed. [N] [S]

---

## 10. Valuation framework

- **EV:** market cap on a **fully diluted** count (outstanding + NVIDIA warrants + convert conversion shares) + other debt − cash (including restricted cash). If you count the conversion shares, don't also add the converts as debt.
- **EV / year-end ARR:** compare against the $7–9B guidance and against peers such as CoreWeave.
- **EV / 2027E adjusted EBITDA:** ~40% group margin on the 2027 revenue run-rate.
- **Sum of the parts:** AI cloud + ClickHouse ($1.52B carrying value) + Toloka ($86.5M) + Avride (last round) + TripleTen.
- **Scenario model:** [`models/output/scenarios.md`](../models/output/scenarios.md) has bear, base and bull paths for ARR, revenue, EBITDA, capex and the 2027 funding gap. Plug its 2027 EBITDA into the multiple above.
- **Peers:** [`research/peer-comparison.md`](peer-comparison.md) compares Nebius with CoreWeave and IREN on growth, backlog, capex intensity and funding.

---

## 11. What to watch in Q3 2026

| # | Item | Why |
|---|---|---|
| 1 | ARR vs. the $7–9B year-end path | Needs ~$5B+ by September to stay on track |
| 2 | Deferred revenue change in the quarter | Did prepayments rebound from Q2's $1.2B? |
| 3 | Free cash flow and new financing | Sizes future dilution |
| 4 | Assets not yet in use → placed in service | Leading indicator of revenue and D&A |
| 5 | RPO and its 24-month share | Backlog growth and conversion speed |
| 6 | Top-customer percentages | Concentration trend |
| 7 | SBC | Does it fall back after the Q2 acquisition spike? |
| 8 | Guidance changes (capex, ARR, power) | Any cut breaks the thesis timeline |
| 9 | Third on-demand price increase, or a shift to auctions and short-term deals | Is list price still trailing the market? [N] |
| 10 | H100 on-demand rate as Blackwell and Rubin capacity lands | Pricing power vs. scarcity rent [N] |
| 11 | Any disclosure of software or platform revenue (inference, agents, Tavily) | The test of the §7 thesis [N] |
| 12 | Basis of "$ per MW" (IT vs. grid MW) and ARR per connected MW | Reconciles the pricing tiers with guidance (§7.3) |
| 13 | Active MW and site milestones (Birmingham, Béthune, Vineland Bloom) | Tracks the author's pipeline (§6) |

---

## Sources

- **[F2]** Nebius Group N.V., Form 6-K, Exhibit 99.2, *Unaudited Condensed Consolidated Financial Statements as of and for the three and six months ended June 30, 2025 and 2026* (exhibit file `nbis-20260812xex99d2.htm`). Page numbers are given as F-x. Filing list: [SEC EDGAR, CIK 1513845](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001513845&type=6-K).
- **[F1]** Nebius Group N.V., Form 6-K dated 2026-05-20, Exhibit 99.2, *Unaudited Condensed Consolidated Financial Statements as of and for the three months ended March 31, 2025 and 2026*.
- **[PR]** Company releases and letters, read via excerpts:
  - [Q2 2026 results release](https://www.businesswire.com/news/home/20260812963359/en/Nebius-reports-second-quarter-2026-financial-results)
  - [Q2 2026 shareholder letter](https://assets.nebius.com/assets/4462517b-ce83-41f2-96ed-f2ac1bc06a05/SHLQ226%20(1).pdf-0)
  - [Q4 2025 shareholder letter](https://assets.nebius.com/assets/e59fb92e-9027-473a-8cac-04f9d2e9ea9a/Shareholder%20Letter%20Q4%202025.pdf?cache-buster=2026-02-12T11%3A43%3A13.446Z)
  - [$5.0B convertible pricing](https://nebius.com/newsroom/nebius-group-announces-pricing-of-upsized-private-offering-of-5-0-billion-of-convertible-senior-notes)
- **[S]** Secondary:
  - [TIKR on Q1 2026](https://www.tikr.com/blog/nbis-has-gained-167-in-2026-the-revenue-chart-explains-why)
  - [Yahoo Finance, Q2 call highlights](https://finance.yahoo.com/technology/ai/articles/nebius-group-q2-earnings-call-150444472.html)
  - [Converge Digest on the Microsoft and Meta deals](https://convergedigest.com/nebius-builds-momentum-with-17-19b-microsoft-deal-and-3b-meta-contract/)
  - [TIKR on the Meta deal](https://www.tikr.com/blog/nebius-nbis-stock-rallies-15-after-12-billion-usd-meta-infrastructure-deal)
  - [24/7 Wall St. (2026-10-01)](https://247wallst.com/investing/2026/10/01/just-how-exposed-is-nebius-at-235/)

- **[N]** Author's notes: [`notes/2026-10-nebius-report-draft.md`](../notes/2026-10-nebius-report-draft.md) (reviewed in [`notes/2026-10-report-review.md`](../notes/2026-10-report-review.md)) and the earlier running notes, `Nebius.MD` (thesis added 2026-09-20; pricing logged 2026-09-22). Its figures for the October 1 price increase match these press reports:
  - [Silicon UK](https://www.silicon.co.uk/cloud/ai/nebius-prices-ai-631634)
  - [FourWeekMBA](https://fourweekmba.com/ai-nebius-lifts-on-demand-gpu-prices-up-to-21-from-1-october/)
  - [Spheron](https://www.spheron.network/blog/nebius-gpu-price-hike-2026-h100-to-b300-rates-rise-up-to-21/)
  - [Finviz](https://finviz.com/news/393074/nebius-shares-jump-111-following-gpu-cloud-service-price-increases)
  - [Stocktwits](https://stocktwits.com/news-articles/markets/equity/nbis-stock-rallies-as-neocloud-operator-hikes-prices-peers-iren-crwv-jump-as-well/cZtrBwmRB5R)

**Still to verify against primary sources:**
- ARR history and 2026 guidance (press release / Exhibit 99.1)
- Power metrics
- Microsoft and Meta contract values
- Conversion rates on the 2025 notes (20-F)
- Terms of the August 2026 convertible and exchange
- The May 2026 price round (~29% average; B300 $6.09 → $7.85), auction results, and per-MW pricing on premium contracts
