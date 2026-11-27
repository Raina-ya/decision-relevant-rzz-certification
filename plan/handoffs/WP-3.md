# WP-3 handoff

- Agent / date: Codex / 2026-11-27
- Branch and last commit: `wp-0-initialize` @ 54ca081 (merged into main)
- What was done: SDK-independent probe schema and exact M0 analytic core
- Acceptance criteria: partial; SDK-independent exact checks pass and HW-P2
  circuits passed backend ISA checks, while local Qiskit adapter tests remain
  skipped because the dependency is not installed
- Open questions for the owner: none at this stage
- What the next WP needs to know: circuit generation exists and has exploratory
  hardware evidence; that evidence is not a confirmatory certificate
- Anything unsure or unverified: no Qiskit installation was found locally
