"""Regression checks for fiscal ownership and missing-source failures."""
import unittest
from consolidation import numeric, require_conservation


class ConsolidationTests(unittest.TestCase):
    def test_zero_residual_is_valid(self):
        self.assertEqual(require_conservation(100, 70, 10, 20, "program"), 0)
        self.assertEqual(require_conservation(0, 0, 0, 0, "zero program"), 0)

    def test_duplicate_or_omitted_component_fails(self):
        for rest in [90, 10, 120]:
            with self.assertRaisesRegex(ValueError, "conservation failed"):
                require_conservation(100, 70, 10, rest, "program")

    def test_missing_is_not_zero(self):
        for value in [None, "", "-", float("nan"), float("inf")]:
            with self.assertRaisesRegex(ValueError, "authoritative cell"):
                numeric(value, "state required cell")
        self.assertEqual(numeric(0, "official zero"), 0)


if __name__ == "__main__":
    unittest.main()
