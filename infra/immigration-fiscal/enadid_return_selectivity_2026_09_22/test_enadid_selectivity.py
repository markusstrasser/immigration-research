"""Re-read the committed artefacts and re-check every claim RESULT.md makes.

These tests do not recompute the survey estimates; they verify that the artefacts on
disk are internally consistent, carry the hashes the audit records, reproduce the
published anchors, and agree with the independently validated counts from the
acquisition lane infra/immigration-fiscal/enadid_2026_09_20/.

  uv run --no-project python3 -m pytest infra/immigration-fiscal/enadid_return_selectivity_2026_09_22/ -q
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

LANE = Path(__file__).resolve().parent
DERIVED = LANE / "derived"
BANDS = ["lt_lower_secondary", "lower_secondary", "upper_secondary", "tertiary"]


@pytest.fixture(scope="module")
def audit() -> dict:
    with open(DERIVED / "audit.json") as fh:
        return json.load(fh)


@pytest.fixture(scope="module")
def anchor() -> pd.DataFrame:
    return pd.read_csv(DERIVED / "anchor.csv")


@pytest.fixture(scope="module")
def returns() -> pd.DataFrame:
    return pd.read_csv(DERIVED / "return_migrants_by_schooling.csv")


@pytest.fixture(scope="module")
def departures() -> pd.DataFrame:
    return pd.read_csv(DERIVED / "departures_by_schooling.csv")


def test_artefacts_exist():
    for name in ("anchor.csv", "return_migrants_by_schooling.csv",
                 "departures_by_schooling.csv", "audit.json"):
        assert (DERIVED / name).is_file(), name


def test_output_hashes_match_audit(audit):
    for name, digest in audit["outputs"].items():
        actual = hashlib.sha256((DERIVED / name).read_bytes()).hexdigest()
        assert actual == digest, f"{name} changed since audit.json was written"


def test_acquisition_gates_all_pass(audit):
    assert audit["gates"] == {
        "bundle_hashes_match_frozen_manifest": True,
        "keys_unique": True,
        "row_counts_reproduced": True,
        "weights_strictly_positive": True,
    }


def test_input_row_counts_match_acquisition_lane(audit):
    expected = {"2018": (385978, 93, 2611, 55), "2023": (359018, 103, 3660, 52)}
    for year, (tr, tc, mr, mc) in expected.items():
        got = audit["inputs"][year]
        assert (got["tsdem_rows"], got["tsdem_cols"]) == (tr, tc)
        assert (got["tmigrante_rows"], got["tmigrante_cols"]) == (mr, mc)


def test_bundle_hashes_are_the_frozen_ones(audit):
    assert audit["inputs"]["2018"]["bundle_sha256"] == (
        "51d01ebd08996f41a781232ea14513a7c08e7c949bfe13b0a9e8cc5900cd8b13")
    assert audit["inputs"]["2023"]["bundle_sha256"] == (
        "248836ef8d4b74dda66d855b390e3557cdc79a1d487cd957b2273baa93ac4485")


def test_published_anchors_reproduce(anchor):
    assert len(anchor) == 8
    assert anchor["diff_pp"].abs().max() <= 0.06
    us = anchor[anchor["figure"].str.contains("destination was the US")]
    assert set(us["published_pct"]) == {84.8, 87.9}


def test_anchor_denominator_is_the_full_migrant_table(anchor):
    us = anchor.set_index("wave")
    rows = us[us["figure"].str.contains("destination was the US")]
    assert rows.loc[2018, "n_unweighted"] == 2611
    assert rows.loc[2023, "n_unweighted"] == 3660


def test_schooling_bands_sum_to_one(returns):
    band = returns[returns["measure"].isin(BANDS)
                   & (returns["group"] != "difference_returnee_minus_nonmigrant")]
    totals = band.groupby(["wave", "slice", "group"])["estimate"].sum()
    assert (totals - 1.0).abs().max() < 1e-9


def test_differences_equal_the_two_group_estimates(returns):
    wide = returns.pivot_table(index=["wave", "slice", "measure"], columns="group",
                               values="estimate")
    wide = wide.dropna(subset=["returnee_from_us", "non_migrant",
                               "difference_returnee_minus_nonmigrant"])
    implied = wide["returnee_from_us"] - wide["non_migrant"]
    assert (implied - wide["difference_returnee_minus_nonmigrant"]).abs().max() < 1e-9


def test_standard_errors_are_positive_and_finite(returns):
    se = returns.loc[returns["measure"].isin(BANDS + ["mean_years_schooling"]), "se"]
    assert se.notna().all() and (se > 0).all() and (se < 1e6).all()


def test_returnee_sample_sizes(returns):
    allslice = returns[(returns["slice"] == "all") & (returns["measure"] == "tertiary")]
    n = allslice.set_index(["wave", "group"])["n_unweighted"]
    assert n.loc[(2018, "returnee_from_us")] == 969
    assert n.loc[(2023, "returnee_from_us")] == 647
    assert n.loc[(2018, "non_migrant")] == 217171
    assert n.loc[(2023, "non_migrant")] == 208155


def test_headline_negative_selection_holds_in_both_waves(returns):
    d = returns[(returns["slice"] == "all")
                & (returns["group"] == "difference_returnee_minus_nonmigrant")]
    d = d.set_index(["wave", "measure"])
    for wave in (2018, 2023):
        tert = d.loc[(wave, "tertiary")]
        yrs = d.loc[(wave, "mean_years_schooling")]
        assert tert["estimate"] < 0 and abs(tert["estimate"]) > 2 * tert["se"]
        assert yrs["estimate"] < 0 and abs(yrs["estimate"]) > 2 * yrs["se"]


def test_women_returnees_are_not_distinguishable_from_non_migrant_women(returns):
    d = returns[(returns["slice"] == "sex:women")
                & (returns["group"] == "difference_returnee_minus_nonmigrant")
                & (returns["measure"] == "mean_years_schooling")].set_index("wave")
    for wave in (2018, 2023):
        assert abs(d.loc[wave, "estimate"]) < 2 * d.loc[wave, "se"]


def test_men_returnees_are_negatively_selected(returns):
    d = returns[(returns["slice"] == "sex:men")
                & (returns["group"] == "difference_returnee_minus_nonmigrant")
                & (returns["measure"] == "mean_years_schooling")].set_index("wave")
    for wave in (2018, 2023):
        assert d.loc[wave, "estimate"] < 0
        assert abs(d.loc[wave, "estimate"]) > 4 * d.loc[wave, "se"]


def test_weighted_counts_match_the_acquisition_lane(departures):
    w = departures[departures["measure"] == "weighted_count"].set_index(["wave", "group"])
    # infra/immigration-fiscal/enadid_2026_09_20/RESULT.md, "Weighted examples" table
    assert round(w.loc[(2018, "all_us_departures"), "estimate"]) == 645458
    assert round(w.loc[(2018, "returned"), "estimate"]) == 220218
    assert round(w.loc[(2023, "all_us_departures"), "estimate"]) == 1072331
    assert round(w.loc[(2023, "returned"), "estimate"]) == 215021


def test_tmigrante_has_no_schooling_variable(audit):
    for year in ("2018", "2023"):
        assert audit["tmigrante_schooling"][year]["has_schooling_variable"] is False


def test_only_returnees_can_be_linked_to_the_person_table(audit, departures):
    for year in ("2018", "2023"):
        assert audit["tmigrante_schooling"][year]["linked_rows_us_still_abroad"] == 0
    cov = departures[departures["measure"] == "linked_to_tsdem_coverage"]
    abroad = cov[cov["group"] == "still_abroad"]
    assert (abroad["n_unweighted"] == 0).all()
    assert not (departures["measure"].str.startswith("linked_schooling")
                & (departures["group"] != "returned")).any()


def test_linked_schooling_covers_most_returnees(departures):
    cov = departures[(departures["measure"] == "linked_to_tsdem_coverage")
                     & (departures["group"] == "returned")].set_index("wave")
    assert cov.loc[2018, "estimate"] > 0.9
    assert cov.loc[2023, "estimate"] > 0.9


def test_departure_shares_sum_to_one(departures):
    for measure in ("share_sex", "share_age_at_departure", "linked_schooling_share",
                    "linked_schooling_share_20_64"):
        sub = departures[departures["measure"] == measure]
        totals = sub.groupby(["wave", "group"])["estimate"].sum()
        assert (totals - 1.0).abs().max() < 1e-9, measure


def test_design_validation_agrees_with_bootstrap(audit):
    for year in ("2018", "2023"):
        v = audit["design_validation"][year]
        assert v["n_bootstrap_replicates"] >= 500
        assert v["relative_gap_bootstrap_vs_taylor_certainty"] < 0.06
        assert v["se_taylor_lonely_adjust"] >= v["se_taylor_lonely_certainty"] - 1e-12


def test_schooling_crosswalk_is_a_function_derived_from_inegis_own_grouping(audit):
    xw = audit["schooling_crosswalk"]
    assert xw["is_function"] is True
    assert xw["n_cells"] == 63
    assert set(xw["bands"]) == set(BANDS)
    assert all("|" in k for k in xw["map"])


def test_variable_map_records_the_wave_specific_question_numbers(audit):
    v = audit["variable_map"]
    assert v["2018"]["birthplace"] == "p3_7" and v["2018"]["prev5"] == "p3_19"
    assert v["2023"]["birthplace"] == "p3_10" and v["2023"]["prev5"] == "p3_24"
    assert v["2018"]["tmig_weight"] == "fac_viv"
    assert v["2023"]["tmig_weight"] == "fac_hog"
    assert v["2018"]["niv_esc"] in (None, "None")
    assert v["2023"]["niv_esc"] == "niv_esc"


def test_no_net_migration_quantity_is_produced(returns, departures):
    combined = set(returns["measure"]) | set(departures["measure"])
    assert not any("net" in m for m in combined)
