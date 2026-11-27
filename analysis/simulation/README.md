# ADEMP development study

The implemented simulation follows an explicit ADEMP structure:

- **Aims:** measure simultaneous M0 coverage, interval availability, three
  verdict rates, false-harmless, and false-harmful rates.
- **Data-generating mechanisms:** M0 residual slopes with visibility and a
  fixed asymmetric-readout scale/offset, followed by binomial sampling.
- **Estimands:** one fixed-angle `(epsilon, a, b)` triple and the signed exact
  downstream gap `gamma`.
- **Methods:** Bonferroni-allocated four-phase Hoeffding intervals, interval
  branch unwrapping, M0 interval arithmetic, global Lipschitz projection, and
  the three-outcome rule.
- **Performance measures:** simultaneous coverage with Monte Carlo standard
  error, interval availability, verdict probabilities, and the two protected
  error probabilities.

This is a development framework, not a completed G3 study. The committed unit
test uses only 40 trials to verify deterministic plumbing. A gate report needs
prespecified scenario grids, enough trials for narrow Monte Carlo uncertainty,
and frozen seeds before execution.

The reproducible development run is:

```powershell
python -m analysis.simulation.run_development
```

Its JSON output is `[sim, development]`. It is deliberately outside the locked
`results/` tree and cannot be used as a G3 verdict.
