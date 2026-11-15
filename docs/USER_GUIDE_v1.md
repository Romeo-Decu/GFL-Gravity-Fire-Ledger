# GFL user guide: bring data in, take results out, get a report

**For:** a scientist who is not a programmer. **Status:** v1, 2026-11-12 (DEC-063). **Made with AI:** written by Claude (Anthropic) for team CCTI.

The GFL web page only reads: it shows results and lets you check them. The three operations below change or produce files, and each takes one command on a computer that holds the GFL repository and Python 3.10 or later. Open a terminal in the repository folder, type the command, read the answer on screen. Running these three operations from the web page itself (an upload field, a report button) is planned, not built: the evaluation of 15 November named it the main obstacle for a user who does not program (RES-065).

One rule applies throughout: whatever comes in keeps the label of where it came from. A value from a paper stays "source-reported"; it is never shown as a GFL measurement.

## 1. Bring data in

### 1.1 A result from another source

Use this for a spread rate published in a paper, measured by another team, or given by NASA's own analysis.

Make a table with one row per value, in a spreadsheet, and save it as CSV (or write JSON with the same field names):

| Column | Required | What to write |
|---|---|---|
| `source` | yes | who produced the value (author and year, team, "NASA SoFIE analysis") |
| `run` | yes | run name exactly as in NASA's BASS-II table (`B6`, `B11`) |
| `air_display` | yes | the AIR display value of the segment, in cm/s as shown on the rig |
| `rate_mm_s` | yes | the spread rate, in mm/s |
| `method` | yes | how it was measured, and what the interval means if you give one |
| `reference` | yes | where the value can be found (DOI, page, table, file) |
| `lo_mm_s`, `hi_mm_s` | no | lower and upper end of the interval; give both or neither |

Example file `my_results.csv`:

```
source,run,air_display,rate_mm_s,lo_mm_s,hi_mm_s,method,reference
Example et al. 2020,B6,3,2.10,1.95,2.25,"pyrolysis front from video, 95 % interval","doi:10.xxxx/xxxxx, Table 2"
```

Then:

```
python -m gfl_analysis import-results my_results.csv --out data/external/example_2020.json
```

What GFL does: it refuses any row with a missing or impossible field and tells you which row and why (it never repairs a row); for each accepted row it finds its own measurement of the same run and air display and reports the ratio and whether the intervals overlap. Possible answers: *intervals overlap*, *intervals do not overlap*, *external value inside / outside the GFL interval* (when you gave no interval), *no GFL measurement for this run and air display*, *run not in the NASA table*.

Read the answer with two cautions that GFL prints with it. Overlap is not proof of agreement, because two methods can share a bias. And GFL measures the luminous edge of the flame; a method that tracks the pyrolysis front measures something slightly different.

With `--out`, the imported set is kept in `data/external/` and appears in the report of that run (section 3).

### 1.2 A table of runs

A CSV laid out like NASA's BASS-II experimental table (same column names).

```
python -m gfl_analysis anomaly-table table.csv
python tools/rank_comparable_runs.py --table table.csv --out ranking.json
```

The first command lists suspect values (oxygen below 10 %, an oxygen drop above 3 points, negative or missing values). A flag says what the check saw, not what it means. The second ranks every run by how close its recorded conditions are to the reference run; a condition the table does not record counts as unknown, never as a match.

### 1.3 The images of a run

A folder with the raw camera stills of one run (Nikon NEF, as NASA publishes them) and a small JSON file with the air display readings over time (the format of `data/derived/B6_VIDEO_OVERLAY_TRANSCRIPTION` files).

```
python -m gfl_analysis measure B6 path/to/stills/ overlay.json --out measured/
```

GFL applies the frozen window rule R-W4 and writes which frames were used and why, and the rate of every constant-flow segment with its interval. This needs the `rawpy` package. Other image formats and video are not supported yet.

## 2. Take results out

| What | Format | Where |
|---|---|---|
| One run, complete | JSON | `python -m gfl_analysis report B6` writes `reports/B6_report.json` |
| One run, as a table | CSV, one row per constant-flow segment: flow, time window, frames, rate, interval, regime | `reports/B6_report.csv`; opens in Excel or LibreOffice |
| All provenance | JSON Lines (the signed ledger) | `ledger/ledger.jsonl` |
| All provenance, standard form | W3C PROV-O, JSON-LD | `data/derived/analysis/GFL_LEDGER_PROV_O.jsonld` |
| Any chart or table of the web page | JSON | `visualization/data/`, listed on the page under Files with fingerprints |

Every exported number comes from a sealed file. To check that a file is the one GFL sealed, compare its SHA-256 fingerprint with the one shown under Files on the page.

## 3. Get a report

```
python -m gfl_analysis report B6 --out reports/
```

This writes three files: `B6_report.html`, `B6_report.json`, `B6_report.csv`. Open the HTML file in a browser; to get a PDF, use the browser's Print command and choose "Save as PDF".

The report has, in order: the run as NASA recorded it; the rate and its interval; every constant-flow segment that qualified; the uncertainty in three layers (statistical, analyst choice, physical unknowns without a bound); the comparison with thin-fuel theory; which other runs the result may inform and under what conditions; values imported from other sources; what the report does not establish; and the fingerprint and ledger entry of every file behind it.

Reports exist only for runs GFL has measured (now B6, B9, B11, B13); for another run the command says so. The four current reports are also on the web page, under Guide.

## 4. What is not possible yet

Uploading a file through the web page; importing video or image formats other than NEF; a report across several runs; PDF written directly (use the browser's Print). These are stated here so nobody looks for them.
