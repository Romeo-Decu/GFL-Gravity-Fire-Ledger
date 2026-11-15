# Window rule R-W3

**Declared:** 2026-11-11, before R-W3 was run on any real run (B6 included) and before the test 2 synthetic data existed. **Author:** Claude (PM). **Code:** `tools/window_rule_r3.py`, which imports the frozen R-W2 code (`tools/b6_window_rule.py`, commit `ea984bd`) and changes only what is listed here. **Basis:** AAL test 1 (RES-031, RES-032; ISS-044, ISS-047).

## Changes from R-W2

| # | R-W2 | R-W3 | Why |
|---|---|---|---|
| 1 | G4 (no gap above 5 s) is cumulative from the first frame of the run | G4 is counted from the first frame where a flame is present (G1); frames before it are outside the record but do not break it; the record ends at the first gap above 5 s after it starts | B11's first still is a pre-burn reference 287 s before the burn, which made every frame unusable (ISS-044) |
| 2 | Reference front: 0.1 of each frame's peak | Reference front: **0.5 of each frame's peak** (midpoint of the leading ramp); 0.8 added to the relative definitions | With a sharpening edge, 0.1 was biased low by 6 % on a known answer; the midpoint does not move when a symmetric edge changes width (ISS-047) |
| 3 | Reported: statistical 95 % interval; definition range separate | Reported interval = statistical 95 % interval widened on each side by the definition systematic s = max(\|r(0.2) − r(0.5)\|, \|r(0.8) − r(0.5)\|), in quadrature; the full range over all definitions still reported | The statistical interval alone did not cover the truth when the definition mattered |

Unchanged: gates G1, G2, G3 and G5, segment = interval between flow-display changes, at least 6 frames over at least 6 s, OLS and Theil–Sen, HAC lag, moving-block bootstrap (4000, seed 20261110), scale 14.7 px/mm with a ±3 % allowance, parallax and luminous-to-pyrolysis offset stated as unknown.

## What R-W3 does not fix

The midpoint is invariant only if the edge stays symmetric about it; an asymmetric edge or a drifting offset between the luminous edge and the pyrolysis front still biases every luminous definition. Test 2 includes both, and the result is reported whatever it is.

## Order of use

1. This document, the code and the test 2 predictions are sealed and anchored.
2. The test 2 synthetic data are generated afterwards, truth withheld.
3. R-W3 then runs on the synthetic data, on B6 (new reference value, replacing nothing until recorded) and on the predicted runs.
