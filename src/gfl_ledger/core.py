"""Ledger core: canonical encoding, hash chain, Ed25519 signatures, verification."""
from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

TYPES = {"ingest": 1, "source_table": 2, "derivation": 3, "supersession": 4, "anchor": None}
SEALED_TIERS = {1, 2}
GENESIS = "0" * 64


class LedgerError(Exception):
    pass


def canonical(obj) -> bytes:
    """Deterministic JSON: sorted keys, no whitespace, UTF-8. The hash and signature cover exactly these bytes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --------------------------------------------------------------------------- keys
def generate_key(private_path: Path, public_path: Path) -> str:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    if private_path.exists():
        raise LedgerError(f"refusing to overwrite existing key {private_path}")
    k = Ed25519PrivateKey.generate()
    raw_pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    key_id = "ed25519:" + sha256_bytes(raw_pub)[:16]
    private_path.parent.mkdir(parents=True, exist_ok=True)
    private_path.write_bytes(k.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                             serialization.NoEncryption()))
    private_path.chmod(0o600)
    public_path.parent.mkdir(parents=True, exist_ok=True)
    public_path.write_text(json.dumps({"key_id": key_id, "alg": "Ed25519",
                                       "public_key_b64": base64.b64encode(raw_pub).decode(),
                                       "created_utc": _now()}, indent=1) + "\n", encoding="utf-8")
    return key_id


def load_private(private_path: Path):
    from cryptography.hazmat.primitives import serialization
    return serialization.load_pem_private_key(private_path.read_bytes(), password=None)


def load_public_keys(keys_dir: Path) -> dict:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    out = {}
    for p in sorted(keys_dir.glob("*.pub.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        out[d["key_id"]] = Ed25519PublicKey.from_public_bytes(base64.b64decode(d["public_key_b64"]))
    return out


# --------------------------------------------------------------------------- ledger
class Ledger:
    """ledger.jsonl: one signed entry per line. Never rewritten; only appended."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def entries(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def head(self) -> str:
        e = self.entries()
        return e[-1]["entry_hash"] if e else GENESIS

    def append(self, body: dict, private_key, key_id: str) -> dict:
        t = body.get("type")
        if t not in TYPES:
            raise LedgerError(f"unknown entry type {t!r}")
        if t == "supersession" and not body.get("supersedes"):
            raise LedgerError("supersession must name the entry it supersedes")
        if t in ("derivation", "supersession") and not body.get("method"):
            raise LedgerError("derivations must declare their method (DEC-025)")
        es = self.entries()
        known = {e["entry_hash"] for e in es}
        for p in body.get("parents", []):
            if p not in known:
                raise LedgerError(f"parent {p[:12]} is not in the ledger")
        if body.get("supersedes") and body["supersedes"] not in known:
            raise LedgerError("superseded entry is not in the ledger")
        entry = {**body, "seq": len(es), "tier": TYPES[t], "prev": es[-1]["entry_hash"] if es else GENESIS,
                 "recorded_utc": body.get("recorded_utc") or _now(), "key_id": key_id}
        entry["entry_hash"] = sha256_bytes(canonical(entry))
        entry["sig"] = base64.b64encode(private_key.sign(bytes.fromhex(entry["entry_hash"]))).decode()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
        return entry


# --------------------------------------------------------------------------- verification
def verify(ledger: Ledger, keys: dict, roots: dict[str, Path]) -> dict:
    """Recompute every hash, link and signature; then check each referenced object.

    roots: {"repo": <repo dir>, "fif_data": <raw data dir>} - object locations are relative to one of these.
    Object states: ok | altered | missing (ISS-030: absence is reported, never treated as ok).
    """
    chain_errors, objects = [], []
    prev, seen = GENESIS, set()
    entries = ledger.entries()
    for i, e in enumerate(entries):
        body = {k: v for k, v in e.items() if k not in ("entry_hash", "sig")}
        h = sha256_bytes(canonical(body))
        if h != e.get("entry_hash"):
            chain_errors.append(f"seq {i}: content does not match its entry_hash (entry altered)")
        if e.get("seq") != i:
            chain_errors.append(f"seq {i}: sequence number {e.get('seq')} (entry inserted or removed)")
        if e.get("prev") != prev:
            chain_errors.append(f"seq {i}: prev link broken (entry inserted, removed or reordered)")
        k = keys.get(e.get("key_id"))
        if k is None:
            chain_errors.append(f"seq {i}: unknown signing key {e.get('key_id')}")
        else:
            try:
                k.verify(base64.b64decode(e["sig"]), bytes.fromhex(e["entry_hash"]))
            except Exception:  # noqa: BLE001 - any failure is a signature failure
                chain_errors.append(f"seq {i}: signature invalid")
        for p in e.get("parents", []) + ([e["supersedes"]] if e.get("supersedes") else []):
            if p not in seen:
                chain_errors.append(f"seq {i}: references {p[:12]} which is not an earlier entry")
        seen.add(e.get("entry_hash"))
        prev = e.get("entry_hash")
        obj = e.get("object")
        if obj and obj.get("location") and obj.get("root") in roots:
            p = roots[obj["root"]] / obj["location"]
            if not p.exists():
                state = "missing"
            else:
                state = "ok" if sha256_file(p) == obj["sha256"] else "altered"
            objects.append({"seq": i, "type": e["type"], "location": obj["location"], "root": obj["root"], "state": state})
    superseded = {e["supersedes"] for e in entries if e.get("supersedes")}
    # a repo object that was superseded may legitimately have changed: judge only the latest entry per location
    latest = {}
    for o in objects:
        latest[(o["root"], o["location"])] = o
    current = [o for o in latest.values()
               if entries[o["seq"]]["entry_hash"] not in superseded]
    summary = {s: sum(o["state"] == s for o in current) for s in ("ok", "altered", "missing")}
    return {"entries": len(entries), "head": prev, "chain_ok": not chain_errors, "chain_errors": chain_errors,
            "objects": summary, "object_detail": [o for o in current if o["state"] != "ok"],
            "sealed_altered": [o for o in current if o["state"] == "altered" and TYPES[o["type"]] in SEALED_TIERS]}
