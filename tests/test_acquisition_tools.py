"""Offline tests for the PSI-25 acquisition tools (no network access)."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fetch = _load("psi25_fetch")
fam = _load("family_assets")

TREE = {"files": [
    {"displayName": "Raw Data", "key": "psi-data/PSI-25/Raw Data/", "files": [
        {"key": "psi-data/PSI-25/Raw Data/PSI-25_Raw Data_BASS_GMT188_SAMPLE_153_TESTB6.mp4",
         "bytes_size": 7590000.0, "size": "7.24 MB", "version": 4, "directory": False, "files": []},
        {"displayName": "Reduced Gravity", "key": "x/", "files": [
            {"key": "psi-data/PSI-25/Raw Data/PSI-25_Raw Data_GMT2014_183_BASS_S150M_TPB16ProofSheet.pdf",
             "bytes_size": 1000, "size": "1 KB", "version": 2, "directory": False, "files": []}]}]},
    {"displayName": "Experimental table", "key": "psi-data/PSI-25/Experimental table/", "files": [
        {"key": "psi-data/PSI-25/Experimental table/PSI-25_Experimental table_BASS-II.csv",
         "bytes_size": 16590, "size": "16.2 KB", "version": 1, "directory": False, "files": []}]},
]}

TABLE = {
    "B6": {"sample": "153m", "gmt": "188"},
    "B15": {"sample": "149m", "gmt": "188"},
    "B16": {"sample": "150m", "gmt": "183"},
    "B17": {"sample": "175m", "gmt": "183"},
    "B3": {"sample": "148", "gmt": "50"},
}


class TestManifestFlattening(unittest.TestCase):
    def test_folders_dropped_files_kept_with_integer_bytes(self):
        files = fetch.flatten_tree(TREE)
        self.assertEqual(len(files), 3)
        self.assertTrue(all(isinstance(f["bytes"], int) for f in files))
        self.assertEqual({f["category"] for f in files}, {"Raw Data", "Experimental table"})

    def test_nested_folder_path_preserved(self):
        f = [x for x in fetch.flatten_tree(TREE) if x["name"].endswith("ProofSheet.pdf")][0]
        self.assertEqual(f["folder"], "Raw Data/Reduced Gravity")
        self.assertEqual(f["version"], 2)


class TestFamilyJoins(unittest.TestCase):
    def test_parse_both_naming_conventions(self):
        self.assertEqual(fam.parse_name("PSI-25_Raw Data_BASS_GMT50_SAMPLE_148_TEST_B3 original videos.zip"),
                         {"gmt": "50", "sample": "148", "test": "B3"})
        self.assertEqual(fam.parse_name("PSI-25_Raw Data_GMT2014_183_BASS_S150M_TPB16ProofSheet.pdf")["test"], "B16")

    def test_test_id_boundary_b1_is_not_b15(self):
        self.assertEqual(fam.parse_name("BASS_GMT188_SAMPLE_149_TESTB15.mp4")["test"], "B15")

    def test_kind_classification_includes_psi_misspelling(self):
        self.assertEqual(fam.asset_kind("X_TESTB9 original vidoes.zip"), "original_video_archive")
        self.assertEqual(fam.asset_kind("X_TESTB6_2ND_VIEW.mp4"), "second_view_video")
        self.assertEqual(fam.asset_kind("X_TESTB6_Still_Sequence.mp4"), "still_sequence_video")

    def _row(self, name, tests):
        man = {"files": [{"name": name, "version": 4, "bytes": 1}]}
        return fam.build(man, TABLE, tests)

    def test_matching_sample_is_not_flagged_and_gmt_leading_zero_ignored(self):
        r = self._row("GMT2014_050_BASS_S148M_TPB3_ProofSheet.pdf", ["B3"])[0]
        self.assertEqual(r["join_status"], "filename_matches_table")

    def test_mislabelled_sample_is_flagged_not_corrected(self):
        r = self._row("BASS_GMT183_SAMPLE_175_TESTB15.mp4", ["B15"])[0]
        self.assertEqual(r["join_status"], "conflict_unresolved")
        self.assertEqual(r["test_id_in_filename"], "B15")  # filename label preserved
        self.assertIn("B17", r["issues"])


class TestCommittedMetadata(unittest.TestCase):
    def test_manifest_and_log_are_consistent(self):
        man = json.loads((ROOT / "data/manifests/PSI-25_v4_manifest.json").read_text(encoding="utf-8"))
        log = json.loads((ROOT / "data/manifests/PSI-25_acquisition_log.json").read_text(encoding="utf-8"))
        self.assertEqual(man["file_count"], len(man["files"]))
        by_name = {f["name"]: f for f in man["files"]}
        for rec in log["records"]:
            self.assertIn(rec["name"], by_name)
            self.assertEqual(rec["bytes"], by_name[rec["name"]]["bytes"])
            self.assertRegex(rec["sha256"], r"^[0-9a-f]{64}$")

    def test_no_raw_media_committed(self):
        tracked = [p for p in ROOT.rglob("*") if ".git" not in p.parts and p.is_file()]
        bad = [p for p in tracked if p.suffix.lower() in {".ts", ".mp4", ".zip", ".nef", ".mov"}]
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()


class TestFlameFrontMath(unittest.TestCase):
    """Pure-function checks for tools/flame_front.py (no raw data needed)."""

    @classmethod
    def setUpClass(cls):
        try:
            cls.ff = _load("flame_front")
        except ImportError as e:  # numpy missing in a minimal environment
            raise unittest.SkipTest(str(e))

    def test_leading_edge_is_last_column_above_threshold(self):
        import numpy as np
        prof = np.array([0, 5, 9, 3, 8, 1, 0], float)
        self.assertEqual(self.ff.leading_edge(prof, 4), 4)
        self.assertIsNone(self.ff.leading_edge(prof, 10))

    def test_linfit_recovers_known_slope(self):
        import numpy as np
        t = np.arange(0, 40, 1.0)
        x = 33.4 * t + 100
        b, se, r = self.ff.linfit(t, x)
        self.assertAlmostEqual(b, 33.4, places=9)
        self.assertLess(abs(r).max(), 1e-9)

    def test_committed_b6_result_is_consistent_with_track(self):
        res = json.loads((ROOT / "data/derived/B6_SPREAD_RATE_RESULT_v0.1.json").read_text(encoding="utf-8"))
        self.assertEqual(res["evidence_status"], "measured")
        comp = res["uncertainty_components_mm_s"]
        u = (comp["fit"] ** 2 + comp["threshold_sensitivity_half_range"] ** 2 + comp["spatial_scale"] ** 2) ** 0.5
        self.assertAlmostEqual(u, res["standard_uncertainty_mm_s"], places=3)
