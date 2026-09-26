# BOM notes

Costs are single-unit estimates in USD for a first prototype (2026), priced by supplier type; no quotes have been requested. Item numbers match the exploded view in `media/exploded.png`, the model in `cad/src/model.py` and drawing LMF-DWG-001 Rev P2. Every item is modeled.

- **Total:** $338.00 for one unit, $113.00 over the $225 `budget_usd` (LMF-DDR-001 D2). `docs/04-calcs/sizing.py` reads this file and prints the total (LMF-CAL-001 v0.2, I1). R16 is not met; the budget figure after re-pricing is awaiting Amish (LMF-DDR-002 O4).
- **Change from the first TRL 3 BOM ($249.00), re-priced for the 50 mm reactor of LMF-DDR-002:** high-reflectance PTFE liner $45 (was $16 for plain PTFE); 57 x 10 mm window $32 (was $14); 90 mm 316 lower cap $42 (was $28); 90 mm acetal upper cap $16 (was $12); 65 mm tube with a sensor hole $26 (was $15); 90 mm sink $13 (was $9); wall photodiode with saddle $26 (was $22); 15 Hz per L/min flow sensor $10 (was $8); M5 tie rods $10 (was $8); bracket $6 (was $5). The LED board now carries an NTC for the thermal cut-back, and the restrictor is 1.2 L/min.
- **Largest cost:** the six UV-C LEDs (item 4), $54, then the liner ($45) and the lower cap ($42). A plain PTFE liner would save most of the liner cost but give 46.3 mJ/cm² instead of 51.9 (LMF-CAL-001, B8).
- **Not in the BOM:** the sediment pre-filter and the pressure-limiting valve (R17) are part of the installation.
- **Food contact:** every wetted part (items 1, 2, 3, 6, 7, 8, 9 window and seal, 11, 15 and the O-rings) must be food-contact grade. Printed plastics are not used on the water path, and no plastic other than PTFE sees UV-C.
- **Shared parts:** LumaFlow uses no SwapCell pack, so the portfolio rule on pricing shared packs once does not apply.
- LMF-CAL-001 states the assumptions (for example, flow coefficients of items 8 and 11) that depend on these parts.
