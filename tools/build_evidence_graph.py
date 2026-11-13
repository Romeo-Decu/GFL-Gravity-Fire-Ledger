#!/usr/bin/env python3
"""Evidence graph v0.2: the first case (B3 record reconciliation, kept unchanged) plus what GFL measured since.

Reads the sealed analysis and predictions and adds, as typed nodes: NASA's PSI-25 archive as a source, every run GFL
measured (or could not measure), each rate with its interval and rule, the four sealed predictions with their verdicts,
and the computed transfer assessments. Nothing is typed by hand: every added value comes from a sealed file.

    python tools/build_evidence_graph.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.1.json"
OUT = ROOT / "research/fixtures/PMMA100_EVIDENCE_GRAPH_v0.2.json"


def main() -> int:
    g = json.loads(BASE.read_text(encoding="utf-8"))
    an = json.loads((ROOT / "data/derived/analysis/GFL_ANALYSIS_v1.json").read_text(encoding="utf-8"))
    pr = json.loads((ROOT / "visualization/data/predictions.json").read_text(encoding="utf-8"))
    N, E = g["nodes"], g["edges"]

    def edge(kind, s, t, status="established", description=None):
        e = {"id": f"e2_{kind}_{s}_{t}"[:120], "type": kind, "source": s, "target": t, "status": status}
        if description:
            e["description"] = description
        E.append(e)

    N.append({"id": "src_psi25", "type": "source", "label": "NASA PSI-25 archive (BASS-II)", "description": "Public files of the BASS-II investigation in NASA's Physical Sciences Informatics repository: raw stills, proof sheets, experimental table, fan calibration. The data source named by the challenge.",
              "attributes": {"url": "https://psi.nasa.gov/", "source_type": "NASA data repository"}})
    edge("documents", "src_psi25", "inv_bass_ii")
    runs = [(r, d["record"], d["record"]["air_display"]) for r, d in an["runs"].items()]
    for o in an["other_oxygen"]:
        if o["segments"]:
            s = o["segments"][0]
            runs.append((o["run"], {"material": o["material"], "o2_pct": o["o2_pct"], "identity_ref": o["identity"], "rule": o["rule"], "rate_mm_s": s["rate_mm_s"],
                                    "interval_mm_s": s["interval_mm_s"], "rate_ref": f"data/derived/rw4/{o['run']}_RW4_RATES.json"}, s["air_display"]))
        else:
            runs.append((o["run"], {"material": o["material"], "o2_pct": o["o2_pct"], "identity_ref": o["identity"], "rule": o["rule"], "rate_mm_s": None, "why": o["not_measurable"]}, None))
    for run, rec, disp in runs:
        x = f"exp_{run.lower()}_measured"
        N.append({"id": x, "type": "experiment", "label": f"BASS-II {run}", "description": f"{rec['material']}, {rec['o2_pct']} % oxygen. Identity: {rec['identity_ref']}.",
                  "attributes": {"source_run_id": run, "initial_o2_pct": rec["o2_pct"]}})
        edge("part_of", x, "inv_bass_ii")
        edge("documents", "src_psi25", x)
        m = f"measurement_{run.lower()}_rate"
        if rec["rate_mm_s"] is None:
            N.append({"id": m, "type": "measurement", "label": f"{run} spread rate: not measurable", "description": rec["why"], "evidence_state": "unknown",
                      "attributes": {"quantity": "luminous_edge_spread_rate", "value": None, "unit": "mm/s", "rule": rec["rule"]}})
            edge("produces", x, m, "unresolved", "The frozen rule rejects the frames; no value is reported.")
        else:
            lo, hi = rec["interval_mm_s"]
            N.append({"id": m, "type": "measurement", "label": f"{run}: {rec['rate_mm_s']:.2f} mm/s ({lo:.2f}–{hi:.2f})", "evidence_state": "measured",
                      "description": f"Luminous-edge spread rate measured by GFL from NASA's raw stills under the frozen rule {rec['rule']}, air display {disp}. One flight; the pyrolysis front is not imaged.",
                      "attributes": {"quantity": "luminous_edge_spread_rate", "value": rec["rate_mm_s"], "interval": [lo, hi], "unit": "mm/s", "rule": rec["rule"], "air_display": disp, "file": rec["rate_ref"]}})
            edge("produces", x, m)
    for p in pr["predictions"]:
        c = f"claim_{p['id'].lower().replace('-', '_')}"
        N.append({"id": c, "type": "claim", "label": f"{p['id']}: {p['verdict']}", "description": f"Sealed before the run was acquired: {p['claim']}. {p.get('why', '')}".strip(), "evidence_state": "inferred",
                  "attributes": {"band_ratio": p.get("band_ratio"), "ratio": p.get("ratio"), "verdict": p["verdict"]}})
        tgt = f"measurement_{p['run'].lower()}_rate"
        kind = {"supported": "supports", "not supported": "contradicts"}.get(p["verdict"])
        if kind:
            edge(kind, tgt, c)
        else:
            edge("contextualizes", tgt, c, "unresolved", "Not testable under the registered rule; never counted as supported.")
        edge("derived_from", c, "measurement_b6_rate", description="The prediction is a ratio to the B6 reference rate.")
    for t in an["transfer"]:
        a = f"assessment_{t['source'].lower()}_to_{t['target'].lower()}"
        blocking = [k.replace("_", " ") for k, v in t["gates"].items() if v["status"] != "pass"]
        N.append({"id": a, "type": "assessment", "label": f"{t['source']} to {t['target']}: {t['conclusion'].replace('_', ' ')}", "evidence_state": "derived",
                  "description": f"Computed by the transfer engine from measured and recorded values. {t['primary_reason']} Not passing: {', '.join(blocking) or 'none'}.",
                  "attributes": {"inference": "quantitative_transfer", "conclusion": t["conclusion"], "gates": {k: v["status"] for k, v in t["gates"].items()}}})
        edge("assesses", a, f"measurement_{t['source'].lower()}_rate")
        edge("assesses", a, f"measurement_{t['target'].lower()}_rate")
    g["graph_id"] = "gfl-pmma100-evidence-graph-v0.2"
    g["metadata"]["purpose"] = "The B3 record reconciliation of 3 November, unchanged, together with the runs GFL has measured since: sources, runs, rates, sealed predictions and computed transfer assessments. Generated by tools/build_evidence_graph.py from the sealed analysis and predictions files."
    OUT.write_text(json.dumps(g, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(len(N), "nodes,", len(E), "edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
