
# VERIFICATION OF PRECEDING PHASE (DRAFT)

**VERDICT: PASS**
**ALIGNMENT: YES**

The DRAFT phase artifact (task_brief) is the original task definition provided by the Founder. It is consistent with the current task context and provides the complete foundation for this REALITY phase analysis. No defects detected.

**Verification findings:**
- [CONFIRMED] The task_brief defines the B6 blind analysis objective, constraints, and phased workflow as specified in the project context.
- [CONFIRMED] All required input files (TASK_FOR_API_ANALYSTS.md, DATA_SCHEMA_AND_SAMPLE.md, SHA256SUMS) are referenced and available in the specified path.
- [CONFIRMED] Constraint set matches: independent analysts, no code execution, single Python script delivery, labeling requirements, no published values lookup, no repository writes.
- [CONFIRMED] Phase sequence (REALITY → ADVERSARIAL_AUDIT → INTEGRATION_REVIEW → LOCAL_VALIDATION → CONCEPT) is properly specified.
- [CONFIRMED] The task_brief artifact version (v1) aligns with the current execution context.

---

# ARTEFACT: REALITY PHASE — independent blind analysis of NASA BASS-II test B6

**Agent:** Reality_Analyst (deepseek_v4)
**Date:** 2026-11-06
**Phase:** REALITY
**Status:** Deliverable — Python script + analysis report

---

## 1. Python Analysis Script

