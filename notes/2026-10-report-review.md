# Review of the October 2026 Draft Report

*Fact-check of [`2026-10-nebius-report-draft.md`](2026-10-nebius-report-draft.md) against the Q1 and Q2 2026 6-K financial statements ([F1], [F2]) and press coverage ([S]).*

**Verdicts:**
- ✅ **Confirmed:** matches a filing or reliable source.
- ⚠️ **Fix:** an arithmetic or factual error.
- ❓ **Unverified:** no source found yet; it needs one before it moves into `research/`.

---

## Summary

The draft's core claims hold up well against the filings. Two numbers need fixing:
- **B200 revenue:** the 70% utilization was left out of the calculation.
- **Token cost example:** 151B tokens and $108K a month don't reconcile.

Three claims need sources:
- the "no more hyperscaler deals" quote
- the $170B three-year capex plan
- the 500M share base in the dilution math

One claim is out of date: the Birmingham substation.

The most important confirmation is the **pricing tiers**. They make clear that "$ per MW" is *annual revenue* per MW, not total contract value. The initiation note had that wrong and has been corrected.

---

## Claim by claim

### Business model
| Claim | Verdict | Evidence |
|---|---|---|
| Netherlands-based AI cloud that designs and runs its own data centers | ✅ | Amsterdam HQ; full-stack infrastructure "spanning data centers, large-scale GPU clusters and servers designed in-house" [F2 F-9] |
| Revenue not broken out by bare metal / managed / serverless | ✅ | Only one AI cloud segment is reported [F2 F-33] |

