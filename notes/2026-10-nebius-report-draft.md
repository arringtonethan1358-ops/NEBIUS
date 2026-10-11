# Nebius Report: Author's Draft

*Working draft, October 2026. Text is the author's own; figures are the author's estimates unless a source is given. For the fact-check against the 6-K filings, see [`2026-10-report-review.md`](2026-10-report-review.md).*

> **Reviewer edits (2026-10-11):** corrections and additions from the fact-check are marked ✎, in italics or as new sub-sections. The author's original wording is unchanged except where ✎ notes a correction. Items still waiting on the author are marked **[needs source]**.

---

## What do they do?

Nebius is Netherlands AI cloud provider that designs and operates their own datacenters. They rent out compute to hyperscalers as well as developer teams, and individual developers They only use NVIDIA GPUs in their datacenters such as H100s, H200s, B200s, B300s, GB200 NVL72, GB300s NVL72, L40s, Vera Rubin NVL72s (Not in production yet). They have the option to rent out their compute in a few different ways with Bare Metal, Managed Kubernetes/Slurm Clusters, or Serverless. Bare Metal is essentially renting out the physical GPU server itself, with no virtualization layer. Bare Metal is good for buyers that want total custom control of the GPU server. For Managed Kubernetes, Nebius operates the orchestration, networking, and storage while the customers run workloads. Serverless is how token factory makes money with dev teams, as well as individual developers. Nebius doesn't break out these three segments in revenue.

## Active Megawatts

As of today im estimating 200-275 MW (94% of contracted capacity is yet to come)

- Vineland, NJ 100-150 MW
- Mäntsälä, Finland 75MW
- London, Iceland, Israel, Paris, Kansas City, Minnesota all collectively make up 45-50MW total

## Connected Megawatts

