# WP-7 handoff

- Agent / date: Codex / 2026-11-27
- Branch and last commit: `wp-7-offline-preflight` @ 9988f3e (merged into main)
- What was done: offline capability and circuit receipts, receipt schema, exact approval guard, fail-closed runner
- Acceptance criteria: partial; dry receipts and refusal tested, Qiskit ISA/backend/timing checks open
- Open questions for the owner: none until an approved local Qiskit environment is available
- What the next WP needs to know: HW-P2 subsequently ran under owner approval;
  its result is exploratory and model-inadequate, not G5 evidence
- Anything unsure or unverified: formal G0 gate closure and an independent
  audit have not occurred
- Addendum (Claude, 2026-11-27): HW-P2 pilot tooling added (`hardware/hw_p2_design.py`, `run_hw_p2.py`, `run_hw_p2.ps1`, `RUN_HW_P2.md`, `src/qiskit_adapter.py`). Dry runs pass on FakeMarrakesh plus a bounded fractional RZZ target [fake-backend]; a mock submission test covers chunking (<=290 circuits/job), the QPU-seconds cap and private job-ID logging. Real G0 evidence will come from the owner's HW-P2 run.
- Addendum (post-run audit, 2026-11-27): HW-P2 ran on `ibm_marrakesh`;
  fractional RZZ exposure, ISA acceptance and timing are recorded in
  `results/hw_p2/HW-P2_report.md`. All pilot certificates were inconclusive
  because the model-adequacy diagnostic triggered.
