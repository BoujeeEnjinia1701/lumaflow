---
doc_id: LMF-DEC-001
title: LumaFlow design decisions register
project: LumaFlow
doc_type: Design decisions register
version: '0.5'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; budget treated as a value-engineering target
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for open decisions 1 to 10 (LMF-DDR-003 accepted with the window seat changed); moved to decisions made; To confirm item 8 and Value engineering updated"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Approved follow-ups carried out: Value engineering repriced (USD 416) with the washer, interlock plug, UV level bar and labels; To confirm items 7 and 9 updated"
- version: "0.4"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: open decision O-1 (concept selection, A and B to Amish, LMF-DDR-004); STEM fixes D-S1 (expanded PTFE gasket and sensor washer) and D-S2 (ring screws 0.3 N m) decided under Amish's standing instruction of 2026-10-23; Value engineering USD 433; after the independent review D-S2 revised, D-S3 (outlet pressure sensor), D-S4 (weighted alarm threshold), open O-3 (dose margin) and O-4 (mixing)"
- version: '0.5'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Amish decided O-4 (option (a), tracer test at TRL 4) and the indoor product render site as recommended on 2026-10-25 ("i concur with your recommendations"); O-1, O-2 and O-3 stay open (no pick)'
---

# LumaFlow design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | To be decided | Options | Recommendation | What it affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| O-1 | Concept selection | A, axial UV-C LED reactor (228 of 275); B, hollow-fibre ultrafilter (229); C, radial UV-C LED reactor (204) | Proposed, awaiting Amish: A and B are within 10 %, so both go to Amish without a pick. Keeping A keeps the pitch and the build plan; B would change the pitch and every design document. C is not recommended | Nothing until decided; the build plan, drawing and BOM describe A | LMF-OPT-001, LMF-DDR-004 |
| O-3 | Dose margin once the LED is chosen | If the chosen LED's datasheet confirms the derating stack (37.5 mJ/cm² worst case, LMF-CAL-001 B11): (a) a seventh and eighth LED on the same board (about USD 18, +4.3 W), (b) buy a guaranteed high output bin, (c) lower the design flow to about 1.0 L/min | Proposed, awaiting Amish: decide after the LED is chosen; (b) first, then (a). (c) changes a requirement Amish set (LMF-DDR-002) | LED board, driver current, power budget, or flow | LMF-STM-001 S33 |
| O-2 | Graft from the runner-up | If A: an automatic leak and stuck-valve check on each idle pulse with the valve shut (no new parts). If B: a flow-switched normally closed valve with an alarm on a differential pressure sensor | Proposed, awaiting Amish, after O-1 | Firmware rule (A) or new parts (B) | LMF-OPT-001, Recommendation |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The flow sensor and the valve have a 3/8 in push-fit port at each end and a flat face for the saddle, and their port centres match the stem height | The stem adaptors plug straight into them and the saddles steady them | LMF-DDR-003, P6 and P9 |
| 2 | Flow coefficients (Kv) of the flow sensor and the valve | R8 rests on assumed values of 0.35 and 0.25; a direct-acting valve of Kv 0.10 gives 0.59 bar (over 0.5) | LMF-CAL-001 [G1]; LMF-DDR-002 E6 |
| 3 | The heat sink's fin gaps are 7.5 mm or more, with nine fins on 90 x 90 mm | The M4 socket heads of the LED head sit in the gaps | LMF-DDR-003, P3 |
| 4 | The LED board's output bin at 275 nm and its mounting holes (three on a 38 mm circle) | The dose rests on 60 mW per LED; the board screws to the sink | LMF-CAL-001 [B1]; BOM line 4 |
| 5 | The pipe clamp's band and rubber are 3 mm thick or less in total | The tie rods pass 2 mm outside the clamp | LMF-DDR-003, P2 |
| 6 | The stem adaptors are 1/4 BSPP male with a 3/8 in stem, stainless, food-contact | The cap ports are tapped 1/4 BSPP | LMF-DDR-003, P6 |
| 7 | The PTFE liner supplier's reflectance data at 275 nm, wetted | R2 rests on 0.95; plain PTFE gives 45.2 mJ/cm² | LMF-CAL-001 [B8] |
| 8 | The window gasket and sensor washer are food-contact expanded PTFE (D-S1, 2026-10-25), the O-rings food-contact EPDM, the O-ring size (about 61 mm inside, 1.78 mm section) is stocked, and a 0.5 mm food-contact PTFE washer for the window seat (decided 2026-10-02) | Wetted parts (R11) | LMF-DDR-003, P1 and P4; this register, 2026-10-02 |
| 10 | The chosen LED's output bin and its output at a 60 to 65 °C junction | The dose margin (O-3) and the alarm reference |  LMF-CAL-001 B11; LMF-STM-001 S33 |
| 11 | The valve, flow sensor and pressure sensor have plastic or stainless wetted parts (no brass) in food-contact, lead-free grades | PR-011, NSF/ANSI 61 and 372 to assess | LMF-STM-001 S31, S32 |
| 9 | The LED head plug and socket are 6-pin, about 12 mm across (GX12 class), and fit the 12 mm hole in the enclosure floor; the LED bar module fits behind the five 6 x 8 mm segments in the lid | The interlock loop (R12) and the UV level bar (R18) | This register, 2026-10-02; BOM lines 10 and 13 |

