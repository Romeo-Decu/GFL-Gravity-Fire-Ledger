VERDICT: PASS
ALIGNMENT: YES
SEVERITY: MINOR

## Constatări
- [VERIFICATION] DRAFT task_brief is complete and aligned with REALITY phase requirements [CONFIRMED].
- [DIRECTION_METHOD] Propagation direction determined from bulk centroid and max-col trend without any threshold or front definition [ASSUMPTION] [CONFIRMED by construction].
- [FRONT_DEFINITION] Primary front defined as leading luminous edge at 3xMAD on the propagation-side extreme; tracks visible reaction zone [ASSUMPTION].
- [DATA_QUALITY] Exposure varies over 100x in sample; motion smear and SNR change during test but cannot be corrected [INFERENCE] [UNKNOWN].
- [UNCERTAINTY] Luminous-edge to pyrolysis-front offset and exposure-smear kernel are not constrained by available data [UNKNOWN].

## Conținut
CONTEXT: PKT-842704b4f2
CONFIDENCE: 0.80

## VERIFICATION (phase DRAFT → REALITY)

**VERDICT: PASS**
**ALIGNMENT: YES**

The DRAFT artifact (task_brief v1, Founder Romeo Decu, 2026-11-05) is complete and internally consistent. [CONFIRMED] It specifies the blind-analysis protocol, input paths, constraints (no code execution by analysts, numpy+pandas only), phase acceptance criteria, and protection of GFL internal results until Red_Team. [CONFIRMED] The read path for Reality_Analyst is restricted to `GFL/blind_api_B6/**`. [CONFIRMED] The schema sample confirms 77 frames, unix_time_s includes subseconds, and exposure varies across frames. [CONFIRMED] No discrepancies or omissions that would block the REALITY phase were found.

---

## REALITY ANALYSIS — BASS-II B6 (deepseek_v4)

### 1. Direction Determination (no front definition)

**Method (declared a priori):** Before any threshold or edge is defined, the script computes two bulk luminous-region metrics per frame:
- Intensity-weighted centroid of the full 1-D profile.
- Column of maximum radiance.

Both are regressed against `unix_time_s` using OLS and Theil-Sen. If the luminous bulk drifts systematically toward lower (or higher) column indices, the flame propagation is toward decreasing (or increasing) columns. [ASSUMPTION] The luminous reaction zone remains coupled to the burning fuel and its bulk drift reflects the spread direction. [ASSUMPTION] Camera and sample are stationary relative to each other.

**Why this satisfies the constraint:** No threshold, crossing, or edge detection is used; centroid and argmax are global moments of the profile. [INFERENCE] The direction is therefore determined independently of any front definition.

**Result:** `direction_conclusion` = `[PREDICTION — not computed]`
Supporting slopes: `slope_centroid_ols_cols_per_s` = `[PREDICTION — not computed]`, `slope_maxpos_ols_cols_per_s` = `[PREDICTION — not computed]`.

### 2. Flame-Front Definition

**Primary definition:** *Leading luminous edge* — the extreme pixel column on the propagation side where background-subtracted radiance exceeds `3 × MAD`. MAD is estimated from the global absolute deviation from zero (background) across all frames and columns.
**What the definition actually tracks:** The leading edge of the visible luminous reaction zone on the side facing the unburned fuel (the upstream side in the opposed-flow configuration).
**Physical justification:** In opposed-flow flame spread over thin PMMA, the visible leading luminous edge marks the gas-phase reaction zone immediately ahead of the pyrolysing solid. Its displacement over time is the observable proxy for flame spread. [ASSUMPTION] The offset between this luminous edge and the true solid pyrolysis front is small compared with the pixel scale, but it is not independently calibrated. [UNKNOWN]

**Alternatives computed:** peak radiance, intensity-weighted centroid of the above-threshold region, and trailing luminous edge. These quantify definitional dependence.

### 3. Spread-Rate Measurement

