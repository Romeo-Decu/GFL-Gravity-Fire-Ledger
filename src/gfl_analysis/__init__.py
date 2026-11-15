"""GFL analysis modules (platform layer over the frozen research scripts).

flow     A0  air display -> opposing-flow speed (NASA fan calibration workbook)
uq       A5  three-layer uncertainty: statistical, analyst choice, physical unknowns
cram1    A3  thermal-regime theory for thin fuels (de Ris / Delichatsios / EST) and thin-thick check
regime   A4  CRAM-2 regime evidence: Damkoehler and radiation numbers, thermal / kinetic / radiative
anomaly  A6  data anomaly detector (tables, frames, overlay)
gates    A2  transfer gates computed from measured and recorded values
measure  A1  measurement through the frozen window rule R-W4
prov     A7  W3C PROV-O export of the ledger

Every number a module uses carries its source; a value without one is labelled approximate.
Nothing here validates combustion physics: it states what the data and the cited theory allow.
"""
__version__ = "0.1.0"
