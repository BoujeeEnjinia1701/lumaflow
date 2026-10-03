---
doc_id: LMF-CAL-001
title: LumaFlow sizing calculations
project: LumaFlow
doc_type: Calculation
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (flow, Monte Carlo optics and dose, dose monitor, switching, power, thermal, pressure drop, window and structure, size, cost, options)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); rerun for the 50 mm bore, 0.95 liner, 1.2 L/min, wall dose sensor, 15 Hz per L/min flow sensor, 10 mm window, M5 rods, pressure limiter and thermal cut-back
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish; rerun with budget_usd $340, R16 now met
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Rerun for the constructable design (LMF-DDR-003); new G8 for the upper cap roof; cost reported against the value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Requirement table: R12 interlock wording and R18 added after the 2026-10-02 decisions (LMF-DEC-001); no figure changed. The window seat washer (A2, option b) is not yet re-run in section B"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Approved follow-ups carried out: section B and the window stress re-run for the 0.5 mm PTFE window washer (LED gap 1.3 mm); new C6 for the UV level bar (R18, now met); idle LED pulse in E4, E6 and F7; mass H2; cost with the washer, interlock plug, bar and labels (USD 416)"
---

# LumaFlow sizing calculations

This note checks the LumaFlow design as revised by LMF-DDR-002 and made constructable by LMF-DDR-003: a 50 mm bore lined with high-reflectance PTFE, a design flow of 1.2 L/min (0.32 gpm), a UV-C photodiode in the tube wall at mid height, a flow sensor of 15 Hz per L/min, an upstream pressure limiter and a thermal cut-back. On paper, LumaFlow meets fourteen of its eighteen requirements, has one at risk (R4) and misses one (R3); one cannot be verified at TRL 3, and the cost (R16) is over its value-engineering target. The reduction equivalent dose (RED) in clear water (90 %/cm UV transmittance, UVT) is 50.9 (laminar) to 74.9 (plug) mJ/cm², so **R2 is met** with the 20 % margin this note requires; in v0.1, with a 25 mm bore at 2.0 L/min, it was 14.7 to 19.0 mJ/cm². The dose at the 70 %/cm test condition is 17.0 to 21.3 mJ/cm² (**R3 not met**, kept visible by decision D1). Value-engineering target: USD 340. Estimated cost of the constructable design: USD 416 (USD 76 over the target) [I1]. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B5], is the line of that script's output that carries it.

> **Safety:** These calculations concern a device meant to disinfect drinking water with UV-C light under mains pressure. They are first-principles estimates for a paper proof of concept, not a substitute for biodosimetry, datasheets or a review by a qualified engineer. A calculated dose above target is not a demonstrated dose. LumaFlow is a research and educational prototype, not a certified water treatment device. See LMF-PRC-001, Safety.

## Scope and method

The note checks every requirement in LMF-REQ-001 v0.8 against the design in LMF-PRC-001 v0.8 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `levels()` and part volumes, so the dimensions used here are the ones in the STEP files and in drawing LMF-DWG-001 Rev P5. It reads prices from `bom/bom.csv` and the value-engineering target (`budget_usd`) from `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py` (about 20 s; it runs the ray trace eight times).

