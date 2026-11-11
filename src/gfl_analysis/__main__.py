"""python -m gfl_analysis <command>: the analysis modules from the command line (JSON on stdout)."""
from __future__ import annotations

import argparse
import json
import sys

from . import anomaly, cram1, flow, gates, predict, records, regime, uq


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="gfl_analysis")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("flow").add_argument("display", type=float)
    sub.add_parser("regime").add_argument("display", type=float)
    c = sub.add_parser("cram1"); c.add_argument("thickness_um", type=float); c.add_argument("--measured", type=float)
    u = sub.add_parser("uq"); u.add_argument("run"); u.add_argument("display", type=int)
    t = sub.add_parser("transfer"); t.add_argument("src"); t.add_argument("src_display", type=int); t.add_argument("tgt"); t.add_argument("tgt_display", type=int)
    a = sub.add_parser("anomaly-table"); a.add_argument("csv")
    p = sub.add_parser("propose", help="pre-registered test: expected rate of a target run from a measured reference")
    p.add_argument("target"); p.add_argument("target_display", type=int); p.add_argument("--reference", default="B6"); p.add_argument("--reference-display", type=int, default=3)
    p.add_argument("--law", choices=list(predict.LAWS), default="thin_fuel_inverse_thickness")
    e = sub.add_parser("score", help="score a registered prediction against the measured target")
    e.add_argument("registry"); e.add_argument("target"); e.add_argument("--law", default="thin_fuel_inverse_thickness")
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
    elif a.cmd == "propose":
        out = predict.propose(records.record(a.reference, a.reference_display), records.record(a.target, a.target_display), a.law)
    elif a.cmd == "score":
        reg = json.load(open(a.registry))
        pr = next(x for x in reg["predictions"] if x["target"] == a.target and x["law"] == a.law)
        ref = records.record(pr["reference"], pr["reference_air_display"])
        out = {"prediction": pr, "result": predict.evaluate(pr, records.record(a.target, pr["target_air_display"]), ref)}
    else:
        out = anomaly.table_checks(a.csv)
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
