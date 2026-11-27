import math
import unittest

from src.diagnostics import (
    DiagnosticResult,
    DiagnosticStatus,
    ModelStatus,
    combine_diagnostics,
    log_linear_visibility_diagnostic,
    phase_linearity_diagnostic,
    z_conservation_diagnostic,
)
from src.estimate import CircularInterval, LinearInterval


def wrap(angle: float) -> float:
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


class ModelDiagnosticTests(unittest.TestCase):
    def test_z_conservation_triggers_only_when_lower_bound_exceeds_threshold(self):
        triggered = z_conservation_diagnostic(80, 1000, allowed_rate=0.02, alpha=0.01)
        uncertain = z_conservation_diagnostic(25, 1000, allowed_rate=0.02, alpha=0.01)
        self.assertEqual(triggered.status, DiagnosticStatus.TRIGGERED)
        self.assertEqual(uncertain.status, DiagnosticStatus.INCONCLUSIVE)

    def test_consistent_phase_ladder_is_not_triggered(self):
        slope = 0.7
        observations = tuple(
            (k, CircularInterval(wrap(k * slope), 0.03, 0.99)) for k in (1, 2, 4, 8)
        )
        result = phase_linearity_diagnostic(observations, LinearInterval(-math.pi, math.pi))
        self.assertEqual(result.status, DiagnosticStatus.NOT_TRIGGERED)

    def test_inconsistent_phase_ladder_triggers(self):
        observations = (
            (1, CircularInterval(0.2, 0.01, 0.99)),
            (2, CircularInterval(2.0, 0.01, 0.99)),
        )
        result = phase_linearity_diagnostic(observations, LinearInterval(-math.pi, math.pi))
        self.assertEqual(result.status, DiagnosticStatus.TRIGGERED)

    def test_exponential_visibility_is_feasible(self):
        observations = tuple(
            (k, LinearInterval(math.exp(-0.04 * k) - 0.005, math.exp(-0.04 * k) + 0.005))
            for k in (1, 2, 4, 8)
        )
        result = log_linear_visibility_diagnostic(observations)
        self.assertEqual(result.status, DiagnosticStatus.NOT_TRIGGERED)

    def test_curved_visibility_triggers_when_intervals_are_separated(self):
        observations = (
            (1, LinearInterval(0.94, 0.95)),
            (2, LinearInterval(0.89, 0.90)),
            (4, LinearInterval(0.50, 0.51)),
        )
        result = log_linear_visibility_diagnostic(observations)
        self.assertEqual(result.status, DiagnosticStatus.TRIGGERED)

    def test_combined_policy_forces_model_inadequate(self):
        results = (
            DiagnosticResult("one", DiagnosticStatus.NOT_TRIGGERED, ""),
            DiagnosticResult("two", DiagnosticStatus.TRIGGERED, ""),
        )
        self.assertEqual(combine_diagnostics(results), ModelStatus.MODEL_INADEQUATE)


if __name__ == "__main__":
    unittest.main()

