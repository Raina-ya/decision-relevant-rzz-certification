# MIKLIN2026 reading note

Reading status: relevant sections read. Reviewed abstract/introduction, the
certification task and gauge-invariant parameter setup, short- and
long-sequence certification results, statistical-analysis section, conclusion,
and the corresponding theorem appendices. The full appendices were not read
line by line.

- Question: Can a high-quality single-qubit pi/2 rotation be soundly certified
  with unknown state preparation and measurement and practical samples?
- Model: unknown qubit state, two-outcome measurement, and time-independent
  CPTP channel. Observable descriptions are gauge-equivalent.
- Design: fixed deterministic sequences, with a short-sequence test followed
  by longer repetitions when the high-quality prerequisite passes.
- Estimand/certificate: a complex PTM rotation eigenvalue, followed by a
  fidelity lower bound up to a unitary change of basis.
- Finite-sample content: observed frequencies are converted to simultaneous
  confidence bounds before the spectral certificate is formed. The trapped-ion
  demonstration uses 22,000 circuit executions and reports 99% confidence.
- Hardware: single trapped calcium ion; target is sqrt-X, not a two-qubit
  parameterized entangling gate.
- Limitations for Ch4: time independence and qubit dimension are substantive;
  the certificate targets gate fidelity/spectrum, not a specified downstream
  decision or an equivalence margin. It does not provide the Ch4 three-outcome
  rule, but it is strong overlapping prior art for repeated-sequence,
  finite-sample, SPAM-robust certification and therefore narrows C2/C3.

