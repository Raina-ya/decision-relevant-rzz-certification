# Preliminary novelty and source-integrity memo

Status: **G1 open**. Search pass dated 2026-11-27. This is not a systematic
review conclusion and does not support a novelty claim.

## Immediate source corrections

Two identifiers in the v0/v1 planning notes do not support the attached
descriptions:

1. `arXiv:2508.10997` resolves to *Reliable high-accuracy error mitigation for
   utility-scale quantum circuits*, not a targeted-layer-calibration paper.
   The planned claim about Ramsey/refocusing characterization must remain
   uncited until the intended primary source is found.
2. `arXiv:2609.28825` resolves to Nikita A. Zemlevskiy's *Fundamental Physics
   at the Frontier of Noisy Quantum Computation*. Its abstract does not support
   the planning note that a Heron workflow calibrates RZZ angles immediately
   before execution. That note must remain uncited pending identification of
   the intended chapter or a different primary source.

Neither mismatched identifier was entered as supporting evidence in
`library.csv`.

## Platform-premise update

Current IBM documentation describes the Heron "RZZ error" as an error averaged
over RZZ angles using a variant of randomized benchmarking for arbitrary
unitaries. This conflicts with the v0/v1 statement that the target merely
copies a non-fractional gate's error value. The thesis may still argue that an
angle-averaged gate metric does not answer an instance- and decision-specific
question, but it must not claim that IBM supplies no RZZ-specific information
without version-bound evidence.

The documentation also confirms that fractional-gate workflows have constraints
involving dynamic circuits and several noise-management options, and that
`FoldRzzAngle` can transform out-of-range angles. Exact endpoint behavior is
worded inconsistently across current pages (`< pi/2` in one description and
`<= pi/2` in workflow guidance), so G0 must inspect the selected backend target
and transpiler version instead of relying on prose alone.

## Contribution-by-contribution preliminary assessment

### C1 - Identifiability

**Preliminary classification: substantially overlapped; narrow or remove the
claim.** Full-text review of `arXiv:2502.06698` shows that it already constructs
three logarithmic-depth RPE experiments for a commuting two-qubit CZ model,
estimates three independent relative phases, and linearly inverts them to the
ZI, IZ and ZZ coefficients. Its atan2 branch selection and consistency checks
also overlap the proposed mechanics. Ch4 can still investigate idle-detuning
separation, fixed-shot confidence, explicit model-inadequacy diagnostics, and
decision projection, but must cite/adapt the underlying identifiability result
rather than present it as a new general construction.

### C2 - Three-outcome decision rule

**Preliminary classification: narrowed, unresolved.** `arXiv:2608.01248`
develops continuous-parameter testing with an acceptable neighborhood and
rules out sufficiently separated competitors. This is close prior art for the
tolerance-testing concept. Its main design is sequential; its convenient
twin-peaks threshold is explicitly not an exact finite-sample error probability
and is calibrated asymptotically. Ch4's possible distinction is a fixed-budget,
frequentist finite-sample rule whose acceptable set is induced by a nonlinear
downstream decision and whose terminal result may be inconclusive. Classical
equivalence/noninferiority literature still must be reviewed before this can be
called a gap.

### C3 - N-star bounds

**Preliminary classification: narrowed, unresolved.** RPE efficiency is prior
art, and `arXiv:2608.01248` derives expected stopping costs governed by the
least distinguishable outside-tolerance alternative through KL divergence and
local Fisher information. A generic claim that Ch4 first connects tolerance,
Fisher information, and sample cost is untenable. Fixed-budget minimax bounds
for a downstream decision functional, and a formal split between observational
non-identifiability and budget insufficiency, remain to be compared.

### C4 - Prospective power gate

Treat this as a methodological safeguard, not a novelty claim.

### C5 - Equal-shot plug-in comparison

Open. The comparison requires literature on uncertainty-ignorant plug-in
certification and equivalence testing before it can be positioned.

### C6 - Hardware result

Any future hardware result will be limited to its backend, pair, time, instance,
and budget. It is not a novelty claim by itself.

## Verified source URLs

- https://arxiv.org/abs/2502.06698
- https://arxiv.org/abs/1502.02677
- https://arxiv.org/abs/1702.01763
- https://arxiv.org/abs/2011.13442
- https://eu-de.quantum.cloud.ibm.com/docs/en/ibm-quantum-compute/fractional-gates
- https://quantum.cloud.ibm.com/docs/en/tutorials/fractional-gates
- https://eu-de.quantum.cloud.ibm.com/docs/en/ibm-quantum-compute/qpu-information
