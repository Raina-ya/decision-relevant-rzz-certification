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

`arXiv:2502.06698` is directly relevant prior art for RPE-based coherent-error
estimation in entangling gates. Only the abstract was reviewed in this pass.
The full model, equivalence classes, idle-detuning treatment, and probe
requirements must be compared before deciding whether L0-L7 add anything.

### C2 - Three-outcome decision rule

No primary source establishing the same downstream-decision tolerance region
and finite-sample three-outcome rule was verified in this pass. Absence from
this small search is not evidence of novelty. Searches for quantum gate
certification, equivalence tests, intersection-union tests, and task-oriented
benchmarking remain required.

### C3 - N-star bounds

RPE efficiency and consistency testing are prior art. Whether projecting
information onto a downstream decision functional and distinguishing
non-identifiability from budget insufficiency is new remains open.

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

