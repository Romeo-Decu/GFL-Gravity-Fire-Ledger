# Evidence-backed synthesis

**Status:** designed. Not built. Deterministic text today exists only as the engine's primary reason and blocking gates.

## What we want
A plain-language summary of what the evidence supports for a question, in which every sentence maps to evidence references, and abstention text appears when evidence is insufficient. An LLM may help phrase the summary, but it is never the source of truth.

## Design
- **Template sentences** are generated from engine output and memory records: conclusion, blocking gates, conflicts, prohibited extrapolations.
- **Optional LLM rewording:** each reworded sentence is checked against its reference set, and any sentence whose references cannot be resolved is removed.
- **Sealing:** the output is sealed in the ledger with its inputs.

## Validation
- Every sentence resolves to at least one record.
- Abstention appears for every undetermined profile.
- No number appears that is absent from the records.

## Blocking conditions
Confabulation by language models (RES-018): the reference check must be strict and automatic.
