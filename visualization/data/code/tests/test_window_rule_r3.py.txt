import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from window_rule_r3 import apply_g4_from_burn_start  # noqa: E402


def row(t, g1=True):
    return {"t_s": t, "G1": g1, "G2": True, "G3": True, "G5": True, "air_display": 3}


def test_pre_burn_frame_and_gap_do_not_break_the_record():
    rows = [row(0.0, g1=False), row(287.0), row(288.0), row(289.1), row(300.0), row(301.0)]
    apply_g4_from_burn_start(rows)
    assert [r["G4"] for r in rows] == [False, True, True, True, False, False]  # record ends at the 10.9 s gap
    assert [r["usable"] for r in rows] == [False, True, True, True, False, False]


def test_no_flame_means_no_record():
    rows = [row(0.0, g1=False), row(1.0, g1=False)]
    apply_g4_from_burn_start(rows)
    assert not any(r["G4"] or r["usable"] for r in rows)
