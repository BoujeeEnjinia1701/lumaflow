---
doc_id: LMF-PRC-001
title: LumaFlow design precis
project: LumaFlow
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, dose, power, thermal and window estimates, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions (LMF-DDR-001); TRL 3 design (316 lower cap, PTFE-shielded acetal upper cap, tie rods); numbers replaced by LMF-CAL-001, including the dose shortfall
---

# LumaFlow design precis

## Summary

LumaFlow is an inline UV-C LED reactor with a flow-activated switch and a dose monitor, sized for a household tap. Water flows up a PTFE-lined stainless tube with a 25 mm bore while six 275 nm LEDs at the bottom shine up a 246 mm water column through a quartz window. A Hall-effect flow sensor turns the LEDs on only while water runs, and a UV-C photodiode at the top measures the light that reaches the far end, which lets the controller estimate the dose and close a valve if it falls too low.

The TRL 3 calculation note (LMF-CAL-001) changes the picture from TRL 2. A ray trace of the reactor shows that the PTFE wall absorbs about half of the LED output, so the water absorbs only 26 % of it at 90 %/cm UV transmittance. The reduction equivalent dose (RED) at 2 L/min (0.5 gpm) is 14.7 to 19.0 mJ/cm² in clear water, not about 40: **R2 is not met**, and at the 70 %/cm test condition the dose is 6.3 to 7.4 mJ/cm² (**R3 not met**). The unit draws 22.6 W while water flows and 0.21 W on standby. Parts cost $249.00, **$24 over the $225 budget (R16 not met)**. The design choices below are decided by Amish (LMF-DDR-001); the ways to close the dose gap are proposals awaiting Amish in `docs/REVIEW.md`.

![Hero render](../media/hero.png)

*Figure 1. LumaFlow model, mounted on its wall bracket under a sink, with the 24 V adapter on the cabinet floor. The grey 1 L bottle is for scale.*

## How it works

1. **Flow starts.** When someone opens the drinking-water faucet, water enters through the Hall-effect flow sensor (item 8). Its pulses tell the controller that flow has started and how fast it is.
2. **LEDs on.** The controller opens the normally closed outlet valve (item 11) and drives the six 275 nm LEDs (item 4) at 350 mA. At the 0.3 L/min threshold the first sensor pulse can take 0.44 s to arrive, so switch-on takes up to 0.46 s against the 0.5 s target (LMF-CAL-001, D2). LEDs reach full output almost at once, so no warm-up or bypass is needed.
3. **Irradiate.** The LEDs sit 0.8 mm under a 6 mm fused quartz window (item 3) in the 316 stainless lower end cap (item 6). Water enters the lower cap just above the window, flows up the 25 mm bore of the PTFE liner (item 2) and leaves through a 316 insert in the acetal upper cap (item 7). PTFE reflects UV-C diffusely, but in water only about 80 % per bounce, and in a 25 mm bore the light meets the wall far more often than the water absorbs it.
4. **Measure.** A UV-C photodiode (item 9) behind a small window in the PTFE top disc looks down the bore. Its signal falls if the water's UVT drops, the window fouls or the LEDs age. The controller combines that reading with the flow rate to estimate the dose, using a proportional rule that blames every loss of signal on the LEDs, which always under-reads (LMF-CAL-001, C3 and C4).
5. **Alarm and shut off.** If the estimated dose falls below 40 mJ/cm², the flow exceeds its limit, a sensor fails or the enclosure lid is opened, the controller closes the valve, sounds the buzzer and shows a red status light. The valve also closes if power is lost, so no untreated water passes silently. With the dose the reactor delivers today, this rule would close the valve in any water; see Key numbers.
6. **Flow stops.** The LEDs stay on for 5 s after flow stops. The water held in the channel receives a volume-average 37 mJ/cm² at 90 %/cm during the run-on, then everything switches off.

![Cutaway](../media/cutaway.png)

*Figure 2. Cutaway through the reactor axis, looking at the wall. From the bottom: heat sink, LED board, quartz window in the stainless lower cap with the inlet, PTFE-lined tube, PTFE top disc in the acetal upper cap with the outlet insert and the photodiode. The controller board is in the enclosure on the right.*

## Main components

Numbers match the exploded view (Figure 3), `bom/bom.csv` and drawing LMF-DWG-001.

