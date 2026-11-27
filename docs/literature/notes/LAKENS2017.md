# LAKENS2017 reading note

Reading status: relevant sections read. Reviewed the TOST construction,
confidence-interval interpretation, equivalence-bound selection, power
analysis, examples, and discussion.

- Question: How can a frequentist analysis support that an effect is smaller
  than a prespecified practically meaningful size?
- Design: specify lower and upper equivalence bounds, then reject both
  one-sided null hypotheses that the effect lies beyond either bound.
- Guarantee: at level `alpha`, equivalence corresponds to a
  `100(1 - 2 alpha)%` confidence interval lying wholly inside the equivalence
  bounds for the standard settings discussed.
- Outcomes: a wide interval crossing a bound is undetermined; lack of ordinary
  significance is not evidence of equivalence.
- Planning: power and sample size depend on the equivalence bounds, which must
  be justified substantively rather than selected after seeing the data.
- Relation to Ch4: the confidence-set-inside-tolerance rule and an inconclusive
  result are established statistical practice. Ch4 must not claim these as a
  general invention; only its quantum model, induced decision set, diagnostic
  safeguards, or new bounds could be contribution candidates.
