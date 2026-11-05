"""Tamper tests for the GFL Evidence Vault ledger (WP-L).

Each test builds a small ledger in a temporary directory, then alters it in one way
and checks that `verify` detects exactly that alteration.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

try:
    from gfl_ledger.core import Ledger, LedgerError, generate_key, load_private, load_public_keys, sha256_file, verify
    HAVE_CRYPTO = True
except Exception:  # pragma: no cover
    HAVE_CRYPTO = False


@unittest.skipUnless(HAVE_CRYPTO, "cryptography not installed")
class LedgerTamperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.data = self.tmp / "data"
        self.data.mkdir()
        (self.data / "raw.bin").write_bytes(b"NASA raw bytes")
        (self.data / "table.csv").write_text("a,b\n1,2\n")
        (self.data / "derived.json").write_text('{"v": 2.27}')
        self.kid = generate_key(self.tmp / "k.pem", self.tmp / "keys" / "t.pub.json")
        self.pk = load_private(self.tmp / "k.pem")
        self.led = Ledger(self.tmp / "ledger.jsonl")

        def o(n):
            p = self.data / n
            return {"root": "d", "location": n, "sha256": sha256_file(p), "bytes": p.stat().st_size}
        self.raw = self.led.append({"type": "ingest", "object": o("raw.bin")}, self.pk, self.kid)["entry_hash"]
        self.tab = self.led.append({"type": "source_table", "object": o("table.csv")}, self.pk, self.kid)["entry_hash"]
        self.der = self.led.append({"type": "derivation", "object": o("derived.json"), "parents": [self.raw, self.tab],
                                    "method": {"tool": "t.py"}}, self.pk, self.kid)["entry_hash"]

    def run_verify(self):
        return verify(self.led, load_public_keys(self.tmp / "keys"), {"d": self.data})

    def lines(self):
        return self.led.path.read_text().splitlines()

    def write(self, lines):
        self.led.path.write_text("\n".join(lines) + "\n")

    def test_intact(self):
        r = self.run_verify()
        self.assertTrue(r["chain_ok"], r["chain_errors"])
        self.assertEqual(r["objects"], {"ok": 3, "altered": 0, "missing": 0})

    def test_raw_byte_changed_is_sealed_alteration(self):
        (self.data / "raw.bin").write_bytes(b"NASA raw bytez")
        r = self.run_verify()
        self.assertEqual(r["objects"]["altered"], 1)
        self.assertEqual(len(r["sealed_altered"]), 1)

    def test_missing_raw_reported_not_ok(self):
        (self.data / "raw.bin").unlink()
        r = self.run_verify()
        self.assertEqual(r["objects"]["missing"], 1)
        self.assertEqual(r["objects"]["ok"], 2)

    def test_entry_edited(self):
        ls = self.lines()
        e = json.loads(ls[1])
        e["object"]["sha256"] = "0" * 64
        ls[1] = json.dumps(e, sort_keys=True)
        self.write(ls)
        self.assertFalse(self.run_verify()["chain_ok"])

    def test_entry_edited_and_rehashed_breaks_signature_and_link(self):
        from gfl_ledger.core import canonical, sha256_bytes
        ls = self.lines()
        e = json.loads(ls[1])
        e["note"] = "administrator edit"
        body = {k: v for k, v in e.items() if k not in ("entry_hash", "sig")}
        e["entry_hash"] = sha256_bytes(canonical(body))
        ls[1] = json.dumps(e, sort_keys=True)
        self.write(ls)
        errs = " ".join(self.run_verify()["chain_errors"])
        self.assertIn("signature invalid", errs)
        self.assertIn("prev link broken", errs)

    def test_entry_removed(self):
        ls = self.lines()
        self.write([ls[0], ls[2]])
        self.assertFalse(self.run_verify()["chain_ok"])

    def test_entries_reordered(self):
        ls = self.lines()
        self.write([ls[1], ls[0], ls[2]])
        self.assertFalse(self.run_verify()["chain_ok"])

    def test_foreign_key_rejected(self):
        generate_key(self.tmp / "k2.pem", self.tmp / "other" / "x.pub.json")
        led2 = Ledger(self.led.path)
        led2.append({"type": "ingest"}, load_private(self.tmp / "k2.pem"), "ed25519:intruder")
        self.assertIn("unknown signing key", " ".join(self.run_verify()["chain_errors"]))

    def test_derivation_without_method_refused(self):
        with self.assertRaises(LedgerError):
            self.led.append({"type": "derivation", "parents": [self.raw]}, self.pk, self.kid)

    def test_unknown_parent_refused(self):
        with self.assertRaises(LedgerError):
            self.led.append({"type": "derivation", "parents": ["f" * 64], "method": {"tool": "x"}}, self.pk, self.kid)

    def test_supersession_allows_changed_derived_file(self):
        (self.data / "derived.json").write_text('{"v": 2.32}')
        self.assertEqual(self.run_verify()["objects"]["altered"], 1)
        p = self.data / "derived.json"
        self.led.append({"type": "supersession", "supersedes": self.der, "parents": [self.raw, self.tab],
                         "method": {"tool": "t.py", "params": {"thr": "relative"}},
                         "object": {"root": "d", "location": "derived.json", "sha256": sha256_file(p), "bytes": p.stat().st_size}},
                        self.pk, self.kid)
        r = self.run_verify()
        self.assertTrue(r["chain_ok"], r["chain_errors"])
        self.assertEqual(r["objects"]["altered"], 0)

    def test_supersession_needs_target(self):
        with self.assertRaises(LedgerError):
            self.led.append({"type": "supersession", "method": {"tool": "x"}}, self.pk, self.kid)


if __name__ == "__main__":
    unittest.main()
