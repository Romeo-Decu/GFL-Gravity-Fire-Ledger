# Model predictive control (real MPC)

**Status:** research direction (DEC-010). Not built. Removed from the demonstrable product after the v4 audit; recorded here so the requirement is not lost.

## Why it was removed
The original v4 "MPC" was fixed if/else thresholds. It had no dynamic model, no horizon, no objective, no constraints and no solver. Ventilation does not act monotonically on a fire: more flow can remove heat, but it also feeds oxygen.

## What a real MPC would require
- **Dynamic model:** a validated model linking ventilation, oxygen and spread (from predictive models), with stated uncertainty.
- **Control problem:** a receding horizon; an objective with explicit safety weights; constraints on actuators and crew procedures; a numerical solver.
- **Integration:** with ECLSS logic and crew procedures, which today stop local ventilation to limit oxygen supply.

## Validation
- Simulation first, against the multiphysics model.
- Then hardware-in-the-loop.
- No flight claim without a qualification path.

## Blocking conditions
- No validated dynamic model exists.
- Safety qualification is far outside the scope of GFL.
- Actuation is out of scope for Release A (DEC-013).
