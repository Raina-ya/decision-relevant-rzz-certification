import unittest

from src.certify import gamma_interval_from_error_box, gamma_interval_grid_bound, gamma_interval_per_candidate
from src.decision import Candidate, EdgeError, MaxCutInstance, signed_gap, signed_gap_per_candidate


class PerCandidateResidualTests(unittest.TestCase):
    def setUp(self):
        self.instance = MaxCutInstance(3, ((0, 1), (1, 2)))
        self.first = Candidate(-0.52, (1.5, 1.5))
        self.second = Candidate(-0.17, (0.56, 0.56))

    def test_reduces_to_shared_residual(self):
        errors = (EdgeError(0.02, -0.01, 0.03), EdgeError(-0.01, 0.0, 0.02))
        self.assertAlmostEqual(
            signed_gap_per_candidate(self.instance, self.first, self.second, errors, errors),
            signed_gap(self.instance, self.first, self.second, errors),
            places=14,
        )
        radii = (EdgeError(0.01, 0.01, 0.01),) * 2
        shared = gamma_interval_from_error_box(self.instance, self.first, self.second, errors, radii, 0.95)
        split = gamma_interval_per_candidate(
            self.instance, self.first, self.second, errors, radii, errors, radii, 0.95
        )
        self.assertAlmostEqual(shared.lower, split.lower, places=14)
        self.assertAlmostEqual(shared.upper, split.upper, places=14)

    def test_interval_contains_sampled_points_inside_the_boxes(self):
        import random

        rng = random.Random(7)
        centers1 = (EdgeError(0.03, 0.01, -0.02), EdgeError(0.0, 0.02, 0.01))
        centers2 = (EdgeError(-0.02, 0.0, 0.01), EdgeError(0.01, -0.01, 0.0))
        radii = (EdgeError(0.02, 0.02, 0.02),) * 2
        interval = gamma_interval_per_candidate(
            self.instance, self.first, self.second, centers1, radii, centers2, radii, 0.95
        )

        def jitter(centers):
            return tuple(
                EdgeError(c.epsilon + rng.uniform(-0.02, 0.02), c.local_left + rng.uniform(-0.02, 0.02),
                          c.local_right + rng.uniform(-0.02, 0.02))
                for c in centers
            )

        for _ in range(200):
            value = signed_gap_per_candidate(
                self.instance, self.first, self.second, jitter(centers1), jitter(centers2)
            )
            self.assertLessEqual(interval.lower - 1e-12, value)
            self.assertLessEqual(value, interval.upper + 1e-12)


    def test_grid_bound_is_valid_and_tighter(self):
        import random

        rng = random.Random(3)
        centers1 = (EdgeError(0.03, 0.01, -0.02), EdgeError(0.0, 0.02, 0.01))
        centers2 = (EdgeError(-0.02, 0.0, 0.01), EdgeError(0.01, -0.01, 0.0))
        radii = (EdgeError(0.02, 0.02, 0.02),) * 2
        loose = gamma_interval_per_candidate(
            self.instance, self.first, self.second, centers1, radii, centers2, radii, 0.95)
        tight = gamma_interval_grid_bound(
            self.instance, self.first, self.second, centers1, radii, centers2, radii, 0.95, points=3)
        self.assertGreaterEqual(tight.lower, loose.lower - 1e-12)
        self.assertLessEqual(tight.upper, loose.upper + 1e-12)
        self.assertLess(tight.upper - tight.lower, 0.8 * (loose.upper - loose.lower))

        def jitter(centers):
            return tuple(
                EdgeError(c.epsilon + rng.uniform(-0.02, 0.02), c.local_left + rng.uniform(-0.02, 0.02),
                          c.local_right + rng.uniform(-0.02, 0.02))
                for c in centers
            )

        for _ in range(200):
            value = signed_gap_per_candidate(
                self.instance, self.first, self.second, jitter(centers1), jitter(centers2))
            self.assertLessEqual(tight.lower - 1e-12, value)
            self.assertLessEqual(value, tight.upper + 1e-12)


if __name__ == "__main__":
    unittest.main()
