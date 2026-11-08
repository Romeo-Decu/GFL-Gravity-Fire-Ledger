import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.signal import correlate

def main():
    # Load data
    meta = pd.read_csv('B6_frames_metadata.csv')
    profiles = pd.read_csv('B6_band_profiles.csv')
    
    # Merge on image name to ensure alignment
    df = meta.copy()
    profile_cols = [c for c in profiles.columns if c.startswith('c')]
    # Ensure same row ordering
    assert all(df['image'].values == profiles['image'].values), "Mismatch between metadata and profiles row order"
    
    # Extract time and exposure info
    t = df['unix_time_s'].values
    exposure = df['exposure_s'].values
    
    # Extract profile matrix (77 rows x 2160 cols)
    prof_matrix = profiles[profile_cols].values  # this is already in counts/s per schema
    n_frames, n_cols = prof_matrix.shape
    
    # Spatial calibration
    col_per_mm = 14.7
    mm_per_col = 1.0 / col_per_mm
    
    # ---------- Direction determination via cross-correlation ----------
    direction_lags = []
    for i in range(n_frames - 1):
        # Use full profiles
        sig1 = prof_matrix[i]
        sig2 = prof_matrix[i+1]
        # Remove mean to avoid offset correlation
        sig1 = sig1 - np.mean(sig1)
        sig2 = sig2 - np.mean(sig2)
        corr = correlate(sig1, sig2, mode='same')
        lags = np.arange(-n_cols//2 + 1, n_cols//2 + 1)
        max_idx = np.argmax(corr)
        lag = lags[max_idx]
        direction_lags.append(lag)
    
    mean_lag = np.mean(direction_lags)
    # Positive lag means signal2 is shifted to the right relative to signal1 (i.e., towards higher columns).
    # Negative lag means motion towards decreasing columns.
    if mean_lag < 0:
        direction_text = "decreasing column index (upstream with respect to air flow)"
    elif mean_lag > 0:
        direction_text = "increasing column index (downstream)"
    else:
        direction_text = "no net motion detected"
    print(f"DIRECTION_MEAN_LAG={mean_lag:.2f}")
    print(f"DIRECTION_INTERPRETATION: Motion is towards {direction_text}")
    
    # ---------- Front detection ----------
    # For each frame, find the leading edge from the right (high column index) towards left
    # We define the search zone: ignore boundaries where edge effects can exist
    search_start_col = n_cols - 100  # 100 columns from right edge
    search_end_col = 50               # stop at column 50
    
    def detect_front(profile, threshold_frac=0.10):
        # Find peak in search zone
        search_zone = profile[search_end_col:search_start_col]
        if np.max(search_zone) <= 0:
            return np.nan
        peak_val = np.max(search_zone)
        thresh_val = threshold_frac * peak_val
        # Find first pixel from right (high index) that exceeds threshold
        for col in range(search_start_col-1, search_end_col-1, -1):
            if profile[col] >= thresh_val:
                return col
        return np.nan
    
    base_threshold = 0.10
    positions_px = np.array([detect_front(prof_matrix[i], base_threshold) for i in range(n_frames)])
    # Convert to mm (reverse coordinate: smaller pixel index means upstream)
    positions_mm = (n_cols - positions_px) * mm_per_col  # distance from right edge? 
    # Better: define origin at column 0 (upstream end). 
    # Motion towards lower columns means distance_increase if measured from column N, but we just need slope.
    # Use coordinate: distance from column 2159 towards 0 is negative slope vs time if motion towards lower columns.
    # For simplicity, define 'upstream position' = position_px * mm_per_col (distance from column 0).
    # If it moves towards lower columns, this value decreases over time.
    upstream_pos_mm = positions_px * mm_per_col
    
    valid = ~np.isnan(upstream_pos_mm)
    t_valid = t[valid]
    pos_valid = upstream_pos_mm[valid]
    
    print(f"VALID_FRAMES={np.sum(valid)}/{n_frames}")
    print(f"MEAN_POSITION_MM={np.mean(pos_valid):.2f}")
    
    # ---------- Spread rate linear fit ----------
    if np.sum(valid) < 5:
        print("ERROR: Too few valid front detections")
        return
    
    # Fit linear model: pos = a*t + b
    t_mean = np.mean(t_valid)
    p_mean = np.mean(pos_valid)
    # Use time relative to first valid frame to avoid large intercept
    t_rel = t_valid - t_valid[0]
    # Linear regression
    A = np.vstack([t_rel, np.ones_like(t_rel)]).T
    coeff, residuals, rank, s = np.linalg.lstsq(A, pos_valid, rcond=None)
    spread_rate_mm_s = coeff[0]  # slope
    intercept_mm = coeff[1]
    
    # Compute R²
    pos_pred = np.dot(A, coeff)
    ss_res = np.sum((pos_valid - pos_pred)**2)
    ss_tot = np.sum((pos_valid - p_mean)**2)
    r_squared = 1 - ss_res / ss_tot
    
    print(f"BASE_THRESHOLD={base_threshold}")
    print(f"SPREAD_RATE_MM_S={spread_rate_mm_s:.4f}")
    print(f"INTERCEPT_MM={intercept_mm:.2f}")
    print(f"R_SQUARED={r_squared:.4f}")
    print(f"N_FRAMES_USED={np.sum(valid)}")
    
    # Sensitivity: different thresholds
    thresholds = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    rates = []
    for th in thresholds:
        pos_th = np.array([detect_front(prof_matrix[i], th) for i in range(n_frames)])
        up = pos_th * mm_per_col
        v = ~np.isnan(up)
        if np.sum(v) < 5:
            rates.append(np.nan)
            continue
        t_rel_th = t[v] - t[v][0]
        A_th = np.vstack([t_rel_th, np.ones_like(t_rel_th)]).T
        coeff_th, _, _, _ = np.linalg.lstsq(A_th, up[v], rcond=None)
        rates.append(coeff_th[0])
        print(f"THRESHOLD_{th}_RATE={coeff_th[0]:.4f}")
    
    valid_rates = [r for r in rates if not np.isnan(r)]
    if valid_rates:
        print(f"RATE_MEAN_ACROSS_THRESHOLDS={np.mean(valid_rates):.4f} mm/s")
        print(f"RATE_STD_ACROSS_THRESHOLDS={np.std(valid_rates):.4f} mm/s")
    
    # Sensitivity: different time windows
    # First half vs second half
    midpoint = len(t_valid) // 2
    for half_name, t_half, pos_half in [('FIRST_HALF', t_valid[:midpoint], pos_valid[:midpoint]),
                                        ('SECOND_HALF', t_valid[midpoint:], pos_valid[midpoint:])]:
        if len(t_half) < 3:
            continue
        t_rel_h = t_half - t_half[0]
        A_h = np.vstack([t_rel_h, np.ones_like(t_rel_h)]).T
        coeff_h, _, _, _ = np.linalg.lstsq(A_h, pos_half, rcond=None)
        print(f"{half_name}_RATE={coeff_h[0]:.4f} mm/s")
    
    # Test for break point: piecewise linear fit with break at frame 38 (approx middle)
    break_idx = n_frames // 2
    t1 = t_valid[:break_idx]
    t2 = t_valid[break_idx:]
    p1 = pos_valid[:break_idx]
    p2 = pos_valid[break_idx:]
    if len(t1) >= 3 and len(t2) >= 3:
        t_rel1 = t1 - t1[0]
        A1 = np.vstack([t_rel1, np.ones_like(t_rel1)]).T
        c1, _, _, _ = np.linalg.lstsq(A1, p1, rcond=None)
        t_rel2 = t2 - t2[0]
        A2 = np.vstack([t_rel2, np.ones_like(t_rel2)]).T
        c2, _, _, _ = np.linalg.lstsq(A2, p2, rcond=None)
        print(f"BREAK_AT_FRAME_{break_idx}_RATE1={c1[0]:.4f} mm/s")
        print(f"BREAK_AT_FRAME_{break_idx}_RATE2={c2[0]:.4f} mm/s")
        print("INFERENCE: Rate change may correspond to air flow adjustment.")
    
    # Uncertainty budget
    print("UNCERTAINTY_BUDGET:")
    print("  - Front definition (threshold sensitivity): see threshold variations above")
    print("  - Time window choice: see halves above")
    print("  - Exposure variability: profile already normalized by exposure time (schema says divided by exposure time)")
    print("  - Pixel scale uncertainty: ±3% systematic contribution")
    print("  - Frame selection: all 77 frames included unless front not detected")
    
    # Check for expired exposure effect: compare short exposure frames vs long exposure frames
    short_exp_idx = exposure < 0.01
    long_exp_idx = exposure >= 0.01
    for name, idx in [('SHORT_EXPOSURE', short_exp_idx), ('LONG_EXPOSURE', long_exp_idx)]:
        subset_valid = idx & valid
        if np.sum(subset_valid) < 3:
            continue
        t_sub = t[subset_valid]
        pos_sub = pos_valid[np.isin(t_valid, t_sub)]  # careful alignment
        # Simplified: recompute from scratch
        pos_sel = upstream_pos_mm[subset_valid]
        t_sel = t[subset_valid]
        t_rel_sel = t_sel - t_sel[0]
        A_sel = np.vstack([t_rel_sel, np.ones_like(t_rel_sel)]).T
        c_sel, _, _, _ = np.linalg.lstsq(A_sel, pos_sel, rcond=None)
        print(f"{name}_RATE={c_sel[0]:.4f} mm/s (n={np.sum(subset_valid)})")
    
if __name__ == "__main__":
    main()
