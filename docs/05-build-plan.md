---
doc_id: LMF-BLD-001
title: LumaFlow prototype build plan
project: LumaFlow
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan with pictures by component and step; design made constructable (LMF-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Decisions of 2026-10-02 carried in: PTFE window washer, LED head cable and plug with interlock loop, five-segment UV level bar, labels; first checks for the interlock and the bar; pictures regenerated"
---

# LumaFlow prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order.*

The prototype is one LumaFlow unit hung on a plate under a kitchen sink: a stainless tube, lined with white PTFE, standing upright between two round end caps, with six UV-C LEDs on a finned heat sink under a quartz window at the bottom, a light sensor in the tube wall, a flow sensor on the way in, a shutoff valve on the way out and a small printed box for the electronics. Water flows up the tube while the LEDs shine up it. Figure 1 shows the 25 components in the order you make or fit them. Eleven are made: the bracket plate, two printed saddles, the stainless lower end cap, the window retaining ring, the drilled heat sink and its spreader ring, four tie rod studs, the tube with its welded sensor boss, the PTFE liner, the acetal upper end cap, the photodiode holder and the printed enclosure. The two caps, the tube boss and the holder need a machine shop with a lathe, a mill and a TIG welder; the rest is sawing, drilling, tapping and 3D printing. Everything else is bought: the window, the PTFE window washer, LEDs, the LED head cable and plug, seals, labels, pipe clamps, push-fit fittings, flow sensor, valve, controller modules and the 24 V adapter. The parts cost about $416 from the bill of materials.

> **Safety:** LumaFlow makes UV-C light, which burns the eyes and skin within seconds to minutes and cannot be seen. Never power the LEDs unless the LED head is on the cap and plugged in, the reactor is closed and the enclosure lid is shut, and wear UV-C blocking eyewear and cover your skin for any bench work with the LEDs. The reactor holds mains water pressure next to electronics: leak test it before any wiring is connected (section 6). Only the certified adapter sees mains voltage; it plugs into a GFCI or RCD-protected outlet. LumaFlow is a research and educational prototype, not a certified water treatment device; do not drink water from it or rely on it as a barrier.

## 2. What changed to make it buildable

The concept showed what the reactor does; some of its parts could not be fitted, fixed, sealed or made as drawn. Each change below keeps what the reactor does (the same water column, LEDs, window, sensor position, flow and size), and all of them are recorded in decision record LMF-DDR-003, which Amish accepted on 2026-10-02 with the window seat changed to a PTFE washer. The last three rows were decided by Amish on 2026-10-02.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Quartz window | Trapped in a pocket narrower above and below than the window; no seal | Pocket open from below; the window goes in from below onto a rubber gasket and is held, on a thin PTFE washer, by a stainless ring with six screws (Figure 10) | It can be fitted and taken out, it seals, and the quartz never bears on bare metal |
| Tie rods | Ending on top of the heat sink with nothing to hold them | Studs screwed into the stainless lower cap, nuts on the upper cap (Figures 15 and 18) | The rods hold the caps together on their own |
| LED head | No fixing; no way out for the LED cable | Four screws from below between the fins into the lower cap; a slot for the cable (Figure 12) | The head comes off for service without opening the water side |
| Tube ends | Butted on flat cap faces, no seal or location | Each end sits 2 mm into a seat on a rubber O-ring; a spigot locates the lower end (Figure 15) | Sealed and located at both ends |
| Upper end cap | 30 mm tall with a 3 mm plastic roof over the water | 40 mm tall with a 13 mm roof (Figure 18) | The 3 mm roof would have been stressed near its breaking point at full pressure |
| Water ports | Plain holes, no thread; 10 mm stubs of tube to the sensor and valve | Threaded ports with stainless stem adaptors that plug straight into the sensor and valve (Figure 25) | Bought fittings, nothing to kink |
| Light sensor mount | A saddle with no clamp; an unsealed window rod | A boss welded to the tube; a small window pressed onto a washer by a screwed holder (Figure 20) | One sealed, welded joint on the pressure wall |
| Wall bracket | Closed rings that only fit before the caps went on; a shelf with no fixing; no wall holes | A drilled aluminium plate, two bought pipe clamps that open, the enclosure screwed to the plate, two saddles for the sensor and valve (Figures 2 to 6) | Every joint is a screw into a tapped hole, and the reactor lifts out after opening two clamps |
| Enclosure | One closed box | A body and a screw-on lid that works the lid switch (Figure 21) | The lid interlock needs a lid |
| Height above the floor | Heat sink fins on the cabinet floor | 25 mm of air under the fins | The fins need free air to cool |
| LED head interlock | Named but not shown | A short cable from the LED head to a plug under the enclosure; two of its wires form a loop that the controller watches (Figure 24) | Unplugging the head stops the LEDs, and the cable is too short for the head to come off while plugged in |
| Status display | One status light in the lid | A five-segment UV level bar in the lid (Figure 22) | Shows the UV level against the alarm point at a glance; it is not a dose reading |
| Labels | None | UV-C warning labels on the lower cap and inside the lid; a product label on the enclosure side | Warn anyone who opens the unit, and name it |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing in front of the unit, facing the cabinet wall; the plumbing is on the left and the electronics on the right. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4. Wear gloves when handling the PTFE liner and the quartz window, and keep both in clean bags until they are fitted.

### 3.1 Bracket plate

![Figure 2. Making sketch of the bracket plate](../cad/drawings/LMF-DWG-101.png)

*Figure 2. Bracket plate making sketch (LMF-DWG-101).*

![Figure 3. Hole positions on the bracket plate](05-build-plan/plate-holes.png)

*Figure 3. Every hole, full size figures, measured across from the left edge and up from the bottom edge.*

**What it is and what it is made from.** The flat plate that everything hangs on and that screws to the cabinet wall. Aluminium plate 6 mm thick, 6061 or 5083 class, 242 x 270 mm.

**How to make it.**

1. Cut the blank to 242 x 270 mm, square. File the edges and round the corners to about 3 mm. Mark one face as the front (the reactor side).
2. Mark every hole from Figure 3, across from the left edge and up from the bottom edge. The reactor's centre line is 112 from the left edge.
3. Clamp studs: two holes on the centre line, 65 and 195 up. Drill 6.8 mm and tap M8.
4. Enclosure: four holes 182 and 226 across, 78 and 192 up. Drill 3.3 mm and tap M4.
5. Saddles: four 4.5 mm holes 25 across, at 15, 29, 241 and 255 up. Countersink them on the back face.
6. Wall: four 5.5 mm holes at 7 and 234 across, 10 and 260 up.
7. Deburr every hole on both faces.

**How it fits the parts next to it.** The back face sits flat on the cabinet wall on four screws. The saddles sit on the front face at the left (Figure 5), the pipe clamps on their studs on the centre line (Figure 6) and the enclosure's back flat on the front face at the right (section 3.12).

**Check before moving on.** Lay the saddles and the enclosure on the plate and look through each hole: the holes line up without forcing a screw.

### 3.2 Sensor and valve saddles (make 2)

![Figure 4. Making sketch of the saddle](../cad/drawings/LMF-DWG-102.png)

*Figure 4. Saddle making sketch (LMF-DWG-102).*

**What it is and what it is made from.** A small printed block that steadies the flow sensor (lower saddle) and the valve (upper saddle) so their push-fit joints carry no bending. PETG, printed with 4 walls and 40 % infill.

**How to make it.**

1. Print two blocks 20 wide, 35 deep and 28 tall, with the 20 x 28 back face flat on the bed.
2. Each has a slot 8 wide and 4 deep running from top to bottom, 6 to 10 mm behind the front face, for a cable tie.
3. Press two M4 heat-set inserts 8 deep into the back face, on the centre line, 7 above and 7 below the middle.

**How it fits the parts next to it.**

![Figure 5. Step 1 picture: saddles on the plate](05-build-plan/step-01.png)

*Figure 5. The back face sits flat on the plate, held by two M4 countersunk screws from behind the plate. The flat back of the flow sensor or valve rests on the front face, and one cable tie through the slot holds it.*

**Check before moving on.** The front face is square to the back face; the inserts are flush.

### 3.3 Pipe clamps and studs (bought)

**What it is and what it is made from.** Two rubber-lined pipe clamps for a 65 mm tube, each with an M8 boss, on an M8 x 20 stainless stud. The band and its rubber together must be 3 mm thick or less, because the tie rods pass 2 mm outside the clamp.

**How it fits the parts next to it.**

![Figure 6. Joint 7: pipe clamp on the tube](05-build-plan/joint-07.png)

*Figure 6. The stud screws into the plate with threadlocker and the clamp onto the stud; the rubber grips the tube. The clamp hinges open to let the reactor in and out.*

**Check before moving on.** Each clamp closes on a 65 mm tube with its screw part way in, and opens fully on its hinge.

### 3.4 Lower end cap

![Figure 7. Making sketch of the lower end cap](../cad/drawings/LMF-DWG-103.png)

*Figure 7. Lower end cap making sketch (LMF-DWG-103).*

![Figure 8. Sections of both end caps](05-build-plan/cap-sections.png)

*Figure 8. Both caps cut through the centre and the port, with the parts that sit in them in blue.*

**What it is and what it is made from.** The stainless block at the bottom of the reactor: it holds the window over the LEDs, carries the water inlet, takes the LED heat into the water and anchors the tie rods. 316 stainless round bar, machined to 90 mm across and 30 mm tall. This is machine-shop work; send them Figures 7 and 8.

**How to make it.** Measure heights from the bottom face (the LED side).

1. Turn the bar to 90 mm across and 30 mm long, faces square.
2. Bottom face: a recess 72.4 across and 2 deep for the retaining ring.
3. Window pocket: 58 across, from the recess up to 13.5 from the bottom face. Leave a fine, flat finish on the shoulder at the top of the pocket; the gasket seals on it.
4. Bore: 50 across, from the shoulder through the top face.
5. Top face: a groove from 59 to 65.5 across and 2 deep for the tube end, leaving a 59 mm spigot inside it; in the floor of that groove, an O-ring groove from 60 to 64.8 across and 1.3 deep.
6. Inlet boss: on the left side, a boss 20 across standing out to 55 from the centre, centred 19 up. Tap it 1/4 BSPP, 11 deep, then drill 7 mm through into the bore.
7. Top face: four M5 tapped holes, 12 deep, on an 80 mm circle, at 45° to the inlet.
8. Floor of the ring recess: six M3 tapped holes, 8 deep, on a 65 mm circle, every 60° starting 30° from the inlet.
9. Bottom face: four M4 tapped holes, 10 deep, 16.3 either side of the centre line and 36 to the front and back.
10. Deburr, clean and passivate.

**How it fits the parts next to it.** The window and its ring fit from below (section 3.5); the LED head screws to the bottom face (section 3.6); the tube sits in the top seat (section 3.8). The stainless bore around the bottom 17.5 mm of the water carries most of the LED heat into the water.

**Check before moving on.** The window drops into its pocket by hand; a 59 mm tube end slides over the spigot.

### 3.5 Window retaining ring, with the window, washer and gasket

![Figure 9. Making sketch of the retaining ring](../cad/drawings/LMF-DWG-104.png)

*Figure 9. Retaining ring making sketch (LMF-DWG-104).*

**What it is and what it is made from.** A flat stainless ring that holds the quartz window up against its gasket. 316 stainless sheet 2 mm, laser cut, 72 across outside and 51 across inside. The window (bought) is UV-grade fused silica, 57 across and 10 thick, both faces polished; the gasket (bought or cut) is food-grade EPDM, 57 across outside, 50 inside, 1 thick; the washer (cut) is food-grade PTFE sheet, 57 across outside, 51 inside, 0.5 thick.

**How to make it.**

1. Laser cut the ring with six 3.4 mm holes on a 65 mm circle, every 60° starting at 30°.
2. Countersink the six holes on the bottom face so M3 countersunk screws sit flush.
3. Check the top face is flat and flatten it if the cut left it bowed. The window never touches the metal: the PTFE washer lies between them and spreads the load.
4. Break the inside edge by 0.3 mm and passivate.

**How it fits the parts next to it.**

![Figure 10. Joint 1: the window, clamped from below](05-build-plan/joint-01.png)

*Figure 10. Cut through the centre: gasket above the window, PTFE washer and ring below it, LEDs 1.3 mm under the window. Water pressure pushes the window down onto the washer and the ring.*

With the cap upside down, the gasket goes into the pocket against the shoulder, then the window, then the washer, then the ring, flush with the cap's bottom face. Six M3 x 8 countersunk screws, tightened evenly in a cross pattern to about 0.5 N·m. The ring's 51 mm opening, and the washer's, is the window's free span used in the stress calculation: do not open either out.

**Check before moving on.** The ring is flat within 0.1 mm across a straight edge; the window sits evenly on the washer with no gap you can see against a light.

### 3.6 Heat sink, spreader ring and LED board

![Figure 11. Making sketch of the heat sink and spreader ring](../cad/drawings/LMF-DWG-105.png)

*Figure 11. Heat sink and spreader ring sketch (LMF-DWG-105).*

**What it is and what it is made from.** The LED head: a bought finned aluminium heat sink, 90 x 90 x 30 with nine fins hanging down; a flat aluminium spreader ring, 3 thick, 90 across outside and 45 inside, that carries heat from the sink into the stainless cap; and the bought LED board, 44 across, with six 275 nm LEDs and a temperature sensor, which sits in the ring's hole.

**How to make it.**

1. Sink: drill four 4.5 mm holes through the base in the second gap from the middle on each side, 16.3 either side of the centre and 36 to the front and back. Spot face the underside so the screw heads sit square.
2. Sink: three M3 tapped holes, 5 deep, on a 38 mm circle at 30°, 150° and 270°, for the LED board.
3. Ring: cut from 3 mm aluminium plate, 90 across with a 45 hole; cut an 8 mm slot from the hole to the edge on the right side for the LED cable; drill four 4.5 mm holes matching the sink.
4. Deburr everything.
5. Make up the LED head cable: six wires of 0.25 mm², about 95 mm from the edge of the board to a 6-pin plug, laid flat where they pass through the slot and sleeved as one round cable beyond it. Two wires carry the LED string, two the board's thermistor, and two form the interlock loop: they are joined to each other at the board, so the loop is complete only while the plug is in and the cable is whole. Keep the length: it is what stops the head coming off while plugged in.
6. Fit the LED board in the ring's hole on a thermal pad, with three M3 x 10 low-head screws, its cable out through the slot (assembly step 5).

**How it fits the parts next to it.**

![Figure 12. Joint 2: LED head on the lower cap, from below](05-build-plan/joint-02.png)

*Figure 12. Each M4 screw head sits between two fins; a long hex key reaches it from below.*

The ring lies flat on the sink base and on the cap's bottom face, with a thermal pad on each side. Four M4 x 16 socket screws go up from below through the sink and ring into the cap. The LED head can come off without draining or opening the reactor.

**Check before moving on.** The ring and the board are level within 0.1 mm; the screw heads clear the fins.

### 3.7 Tie rod studs (make 4)

![Figure 13. Making sketch of the tie rod stud](../cad/drawings/LMF-DWG-109.png)

*Figure 13. Tie rod stud making sketch (LMF-DWG-109).*

**What it is and what it is made from.** The four rods that hold the two end caps together against the water pressure. M5 threaded rod in A4 (316) stainless.

**How to make it.**

1. Cut four lengths of 258 from M5 A4 threaded rod.
2. Chamfer and dress both ends so a nut runs on by hand.

**How it fits the parts next to it.** One end screws 12 mm into the lower cap with a drop of medium threadlocker (run it in with two nuts locked together, then take the nuts off). The other end passes through the upper cap and carries a washer and an acorn nut (Figure 18). The studs pass 2 mm outside the pipe clamps.

**Check before moving on.** All four studs stand 246 above the lower cap's top face, square to it.

### 3.8 Reactor tube with its sensor boss

![Figure 14. Making sketch of the reactor tube](../cad/drawings/LMF-DWG-106.png)

*Figure 14. Reactor tube making sketch (LMF-DWG-106).*

**What it is and what it is made from.** The pressure wall of the reactor, which also blocks all UV-C. 316 stainless tube 65 across and 3 thick, 204 long, with a small boss welded on at mid height for the light sensor. Machine-shop and welding work.

**How to make it.**

1. Cut the tube 204 long and face both ends square and smooth: the O-rings seal on the end faces.
2. Turn a boss 22 across and 14 long from 316 bar, and shape one end to the curve of the tube.
3. TIG weld the boss on, centred 105 up from the bottom end, with argon inside the tube. Keep the weld off the bore.
4. After welding, drill 8 mm through the boss and the tube wall. From the outer face of the boss, cut an M12 x 1 thread 5 deep, then a flat-bottomed seat 10.2 across and 3.5 deeper.
5. Pickle and passivate inside and out. The bore must be clean and free of spatter so the liner slides in.

**How it fits the parts next to it.**

![Figure 15. Joint 3: tube end in the lower cap](05-build-plan/joint-03.png)

*Figure 15. Cut through the centre, right side: the tube slides over the spigot and presses its end face onto the O-ring; the liner stands on the spigot.*

Each end sits 2 mm into its cap's seat on a food-grade EPDM O-ring (about 61 mm inside diameter, 1.78 mm section, lightly greased with food-grade silicone grease). The studs press the ends onto the O-rings. The boss faces right, toward the enclosure.

**Check before moving on.** The liner slides through by hand; the boss's axis is square to the tube's axis.

### 3.9 PTFE liner and top disc

![Figure 16. Making sketch of the PTFE liner](../cad/drawings/LMF-DWG-107.png)

*Figure 16. PTFE liner making sketch (LMF-DWG-107).*

**What it is and what it is made from.** The white reflective lining of the water channel, closed at the top. High-reflectance sintered or expanded PTFE tube, 59 across outside and 50 inside, and a 56 x 3 disc of the same material. Its whiteness is what makes the dose; never touch the bore, and handle it only with clean gloves.

**How to make it.**

1. Cut the tube 227 long. Turn the top 25 down to 56 across.
2. Press the disc into the top of the bore, flush with the end; the bore is then 224 deep.
3. Drill the outlet hole 7 across, 215 up from the bottom end, on the left.
4. Drill the sensor hole 8 across, 103 up from the bottom end, exactly opposite the outlet hole.

**How it fits the parts next to it.** It slides into the tube from the top with its sensor hole on the boss, stands on the lower cap's spigot, and its turned top goes into the upper cap's pocket (Figures 15 and 18).

**Check before moving on.** Looking in through the boss, the 8 mm hole is centred.

### 3.10 Upper end cap and outlet sleeve

![Figure 17. Making sketch of the upper end cap](../cad/drawings/LMF-DWG-108.png)

*Figure 17. Upper end cap making sketch (LMF-DWG-108).*

**What it is and what it is made from.** The top of the reactor, with the water outlet. Food-contact acetal round bar, machined to 90 across and 40 tall. It sees no UV-C: the PTFE top disc and liner and a short stainless sleeve in the outlet shield it. The sleeve is 316 tube 9.5 across and 7 inside, 17 long.

**How to make it.** Measure heights from the bottom face (the tube side).

1. Turn to 90 across and 40 tall.
2. Bottom face: a tube seat 65.5 across and 2 deep, with an O-ring groove from 60 to 64.8 across and 1.3 deep in its floor.
3. Liner pocket: 56.2 across, from the seat floor up to 27 from the bottom face. The 13 mm of acetal left above it is the pressure roof; do not go deeper.
4. Outlet boss on the left, 20 across, standing out to 55 from the centre, centred 15 up: tap 1/4 BSPP 11 deep, then bore 9.6 through into the pocket.
5. Four 5.4 mm holes on an 80 mm circle, at 45° to the outlet.
6. Press the stainless sleeve into the 9.6 bore from the thread end until it meets the liner's position (its inner end 28 from the centre).

**How it fits the parts next to it.**

![Figure 18. Joint 4: upper cap, outlet and roof](05-build-plan/joint-04.png)

*Figure 18. Cut through the centre: 13 mm roof over the liner; the stainless sleeve meets the liner so no UV-C reaches the acetal; the stem adaptor screws into the thread.*

The tube's top end sits in the seat on the second O-ring; the liner's turned top fills the pocket; the studs pass through the four holes, each with a washer and an acorn nut.

**Check before moving on.** The liner's turned top enters the pocket by hand; the sleeve's bore lines up with the liner's outlet hole.

### 3.11 Light sensor: window, holder and photodiode

![Figure 19. Making sketch of the photodiode holder](../cad/drawings/LMF-DWG-110.png)

*Figure 19. Photodiode holder making sketch (LMF-DWG-110).*

**What it is and what it is made from.** The dose sensor that looks into the water through the tube wall. A quartz window 10 across and 3 thick (bought), a 0.5 mm EPDM washer, a holder turned from 316 bar, a bought UV-C photodiode in a small metal can, and a bought amplifier.

**How to make it.**

1. Turn the holder from 16 mm 316 bar: an M12 x 1 threaded nose 5 long, then a body 14 across and 8 long with two spanner flats 12 across.
2. Bore 5.4 through for the photodiode can, with a counterbore at the outer end to suit the can's flange. The nose's end face must be flat and smooth.
3. Fix the photodiode in the bore with UV-stable epoxy, its window toward the nose.
4. Mount the amplifier on the outer end and fit its lead.

**How it fits the parts next to it.**

![Figure 20. Joint 5: dose sensor in its boss](05-build-plan/joint-05.png)

*Figure 20. Cut through the boss: the holder's nose presses the window onto the washer on the seat; an 8 mm hole leads to the water.*

The washer and window drop into the boss's seat, the holder screws in by hand and then a quarter turn with a spanner. The amplifier's lead runs to the enclosure's gland.

**Check before moving on.** With the holder screwed into a spare M12 x 1 nut and held to a lamp, no light leaks round the nose.

### 3.12 Electronics enclosure

![Figure 21. Making sketch of the enclosure](../cad/drawings/LMF-DWG-111.png)

*Figure 21. Enclosure making sketch (LMF-DWG-111).*

**What it is and what it is made from.** The box that holds the controller, the LED driver and the valve driver. PETG, printed with 4 walls and 30 % infill: a body open at the front, 60 wide, 44 deep and 130 tall, walls 2.5, and a lid.

**How to make it.**

1. Print the body back face down: four 4.4 mm holes in the back, 8 in from each side and from the top and bottom; an 8 mm hole in the left side, 20 up from the bottom, for the cable gland.
2. In the floor, a 12 mm hole for the LED head's socket, 8 in from the left side and 15 behind the lid's front face.
3. Inside, add bosses with M3 heat-set inserts for the modules and a pocket for the lid reed switch near the front top corner.
4. Print the lid, 60 x 130 x 2.5, with five windows for the UV level bar, each 6 wide and 8 tall, 2 apart, centred across the lid and 22 to 30 below its top edge, and a pocket for the magnet; four M3 screws hold it to the body. Print five segments in clear PETG to fit the windows, standing 1 mm proud of the front; the bar's five LEDs sit behind them.
5. Stick the UV-C warning label inside the lid (Figure 22) and the product label on the right side of the body.

![Figure 22. The lid from inside: UV level bar and UV-C label](05-build-plan/joint-09.png)

*Figure 22. The lid seen from inside: the five bar segments in their windows and the UV-C warning label on the inside face.*

**How it fits the parts next to it.** The back sits flat on the bracket plate, held by four M4 x 10 pan-head screws from inside into the plate's tapped holes. The LED head's socket is screwed into the floor hole from inside. Closing the lid brings the magnet to the reed switch, which closes the LED supply.

**Check before moving on.** With a meter on the reed switch, it closes when the lid is on and opens when the lid is lifted 5 mm.

#### 3.12.1 Wiring

![Figure 23. Block-level wiring](05-build-plan/wiring.png)

*Figure 23. Block-level wiring with wire sizes. No circuit board is laid out at this stage; bought modules stand in for the controller board.*

The controller in the bill of materials is module based. Buy modules that meet this specification:

*Table 2. Modules.*

| Module | What to buy |
| --- | --- |
| Controller | Small microcontroller board with a pulse input, an analog input for the sensor amplifier, a thermistor input, a lid switch input, an input for the LED head's interlock loop, outputs for the drivers and five outputs for the UV level bar, run from a 24 V to 5 V converter |
| LED driver | 350 mA constant-current boost driver for a six-LED string of about 37 V, up to 40 V out from the 24 V input, with a dimming input |
| Valve and display drivers | Logic-level MOSFET module with a flyback diode for the 24 V valve; small buzzer; a five-LED bar module behind the lid's five segments |
| LED head plug and socket | 6-pin circular plug and panel socket about 12 mm across, rated for the LED current |
| Fuse | 1.6 A fuse on the 24 V input |

Wire it like this, with stranded copper and a ferrule on every screw terminal:

1. Adapter to the input fuse: 0.75 mm² (18 AWG).
2. Fuse to the controller's 24 V input and to the valve driver: 0.5 mm² (20 AWG).
3. Fuse to the LED driver through the lid reed switch: 0.5 mm².
4. LED driver to the LED head's socket in the enclosure floor: 0.5 mm². The head's own cable (section 3.6) is six wires of 0.25 mm² (24 AWG) from the socket to the board.
5. LED board thermistor to the controller: 0.25 mm², through the same socket.
6. Interlock loop: the two loop pins of the socket to the controller's interlock input, 0.25 mm². The controller keeps the LED driver off unless the loop is complete, so pulling the plug stops the LEDs.
7. Sensor amplifier to the controller: three-core screened cable through the gland, screen grounded at the controller only.
8. Flow sensor to the controller: 0.25 mm², three-way, through the gland.
9. Valve driver to the valve: 0.5 mm², two-way, through the gland.
10. UV level bar module to the controller's five bar outputs, short leads inside the lid.

![Figure 24. Joint 8: LED head cable and plug](05-build-plan/joint-08.png)

*Figure 24. The LED head's cable runs from the slot in the spreader ring to its plug under the enclosure. It reaches the socket with a little slack, but it is about 39 mm too short for the head to slide clear of the cap while the plug is in.*

**Check before moving on.** Every wire continues end to end; with the adapter unplugged and the lid off, the LED driver's input reads open; the two loop pins of the LED head's plug read a closed circuit, and open as soon as the plug is pulled.

### 3.13 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Quartz window (line 3).** UV-grade fused silica (JGS1 class), 57 across and 10 thick, both faces polished, edges chamfered.
- **LED board (line 4).** Six 275 nm 3535 LEDs, about 60 mW each at 350 mA, on a round 44 mm aluminium-core board with a thermistor and three 3.4 mm holes on a 38 mm circle.
- **Heat sink (line 5).** Aluminium, 90 x 90 x 30, nine fins, gaps of 7.5 mm or more so an M4 socket head fits.
- **Flow sensor (line 8).** Food-grade Hall-effect sensor, 3/8 in push-fit port at each end, flat back, 0.3 to 6 L/min, 15 pulses per second per L/min or more.
- **Photodiode and amplifier (line 9).** SiC UV-C photodiode in a TO-46 can with a transimpedance amplifier.
- **Controller, drivers, LED head plug and socket (line 10).** As Table 2.
- **UV level bar (line 13).** A five-LED bar module behind the five printed segments of the lid.
- **Valve (line 11).** 24 V DC, normally closed, food-grade, 3/8 in push-fit port at each end, flat base, about 0.2 A.
- **Adapter (line 12).** Certified external 24 V DC, 1.25 A adapter, no-load draw 0.1 W or less.
- **Fittings (line 15).** Two stainless push-fit stem adaptors, 1/4 BSPP male to a 3/8 in stem, with bonded sealing washers; 1 m food-grade 3/8 in tube; cold-line tee; 1.2 L/min flow restrictor.

![Figure 25. Joint 6: inlet port, flow sensor and saddle](05-build-plan/joint-06.png)

*Figure 25. The stem adaptor screws into the lower cap's boss; its stem pushes into the flow sensor's port; the saddle and a cable tie steady the sensor. The outlet and valve are the same at the top.*

- **Seals and window washer (line 17).** Food-grade EPDM: the window gasket (section 3.5) and two O-rings about 61 inside diameter, 1.78 section. Food-grade PTFE sheet 0.5 mm for the window washer.
- **Labels (line 19).** Two UV-C warning labels with the optical radiation warning sign and the words "UV-C: do not look into the reactor; disconnect power before removing the LED head"; one product label with the name, the 24 V DC rating and "research and educational prototype, not a certified water treatment device".
- **Pipe clamps (line 18).** As section 3.3.
- **Fixings (line 16).** Stainless: four M5 acorn nuts and washers; six M3 x 8 countersunk; four M4 x 16 socket head; three M3 x 10 low head; four M4 x 10 pan head; four M4 x 10 countersunk; two M8 x 20 studs; four wall screws; food-grade silicone grease, thermal pads and paste, medium threadlocker, cable ties.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: saddles onto the bracket plate

![Step 1](05-build-plan/step-01.png)

Two M4 countersunk screws each, from the back of the plate into the heat-set inserts.

### Step 2: clamp studs and pipe clamps onto the plate, plate onto the wall

![Step 2](05-build-plan/step-02.png)

Studs into the M8 holes with threadlocker, clamps onto the studs, left open. Screw the plate to the cabinet wall (or to a bench board for the first build) on four screws, level, with its bottom edge at least 55 mm above the cabinet floor so the fins will have 25 mm of air under them.

### Step 3: gasket and window into the lower cap, from below

![Step 3](05-build-plan/step-03.png)

Stand the cap upside down on a clean cloth (the picture shows it upright, seen from below). Gloves on. The gasket goes against the shoulder, then the window, polished faces clean.

### Step 4: PTFE washer, retaining ring and cap label

![Step 4](05-build-plan/step-04.png)

The PTFE washer on the window, then the ring on the washer. Six M3 countersunk screws, tightened evenly in a cross pattern to about 0.5 N·m. Do not overtighten: quartz cracks under uneven load. Wipe the front of the cap clean and stick on the UV-C warning label, centred on the front of the cap.

### Step 5: LED board and its cable onto the heat sink

![Step 5](05-build-plan/step-05.png)

Thermal pad on the sink, ring on the pad, board in the ring's hole on its own pad, three M3 screws; the flat part of the cable leaves through the slot on the right.

### Step 6: LED head onto the lower cap

![Step 6](05-build-plan/step-06.png)

Thermal pad on the ring, head up against the cap's bottom face, four M4 x 16 screws from below in the fin gaps. **Hold point:** no gap at the joint, and no light from a torch inside the cap leaks out round the head.

### Step 7: studs and lower O-ring into the lower cap

![Step 7](05-build-plan/step-07.png)

Studs 12 mm in with threadlocker; let it cure. The O-ring, lightly greased, into the groove in the floor of the tube seat.

### Step 8: tube and liner onto the lower cap

![Step 8](05-build-plan/step-08.png)

Slide the liner into the tube first, its sensor hole on the boss. Lower the tube between the studs onto the spigot, boss to the right, until it sits on the O-ring.

### Step 9: upper O-ring and upper cap

![Step 9](05-build-plan/step-09.png)

O-ring into the cap's groove; cap over the studs with its outlet on the left, above the inlet; washers and acorn nuts. Tighten the nuts a quarter turn at a time in a cross pattern until both tube ends are down on their seats, then to about 2 N·m.

### Step 10: outlet sleeve and stem adaptors into the ports

![Step 10](05-build-plan/step-10.png)

Check the sleeve is home against the liner; screw each stem adaptor in with its sealing washer, spanner tight.

### Step 11: dose sensor into the boss

![Step 11](05-build-plan/step-11.png)

Washer and window into the seat, then the holder, hand tight plus a quarter turn. **Hold point:** the leak test of safety stop S2 passes before anything electrical is connected.

### Step 12: reactor into the pipe clamps

![Step 12](05-build-plan/step-12.png)

Lift the reactor into the open clamps, boss to the right, so the fins have at least 25 mm of air under them, and close the clamps until the rubber grips.

### Step 13: enclosure onto the plate

![Step 13](05-build-plan/step-13.png)

Controller modules and the LED head socket already fitted, product label on the right side. Four M4 screws from inside the enclosure into the plate.

### Step 14: plug in the LED head, wire up, close the lid

![Step 14](05-build-plan/step-14.png)

Push the LED head's plug up into its socket under the enclosure and screw its collar home. Wire as Figure 23, the sensor, flow sensor and valve leads through the gland. Lid on with four M3 screws, the bar segments at the top. **Hold point:** safety stop S3.

### Step 15: flow sensor and valve onto the stems and saddles

![Step 15](05-build-plan/step-15.png)

Push each onto its adaptor's stem until it stops, flow arrows pointing up the water path (into the reactor at the bottom, out at the top). One cable tie through each saddle.

### Step 16: water lines and the 24 V adapter

![Step 16](05-build-plan/step-16.png)

Supply line from the cold-line tee, after the sediment pre-filter and the pressure-limiting valve set at 4 bar or less, into the flow sensor; outlet line from the valve to the faucet, with the 1.2 L/min restrictor. Adapter on the cabinet floor, plugged into a GFCI or RCD-protected outlet above any likely water level. **Hold point:** safety stops S4 and S5.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of LMF-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Pressure and leaks | R7, R17 | Reactor alone, ports plugged except one, filled with water and pressed to 8 bar with a hand pump for 10 minutes, LEDs unpowered | No drop on the gauge and no water at the window, tube ends or sensor boss |
| Flow | R1 | Measure the time to fill a 1 L jug at the faucet | 1.2 L/min, give or take 10 % (about 50 s) |
| Pressure drop | R8 | Gauges before the flow sensor and after the valve, restrictor out of the line | 0.5 bar or less at 1.2 L/min |
| Switch on and run-on | R5 | Open the faucet slowly; watch the UV level bar and time it | LEDs on within 0.5 s of flow above 0.3 L/min; off 5 s after flow stops |
| Valve fails closed | R4 | Unplug the adapter with the faucet open | Flow stops at once |
| Lid interlock | R12 | Lift the lid with water flowing | LED driver input goes dead; valve closes; buzzer sounds |
| LED head interlock | R12 | Eyewear on. With water flowing and the LEDs on, pull the LED head's plug from its socket. Then, with the plug back in, the water off and the adapter unplugged, take out the four head screws and try to slide the head clear of the cap | Removing the plug stops the LEDs at once, the valve closes and the buzzer sounds; the cable stops the head before it is clear of the cap |
| UV level bar | R18 | With clear water flowing, add a little instant coffee to the supply | The bar loses segments as the sensor reading falls, and the last one goes out as the alarm trips |
| No UV-C outside | R12 | UV-C indicator card at every joint, the gland and the sensor boss with the LEDs on | No card shows any change |
| Board temperature | R10 | Thermistor reading after 10 minutes of flow at 25 °C water | 50 °C or less |
| Power | R9 | Plug-in power meter, flowing and idle | 25 W or less flowing; 0.5 W or less on standby |
| Sensor signal | R4 | Amplifier output with clear water flowing | A steady reading that falls when a little instant coffee is added to the supply |
| Service | R15 | Time the removal and refitting of the LED head and of the window | 15 minutes or less each |
| Size | R14 | Tape measure | 350 x 150 x 350 mm or less, adapter excluded |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before any part goes on the water.** Every wetted part is food-contact grade: 316 stainless, PTFE, fused quartz, EPDM, acetal. No printed plastic touches the water. Parts cleaned with mild detergent and rinsed.
- **S2. Before anything electrical is connected.** The reactor passes the 8 bar leak test of section 5, with nothing electrical within reach of a spray. The window shows no chip or crack under a bright lamp.
- **S3. Before the LEDs are first powered.** The reactor is closed: LED head on and plugged in, both caps and the sensor holder in. The enclosure lid is shut and the lid switch tested open and closed with a meter. Everyone nearby wears UV-C blocking eyewear; no one looks at the window, boss or ports. Water is flowing, so the LEDs are cooled.
- **S4. Before mains is involved.** Only the certified adapter plugs into the mains, into a GFCI or RCD-protected outlet above any likely water level; no mains wiring is part of this build.
- **S5. Before the unit is left running.** The pressure-limiting valve is fitted upstream and set at 4 bar or less; the lid interlock, the valve's fail-closed check and the board temperature check of section 5 all pass. Never bypass the valve or the interlock.
- **S6. Always.** LumaFlow is a research and educational prototype, not a certified water treatment device. Do not drink water from it or rely on it as a barrier; its dose is calculated, not measured.

## 7. Tools, skills and workspace

**Tools.** Hacksaw or bandsaw; bench vice with soft jaws; bench drill; drills 2.5 to 12 mm; countersink; M3, M4 and M8 taps and tap wrench; files and a deburring tool; scriber, square, steel rule and calipers; straight edge and fine abrasive paper on a sheet of glass; 3D printer that prints PETG; soldering iron for heat-set inserts and wiring; ferrule crimper and wire strippers; multimeter; long-reach 3 mm hex key; spanners for the stem adaptors and the holder; torque screwdriver covering about 0.5 to 2 N·m; hand pressure pump with a gauge to 10 bar and blanking plugs; plug-in power meter; UV-C indicator cards. The two end caps, the tube boss and weld, and the photodiode holder go to a machine shop.

**Skills.** No certified trade is needed for the work in this plan. Basic metalwork (marking out, drilling, tapping), 3D printing, push-fit plumbing, through-hole soldering and crimping. TIG welding of the sensor boss and lathe work on the caps are done by the machine shop. All circuits at the unit are 24 V DC or less; mains stays inside the certified adapter.

**Workspace.** A clean bench about 1.2 x 0.6 m; a metalwork corner kept apart from the optical parts so chips and oil stay off the window and liner; a sink or tray for leak tests; a ventilated place for the printer.

**Personal protective equipment.** Safety glasses for cutting and drilling; UV-C blocking eyewear and covered skin whenever the LEDs can run; clean nitrile gloves for the liner and window; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 500 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/LMF-DWG-101` to `LMF-DWG-111`.
- General arrangement: `cad/drawings/LMF-DWG-001.pdf`, Rev P5.
- Calculations: `docs/04-calcs/01-sizing.md` (LMF-CAL-001 v0.6) and `docs/04-calcs/sizing.py`; window stress [G4], end load [G7], upper cap roof [G8], thermal [F1] to [F3], size and mass [H1, H2], cost [I1], UV level bar [C6]; LED head cable length from the model's interlock check.
- Bill of materials: `bom/bom.csv` and `bom/bom-notes.md`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (LMF-DDR-003), with LMF-DDR-001 and LMF-DDR-002; the register `docs/06-design-decisions.md` (LMF-DEC-001).
- Requirements: `docs/03-requirements.md` (LMF-REQ-001 v0.8).
