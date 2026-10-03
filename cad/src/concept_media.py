"""LumaFlow concept media (TRL 3, design revised by LMF-DDR-002, made constructable by LMF-DDR-003, decisions of 2026-10-02 carried in), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Writes media/hero.png, cutaway.png, exploded.png, flow.png, concept-blueprint.*, model.glb and viewer.html
with .kit/concept.py. Figures are those printed by docs/04-calcs/sizing.py (LMF-CAL-001); tags in brackets.
Massing-plus model; not for fabrication.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Cylinder, Pos  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import PARAMS, build_parts  # noqa: E402

GROUP = {10: "Controller, driver, LED head cable", 13: "Enclosure, lid and UV level bar", 19: "Labels", 14: "Bracket plate and saddles", 16: "Tie rods and screws",
         17: "Window ring, washer, gasket, O-rings"}   # one legend name per BOM line
parts = [Part(GROUP.get(bom, name), shape, color, bom, explode) for _, name, shape, bom, color, explode in build_parts()]


def zcyl(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


# Context for scale (hero only): a 1 L bottle standing on the same cabinet floor
fz = -PARAMS["floor_gap"]
bottle = zcyl(42, fz, fz + 230, x=300) + zcyl(26, fz + 230, fz + 255, x=300) + zcyl(16, fz + 255, fz + 275, x=300)
context = [Part("1 L water bottle", bottle, "#C8CDD3")]

if __name__ == "__main__":
    render_all(
        parts, project="LumaFlow", title="Inline UV-C LED reactor concept", dwg_no="LMF-DWG-010", rev="P5",
        date="2026-10-02",
        key_figures=["1.2 L/min (0.32 gpm), 50 mm bore x 242 mm channel",
                     "6 x 275 nm LEDs, 0.36 W UV-C; 53 % absorbed by water",
                     "RED 51 to 75 mJ/cm² at 90 % UVT: R2 (40) met",
                     "22.6 W while flowing, 0.21 W standby (estimates)",
                     "$416 estimated; value-engineering target $340"],
        scale_figure=False, context=context,
        cut_exclude=("Bracket plate", "Sensor and valve saddles", "Pipe clamps", "24 V power adapter"),
        flow={"title": "power flow while water runs at 1.2 L/min (estimates from LMF-CAL-001 v0.6, W)", "unit": "W",
              "stages": [("Mains input", 22.6), ("24 V DC bus", 19.9), ("LED array", 13.0),
                         ("UV-C light out", 0.36), ("UV-C into water", 0.31), ("Absorbed by water", 0.19)],
              "losses": [(0, "Adapter", 2.7), (1, "Driver, valve, MCU", 6.9),
                         (2, "LED heat", 12.66), (3, "Seat, Fresnel", 0.05),
                         (4, "Walls, window", 0.12)]},
    )
