# A Debt Structure for the 5 GW Build

*October 15, 2026. Model: [`models/debt_structure.py`](../models/debt_structure.py), output in [`models/output/debt_structure.md`](../models/output/debt_structure.md). Built on the pricing tiers in the author's Nebius.MD (folded into the [initiation note](nebius-initiation.md) §7) and on the reconciled [5 GW funding model](../models/output/funding_5gw.md).*

> Not investment advice.

## The problem

Nebius pays for its build mostly with customer prepayments, unsecured converts and new shares, whatever the contract behind the capacity:

- **H1 2026:** prepayments $4.4B, converts $4.3B, NVIDIA warrants $2.0B, ATM $2.8B, against $8.1B of capex. [F2 F-7]
- **Secured debt so far:** a single $775M facility (July 2026).

The cost doesn't show up as interest. It shows up as shares:
- The August converts pay 0.50% (2030) and 4.50% (2034), but convert at a 40–45% premium. [PR]
- The older converts trade at $20.8B against $8.5B on the books. [F2 F-29]
- The reconciled funding model needs $51B of new equity for 2027–30, which is +57% dilution, before any of it earns back its depreciation.

## The fix: give each tier of contract its own tranche

Nebius.MD prices capacity in three tiers. Each tier carries a different amount of debt:

| Tier | Price per MW a year | Customers | Funded by |
|---|---|---|---|
| Hyperscaler, 5-year | ~$12M | Microsoft, Meta (investment grade) | **A. Contract-backed GPU term loan:** SOFR + 2.50%, tenor = contract, sized to 1.25x DSCR |
| Core, 1–3 year | $20–25M | AI labs, enterprises | **B. Delayed-draw term loan:** ~10.4%, tenor = contract, sized to 1.35x DSCR |
| Short-term and auction | $40–50M | Spot and premium buyers | **D. Equity and converts.** No term debt on cash flow nobody has contracted |
| *Every site's shell* | | | **C. Sale-leaseback** of land, buildings and power to infrastructure capital, ~8% rent yield |

Each piece already has a precedent:

