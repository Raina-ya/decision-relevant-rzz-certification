import unittest

from analysis.tolerance.instances import generate_decision_family
from analysis.tolerance.regions import (
    conservative_equal_box_halfwidth,
    conservative_l1_inner_radius,
    in_tolerance_region,
    inner_box_corners,
    sampled_radial_crossing,
)
from src.decision import EdgeError, signed_gap


class ToleranceRegionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = generate_decision_family(20261127)[0]
        cls.instance, cls.first, cls.second = cls.record.objects()

    def test_zero_error_is_inside_development_tolerance(self):
        self.assertTrue(
            in_tolerance_region(
                self.instance, self.first, self.second, (EdgeError(),), self.record.margin
            )
        )

    def test_conservative_inner_box_corners_are_inside(self):
        halfwidth = conservative_equal_box_halfwidth(
            self.instance, self.first, self.second, self.record.margin
        )
        self.assertGreater(halfwidth, 0.0)
        for corner in inner_box_corners(len(self.instance.edges), halfwidth):
            self.assertTrue(
                in_tolerance_region(
                    self.instance, self.first, self.second, corner, self.record.margin
                )
            )

    def test_l1_radius_matches_box_dimension(self):
        radius = conservative_l1_inner_radius(
            self.instance, self.first, self.second, self.record.margin
        )
        halfwidth = conservative_equal_box_halfwidth(
            self.instance, self.first, self.second, self.record.margin
        )
        self.assertAlmostEqual(radius, 3 * halfwidth)

    def test_sampled_crossing_brackets_margin_when_found(self):
        directions = (
            (EdgeError(1.0, 0.0, 0.0),),
            (EdgeError(0.0, 1.0, 0.0),),
            (EdgeError(0.0, 0.0, 1.0),),
        )
        found = 0
        for direction in directions:
            crossing = sampled_radial_crossing(
                self.instance,
                self.first,
                self.second,
                self.record.margin,
                direction,
                max_scale=3.2,
            )
            if crossing is None:
                continue
            found += 1
            self.assertGreaterEqual(crossing.gamma_inside, self.record.margin)
            self.assertLess(crossing.gamma_outside, self.record.margin)
            error = tuple(
                EdgeError(
                    crossing.scale * item.epsilon,
                    crossing.scale * item.local_left,
                    crossing.scale * item.local_right,
                )
                for item in crossing.direction
            )
            self.assertAlmostEqual(
                signed_gap(self.instance, self.first, self.second, error),
                self.record.margin,
                places=7,
            )
        self.assertGreaterEqual(found, 1)


if __name__ == "__main__":
    unittest.main()

