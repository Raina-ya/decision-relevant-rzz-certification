"""Prespecified finite-sample model diagnostics."""

from dataclasses import dataclass
from enum import Enum
from math import inf, log, sqrt

from .estimate import CircularInterval, LinearInterval, UnwrapStatus, unwrap_phase_intervals


class DiagnosticStatus(str, Enum):
    NOT_TRIGGERED = "not-triggered"
    TRIGGERED = "triggered"
    INCONCLUSIVE = "inconclusive"


class ModelStatus(str, Enum):
    ADEQUATE_NOT_REJECTED = "adequate-not-rejected"
    MODEL_INADEQUATE = "model-inadequate"
    DIAGNOSTIC_INCONCLUSIVE = "diagnostic-inconclusive"


@dataclass(frozen=True, slots=True)
class DiagnosticResult:
    name: str
    status: DiagnosticStatus
    detail: str


@dataclass(frozen=True, slots=True)
class DiagnosticAlphaAllocation:
    total: float
    z_conservation: float
    phase_linearity: float
    visibility_linearity: float


def allocate_diagnostic_alpha(alpha_diag: float) -> DiagnosticAlphaAllocation:
    """Bonferroni allocation over the three primary diagnostic families."""
    if not 0.0 < alpha_diag < 1.0:
        raise ValueError("alpha_diag must lie in (0, 1)")
    per_family = alpha_diag / 3.0
    return DiagnosticAlphaAllocation(
        total=alpha_diag,
        z_conservation=per_family,
        phase_linearity=per_family,
        visibility_linearity=per_family,
    )


def z_conservation_diagnostic(
    flips: int,
    shots: int,
    allowed_rate: float,
    alpha: float,
) -> DiagnosticResult:
    """Test whether control-qubit flip probability exceeds a threshold."""
    if shots <= 0 or not 0 <= flips <= shots:
        raise ValueError("invalid flip counts")
    if not 0.0 <= allowed_rate <= 1.0:
        raise ValueError("allowed_rate must lie in [0, 1]")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    estimate = flips / shots
    radius = sqrt(log(1.0 / alpha) / (2.0 * shots))
    lower, upper = max(0.0, estimate - radius), min(1.0, estimate + radius)
    if lower > allowed_rate:
        status = DiagnosticStatus.TRIGGERED
    elif upper <= allowed_rate:
        status = DiagnosticStatus.NOT_TRIGGERED
    else:
        status = DiagnosticStatus.INCONCLUSIVE
    return DiagnosticResult(
        "z-conservation",
        status,
        f"one-sided-compatible interval=[{lower:.12g}, {upper:.12g}], threshold={allowed_rate:.12g}",
    )


def phase_linearity_diagnostic(
    observations: tuple[tuple[int, CircularInterval], ...],
    prior: LinearInterval,
) -> DiagnosticResult:
    """Use interval feasibility of a single per-gate phase slope."""
    result = unwrap_phase_intervals(observations, prior)
    if result.status is UnwrapStatus.INCONSISTENT:
        status = DiagnosticStatus.TRIGGERED
    elif result.status is UnwrapStatus.AMBIGUOUS:
        status = DiagnosticStatus.INCONCLUSIVE
    else:
        status = DiagnosticStatus.NOT_TRIGGERED
    return DiagnosticResult("k-linearity", status, f"unwrap={result.status.value}, last_k={result.last_k}")


def log_linear_visibility_diagnostic(
    observations: tuple[tuple[int, LinearInterval], ...],
) -> DiagnosticResult:
    """Check feasibility of log(V_k) = intercept + slope*k over intervals."""
    if len(observations) < 2:
        return DiagnosticResult(
            "visibility-log-linearity", DiagnosticStatus.INCONCLUSIVE, "fewer than two k values"
        )
    ordered = sorted(observations, key=lambda item: item[0])
    if len({k for k, _ in ordered}) != len(ordered) or ordered[0][0] < 0:
        raise ValueError("k values must be unique and non-negative")
    logged: list[tuple[int, LinearInterval]] = []
    for k, interval in ordered:
        if interval.lower <= 0.0 or interval.upper > 1.0:
            return DiagnosticResult(
                "visibility-log-linearity",
                DiagnosticStatus.INCONCLUSIVE,
                "visibility interval must be contained in (0, 1]",
            )
        logged.append((k, LinearInterval(log(interval.lower), log(interval.upper))))

    slope_lower, slope_upper = -inf, inf
    for index, (k_i, interval_i) in enumerate(logged):
        for k_j, interval_j in logged[index + 1 :]:
            delta = k_j - k_i
            slope_lower = max(slope_lower, (interval_j.lower - interval_i.upper) / delta)
            slope_upper = min(slope_upper, (interval_j.upper - interval_i.lower) / delta)
    status = (
        DiagnosticStatus.NOT_TRIGGERED
        if slope_lower <= slope_upper
        else DiagnosticStatus.TRIGGERED
    )
    return DiagnosticResult(
        "visibility-log-linearity",
        status,
        f"feasible_slope=[{slope_lower:.12g}, {slope_upper:.12g}]",
    )


def combine_diagnostics(results: tuple[DiagnosticResult, ...]) -> ModelStatus:
    if not results:
        return ModelStatus.DIAGNOSTIC_INCONCLUSIVE
    if any(result.status is DiagnosticStatus.TRIGGERED for result in results):
        return ModelStatus.MODEL_INADEQUATE
    if any(result.status is DiagnosticStatus.INCONCLUSIVE for result in results):
        return ModelStatus.DIAGNOSTIC_INCONCLUSIVE
    return ModelStatus.ADEQUATE_NOT_REJECTED