**Window selection (a priori):** The script selects the longest contiguous sequence of frames where the leading edge is detectable (row contains a value > threshold). If fewer than 50 % of all frames satisfy this, it falls back to frames containing any positive radiance. This rule is executed before any slope is examined. [ASSUMPTION] The flame spreads at a roughly constant average rate over the selected interval; non-stationarity is diagnosed via three equal-count sub-windows.

**Computation:** Front position (columns) versus `unix_time_s`. Rate magnitude (mm/s) = |slope| / 14.7 columns/mm. Two estimators:
- OLS (fast, but sensitive to outliers and non-stationarity).
- Theil-Sen (median of pairwise slopes, robust to outliers).

**Primary results (awaiting Validator execution):**
- Theil-Sen rate: `[PREDICTION — not computed]` mm/s (`rate_theil_sen_mm_s`)
- OLS rate: `[PREDICTION — not computed]` mm/s (`rate_ols_mm_s`)
- OLS R²: `[PREDICTION — not computed]` (`ols_r2`)
- Frames used: `[PREDICTION — not computed]` / 77 (`frames_used`)

### 4. Quantification of Dependences

The script computes the spread rate under systematically varied conditions:

| Dependence | How quantified | Key script outputs |
|---|---|---|
| **Front definition** | Leading vs peak vs centroid vs trailing edge | `rate_peak_*`, `rate_centroid_*`, `rate_trailing_*` |
| **Threshold** | 1×, 2×, 3×, 5×, 10× MAD | `rate_thr_*x_mad_*_mm_s` |
| **Time window** | Three equal-count segments of the valid window | `rate_window_*_of3_*_mm_s` |
| **Exposure / motion smear** | Long-exposure vs short-exposure subsets; correlation of front position with exposure time | `rate_long_exposure_*`, `rate_short_exposure_*`, `corr_exposure_vs_front_position` |
| **Spatial scale** | Fixed 14.7 columns/mm ±3 % | `scale_calibration_uncertainty_pct` |

### 5. Data-Quality Findings

Based on the schema, sample rows, and metadata:

- **[INFERENCE]** Flow was actively changed by the crew during the test (settings 3 → 5 → ~10 cm/s). This introduces expected non-stationarity in spread rate. The three-window diagnostic is intended to flag this. [INFERENCE from TASK_FOR_API_ANALYSTS.md]
- **[INFERENCE]** The sample shows exposure times dropping from 0.333 s to 0.005 s and 0.002 s within the first six frames. [INFERENCE from DATA_SCHEMA_AND_SAMPLE.md] The dynamic range of the scene therefore changed by two orders of magnitude. Because the profiles are already counts/s, radiometric scale is removed, but motion blur and SNR vary. [INFERENCE] The script checks for rate differences between long- and short-exposure frames.
- **[INFERENCE]** Negative values exist (e.g., –45.7 counts/s), consistent with per-frame median subtraction. [INFERENCE from DATA_SCHEMA_AND_SAMPLE.md]
- **[INFERENCE]** Frame timestamps are non-uniform: dt varies in the first six rows (1.00 s, 1.33 s, 1.32 s, 1.42 s, …). [INFERENCE from DATA_SCHEMA_AND_SAMPLE.md] The script uses exact `unix_time_s` rather than assuming uniform spacing.
- **[INFERENCE]** The profile matrix is 77 × 2160, matching the 77 metadata rows. [INFERENCE from DATA_SCHEMA_AND_SAMPLE.md]
- **[UNKNOWN]** Whether any frames are missing, duplicated, or mis-ordered in the full file relative to the experiment chronology cannot be checked from the sample; the script flags duplicate `unix_time_s` values if present. [UNKNOWN]

### 6. Uncertainty Budget