### Capacity
| Claim | Verdict | Evidence |
|---|---|---|
| ~200–275 MW active today | ✅ plausible | ~170 MW active at end-2025 per the Q4 2025 letter [PR]; site build-up is the author's estimate |
| ~4 GW contracted, by site | ✅ arithmetic | Site totals add up: US owned 2.70 + US leased 0.47 + Europe 0.80 + Israel 0.08 = **4.05 GW**. The company's year-end target is 5 GW [PR] |
| "94% of contracted capacity is yet to come" | ✅ | ~250 MW / 4.05 GW ≈ 6% active |
| Vineland Bloom fuel cells, 250 MW, none operating | ✅ partly | A 250 MW guaranteed Bloom agreement was signed May 14, 2026 [F1 F-30]. The filing doesn't name the site or say whether any of it is operating |
| Birmingham "denied substation approval" puts Q4 2026 energization at risk | ⚠️ **out of date** | On Mar 26 the zoning board denied a *switching station*, not the substation. A city legal memo later found neither needed zoning-board approval, and the city's moratorium doesn't apply. **A Humane Society lawsuit is pending**, and that's the live risk. [Birmingham Watch](https://birminghamwatch.org/?p=129416), [WBRC](https://www.wbrc.com/2026/04/10/zoning-clarification-allows-key-parts-ai-factory-project-move-forward-oxmoor-valley/), [Let's Data Science](https://letsdatascience.com/news/humane-society-challenges-nebius-alabama-data-center-6590a952) |
| Béthune first phase missed its summer target | ❓ | No coverage found |
| Company "connected power" vs. the author's "connected" (0–50 MW) | ⚠️ **different definitions** | The company guides 0.8–1.0 GW *connected* by year-end, becoming active in 1H 2027 [PR]. That bucket includes capacity the author counts as active or under construction. Label which definition is in use whenever the two are compared |

### Pricing per MW
| Claim | Verdict | Evidence |
|---|---|---|
| Tiers: short-term ~$40M, 1–3 year $20–25M, 5-year ~$12M per MW | ✅ consistent | The Microsoft deal ($17.4–19.4B over 5 years [S]) spread over Vineland's 300 MW is **$11.6–12.9M per MW per year**, which matches the 5-year tier. So these figures are *annual revenue per MW*. IREN reports >$20M per MW on 3-year deals [S] |
| Implication | — | Even the 5-year tier ($12M) is above the ~$7–11M ARR per *connected* MW implied by 2026 guidance ($7–9B on 0.8–1.0 GW). One of three things is true: guidance is conservative, prices are quoted per IT MW rather than per grid MW (a PUE of ~1.2–1.3 would close most of the gap), or some connected capacity isn't billing yet. **Worth asking on the Q3 call** |

### Funding
| Claim | Verdict | Evidence |
|---|---|---|
| Meta and Microsoft deals carried ~50% prepayments | ✅ | Prepayments covered 54% of H1 2026 capex: $4,397.7M deferred-revenue increase vs. $8,130.3M capex [F2 F-7, F-19] |
| The CRO said there will be no more hyperscaler deals | ❓ **no source found** | The only Boroditsky quotes found say the opposite: "We're not going to miss out on an opportunity like that," plus diversification if hyperscalers pull back ([Fierce Network](https://www.fierce-network.com/cloud/nebius-isnt-really-worried-about-ai-bubble-bursting)). His first name is **Marc**. Find the original quote, or drop the claim |
| ~$15B Meta backstop | ✅ partly | Press reports a ~$27B Meta deal: ~$12B dedicated plus an option component [S]. The structure isn't in the filings |
| ~$170B of capex over 3 years | ❓ | No source found. It's ~$57B a year vs. 2026 guidance of $20–25B [PR]. If it comes from your model rather than management, label it as an estimate |
| $50–60M per MW all-in; 5 GW = $250–300B | ✅ arithmetic | 5,000 MW × $50–60M = $250–300B |
| +35% dilution over 4 years at 8% a year | ✅ arithmetic, ❓ base | 1.08⁴ = 1.36. But shares were **271.9M outstanding + 21.1M NVIDIA warrants = 292.9M** at June 30 [F2 F-5, F-31], ~309M after the August note exchange. Clarify whether "500M shares" is the ending count, a fully diluted count including converts, or a typo |
| Secured loan at SOFR + 2.5% | ✅ | July 10, 2026 facility: ~$775M at SOFR + 2.50%, maturing Oct 31, 2030 [F2 F-34] |

### GPU unit economics
| Claim | Verdict | Evidence |
|---|---|---|
| H100: $36K per GPU ($285K server) | ✅ arithmetic | $285K / 8 = $35.6K |
| B200: $56K per GPU ($450K server) | ✅ arithmetic | $450K / 8 = $56.3K |
| H100: $2.77 × 8,760 h × 70% ≈ $17K | ✅ | $16,986 |
| B200: $4.20 × 8,760 h × 70% ≈ **$36.8K** | ⚠️ **fix** | $36.8K is at **100%** utilization. At 70% it's **$25.8K**. After $2.8K of power and ops and $14.8K of debt service, a new financed B200 nets about **$8.2K a year**, not ~$19K. Break-even utilization ≈ (2.8 + 14.8) / 36.8 ≈ **48%** |
| $14.8K a year of debt service on a B200 | ✅ plausible | Paying off $56.3K at 6.38% over ~4.5 years (the facility runs to 2030) ≈ $14.8K a year |
| "Equilibrium" definition | — | With the fix, a paid-off H100 nets **~$15K** a year vs. **~$8K** for a new financed B200 at 70%. Paid-off older GPUs out-earn new ones while the debt is outstanding, which supports the draft's "older GPUs are a floor" argument. Add utilization sensitivity (50%, 70%, 90%) to finish the section |

### Software layer and acquisitions
| Claim | Verdict | Evidence |
|---|---|---|
| Tavily acquired in February | ✅ | Feb 19, 2026 [F2 F-13] |
| Eigen AI bought in June; about half the price was retention | ✅ **more than half** | Closed **June 10, 2026**. Purchase price **$331.4M** ($8.4M cash + $24.3M deferred cash + ~1.4M shares worth $298.7M). Separately, **~2.4M shares worth $508.1M** vest over 4 years with continued employment, plus $10.5M cash and $30.6M deferred cash, all booked as compensation [F2 F-15/16]. Retention = $549.2M of ~$880.6M total, **~62%**. This is also why Q2 SBC jumped to $102.5M |
| Inferize is the newest acquisition | ✅ | Announced **Oct 1, 2026**. Inferize targets cold-start delays in loading and scaling models, and is going into Token Factory. Terms undisclosed; press estimates $100–150M; 17 staff in Tel Aviv; founders previously built Granulate (sold to Intel). [Nebius newsroom](https://nebius.com/newsroom/nebius-acquires-inferize-to-strengthen-nebius-token-factorys-production-inference-stack), [Calcalist](https://www.calcalistech.com/ctechnews/article/byzggtiqgx), [Dealroom](https://dealroom.co/news/158426-nebius-buys-10-month-old-israeli-startup-inferize-for-up-to-130m/) |
| Token Factory launched November 2025 | ❓ | Not in the filings checked; find the launch announcement |
| Several agents all day ≈ 151B tokens ≈ $108K a month on the Claude API | ⚠️ **doesn't reconcile** | Those two numbers imply ~$0.72 per million tokens. Check that against current Claude API pricing for the model and the input/output mix you assumed. One of the two figures is likely off |

### Demand and notes
| Claim | Verdict | Evidence |
|---|---|---|
| Memory, power, optics and grid are the bottlenecks, not chips | ✅ supported | On Oct 1, memory prices rose **+41%** vs. ~+17–21% for GPUs [S]. Long-dated power commitments of ~$540M a year in 2027–2030 [F2 F-26] |
| NVIDIA quotas push hyperscalers to neoclouds | ❓ | Opinion; no source given |

---

## Suggested next edits to the draft
1. Fix the B200 math (70% → $25.8K) and add a utilization sensitivity table.
2. Source or drop the "no more hyperscaler deals" quote; correct the name to Marc Boroditsky.
3. Replace "denied substation" with the switching-station ruling, the city memo and the pending lawsuit.
4. Say whether $/MW figures are per IT MW or per grid MW, and annual (they appear to be).
5. Clarify the 500M share base and the $170B capex source. Upload `NBIS_5GW_Funding_Model.xlsx` to reconcile with the repo's scenario model.
6. Finish the Inferize section (facts above) and the equilibrium conclusion.

## Sources
- **[F1]**, **[F2]**: Nebius Q1 and Q2 2026 6-K, Exhibit 99.2. See `research/nebius-initiation.md` for full references.
- **[PR]**: Nebius Q2 2026 release and shareholder letter; Q4 2025 letter.
- **[S]**: Press cited inline, plus the Microsoft and Meta deal coverage cited in the initiation note §5.
