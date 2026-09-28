"""Regression checks for pairing a unit's numbers with its map rows (audit_numbers._align).

    uv run --no-project --offline python3 -m pytest infra/immigration-fiscal/number_drift_audit_2026_09_29/ -q
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_numbers as A  # noqa: E402

Y = A._YEAR


def test_an_inserted_number_does_not_shift_its_neighbours():
    # INDEX line 112 at 263def3: "39.71M" went in before nine mapped numbers, four of them edited.
    # Paired by position, every number met the source of the number now after it.
    a = ["24.2%", "20.3%", "31.1%", "29.6%", "12%", "46%", "18%", "32%", "53–61%"]
    b = ["39.71M", "24.2%", "20.5%", "31.0%", "29.8%", "12%", "46%", "18%", "32%", "52–61%"]
    assert A._align(a, b) == [(i, i + 1) for i in range(9)]


def test_numbers_edited_in_place_keep_their_rows():
    assert A._align(["5", "7"], ["7", "7"]) == [(0, 0), (1, 1)]
    assert A._align(["5", "7"], ["6", "9"]) == [(0, 0), (1, 1)]


def test_a_deleted_number_leaves_its_row_unpaired():
    assert A._align(["$5bn", "$6bn", "$7bn"], ["$5bn", "$7bn"]) == [(0, 0), (2, 1)]


def test_a_year_pairs_only_with_a_year():
    # an unmapped year fills its gap, so the edited number after it keeps its row
    assert A._align([Y, "$5bn"], [Y, "$6bn"]) == [(0, 0), (1, 1)]
    assert A._align(["$5bn"], [Y, "$6bn"]) == [(0, 1)]
