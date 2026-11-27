# G2.5 diagnostic calibration - development simulation

Evidence label: **[sim, development]**. This is not a G2.5 pass, a locked
threshold choice or a hardware result.

## Design

- Trials: 2,000 per scenario with fixed, recorded seeds.
- `alpha_diag = 0.05`, split equally over Z conservation, phase linearity and
  log-linear contrast-amplitude diagnostics.
- Phase/amplitude family error is split over `k = (1, 2, 4, 8)`.
- Four-phase shots: 16,000 per phase and k; Z-conservation shots: 32,000.
- Allowed control-flip rate: 0.02.
- Nominal M0: flip rate 0.01, phase slope 0.12, exponential visibility decay
  0.015 per repetition, readout scale 0.94 and offset -0.03.

These large development counts are a consequence of conservative Hoeffding
sets. They are not a recommended hardware budget.

## Results

The table reports the combined probability of any diagnostic trigger. The
95% intervals are Wilson Monte Carlo intervals, not confidence statements
about unmodelled hardware populations.

| Scenario | Any trigger | 95% MC interval | Inconclusive | Triggering family |
|---|---:|---:|---:|---|
| M0 null, flip 0.01 | 0.000 | [0.000, 0.00192] | 0.001 | none |
| Z boundary null, flip 0.02 | 0.000 | [0.000, 0.00192] | 1.000 | none |
| Z alternative, flip 0.03 | 0.984 | [0.9775, 0.9886] | 0.016 | Z |
| Z alternative, flip 0.05 | 1.000 | [0.9981, 1.000] | 0.000 | Z |
| Z alternative, flip 0.08 | 1.000 | [0.9981, 1.000] | 0.000 | Z |
| Phase curvature 0.005 | 0.873 | [0.8572, 0.8864] | 0.000 | phase |
| Phase curvature 0.015 | 1.000 | [0.9981, 1.000] | 0.000 | phase |
| Phase curvature 0.030 | 1.000 | [0.9981, 1.000] | 0.000 | phase |
| Visibility curvature 0.005 | 0.000 | [0.000, 0.00192] | 0.001 | none |
| Visibility curvature 0.010 | 0.220 | [0.2024, 0.2387] | 0.001 | visibility |
| Visibility curvature 0.020 | 1.000 | [0.9981, 1.000] | 0.000 | visibility |

## Interpretation

The implementation is conservative under the simulated null and has high
power for the larger Z and phase alternatives. It deliberately returns
inconclusive at the exact Z threshold because the confidence interval cannot
prove either side of the tolerance boundary.

Visibility curvature is the limiting diagnostic: curvature 0.005 is not
detected and curvature 0.010 is detected in only 22.0% of trials. Therefore a
non-triggered visibility diagnostic cannot be presented as strong evidence of
an exponential decay law at this budget. This result supports retaining the
OD11 rule that non-triggered means only "not rejected", never "validated".

## Remaining boundary

Before G2.5 can be evaluated, the final alternatives, shot allocation and
thresholds must be connected to G3, and WP10 must independently audit the
coverage argument and simulation. No choice in this document is frozen.
