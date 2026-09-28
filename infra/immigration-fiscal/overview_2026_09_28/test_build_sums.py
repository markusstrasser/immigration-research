"""The build's printed-sum gate: in every ledger block, the printed lines add to the printed total.

    uv run --no-project python3 -m pytest infra/immigration-fiscal/overview_2026_09_28/test_build_sums.py -q
"""

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402


def row(kind, label, low, high, signed=True):
    return f'<tr class="item" data-sum="{kind}"><td>{label}</td>{B.cells([Decimal(low), Decimal(high)], signed)}</tr>'


def test_a_running_total_that_reads_as_bad_arithmetic_fails():
    # the operator's example at whole billions: 295 + 77 is printed as 371
    table = (row("start", "Main estimate", "295", "362", False) + row("step", "Pensions", "77", "73")
             + row("running", "= total", "371", "435", False))
    assert B.displayed_sum_errors(table) == ["'Pensions', low end: the parts add to 372, the table prints 371"]
    table = (row("start", "Main estimate", "294.7", "361.8", False) + row("step", "Pensions", "76.7", "73.0")
             + row("running", "= total", "371.4", "434.8", False))
    assert B.displayed_sum_errors(table) == []


def test_ledger_lines_must_add_to_their_subtotal_and_subtotals_to_the_total():
    parts = [("-70.1", "-60.3"), ("-51.0", "-53.6"), ("48.7", "50.3"), ("-13.3", "-8.8"), ("-4.1", "-4.1")]
    table = (row("subtotal", "Own taxes and benefits", "-89.8", "-76.4") + "".join(row("part", "x", *p) for p in parts)
             + row("total", "Main estimate", "-89.8", "-76.4", False))
    assert B.displayed_sum_errors(table) == [
        "'Own taxes and benefits', high end: the parts add to -76.5, the table prints -76.4"]


def test_a_table_with_no_marked_sums_fails():
    assert B.displayed_sum_errors("<table></table>") == [
        "no printed sums found (the rows lost their data-sum marks?)"]


def test_the_built_tables_add_and_rounding_each_line_alone_breaks_them():
    s, _bands, stairs = B.load_numbers()
    rows = B.waterfall_rows(s, stairs)
    tables = lambda: [B.ledger_html(rows)[0], B.alternatives_html(rows)[0]]  # noqa: E731
    assert [B.displayed_sum_errors(t) for t in tables()] == [[], []]
    try:
        B.ROUND_EACH = True
        assert all(B.displayed_sum_errors(t) for t in tables())
    finally:
        B.ROUND_EACH = False
