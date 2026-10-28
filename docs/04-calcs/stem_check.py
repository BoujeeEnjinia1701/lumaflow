"""LumaFlow STEM check calculations (LMF-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py      (about 30 s: it imports sizing.py, which
builds the model and runs the Monte Carlo ray trace)
Writes docs/04-calcs/stem_results.csv, which the table in docs/01b-stem-check.md reproduces.

Rows S1 to S32 check option A, the constructable design of LMF-CAL-001 v0.6, most of them against the numbers
that docs/04-calcs/sizing.py prints; rows B1 to B6 and C1 to C6 are first-order screens of options B
(hollow-fibre ultrafilter) and C (radial UV-C LED reactor) of LMF-OPT-001. Two rows of option A failed on
the first run (2026-10-25) and were fixed under Amish's standing instruction of 2026-10-23 (LMF-DEC-001):
S9, UV-C on the EPDM window gasket and sensor window washer (now expanded PTFE), and S12, the retaining ring
bending at the screw torque the build plan gave (now 0.3 N m instead of 0.5 N m). The failed values are kept
in the 'first run' prints below.
"""
import contextlib
import io
import math
import sys

import numpy as np

sys.path[:0] = [".kit", "docs/04-calcs"]
from stem_check import Check, WITHIN, PLAUSIBLE, FIX  # noqa: E402,F401

with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  LMF-CAL-001; reads cad/src/model.py

P, L = CAL.P, CAL.L
c = Check()

# ------------------------------------------------------------------ Physics: optics and dose (option A)
F90 = CAL.F90
Ptot = CAL.Ptot
out_terms = {k: F90[k] for k in ("absorbed by water", "lost at walls", "lost at top disc", "lost at bottom", "to detector window")}
c.balance("S1", "Of the 0.36 W of UV-C from the LEDs, 84.8 % enters the water and 52.9 % is absorbed by it at 90 %/cm",
          "Physics", "Optics and radiation", inputs={"enters water": F90["enters water"]}, outputs=out_terms, unit="W",
          tolerance=0.01, law="Conservation of radiant power in the Monte Carlo ray trace (absorbed + lost = entering)",
          closed_by="LMF-CAL-001 B2, B3")
c.claim("S2", "Reduction equivalent dose (RED) at 1.2 L/min and 90 %/cm reaches 40 mJ/cm2 for a 254 nm-equivalent response (laminar profile)",
        "Physics", "Optics and radiation", "Fluence rate = absorbed power density / alpha; dose = fluence rate x residence time "
        "along each streamline; RED for a 20 mJ/cm2-per-log challenge organism",
        round(CAL.RED90_l, 1), 40.0, "mJ/cm2", rule="above", closed_by="LMF-CAL-001 B5")
K275 = 0.93      # MS2 inactivation rate per fluence at a 280 nm LED relative to a 254 nm LP lamp (Beck et al. 2017)
c.claim("S3", "Organism response at 275 nm is close enough to that at 254 nm that the RED stays above 40 mJ/cm2",
        "Biology", "Microbiology", "Fluence-based rate constants of MS2: 280 nm LED 0.052 against LP lamp 0.056 cm2/mJ "
        "(ratio 0.93, taken for 275 nm though measured at 280 nm); E. coli 0.31 against 0.27 (Beck et al. 2017); RED x 0.93",
        round(CAL.RED90_w, 1), 40.0, "mJ/cm2", rule="above", closed_by="LMF-CAL-001 B10 (margin 18 %; PR-002 at risk)")
dmin = float(CAL.Dr_l.min())
c.claim("S4", "Even the least-dosed streamline (laminar, on the axis) gets the 4-log dose for Cryptosporidium and Giardia",
        "Biology", "Microbiology", "40 CFR 141.720(d)(1): 22 mJ/cm2 for 4-log Cryptosporidium and Giardia at 254 nm",
        round(dmin * K275, 1), 22.0, "mJ/cm2", rule="above", closed_by="LMF-CAL-001 B7 x 0.93")
