---
doc_id: LMF-CAL-001
title: LumaFlow sizing calculations
project: LumaFlow
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (flow, Monte Carlo optics and dose, dose monitor, switching, power, thermal, pressure drop, window and structure, size, cost, options)
---

# LumaFlow sizing calculations

On paper, LumaFlow meets eight of its sixteen requirements, has four at risk and misses three; one cannot be verified at TRL 3. The main finding is that the TRL 2 dose estimate was about three times too high. A Monte Carlo ray trace of the 25 mm bore shows that the PTFE wall absorbs about half of the LED output before the water can, so only 26 % of the UV-C is absorbed by the water at 90 %/cm UV transmittance (UVT), not about 78 % as assumed. The reduction equivalent dose (RED) at 2.0 L/min is therefore 14.7 to 19.0 mJ/cm² in clear water, against the 40 mJ/cm² target: **R2 is not met**, in addition to R3 (70 %/cm) and R16 (cost, $249 against $225). The power, window, pressure and size targets hold. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B5], is the line of that script's output that carries it.

> **Safety:** These calculations concern a device meant to disinfect drinking water with UV-C light under mains pressure. They are first-principles estimates for a paper proof of concept, not a substitute for biodosimetry, datasheets or a review by a qualified engineer. The dose results in this note show that the concept, as drawn, does **not** reach the disinfection dose it was sized for. LumaFlow is a research and educational prototype, not a certified water treatment device. See LMF-PRC-001, Safety.

## Scope and method

The note checks every requirement in LMF-REQ-001 v0.3 against the design in LMF-PRC-001 v0.3 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, `levels()` and part volumes, so the dimensions used here are the ones in the STEP files and in drawing LMF-DWG-001. It reads prices from `bom/bom.csv` and the budget from `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py` (about 30 s; it runs the ray trace eleven times and repeats sections A and B for two larger bores).

