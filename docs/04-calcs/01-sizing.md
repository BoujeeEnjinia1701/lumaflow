---
doc_id: LMF-CAL-001
title: LumaFlow sizing calculations
project: LumaFlow
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# LumaFlow sizing calculations

This note checks the LumaFlow design as revised by LMF-DDR-002: a 50 mm bore lined with high-reflectance PTFE, a design flow of 1.2 L/min (0.32 gpm), a UV-C photodiode in the tube wall at mid height, a flow sensor of 15 Hz per L/min, an upstream pressure limiter and a thermal cut-back. On paper, LumaFlow now meets thirteen of its seventeen requirements, has one at risk (R4) and misses two (R3 and R16); one cannot be verified at TRL 3. The reduction equivalent dose (RED) in clear water (90 %/cm UV transmittance, UVT) is 51.9 (laminar) to 76.3 (plug) mJ/cm², so **R2 is now met** with the 20 % margin this note requires; in v0.1, with a 25 mm bore at 2.0 L/min, it was 14.7 to 19.0 mJ/cm². The dose at the 70 %/cm test condition is 17.4 to 21.8 mJ/cm² (**R3 not met**, kept visible by decision D1), and the parts cost $338.00 against the $225 budget (**R16 not met**). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B5], is the line of that script's output that carries it.

> **Safety:** These calculations concern a device meant to disinfect drinking water with UV-C light under mains pressure. They are first-principles estimates for a paper proof of concept, not a substitute for biodosimetry, datasheets or a review by a qualified engineer. A calculated dose above target is not a demonstrated dose. LumaFlow is a research and educational prototype, not a certified water treatment device. See LMF-PRC-001, Safety.

## Scope and method

The note checks every requirement in LMF-REQ-001 v0.4 against the design in LMF-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `levels()` and part volumes, so the dimensions used here are the ones in the STEP files and in drawing LMF-DWG-001 Rev P2. It reads prices from `bom/bom.csv` and the budget from `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py` (about 20 s; it runs the ray trace eight times).

Status rule for the dose: the laminar-flow RED is the design value, because the laminar profile is the more pessimistic of the two limits and the real profile lies between them [A5]. **Met** needs the laminar RED to clear the target by 20 %.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Flow | 1.2 L/min (0.32 gpm), set by the restrictor; water at 20 °C for hydraulics, 25 °C for the thermal case | LMF-REQ-001 v0.4, R1 |
| LEDs | Six 275 nm LEDs on a 32 mm circle, 60 mW UV-C each at 350 mA and 6.2 V (0.36 W, 13.02 W electrical); Lambertian emission | Typical 3535-class UV-C LED ratings; bin to be confirmed |
| Window | UV-grade fused silica, 57 x 10 mm on a 51 mm seat, n = 1.496 at 275 nm, bulk transmittance 0.995; air gap 0.8 mm; unpolarized Fresnel losses at both faces; light outside the seat aperture or the 50 mm bore is lost | Standard optics |
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

The irradiated channel is 50 mm across and 242 mm long, from the window to the PTFE top disc; the flow path from inlet to outlet is 226 mm [A1]. The channel holds 475 mL, 444 mL of it between the ports [A2]. At 1.2 L/min the mean velocity is 1.02 cm/s and the mean residence time 22.2 s [A3]. The Reynolds number is 507 at 20 °C and 334 at 5 °C, so the flow is laminar [A4]. The laminar entrance length, about 1.3 m, is far longer than the flow path [A5], so the velocity profile lies between plug flow and a parabola; both limits are carried through section B. R1 is met by the 1.2 L/min restrictor, and the flow sensor range of 0.3 to 6 L/min covers it.

## B. Optics and UV-C dose (R2, R3)

