"""GFL owner signing tool (DEC-031) - runs ONLY on the Project Owner's own computer.

Purpose: decisions of the Project Owner are signed with a key that the processing
environment and the AI agent never hold. The private key is encrypted with a
passphrase that only the owner types; this file never sends it anywhere.

Self-contained on purpose (one file, one dependency: `pip install cryptography`),
so it can be read and audited end to end.

    python gfl_owner.py keygen  --out-dir E:\\GFL_vault\\owner
        -> owner.private.pem (encrypted, stays with the owner)
        -> owner.pub.json    (public; goes into the repository, ledger/keys/)

    python gfl_owner.py sign    request.json  --key E:\\GFL_vault\\owner\\owner.private.pem
        -> shows the decision text, recomputes every hash itself, asks for YES,
           writes request.signed.json (give that file back to the pipeline)
"""
from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def keygen(out_dir: Path) -> int:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    out_dir.mkdir(parents=True, exist_ok=True)
    priv = out_dir / "owner.private.pem"
    if priv.exists():
        print("refusing to overwrite", priv)
        return 1
    p1 = getpass.getpass("New passphrase (min 12 characters): ")
    if len(p1) < 12 or p1 != getpass.getpass("Repeat passphrase: "):
        print("passphrases differ or are too short - nothing written")
        return 1
    k = Ed25519PrivateKey.generate()
    raw = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    kid = "ed25519:" + sha(raw)[:16]
    priv.write_bytes(k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                     serialization.BestAvailableEncryption(p1.encode())))
    (out_dir / "owner.pub.json").write_text(json.dumps(
        {"key_id": kid, "alg": "Ed25519", "role": "owner", "holder": "Project Owner",
         "public_key_b64": base64.b64encode(raw).decode(),
         "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}, indent=1) + "\n", encoding="utf-8")
    print("owner key", kid)
    print("KEEP:", priv, "(encrypted)  |  PUBLISH:", out_dir / "owner.pub.json")
    return 0


def sign(req_path: Path, key_path: Path) -> int:
    from cryptography.hazmat.primitives import serialization
    req = json.loads(req_path.read_text(encoding="utf-8"))
    entry = req["entry"]
    if entry.get("type") != "approval":
        print("this tool signs approvals only; refusing type", entry.get("type"))
        return 1
    body = {k: v for k, v in entry.items() if k not in ("entry_hash", "sig")}
    h = sha(canonical(body))                                   # recomputed here, never taken from the request
    ap = entry["approves"]
    if sha(ap["text"].encode("utf-8")) != ap["text_sha256"]:
        print("decision text does not match its hash - refusing")
        return 1
    print("=" * 72)
    print("DECISION", ap["decision_id"])
    print("-" * 72)
    print(ap["text"])
    print("-" * 72)
    print("ledger position: seq", entry["seq"], " after", entry["prev"][:16])
    print("entry hash     :", h)
    print("=" * 72)
    if input('Type YES to sign this approval: ').strip() != "YES":
        print("not signed")
        return 1
    k = serialization.load_pem_private_key(key_path.read_bytes(), password=getpass.getpass("Passphrase: ").encode())
    pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    kid = "ed25519:" + sha(pub)[:16]
    if kid != entry["key_id"]:
        print("this request expects key", entry["key_id"], "but the key file is", kid)
        return 1
    entry["entry_hash"] = h
    entry["sig"] = base64.b64encode(k.sign(bytes.fromhex(h))).decode()
    out = req_path.with_name(req_path.stem + ".signed.json")
    out.write_text(json.dumps(entry, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("signed ->", out)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gfl_owner")
    sp = ap.add_subparsers(dest="cmd", required=True)
    g = sp.add_parser("keygen")
    g.add_argument("--out-dir", required=True, type=Path)
    s = sp.add_parser("sign")
    s.add_argument("request", type=Path)
    s.add_argument("--key", required=True, type=Path)
    a = ap.parse_args(argv)
    return keygen(a.out_dir) if a.cmd == "keygen" else sign(a.request, a.key)


if __name__ == "__main__":
    sys.exit(main())
