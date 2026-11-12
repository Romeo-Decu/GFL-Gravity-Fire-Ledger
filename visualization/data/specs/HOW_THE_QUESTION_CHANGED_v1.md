# How the question changed

**Status:** v1, 2026-11-12. **Author:** Claude (PM) for team CCTI, from the owner's account of the project and the register. **Made with AI.**

GFL did not start as what it is now. It started as a dashboard, and each answer exposed a question the architecture of the day could not handle. This page lists those turns, each with its date and the record that holds the evidence, so that the route can be checked and not only told. Records are in `docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md`; sealed files are in the ledger.

## Short GFL history

We set out to build a dashboard over NASA's microgravity flame data. The first audit showed that the sources did not agree with each other, so the problem was not display but exactness. We measured from NASA's raw images, sealed every step in a signed ledger, had other analysts repeat the work blind, and wrote predictions down before opening the data. One prediction held and one did not; both are on the page. GFL does not claim a better number: it shows what each number is made of, and where it stops being reliable.

## Where it started

The team chose this challenge because thermodynamics and informatics are what CCTI works on. Combustion science itself was not the team's field: it was covered by reading the literature, by the project's own library of papers, and by AI. No external human expert in combustion has reviewed the physics, and GFL says so wherever a result is shown.

## The instrument: AAL

The blind analyses, the red teams and the audits in turn 4 were run through AAL (AI Automation Lab), an application built in house by the same team. AAL is local-first software for coordinating, observing and governing a workflow made of people, AI models, software development tools and real validation environments. In GFL it gave us several different models, each with its own role, coordinated over MCP and API. They worked blind, attacked the result, and GFL re-ran their code. We describe them as models with roles, not as autonomous agents: a person approved each phase, and no model's report was accepted without re-execution. That is AI used inside the research process, and it is documented, failures included (`docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md`, RES-011 to RES-020, ISS-041).

AAL's wider design goal, a multi-model, multi-role platform that improves from its own runs across different projects, is the team's and is not used or claimed in GFL.

## The six turns

| # | Date | The question we thought we had | What the answer showed | What changed in GFL | Evidence |
|---|---|---|---|---|---|
| 1 | 1–3 Nov | How do we show NASA's combustion data in one place? | The sources disagree: the airflow of run B3 is 2 cm/s in one and 3 cm/s in another, oxygen columns differ between table versions, and a published 2.2 mm/s could not be tied to one run | From display to exactness: three separate questions (relevance, comparability, transferability) and a register of deviations that are never corrected silently | `research/SOURCE_CORRECTION_B3_OXYGEN_COLUMNS_2026-11-03.md`, `research/CARMIGNANI_2019_BASS_B3_CROSS_SOURCE_AUDIT_2026-11-03.md`, ISS-013 |
| 2 | 4–5 Nov | Which published value is right? | That cannot be settled from publications. B3 was dropped as the measured case because its link to the published value was never established | GFL measures from NASA's raw stills itself: run B6, 77 images | RES-001, `docs/GFL_MAP_2026-11-11.md` §1 |
| 3 | 5 Nov | How do we show we did not choose the result we liked? | A measurement with free choices can be steered, knowingly or not | A signed, hash-chained ledger with two keys and external time stamps; raw files re-downloaded with identical fingerprints | RES-003, RES-004, DEC-031 |
| 4 | 5–11 Nov | Would other analysts get the same number? | Blind AI analysts got a third of our value, entirely because of which frames they used; one reported a table its own code did not produce; an auditor certified things it had not checked. Our own first number (2.27 mm/s) rested on a hand-picked window and was replaced (1.99 mm/s) under a rule fixed before fitting. On synthetic data with a known answer, intervals covered the truth in 15 of 24 cases, and in one case every analyst, GFL included, was wrong in the same direction | Rules frozen and anchored before use; AI claims ranked by re-execution, not by confidence; failures kept as records; rates labelled as luminous-edge rates | RES-009, RES-014, RES-019, RES-021, RES-022, RES-034, ISS-050, DEC-056 |
| 5 | 11 Nov | Does a result from one run say anything about another? | Four predictions were sealed before the runs were downloaded: one supported (B9), one not supported (B13), two not testable under the registered rule | Predictions became a function any user can run; a result that cannot be tested never counts as supported | RES-035, RES-036, RES-037, DEC-061 |
| 6 | 11–12 Nov | Is the platform doing physics, or only bookkeeping? | A file-by-file audit of our own dossier: the transfer engine judged declared states and computed nothing; 3 of 14 promised modules were delivered | Analysis modules built as platform code and run on the four measured runs: flow calibration, thin-fuel theory, regime, three-layer uncertainty, anomaly detection, computed transfer conditions, standard provenance export | `docs/GFL_MAP_2026-11-11.md` §7, DEC-060, RES-040 to RES-047 |

## What the route shows

Each turn was forced by a result, not chosen for effect, and several went against us: our first number was replaced, one of our predictions failed, our own audit found most promised modules missing. They are in the record because the method requires it. Everything measured so far stays open until it is compared with the official challenge data (DEC-058).

## What this page does not claim

That the route was planned; it was not. That the present architecture is final. That any external human expert in combustion has reviewed the physics (none has, DEC-045).
