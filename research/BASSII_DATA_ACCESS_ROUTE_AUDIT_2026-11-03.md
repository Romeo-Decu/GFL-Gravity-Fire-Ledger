# FiF — Data Access Route Audit: NASA PSI and SDSU Research Archive

**Date:** 2026-11-03  
**Status:** Access-path assessment; no private data requested or retrieved  
**Scope:** BASS-II Bhattacharjee 100-µm PMMA comparison data

## 1. Executive finding

The most defensible route for the BASS-II raw media is now:

1. **NASA PSI-25, Version 4** — canonical public repository and first retrieval target.
2. **SDSU flame.sdsu.edu** — research-group archive identified by both NASA's report and Carmignani's dissertation; currently times out when accessed through the public web endpoint.
3. **SDSU research group / PI** — fallback for locating the legacy media and reduced Flame Analyzer/FIAT outputs if public links are unavailable.
4. **NASA GIPOC** — not assumed to be a public download route. It is an operations facility; current NASA Task Book material says a later SoFIE project downloaded its large data collection from GIPOC to an SDSU secure NAS. This is evidence about later SoFIE data custody, not proof that BASS-II data are held there or that FiF can access them.

## 2. NASA PSI-25 is the first retrieval target

NASA PSI-25 identifies BASS-II, DOI 10.60555/4qc4-de67, with CC0-1.0 licence. The current landing page reports Version 4, updated 24 November 2025, and exposes categories including:
- Investigation Metadata Files
- Engineering Documents
- Raw Data
- Reference Data
- Science Documents
- Reports
- Representative Images
- Experimental table

The Version 4 change log reports 694 files added and 131 removed. These are version-change counts, not a verified current inventory total.

The change log gives an example raw video filename:
BASS_GMT50_SAMPLE_147_TEST_B1.mp4

This establishes a useful naming pattern but does not establish the filename for B3. The B3 test-matrix row identifies sample 148, so BASS_GMT50_SAMPLE_148_TEST_B3.mp4 is only a search hypothesis and must not be treated as a verified asset path.

NASA PSI landing page:
https://psi.nasa.gov/physci/repo/data/investigations/PSI-25

## 3. SDSU archive and software

NASA/TM-20210011385, §2.3.6, says the BASS still images were converted into videos and posted together with videos from the downward experiments at flame.sdsu.edu. It describes Flame Analyzer as a MATLAB-based application for finding instantaneous flame spread rate from top-view video.

Carmignani's 2019 dissertation independently points to flame.sdsu.edu for FIAT information, instructions and video tutorials. The dissertation documents the BASS camera setup and metadata overlay.

The archive timed out on direct public-web access during this audit. This does not prove the site is offline; it may be a legacy host, a TLS/redirect issue, or a server that rejects automated requests.

## 4. Current SDSU research continuity — distinguish from BASS-II

NASA Task Book project Residence Time Driven Flame Spread: The Final Phase (FY2026) lists:
- PI: Subrata Bhattacharjee, San Diego State University;
- co-investigator: Luca Carmignani;
- project end date: 31 March 2027;
- NASA grant: 80NSSC21K1126;
- public PI email: prof.bhattacharjee@gmail.com.

The FY2026 report says the later SoFIE project downloaded more than 1 TB of experiment files (images, sensor recordings and telemetry) from GIPOC to a secure SDSU NAS and processed selected videos using Flame Tracker.

This confirms ongoing research continuity and identifies a potential institutional contact route. It does not establish that the SoFIE archive contains BASS-II files, that the legacy BASS archive has been migrated, or that the PI has agreed to share any additional material. No email has been sent.

NASA Task Book page:
https://taskbook.nasaprs.com/tbp/index.cfm?TASKID=2413F182B9F30E0CDB221036094EFF0F&action=public_query_taskbook_content

## 5. Immediate retrieval protocol

### Step A — PSI-25 inventory

In the PSI-25 landing page:
1. Select the Raw Data category.
2. Search B3, 148, and TEST_B3 independently.
3. Search engineering/reference documents for BASS data dictionary, video naming convention, Flame Analyzer outputs, sample/test mapping and calibration.
4. Record each candidate file's exact displayed name, size, date, category and download location.
5. Do not assume the file naming pattern is complete or unique.
6. Retrieve a small candidate set first; preserve the original filenames and calculate SHA-256 checksums after download.

### Step B — establish asset join

For each candidate media file:
- verify that embedded overlay, timestamps and test/sample IDs match the Appendix A.1 record;
- inspect image metadata and frame interval;
- establish the sample geometry and visible orientation;
- compare a representative frame with NASA Figure 2.20(B03);
- record whether the file is a still-derived video, original side video, or processed/composite video.

### Step C — normal-gravity counterpart

Search SDSU/PSI/reference materials for the downward 100-µm NASA PMMA specimen:
- run ID and date;
- sample grade/batch and manufacturing route;
- raw video or image sequence;
- reduced leading-edge position/time data;
- exact oxygen/pressure and ignition metadata.

### Step D — contact fallback

If PSI-25 does not expose the required assets or if the SDSU archive remains inaccessible, prepare a concise data-location request to the SDSU research group. Ask specifically for:
1. the BASS-II B03/B3 100-µm PMMA top-view image sequence/video;
2. the corresponding side-view video and telemetry/overlay if retained;
3. the 100-µm normal-gravity NASA PMMA downward-spread video used for NASA Figure 2.19/2.20;
4. the Flame Analyzer/FIAT reduced leading-edge position-versus-time data and processing settings;
5. a test/sample/video crosswalk and any material batch/property records.

The request should cite NASA/TM-20210011385, NASA PSI-25 DOI 10.60555/4qc4-de67, and the relevant figure/table identifiers. Do not ask for the later SoFIE archive as a substitute for BASS-II data.

## 6. Evidence and access boundaries

- NASA PSI-25 is a public repository and identifies the dataset as CC0-1.0.
- NASA's BPS Data portal describes PSI as the public physical-sciences data repository.
- The SDSU legacy archive is referenced by the research sources but was not retrieved in this audit.
- The current NASA Task Book's secure NAS/GIPOC description applies to the later SoFIE project, not necessarily to BASS-II.
- No login, restricted access, or private data has been accessed.
- No files have been downloaded or independently analyzed by FiF in this audit.
- No request or email has been sent.

## 7. Sources

1. NASA PSI-25, BASS-II, DOI 10.60555/4qc4-de67: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25
2. NASA/TM-20210011385, §§2.3.5–2.3.7 and Appendix A.1: https://ntrs.nasa.gov/citations/20210011385
3. Carmignani, L. (2019), Opposed-Flow Flame Spread over Solid Fuels in Different Burning Regimes: https://escholarship.org/uc/item/0rb693zc
4. NASA Task Book, Residence Time Driven Flame Spread: The Final Phase: https://taskbook.nasaprs.com/tbp/index.cfm?TASKID=2413F182B9F30E0CDB221036094EFF0F&action=public_query_taskbook_content
5. NASA BPS Data portal: https://science.nasa.gov/biological-physical/data/

**Decision:** Attempt PSI-25 file-level retrieval before contacting the SDSU research group. The current Task Book provides a credible fallback contact, but no outreach should be represented as having occurred.
