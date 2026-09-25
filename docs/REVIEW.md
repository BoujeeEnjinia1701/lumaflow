# Review note: LumaFlow

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (LMF-PRB-001 v0.2): problem (mercury, warm-up, yearly lamp change, silent failure), prior work and standards with inline sources, users and context, constraints, out of scope, open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (LMF-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, status against the estimates and planned verification, plus assumptions.
- `docs/02-concept.md` (LMF-PRC-001 v0.2): how it works, 16 numbered components, flow, dose, dose monitor, power, heat, window stress, size and cost estimates, design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the vertical reactor (tube, liner, window, LED board, heat sink, two end caps, flow sensor, photodiode, valve, controller, enclosure, bracket, fittings, adapter) with a 1 L bottle as the scale context, since the unit is sink-cabinet size.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `cutaway.png`, `exploded.png` with callouts 1 to 15 matching the BOM, `flow.png` (power flow, all values estimates), `model.glb` and `viewer.html`. Temporary `_views` folders removed.
- `bom/bom.csv`: 16 lines with indicative prices, numbered to match the exploded view (line 16, hardware, is not modeled); `bom/bom-notes.md` updated.
- `README.md`: hero image and links line added before "## Problem"; concept, key components and safety text brought in line with the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- Not changed: `project.yaml` (pitch and problem still fit the numbers), `cad/src/model.py` placeholder (TRL 3 work).

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Design flow | 2.0 L/min (0.5 gpm), capped by a restrictor | R1 met by design |
| Residence time, Reynolds number | about 2.9 s, about 1,700 (laminar) | |
| UV-C output | about 0.36 W from six 275 nm LEDs at about 13 W electrical | |
| Dose at 90 %/cm UVT | about 40 mJ/cm² (reactor efficiency 0.5 assumed) | R2 met, no margin |
| Dose at 70 %/cm UVT | about 14 mJ/cm² | **R3 not met** |
| Power while flowing, standby | about 21.6 W, about 0.3 W | R9 met |
| Energy | about 10 Wh per day, about 3.8 kWh per year | |
| Water temperature rise | about 0.09 K | |
| Quartz window stress at 8 bar | about 4.5 MPa at 6 mm (about 18 MPa at 3 mm) | R7 met on estimate |
| Envelope | about 240 x 75 x 325 mm without the adapter | R14 met |
| Parts cost | about $217 | **R16 not met, about $17 (9 %) over** |

Requirements not met or unverified:

- **R3 not met:** at the NSF/ANSI 55 test water quality the dose is about a third of the target and below even the Class B level.
- **R16 not met:** about $217 against $200.
- **R2 met with no margin:** it rests on an assumed reactor efficiency of 0.5, the largest uncertainty in the concept.
- **R8 (pressure drop) and R10 (LED temperature) unverified.**

### Proposed, awaiting Amish

1. **Design water quality and dose target.** Option A: design for 90 %/cm UVT, alarm and close the valve below 40 mJ/cm², and keep R3 visibly not met. Option B: meet 40 mJ/cm² at 70 %/cm and 2 L/min with about 17 LEDs, about 40 W and about $100 more in LEDs alone. Option C: six LEDs plus a proportional valve that limits flow to about 0.7 L/min in poor water. Recommendation: A, with C as a later upgrade.
2. **Budget.** Options: (a) raise `budget_usd` to $225; (b) drop the shutoff valve and rely on the alarm alone (about $205, still over, and weaker fail-safe); (c) find cheaper LEDs or machine the end caps in-house to reach $200. Recommendation: (a), because the valve is the fail-safe. `project.yaml` is unchanged.
3. **Axial LED head with a flat quartz window** instead of the scaffold's quartz sleeve with LEDs around it. Recommendation: axial.
4. **275 nm LEDs** rather than 265 nm. Recommendation: 275 nm, revisit prices at TRL 3.
5. **Hall-effect flow sensor** as the flow switch and meter, rather than a reed flow switch.
6. **Normally closed outlet valve** that closes on alarm and on power loss.
7. **Vertical mounting with upward flow**, LEDs at the bottom, so air purges at the top.
8. **External certified 24 V adapter** on a GFCI or RCD outlet, so only 24 V DC is at the unit.
9. **First user and partner:** a well-water household with a sediment pre-filter, and a partner that can supply real UVT data.

### Safety concerns

- UV-C exposure to eyes and skin: metal body blocks UV-C; interlocks on the lid and LED head are required.
- False sense of safety: UV removes no chemicals, leaves no residual, fails in cloudy water and is not a full virus barrier at 40 mJ/cm² (adenovirus needs about 186 mJ/cm² for 4 logs). The documents state that LumaFlow is a research and educational prototype, not a certified water treatment device.
- Pressure and leaks at up to 8 bar next to electronics; a cracked window floods the 24 V LED head.
- Mains in a wet cabinet: confined to a certified adapter on a GFCI or RCD outlet.
- LED overheating if left on without flow: firmware must switch off when flow stops.

### Problems and notes

- `project.yaml` pitch and problem were left unchanged; the numbers found do not make them wrong.
- The scaffold BOM listed a quartz sleeve; the concept uses a flat window instead (decision 3). If Amish prefers the sleeve layout, the model and BOM need rework.
- Web search hit its session limit before a few facts could be sourced directly: the fused quartz design stress of about 7 MPa and the 10 to 25 W typical power of mercury point-of-use units are stated as assumptions in LMF-PRC-001 and should be sourced at TRL 3.

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the dose (reactor efficiency, reflectance, mixing), the dose monitor mapping, LED temperature, pressure drop and window stress by calculation, and produce the parametric model and drawing sheet.
