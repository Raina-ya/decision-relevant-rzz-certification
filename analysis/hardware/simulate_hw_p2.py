"""Synthetic HW-P2 data for validating the prespecified analysis [sim].

Noise model (named, as AGENTS.md Section 3 requires): diagonal M0 residual
e(theta) = (eps0 + eps1*theta, a0 + a1*theta, b0), idle detuning, a fixed
reference offset, per-gate visibility lambda^k, symmetric-free readout
assignment errors (p01, p10) on the target bit, and a control flip rate.
No qiskit is needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi
import random

from hardware.hw_p2_design import Block
from src.model import M0Parameters, residual_phase
from src.types import CircuitKind, ProbeKey


@dataclass(frozen=True, slots=True)
class SimModel:
    eps0: float = 0.012
    eps1: float = -0.010
    a0: float = 0.020
    a1: float = 0.015
    b0: float = -0.018
    detuning_1: float = 2.0e4  # rad/s
    detuning_2: float = -1.5e4
    reference_offset: float = -pi / 2
    gate_seconds: float = 68e-9
    lam: float = 0.985
    p01: float = 0.015  # P(read 1 | 0)
    p10: float = 0.035  # P(read 0 | 1)
    control_flip: float = 0.004

    def residual(self, theta: float) -> tuple[float, float, float]:
        return (self.eps0 + self.eps1 * theta, self.a0 + self.a1 * theta, self.b0)


def _p_target_zero(model: SimModel, key: ProbeKey) -> float:
    epsilon, a, b = model.residual(key.theta)
    params = M0Parameters(epsilon, a, b, model.detuning_1, model.detuning_2,
                          model.reference_offset, model.reference_offset)
    psi = residual_phase(key, params, model.gate_seconds)
    visibility = model.lam ** key.k
    ideal_zero = 0.5 * (1.0 + visibility * cos(psi - key.analysis_phase))
    return ideal_zero * (1 - model.p01) + (1 - ideal_zero) * model.p10


def simulate_block(block: Block, chain: tuple[int, int, int], model: SimModel, seed: int) -> dict:
    rng = random.Random(seed)
    pair = [chain[0], chain[1]] if block.pair == "A" else [chain[1], chain[2]]
    records = []
    for key in block.keys:
        p0 = _p_target_zero(model, key)
        counts = {"00": 0, "01": 0, "10": 0, "11": 0}
        for _ in range(block.shots):
            target = 0 if rng.random() < p0 else 1
            control = key.control if rng.random() >= model.control_flip else 1 - key.control
            counts[f"{control}{target}"] += 1
        meta = {"type": "probe", "pair": pair, "theta": key.theta, "k": key.k, "control": key.control,
                "role": key.role, "analysis_phase": key.analysis_phase, "circuit_kind": key.circuit_kind.value}
        records.append({"meta": meta, "counts": counts})
    for state in range(4):
        counts = {"00": 0, "01": 0, "10": 0, "11": 0}
        for _ in range(block.shots):
            bits = []
            for bit in range(2):
                prepared = (state >> bit) & 1
                flip = model.p01 if prepared == 0 else model.p10
                bits.append(prepared ^ (rng.random() < flip))
            counts[f"{bits[1]}{bits[0]}"] += 1
        records.append({"meta": {"type": "readout", "prepared": state, "qubits": 2, "pair": pair}, "counts": counts})
    return {"schema": "hw-p2-block-v1", "evidence": "[sim]", "label": "sim", "block": block.name,
            "chain": list(chain), "shots": block.shots, "records": records}
