# CAMPOS2021 reading note

Reading status: relevant sections read. Reviewed the layerwise-QAOA definition,
saturation definition and numerical result, necessary-condition derivation,
coherent phase-noise experiment, discussion, and the relevant appendix example.

- Question: Why does greedy layerwise QAOA training stop improving after a
  finite depth, and can a perturbation move the state away from the saturated
  family?
- Model and objective: a target computational-basis state, standard X mixer,
  and target-state overlap optimized one newly added layer at a time. This is
  not the graph MaxCut objective used by Ch4.
- Finding: the reported numerical experiments observe saturation at depth
  equal to the qubit count for the studied setup. The paper derives necessary
  saturation conditions and exhibits non-trainable state families.
- Noise experiment: independently sampled local coherent phase rotations are
  introduced probabilistically during training. Some numerical trials obtain
  higher overlap because the perturbation breaks the saturation condition.
- Evidence boundary: this is simulation evidence for a particular greedy
  training pathology. It is not a confidence-qualified robustness result and
  does not show that coherent phase error is generally beneficial.
- Relation to Ch4: it confirms that coherent phase perturbations can alter a
  QAOA training outcome, but it neither models an RZZ overrotation on a fixed
  MaxCut instance nor certifies preservation of a downstream decision. It is
  adjacent evidence, not direct overlap with the proposed decision-functional
  certificate.
