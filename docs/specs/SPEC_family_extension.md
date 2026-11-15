# Extension to the other NASA combustion families

**Status:** designed. BASS-II is acquired and measured; the other families are identified, not inventoried.

## What we want
Bring SoFIE, SAFFIRE, SAME / SAME-R, FLEX / FLEX-2, ACME / BRE and SPICE into GFL with the same discipline as BASS-II:
- collection identity;
- a manifest with hashes;
- a run-level table;
- reconciliation within each experiment;
- only then, comparison across experiments.

## The rule that matters
Families are **not pooled** because they all concern combustion in microgravity. They differ in:
- fuel phase (solid, liquid droplet, gas);
- apparatus and scale (duct, Cygnus vehicle);
- boundary conditions;
- observable (spread rate, extinction, smoke, droplet burning).

A finding crosses families only through the transfer engine, with the blocking dimension named when it cannot.

## Order (work priority, not scientific ranking)
1. SoFIE: second solid-fuel family.
2. SAFFIRE: scale contrast.
3. SAME / SAME-R: smoke and aerosols.
4. FLEX / FLEX-2: droplets.
5. ACME / BRE: gas flames and the burning-rate emulator.
6. SPICE: scope to be established.

## Per family, the same steps
1. Locate the collection (PSI ID, DOI, version).
2. Build the manifest with SHA-256.
3. Audit the run table: preserve native identifiers; never correct, only flag.
4. Acquire primary files for a bounded case and seal them.
5. Apply the measurement and comparability rules; record failures.

## Blocking conditions
Data custody for some families (for example the SoFIE data held at SDSU); file sizes; licences per collection.
