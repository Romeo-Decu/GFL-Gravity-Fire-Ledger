# FiF software tests

Run from the repository root:

```bash
python -m unittest discover -s tests -v
```

Install the local package to use the command-line interface from the repository root:

```bash
python -m pip install -e .
```

Run the bounded PMMA-100 examples:

```bash
python -m fif_transfer --ruleset configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json --request examples/PMMA100_DOCUMENTARY_SUMMARY_REQUEST_v0.1.json
python -m fif_transfer --ruleset configs/PMMA100_FLAME_SPREAD_RULESET_v0.1.json --request examples/PMMA100_QUANTITATIVE_TRANSFER_REQUEST_v0.1.json
```

The tests verify deterministic software behavior against the declared v0.1 contracts and the current PMMA-100 evidence-gate configuration. They do not validate combustion physics, NASA source data, or scientific transferability.