The six LEDs give 0.36 W of UV-C from 13.02 W electrical, a UV-C efficiency of 2.8 % [B1]. Of that, 87.0 % enters the water [B2]. In the 50 mm bore light crosses twice as much water between wall reflections as in the old 25 mm bore, and the liner returns 95 % of what reaches it. At 90 %/cm the water absorbs 54.0 % of the LED output and the walls 27.0 % (v0.1: 26.1 % and 49.8 %); at 70 %/cm the water absorbs 68.1 % [B3, B4].

*Table 2. Dose at 1.2 L/min (mJ/cm²). Average is the flow-weighted average dose; RED is for the 20 mJ/cm² per log organism.*

| UVT (%/cm) | Average dose | RED, plug flow | RED, laminar flow | Reactor efficiency, laminar |
| --- | --- | --- | --- | --- |
| 95 | 134.3 | 133.7 | 84.5 | 0.63 |
| 90 | 76.8 | 76.3 | 51.9 | 0.68 |
| 85 | 51.7 | 51.3 | 36.8 | 0.71 |
| 80 | 37.5 | 37.2 | 27.7 | 0.74 |
| 75 | 28.4 | 28.1 | 21.7 | 0.77 |
| 70 | 22.0 | 21.8 | 17.4 | 0.79 |

At the design water quality of 90 %/cm the RED is 51.9 (laminar) to 76.3 (plug) mJ/cm² [B5]. **R2 (40 mJ/cm²) is met**, with the laminar value 30 % above the target. At 70 %/cm it is 17.4 to 21.8 mJ/cm² [B6], so **R3 is not met**, as decision D1 accepted; it is now above the Class B level of 16 mJ/cm².

The reactor efficiency (RED over average dose) is 0.68, lower than the 0.77 of v0.1: the slow laminar core on a wide bore sees less light than the water beside the wall. Streamline doses at 90 %/cm range from 42 mJ/cm² on the axis to 80 at mid radius and 1,453 beside the wall [B7]. The liner reflectance is the main optical uncertainty: 46.3, 49.9 and 51.9 mJ/cm² at 0.80 (plain PTFE), 0.90 and 0.95 [B8], so even plain PTFE meets 40 mJ/cm² but not the 20 % margin. LEDs 20 % below rating (bin, aging or temperature) give 41.5 mJ/cm² [B9].

## C. Dose monitor (R4)

The photodiode now sits behind an 8 mm quartz window in the tube wall at mid height (Z = 166 mm), facing the enclosure. It sees 0.23 mW/cm² and gives about 16.3 nA at 90 %/cm, 2.6 nA at 80 %/cm and 0.38 nA at 70 %/cm [C1], a signal across the whole range; the top-disc position of v0.1 gave 2.4 nA at 90 %/cm and nothing resolvable at 70 %/cm. Between 90 and 85 %/cm the wall signal falls 2.9 times as fast, in log terms, as the RED [C2] (4.4 times for the old position).

*Table 3. Wall sensor signal against UVT.*

| UVT (%/cm) | Irradiance (mW/cm²) | Photocurrent (nA) | Signal relative to 90 % | RED relative to 90 % |
| --- | --- | --- | --- | --- |
| 95 | 0.738 | 53.0 | 3.25 | 1.63 |
| 90 | 0.227 | 16.3 | 1.00 | 1.00 |
| 85 | 0.084 | 6.1 | 0.37 | 0.71 |
| 80 | 0.036 | 2.6 | 0.16 | 0.54 |
| 75 | 0.012 | 0.9 | 0.055 | 0.42 |
| 70 | 0.005 | 0.38 | 0.024 | 0.34 |

The controller keeps the proportional mapping RED_est = RED_ref x (S/S_ref) x (Q_ref/Q), which blames every loss of signal on the LEDs and so always under-reads. With RED_ref = 51.9 mJ/cm² the alarm threshold is S/S_ref = 0.77 [C3]. With LEDs at rated output the alarm trips below about 88.7 %/cm UVT, and LEDs aged to 77 % of output trip it in 90 %/cm water, where the true RED is 40.0 mJ/cm² [C4]. A mapping that blamed the water instead would be unsafe: with LEDs at 70 % output in 90 %/cm water it would claim 46.4 mJ/cm² when the true RED is 36.3 [C5]. R4 stays **at risk** because the sub-nanoampere signal in poor water, the mapping and the 1 s fail-safe still need firmware and a test, which are TRL 4 work.

