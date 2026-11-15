import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from indus_relevance import chunk_pages, rank  # noqa: E402  (no model or pypdf needed)


def test_chunking_keeps_pages_and_size():
    page = "Flame spread was measured. " * 80
    chunks = chunk_pages([page, "", "Short."])
    assert chunks and all(p == 1 for p, _ in chunks)  # empty and tiny pages give no passage
    assert all(len(t) <= 900 + 40 for _, t in chunks)


def test_rank_orders_by_cosine():
    res = rank([[1.0, 0.0]], [[0.0, 1.0], [2.0, 0.1], [1.0, 1.0]], top_k=2)
    assert [i for i, _ in res[0]] == [1, 2]
    assert res[0][0][1] > res[0][1][1]
