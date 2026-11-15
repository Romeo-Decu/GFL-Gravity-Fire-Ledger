# Multiphysics simulation

**Status:** research direction (DEC-010). Not built.

## Problem
Simulate opposed-flow spread over thin PMMA with coupled gas and solid phases, to test hypotheses that measurements cannot isolate, such as edge sharpening or the offset between the luminous edge and the pyrolysis front.

## Theory and assumptions
- **Equations:** reacting low-Mach Navier–Stokes; one-step or reduced chemistry; solid pyrolysis with Arrhenius kinetics; radiation through a grey or banded model.
- **Microgravity:** gravity is set from measured residual acceleration, not assumed zero.

## Architecture and interfaces
- **Solver:** an external open solver (for example FDS or an OpenFOAM-based code), run from a parameter file sealed in the ledger.
- **Outputs:** treated as derived evidence with qualifiers, never as measurements.
- **Comparison:** against GFL measurements only through the same observable definition. For example, the simulated luminous edge at 0.1 of peak is compared with the measured one.

## Required data
Fuel properties, duct geometry, flow profile, oxygen, and the ignition history from the source documents.

## Validation and falsification
- Mesh and time-step convergence.
- Reproduction of the measured B6 rate and edge sharpening within the stated budget.
- Failure is reported as a result.

## Blocking conditions
Compute cost; chemistry uncertainty; unknown boundary conditions (holder heat loss).
