# Tolerance analysis

Status: development only. No decision family, margin, seed, or tolerance region
is locked.

`src/decision.py` provides exact p=1 MaxCut expectations for 2-4 qubit graph
instances, two prespecified candidate parameter sets, and one M0 error triple
per edge. It defines the signed decision functional `gamma(e)` without assuming
that error is affine across angles.

The current implementation intentionally does not generate instances or choose
candidates: those scientific choices must be recorded as explicit inputs before
the tolerance-region computation is treated as a result.

