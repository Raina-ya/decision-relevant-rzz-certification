import math
import unittest

from src.decision import (
    Candidate,
    EdgeError,
    MaxCutInstance,
    decision_gap,
    exact_expected_cut,
    globally_depolarized_gap,
    signed_gap,
)


class ExactDecisionTests(unittest.TestCase):
    def setUp(self):
        self.edge = MaxCutInstance(2, ((0, 1),))

    def test_uniform_state_has_half_cut_per_edge(self):
        candidate = Candidate(beta=0.0, rzz_angles=(0.0,))
        self.assertAlmostEqual(exact_expected_cut(self.edge, candidate), 0.5, places=14)

    def test_state_remains_normalized_indirectly(self):
        triangle = MaxCutInstance(3, ((0, 1), (1, 2), (0, 2)))
        candidate = Candidate(beta=0.37, rzz_angles=(0.2, 0.4, 0.6))
        value = exact_expected_cut(triangle, candidate)
        self.assertGreaterEqual(value, 0.0)
        self.assertLessEqual(value, 3.0)

    def test_zero_error_matches_ideal(self):
        candidate = Candidate(beta=0.21, rzz_angles=(math.pi / 4,))
        self.assertAlmostEqual(
            exact_expected_cut(self.edge, candidate, (EdgeError(),)),
            exact_expected_cut(self.edge, candidate),
            places=14,
        )

    def test_signed_gap_is_positive_at_ideal_point(self):
        first = Candidate(beta=0.2, rzz_angles=(0.3,))
        second = Candidate(beta=-0.1, rzz_angles=(0.7,))
        self.assertNotEqual(decision_gap(self.edge, first, second), 0.0)
        self.assertGreater(signed_gap(self.edge, first, second), 0.0)

    def test_global_depolarization_preserves_sign_for_positive_visibility(self):
        for gap in (-0.4, 0.2):
            scaled = globally_depolarized_gap(gap, 0.63)
            self.assertEqual(scaled > 0.0, gap > 0.0)
            self.assertAlmostEqual(scaled, 0.63 * gap)

    def test_rejects_non_heavy_family_size(self):
        with self.assertRaises(ValueError):
            MaxCutInstance(5, ((0, 1),))


if __name__ == "__main__":
    unittest.main()

