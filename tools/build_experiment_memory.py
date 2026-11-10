#!/usr/bin/env python3
"""Build GFL's experiment memory (DEC-042) from the register and the ledger.

Every register item (RES, DEC, ISS, IDEA) becomes a record with its full history
(an ID that appears more than once keeps every appearance, in order), the IDs it
cites, the repository files it names, and for each file the ledger entries that
seal it (seq, entry hash, qualifiers, supersession). Failures are kept as
first-class records: rejected, withdrawn, superseded and failed items are flagged,
never dropped.

A curated storyline (research/fixtures/B6_STORY_v1.json, editorial captions) is
merged in as the ordered B6 path used by the dashboard.

    python tools/build_experiment_memory.py --out visualization/data/experiment_memory.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md"
LEDGER = ROOT / "ledger/ledger.jsonl"
STORY = ROOT / "research/fixtures/B6_STORY_v1.json"

ROW = re.compile(r"^\| (RES-\d+|DEC-\d+|ISS-\d+|IDEA-\d+(?:-[A-Z])?) \| (.+) \| ([^|]+) \|$", re.M)
ID_REF = re.compile(r"\b(?:RES|DEC|ISS|IDEA)-\d+(?:-[A-Z])?\b")
PATH_REF = re.compile(r"`((?:data|tools|docs|research|src|ledger|visualization)/[^`\s]+)`")
KIND = {"RES": "result", "DEC": "decision", "ISS": "issue", "IDEA": "idea"}


def classify(status: str, text: str) -> dict:
    s, t = status.lower(), text.lower()
    state = "other"
    for key, val in (("withdrawn", "withdrawn"), ("superseded", "superseded"), ("rejected", "rejected"),
                     ("verified", "verified"), ("accepted", "accepted"), ("approved", "accepted"),
                     ("closed", "closed"), ("open", "open"), ("proposed", "proposed"), ("captured", "proposed"),
                     ("observation", "observation"), ("measured", "verified"), ("mitigated", "open"),
                     ("explained", "closed"), ("confirmed", "verified"), ("reviewed", "closed"), ("fixed", "accepted")):
        if key in s:
            state = val
            break
    negatives = sorted({w for w in ("rejected", "withdrawn", "fabricat", "fail", "superseded", "not used",
                                    "contaminated", "confabul", "defect") if w in t})
    return {"state": state, "negative_signals": negatives}


def load_ledger():
    entries = [json.loads(line) for line in LEDGER.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_loc, quals, superseded_by = {}, {}, {}
    for e in entries:
        loc = (e.get("object") or {}).get("location")
        if loc:
            by_loc.setdefault(loc, []).append(e)
        if e.get("type") == "qualification":
            quals.setdefault(e["qualifies"], []).append({"qualifiers": e["qualifiers"], "reason": e["reason"], "seq": e["seq"]})
        if e.get("supersedes"):
            superseded_by[e["supersedes"]] = e["entry_hash"]
    return entries, by_loc, quals, superseded_by


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    text = REGISTER.read_text(encoding="utf-8")
    entries, by_loc, quals, superseded_by = load_ledger()
    records: dict[str, dict] = {}
    for order, m in enumerate(ROW.finditer(text)):
        rid, body, status = m.group(1), m.group(2).strip(), m.group(3).strip()
        line_no = text.count("\n", 0, m.start()) + 1
        if "/" in status or status.endswith(".md"):     # early register tables: last column is the source file
            body, status = body + " | " + status, (re.search(r"\b(Accepted|Rejected|Open|Closed|Proposed|Withdrawn)\b", body) or [None, "see text"])[1]
        cls = classify(status, body)
        cites = sorted(set(ID_REF.findall(body)) - {rid})
        paths = sorted(set(PATH_REF.findall(body)))
        files = []
        for p in paths:
            seals = [{"seq": e["seq"], "type": e["type"], "entry_hash": e["entry_hash"],
                      "sha256": e["object"].get("sha256"),
                      "qualifications": quals.get(e["entry_hash"], []),
                      "superseded_by": superseded_by.get(e["entry_hash"])} for e in by_loc.get(p, [])]
            files.append({"path": p, "in_ledger": bool(seals), "ledger": seals})
        rec = records.setdefault(rid, {"id": rid, "kind": KIND[rid.split("-")[0]], "history": []})
        rec["history"].append({"order": order, "register_line": line_no, "status": status, **cls,
                               "text": body, "cites": cites, "files": files})
    for rec in records.values():
        last = rec["history"][-1]
        rec["current_state"] = last["state"]
        rec["current_status"] = last["status"]
        rec["negative_record"] = any(h["negative_signals"] for h in rec["history"]) or last["state"] in (
            "withdrawn", "superseded", "rejected")
        rec["cites"] = sorted({c for h in rec["history"] for c in h["cites"]})
        seals = [s for f in last["files"] for s in f["ledger"]]
        rec["superseded_in_ledger"] = any(s["superseded_by"] for s in seals)
        rec["ledger_qualifiers"] = sorted({q for s in seals for qq in s["qualifications"] for q in qq["qualifiers"]})
        if rec["superseded_in_ledger"]:
            rec["current_state"] = "superseded"
            rec["negative_record"] = True
    cited_by: dict[str, set] = {}
    for rec in records.values():
        for c in rec["cites"]:
            cited_by.setdefault(c, set()).add(rec["id"])
    for rid, rec in records.items():
        rec["cited_by"] = sorted(cited_by.get(rid, set()))
    story = json.loads(STORY.read_text(encoding="utf-8"))
    for step in story["steps"]:
        for rid in step["records"]:
            assert rid in records, f"storyline cites unknown record {rid}"
    out = {"schema": "gfl.experiment_memory.v1",
           "sources": {"register": {"path": str(REGISTER.relative_to(ROOT)),
                                    "sha256": hashlib.sha256(REGISTER.read_bytes()).hexdigest()},
                       "ledger": {"path": str(LEDGER.relative_to(ROOT)), "entries": len(entries),
                                  "head": entries[-1]["entry_hash"]}},
           "counts": {k: sum(1 for r in records.values() if r["kind"] == k) for k in KIND.values()},
           "negative_records": sum(1 for r in records.values() if r["negative_record"]),
           "storyline": story,
           "records": [records[k] for k in sorted(records, key=lambda x: (x.split("-")[0], int(x.split("-")[1])))]}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    shutil.copyfile(LEDGER, a.out.parent / "ledger.jsonl")
    for f in sorted((ROOT / "ledger/keys").glob("*.json")):
        shutil.copyfile(f, a.out.parent / f.name)
    print(json.dumps({"records": len(records), **out["counts"], "negative_records": out["negative_records"],
                      "story_steps": len(story["steps"])}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
