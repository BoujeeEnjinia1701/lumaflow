"""LumaFlow concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: Z up along the reactor axis (water flows upward, LEDs at the bottom shine up),
X to the right (-X is the plumbing side), Y toward the cabinet wall (+Y). Units mm.
Part numbers match bom/bom.csv and the exploded view.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all
import math


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def zcyl(r, z0, z1, x=0.0, y=0.0):
    """Vertical cylinder from z0 to z1."""
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def xcyl(r, x0, x1, y=0.0, z=0.0):
    """Cylinder along X from x0 to x1."""
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


# Key dimensions (mm)
TUBE_OD, TUBE_ID = 40.0, 34.0      # stainless reactor tube
BORE = 25.0                         # PTFE liner bore, the water channel
Z_SINK, Z_LED, Z_CAP0 = 30.0, 33.0, 63.0
REACT_L = 200.0                     # irradiated length
Z_CAP1 = Z_CAP0 + REACT_L           # 263
Z_TOP = Z_CAP1 + 30.0               # 293
Z_IN, Z_OUT = 48.0, 278.0           # port heights

# 1 Reactor tube, 316 stainless
tube = zcyl(TUBE_OD / 2, Z_CAP0, Z_CAP1) - zcyl(TUBE_ID / 2, Z_CAP0 - 1, Z_CAP1 + 1)
# 2 PTFE diffuse reflector liner
liner = zcyl(TUBE_ID / 2, Z_CAP0, Z_CAP1) - zcyl(BORE / 2, Z_CAP0 - 1, Z_CAP1 + 1)
# 3 Quartz window, seated in the lower end cap above the LEDs
window = zcyl(16.0, 35.0, 41.0)   # 6 mm thick for 8 bar (see LMF-PRC-001)
# 4 UV-C LED array: six 275 nm LEDs on a round metal-core board
led_board = zcyl(17.0, Z_SINK, Z_LED)
for i in range(6):
    a = math.radians(60 * i)
    led_board = led_board + box(8 * math.cos(a) - 1.8, 8 * math.cos(a) + 1.8,
                                8 * math.sin(a) - 1.8, 8 * math.sin(a) + 1.8, Z_LED, Z_LED + 1.2)
# 5 Heat spreader and finned heat sink under the LED board
sink = box(-32, 32, -32, 32, 24, Z_SINK)
for i in range(7):
    x = -30 + i * 9.8
    sink = sink + box(x, x + 3, -32, 32, 0, 24)
# 6 Lower end cap (inlet port, window seat) and 7 upper end cap (outlet port, sensor port), both with O-ring grooves
cap_lo = (zcyl(25, Z_LED, Z_CAP0) - zcyl(BORE / 2, 41, Z_CAP0 + 1) - zcyl(16.5, Z_LED - 1, 41)
          + xcyl(7, -45, -20, z=Z_IN))
cap_hi = (zcyl(25, Z_CAP1, Z_TOP) - zcyl(BORE / 2, Z_CAP1 - 1, Z_TOP - 6) - zcyl(4, Z_TOP - 7, Z_TOP + 1)
          + xcyl(7, -45, -20, z=Z_OUT))
# 8 Hall-effect flow sensor on the inlet line
flow = box(-85, -45, -14, 14, Z_IN - 14, Z_IN + 14) + zcyl(8, Z_IN + 14, Z_IN + 24, x=-65)
# 9 UV-C photodiode and amplifier on the upper cap, looking down the bore
pd = zcyl(9, Z_TOP, Z_TOP + 14) + box(-10, 10, -6, 6, Z_TOP + 14, Z_TOP + 22)
# 11 Normally closed solenoid shutoff valve on the outlet line
valve = box(-85, -45, -14, 14, Z_OUT - 14, Z_OUT + 14) + zcyl(14, Z_OUT + 14, Z_OUT + 44, x=-65)
# 13 Electronics enclosure with status light, buzzer and lid interlock (right of the reactor)
EX0, EX1, EY0, EY1, EZ0, EZ1 = 40.0, 100.0, -22.0, 22.0, 100.0, 230.0
encl = box(EX0, EX1, EY0, EY1, EZ0, EZ1) - box(EX0 + 2.5, EX1 - 2.5, EY0 + 2.5, EY1 - 2.5, EZ0 + 2.5, EZ1 - 2.5)
encl = encl + xcyl(4, EX0 - 12, EX0, y=0, z=EZ0 + 20) + box(58, 82, EY0 - 3, EY0, EZ1 - 30, EZ1 - 18)
# 10 Controller and LED driver board inside the enclosure (sits in the +Y half so the cutaway shows it)
board = box(EX0 + 6, EX1 - 6, 4, 6, EZ0 + 8, EZ1 - 8) + box(EX0 + 12, EX0 + 30, -4, 4, EZ0 + 30, EZ0 + 48) \
    + box(EX0 + 30, EX1 - 12, -2, 4, EZ0 + 70, EZ0 + 90)
# 12 24 V DC power adapter, on the cabinet floor
adapter = box(130, 225, -30, 20, 0, 34) + xcyl(3, 100, 130, y=-5, z=17)
# 14 Wall bracket: backplate and two clamp rings around the reactor tube
bracket = box(-40, 110, 34, 40, 80, 250)
for z in (95.0, 225.0):
    bracket = bracket + (zcyl(26, z - 8, z + 8) - zcyl(TUBE_OD / 2, z - 9, z + 9)) + box(-6, 6, 24, 34, z - 8, z + 8)
bracket = bracket + box(EX0, EX1, EY1, 34, 150, 180)
# 15 Fittings and tubing: supply line into the flow sensor and outlet line to the faucet
fittings = xcyl(5, -125, -85, z=Z_IN) + xcyl(5, -125, -85, z=Z_OUT)

parts = [
    Part("Reactor tube, 316 stainless", tube, "#A8B0B8", 1, (0, 0, 0)),
    Part("PTFE reflector liner", liner, "#F3F4F6", 2, (0, -120, 70)),
    Part("Quartz window", window, "#7DD3FC", 3, (0, 0, -115)),
    Part("UV-C LED array, 6 x 275 nm", led_board, "#7C3AED", 4, (0, 0, -160)),
    Part("Heat spreader and heat sink", sink, "#6B7280", 5, (0, 0, -210)),
    Part("Lower end cap, inlet port", cap_lo, "#1F2937", 6, (0, 0, -55)),
    Part("Upper end cap, outlet and sensor ports", cap_hi, "#374151", 7, (0, 0, 55)),
    Part("Hall-effect flow sensor", flow, "#0F766E", 8, (0, 0, -55)),
    Part("UV-C photodiode and amplifier", pd, "#D4A017", 9, (0, 0, 115)),
    Part("Controller and LED driver", board, "#15803D", 10, (70, 0, 0)),
    Part("Solenoid shutoff valve", valve, "#C2410C", 11, (0, 0, 55)),
    Part("24 V power adapter", adapter, "#4B5563", 12, (80, 0, -120)),
    Part("Electronics enclosure", encl, "#E5E7EB", 13, (140, 0, 0)),
    Part("Wall bracket", bracket, "#9CA3AF", 14, (0, 120, 0)),
    Part("Fittings and tubing", fittings, "#60A5FA", 15, (-30, 0, -170)),
]

# Context for scale (hero only): a 1 L bottle standing on the same cabinet floor
bottle = zcyl(42, 0, 230, x=290, y=0) + zcyl(26, 230, 255, x=290) + zcyl(16, 255, 275, x=290)
context = [Part("1 L water bottle", bottle, "#C8CDD3")]

if __name__ == "__main__":
    render_all(
        parts, project="LumaFlow", title="Inline UV-C LED reactor concept", dwg_no="LMF-DWG-010",
        date="2026-09-25",
        key_figures=["2 L/min (0.5 gpm) design flow, 25 mm bore x 200 mm",
                     "6 x 275 nm LEDs, about 0.36 W UV-C (estimate)",
                     "About 40 mJ/cm² at 90 % UVT, about 14 at 70 % (estimate)",
                     "About 22 W while water flows, 0.3 W standby (estimate)",
                     "About $217 in parts, over the $200 budget (indicative)"],
        scale_figure=False, context=context,
        cut_exclude=("Wall bracket", "24 V power adapter"),
        flow={"title": "power flow while water runs at 2 L/min (all values estimates, W)", "unit": "W",
              "stages": [("Mains input", 21.6), ("24 V DC bus", 19.0), ("LED array", 13.0),
                         ("UV-C light out", 0.36), ("UV absorbed in water", 0.28)],
              "losses": [(0, "Adapter loss", 2.6), (1, "Driver, valve, controller", 6.0),
                         (2, "Heat into sink and water", 12.6), (3, "Wall and window loss", 0.08)]},
    )
