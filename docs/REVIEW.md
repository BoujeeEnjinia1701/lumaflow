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

All nine items below were later decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-001, D1 to D9).

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

1. Partner that can supply real well-water UVT data (O1). Portfolio rule: partners are picked per area later. Still Proposed, awaiting Amish (no recommendation).
2. End cap material (O2). Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-002 E1). The TRL 3 model uses a 316 stainless lower cap (its bore sees full UV-C, and it is the water-cooled heat path; an acetal cap would let the LED board reach 85 °C) and an acetal upper cap shielded by the PTFE liner, top disc and a 316 outlet insert. Recommendation: confirm.

New from TRL 3:

3. **Route to close R2 (most important).** Options: (a) lower the design flow to about 0.6 L/min (R1 falls to a third); (b) 17 LEDs at 2 L/min (53 W, R9 fails, about $99 more); (c) a higher-reflectance liner (0.95 gives 17.3 mJ/cm², not enough alone); (d) a wider bore of about 50 mm (30.0 to 41.0 mJ/cm² at 2 L/min, window about 9.5 mm, larger parts), which can be combined with (c) and a modest flow cut. Recommendation: (d) with (c), as a TRL 3 design iteration re-run through LMF-CAL-001, keeping (a) as the fallback. Until then, D1's rule means the unit would never open its valve. Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-002 E2).
4. **Dose monitor position (R4).** Move the photodiode from the top disc to the tube wall at mid height (about 20 times more signal at 90 %/cm and a usable signal at 70 %/cm), and keep the proportional mapping, which always under-reads. Recommendation: adopt; optionally add a second reference sensor near the LEDs to separate LED aging from water quality. Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-002 E3).
5. **Budget (R16).** $249.00 against $225. Options: (a) raise `budget_usd` to $250; (b) cut cost (for example an acetal lower cap, which fails R10 and R11); (c) hold until the R2 route is chosen, since it changes the tube, caps and window. Recommendation: (c), then re-price. `budget_usd` stays at $225. Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-002 E4).
6. **Flow sensor pulse rate (R5).** Choose a sensor of 15 Hz per L/min or more, halving the worst-case detection time. Recommendation: adopt. Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-002 E5).
7. **R8 wording.** State that the 0.5 bar excludes the flow restrictor, which absorbs excess supply pressure by design; confirm the valve and sensor flow coefficients from datasheets. Recommendation: adopt. Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-002 E6).
8. **Pressure limiter and thermal cut-back.** Make an upstream pressure-limiting valve an installation requirement (a 16 bar spike gives 8.9 MPa in the window), and add a board temperature sensor that cuts LED current above 50 °C (R10). Recommendation: adopt both. Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-002 E7, E8).

### Safety concerns

- **False sense of safety, now larger.** The calculated dose is 14.7 to 19.0 mJ/cm² in clear water, below the 40 mJ/cm² target and near or below the Class B level of 16. Every document says LumaFlow is a research and educational prototype, not a certified water treatment device, and that it must not be relied on as a barrier.
- UV-C exposure to eyes and skin: metal and PTFE block UV-C in the model; interlocks on the lid and LED head are required.
- Pressure: the window has margin at 8 bar but not at a 16 bar spike; an upstream pressure limiter is required. A cracked window floods the 24 V LED head.
- Heat: LEDs stuck on without flow take the board to about 69 °C; firmware must switch off when flow stops, with a thermal cut-back as backup.
- Mains in a wet cabinet: confined to a certified adapter on a GFCI or RCD outlet.

### Recommended next step

