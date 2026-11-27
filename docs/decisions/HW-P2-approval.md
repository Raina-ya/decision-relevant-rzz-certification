# HW-P2 hardware pilot approval

The machine-checked record is `HW-P2-approval.json`. It names the commit that
contains the runner, the runner's SHA-256 and the allowed backends.
`hardware/approval.py::verify_pilot_approval` refuses submission if any file
outside `docs/decisions/`, `results/`, `plan/handoffs/` or `hardware/private/`
changed after that commit, or if the runner hash differs.

Basis: the owner's chat authorization of 2026-11-27 (11:37 and 11:41 +08:00)
to run IBM Quantum hardware with the remaining quota on two accounts. The
owner runs the submission personally; no agent holds credentials. The scope
is the exploratory pilot only; G4 and the confirmatory run still require
their own approval.