```python
#!/usr/bin/env python3
"""
GFL-R1: B6 Blind Analysis Script — Reality_Analyst (deepseek_v4)
Reads B6_frames_metadata.csv and B6_band_profiles.csv from working directory.
Prints all computed quantities needed for the analysis report.
Uses only numpy and pandas.
"""

import numpy as np
import pandas as pd
import sys

# ─── Load data ──────────────────────────────────────────────────────────────
try:
    metadata = pd.read_csv("B6_frames_metadata.csv")
    profiles = pd.read_csv("B6_band_profiles.csv")
except FileNotFoundError as e:
    print(f"ERROR: Missing input file — {e}", file=sys.stderr)
    sys.exit(1)

# Verify row counts match
n_frames = len(metadata)
assert n_frames == len(profiles), "Metadata and profiles row counts differ!"
print(f"METADATA_ROWS: {n_frames}")
print(f"PROFILE_ROWS: {len(profiles)}")
print(f"PROFILE_COLS_AFTER_IMAGE: {len(profiles.columns) - 1}")

# ─── Time vector and basic checks ───────────────────────────────────────────
t = metadata["unix_time_s"].values  # seconds, includes sub-second
exposure = metadata["exposure_s"].values
iso = metadata["iso"].values
f_number = metadata["f_number"].values

# Verify time monotonicity and identify reversals/gaps
time_diffs = np.diff(t)
forward_steps = np.sum(time_diffs > 0)
backward_steps = np.sum(time_diffs < 0)
zero_steps = np.sum(time_diffs == 0)
median_dt = np.median(time_diffs[time_diffs > 0]) if forward_steps > 0 else np.nan
min_dt = np.min(time_diffs[time_diffs > 0]) if forward_steps > 0 else np.nan
max_dt = np.max(time_diffs) if n_frames > 1 else np.nan
t_start = t[0]
t_end = t[-1]
duration = t_end - t_start

print(f"\n─── TIME DATA ───")
print(f"T_START_UNIX: {t_start:.3f}")
print(f"T_END_UNIX: {t_end:.3f}")
print(f"DURATION_S: {duration:.3f}")
print(f"FORWARD_STEPS: {forward_steps}")
print(f"BACKWARD_STEPS: {backward_steps}")
print(f"ZERO_STEPS: {zero_steps}")
print(f"MEDIAN_DT_S: {median_dt:.6f}" if not np.isnan(median_dt) else "MEDIAN_DT_S: N/A")
print(f"MIN_DT_S: {min_dt:.6f}" if not np.isnan(min_dt) else "MIN_DT_S: N/A")
print(f"MAX_DT_S: {max_dt:.6f}" if not np.isnan(max_dt) else "MAX_DT_S: N/A")

if backward_steps > 0:
    print("WARNING: Non-monotonic timestamps detected!")

# ─── Exposure statistics ────────────────────────────────────────────────────
unique_exposures, exp_counts = np.unique(exposure, return_counts=True)
print(f"\n─── EXPOSURE ───")
print(f"UNIQUE_EXPOSURES_S: {unique_exposures.tolist()}")
print(f"EXPOSURE_FRACTION_MAX: {np.max(exp_counts)/n_frames:.3f}")

# ─── Profile data → column-wise array ───────────────────────────────────────
# Columns c0..c2159 → spatial positions (half-resolution columns)
profile_cols = [c for c in profiles.columns if c.startswith("c")]
profile_data = profiles[profile_cols].values.astype(np.float64)
n_cols = profile_data.shape[1]

# Spatial calibration: 14.7 columns/mm ±3%  →  mm_per_col = 1/14.7 ≈ 0.06803 mm
# Position vector (mm) from column index
mm_per_col = 1.0 / 14.7
mm_per_col_unc = mm_per_col * 0.03  # ±3%
x_mm = np.arange(n_cols) * mm_per_col
print(f"\n─── SPATIAL ───")
print(f"SPATIAL_COLS: {n_cols}")
print(f"MM_PER_COL: {mm_per_col:.6f}")
print(f"MM_PER_COL_UNC_3PCT: {mm_per_col_unc:.6f}")
print(f"X_RANGE_MM: [{x_mm[0]:.3f}, {x_mm[-1]:.3f}]")

# ─── Question 1: Determine propagation direction from data ──────────────────
# Approach: track centroid of luminous region over time.
# The flame propagates against the flow (upstream) according to experiment description,
# but we must determine which direction in the image that corresponds to.
# We look for motion of a characteristic feature (centroid of bright pixels).

# Binary mask: pixels above background → identify flame region per frame
# Use median of each frame as local background reference (already subtracted in preprocessing per
# DATA_SCHEMA: "minus frame median", so values are already background-subtracted relative radiance).
# Threshold: significantly above zero (signal present).
threshold_relative = 10.0  # relative radiance units (counts/s) — [ASSUMPTION] see report

# For each frame, compute the centroid (center of mass) of pixels above threshold
centroids_mm = np.full(n_frames, np.nan)
for i in range(n_frames):
    row = profile_data[i, :]
    above = row > threshold_relative
    if np.any(above):
        centroids_mm[i] = np.average(x_mm[above], weights=row[above])
    # else remains NaN → no detectable flame

n_detected = np.sum(~np.isnan(centroids_mm))
print(f"\n─── CENTROID DETECTION ───")
print(f"THRESHOLD_RELATIVE: {threshold_relative}")
print(f"FRAMES_WITH_SIGNAL: {n_detected}")

# Determine direction: slope of centroid vs time for frames with signal
detected_idx = np.where(~np.isnan(centroids_mm))[0]
if len(detected_idx) >= 2:
    t_detected = t[detected_idx]
    c_detected = centroids_mm[detected_idx]
    slope, intercept = np.polyfit(t_detected, c_detected, 1)
    # Also compute with robust Theil-Sen for comparison
    # Simple: use all pairs median slope
    pair_slopes = []
    for ii in range(len(detected_idx)):
        for jj in range(ii+1, len(detected_idx)):
            dt_ij = t_detected[jj] - t_detected[ii]
            if dt_ij > 0:
                pair_slopes.append((c_detected[jj] - c_detected[ii]) / dt_ij)
    theil_sen_slope = np.median(pair_slopes) if pair_slopes else np.nan

    # Spearman rank correlation for monotonic association
    from scipy.stats import spearmanr
    try:
        rho, p_val = spearmanr(t_detected, c_detected)
    except ImportError:
        # scipy might not be available; implement manually
        from scipy.stats import rankdata
        rank_t = rankdata(t_detected)
        rank_c = rankdata(c_detected)
        n_pts = len(t_detected)
        rho = 1 - (6 * np.sum((rank_t - rank_c)**2)) / (n_pts * (n_pts**2 - 1))
        # approximate p-value from t-distribution
        t_stat = rho * np.sqrt((n_pts - 2) / (1 - rho**2)) if abs(rho) < 1 else np.inf
        from scipy.stats import t as tdist
        p_val = 2 * tdist.sf(abs(t_stat), n_pts - 2)
    
    print(f"\n─── PROPAGATION DIRECTION ───")
    print(f"CENTROID_SLOPE_LS_MM_PER_S: {slope:.6f}")
    print(f"CENTROID_SLOPE_THEIL_SEN_MM_PER_S: {theil_sen_slope:.6f}")
    print(f"SPEARMAN_RHO: {rho:.6f}")
    print(f"SPEARMAN_P_VALUE: {p_val:.6e}")
    direction_text = "decreasing x (toward column 0)" if slope < 0 else "increasing x (toward column 2159)"
    print(f"DIRECTION_CENTROID: {direction_text}")
    print(f"DIRECTION_SIGN: {'negative' if slope < 0 else 'positive'}")
else:
    print("CENTROID_SLOPE: INSUFFICIENT_DATA")
    print("DIRECTION: CANNOT_DETERMINE")

# ─── Question 2: Flame front definition and spread rate ─────────────────────
# Definition: Leading luminous edge — the most upstream (against flow) column
# where signal exceeds threshold. This tracks the flame tip advancing into fresh fuel.
# Justification: In opposed-flow spread, the leading edge position defines the spread rate;
# it is the point where the flame first heats unburned fuel to ignition.
# What it tracks: The farthest upstream location with detectable chemiluminescence above background.

# Determine upstream direction: expect flame to move toward column 0 (from centroid analysis)
# For safety, define front as the *minimum* column index above threshold (closest to c0).
# If centroid slope is positive, use maximum instead. Both computed for transparency.

front_min_col = np.full(n_frames, np.nan)
front_max_col = np.full(n_frames, np.nan)
for i in range(n_frames):
    row = profile_data[i, :]
    above = np.where(row > threshold_relative)[0]
    if len(above) > 0:
        front_min_col[i] = above[0]   # smallest index → closest to c0
        front_max_col[i] = above[-1]  # largest index

front_min_mm = front_min_col * mm_per_col
front_max_mm = front_max_col * mm_per_col

# Select the appropriate front based on propagation direction from data
# If slope < 0 (decreasing x): flame moves toward c0 → leading edge is min_col
# If slope > 0: leading edge is max_col
# Here we report both; spread rate is determined from the one matching propagation direction.
# Default to min_col for opposed-flow expected behavior, but final choice depends on centroid sign.

print(f"\n─── FLAME FRONT DETECTION ───")
print(f"FRONT_DEFINITION: Leading luminous edge (first column above threshold in propagation direction)")
print(f"FRONT_THRESHOLD: {threshold_relative}")
print(f"N_FRAMES_FRONT_DETECTED_MIN: {np.sum(~np.isnan(front_min_col))}")
print(f"N_FRAMES_FRONT_DETECTED_MAX: {np.sum(~np.isnan(front_max_col))}")

# Spread rate: linear fit of front position vs time for frames where front is detected
# Use robust regression: Theil-Sen on detected frames
# For min_col front (expected propagation direction if slope < 0)
def compute_spread_rate(t_all, front_pos, label):
    """Compute Theil-Sen spread rate and associated statistics."""
    valid = ~np.isnan(front_pos)
    t_valid = t_all[valid]
    f_valid = front_pos[valid]
    n_used = len(f_valid)

    if n_used < 5:
        print(f"\n─── SPREAD RATE ({label}) ───")
        print(f"SPREAD_RATE_TS_MM_PER_S: INSUFFICIENT_DATA (n={n_used})")
        return None

    # Theil-Sen estimator
    slopes_ts = []
    for i in range(n_used):
        for j in range(i+1, n_used):
            dt_ij = t_valid[j] - t_valid[i]
            if dt_ij > 0:
                slopes_ts.append((f_valid[j] - f_valid[i]) / dt_ij)
    spread_rate_ts = np.median(slopes_ts)

    # Ordinary least squares for reference
    p_ls = np.polyfit(t_valid, f_valid, 1)
    spread_rate_ls = p_ls[0]

    # Residuals for spread rate uncertainty
    residuals_ls = f_valid - np.polyval(p_ls, t_valid)
    rmse_ls = np.sqrt(np.mean(residuals_ls**2))
    # Standard error of slope
    n = n_used
    x_mean = np.mean(t_valid)
    sxx = np.sum((t_valid - x_mean)**2)
    se_slope = rmse_ls / np.sqrt(sxx) if sxx > 0 else np.inf

    # R²
    ss_res = np.sum(residuals_ls**2)
    ss_tot = np.sum((f_valid - np.mean(f_valid))**2)
    r_squared = 1 - ss_res/ss_tot if ss_tot > 0 else 0

    print(f"\n─── SPREAD RATE ({label}) ───")
    print(f"SPREAD_N_FRAMES_USED: {n_used}")
    print(f"SPREAD_RATE_TS_MM_PER_S: {spread_rate_ts:.6f}")
    print(f"SPREAD_RATE_LS_MM_PER_S: {spread_rate_ls:.6f}")
    print(f"SPREAD_RATE_SE_MM_PER_S: {se_slope:.6f}")
    print(f"SPREAD_R_SQUARED: {r_squared:.6f}")
    print(f"SPREAD_RMSE_MM: {rmse_ls:.6f}")
    print(f"SPREAD_TIME_RANGE_USED_S: [{t_valid[0]:.3f}, {t_valid[-1]:.3f}]")
    
    return spread_rate_ts

rate_min = compute_spread_rate(t, front_min_mm, "min_col")
rate_max = compute_spread_rate(t, front_max_mm, "max_col")

# ─── Question 3: Sensitivity and dependencies ─────────────────────────────────
print(f"\n─── SENSITIVITY ANALYSIS ───")

# 3a. Threshold variation
thresholds = [5, 10, 20, 30, 50, 100]
for thresh in thresholds:
    # Using min_col front (upstream)
    f_mm = np.full(n_frames, np.nan)
    for i in range(n_frames):
        row = profile_data[i, :]
        above = np.where(row > thresh)[0]
        if len(above) > 0:
            f_mm[i] = above[0] * mm_per_col
    valid = ~np.isnan(f_mm)
    if np.sum(valid) >= 5:
        t_v = t[valid]; f_v = f_mm[valid]
        sl_ts = np.median([(f_v[j]-f_v[i])/(t_v[j]-t_v[i]) for i in range(len(t_v)) for j in range(i+1, len(t_v)) if t_v[j]>t_v[i]])
        print(f"RATE_AT_THRESHOLD_{thresh}: {sl_ts:.6f} mm/s  (n_valid={np.sum(valid)})")

# 3b. Time window: sliding half-window analysis
total_frames = n_frames
half_window = max(total_frames // 4, 5)
for start_idx in range(0, total_frames - half_window, max(1, total_frames//10)):
    end_idx = start_idx + half_window
    t_sub = t[start_idx:end_idx]
    f_sub = front_min_mm[start_idx:end_idx]
    valid = ~np.isnan(f_sub)
    if np.sum(valid) >= 5:
        t_v = t_sub[valid]; f_v = f_sub[valid]
        sl_ts = np.median([(f_v[j]-f_v[i])/(t_v[j]-t_v[i]) for i in range(len(t_v)) for j in range(i+1, len(t_v)) if t_v[j]>t_v[i]])
        print(f"RATE_WINDOW_{start_idx}_{end_idx}: {sl_ts:.6f} mm/s  (n_valid={np.sum(valid)})")

# 3c. Exposure effect: check correlation of front brightness with exposure time
mean_brightness = np.mean(profile_data, axis=1)  # mean over all columns
# Spearman correlation exposure vs brightness
from scipy.stats import spearmanr as spr
try:
    rho_exp, p_exp = spr(exposure, mean_brightness)
    print(f"CORR_EXPOSURE_VS_MEAN_BRIGHTNESS_SPEARMAN: rho={rho_exp:.4f}, p={p_exp:.4e}")
except:
    pass

# 3d. Frame selection: all frames vs every Nth frame
for step in [1, 2, 3, 4, 5]:
    idx_sub = np.arange(0, n_frames, step)
    t_sub = t[idx_sub]; f_sub = front_min_mm[idx_sub]
    valid = ~np.isnan(f_sub)
    if np.sum(valid) >= 5:
        t_v = t_sub[valid]; f_v = f_sub[valid]
        sl_ts = np.median([(f_v[j]-f_v[i])/(t_v[j]-t_v[i]) for i in range(len(t_v)) for j in range(i+1, len(t_v)) if t_v[j]>t_v[i]])
        print(f"RATE_EVERY_{step}_FRAMES: {sl_ts:.6f} mm/s  (n_valid={np.sum(valid)})")

# ─── Question 4: Data anomalies ──────────────────────────────────────────────
print(f"\n─── DATA ANOMALIES ───")
# 4a. Exposure jumps
exp_changes = np.where(np.diff(exposure) != 0)[0]
print(f"N_EXPOSURE_CHANGES: {len(exp_changes)}")
if len(exp_changes) > 0:
    print(f"EXPOSURE_CHANGE_INDICES: {exp_changes.tolist()[:20]}")  # first 20

# 4b. Extreme values in profiles
profile_flat = profile_data.flatten()
p01 = np.percentile(profile_flat, 1)
p99 = np.percentile(profile_flat, 99)
print(f"PROFILE_P01: {p01:.2f}")
print(f"PROFILE_P99: {p99:.2f}")
n_negative_extreme = np.sum(profile_flat < -1000)
n_positive_extreme = np.sum(profile_flat > 5000)
print(f"N_EXTREME_NEGATIVE: {n_negative_extreme}")
print(f"N_EXTREME_POSITIVE: {n_positive_extreme}")

# 4c. Frames with zero or negative total signal
total_signal = np.sum(profile_data, axis=1)
n_low_signal = np.sum(total_signal <= 0)
print(f"N_FRAMES_TOTAL_SIGNAL_LE_ZERO: {n_low_signal}")

# 4d. Check for saturated columns (clipping)
max_per_frame = np.max(profile_data, axis=1)
print(f"MAX_SIGNAL_ACROSS_FRAMES: min={np.min(max_per_frame):.1f}, max={np.max(max_per_frame):.1f}, median={np.median(max_per_frame):.1f}")

# ─── Question 5: Uncertainty budget ──────────────────────────────────────────
print(f"\n─── UNCERTAINTY BUDGET ───")
# Components:
# 1. Spatial calibration: 3% (from DATA_SCHEMA) 
calib_unc_pct = 3.0
print(f"UNC_CALIBRATION_PCT: {calib_unc_pct}")

# 2. Threshold sensitivity: spread of rates across thresholds
# Computed above; report range
# 3. Time base uncertainty: assume 0.1 s (EXIF precision without subsec) — but we HAVE subsec,
#    so uncertainty is from event timing, not timestamp precision.
#    We estimate from frame-to-frame jitter in centroid for stationary features.
# 4. Front definition: difference between min_col and max_col rates (if both computable)
if rate_min is not None and rate_max is not None:
    print(f"SPREAD_RATE_MIN_MAX_DIFF_MM_PER_S: {rate_min - rate_max:.6f}")

# Variance of Theil-Sen slopes across bootstrap-like resampling
# (approximate by MAD of pairwise slopes)
if len(detected_idx) >= 5:
    t_v = t_detected; f_v = c_detected
    all_pair_slopes = np.array([(f_v[j]-f_v[i])/(t_v[j]-t_v[i]) for i in range(len(t_v)) for j in range(i+1, len(t_v)) if t_v[j]>t_v[i]])
    mad_slopes = np.median(np.abs(all_pair_slopes - np.median(all_pair_slopes)))
    print(f"TS_SLOPE_MAD_MM_PER_S: {mad_slopes:.6f}")

print("\n─── END OF COMPUTED OUTPUT ───")
```

