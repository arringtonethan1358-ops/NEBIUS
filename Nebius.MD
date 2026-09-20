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
