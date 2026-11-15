# Submission texts, NASA Space Apps 2026

Team CCTI, project Gravity Fire Ledger (GFL), challenge "Flame in Freefall". Every figure below is taken from a sealed file in this repository, as it stood on 14 November 2026. Made with AI: drafted by Claude (Anthropic) for the team, edited and approved by the team.

---

## 1. Summary (form field, 50–200 words recommended)

Gravity Fire Ledger (GFL) is a microgravity combustion analysis platform that turns NASA's public combustion data into evidence a fire-safety engineer can check. NASA's own BASS results show that the standard ground flammability test is not conservative in microgravity, so evidence does not carry over by default. GFL answers three questions that are usually mixed up: does a source address my question, were the conditions comparable, and can a finding be carried to another context? GFL measured flame-spread rates from NASA's raw BASS-II images under rules frozen before the data were opened, sealed every step in a signed ledger your browser re-verifies, and mapped all 24 combustion investigations in NASA's Physical Sciences Informatics repository by fire-safety function, from ignition to suppression. Three AI models from three providers extract what NASA's records state, every value is checked word for word against the record, and fixed rules decide what may transfer. The honest result: at record level, no pair of investigations can be said to transfer; GFL shows, pair by pair, what is missing. Applied to Apollo 1, the archive holds no flame-spread data for solid materials in enriched oxygen. Knowing exactly where the evidence stops makes fire-safety decisions defensible.

(198 words.)

---

## 2. Project details (form field)

**What it does**

GFL is a web platform for anyone who must decide what NASA's microgravity fire experiments do and do not tell them: a spacecraft fire-safety engineer, a researcher planning the next experiment, a reviewer. It keeps three questions apart. Relevance: does an experiment address my question? Comparability: were its conditions the ones I care about, and are they recorded? Transferability: may a finding inform another context, within what stated limits? Unknown is never treated as compatible, a conflict between sources is not treated as a physical difference, and a value reported by a source is never presented as a GFL measurement.

**How it works**

1. *Measurement from NASA's raw data.* From the raw camera stills of the BASS-II investigation (PSI-25), GFL measures the luminous-edge spread rate of a thin PMMA film in microgravity. The rule that picks the frames and the edge was frozen and anchored in the ledger before it touched real data. Result for run B6: 2.20 mm/s (95 % interval 1.91–2.37). Six more runs were measured with the same rule, including two at 17 % oxygen, where the film burns at about half the rate (local exponent about 3.5). Four predictions were sealed before their runs were downloaded: one supported, one not supported, two not testable; all four are shown.
2. *A signed ledger.* Every input file, rule, result and decision is a hash-chained entry signed with Ed25519 and anchored to Git commits and external time stamps. The page re-verifies all entries in the visitor's browser. One command rebuilds the results in an empty copy and compares them with the sealed fingerprints: 30 of 30 identical from NASA's raw files.
3. *A fire-safety evidence map.* For the 24 investigations NASA lists under Combustion Science, three AI models from three providers (grok-4.7, Kimi-K2.6, gpt-5.5) read NASA's record text and fill one form: fuel phase, gravity, flow, atmosphere, and the fire-safety functions served. A value is kept only if its quoted passage is found word for word in NASA's record, and only if all three models give it. NASA's own INDUS language model measures relevance, separately, and flags quotes for a human reading. Fixed rules then decide, for all 276 pairs of investigations, whether a finding may be carried: 97 share no fire-safety function, 98 are not directly transferable because a recorded condition differs, 81 are not established because a condition is not stated, and none is conditionally informative on record text alone. A matrix shows every pair; one click gives the reason.
4. *One level down.* 20 of the 24 investigations also publish a table with one row per run. GFL inventories what those tables record and shows that evidence beside each open condition. It also works one transfer end to end from them: Saffire-II's 5 cm fabric strips spread at 2.1–2.6 mm/s according to NASA; the Saffire-I sample, eight times wider, gives 2.24 mm/s from its length and burn time. Conditionally informative as a comparison of reported values; undetermined as a quantitative transfer, because no uncertainty is reported. GFL then tried to measure Saffire from the images under two rules frozen in advance; both failed, and both failures are reported, not tuned away.
5. *Real incidents.* For Apollo 1, Apollo 13 and the Mir fire, GFL lists the functions involved and what the archive holds for them. Apollo 1 burned in pure oxygen: the archive has no flame-spread data for solid materials in enriched oxygen.

