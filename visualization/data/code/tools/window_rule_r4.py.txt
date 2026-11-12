#!/usr/bin/env python3
"""Window rule R-W4: R-W3 with one declared change (docs/WINDOW_RULE_R-W4.md, ISS-049).

The burn record starts at the first frame that passes G1 (bright enough) AND G2 (an edge inside the
field), instead of G1 alone. A bright pre-burn reference still with no flame edge no longer opens the
record. Selection only: definitions, estimators, interval and every parameter are R-W3 unchanged, and
R-W3 (tools/window_rule_r3.py) is imported, not edited.

    python tools/window_rule_r4.py select --nef-dir <dir> --overlay <csv> --out <json>
    python tools/window_rule_r4.py fit --nef-dir <dir> --selection <json> --out <json>
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b6_window_rule as wr  # noqa: E402
import window_rule_r3 as r3  # noqa: E402


def apply_g4_from_flame_start(rows: list[dict]) -> None:
    """Recompute G4 and 'usable' in place: continuity counted from the first frame passing G1 and G2."""
    start = next((i for i, r in enumerate(rows) if r["G1"] and r["G2"]), None)
    in_record = [False] * len(rows)
    if start is not None:
        in_record[start] = True
        for i in range(start + 1, len(rows)):
            if rows[i]["t_s"] - rows[i - 1]["t_s"] > wr.G4_MAX_GAP_S:
                break
            in_record[i] = True
    for r, ok in zip(rows, in_record):
        r["G4"] = ok
        r["usable"] = bool(r["G1"] and r["G2"] and r["G3"] and ok and r["G5"] and r["air_display"] is not None)


def main(argv=None) -> int:
    r3.RULE = "R-W4"
    r3.apply_g4_from_burn_start = apply_g4_from_flame_start
    real_select = r3.cmd_select

    def select(a):
        rc = real_select(a)
        import json
        sel = json.loads(a.out.read_text())
        sel["rule_doc"] = "docs/WINDOW_RULE_R-W4.md"
        sel["parameters"]["G4_applied_from"] = "first frame passing G1 and G2"
        a.out.write_text(json.dumps(sel, indent=1) + "\n", encoding="utf-8")
        return rc

    r3.cmd_select = select
    return r3.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
