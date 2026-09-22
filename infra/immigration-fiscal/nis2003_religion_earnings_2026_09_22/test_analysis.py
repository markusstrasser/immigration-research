"""Gate and unit tests for the NIS-2003 religion/earnings lane.

Tests that need the extracted microdata skip when `_cache/ICPSR_38031` is absent
(it is git-ignored); the pure-arithmetic and documentation-consistency tests always run.
"""
from __future__ import annotations

import json
import pathlib

import numpy as np
import pandas as pd
import pytest

import analysis as A

LANE = pathlib.Path(__file__).resolve().parent
DERIVED = LANE / "derived"
needs_cache = pytest.mark.skipif(not A.CACHE.exists(), reason="microdata not extracted into _cache/")
needs_derived = pytest.mark.skipif(not (DERIVED / "audit.json").exists(), reason="analysis.py not run yet")


# --------------------------------------------------------------------- helpers
def test_wmean_matches_hand_calculation():
    assert A.wmean(np.array([1.0, 3.0]), np.array([1.0, 3.0])) == pytest.approx(2.5)
    assert A.wmean(np.array([0.0, 1.0]), np.array([1.0, 1.0])) == pytest.approx(0.5)


def test_wmedian_equal_weights_matches_numpy():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    assert A.wmedian(x, np.ones(5)) == pytest.approx(np.median(x))


def test_wmedian_moves_with_weight():
    x = np.array([10.0, 20.0])
    assert A.wmedian(x, np.array([9.0, 1.0])) < 15.0
    assert A.wmedian(x, np.array([1.0, 9.0])) > 15.0


def test_wls_recovers_a_known_line():
    rng = np.random.default_rng(0)
    n = 500
    x = rng.normal(size=n)
    y = 2.0 + 3.0 * x
    b = A.wls(np.column_stack([np.ones(n), x]), y, np.ones(n))
    assert b[0] == pytest.approx(2.0, abs=1e-8)
    assert b[1] == pytest.approx(3.0, abs=1e-8)


# ------------------------------------------------------- documentation constants
def test_weight_table_totals_match_the_documented_totals():
    frame = sum(f for st in A.WEIGHT_TABLE.values() for f, _, _ in st.values())
    sampled = sum(s for st in A.WEIGHT_TABLE.values() for _, s, _ in st.values())
    complete = sum(c for st in A.WEIGHT_TABLE.values() for _, _, c in st.values())
    assert (frame, sampled, complete) == (A.FRAME_TOTAL, A.SAMPLED_TOTAL, A.N_ADULT)


def test_religion_codes_cover_every_analysis_group():
    assert set(A.RELIGION_GROUP) <= set(A.RELIGION_CODES)
    assert set(A.CHRISTIAN) < set(A.RELIGION_GROUP.values())
    assert A.RELIGION_GROUP[4] == "Muslim"


def test_every_named_country_maps_into_a_documented_region_code():
    for country, region in A.COUNTRY_TO_REGION.items():
        assert country in A.COUNTRY_CODES
        assert region in A.COUNTRY_CODES
        assert 300 <= region <= 310


def test_code_sources_are_named_for_every_recoded_variable():
    for key in ["J30_1MO", "J14", "C1", "C47_1", "C48A2_1", "G7/G15", "VISACATMO", "CISCOBINSMO"]:
        assert key in A.CODE_SOURCES and ".pdf" in A.CODE_SOURCES[key]


# ------------------------------------------------------------------ annualisation
def _synthetic(unit, pay_kind, salary, hourly, hours, weeks):
    cols = {c: [""] for ds in A.DATASETS.values() for c in ds}
    cols.update({c: [""] for ds in A.SPOUSE_DATASETS.values() for c in ds if c != "PU_ID"})
    cols = {("S_" + c if c in ("G1", "G15", "G16PPP") else c): v for c, v in cols.items()}
    d = pd.DataFrame(cols)
    d["PU_ID"] = ["000110"]
    d["NISWGTSAMP1"] = ["1.0"]
    d["NISADULTSTR"] = ["4"]
    d["A7"] = ["1970"]
    d["STRTYR"] = ["2003"]
    d["C47_1"] = [str(pay_kind)]
    d["C48A2_1"] = [str(unit)]
    d["C48_1PPP"] = [str(salary)]
    d["C49_1PPP"] = [str(hourly)]
    d["C33_1"] = [str(hours)]
    d["C37_1"] = [str(weeks)]
    return d


@pytest.mark.parametrize("unit,expect", [(5, 50000.0), (4, 600000.0), (2, 2600000.0), (3, 1300000.0)])
def test_salary_unit_factors(unit, expect):
    out = A.build(_synthetic(unit, 1, 50000, "", 40, 52))
    assert out.earn_annual.iloc[0] == pytest.approx(expect)


def test_hourly_annualisation_uses_hours_times_weeks():
    out = A.build(_synthetic(-2, 2, "", 20, 35, 50))
    assert out.earn_annual.iloc[0] == pytest.approx(20 * 35 * 50)


def test_full_time_restriction_drops_short_hours():
    assert pd.isna(A.build(_synthetic(-2, 2, "", 20, 20, 52)).earn_ft.iloc[0])
    assert A.build(_synthetic(-2, 2, "", 20, 30, 52)).earn_ft.iloc[0] == pytest.approx(20 * 30 * 52)


