import math
import unittest

from model import bridge, normalized_gap, reconcile


class AccountTests(unittest.TestCase):
    def test_signed_conservation_and_unknown_are_distinct(self):
        self.assertEqual(reconcile(-10, -1, -7, -1, -1), 0)
        with self.assertRaisesRegex(ValueError, "conservation"):
            reconcile(100, 10, 80, 5, 0)
        with self.assertRaisesRegex(ValueError, "Nonfinite"):
            reconcile(100, math.nan, 100, 0, 0)

    def test_equal_per_person_flow_cancels_only_on_matching_universe(self):
        original = normalized_gap(-30, -70, 10, 100)
        after_uniform_cost = normalized_gap(-50, -250, 10, 100)
        self.assertAlmostEqual(original, after_uniform_cost)
        # Foreign flows are not added to resident balances.
        self.assertNotAlmostEqual(original, normalized_gap(-30, -90, 10, 100))
        with self.assertRaisesRegex(ValueError, "Population"):
            normalized_gap(-30, -70, 100, 100)

    def test_taxes_and_transfers_are_not_free_private_surplus(self):
        # A tax change transfers $50 from outside owners to government.
        original = bridge(-20, 15, 5)
        taxed = bridge(-20, -35, 55)
        self.assertAlmostEqual(original["welfare_bn"], taxed["welfare_bn"])
        transfer = bridge(-20, 15, 5, transfer_saving=7)
        self.assertAlmostEqual(original["welfare_bn"], transfer["welfare_bn"])
        # Valuing only private welfare no longer cancels government transfers.
        private = bridge(-20, 15, 5, transfer_saving=7, fiscal_weight=0)
        self.assertEqual(private["welfare_bn"], 8)

    def test_overlap_and_break_even_have_correct_direction(self):
        result = bridge(-20, 15, 5, overlap=4)
        self.assertEqual(result["welfare_bn"], -4)
        self.assertEqual(result["break_even_omitted_bn"], 4)
        self.assertAlmostEqual(result["break_even_fiscal_weight"], 15/19)
        self.assertEqual(bridge(-20, 15, 5, overlap=4, omitted=4)["welfare_bn"], 0)
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            bridge(0, 0, 0, overlap=-1)


if __name__ == "__main__":
    unittest.main()
