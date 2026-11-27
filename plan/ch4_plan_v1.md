# Ch4 plan v1.1 implementation baseline

Status: unlocked draft. The full planning source is the owner's v1 plan
(Claude Docs, 2026-11-27). This file records the implementation constraints
and the literature-driven revisions made on 2026-11-27. It is not a protocol
lock.

## Research objective (revised after the second literature pass)

Native fractional `RZZ(theta)` gates on IBM Heron cannot be Pauli-twirled, so
RB-type, layer-fidelity and Clifford-proxy guarantees do not apply, and IBM
reports an angle-averaged RZZ error. For a prespecified downstream decision
and fixed shot budget, classify the coherent residual as harmless, harmful or
inconclusive with an error probability bounded at every shot budget, and give
the minimum shots any procedure needs.

The primary model is angle-local: for every decision angle `theta_j`, estimate
`e_j = (epsilon_j, a_j, b_j)`. Cross-angle linear models are secondary only.

## What is prior art and must be cited, not claimed

| Building block | Prior art |
|---|---|
| Diagonal ZI/IZ/ZZ model and RPE identifiability | RUDINGER2025 |
| Control-branch slope separation (ZZ opposite slopes, local phase common slope) | CHAI2026 |
| Three outcomes with prespecified tolerance, simultaneous confidence, separate model rejection | DENG2026, SCHUIRMANN1987, BERGER1996, LAKENS2017, EGGERS2026 |
| Readout symmetrization behind phase cycling | SMITH2021, VANDENBERG2022TREX |
| Decision-risk framing at equal cost | SCAVINO2026 |
| QAOA output sensitivity to coherent control error | QUIROZ2021, DONG2019 |

## Remaining candidate contributions (G1 still open)

1. Decision-induced tolerance from a nonlinear QAOA decision functional of the
   measured gate residual (gap G-B).
2. Strict finite-sample validity through unwrapping and functional projection
   (gap G-C).
3. A two-point lower bound for the decision projection matching the upper
   bound up to constants (gap G-D).
4. Finite-sample model diagnostics including an off-diagonal (Z-conservation)
   check, with allocated false-trigger rate (gap G-F).
5. C7: equal average gate fidelity does not determine the decision; exact
   witnesses exist on the 3- and 4-qubit development instances
   (`theory/average_metric_insufficiency.md`).
6. Native-RZZ hardware evidence without pulse access, with replication
   (gaps G-G, G-H); instance- and budget-specific only.

See `docs/literature/gap_map.md` for the feature matrix and sources.

## Active gates

- G0 platform support: exploratory evidence obtained on `ibm_marrakesh` in
  HW-P2 (fractional RZZ exposure, ISA acceptance and timing). Formal gate
  closure has not been independently audited or recorded.
- G1 literature novelty: open; 142 library sources, 19 papers read at
  relevant-section level or deeper, plus three IBM documentation pages;
  bibliographic integrity tests do not by themselves verify scientific claims.
  Forward-citation passes on RUDINGER2025, CHAI2026 and DENG2026 are
  required before G1 can pass.
- G2 identifiability: L0-L2 draft with exact checks; C7.1-C7.4 draft added.
- G2.5 model diagnostics: logic implemented; thresholds not calibrated.
- G3 prospective power: formulas and ADEMP pipeline exist; not evaluated.
- G4 lock and external timestamp: prohibited until prior gates pass.
- G5-G6 confirmatory hardware and replication: prohibited until a valid G4
  approval. Exploratory HW-P2/HW-P3 pilot approvals do not satisfy G4.

## Resolved design question (OD1 v2)

C7 showed the original 2-qubit instance is insensitive to the ZZ sign
ambiguity. OD1 v2 keeps it as a robust control and adds `path-2q-sign`
(angles pi/16 and pi/8, both measured on pair A), where equal-fidelity
residuals eps = +0.28 and -0.28 give opposite verdicts [exact]. See
`docs/decisions/OD1-v2-sign-sensitive.md`.

## Hardware pilot HW-P2 (exploratory)

Protocol `docs/protocol/HW-P2_pilot_protocol.md`; runner
`hardware/run_hw_p2.py` (or `hardware/run_hw_p2.ps1`), executed by the owner
with two IBM Quantum accounts. Outputs calibrate G3 and G2.5; they are not the
confirmatory G5 run. The primary gamma bound is now
`gamma_interval_grid_bound` (valid, about 3x narrower than the L1 Lipschitz
projection [sim]).

HW-P2 produced platform evidence but no certificate: all prespecified pilot
certificates were inconclusive because the model-adequacy diagnostic triggered.
The result is retained as a negative exploratory finding. See
`results/hw_p2/HW-P2_report.md`.

## Delegation record

- 2026-11-27 (chat): the owner delegated all project decisions except
  `git push` to the working agent (Claude). Recorded in
  `docs/decisions/OD10-integrator.md`.
- No hardware, freeze or preregistration action is taken under this
  delegation, because AGENTS.md Section 1 requires a written owner approval
  naming a locked commit for hardware and the owner pushes.

## Work-package ownership

The canonical cross-WP interfaces live in `src/types.py`. Later changes
require a handoff note. Ownership follows the full v1 plan Section 12.
