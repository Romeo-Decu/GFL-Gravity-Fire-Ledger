# ECLSS decision support

**Status:** research direction (DEC-010). Not built. GFL is not an ECLSS controller.

## Problem
Give environmental-control engineers an evidence view: for the current cabin state (oxygen, pressure, ventilation, materials present), which experiments are relevant and how far their findings transfer. The output is decision support with stated limits, never an automatic action.

## Design
- **Input:** cabin parameters from telemetry or from a planning scenario.
- **Engine:** the comparability engine and the experiment memory produce the evidence view.
- **Output:** every recommendation-like statement cites records and states what is not covered.

## Required data
Families beyond BASS-II; materials catalogue; validated regime gates.

## Validation
Review with ECLSS domain experts; refusal tests for out-of-domain states.

## Blocking conditions
Access to operational telemetry formats; family inventories; certification boundaries.
