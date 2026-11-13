"""A9. Physical model and parameter registry: every equation and property GFL uses, in one place.

Parameters are read from sources.py (the only place modules take them from). For each: value, unit, source, whether it
is sourced or approximate, and which model uses it. `used_by` is not declared by hand: it is found by changing the value
and seeing which model outputs move, so the registry cannot drift from the code.
"""
from __future__ import annotations

import copy

from . import cram1, regime, sources

UNITS = {"rho_s_kg_m3": "kg/m3", "c_s_J_kgK": "J/(kg K)", "T_v_K": "K", "T_f_K": "K", "k_g_W_mK": "W/(m K)", "A_gas_m3_kgs": "m3/(kg s)", "E_gas_J_mol": "J/mol",
         "k_s_W_mK": "W/(m K)", "emissivity_surface": "-", "rho_kg_m3": "kg/m3", "cp_J_kgK": "J/(kg K)", "k_W_mK": "W/(m K)"}
MEANING = {"rho_s_kg_m3": "solid density", "c_s_J_kgK": "solid specific heat", "T_v_K": "vaporisation temperature", "T_f_K": "flame temperature (air, 21 % oxygen)",
           "k_g_W_mK": "gas conductivity", "A_gas_m3_kgs": "gas-phase pre-exponential factor", "E_gas_J_mol": "gas-phase activation energy",
           "k_s_W_mK": "solid conductivity", "emissivity_surface": "surface emissivity", "rho_kg_m3": "air density at 700 K", "cp_J_kgK": "air specific heat at 700 K", "k_W_mK": "air conductivity at 700 K"}
MODELS = {
    "thin_fuel_spread_rate": {"module": "src/gfl_analysis/cram1.py", "equation": "V_f = C k_g (T_f - T_v) / (rho_s c_s tau (T_v - T_inf)), tau = half thickness",
                              "constants": "C = pi/4 (Delichatsios), sqrt(2) (de Ris), 1 (EST)", "domain": "opposed-flow spread over a thermally thin fuel in the thermal regime; air at 21 % oxygen",
                              "output": lambda p: cram1.predict(100, p)["rate_mm_s_by_constant"]},
    "damkohler_number": {"module": "src/gfl_analysis/regime.py", "equation": "Da = (alpha_g / U^2) A rho_f Y_O2 exp(-E / (R T_f))", "constants": "kinetic anchor at 60 cm/s (Rojas-Alva 2022)",
                         "domain": "order of magnitude; forced opposed flow above zero", "output": lambda p: regime.damkohler(5.0, p)},
    "radiation_number": {"module": "src/gfl_analysis/regime.py", "equation": "Rr = eps sigma (T_v^4 - T_inf^4) (alpha_g / U) / (k_g (T_f - T_v))", "constants": "Stefan-Boltzmann constant",
                         "domain": "order of magnitude; forced opposed flow above zero", "output": lambda p: regime.radiation_number(5.0, p)},
}


def _used_by(key: str) -> list[str]:
    changed = copy.deepcopy(sources.PMMA)
    changed[key] = (changed[key][0] * 1.1, changed[key][1])
    return [name for name, m in MODELS.items() if m["output"](changed) != m["output"](sources.PMMA)]


def build() -> dict:
    params = []
    for key, (value, source) in sources.PMMA.items():
        params.append({"set": "PMMA and flame", "key": key, "meaning": MEANING[key], "value": value, "unit": UNITS[key], "source": source,
                       "sourced": not source.startswith("approximate"), "used_by": _used_by(key)})
    for key, (value, source) in sources.AIR_700K.items():  # read as module constants, so use is stated from the equations, not probed
        params.append({"set": "air at 700 K", "key": key, "meaning": MEANING[key], "value": value, "unit": UNITS[key], "source": source,
                       "sourced": not source.startswith("approximate"), "used_by": ["damkohler_number", "radiation_number"]})
    params.append({"set": "ambient", "key": "T_AMBIENT_K", "meaning": "ambient temperature", "value": sources.T_AMBIENT_K[0], "unit": "K", "source": sources.T_AMBIENT_K[1], "sourced": False,
                   "used_by": ["thin_fuel_spread_rate", "radiation_number"]})
    params.append({"set": "ambient", "key": "Y_O2_AIR", "meaning": "oxygen mass fraction of air", "value": sources.Y_O2_AIR[0], "unit": "-", "source": sources.Y_O2_AIR[1], "sourced": True, "used_by": ["damkohler_number"]})
    params.append({"set": "flow", "key": "fan_calibration", "meaning": "flow speed per unit of air display", "value": 1.0066, "unit": "cm/s per display unit", "source": sources.NASA_FAN_CAL, "sourced": True,
                   "used_by": ["damkohler_number", "radiation_number"]})
    models = [{"name": k, **{f: v for f, v in m.items() if f != "output"}, "parameters": sorted(p["key"] for p in params if k in p["used_by"])} for k, m in MODELS.items()]
    return {"parameters": params, "models": models, "approximate": [p["key"] for p in params if not p["sourced"]],
            "note": "Literature values, not the BASS-II PMMA lot (its material data are not published). Flame temperature is sourced for 21 % oxygen only."}
