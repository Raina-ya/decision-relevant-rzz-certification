# decision-relevant-rzz-certification

Thesis Chapter 4: fixed-budget certification of whether the coherent residual
of IBM Heron's native fractional `RZZ(theta)` gate is harmless, harmful, or
inconclusive for a prespecified downstream decision.

## Status

**Unlocked development with exploratory hardware evidence.** HW-P2 was run on
`ibm_marrakesh` under a separate owner-approved pilot lock. Its outputs are
labelled `[hardware-locked, exploratory pilot HW-P2]`; they are not a G5
confirmatory result. No G4 protocol has been frozen or externally timestamped,
and nothing is preregistered. HW-P3 was also completed under a separate
exploratory pilot lock; neither pilot is confirmatory.

## Why this question

Fractional gates cannot be Pauli-twirled, and IBM reports an angle-averaged
RZZ error. Averaged and twirled metrics discard exactly the coherent,
sign-carrying part of the error. `theory/average_metric_insufficiency.md`
shows exact cases where two residuals with identical average gate fidelity
lead to opposite decisions.

## What is implemented

| Area | Files | State |
|---|---|---|
| Diagonal model M0, probes, four-phase cycling | `src/model.py`, `src/probes.py`, `src/circuits.py` | exact checks; HW-P2 circuits passed ISA checks on the pilot backend |
| Finite-sample intervals, unwrapping, verdict rule | `src/estimate.py`, `src/certify.py` | finite-sample sets and development alpha allocations tested |
| Exact decision functional, tolerance inner sets | `src/decision.py`, `analysis/tolerance/` | development family (unlocked) |
| Average-metric insufficiency (C7) | `analysis/tolerance/average_metric.py` | exact witnesses |
| Model diagnostics | `src/diagnostics.py`, `analysis/diagnostics/` | development calibration complete; G2.5 not evaluated |
| Power bounds, ADEMP pipeline | `analysis/power/`, `analysis/simulation/` | one-edge two-angle grid complete; G3 not evaluated |
| Preflight, approval guard, pilot runners | `hardware/` | HW-P2 and HW-P3 exploratory pilots completed |
| Exploratory hardware evidence | `results/hw_p2/`, `results/hw_p3/` | model limitations disclosed; not confirmatory |
| Literature (142 sources), gap map | `docs/literature/` | G1 open; 19 papers read at relevant-section level or deeper |
| Claim ledger and manuscript | `docs/claim_ledger.md`, `paper/` | unlocked source draft; not TeX-compiled |

## Run checks

```powershell
python -m unittest discover -s tests -v
python tools/build_bib.py   # after editing docs/literature/library.csv
```

All contributors must follow [AGENTS.md](AGENTS.md). The working plan is
[plan/ch4_plan_v1.md](plan/ch4_plan_v1.md); the research-gap map is
[docs/literature/gap_map.md](docs/literature/gap_map.md). The current gate and
work-package audit is [docs/audits/2026-11-27-completion-audit.md](docs/audits/2026-11-27-completion-audit.md).

## Author

Zhen-Jun Liu