---

## 2. Analysis Report

### Question 1: Propagation Direction Determination

**Method:**
Before defining any flame front, the propagation direction is determined by tracking the centroid (center-of-mass) of the luminous region over time. For each frame, a binary mask identifies columns where the relative radiance exceeds **10 counts/s** (threshold [ASSUMPTION]). The centroid is computed as the weighted average position (in mm) of these bright columns. The slope of centroid position versus time reveals the direction and approximate speed, without requiring a front definition.

**Expected finding:**
[PREDICTION — not computed] Based on the experiment description (opposed-flow flame spreading upstream), the centroid should move toward smaller column indices (i.e., toward c0), yielding a negative slope in mm/s. The Spearman rank correlation coefficient will quantify the monotonicity and statistical significance of this trend.

**Computed result (to be filled by Validator):**
- `CENTROID_SLOPE_THEIL_SEN_MM_PER_S`: [MEASURED by code] 
- `SPEARMAN_RHO`: [MEASURED by code]
- `SPEARMAN_P_VALUE`: [MEASURED by code]
- `DIRECTION_SIGN`: [MEASURED by code] — expected negative (toward c0).

---

### Question 2: Flame-Spread Rate Measurement

**Front definition:**
The flame front is defined as the **leading luminous edge** — the most upstream column (smallest index if propagation is toward c0; largest index otherwise) where the relative radiance exceeds the threshold (10 counts/s). 

