# WF-0011 REALITY: Validator execution (Claude), 2026-11-08

Protocol ISS-037. Each script ran in its own empty temporary directory. That directory held only the two blind CSVs, with hashes checked against `GFL_blind_B6/SHA256SUMS`. The command was `env -i PATH=/usr/bin:/bin`, `python3 -I`, with a 120 s timeout. The Python environment was the container's system interpreter: numpy 2.5.3, pandas 3.0.5, scipy 1.18.1.

Artefacts were extracted from the owner's AAL export (`AAL_WF-0011_20261108-1827.md`, sha256 92571cff…). Each one was verified byte-for-byte against the AAL `content_hash`, using the normalization in `aal.anti_loop.content_hash`:
- verification (kimi26) 29d10820…
- reality_brief (deepseek_v4) d4dfed83…

The scripts are the last ```python block of each artefact and were executed unmodified.

The deepseek_v4 script imports scipy, which violates the task's numpy+pandas constraint. It was executed as delivered, and the violation is recorded.

These outputs stay out of AAL until LOCAL_VALIDATION, so the auditor and the red team do not see them before their phases.
