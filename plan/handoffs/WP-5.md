# WP-5 handoff

- Agent / date: Codex / 2026-11-27
- Branch and last commit: `wp-5-finite-confidence` @ c8f71a0, `wp-5-gamma-projection` @ c432792, `wp-5-interval-unwrapping` @ d8436e4 (all merged into main)
- What was done: finite-sample phase intervals, non-heuristic interval unwrapping, simultaneous-slope M0 box mapping, verdict rule, and conservative gamma projection
- Acceptance criteria: partial; core finite-sample chain exists, full multi-circuit alpha allocation and ADEMP coverage open
- Open questions for the owner: scientific thresholds remain inputs, not defaults
- What the next WP needs to know: phase non-identifiability returns a full-circle interval
- Anything unsure or unverified: intercept subtraction, full alpha allocation, and a less conservative functional interval remain open
- Addendum (Claude, 2026-11-27): per-candidate residual gap and two valid gamma projections (`gamma_interval_per_candidate`, tighter `gamma_interval_grid_bound`); prespecified hardware analysis in `analysis/hardware/analyze_hw_p2.py` validated on the named synthetic model [sim]. Open: combining replicate blocks, anchor-drift summary, Bonferroni across instances.
