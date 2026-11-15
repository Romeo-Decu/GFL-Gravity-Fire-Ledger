#!/usr/bin/env python3
"""Score AAL test 2 part S2 against the withheld truth (docs/AAL_TEST2_PROTOCOL_v1.md).

Primary metric: coverage, the share of case results whose reported 95 % interval contains the truth.
Secondary: relative error, direction, re-execution status, third-party imports.

    python tools/score_test2.py --validation <VALIDATION.json> --truth <TRUTH.json> --gfl data/derived/aal_test2 --out <SCORES.json>
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

TRUTH_SHA = "2d9fb28ed2fee741c2a602d4b3d6c8535d335be3627bff2719c46549dd644af6"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--validation", required=True, type=Path)
    ap.add_argument("--truth", required=True, type=Path)
    ap.add_argument("--gfl", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    assert hashlib.sha256(a.truth.read_bytes()).hexdigest() == TRUTH_SHA, "truth file does not match the sealed hash"
    tr = json.loads(a.truth.read_text())
    vt = {c: next(s["v_mm_s"] for s in tr["cases"][c]["schedule"] if s["air"] == tr["estimand_air"][c]) for c in tr["cases"]}
    entries = {}
    for name, v in json.loads(a.validation.read_text()).items():
        if v.get("status") == "ran":
            entries[name] = {"results": v["results"], "returncode": v["returncode"], "third_party": v.get("third_party", []),
                             "own_output_reproduced": v.get("own_output_reproduced")}
        else:
            entries[name] = {"results": {}, "status": v.get("status")}
    g = {}
    for c in vt:
        r = json.loads((a.gfl / f"{c}_rw3_rates.json").read_text())
        seg = next(s for s in r["segments"] if s["air_display"] == tr["estimand_air"][c] and s.get("budget"))
        b = seg["budget"]
        g[c] = {"speed": b["rate_mm_s"], "lo": b["reported_interval_mm_s"][0], "hi": b["reported_interval_mm_s"][1],
                "direction": "increasing", "statistical_only": b["statistical_95_mm_s"]}
    entries["GFL R-W3"] = {"results": g, "returncode": 0, "third_party": []}
    rows = []
    for name, e in entries.items():
        cases, cov = {}, []
        for c, t in vt.items():
            r = e["results"].get(c)
            if not r:
                cases[c] = None
                continue
            err = abs(r["speed"] - t) / t
            covers = r["lo"] <= t <= r["hi"]
            cov.append(covers)
            cases[c] = {"speed": round(r["speed"], 4), "ci95": [round(r["lo"], 4), round(r["hi"], 4)], "rel_error": round(err, 4),
                        "covers": covers, "direction_ok": r["direction"] == "increasing"}
            if "statistical_only" in r:
                lo, hi = r["statistical_only"]
                cases[c]["statistical_only_covers"] = lo <= t <= hi
        rows.append({"analyst": name, "cases": cases, "coverage": f"{sum(cov)}/{len(vt)}",
                     "mean_rel_error": round(sum(x["rel_error"] for x in cases.values() if x) / max(1, sum(1 for x in cases.values() if x)), 4),
                     "returncode": e.get("returncode"), "third_party": e.get("third_party"), "own_output_reproduced": e.get("own_output_reproduced")})
    out = {"truth_sha256": TRUTH_SHA, "truth_estimand_mm_s": vt, "estimand_air": tr["estimand_air"], "rows": rows}
    a.out.write_text(json.dumps(out, indent=1) + "\n")
    print("truth", vt)
    for r in rows:
        print(f"{r['analyst']:14s} coverage {r['coverage']}  mean err {r['mean_rel_error']}",
              {c: (x["speed"], x["covers"]) if x else None for c, x in r["cases"].items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