c.cited("S5", "LumaFlow is not a virus barrier: 40 to 51 mJ/cm2 is far below the 186 mJ/cm2 for 4-log virus (adenovirus)",
        "Biology", "Microbiology", "40 CFR 141.720(d)(1) virus column: 39 mJ/cm2 for 0.5 log, 186 for 4 log",
        "Non-claim kept in PRC, PRS and the safety notes; about 0.5 log of adenovirus at the design dose", WITHIN, "LMF-PRC-001 Safety; PRS PR-019")
c.cited("S6", "Bacteria do not regain viability by photoreactivation or dark repair after the design dose",
        "Biology", "Microbiology", "Photorepair of UV-C damage is known in bacteria and is smaller at higher doses and at "
        "LED wavelengths near 280 nm (literature review in Beck et al. 2017); not quantified for this reactor",
        "No calculation possible; plate counts with light and dark holding at TRL 4", PLAUSIBLE, "")
c.cited("S7", "Water left standing in the reactor between draws does not regrow bacteria past the outlet, with the "
        "idle LED pulse of 10 s every 4 h", "Biology", "Microbiology",
        "Biofilm regrows in stagnant point-of-use devices; the idle pulse gives the standing water about 38 mJ/cm2 "
        "volume-average per 10 s pulse (twice the 5 s run-on dose of LMF-CAL-001 D4; corrected after the independent review); "
        "downstream valve and tubing are not dosed", "Plate counts at TRL 4 (decided 2026-10-02)", PLAUSIBLE, "")
c.claim("S8", "The dose target is met even if the liner reflects only 0.80, as plain PTFE might, not 0.95",
        "Physics", "Optics and radiation", "Ray trace rerun at a wetted reflectance of 0.80, times the 275 nm factor 0.93; "
        "reflectance of wetted sintered PTFE at 275 nm to be measured (the reviewer's trace needs about 0.72 or more)",
        round(CAL.sens[0.80] * K275, 1), 40.0, "mJ/cm2", rule="above", closed_by="LMF-CAL-001 B8 x 0.93 (5 % margin)")

# S9: UV-C reaching the window gasket. The window is 57 mm across but the retaining ring lets light in only
# within 51 mm; rays refracted outward in 10 mm of quartz reach the top face out to about 34 mm radius, where the
# gasket (25 to 28.5 mm) sits on it, and the gasket's inner edge is the bottom of the water channel.
rng = np.random.default_rng(7)
n = 400_000
k = rng.integers(0, P["led_n"], n)
ang = 2 * np.pi * k / P["led_n"]
z_led = -(P["win_t"] + L["led_gap"]) / 10
pos = np.stack([P["led_pcr"] / 10 * np.cos(ang), P["led_pcr"] / 10 * np.sin(ang), np.full(n, z_led)], 1)
d = CAL.lambert(n, rng, np.tile([0, 0, 1.0], (n, 1)))
z_w0 = -P["win_t"] / 10
pos = pos + d * ((z_w0 - pos[:, 2]) / d[:, 2])[:, None]
ok = np.hypot(pos[:, 0], pos[:, 1]) < P["aperture_d"] / 20
T1, ct = CAL.fresnel_T(d[:, 2], 1.0, CAL.N_QUARTZ)
s = 1.0 / CAL.N_QUARTZ
d = np.column_stack([d[:, 0] * s, d[:, 1] * s, ct])
pos = pos + d * ((0 - pos[:, 2]) / d[:, 2])[:, None]
r_top = np.hypot(pos[:, 0], pos[:, 1])
on_gasket = ok & (r_top >= P["bore_d"] / 20) & (r_top < P["win_d"] / 20)
frac_g = float((T1 * on_gasket).sum() / n)
a_g = math.pi * ((P["win_d"] / 20) ** 2 - (P["bore_d"] / 20) ** 2)          # cm2
e_g = frac_g * Ptot / a_g * 1e3                                              # mW/cm2
hours = 92.0                                                                 # LED hours a year, LMF-CAL-001 E4
dose_g = e_g * 1e-3 * hours * 3600                                           # J/cm2 a year
print(f"S9 first run: {frac_g*100:.1f} % of the LED output reaches the window gasket annulus through the quartz, "
      f"{e_g:.1f} mW/cm2, about {dose_g:.0f} J/cm2 of UV-C a year on EPDM (EPDM was not UV-C stable: fails, fix proposed)")
