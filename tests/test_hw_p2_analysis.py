from math import pi
import unittest

from analysis.hardware.analyze_hw_p2 import analyze_decision_records, analyze_probe_records
from analysis.hardware.simulate_hw_p2 import SimModel, simulate_block
from hardware.hw_p2_design import DECISION_2Q, KS, PLANS, characterization


class HwP2AnalysisTests(unittest.TestCase):
    def test_plans_have_expected_block_order(self):
        self.assertEqual(PLANS["A"][0].name, "A0-calibration")
        self.assertEqual(PLANS["A"][1].name, "A1-decision-2q")
        replicate = next(b for b in PLANS["B"] if b.name == "B2-replicate-2q-pairA")
        self.assertEqual(replicate.pair, "A")  # cross-account replication of pair A

    def test_injected_residuals_fall_inside_finite_sample_boxes(self):
        model = SimModel()
        block = characterization("sim", "A", DECISION_2Q, KS, 4000, "sim", anchors=False)
        data = simulate_block(block, (3, 4, 5), model, seed=11)
        entries = analyze_probe_records(data["records"])
        self.assertEqual(len(entries), 2)
        for entry in entries:
            self.assertIsNotNone(entry["epsilon"], entry["unwrap_status"])
            eps, a, b = model.residual(entry["theta"])
            self.assertLessEqual(entry["epsilon"][0], eps)
            self.assertLessEqual(eps, entry["epsilon"][1])
            self.assertLessEqual(entry["a"][0], a)
            self.assertLessEqual(a, entry["a"][1])
            self.assertLessEqual(entry["b"][0], b)
            self.assertLessEqual(b, entry["b"][1])
            for diag in entry["z_conservation"]:
                self.assertNotEqual(diag["status"], "triggered")

    def test_t1_reference_block_and_flip_comparison(self):
        from analysis.hardware.analyze_hw_p2 import control_flip_comparison
        from hardware.hw_p2_design import PLANS

        names = [b.name for b in PLANS["A"]]
        self.assertLess(names.index("A7-t1-reference"), names.index("A3-grid"))
        rec = lambda kind, flips: {"meta": {"type": "probe", "pair": [1, 2], "control": 1, "circuit_kind": kind,
                                             "k": 64, "role": 2, "theta": 0.6, "analysis_phase": 0.0},
                                    "counts": {"00": flips, "10": 1000 - flips}}
        rows = control_flip_comparison([rec("probe", 110), rec("delay", 100)])
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["excess"], 0.01, places=12)

    def test_direct_decision_gap_from_counts(self):
        records = [
            {"meta": {"type": "decision", "instance_id": "path-2q", "implementation": "native-rzz",
                      "candidate": "first", "ideal_gap": -0.42}, "counts": {"00": 700, "11": 300}},
            {"meta": {"type": "decision", "instance_id": "path-2q", "implementation": "native-rzz",
                      "candidate": "second", "ideal_gap": -0.42}, "counts": {"01": 700, "10": 200, "00": 100}},
        ]
        out = analyze_decision_records(records)
        self.assertEqual(len(out), 1)
        self.assertAlmostEqual(out[0]["signed_gap"], 0.9, places=12)


if __name__ == "__main__":
    unittest.main()
