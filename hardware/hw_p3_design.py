"""HW-P3: chip-wide parallel probes (exploratory, follows HW-P2).

Every circuit applies the same probe key simultaneously to a fixed matching of
disjoint RZZ pairs, so one circuit characterizes all pairs at once and the
spectators of each pair are active (context differs from HW-P2's isolated
pair). Pair (53, 54) is forced into the matching so its parallel-context
residuals can be compared with HW-P2's isolated ones.

Outputs carry [hardware-locked, exploratory pilot HW-P3].
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi

from hardware.hw_p2_design import DECISION_2Q, SIGN_2Q, angle_keys, zero_keys
from src.probes import ANALYSIS_PHASES
from src.types import CircuitKind, ProbeKey

KS_P3 = (1, 2, 4, 8, 16, 32)  # k = 64 dropped: HW-P2 showed M0 breaks there on q53
FORCED_PAIR = (53, 54)
SEED = 20261128


@dataclass(frozen=True, slots=True)
class ParallelBlock:
    name: str
    keys: tuple[ProbeKey, ...]
    shots: int
    purpose: str


def parallel_block(name: str, theta: float, shots: int, purpose: str) -> ParallelBlock:
    return ParallelBlock(name, angle_keys((theta,), KS_P3) + zero_keys(), shots, purpose)


def parallel_t1_reference(name: str, shots: int) -> ParallelBlock:
    """Control in |1>, equal-duration delay instead of RZZ on every pair (no RZZ).

    Added after HW-P3's first four blocks: Z conservation triggered on about
    60% of pairs, and HW-P2 showed part of such triggers is idle relaxation.
    Control flips here versus the probe blocks at equal k separate the two.
    Taken hours after the probe blocks, so drift between them is possible.
    """
    keys = tuple(
        ProbeKey(DECISION_2Q[0], k, 1, role, phase, CircuitKind.DELAY)
        for k in KS_P3
        for role in (1, 2)
        for phase in ANALYSIS_PHASES
    )
    return ParallelBlock(name, keys, shots, "chip-wide T1 reference for the Z-conservation diagnostic")


PLANS_P3: dict[str, tuple[ParallelBlock, ...]] = {
    "A": (
        parallel_block("P3A1-parallel-0.612", DECISION_2Q[0], 1000, "all pairs at the path-2q angle; context versus HW-P2"),
        parallel_block("P3A2-parallel-pi16", SIGN_2Q[0], 1000, "all pairs at the sign-sensitive angle pi/16"),
    ),
    "B": (
        parallel_block("P3B1-parallel-1.348", DECISION_2Q[1], 1000, "all pairs at the second path-2q angle"),
        parallel_block("P3B2-parallel-pi8", SIGN_2Q[1], 1000, "all pairs at the sign-sensitive angle pi/8"),
        parallel_t1_reference("P3B3-parallel-t1-reference", 2200),
    ),
}


def select_matching(target, forced=FORCED_PAIR) -> tuple[tuple[int, int], ...]:
    """Deterministic greedy matching of disjoint rzz pairs by ascending reported error.

    Pairs without a reported rzz error or with a readout error above 0.05 on
    either qubit are excluded. The forced pair is taken first.
    """
    rzz, measure = target["rzz"], target["measure"]

    def readout(q):
        props = measure.get((q,))
        return None if props is None else props.error

    edges = {}
    for (a, b), props in rzz.items():
        if props is None or props.error is None:
            continue
        key = (min(a, b), max(a, b))
        edges[key] = min(edges.get(key, 1.0), float(props.error))
    used: set[int] = set()
    chosen = []
    ordered = sorted(edges.items(), key=lambda item: (item[1], item[0]))
    if forced in edges:
        ordered = [(forced, edges[forced])] + [item for item in ordered if item[0] != forced]
    for (a, b), _err in ordered:
        if a in used or b in used:
            continue
        ra, rb = readout(a), readout(b)
        if ra is None or rb is None or ra > 0.05 or rb > 0.05:
            continue
        chosen.append((a, b) if (a, b) != forced[::-1] else forced)
        used.update((a, b))
    return tuple(chosen)
