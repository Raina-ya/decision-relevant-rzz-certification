# Project completion audit - 2026-11-27

Scope: repository evidence based on commit `0794672`, plus the documented
family-wise HW-P3 T1 sensitivity analysis and status synchronization in the
audited working tree. This includes the completed HW-P2 and HW-P3 exploratory
pilots. It is an integrator development audit, not the independent WP10
scientific review required for gate approval.

## Executive finding

The executable research infrastructure and exploratory HW-P2 pilot are
substantial. The confirmatory chapter is not complete: G1-G3 remain open, G4
has not occurred, and the exploratory pilots do not count as G5-G6.

## Gate ledger

| Gate | State | Evidence boundary | Required next evidence |
|---|---|---|---|
| G0 | exploratory evidence obtained; formal closure absent | HW-P2 exposed fractional RZZ, passed ISA checks and recorded timing on `ibm_marrakesh` | independent audit and an explicit gate decision |
| G1 | open | 142 sources; 19 papers read at relevant-section level or deeper; novelty memo remains preliminary | finish the logged search families and forward-citation passes; adjudicate the gap map |
| G2 | partial | L0-L2, T1, T2 and C7 drafts exist with computational checks where applicable | optimize the full observation-law lower bound and obtain independent mathematical review |
| G2.5 | not evaluated | finite-sample diagnostics and a seeded development calibration exist; HW-P2/HW-P3 exposed model limitations | connect final thresholds and alternatives to G3 and obtain WP10 audit |
| G3 | not evaluated | formulas and a seeded one-edge two-angle grid with MC intervals exist | add multi-edge, angle-dependent and diagnostic-inclusive scenarios; resolve owner inputs |
| G4 | not started | no freeze manifest, external timestamp or preregistration | prohibited until the prerequisite gates pass |
| G5 | not started | HW-P2 is explicitly exploratory and yielded model-inadequate/inconclusive certificates | valid G4 approval followed by the one-time confirmatory run |
| G6 | not started | no confirmatory result exists to replicate | independent replication after G5 |

## Work-package ledger

| WP | State | Audit note |
|---|---|---|
| WP0 | development acceptance met | repository skeleton and test framework operate |
| WP1 | partial | library scale is adequate; reading depth and novelty review are not |
| WP2 | partial | principal identifiability, error-control and pairwise lower-bound drafts exist; full N-star optimization and independent audit open |
| WP3 | partial | analytic and semantic circuits exist; local Qiskit tests are dependency-skipped |
| WP4 | development scope met | exact decision family and tolerance tools tested; inputs remain unlocked |
| WP5 | partial | finite-sample chain exists; full alpha allocation and coverage study open |
| WP6 | partial | one-edge two-angle prospective study complete; full scenario family open |
| WP7 | exploratory pilot stage complete | HW-P2 platform evidence exists; no confirmatory claim |
| WP8 | exploratory pilot integration complete | HW-P3 approval, raw outputs and report exist; this is not G4 freeze work |
| WP9 | no acceptance handoff | no auditable WP-level completion record |
| WP10 | no acceptance handoff | independent diagnostic audit remains explicitly required |
| WP11 | partial | claim ledger and source-only development manuscript exist; scientific gates and TeX render open |
| WP12 | partial | diagnostic policy, finite-sample intervals and development calibration exist; final design/audit open |

## Verification snapshot

- `python -m unittest discover -s tests -v`: 103 run, 0 failures, 5 skipped.
- The five skips require `qiskit` and/or `qiskit-ibm-runtime`; they are not
  counted as Qiskit-path verification.
- BibTeX/library integrity is covered by the passing literature tests. This
  proves structural consistency, not correctness of every scientific claim.
- LaTeX source checks found all cited BibTeX keys, balanced braces and the
  required section order. No TeX engine was available, so compilation and
  visual inspection remain unverified.

## Highest-priority closure sequence

1. Complete G1 reading and forward-citation review; adjudicate contribution
   claims before investing in confirmatory design.
2. Repair the M0 inadequacy exposed by HW-P2 and calibrate G2.5 diagnostics.
3. Finish the G2 theory audit and G3 prospective scenario study.
4. Re-audit all claims and only then consider G4 freeze and external timestamp.

Negative and inconclusive evidence is retained. Nothing in this audit upgrades
HW-P2 or HW-P3 to confirmatory status.
