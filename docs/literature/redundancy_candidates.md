# Literature consolidation candidates

Status: review aid only, 2026-11-27. No library or BibTeX entry has been
removed. A source is a removal candidate only for the Chapter 4 working
library; it may still be useful elsewhere in the thesis.

## Decision rule

Retain a source when it supports a specific premise, method, counterexample,
statistical guarantee, hardware constraint or novelty comparison. Flag a
source when it is abstract/bibliographic-only, has no unique Ch4 claim in the
current gap map, and is covered more directly by another retained source.
Recency alone is not a reason to retain or remove a paper.

## Keep as the minimum benchmarking backbone

These entries prevent over-pruning of the comparison literature:

- `KNILL2007`, `MAGESAN2010`: foundational randomized benchmarking.
- `WALLMAN2015UNITARITY`: coherent-noise quantity directly relevant to the
  average-metric limitation.
- `WALLMAN2017`: gate-dependent-noise limitation.
- `ERHARD2019`, `POLLORENO2023`: modern cycle/direct RB representatives.
- `KUENG2016`, `SANDERS2016`: average-fidelity versus worst-case error.
- `PROCTOR2022CAP`, `MERKEL2025`: application-level/proxy-metric comparison.

## High-confidence consolidation candidates

These currently have no unique role in the Ch4 claim map. They should be the
first group considered for removal unless a later full-text reading finds a
specific needed result.

| ID | Why it appears redundant | Retain if |
|---|---|---|
| `GRANADE2016` | inference-software paper; no current method uses QInfer | the implementation or methods discussion adopts QInfer |
| `MUHONEN2014` | platform-specific single-atom RB example | cross-platform RB evidence becomes a stated claim |
| `HOTHEM2024` | mid-circuit-measurement benchmarking is outside the protocol | dynamic/mid-circuit measurements enter the design |
| `WYSOCKI2026` | logical GST is outside native physical fractional RZZ scope | the chapter makes a logical-gate comparison |
| `BARBERARODRIGUEZ2026` | direct fidelity-estimation grouping has no current role | measurement grouping is used in the estimator |
| `LI2026QST` | quantum-program output-dominance testing is remote from the gate certificate | software-testing baselines enter the related-work comparison |
| `VIKSTAL2023` | cat-qubit QAOA hardware is not comparable to IBM Heron RZZ | hardware-modality generalization is discussed |
| `BRAVYI2024` | shallow-circuit identity checking does not support a current claim | identity testing becomes a formal baseline |

## RB-family compression candidates

The library contains a large RB survey cluster. The following entries overlap
the retained backbone and are currently only abstract- or bibliographic-level:

`WALLMAN2014`, `HELSEN2019`, `HARPER2019`, `HELSEN2021`, `HARPER2016`,
`FIGUEROAROMERO2021`, `FIGUEROAROMERO2022`, `FLAMMIA2021`, `KONG2021`,
`SHELDON2015`, `ONORATI2018`, `HASHAGEN2018`, `COMBES2017`, `CROSS2015`,
`WALLMAN2014LEAKAGE`, `GRANADE2014`, `FOGARTY2015`, `WOOD2017`, `DIRKSE2018`,
`EPSTEIN2013`, `BALL2015`, `PROCTOR2021` and `PROCTOR2018`.

Do not remove this block mechanically. Retain an entry if the final text cites
its unique condition: confidence intervals, few-sample behavior,
non-Markovianity, leakage, unitarity, gate dependence, mirror circuits or
non-Clifford benchmarking. Otherwise one representative per condition is
enough for the working library.

## QAOA-background compression candidates

- `CROOKS2018` and `ZHOU2018` overlap as general MaxCut-QAOA mechanism and
  implementation background. Retain at most the one actually cited for the
  chosen statement, in addition to foundational `FARHI2014`.
- `MARSHALL2020`, `XUE2021`, `STILCKFRANCA2021` and `WANG2020NIBP` cover
  different noise effects and are not strict duplicates. If the chapter only
  needs the narrow coherent-control-sensitivity claim, prioritize
  `QUIROZ2021`, `DONG2019` and `ALAM2019`; move the others to thesis-wide
  background rather than deleting them outright.
- `BLEKOS2024` is useful as a review but should not replace primary sources.

## Sources to read before any removal decision

Do not prune these merely because they are currently abstract-only:

- `KIMMEL2015`, `RUSSO2020`: RPE guarantees and consistency diagnostics.
- `KUENG2016`, `SANDERS2016`, `CHO2026`: coherent/worst-case error versus
  average fidelity.
- `SMITH2021`, `VANDENBERG2022TREX`: readout treatment used by the protocol.
- `HOWARD2021`, `WAUDBYSMITH2024`, `HOEFFDING1963`: finite-sample guarantees.
- `SCHUIRMANN1987`, `BERGER1996`, `EGGERS2026`: equivalence/classification
  logic.
- `PROCTOR2020DRIFT`, `DASGUPTA2021`, `DASGUPTA2024`: drift and replication.
- `MILAZZO2023`, `BARRON2024`: functional testing and noisy-sample bounds.

## Suggested adjudication fields

For each proposed removal, record: `decision`, `unique_claim`,
`replacement_source`, `full_text_checked`, and `reason`. Deletion should update
`library.csv`, `topic_map.csv`, reading notes, prose citations and the generated
`references.bib` in one reviewed change.
