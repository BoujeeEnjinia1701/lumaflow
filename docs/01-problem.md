---
doc_id: LMF-PRB-001
title: LumaFlow problem statement
project: LumaFlow
doc_type: Problem statement
version: "0.5"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions (LMF-DDR-001) on the first user, dose target and budget; partner stays open
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); dose gap closed at 1.2 L/min, pressure limiter at installation, budget figure open
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish ($340)
---

# LumaFlow problem statement

Point-of-use disinfection often depends on mercury UV lamps that break, need a warm-up, run around the clock and are replaced every year, so households with a private well or an unreliable supply either pay for that upkeep or go without. There is no open, inspectable design for a small UV-C LED reactor that switches on only when water flows and tells the user whether the dose was delivered.

## The problem

Ultraviolet light at about 250 to 280 nm inactivates bacteria, viruses and protozoa by damaging their DNA and RNA, without adding chemicals or changing taste. Household UV systems have used low-pressure mercury lamps for decades. Those lamps have four drawbacks at the scale of one kitchen tap:

1. **Mercury and glass.** The lamp contains mercury inside a quartz sleeve. A cracked sleeve or lamp can release mercury into the water line and the home. The Minamata Convention on Mercury is driving mercury-containing lamps out of general use ([Minamata Convention](https://minamataconvention.org/en/news/mercury-containing-lamps-phased-out-minamata-convention-offices-geneva)), and makers of UV-C LED systems market mercury-free operation as the main reason to switch ([AquiSense](https://aquisense.com/mercury-free/)).
2. **Warm-up and continuous running.** A mercury lamp takes time to reach full output, so household units usually run all day and night even though water flows for only a few minutes a day. That wastes energy and heats standing water.
3. **Annual replacement.** Lamp output falls with use, so suppliers advise replacing the lamp about once a year whether or not it has failed ([Fresh Water Systems](https://www.freshwatersystems.com/blogs/blog/how-to-maintain-your-uv-system)).
4. **Silent failure.** Many low-cost units have no UV sensor. The user cannot tell whether the lamp has aged or the sleeve has fouled. NSF/ANSI 55 Class A systems must include a UV sensor and an alarm, but lower-cost Class B and uncertified units need not ([Fresh Water Systems, NSF Class A and B](https://www.freshwatersystems.com/blogs/blog/nsf-class-a-and-class-b); [ANSI blog on NSF/ANSI 55-2024](https://blog.ansi.org/ansi/nsf-ansi-55-2024-ultraviolet-uv-water-treatment/)).

UV-C LEDs remove the mercury, reach full output in microseconds and can switch with the flow. Their weakness is efficiency: current UV-C LEDs turn only about 2 to 5 % of electrical input into UV-C, and many lose 30 to 50 % of their output within 5,000 to 10,000 h ([Tech-LED selection guide](https://tech-led.com/uv-c-leds-for-disinfection-and-sterilization-component-selection-265-280-nm/); [status of 265 nm LEDs, 2023](https://www.researchgate.net/publication/373791832_Status_of_Performance_and_Reliability_of_265_nm_Commercial_UV-C_LEDs_in_2023)). A reactor that runs only while water flows turns that weakness around: a few minutes of on-time a day makes the rated life last for many years.

## Prior work

- **Commercial UV-C LED units.** AquiSense sells compact flow-through UV-C LED reactors for point-of-use integration ([PearlAqua Micro](https://aquisense.com/products/water-treatment/pearl-aqua-micro/)) and a whole-house point-of-entry unit ([PearlAqua Deca launch](https://aquisense.com/pearlaqua-deca-point-of-entry-launch/)). These are closed designs sold to integrators and households at commercial prices.
- **Research reactors.** Flow-through UV-C LED reactors have been studied for their optics, flow pattern and LED placement ([efficiency improvement of a flow-through reactor](https://www.sciencedirect.com/science/article/abs/pii/S2214714420306966); [cylindrical reactor design optimization](https://www.sciencedirect.com/science/article/abs/pii/S2213343724004962); [dual-wavelength point-of-use device](https://doi.org/10.3390/w17202965)). Reviews conclude that LED reactors are practical at small flows and that reactor design, not only LED power, sets the delivered dose ([critical review, 2024](https://www.sciencedirect.com/science/article/pii/S2589914724000616)). UV-C LED dose response depends strongly on water quality ([UVC-LED efficacy and water quality](https://pubmed.ncbi.nlm.nih.gov/39213680/)).
- **Standards and schemes.** NSF/ANSI 55 Class A calls for 40 mJ/cm² at the rated flow and at 70 % UV transmittance or the alarm set point, whichever is lower; Class B calls for 16 mJ/cm² (sources above). The WHO International Scheme to Evaluate Household Water Treatment Technologies rates devices by their log reduction of bacteria, viruses and protozoa ([WHO HWT scheme](https://www.who.int/tools/international-scheme-to-evaluate-household-water-treatment-technologies)). The US EPA UV guidance gives dose tables per pathogen; adenovirus in particular needs far higher doses than bacteria ([EPA UV toolkit](https://www.epa.gov/system/files/documents/2022-05/uv-toolkit-815-B-21-007_0.pdf)).

The gap LumaFlow addresses is an **open, documented, garage-buildable** tap-scale reactor with flow switching and a dose monitor that fails safe, which researchers, makers and small water projects can inspect, reproduce and test.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Household on a private well or rainwater tank | Safe drinking water at one tap without chemicals, mercury or a yearly lamp | Under the kitchen sink, feeding a dedicated drinking-water faucet |
| Household with an intermittent or suspect municipal supply | A barrier against microbial contamination after pressure drops or boil-water events | Same, downstream of a sediment or carbon filter |
| Small clinic, school or community water point | A low-maintenance disinfection stage for a drinking-water tap | Indoor, mains power available |
| Researcher or maker | An open reference design to test reactor geometries, LEDs and dose sensing | Lab bench, makerspace |

Typical conditions assumed for the concept: water supply pressure of 2 to 6 bar (29 to 87 psi), water temperature 5 to 30 °C, cabinet air up to 35 °C, and a drinking and cooking demand of about 10 to 20 L per household per day drawn in short bursts.

## Constraints

- Garage-buildable prototype, $340 USD or less in parts (budget raised from $200 to $225 by Amish, LMF-DDR-001 D2, then to $340 by the budget top-up Amish approved on 2026-09-26), from off-the-shelf LEDs, sensors and plumbing plus simple machined end caps. The re-priced 50 mm reactor costs $338.00.
- A drinking-water flow of 1.2 L/min (0.32 gpm) is enough for one tap; it fills a 1 L bottle in about 50 s.
- A sediment pre-filter and a pressure-limiting valve at 4 bar (58 psi) or less are part of the installation.
- Fits under a kitchen sink and connects to a standard cold line with push-fit fittings.
- Wetted parts must be food-contact grade; no printed plastic on the water path.
- Only safety extra-low voltage (24 V DC) at the unit; mains stays inside a certified external adapter.
- Research and educational prototype only. LumaFlow is not a certified water treatment device, and the documents must not claim that its water is safe to drink.

## Out of scope

- Removal of chemicals, metals, nitrate, taste or odor. UV does not remove them, and it leaves no residual disinfectant in the pipes after the reactor.
- Whole-house (point-of-entry) flow rates of 20 L/min or more.
- Turbid or iron-rich water without pre-treatment; UV needs clear water to work.
- Certification testing to NSF/ANSI 55 or the WHO scheme (a later step, not part of this portfolio phase).

## Decisions and open questions

- **First user (decided).** A well-water household with a sediment pre-filter. Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-001 D9). This sets the design water quality at 90 %/cm UVT or better.
- **Dose target (decided).** The Class A dose level of 40 mJ/cm² is the target for clear water (90 %/cm or better), with an alarm and valve closure below it, and the 70 %/cm test condition kept visibly not met. Decided by Amish, 2026-09-25: go with recommendation (LMF-DDR-001 D1). The first TRL 3 calculation found only 14.7 to 19.0 mJ/cm² in clear water; with the route Amish accepted on 2026-09-25 (LMF-DDR-002: 50 mm bore, high-reflectance liner, 1.2 L/min design flow) LMF-CAL-001 v0.2 gives 51.9 to 76.3 mJ/cm².
- **Partner (open).** Which partner (a well-water association, a university lab or a water charity) could supply real water-quality data and later test the reactor? Proposed, awaiting Amish; the portfolio decision is to pick partners per area later.
