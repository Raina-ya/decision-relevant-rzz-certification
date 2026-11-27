# OD11 - Model-diagnostic policy

- Date: 2026-11-27
- Decision: if any locked primary model diagnostic is triggered, the primary
  certification output is forced to `inconclusive (model-inadequate)` and the
  triggering diagnostic is reported.
- If no diagnostic triggers but at least one is statistically inconclusive,
  the primary certification output remains inconclusive.
- "Not triggered" means the model was not rejected at the prespecified
  threshold; it is not evidence that the model is true.
- Status: development decision. It becomes binding only if included in a later
  approved freeze manifest.

