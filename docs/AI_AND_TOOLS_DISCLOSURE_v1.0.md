# Use of Artificial Intelligence and Tools — Gravity Fire Ledger (GFL)

**Version:** 1.0 draft, 2026-11-09. **Decisions:** DEC-034, DEC-036, DEC-037 (register).
**Status:** owner review. WF-0011 ended on 2026-11-09, stopped by the owner (RES-018). This text feeds the submission field *Use of Artificial Intelligence*.

## 1. Principle
GFL is built on zero trust (DEC-030), and the rule applies to its own tools as well. Every AI system that contributed or was evaluated is listed below with what it actually did and how its output was treated.

Models whose output was rejected are listed as **evaluated and rejected, with the reason**. They are neither omitted nor credited as contributors. No AI-reported number enters GFL until GFL has re-executed it from the original data (ISS-035).

## 2. People
| Person | Role |
|---|---|
| Romeo Decu (Team Owner) | Idea, concept and scientific direction (Phase 1, up to the PM appointment). Owner decisions and approvals, signed with a separate owner key (DEC-031). |
| Cristina Simion | Project coordination and usability testing. |

## 3. AI systems
| System | Role | What it produced | Outcome |
|---|---|---|---|
| **ChatGPT** (OpenAI) | Phase 1 drafting assistant; red team in Phase 2 | Phase 1: assisted drafting of the concept documents (idea and concept are the owner's). Phase 2: red-team reviews RT#1 (RES-005) and RT#2 (RES-008) | **Used.** Each objection was checked against the repository and data; the accepted ones are recorded in the register. |
| **Claude** (Anthropic) | Project manager and engineer from the PM appointment | Implementation (ledger, measurement tools, tests), verification, re-execution of external analyses, documentation, diagrams, icon set (as code) | **Used.** Work since the PM appointment carries `Co-Authored-By` trailers in Git; about 56 of the first 225 commits do not (ISS-036), and for those the register, the session syntheses and the ledger record who did what. Its own errors are recorded as well (for example ISS-031 and ISS-034). |
| **Manus** | Scientific check | Check of the working hypothesis and of the first GFL architecture (owner-reported, RES-013) | **Used** as an early review. No numeric result taken. |
| **Gemini** (Google) | Blind independent analyst (personal account) | B6 blind analysis, attempt 1: a results table that its own code did not produce (RES-009). Attempt 2: real output, identical to GFL's re-execution, but measuring the trailing edge (RES-010) | **Attempt 1 rejected** (numbers not reproducible). **Attempt 2: comparison only.** |
| **Kimi K2.6** (via AAL) | Blind Reality_Analyst, WF-0011 | Verification plus a numpy/pandas script; every number correctly labelled as an uncomputed prediction | **Comparison only.** Executed by GFL: 0.43 mm/s, unstable across thresholds and windows (RES-012). First call stopped at its token limit (RES-011). |
| **DeepSeek-V4-Pro** (via AAL) | Blind Reality_Analyst, WF-0011 | Reality brief plus a script | **Rejected as evidence.** It used scipy, which the brief forbids; it labelled untested claims "measured"; its own code contradicts its stated direction (RES-012). |
| **Mistral Large 3** (via AAL) | Independent adversarial auditor, WF-0011 | Audit of both blind analyses (two rounds) | **Rejected as audit.** Round 1 marked false statements as "confirmed" and missed every real defect found by re-execution (RES-014, RES-016). Round 2, after the red team returned it, received a packet without the analyses (an AAL defect) and fabricated line references and claims about code it had not seen (RES-018). Its value is negative evidence: an AI auditor needs re-execution behind it. |
| **grok-4.7** (via AAL) | Red team, WF-0011 | Verification of the audit (FAIL) and 12 objections against the blind analyses and against GFL's own result | **Used as critique.** Every point was checked against data or code: the window hypothesis was then confirmed by re-execution (RES-019); one objection traced back to the PM's own wording (RES-017). No number taken from it. |
| **GPT-5.5** (via AAL) | Red team, WF-0011 | Verification of the second audit (FAIL, fabrication) and objections | **Used as critique.** Same checks. Its fabrication finding was partly primed by a Founder comment that reached its packet, which we disclose (RES-018, ISS-041). |
| **GPT-6 Astra** (via AAL) | Concept synthesis, WF-0011 | Not run: WF-0011 was stopped before that phase | **Not used.** |
| **GPT-6 Astra** (Azure Foundry API, direct) | Second-model check of the AI-finding summaries, 2026-11-10 | Read every summary sentence against the records it cites: 27 supported, 4 partly supported (`data/derived/AI_FINDINGS_SECOND_CHECK_v1.json`) | **Used as a check.** The 4 partly supported sentences were reworded; the page shows its verdict per finding. Called once through the API by `tools/ai_second_check.py` on the owner's machine; not connected over MCP and not live on the page. |
| **INDUS-Retriever-small** (NASA–IBM, `nasa-impact/nasa-ibm-st.38m`, Apache-2.0) | Relevance search over the project library (question 1), 2026-11-10 | Ranked 2214 passages from 24 PDFs for six open questions (RES-030) | **Used for relevance only.** A retrieval model, not a generative one: it points to passages to read; it does not judge comparability or transfer. Run locally on the owner's machine. |

## 4. AAL — the orchestration platform
AAL is a multi-agent orchestration platform developed by the Team Owner at CCTI (private software). GFL used it to run blind, independent AI analyses under an append-only audit log. In WF-0011, AAL provided:
- **Controlled context packets.** Each agent received only the task brief and the two blind data descriptions; the packets are hash-recorded. The blind analysts never saw GFL's results or each other's work (an "independent phase").
- **Roles and phases.** The phases were reality analysis, adversarial audit, red team, local validation and concept synthesis, each with Founder gates.
- **Enforced answer format.** A strict JSON schema, validated by AAL; an answer in the wrong format is refused, but kept in the log.
- **Measured cost, tokens and time** for every call, with the reason when a call stopped (for example a token limit or a timeout).

AAL's first real task, this one, exposed six defects in AAL itself. Each was fixed with a regression test before any result was used (ISS-039; AAL PRs #120–#126). Its later phases exposed five more (ISS-041), among them a return packet that carried no evidence. The owner stopped the workflow there and treated the stop as a result. GFL then settled the open question with deterministic re-execution, without any AI model (RES-019). Reports were obtained by exporting the workflow from AAL. Every artefact was verified byte-for-byte against AAL's content hash before GFL executed its code (`data/external/2026-11-08_aal_WF-0011_reality/`).

## 5. Software, libraries and services (non-AI)
| Item | Use |
|---|---|
| Python 3, NumPy, SciPy (GFL's own tools only), Matplotlib | Measurement, statistics, figures |
| rawpy (LibRaw), ExifRead | NEF raw decoding (linear, 14-bit), EXIF timing |
| cryptography (Ed25519) | Ledger signatures |
| Git, GitHub, GitHub Actions | Version control, CI (tests and ledger verification) |
| FreeTSA (RFC 3161) | External timestamps of the ledger head |
| ELK.js, Cytoscape.js, Plotly.js, Mermaid | Visualisation and diagrams (ADR-001) |
| Microsoft Azure AI Foundry | Hosting of the API models used through AAL and of GPT-6 Astra for the second-model check; Azure also hosts AAL's Linux CI runner (RES-028) |
| sentence-transformers, pypdf, PyTorch | Running INDUS and reading the library PDFs (optional, owner machine) |
| GIMP 3.2.6, Inkscape | Photo and vector editing (owner) |

## 6. Images, logo and icons
The GFL mark and the 59-icon set are geometry written as code (`make_logo.py`, `make_icons.py`) by an AI system (Claude), on the owner's direction. Following the Submission Guide, they are labelled "generated by AI-written code". They contain no NASA logo, flag or mission identifier. An earlier logo draft derived from commercial references was withdrawn (ISS-031).

## 7. Where the AI's role ends, and where it does not
- **No AI model's number is reported as a GFL result.** GFL results are produced by GFL code from NASA bytes and sealed in the ledger. External AI analysts (Gemini, Kimi, DeepSeek) were used for comparison or critique only.
- **Claude did more than engineering, and this is stated plainly.** Claude (the project manager, an AI) wrote the measurement code, the B6 window rule, the choice of reference definition and the physics interpretation in AR-001. It also holds the pipeline signing key. These are AI-authored scientific judgements; they are open to review through the register, the analysis record and the code.
- **Owner approval and owner signature are different things, and both are reported.**
  - The owner approves decisions in the project conversation, and the register records them.
  - Only one decision is so far signed with the owner's separate key in the ledger: DEC-029, which concerns the superseded first result.
  - DEC-041, which adopted the current B6 result, is approved but not yet signed (see the register).
- **Software execution does not validate combustion physics.** No human combustion expert outside the team has reviewed GFL's physics yet; that review is an open item.
