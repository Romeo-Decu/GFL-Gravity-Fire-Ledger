#!/usr/bin/env python3
"""Relevance (question 1) over the project's literature library with NASA's INDUS retriever.

GFL keeps relevance, comparability and transferability apart. This tool answers only the first:
which passages in the library address a question. It uses INDUS-Retriever-small
(nasa-impact/nasa-ibm-st.38m, Apache-2.0, trained by NASA and IBM on science text including
NASA SMD abstracts). A high score means "this passage is about the question", never "these
conditions are comparable" or "this finding transfers"; those come from the ranking rules and the
transfer engine.

Optional dependencies, not used by CI or the dashboard: sentence-transformers, pypdf.
Runs on the owner's machine (the cloud sandbox cannot reach Hugging Face):

    pip install sentence-transformers pypdf
    python tools/indus_relevance.py --library "<...>/Studies Fire in Microgravity" \
        --queries research/fixtures/RELEVANCE_QUERIES_v1.json --out data/derived/LITERATURE_RELEVANCE_v1.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
from datetime import datetime, timezone
from pathlib import Path

MODEL = "nasa-impact/nasa-ibm-st.38m"
CHUNK_CHARS = 900
SNIPPET_CHARS = 200


def chunk_pages(pages: list[str], size: int = CHUNK_CHARS) -> list[tuple[int, str]]:
    """Split page texts into passages of about `size` characters at sentence boundaries; keep page numbers."""
    out = []
    for pno, text in enumerate(pages, 1):
        text = re.sub(r"\s+", " ", text or "").strip()
        buf = ""
        for sent in re.split(r"(?<=[.!?])\s+", text):
            if len(buf) + len(sent) > size and buf:
                out.append((pno, buf.strip()))
                buf = ""
            buf += sent + " "
        if len(buf.strip()) > 80:
            out.append((pno, buf.strip()))
    return out


def rank(query_vecs, passage_vecs, top_k: int):
    """Cosine ranking; vectors are lists of floats (normalised here)."""
    import math

    def norm(v):
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / n for x in v]
    P = [norm(p) for p in passage_vecs]
    res = []
    for q in query_vecs:
        q = norm(q)
        scores = [sum(a * b for a, b in zip(q, p)) for p in P]
        order = sorted(range(len(P)), key=lambda i: -scores[i])[:top_k]
        res.append([(i, scores[i]) for i in order])
    return res


def read_pdf(path: Path) -> list[str]:
    from pypdf import PdfReader
    return [p.extract_text() or "" for p in PdfReader(str(path)).pages]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--library", required=True, type=Path)
    ap.add_argument("--queries", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--top-k", type=int, default=8)
    a = ap.parse_args(argv)
    from sentence_transformers import SentenceTransformer, __version__ as st_version

    corpus, passages = [], []
    for pdf in sorted(a.library.glob("*.pdf")):
        sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
        try:
            pages = read_pdf(pdf)
        except Exception as e:  # noqa: BLE001 - recorded, not hidden
            corpus.append({"file": pdf.name, "sha256": sha, "pages": 0, "passages": 0, "error": f"{type(e).__name__}: {e}"})
            continue
        chunks = chunk_pages(pages)
        corpus.append({"file": pdf.name, "sha256": sha, "pages": len(pages), "passages": len(chunks)})
        passages += [{"file": pdf.name, "sha256": sha, "page": p, "text": t} for p, t in chunks]
    queries = json.loads(a.queries.read_text(encoding="utf-8"))["queries"]
    model = SentenceTransformer(a.model)
    pv = model.encode([p["text"] for p in passages], batch_size=32, show_progress_bar=True).tolist()
    qv = model.encode([q["text"] for q in queries]).tolist()
    ranked = rank(qv, pv, a.top_k)
    results = []
    for q, hits in zip(queries, ranked):
        results.append({"id": q["id"], "question": q["text"], "why": q.get("why", ""),
                        "hits": [{"rank": n, "score": round(s, 4), "file": passages[i]["file"], "page": passages[i]["page"],
                                  "sha256": passages[i]["sha256"], "snippet": passages[i]["text"][:SNIPPET_CHARS]}
                                 for n, (i, s) in enumerate(hits, 1)]})
    out = {"question_answered": "relevance only: does a passage address the question",
           "not_answered": "comparability of conditions and transferability of findings",
           "model": a.model, "model_card": f"https://huggingface.co/{a.model}", "sentence_transformers": st_version,
           "python": platform.python_version(), "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "chunk_chars": CHUNK_CHARS, "corpus": corpus, "passages": len(passages), "results": results,
           "note": "scores are cosine similarities between embeddings; they rank passages for reading, they are not probabilities"}
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(corpus)} files, {len(passages)} passages, {len(queries)} questions -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
