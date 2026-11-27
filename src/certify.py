"""Three-outcome certification from an already-valid gamma interval."""

from dataclasses import dataclass
from enum import Enum
from math import isfinite

from itertools import product

from .decision import (
    Candidate,
    EdgeError,
    MaxCutInstance,
    decision_gap,
    exact_expected_cut,
    signed_gap,
    signed_gap_per_candidate,
)


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


def gamma_interval_per_candidate(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    first_centers: tuple[EdgeError, ...],
    first_radii: tuple[EdgeError, ...],
    second_centers: tuple[EdgeError, ...],
    second_radii: tuple[EdgeError, ...],
    confidence: float,
) -> GammaInterval:
    """Conservative gamma interval with separate residual boxes per candidate.

    Each candidate expectation is `edges`-Lipschitz in every residual angle
    under the L1 norm (same argument as `gamma_interval_from_error_box`), so
    the gap radius is `edges * (R_first + R_second)`. With identical boxes this
    reduces to the existing `2 * edges * R`.
    """
    totals = []
    for radii in (first_radii, second_radii):
        if len(radii) != len(instance.edges):
            raise ValueError("one radius triple is required per edge")
        total = 0.0
        for radius in radii:
            values = (radius.epsilon, radius.local_left, radius.local_right)
            if any(value < 0.0 or not isfinite(value) for value in values):
                raise ValueError("error radii must be finite and non-negative")
            total += sum(values)
        totals.append(total)
    center = signed_gap_per_candidate(instance, first, second, first_centers, second_centers)
    radius = len(instance.edges) * (totals[0] + totals[1])
    return GammaInterval(center - radius, center + radius, confidence)


def _expectation_range(instance, candidate, centers, radii, points):
    """Valid [min, max] of one candidate's expected cut over a residual box.

    Grid evaluation plus a Lipschitz remainder: the expectation is
    `edges`-Lipschitz in every residual angle under the L1 norm, and every
    point of the box lies within half a grid cell of a grid point in each
    coordinate, so the remainder is edges * sum(half cell widths) [theory, draft].
    """
    axes, half_cells = [], 0.0
    for center, radius in zip(centers, radii):
        for c, r in ((center.epsilon, radius.epsilon), (center.local_left, radius.local_left),
                     (center.local_right, radius.local_right)):
            if r < 0.0 or not isfinite(r):
                raise ValueError("error radii must be finite and non-negative")
            if r == 0.0 or points == 1:
                axes.append((c,))
                half_cells += r
            else:
                step = 2.0 * r / (points - 1)
                axes.append(tuple(c - r + step * i for i in range(points)))
                half_cells += 0.5 * step
    values = []
    for flat in product(*axes):
        errors = tuple(EdgeError(*flat[3 * e: 3 * e + 3]) for e in range(len(instance.edges)))
        values.append(exact_expected_cut(instance, candidate, errors))
    remainder = len(instance.edges) * half_cells
    return min(values) - remainder, max(values) + remainder


def gamma_interval_grid_bound(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    first_centers: tuple[EdgeError, ...],
    first_radii: tuple[EdgeError, ...],
    second_centers: tuple[EdgeError, ...],
    second_radii: tuple[EdgeError, ...],
    confidence: float,
    points: int = 5,
) -> GammaInterval:
    """Gamma interval from per-candidate box optimization (tighter, still valid).

    The two candidates' residual boxes are independent, so
    min gamma = sigma-signed (min f_first - max f_second) and likewise for the
    maximum. Each range is bounded by `_expectation_range`. With points=1 this
    reproduces gamma_interval_per_candidate.
    """
    if points < 1:
        raise ValueError("points must be at least 1")
    ideal = decision_gap(instance, first, second)
    if ideal == 0.0:
        raise ValueError("the ideal decision must not be tied")
    lo1, hi1 = _expectation_range(instance, first, first_centers, first_radii, points)
    lo2, hi2 = _expectation_range(instance, second, second_centers, second_radii, points)
    if ideal > 0.0:
        lower, upper = lo1 - hi2, hi1 - lo2
    else:
        lower, upper = lo2 - hi1, hi2 - lo1
    return GammaInterval(lower, upper, confidence)
