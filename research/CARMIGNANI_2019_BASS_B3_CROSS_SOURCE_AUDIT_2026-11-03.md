# FiF — Cross-Source Audit: Carmignani 2019 Thesis and BASS B3

**Date:** 2026-11-03  
**Status:** Supporting primary-research source; linkage strengthened, comparison result still unresolved  
**Document:** Luca Carmignani, *Opposed-Flow Flame Spread over Solid Fuels in Different Burning Regimes*, PhD dissertation, UC San Diego / San Diego State University, 2019.  
**Permanent source:** https://escholarship.org/uc/item/0rb693zc  
**PDF:** https://escholarship.org/content/qt0rb693zc/qt0rb693zc.pdf

## 1. Why this source matters

The dissertation provides an independent, detailed account of the BASS apparatus, experiment matrix, imaging and flame-tracking methods. It is a research source from the same SDSU research group involved in the NASA BASS-II work, not a secondary web transcription.

It provides useful cross-checks for the BASS test matrix and the data-processing lineage. However, it must not be conflated with the NASA BASS-II report: source names, project phases, experiment identifiers and comparison analyses must remain attached to their originating documents.

## 2. BASS B3 cross-check

The dissertation's Appendix A, Table A.2, lists:
- Experiment: B3
- Thickness: 0.1 mm
- Width: 20 mm
- Flow velocity: 2–0 cm/s (initial-to-final)
- Oxygen concentration: 22.2%

This agrees numerically with the NASA BASS-II Appendix A.1 B3 record in the following fields:
- nominal thickness: 100 µm;
- width: 2 cm;
- calibrated initial O2: 22.2%;
- calibrated final O2: 21.8%;
- Air display: 2 cm/s.

The dissertation table reports a single oxygen concentration of 22.2%, not the NASA report's initial/final pair. Do not infer that the dissertation table independently validates the final value or the calibration procedure.

**Interpretation:** The cross-source match strengthens the identification of the B3 test-matrix record. It does not, by itself, establish which video/image asset is Figure 2.20(B03), nor does it link B3 to the 2.2 mm/s comparison result in NASA Section 2.3.

## 3. Imaging and measurement chain

The dissertation states:
- BASS used a 76 × 76 mm square wind tunnel inside the ISS Microgravity Science Glovebox.
- The flow was measured with an omnidirectional spherical air-velocity transducer (TSI 8475).
- Twenty-two flat PMMA samples were tested, approximately 100 mm long, with flow velocities from 0 to 42 cm/s, oxygen from 15 to 22.2%, thickness from 0.1 to 0.4 mm, and width 10 or 20 mm.
- A side-view Panasonic WV-CP654 camera recorded at 760 × 480 pixels.
- Top-view still images from a Nikon D300s (4320 × 2968 pixels) were taken approximately once per second.
- Radiometer signal, measured flow velocity and fan power were superimposed on experiment videos and could be associated with flame positions during image analysis.
- The Flame Image Analyzer Tool (FIAT) was developed to track flame behavior; the dissertation says further details, instructions and video tutorials were available at flame.sdsu.edu.

This gives FiF a more precise list of expected media and metadata than the NASA summary alone. It does not mean the original media are now accessible or have been inspected.

## 4. Important B3 versus 3 cm/s discrepancy

The NASA Summary Report, Section 2.3.6, says that the 100-µm comparison experiment used 3 cm/s opposing flow in microgravity.

The NASA Appendix A.1 B3 row reports 2 cm/s in its Air display field. The dissertation's Appendix A.2 independently lists B3 as 2–0 cm/s.

The dissertation also discusses 100-µm tests B6 and B1 in Figure 5.4 at a stated 3 cm/s comparison condition, with oxygen levels of 21% and 22.2%, respectively. That passage concerns flame-length and numerical-profile comparisons; it does not identify the 2.2 mm/s result in NASA Figure 2.19 as B3.

Therefore:
- B3 is a strong candidate for the B03 image/test-matrix identity.
- B3 is not yet linked to the NASA Section 2.3 comparison's 3 cm/s condition.
- The 2.2 mm/s result must not be assigned to B3 solely from thickness or figure proximity.
- B1/B6 are additional candidate 100-µm runs in the dissertation's distinct analysis context; they must not be substituted into NASA Figure 2.19 without a source-level join.

## 5. Normal-gravity comparison data

The dissertation documents separate downward-spread experiments and describes the Flame Stabilizer apparatus, sample handling, video recording and flame-tracking approach. This supports the existence of a traceable ground-experiment data stream at SDSU.

It does not yet identify the exact 100-µm NASA PMMA run shown in NASA Figure 2.20(e), nor provide its raw video filename, sample batch/grade, reduced time series or run identifier.

The normal-gravity link remains open.

## 6. FiF data-lineage status

| Evidence link | Current status |
|---|---|
| NASA Appendix A.1 B3 ↔ dissertation Appendix A Table A.2 B3 | Strong cross-source match on thickness, width, initial flow and O2 |
| B3 ↔ BASS-II B03 image in NASA Figure 2.20 | Strong candidate; original asset-level join not yet inspected |
| B3 ↔ NASA Section 2.3 3 cm/s comparison condition | Unresolved; B3 matrix says 2–0 cm/s |
| B3 ↔ NASA Section 2.3 2.2 mm/s result | Not established |
| NASA Figure 2.20(e) ↔ exact normal-gravity 100-µm run | Unresolved |
| Original videos / stills / reduced data retrieved by FiF | No |

## 7. Decision and next actions

1. Add the dissertation as a linked source in the FiF source register.
2. Preserve the B3 cross-source agreement as a provenance relation, not as proof of spread-rate attribution.
3. Retrieve or request the BASS media and FIAT/Flame Analyzer data from the SDSU research archive or responsible research group.
4. Identify the exact 100-µm normal-gravity run corresponding to Figure 2.20(e).
5. Reconcile the 2 cm/s B3 matrix value with the 3 cm/s condition stated for the Section 2.3 comparison.
6. Only after these joins are established, construct the first machine-readable matched experiment pair.

## 8. Source locations in the dissertation

- Bibliographic identity and authorship: front matter, PDF pages iii–iv.
- BASS apparatus, imaging and experiment conditions: Chapter 2, §2.4, printed pp. 16–17; PDF text lines around 1257–1279.
- FIAT description and SDSU archive reference: Chapter 2, §2.5, printed pp. 16–19; PDF text lines around 1280–1300.
- BASS B3 matrix: Appendix A, Table A.2, printed p. 105; PDF text lines around 4088–4112.
- 100-µm B1/B6 3 cm/s comparison in a separate flame-length analysis: Chapter 5, printed pp. 74–75; PDF text lines around 3098–3114.

**Conclusion:** The dissertation materially strengthens B3's experimental metadata provenance and clarifies the expected video-processing chain. It does not close the central quantitative data join between B3 and the NASA Section 2.3 2.2 mm/s result.
