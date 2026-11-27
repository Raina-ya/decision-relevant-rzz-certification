import math
import unittest

from src.model import (
    M0Parameters,
    cycle_phase,
    phase_cycle_signals,
    recover_fixed_angle,
    residual_phase,
)
from src.types import CircuitKind, ProbeKey


class PhaseCycleTests(unittest.TestCase):
    def test_cycle_recovers_phase_despite_scale_and_offset(self):
        for phase in (-2.4, -0.7, 0.0, 1.1, 2.8):
            signals = phase_cycle_signals(
                phase, visibility=0.61, readout_scale=0.83, readout_offset=-0.14
            )
            self.assertAlmostEqual(cycle_phase(signals), phase, places=12)


class IdentifiabilityTests(unittest.TestCase):
    def test_l2_exact_recovery_with_delay_control(self):
        epsilon = 0.013
        local = -0.021
        detuning_phase = 0.004
        slope_0 = epsilon + local + detuning_phase
        slope_1 = -epsilon + local + detuning_phase
        recovered = recover_fixed_angle(slope_0, slope_1, detuning_phase)
        self.assertAlmostEqual(recovered[0], epsilon, places=14)
        self.assertAlmostEqual(recovered[1], local, places=14)

    def test_l2_equivalent_parameters_without_delay_control(self):
        local = 0.03
        detuning = 0.002
        duration = 5.0
        delta = 0.017
        original = local + detuning * duration
        equivalent = (local + delta) + (detuning - delta / duration) * duration
        self.assertAlmostEqual(original, equivalent, places=14)

    def test_role_swap_exposes_b(self):
        params = M0Parameters(epsilon=0.01, a=0.02, b=-0.04)
        key_1 = ProbeKey(math.pi / 4, 2, 0, 1, 0.0)
        key_2 = ProbeKey(math.pi / 4, 2, 0, 2, 0.0)
        self.assertAlmostEqual(residual_phase(key_1, params, 0.0), 0.06)
        self.assertAlmostEqual(residual_phase(key_2, params, 0.0), -0.06)

    def test_delay_and_zero_controls(self):
        params = M0Parameters(
            epsilon=0.01,
            a=0.02,
            b=0.03,
            detuning_1=0.004,
            spam_phase_1=0.2,
        )
        delay = ProbeKey(math.pi / 4, 3, 0, 1, 0.0, CircuitKind.DELAY)
        zero = ProbeKey(math.pi / 4, 0, 0, 1, 0.0, CircuitKind.ZERO)
        self.assertAlmostEqual(residual_phase(delay, params, 2.0), 0.224)
        self.assertAlmostEqual(residual_phase(zero, params, 2.0), 0.2)


if __name__ == "__main__":
    unittest.main()

