# Gravity Fire Ledger (GFL)

**Microgravity Combustion Analysis Platform: comparability and transferability.** It measures flame spread from NASA's raw images under rules frozen in advance, seals every step in a ledger your browser re-verifies, and maps all 24 combustion investigations in NASA's Physical Sciences Informatics repository by fire-safety function: what carries over from one experiment to another, and why the rest does not. Team CCTI, NASA Space Apps 2026, challenge "Flame in Freefall". Made with AI, checked by re-execution.

GFL keeps three questions apart that are often conflated:

1. **Relevance:** does a source address the question?
2. **Comparability:** are the governing conditions characterised well enough for the phenomenon and outcome?
3. **Transferability:** can a finding inform another context, and within which declared limits?

Safeguards: unknown is never compatible; a conflict between sources is not read as a physical incompatibility; source-reported values are not GFL measurements; software execution does not validate combustion physics.

**New here? Open [`START_HERE.md`](START_HERE.md).** To see the dashboard: double-click `START_GFL.bat` (Windows) or run `./START_GFL.sh` (macOS, Linux); it needs only Python 3.10 or later.

## What is in this repository today

| Part | What it does | Where |
|---|---|---|
| Signed ledger | Append-only, hash-chained, Ed25519-signed record of every ingest, derivation, supersession and approval; anchored in Git and RFC 3161 | `src/gfl_ledger`, `ledger/` |
| B6 measurement | Flame-front measurement on the 77 raw NEF stills of NASA BASS-II run B6, window rule fixed before fitting, uncertainty by component | `tools/flame_front.py`, `tools/b6_window_rule.py`, `docs/analysis/AR-001_*` |
| Comparable-run ranking | Every row of NASA's BASS-II experimental table ranked against B6, condition by condition; unknown counts against | `tools/rank_comparable_runs.py` |
| Fire-safety evidence map | For seven fire-safety functions: which of NASA's 24 PSI combustion investigations give evidence, under which stated conditions, and between which a finding may be carried; two AI extractors, every value checked word for word against NASA's record; NASA's INDUS encoder for relevance | `src/gfl_map`, `tools/evidence_map_*.py`, `tools/indus_rank.py`, `docs/GFL_EVIDENCE_MAP_PROTOCOL_v1.md` |
| Analysis modules | Flow calibration, thin-fuel theory, regime, three-layer uncertainty, anomaly detection, transfer gates computed from data, per-run reports | `src/gfl_analysis` |
| Transfer engine | Deterministic decision on whether a finding can inform another context, with the blocking dimension named | `src/fif_transfer`, `configs/` |
| AI findings | Claims from seven AI models (blind analysts, red teams, auditor) ranked by what GFL's re-execution showed; summaries pass an automatic citation check | `research/fixtures/AI_FINDINGS_v1.json`, `tools/check_citations.py` |
| MCP server | Read-only access for any AI client: memory, records, ledger check, run ranking, transfer engine | `src/gfl_mcp` |
| Experiment memory | Every result, decision, issue and idea with its history, including failures | `docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md` |
| Dashboard | The case file, the rate, AI findings, transferability, comparable runs, NASA families, memory, vault; re-verifies the ledger and its own data in the browser | `visualization/gfl.html` |

## Current result

B6, BASS-II, 100 µm PMMA film, air display 3 (3.02 cm/s on the duct centreline by NASA's fan calibration; 18.5–28.6 s, 10 frames): luminous-edge spread rate **2.20 mm/s** under the frozen rule R-W4 (front at half of peak brightness), reported interval 1.91–2.37 mm/s. History, kept in the ledger: 1.99 mm/s under the earlier rule R-W2 (front at 0.1 of peak) and 2.274 ± 0.094 mm/s from a window chosen by hand (RES-001). Six more runs were measured with the same rule: B9, B11, B13 at 21 % oxygen and B19, B20 at 17 % (B16 is not measurable under it). Four predictions were sealed before their runs were acquired: one supported, one not supported, two not testable; all are shown. The data come from NASA's public PSI archive, the source named by the challenge. The archive does not contain the pyrolysis front, the flow at the sample surface or repeat runs; GFL states these as limits of the evidence.

## Run it

```bash
python -m pytest -q tests                                   # software tests
PYTHONPATH=src python -m gfl_ledger verify --allow-missing  # ledger: hashes, chain, signatures
PYTHONPATH=src python -m gfl_mcp                            # MCP server on stdio
./START_GFL.sh   (Windows: START_GFL.bat)                   # the dashboard, on this computer
```

Raw NASA data are fetched reproducibly into `FIF_DATA`, outside Git (`tools/psi25_fetch.py`); only manifests, hashes and derived tables are committed. Without the raw bytes, `verify` reports those objects as missing, never as verified.

MCP client configuration: `{"command": "python", "args": ["-m", "gfl_mcp"], "env": {"PYTHONPATH": "<repo>/src"}}`.

## Scientific status

GFL is a research prototype. It is not a fire-prediction system, a spacecraft fire-safety certification tool or a validated combustion model. Six BASS-II runs (B6, B9, B11, B13, B19, B20) have been measured under a window rule frozen before each run, with run identity confirmed against NASA proof sheets; the data are NASA's public PSI archive, the source named by the challenge (DEC-068). The analysis modules are in `src/gfl_analysis` (A0–A7). The other NASA families are identified and kept separate. Status of every function, built, partial or designed: `research/fixtures/GFL_CAPABILITIES_v1.json` and the dashboard's function map. AI and tool use, and who did what: `docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md`.

## Project control

- Release scope: [Release A Scope & Acceptance](docs/RELEASE_A_SCOPE_AND_ACCEPTANCE_v1.0.md)
- Register of decisions, results, issues and ideas: [register](docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md)
- Master map: [Project Master Map](docs/PROJECT_MASTER_MAP_AND_COMPLETION_ROADMAP_v1.0.md)

The first case selected (B3) is kept as history: its link to the published 2.2 mm/s value was never established, and B6 became the measured case.
