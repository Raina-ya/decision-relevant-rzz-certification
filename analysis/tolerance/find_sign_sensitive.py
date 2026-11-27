"""Search for a 2-qubit decision instance where the ZZ sign ambiguity bites.

Constraint: both RZZ angles are among the HW-P2 measured angles, so the pilot
data can evaluate the instance. Criterion: ideal |gap| >= 0.15, margin =
|gap|/2, and a pure-ZZ residual pair (+eps, -eps) with equal average gate
fidelity such that one is harmless (gamma >= m) and the other harmful
(gamma < 0), both by at least 0.02. Smallest eps on a 0.02 grid wins.
All outputs are [exact].
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.tolerance.average_metric import average_gate_fidelity
from hardware.hw_p2_design import DECISION_2Q, DECISION_3Q, GRID


def cut2(beta, theta, eps):
    zs = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    amps = [0.5 * np.exp(-0.5j * ((theta + eps) * z0 * z1)) for z0, z1 in zs]
    c, s = np.cos(beta), -1j * np.sin(beta)
    a0, a1, a2, a3 = amps
    a0, a1 = c * a0 + s * a1, s * a0 + c * a1
    a2, a3 = c * a2 + s * a3, s * a2 + c * a3
    a0, a2 = c * a0 + s * a2, s * a0 + c * a2
    a1, a3 = c * a1 + s * a3, s * a1 + c * a3
    return np.abs(a1) ** 2 + np.abs(a2) ** 2


def search(beta_points: int = 181, robustness: float = 0.02) -> dict:
    angles = np.array(sorted(set(GRID + DECISION_2Q + DECISION_3Q)))
    betas = np.linspace(-np.pi / 2, np.pi / 2, beta_points)
    b1, t1, b2, t2 = np.meshgrid(betas, angles, betas, angles, indexing="ij")
    g0 = cut2(b1, t1, 0.0) - cut2(b2, t2, 0.0)
    ok = (t1 != t2) & (np.abs(g0) >= 0.15)
    sign, margin = np.sign(g0), np.abs(g0) / 2
    for eps in np.arange(0.02, 0.42, 0.02):
        gp = sign * (cut2(b1, t1, eps) - cut2(b2, t2, eps))
        gm = sign * (cut2(b1, t1, -eps) - cut2(b2, t2, -eps))
        rob = np.maximum(np.minimum(gp - margin, -gm), np.minimum(gm - margin, -gp))
        rob = np.where(ok, rob, -np.inf)
        j = np.unravel_index(np.argmax(rob), rob.shape)
        if rob[j] >= robustness:
            eps = float(round(eps, 3))
            return {
                "instance_id": "path-2q-sign", "qubits": 2, "edges": [[0, 1]],
                "first_beta": float(b1[j]), "first_theta": float(t1[j]),
                "second_beta": float(b2[j]), "second_theta": float(t2[j]),
                "ideal_gap": float(g0[j]), "margin": float(abs(g0[j]) / 2), "attempts": 1,
                "scope": "hardware-primary-sign-sensitive", "evidence": "[exact]",
                "witness": {"eps": eps, "gamma_plus": float(gp[j]), "gamma_minus": float(gm[j]),
                            "robustness": float(rob[j]), "average_gate_fidelity": average_gate_fidelity((eps, 0.0, 0.0))},
            }
    raise RuntimeError("no sign-sensitive instance on the grid")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    record = search()
    payload = {"status": "unlocked-development", "rule": __doc__.strip().splitlines()[0],
               "search": "analysis/tolerance/find_sign_sensitive.py (beta grid 181, eps step 0.02)",
               "instances": [record]}
    (root / "analysis" / "tolerance" / "instances_sign_sensitive.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(record, indent=1))
