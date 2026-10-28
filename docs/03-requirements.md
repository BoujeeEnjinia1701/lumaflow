---
doc_id: LMF-PRS-001
title: LumaFlow product requirements and specifications
project: LumaFlow
doc_type: Product requirements and specifications
version: "0.9"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions (LMF-DDR-001); R16 redefined to $225; R7 design stress sourced (6.8 MPa); status from LMF-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); R1 to 1.2 L/min, R8 restated, R10 adds the thermal cut-back, new R17 pressure limiter; status from LMF-CAL-001 v0.2
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish; R16 target $340, now met (LMF-CAL-001 v0.3)
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Rerun for the constructable design (LMF-DDR-003); R16 reported against the value-engineering target; R15 note
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R12 status names the LED head loop wire; R18 added for the five-segment UV level bar (LMF-DEC-001, 2026-10-02)"
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Approved follow-ups carried out (LMF-CAL-001 v0.6): R18 now met; R12 interlock now in the model and build plan; R2, R3, R4, R10 and R16 figures updated for the PTFE window washer and the new BOM lines"
- version: "0.9"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.8 upgrade: LMF-REQ-001 becomes LMF-PRS-001; R1 to R18 migrated to PR-001 to PR-018 with the same targets (old number in Was), tolerance, units and the user requirement each traces to; PR-019 (honest claims) added; PR-011 updated for the expanded PTFE gasket (LMF-DEC-001 D-S1); after the independent review PR-002 and PR-008 at risk, PR-005 start-up by the outlet pressure sensor (D-S3), alarm threshold weighted for 275 nm (D-S4); cost USD 433"
---

# LumaFlow product requirements and specifications

