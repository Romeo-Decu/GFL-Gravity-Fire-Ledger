"""A3. CRAM-1: thermal-regime theory for opposed-flow spread over a thin fuel.

    V_f = C * k_g * (T_f - T_v) / (rho_s * c_s * tau * (T_v - T_inf)),  tau = fuel semi-thickness

C = sqrt(2) (de Ris 1969), pi/4 (Delichatsios exact thin solution), 1 (extended simplified theory, EST).
In the thermal regime the rate does not depend on the flow speed or on the reaction rate and scales as 1/tau.
The absolute value depends strongly on property choices (Bhattacharjee et al. 2016): GFL reports the band over the
three constants and over the published range of F = (T_f - T_v)/(T_v - T_inf), 4.4 to 5.5 (Carmignani et al.).
F = 4.76 is fitted to thin-fuel data, so it is never used here as a prediction.

Thin-thick check: the fuel is thermally thin when its semi-thickness is small compared with the solid heating depth
delta_s = alpha_s / V_f (Carmignani et al.; de Ris). Reported as the ratio tau / delta_s.
"""
from __future__ import annotations

import math

from .sources import CARMIGNANI, PMMA, T_AMBIENT_K

CONSTANTS = {"de_Ris_sqrt2": math.sqrt(2), "Delichatsios_pi_over_4": math.pi / 4, "EST_1": 1.0}
F_RANGE = (4.4, 5.5)


def v(props: dict, tau_m: float, C: float, F: float) -> float:
    return C * props["k_g_W_mK"][0] * F / (props["rho_s_kg_m3"][0] * props["c_s_J_kgK"][0] * tau_m)


def predict(thickness_um: float, props: dict = PMMA) -> dict:
    tau = thickness_um * 1e-6 / 2
    F_props = (props["T_f_K"][0] - props["T_v_K"][0]) / (props["T_v_K"][0] - T_AMBIENT_K[0])
    table = {name: round(1e3 * v(props, tau, C, F_props), 4) for name, C in CONSTANTS.items()}
    band = [1e3 * v(props, tau, min(CONSTANTS.values()), F_RANGE[0]), 1e3 * v(props, tau, max(CONSTANTS.values()), F_RANGE[1])]
    return {"thickness_um": thickness_um, "semi_thickness_m": tau, "F_from_properties": round(F_props, 3),
            "rate_mm_s_by_constant": table, "band_mm_s": [round(b, 4) for b in band],
            "scaling": "1/thickness; independent of flow speed in the thermal regime",
            "sources": {k: s for k, (_, s) in props.items() if k in ("rho_s_kg_m3", "c_s_J_kgK", "T_v_K", "T_f_K", "k_g_W_mK")} | {"F_range": CARMIGNANI}}


def thin_check(thickness_um: float, measured_rate_mm_s: float, props: dict = PMMA) -> dict:
    alpha_s = props["k_s_W_mK"][0] / (props["rho_s_kg_m3"][0] * props["c_s_J_kgK"][0])
    delta = alpha_s / (measured_rate_mm_s * 1e-3)
    tau = thickness_um * 1e-6 / 2
    r = tau / delta
    return {"semi_thickness_mm": tau * 1e3, "solid_heating_depth_mm": round(delta * 1e3, 4), "ratio_tau_over_delta": round(r, 3),
            "reading": "thin" if r < 0.3 else ("transitional" if r < 3 else "thick"),
            "note": "order-of-magnitude criterion; k_s is approximate (not in the project library)"}


def compare(thickness_um: float, measured_rate_mm_s: float, interval_mm_s: list[float] | None = None) -> dict:
    p = predict(thickness_um)
    lo, hi = p["band_mm_s"]
    out = {"prediction": p, "measured_mm_s": measured_rate_mm_s, "measured_interval_mm_s": interval_mm_s,
           "inside_theory_band": lo <= measured_rate_mm_s <= hi, "thin_check": thin_check(thickness_um, measured_rate_mm_s)}
    return out
