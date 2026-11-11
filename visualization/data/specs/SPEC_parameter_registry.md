# Physical model and parameter registry

**Status:** research direction (DEC-060; restored after the dossier audit). Partly present: `src/gfl_analysis/sources.py` already keeps every property CRAM-1 and CRAM-2 use with its source, or labels it approximate.

## Problem
Every equation and property GFL uses should live in one registry: the equation, its validity domain, each parameter with value, unit, source, temperature of evaluation and uncertainty, and which modules use it.

## Architecture and interfaces
- **Entries:** models (de Ris thin, Delichatsios, EST, Damköhler, radiation number) and parameters (PMMA, air, kinetics).
- **Rules:** a module may only read parameters from the registry; a parameter without a source is shown as approximate on every output that uses it.

## Required data
Primary sources for the parameters now marked approximate (solid conductivity, surface emissivity, air properties at 700 K) and for the actual PMMA used in BASS-II.

## Validation and falsification
Unit and dimension checks on every model; regression tests that change in a parameter changes outputs only where the registry says it is used.

## Feasibility gaps and blocking conditions
Material data for the BASS-II PMMA lot are not published; the registry can only carry literature values with their spread.
