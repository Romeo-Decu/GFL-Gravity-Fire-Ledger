# FiF — NASA Combustion Evidence Family Inventory v0.1

**Status:** Initial discovery inventory — not a verified dataset catalogue  
**Date:** 2026-11-04  
**Working branch:** `acquisition/pmma100-bass-b3`  
**Project gate:** Gate 1 — Evidence Inventory  
**Companion control document:** `docs/PROJECT_CONTROL_BASELINE_AND_EVIDENCE_RECONCILIATION_PLAN_v0.1.md`

---

## 1. Purpose and interpretation

This document records the NASA combustion-research experiment families already identified in the FiF research baseline. It is the first inventory layer, not a declaration that every family has been retrieved, inspected or reconciled.

The purpose is to stop treating “NASA combustion data” as one homogeneous collection. Each programme/family is a discovery group. Individual investigations, campaigns, runs, specimens, measurements, files, publications and derivative products must later receive separate identities.

**Inventory rule:** inclusion here means “identified as a candidate evidence family in the current FiF research record”. It does not mean that its source files, data completeness, experimental metadata, licence, acquisition method or scientific suitability have been independently verified.

## 2. Source basis and limits

This initial inventory is based on:

1. The attached FiF research document, *Cercetare pentru NASA Space Apps.txt*, section “Documentația NASA” and its experiment-family overview.
2. Existing FiF repository records, especially:
   - `research/FIRST_PHYSICS_CASE_SELECTION_v0.1.md`
   - `research/LANDSCAPE_AND_DIFFERENTIATION_DECISION_v0.1.md`
   - `research/BASSII_DATA_ACCESS_ROUTE_AUDIT_2026-11-03.md`
   - `research/PMMA_SOURCE_RECONCILIATION_AUDIT_v0.1.md`
   - `docs/SCIENTIFIC_EVIDENCE_ACQUISITION_PROTOCOL_v0.1.md`
3. Existing repository README and source-specific audit records.

The attached research document identifies NASA PSI research categories and names ACME, BASS, BASS-II, FLEX, FLEX-2, SAFFIRE, SAME, SAME-R and SPICE. It also describes SoFIE as a high-priority solid-fuel family. Existing FiF landscape review additionally references LUCI as an adjacent record used by MicroFire Atlas; LUCI is not promoted here to a confirmed NASA combustion family or PSI collection.

No complete NASA PSI catalogue export, full set of investigation landing pages, raw file inventory or collection-wide metadata audit has yet been completed in this step.

## 3. Family-level inventory

The family descriptions below preserve the scope stated in the existing FiF research baseline. They are discovery labels, not proof that all individual tests within a family share the same phenomenon, apparatus or data structure.

| Inventory ID | Family / programme | Evidence domain indicated by current FiF sources | Initial FiF relevance | Current identification state |
|---|---|---|---|---|
| FAM-001 | BASS | Burning/suppression of solid fuels; ignition, flame growth/spread and extinction under forced flow | High; related historical family, must remain separate from BASS-II | Named in attached research document; individual collection and source records not inventoried here |
| FAM-002 | BASS-II | Solid-fuel burning/suppression; opposed-flow flame spread, ignition and extinction; PMMA case selected | Very high; first reconciliation pilot | PSI-25 Version 4 identified; DOI 10.60555/4qc4-de67; detailed source audits already exist |
| FAM-003 | SoFIE | Solid-fuel ignition and extinction; effects of fuel temperature, geometry, flow, oxygen and pressure are identified in the FiF baseline | Very high; candidate for second solid-fuel evidence family | Named in attached research document and repository context; individual investigation IDs, datasets and file inventory not yet recorded in this catalogue |
| FAM-004 | SAFFIRE | Larger-scale spacecraft fire experiments; flame spread/fire development and smoke behaviour in an uncrewed Cygnus vehicle | Very high; scale/configuration contrast to material-scale tests | SAFFIRE-I PSI-98 and DOI 10.60555/0t15-1z43 identified in attached research baseline; version/file inventory not completed |
| FAM-005 | SAME | Smoke and aerosol measurement/characterization | High for detection and combustion-product evidence; not a flame-spread dataset | Named in attached research document; investigation-level inventory not completed |
| FAM-006 | SAME-R | Follow-on/related smoke and aerosol measurement family | High for smoke/aerosol evidence; keep distinct from SAME until lineage is established | Named in attached research document; exact collection identifiers and relationship to SAME not reconciled |
| FAM-007 | FLEX | Liquid-droplet combustion, flame behaviour and extinguishment | Selective; separate physical phenomenon from solid-fuel spread | Named in attached research document; individual dataset inventory not completed |
| FAM-008 | FLEX-2 | Follow-on/related droplet-combustion and flame-extinguishment research | Selective; do not merge records with FLEX by name alone | Named in attached research document; exact investigation and data lineage not inventoried |
| FAM-009 | ACME | Gas-phase, non-premixed flame experiments | Selective; useful for gas-flame mechanisms, not automatically direct evidence for solid-fuel spread | Named in attached research document; individual experiment inventory not completed |
| FAM-010 | BRE | Burning Rate Emulator; gas-fuel-based simulation of selected solid/liquid material burning conditions, as described in the FiF baseline | Selective; keep separate from other ACME experiment tracks | Named in attached research document; exact investigation IDs and data assets not inventoried |
| FAM-011 | SPICE | NASA PSI combustion-related investigation family named in the attached source | Undetermined until primary investigation scope and data are inspected | Name identified; no experiment-level description or file audit completed |

