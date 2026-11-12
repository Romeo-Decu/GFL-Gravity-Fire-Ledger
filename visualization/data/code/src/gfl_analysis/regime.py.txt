"""A4. CRAM-2: which opposed-flow regime a run is in (Bhattacharjee et al. 2016; de Ris 1969).

Two dimensionless groups, computed from the calibrated flow speed (A0) and cited properties:
  Damkoehler  Da = t_res / t_chem,  t_res = alpha_g / U^2,  t_chem = 1 / (A * rho_f * Y_O2 * exp(-E / (R T_f)))
  radiation   Rr = surface re-radiation over the gas-phase preheat length / conductive heat flux into the fuel
              = eps * sigma * (T_v^4 - T_inf^4) * (alpha_g / U) / (k_g * (T_f - T_v))
Reading: radiative when Rr >= 1; kinetic when Da <= Da_kin; thermal otherwise; transitional within a factor of 3
of either boundary. Da_kin is anchored where kinetic slowing was observed for thin PMMA (0.125 mm film, about
60 cm/s, Rojas-Alva 2022), evaluated with the same properties, so only ratios of Da matter.
These are order-of-magnitude groups: the classification is evidence, not a measurement, and GFL never pools runs
across regimes on the strength of it alone.
"""
from __future__ import annotations

import math

from .flow import air_display_to_velocity
from .sources import AIR_700K, PMMA, R_GAS, SIGMA, T_AMBIENT_K, Y_O2_AIR, ROJAS_ALVA_2022

U_KINETIC_ONSET_CM_S = (60.0, ROJAS_ALVA_2022 + ", kinetics noticeable above about 60 cm/s for 0.125 mm PMMA film")


def _alpha_g():
    return AIR_700K["k_W_mK"][0] / (AIR_700K["rho_kg_m3"][0] * AIR_700K["cp_J_kgK"][0])


def damkohler(u_cm_s: float, props: dict = PMMA) -> float:
    u = u_cm_s / 100
    t_res = _alpha_g() / u ** 2
    Tf = props["T_f_K"][0]
    rho_f = AIR_700K["rho_kg_m3"][0] * 700.0 / Tf
    rate = props["A_gas_m3_kgs"][0] * rho_f * Y_O2_AIR[0] * math.exp(-props["E_gas_J_mol"][0] / (R_GAS * Tf))
    return t_res * rate


def radiation_number(u_cm_s: float, props: dict = PMMA) -> float:
    u = u_cm_s / 100
    Tv, Tf, Ti = props["T_v_K"][0], props["T_f_K"][0], T_AMBIENT_K[0]
    loss = props["emissivity_surface"][0] * SIGMA * (Tv ** 4 - Ti ** 4)
    return loss * (_alpha_g() / u) / (props["k_g_W_mK"][0] * (Tf - Tv))


def classify(air_display: float) -> dict:
    f = air_display_to_velocity(air_display)
    u = f["value_cm_s"]
    if u is None:
        return {"air_display": air_display, "regime": "undetermined", "reason": "no flow reading", "flow": f}
    if u == 0:
        return {"air_display": air_display, "u_cm_s": 0.0, "regime": "radiative side (no forced flow)",
                "reason": "with no forced flow the radiation number grows without bound; the only flow is flame-induced "
                          "(thermal expansion, diffusion), which is not characterised, so no number is reported", "flow": f}
    da, rr = damkohler(u), radiation_number(u)
    da_kin = damkohler(U_KINETIC_ONSET_CM_S[0])
    if rr >= 1:
        reg = "radiative"
    elif da <= da_kin:
        reg = "kinetic"
    else:
        reg = "thermal"
    near = (rr >= 1 / 3 and rr < 3) or (da_kin / 3 < da < 3 * da_kin)
    return {"air_display": air_display, "u_cm_s": u, "damkohler": round(da, 2), "damkohler_kinetic_anchor": round(da_kin, 2),
            "radiation_number": round(rr, 3), "regime": reg + (" (transitional)" if near else ""),
            "flow": f, "basis": "order-of-magnitude groups with cited and approximate properties (see sources.py)"}


def consistency_with_measurement(rates_by_display: dict[float, float]) -> dict:
    """Thermal-regime signature: the rate does not depend on flow. Reports the spread of rates across displays."""
    vals = [r for r in rates_by_display.values() if r]
    if len(vals) < 2:
        return {"status": "undetermined", "reason": "fewer than two flow levels measured in the thermal regime; segments in the transitional or radiative regime are not part of this check"}
    spread = (max(vals) - min(vals)) / (sum(vals) / len(vals))
    return {"rates_by_display": rates_by_display, "relative_spread": round(spread, 3),
            "reading": "consistent with flow independence" if spread <= 0.15 else "flow dependence or measurement scatter above 15 %"}
