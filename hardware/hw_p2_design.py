"""Prespecified design for hardware pilot HW-P2 (exploratory, two accounts).

HW-P2 is an exploratory pilot, not the confirmatory G5 run. Its outputs are
labelled [hardware-locked, exploratory] and may calibrate G3 effect sizes and
G2.5 thresholds; the confirmatory run must use fresh data.

Layout: a 3-qubit chain q0-q1-q2 chosen by `select_chain`. Pair A = (q0, q1),
pair B = (q1, q2). Account A characterizes pair A; account B characterizes
pair B, replicates pair A at the 2-qubit decision angles, and runs the 3-qubit
decision circuits.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi

from src.probes import ANALYSIS_PHASES
from src.types import CircuitKind, ProbeKey

# Decision angles of the unlocked development family (analysis/tolerance).
DECISION_2Q = (0.6118624420100085, 1.347950023138716)
DECISION_3Q = (1.5057887057410613, 0.5647605185118689)
GRID = (pi / 16, pi / 8, pi / 4, 3 * pi / 8, pi / 2)
KS = (1, 2, 4, 8, 16)
DEEP_KS = (32, 64)
KS_FULL = KS + DEEP_KS  # deep k narrows boxes ~2.5x at equal shots [sim]
ANCHOR = ProbeKey(DECISION_2Q[0], 4, 0, 1, 0.0, CircuitKind.ANCHOR)
ANCHOR_REPEATS = 8
SEED = 20261127


@dataclass(frozen=True, slots=True)
class Block:
    name: str
    pair: str  # "A", "B" or "chain"
    kind: str  # "probe" or "decision"
    keys: tuple[ProbeKey, ...]
    readout_qubits: int
    shots: int
    purpose: str


def angle_keys(thetas: tuple[float, ...], ks: tuple[int, ...]) -> tuple[ProbeKey, ...]:
    keys = []
    for theta in thetas:
        for k in ks:
            for role in (1, 2):
                for phase in ANALYSIS_PHASES:
                    for control in (0, 1):
                        keys.append(ProbeKey(theta, k, control, role, phase))
                    keys.append(ProbeKey(theta, k, 0, role, phase, CircuitKind.DELAY))
    return tuple(keys)


def zero_keys() -> tuple[ProbeKey, ...]:
    return tuple(
        ProbeKey(pi / 4, 0, control, role, phase, CircuitKind.ZERO)
        for control in (0, 1)
        for role in (1, 2)
        for phase in ANALYSIS_PHASES
    )


def characterization(name, pair, thetas, ks, shots, purpose, anchors=True) -> Block:
    keys = angle_keys(thetas, ks) + zero_keys()
    if anchors:
        keys += (ANCHOR,) * ANCHOR_REPEATS
    return Block(name, pair, "probe", keys, 2, shots, purpose)


def calibration(name, pair) -> Block:
    keys = zero_keys() + angle_keys((pi / 4,), (1, 16))
    return Block(name, pair, "probe", keys, 2, 500, "G0 platform check and per-shot timing")


def decision(name, instance_id, shots=20000) -> Block:
    return Block(name, instance_id, "decision", (), 0, shots, "direct decision circuits, native and CZ-decomposed")


PLANS: dict[str, tuple[Block, ...]] = {
    "A": (
        calibration("A0-calibration", "A"),
        characterization("A1-decision-2q", "A", DECISION_2Q, KS_FULL, 1000, "residuals at 2q decision angles, k=1..64"),
        decision("A5-decision-circuits-2q", "path-2q"),
        characterization("A2-decision-3q-pairA", "A", DECISION_3Q, KS_FULL, 1000, "pair-A residuals at 3q decision angles"),
        characterization("A3-grid", "A", GRID, KS_FULL, 500, "angle dependence over the native range"),
    ),
    "B": (
        calibration("B0-calibration", "B"),
        characterization("B2-replicate-2q-pairA", "A", DECISION_2Q, KS_FULL, 1000, "cross-account replication of A1"),
        characterization("B1-decision-3q-pairB", "B", DECISION_3Q, KS_FULL, 1000, "pair-B residuals at 3q decision angles"),
        decision("B3-decision-circuits-3q", "path-3q"),
        characterization("B4-grid-pairB", "B", GRID, KS_FULL, 500, "angle dependence on pair B"),
    ),
}


def block_shots(block: Block) -> int:
    if block.kind == "decision":
        return 4 * block.shots
    readout = 2 ** block.readout_qubits
    return (len(block.keys) + readout) * block.shots


def plan_summary(label: str) -> list[dict]:
    return [
        {
            "block": block.name,
            "pair": block.pair,
            "circuits": (4 if block.kind == "decision" else len(block.keys) + 2**block.readout_qubits),
            "shots_per_circuit": block.shots,
            "total_shots": block_shots(block),
            "purpose": block.purpose,
        }
        for block in PLANS[label]
    ]
