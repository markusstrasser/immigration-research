"""Live pairing must ignore historical-only blanks and fail on missing live numbers."""
import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("tables_oct14", HERE / "tables_oct14.py")
tables = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tables)


def test_live_pairing_historical_annotations_and_invalid_live_values():
    records = tables.rows(tables.F / "sept24_propagation_2026_09_24/derived/oct14/real_costs_totals.csv")
    assert any(row["section"] != "7" and row["oct14"] == "" for row in records)
    values = tables.live_pairing_values(records)
    assert values["pairing_on_priced_count", "published pairing (low)"] > 0
    changed = [dict(row) for row in records]
    live = next(row for row in changed if row["column"] == "pairing_on_priced_count"
                and row["item"] == "published pairing (low)")
    live["oct14"] = ""
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] missing or non-numeric oct14"):
        tables.live_pairing_values(changed)


def test_debt_principal_columns_close_without_summing_rounded_cells():
    path = tables.F / "debt_legacy_2026_09_23/derived/oct14"
    case = json.loads((path / "summary.json").read_text())["case"]
    for end in ("low", "high"):
        printed = next(row for row in tables.rows(path / "federal_split_2024.csv")
                       if row["profile"] == "long_run_non_school_full" and row["convention"] == "central"
                       and row["end"] == end)
        raw = tables.debt_split_values(case, end, printed)
        total = sum(raw[key] for key in ("fiscal_gap_bn", "resource_cost_bn", "displaced_bn", "accrual_bn"))
        assert abs(total - case["v4"]["headline_2024"][end]["set_net_cost_bn"]
                   - float(printed["production_P_bn"])) < 1e-6
        changed = dict(printed, fiscal_gap_bn=str(float(printed["fiscal_gap_bn"]) + 1e-5))
        with pytest.raises(SystemExit, match=r"\[BLOCKED\] C5 .* printed fiscal_gap_bn"):
            tables.debt_split_values(case, end, changed)
