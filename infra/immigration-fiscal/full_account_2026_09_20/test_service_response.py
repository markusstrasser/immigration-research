import unittest

import pandas as pd

from service_response import SERVICE_CATEGORIES, education_bounds, responsive_services, validate_baseline


class ServiceResponseTests(unittest.TestCase):
    def test_reference_shape_finiteness_and_fixed_capital_are_enforced(self):
        reference = pd.DataFrame([
            dict(allocation=a, normalization=n, private_plus_receipts_bn=10., welfare_bn=-20.,
                 capital_adjustment=1., excluded_capital_owner_share=0.,
                 public_goods_response=0., fiscal_weight=1.)
            for a in ["personal", "shared"] for n in ["cash", "gdp"]])
        validate_baseline(reference)
        invalid = reference.copy()
        invalid.loc[0, "normalization"] = "unexpected"
        with self.assertRaisesRegex(ValueError, "Cartesian"):
            validate_baseline(invalid)
        invalid = reference.copy()
        invalid.loc[0, "welfare_bn"] = float("inf")
        with self.assertRaisesRegex(ValueError, "Nonfinite"):
            validate_baseline(invalid)
        invalid = reference.copy()
        invalid.loc[0, "capital_adjustment"] = 0.
        with self.assertRaisesRegex(ValueError, "assumptions"):
            validate_baseline(invalid)

    def test_investment_bounds_exclude_capital_and_contain_feasible_splits(self):
        # Gross: schools80, other40; consumption100, investment20.
        low, high = education_bounds(120, 80, 100)
        self.assertEqual((low, high), (.6, .8))
        for school_investment in [0, 5, 10, 20]:
            share = (80-school_investment)/100
            self.assertLessEqual(low, share)
            self.assertGreaterEqual(high, share)
        with self.assertRaises(ValueError):
            education_bounds(100, 80, 120)

    def test_full_response_conserves_cost_and_school_rate_does_not_discount_college(self):
        services = dict.fromkeys(SERVICE_CATEGORIES, 10.)
        services["education_services"] = 100.
        full = responsive_services(services, .8, 1, 1, 1)
        self.assertAlmostEqual(full.responsive_bn.sum(), 160.)
        partial = responsive_services(services, .8, .63, 1, 0).set_index("component")
        self.assertAlmostEqual(partial.loc["school_current", "responsive_bn"], 50.4)
        self.assertAlmostEqual(partial.loc["other_education_current", "responsive_bn"], 20.)
        self.assertEqual(partial.loc["economic_affairs_services", "responsive_bn"], 0)
        self.assertEqual(partial.loc["public_order_safety", "responsive_bn"], 10)
        self.assertAlmostEqual(partial.responsive_bn.sum(), 110.4)

    def test_missing_category_and_nonfinite_input_fail(self):
        services = dict.fromkeys(SERVICE_CATEGORIES, 10.)
        services.pop("health_services")
        with self.assertRaisesRegex(ValueError, "category"):
            responsive_services(services, .8, .63, 1, 0)
        services["health_services"] = float("nan")
        with self.assertRaisesRegex(ValueError, "amount"):
            responsive_services(services, .8, .63, 1, 0)


if __name__ == "__main__":
    unittest.main()
