---
doc_id: LMF-DEC-001
title: LumaFlow design decisions register
project: LumaFlow
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
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
---

# LumaFlow design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The flow sensor and the valve have a 3/8 in push-fit port at each end and a flat face for the saddle, and their port centres match the stem height | The stem adaptors plug straight into them and the saddles steady them | LMF-DDR-003, P6 and P9 |
| 2 | Flow coefficients (Kv) of the flow sensor and the valve | R8 rests on assumed values of 0.35 and 0.25 | LMF-CAL-001 [G1]; LMF-DDR-002 E6 |
| 3 | The heat sink's fin gaps are 7.5 mm or more, with nine fins on 90 x 90 mm | The M4 socket heads of the LED head sit in the gaps | LMF-DDR-003, P3 |
| 4 | The LED board's output bin at 275 nm and its mounting holes (three on a 38 mm circle) | The dose rests on 60 mW per LED; the board screws to the sink | LMF-CAL-001 [B1]; BOM line 4 |
| 5 | The pipe clamp's band and rubber are 3 mm thick or less in total | The tie rods pass 2 mm outside the clamp | LMF-DDR-003, P2 |
| 6 | The stem adaptors are 1/4 BSPP male with a 3/8 in stem, stainless, food-contact | The cap ports are tapped 1/4 BSPP | LMF-DDR-003, P6 |
| 7 | The PTFE liner supplier's reflectance data at 275 nm, wetted | R2 rests on 0.95; plain PTFE gives 45.2 mJ/cm² | LMF-CAL-001 [B8] |
| 8 | Seal materials are food-contact EPDM, the O-ring size (about 61 mm inside, 1.78 mm section) is stocked, and a 0.5 mm food-contact PTFE washer for the window seat (decided 2026-10-02) | Wetted parts (R11) | LMF-DDR-003, P1 and P4; this register, 2026-10-02 |
| 9 | The LED head plug and socket are 6-pin, about 12 mm across (GX12 class), and fit the 12 mm hole in the enclosure floor; the LED bar module fits behind the five 6 x 8 mm segments in the lid | The interlock loop (R12) and the UV level bar (R18) | This register, 2026-10-02; BOM lines 10 and 13 |

## Value engineering

Value-engineering target: USD 340 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 416 (USD 76 over the target). Main cost drivers and savings worth trying:

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
