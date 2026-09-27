"""LumaFlow product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: brushed 316 reactor tube with a product label and
tie rods under acorn nuts, filleted stainless lower cap with a UV-C warning label, dark acetal
upper cap, anodized heat sink, a flow switch and a solenoid valve on push-fit tubing, the wall
dose sensor on its saddle, and an electronics enclosure with a lid parting line, screws, a buzzer
grille, a lit status light and a dose bar. Inside: PTFE liner, quartz window and the LED board.
Context: a short section of cabinet wall and floor, the cold-water angle stop, and the counter
with a sink edge and the drinking-water tap that the outlet line feeds.

UV-C is never shown as visible light: the LEDs are modeled as dark packages, and every UV-C
path stays behind stainless, PTFE or quartz. Only the status light and dose bar glow.

APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, levels() and build_parts() in model.py.
Axes as model.py: Z up along the reactor axis, X to the right (-X is the plumbing side), Y toward
the cabinet wall (+Y); the front is -Y. Cabinet floor at Z = 0.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, GeomType, Plane, Polygon, Pos, RegularPolygon, Rot,
                       Solid, Sphere, Text, Torus, Vector, extrude, fillet)
from model import PARAMS, levels, build_parts

TITLE = "LumaFlow: under-sink UV-C LED water disinfection reactor for a drinking-water tap"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); reactor on its wall "
             "bracket under the sink, flow switch and valve at left, enclosure with lit status light at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): upper cap, PTFE liner, "
             "reactor tube, lower cap, quartz window, UV-C LED board, heat sink, flow switch, valve, dose "
             "sensor, enclosure lid and controller, bracket, 24 V adapter"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 20, "az": -35,
     "note": "Detail view from the front right, slightly above (about 20 deg elevation): the unit without "
             "its cabinet, dose sensor saddle and enclosure status light facing the camera"},
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
    m = {k: (s, bom) for k, _, s, bom, *_ in build_parts(P)}
    rb, rl, rt, rc = P["bore_d"] / 2, P["liner_od"] / 2, P["tube_od"] / 2, P["cap_d"] / 2
    rp = P["port_od"] / 2
    zd, zi, zo = L["z_det"], L["z_in"], L["z_out"]
    xs = -rc - 62                                   # outer end of the flow sensor and valve bodies (as model.py)
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ---- 1 reactor tube (brushed 316) with a wrapped product label on the front (-Y)
    add("Reactor tube, 316 stainless", m["tube"][0], C_STEEL, "metal", 1, "shell", (0, 0, 0))
    label = _sector(rt, rt + 0.25, 120.0, 215.0, -90.0, 22.0)
    add("Product label", label, C_LABEL, "paper", 1, "shell", (0, 0, 0))
    band = _sector(rt + 0.25, rt + 0.45, 204.0, 209.0, -90.0, 22.0)
    add("Label accent band", band, C_ACCENT, "plastic", 1, "shell", (0, 0, 0))
    try:
        pl = Plane(origin=(0, -(rt + 0.25), 162.0), x_dir=(0, 0, 1), z_dir=(0, -1, 0))
        txt = extrude(pl * Text("LumaFlow", 6.5), amount=0.3)
        if txt.is_valid:
            add("Label wordmark", txt, "#2B2F36", "plastic", 1, "shell", (0, 0, 0))
    except Exception:
        pass

    # ---- 2 PTFE liner and top disc, 3 quartz window (internal)
    add("High-reflectance PTFE liner and top disc", m["liner"][0], C_PTFE, "plastic", 2, "internal", (0, -120, 70))
    add("Quartz window", m["window"][0], C_QUARTZ, "clear", 3, "internal", (0, 0, -115))

    # ---- 4 UV-C LED board: aluminum-core disc, six dark LED packages (UV-C is invisible: no glow)
    board = _zcyl(P["board_d"] / 2, L["z_sink1"], L["z_board1"])
    board = _fillet_try(board, _circle_edges(board, P["board_d"] / 2), [0.5, 0.3])
    add("UV-C LED board (aluminum core)", board, C_LEDBOARD, "plastic", 4, "internal", (0, 0, -160))
    s = P["led_size"] / 2
    leds = lens = None
    for i in range(P["led_n"]):
        a = 2 * math.pi * i / P["led_n"]
        x, y = P["led_pcr"] * math.cos(a), P["led_pcr"] * math.sin(a)
        pk = _box(x - s, x + s, y - s, y + s, L["z_board1"], L["z_led1"] - 0.3)
        ln = _box(x - s + 0.6, x + s - 0.6, y - s + 0.6, y + s - 0.6, L["z_led1"] - 0.3, L["z_led1"])
        leds = pk if leds is None else leds + pk
        lens = ln if lens is None else lens + ln
    leds += _box(-3, 3, -19.5, -16.5, L["z_board1"], L["z_board1"] + 2.0)     # board connector
    leds += _box(8.5, 10.5, -8.0, -6.8, L["z_board1"], L["z_board1"] + 0.8)   # NTC sensor
    add("UV-C LED packages, 6 x 275 nm", leds, "#3A3A3F", "plastic", 4, "internal", (0, 0, -160))
    add("LED package windows", lens, "#AEB6BF", "metal", 4, "internal", (0, 0, -160))

    # ---- 5 heat sink (anodized, fins down) and aluminum spreader ring
    hw = P["sink_w"] / 2
    sink = _box(-hw, hw, -hw, hw, P["fin_h"], L["z_sink1"])
    sink = _fillet_try(sink, sink.edges().filter_by(Axis.Z), [2.0, 1.0])
    pitch = (P["sink_w"] - P["fin_t"]) / (P["n_fins"] - 1)
    for i in range(P["n_fins"]):
        x = -hw + i * pitch
        sink += _box(x, x + P["fin_t"], -hw, hw, 0, P["fin_h"] + 0.5)
    ring = _zcyl(rc, L["z_sink1"], L["z_board1"]) - _zcyl(P["board_d"] / 2 + 0.5, L["z_sink1"] - 1, L["z_board1"] + 1)
    for i in range(P["n_rod"]):
        a = math.radians(45 + 360 * i / P["n_rod"])
        x, y = P["rod_pcr"] * math.cos(a), P["rod_pcr"] * math.sin(a)
        hole = _zcyl(P["rod_d"] / 2 + 0.2, L["z_sink1"] - 1, L["z_board1"] + 1, x, y)
        sink -= _zcyl(P["rod_d"] / 2 + 0.2, P["fin_h"] - 1, L["z_sink1"] + 1, x, y)
        ring -= hole
    add("Heat sink (black anodized)", sink, C_ANOD, "painted", 5, "shell", (0, 0, -210))
    add("Heat spreader ring, aluminum", ring, C_ALU, "metal", 5, "shell", (0, 0, -185))

    # ---- 6 lower end cap (316), rims filleted, UV-C warning label on the front
    cap_lo = m["cap_lo"][0]
    cap_lo = _fillet_try(cap_lo, _circle_edges(cap_lo, rc), [1.5, 1.0, 0.6])
    add("Lower end cap, 316 stainless", cap_lo, C_STEEL_DK, "metal", 6, "shell", (0, 0, -55))
    warn = _sector(rc, rc + 0.25, L["z_board1"] + 7.0, L["z_cap0"] - 7.0, -70.0, 12.0)
    add("UV-C warning label", warn, C_WARN, "paper", 6, "shell", (0, 0, -55))
    ang = math.radians(-70.0)
    tri = Plane(origin=((rc + 0.35) * math.cos(ang), (rc + 0.35) * math.sin(ang), (L["z_board1"] + L["z_cap0"]) / 2),
                x_dir=(-math.sin(ang), math.cos(ang), 0), z_dir=(math.cos(ang), math.sin(ang), 0))
    mark = extrude(tri * RegularPolygon(4.5, 3, rotation=90), amount=0.25)
    add("UV-C warning symbol", mark, C_BLACK, "plastic", 6, "shell", (0, 0, -55))

    # ---- 7 upper end cap (acetal)
    cap_hi = m["cap_hi"][0]
    cap_hi = _fillet_try(cap_hi, _circle_edges(cap_hi, rc), [1.5, 1.0, 0.6])
    add("Upper end cap, acetal", cap_hi, C_ACETAL, "plastic", 7, "shell", (0, 0, 55))

    # ---- 16 tie rods with washers, hex nuts and acorn domes on top
    rods = nuts = None
    for i in range(P["n_rod"]):
        a = math.radians(45 + 360 * i / P["n_rod"])
        x, y = P["rod_pcr"] * math.cos(a), P["rod_pcr"] * math.sin(a)
        r = _zcyl(P["rod_d"] / 2, L["z_sink1"], L["z_top"] + 3.2, x, y)
        n = _zcyl(4.9, L["z_top"], L["z_top"] + 0.8, x, y)
        n += Pos(x, y, L["z_top"] + 0.8) * extrude(RegularPolygon(4.6, 6), amount=3.2)
        n += Pos(x, y, L["z_top"] + 4.0) * (Sphere(3.6) & _zcyl(4, 0, 4))
        rods = r if rods is None else rods + r
        nuts = n if nuts is None else nuts + n
    add("Tie rods, M5 316", rods, C_STEEL, "metal", 16, "shell", (0, 0, 30))
    add("Acorn nuts and washers, 316", nuts, C_STEEL, "metal", 16, "shell", (0, 0, 95))

    # ---- 8 Hall-effect flow switch on the inlet line: filleted body, teal cap, flow arrow, collets
    fb = _box(xs, xs + 40, -14, 14, zi - 14, zi + 14)
    fb = _fillet_try(fb, fb.edges().filter_by(Axis.X), [4.0, 3.0, 2.0])
    fb = _fillet_try(fb, fb.faces().sort_by(Axis.X)[0].edges() + fb.faces().sort_by(Axis.X)[-1].edges(), [1.2, 0.8])
    fb += _xcyl(8.5, xs - 5, xs, z=zi) + _xcyl(8.5, xs + 40, xs + 45, z=zi)
    add("Flow switch body", fb, C_LIGHT, "plastic", 8, "shell", (-60, 0, -55))
    pod = _zcyl(8, zi + 14, zi + 24, x=xs + 20)
    pod = _fillet_try(pod, _circle_edges(pod, 8), [1.5, 1.0])
    add("Flow switch sensor cap", pod, C_ACCENT, "plastic", 8, "shell", (-60, 0, -55))
    arrow = _box(xs + 10, xs + 26, -14.3, -14.0, zi - 1.0, zi + 1.0)
    arrow += Pos(xs + 29, -14.15, zi) * Rot(90, 0, 0) * extrude(RegularPolygon(4.0, 3), amount=0.3, both=True)
    add("Flow arrow marking", arrow, C_ACCENT, "plastic", 8, "shell", (-60, 0, -55))
    cable = _pipe([(xs + 20, 0, zi + 24), (xs + 20, 0, zi + 30), (xs + 20, 20, zi + 30)], 1.8)
    add("Flow switch lead", cable, C_BLACK, "rubber", 8, "shell", (-60, 0, -55))

    # ---- 11 normally closed solenoid valve on the outlet line
    vb = _box(xs, xs + 40, -14, 14, zo - 14, zo + 14)
    vb = _fillet_try(vb, vb.edges().filter_by(Axis.X), [3.0, 2.0])
    vb += _xcyl(8.5, xs - 5, xs, z=zo) + _xcyl(8.5, xs + 40, xs + 45, z=zo)
    add("Solenoid valve body", vb, C_GREY, "plastic", 11, "shell", (-60, 0, 55))
    coil = _zcyl(14, zo + 14, zo + 40, x=xs + 20)
    coil = _fillet_try(coil, _circle_edges(coil, 14), [2.0, 1.2])
    conn = _box(xs + 13, xs + 27, -21, -12, zo + 18, zo + 36)
    conn = _fillet_try(conn, conn.edges().filter_by(Axis.Y), [1.5, 1.0])
    add("Solenoid coil and connector", coil + conn, C_BLACK, "plastic", 11, "shell", (-60, 0, 55))
    core = Pos(xs + 20, 0, zo + 40) * extrude(RegularPolygon(7.0, 6), amount=3.0) + _zcyl(3.5, zo + 43, zo + 44, x=xs + 20)
    add("Solenoid core nut", core, C_STEEL, "metal", 11, "shell", (-60, 0, 55))
    vl = _pipe([(xs + 20, -21, zo + 27), (xs + 20, -26, zo + 27), (xs + 20, -26, zo + 50),
                (xs + 20, 20, zo + 50)], 1.8)
    add("Valve lead", vl, C_BLACK, "rubber", 11, "shell", (-60, 0, 55))

    # ---- 15 push-fit tubing and outlet insert (as model.py) with collets at the ports
    fit = m["fittings"][0]
    zmid = (zi + zo) / 2
    for tag, z, ex, sl in (("inlet", zi, (-30, 0, -55), _box(-400, 0, -50, 50, zi - 30, zmid)),
                           ("outlet", zo, (-30, 0, 55), _box(-400, 0, -50, 50, zmid, zo + 30))):
        add(f"Push-fit tubing, {tag} line" + (" and 316 outlet insert" if tag == "outlet" else ""),
            fit & sl, C_TUBE, "plastic", 15, "shell", ex)
        col = None
        for x0 in (xs - 9, xs + 45, -rc - 16):
            c = _collet(x0, x0 + 4, z, rp + 2.6)
            col = c if col is None else col + c
        add(f"Push-fit collets, {tag} line", col, C_GREY, "plastic", 15, "shell", ex)

    # ---- 9 wall dose sensor: 316 saddle, quartz sensor window, amplifier housing, lead to the enclosure
    add("Sensor quartz window", _xcyl(P["det_win_d"] / 2 - 0.2, rb, rt, z=zd), C_QUARTZ, "clear", 9, "internal", (75, 0, 0))
    sad = _xcyl(11, rt - 4, rt + 6, z=zd) - _zcyl(rt, zd - 12, zd + 12)
    sad += _xcyl(6, rt + 6, rt + 14, z=zd)
    sad = _fillet_try(sad, _circle_edges(sad, 11), [1.0, 0.6])
    add("Dose sensor saddle, 316", sad, C_STEEL, "metal", 9, "shell", (75, 0, 0))
    amp = _box(rt + 14, rt + 22, -9, 9, zd - 9, zd + 9)
    amp = _fillet_try(amp, amp.edges().filter_by(Axis.X), [2.0, 1.2])
    amp += _xcyl(2.2, rt + 22, EX0, z=zd)
    add("Dose sensor amplifier housing", amp, C_ACETAL, "plastic", 9, "shell", (75, 0, 0))

    # ---- 13 electronics enclosure: rear body and front lid split at a parting line
    ob = _box(EX0, EX1, EY0, EY1, EZ0, EZ1)
    ob = _fillet_try(ob, ob.edges().filter_by(Axis.Y), [7.0, 5.0, 3.0])
    ob = _fillet_try(ob, ob.faces().sort_by(Axis.Y)[0].edges(), [2.5, 1.5, 1.0])
    ib = _box(EX0 + 2.5, EX1 - 2.5, EY0 + 2.5, EY1 - 2.5, EZ0 + 2.5, EZ1 - 2.5)
    shell = ob - ib
    ys = EY0 + 6.0                                     # parting line 6 mm behind the front face
    groove = _box(EX0 - 2, EX1 + 2, ys - 0.3, ys + 0.3, EZ0 - 2, EZ1 + 2) - \
        _box(EX0 + 0.6, EX1 - 0.6, ys - 1, ys + 1, EZ0 + 0.6, EZ1 - 0.6)
    shell -= groove
    lid = shell & _box(EX0 - 5, EX1 + 5, EY0 - 5, ys, EZ0 - 5, EZ1 + 5)
    body = shell & _box(EX0 - 5, EX1 + 5, ys, EY1 + 5, EZ0 - 5, EZ1 + 5)
    # buzzer grille slots and screw counterbores in the lid
    for k in range(5):
        lid -= _box(EX0 + 17, EX1 - 17, EY0 - 1, EY0 + 1.0, EZ0 + 16 + 4 * k, EZ0 + 17.6 + 4 * k)
    screws_xz = [(EX0 + 7, EZ0 + 7), (EX1 - 7, EZ0 + 7), (EX0 + 7, EZ1 - 7), (EX1 - 7, EZ1 - 7)]
    for (x, z) in screws_xz:
        lid -= _ycyl(3.0, EY0 - 1, EY0 + 1.0, x=x, z=z)
    # cable gland (left face), sensor lead entry grommet
    gl = Pos(EX0 - 6, 0, EZ0 + 20) * Rot(0, 90, 0) * extrude(RegularPolygon(6.5, 6), amount=6.0, both=True)
    gl += _xcyl(4.6, EX0 - 12, EX0 - 9, z=EZ0 + 20)
    gl += _xcyl(3.4, EX0 - 12.5, EX0 - 12, z=EZ0 + 20)
    body += _xcyl(3.6, EX0 - 1.5, EX0, z=zd)
    add("Enclosure body", body, C_ENCL, "plastic", 13, "shell", (140, 0, 0))
    add("Enclosure front lid", lid, C_ENCL, "plastic", 13, "shell", (140, -70, 0))
    add("Cable gland", gl, C_BLACK, "rubber", 13, "shell", (140, 0, 0))
    sc = None
    for (x, z) in screws_xz:
        h = _ycyl(2.6, EY0 - 0.2, EY0 + 1.0, x=x, z=z)
        h = _fillet_try(h, _circle_edges(h, 2.6), [0.4, 0.2])
        h -= Pos(x, EY0 - 0.2, z) * Rot(90, 0, 0) * extrude(RegularPolygon(1.2, 6), amount=0.8, both=True)
        sc = h if sc is None else sc + h
    add("Lid screws", sc, C_STEEL, "metal", 13, "shell", (140, -70, 0))
    # status bezel (as the model's status light block), lit status LED and dose bar
    bz = _box(EX0 + 12, EX1 - 12, EY0 - 3, EY0, EZ1 - 30, EZ1 - 18)
    bz = _fillet_try(bz, bz.edges().filter_by(Axis.Y), [3.0, 2.0])
    bz = _fillet_try(bz, bz.faces().sort_by(Axis.Y)[0].edges(), [0.6, 0.4])
    add("Status and dose display bezel", bz, C_BLACK, "screen", 13, "shell", (140, -70, 0))
    zb = EZ1 - 24
    led = Pos(EX0 + 17.5, EY0 - 3.2, zb) * Rot(90, 0, 0) * Cylinder(1.8, 0.6)
    add("Status light (lit, green)", led, C_OK, "emissive", 13, "shell", (140, -70, 0))
    bars_on = bars_off = None
    for k in range(5):
        x0 = EX0 + 23 + 4.2 * k
        b = _box(x0, x0 + 3.0, EY0 - 3.3, EY0 - 2.9, zb - 1.6, zb + 1.6)
        if k < 4:
            bars_on = b if bars_on is None else bars_on + b
        else:
            bars_off = b
    add("Dose bar (lit segments)", bars_on, "#2DD4BF", "emissive", 13, "shell", (140, -70, 0))
    add("Dose bar (unlit segment)", bars_off, "#3A3F47", "plastic", 13, "shell", (140, -70, 0))
    stripe = _box(EX0 + 12, EX1 - 12, EY0 - 0.3, EY0, EZ1 - 36, EZ1 - 34.5)
    add("Enclosure accent stripe", stripe, C_ACCENT, "plastic", 13, "shell", (140, -70, 0))

    # ---- 10 controller and LED driver modules (internal)
    add("Controller and LED driver", m["ctrl"][0], C_PCB, "plastic", 10, "internal", (70, 0, 0))
    chips = _box(EX0 + 14, EX0 + 22, -5, -4, EZ0 + 34, EZ0 + 42) + _box(EX0 + 36, EX0 + 44, -3, -2, EZ0 + 74, EZ0 + 84)
    chips += _box(EX1 - 20, EX1 - 12, 2, 4, EZ0 + 14, EZ0 + 22)
    add("Controller components", chips, C_CHIP, "plastic", 10, "internal", (70, 0, 0))

    # ---- 14 wall bracket: filleted backplate, clamp rings, enclosure shelf, wall screws
    by0, by1 = P["bracket_y"]
    plate = _box(-50, EX1 + 8, by0, by1, 80, 250)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [8.0, 5.0])
    plate = _fillet_try(plate, plate.faces().sort_by(Axis.Y)[0].edges(), [1.0, 0.6])
    br = plate
    for z in P["ring_z"]:
        rg = _zcyl(P["ring_od"] / 2, z - 8, z + 8) - _zcyl(rt, z - 9, z + 9)
        rg = _fillet_try(rg, _circle_edges(rg, P["ring_od"] / 2), [1.2, 0.8])
        br = br + rg + _box(-6, 6, P["ring_od"] / 2 - 1, by0, z - 8, z + 8)
    br += _box(EX0, EX1, EY1, by0, 150, 180)
    for (x, z) in [(-38, 92), (-38, 238), (EX1 - 4, 238), (EX1 - 4, 92)]:
        br -= _ycyl(4.4, by0 - 1, by0 + 1.0, x=x, z=z)
    add("Wall bracket", br, C_BRACKET, "painted", 14, "shell", (0, 120, 0))
    ws = None
    for (x, z) in [(-38, 92), (-38, 238), (EX1 - 4, 238), (EX1 - 4, 92)]:
        h = _ycyl(4.0, by0 - 1.8, by0 + 1.0, x=x, z=z)
        h = _fillet_try(h, _circle_edges(h, 4.0), [0.8, 0.5])
        h -= _box(x - 2.2, x + 2.2, by0 - 2.5, by0 - 1.0, z - 0.4, z + 0.4)
        h -= _box(x - 0.4, x + 0.4, by0 - 2.5, by0 - 1.0, z - 2.2, z + 2.2)
        ws = h if ws is None else ws + h
    add("Bracket wall screws", ws, C_STEEL, "metal", 14, "shell", (0, 120, 0))

    # ---- 12 24 V adapter (accessory in the exploded view; sits on the cabinet floor in model.py)
    ad = _box(150, 245, -30, 20, 0, 34)
    ad = _fillet_try(ad, ad.edges().filter_by(Axis.Z), [6.0, 4.0])
    ad = _fillet_try(ad, ad.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 2.0])
    ad += _box(158, 172, -30.3, -30.0, 14, 20)
    add("24 V power adapter", ad, C_GREY, "plastic", 12, "accessory", (80, 0, -120))

    # ---- context: cabinet wall and floor, cold supply with angle stop, counter, sink edge, tap
    WY = by1                                         # cabinet wall face behind the bracket
    add("Cabinet wall section", _box(-265, 145, WY, WY + 16, -12, 380), C_WALL, "painted", None, "context", (0, 0, 0))
    add("Cabinet floor section", _box(-265, 145, -85, WY + 16, -12, 0), C_FLOOR, "painted", None, "context", (0, 0, 0))
    cord = _pipe([(EX0 - 12.5, 0, EZ0 + 20), (42, 0, EZ0 + 20), (42, 0, 74), (42, WY, 74)], 2.6)
    cord += _ycyl(7.0, WY - 2, WY, x=42, z=74)
    add("DC cord to adapter", cord, C_BLACK, "rubber", 12, "context", (0, 0, 0))
    # inlet: tubing continues from the flow switch to a chrome angle stop on the wall
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
    # outlet: tubing from the valve up through the counter to the drinking-water tap
    tx, ty = -160.0, 20.0
    zc0, zc1 = 380.0, 410.0
    add("Tap supply tubing", _pipe([(xs - 40, 0, zo), (tx, 0, zo), (tx, ty, zo + 12), (tx, ty, zc0)], rp),
        C_TUBE, "plastic", None, "context", (0, 0, 0))
    counter = _box(-265, -70, -85, WY + 16, zc0, zc1)
    counter = _fillet_try(counter, [e for e in counter.edges().filter_by(Axis.Y)
                                    if e.center().X > -100 and e.center().Z > zc1 - 1], [3.0, 2.0])
    sink_cut = _box(-275, -205, -70, 30, zc0 - 1, zc1 + 1)
    counter -= sink_cut
    add("Countertop section", counter, C_COUNTER, "painted", None, "context", (0, 0, 0))
    bowl = _box(-265, -209, -66, 26, 270, zc0) - _box(-266, -210.2, -64.8, 24.8, 271.2, zc0 + 1)
    bowl = _fillet_try(bowl, bowl.edges().filter_by(Axis.X), [8.0, 5.0])
    bowl += _box(-265, -201, -74, 34, zc1, zc1 + 1.2) - _box(-266, -209, -66, 26, zc1 - 1, zc1 + 2)
    add("Sink bowl edge, stainless", bowl, C_CHROME, "metal", None, "context", (0, 0, 0))
    tap = _zcyl(22, zc1, zc1 + 5, x=tx, y=ty) + _zcyl(12, zc1 + 5, zc1 + 120, x=tx, y=ty)
    tap = _fillet_try(tap, _circle_edges(tap, 22), [2.0, 1.0])
    R, rs = 40.0, 7.0
    bend = Pos(tx - R, ty, zc1 + 120) * Rot(90, 0, 0) * Torus(R, rs)
    bend &= _box(tx - 2 * R - rs - 1, tx + rs + 1, ty - 20, ty + 20, zc1 + 120, zc1 + 120 + R + rs + 1)
    tap += bend + _zcyl(rs, zc1 + 95, zc1 + 120, x=tx - 2 * R, y=ty)
    tap += _zcyl(rs + 1.5, zc1 + 88, zc1 + 95, x=tx - 2 * R, y=ty)
    lever = _xcyl(4.0, tx + 10, tx + 42, y=ty, z=zc1 + 70)
    lever = _fillet_try(lever, _circle_edges(lever, 4.0), [1.5, 1.0])
    tap += lever + _zcyl(13.5, zc1 + 64, zc1 + 76, x=tx, y=ty)
    add("Drinking-water tap, chrome", tap, C_CHROME, "metal", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:8.2f} cm3")
