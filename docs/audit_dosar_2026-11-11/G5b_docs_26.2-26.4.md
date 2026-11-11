# Dossier audit, G5b docs 26.2-26.4

Independent agent report, 2026-11-11 evening (brief: AUDIT_BRIEF.md in this folder). Ground truth: repository at that time.

## 26.2. GFL Inscrierea in Competie.md
This is a chat transcript of the Space Apps registration: the account, the Universal Event, the team, adding Cristina, and the first compliance rules.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Register owner for the hackathon, choose Universal (virtual) Event | governance | delivered (per transcript; cannot be checked from the repo) | transcript; `docs/SPACE_APPS_2026_COMPLIANCE_CHECKLIST.md` row 1 still "Open" | critical |
| 2 | Team "Gravity Fire Ledger", official challenge Flame in Freefall (not Create-Your-Own) | governance | delivered (per transcript) | checklist rows 1–2 not updated (still Open) | critical |
| 3 | Cristina joins with a real role ("Project coordination & usability testing") | governance | delivered | `docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md` §2 | important |
| 4 | Disable "Accepting Team Members" | governance | not done (the site had no edit option) | transcript | nice |
| 5 | Declare AI use openly | docs | partial | `docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md` (v1.0 draft, "owner review"); DEC-034 still "Proposed", not signed | critical |
| 6 | Repo becomes public with an open-source licence at submission (NASA refuses unlicensed work; Apache-2.0 is the default) | governance | not done | no LICENSE file in the repo; checklist row 6 "Decision needed" | critical |
| 7 | Tick every compliance rule before submission (English, cite every source including AI tools, no commercial promotion, no PII) | governance | documented only | checklist rows 4–12 all "Open"; no References file found | critical |
| 8 | Add a ranking of experiments to the dashboard so every verb in the challenge statement (summarise / rank / interpret) is covered | analytics / UI | delivered (ranks table conditions, not physics) | `tools/rank_comparable_runs.py`, `data/derived/BASSII_COMPARABLE_RUNS_v1.json`, `visualization/gfl.html` ranking section | critical |
| 9 | Upload rehearsal on 14 Nov; package final by 15 Nov 19:59 | governance | not done yet (future date) | checklist row 3 "Planned" | critical |
| 10 | Team photo (GFL_mark_512.png) | UI | not done (optional) | none found | irrelevant |

**What the submission needs, according to this file, and whether it is ready:**
- **Registration, event, team, challenge:** done according to the transcript. The repo checklist was never updated, so the repo does not confirm it.
- **Team size: an unresolved contradiction.** The transcript says global judging needs at least 2 members. The checklist says teams of 1–6. Someone should check this against the official text.
- **Open-source licence and public materials:** not ready. There is no LICENSE file and the repo is still private.
- **English throughout:** the repo appears to be in English. The page, video and slides do not exist yet.
- **Cite every source, AI tools included:** not ready. There is no References or bibliography file.
- **No commercial promotion and no PII:** not reviewed yet (rows 8–9 Open). Note: "CCTI" appears once on the dashboard page and once in the README.
- **Deadline:** an internal contradiction. The file says Romanian registration closes 13 Nov, and later says registration stays open until 15 Nov.

