---
doc_id: LMF-DDR-003
title: LumaFlow design for construction
project: LumaFlow
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction and open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. Made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The LumaFlow model of LMF-DDR-002 shows what the reactor does and carries every calculation, but checking it with build123d (overlaps, contacts, removal paths and the process for each part) found eleven places where a part could not be fitted, fixed, sealed or made as drawn (P1 to P11 below).

The changes keep what LumaFlow does: the same 50 mm bore and 242 mm water column, the same six LEDs 0.8 mm under the same 57 x 10 mm window on a 51 mm open span, the same wall sensor position, ports, flow, power and envelope. The optics, dose, dose monitor, pressure drop and window stress results of LMF-CAL-001 are unchanged. Nothing here changes the pitch or the safety case; one item that touches the safety case is left as a proposal (Table 3, A1). Every change is in `cad/src/model.py`, which now runs 324 constructability checks (`python cad/src/model.py --check`): no two parts overlap, the parts of every joint touch, the listed parts keep their clearances, and the window and the LED head each have a clear path out. All 324 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The 57 mm window sat in a pocket closed above by the 50 mm bore and below by the 51 mm seat, both narrower than the window, so it could not be put in; it also had no seal. | The pocket is open to the bottom face. The window goes in from below onto a 1 mm EPDM gasket against a new shoulder 13 mm up, and is held by a 316 retaining ring (72 x 51 x 2 mm) with six M3 countersunk screws, flush in a recess in the cap's bottom face. | The way a sight glass is clamped. Water pressure pushes the window onto the ring, so the ring carries the load, as the concept's seat did. The open span (51 mm), the window's height and the 0.8 mm LED gap are unchanged, so the stress [G4] and the optics are unchanged. |
| P2 | The tie rods started at the top of the heat sink base, in 1 mm deep holes, with nothing under them; a nut (8 mm across flats) does not fit the 7.9 mm gap between fins. | Four M5 316 studs threaded 12 mm into the stainless lower cap with threadlocker, through the upper cap, with washers and acorn nuts. Pitch circle 78 to 80 mm, so the studs clear the pipe clamps by 2 mm. | The studs now hold the two caps together against the 2,655 N end load [G7] and nothing else, and the LED head can come off without loosening them. |
| P3 | The LED head (sink, spreader ring, board) had no fixing of its own; the board was loose in the ring with no route out for its cable. | Four M4 socket screws from below, through the fin gaps, the sink base and the ring into the lower cap; three M3 screws hold the board to the sink base; an 8 mm slot in the ring takes the LED cable toward the enclosure. | The head comes off from below with a hex key without opening the water side, which serves R15. |
| P4 | Each tube end butted on a flat cap face with no seal and no location. | The tube is 204 mm long and sits 2 mm into a seat in each cap, on a 1.78 mm EPDM face O-ring in the floor of the seat. In the lower cap the seat leaves a 59 mm spigot that locates the tube and carries the liner. The liner's top 22 mm is turned down to 56 mm so the upper O-ring groove keeps a 1.9 mm wall from the liner pocket. | A face seal pressed by the studs, and a location at each end. The wetted steel length in the lower cap is unchanged, so the thermal path [F2] is unchanged. |
| P5 | The acetal upper cap's roof over the liner pocket was 3 mm thick: about 59 MPa at 8 bar, near the short-term strength of acetal. | Upper cap 30 to 40 mm tall: a 13 mm roof over a 56.2 mm pocket, 2.8 MPa at 8 bar [G8]. | The highest point of the unit is still the valve coil, so the envelope (277 x 100 x 322 mm) is unchanged. |
| P6 | The ports were plain 7 mm holes in 13.5 mm bosses, with no thread for a fitting; the flow sensor and valve were joined to them by 10 mm stubs of tube, too short for push-fit joints. | 20 mm bosses tapped 1/4 BSPP; stainless push-fit stem adaptors screw in, and their stems plug straight into the push-fit ports of the flow sensor and the valve, which keep their positions. | Catalogue parts; no tube stub to cut or kink. |
| P7 | The 316 outlet insert overlapped the PTFE liner by 0.1 mm. | A 316 sleeve 9.5 x 7 x 17 mm pressed into a 9.6 mm bore in the upper cap, ending at the liner's outside face, in line with the liner's 7 mm outlet hole. | Keeps UV-C off the acetal bore, as LMF-DDR-002 E1 requires, without a clash. |
| P8 | The "clamp-on" sensor saddle had no clamp, and the sensor window was a rod through the liner and the tube wall with no seal. | A 316 boss TIG-welded to the tube at mid height, bored 8 mm through; a 10 x 3 mm quartz sensor window on a 0.5 mm EPDM washer in a 10.2 mm seat, pressed by a 316 photodiode holder screwed in on an M12 x 1 thread. | One sealed, welded joint on the pressure wall. The 8 mm open span keeps the window stress at 1.69 MPa [G6]. |
| P9 | The bracket was a printed plate with two closed rings and a solid shelf: the reactor could only be threaded through the rings before its caps went on, the enclosure had no fixing on the shelf, the plate had no wall holes, and the flow sensor and valve had no support. | A 6 mm aluminium plate (242 x 270 mm), drilled and tapped; two bought rubber-lined 65 mm pipe clamps on M8 studs, which open to take the reactor; the enclosure's back screwed straight to the plate with four M4 screws (it moves 27 mm back, same footprint); two printed saddles with a cable tie each steady the flow sensor and the valve; four wall holes. | Every joint is a screw into a tapped hole or an insert, and the reactor can be lifted out after opening two clamps. |
| P10 | The enclosure was one closed box with no lid, although it carries a lid interlock. | A printed body open at the front and a screw-on lid that carries the light pipe and the magnet for the reed switch. | The lid interlock of R12 needs a lid. |
| P11 | The heat sink fins stood on the cabinet floor, at the same level as the adapter. | The unit hangs on its bracket with 25 mm of air under the fins; the adapter stays on the floor. | The thermal calculation [F1] assumes free air round the fins. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Cost | BOM lines 1, 2, 4 to 9, 11, 13 to 16 respecified and repriced; line 17 (retaining ring and seals, $12) and line 18 (pipe clamps, $8) added. Value-engineering target: USD 340. Estimated cost of the constructable design: USD 402 (USD 62 over the target) [I1]. The concept was $338.00. | Parts and machining added for construction. Savings worth trying are in the design decisions register (LMF-DEC-001). |
| Calculations | LMF-CAL-001 v0.4: new G8 (upper cap roof); heat capacity 802 to 781 J/K [F1]; acetal-cap comparison 31.4 to 30.5 min [F5]; R16 reported against the target. Dose, monitor, power, pressure drop, window, size and requirement status otherwise unchanged. | Follows the model. |
| Drawings | LMF-DWG-001 Rev P4; concept sheet LMF-DWG-010 Rev P4; making sketches LMF-DWG-101 to 111 added. | Follows the model. |
| Documents | LMF-REQ-001 v0.6 (R15 note, R16 wording), LMF-PRC-001 v0.6 (components 13 to 18, cost), LMF-PRB-001 v0.6 (cost line). No requirement changed status other than R16, which is now reported as over its value-engineering target. | Follows the model and Amish's 2026-10-01 instruction on budgets. |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | R12 says the LEDs cannot run with the LED head removed, but the concept has no mechanism for this; now that the head comes off on four screws, it matters. This touches the safety case. | (a) a loop wire in the LED head's plug, so the head cannot come off without unplugging it, which opens a loop the controller watches and cuts the LED supply; (b) a microswitch pressed by the sink base; (c) rely on the procedure and the lid interlock alone. | (a): one more wire pair, no moving part. |
| A2 | The window bears on the lapped stainless ring, metal to glass, as on the concept's seat. A thin PTFE washer under it would spread the load but lift the window 0.5 mm, which changes the LED gap and needs the ray trace re-run. | (a) metal to glass on a lapped ring, as modelled; (b) add a 0.5 mm PTFE washer and re-run LMF-CAL-001 section B. | (a) for the first prototype; look at the window edge after the TRL 4 pressure test. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan LMF-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: 13 met, 1 not met (R3, accepted by D1), 1 at risk (R4), 1 not verifiable at TRL 3 (R15), and R16 over its value-engineering target by USD 62 (LMF-CAL-001 v0.4).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: closed bracket rings, a 30 mm upper cap, the clamp-on sensor saddle and the shelf-mounted enclosure. They need updating on Amish's Mac, where Blender is.
- The flow sensor and valve must have push-fit ports at both ends and a flat face for the saddle; the heat sink's fin gap must take an M4 socket head. These are items to confirm when parts are bought (LMF-DEC-001).
