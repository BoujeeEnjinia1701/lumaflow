"""LumaFlow product appearance model (build123d), TRL 3, constructable design.

Finished-product look for photoreal renders of the constructable design (LMF-DDR-003, accepted
2026-10-02) with the decisions of 2026-10-02 carried in (LMF-DEC-001): brushed 316 reactor tube
with its welded sensor boss and photodiode holder, tie rod studs under acorn nuts, stainless lower
cap with a UV-C warning label, dark acetal upper cap, anodized heat sink and spreader ring, the LED
head cable to its plug under the enclosure, a flow switch and a solenoid valve on stem adaptors and
saddles, the drilled aluminium bracket plate with two rubber-lined pipe clamps, and the electronics
enclosure with its lid, five-segment UV level bar and product label. Inside: PTFE liner, quartz
window on its PTFE washer, retaining ring and the LED board. Context: a short section of cabinet wall
and floor, the DC cord entering the cabinet wall (decision 8; the 24 V adapter stays in the model and
BOM and is shown only in the exploded view), the cold-water angle stop, and the counter with a sink
edge and the drinking-water tap that the outlet line feeds.

UV-C is never shown as visible light: the LEDs are modeled as dark packages, and every UV-C
path stays behind stainless, PTFE or quartz. Only the UV level bar glows.

APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, levels(), positions() and build_parts() in
model.py; most parts are the model's own solids with an appearance material.
Axes as model.py: Z up along the reactor axis, X to the right (-X is the plumbing side), Y toward
the cabinet wall (+Y); the front is -Y. Z = 0 is the bottom of the heat sink fins; the cabinet
floor is PARAMS["floor_gap"] lower.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, GeomType, Plane, Polygon, Pos, RegularPolygon, Rot,
                       Solid, Sphere, Text, Torus, Vector, extrude, fillet)
from model import PARAMS, levels, build_parts, positions

TITLE = "LumaFlow: under-sink UV-C LED water disinfection reactor for a drinking-water tap"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); reactor in its pipe "
             "clamps on the bracket plate under the sink, flow switch and valve at left, enclosure with the "
             "lit UV level bar at right, DC cord entering the cabinet wall"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): upper cap, PTFE liner, "
             "reactor tube, lower cap, quartz window, PTFE washer and retaining ring, UV-C LED board, heat "
             "sink, LED head cable, flow switch, valve, dose sensor, enclosure lid and controller, bracket "
             "plate and clamps, 24 V adapter"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 20, "az": -35,
     "note": "Detail view from the front right, slightly above (about 20 deg elevation): the unit without "
             "its cabinet, dose sensor boss and the enclosure UV level bar facing the camera"},
]

# Colours (restrained product palette; accent from the kit)
C_ACCENT = "#0F766E"
C_STEEL = "#B9BFC6"
C_STEEL_DK = "#9AA2AB"
C_ACETAL = "#25282D"
C_ANOD = "#2F333A"
C_ALU = "#C7CBD0"
C_ENCL = "#E8EAED"
C_BRACKET = "#4B5563"
C_BLACK = "#1C1F24"
C_GREY = "#5B636E"
C_LIGHT = "#D5D9DE"
C_TUBE = "#EEF1F3"
C_PTFE = "#F7F7F5"
C_QUARTZ = "#DCEBF5"
C_PCB = "#166534"
C_LEDBOARD = "#E6E4DE"
C_CHIP = "#111827"
C_LABEL = "#F4F4F2"
C_WARN = "#F2C94C"
C_OK = "#22C55E"
C_WALL = "#E4E1DC"
C_FLOOR = "#D6D2CA"
C_COUNTER = "#F2F1EE"
C_CHROME = "#D0D4D8"


# ---------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _xcyl(r, x0, x1, y=0.0, z=0.0):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def _ycyl(r, y0, y1, x=0.0, z=0.0):
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def _rod(p0, p1, r):
    """Cylinder of radius r from point p0 to point p1."""
    p0, p1 = Vector(*p0), Vector(*p1)
    d = p1 - p0
    return Solid.make_cylinder(r, d.length, Plane(origin=p0, z_dir=d.normalized()))


def _pipe(pts, r):
    """Round tube along a polyline, with spheres at the bends."""
    s = None
    for a, b in zip(pts[:-1], pts[1:]):
        seg = _rod(a, b, r)
        s = seg if s is None else s + seg
    for p in pts[1:-1]:
        s += Pos(*p) * Sphere(r)
    return s


def _sector(r0, r1, z0, z1, ang_c, half):
    """Thin cylindrical shell sector (a wrapped label), centred on azimuth ang_c (deg from +X)."""
    R = r1 * 1.5
    n = 12
    pts = [(0.0, 0.0)] + [(R * math.cos(math.radians(ang_c - half + 2 * half * i / n)),
                           R * math.sin(math.radians(ang_c - half + 2 * half * i / n))) for i in range(n + 1)]
    wedge = Pos(0, 0, z0) * extrude(Polygon(*pts, align=None), amount=z1 - z0)
    return (_zcyl(r1, z0, z1) - _zcyl(r0, z0 - 1, z1 + 1)) & wedge


def _circle_edges(shape, r, tol=0.05):
    """Circular edges of radius r (outer rims of turned parts)."""
    out = []
    for e in shape.edges().filter_by(GeomType.CIRCLE):
        try:
            if abs(e.radius - r) < tol:
                out.append(e)
        except Exception:
            pass
    return out


def _collet(x0, x1, z, r, y=0.0):
    """Push-fit collet collar with a lighter release ring on its outer end (along X)."""
    body = _xcyl(r, x0, x1, y=y, z=z)
    return _fillet_try(body, _circle_edges(body, r), [0.8, 0.5])


# ---------------------------------------------------------------- product parts
def product_parts(P=PARAMS):
    L = levels(P)
    m = {k: s_ for k, _, s_, *_ in build_parts(P)}
    rt, rc = P["tube_od"] / 2, P["cap_d"] / 2
    rp = P["port_od"] / 2
    zd, zi, zo = L["z_det"], L["z_in"], L["z_out"]
    xs = -rc - 62                                   # outer end of the flow sensor and valve bodies (as model.py)
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    ym = (EY0 + EY1) / 2
    fz = -P["floor_gap"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ---- 1 reactor tube with its welded sensor boss (brushed 316)
    add("Reactor tube with sensor boss, 316 stainless", m["tube"], C_STEEL, "metal", 1, "shell", (0, 0, 0))
    # ---- 2, 3, 17 internal optics: liner, window, PTFE washer, retaining ring and screws, seals
    add("High-reflectance PTFE liner and top disc", m["liner"], C_PTFE, "plastic", 2, "internal", (0, -120, 70))
    add("Quartz window", m["window"], C_QUARTZ, "clear", 3, "internal", (0, 0, -115))
    add("PTFE window washer", m["washer"], C_PTFE, "plastic", 17, "internal", (0, 0, -125))
    add("Window retaining ring and screws, 316", m["retainer"] + m["ret_screws"], C_STEEL, "metal", 17, "shell", (0, 0, -140))
    add("Window gasket and face O-rings, EPDM", m["gasket"] + m["orings"], C_BLACK, "rubber", 17, "internal", (0, 0, -20))

    # ---- 4 UV-C LED board: aluminum-core disc, six dark LED packages (UV-C is invisible: no glow)
    board = _zcyl(P["board_d"] / 2, L["z_sink1"], L["z_board1"])
    for x, y in positions(P)["board"]:
        board -= _zcyl(1.7, L["z_sink1"] - 1, L["z_board1"] + 1, x, y)
    add("UV-C LED board (aluminum core)", board, C_LEDBOARD, "plastic", 4, "internal", (0, 0, -160))
    s_ = P["led_size"] / 2
    leds = lens = None
    for i in range(P["led_n"]):
        a = 2 * math.pi * i / P["led_n"]
        x, y = P["led_pcr"] * math.cos(a), P["led_pcr"] * math.sin(a)
        pk = _box(x - s_, x + s_, y - s_, y + s_, L["z_board1"], L["z_led1"] - 0.3)
        ln = _box(x - s_ + 0.6, x + s_ - 0.6, y - s_ + 0.6, y + s_ - 0.6, L["z_led1"] - 0.3, L["z_led1"])
        leds = pk if leds is None else leds + pk
        lens = ln if lens is None else lens + ln
    add("UV-C LED packages, 6 x 275 nm", leds, "#3A3A3F", "plastic", 4, "internal", (0, 0, -160))
    add("LED package windows", lens, "#AEB6BF", "metal", 4, "internal", (0, 0, -160))
    add("LED board screws", m["board_screws"], C_STEEL, "metal", 16, "internal", (0, 0, -170))

    # ---- 5 heat sink and spreader ring (anodized), head screws in the fin gaps
    add("Heat sink and spreader ring (black anodized)", m["sink"], C_ANOD, "painted", 5, "shell", (0, 0, -210))
    add("LED head screws, M4", m["head_screws"], C_STEEL, "metal", 16, "shell", (0, 0, -210))
    # ---- 10 LED head cable and its plug under the enclosure (interlock loop inside)
    add("LED head cable and plug", m["led_cable"], C_BLACK, "rubber", 10, "shell", (40, -40, -120))

    # ---- 6 lower end cap (316) with the UV-C warning label and symbol on the front
    add("Lower end cap, 316 stainless", m["cap_lo"], C_STEEL_DK, "metal", 6, "shell", (0, 0, -55))
    add("UV-C warning label, lower cap", m["label_cap"], C_WARN, "paper", 19, "shell", (0, 0, -55))
    zc = (L["z_board1"] + L["z_cap0"]) / 2
    tri = Plane(origin=(0, -(rc + 0.2), zc), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    add("UV-C warning symbol", extrude(tri * RegularPolygon(4.5, 3, rotation=90), amount=0.25), C_BLACK,
        "plastic", 19, "shell", (0, 0, -55))

    # ---- 7 upper end cap (acetal); 16 tie rod studs, washers and acorn nuts (domed for appearance)
    add("Upper end cap, acetal", m["cap_hi"], C_ACETAL, "plastic", 7, "shell", (0, 0, 55))
    domes = None
    for x, y in positions(P)["rods"]:
        d = Pos(x, y, L["z_top"] + 7.0) * (Sphere(4.0) & _zcyl(4.5, 0, 4.5))
        domes = d if domes is None else domes + d
    add("Tie rod studs, washers and acorn nuts, 316", m["rods"] + domes, C_STEEL, "metal", 16, "shell", (0, 0, 30))

    # ---- 8 Hall-effect flow switch on the inlet stem: filleted body, teal cap, flow arrow, collets
    fb = _box(xs, xs + 40, -14, 14, zi - 14, zi + 14)
    fb = _fillet_try(fb, fb.edges().filter_by(Axis.X), [4.0, 3.0, 2.0])
    add("Flow switch body", fb, C_LIGHT, "plastic", 8, "shell", (-60, 0, -55))
    pod = _zcyl(8, zi + 14, zi + 24, x=xs + 20)
    pod = _fillet_try(pod, _circle_edges(pod, 8), [1.5, 1.0])
    add("Flow switch sensor cap", pod, C_ACCENT, "plastic", 8, "shell", (-60, 0, -55))
    arrow = _box(xs + 10, xs + 26, -14.3, -14.0, zi - 1.0, zi + 1.0)
    arrow += Pos(xs + 29, -14.15, zi) * Rot(90, 0, 0) * extrude(RegularPolygon(4.0, 3), amount=0.3, both=True)
    add("Flow arrow marking", arrow, C_ACCENT, "plastic", 8, "shell", (-60, 0, -55))
    add("Flow switch lead", _pipe([(xs + 20, 0, zi + 24), (xs + 20, 0, zi + 30), (xs + 20, 12, zi + 30)], 1.8),
        C_BLACK, "rubber", 8, "shell", (-60, 0, -55))

    # ---- 11 normally closed solenoid valve on the outlet stem
    vb = _box(xs, xs + 40, -14, 14, zo - 14, zo + 14)
    vb = _fillet_try(vb, vb.edges().filter_by(Axis.X), [3.0, 2.0])
    add("Solenoid valve body", vb, C_GREY, "plastic", 11, "shell", (-60, 0, 55))
    coil = _zcyl(14, zo + 14, zo + 40, x=xs + 20)
    coil = _fillet_try(coil, _circle_edges(coil, 14), [2.0, 1.2])
    conn = _box(xs + 13, xs + 27, -21, -14, zo + 18, zo + 36)
    add("Solenoid coil and connector", coil + conn, C_BLACK, "plastic", 11, "shell", (-60, 0, 55))
    core = Pos(xs + 20, 0, zo + 40) * extrude(RegularPolygon(7.0, 6), amount=3.0) + _zcyl(3.5, zo + 43, zo + 44, x=xs + 20)
    add("Solenoid core nut", core, C_STEEL, "metal", 11, "shell", (-60, 0, 55))
    add("Valve lead", _pipe([(xs + 20, -21, zo + 27), (xs + 20, -26, zo + 27), (xs + 20, -26, zo + 50),
                             (xs + 20, 12, zo + 50)], 1.8), C_BLACK, "rubber", 11, "shell", (-60, 0, 55))

    # ---- 15 stem adaptors, outlet sleeve and push-fit lines (as model.py), collets at the open ports
    fit = m["fittings"]
    zmid = (zi + zo) / 2
    for tag, z, ex, sl in (("inlet", zi, (-30, 0, -55), _box(-400, 0, -50, 50, zi - 30, zmid)),
                           ("outlet", zo, (-30, 0, 55), _box(-400, 0, -50, 50, zmid, zo + 30))):
        add(f"Stem adaptor and push-fit line, {tag}" + (", 316 outlet sleeve" if tag == "outlet" else ""),
            fit & sl, C_TUBE, "plastic", 15, "shell", ex)
        add(f"Push-fit collet, {tag} line", _collet(xs - 4, xs, z, rp + 2.6), C_GREY, "plastic", 15, "shell", ex)

    # ---- 9 dose sensor: quartz window and holder in the welded boss, amplifier box
    pd = m["pd"]
    hold = pd & _box(rt, rt + 18, -20, 20, zd - 20, zd + 20)
    amp = pd & _box(rt + 18, rt + 40, -20, 20, zd - 20, zd + 20)
    add("Photodiode holder, 316", hold, C_STEEL, "metal", 9, "shell", (75, 0, 0))
    add("Dose sensor amplifier", amp, C_ACETAL, "plastic", 9, "shell", (75, 0, 0))
    add("Sensor lead", _pipe([(rt + 26, 0, zd), (EX0 - 4, 0, zd), (EX0 - 4, ym, zd), (EX0 - 4, ym, EZ0 + 26),
                              (EX0 - 12, ym, EZ0 + 22)], 1.6), C_BLACK, "rubber", 9, "shell", (75, 0, 0))

    # ---- 13 electronics enclosure: body (with gland and LED head socket), lid, UV level bar, labels
    add("Enclosure body", m["encl"], C_ENCL, "plastic", 13, "shell", (140, 0, 0))
    add("Enclosure front lid", m["lid"], C_ENCL, "plastic", 13, "shell", (140, -70, 0))
    segs = sorted(m["bar"].solids(), key=lambda sd: sd.center().X)
    lit = segs[0]
    for sd in segs[1:4]:
        lit = lit + sd
    add("UV level bar, lit segments", lit, "#2DD4BF", "emissive", 13, "shell", (140, -70, 0))
    add("UV level bar, unlit segment", segs[4], "#3A3F47", "plastic", 13, "shell", (140, -70, 0))
    add("UV-C warning label, inside the lid", m["label_lid"], C_WARN, "paper", 19, "internal", (140, -65, 0))
    sc = None
    for x, z in [(EX0 + 6, EZ0 + 6), (EX1 - 6, EZ0 + 6), (EX0 + 6, EZ1 - 6), (EX1 - 6, EZ1 - 6)]:
        h = _ycyl(2.6, EY0 - 0.8, EY0, x=x, z=z)
        sc = h if sc is None else sc + h
    add("Lid screws", sc, C_STEEL, "metal", 16, "shell", (140, -70, 0))
    add("Product label", m["label_prod"], C_LABEL, "paper", 19, "shell", (160, 0, 0))
    try:
        pl = Plane(origin=(EX1 + 0.2, (EY0 + EY1) / 2 + 2, EZ0 + 65), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        txt = extrude(pl * Text("LumaFlow", 6.0), amount=0.3)
        if txt.is_valid:
            add("Product label wordmark", txt, "#2B2F36", "plastic", 19, "shell", (160, 0, 0))
    except Exception:
        pass
    add("Product label accent band", _box(EX1 + 0.2, EX1 + 0.4, EY0 + 10, EY1 - 6, EZ0 + 84, EZ0 + 88),
        C_ACCENT, "plastic", 19, "shell", (160, 0, 0))

    # ---- 10 controller and LED driver modules (internal)
    add("Controller and LED driver", m["ctrl"], C_PCB, "plastic", 10, "internal", (70, 0, 0))

    # ---- 14 bracket plate and saddles; 18 rubber-lined pipe clamps
    add("Bracket plate, aluminium", m["bracket"], C_ALU, "metal", 14, "shell", (0, 120, 0))
    add("Sensor and valve saddles", m["saddles"], C_GREY, "plastic", 14, "shell", (0, 90, 0))
    add("Pipe clamps", m["clamps"], C_BRACKET, "painted", 18, "shell", (0, 70, 0))

    # ---- 12 24 V adapter (accessory: exploded view only; stays in the model and BOM)
    add("24 V power adapter", m["adapter"], C_GREY, "plastic", 12, "accessory", (80, 0, -120))

    # ---- context: cabinet wall and floor, DC cord into the wall, cold supply with angle stop,
    #      counter, sink edge, tap
    WY = P["bracket_y"][1]                           # cabinet wall face behind the bracket plate
    add("Cabinet wall section", _box(-265, 175, WY, WY + 16, fz - 12, 380), C_WALL, "painted", None, "context", (0, 0, 0))
    add("Cabinet floor section", _box(-265, 175, -85, WY + 16, fz - 12, fz), C_FLOOR, "painted", None, "context", (0, 0, 0))
    gx = EX0 - 12.5                                  # outer end of the cable gland
    cord = _pipe([(gx, ym, EZ0 + 20), (gx, ym, 12.0), (gx, WY, 12.0)], 2.6)
    cord += _ycyl(6.0, WY - 2, WY, x=gx, z=12.0)                 # grommet where the cord enters the wall
    add("DC cord into the cabinet wall", cord, C_BLACK, "rubber", 12, "context", (0, 0, 0))
    sx = -178.0
    add("Cold supply tubing", _pipe([(xs - 40, 0, zi), (sx, 0, zi), (sx, 0, zi + 26)], rp), C_TUBE, "plastic",
        None, "context", (0, 0, 0))
    stop = Pos(sx, 0, zi + 40) * Sphere(10.0) + _zcyl(6.5, zi + 26, zi + 40, x=sx)
    stop += _ycyl(7.0, 0, WY, x=sx, z=zi + 40)
    stop += _ycyl(16.0, WY - 3, WY, x=sx, z=zi + 40)
    stop += _ycyl(3.0, -22, 0, x=sx, z=zi + 40)
    knob = Pos(sx, -24, zi + 40) * Box(22.0, 6.0, 9.0)
    stop += _fillet_try(knob, knob.edges().filter_by(Axis.Y), [3.0, 2.0])
    add("Angle stop valve, chrome", stop, C_CHROME, "metal", None, "context", (0, 0, 0))
    tx, ty = -160.0, 20.0
    zc0, zc1 = 380.0, 410.0
    add("Tap supply tubing", _pipe([(xs - 40, 0, zo), (tx, 0, zo), (tx, ty, zo + 12), (tx, ty, zc0)], rp),
        C_TUBE, "plastic", None, "context", (0, 0, 0))
    counter = _box(-265, -70, -85, WY + 16, zc0, zc1)
    counter -= _box(-275, -205, -70, 30, zc0 - 1, zc1 + 1)
    add("Countertop section", counter, C_COUNTER, "painted", None, "context", (0, 0, 0))
    bowl = _box(-265, -209, -66, 26, 270, zc0) - _box(-266, -210.2, -64.8, 24.8, 271.2, zc0 + 1)
    bowl += _box(-265, -201, -74, 34, zc1, zc1 + 1.2) - _box(-266, -209, -66, 26, zc1 - 1, zc1 + 2)
    add("Sink bowl edge, stainless", bowl, C_CHROME, "metal", None, "context", (0, 0, 0))
    tap = _zcyl(22, zc1, zc1 + 5, x=tx, y=ty) + _zcyl(12, zc1 + 5, zc1 + 120, x=tx, y=ty)
    R, rs = 40.0, 7.0
    bend = Pos(tx - R, ty, zc1 + 120) * Rot(90, 0, 0) * Torus(R, rs)
    bend &= _box(tx - 2 * R - rs - 1, tx + rs + 1, ty - 20, ty + 20, zc1 + 120, zc1 + 120 + R + rs + 1)
    tap += bend + _zcyl(rs, zc1 + 95, zc1 + 120, x=tx - 2 * R, y=ty)
    tap += _zcyl(rs + 1.5, zc1 + 88, zc1 + 95, x=tx - 2 * R, y=ty)
    tap += _xcyl(4.0, tx + 10, tx + 42, y=ty, z=zc1 + 70) + _zcyl(13.5, zc1 + 64, zc1 + 76, x=tx, y=ty)
    add("Drinking-water tap, chrome", tap, C_CHROME, "metal", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:46s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:8.2f} cm3")
