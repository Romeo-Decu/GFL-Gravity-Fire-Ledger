# GFL icon catalogue v1 (59 icons)

Every icon is authored geometry in `make_icons.py`, in the same grammar as the mark. Each one comes in a dark version (`*.svg`) and a light version (`light/*.svg`). The table maps GFL functions, taken from the repository, the register and the MVP matrix, to their icon.

## Ledger and evidence (WP-L, `src/gfl_ledger`)
| Function | Icon |
|---|---|
| Ingest of a primary file (entry type 1) | `ingest` |
| SHA-256 content address / seal | `seal` |
| Append-only hash chain | `ledger` |
| Source table (entry type 2) | `dataset` |
| Derivation (entry type 3) | `derivation` |
| Supersession (entry type 4) | `supersession` |
| Pipeline signature (Ed25519) | `key` |
| Owner signature / approval (DEC-031) | `owner_key`, `approval` |
| Git anchor | `anchor_git` |
| RFC 3161 timestamp (FreeTSA) | `timestamp` |
| `gfl verify`: OK / altered / missing | `verified`, `altered`, `missing` |
| `gfl lineage` / provenance | `lineage` |
| Qualification (qualifiers carried downstream) | `qualifier` |
| Chain of custody | `chain_of_custody` |

## Evidence Vault / black box (DEC-025, DEC-027)
| Function | Icon |
|---|---|
| Evidence Vault (sealed tiers 1–2) | `evidence_vault` |
| Black box: the portable post-GFL product, AI-project black box | `black_box` |
| Write-once (WORM) storage | `worm` |

## Data and science (MVP-01 … MVP-12, B6)
| Function | Icon |
|---|---|
| NASA data source / PSI-25 archive | `source` |
| Experiment / test (BASS-II run) | `experiment` |
| Image frame / NEF still | `frame` |
| Exposure / radiometry audit | `exposure` |
| Spatial calibration (ruler scale) | `scale` |
| Flame front definition | `flame_front` |
| Spread rate (x–t fit) | `spread_rate` |
| Uncertainty quantification (MVP-11) | `uncertainty` |
| Experiment comparison (MVP-02) | `comparison` |
| Physics-based similarity (MVP-03) | `similarity` |
| Evidence-backed synthesis (MVP-04) | `synthesis` |
| Transferability (MVP-12) | `transferability` |
| Probabilistic anomaly detection (MVP-10) | `anomaly` |
| CRAM-1 thermodynamics and transport (MVP-07) | `thermo` |
| CRAM-2 combustion regimes (MVP-08) | `regime` |
| CRAM-3 nonlinear dynamics (MVP-09) | `nonlinear` |
| Microgravity context | `microgravity` |

## Process, roles and AAL
| Function | Icon |
|---|---|
| Project manager | `pm` |
| Human (owner, researcher) | `human` |
| AI agent | `ai_agent` |
| AAL orchestration | `orchestrator` |
| Pipeline / phases | `pipeline` |
| Blind analysis (independent phase) | `blind` |
| Red team | `red_team` |
| Independent auditor | `auditor` |
| Validator (re-execution) | `validator` |
| Decision (register) | `decision` |
| Issue | `issue` |
| Idea | `idea` |
| Reproducibility | `reproducible` |
| Code / script | `code` |
| Dashboard | `dashboard` |
| Search | `search` |
| Export | `export` |

## Evidence states (canonical graph contract, controlled vocabulary)
| State | Icon |
|---|---|
| Established relation | `established` |
| Provisional relation | `provisional` |
| Unresolved relation | `unresolved` |
| Unknown value (never filled with a guess) | `unknown` |
| Information | `info` |
