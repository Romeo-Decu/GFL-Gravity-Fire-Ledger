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

## First run, 2026-11-13

48 calls, all answered. Result as built, before any amendment: 24 investigations; of 276 pairs, 110 share no fire-safety function, 109 are not directly transferable, 56 are not established, 1 is conditionally informative. Five items were dropped by the quote check (PSI-10: one per extractor; PSI-23, PSI-68, PSI-102: one each from Kimi-K2.6). One answer (PSI-20, Kimi-K2.6) was cut off by the 16 000-token budget before the form was complete, so PSI-20 has a single extractor. The owner's build and a rebuild from the same raw answers in the repository give the same map.

## Amendment A1, 2026-11-13: an answer cut off by the token budget

Reason: a cut-off answer is a transport failure, not a reading of the record. Rule: a call whose finish reason is "length" is repeated once with twice the budget (`--redo-truncated`); the cut answer is kept beside it as `*_truncated.json` and is not used. No other call is repeated, whatever it says. Written before the repeat was run.

## Amendment A2, 2026-11-13: retrieval relevance with INDUS

Reason: GFL keeps three questions apart: relevance, comparability, transferability. The map above answers the second and third from extracted conditions; it has no measure of the first. Rule: NASA's INDUS sentence encoder (`nasa-impact/nasa-smd-ibm-st-v2`, public) scores each investigation's record against seven fixed questions, one per fire-safety function (`tools/indus_rank.py`, questions in the file). The score is the highest cosine similarity over passages of about 90 words; the passage is shown. The score is relevance only and enters no gate and no verdict. Questions and code are anchored before the encoder is run. What will be reported whatever it shows: for each function, how the INDUS ranking compares with the investigations the two extractors agreed on.

## Result after A1 and A2, 2026-11-13

A1: the repeated PSI-20 answer was complete; all 24 investigations now have two extractors. Of 276 pairs: 96 share no fire-safety function, 122 are not directly transferable, 57 are not established, 1 is conditionally informative (PSI-98 with PSI-99). The quote check dropped the same five items as in the first run. The owner's build and the repository rebuild are identical.

A2: INDUS (`nasa-impact/nasa-smd-ibm-st-v2`, sentence-transformers 6.2.0, run on the owner's machine) against the investigations both extractors agreed on. For each function with n agreed investigations, how many of them are in INDUS's top n: material flammability 7 of 10, ignition 3 of 5, flame spread 5 of 6, extinction 5 of 10, detection 2 of 6, suppression 2 of 5, soot and smoke 9 of 15. Scores span 0.41 to 0.72, a narrow range for 24 records that all concern combustion. Reading: similarity to a question and stated evidence for a function are different things, which is the separation GFL keeps; the ranking is shown beside the map and decides nothing in it.