TRL 4 is on hold by Amish's instruction; no TRL 4 work was started. The next step is to decide item 3 (route to close R2) and, if Amish wishes, run one more TRL 3 design iteration: rerun LMF-CAL-001 with the chosen bore, reflector and flow, move the dose sensor (item 4), and re-price the BOM (item 5). For reference only, TRL 4 would need: a bench reactor built from the BOM, a measured wetted PTFE reflectance and LED output at 275 nm, a lab test report (TST, `environment: lab`) with collimated-beam and flow-through biodosimetry against the dose model, pressure and leak tests of the window and caps, LED board temperature under continuous flow, flow switching timing on a firmware sketch, and build-log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now decided by Amish, 2026-09-25: go with recommendation, recorded in `docs/decisions/0002-recommendations-accepted.md` (LMF-DDR-002 v0.1). TRL 4 remains on hold.

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| E1 | End caps: 316 lower, PTFE-shielded acetal upper (confirm) | Proposed | Decided; no geometry change |
| E2 | Route to close R2: 50 mm bore with a high-reflectance liner and a modest flow cut | 25 mm bore, liner 0.80, 2.0 L/min; RED 14.7 to 19.0 mJ/cm² at 90 %/cm | 50 mm bore, liner 0.95, 1.2 L/min; RED 51.9 to 76.3 mJ/cm² (R2 met) |
| E2 | Consequential geometry | Tube 40 mm OD, caps 60 mm, window 32 x 6 mm, sink 64 mm, M4 rods; 235 x 72 x 322 mm | Tube 65 mm, caps 90 mm, window 57 x 10 mm, sink 90 mm, M5 rods; 277 x 100 x 322 mm |
| E3 | Dose sensor in the tube wall at mid height | Top disc; 2.4 nA at 90 %/cm, unresolved at 70 %/cm | Wall, Z = 166 mm; 16.3 nA and 0.38 nA; alarm below about 89 %/cm |
| E4 | Budget: hold, then re-price | BOM $249.00, `budget_usd` 225 | BOM $338.00, `budget_usd` 225 (unchanged; figure now open as O4) |
| E5 | Flow sensor 15 Hz per L/min | 0.46 s worst-case switch-on | 0.24 s (R5 met) |
| E6 | R8 excludes the restrictor | 0.42 bar at 2.0 L/min | 0.15 bar at 1.2 L/min (R8 met, Kv assumed) |
| E7 | Pressure limiter as an installation requirement | Assumption only | New R17: limiter at 4 bar or less; window 6.18 MPa at an 8 bar transient |
| E8 | Thermal cut-back above 50 °C | Board 44.1 to 55.9 °C (R10 at risk) | NTC on the board; 37.1 to 44.8 °C (R10 met) |

Files changed: `cad/src/model.py` and the STEP and STL exports; `cad/src/sheets.py` and LMF-DWG-001 (Rev P1 to P2); `cad/src/concept_media.py` and all of `media/` (concept sheet LMF-DWG-010 Rev P2; temporary `_views` folders deleted); `bom/bom.csv` and `bom/bom-notes.md`; `docs/04-calcs/sizing.py` and LMF-CAL-001 v0.2 (wall-sensor ray trace, new flow limits, bore study removed as no longer needed); LMF-PRB-001, LMF-PRC-001 and LMF-REQ-001 to v0.4; LMF-DDR-001 to v0.2; `project.yaml` (DDR-002 added to the evidence; `trl: 3`, `trl_target: 3`, `budget_usd: 225`); `README.md` (concept, components, safety, and new sections on concept rationale, burning platform, where it could be used and what sparked the idea); PDFs in `docs/pdf/`.

### Requirement status (LMF-CAL-001 v0.2)

13 met, 2 not met, 1 at risk, 1 not verifiable at TRL 3, of 17 (before: 8 met, 3 not met, 4 at risk, 1 not verifiable, of 16).

| ID | Status | Value against target |
| --- | --- | --- |
| R3 | **Not met** (accepted by D1) | 17.4 to 21.8 mJ/cm² at 70 %/cm against 40 |
| R16 | **Not met** | $338.00 against $225 |
| R4 | At risk | Wall signal 16.3 nA at 90 %/cm, 0.38 nA at 70 %/cm; mapping and 1 s fail-safe need firmware and test |
| R15 | Not verifiable at TRL 3 | Service time needs a build |
| R1, R2, R5 to R14, R17 | Met | 1.2 L/min; RED 51.9 to 76.3 mJ/cm²; 0.24 s; window 6.18 MPa; 0.15 bar; 22.6 W and 0.21 W; board up to 44.8 °C; 277 x 100 x 322 mm; limiter at 4 bar |

