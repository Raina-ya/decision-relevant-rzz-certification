# Ch4 plan v1 implementation baseline

Status: unlocked draft derived from the owner's 33-page v1 plan dated
2026-11-27. The PDF remains the full planning source; this file records only
the implementation constraints needed to begin work and must not be treated as
a protocol lock.

## Research objective

For a prespecified downstream decision and fixed shot budget, classify native
fractional `RZZ(theta)` coherent error as harmless, harmful, or inconclusive,
with controlled error probability.

The primary model is angle-local: for every decision angle `theta_j`, estimate
`e_j = (epsilon_j, a_j, b_j)`. Cross-angle linear models are secondary only.

## Active gates

- G0 platform support: open; no Qiskit runtime is installed in the current
  environment and no hardware query has been made.
- G1 literature novelty: open; no contribution is currently called novel.
- G2 identifiability: draft work may proceed; L0-L2 exact checks are the first
  target.
- G2.5 model diagnostics: open.
- G3 prospective power: blocked on estimators, decision instances, and owner
  thresholds.
- G4 lock and external timestamp: prohibited until prior gates pass.
- G5-G6 hardware and replication: prohibited until a valid G4 approval.

## Initial decisions delegated on 2026-11-27

- OD10: Codex acts as temporary integrator for repository initialization.
- OD16: standard development cadence, without promising calendar completion.
- No hardware, freeze, or preregistration authority is inferred from this
  delegation.
- Other decisions remain proposals until their inputs exist; code must expose
  them as explicit inputs rather than silently fixing scientific values.

## Work-package ownership used now

| WP | Write paths | Immediate acceptance target |
|---|---|---|
| WP0 | repository-wide initialization | structure exists and unit tests run |
| WP2 | `theory/` | L0-L2 draft statements with exact checks |
| WP3 | `src/model.py`, `src/probes.py`, `tests/` | exact M0 recovery core; Qiskit ISA checks remain open |

The canonical cross-WP interfaces live in `src/types.py`. Later changes require
a handoff note.

