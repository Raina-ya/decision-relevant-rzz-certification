import unittest
import random

from src.certify import GammaInterval, Verdict, certify, gamma_interval_from_error_box
from src.decision import Candidate, EdgeError, MaxCutInstance, signed_gap


class CertificationRuleTests(unittest.TestCase):
    def test_harmless_requires_lower_bound_at_margin(self):
        self.assertEqual(certify(GammaInterval(0.2, 0.4, 0.95), 0.2), Verdict.HARMLESS)

    def test_harmful_requires_upper_bound_below_zero(self):
        self.assertEqual(certify(GammaInterval(-0.4, -0.01, 0.95), 0.2), Verdict.HARMFUL)

    def test_gray_zone_and_boundary_are_inconclusive(self):
        self.assertEqual(certify(GammaInterval(-0.1, 0.2, 0.95), 0.2), Verdict.INCONCLUSIVE)
        self.assertEqual(certify(GammaInterval(-0.2, 0.0, 0.95), 0.2), Verdict.INCONCLUSIVE)

    def test_rejects_invalid_interval(self):
        with self.assertRaises(ValueError):
            GammaInterval(1.0, 0.0, 0.95)

    def test_lipschitz_projection_contains_sampled_box(self):
        instance = MaxCutInstance(3, ((0, 1), (1, 2), (0, 2)))
        first = Candidate(0.27, (0.2, 0.3, 0.4))
        second = Candidate(-0.19, (0.4, 0.2, 0.1))
        centers = (
            EdgeError(0.01, -0.02, 0.015),
            EdgeError(-0.015, 0.01, 0.0),
            EdgeError(0.0, 0.005, -0.01),
        )
        radii = tuple(EdgeError(0.02, 0.015, 0.01) for _ in instance.edges)
        interval = gamma_interval_from_error_box(
            instance, first, second, centers, radii, confidence=0.95
        )
        generator = random.Random(20261127)
        for _ in range(500):
            errors = tuple(
                EdgeError(
                    center.epsilon + generator.uniform(-radius.epsilon, radius.epsilon),
                    center.local_left
                    + generator.uniform(-radius.local_left, radius.local_left),
                    center.local_right
                    + generator.uniform(-radius.local_right, radius.local_right),
                )
                for center, radius in zip(centers, radii)
            )
            value = signed_gap(instance, first, second, errors)
            self.assertLessEqual(interval.lower, value)
            self.assertGreaterEqual(interval.upper, value)

    def test_rejects_negative_error_radius(self):
        instance = MaxCutInstance(2, ((0, 1),))
        first = Candidate(0.2, (0.3,))
        second = Candidate(-0.1, (0.4,))
        with self.assertRaises(ValueError):
            gamma_interval_from_error_box(
                instance,
                first,
                second,
                (EdgeError(),),
                (EdgeError(epsilon=-0.1),),
                0.95,
            )


if __name__ == "__main__":
    unittest.main()
