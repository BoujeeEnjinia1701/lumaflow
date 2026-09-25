"""LumaFlow general arrangement sheet LMF-DWG-001, Rev P1 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/LMF-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py. Dimensions are taken from the model bounding box and levels(), so they follow
any parameter change. The 24 V adapter (item 12) sits loose on the cabinet floor and is not drawn.
The concept sheet in media/ is LMF-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, project_views, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build, levels  # noqa: E402

DATE = "2026-09-25"


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text):
    a = 1.4
    cx, cy = x - 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    L = levels()
    work = ROOT / "cad" / "drawings" / "_views"
    asm = build(include_adapter=False)
    views = project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="LumaFlow", title="General arrangement", dwg_no="LMF-DWG-001", rev="P1",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="316 tube and lower cap, PTFE liner, fused silica window, acetal upper cap; see bom/bom.csv. "
                       "PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    out = []
    # top view: overall width and depth
    x, y, w, h = c["top"]
    out += dim_h(x, x + w, y - 3.5, f"{bb.size.X:.0f} overall")
    out += dim_v(x - 4, y, y + h, f"{bb.size.Y:.0f}")
    # front view (from -Y): overall height; port and window heights from the cabinet floor
    x, y, w, h = c["front"]
    zb = y + h
    ax_x = x + (0 - bb.min.X) * k                                  # reactor axis
    out += dim_v(x - 26, y, zb, f"{bb.size.Z:.0f} overall")
    for i, (z, name) in enumerate([(L["z_out"], "outlet"), (L["z_in"], "inlet"), (L["z_win1"], "window")]):
        zy = zb - z * k
        xd = x - 5 - 7 * i
        out += [ext(x - 0.5 if i < 2 else ax_x, zy, xd - 1, zy)]
        out += dim_v(xd, zy, zb, f"{z:.0f} {name}")
    # right view (from +X): cap diameter
    x, y, w, h = c["right"]
    yc = x + (0 - bb.min.Y) * k
    cl, cr = yc - P["cap_d"] / 2 * k, yc + P["cap_d"] / 2 * k
    yt = y + h - L["z_top"] * k
    out += [ext(cl, yt, cl, y - 5), ext(cr, yt, cr, y - 5)]
    out += dim_h(cl, cr, y - 4, f"D{P['cap_d']:.0f} caps")
    s._layers += out
    s.add_svg(views["iso"], 276, 32, 140, 100, label="Isometric view", sublabel="Not to scale; adapter not shown")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Unit {bb.size.X:.0f} W x {bb.size.Y:.0f} D x {bb.size.Z:.0f} H, adapter excluded",
        f"Channel D{P['bore_d']:.0f} x {L['channel_len']:.0f}; ports at Z {L['z_in']:.0f} and {L['z_out']:.0f}",
        f"Tube D{P['tube_od']:.0f} x 3 wall x {P['tube_len']:.0f}, 316; PTFE liner D{P['liner_od']:.0f}",
        f"Window D{P['win_d']:.0f} x {P['win_t']:.0f} fused silica on a D{P['aperture_d']:.0f} seat",
        f"{P['led_n']} x 275 nm LEDs on a {2 * P['led_pcr']:.0f} mm circle, {P['led_gap']} mm below window",
        f"Caps D{P['cap_d']:.0f} x {P['cap_lo_h']:.0f}; {P['n_rod']} x M4 316 tie rods on D{2 * P['rod_pcr']:.0f}",
        "Ports 3/8 in push-fit; outlet through a 316 insert",
        f"Heat sink {P['sink_w']:.0f} x {P['sink_w']:.0f} x {P['fin_h'] + P['sink_base']:.0f}, fins down",
        "Working pressure 8 bar; flow up; mount vertical",
        "Third-angle; front view from -Y, right view from +X",
    ], x=276, y=150, width=140)
    path = s.save(ROOT / "cad" / "drawings" / "LMF-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {path} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
