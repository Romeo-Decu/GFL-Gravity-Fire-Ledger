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

from .core import Ledger, generate_key, lineage, load_key_roles, load_private, load_public_keys, verify

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "ledger" / "ledger.jsonl"
KEYS = REPO / "ledger" / "keys"


def PIPELINE_KID() -> str:  # noqa: N802
    return json.loads((KEYS / "release-a.pub.json").read_text())["key_id"]


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
    t = sp.add_parser("anchor-tsa", help="RFC 3161 timestamp of the chain head (FreeTSA), stored in ledger/anchors/")
    t.add_argument("--private", required=True, type=Path)
    t.add_argument("--tsa", default="https://freetsa.org/tsr")
    rq = sp.add_parser("request-approval", help="prepare an approval for the owner to sign on his own machine")
    rq.add_argument("--decision", required=True)
    rq.add_argument("--text", required=True, help="exact decision text the owner approves")
    rq.add_argument("--out", required=True, type=Path)
    at = sp.add_parser("attach-approval", help="append an approval signed by the owner")
    at.add_argument("signed", type=Path)
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
    if a.cmd == "request-approval":
        from .core import sha256_bytes
        owner = [json.loads(p.read_text()) for p in KEYS.glob("*.pub.json") if json.loads(p.read_text()).get("role") == "owner"]
        if not owner:
            print("no owner public key in ledger/keys/")
            return 1
        e = led.build({"type": "approval", "approves": {"decision_id": a.decision, "text": a.text,
                                                        "text_sha256": sha256_bytes(a.text.encode("utf-8")),
                                                        "register": "docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md"}},
                      owner[0]["key_id"])
        a.out.write_text(json.dumps({"entry": e}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print("request written:", a.out, " seq", e["seq"])
        return 0
    if a.cmd == "attach-approval":
        e = json.loads(a.signed.read_text(encoding="utf-8"))
        if e.get("type") != "approval":
            print("not an approval")
            return 1
        keys = load_public_keys(KEYS)
        if load_key_roles(KEYS).get(e["key_id"]) != "owner":
            print("approval is not signed by an owner key - refused")
            return 1
        led.attach(e, keys[e["key_id"]])
        print("approval attached: seq", e["seq"], e["approves"]["decision_id"])
        return 0
    if a.cmd == "anchor-tsa":
        import subprocess
        from .core import sha256_file
        h = led.head()
        d = REPO / "ledger" / "anchors"
        q, r = d / f"head_{h[:16]}.tsq", d / f"head_{h[:16]}.tsr"
        subprocess.run(["openssl", "ts", "-query", "-digest", h, "-sha256", "-cert", "-out", str(q)], check=True, capture_output=True)
        subprocess.run(["curl", "-sS", "-H", "Content-Type: application/timestamp-query", "--data-binary", f"@{q}",
                        "-o", str(r), a.tsa], check=True)
        ca, crt = d / "tsa" / "freetsa_cacert.pem", d / "tsa" / "freetsa_tsa.crt"
        v = subprocess.run(["openssl", "ts", "-verify", "-digest", h, "-in", str(r), "-CAfile", str(ca), "-untrusted", str(crt)],
                           capture_output=True, text=True)
        if "Verification: OK" not in v.stdout:
            print("TSA reply did not verify:", v.stdout, v.stderr)
            return 1
        txt = subprocess.run(["openssl", "ts", "-reply", "-in", str(r), "-text"], capture_output=True, text=True).stdout
        gen = next((ln.split(":", 1)[1].strip() for ln in txt.splitlines() if ln.startswith("Time stamp:")), "")
        rel = r.relative_to(REPO).as_posix()
        kid = PIPELINE_KID()
        e = led.append({"type": "anchor", "covers_head": h,
                        "anchor": {"kind": "rfc3161", "tsa": a.tsa, "hash_alg": "sha256", "gen_time": gen,
                                   "verify": f"openssl ts -verify -digest {h} -in {rel} -CAfile ledger/anchors/tsa/freetsa_cacert.pem -untrusted ledger/anchors/tsa/freetsa_tsa.crt"},
                        "object": {"root": "repo", "location": rel, "sha256": sha256_file(r), "bytes": r.stat().st_size}},
                       load_private(a.private.expanduser()), kid)
        print(gen, e["entry_hash"])
        return 0
    if a.cmd == "anchor-git":
        pk = load_private(a.private.expanduser())
        kid = PIPELINE_KID()
        e = led.append({"type": "anchor", "anchor": {"kind": "git_commit", "repo": "Romeo-Decu/GFL-Gravity-Fire-Ledger",
                                                      "commit": a.commit, "note": a.note},
                        "covers_head": led.head()}, pk, kid)
        print(e["entry_hash"])
        return 0
    r = verify(led, load_public_keys(KEYS), {"repo": REPO, "fif_data": _fif_data(a)}, load_key_roles(KEYS))
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
