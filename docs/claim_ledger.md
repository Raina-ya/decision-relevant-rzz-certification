# Claim ledger

Status: unlocked development ledger. A claim may appear in a draft only at or
below the evidence level recorded here. Gate passage requires a separate audit.

| ID | Draft claim | Evidence label | Authoritative evidence | Current boundary |
|---|---|---|---|---|
| C-M0 | Every diagonal two-qubit coherent unitary, modulo global phase, has a ZI/IZ/ZZ representation | `[theory, draft]` | `theory/identifiability.md`; `tests/test_simulate.py` | excludes non-diagonal, leakage, non-Markovian and contextual error |
| C-ID | Control-state differencing identifies epsilon; matched delay and role swap separate local phases under M0 | `[theory, draft]` + `[exact]` checks | `theory/identifiability.md`; `tests/test_model.py` | fixed angle; assumes the stated probe law and unambiguous branches |
| C-RULE | A uniformly covering gamma interval yields directional false-claim probability at most alpha | `[theory, draft]` | `theory/three_outcome_rule.md`; `src/certify.py`; `tests/test_certify.py` | inherits all interval/model assumptions; says nothing about inconclusive probability |
| C-LOWER | Every named harmless/unsafe Bernoulli pair obeys the two-point Bretagnolle-Huber necessary sample bound | `[theory, draft]` | `theory/decision_cost_lower_bound.md`; `analysis/power/power.py`; `tests/test_power.py` | necessary, pair-specific, iid; not a matching N-star characterization |
| C-C7 | Equal average gate fidelity can coexist with opposite downstream decisions on named development instances | `[exact, development]` | `theory/average_metric_insufficiency.md`; `analysis/tolerance/average_metric_development.json`; `tests/test_average_metric.py` | named 3q/4q and sign-sensitive witnesses; not a universal hardware claim |
| C-G25 | The implemented diagnostics control false triggers conservatively under the named M0 simulation | `[sim, development]` | `analysis/diagnostics/development_calibration.json`; `development_calibration.md` | 2,000 trials/scenario; visibility power is weak for small curvature; not independently audited |
| C-G3 | The one-edge two-angle certificate becomes informative between 2,000 and 4,000 shots/phase for named alternatives | `[sim, development]` | `analysis/simulation/g3_development_grid.json`; `analysis/power/g3_development_report.md` | unlocked instance; shared truth across angles; excludes diagnostics, drift and overhead |
| C-G0 | Fractional RZZ was exposed and all submitted HW-P2 circuits passed stored ISA checks on `ibm_marrakesh` | `[hardware-locked, exploratory pilot HW-P2]` | `results/hw_p2/HW-P2_report.md`; raw HW-P2 blocks | one backend snapshot and selected pairs; not formal G0 closure |
| C-HWP2 | All three prespecified HW-P2 pilot certificates were inconclusive because model inadequacy triggered | `[hardware-locked, exploratory pilot HW-P2]` | `results/hw_p2/HW-P2_report.md`; `results/hw_p2/certificates_raw.json` | exploratory, with a result-informed T1 amendment disclosed separately |
| C-NOVEL | The combined decision-induced, finite-sample, native-fractional-RZZ contribution remains a candidate gap | `[literature, preliminary]` | `docs/literature/gap_map.md`; `novelty_memo.md` | G1 open; no definitive novelty claim allowed |

## Prohibited upgrades

- Do not rewrite exploratory HW-P2 evidence as confirmatory G5 evidence.
- Do not rewrite a non-triggered diagnostic as model validation.
- Do not report Monte Carlo coverage as a theorem or hardware frequency.
- Do not call the development instances, thresholds or budgets prespecified
  beyond their named development/pilot scope.
- Do not claim G1, G2, G2.5 or G3 passed without a separate gate record.
