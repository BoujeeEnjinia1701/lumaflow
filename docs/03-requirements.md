---
doc_id: LMF-REQ-001
title: LumaFlow requirements
project: LumaFlow
doc_type: Requirements
version: "0.8"
status: Draft
date: '2026-10-02'
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
---

# LumaFlow requirements

These are the requirements for the concept, checked by calculation at TRL 3 in LMF-CAL-001 v0.6, for the constructable design of LMF-DDR-003 with the decisions of 2026-10-02 (LMF-DEC-001) carried into it. The status column reports that note; bracketed tags such as [B5] point to the line of `docs/04-calcs/sizing.py` that carries the number. One requirement is **not met**: R3 (dose at the 70 %/cm test condition, accepted as not met by decision D1). R16 (cost) is reported against its value-engineering target: the constructable design is estimated at USD 416, USD 76 over the USD 340 target. One is at risk: R4. The dose targets (R2, R3) and the budget (R16) follow Amish's decisions in LMF-DDR-001; R1, R8, R10 and the new R17 follow the recommendations Amish accepted on 2026-09-25 (LMF-DDR-002).

Table 1. Requirements and status at TRL 3.

| ID | Requirement | Target | Status (LMF-CAL-001 v0.6) | Verification |
| --- | --- | --- | --- | --- |
| R1 | Deliver a useful drinking-water flow | 1.2 L/min (0.32 gpm) at the faucet, capped by a flow restrictor (was 2.0 L/min; reduced by LMF-DDR-002 so that R2 is met with margin) | Met by design [A3] | Restrictor rating; flow calculation |
| R2 | Deliver the Class A dose level in clear water | Reduction equivalent dose (RED) of 40 mJ/cm² or more at 1.2 L/min and UV transmittance (UVT) of 90 %/cm | Met (50.9 laminar to 74.9 plug mJ/cm², with the window on its 0.5 mm PTFE washer) [B5] | Ray-trace dose calculation; later biodosimetry |
| R3 | Deliver the Class A dose level at the NSF/ANSI 55 test water quality | RED of 40 mJ/cm² or more at 1.2 L/min and 70 %/cm UVT | **Not met** (17.0 to 21.3 mJ/cm²) [B6]; kept visibly not met by decision D1 | Dose calculation |
| R4 | Monitor the dose and fail safe | UV-C sensor in the tube wall reading through the water; visual and audible alarm and outlet valve closed within 1 s when the estimated dose falls below 40 mJ/cm², the sensor fails or power is lost | At risk: the wall signal is 13.4 nA at 90 %/cm and 0.19 nA at 70 %/cm, and the proportional mapping trips below about 89 %/cm, but the mapping and 1 s fail-safe need firmware and a test [C1, C4] | Signal calculation; later firmware and test |
| R5 | Switch with the flow | LEDs on within 0.5 s of flow above 0.3 L/min; LEDs held on for 5 s after flow stops; LEDs off otherwise | Met (0.24 s worst case with a 15 Hz per L/min sensor) [D2] | Timing calculation; later firmware sketch review |
| R6 | No mercury and no warm-up | No mercury in any part; full UV output within 0.1 s of switch-on | Met by design | Design review; LED datasheet |
| R7 | Withstand household water pressure | Working pressure 8 bar (116 psi); quartz window stress 6.8 MPa (1,000 psi) or less at 8 bar | Met (6.18 MPa with a 10 mm window on a 51 mm seat) [G4] | Plate stress calculation |
| R8 | Low pressure drop | 0.5 bar (7 psi) or less across the unit at 1.2 L/min, excluding the flow restrictor, which absorbs excess supply pressure by design; sensor and valve flow coefficients from their datasheets | Met (0.15 bar on assumed flow coefficients; datasheet values to be confirmed when parts are chosen) [G2] | Component data and hydraulic calculation |
| R9 | Low energy use | 25 W or less while water flows; 0.5 W or less on standby | Met (22.6 W and 0.21 W) [E1, E2] | Power budget calculation |
| R10 | Keep the LEDs cool | LED board 50 °C or less with 30 °C cabinet air and 25 °C water, including the 5 s run-on; a board temperature sensor cuts LED current above 50 °C | Met (37.3 to 45.1 °C over the film-coefficient range) [F3] | Thermal calculation; cut-back reviewed as a firmware rule |
| R11 | Food-safe wetted parts | Every wetted material food-contact grade (316 stainless steel, PTFE, fused quartz, EPDM or silicone O-rings, acetal); no UV-C on any plastic other than PTFE | Met by design (316 lower cap; PTFE liner, top disc and 316 insert shield the acetal upper cap) | Material review of the model |
| R12 | Contain the UV-C light | No UV-C outside the unit in normal use; LEDs cannot run with the LED head or enclosure lid removed | Met by design: lid reed switch, and an interlock loop in the LED head's plug; the head's 95 mm cable is 39 mm too short for the head to clear the cap while still plugged in (model check; decided 2026-10-02, LMF-DEC-001) | Design review of interlock and light path |
| R13 | Electrical safety | Only 24 V DC at the unit; mains confined to a certified external adapter; fuse on the 24 V input | Met by design | Design review |
| R14 | Fit under a kitchen sink | Envelope 350 x 150 x 350 mm (13.8 x 5.9 x 13.8 in) or less, excluding the adapter | Met (277 x 100 x 322 mm) [H1] | Parametric model |
| R15 | Easy service | Window and LED head replaceable with hand tools in 15 min or less; status LED shows run, fault and service due | Not verifiable at TRL 3 (LED head unplugged, then off on four screws from below, and window out after six ring screws, with no plumbing disturbed; needs a build to time). Run, fault and service due are shown on the UV level bar, which replaced the single status light (2026-10-02) | Timed service on a build |
| R16 | Low cost and buildable | Value-engineering target of USD 340 per unit in parts (`budget_usd`, a hypothetical control target, not a limit; set from $200 by decision D2, then $225, then $340 by the top-up Amish approved on 2026-09-26); no custom PCB for the first build | Over the value-engineering target by USD 76 (estimated cost of the constructable design USD 416; the concept was $338.00) [I1] | Priced BOM |
| R17 | Pressure protection (installation) | A pressure-limiting valve upstream of the unit, set at 4 bar (58 psi) or less, so that transients stay within the 8 bar window rating (new, LMF-DDR-002) | Met (window 3.09 MPa at 4 bar, 6.18 MPa at a transient of twice the setting) [G5] | Plate stress calculation; installation instructions |
| R18 | Show UV level at a glance | A five-segment bar on the enclosure lid showing UV level relative to the alarm threshold, read from the wall sensor; labelled as UV level, not as a dose in units (new, decided by Amish on 2026-10-02, LMF-DEC-001) | Met by design: three of five segments lit at 90 %/cm with rated LEDs, the last segment going out where the alarm trips; in the model and BOM line 13 [C6] | Design review; later bench check against the wall sensor reading |

