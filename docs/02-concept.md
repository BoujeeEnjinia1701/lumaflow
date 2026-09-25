---
doc_id: LMF-PRC-001
title: LumaFlow design precis
project: LumaFlow
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, dose, power, thermal and window estimates, safety, media)
---

# LumaFlow design precis

## Summary

LumaFlow is an inline UV-C LED reactor with a flow-activated switch and a dose monitor, sized for a household tap. Water flows up a PTFE-lined stainless tube, 25 mm bore and 200 mm long, while six 275 nm LEDs at the bottom shine up the water column through a quartz window. A Hall-effect flow sensor turns the LEDs on only while water runs, and a UV-C photodiode at the top measures the light that reaches the far end, which lets the controller estimate the dose and close a valve if it falls too low.

First-order numbers, all estimates to be checked at TRL 3: at 2 L/min (0.5 gpm) in clear water (90 %/cm UV transmittance) the reactor delivers a reduction equivalent dose of about 40 mJ/cm², the NSF/ANSI 55 Class A level, with no margin. At 70 %/cm UVT, the Class A test condition, it delivers only about 14 mJ/cm², so **R3 is not met**. It draws about 22 W while water flows and about 0.3 W on standby, about 10 Wh per day in all. Parts cost about $217, **about $17 over the $200 budget (R16 not met)**.

![Hero render](../media/hero.png)

*Figure 1. LumaFlow massing model, mounted on its wall bracket under a sink, with the 24 V adapter on the cabinet floor. The grey 1 L bottle is for scale.*

## How it works

1. **Flow starts.** When someone opens the drinking-water faucet, water enters through the Hall-effect flow sensor (item 8). Its pulses tell the controller that flow has started and how fast it is.
2. **LEDs on.** Within about 0.5 s the controller opens the normally closed outlet valve (item 11) and drives the six 275 nm LEDs (item 4) at 350 mA. LEDs reach full output almost at once, so no warm-up or bypass is needed.
3. **Irradiate.** The LEDs sit under a 6 mm fused quartz window (item 3) at the bottom of the reactor and shine up the 200 mm water column. Water enters at the bottom (item 6), flows up through the 25 mm bore of the PTFE liner (item 2), and leaves at the top (item 7). PTFE is a strong diffuse reflector in the UV-C band, so light that reaches the wall is mostly scattered back into the water instead of lost.
4. **Measure.** A UV-C photodiode (item 9) behind a small window in the upper cap looks down the bore and measures the light that has crossed the whole water column. Its signal falls if the water's UVT drops, the window fouls or the LEDs age. The controller combines that reading with the flow rate to estimate the dose.
5. **Alarm and shut off.** If the estimated dose falls below 40 mJ/cm², the flow exceeds its limit, a sensor fails or the enclosure lid is opened, the controller closes the valve, sounds the buzzer and shows a red status light. The valve also closes if power is lost, so no untreated water passes silently.
6. **Flow stops.** The LEDs stay on for 5 s after flow stops, so the water left in the reactor (about 0.1 L) receives more than a full dose, then everything switches off.

![Cutaway](../media/cutaway.png)

