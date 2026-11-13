#!/usr/bin/env python3
"""Retrieval relevance with NASA's INDUS sentence encoder (DEC-071, protocol amendment A2).

For each fixed fire-safety question, ranks the 24 PSI combustion investigations by the cosine similarity
between the question and the passages of NASA's record text (gfl_map.record_text). Relevance only: a high
score says the record talks about the question, not that conditions are comparable or a finding transferable.
Runs on the owner's machine; needs `sentence-transformers` and downloads the public model once.

    python tools/indus_rank.py --catalog data/manifests/PSI_CATALOG_v1.json --out evidence_map/INDUS_RELEVANCE_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import gfl_map  # noqa: E402

MODEL = "nasa-impact/nasa-smd-ibm-st-v2"
QUESTIONS = {  # fixed before the run; one per fire-safety function of the map
    "material flammability": "Which materials burn in a spacecraft atmosphere, and at what oxygen concentration do they stop burning?",
    "ignition": "What conditions ignite a fuel in microgravity?",
    "flame spread": "How fast does a flame spread over a solid fuel in low-speed flow in microgravity?",
    "extinction": "At what flow speed or oxygen level does a flame go out in microgravity?",
    "detection": "How can a fire be detected early in a spacecraft from smoke particles or gases?",
    "suppression": "How can a fire be extinguished in a spacecraft, and which suppressant works?",
    "soot and smoke": "How much soot and smoke does a flame produce in microgravity, and what are the particles like?",
}


def passages(text: str, words: int = 90) -> list[str]:
    """Record text cut at sentence ends into passages of about `words` words; each is a verbatim piece of the record."""
    out, cur = [], []
    for sent in re.split(r"(?<=[.!?])\s+|\n\n", text):
        if not sent.strip():
            continue
        cur.append(sent.strip())
        if sum(len(x.split()) for x in cur) >= words:
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def rank(studies: list[dict], encode) -> dict:
    """encode(list of str) -> list of unit vectors. Kept apart from the model so the ranking logic is testable."""
    qs = list(QUESTIONS)
    qv = encode([QUESTIONS[q] for q in qs])
    res = {q: [] for q in qs}
    for s in studies:
        ps = passages(gfl_map.record_text(s))
        pv = encode(ps)
        for q, v in zip(qs, qv):
            sims = [sum(a * b for a, b in zip(v, p)) for p in pv]
            k = max(range(len(sims)), key=sims.__getitem__)
            res[q].append({"study": s["id"], "score": round(float(sims[k]), 4), "passage": ps[k]})
    for q in qs:
        res[q].sort(key=lambda x: -x["score"])
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    from sentence_transformers import SentenceTransformer  # imported here: only this tool needs it
    import sentence_transformers
    model = SentenceTransformer(MODEL)
    studies = [s for s in json.loads(a.catalog.read_text(encoding="utf-8"))["studies"] if s["fields"].get("Research Area") == "Combustion Science"]
    res = rank(studies, lambda xs: model.encode(xs, normalize_embeddings=True).tolist())
    out = {"version": "1", "model": MODEL, "library": f"sentence-transformers {sentence_transformers.__version__}",
           "label": "Retrieval relevance only (cosine similarity of NASA's INDUS encoder). Not comparability, not transferability.",
           "questions": QUESTIONS, "catalog_sha256": hashlib.sha256(a.catalog.read_bytes().replace(b"\r\n", b"\n")).hexdigest(), "ranking": res}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for q, r in res.items():
        print(q, [(x["study"], x["score"]) for x in r[:3]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
