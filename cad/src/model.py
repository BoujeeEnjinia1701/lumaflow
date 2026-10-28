"""LumaFlow parametric model (build123d), TRL 3, constructable design.
Revised for LMF-DDR-002 (2026-09-25): 50 mm bore, high-reflectance PTFE liner, wall dose sensor at mid height.
Revised for LMF-DDR-003 (2026-10-01): design for construction. The window drops in from below and is
clamped by a retaining ring; the tube seats in both caps on face O-rings; the tie rods are studs in the
lower cap; the LED head is screwed to the lower cap; the ports are threaded for push-fit stem adaptors;
the upper cap roof is 13 mm thick; the sensor sits in a welded boss; the bracket is a drilled plate with
two bought pipe clamps, two printed saddles and the enclosure screwed straight to it.
Revised for the decisions of 2026-10-02 (LMF-DEC-001): the window sits on a 0.5 mm PTFE washer on the
retaining ring (LED gap 0.8 to 1.3 mm); the LED head has a cable with a plug on the enclosure underside,
carrying an interlock loop and too short for the head to come off while plugged in; the enclosure lid
carries a five-segment UV level bar in place of the single light pipe; UV-C warning labels sit on the
lower cap and inside the lid, and the product label on the enclosure side.

Run from the repo root:  python cad/src/model.py            exports STEP and STL and prints the checks
                         python cad/src/model.py --check    prints the constructability checks only
Exports into cad/step and cad/stl:
    lumaflow-assembly.step / .stl     whole unit on its wall bracket, adapter on the cabinet floor
    reactor.step / .stl               tube, PTFE liner and top disc, end caps, quartz window, retainer, rods
    led-head.step / .stl              LED board, heat spreader ring and finned heat sink

Axes: Z up along the reactor axis (water flows upward, LEDs at the bottom shine up),
X to the right (-X is the plumbing side), Y toward the cabinet wall (+Y). Z = 0 is the bottom of the
heat sink fins; the cabinet floor is 25 mm lower. Units mm. BOM line numbers match bom/bom.csv.

Kit 1.9 (2026-10-25): the model carries the kit 1.9 interface (STANDARDS section 24): OPTIONS, PRINCIPLES,
CHOSEN, OPTION_VIEWS, ALLOWED_CONTACTS and components(option), which returns cad_parts.part() dicts for every
concept option at detail level D3 (LMF-OPT-001): A, the axial UV-C LED reactor (the design above, unchanged
in every dimension), B, a hollow-fibre ultrafilter, and C, a radial UV-C LED reactor. Option A is built from
named sub-parts (every screw, stud, washer, nut, insert, weld bead, PCB and connector); build_parts() unions
them into the legacy parts that sizing.py, sheets.py and the media scripts read. Window gasket and sensor
window washer are expanded PTFE (STEM fix, LMF-DEC-001, 2026-10-25).
    python .kit/cad_check.py --export   fidelity check, STEP per part (chosen option) and per option assembly

Main dimensions and interfaces; no tolerances before TRL 4; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (LMF-CAL-001).
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # water channel and reactor tube (bore widened from 25 to 50 mm by LMF-DDR-002)
    "bore_d": 50.0,          # high-reflectance PTFE liner bore = water channel diameter
    "liner_od": 59.0,        # PTFE liner outside diameter = tube inside diameter
    "liner_top_od": 56.0,    # liner turned down above the tube, inside the upper cap (LMF-DDR-003)
    "liner_ext": 24.0,       # liner length above the tube's visible top, into the upper cap
    "tube_od": 65.0,         # 316 stainless reactor tube, 3 mm wall
    "tube_len": 200.0,       # tube visible between the end caps
    "tube_seat": 2.0,        # depth the tube sits into each cap (cut length tube_len + 2 x tube_seat)
    # end caps (lower: 316 stainless; upper: acetal shielded by PTFE), tie rods
    "cap_d": 90.0, "cap_lo_h": 30.0, "cap_hi_h": 40.0,   # upper cap 30 to 40 mm: 13 mm roof (LMF-DDR-003)
    "top_disc_t": 3.0,       # PTFE disc closing the channel under the upper cap
    "rod_d": 5.0, "rod_pcr": 40.0, "n_rod": 4,   # M5 316 studs on a 40 mm pitch radius (39 before LMF-DDR-003)
    "rod_engage": 12.0,      # stud thread depth in the lower cap
    "oring_cs": 1.78,        # tube-to-cap face O-ring cross-section
    # quartz window, retaining ring and gasket, LED head
    "win_d": 57.0, "win_t": 10.0,
    "aperture_d": 51.0,      # unsupported window diameter = retaining ring bore
    "ret_od": 72.0, "ret_t": 2.0, "ret_pcr": 32.5, "n_ret": 6,   # 316 retaining ring, six M3 countersunk screws
    "gasket_t": 1.0,         # EPDM gasket between the window top and the cap shoulder
    "washer_t": 0.5,         # PTFE washer between the retaining ring and the window (2026-10-02); LED gap 1.3 mm
    "led_n": 6, "led_pcr": 16.0, "led_size": 3.5, "led_h": 1.2,
    "board_d": 44.0, "board_t": 3.0,
    # heat sink (under the LED board) and spreader ring (sink base to lower cap)
    "sink_w": 90.0, "sink_base": 6.0, "fin_h": 24.0, "fin_t": 3.0, "n_fins": 9,
    "head_screw_y": 36.0,    # four M4 screws from below, in fin gaps, into the lower cap
    # ports: 3/8 in (9.5 mm) tube, 7 mm bore; heights above the window top and below the top disc
    "port_od": 9.525, "port_bore": 7.0, "port_in_dz": 6.5, "port_out_dz": 9.0,   # inlet kept 19 mm up the cap
    "boss_d": 20.0,          # port boss, tapped 1/4 BSPP for a push-fit stem adaptor
    # UV-C photodiode window in the tube wall at mid height of the channel, facing +X (LMF-DDR-002)
    "det_win_d": 8.0,
    # electronics enclosure (right of the reactor), X0, X1, Y0, Y1, Z0, Z1; back face on the bracket plate
    "encl": (62.0, 122.0, 5.0, 49.0, 100.0, 230.0),
    # LED head cable (2026-10-02): flat run through the spreader ring slot, round 6-core cable to a 6-pin plug
    # on the enclosure underside (X, Y of the socket); the plug carries the interlock loop
    "led_plug_xy": (70.0, 20.0), "led_plug_d": 15.0, "led_plug_h": 12.0, "led_cable_d": 4.5,
    "led_cable_len": 95.0,   # board edge to plug, as bought or made up
    # five-segment UV level bar on the enclosure lid (R18): segment width, gap, height
    "bar_n": 5, "bar_w": 6.0, "bar_gap": 2.0, "bar_h": 8.0,
    # wall bracket: plate Y and outline, pipe clamp heights
    "bracket_y": (49.0, 55.0), "plate_x": (-112.0, 130.0), "plate_z": (30.0, 300.0),
    "ring_z": (95.0, 225.0), "ring_od": 71.0, "ring_h": 20.0,
    "floor_gap": 25.0,       # air gap under the fins, to the cabinet floor
}


def levels(P=PARAMS):
    """Key heights (mm) derived from PARAMS. Used by the drawing sheet and the calc note."""
    L = {}
    L["z_sink0"] = 0.0
    L["z_sink1"] = P["fin_h"] + P["sink_base"]                  # top of sink base, 30
    L["z_board1"] = L["z_sink1"] + P["board_t"]                 # top of LED board = lower cap bottom, 33
    L["z_led1"] = L["z_board1"] + P["led_h"]
    L["z_ret1"] = L["z_board1"] + P["ret_t"]                    # retaining ring top
    L["z_win0"] = L["z_ret1"] + P["washer_t"]                   # window underside, on the PTFE washer
    L["led_gap"] = L["z_win0"] - L["z_led1"]                    # LED top to window underside, 1.3
    L["z_win1"] = L["z_win0"] + P["win_t"]                      # window top = channel bottom
    L["z_bore0"] = L["z_win1"] + P["gasket_t"]                  # cap shoulder above the gasket
    L["z_cap0"] = L["z_board1"] + P["cap_lo_h"]                 # lower cap top = visible tube bottom
    L["z_cap1"] = L["z_cap0"] + P["tube_len"]                   # visible tube top = upper cap bottom
    L["z_tube0"] = L["z_cap0"] - P["tube_seat"]
    L["z_tube1"] = L["z_cap1"] + P["tube_seat"]
    L["z_top"] = L["z_cap1"] + P["cap_hi_h"]                    # upper cap top
    L["z_disc0"] = L["z_cap1"] + P["liner_ext"]                 # channel top
    L["z_disc1"] = L["z_disc0"] + P["top_disc_t"]               # top disc top face
    L["roof_t"] = L["z_top"] - L["z_disc1"]                     # acetal over the liner pocket
    L["z_in"] = L["z_win1"] + P["port_in_dz"]
    L["z_out"] = L["z_disc0"] - P["port_out_dz"]
    L["channel_len"] = L["z_disc0"] - L["z_win1"]               # irradiated water column
    L["flow_len"] = L["z_out"] - L["z_in"]                      # inlet to outlet
    L["steel_len"] = L["z_cap0"] - L["z_win1"]                  # channel length with a stainless wall
    L["z_det"] = (L["z_win1"] + L["z_disc0"]) / 2               # wall dose sensor, mid height of the channel
    return L


def _fin_gap_x(P=PARAMS):
    """Centre of the second fin gap from the middle: where the LED-head screws pass."""
    pitch = (P["sink_w"] - P["fin_t"]) / (P["n_fins"] - 1)
    xs = [-P["sink_w"] / 2 + i * pitch for i in range(P["n_fins"])]
    gaps = sorted((xs[i] + P["fin_t"] + xs[i + 1]) / 2 for i in range(P["n_fins"] - 1))
    pos = [g for g in gaps if g > 1]
    return pos[1], pitch - P["fin_t"]


def positions(P=PARAMS):
    """Hole and fixing positions shared by the model, the sketches and the checks."""
    rods = [(P["rod_pcr"] * math.cos(math.radians(45 + 90 * i)), P["rod_pcr"] * math.sin(math.radians(45 + 90 * i)))
            for i in range(P["n_rod"])]
    ret = [(P["ret_pcr"] * math.cos(math.radians(30 + 60 * i)), P["ret_pcr"] * math.sin(math.radians(30 + 60 * i)))
           for i in range(P["n_ret"])]
    gx, gap = _fin_gap_x(P)
    head = [(sx * gx, sy * P["head_screw_y"]) for sx in (1, -1) for sy in (1, -1)]
    board = [(19 * math.cos(math.radians(a)), 19 * math.sin(math.radians(a))) for a in (30, 150, 270)]
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    encl = [(x, z) for x in (EX0 + 8, EX1 - 8) for z in (EZ0 + 8, EZ1 - 8)]
    px0, px1 = P["plate_x"]; pz0, pz1 = P["plate_z"]
    wall = [(px0 + 7, pz0 + 10), (px0 + 7, pz1 - 10), (px1 - 8, pz0 + 10), (px1 - 8, pz1 - 10)]
    bw, bg, bh = P["bar_w"], P["bar_gap"], P["bar_h"]
    bx0 = (EX0 + EX1) / 2 - (P["bar_n"] * bw + (P["bar_n"] - 1) * bg) / 2
    bar = [(bx0 + i * (bw + bg), bx0 + i * (bw + bg) + bw, EZ1 - 30, EZ1 - 30 + bh) for i in range(P["bar_n"])]
    return {"rods": rods, "ret": ret, "head": head, "fin_gap": gap, "board": board, "encl": encl, "wall": wall, "bar": bar,
            "clamps": [(0.0, z) for z in P["ring_z"]]}


# ------------------------------------------------------------------ kit 1.9 interface (STANDARDS section 24)
TITLE = "LumaFlow"
OPTIONS = {"A": "Axial UV-C LED reactor", "B": "Hollow-fibre ultrafilter", "C": "Radial UV-C LED reactor"}
PRINCIPLES = {
    "A": "Six 275 nm LEDs under a quartz window shine up a 50 mm PTFE-lined tube; the reflective wall returns the light "
         "until the water absorbs it. A flow switch runs the LEDs and a wall photodiode closes a valve on low dose.",
    "B": "Water is pushed through hollow fibres with 0.02 µm pores, which hold back bacteria and protozoa by size. No power "
         "treats the water; two gauges show fouling and a hand-pump pressure-decay test checks the fibres are intact.",
    "C": "Water flows up a 20 mm fused quartz tube while twelve 275 nm LEDs on four air-cooled strips shine across it "
         "from outside. The LEDs stay dry and no seal sits in the light path below them.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 24, "az": -40, "scale": "person", "ground_z": -25.0} for k in OPTIONS}
# Pairs whose solids may share volume: weld beads fill the corner they join; heat-set inserts are pressed into
# printed plastic; threads are drawn at the minor diameter in tapped holes (no shared volume, listed for safety).
ALLOWED_CONTACTS = [("weld", "Reactor tube"), ("weld", "Sensor boss"), ("weld", "Flange"), ("weld", "body")]

# Extra parameters for options B and C (option A's parameters above are unchanged)
PARAMS.update({
    # option B: 2.5 x 10 in (slim) filter housing with a hollow-fibre UF cartridge, axis at (0, b_y)
    "b_y": -12.0, "b_head_w": 118.0, "b_head_h": 52.0, "b_bowl_od": 112.0, "b_bowl_h": 262.0, "b_bowl_t": 4.0,
    "b_cart_od": 70.0, "b_cart_len": 250.0, "b_z0": 90.0,
    # option C: 20 mm ID fused quartz flow tube between two 316 end fittings with flanges, 12 LEDs on 4 strips
    "c_tube_od": 24.0, "c_tube_id": 20.0, "c_body_r": 18.0, "c_flange_r": 35.0, "c_flange_t": 6.0,
    "c_z_lo": (13.0, 73.0), "c_z_hi": (253.0, 320.0), "c_board_x": 18.0, "c_led_n": 3, "c_rod_r": 30.0,
})


def _geo():
    from build123d import Box, Cylinder, Plane, Polygon, Pos, Rot, Solid, Sphere, Torus, Vector, extrude, Cone

    def box(x0, x1, y0, y1, z0, z1):
        return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)

    def zcyl(r, z0, z1, x=0.0, y=0.0):
        return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)

    def xcyl(r, x0, x1, y=0.0, z=0.0):
        return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)

    def ycyl(r, y0, y1, x=0.0, z=0.0):
        return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)

    def ring(r0, r1, z0, z1, x=0.0, y=0.0):
        return zcyl(r1, z0, z1, x, y) - zcyl(r0, z0 - 1, z1 + 1, x, y)

    def xring(r0, r1, x0, x1, y=0.0, z=0.0):
        return xcyl(r1, x0, x1, y, z) - xcyl(r0, x0 - 1, x1 + 1, y, z)

    def yring(r0, r1, y0, y1, x=0.0, z=0.0):
        return ycyl(r1, y0, y1, x, z) - ycyl(r0, y0 - 1, y1 + 1, x, z)

    def rod(p0, p1, r):
        p0, p1 = Vector(*p0), Vector(*p1)
        return Solid.make_cylinder(r, (p1 - p0).length, Plane(origin=p0, z_dir=(p1 - p0).normalized()))

    def ycone(r_small, r_big, y_small, y_big, x=0.0, z=0.0):
        """Cone along Y from r_small at y_small to r_big at y_big (countersinks)."""
        h = abs(y_big - y_small)
        c = Cone(r_small, r_big, h)                      # along +Z, small end at -h/2
        return Pos(x, (y_small + y_big) / 2, z) * Rot(-90 if y_big > y_small else 90, 0, 0) * c

    def sector(r0, r1, z0, z1, ang_c, half):
        Rr = r1 * 1.5
        pts = [(0.0, 0.0)] + [(Rr * math.cos(math.radians(ang_c - half + 2 * half * i / 12)),
                               Rr * math.sin(math.radians(ang_c - half + 2 * half * i / 12))) for i in range(13)]
        wedge = Pos(0, 0, z0) * extrude(Polygon(*pts, align=None), amount=z1 - z0)
        return ring(r0, r1, z0, z1) & wedge

    def plate_y(x0, x1, y0, y1, z0, z1, r=2.0):
        """Plate in the XZ plane, Y thickness, rounded corners (labels, small plates)."""
        from build123d import RectangleRounded
        sk = Plane.XZ * RectangleRounded(x1 - x0, z1 - z0, min(r, (x1 - x0) / 2 - 0.01, (z1 - z0) / 2 - 0.01))
        s = extrude(sk, amount=y1 - y0)
        bb = s.bounding_box()
        return Pos((x0 + x1) / 2 - bb.center().X, y0 - bb.min.Y, (z0 + z1) / 2 - bb.center().Z) * s

    def plate_x(x0, x1, y0, y1, z0, z1, r=2.0):
        """Plate in the YZ plane, X thickness, rounded corners."""
        from build123d import RectangleRounded
        sk = Plane.YZ * RectangleRounded(y1 - y0, z1 - z0, min(r, (y1 - y0) / 2 - 0.01, (z1 - z0) / 2 - 0.01))
        s = extrude(sk, amount=x1 - x0)
        bb = s.bounding_box()
        return Pos(x0 - bb.min.X, (y0 + y1) / 2 - bb.center().Y, (z0 + z1) / 2 - bb.center().Z) * s

    def hexy(s_flats, y0, y1, x=0.0, z=0.0):
        """Hex prism along Y (nuts, adaptor bodies)."""
        from build123d import RegularPolygon
        h = extrude(Plane.XZ * RegularPolygon(s_flats / math.sqrt(3), 6), amount=y1 - y0)
        bb = h.bounding_box()
        return Pos(x - bb.center().X, y0 - bb.min.Y, z - bb.center().Z) * h

    def hexx(s_flats, x0, x1, y=0.0, z=0.0):
        from build123d import RegularPolygon
        h = extrude(Plane.YZ * RegularPolygon(s_flats / math.sqrt(3), 6), amount=x1 - x0)
        bb = h.bounding_box()
        return Pos(x0 - bb.min.X, y - bb.center().Y, z - bb.center().Z) * h

    def hexz(s_flats, z0, z1, x=0.0, y=0.0):
        from build123d import RegularPolygon
        return Pos(x, y, z0) * extrude(RegularPolygon(s_flats / math.sqrt(3), 6), amount=z1 - z0)

    return dict(box=box, zcyl=zcyl, xcyl=xcyl, ycyl=ycyl, ring=ring, xring=xring, yring=yring, rod=rod,
                ycone=ycone, sector=sector, plate_y=plate_y, plate_x=plate_x, hexy=hexy, hexx=hexx, hexz=hexz,
                Pos=Pos, Rot=Rot, Sphere=Sphere, Torus=Torus)


def _chamfer(shape, r):
    try:
        import cad_parts
        return cad_parts.break_edges(shape, r)
    except Exception:
        return shape


# Sub-part record: (key, name, shape, bom, kind, material, group). `key` groups sub-parts into the legacy parts of
# build_parts(); components() lists every sub-part on its own.
def _periphery(P, clamp_z, clamp_r, xs, encl_lid_label=True, socket=True, plate_z=None):
    """Bracket plate with saddles, enclosure with controller, flow sensor, valve, adapter and the fasteners that
    hold them; shared by options A and C (clamp heights and radius differ)."""
    g = _geo(); box, zcyl, xcyl, ycyl, ring, yring = g["box"], g["zcyl"], g["xcyl"], g["ycyl"], g["ring"], g["yring"]
    L = levels(P)
    H = positions(P)
    out = []
    add = lambda *a: out.append(a)
    # 13 Electronics enclosure: printed PETG body (2.5 mm walls) with lid screw bosses, cable gland hole, LED head
    #    socket hole and four holes in the back; front lid with five segment windows; gland, socket, screws
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    ym = (EY0 + EY1) / 2
    lid_pts = [(EX0 + 6, EZ0 + 30), (EX1 - 6, EZ0 + 30), (EX0 + 6, EZ1 - 9), (EX1 - 6, EZ1 - 9)]
    body = box(EX0, EX1, EY0 + 2.5, EY1, EZ0, EZ1) - box(EX0 + 2.5, EX1 - 2.5, EY0 + 2.4, EY1 - 2.5, EZ0 + 2.5, EZ1 - 2.5)
    for x, z in lid_pts:
        body = body + ycyl(3.5, EY0 + 2.5, EY0 + 14, x=x, z=z)
    for x, z in lid_pts:
        body = body - ycyl(1.25, EY0 + 2.4, EY0 + 14.5, x=x, z=z)
    for x, z in H["encl"]:
        body = body - ycyl(2.2, EY1 - 3, EY1 + 1, x=x, z=z)
    lpx, lpy = P["led_plug_xy"]
    body = body - zcyl(6.0, EZ0 - 1, EZ0 + 3, lpx, lpy)
    body = body - xcyl(4.0, EX0 - 1, EX0 + 3.5, y=ym, z=EZ0 + 20)
    add("encl", "Enclosure body, printed PETG", body, 13, "made", "hdpe_natural", "shell")
    gland = xcyl(4.0, EX0 - 8, EX0 + 2.5, y=ym, z=EZ0 + 20) + g["hexx"](10, EX0 - 12, EX0 - 8, y=ym, z=EZ0 + 20)
    gland = gland - xcyl(2.0, EX0 - 13, EX0 + 3, y=ym, z=EZ0 + 20)
    add("encl", "Cable gland, M8, nylon", gland, 13, "bought", "matte_black", "shell")
    lid = box(EX0, EX1, EY0, EY0 + 2.5, EZ0, EZ1)
    for x0, x1, z0, z1 in H["bar"]:
        lid = lid - box(x0, x1, EY0 - 1, EY0 + 3.5, z0, z1)
    for x, z in lid_pts:
        lid = lid - ycyl(1.7, EY0 - 1, EY0 + 3.5, x=x, z=z)
    add("lid", "Enclosure lid, printed PETG", lid, 13, "made", "hdpe_natural", "shell")
    bar = None
    for x0, x1, z0, z1 in H["bar"]:
        seg = box(x0, x1, EY0 - 1.0, EY0 + 2.5, z0, z1)
        bar = seg if bar is None else bar + seg
    add("bar", "UV level bar light-pipe segments", bar, 13, "bought", "polycarbonate", "shell")
    bx0 = H["bar"][0][0] - 1; bx1 = H["bar"][-1][1] + 1
    zb0 = H["bar"][0][2] - 2; zb1 = H["bar"][0][3] + 2
    add("bar", "UV level bar LED module (5-LED PCB)", _chamfer(box(bx0, bx1, EY0 + 2.5, EY0 + 4.1, zb0, zb1), 0.4), 13, "bought", "hdpe_recycled", "internal")
    for i, (x, z) in enumerate(lid_pts, 1):
        s = ycyl(2.75, EY0 - 2.0, EY0, x=x, z=z) + ycyl(1.25, EY0, EY0 + 10.0, x=x, z=z)
        add("lid_screws", f"Lid screw M3 x 12 pan head {i}", s, 16, "fastener", "stainless", "shell")
    for i, (x, z) in enumerate(H["encl"], 1):
        s = ycyl(3.5, EY1 - 5.2, EY1 - 2.5, x=x, z=z) + ycyl(1.62, EY1 - 2.5, EY1 + 6.0, x=x, z=z)
        add("encl_screws", f"Enclosure screw M4 x 10 pan head {i}", s, 16, "fastener", "stainless", "internal")
    if socket:
        sk = zcyl(5.95, EZ0, EZ0 + 2.5, lpx, lpy) + zcyl(5.0, EZ0 + 2.5, EZ0 + 14, lpx, lpy)
        add("socket", "LED head panel socket, 6-pin GX12 class", sk, 10, "bought", "zinc_plated", "internal")
    # 10 Controller: carrier PCB on standoffs, MCU module, LED driver module, buzzer, reed switch and lid magnet
    cy0, cy1 = EY1 - 7.5, EY1 - 5.5
    so_pts = [(EX0 + 12, EZ0 + 16), (EX1 - 12, EZ0 + 16), (EX0 + 12, EZ1 - 16), (EX1 - 12, EZ1 - 16)]
    carrier = box(EX0 + 6, EX1 - 6, cy0, cy1, EZ0 + 8, EZ1 - 8)
    for x, z in so_pts:
        carrier = carrier - ycyl(1.6, cy0 - 1, cy1 + 1, x=x, z=z)
    add("ctrl", "Controller carrier PCB", carrier, 10, "bought", "hdpe_recycled", "internal")
    for i, (x, z) in enumerate(so_pts, 1):
        add("ctrl", f"PCB standoff {i}", yring(1.25, 2.5, cy1, EY1 - 2.5, x=x, z=z), 10, "bought", "brass", "internal")
        sc = ycyl(2.75, cy0 - 2.0, cy0, x=x, z=z) + ycyl(1.25, cy0, cy1 + 2.5, x=x, z=z)
        add("ctrl_screws", f"PCB screw M2.5 x 6 {i}", sc, 16, "fastener", "stainless", "internal")
    add("ctrl", "Microcontroller module", box(72, 96, cy0 - 6.5, cy0 - 4.9, 150, 200)
        + box(73, 75, cy0 - 4.9, cy0, 152, 198) + box(93, 95, cy0 - 4.9, cy0, 152, 198), 10, "bought", "hdpe_recycled", "internal")
    add("ctrl", "LED driver module, 350 mA constant current", box(98, 112, cy0 - 6.5, cy0 - 4.9, 120, 145)
        + box(99, 111, cy0 - 4.9, cy0, 121, 123) + ycyl(4.0, cy0 - 10.5, cy0 - 6.5, x=105, z=135), 10, "bought", "hdpe_recycled", "internal")
    add("ctrl", "Buzzer", ycyl(6.0, cy0 - 8.0, cy0, x=80, z=130) - ycyl(1.0, cy0 - 8.5, cy0 - 6, x=80, z=130), 10, "bought", "matte_black", "internal")
    add("ctrl", "Lid reed switch", box(84, 96, cy0 - 2.0, cy0, 212, 217) + ycyl(1.0, cy0 - 2.5, cy0 - 2.0, x=90, z=214.5), 10, "bought", "glass", "internal")
    add("ctrl", "Lid interlock magnet", _chamfer(box(84, 96, EY0 + 2.5, EY0 + 5.5, 212, 217), 0.5), 13, "bought", "mild_steel", "internal")
    # 14 Wall bracket plate (6 mm aluminium) and two printed saddles with brass heat-set inserts
    by0, by1 = P["bracket_y"]
    px0, px1 = P["plate_x"]; pz0, pz1 = plate_z or P["plate_z"]
    plate = g["plate_y"](px0, px1, by0, by1, pz0, pz1, r=6.0)
    for x, z in H["wall"]:
        plate = plate - ycyl(2.75, by0 - 1, by1 + 1, x=x, z=z)
    for z in clamp_z:
        plate = plate - ycyl(3.4, by0 - 1, by1 + 1, x=0.0, z=z)
    for x, z in H["encl"]:
        plate = plate - ycyl(1.62, by0 - 1, by1 + 1, x=x, z=z)
    sx0, sx1 = xs + 10, xs + 30
    sxm = (sx0 + sx1) / 2
    saddle_pts = [(sxm, zz + dz) for zz in (L["z_in"], L["z_out"]) for dz in (-7, 7)]
    for x, z in saddle_pts:
        plate = plate - ycyl(2.25, by0 - 1, by1 + 1, x=x, z=z) - g["ycone"](2.25, 4.2, by1 - 1.95, by1 + 0.01, x=x, z=z)
    add("bracket", "Bracket plate, 6 mm aluminium", plate, 14, "made", "aluminium", "shell")
    for zz in (L["z_in"], L["z_out"]):
        sd = box(sx0, sx1, 14, by0, zz - 14, zz + 14) - box(sx0 + 6, sx1 - 6, 20, 24, zz - 15, zz + 15)
        for dz in (-7, 7):
            sd = sd - ycyl(2.8, by0 - 8.5, by0 + 1, x=sxm, z=zz + dz)
        add("saddles", f"Saddle, printed PETG, {'flow sensor' if zz == L['z_in'] else 'valve'}", _chamfer(sd, 0.8), 14, "made", "hdpe_natural", "shell")
    for i, (x, z) in enumerate(saddle_pts, 1):
        add("inserts", f"Heat-set insert M4, brass {i}", yring(2.0, 2.8, by0 - 8, by0, x=x, z=z), 14, "fastener", "brass", "shell")
        sc = ycyl(2.0, by0 - 8, by1 - 2.0, x=x, z=z) + g["ycone"](2.0, 4.0, by1 - 2.0, by1, x=x, z=z)
        add("saddle_screws", f"Saddle screw M4 x 12 countersunk {i}", sc, 16, "fastener", "stainless", "shell")
    for i, (x, z) in enumerate(H["wall"], 1):
        sc = ycyl(5.0, by0 - 3.5, by0, x=x, z=z) + ycyl(2.5, by0, by1 + 30, x=x, z=z)
        add("wall_screws", f"Wall screw 5 x 40 pan head {i}", sc, 16, "fastener", "zinc_plated", "shell")
    # 8 Hall-effect flow sensor (inlet) and 11 normally closed solenoid valve (outlet), on the saddles
    zi, zo = L["z_in"], L["z_out"]
    fb = _chamfer(box(xs, xs + 40, -14, 14, zi - 14, zi + 14), 2.0) + zcyl(8, zi + 14, zi + 24, x=xs + 20)
    add("flow", "Hall-effect flow sensor, 3/8 in push-fit", fb, 8, "bought", "hdpe_natural", "shell")
    vb = (_chamfer(box(xs, xs + 40, -14, 14, zo - 14, zo + 14), 2.0) + zcyl(14, zo + 14, zo + 44, x=xs + 20))
    add("valve", "Solenoid valve, 24 V DC, normally closed", vb, 11, "bought", "matte_black", "shell")
    # 15 Supply and faucet lines (3/8 in food-grade tube) into the sensor and the valve
    add("fittings", "3/8 in food-grade tube to the supply", g["xring"](3.2, P["port_od"] / 2, xs - 40, xs, z=zi), 15, "bought", "hdpe_natural", "shell")
    # faucet line with the push-fit tee and the outlet pressure sensor that starts the unit (STEM fix D-S3, 2026-10-25):
    # with the valve shut in standby, opening the faucet drops this line's pressure, which wakes the controller
    add("fittings", "3/8 in food-grade tube to the faucet", g["xring"](3.2, P["port_od"] / 2, xs - 40, xs - 30, z=zo), 15, "bought", "hdpe_natural", "shell")
    add("fittings", "3/8 in food-grade tube, tee to valve", g["xring"](3.2, P["port_od"] / 2, xs - 10, xs, z=zo), 15, "bought", "hdpe_natural", "shell")
    tee = xcyl(7.0, xs - 30, xs - 10, z=zo) + zcyl(6.0, zo - 22, zo, x=xs - 20)
    tee = tee - xcyl(3.2, xs - 31, xs - 9, z=zo) - zcyl(3.0, zo - 23, zo, x=xs - 20)
    add("psensor", "Push-fit tee for the outlet pressure sensor", tee, 20, "bought", "hdpe_natural", "shell")
    ps = g["hexz"](14, zo - 32, zo - 22, x=xs - 20) + zcyl(9.0, zo - 62, zo - 32, x=xs - 20) + zcyl(4.0, zo - 70, zo - 62, x=xs - 20)
    add("psensor", "Outlet pressure sensor 0 to 10 bar, 5 V", ps, 20, "bought", "stainless", "shell")
    # 12 24 V DC adapter on the cabinet floor
    fz = -P["floor_gap"]
    add("adapter", "24 V DC power adapter, 30 W", _chamfer(box(150, 245, -30, 20, fz, fz + 34), 4.0), 12, "bought", "matte_black", "accessory")
    # 19 Product label on the enclosure side, UV-C label inside the lid
    if encl_lid_label:
        add("label_lid", "UV-C warning label, inside the lid", g["plate_y"](EX0 + 12, EX1 - 12, EY0 + 2.5, EY0 + 2.7, EZ0 + 55, EZ0 + 85, 2.0), 19, "bought", "label", "internal")
    add("label_prod", "Product label", g["plate_x"](EX1, EX1 + 0.2, EY0 + 10, EY1 - 6, EZ0 + 40, EZ0 + 90, 2.0), 19, "bought", "label", "shell")
    # 18 Rubber-lined pipe clamps on M8 studs into the plate
    rr = clamp_r + 3.0
    for i, z in enumerate(clamp_z, 1):
        liner = ring(clamp_r, clamp_r + 1.0, z - P["ring_h"] / 2, z + P["ring_h"] / 2)
        band = ring(clamp_r + 1.0, rr, z - P["ring_h"] / 2, z + P["ring_h"] / 2) + (box(-9, 9, rr - 1, rr + 6, z - 8, z + 8) - zcyl(rr - 0.01, z - 9, z + 9))
        band = band - ycyl(3.4, rr - 0.5, rr + 7, z=z)
        add("clamps", f"Pipe clamp band with M8 boss {i}", band, 18, "bought", "stainless", "shell")
        add("clamps", f"Pipe clamp rubber liner {i}", liner, 18, "bought", "epdm", "shell")
        add("clamps", f"Clamp stud M8 x 20 {i}", ycyl(3.4, rr + 0.5, by1, z=z), 16, "fastener", "stainless", "shell")
        add("clamps", f"Clamp lock nut M8 {i}", g["hexy"](13, rr + 6, rr + 12.8, z=z) - ycyl(3.4, rr + 5, rr + 14, z=z), 16, "fastener", "stainless", "shell")
    return out


def _a_subparts(P=PARAMS):
    """Option A, the constructable design, as sub-parts. Geometry and every dimension as in LMF-DWG-001 Rev P5."""
    g = _geo(); box, zcyl, xcyl, ycyl, ring, rod = g["box"], g["zcyl"], g["xcyl"], g["ycyl"], g["ring"], g["rod"]
    Pos, Rot, Sphere, Torus = g["Pos"], g["Rot"], g["Sphere"], g["Torus"]
    L = levels(P)
    H = positions(P)
    rb, rl, rt, rc = P["bore_d"] / 2, P["liner_od"] / 2, P["tube_od"] / 2, P["cap_d"] / 2
    rlt = P["liner_top_od"] / 2
    rp, rpb = P["port_od"] / 2, P["port_bore"] / 2
    rd, zd = P["det_win_d"] / 2, L["z_det"]
    rbo = P["boss_d"] / 2
    r_thr = 6.6
    r_seat = rt + 0.25
    og0, og1, og_d = 30.0, 32.4, 1.3
    xs = -rc - 62
    xb = -rc - 10
    out = []
    add = lambda *a: out.append(a)

    # 1 Reactor tube (316) and the sensor boss TIG-welded on at mid height, with its weld bead
    tube = zcyl(rt, L["z_tube0"], L["z_tube1"]) - zcyl(rl, L["z_tube0"] - 1, L["z_tube1"] + 1)
    tube = tube - xcyl(rd, rl - 1, rt + 1.5, z=zd)
    add("tube", "Reactor tube, 316, 65 x 3 x 204", tube, 1, "made", "stainless", "shell")
    boss = xcyl(11, rt - 4, rt + 10, z=zd) - zcyl(rt, zd - 12, zd + 12)
    boss = boss - xcyl(rd, rl - 1, rt + 1.5, z=zd) - xcyl(5.1, rt + 1.5, rt + 5, z=zd) - xcyl(6.0, rt + 5, rt + 11, z=zd)
    add("tube", "Sensor boss, 316, welded to the tube", boss, 1, "made", "stainless", "shell")
    bead = (Pos(rt - 0.4, 0, zd) * Rot(0, 90, 0) * Torus(11.0, 2.2)) - zcyl(rt, zd - 16, zd + 16) - xcyl(11, rt - 6, rt + 12, z=zd)
    add("weld", "Fillet weld bead, sensor boss to tube", bead, 1, "weld", "stainless", "shell")
    # 2 High-reflectance PTFE liner with its turned-down top and solid top disc
    liner = (zcyl(rl, L["z_cap0"], L["z_tube1"]) + zcyl(rlt, L["z_tube1"], L["z_disc1"]) - zcyl(rb, L["z_cap0"] - 1, L["z_disc0"]))
    liner = liner - xcyl(rpb, -rl - 1, -rb + 0.5, z=L["z_out"]) - xcyl(rd, rb - 1, rl + 1, z=zd)
    add("liner", "High-reflectance PTFE liner and top disc", liner, 2, "bought", "hdpe_natural", "internal")
    # 3 Quartz window (edges chamfered 0.3 mm)
    add("window", "Quartz window, fused silica 57 x 10", _chamfer(zcyl(P["win_d"] / 2, L["z_win0"], L["z_win1"]), 0.3), 3, "bought", "glass", "internal")
    # 4 LED board: aluminium-core PCB, six 3535 LEDs, NTC sensor
    pcb = zcyl(P["board_d"] / 2, L["z_sink1"], L["z_board1"])
    for x, y in H["board"]:
        pcb = pcb - zcyl(1.7, L["z_sink1"] - 1, L["z_board1"] + 1, x, y)
    add("board", "LED board, 44 mm aluminium-core PCB", pcb, 4, "bought", "aluminium", "internal")
    s = P["led_size"] / 2
    for i in range(P["led_n"]):
        a = 2 * math.pi * i / P["led_n"]
        x, y = P["led_pcr"] * math.cos(a), P["led_pcr"] * math.sin(a)
        add("board", f"UV-C LED 275 nm, 3535 package {i + 1}", box(x - s, x + s, y - s, y + s, L["z_board1"], L["z_led1"] - 0.4)
            + box(x - s + 0.5, x + s - 0.5, y - s + 0.5, y + s - 0.5, L["z_led1"] - 0.4, L["z_led1"]), 4, "bought", "matte_black", "internal")
    add("board", "NTC board temperature sensor, 0603", _chamfer(box(-1.0, 1.0, -0.6, 0.6, L["z_board1"], L["z_board1"] + 0.8), 0.15), 4, "bought", "matte_black", "internal")
    # 5 Heat sink (fins down) and spreader ring
    hw = P["sink_w"] / 2
    sink = box(-hw, hw, -hw, hw, P["fin_h"], L["z_sink1"])
    pitch = (P["sink_w"] - P["fin_t"]) / (P["n_fins"] - 1)
    for i in range(P["n_fins"]):
        x = -hw + i * pitch
        sink = sink + box(x, x + P["fin_t"], -hw, hw, 0, P["fin_h"])
    for x, y in H["head"]:
        sink = sink - zcyl(2.25, P["fin_h"] - 1, L["z_sink1"] + 1, x, y)
    for x, y in H["board"]:
        sink = sink - zcyl(1.25, P["fin_h"] + 1, L["z_sink1"] + 0.1, x, y)
    add("sink", "Heat sink, aluminium 90 x 90 x 30, drilled", sink, 5, "bought", "aluminium", "shell")
    spreader = ring(P["board_d"] / 2 + 0.5, rc, L["z_sink1"], L["z_board1"]) - box(P["board_d"] / 2, rc + 1, -4, 4, L["z_sink1"] - 1, L["z_board1"] + 1)
    for x, y in H["head"]:
        spreader = spreader - zcyl(2.25, L["z_sink1"] - 1, L["z_board1"] + 1, x, y)
    add("sink", "Spreader ring, aluminium 90 x 45 x 3", spreader, 5, "made", "aluminium", "shell")
    # 6 Lower end cap, 316
    zc0, zc1 = L["z_board1"], L["z_cap0"]
    cap_lo = zcyl(rc, zc0, zc1) + xcyl(rbo, xb, -rc + 4, z=L["z_in"])
    cap_lo = (cap_lo - zcyl(P["ret_od"] / 2 + 0.2, zc0 - 1, L["z_ret1"]) - zcyl(P["win_d"] / 2 + 0.5, L["z_ret1"] - 0.1, L["z_bore0"])
              - zcyl(rb, L["z_bore0"] - 0.1, zc1 + 1) - ring(rl, r_seat, L["z_tube0"], zc1 + 1)
              - ring(og0, og1, L["z_tube0"] - og_d, L["z_tube0"] + 0.1) - xcyl(r_thr, xb - 1, xb + 11, z=L["z_in"])
              - xcyl(rpb, xb + 10, -rb + 0.5, z=L["z_in"]))
    for x, y in H["rods"]:
        cap_lo = cap_lo - zcyl(2.1, zc1 - P["rod_engage"], zc1 + 1, x, y)
    for x, y in H["ret"]:
        cap_lo = cap_lo - zcyl(1.25, L["z_ret1"] - 0.1, L["z_ret1"] + 8, x, y)
    for x, y in H["head"]:
        cap_lo = cap_lo - zcyl(1.65, zc0 - 1, zc0 + 10, x, y)
    add("cap_lo", "Lower end cap, 316 stainless", cap_lo, 6, "made", "stainless", "shell")
    # 7 Upper end cap, acetal
    zu0, zu1 = L["z_cap1"], L["z_top"]
    cap_hi = zcyl(rc, zu0, zu1) + xcyl(rbo, xb, -rc + 4, z=L["z_out"])
    cap_hi = (cap_hi - zcyl(r_seat, zu0 - 1, L["z_tube1"]) - ring(og0, og1, L["z_tube1"] - 0.1, L["z_tube1"] + og_d)
              - zcyl(rlt + 0.1, L["z_tube1"] - 0.1, L["z_disc1"]) - xcyl(r_thr, xb - 1, xb + 11, z=L["z_out"])
              - xcyl(rp + 0.05, xb + 10, -rlt, z=L["z_out"]))
    for x, y in H["rods"]:
        cap_hi = cap_hi - zcyl(2.7, zu0 - 1, zu1 + 1, x, y)
    add("cap_hi", "Upper end cap, acetal", cap_hi, 7, "made", "hdpe_black", "shell")
    # 16 Tie rods: four M5 316 studs threaded into the lower cap, washers and acorn nuts on the upper cap
    for i, (x, y) in enumerate(H["rods"], 1):
        add("rods", f"Tie rod stud M5 x 260, 316 {i}", zcyl(2.1, zc1 - P["rod_engage"], zc1, x, y) + zcyl(P["rod_d"] / 2, zc1, zu1 + 6.0, x, y), 16, "fastener", "stainless", "shell")
        add("rods", f"Washer M5 (ISO 7089) {i}", ring(2.7, 5.0, zu1, zu1 + 1.0, x, y), 16, "fastener", "stainless", "shell")
        nut = g["hexz"](8, zu1 + 1.0, zu1 + 5.0, x, y) + (Pos(x, y, zu1 + 5.0) * Sphere(3.9) & zcyl(4.0, zu1 + 5.0, zu1 + 9.0, x, y))
        nut = nut - zcyl(P["rod_d"] / 2, zu1, zu1 + 6.0, x, y)
        add("rods", f"Acorn nut M5 (DIN 1587) {i}", nut, 16, "fastener", "stainless", "shell")
    # 17 Window retaining ring, PTFE washer, ePTFE window gasket (STEM fix 2026-10-25), face O-rings
    retainer = ring(P["aperture_d"] / 2, P["ret_od"] / 2, zc0, L["z_ret1"])
    for x, y in H["ret"]:
        retainer = retainer - zcyl(1.7, zc0 - 1, L["z_ret1"] + 1, x, y)
    add("retainer", "Window retaining ring, 316, 72 x 51 x 2", retainer, 17, "made", "stainless", "shell")
    add("washer", "Window washer, PTFE 0.5 mm", ring(P["aperture_d"] / 2, P["win_d"] / 2, L["z_ret1"], L["z_win0"]), 17, "made", "hdpe_natural", "internal")
    add("gasket", "Window gasket, expanded PTFE 1 mm", ring(rb, P["win_d"] / 2, L["z_win1"], L["z_bore0"]), 17, "bought", "hdpe_natural", "internal")
    oc = (og0 + og1) / 2
    add("orings", "Face O-ring, EPDM, lower", Pos(0, 0, L["z_tube0"] - 0.65) * Torus(oc, 0.65), 17, "bought", "epdm", "internal")
    add("orings", "Face O-ring, EPDM, upper", Pos(0, 0, L["z_tube1"] + 0.65) * Torus(oc, 0.65), 17, "bought", "epdm", "internal")
    # 16 Screws: retaining ring (M3 countersunk, flush), LED head (M4 socket head in the fin gaps), LED board (M3 low head)
    for i, (x, y) in enumerate(H["ret"], 1):
        add("ret_screws", f"Ring screw M3 x 8 countersunk {i}", zcyl(1.25, zc0, L["z_ret1"] + 6, x, y) + zcyl(1.7, zc0, zc0 + 1.5, x, y), 16, "fastener", "stainless", "shell")
    for i, (x, y) in enumerate(H["head"], 1):
        sc = zcyl(1.65, P["fin_h"], zc0 + 8, x, y) + (zcyl(3.5, P["fin_h"] - 4, P["fin_h"], x, y) - g["hexz"](3.0, P["fin_h"] - 4.1, P["fin_h"] - 2.0, x, y))
        add("head_screws", f"LED head screw M4 x 16 socket head {i}", sc, 16, "fastener", "stainless", "shell")
    for i, (x, y) in enumerate(H["board"], 1):
        add("board_screws", f"LED board screw M3 x 10 low head {i}", zcyl(1.25, P["fin_h"] + 2, L["z_board1"], x, y) + zcyl(2.6, L["z_board1"], L["z_board1"] + 1.5, x, y), 16, "fastener", "stainless", "internal")
    # 9 Dose sensor: ePTFE washer, quartz sensor window, 316 holder, SiC photodiode, amplifier
    add("pd", "Sensor window washer, expanded PTFE 0.5 mm", g["xring"](4.0, 5.0, rt + 1.5, rt + 2.0, z=zd), 9, "bought", "hdpe_natural", "internal")
    add("pd", "Sensor window, fused silica 10 x 3", _chamfer(xcyl(5.0, rt + 2.0, rt + 5.0, z=zd), 0.2), 9, "bought", "glass", "internal")
    holder = xcyl(5.98, rt + 5.0, rt + 10, z=zd) + g["hexx"](12, rt + 10, rt + 18, z=zd)
    holder = holder - xcyl(2.75, rt + 4.9, rt + 18.1, z=zd)
    add("pd", "Photodiode holder, 316, M12 x 1", holder, 9, "made", "stainless", "shell")
    add("pd", "SiC UV-C photodiode, TO-46", xcyl(2.7, rt + 5.5, rt + 10.0, z=zd) + xcyl(0.3, rt + 10.0, rt + 17.9, y=1.0, z=zd)
        + xcyl(0.3, rt + 10.0, rt + 17.9, y=-1.0, z=zd), 9, "bought", "zinc_plated", "internal")
    amp = _chamfer(box(rt + 18, rt + 26, -9, 9, zd - 9, zd + 9), 1.0) - xcyl(2.0, rt + 25, rt + 27, z=zd)
    add("pd", "Transimpedance amplifier in housing", amp, 9, "bought", "matte_black", "shell")
    # 10 LED head cable (flat run through the spreader slot, then round 6-core cable) and its plug
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    zcab = (L["z_sink1"] + L["z_board1"]) / 2
    rcab = P["led_cable_d"] / 2
    lpx, lpy = P["led_plug_xy"]
    pz0 = EZ0 - P["led_plug_h"]
    cab = box(P["board_d"] / 2, rc + 3, -3.5, 3.5, zcab - 0.75, zcab + 0.75)
    cab = cab + rod((rc + 3, 0, zcab), (lpx, lpy, pz0), rcab) + (Pos(rc + 3, 0, zcab) * Sphere(rcab))
    add("led_cable", "LED head cable, 6-core with interlock loop", cab, 10, "bought", "epdm", "shell")
    plug = zcyl(P["led_plug_d"] / 2, pz0, EZ0 - 3, lpx, lpy) + zcyl(6.5, EZ0 - 3, EZ0, lpx, lpy)
    add("led_cable", "LED head plug, 6-pin GX12 class", plug, 10, "bought", "zinc_plated", "shell")
    # 15 Stem adaptors (1/4 BSPP x 3/8 in stem) in both ports and the 316 outlet sleeve
    for zz, nm in ((L["z_in"], "inlet"), (L["z_out"], "outlet")):
        ad = g["hexx"](14, xs + 40, xb, z=zz) + xcyl(6.55, xb, xb + 10, z=zz)
        ad = ad - xcyl(rpb, xs + 39, xb + 11, z=zz)
        add("fittings", f"Stem adaptor 1/4 BSPP x 3/8 in, stainless, {nm}", ad, 15, "bought", "stainless", "shell")
    sleeve = xcyl(rp, xb + 10.1, -rlt - 0.05, z=L["z_out"]) - xcyl(rpb, xb + 10, -rlt + 1, z=L["z_out"])
    add("fittings", "Outlet sleeve, 316, 9.5 x 7 x 17", sleeve, 15, "made", "stainless", "internal")
    # 19 UV-C warning label on the lower cap
    add("label_cap", "UV-C warning label, lower cap", g["sector"](rc, rc + 0.2, zc0 + 8, zc1 - 8, -90.0, 20.0), 19, "bought", "label", "shell")
    out += _periphery(P, P["ring_z"], rt, xs)
    return out


# legacy part names, colours and explode offsets (build_parts keeps the kit 1.7 interface for sizing.py,
# sheets.py, build_plan_media.py and concept_media.py)
_LEGACY = [
    ("tube", "Reactor tube with welded sensor boss, 316", 1, "#A8B0B8", (0, 0, 0)),
    ("liner", "High-reflectance PTFE liner and top disc", 2, "#F3F4F6", (0, -120, 70)),
    ("window", "Quartz window", 3, "#7DD3FC", (0, 0, -115)),
    ("board", "UV-C LED array, 6 x 275 nm", 4, "#7C3AED", (0, 0, -160)),
    ("sink", "Heat sink and spreader ring", 5, "#6B7280", (0, 0, -210)),
    ("cap_lo", "Lower end cap, 316 stainless", 6, "#7B8794", (0, 0, -55)),
    ("cap_hi", "Upper end cap, acetal", 7, "#374151", (0, 0, 55)),
    ("flow", "Hall-effect flow sensor", 8, "#0F766E", (0, 0, -55)),
    ("pd", "UV-C sensor window, photodiode and amplifier", 9, "#D4A017", (75, 0, 0)),
    ("ctrl", "Controller and LED driver", 10, "#15803D", (70, 0, 0)),
    ("valve", "Solenoid shutoff valve", 11, "#C2410C", (0, 0, 55)),
    ("adapter", "24 V power adapter", 12, "#4B5563", (80, 0, -120)),
    ("encl", "Electronics enclosure", 13, "#E5E7EB", (140, 0, 0)),
    ("lid", "Enclosure lid", 13, "#F3F4F6", (140, -60, 0)),
    ("bar", "UV level bar, five segments", 13, "#2DD4BF", (140, -75, 0)),
    ("led_cable", "LED head cable and plug, with interlock loop", 10, "#111827", (40, -40, -120)),
    ("bracket", "Bracket plate", 14, "#9CA3AF", (0, 120, 0)),
    ("saddles", "Sensor and valve saddles", 14, "#A3A3A3", (0, 90, 0)),
    ("clamps", "Pipe clamps", 18, "#52525B", (0, 70, 0)),
    ("fittings", "Fittings, stem adaptors and outlet sleeve", 15, "#60A5FA", (-30, 0, -170)),
    ("rods", "Tie rods, M5 316", 16, "#52525B", (0, 0, 30)),
    ("ret_screws", "Retaining ring screws, M3 countersunk", 16, "#27272A", (0, 0, -90)),
    ("head_screws", "LED head screws, M4", 16, "#27272A", (0, 0, -60)),
    ("board_screws", "LED board screws, M3", 16, "#27272A", (0, 0, -170)),
    ("retainer", "Window retaining ring", 17, "#94A3B8", (0, 0, -90)),
    ("washer", "Window washer, PTFE 0.5 mm", 17, "#E5E7EB", (0, 0, -95)),
    ("gasket", "Window gasket, expanded PTFE", 17, "#E5E7EB", (0, 0, -100)),
    ("orings", "Face O-rings, EPDM", 17, "#1F2937", (0, 0, -20)),
    ("label_cap", "UV-C warning label, lower cap", 19, "#F2C94C", (0, -30, -55)),
    ("label_lid", "UV-C warning label, inside the lid", 19, "#F2C94C", (140, -65, 0)),
    ("label_prod", "Product label", 19, "#F4F4F2", (160, 0, 0)),
    # added in kit 1.9 (2026-10-25): fasteners and parts that were in the BOM but not drawn
    ("weld", "Sensor boss weld bead", 1, "#A8B0B8", (0, 0, 0)),
    ("psensor", "Outlet pressure sensor and tee", 20, "#64748B", (-60, 0, 55)),
    ("socket", "LED head panel socket", 10, "#6B7280", (140, 0, 0)),
    ("encl_screws", "Enclosure screws, M4 pan head", 16, "#27272A", (140, 0, 0)),
    ("lid_screws", "Lid screws, M3 pan head", 16, "#27272A", (140, -60, 0)),
    ("ctrl_screws", "Controller PCB screws, M2.5", 16, "#27272A", (70, 0, 0)),
    ("inserts", "Heat-set inserts, M4 brass", 14, "#B58B3A", (0, 90, 0)),
    ("saddle_screws", "Saddle screws, M4 countersunk", 16, "#27272A", (0, 120, 0)),
    ("wall_screws", "Wall screws", 16, "#27272A", (0, 140, 0)),
]


def build_parts(P=PARAMS):
    """Return [(key, name, shape, bom, color, explode)] for every modelled part of the chosen design (option A),
    each the union of its sub-parts in _a_subparts(). Kept for sizing.py, sheets.py and the media scripts."""
    from build123d import Compound
    groups = {}
    for key, name, shape, *_ in _a_subparts(P):
        groups.setdefault(key, []).append(shape)
    out = []
    for key, name, bom, color, ex in _LEGACY:
        shapes = groups.get(key)
        if not shapes:
            continue
        s = shapes[0]
        for t in shapes[1:]:
            s = s + t
        out.append((key, name, s, bom, color, ex))
    return out


_EXPLODE = {k: ex for k, _, _, _, ex in _LEGACY}


def _parts_from(sub, chosen):
    import cad_parts
    out = []
    for key, name, shape, bom, kind, mat, group in sub:
        out.append(cad_parts.part(name, shape, mat, kind=kind, bom=bom if chosen else None, group=group,
                                  explode=_EXPLODE.get(key, (0, 0, 0))))
    return out


# ------------------------------------------------------------------ option B: hollow-fibre ultrafilter
def _b_subparts(P=PARAMS):
    g = _geo(); box, zcyl, xcyl, ycyl, ring, xring = g["box"], g["zcyl"], g["xcyl"], g["ycyl"], g["ring"], g["xring"]
    Pos, Torus = g["Pos"], g["Torus"]
    by0, by1 = P["bracket_y"]
    cy = P["b_y"]
    hw, hh = P["b_head_w"] / 2, P["b_head_h"]
    rbw, tb = P["b_bowl_od"] / 2, P["b_bowl_t"]
    z0 = P["b_z0"]                                   # bowl bottom
    zb1 = z0 + P["b_bowl_h"]                         # bowl top = head underside
    zh1 = zb1 + hh                                   # head top
    zp = zb1 + hh / 2                                # port centre height
    rco = P["b_cart_od"] / 2
    c0, c1 = z0 + tb + 4, z0 + tb + 4 + P["b_cart_len"]
    out = []
    add = lambda *a: out.append(a)
    # 1 filter head (glass-filled PP): block, threaded spigot for the bowl, two 1/4 BSP side ports, two gauge ports
    head = _chamfer(box(-hw, hw, cy - 45, cy + 45, zb1, zh1), 3.0)
    head = head + ring(rbw - 9, rbw - 4.5, zb1 - 18, zb1 + 0.5, y=cy)
    head = head + xcyl(9, -hw - 12, -hw + 1, y=cy, z=zp) + xcyl(9, hw - 1, hw + 12, y=cy, z=zp)
    head = (head - zcyl(15.7, zb1 - 3, c1 + 14, y=cy) - zcyl(14.5, c1 + 13.9, zp + 6, y=cy)
            - xcyl(6.6, -hw - 13, -hw + 2, y=cy, z=zp) - xcyl(6.6, hw - 2, hw + 13, y=cy, z=zp)
            - xcyl(3.5, -hw + 1, 0, y=cy, z=zp) - xcyl(3.5, 0, hw - 1, y=cy, z=zp + 4))
    for x in (-30, 30):
        head = head - zcyl(4.0, zh1 - 8, zh1 + 1, x=x, y=cy)
    for x in (-40, 40):
        for z in (zb1 + 14, zh1 - 14):
            head = head - ycyl(2.5, cy + 34, cy + 46, x=x, z=z)
    add("head", "Filter head, 2.5 x 10 in slim, glass-filled PP", head, 1, "bought", "hdpe_natural", "shell")
    # 2 bowl (sump), clear, with a threaded neck, grip ribs and a tapped bottom drain boss
    bowl = (zcyl(rbw, z0, zb1 - 18, y=cy) - zcyl(rbw - tb, z0 + tb, zb1, y=cy)) + ring(rbw - 4.5, rbw, zb1 - 18, zb1 - 2, y=cy)
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        rx, ry = (rbw + 1.0) * math.cos(a), cy + (rbw + 1.0) * math.sin(a)
        bowl = bowl + Pos(rx, ry, 0) * box(-2, 2, -2, 2, zb1 - 50, zb1 - 22)
    bowl = bowl + zcyl(8, z0 - 8, z0, y=cy) - zcyl(6.6, z0 - 9, z0 - 1, y=cy) - zcyl(3.5, z0 - 2, z0 + tb + 1, y=cy)
    add("bowl", "Filter bowl, clear, with drain boss", bowl, 2, "bought", "polycarbonate", "shell")
    add("seals", "Bowl O-ring, EPDM", Pos(0, cy, zb1 - 18.8) * Torus(rbw - 6.75, 0.75), 3, "bought", "epdm", "internal")
    # 4 UF cartridge: end caps, potted hollow-fibre bundle, outer net, outlet spigot with two O-rings
    add("cart", "UF cartridge bottom end cap, PP", ring(4, rco, c0, c0 + 10, y=cy) + zcyl(4, z0 + tb, c0 + 3, y=cy), 4, "bought", "hdpe_natural", "internal")
    add("cart", "UF cartridge top end cap, PP", ring(9, rco, c1 - 10, c1, y=cy), 4, "bought", "hdpe_natural", "internal")
    bundle = ring(9, rco - 1.5, c0 + 10, c1 - 10, y=cy)
    for i in range(12):
        z = c0 + 25 + i * 18
        bundle = bundle - ring(rco - 2.5, rco, z, z + 3, y=cy)
    add("cart", "Hollow-fibre bundle, PVDF 0.02 um, potted", bundle, 4, "bought", "insulated_white", "internal")
    add("cart", "Cartridge outer net, PP", ring(rco - 1.5, rco, c0 + 10, c0 + 40, y=cy) + ring(rco - 1.5, rco, c1 - 40, c1 - 10, y=cy), 4, "bought", "hdpe_natural", "internal")
    add("cart", "Cartridge outlet spigot, PP", ring(6.5, 14.4, c1, zb1 + 2, y=cy), 4, "bought", "hdpe_natural", "internal")
    for i, dz in enumerate((5.0, 10.0), 1):
        add("seals", f"Cartridge spigot O-ring {i}, EPDM", ring(14.4, 15.6, c1 + dz, c1 + dz + 1.6, y=cy), 3, "bought", "epdm", "internal")
    # 5 two pressure gauges on the head top (inlet and outlet: the difference shows fouling)
    for i, x in enumerate((-30, 30), 1):
        st = zcyl(4.0, zh1 - 8, zh1 + 12, x=x, y=cy) + g["hexz"](14, zh1, zh1 + 6, x=x, y=cy) - zcyl(1.5, zh1 - 9, zh1 + 13, x=x, y=cy)
        add("gauges", f"Gauge adaptor 1/8 BSP, brass {i}", st, 5, "bought", "brass", "shell")
        dial = ycyl(20, cy - 12, cy + 12, x=x, z=zh1 + 34) - ycyl(17, cy - 13, cy - 10, x=x, z=zh1 + 34) + zcyl(4.0, zh1 + 12, zh1 + 14.0, x=x, y=cy)
        add("gauges", f"Pressure gauge 0 to 10 bar, 40 mm, {'inlet' if x < 0 else 'outlet'}", dial, 5, "bought", "stainless", "shell")
    # 6 forward-flush ball valve on the bowl drain, drain line to the sink trap
    add("valves", "Drain stem 1/4 BSP, stainless", zcyl(6.55, z0 - 8, z0 - 1, y=cy) + g["hexz"](14, z0 - 14, z0 - 8, y=cy) - zcyl(3.5, z0 - 15, z0, y=cy), 6, "bought", "stainless", "shell")
    bv = g["hexz"](16, z0 - 36, z0 - 14, y=cy) + xcyl(3, 0, 26, y=cy, z=z0 - 25) + box(24, 50, cy - 3, cy + 3, z0 - 28, z0 - 22)
    add("valves", "Flush ball valve 1/4 in, brass, lever", bv - zcyl(3.5, z0 - 37, z0 - 13, y=cy), 6, "bought", "brass", "shell")
    add("valves", "Drain tube 3/8 in to the trap", zcyl(4.76, z0 - 90, z0 - 36, y=cy) - zcyl(3.2, z0 - 91, z0 - 35, y=cy), 6, "bought", "hdpe_natural", "shell")
    # 7 port fittings: stem adaptors, inlet tee with the Schrader integrity-test valve, lines
    for lo, hi, th0, th1, nm in ((-hw - 40, -hw - 12, -hw - 12, -hw + 1, "inlet"), (hw + 12, hw + 40, hw - 1, hw + 12, "outlet")):
        ad = g["hexx"](14, lo, hi, y=cy, z=zp) + xcyl(6.55, th0, th1, y=cy, z=zp)
        ad = ad - xcyl(3.5, min(lo, th0) - 1, max(hi, th1) + 1, y=cy, z=zp)
        add("fittings", f"Push-fit stem adaptor 1/4 BSP x 3/8 in, {nm}", ad, 7, "bought", "stainless", "shell")
    tee = xcyl(9, -hw - 80, -hw - 40, y=cy, z=zp) + zcyl(7, zp, zp + 22, x=-hw - 60, y=cy)
    tee = tee - xcyl(3.5, -hw - 81, -hw - 39, y=cy, z=zp) - zcyl(3.0, zp, zp + 23, x=-hw - 60, y=cy)
    add("fittings", "Push-fit tee with test port, inlet", tee, 7, "bought", "hdpe_natural", "shell")
    add("fittings", "Schrader valve, integrity test port", zcyl(3.0, zp + 26, zp + 36, x=-hw - 60, y=cy) + g["hexz"](10, zp + 22, zp + 26, x=-hw - 60, y=cy), 7, "bought", "brass", "shell")
    for x0, x1, nm in ((-hw - 120, -hw - 80, "supply"), (hw + 40, hw + 80, "faucet")):
        add("fittings", f"3/8 in food-grade tube to the {nm}", xring(3.2, 4.76, x0, x1, y=cy, z=zp), 7, "bought", "hdpe_natural", "shell")
    # 8 folded 316 head bracket between the head and the wall plate; 9 screws
    brk = box(-50, 50, cy + 45, cy + 47, zb1 + 4, zh1 - 4)
    for x in (-40, 40):
        for z in (zb1 + 14, zh1 - 14):
            brk = brk - ycyl(2.75, cy + 44, cy + 48, x=x, z=z)
    for sx in (-1, 1):
        brk = brk + box(min(sx * 46, sx * 50), max(sx * 46, sx * 50), cy + 47, by0 - 2, zb1 + 4, zh1 - 4)
        brk = brk + box(min(sx * 46, sx * 62), max(sx * 46, sx * 62), by0 - 2, by0, zb1 + 4, zh1 - 4)
        brk = brk - ycyl(2.75, by0 - 3, by0 + 1, x=sx * 56, z=zp)
    add("bracket", "Head bracket, folded 316 sheet 2 mm", _chamfer(brk, 0.5), 8, "made", "stainless", "shell")
    for i, (x, z) in enumerate([(x, z) for x in (-40, 40) for z in (zb1 + 14, zh1 - 14)], 1):
        add("screws", f"Head screw M5 x 12 pan head {i}", ycyl(4.5, cy + 47, cy + 50.5, x=x, z=z) + ycyl(2.5, cy + 37, cy + 47, x=x, z=z), 9, "fastener", "stainless", "shell")
    for i, x in enumerate((-56, 56), 1):
        add("screws", f"Bracket screw M5 x 10 pan head {i}", ycyl(4.5, by0 - 5.5, by0 - 2, x=x, z=zp) + ycyl(2.5, by0 - 2, by0, x=x, z=zp) + ycyl(2.1, by0, by1, x=x, z=zp), 9, "fastener", "stainless", "shell")
    # 10 wall plate, 6 mm aluminium, tapped M5 for the bracket; wall screws
    px0, px1, pz0, pz1 = -120.0, 120.0, z0 - 10, zh1 + 10
    plate = g["plate_y"](px0, px1, by0, by1, pz0, pz1, r=6.0)
    for x in (-56, 56):
        plate = plate - ycyl(2.1, by0 - 1, by1 + 1, x=x, z=zp)
    wall = [(px0 + 10, pz0 + 10), (px0 + 10, pz1 - 10), (px1 - 10, pz0 + 10), (px1 - 10, pz1 - 10)]
    for x, z in wall:
        plate = plate - ycyl(2.75, by0 - 1, by1 + 1, x=x, z=z)
    add("plate", "Wall plate, 6 mm aluminium", plate, 10, "made", "aluminium", "shell")
    for i, (x, z) in enumerate(wall, 1):
        add("screws", f"Wall screw 5 x 40 pan head {i}", ycyl(5.0, by0 - 3.5, by0, x=x, z=z) + ycyl(2.5, by0, by1 + 30, x=x, z=z), 9, "fastener", "zinc_plated", "shell")
    # 11 labels
    add("labels", "Product label with flush and test instructions", g["plate_y"](-40, 40, cy - 45.2, cy - 45.0, zb1 + 10, zb1 + 40, 2.0), 11, "bought", "label", "shell")
    return out


# ------------------------------------------------------------------ option C: radial UV-C LED reactor
def _c_subparts(P=PARAMS):
    g = _geo(); box, zcyl, xcyl, ycyl, ring, xring = g["box"], g["zcyl"], g["xcyl"], g["ycyl"], g["ring"], g["xring"]
    Pos, Rot, Torus = g["Pos"], g["Rot"], g["Torus"]
    L = levels(P)
    ro, ri = P["c_tube_od"] / 2, P["c_tube_id"] / 2
    rbd, rfl, tfl = P["c_body_r"], P["c_flange_r"], P["c_flange_t"]
    zl0, zl1 = P["c_z_lo"]
    zh0, zh1 = P["c_z_hi"]
    zi, zo = L["z_in"], L["z_out"]
    rc = P["cap_d"] / 2
    xs, xb = -rc - 62, -rc - 10
    out = []
    add = lambda *a: out.append(a)
    sock = 12.0
    rods = [(P["c_rod_r"] * math.cos(math.radians(a)), P["c_rod_r"] * math.sin(math.radians(a))) for a in (45, 135, 225, 315)]
    bars = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in (0, 90, 180, 270)]
    bx = P["c_board_x"]
    # 1 quartz flow tube
    add("qtube", "Fused quartz flow tube, 24 x 2 x 204", _chamfer(ring(ri, ro, zl1 - sock, zh0 + sock), 0.3), 1, "bought", "glass", "internal")
    # 2, 3 end fittings (316): body with tube socket, O-ring groove, port boss tapped 1/4 BSPP, flange with rod holes
    for tag, zb0, zb1, zf0, zf1, zp, socket0, socket1, bore0, bore1 in (
            ("lower", zl0, zl1, zl1 - tfl, zl1, zi, zl1 - sock, zl1, zl0 + 8, zl1 - sock),
            ("upper", zh0, zh1, zh0, zh0 + tfl, zo, zh0, zh0 + sock, zh0 + sock, zh1 - 8)):
        body = zcyl(rbd, zb0, zb1) + zcyl(rfl, zf0, zf1) + xcyl(10, xb, -rbd + 3, z=zp)
        body = body - zcyl(ro + 0.2, socket0 - (0 if tag == "lower" else 0.01), socket1 + (0.01 if tag == "lower" else 0))
        gz = (socket0 + socket1) / 2
        body = body - ring(ro + 0.2, ro + 2.6, gz - 1.2, gz + 1.2)
        body = body - zcyl(ri, bore0 - 0.01, bore1 + 0.01) - xcyl(6.6, xb - 1, xb + 11, z=zp) - xcyl(3.5, xb + 10, 0, z=zp)
        for x, y in rods:
            body = body - zcyl(2.75, zf0 - 1, zf1 + 1, x, y)
        for ux, uy in bars:
            body = body - zcyl(1.7, zf0 - 1, zf1 + 1, ux * (bx + 7.5), uy * (bx + 7.5))
        add("fit", f"End fitting with flange, 316, {tag}", body, 2 if tag == "lower" else 3, "made", "stainless", "shell")
        add("seals", f"Tube O-ring, PTFE-encapsulated, {tag}", Pos(0, 0, gz) * Torus(ro + 1.4, 1.15), 4, "bought", "hdpe_natural", "internal")
    # 5, 6 four LED strips (aluminium-core PCB, three LEDs each) on finned aluminium bars between the flanges
    zs0, zs1 = zl1, zh0
    zm = (zs0 + zs1) / 2
    for k, (ux, uy) in enumerate(bars, 1):
        rot = Rot(0, 0, 90 * (k - 1))
        barsh = box(bx + 1.6, bx + 11.6, -6, 6, zs0, zs1)
        for f in (-4.5, 0.0, 4.5):
            barsh = barsh + box(bx + 11.6, bx + 21.6, f - 1.0, f + 1.0, zs0 + 5, zs1 - 5)
        barsh = barsh - zcyl(1.25, zs0 - 1, zs0 + 8, bx + 7.5, 0) - zcyl(1.25, zs1 - 8, zs1 + 1, bx + 7.5, 0)
        barsh = barsh - box(bx + 1.5, bx + 3.0, -2, 2, zs0 + 30, zs1 - 30)
        pcb = box(bx, bx + 1.6, -6, 6, zs0 + 10, zs1 - 10)
        for zz in (zs0 + 18, zs1 - 18):
            pcb = pcb - xcyl(1.6, bx - 1, bx + 2.6, z=zz)
            barsh = barsh - xcyl(1.25, bx + 1.5, bx + 9.6, z=zz)
            add("screws", f"Strip screw M2.5 x 8, strip {k} at {zz:.0f}", rot * (xcyl(2.5, bx - 1.5, bx, z=zz) + xcyl(1.25, bx, bx + 9.6, z=zz)), 8, "fastener", "stainless", "internal")
        add("bars", f"Heat-sink bar, aluminium, strip {k}", rot * barsh, 5, "made", "aluminium", "shell")
        add("strips", f"LED strip PCB, aluminium core, {k}", rot * pcb, 6, "bought", "aluminium", "internal")
        for j in range(P["c_led_n"]):
            z = zs0 + 45 + j * (zs1 - zs0 - 90) / (P["c_led_n"] - 1)
            led = box(bx - 0.8, bx, -1.75, 1.75, z - 1.75, z + 1.75) + box(bx - 1.2, bx - 0.8, -1.25, 1.25, z - 1.25, z + 1.25)
            add("strips", f"UV-C LED 275 nm, strip {k} LED {j + 1}", rot * led, 6, "bought", "matte_black", "internal")
    # 7 corner reflectors (polished aluminium strips) between the strips
    for k in range(4):
        a = 45 + 90 * k
        refl = Rot(0, 0, a) * _chamfer(box(17.5, 18.0, -8.0, 8.0, zs0 + 2, zs1 - 2) - xcyl(2.0, 17, 18.5, z=zm) if k == 0 else box(17.5, 18.0, -8.0, 8.0, zs0 + 2, zs1 - 2), 0.15)
        add("refl", f"Corner reflector, polished aluminium {k + 1}", refl, 7, "bought", "mirror", "internal")
    # 8 four M5 tie rods with nuts and washers clamping the two flanges
    for i, (x, y) in enumerate(rods, 1):
        add("rods", f"Tie rod M5, 316 {i}", zcyl(2.5, zl1 - tfl - 10, zh0 + tfl + 10, x, y), 8, "fastener", "stainless", "shell")
        for zz, d in ((zl1 - tfl, -1), (zh0 + tfl, 1)):
            w0, w1 = (zz, zz + d * 1.0)
            add("rods", f"Washer M5 {i} {'low' if d < 0 else 'high'}", ring(2.7, 5.0, min(w0, w1), max(w0, w1), x, y), 8, "fastener", "stainless", "shell")
            n0 = zz + d * 1.0
            n1 = n0 + d * 4.7
            add("rods", f"Hex nut M5 {i} {'low' if d < 0 else 'high'}", g["hexz"](8, min(n0, n1), max(n0, n1), x, y) - zcyl(2.5, min(n0, n1) - 1, max(n0, n1) + 1, x, y), 8, "fastener", "stainless", "shell")
    # 8 M3 screws, flange to bar ends (two per bar)
    for k, (ux, uy) in enumerate(bars, 1):
        x, y = ux * (bx + 7.5), uy * (bx + 7.5)
        add("screws", f"Bar screw M3 x 12, strip {k} low", zcyl(2.75, zl1 - tfl - 2.0, zl1 - tfl, x, y) + zcyl(1.25, zl1 - tfl, zs0 + 6, x, y), 8, "fastener", "stainless", "shell")
        add("screws", f"Bar screw M3 x 12, strip {k} high", zcyl(2.75, zh0 + tfl, zh0 + tfl + 2.0, x, y) + zcyl(1.25, zs1 - 6, zh0 + tfl, x, y), 8, "fastener", "stainless", "shell")
    # 9 dose photodiode looking across the tube between two strips (in the reflector gap), with holder
    a = math.radians(45)
    pdx = lambda r: (r * math.cos(a), r * math.sin(a))
    from build123d import Plane, Solid, Vector
    def radial(r0, r1, rad):
        p0, p1 = Vector(*pdx(r0), zm), Vector(*pdx(r1), zm)
        return Solid.make_cylinder(rad, (p1 - p0).length, Plane(origin=p0, z_dir=(p1 - p0).normalized()))
    add("pd", "SiC UV-C photodiode in holder", radial(18.5, 19.5, 1.8) + radial(19.5, 25.5, 2.7), 9, "bought", "zinc_plated", "internal")
    # periphery shared with option A (plate, enclosure, controller, flow sensor, valve, clamps on the fitting bodies)
    out += _periphery(P, (zl0 + 10.0, zh1 - 15.0), rbd, xs, plate_z=(5.0, 330.0))
    # 10 stem adaptors into the end fittings
    for zz, nm in ((zi, "inlet"), (zo, "outlet")):
        ad = g["hexx"](14, xs + 40, xb, z=zz) + xcyl(6.55, xb, xb + 10, z=zz)
        ad = ad - xcyl(3.5, xs + 39, xb + 11, z=zz)
        add("fittings", f"Stem adaptor 1/4 BSPP x 3/8 in, stainless, {nm}", ad, 15, "bought", "stainless", "shell")
    # LED cable from strip 1 to the panel socket
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    lpx, lpy = P["led_plug_xy"]
    pz0 = EZ0 - P["led_plug_h"]
    cab = g["rod"]((bx + 22.5, 0.0, zs0 + 20), (lpx, lpy, pz0 - 10), 2.25) + g["Pos"](lpx, lpy, pz0 - 10) * g["Sphere"](2.25) + zcyl(2.25, pz0 - 10, pz0, lpx, lpy)
    add("led_cable", "LED strip cable, 6-core with interlock loop", cab, 10, "bought", "epdm", "shell")
    add("led_cable", "LED plug, 6-pin GX12 class", zcyl(7.5, pz0, EZ0 - 3, lpx, lpy) + zcyl(6.5, EZ0 - 3, EZ0, lpx, lpy), 10, "bought", "zinc_plated", "shell")
    add("labels", "UV-C warning label, reactor", g["plate_x"](bx + 21.6, bx + 21.8, -10, 10, zm + 30, zm + 60, 2.0), 19, "bought", "label", "shell")
    return out


def components(option=CHOSEN, P=PARAMS):
    """Kit 1.9: every part of a concept option as cad_parts.part() dicts (made, bought, fastener, weld).
    BOM line numbers are given for the chosen option only; B and C number their own lines for the parts list in
    LMF-OPT-001."""
    import sys as _s
    kit = str(Path(__file__).resolve().parents[2] / ".kit")
    if kit not in _s.path:
        _s.path.insert(0, kit)
    if option == "A":
        return _parts_from(_a_subparts(P), True)
    if option == "B":
        return _parts_from(_b_subparts(P), False)
    if option == "C":
        return _parts_from(_c_subparts(P), False)
    raise KeyError(option)


def build(P=PARAMS, include_adapter=True):
    """Whole assembly as one Compound."""
    from build123d import Compound
    # without the adapter: the unit as installed, also without the wall screws, which run into the cabinet wall
    return Compound(children=[s for k, _, s, *_ in build_parts(P) if include_adapter or k not in ("adapter", "wall_screws")])


# ------------------------------------------------------------------ constructability checks
CONTACTS = [  # pairs that must touch (gap 0): the faces that carry each joint
    ("tube", "cap_lo", "tube end in the lower cap seat"), ("tube", "cap_hi", "tube end in the upper cap seat"),
    ("tube", "liner", "liner inside the tube"), ("liner", "cap_lo", "liner on the lower cap spigot"),
    ("window", "washer", "window on the PTFE washer"), ("washer", "retainer", "washer on the retaining ring"),
    ("window", "gasket", "window under the gasket"),
    ("gasket", "cap_lo", "gasket on the cap shoulder"), ("orings", "cap_lo", "lower O-ring in its groove"),
    ("orings", "cap_hi", "upper O-ring in its groove"), ("orings", "tube", "O-rings on the tube ends"),
    ("retainer", "cap_lo", "retaining ring in its recess"), ("retainer", "sink", "spreader ring under the retaining ring"),
    ("board", "sink", "LED board on the sink base"), ("sink", "cap_lo", "spreader ring on the cap"),
    ("rods", "cap_lo", "studs in the lower cap"), ("rods", "cap_hi", "nuts on the upper cap"),
    ("ret_screws", "retainer", "ring screws in the ring"), ("ret_screws", "cap_lo", "ring screws in the cap"),
    ("head_screws", "sink", "head screws under the sink base"), ("head_screws", "cap_lo", "head screws in the cap"),
    ("board_screws", "board", "board screws on the board"), ("board_screws", "sink", "board screws in the sink base"),
    ("fittings", "cap_lo", "inlet adaptor in its thread"), ("fittings", "cap_hi", "outlet adaptor and sleeve"),
    ("fittings", "flow", "stem into the flow sensor"), ("fittings", "valve", "stem into the valve"),
    ("pd", "tube", "sensor window and holder in the boss"),
    ("encl", "bracket", "enclosure back on the plate"), ("lid", "encl", "lid on the enclosure"),
    ("clamps", "tube", "clamp rubber on the tube"), ("clamps", "bracket", "clamp studs on the plate"),
    ("saddles", "bracket", "saddles on the plate"), ("saddles", "flow", "flow sensor on its saddle"),
    ("saddles", "valve", "valve on its saddle"),
    ("bar", "lid", "UV level bar segments in the lid"), ("led_cable", "board", "LED cable on the LED board"),
    ("led_cable", "encl", "LED plug on the enclosure socket"), ("label_cap", "cap_lo", "UV-C label on the lower cap"),
    ("label_lid", "lid", "UV-C label inside the lid"), ("label_prod", "encl", "product label on the enclosure"),
]
CLEAR = [  # pairs that must stay apart by at least this gap (mm)
    ("board", "window", 0.5, "LEDs below the window"), ("board_screws", "window", 0.2, "board screw heads below the window"),
    ("pd", "encl", 2.0, "sensor clear of the enclosure"), ("pd", "clamps", 5.0, "sensor clear of the clamps"),
    ("valve", "cap_hi", 5.0, "valve clear of the upper cap"), ("flow", "cap_lo", 5.0, "sensor clear of the lower cap"),
    ("sink", "bracket", 2.0, "heat sink clear of the plate"), ("encl", "clamps", 5.0, "enclosure clear of the clamps"),
    ("cap_hi", "bracket", 2.0, "upper cap clear of the plate"), ("cap_lo", "bracket", 2.0, "lower cap clear of the plate"),
    ("rods", "liner", 3.0, "studs clear of the liner"), ("rods", "clamps", 1.9, "studs clear of the clamps"),
    ("board", "washer", 0.5, "LEDs clear of the window washer"),
    ("led_cable", "cap_lo", 0.5, "LED cable clear of the lower cap"), ("led_cable", "sink", 0.5, "LED cable in the ring slot"),
    ("led_cable", "retainer", 0.5, "LED cable clear of the retaining ring"),
    ("led_cable", "clamps", 5.0, "LED cable clear of the clamps"), ("led_cable", "pd", 5.0, "LED cable clear of the sensor"),
    ("label_cap", "rods", 2.0, "cap label clear of the studs"), ("label_lid", "ctrl", 2.0, "lid label clear of the modules"),
]


def led_cable_route(P=PARAMS):
    """Cable path from the LED board edge to the plug (mm): flat run in the slot, then straight to the plug."""
    L = levels(P)
    rc = P["cap_d"] / 2
    zcab = (L["z_sink1"] + L["z_board1"]) / 2
    lpx, lpy = P["led_plug_xy"]
    pts = [(P["board_d"] / 2, 0.0, zcab), (rc + 3, 0.0, zcab), (lpx, lpy, P["encl"][4] - P["led_plug_h"])]
    length = sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))
    # the head is clear of the cap once it has dropped 3 mm and slid forward (-Y) by the sink width plus the
    # cap radius; the straight distance from the cable's board end to the plug is then the least cable it needs
    a = pts[0]
    clear = math.dist((a[0], a[1] - (P["sink_w"] / 2 + rc), a[2] - 3.0), pts[-1])
    # resting on the cabinet floor while still plugged in
    floor = math.dist((a[0], a[1], a[2] - P["floor_gap"]), pts[-1])
    return {"points": pts, "route": length, "clear": clear, "floor": floor}


def checks(P=PARAMS):
    """Returns [(description, overlap mm3, gap mm, expectation, ok)]: no two parts overlap; listed joints
    touch; listed parts keep their clearance; the window and the LED head can come out downward."""
    parts = {k: s for k, _, s, *_ in build_parts(P)}
    keys = [k for k in parts if k != "adapter"]
    res = []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            v = (parts[a] & parts[b]).volume
            res.append((f"{a} / {b}: no overlap", v, None, "overlap < 0.5 mm3", v < 0.5))
    for a, b, why in CONTACTS:
        d = parts[a].distance_to(parts[b])
        res.append((f"{a} / {b}: {why}", None, d, "touch", d < 0.05))
    for a, b, g, why in CLEAR:
        d = parts[a].distance_to(parts[b])
        res.append((f"{a} / {b}: {why}", None, d, f"gap >= {g}", d >= g))
    # removal paths: the window drops out of the cap once the retaining ring is off (nothing above it narrower
    # than the pocket below it), and the LED head drops away once its four screws are out
    from build123d import Pos
    L = levels(P)
    w = parts["window"]
    path = Pos(0, 0, -(L["z_win0"] - L["z_board1"] + 0.5)) * w
    ok = (path & parts["cap_lo"]).volume < 0.5
    res.append(("window drops out of the cap from below", None, None, "clear path", ok))
    head = parts["sink"] + parts["board"]
    ok = all((Pos(0, 0, -dz) * head & parts["cap_lo"]).volume < 0.5 for dz in (0.5, 2, 5))
    res.append(("LED head drops away from the cap", None, None, "clear path", ok))
    # LED head interlock (2026-10-02): the cable reaches the plug as routed, with a little slack, but is at
    # least 10 mm too short for the head to come clear of the cap while the plug is still in
    R = led_cable_route(P)
    cl = P["led_cable_len"]
    res.append((f"LED cable {cl:.0f} mm covers its {R['route']:.1f} mm route with up to 10 mm slack", None, cl - R["route"],
                "0 to 10 mm slack", 0 <= cl - R["route"] <= 10))
    res.append((f"LED head cannot clear the cap while plugged in ({R['clear']:.0f} mm needed)", None, R["clear"] - cl,
                "short by 10 mm or more", R["clear"] - cl >= 10))
    return res


def print_checks(P=PARAMS):
    res = checks(P)
    bad = [r for r in res if not r[4]]
    for d, v, g, e, ok in res:
        if not ok or "no overlap" not in d:
            val = f"gap {g:.2f} mm" if g is not None else (f"overlap {v:.2f} mm3" if v is not None else "")
            print(f"  {'ok  ' if ok else 'FAIL'} {d}: {val} ({e})")
    print(f"{len(res)} constructability checks, {len(res) - len(bad)} pass, {len(bad)} fail")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = {k: s for k, _, s, *_ in build_parts()}
    groups = {"reactor": ["tube", "liner", "window", "cap_lo", "cap_hi", "rods", "retainer", "washer", "gasket", "orings",
                          "ret_screws", "label_cap"],
              "led-head": ["board", "sink", "board_screws", "head_screws", "led_cable"]}
    for name, keys in groups.items():  # export groups before the parts are adopted by the assembly compound
        shape = Compound(children=[parts[k] for k in keys])
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.15, angular_tolerance=0.3)
    asm = build()
    export_step(asm, str(out / "step" / "lumaflow-assembly.step"))
    export_stl(asm, str(out / "stl" / "lumaflow-assembly.stl"), tolerance=0.15, angular_tolerance=0.3)
    L = levels()
    bb = build(include_adapter=False).bounding_box()
    print(f"unit without adapter {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm; "
          f"channel {PARAMS['bore_d']:.0f} mm x {L['channel_len']:.0f} mm, inlet to outlet {L['flow_len']:.0f} mm, "
          f"wall sensor at Z {L['z_det']:.0f} mm")
    for k, n, s, *_ in build_parts():
        if not s.is_valid:
            print(f"warning: {n} is not a valid solid")
    print("exported STEP and STL to cad/step and cad/stl")
    print_checks()
