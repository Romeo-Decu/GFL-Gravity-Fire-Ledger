# Portable black box

**Status:** designed (IDEA-005). Not built.

## What we want
A small, self-contained package that carries the sealed core of a project and can be verified anywhere, offline, from a USB stick, without trusting the machine it was made on. The package holds:
- the Evidence Vault index;
- the ledger;
- the public keys;
- a verifier.

The same pattern serves any project, scientific or not, and AI-assisted projects in particular: a sealed core, a regenerated state file and a cold archive.

## Design
- **Contents:**
  - `ledger.jsonl`;
  - `keys/*.pub.json`;
  - the vault manifest (tier 1–2 hashes and sizes);
  - anchors (Git commit IDs, RFC 3161 tokens);
  - a single-file verifier: the browser page already in GFL (`ledger-verify.js`), plus a command-line twin.
- **Verification without network:**
  - recompute every hash, link and signature;
  - check RFC 3161 tokens against the bundled TSA certificate;
  - report each object as `ok`, `altered` or `missing`.
- **Optional payload:** the tier 1–2 bytes themselves, when size allows.

## Validation
- Verify the same package on three operating systems and in a browser with no network; results must be identical.
- Tamper suite as for the ledger, plus a removed-file test (must say "missing").

## Blocking conditions
- TSA certificate chains expire; the package must carry the chain valid at timestamp time.
- Large primary data (hundreds of GiB) cannot travel in the package; the package then proves integrity of what is present and lists what is not.
