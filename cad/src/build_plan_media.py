"""LumaFlow prototype build plan pictures (LMF-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything; `sheets 103` draws one making sketch. Every picture is drawn
from cad/src/model.py (build_parts), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/LMF-DWG-101 to 111        making sketches for the made and drilled components
    docs/05-build-plan/plate-holes.png     bracket plate drilling layout
    docs/05-build-plan/cap-sections.png    half sections of the two end caps with their sizes
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_parts, levels, positions  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
L = levels(P)
H = positions(P)
C = {k: (n, s, bom, col, ex) for k, n, s, bom, col, ex in build_parts(P)}
rt, rc = P["tube_od"] / 2, P["cap_d"] / 2
zd = L["z_det"]
REPO = "github.com/BoujeeEnjinia1701/lumaflow"


def shape(*ks):
    out = None
    for k in ks:
        out = C[k][1] if out is None else out + C[k][1]
    return out


def part(key, name=None, color=None, explode=None, sh=None):
    n, s, bom, col, ex = C[key]
    return Part(name or n, sh if sh is not None else s, color or col, None, tuple(explode if explode is not None else ex), 1.0)


def win(sh, x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return sh & (Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0))


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def flr(length=440):
    """A strip of cabinet floor and wall for the steps that show the unit in place."""
    from build123d import Box, Pos
    fz = -P["floor_gap"]
    return Part("Cabinet floor", Pos(90, 10, fz - 3) * Box(length, 150, 6), "#E5E7EB", None, (0, 0, 0), 0.6)


# ----------------------------------------------------------------- overview
ORDER = [
    ("bracket", "Bracket plate", (270, 130, 60)),
    ("saddles", "Sensor and valve saddles (2)", (270, 0, 60)),
    ("clamps", "Pipe clamps (2) on M8 studs", (270, 70, 60)),
    ("cap_lo", "Lower end cap, 316", (0, 0, -40)),
    ("gasket", "Window gasket", (0, 0, -70)),
    ("window", "Quartz window", (0, 0, -100)),
    ("washer", "PTFE window washer", (0, 0, -118)),
    ("retainer", "Retaining ring and six M3 screws", (0, 0, -138)),
    ("label_cap", "UV-C warning label, lower cap", (0, -60, -40)),
    ("board", "UV-C LED board and three M3 screws", (0, 0, -170)),
    ("led_cable", "LED head cable and plug", (40, -60, -175)),
    ("sink", "Heat sink, spreader ring, four M4 screws", (0, 0, -215)),
    ("rods", "Tie rod studs (4), washers, acorn nuts", (0, 0, 120)),
    ("orings", "Face O-rings (2)", (0, 0, 0)),
    ("tube", "Reactor tube with welded sensor boss", (0, 0, 40)),
    ("liner", "PTFE liner and top disc", (0, -150, 60)),
    ("cap_hi", "Upper end cap, acetal", (0, 0, 90)),
    ("fittings", "Stem adaptors, outlet sleeve, lines", (-60, 0, 0)),
    ("pd", "Sensor window and photodiode holder", (30, -110, 0)),
    ("encl", "Enclosure body with controller", (90, 0, 0)),
    ("label_prod", "Product label", (150, -150, -60)),
    ("lid", "Lid, UV level bar, UV-C label", (90, -90, 0)),
    ("flow", "Flow sensor", (-90, 0, 0)),
    ("valve", "Solenoid valve", (-90, 0, 0)),
    ("adapter", "24 V adapter", (60, 0, 0)),
]


def overview():
    parts = []
    for k, name, off in ORDER:
        if k == "board":
            sh = shape("board", "board_screws")
        elif k == "sink":
            sh = shape("sink", "head_screws")
        elif k == "retainer":
            sh = shape("retainer", "ret_screws")
        elif k == "encl":
            sh = shape("encl", "ctrl")
        elif k == "lid":
            sh = shape("lid", "bar", "label_lid")
        else:
            sh = None
        p = part(k, name, explode=off, sh=sh)
        if k == "orings":   # the two O-rings sit at the two tube ends; pull them out with their caps
            lo = win(C["orings"][1], -40, 40, -40, 40, 50, 70)
            hi = win(C["orings"][1], -40, 40, -40, 40, 255, 275)
            from build123d import Pos
            p = Part(name, (Pos(0, 0, -20) * lo) + (Pos(0, 0, 65) * hi), p.color, None, (0, 0, 0), 1.0)
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "LumaFlow prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the wall is behind the plate",
                       elev=16, azim=-62, size=(12, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    from build123d import Pos
    P2 = {103: "Window pocket to 13.5 for the PTFE washer", 104: "PTFE washer under the window; no lapping",
          105: "LED head cable through the slot", 111: "UV level bar, LED head socket, labels"}
    out = []

    def B(n):   # rev P2 for the sheets the 2026-10-02 decisions changed; the others stay P1 of 2026-10-01
        first = ("P1", "Making sketch for the prototype build plan", "2026-10-01", "AC")
        if n in P2:
            return dict(project="LumaFlow", date=DATE, rev="P2", revisions=[first, ("P2", P2[n], DATE, "AC")])
        return dict(project="LumaFlow", date="2026-10-01", rev="P1", revisions=[first])
    want = lambda n: only is None or str(n) in only  # noqa: E731
    G = lambda k: Part(C[k][0], C[k][1], "#D1D5DB", None, (0, 0, 0), 1.0)  # noqa: E731
    reactor = [G(k) for k in ("tube", "cap_lo", "cap_hi", "sink", "rods")]

    if want(101):
        out.append(bv.component_sheet(
            part("bracket"), reactor + [G("encl"), G("flow"), G("valve"), G("saddles"), G("clamps")],
            dwg_no="LMF-DWG-101", title="LumaFlow bracket plate: making sketch",
            material="Aluminium plate 6 mm, 6061 or 5083 class",
            notes=["Cut the blank 242 wide x 270 tall from 6 mm plate; square, deburr,",
                   "  round the corners to about 3 mm. Front view is the reactor side.",
                   "Measure across from the left edge and up from the bottom edge.",
                   "Clamp studs: two M8 tapped holes (drill 6.8) 112 across, 65 and",
                   "  195 up. The reactor axis is 112 from the left edge.",
                   "Enclosure: four M4 tapped holes (drill 3.3) 182 and 226 across,",
                   "  78 and 192 up.",
                   "Saddles: four 4.5 mm holes 25 across, 15, 29, 241 and 255 up;",
                   "  countersink them on the back (wall) face.",
                   "Wall: four 5.5 mm holes 7 and 234 across, 10 and 260 up.",
                   "Deburr every hole on both faces.",
                   "Check: lay the saddles and the enclosure on it and look through",
                   "  each hole; the holes line up without forcing a screw."],
            view_shape=C["bracket"][1], inset_view=(18, -62), **B(101)))

    if want(102):
        sd = win(C["saddles"][1], -200, 0, 0, 60, 20, 90)
        out.append(bv.component_sheet(
            Part("Saddle", sd, "#A3A3A3", None, (0, 0, 0), 1.0), [G("bracket"), G("flow"), G("fittings"), G("cap_lo")],
            dwg_no="LMF-DWG-102", title="LumaFlow sensor and valve saddle (make 2): making sketch",
            material="PETG, 3D printed, 4 walls, 40 % infill",
            notes=["Print two blocks 20 wide x 35 deep x 28 tall, the 20 x 28 back",
                   "  face (the face that goes on the plate) flat on the bed.",
                   "Cable-tie slot: 8 wide x 4 deep, right through from top to",
                   "  bottom, 6 to 10 mm from the front face.",
                   "Back face: two M4 heat-set inserts on the centre line, 14 apart",
                   "  (7 above and below the middle), 8 deep.",
                   "Fit: two M4 x 10 countersunk screws from behind the plate.",
                   "  The flat back of the flow sensor (lower saddle) or the valve",
                   "  (upper saddle) rests on the front face; one cable tie through",
                   "  the slot and round the body holds it.",
                   "The saddle only steadies the body; the stem adaptor carries",
                   "  the water connection.",
                   "Check: the front face is square to the back face."],
            view_shape=Pos(87, -31.5, -L["z_in"]) * sd, inset_view=(18, -120), **B(102)))

    if want(103):
        cap = C["cap_lo"][1]
        out.append(bv.component_sheet(
            part("cap_lo"), [G("tube"), G("sink"), G("flow"), G("fittings"), G("rods")],
            dwg_no="LMF-DWG-103", title="LumaFlow lower end cap: making sketch",
            material="316 stainless round bar 95 mm; machine shop (lathe and mill)",
            notes=["Turn to 90 dia x 30. Bottom face (LED side) down in the views.",
                   "From the bottom: recess 72.4 dia x 2 deep for the retaining ring;",
                   "  window pocket 58 dia up to 13.5 from the bottom; shoulder there;",
                   "  50 mm bore from 13.5 up to the top face. Fine finish on the shoulder.",
                   "Top face: tube seat, a groove 59 to 65.5 dia, 2 deep, leaving a",
                   "  59 dia spigot that the tube slides over; O-ring groove 60 to",
                   "  64.8 dia, 1.3 deep, in the floor of the seat.",
                   "Inlet boss 20 dia on the left side, centre 19 up, face 55 from the",
                   "  axis; tap 1/4 BSPP 11 deep, then drill 7 through to the bore.",
                   "Top face: four M5 tapped holes 12 deep on an 80 circle, at 45 deg.",
                   "Recess floor: six M3 tapped holes 8 deep on a 65 circle, at 30 deg.",
                   "Bottom face: four M4 tapped 10 deep at 16.3 and 36 from the axis.",
                   "Section picture: cap-sections.png in the build plan.",
                   "Check: the window drops into the pocket by hand."],
            view_shape=Pos(0, 0, -L["z_board1"]) * cap, inset_view=(-25, -60), **B(103)))

    if want(104):
        out.append(bv.component_sheet(
            part("retainer", sh=shape("retainer")), [G("cap_lo"), G("window"), G("washer")],
            dwg_no="LMF-DWG-104", title="LumaFlow window retaining ring: making sketch",
            material="316 stainless sheet 2 mm; laser cut",
            notes=["Laser cut a ring 72 outside dia, 51 inside dia, from 2 mm 316.",
                   "Six 3.4 mm holes on a 65 dia circle, every 60 deg starting at",
                   "  30 deg; countersink them 90 deg on the bottom (LED) face so",
                   "  M3 countersunk screws sit flush.",
                   "Flatten the top face if the cut left it bowed. The window does",
                   "  not touch it: a 0.5 mm PTFE washer, 57 outside and 51 inside,",
                   "  lies between the ring and the window.",
                   "Break the inside edge 0.3 mm. Passivate.",
                   "Fit: it sits in the 72.4 recess in the cap's bottom face, flush",
                   "  with that face. Six M3 x 8 screws into the cap, tightened",
                   "  evenly in a cross pattern to about 0.5 N m.",
                   "The 51 mm bore is the window's open span used in the stress",
                   "  calculation; do not open it out.",
                   "Check: flat within 0.1 mm across a straight edge."],
            view_shape=Pos(0, 0, -L["z_board1"]) * C["retainer"][1], inset_view=(-40, -60), **B(104)))

    if want(105):
        out.append(bv.component_sheet(
            part("sink"), [G("cap_lo"), G("board"), G("tube"), G("retainer")],
            dwg_no="LMF-DWG-105", title="LumaFlow heat sink and spreader ring: drilling and making sketch",
            material="Bought aluminium finned sink 90 x 90 x 30; ring from 3 mm aluminium plate",
            notes=["Sink: bought, 90 x 90 x 30, nine fins hanging down, 6 mm base.",
                   "  Fins run front to back. Drill four 4.5 mm holes through the",
                   "  base in the second fin gap each side, 16.3 from the centre",
                   "  across and 36 front and back. Spot face for the screw heads.",
                   "  Three M3 tapped holes (drill 2.5) 5 deep on a 38 dia circle at",
                   "  30, 150 and 270 deg for the LED board.",
                   "Ring: cut 90 outside, 45 inside dia from 3 mm aluminium; an 8 mm",
                   "  wide slot from the hole to the edge on the right side (toward",
                   "  the enclosure) for the LED cable; drill four 4.5 mm holes",
                   "  matching the sink. Deburr.",
                   "Fit: thermal pad, ring on the sink base, LED board in the ring's",
                   "  hole, its flat cable out through the slot; the stack bolts to",
                   "  the cap with four M4 x 16 screws.",
                   "Check: ring and board tops level within 0.1 mm."],
            view_shape=C["sink"][1], inset_view=(-25, -60), **B(105)))

    if want(106):
        out.append(bv.component_sheet(
            part("tube"), [G("cap_lo"), G("cap_hi"), G("pd"), G("clamps")],
            dwg_no="LMF-DWG-106", title="LumaFlow reactor tube with sensor boss: making sketch",
            material="316 stainless tube 65 x 3; 316 bar 25 mm for the boss; machine shop",
            notes=["Cut 204 long, ends faced square and deburred (200 between caps",
                   "  plus 2 into each cap's seat). Keep the outside smooth near the",
                   "  ends: the O-rings seal on the end faces.",
                   "Boss: 22 dia x 14 long from 316 bar, one end bored to the tube's",
                   "  curve. TIG weld it on, centred 105 up from the bottom end, with",
                   "  argon purge inside; keep weld bead off the bore.",
                   "After welding: drill 8 through the boss and the wall; from the",
                   "  boss face cut an M12 x 1 thread 5 deep, then a 10.2 dia",
                   "  window seat 3.5 deeper, flat bottomed.",
                   "Pickle and passivate. The bore must be free of weld spatter so",
                   "  the liner slides in.",
                   "Check: the liner slides through by hand; the boss axis is",
                   "  square to the tube axis."],
            view_shape=Pos(0, 0, -L["z_tube0"]) * C["tube"][1], inset_view=(18, -40), **B(106)))

    if want(107):
        out.append(bv.component_sheet(
            part("liner"), [Part(C[k][0], win(C[k][1], -60, 60, 0, 60, 0, 400), "#D1D5DB", None, (0, 0, 0), 1.0) for k in ("tube", "cap_lo", "cap_hi")],
            dwg_no="LMF-DWG-107", title="LumaFlow PTFE liner and top disc: making sketch",
            material="High-reflectance sintered or expanded PTFE tube 59 x 50",
            notes=["Cut the PTFE tube 227 long. Turn the top 25 down to 56 dia.",
                   "Top disc: 56 dia x 3 from the same material, pressed into the",
                   "  top of the bore (bore depth 224) and flush with the end.",
                   "Outlet hole: 7 dia, 215 up from the bottom end, on the left.",
                   "Sensor hole: 8 dia, 103 up from the bottom end, on the right,",
                   "  exactly opposite the outlet hole.",
                   "Handle with clean gloves; never touch the bore. Any mark",
                   "  lowers the reflectance the dose depends on.",
                   "Fit: slides into the tube from the top with the sensor hole",
                   "  lined up with the boss; its bottom end sits on the lower",
                   "  cap's spigot, its turned top in the upper cap's pocket.",
                   "Check: look through the boss: the 8 mm hole is centred."],
            view_shape=Pos(0, 0, -L["z_cap0"]) * C["liner"][1], inset_view=(18, -40), **B(107)))

    if want(108):
        out.append(bv.component_sheet(
            part("cap_hi"), [G("tube"), G("valve"), G("fittings"), G("rods")],
            dwg_no="LMF-DWG-108", title="LumaFlow upper end cap: making sketch",
            material="Acetal (POM) food-contact grade round bar 95 mm",
            notes=["Turn to 90 dia x 40. Bottom face (tube side) down in the views.",
                   "Bottom face: tube seat 65.5 dia x 2 deep; in its floor an O-ring",
                   "  groove 60 to 64.8 dia, 1.3 deep.",
                   "Liner pocket 56.2 dia from the seat floor up to 27 from the",
                   "  bottom face. The 13 mm left above it is the pressure roof.",
                   "Outlet boss 20 dia on the left, centre 15 up, face 55 from the",
                   "  axis; tap 1/4 BSPP 11 deep, then bore 9.6 through to the pocket.",
                   "Outlet sleeve: 316 tube 9.5 x 7, 17 long, pressed into the 9.6",
                   "  bore from the thread end until it meets the liner.",
                   "Four 5.4 mm holes on an 80 circle, at 45 deg, for the studs.",
                   "Check: the liner's turned top enters the pocket by hand."],
            view_shape=Pos(0, 0, -L["z_cap1"]) * C["cap_hi"][1], inset_view=(18, -60), **B(108)))

    if want(109):
        from build123d import Cylinder, Rot
        x, y = H["rods"][0]
        rod = win(C["rods"][1], x - 6, x + 6, y - 6, y + 6, 0, 400)
        out.append(bv.component_sheet(
            Part("Tie rod stud", rod, "#52525B", None, (0, 0, 0), 1.0), [G("cap_lo"), G("cap_hi"), G("tube")],
            dwg_no="LMF-DWG-109", title="LumaFlow tie rod stud (make 4): making sketch",
            material="M5 threaded rod, A4 (316) stainless",
            notes=["Cut four 258 long from M5 A4 threaded rod; chamfer and dress",
                   "  both ends so a nut runs on by hand.",
                   "One end goes 12 into the lower cap's tapped holes with a drop",
                   "  of medium threadlocker; run it in with two nuts locked",
                   "  together, then remove the nuts.",
                   "The other end passes through the upper cap and carries a",
                   "  10 mm washer and an M5 acorn nut.",
                   "Tighten the four acorn nuts evenly, a quarter turn at a time,",
                   "  until both tube ends are down on their seats, then to about",
                   "  2 N m. Do not over-tighten: the upper cap is acetal.",
                   "Check: all four studs stand 246 above the lower cap's top face."],
            view_shape=Rot(0, 90, 0) * Cylinder(P["rod_d"] / 2, 258),
            inset_view=(18, -60), **B(109)))

    if want(110):
        holder = win(C["pd"][1], rt + 5, rt + 30, -12, 12, zd - 12, zd + 12)
        out.append(bv.component_sheet(
            Part("Photodiode holder", holder, "#D4A017", None, (0, 0, 0), 1.0), [G("tube"), G("encl"), G("liner")],
            dwg_no="LMF-DWG-110", title="LumaFlow photodiode holder: making sketch",
            material="316 stainless bar 16 mm; amplifier box bought",
            notes=["Turn from 16 mm 316: an M12 x 1 nose 5 long, then a 14 dia",
                   "  body 8 long with two spanner flats 12 across.",
                   "Bore 5.4 through for the TO-46 photodiode can; counterbore",
                   "  from the outer end to suit the can's flange.",
                   "The nose's end face is flat and smooth: it presses the 10 x 3",
                   "  quartz sensor window onto a 0.5 mm EPDM washer in the boss.",
                   "Fix the photodiode in the bore with UV-stable epoxy, window side",
                   "  facing the water. The amplifier (8 x 18 x 18) sits on the",
                   "  outer end; its lead runs to the enclosure gland.",
                   "Screw in by hand, then a quarter turn with a spanner.",
                   "Check: no light leaks round the nose when held to a lamp."],
            view_shape=Pos(-rt, 0, -zd) * holder, inset_view=(18, -40), **B(110)))

    if want(111):
        out.append(bv.component_sheet(
            part("encl", sh=shape("encl", "lid", "bar")), [G("bracket"), G("tube"), G("pd"), G("led_cable")],
            dwg_no="LMF-DWG-111", title="LumaFlow electronics enclosure: making sketch",
            material="PETG, 3D printed, 4 walls, 30 % infill",
            notes=["Body: a box 60 wide x 44 deep x 130 tall outside, walls 2.5,",
                   "  open at the front. Print it back face down.",
                   "Back face: four 4.4 mm holes, 8 in from each side and from",
                   "  the top and bottom, for M4 screws into the bracket plate.",
                   "Left side: 8 mm hole for the cable gland, 20 up from the bottom.",
                   "Floor: 12 mm hole for the LED head socket, 8 in from the left",
                   "  side and 15 behind the lid's front face.",
                   "Inside: bosses with M3 heat-set inserts for the modules, and a",
                   "  pocket for the lid reed switch near the front top corner.",
                   "Lid: 60 x 130 x 2.5. UV level bar: five windows 6 wide x 8 tall,",
                   "  2 apart, centred across, 22 to 30 below the top; print the",
                   "  segments in clear PETG. Magnet; four M3 screws to the body.",
                   "Labels: UV-C warning label inside the lid, product label on",
                   "  the right side.",
                   "Check: the lid closes the reed switch; opening it opens it."],
            view_shape=C["encl"][1] + C["lid"][1] + C["bar"][1], inset_view=(18, -62), **B(111)))
    return out


# ----------------------------------------------------------------- 2D layouts
def _section_polys(sh):
    """Section of a solid in the XZ plane (y = 0) as a list of (outer, holes) point lists."""
    from build123d import Plane
    polys = []
    for f in sh.intersect(Plane.XZ):
        rings = []
        for w in [f.outer_wire()] + list(f.inner_wires()):
            pts = []
            for e in w.order_edges() if hasattr(w, "order_edges") else w.edges():
                ps = [(v.X, v.Z) for v in e.positions([i / 24 for i in range(25)])]
                if pts and abs(pts[-1][0] - ps[-1][0]) + abs(pts[-1][1] - ps[-1][1]) < abs(pts[-1][0] - ps[0][0]) + abs(pts[-1][1] - ps[0][1]):
                    ps = ps[::-1]
                pts += ps
            rings.append(pts)
        polys.append(rings)
    return polys


def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Polygon
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    OUT.mkdir(parents=True, exist_ok=True)
    res = []
    # bracket plate seen from the front (the reactor side), from the model's holes
    pl = C["bracket"][1]
    yf = P["bracket_y"][0]
    face = [f for f in pl.faces() if abs(f.center().Y - yf) < 0.01 and f.area > 1e4][0]
    x0, z0 = P["plate_x"][0], P["plate_z"][0]
    W, Hh = P["plate_x"][1] - x0, P["plate_z"][1] - z0
    kinds = {6.8: ("M8 tapped (drill 6.8)", "clamp studs"), 3.3: ("M4 tapped (drill 3.3)", "enclosure"),
             4.5: ("4.5, countersunk at the back", "saddles"), 5.5: ("5.5", "wall screws")}
    fig = plt.figure(figsize=(11, 10.5), dpi=150)
    ax = fig.add_axes([0.07, 0.07, 0.62, 0.84]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), W, Hh, fc="#F5F5F4", ec=INK, lw=1.2))
    ax.plot([-x0, -x0], [-4, Hh + 4], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    ax.text(-x0 + 2, Hh + 3, "reactor axis", fontsize=7, color=MUT, va="bottom")
    xs, zs = set(), set()
    for w in face.inner_wires():
        bb = w.bounding_box()
        d = round(bb.size.X, 1)
        x, z = bb.center().X - x0, bb.center().Z - z0
        lab = {6.8: 6.8, 3.3: 3.3, 4.5: 4.5, 5.5: 5.5}[min((6.8, 3.3, 4.5, 5.5), key=lambda k: abs(k - d))]
        ax.add_patch(plt.Circle((x, z), d / 2, fc="white", ec=INK, lw=1))
        ax.plot([x - d / 2 - 2.5, x + d / 2 + 2.5], [z, z], color=MUT, lw=0.4); ax.plot([x, x], [z - d / 2 - 2.5, z + d / 2 + 2.5], color=MUT, lw=0.4)
        if lab != 5.5:
            ax.text(x + d / 2 + 2, z + d / 2 + 1, kinds[lab][1], fontsize=6.5, color=MUT)
        xs.add(round(x, 1)); zs.add(round(z, 1))
    for i, x in enumerate(sorted(xs)):
        yl = -9 - 9 * (i % 2)
        ax.plot([x, x], [0, yl + 3], color=AC, lw=0.4, ls=":")
        ax.text(x, yl, f"{x:g}", ha="center", va="top", fontsize=8, color=AC)
    ax.text(W / 2, -30, "across from the left edge, mm", ha="center", fontsize=8.5, color=MUT)
    for i, z in enumerate(sorted(zs)):
        xl = -6 - 15 * (i % 2)
        ax.plot([xl + 2, 0], [z, z], color=AC, lw=0.4, ls=":")
        ax.text(xl, z, f"{z:g}", ha="right", va="center", fontsize=8, color=AC)
    ax.text(-36, Hh / 2, "up from the bottom edge, mm", rotation=90, ha="center", va="center", fontsize=8.5, color=MUT)
    ax.set_xlim(-44, W + 6); ax.set_ylim(-36, Hh + 10)
    fig.text(0.04, 0.975, "Bracket plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.95, "Seen from the front (the reactor side). Plate 242 x 270 x 6 mm aluminium. Full size figures in mm, from the model.",
             fontsize=8.5, color=MUT, va="top")
    key = ["Clamp studs: M8 tapped (drill 6.8),", "  on the reactor axis", "Enclosure: M4 tapped (drill 3.3)",
           "Saddles: 4.5, countersunk on", "  the back (wall) face", "Wall screws: 5.5, the four", "  corner holes", "",
           "The flow sensor saddle is the lower", "  pair at the left, the valve saddle", "  the upper pair."]
    fig.text(0.72, 0.86, "What each hole is", fontsize=9.5, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.72, 0.83 - i * 0.024, t, fontsize=8.5, color=INK, va="top")
    fig.text(0.04, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "plate-holes.png")

    # half sections of the two caps (cut through the ports, seen from the front)
    fig = plt.figure(figsize=(13, 8.2), dpi=150)
    fig.text(0.03, 0.975, "End caps: sections through the axis and the port", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.948, "Cut on the reactor axis, seen from the front; the port is on the left. Sizes in mm, heights from the cap's "
             "bottom face. Grey: the cap. Blue: the parts that sit in it.", fontsize=8.5, color=MUT, va="top")
    specs = [("cap_lo", "Lower end cap, 316 stainless, LED side down (30 tall)", L["z_board1"], P["cap_lo_h"],
              ["window", "washer", "gasket", "retainer", "tube", "liner", "orings", "fittings"],
              [("72.4 dia x 2 deep: retaining ring recess", (35.5, 1.0), -1),
               ("58 dia window pocket, from 2 up to 13.5 up", (29, 7), 5),
               ("shoulder at 13.5 up; 50 dia bore above it", (25, 15), 11),
               ("O-ring groove 60 to 64.8 dia, 1.3 deep", (31.2, 27.3), 17),
               ("tube seat 59 to 65.5 dia, 2 deep;", (32.6, 29.3), 23),
               ("  the 59 dia spigot inside it", (29.2, 29.6), 27)],
              [("1/4 BSPP thread, 11 deep, then", (-50, 19), 23), ("7 dia to the bore; centre 19 up", (-50, 19), 19)]),
             ("cap_hi", "Upper end cap, acetal, tube side down (40 tall)", L["z_cap1"], P["cap_hi_h"],
              ["tube", "liner", "orings", "fittings"],
              [("tube seat 65.5 dia, 2 deep", (32.6, 1.0), -1),
               ("O-ring groove 60 to 64.8 dia, 1.3 deep", (31.2, 2.6), 4),
               ("56.2 dia liner pocket, from 2 up to 27 up", (28.1, 14), 13),
               ("13 mm roof above the pocket", (12, 33), 33)],
              [("1/4 BSPP thread, 11 deep, then a", (-50, 15), 19), ("9.6 bore for the 316 sleeve; centre 15 up", (-50, 15), 15)])]
    for i, (key, title, zb, hgt, inside, right, left) in enumerate(specs):
        ax = fig.add_axes([0.02, 0.5 - i * 0.45, 0.96, 0.42]); ax.set_aspect("equal"); ax.set_axis_off()
        for k in inside:
            for rings in _section_polys(win(C[k][1], -55.5, 200, -200, 200, zb - 0.01, zb + hgt + 0.01)):
                ax.add_patch(Polygon([(x, z - zb) for x, z in rings[0]], closed=True, fc="#BFDBFE", ec="#2563EB", lw=0.6))
                for hole in rings[1:]:
                    ax.add_patch(Polygon([(x, z - zb) for x, z in hole], closed=True, fc="white", ec="#2563EB", lw=0.6))
        for rings in _section_polys(C[key][1]):
            ax.add_patch(Polygon([(x, z - zb) for x, z in rings[0]], closed=True, fc="#D1D5DB", ec=INK, lw=0.9))
            for hole in rings[1:]:
                ax.add_patch(Polygon([(x, z - zb) for x, z in hole], closed=True, fc="white", ec=INK, lw=0.9))
        ax.plot([0, 0], [-4, hgt + 4], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
        ax.text(1, hgt + 3, "axis", fontsize=7.5, color=MUT)
        for t, (fx, fz), ty in right:
            ax.annotate(t, xy=(fx, fz), xytext=(56, ty), fontsize=8, color=INK, va="center",
                        arrowprops=dict(arrowstyle="-", color=AC, lw=0.5, shrinkA=1, shrinkB=0))
        for t, (fx, fz), ty in left:
            ax.annotate(t, xy=(fx, fz), xytext=(-68, ty), fontsize=8, color=INK, va="center", ha="right",
                        arrowprops=dict(arrowstyle="-", color=AC, lw=0.5, shrinkA=1, shrinkB=0) if "centre" in t else None)
        ax.plot([-45, 45], [-6, -6], color=AC, lw=0.6); ax.plot([-45, -45], [-7, -5], color=AC, lw=0.6); ax.plot([45, 45], [-7, -5], color=AC, lw=0.6)
        ax.text(0, -7, "90 dia", ha="center", va="top", fontsize=8, color=AC)
        ax.set_xlim(-125, 128); ax.set_ylim(-12, hgt + 6)
        ax.text(-123, hgt + 5, title, fontsize=10, color=INK, va="top", fontweight="bold")
    fig.savefig(OUT / "cap-sections.png", facecolor="white"); plt.close(fig); res.append(OUT / "cap-sections.png")
    return res


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []
    W = lambda k, *b: win(C[k][1], *b)  # noqa: E731

    def jp(k, name, box, color=None):
        return Part(name, W(k, *box), color or C[k][3], None, (0, 0, 0), 1.0)

    if only:                     # draw only the listed joints: skip bv.joint for the others
        real = bv.joint
        bv.joint = lambda parts, path, *a, **k: real(parts, path, *a, **k) if any(f"joint-{int(n):02d}" in str(path) for n in only) else path

    # 01 window clamp, cut on the axis
    b = (-52, 52, 0, 60, 18, 72)
    out.append(bv.joint([jp("cap_lo", "Lower end cap", b), jp("gasket", "Gasket, EPDM 1 mm", b, "#111827"),
                         jp("window", "Quartz window", b), jp("washer", "PTFE washer, 0.5 mm", b, "#B45309"),
                         jp("retainer", "Retaining ring", b),
                         jp("board", "LED board", b),
                         jp("sink", "Spreader ring and sink base", b), jp("liner", "PTFE liner", b), jp("tube", "Tube", b)],
                        OUT / "joint-01.png", "Joint 1: the window, clamped from below (cut on the axis)",
                        subtitle="Gasket above the window, PTFE washer and ring below it; water pressure pushes it onto the washer",
                        elev=2, azim=-90, size=(8, 6)))
    # 02 LED head from below
    b = (-50, 50, -50, 50, 14, 42)
    out.append(bv.joint([jp("sink", "Heat sink, fins hanging down", b), jp("head_screws", "Four M4 screws, in the fin gaps", b, "#B45309"),
                         jp("cap_lo", "Lower end cap", (-50, 50, -50, 50, 30, 45))],
                        OUT / "joint-02.png", "Joint 2: LED head on the lower cap, seen from below",
                        subtitle="Each screw head sits between two fins; a long hex key reaches it from below",
                        elev=-40, azim=-70, size=(8, 6)))
    # 03 lower tube seat, cut
    b = (22, 50, 0, 10, 52, 76)
    out.append(bv.joint([jp("cap_lo", "Lower end cap (spigot and seat)", b), jp("tube", "Tube end", b),
                         jp("liner", "PTFE liner on the spigot", b), jp("orings", "Face O-ring", b, "#B45309")],
                        OUT / "joint-03.png", "Joint 3: tube end in the lower cap (cut on the axis, right side)",
                        subtitle="The tube slides over the spigot and presses its end face onto the O-ring",
                        elev=2, azim=-90, size=(8, 6)))
    # 04 upper cap, cut through the outlet
    b = (-70, 48, 0, 10, 255, 312)
    out.append(bv.joint([jp("cap_hi", "Upper end cap, acetal", b), jp("tube", "Tube end", b),
                         jp("liner", "Liner, turned top and top disc", b), jp("orings", "Face O-ring", b, "#B45309"),
                         jp("fittings", "316 sleeve and stem adaptor", b)],
                        OUT / "joint-04.png", "Joint 4: upper cap, outlet and roof (cut on the axis)",
                        subtitle="13 mm acetal roof over the liner; the 316 sleeve meets the liner so no UV-C reaches the acetal",
                        elev=2, azim=-90, size=(8, 6)))
    # 05 sensor boss, cut
    b = (18, 64, 0, 10, zd - 16, zd + 16)
    out.append(bv.joint([jp("tube", "Tube wall and welded boss", b), jp("liner", "PTFE liner", b),
                         jp("pd", "Quartz sensor window, 10 x 3 mm", (rt + 1.5, rt + 5.01, 0, 10, zd - 16, zd + 16), "#7DD3FC"),
                         jp("pd", "Photodiode holder and amplifier", (rt + 5.01, 64, 0, 10, zd - 16, zd + 16))],
                        OUT / "joint-05.png", "Joint 5: dose sensor in its boss (cut on the boss axis)",
                        subtitle="The holder's nose presses the 10 x 3 mm window onto a washer on the seat; 8 mm hole to the water",
                        elev=2, azim=-90, size=(8, 6)))
    # 06 inlet port, sensor and saddle
    b = (-112, -30, -20, 56, 30, 82)
    out.append(bv.joint([jp("cap_lo", "Lower cap inlet boss", b), jp("fittings", "Stem adaptor and supply line", b),
                         jp("flow", "Flow sensor", b), jp("saddles", "Saddle and cable tie slot", b), jp("bracket", "Bracket plate", b)],
                        OUT / "joint-06.png", "Joint 6: inlet port, flow sensor and saddle",
                        subtitle="The adaptor screws into the boss; its stem pushes into the sensor; the saddle steadies the sensor",
                        elev=22, azim=-125, size=(8, 6)))
    # 07 pipe clamp
    b = (-48, 48, -42, 56, 80, 112)
    out.append(bv.joint([jp("tube", "Tube", b), jp("clamps", "Rubber-lined pipe clamp and M8 stud", b, "#0F766E"),
                         jp("bracket", "Bracket plate", b), jp("rods", "Tie rods, 2 mm clear of the clamp", b)],
                        OUT / "joint-07.png", "Joint 7: pipe clamp on the tube (lower clamp)",
                        subtitle="The stud screws into the plate; the clamp opens to let the reactor in and out",
                        elev=30, azim=-15, size=(8, 6)))
    # 08 LED head cable and plug (interlock loop)
    b = (-50, 130, -50, 50, 0, 125)
    out.append(bv.joint([jp("sink", "LED head", b), jp("cap_lo", "Lower end cap", b),
                         jp("led_cable", "Cable and plug, interlock loop inside", b, "#B45309"),
                         jp("encl", "Enclosure floor and socket", (55, 130, 0, 55, 95, 125))],
                        OUT / "joint-08.png", "Joint 8: LED head cable and plug",
                        subtitle="The 95 mm cable reaches the socket but is too short for the head to come clear while plugged in",
                        elev=12, azim=-60, size=(8, 6)))
    # 09 lid from inside: UV level bar segments and the UV-C warning label
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    b = (EX0 - 1, EX1 + 1, EY0 - 2, EY0 + 4, EZ0 - 1, EZ1 + 1)
    import numpy as np
    keep = bv._anchor
    # anchor each leader at the part's lowest corner, so the lid's leader lands on bare lid, not on the bar
    bv._anchor = lambda v: v[np.argmin(v[:, 2] - 0.01 * v[:, 0])]
    out.append(bv.joint([jp("lid", "Enclosure lid", b), jp("bar", "Five UV level bar segments", b, "#0F766E"),
                         jp("label_lid", "UV-C warning label", b, "#B45309")],
                        OUT / "joint-09.png", "Joint 9: enclosure lid, seen from inside",
                        subtitle="Bar segments pressed into the five windows; UV-C warning label on the inside face",
                        elev=10, azim=75, size=(8, 6)))
    bv._anchor = keep
    if only:
        bv.joint = real
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []

    def vivid(p):
        c = p.color.lstrip("#")
        rgb = [int(c[i:i + 2], 16) for i in (0, 2, 4)]
        if max(rgb) - min(rgb) < 40 and p.color not in ("#1F2937",):      # a grey part would vanish among the grey fitted parts
            return Part(p.name, p.shape, "#0F766E", None, p.explode, p.alpha)
        return p

    def st(n, done, new, title, sub, **kw):
        if only and str(n) not in only:
            return
        out.append(bv.step(done, [vivid(p) for p in new], OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    plate = part("bracket")
    sad = part("saddles", "Saddles (2)", explode=(0, -50, 0))
    st(1, [plate], [sad], "saddles onto the bracket plate",
       "Two M4 countersunk screws each from the back of the plate into the heat-set inserts", elev=18, azim=-62, label_done=False)
    st(2, [plate, part("saddles")], [part("clamps", "Pipe clamps on M8 studs (2)", explode=(0, -60, 0))],
       "clamp studs and pipe clamps onto the plate",
       "Studs into the M8 holes with threadlocker; clamps on the studs, left open. Then screw the plate to the wall",
       elev=18, azim=-62, label_done=False)
    cap = part("cap_lo")
    st(3, [cap], [part("gasket", "Gasket", explode=(0, 0, -45)), part("window", "Quartz window", explode=(0, 0, -90))],
       "gasket and window into the lower cap, from below",
       "Cap upside down on a clean cloth in real life; shown upright. Gloves on: no fingerprints on the window",
       elev=-28, azim=-60)
    st(4, [cap, part("gasket"), part("window")], [part("washer", "PTFE washer", explode=(0, 0, -35)),
                                                   part("retainer", "Retaining ring and six M3 screws", sh=shape("retainer", "ret_screws"), explode=(0, 0, -70)),
                                                   part("label_cap", "UV-C warning label", explode=(0, -40, 0))],
       "PTFE washer, retaining ring and cap label",
       "Washer on the window, ring on the washer, six M3 screws evenly to about 0.5 N m; UV-C label on the front", elev=-28, azim=-60, label_done=False)
    st(5, [part("sink")], [part("board", "LED board, cable and three M3 screws", sh=shape("board", "board_screws", "led_cable"), explode=(0, 0, 50))],
       "LED board and its cable onto the heat sink",
       "Thermal pad under the board; the flat cable out through the ring's slot toward the right", elev=30, azim=-60, label_done=True)
    lo = [cap, part("gasket"), part("window"), part("washer"), part("retainer", sh=shape("retainer", "ret_screws")), part("label_cap")]
    st(6, lo, [part("sink", "LED head, cable and four M4 screws", sh=shape("sink", "board", "board_screws", "head_screws", "led_cable"), explode=(0, 0, -70))],
       "LED head onto the lower cap",
       "Four M4 x 16 screws from below, in the fin gaps. Hold point: no light leak at the joint", elev=-25, azim=-60, label_done=False)
    head = part("sink", sh=shape("sink", "board", "board_screws", "head_screws", "led_cable"))
    lo2 = lo + [head]
    lo_ring = win(C["orings"][1], -40, 40, -40, 40, 50, 70)
    hi_ring = win(C["orings"][1], -40, 40, -40, 40, 255, 275)
    st(7, lo2, [part("rods", "Four studs", explode=(0, 0, 80)), Part("Lower face O-ring", lo_ring, "#B45309", None, (0, 0, 40), 1.0)],
       "studs and lower O-ring into the lower cap",
       "Studs 12 mm in with threadlocker; O-ring into the groove in the seat floor, lightly greased", elev=20, azim=-60, label_done=False)
    lo3 = lo2 + [part("rods"), Part("O-ring", lo_ring, "#D1D5DB", None, (0, 0, 0), 1.0)]
    st(8, lo3, [part("tube", "Tube with the liner inside", sh=shape("tube", "liner"), explode=(0, 0, 120))],
       "tube and liner onto the lower cap",
       "Liner into the tube first, sensor hole on the boss; then down between the studs onto the spigot, boss to the right",
       elev=20, azim=-60, label_done=False)
    lo4 = lo3 + [part("tube", sh=shape("tube", "liner"))]
    st(9, lo4, [Part("Upper face O-ring", hi_ring, "#B45309", None, (0, 0, 60), 1.0),
                part("cap_hi", "Upper end cap", explode=(0, 0, 110))],
       "upper O-ring and upper cap",
       "O-ring in the cap's groove; cap over the studs, outlet boss on the left; washers and acorn nuts, even quarter turns",
       elev=20, azim=-60, label_done=False)
    reactor = lo4 + [part("cap_hi"), Part("O-ring", hi_ring, "#D1D5DB", None, (0, 0, 0), 1.0)]
    fit = C["fittings"][1]
    adapt = win(fit, -70, -28, -15, 15, 0, 400)
    st(10, reactor, [Part("Stem adaptors and outlet sleeve", adapt, C["fittings"][3], None, (-60, 0, 0), 1.0)],
       "outlet sleeve and stem adaptors into the ports",
       "Sleeve pressed in to meet the liner; adaptors with their sealing washers, spanner tight", elev=20, azim=-120, label_done=False)
    reactor2 = reactor + [Part("Adaptors", adapt, "#D1D5DB", None, (0, 0, 0), 1.0)]
    st(11, reactor2, [part("pd", "Sensor window, washer and photodiode holder", explode=(60, 0, 0))],
       "dose sensor into the boss",
       "Washer and window into the seat, then the holder; hand tight plus a quarter turn. Hold point: leak test (section 6)",
       elev=20, azim=-40, label_done=False)
    unit = reactor2 + [part("pd")]
    base = [plate, part("saddles"), part("clamps")]
    st(12, base, [Part("Reactor assembly", shape("tube", "liner", "cap_lo", "cap_hi", "rods", "sink", "board", "pd", "retainer", "led_cable", "label_cap"), "#7B8794",
                       None, (0, -120, 0), 1.0)] + [Part("Adaptors", adapt, C["fittings"][3], None, (0, -120, 0), 1.0)],
       "reactor into the pipe clamps",
       "Lift the reactor into the open clamps, boss to the right, fins at least 25 mm above the floor; close the clamps",
       context=[flr()], elev=18, azim=-62, label_done=False)
    mounted = base + [Part("Reactor", shape("tube", "cap_lo", "cap_hi", "rods", "sink", "pd"), "#D1D5DB", None, (0, 0, 0), 1.0),
                      Part("Adaptors", adapt, "#D1D5DB", None, (0, 0, 0), 1.0), Part("UV-C label", C["label_cap"][1], "#D1D5DB", None, (0, 0, 0), 1.0)]
    st(13, mounted + [Part("LED cable", C["led_cable"][1], "#D1D5DB", None, (0, 0, 0), 1.0)],
       [part("encl", "Enclosure body with controller", sh=shape("encl", "ctrl"), explode=(60, -40, 0)),
        part("label_prod", "Product label", color="#F59E0B", explode=(60, -40, 0))],
       "enclosure onto the plate",
       "Four M4 screws from inside into the plate; modules on their bosses; product label on the right side", elev=18, azim=-62, label_done=False)
    encl_done = part("encl", sh=shape("encl", "ctrl", "label_prod"))
    EZ0 = P["encl"][4]
    plug = win(C["led_cable"][1], 55, 90, 5, 35, EZ0 - P["led_plug_h"] - 0.1, EZ0 + 0.1)
    lead = win(C["led_cable"][1], 0, 90, -10, 35, 0, EZ0 - P["led_plug_h"] - 0.1)
    import numpy as np
    keep = bv._anchor
    bv._anchor = lambda v: v[np.argmin(v[:, 2] - 0.01 * v[:, 0])]     # leaders to each part's lowest corner
    st(14, mounted + [encl_done, Part("LED cable", lead, "#D1D5DB", None, (0, 0, 0), 1.0)],
       [Part("LED head plug into its socket", plug, "#B45309", None, (0, 0, -20), 1.0),
        part("lid", "Lid with UV-C label inside", sh=shape("lid", "label_lid"), explode=(60, -50, 0)),
        part("bar", "UV level bar segments", explode=(60, -50, 0))],
       "plug in the LED head, wire up, close the lid",
       "LED head plug into the socket under the enclosure; wire as the wiring diagram; lid with four M3 screws", elev=18, azim=-62, label_done=False)
    bv._anchor = keep
    boxed = mounted + [part("encl", sh=shape("encl", "lid", "bar", "ctrl", "label_prod", "led_cable"))]
    st(15, boxed, [part("flow", "Flow sensor", explode=(-60, 0, 0)), part("valve", "Solenoid valve", explode=(-60, 0, 0))],
       "flow sensor and valve onto the stems and saddles",
       "Push each onto its adaptor stem until it stops, arrows pointing up the water path; one cable tie each",
       elev=18, azim=-118, label_done=False)
    lines = win(fit, -200, -105, -15, 15, 0, 400)
    st(16, boxed + [part("flow"), part("valve")],
       [Part("Supply and outlet lines", lines, C["fittings"][3], None, (-60, 0, 0), 1.0), part("adapter", "24 V adapter", explode=(60, 0, 0))],
       "water lines and the 24 V adapter",
       "Supply from the cold-line tee (after the pre-filter and pressure limiter); outlet to the faucet; adapter on the floor",
       context=[flr()], elev=18, azim=-62, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 72); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 70, "LumaFlow prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 66.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((21, 12), 53, 50, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(22.5, 60.8, "Inside the enclosure (closing the lid closes the reed switch)", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.3, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY = "#B91C1C", "#1D4ED8", "#6B7280"
    blk(2, 46, 14, 11, "24 V adapter", "certified, 30 W,\non a GFCI or RCD\noutlet", "#4B5563")
    blk(24, 46, 14, 11, "Input fuse", "1.6 A on the\n24 V bus", "#7C3AED")
    blk(48, 46, 22, 11, "Controller module", "microcontroller; inputs for\nflow, sensor, NTC, lid,\nLED head loop", "#15803D")
    blk(24, 24, 16, 12, "LED driver", "350 mA constant\ncurrent, dimming in;\nfed through the\nlid reed switch", "#15803D")
    blk(48, 24, 22, 12, "Valve and display drivers", "MOSFET for the valve,\nbuzzer, five-segment\nUV level bar", "#15803D")
    blk(88, 48, 28, 9, "LED head", "6 LEDs in series, NTC on the board;\n6-pin plug under the enclosure", "#7C3AED")
    blk(88, 35, 28, 9, "Dose sensor amplifier", "photodiode in the boss;\n3-way: 5 V, 0 V, signal", "#D4A017")
    blk(88, 22, 13, 9, "Flow sensor", "3-way: 5 V,\n0 V, pulse", "#0F766E")
    blk(103, 22, 13, 9, "Valve", "24 V, 0.2 A,\nnormally closed", "#C2410C")
    wire([(16, 51.5), (24, 51.5)], RED); lab(20, 54.5, "24 V,\n0.75 mm²", RED, "center")
    wire([(38, 51.5), (48, 51.5)], RED); lab(43, 54, "0.5 mm²", RED, "center")
    wire([(31, 46), (31, 36)], RED); lab(31.6, 41, "24 V via the\nreed switch", RED)
    wire([(48, 48), (44, 48), (44, 30), (40, 30)], GRY, 1.2); lab(44.6, 38, "dim", GRY)
    wire([(59, 46), (59, 36)], GRY, 1.2); lab(59.6, 41, "gate signals", GRY)
    wire([(70, 54.6), (88, 54.6)], GRY, 1.2); wire([(70, 52.4), (88, 52.4)], "#B45309", 1.4)
    lab(79, 57.6, "NTC, 0.25 mm²", GRY, "center"); lab(79, 51.0, "interlock loop, 0.25 mm²", "#B45309", "center")
    wire([(70, 49.5), (80, 49.5), (80, 39.5), (88, 39.5)], BLU, 1.4); lab(80.6, 44.5, "sensor,\nscreened", BLU)
    wire([(70, 27), (88, 27)], BLU, 1.4); lab(79, 28.8, "pulse, 0.25 mm²", BLU, "center")
    wire([(66, 24), (66, 20), (109.5, 20), (109.5, 22)], RED); lab(76, 21.6, "valve, 0.5 mm²", RED)
    wire([(32, 24), (32, 17), (118, 17), (118, 52.5), (116, 52.5)], RED); lab(52, 15.4, "LED string, 0.5 mm²", RED)
    ax.text(2, 8.6, "Safety: the LEDs run only with the lid reed switch closed and the LED head's loop complete; unplugging the head stops them.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(2, 5.4, "Red: power. Blue: signal. Grey: sensing and control. Amber: interlock loop, two cores in the LED head cable joined on the LED board. 24 V DC or less; "
            "mains stays in the certified adapter.", fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    if args[0] in ("sheets", "steps", "joints") and len(args) > 1:
        print(fns[args[0]](only=args[1:]))
    else:
        for w in args:
            print(w, "->", fns[w]())
