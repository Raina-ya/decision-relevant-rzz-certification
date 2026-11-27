# G2.5 model-diagnostic report - draft

Status: **not evaluated / not passed**.

Implemented finite-sample decision logic:

- Z conservation uses a one-sided Hoeffding lower bound for the control-qubit
  flip rate.
- k-linearity asks whether one unwrapped per-gate phase is compatible with all
  circular confidence intervals. An ambiguous branch is inconclusive.
- visibility decay asks whether a line in `(k, log V)` intersects every input
  contrast-amplitude interval. The amplitude is obtained directly from the
  same four-phase confidence rectangle and equals readout scale times
  visibility under M0. Intervals touching zero are inconclusive rather than
  coerced.
- OD11 maps any triggered primary diagnostic to
  `inconclusive (model-inadequate)`.

Development calibration is recorded in `development_calibration.md` and
`development_calibration.json`. It uses a Bonferroni allocation of
`alpha_diag=0.05` over the three diagnostic families and then over the four
`k` values for the joint phase/amplitude confidence sets. This closes the
implementation gaps for alpha allocation and finite-sample amplitude
intervals, but does not lock those choices.

Still required before G2.5 can be evaluated:

- owner-reviewed final diagnostic thresholds, instances and shot allocation;
- a sensitivity grid connecting the diagnostics to final G3 budgets rather
  than the development-only alternatives;
- an independent WP10 audit.
