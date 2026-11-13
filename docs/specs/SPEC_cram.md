# CRAM: physics analysis modules

**Status:** CRAM-1 built (RES-043, `src/gfl_analysis/cram1.py`); CRAM-2 partial (RES-044, `regime.py`: dimensionless groups and a regime reading, boundaries order-of-magnitude; not confirmed by the measured curves: flow independence is not shown inside B13 and the groups do not account for the oxygen sensitivity of RES-055); CRAM-3 designed, not built.

## CRAM-1 Thermodynamics and transport
- **What it does:** a thin-fuel thermal-regime comparison (de Ris) using PMMA properties from the literature, with property provenance and units.
- **Labelling:** marked "not validated" until compared with independent data.

## CRAM-2 Combustion regime
- **What it does:** classifies runs as radiative, thermal or kinetic on the measured spread rate versus flow curve, with rules traceable to the Bhattacharjee framework.
- **Precondition:** the curve exists only when several flow segments can be measured. B6 alone gives one segment (RES-021).

## CRAM-3 Nonlinear dynamics
- **What it does:** analyses oscillation of flame area and position.
- **Significance:** tested against surrogate data (phase-randomised, AAFT).
- **Verification:** on synthetic signals with known dynamics first.

## Validation (all three)
- Synthetic inputs with known answers, units tests, and counter-example tests.
- No module output enters a result without a ledger derivation entry and its qualifiers.

## Blocking conditions
- Enough measured segments per run; flow mapping (ISS-013); property data for the actual PMMA.
