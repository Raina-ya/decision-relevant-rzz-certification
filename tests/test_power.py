import math
import unittest

from analysis.power.power import (
    bernoulli_kl,
    bretagnolle_huber_required_samples,
    direct_hoeffding_shots,
    estimated_qpu_seconds,
    required_shots_phase_radius,
    two_point_required_samples,
)
from src.estimate import hoeffding_signed_mean_radius


class PowerBoundTests(unittest.TestCase):
    def test_phase_budget_meets_derived_geometric_condition(self):
        budget = required_shots_phase_radius(0.75, 0.2, 0.05)
        component = hoeffding_signed_mean_radius(budget.shots_per_phase, 0.05)
        vector_radius = math.sqrt(2.0) * component
        estimated_norm_lower = 0.75 - vector_radius
        achieved = math.asin(vector_radius / estimated_norm_lower)
        self.assertLessEqual(achieved, 0.2)

    def test_phase_budget_increases_for_weaker_visibility(self):
        strong = required_shots_phase_radius(0.9, 0.2, 0.05)
        weak = required_shots_phase_radius(0.5, 0.2, 0.05)
        self.assertGreater(weak.shots_per_phase, strong.shots_per_phase)

    def test_direct_bound_scales_inverse_square(self):
        coarse = direct_hoeffding_shots(1.0, 0.2, 0.05)
        fine = direct_hoeffding_shots(1.0, 0.1, 0.05)
        self.assertGreaterEqual(fine, 3 * coarse)

    def test_bernoulli_kl_and_bh_bound(self):
        self.assertEqual(bernoulli_kl(0.3, 0.3), 0.0)
        self.assertGreater(bernoulli_kl(0.3, 0.4), 0.0)
        self.assertEqual(bretagnolle_huber_required_samples(0.3, 0.3, 0.05), math.inf)
        self.assertGreater(bretagnolle_huber_required_samples(0.3, 0.4, 0.05), 1)

    def test_general_two_point_bound_reduces_to_symmetric_bound(self):
        symmetric = bretagnolle_huber_required_samples(0.3, 0.4, 0.05)
        general = two_point_required_samples(0.3, 0.4, 0.05, 0.05)
        self.assertEqual(general, symmetric)

    def test_two_point_bound_detects_nonidentifiability(self):
        self.assertEqual(two_point_required_samples(0.3, 0.3, 0.02, 0.1), math.inf)
        with self.assertRaises(ValueError):
            two_point_required_samples(0.3, 0.4, 0.25, 0.25)

    def test_qpu_estimate_reproduces_linear_arithmetic(self):
        self.assertAlmostEqual(estimated_qpu_seconds(256, 2000, 4.16e-4), 212.992)


if __name__ == "__main__":
    unittest.main()
