import math
import random
import unittest

from src.estimate import BinomialCount, four_phase_confidence, hoeffding_signed_mean_radius
from src.model import phase_cycle_signals


def draw_binomial(generator: random.Random, shots: int, probability: float) -> int:
    return sum(generator.random() < probability for _ in range(shots))


class FiniteConfidenceTests(unittest.TestCase):
    def test_hoeffding_radius_decreases_with_shots(self):
        self.assertGreater(
            hoeffding_signed_mean_radius(100, 0.05),
            hoeffding_signed_mean_radius(400, 0.05),
        )

    def test_interval_is_full_circle_when_signal_is_unresolved(self):
        counts = tuple(BinomialCount(50, 100) for _ in range(4))
        estimate = four_phase_confidence(counts, alpha=0.05)
        self.assertEqual(estimate.confidence_interval.radius, math.pi)
        self.assertTrue(estimate.confidence_interval.contains(-2.7))

    def test_fixed_seed_coverage_study(self):
        generator = random.Random(20261127)
        shots = 400
        alpha = 0.05
        trials = 1000
        phase = 0.73
        signals = phase_cycle_signals(
            phase, visibility=0.82, readout_scale=0.91, readout_offset=-0.06
        )
        probabilities = tuple((signal + 1.0) / 2.0 for signal in signals)
        covered = 0
        for _ in range(trials):
            counts = tuple(
                BinomialCount(draw_binomial(generator, shots, probability), shots)
                for probability in probabilities
            )
            interval = four_phase_confidence(counts, alpha).confidence_interval
            covered += interval.contains(phase)
        # [sim] Deterministic development check, not the full G3 ADEMP study.
        self.assertGreaterEqual(covered / trials, 0.95)

    def test_rejects_invalid_counts(self):
        with self.assertRaises(ValueError):
            BinomialCount(11, 10)


if __name__ == "__main__":
    unittest.main()

