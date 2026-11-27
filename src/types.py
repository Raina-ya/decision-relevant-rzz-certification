"""Frozen initial interfaces between circuit, estimation, and decision WPs."""

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class CircuitKind(str, Enum):
    PROBE = "probe"
    DELAY = "delay"
    ZERO = "k_zero"
    READOUT = "readout"
    ANCHOR = "anchor"


@dataclass(frozen=True, slots=True)
class ProbeKey:
    theta: float
    k: int
    control: int
    role: int
    analysis_phase: float
    circuit_kind: CircuitKind = CircuitKind.PROBE


@dataclass(frozen=True, slots=True)
class ProbeCounts:
    key: ProbeKey
    counts: Mapping[str, int]
    circuit_hash: str


@dataclass(frozen=True, slots=True)
class DecisionFunctional:
    """Values needed by the estimation WP without owning decision internals."""

    ideal_sign: int
    margin: float
    gradient: tuple[float, ...]
    hessian: tuple[tuple[float, ...], ...]