# --------------------------------------------------------------------- microdata
@pytest.fixture(scope="module")
def built():
    return A.build(A.load()[0])


@needs_cache
def test_g2_every_dataset_has_8573_unique_respondents():
    _, gate2 = A.load()
    for ds, info in gate2.items():
        assert info["unique_PU_ID"], ds
        if "spouse" not in ds:
            assert info["rows"] == A.N_ADULT, ds


@needs_cache
def test_design_weights_reproduce_the_documentation_exactly(built):
    doc = {}
    for rep, strata in A.WEIGHT_TABLE.items():
        for st, (frame, sampled, _) in strata.items():
            doc.setdefault(st, []).append(1.0 / ((sampled / frame) * (A.FRAME_TOTAL / A.SAMPLED_TOTAL)))
    for st, group in built.groupby("stratum"):
        for w in group.w.unique():
            assert min(abs(w - c) for c in doc[int(st)]) < 1e-9


@needs_cache
def test_every_respondent_lands_in_a_documented_design_cell(built):
    assert (built.design_cell != "UNMATCHED").all()
    assert built.design_cell.nunique() == 32


@needs_cache
def test_religion_values_come_only_from_the_documented_picklist(built):
    observed = set(built.rel_code.dropna().astype(int))
    assert observed <= set(A.RELIGION_CODES)
    assert set(built.religion.dropna()) <= set(A.RELIGION_GROUP.values())


@needs_cache
def test_employment_is_derived_only_from_documented_c1_codes(built):
    assert set(built.c1.dropna().astype(int)) <= set(A.C1_CODES)
    assert built.loc[built.c1 == 1, "employed"].eq(1).all()
    assert built.loc[built.c1.isin([2, 3, 4, 5, 6, 97]), "employed"].eq(0).all()
    assert built.loc[built.c1.isna(), "employed"].isna().all()


@needs_cache
def test_spouse_path_recovers_wage_reports_the_main_file_lacks(built):
    """Recovery is exhaustive over the universe the questionnaire actually allows.

    The recoverable universe is the spouse's G15, not the spouse's G1. Section G item G13
    (which leads to G15) is reached only "IF NOT MARRIED/PARTNERED OR G2=1: G21", so the
    spouse income block is skipped unless the respondent is married or partnered AND the
    spouse worked for pay. Measured on this file: 4,145 adults lack their own G7; 1,522 of
    them have a valid spouse G1, but only 848 reach the G13 branch (spouse G2 in {2,3}),
    849 have a valid G15 and 840 a usable yes/no. So 840, not ~1,500, is the ceiling.
    """
    own_missing = A.num(built.G7).isna()
    recovered = built.wage_src == "spouse Section G"
    usable_spouse_report = A.num(built.S_G15).isin([1, 2])
    # never overwrite a respondent's own answer
    assert (recovered & ~own_missing).sum() == 0
    # every recovered case really carries a usable spouse report
    assert (recovered & ~usable_spouse_report).sum() == 0
    # and every case that could be recovered was recovered
    assert recovered.sum() == (own_missing & usable_spouse_report).sum()
    # the G15 universe is strictly inside the G1 universe, per the G13 skip
    assert (own_missing & usable_spouse_report).sum() < (own_missing & A.num(built.S_G1).notna()).sum()
    assert recovered.sum() == 840  # regression guard on the verified count


# ------------------------------------------------------------------ gate outputs
@needs_derived
def test_g3_at_least_three_published_counts_reproduced_exactly():
    anc = pd.read_csv(DERIVED / "anchors.csv")
    assert int(anc.exact.sum()) >= 3
    for name in ["max |NISWGTSAMP1 - documented design weight|",
                 "distinct design weights reconstructed from Table 1",
                 "completed adult interviews (weights Table 1)"]:
        assert bool(anc.loc[anc.anchor == name, "exact"].iloc[0]), name


@needs_derived
def test_g5_reported_cells_have_n_at_least_50_and_finite_standard_errors():
    res = pd.read_csv(DERIVED / "earnings_gaps.csv", keep_default_na=False, na_values=[""])
    rep = res[res.reported.astype(str).str.lower() == "true"]
    assert len(rep) > 0
    assert (rep.n_cell >= 50).all()
    assert np.isfinite(rep.se.astype(float)).all()
    assert np.isfinite(rep.estimate.astype(float)).all()


@needs_derived
def test_audit_records_the_verified_zip_hash_and_every_code_list():
    audit = json.loads((DERIVED / "audit.json").read_text())
    assert audit["source_zip_sha256"] == A.ZIP_SHA256
    assert audit["gates"]["G1_zip_sha256"] == "PASS"
    for label in ["J30_1MO religion (RELPICK1)", "C1 current employment",
                  "CISCOBINSMO country of birth", "J14 how well speak English"]:
        assert label in audit["code_lists"] and audit["code_lists"][label]


@needs_derived
def test_muslim_and_christian_cells_clear_the_minimum_size():
    cells = pd.read_csv(DERIVED / "religion_cells.csv")
    cells = cells.set_index("group")
    for g in ["Muslim", "Christian", "Catholic", "Protestant", "Orthodox", "Hindu"]:
        assert cells.loc[g, "n_with_employment"] >= 50
        assert cells.loc[g, "n_with_earnings_C"] >= 50
