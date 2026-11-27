"""Independent exact matrix calculations using only the Python standard library."""

from cmath import exp, phase
from itertools import product


def diagonal_m0(theta_zz: float, a: float, b: float) -> tuple[complex, ...]:
    """Return M0 diagonal in computational basis order 00, 01, 10, 11."""
    values = []
    for bit_1, bit_2 in product((0, 1), repeat=2):
        z_1 = 1 if bit_1 == 0 else -1
        z_2 = 1 if bit_2 == 0 else -1
        generator = theta_zz * z_1 * z_2 + a * z_1 + b * z_2
        values.append(exp(-0.5j * generator))
    return tuple(values)


def decompose_unwrapped_diagonal(
    phases: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    """Decompose unwrapped diagonal phases into global, ZZ, ZI, and IZ terms."""
    basis = tuple(product((1, -1), repeat=2))
    global_phase = sum(phases) / 4
    theta_zz = -0.5 * sum(value * z_1 * z_2 for value, (z_1, z_2) in zip(phases, basis))
    a = -0.5 * sum(value * z_1 for value, (z_1, _) in zip(phases, basis))
    b = -0.5 * sum(value * z_2 for value, (_, z_2) in zip(phases, basis))
    return global_phase, theta_zz, a, b


def principal_phases(diagonal: tuple[complex, ...]) -> tuple[float, ...]:
    return tuple(phase(value) for value in diagonal)


def reduced_target_relative_phase(
    diagonal: tuple[complex, complex, complex, complex], control: int, role: int
) -> float:
    """Return arg(U_target[1]/U_target[0]) for a fixed control basis state."""
    if role == 1:
        index_0, index_1 = (control, control + 2)
    elif role == 2:
        index_0, index_1 = (2 * control, 2 * control + 1)
    else:
        raise ValueError("role must be 1 or 2")
    return phase(diagonal[index_1] / diagonal[index_0])

