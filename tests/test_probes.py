import math
import unittest

from src.probes import ANALYSIS_PHASES, probe_grid, validate_probe
from src.types import CircuitKind, ProbeKey


class ProbeValidationTests(unittest.TestCase):
    def test_grid_has_expected_factorial_size(self):
        keys = probe_grid((math.pi / 8, math.pi / 4), (1, 2, 4))
        self.assertEqual(len(keys), 2 * 3 * 2 * 2 * 4)
        self.assertEqual({key.analysis_phase for key in keys}, set(ANALYSIS_PHASES))

    def test_rejects_invalid_theta(self):
        with self.assertRaises(ValueError):
            validate_probe(ProbeKey(0.0, 1, 0, 1, 0.0))

    def test_rejects_nonzero_k_zero_control(self):
        with self.assertRaises(ValueError):
            validate_probe(ProbeKey(math.pi / 4, 1, 0, 1, 0.0, CircuitKind.ZERO))


if __name__ == "__main__":
    unittest.main()

