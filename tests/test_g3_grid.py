import json
from pathlib import Path
import unittest

from analysis.simulation.ademp import AdempScenario
from analysis.simulation.g3_grid import run_two_angle_grid_point
from src.decision import Candidate, MaxCutInstance


class G3GridTests(unittest.TestCase):
    def setUp(self):
        path = Path("analysis/tolerance/instances_sign_sensitive.json")
        record = json.loads(path.read_text(encoding="utf-8"))["instances"][0]
        self.instance = MaxCutInstance(2, ((0, 1),))
        self.first = Candidate(record["first_beta"], (record["first_theta"],))
        self.second = Candidate(record["second_beta"], (record["second_theta"],))
        self.scenario = AdempScenario(
            -0.4, 0.0, 0.0, 0.0, 0.0, 0.85, 0.94, -0.03, 200, 0.05,
            record["margin"], (1, 2, 4),
        )

    def test_two_angle_grid_is_reproducible_and_counts_cost(self):
        first = run_two_angle_grid_point(
            self.scenario, self.instance, self.first, self.second, 20, 9
        )
        second = run_two_angle_grid_point(
            self.scenario, self.instance, self.first, self.second, 20, 9
        )
        self.assertEqual(first, second)
        self.assertEqual(first.total_probe_circuits, 2 * 6 * 3 * 4)
        self.assertEqual(first.total_probe_shots, first.total_probe_circuits * 200)

    def test_multi_edge_scope_is_rejected(self):
        with self.assertRaises(ValueError):
            run_two_angle_grid_point(
                self.scenario,
                MaxCutInstance(3, ((0, 1), (1, 2))),
                Candidate(0.1, (0.2, 0.2)),
                Candidate(0.2, (0.3, 0.3)),
                2,
                1,
            )


if __name__ == "__main__":
    unittest.main()
