"""Exact small-instance QAOA MaxCut decision calculations."""

from cmath import exp
from dataclasses import dataclass
from math import cos, isfinite, sin


@dataclass(frozen=True, slots=True)
class MaxCutInstance:
    qubits: int
    edges: tuple[tuple[int, int], ...]

    def __post_init__(self) -> None:
        if not 2 <= self.qubits <= 4:
            raise ValueError("the prespecified initial family supports 2-4 qubits")
        if not self.edges:
            raise ValueError("at least one edge is required")
        canonical = set()
        for left, right in self.edges:
            if not 0 <= left < self.qubits or not 0 <= right < self.qubits:
                raise ValueError("edge endpoint outside instance")
            if left == right:
                raise ValueError("self-loops are not supported")
            edge = tuple(sorted((left, right)))
            if edge in canonical:
                raise ValueError("duplicate edge")
            canonical.add(edge)


@dataclass(frozen=True, slots=True)
class Candidate:
    beta: float
    rzz_angles: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class EdgeError:
    epsilon: float = 0.0
    local_left: float = 0.0
    local_right: float = 0.0


def _z(index: int, qubit: int) -> int:
    return 1 if ((index >> qubit) & 1) == 0 else -1


def _apply_rx_layer(state: list[complex], qubits: int, beta: float) -> None:
    diagonal = cos(beta)
    off_diagonal = -1j * sin(beta)
    for qubit in range(qubits):
        mask = 1 << qubit
        for index in range(len(state)):
            if index & mask:
                continue
            paired = index | mask
            low, high = state[index], state[paired]
            state[index] = diagonal * low + off_diagonal * high
            state[paired] = off_diagonal * low + diagonal * high


def exact_expected_cut(
    instance: MaxCutInstance,
    candidate: Candidate,
    errors: tuple[EdgeError, ...] | None = None,
) -> float:
    """Return the exact p=1 expected cut value [exact]."""
    if len(candidate.rzz_angles) != len(instance.edges):
        raise ValueError("one RZZ angle is required per edge")
    if errors is None:
        errors = tuple(EdgeError() for _ in instance.edges)
    if len(errors) != len(instance.edges):
        raise ValueError("one error triple is required per edge")
    if not isfinite(candidate.beta):
        raise ValueError("beta must be finite")

    dimension = 1 << instance.qubits
    state = [complex(dimension ** -0.5) for _ in range(dimension)]
    for index in range(dimension):
        phase_generator = 0.0
        for (left, right), theta, error in zip(
            instance.edges, candidate.rzz_angles, errors
        ):
            z_left, z_right = _z(index, left), _z(index, right)
            phase_generator += (
                (theta + error.epsilon) * z_left * z_right
                + error.local_left * z_left
                + error.local_right * z_right
            )
        state[index] *= exp(-0.5j * phase_generator)
    _apply_rx_layer(state, instance.qubits, candidate.beta)

    expectation = 0.0
    for index, amplitude in enumerate(state):
        cut = sum(((index >> left) & 1) != ((index >> right) & 1) for left, right in instance.edges)
        expectation += abs(amplitude) ** 2 * cut
    return expectation


def decision_gap(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    errors: tuple[EdgeError, ...] | None = None,
) -> float:
    return exact_expected_cut(instance, first, errors) - exact_expected_cut(
        instance, second, errors
    )


def signed_gap(
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    errors: tuple[EdgeError, ...] | None = None,
) -> float:
    ideal = decision_gap(instance, first, second)
    if ideal == 0.0:
        raise ValueError("the ideal decision must not be tied")
    sign = 1.0 if ideal > 0.0 else -1.0
    return sign * decision_gap(instance, first, second, errors)


def globally_depolarized_gap(gap: float, visibility: float) -> float:
    """Global depolarization scales a same-observable candidate gap [theory, draft]."""
    if not 0.0 <= visibility <= 1.0:
        raise ValueError("visibility must lie in [0, 1]")
    return visibility * gap

