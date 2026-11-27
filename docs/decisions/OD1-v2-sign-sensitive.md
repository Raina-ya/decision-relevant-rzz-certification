# OD1 v2 - Add a sign-sensitive 2-qubit instance

- Date: 2026-11-27. Status: development decision under the owner's
  delegation (OD10); binding only through a later freeze manifest.
- Problem: C7 showed that the original 2-qubit hardware-primary instance has
  no equal-fidelity witness within |e| <= 0.6, so it cannot show why an
  average metric is insufficient.
- Decision: keep `path-2q` as the robust control and add `path-2q-sign`
  (`analysis/tolerance/instances_sign_sensitive.json`), found by
  `analysis/tolerance/find_sign_sensitive.py`. Both of its RZZ angles
  (pi/16, pi/8) are measured on pair A by HW-P2, so the hardware scope stays
  one pair.
- Witness [exact]: eps = +0.28 gives gamma = 0.315 (harmless, margin 0.075);
  eps = -0.28 gives gamma = -0.026 (harmful); both have average gate
  fidelity 0.98442.
- 3- and 4-qubit paths remain [exact]/[sim] extensions; `path-3q` is also
  evaluated by HW-P2 through pair B.
