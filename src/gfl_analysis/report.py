"""Per-run report: everything GFL holds about one measured run, as JSON, CSV (segments) and a self-contained HTML page
that prints to PDF from any browser. Every number is read from sealed files; nothing is computed here.

    python -m gfl_analysis report B6 --out reports/
"""
from __future__ import annotations

import csv
import html
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "data/derived/analysis/GFL_ANALYSIS_v1.json"
LEDGER = ROOT / "ledger/ledger.jsonl"
EXTERNAL = ROOT / "data/external"
AI_LABEL = "Made with AI: this report is produced by code written by Claude (Anthropic) under the direction of team CCTI."


def _seals(patterns: list[str]) -> list[dict]:
    latest = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        o = e.get("object")
        if o and any(re.search(p, o["location"]) for p in patterns):
            latest[o["location"]] = {"file": o["location"], "kept_in": "repository" if o["root"] == "repo" else "NASA PSI-25 download (outside the repository)",
                                     "sha256": o["sha256"], "bytes": o["bytes"], "ledger_seq": e["seq"], "sealed_utc": e["recorded_utc"]}
    return [latest[k] for k in sorted(latest)]


def build(run: str) -> dict:
    a = json.loads(ANALYSIS.read_text(encoding="utf-8"))
    if run not in a["runs"]:
        raise ValueError(f"{run} has no GFL measurement; measured runs: {', '.join(a['runs'])}")
    r = a["runs"][run]
    rec = r["record"]
    rates = json.loads((ROOT / rec["rate_ref"]).read_text(encoding="utf-8"))
    segs = [{"air_display": s["air_display"], "flow_cm_s": g["u_cm_s"], "t_start_s": s["t_start_s"], "t_end_s": s["t_end_s"], "frames": s["frames"],
             "rate_mm_s": s["budget"]["rate_mm_s"], "lo_mm_s": s["budget"]["reported_interval_mm_s"][0], "hi_mm_s": s["budget"]["reported_interval_mm_s"][1],
             "regime": g["regime"], "label": g["label"], "reference_segment": s["air_display"] == rec["air_display"]}
            for s, g in zip([s for s in rates["segments"] if s.get("budget")], r["regime_by_segment"])]
    n = re.sub(r"\D", "", run)
    ext = []
    if EXTERNAL.is_dir():
        for f in sorted(EXTERNAL.glob("*.json")):
            ext += [c for c in json.loads(f.read_text(encoding="utf-8"))["accepted"] if c["external"]["run"] == run]
    return {"run": run, "status": a["status"], "analysis_version": a["version"],
            "as_recorded_by_nasa": {k: rec[k] for k in ("material", "thickness_um", "width_cm", "restrictor", "o2_pct")},
            "identity": rec["identity_ref"],
            "result": {"rate_mm_s": rec["rate_mm_s"], "interval_mm_s": rec["interval_mm_s"], "air_display": rec["air_display"], "flow_cm_s": r["flow"]["value_cm_s"],
                       "rule": rec["rule"], "front_definition": rec["reference_definition"], "what_it_is": "luminous-edge spread rate (DEC-056)",
                       "bootstrap": rates["bootstrap"]},
            "segments": segs, "uncertainty": r["uq"], "theory": r["cram1"], "flow": r["flow"], "flow_independence": r["flow_independence"],
            "transfer": [t for t in a["transfer"] if run in (t["source"], t["target"])],
            "external_values": ext,
            "provenance": _seals([rf"rw4/{run}_", rf"TPB{n}_?ProofSheet", r"analysis/GFL_ANALYSIS_v1\.json$", r"Experimental table/"]),
            "label": AI_LABEL,
            "source": "NASA PSI-25 BASS-II, DOI 10.60555/4qc4-de67 (public data). GFL is an independent analysis and is not endorsed by NASA."}


def to_csv(rep: dict) -> str:
    buf = io.StringIO()
    cols = ["run", "air_display", "flow_cm_s", "t_start_s", "t_end_s", "frames", "rate_mm_s", "lo_mm_s", "hi_mm_s", "regime", "label", "reference_segment"]
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    for s in rep["segments"]:
        w.writerow(dict(s, run=rep["run"]))
    return buf.getvalue()


