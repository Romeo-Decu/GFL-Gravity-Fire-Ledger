# Evidence Vault (sealed tiers 1–2)

**Status:** partial. The rules, the ledger tiers and the key custody are in operation; write-once storage and a vault package are designed.
**Decisions:** DEC-025 (vault sealed after phase 2), DEC-027 (name and model), DEC-031 (separate owner key).

## What we want
- **What it holds:** the primary evidence of every experiment.
  - Tier 1: instrument files exactly as delivered, plus the instrument record (model, resolution, calibration, clock).
  - Tier 2: source tables exactly as published. Any value the source computed is flagged `source_derived` and never corrected.
- **What it guarantees:** once sealed, nothing in the vault can change without detection, including by the project owner or by an AI agent.
- **Where analyses live:** outside the vault, in the Derivation Ledger (tiers 3–4). They stay exposed to correction.

## What exists today
- Every primary file is content-addressed: its SHA-256 is recorded in a signed ledger entry, tier 1 or tier 2.
- The ledger is append-only and hash-chained. The chain head is anchored in Git and with RFC 3161 timestamps (FreeTSA).
- **Two keys, two roles:**
  - The pipeline key signs processing entries.
  - Only the owner's key can sign approvals.
  - The owner key and the pipeline key backup are held offline by the owner.
- **Missing raw files are reported as "missing", never as verified.** Raw NASA bytes are not stored in Git; the ledger keeps their hashes.

## How we will finish it
1. **Write-once storage.** Object-lock bucket (WORM, compliance mode) or optical/offline media for tier 1–2 bytes, addressed by SHA-256.
2. **Seal event.** A signed ledger entry listing every tier 1–2 hash. After it, only new entries can be added, never edits.
3. **Restore drill.** Rebuild the project from the vault and the ledger alone, timed and recorded.

## Validation
- Tamper tests: alter one byte, one entry, one link or one signature; verification must fail (already 12 tests for the ledger).
- Restore drill reproduces every derived value from vault bytes.

## Blocking conditions
- Cost and custody of WORM storage for about 256 GiB of PSI-25 data.
- The owner must keep the offline key copies; loss of the owner key ends owner approvals (no recovery by design).
