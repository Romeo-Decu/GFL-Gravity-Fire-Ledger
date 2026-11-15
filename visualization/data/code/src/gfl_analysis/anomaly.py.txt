"""A6. Data anomaly detector: records, frames and the flow overlay.

Every check is declared here with its threshold; a flag says what was seen, never what it means physically.
Thresholds follow the frozen window rule where one exists (G4: gaps over 5 s).
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

GAP_S = 5.0                # same as window rule G4
FLICKER_REL = 0.05         # robust scatter of frame brightness about a running median
O2_FLOOR = 10.0            # % by volume; BASS-II ran down to about 15 % on purpose, below 10 % is not a test atmosphere
O2_DROP = 3.0              # percentage points within one test, in either direction (a rise is flagged as o2_rise)


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def table_o2(csv_path: Path) -> list[dict]:
    """Initial and final calibrated O2 of every test that records both: the picture behind the o2 checks."""
    rows = list(csv.DictReader(Path(csv_path).open(encoding="utf-8-sig")))
    key = lambda r, s: next((v for k, v in r.items() if k and s.lower() in k.lower()), None)  # noqa: E731
    out = []
    for r in rows:
        a, b = _num(key(r, "initial O2")), _num(key(r, "final O2"))
        if a is not None and b is not None:
            out.append({"test": (r.get("Test #") or "").strip(), "o2_initial": a, "o2_final": b,
                        "flagged": b < O2_FLOOR or a < O2_FLOOR or abs(a - b) > O2_DROP})
    return out


def table_checks(csv_path: Path) -> list[dict]:
    rows = list(csv.DictReader(Path(csv_path).open(encoding="utf-8-sig")))
    key = lambda r, s: next((v for k, v in r.items() if k and s.lower() in k.lower()), None)  # noqa: E731
    flags = []
    for r in rows:
        t = (r.get("Test #") or "").strip()
        o2i, o2f = _num(key(r, "initial O2")), _num(key(r, "final O2"))
        coi, cof = _num(key(r, "Initial CO (")), _num(key(r, "Final CO ("))
        for name, v in (("initial O2", o2i), ("final O2", o2f)):
            if v is not None and v < O2_FLOOR:
                flags.append({"test": t, "check": "o2_implausible", "field": name, "value": v, "floor": O2_FLOOR})
        if o2i is not None and o2f is not None and o2i - o2f > O2_DROP:
            flags.append({"test": t, "check": "o2_drop", "value": round(o2i - o2f, 2)})
        if o2i is not None and o2f is not None and o2f - o2i > O2_DROP:
            flags.append({"test": t, "check": "o2_rise", "value": round(o2f - o2i, 2)})
        for name, v in (("initial CO", coi), ("final CO", cof)):
            if v is not None and v < 0:
                flags.append({"test": t, "check": "negative_concentration", "field": name, "value": v})
        for name in ("final O2", "Final CO2", "Final CO ("):
            raw = key(r, name)
            if raw is not None and raw.strip() == "":
                flags.append({"test": t, "check": "missing_value", "field": name.strip(" (")})
    return flags


def frame_checks(frames: list[dict]) -> list[dict]:
    """frames: dicts with t_s, exposure_s, optional brightness (sum of the band profile) and sat_px."""
    flags = []
    for i in range(1, len(frames)):
        dt = frames[i]["t_s"] - frames[i - 1]["t_s"]
        if dt <= 0:
            flags.append({"frame": i, "check": "time_not_increasing", "dt_s": round(dt, 3)})
        elif dt > GAP_S:
            flags.append({"frame": i, "check": "time_gap", "dt_s": round(dt, 2)})
        if abs(frames[i]["exposure_s"] - frames[i - 1]["exposure_s"]) > 1e-9:
            flags.append({"frame": i, "check": "exposure_change", "severity": "info", "from_s": frames[i - 1]["exposure_s"], "to_s": frames[i]["exposure_s"]})
    for i, f in enumerate(frames):
        if f.get("sat_px"):
            flags.append({"frame": i, "check": "saturation", "sat_px": f["sat_px"]})
    lit = [f for f in frames if (f.get("brightness") or 0) > 0]
    if len(lit) >= 7:
        lb = [math.log(f["brightness"] / f["exposure_s"]) for f in lit]
        res = []
        for i in range(2, len(lb) - 2):
            w = sorted(lb[i - 2:i + 3])
            res.append(lb[i] - w[2])
        mad = sorted(abs(r) for r in res)[len(res) // 2]
        scatter = 1.4826 * mad
        if scatter > FLICKER_REL:
            flags.append({"frame": None, "check": "brightness_flicker", "robust_scatter": round(scatter, 4), "threshold": FLICKER_REL})
    return flags


def overlay_checks(readings: list[tuple[float, float]]) -> list[dict]:
    """readings: (t_s, display) in time order. Flags a value that changes and returns at the next reading."""
    flags = []
    for i in range(1, len(readings) - 1):
        a, b, c = readings[i - 1][1], readings[i][1], readings[i + 1][1]
        if b != a and c == a:
            flags.append({"t_s": readings[i][0], "check": "display_flicker", "values": [a, b, c]})
    return flags