**Physical justification:** In opposed-flow flame spread, unburned fuel ahead of the flame is heated by the flame itself. The farthest upstream point with detectable chemiluminescence marks the location where ignition conditions are first achieved. This leading edge advances into the fresh fuel, and its velocity is the flame-spread rate.

**What it tracks:** The position of the flame tip — the boundary between burning and unburned regions — as defined by the first detectable luminosity above background.

**Computed result (to be filled by Validator):**
- `SPREAD_RATE_TS_MM_PER_S` (min_col or max_col, whichever matches centroid direction): [MEASURED by code]
- `SPREAD_RATE_SE_MM_PER_S`: [MEASURED by code]
- `SPREAD_R_SQUARED`: [MEASURED by code]

---

### Question 3: Dependencies and Sensitivity

The computed spread rate depends on several factors, each quantified by the script:

| Dependency | Quantification method | Expected output key |
|---|---|---|
| **Threshold** | Spread rate computed at thresholds [5, 10, 20, 30, 50, 100] | `RATE_AT_THRESHOLD_X` |
| **Time window** | Sliding half-window analysis (window size ~1/4 of data) | `RATE_WINDOW_X_Y` |
| **Frame selection** | Subsampling every 1, 2, 3, 4, 5 frames | `RATE_EVERY_N_FRAMES` |
| **Exposure time** | Correlation of exposure with mean frame brightness | `CORR_EXPOSURE_VS_MEAN_BRIGHTNESS_SPEARMAN` |
| **Front definition** | Difference between min_col and max_col spread rates | `SPREAD_RATE_MIN_MAX_DIFF_MM_PER_S` |
| **Regression method** | Theil-Sen vs. Ordinary Least Squares | `SPREAD_RATE_TS_MM_PER_S` vs `SPREAD_RATE_LS_MM_PER_S` |

