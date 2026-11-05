"""GFL Evidence Vault ledger (WP-L, DEC-018 / DEC-023 / DEC-025 / DEC-027).

Append-only, hash-chained, Ed25519-signed record of every object GFL relies on:

  tier 1  ingest        primary instrument file (raw bytes as published)   - sealed
  tier 2  source_table  source table exactly as published                  - sealed
  tier 3  derivation    any analysis output (method, code hash, params, parents)
  tier 4  supersession  a newer derivation that explicitly replaces an older one
          anchor        external anchor of the chain head (Git commit, RFC 3161)

Claim wording: tamper-evident, not tamper-proof.
"""
from .core import Ledger, LedgerError, canonical, sha256_bytes, sha256_file  # noqa: F401

__version__ = "0.1.0"
