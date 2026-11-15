"""Ledger core: canonical encoding, hash chain, Ed25519 signatures, verification."""
from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

TYPES = {"ingest": 1, "source_table": 2, "derivation": 3, "supersession": 4, "anchor": None, "qualification": None,
         "approval": None}
OWNER_ONLY = {"approval"}          # DEC-031: only a key with role "owner" may sign these, and an owner key signs nothing else
# qualifiers that must travel downstream: a value derived from an approximate value is never certain (DEC-030)
QUALIFIERS = {"approximate", "provisional", "manual", "declared", "secondary_source", "code_not_committed",
              "unresolved_mapping", "systematic_effect_open"}
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


def load_key_roles(keys_dir: Path) -> dict:
    """key_id -> role. Keys without a role are pipeline keys (held by the processing environment / AI agent)."""
    return {json.loads(p.read_text(encoding="utf-8"))["key_id"]: json.loads(p.read_text(encoding="utf-8")).get("role", "pipeline")
            for p in sorted(keys_dir.glob("*.pub.json"))}


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

    def build(self, body: dict, key_id: str) -> dict:
        """Validate a new entry against the current chain and return it unsigned (entry_hash set)."""
        t = body.get("type")
        if t not in TYPES:
            raise LedgerError(f"unknown entry type {t!r}")
        if t == "qualification":
            if not body.get("qualifies") or not body.get("qualifiers") or not body.get("reason"):
                raise LedgerError("qualification needs qualifies, qualifiers and reason")
            bad = set(body["qualifiers"]) - QUALIFIERS
            if bad:
                raise LedgerError(f"unknown qualifiers {sorted(bad)}")
        if t == "approval":
            ap = body.get("approves") or {}
            if not ap.get("decision_id") or not ap.get("text_sha256") or not ap.get("text"):
                raise LedgerError("approval needs approves.decision_id, approves.text and approves.text_sha256")
            if sha256_bytes(ap["text"].encode("utf-8")) != ap["text_sha256"]:
                raise LedgerError("approval text does not match its hash")
        if t == "supersession" and not body.get("supersedes"):
            raise LedgerError("supersession must name the entry it supersedes")
        if t in ("derivation", "supersession") and not body.get("method"):
            raise LedgerError("derivations must declare their method (DEC-025)")
        es = self.entries()
        known = {e["entry_hash"] for e in es}
        for p in body.get("parents", []):
            if p not in known:
                raise LedgerError(f"parent {p[:12]} is not in the ledger")
        for k in ("qualifies", "supersedes"):
            if body.get(k) and body[k] not in known:
                raise LedgerError(f"{k} target is not in the ledger")
        entry = {**body, "seq": len(es), "tier": TYPES[t], "prev": es[-1]["entry_hash"] if es else GENESIS,
                 "recorded_utc": body.get("recorded_utc") or _now(), "key_id": key_id}
        entry["entry_hash"] = sha256_bytes(canonical(entry))
        return entry

    def attach(self, entry: dict, public_key) -> dict:
        """Append an entry signed elsewhere (e.g. by the owner on his own machine). Re-checks everything."""
        body = {k: v for k, v in entry.items() if k not in ("entry_hash", "sig")}
        if sha256_bytes(canonical(body)) != entry["entry_hash"]:
            raise LedgerError("signed entry content does not match its hash")
        if entry["prev"] != self.head() or entry["seq"] != len(self.entries()):
            raise LedgerError("signed entry was built on an older head - request a new signature")
        public_key.verify(base64.b64decode(entry["sig"]), bytes.fromhex(entry["entry_hash"]))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
        return entry

    def append(self, body: dict, private_key, key_id: str) -> dict:
        entry = self.build(body, key_id)
        entry["sig"] = base64.b64encode(private_key.sign(bytes.fromhex(entry["entry_hash"]))).decode()
        return self.attach(entry, private_key.public_key())


# --------------------------------------------------------------------------- verification
def verify(ledger: Ledger, keys: dict, roots: dict[str, Path], roles: dict | None = None) -> dict:
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
        for p in e.get("parents", []) + [e[k] for k in ("supersedes", "qualifies") if e.get(k)]:
            if p not in seen:
                chain_errors.append(f"seq {i}: references {p[:12]} which is not an earlier entry")
        if roles is not None:
            role = roles.get(e.get("key_id"), "pipeline")
            if e.get("type") in OWNER_ONLY and role != "owner":
                chain_errors.append(f"seq {i}: {e['type']} signed by a {role} key - only the owner may sign approvals")
            if role == "owner" and e.get("type") not in OWNER_ONLY:
                chain_errors.append(f"seq {i}: owner key used for a {e.get('type')} entry - role separation violated")
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


# --------------------------------------------------------------------------- lineage
def own_qualifiers(e: dict) -> set:
    q = set(e.get("qualifiers", []))
    m = e.get("method") or {}
    if m.get("kind") in ("manual", "declared"):
        q.add(m["kind"])
    if m and m.get("kind") == "software" and not m.get("code_commit"):
        q.add("code_not_committed")
    return q


def lineage(ledger: Ledger) -> dict:
    """For every entry: its own qualifiers, the qualifiers inherited from all ancestors, and the
    ancestor entries that introduced them. Qualifications are appended later and attach to their target."""
    es = ledger.entries()
    by = {e["entry_hash"]: e for e in es}
    own = {h: own_qualifiers(e) for h, e in by.items()}
    for e in es:
        if e["type"] == "qualification":
            own[e["qualifies"]] |= set(e["qualifiers"])
    out = {}
    for e in es:   # entries are in causal order, so parents are already resolved
        h = e["entry_hash"]
        inh, src = set(), {}
        for p in e.get("parents", []) + ([e["supersedes"]] if e.get("supersedes") else []):
            for q in own[p] | out[p]["inherited"]:
                inh.add(q)
            for q in own[p]:
                src.setdefault(q, set()).add(p)
            for q, ps in out[p]["introduced_by"].items():
                src.setdefault(q, set()).update(ps)
        out[h] = {"own": own[h], "inherited": inh, "introduced_by": src}
    return out
