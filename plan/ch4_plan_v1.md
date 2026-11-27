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

- G0 platform support: open; no Qiskit runtime is installed and no hardware
  query has been made.
- G1 literature novelty: open; 138 verified sources, 17 read beyond the
  abstract; forward-citation passes on RUDINGER2025, CHAI2026, DENG2026 are
  required before G1 can pass.
- G2 identifiability: L0-L2 draft with exact checks; C7 draft added.
- G2.5 model diagnostics: logic implemented; thresholds not calibrated.
- G3 prospective power: formulas and ADEMP pipeline exist; not evaluated.
- G4 lock and external timestamp: prohibited until prior gates pass.
- G5-G6 hardware and replication: prohibited until a valid G4 approval.

## Open design question raised by C7

The 2-qubit hardware-primary instance has no equal-fidelity witness within
|e| <= 0.6, so it is insensitive to the ZZ sign ambiguity that motivates the
chapter. OD1 should be reconsidered before G3: either keep the 2-qubit
instance as a "robust" control and add a second instance where the
average-metric argument bites, or move the hardware-primary instance to a
3-qubit path (which needs two probed pairs and a larger budget).

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
