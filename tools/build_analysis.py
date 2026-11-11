#!/usr/bin/env python3
"""Run every gfl_analysis module on the measured runs and write data/derived/analysis/GFL_ANALYSIS_v1.json
(and visualization/data/analysis.json for the dashboard). Inputs are sealed files only; the NASA table is read from
FIF_DATA for the anomaly scan when present.

    FIF_DATA=<raw data root> python tools/build_analysis.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gfl_analysis import anomaly, cram1, flow, gates, prov, records, regime, uq  # noqa: E402

RUNS = {"B6": (100, 3), "B9": (100, 2), "B11": (200, 2), "B13": (400, 3)}


def main() -> int:
    runs = {}
    for run, (um, disp) in RUNS.items():
        rec = records.record(run, disp)
        rf = ROOT / rec["rate_ref"]
        segs = [s for s in json.loads(rf.read_text())["segments"] if s.get("budget")]
        runs[run] = {"record": rec, "flow": flow.air_display_to_velocity(disp), "uq": uq.from_rates_file(rf, disp),
                     "cram1": cram1.compare(um, rec["rate_mm_s"], rec["interval_mm_s"]),
                     "regime_by_segment": [dict(regime.classify(s["air_display"]), rate_mm_s=s["budget"]["rate_mm_s"],
                                               interval_mm_s=s["budget"]["reported_interval_mm_s"], frames=s["frames"]) for s in segs],
                     "flow_independence": regime.consistency_with_measurement({s["air_display"]: s["budget"]["rate_mm_s"] for s in segs
                                                                              if s["budget"]["reported_interval_mm_s"][0] > 0
                                                                              and regime.classify(s["air_display"])["regime"].startswith("thermal")})}
    pairs = [("B6", "B9"), ("B6", "B11"), ("B6", "B13"), ("B9", "B6")]
    transfer = []
    for a, b in pairs:
        r = gates.assess_pair(records.record(a, RUNS[a][1]), records.record(b, RUNS[b][1]))
        transfer.append({"source": a, "target": b, "conclusion": r["conclusion"], "primary_reason": r["primary_reason"],
                         "gates": {g["gate_id"]: {"status": g["status"], "reasons": g["reasons"]} for g in r["gate_assessments"]}})
    table = None
    fd = os.environ.get("FIF_DATA")
    if fd:
        p = Path(fd) / "Experimental table/PSI-25_Experimental table_BASS-II.csv"
        if p.exists():
            table = anomaly.table_checks(p)
    p = prov.export(ROOT / "ledger/ledger.jsonl")
    ratio = {r: round(runs[r]["record"]["rate_mm_s"] / runs[r]["cram1"]["prediction"]["band_mm_s"][0], 3) for r in runs}
    out = {"version": "1.0", "status": "open until compared with the official challenge data (DEC-058)",
           "modules": {"A0": "flow", "A1": "measure", "A2": "gates", "A3": "cram1", "A4": "regime", "A5": "uq", "A6": "anomaly", "A7": "prov"},
           "runs": runs, "transfer": transfer, "table_anomalies": table,
           "cram1_measured_over_lowest_theory": ratio,
           "prov_summary": {"nodes": len(p["@graph"]), "entities": sum(1 for x in p["@graph"] if x.get("@type") == "prov:Entity")}}
    d = ROOT / "data/derived/analysis"
    d.mkdir(parents=True, exist_ok=True)
    (d / "GFL_ANALYSIS_v1.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    (d / "GFL_LEDGER_PROV_O.jsonld").write_text(json.dumps(p, indent=1) + "\n")
    (ROOT / "visualization/data/analysis.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({r: (runs[r]["record"]["rate_mm_s"], runs[r]["cram1"]["prediction"]["band_mm_s"], runs[r]["cram1"]["thin_check"]["reading"],
                          [x["regime"] for x in runs[r]["regime_by_segment"]], runs[r]["flow_independence"].get("relative_spread")) for r in runs}, indent=0))
    print([(t["source"], t["target"], t["conclusion"]) for t in transfer], "table flags", len(table or []), "ratio", ratio)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
