# BOM notes

Costs are indicative single-unit prices in USD for a first prototype (2026) and will be checked against named suppliers at TRL 3. Item numbers match the exploded view in `media/exploded.png` and the massing model in `cad/src/concept_media.py`. Item 16 is not modeled.

- **Total:** about $217 for one unit, which is about $17 (about 9 %) over the $200 `budget_usd`. The budget options are in `docs/REVIEW.md` as a proposal awaiting Amish; `project.yaml` is unchanged.
- **Largest cost:** the six UV-C LEDs (item 4), about $54. UV-C LED prices vary widely by supplier and bin.
- **Food contact:** every wetted part (items 1, 2, 3, 6, 7, 8, 11, 15 and the O-rings) must be food-contact grade. Printed plastics are not used on the water path.
- Section 4 of the design precis (LMF-PRC-001) states the assumptions behind the numbers.
