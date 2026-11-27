import unittest

from src.certify import GammaInterval, Verdict, certify


class CertificationRuleTests(unittest.TestCase):
    def test_harmless_requires_lower_bound_at_margin(self):
        self.assertEqual(certify(GammaInterval(0.2, 0.4, 0.95), 0.2), Verdict.HARMLESS)

    def test_harmful_requires_upper_bound_below_zero(self):
        self.assertEqual(certify(GammaInterval(-0.4, -0.01, 0.95), 0.2), Verdict.HARMFUL)

    def test_gray_zone_and_boundary_are_inconclusive(self):
        self.assertEqual(certify(GammaInterval(-0.1, 0.2, 0.95), 0.2), Verdict.INCONCLUSIVE)
        self.assertEqual(certify(GammaInterval(-0.2, 0.0, 0.95), 0.2), Verdict.INCONCLUSIVE)

    def test_rejects_invalid_interval(self):
        with self.assertRaises(ValueError):
            GammaInterval(1.0, 0.0, 0.95)


if __name__ == "__main__":
    unittest.main()

