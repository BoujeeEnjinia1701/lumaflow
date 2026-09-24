# LumaFlow

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Water Security · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $200 USD · **Difficulty:** 2 of 5

Inline UV-C LED reactor with a flow-activated switch and a dose monitor, sized for a household tap.

## Problem

Point-of-use disinfection often depends on mercury UV lamps that break.

## Concept

Inline UV-C LED reactor with a flow-activated switch and a dose monitor, sized for a household tap.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- UV-C LEDs 265 to 280 nm
- Aluminum heat sink
- Quartz sleeve
- Flow switch
- UV photodiode
- LED driver

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> UV-C light damages eyes and skin. Interlock the housing so LEDs cannot run when open.

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
