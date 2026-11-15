"""Reproducible acquisition of NASA PSI-25 (BASS-II) files.

Raw bytes are written OUTSIDE the repository (FIF_DATA, default ~/FiF_Data).
Only metadata (manifest, hashes, acquisition records) may be committed.

Usage:
    python tools/psi25_fetch.py manifest --out data/manifests/PSI-25_v4_manifest.json
    python tools/psi25_fetch.py get "<exact PSI file name>" [...] --log data/manifests/PSI-25_acquisition_log.json

Network endpoints are the ones used by the public PSI web page itself:
    POST https://psi.nasa.gov/geode-py/ws/files/v2   (file tree)
    GET  https://psi.nasa.gov/geode-py/ws/studies/PSI-25/download?file=...&version=...&redirect=false
         -> returns a short-lived signed URL to the file bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

STUDY = "PSI-25"
API = "https://psi.nasa.gov/geode-py/ws"
UA = {"User-Agent": "FiF-acquisition/0.1 (+research; NASA PSI public data)"}


def _http(url: str, data: bytes | None = None, headers: dict | None = None, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 - fixed public NASA host
        return r.read()


def flatten_tree(tree: dict) -> list[dict]:
    """Flatten the PSI /files/v2 response into one record per file (folders dropped)."""
    out: list[dict] = []

    def walk(node: dict, folders: list[str]) -> None:
        for item in node.get("files") or []:
            if item.get("files"):
                walk(item, folders + [item.get("displayName") or item.get("key", "").rstrip("/").split("/")[-1]])
            elif not item.get("directory"):
                key = item.get("key", "")
                out.append({
                    "category": folders[0] if folders else None,
                    "folder": "/".join(folders),
                    "name": key.split("/")[-1],
                    "key": key,
                    "bytes": None if item.get("bytes_size") is None else int(item["bytes_size"]),
                    "size_label": item.get("size"),
                    "version": item.get("version"),
                    "updated": item.get("updated"),
                    "restricted": bool(item.get("restricted") or item.get("restrictedAccess")),
                })

    walk(tree, [])
    out.sort(key=lambda r: r["key"])
    return out


def fetch_manifest(study_version: int = 4) -> dict:
    body = json.dumps({"folder": "", "fileType": "study", "studyId": STUDY, "version": study_version}).encode()
    raw = _http(f"{API}/files/v2", data=body, headers={"Content-Type": "application/json"})
    files = flatten_tree(json.loads(raw))
    return {
        "study": STUDY,
        "study_version": study_version,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "endpoint": f"POST {API}/files/v2 fileType=study",
        "file_count": len(files),
        "total_bytes": sum(f["bytes"] or 0 for f in files),
        "evidence_status": "source_reported_inventory",
        "files": files,
    }


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(name: str, version: int, dest_dir: Path) -> dict:
    q = urllib.parse.urlencode({"file": name, "version": version, "redirect": "false"})
    signed = _http(f"{API}/studies/{STUDY}/download?{q}").decode().strip().strip('"')
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / name
    tmp = target.with_suffix(target.suffix + ".part")
    req = urllib.request.Request(signed, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(tmp, "wb") as f:  # noqa: S310
        expected = r.headers.get("Content-Length")
        while chunk := r.read(4 << 20):
            f.write(chunk)
    got = tmp.stat().st_size
    if expected is not None and got != int(expected):
        raise IOError(f"{name}: received {got} bytes, server announced {expected}; partial file kept as {tmp.name}")
    tmp.replace(target)
    return {
        "name": name,
        "psi_version": version,
        "bytes": target.stat().st_size,
        "sha256": sha256_file(target),
        "acquired_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "method": "PSI public download API (signed URL)",
        "local_path_relative_to_FIF_DATA": str(target.relative_to(dest_dir.parent)),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="psi25_fetch")
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("manifest")
    m.add_argument("--out", required=True)
    m.add_argument("--study-version", type=int, default=4)
    g = sub.add_parser("get")
    g.add_argument("names", nargs="+")
    g.add_argument("--manifest", default="data/manifests/PSI-25_v4_manifest.json")
    g.add_argument("--log", default="data/manifests/PSI-25_acquisition_log.json")
    a = p.parse_args(argv)

    if a.cmd == "manifest":
        man = fetch_manifest(a.study_version)
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{man['file_count']} files, {man['total_bytes'] / 1024**3:.2f} GiB -> {a.out}")
        return 0

    man = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    by_name = {f["name"]: f for f in man["files"]}
    data_root = Path(os.environ.get("FIF_DATA", Path.home() / "FiF_Data")) / "psi25"
    log_path = Path(a.log)
    log = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else {"study": STUDY, "records": []}
    for name in a.names:
        if name not in by_name:
            print(f"not in manifest: {name}", file=sys.stderr)
            return 2
        f = by_name[name]
        rec = download(name, f["version"], data_root / (f["category"] or "unknown"))
        if f["bytes"] is not None and rec["bytes"] != f["bytes"]:
            print(f"SIZE MISMATCH {name}: got {rec['bytes']} manifest {f['bytes']}", file=sys.stderr)
            return 3
        rec["manifest_bytes"] = f["bytes"]
        log["records"] = [r for r in log["records"] if r["name"] != name] + [rec]
        log["records"].sort(key=lambda r: r["name"])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(log, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")  # after every file
        print(f"{rec['sha256']}  {rec['bytes']:>12}  {name}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
