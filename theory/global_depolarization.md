# Global depolarization and decision ordering

Status: **[theory, draft]**.

For dimension `d`, global depolarization maps each candidate state to

`rho_i' = v rho_i + (1-v) I/d`.

For the same downstream observable `C`, the difference between two candidate
expectations is

`Tr[C(rho_1' - rho_2')] = v Tr[C(rho_1 - rho_2)]`.

Thus `v > 0` preserves the sign of the candidate gap. At `v = 0` every gap is
zero, so sign preservation is not claimed. This result does not cover local,
gate-dependent, or candidate-dependent noise and is not evidence that hardware
noise is globally depolarizing.

