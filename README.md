# LumaFlow

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Water Security · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $225 USD · **Difficulty:** 2 of 5

Inline UV-C LED reactor with a flow-activated switch and a dose monitor, sized for a household tap.

![LumaFlow concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/LMF-DWG-001.pdf) · [Calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Point-of-use disinfection often depends on mercury UV lamps that break.

## Concept

Water flows up a PTFE-lined stainless tube (25 mm bore, 246 mm water column) while six 275 nm UV-C LEDs at the bottom shine up through a quartz window. A flow sensor switches the LEDs on only while water runs, and a UV-C photodiode estimates the dose; if it falls too low, a normally closed valve shuts off the water and an alarm sounds. The TRL 3 calculations ([LMF-CAL-001](docs/04-calcs/01-sizing.md)) found that the PTFE wall absorbs about half of the light in this narrow bore, so the dose at 2 L/min (0.5 gpm) in clear water (90 %/cm UV transmittance) is only 15 to 19 mJ/cm² against the 40 mJ/cm² target. The unit draws 22.6 W while flowing and 0.21 W on standby, and the parts cost $249 against the $225 budget. The routes to close the dose and cost gaps are open decisions in the [review note](docs/REVIEW.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Six 275 nm UV-C LEDs on a heat sink, cooled through a 316 stainless lower end cap into the water
- 316 stainless reactor tube with a PTFE reflector liner and top disc; acetal upper cap shielded from UV-C
- Fused quartz window (6 mm) between the LEDs and the water
- Hall-effect flow sensor acting as the flow switch
- UV-C photodiode dose monitor
- Controller with constant-current LED driver, normally closed shutoff valve, external 24 V adapter

The priced bill of materials is in [bom/bom.csv](bom/bom.csv); the parametric model is `cad/src/model.py`, with STEP and STL exports in `cad/step/` and `cad/stl/`.

## Safety

> UV-C light damages eyes and skin. Interlock the housing so LEDs cannot run when open. LumaFlow is a research and educational prototype, not a certified water treatment device, and as drawn it does not reach its target dose; do not rely on it as a barrier for drinking water. See the safety section of the [design precis](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (LMF-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `LMF-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
