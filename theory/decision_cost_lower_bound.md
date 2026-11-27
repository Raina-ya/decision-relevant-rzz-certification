# Two-point lower bound for decision certification

Status: **[theory, draft]**. Not owner-reviewed or independently audited.

## Setup

Fix two prespecified parameter points. At the harmless point `h`, the true
decision gap is at least the margin. At the unsafe point `u`, the gap is below
the margin. Let `A` be the event that a procedure reports harmless after `N`
independent records. Require

- false harmless control: `P_u(A) <= alpha_c`, and
- harmless power: `P_h(A) >= 1-beta`.

The inconclusive and harmful outputs may be combined into `A^c`; therefore the
argument applies to every three-outcome rule, regardless of how those two
outputs are separated.

## Draft theorem T2 - necessary samples for a named pair

Bretagnolle-Huber gives

`P_u(A) + P_h(A^c) >= 0.5 exp(-KL(P_h^N || P_u^N))`.

For independent identical records,
`KL(P_h^N || P_u^N) = N KL(P_h || P_u)`. Consequently, whenever
`alpha_c + beta < 1/2`, every rule meeting the two requirements must satisfy

`N >= log(1/(2(alpha_c+beta))) / KL(P_h || P_u)`.

The implementation rounds this value upward in
`analysis.power.power.two_point_required_samples`. The KL direction is part of
the theorem: harmless is the first distribution and unsafe the second.

For a Bernoulli record with probabilities `p_h` and `p_u`, the denominator is
`kl(p_h,p_u)`. If the pair induces the same record distribution, the KL is
zero and the bound is infinite. This is a concrete non-identifiability result:
no number of those records can simultaneously provide the named false-harmless
control and power for that pair.

## Relation to N-star

For a composite harmless set `H` and unsafe set `U`, any valid procedure must
obey the bound for every named pair `(h,u)`. Thus

`N-star >= sup_(h in H, u in U) log(1/(2(alpha_c+beta))) / KL(P_h || P_u)`.

This expression is only useful after the observation law and admissible pair
set are specified. The repository currently evaluates Bernoulli pairs as
development witnesses; it does not claim to have optimized the supremum over
the full phase-cycle experiment. Therefore it is a lower-bound component, not
a completed matching characterization of `N-star`.

## Boundaries and limitations

- The result assumes independent records. Drift, adaptive stopping and
  cross-circuit dependence require a different likelihood argument.
- It is a necessary bound and does not prove attainability.
- A small bound for one pair says nothing about the hardest pair.
- The result does not convert average gate fidelity into decision distance.
- The G3 Monte Carlo grid is an upper-bound construction under a named model;
  it is not yet matched to the hardest two-point lower-bound pair.
