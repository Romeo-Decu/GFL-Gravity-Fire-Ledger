import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { verifyLedger, canonical, parseRaw } from "../src/ledger-verify.js";

const ledger = readFileSync(new URL("../data/ledger.jsonl", import.meta.url), "utf8");
const keys = ["release-a.pub.json", "owner.pub.json"].map((f) => JSON.parse(readFileSync(new URL(`../data/${f}`, import.meta.url), "utf8")));

test("every ledger entry verifies in JavaScript exactly as in Python", async () => {
  const r = await verifyLedger(ledger, keys);
  const bad = r.filter((x) => !x.ok);
  assert.equal(bad.length, 0, JSON.stringify(bad.slice(0, 3).map((b) => [b.seq, b.errors])));
  assert.ok(r.length >= 100);
});

test("tampering one character is detected", async () => {
  const lines = ledger.split("\n").filter(Boolean);
  lines[5] = lines[5].replace(/"bytes": (\d+)/, (m, n) => `"bytes": ${Number(n) + 1}`);
  const r = await verifyLedger(lines.join("\n"), keys);
  assert.equal(r[5].ok, false);
  assert.ok(r[5].errors.includes("content does not match entry_hash"));
});

test("numbers keep their Python lexeme", () => {
  assert.equal(canonical(parseRaw('{"b":1.0,"a":1e-05,"c":"ș"}')), '{"a":1e-05,"b":1.0,"c":"ș"}');
});
