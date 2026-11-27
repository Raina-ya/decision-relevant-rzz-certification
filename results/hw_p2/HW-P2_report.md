# HW-P2 exploratory hardware pilot: report

Evidence label for every number: **[hardware-locked, exploratory pilot
HW-P2]** unless marked [post-lock]. Backend ibm_marrakesh (IBM Heron), chain
q53-q54-q55 selected by the prespecified rule; pair A = (53, 54), pair B =
(54, 55). Runs on 2026-11-27 between 05:58 and 06:29 UTC. Account A used 437
QPU s, account B 433 QPU s. Measured cost about 0.28 ms per shot.
Analysis: `analysis/hardware/analyze_hw_p2.py` (prespecified), raw outputs in
`analysis_raw.json` and `certificates_raw.json`.

## 1. Platform (G0 evidence)

- `use_fractional_gates=True` exposed `rzz` on both pairs; reported RZZ error
  1.34e-3 (53-54) and 1.16e-3 (54-55), duration 68 ns.
- Every submitted circuit passed the ISA check (RZZ count, angle, pair; no
  folding or merging). No submission failed.

## 2. Coherent residuals per gate (finite-sample boxes, alpha = 0.05 each)

- ZZ residual epsilon: every one of the 19 identified (pair, angle) boxes
  contains 0; half-widths 0.006-0.011 rad. No detectable ZZ over- or
  under-rotation at any angle from pi/16 to pi/2.
- Local phase on q54 as pair-A target (b): -0.032 to -0.041 rad per gate at
  every angle, all boxes exclude 0. This is the dominant coherent residual.
- Local phase on q53 (pair A, a): angle dependent, from about 0 at small
  angles to -0.031 +/- 0.013 rad at theta = 1.348.
- Pair B, local phase on q55 (b): angle dependent, from +0.009 (pi/16) to
  -0.062 (theta = 1.506).
- Cross-account replication (A1/A6 versus B2, same pair and angles, about 15
  minutes apart): every box pair overlaps; e.g. a at theta = 1.348 is
  -0.031 +/- 0.013 (A) and -0.033 +/- 0.018 (B).

## 3. Model diagnostics

- The prespecified Z-conservation diagnostic triggered at the largest k for
  almost every box, always for control = 1.
- Amendment-1 T1 reference (A7, delay only, control in |1>) [post-lock
  comparison, labelled as result-informed]:
  - control q54 (role 1): RZZ and delay flip rates agree at every k
    (k = 64: 0.057 versus 0.066). Idle relaxation suffices.
  - control q53 (role 2): RZZ exceeds delay at k = 32 (+0.045 +/- 0.032) and
    k = 64 (+0.079 +/- 0.032). Gate-induced population change of q53 in |1>.
    Possible cause, not tested: exchange-type (XY) error or leakage.
- So M0 is inadequate for pair A when q53 is the excited control at
  k >= 32; at k <= 16 the excess is within its interval.

## 4. Certificates

| Instance | Margin | Gamma interval, k <= 64 | Prespecified verdict (OD11) | Raw rule ignoring diagnostics | [post-lock] k <= 16 |
|---|---|---|---|---|---|
| path-2q | 0.210 | [0.402, 0.438] | inconclusive (model-inadequate) | harmless | harmless [0.351, 0.487] |
| path-2q-sign | 0.075 | [0.131, 0.172] | inconclusive (model-inadequate) | harmless | inconclusive [0.075, 0.229] |
| path-3q | 0.077 | [-0.015, 0.331] | inconclusive (model-inadequate) | inconclusive | inconclusive |

The replicate (B2) gives the same pattern for both 2-qubit instances.

## 5. Direct decision circuits (20000 shots each)

All eight direct comparisons preserve the ideal decision, for both native RZZ
and CZ-decomposed implementations:

| Instance | Native RZZ signed gap | CZ-decomposed signed gap |
|---|---|---|
| path-2q (A5) | 0.408 [0.386, 0.431] | 0.410 [0.388, 0.433] |
| path-2q-sign (A5) | 0.147 [0.125, 0.170] | 0.138 [0.116, 0.161] |
| path-2q-sign (B3) | 0.121 [0.099, 0.144] | 0.120 [0.098, 0.143] |
| path-3q (B3) | 0.134 [0.088, 0.179] | 0.150 [0.105, 0.195] |

These include incoherent noise (gap shrinkage) and are an operational check,
not a certificate.

## 6. What this pilot supports and does not support

Supports: on this pair, this backend and this half hour, no ZZ over-rotation
was detectable at 0.01 rad per gate; the coherent residual is a local Z phase
of about 0.035 rad per gate on q54; replication across accounts is
consistent; the prespecified rule would certify both 2-qubit decisions were
it not for a diagnostic that the T1 reference shows is partly genuine.

Does not support: that native RZZ is harmless in general; any physical cause;
any statement about other pairs or times; a confirmatory verdict.

## 7. Consequences for the confirmatory design

1. Add the delay-only control-|1> reference to the protocol, and define the
   Z-conservation diagnostic on the excess over it.
2. Cap k at 16 or 32 for pairs with an excited-control excess, or model the
   excess explicitly; k = 64 gains precision but breaks M0 on q53.
3. Local phases dominate; decisions whose gap depends mainly on local phases
   (mixer-side sensitivity) are the natural next sign-sensitive instances.
4. Cost model for G3: 0.28 ms per shot on ibm_marrakesh, including overhead.
5. The 3-qubit certificate is limited by the conservative 3-point grid bound
   in six dimensions; a finer or exact bound is needed before G3.
