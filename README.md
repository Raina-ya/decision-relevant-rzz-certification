# decision-relevant-rzz-certification

Planning and analysis code for thesis Chapter 4: fixed-budget certification of
whether native fractional `RZZ(theta)` gate errors are harmless, harmful, or
inconclusive for a prespecified downstream decision.

## Status

This repository is an **unlocked implementation draft**. No hardware job has
been submitted, no protocol has been frozen, and nothing is preregistered.
Current results are analytic or exact-computation development checks only.

## Current scope

- Typed probe and result interfaces.
- Exact analytic model for the diagonal coherent-error model `M0`.
- Four-phase readout-cycle calculations.
- Initial exact-recovery tests supporting draft lemmas L0-L2.

Qiskit ISA generation, fake-backend checks, statistical confidence bounds,
power analysis, and hardware preflight remain future gated work.

## Run checks

```powershell
python -m unittest discover -s tests -v
```

All contributors must follow [AGENTS.md](AGENTS.md). The working plan baseline
is [plan/ch4_plan_v1.md](plan/ch4_plan_v1.md).

## Author

Zhen-Jun Liu

