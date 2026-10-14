"""P7 failure injection and financial invariants, including the preserved live control."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import backcast as b
from backcast_categories import Cells


def test_only_exact_source_year_blanks_are_structural_zero():
    values = pd.Series(1.0, index=b.YEARS)
    values[2007] = np.nan
    assert b.checked_years(values, "T31200-A:20")[2007] == 0
    with pytest.raises(ValueError, match="BLOCKED.*2007"):
        b.checked_years(values, "T31200-A:19")
    values[2019] = np.nan
    with pytest.raises(ValueError, match="BLOCKED.*2019"):
        b.checked_years(values, "T31200-A:20")


def test_missing_year_and_nonfinite_fail_closed():
    values = pd.Series(1.0, index=b.YEARS)
    with pytest.raises(ValueError, match="BLOCKED.*2010"):
        b.checked_years(values.drop(2010), "T30100-A:20")
    values[2018] = np.inf
    with pytest.raises(ValueError, match="BLOCKED"):
        b.checked_years(values, "T30100-A:20")


def test_programme_cells_reject_injected_gap_before_sum():
    cells = Cells(None)
    cells.tables["T31200-A"] = pd.DataFrame(1.0, index=[19, 20], columns=b.YEARS)
    cells.tables["T31200-A"].loc[19, 2019] = np.nan
    with pytest.raises(ValueError, match="BLOCKED.*2019"):
        cells.get("T31200-A:19;T31200-A:20")


def test_actual_bea_structural_zero_whitelist_covers_only_expected_gaps():
    book = b.workbook(b.ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx")
    values = b.line(book, "T31200-A:20")
    assert values.loc[2005:2014].eq(0).all()
    assert values.loc[2015:2024].gt(0).all()


def test_p7_national_closure_and_high_rate_control():
    charged = pd.read_csv(HERE / "derived/p7/charged_base.csv")
    assert (charged.total_bn - charged.charged_bn - charged.defense - charged.interest - charged.subsidies).abs().max() < 1e-6
    windows = pd.read_csv(HERE / "derived/p7/windows.csv")
    rates = windows[(windows.end == "high") & windows.scenario.isin(["yield_floor0", "yield_unfloored"])]
    assert rates.filter(like="delta_bn").abs().to_numpy().max() < 1e-9
    preserved = windows[windows.scenario == "fixed_2pct"]
    assert preserved.anchor_change_bn.abs().max() < 1e-9
    programmes = windows[windows.scenario.str.startswith("programme")]
    assert programmes.anchor_change_bn.abs().max() < 1e-6
    audit = json.loads((HERE / "derived/p7/audit.json").read_text())
    assert audit["positive_control"] == "four live files byte-identical"


def test_p7_low_rate_reports_2024_movement_and_stack_closes():
    table = pd.read_csv(HERE / "derived/p7/windows.csv").set_index(["end", "rule", "population", "scenario"]).sort_index()
    assert abs(table.loc[("low", "ratio", "lineage", "yield_floor0"), "anchor_change_bn"]) > .01
    for end in ("low", "high"):
        for rule in ("flat", "ratio", "income"):
            for pop in ("union", "lineage"):
                block = table.loc[(end, rule, pop)]
                for col in ("10y_2015_2024_delta_bn", "15y_2010_2024_delta_bn", "20y_2005_2024_delta_bn"):
                    assert abs(block.loc["stack", col] - block.loc[["yield_floor0", "charged_base", "income_linked"], col].sum()) < 1e-6


def test_programme_medicaid_anchor_and_covariance_receipt():
    table = pd.read_csv(HERE / "derived/p7/programme_medicaid_se.csv")
    assert table[table.year == 2024][["delta_bn", "conditional_se_bn"]].abs().to_numpy().max() == 0
    assert table[table.year != 2024].conditional_se_bn.gt(0).all()
    assert set(table.year) == set(range(2019, 2025))


def test_pandemic_component_uncertainty_bounds_keep_unknown_covariance_explicit():
    table = pd.read_csv(HERE / "derived/p7/programme_pandemic_se.csv")
    assert (table.eip_se_lower_bn <= table.eip_se_upper_bn).all()
    assert table.eip_se_lower_bn.ge(0).all()
    single = table[table.year == 2020]
    assert (single.eip_se_lower_bn - single.eip_se_upper_bn).abs().max() < 1e-9
    assert table.credit_rest_conditional_se_bn.gt(0).all()


def test_programme_production_retains_existing_gdp_source_path():
    bea = b.ROOT / "sources/immigration-fiscal/data/external/bea_nipa"
    book = b.workbook(bea / "Section1All_xls.xlsx")
    gdp = b.line(book, b.V4_GDP[0]).reindex(b.YEARS)
    price = b.series(book, "T10109-A", "Gross domestic product").reindex(b.YEARS)
    people = b.series(b.workbook(HERE / "_cache/Section7All_xls.xlsx"), "T70100-A", "Population (midperiod, thousands)")
    # Recover the exact population path from ACS instead of the published four-decimal counts.
    group = pd.read_csv(HERE / "inputs/acs_mexican_origin.csv").set_index("year").acs_mexican_origin.reindex(b.YEARS).interpolate()
    share = group / people.reindex(b.YEARS)
    expected = gdp / gdp[2024] * price[2024] / price * share / share[2024]
    parts = pd.read_csv(HERE / "derived/p7/programme_lines.csv")
    parts = parts[(parts.population == "union") & (parts.rule == "programme") & (parts.variant == "programme")
                  & parts.part.isin(["production_private", "production_receipts"])]
    for _, block in parts.groupby(["end", "part"]):
        values = block.set_index("year").cost_bn.reindex(b.YEARS)
        assert (values / values[2024] - expected).abs().max() < 1e-9
