WF-0011 INTEGRATION_REVIEW — information for Red_Team (Founder directive, GFL). Use only for WF-0011.

GFL's own B6 result, now disclosed for you to attack:
- Data: NASA PSI-25 BASS-II test B6, NEF raw 14-bit stills, linear demosaic; relative radiance = signal / exposure time; width-averaged profile over rows 655–1017 (half-size frame); scale 14.7 px/mm (±3 %); EXIF time.
- Front moves toward INCREASING column index.
- Fit window 13–53 s after the first frame, 40 frames. Reference result 2.274 ± 0.094 mm/s (absolute thresholds 2e5/5e5/1e6 counts/s → 2.21 / 2.27 / 2.34 mm/s).
- Brightness-invariant definition (threshold relative to each frame's own peak, fractions 0.05–0.5): 2.07–2.20 mm/s. Peak position 2.17 mm/s; centroid 1.97 mm/s (tracks flame growth, not propagation).
- Over 300+ windows (start 8–25 s, end 40–60 s) the reference threshold gives 2.20–2.30 mm/s.
- Flame radiance rises ×6.3 in the window while the crew raised opposed flow 3 → 5 cm/s; the leading ramp sharpens 8.8 → 4.0 mm; flame clipping at 13–17 s and 52.6 s; residual autocorrelation ≈ 0.8.

Validator execution of the two blind scripts on the full files (isolated, unmodified):
- kimi26: direction INCREASING columns; primary OLS 0.43 mm/s (R² 0.19), Theil–Sen 0.78; 69/77 frames used; threshold sensitivity 0.01–2.12 mm/s (Theil–Sen at 5–10×MAD: 2.11–2.12); window thirds 3.21 / 0.98 / ≈0 mm/s; max gap between frames 106 s; exposures 0.0008–0.333 s.
- deepseek_v4: cross-correlation says DECREASING columns (mean lag −14.8), but its own front slope is positive (+0.61 mm/s, R² 0.46); thresholds 5–30 % → 0.60–0.63 mm/s; imports scipy (constraint numpy+pandas violated).

Your task: objections in OBIECȚIE format against (1) both blind analyses and (2) GFL's own result. In particular: why do the blind analyses give 0.4–0.8 mm/s and GFL 2.1–2.3 mm/s? Is GFL's 13–53 s window justified or chosen? Which result would a hostile NASA judge accept, and why? Label every statement [VERIFIED] / [REPORTED BY SOURCE] / [INFERENCE] / [UNKNOWN]. Do not look up published values for B6.
