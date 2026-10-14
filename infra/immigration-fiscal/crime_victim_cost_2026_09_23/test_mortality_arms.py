import numpy as np
import pandas as pd
import pytest

import mortality_arms as arms
import vsl_standard as vsl


def test_life_years_fail_without_explicit_years_and_unknown_standards():
    with pytest.raises(ValueError, match="requires remaining years"):
        vsl.mortality_value("dot_life_years")
    with pytest.raises(ValueError, match="unknown vsl_standard"):
        vsl.mortality_value("missing")


def test_shared_calibration_reproduces_dot():
    reference = vsl.remaining_years(vsl.REFERENCE_AGE)
    assert vsl.mortality_value("dot_life_years", remaining_years=reference) == pytest.approx(vsl.dot_vsl())


def test_mortality_replacement_preserves_counts_nonfatal_and_has_no_earnings_addition():
    legacy = arms.active_victim_detail("mixed", "legacy")
    dot = arms.active_victim_detail("mixed", "dot_uniform")
    assert np.array_equal(legacy.outside_victims, dot.outside_victims)
    murder = dot.offence.eq("Murder")
    assert np.array_equal(legacy.loc[~murder, "cost_full"], dot.loc[~murder, "cost_full"])
    assert np.all(dot.loc[murder, "unit_full"] == vsl.dot_vsl())


def test_high_end_mixed_correction_uses_the_same_custody_multiplier():
    equal = arms.active_victim_detail("equal", "legacy")
    mixed = arms.active_victim_detail("mixed", "legacy")
    custody = arms.active_victim_detail("custody", "legacy")
    vc, _ = arms.context()
    ratio = vc.institutional_ratio()["ratio_generic_reallocated"]
    assert custody.cost_full.sum() == pytest.approx(mixed.cost_full.sum() * ratio, abs=1e-6)
    assert custody.cost_full.sum() - equal.cost_full.sum() * ratio == pytest.approx(
        (mixed.cost_full.sum() - equal.cost_full.sum()) * ratio, abs=1e-6)


def test_age_missingness_bounds_and_discount_sensitivity():
    profile = arms.victim_age_profile()
    assert np.all(profile.missing_age_low_years <= profile.remaining_years)
    assert np.all(profile.missing_age_high_years >= profile.remaining_years)
    assert np.all(profile.known_age_records + profile.missing_age_records == profile.all_records)
    for victim, rows in profile.groupby("victim"):
        assert rows.set_index("real_discount_rate").loc[0.03, "remaining_years"] < rows.set_index("real_discount_rate").loc[0.0, "remaining_years"]


@pytest.mark.parametrize("footing,standard,historical", [
    ("envelope_low_unmixed", "legacy", "ENVELOPE low, miller2021"),
    ("envelope_high_unmixed", "dot_uniform", "ENVELOPE high, miller2021_dot_vsl"),
])
def test_unmixed_envelopes_reproduce_native_prices_and_isolate_mixed_changes(footing, standard, historical):
    held = pd.read_csv(arms.OUT / "arms.csv").set_index("arm")
    unchanged = arms.active_victim_detail(footing, standard)
    assert round(unchanged.cost_full.sum() / 1e9, 4) == held.loc[historical, "full_bn"]
    mixed = arms.active_victim_detail(footing.removesuffix("_unmixed"), standard)
    homicide = unchanged.offence.eq("Murder")
    assert np.array_equal(unchanged.loc[homicide, "cost_full"], mixed.loc[homicide, "cost_full"])
    assert np.array_equal(unchanged.unit_full, mixed.unit_full)
    assert mixed.cost_full.sum() > unchanged.cost_full.sum()
