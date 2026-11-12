"""Import of external results and per-run reports (DEC-062)."""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gfl_analysis import external, records, report  # noqa: E402

GOOD = {"source": "X", "run": "B6", "air_display": "3", "rate_mm_s": "2.2", "method": "m", "reference": "r"}


class External(unittest.TestCase):
    def test_missing_field_is_refused_not_repaired(self):
        row = dict(GOOD); del row["reference"]
        clean, err = external.validate(row)
        self.assertIsNone(clean)
        self.assertIn("missing reference", err)

    def test_bad_numbers_are_refused(self):
        self.assertTrue(external.validate(dict(GOOD, rate_mm_s="-1"))[1])
        self.assertTrue(external.validate(dict(GOOD, rate_mm_s="fast"))[1])
        self.assertTrue(external.validate(dict(GOOD, lo_mm_s="2.0"))[1])
        self.assertTrue(external.validate(dict(GOOD, lo_mm_s="2.3", hi_mm_s="2.5"))[1])

    def test_value_keeps_source_label_and_is_compared(self):
        clean, _ = external.validate(GOOD)
        c = external.compare(clean)
        self.assertEqual(c["external"]["label"], "source-reported, not a GFL measurement")
        g = records.record("B6", 3)
        self.assertEqual(c["ratio_external_over_gfl"], round(2.2 / g["rate_mm_s"], 3))
        self.assertEqual(c["verdict"], "external value inside the GFL interval")
        self.assertIn("no interval", c["note"])

    def test_interval_overlap(self):
        far, _ = external.validate(dict(GOOD, rate_mm_s="5", lo_mm_s="4.5", hi_mm_s="5.5"))
        self.assertEqual(external.compare(far)["verdict"], "intervals do not overlap")
        near, _ = external.validate(dict(GOOD, lo_mm_s="2.0", hi_mm_s="2.4"))
        self.assertEqual(external.compare(near)["verdict"], "intervals overlap")

    def test_unknown_run_and_unmeasured_run(self):
        a, _ = external.validate(dict(GOOD, run="ZZ99"))
        self.assertEqual(external.compare(a)["verdict"], "run not in the NASA table")
        b, _ = external.validate(dict(GOOD, run="B15"))
        self.assertEqual(external.compare(b)["verdict"], "no GFL measurement for this run and air display")

    def test_csv_and_json_files(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "x.csv"
            p.write_text("source,run,air_display,rate_mm_s,method,reference\nX,B6,3,2.2,m,r\nX,B6,3,,m,r\n", encoding="utf-8")
            out = external.import_file(p)
            self.assertEqual((len(out["accepted"]), len(out["refused"])), (1, 1))
            self.assertEqual(out["refused"][0]["row"], 2)
            q = Path(d) / "x.json"
            q.write_text(json.dumps(GOOD), encoding="utf-8")
            self.assertEqual(len(external.import_file(q)["accepted"]), 1)


class Report(unittest.TestCase):
    def test_report_numbers_come_from_the_sealed_files(self):
        rep = report.build("B11")
        g = records.record("B11", 2)
        self.assertEqual(rep["result"]["rate_mm_s"], g["rate_mm_s"])
        self.assertEqual(rep["result"]["interval_mm_s"], g["interval_mm_s"])
        self.assertIn("open", rep["status"])
        self.assertTrue(all(len(f["sha256"]) == 64 and isinstance(f["ledger_seq"], int) for f in rep["provenance"]))
        self.assertTrue(rep["provenance"])

    def test_html_and_csv(self):
        rep = report.build("B6")
        html = report.to_html(rep)
        self.assertIn(f"{rep['result']['rate_mm_s']:.2f} mm/s", html)
        self.assertIn("Made with AI", html)
        self.assertIn("not established", html)
        self.assertNotIn("<script", html)
        rows = report.to_csv(rep).strip().splitlines()
        self.assertEqual(len(rows), 1 + len(rep["segments"]))

    def test_deterministic(self):
        self.assertEqual(report.to_html(report.build("B9")), report.to_html(report.build("B9")))

    def test_unmeasured_run_is_refused(self):
        with self.assertRaises(ValueError):
            report.build("B15")


if __name__ == "__main__":
    unittest.main()
