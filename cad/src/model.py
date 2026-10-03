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


def build_parts(P=PARAMS):
    """Return [(key, name, shape, bom, color, explode)] for every modeled part."""
    from build123d import Box, Cylinder, Plane, Polygon, Pos, Rot, Solid, Sphere, Torus, Vector, extrude

    def box(x0, x1, y0, y1, z0, z1):
        return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)

    def zcyl(r, z0, z1, x=0.0, y=0.0):
        return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)

    def xcyl(r, x0, x1, y=0.0, z=0.0):
        return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)

    def ycyl(r, y0, y1, x=0.0, z=0.0):
        return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)

    def ring(r0, r1, z0, z1):
        return zcyl(r1, z0, z1) - zcyl(r0, z0 - 1, z1 + 1)

    def rod(p0, p1, r):
        p0, p1 = Vector(*p0), Vector(*p1)
        return Solid.make_cylinder(r, (p1 - p0).length, Plane(origin=p0, z_dir=(p1 - p0).normalized()))

    def sector(r0, r1, z0, z1, ang_c, half):
        """Thin cylindrical shell sector (a wrapped label) centred on azimuth ang_c (deg from +X)."""
        Rr = r1 * 1.5
        pts = [(0.0, 0.0)] + [(Rr * math.cos(math.radians(ang_c - half + 2 * half * i / 12)),
                               Rr * math.sin(math.radians(ang_c - half + 2 * half * i / 12))) for i in range(13)]
        wedge = Pos(0, 0, z0) * extrude(Polygon(*pts, align=None), amount=z1 - z0)
        return ring(r0, r1, z0, z1) & wedge

    L = levels(P)
    H = positions(P)
    rb, rl, rt, rc = P["bore_d"] / 2, P["liner_od"] / 2, P["tube_od"] / 2, P["cap_d"] / 2
    rlt = P["liner_top_od"] / 2
    rp, rpb = P["port_od"] / 2, P["port_bore"] / 2
    rd, zd = P["det_win_d"] / 2, L["z_det"]
    rbo = P["boss_d"] / 2
    r_thr = 6.6                                                    # 1/4 BSPP tapped hole (13.2 mm major diameter)
    r_seat = rt + 0.25                                             # tube seat in the caps
    og0, og1, og_d = 30.0, 32.4, 1.3                               # face O-ring groove under the tube end
    xs = -rc - 62                                                  # outer end of the flow sensor and valve bodies
    xb = -rc - 10                                                  # outer face of the port bosses
    parts = []

    # 1 Reactor tube, 316 stainless, with the sensor boss welded on at mid height (bore 8 mm, window seat, M12 x 1)
    tube = zcyl(rt, L["z_tube0"], L["z_tube1"]) - zcyl(rl, L["z_tube0"] - 1, L["z_tube1"] + 1)
    boss = xcyl(11, rt - 4, rt + 10, z=zd) - zcyl(rl, zd - 12, zd + 12)
    tube = (tube + boss) - xcyl(rd, rl - 1, rt + 1.5, z=zd) - xcyl(5.1, rt + 1.5, rt + 5, z=zd) - xcyl(6.0, rt + 5, rt + 11, z=zd)
    # 2 High-reflectance PTFE liner: tube length, a turned-down extension into the upper cap, a solid top disc,
    #   the outlet hole and the sensor hole in the wall
    liner = (zcyl(rl, L["z_cap0"], L["z_tube1"]) + zcyl(rlt, L["z_tube1"], L["z_disc1"])
             - zcyl(rb, L["z_cap0"] - 1, L["z_disc0"]))
    liner = liner - xcyl(rpb, -rl - 1, -rb + 0.5, z=L["z_out"]) - xcyl(rd, rb - 1, rl + 1, z=zd)
    # 3 Quartz window, dropped in from below
    window = zcyl(P["win_d"] / 2, L["z_win0"], L["z_win1"])
    # 4 UV-C LED array on a round aluminum-core board, three M3 screws into the sink base
    board = zcyl(P["board_d"] / 2, L["z_sink1"], L["z_board1"])
    s = P["led_size"] / 2
    for i in range(P["led_n"]):
        a = 2 * math.pi * i / P["led_n"]
        x, y = P["led_pcr"] * math.cos(a), P["led_pcr"] * math.sin(a)
        board = board + box(x - s, x + s, y - s, y + s, L["z_board1"], L["z_led1"])
    for x, y in H["board"]:
        board = board - zcyl(1.7, L["z_sink1"] - 1, L["z_board1"] + 1, x, y)
    # 5 Heat sink (fins down) and aluminum spreader ring from the sink base to the stainless lower cap,
    #   with a cable slot toward the enclosure and the four head screw holes
    hw = P["sink_w"] / 2
    sink = box(-hw, hw, -hw, hw, P["fin_h"], L["z_sink1"])
    pitch = (P["sink_w"] - P["fin_t"]) / (P["n_fins"] - 1)
    for i in range(P["n_fins"]):
        x = -hw + i * pitch
        sink = sink + box(x, x + P["fin_t"], -hw, hw, 0, P["fin_h"])
    spreader = ring(P["board_d"] / 2 + 0.5, rc, L["z_sink1"], L["z_board1"]) - box(P["board_d"] / 2, rc + 1, -4, 4, L["z_sink1"] - 1, L["z_board1"] + 1)
    sink = sink + spreader
    for x, y in H["head"]:
        sink = sink - zcyl(2.25, P["fin_h"] - 1, L["z_board1"] + 1, x, y)
    for x, y in H["board"]:
        sink = sink - zcyl(1.25, P["fin_h"] + 1, L["z_sink1"] + 0.1, x, y)
    # 6 Lower end cap, 316 stainless: retaining ring recess, window pocket open from below, shoulder, bore,
    #   tube seat with face O-ring groove, inlet boss tapped 1/4 BSPP, stud and screw holes
    zc0, zc1 = L["z_board1"], L["z_cap0"]
    cap_lo = zcyl(rc, zc0, zc1) + xcyl(rbo, xb, -rc + 4, z=L["z_in"])
    cap_lo = (cap_lo
              - zcyl(P["ret_od"] / 2 + 0.2, zc0 - 1, L["z_ret1"])
              - zcyl(P["win_d"] / 2 + 0.5, L["z_ret1"] - 0.1, L["z_bore0"])
              - zcyl(rb, L["z_bore0"] - 0.1, zc1 + 1)
              - ring(rl, r_seat, L["z_tube0"], zc1 + 1)
              - ring(og0, og1, L["z_tube0"] - og_d, L["z_tube0"] + 0.1)
              - xcyl(r_thr, xb - 1, xb + 11, z=L["z_in"])
              - xcyl(rpb, xb + 10, -rb + 0.5, z=L["z_in"]))
    for x, y in H["rods"]:
        cap_lo = cap_lo - zcyl(2.1, zc1 - P["rod_engage"], zc1 + 1, x, y)
    for x, y in H["ret"]:
        cap_lo = cap_lo - zcyl(1.25, L["z_ret1"] - 0.1, L["z_ret1"] + 8, x, y)
    for x, y in H["head"]:
        cap_lo = cap_lo - zcyl(1.65, zc0 - 1, zc0 + 10, x, y)
    # 7 Upper end cap, acetal: tube seat with face O-ring groove, liner pocket, 13 mm roof,
    #   outlet boss tapped 1/4 BSPP with the 316 sleeve bore, stud clearance holes
    zu0, zu1 = L["z_cap1"], L["z_top"]
    cap_hi = zcyl(rc, zu0, zu1) + xcyl(rbo, xb, -rc + 4, z=L["z_out"])
    cap_hi = (cap_hi
              - zcyl(r_seat, zu0 - 1, L["z_tube1"])
              - ring(og0, og1, L["z_tube1"] - 0.1, L["z_tube1"] + og_d)
              - zcyl(rlt + 0.1, L["z_tube1"] - 0.1, L["z_disc1"])
              - xcyl(r_thr, xb - 1, xb + 11, z=L["z_out"])
              - xcyl(rp + 0.05, xb + 10, -rlt, z=L["z_out"]))
    for x, y in H["rods"]:
        cap_hi = cap_hi - zcyl(2.7, zu0 - 1, zu1 + 1, x, y)
    # 16 Tie rods: four M5 316 studs threaded into the lower cap, washers and acorn nuts on the upper cap
    rods = None
    for x, y in H["rods"]:
        r = (zcyl(2.1, zc1 - P["rod_engage"], zc1, x, y) + zcyl(P["rod_d"] / 2, zc1, zu1 + 6.0, x, y)
             + zcyl(5.0, zu1, zu1 + 1.0, x, y) + zcyl(4.0, zu1 + 1.0, zu1 + 7.0, x, y))
        rods = r if rods is None else rods + r
    # 17 Window retaining ring (316, six M3 countersunk screws), PTFE window washer, window gasket and the
    #    two face O-rings
    retainer = ring(P["aperture_d"] / 2, P["ret_od"] / 2, zc0, L["z_ret1"])
    for x, y in H["ret"]:
        retainer = retainer - zcyl(1.7, zc0 - 1, L["z_ret1"] + 1, x, y)
    washer = ring(P["aperture_d"] / 2, P["win_d"] / 2, L["z_ret1"], L["z_win0"])
    gasket = ring(rb, P["win_d"] / 2, L["z_win1"], L["z_bore0"])
    oc = (og0 + og1) / 2
    orings = (Pos(0, 0, L["z_tube0"] - 0.65) * Torus(oc, 0.65)) + (Pos(0, 0, L["z_tube1"] + 0.65) * Torus(oc, 0.65))
    # 16 Screws: retaining ring (M3 countersunk, flush), LED head (M4 socket heads in the fin gaps),
    #   LED board (M3 low heads)
    ret_screws = head_screws = board_screws = None
    for x, y in H["ret"]:
        sc = zcyl(1.25, zc0, L["z_ret1"] + 6, x, y) + zcyl(1.7, zc0, zc0 + 1.5, x, y)
        ret_screws = sc if ret_screws is None else ret_screws + sc
    for x, y in H["head"]:
        sc = zcyl(1.65, P["fin_h"], zc0 + 8, x, y) + zcyl(3.5, P["fin_h"] - 4, P["fin_h"], x, y)
        head_screws = sc if head_screws is None else head_screws + sc
    for x, y in H["board"]:
        sc = zcyl(1.25, P["fin_h"] + 2, L["z_board1"], x, y) + zcyl(2.6, L["z_board1"], L["z_board1"] + 1.5, x, y)
        board_screws = sc if board_screws is None else board_screws + sc
    # 8 Hall-effect flow sensor on the inlet line; 11 normally closed valve on the outlet line
    flow = box(xs, xs + 40, -14, 14, L["z_in"] - 14, L["z_in"] + 14) + zcyl(8, L["z_in"] + 14, L["z_in"] + 24, x=xs + 20)
    valve = (box(xs, xs + 40, -14, 14, L["z_out"] - 14, L["z_out"] + 14)
             + zcyl(14, L["z_out"] + 14, L["z_out"] + 44, x=xs + 20))
    # 9 Dose sensor: quartz sensor window (10 x 3 mm on the 8 mm bore), photodiode holder screwed into the
    #   boss, TO-46 photodiode and amplifier box, facing +X toward the enclosure
    pd = (xcyl(5.0, rt + 2.0, rt + 5.0, z=zd)
          + xcyl(5.98, rt + 5.0, rt + 10, z=zd) + xcyl(7.0, rt + 10, rt + 18, z=zd)
          + box(rt + 18, rt + 26, -9, 9, zd - 9, zd + 9))
    # 13 Electronics enclosure: printed body with its back on the bracket plate, front lid with the
    #    five-segment UV level bar (R18), cable gland, and the LED head socket in the floor
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    ym = (EY0 + EY1) / 2
    encl = box(EX0, EX1, EY0 + 2.5, EY1, EZ0, EZ1) - box(EX0 + 2.5, EX1 - 2.5, EY0 + 2.4, EY1 - 2.5, EZ0 + 2.5, EZ1 - 2.5)
    encl = encl + xcyl(4, EX0 - 12, EX0, y=ym, z=EZ0 + 20)
    for x, z in H["encl"]:
        encl = encl - ycyl(2.2, EY1 - 3, EY1 + 1, x=x, z=z)
    lpx, lpy = P["led_plug_xy"]
    encl = encl - zcyl(6.0, EZ0 - 1, EZ0 + 3, lpx, lpy)              # 12 mm hole for the LED head socket
    lid = box(EX0, EX1, EY0, EY0 + 2.5, EZ0, EZ1)
    bar = None
    for x0, x1, z0, z1 in H["bar"]:
        lid = lid - box(x0, x1, EY0 - 1, EY0 + 3.5, z0, z1)
        seg = box(x0, x1, EY0 - 1.0, EY0 + 2.5, z0, z1)
        bar = seg if bar is None else bar + seg
    # 19 Labels: UV-C warning label on the lower cap front and inside the lid; product label on the enclosure side
    lab_cap = sector(rc, rc + 0.2, zc0 + 8, zc1 - 8, -90.0, 20.0)
    lab_lid = box(EX0 + 12, EX1 - 12, EY0 + 2.5, EY0 + 2.7, EZ0 + 55, EZ0 + 85)
    lab_prod = box(EX1, EX1 + 0.2, EY0 + 10, EY1 - 6, EZ0 + 40, EZ0 + 90)
    # 10 LED head cable: flat run through the spreader ring slot, then a round 6-core cable to the plug
    zcab = (L["z_sink1"] + L["z_board1"]) / 2
    rcab = P["led_cable_d"] / 2
    pz0 = EZ0 - P["led_plug_h"]
    cab = box(P["board_d"] / 2, rc + 3, -3.5, 3.5, zcab - 0.75, zcab + 0.75)
    cab = cab + rod((rc + 3, 0, zcab), (lpx, lpy, pz0), rcab) + (Pos(rc + 3, 0, zcab) * Sphere(rcab))
    cab = cab + zcyl(P["led_plug_d"] / 2, pz0, EZ0, lpx, lpy)
    # 10 Controller and LED driver modules inside the enclosure
    ctrl = (box(EX0 + 6, EX1 - 6, EY1 - 7.5, EY1 - 5.5, EZ0 + 8, EZ1 - 8) + box(EX0 + 12, EX0 + 30, ym - 4, ym + 4, EZ0 + 30, EZ0 + 48)
            + box(EX0 + 30, EX1 - 12, ym - 2, ym + 4, EZ0 + 70, EZ0 + 90))
    # 12 24 V DC adapter on the cabinet floor
    fz = -P["floor_gap"]
    adapter = box(150, 245, -30, 20, fz, fz + 34)
    # 14 Wall bracket: 6 mm aluminium plate (tapped for the clamps and the enclosure, wall holes) and two printed
    #    saddles that carry the flow sensor and the valve
    by0, by1 = P["bracket_y"]
    px0, px1 = P["plate_x"]; pz0, pz1 = P["plate_z"]
    plate = box(px0, px1, by0, by1, pz0, pz1)
    for x, z in H["wall"]:
        plate = plate - ycyl(2.75, by0 - 1, by1 + 1, x=x, z=z)
    for x, z in H["clamps"]:
        plate = plate - ycyl(3.4, by0 - 1, by1 + 1, x=x, z=z)
    for x, z in H["encl"]:
        plate = plate - ycyl(1.65, by0 - 1, by1 + 1, x=x, z=z)
    sx0, sx1 = xs + 10, xs + 30
    saddles = None
    for zz in (L["z_in"], L["z_out"]):
        sd = box(sx0, sx1, 14, by0, zz - 14, zz + 14) - box(sx0 + 6, sx1 - 6, 20, 24, zz - 15, zz + 15)
        saddles = sd if saddles is None else saddles + sd
        for dz in (-7, 7):
            plate = plate - ycyl(2.25, by0 - 1, by1 + 1, x=(sx0 + sx1) / 2, z=zz + dz)
    # 18 Pipe clamps: rubber-lined 65 mm clamps with an M8 boss, on M8 studs into the plate
    clamps = None
    rr = P["ring_od"] / 2
    for x, z in H["clamps"]:
        c = (ring(rt, rr, z - P["ring_h"] / 2, z + P["ring_h"] / 2) + box(-9, 9, rr - 1, rr + 6, z - 8, z + 8)
             + ycyl(4.0, rr + 6, by0, x=x, z=z))
        clamps = c if clamps is None else clamps + c
    # 15 Fittings: supply line into the flow sensor; stainless stem adaptors (1/4 BSPP x 3/8 in stem) in both
    #    ports; 316 outlet sleeve in the acetal cap; line from the valve to the faucet
    fittings = (xcyl(rp, xs - 40, xs, z=L["z_in"]) + xcyl(rp, xs - 40, xs, z=L["z_out"]))
    for zz in (L["z_in"], L["z_out"]):
        fittings = fittings + xcyl(7.5, xs + 40, xb, z=zz) + (xcyl(6.55, xb, xb + 10, z=zz) - xcyl(rpb, xb - 1, xb + 11, z=zz))
    fittings = fittings + (xcyl(rp, xb + 10.1, -rlt - 0.05, z=L["z_out"]) - xcyl(rpb, xb + 10, -rlt + 1, z=L["z_out"]))

    parts += [
        ("tube", "Reactor tube with welded sensor boss, 316", tube, 1, "#A8B0B8", (0, 0, 0)),
        ("liner", "High-reflectance PTFE liner and top disc", liner, 2, "#F3F4F6", (0, -120, 70)),
        ("window", "Quartz window", window, 3, "#7DD3FC", (0, 0, -115)),
        ("board", "UV-C LED array, 6 x 275 nm", board, 4, "#7C3AED", (0, 0, -160)),
        ("sink", "Heat sink and spreader ring", sink, 5, "#6B7280", (0, 0, -210)),
        ("cap_lo", "Lower end cap, 316 stainless", cap_lo, 6, "#7B8794", (0, 0, -55)),
        ("cap_hi", "Upper end cap, acetal", cap_hi, 7, "#374151", (0, 0, 55)),
        ("flow", "Hall-effect flow sensor", flow, 8, "#0F766E", (0, 0, -55)),
        ("pd", "UV-C sensor window, photodiode and amplifier", pd, 9, "#D4A017", (75, 0, 0)),
        ("ctrl", "Controller and LED driver", ctrl, 10, "#15803D", (70, 0, 0)),
        ("valve", "Solenoid shutoff valve", valve, 11, "#C2410C", (0, 0, 55)),
        ("adapter", "24 V power adapter", adapter, 12, "#4B5563", (80, 0, -120)),
        ("encl", "Electronics enclosure", encl, 13, "#E5E7EB", (140, 0, 0)),
        ("lid", "Enclosure lid", lid, 13, "#F3F4F6", (140, -60, 0)),
        ("bar", "UV level bar, five segments", bar, 13, "#2DD4BF", (140, -75, 0)),
        ("led_cable", "LED head cable and plug, with interlock loop", cab, 10, "#111827", (40, -40, -120)),
        ("bracket", "Bracket plate", plate, 14, "#9CA3AF", (0, 120, 0)),
        ("saddles", "Sensor and valve saddles", saddles, 14, "#A3A3A3", (0, 90, 0)),
        ("clamps", "Pipe clamps", clamps, 18, "#52525B", (0, 70, 0)),
        ("fittings", "Fittings, stem adaptors and outlet sleeve", fittings, 15, "#60A5FA", (-30, 0, -170)),
        ("rods", "Tie rods, M5 316", rods, 16, "#52525B", (0, 0, 30)),
        ("ret_screws", "Retaining ring screws, M3 countersunk", ret_screws, 16, "#27272A", (0, 0, -90)),
        ("head_screws", "LED head screws, M4", head_screws, 16, "#27272A", (0, 0, -60)),
        ("board_screws", "LED board screws, M3", board_screws, 16, "#27272A", (0, 0, -170)),
        ("retainer", "Window retaining ring", retainer, 17, "#94A3B8", (0, 0, -90)),
        ("washer", "Window washer, PTFE 0.5 mm", washer, 17, "#E5E7EB", (0, 0, -95)),
        ("gasket", "Window gasket, EPDM", gasket, 17, "#1F2937", (0, 0, -100)),
        ("orings", "Face O-rings, EPDM", orings, 17, "#1F2937", (0, 0, -20)),
        ("label_cap", "UV-C warning label, lower cap", lab_cap, 19, "#F2C94C", (0, -30, -55)),
        ("label_lid", "UV-C warning label, inside the lid", lab_lid, 19, "#F2C94C", (140, -65, 0)),
        ("label_prod", "Product label", lab_prod, 19, "#F4F4F2", (160, 0, 0)),
    ]
    return parts


def build(P=PARAMS, include_adapter=True):
    """Whole assembly as one Compound."""
    from build123d import Compound
    return Compound(children=[s for k, _, s, *_ in build_parts(P) if include_adapter or k != "adapter"])


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
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
    asm = build()
    export_step(asm, str(out / "step" / "lumaflow-assembly.step"))
    export_stl(asm, str(out / "stl" / "lumaflow-assembly.stl"), tolerance=0.05, angular_tolerance=0.3)
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