Status rule for the dose: the laminar-flow RED is the design value, because the laminar profile is the more pessimistic of the two limits and the real profile lies between them [A5]. **Met** needs the laminar RED to clear the target by 20 %.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Flow | 1.2 L/min (0.32 gpm), set by the restrictor; water at 20 °C for hydraulics, 25 °C for the thermal case | LMF-REQ-001 v0.4, R1 |
| LEDs | Six 275 nm LEDs on a 32 mm circle, 60 mW UV-C each at 350 mA and 6.2 V (0.36 W, 13.02 W electrical); Lambertian emission | Typical 3535-class UV-C LED ratings; bin to be confirmed |
| Window | UV-grade fused silica, 57 x 10 mm on a 51 mm seat, n = 1.496 at 275 nm, bulk transmittance 0.995; air gap 1.3 mm (the window sits on a 0.5 mm PTFE washer on the retaining ring); unpolarized Fresnel losses at both faces; light outside the seat aperture or the 50 mm bore is lost | Standard optics |
| Water | n = 1.372; base-e absorption α = −ln(UVT) per cm (0.105/cm at 90 %/cm, 0.357/cm at 70 %/cm); no scattering | UVT definition |
| Walls | Diffuse (Lambertian) reflection. Wetted high-reflectance PTFE liner 0.95 (sensitivity 0.80 and 0.90); wetted 316 stainless in the lower cap bore 0.30; window and LED side seen from the water 0.10 | Engineering judgment for a sintered or expanded high-reflectance PTFE; to be measured |
| Ray trace | 600,000 rays per case, 20 equal-area annuli by 60 axial bins; fluence rate = absorbed power / (α x bin volume); the wall sensor window is an 8 x 8 mm absorbing patch at mid height | Collision estimator |
| Flow profile | Two limits: plug flow and fully developed laminar (parabolic) flow | Entrance length [A5] |
| Dose response | First-order inactivation of a challenge organism with 20 mJ/cm² per log (MS2-like), with the same response at 275 nm as at 254 nm | Assumption; the wavelength response must be checked |
| Photodiode | SiC, 0.13 A/W at 275 nm, 0.06 mm² active area, behind an 8 mm quartz window of 0.92 transmittance in the tube wall | Typical TO-46 SiC photodiode |
| Flow sensor | Hall-effect turbine, 15 Hz per L/min; Kv 0.35 m³/h | Pulse rate set by LMF-DDR-002; Kv to confirm |
| Valve | 24 V DC normally closed, 4.8 W (0.2 A) held open, Kv 0.25 m³/h | Typical small direct-acting solenoid |
| Electronics | Driver 90 %; controller 0.6 W active; adapter 88 % at load, 70 % at light load, 0.1 W no-load | US DOE Level VI no-load class for small adapters |
| Use | 15 L/day in 20 draws, 5 s run-on per draw | LMF-REQ-001 |
| Thermal | Sink natural convection 5 W/(m²·K) (fins hanging down) plus radiation, ε = 0.85; 0.5 mm pads of 3 W/(m·K); 316 at 16 W/(m·K); water film 300 W/(m²·K) in the lower cap (range 150 to 600); 10 K/W junction to board per LED | Engineering judgment; film coefficient is the main uncertainty |
| Structure | Fused quartz design tensile stress 6.8 MPa (1,000 psi) ([Momentive, mechanical properties](https://www.momentivetech.com/materials/fused-quartz-materials/quartz-properties/mechanical-properties)); Poisson ratio 0.17; simply supported edge; 8 bar working pressure; pressure limiter set at 4 bar | Roark circular plate, uniform load |

## A. Flow and hydraulics (R1)

The irradiated channel is 50 mm across and 242 mm long, from the window to the PTFE top disc; the flow path from inlet to outlet is 226 mm [A1]. The channel holds 474 mL, 444 mL of it between the ports [A2]. At 1.2 L/min the mean velocity is 1.02 cm/s and the mean residence time 22.2 s [A3]. The Reynolds number is 507 at 20 °C and 334 at 5 °C, so the flow is laminar [A4]. The laminar entrance length, about 1.3 m, is far longer than the flow path [A5], so the velocity profile lies between plug flow and a parabola; both limits are carried through section B. R1 is met by the 1.2 L/min restrictor, and the flow sensor range of 0.3 to 6 L/min covers it.

## B. Optics and UV-C dose (R2, R3)

The six LEDs give 0.36 W of UV-C from 13.02 W electrical, a UV-C efficiency of 2.8 % [B1]. Of that, 84.8 % enters the water [B2]; it was 87.0 % with the 0.8 mm gap of v0.5, because the LEDs now sit 0.5 mm lower and a little more of their light misses the 51 mm open span. In the 50 mm bore light crosses twice as much water between wall reflections as in the old 25 mm bore, and the liner returns 95 % of what reaches it. At 90 %/cm the water absorbs 52.9 % of the LED output and the walls 25.9 % (v0.1: 26.1 % and 49.8 %); at 70 %/cm the water absorbs 66.5 % [B3, B4].

*Table 2. Dose at 1.2 L/min (mJ/cm²). Average is the flow-weighted average dose; RED is for the 20 mJ/cm² per log organism.*

| UVT (%/cm) | Average dose | RED, plug flow | RED, laminar flow | Reactor efficiency, laminar |
| --- | --- | --- | --- | --- |
| 95 | 131.9 | 131.4 | 82.7 | 0.63 |
| 90 | 75.4 | 74.9 | 50.9 | 0.67 |
| 85 | 50.8 | 50.5 | 35.9 | 0.71 |
| 80 | 36.8 | 36.5 | 27.2 | 0.74 |
| 75 | 27.8 | 27.5 | 21.3 | 0.77 |
| 70 | 21.5 | 21.3 | 17.0 | 0.79 |

At the design water quality of 90 %/cm the RED is 50.9 (laminar) to 74.9 (plug) mJ/cm² [B5]. **R2 (40 mJ/cm²) is met**, with the laminar value 27 % above the target (30 % with the 0.8 mm gap of v0.5). At 70 %/cm it is 17.0 to 21.3 mJ/cm² [B6], so **R3 is not met**, as decision D1 accepted; it is now above the Class B level of 16 mJ/cm².

The reactor efficiency (RED over average dose) is 0.67, lower than the 0.77 of v0.1: the slow laminar core on a wide bore sees less light than the water beside the wall. Streamline doses at 90 %/cm range from 41 mJ/cm² on the axis to 79 at mid radius and 1,433 beside the wall [B7]. The liner reflectance is the main optical uncertainty: 45.2, 48.7 and 50.9 mJ/cm² at 0.80 (plain PTFE), 0.90 and 0.95 [B8], so even plain PTFE meets 40 mJ/cm² but not the 20 % margin. LEDs 20 % below rating (bin, aging or temperature) give 40.7 mJ/cm² [B9].

## C. Dose monitor (R4)

The photodiode now sits behind an 8 mm quartz window in the tube wall at mid height (Z = 166 mm), facing the enclosure. It sees 0.19 mW/cm² and gives about 13.4 nA at 90 %/cm, 2.4 nA at 80 %/cm and 0.19 nA at 70 %/cm [C1], a signal across the whole range; the top-disc position of v0.1 gave 2.4 nA at 90 %/cm and nothing resolvable at 70 %/cm. Between 90 and 85 %/cm the wall signal falls 2.6 times as fast, in log terms, as the RED [C2] (4.4 times for the old position).

*Table 3. Wall sensor signal against UVT.*

| UVT (%/cm) | Irradiance (mW/cm²) | Photocurrent (nA) | Signal relative to 90 % | RED relative to 90 % |
| --- | --- | --- | --- | --- |
| 95 | 0.752 | 54.0 | 4.02 | 1.63 |
| 90 | 0.187 | 13.4 | 1.00 | 1.00 |
| 85 | 0.077 | 5.5 | 0.41 | 0.71 |
| 80 | 0.033 | 2.4 | 0.18 | 0.54 |
| 75 | 0.013 | 0.96 | 0.072 | 0.42 |
| 70 | 0.003 | 0.19 | 0.014 | 0.34 |

The controller keeps the proportional mapping RED_est = RED_ref x (S/S_ref) x (Q_ref/Q), which blames every loss of signal on the LEDs and so always under-reads. With RED_ref = 50.9 mJ/cm² the alarm threshold is S/S_ref = 0.79 [C3]. With LEDs at rated output the alarm trips below about 88.7 %/cm UVT, and LEDs aged to 79 % of output trip it in 90 %/cm water, where the true RED is 40.0 mJ/cm² [C4]. A mapping that blamed the water instead would be unsafe: with LEDs at 70 % output in 90 %/cm water it would claim 44.9 mJ/cm² when the true RED is 35.6 [C5]. R4 stays **at risk** because the sub-nanoampere signal in poor water, the mapping and the 1 s fail-safe still need firmware and a test, which are TRL 4 work. The wall-sensor signals in poor water come from few rays in the trace, so the sub-nanoampere figures move between runs (0.38 nA at 70 %/cm in v0.5, 0.19 nA now); the trend, not the last digit, is the result.

The five-segment UV level bar on the enclosure lid (R18) shows the same wall signal relative to the alarm threshold, not a dose. Its segments light at 1.0, 1.1, 1.2, 1.3 and 1.5 times the alarm signal. With rated LEDs it shows three of five segments in 90 %/cm water (1.27 times the alarm signal) and all five above about 90.6 %/cm; the last segment goes out at 88.7 %/cm, exactly where the alarm trips. In 90 %/cm water the segments go out one by one as the LEDs age to 118, 102, 94, 87 and 79 % of their rated output [C6]. **R18 is met** by design; the bench check against the wall sensor reading is TRL 4 work.

## D. Flow switching and run-on (R5)

At the 0.3 L/min switch-on threshold the 15 Hz per L/min sensor gives 4.5 Hz, one pulse every 0.22 s [D1]. With the LED rise time the worst-case switch-on is 0.24 s against 0.5 s [D2] (v0.1: 0.46 s with a 7.5 Hz per L/min sensor): **R5 is met**.

During the 5 s run-on the water held in the channel receives a volume-average 19 mJ/cm² at 90 %/cm [D4]. Taking the dose each parcel collected while flowing plus the run-on, every parcel in the flow path has at least 61 mJ/cm² when flow stops (plug flow) [D3].

## E. Power and energy (R9)

The LEDs draw 13.02 W; with the driver, the 4.8 W valve and the controller the 24 V bus carries 19.87 W, and the mains draw is 22.6 W while water flows [E1]. Standby is 0.21 W, dominated by the adapter's no-load draw and the powered flow sensor [E2]. **R9 is met** (25 W and 0.5 W).

At 15 L/day and 1.2 L/min the LEDs run 14.2 min/day (86 h/year); the unit uses 10.4 Wh/day or 3.8 kWh/year [E3]. The idle pulse decided on 2026-10-02 runs the LEDs for about 10 s every 4 h of idle with the valve shut: 59 s a day, 6.0 h a year of LED time, 17.1 W while it runs and 0.28 Wh a day, so the unit uses 3.9 kWh a year in all [E6]. With the pulses the LEDs run 92 h a year, and 10,000 h of LED on-time would take 108 years (116 years without them) [E4], so LED life is still set by aging in storage and by switching, not by on-time. For comparison, tap-scale mercury units drawing 13 to 22 W all day ([VIQUA VT1, VT4 and S2Q-PA spec sheet](https://viqua.com/wp-content/uploads/LIT520326_SpecSheet.pdf)) use 114 to 193 kWh/year [E5].

## F. Thermal (R10)

The LEDs turn 12.66 W into heat. The larger 90 x 90 mm finned sink rejects it to cabinet air through 2.46 K/W; the sink, spreader ring, lower cap and board store 780 J/K [F1]. The water path through the spreader ring and the 316 stainless lower cap is 1.58 K/W and carries 8.9 W of the 12.7 W into the water, which warms by 0.11 K [F2].

With continuous flow the LED board settles at 45.1, 40.5 or 37.3 °C for water-film coefficients of 150, 300 or 600 W/(m²·K) [F3], below 50 °C in every case; the LED junctions sit near 62 °C [F4]. The board temperature sensor and the cut-back of LED current above 50 °C (decision in LMF-DDR-002) are a backstop for the uncertain film coefficient: **R10 is met**. An acetal lower cap, with no water path, would settle at 63 °C and pass 50 °C after 30.5 min of flow [F5], which supports the 316 lower cap (LMF-DDR-002 confirms it). If the LEDs stuck on with no flow, the board would head for 53 °C, where the cut-back would act; the 5 s run-on adds only 0.08 K [F6]. A 10 s idle pulse in still water warms the LED head by 0.16 K [F7].

## G. Pressure drop, window and structure (R7, R8, R17)

*Table 4. Pressure drop at 1.2 L/min, excluding the flow restrictor [G1, G2].*

| Element | Drop (bar) |
| --- | --- |
| Flow sensor (Kv 0.35) | 0.04 |
| Solenoid valve (Kv 0.25) | 0.08 |
| 1 m of 1/4 in bore tube | 0.012 |
| Fittings (K = 6 in all) | 0.012 |
| Reactor ports | 0.002 |
| Reactor channel | below 0.00001 |
| **Total** | **0.15 (2.2 psi)** |

R8 is now worded to exclude the flow restrictor, which absorbs excess supply pressure by design. The unit drops 0.15 bar against 0.5 bar [G2]; with a Kv 0.5 sensor and a Kv 0.4 valve it would be 0.08 bar, and at the minimum supply of 2 bar, 1.85 bar remains for the restrictor and faucet [G3]. The margin covers the assumed flow coefficients, so **R8 is met**; the coefficients are still to be confirmed from the datasheets of the parts chosen.

The 57 x 10 mm window on its 51 mm seat carries a peak stress of 6.18 MPa at 8 bar, inside the 6.8 MPa design stress [G4]: **R7 is met**, with a 9 % margin (v0.1: 4.46 MPa on a 26 mm seat). Re-run for the PTFE washer under the window: the washer's 51 mm bore matches the retaining ring, so the open span and the stress are unchanged; a compliant washer makes the simply supported edge of the calculation a closer match to the real seat than metal on glass was. Unprotected, a 16 bar water-hammer spike would raise it to 12.4 MPa. With the pressure limiter set at 4 bar the window carries 3.09 MPa static, and a transient doubling to 8 bar gives 6.18 MPa [G5]: **R17 is met** as an installation requirement. The 8 mm sensor window sees 1.69 MPa and the tube hoop stress is 8.3 MPa [G6]. Each cap carries an end load of 2,655 N; four M5 316 studs, threaded 12 mm into the stainless lower cap, take 664 N each, 47 MPa in the thread [G7]. The acetal upper cap closes the channel above the PTFE top disc; its roof over the 56.2 mm liner pocket is 13 mm thick and carries 2.8 MPa at 8 bar with a clamped edge, against a long-term design stress of 10 MPa taken for acetal [G8]. The 3 mm roof of the concept model would have carried about 59 MPa, near the short-term strength of acetal, which is why LMF-DDR-003 made the cap 40 mm tall.

## H. Size and I. Cost (R14, R16)

The unit is 277 x 100 x 322 mm without the adapter, inside the 350 x 150 x 350 mm envelope [H1]: **R14 is met**. It weighs about 5.0 kg dry and 5.4 kg full of water; the aluminium bracket plate (1.05 kg), the stainless tube (0.98 kg) and the stainless lower cap (0.94 kg) are the heaviest parts, and the adapter adds about 0.2 kg on the floor [H2]. Made parts are weighed from the model's volumes; bought parts at typical catalogue masses.

Value-engineering target: USD 340 (`budget_usd`, a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 416 (USD 76 over the target), from the 19-line BOM [I1]. The largest lines are the LEDs ($54), the machined 316 lower cap ($48) and the high-reflectance PTFE liner ($45) [I2]. The concept BOM was $338.00; making the design buildable (LMF-DDR-003) added the welded sensor boss, the window retaining ring and seals, the threaded ports with stem adaptors, the drilled bracket plate and saddles, the pipe clamps and more fixings (USD 402 in v0.5). The decisions of 2026-10-02 add USD 14: the PTFE window washer (USD 2), the LED head plug, socket and interlock-loop cable (USD 4), the five-segment UV level bar (USD 3) and the labels line (USD 5). R16 is reported against the target, not as a failure; savings worth trying are listed in the design decisions register (LMF-DEC-001).

## J. Flow limits and options

*Table 5. Flow limits for this reactor and the options against R3.*

| Case | Result |
| --- | --- |
| Six LEDs, 90 %/cm | 40 mJ/cm² (laminar) up to 1.56 L/min; 48 mJ/cm² (Met with margin) up to 1.26 L/min [J1] |
| Same reactor at the former 2.0 L/min | 32.1 (laminar) to 45.0 (plug) mJ/cm² [J2] |
| Option B (R3 at 70 %/cm) | 15 LEDs, 33 W of LED power [J3]; R9 would fail |
| Option C (R3 at 70 %/cm) | Six LEDs meet 40 mJ/cm² below 0.46 L/min [J4]; proportional valve, later upgrade under D1 |

The 1.2 L/min design flow sits inside the 1.26 L/min limit for the 20 % margin; the 0.5 mm washer took 0.04 L/min off that limit. Filling a 1 L bottle takes about 50 s.

## K. Requirement status

*Table 6. Requirement status at TRL 3 (LMF-REQ-001 v0.8). Not met items first.*

| ID | Target | Value (tag) | Status |
| --- | --- | --- | --- |
| R3 | RED 40 mJ/cm² or more at 1.2 L/min, 70 %/cm | 17.0 to 21.3 mJ/cm² [B6] | **Not met** (accepted by D1) |
| R16 | Value-engineering target USD 340; no custom PCB | $416.00 [I1]; module-based electronics | Over the target by USD 76 |
| R4 | Dose monitor; alarm and valve closed within 1 s | Wall signal 13.4 nA at 90 %/cm, 0.19 nA at 70 %/cm; alarm below about 89 %/cm [C1, C4] | At risk |
| R15 | Window and LED head replaced in 15 min | LED head off on four screws from below, window out after six ring screws, no plumbing disturbed; needs a build to time | Not verifiable at TRL 3 |
| R1 | 1.2 L/min, restrictor | Restrictor; sensor range covers it [A3] | Met |
| R2 | RED 40 mJ/cm² or more at 1.2 L/min, 90 %/cm | 50.9 (laminar) to 74.9 (plug) mJ/cm² [B5] | Met |
| R5 | LEDs on within 0.5 s above 0.3 L/min; 5 s run-on | 0.24 s worst case [D2] | Met |
| R6 | No mercury; full output in 0.1 s | LEDs, microsecond rise | Met |
| R7 | Window 6.8 MPa or less at 8 bar | 6.18 MPa [G4] | Met |
| R8 | 0.5 bar or less at 1.2 L/min, excluding the restrictor | 0.15 bar, on assumed Kv [G2] | Met |
| R9 | 25 W flowing, 0.5 W standby | 22.6 W, 0.21 W [E1, E2] | Met |
| R10 | LED board 50 °C or less; cut-back above 50 °C | 37.3 to 45.1 °C steady [F3] | Met |
| R11 | Food-contact wetted parts; no UV-C on plastics but PTFE | 316 lower cap; PTFE liner, top disc and 316 outlet sleeve shield the acetal upper cap; EPDM gasket and O-rings | Met |
| R12 | No UV-C outside the unit; interlocks | Metal and PTFE light path; sensor window sealed in the welded boss by the photodiode holder; interlocks: the lid reed switch, and an interlock loop in the LED head's plug, whose 95 mm cable is 39 mm short of letting the head clear the cap while plugged in (model check) | Met |
| R13 | 24 V DC only at the unit | Certified adapter and input fuse | Met |
| R14 | 350 x 150 x 350 mm or less | 277 x 100 x 322 mm [H1] | Met |
| R17 | Pressure limiter at 4 bar or less upstream | Window 6.18 MPa at twice the setting [G5] | Met |
| R18 | Five-segment UV level bar, UV level relative to the alarm threshold | Three of five segments at 90 %/cm; last segment goes out where the alarm trips [C6]; bar in the model and BOM line 13 | Met |

Counts: 14 met, 1 not met, 1 at risk, 1 not verifiable at TRL 3, and R16 over its value-engineering target by USD 76 [K1].

## Numbers changed from v0.1

*Table 7. v0.1 (25 mm bore, 2.0 L/min) against v0.2 (LMF-DDR-002 design).*

| Quantity | v0.1 | v0.2 |
| --- | --- | --- |
| Bore, channel, window | 25 mm, 246 mm, 32 x 6 mm | 50 mm, 242 mm, 57 x 10 mm [A1, G4] |
| Design flow | 2.0 L/min | 1.2 L/min [A3] |
| Liner reflectance (assumed) | 0.80 | 0.95 |
| UV-C absorbed by water at 90 %/cm | 26.1 % | 54.0 % [B3] |
| RED at 90 %/cm | 14.7 to 19.0 mJ/cm² (R2 not met) | 51.9 to 76.3 mJ/cm² (R2 met) [B5] |
| RED at 70 %/cm | 6.3 to 7.4 mJ/cm² | 17.4 to 21.8 mJ/cm² [B6] |
| Dose sensor signal at 90 %/cm and 70 %/cm | 2.4 nA, unresolved | 16.3 nA, 0.38 nA [C1] |
| Worst-case switch-on | 0.46 s | 0.24 s [D2] |
| Pressure drop | 0.42 bar | 0.15 bar [G2] |
| LED board, nominal | 48.9 °C | 40.3 °C [F3] |
| Window stress at 8 bar | 4.46 MPa | 6.18 MPa [G4] |
| Energy | 3.1 kWh/year | 3.8 kWh/year [E3] |
| Envelope | 235 x 72 x 322 mm | 277 x 100 x 322 mm [H1] |
| Parts cost | $249.00 | $338.00 [I1] |
| Requirements | 8 met, 4 at risk, 3 not met, 1 not verifiable (16) | 13 met, 1 at risk, 2 not met, 1 not verifiable (17); 14 met and 1 not met in v0.3 after the budget top-up [K1] |

*Table 8. v0.3 against v0.4 (constructable design, LMF-DDR-003). Every other number is unchanged.*

| Quantity | v0.3 | v0.4 |
| --- | --- | --- |
| Heat capacity of sink, ring, cap and board | 802 J/K | 781 J/K [F1] |
| Acetal lower cap case: time to 50 °C | 31.4 min | 30.5 min [F5] |
| Upper cap roof stress at 8 bar | not checked (3 mm roof, about 59 MPa) | 2.8 MPa, 13 mm roof [G8] |
| Estimated cost | $338.00, 16 lines | $402.00, 18 lines [I1] |
| R16 | Met | Over the value-engineering target by USD 62 [K1] |

*Table 9. v0.5 against v0.6 (decisions of 2026-10-02 carried into the design). Every other number is unchanged.*

| Quantity | v0.5 | v0.6 |
| --- | --- | --- |
| LED to window gap | 0.8 mm | 1.3 mm, window on a 0.5 mm PTFE washer |
| UV-C entering the water | 87.0 % | 84.8 % [B2] |
| RED at 90 %/cm | 51.9 to 76.3 mJ/cm² | 50.9 to 74.9 mJ/cm² [B5] |
| RED at 70 %/cm | 17.4 to 21.8 mJ/cm² | 17.0 to 21.3 mJ/cm² [B6] |
| Flow for the 20 % margin at 90 %/cm | 1.30 L/min | 1.26 L/min [J1] |
| Wall sensor at 90 %/cm | 16.3 nA | 13.4 nA [C1] |
| Alarm threshold S/S_ref | 0.77 | 0.79 [C3] |
| Window stress at 8 bar | 6.18 MPa | 6.18 MPa, unchanged [G4] |
| LED on-time | 86 h/year | 92 h/year with the idle pulse [E4, E6] |
| Mass | not estimated | 4.97 kg dry, 5.44 kg full [H2] |
| Estimated cost | $402.00, 18 lines | $416.00, 19 lines [I1] |
| R18 | Not verifiable at TRL 3 | Met [C6] |
| Requirements | 13 met | 14 met, 1 not met, 1 at risk, 1 not verifiable, R16 over its target by USD 76 [K1] |
