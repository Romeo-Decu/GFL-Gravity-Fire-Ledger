# GFL diagrams as code

Each diagram is a Mermaid text source (`*.mmd`), versioned with the code it describes. GitHub renders the copies below directly. Each source states where its facts come from, and every one is checked to render with `mmdc`.

Not drawn yet, and planned for the WP5 documentation: CI and AAL Verify workflow; the role of each AI and tool (DEC-037 table); dashboard screen map.

## D01 — System architecture: one canonical core, two interfaces
Source: [`D01_system_architecture.mmd`](D01_system_architecture.mmd)

```mermaid
%% D01 — GFL system architecture: one canonical scientific core, two interfaces.
%% Source: docs/FIF_PRODUCT_MODULE_TRACEABILITY_MATRIX_v1.0.md §4, PROJECT_MASTER_MAP §4.
flowchart TB
  subgraph SRC["1 · NASA source acquisition"]
    S1[PSI-25 BASS-II archive<br/>DOI 10.60555/4qc4-de67, CC0]
    S2[Source registry · licence · version]
  end
  subgraph VAULT["Evidence Vault — sealed tiers 1–2 (DEC-025/027)"]
    V1[Tier 1 · primary instrument files<br/>NEF raw, video, instrument record]
    V2[Tier 2 · source tables as published<br/>source_derived flagged, never corrected]
  end
  subgraph LEDGER["Derivation Ledger — append-only tiers 3–4"]
    L3[Tier 3 · analyses & measurements<br/>method · code hash · parameters · parents]
    L4[Tier 4 · comparisons · updates · predictions]
    LQ[Qualifiers carried downstream<br/>approximate · provisional · manual …]
  end
  subgraph CORE["Scientific core"]
    P[Physics foundation<br/>properties · equations · validity domains]
    A[Analysis engines<br/>comparison · similarity · CRAM-1/2/3 · anomaly · UQ]
    T[Transferability & synthesis<br/>claim → evidence · explicit abstention]
  end
  subgraph TRUST["Zero-trust controls (cross-cutting)"]
    Z1[SHA-256 content addresses · hash chain]
    Z2[Ed25519 signatures · pipeline vs owner key]
    Z3[External anchors · Git + RFC 3161]
    Z4[Re-execution · blind analyses · red team · audit]
  end
  subgraph UI["Interfaces over the same core"]
    H[Human-first dashboard]
    M[Machine interface<br/>gfl verify --json · gfl lineage · JSON schemas]
  end
  S1 --> V1
  S2 --> V2
  V1 --> L3
  V2 --> L3
  L3 --> L4
  L3 -.-> LQ
  L4 -.-> LQ
  L3 --> A
  P --> A --> T --> L4
  T --> H
  T --> M
  TRUST -.-> VAULT
  TRUST -.-> LEDGER
```

## D02 — Evidence data path
Source: [`D02_evidence_data_path.mmd`](D02_evidence_data_path.mmd)

```mermaid
%% D02 — Evidence data path, source to audit result (PROJECT_MASTER_MAP §4.1).
flowchart LR
  a[Source registry] --> b[Acquisition<br/>immutable raw inventory] --> c[Format-specific extraction<br/>PDF · CSV · XLSX · NEF · video]
  c --> d[Source assertions<br/>exact locators] --> e[Identity resolution<br/>experiment · run · sample · config]
  e --> f[Typed quantities<br/>original units · lineage] --> g[(Canonical evidence graph)]
  g --> h[Provenance & integrity validation] --> i[Outcome-specific comparability] --> j[Transfer assessment<br/>uncertainty · limits]
  j --> k[Machine-readable audit result<br/>+ human explanation]
  h -. failure .-> x[Flag — never silent deletion]
```

## D03 — Ledger entry model
Source: [`D03_ledger_model.mmd`](D03_ledger_model.mmd)

