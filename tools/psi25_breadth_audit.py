#!/usr/bin/env python3
"""Breadth audit of the whole PSI-25 investigation at inventory level (DEC-022 part 3).

Inputs: the PSI-25 file manifest (695 files: names and sizes, no contents) and NASA's BASS-II experimental table.
The checks below are fixed in this file, which is committed and anchored before it is run on the real inventory.
A low count is a valid result. Wording rule: sources "disagree" or a file is "not joined"; nothing here says which
source is right.

Checks
  K1  every Raw Data file name is parsed into (GMT day, sample, test) by one of two NASA naming patterns;
      names that follow neither are listed as unparsed (still archives iss0NNeNNNNNN.zip carry no test in the name
      and are counted separately).
  K2  per table row: which kinds of file exist (video, original videos, proof sheet, still sequence, second view,
      test-point archive); rows with no file at all, with no proof sheet, with no video.
  K3  file names whose test is not in the table; whose sample number differs from the table's sample for that test;
      whose GMT day differs from the table's GMT for that test.
  K4  exact duplicate names; groups of two or more files of the same kind with the same byte size.
  K5  counts only: still archives against table rows that record frames shot (the mapping needs file contents).

    python tools/psi25_breadth_audit.py --manifest data/manifests/PSI-25_v4_manifest.json --table <BASS-II table.csv> --out data/derived/PSI25_BREADTH_AUDIT_v1.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

A = re.compile(r"BASS_GMT(?P<gmt>\d+)_SAMPLE_(?P<sample>\d+)_TEST_?(?P<test>[A-Z]\d+[a-z]?)(?P<rest>.*)$")
B = re.compile(r"GMT2014_(?P<gmt>\d+)_BASS_S(?P<sample>\d+)M?_TP(?P<test>[A-Z]\d+[a-z]?)(?P<rest>.*)$")
STILL = re.compile(r"iss\d{3}e\d{6}\.zip$")


def norm_test(t: str) -> str:
    m = re.match(r"([A-Za-z]+)0*(\d+)([a-z]?)$", t.strip())
    return f"{m.group(1).upper()}{m.group(2)}{m.group(3)}" if m else t.strip()


def kind(rest: str, pattern: str) -> str:
    r = rest.lower()
    if "proofsheet" in r:
        return "proof sheet"
    if "original videos" in r:
        return "original videos"
    if "still_sequence" in r:
        return "still sequence"
    if "2nd_view" in r:
        return "second view"
    if pattern == "B" and r.endswith(".zip"):
        return "test-point archive"
    if r.endswith(".mp4"):
        return "video"
    return "other"


def audit(manifest: dict, rows: list[dict]) -> dict:
    table = {}
    for i, r in enumerate(rows, 2):
        t = norm_test(r.get("Test #") or "")
        if t:
            table[t] = {"row": i, "gmt": (r.get("GMT") or "").strip(), "sample": re.sub(r"\D", "", r.get("Sample #") or ""),
                        "frames": (r.get("Total Frames Shot") or "").strip()}
    raw = [f for f in manifest["files"] if f["category"] == "Raw Data"]
    per_test, unparsed, stills, not_in_table, sample_diff, gmt_diff = defaultdict(Counter), [], [], [], [], []
    by_kind_size = defaultdict(list)
    for f in raw:
        name = f["name"].replace("PSI-25_Raw Data_", "", 1)
        if STILL.match(name):
            stills.append(name)
            by_kind_size[("still archive", f["bytes"])].append(name)
            continue
        m, pat = (A.match(name), "A")
        if not m:
            m, pat = (B.match(name), "B")
        if not m:
            unparsed.append(name)
            continue
        t, k = norm_test(m["test"]), kind(m["rest"], pat)
        by_kind_size[(k, f["bytes"])].append(name)
        if t not in table:
            not_in_table.append({"file": name, "test_in_name": t})
            continue
        per_test[t][k] += 1
        if m["sample"] != table[t]["sample"]:
            sample_diff.append({"file": name, "test": t, "sample_in_name": m["sample"], "sample_in_table": table[t]["sample"], "table_row": table[t]["row"]})
        if str(int(m["gmt"])) != str(int(table[t]["gmt"])) if table[t]["gmt"].isdigit() else True:
            gmt_diff.append({"file": name, "test": t, "gmt_in_name": m["gmt"], "gmt_in_table": table[t]["gmt"], "table_row": table[t]["row"]})
    names = Counter(f["name"] for f in manifest["files"])
    with_frames = [t for t, v in table.items() if v["frames"] and v["frames"].lower() != "none"]
    return {
        "inputs": {"files_in_manifest": len(manifest["files"]), "raw_data_files": len(raw), "table_rows": len(rows), "tests_in_table": len(table)},
        "K1_parsing": {"parsed_to_a_test": sum(sum(c.values()) for c in per_test.values()) + len(not_in_table), "still_archives": len(stills), "unparsed": sorted(unparsed)},
        "K2_coverage": {"files_per_kind": dict(sum((c for c in per_test.values()), Counter())),
                        "tests_with_no_file": sorted(t for t in table if t not in per_test),
                        "tests_with_no_proof_sheet": sorted(t for t in table if t in per_test and not per_test[t]["proof sheet"]),
                        "tests_with_no_video": sorted(t for t in table if t in per_test and not (per_test[t]["video"] or per_test[t]["original videos"]))},
        "K3_disagreements": {"test_in_name_not_in_table": not_in_table, "sample_differs": sample_diff, "gmt_differs": gmt_diff},
        "K4_duplicates": {"duplicate_names": sorted(n for n, c in names.items() if c > 1),
                          "same_kind_same_size": [{"kind": k, "bytes": b, "files": sorted(v)} for (k, b), v in sorted(by_kind_size.items(), key=lambda x: str(x[0])) if len(v) > 1]},
        "K5_counts": {"still_archives": len(stills), "table_rows_recording_frames": len(with_frames),
                      "note": "which archive belongs to which test needs the file contents; done for the ten proof sheets held (RES-048)"},
        "wording": "a disagreement means the file name and the table differ; this audit does not say which is right",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--table", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    res = audit(json.loads(a.manifest.read_text(encoding="utf-8")), list(csv.DictReader(a.table.open(encoding="utf-8-sig"))))
    res["inputs"]["manifest_sha256"] = hashlib.sha256(a.manifest.read_bytes()).hexdigest()
    res["inputs"]["table_sha256"] = hashlib.sha256(a.table.read_bytes()).hexdigest()
    text = json.dumps(res, indent=1, ensure_ascii=False) + "\n"
    if a.out:
        a.out.write_text(text, encoding="utf-8")
    k2, k3, k4 = res["K2_coverage"], res["K3_disagreements"], res["K4_duplicates"]
    print(json.dumps({"inputs": res["inputs"], "unparsed": len(res["K1_parsing"]["unparsed"]), "no_file": len(k2["tests_with_no_file"]),
                      "no_proof_sheet": len(k2["tests_with_no_proof_sheet"]), "no_video": len(k2["tests_with_no_video"]),
                      "not_in_table": len(k3["test_in_name_not_in_table"]), "sample_differs": len(k3["sample_differs"]), "gmt_differs": len(k3["gmt_differs"]),
                      "duplicate_names": len(k4["duplicate_names"]), "same_size_groups": len(k4["same_kind_same_size"])}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
