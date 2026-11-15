"""A0. Opposing-flow speed from the BASS-II air display (resolves ISS-013 within the limits stated)."""
from __future__ import annotations

from .sources import NASA_FAN_CAL

FACTOR = 1.0066


def air_display_to_velocity(display: float | None) -> dict:
    """Convert an AIR display reading to the calibrated flow speed in cm/s.

    The workbook gives U [cm/s] = 1.0066 x AIR, measured on the duct centreline 56 mm downstream and 36 mm from
    the bottom. It is not the speed at the sample surface (boundary layer) and carries no stated uncertainty;
    the display is an integer, so the reading itself is known to +-0.5 display units.
    """
    if display is None:
        return {"value_cm_s": None, "status": "unknown", "reason": "no display reading"}
    v = FACTOR * float(display)
    return {"value_cm_s": round(v, 4), "reading_resolution_cm_s": round(FACTOR * 0.5, 4), "factor": FACTOR,
            "location": "duct centreline, 56 mm downstream, 36 mm from bottom", "source": NASA_FAN_CAL,
            "status": "source_reported_calibration",
            "not_known": ["speed at the sample surface (boundary layer)", "calibration uncertainty (not stated)",
                          "day-to-day drift (fan calibrations differ between GMT days in the workbook)"]}
