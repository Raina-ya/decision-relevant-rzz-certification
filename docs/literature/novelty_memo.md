# Preliminary novelty and source-integrity memo

Status: **G1 open**. Search pass dated 2026-11-27. This is not a systematic
review conclusion and does not support a novelty claim.

## Update after library expansion (2026-11-27, 142 sources)

The second search pass (S016-S027) found two sources that sit closer to Ch4
than anything in the first pass, and changes the classification as follows.
Details and a feature matrix are in `gap_map.md`.

| Claim | Previous classification | Updated classification | Decisive sources |
|---|---|---|---|
| C1 identifiability | substantially overlapped | probe principle is prior art; only the delay-control separation, the off-diagonal diagnostic and the finite-sample treatment remain candidates | RUDINGER2025, CHAI2026, DENG2026 |
| C2 three-outcome rule | generic rule overlapped | mechanics (prespecified tolerance, simultaneous confidence, unresolved outcome, model rejection kept separate) are prior art; only a decision-induced tolerance with strict finite-sample validity remains a candidate | DENG2026, EGGERS2026, BERGER1996, SCHUIRMANN1987 |
| C3 N* bounds | narrowed | a matching two-point lower bound for the decision projection remains a candidate, because DENG2026 states it has none and MORELLI2026 is sequential and asymptotic | DENG2026, MORELLI2026, ZHANG2021 |
| C5 plug-in comparison | overlapped | comparator only | SCAVINO2026 |
| C7 (new) average-metric insufficiency | - | candidate: explicit pairs with equal twirled/angle-averaged fidelity and opposite decisions | KUENG2016, MERKEL2025, IBM-QPU-INFO |

Recommended framing: the twirl-free gap (fractional gates cannot be twirled,
so RB-type, layer-fidelity and Clifford-proxy guarantees do not apply) plus a
decision-induced tolerance and strict finite-sample validity. G1 stays open
until the forward-citation passes in `gap_map.md` Section 6 are complete.

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

### Cross-cutting QAOA sensitivity prior art

`QUIROZ2021` directly models coherent and stochastic QAOA parameter
misspecification as control noise and derives bounds on observable error,
approximation ratio, gradients, and unitary error. `DONG2019` optimizes a QAOA
objective against a bounded coherent-Hamiltonian uncertainty set. Consequently,
the broad idea of propagating coherent angle/control uncertainty into a QAOA
output or worst-case objective is established prior art. Ch4's defensible
question must start after that step: how to obtain a finite-shot, diagnostically
qualified uncertainty set from a native fractional RZZ implementation and how
to turn it into an error-controlled decision for a prespecified instance and
budget.

`SCAVINO2026` is even closer at the decision layer: it propagates finite-shot
QEM residuals into QAOA-MaxCut candidate gaps, compares MSE with selection risk
at matched acquisition cost, and connects decision-certification limits to KL
and local Fisher geometry. It does not estimate a native RZZ residual, but it
means that decision-aware quantum estimation, equal-budget ranking risk, and
margin/covariance sample-cost analysis are not broad Ch4 novelty claims.

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

**Preliminary classification: generic rule overlapped; application-specific
construction unresolved.** Classical TOST and intersection-union testing
already establish prespecified practical-equivalence regions, confidence
interval inclusion, controlled error, power planning, and an undetermined
outcome when the interval is too wide (`SCHUIRMANN1987`, `LAKENS2017`,
`LAKENS2018`, `ARBORETTI2018`). Therefore Ch4 cannot claim the general
confidence-set-inside-tolerance or inconclusive logic as new. In parallel,
`arXiv:2608.01248` develops continuous-parameter testing with an acceptable
neighborhood and rules out sufficiently separated competitors. Its main design
is sequential and its convenient twin-peaks threshold is asymptotically rather
than exactly calibrated. A possible Ch4 contribution is now limited to a
correctly derived fixed-budget frequentist construction for an acceptable set
induced by a nonlinear downstream decision, coupled to the specific RZZ probe
model and model-inadequacy diagnostics. That integration remains unresolved,
not established as novel.

### C3 - N-star bounds

**Preliminary classification: substantially narrowed, unresolved.** RPE
efficiency is prior art. `ZHANG2021` already gives confidence-qualified
finite-sample gate verification and ideal sample scaling proportional to
`log(1/delta)/epsilon`; `arXiv:2608.01248` derives expected stopping costs
governed by the least distinguishable outside-tolerance alternative through KL
divergence and local Fisher information. Classical equivalence work also
includes prospective power planning. A generic claim that Ch4 first connects
tolerance, confidence, and sample cost is untenable. `QUIROZ2021` rules out any
broad claim that QAOA output-error bounds under coherent parameter noise are
new. `SCAVINO2026` also supplies decision-margin, covariance, KL/Fisher, and
fixed-cost selection analyses for quantum estimates. Only new finite-sample
bounds joining this native-RZZ probe family and its diagnostics to the
nonlinear downstream decision functional, if proved and shown nontrivial
relative to these baselines, remain candidates.

### C4 - Prospective power gate

Treat this as a methodological safeguard, not a novelty claim.

### C5 - Equal-shot plug-in comparison

**Preliminary classification: substantially overlapped; retain only as a
problem-specific comparator.** Equivalence-testing literature already explains
why a plug-in estimate inside a practical region does not establish
equivalence. More directly, `SCAVINO2026` compares estimation accuracy with
finite-shot QAOA-MaxCut selection risk at equal evaluation or total acquisition
cost and demonstrates that lower MSE can coincide with unchanged or worse
decision failure. Ch4 may still compare a named gate-calibration plug-in
baseline against its native-RZZ certificate, but the equal-shot decision-risk
comparison is not itself a novelty claim. Any remaining contribution must be
specific to the experimentally inferred gate-error set and exact finite-sample
false-certification control.

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
