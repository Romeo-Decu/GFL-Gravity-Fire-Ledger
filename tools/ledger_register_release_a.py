"""Retroactive registration of every Release A object in the GFL ledger (WP-L, DEC-025).

Run once on an empty ledger. Every entry is marked `retroactive` and carries the time
of the original record; the ledger time is the registration time. Objects are hashed
now and compared with the recorded hash - a mismatch aborts registration.

    FIF_DATA=... python tools/ledger_register_release_a.py --private ~/.gfl/keys/release-a.pem
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gfl_ledger.core import Ledger, LedgerError, load_private, sha256_file  # noqa: E402

DOI = "10.60555/4qc4-de67"
CODE_COMMIT = "97371fcf0eb4c8576c0385091ef658e879b6388a"   # main after PR #6: code that produced Release A outputs
TABLE_EXT = (".csv", ".xlsx")


def blob(path: str) -> str:
    """Git blob id of a file at CODE_COMMIT - identifies the exact code version that ran."""
    return subprocess.run(["git", "-C", str(REPO), "rev-parse", f"{CODE_COMMIT}:{path}"],
                          capture_output=True, text=True, check=True).stdout.strip()


def obj(root: str, loc: str, base: Path, expect: str | None = None) -> dict:
    p = base / loc
    h = sha256_file(p)
    if expect and h != expect:
        raise LedgerError(f"{loc}: hash now {h[:12]} differs from recorded {expect[:12]} - refusing to register")
    return {"root": root, "location": loc, "sha256": h, "bytes": p.stat().st_size}


def instrument(name: str) -> dict:
    if name.endswith(".zip") and "_iss0" in name:
        return {"kind": "still camera", "model": "Nikon D300s", "evidence": "EXIF Make/Model of contained NEF files",
                "timing": "EXIF DateTimeOriginal + SubSecTimeOriginal", "raw_format": "NEF 4320x2868"}
    if "original vid" in name:
        return {"kind": "video camera", "model": "not stated in source",
                "evidence": "MPEG-TS H.264 720x480 29.97 fps with burned-in overlay clock", "raw_format": "TS"}
    return {"kind": "document", "model": "n/a"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--private", required=True, type=Path)
    a = ap.parse_args(argv)
    fif = Path(os.environ.get("FIF_DATA", Path.home() / "FiF_Data"))
    led = Ledger(REPO / "ledger" / "ledger.jsonl")
    if led.entries():
        raise LedgerError("ledger is not empty; retroactive registration runs once")
    pk = load_private(a.private.expanduser())
    kid = json.loads(next((REPO / "ledger" / "keys").glob("*.pub.json")).read_text())["key_id"]
    E = {}

    def add(key, body):
        E[key] = led.append(body, pk, kid)["entry_hash"]

    # ---- tier 2: the published file tree (manifest) ---------------------------------------------
    man = "data/manifests/PSI-25_v4_manifest.json"
    add("manifest", {"type": "source_table", "object": obj("repo", man, REPO),
                     "source": {"study": "PSI-25", "doi": DOI, "study_version": 4,
                                "endpoint": "POST https://psi.nasa.gov/geode-py/ws/files/v2"},
                     "note": "file tree exactly as returned by NASA PSI; not edited",
                     "retroactive": {"original_record": "2026-11-04, commit 97371fc"}})

    # ---- tier 1 / tier 2: every acquired NASA file -------------------------------------------------
    log = json.loads((REPO / "data/manifests/PSI-25_acquisition_log.json").read_text(encoding="utf-8"))
    for r in log["records"]:
        tier2 = r["name"].lower().endswith(TABLE_EXT)
        add(r["name"], {"type": "source_table" if tier2 else "ingest",
                        "object": obj("fif_data", r["local_path_relative_to_FIF_DATA"], fif, r["sha256"]),
                        "source": {"study": "PSI-25", "doi": DOI, "psi_name": r["name"], "psi_version": r["psi_version"],
                                   "method": r["method"]},
                        "instrument": instrument(r["name"]),
                        "parents": [E["manifest"]],
                        "retroactive": {"original_record_utc": r["acquired_utc"],
                                        "re_acquired": "2026-11-05, 31/31 SHA-256 match (RES-003)"}})

    table = E["PSI-25_Experimental table_BASS-II.csv"]
    nef = [E[k] for k in E if k.startswith("PSI-25_Raw Data_iss0")]
    vid = {k: E[k] for k in E if "original vid" in k}
    b6_nef = E["PSI-25_Raw Data_iss040e045728.zip"]
    b6_vid = vid["PSI-25_Raw Data_BASS_GMT188_SAMPLE_153_TESTB6 original videos.zip"]

    def code(tool, params=None, kind="software"):
        return {"kind": kind, "tool": tool, "code_commit": CODE_COMMIT, "code_blob": blob(tool), **({"params": params} if params else {})}

    def der(key, loc, parents, method, note="", orig="2026-11-04, commit 97371fc"):
        add(key, {"type": "derivation", "object": obj("repo", loc, REPO), "parents": parents, "method": method,
                  **({"note": note} if note else {}), "retroactive": {"original_record": orig}})

    D = "data/derived/"
    der("acq_log", "data/manifests/PSI-25_acquisition_log.json", [E["manifest"]], code("tools/psi25_fetch.py"))
    der("nef_index", "data/manifests/PSI-25_NEF_archive_index.json", [E["manifest"]],
        {"kind": "software", "tool": "ZIP central directory via HTTP Range (session script, not in repo)",
         "code_commit": None}, "code of this derivation was not committed - recorded as a gap (ISS-033)")
    der("family_assets", D + "BASSII_100UM_FAMILY_ASSETS_v0.1.csv", [E["manifest"], table], code("tools/family_assets.py"))
    der("b6_source_values", D + "BASSII_B6_SOURCE_VALUES_v0.1.csv", [table],
        {"kind": "manual", "tool": "values copied from the PSI experimental table and cited literature"})
    der("b6_overlay", D + "B6_VIDEO_OVERLAY_TRANSCRIPTION_v0.1.csv", [b6_vid],
        {"kind": "manual", "tool": "visual transcription of the burned-in video overlay (ISS-013: OCR pending)"})
    der("b6_track", D + "B6_FRONT_TRACK_v0.1.csv", [b6_nef],
        code("tools/flame_front.py", {"rows": [655, 1017], "t_window": [13, 53], "px_per_mm_half": 14.7,
                                       "thresholds": [2e5, 5e5, 1e6]}))
    der("b6_result", D + "B6_SPREAD_RATE_RESULT_v0.1.json", [E["b6_track"]], code("tools/flame_front.py"))
    der("b6_comparison", D + "B6_COMPARISON_v0.1.json", [E["b6_result"], E["b6_source_values"]],
        {"kind": "manual", "tool": "comparison record against Carmignani 2019 and NASA/TM-20210011385"})
    der("family_config", D + "BASSII_100UM_MEASUREMENT_CONFIG_v0.1.json", nef,
        {"kind": "declared", "tool": "visually declared row bands and burnt lengths + tools/ruler_scale.py periods",
         "code_commit": CODE_COMMIT, "code_blob": blob("tools/ruler_scale.py")},
        "run-to-archive mapping of the NEF directories is not recorded in the config (ISS-032)")
    der("family_rates", D + "BASSII_100UM_SPREAD_RATES_v0.1.json", [E["family_config"]] + nef, code("tools/family_measure.py"))
    der("reacq", "data/manifests/PSI-25_reacquisition_check_2026-11-05.json", [E["acq_log"]],
        {"kind": "software", "tool": "re-download by logged name/version + SHA-256 comparison (session script)", "code_commit": None},
        "code of this derivation was not committed - recorded as a gap (ISS-033)", orig="2026-11-05, commit 8d6a8b0")
    print(json.dumps({"entries": len(led.entries()), "head": led.head()}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