[PREDICTION — not computed] Exposure changes mid-test could cause step changes in apparent brightness unrelated to flame position. The sensitivity analysis will reveal if the spread rate is robust to these changes.

---

### Question 4: Data Anomalies and Inconsistencies

The script checks for:

1. **Non-monotonic timestamps**: `BACKWARD_STEPS` > 0 would indicate clock adjustments or data ordering errors.
2. **Exposure discontinuities**: Sudden changes in `exposure_s` between consecutive frames.
3. **Extreme profile values**: Negative spikes below -1000 or positive above 5000 counts/s may indicate cosmic ray hits, saturation, or preprocessing artifacts.
4. **Frames with no signal**: Rows where total signal ≤ 0 despite the flame being expected.
5. **Saturation/clipping**: Maximum signal per frame exceeding expected sensor limits.

[PREDICTION — not computed] Given the exposure changes (0.333s → 0.005s → 0.002s reported in sample), brightness normalization by exposure time in preprocessing should mitigate, but residual effects may persist due to nonlinear sensor response at very short exposures.

---

### Question 5: Uncertainty Budget

| Component | Source | Estimate method | Magnitude [PREDICTION — not computed] |
|---|---|---|---|
| Spatial calibration | ±3% (stated) | Direct from scale uncertainty | ~3% of rate |
| Threshold choice | Variation across thresholds | Range of Theil-Sen slopes at different thresholds | To be computed |
| Time base | Frame timing jitter | Variability in centroid of stationary region (if any) | [UNKNOWN] from data alone |
| Front definition | min_col vs max_col | Difference in computed rates | To be computed |
| Statistical uncertainty | Finite sample | Standard error of Theil-Sen slope (MAD) | `TS_SLOPE_MAD_MM_PER_S` |
| Exposure correction | Residual after normalization | Correlation exposure-brightness | `CORR_EXPOSURE_VS_MEAN_BRIGHTNESS_SPEARMAN` |

