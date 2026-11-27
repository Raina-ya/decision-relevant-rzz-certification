"""Tolerance membership, conservative inner sets, and sampled radial crossings."""

from dataclasses import dataclass
from itertools import product
from math import isfinite

from src.decision import Candidate, EdgeError, MaxCutInstance, signed_gap


def in_tolerance_region(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    errors: tuple[EdgeError, ...],
    margin: float,
) -> bool:
    if margin < 0.0:
        raise ValueError("margin must be non-negative")
    return signed_gap(instance, first, second, errors) >= margin


def conservative_l1_inner_radius(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    margin: float,
) -> float:
    """Globally valid L1 radius around zero error under the draft bound."""
    ideal_gamma = signed_gap(instance, first, second)
    if ideal_gamma < margin:
        return 0.0
    return (ideal_gamma - margin) / (2.0 * len(instance.edges))


def conservative_equal_box_halfwidth(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    margin: float,
) -> float:
    dimensions = 3 * len(instance.edges)
    return conservative_l1_inner_radius(instance, first, second, margin) / dimensions


def inner_box_corners(edges: int, halfwidth: float) -> tuple[tuple[EdgeError, ...], ...]:
    """Enumerate corners for small-instance tests and audit artifacts."""
    if edges <= 0 or halfwidth < 0.0:
        raise ValueError("invalid box dimensions")
    corners = []
    for signs in product((-1.0, 1.0), repeat=3 * edges):
        corners.append(
            tuple(
                EdgeError(
                    signs[3 * edge] * halfwidth,
                    signs[3 * edge + 1] * halfwidth,
                    signs[3 * edge + 2] * halfwidth,
                )
                for edge in range(edges)
            )
        )
    return tuple(corners)


@dataclass(frozen=True, slots=True)
class RadialCrossing:
    direction: tuple[EdgeError, ...]
    scale: float
    gamma_inside: float
    gamma_outside: float
    bracket_steps: int
    tolerance: float
    status: str = "sampled-first-crossing"


def _scaled(direction: tuple[EdgeError, ...], scale: float) -> tuple[EdgeError, ...]:
    return tuple(
        EdgeError(
            scale * component.epsilon,
            scale * component.local_left,
            scale * component.local_right,
        )
        for component in direction
    )


def sampled_radial_crossing(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    margin: float,
    direction: tuple[EdgeError, ...],
    max_scale: float = 1.0,
    bracket_steps: int = 1000,
    tolerance: float = 1e-10,
) -> RadialCrossing | None:
    """Find the first sampled inside-to-outside bracket, then bisect it.

    This is a reproducible numerical diagnostic, not a proof that no earlier
    crossing occurs between grid points.
    """
    if len(direction) != len(instance.edges):
        raise ValueError("one direction triple is required per edge")
    norm = sum(
        abs(value)
        for component in direction
        for value in (component.epsilon, component.local_left, component.local_right)
    )
    if norm == 0.0 or not isfinite(norm):
        raise ValueError("direction must have finite nonzero L1 norm")
    if max_scale <= 0.0 or bracket_steps <= 0 or tolerance <= 0.0:
        raise ValueError("search controls must be positive")
    normalized = tuple(
        EdgeError(
            component.epsilon / norm,
            component.local_left / norm,
            component.local_right / norm,
        )
        for component in direction
    )
    zero_gamma = signed_gap(instance, first, second)
    if zero_gamma < margin:
        raise ValueError("zero error is outside the requested tolerance region")

    previous_scale, previous_gamma = 0.0, zero_gamma
    lower = upper = gamma_upper = None
    for step in range(1, bracket_steps + 1):
        scale = max_scale * step / bracket_steps
        gamma = signed_gap(instance, first, second, _scaled(normalized, scale))
        if gamma < margin and previous_gamma >= margin:
            lower, upper, gamma_upper = previous_scale, scale, gamma
            break
        previous_scale, previous_gamma = scale, gamma
    if lower is None or upper is None or gamma_upper is None:
        return None

    gamma_lower = previous_gamma
    while upper - lower > tolerance:
        midpoint = 0.5 * (lower + upper)
        gamma = signed_gap(instance, first, second, _scaled(normalized, midpoint))
        if gamma >= margin:
            lower, gamma_lower = midpoint, gamma
        else:
            upper, gamma_upper = midpoint, gamma
    return RadialCrossing(
        normalized,
        0.5 * (lower + upper),
        gamma_lower,
        gamma_upper,
        bracket_steps,
        tolerance,
    )

