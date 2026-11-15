# Measurement rule R-S2: the dark front in NASA's backlit Saffire images

**Status:** frozen 2026-11-14, after R-S1 failed (RES-060) and **after frames of sample 2-5 had been seen**, before any rate was computed with this rule and before any frame of sample 2-6 or of Saffire-I was viewed. It is therefore not blind for 2-5; it is blind for 2-6. Code: `tools/saffire_measure.py --rule R-S2`.

## Why a second rule

R-S1 assumed a luminous flame on a dark background, as in BASS-II. NASA's Saffire-II cameras image the sample in transmission against a green backlight: unburned fabric is bright, the burning and burned region is dark, and the backlight is off or saturated in parts of the record. The quantity that moves is the boundary of the dark region, a burn front seen in transmission, not a luminous edge.

## Rule

1. **Images, scale, time:** as R-S1 (NASA's mapped JPEGs of camera 1; checker period of the mapped grid; epoch milliseconds in the file name).
2. **Profile:** luminance averaged over the central half of the rows, smoothed with a 9-pixel moving average, along the long axis. No background subtraction.
3. **Valid frame:** the 95th percentile of the profile lies between 60 and 240 (backlight on, not saturated).
4. **Ignition end:** the end whose outer tenth is darker in the first valid frame.
5. **Bright reference:** the median of the profile over the tenth of the image farthest from the ignition end.
6. **Front:** scanning from the far end toward the ignition end, the first position where the profile falls below 0.5 of the bright reference.
7. **Window, rate, interval, sensitivity:** as R-S1 (front between 20 % and 80 % of the length; at least 20 frames; least-squares slope; moving-block bootstrap; thresholds 0.3 and 0.7 beside).
8. **Acceptance:** as R-S1, within 20 % of the rate NASA reports, for both strips. If it fails, the failure is reported, the rule is not changed, and Saffire-I is not measured with it.

## What it measures

The edge of the region that no longer transmits the backlight: burned or charred fabric, soot or a flame dense enough to block it. It is neither the luminous edge of R-W4 nor a demonstrated pyrolysis front.
