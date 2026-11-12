#!/usr/bin/env python3
"""Write the report of every measured run (HTML, JSON, CSV) to visualization/data/reports/.

    python tools/build_reports.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gfl_analysis import report  # noqa: E402


def main() -> int:
    out = ROOT / "visualization/data/reports"
    runs = list(json.loads(report.ANALYSIS.read_text(encoding="utf-8"))["runs"])
    for run in runs:
        report.write(run, out)
    (out / "index.json").write_text(json.dumps({"runs": runs, "formats": ["html", "json", "csv"]}, indent=1) + "\n", encoding="utf-8")
    print(runs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
