# HW-P4 plan: depth (draft for the next quota cycle)

Status: plan only, no runner yet. Motivation: coherent residuals add up
linearly with depth, so decision relevance should appear only beyond some
depth; finding that depth is the large-scale form of the chapter question.

## Experiments (priority order, about 10 QPU minutes per account)

1. **Depth-scan QAOA on the probed chain 53-54-55 and on (151, 152).**
   p = 1, 2, 4, 8 layers (up to 16 native RZZ per qubit pair per candidate),
   native and CZ-decomposed, two candidate parameter sets per p. Prediction:
   exact simulation with the HW-P2/HW-P3 residual boxes composed layer by
   layer; test: does the predicted certificate (harmless / harmful /
   inconclusive) agree with the directly measured decision as p grows?
   (151, 152) is the strongest test because its residual is large and
   sign-changing.
2. **Deep k ladder with T1 reference** on (53, 54) and (151, 152): k up to
   256 for probe and delay-only control-|1> circuits, to measure where
   coherent amplification stops paying (k*) and to calibrate G3.
3. **Parallel probes with T1 reference** at the remaining grid angles, so
   OD11 can be applied chip-wide without over-flagging.

## Needed before running

- Layer-composition theory for the certificate (residual per gate applied
  p times; Lipschitz constant grows with p).
- Exact simulator for p-layer QAOA on up to 3 qubits with per-candidate
  residuals (cheap), light-cone simulator for larger subgraphs (later).
- Dry runs, mock submission test, approval record.