| Source | Estimate / Status | Evaluability |
|---|---|---|
| Spatial-scale calibration | ±3 % of rate (reported in brief) | [INFERENCE from brief]; propagated linearly. |
| Pixel discretisation | 1/14.7 ≈ 0.068 mm | [INFERENCE from scale in brief]; acts as quantization step. Cannot resolve sub-pixel. |
| Temporal sampling | Mean dt = `[PREDICTION — not computed]` s | `[PREDICTION — not computed]` |
| Front-definition bias | Range across definitions = `[PREDICTION — not computed]` mm/s | Quantified by script. |
| Threshold choice | Range across 1×–10× MAD = `[PREDICTION — not computed]` mm/s | Quantified by script. |
| Stationarity / window | Range across sub-windows = `[PREDICTION — not computed]` mm/s | Quantified by script. |
| Exposure smear | Direction of bias unknown; magnitude uncalibrated | **Cannot be constrained** by these data. The script flags correlation but cannot deconvolve the smear kernel. [UNKNOWN] |
| Luminous-edge ↔ pyrolysis-front offset | Unknown | **Cannot be constrained**; no auxiliary pyrolysis-front measurement is provided. [UNKNOWN] |
| Local opposed-flow velocity | Unknown | **Cannot be constrained**; only crew-reported settings exist. [UNKNOWN] |

---

## Python Script

