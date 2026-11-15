# Comparability-aware search across external literature

**Status:** designed. Not built.

## What we want
Extend the experiment memory beyond GFL's own records: published experiments are indexed with their conditions, so that a question returns comparable prior work and states why other work is not comparable.

## Design
- **Extraction:** conditions are extracted from papers into the GFL comparability vocabulary. Each value is labelled source-reported, carries its locator (page, table, figure) and is never treated as a GFL measurement.
- **Conflicts:** between sources, conflicts are kept as conflicts. They are not resolved by majority and are not read as physical incompatibility.
- **Ranking:** comparability first, through the gates, and textual relevance second. Relevance is not comparability.

## Validation
- A curated set of papers with hand-checked conditions.
- Extraction precision and recall are reported.
- No extracted number enters a result without a locator.

## Blocking conditions
- Access rights to full texts.
- Extraction errors by AI tools must be caught by locator checks (zero trust).
