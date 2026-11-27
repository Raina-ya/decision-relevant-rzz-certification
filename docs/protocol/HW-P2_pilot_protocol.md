# HW-P2 exploratory hardware pilot protocol

Status: prespecified under an internal lock (the approved commit named in
`docs/decisions/HW-P2-approval.json`). Not preregistered. Exploratory: it does
not replace G3, G4 or the confirmatory G5 run.

## Why a pilot now

- G0 needs real platform evidence: does `use_fractional_gates=True` expose a
  bounded `rzz` on the selected pair, with what duration, and do ISA circuits
  survive without folding or merging?
- G3 needs real effect sizes and visibilities; G2.5 needs real diagnostic
  base rates. The pilot supplies both without touching the confirmatory data.
- The owner has quota that expires at the end of the current cycle
  (2026-11-27 UTC) on one account and a second account available.

## What the pilot may and may not claim

| May report | May not report |
|---|---|
| Finite-sample M0 boxes per (pair, angle) on this backend at this time | that the gate is reliable in general |
| Diagnostic outcomes (Z conservation, unwrap status) | a physical cause of any residual |
| Pilot certificates for the development instances, labelled exploratory | confirmatory harmless/harmful findings |
| Direct decision-circuit gaps, native versus CZ-decomposed | that native is better or worse in general |
| Measured QPU seconds per shot | budgets for other backends |

All numbers carry `[hardware-locked, exploratory pilot HW-P2]`.

## Layout

A 3-qubit chain q0-q1-q2 chosen by `select_chain` in `hardware/run_hw_p2.py`:
minimum of the summed reported `rzz` error on both edges plus readout error on
the three qubits, from the target at selection time. Pair A = (q0, q1),
pair B = (q1, q2). Account A selects and records the chain in
`results/hw_p2/A/selection.json`; account B reuses it unchanged.

## Design

Defined in `hardware/hw_p2_design.py`; blocks run in this priority order and
the runner stops before any block whose estimated cost would exceed the
`--max-qpu-seconds` cap.

| Account | Block | Content | Circuits x shots |
|---|---|---|---|
| A | A0 | readout, k=0 references, theta=pi/4 at k in {1,16}; timing | 68 x 500 |
| A | A1 | pair A at the 2q decision angles, k = 1..64, delay controls, 8 anchors | 364 x 1000 |
| A | A5 | 2q decision circuits, native RZZ and CZ-decomposed | 4 x 20000 |
| A | A2 | pair A at the 3q decision angles | 364 x 1000 |
| A | A7 | T1 reference: control in |1>, delay only, k = 1..64 (added after the first A run) | 60 x 1000 |
| A | A3 | pair A at grid angles pi/4, 3pi/8, pi/2 | 532 x 500 |
| B | B0 | as A0 on pair B | 68 x 500 |
| B | B5 | T1 reference on pair B | 60 x 1000 |
| B | B2 | cross-account replication of A1 on pair A | 364 x 1000 |
| B | B1 | pair B at the 3q decision angles | 364 x 1000 |
| B | B3 | 3q decision circuits on the chain, native and CZ | 4 x 20000 |
| B | B4 | pair B at five grid angles | 868 x 500 |

Circuit order inside each block is randomized with a fixed seed. Sampler
options: dynamical decoupling off, gate and measurement twirling off (twirling
is not available for fractional gates). Each block is split into jobs of at
most 290 circuits.

## Prespecified analysis

`analysis/hardware/analyze_hw_p2.py`, validated on synthetic data in
`tests/test_hw_p2_analysis.py` (noise model in
`analysis/hardware/simulate_hw_p2.py`). Choices fixed in its module docstring:
alpha = 0.05 per (pair, angle) with Bonferroni over all phase intervals, k=0
offset subtraction, interval unwrapping without forced branch choice,
Z-conservation threshold, and `gamma_interval_per_candidate` for verdicts.

## Run rules

- Account A runs first. Account B starts after A has written
  `selection.json`, preferably at least one hour later (drift information).
- A failed or cancelled job is rerun with the same script and seed; a block
  file that exists is never overwritten.
- No rerun because a result looks unexpected.
- Job IDs stay in `hardware/private/` (git-ignored) until the owner clears
  them.
- Deviations are logged in `docs/protocol/deviations.md`.

## Amendment 1 (2026-11-27, after account A blocks A0-A2, A5, A6)

Account A's prespecified Z-conservation diagnostic triggered only for
control = 1 at k = 64. Because the diagnostic cannot distinguish idle
relaxation of the control from gate-induced flips, blocks A7 and B5 add a
delay-only reference with the control in |1> at the same elapsed times, and
`control_flip_comparison` reports probe minus delay flip rates. This is a
result-informed addition: it is labelled as such, it does not change any
existing block, threshold or verdict rule, and the A results already
recorded are analysed exactly as before. Logged in deviations.md.
