"""Exact analytic calculations for diagonal coherent-error model M0."""

from dataclasses import dataclass
from math import atan2, cos, sin

from .types import CircuitKind, ProbeKey


@dataclass(frozen=True, slots=True)
class M0Parameters:
    epsilon: float
    a: float
    b: float
    detuning_1: float = 0.0
    detuning_2: float = 0.0
    spam_phase_1: float = 0.0
    spam_phase_2: float = 0.0


def residual_phase(key: ProbeKey, params: M0Parameters, gate_duration: float) -> float:
    """Return the unwrapped residual phase [theory, draft]."""
    local = params.a if key.role == 1 else params.b
    detuning = params.detuning_1 if key.role == 1 else params.detuning_2
    spam = params.spam_phase_1 if key.role == 1 else params.spam_phase_2
    if key.circuit_kind is CircuitKind.ZERO:
        return spam
    if key.circuit_kind is CircuitKind.DELAY:
        return spam + key.k * detuning * gate_duration
    sign = 1.0 if key.control == 0 else -1.0
    return spam + key.k * (sign * params.epsilon + local + detuning * gate_duration)


def measured_signal(
    phase: float,
    analysis_phase: float,
    visibility: float = 1.0,
    readout_scale: float = 1.0,
    readout_offset: float = 0.0,
) -> float:
    """Expected signed readout for one analysis phase [theory, draft]."""
    return readout_scale * visibility * cos(phase - analysis_phase) + readout_offset


def cycle_xy(signals: tuple[float, float, float, float]) -> tuple[float, float]:
    m0, m90, m180, m270 = signals
    return 0.5 * (m0 - m180), 0.5 * (m90 - m270)


def cycle_phase(signals: tuple[float, float, float, float]) -> float:
    x, y = cycle_xy(signals)
    return atan2(y, x)


def phase_cycle_signals(
    phase: float,
    visibility: float = 1.0,
    readout_scale: float = 1.0,
    readout_offset: float = 0.0,
) -> tuple[float, float, float, float]:
    phases = (0.0, 0.5 * 3.141592653589793, 3.141592653589793, 1.5 * 3.141592653589793)
    return tuple(
        measured_signal(phase, analysis, visibility, readout_scale, readout_offset)
        for analysis in phases
    )


def recover_fixed_angle(
    slope_control_0: float,
    slope_control_1: float,
    delay_slope: float,
) -> tuple[float, float]:
    """Recover epsilon and the role-local phase from exact slopes."""
    epsilon = 0.5 * (slope_control_0 - slope_control_1)
    local = 0.5 * (slope_control_0 + slope_control_1) - delay_slope
    return epsilon, local

