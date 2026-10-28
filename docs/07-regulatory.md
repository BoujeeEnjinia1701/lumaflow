---
doc_id: LMF-REG-001
title: LumaFlow regulatory and standards register
project: LumaFlow
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.8 upgrade: first register for the TRL 3 design (option A), with notes for option B"
---

# LumaFlow regulatory and standards register

Which standards and regulations would apply to LumaFlow as a product, where, and what is needed. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. LumaFlow is a research and educational prototype, not a certified water treatment device (PR-019), and no certification is pursued while the portfolio is capped at TRL 3. Method: STANDARDS section 23. Water-security repos in the portfolio share this research; each row was checked on the date in its source.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | NSF/ANSI 55, ultraviolet microbiological water treatment systems (Class A: 40 mJ/cm² at rated flow and 70 % UVT or the alarm set point, with a UV sensor and alarm; Class B: 16 mJ/cm²) | United States and Canada (voluntary, often required by health authorities) | Performance, sensor and alarm of UV point-of-use and point-of-entry systems | The dose target (PR-002) borrows the Class A dose level; PR-003 (the 70 %/cm condition) is not met, so a Class A claim is not possible as designed | Design lead | Certification needed later; Class A not met (PR-003) |
| G2 | NSF/ANSI 61, drinking water system components, health effects | United States and Canada | Contaminants leached from materials in contact with drinking water | Every wetted part: 316, PTFE, expanded PTFE, fused silica, EPDM O-rings, acetal, push-fit fittings | Design lead with a certification body | To assess (choose certified grades at part selection) |
| G3 | NSF/ANSI 372, lead content | United States | Weighted average lead content of wetted surfaces | Stainless and polymer wetted parts; push-fit fittings and stem adaptors must be lead-free grades | Design lead | To assess |
| G4 | 21 CFR 177.1550 (perfluorocarbon resins), 177.2470 (polyoxymethylene copolymer), 177.2600 (rubber articles) | United States | Food-contact materials | PTFE liner, top disc, washers and expanded PTFE gasket; acetal upper cap; EPDM O-rings | Design lead | Applies: specify compliant grades (PR-011) |
| G5 | IEC 60335-2-109, safety of UV radiation water treatment appliances | International (adopted regionally, for example as EN 60335-2-109) | Electrical and UV radiation safety of household UV water treatment appliances | Applies to LumaFlow as a product: enclosure, interlocks (PR-012), marking | Electrical safety reviewer | Certification needed later; to assess with a test laboratory |
| G6 | IEC 62471, photobiological safety of lamps and lamp systems | International | Risk groups for optical radiation, including UV-C | The LEDs are fully enclosed in use; applies to service with the head removed (warning labels, interlock) | Electrical safety reviewer | To assess |
| G7 | IEC 62368-1 (or the regional equivalent) for the 24 V adapter | International | Safety of power supplies | Met by buying a certified adapter (PR-013) | Design lead | Met by design (bought, certified) |
| G8 | US FCC Part 15 and EU EMC Directive 2014/30/EU | United States; European Union | Emissions from the controller and LED driver | The microcontroller and switching LED driver are unintentional radiators | Electronics lead | To assess (product stage) |
| G9 | EU RoHS Directive 2011/65/EU and WEEE Directive 2012/19/EU | European Union | Hazardous substances in and take-back of electrical equipment | LEDs, boards, adapter | Electronics lead | To assess (product stage) |
| G10 | Minamata Convention on Mercury | International | Phase-out of mercury-added products, including lamps | LumaFlow uses no mercury (PR-006); the convention is part of the case for LED disinfection | Project lead | Met by design |
| G11 | EU Drinking Water Directive (EU) 2020/2184, Article 11 (materials in contact with water) | European Union | Hygiene requirements for materials and products in contact with drinking water | Wetted materials if sold in the EU | Design lead | To assess |
| G12 | WHO International Scheme to Evaluate Household Water Treatment Technologies | International | Performance classes by log reduction of bacteria, viruses and protozoa | A route to an independent performance rating; LumaFlow's virus reduction is small (STM S5) | Project lead with a partner laboratory | To assess (TRL 5 or later) |
| G13 | US EPA Ground Water Rule and state well-water guidance | United States | Private wells are outside the Safe Drinking Water Act; guidance only | Context for the first user (private well household) | Project lead | Does not apply to the device |
| G14 | Plumbing codes for point-of-use devices and backflow (for example the Uniform and International Plumbing Codes) | United States (local adoption) | Connection to the cold line, backflow, accessible shutoff | The installation (tee, pressure-limiting valve, pre-filter, PR-017) | Installer | To assess at installation |

Status: to assess, applies, does not apply, met by design, certification needed later.

Option B (hollow-fibre ultrafilter), if chosen, would fall under NSF/ANSI 53 (health effects of filtration, including cyst reduction) or NSF/ANSI P231 or NSF/ANSI 244 for microbiological claims, in place of G1, G5 and G6; to assess.

## Sources

- NSF/ANSI 55 Class A and B summary: Fresh Water Systems, "NSF Class A and Class B," https://www.freshwatersystems.com/blogs/blog/nsf-class-a-and-class-b, and ANSI blog, "NSF/ANSI 55-2024," https://blog.ansi.org/ansi/nsf-ansi-55-2024-ultraviolet-uv-water-treatment/, both cited in LMF-PRB-001 (checked 2026-09-25).
- NSF/ANSI 61 and 372 scope: UL Solutions, "Health effects and lead content of drinking water products," https://www.ul.com/services/health-effects-and-lead-content-drinking-water-products, accessed 2026-10-25.
- 21 CFR 177.1550 and 177.2470: https://www.law.cornell.edu/cfr/text/21/177.1550 and https://www.law.cornell.edu/cfr/text/21/177.2470, accessed 2026-10-25.
- IEC 60335-2-109:2023 listing (household UV water treatment appliances): Standards Council of Canada, https://scc-ccn.ca/standardsdb/standards/2053444, accessed 2026-10-25.
- Minamata Convention on Mercury, "Mercury-containing lamps phased out," https://minamataconvention.org/en/news/mercury-containing-lamps-phased-out-minamata-convention-offices-geneva, cited in LMF-PRB-001.
- WHO International Scheme to Evaluate Household Water Treatment Technologies, https://www.who.int/tools/international-scheme-to-evaluate-household-water-treatment-technologies, cited in LMF-PRB-001.
- Rows G6 to G9, G11, G14 and the NSF standards named for option B are listed from the standards' own titles; their applicability is "to assess" and needs a test laboratory or regulatory consultant.
