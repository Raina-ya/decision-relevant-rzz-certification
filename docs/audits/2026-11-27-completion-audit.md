# Project completion audit - 2026-11-27

Scope: repository evidence at commit `72f5c86`, plus the untracked HW-P3
selection artifact observed during the audit. This is a development audit, not
an independent scientific review or a gate approval.

## Executive finding

The executable research infrastructure and exploratory HW-P2 pilot are
substantial. The confirmatory chapter is not complete: G1-G3 remain open, G4
has not occurred, and the exploratory pilots do not count as G5-G6.

## Gate ledger

| Gate | State | Evidence boundary | Required next evidence |
|---|---|---|---|
| G0 | exploratory evidence obtained; formal closure absent | HW-P2 exposed fractional RZZ, passed ISA checks and recorded timing on `ibm_marrakesh` | independent audit and an explicit gate decision |
| G1 | open | 142 sources; 19 papers read at relevant-section level or deeper; novelty memo remains preliminary | finish the logged search families and forward-citation passes; adjudicate the gap map |
| G2 | partial | L0-L2 and C7 drafts have exact checks | complete the intended lemma chain and independent mathematical review |
| G2.5 | not evaluated | diagnostic logic is tested; HW-P2 triggered model inadequacy | prespecify multiplicity and thresholds; run false-trigger/power calibration |
| G3 | not evaluated | formulas and ADEMP plumbing tests exist | freeze development inputs and run the prospective scenario grid |
| G4 | not started | no freeze manifest, external timestamp or preregistration | prohibited until the prerequisite gates pass |
| G5 | not started | HW-P2 is explicitly exploratory and yielded model-inadequate/inconclusive certificates | valid G4 approval followed by the one-time confirmatory run |
| G6 | not started | no confirmatory result exists to replicate | independent replication after G5 |

## Work-package ledger

| WP | State | Audit note |
|---|---|---|
| WP0 | development acceptance met | repository skeleton and test framework operate |
| WP1 | partial | library scale is adequate; reading depth and novelty review are not |
| WP2 | partial | L0-L2 tested; later theory and independent audit open |
| WP3 | partial | analytic and semantic circuits exist; local Qiskit tests are dependency-skipped |
| WP4 | development scope met | exact decision family and tolerance tools tested; inputs remain unlocked |
| WP5 | partial | finite-sample chain exists; full alpha allocation and coverage study open |
| WP6 | partial | power and ADEMP code tested; scientific scenario study open |
| WP7 | exploratory pilot stage complete | HW-P2 platform evidence exists; no confirmatory claim |
| WP8 | started | HW-P3 approval/protocol and pair selection exist; no result report |
| WP9 | no acceptance handoff | no auditable WP-level completion record |
| WP10 | no acceptance handoff | independent diagnostic audit remains explicitly required |
| WP11 | no acceptance handoff | no auditable WP-level completion record |
| WP12 | partial | diagnostic policy and logic tested; calibration open |

## Verification snapshot

- `python -m unittest discover -s tests -v`: 90 run, 0 failures, 5 skipped.
- The five skips require `qiskit` and/or `qiskit-ibm-runtime`; they are not
  counted as Qiskit-path verification.
- BibTeX/library integrity is covered by the passing literature tests. This
  proves structural consistency, not correctness of every scientific claim.
- The worktree contained untracked `results/hw_p3/matching.json` and an empty
  `results/hw_p3/A/` directory during the audit. Neither is hardware-result
  evidence.

## Highest-priority closure sequence

1. Complete G1 reading and forward-citation review; adjudicate contribution
   claims before investing in confirmatory design.
2. Repair the M0 inadequacy exposed by HW-P2 and calibrate G2.5 diagnostics.
3. Finish the G2 theory audit and G3 prospective scenario study.
4. Re-audit all claims and only then consider G4 freeze and external timestamp.

Negative and inconclusive evidence is retained. Nothing in this audit upgrades
HW-P2 or HW-P3 to confirmatory status.
