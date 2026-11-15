# Partial gravity: Moon and Mars

**Status:** specified, not built (DEC-071).

## Problem
Fire behaviour at lunar (0.17 g) and Martian (0.38 g) gravity is neither the microgravity case nor the Earth case: a weak buoyant flow returns, and published work suggests materials can be more flammable at partial gravity than at either extreme. The question: what in the microgravity and normal-gravity record may inform partial gravity.

## Design
- **Gravity as a continuous condition**, not three labels: the buoyant velocity scale replaces or adds to the forced flow in the regime calculation (CRAM-2), so a run in forced flow in microgravity and a run in buoyant flow can be placed on one axis of effective opposed flow.
- **Transfer gates** then compare effective flow, not the gravity label; the mixed-convection assumption is stated as an assumption with its own bound.
- **Sources:** centrifuge and aircraft partial-gravity experiments in the literature library; drop-tower and ISS runs for the two ends.

## Required data
Partial-gravity runs with recorded gravity level and flow; these are mostly in publications, not in PSI (the evidence map found none stating partial gravity).

## Validation
Reproduce a published partial-gravity trend for one material from the two ends before using the method anywhere else; report where it fails.

## Blocking conditions
Almost no partial-gravity raw data are public; the effective-flow assumption is untested in GFL.
