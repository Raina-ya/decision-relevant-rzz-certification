# G2.5 model-diagnostic report - draft

Status: **not evaluated / not passed**.

Implemented finite-sample decision logic:

- Z conservation uses a one-sided Hoeffding lower bound for the control-qubit
  flip rate.
- k-linearity asks whether one unwrapped per-gate phase is compatible with all
  circular confidence intervals. An ambiguous branch is inconclusive.
- visibility decay asks whether a line in `(k, log V)` intersects every input
  interval. Intervals touching zero are inconclusive rather than coerced.
- OD11 maps any triggered primary diagnostic to
  `inconclusive (model-inadequate)`.

Still required before G2.5 can be evaluated:

- multiplicity allocation `alpha_diag` across all diagnostics;
- a finite-sample construction of visibility intervals from four-phase data;
- simulated false-trigger and detection-power tables with Monte Carlo error;
- fixed diagnostic thresholds and decision instances;
- an independent WP10 audit.

