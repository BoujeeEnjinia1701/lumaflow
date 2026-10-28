---
doc_id: LMF-PLN-001
title: LumaFlow project plan
project: LumaFlow
doc_type: Project plan
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.8 upgrade: workstreams, resources, stage gates and references"
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Reactor tracer test added to P4 verification (O-4 (a), decided by Amish 2026-10-25)'
---

# LumaFlow project plan

LumaFlow is at TRL 3 and pipeline stage P3 (design outputs), the portfolio cap. The next gate, P4 verification, is on hold until Amish lifts the cap; the decision requested now is the concept selection between options A and B (LMF-DEC-001, O-1). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept and requirements | Project lead (Amish) | PRB, URS, PRS, OPT, concept selection | Done on paper; O-1 awaiting Amish |
| Science and calculations | Design lead | STM, CAL, RTM | Done; STEM check open on four measurement items |
| Design outputs | Design lead | Model at D3 for every option, STEP, drawings, priced BOM, build plan, DEC | Done for option A |
| Regulatory and risk | Design lead with a consultant later | REG, RSK with design FMEA | First pass done; many rows "to assess" |
| Partner | Project lead (Amish) | Agreement with a university extension programme for private well owners | Not yet approached |
| Verification (P4) | Design lead with the partner | Test plans and lab reports, including the reactor tracer test for the residence-time distribution (O-4, decided by Amish 2026-10-25) | On hold (TRL cap 3) |

## Resources needed

Table 2. Resources (for P4, on hold; costs are rough estimates for planning, not quotes).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Prototype parts | One unit to the build plan | Parts as BOM | 433 (priced BOM) |
| Machine shop | Two end caps, tube boss weld, holder | 1 to 2 days of shop time | Included in the BOM estimates |
| UV-C reflectance and transmittance measurement | Liner reflectance (S8) and transmittance (S10) at 275 nm | Partner or university optics lab | To assess |
| Biodosimetry (MS2 or similar) | Measured RED at 90 %/cm and 70 %/cm | Partner microbiology lab | To assess |
| Firmware sketch and bench rig | Dose rule, 1 s fail-safe, interlocks (PR-004) | Electronics lead, about 2 weeks | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Met (kit 1.8 upgrade, 2026-10-25) |
| P1 Definition | URS, PRS draft, RSK, MKT | Met |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR | Met on paper; the DDR is proposed, awaiting Amish |
| P3 Design outputs | Model, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability | Met for option A (2026-10-25) |
| P4 Verification | Test plans and lab reports, verification report | On hold (TRL cap 3) |
| P5 Validation | Field trial with the partner on real wells | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. **Amish:** choose between option A (axial UV-C LED reactor) and option B (hollow-fibre ultrafilter), which scored within 10 % (O-1), and whether to graft the runner-up's best idea (O-2).
2. **Amish:** send the first message to the extension programme (draft in the review note of 2026-10-02).
3. When the TRL cap is lifted: measure the liner (S8, S10), run biodosimetry (PR-002, PR-003), write the firmware sketch and test PR-004, then plate counts for regrowth and photorepair (S6, S7).

## References

- Beck, S. E., et al. "Evaluating UV-C LED Disinfection Performance and Investigating Potential Dual-Wavelength Synergy." *Water Research* 109 (2017): 207 to 216. https://pmc.ncbi.nlm.nih.gov/articles/PMC6145099.
- US Code of Federal Regulations. 40 CFR 141.720. https://www.law.cornell.edu/cfr/text/40/141.720.
- US Code of Federal Regulations. 21 CFR 177.1550 and 177.2470. https://www.law.cornell.edu/cfr/text/21/177.1550; https://www.law.cornell.edu/cfr/text/21/177.2470.
- US EPA. *Ultraviolet Disinfection Guidance Manual toolkit*, EPA 815-B-21-007. https://www.epa.gov/system/files/documents/2022-05/uv-toolkit-815-B-21-007_0.pdf.
- US EPA. *Membrane Filtration Guidance Manual*, EPA 815-R-06-009. 2005.
- Fresh Water Systems. "NSF Class A and Class B." https://www.freshwatersystems.com/blogs/blog/nsf-class-a-and-class-b.
- Fresh Water Systems. "How to maintain your UV system." https://www.freshwatersystems.com/blogs/blog/how-to-maintain-your-uv-system.
- Fresh Water Systems. VIQUA VT1 and VH200-F10 product pages. Accessed 2026-10-25.
- ANSI. "NSF/ANSI 55-2024." https://blog.ansi.org/ansi/nsf-ansi-55-2024-ultraviolet-uv-water-treatment/.
- AquiSense. "Mercury-free." https://aquisense.com/mercury-free/; PearlAqua Micro and Deca pages.
- Minamata Convention on Mercury. https://minamataconvention.org/en/news/mercury-containing-lamps-phased-out-minamata-convention-offices-geneva.
- Momentive Technologies. Fused quartz mechanical properties. https://www.momentivetech.com/materials/fused-quartz-materials/quartz-properties/mechanical-properties.
- Nomadic Supply. Acuva ArrowMax 2.0. https://nomadicsupply.com/acuva-arrowmax-2-0-12v-ac-dc-uv-water-purifier/. Accessed 2026-10-25.
- Standards Council of Canada. IEC 60335-2-109:2023. https://scc-ccn.ca/standardsdb/standards/2053444. Accessed 2026-10-25.
- Tech-LED. "UV-C LEDs for disinfection and sterilization." https://tech-led.com/uv-c-leds-for-disinfection-and-sterilization-component-selection-265-280-nm/.
- UL Solutions. "Health effects and lead content of drinking water products." https://www.ul.com/services/health-effects-and-lead-content-drinking-water-products. Accessed 2026-10-25.
- USGS. Domestic (private) supply wells. https://www.usgs.gov/mission-areas/water-resources/science/domestic-private-supply-wells.
- VIQUA. Specification sheet LIT520326. https://viqua.com/wp-content/uploads/LIT520326_SpecSheet.pdf.
- Waterdrop Canada. Under-sink ultrafiltration system. https://waterdropfilter.ca/products/undersink-ultrafiltration-water-filter-system-with-dedicated-faucet. Accessed 2026-10-25.
- WHO. Drinking-water fact sheet. https://www.who.int/news-room/fact-sheets/detail/drinking-water.
- WHO. International Scheme to Evaluate Household Water Treatment Technologies. https://www.who.int/tools/international-scheme-to-evaluate-household-water-treatment-technologies.
- WHO and UNICEF JMP. *Progress on Household Drinking Water, Sanitation and Hygiene 2000 to 2022*. 2023.
- Young, W. C., and R. G. Budynas. *Roark's Formulas for Stress and Strain*. 7th ed. New York: McGraw-Hill, 2002.
- Research reactor papers cited in LMF-PRB-001 (flow-through reactor efficiency, cylindrical reactor optimization, dual-wavelength point-of-use device, critical review 2024, UVC-LED efficacy and water quality).
