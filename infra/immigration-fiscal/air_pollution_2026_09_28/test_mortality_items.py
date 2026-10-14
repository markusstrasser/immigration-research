"""PM valuation edge cases and published producer control, without new output writes."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import mortality_items as M


def test_equal_mortality_risks_restore_exposure_self_share():
    """The correction must vanish when mortality composition is identical."""
    context = dict(local_odds_ratio=np.ones(81), national_rate_ratio=np.ones(81))
    L, iota, share = 0.35, 0.30, 0.12
    result = M.self_share(context, L, iota, share)
    np.testing.assert_allclose(result, L * iota + (1 - L) * share, rtol=0, atol=1e-15)


def test_no_group_and_all_group_limits_conserve_deaths():
    for exposure in (0.0, 1.0):
        for ratio in (0.01, 1.0, 100.0):
            assert abs(M.odds_adjust(exposure, ratio) - exposure) < 1e-15
    assert M.odds_adjust(0.2, 0.4) < 0.2 < M.odds_adjust(0.2, 2.0)


def test_life_year_reference_uses_the_common_crime_standard():
    years = M.V.reference_life_years()
    assert abs(M.V.mortality_value("dot_life_years", remaining_years=years) - M.V.dot_vsl()) < 1e-8
    with pytest.raises(ValueError, match="requires remaining years"):
        M.V.mortality_value("dot_life_years")


def test_stale_primary_source_fails_loudly(monkeypatch):
    monkeypatch.setattr(M, "digest", lambda path: "stale")
    with pytest.raises(ValueError, match="BLOCKED.*pinned"):
        M.verify_pins()


def test_current_row4_control_and_declared_lineage_transport():
    rows = pd.read_csv(M.OUT / "mortality_items.csv")
    context = json.loads((M.OUT / "mortality_context.json").read_text())
    current = pd.read_csv(M.FISCAL / "population_basis_2026_09_29/derived/reeval.csv").set_index("row")
    row4 = rows[(rows.population_basis == "row4") & (rows.item == "pm25_consumption_mortality")].iloc[0]
    assert abs(row4.frame_matched_original_bn - current.loc["pm25_consumption", "row4_bn"]) < 1e-9
    c = context["row4"]
    # Mortality is reweighted before shares; illness retains exposure dollars.
    morbidity = 1.03
    expected = row4.frame_matched_original_bn / morbidity * (
        c["receptor_mortality_scale"] * (1-c["self_share"]) / (1-c["old_exposure_self_share"]) + morbidity-1)
    assert abs(expected - row4.central_bn) < 1e-9
    line = rows[(rows.population_basis == "lineage_fixed_boundary") & (rows.item == "pm25_consumption_mortality")].iloc[0]
    assert abs(line.central_bn - row4.central_bn * context["lineage_fixed_boundary"]["factor"]) < 1e-9
    assert "receiver boundary remains identified union" in line.method_note


def test_receptor_risk_changes_total_before_shares():
    context = dict(local_odds_ratio=np.array([0.4]), national_rate_ratio=np.array([0.4]),
                   local_pop_self=np.array([0.2]), group=dict(pop=np.array([20.])), other=dict(pop=np.array([80.])))
    group, other, local, nonlocal_ = M.mortality_reweight(context, .35, .3, .224)
    assert group+other < 1
    assert abs(other-local-nonlocal_) < 1e-15
    # Lower group mortality cannot turn all previously group deaths into
    # outsider deaths merely by changing the denominator.
    assert other < 1-M.self_share(context, .35, .3, .224)
    context["local_odds_ratio"] = context["national_rate_ratio"] = np.ones(1)
    group, other, _, _ = M.mortality_reweight(context, .35, .3, .224)
    np.testing.assert_allclose(group+other, 1, atol=1e-15, rtol=0)
    np.testing.assert_allclose(other, 1-(.35*.3+.65*.224), atol=1e-15, rtol=0)


def test_cap_gap_cannot_be_mistaken_for_zero():
    caps = json.loads((M.OUT / "binding_caps.json").read_text())
    assert caps["binding_marginal_precursor_share"] is None
    assert caps["csapr_2024_12state_available_after_rule"] > caps["csapr_2024_12state_emissions"]
    assert caps["csapr_2024_12state_residual"] == caps["csapr_2024_12state_available_after_rule"] - caps["csapr_2024_12state_emissions"]
