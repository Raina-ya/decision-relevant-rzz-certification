import math
import random
import unittest

from src.estimate import (
    BinomialCount,
    CircularInterval,
    LinearInterval,
    UnwrapStatus,
    four_phase_confidence,
    four_phase_joint_confidence,
    hoeffding_signed_mean_radius,
    recover_m0_intervals,
    unwrap_phase_intervals,
)
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

    def test_joint_amplitude_interval_contains_true_contrast(self):
        phase = 0.43
        visibility = 0.82
        readout_scale = 0.91
        signals = phase_cycle_signals(
            phase, visibility=visibility, readout_scale=readout_scale, readout_offset=-0.06
        )
        shots = 20000
        counts = tuple(
            BinomialCount(round(shots * (signal + 1.0) / 2.0), shots)
            for signal in signals
        )
        estimate = four_phase_joint_confidence(counts, alpha=0.01)
        self.assertTrue(estimate.amplitude_interval.contains(visibility * readout_scale))

    def test_joint_amplitude_interval_is_physical_when_unresolved(self):
        counts = tuple(BinomialCount(5, 10) for _ in range(4))
        estimate = four_phase_joint_confidence(counts, alpha=0.05)
        self.assertEqual(estimate.amplitude_interval.lower, 0.0)
        self.assertEqual(estimate.amplitude_interval.upper, 1.0)

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


def wrap(angle: float) -> float:
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


class IntervalUnwrappingTests(unittest.TestCase):
    def test_power_of_two_ladder_identifies_large_slope(self):
        slope = 1.2
        observations = tuple(
            (k, CircularInterval(wrap(k * slope), 0.08, 0.99)) for k in (1, 2, 4, 8, 16)
        )
        result = unwrap_phase_intervals(observations)
        self.assertEqual(result.status, UnwrapStatus.IDENTIFIED)
        self.assertTrue(result.interval.contains(slope))
        self.assertLessEqual(result.interval.upper - result.interval.lower, 0.01)

    def test_missing_coarse_stage_is_reported_ambiguous(self):
        slope = 1.2
        result = unwrap_phase_intervals(
            ((8, CircularInterval(wrap(8 * slope), 0.05, 0.95)),)
        )
        self.assertEqual(result.status, UnwrapStatus.AMBIGUOUS)

    def test_contradictory_stage_is_reported_inconsistent(self):
        observations = (
            (1, CircularInterval(0.2, 0.01, 0.95)),
            (2, CircularInterval(2.0, 0.01, 0.95)),
        )
        result = unwrap_phase_intervals(observations)
        self.assertEqual(result.status, UnwrapStatus.INCONSISTENT)

    def test_full_circle_stage_does_not_fake_information(self):
        result = unwrap_phase_intervals(((1, CircularInterval(0.0, math.pi, 0.95)),))
        self.assertEqual(result.interval, LinearInterval(-math.pi, math.pi))

    def test_m0_interval_recovery_contains_truth(self):
        epsilon, a, b, d1, d2 = 0.03, -0.02, 0.04, 0.01, -0.015

        def around(value: float, radius: float = 0.002) -> LinearInterval:
            return LinearInterval(value - radius, value + radius)

        box = recover_m0_intervals(
            around(epsilon + a + d1),
            around(-epsilon + a + d1),
            around(d1),
            around(epsilon + b + d2),
            around(-epsilon + b + d2),
            around(d2),
        )
        self.assertTrue(box.epsilon.contains(epsilon))
        self.assertTrue(box.a.contains(a))
        self.assertTrue(box.b.contains(b))


if __name__ == "__main__":
    unittest.main()