c.cited("S9", "No UV-C falls on an elastomer: window gasket and sensor window washer", "Chemistry",
        "Materials and polymer chemistry",
        "Photo-oxidation of EPDM under UV-C; ray trace of the light refracted outward in the window: "
        f"{frac_g*100:.1f} % of the LED output, {e_g:.1f} mW/cm2, about {dose_g:.0f} J/cm2 a year on the gasket annulus",
        f"First run: EPDM in the light path (failed). Fix: both seals in food-contact expanded PTFE, which UV-C does not degrade",
        WITHIN, "LMF-DEC-001 D-S1 (2026-10-25)")
c.cited("S10", "UV-C passing through the 3 mm PTFE wall and top disc is too weak to degrade the acetal upper cap",
        "Chemistry", "Materials and polymer chemistry",
        "Sintered PTFE is a diffuse reflector but not opaque at 3 mm; acetal yellows and embrittles under UV; "
        "diffuse transmittance of the liner grade at 275 nm is not published for this part",
        "Measure the liner's transmittance at TRL 4; fallback: a 0.3 mm 316 foil cup in the liner pocket", PLAUSIBLE, "")

# ------------------------------------------------------------------ Physics: strength of materials (option A)
c.claim("S11", "Quartz window 57 x 10 mm on a 51 mm seat stays below the 6.8 MPa design stress at 8 bar",
        "Physics", "Strength of materials", "Simply supported circular plate, sigma = 3 (3 + nu) p a^2 / (8 t^2); "
        "fused quartz design stress 6.8 MPa (Momentive)", round(CAL.OUT["G4"], 2), 6.8, "MPa", closed_by="LMF-CAL-001 G4")
# S12: retaining ring bending under the screw preload
SY_316 = 205.0                    # MPa, 0.2 % proof of 316 sheet (ASTM A240 minimum)
r_scr = P["ret_pcr"]; r_w = (P["aperture_d"] / 2 + P["win_d"] / 2) / 2
arm = r_scr - r_w


def ring_stress(torque_nm, k_nut=0.2):
    f = torque_nm / (k_nut * 0.003) * P["n_ret"]                         # total preload, N (M3)
    m = f / (2 * math.pi * r_scr) * arm                                  # N mm per mm of circumference
    return f, 6 * m / P["ret_t"] ** 2


f05, s05 = ring_stress(0.5)
f03, s03 = ring_stress(0.3)
_, s03hi = ring_stress(0.3, 0.15)
T_FIX, K_LO, K_HI = 0.21, 0.13, 0.16     # D-S2 as revised after the independent review: anti-seize on A4 screws
f_hi, s_hi = ring_stress(T_FIX, K_LO)    # most preload: ring check
f_lo, _ = ring_stress(T_FIX, K_HI)       # least preload: gasket check
print(f"S12 first run: 0.5 N m gives {f05/1e3:.1f} kN of preload and {s05:.0f} MPa in the 2 mm ring against "
      f"{SY_316/1.5:.0f} MPa allowable (205 / 1.5): fails, fix proposed. Fix 0.3 N m: {f03/1e3:.1f} kN, {s03:.0f} MPa "
      f"({s03hi:.0f} MPa if the nut factor is 0.15)")
c.claim("S12", "The 2 mm 316 retaining ring stays within 2/3 of its proof stress at the specified screw torque",
        "Physics", "Strength of materials", "Ring as a cantilever strip between the screw circle (65 mm) and the washer "
        f"centre ({2*r_w:.0f} mm), arm {arm:.1f} mm; preload = T / (K d), K 0.13 to 0.16 with anti-seize; first run at 0.5 N m dry: "
        f"{s05:.0f} MPa (failed); 0.3 N m dry was {s03:.0f} to {s03hi:.0f} MPa (reviewer: too narrow a window)",
        round(s_hi, 0), round(SY_316 / 1.5, 0), "MPa", closed_by="LMF-DEC-001 D-S2 (2026-10-25): 316 sheet, anti-seize, 0.21 N m; worst nut factor 0.13")
