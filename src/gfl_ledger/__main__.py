"""gfl - Evidence Vault ledger command line.

    python -m gfl_ledger keygen  --private ~/.gfl/keys/release-a.pem
    python -m gfl_ledger verify  [--fif-data DIR] [--json]
    python -m gfl_ledger status
    python -m gfl_ledger anchor-git --private ... --commit <sha>

Exit code of `verify`: 0 = chain intact and every current object ok;
1 = chain broken or a sealed (tier 1-2) object altered; 2 = chain intact but objects missing/altered.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .core import Ledger, generate_key, lineage, load_private, load_public_keys, verify

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "ledger" / "ledger.jsonl"
KEYS = REPO / "ledger" / "keys"


def _fif_data(a) -> Path:
    return Path(a.fif_data or os.environ.get("FIF_DATA", Path.home() / "FiF_Data"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gfl")
    sp = ap.add_subparsers(dest="cmd", required=True)
    k = sp.add_parser("keygen")
    k.add_argument("--private", required=True, type=Path)
    k.add_argument("--name", default="release-a")
    v = sp.add_parser("verify")
    v.add_argument("--fif-data")
    v.add_argument("--json", action="store_true")
    v.add_argument("--allow-missing", action="store_true",
                   help="exit 0 when raw objects are absent (e.g. CI without NASA bytes); alterations still fail")
    sp.add_parser("status")
    ln = sp.add_parser("lineage", help="qualifiers (approximate, manual, ...) carried by an object and where they entered")
    ln.add_argument("location")
    g = sp.add_parser("anchor-git")
    g.add_argument("--private", required=True, type=Path)
    g.add_argument("--commit", required=True)
    g.add_argument("--note", default="")
    a = ap.parse_args(argv)

    if a.cmd == "keygen":
        kid = generate_key(a.private.expanduser(), KEYS / f"{a.name}.pub.json")
        print(kid)
        return 0
    led = Ledger(LEDGER)
    if a.cmd == "status":
        es = led.entries()
        by = {}
        for e in es:
            by[e["type"]] = by.get(e["type"], 0) + 1
        print(json.dumps({"entries": len(es), "head": led.head(), "by_type": by}, indent=1))
        return 0
    if a.cmd == "lineage":
        es = led.entries()
        L = lineage(led)
        hits = [e for e in es if (e.get("object") or {}).get("location") == a.location]
        if not hits:
            print("no ledger entry for", a.location)
            return 1
        e = hits[-1]
        r = L[e["entry_hash"]]
        loc = {x["entry_hash"]: (x.get("object") or {}).get("location", x["type"]) for x in es}
        print(f"{a.location}  (seq {e['seq']}, {e['type']})")
        print("  own:", ", ".join(sorted(r["own"])) or "-")
        print("  inherited:", ", ".join(sorted(r["inherited"])) or "-")
        for q, ps in sorted(r["introduced_by"].items()):
            print(f"    {q:24s} <- " + "; ".join(sorted(loc[p] for p in ps)))
        return 0
    if a.cmd == "anchor-git":
        pk = load_private(a.private.expanduser())
        kid = next(iter(json.loads(p.read_text())["key_id"] for p in KEYS.glob("*.pub.json")))
        e = led.append({"type": "anchor", "anchor": {"kind": "git_commit", "repo": "Romeo-Decu/FiF",
                                                      "commit": a.commit, "note": a.note},
                        "covers_head": led.head()}, pk, kid)
        print(e["entry_hash"])
        return 0
    r = verify(led, load_public_keys(KEYS), {"repo": REPO, "fif_data": _fif_data(a)})
    if a.json:
        print(json.dumps(r, indent=1))
    else:
        print(f"entries {r['entries']}  head {r['head'][:16]}  chain {'OK' if r['chain_ok'] else 'BROKEN'}")
        for err in r["chain_errors"]:
            print("  CHAIN:", err)
        print(f"objects ok {r['objects']['ok']}  altered {r['objects']['altered']}  missing {r['objects']['missing']}")
        for o in r["object_detail"]:
            print(f"  {o['state'].upper():8s} tier-{o['type']:13s} {o['root']}:{o['location']}")
    if not r["chain_ok"] or r["sealed_altered"]:
        return 1
    if r["objects"]["altered"]:
        return 2
    return 0 if (a.allow_missing or r["objects"]["missing"] == 0) else 2


if __name__ == "__main__":
    sys.exit(main())
