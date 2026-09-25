# BOM notes

Costs are single-unit estimates in USD for a first prototype (2026), priced by supplier type; no quotes have been requested. Item numbers match the exploded view in `media/exploded.png`, the model in `cad/src/model.py` and drawing LMF-DWG-001. Every item, including item 16, is now modeled.

- **Total:** $249.00 for one unit, $24.00 (about 11 %) over the $225 `budget_usd` set by Amish on 2026-09-25 (LMF-DDR-001 D2). `docs/04-calcs/sizing.py` reads this file and prints the total (LMF-CAL-001, I1). R16 is not met; options are in `docs/REVIEW.md`.
- **Change from TRL 2 ($217):** the lower end cap is now machined 316 stainless ($28, was $10) because its bore sees full UV-C and it carries heat to the water; the PTFE liner runs into the upper cap with a top disc ($16, was $14); a 316 outlet insert is added to the fittings ($14, was $10); four M4 316 tie rods hold the caps against the 8 bar end load ($8, was $5 for hardware); the photodiode line now includes its quartz window ($22, was $20); the heat sink gains a spreader ring ($9, was $8); the acetal upper cap is larger ($12, was $10).
- **Largest cost:** the six UV-C LEDs (item 4), $54. UV-C LED prices vary widely by supplier and output bin.
- **Food contact:** every wetted part (items 1, 2, 3, 6, 7, 8, 11, 15 and the O-rings) must be food-contact grade. Printed plastics are not used on the water path, and no plastic other than PTFE sees UV-C.
- **Shared parts:** LumaFlow uses no SwapCell pack, so the portfolio rule on pricing shared packs once does not apply.
- LMF-CAL-001 states the assumptions (for example, flow coefficients of items 8 and 11) that depend on these parts.
