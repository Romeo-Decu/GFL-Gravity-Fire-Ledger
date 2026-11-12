#!/usr/bin/env python3
"""Export the ledger as W3C PROV-O (JSON-LD). A snapshot: it changes whenever the ledger grows, so it is written
last, after every seal, and sealed by its own entry (ISS-055).

    python tools/export_prov.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gfl_analysis import prov  # noqa: E402


def main() -> int:
    p = prov.export(ROOT / "ledger/ledger.jsonl")
    (ROOT / "data/derived/analysis/GFL_LEDGER_PROV_O.jsonld").write_text(json.dumps(p, indent=1) + "\n")
    print(len(p["@graph"]), "nodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
