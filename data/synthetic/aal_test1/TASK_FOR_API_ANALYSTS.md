# Flame-spread rate from two sets of flame profiles (S1, S2), code-carrying analysis

Read first: `DATA_SCHEMA_AND_SAMPLE.md`. You do **not** receive the full data and you **cannot run code**. Your deliverable is **code + reasoning**: the Validator executes your code on the full files and records its real output. **Do not state any numerical result you did not compute**; predictions are allowed only if labelled `[PREDICTION — not computed]`.

## The data
Two data sets (S1, S2) with the structure of a top-view flame-spread record from a microgravity experiment: a thin solid fuel strip burning against a forced opposing air flow, photographed about once per second. Nobody expects a particular number. Do not look for published values.

## Questions, for each case separately
1. **Determine the direction of propagation from the data** (towards increasing or decreasing column index) before you define any front. Say how.
2. The **front speed (mm/s) during the interval when the air display shows 3**. Define the flame front yourself, justify it, and name what your definition tracks.
3. A **95 % interval** for that speed, with the method.
4. **Everything the result depends on** (front definition, threshold, frame selection, anything else), quantified by your code where possible.
5. **Anomalies**: anything in the data that looks wrong, surprising or inconsistent.

## Rules
- Python 3 with **numpy and pandas only**. Read only the files described in the schema.
- Decide method and frame selection before seeing slopes; log every change of mind.
- Label statements: [MEASURED by code] (only once the Validator ran it) / [ASSUMPTION] / [INFERENCE] / [UNKNOWN] / [PREDICTION — not computed].

## Deliver (one answer)
- One complete Python 3 script, reading `S1_frames_metadata.csv`, `S1_band_profiles.csv`, `S1_flow_display.csv` and the same three files for S2 from the working directory, and printing, for each case, a line exactly of the form:
  `RESULT <case> speed_mm_s=<value> ci95_low=<value> ci95_high=<value> direction=<increasing|decreasing>`
  plus every other number your report needs.
- The report, with every number written as a placeholder filled from the script's printed output.
