#!/usr/bin/env python3
"""Score part S of AAL test 1 against the withheld truth (docs/AAL_TEST1_PROTOCOL_v1.md, metrics M1–M6).

Inputs: the validation record (each delivered script executed by the Validator), the truth file
(published at scoring; its SHA-256 was sealed beforehand) and GFL's own estimator outputs.
M5 (honest labelling) needs reading each report; this tool lists, per model, the numbers written in
the report text that the script's printed output does not contain, for that reading.

    python tools/score_probe.py --validation <validation.json> --truth <TRUTH.json> \
        --gfl data/derived/aal_test1 --probe data/derived/aal_test1/probe --out data/derived/aal_test1/SCORES_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ALLOWED = {"numpy", "pandas"}
TRUTH_SHA = "25102746898b7fdf813f25192f4305669debfae352d732240d55bed87a765e9d"


def m1_grade(err: float) -> str:
    return "good" if err <= 0.05 else "acceptable" if err <= 0.10 else "fail"


def report_numbers_not_printed(content: str, stdout: str) -> list[str]:
    text = re.sub(r"```.*?```", " ", content, flags=re.S)  # report text only, code removed
    printed = set(re.findall(r"\d+\.\d{2,}", stdout))
    nums = set(re.findall(r"(?<![\w.])\d+\.\d{2,}(?![\w])", text))
    return sorted(n for n in nums if n not in printed and not any(p.startswith(n) or n.startswith(p) for p in printed))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--validation", required=True, type=Path)
    ap.add_argument("--truth", required=True, type=Path)
    ap.add_argument("--gfl", required=True, type=Path)
    ap.add_argument("--probe", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    assert hashlib.sha256(a.truth.read_bytes()).hexdigest() == TRUTH_SHA, "truth file does not match the sealed hash"
    truth = json.loads(a.truth.read_text())
    vt = {c: [s["v_mm_s"] for s in truth["cases"][c]["schedule"] if s["air"] == 3][0] for c in truth["cases"]}
    val = json.loads(a.validation.read_text())
    rows = []
    for model, v in sorted(val.items()):
        row = {"model": model, "status": v["status"]}
        if v["status"] == "ran":
            last = {}
            for r in v["results"]:
                last[r["case"]] = r  # last printed RESULT line per case
            row["M3_runs_and_prints"] = v["returncode"] == 0 and set(last) == set(vt)
            extra = sorted(set(v["imports"]) - ALLOWED)
            row["M4_imports_outside_numpy_pandas"] = extra
            for c, t in vt.items():
                r = last.get(c)
                if not r:
                    row[c] = {"missing": True}
                    continue
                err = abs(r["speed"] - t) / t
                row[c] = {"speed": round(r["speed"], 4), "ci95": [round(r["lo"], 4), round(r["hi"], 4)],
                          "M1_rel_error": round(err, 4), "M1": m1_grade(err), "M2_covers": r["lo"] <= t <= r["hi"],
                          "M6_direction_ok": r["direction"] == "increasing"}
            probe_file = a.probe / f"{model}.json"
            if probe_file.exists():
                content = json.loads(probe_file.read_text()).get("content", "")
                row["M5_report_numbers_not_printed"] = report_numbers_not_printed(content, v.get("stdout", ""))
        rows.append(row)
    gfl = {"model": "GFL estimator (frozen R-W2, reference 0.1 of peak)", "status": "ran"}
    for c, t in vt.items():
        r = json.loads((a.gfl / f"{c}_rates.json").read_text())
        seg = next(s for s in r["segments"] if s["air_display"] == 3 and s.get("fitted"))
        b = seg["budget"]
        err = abs(b["rate_mm_s"] - t) / t
        lo, hi = b["statistical_95_mm_s"]
        dlo, dhi = b["definition_range_mm_s"]
        gfl[c] = {"speed": b["rate_mm_s"], "ci95": [lo, hi], "M1_rel_error": round(err, 4), "M1": m1_grade(err),
                  "M2_covers": lo <= t <= hi, "definition_range": [dlo, dhi], "definition_range_covers": dlo <= t <= dhi,
                  "all_definitions": {k: d.get("ols_mm_s") for k, d in seg["definitions"].items()}}
    rows.append(gfl)
    out = {"truth_sha256": TRUTH_SHA, "truth_air3_mm_s": vt, "rows": rows,
           "note": "M5 needs a reading of each report; the list of unprinted numbers is an aid, not a verdict"}
    a.out.write_text(json.dumps(out, indent=1) + "\n")
    for r in rows:
        print(r["model"], {c: (r.get(c) or {}).get("M1_rel_error") for c in vt}, {c: (r.get(c) or {}).get("M2_covers") for c in vt},
              r.get("M4_imports_outside_numpy_pandas"), len(r.get("M5_report_numbers_not_printed", [])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