**Benefits and intended impact**

GFL makes NASA's combustion archive usable for decisions that must be defended: it shows what was measured, how sure we are, what carries over and why the rest does not. The method is not tied to fire: the ledger, frozen rules and quote-checked extraction can be applied to any experimental archive. Three directions are specified but not built: enriched-oxygen cabins for exploration vehicles, partial gravity for the Moon and Mars, and confined low-flow fires on Earth.

**What the data cannot settle, and the next question**

NASA's images show the luminous edge of the flame, not the pyrolysis front; the flow speed at the sample surface was not recorded; each condition was flown once. GFL states these limits beside its results. The next research question is how far independent evidence, such as a second observable, a flow model or a matched ground test, can bound what a single flight image cannot. Saffire's backlit cameras, which record the burn front in transmission, are one such second observable.

**How it was built**

Two people, Romeo Decu and Cristina Simion, set the questions, made every decision and approved each step. AI models in declared roles wrote the code and analyses and attacked the results; GFL re-ran their work rather than trusting it. Coordination ran through AAL, the team's own orchestration software.

**Tools**

Python 3.10+ (NumPy, SciPy, rawpy, Pillow, cryptography), JavaScript with Plotly.js, Cytoscape.js and ELK.js, HTML and CSS, Git and GitHub Actions (tests on Python 3.10 to 3.13, ledger verification and browser tests in Chromium and Firefox on every change), Azure AI Foundry for the extraction models, sentence-transformers for INDUS, Playwright for browser tests. It runs on any computer with Python: double-click START_GFL.bat (Windows) or run START_GFL.sh.

**Creativity**

Most tools ask "which data look relevant?". GFL asks what a finding is allowed to say about another experiment, and shows its own failures: a prediction that did not hold, two measurement rules that failed, a pair that stopped being transferable when a third model was added. Every claim can be checked by re-execution in the visitor's own browser.

---

## 3. Use of Super Intelligence (form field; not seen by the judges)

Select: code, text, data analysis, images (and video if the generated intro is used).

Text for the description:

The idea, the questions and every decision are the team's. AI was used as follows, and is marked where it appears in the project.
- Code, tests, documentation and the web page: written by Claude (Anthropic) under the team's direction; marked "Human + AI, checked by re-execution" on the page and in the code metadata (codemeta.json, page meta tags).
- Analyses by AI models in declared roles, through Azure AI Foundry and the team's AAL software: grok-4.7 (xAI), Kimi-K2.6 (Moonshot AI) and gpt-5.5 (OpenAI) extract conditions and functions from NASA's record text, each value checked word for word by deterministic code; gpt-6-astra and gpt-5.5 reviewed the physics; several models ran blind re-analyses whose code GFL re-executed. A DeepSeek model was called once in a red-team test and refused; the refusal is kept as a record. All outputs are labelled where shown, with their errors.
- NASA's INDUS sentence encoder ranks relevance and flags quotes for a human reading.
- Images: the team logo was made with Nano Banana 2 (Google) and refined by the team; the GFL logo and icons are drawn by AI-written code; both carry a visible "Made with AI" mark where shown. Demo video: the intro animation and posters are generated by AI-written code and carry the mark.
- No NASA logo, insignia or mission identifier was generated or modified.

---

## 4. NASA data and resources (form field: link text, link URL)

| Link text | URL |
|---|---|
| PSI Data Repository: BASS-II (PSI-25), raw images, proof sheets, experimental table, fan calibration | https://psi.nasa.gov/ |
| PSI Data Repository: records and experimental tables of the 24 Combustion Science investigations | https://psi.nasa.gov/physci/repo/search?q=combustion |
| PSI Data Repository: Saffire-I and Saffire-II (PSI-98, PSI-99) images, tables, readmes | https://psi.nasa.gov/ |
| INDUS sentence encoder (NASA IMPACT, nasa-smd-ibm-st-v2) | https://huggingface.co/nasa-impact/nasa-smd-ibm-st-v2 |
| NASA Combustion Science | https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/ |
| A Researcher's Guide to International Space Station Combustion Science | https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/ |
| Apollo 1 (lessons learned) | https://sma.nasa.gov/sma-disciplines/accllp/apollo-1 |
| Apollo 13 (lessons learned) | https://sma.nasa.gov/sma-disciplines/accllp/apollo-13 |
| 25 Years Ago: Fire Aboard Space Station Mir | https://www.nasa.gov/history/25-years-ago-fire-aboard-space-station-mir/ |
| NASA ScienceCasts: The Power of Studying Combustion on the ISS | https://www.youtube.com/watch?v=W1oXykoz9zg |

