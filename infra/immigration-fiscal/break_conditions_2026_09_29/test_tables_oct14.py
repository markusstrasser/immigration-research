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


def test_first_year_item6_changes_companions_and_flips_c1_horizon_verdict():
    report = json.loads((tables.D / "first_year_item6_oct14.json").read_text())
    expected = {
        "fixed_capital": {"set": [273.4474, 325.8062], "cash": [198.3210, 250.6797]},
        "whole": {"set": [235.9882, 298.2884], "cash": [160.8617, 223.1620]},
        "corporate_only": {"set": [262.6732, 324.9735], "cash": [187.5468, 249.8470]},
        "off": {"set": [307.7593, 341.6553], "cash": [232.6329, 266.5289]},
    }
    for mode, cases in expected.items():
        for basis, values in cases.items():
            assert report["variants"][mode][basis] == pytest.approx(values, abs=1e-4, rel=0)
    cut = report["thresholds"]["low_bn"]
    assert sum(report["variants"]["whole"]["set"])/2 < cut
    assert sum(report["variants"]["fixed_capital"]["set"])/2 > cut
    assert not report["first_year_breaks_alone"]
    for basis in ("set", "cash"):
        for end in ("low_end_16", "high_end_11"):
            rows = [r for r in report["components"] if r["mode"] == "fixed_capital"
                    and r["basis"] == basis and r["end"] == end]
            for scope in ("union", "added", "lineage"):
                cells = [r for r in rows if r["scope"] == scope]
                assert len(cells) == 4
                for cell in cells:
                    factor = 0 if cell["line"] == "remaining_production_property" else 0.65
                    assert cell["first_year_response"] == pytest.approx(cell["long_run_response"] * factor, abs=1e-12)
            changes = {s: sum(r["cost_change_from_whole_bn"] for r in rows if r["scope"] == s)
                       for s in ("union", "added", "lineage")}
            assert changes["lineage"] == pytest.approx(changes["union"] + changes["added"], abs=1e-9)


def test_first_year_live_tables_use_revised_horizon_and_preserve_other_conditions():
    conclusions = {r["id"]: r for r in tables.rows(tables.D / "conclusions_oct14.csv")}
    assert "does not break C1 alone" in conclusions["C1"]["break_condition"]
    assert "$273.4 / 325.8bn" in conclusions["C1"]["rival_reading"]
    assert "$198.3 / 250.7bn" in conclusions["C1"]["rival_reading"]
    p02 = next(r for r in tables.rows(tables.D / "common_mode_oct14.csv") if r["premise_id"] == "P02")
    assert "does not break C1 alone" in p02["effect_if_swapped"]