## D. Flow switching and run-on (R5)

At the 0.3 L/min switch-on threshold the 15 Hz per L/min sensor gives 4.5 Hz, one pulse every 0.22 s [D1]. With the LED rise time the worst-case switch-on is 0.24 s against 0.5 s [D2] (v0.1: 0.46 s with a 7.5 Hz per L/min sensor): **R5 is met**.

During the 5 s run-on the water held in the channel receives a volume-average 19 mJ/cm² at 90 %/cm [D4]. Taking the dose each parcel collected while flowing plus the run-on, every parcel in the flow path has at least 62 mJ/cm² when flow stops (plug flow) [D3].

## E. Power and energy (R9)

The LEDs draw 13.02 W; with the driver, the 4.8 W valve and the controller the 24 V bus carries 19.87 W, and the mains draw is 22.6 W while water flows [E1]. Standby is 0.21 W, dominated by the adapter's no-load draw and the powered flow sensor [E2]. **R9 is met** (25 W and 0.5 W).

At 15 L/day and 1.2 L/min the LEDs run 14.2 min/day (86 h/year); the unit uses 10.4 Wh/day or 3.8 kWh/year [E3]. At that rate 10,000 h of LED on-time would take 116 years [E4], so LED life is set by aging in storage and by switching, not by on-time. For comparison, tap-scale mercury units drawing 13 to 22 W all day ([VIQUA VT1, VT4 and S2Q-PA spec sheet](https://viqua.com/wp-content/uploads/LIT520326_SpecSheet.pdf)) use 114 to 193 kWh/year [E5].

## F. Thermal (R10)

The LEDs turn 12.66 W into heat. The larger 90 x 90 mm finned sink rejects it to cabinet air through 2.46 K/W; the sink, spreader ring, lower cap and board store 802 J/K [F1]. The water path through the spreader ring and the 316 stainless lower cap is 1.55 K/W and carries 9.0 W of the 12.7 W into the water, which warms by 0.11 K [F2].

With continuous flow the LED board settles at 44.8, 40.3 or 37.1 °C for water-film coefficients of 150, 300 or 600 W/(m²·K) [F3], below 50 °C in every case; the LED junctions sit near 61 °C [F4]. The board temperature sensor and the cut-back of LED current above 50 °C (decision in LMF-DDR-002) are a backstop for the uncertain film coefficient: **R10 is met**. An acetal lower cap, with no water path, would settle at 63 °C and pass 50 °C after 31.4 min of flow [F5], which supports the 316 lower cap (LMF-DDR-002 confirms it). If the LEDs stuck on with no flow, the board would head for 53 °C, where the cut-back would act; the 5 s run-on adds only 0.08 K [F6].

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

The 57 x 10 mm window on its 51 mm seat carries a peak stress of 6.18 MPa at 8 bar, inside the 6.8 MPa design stress [G4]: **R7 is met**, with a 9 % margin (v0.1: 4.46 MPa on a 26 mm seat). Unprotected, a 16 bar water-hammer spike would raise it to 12.4 MPa. With the pressure limiter set at 4 bar the window carries 3.09 MPa static, and a transient doubling to 8 bar gives 6.18 MPa [G5]: **R17 is met** as an installation requirement. The 8 mm sensor window sees 1.69 MPa and the tube hoop stress is 8.3 MPa [G6]. Each cap carries an end load of 2,655 N; four M5 316 rods take 664 N each, 47 MPa in the thread [G7].

## H. Size and I. Cost (R14, R16)

The unit is 277 x 100 x 322 mm without the adapter, inside the 350 x 150 x 350 mm envelope [H1]: **R14 is met**.

The 16-line BOM totals $338.00 against the `budget_usd` of $225, $113.00 over [I1]: **R16 is not met**. The largest lines are the LEDs ($54), the high-reflectance PTFE liner ($45) and the machined 316 lower cap ($42) [I2]. The rise from $249.00 comes from the larger reactor: the liner, window, caps, tube and sink all grow with the 50 mm bore.

## J. Flow limits and options

*Table 5. Flow limits for this reactor and the options against R3.*

| Case | Result |
| --- | --- |
| Six LEDs, 90 %/cm | 40 mJ/cm² (laminar) up to 1.60 L/min; 48 mJ/cm² (Met with margin) up to 1.30 L/min [J1] |
| Same reactor at the former 2.0 L/min | 32.7 (laminar) to 45.9 (plug) mJ/cm² [J2] |
| Option B (R3 at 70 %/cm) | 14 LEDs, 30 W of LED power [J3]; R9 would fail |
| Option C (R3 at 70 %/cm) | Six LEDs meet 40 mJ/cm² below 0.48 L/min [J4]; proportional valve, later upgrade under D1 |

The 1.2 L/min design flow sits inside the 1.30 L/min limit for the 20 % margin. Filling a 1 L bottle takes about 50 s.

## K. Requirement status

*Table 6. Requirement status at TRL 3 (LMF-REQ-001 v0.4). Not met items first.*

| ID | Target | Value (tag) | Status |
| --- | --- | --- | --- |
| R3 | RED 40 mJ/cm² or more at 1.2 L/min, 70 %/cm | 17.4 to 21.8 mJ/cm² [B6] | **Not met** (accepted by D1) |
| R16 | Parts cost $225 or less; no custom PCB | $338.00 [I1]; module-based electronics | **Not met** |
| R4 | Dose monitor; alarm and valve closed within 1 s | Wall signal 16.3 nA at 90 %/cm, 0.38 nA at 70 %/cm; alarm below about 89 %/cm [C1, C4] | At risk |
| R15 | Window and LED head replaced in 15 min | Four tie rods and two push-fit ports; needs a build to time | Not verifiable at TRL 3 |
| R1 | 1.2 L/min, restrictor | Restrictor; sensor range covers it [A3] | Met |
| R2 | RED 40 mJ/cm² or more at 1.2 L/min, 90 %/cm | 51.9 (laminar) to 76.3 (plug) mJ/cm² [B5] | Met |
| R5 | LEDs on within 0.5 s above 0.3 L/min; 5 s run-on | 0.24 s worst case [D2] | Met |
| R6 | No mercury; full output in 0.1 s | LEDs, microsecond rise | Met |
| R7 | Window 6.8 MPa or less at 8 bar | 6.18 MPa [G4] | Met |
| R8 | 0.5 bar or less at 1.2 L/min, excluding the restrictor | 0.15 bar, on assumed Kv [G2] | Met |
| R9 | 25 W flowing, 0.5 W standby | 22.6 W, 0.21 W [E1, E2] | Met |
| R10 | LED board 50 °C or less; cut-back above 50 °C | 37.1 to 44.8 °C steady [F3] | Met |
| R11 | Food-contact wetted parts; no UV-C on plastics but PTFE | 316 lower cap; PTFE liner, top disc and 316 insert shield the acetal upper cap | Met |
| R12 | No UV-C outside the unit; interlocks | Metal and PTFE light path; sensor window sealed by the photodiode saddle; interlock by design | Met |
| R13 | 24 V DC only at the unit | Certified adapter and input fuse | Met |
| R14 | 350 x 150 x 350 mm or less | 277 x 100 x 322 mm [H1] | Met |
| R17 | Pressure limiter at 4 bar or less upstream | Window 6.18 MPa at twice the setting [G5] | Met |

Counts: 13 met, 2 not met, 1 at risk, 1 not verifiable at TRL 3 [K1].

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
| Requirements | 8 met, 4 at risk, 3 not met, 1 not verifiable (16) | 13 met, 1 at risk, 2 not met, 1 not verifiable (17) [K1] |
