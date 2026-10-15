"""Producer-grounded spending geography, including signed prison corrections."""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import p8_recipient_keys as K


FISCAL = Path(__file__).resolve().parent.parent


def fixture_sources(tmp_path, *, include_dc=False, police=False):
    lane = tmp_path / "state_priced_services_2026_09_29/derived"
    lane.mkdir(parents=True)
    states = [6, 48] + ([11] if include_dc else [])
    pd.DataFrame(dict(year=2024, basis="direct", fips=states, function="police",
                      relative=[1.2, 1.1] + ([1.0] if include_dc else []), population=100))\
        .to_csv(lane / "state_per_capita.csv", index=False, lineterminator="\n")
    parts = [dict(line="public_order_safety", function="corrections_per_inmate",
                  sl_amount_bn=10, candidate=True)]
    if police:
        parts.append(dict(line="public_order_safety", function="police",
                          sl_amount_bn=10, candidate=True))
    pd.DataFrame(parts).to_csv(lane / "corrections.csv", index=False, lineterminator="\n")
    pd.DataFrame(dict(fips=[6, 48], relative=[2, 0.5], prisoners=[1, 3]))\
        .to_csv(lane / "prison_cost_by_state.csv", index=False, lineterminator="\n")
    school = tmp_path / "school_cost_where_enrolled_2026_09_24/derived"
    school.mkdir(parents=True)
    pd.DataFrame(dict(fips=states, group_spending_per_pupil=100, assf_per_pupil=100,
                      account_group_pupils=10, admin_group_pupils=10,
                      group_pupils_admin_over_account=1))\
        .to_csv(school / "state_breakdown.csv", index=False, lineterminator="\n")
    return pd.DataFrame(dict(st=states, A_AGE=40, target=True, A_ENRLW=0,
                             A_HSCOL=0, MCAID=0))


def cost_by_programme(audit, name):
    return {r["state"]: r["cost_bn"] for r in audit["programme_state_rows"]
            if r["programme"] == name}


def test_prison_rate_changes_sign_and_preserves_negative_state_correction(tmp_path):
    d = fixture_sources(tmp_path)
    programmes = [dict(id="public_order_safety", state_local_bn=100),
                  dict(id="state_price_public_order_safety", state_local_bn=-1.25)]
    shares, audit = K.state_spending_shares(d, np.ones(2), programmes, tmp_path, "low")
    # Equal group populations but 1:3 imprisonment: cost gaps are
    # 10×1/4×(2−1)=+2.5 and 10×3/4×(0.5−1)=−3.75.
    # Population-only prison pricing would instead produce a positive total.
    assert cost_by_programme(audit, "public_order_safety") == {6: 50, 48: 50}
    assert cost_by_programme(audit, "state_price_public_order_safety") == pytest.approx({6: 2.5, 48: -3.75})
    assert shares == pytest.approx({6: 52.5 / 98.75, 48: 46.25 / 98.75})
    assert audit["spending_bn"] == pytest.approx(98.75)


def test_other_pos_parts_keep_population_geography_and_parent_is_not_repriced(tmp_path):
    d = fixture_sources(tmp_path, police=True)
    programmes = [dict(id="public_order_safety", state_local_bn=100),
                  dict(id="state_price_public_order_safety", state_local_bn=0.25)]
    _, audit = K.state_spending_shares(d, np.ones(2), programmes, tmp_path, "central")
    assert cost_by_programme(audit, "public_order_safety") == {6: 50, 48: 50}
    assert cost_by_programme(audit, "state_price_public_order_safety") == pytest.approx({6: 3.5, 48: -3.25})
    police = [r for r in audit["price_component_state_rows"] if r["function"] == "police"]
    assert [r["use_share"] for r in police] == [0.5, 0.5]


def test_dc_has_no_state_prison_correction_and_no_silent_other_state_fill(tmp_path):
    d = fixture_sources(tmp_path, include_dc=True)
    programmes = [dict(id="public_order_safety", state_local_bn=100),
                  dict(id="state_price_public_order_safety", state_local_bn=-1.25)]
    _, audit = K.state_spending_shares(d, np.ones(3), programmes, tmp_path, "high")
    assert cost_by_programme(audit, "state_price_public_order_safety")[11] == 0
    d.loc[d.st.eq(11), "st"] = 32
    with pytest.raises(ValueError, match="missing state imprisonment input"):
        K.state_spending_shares(d, np.ones(3), programmes, tmp_path, "high")


def test_real_prison_geography_recovers_producer_central_index():
    source = FISCAL / "state_priced_services_2026_09_29/derived"
    gp = pd.read_csv(source / "group_population_by_state.csv")
    d = pd.DataFrame(dict(st=gp.fips, A_AGE=40, target=True, A_ENRLW=0, A_HSCOL=0, MCAID=0))
    parts = pd.read_csv(source / "corrections.csv")
    row = parts[parts.function.eq("corrections_per_inmate")].iloc[0]
    programmes = [dict(id="public_order_safety", state_local_bn=100),
                  dict(id="state_price_public_order_safety", state_local_bn=6.4)]
    shares, audit = K.state_spending_shares(d, gp.group.to_numpy(), programmes, FISCAL, "central")
    prison = [r for r in audit["price_component_state_rows"] if r["function"] == "corrections_per_inmate"]
    reproduced = 1 + sum(r["correction_mass"] for r in prison) / row.sl_amount_bn
    assert reproduced == pytest.approx(row["index"], abs=2e-8)
    assert sum(r["use_share"] for r in prison) == pytest.approx(1)
    assert sum(shares.values()) == pytest.approx(1)
    assert {r["state"]: r["correction_mass"] for r in prison}[11] == 0


def test_school_base_price_and_signed_correction_are_separate(tmp_path):
    d = fixture_sources(tmp_path)
    d["A_AGE"] = 10
    school = tmp_path / "school_cost_where_enrolled_2026_09_24/derived"
    pd.DataFrame(dict(fips=[6, 48], assf_per_pupil=[100, 300],
                      group_spending_per_pupil=[110, 280], account_group_pupils=10,
                      admin_group_pupils=10, group_pupils_admin_over_account=1))\
        .to_csv(school / "state_breakdown.csv", index=False, lineterminator="\n")
    (school / "within_district.json").write_text('{"TCURELSCS":{"factor_all_districts":1}}\n')
    programmes = [dict(id="education_k12", state_local_bn=400),
                  dict(id="school_reprice", state_local_bn=-10)]
    shares, audit = K.state_spending_shares(d, np.ones(2), programmes, tmp_path, "high")
    assert cost_by_programme(audit, "education_k12") == pytest.approx({6: 100, 48: 300})
    assert cost_by_programme(audit, "school_reprice") == pytest.approx({6: 10, 48: -20})
    assert shares == pytest.approx({6: 110 / 390, 48: 280 / 390})
    assert any(s.startswith("[DEGRADED]") for s in audit["notices"])
    assert str(school / "within_district.json") in audit["source_paths"]
