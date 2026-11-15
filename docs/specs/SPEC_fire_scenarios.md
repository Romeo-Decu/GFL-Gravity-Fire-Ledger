# Fire-scenario analysis

**Status:** research direction (DEC-010). Not built. GFL is not a fire-prediction or safety-certification tool (DEC-013).

## Problem
Given a spacecraft cabin scenario (material, oxygen, pressure, ventilation), show which NASA experiments give relevant evidence, what can be transferred and what cannot. The output is an evidence map for a scenario, not a prediction of what a fire will do.

## Design
- **Scenario description:** written in the comparability vocabulary.
- **Families searched:** BASS-II, SoFIE, SAFFIRE and others, each kept separate.
- **Per scenario dimension:** the transfer engine reports supported, conditional, qualitative, not transferable or undetermined.
- **Gaps:** the gaps between evidence and scenario are listed as the main output.

## Required data
Inventories of the families beyond BASS-II, at run level. Today only BASS-II is acquired.

## Validation
- An expert review of evidence maps for known historical scenarios.
- A test that no scenario receives "directly supported" without matched evidence.

## Blocking conditions
Family inventories; scale gap between material tests and cabin fires (SAFFIRE is the bridge candidate).
