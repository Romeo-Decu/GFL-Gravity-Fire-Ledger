# Measurement rule R-S1: concurrent-flow spread over Saffire fabric samples

**Status:** frozen 2026-11-14, before any Saffire flame image was opened. Anchored in the ledger with the code that applies it (`tools/saffire_measure.py`). The calibration images (checkerboard distortion grids) were opened to choose the scale rule; no flame image was.

## Question

Can GFL's luminous-edge method, frozen before the data, reproduce the spread rates NASA reports for the two SIBAL strips of Saffire-II (samples 2-5 and 2-6: 2.1 and 2.6 mm/s)? If it can, the same rule measures the Saffire-I sample, and the Saffire-II to Saffire-I comparison (RES-059) rests on GFL measurements on both sides.

## Rule

1. **Images:** NASA's `Jpeg_Mapped` images (distortion corrected to a flat grid by NASA) of camera 1 for the sample. Time of each frame: the epoch milliseconds in its file name.
2. **Scale:** from NASA's mapped distortion-grid image of the same sample and camera (30 mm checker blocks): the period of the checker pattern along the image's long axis, by autocorrelation of the column-mean brightness, gives pixels per 30 mm.
3. **Profile:** for each frame, luminance (0.299 R + 0.587 G + 0.114 B) averaged over the central half of the rows, minus the median profile of the first 30 frames of the set (taken as before ignition). Axis: along the image's long side.
4. **Valid frame:** the background-subtracted profile peaks at 40 or more (8-bit units).
5. **Edge:** the position at half of the frame's peak (0.5, as R-W4), the farthest from the ignition end. Ignition end: the half of the image holding the peak of the first valid frame.
6. **Window:** valid frames whose edge lies between 20 % and 80 % of the image length from the ignition end. Fewer than 20 such frames: not measurable.
7. **Rate:** least-squares slope of edge position against time. Interval: 95 % from a moving-block bootstrap (blocks of 1 s, 2,000 resamples, seed 20261114). Sensitivity: the same at thresholds 0.3 and 0.7, reported beside, not merged.
8. **Acceptance, fixed now:** R-S1 reproduces NASA's value for a strip when the measured rate is within 20 % of it. The rule is accepted only if both strips pass. If either fails, the result is reported as a failure and the rule is not changed; Saffire-I is not measured with it.

## What it measures, and what it does not

A luminous-edge rate, like R-W4, not a pyrolysis front. NASA's tables do not say how NASA obtained 2.1 and 2.6 mm/s; agreement within 20 % says the two methods agree on these samples, not that either is the true front speed. One flight per sample.
