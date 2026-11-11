#!/usr/bin/env python3
"""Validator: re-execute every delivered analysis script on the full synthetic files.

For each response (`<probe>/*.json`, content with a Python code block) the script is written into a
fresh directory with only the package CSVs, run with `python -I` and an empty environment, and the
`RESULT <case> speed_mm_s=… ci95_low=… ci95_high=… direction=…` lines are read from what it prints.
Nothing in the script is changed, except the data location of a script written for another machine
(recorded as `path_fix`).

    python tools/validate_probe.py --package data/synthetic/aal_test2 --probe data/derived/aal_test2/probe \
        --work <scratch dir> --out data/derived/aal_test2/VALIDATION_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RESULT = re.compile(r"RESULT\s+(\w+)\s+speed_mm_s=([-\d.eE+naN]+)\s+ci95_low=([-\d.eE+naN]+)\s+ci95_high=([-\d.eE+naN]+)\s+direction=(\w+)")
CODE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S)
STDLIB = set(getattr(sys, "stdlib_module_names", ()))


def run_one(name: str, code: str, package: Path, work: Path) -> dict:
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    for p in package.glob("*.csv"):
        shutil.copy(p, d / p.name)
    path_fix = None
    m = re.search(r'^(BASE|DATA_DIR|DATA)\s*=\s*["\'](/[^"\']+)["\']', code, re.M)
    if m:
        code = code.replace(m.group(0), f'{m.group(1)} = "."')
        path_fix = f"{m.group(1)} set to the working directory (was {m.group(2)})"
    (d / "analysis.py").write_text(code)
    imports = sorted(set(re.findall(r"^\s*(?:import|from)\s+([A-Za-z_]\w*)", code, re.M)))
    try:
        r = subprocess.run([sys.executable, "-I", "analysis.py"], cwd=d, capture_output=True, text=True, timeout=900,
                           env={"PATH": "/usr/bin:/bin", "HOME": str(d)})
        out, err, rc = r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        out, err, rc = "", "TIMEOUT", -9
    results = {}
    for c, s, lo, hi, dr in RESULT.findall(out):
        results[c] = {"speed": float(s), "lo": float(lo), "hi": float(hi), "direction": dr}  # last line per case wins
    return {"status": "ran", "returncode": rc, "imports": imports,
            "third_party": sorted(i for i in imports if i not in STDLIB and i not in ("numpy", "pandas")),
            "code_sha256": hashlib.sha256(code.encode()).hexdigest(), "path_fix": path_fix,
            "results": results, "stdout": out, "stderr_tail": err[-800:]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True, type=Path)
    ap.add_argument("--probe", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    res = {}
    for f in sorted(a.probe.glob("*.json")):
        d = json.loads(f.read_text())
        if not d.get("ok") or not d.get("content"):
            res[f.stem] = {"status": "no_response", "detail": d.get("error") or d.get("finish_reason")}
            continue
        blocks = [b for b in CODE.findall(d["content"]) if "import" in b]
        res[f.stem] = run_one(f.stem, max(blocks, key=len), a.package, a.work) if blocks else {"status": "no_script"}
    for sub in sorted(p for p in a.probe.iterdir() if p.is_dir()):  # agents that ran their own code (Manus)
        scripts = sorted(sub.glob("*.py"))
        if scripts:
            r = run_one(sub.name, scripts[0].read_text(), a.package, a.work)
            claimed = "\n".join(p.read_text() for p in sub.glob("*.txt"))
            r["own_output_reproduced"] = {c: v for c, v in r["results"].items()} == {
                c: {"speed": float(s), "lo": float(lo), "hi": float(hi), "direction": dr} for c, s, lo, hi, dr in RESULT.findall(claimed)}
            res[sub.name] = r
    a.out.write_text(json.dumps(res, indent=1) + "\n")
    for k, v in res.items():
        print(k, v["status"], v.get("returncode"), v.get("third_party"), {c: round(x["speed"], 4) for c, x in v.get("results", {}).items()},
              "reproduced" if v.get("own_output_reproduced") else "", (v.get("stderr_tail") or "")[-160:].replace("\n", " | ") if v.get("returncode") else "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
