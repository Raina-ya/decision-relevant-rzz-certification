import math
import unittest

from src.circuits import circuit_hash, semantic_operations
from src.types import ProbeKey


class SemanticCircuitTests(unittest.TestCase):
    def test_repeated_rzz_gates_are_not_folded(self):
        key = ProbeKey(math.pi / 8, 8, 0, 1, math.pi / 2)
        operations = semantic_operations(key)
        rzz = [operation for operation in operations if operation.name == "rzz"]
        barriers = [operation for operation in operations if operation.name == "barrier"]
        self.assertEqual(len(rzz), 8)
        self.assertEqual(len(barriers), 8)
        self.assertTrue(all(operation.angle == math.pi / 8 for operation in rzz))

    def test_hash_is_deterministic_and_sensitive_to_control(self):
        first = ProbeKey(math.pi / 4, 4, 0, 2, 0.0)
        second = ProbeKey(math.pi / 4, 4, 1, 2, 0.0)
        self.assertEqual(circuit_hash(first), circuit_hash(first))
        self.assertNotEqual(circuit_hash(first), circuit_hash(second))

    def test_reference_angle_has_control_dependent_sign(self):
        refs = []
        for control in (0, 1):
            key = ProbeKey(math.pi / 8, 4, control, 1, 0.0)
            operations = semantic_operations(key)
            refs.append([op.angle for op in operations if op.name == "rz"][-2])
        self.assertEqual(refs, [-math.pi / 2, math.pi / 2])


if __name__ == "__main__":
    unittest.main()

