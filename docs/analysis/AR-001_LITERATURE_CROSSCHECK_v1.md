# AR-001 literature cross-check (DEC-045)

**Date:** 2026-11-10 · **Author:** Claude (PM) · **Status:** cross-check against the literature, **not a peer review**

No external combustion-science expert has reviewed GFL's B6 physics (DEC-045). This record does the next best thing that can be checked: it compares the B6 result and its interpretation with what the sources in the project library and the acquired NASA documents report, and says where they agree, where they cannot be compared, and what remains open. Every statement cites its source; values reported by others are not GFL measurements.

## 1. The result being checked

AR-001 / DEC-041: B6, BASS-II, 100 µm PMMA film, 20 mm wide, airflow display setting 3 (18.5–28.6 s): leading-edge spread rate **1.99 mm/s** (reference definition, 0.1 of each frame's peak), front-definition range 1.99–2.54 mm/s, provisional. The airflow display setting is not established in cm/s (ISS-013).

## 2. Sources used

| ID | Source | What kind of evidence |
|---|---|---|
| S1 | Olson et al., NASA/TM-20210011385 (2021), Section 2.2–2.3 and Appendix A.1 | NASA report; summary values; the experimental table |
| S2 | Bhattacharjee et al., "Opposed-flow flame spread: A comparison of microgravity and normal gravity experiments to establish the thermal regime", *Fire Safety Journal* 79 (2016) 111–118, DOI 10.1016/j.firesaf.2015.11.011 (project library) | Peer-reviewed paper on the same BASS-II thin-PMMA series |
| S3 | Carmignani, *Opposed-Flow Flame Spread over Solid Fuels in Different Burning Regimes*, PhD dissertation, UCSD/SDSU (2019), Appendix A Table A.2 and Chapter 5 | Dissertation; B6-specific discussion |
| S4 | de Ris (1969) thin-fuel opposed-flow formula, as presented in S1 §2.3 and in Rojas-Alva (2022, project library, Eq. 5) | Theory |
| S5 | Rojas-Alva, *Flammability of Materials intended for use in Microgravity Environments* (2022, project library), literature tables | Review of the field; context only |

Extractions already in the repository: `research/BASSII_B6_CARMIGNANI_2019_EXTRACTION_v0.1.md`, `research/SECTION_2_3_100UM_DATA_LINKAGE_AUDIT_2026-11-03.md`, `research/PHYSICS_AND_COMBUSTION_FRAMEWORK_THIN_PMMA_v0.1.md`.

## 3. Comparisons

| # | Question | What the sources report | GFL B6 | Verdict |
|---|---|---|---|---|
| L1 | Is the magnitude plausible for 100 µm PMMA in microgravity? | S1/S2: highest microgravity spread rate ≈ 2.2 mm/s for 100 µm while opposing flow was varied over roughly 1–40 cm/s; normal-gravity downward average ≈ 2.0 mm/s | 1.99 mm/s (1.99–2.54 across definitions) | **Consistent.** A single-segment rate at or below a reported series maximum is expected. |
| L2 | Does B6 itself have a published rate? | S3: B6 at a nominal 3 cm/s and B1 at 5 cm/s both spread at approximately 2 mm/s (dissertation, approximate, interval and front definition not stated) | 1.99 mm/s at display setting 3 | **Consistent, weakly.** Same run and same nominal flow label; the dissertation value is approximate and its method differs (FIAT), so this is agreement in magnitude, not a reproduction. |
| L3 | Is the thermal regime assumption reasonable at this flow? | S2: thin-PMMA spread in microgravity and downward normal gravity fit the de Ris thermal regime (coefficient 4.76 for 21 % O₂); S4: in the thin thermal regime the rate does not depend on opposing-flow velocity. S1 §2.2: a separate 100 µm test extinguished near 1.1 cm/s when flow was reduced (radiative regime at very low flow) | Setting 3, nominally 3 cm/s in S3 | **Plausible, not established.** Nominal 3 cm/s lies above the reported extinction flow; how close B6 is to the radiative regime is not quantified (no emissivity or local velocity measurement in GFL). |
| L4 | Does the flow label mean cm/s? | S3 lists B6 flow as 1–7 cm/s (initial–final pair) and discusses it at 3 cm/s; S1 Appendix A.1 records "Air display: 3 5 approaching 10" for B6; S1 §2.3 gives 3 cm/s for the 100 µm comparison while the B3 table row says 2 | display setting 3 | **Conflict between sources, kept open (ISS-013).** S3's 1–7 cm/s and S1's display sequence ending near 10 do not match; the anemometer has a response time of about one minute (S3). GFL does not convert the display to cm/s. |
| L5 | Does the flame edge GFL measures correspond to what others call the spread front? | S3 measures the leading edge with FIAT; S1 describes a MATLAB "Flame Analyzer" thresholding top-view video | luminous leading edge at fixed fractions of each frame's peak, eight definitions | **Comparable in intent, not in definition.** Neither source gives a threshold that can be applied to raw stills; the 1.99–2.54 definition range is GFL's own statement of this ambiguity. The offset between luminous edge and pyrolysis front is unknown in all three. |

## 4. What the literature does not settle

1. Whether B6's display setting 3 equals 3 cm/s at the sample (L4).
2. Whether B6 at that flow is fully in the thermal regime or already influenced by radiative loss (L3).
3. Any uncertainty for the published values: S1, S2 and S3 give none for these rates.

## 5. A prediction registered before measurement

S2 and S4 imply that, in the thin thermal regime, spread rate scales inversely with fuel thickness. GFL's comparable-run ranking (`data/derived/BASSII_COMPARABLE_RUNS_v1.json`) lists **B11** (2 cm, 200 µm PMMA film, flow restrictor 2, 21 % O₂, air display sequence including 3) as "close" to B6 with thickness as the only differing recorded condition.

**Prediction (registered 2026-11-10, before any B11 file has been acquired or measured by GFL):** if B6 and B11 at display setting 3 are both in the thin thermal regime, B11's leading-edge rate under the same window rule (R-W2) and the same reference definition is about half of B6's, i.e. **0.85–1.15 mm/s** (1.99 / 2 ≈ 1.0 mm/s, ±15 % for front-definition spread and scale). A value outside this band means the inverse-thickness scaling is not supported for this pair at this flow. If B11 has no AIR-3 segment that passes the rule's gates, the test is reported as not possible, not as passed. S2 already reports that thin-PMMA maxima across thicknesses fit de Ris; this is a check that GFL's measurement chain reproduces that scaling on a run it has not yet seen, not a new physical claim.

## 6. Conclusion

The B6 result is consistent in magnitude with every published value that can be compared (L1, L2), and its thermal-regime interpretation is plausible but not established at this flow (L3). The sources conflict on what the flow setting means (L4), and none of them, including GFL, measures the pyrolysis front (L5). The cross-check therefore supports keeping AR-001 as **provisional** and does not upgrade it.
