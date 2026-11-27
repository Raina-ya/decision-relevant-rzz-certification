# HW-P3 chip-wide parallel probe pilot (exploratory)

Status: prespecified under an internal lock (`docs/decisions/HW-P3-approval.json`).
Exploratory; outputs carry `[hardware-locked, exploratory pilot HW-P3]`.

- **Question.** Do per-pair residual boxes stay the same when all pairs of a
  matching run simultaneously (spectators active), and how do residuals vary
  across the chip?
- **Layout.** `select_matching`: greedy disjoint `rzz` pairs by ascending
  reported error, readout error <= 0.05 on both qubits, pair (53, 54) forced so
  it can be compared with HW-P2. Recorded in `results/hw_p3/matching.json`.
- **Design.** Each circuit applies one probe key to every pair at once:
  k in {1, 2, 4, 8, 16, 32} (k = 64 dropped after HW-P2), control in {0, 1},
  both roles, four analysis phases, delay and k = 0 controls, plus four
  parallel readout circuits; 164 circuits x 1000 shots per angle.
  Account A: angles 0.6119 and pi/16. Account B: 1.3480 and pi/8.
- **Stored data.** Per-pair 2-bit marginal counts only.
- **Analysis.** `analysis/hardware/analyze_hw_p3.py`, identical choices to
  HW-P2 applied per pair; plus the (53, 54) parallel-versus-isolated
  comparison at matching angles.
- **Not claimed.** Any crosstalk mechanism; any confirmatory verdict.

## Amendment 1 (2026-11-27, after blocks P3A1-P3B2 were recorded)

Block P3B3-parallel-t1-reference added for account B (remaining 0.63 RU):
control prepared in |1>, delay equal to k RZZ durations on every pair,
k = 1..32, both roles, four phases, 2200 shots (owner, 15:04: use all remaining quota on account B), no RZZ. Analysis: per pair,
control-flip excess of the probe blocks over this reference at equal k; the
OD11 column of the HW-P3 report is re-stated with and without this
correction, both kept. Taken hours after the probe blocks (drift possible).