### 3.1 Separate entities — do not collapse

The following are intentionally separate inventory entries:

- BASS and BASS-II;
- SoFIE and BASS-II;
- SAME and SAME-R;
- FLEX and FLEX-2;
- ACME and BRE.

A shared programme name, follow-on relationship, common facility, similar material or overlapping scientific objective is not sufficient to merge evidence records. Relationships will be represented explicitly only when supported by primary programme documentation.

### 3.2 Adjacent / external reference — not a NASA family entry

**LUCI:** mentioned in the FiF competitor landscape review as an evidence record included by MicroFire Atlas. It is retained as an external/adjacent reference for competitor-audit purposes only. This inventory does not establish its NASA programme status, data custody, or comparability with the families above.

## 4. Known collection-level identifiers and access routes

| Family | Known collection / identifier | Source route currently recorded | What is actually established |
|---|---|---|---|
| BASS-II | PSI-25, Version 4; DOI 10.60555/4qc4-de67 | NASA PSI-25 investigation page | Collection identity, version and DOI are recorded. Individual raw files and complete file-to-run mappings are not yet reconciled. |
| SAFFIRE-I | PSI-98; DOI 10.60555/0t15-1z43 | NASA PSI investigation record | Collection identity and DOI are named in the attached FiF research document. Version and file inventory remain open. |
| SoFIE | No specific PSI investigation ID entered in this inventory | NASA PSI / NASA project and Task Book records to be located per investigation | FiF research notes describe later SoFIE data custody involving GIPOC and a secure SDSU NAS. This is not evidence that BASS-II files are held there or that the full SoFIE collection is publicly accessible. |
| Other families | No specific collection identifiers entered | NASA PSI investigation catalogue to be searched | Family names only at this stage. |

### 4.1 BASS-II access boundary retained from prior audit

The current FiF audit identifies NASA PSI-25 as the primary public retrieval route for BASS-II. NASA/TM-20210011385 is the primary report used in the PMMA case. The SDSU `flame.sdsu.edu` archive is cited by NASA as a location for still-image-derived videos and downward-test videos, but direct access timed out during the earlier audit. This does not prove that the archive is offline or complete.

The AWS `s3://nasa-psi` bucket is **not** an established BASS-II route. Existing audit notes state that its exposed top-level resources did not establish BASS-II availability. Do not use it as a BASS-II source without locating a specific object.

## 5. Inventory completeness by evidence layer

At family level, the following fields are required for each individual investigation and then for each experiment/run/sample:

