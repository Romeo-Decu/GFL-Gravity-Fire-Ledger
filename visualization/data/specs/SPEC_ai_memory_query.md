# AI query of the experiment memory, with blind mode

**Status:** designed (DEC-042). The memory index the AI would read is built; the AI access is not.

## What we want
A researcher, an engineer or an AI model can ask: "Has this hypothesis been tested? When, by whom, under which conditions, with which method and instrument, and what happened?" The answer must point to records, never be a free narrative.

## Design
- **Interface:** an MCP server and a plain HTTP API over `experiment_memory.json` and the ledger. Tools:
  - `search_records(query, conditions)`;
  - `get_record(id)`;
  - `lineage(entry_hash)`;
  - `verify(entry_hash)`.
- **Comparability-aware search:** conditions are expressed in the GFL comparability vocabulary (material, thickness, flow, oxygen, gravity, observable). The answer says whether a prior test is comparable, and which dimension blocks it.
- **Zero-trust answers:** every statement carries a record ID and a ledger hash. A statement without a citation is labelled [UNKNOWN].
- **Blind mode:** the user first commits their own hypothesis and method, as a signed ledger entry. Only then are prior results shown. This prevents anchoring, the failure seen when analysts copy earlier numbers.

## Validation
- A question set with known answers drawn from the register, including failures (for example: "Was a hand-chosen window used for B6?" must return RES-001 superseded, DEC-040/041).
- Hallucination test: questions with no record must return "no record", never an invented one.

## Blocking conditions
- Models that confabulate under missing inputs (observed in WF-0011, RES-018) must be excluded or wrapped, so that only cited answers pass.
