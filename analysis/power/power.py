"""Analytic prospective sample-size bounds."""

from dataclasses import dataclass
from math import ceil, inf, isfinite, log, sin


@dataclass(frozen=True, slots=True)
class PhaseBudget:
    shots_per_phase: int
    shots_per_probe: int
    alpha: float
    amplitude_min: float
    angular_radius: float


def required_shots_phase_radius(
    amplitude_min: float,
    angular_radius: float,
    alpha: float,
) -> PhaseBudget:
    """Sufficient four-phase shots for a target angular confidence radius.

    The result is a finite-sample Hoeffding upper bound, not an optimized
    allocation and not a lower bound on N*.
    """
    if not 0.0 < amplitude_min <= 1.0:
        raise ValueError("amplitude_min must lie in (0, 1]")
    if not 0.0 < angular_radius < 0.5 * 3.141592653589793:
        raise ValueError("angular_radius must lie in (0, pi/2)")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    target = sin(angular_radius)
    shots = ceil(
        4.0
        * log(8.0 / alpha)
        * (1.0 + target) ** 2
        / (amplitude_min**2 * target**2)
    )
    return PhaseBudget(shots, 4 * shots, alpha, amplitude_min, angular_radius)


def direct_hoeffding_shots(range_width: float, half_width: float, alpha: float) -> int:
    """Sufficient samples for a bounded scalar mean confidence half-width."""
    if not isfinite(range_width) or range_width <= 0.0:
        raise ValueError("range_width must be finite and positive")
    if not isfinite(half_width) or half_width <= 0.0:
        raise ValueError("half_width must be finite and positive")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    return ceil(range_width**2 * log(2.0 / alpha) / (2.0 * half_width**2))


def bernoulli_kl(first: float, second: float) -> float:
    """KL(Bernoulli(first) || Bernoulli(second))."""
    if not 0.0 <= first <= 1.0 or not 0.0 <= second <= 1.0:
        raise ValueError("Bernoulli probabilities must lie in [0, 1]")
    if first == second:
        return 0.0
    if second in (0.0, 1.0):
        return inf
    left = 0.0 if first == 0.0 else first * log(first / second)
    right = 0.0 if first == 1.0 else (1.0 - first) * log((1.0 - first) / (1.0 - second))
    return left + right


def bretagnolle_huber_required_samples(first: float, second: float, error: float) -> int | float:
    """Necessary samples if both simple-hypothesis errors are at most `error`.

    Bretagnolle-Huber gives type-I + type-II >= exp(-N KL)/2. Requiring both
    errors at most `error` therefore requires N >= log(1/(4 error))/KL when
    `error < 1/4`.
    """
    if not 0.0 < error < 0.25:
        raise ValueError("this nontrivial bound requires error in (0, 1/4)")
    divergence = bernoulli_kl(first, second)
    if divergence == 0.0:
        return inf
    if divergence == inf:
        return 1
    return ceil(log(1.0 / (4.0 * error)) / divergence)


def estimated_qpu_seconds(circuits: int, shots_per_circuit: int, seconds_per_shot: float) -> float:
    """Linear development estimate; job overhead must be added after preflight."""
    if circuits <= 0 or shots_per_circuit <= 0:
        raise ValueError("circuits and shots must be positive")
    if not isfinite(seconds_per_shot) or seconds_per_shot <= 0.0:
        raise ValueError("seconds_per_shot must be finite and positive")
    return circuits * shots_per_circuit * seconds_per_shot

