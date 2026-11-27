# Identifiability lemmas L0-L2

Status: **[theory, draft]**. These statements are not owner-reviewed.

## L0 - Completeness of the diagonal coherent model

After quotienting out global phase, a two-qubit diagonal unitary has three
independent phases. The commuting traceless diagonal Pauli products `ZI`, `IZ`,
and `ZZ` are linearly independent and span this three-dimensional Lie algebra.
Therefore every diagonal two-qubit coherent unitary error has an M0
representation. This does not cover non-diagonal, non-Markovian, leakage, or
context-dependent error.

## L1 - Reduced target dynamics

For control eigenvalue `z_c = (-1)^c`, restricting

`exp(-i(Theta ZZ + A ZI + B IZ)/2)`

to the control state yields a target rotation with angle `z_c Theta + A` when
qubit 1 is the target. The term acting only on the control contributes a global
phase within that restricted subspace. Swapping target and control exchanges
`A` and `B`.

## L2 - Fixed-angle identifiability

At fixed angle, differencing the two control-state phase slopes identifies
`epsilon`; averaging identifies only `a + delta_1 tau` (or
`b + delta_2 tau`). Without a matched delay control, the transformation

`(a, delta_1) -> (a + Delta, delta_1 - Delta/tau)`

leaves all probe distributions unchanged. A matched delay control separately
identifies `delta_1 tau`, making `a` identifiable. Role swapping supplies the
same result for `b`.

Exact arithmetic checks implementing these constructions are in
`tests/test_model.py`. They are development evidence, not a completed G2 audit.

## Interval branch handling

`unwrap_phase_intervals` intersects each circular observation of `k*x` with
the current linear interval for `x`. Refinement occurs only when exactly one
integer branch intersects. Zero branches are reported as inconsistent and two
or more as ambiguous. Therefore the implementation does not turn a branch
choice heuristic into evidence of identifiability.

If all circular intervals simultaneously cover their true phases and the true
slope lies in the prespecified prior, every identified output interval contains
the true slope. `recover_m0_intervals` then applies interval arithmetic to the
two control states, two roles, and matched delays. Its coverage is inherited
from the joint input event; marginal intervals require multiplicity control.
