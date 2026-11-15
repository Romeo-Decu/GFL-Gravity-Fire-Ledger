import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from window_rule_r4 import apply_g4_from_flame_start  # noqa: E402


def row(t, g1=True, g2=True):
    return {"t_s": t, "G1": g1, "G2": g2, "G3": True, "G5": True, "air_display": 3}


def test_bright_pre_burn_frame_without_edge_does_not_start_the_record():
    # ISS-049: an illuminated reference still passes G1 (brightness) but fails G2 (no edge in the field)
    rows = [row(0.0, g1=True, g2=False), row(287.0), row(288.0), row(289.1), row(300.0)]
    apply_g4_from_flame_start(rows)
    assert [r["G4"] for r in rows] == [False, True, True, True, False]
    assert [r["usable"] for r in rows] == [False, True, True, True, False]


def test_frames_after_the_start_that_fail_g2_stay_in_the_record():
    rows = [row(0.0), row(1.0, g2=False), row(2.0)]
    apply_g4_from_flame_start(rows)
    assert [r["G4"] for r in rows] == [True, True, True]
    assert [r["usable"] for r in rows] == [True, False, True]


def test_no_flame_with_edge_means_no_record():
    rows = [row(0.0, g2=False), row(1.0, g1=False)]
    apply_g4_from_flame_start(rows)
    assert not any(r["G4"] or r["usable"] for r in rows)
