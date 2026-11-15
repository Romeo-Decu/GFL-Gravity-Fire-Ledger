"""Physical constants and property sets with their sources. Values marked approximate have no source in the project library."""
from __future__ import annotations

ROJAS_ALVA_2022 = "Rojas-Alva 2022, Flammability of materials intended for use in microgravity environments, Table 10 (PMMA film, Acryplen HBS006)"
CARMIGNANI = "Carmignani et al., Influence of edge propagation on downward flame spread over three-dimensional PMMA samples (thin and thick limits; F between 4.4 and 5.5, 4.76 fitted to data)"
NASA_FAN_CAL = "PSI-25 Reference Data, Fan calibration data.xlsx: U = 1.0066 x AIR display, SPICE calibration at 56 mm downstream, 36 mm from bottom (centreline)"

# PMMA and flame, Rojas-Alva 2022 Table 10
PMMA = {
    "rho_s_kg_m3": (1140.0, ROJAS_ALVA_2022),
    "c_s_J_kgK": (1465.0, ROJAS_ALVA_2022),
    "T_v_K": (670.0, ROJAS_ALVA_2022),
    "T_f_K": (2640.0, ROJAS_ALVA_2022),
    "k_g_W_mK": (0.051, ROJAS_ALVA_2022 + " (5.1e-5 W/mmK)"),
    "A_gas_m3_kgs": (1.0e9, ROJAS_ALVA_2022),
    "E_gas_J_mol": (1.5e5, ROJAS_ALVA_2022),
    # not in the project library: standard handbook values, labelled approximate
    "k_s_W_mK": (0.19, "approximate (handbook value for PMMA near room temperature)"),
    "emissivity_surface": (0.9, "approximate (typical for PMMA surface)"),
}
# air near 700 K (leading-edge temperature used by Carmignani et al.)
AIR_700K = {
    "rho_kg_m3": (0.498, "approximate (air tables, 700 K, 1 atm)"),
    "cp_J_kgK": (1075.0, "approximate (air tables, 700 K)"),
    "k_W_mK": (0.051, ROJAS_ALVA_2022),
}
T_AMBIENT_K = (300.0, "approximate (cabin ambient)")
SIGMA = 5.670374419e-8
R_GAS = 8.314462618
Y_O2_AIR = (0.233, "mass fraction of O2 in air at 21 % by volume")