## 26.3. GFL Analiza Tehnica 3.md
This is the session log for 5–6 Nov: re-acquiring the raw data, the signed ledger (WP-L), the vault boundary, the two-key zero-trust model, ChatGPT and Gemini reviews of B6, the B6 front-definition saga (DEC-029/032/033), and setting up the GFL project in AAL.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Re-download all 31 raw NASA files and match the SHA-256 hashes (first piece of the DEC-022 clean-room rebuild) | data / provenance | delivered | RES-003 | critical |
| 2 | DEC-022 in full: one-command rebuild from the manifest, breadth audit of all PSI-25 (129 tests, 695 files) with checks fixed in code beforehand, then SoFIE/SAFFIRE | analytics / data | not done | ISS-043 A8; GFL_MAP §2 ("No one-command rebuild"; "Breadth audit … not done"); SoFIE/SAFFIRE appear only in specs | critical (answers "you were lucky with one dataset") |
| 3 | Signed ledger: hash chain, Ed25519, `gfl verify`, retroactive registration, CI check | provenance | delivered | `src/gfl_ledger/core.py`, `tests/test_gfl_ledger.py`, `.github/workflows/tests.yml:34`, RES-004; 218 entries | critical |
| 4 | `gfl verify` reports missing objects separately from altered ones (ISS-030) | provenance | delivered | `core.py` verify ("ok/altered/missing") | important |
| 5 | Four entry types, with an instrument record attached at phase 1 | provenance | delivered | `TYPES` in core.py; `tools/ledger_register_release_a.py` `instrument()` | important |
| 6 | Vault sealed after phase 2; phases 3–4 append-only (DEC-025); names Evidence Vault / Derivation Ledger (DEC-027) | provenance / docs | partial | DEC-025/027; `docs/specs/SPEC_evidence_vault.md` itself says "partial"; no write-once storage | important |
| 7 | Evidence vault replicated in ≥2 places (IDEA-004); portable black box (IDEA-005) | provenance | dropped by decision (after the contest) | IDEA-004/005; `SPEC_portable_black_box.md` | nice |
| 8 | Architecture document (WP5) to carry: vault design, the owner's "stable pillar" sentence, a section "Zero-trust model — including the AI agent" | docs | not done | the phrase appears only in the register; not in `SCIENTIFIC_SYSTEM_ARCHITECTURE_v0.1.md` | important |
| 9 | RFC 3161 timestamp anchors from FreeTSA plus Git anchors after each session | provenance | delivered | `ledger/anchors/` (15 .tsr); RES-004 | important |
| 10 | Signing-key custody: Seagate copy with protocol (DEC-028), plus a second independent copy | provenance | partial | DEC-028 ("Second independent copy pending") | nice |
| 11 | Qualifiers inherited downstream; `gfl lineage` (DEC-030) | provenance / analytics | delivered | `core.py lineage()`; 17 qualification entries | critical (central to the method) |
| 12 | Separate owner key; approvals signed only by the owner (DEC-031); `gfl_owner.py` | provenance / governance | delivered | `tools/gfl_owner.py`, `ledger/keys/owner.pub.json`, `ledger/approvals/DEC-029.signed.json` | critical |
| 13 | Owner signs DEC-032 / DEC-033 / DEC-034 | governance | not done | only DEC-029 is signed (1 approval entry); GFL_MAP row 1 "Owner signatures pending" | important |
| 14 | PROJECT_STATE.md regenerated at the end of each session; replicated in 3 places | governance | not done | no such file | nice |
| 15 | Re-measure B6 and confirm 2.274 ± 0.094 mm/s | analytics | delivered | RES-006 (track byte-identical) | critical |
| 16 | B6 robustness: window scan, front definitions, autocorrelation of residuals | analytics | delivered | `tools/b6_sensitivity.py`, `data/derived/B6_SENSITIVITY_v0.1.json` | critical |
| 17 | Resolve ISS-034 (exposure effect) | analytics / physics | delivered | RES-007, `B6_SENSITIVITY_v0.2.json` (cause: brightening flame, not exposure) | critical |
| 18 | Radiometric / morphological audit answering red team #2 (edge sharpening, 6.3× check, saturation) | analytics / physics | delivered | `tools/b6_radiometric_audit.py`, `B6_RADIOMETRIC_AUDIT_v0.1.json`, RES-008 | critical |
| 19 | DEC-029 B6 wording: 2.27 mm/s, range 2.1–2.4 | analytics | superseded | DEC-041 (1.99 mm/s, R-W2), RES-033 (2.197, 1.915–2.368, R-W3); headline still open (GFL_MAP Q5) | critical (see cross-file findings) |
| 20 | DEC-032 per-frame threshold definition | analytics | dropped by decision | DEC-032 withdrawn (RES-008) | — |
| 21 | DEC-033: B6 reported as a frozen set of indicators, no single "front speed", term "luminous leading edge" | analytics | superseded | DEC-033 never moved past "Proposed"; DEC-040/041/055 pick a single reference definition (0.1, then 0.5 of peak); DEC-056 restores the "luminous-edge" label; multi-definition rates kept in `B6_SEGMENT_RATES_v2.json` | important |
| 22 | Piecewise fits per constant-flow interval, using the overlay flow timeline (ISS-013) | analytics / physics | partial | segment fits in `B6_SEGMENT_RATES_v2.json`; overlay at 3-s steps; automated OCR pending; flow speed at the sample still unknown (ISS-013, GFL_MAP) | critical |
| 23 | Apply the frozen definition to B15, B16, B19, B20 | analytics | not done | family measured instead on B9, B11, B13 (RES-033–038); ISS-029 (dim 17 % O₂ flames) still open, blocking the cross-O₂ test | critical |
| 24 | Map NEF archives to runs B19/B20 (ISS-032) | provenance | partial | closed for B9 (RES-035); B19/B20 still unresolved (qualifier `unresolved_mapping`) | important |
| 25 | Commit the two uncommitted session scripts (ISS-033) | provenance | not done | ISS-033 Open; no archive-index or re-acquisition tool in `tools/` | nice |
| 26 | Scale-plane correction (ISS-020) | physics | not done | ISS-020 "Open — plane correction"; ±3 % allowance in METHODS §5 | important |
| 27 | ChatGPT role-change prompt; red team #1 and #2 processed and recorded | AI layer | delivered | RES-005, RES-008; `data/external/2026-11-05_chatgpt_redteam2_DEC-032.md` | important |
| 28 | Blind reproduction by Gemini; re-execute its code; record it in the ledger with a qualifier | AI layer | delivered | RES-009/010, `data/external/2026-11-05_gemini_blind_B6/`, ledger qualifications | important |
| 29 | Rule: an external number counts only with its code and GFL's re-execution (ISS-035) | AI layer / governance | delivered | ISS-035; `tools/wf0011_cross_validation.py`, RES-019 | critical |
| 30 | Safe execution of AI-written code (ISS-037) | AI layer | delivered | `tools/wf0011_cross_validation.py` (temp dir, `python3 -I`, 120 s timeout) | important |
| 31 | GFL project in AAL, `gfl_review` pipeline, blind packets, team of 5 model families | AI layer | delivered | AAL `config/aal.yaml` (GFL, gfl_review, `independent: true`); PR #118 | important |
| 32 | AAL lessons L-013/L-014; ideas I-156 (auto re-execution in curation) and I-157 (signed AAL ledger) | AI layer | documented only | no re-execution code found in AAL | nice |
| 33 | Independent re-check by fresh agents (DEC-022 item 2) | governance | partial | RES-024 cold review; ISS-053 audit; no human expert (ISS-043 A3) | critical |

