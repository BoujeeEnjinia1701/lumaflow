"""LumaFlow parametric model (build123d), TRL 3, massing-plus level of detail.
Revised for LMF-DDR-002 (2026-09-25): 50 mm bore, high-reflectance PTFE liner, wall dose sensor at mid height.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    lumaflow-assembly.step / .stl     whole unit on its wall bracket, adapter on the cabinet floor
    reactor.step / .stl               tube, PTFE liner and top disc, end caps, quartz window, tie rods
    led-head.step / .stl              LED board, heat spreader ring and finned heat sink

Axes: Z up along the reactor axis (water flows upward, LEDs at the bottom shine up),
X to the right (-X is the plumbing side), Y toward the cabinet wall (+Y). Cabinet floor at Z = 0.
Units mm. Part numbers match bom/bom.csv and the exploded view.

Main dimensions and interfaces only; not fabrication detail; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (LMF-CAL-001).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # water channel and reactor tube (bore widened from 25 to 50 mm by LMF-DDR-002)
    "bore_d": 50.0,          # high-reflectance PTFE liner bore = water channel diameter
    "liner_od": 59.0,        # PTFE liner outside diameter = tube inside diameter
    "tube_od": 65.0,         # 316 stainless reactor tube, 3 mm wall
    "tube_len": 200.0,       # tube between the end caps
    # end caps (lower: 316 stainless; upper: acetal shielded by PTFE), tie rods
    "cap_d": 90.0, "cap_lo_h": 30.0, "cap_hi_h": 30.0,
    "top_disc_t": 3.0,       # PTFE disc closing the channel under the upper cap
    "rod_d": 5.0, "rod_pcr": 39.0, "n_rod": 4,   # M5 316 tie rods on a 39 mm pitch radius
    # quartz window and LED head
    "win_d": 57.0, "win_t": 10.0,
    "aperture_d": 51.0,      # unsupported window diameter (seat shoulder under the rim)
    "led_gap": 0.8,          # LED top to window underside
    "led_n": 6, "led_pcr": 16.0, "led_size": 3.5, "led_h": 1.2,
    "board_d": 44.0, "board_t": 3.0,
    # heat sink (under the LED board) and spreader ring (sink base to lower cap)
    "sink_w": 90.0, "sink_base": 6.0, "fin_h": 24.0, "fin_t": 3.0, "n_fins": 9,
    # ports: 3/8 in (9.5 mm) tube, 7 mm bore; heights above the window top and below the top disc
    "port_od": 9.525, "port_bore": 7.0, "port_in_dz": 7.0, "port_out_dz": 9.0,
    # UV-C photodiode window in the tube wall at mid height of the channel, facing +X (LMF-DDR-002)
    "det_win_d": 8.0,
    # electronics enclosure (right of the reactor), X0, X1, Y0, Y1, Z0, Z1
    "encl": (62.0, 122.0, -22.0, 22.0, 100.0, 230.0),
    # wall bracket: backplate Y and clamp ring heights
    "bracket_y": (49.0, 55.0), "ring_z": (95.0, 225.0), "ring_od": 71.0,
}


def levels(P=PARAMS):
    """Key heights (mm) derived from PARAMS. Used by the drawing sheet and the calc note."""
    L = {}
    L["z_sink0"] = 0.0
    L["z_sink1"] = P["fin_h"] + P["sink_base"]                  # top of sink base, 30
    L["z_board1"] = L["z_sink1"] + P["board_t"]                 # top of LED board = lower cap bottom, 33
    L["z_led1"] = L["z_board1"] + P["led_h"]
    L["z_win0"] = L["z_led1"] + P["led_gap"]                    # window underside, on the seat shoulder
    L["z_win1"] = L["z_win0"] + P["win_t"]                      # window top = channel bottom
    L["z_cap0"] = L["z_board1"] + P["cap_lo_h"]                 # lower cap top = tube bottom
    L["z_cap1"] = L["z_cap0"] + P["tube_len"]                   # tube top = upper cap bottom
    L["z_top"] = L["z_cap1"] + P["cap_hi_h"]                    # upper cap top
    L["z_disc1"] = L["z_top"] - 3.0                             # top disc top face (3 mm cap roof)
    L["z_disc0"] = L["z_disc1"] - P["top_disc_t"]               # channel top
    L["z_in"] = L["z_win1"] + P["port_in_dz"]
    L["z_out"] = L["z_disc0"] - P["port_out_dz"]
    L["channel_len"] = L["z_disc0"] - L["z_win1"]               # irradiated water column
    L["flow_len"] = L["z_out"] - L["z_in"]                      # inlet to outlet
    L["steel_len"] = L["z_cap0"] - L["z_win1"]                  # channel length with a stainless wall
    L["z_det"] = (L["z_win1"] + L["z_disc0"]) / 2               # wall dose sensor, mid height of the channel
    return L


def build_parts(P=PARAMS):
    """Return [(key, name, shape, bom, color, explode)] for every modeled part."""
    from build123d import Box, Cylinder, Pos, Rot

    def box(x0, x1, y0, y1, z0, z1):
        return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)

    def zcyl(r, z0, z1, x=0.0, y=0.0):
        return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)

    def xcyl(r, x0, x1, y=0.0, z=0.0):
        return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)

    def ycyl(r, y0, y1, x=0.0, z=0.0):
        return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)

    L = levels(P)
    rb, rl, rt, rc = P["bore_d"] / 2, P["liner_od"] / 2, P["tube_od"] / 2, P["cap_d"] / 2
    rp, rpb = P["port_od"] / 2, P["port_bore"] / 2
    rd, zd = P["det_win_d"] / 2, L["z_det"]
    xs = -rc - 62                                                  # outer end of the flow sensor and valve bodies
    parts = []

    # 1 Reactor tube, 316 stainless
    tube = (zcyl(rt, L["z_cap0"], L["z_cap1"]) - zcyl(rl, L["z_cap0"] - 1, L["z_cap1"] + 1)
            - xcyl(rd + 0.5, rl - 1, rt + 1, z=zd))                   # sensor window bore at mid height
    # 2 High-reflectance PTFE liner: tube length plus the extension into the upper cap, a solid top disc,
    #   and the sensor window hole in the wall
    liner = (zcyl(rl, L["z_cap0"], L["z_disc0"]) - zcyl(rb, L["z_cap0"] - 1, L["z_disc0"] + 1)
             + zcyl(rl, L["z_disc0"], L["z_disc1"]))
    liner = liner - xcyl(rpb, -rl - 1, -rb + 0.5, z=L["z_out"]) - xcyl(rd, rb - 1, rl + 1, z=zd)
    # 3 Quartz window on the seat shoulder
    window = zcyl(P["win_d"] / 2, L["z_win0"], L["z_win1"])
    # 4 UV-C LED array on a round aluminum-core board
    board = zcyl(P["board_d"] / 2, L["z_sink1"], L["z_board1"])
    s = P["led_size"] / 2
    for i in range(P["led_n"]):
        a = 2 * math.pi * i / P["led_n"]
        x, y = P["led_pcr"] * math.cos(a), P["led_pcr"] * math.sin(a)
        board = board + box(x - s, x + s, y - s, y + s, L["z_board1"], L["z_led1"])
    # 5 Heat sink (fins down) and aluminum spreader ring from the sink base to the stainless lower cap
    hw = P["sink_w"] / 2
    sink = box(-hw, hw, -hw, hw, P["fin_h"], L["z_sink1"])
    pitch = (P["sink_w"] - P["fin_t"]) / (P["n_fins"] - 1)
    for i in range(P["n_fins"]):
        x = -hw + i * pitch
        sink = sink + box(x, x + P["fin_t"], -hw, hw, 0, P["fin_h"])
    sink = sink + (zcyl(rc, L["z_sink1"], L["z_board1"]) - zcyl(P["board_d"] / 2 + 0.5, L["z_sink1"] - 1, L["z_board1"] + 1))
    # 6 Lower end cap, 316 stainless: LED aperture, window pocket and seat, bore, inlet port boss
    cap_lo = (zcyl(rc, L["z_board1"], L["z_cap0"])
              - zcyl(P["aperture_d"] / 2, L["z_board1"] - 1, L["z_win0"])
              - zcyl(P["win_d"] / 2 + 0.5, L["z_win0"], L["z_win1"])
              - zcyl(rb, L["z_win1"] - 0.1, L["z_cap0"] + 1)
              + xcyl(rp + 2, -rc - 12, -rc + 2, z=L["z_in"]))
    cap_lo = cap_lo - xcyl(rpb, -rc - 13, -rb + 0.5, z=L["z_in"])
    # 7 Upper end cap, acetal: liner pocket, outlet port boss
    cap_hi = (zcyl(rc, L["z_cap1"], L["z_top"])
              - zcyl(rl + 0.2, L["z_cap1"] - 1, L["z_disc1"])
              + xcyl(rp + 2, -rc - 12, -rc + 2, z=L["z_out"]))
    cap_hi = cap_hi - xcyl(rp, -rc - 13, -rl + 0.1, z=L["z_out"])
    # 16 Tie rods (M5, 316) with nuts, holding the caps against the 8 bar end load
    rods = None
    for i in range(P["n_rod"]):
        a = math.radians(45 + 360 * i / P["n_rod"])
        x, y = P["rod_pcr"] * math.cos(a), P["rod_pcr"] * math.sin(a)
        r = (zcyl(P["rod_d"] / 2, L["z_sink1"], L["z_top"] + 3.2, x, y)
             + zcyl(4.0, L["z_top"], L["z_top"] + 4.0, x, y))
        rods = r if rods is None else rods + r
        hole = zcyl(P["rod_d"] / 2 + 0.2, L["z_sink1"] - 1, L["z_top"] + 1, x, y)
        cap_lo, cap_hi, sink = cap_lo - hole, cap_hi - hole, sink - hole
    # 8 Hall-effect flow sensor on the inlet line; 11 normally closed valve on the outlet line
    flow = box(xs, xs + 40, -14, 14, L["z_in"] - 14, L["z_in"] + 14) + zcyl(8, L["z_in"] + 14, L["z_in"] + 24, x=xs + 20)
    valve = (box(xs, xs + 40, -14, 14, L["z_out"] - 14, L["z_out"] + 14)
             + zcyl(14, L["z_out"] + 14, L["z_out"] + 44, x=xs + 20))
    # 9 UV-C photodiode in the tube wall at mid height: quartz sensor window in the liner and tube,
    #   clamp-on saddle, TO-46 photodiode can and amplifier, facing +X toward the enclosure
    pd = (xcyl(rd - 0.2, rb, rt, z=zd)
          + (xcyl(11, rt - 4, rt + 6, z=zd) - zcyl(rt, zd - 12, zd + 12))
          + xcyl(6, rt + 6, rt + 14, z=zd) + box(rt + 14, rt + 22, -9, 9, zd - 9, zd + 9))
    # 13 Electronics enclosure with status light, buzzer, lid interlock and cable gland
    EX0, EX1, EY0, EY1, EZ0, EZ1 = P["encl"]
    encl = box(EX0, EX1, EY0, EY1, EZ0, EZ1) - box(EX0 + 2.5, EX1 - 2.5, EY0 + 2.5, EY1 - 2.5, EZ0 + 2.5, EZ1 - 2.5)
    encl = encl + xcyl(4, EX0 - 12, EX0, z=EZ0 + 20) + box(EX0 + 18, EX0 + 42, EY0 - 3, EY0, EZ1 - 30, EZ1 - 18)
    # 10 Controller and LED driver modules inside the enclosure
    ctrl = (box(EX0 + 6, EX1 - 6, 4, 6, EZ0 + 8, EZ1 - 8) + box(EX0 + 12, EX0 + 30, -4, 4, EZ0 + 30, EZ0 + 48)
            + box(EX0 + 30, EX1 - 12, -2, 4, EZ0 + 70, EZ0 + 90))
    # 12 24 V DC adapter on the cabinet floor
    adapter = box(150, 245, -30, 20, 0, 34) + xcyl(3, EX1, 150, y=-5, z=17)
    # 14 Wall bracket: backplate, two clamp rings on the tube, enclosure shelf
    by0, by1 = P["bracket_y"]
    bracket = box(-50, EX1 + 8, by0, by1, 80, 250)
    for z in P["ring_z"]:
        bracket = (bracket + (zcyl(P["ring_od"] / 2, z - 8, z + 8) - zcyl(rt, z - 9, z + 9))
                   + box(-6, 6, P["ring_od"] / 2 - 1, by0, z - 8, z + 8))
    bracket = bracket + box(EX0, EX1, EY1, by0, 150, 180)
    # 15 Fittings: supply line into the flow sensor, sensor to inlet, outlet insert (316) to valve, valve to faucet line
    fittings = (xcyl(rp, xs - 40, xs, z=L["z_in"]) + xcyl(rp, xs + 40, -rc - 12, z=L["z_in"])
                + (xcyl(rp, xs - 40, xs, z=L["z_out"]))
                + (xcyl(rp, xs + 40, -rl + 0.1, z=L["z_out"]) - xcyl(rpb, xs + 39, -rl, z=L["z_out"])))

    parts += [
        ("tube", "Reactor tube, 316 stainless", tube, 1, "#A8B0B8", (0, 0, 0)),
        ("liner", "High-reflectance PTFE liner and top disc", liner, 2, "#F3F4F6", (0, -120, 70)),
        ("window", "Quartz window", window, 3, "#7DD3FC", (0, 0, -115)),
        ("board", "UV-C LED array, 6 x 275 nm", board, 4, "#7C3AED", (0, 0, -160)),
        ("sink", "Heat sink and spreader ring", sink, 5, "#6B7280", (0, 0, -210)),
        ("cap_lo", "Lower end cap, 316 stainless", cap_lo, 6, "#7B8794", (0, 0, -55)),
        ("cap_hi", "Upper end cap, acetal", cap_hi, 7, "#374151", (0, 0, 55)),
        ("flow", "Hall-effect flow sensor", flow, 8, "#0F766E", (0, 0, -55)),
        ("pd", "UV-C wall photodiode and amplifier", pd, 9, "#D4A017", (75, 0, 0)),
        ("ctrl", "Controller and LED driver", ctrl, 10, "#15803D", (70, 0, 0)),
        ("valve", "Solenoid shutoff valve", valve, 11, "#C2410C", (0, 0, 55)),
        ("adapter", "24 V power adapter", adapter, 12, "#4B5563", (80, 0, -120)),
        ("encl", "Electronics enclosure", encl, 13, "#E5E7EB", (140, 0, 0)),
        ("bracket", "Wall bracket", bracket, 14, "#9CA3AF", (0, 120, 0)),
        ("fittings", "Fittings and outlet insert", fittings, 15, "#60A5FA", (-30, 0, -170)),
        ("rods", "Tie rods, M5 316", rods, 16, "#52525B", (0, 0, 30)),
    ]
    return parts


def build(P=PARAMS, include_adapter=True):
    """Whole assembly as one Compound."""
    from build123d import Compound
    return Compound(children=[s for k, _, s, *_ in build_parts(P) if include_adapter or k != "adapter"])


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = {k: s for k, _, s, *_ in build_parts()}
    groups = {"reactor": ["tube", "liner", "window", "cap_lo", "cap_hi", "rods"], "led-head": ["board", "sink"]}
    for name, keys in groups.items():  # export groups before the parts are adopted by the assembly compound
        shape = Compound(children=[parts[k] for k in keys])
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"))
    asm = build()
    export_step(asm, str(out / "step" / "lumaflow-assembly.step"))
    export_stl(asm, str(out / "stl" / "lumaflow-assembly.stl"))
    L = levels()
    bb = build(include_adapter=False).bounding_box()
    print(f"unit without adapter {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm; "
          f"channel {PARAMS['bore_d']:.0f} mm x {L['channel_len']:.0f} mm, inlet to outlet {L['flow_len']:.0f} mm, "
          f"wall sensor at Z {L['z_det']:.0f} mm")
    for k, n, s, *_ in build_parts():
        if not s.is_valid:
            print(f"warning: {n} is not a valid solid")
    print("exported STEP and STL to cad/step and cad/stl")
