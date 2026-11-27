# WP-4 handoff

- Agent / date: Codex / 2026-11-27
- Branch and last commit: `wp-4-exact-decision` @ 757b971, `wp-4-instance-family` @ 7855c65, `wp-4-tolerance-region` @ 4cfb9ae (all merged into main)
- What was done: exact membership, conservative global inner ball/box, sampled radial crossing, seeded scoped family, OD1/OD2, and depolarization lemma
- Acceptance criteria: met for development scope; exact membership and conservative inner box are reproducible and tested
- Open questions for the owner: none needed to continue infrastructure work
- What the next WP needs to know: candidates, graphs, margins, and seeds remain explicit unlocked inputs
- Anything unsure or unverified: Ch3 Lemma-B normalization and numerical radial-boundary globality are explicitly not claimed
- Addendum (Claude, 2026-11-27): `wp-4-average-metric` @ 39a3fa2 adds C7 (`analysis/tolerance/average_metric.py`, `theory/average_metric_insufficiency.md`, `tests/test_average_metric.py`). Equal-fidelity witnesses exist on the 3q/4q instances but not on the 2q hardware-primary instance within |e| <= 0.6; OD1 should be revisited before G3.
