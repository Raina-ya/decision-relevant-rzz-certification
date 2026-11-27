# WP1 systematic literature review protocol

Status: development protocol, version 0.1, 2026-11-27. This protocol is not a
preregistration and G1 remains open.

## Review questions

The review asks whether prior work already establishes any of the proposed
contributions C1-C5, and which adjacent results constrain a defensible Ch4
question. C6 is an instance-specific hardware result, not a novelty claim.

1. Which coherent parameters of parameterized two-qubit diagonal gates are
   identifiable under SPAM, idle detuning, repeated sequences, and contextual
   errors?
2. Which quantum-gate certification or equivalence-testing procedures provide
   finite-sample error control, abstention or indifference regions, and sample
   complexity bounds?
3. Which benchmarking methods define success through an application output or
   downstream decision rather than gate fidelity alone?
4. What is known about QAOA decision sensitivity to coherent RZZ-like errors?
5. What evidence exists for native fractional two-qubit gates on IBM Heron,
   including reported metrics, compilation constraints, and calibration?

## Sources and search families

Search arXiv, Crossref/publisher records when a DOI is present, and official
IBM Quantum documentation. Technical claims must be traced to primary papers
or official documentation. Searches cover these families:

- `quantum gate certification` AND (`finite sample` OR confidence OR sample
  complexity)
- (`quantum process` OR `quantum gate`) AND (hypothesis test OR equivalence OR
  verification)
- (`robust phase estimation` OR Ramsey OR `error amplification`) AND
  (`two-qubit gate` OR entangling OR RZZ)
- (`task-oriented` OR `application-oriented` OR `application-level`) AND
  (`quantum benchmarking` OR QCVV)
- QAOA AND (`coherent error` OR overrotation OR sensitivity OR robustness)
- (`fractional gate` OR RZZ) AND (Heron OR IBM) AND (calibration OR benchmark)
- (`cycle benchmarking` OR `gate set tomography`) AND (`context dependence`
  OR model violation OR finite sample)

For every search pass, record the literal query, date, source, and disposition
in `search_log.csv`. Forward citation chasing and reference-list chasing are
recorded as separate search passes.

## Eligibility

Include primary research or official platform documentation that addresses at
least one review question through a theorem, method, experiment, or platform
specification. Include foundational statistical work only when it supplies a
tool actually used to assess C1-C5. Exclude secondary summaries, unsourced
blogs, machine-learning calibration methods (out of project scope),
pulse-control-only work with no transferable result, and papers mentioning a
keyword without addressing a review question.

No date or hardware-platform restriction is imposed. English-language sources
are included. A later version supersedes an earlier version of the same work;
the earlier version remains in the screening log but not as a separate study.

## Screening and deduplication

Deduplicate by DOI, then arXiv identifier, then normalized title and author.
Screen title/abstract first. Retrieve full text for every included candidate.
Record one exclusion reason: off topic, secondary source, duplicate,
out-of-scope ML, pulse-only, inaccessible full text, or insufficient evidence.
Inaccessible work is not treated as evidence of absence.

## Reading and evidence levels

`library.csv` uses exactly these reading statuses:

- `bibliographic only`: identity verified; content not assessed.
- `abstract only`: abstract read; notes start with `[abstract only]`.
- `relevant sections read`: methods/results relevant to the review question
  read, with sections or pages listed in a paper note.
- `full text read`: complete main text and relevant appendices read.
- `documentation page reviewed`: complete relevant official page reviewed and
  access date recorded.

Each included paper receives `notes/<id>.md` containing the research question,
model and assumptions, estimand, design/probes, statistical guarantee, sample
complexity, hardware evidence, limitations, relation to C1-C5, and exact
sections actually read. Numerical and theorem claims cannot be promoted from
an abstract-only record.

## Synthesis and stopping rule

Populate `method_matrix.csv` only from paper notes. A proposed contribution is
classified as `overlapped`, `narrowed`, `unresolved`, or `not found in this
review`; the last category is not proof of novelty.

The initial G1 pass stops only after all search families have been run, all
included candidates have at least relevant-section notes, and two consecutive
backward/forward citation passes add no study that changes a C1-C5
classification. New relevant work reopens the corresponding classification.