a_seal = math.pi * (P["bore_d"] / 2) ** 2
f_p = 0.8 * a_seal
a_gk = math.pi * ((P["win_d"] / 2) ** 2 - (P["bore_d"] / 2) ** 2)
resid = (f_lo - f_p) / a_gk
c.claim("S13", "At 8 bar the window gasket keeps at least twice the water pressure as seating stress",
        "Physics", "Mechanics and statics", f"Least preload {f_lo/1e3:.2f} kN (0.21 N m, K 0.16) less the pressure load on the 50 mm seal "
        f"({f_p/1e3:.2f} kN) over the {a_gk:.0f} mm2 gasket", round(resid, 2), 1.6, "MPa", rule="above",
        closed_by="LMF-DEC-001 D-S2")
F_rod = 0.8 * math.pi * (P["tube_od"] / 2) ** 2 / P["n_rod"]
c.claim("S14", "M5 316 tie rods carry the end load at 8 bar within 0.6 of their proof stress", "Physics",
        "Strength of materials", "Stress = end load / (4 x 14.2 mm2); A4-70 proof stress 450 MPa (ISO 3506-1)",
        round(F_rod / 14.2, 0), 270.0, "MPa", closed_by="LMF-CAL-001 G7")
c.claim("S15", "Reactor tube hoop stress at 8 bar is a small share of the 316 proof stress", "Physics",
        "Strength of materials", "Thin-wall hoop stress p r / t; allowable 205 / 3", round(0.8 * (P["tube_od"] / 2 - 1.5) / 3, 1),
        round(SY_316 / 3, 0), "MPa", closed_by="LMF-CAL-001 G6")
c.claim("S16", "Acetal roof over the liner pocket stays below its long-term design stress at 8 bar", "Physics",
        "Strength of materials", "Clamped circular plate, sigma = 0.75 p a^2 / t^2; acetal long-term design stress 10 MPa (assumed)",
        round(CAL.OUT["G8"], 1), 10.0, "MPa", closed_by="LMF-CAL-001 G8")

# ------------------------------------------------------------------ Physics: heat (option A)
c.claim("S17", "LED board stays at or below 50 degC with continuous flow, at the worst film coefficient", "Physics",
        "Heat transfer", "Two thermal paths in parallel: finned sink to 30 degC air, spreader and 316 cap to 25 degC water",
        round(CAL.OUT["F3"], 1), 50.0, "degC", closed_by="LMF-CAL-001 F3")
Tj = CAL.res_T[300][0] + CAL.P_EACH * CAL.R_JB
c.claim("S18", "LED junctions stay below an 85 degC rating", "Engineering and technology", "Power and link budgets",
        "Board temperature + 10 K/W x 2.11 W per LED; 85 degC is a common junction limit for 3535 UV-C LEDs, to confirm "
        "on the chosen part", round(Tj, 0), 85.0, "degC", closed_by="LMF-CAL-001 F4")
dT = 8.9 / (CAL.Q * CAL.RHO * CAL.CP_W)
c.order_of_magnitude("S19", "The water warms by about 0.11 K carrying 8.9 W of LED heat", "Physics", "Thermodynamics",
                     claimed=0.11, estimate=dT, unit="K", law="Q = m_dot cp dT at 1.2 L/min", closed_by="LMF-CAL-001 F2")
c.claim("S20", "Thermal shock from 5 degC water on a warm window does not crack fused quartz", "Physics", "Heat transfer",
        "Fused silica expansion 0.55e-6 /K (Momentive); thermal stress E alpha dT / (1 - nu) for a 40 K step with E 72 GPa",
        round(72e3 * 0.55e-6 * 40 / (1 - 0.17), 1), 6.8, "MPa", closed_by="This check")

# ------------------------------------------------------------------ Physics: fluids and circuits (option A)
c.claim("S21", "Flow in the 50 mm bore is laminar at 1.2 L/min (the profile itself is not known: see S34)", "Physics",
        "Fluid mechanics", "Re = rho U D / mu with D 50 mm; transition near 2,300", round(CAL.Re20, 0), 2300.0, "",
        closed_by="LMF-CAL-001 A4")
