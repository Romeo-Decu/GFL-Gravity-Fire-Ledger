# Independent evaluation of GFL: protocol and questionnaire v1

**Registered:** 2026-11-12, before any evaluator is run. **Decision:** owner's plan of 11 Nov (step 2b) and message of 12 Nov 14:57. **Author:** Claude (PM). **Made with AI.**

## Purpose

Three AI models from three different providers evaluate GFL as it stands after P0, P1 and P2: strengths, weaknesses, solutions, what is urgent, what should stay as documentation, what is missing, and what would move it from a good student project to academic and R&D level. The PM (Claude) built GFL and therefore does not evaluate it; the PM only checks whether each evaluator's statements are supported by the packet.

## Evaluators and roles

| Role | What the role looks for | Model (proposed by the owner) |
|---|---|---|
| Juror | A hostile but fair NASA Space Apps judge: is the claim true, new, useful, and shown clearly in a few minutes | grok-4.7, the strongest critic in WF-0011 (RES-020) |
| Physicist | A combustion scientist: is the physics right, are the numbers used correctly, what would a reviewer reject | gpt-6-astra |
| User | A research engineer who is not a programmer and must use GFL tomorrow: where does one get stuck | Kimi-K2.6, honest about what it cannot do in WF-0011 (RES-020) |

Each evaluator works alone, in one call, with no history, and sees neither the other evaluators nor the PM's opinion. None of the three wrote any part of GFL.

## What they receive

One text packet built by `tools/build_evaluation_packet.py` from files in the repository at a named commit: README, methods, GFL map, project history, user guide, AI disclosure, window rule, comparison protocol, the list of functions with status and evidence checks, the key numbers of the analysis, one full run report, and the register rows of results, open issues and recent decisions. They do not receive the source code, the raw NASA files or the web page; the packet says so, and "cannot verify" is an accepted answer.

## Rules given to the evaluators

1. Every statement about GFL, favourable or not, carries a locator: the packet file and a verbatim quote of at most 25 words from it. A statement with no locator is not counted.
2. Numbers are quoted from the packet, never recalled or estimated.
3. If something cannot be checked from the packet, say "cannot verify" and say what would be needed. Do not guess.
4. Do not invent files, sections, results or references. Do not praise in general terms.
5. Every weakness comes with a concrete solution and an effort estimate in hours.
6. Answer in English, as one JSON object in the format below.

## Questionnaire

**A. Reading checks** (answers are in the packet)
- A1. Under rule R-W4, what is the B6 spread rate and its reported interval, in mm/s?
- A2. The methods document is said to contain a section describing the kinetic model GFL uses to predict blow-off. Does that section exist? If it does, give its parameters; if not, say what the document states instead.
- A3. Which of the four predictions registered on 11 Nov was not supported, and what was its measured ratio?

**B. Strengths** (at most 5): what is solid, and why it matters to your role.

**C. Weaknesses** (at most 12, most serious first): severity (blocker, major, minor), what is wrong, the solution, effort in hours, and what evidence would change your mind.

**D. Missing**: essential functions or evidence that GFL lacks for its stated purpose (at most 5).

**E. Not worth it**: parts that do not deserve more resources before the deadline of 15 Nov, and whether to keep them as documentation or remove them (at most 5).

**F. Triage**: for each function marked partial or designed in the function list, one of: finish now, keep as documentation, remove. Give the function id.

**G. Open decisions**: your recommendation and reason on each.
- G1. Headline number for B6: 1.99 mm/s (rule R-W2, front at 0.1 of peak) or 2.20 mm/s (rule R-W4, front at 0.5 of peak)?
- G2. Run B16 (17 % O₂) is not measurable under the frozen rule. Write a new declared rule for it now (the result would be post hoc), or leave it specified?
- G3. Prediction P-B13 was not supported and the thin-to-thick explanation is not supported either. Report it as an open finding, or is there an explanation the data in the packet support?
- G4. The B6 page headline, the reports and the methods document use two rules. Is that acceptable if stated, or must there be one?

**H. Level**: the three changes that would do most to move GFL from a strong student project to academic and R&D level. Say which are possible in three days and which are not.

**I. Role questions**
- Juror: score 1 to 5, with a reason and a locator, on impact, creativity, validity, relevance and presentation; then the one sentence you would say against this project in the jury room, and the one in its favour.
- Physicist: (1) is the thin-fuel formula applied correctly, including the meaning of the thickness; (2) are the Damköhler and radiation numbers used within what order-of-magnitude groups can support; (3) what do the 17 % O₂ results allow one to say, and not say; (4) is the thickness exponent of −1.19 with its interval read correctly; (5) is the three-layer uncertainty a sound way to report, and what is missing from it.
- User: follow the three operations of the user guide (import a result, export a run, get a report) and say, for each, where a scientist who is not a programmer stops and why; then say what you would need on the first screen.

