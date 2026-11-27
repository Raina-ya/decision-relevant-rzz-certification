# OD1 and OD2 - Development decision family and margin

- Date: 2026-11-27
- Status: unlocked development decision; not a protocol freeze.
- OD1: use 2-, 3-, and 4-qubit path graphs as tier-A heavy-hex subgraphs. For
  each graph, compare two p=1 QAOA candidates. Every edge in a candidate uses
  the same RZZ angle, so each instance uses exactly two decision angles
  (`J = 2`). Candidates come from the fixed seeded rejection rule in
  `analysis/tolerance/instances.py`; an ideal absolute gap below 0.15 is
  rejected before any hardware data exist.
- OD2: the decision is the sign of the exact expected MaxCut gap. The harmless
  margin is one half of the instance's exact ideal absolute gap.
- Rationale: this is the smallest family spanning 2-4 qubits while avoiding
  routing and preserving the v1 decision-angle QPU budget.
- Boundary: G1-G3 or owner review may replace this development family before
  any lock. Existing development simulations must then be labeled obsolete,
  not silently reused.

