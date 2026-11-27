"""Finite-sample confidence sets for four-phase probe measurements."""

from dataclasses import dataclass
from enum import Enum
from math import asin, atan2, ceil, floor, hypot, log, pi, sqrt


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


@dataclass(frozen=True, slots=True)
class LinearInterval:
    lower: float
    upper: float

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise ValueError("lower cannot exceed upper")

    def contains(self, value: float, tolerance: float = 1e-12) -> bool:
        return self.lower - tolerance <= value <= self.upper + tolerance

    def intersection(self, other: "LinearInterval") -> "LinearInterval | None":
        lower, upper = max(self.lower, other.lower), min(self.upper, other.upper)
        return None if lower > upper else LinearInterval(lower, upper)


class UnwrapStatus(str, Enum):
    IDENTIFIED = "identified"
    AMBIGUOUS = "ambiguous"
    INCONSISTENT = "inconsistent"


@dataclass(frozen=True, slots=True)
class UnwrapResult:
    interval: LinearInterval
    status: UnwrapStatus
    last_k: int


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


def unwrap_phase_intervals(
    observations: tuple[tuple[int, CircularInterval], ...],
    prior: LinearInterval = LinearInterval(-pi, pi),
) -> UnwrapResult:
    """Sequentially unwrap intervals for observations of `k * slope` modulo 2pi.

    The routine refines only when exactly one branch intersects the current
    interval. It never resolves ambiguity by selecting a closest point.
    """
    current = prior
    last_k = 0
    for k, circular in sorted(observations, key=lambda item: item[0]):
        if k <= 0 or k <= last_k:
            raise ValueError("k values must be positive and unique")
        last_k = k
        if circular.radius >= pi:
            continue
        n_min = ceil((k * current.lower - circular.center - circular.radius) / (2.0 * pi))
        n_max = floor((k * current.upper - circular.center + circular.radius) / (2.0 * pi))
        intersections: list[LinearInterval] = []
        for branch in range(n_min, n_max + 1):
            candidate = LinearInterval(
                (circular.center - circular.radius + 2.0 * pi * branch) / k,
                (circular.center + circular.radius + 2.0 * pi * branch) / k,
            )
            overlap = current.intersection(candidate)
            if overlap is not None:
                intersections.append(overlap)
        if not intersections:
            return UnwrapResult(current, UnwrapStatus.INCONSISTENT, k)
        if len(intersections) > 1:
            return UnwrapResult(current, UnwrapStatus.AMBIGUOUS, k)
        current = intersections[0]
    return UnwrapResult(current, UnwrapStatus.IDENTIFIED, last_k)


@dataclass(frozen=True, slots=True)
class M0Interval:
    epsilon: LinearInterval
    a: LinearInterval
    b: LinearInterval


def recover_m0_intervals(
    role1_control0: LinearInterval,
    role1_control1: LinearInterval,
    role1_delay: LinearInterval,
    role2_control0: LinearInterval,
    role2_control1: LinearInterval,
    role2_delay: LinearInterval,
) -> M0Interval:
    """Map simultaneous slope intervals to an M0 parameter box."""
    epsilon_1 = LinearInterval(
        0.5 * (role1_control0.lower - role1_control1.upper),
        0.5 * (role1_control0.upper - role1_control1.lower),
    )
    epsilon_2 = LinearInterval(
        0.5 * (role2_control0.lower - role2_control1.upper),
        0.5 * (role2_control0.upper - role2_control1.lower),
    )
    epsilon = epsilon_1.intersection(epsilon_2)
    if epsilon is None:
        raise ValueError("role-specific epsilon intervals are inconsistent")
    a = LinearInterval(
        0.5 * (role1_control0.lower + role1_control1.lower) - role1_delay.upper,
        0.5 * (role1_control0.upper + role1_control1.upper) - role1_delay.lower,
    )
    b = LinearInterval(
        0.5 * (role2_control0.lower + role2_control1.lower) - role2_delay.upper,
        0.5 * (role2_control0.upper + role2_control1.upper) - role2_delay.lower,
    )
    return M0Interval(epsilon, a, b)
