# G3 prospective power - one-edge development grid

Evidence label: **[sim, development]**. Status: **G3 not evaluated / not
passed**.

## Scope and design

The grid uses the unlocked `path-2q-sign` instance because it contains
harmless, harmful and true gray-zone regimes within a single-edge model. The
two decision angles receive independent M0 confidence boxes; the total
`alpha=0.05` is split equally between them and then over six slopes, five k
values and the four-phase means.

Each cell contains 1,000 seeded trials. Visibility is 0.85, readout scale 0.94
and readout offset -0.03. The simulated truth uses the same residual at both
angles, but the estimator does not assume a shared confidence box. Results use
the conservative per-candidate Lipschitz projection.

## Prospective classification rates

`H0` is harmless, `H1` harmful and `?` inconclusive. Parenthesized values are
95% Wilson Monte Carlo intervals for the correct non-inconclusive verdict.

| epsilon | True class | shots/phase | H0 | H1 | ? | Linear QPU s |
|---:|---|---:|---:|---:|---:|---:|
| -0.40 | harmful | 500 | 0.000 | 0.000 | 1.000 | 33.6 |
| -0.40 | harmful | 1,000 | 0.000 | 0.000 | 1.000 | 67.2 |
| -0.40 | harmful | 2,000 | 0.000 | 0.000 | 1.000 | 134.4 |
| -0.40 | harmful | 4,000 | 0.000 | 1.000 ([0.9962, 1.000]) | 0.000 | 268.8 |
| -0.20 | gray zone | 500 | 0.000 | 0.000 | 1.000 | 33.6 |
| -0.20 | gray zone | 1,000 | 0.000 | 0.000 | 1.000 | 67.2 |
| -0.20 | gray zone | 2,000 | 0.000 | 0.000 | 1.000 | 134.4 |
| -0.20 | gray zone | 4,000 | 0.000 | 0.000 | 1.000 | 268.8 |
| 0.00 | harmless | 500 | 0.000 | 0.000 | 1.000 | 33.6 |
| 0.00 | harmless | 1,000 | 0.000 | 0.000 | 1.000 | 67.2 |
| 0.00 | harmless | 2,000 | 0.000 | 0.000 | 1.000 | 134.4 |
| 0.00 | harmless | 4,000 | 0.951 ([0.9358, 0.9627]) | 0.000 | 0.049 | 268.8 |
| 0.10 | harmless | 500 | 0.000 | 0.000 | 1.000 | 33.6 |
| 0.10 | harmless | 1,000 | 0.000 | 0.000 | 1.000 | 67.2 |
| 0.10 | harmless | 2,000 | 1.000 ([0.9962, 1.000]) | 0.000 | 0.000 | 134.4 |
| 0.10 | harmless | 4,000 | 1.000 ([0.9962, 1.000]) | 0.000 | 0.000 | 268.8 |

All cells had 100% interval availability and 100% observed joint M0 coverage.
The 95% Wilson interval for 1,000/1,000 coverage is [0.9962, 1.000]. No false
harmless or false harmful verdict occurred; the corresponding zero-event
upper bound is 0.00383 per cell. These are Monte Carlo bounds under the named
data-generating model, not hardware guarantees.

## Interpretation

The conservative method has a sharp cost transition. At the ideal residual,
4,000 shots per phase are needed for approximately 95% harmless power, while
the more separated harmless alternative reaches 100% observed power at 2,000.
The harmful alternative also needs 4,000. The genuine gray-zone alternative
correctly remains inconclusive at every tested budget.

The linear QPU estimate uses the HW-P2 measured value 0.28 ms/shot and counts
240 probe circuits per instance: two angles, six slopes, five k values and
four phases. It excludes diagnostic circuits, job overhead, queue time and
depth dependence.

## Limitations blocking G3

- The instance and alternatives are unlocked development choices.
- The truth is shared across the two angles; no cross-angle model is used by
  the estimator, but angle-dependent alternatives still need simulation.
- The grid covers one edge only. Multi-edge alpha allocation and heterogeneous
  residuals are absent.
- Diagnostic costs and diagnostic-triggered model rejection are not integrated.
- The Lipschitz projection is valid but may be substantially conservative.
- No independent mathematical or simulation audit has occurred.

Consequently this grid narrows the plausible budget range but does not support
a G3 pass/fail decision or a G4 freeze.
