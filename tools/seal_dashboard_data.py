#!/usr/bin/env python3
"""Seal the dashboard data files in the ledger after they are regenerated, then ship the ledger copy.

For each top-level visualization/data/*.json: no ledger entry yet -> derivation; entry
exists with a different SHA-256 -> supersession of the latest entry; unchanged -> nothing.
Prevents the "altered" state seen on 2026-11-10 when a regenerated file was not re-sealed.

    python tools/seal_dashboard_data.py --key ~/.gfl/keys/release-a.pem --key-id ed25519:5a0c1218bd46311f
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gfl_ledger.core import Ledger, load_private, sha256_file  # noqa: E402

BUILDERS = {"experiment_memory.json": "tools/build_experiment_memory.py", "b6_series.json": "tools/build_dashboard_b6.py"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, type=Path)
    ap.add_argument("--key-id", required=True)
    a = ap.parse_args(argv)
    key = load_private(a.key)
    led = Ledger(ROOT / "ledger/ledger.jsonl")
    for p in sorted((ROOT / "visualization/data").glob("*.json")):
        rel = str(p.relative_to(ROOT))
        tool = BUILDERS.get(p.name, "tools/build_dashboard_extras.py")
        sha = sha256_file(p)
        prev = [e for e in led.entries() if (e.get("object") or {}).get("location") == rel]
        if prev and prev[-1]["object"]["sha256"] == sha:
            continue
        body = {"object": {"root": "repo", "location": rel, "sha256": sha, "bytes": p.stat().st_size}, "parents": [],
                "method": {"name": Path(tool).stem, "script": tool, "script_sha256": sha256_file(ROOT / tool)},
                "note": "dashboard data, regenerated from the register, the ledger and sealed results"}
        if prev:
            body.update({"type": "supersession", "supersedes": prev[-1]["entry_hash"]})
        else:
            body["type"] = "derivation"
        e = led.append(body, key, a.key_id)
        print(f"{e['seq']:4d} {e['type']:12s} {rel}")
    # the page verifies the ledger itself: ship the current ledger, after the seals above
    (ROOT / "visualization/data/ledger.jsonl").write_bytes((ROOT / "ledger/ledger.jsonl").read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