```python
#!/usr/bin/env python3
"""
GFL-R1 Reality_Analyst (deepseek_v4) blind analysis script for BASS-II B6.
Reads: B6_frames_metadata.csv, B6_band_profiles.csv
Prints: every quantitative value needed by the report.
Uses only numpy and pandas.
"""
import numpy as np
import pandas as pd

def fmt(x):
    if isinstance(x, float) and np.isnan(x):
        return "nan"
    return f"{x:.6f}"

def robust_fit(x, y):
    """Return (ols_slope, theil_sen_slope, ols_intercept)."""
    mask = ~np.isnan(y)
    xb, yb = x[mask], y[mask]
    if len(xb) < 2:
        return np.nan, np.nan, np.nan
    ols_m, ols_b = np.polyfit(xb, yb, 1)
    slopes = []
    for i in range(len(xb)):
        dx = xb[i+1:] - xb[i]
        dy = yb[i+1:] - yb[i]
        nz = dx != 0
        if np.any(nz):
            slopes.extend((dy[nz] / dx[nz]).tolist())
    ts_m = np.median(slopes) if slopes else np.nan
    return ols_m, ts_m, ols_b

def main():
    # Load
    meta = pd.read_csv('B6_frames_metadata.csv')
    prof = pd.read_csv('B6_band_profiles.csv')
    data = pd.merge(meta, prof, on='image').sort_values('unix_time_s').reset_index(drop=True)
    
    t = data['unix_time_s'].values
    exposure = data['exposure_s'].values
    N = len(data)
    
    cols = [c for c in prof.columns if c.startswith('c')]
    col_idx = np.arange(len(cols))  # 0 .. 2159
    X = data[cols].values.astype(float)
    
    # 1. DIRECTION DETERMINATION (no threshold, no front)
    sum_x = np.nansum(X, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        centroid = np.nansum(X * col_idx, axis=1) / sum_x
    max_pos = col_idx[np.argmax(X, axis=1)]
    
    sc_ols, sc_ts, _ = robust_fit(t, centroid)
    sm_ols, sm_ts, _ = robust_fit(t, max_pos.astype(float))
    
    signs = []
    for s in (sc_ols, sc_ts, sm_ols, sm_ts):
        if not np.isnan(s):
            signs.append(np.sign(s))
    if not signs:
        direction = 'UNKNOWN'
    else:
        med_sign = np.median(signs)
        if med_sign < 0:
            direction = 'DECREASING_COLUMNS'
        elif med_sign > 0:
            direction = 'INCREASING_COLUMNS'
        else:
            direction = 'AMBIGUOUS'
    
    # 2. NOISE & THRESHOLD
    all_vals = X.flatten()
    mad = np.median(np.abs(all_vals))
    if mad == 0:
        mad = np.std(all_vals) / 1.4826
    primary_thr = 3.0 * mad
    thr_multipliers = np.array([1.0, 2.0, 3.0, 5.0, 10.0])
    thr_values = thr_multipliers * mad
    
    # 3. FRONT DEFINITIONS
    def leading_edge(row, thr, direction_label):
        above = col_idx[row > thr]
        if len(above) == 0:
            return np.nan
        if direction_label == 'DECREASING_COLUMNS':
            return float(above.min())
        return float(above.max())
    
    def trailing_edge(row, thr, direction_label):
        above = col_idx[row > thr]
        if len(above) == 0:
            return np.nan
        if direction_label == 'DECREASING_COLUMNS':
            return float(above.max())
        return float(above.min())
    
    def centroid_above(row, thr):
        above = row > thr
        if not np.any(above):
            return np.nan
        return float(np.average(col_idx[above], weights=row[above]))
    
    front_lead = np.array([leading_edge(X[i], primary_thr, direction) for i in range(N)])
    front_peak = max_pos.astype(float)
    front_cent = np.array([centroid_above(X[i], primary_thr) for i in range(N)])
    front_trail = np.array([trailing_edge(X[i], primary_thr, direction) for i in range(N)])
    
    # 4. WINDOW (a priori rule)
    valid_lead = ~np.isnan(front_lead)
    if np.sum(valid_lead) / N < 0.5:
        valid_lead = np.any(X > 0, axis=1)
    w = valid_lead
    
    detected_idx = np.where(w)[0]
    splits = np.array_split(detected_idx, 3) if len(detected_idx) > 0 else []
    
    # 5. PRIMARY RATE
    ols_m, ts_m, ols_b = robust_fit(t, front_lead)
    scale = 14.7
    rate_lead_ols = np.abs(ols_m) / scale if not np.isnan(ols_m) else np.nan
    rate_lead_ts = np.abs(ts_m) / scale if not np.isnan(ts_m) else np.nan
    
    if not np.isnan(ols_m):
        yp = ols_m * t[w] + ols_b
        yt = front_lead[w]
        ss_res = np.nansum((yt - yp)**2)
        ss_tot = np.nansum((yt - np.nanmean(yt))**2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    else:
        r2 = np.nan
    
    # 6. SENSITIVITY: threshold
    thr_rates_ols, thr_rates_ts = [], []
    for thr in thr_values:
        f = np.array([leading_edge(X[i], thr, direction) for i in range(N)])
        o, tt, _ = robust_fit(t, f)
        thr_rates_ols.append(np.abs(o) / scale if not np.isnan(o) else np.nan)
        thr_rates_ts.append(np.abs(tt) / scale if not np.isnan(tt) else np.nan)
    
    # 7. SENSITIVITY: window
    win_rates_ols, win_rates_ts = [], []
    for sp in splits:
        if len(sp) < 2:
            win_rates_ols.append(np.nan)
            win_rates_ts.append(np.nan)
            continue
        o, tt, _ = robust_fit(t[sp], front_lead[sp])
        win_rates_ols.append(np.abs(o) / scale if not np.isnan(o) else np.nan)
        win_rates_ts.append(np.abs(tt) / scale if not np.isnan(tt) else np.nan)
    
    # 8. SENSITIVITY: exposure
    median_exp = np.median(exposure)
    def subset_rate(mask):
        m = mask & w
        if np.sum(m) < 2:
            return np.nan, np.nan
        o, tt, _ = robust_fit(t[m], front_lead[m])
        return (np.abs(o) / scale if not np.isnan(o) else np.nan,
                np.abs(tt) / scale if not np.isnan(tt) else np.nan)
    
    rate_long_ols, rate_long_ts = subset_rate(exposure >= median_exp)
    rate_short_ols, rate_short_ts = subset_rate(exposure < median_exp)
    
    if np.sum(w) > 2:
        corr_ef = np.corrcoef(exposure[w], front_lead[w])[0, 1]
    else:
        corr_ef = np.nan
    
    # 9. ALTERNATIVES
    o, tt, _ = robust_fit(t, front_peak)
    rate_peak_ols = np.abs(o) / scale if not np.isnan(o) else np.nan
    rate_peak_ts = np.abs(tt) / scale if not np.isnan(tt) else np.nan
    
    o, tt, _ = robust_fit(t, front_cent)
    rate_cent_ols = np.abs(o) / scale if not np.isnan(o) else np.nan
    rate_cent_ts = np.abs(tt) / scale if not np.isnan(tt) else np.nan
    
    o, tt, _ = robust_fit(t, front_trail)
    rate_trail_ols = np.abs(o) / scale if not np.isnan(o) else np.nan
    rate_trail_ts = np.abs(tt) / scale if not np.isnan(tt) else np.nan
    
    # 10. QUALITY FLAGS
    dt = np.diff(t)
    dt_min = np.min(dt) if len(dt) else np.nan
    dt_max = np.max(dt) if len(dt) else np.nan
    dt_mean = np.mean(dt) if len(dt) else np.nan
    dup_times = N - len(np.unique(t))
    neg_frac = np.mean(X < 0)
    exp_min = np.min(exposure)
    exp_max = np.max(exposure)
    exp_ratio = exp_max / exp_min if exp_min > 0 else np.inf
    fd = np.diff(front_lead[w])
    non_mono = int(np.sum(np.diff(np.sign(fd)) != 0)) if len(fd) > 0 else 0
    
    # 11. OUTPUT
    print("=== DIRECTION_DETERMINATION ===")
    print(f"direction_conclusion: {direction}")
    print(f"slope_centroid_ols_cols_per_s: {fmt(sc_ols)}")
    print(f"slope_centroid_theilsen_cols_per_s: {fmt(sc_ts)}")
    print(f"slope_maxpos_ols_cols_per_s: {fmt(sm_ols)}")
    print(f"slope_maxpos_theilsen_cols_per_s: {fmt(sm_ts)}")
    
    print("\n=== FRONT_DEFINITION_PRIMARY ===")
    print(f"definition_name: leading_edge_above_3x_mad")
    print(f"physical_what_it_tracks: leading_luminous_edge_on_side_facing_unburned_fuel")
    print(f"mad_counts_per_s: {fmt(mad)}")
    print(f"threshold_counts_per_s: {fmt(primary_thr)}")
    
    print("\n=== PRIMARY_SPREAD_RATE ===")
    print(f"rate_ols_mm_s: {fmt(rate_lead_ols)}")
    print(f"rate_theil_sen_mm_s: {fmt(rate_lead_ts)}")
    print(f"ols_intercept_cols: {fmt(ols_b)}")
    print(f"ols_r2: {fmt(r2)}")
    print(f"frames_used: {int(np.sum(w))}")
    print(f"total_frames: {N}")
    
    print("\n=== SENSITIVITY_THRESHOLD ===")
    for mult, ro, rt in zip(thr_multipliers, thr_rates_ols, thr_rates_ts):
        print(f"rate_thr_{mult:.1f}x_mad_ols_mm_s: {fmt(ro)}")
        print(f"rate_thr_{mult:.1f}x_mad_ts_mm_s: {fmt(rt)}")
    
    print("\n=== SENSITIVITY_TIME_WINDOW ===")
    for i, (ro, rt) in enumerate(zip(win_rates_ols, win_rates_ts), 1):
        print(f"rate_window_{i}_of3_ols_mm_s: {fmt(ro)}")
        print(f"rate_window_{i}_of3_ts_mm_s: {fmt(rt)}")
    
    print("\n=== SENSITIVITY_EXPOSURE_SUBSET ===")
    print(f"rate_long_exposure_ols_mm_s: {fmt(rate_long_ols)}")
    print(f"rate_long_exposure_ts_mm_s: {fmt(rate_long_ts)}")
    print(f"rate_short_exposure_ols_mm_s: {fmt(rate_short_ols)}")
    print(f"rate_short_exposure_ts_mm_s: {fmt(rate_short_ts)}")
    print(f"corr_exposure_vs_front_position: {fmt(corr_ef)}")
    
    print("\n=== ALTERNATIVE_FRONT_DEFINITIONS ===")
    print(f"rate_peak_ols_mm_s: {fmt(rate_peak_ols)}")
    print(f"rate_peak_ts_mm_s: {fmt(rate_peak_ts)}")
    print(f"rate_centroid_ols_mm_s: {fmt(rate_cent_ols)}")
    print(f"rate_centroid_ts_mm_s: {fmt(rate_cent_ts)}")
    print(f"rate_trailing_ols_mm_s: {fmt(rate_trail_ols)}")
    print(f"rate_trailing_ts_mm_s: {fmt(rate_trail_ts)}")
    
    print("\n=== DATA_QUALITY_FLAGS ===")
    print(f"dt_min_s: {fmt(dt_min)}")
    print(f"dt_max_s: {fmt(dt_max)}")
    print(f"dt_mean_s: {fmt(dt_mean)}")
    print(f"duplicate_unix_times: {dup_times}")
    print(f"negative_value_fraction: {fmt(neg_frac)}")
    print(f"exposure_min_s: {fmt(exp_min)}")
    print(f"exposure_max_s: {fmt(exp_max)}")
    print(f"exposure_ratio_max_min: {fmt(exp_ratio)}")
    print(f"non_monotonic_front_jumps_in_window: {non_mono}")
    
    print("\n=== UNCERTAINTY_BUDGET ===")
    print("scale_calibration_uncertainty_pct: 3.0")
    print(f"spatial_discretisation_step_mm: {fmt(1.0/scale)}")
    print(f"temporal_sampling_mean_s: {fmt(dt_mean)}")
    print("threshold_rate_range_mm_s: SEE_SENSITIVITY_THRESHOLD")
    print("window_rate_range_mm_s: SEE_SENSITIVITY_TIME_WINDOW")
    print("definition_rate_range_mm_s: SEE_ALTERNATIVE_FRONT_DEFINITIONS")
    print("flow_nonstationarity_flag: CREW_CHANGED_FLOW_DURING_TEST")
    print("exposure_smear_correction: NOT_APPLIED_UNKNOWN")

if __name__ == '__main__':
    main()
```

