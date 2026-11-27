import unittest

from analysis.simulation.ademp import AdempScenario, run_ademp, wilson_interval
from src.decision import Candidate, MaxCutInstance


class AdempPipelineTests(unittest.TestCase):
    def test_end_to_end_study_is_reproducible_and_rates_partition(self):
        scenario = AdempScenario(
            epsilon=0.02,
            a=-0.01,
            b=0.015,
            detuning_1=0.005,
            detuning_2=-0.004,
            visibility=0.9,
            readout_scale=0.94,
            readout_offset=-0.03,
            shots_per_phase=500,
            alpha_total=0.05,
            margin=0.05,
        )
        instance = MaxCutInstance(2, ((0, 1),))
        first = Candidate(0.3, (0.4,))
        second = Candidate(-0.2, (0.7,))
        first_run = run_ademp(scenario, instance, first, second, trials=40, seed=20261127)
        second_run = run_ademp(scenario, instance, first, second, trials=40, seed=20261127)
        self.assertEqual(first_run, second_run)
        self.assertAlmostEqual(
            first_run.harmless_rate + first_run.harmful_rate + first_run.inconclusive_rate,
            1.0,
        )
        self.assertGreaterEqual(first_run.m0_coverage, 0.95)
        self.assertGreater(first_run.false_harmless_wilson95[1], 0.0)

    def test_invalid_trial_count_is_rejected(self):
        scenario = AdempScenario(0, 0, 0, 0, 0, 0.9, 0.9, 0, 100, 0.05, 0.0)
        instance = MaxCutInstance(2, ((0, 1),))
        candidate = Candidate(0.1, (0.2,))
        with self.assertRaises(ValueError):
            run_ademp(scenario, instance, candidate, candidate, trials=0, seed=1)

    def test_wilson_interval_is_non_degenerate_at_boundary(self):
        lower, upper = wilson_interval(0, 2000)
        self.assertEqual(lower, 0.0)
        self.assertGreater(upper, 0.0)


if __name__ == "__main__":
    unittest.main()
