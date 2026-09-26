---
doc_id: LMF-DDR-001
title: LumaFlow TRL 2 review decisions
project: LumaFlow
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); O2 and O3 decided, O1 stays open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D9; O2 and O3 accepted in LMF-DDR-002; O1 remains proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open. TRL 4 work is on hold by the same instruction.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (TRL 2 session) and in LMF-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Design water quality and dose target | Option A: design for 90 %/cm UVT, alarm and close the valve below 40 mJ/cm², and keep R3 (70 %/cm) visibly not met; Option C (flow limiting in poor water) is a later upgrade. Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Budget | Raise `budget_usd` from $200 to $225, keeping the shutoff valve as the fail-safe. Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | LED layout | Axial LED head shining up the tube through a flat quartz window, rather than LEDs around a quartz sleeve. Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | Wavelength | 275 nm LEDs rather than 265 nm, prices to be revisited. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Flow switch | Hall-effect flow sensor as both switch and meter, rather than a reed flow switch. Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | Fail-safe | Normally closed outlet valve that closes on alarm and on power loss. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Orientation | Vertical mounting with upward flow and the LEDs at the bottom. Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | Power | External certified 24 V adapter on a GFCI or RCD-protected outlet; only 24 V DC at the unit. Decided by Amish, 2026-09-25: go with recommendation. |
| D9 | First user | A well-water household with a sediment pre-filter. Decided by Amish, 2026-09-25: go with recommendation. |

Notes on the decided items:

- **D1.** R2 and R3 in LMF-REQ-001 v0.3 keep their targets. LMF-CAL-001 shows that the TRL 2 dose estimate was about three times too high: at 90 %/cm the laminar RED is 14.7 mJ/cm² [B5], so R2 is now not met as well as R3. Under D1 the unit, as drawn, would alarm and close its valve in any water. The routes to close R2 are new proposals (O3) in `docs/REVIEW.md`; D1 itself is recorded as decided and not reopened here.
- **D2.** `budget_usd` in `project.yaml` is now 225, and R16 is redefined to $225. The TRL 3 BOM totals $249.00 [I1], so R16 is still not met; see O3.
- **D5.** At TRL 3 the assumed sensor gives only 0.04 s of margin on the 0.5 s switch-on time (LMF-CAL-001, D2); a higher pulse-rate sensor is proposed in O3. The decision to use a Hall-effect sensor stands.
- **SwapCell.** LumaFlow is mains-powered through a 24 V adapter and uses no SwapCell pack. The portfolio decisions of 2026-09-25 on the SwapCell interface (v0.3 items: wake without CAN, charge-while-discharging mode, latch vibration rating) and on pricing shared packs once do not change the LumaFlow design or BOM.
- **Pitch and problem lines.** The review recommended no change to the `pitch` or `problem` wording, so `project.yaml` and `README.md` keep them.

*Table 2. Items left open by this record. O2 and O3 were decided on 2026-09-25 in LMF-DDR-002; O1 stays open.*

| # | Item | Why it stays open |
| --- | --- | --- |
| O1 | Partner that can supply real well-water UVT data and later test the reactor (a well-water association, a university lab or a water charity) | Proposed, awaiting Amish. No partner was recommended; the portfolio decision is to pick co-design partners per area later |
| O2 | End cap material (acetal or 316 stainless) | Listed as an open question at TRL 2 with no recommendation. The TRL 3 model uses a 316 lower cap and a PTFE-shielded acetal upper cap, which LMF-CAL-001 supports (F5 and R11). Decided by Amish, 2026-09-25: go with recommendation (confirm), LMF-DDR-002 E1 |
| O3 | New TRL 3 proposals: route to close R2, dose monitor position, budget after re-pricing, flow sensor pulse rate, pressure limiter as an installation requirement, thermal cut-back | Raised by LMF-CAL-001 after the decision. Decided by Amish, 2026-09-25: go with recommendation, LMF-DDR-002 E2 to E8 (the budget figure after re-pricing stays open) |

## Consequences

- LMF-PRB-001, LMF-PRC-001 and LMF-REQ-001 are revised to v0.3 to show the decisions: the design choices D1 and D3 to D8 are no longer "proposed", the first user is named, R16 carries the $225 target, and the numbers are replaced by those of LMF-CAL-001.
- `project.yaml` carries `budget_usd: 225`.
- The partner question (O1) stays open in LMF-PRB-001.