Notes: R2 rests on the assumed liner reflectance of 0.95 (plain PTFE gives 46.3 mJ/cm², still above 40 but inside the 20 % margin) and on the organism's response at 275 nm. The window margin at 8 bar is now 9 % (6.18 against 6.8 MPa), which is why R17 matters.

### Still awaiting Amish

1. **Partner with real well-water UVT data (O1).** No recommendation; stays Proposed, awaiting Amish.
2. **Budget figure after re-pricing (O4, new).** $338.00 against $225. Options: (a) raise `budget_usd` to about $340; (b) keep $225 and cut cost (a plain PTFE liner saves most of $45 but drops the laminar RED to 46.3 mJ/cm², inside the 20 % margin; simpler machined caps); (c) keep $225 and leave R16 visibly not met. No recommendation is recorded as a decision; `budget_usd` stays at $225. **Decided by Amish, 2026-09-26: budget top-up to $340 (option (a)); see the session below.**

### Cross-repo actions

None. LumaFlow shares no part or interface with another repo.

### Safety concerns

- The dose is calculated, not measured. Every document keeps the statement that LumaFlow is a research and educational prototype, not a certified water treatment device.
- The larger window has a 9 % stress margin at 8 bar; the pressure limiter (R17) is required, not optional.
- The new wall sensor port is a UV-C and pressure boundary; the saddle, O-ring and quartz window must seal it, and the interlock rules apply.
- UV-C exposure, mains in a wet cabinet and heat: unchanged from the TRL 3 session, with the thermal cut-back added as a backstop.

### TRL 4

TRL 4 remains on hold by Amish's instruction; `trl: 3` and `trl_target: 3` are unchanged, and no TRL 4 material was created. Decided but on hold: measuring the liner reflectance and biodosimetry (E2), firmware for the dose mapping, fail-safe and cut-back (E3, E8), and quotes or purchasing for the re-priced BOM (E4).

## Session 2026-09-26: sources strengthened

Sources in the README were checked against the standard of 2026-09-26 ("Fix the weaker sources"); every kept link (WHO drinking-water fact sheet, USGS domestic wells, CMAJ 2010, patent US 1,151,267) was fetched and confirms its claim.

| Where | Old source | New source |
| --- | --- | --- |
| Region table, Sub-Saharan Africa | WHO drinking-water fact sheet, which gives no regional breakdown | WHO and UNICEF JMP, *Progress on household drinking water, sanitation and hygiene 2000-2022* (2023), p. 14: urban and rural gap in safely managed drinking water of 38 percentage points, the widest of any region |
| Region table, South Asia | None (uncited claim about shallow tube wells) | Row replaced by Bangladesh: Khan et al., *Environmental Science and Pollution Research* (2022), MICS 2019 data, high household *E. coli* contamination linked to 2.28 times the odds of child diarrhea |
| Region table, Andean and rural Latin America | None (uncited) | Row replaced by Latin America and the Caribbean: JMP 2023, p. 14, urban and rural gap of 27 percentage points |
| Region table, Pacific island states | None (uncited claims about rainwater tanks and mercury lamp disposal) | Row rewritten as Pacific islands (Oceania): JMP 2023, p. 14, at least basic drinking water for 93 % of urban and 51 % of rural people in 2022 |

"What sparked the idea" was already on a primary source (patent US 1,151,267 on Google Patents) and is unchanged.

### Budget top-up

Budget top-up to $340: decided by Amish, 2026-09-26 ("I am ok with the budget top ups"). `project.yaml` `budget_usd` is 340 (was 225). `docs/04-calcs/sizing.py` reads the budget from `project.yaml` and was re-run: BOM $338.00, $2.00 under [I1]; R16 now met. Counts: 14 met, 1 not met (R3, accepted by D1), 1 at risk (R4), 1 not verifiable at TRL 3 (R15). Open item O4 is decided.

