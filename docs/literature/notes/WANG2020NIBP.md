# WANG2020NIBP reading note

Reading status: relevant sections read. Reviewed the main local-noise theorem,
QAOA specialization, MaxCut numerical heuristics with a realistic hardware
noise model, shot-complexity interpretation, and limitations.

- Question: Does local hardware noise impose an asymptotic trainability limit
  on layered variational algorithms?
- Model: local Pauli noise acts around circuit layers. The central theorem
  bounds gradients by a factor that decays exponentially with layer depth.
- QAOA evidence: the generic theorem is specialized to QAOA compilation, and
  MaxCut simulations show cost concentration and degraded approximation ratio
  with increasing depth under a realistic device-derived model.
- Statistical implication: resolving an exponentially suppressed gradient to
  fixed precision requires an exponentially growing number of shots. This is
  a training-cost result, not a confidence certificate for a fixed gate error.
- Limitations for Ch4: the theorem's core channel is incoherent Pauli noise,
  not a systematic coherent RZZ residual; the target is trainability rather
  than whether a prespecified pairwise decision changes.
- Novelty implication: broad claims about QAOA noise-cost scaling are not
  available to Ch4. The native coherent-error probe and fixed-instance
  decision certificate remain the narrower comparison.