Table 1. Main components.

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Reactor tube | 316 stainless, 40 mm OD x 3 mm wall x 200 mm | Carries pressure and blocks all UV-C |
| 2 | PTFE liner and top disc | Virgin PTFE tube, 25 mm bore, 224 mm long, and a 3 mm top disc with an 8 mm detector hole | Water channel and diffuse reflector; shields the acetal cap |
| 3 | Quartz window | UV-grade fused silica, 32 mm diameter x 6 mm, on a 26 mm seat | 4.46 MPa at 8 bar (LMF-CAL-001, G4) |
| 4 | UV-C LED array | Six 275 nm LEDs on a 16 mm circle, about 60 mW each at 350 mA, on one aluminum-core board | Decision D4 |
| 5 | Heat sink and spreader ring | Finned aluminum sink 64 x 64 x 30 mm and a 60 mm spreader ring to the stainless cap | Water carries 8.7 of 12.7 W of heat |
| 6 | Lower end cap | 316 stainless, 60 mm diameter x 30 mm, LED aperture, window seat, 3/8 in inlet | Stainless because its bore sees full UV-C and it is the water-cooled heat path; proposed, awaiting Amish (LMF-DDR-001 O2) |
| 7 | Upper end cap | Acetal, 60 mm diameter x 30 mm, liner pocket, detector bore, outlet boss | Sees no UV-C behind the PTFE and the 316 insert |
| 8 | Hall-effect flow sensor | Food-grade, 0.3 to 6 L/min, pulse output | Switch and meter (decision D5) |
| 9 | UV-C photodiode and amplifier | SiC photodiode with transimpedance amplifier behind an 8 mm quartz window | Dose monitor |
| 10 | Controller and LED driver | Microcontroller, 350 mA constant-current driver, valve driver, input fuse | Module-based; no custom PCB |
| 11 | Solenoid shutoff valve | 24 V DC, normally closed, food-grade | Closes on alarm or power loss (decision D6) |
| 12 | 24 V power adapter | Certified external adapter, 30 W | The only part at mains voltage (decision D8) |
| 13 | Electronics enclosure | Printed PETG, lid interlock, status light, buzzer | Dry side only |
| 14 | Wall bracket | Backplate with two clamp rings and an enclosure shelf | Holds the reactor vertical (decision D7) |
| 15 | Fittings and outlet insert | 3/8 in push-fit, tee to the cold line, 2 L/min restrictor, 316 outlet insert | Restrictor enforces R1 |
| 16 | Tie rods and hardware | Four M4 316 rods on a 53 mm circle | 251 N each at 8 bar (G7) |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

## Key numbers

Every number in this section comes from LMF-CAL-001, which states the assumptions; the tag in brackets is the line of `docs/04-calcs/sizing.py` that prints it.

### Flow

The channel is 25 mm across and 246 mm long and holds 121 mL [A1, A2]. At 2.0 L/min the mean velocity is 6.79 cm/s, the residence time between the ports 3.39 s and the Reynolds number 1,691, so the flow is laminar [A3, A4]. The entrance length is far longer than the tube [A5], so the true profile lies between plug flow and a parabola; the dose is given for both.

### UV-C dose

Table 2. Dose at 2.0 L/min [B3 to B6].

| Quantity | 90 %/cm UVT (design water) | 70 %/cm UVT (NSF/ANSI 55 test water) |
| --- | --- | --- |
| UV-C entering the water | 80.2 % of 0.36 W | 80.2 % of 0.36 W |
| UV-C absorbed by the water | 26.1 % | 46.2 % |
| Lost at the walls | 49.8 % | 31.6 % |
| Average dose | 19.1 mJ/cm² | 7.4 mJ/cm² |
| **RED (laminar to plug flow)** | **14.7 to 19.0 mJ/cm²** | **6.3 to 7.4 mJ/cm²** |
| Requirement | **R2 not met** | **R3 not met** |

The reactor efficiency (RED over average dose) is 0.77, better than the 0.5 assumed at TRL 2 [B5]; the shortfall is in the optics. Even a PTFE reflectance of 0.90 gives only 16.2 mJ/cm² [B8]. The options in Table 3 (LMF-CAL-001, section J) are proposals awaiting Amish.

Table 3. Ways to reach 40 mJ/cm² at 90 %/cm (laminar RED).

