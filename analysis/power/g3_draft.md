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
- Multi-edge simultaneous M0 boxes and their alpha allocation. The one-edge
  two-angle construction is implemented and simulated.
- Final diagnostic thresholds and diagnostic-inclusive cost/power accounting.
- Preflight amplitude and timing bounds.
- A locked budget ceiling and multiplicity policy.
- Full multi-edge ADEMP coverage and power results with Monte Carlo
  uncertainty.

The end-to-end ADEMP pipeline exists in `analysis/simulation/ademp.py`. A
two-angle development grid for the one-edge sign-sensitive instance is now
recorded in `analysis/simulation/g3_development_grid.json` and
`g3_development_report.md`. It allocates alpha separately across both decision
angles and reports Monte Carlo intervals and a linear QPU-time estimate.

That grid is deliberately narrower than G3: the residual truth is shared
across angles even though the confidence boxes are separate; multi-edge
instances, diagnostic costs, drift and job overhead are excluded; and the
instance family remains unlocked. It therefore provides prospective
development evidence but not a gate verdict.

Until the remaining inputs are owner-reviewed and the multi-edge and
diagnostic-inclusive grid is complete, reporting G3 as pass or fail would be
unsupported.
