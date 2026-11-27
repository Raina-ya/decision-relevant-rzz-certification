# Research-gap map after library expansion

Status: WP1 working document, 2026-11-27. Based on 142 library entries
(19 papers read at relevant-section level or deeper, three documentation pages
reviewed, 108 abstract-only and 12 bibliographic-only). G1
remains open; nothing here is a novelty claim. Wording follows AGENTS.md
Section 2: no "first" or "novel".

## 1. Feature matrix of the closest prior work

Legend: Y = present, P = partial, N = absent, ? = not yet verified in full text.

| Source | Native fractional / continuous angle family | Works without twirling | Strict finite-sample validity | Tolerance induced by a downstream decision | Three outcomes | Model rejection kept separate | Off-diagonal diagnostic | Delay/reference controls for frame phase | Lower bound on cost | Hardware |
|---|---|---|---|---|---|---|---|---|---|---|
| RUDINGER2025 (RPE of ZI/IZ/ZZ) | N (CZ) | Y | N | N | N | P (consistency) | N | ? | N | Y |
| CHAI2026 (branch-resolved Pauli block) | N (CZ) | Y | N (bootstrap) | N | N | N | N | N | N | Y (pulse level) |
| DENG2026 (structured diagonal learning) | P (C^mZ phases) | Y | N (asymptotic) | N (user tolerance) | Y | Y | N (stated limitation) | P (equal-duration reference) | N (stated) | N |
| MIKLIN2026 (sound gate certification) | N (sqrt-X) | Y | Y | N | P | N | N | N | P | Y |
| ZHANG2021 (gate verification) | N | ? | Y | N | N | N | N | N | Y (scaling) | Y |
| SHAFFER2022 (continuous-gate verification) | Y | P | P | N | N | N | N | N | P | Y |
| MORELLI2026 (sequential parameter testing) | general | n/a | N (asymptotic threshold) | N (acceptable neighbourhood) | Y | N | N | n/a | Y (expected cost) | N |
| MILAZZO2023 (functional testing) | general | n/a | P | N (producer specs) | N (accept/reject) | N | N | n/a | N | N |
| SCAVINO2026 (QEM decision risk) | N | n/a | N (Gaussian) | Y (selection decision) | N | N | N | n/a | P (KL/Fisher converse) | P |
| BARRON2024 (provable output bounds) | N | N (layer fidelity, twirled) | Y | P (output value, not decision) | N | N | N | n/a | N | Y (IBM) |
| QUIROZ2021 (QAOA precision errors) | n/a | n/a | n/a (deterministic bounds) | P (output error) | N | N | N | n/a | N | N |
| Ch4 target | Y (native RZZ on Heron) | Y (required) | Y | Y | Y | Y | Y (Z conservation) | Y | Y (candidate) | Y (planned) |

## 2. Gap statements (each must survive G1)

- **G-A Twirl-free regime.** Fractional gates on IBM cannot be Pauli-twirled
  (IBM-FRACTIONAL). Twirling underpins RB-type, cycle-benchmarking,
  layer-fidelity and Clifford-proxy guarantees (ERHARD2019, MCKAY2023LF,
  MERKEL2025). Coherent residuals are exactly what averaged metrics hide
  (KUENG2016, SANDERS2016). IBM reports an angle-averaged RZZ error
  (IBM-QPU-INFO). Gap: certification of a coherent, angle-specific residual
  where the standard averaging toolchain is unavailable.
- **G-B Decision-induced tolerance.** Gate-certification works use generic
  fidelity thresholds (MIKLIN2026, ZHANG2021), producer specifications
  (MILAZZO2023) or user-specified tolerances (DENG2026). Decision-aware work
  (SCAVINO2026) targets QEM estimators, not gate residuals. Gap: a tolerance
  set derived from a nonlinear downstream decision functional of the
  measured gate residual.
- **G-C End-to-end finite-sample validity.** The closest probe papers report
  bootstrap (CHAI2026) or asymptotic (DENG2026) uncertainty. Gap: a verdict
  whose error probability is bounded for every shot budget, including the
  phase-unwrapping and functional-projection steps (CHRISTANDL2012,
  SUGIYAMA2015 and WAUDBYSMITH2024 supply tools, not this chain).
- **G-D Lower bound for the decision projection.** DENG2026 states it has no
  minimax lower bound; MORELLI2026 analyses expected sequential cost.
  Gap: a two-point (Le Cam / Bretagnolle-Huber) lower bound for certifying
  the decision projection with this probe family, matching the upper bound
  up to constants.