| Option | Result |
| --- | --- |
| Lower the design flow | Met up to 0.64 L/min [J3] |
| More LEDs at 2.0 L/min | 17 LEDs, 53 W, about $99 more; R9 fails [J4] |
| Liner reflectance 0.95 | 17.3 mJ/cm² at 2.0 L/min; met up to 0.78 L/min [J5] |
| 50 mm bore | 30.0 to 41.0 mJ/cm² at 2.0 L/min; window about 9.5 mm [J6-50, J7] |

The dose target is the NSF/ANSI 55 Class A dose level for context only ([Fresh Water Systems](https://www.freshwatersystems.com/blogs/blog/nsf-class-a-and-class-b)). 40 mJ/cm² inactivates common bacteria and *Cryptosporidium* by several logs, but adenovirus needs about 186 mJ/cm² for 4 logs ([EPA UV toolkit](https://www.epa.gov/system/files/documents/2022-05/uv-toolkit-815-B-21-007_0.pdf)), so LumaFlow would not be a full virus barrier even at its target. Published flow-through LED reactors show that the reactor layout changes the delivered dose a great deal ([flow-through reactor efficiency](https://www.sciencedirect.com/science/article/abs/pii/S2214714420306966); [cylindrical reactor optimization](https://www.sciencedirect.com/science/article/abs/pii/S2213343724004962)).

### Dose monitor

The far-end photodiode gives about 2.4 nA at 90 %/cm, 0.08 nA at 80 %/cm and nothing resolvable at 70 %/cm [C1], and its signal falls 4.4 times faster than the dose [C2]. The proportional mapping is safe but, while the reference dose is below 40 mJ/cm², it trips in any water [C3]. A sensor in the tube wall at mid height would see about 20 times more light at 90 %/cm and a usable signal at 70 %/cm [C5]; moving it there is a proposal awaiting Amish. R4 is at risk.

### Power and energy

Table 4. Power and energy [E1 to E5].

| Quantity | Value | Requirement |
| --- | --- | --- |
| LED electrical power | 13.02 W | |
| Power from mains while flowing | 22.6 W | R9 met (25 W) |
| Standby power | 0.21 W | R9 met (0.5 W) |
| LED on-time | 9.2 min/day, 56 h/year | |
| Energy | 8.6 Wh/day, 3.1 kWh/year | |
| Tap-scale mercury unit of 13 to 22 W running all day ([VIQUA spec sheet](https://viqua.com/wp-content/uploads/LIT520326_SpecSheet.pdf)) | 114 to 193 kWh/year | For comparison |

![Power flow](../media/flow.png)

*Figure 4. Power flow while water runs at 2 L/min. All values are estimates from LMF-CAL-001, in watts.*

### Heat

The LEDs turn 12.66 W into heat. The spreader ring passes it into the stainless lower cap, whose wetted bore gives it to the water (8.7 W; the water warms by 0.06 K), and the finned sink gives the rest to the air [F1, F2]. With continuous flow the LED board settles at 48.9 °C for a water-film coefficient of 300 W/(m²·K), but 55.9 °C at 150 W/(m²·K), so R10 is at risk [F3]. An acetal lower cap would let the board reach 85 °C [F5]. With the LEDs stuck on and no flow the board heads for 69 °C [F6]; the controller must switch them off when flow stops.

### Pressure and structure

The unit drops 0.42 bar at 2.0 L/min, not counting the restrictor, against 0.5 bar (R8 at risk, on assumed flow coefficients) [G2]. The 6 mm window carries 4.46 MPa at 8 bar against a design stress of 6.8 MPa (1,000 psi) for fused quartz ([Momentive](https://www.momentivetech.com/materials/fused-quartz-materials/quartz-properties/mechanical-properties)); R7 is met [G4]. A 16 bar spike would give 8.9 MPa [G5], so a pressure-limiting valve upstream is required. Four M4 rods carry the 1,005 N end load [G7].

### Size and cost

The unit is 235 x 72 x 322 mm without the adapter, inside R14 [H1]. Parts cost $249.00 against $225 [I1]; the LEDs ($54), the stainless lower cap ($28) and the photodiode ($22) are the largest lines. **R16 is not met.**

## Key design choices

Items marked "Decided" were decided by Amish on 2026-09-25, going with the recommendation (LMF-DDR-001).

- **Axial LED head with a flat window (Decided, D3).** LEDs at one end shine along the tube through a small flat window; this uses few LEDs and a simple reflector. LMF-CAL-001 shows its weakness: in a narrow bore most light is lost to the wall before the water absorbs it. A wider bore is the strongest lever (Table 3).
- **275 nm LEDs (Decided, D4).** 275 nm gives the most UV-C output per dollar ([Tech-LED](https://tech-led.com/uv-c-leds-for-disinfection-and-sterilization-component-selection-265-280-nm/)); prices to be revisited. The dose calculation takes the organism's response at 275 nm as equal to that at 254 nm, which must be checked.
- **Design water quality and dose target (Decided, D1).** Design for 90 %/cm UVT, alarm and close the valve below 40 mJ/cm², and keep R3 visibly not met; flow limiting in poor water (Option C) is a later upgrade.
- **Flow sensor as the switch (Decided, D5).** A Hall-effect sensor gives both the on signal and the flow rate. A higher pulse rate than the assumed 7.5 Hz per L/min would widen the R5 margin (proposal).
- **Normally closed outlet valve (Decided, D6).** Fails closed on alarm and on power loss.
- **Vertical mounting, flow upward (Decided, D7).** Purges air bubbles from under the window.
- **External 24 V adapter (Decided, D8).** Certified adapter on a GFCI or RCD-protected outlet.
- **Budget (Decided, D2).** `budget_usd` raised to $225; the TRL 3 BOM is $249.00.
- **End caps (Proposed, awaiting Amish).** 316 stainless lower cap for UV-C exposure and heat, acetal upper cap shielded by the PTFE liner, top disc and a 316 outlet insert. Recommendation: confirm.

## Safety

> **Safety:** LumaFlow emits UV-C light that injures eyes and skin, sits under pressure next to mains power in a wet cabinet, and is meant to make water safe to drink. The TRL 3 calculation shows that the concept as drawn delivers well under its target dose, even in clear water. It is a research and educational prototype, not a certified water treatment device. Do not rely on it as a barrier for drinking water.

- **UV-C exposure.** UV-C burns the cornea and skin within seconds to minutes at close range and is invisible. The stainless tube, stainless lower cap and PTFE-shielded upper cap block all UV-C in normal use. An interlock on the enclosure lid and on the LED head must cut LED power when either is opened, and no one should look into the bore or window while the LEDs can run. Any bench work needs UV-C blocking eyewear and covered skin.
- **False sense of safety.** The dose is 14.7 to 19.0 mJ/cm² at 90 %/cm, under the 40 mJ/cm² target. UV does not remove chemicals, lead, nitrate or particles, leaves no residual disinfectant, and works poorly in cloudy or iron-rich water. A dose below target must stop the water, not only warn. Downstream pipework and the faucet can grow biofilm.
- **Pressure and leaks.** Supply pressure acts on the window, caps and tubing; a 16 bar spike would overstress the window. Fit a shutoff valve and a pressure-limiting valve upstream. A cracked window would flood the LED head; the board runs at 24 V, so the hazard is short circuit and loss of treatment rather than shock. The fuse on the 24 V input and a leak check in the fault logic are required.
- **Electrical.** Mains is confined to the certified adapter, which should plug into a GFCI or RCD-protected outlet above any likely water level in the cabinet.
- **Heat.** LEDs left on without flow would reach about 69 °C at the board. The controller must switch them off when flow stops, and a board temperature cut-back is proposed.
- **Materials.** UV-C degrades most plastics; only PTFE, quartz and metal may see it. Every wetted part must be food-contact grade.

## Open questions

- [x] Design water quality and dose target (decided, D1).
- [x] Estimate the reactor efficiency for this axial, laminar geometry (LMF-CAL-001: 0.77; the loss is in the optics).
- [ ] Choose a route to close R2 (Table 3); proposed, awaiting Amish.
- [ ] Move the dose sensor to the tube wall and confirm the mapping; proposed, awaiting Amish.
- [ ] Measure the wetted reflectance of the PTFE liner at 275 nm, and the organism response at 275 nm.
- [ ] Confirm the flow coefficients of the sensor and valve (R8) and the water-film coefficient in the lower cap (R10).
- [ ] Confirm the end cap materials (LMF-DDR-001 O2).
- [ ] Decide whether a brief LED pulse during long idle periods is worth adding to limit growth in the reactor.
- [ ] Close the $24 cost gap or propose a budget change once the R2 route is chosen.
- [ ] Find a partner with real well-water UVT data (LMF-DDR-001 O1).

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: [LMF-DWG-001](../cad/drawings/LMF-DWG-001.pdf).
