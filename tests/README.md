# FiF software tests

Run from the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests verify deterministic software behavior against the declared v0.1 contracts and the current PMMA-100 evidence-gate configuration. They do not validate combustion physics, NASA source data, or scientific transferability.
