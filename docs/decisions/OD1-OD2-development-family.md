# OD1 and OD2 - Development decision family and margin

- Date: 2026-11-27
- Status: unlocked development decision; not a protocol freeze.
- OD1: the hardware-primary decision is the 2-qubit, one-edge path, matching
  the one-pair probe design and budget. The generated 3- and 4-qubit paths are
  method extensions supported only by `[exact]` and `[sim]` evidence. They
  cannot receive a hardware certificate unless every physical pair is probed
  and the multiplicity and QPU budgets are expanded first. For each graph,
  compare two p=1 QAOA candidates. Every edge in a candidate uses the same RZZ
  angle, so each instance uses exactly two decision angles (`J = 2`).
  Candidates come from the fixed seeded rejection rule in
  `analysis/tolerance/instances.py`; an ideal absolute gap below 0.15 is
  rejected before any hardware data exist.
- OD2: the decision is the sign of the exact expected MaxCut gap. The harmless
  margin is one half of the instance's exact ideal absolute gap.
- Rationale: this preserves the v1 one-pair hardware scope. Treating a single
  pair's characterization as evidence for unmeasured pairs would be an invalid
  sensor-target transfer assumption. The extension family remains useful for
  scaling analysis without making that transfer.
- Boundary: G1-G3 or owner review may replace this development family before
  any lock. Existing development simulations must then be labeled obsolete,
  not silently reused.
