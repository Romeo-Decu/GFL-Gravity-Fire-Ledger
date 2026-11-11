"""python -m gfl_analysis <command>: the analysis modules from the command line (JSON on stdout)."""
from __future__ import annotations

import argparse
import json
import sys

from . import anomaly, cram1, flow, gates, records, regime, uq


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gfl_analysis")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("flow").add_argument("display", type=float)
    sub.add_parser("regime").add_argument("display", type=float)
    c = sub.add_parser("cram1"); c.add_argument("thickness_um", type=float); c.add_argument("--measured", type=float)
    u = sub.add_parser("uq"); u.add_argument("run"); u.add_argument("display", type=int)
    t = sub.add_parser("transfer"); t.add_argument("src"); t.add_argument("src_display", type=int); t.add_argument("tgt"); t.add_argument("tgt_display", type=int)
    a = sub.add_parser("anomaly-table"); a.add_argument("csv")
    a = ap.parse_args(argv)
    if a.cmd == "flow":
        out = flow.air_display_to_velocity(a.display)
    elif a.cmd == "regime":
        out = regime.classify(a.display)
    elif a.cmd == "cram1":
        out = cram1.compare(a.thickness_um, a.measured) if a.measured else cram1.predict(a.thickness_um)
    elif a.cmd == "uq":
        out = uq.from_rates_file(records.RATES / f"{a.run}_RW4_RATES.json", a.display)
    elif a.cmd == "transfer":
        out = gates.assess_pair(records.record(a.src, a.src_display), records.record(a.tgt, a.tgt_display))
    else:
        out = anomaly.table_checks(a.csv)
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
