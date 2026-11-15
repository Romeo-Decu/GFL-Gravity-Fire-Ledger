# GFL checked against NASA's Researcher's Guide to Combustion Science (2015)

**Source.** S. A. Gokoglu, D. L. Dietrich, D. P. Stocker, P. V. Ferkul, S. L. Olson, M. C. Hicks, *A Researcher's Guide to: International Space Station Combustion Science*, NASA ISS Program Science Office, NP-2015-10-034-JSC (2015). File `np-2015-10-034-jsc_combustion_in_reduced_gravity-iss-mini-book-011116-508.pdf`, SHA-256 `5fe046efe4e35e506023e27a9784d041e893026f19c9987591483614aea5d6b6`, from nasa.gov. The PDF is not in this repository; the quotes below were matched word for word against its text (pdftotext), on 2026-11-15.

**Why this check.** The guide is NASA's own summary of ISS combustion science, written by the scientists behind BASS and Saffire. GFL's statements about BASS-II, regimes, limits and fire safety should not contradict it. Where they are in tension, the tension is reported, not resolved by changing a rule after reading the source.

## Results

| # | GFL statement | Guide (page, verbatim) | Verdict |
|---|---|---|---|
| 1 | Central premise: a finding does not transfer to another context without declared limits; ground tests do not stand in for microgravity | p. 31: "NASA-STD-6001 Test 1 is not conservative, and materials can burn at lower oxygen levels in microgravity than on Earth." | **Consistent.** NASA's own BASS results show the standard ground test does not transfer conservatively to microgravity. |
| 2 | B6 is "consistent with the thermal regime" at 3.02 cm/s; CRAM-2 radiation number 0.31, just under GFL's "near a boundary" bound of 1/3 | p. 31: "At low-characteristic velocities (low-flame stretch), radiative loss begins to dominate"; the minimum of the flammability curve "is on the order of 10 cm/s and also corresponds to a maximum in the flame spread rate." | **Tension, reported.** B6 sits below the velocity NASA associates with the maximum spread rate, on the side where radiative loss grows. GFL's own number agrees that radiation is not negligible (0.31 of conduction). The 1/3 bound was set before this reading and is not moved; the regime label stays "consistent with", and this source is shown beside it. |
| 3 | Flow at the sample is not in NASA's BASS-II archive; listed as a limit and the next question | p. 21 (on SoFIE, BASS's successor): "The flow field must be well-characterized so the models will have accurate boundary conditions." | **Consistent.** NASA names a characterized flow field as a requirement for model boundary conditions. The guide does not say whether BASS recorded it. |
| 4 | Pyrolysis front and surface temperature are not in the archive; GFL reports luminous-edge rates | No surface-temperature or thermocouple measurement is described for BASS solid fuels; imaging is the diagnostic described (pp. 19–21). | **Consistent** (absence in the guide, not proof of absence in NASA's files). |
| 5 | BASS-II ran in air and at reduced oxygen (17 % O₂ dim flames, ISS-029) | p. 19: the glovebox air was diluted with nitrogen, "used to perform tests as low as 17 percent oxygen." | **Consistent.** |
| 6 | Incidents: Apollo 1 exposes a gap, no archive data for solids in enriched oxygen | SoFIE is planned for "oxygen from 10 percent to 40 percent by volume" (p. 19), i.e. future, not in the BASS archive. | **Consistent.** |
| 7 | Evidence map, suppression: archive evidence is thin and does not transfer by default | p. 31: "local application of suppressant is not adequate for flame extinguishment. The local jet entrains air and sustains the flame even when the ambient airflow is turned off." p. 22: nitrogen "can actually strengthen it". | **Consistent.** A ground suppression practice does not transfer as expected. |
| 8 | Ignition in microgravity differs from ground | p. 18: "Materials are easier to ignite in low gravity because of reduced natural convective cooling from the fuel surface." p. 24: the critical heat flux for ignition "can be as short as half the value measured in normal gravity". | **Consistent**, and outside GFL's measured scope (no ignition measurement). |

No GFL statement was found to contradict the guide. One tension (row 2) is recorded as a limit of the regime classification.

## What changes

Nothing in the rules, thresholds or results. Row 1 is added as a cited NASA source for GFL's premise; row 2 is stated next to the regime result. Register entry: RES-064.
