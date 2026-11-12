#!/usr/bin/env python3
"""Deterministic check of the evaluators' answers (docs/GFL_EVALUATION_PROTOCOL_v1.md): locators and reading checks.

    python tools/score_evaluation.py --packet evaluation/PACKET_v1.md --raw evaluation/raw --out evaluation/SCORES_v1.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_evaluation_packet import split  # noqa: E402


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("“", '"').replace("”", '"').replace("…", "...")
    return re.sub(r"\s+", " ", s).strip().strip('"').strip("'").strip(".").lower()


def parse(content: str):
    m = re.search(r"\{.*\}", content, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def locator_state(item, files: dict) -> str:
    loc = item.get("locator") if isinstance(item, dict) else None
    if not isinstance(loc, dict) or not str(loc.get("quote", "")).strip():
        return "no locator"
    name = str(loc.get("file", "")).strip()
    match = next((f for f in files if f == name or f.endswith("/" + name) or name.endswith("/" + f)), None)
    if match is None:
        return "file not in packet"
    q = norm(str(loc["quote"]))
    if len(q.split()) > 30:
        return "quote too long"
    return "verified" if q and q in norm(files[match]) else "quote not found"


def reading(ans: dict) -> dict:
    a = ans.get("A") or {}
    out = {}
    try:
        a1 = a["A1"]
        out["A1"] = round(float(a1["rate_mm_s"]), 2) == 2.20 and [round(float(x), 2) for x in a1["interval_mm_s"]] == [1.91, 2.37]
    except (KeyError, TypeError, ValueError):
        out["A1"] = False
    out["A2"] = isinstance(a.get("A2"), dict) and a["A2"].get("section_exists") is False
    try:
        a3 = a["A3"]
        out["A3"] = "b13" in str(a3["prediction"]).lower() and round(float(a3["ratio"]), 2) == 0.19
    except (KeyError, TypeError, ValueError):
        out["A3"] = False
    out["invented_content"] = isinstance(a.get("A2"), dict) and a["A2"].get("section_exists") is True
    return out


def score(raw: dict, files: dict) -> dict:
    res = {"role": raw.get("role"), "deployment": raw.get("deployment"), "model_reported": raw.get("model_reported"), "call_ok": bool(raw.get("ok")),
           "finish_reason": raw.get("finish_reason")}
    ans = parse(raw.get("content") or "") if raw.get("ok") else None
    if ans is None:
        return dict(res, parsed=False)
    res.update(parsed=True, reading_checks=reading(ans), sections={})
    for sec in ("B", "C", "D", "E", "L"):
        items = ans.get(sec) if isinstance(ans.get(sec), list) else []
        states = [locator_state(it, files) for it in items]
        res["sections"][sec] = {"items": len(items), "verified": states.count("verified"),
                                "not_counted": [{"n": i + 1, "state": s, "item": it} for i, (s, it) in enumerate(zip(states, items)) if s != "verified"]}
    res["counts"] = {k: len(ans.get(k) or []) for k in ("F", "H", "J")}
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True, type=Path)
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    files = split(a.packet.read_text(encoding="utf-8"))
    out = {"protocol": "docs/GFL_EVALUATION_PROTOCOL_v1.md", "evaluators": [score(json.loads(p.read_text(encoding="utf-8")), files) for p in sorted(a.raw.glob("*.json"))]}
    text = json.dumps(out, indent=1, ensure_ascii=False) + "\n"
    if a.out:
        a.out.write_text(text, encoding="utf-8")
    for e in out["evaluators"]:
        print(e["role"], e["deployment"], "parsed" if e.get("parsed") else "NOT PARSED", e.get("reading_checks"),
              {k: f"{v['verified']}/{v['items']}" for k, v in (e.get("sections") or {}).items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
