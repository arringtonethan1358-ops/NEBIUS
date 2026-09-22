# Nebius ($NBIS) — Notes & Thesis

A running file of theses, notes, and alpha on Nebius.

---

## The AI Stack: Value Add on Top of the Accelerator

*Added 2026-09-20*

The hyperscalers didn't just build businesses renting out CPU compute. They built extremely valuable products around data, networking, security, storage, etc. We're now building around AI accelerators, but the playbook of building value add software on top is the same.

Turns out GPUs are really good for running AI models. That is why inference engines, which take a trained model and compute and produce intelligent tokens that can do real work, have become the first piece of this software stack. But, there is so much more to build than just this!

Training helps you turn compute into better models that produce more valuable tokens. Routing helps you pick the right model to generate those tokens at the right cost and quality. Security monitoring helps you check what's going into and coming out of those models. Then there's agent observability, context management, sandboxing, etc. All of these things will be part of the new AI stack and the opportunity is much bigger than just serving a model.

This definitely isn't a winner-take-all market, whether we're talking about open models vs. the frontier or the players within each category. Customers want choice, flexibility, and access to the fundamental building blocks to create their own systems.

Constrained GPU supply will actually act like a regularizer and draw this fight out longer. Customers are looking for both compute capacity AND value add on top of it. When someone doesn't have capacity, you go somewhere else. That means more players get exposure to customers and the opportunity to address value add.

Getting a customer because you have available GPUs is different from keeping them because your software is better. In the limit, the value add on top of the GPU will win out. The companies that do the best job building that software AND verticalize the fastest to own everything from chip to token will take the lion's share. It's important to be building for that now, even when the immediate customer need is just more compute.

### Takeaways

- **The CPU-cloud playbook repeats on accelerators.** Raw rental is the entry point; the durable margin sits in the software layer built on top (data, networking, security, storage → now training, routing, security monitoring, agent observability, context management, sandboxing).
- **Inference is the first layer, not the last.** Serving a model is the smallest slice of the eventual stack.
- **Not winner-take-all.** Customers demand choice and building blocks across both open and frontier models.
- **Scarce GPUs extend the game.** Capacity shortages push customers to shop around, which hands more players a shot at proving out their value add.
- **Acquisition ≠ retention.** Available GPUs win the customer; better software keeps them.
- **Verticalize chip → token.** The share goes to whoever pairs the best software with the fastest path to owning the full stack — and that has to be built now, while customers are still only asking for more compute.

---

## Pricing: On-Demand GPU Rate Increase, Effective Oct 1, 2026

*Announced 2026-09-17 · logged 2026-09-22*

Nebius notified customers of a second on-demand price increase this year, taking effect **October 1, 2026**. Per-GPU-hour list rates:

| Instance | Old | New | Change |
| --- | --- | --- | --- |
| NVIDIA H100 | $3.85 | $4.50 | ~+17% |
| NVIDIA H200 | $4.50 | $5.40 | ~+20% |
| NVIDIA B200 | $7.15 | $8.50 | ~+19% |
| NVIDIA B300 | $7.85 | $9.50 | ~+21% |

Non-GPU resources moved harder:

- **AMD EPYC Genoa CPU-only instances: ~+25%**
- **Memory: ~+41%**

### Context

- **Second hike since May.** The May round averaged ~29% on on-demand capacity. Stacked, that puts B300 up **~56% year to date** ($6.09 → $7.85 → $9.50).
- **Stated reason.** A Nebius spokesperson: "Demand for computing capacity to train and run AI models is surging."
- **Market reaction.** NBIS jumped ~9–11% on the announcement (Thu, Sept 17).
- **Live price discovery.** Nebius' first capacity auction cleared **15% above the highest price it had ever charged** for Blackwell-generation chips, and ~20% above Blackwell pipeline pricing. Short-duration premium contracts are pricing at **$40–50M per MW** vs. **$20–25M per MW** on core long-term deals. CEO Arkady Volozh said the company could "sell today our entire 2027 capacity" at current terms. Adjusted EBITDA margin came in at 41%.

### Read-Through

- **The regularizer is real, and it's priced.** Constrained supply isn't just drawing the fight out — it's letting Nebius reprice the same silicon twice in five months without losing the customer. That's the "getting a customer because you have available GPUs" phase paying cash today.
- **Raising list price on H100s is a supply statement, not a demand statement.** Last-gen Hopper repricing +17% means even the older fleet is sold out. Watch whether H100 rates hold once B300/Rubin capacity lands at scale — that's the first honest test of pricing power vs. scarcity rent.
- **Memory +41% > GPU +~20% is the tell.** The bottleneck is spreading past the accelerator to the rest of the box. That is the same "data, networking, storage" surface the hyperscalers monetized, showing up as a pricing lever before it shows up as a product.
- **Auction > list price.** The auction clearing 15% over the highest price ever charged says list rates are trailing the market. Expect a third hike, or expect more revenue to shift to auctioned/short-duration contracts at 2x the $/MW of core deals.
- **The risk to underwrite.** Price hikes are the easy revenue. They are also the part a competitor with free capacity can undercut tomorrow. The thesis above still holds: this buys time to build the software layer that makes the customer stay when someone else has GPUs at $7.85.
