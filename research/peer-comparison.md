# Neocloud Peer Comparison: Nebius vs. CoreWeave vs. IREN

*As of 2026-10-11, using each company's latest reported quarter (the quarter ended June 30, 2026 for all three).*

> **Not investment advice.** Nebius figures come from its Q2 2026 6-K (Exhibit 99.2, page numbers F-x) unless tagged otherwise. **CoreWeave and IREN figures are secondary** (press and aggregator coverage of their releases), and sources disagree on some of them; see [Caveats](#caveats).

---

## TL;DR

- **Nebius is the fastest-growing and the least levered of the three, and the most capital-hungry relative to its size.** It is smaller than CoreWeave (Q2 revenue $0.58B vs. $2.58B) but grew 454% vs. 112%. Its backlog covers **~16x** annualized revenue vs. ~10x at CoreWeave. 2026 capex guidance is **~7x** 2026 revenue vs. ~3x at CoreWeave.
- **They fund themselves differently.** CoreWeave runs on secured debt and leases (~$25B of debt plus ~$10B of leases reported at end-Q1; ~$640M of Q2 interest). Nebius runs on customer prepayments ($6.0B of deferred revenue), unsecured convertibles and equity. That means less leverage and more dilution: Nebius's risk is the share count, CoreWeave's is the debt.
- **Contract pricing looks similar across the group.** Nebius's 1–3 year deals are reported at ~$20–25M of annual revenue per MW (~$12M on 5-year hyperscaler deals), and IREN's recent 3-year deals at >$20M per MW, with talks around $25M. So the industry rate looks similar. Where Nebius stands out is in **raising on-demand list prices twice in 2026** and running auctions that clear above list price (see the initiation note, §7).
- **What it means for NBIS:** Nebius is priced as the higher-growth, earlier-stage version of CoreWeave. If it hits its 2026 ARR guidance, it would go from ~1/4 of CoreWeave's quarterly revenue to ~40% of CoreWeave's year-end ARR within a year. That convergence is the core of the bull case.

---

## Side by side

| | **Nebius (NBIS)** | **CoreWeave (CRWV)** | **IREN (IREN)** |
|---|---|---|---|
| Quarter ended June 30, 2026 | Q2 2026 | Q2 2026 | Fiscal Q4 2026 |
| Revenue | **$582.3M** [F2 F-3] | ~$2.58B [S1] | $137.2M total; **$70.5M AI cloud** [S3] |
| YoY growth | **+454%** | +112% [S1] | AI cloud up ~2.1x QoQ (from $33.6M) [S3] |
| Profitability metric | Adj. EBITDA **$236.2M (41%)**; AI cloud 50% [F2 F-33] | Adj. *operating income* $128M (~5%) [S1] | Adj. EBITDA $19.2M [S3] |
| GAAP net income (loss) | $(190.4)M [F2 F-3] | ~$(626)M [S1] | ~$(684)M, mostly impairments [S3] |
| Interest expense, quarter | $119.1M (20% of revenue) [F2 F-3] | ~$640M (~25% of revenue) [S1] | n/a |
| Backlog | **RPO $37.5B** (36% within 24 months) [F2 F-19] | ~$104B, plus >$25B of commitments added in early Q3 [S1] | $4B contracted ARR for 2026 capacity [S3] |
| Backlog / annualized quarterly revenue *(derived)* | **~16x** | ~10x | — |
| 2026 revenue guidance | $3.0–3.4B [PR] | $12.4–13.2B [S1] | — |
| Year-end 2026 ARR target | $7–9B [PR] | $18.5–19.5B [S1] | >$4B by the December quarter [S3] |
| ARR target / annualized Q2 revenue *(derived)* | **~3.4x** | ~1.8x | — |
| 2026 capex guidance | $20–25B [PR] | $35–39B (raised from $31–35B) [S1] | — |
| 2026 capex / 2026 revenue at guidance midpoints *(derived)* | **~7.0x** | ~2.9x | — |
| Power | 5 GW contracted target; 0.8–1.0 GW connected by YE26 [PR] | >1 GW active, 3.5 GW contracted; >1.85 GW active target by YE26 [S2] | ~200 MW active, >5 GW contracted (older figure) [S2] |
| Reported contract pricing | ~$20–25M per MW per year on 1–3 year deals; ~$12M on 5-year deals; ~$40M short-term [N] | — | >$20M per MW on 3-year deals; talks around $25M [S3] |
| Main funding sources | Prepayments ($6.0B deferred revenue), converts ($10.0B accreted principal), ATM, NVIDIA warrants [F2] | Secured debt (~$25B) and leases (~$10B), reported at end-Q1 [S2] | $3.6B investment-grade GPU financing at 6.0% for the Microsoft contract [S3] |
| Anchor customers | Three unnamed customers = 59% of revenue; Microsoft and Meta per press [F2 F-17] [S] | Not covered in sources used here | Microsoft ($9.7B contract) [S2] |

---

## What this says about Nebius

1. **The growth premium has a reason.** Nebius has the most backlog per dollar of current revenue (~16x vs. ~10x) and the steepest guided ARR ramp (~3.4x vs. ~1.8x). Its backlog is also shifting toward near-term recognition (36% due within 24 months, up from 29% in March). [F2 F-19]
2. **Margins are on a different basis.** Nebius's 41% is adjusted *EBITDA*. CoreWeave headlines adjusted *operating income*, which is after depreciation. They are not comparable. On a like-for-like operating basis, Nebius is still loss-making (Q2 operating loss $175.9M). [F2 F-3] Compare EBITDA to EBITDA, or EBIT to EBIT, once CoreWeave's EBITDA is pulled from its release.
3. **Leverage vs. dilution.** CoreWeave's interest burden (~25% of revenue) is the cost of debt-funding the build-out. Nebius's interest is lower (20% of revenue), and much of it is non-cash: Q2 included $67.0M of convertible discount accretion against $40.5M of contractual coupon, before $40.2M was capitalized. [F2 F-28] But its converts carry a $20.8B fair value against $8.5B on the books, and it issued ~38M share equivalents in H1. [F2 F-29, F-31] If you care about dilution, CoreWeave is safer. If you care about refinancing risk, Nebius is.
4. **Capex intensity is the Nebius-specific risk.** Spending ~7x its 2026 revenue (vs. ~3x at CoreWeave) means Nebius's 2026 results depend heavily on capacity built for 2027. Any slip in connected power hits Nebius harder. The scenario model ([`models/output/scenarios.md`](../models/output/scenarios.md)) shows a 2027 funding gap of ~$14–24B across scenarios, at the author's all-in capex of $50–60M per MW.
5. **Pricing is industry-wide, and so is the scarcity.** IREN's >$20M per MW on 3-year deals matches Nebius's $20–25M per MW on 1–3 year deals, so the long-term contract market is pricing consistently. The October 1 on-demand increase and above-list auctions are Nebius-specific evidence that the spot market is tighter than the contract market. [N]

---

## Caveats

- **CoreWeave and IREN figures are secondary** and should be checked against their filings. Known conflicts:
  - CoreWeave's Q2 capex is reported as both $9.4B and $6.4B, so it is left out.
  - CoreWeave's debt and power figures are as of Q1 2026.
  - IREN's net loss differs between the Q4 and full-year figures ($684M vs. $702.6M).
- **Fiscal calendars differ.** IREN's fiscal year ends in June, so its "Q4 FY2026" is the same calendar quarter as the others' Q2 2026.
- **Metric definitions differ:** ARR (Nebius: AI cloud run-rate; IREN: contracted vs. operating ARR), backlog (RPO vs. contracted ARR), and adjusted profit (EBITDA vs. operating income).
- **Not covered:** Lambda (private, no audited figures), Oracle OCI and the hyperscalers (segments inside much larger companies).

## Sources

- **[F2]** Nebius Group N.V., Form 6-K, Exhibit 99.2, Q2 2026 unaudited financial statements (page numbers F-x). [SEC EDGAR, CIK 1513845](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001513845&type=6-K).
- **[PR]** [Nebius Q2 2026 results release](https://www.businesswire.com/news/home/20260812963359/en/Nebius-reports-second-quarter-2026-financial-results) and [Q2 2026 shareholder letter](https://assets.nebius.com/assets/4462517b-ce83-41f2-96ed-f2ac1bc06a05/SHLQ226%20(1).pdf-0).
- **[N]** The author's notes; see `research/nebius-initiation.md` §7.
- **[S1]** CoreWeave Q2 2026 coverage:
  - [01net (release reprint)](https://www.01net.it/coreweave-reports-strong-second-quarter-2026-results/)
  - [Pulse 2.0](https://pulse2.com/coreweave-revenue-backlog-reaches-104-billion-before-another-25-billion-of-new-commitments/)
  - [Beancount.io](https://beancount.io/blog/2026/09/22/coreweave-fy2026-q2-earnings-analysis)
  - [Channelchek](https://dashboard.channelchek.com/?p=104902)
  - [Quartr event summary](https://quartr.com/events/coreweave-inc-crwv-q2-2026_F6huCJA4)
- **[S2]** Peer comparisons:
  - [INDmoney, CoreWeave vs. IREN vs. Nebius](https://www.indmoney.com/blog/us-stocks/coreweave-vs-iren-vs-nebius-ai-cloud-stocks-analysis)
  - [The Next Platform (2026-08-14)](https://www.nextplatform.com/cloud/2026/08/14/the-neoclouds-build-cash-hoards-faster-than-revenues/5288040)
  - [Exoswan](https://exoswan.com/neocloud-stocks)
- **[S3]** IREN FY2026 results:
  - [IREN release](https://irisenergy.gcs-web.com/news-releases/news-release-details/iren-reports-fy26-results)
  - [Pulse 2.0](https://pulse2.com/iren-contracted-arr-reaches-4-billion-as-ai-cloud-revenue-jumps-nearly-eightfold/)
  - [KuCoin News](https://www.kucoin.com/news/flash/iren-q4-fy2026-revenue-meets-expectations-ai-cloud-revenue-doubles)
- **[S]** Press identification of Nebius's largest customers; see the initiation note, §5.