dp_bad = (CAL.q_m3h / 0.2) ** 2 + (CAL.q_m3h / 0.15) ** 2 + CAL.dp_tube + CAL.dp_fit + CAL.dp_ports
c.cited("S22", "Pressure drop stays below 0.5 bar at 1.2 L/min", "Physics", "Fluid mechanics",
        f"dp = (Q / Kv)^2 per component: {CAL.dp:.2f} bar on the assumed Kv 0.35 and 0.25, {dp_bad:.2f} with 0.2 and 0.15, "
        f"{CAL.dp_kv01:.2f} with a direct-acting valve of Kv 0.10 (independent review)",
        "Depends on datasheet Kv; PR-008 at risk until the sensor and valve are chosen", PLAUSIBLE, "")
c.claim("S23", "Mains power while water flows stays at or below 25 W", "Physics", "Electromagnetism and circuits",
        "LED 6 x 350 mA x 6.2 V through a 90 % driver, valve 4.8 W, controller 0.6 W, adapter 88 %",
        round(CAL.P_ac, 1), 25.0, "W", closed_by="LMF-CAL-001 E1")
c.claim("S24", "Standby power stays at or below 0.5 W", "Physics", "Electromagnetism and circuits",
        "Flow sensor 75 mW, outlet pressure sensor 10 mW and MCU sleep through a 70 % light-load adapter, plus 0.1 W no-load", round(CAL.P_sb, 2), 0.5, "W",
        closed_by="LMF-CAL-001 E2")
i_alarm = float(CAL.cur[0.90]) * CAL.thr
c.claim("S25", "The wall photodiode signal at the alarm threshold is well above the amplifier noise floor", "Engineering and technology",
        "Sensing resolution", "Photocurrent at S/S_ref = 0.79 against 10 pA (a hundred times a SiC photodiode's dark current of "
        "about 0.1 pA through a transimpedance amplifier)", round(i_alarm * 1e9, 2), 0.01, "nA", rule="above", closed_by="LMF-CAL-001 C1, C3")
c.claim("S26", "LEDs switch on within 0.5 s of flow starting at 0.3 L/min", "Engineering and technology", "Control",
        "First pulse of a 15 Hz per L/min sensor plus 20 ms", round(CAL.t_on, 2), 0.5, "s", closed_by="LMF-CAL-001 D2")
c.claim("S27", "LED running hours do not limit life within 10 years of household use", "Engineering and technology",
        "Power and link budgets", "92 h a year (flow plus idle pulse) x 10 years against a 10,000 h rated life (L70 class, "
        "to confirm on the chosen part)", 92.0 * 10, 10000.0, "h", closed_by="LMF-CAL-001 E4")

# ------------------------------------------------------------------ added after the independent review (2026-10-25)
c.cited("S33", "The dose stays above 40 mJ/cm2 with the LEDs derated for junction temperature and bin", "Engineering and technology",
        "Power and link budgets", f"Nominal {CAL.RED90_w:.1f} mJ/cm2 (B10); with about 12 % less output near 62 degC and a 10 % "
        "low bin: 37.5 (B11); both factors typical, not yet from the chosen LED's datasheet",
        "Closes when the LED is chosen; if the stack holds, routes to Amish (LMF-DEC-001 O-3)", PLAUSIBLE, "")
c.cited("S34", "Mixing in the reactor leaves the RED between the plug and laminar limits", "Physics", "Fluid mechanics",
        "The laminar profile never develops (entrance length 1.3 m against 0.23 m), the inlet jet has a port Reynolds number of "
        "about 3,000 to 6,000 and the heated lower cap drives buoyant mixing (Richardson number about 6 to 12); a back-mixed "
        "reactor of 5 to 10 tanks in series would give 31 to 39 mJ/cm2 (reviewer's trace)",
        "Residence-time distribution by tracer test at TRL 4 with the side inlet kept (O-4 (a), decided by Amish 2026-10-25); perforated PTFE inlet ring ready if the test shows strong back-mixing", PLAUSIBLE, "")
