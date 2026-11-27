import importlib.util
import unittest

from analysis.hardware.analyze_hw_p3 import analyze_block, t1_excess_analysis
from analysis.hardware.simulate_hw_p2 import SimModel, simulate_block
from hardware.hw_p2_design import characterization
from hardware.hw_p3_design import KS_P3

HAVE_QISKIT = (
    importlib.util.find_spec("qiskit") is not None
    and importlib.util.find_spec("qiskit_ibm_runtime") is not None
)


class HwP3AnalysisTests(unittest.TestCase):
    def test_split_per_pair_recovers_each_pairs_residual(self):
        models = [SimModel(eps0=0.01, eps1=0.0), SimModel(eps0=-0.02, eps1=0.0, b0=0.03)]
        block = characterization("sim", "A", (0.6118624420100085,), KS_P3, 3000, "sim", anchors=False)
        sims = [simulate_block(block, (2 * i, 2 * i + 1, 99), m, seed=i) for i, m in enumerate(models)]
        records = []
        for j, record in enumerate(sims[0]["records"]):
            records.append({"meta": {k: v for k, v in record["meta"].items() if k != "pair"},
                            "pair_counts": [s["records"][j]["counts"] for s in sims]})
        entries = analyze_block({"block": "sim", "pairs": [[0, 1], [2, 3]], "records": records})
        self.assertEqual(len(entries), 2)
        for entry, model in zip(entries, models):
            eps, a, b = model.residual(entry["theta"])
            self.assertLessEqual(entry["epsilon"][0], eps)
            self.assertLessEqual(eps, entry["epsilon"][1])
            self.assertLessEqual(entry["b"][0], b)
            self.assertLessEqual(b, entry["b"][1])

    def test_t1_excess_is_angle_matched_and_detects_clear_excess(self):
        def record(theta, kind, wrong, shots=10000):
            return {
                "meta": {
                    "type": "probe", "theta": theta, "k": 4, "control": 1,
                    "role": 1, "analysis_phase": 0.0, "circuit_kind": kind,
                },
                "pair_counts": [{"10": shots - wrong, "00": wrong}],
            }

        probe = {"block": "probe", "pairs": [[1, 2]], "records": [record(0.2, "probe", 1000)]}
        reference = {
            "block": "t1-reference", "pairs": [[1, 2]],
            "records": [record(0.2, "delay", 100), record(0.4, "delay", 3000)],
        }
        result = t1_excess_analysis([probe], reference, alpha=0.05)
        self.assertEqual(result["matched_rows"], 1)
        self.assertEqual(result["triggered_pairs"], [[1, 2]])

    def test_t1_excess_without_matching_records_has_no_rows(self):
        empty = {"block": "empty", "pairs": [[1, 2]], "records": []}
        result = t1_excess_analysis([empty], empty)
        self.assertEqual(result["rows"], [])


@unittest.skipUnless(HAVE_QISKIT, "qiskit not installed")
class HwP3BuildTests(unittest.TestCase):
    def test_parallel_isa_keeps_per_pair_rzz_and_marginals_slice_correct_bits(self):
        from qiskit_ibm_runtime.fake_provider import FakeMarrakesh

        from hardware.hw_p3_design import PLANS_P3, select_matching
        from hardware.run_hw_p3 import build, marginals
        from src.qiskit_adapter import fractional_target

        target = fractional_target(FakeMarrakesh().target)
        pairs = select_matching(target)
        self.assertIn((53, 54), pairs)
        self.assertGreater(len(pairs), 40)
        items = build(PLANS_P3["A"][0], target, pairs[:3])  # verify_parallel raises on any violation
        self.assertEqual(len(items), 164)

        class Bits:
            def slice_bits(self, idx):
                return type("C", (), {"get_counts": lambda s, i=tuple(idx): {"".join("1" if b % 2 else "0" for b in reversed(i)): 7}})()

        counts = marginals(Bits(), 2)
        self.assertEqual(counts, [{"10": 7}, {"10": 7}])


if __name__ == "__main__":
    unittest.main()
