# Flame-front speed from four sets of flame profiles (T1–T4), code-carrying analysis

Read first: `DATA_SCHEMA_AND_SAMPLE.md`. You do **not** receive the full data and you **cannot run code**. Your deliverable is **code + reasoning**: the Validator executes your code on the full files and records its real output. **Do not state any numerical result you did not compute**; predictions only if labelled `[PREDICTION — not computed]`.

## The data
Four data sets with the structure of a top-view flame-spread record from a microgravity experiment: a thin solid fuel strip burning against a forced opposing air flow, photographed about once per second. Nobody expects a particular number. Do not look for published values.

## Questions, for each case separately
1. **Determine the direction of propagation from the data** (towards increasing or decreasing column index) before you define any front. Say how.
2. The **speed of the flame front (mm/s) during the estimand interval**: the interval when the air display shows **3** for T1, T2 and T4, and **2** for T3. Define the flame front yourself, justify it, and name what your definition tracks. Note that a luminous edge is not necessarily the same thing as the physical front of the burning solid.
3. A **95 % interval** for that speed that you are willing to defend, including every source of uncertainty you can identify. State which sources you could not quantify.
4. **Everything the result depends on**, quantified where possible.
5. **Anomalies**: anything in the data that looks wrong, surprising or inconsistent.

## Rules
- Python 3: the standard library is allowed; **no third-party package other than numpy and pandas**. Read only the files described.
- Decide method and frame selection before seeing slopes; log every change of mind.
- Label statements: [MEASURED by code] / [ASSUMPTION] / [INFERENCE] / [UNKNOWN] / [PREDICTION — not computed].

## Deliver (one answer)
- One complete Python 3 script reading `<case>_frames_metadata.csv`, `<case>_band_profiles.csv`, `<case>_flow_display.csv` for T1, T2, T3, T4 from the working directory and printing, for each case, a line exactly of the form:
  `RESULT <case> speed_mm_s=<value> ci95_low=<value> ci95_high=<value> direction=<increasing|decreasing>`
  plus every other number your report needs.
- The report, with every number written as a placeholder filled from the script's printed output.