pr_w, k_w, nu_w = 6.1, 0.607, 0.89e-6
re_w = CAL.U * P["bore_d"] / 1e3 / nu_w
gz = re_w * pr_w * P["bore_d"] / L["steel_len"]
h_st = 1.86 * gz ** (1 / 3) * k_w / (P["bore_d"] / 1e3)
c.claim("S35", "The water-film coefficient in the stainless lower cap bore is at least the 150 W/(m2 K) low end used for the board temperature",
        "Physics", "Heat transfer", f"Developing laminar flow over the first {L['steel_len']:.0f} mm (Sieder-Tate, Nu = 1.86 Gz^(1/3), "
        f"Gz = {gz:.0f}); the fully developed value Nu 3.66 (h about 44) the reviewer used applies only far downstream",
        round(h_st, 0), 150.0, "W/(m2 K)", rule="above", closed_by="This check; LMF-CAL-001 F3")
v_t = CAL.v_t
c.claim("S36", "Closing the outlet valve at full flow keeps the reactor within the 8 bar window rating",
        "Physics", "Fluid mechanics", f"Joukowsky surge rho c v in the 1 m PE inlet tube (c about 400 m/s, v {v_t:.2f} m/s) added "
        "to the 4 bar limiter setting; a rigid copper line would add more, so the tube from the tee stays PE (BOM line 15)",
        round(4.0 + 1000 * 400 * v_t / 1e5, 1), 8.0, "bar", closed_by="This check; PR-017")
c.cited("S37", "Opening the faucet starts the unit", "Engineering and technology", "Control",
        "First run: the normally closed valve sits downstream of the flow sensor, so with the faucet open and the valve shut no "
        "water flows and the flow sensor can never wake the controller (failed). Fix: an outlet pressure sensor between valve and "
        "faucet; the drop in line pressure starts the LEDs, then the valve opens and the flow sensor must confirm flow",
        "Start-up sequence in LMF-CAL-001 D5; standby 0.23 W", WITHIN, "LMF-DEC-001 D-S3 (2026-10-25)")
c.claim("S38", "One failed LED of six trips the low-dose alarm", "Engineering and technology", "Sensing resolution",
        "The wall sensor sees the six LEDs about equally: S/S_ref = 5/6 against the alarm threshold, now set from the 275 nm "
        "weighted RED (40 / 47.3)", round(5 / 6, 3), round(CAL.thr, 3), "S/S_ref", closed_by="LMF-DEC-001 D-S4 (2026-10-25)")
c.cited("S39", "The SiC photodiode reads the UV-C, not the LEDs' longer-wavelength tail", "Physics", "Optics and radiation",
        "SiC (band gap about 3.26 eV) has little response above about 380 nm; AlGaN LEDs emit a weak parasitic band near 300 to "
        "400 nm that water hardly absorbs", "Check against the chosen LED's spectrum and the photodiode's response curve", PLAUSIBLE, "")

# ------------------------------------------------------------------ Mathematics (option A)
p_abs = F90["absorbed by water"]
avg_an = p_abs / (CAL.a90 * CAL.Q * 1e6) * 1e3
c.order_of_magnitude("S28", "Average dose of 75.4 mJ/cm2 at 90 %/cm and 1.2 L/min", "Mathematics", "Units and dimensional analysis",
                     claimed=round(CAL.AVG90, 1), estimate=avg_an, unit="mJ/cm2",
                     law="Volume-average dose = absorbed power / (alpha Q), independent of geometry (the ray trace counts only "
                         "the water between the ports, so it reads lower)", closed_by="LMF-CAL-001 B5")
with contextlib.redirect_stdout(io.StringIO()):
    E3, _, _ = CAL.trace(0.90, seed=3)
red3 = CAL.dose(E3, CAL.Q_LPM, "laminar")[3]
c.claim("S29", "Monte Carlo noise in the RED is under 3 %", "Mathematics", "Numerical method",
        "Second run of 600,000 photons with another seed", round(abs(red3 - CAL.RED90_l) / CAL.RED90_l * 100, 2), 3.0, "%",
        closed_by="This check")

