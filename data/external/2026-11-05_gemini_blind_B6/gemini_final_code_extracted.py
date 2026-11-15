import pandas as pd
import numpy as np
metadata = pd.read_csv('B6_frames_metadata.csv')
profiles = pd.read_csv('B6_band_profiles.csv')
metadata['t_exact'] = metadata['unix_time_s'] + metadata['subsec'] / 100.0
metadata['t_rel'] = metadata['t_exact'] - metadata['t_exact'].iloc[0]
matrix = profiles.drop(columns=['image']).values
spatial_scale = 14.7
def get_front_positions(matrix, method='peak'):
    positions = []
    for i in range(matrix.shape[0]):
        row = matrix[i]
        if method == 'peak':
            pos = np.argmax(row)
        elif method == 'half_max_leading':
            peak_val = np.max(row); min_val = np.min(row)
            thresh = min_val + 0.5 * (peak_val - min_val)
            peak_idx = np.argmax(row)
            left_idx = np.where(row[:peak_idx] >= thresh)[0]
            pos = left_idx[0] if len(left_idx) > 0 else peak_idx
        elif method == 'fixed_thresh_1e5':
            idx = np.where(row >= 1e5)[0]
            pos = idx[0] if len(idx) > 0 else np.nan
        positions.append(pos)
    return np.array(positions)
results = []
methods = ['peak', 'half_max_leading', 'fixed_thresh_1e5']
windows = {'Window A (Frames 5-64)': (5, 64), 'Window B (Frames 4-67)': (4, 67)}
for m_name in methods:
    pos_cols = get_front_positions(matrix, method=m_name)
    pos_mm = pos_cols / spatial_scale
    for w_name, (start_f, end_f) in windows.items():
        t_sub = metadata['t_rel'].values[start_f:end_f+1]
        x_sub = pos_mm[start_f:end_f+1]
        valid = ~np.isnan(x_sub)
        t_valid, x_valid = t_sub[valid], x_sub[valid]
        slope, intercept = np.polyfit(t_valid, x_valid, 1)
        residuals = x_valid - (slope * t_valid + intercept)
        rmse = np.sqrt(np.mean(residuals**2))
        r2 = 1 - (np.sum(residuals**2) / np.sum((x_valid - np.mean(x_valid))**2))
        results.append({'Front Definition': m_name,'Time Window': w_name,'Spread Rate (mm/s)': slope,'R-squared': r2,'RMSE (mm)': rmse})
print(pd.DataFrame(results).to_string(index=False))
