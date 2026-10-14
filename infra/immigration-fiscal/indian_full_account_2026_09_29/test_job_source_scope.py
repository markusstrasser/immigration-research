"""Domestic-source receipt scope and fail-loud comparator controls."""
import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("indian_job_source_scope", HERE / "job_capital_factors.py")
J = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(J)


def test_domestic_scope_measures_two_own_job_lines():
    before = [("receipts", "corporate_capital", 100, 12, 1),
              ("receipts", "corporate_labor", 20, 3, 0.37),
              ("spending", "education_services", 80, 10, 1)]
    after = [("receipts", "corporate_capital", 100, 9, 1),
             ("receipts", "corporate_labor", 20, 2, 0.37),
             ("spending", "education_services", 80, 10, 1)]
    rows = J.source_tax_line_changes(before, after)
    assert sum(r["net_cost_change_bn"] for r in rows) == pytest.approx(3.37)


@pytest.mark.parametrize("changed", [
    [("receipts", "corporate_capital", 100, 9, 1)],
    [("receipts", "corporate_capital", 101, 9, 1), ("receipts", "corporate_labor", 20, 2, 0.37)],
    [("receipts", "corporate_capital", 100, 9, 0.37), ("receipts", "corporate_labor", 20, 2, 0.37)],
    [("receipts", "corporate_capital", 100, 9, 1), ("receipts", "corporate_labor", 20, 2, 0.37),
     ("spending", "education_services", 80, 11, 1)],
])
def test_item9_rejects_unmatched_or_changed_scope(changed):
    before = [("receipts", "corporate_capital", 100, 12, 1),
              ("receipts", "corporate_labor", 20, 3, 0.37)]
    if any(row[1] == "education_services" for row in changed):
        before.append(("spending", "education_services", 80, 10, 1))
    with pytest.raises(SystemExit, match="BLOCKED"):
        J.source_tax_line_changes(before, changed)


def test_duplicate_receipt_is_rejected():
    rows = [("receipts", "corporate_capital", 100, 12, 1),
            ("receipts", "corporate_capital", 100, 12, 1),
            ("receipts", "corporate_labor", 20, 3, 0.37)]
    with pytest.raises(SystemExit, match="duplicate"):
        J.source_tax_line_changes(rows, rows)
