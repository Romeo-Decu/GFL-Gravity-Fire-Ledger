#!/usr/bin/env python3
"""Build the evidence map from the raw extractor answers (DEC-071). Deterministic; calls no model.

    python tools/evidence_map_build.py --catalog data/manifests/PSI_CATALOG_v1.json --raw data/derived/evidence_map/raw --out data/derived/evidence_map/EVIDENCE_MAP_v1.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import gfl_map  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True, type=Path)
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    studies = [s for s in json.loads(a.catalog.read_text(encoding="utf-8"))["studies"] if s["fields"].get("Research Area") == "Combustion Science"]
    inv, log = {}, []
    for s in studies:
        text = gfl_map.record_text(s)
        by_model = {}
        for f in sorted(a.raw.glob(f"{s['id']}_*.json")):
            r = json.loads(f.read_text(encoding="utf-8"))
            ans = gfl_map.parse(r.get("content") or "") if r.get("ok") else None
            log.append({"study": s["id"], "model": r.get("deployment"), "ok": bool(r.get("ok")), "parsed": ans is not None, "content_sha256": r.get("content_sha256")})
            if ans is not None:
                by_model[r["deployment"]] = gfl_map.validate(ans, text)
        if by_model:
            inv[s["id"]] = {"title": s["title"], "acronym": s["fields"].get("Investigation Acronym"), "sub_area": s["fields"].get("SubResearch Area"),
                            "source": s["source"], "publications": len(s.get("publications") or []), **gfl_map.merge(by_model)}
    ids = sorted(inv, key=lambda x: int(x.split("-")[1]))
    pairs = [{"from": x, "to": y, **gfl_map.transfer(inv[x], inv[y])} for i, x in enumerate(ids) for y in ids[i + 1:]]
    by_function = {f: [{"study": i, "status": g["status"]} for i in ids for g in inv[i]["functions"] if g["function"] == f] for f in gfl_map.FUNCTIONS}
    counts = {}
    for p in pairs:
        counts[p["verdict"]] = counts.get(p["verdict"], 0) + 1
    out = {"version": "1", "label": "Extracted by AI models from NASA's PSI record text; every kept item quotes the record word for word. Not NASA's own classification.",
           "method": "docs/GFL_EVIDENCE_MAP_PROTOCOL_v1.md", "vocabulary": {"slots": gfl_map.SLOTS, "functions": gfl_map.FUNCTIONS},
           "investigations": {i: inv[i] for i in ids}, "by_function": by_function, "pairs": pairs, "pair_verdicts": counts, "calls": log}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(len(ids), "investigations;", counts, "; dropped:", {i: inv[i]["dropped"] for i in ids if any(inv[i]["dropped"].values())})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
