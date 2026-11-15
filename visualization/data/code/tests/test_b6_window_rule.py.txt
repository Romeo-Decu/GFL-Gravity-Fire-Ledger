"""Unit tests for the B6 window rule helpers (DEC-040/041)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import b6_window_rule as w  # noqa: E402


def gaussian(center, width=40, n=600, amp=1.0):
    x = np.arange(n)
    return amp * np.exp(-0.5 * ((x - center) / width) ** 2)


def test_leading_edge_is_on_the_increasing_side_of_the_peak():
    p = gaussian(300) + gaussian(100, amp=0.8)          # secondary blob behind the front
    e = w.lead_rel(p, 0.1)
    assert e > 300                                        # never picks the trailing blob
    assert abs(e - (300 + 40 * np.sqrt(2 * np.log(10)))) <= 1


def test_relative_edge_is_brightness_invariant_absolute_is_not():
    p1, p2 = gaussian(300), gaussian(300, amp=6.3)
    assert w.lead_rel(p1, 0.1) == w.lead_rel(p2, 0.1)
    assert w.lead_abs(p2, 0.1) > w.lead_abs(p1, 0.1)


def test_air_at_uses_last_sample_at_or_before_t():
    ov = [(1.0, 4), (7.0, 3), (34.0, 4)]
    assert w.air_at(ov, 0.5) is None
    assert w.air_at(ov, 6.9) == 4
    assert w.air_at(ov, 7.0) == 3
    assert w.air_at(ov, 40.0) == 4


def test_rate_block_recovers_known_slope_in_mm_per_s():
    rng = np.random.default_rng(1)
    t = np.arange(10, dtype=float)
    x = 100 + 2.0 * w.PX_PER_MM * t + rng.normal(0, 0.5, t.size)    # 2.0 mm/s
    r = w.rate_block(t, x, np.random.default_rng(2))
    assert abs(r["ols_mm_s"] - 2.0) < 0.01
    assert abs(r["theil_sen_mm_s"] - 2.0) < 0.01
    lo, hi = r["boot95_mm_s"]
    assert lo < 2.0 < hi


def test_hac_exceeds_iid_se_for_positively_autocorrelated_residuals():
    t = np.arange(40, dtype=float)
    e = np.zeros(40)
    rng = np.random.default_rng(3)
    for i in range(1, 40):
        e[i] = 0.9 * e[i - 1] + rng.normal()
    x = 3.0 * t + e
    b, res, tm = w.ols(t, x)
    se_iid = np.sqrt((res ** 2).sum() / 38 / (tm ** 2).sum())
    assert w.hac_se(t, x, 6) > se_iid
