"""Regression gates for source extraction and the fiscal accounting boundary."""
import unittest
import pandas as pd

from builder import budget_response, close, parse_sheet
from finance_vintage import parse_api, us_state_population


class SourceTests(unittest.TestCase):
    def test_state_population_excludes_separately_reported_puerto_rico(self):
        frame = pd.DataFrame(dict(SUMLEV=[10, 40, 40, 40], STATE=[0, 1, 11, 72], POPESTIMATE2024=[99, 3, 4, 5]))
        self.assertEqual(us_state_population(frame).to_dict(), {1: 3, 11: 4})

    def test_identical_repeated_predicate_fields_are_collapsed(self):
        frame = parse_api([["GOVTYPE", "AMOUNT", "GOVTYPE"], ["001", "42", "001"]])
        self.assertEqual(list(frame.columns), ["GOVTYPE", "AMOUNT"])
        self.assertTrue(frame.GOVTYPE.eq("001").all())

    def test_conflicting_repeated_fields_fail(self):
        with self.assertRaisesRegex(ValueError, "Conflicting duplicate"):
            parse_api([["GOVTYPE", "GOVTYPE"], ["001", "002"]])

    def test_fee_receipts_are_lost_even_when_spending_does_not_respond(self):
        tax, fees, net_spending = 100, 20, 140
        self.assertEqual(budget_response(tax + fees, net_spending + fees, 0), -120)
        self.assertEqual(budget_response(tax + fees, net_spending + fees, 1), 40)

    def rows(self):
        return [("Title", None, None, None, None),
                ("[Millions of dollars]", None, None, None, None),
                ("Line", None, None, "2023", "2024"),
                ("1", "Current receipts", "X", 2024, 8008290)]

    def test_declared_header_not_matching_data_cell(self):
        self.assertEqual(parse_sheet(self.rows(), 2024)[1]["amount_bn"], 8008.290)

    def test_missing_year_does_not_select_numeric_observation(self):
        rows = self.rows()
        rows[2] = ("Line", None, None, "2022", "2023")
        with self.assertRaisesRegex(ValueError, "no unique year"):
            parse_sheet(rows, 2024)

    def test_missing_official_value_is_not_zero(self):
        rows = self.rows()
        rows[3] = ("1", "Current receipts", "X", 2024, ".....")
        with self.assertRaisesRegex(ValueError, "Missing/duplicate/nonfinite"):
            parse_sheet(rows, 2024)

    def test_units_must_be_explicit(self):
        rows = self.rows()
        rows[1] = ("[Billions of dollars]", None, None, None, None)
        with self.assertRaisesRegex(ValueError, "source units"):
            parse_sheet(rows, 2024)

    def test_duplicate_source_lines_fail(self):
        rows = self.rows()
        rows.append(rows[3])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_sheet(rows, 2024)

    def test_fiscal_year_table_qualifier_preserves_million_units(self):
        rows = self.rows()
        rows[1] = ("[Millions of dollars; quarterly totals not seasonally adjusted]", None, None, None, None)
        self.assertEqual(parse_sheet(rows, 2024)[1]["amount_bn"], 8008.290)

    def test_second_grant_netting_fails_identity(self):
        with self.assertRaisesRegex(ValueError, "net grants"):
            close(8008.290, 5178.912 + 3790.853 - 2 * 961.474, "net grants")

    def test_current_saving_cannot_be_called_net_borrowing(self):
        with self.assertRaisesRegex(ValueError, "different boundaries"):
            close(8008.290 - 10061.458, 8057.709 - 10424.075, "different boundaries")


if __name__ == "__main__":
    unittest.main()
