#!/usr/bin/env python3
"""INDUS as a non-generative check on the evidence map (protocol amendment A4).

For every fire-safety function an extractor named, with a quote that passed the word-for-word check: the cosine
similarity between that function's fixed question (tools/indus_rank.py) and the quoted passage. Baseline for a
question: the median similarity between it and every passage of all 24 records. An item is flagged when its quote
is no closer to the question than that median, that is, no closer than a typical passage of the archive.
A flag is a request for a human reading, not a verdict. Runs on the owner's machine.

    python tools/indus_quote_check.py --catalog data/manifests/PSI_CATALOG_v1.json --map evidence_map/EVIDENCE_MAP_v2.json --out evidence_map/INDUS_QUOTE_CHECK_v1.json
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import gfl_map  # noqa: E402
import indus_rank  # noqa: E402

SEED = "GFL evidence map, human check, 2026-11-14"  # fixed in the protocol before the run


def dot(a, b):
    return float(sum(x * y for x, y in zip(a, b)))


def check(emap: dict, studies: list[dict], encode) -> dict:
    qs = list(indus_rank.QUESTIONS)
    qv = dict(zip(qs, encode([indus_rank.QUESTIONS[q] for q in qs])))
    allp = [p for s in studies for p in indus_rank.passages(gfl_map.record_text(s))]
    pv = encode(allp)
    base = {q: round(statistics.median(dot(qv[q], v) for v in pv), 4) for q in qs}
    items = []
    for sid, inv in emap["investigations"].items():
        for f in inv["functions"]:
            if f["function"] not in qv:
                continue
            for model, it in f["by"].items():
                items.append({"study": sid, "function": f["function"], "status": f["status"], "model": model, "quote": it["quote"]})
    for it, v in zip(items, encode([i["quote"] for i in items])):
        it["score"] = round(dot(qv[it["function"]], v), 4)
        it["baseline"] = base[it["function"]]
        it["flagged"] = it["score"] <= it["baseline"]
    ids = sorted(emap["investigations"], key=lambda x: int(x.split("-")[1]))
    sample = sorted(random.Random(SEED).sample(ids, 3), key=lambda x: int(x.split("-")[1]))
    flagged = sorted({(i["study"], i["function"]) for i in items if i["flagged"]})
    return {"baseline_median": base, "items": items, "flagged_pairs": [{"study": s, "function": f} for s, f in flagged],
            "summary": {"items": len(items), "flagged_items": sum(i["flagged"] for i in items), "flagged_agreed_functions": len({(i["study"], i["function"]) for i in items if i["flagged"] and i["status"] == "agreed"})},
            "human_check": {"seed": SEED, "random_sample": sample, "rule": "a person reads every flagged item and all functions and conditions of the three sampled investigations against NASA's record"}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True, type=Path)
    ap.add_argument("--map", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    import sentence_transformers
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(indus_rank.MODEL)
    studies = [s for s in json.loads(a.catalog.read_text(encoding="utf-8"))["studies"] if s["fields"].get("Research Area") == "Combustion Science"]
    res = check(json.loads(a.map.read_text(encoding="utf-8")), studies, lambda xs: model.encode(xs, normalize_embeddings=True).tolist())
    out = {"version": "1", "model": indus_rank.MODEL, "library": f"sentence-transformers {sentence_transformers.__version__}",
           "label": "Similarity between a function's question and the quoted passage. A flag asks for a human reading; it is not a verdict.", **res}
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(res["summary"]), "sample:", res["human_check"]["random_sample"], "flagged:", [(p["study"], p["function"]) for p in res["flagged_pairs"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
