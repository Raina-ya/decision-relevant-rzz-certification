"""Finite-sample confidence sets for four-phase probe measurements."""

from dataclasses import dataclass
from math import asin, atan2, hypot, log, pi, sqrt


@dataclass(frozen=True, slots=True)
class BinomialCount:
    zeros: int
    shots: int

    def __post_init__(self) -> None:
        if self.shots <= 0:
            raise ValueError("shots must be positive")
        if not 0 <= self.zeros <= self.shots:
            raise ValueError("zeros must lie between zero and shots")

    @property
    def signed_mean(self) -> float:
        return 2.0 * self.zeros / self.shots - 1.0


@dataclass(frozen=True, slots=True)
class CircularInterval:
    """A connected circular interval, or the full circle when radius is pi."""

    center: float
    radius: float
    confidence: float

    def contains(self, angle: float, tolerance: float = 1e-12) -> bool:
        distance = abs((angle - self.center + pi) % (2.0 * pi) - pi)
        return distance <= self.radius + tolerance


@dataclass(frozen=True, slots=True)
class PhaseEstimate:
    x: float
    y: float
    phase: float
    confidence_interval: CircularInterval
    signed_mean_radius: float


def hoeffding_signed_mean_radius(shots: int, alpha: float, comparisons: int = 4) -> float:
    """Two-sided Hoeffding radius with a union bound over `comparisons` means."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    if comparisons <= 0:
        raise ValueError("comparisons must be positive")
    return sqrt(2.0 * log(2.0 * comparisons / alpha) / shots)


def four_phase_confidence(
    counts: tuple[BinomialCount, BinomialCount, BinomialCount, BinomialCount],
    alpha: float,
) -> PhaseEstimate:
    """Construct a finite-sample valid phase confidence interval.

    Validity uses a two-sided Hoeffding bound for each of the four signed
    means, followed by a union bound and deterministic projection of the
    resulting rectangle to an angular interval. Unequal shot counts use the
    largest component radius.
    """
    means = tuple(count.signed_mean for count in counts)
    component_radius = max(
        hoeffding_signed_mean_radius(count.shots, alpha, comparisons=4)
        for count in counts
    )
    x = 0.5 * (means[0] - means[2])
    y = 0.5 * (means[1] - means[3])
    center = atan2(y, x)
    vector_radius = sqrt(2.0) * component_radius
    norm = hypot(x, y)
    angular_radius = pi if norm <= vector_radius else asin(min(1.0, vector_radius / norm))
    interval = CircularInterval(center, angular_radius, 1.0 - alpha)
    return PhaseEstimate(x, y, center, interval, component_radius)

