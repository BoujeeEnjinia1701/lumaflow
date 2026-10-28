---
doc_id: LMF-DDR-004
title: LumaFlow concept selection
project: LumaFlow
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Concept selection argued for Amish (kit 1.8 upgrade): options A and B within 10 %, both put to him without a pick"
---

# 0004: Concept selection

- **Date:** 2026-10-25
- **Status:** Proposed, awaiting Amish. Options A and B score within 10 % of each other (228 and 229 of 275, LMF-OPT-001), so both go to Amish without a pick (STANDARDS section 21). Until he decides, the repo stays on option A, the existing design; nothing is redesigned.

## Context

LumaFlow was designed before kit 1.8, so its design is option A. The kit 1.8 upgrade asks for at least one more option with a different working principle, scored against the user requirements (LMF-URS-001). Two were added and modelled at the same detail level as option A (D3, `cad/src/model.py`): a hollow-fibre ultrafilter (B), which removes microbes by size and needs no power, and a radial UV-C LED reactor (C), which shines across a thin quartz tube from outside.

## Options considered

1. **A, axial UV-C LED reactor** (228). Automatic: flow switch, wall dose sensor, normally closed valve and alarm. Meets the clear-water dose on paper with an 18 % margin after the 275 nm response factor; misses the 70 %/cm test water (PR-003, accepted by D1); USD 433 against the USD 340 value-engineering target; needs a machine shop for the 316 parts.
2. **B, hollow-fibre ultrafilter** (229). Unpowered, mostly bought, about USD 120 to 180 (first-order estimate), works in cloudier water; but no automatic alarm on a broken fibre (a manual pressure-decay test instead), about 460 mm tall (over the 350 mm envelope of PR-014), recurring cartridge cost, partial virus removal, and it changes the pitch from "inline UV-C LED reactor".
3. **C, radial UV-C LED reactor** (204). Dry LEDs and no seal in the light path, but about 39 W while flowing (over PR-009), a dose still to be ray-traced and a sensor that reads UVT less directly.

## Decision

Proposed, awaiting Amish: choose between A and B. If A is kept (the repo's pitch), graft from B an automatic leak and stuck-valve check run on each idle pulse with the valve shut, which needs no new parts. If B is chosen, the pitch, PRB, PRC, PRS, CAL, model, drawings, BOM and build plan are redone around it in a later session, and A's flow-switched normally closed valve with an alarm is grafted onto B, driven by a differential pressure sensor. C is not recommended.

## Consequences

- `project.yaml` lists `concept_options: [A, B, C]` and leaves `concept_chosen` unset until Amish decides.
- Every option stays in `cad/src/model.py` at D3 so it can be rendered and compared; the drawing, priced BOM and build plan describe option A only.
- The open decision is entry O-1 in the design decisions register, LMF-DEC-001.
