import unittest
from builder import credit_presentation, read_table, value


class BoundaryTests(unittest.TestCase):
    def test_credit_reclassification_cannot_change_deficit(self):
        receipts, spending = credit_presentation(500, 700, 60)
        self.assertEqual((receipts, spending), (560, 760))
        self.assertEqual(receipts-spending, -200)

    def test_missing_source_cell_cannot_be_zero(self):
        rows = [["title"], ["[Millions of dollars]"], ["Line", "Name", 2024], ["1", "Unavailable", "....."]]
        tables = {"test": read_table(rows)}
        with self.assertRaisesRegex(ValueError, "Missing required"):
            value(tables, "test", 1)

    def test_units_and_duplicate_lines_fail(self):
        rows = [["title"], ["[Billions of dollars]"], ["Line", "Name", 2024], ["1", "Value", 1000]]
        with self.assertRaisesRegex(ValueError, "units"):
            read_table(rows)
        rows[1] = ["[Millions of dollars]"]
        rows.append(rows[-1])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            read_table(rows)

    def test_year_comes_from_header_not_data(self):
        rows = [["title"], ["[Millions of dollars]"], ["Line", "Name", 2023], ["1", "Value", 2024]]
        with self.assertRaisesRegex(ValueError, "year"):
            read_table(rows)


if __name__ == "__main__":
    unittest.main()
