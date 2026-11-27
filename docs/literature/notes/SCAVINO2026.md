# SCAVINO2026 reading note

Reading status: relevant sections read. Reviewed the prior-work positioning,
gap-law sufficiency result, marginal-accuracy counterexamples, covariance
propagation, Gaussian decision rates, decision-aware design, certification
limits, finite-shot QAOA-MaxCut controls, and stated limitations. Detailed QEM
implementation appendices were not read line by line.

- Question: At a fixed acquisition cost, how do quantum-error-mitigation bias,
  covariance, and sampling overhead affect candidate-selection decisions?
- Decision representation: shift-invariant finite-candidate rules factor
  through contrasts. The law of residual candidate gaps, rather than marginal
  MSE alone, determines selection risk.
- Cost and limits: mitigation maps and shared records induce a gap covariance.
  In a Gaussian working model, margins and covariance give finite-budget risk
  and large-budget rates. A converse section connects alternative instances
  to KL and local Fisher geometry for fixed primitive measurements.
- QAOA evidence: finite-shot QAOA-MaxCut controls compare raw, CDR, and PEC
  estimators at equal evaluation or total acquisition cost. They demonstrate
  that lower MSE can coexist with unchanged or higher selection failure.
- Evidence boundary: several comparisons are retrospective or oracle-assisted;
  Gaussian rates require separate deviation justification for the underlying
  discrete shot model. The target is QEM selection, not inference on a native
  gate's coherent residual.
- Novelty implication: C5 is substantially overlapped at the conceptual and
  experimental-design level. C3 is also narrowed because decision margins,
  covariance, KL/Fisher geometry, and acquisition cost are already joined.
  A Ch4 contribution would have to be the native-RZZ probe-to-error-set link,
  exact finite-sample coverage, explicit model diagnostics, and a theorem or
  empirical result specific to that link; an equal-shot decision-risk curve
  alone is not new.
