# GFL evidence map: protocol v1

Registered and anchored before any extraction run (DEC-071). Changes after the first run are amendments with a date and a reason.

## Question

For each fire-safety function (material flammability, ignition, flame spread, extinction, detection, suppression, soot and smoke), which NASA combustion investigations in the PSI repository give evidence, under which conditions, and between which of them may a finding be carried?

## Material

The 24 investigations that NASA's PSI repository lists under Research Area "Combustion Science" (`data/manifests/PSI_CATALOG_v1.json`, retrieved from `psi.nasa.gov`, each record with its SHA-256). For each, the extractor sees NASA's own record text only: objective, hypothesis, approach, research impacts, experiment hardware, sub-area, flight platform, descriptors (`gfl_map.record_text`). It does not see the data files or the publications.

## Extraction

Two models from two providers (grok-4.7, Kimi-K2.6), one call per investigation, no history, the same prompt (`tools/evidence_map_run.py`, `--print-prompt` shows it). Each fills one form: four condition slots with closed vocabularies (fuel phase, gravity, flow, atmosphere), the fire-safety functions served, and up to five further statements. Every value other than "unknown" must carry a passage copied from the record word for word. Raw answers are kept with the hash of the record and of the prompt.

## Deterministic check (`src/gfl_map`, no model involved)

1. A value or statement is kept only if its quote is in the record word for word (case and white space aside, at least 12 characters). Otherwise the value becomes unknown, the statement is dropped, and the drop is counted and published.
2. A slot value stands only when both extractors gave the same value, each with a valid quote. Different values are shown as disputed and count as unknown. Nothing is averaged or adjudicated by a third model.
3. A function is "agreed" when both extractors named it with valid quotes, otherwise "one extractor".

## Transfer between investigations

For every pair, on the agreed values only:

- no fire-safety function in common: "no shared fire-safety function";
- a condition slot differs: "not directly transferable", with the slot named;
- a slot is unknown or disputed on either side: "not established" (unknown is not compatible);
- all four slots equal: "conditionally informative", never more, because record text carries no quantitative conditions.

## What the map is and is not

It is a map of what NASA's records state, with the passage for each item. It is not NASA's classification, not a review of the publications, and not a statement about results the records do not mention. The quote check proves that a passage exists in the record; it does not prove that the model read it correctly, which is why the passage is shown next to every item. Agreement between two models is not truth; it lowers the rate of single-model errors.

## Fixed before the run

Vocabularies, prompt, validator, merge rule, transfer rule and tests (`tests/test_gfl_map.py`) are in the commit this protocol is anchored with. Counts are reported whatever they are, including investigations where the extractors disagree or the record states too little.
