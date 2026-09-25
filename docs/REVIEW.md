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

## Session 2026-09-25: TRL 3

Amish's instruction for this session (2026-09-25): "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." LumaFlow now claims TRL 3 (proof of concept on paper). TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (LMF-DDR-001 v0.1): the nine TRL 2 review items with a recommendation recorded as decided by Amish, 2026-09-25 (D1 to D9), and the items that stay open (O1 to O3).
- `docs/04-calcs/01-sizing.md` (LMF-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: flow and hydraulics; a Monte Carlo ray trace of the reactor (LED emission, window refraction and Fresnel losses, diffuse PTFE and stainless walls, water absorption) giving the fluence field; dose per streamline and RED for plug and laminar flow; dose monitor signal and mapping; switching and run-on; power and energy; a thermal network with a water path; pressure drop, window, sensor window, tube and tie rods; size from the model; cost from the BOM; options for the dose gap, including a bore study that reruns the ray trace at 40 and 50 mm. The script imports the model's `PARAMS`, `levels()` and part volumes and prints every number the note quotes, tagged [A1] to [K1]. It runs in about 30 s.
- `cad/src/model.py`: parametric build123d model (tube, PTFE liner and top disc, quartz window, LED board, heat sink and spreader ring, 316 lower cap, acetal upper cap, tie rods, flow sensor, photodiode, valve, controller, enclosure, bracket, fittings with the 316 outlet insert, adapter), exporting `cad/step/lumaflow-assembly.step`, `reactor.step`, `led-head.step` and matching STL files.
- `cad/src/sheets.py` and `cad/drawings/LMF-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, scale 1:5, with overall, port and window heights and cap diameter drawn from the model, and a main-dimensions box. The sheet carries "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet stays LMF-DWG-010, so DWG-001 was the next free number.
- `bom/bom.csv` and `bom/bom-notes.md`: all 16 lines priced with a supplier type; total $249.00 against the new $225 budget.
- `cad/src/concept_media.py` now builds the media from `model.py` with figures from the calc; all media in `media/` were regenerated and checked by eye (the overlapping loss labels on the flow diagram were shortened; the stainless lower cap was recolored so it reads as steel in the cutaway); temporary `media/_views*` folders were deleted.
- LMF-PRB-001, LMF-PRC-001 and LMF-REQ-001 revised to v0.3 (decisions recorded, numbers replaced by LMF-CAL-001, status column from the calc); `README.md` updated to TRL 3 with links; `project.yaml` set to `trl: 3`, `trl_target: 3`, `budget_usd: 225`, with the evidence files listed. PDFs are in `docs/pdf/`.
- Citations: the two facts flagged at TRL 2 are now sourced. The fused quartz design stress is 6.8 MPa (1,000 psi) ([Momentive](https://www.momentivetech.com/materials/fused-quartz-materials/quartz-properties/mechanical-properties)), so R7 now reads 6.8 MPa rather than 7 MPa; tap-scale mercury units draw 13 to 22 W ([VIQUA spec sheet](https://viqua.com/wp-content/uploads/LIT520326_SpecSheet.pdf)), replacing the assumed 10 to 25 W.
- No TRL 4 material exists in the repo (`firmware/`, `electronics/` and `build-log/` hold only placeholders), and none was created.

### Requirements (LMF-CAL-001, Table 5)

8 met, 4 at risk, 3 not met, 1 not verifiable at TRL 3. The dose is judged on the laminar-flow RED, the more pessimistic of the two flow limits.

| ID | Status | Value against target |
| --- | --- | --- |
| R2 | **Not met** | RED 14.7 (laminar) to 19.0 (plug) mJ/cm² at 90 %/cm and 2.0 L/min, against 40. At TRL 2 this was estimated at about 40 and "met" |
| R3 | **Not met** | 6.3 to 7.4 mJ/cm² at 70 %/cm, against 40; kept visibly not met by decision D1 |
| R16 | **Not met** | $249.00 against the new $225 budget |
| R4 | At risk | Far-end photodiode gives about 2.4 nA at 90 %/cm and nothing resolvable at 70 %/cm; with the safe proportional mapping the alarm would close the valve in any water while R2 is not met |
| R5 | At risk | 0.46 s worst-case switch-on at 0.3 L/min, against 0.5 s |
| R8 | At risk | 0.42 bar against 0.5 bar, resting on assumed valve and sensor flow coefficients |
| R10 | At risk | LED board 48.9 °C nominal, 44.1 to 55.9 °C over the water-film range, against 50 °C |
| R15 | Not verifiable at TRL 3 | Service time needs a build |
| R1, R6, R7, R9, R11, R12, R13, R14 | Met | 2 L/min restrictor; LEDs; window 4.46 MPa; 22.6 W and 0.21 W; 316 lower cap and PTFE shielding; light path and interlock by design; 24 V only; 235 x 72 x 322 mm |

Key numbers: only 26.1 % of the 0.36 W of UV-C is absorbed by the water at 90 %/cm, against about 78 % assumed at TRL 2; the PTFE wall (reflectance 0.80 wetted, assumed) takes 49.8 %. The reactor efficiency is 0.77, better than the 0.5 assumed, so the loss is optical, not hydraulic. Six LEDs reach 40 mJ/cm² at 90 %/cm only below 0.64 L/min; a 50 mm bore would give 30.0 to 41.0 mJ/cm² at 2.0 L/min. Energy 3.1 kWh/year against 114 to 193 kWh/year for a mercury unit. Every TRL 2 number in the docs was checked against the script and corrected where it differed (LMF-CAL-001, Table 6).

### Decisions recorded (LMF-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 design for 90 %/cm UVT with alarm and valve closure below 40 mJ/cm², R3 kept visibly not met, Option C later; D2 `budget_usd` raised to $225 (set in `project.yaml`, R16 redefined); D3 axial LED head with a flat quartz window; D4 275 nm LEDs; D5 Hall-effect flow sensor; D6 normally closed outlet valve; D7 vertical mounting with upward flow; D8 external certified 24 V adapter on a GFCI or RCD outlet; D9 first user is a well-water household with a sediment pre-filter. The pitch and problem lines were not asked to change and are unchanged. LumaFlow uses no SwapCell pack, so the SwapCell interface v0.3 items and the shared-pack pricing rule do not affect it.

### Proposed, awaiting Amish

Still open from TRL 2 (no recommendation was made):

1. Partner that can supply real well-water UVT data (O1). Portfolio rule: partners are picked per area later.
2. End cap material (O2). The TRL 3 model uses a 316 stainless lower cap (its bore sees full UV-C, and it is the water-cooled heat path; an acetal cap would let the LED board reach 85 °C) and an acetal upper cap shielded by the PTFE liner, top disc and a 316 outlet insert. Recommendation: confirm.

New from TRL 3:

3. **Route to close R2 (most important).** Options: (a) lower the design flow to about 0.6 L/min (R1 falls to a third); (b) 17 LEDs at 2 L/min (53 W, R9 fails, about $99 more); (c) a higher-reflectance liner (0.95 gives 17.3 mJ/cm², not enough alone); (d) a wider bore of about 50 mm (30.0 to 41.0 mJ/cm² at 2 L/min, window about 9.5 mm, larger parts), which can be combined with (c) and a modest flow cut. Recommendation: (d) with (c), as a TRL 3 design iteration re-run through LMF-CAL-001, keeping (a) as the fallback. Until then, D1's rule means the unit would never open its valve.
4. **Dose monitor position (R4).** Move the photodiode from the top disc to the tube wall at mid height (about 20 times more signal at 90 %/cm and a usable signal at 70 %/cm), and keep the proportional mapping, which always under-reads. Recommendation: adopt; optionally add a second reference sensor near the LEDs to separate LED aging from water quality.
5. **Budget (R16).** $249.00 against $225. Options: (a) raise `budget_usd` to $250; (b) cut cost (for example an acetal lower cap, which fails R10 and R11); (c) hold until the R2 route is chosen, since it changes the tube, caps and window. Recommendation: (c), then re-price. `budget_usd` stays at $225.
6. **Flow sensor pulse rate (R5).** Choose a sensor of 15 Hz per L/min or more, halving the worst-case detection time. Recommendation: adopt.
7. **R8 wording.** State that the 0.5 bar excludes the flow restrictor, which absorbs excess supply pressure by design; confirm the valve and sensor flow coefficients from datasheets. Recommendation: adopt.
8. **Pressure limiter and thermal cut-back.** Make an upstream pressure-limiting valve an installation requirement (a 16 bar spike gives 8.9 MPa in the window), and add a board temperature sensor that cuts LED current above 50 °C (R10). Recommendation: adopt both.

### Safety concerns

- **False sense of safety, now larger.** The calculated dose is 14.7 to 19.0 mJ/cm² in clear water, below the 40 mJ/cm² target and near or below the Class B level of 16. Every document says LumaFlow is a research and educational prototype, not a certified water treatment device, and that it must not be relied on as a barrier.
- UV-C exposure to eyes and skin: metal and PTFE block UV-C in the model; interlocks on the lid and LED head are required.
- Pressure: the window has margin at 8 bar but not at a 16 bar spike; an upstream pressure limiter is required. A cracked window floods the 24 V LED head.
- Heat: LEDs stuck on without flow take the board to about 69 °C; firmware must switch off when flow stops, with a thermal cut-back as backup.
- Mains in a wet cabinet: confined to a certified adapter on a GFCI or RCD outlet.

### Recommended next step

TRL 4 is on hold by Amish's instruction; no TRL 4 work was started. The next step is to decide item 3 (route to close R2) and, if Amish wishes, run one more TRL 3 design iteration: rerun LMF-CAL-001 with the chosen bore, reflector and flow, move the dose sensor (item 4), and re-price the BOM (item 5). For reference only, TRL 4 would need: a bench reactor built from the BOM, a measured wetted PTFE reflectance and LED output at 275 nm, a lab test report (TST, `environment: lab`) with collimated-beam and flow-through biodosimetry against the dose model, pressure and leak tests of the window and caps, LED board temperature under continuous flow, flow switching timing on a firmware sketch, and build-log entries.
