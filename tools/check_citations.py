#!/usr/bin/env python3
"""Deterministic citation check for AI-written summaries, and the ai_findings.json builder.

A summary passes only if:
  C1 every sentence ends with at least one citation such as [RES-019] or [RES-012, ISS-041];
  C2 every cited id exists in the experiment memory;
  C3 every number written in a sentence appears in the text of at least one record it cites
     (a number the model invented, rounded or moved between records fails here).
This checks grounding, not physics: a sentence can cite the right record and still interpret
it badly. A second model reading cited records against sentences is a separate check.

    python tools/check_citations.py --findings research/fixtures/AI_FINDINGS_v1.json \
        --memory visualization/data/experiment_memory.json --out visualization/data/ai_findings.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CITE = re.compile(r"\[((?:[A-Z]+-\d+[A-Z]?)(?:\s*,\s*[A-Z]+-\d+[A-Z]?)*)\]")
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\[])")  # fail-safe: an abbreviation splits a sentence, which can only reject
NUM = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w])")
ORDER = ["upheld", "partly_upheld", "not_upheld", "fabricated"]


def norm(s: str) -> str:
    return s.replace(" ", " ").replace(" ", " ").replace("−", "-")


def check_summary(summary: str, texts: dict[str, str]) -> dict:
    errors, sentences = [], [s.strip() for s in SENT.split(summary.strip()) if s.strip()]
    for s in sentences:
        s = s.rstrip(".")
        cites = CITE.findall(s)
        if not s.endswith("]") or not cites:
            errors.append(f"C1 uncited sentence: {s[:80]}")
            continue
        ids = [x.strip() for c in cites for x in c.split(",")]
        unknown = [i for i in ids if i not in texts]
        if unknown:
            errors.append(f"C2 unknown record {unknown} in: {s[:60]}")
            continue
        body = norm(CITE.sub("", s))
        pool = set(NUM.findall(norm(" ".join(texts[i] for i in ids))))
        for n in NUM.findall(body):
            if n not in pool:  # whole-number match: 2.12 does not match 2.120
                errors.append(f"C3 number {n} not in cited {ids}: {s[:60]}")
    return {"sentences": len(sentences), "passed": not errors, "errors": errors}


def memory_texts(memory: dict) -> dict[str, str]:
    return {r["id"]: " ".join(h["text"] for h in r["history"]) for r in memory["records"]}


def build(findings: dict, memory: dict) -> dict:
    texts = memory_texts(memory)
    out = []
    for f in findings["findings"]:
        chk = check_summary(f["summary"], texts)
        missing = [r for r in f["records"] if r not in texts]
        if missing:
            chk["passed"] = False
            chk["errors"].append(f"C2 unknown listed record {missing}")
        out.append(dict(f, citation_check=chk))
    out.sort(key=lambda f: (ORDER.index(f["verdict"]), f["date"], f["id"]))
    for n, f in enumerate(out, 1):
        f["rank"] = n
    counts = {v: sum(f["verdict"] == v for f in out) for v in ORDER}
    models = sorted({f["model"] for f in out})
    return {"note": findings["note"], "ranking_rule": findings["ranking_rule"], "verdicts": findings["verdicts"],
            "label": "AI-generated summaries; citations checked automatically; physics not validated by the check",
            "checker": "tools/check_citations.py (C1 every sentence cited, C2 cited records exist, C3 numbers appear in cited records)",
            "counts": counts, "models": models, "all_passed": all(f["citation_check"]["passed"] for f in out), "findings": out}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--findings", required=True, type=Path)
    ap.add_argument("--memory", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    res = build(json.loads(a.findings.read_text(encoding="utf-8")), json.loads(a.memory.read_text(encoding="utf-8")))
    for f in res["findings"]:
        if not f["citation_check"]["passed"]:
            print(f["id"], f["citation_check"]["errors"], file=sys.stderr)
    if not res["all_passed"]:
        return 1
    if a.out:
        a.out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"counts": res["counts"], "all_passed": res["all_passed"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
