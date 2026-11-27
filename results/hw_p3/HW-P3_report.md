# HW-P3 chip-wide parallel probe pilot: report

Evidence label: **[hardware-locked, exploratory pilot HW-P3]** unless marked.
ibm_marrakesh, 49 disjoint RZZ pairs run in parallel (98 qubits per
circuit), angles 0.6119 and pi/16 (account A, 06:38-06:41 UTC) and 1.348 and
pi/8 (account B, 06:45-06:48 UTC), k = 1..32, 1000 shots per circuit,
188 QPU s in total. Analysis: `analysis/hardware/analyze_hw_p3.py` per pair,
same prespecified choices as HW-P2. Certificate map:
`certificate_map.json`.

## 1. Residuals across the chip

- 195 of 196 (pair, angle) boxes identified (one unwrap failure).
- epsilon boxes excluding 0: 5, 4, 3 and 13 of 49 at pi/16, pi/8, 0.612 and
  1.348. With 49 boxes per angle at alpha = 0.05 each, about 2-3 exclusions per
  angle are expected by chance; the counts at pi/16 and 1.348 exceed that.
- Three pairs show large, angle-dependent ZZ residuals that change sign
  between small and large angles, consistent with a miscalibrated scale and
  offset Theta = s*theta + phi (possible cause, not tested):
  - (151, 152): +0.168 (pi/16), +0.103 (pi/8), -0.174 (1.348) rad per gate
  - (27, 28): +0.068, +0.035, -0.063
  - (87, 88): +0.062, +0.024, -0.064
- Median |epsilon| 0.003-0.007 rad; median |local phase| 0.010-0.020 rad.

## 2. Context: pair (53, 54) isolated (HW-P2, k <= 32) versus parallel (HW-P3)

All 12 (angle, parameter) box pairs overlap, for example b at theta = 0.612:
-0.036 +/- 0.024 isolated versus -0.038 +/- 0.025 parallel. No context effect is
detectable on this pair at this precision.

## 3. Certificate map (per pair, grid-bound gamma interval)

| Instance | harmless | inconclusive | not evaluable | After OD11 (Z conservation) |
|---|---|---|---|---|
| path-2q | 46 | 2 | 1 | 17 harmless, 31 inconclusive (model-inadequate) |
| path-2q-sign | 47 | 2 | 0 | 18 harmless, 30 inconclusive (model-inadequate), 1 inconclusive |

- No pair is harmful for either decision. The large residual on (151, 152)
  is harmless for path-2q-sign because its sign at pi/16 and pi/8 moves gamma
  away from the boundary: a large error is not automatically a decision
  error.
- The two inconclusive pairs, (44, 45) and (117, 125), have very wide boxes.
- Z conservation triggers on about 60% of pairs. HW-P3 has no T1 reference,
  and HW-P2 showed that part of such triggers is idle relaxation, so the OD11
  column is conservative.

## 4. Consequences

1. The chapter's premise has direct chip-wide support: per-pair, angle-
   dependent ZZ residuals exist on a minority of pairs and are invisible to
   an angle-averaged error report.
2. Decision relevance depends on the sign pattern across the decision's
   angles, as C7 predicts.
3. A T1 reference must accompany every parallel probe run before OD11 can be
   applied without over-flagging.
4. Multiplicity across pairs needs an explicit rule (for example Holm over
   pairs) for any chip-level claim.

## 5. Amendment 1: chip-wide T1 reference (block P3B3, account B, 07:06 UTC)

Block P3B3: 52 circuits on all 49 pairs at once (control in |1>, delay equal
to k RZZ durations, no RZZ, 2200 shots), 33 QPU s. Script:
`analysis/hardware/t1_correct_hw_p3.py`; per-cell table `t1_excess.json`;
both new OD11 columns added to `certificate_map.json`.
[hardware-locked, exploratory pilot HW-P3; post-hoc analysis]

- The section 3 expectation that OD11 over-flags because of idle
  relaxation is **not supported**. Control flips in the RZZ probe circuits
  exceed the equal-duration delay reference in 455 of 2352 (pair, angle, k,
  role) cells (lower bound of the excess > 0), on 43 of 49 pairs, against
  about 59 expected by chance. The median excess grows with k: +0.002 (k = 1),
  +0.004 (k = 4), +0.012 (k = 16), +0.024 (k = 32), while the median delay
  flip rate at k = 32 is 0.052.
- 125 cells, on 23 pairs, exceed even the diagnostic's allowed rate (0.073)
  in the excess alone.
- Gate-induced control flips are therefore widespread across the chip in
  this parallel context. Possible causes (not tested): leakage or an XY
  component of the native RZZ, and crosstalk from the 48 simultaneous
  neighbouring RZZs. The HW-P2 isolated pair 53-54 showed the same pattern
  more weakly (k = 32 excess up to +0.09 here, versus +0.045 isolated).
- Two pairs show near-complete control depolarization within one block,
  (65, 66) at pi/8 even at k = 1 (probe flip rate 0.50 versus 0.06 delay) and
  (36, 41) at pi/8. This is consistent with a transient defect during that
  block (possible cause, not tested).
- The reference was taken 18-28 minutes after the probe blocks, so drift
  between them is possible.

Re-stated OD11 verdicts (raw verdicts in section 3 unchanged):

| Instance | OD11 absolute (section 3) | OD11, any excess over delay | OD11, excess over allowed rate |
|---|---|---|---|
| path-2q | 17 harmless / 31 model-inadequate | 8 / 40 | 30 / 17 (+1 inconclusive) |
| path-2q-sign | 18 / 30 (+1 inconclusive) | 10 / 39 | 34 / 14 (+1 inconclusive) |

(One path-2q pair is not evaluable in every column.)

Consequence for the chapter: the diagonal model M0 does not hold on most of
the chip at k up to 32 once gate-induced population transfer is resolved
against a delay reference. The certificate's harmless verdicts are
conditional on M0, and the OD11 gate is what keeps them from being reported
unconditionally. Which version of the diagnostic is primary must be fixed
before any confirmatory run (open decision; the absolute-threshold version
stays primary for HW-P2 and HW-P3 because it was the prespecified one).