- **A. Nebius has already done one.** The July facility:
  - borrowers are ring-fenced subsidiaries (Nebius Compute II, LLC and Oy)
  - collateral is the GPUs plus an investment-grade customer contract
  - priced at SOFR + 2.50%, matures October 2030
  - Nebius says the loan plus customer cash flows cover more than 100% of the GPU capex, and calls it a template for the more than $40B of IG contracted revenue still unfinanced. ([TNW](https://thenextweb.com/news/nebius-775-million-gpu-backed-debt-financing), [Blockspace](https://blockspace.media/insight/nebius-secures-775-million-ai-cloud-loan-2026/))

  Peer deals on the same terms:
  - CoreWeave's DDTL 4.0 priced at SOFR + 2.25% and was rated A3 ([The Energy Mag](https://theenergymag.com/news/2026-03-31/coreweave-ai-loan-billion)).
  - IREN funded its Microsoft contract at ~5.9%. With Microsoft's prepayment, that covered 95% of the GPU capex ([The Energy Mag](https://theenergymag.com/news/2026-06-01/iren-microsoft-gpu-ai-loan), [IREN 10-K](https://www.sec.gov/Archives/edgar/data/0001878848/000187884826000052/iren-20260630.htm)).
- **B. Price it on a matched tenor.** CoreWeave's DDTL 5.5 closed at SOFR + 5.50% at 97, a 10.44% yield. One reason for the price: its contracts average about 3 years against a 5-year loan ([Global Data Center Hub](https://www.globaldatacenterhub.com/p/coreweave-ddtl-5-5-infrastructure-loan), [The Energy Mag](https://theenergymag.com/news/2026-08-11/coreweave-ai-2-6-billion-wider-spread/)). The model uses that yield, but sets the tenor equal to the contract.
- **C. Hyperscalers have done this with their shells.**
  - Meta's Hyperion JV: Blue Owl owns 80%, ~$27B of A+ project bonds ([Meta](https://about.fb.com/news/2025/10/meta-blue-owl-capital-develop-hyperion-data-center/amp/)).
  - QTS: $3.9B for a Microsoft-leased campus at 7.23% ([GlobalCapital via SFA](https://structuredfinance.org/wp-content/uploads/2026/07/SFA-Research-Corner_How-Data-Center-ABS-and-CMBS-Fit-in-a-Broader-Financing-Ecosystem.pdf)).
  - Nebius is an unrated tenant, so the model uses 8%.
  - Nebius owns 2.7 GW of US sites (Missouri, Pennsylvania, Birmingham), the obvious candidates ([`data/contracted_sites.csv`](../data/contracted_sites.csv)).

## What it does to the numbers

Per MW, at $58.7M of capex. Debt is sized on project cash flow: contract revenue less ~$1.87M a year of power and site operations, from [`data/gpu_economics.csv`](../data/gpu_economics.csv).

| | Hyperscaler, today | Hyperscaler, tiered | Core, today | Core, tiered |
|---|---|---|---|---|
| Customer prepayment | $12.0M | $12.0M | $6.8M | $6.8M |
| Secured GPU loan | — | $20.1M | — | $28.9M |
| Shell sale-leaseback | — | $21.1M | — | $21.1M |
| **Nebius equity or converts** | **$46.7M** | **$7.8M** | **$51.9M** | **$7.7M** |
| Equity IRR over 5 years | 7.2% | 15.8% | 23.6% | 79.5% |
| **Price per MW needed for 12%** | **$13.7M** | **$11.7M** | $15.8M | $13.5M |

1. **The hyperscaler deal goes from losing value to earning its cost of capital.**
   - Funded with equity, a $12M 5-year contract needs $13.7M to earn 12%.
   - Funded with its own contract-backed loan and a leased shell, it needs $11.7M.
   - The structure doesn't change the contract. It cuts the price the contract needs to clear by ~$2M per MW, which is the difference between destroying value at $12M and earning 12%.
2. **Equity per MW falls about 6x.** It goes from ~$47–52M to ~$8M on contracted capacity.
   - For the 2027–30 build (4.33 GW, base mix of 60% hyperscaler, 30% core, 10% short-term), Nebius's equity need falls from $214B to $47B before operating cash flow.
   - That is +68% dilution at $221 instead of +314%.
   - Cash from the existing 0.67 GW base (~$4B of EBITDA a year) reduces it further.
3. **The debt pays itself down.**
   - Secured debt peaks at ~$57B in 2030.
   - It amortizes to zero by 2035, because every loan ends with its contract.
   - Portfolio DSCR stays at 1.6–1.9x through the build ([schedule](../models/output/debt_structure.md#secured-debt-schedule-base-mix-proposed-structure-b)).

## What it costs, and what has to be true

- **Leases are debt.**
  - The shell sale-leasebacks total ~$92B.
  - Rent at full build is ~$7.3B a year, for 15–20 years, on sites whose first GPU contracts last 5.
  - Rating agencies and investors will capitalize that rent.
  - The structure trades dilution for fixed charges. Re-contracting risk on the shell stays with Nebius equity.
- **Debt only follows signed contracts.**
  - Tranche A needs investment-grade contracts: $156B of them for the base mix, against the ~$40B Nebius cited in July (~0.67 GW at $60M of contract value per MW).
  - So the binding constraint on the build is **contracting, not capital**.
  - Build a tranche only when its contract is signed.
- **The project margin has to be a project margin.**
  - Lenders size on revenue less power and site costs (~84% at $12M).
  - The AI cloud segment's 50% EBITDA margin also carries platform, R&D and sales costs.
  - At a 50% project margin, the hyperscaler tier needs $15.6M per MW even with this structure, and no financing fixes that ([sensitivity](../models/output/debt_structure.md#sensitivity-the-hyperscaler-tier)).
- **The GPUs need some value after 5 years.**
  - At 0% residual the tier needs $12.5M.
  - At 30% it needs $11.0M.
  - The H100 economics in initiation note §7.4 argue for a positive residual.
- **Prepayments are per contract.**
  - Deferred revenue is 16% of RPO ($6.0B / $37.5B); IREN got ~20%. The model uses 20%.
  - The workbook's "45% of capex" equals ~44% of a 5-year hyperscaler contract. No customer has paid that so far.

## Where Nebius.MD comes in

The software-layer thesis in Nebius.MD ("available GPUs win the customer; better software keeps them") is also a credit argument:

- **Lenders price re-contracting risk.** That risk is why CoreWeave's short-contract DDTL costs SOFR + 5.50% and its IG one costs SOFR + 2.25%.
- **Proving retention makes debt cheaper.** If Nebius can show customers renew at contract end (Tavily, ClarifAI and Eigen AI in the stack, auctions clearing above list), it can stretch tenors past the contract and borrow against GPU residual value.
- **Short-term capacity stays equity-funded.** Contracting the $40–50M auction capacity would mean giving up exactly the scarcity pricing Nebius.MD says is "letting Nebius reprice the same silicon twice in five months". Keep it equity-funded and treat it as the source of the operating cash that pays for equity slices elsewhere.

## Questions for the Q3 call (November 10–11)

1. How much of the ~$40B of IG contracted revenue will be financed on the July template, and when?
2. Will Nebius sell or JV the owned US shells, or keep them on balance sheet?
3. What is the contract-level margin on the Microsoft and Meta deals, as opposed to the segment margin?
4. What share of new contracts are 5-year vs. 1–3 year, and what prepayment share of contract value is Nebius getting?
5. What are the DSCR and liquidity covenants on the July facility?

## Sources

- **[F2]** Nebius Q2 2026 Form 6-K, Exhibit 99.2. See the [initiation note](nebius-initiation.md#sources).
- **[PR]** [Nebius, pricing of $5.0B convertible notes (August 2026)](https://nebius.com/newsroom/nebius-group-announces-pricing-of-upsized-private-offering-of-5-0-billion-of-convertible-senior-notes).
- **Nebius.MD:** the author's notes, branch `claude/ai-stack-value-add-ttlhzu`. Tier prices are `author_notes` quality.
- The financing precedents are linked inline. All of them are secondary sources except the IREN 10-K and Meta's release.
