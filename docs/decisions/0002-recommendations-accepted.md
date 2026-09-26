---
doc_id: LMF-DDR-002
title: LumaFlow recommendations accepted
project: LumaFlow
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); record the decided TRL 3 items, the design changes they caused and the items still open
- version: "0.2"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish; O4 decided ($340)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items E1 to E8; O4 decided on 2026-09-26 (budget top-up to $340); item O1 remains proposed

## Context

After the TRL 3 session, `docs/REVIEW.md` (session 2026-09-25, TRL 3) and LMF-DDR-001 (O2, O3) listed eight items as "Proposed, awaiting Amish". Seven carried a recommendation, and the partner question (O1) did not. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided in favor of it; where the recommendation named several options, the recommended option is the decision. Items without a recommendation stay open. TRL 4 remains on hold by Amish's instruction, so anything that needs a build, a measurement, firmware beyond a sketch or purchasing is recorded as decided but on hold.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (TRL 3 session) and in LMF-CAL-001 v0.1, section J.

## Decision

*Table 1. Decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation".*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| E1 | End cap material (DDR-001 O2) | Confirm a 316 stainless lower cap and an acetal upper cap shielded by the PTFE liner, top disc and a 316 outlet insert | Wording only; LMF-PRC-001 v0.4 marks the choice as decided. The design already used these materials |
| E2 | Route to close R2 | Option (d), a wider bore of about 50 mm, combined with option (c), a high-reflectance liner, plus a modest flow cut; lower flow alone (a) stays the fallback | `cad/src/model.py`: bore 25 to 50 mm, liner 34 to 59 mm OD, tube 40 to 65 mm OD, caps 60 to 90 mm, window 32 x 6 to 57 x 10 mm on a 51 mm seat, LED circle 16 to 32 mm, sink 64 to 90 mm, M4 to M5 tie rods. Liner reflectance 0.80 to 0.95. Design flow 2.0 to 1.2 L/min, the largest round flow that keeps the 20 % margin (limit 1.30 L/min, LMF-CAL-001 v0.2, J1). RED at 90 %/cm 14.7 to 19.0 became 51.9 to 76.3 mJ/cm²; R2 not met became met. R1 restated to 1.2 L/min |
| E3 | Dose monitor position (R4) | Move the photodiode from the top disc to the tube wall at mid height and keep the proportional mapping | Photodiode, sensor window and a clamp-on saddle at Z = 166 mm in the model; top disc now solid. Signal at 90 %/cm 2.4 to 16.3 nA; at 70 %/cm unresolved to 0.38 nA. R4 stays at risk (firmware and test needed). The optional second reference sensor was not added |
| E4 | Budget (R16) | Option (c): hold the budget until the R2 route is chosen, then re-price | BOM re-priced for the 50 mm reactor: $249.00 to $338.00. The recommendation named no figure that covers this total (option (a) was $250), so `budget_usd` stays at $225 and the new figure is an open item (O4) |
| E5 | Flow sensor pulse rate (R5) | A sensor of 15 Hz per L/min or more | BOM line 8 and the calc: worst-case switch-on 0.46 to 0.24 s; R5 at risk became met |
| E6 | R8 wording | State that the 0.5 bar excludes the flow restrictor; confirm the sensor and valve flow coefficients from datasheets | R8 restated in LMF-REQ-001 v0.4. Pressure drop 0.42 to 0.15 bar at the new flow; R8 at risk became met. Datasheet values are to be read when specific parts are chosen |
| E7 | Pressure limiter | An upstream pressure-limiting valve is an installation requirement | New R17 (limiter at 4 bar or less). Window 3.09 MPa at 4 bar and 6.18 MPa at a transient of twice the setting, against 6.8 MPa. Installation part, not in the BOM, like the sediment pre-filter |
| E8 | Thermal cut-back | A board temperature sensor that cuts LED current above 50 °C | NTC on the LED board (BOM line 4) and a dimming input on the driver (line 10); R10 restated. Board 44.1 to 55.9 °C became 37.1 to 44.8 °C with the larger sink and cap; R10 at risk became met. The cut-back is a firmware rule, documented only |

*Table 2. Items still open (Proposed, awaiting Amish).*

| # | Item | Why it stays open |
| --- | --- | --- |
| O1 | Partner that can supply real well-water UVT data (DDR-001 O1) | No recommendation was made; partners are picked per area later |
| O4 | Budget figure for the $338.00 BOM | New after re-pricing. Options: (a) raise `budget_usd` to about $340; (b) keep $225 and cut cost, for example a plain PTFE liner (46.3 mJ/cm² at 1.2 L/min, below the 20 % margin) or fewer machined parts; (c) keep $225 and leave R16 visibly not met. **Budget top-up to $340: decided by Amish, 2026-09-26** ("I am ok with the budget top ups"). `budget_usd` is now 340 and R16 is met ($338.00, $2.00 under; LMF-REQ-001 v0.5, LMF-CAL-001 v0.3) |

*Table 3. Decided but on hold (TRL 4, on hold by Amish's instruction).*

| Item | Work on hold |
| --- | --- |
| E2 | Measuring the wetted liner reflectance at 275 nm and biodosimetry of the reactor |
| E3, E8 | Firmware for the dose mapping, the 1 s fail-safe and the thermal cut-back, beyond a labeled sketch |
| E4 | Quotes and purchasing for the re-priced BOM |

## Consequences

- LMF-PRB-001 v0.4, LMF-PRC-001 v0.4, LMF-REQ-001 v0.4, LMF-CAL-001 v0.2 and LMF-DDR-001 v0.2 record these decisions.
- `cad/src/model.py`, the STEP and STL exports, drawing LMF-DWG-001 (Rev P1 to P2), the concept sheet LMF-DWG-010 (Rev P2), all media and `bom/bom.csv` follow the new design.
- Requirement status (LMF-CAL-001 v0.2): 13 met, 1 at risk (R4), 2 not met (R3, accepted by D1; R16), 1 not verifiable at TRL 3 (R15). Before: 8 met, 4 at risk, 3 not met, 1 not verifiable, of 16.
- `project.yaml` keeps `trl: 3` and `trl_target: 3`; `budget_usd` stayed at 225 until the budget top-up to $340 (O4, decided by Amish on 2026-09-26), after which R16 is met and the count is 14 met, 1 at risk, 1 not met (R3), 1 not verifiable. The pitch is unchanged; it does not name a flow rate.
- No other repo is affected: LumaFlow uses no SwapCell pack or shared part.