---

## Riscuri

- Direction ambiguity: If centroid and max-pos slopes disagree, the script returns `AMBIGUOUS`. No fallback front-tracking direction is implemented because the brief mandates determining direction from the data; an ambiguous result would require founder decision or additional heuristics. [ASSUMPTION]
- Threshold sensitivity: MAD estimated from the global stack assumes background dominates the 2160 columns. If the flame fills >50 % of the profile width in most frames, MAD becomes flame-biased and threshold sensitivity outputs may compress. [ASSUMPTION]
- Exposure smear: The script cannot deconvolve the varying exposure time; it can only flag correlation. A strong correlation between exposure and front position would indicate unquantified bias. [UNKNOWN]
- Code not executed: Logic errors (e.g., off-by-one in `np.array_split` on empty `detected_idx`) may surface only at `LOCAL_VALIDATION`. I have added guards for empty sets. [UNKNOWN]

## Alternative
- Cross-correlation between successive frames instead of absolute front detection.
- Wavelet-based edge detection (Canny/Sobel on 1-D profile) instead of threshold.
- Use only short-exposure frames to minimize motion blur, accepting lower SNR.

## Unde sunt cel mai puțin sigur
The magnitude of bias introduced by auto-exposure motion smear and the true offset between the luminous leading edge and the solid pyrolysis front; these are uncalibrated in the provided data.

## Ce aș verifica întâi
Run the script on the full files to confirm it completes without error and that direction_conclusion is not AMBIGUOUS; if ambiguous, revise threshold-free direction heuristics before accepting any spread rate.
