# Finite-sample three-outcome rule

Status: **[theory, draft]**. Not owner-reviewed and not a completed G2 result.

Let `gamma` be the signed downstream decision gap, let `m >= 0` be the
prespecified harmless margin, and let `[L, U]` be a confidence interval with
uniform coverage at least `1 - alpha_c` over the model under study.

The rule reports harmless if `L >= m`, harmful if `U < 0`, and inconclusive
otherwise.

## Error-control argument

If `gamma < m` but the rule reports harmless, then `L > gamma`, so the
confidence interval failed to cover the truth. Therefore
`P_gamma(harmless) <= alpha_c`. Likewise, if `gamma >= 0` but the rule reports
harmful, then `U < gamma`, which also implies noncoverage, so
`P_gamma(harmful) <= alpha_c`.

The guarantee inherits every condition required for uniform interval coverage.
A pointwise, asymptotic, or empirically calibrated interval is not silently
promoted to this guarantee.

## Four-phase input interval

`src/estimate.py` applies a two-sided Hoeffding inequality to each of four
binomial signed means, uses a union bound, encloses the resulting `(X, Y)`
rectangle by a Euclidean ball, and projects that ball onto the circle. If the
ball contains the origin, the phase interval is the full circle.

This phase interval is one input toward a gamma interval; it is not by itself
an end-to-end decision certificate.

## Conservative error-box projection

For the MaxCut observable `C`, `||C||` is at most the number of graph edges.
For a parameter entering a unitary as `exp(-i x P/2)` with `||P|| = 1`, the
absolute derivative of one candidate expectation is at most `||C||`. The gap
of two candidates is consequently `2||C||`-Lipschitz in each error angle.

`gamma_interval_from_error_box` applies this bound to a simultaneous box for
all `epsilon`, local-left, and local-right angles. The projection is globally
valid under the exact model but deliberately loose. Its confidence is only as
valid as the simultaneous input box; independent marginal intervals cannot be
passed in without a valid multiplicity adjustment.
