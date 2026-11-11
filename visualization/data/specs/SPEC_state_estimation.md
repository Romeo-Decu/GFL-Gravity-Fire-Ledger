# State estimation (Kalman-type filtering)

**Status:** research direction (DEC-060; restored after the dossier audit). Not built and not claimed. The v4 claim of a validated EKF was withdrawn (doc 0.0).

## Problem
Estimate the flame-front position and speed continuously between stills, and the hidden state (for example the edge-to-front offset) from several noisy observations.

## Governing theory and assumptions
- **Model:** a state-space model of the front (position, speed, edge width), Kalman filter for linear noise, extended or ensemble filter for nonlinear observation models.
- **Assumption that limits it:** the process and observation noise must be characterised; without that the filter's interval is not honest (blind test 2 showed intervals that are too narrow, RES-034).

## Architecture and interfaces
- **Inputs:** front positions per still with their measurement uncertainty, video frames for timing, overlay flow.
- **Outputs:** filtered position and speed with covariance; compared with the window-rule rate on the same data.

## Required data
A second observation of the front independent of luminosity (surface temperature or side view) to make the offset observable; without it the offset is not identifiable.

## Validation and falsification
Synthetic burns with known state (the test 2 generator); coverage of the filter's interval must be at its nominal level.

## Feasibility gaps and blocking conditions
No independent front observation in BASS-II files held; noise models not characterised.