## Value engineering

Value-engineering target: USD 340 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 433 (USD 93 over the target). The STEM fixes of 2026-10-25 added an estimated USD 17: the expanded PTFE gasket in place of EPDM (USD 2 on line 17, D-S1) and the outlet pressure sensor with its tee (USD 15, new line 20, D-S3); both prices are estimates to confirm with suppliers. Main cost drivers and savings worth trying:

- The largest lines are the six UV-C LEDs (USD 54), the machined 316 lower cap (USD 48), the high-reflectance PTFE liner (USD 45), the tube with its welded sensor boss (USD 38) and the quartz window (USD 32).
- Making the design constructable added USD 64: the welded sensor boss (USD 12 more on the tube line), the retaining ring and seals (USD 12), the threaded ports and stem adaptors (USD 10 more on fittings), the drilled bracket plate and saddles (USD 10 more), the pipe clamps (USD 8), more machining on both caps (USD 9), more fixings (USD 4) and drilling of the heat sink (USD 1), less USD 2 on the sensor line.
- Savings worth trying: a plain PTFE liner instead of the high-reflectance grade (most of USD 45, but the laminar dose falls to 45.2 mJ/cm², inside the 20 % margin, so R2 would be at risk); a clamp-on saddle with a band clamp instead of the welded boss (about USD 10); one machine shop quote for both caps, the tube boss and the holder together; LED prices at quantity, which fall fastest of all the lines.
- The decisions of 2026-10-02 added USD 14, now priced in the BOM: the PTFE window washer (USD 2), the LED head plug, socket and interlock-loop cable (USD 4), the five-segment UV level bar (USD 3) and the labels line (USD 5). Labels printed in-house on vinyl would save most of their USD 5.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: design for 90 %/cm water with alarm and valve closure below 40 mJ/cm², R3 kept visibly not met; budget to $225; axial LED head with a flat quartz window; 275 nm LEDs; Hall-effect flow sensor; normally closed valve; vertical mounting with upward flow; external certified 24 V adapter; first user a well-water household | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | LMF-DDR-001 |
| 2026-09-25 | TRL 3 items E1 to E8: 316 lower cap and shielded acetal upper cap; 50 mm bore, high-reflectance liner and 1.2 L/min; wall dose sensor; hold the budget and re-price; 15 Hz per L/min flow sensor; R8 excludes the restrictor; upstream pressure limiter; thermal cut-back | Amish: "i accept all your recommendations, go with them across all repos." | LMF-DDR-002 |
| 2026-09-26 | Budget top-up to $340 for the $338.00 concept BOM | Amish: "I am ok with the budget top ups" | LMF-DDR-002, O4 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | LMF-DDR-003 (accepted on 2026-10-02, below) |
| 2026-09-30 | Outstanding decisions go in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, reported as over or under, not as a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | LMF-CAL-001 v0.4, LMF-REQ-001 v0.6 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P11 as made, except the window seat of P1, which is settled by the PTFE washer decision below (window on a 0.5 mm PTFE washer, not metal to glass) | Amish: "i approve your recommendations for all 555 open decisions." | LMF-DDR-003, P1 to P11 |
| 2026-10-02 | LED head interlock (R12): a loop wire in the LED head's plug that the controller watches (option a), with the LED cable routed so it is too short for the head to come off while still plugged in | Amish: "i approve your recommendations for all 555 open decisions." | LMF-DDR-003, A1 |
| 2026-10-02 | Window seat: a 0.5 mm PTFE washer under the window (option b), with the optical check re-run for the 0.5 mm larger LED gap; metal on glass only if a TRL 4 pressure test on that seat shows no edge chipping. This differs from the register's earlier recommendation (a) | Amish: "i approve your recommendations for all 555 open decisions." | LMF-DDR-003, A2 |
| 2026-10-02 | Partner for well-water UV transmittance data: a university extension programme for private well owners, with the Texas A&M AgriLife Extension Texas Well Owner Network as the first candidate to approach | Amish: "i approve your recommendations for all 555 open decisions." | LMF-DDR-001 O1, LMF-DDR-002 O1 |
| 2026-10-02 | Dose bar: keep the five-segment bar on the enclosure and add it to the requirements (R18), labelled as UV level relative to the alarm threshold, read from the wall sensor, not as a dose in units | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 1 |
| 2026-10-02 | Tie rods: acorn nuts, as already in the constructable design | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 2 |
| 2026-10-02 | Solenoid connector and port collars accepted as drawn in the renders (catalogue-part detail) | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 3 |
| 2026-10-02 | Hero render: show the cord entering the cabinet wall; keep the adapter in the model and the BOM | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 4 |
| 2026-10-02 | Labels: a labels line in the BOM now, with a UV-C warning label on the lower cap and on the inside of the enclosure lid, and the product label | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 5 |
| 2026-10-02 | Idle LED pulse: a firmware rule runs the LEDs for about 10 s every 4 h of idle, with both interlocks and the valve logic unchanged; its effect checked with plate counts at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | LMF-PRC-001, open questions |
| 2026-10-25 | D-S1, STEM fix: the window gasket and the sensor window washer are food-contact expanded PTFE instead of EPDM, because UV-C refracted outward in the window reaches them (about 4.2 % of the LED output, 2.6 mW/cm²; LMF-STM-001 S9). Options weighed: PTFE-enveloped rubber gasket, metal mask ring, expanded PTFE (chosen, same size, no geometry change). Cost about USD 2 (estimate) | Decided by Claude under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix for the design and its constructability"); Amish can reverse it | LMF-STM-001 S9 |
| 2026-10-25 | D-S2, STEM fix: the six M3 retaining ring screws are A4, threads in anti-seize, tightened to 0.21 N·m, and the ring is 316 sheet (not 316L), because 0.5 N·m dry bends the 2 mm ring to about its proof stress (202 MPa) and overloads the PTFE washer. First set at 0.3 N·m dry; the independent review showed the dry nut factor scatters too widely (0.15 overstresses the ring, 0.25 unseats the gasket), so anti-seize narrows it to about 0.13 to 0.16: ring at most 131 MPa against 137, gasket at least 1.79 MPa at 8 bar. Options weighed: a 3 mm ring (changes the window height and the optics), Belleville washers (more parts), lubricated threads at a lower torque (chosen). No cost | Decided by Claude under Amish's standing instruction of 2026-10-23; Amish can reverse it | LMF-STM-001 S12, S13 |
| 2026-10-25 | D-S3, STEM fix found by the independent review: an outlet pressure sensor on a push-fit tee between the valve and the faucet starts the unit. With the normally closed valve downstream of the flow sensor, opening the faucet could not make water flow, so the flow sensor could never wake the controller. Now the drop in outlet-line pressure switches the LEDs on, the valve opens 20 ms later and the flow sensor must confirm flow within 0.5 s or the valve shuts again. Options weighed: valve held open in standby (4.8 W, breaks the standby limit), a latching valve with stored energy to close on power loss (more parts, weaker fail-safe), a faucet with a switch (not in the BOM, user-facing), an outlet pressure sensor (chosen: keeps the normally closed fail-safe). Cost about USD 15 (estimate), standby 0.21 to 0.23 W | Decided by Claude under Amish's standing instruction of 2026-10-23; Amish can reverse it | LMF-STM-001 S37; BOM line 20 |
| 2026-10-25 | D-S4, STEM fix found by the independent review: the dose alarm threshold is set from the 275 nm weighted reference dose (47.3 mJ/cm²), so S/S_ref = 0.85 instead of 0.79. At 0.79 the true weighted dose at the alarm point was about 37 mJ/cm², and one failed LED of six (S/S_ref 0.83) would not have tripped it. A firmware parameter; no cost. The UV level bar now shows two of five segments in design water | Decided by Claude under Amish's standing instruction of 2026-10-23; Amish can reverse it | LMF-STM-001 S38; LMF-CAL-001 C3 to C6 |
| 2026-10-25 | O-4 mixing in the reactor: option (a), keep the side inlet and measure the residence-time distribution by tracer test at TRL 4; the perforated PTFE inlet ring (b) is held ready if the test shows strong back-mixing. No part changed | Amish: "i concur with your recommendations" | LMF-STM-001 S34; LMF-RSK-001 P8; LMF-PLN-001 |
| 2026-10-25 | Product render site: the hero is a studio render of the unit in a kitchen sink base cabinet with a 1.75 m mannequin on the kitchen floor, not a kit 1.9 outdoor scene, because the real site is indoors (as proposed on 2026-10-24) | Amish: "i concur with your recommendations" | `cad/src/product_model.py`; `docs/REVIEW.md`, session 2026-10-24 |
