"""Import of results produced outside GFL (a paper, another team, NASA's own analysis) and comparison with GFL's
measurement of the same run. An imported value is source-reported: it is never relabelled as a GFL measurement.

Accepted files: CSV with a header row, or JSON (one object or a list). Fields:
    source, run, air_display, rate_mm_s, method, reference      required
    lo_mm_s, hi_mm_s                                            optional interval (state what it is in `method`)
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from . import records

REQUIRED = ("source", "run", "air_display", "rate_mm_s", "method", "reference")
OPTIONAL = ("lo_mm_s", "hi_mm_s")
LABEL = "source-reported, not a GFL measurement"


def load(path: Path) -> list[dict]:
    path = Path(path)
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as f:
            return [dict(r) for r in csv.DictReader(f)]
    d = json.loads(path.read_text(encoding="utf-8"))
    return d if isinstance(d, list) else [d]


def validate(row: dict) -> tuple[dict | None, list[str]]:
    """Return (clean row, errors). A row with errors is refused, never repaired."""
    err = [f"missing {k}" for k in REQUIRED if str(row.get(k, "")).strip() == ""]
    out = {k: str(row.get(k, "")).strip() for k in ("source", "run", "method", "reference")}
    for k in ("air_display", "rate_mm_s") + OPTIONAL:
        v = str(row.get(k, "") if row.get(k) is not None else "").strip()
        if v == "":
            out[k] = None
            continue
        try:
            out[k] = float(v)
        except ValueError:
            err.append(f"{k} is not a number: {v!r}")
            out[k] = None
    if out.get("rate_mm_s") is not None and out["rate_mm_s"] <= 0:
        err.append("rate_mm_s must be positive")
    lo, hi = out.get("lo_mm_s"), out.get("hi_mm_s")
    if (lo is None) != (hi is None):
        err.append("give both lo_mm_s and hi_mm_s, or neither")
    elif lo is not None and out.get("rate_mm_s") is not None and not lo <= out["rate_mm_s"] <= hi:
        err.append("rate_mm_s is outside its own interval")
    return (None, err) if err else (out, [])


def compare(ext: dict) -> dict:
    """Compare one validated external value with GFL's record of the same run and air display."""
    res = {"external": dict(ext, label=LABEL), "gfl": None, "ratio_external_over_gfl": None}
    try:
        rec = records.record(ext["run"], int(ext["air_display"]))
    except StopIteration:
        return dict(res, verdict="run not in the NASA table", note="check the run name as written in the BASS-II table")
    if rec["rate_mm_s"] is None:
        return dict(res, verdict="no GFL measurement for this run and air display",
                    note="the external value is kept; nothing to compare it with yet")
    g_lo, g_hi = rec["interval_mm_s"]
    res["gfl"] = {k: rec[k] for k in ("run", "air_display", "rule", "reference_definition", "rate_mm_s", "interval_mm_s", "rate_ref")}
    res["ratio_external_over_gfl"] = round(ext["rate_mm_s"] / rec["rate_mm_s"], 3)
    if ext["lo_mm_s"] is None:
        inside = g_lo <= ext["rate_mm_s"] <= g_hi
        verdict = "external value inside the GFL interval" if inside else "external value outside the GFL interval"
        note = "the external value has no interval, so agreement cannot be assessed on both sides"
    else:
        overlap = ext["lo_mm_s"] <= g_hi and g_lo <= ext["hi_mm_s"]
        verdict = "intervals overlap" if overlap else "intervals do not overlap"
        note = "overlap is not proof of agreement: both sides may share a bias (ISS-050)"
    return dict(res, verdict=verdict, note=note + "; GFL reports luminous-edge rates (DEC-056), so a difference in front definition "
                "between the two methods is a difference in what was measured, not necessarily an error")


def import_file(path: Path) -> dict:
    path = Path(path)
    rows = load(path)
    accepted, refused = [], []
    for i, row in enumerate(rows, 1):
        clean, err = validate(row)
        (refused.append({"row": i, "errors": err, "as_given": row}) if err else accepted.append(compare(clean)))
    return {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "label": LABEL,
            "accepted": accepted, "refused": refused}
