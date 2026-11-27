from math import pi
import unittest

from analysis.tolerance.instances import generate_decision_family
from src.decision import decision_gap


class DecisionFamilyTests(unittest.TestCase):
    def test_generation_is_reproducible(self):
        self.assertEqual(generate_decision_family(20261127), generate_decision_family(20261127))

    def test_family_has_three_heavy_hex_subgraphs_and_two_angles_each(self):
        family = generate_decision_family(20261127)
        self.assertEqual([decision.qubits for decision in family], [2, 3, 4])
        self.assertEqual(family[0].scope, "hardware-primary")
        self.assertTrue(all(decision.scope == "method-extension" for decision in family[1:]))
        for decision in family:
            self.assertEqual(decision.edges, tuple((i, i + 1) for i in range(decision.qubits - 1)))
            self.assertGreater(decision.first_theta, 0.0)
            self.assertLessEqual(decision.first_theta, pi / 2)
            self.assertGreater(decision.second_theta, 0.0)
            self.assertLessEqual(decision.second_theta, pi / 2)
            self.assertEqual(len({decision.first_theta, decision.second_theta}), 2)

    def test_recorded_exact_gap_and_margin_recompute(self):
        for decision in generate_decision_family(20261127):
            instance, first, second = decision.objects()
            self.assertAlmostEqual(decision_gap(instance, first, second), decision.ideal_gap, places=14)
            self.assertAlmostEqual(decision.margin, 0.5 * abs(decision.ideal_gap), places=14)
            self.assertGreaterEqual(abs(decision.ideal_gap), 0.15)


if __name__ == "__main__":
    unittest.main()
