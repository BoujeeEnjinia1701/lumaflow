---
doc_id: LMF-MKT-001
title: LumaFlow market and viability
project: LumaFlow
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.8 upgrade: segments, cited benchmarks and the open route"
---

# LumaFlow market and viability

LumaFlow is for households on private wells, small clinics and researchers who want an inspectable, flow-switched UV-C LED stage at one drinking tap; it competes with tap-scale mercury UV units that run all day and closed UV-C LED purifiers, and its value is that every dimension, dose calculation and part is open. At an estimated USD 433 in prototype parts it costs about the same as the commercial units it is compared with, so its case rests on openness, repairability and no mercury, not on price. Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Private-well households | 43 million people on private wells in the United States (USGS) and 3 to 4 million in Canada (CMAJ), cited in the README | VIQUA VT1 tap-scale mercury UV system, 1 gpm, 13 W: USD 315.00 (MSRP USD 390.00), Fresh Water Systems, checked 2026-10-25 | 418 (prototype parts, BOM) | No mercury, no warm-up, no yearly lamp, about 3.9 kWh a year instead of about 114 kWh; an alarm and valve rather than silent failure |
| UV-C LED point-of-use buyers (homes, RVs, boats, cabins) | North America, off-grid users on 12 to 24 V DC | Acuva ArrowMax 2.0 UV-LED purifier, 2.0 L/min, 9 W active: USD 349.95 (list USD 599.95), Nomadic Supply, checked 2026-10-25 | 433 | Open and repairable; the same flow-switched principle with published dose calculations |
| Small clinics, schools, community water points | Rural sites with mains power, low- and middle-income countries | Commercial UV-C LED units above (no clinic-specific price found) | 433, less with LED quantity prices | Local repair from catalogue parts; status bar visible to staff |
| Researchers and makers | University labs, makerspaces | Closed commercial reactors (AquiSense PearlAqua Micro, price on request; not cited) | 433 | A documented reference reactor to test optics, LEDs and dose sensing |
| Option B comparison (if chosen) | Same households | Waterdrop under-sink ultrafiltration system, 0.01 µm: CAD 125.99 (sale), Waterdrop Canada, checked 2026-10-25 | 120 to 180 (first-order estimate) | Unpowered; an open design would add an integrity test port and gauges |

Whole-house UV for comparison: VIQUA VH200-F10, 9 gpm, 35 W, USD 980.00 (MSRP USD 1,195.00), Fresh Water Systems, checked 2026-10-25. It treats every tap and is outside LumaFlow's scope.

## Open route

LumaFlow spreads as an open design under CERN-OHL-S-2.0 (hardware) and MIT (software): a university extension programme, makerspace or water charity can build one from catalogue LEDs, a stainless tube, two machined caps and push-fit plumbing, test it and publish improvements through the build-report issue template. The first route is the co-design partner decided by Amish (a university extension programme for private well owners), which can measure UV transmittance on real wells and run TRL 4 tests. What keeps it open: the strong reciprocal licence, the published calculation scripts and model, and no certification claim that would tie the design to one maker. A certified product, if anyone pursues one, would be a separate step with a partner and a test laboratory (LMF-REG-001).

## Sources

- Fresh Water Systems, "VIQUA VT1 Copper Series UV System, 1 gpm, 120 V," https://www.freshwatersystems.com/products/viqua-vt1-copper-series-uv-system-powered-by-sterilight-1gpm-120-volt, accessed 2026-10-25.
- Fresh Water Systems, "VIQUA VH200-F10 Cobalt Series UV System, 9 gpm," https://www.freshwatersystems.com/products/viqua-vh200-f10-cobalt-series-uv-system-powered-by-sterilight-9-gpm, accessed 2026-10-25.
- Nomadic Supply, "Acuva ArrowMax 2.0 12 V AC/DC UV Water Purifier," https://nomadicsupply.com/acuva-arrowmax-2-0-12v-ac-dc-uv-water-purifier/, accessed 2026-10-25.
- Waterdrop Canada, "Undersink ultrafiltration water filter system with dedicated faucet," https://waterdropfilter.ca/products/undersink-ultrafiltration-water-filter-system-with-dedicated-faucet, accessed 2026-10-25.
- USGS, domestic (private) supply wells, https://www.usgs.gov/mission-areas/water-resources/science/domestic-private-supply-wells; CMAJ (2010), https://www.cmaj.ca/content/182/10/1061, both cited in the README.
- AquiSense, PearlAqua Micro, https://aquisense.com/products/water-treatment/pearl-aqua-micro/, cited in LMF-PRB-001 (no price published).
