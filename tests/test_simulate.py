import random
import unittest

from src.simulate import (
    decompose_unwrapped_diagonal,
    diagonal_m0,
    reduced_target_relative_phase,
)


class ExactMatrixTests(unittest.TestCase):
    def test_l0_decomposition_reconstructs_parameters(self):
        generator = random.Random(20261127)
        for _ in range(100):
            theta, a, b = (generator.uniform(-0.4, 0.4) for _ in range(3))
            phases = tuple(
                -0.5 * (theta * z1 * z2 + a * z1 + b * z2)
                for z1, z2 in ((1, 1), (1, -1), (-1, 1), (-1, -1))
            )
            global_phase, got_theta, got_a, got_b = decompose_unwrapped_diagonal(phases)
            self.assertAlmostEqual(global_phase, 0.0, places=14)
            self.assertAlmostEqual(got_theta, theta, places=14)
            self.assertAlmostEqual(got_a, a, places=14)
            self.assertAlmostEqual(got_b, b, places=14)

    def test_l1_reduced_dynamics_for_both_roles(self):
        theta, a, b = 0.17, -0.08, 0.05
        diagonal = diagonal_m0(theta, a, b)
        for control in (0, 1):
            sign = 1 if control == 0 else -1
            self.assertAlmostEqual(
                reduced_target_relative_phase(diagonal, control, role=1),
                sign * theta + a,
                places=14,
            )
            self.assertAlmostEqual(
                reduced_target_relative_phase(diagonal, control, role=2),
                sign * theta + b,
                places=14,
            )


if __name__ == "__main__":
    unittest.main()
