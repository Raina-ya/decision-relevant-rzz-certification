import unittest

from analysis.diagnostics.calibrate import (
    CalibrationDesign,
    DiagnosticScenario,
    run_calibration,
)


class DiagnosticCalibrationTests(unittest.TestCase):
    def test_seeded_calibration_is_reproducible(self):
        design = CalibrationDesign(shots_per_phase=500, z_shots=500, ks=(1, 2, 4))
        scenario = DiagnosticScenario("null", 0.01, 0.1, 0.0, 0.02, 0.0)
        first = run_calibration(scenario, design, trials=20, seed=42)
        second = run_calibration(scenario, design, trials=20, seed=42)
        self.assertEqual(first, second)

    def test_clear_z_alternative_is_more_detectable_than_null(self):
        design = CalibrationDesign(shots_per_phase=500, z_shots=1000, ks=(1, 2, 4))
        null = DiagnosticScenario("null", 0.01, 0.1, 0.0, 0.02, 0.0)
        alternative = DiagnosticScenario("z", 0.15, 0.1, 0.0, 0.02, 0.0)
        null_result = run_calibration(null, design, trials=80, seed=7)
        alt_result = run_calibration(alternative, design, trials=80, seed=7)
        self.assertGreater(alt_result.z_trigger_rate, null_result.z_trigger_rate)

    def test_invalid_design_is_rejected(self):
        scenario = DiagnosticScenario("null", 0.01, 0.1, 0.0, 0.02, 0.0)
        with self.assertRaises(ValueError):
            run_calibration(scenario, CalibrationDesign(ks=()), trials=10, seed=1)


if __name__ == "__main__":
    unittest.main()
