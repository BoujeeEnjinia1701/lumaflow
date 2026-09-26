"""LumaFlow sizing calculations for LMF-CAL-001 v0.2 (TRL 3, design as revised by LMF-DDR-002).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md, each tagged [A1], [B2] ...
Geometry comes from cad/src/model.py (PARAMS, levels() and part volumes); prices from bom/bom.csv.

Sections: A flow and hydraulics, B optics and UV-C dose (Monte Carlo ray trace), C dose monitor,
D flow switching and run-on, E power and energy, F thermal, G pressure and structure,
H size, I cost, J options, K requirement status.
All values are first-principles estimates for a paper proof of concept.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, levels, build_parts, build  # noqa: E402

L = levels()
OUT = {}


def show(tag, text, value=None):
    """Print one tagged result line and keep the value for the requirement table."""
    print(f"[{tag}] {text}")
    if value is not None:
        OUT[tag] = value


def head(title):
    print(f"\n== {title} ==")


# ---------------------------------------------------------------- assumptions
Q_LPM = 1.2                       # design flow, L/min (R1), set by the restrictor (LMF-DDR-002)
T_WATER, T_AIR = 25.0, 30.0       # R10 thermal case, degC
RHO, MU20, MU5 = 998.0, 1.002e-3, 1.52e-3   # water density kg/m3, viscosity Pa s at 20 and 5 degC
CP_W = 4180.0                     # J/(kg K)
N_LED, I_LED, V_LED, PO_LED = P["led_n"], 0.350, 6.2, 0.060   # A, V, W optical per LED
ETA_DRV, P_VALVE, P_CTRL, ETA_AD = 0.90, 4.8, 0.6, 0.88
P_SENSE_SB, P_MCU_SB, P_AD_NL, ETA_AD_LIGHT = 0.075, 0.005, 0.10, 0.70
DRAWS, L_DAY, RUNON = 20, 15.0, 5.0
N_QUARTZ, N_WATER = 1.496, 1.372  # refractive indices near 275 nm
R_PTFE, R_STEEL, R_BOTTOM = 0.95, 0.30, 0.10   # wetted diffuse reflectances (assumed); 0.95 high-reflectance PTFE
D10 = 20.0                        # challenge organism, mJ/cm2 per log (MS2-like), taken as valid at 275 nm
NPHOT = 600_000
DOSE_T = 40.0                     # mJ/cm2, R2 and R3
UVT_DESIGN, UVT_TEST = 0.90, 0.70

# ---------------------------------------------------------------- A flow
head("A. Flow and hydraulics")
Q = Q_LPM / 60e3                              # m3/s
R_b = P["bore_d"] / 2e3                       # m
A_b = math.pi * R_b ** 2
U = Q / A_b
V_ch = A_b * L["channel_len"] / 1e3
V_fl = A_b * L["flow_len"] / 1e3
show("A1", f"Channel {P['bore_d']:.0f} mm bore x {L['channel_len']:.0f} mm (window to top disc); inlet to outlet {L['flow_len']:.0f} mm")
show("A2", f"Water in channel {V_ch*1e6:.0f} mL; between the ports {V_fl*1e6:.0f} mL")
show("A3", f"Mean velocity {U*100:.2f} cm/s; mean residence time between ports {V_fl/Q:.2f} s at {Q_LPM} L/min")
Re20, Re5 = RHO * U * 2 * R_b / MU20, RHO * U * 2 * R_b / MU5
show("A4", f"Reynolds number {Re20:.0f} at 20 degC, {Re5:.0f} at 5 degC (laminar)")
Le = 0.05 * Re20 * 2 * R_b
show("A5", f"Laminar entrance length about {Le*1e3:.0f} mm, longer than the {L['flow_len']:.0f} mm flow path, "
     "so the profile lies between plug flow and a parabola")

# ---------------------------------------------------------------- B optics
head("B. Optics and UV-C dose (Monte Carlo)")


def fresnel_T(cos_i, n1, n2):
    """Unpolarized Fresnel transmittance and the refracted cosine."""
    sin_i = np.sqrt(np.clip(1 - cos_i ** 2, 0, 1))
    sin_t = n1 / n2 * sin_i
    tir = sin_t >= 1
    cos_t = np.sqrt(np.clip(1 - sin_t ** 2, 0, 1))
    rs = ((n1 * cos_i - n2 * cos_t) / (n1 * cos_i + n2 * cos_t)) ** 2
    rp = ((n1 * cos_t - n2 * cos_i) / (n1 * cos_t + n2 * cos_i)) ** 2
    T = 1 - 0.5 * (rs + rp)
    T[tir] = 0
    return T, cos_t


def lambert(n, rng, normal):
    """Cosine-weighted directions about unit normals (N,3)."""
    u1, u2 = rng.random(n), rng.random(n)
    ct, phi = np.sqrt(u1), 2 * np.pi * u2
    st = np.sqrt(1 - ct ** 2)
    a = np.where(np.abs(normal[:, 0:1]) < 0.9, [[1.0, 0, 0]], [[0, 1.0, 0]])
    t1 = np.cross(normal, a); t1 /= np.linalg.norm(t1, axis=1)[:, None]
    t2 = np.cross(normal, t1)
    return t1 * (st * np.cos(phi))[:, None] + t2 * (st * np.sin(phi))[:, None] + normal * ct[:, None]


NR, NZ = 20, 60
R_cm, L_cm = P["bore_d"] / 20, L["channel_len"] / 10
r_edges = R_cm * np.sqrt(np.linspace(0, 1, NR + 1))          # equal-area annuli
z_edges = np.linspace(0, L_cm, NZ + 1)
r_mid = np.sqrt((r_edges[:-1] ** 2 + r_edges[1:] ** 2) / 2)
z_mid = (z_edges[:-1] + z_edges[1:]) / 2
V_bin = np.pi * np.diff(r_edges ** 2)[:, None] * np.diff(z_edges)[None, :]


def trace(uvt, r_ptfe=R_PTFE, n=NPHOT, seed=1):
    """Trace LED photons into the water column. Returns fluence rate E (W/cm2) per (r, z) bin
    for the full LED output, and the power fractions of each fate."""
    rng = np.random.default_rng(seed)
    alpha = -math.log(uvt)                                       # base-e absorption coefficient, 1/cm
    p_ph = N_LED * PO_LED / n
    # emission: Lambertian from six LED points on a ring, below the window
    k = rng.integers(0, N_LED, n)
    ang = 2 * np.pi * k / N_LED
    z_led = -(P["win_t"] + P["led_gap"]) / 10
    pos = np.stack([P["led_pcr"] / 10 * np.cos(ang), P["led_pcr"] / 10 * np.sin(ang), np.full(n, z_led)], 1)
    d = lambert(n, rng, np.tile([0, 0, 1.0], (n, 1)))
    # air gap to the window underside; the seat shoulder blocks r > aperture
    z_w0 = -P["win_t"] / 10
    pos = pos + d * ((z_w0 - pos[:, 2]) / d[:, 2])[:, None]
    ok = np.hypot(pos[:, 0], pos[:, 1]) < P["aperture_d"] / 20
    T1, ct = fresnel_T(d[:, 2], 1.0, N_QUARTZ)
    s = 1.0 / N_QUARTZ
    d = np.column_stack([d[:, 0] * s, d[:, 1] * s, ct])
    pos = pos + d * ((0 - pos[:, 2]) / d[:, 2])[:, None]
    ok &= np.hypot(pos[:, 0], pos[:, 1]) < R_cm                  # only the bore is wetted
    T2, ct = fresnel_T(d[:, 2], N_QUARTZ, N_WATER)
    s = N_QUARTZ / N_WATER
    d = np.column_stack([d[:, 0] * s, d[:, 1] * s, ct])
    w = np.where(ok, T1 * T2 * 0.995, 0.0)                       # 0.995: quartz bulk transmittance
    fate = {"enters water": w.sum() * p_ph}
    pos[:, 2] = 1e-6
    absorbed = np.zeros((NR, NZ))
    lost_wall = lost_top = lost_bottom = to_det = 0.0
    det_r = P["det_win_d"] / 20                                  # wall sensor window, taken as a square patch
    det_z = (L["z_det"] - L["z_win1"]) / 10
    steel_z = L["steel_len"] / 10
    alive = w > 0
    for _ in range(200):
        idx = np.nonzero(alive)[0]
        if idx.size == 0:
            break
        p, dd, ww = pos[idx], d[idx], w[idx]
        a = dd[:, 0] ** 2 + dd[:, 1] ** 2
        b = 2 * (p[:, 0] * dd[:, 0] + p[:, 1] * dd[:, 1])
        c = p[:, 0] ** 2 + p[:, 1] ** 2 - R_cm ** 2
        with np.errstate(divide="ignore", invalid="ignore"):
            t_wall = np.where(a > 1e-12, (-b + np.sqrt(np.maximum(b * b - 4 * a * c, 0))) / (2 * a), np.inf)
            t_z = np.where(dd[:, 2] > 0, (L_cm - p[:, 2]) / dd[:, 2],
                           np.where(dd[:, 2] < 0, -p[:, 2] / dd[:, 2], np.inf))
        s_free = -np.log(rng.random(idx.size)) / alpha
        t_hit = np.minimum(t_wall, t_z)
        absb = s_free < t_hit
        q = p[absb] + dd[absb] * s_free[absb][:, None]
        ri = np.clip(np.searchsorted(r_edges, np.hypot(q[:, 0], q[:, 1])) - 1, 0, NR - 1)
        zi = np.clip(np.searchsorted(z_edges, q[:, 2]) - 1, 0, NZ - 1)
        np.add.at(absorbed, (ri, zi), ww[absb] * p_ph)
        alive[idx[absb]] = False
        mv = ~absb
        ii, p2, d2, w2 = idx[mv], p[mv] + dd[mv] * t_hit[mv][:, None], dd[mv], ww[mv]
        wall = t_wall[mv] <= t_z[mv]
        top = ~wall & (d2[:, 2] > 0)
        bot = ~wall & ~top
        u = rng.random(ii.size)
        # wall: stainless in the lower cap, PTFE above
        refl = np.where(p2[:, 2] < steel_z, R_STEEL, r_ptfe)
        det = wall & (np.abs(p2[:, 2] - det_z) < det_r) & (np.abs(p2[:, 1]) < det_r) & (p2[:, 0] > 0)
        to_det += w2[det].sum() * p_ph
        R_here = np.where(wall, refl, np.where(top, r_ptfe, R_BOTTOM))
        R_here = np.where(det, 0.0, R_here)
        keep = u < R_here
        lost = ~keep & ~det
        lost_wall += w2[lost & wall].sum() * p_ph
        lost_top += w2[lost & top].sum() * p_ph
        lost_bottom += w2[lost & bot].sum() * p_ph
        alive[ii[~keep]] = False
        kk = ii[keep]
        normal = np.zeros((kk.size, 3))
        wk, tk = wall[keep], top[keep]
        pk = p2[keep]
        normal[wk, 0] = -pk[wk, 0] / R_cm; normal[wk, 1] = -pk[wk, 1] / R_cm
        normal[~wk & tk, 2] = -1.0
        normal[~wk & ~tk, 2] = 1.0
        d[kk] = lambert(kk.size, rng, normal)
        pos[kk] = pk + normal * 1e-7
    fate.update({"absorbed by water": absorbed.sum(), "lost at walls": lost_wall, "lost at top disc": lost_top,
                 "lost at bottom": lost_bottom, "to detector window": to_det})
    E = absorbed / (alpha * V_bin)                               # fluence rate, W/cm2
    return E, fate, alpha


zi_in = np.searchsorted(z_mid, (L["z_in"] - L["z_win1"]) / 10)
zi_out = np.searchsorted(z_mid, (L["z_out"] - L["z_win1"]) / 10)
dz = z_edges[1] - z_edges[0]
w_area = np.diff(r_edges ** 2) / R_cm ** 2                     # equal-area weights


def dose(E, q_lpm, profile, n_led=N_LED):
    """Dose per streamline (mJ/cm2), flow weights, average dose and RED for the D10 organism."""
    Ucm = q_lpm * 1000 / 60 / (math.pi * R_cm ** 2)
    u = np.full(NR, Ucm) if profile == "plug" else 2 * Ucm * (1 - (r_mid / R_cm) ** 2)
    Dr = 1000 * E[:, zi_in:zi_out].sum(1) * dz / u * n_led / N_LED
    wq = w_area * u / (w_area * u).sum()
    kk = math.log(10) / D10
    red = -math.log((wq * np.exp(-kk * Dr)).sum()) / kk
    return Dr, wq, (wq * Dr).sum(), red


CASES = [0.95, 0.90, 0.85, 0.80, 0.75, 0.70]
runs = {uvt: trace(uvt) for uvt in CASES}
E90, F90, a90 = runs[0.90]
Ptot = N_LED * PO_LED
show("B1", f"LED output {N_LED} x {PO_LED*1e3:.0f} mW = {Ptot:.2f} W UV-C at {I_LED*1e3:.0f} mA, "
     f"{N_LED*I_LED*V_LED:.2f} W electrical (UV-C efficiency {Ptot/(N_LED*I_LED*V_LED)*100:.1f} %)")
show("B2", f"Enters the water through the window: {F90['enters water']/Ptot*100:.1f} % of LED output "
     "(seat shoulder, bore edge and Fresnel losses)")
for uvt in (0.90, 0.70):
    E, F, a = runs[uvt]
    tag = "B3" if uvt == 0.90 else "B4"
    show(tag, f"UVT {uvt*100:.0f} %/cm (alpha {a:.3f}/cm): absorbed by water {F['absorbed by water']/Ptot*100:.1f} %, "
         f"walls {F['lost at walls']/Ptot*100:.1f} %, top {F['lost at top disc']/Ptot*100:.1f} %, "
         f"bottom {F['lost at bottom']/Ptot*100:.1f} %, detector {F['to detector window']/Ptot*100:.3f} % of LED output")
res = {}
for uvt in CASES:
    E = runs[uvt][0]
    res[uvt] = {pr: dose(E, Q_LPM, pr) for pr in ("plug", "laminar")}
print(f"  Table: dose at {Q_LPM} L/min by UVT (mJ/cm2). avg = flow-weighted average dose; RED for D10 = 20 mJ/cm2")
print("  UVT    avg(plug)  RED(plug)  avg(lam)  RED(lam)  eff(lam)")
for uvt in CASES:
    (_, _, ap, rp), (_, _, al, rl) = res[uvt]["plug"], res[uvt]["laminar"]
    print(f"  {uvt*100:3.0f} %   {ap:8.1f}  {rp:9.1f}  {al:8.1f}  {rl:8.1f}  {rl/al:8.2f}")
RED90_p, RED90_l = res[0.90]["plug"][3], res[0.90]["laminar"][3]
RED70_p, RED70_l = res[0.70]["plug"][3], res[0.70]["laminar"][3]
AVG90 = res[0.90]["laminar"][2]
show("B5", f"90 %/cm, {Q_LPM} L/min: average dose {AVG90:.1f} mJ/cm2; RED {RED90_l:.1f} (laminar) to {RED90_p:.1f} (plug) mJ/cm2; "
     f"reactor efficiency {RED90_l/AVG90:.2f} laminar", RED90_l)
show("B6", f"70 %/cm, {Q_LPM} L/min: average dose {res[0.70]['laminar'][2]:.1f} mJ/cm2; RED {RED70_l:.1f} (laminar) to {RED70_p:.1f} (plug) mJ/cm2", RED70_l)
Dr_l = res[0.90]["laminar"][0]
show("B7", f"Laminar streamline doses at 90 %/cm: {Dr_l[0]:.0f} mJ/cm2 on the axis, {Dr_l[NR//2]:.0f} at mid radius, "
     f"{Dr_l[-1]:.0f} next to the wall")
sens = {}
for rp_ in (0.80, 0.90):
    E, _, _ = trace(0.90, r_ptfe=rp_, seed=2)
    sens[rp_] = dose(E, Q_LPM, "laminar")[3]
show("B8", f"Sensitivity to wetted liner reflectance at 90 %/cm (laminar RED): {sens[0.80]:.1f} at 0.80 (plain PTFE), "
     f"{sens[0.90]:.1f} at 0.90, {RED90_l:.1f} at 0.95 mJ/cm2", sens[0.80])
show("B9", f"LED output 20 % low (aging, bin, temperature): laminar RED {RED90_l*0.8:.1f} mJ/cm2 at 90 %/cm")

# ---------------------------------------------------------------- C dose monitor
head("C. Dose monitor (wall sensor at mid height)")
RESP, A_PD, T_SWIN = 0.13, 0.06e-2, 0.92     # A/W, active area cm2 (0.06 mm2), sensor window transmittance
det_area = (P["det_win_d"] / 10) ** 2        # square patch used in the ray trace, cm2
S = {uvt: runs[uvt][1]["to detector window"] / det_area for uvt in CASES}   # W/cm2 on the wall window
cur = {uvt: S[uvt] * A_PD * T_SWIN * RESP for uvt in CASES}
print("  UVT    irradiance at wall window (mW/cm2)  photocurrent (nA)  signal / signal at 90 %   RED lam / RED lam at 90 %")
for uvt in CASES:
    print(f"  {uvt*100:3.0f} %   {S[uvt]*1e3:12.3f}                      {cur[uvt]*1e9:10.2f}        {S[uvt]/S[0.90]:8.4f}"
          f"              {res[uvt]['laminar'][3]/RED90_l:6.3f}")
show("C1", f"Wall sensor at Z {L['z_det']:.0f} mm: {S[0.90]*1e3:.2f} mW/cm2 and {cur[0.90]*1e9:.1f} nA at 90 %/cm, "
     f"{cur[0.80]*1e9:.1f} nA at 80 %/cm, {cur[0.70]*1e9:.2f} nA at 70 %/cm (SiC, {RESP} A/W, 0.06 mm2)", cur[0.90])
g = math.log(S[0.85] / S[0.90]) / math.log(res[0.85]["laminar"][3] / RED90_l)
show("C2", f"Between 90 and 85 %/cm the wall signal falls {g:.1f} times as fast (in log terms) as the RED")
thr = DOSE_T / RED90_l
show("C3", f"Proportional mapping RED_est = RED_ref x (S/S_ref) x (Q_ref/Q) is always conservative; with RED_ref "
     f"{RED90_l:.1f} mJ/cm2 the alarm threshold is S/S_ref = {thr:.2f}", thr)
uvts = np.array(CASES[::-1]); sig = np.array([S[u] for u in uvts]); reds = np.array([res[u]["laminar"][3] for u in uvts])
u_trip = float(np.interp(math.log(thr * S[0.90]), np.log(sig), uvts))
show("C4", f"With LEDs at rated output the alarm trips below about {u_trip*100:.1f} %/cm UVT; LEDs aged to "
     f"{thr*100:.0f} % of output trip it in 90 %/cm water, where the true RED is {thr*RED90_l:.1f} mJ/cm2 (safe)", u_trip)
S_age = 0.7 * S[0.90]
uvt_claim = float(np.interp(math.log(S_age), np.log(sig), uvts))
red_claim = float(np.interp(uvt_claim, uvts, reds))
show("C5", f"Aged LEDs at 70 % output in 90 %/cm water: true RED {0.7*RED90_l:.1f}; a mapping that blames UVT would read "
     f"UVT {uvt_claim*100:.1f} %/cm and claim RED {red_claim:.1f}; the proportional mapping reads {0.7*RED90_l:.1f}")

# ---------------------------------------------------------------- D flow switching and run-on
head("D. Flow switching and run-on")
K_HZ = 15.0                                  # Hz per L/min, higher pulse-rate sensor (LMF-DDR-002)
show("D1", f"Sensor pulses at 0.3 L/min: {K_HZ*0.3:.2f} Hz, one pulse every {1/(K_HZ*0.3):.2f} s; at {Q_LPM} L/min {K_HZ*Q_LPM:.1f} Hz", 1 / (K_HZ * 0.3))
t_on = 1 / (K_HZ * 0.3) + 0.02
show("D2", f"Worst-case detection plus LED rise at 0.3 L/min: {t_on:.2f} s against 0.5 s", t_on)
# stagnant parcel doses (plug flow): prior pass + 5 s run-on + remainder after restart with a 0.5 s dark delay
Ucm = Q_LPM * 1000 / 60 / (math.pi * R_cm ** 2)
E = E90
cum = np.cumsum(E[:, zi_in:zi_out], 1) * dz
tot = cum[:, -1:]
shift = int(round(Ucm * 0.5 / dz))
rest = np.zeros_like(cum)
rest[:, :-shift - 1] = tot - cum[:, shift:-1] if shift else tot - cum[:, :-1]
d_stag = 1000 * (cum / Ucm + E[:, zi_in:zi_out] * RUNON + rest / Ucm)
d_first = 1000 * (cum / Ucm + E[:, zi_in:zi_out] * RUNON)     # parcel pushed out on restart before the LEDs see it again
show("D3", f"Stagnant 5 s run-on at 90 %/cm: every parcel in the flow path receives at least {d_first.min():.0f} mJ/cm2 "
     f"before and during run-on (plug flow)", d_first.min())
show("D4", f"Volume-average run-on dose for the water held in the channel: "
     f"{runs[0.90][1]['absorbed by water']*RUNON/(a90*V_ch*1e6)*1e3:.0f} mJ/cm2 at 90 %/cm")

# ---------------------------------------------------------------- E power
head("E. Power and energy")
P_led = N_LED * I_LED * V_LED
P_dc = P_led / ETA_DRV + P_VALVE + P_CTRL
P_ac = P_dc / ETA_AD
P_sb = (P_SENSE_SB + P_MCU_SB) / ETA_AD_LIGHT + P_AD_NL
show("E1", f"LED {P_led:.2f} W; 24 V bus {P_dc:.2f} W (driver 90 %, valve {P_VALVE} W, controller {P_CTRL} W); "
     f"from mains {P_ac:.1f} W", P_ac)
show("E2", f"Standby from mains {P_sb:.2f} W (flow sensor {P_SENSE_SB*1e3:.0f} mW, MCU sleep, adapter no-load {P_AD_NL} W)", P_sb)
t_day = L_DAY / Q_LPM * 60 + DRAWS * RUNON
e_day = P_ac * t_day / 3600 + P_sb * (24 - t_day / 3600)
show("E3", f"On-time {t_day/60:.1f} min/day ({t_day/3600*365:.0f} h/year); energy {e_day:.1f} Wh/day, {e_day*365/1000:.1f} kWh/year")
show("E4", f"Years to 10,000 h of LED on-time at this use: {10000/(t_day/3600*365):.0f}")
show("E5", f"For comparison, a tap-scale mercury unit drawing 13 to 22 W all day (VIQUA VT1, VT4, S2Q-PA): "
     f"{13*8.76:.0f} to {22*8.76:.0f} kWh/year")

# ---------------------------------------------------------------- F thermal
head("F. Thermal (R10)")
parts = {k: s for k, _, s, *_ in build_parts()}
v_sink = parts["sink"].volume * 1e-9          # m3, sink plus spreader ring
v_cap = parts["cap_lo"].volume * 1e-9
Q_h = P_led - Ptot
C = v_sink * 2700 * 900 + v_cap * 7990 * 500 + 0.02 * 900     # J/K, sink, stainless cap, board
hw = P["sink_w"] / 1e3
A_conv = (P["n_fins"] * 2 * P["fin_h"] * P["sink_w"] + P["n_fins"] * P["fin_t"] * P["sink_w"]
          + (P["sink_w"] - P["n_fins"] * P["fin_t"]) * P["sink_w"] + 4 * P["sink_w"] * (P["fin_h"] + P["sink_base"])) * 1e-6
A_env = hw * hw + 4 * hw * (P["fin_h"] + P["sink_base"]) / 1e3
H_NC, EPS = 5.0, 0.85
T_m = 273.15 + 45
h_r = 4 * 5.67e-8 * EPS * T_m ** 3
R_air = 1 / (H_NC * A_conv + h_r * A_env)
A_ring = math.pi * ((P["cap_d"] / 2e3) ** 2 - (P["board_d"] / 2e3 + 0.0005) ** 2)
R_pad = 0.0005 / 3.0                                # 0.5 mm pad, 3 W/(m K), per m2
R_ring = 2 * R_pad / A_ring
h_cap = L["steel_len"] / 1e3
R_cap = math.log((P["cap_d"] / 2) / (P["bore_d"] / 2)) / (2 * math.pi * 16 * h_cap) + 0.010 / (16 * A_ring)
A_wet = math.pi * P["bore_d"] / 1e3 * h_cap + math.pi * P["port_bore"] / 1e3 * (P["cap_d"] / 2 - P["bore_d"] / 2) / 1e3
R_bs = R_pad / (math.pi * (P["board_d"] / 2e3) ** 2)
R_JB, P_EACH = 10.0, (P_led - Ptot) / N_LED


def board_T(h_w):
    R_w = R_ring + R_cap + 1 / (h_w * A_wet)
    Ts = (T_AIR / R_air + T_WATER / R_w + Q_h) / (1 / R_air + 1 / R_w)
    return Ts + Q_h * R_bs, R_w, Ts


show("F1", f"LED heat {Q_h:.2f} W; sink to air {R_air:.2f} K/W (h {H_NC} W/(m2 K) on {A_conv*1e4:.0f} cm2 plus radiation); "
     f"heat capacity {C:.0f} J/K")
res_T = {}
for h_w in (150, 300, 600):
    Tb, R_w, Ts = board_T(h_w)
    res_T[h_w] = (Tb, R_w, Ts)
Tb, R_w, Ts = res_T[300]
q_water = (Ts - T_WATER) / R_w
show("F2", f"Water path (spreader, 316 cap, film at 300 W/(m2 K) on {A_wet*1e4:.1f} cm2): {R_w:.2f} K/W; "
     f"{q_water:.1f} W of {Q_h:.1f} W goes to the water, which warms {q_water/(Q*RHO*CP_W):.2f} K")
show("F3", f"Steady LED board with continuous flow: {res_T[150][0]:.1f} / {Tb:.1f} / {res_T[600][0]:.1f} degC "
     "at film coefficients 150 / 300 / 600 W/(m2 K) (target 50)", res_T[150][0])
show("F4", f"LED junctions about {Tb + P_EACH*R_JB:.0f} degC at 300 W/(m2 K) (10 K/W, {P_EACH:.2f} W each)")
Tb_air = T_AIR + Q_h * (R_air + R_bs)
tau_air = C * R_air
t50 = -tau_air * math.log(1 - (50 - T_AIR) / (Tb_air - T_AIR))
show("F5", f"Acetal lower cap instead (no water path): steady board {Tb_air:.0f} degC; 50 degC after {t50/60:.1f} min of flow")
R_nf = R_ring + R_cap + 1 / (50 * A_wet)                     # still water in the cap
Ts_nf = (T_AIR / R_air + T_WATER / R_nf + Q_h) / (1 / R_air + 1 / R_nf)
tau_nf = C / (1 / R_air + 1 / R_nf)
t85 = -tau_nf * math.log(1 - (85 - 20 - T_AIR) / (Ts_nf - T_AIR)) if Ts_nf - T_AIR > 35 else float("inf")
t65 = f"reaching 65 degC board after {t85/60:.1f} min" if math.isfinite(t85) else "never reaching 65 degC"
show("F6", f"Fault, LEDs stuck on with no flow: board heads for {Ts_nf + Q_h*R_bs:.0f} degC (junction +{P_EACH*R_JB:.0f} K), "
     f"{t65}; run-on of 5 s adds {Q_h*RUNON/C:.2f} K", Ts_nf + Q_h * R_bs)

# ---------------------------------------------------------------- G pressure and structure
head("G. Pressure drop (R8), window and structure (R7)")
KV_SENS, KV_VALVE, K_FIT = 0.35, 0.25, 6.0
q_m3h = Q_LPM * 60 / 1000
dp_s, dp_v = (q_m3h / KV_SENS) ** 2, (q_m3h / KV_VALVE) ** 2
d_t = 6.35e-3
v_t = Q / (math.pi * d_t ** 2 / 4)
Re_t = RHO * v_t * d_t / MU20
f_t = 0.316 / Re_t ** 0.25
dp_tube = f_t * 1.0 / d_t * RHO * v_t ** 2 / 2 / 1e5
dp_fit = K_FIT * RHO * v_t ** 2 / 2 / 1e5
v_p = Q / (math.pi * (P["port_bore"] / 2e3) ** 2)
dp_ports = 1.5 * RHO * v_p ** 2 / 2 / 1e5
dp_reac = 32 * MU20 * L["flow_len"] / 1e3 * U / (2 * R_b) ** 2 / 1e5
dp = dp_s + dp_v + dp_tube + dp_fit + dp_ports + dp_reac
show("G1", f"Flow sensor {dp_s:.2f} (Kv {KV_SENS}), valve {dp_v:.2f} (Kv {KV_VALVE}), 1 m of 1/4 in bore tube {dp_tube:.3f}, "
     f"fittings {dp_fit:.3f}, ports {dp_ports:.3f}, reactor {dp_reac:.5f} bar")
show("G2", f"Total at {Q_LPM} L/min, excluding the flow restrictor: {dp:.2f} bar ({dp*14.5:.1f} psi) against 0.5 bar", dp)
dp_lo = (q_m3h / 0.5) ** 2 + (q_m3h / 0.4) ** 2 + dp_tube + dp_fit + dp_ports
show("G3", f"With Kv 0.5 sensor and Kv 0.4 valve: {dp_lo:.2f} bar; at 2 bar supply {2-dp:.2f} bar is left for the restrictor and faucet")
p = 0.8
a_w = P["aperture_d"] / 2
sig = lambda t, pr=p: 3 * (3 + 0.17) / 8 * pr * a_w ** 2 / t ** 2
show("G4", f"Window {P['win_d']:.0f} x {P['win_t']:.0f} mm on a {P['aperture_d']:.0f} mm seat, simply supported: "
     f"{sig(P['win_t']):.2f} MPa at 8 bar (3 mm: {sig(3):.1f} MPa); allowable 6.8 MPa", sig(P["win_t"]))
P_LIM = 0.4                                  # MPa, upstream pressure-limiting valve setting (installation requirement)
show("G5", f"Unprotected 16 bar water-hammer spike: {sig(P['win_t'], 1.6):.1f} MPa (over 6.8). With the limiter at "
     f"{P_LIM*10:.0f} bar: {sig(P['win_t'], P_LIM):.2f} MPa static; a transient doubling to {2*P_LIM*10:.0f} bar gives "
     f"{sig(P['win_t'], 2*P_LIM):.2f} MPa", sig(P["win_t"], 2 * P_LIM))
sig_det = 3 * 3.17 / 8 * p * (P["det_win_d"] / 2) ** 2 / 3.0 ** 2
show("G6", f"Sensor window {P['det_win_d']:.0f} mm x 3 mm: {sig_det:.2f} MPa; tube hoop stress "
     f"{p*(P['tube_od']/2-1.5)/3:.1f} MPa (316, 3 mm wall)")
F_end = p * math.pi * (P["tube_od"] / 2) ** 2
A_S = {4.0: 8.78, 5.0: 14.2, 6.0: 20.1}[P["rod_d"]]
show("G7", f"End load on each cap {F_end:.0f} N (seal at the tube OD); per M{P['rod_d']:.0f} rod {F_end/P['n_rod']:.0f} N, "
     f"{F_end/P['n_rod']/A_S:.0f} MPa in the {A_S} mm2 stress area")

# ---------------------------------------------------------------- H size
head("H. Size (R14)")
bb = build(include_adapter=False).bounding_box()
show("H1", f"Unit without the adapter {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm against 350 x 150 x 350 mm",
     (bb.size.X, bb.size.Y, bb.size.Z))

# ---------------------------------------------------------------- I cost
head("I. Cost (R16)")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
top = sorted(rows, key=lambda r: -float(r["qty"]) * float(r["unit_cost_usd"]))[:3]
show("I1", f"BOM {len(rows)} lines, total ${total:.2f} against budget_usd ${budget:.0f} "
     f"({'under' if total <= budget else 'over'} by ${abs(budget-total):.2f})", total)
show("I2", "Largest lines: " + "; ".join(f"{r['item']} ${float(r['qty'])*float(r['unit_cost_usd']):.0f}" for r in top))

# ---------------------------------------------------------------- J options
head("J. Flow limits and options")
qs = np.linspace(0.2, 3.0, 141)
q90 = np.array([dose(E90, q, "laminar")[3] for q in qs])
Q_R2 = float(qs[q90 >= DOSE_T].max())
Q_met = float(qs[q90 >= 1.2 * DOSE_T].max())
show("J1", f"Six LEDs, this reactor, 90 %/cm (laminar RED): 40 mJ/cm2 up to {Q_R2:.2f} L/min; "
     f"48 mJ/cm2 (the 20 % margin for Met) up to {Q_met:.2f} L/min", Q_R2)
red2 = dose(E90, 2.0, "laminar")[3]; red2p = dose(E90, 2.0, "plug")[3]
show("J2", f"At the former 2.0 L/min: RED {red2:.1f} (laminar) to {red2p:.1f} (plug) mJ/cm2 at 90 %/cm")
n_b = math.ceil(N_LED * DOSE_T / RED70_l)
show("J3", f"Option B (R3): LEDs for 40 mJ/cm2 at 70 %/cm and {Q_LPM} L/min (laminar): {n_b}; LED power {n_b*I_LED*V_LED:.0f} W")
reds70 = np.array([dose(runs[0.70][0], q, "laminar")[3] for q in qs])
q_c = float(qs[reds70 >= DOSE_T].max()) if (reds70 >= DOSE_T).any() else float("nan")
show("J4", f"Option C (R3): flow at which six LEDs give 40 mJ/cm2 at 70 %/cm (laminar): {q_c:.2f} L/min")

# ---------------------------------------------------------------- K requirement status
head("K. Requirement status")
dims = OUT["H1"]
status = [
    ("R1", f"{Q_LPM} L/min, restrictor", f"{Q_LPM} L/min restrictor; sensor range 0.3 to 6 L/min", "Met"),
    ("R2", f"RED >= 40 at 90 %/cm, {Q_LPM} L/min", f"{RED90_l:.1f} (laminar) to {RED90_p:.1f} (plug) mJ/cm2",
     "Met" if RED90_l >= DOSE_T * 1.2 else ("At risk" if RED90_p >= DOSE_T else "Not met")),
    ("R3", "RED >= 40 at 70 %/cm", f"{RED70_l:.1f} to {RED70_p:.1f} mJ/cm2", "Met" if RED70_l >= DOSE_T else "Not met"),
    ("R4", "Dose monitor, fail closed in 1 s", f"wall signal {cur[0.90]*1e9:.1f} nA at 90 %/cm, {cur[0.70]*1e9:.2f} nA at 70 %/cm; "
     f"alarm below about {u_trip*100:.0f} %/cm; mapping and fail-safe need firmware and test",
     "Met" if RED90_l >= DOSE_T and cur[0.70] > 1e-9 else "At risk"),
    ("R5", "LEDs on in 0.5 s above 0.3 L/min; 5 s run-on", f"{t_on:.2f} s worst case", "At risk" if t_on > 0.4 else "Met"),
    ("R6", "No mercury; full output in 0.1 s", "LEDs, microsecond rise", "Met"),
    ("R7", "Window <= 6.8 MPa at 8 bar", f"{OUT['G4']:.2f} MPa", "Met" if OUT["G4"] <= 6.8 else "Not met"),
    ("R8", f"<= 0.5 bar at {Q_LPM} L/min, excluding the restrictor", f"{dp:.2f} bar on assumed Kv",
     "Met" if dp <= 0.35 else ("At risk" if dp <= 0.5 else "Not met")),
    ("R9", "<= 25 W flowing, <= 0.5 W standby", f"{P_ac:.1f} W, {P_sb:.2f} W", "Met" if P_ac <= 25 and P_sb <= 0.5 else "Not met"),
    ("R10", "Board <= 50 degC; cut-back above 50 degC", f"{res_T[600][0]:.0f} to {res_T[150][0]:.0f} degC steady",
     "Met" if res_T[150][0] <= 50 else ("At risk" if Tb <= 50 else "Not met")),
    ("R11", "Food-contact wetted parts; no UV-C on plastics but PTFE", "316 lower cap; PTFE shields acetal", "Met"),
    ("R12", "No UV-C outside; interlocks", "Metal and PTFE light path; interlock by design", "Met"),
    ("R13", "24 V DC only at the unit", "Certified adapter, fuse", "Met"),
    ("R14", "<= 350 x 150 x 350 mm", f"{dims[0]:.0f} x {dims[1]:.0f} x {dims[2]:.0f} mm", "Met"),
    ("R15", "Service in 15 min", "Needs a build to time", "Not verifiable at TRL 3"),
    ("R16", f"<= ${budget:.0f}", f"${total:.0f}", "Met" if total <= budget else "Not met"),
    ("R17", "Pressure limiter <= 4 bar upstream (installation)", f"window {OUT['G5']:.2f} MPa at twice the setting",
     "Met" if OUT["G5"] <= 6.8 else "Not met"),
]
for rid, tgt, val, st in status:
    print(f"  {rid:4s} {st:24s} {val}  (target: {tgt})")
counts = {}
for *_, st in status:
    counts[st] = counts.get(st, 0) + 1
show("K1", "Counts: " + ", ".join(f"{v} {k.lower()}" for k, v in counts.items()))
