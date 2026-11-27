# ZHANG2021 reading note

Reading status: relevant sections read. Reviewed the verification construction,
robust confidence analysis, sample-complexity discussion, CNOT and Toffoli
experiments, and stated assumptions and limitations. Proof details not needed
for the Ch4 comparison were not read line by line.

- Question: Can multi-qubit gates be verified efficiently using only local
  state preparation and measurement despite realistic gate imperfections?
- Model: repeated runs use an identical channel; the certificate is expressed
  through average gate fidelity and a verification operator with spectral gap.
- Design: prepare locally accessible test states, apply the target gate, and
  perform local pass/fail measurements.
- Finite-sample guarantee: passing frequencies yield confidence bounds through
  a binary relative-entropy tail bound. The idealized optimal scaling is
  proportional to `log(1/delta)/epsilon` for target infidelity `epsilon` and
  failure probability `delta`.
- Hardware: photonic implementations of a two-qubit CNOT and three-qubit
  Toffoli gate; the reported experiments use finite measurement counts and
  state confidence-qualified fidelity lower bounds.
- Limitations for Ch4: the i.i.d. channel assumption is substantive, and the
  target is average gate fidelity rather than an RZZ parameter or downstream
  decision functional.
- Novelty implication: finite-sample gate certification, confidence-qualified
  fidelity lower bounds, and sample-size scaling are established prior art.
  C2/C3 can only claim an RZZ- and decision-functional-specific construction
  if its guarantees are independently derived and compared.
