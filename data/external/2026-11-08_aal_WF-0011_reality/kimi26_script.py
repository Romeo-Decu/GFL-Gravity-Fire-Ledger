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