| Evidence layer | Required inventory fields | Current family-level status |
|---|---|---|
| Identity | NASA investigation ID, PSI ID, DOI, programme, campaign, experiment/run/test/sample identifiers, aliases | Partial; BASS-II and SAFFIRE-I have collection identifiers; most others remain family-name only |
| Scientific scope | Phenomenon, phase(s), fuel/oxidizer, outcome measured, research question | Partial; broad family descriptions only |
| Experimental context | Gravity/acceleration, pressure, atmosphere, oxygen, flow, geometry, orientation, ignition, boundary conditions | Not inventoried family-wide |
| Material / specimen | Material, grade, batch, manufacture, dimensions, conditioning/history, property source | Not inventoried family-wide; BASS-II PMMA has a dedicated preliminary audit |
| Apparatus | Facility, chamber/duct, holder, camera, sensors, model/range, placement, response time | Not inventoried family-wide |
| Acquisition | Instrument outputs, sampling frequency, frame interval, synchronization, calibration and timebase | Not inventoried family-wide |
| Original assets | Exact filenames, paths, sizes, formats, checksums, archive membership, access/licence | Not inventoried family-wide |
| Processing | Software/scripts, version, filters, thresholds, calibration, conversions, derived media/data | Not inventoried family-wide |
| Publication lineage | Source reports, papers, figures/tables, cited source datasets, reproduced/secondary records | Partial; strong BASS-II source trail, not complete for other families |
| Quality / uncertainty | Instrument uncertainty, measurement uncertainty, processing uncertainty, missing/conflicting metadata | Not inventoried family-wide |
| Access state | Public/restricted/inaccessible/not found; retrieval date and method | Partial; BASS-II route audited, others open |
| Competitor representation | Platforms using the record, displayed values, labels, omitted metadata, transformations | Partial; MicroFire Atlas limited inspection only |

“Not inventoried” means FiF has not yet performed the relevant family-wide audit. It does not mean the information is absent from NASA records.

## 6. Evidence-family separation and future pairing logic

The family catalogue is only the top level. The working hierarchy for subsequent inventory is:

`Research family → NASA investigation/collection → campaign/experiment → run/test → specimen/sample → acquisition stream → original asset → derivative asset → extraction/assertion → publication claim`

Not every family will use every level or the same terminology. FiF must preserve the source's native entity names and map them to a shared internal structure only with explicit mapping provenance.

For a single run, multiple streams may exist (for example, top-view still images, side-view video, sensor telemetry and processed video). These are separate assets with candidate relationships. A report, thesis and secondary application may all describe the same run but are not independent experiments.

The first reconciliation unit remains BASS-II B3/sample 148. B1 is a separate run dossier. No cross-run comparison or control designation is implied by this inventory.

## 7. Priority for detailed inventory

The following is a work-priority order, not a scientific ranking:

1. **BASS-II** — complete the already-started source and asset inventory; finish the B3 pilot dossier and keep B1 separate.
2. **SoFIE** — next solid-fuel family to inventory, because the FiF baseline identifies direct relevance to ignition/extinction and because later data-custody references exist. First establish exact investigation IDs and public data routes.
3. **SAFFIRE** — inventory run-level records, geometry, scale, materials, atmosphere, sensor/video streams and smoke/fire outcomes.
4. **SAME / SAME-R** — inventory as smoke/aerosol evidence, with separate investigation identities and measurement systems.
5. **FLEX / FLEX-2** — inventory liquid-droplet experiments separately from solid-fuel and gas-flame evidence.
6. **ACME / BRE** — separate individual gas-flame and emulator experiment tracks; determine which findings are directly relevant to the specific FiF question.
7. **SPICE** — establish primary source identity and scientific scope before assigning priority.

This order can change if the NASA challenge deliverable or actual data availability requires it. Any change must be recorded with rationale.

## 8. Next bounded task

**Next task: BASS-II family inventory completion (not another physical analysis).**

1. Enumerate PSI-25 investigation-level categories and all relevant source documents.
2. Inventory each available BASS-II data group by exact displayed name, category, version, size and URL.
3. Separate investigation metadata, engineering/reference documents, raw data, reference data, science documents, reports, representative images and experimental tables.
4. Identify experiment/run/sample records and preserve their exact native identifiers.
5. Build candidate links from records to files and publications; label every unverified join.
6. Record file acquisition and checksum status without claiming inspection where no bytes were retrieved.
7. Keep BASS-II family inventory separate from the B3 and B1 reconciliation dossiers.

After the BASS-II family inventory is stable, start the SoFIE investigation-level inventory. Do not attempt to compare these families scientifically until their own evidence records are sufficiently characterized.

---

**Gate 1 status:** initial family-level discovery inventory created.  
**Not complete:** investigation-level catalogue, file-level catalogue, metadata audit, acquisition verification and within-experiment reconciliation.
