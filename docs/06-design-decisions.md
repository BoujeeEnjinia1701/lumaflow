---
doc_id: LMF-DEC-001
title: LumaFlow design decisions register
project: LumaFlow
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; budget treated as a value-engineering target
---

# LumaFlow design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes (window clamped from below, studs in the lower cap, screwed LED head, sealed tube seats, 40 mm upper cap, threaded ports, welded sensor boss, drilled bracket plate with pipe clamps and saddles, enclosure lid, 25 mm under the fins) | Accept all; accept some and revise others | Accept all | Every component | LMF-DDR-003, P1 to P11 |
| 2 | How the LEDs are stopped when the LED head is off the cap (R12 requires it; the concept had no mechanism) | (a) a loop wire in the LED head's plug that the controller watches; (b) a microswitch pressed by the sink base; (c) procedure and the lid interlock only | (a) | LED head plug and wiring (build plan section 3.12.1) | LMF-DDR-003, A1 |
| 3 | What the quartz window bears on | (a) metal to glass on the lapped stainless ring, as modelled; (b) a 0.5 mm PTFE washer under the window, with the optics re-run | (a) for the first prototype; inspect the window edge after the TRL 4 pressure test | Window stack (build plan section 3.5) | LMF-DDR-003, A2 |
| 4 | Partner that can supply real well-water UV transmittance data and later test the reactor | A well-water association, a university lab or a water charity | None yet (partners are picked per area later) | Not part of the TRL 3 build | LMF-DDR-001 O1, LMF-DDR-002 O1 |
| 5 | Dose bar on the enclosure in the product renders | Keep it and add it to the requirements; remove it from the appearance model | Keep it | Lid light pipe (a five-segment bar instead of one light) | REVIEW 2026-09-26, item 1 |
| 6 | Acorn nuts on the tie rods (appearance model) | Acorn nuts; plain nuts | Acorn nuts | Already used in the constructable design | REVIEW 2026-09-26, item 2 |
| 7 | Solenoid connector and port collars as drawn in the renders | Accept as catalogue-part detail; simplify | Accept | None | REVIEW 2026-09-26, item 3 |
| 8 | Adapter and power cord in the hero render | Show the cord entering the cabinet wall; show the adapter | Show the cord, keep the adapter in the model and BOM | None | REVIEW 2026-09-26, item 4 |
| 9 | Product label and UV-C warning label | Add a labels line to the BOM; leave out | Add a UV-C warning label line at the next BOM revision | A label on the lower cap | REVIEW 2026-09-26, item 5 |
| 10 | A brief LED pulse during long idle periods to limit growth in the reactor | Add a firmware rule; leave out | None yet | Firmware only; not part of the TRL 3 build | LMF-PRC-001, open questions |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The flow sensor and the valve have a 3/8 in push-fit port at each end and a flat face for the saddle, and their port centres match the stem height | The stem adaptors plug straight into them and the saddles steady them | LMF-DDR-003, P6 and P9 |
| 2 | Flow coefficients (Kv) of the flow sensor and the valve | R8 rests on assumed values of 0.35 and 0.25 | LMF-CAL-001 [G1]; LMF-DDR-002 E6 |
| 3 | The heat sink's fin gaps are 7.5 mm or more, with nine fins on 90 x 90 mm | The M4 socket heads of the LED head sit in the gaps | LMF-DDR-003, P3 |
| 4 | The LED board's output bin at 275 nm and its mounting holes (three on a 38 mm circle) | The dose rests on 60 mW per LED; the board screws to the sink | LMF-CAL-001 [B1]; BOM line 4 |
| 5 | The pipe clamp's band and rubber are 3 mm thick or less in total | The tie rods pass 2 mm outside the clamp | LMF-DDR-003, P2 |
| 6 | The stem adaptors are 1/4 BSPP male with a 3/8 in stem, stainless, food-contact | The cap ports are tapped 1/4 BSPP | LMF-DDR-003, P6 |
| 7 | The PTFE liner supplier's reflectance data at 275 nm, wetted | R2 rests on 0.95; plain PTFE gives 46.3 mJ/cm² | LMF-CAL-001 [B8] |
| 8 | Seal materials are food-contact EPDM and the O-ring size (about 61 mm inside, 1.78 mm section) is stocked | Wetted parts (R11) | LMF-DDR-003, P1 and P4 |

## Value engineering

Value-engineering target: USD 340 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 402 (USD 62 over the target). Main cost drivers and savings worth trying:

- The largest lines are the six UV-C LEDs (USD 54), the machined 316 lower cap (USD 48), the high-reflectance PTFE liner (USD 45), the tube with its welded sensor boss (USD 38) and the quartz window (USD 32).
- Making the design constructable added USD 64: the welded sensor boss (USD 12 more on the tube line), the retaining ring and seals (USD 12), the threaded ports and stem adaptors (USD 10 more on fittings), the drilled bracket plate and saddles (USD 10 more), the pipe clamps (USD 8), more machining on both caps (USD 9), more fixings (USD 4) and drilling of the heat sink (USD 1), less USD 2 on the sensor line.
- Savings worth trying: a plain PTFE liner instead of the high-reflectance grade (most of USD 45, but the laminar dose falls to 46.3 mJ/cm², inside the 20 % margin, so R2 would be at risk); a clamp-on saddle with a band clamp instead of the welded boss (about USD 10); one machine shop quote for both caps, the tube boss and the holder together; LED prices at quantity, which fall fastest of all the lines.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: design for 90 %/cm water with alarm and valve closure below 40 mJ/cm², R3 kept visibly not met; budget to $225; axial LED head with a flat quartz window; 275 nm LEDs; Hall-effect flow sensor; normally closed valve; vertical mounting with upward flow; external certified 24 V adapter; first user a well-water household | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | LMF-DDR-001 |
| 2026-09-25 | TRL 3 items E1 to E8: 316 lower cap and shielded acetal upper cap; 50 mm bore, high-reflectance liner and 1.2 L/min; wall dose sensor; hold the budget and re-price; 15 Hz per L/min flow sensor; R8 excludes the restrictor; upstream pressure limiter; thermal cut-back | Amish: "i accept all your recommendations, go with them across all repos." | LMF-DDR-002 |
| 2026-09-26 | Budget top-up to $340 for the $338.00 concept BOM | Amish: "I am ok with the budget top ups" | LMF-DDR-002, O4 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | LMF-DDR-003 (open for review, open decision 1) |
| 2026-09-30 | Outstanding decisions go in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, reported as over or under, not as a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | LMF-CAL-001 v0.4, LMF-REQ-001 v0.6 |
