"""LumaFlow product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.

Every product part is components(CHOSEN) from cad/src/model.py as it is (option A at detail level D3): the
316 tube with its welded sensor boss and weld bead, PTFE liner, quartz window on its PTFE washer, expanded
PTFE gasket, retaining ring and its six screws, LED board with six LEDs, heat sink and spreader ring, both end
caps, four tie rod studs with washers and acorn nuts, the photodiode holder and amplifier, the flow sensor and
valve on their saddles with heat-set inserts and screws, the stem adaptors, the bracket plate with wall screws,
both pipe clamps with liners, studs and nuts, the enclosure with its lid, UV level bar, gland, socket,
controller boards and labels, and the LED head cable and plug. Only the site is added, as context parts named
"(site)": a kitchen sink base cabinet with its floor, back and left side, toe kick, the countertop with a
stainless sink bowl and the drinking-water tap, the cold-water angle stop, the supply and tap lines, the DC
cord into the cabinet back, the kitchen wall and floor, and a 1.75 m person standing at the counter for scale
("(scale)").

The kitchen floor is z = 0 (the model is lifted by LIFT so the cabinet floor top sits 120 mm above it). The
site is indoors, so the hero is a studio render of the product in its cabinet rather than a kit 1.9 outdoor
scene (deviation recorded in docs/REVIEW.md, proposed, awaiting Amish).
UV-C is never shown as visible light; only the UV level bar glows. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR
FABRICATION.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot, Sphere, Torus, Cylinder  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "LumaFlow: under-sink UV-C LED water disinfection reactor for a drinking-water tap"
LIFT = 120.0 + M.PARAMS["floor_gap"]          # model z = 0 (bottom of the fins) sits 145 mm above the kitchen floor

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -38,
     "note": "Product in its real site, from the front right and a little above (about 22 deg elevation): the reactor "
             "in its pipe clamps on the bracket plate inside a kitchen sink base cabinet (doors and right side left out), "
             "flow sensor and valve at left, enclosure with the lit UV level bar at right, the tap above on the counter; "
             "a 1.75 m person standing at the counter for scale"},
    {"name": "studio", "groups": ["shell", "internal"], "explode": False, "el": 20, "az": -35,
     "note": "Studio render of the unit alone from the front right, slightly above (about 20 deg elevation): dose "
             "sensor boss and amplifier, enclosure lid with the UV level bar, acorn nuts on the tie rods"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): every part of the detailed model "
             "pulled apart along its fitting direction, fasteners with the parts they hold, 24 V adapter"},
]


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _xcyl(r, x0, x1, y=0.0, z=0.0):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def _ycyl(r, y0, y1, x=0.0, z=0.0):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def site():
    """Kitchen sink base cabinet and the room around it (context). Kitchen floor at z = 0."""
    P = M.PARAMS
    L = M.levels()
    out = []
    ctx = lambda n, sh, mat: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))
    WY = P["bracket_y"][1]                        # cabinet back face, model y
    zf = 120.0                                    # cabinet floor top above the kitchen floor
    ctx("Kitchen floor", _box(-1500, 1500, -2500, 400, -60, 0), "concrete")
    ctx("Kitchen wall", _box(-1500, 1500, WY + 18, WY + 118, -60, 1800), "insulated_white")
    ctx("Cabinet back panel", _box(-318, 318, WY, WY + 18, zf - 18, 870), "plywood")
    ctx("Cabinet floor panel", _box(-318, 318, -560, WY, zf - 18, zf), "plywood")
    ctx("Cabinet left side", _box(-336, -318, -560, WY + 18, 0, 870), "plywood")
    ctx("Toe kick", _box(-318, 318, -500, -482, 0, zf - 18), "plywood")
    top = _box(-340, 1100, -600, WY + 18, 870, 900)
    top = top - _box(-280, -20, -470, -80, 860, 910)
    ctx("Countertop", break_edges(top, 2.0), "concrete")
    bowl = _box(-280, -20, -470, -80, 690, 870) - _box(-278.8, -21.2, -468.8, -81.2, 691.2, 880)
    ctx("Sink bowl, stainless", bowl + (_box(-290, -10, -480, -70, 900, 901.2) - _box(-280, -20, -470, -80, 899, 903)), "stainless")
    tx, ty = 40.0, -40.0
    tap = _zcyl(22, 900, 905, tx, ty) + _zcyl(12, 905, 1080, tx, ty)
    tap = tap + (Pos(tx - 45, ty, 1080) * Rot(90, 0, 0) * Torus(45, 7) & _box(tx - 100, tx + 10, ty - 20, ty + 20, 1080, 1140))
    tap = tap + _zcyl(7, 1040, 1080, tx - 90, ty) + _xcyl(4, tx + 10, tx + 40, y=ty, z=1020)
    ctx("Drinking-water tap, chrome", tap, "stainless")
    xs = -P["cap_d"] / 2 - 62
    zi, zo = L["z_in"] + LIFT, L["z_out"] + LIFT
    sx = -200.0
    sup = _xcyl(4.76, sx, xs - 40, z=zi) + _zcyl(4.76, zi, zi + 30, x=sx) + Pos(sx, 0, zi) * Sphere(4.76)
    ctx("Cold supply line", sup, "hdpe_natural")
    stop = Pos(sx, 0, zi + 44) * Sphere(10.0) + _zcyl(6.5, zi + 30, zi + 44, x=sx) + _ycyl(7.0, 0, WY, x=sx, z=zi + 44)
    stop = stop + _ycyl(16.0, WY - 3, WY, x=sx, z=zi + 44) + _box(sx - 11, sx + 11, -28, -20, zi + 40, zi + 48)
    ctx("Angle stop valve, chrome", stop, "stainless")
    tl = _xcyl(4.76, -170, xs - 40, z=zo) + _zcyl(4.76, zo, 890, x=-170) + Pos(-170, 0, zo) * Sphere(4.76)
    tl = tl + _ycyl(4.76, ty, 0, x=-170, z=890) + _xcyl(4.76, -170, tx, y=ty, z=890) + Pos(-170, 0, 890) * Sphere(4.76)
    ctx("Line to the drinking-water tap", tl, "hdpe_natural")
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    gx = EX0 - 12.5
    ym = (EY0 + EY1) / 2
    cord = _xcyl(2.6, gx - 30, gx, y=ym, z=EZ0 + 20 + LIFT) + _zcyl(2.6, zf + 3, EZ0 + 20 + LIFT, x=gx - 30, y=ym)
    cord = cord + _ycyl(2.6, ym, WY + 18, x=gx - 30, z=zf + 3)
    ctx("DC cord into the cabinet back", cord, "epdm")
    try:
        import context_parts
        man = Pos(650, -950, 0) * Rot(0, 0, 10) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:    # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        q = dict(p)
        q["shape"] = Pos(0, 0, LIFT) * p["shape"]
        if q["group"] not in ("shell", "internal", "accessory"):
            q["group"] = "shell"
        if q["name"] == "UV level bar light-pipe segments":
            q["material"] = "emissive"; q["color"] = "#2DD4BF"
        out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "context" for p in ps), "context;",
          sum(not p["shape"].is_valid for p in ps), "invalid")