- **G-E Angle dependence.** Continuous-gate residuals vary with angle
  (YALE2025: light shift linear in theta; SCARATO2025; YALE2024).
  Gap: per-angle certificates and a quantified rule for when a certificate at
  probed angles transfers to unprobed decision angles.
- **G-F Model-adequacy diagnostics with error control.** DENG2026 separates
  model rejection but cannot represent off-diagonal error; RUSSO2020 offers
  RPE consistency checks. Gap: finite-sample diagnostics (Z conservation,
  k-linearity, visibility curvature) whose false-trigger rate is allocated
  in advance and whose trigger forces a prespecified verdict.
- **G-G Public-cloud, no-pulse setting.** CHAI2026 uses pulse-level access on
  one pair once. Gap: a protocol that runs with only ISA circuits and virtual Z
  on a public platform, with replication (G6).
- **G-H Platform evidence of a problem.** Independent users report fractional
  RZZ behaving worse than expected (RYBOTYCKI2025, to be confirmed in full
  text) while many recent works rely on it without gate-specific evidence
  (MONTANEZBARRERA2025, HUNG2025, WANG2025LCQAOA, AWUAH2026).

## 3. Candidate contribution statement (to replace README Section "What is and is not new")

> Ch4 asks whether a coherent residual of IBM Heron's native fractional RZZ
> gate, which twirling-based and angle-averaged metrics cannot resolve, can be
> certified as harmless or harmful for a prespecified downstream decision
> with an error probability that is bounded at every shot budget, and how
> many shots that requires at minimum.

Building blocks that are prior art and must be cited, not claimed: the
diagonal ZI/IZ/ZZ model and its RPE identifiability (RUDINGER2025), the
control-branch slope separation (CHAI2026), three-outcome equivalence logic
(SCHUIRMANN1987, BERGER1996, LAKENS2017, EGGERS2026, DENG2026), readout
symmetrization (SMITH2021, VANDENBERG2022TREX), decision-risk framing
(SCAVINO2026).

## 4. A cheap, high-value new result to attempt (candidate C7)

**Average-metric insufficiency for decisions.** Construct two RZZ residuals
with identical angle-averaged (twirled) fidelity whose induced QAOA decisions
differ, and characterize the set of such pairs. This turns the motivating
claim of G-A and G-H into a proposition with an explicit construction, which
the AGENTS.md rules require for any non-identifiability statement. It reuses
`src/decision.py` and needs no hardware.

## 5. Open problems that extend beyond Ch4 (candidate Ch5 directions)

| Direction | Open problem | Entry points in the library | Reuses from Ch4 |
|---|---|---|---|
| Certificate lifetime | How long does a certificate stay valid under drift; when to re-certify without losing alpha control | PROCTOR2020DRIFT, HOWARD2021, RAMDAS2023, CHEN2026SCREEN, DASGUPTA2024 | probes, finite-sample intervals, receipts |
| Angle transfer | Certified interpolation from probed to unprobed angles | YALE2025, SCARATO2025, LAZAR2022 | M1/M2 lack-of-fit tests |
| Context transfer | Probe context (spectators idle) versus decision context | SAROVAR2020, SUNDARESAN2020, ZHAO2022, Ch3 sensor offset | Z-conservation diagnostic |
| Decision-aware probe design | c-optimal or two-stage adaptive allocation of shots across angles and depths | GRANADE2012, SCAVINO2026, MILAZZO2023 | Fisher analysis, N* bounds |
| Tighter strict intervals | Replace Hoeffding with betting or exact intervals while keeping validity | WAUDBYSMITH2024, CLOPPER1934, BROWN2001 | src/estimate.py |
| Layer-level certification | Joint certificate for a full cost layer on many pairs | MCKAY2023LF, PROCTOR2022CAP | R-functional |
| Decision-theoretic alternative | Expected-loss formulation as a secondary analysis | LINDLEY1998 | decision functional |

## 6. Remaining review work

- Read CHAI2026 Sections on echo variants and DENG2026 decision rule in
  full; confirm RYBOTYCKI2025's RZZ statement in full text.
- Read arXiv:2611.20613 (blocked by rate limiting on 2026-11-27).
- Forward-citation pass on RUDINGER2025, CHAI2026 and DENG2026.
- Upgrade at least 30 core entries from abstract-only to relevant-sections
  read before G1.
