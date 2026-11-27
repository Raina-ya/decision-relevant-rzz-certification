# NOLLER2024 reading note

Reading status: relevant sections read. Reviewed introduction, definitions,
protocol, the single-qubit phase-gate certification result and sample-complexity
argument, conclusion, and the statement/proof structure of the principal
theorems. Supporting lemmata were not read line by line.

- Question: Can a classical user certify a black-box quantum gate without
  trusted SPAM, assuming only system dimension?
- Model: a target state/gate/measurement model and an unknown implementation,
  considered correct up to unitary or anti-unitary symmetry.
- Design: exact-computation tests with deterministic ideal outcomes.
- Estimand/certificate: closeness of the whole model, with average gate
  infidelity used for gates.
- Sample complexity: for the studied single-qubit pi/2 phase gate, the paper
  proves O(epsilon^-1) scaling in average gate infidelity.
- Limitations for Ch4: the detailed result is single-qubit and target-fidelity
  based. The authors describe multi-qubit extension as future/preliminary work.
  There is no downstream decision tolerance or harmless/harmful/inconclusive
  classification.
- Relation: directly narrows broad claims that Ch4 introduces finite-sample
  gate certification or certification cost analysis; it does not presently
  overlap the proposed decision-functional layer.

