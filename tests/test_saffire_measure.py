import importlib.util
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("saffire_measure", ROOT / "tools/saffire_measure.py")
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)


def test_scale_is_read_from_a_checkerboard_of_30_mm_blocks(tmp_path):
    w = 66  # pixels per 30 mm block
    a = np.zeros((150, 660, 3), np.uint8)
    for k in range(10):
        if k % 2 == 0:
            a[:, k * w:(k + 1) * w] = 200
    Image.fromarray(a).save(tmp_path / "g.png")
    s = sm.scale_px_per_mm(tmp_path / "g.png")
    assert abs(s["px_per_mm"] - 2 * w / 60) < 0.05 and s["long_axis"] == "columns"


def test_a_synthetic_flame_moving_at_a_known_speed_is_measured(tmp_path):
    w, px_per_mm, v = 66, 2.2, 2.0  # mm/s
    g = np.zeros((150, 660, 3), np.uint8)
    for k in range(10):
        if k % 2 == 0:
            g[:, k * w:(k + 1) * w] = 200
    Image.fromarray(g).save(tmp_path / "grid.png")
    d = tmp_path / "imgs"; d.mkdir()
    t0 = 1479775627704
    for i in range(400):
        t = i / 3.0  # 3 frames per second
        a = np.full((120, 660, 3), 20, np.uint8)
        if i >= 40:
            front = 30 + v * (t - 40 / 3.0) * (2 * w / 60)
            x = np.arange(660)
            prof = np.clip(1 - (x - front) / 25.0, 0, 1) * (x > 10) * 200
            prof[x < front - 120] = 60
            a[:, :, :] = np.clip(20 + prof, 0, 255).astype(np.uint8)[None, :, None]
        Image.fromarray(a).save(d / f"S5C1-{t0 + int(i * 1000 / 3)}.jpeg", quality=95)
    r = sm.measure(sorted(d.glob("*.jpeg")), tmp_path / "grid.png")
    m = r["t0.5"]
    assert r["ignition_end"] == "left" and abs(m["rate_mm_s"] - v) / v < 0.05
    assert m["interval_mm_s"][0] <= m["rate_mm_s"] <= m["interval_mm_s"][1]
