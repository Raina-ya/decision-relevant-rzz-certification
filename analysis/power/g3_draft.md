# G3 prospective power report - draft

Status: **not evaluated / not passed**. All values below are methods or
development estimates, not a locked design.

## Implemented bounds

1. `required_shots_phase_radius` gives a finite-sample sufficient upper bound
   for four-phase estimation when a minimum observed amplitude and desired
   angular radius are prespecified.
2. `direct_hoeffding_shots` is a reference upper bound for a directly observed
   bounded scalar mean. It is not silently used as the RZZ design cost.
3. `bretagnolle_huber_required_samples` gives a necessary sample lower bound
   for two simple Bernoulli hypotheses. It distinguishes a zero-KL
   non-identifiable pair (`N = infinity`) from a finite but possibly expensive
   pair.
4. `estimated_qpu_seconds` reproduces the v1 linear extrapolation but excludes
   unmeasured job overhead and depth dependence.

## Missing inputs before a G3 verdict

- Final decision instances, candidates, and margins.
- Simultaneous unwrapped M0 confidence box construction across `k`, controls,
  roles, angles, and delay controls.
- Diagnostic thresholds and their allocated error probability.
- Preflight amplitude and timing bounds.
- A locked budget ceiling and multiplicity policy.
- Full ADEMP coverage and power results with Monte Carlo uncertainty.

Until these exist, reporting G3 as pass or fail would be unsupported.