def _e(x) -> str:
    return html.escape(str(x))


def _table(head: list[str], rows: list[list]) -> str:
    return ("<table><thead><tr>" + "".join(f"<th>{_e(h)}</th>" for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{_e(c)}</td>" for c in row) + "</tr>" for row in rows) + "</tbody></table>")


CSS = ("body{font:15px/1.5 Georgia,serif;color:#111;background:#fff;max-width:820px;margin:0 auto;padding:28px 18px}"
       "h1{font:600 26px/1.2 system-ui,sans-serif;margin:0 0 4px}h2{font:600 17px system-ui,sans-serif;margin:28px 0 8px;border-bottom:1px solid #bbb;padding-bottom:3px}"
       "table{border-collapse:collapse;width:100%;font:13px system-ui,sans-serif;margin:8px 0}th,td{border-bottom:1px solid #ccc;padding:5px 6px;text-align:left;vertical-align:top}"
       ".big{font:600 30px system-ui,sans-serif}.note{color:#444;font-size:13px}.open{border:1px solid #999;padding:8px 10px;font:13px system-ui,sans-serif}"
       "code{font-size:12px;overflow-wrap:anywhere}.wrap{overflow-x:auto}@media print{body{padding:0}h2{break-after:avoid}table{break-inside:avoid}}")


def to_html(rep: dict) -> str:
    res, uq, th, n = rep["result"], rep["uncertainty"], rep["theory"], rep["as_recorded_by_nasa"]
    l2 = uq["layer2_analyst_choice"]
    p = [f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
         f"<title>GFL report, BASS-II {_e(rep['run'])}</title><style>{CSS}</style></head><body>",
         f"<h1>BASS-II run {_e(rep['run'])}: opposed-flow flame spread</h1>",
         f"<p class=\"note\">Gravity Fire Ledger, team CCTI, NASA Space Apps 2026. {_e(rep['source'])}</p>",
         f"<p class=\"open\"><strong>Status: {_e(rep['status'])}.</strong> {_e(rep['label'])}</p>",
         "<h2>1. The run, as recorded by NASA</h2>",
         _table(["Material", "Thickness", "Width", "Flow restrictor", "Initial O₂"],
                [[n["material"], f"{n['thickness_um']:g} µm", f"{n['width_cm']:g} cm", n["restrictor"], f"{n['o2_pct']:g} %"]]),
         f"<p class=\"note\">Run identity: {_e(rep['identity'])}.</p>",
         "<h2>2. Result</h2>",
         f"<p class=\"big\">{res['rate_mm_s']:.2f} mm/s</p>",
         f"<p>Reported interval {res['interval_mm_s'][0]:.2f}–{res['interval_mm_s'][1]:.2f} mm/s, at air display {res['air_display']} "
         f"({res['flow_cm_s']:.2f} cm/s on the duct centreline by NASA's fan calibration). This is a {_e(res['what_it_is'])}: the speed of the "
         f"flame's luminous edge, taken at {_e(res['front_definition'].replace('rel_peak_', ''))} of each frame's peak brightness, under the frozen window rule {_e(res['rule'])}.</p>",
         "<h2>3. Every constant-flow segment that qualified</h2><div class=\"wrap\">",
         _table(["Air display", "Flow, cm/s", "Time, s", "Frames", "Rate, mm/s", "Interval, mm/s", "Regime indication (order of magnitude)"],
                [[f"{s['air_display']}{' (reported)' if s['reference_segment'] else ''}", f"{s['flow_cm_s']:.2f}", f"{s['t_start_s']:.1f}–{s['t_end_s']:.1f}", s["frames"],
                  f"{s['rate_mm_s']:.2f}", f"{s['lo_mm_s']:.2f}–{s['hi_mm_s']:.2f}", s["label"]] for s in rep["segments"]]),
         f"</div><p class=\"note\">Dependence on flow across thermal-regime segments: {_e(rep['flow_independence'].get('reading') or rep['flow_independence']['reason'])}.</p>",
         "<h2>4. Uncertainty, in three layers</h2>",
         _table(["Layer", "What it covers", "Value"],
                [["1. Statistical", "scatter of the frames (block bootstrap, 95 %)", f"{uq['layer1_statistical_95_mm_s'][0]:.2f}–{uq['layer1_statistical_95_mm_s'][1]:.2f} mm/s"],
                 ["2. Analyst choice", "which brightness level is called the front", f"{l2['definition_range_mm_s'][0]:.2f}–{l2['definition_range_mm_s'][1]:.2f} mm/s across definitions"]]
                + [[f"3. {u['what']}", u["evidence"], f"±{u['bound_rel'] * 100:g} % allowance" if u.get("bound_rel") else "not established: no bound"]
                   for u in uq["layer3_physical_unknowns"]]),
         f"<p class=\"note\">{_e(uq['reading'][0].upper() + uq['reading'][1:])}.</p>",
         "<h2>5. Comparison with thin-fuel theory</h2>",
         _table(["Constant", "Theoretical rate, mm/s"], [[k.replace("_", " "), f"{v:.2f}"] for k, v in th["prediction"]["rate_mm_s_by_constant"].items()]),
         f"<p>Measured rate {'inside' if th['inside_theory_band'] else 'outside'} the band of the three constants "
         f"({th['prediction']['band_mm_s'][0]:.2f}–{th['prediction']['band_mm_s'][1]:.2f} mm/s; a sensitivity range, not a prediction interval: lower end from the Delichatsios constant with F = 4.4, upper end from the de Ris constant with F = 5.5). Thin-fuel check: {_e(th['thin_check']['reading'])} "
         f"(semi-thickness over solid heating depth = {th['thin_check']['ratio_tau_over_delta']}; {_e(th['thin_check']['note'])}).</p>",
         "<p class=\"note\">Properties: " + _e("; ".join(sorted(set(th["prediction"]["sources"].values())))) + ".</p>"]
    if rep["transfer"]:
        p += ["<h2>6. Can this result inform another run?</h2><div class=\"wrap\">",
              _table(["From → to", "Conclusion", "Conditions that are only partly met"],
                     [[f"{t['source']} → {t['target']}", t["conclusion"].replace("_", " "),
                       "; ".join(k.replace("_", " ") for k, g in t["gates"].items() if g["status"] != "pass") or "none"] for t in rep["transfer"]]), "</div>"]
    if rep["external_values"]:
        p += ["<h2>Values from other sources (source-reported, not GFL measurements)</h2><div class=\"wrap\">",
              _table(["Source", "Rate, mm/s", "Method", "Reference", "Against GFL"],
                     [[c["external"]["source"], c["external"]["rate_mm_s"], c["external"]["method"], c["external"]["reference"], c["verdict"]] for c in rep["external_values"]]), "</div>"]
    p += ["<h2>What this report does not establish</h2><ul>"
          "<li>The position of the burning (pyrolysis) front: only the luminous edge is measured, and their offset may change during a run.</li>"
          "<li>The flow speed at the sample surface: the calibration is on the duct centreline.</li>"
          "<li>Run-to-run scatter: this condition was flown once.</li></ul>"
          "<p class=\"note\">These are limits of the public archive, not of the method: the data that would settle them are not in it.</p>",
          "<h2>Provenance</h2><p class=\"note\">Each file below is sealed in the signed GFL ledger; the SHA-256 lets anyone check that the bytes are the same.</p><div class=\"wrap\">",
          _table(["File", "Kept in", "Ledger entry", "SHA-256"], [[f["file"], f["kept_in"], f["ledger_seq"], f["sha256"]] for f in rep["provenance"]]),
          "</div></body></html>"]
    return "\n".join(p) + "\n"


def write(run: str, out_dir: Path) -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rep = build(run)
    files = {f"{run}_report.json": json.dumps(rep, indent=1, ensure_ascii=False) + "\n", f"{run}_report.csv": to_csv(rep), f"{run}_report.html": to_html(rep)}
    for name, text in files.items():
        (out_dir / name).write_text(text, encoding="utf-8")
    return [out_dir / n for n in files]
