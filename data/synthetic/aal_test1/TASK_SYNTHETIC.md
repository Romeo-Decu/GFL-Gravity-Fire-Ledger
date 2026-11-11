# Flame-spread rate from two sets of flame profiles (S1, S2)

You are an independent analyst. These two data sets have the structure of a top-view flame-spread record from a microgravity experiment: a thin solid fuel strip burning against a forced opposing air flow, photographed about once per second. Nobody expects a particular number. Do not look for published values.

## What you receive (per case, S1 and S2)
1. `<case>_frames_metadata.csv`: one row per frame in time order: image id, time `t_s` (seconds), `exposure_s` (the camera chose the shutter).
2. `<case>_band_profiles.csv`: one row per frame, 2160 values `c0 … c2159`, one per image column along the propagation direction. Values are relative radiance (counts per second): raw values divided by the frame's exposure time, frame median removed, averaged over the image rows that see the fuel strip.
3. `<case>_flow_display.csv`: the air-flow display setting and the time from which it applies.

Spatial scale: **14.7 columns per mm**.

## What we ask, for each case separately
1. The **front speed (mm/s) during the interval when the air display shows 3**. Define the flame front yourself and justify it.
2. A **95 % interval** for that speed, with the method.
3. The **direction** of propagation (towards increasing or decreasing column index).
4. **Everything the result depends on** (front definition, thresholds, frame selection, anything else), quantified where you can.
5. **Anomalies:** anything in the data that looks wrong, surprising or inconsistent, even if you cannot explain it.

## Rules
- Use Python with **numpy and pandas only**. Read only these files.
- Decide your method and frame selection **before** looking at fitted slopes, and write down any change of mind.
- Label every statement: [MEASURED from these files] / [ASSUMPTION] / [INFERENCE] / [UNKNOWN]. Never present a number as computed unless your code computes it.

## Deliver
- The complete code you ran (runnable on these files as given, no other input).
- For each case: preferred speed, 95 % interval, front definition, direction, the frames used.
- The dependency list and the anomaly list.
