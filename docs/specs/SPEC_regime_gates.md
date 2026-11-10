# Physics-based similarity: regime gates computed from data

**Status:** partial. The deterministic transfer engine and its gates exist; gate states for the PMMA-100 case are declared from the source audit, not yet computed from measured data.

## What we want
Two experiments are comparable for a given question only if they share the same governing physics. For thin-fuel opposed-flow flame spread, the gates are computed from measured or source values, each with a rule ID. When an input is missing, the gate abstains.

## Design
- **Thermal regime (de Ris thin-fuel).** Compare the measured spread rate with the thermal-theory prediction from fuel properties, flow and oxygen; record the ratio.
- **Damköhler-type kinetic gate.** Compare the residence time with the chemical time. Near extinction the regime is kinetic; the gate fails if one experiment is kinetic and the other thermal.
- **Radiative gate.** Estimate the radiative-loss parameter at low flow, which is relevant to microgravity; flag the radiative regime.
- **Output:** each gate returns pass, partial, fail or unknown, with its inputs, provenance and rule ID. The transfer engine consumes these states unchanged.

## Data
Fuel properties come from the literature, with provenance. Flow comes from the overlay or calibration (ISS-013 must be resolved first). Oxygen comes from the PSI-25 table, using the calibrated column.

## Validation
- Unit and dimension tests.
- Counter-examples: synthetic inputs placed on each side of a regime boundary must flip the gate.
- Abstention tests: any missing input must give "unknown".

## Blocking conditions
- AIR display to cm/s mapping (ISS-013).
- Property uncertainty for the specific PMMA lot.
