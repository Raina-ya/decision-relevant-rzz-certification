import json
from pathlib import Path
import unittest

from analysis.tolerance.average_metric import (
    average_gate_fidelity,
    find_witness,
    fidelity_orbit,
)
from analysis.tolerance.instances import GeneratedDecision
from src.decision import EdgeError, signed_gap


ROOT = Path(__file__).resolve().parents[1]


class AverageMetricInsufficiencyTests(unittest.TestCase):
    def test_identity_has_unit_fidelity(self):
        self.assertAlmostEqual(average_gate_fidelity((0.0, 0.0, 0.0)), 1.0, places=14)

    def test_orbit_preserves_average_fidelity(self):
        residual = (0.13, -0.07, 0.21)
        reference = average_gate_fidelity(residual)
        orbit = fidelity_orbit(residual)
        self.assertEqual(len(orbit), 8)
        for image in orbit:
            self.assertAlmostEqual(average_gate_fidelity(image), reference, places=13)

    def test_equal_fidelity_witness_flips_a_development_decision(self):
        family = json.loads(
            (ROOT / "analysis" / "tolerance" / "instances_development.json").read_text(encoding="utf-8")
        )
        record = next(item for item in family["instances"] if item["instance_id"] == "path-3q")
        grid = tuple(0.05 * index for index in range(-6, 7))
        witness = find_witness(record, grid)
        self.assertIsNotNone(witness)
        self.assertAlmostEqual(
            average_gate_fidelity(witness.harmless_residual),
            average_gate_fidelity(witness.harmful_residual),
            places=12,
        )
        self.assertGreaterEqual(witness.harmless_gamma, witness.margin)
        self.assertLess(witness.harmful_gamma, 0.0)
        values = dict(record)
        values["edges"] = tuple(tuple(edge) for edge in values["edges"])
        instance, first, second = GeneratedDecision(**values).objects()
        errors = tuple(EdgeError(*witness.harmful_residual) for _ in instance.edges)
        self.assertAlmostEqual(signed_gap(instance, first, second, errors), witness.harmful_gamma, places=12)


if __name__ == "__main__":
    unittest.main()
