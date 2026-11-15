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

## Amendment A3, 2026-11-14: a third extractor

Reason: two extractors agreeing can share an error; a third from another provider shows how stable the map is. Rule: gpt-5.5 answers the same prompt for the same 24 records, under the same quote check and A1. The three-extractor map (`EVIDENCE_MAP_v2.json`) keeps the merge rule unchanged: a slot value or a function is "agreed" only when all three extractors gave it, each with a valid quote. The two-extractor map of 13 November stays sealed as v1 and is not edited. Reported whatever it shows: how many agreed values and functions of v1 survive in v2, and how the pair verdicts change. Written and anchored before the third extractor was run.

## Amendment A4, 2026-11-14: INDUS on the quoted passages, and a human reading

Reason: the quote check proves a passage exists, not that it supports the function it is cited for. Rule (`tools/indus_quote_check.py`): for each function an extractor named, the cosine similarity between that function's fixed question (A2) and the quoted passage, by the same INDUS encoder. Baseline for a question: the median similarity between it and every passage of the 24 records. An item is flagged when its quote scores no higher than that median. A flag is a request for a human reading, not a verdict, and changes nothing in the map.

Human reading: two team members, separately, read against NASA's record (a) every flagged item and (b) every function and condition of three investigations drawn at random with the fixed seed "GFL evidence map, human check, 2026-11-14", which gives PSI-26, PSI-68 and PSI-107. For each item: correct, wrong, or cannot tell. The counts are recorded whatever they are. The random sample is what estimates how much passes unflagged; the flagged set alone cannot.

What this chain does not catch: an error in NASA's record itself; a passage three models misread in the same way and that is close to the question; anything outside the sampled investigations that no check flagged.

## Result after A3 and A4, 2026-11-14

A3: gpt-5.5 answered all 24 records; none was cut off, and the quote check dropped none of its items. With three extractors, every fire-safety function agreed by two is agreed by three: the seven function lists are unchanged (one investigation leaves "combustion fundamentals"). Of 65 agreed condition values, 58 remain; the seven that do not: fuel phase of PSI-99, PSI-102 and PSI-106, gravity of PSI-107, flow of PSI-159, atmosphere of PSI-10 and PSI-25. Pair verdicts: 97 no shared function, 98 not directly transferable, 81 not established, 0 conditionally informative. The single conditionally informative pair of the two-extractor map (PSI-98 with PSI-99) is gone, because the third extractor reads the fuel phase of PSI-99 as not stated in the record. Reading: which functions an investigation serves is stable across models; the condition labels are less so, and at record level no pair of investigations can be said to transfer.

A4: of 183 quoted passages, 64 score no higher than the baseline of their question and are flagged, covering 29 investigation-function items, 24 of them agreed by all three extractors. The flag rate is high: a short quote is compared with a baseline made of 90-word passages, so the rule is coarse. It was fixed before the run and is reported as it is; the human reading decides what the flags are worth.

## Amendment A5, 2026-11-14: run-level condition inventory

Reason: with three extractors, no pair of investigations can be said to transfer on record text alone, mostly because conditions are not stated there. NASA's PSI repository also holds, for most investigations, an "Experimental table" with one row per run. Rule (`tools/psi_run_tables.py`, no model involved): download every experimental table of the 24 investigations; classify each column header by the keyword rules fixed in the tool (fuel or material, oxygen, pressure, flow, gravity, geometry, diluent or suppressant, ignition, outcome); a condition counts as recorded per run when a matching column has at least one filled cell. Reported whatever it shows: for each investigation, which conditions the tables record, and which map slots left unknown by the record text could be settled from them. The rules were written after seeing only the three Saffire tables and before the others were downloaded. A column existing is not a value checked: this inventory says where the evidence is, not what it says.

## Result of A5, 2026-11-14

20 of the 24 investigations publish an experimental table (22 files, about 2,000 rows; some rows are notes); PSI-60, PSI-62, PSI-115 and PSI-117 do not. Investigations with a filled column, by class: fuel or material 19, oxygen 8, pressure 5, flow 9, gravity 0, geometry 6, diluent or suppressant 4, ignition 8, outcome 12. Of the 38 conditions left unsettled by the record text in the three-extractor map, 13 have a column at run level. The keyword rules misfire in places ("Atmosphere" matches "atm" and counts as pressure in PSI-23; "O2 flow rate" counts as flow in PSI-159; "(Note 1)" counts as outcome) and were not changed after the tables were read. One transfer was then worked end to end from the tables, Saffire-II to Saffire-I (`tools/build_saffire_transfer.py`, RES-059).

## Amendment A6, 2026-11-14: run-table evidence beside open conditions

Reason: where the extractors disagree or none finds a condition in the record text, NASA's run table may hold it. Rule (`tools/run_table_evidence.py`, no model): for each condition not agreed by all three extractors, if the investigation's experimental table has a matching column, the page shows what it holds; for oxygen (concentration columns, final values excluded) and flow (speed columns) a fixed numeric reading is added; material names are shown and not classified. These rules were written after the disputes had been seen, which is why they change no verdict of the map: they show evidence beside it. Result: 11 conditions in 10 investigations gain run-table evidence. Where a reading is possible it sides with gpt-5.5 on the oxygen of PSI-10, PSI-25 and PSI-159 ("varied"; BASS-II initial oxygen 13.6 to 22.2 %) and with the two other extractors where the fuel is named as a gas (PSI-106). The SAME table (PSI-102) lists a liquid, a film and a wick among its samples, so "solid" was not right for every sample either.

## Result of the human reading (A4), 2026-11-14

Two team members read the 46 items separately against NASA's record (`data/derived/evidence_map/human_check/`, `tools/human_check_summary.py`). Romeo: 45 correct, 1 cannot tell, 0 wrong. Cristina: 43 correct, 3 cannot tell, 0 wrong. Same verdict on 42 of 46. All 29 INDUS-flagged items were judged correct by one reader and 28 by the other, so the flags were false alarms, as the coarse rule suggested. On the 17 items of the random sample (PSI-26, PSI-68, PSI-107) no error was found, which bounds the error rate of unflagged items below about 18 % at 95 % confidence (rule of three), not at zero. The readers are team members, and each item showed the map's claim beside the passage, which favours agreement.
