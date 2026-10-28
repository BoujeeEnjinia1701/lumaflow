---
doc_id: LMF-FEA-001
title: LumaFlow feasibility assessment
project: LumaFlow
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.8 upgrade: feasibility of the TRL 3 design (option A), closed on paper"
---

# LumaFlow feasibility assessment

Option A is feasible on paper as a garage-built prototype: the science holds (LMF-STM-001, after four detail fixes, two of them found by the independent review), the dose clears 40 mJ/cm² in clear water with an 18 % margin once the 275 nm response factor is applied (below the 20 % the calculation note asks for, so PR-002 is at risk), every part can be made or bought (LMF-BLD-001), and the open questions are measurements for TRL 4, not unknowns that could sink the concept. The weakest points are the liner's wetted reflectance, LED derating (a worst-case stack gives 37.5 mJ/cm²), how well the reactor mixes, the dose rule in firmware, and cost (USD 93 over the value-engineering target). Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Axial reactor with a reflective PTFE-lined bore meets the clear-water dose on paper (RED 50.9 to 74.9 mJ/cm², 47.3 with the 275 nm factor); misses the 70 %/cm test water by design (PR-003, decision D1) | Medium | Dose rests on a liner reflectance of 0.95 (0.80 gives 42.1 with the 275 nm factor), LED derating (S33) and the residence-time distribution (S34), none yet measured | STM S2, S3, S8, S33, S34; CAL B5, B8, B10, B11 |
| Materials | 316, PTFE and expanded PTFE, fused silica, EPDM O-rings out of the light, acetal behind PTFE; food-contact grades exist for each | Medium | UV-C through 3 mm of PTFE onto the acetal cap is unmeasured (STM S10); fallback a 316 foil cup | STM S9, S10, S31; REG G2, G4 |
| Manufacturing and assembly | Two machined caps, a TIG-welded boss and a turned holder at a machine shop; the rest is sawing, drilling, tapping and 3D printing; every joint checked in the model (806 contact, clearance and overlap checks pass) and at D3 by `cad_check.py` | High | Ring screws in anti-seize at 0.21 N·m (D-S2); PTFE liner from a specialist supplier | BLD-001; `cad/fidelity.json`; DEC D-S2 |
| Power and controls | 22.6 W flowing, 0.23 W standby; an outlet pressure sensor starts the unit when the faucet opens (D-S3), the flow sensor confirms flow; wall photodiode 13.4 nA at 90 %/cm, 11.4 nA at the alarm point, which one failed LED also trips (D-S4) | Medium | The proportional dose rule and the 1 s fail-safe exist only on paper (PR-004 at risk); firmware sketch and a bench test needed at TRL 4 | CAL C1 to C5, D2, D5, E1, E2; STM S23 to S26, S37, S38 |
| Supply of parts | Catalogue LEDs, quartz windows, sensors, valves and fittings; one specialist item (high-reflectance PTFE tube) | Medium | LED output bin and price at quantity; flow coefficients of the sensor and valve; liner reflectance data from the supplier | BOM; DEC To confirm 2, 4, 7 |
| Cost | USD 433 against a USD 340 value-engineering target | Medium | Drivers: LEDs, 316 cap, liner, tube, window; savings listed in DEC | CAL I1; DEC Value engineering |

Ratings: High, Medium, Low.