*Figure 2. Cutaway through the reactor axis, looking at the wall. From the bottom: heat sink, LED board, quartz window, lower end cap with inlet, PTFE-lined tube, upper end cap with outlet and photodiode. The controller board is visible in the enclosure on the right.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`. Table 1 lists the proposed choices; every choice is proposed, awaiting Amish.

Table 1. Main components.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Reactor tube | 316 stainless, 40 mm OD x 3 mm wall x 200 mm | Carries pressure and blocks all UV-C |
| 2 | PTFE reflector liner | Virgin PTFE tube, 25 mm bore | Forms the water channel and reflects UV-C back into the water |
| 3 | Quartz window | UV-grade fused silica, 32 mm diameter x 6 mm | Thickness set by the 8 bar stress estimate below |
| 4 | UV-C LED array | Six 275 nm LEDs, about 60 mW each at 350 mA, on one aluminum-core board | 275 nm gives the most output per dollar; 265 nm is closer to the germicidal peak |
| 5 | Heat spreader and heat sink | Finned aluminum sink with a stainless contact plate to the wetted cap | LEDs run only while water flows, so the water carries most of the heat |
| 6 | Lower end cap | Acetal or 316 stainless, 3/8 in inlet port, window seat, O-rings | Food-contact grade |
| 7 | Upper end cap | Acetal or 316 stainless, 3/8 in outlet port, sensor port | Outlet at the top purges air |
| 8 | Hall-effect flow sensor | Food-grade, 0.3 to 6 L/min, pulse output | Acts as the flow switch and the flow meter |
| 9 | UV-C photodiode and amplifier | SiC or AlGaN photodiode with transimpedance amplifier | Dose monitor |
| 10 | Controller and LED driver | Microcontroller, 350 mA constant-current driver, valve driver | Module-based; no custom PCB at first |
| 11 | Solenoid shutoff valve | 24 V DC, normally closed, food-grade | Closes on alarm or power loss |
| 12 | 24 V power adapter | Certified external adapter, 30 W | The only part at mains voltage |
| 13 | Electronics enclosure | Printed PETG, lid interlock, status light, buzzer | Dry side only |
| 14 | Wall bracket | Backplate with two clamp rings | Holds the reactor vertical |
| 15 | Fittings and tubing | 3/8 in push-fit, tee to the cold line, 2 L/min flow restrictor | Restrictor enforces R1 |
| 16 | Hardware and consumables | Screws, wire, thermal paste | Not modeled |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions are stated with each calculation.

### Flow and residence time

Assumptions: 2.0 L/min (33.3 cm³/s) through a 25 mm bore, 200 mm long, water at 20 °C.

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Irradiated volume | about 98 mL | π x (1.25 cm)² x 20 cm |
| Mean residence time | about 2.9 s | 98 mL / 33.3 mL/s |
| Mean velocity | about 6.8 cm/s | 33.3 cm³/s / 4.9 cm² |
| Reynolds number | about 1,700 | Laminar to transitional flow |

Laminar flow is a weakness: water near the axis passes faster than the average and water near the wall slower, so the dose spreads widely. That is why the dose estimate below uses a low reactor efficiency, and why a simple flow mixer at the inlet is an open question.

### UV-C dose

Assumptions: six LEDs at about 60 mW optical each (0.36 W total) at 350 mA and about 6.2 V; UV-C wall-plug efficiency about 2.8 %, inside the 2 to 5 % range reported for current UV-C LEDs ([Tech-LED](https://tech-led.com/uv-c-leds-for-disinfection-and-sterilization-component-selection-265-280-nm/)); about 78 % of the emitted light is absorbed by the water at 90 %/cm UVT after window and wall losses, rising to about 92 % at 70 %/cm; and a reactor efficiency (reduction equivalent dose divided by average dose) of 0.5 for this simple laminar reactor. The volume-average dose is the absorbed UV power divided by the flow and the water's absorption coefficient α (base e): D = P / (Q x α).

Table 2. Dose estimates at 2.0 L/min.

| Quantity | 90 %/cm UVT (design water) | 70 %/cm UVT (NSF/ANSI 55 test water) |
| --- | --- | --- |
| Absorption coefficient α | 0.105 /cm | 0.357 /cm |
| Light left after one pass of 20 cm | about 12 % | under 0.1 % |
| UV-C absorbed by water | about 0.28 W | about 0.33 W |
| Average dose | about 80 mJ/cm² | about 28 mJ/cm² |
| **Reduction equivalent dose (x 0.5)** | **about 40 mJ/cm²** | **about 14 mJ/cm²** |
| Requirement | R2 met, no margin | **R3 not met**; below even the Class B level of 16 mJ/cm² |

Clearer water is much easier to treat because less of the light is wasted heating the water itself. To reach 40 mJ/cm² at 70 %/cm UVT the reactor would need about 2.9 times the UV output (about 17 LEDs and 40 W) or would have to limit flow to about 0.7 L/min. Both are listed as options below.

The dose target is the NSF/ANSI 55 Class A dose level for context only ([Fresh Water Systems](https://www.freshwatersystems.com/blogs/blog/nsf-class-a-and-class-b)). 40 mJ/cm² inactivates common bacteria and *Cryptosporidium* by several logs, but adenovirus needs about 186 mJ/cm² for 4 logs ([EPA UV toolkit](https://www.epa.gov/system/files/documents/2022-05/uv-toolkit-815-B-21-007_0.pdf)), so LumaFlow is not a full virus barrier. The reactor efficiency of 0.5 is the largest uncertainty; published flow-through LED reactors show that LED layout, reflectors and mixing change it a great deal ([flow-through reactor efficiency](https://www.sciencedirect.com/science/article/abs/pii/S2214714420306966); [cylindrical reactor optimization](https://www.sciencedirect.com/science/article/abs/pii/S2213343724004962)).

### Dose monitor

The photodiode sees the light left after the full water column. At 90 %/cm UVT that is about 12 % of the output; at 70 %/cm it is under 0.1 %. A factor of more than 100 between good and poor water gives the controller a clear signal. A fouled window, aged LEDs or poor water all reduce the signal, so every failure reads as low dose, which is the safe direction. At TRL 3 the sensor reading and flow must be mapped to dose by calculation; at TRL 4 by biodosimetry.

### Power and energy

Assumptions: LED driver efficiency 90 %, valve holding power 4 W, controller 0.6 W while active, adapter efficiency 88 %, standby 0.3 W, and about 9 min of LED on-time per day (15 L at 2 L/min plus 5 s run-on on 20 draws).

![Power flow](../media/flow.png)

*Figure 4. Power flow while water runs at 2 L/min. All values are estimates in watts.*

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| LED electrical power | about 13.0 W | |
| Power from mains while flowing | about 21.6 W | R9 met (25 W) |
| Standby power | about 0.3 W | R9 met (0.5 W) |
| Daily energy | about 3 Wh flowing plus 7 Wh standby, about 10 Wh | |
| Yearly energy | about 3.8 kWh | |
| Mercury unit of 10 to 25 W running all day, for comparison | about 90 to 220 kWh per year | Assumed typical lamp power |
| LED on-time | about 55 h per year | Rated life of 5,000 to 10,000 h is not the limit; aging and switching are unverified |

### Heat

The LEDs turn about 12.6 W into heat. Because they run only while water flows, the lower end cap and heat spreader pass most of that heat into the passing water, which warms by only about 0.09 K (12.6 W / (33.3 g/s x 4.18 J/(g·K))). The finned sink covers the 5 s run-on and any fault that leaves the LEDs on without flow; the controller must switch the LEDs off if the flow sensor reads zero for more than 5 s. The LED board temperature (R10) is unverified.

### Window and pressure

Assumptions: 8 bar (0.8 MPa, 116 psi) working pressure, window unsupported over a 26 mm diameter, simply supported edge, and an allowable tensile stress of about 7 MPa (1,000 psi) for fused quartz, a common design value to be checked against supplier data. The peak stress in a simply supported circular plate is about 1.19 x p x r² / t².

| Window thickness | Peak stress at 8 bar | Result |
| --- | --- | --- |
| 3 mm | about 18 MPa | Too high |
| 6 mm | about 4.5 MPa | R7 met on estimate |

A 6 mm window is therefore proposed. A pressure-limiting valve upstream is recommended where supply pressure can exceed 6 bar.

### Size and cost

The massing model fits in about 240 x 75 x 325 mm without the adapter, inside the R14 envelope. Parts cost about $217 (Table 1 and `bom/bom.csv`); the six LEDs are about a quarter of it. **R16 ($200) is not met.**

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Axial LED head instead of LEDs around a quartz sleeve.** The scaffold listed a quartz sleeve, as in a mercury unit. Putting the LEDs at one end and shining along the tube uses few LEDs, needs only a small flat window and a short, simple PTFE reflector, and lets the water cool the LEDs. The alternative is a quartz tube with LED strips along its length, which gives a more even dose but needs many more LEDs and a long, fragile quartz tube. Recommendation: axial head with a window.
- **275 nm LEDs.** 275 nm gives the most UV-C output per dollar today, while 265 nm is closer to the germicidal peak but costs more per milliwatt ([Tech-LED](https://tech-led.com/uv-c-leds-for-disinfection-and-sterilization-component-selection-265-280-nm/)). Recommendation: 275 nm, revisit at TRL 3 with current prices.
- **Design water quality and dose target.** Option A: design for 90 %/cm UVT with an alarm that closes the valve below the dose set point, and state that R3 is not met. Option B: design for the NSF/ANSI 55 test condition of 70 %/cm UVT at 2 L/min, with about 17 LEDs, about 40 W and about $100 more in LEDs alone. Option C: keep six LEDs and let the controller limit flow to about 0.7 L/min when UVT is low, which needs a proportional valve. Recommendation: Option A, with Option C as a later upgrade.
- **Flow sensor as the switch.** A Hall-effect flow sensor gives both the on signal and the flow rate for the dose estimate. A reed-type flow switch is simpler but gives no rate. Recommendation: Hall-effect sensor.
- **Normally closed outlet valve.** The valve makes the unit fail closed on alarm and on power loss, which NSF/ANSI 55 Class A permits as an alternative to alarm-only. Dropping it saves about $12 and 4 W but leaves only an alarm. Recommendation: keep the valve.
- **Vertical mounting, flow upward.** Upward flow purges air bubbles, which would otherwise gather under the window and block light. Recommendation: vertical, LEDs at the bottom.
- **External 24 V adapter.** Keeps mains voltage away from the wet cabinet. Recommendation: certified adapter plugged into a GFCI or RCD-protected outlet.
- **Budget.** The parts cost is about $17 over `budget_usd` of $200. Options are in `docs/REVIEW.md`; `project.yaml` is unchanged.

## Safety

> **Safety:** LumaFlow emits UV-C light that injures eyes and skin, sits under pressure next to mains power in a wet cabinet, and is meant to make water safe to drink. It is a research and educational prototype, not a certified water treatment device. Do not rely on it as the only barrier for drinking water.

- **UV-C exposure.** UV-C burns the cornea and skin within seconds to minutes at close range and is invisible. The stainless tube and end caps block all UV-C in normal use. An interlock on the enclosure lid and on the LED head must cut LED power when either is opened, and no one should look into the bore or window while the LEDs can run. Any bench testing needs UV-C blocking eyewear and covered skin.
- **False sense of safety.** UV does not remove chemicals, lead, nitrate or particles, leaves no residual disinfectant, and works poorly in cloudy or iron-rich water. A dose below target must stop the water, not only warn. Pipework and the faucet downstream of the reactor can grow biofilm; they need occasional cleaning. The first water drawn after a long idle period sits in untreated downstream pipe.
- **Pressure and leaks.** Supply pressure acts on the window, caps and tubing. A cracked window would flood the LED head; the board runs at 24 V, so the hazard is short circuit and loss of treatment rather than shock. The fuse on the 24 V input and a leak check in the fault logic are required. Fit a shutoff valve upstream and a pressure-limiting valve where supply can exceed 6 bar.
- **Electrical.** Mains is confined to the certified adapter, which should plug into a GFCI or RCD-protected outlet above any likely water level in the cabinet.
- **Heat.** LEDs left on without flow would overheat. The controller must switch them off when flow stops, and the heat sink must survive the 5 s run-on.
- **Materials.** UV-C degrades most plastics; only PTFE, quartz and metal may see it. Every wetted part must be food-contact grade.

## Open questions

- [ ] Confirm the design water quality and dose target (Options A to C above) with Amish.
- [ ] Estimate the reactor efficiency more carefully for this axial, laminar geometry, including PTFE reflectance at 275 nm and the effect of an inlet flow mixer.
- [ ] Map the photodiode reading and flow rate to dose, and set the alarm threshold with margin.
- [ ] Check LED board temperature with water cooling and during the run-on (R10).
- [ ] Check pressure drop across the flow sensor, valve and restrictor (R8).
- [ ] Choose the end cap material (acetal or 316 stainless) and confirm food-contact approval of every wetted part.
- [ ] Decide whether a brief LED pulse during long idle periods is worth adding to limit growth in the reactor.
- [ ] Close the $17 cost gap or propose a budget change.
- [ ] Find a partner with real well-water UVT data for later testing.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