**J. Cannot verify**: everything you were asked that the packet does not let you check.

**K. Verdict**: one paragraph.

**L. Fit to the challenge** (amendment A1): against the challenge statement in the packet (file `CHALLENGE`), which of its requests GFL answers, which it answers in part, and which it does not answer (at most 8 items). For each, quote the challenge statement in the locator.

## Answer format

```json
{"role": "juror|physicist|user",
 "A": {"A1": {"rate_mm_s": 0.0, "interval_mm_s": [0.0, 0.0], "locator": {"file": "", "quote": ""}},
       "A2": {"section_exists": false, "what_the_document_states": "", "locator": {"file": "", "quote": ""}},
       "A3": {"prediction": "", "ratio": 0.0, "locator": {"file": "", "quote": ""}}},
 "B": [{"statement": "", "why_it_matters": "", "locator": {"file": "", "quote": ""}}],
 "C": [{"severity": "blocker|major|minor", "statement": "", "solution": "", "effort_hours": 0, "would_change_my_mind": "", "locator": {"file": "", "quote": ""}}],
 "D": [{"missing": "", "why_essential": "", "locator": {"file": "", "quote": ""}}],
 "E": [{"part": "", "keep_as_documentation_or_remove": "", "reason": "", "locator": {"file": "", "quote": ""}}],
 "F": [{"function_id": "", "decision": "finish now|keep as documentation|remove", "reason": ""}],
 "G": {"G1": {"recommendation": "", "reason": ""}, "G2": {"recommendation": "", "reason": ""}, "G3": {"recommendation": "", "reason": ""}, "G4": {"recommendation": "", "reason": ""}},
 "H": [{"change": "", "possible_in_three_days": true, "reason": ""}],
 "I": {},
 "J": [""],
 "L": [{"request": "", "answered": "yes|in part|no", "how_or_why_not": "", "locator": {"file": "CHALLENGE", "quote": ""}}],
 "K": ""}
```

## How the answers are checked (fixed before the run)

`tools/score_evaluation.py`, deterministic:

- **Locators.** For every item in B, C, D, E and L the named file must be in the packet and the quote must occur in that file, compared without case and with whitespace collapsed. Result per item: verified, quote not found, file not in packet, or no locator. Items that are not verified are listed and are not counted.
- **Reading checks.** A1 is correct if the rate is 2.20 and the interval 1.91 to 2.37 after rounding to two decimals. A2 is correct if `section_exists` is false. A3 is correct if the prediction names B13 and the ratio is 0.19 after rounding. An evaluator that fails A2 by describing a kinetic model is marked as having invented content, and its other answers are read with that in mind.
- **What the PM does afterwards.** Each verified weakness is classed by the PM against the repository: confirmed, partly confirmed, not confirmed, already known (with the register record). The classing is published with the evaluators' own words beside it. Agreement between evaluators is reported, and is not treated as proof (ISS-050).
- **Nothing is discarded.** Raw responses are stored with hashes and sealed, including failed calls and rejected items.

## Amendment A1 (2026-11-12, before any evaluator was run)

Raised by the owner: the evaluators need the context of the contest. The packet now starts with the challenge statement, as copied by the owner from the NASA Space Apps 2026 challenge page on 8 Nov 2026 (the PM cannot reach that page from its workspace; the copy's SHA-256 is printed in the packet header). The copy is given to the evaluators and is not published in the repository. Part L is added to the questionnaire and to the locator check. The juror's five criteria are those used by Space Apps in earlier years; the 2026 judging guide was not available to the PM when this was written. Nothing else changes.

## Limits

Three models reading documents are not a human expert in combustion (DEC-045 stays as it is). They see the packet, not the code or the page. The PM who checks the locators is the author of GFL; the locator check is deterministic for that reason, and the classing step is published so that it can be contested.

## How to run (owner's machine; the key stays in the environment)

```
python tools/build_evaluation_packet.py --challenge evaluation/CHALLENGE.md --out evaluation/PACKET_v1.md
python tools/run_evaluation.py --packet evaluation/PACKET_v1.md --out evaluation/raw --assign juror=grok-4.7 physicist=gpt-6-astra user=Kimi-K2.6
python tools/score_evaluation.py --packet evaluation/PACKET_v1.md --raw evaluation/raw --out evaluation/SCORES_v1.json
```
