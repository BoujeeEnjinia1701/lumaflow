---
doc_id: LMF-REQ-001
title: LumaFlow requirements
project: LumaFlow
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# LumaFlow requirements

These are first-pass requirements for the concept. Targets are proposals for review, awaiting Amish, and will be checked by calculation at TRL 3. The status column reports the TRL 2 estimates in LMF-PRC-001; "by design" means the concept includes the feature but nothing has been built or tested. Two requirements are **not met** by the current concept: R3 (dose at 70 % UV transmittance) and R16 (cost).

Table 1. Requirements and status at TRL 2.

| ID | Requirement | Target | Status (estimate) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Deliver a useful drinking-water flow | 2.0 L/min (0.5 gpm) at the faucet, capped by a flow restrictor | Met by design | Restrictor rating; flow calculation |
| R2 | Deliver the Class A dose level in clear water | Reduction equivalent dose (RED) of 40 mJ/cm² or more at 2.0 L/min and UV transmittance (UVT) of 90 %/cm | Met on estimate (about 40 mJ/cm²), no margin | Dose calculation; later biodosimetry |
| R3 | Deliver the Class A dose level at the NSF/ANSI 55 test water quality | RED of 40 mJ/cm² or more at 2.0 L/min and 70 %/cm UVT | **Not met** (about 14 mJ/cm²) | Dose calculation |
| R4 | Monitor the dose and fail safe | UV-C sensor reading through the water column; visual and audible alarm and outlet valve closed within 1 s when the estimated dose falls below 40 mJ/cm², the sensor fails or power is lost | Met by design | Design review; fault analysis |
| R5 | Switch with the flow | LEDs on within 0.5 s of flow above 0.3 L/min; LEDs held on for 5 s after flow stops; LEDs off otherwise | Met by design | Firmware sketch review; timing calculation |
| R6 | No mercury and no warm-up | No mercury in any part; full UV output within 0.1 s of switch-on | Met by design | Design review; LED datasheet |
| R7 | Withstand household water pressure | Working pressure 8 bar (116 psi); quartz window stress 7 MPa (1,000 psi) or less at 8 bar | Met on estimate (about 4.5 MPa with a 6 mm window) | Plate stress calculation |
| R8 | Low pressure drop | 0.5 bar (7 psi) or less across the unit at 2.0 L/min | Unverified | Component data and hydraulic calculation |
| R9 | Low energy use | 25 W or less while water flows; 0.5 W or less on standby | Met on estimate (about 21.6 W and 0.3 W) | Power budget calculation |
| R10 | Keep the LEDs cool | LED board 50 °C or less with 30 °C cabinet air and 25 °C water, including the 5 s run-on | Unverified | Thermal calculation |
| R11 | Food-safe wetted parts | Every wetted material food-contact grade (316 stainless steel, PTFE, fused quartz, EPDM or silicone O-rings, acetal); no UV-C on any plastic other than PTFE | Met by design | Material review |
| R12 | Contain the UV-C light | No UV-C outside the unit in normal use; LEDs cannot run with the LED head or enclosure lid removed | Met by design | Design review of interlock and light path |
| R13 | Electrical safety | Only 24 V DC at the unit; mains confined to a certified external adapter; fuse on the 24 V input | Met by design | Design review |
| R14 | Fit under a kitchen sink | Envelope 350 x 150 x 350 mm (13.8 x 5.9 x 13.8 in) or less, excluding the adapter | Met (massing model about 240 x 75 x 325 mm) | Massing model |
| R15 | Easy service | Window and LED head replaceable with hand tools in 15 min or less; status LED shows run, fault and service due | Met by design | Design review |
| R16 | Low cost and buildable | Parts cost $200 or less per unit; no custom PCB for the first build | **Not met** (about $217) | Priced BOM |

## Assumptions

- **Water quality.** The design water is clear, pre-filtered well or tap water: UVT of 90 %/cm or better at 275 nm, turbidity below 1 NTU, after a 5 µm sediment pre-filter. Many groundwaters and treated supplies reach this, but UVT must be measured for each site. Iron, manganese and hardness foul the window and must be within the limits commonly given for UV systems; this is an installation requirement, not a LumaFlow feature.
- **Dose target.** 40 mJ/cm² is the NSF/ANSI 55 Class A dose level. Reaching it does not make LumaFlow Class A compliant or certified. It inactivates bacteria and protozoa such as *Cryptosporidium* by several logs but gives a much smaller log reduction of adenovirus, which the US EPA dose tables show needs about 186 mJ/cm² for 4 logs ([EPA UV toolkit](https://www.epa.gov/system/files/documents/2022-05/uv-toolkit-815-B-21-007_0.pdf)).
- **Demand.** 10 to 20 L per household per day, drawn in about 20 short draws.
- All targets are proposals, awaiting Amish. R3 and R16 are kept as stated so that the gap stays visible; the options for closing them are in LMF-PRC-001 and `docs/REVIEW.md`.
