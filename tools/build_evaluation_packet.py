#!/usr/bin/env python3
"""Build the single text packet given to the independent evaluators (docs/GFL_EVALUATION_PROTOCOL_v1.md).

Everything in it is copied from files of the repository; nothing is written for the occasion except the header.

    python tools/build_evaluation_packet.py --out evaluation/PACKET_v1.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ["README.md", "docs/METHODS_AND_VALIDATION_v1.md", "docs/GFL_MAP_2026-11-11.md", "docs/HOW_THE_QUESTION_CHANGED_v1.md",
        "docs/USER_GUIDE_v1.md", "docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md", "docs/WINDOW_RULE_R-W4.md", "docs/OFFICIAL_DATA_COMPARISON_PROTOCOL_v1.md"]
REGISTER = "docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md"
SEP = "\n\n=== FILE: {} ===\n\n"


PHYSICS_DOCS = ["docs/METHODS_AND_VALIDATION_v1.md", "docs/WINDOW_RULE_R-W4.md"]
PHYSICS_ROWS = {"ISS-013", "ISS-020", "ISS-029", "ISS-050", "ISS-051", "ISS-053", "ISS-056", "DEC-045", "DEC-056", "DEC-057", "DEC-058", "DEC-059"}


def register_rows(physics: bool = False) -> str:
    if physics:
        rows = [line for line in (ROOT / REGISTER).read_text(encoding="utf-8").splitlines()
                if (m := re.match(r"\| ((RES|ISS|DEC)-(\d+)) \|", line)) and (m.group(1) in PHYSICS_ROWS or (m.group(2) == "RES" and int(m.group(3)) >= 33))]
        return "Rows copied from the register: results from RES-033 and the issues and decisions that bear on the physics.\n\n" + "\n".join(rows)
    keep = []
    for line in (ROOT / REGISTER).read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| (RES|ISS|DEC|IMPL)-(\d+)", line)
        if not m:
            continue
        kind, n = m.group(1), int(m.group(2))
        state = line.rsplit("|", 2)[-2].lower()
        if (kind == "RES" and n >= 19) or (kind == "DEC" and n >= 45) or kind == "IMPL" or (kind == "ISS" and ("open" in state or n >= 41)):
            keep.append(line)
    return "Rows copied from the register: results from RES-019, decisions from DEC-045, every open issue and every issue from ISS-041, implementation notes.\n\n" + "\n".join(keep)


def functions() -> str:
    caps = json.loads((ROOT / "visualization/data/capabilities.json").read_text(encoding="utf-8"))
    out = ["Function list as shown on the page. Status is stated by the PM: built, partial or designed. The five checks count evidence, not completeness: "
           + "; ".join(f"{k} = {v}" for k, v in caps["criteria"]) + ".", ""]
    for g in caps["groups"]:
        out.append(f"## {g['name']}")
        for it in g["items"]:
            met = [k for k, v in it["maturity"].items() if v]
            out.append(f"- id `{it['id']}` | {it['name']} | status: {it['status']} | checks met: {', '.join(met) or 'none'} | {it['summary']}"
                       + (f" | evidence on NASA data: {it['real'][0]}, {it['real'][1]}" if it.get("real") else "")
                       + (f" | needs: {', '.join(it['needs'])}" if it["needs"] else ""))
    return "\n".join(out)


def key_numbers() -> str:
    a = json.loads((ROOT / "data/derived/analysis/GFL_ANALYSIS_v1.json").read_text(encoding="utf-8"))
    p = json.loads((ROOT / "visualization/data/predictions.json").read_text(encoding="utf-8"))
    keep = {"status": a["status"],
            "runs": {r: {"record": v["record"], "flow_cm_s": v["flow"]["value_cm_s"], "uncertainty": {k: v["uq"][k] for k in ("layer1_statistical_95_mm_s", "layer2_analyst_choice", "reported_interval_mm_s", "interval_with_bounded_unknowns_mm_s")},
                         "physical_unknowns": [{k: u.get(k) for k in ("what", "bound", "bound_rel")} for u in v["uq"]["layer3_physical_unknowns"]],
                         "thin_fuel_theory_mm_s": v["cram1"]["prediction"]["rate_mm_s_by_constant"], "inside_theory_band": v["cram1"]["inside_theory_band"], "thin_check": v["cram1"]["thin_check"],
                         "segments": [{k: s.get(k) for k in ("air_display", "u_cm_s", "damkohler", "radiation_number", "regime", "rate_mm_s", "interval_mm_s", "frames")} for s in v["regime_by_segment"]],
                         "flow_independence": v["flow_independence"]} for r, v in a["runs"].items()},
            "measured_over_lowest_theory": a["cram1_measured_over_lowest_theory"],
            "transfer_between_measured_runs": [{"pair": f"{t['source']} -> {t['target']}", "conclusion": t["conclusion"], "gates": {g: x["status"] for g, x in t["gates"].items()}} for t in a["transfer"]],
            "runs_at_17_percent_oxygen": a["other_oxygen"], "table_flags": a["table_anomalies"],
            "predictions_registered_11_nov": [{k: x.get(k) for k in ("id", "claim", "band_ratio", "ratio", "ratio_interval", "verdict", "why")} for x in p["predictions"]],
            "thickness_exponent": p["thickness_series"]["exponent"],
            "blind_test_2": {"lesson": p["blind_test"]["lesson"], "rows": [{k: r[k] for k in ("analyst", "coverage", "mean_rel_error")} for r in p["blind_test"]["rows"]]},
            "predictions_registered_12_nov_not_yet_scored": [{k: x[k] for k in ("target", "target_air_display", "law", "expected_ratio", "band_ratio")} for x in a["pre_registered"]["registered"]]}
    return "Numbers copied from data/derived/analysis/GFL_ANALYSIS_v1.json and visualization/data/predictions.json.\n\n```json\n" + json.dumps(keep, indent=1, ensure_ascii=False) + "\n```"


def build(challenge: Path | None = None, physics: bool = False) -> str:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    parts = [f"# GFL evaluation packet v1\n\nRepository commit {commit}. Team CCTI, NASA Space Apps 2026, challenge Flame in Freefall. Built by tools/build_evaluation_packet.py.\n\n"
             "You have documents and numbers copied from the repository. You do not have the source code, the raw NASA files or the web page; "
             "where a question needs them, answer \"cannot verify\". Each part below starts with a line `=== FILE: <name> ===`; use that name in your locators."]
    if challenge:
        text = challenge.read_text(encoding="utf-8").strip()
        parts[0] += f" The challenge statement below was copied by the team owner from the NASA Space Apps 2026 challenge page (sha256 of the copy {hashlib.sha256(text.encode()).hexdigest()})."
        parts.append(SEP.format("CHALLENGE") + text)
    if physics:
        parts[0] += " This is the physics packet (amendment A2): methods, window rule, numbers, one report and the physics rows of the register; the README, map, history, user guide, AI disclosure and function list are not included."
    for d in (PHYSICS_DOCS if physics else DOCS):
        parts.append(SEP.format(d) + (ROOT / d).read_text(encoding="utf-8").strip())
    if not physics:
        parts.append(SEP.format("FUNCTIONS") + functions())
    parts.append(SEP.format("KEY_NUMBERS") + key_numbers())
    parts.append(SEP.format("REPORT_B11") + "The report of one run, as GFL writes it (visualization/data/reports/B11_report.json).\n\n```json\n"
                 + (ROOT / "visualization/data/reports/B11_report.json").read_text(encoding="utf-8").strip() + "\n```")
    parts.append(SEP.format("REGISTER") + register_rows(physics))
    return "".join(parts) + "\n"


def split(packet: str) -> dict:
    """File name -> text, as the scorer reads the packet."""
    out, name = {}, None
    for chunk in re.split(r"\n=== FILE: (.+?) ===\n", packet):
        if name is None:
            name = "HEADER"
            out[name] = chunk
            name = ""
        elif name == "":
            name = chunk
        else:
            out[name] = chunk
            name = ""
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--challenge", type=Path, help="the challenge statement as copied from the Space Apps page (kept outside the repository)")
    ap.add_argument("--physics", action="store_true", help="the smaller physics packet of amendment A2")
    a = ap.parse_args(argv)
    text = build(a.challenge, a.physics)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(text, encoding="utf-8")
    print(json.dumps({"out": str(a.out), "chars": len(text), "sha256": hashlib.sha256(text.encode()).hexdigest(), "files": list(split(text))}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
