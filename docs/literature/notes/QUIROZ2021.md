# QUIROZ2021 reading note

Reading status: relevant sections read. Reviewed the precision-error model,
QAOA control formulation, coherent and stochastic cumulant calculations,
observable/approximation-ratio/gradient/unitary bounds, numerical Grover and
Ising examples, mitigation discussion, finite-sampling appendix, and stated
limitations. Algebraic appendices were sampled where needed rather than read
line by line.

- Question: How do static coherent and time-varying stochastic errors in QAOA
  control parameters affect training and algorithmic performance?
- Model: multiplicative misspecification of the mixer and cost Hamiltonian
  controls. Constant nonzero-mean errors represent coherent precision error;
  zero-mean white processes represent stochastic precision error.
- Method: a cumulant expansion in a toggling/control frame approximates the
  noisy dynamics and yields norm bounds on expectation-value error,
  approximation ratio, parameter gradients, and unitary error.
- Evidence: analytical bounds are compared with simulations of Grover-search
  QAOA and a one-dimensional Ising/2-SAT example. Coherent-error behavior can
  be nonmonotone outside the initial weak-error regime.
- Sampling: the appendix adds finite sampling of bounded observables to the
  performance bounds. It does not construct a confidence region for an
  experimentally estimated native-gate residual or a three-outcome
  certification rule.
- Limitations for Ch4: the precision error is imposed at the algorithmic
  control level rather than identified from native fractional RZZ probes; the
  numerical examples are not the fixed MaxCut candidate-selection family; no
  SPAM/model diagnostic or false-harmless guarantee is supplied.
- Novelty implication: mapping coherent parameter errors to QAOA observables
  and deriving general performance bounds are prior art. Ch4 can only claim a
  narrower measurement-to-certificate result, plus any genuinely new
  fixed-budget lower/upper bound for its particular decision functional.
