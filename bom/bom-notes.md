# BOM notes

Costs are single-unit estimates in USD for a first prototype (2026), priced by supplier type; no quotes have been requested. Item numbers match the exploded view in `media/exploded.png`, the model in `cad/src/model.py`, drawing LMF-DWG-001 Rev P4 and the build plan LMF-BLD-001. Every item is modeled.

- **Total:** Value-engineering target: USD 340 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 402.00 (USD 62 over the target). `docs/04-calcs/sizing.py` reads this file and prints the total (LMF-CAL-001 v0.4, I1).
- **Change from the concept BOM ($338.00), made to render the design buildable (LMF-DDR-003):** tube with a welded sensor boss $38 (was $26); lower cap $48 (was $42) and upper cap, now 40 mm tall, $19 (was $16); heat sink drilled $14 (was $13); sensor line $24 (was $26, the boss moved to line 1); bracket now a drilled 6 mm aluminium plate with two printed saddles $16 (was $6); fittings with two stainless stem adaptors and the 316 outlet sleeve $24 (was $14); fixings $14 (was $10); new line 17, window retaining ring and seals, $12; new line 18, two pipe clamps, $8.
- **Largest cost:** the six UV-C LEDs (item 4), $54, then the lower cap ($48) and the liner ($45). The cost drivers and savings worth trying are in the design decisions register, LMF-DEC-001.
- **Not in the BOM:** the sediment pre-filter and the pressure-limiting valve (R17) are part of the installation.
- **Decided on 2026-10-02, not yet in the BOM (LMF-DEC-001):** a labels line (UV-C warning label on the lower cap and inside the enclosure lid, and the product label); a 0.5 mm food-contact PTFE washer under the window (item 17); the loop wire pair in the LED head plug (item 10 wiring); and the five-segment UV level bar on the enclosure lid (item 13). The adapter (item 12) stays in the BOM.
- **Food contact:** every wetted part (items 1, 2, 3, 6, 7, 8, 9 window and washer, 11, 15, 17) must be food-contact grade. Printed plastics are not used on the water path, and no plastic other than PTFE sees UV-C.
- **Shared parts:** LumaFlow uses no SwapCell pack, so the portfolio rule on pricing shared packs once does not apply.
- LMF-CAL-001 states the assumptions (for example, flow coefficients of items 8 and 11) that depend on these parts.