# ------------------------------------------------------------------ Chemistry (option A)
c.cited("S30", "No mercury anywhere in the unit", "Chemistry", "Environmental and atmospheric chemistry",
        "AlGaN UV-C LEDs contain no mercury (Minamata Convention context in PRB)", "Bill of materials review: no lamp, no mercury",
        WITHIN, "BOM lines 1 to 19")
c.cited("S31", "Every wetted material is suitable for food contact: 316, PTFE and expanded PTFE, fused silica, EPDM O-rings "
        "out of the light, acetal; and the bought parts on the water path (flow sensor, valve, pressure sensor, tee, tube, "
        "restrictor) in food-contact, lead-free grades", "Chemistry", "Materials and polymer chemistry",
        "21 CFR 177.1550 (perfluorocarbon resins), 177.2470 (acetal copolymer), 177.2600 (rubber articles); "
        "NSF/ANSI 61 certification to assess for the chosen grades", "Reactor reviewed in the model; bought water-path parts to confirm at purchase (DEC To confirm); acetal is "
        "poorer in chloraminated water, which the well-water first user does not have", WITHIN, "PRS PR-011; REG G2, G3")
c.cited("S32", "No galvanic cell between the aluminium heat path and the 316 cap", "Chemistry", "Electrochemistry and batteries",
        "Aluminium and 316 touch only through the thermal pads on the dry side; the reactor's wetted metal is all 316, and the "
        "valve, flow sensor and pressure sensor are specified with plastic or stainless wetted parts (no brass)",
        "Design review of the joint stack", WITHIN, "BOM line 5")

# ------------------------------------------------------------------ Option B: hollow-fibre ultrafilter
Q_lh = CAL.Q_LPM * 60
A_m2 = 0.8
flux = Q_lh / A_m2
c.cited("B1", "A 0.8 m2 hollow-fibre cartridge passes 1.2 L/min at no more than 0.5 bar transmembrane pressure",
        "Physics", "Fluid mechanics", f"Darcy flow through the membrane: flux {flux:.0f} L/(m2 h) at 0.5 bar needs a clean-water "
        f"permeability of {flux/0.5:.0f} L/(m2 h bar); PVDF and PES UF membranes span roughly 100 to 500",
        "To confirm on a cartridge datasheet; a larger cartridge if not", PLAUSIBLE, "")
c.cited("B2", "Intact 0.01 to 0.02 um fibres remove bacteria (0.5 um and up) and protozoan cysts (3 um and up) by size",
        "Biology", "Microbiology", "Size exclusion; US EPA Membrane Filtration Guidance Manual (EPA 815-R-06-009) credits "
        "log removal of Cryptosporidium only with direct integrity testing", "Pore size 25 times smaller than the smallest bacteria",
        WITHIN, "")
c.cited("B3", "Viruses (20 to 100 nm) are only partly removed", "Biology", "Microbiology",
        "Virus sizes overlap the pore size; removal depends on the membrane grade", "Not credited in scoring", PLAUSIBLE, "")
bubble = 4 * 0.072 / 0.02e-6 / 1e6
c.claim("B4", "A 1 bar air pressure-decay test finds a broken fibre without forcing air through intact pores",
        "Physics", "Fluid mechanics", "Young-Laplace bubble point 4 gamma / d for a 0.02 um pore (ASTM D6908 practice)",
        0.1, round(bubble, 1), "MPa", closed_by="")
c.cited("B5", "The slim 10 in housing holds 8 bar", "Engineering and technology", "Standards practice",
        "Catalogue housings are commonly rated near 8.6 bar (125 psi); to confirm on the chosen housing", "Datasheet check", PLAUSIBLE, "")
c.cited("B6", "Treatment needs no power; fouling shows as a rising gap between the two gauges", "Physics", "Fluid mechanics",
        "Supply pressure drives the flow; TMP rises as the cake layer grows (Darcy)", "No calculation needed", WITHIN, "")

