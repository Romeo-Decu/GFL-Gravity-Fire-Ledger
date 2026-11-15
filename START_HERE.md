# Start here

Gravity Fire Ledger (GFL), team CCTI, NASA Space Apps 2026, challenge "Flame in Freefall". Made with AI; see `docs/AI_AND_TOOLS_DISCLOSURE_v1.0.md`.

## See it in two minutes

1. Download or clone this repository.
2. Windows: double-click `START_GFL.bat`. macOS or Linux: run `./START_GFL.sh`.
3. The dashboard opens in your browser at `http://localhost:8137/visualization/gfl.html`.

It needs Python 3.10 or later and nothing else: no installation, no account, no network after the page has loaded its chart library. The page only reads; it changes nothing on your computer.

Short version: seven slides, [`docs/GFL_slides.pdf`](docs/GFL_slides.pdf).

## What to look at, in order

| Step | Where on the page | What it shows |
|---|---|---|
| 1 | First screen | The finding across NASA's 24 PSI combustion investigations, why it matters (NASA's own guide: the ground test is not conservative in microgravity), and one measured result, the spread rate of BASS-II run B6, with what its interval contains and what NASA's archive cannot tell |
| 2 | Signed ledger | Your browser re-checks every signed entry; you do not have to trust us |
| 3 | Evidence map | For seven fire-safety functions: which of NASA's 24 PSI combustion investigations give evidence, under which conditions, and between which a finding may be carried |
| 4 | Predictions | Four predictions sealed before the data were opened: one held, one did not, two could not be tested. All are shown |
| 5 | Analysis | Flow calibration, thin-fuel theory, regime, uncertainty in three layers, anomaly checks, computed transfer gates |
| 6 | Functions and Architecture | Every module with its state: built, partial, or specified and not built, each linked to its code and tests |
| 7 | Guide | How the question changed, the user guide, the per-run reports, and what the data cannot settle |
| 8 | How we tried to break GFL | Six attempts to find our own errors, including the ones that went against us |

## Check it yourself

```
python -m pip install -e .                                   # once
python -m pytest -q tests                                    # software tests
python -m gfl_ledger verify --allow-missing                  # ledger: hashes, chain, signatures
python tools/rebuild_all.py                                  # rebuild the results and compare with the sealed fingerprints
```

NASA's raw files are not in the repository (only their fingerprints are). `tools/psi25_fetch.py` downloads them from NASA's PSI repository; with them, `python tools/rebuild_all.py --raw <folder>` re-measures the runs from the raw images.

## Where things are

| Folder | Content |
|---|---|
| `visualization/` | The dashboard and the data it shows |
| `src/` | Platform code: ledger, analysis modules, evidence map, transfer engine, MCP server |
| `tools/` | Scripts that build every result from its inputs |
| `tests/` | Automated tests |
| `ledger/` | The signed ledger |
| `data/` | Manifests, fingerprints and derived results; no raw NASA bytes |
| `docs/` | Methods, protocols fixed before the runs, the register of decisions, results, issues and failures |

## What GFL is not

Not a fire-prediction or safety-certification tool. It measures luminous-edge spread rates from public images, one flight per condition, and says where the evidence stops. It is not affiliated with or endorsed by NASA.
