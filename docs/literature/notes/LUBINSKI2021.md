# LUBINSKI2021 reading note

Reading status: relevant sections read. Reviewed introduction/background,
application-oriented benchmark definition, circuit construction and execution,
result-fidelity metric and its limitations, hardware/simulator analyses, and
conclusion. Algorithm appendices were sampled only where relevant.

- Question: How should hardware be benchmarked on recognizable algorithms and
  applications rather than component metrics alone?
- Design: circuits from multiple application families are run across width and
  depth, with compilation included in the tested execution pipeline.
- Outcome: result fidelity and execution time, summarized volumetrically.
- Statistical guarantee: shots and circuits are user-selected; this work is a
  benchmarking framework, not an equivalence test with finite-sample
  false-certification control.
- Relation: establishes substantial prior art for application-oriented
  positioning. Ch4 cannot claim to introduce task-oriented benchmarking. Its
  narrower possible distinction is a prespecified decision functional plus
  finite-sample three-outcome error control for a particular gate error.

