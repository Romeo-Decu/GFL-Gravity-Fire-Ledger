# Validated predictive models

**Status:** research direction (DEC-010, roadmap §17.2). Not built and not claimed.

## Problem
Predict a flame-spread observable, for example the spread rate as a function of flow, oxygen and thickness, for a condition that was not tested, with a stated validity domain and uncertainty.

## Governing theory and assumptions
- **Thin-fuel thermal regime (de Ris):** applies only inside the thermal regime.
- **Near the kinetic and radiative limits:** corrections using the Damköhler number and a radiative-loss parameter.
- **Basis of every model:** the regime gates. A model is not used outside the regime in which it was fitted.

## Architecture and interfaces
- **Inputs:** measured GFL results with their full budget (for example AR-001), plus fuel properties with provenance.
- **Outputs:** prediction, interval, and the gate states that justify use.
- **Out of domain:** the transfer engine returns "not transferable on current evidence". No prediction is shown without a passing domain check.

## Required data
Spread rates measured under a slope-independent rule at several flows and oxygen levels, within one family and one apparatus. At present B6 provides one flow segment (RES-021).

## Validation and falsification
- Held-out runs fixed before fitting (see held-out transferability).
- The model is falsified if held-out errors exceed the stated interval in more than the nominal share of cases.

## Feasibility gaps and blocking conditions
- Too few measured segments.
- The AIR display to cm/s mapping (ISS-013).
- Property data for the specific PMMA.