Files changed: `project.yaml`; `README.md` (budget line, cost sentence, region table); LMF-REQ-001 v0.5 (R16 target $340, met); LMF-CAL-001 v0.3; LMF-DDR-002 v0.2 (O4 decided); LMF-PRC-001 v0.5 and LMF-PRB-001 v0.5 (budget figure); `cad/src/concept_media.py` and `media/` regenerated (concept sheet LMF-DWG-010 Rev P3, key figure now "$338 in parts against the $340 budget"); PDFs in `docs/pdf/`. The margin is only $2.00, so any price rise at quoting reopens R16.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added an appearance model for photoreal renders; the renders themselves (`media/render-hero.png`, `media/render-exploded.png`) are produced later by the portfolio render pipeline.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 55 parts (37 shell, 8 internal, 1 accessory, 9 context) with colour, material, BOM line, group and explode offset. It imports `PARAMS`, `levels()` and `build_parts()` from `cad/src/model.py`, so every main dimension and interface is unchanged. It also sets `TITLE` and three `RENDER_VIEWS`: hero (with context), exploded, and a detail view without the cabinet so the unit fills the frame.
- What it adds over the massing model:
  - Filleted rims on both end caps, the heat sink base, the enclosure, the bracket plate and clamp rings, the flow switch and valve bodies.
  - A wrapped product label with a wordmark and accent band on the tube, and a yellow UV-C warning label on the lower cap.
  - Acorn nuts and washers on the tie rods; screw heads on the enclosure lid and the bracket.
  - Enclosure split into a rear body and a front lid at a parting-line groove, with a buzzer grille, a cable gland, a status and dose bezel, a lit green status light and a lit dose bar.
  - Flow switch with a teal sensor cap, a flow-direction arrow and a lead; solenoid valve with a coil, a connector, a core nut and a lead; push-fit collets at every port.
  - Dose sensor split into a 316 saddle, a quartz sensor window and an amplifier housing with a lead to the enclosure.
  - Internals for the exploded view: PTFE liner, quartz window, and the LED board with six dark LED packages, a connector and the NTC.
  - Context: a short section of cabinet wall and floor, a chrome angle stop on the cold line, a countertop section with a stainless sink edge, and the drinking-water tap fed by the outlet line.
- UV-C safety in the renders: the LEDs are modeled as dark, unlit packages, and no part suggests visible or exposed UV-C light. Only the status light and the dose bar are emissive.
- `README.md`: hero image now points to `media/render-hero.png`, with an "Exploded render" link added to the links line.
- Previews were checked with the kit's matplotlib renderer (clear parts left out).

### Differences from model.py (appearance only)

1. **Dose bar on the enclosure.** The concept documents name a status light and a buzzer; the appearance model adds a five-segment dose bar beside the status light. Proposed, awaiting Amish. Recommendation: keep it, since it makes the dose monitor legible to a user at a glance and costs little (a few LEDs on the controller module); record it in the requirements if accepted, otherwise remove it from `product_model.py`.
2. **Acorn nuts on the tie rods.** The domed nuts stand about 3.6 mm above the plain nuts in `model.py` (overall height about 301 mm instead of 297 mm). Proposed, awaiting Amish. Recommendation: accept acorn nuts; they cover the rod ends and the change is within R14.
3. **Solenoid connector and port collars.** The valve coil carries a plug-in connector that stands 7 mm in front of the model's valve envelope, and both the flow switch and the valve gain 5 mm port collars and push-fit collets at each end. Proposed, awaiting Amish. Recommendation: accept; they reflect catalog parts of the kind already in the BOM.
4. **Adapter and power cord in the hero.** The 24 V adapter is shown only in the exploded view; in the hero the DC cord leaves the gland and enters the cabinet wall rather than running to the adapter on the floor, to keep the frame on the unit. Proposed, awaiting Amish. Recommendation: accept for the renders; the model, drawing and BOM still place the adapter on the cabinet floor.
5. **Labels.** The product label and the UV-C warning label are not in the BOM. Proposed, awaiting Amish. Recommendation: add a labels line (a few dollars) at the next BOM revision; a UV-C warning label is good practice regardless, but note the budget margin is only $2.00.
6. **Not modeled.** The LED supply cable from the enclosure to the LED head is left out of the appearance model for clarity.

### TRL

This is an appearance model only: no tolerances, no fabrication detail. `trl` stays 3 and TRL 4 remains on hold; no TRL 4 material was created.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.