```mermaid
%% D03 — GFL ledger entry model (src/gfl_ledger/core.py).
classDiagram
  class Entry {
    seq : int
    type : str
    tier : 1|2|3|4|null
    prev : sha256
    entry_hash : sha256
    key_id : ed25519 key id
    signature : Ed25519 over canonical JSON
  }
  class Ingest { tier 1 · object sha256 · source }
  class SourceTable { tier 2 · source_derived flags }
  class Derivation { tier 3 · method · code hash · parameters · parents }
  class Supersession { tier 4 · replaces · version }
  class Qualification { qualifies · qualifiers · reason }
  class Anchor { git commit | RFC 3161 token }
  class Approval { OWNER key only — DEC-031 }
  Entry <|-- Ingest
  Entry <|-- SourceTable
  Entry <|-- Derivation
  Entry <|-- Supersession
  Entry <|-- Qualification
  Entry <|-- Anchor
  Entry <|-- Approval
  Derivation --> Ingest : parents
  Derivation --> SourceTable : parents
  Supersession --> Derivation : supersedes
  Qualification --> Entry : qualifies
```

## D04 — `gfl verify`: checks and outcomes
Source: [`D04_verify_flow.mmd`](D04_verify_flow.mmd)

```mermaid
%% D04 — gfl verify: what is checked and how outcomes are reported.
flowchart TD
  s([gfl verify]) --> c1{Hash chain intact?<br/>prev = previous entry_hash}
  c1 -- no --> F1[CHAIN BROKEN]
  c1 -- yes --> c2{Every signature valid<br/>for its public key?}
  c2 -- no --> F2[BAD SIGNATURE]
  c2 -- yes --> c3{Key role allowed for type?<br/>approval ⇔ owner key}
  c3 -- no --> F3[ROLE VIOLATION]
  c3 -- yes --> c4{Each object: recompute SHA-256}
  c4 -- equal --> OK[ok]
  c4 -- different --> AL[ALTERED<br/>sealed tier 1–2 = critical]
  c4 -- file absent --> MI[MISSING<br/>reported separately · --allow-missing in CI]
  OK --> r([report · --json for machines])
  AL --> r
  MI --> r
```

## D05 — Separation of signing authority and external anchors
Source: [`D05_signing_authority.mmd`](D05_signing_authority.mmd)

```mermaid
%% D05 — Separation of signing authority (DEC-031) and external anchoring.
sequenceDiagram
  autonumber
  participant P as Pipeline (Claude, pipeline key)
  participant L as Ledger (append-only)
  participant O as Owner (owner key on Seagate, offline)
  participant G as Git remote
  participant T as FreeTSA (RFC 3161)
  P->>L: ingest / derivation / qualification (signed, role pipeline)
  P->>O: request-approval (decision text + hashes)
  O->>O: gfl_owner.py sign — recompute hashes, type YES
  O-->>P: signed approval file
  P->>L: attach-approval (verify: role owner, type approval)
  P->>G: anchor-git (chain head → commit)
  P->>T: anchor-tsa (chain head → timestamp token)
  Note over L: verify rejects an owner key signing anything else,<br/>and a pipeline key signing an approval
```

## D06 — Evidence Vault phases
Source: [`D06_vault_phases.mmd`](D06_vault_phases.mmd)

```mermaid
%% D06 — Evidence Vault phases (DEC-025): the seal protects evidence, not conclusions.
flowchart LR
  subgraph SEALED["Sealed — immutable, content-addressed"]
    p1[Phase 1<br/>primary instrument files<br/>+ instrument record]
    p2[Phase 2<br/>source tables exactly as published]
  end
  subgraph OPEN["Outside the seal — append-only"]
    p3[Phase 3<br/>every analysis, incl. GFL's own]
    p4[Phase 4<br/>comparisons · updates · predictions]
  end
  p1 --> p3
  p2 --> p3
  p3 --> p4
  p4 -. error found .-> sup[New supersession entry<br/>old entry stays findable]
  sup -. lineage walk .-> p1
```

## D07 — B6 flame-spread measurement pipeline
Source: [`D07_b6_measurement.mmd`](D07_b6_measurement.mmd)

```mermaid
%% D07 — B6 flame-spread measurement pipeline (tools/flame_front.py, b6_sensitivity.py, b6_radiometric_audit.py).
flowchart TD
  n[NASA NEF stills, 14-bit raw<br/>sha256 in ledger] --> t[EXIF time<br/>DateTimeOriginal + SubSec]
  n --> d[Linear demosaic, gamma 1<br/>rawpy, no auto-bright]
  d --> r[Relative radiance<br/>÷ exposure time]
  r --> b[Width-averaged profile<br/>declared row band 655–1016<br/>code slice 655:1017]
  b --> f[Front definitions<br/>abs. thresholds · per-frame fractions · peak · centroid]
  t --> x[x–t series]
  f --> x
  x --> w[Fit window 13–53 s<br/>+ all windows 8–25 → 40–60 s]
  w --> s[Spread-rate set<br/>2.07–2.42 mm/s]
  s --> u[Uncertainty<br/>scale ±3 % · block bootstrap · autocorrelation]
  r --> q[Radiometric audit<br/>saturation · brightening ×6.3 · ramp width]
  q -. qualifies .-> s
```