I'm estimating 0–50 MW effectively nothing. "Connected" means power is flowing but no revenue is being generated yet: the building is done, the network and GPU clusters are being deployed, the customer is onboarding. Management says this stage takes a few months, and because it converts to active that quickly, it never accumulates into a measurable bucket. Nobody discloses it at the site level, so this is the least observable stage of the pipeline. You can't watch energization arrive, you only see it after it becomes revenue. *✎ Note: this is narrower than the company's definition. Its 0.8–1.0 GW "connected" target for year-end 2026 also includes capacity counted here as active or under construction, so the two numbers aren't comparable.* The things to watch instead: Vineland's Bloom fuel cells (250 MW being installed, zero operational today), Birmingham's denied substation approval (first energization guided for Q4 2026 is at risk) *✎ Correction: the zoning board denied a* switching station*, not the substation, and a city legal memo later found neither needed its approval. The live risk is a pending Humane Society lawsuit ([Birmingham Watch](https://birminghamwatch.org/?p=129416), [WBRC](https://www.wbrc.com/2026/04/10/zoning-clarification-allows-key-parts-ai-factory-project-move-forward-oxmoor-valley/))*, and Béthune's first phase, which missed its summer target and is still in permitting.

## Under Construction Megawatts

1 GW under construction (range 0.8–1.3 GW). Nebius has never published a number, so this is my estimate.

- 0.3–0.6 GW finishing by end of 2026 leased sites plus Birmingham's first phase
- 0.5–0.8 GW for 2027 first phases of Missouri and Pennsylvania plus Meta's second deal
- 3.1–3.8 GW of the 5 GW target hasn't started construction. Pennsylvania construction still isn't confirmed.

## Contracted Megawatts

4ish GW contracted after accounting for active, connected, and constructed

- US owned 2.7 GW: Missouri 1200 MW, Pennsylvania 1200 MW, Birmingham 300 MW (Missouri is "up to" 1.2 GW, real number is probably closer to 800 MW)
- US leased 0.47 GW: Vineland 300 MW, Oklahoma 100+ MW, Kansas City 40 MW, Minnesota 31 MW est
- Europe 0.8 GW: Lappeenranta 310 MW, Béthune 240 MW, UK 65 MW, Finland 145 MW, Estonia 22 MW, Spain 18 MW
- Israel 0.08 GW: Masmiyya 22 MW, Beit Shemesh 58 MW
- New since May: UK 22 MW, Spain 18 MW, Estonia 22 MW, Mäntsälä 2 (70 MW), Vantage Newport (MW not disclosed)

## Revenue per Megawatt

As of Q2 26 the most recent quarter has pricing per MW at a floor of 20M-25M. This is roughly 2x the 2026 base MW pricing. Nebius also states that they are reserving capacity for 2027 because they believe they can sell MW for higher prices. Short term prices for MWs have reached 40M. The team does not break out the categories but there are 3 different customer types. There is short term (40M per MW), Mid term 1-3 years (20M-25M per MW), and Long term 5 years (12M per MW). *✎ These are annual revenue per MW: Microsoft's $17.4–19.4B over 5 years on ~300 MW at Vineland is $11.6–12.9M per MW per year, matching the 5-year tier. Open question: is that per IT MW or per grid MW? Even $12M is above the ~$7–11M of ARR per connected MW implied by 2026 guidance.*

## Equity and Debt

As of today the CRO Mark a Boroditsky's announced that there are no longer going to be any hyperscaler deals. **[needs source]** *✎ No source found for this. The CRO is Marc Boroditsky, and the quotes on record point the other way ("We're not going to miss out on an opportunity like that," [Fierce Network](https://www.fierce-network.com/cloud/nebius-isnt-really-worried-about-ai-bubble-bursting)). Link the original, or drop the claim.* For the past year Nebius has been signing Meta and Microsoft deals at 50% prepayments but this is more so to access cheap financing. If Nebius can obtain cheap capital off of a 15 billion dollar backstop by META that is a much more favorable outcome opposed to convertible notes, and Non secured loans. Nebius plans to spend about 170B over the next 3 years building out datacenters. **[needs source]** *✎ That's ~$57B a year vs. 2026 guidance of $20–25B. A search found no public source for $170B. The closest public figures: NVIDIA has committed to support Nebius building >5 GW by 2030, and Nebius plans >1 GW of new capacity in 2027 ([Nasdaq/Zacks](https://www.nasdaq.com/articles/nebius-heavy-capex-push-can-customer-prepayments-ease-strain)). At $50–60M per MW, 3 GW over three years would be $150–180B, so $170B reads as the author's own estimate. Label it that way, or cite the funding model.* Each Datacenter costs about 50-60 billion (will probably continue to move higher due to increasing costs) 50-60 billion is 250-300 billion in capex. Funding the guided 5GW build through 2030 at 50-60M per MW implies +35% dilution over 4 years in the base case at 500M shares, increasing 8% a year, **[needs source]** *✎ 1.08⁴ = 1.36, so the math checks. But shares were 271.9M outstanding plus 21.1M NVIDIA warrants (292.9M) at June 30 [Q2 6-K F-5, F-31], ~309M after the August note exchange. Say whether 500M is the ending count or a fully diluted count including converts.* and 95B-115B in debt , 55B of it is secured debt.

*Working model: `NBIS_5GW_Funding_Model.xlsx` (author's spreadsheet, not yet in the repo).*

## GPU depreciation (does the chip earn its keep)

H100s cost around 36k each inside a full server (285k server) and B200s are 56k each inside a full server (450k server).

H100: at 70% utilization $2.77 times 8760 hours you're getting 17k per GPU minus the power at .08/kWh works out to about 2k in power plus ops. That's 15k that GPU earns

B200: at 70% utilization $4.20 times 8760 hours you're getting ~~36.8k~~ **25.8k** per GPU *(✎ 36.8k is the 100% figure)* minus the power at .08/kWh works out to about 2.8k in power plus ops. The cheap rate is 6.4% SOFR at 3.88% plus 2.5 points which is what Nebiuses secured loan pays, so subtract 14.8k for debt payment. *✎ That leaves ~8.2k a year for a new financed B200.*

My definition of reaching equilibrium is when the cost of buying and financing a new GPU to rent out is yields the same as a paid off vintage GPU.

### ✎ Utilization sensitivity and the equilibrium point

Net per GPU per year, at the rates above. Power and operations are held at the estimates above; debt service is ~$14.8K a year at ~6.4% until the loan is paid off.

| Utilization | H100 (paid off, $2.77/h) | B200 (new, financed, $4.20/h) | B200 (paid off, $4.20/h) |
|---|---|---|---|
| 50% | ~$10.1K | ~$0.8K | ~$15.6K |
| 70% | ~$15.0K | ~$8.2K | ~$23.0K |
| 90% | ~$19.8K | ~$15.5K | ~$30.3K |

**Equilibrium:** a new financed B200 matches a paid-off H100 running at 70% only when it runs at **~89% utilization**, or when it rents for **~$5.31 an hour** instead of $4.20 at 70%. Below that, the paid-off older chip earns more per GPU.
- **Break-even:** the new B200 covers its power and debt at ~48% utilization.
- **List prices:** on-demand list prices since Oct 1 ($8.50 B200, $4.50 H100) are far above these contract-style rates. At list price and 70% utilization, a financed B200 nets ~$34.5K and a paid-off H100 ~$25.6K.

So scarcity pricing pushes new chips well past equilibrium, and the open question is how long those prices hold.

## The Importance of Recent Acquisitions

Nebius token Factory was announced back in November of last year, with the goal of making inference more efficient and economical at scale. Bare Metal is a commodity, so I would imagine Nebiuses long term goal is not to rent out bare metal compute. Managed inference flips the unit economics to the sale of the token versus the GPU per hour metric. I will get to it later in this report, but owning the entire stack allows Nebius to optimize token efficiency leading to higher margins. As long as Nebius can bring down the cost per token on their side faster than the rate they charge for tokens in the market, they will be a big winner on margins. You may have seen charts showing that token costs are dropping enormously each year, and the market initially mistook it for a bad thing, but its actually very helpful for the long-term economics of AI. Right now if you were to employ an AI agent, you would very quickly run out of tokens. Running several agents all at once all day would cost around 151 billion tokens or 108k a month, using Claudes anthropic through its API. **[needs source]** *✎ These two figures imply ~$0.72 per million tokens. Check them against current Claude API pricing for the model and input/output mix you assumed; one of the two is likely off.* I continue to see signs we haven't reached mass enterprise adoption for AI agents yet, as they can be hard to configure and setup for enterprises. This leads me to believe that although demand for compute is already high, there is a second wave of demand coming for compute. I believe that as humanity continues to find new use cases for compute, the ceiling for compute demand will continue to rise (Yes I know I could've just stated Jevons paradox). Factor this with margin expansion from Nebius bringing their cost to serve tokens down (keeping the additional margin) while continuing to discount token prices to the consumer.

### Tavily

Im not going to spend too much time explaining specifically what they do, but just understand back in February Nebius aquired them as a tuck in acquisition to contribute to what they are building at token factory. In summary Tavily is a way for agents to search the web in a more efficient manor without going through unnecessary pages on the internet thereby saving on tokens. An agent will send its query, and Tavily will send back snippets of text from the page on a website.

### Eigen AI

Nebius bought them in June, but what's more interesting is that half of what they paid for the business was just to keep the people working for them for 4 years (so golden handcuffs if you will). *✎ The filing says it's more than half. Closed June 10, 2026. The purchase price was $331.4M (~1.4M shares plus $32.7M cash), while $549.2M (~2.4M shares worth $508.1M vesting over 4 years, plus $41.1M cash) is booked as compensation. That's ~62% of the total, and it's why Q2 stock-based comp jumped to $102.5M [Q2 6-K F-15/16].* Some of the ways that they do this is through shrinking the model. They are able to compress models to a quarter of its size with barely any quality loss, meaning you can serve more users at once on the same chip. They also optimize KV cache, have smarter batching, and do speculative decoding.

- **KV Cache** is the tokens used inside a context window, so that the model doesn't have to recall the text.
- **Prefill** = reading, and **Decoding** = writing.
- **Batching:** Serving user requests together in a group instead of one at a time. (Think Fixed costs per token going down)
- **Custom Kernels:** Low level programs running on GPU cores that help fast memory
- **Speculative Decoding:** Small models draft the next few words in guesses, and the big model verifies them in a single pass. (faster output)

### Inferize

This is actually the newest acquisition they have made

*✎ Added from sources:* Nebius announced the Inferize acquisition on **October 1, 2026**, and it is being folded into Token Factory.
- **What it fixes:** "cold starts", the delay in loading and scaling a model when demand spikes. Those delays leave GPUs idle and force providers to keep spare capacity on standby. Inferize lets capacity track real usage more closely, which means more tokens served per GPU.
- **Team:** about 17 people in Tel Aviv. The founders, Guy Bortnikov and Lior Gorbonos, previously built Granulate, which Intel bought in 2022.
- **Price:** not disclosed; press estimates $100–150M.

It is the same playbook as Eigen AI: buy the engineers who raise token output per chip, and keep the efficiency gains as margin.

Sources: [Nebius newsroom](https://nebius.com/newsroom/nebius-acquires-inferize-to-strengthen-nebius-token-factorys-production-inference-stack), [Calcalist](https://www.calcalistech.com/ctechnews/article/byzggtiqgx), [Dealroom](https://dealroom.co/news/158426-nebius-buys-10-month-old-israeli-startup-inferize-for-up-to-130m/)

## Demand / Why am I so confident?

Chips are not the scarce resource. It is Memory, Power, Optics, Grid connection contracts as far as physical bottlenecks to deliver AI go. A lot of people are talking about how chips are going to become abundant over the next few years, and while yes GPUs are going to be far less scarce than they are today, I am of the belief that connected megawatts is going to be the bottleneck for far longer than everyone is anticipating.

We have talked about token economics but we have not talked about the depreciation of GPUs and the math on these depreciating assets. That sounds like an oxymoron but funnily enough each year the GPUs are able to produce more tokens per second due to software optimization. This works as a floor that holds longer for the GPUs as they depreciate towards their economic life. Theoretically Spot prices in older GPUs should reflect discounted prices relative to the Flagship GPUs token output per second.

## Notes

NVIDIA forces hyperscalers to go to neoclouds to access their GPUs because of the quota **[needs source]** *✎ Partial support only. Microsoft has reportedly committed $60B+ across neocloud deals (Nscale, Nebius, CoreWeave, IREN, Lambda), NVIDIA has invested ~$2B each in CoreWeave and Nebius, and Nebius says four or more customers typically compete for each GPU it brings online ([IO Fund](https://io-fund.com/ai-stocks/nvidia-coreweave-nebius-circular-financing-gpu-boom), [Technology Match](https://technologymatch.com/blog/coreweave-vs-lambda-vs-nebius-gpu-capacity-enterprise-ai)). No source says NVIDIA uses quotas to steer hyperscalers to neoclouds. Reword it as "NVIDIA's allocations and investments favor neoclouds", or find the original.*
