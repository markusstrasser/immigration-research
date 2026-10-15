"""Guard source units, multiple-imputation structure, and sparse-tail diagnostics."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import pyreadstat

SPEC = importlib.util.spec_from_file_location("outside_checks", Path(__file__).with_name("outside_checks.py"))
oc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(oc)


def toy():
    rows = []
    for household, income, hispanic, weight in [(1, 600_000, True, 100), (2, 600_000, False, 300)]:
        for imp in range(1, 6):
            row = {c: 0 for c in oc.COLS}
            row.update(y1=household * 10 + imp, yy1=household, x5729=income,
                       x42001=weight, x7004=1 if hispanic else 5,
                       x6809=3 if hispanic else 1, x6810=5)
            rows.append(row)
    return pd.DataFrame(rows)


def test_five_implicates_do_not_quintuple_families():
    detailed, average = oc.summarize(toy(), 2022, {2021: 1, 2023: 1})
    row = next(r for r in average if r["bin"] == "500k_1m" and r["hispanic_definition"] == "hispanic_any_race")
    assert row["families_weighted"] == 400
    assert row["family_share"] == .25
    assert row["income_share"] == .25
    assert row["unique_families_any_implicate"] == 2
    assert row["sample_hispanic_families_max"] == 1


def test_pension_withdrawals_are_income_and_convert_frequency():
    d = toy().iloc[:1].copy()
    d["x6558"] = 1000
    d["x6464"] = 100
    d["x6465"] = 4
    assert oc.gross_income(d)[0] == 602_200
    np.testing.assert_allclose(oc.monthly_factor(pd.Series([2, 3, 4, 5, 6, 11, 12, 31, 23, 24, 99])),
                               [52 / 12, 26 / 12, 1, 1 / 3, 1 / 12, 1 / 6, 1 / 2, 2, 13 / 12, 52 / 72, 0])


def test_income_year_is_previous_year_not_survey_year():
    _, average = oc.summarize(toy(), 2022, {2021: 1, 2022: 2, 2023: 2})
    row = next(r for r in average if r["bin"] == "1m_plus" and r["hispanic_definition"] == "hispanic_any_race")
    assert row["unique_families_any_implicate"] == 2


def test_missing_implicate_fails_loud():
    with pytest.raises(ValueError, match="all five implicates"):
        oc.validate_implicates(toy().iloc[1:])


def test_cpi_is_authoritative_annual_average():
    cpi = oc.cpi_annual()
    assert cpi[2018] == 251.107
    assert cpi[2021] == 270.970
    assert cpi[2023] == 304.702


def test_real_outputs_record_sparse_independent_families():
    d = pd.read_csv(oc.LANE / "derived/outside_scf.csv")
    tail = d[(d.bin == "1m_plus") & (d.hispanic_definition == "hispanic_any_race")]
    assert tail.scf_year.tolist() == [2019, 2022]
    assert (tail.unique_hispanic_families_any_implicate <= 20).all()
    assert tail.sampling_se_status.str.startswith("NOT_ESTIMATED").all()
    assert (tail.sample_hispanic_families_max < tail.unique_hispanic_families_any_implicate * 5).all()


def test_raw_income_reconstruction_matches_fed_summary_at_common_price_scale():
    raw, _ = pyreadstat.read_dta(oc.RAW[2022], usecols=oc.COLS)
    summary_path = oc.RAW[2022].with_name("rscfp2022.dta")
    summary, _ = pyreadstat.read_dta(summary_path, usecols=["y1", "income", "wgt"])
    reconstructed = pd.DataFrame({"y1": raw.y1, "raw_income": oc.gross_income(raw),
                                  "raw_wgt": raw.x42001 / 5})
    merged = summary.merge(reconstructed, on="y1", validate="one_to_one")
    assert len(merged) == len(raw) == len(summary)
    positive = merged.raw_income > 0
    scale = float((merged.loc[positive, "income"] / merged.loc[positive, "raw_income"]).median())
    np.testing.assert_allclose(merged.income, merged.raw_income * scale, rtol=1e-12, atol=1e-6)
    np.testing.assert_allclose(merged.wgt, merged.raw_wgt, rtol=1e-12)


def test_bridge_uses_200k_500k_not_100k_500k():
    bridge = pd.DataFrame([dict(sample="pooled_real2023", bin19="12", ratio=.5, carrier_ratio=.4,
                                union_records=10, hispanic_records=20),
                           dict(sample="year_2019_real2023", bin19="12", ratio=.6, carrier_ratio=.5,
                                union_records=12, hispanic_records=24)])
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "bridge.csv"
        bridge.to_csv(path, index=False)
        rows = oc.bridge_rows([dict(scf_year=2019, bin="200k_500k", hispanic_definition="hispanic_any_race",
                                    family_share=.1, income_share=.08, unique_hispanic_families_any_implicate=3)], path)
    assert rows[0]["conditional_tax_share_proxy"] == .048
    assert rows[1]["conditional_tax_share_proxy"] == .04