## D08 — Zero-trust verification loop
Source: [`D08_zero_trust_loop.mmd`](D08_zero_trust_loop.mmd)

```mermaid
%% D08 — Zero-trust verification loop applied to every result (DEC-030).
flowchart LR
  m[Measurement / claim] --> rt[Red team<br/>objections]
  m --> bl[Blind independent analyses<br/>no access to GFL results]
  bl --> ex[Validator re-execution<br/>isolated env · same data hashes]
  rt --> rg[(Register<br/>DEC · ISS · RES)]
  ex --> cmp{Numbers reproduce?}
  cmp -- yes --> acc[Accepted with qualifiers]
  cmp -- no --> rej[Rejected · reason recorded]
  acc --> rg
  rej --> rg
  rg --> own{Owner decision<br/>owner key signature}
  own --> L[(Ledger)]
```

## D09 — AAL pipeline `gfl_review` (WF-0011)
Source: [`D09_aal_gfl_review.mmd`](D09_aal_gfl_review.mmd)

```mermaid
%% D09 — AAL pipeline gfl_review as run in WF-0011.
stateDiagram-v2
  [*] --> DRAFT : task brief (Founder)
  DRAFT --> REALITY : LAUNCH
  state REALITY {
    direction LR
    kimi26 : kimi26 · verification + analysis
    deepseek : deepseek_v4 · reality_brief
  }
  note right of REALITY : independent phase — analysts never see each other
  REALITY --> HOLD : Founder on behalf of API agent (probation)
  HOLD --> ADVERSARIAL_AUDIT : Founder approval
  ADVERSARIAL_AUDIT --> INTEGRATION_REVIEW : Mistral audit
  INTEGRATION_REVIEW --> LOCAL_VALIDATION : Red team (grok47, gpt55) vs GFL
  LOCAL_VALIDATION --> CONCEPT : Validator re-executes every script
  CONCEPT --> AWAITING_GATE : synthesis (gpt6_astra)
  AWAITING_GATE --> [*] : Founder decision → GFL register
```

## D10 — Delivery plan to the freeze
Source: [`D10_roadmap.mmd`](D10_roadmap.mmd)

```mermaid
%% D10 — Delivery plan to the internal freeze (15 Nov 2026, 19:59).
gantt
  dateFormat  YYYY-MM-DD
  title GFL — NASA Space Apps 2026 delivery
  section Evidence & ledger
  Release A (B6 measurement, ledger)      :done, 2026-11-01, 2026-11-05
  Robustness, red team, blind tests       :done, 2026-11-05, 2026-11-08
  section AAL test WF-0011
  REALITY (blind analyses)                :done, 2026-11-06, 2026-11-08
  Audit · red team · validation           :active, 2026-11-08, 2026-11-10
  section Documentation & interface
  WP5 documentation, AI disclosure table  :2026-11-10, 2026-11-13
  Dashboard + diagrams + icons            :2026-11-10, 2026-11-13
  section Release
  Final verification, package, freeze     :crit, 2026-11-13, 2026-11-15
```

## D11 — Canonical evidence graph node classes
Source: [`D11_evidence_graph.mmd`](D11_evidence_graph.mmd)

```mermaid
%% D11 — Canonical evidence graph node classes (docs/CANONICAL_EVIDENCE_GRAPH_CONTRACT_v0.1.md).
flowchart LR
  source[source] --> investigation[investigation] --> experiment[experiment]
  experiment --> configuration[configuration]
  experiment --> sample[sample]
  experiment --> measurement[measurement<br/>quantity · unit · method · uncertainty]
  source --> assertion[assertion<br/>reported · measured · derived · inferred]
  measurement --> assertion
  assertion --> claim[claim]
  claim --> comparison[comparison]
  comparison --> assessment[assessment<br/>versioned · one inference]
  assertion -. unresolved .-> claim
```
