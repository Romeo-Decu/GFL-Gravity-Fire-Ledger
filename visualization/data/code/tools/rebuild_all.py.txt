#!/usr/bin/env python3
"""Clean-room rebuild (DEC-022): regenerate the release results in an empty copy of the repository and compare every
output, byte for byte, with the fingerprint sealed in the ledger.

    python tools/rebuild_all.py                      # from sealed derived files (no NASA bytes needed)
    python tools/rebuild_all.py --raw "$FIF_DATA"    # also re-measure the four runs from NASA's raw stills

What it does: copies the tracked files to a temporary directory, deletes every output listed below, runs the steps in
order, and reports each output as identical, differs, or not rebuilt (with the reason). Nothing in the working
repository is changed. Exit code 0 only if no output differs.

Outputs that are snapshots of the ledger (they change whenever the ledger grows) are rebuilt and listed, but not
compared: vault.json, the experiment memory (it lists the ledger entries of each record) and the PROV-O export.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = {"B6": "b6_nef", "B9": "B9_nef", "B11": "B11_nef", "B13": "B13_nef"}
TABLE = "Experimental table/PSI-25_Experimental table_BASS-II.csv"
SNAPSHOTS = ["visualization/data/vault.json", "visualization/data/experiment_memory.json", "data/derived/analysis/GFL_LEDGER_PROV_O.jsonld"]


def steps(raw: Path | None) -> list[dict]:
    py = [sys.executable]
    out = []
    if raw:
        for run, d in RUNS.items():
            out.append({"name": f"measure {run} from raw stills (rule R-W4)", "needs_raw": True,
                        "cmd": py + ["-m", "gfl_analysis", "measure", run, str(raw / "derived" / d), f"data/derived/{run}_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv", "--out", "data/derived/rw4"],
                        "outputs": [f"data/derived/rw4/{run}_RW4_SELECTION.json", f"data/derived/rw4/{run}_RW4_RATES.json"]})
        out.append({"name": "rank the NASA table against B6", "needs_raw": True,
                    "cmd": py + ["tools/rank_comparable_runs.py", "--table", str(raw / TABLE), "--out", "data/derived/BASSII_COMPARABLE_RUNS_v1.json"],
                    "outputs": ["data/derived/BASSII_COMPARABLE_RUNS_v1.json"]})
    out += [
        {"name": "thickness exponent", "cmd": py + ["tools/thickness_exponent.py"], "stdout_to": "data/derived/rw4/THICKNESS_EXPONENT_v1.json",
         "outputs": ["data/derived/rw4/THICKNESS_EXPONENT_v1.json"]},
        {"name": "predictions and blind-test scores", "cmd": py + ["tools/build_predictions.py"], "outputs": ["visualization/data/predictions.json"]},
    ]
    if raw:  # the anomaly scan reads the NASA table; without it the analysis file would lack that part
        out.append({"name": "analysis modules A0 to A6 on the measured runs", "needs_raw": True, "cmd": py + ["tools/build_analysis.py"], "env": {"FIF_DATA": str(raw)},
                    "outputs": ["data/derived/analysis/GFL_ANALYSIS_v1.json", "visualization/data/analysis.json"]})
    out += [
        {"name": "per-run reports", "cmd": py + ["tools/build_reports.py"],
         "outputs": [f"visualization/data/reports/{r}_report.{e}" for r in RUNS for e in ("html", "json", "csv")]},
        {"name": "experiment memory", "cmd": py + ["tools/build_experiment_memory.py", "--out", "visualization/data/experiment_memory.json"],
         "outputs": ["visualization/data/experiment_memory.json"]},
        {"name": "function map, transfer results, families, AI findings", "cmd": py + ["tools/build_dashboard_extras.py", "--out", "visualization/data"],
         "outputs": [f"visualization/data/{f}" for f in ("capabilities.json", "transfer_pmma100.json", "families.json", "ai_findings.json", "comparable_runs.json")] + SNAPSHOTS[:1]},
        {"name": "evidence map from the sealed extractor answers", "cmd": py + ["tools/evidence_map_build.py", "--catalog", "data/manifests/PSI_CATALOG_v1.json", "--raw", "data/derived/evidence_map/raw", "--models", "grok-4.7", "Kimi-K2.6",
                                                                         "--out", "data/derived/evidence_map/EVIDENCE_MAP_v1.json"],
         "outputs": ["data/derived/evidence_map/EVIDENCE_MAP_v1.json"]},
        {"name": "evidence map with three extractors (A3), compared with the first", "cmd": py + ["tools/evidence_map_build.py", "--catalog", "data/manifests/PSI_CATALOG_v1.json", "--raw", "data/derived/evidence_map/raw",
                                                                                         "--out", "data/derived/evidence_map/EVIDENCE_MAP_v2.json", "--compare", "data/derived/evidence_map/EVIDENCE_MAP_v1.json",
                                                                                         "--page", "visualization/data/evidence_map.json"],
         "outputs": ["data/derived/evidence_map/EVIDENCE_MAP_v2.json", "visualization/data/evidence_map.json"]},
        {"name": "evidence graph v0.2 from the sealed analysis and predictions", "cmd": py + ["tools/build_evidence_graph.py"], "outputs": ["research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.2.json"]},
        {"name": "PROV-O export of the ledger", "cmd": py + ["tools/export_prov.py"], "outputs": SNAPSHOTS[2:]},
    ]
    return out


def sealed() -> dict:
    latest = {}
    for line in (ROOT / "ledger/ledger.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            e = json.loads(line)
            o = e.get("object")
            if o and o.get("root") == "repo":
                latest[o["location"]] = (o["sha256"], e["seq"])
    return latest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raw", type=Path, help="root of the NASA PSI-25 download (FIF_DATA), with the extracted stills under derived/")
    ap.add_argument("--keep", type=Path, help="keep the rebuilt copy in this directory")
    ap.add_argument("--report", type=Path, help="write the result as JSON")
    a = ap.parse_args(argv)
    work = a.keep or Path(tempfile.mkdtemp(prefix="gfl_rebuild_"))
    work.mkdir(parents=True, exist_ok=True)
    for f in subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT, text=True).split("\0"):
        if f and (ROOT / f).is_file():
            (work / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / f, work / f)
    plan = steps(a.raw)
    for st in plan:
        for o in st["outputs"]:
            (work / o).unlink(missing_ok=True)
    seals, rows, failed = sealed(), [], []
    env = dict(os.environ, PYTHONPATH=str(work / "src"), PYTHONHASHSEED="0")
    env.pop("FIF_DATA", None)
    for st in plan:
        r = subprocess.run(st["cmd"], cwd=work, env=dict(env, **st.get("env", {})), capture_output=True, text=True)
        if r.returncode == 0 and st.get("stdout_to"):
            (work / st["stdout_to"]).write_text(r.stdout, encoding="utf-8")
        if r.returncode != 0:
            failed.append({"step": st["name"], "error": r.stderr.strip().splitlines()[-1:] or ["no message"]})
        for o in st["outputs"]:
            p = work / o
            if not p.exists():
                state, sha = "not produced", None
            else:
                sha = hashlib.sha256(p.read_bytes()).hexdigest()
                state = ("ledger snapshot, not compared" if o in SNAPSHOTS else "not sealed" if o not in seals
                         else "identical" if seals[o][0] == sha else "differs")
            rows.append({"output": o, "step": st["name"], "state": state, "rebuilt_sha256": sha, "sealed_sha256": seals.get(o, (None, None))[0], "ledger_seq": seals.get(o, (None, None))[1]})
    skipped = [] if a.raw else ["measurement of the four runs from raw stills", "ranking of the NASA table", "analysis modules (the anomaly scan reads the NASA table)"]
    counts = {s: sum(r["state"] == s for r in rows) for s in sorted({r["state"] for r in rows})}
    result = {"mode": "from raw NASA files" if a.raw else "from sealed derived files", "counts": counts, "failed_steps": failed,
              "not_rebuilt_in_this_mode": skipped,
              "not_rebuilt_ever": ["visualization/data/b6_series.json (its input, the blind B6 profile package, is kept outside the repository)",
                                   "visualization/data/relevance.json (INDUS model run on the owner's machine)"],
              "outputs": rows}
    if a.report:
        a.report.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    for r in rows:
        print(f"{r['state']:32s} {r['output']}")
    print(json.dumps({k: result[k] for k in ("mode", "counts", "failed_steps", "not_rebuilt_in_this_mode")}, indent=1))
    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)
    return 1 if failed or counts.get("differs") or counts.get("not produced") else 0


if __name__ == "__main__":
    raise SystemExit(main())
