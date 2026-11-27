"""Probe specifications independent of a particular quantum SDK."""

from math import isfinite, pi

from .types import CircuitKind, ProbeKey


ANALYSIS_PHASES = (0.0, pi / 2, pi, 3 * pi / 2)


def validate_probe(key: ProbeKey) -> None:
    if not isfinite(key.theta) or not 0.0 < key.theta <= pi / 2:
        raise ValueError("theta must be finite and in (0, pi/2]")
    if key.k < 0:
        raise ValueError("k must be non-negative")
    if key.control not in (0, 1):
        raise ValueError("control must be 0 or 1")
    if key.role not in (1, 2):
        raise ValueError("role must be 1 or 2")
    if key.analysis_phase not in ANALYSIS_PHASES:
        raise ValueError("analysis_phase must be in the four-phase cycle")
    if key.circuit_kind is CircuitKind.ZERO and key.k != 0:
        raise ValueError("k_zero probes require k=0")


def probe_grid(thetas: tuple[float, ...], ks: tuple[int, ...]) -> tuple[ProbeKey, ...]:
    keys = tuple(
        ProbeKey(theta, k, control, role, phase)
        for theta in thetas
        for k in ks
        for control in (0, 1)
        for role in (1, 2)
        for phase in ANALYSIS_PHASES
    )
    for key in keys:
        validate_probe(key)
    return keys

