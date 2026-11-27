# Conservative tolerance inner set

Status: **[theory, draft]**.

For a MaxCut observable `C` on `E` edges, `||C|| <= E`. If an M0 angle
parameter `x` enters one candidate unitary as `exp(-i x P/2)` with `||P||=1`,
the derivative of that candidate's expectation has magnitude at most `E`.
For the gap of two candidates, each coordinate derivative is therefore bounded
by `2E`.

Consequently,

`|gamma(e) - gamma(0)| <= 2E ||e||_1`.

If `gamma(0) >= m`, the L1 ball with radius

`r = (gamma(0)-m)/(2E)`

is contained in the tolerance region `{e: gamma(e) >= m}`. For `d` error
coordinates, the symmetric equal-width box with halfwidth `r/d` lies inside
that ball. This is the conservative inner set implemented in
`analysis/tolerance/regions.py`.

This bound is intentionally more general and looser than any Ch3 lemma whose
constant depends on a specific circuit or cost normalization. It must not be
renamed "Lemma B" until the assumptions and normalization are checked against
the authoritative Ch3 proof.

The radial-crossing routine in the same module is numerical: it samples a
direction to find the first observed bracket and then bisects it. Because
`gamma` need not be monotone along a ray, that crossing is not a proof of a
global tolerance boundary.