## 26.3.1. GFL Logo.md
This is a short log of how the logo was designed and adopted.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | Logo built from the measured B6 flame contour ("our logo is a measurement") | UI | dropped (the author abandoned it in the same document) | logo drawn from scratch instead | irrelevant |
| 2 | Node-flame on hash-linked blocks, geometry fully defined in code | UI / provenance | delivered | `visualization/assets/brand/make_logo.py`, DEC-026 | nice |
| 3 | Variants: full, flame-only, simple icon, inverted; 512/128/32 px | UI | delivered | `visualization/assets/brand/` (8 files) | nice |
| 4 | Old logo archived with a supersession note, nothing deleted | provenance | delivered | `archive/brand_v0/SUPERSEDED.md` | nice |

## 26.3.2 GFL Special Update Project Submission.md
This file covers the AI-disclosure rules from the Project Submission Guide (DEC-034, ISS-036), a recap of DEC-022/DEC-019, the AAL PR #118 audit triage (ISS-037), and the setup script for the AAL GFL project.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | "Use of AI" field lists every AI system, its role, and what it got wrong | docs | partial | `docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md` (draft); DEC-034 Proposed, not signed | critical |
| 2 | AAL named as CCTI's private orchestration platform | docs | delivered | disclosure §4 | important |
| 3 | AI metadata: commit trailers, an `AI_USE` section in the README for older history, model named in the ledger | provenance / docs | partial | README has only a pointer, no AI_USE section; about 169/225 commits carry trailers; the disclosure claims "All work is in Git with Co-Authored-By trailers", which is not true for the early commits (ISS-036) | critical (Submission Guide rule) |
| 4 | Visible "generated by AI-written code" label on logo and visuals; no NASA branding | UI / docs | partial | label exists only in docs (disclosure §6, checklist row 13); not on `gfl.html` or the brand assets; no NASA logo found in assets | critical (watermark rule) |
| 5 | Methods declared with maturity V/P/D; potential shown as a roadmap, not as a capability | docs / analytics | partial | `research/fixtures/GFL_CAPABILITIES_v1.json`, dashboard function map, GFL_MAP §2; 16 specs | critical |
| 6 | Every development direction states data, model, validation and blocker (DEC-014 format) | docs | partial | `docs/specs/*.md` (16) — format compliance not checked one by one | important |
| 7 | Show the correction process (DEC-032 withdrawn, Gemini table, checklist error) | docs | delivered | register; dashboard experiment memory | important |
| 8 | Second analysed experiment: full PSI-25 audit, then SoFIE/SAFFIRE (9–11 Nov) | analytics / data | not done | GFL_MAP §2; ISS-043 A5/A8 | critical |
| 9 | Pending work: dim 17 % O₂ flames (ISS-029), B19/B20 (ISS-032), rule engine v0.2, dashboard | analytics / UI | partial | dashboard delivered; ISS-029 and B19/B20 open | important |
| 10 | Safe-execution protocol for AI code (ISS-037) | AI layer | delivered | `tools/wf0011_cross_validation.py` | important |
| 11 | Restrict AAL Red_Team/Validator reads to blind_api_*/redteam_* | AI layer | delivered | AAL commit 3adbe60 | nice |
| 12 | `AAL_GFL_setup.ps1`; create WF "GFL-R1" | AI layer | delivered | WF-0010/0011 created (26.4) | nice |

