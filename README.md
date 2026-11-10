# Gravity Fire Ledger (GFL)

**Flame in Freefall**: a scientific evidence ledger for microgravity combustion research. Team CCTI, NASA Space Apps 2026.

GFL keeps three questions apart that are often conflated:

1. **Relevance:** does a source address the question?
2. **Comparability:** are the governing conditions characterised well enough for the phenomenon and outcome?
3. **Transferability:** can a finding inform another context, and within which declared limits?

Safeguards: unknown is never compatible; a conflict between sources is not read as a physical incompatibility; source-reported values are not GFL measurements; software execution does not validate combustion physics.

## What is in this repository today

| Part | What it does | Where |
|---|---|---|
| Signed ledger | Append-only, hash-chained, Ed25519-signed record of every ingest, derivation, supersession and approval; anchored in Git and RFC 3161 | `src/gfl_ledger`, `ledger/` |
| B6 measurement | Flame-front measurement on the 77 raw NEF stills of NASA BASS-II run B6, window rule fixed before fitting, uncertainty by component | `tools/flame_front.py`, `tools/b6_window_rule.py`, `docs/analysis/AR-001_*` |
| Comparable-run ranking | Every row of NASA's BASS-II experimental table ranked against B6, condition by condition; unknown counts against | `tools/rank_comparable_runs.py` |
| Transfer engine | Deterministic decision on whether a finding can inform another context, with the blocking dimension named | `src/fif_transfer`, `configs/` |
| AI findings | Claims from seven AI models (blind analysts, red teams, auditor) ranked by what GFL's re-execution showed; summaries pass an automatic citation check | `research/fixtures/AI_FINDINGS_v1.json`, `tools/check_citations.py` |
| MCP server | Read-only access for any AI client: memory, records, ledger check, run ranking, transfer engine | `src/gfl_mcp` |
| Experiment memory | Every result, decision, issue and idea with its history, including failures | `docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md` |
| Dashboard | The case file, the rate, AI findings, transferability, comparable runs, NASA families, memory, vault; re-verifies the ledger and its own data in the browser | `visualization/gfl.html` |

## Current result

B6, BASS-II, 100 µm PMMA film, airflow display setting 3 (18.5–28.6 s): leading-edge spread rate **1.99 mm/s**, front-definition range 1.99–2.54 mm/s, **provisional**; the display setting's value in cm/s is not established (ISS-013). It replaces an earlier 2.274 ± 0.094 mm/s whose window was chosen by hand (RES-001, superseded). Literature cross-check: `docs/analysis/AR-001_LITERATURE_CROSSCHECK_v1.md` (no external expert has reviewed the physics). A prediction for run B11 was registered and timestamped before any B11 file was acquired (DEC-047).

## Run it

```bash
python -m pytest -q tests                                   # software tests
PYTHONPATH=src python -m gfl_ledger verify --allow-missing  # ledger: hashes, chain, signatures
PYTHONPATH=src python -m gfl_mcp                            # MCP server on stdio
python -m http.server 8000                                  # then open /visualization/gfl.html
```

Raw NASA data are fetched reproducibly into `FIF_DATA`, outside Git (`tools/psi25_fetch.py`); only manifests, hashes and derived tables are committed. Without the raw bytes, `verify` reports those objects as missing, never as verified.

MCP client configuration: `{"command": "python", "args": ["-m", "gfl_mcp"], "env": {"PYTHONPATH": "<repo>/src"}}`.

## Scientific status

GFL is a research prototype. It is not a fire-prediction system, a spacecraft fire-safety certification tool or a validated combustion model. One run (B6) has been measured under the window rule; the other NASA families are identified and kept separate. Status of every function, built, partial or designed: `research/fixtures/GFL_CAPABILITIES_v1.json` and the dashboard's function map. AI and tool use, and who did what: `docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md`.

## Project control

- Release scope: [Release A Scope & Acceptance](docs/RELEASE_A_SCOPE_AND_ACCEPTANCE_v1.0.md)
- Register of decisions, results, issues and ideas: [register](docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md)
- Master map: [Project Master Map](docs/PROJECT_MASTER_MAP_AND_COMPLETION_ROADMAP_v1.0.md)

The first case selected (B3) is kept as history: its link to the published 2.2 mm/s value was never established, and B6 became the measured case.
