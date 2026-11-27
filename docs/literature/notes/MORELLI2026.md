# MORELLI2026 reading note

Reading status: relevant sections read. Reviewed framework, all three parameter
tests and their stopping rules, stopping-time analysis, phase and purity
examples, fixed-sample comparison, conclusions, and relevant appendices. The
quantum-hypothesis background proofs were not read line by line.

- Question: How can an unknown continuous parameter be determined only up to a
  prescribed tolerance while controlling evidence/error and allowing a random
  stopping time?
- Design: sequential complement, concentration, and twin-peaks tests. A reported
  estimate defines an acceptable neighborhood; sufficiently separated
  alternatives must be ruled out.
- Guarantee: the complement test has a posterior-region interpretation. The
  computationally convenient twin-peaks rule compares the strongest outside
  competitor, but the paper explicitly states that its threshold is not an
  exact finite-sample posterior error probability; its calibration and the
  equivalence of the three tests are asymptotic.
- Cost: expected stopping time is controlled by the least distinguishable
  alternative through KL divergence, with a local Fisher-information
  approximation. Phase and purity examples compare sequential and fixed-copy
  strategies.
- Relation to Ch4: this is close prior art for tolerance-based parameter testing
  and for the idea that the hardest outside alternative controls sample cost.
  It narrows C2/C3 substantially.
- Remaining distinction: Ch4 proposes a fixed maximum budget, frequentist
  finite-sample confidence coverage, a tolerance defined by a nonlinear
  downstream decision functional rather than parameter distance, and three
  terminal labels including inconclusive. Those distinctions require further
  comparison with equivalence/noninferiority testing before any novelty claim.

