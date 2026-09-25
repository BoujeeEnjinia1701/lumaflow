---
doc_id: LMF-REQ-001
title: LumaFlow requirements
project: LumaFlow
doc_type: Requirements
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions (LMF-DDR-001); R16 redefined to $225; R7 design stress sourced (6.8 MPa); status from LMF-CAL-001
---

# LumaFlow requirements

These are the requirements for the concept, checked by calculation at TRL 3 in LMF-CAL-001. The status column reports that note; bracketed tags such as [B5] point to the line of `docs/04-calcs/sizing.py` that carries the number. Three requirements are **not met**: R2 and R3 (dose) and R16 (cost). Four are at risk: R4, R5, R8 and R10. The targets were set as proposals at TRL 2; the dose targets (R2, R3) and the budget (R16) now follow Amish's decisions of 2026-09-25 in LMF-DDR-001.

Table 1. Requirements and status at TRL 3.

| ID | Requirement | Target | Status (LMF-CAL-001) | Verification |
| --- | --- | --- | --- | --- |
| R1 | Deliver a useful drinking-water flow | 2.0 L/min (0.5 gpm) at the faucet, capped by a flow restrictor | Met by design [A3] | Restrictor rating; flow calculation |
| R2 | Deliver the Class A dose level in clear water | Reduction equivalent dose (RED) of 40 mJ/cm² or more at 2.0 L/min and UV transmittance (UVT) of 90 %/cm | **Not met** (14.7 laminar to 19.0 plug mJ/cm²) [B5] | Ray-trace dose calculation; later biodosimetry |
| R3 | Deliver the Class A dose level at the NSF/ANSI 55 test water quality | RED of 40 mJ/cm² or more at 2.0 L/min and 70 %/cm UVT | **Not met** (6.3 to 7.4 mJ/cm²) [B6]; kept visibly not met by decision D1 | Dose calculation |
| R4 | Monitor the dose and fail safe | UV-C sensor reading through the water column; visual and audible alarm and outlet valve closed within 1 s when the estimated dose falls below 40 mJ/cm², the sensor fails or power is lost | At risk: the far-end signal is about 2.4 nA at 90 %/cm and unresolved at 70 %/cm, and while R2 is not met the alarm would trip in any water [C1, C3] | Signal calculation; later firmware and test |
| R5 | Switch with the flow | LEDs on within 0.5 s of flow above 0.3 L/min; LEDs held on for 5 s after flow stops; LEDs off otherwise | At risk (0.46 s worst case) [D2] | Timing calculation; later firmware sketch review |
| R6 | No mercury and no warm-up | No mercury in any part; full UV output within 0.1 s of switch-on | Met by design | Design review; LED datasheet |
| R7 | Withstand household water pressure | Working pressure 8 bar (116 psi); quartz window stress 6.8 MPa (1,000 psi) or less at 8 bar | Met (4.46 MPa with a 6 mm window) [G4] | Plate stress calculation |
| R8 | Low pressure drop | 0.5 bar (7 psi) or less across the unit at 2.0 L/min | At risk (0.42 bar on assumed flow coefficients, calculated without the flow restrictor, which absorbs excess supply pressure by design; clarifying the wording is proposed, awaiting Amish) [G2] | Component data and hydraulic calculation |
| R9 | Low energy use | 25 W or less while water flows; 0.5 W or less on standby | Met (22.6 W and 0.21 W) [E1, E2] | Power budget calculation |
| R10 | Keep the LEDs cool | LED board 50 °C or less with 30 °C cabinet air and 25 °C water, including the 5 s run-on | At risk (48.9 °C nominal, 44.1 to 55.9 °C over the film-coefficient range) [F3] | Thermal calculation |
| R11 | Food-safe wetted parts | Every wetted material food-contact grade (316 stainless steel, PTFE, fused quartz, EPDM or silicone O-rings, acetal); no UV-C on any plastic other than PTFE | Met by design (316 lower cap; PTFE liner, top disc and 316 insert shield the acetal upper cap) | Material review of the model |
| R12 | Contain the UV-C light | No UV-C outside the unit in normal use; LEDs cannot run with the LED head or enclosure lid removed | Met by design | Design review of interlock and light path |
| R13 | Electrical safety | Only 24 V DC at the unit; mains confined to a certified external adapter; fuse on the 24 V input | Met by design | Design review |
| R14 | Fit under a kitchen sink | Envelope 350 x 150 x 350 mm (13.8 x 5.9 x 13.8 in) or less, excluding the adapter | Met (235 x 72 x 322 mm) [H1] | Parametric model |
| R15 | Easy service | Window and LED head replaceable with hand tools in 15 min or less; status LED shows run, fault and service due | Not verifiable at TRL 3 (four tie rods and two push-fit ports; needs a build to time) | Timed service on a build |
| R16 | Low cost and buildable | Parts cost $225 or less per unit (redefined from $200 by decision D2); no custom PCB for the first build | **Not met** ($249.00) [I1] | Priced BOM |

## Assumptions

- **Water quality.** The design water is clear, pre-filtered well water (decision D9): UVT of 90 %/cm or better at 275 nm, turbidity below 1 NTU, after a 5 µm sediment pre-filter. UVT must be measured for each site. Iron, manganese and hardness foul the window and must be within the limits commonly given for UV systems; this is an installation requirement, not a LumaFlow feature.
- **Dose target.** 40 mJ/cm² is the NSF/ANSI 55 Class A dose level. Reaching it would not make LumaFlow Class A compliant or certified. It inactivates bacteria and protozoa such as *Cryptosporidium* by several logs but gives a much smaller log reduction of adenovirus, which the US EPA dose tables show needs about 186 mJ/cm² for 4 logs ([EPA UV toolkit](https://www.epa.gov/system/files/documents/2022-05/uv-toolkit-815-B-21-007_0.pdf)). RED in LMF-CAL-001 is computed for a challenge organism of 20 mJ/cm² per log.
- **Pressure.** A pressure-limiting valve upstream is an installation requirement where supply can exceed 6 bar or water hammer occurs (LMF-CAL-001, G5).
- **Demand.** 10 to 20 L per household per day, drawn in about 20 short draws.
- R2, R3 and R16 are kept as stated so that the gaps stay visible. The routes to close R2 and R16 are proposals awaiting Amish in `docs/REVIEW.md`.
