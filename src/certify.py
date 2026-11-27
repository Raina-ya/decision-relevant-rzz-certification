"""Three-outcome certification from an already-valid gamma interval."""

from dataclasses import dataclass
from enum import Enum
from math import isfinite

from .decision import Candidate, EdgeError, MaxCutInstance, signed_gap


class Verdict(str, Enum):
    HARMLESS = "harmless"
    HARMFUL = "harmful"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class GammaInterval:
    lower: float
    upper: float
    confidence: float

    def __post_init__(self) -> None:
        if not isfinite(self.lower) or not isfinite(self.upper):
            raise ValueError("gamma bounds must be finite")
        if self.lower > self.upper:
            raise ValueError("lower bound cannot exceed upper bound")
        if not 0.0 < self.confidence < 1.0:
            raise ValueError("confidence must lie in (0, 1)")


def certify(interval: GammaInterval, margin: float) -> Verdict:
    """Apply the prespecified three-outcome rule [theory, draft]."""
    if margin < 0.0:
        raise ValueError("margin must be non-negative")
    if interval.lower >= margin:
        return Verdict.HARMLESS
    if interval.upper < 0.0:
        return Verdict.HARMFUL
    return Verdict.INCONCLUSIVE


def gamma_interval_from_error_box(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    centers: tuple[EdgeError, ...],
    radii: tuple[EdgeError, ...],
    confidence: float,
) -> GammaInterval:
    """Project a simultaneous M0 error box to a conservative gamma interval.

    For a MaxCut observable with operator norm at most the number of edges,
    each unitary angle derivative of one candidate expectation is bounded by
    that norm. A gap between two candidates is therefore `2 * edges` Lipschitz
    in every angle under the L1 norm. This is deliberately conservative.
    """
    if len(centers) != len(instance.edges) or len(radii) != len(instance.edges):
        raise ValueError("one center and radius triple is required per edge")
    total_radius = 0.0
    for radius in radii:
        values = (radius.epsilon, radius.local_left, radius.local_right)
        if any(value < 0.0 or not isfinite(value) for value in values):
            raise ValueError("error radii must be finite and non-negative")
        total_radius += sum(values)
    center = signed_gap(instance, first, second, centers)
    gap_radius = 2.0 * len(instance.edges) * total_radius
    return GammaInterval(center - gap_radius, center + gap_radius, confidence)
