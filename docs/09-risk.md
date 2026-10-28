---
doc_id: LMF-RSK-001
title: LumaFlow risk register and hazard analysis
project: LumaFlow
doc_type: Risk register
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.8 upgrade: project risks, preliminary hazard analysis and first-pass design FMEA (P3) for option A, updated for the independent review of 2026-10-25"
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'P8 mitigation as decided by Amish (O-4 (a), 2026-10-25)'
---

# LumaFlow risk register and hazard analysis

The top risk is a false sense of safety: a calculated dose is not a demonstrated one, and a household could trust LumaFlow's water when the liner reflects less, the water is cloudier or the firmware rule is wrong. The controls are the normally closed valve that stops the water on a low sensor reading, conservative dose mapping, and plain statements everywhere that LumaFlow is a research and educational prototype, not a certified device. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be found) to 5 (unlikely to be found).

> **Safety:** LumaFlow emits UV-C, holds mains water pressure next to electronics and is meant to make water safer to drink. It is a research and educational prototype, not a certified water treatment device. Nothing in this document is a test result; every rating is a paper estimate.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Dose below target in the built reactor | Liner reflectance below 0.95, LED bin low, 275 nm response below 254 nm | PR-002 not met; more LEDs or less flow | 3 | 4 | Design lead | Margins stated (S3, S8, B9); measure reflectance and do biodosimetry at TRL 4 |
| P2 | No co-design partner | The extension programme is not approached or declines | Requirements stay unvalidated; no real UVT data | 3 | 3 | Project lead (Amish) | Draft first message exists (REVIEW 2026-10-02); second candidates in PLN |
| P3 | Cost stays over the value-engineering target | Machined 316 cap, specialist liner, LED prices | USD 433 against USD 340 | 4 | 2 | Design lead | Savings in DEC (plain PTFE, one machine-shop quote, LED quantity prices) |
| P4 | Concept choice changes the project | Option B scores level with A | Redesign of every document if B is chosen | 2 | 4 | Project lead (Amish) | Decision O-1 put to Amish with both options argued (LMF-DDR-004) |
| P7 | Dose margin thinner than the note's rule | 275 nm response factor and LED derating (S3, S33) | PR-002 at risk; 37.5 mJ/cm² worst case | 3 | 4 | Design lead | Decision O-3 after the LED is chosen |
| P8 | Reactor mixes more than assumed | Inlet jet and buoyancy (S34) | RED below the laminar value | 3 | 4 | Design lead | Tracer test at TRL 4 with the side inlet kept; perforated PTFE inlet ring ready (O-4 (a), decided by Amish 2026-10-25) |
| P5 | Firmware dose rule is wrong or slow | Mapping and 1 s fail-safe exist only on paper | Untreated water passes during a fault | 3 | 5 | Electronics lead | PR-004 at risk; firmware sketch review and bench test at TRL 4 |
| P6 | Misuse of the open design as a certified product | A builder sells or relies on copies | Harm and reputational risk | 2 | 5 | Project lead | PR-019 labels and documents; CERN-OHL-S licence; no certification claims |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | UV-C exposure of eyes or skin | LED head removed or lid opened while powered; light leak at a seal or port | Photokeratitis, skin erythema | 4 | 2 | Metal and PTFE light path; lid reed switch; interlock loop in the LED head plug on a cable too short to clear the cap (PR-012); warning labels; UV-C eyewear for bench work | Low |
| H2 | Under-treated water drunk | Cloudy water, fouled window, aged LEDs, sensor or firmware fault | Waterborne illness | 5 | 2 | Wall sensor with conservative proportional mapping; normally closed valve closes on low dose, fault or power loss (PR-004); pre-filter required; not a virus barrier (S5) | Medium (PR-004 at risk until tested) |
| H3 | False sense of safety | User trusts a research prototype | Illness from chemical or viral contamination UV does not treat | 5 | 3 | PR-019 labelling; README and PRC safety notes; no certification claims | Medium |
| H4 | Leak or burst under pressure | Window crack from a pressure spike; seal failure | Flooded cabinet; water on electronics | 3 | 2 | Window 6.18 MPa at 8 bar against 6.8 MPa; pressure limiter at 4 bar (PR-017); gasket seated at 2.4 MPa at 8 bar (S13); leak test before wiring | Low |
| H5 | Electric shock | Mains in a wet cabinet | Injury | 5 | 1 | Only 24 V DC at the unit; certified adapter on a GFCI or RCD outlet above the water level (PR-013) | Low |
| H6 | Hot surface or LED overheating | LEDs stuck on with no flow | Burn risk low; LED damage | 2 | 2 | Board sensor cuts current above 50 °C; stuck-on fault heads for 53 °C (CAL F6) | Low |
| H7 | Material leaching into water | Wrong grade of plastic or rubber, UV-aged polymer | Contaminants in drinking water | 3 | 2 | Food-contact grades (PR-011); expanded PTFE in the light path (D-S1); acetal exposure to verify (S10) | Low to medium |
| H8 | Bacterial regrowth after treatment | Water standing in the reactor and downstream tubing | Contaminated first draw | 3 | 3 | Idle LED pulse every 4 h; no residual disinfectant (stated); plate counts at TRL 4 (S7) | Medium |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | PTFE liner (line 2) | Reflect UV-C back into the water | Reflectance lower than 0.95 when wetted | Dose falls (45.2 mJ/cm² at 0.80) | Grade, surface fouling | 4 | 3 | 3 | 36 | Supplier data and a measurement at TRL 4; the sensor sees a fouled liner as low signal |
| F2 | UV-C LEDs (line 4) | Emit 60 mW each at 275 nm | Output low or aging | Dose falls | Bin, junction temperature, hours | 4 | 3 | 2 | 24 | Proportional mapping blames every loss on the LEDs (CAL C5); service-due segment on the bar |
| F3 | Quartz window (line 3) | Pass UV-C, hold pressure | Crack | Leak into the LED head; loss of treatment | Pressure spike, uneven clamping | 4 | 2 | 2 | 16 | Pressure limiter (PR-017); ring screws in anti-seize at 0.21 N·m (D-S2); fuse and leak logic |
| F4 | Window gasket (line 17) | Seal the window to the cap | Leak | Water in the LED head | Under-seated gasket, PTFE creep | 3 | 2 | 3 | 18 | Expanded PTFE seated at 1.8 MPa or more at 8 bar (S13); re-torque check 24 h after the first fill (build plan first checks) |
| F5 | Wall photodiode (line 9) | Measure UV-C in the water | Reads high (stuck or saturated) | Low dose not caught | Electronics fault, stray light | 5 | 2 | 4 | 40 | Sensor-fail detection in firmware (PR-004); light-tight holder; reading checked on the idle pulse |
| F6 | Flow sensor (line 8) | Confirm flow after start-up | No pulses at low flow | Valve shut as a fault, or water passes unmetered | Sensor below its range, fouled rotor | 4 | 2 | 3 | 24 | LEDs come on before the valve opens (D-S3); no pulse in 0.5 s shuts the valve; the dose estimate uses the measured flow |
| F11 | Outlet pressure sensor (line 20) | Start the unit when the faucet opens | Stuck or drifting | Unit does not start (fails safe), or starts without demand | Sensor fault, air in the tee | 2 | 2 | 2 | 8 | Start-up check in the build plan; controller watches for a reading out of range |
| F7 | Solenoid valve (line 11) | Stop water on alarm or power loss | Sticks open | Untreated water on a fault | Debris, wear | 5 | 2 | 4 | 40 | Pre-filter; graft from option B (O-2): leak and stuck-valve check with the valve shut on each idle pulse |
| F8 | LED head interlock (line 10) | Stop the LEDs with the head off | Loop shorted or bypassed | UV-C exposure during service | Wiring fault, tampering | 4 | 1 | 3 | 12 | Cable too short for the head to clear the cap while plugged in (model check); warning labels |
| F9 | Acetal upper cap (line 7) | Hold the outlet and the tube end | Ages under UV-C passing through the PTFE | Cracking, leaching | PTFE transmittance at 275 nm | 3 | 2 | 4 | 24 | Measure at TRL 4 (S10); fallback 316 foil cup in the liner pocket |
| F10 | Retaining ring screws (line 16) | Clamp the window stack | Over-torqued | Ring yields, washer creeps, window loads unevenly | 0.5 N·m dry in the earlier plan; scatter of the dry nut factor | 3 | 2 | 3 | 18 | Anti-seize and 0.21 N·m with a torque screwdriver, ring in 316 (D-S2) |
