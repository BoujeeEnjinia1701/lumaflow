"""Shaded preview of the concept options picture, media/options.png (LMF-OPT-001), from the detailed models.

Run from the repo root:  python cad/src/options_preview.py
Each panel is components(option) from cad/src/model.py, shaded with .kit/concept.py, with the kit's 1.75 m
scale figure standing on the cabinet floor. It is a stand-in so the repo carries an options picture between
publishes: the kit 1.9 picture is a Blender Cycles render made with `python .kit/options.py` (or --export and
--compose on the studio machine), which overwrites this file. Repo-specific helper; nothing here is in .kit/.
"""
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402
import concept  # noqa: E402
import model as M  # noqa: E402

INK, MUTED, ACCENT = "#111827", "#4B5563", "#0F766E"


def panel(key, path):
    parts = [concept.Part(p["name"], p["shape"], p["color"], p.get("bom")) for p in M.components(key)
             if p["kind"] != "context"]
    parts = concept.with_scale_figure(parts, gap=250.0)
    v = M.OPTION_VIEWS.get(key, {})
    concept._render(parts, path, elev=v.get("el", 22), azim=v.get("az", -55), size=(5, 5), dpi=160)
    return Image.open(path).convert("RGB")


def main():
    keys = list(M.OPTIONS)
    n = len(keys)
    with tempfile.TemporaryDirectory() as tmp:
        imgs = [panel(k, Path(tmp) / f"opt-{k}.png") for k in keys]
    fig = plt.figure(figsize=(5.2 * n, 6.6), dpi=160)
    fig.text(0.015, 0.975, f"{M.TITLE}: concept options", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.015, 0.935, "CONCEPT OPTIONS, NOT FOR FABRICATION. Same scale reference in every panel. Shaded preview; "
             "the Cycles render replaces it.", fontsize=8, color="#B45309", va="top")
    fig.text(0.985, 0.975, "github.com/BoujeeEnjinia1701/lumaflow", fontsize=8, color=ACCENT, va="top", ha="right", family="monospace")
    for i, (k, im) in enumerate(zip(keys, imgs)):
        ax = fig.add_axes([i / n + 0.01, 0.2, 1 / n - 0.02, 0.68])
        ax.imshow(im); ax.axis("off")
        fig.text(i / n + 0.02, 0.17, f"Option {k}: {M.OPTIONS[k]}", fontsize=11, fontweight="bold", color=INK, va="top")
        fig.text(i / n + 0.02, 0.12, textwrap.fill(M.PRINCIPLES.get(k, ""), 52), fontsize=8.5, color=MUTED, va="top")
        if k == M.CHOSEN:
            fig.text((i + 1) / n - 0.02, 0.17, "CURRENT DESIGN", fontsize=8, fontweight="bold", color=ACCENT, va="top", ha="right")
    out = ROOT / "media/options.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