## Assumptions

- **Water quality.** The design water is clear, pre-filtered well water (decision D9): UVT of 90 %/cm or better at 275 nm, turbidity below 1 NTU, after a 5 µm sediment pre-filter. UVT must be measured for each site. Iron, manganese and hardness foul the window and must be within the limits commonly given for UV systems; this is an installation requirement, not a LumaFlow feature.
- **Dose target.** 40 mJ/cm² is the NSF/ANSI 55 Class A dose level. Reaching it would not make LumaFlow Class A compliant or certified. It inactivates bacteria and protozoa such as *Cryptosporidium* by several logs but gives a much smaller log reduction of adenovirus, which the US EPA dose tables show needs about 186 mJ/cm² for 4 logs ([EPA UV toolkit](https://www.epa.gov/system/files/documents/2022-05/uv-toolkit-815-B-21-007_0.pdf)). RED in LMF-CAL-001 is computed for a challenge organism of 20 mJ/cm² per log.
- **Liner reflectance.** R2 rests on a wetted reflectance of 0.95 for the high-reflectance PTFE liner, which must be measured; plain PTFE (0.80) would give 45.2 mJ/cm², still above 40 (LMF-CAL-001, B8).
- **Pressure.** The pressure-limiting valve (R17) is part of the installation, like the sediment pre-filter, and is not in the LumaFlow BOM.
- **Demand.** 10 to 20 L per household per day, drawn in about 20 short draws.
- R3 is kept as stated so that the gap stays visible. The R16 figure of $340 is a value-engineering target (Amish, 2026-10-01); the cost drivers and savings worth trying are in the design decisions register, LMF-DEC-001.