**What the submission needs, according to this file, and whether it is ready:**
- **Mandatory "Use of Artificial Intelligence" field:** draft text exists in the disclosure. DEC-034 is not owner-signed. Not final.
- **Visible watermark on AI-generated images and video:** not ready. There is no label on the page or assets, and no video exists yet.
- **AI acknowledgement in code/data text and metadata:** partial. The README has no AI_USE section, and the disclosure overstates trailer coverage.
- **No NASA branding in AI material:** appears satisfied; no NASA logo found in the assets.
- **Originality and intent judged in an AI context:** covered in substance by the disclosure, which separates who did what.
- **Not covered by this file or the checklist, from my general knowledge of Space Apps, unverified:** the submission normally needs a project summary and a demo (short video or slides) plus a link to the project. None of these exist in the repo. The checklist itself says the Submission and Judging guides should be re-read on 13 Nov.

## 26.4. GFL Test AAL.md
This is the log of the first AAL test run (WF-0010/WF-0011): AAL bugs found and fixed, the brief for robust API execution, the Kimi result, and the blind-packet leak and its fix.

| # | Commitment | Area | Status | Evidence | Criticality |
|---|---|---|---|---|---|
| 1 | API executor uses roles assigned per project (UI bug) | AI layer (AAL) | delivered | AAL PR #119 (220f6f4) | irrelevant for the jury |
| 2 | Robust API execution: cost cap, streaming, diagnostics, enforced format, UI progress (brief 35, PR-A) | AI layer (AAL) | delivered | AAL PR #120 (873456a) | nice |
| 3 | PR-B: per-agent scorecard from validation agreement; eject agents that invent numbers | AI layer (AAL) | not done | no scorecard or ejection code in AAL | nice |
| 4 | Separate DB connection for the background call (#121); independent phase (#122); I-161 role fix | AI layer (AAL) | delivered | AAL #121, #122, #126 (8f4d3d6); ISS-039 | important (blindness of the test) |
| 5 | Archive WF-0011 with SHA-256 and register it in the GFL ledger | provenance | delivered | `data/external/2026-11-0{6,8,9}_aal_WF-0011*` | important |
| 6 | Re-execute Kimi and DeepSeek scripts on full data before evaluating their method | analytics / AI layer | delivered | RES-012, RES-019, `WF0011_CROSS_VALIDATION_v0.1.json` (Kimi 0.43 mm/s, unstable; DeepSeek rejected) | important |
| 7 | Complete the AAL GFL charter (CHARTER_INCOMPLETE) | governance | not done | AAL `charter: advisory`; nothing found | irrelevant |
| 8 | Brief upload only by copy/paste (note it as an improvement idea) | AI layer | documented only | not checked further | irrelevant |
| 9 | AAL kept off GFL's critical path (ISS-038) | governance | delivered in effect | WF-0011 stopped by the owner (RES-018); GFL closed the question deterministically (RES-019) | important |
| 10 | Remaining AAL defects fixed after the contest | AI layer | dropped by decision (deferred) | ISS-041 | irrelevant |

## Cross-file findings
- **The analytics core promised for Release A is mostly absent as platform modules.** GFL_MAP §2 itself marks regime gates computed from data, CRAM-1 (de Ris), CRAM-2 and CRAM-3 as not met. CRAM-2 has only "first evidence" (exploratory ratios). Anomaly detection is partial, with no standalone detector. Nothing in these files' commitments gets beyond B6 sensitivity tools and window rules, which live as research scripts in `tools/`, not in `src/`. `src/` contains only the transfer engine, the ledger and the MCP server.
- **DEC-022 is not done.** No one-command rebuild, no breadth audit of PSI-25, no second investigation (SoFIE/SAFFIRE). 26.3 and 26.3.2 both name this as the answer to "you were lucky with one odd dataset". Its absence is the biggest scientific-credibility gap (ISS-043 A5/A8).
- **The only owner-signed approval is contradicted by the current numbers.** DEC-029 (signed: B6 = 2.27 mm/s, range 2.1–2.4) is contradicted by the current results: 1.99 mm/s (DEC-041, R-W2) lies outside 2.1–2.4, and R-W3 gives 2.197 (1.915–2.368). The newer numbers were approved but never signed with the owner key. No signed supersession of DEC-029 was found; the headline is still undecided (GFL_MAP Q5).
- **DEC-033 was never adopted and was quietly overtaken.** It said "no single front speed is selected; freeze the indicator list". DEC-040/041/055 later chose a single reference definition, first 0.1 of peak, then 0.5 after ISS-047 showed 0.1 is biased low. No register entry marks DEC-033 as superseded or rejected; it still reads "Proposed".
- **The test planned for the measured family was not run.** The family measurement promised in 26.3 (B15, B16, B19, B20 under one frozen definition, then a cross-O₂ holdout) did not happen. ISS-029 (dim 17 % O₂ flames) and ISS-032 (B19/B20 mapping) remain open. Transfer was instead tested on B9/B11/B13: 1 supported, 1 not supported, 2 not testable.
- **Physics inputs still open:** the flow speed at the sample (ISS-013) and the scale-plane correction (ISS-020). Every rate carries these as unresolved systematics, and the "flow independence" evidence for CRAM-2 depends on ISS-013.
- **The submission is not ready on hard eligibility points.** There is no LICENSE file, the repo is private, there is no References file, DEC-034 is not signed, and there is no visible AI label on the logo or visuals. There is also no video, slide deck or project summary in the repo. Every row in the compliance checklist is still "Open".
- **The disclosure overstates its own metadata.** `AI_AND_TOOLS_DISCLOSURE_v1.0.md` says "All work is in Git with Co-Authored-By trailers". ISS-036 records 118/162 early commits without trailers, and about 56 of 225 commits still lack one. The README AI_USE section promised by DEC-034 is missing. This is a contradiction a judge could find.
- **Small inconsistencies inside 26.3:** it says "2.07–2.42 fits inside 2.1–2.4", but 2.07 is below 2.1. In 26.2, "two members are required for global judging" conflicts with the checklist's "team 1–6".
- **Ideas recorded but not built (correctly marked as ideas, not capabilities):** IDEA-004/005 vault replication and the portable box, AAL I-156 re-execution in curation, the AAL agent scorecard, and PROJECT_STATE.md. The page and the jury text must not present any of these as existing.

Key files: `/home/claude/fif/docs/GFL_MAP_2026-11-11.md`, `/home/claude/fif/docs/DECISION_ISSUE_IDEA_IMPLEMENTATION_REGISTER_v0.1.md`, `/home/claude/fif/docs/SPACE_APPS_2026_COMPLIANCE_CHECKLIST.md`, `/home/claude/fif/docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md`, `/home/claude/fif/src/gfl_ledger/core.py`, `/home/claude/fif/ledger/approvals/DEC-029.signed.json`, `/home/claude/fif/data/derived/B6_SEGMENT_RATES_v2.json`, `/home/claude/aal/config/aal.yaml`.
