"""A1. Spread-rate measurement through the frozen window rule R-W4 (docs/WINDOW_RULE_R-W4.md).

The rule code stays in tools/ exactly as sealed in the ledger (window_rule_r4 imports R-W3 and R-W2); this module is the
platform entry point that runs it and returns the result with its three-layer uncertainty (A5).
"""
from __future__ import annotations

import hashlib
import json
import sys
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"


def _rule():
    if str(TOOLS) not in sys.path:
        sys.path.insert(0, str(TOOLS))
    import b6_window_rule as wr  # noqa: E402
    import window_rule_r3 as r3  # noqa: E402
    import window_rule_r4 as r4  # noqa: E402
    r3.RULE = "R-W4"
    r3.apply_g4_from_burn_start = r4.apply_g4_from_flame_start
    return wr, r3


def rule_sha256() -> dict:
    return {p: hashlib.sha256((TOOLS / p).read_bytes()).hexdigest() for p in ("b6_window_rule.py", "window_rule_r3.py", "window_rule_r4.py")}


def measure(nef_dir: Path, overlay: Path, out_dir: Path, run: str) -> dict:
    """Run selection and fit on NEF stills plus the transcribed overlay; write <run>_RW4_SELECTION/RATES.json."""
    wr, r3 = _rule()
    out_dir.mkdir(parents=True, exist_ok=True)
    sel, rates = out_dir / f"{run}_RW4_SELECTION.json", out_dir / f"{run}_RW4_RATES.json"
    _select(r3, Namespace(nef_dir=Path(nef_dir), overlay=Path(overlay), out=sel))
    r3.cmd_fit(Namespace(nef_dir=Path(nef_dir), selection=sel, out=rates))
    return json.loads(rates.read_text())


def _select(r3, a):
    r3.cmd_select(a)
    s = json.loads(a.out.read_text())
    s["rule_doc"] = "docs/WINDOW_RULE_R-W4.md"
    s["parameters"]["G4_applied_from"] = "first frame passing G1 and G2"
    a.out.write_text(json.dumps(s, indent=1) + "\n", encoding="utf-8")


def measure_synthetic(package: Path, side: Path, case: str, out_dir: Path) -> dict:
    """Same rule on a synthetic package (frames from CSV, as in tools/synthetic_front_check.py)."""
    wr, r3 = _rule()
    import synthetic_front_check as sfc  # noqa: E402
    frames = sfc.load_frames(Path(package), json.loads(Path(side).read_text()), case)
    wr.frame_data = lambda _nef_dir: frames
    out_dir.mkdir(parents=True, exist_ok=True)
    ov = sfc.overlay_csv(Path(package), case, max(f["t_s"] for f in frames), out_dir / f"{case}_overlay.csv")
    sel, rates = out_dir / f"{case}_RW4_SELECTION.json", out_dir / f"{case}_RW4_RATES.json"
    _select(r3, Namespace(nef_dir=None, overlay=ov, out=sel))
    r3.cmd_fit(Namespace(nef_dir=None, selection=sel, out=rates))
    return json.loads(rates.read_text())