Status rule for the dose: the laminar-flow RED is the design value, because the laminar profile is the more pessimistic of the two limits and the real profile lies between them [A5]. **Met** needs the laminar RED to clear the target by 20 %.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Flow | 2.0 L/min (0.5 gpm), water at 20 °C for hydraulics, 25 °C for the thermal case | LMF-REQ-001 |
| LEDs | Six 275 nm LEDs, 60 mW UV-C each at 350 mA and 6.2 V (0.36 W, 13.02 W electrical); Lambertian emission | Typical 3535-class UV-C LED ratings; bin to be confirmed |
| Window | UV-grade fused silica, n = 1.496 at 275 nm, bulk transmittance 0.995; air gap 0.8 mm; unpolarized Fresnel losses at both faces; light outside the 26 mm seat aperture or the 25 mm bore is lost | Standard optics |
| Water | n = 1.372; base-e absorption α = −ln(UVT) per cm (0.105/cm at 90 %/cm, 0.357/cm at 70 %/cm); no scattering | UVT definition |
| Walls | Diffuse (Lambertian) reflection. Wetted PTFE 0.80 (sensitivity 0.60 to 0.95); wetted 316 stainless in the lower cap bore 0.30; window and LED side seen from the water 0.10 | Engineering judgment; PTFE in water reflects less than dry PTFE; to be measured |
| Ray trace | 600,000 rays per case, 20 equal-area annuli by 60 axial bins; fluence rate = absorbed power / (α x bin volume) | Collision estimator |
| Flow profile | Two limits: plug flow and fully developed laminar (parabolic) flow | Entrance length [A5] |
| Dose response | First-order inactivation of a challenge organism with 20 mJ/cm² per log (MS2-like), with the same response at 275 nm as at 254 nm | Assumption; the wavelength response must be checked |
| Photodiode | SiC, 0.13 A/W at 275 nm, 0.06 mm² active area, behind an 8 mm quartz window of 0.92 transmittance | Typical TO-46 SiC photodiode |
| Flow sensor | Hall-effect turbine, about 7.5 Hz per L/min; Kv 0.35 m³/h | Typical of this sensor class; to confirm |
| Valve | 24 V DC normally closed, 4.8 W (0.2 A) held open, Kv 0.25 m³/h | Typical small direct-acting solenoid |
| Electronics | Driver 90 %; controller 0.6 W active; adapter 88 % at load, 70 % at light load, 0.1 W no-load | US DOE Level VI no-load class for small adapters |
| Use | 15 L/day in 20 draws, 5 s run-on per draw | LMF-REQ-001 |
| Thermal | Sink natural convection 5 W/(m²·K) (fins hanging down) plus radiation, ε = 0.85; 0.5 mm pads of 3 W/(m·K); 316 at 16 W/(m·K); water film 300 W/(m²·K) in the lower cap (range 150 to 600); 10 K/W junction to board per LED | Engineering judgment; film coefficient is the main uncertainty |
| Structure | Fused quartz design tensile stress 6.8 MPa (1,000 psi) ([Momentive, mechanical properties](https://www.momentivetech.com/materials/fused-quartz-materials/quartz-properties/mechanical-properties)); Poisson ratio 0.17; simply supported edge; 8 bar working pressure | Roark circular plate, uniform load |

## A. Flow and hydraulics (R1)

The irradiated channel is 25 mm across and 246 mm long, from the window to the PTFE top disc; the flow path from inlet to outlet is 230 mm [A1]. The channel holds 121 mL, 113 mL of it between the ports [A2]. At 2.0 L/min the mean velocity is 6.79 cm/s and the mean residence time 3.39 s [A3]. The Reynolds number is 1,691 at 20 °C and 1,115 at 5 °C, so the flow is laminar [A4]. The laminar entrance length, about 2.1 m, is far longer than the flow path [A5], so the velocity profile lies between plug flow and a parabola; both limits are carried through section B. R1 is met by the 2 L/min restrictor, and the flow sensor range of 0.3 to 6 L/min covers it.

## B. Optics and UV-C dose (R2, R3)

The six LEDs give 0.36 W of UV-C from 13.02 W electrical, a UV-C efficiency of 2.8 % [B1]. Of that, 80.2 % enters the water; the rest is lost at the window seat, the edge of the bore and the two window faces [B2]. Once in the water, light crossing a 25 mm bore meets the wall after a few centimeters, far sooner than clear water absorbs it (mean free path 1/α = 9.5 cm at 90 %/cm). With a wetted PTFE reflectance of 0.80 the walls take 49.8 % of the LED output and the water only 26.1 %; at 70 %/cm the water takes 46.2 % [B3, B4]. The TRL 2 estimate assumed about 78 %, which is why its dose was too high.

*Table 2. Dose at 2.0 L/min (mJ/cm²). Average is the flow-weighted average dose; RED is for the 20 mJ/cm² per log organism.*

| UVT (%/cm) | Average dose | RED, plug flow | RED, laminar flow | Reactor efficiency, laminar |
| --- | --- | --- | --- | --- |
| 95 | 26.3 | 26.2 | 19.5 | 0.74 |
| 90 | 19.1 | 19.0 | 14.7 | 0.77 |
| 85 | 14.6 | 14.5 | 11.6 | 0.80 |
| 80 | 11.4 | 11.4 | 9.3 | 0.81 |
| 75 | 9.2 | 9.2 | 7.6 | 0.83 |
| 70 | 7.4 | 7.4 | 6.3 | 0.85 |

At the design water quality of 90 %/cm the RED is 14.7 (laminar) to 19.0 (plug) mJ/cm² [B5]. **R2 (40 mJ/cm²) is not met**; the dose is about 37 to 48 % of the target. At 70 %/cm it is 6.3 to 7.4 mJ/cm² [B6], so **R3 is not met** either, and both values are below the Class B level of 16 mJ/cm² except the plug-flow limit at 90 %/cm.

The reactor efficiency (RED over average dose) of 0.77 is better than the 0.5 assumed at TRL 2, because the axial beam puts the highest fluence on the axis where laminar water moves fastest. Streamline doses at 90 %/cm range from 10 mJ/cm² on the axis to 20 at mid radius and 366 beside the wall [B7]. The loss is in the optics, not in the mixing. The wetted PTFE reflectance moves the result only modestly: 12.8, 14.7 and 16.2 mJ/cm² at reflectances of 0.60, 0.80 and 0.90 [B8]. LEDs 20 % below rating (bin, aging or temperature) give 11.8 mJ/cm² [B9].

## C. Dose monitor (R4)

The photodiode behind the top disc looks down 246 mm of water and reflective wall. It sees 0.033 mW/cm² and gives a photocurrent of about 2.4 nA at 90 %/cm, 0.08 nA at 80 %/cm, and nothing the ray trace can resolve at 70 %/cm [C1]. Between 90 and 85 %/cm the far-end signal falls 4.4 times faster, in log terms, than the RED [C2].

That steep slope makes one mapping unsafe. If the controller blamed every loss of signal on the water, LEDs aged to 70 % output in 90 %/cm water would read as 88.3 %/cm and claim 13.6 mJ/cm², when the true RED is 10.3 [C4]. The safe rule is the proportional mapping RED_est = RED_ref x (S/S_ref) x (Q_ref/Q), which blames every loss on the LEDs and so always under-reads [C3, C4]. Because the reference RED (14.7 mJ/cm²) is already below 40, the alarm threshold S/S_ref = 2.72 is above 1, and the unit as drawn would alarm and close its valve in any water [C3]. That is safe, but it means R4 cannot work as intended until R2 is met.

A sensor in the tube wall at mid height would see 0.67 mW/cm² at 90 %/cm and 0.032 mW/cm² at 70 %/cm, a usable signal across the whole range, and its signal falls only 2.8 times as fast as the RED [C5]. R4 is **at risk**.

## D. Flow switching and run-on (R5)

At the 0.3 L/min switch-on threshold the flow sensor gives 2.25 Hz, one pulse every 0.44 s [D1]. With the LED rise time the worst-case switch-on is 0.46 s against 0.5 s [D2], a thin margin: R5 is **at risk**. A sensor with a higher pulse rate would widen it.

During the 5 s run-on the water held in the channel receives a volume-average 37 mJ/cm² at 90 %/cm [D4]. Taking the dose each parcel collected while flowing plus the run-on, every parcel in the flow path has at least 18 mJ/cm² when flow stops (plug flow) [D3]. The run-on therefore does not leave a worse slug than a normal pass; it cannot make up for the low dose of section B.

## E. Power and energy (R9)

The LEDs draw 13.02 W; with the driver, the 4.8 W valve and the controller the 24 V bus carries 19.87 W, and the mains draw is 22.6 W while water flows [E1]. Standby is 0.21 W, dominated by the adapter's no-load draw and the powered flow sensor [E2]. **R9 is met** (25 W and 0.5 W).

At 15 L/day the LEDs run 9.2 min/day (56 h/year); the unit uses 8.6 Wh/day or 3.1 kWh/year [E3]. At that rate 10,000 h of LED on-time would take 179 years [E4], so LED life is set by aging in storage and by switching, not by on-time. For comparison, tap-scale mercury units drawing 13 to 22 W all day ([VIQUA VT1, VT4 and S2Q-PA spec sheet](https://viqua.com/wp-content/uploads/LIT520326_SpecSheet.pdf)) use 114 to 193 kWh/year [E5].

## F. Thermal (R10)

The LEDs turn 12.66 W into heat. The finned sink alone rejects it to cabinet air through 4.18 K/W; the sink, spreader ring, lower cap and board store 435 J/K [F1]. The TRL 3 design adds a water path: an aluminum spreader ring from the sink base to a 316 stainless lower cap whose bore and inlet port are wetted. That path is 2.49 K/W, and it carries 8.7 W of the 12.7 W into the water, which warms by 0.06 K [F2].

With continuous flow the LED board settles at 55.9, 48.9 or 44.1 °C for water-film coefficients of 150, 300 or 600 W/(m²·K) [F3], against 50 °C. The nominal case meets the target with 1.1 K to spare, and the low case does not, so R10 is **at risk**. The LED junctions sit near 70 °C [F4]. An acetal lower cap, with no water path, would settle at 85 °C and pass 50 °C after 13.6 min of flow [F5]; that result is why the TRL 3 model uses a stainless lower cap. If the LEDs stuck on with no flow, the board would head for 69 °C, reaching 65 °C after 72.6 min; the 5 s run-on adds only 0.15 K [F6].

## G. Pressure drop, window and structure (R7, R8)

*Table 3. Pressure drop at 2.0 L/min, excluding the flow restrictor [G1, G2].*

| Element | Drop (bar) |
| --- | --- |
| Flow sensor (Kv 0.35) | 0.12 |
| Solenoid valve (Kv 0.25) | 0.23 |
| 1 m of 1/4 in bore tube | 0.030 |
| Fittings (K = 6 in all) | 0.033 |
| Reactor ports | 0.006 |
| Reactor channel | 0.00001 |
| **Total** | **0.42 (6.0 psi)** |

The unit drops 0.42 bar against the 0.5 bar target [G2]. The margin rests on two assumed flow coefficients; with a Kv 0.5 sensor and a Kv 0.4 valve the drop would be 0.22 bar [G3]. R8 is **at risk** until the datasheets confirm the coefficients. The restrictor is excluded because it is meant to absorb the excess supply pressure; at the minimum supply of 2 bar, 1.58 bar remains for the restrictor and faucet [G3].

The 32 x 6 mm window on its 26 mm seat carries a peak stress of 4.46 MPa at 8 bar, inside the 6.8 MPa design stress (a 3 mm window would see 17.9 MPa) [G4]: **R7 is met**. A 16 bar water-hammer spike would raise it to 8.9 MPa [G5], so the pressure-limiting valve upstream is a requirement of the installation, not an option. The 8 mm sensor window sees 1.69 MPa and the tube hoop stress is 4.9 MPa [G6]. Each cap carries an end load of 1,005 N, 251 N per M4 tie rod or 29 MPa in the thread, well within 316 stainless [G7].

## H. Size and I. Cost (R14, R16)

The unit is 235 x 72 x 322 mm without the adapter, inside the 350 x 150 x 350 mm envelope [H1]: **R14 is met**.

The 16-line BOM totals $249.00 against the new `budget_usd` of $225, $24.00 over [I1]: **R16 is not met**. The largest lines are the LEDs ($54), the machined 316 lower cap ($28) and the photodiode ($22) [I2]. The TRL 2 total was $217; the stainless lower cap, the PTFE extension and insert that keep UV-C off the acetal cap, and the tie rods account for most of the rise.

## J. Options for the dose shortfall

*Table 4. Ways to reach 40 mJ/cm² (laminar RED). All keep six LEDs unless stated.*

| Option | Result | Cost of the change |
| --- | --- | --- |
| R2-a: lower the design flow | 40 mJ/cm² at 90 %/cm up to 0.64 L/min [J3] | R1 falls to about a third; filling a 1 L bottle takes about 1.6 min |
| R2-b: more LEDs at 2.0 L/min | 17 LEDs; 53 W from the mains [J4] | About $99 more; R9 (25 W) fails |
| R2-c: liner reflectance 0.95 | 17.3 mJ/cm² at 2.0 L/min; 40 mJ/cm² up to 0.78 L/min [J5] | Specialty reflector; small gain alone |
| R2-d: larger bore, 40 mm | 25.0 (laminar) to 33.7 (plug) mJ/cm² at 2.0 L/min [J6-40] | Larger window, caps and tube |
| R2-d: larger bore, 50 mm | 30.0 (laminar) to 41.0 (plug) mJ/cm² at 2.0 L/min [J6-50] | Window about 9.5 mm thick [J7]; larger parts |
| Option B (R3 at 70 %/cm) | 38 LEDs, 82 W of LED power [J1] | Out of scope for this budget |
| Option C (R3 at 70 %/cm) | Six LEDs meet 40 mJ/cm² only below 0.26 L/min [J2] | Proportional valve; very slow tap |

A wider bore is the strongest single lever, because the light then crosses more water between wall reflections. Options R2-c and R2-d combine. These are proposals for Amish (see `docs/REVIEW.md`); the model and BOM stay at the 25 mm bore.

## K. Requirement status

*Table 5. Requirement status at TRL 3 (LMF-REQ-001 v0.3). Not met items first.*

| ID | Target | Value (tag) | Status |
| --- | --- | --- | --- |
| R2 | RED 40 mJ/cm² or more at 2.0 L/min, 90 %/cm | 14.7 (laminar) to 19.0 (plug) mJ/cm² [B5] | **Not met** |
| R3 | RED 40 mJ/cm² or more at 2.0 L/min, 70 %/cm | 6.3 to 7.4 mJ/cm² [B6] | **Not met** |
| R16 | Parts cost $225 or less; no custom PCB | $249.00 [I1]; module-based electronics | **Not met** |
| R4 | Dose monitor; alarm and valve closed within 1 s | Far-end signal 2.4 nA at 90 %/cm, unresolved at 70 %/cm; alarm would trip in any water while R2 is not met [C1, C3] | At risk |
| R5 | LEDs on within 0.5 s above 0.3 L/min; 5 s run-on | 0.46 s worst case [D2] | At risk |
| R8 | 0.5 bar or less at 2.0 L/min | 0.42 bar, on assumed Kv [G2] | At risk |
| R10 | LED board 50 °C or less | 44.1 to 55.9 °C steady; 48.9 nominal [F3] | At risk |
| R15 | Window and LED head replaced in 15 min | Four tie rods and two push-fit ports; needs a build to time | Not verifiable at TRL 3 |
| R1 | 2.0 L/min, restrictor | Restrictor; sensor range covers it [A3] | Met |
| R6 | No mercury; full output in 0.1 s | LEDs, microsecond rise | Met |
| R7 | Window 6.8 MPa or less at 8 bar | 4.46 MPa [G4] | Met |
| R9 | 25 W flowing, 0.5 W standby | 22.6 W, 0.21 W [E1, E2] | Met |
| R11 | Food-contact wetted parts; no UV-C on plastics but PTFE | 316 lower cap; PTFE liner, top disc and 316 insert shield the acetal upper cap | Met |
| R12 | No UV-C outside the unit; interlocks | Metal and PTFE light path in the model; interlock by design | Met |
| R13 | 24 V DC only at the unit | Certified adapter and input fuse | Met |
| R14 | 350 x 150 x 350 mm or less | 235 x 72 x 322 mm [H1] | Met |

Counts: 8 met, 3 not met, 4 at risk, 1 not verifiable at TRL 3 [K1].

## Numbers corrected in the design documents

*Table 6. TRL 2 figures checked against this note.*

| Quantity | TRL 2 (v0.2) | TRL 3 (this note) |
| --- | --- | --- |
| UV-C absorbed by water at 90 %/cm | about 78 %, 0.28 W | 26.1 %, 0.094 W [B3] |
| Average dose at 90 %/cm | about 80 mJ/cm² | 19.1 mJ/cm² [B5] |
| RED at 90 %/cm | about 40 mJ/cm² (R2 met) | 14.7 to 19.0 mJ/cm² (R2 not met) [B5] |
| RED at 70 %/cm | about 14 mJ/cm² | 6.3 to 7.4 mJ/cm² [B6] |
| Reactor efficiency | 0.5 assumed | 0.77 laminar [B5] |
| Light left at the far end, 90 %/cm | about 12 % | 0.005 % reaches the sensor window [B3] |
| Irradiated length, volume, residence | 200 mm, 98 mL, 2.9 s | 246 mm, 121 mL; 3.39 s between ports [A1 to A3] |
| Mains power, standby | 21.6 W, 0.3 W | 22.6 W, 0.21 W [E1, E2] |
| Daily and yearly energy | 10 Wh, 3.8 kWh | 8.6 Wh, 3.1 kWh [E3] |
| Mercury comparison | 10 to 25 W, 90 to 220 kWh | 13 to 22 W, 114 to 193 kWh (sourced) [E5] |
| Water temperature rise | 0.09 K | 0.06 K [F2] |
| Window stress at 8 bar, 6 mm | 4.5 MPa | 4.46 MPa [G4] |
| Envelope | 240 x 75 x 325 mm | 235 x 72 x 322 mm [H1] |
| Parts cost | $217 | $249.00 [I1] |
| Option B (R3) | about 17 LEDs, 40 W | 38 LEDs, 82 W [J1] |
| Option C (R3) | about 0.7 L/min | 0.26 L/min [J2] |
