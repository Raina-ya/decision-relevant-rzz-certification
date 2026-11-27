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
from src.types import ProbeKey

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


PLANS_P3: dict[str, tuple[ParallelBlock, ...]] = {
    "A": (
        parallel_block("P3A1-parallel-0.612", DECISION_2Q[0], 1000, "all pairs at the path-2q angle; context versus HW-P2"),
        parallel_block("P3A2-parallel-pi16", SIGN_2Q[0], 1000, "all pairs at the sign-sensitive angle pi/16"),
    ),
    "B": (
        parallel_block("P3B1-parallel-1.348", DECISION_2Q[1], 1000, "all pairs at the second path-2q angle"),
        parallel_block("P3B2-parallel-pi8", SIGN_2Q[1], 1000, "all pairs at the sign-sensitive angle pi/8"),
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
