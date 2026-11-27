"""Three-outcome certification from an already-valid gamma interval."""

from dataclasses import dataclass
from enum import Enum
from math import isfinite


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