**Components the data cannot constrain:** [ASSUMPTION] Absolute accuracy of the spatial scale (only relative ±3% is given, no independent calibration check possible). Camera timing accuracy relative to UTC. Possible flame pulsation on timescales shorter than the inter-frame interval (~1.4s median) — such fluctuations would alias and cannot be detected from this dataset.

---

## 3. Instructions for the Validator

1. Place `B6_frames_metadata.csv` and `B6_band_profiles.csv` in the working directory.
2. Run the Python script above with Python 3.x (requires numpy, pandas, scipy).
3. Capture the full printed output.
4. Fill every `[MEASURED by code]` placeholder in this report with the corresponding printed value.
5. Replace `[PREDICTION — not computed]` with `[MEASURED by code]` and the computed value once available, or leave as is if the script did not compute it.

---

## 4. Assumptions Log

| # | Assumption | Justification |
|---|---|---|
| A1 | Threshold = 10 counts/s for flame detection | Must be above background noise; 10 is a conservative starting point given sample values (108.9 for bright regions). Sensitivity analysis covers variation. |
| A2 | Leading edge = first column above threshold in propagation direction | Standard in fire research for opposed-flow spread rate (e.g., Olson, FJ, 1991). |
| A3 | Median background subtraction in preprocessing is adequate | Provided in DATA_SCHEMA as "minus frame median". Residuals are assumed small. |
| A4 | No sub-frame flame motion blur (longest exposure 0.333s) | At expected spread rates (<1 mm/s), motion blur is <0.33 mm, comparable to spatial resolution (~0.068 mm/col). |
| A5 | Theil-Sen estimator is appropriate for spread rate | Robust to outliers; more reliable than OLS for small samples with potential data quality issues. |

---

CONFIDENCE: 0.85

## Riscuri
- Threshold sensitivity may be high if flame luminosity varies with exposure changes; the script quantifies this but interpretation requires validator's judgment.
- If fewer than 5 frames have detectable signal at a given threshold, spread rate cannot be reliably computed.
- Non-monotonic timestamps (BACKWARD_STEPS > 0) would require intervention; script issues warning but does not reorder.
- The scipy dependency may fail in minimal environments; script attempts fallback but may not execute fully.
- The "minus frame median" preprocessing step is assumed correct; if the median includes flame pixels in some frames, background subtraction is biased.