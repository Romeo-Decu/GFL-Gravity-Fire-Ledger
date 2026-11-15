# Window rule R-W4

**Declared:** 2026-11-11, by Claude (PM) under the owner's mandate to decide while he is away. Sealed and anchored **before** R-W4 runs on any real run. **Status:** declared; adoption as the release rule is the owner's decision (review 12 Nov).

## The one change from R-W3

R-W3 starts the burn record at the first frame passing G1 (peak above 20 × noise). G1 is a brightness test, not a flame test: B11's pre-burn reference still (illuminated scene, 1/3 s exposure) passes G1 and fails G2 (no edge inside the field). The record therefore opens at t = 0 and breaks at B11's 287 s gap, leaving no usable frame (ISS-049).

R-W4 starts the burn record at the first frame passing **G1 and G2**. Frames after the start that fail G2 stay inside the record (they still are not usable), so a single bad frame does not end it. Nothing else changes: gates G1–G3 and G5, the 5 s continuity limit, segment minimums, front definitions (reference 0.5 of peak), estimators, bootstrap and the reported interval are R-W3 as written. `tools/window_rule_r4.py` imports R-W3 and replaces only the record-start function; tests in `tests/test_window_rule_r4.py`.

## Why this is not fitting the rule to a result

The defect was found and recorded (ISS-049, 2026-11-11 afternoon) before any B11 rate had been computed under any rule; B11 has no measured rate in the repository. The change follows from what the gates mean, not from a value. The expected effect on runs without a bright pre-burn frame before a long gap (B6, B9, B13, the synthetic packages) is none; this is checked and reported, and any difference is a finding.

## How B11 results under R-W4 are reported

P-B11a and P-B11b were registered under R-W3 and stay **not testable** in the protocol scorecard (RES-037). A B11 result under R-W4 is reported separately as a **post-protocol measurement with a declared rule change**, compared with the same bands for information, and never counted as a supported prediction.