What the design must do, each traced to a user need in LMF-URS-001. Targets are proposals for review with a co-design partner. Method: STANDARDS section 22. Status comes from the calculation note LMF-CAL-001 v0.7 (tags such as [B5] point to the line of `docs/04-calcs/sizing.py` that prints the number) and the STEM check LMF-STM-001. This document replaces LMF-REQ-001; the R numbers survive in the "Was" column. On paper, 13 of 19 requirements are met. PR-003 is **not met** (dose at the 70 %/cm test water, kept visible by decision D1). Three are **at risk**: PR-002 (the clear-water dose is 47.3 mJ/cm² with the 275 nm response factor, 18 % over 40 against the 20 % margin the note asks for), PR-004 (the dose rule and 1 s fail-safe need firmware and a test) and PR-008 (the pressure drop depends on the valve's flow coefficient). PR-015 can only be verified on a build, and PR-016 is **over its value-engineering target** by USD 93 (USD 433 against USD 340).

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-002 | Performance | Drinking-water flow | The unit shall deliver its design flow at the faucet, capped by a flow restrictor | 1.2 (0.32 gpm) | +0 / -0.2 | L/min | Analysis (CAL A3), TRL 3; restrictor rating | Met by design [A3] | R1 |
| PR-002 | UR-001 | Performance | Class A dose level in clear water | The reduction equivalent dose (RED) at the design flow and 90 %/cm UV transmittance shall reach the target | 40 | min; 20 % margin for Met | mJ/cm² | Analysis (ray trace, CAL B5), TRL 3; biodosimetry at TRL 4 | At risk: 50.9 (laminar) to 74.9 (plug) [B5]; 47.3 with the 275 nm response factor of 0.93 [B10], margin 18 % against the 20 % rule; 37.5 with a worst-case LED derating stack [B11] (STM S33); mixing to verify (S34) | R2 |
| PR-003 | UR-003 | Performance | Dose at the test water quality | The RED at the design flow and 70 %/cm UVT shall reach the target | 40 | min | mJ/cm² | Analysis (CAL B6), TRL 3 | Not met: 17.0 to 21.3 [B6], 15.8 with the 275 nm factor [B10]; kept visible by decision D1 | R3 |
| PR-004 | UR-004, UR-003 | Safety | Dose monitor and fail-safe | A UV-C sensor reading through the water shall trip a visual and audible alarm and close the outlet valve when the estimated dose falls below 40 mJ/cm², the sensor fails or power is lost | 1 | max | s | Analysis (CAL C1 to C5), TRL 3; firmware review and test at TRL 4 | At risk: 13.4 nA at 90 %/cm; alarm at S/S_ref 0.85, set from the 275 nm weighted RED, below about 89 %/cm and on one failed LED [C1, C3, C4]; mapping and 1 s fail-safe need firmware and a test | R4 |
| PR-005 | UR-005 | Software | Switch with the flow | The LEDs shall be on within the target time of flow above 0.3 L/min, held on 5 s after flow stops, and off otherwise | 0.5 | max | s | Analysis (CAL D2, D5), TRL 3 | Met on paper: the outlet pressure sensor wakes the unit when the faucet opens, LEDs on before the valve opens; 0.24 s to confirm flow at 0.3 L/min [D2, D5] | R5 |
| PR-006 | UR-005, UR-006 | Materials | No mercury, no warm-up | No part shall contain mercury; full UV output shall be reached within the target time of switch-on | 0.1 | max | s | Inspection of BOM and LED datasheet, TRL 3 | Met by design | R6 |
| PR-007 | UR-007 | Physical architecture | Window under pressure | The quartz window stress at 8 bar (116 psi) shall not exceed the target | 6.8 | max | MPa | Analysis (CAL G4), TRL 3; pressure test at TRL 4 | Met on paper: 6.18 [G4] | R7 |
| PR-008 | UR-008 | Performance | Pressure drop | The drop across the unit at the design flow, excluding the restrictor, shall not exceed the target | 0.5 (7 psi) | max | bar | Analysis (CAL G2), TRL 3; datasheet Kv at part selection | At risk: 0.15 on assumed Kv [G2]; 0.59 with a direct-acting valve of Kv 0.10 [G9] (STM S22) | R8 |
| PR-009 | UR-009 | Electrical | Energy use | Mains power shall not exceed 25 W while water flows nor the standby target | 0.5 (standby); 25 (flowing) | max | W | Analysis (CAL E1, E2), TRL 3 | Met on paper: 22.6 and 0.23 [E1, E2] | R9 |
| PR-010 | UR-010 | Physical architecture | LED board temperature | The LED board shall stay at or below the target with 30 °C air and 25 °C water, including the 5 s run-on; a board sensor shall cut LED current above it | 50 | max | °C | Analysis (CAL F3), TRL 3 | Met on paper: 37.3 to 45.1 [F3]; the film coefficient in the cap bore is about 490 W/(m² K) for developing flow, above the 150 low end (STM S35) | R10 |
| PR-011 | UR-011 | Materials | Food-safe wetted parts | Every wetted material shall be food-contact grade, and no UV-C shall fall on any polymer or elastomer other than PTFE | 0 | none | UV-C on other polymers | Inspection of the model and BOM, TRL 3; PTFE transmittance at TRL 4 | Met by design: window gasket and sensor washer now expanded PTFE (LMF-DEC-001 D-S1); light reaching the acetal cap through 3 mm of PTFE to verify at TRL 4 (STM S10) | R11 |
| PR-012 | UR-012 | Safety | Contain the UV-C | No UV-C shall leave the unit in normal use; the LEDs shall not run with the LED head or enclosure lid removed | 0 | none | exposed UV-C paths | Inspection (design review, model check), TRL 3 | Met by design: lid reed switch; interlock loop in the LED head plug on a cable 39 mm short of letting the head clear the cap | R12 |
| PR-013 | UR-013 | Electrical | Electrical safety | Only 24 V DC shall be present at the unit; mains confined to a certified external adapter; fuse on the 24 V input | 24 | max | V DC | Inspection, TRL 3 | Met by design | R13 |
| PR-014 | UR-014 | Physical architecture | Fit under a sink | The unit without the adapter shall fit inside the target envelope | 350 x 150 x 350 | max | mm | Analysis (model, CAL H1), TRL 3 | Met on paper: 277 x 100 x 322 [H1] | R14 |
| PR-015 | UR-015, UR-017 | Usability | Easy service | Window and LED head shall be replaceable with hand tools within the target time; the status display shall show run, fault and service due | 15 | max | min | Demonstration on a build, TRL 4 | To verify at TRL 4 | R15 |
| PR-016 | UR-016 | Physical architecture | Cost and buildability | Estimated parts cost against the value-engineering target (`budget_usd`, a hypothetical control target, not a limit); no custom PCB for the first build | 340 | target | USD | Analysis (priced BOM, CAL I1), TRL 3 | Over target: USD 433, USD 93 over [I1] | R16 |
| PR-017 | UR-007 | Safety | Pressure protection (installation) | A pressure-limiting valve upstream shall be set at or below the target so transients stay within the window rating | 4 (58 psi) | max | bar | Analysis (CAL G5), TRL 3; installation instructions | Met on paper: 3.09 MPa at 4 bar, 6.18 MPa at twice the setting [G5] | R17 |
| PR-018 | UR-017 | Usability | UV level at a glance | A five-segment bar on the lid shall show the UV level relative to the alarm threshold, read from the wall sensor, labelled as UV level, not as a dose | 5 | segments | count | Analysis (CAL C6), TRL 3; bench check at TRL 4 | Met by design: 2 of 5 at 90 %/cm with the weighted threshold, last segment out at the alarm [C6] | R18 |
| PR-019 | UR-018 | Safety | Honest claims | The product label, README and every document shall state that LumaFlow is a research and educational prototype, not a certified water treatment device, and shall not claim virus removal | 0 | none | certification or virus claims | Inspection of labels and documents, TRL 3 | Met by design (BOM line 19; PRC safety; STM S5) | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- **Water quality.** The design water is clear, pre-filtered well water (decision D9): UVT of 90 %/cm or better at 275 nm, turbidity below 1 NTU, after a 5 µm sediment pre-filter. UVT must be measured for each site. Iron, manganese and hardness foul the window and must be within the limits commonly given for UV systems; this is an installation requirement, not a LumaFlow feature.
- **Dose target.** 40 mJ/cm² is the NSF/ANSI 55 Class A dose level. Reaching it would not make LumaFlow Class A compliant or certified. It gives 4-log inactivation of *Cryptosporidium* and *Giardia* (22 mJ/cm² each, 40 CFR 141.720) but only about 0.5 log of virus such as adenovirus, which needs 186 mJ/cm² for 4 logs. RED in LMF-CAL-001 is computed for a challenge organism of 20 mJ/cm² per log, taken as equally sensitive at 275 and 254 nm; the measured ratio for MS2 at 280 nm is 0.93 (Beck et al. 2017; LMF-STM-001, S3).
- **Liner reflectance.** PR-002 rests on a wetted reflectance of 0.95 for the high-reflectance PTFE liner, which must be measured; plain PTFE (0.80) would give 45.2 mJ/cm², still above 40 (LMF-CAL-001, B8).
- **Pressure.** The pressure-limiting valve (PR-017) is part of the installation, like the sediment pre-filter, and is not in the LumaFlow BOM.
- **Demand.** 10 to 20 L per household per day, drawn in about 20 short draws.
- PR-003 is kept as stated so that the gap stays visible. The PR-016 figure of USD 340 is a value-engineering target (Amish, 2026-10-01); the cost drivers and savings worth trying are in the design decisions register, LMF-DEC-001.