---

## 5. Space Agency Partner and other data, code, text and images (form field)

| Link text | URL |
|---|---|
| Plotly.js (MIT licence) | https://github.com/plotly/plotly.js |
| Cytoscape.js (MIT) | https://github.com/cytoscape/cytoscape.js |
| ELK.js (EPL-2.0) | https://github.com/kieler/elkjs |
| marked (MIT) | https://github.com/markedjs/marked |
| NumPy | https://numpy.org/ |
| SciPy | https://scipy.org/ |
| rawpy (LibRaw) | https://github.com/letmaik/rawpy |
| Pillow | https://python-pillow.org/ |
| cryptography (Ed25519 signatures) | https://cryptography.io/ |
| sentence-transformers | https://www.sbert.net/ |
| Playwright (browser tests) | https://playwright.dev/ |
| IBM Plex Sans font (SIL Open Font Licence) | https://fonts.google.com/specimen/IBM+Plex+Sans |
| Azure AI Foundry (grok-4.7, Kimi-K2.6, gpt-5.5, gpt-6-astra) | https://azure.microsoft.com/en-us/products/ai-foundry |
| Claude (Anthropic), code and documents | https://www.anthropic.com/claude |
| Nano Banana 2 (Google), team logo | https://gemini.google/overview/image-generation/ |
| FreeTSA, RFC 3161 time stamps for the ledger | https://freetsa.org/ |
| de Ris (1969), opposed-flow flame spread theory; Bhattacharjee et al. (2016); Rojas-Alva (2022), PMMA properties; Carmignani et al., edge propagation: cited in docs/METHODS_AND_VALIDATION_v1.md, not redistributed | see docs/METHODS_AND_VALIDATION_v1.md |

| Sound effect "Match Sizzle 03" by freesound_community, Pixabay Content License (demo video) | https://pixabay.com/sound-effects/search/match%20sizzle/ |
| Sound effect "Fire sound effect, designed fire short swoosh" by Gregor Quendel, Pixabay Content License (demo video) | https://pixabay.com/sound-effects/search/fire%20swoosh/ |

Use only the two sounds that end up in the video; replace each search link with the sound's own Pixabay page.

---

## 6. First screen: two variants (for Romeo to choose)

**A. The question first**

> Can a fire result from one microgravity experiment be trusted in another? GFL measures from NASA's raw images, seals every step so you can check it, and shows, for 24 NASA combustion investigations, what carries over and what does not, with the reason.

**B. The finding first**

> NASA has flown 24 combustion investigations. GFL read all of them: what each says about fire safety, under which conditions, and whether one result may inform another. On record text alone, none may; GFL shows exactly what is missing. Every number on this page is re-checked by your browser.

Recommendation: B. It states a result a judge remembers, and it is true as of the sealed map.

---

## 7. History, seventh turn (for docs/HOW_THE_QUESTION_CHANGED_v1.md)

| # | Date | The question we thought we had | What the answer showed | What changed in GFL | Evidence |
|---|---|---|---|---|---|
| 7 | 13–14 Nov | Does one well-measured experiment answer a fire-safety question? | An independent evaluation said the work was rigorous but narrow. Reading all 24 NASA combustion investigations with three models showed that, on record text alone, no pair can be said to transfer; one level down, NASA's run tables hold part of what is missing; two rules for measuring Saffire from its images failed and were reported | From one run to the whole archive: an evidence map by fire-safety function, a transfer matrix over every pair, run-table evidence beside open conditions, and three real incidents read against the archive | RES-053 to RES-062, DEC-071 to DEC-073 |