# ------------------------------------------------------------------ Option C: radial UV-C LED reactor
alpha = -math.log(0.90)
chord = math.pi / 4 * 2.0                      # cm, mean chord of a 20 mm circle
a1 = 1 - math.exp(-alpha * chord)
RT2 = 0.80 * 0.92 ** 2                         # aluminium reflector 0.80 at 275 nm, two quartz passes
f_abs = 0.8 * a1 / (1 - (1 - a1) * RT2)       # 0.8: share of LED light that reaches the tube
P_c = 12 * 0.060
avg_c = P_c * f_abs / (alpha * CAL.Q * 1e6) * 1e3
c.order_of_magnitude("C1", "Twelve LEDs give an average dose of about 100 mJ/cm2 at 90 %/cm and 1.2 L/min", "Physics",
                     "Optics and radiation", claimed=100.0, estimate=avg_c, unit="mJ/cm2",
                     law=f"Absorbed share {f_abs*100:.0f} % from single-pass absorption across the tube and a reflector "
                         "of 0.80; average dose = absorbed power / (alpha Q); RED to come from a ray trace")
c.cited("C2", "The RED of the radial reactor reaches 40 mJ/cm2", "Physics", "Optics and radiation",
        "Laminar flow in a 20 mm tube (Re about 1,270) gives a reactor efficiency near 0.5, so RED about half the average",
        "Ray trace needed before C could be chosen", PLAUSIBLE, "")
ro = P["c_tube_od"] / 2; t_q = (P["c_tube_od"] - P["c_tube_id"]) / 2
c.claim("C3", "The quartz flow tube holds 8 bar", "Physics", "Strength of materials",
        "Hoop stress p r / t against the 6.8 MPa design stress", round(0.8 * (ro - t_q / 2) / t_q, 1), 6.8, "MPa")
q_led = 12 * 0.35 * 6.2 - P_c
R_air = 1 / (7.0 * 0.064)
R_w = 0.76
dT_c = q_led / (1 / R_air + 1 / R_w)
c.claim("C4", "LED strips stay at or below 50 degC with flow, cooled by their fins and through the end fittings into the water",
        "Physics", "Heat transfer", f"{q_led:.1f} W through air ({R_air:.1f} K/W) and water ({R_w} K/W) paths in parallel "
        "from 25 degC water", round(25 + dT_c, 0), 50.0, "degC")
P_c_mains = (12 * 0.35 * 6.2 / 0.9 + 5.4) / 0.88
print(f"C5: twelve LEDs draw {P_c_mains:.0f} W from the mains while water flows (PR-009 limit 25 W; scored in LMF-OPT-001)")
c.cited("C5", "The seals at the tube ends stay out of UV-C guided along the quartz wall", "Chemistry",
        "Materials and polymer chemistry", "Light trapped in the quartz wall by total internal reflection reaches its ends; "
        "PTFE-encapsulated O-rings there", "By design in the option C model", WITHIN, "")
c.cited("C6", "The same flow switch, dose photodiode and valve logic as option A work across a thin radial column",
        "Engineering and technology", "Control", "The photodiode in the reflector gap sees direct LED light as well as light "
        "through the water, so its signal depends less on UVT than option A's; mapping to assess", "To assess if C is chosen",
        PLAUSIBLE, "")

state = c.write()
print("stem_check:", state)

# refresh Table 1 of docs/01b-stem-check.md (between the STM_TABLE markers) from the results
import csv, re
from pathlib import Path
doc = Path("docs/01b-stem-check.md")
if doc.exists():
    rows = list(csv.DictReader(open("docs/04-calcs/stem_results.csv")))
    cell = lambda r, k: (r[k] or "").replace("|", "/")
    lines = ["| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    lines += [f"| {r['id']} | {cell(r, 'claim')} | {r['field']} | {cell(r, 'branch')} | {cell(r, 'law')} | {cell(r, 'check')} | "
              f"{r['verdict']} | {cell(r, 'closed_by') or 'Open'} |" for r in rows]
    text = re.sub(r"<!-- STM_TABLE -->.*<!-- /STM_TABLE -->", lambda m: "<!-- STM_TABLE -->\n" + "\n".join(lines) + "\n<!-- /STM_TABLE -->",
                  doc.read_text(), flags=re.S)
    doc.write_text(text)
    print(f"refreshed Table 1 of {doc} ({len(rows)} rows)")
