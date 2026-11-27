# WP-6 handoff

- Agent / date: Codex / 2026-11-27
- Branch and last commit: `wp-6-power-bounds` @ 42021c2, `wp-6-ademp-simulation` @ bdcf86c (both merged into main)
- What was done: finite-sample phase upper bound, direct-mean reference bound, Bernoulli BH lower bound, linear QPU estimate, and end-to-end ADEMP simulation pipeline
- Acceptance criteria: partial; formulas, pipeline and a two-angle one-edge
  prospective development grid are tested; multi-edge and
  diagnostic-inclusive ADEMP remain open
- Open questions for the owner: none required until scientific inputs are ready
- What the next WP needs to know: `g3_draft.md` explicitly records why no verdict is supported
- Anything unsure or unverified: constants have not received independent
  mathematical audit; the linear QPU-time estimate excludes job overhead,
  drift and diagnostic circuits
