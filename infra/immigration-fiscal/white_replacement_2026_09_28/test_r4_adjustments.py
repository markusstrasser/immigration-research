from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

import r4_adjustments as A


@pytest.fixture
def frame(monkeypatch):
    stored = {"states": [dict(state_fips=6, hispanic_minus_all_charged=200.,
                             nh_white_minus_all_charged=-100., black_minus_all_charged=300.)]}
    monkeypatch.setattr(A, "source_inputs", lambda: (stored, {6: 10000.}, 2., 1.01))
    A._FRAME_CACHE.clear()
    R = SimpleNamespace(K={"k12": np.array([0., 7500., 5000., 10000.])}, TARGET=100.,
                        K12_PART=.7, w=np.array([10., 20., 30., 40.]))
    dump = {basis: {end: {"lines": [dict(side="spending", id="education_services", national_bn=.002)]}
                    for end in ("low", "high")} for basis in ("cash", "accrual")}
    W = SimpleNamespace(STATE=np.array([6] * 4), META={"responses": {"row8_factor": .95}}, DUMP=dump)
    extra = pd.DataFrame({"PEHSPNON": [2, 1, 2, 2], "PRDTRACE": [1, 1, 2, 4]})
    sc = dict(cps_w=np.array([10., 20., 30., 40.]), population=100.)
    return R, W, extra, sc


def test_raw_weights_own_race_and_unmeasured(frame):
    out = A.scenario_adjustments(*frame)
    assert out["district_raw_bn"] == pytest.approx(7500 / 1e9)
    assert out["district_price_scale"] == pytest.approx(2.)
    assert out["district_bn"] == pytest.approx(15000 / 1e9)
    assert out["row8_bn"] == pytest.approx(1.9)
    assert out["pupil_count"] == 70
    assert out["nh_other_unmeasured_pupils"] == 40
    assert out["black_multiracial_proxy_pupils"] == 0


def test_reweighted_block_is_linear_and_does_not_change_cost(frame):
    R, W, extra, sc = frame
    sc["cost"] = 123.
    base = A.scenario_adjustments(R, W, extra, sc)
    sc2 = dict(sc, cps_w=sc["cps_w"] * 2, population=200.)
    scaled = A.scenario_adjustments(R, W, extra, sc2)
    for name in base:
        assert scaled[name] == pytest.approx(base[name] * (1 if name == 'district_price_scale' else 2))
    assert sc["cost"] == 123.
    assert len(A._FRAME_CACHE) == 1


def test_current_row8_factor_and_identified_denominator_are_live(frame):
    R, W, extra, sc = frame
    A.scenario_adjustments(*frame)
    R.TARGET = 50.
    W.META["responses"]["row8_factor"] = .9
    assert A.scenario_adjustments(R, W, extra, sc)["row8_bn"] == pytest.approx(3.6)


def test_mismatched_population_fails(frame):
    R, W, extra, sc = frame
    with pytest.raises(SystemExit, match="population differs"):
        A.scenario_adjustments(R, W, extra, dict(sc, population=99.))


def test_source_declarations_are_current():
    # Raw-source national known controls belong to district_prices tests.
    stored, prices, constant, factor = A.source_inputs()
    assert constant == 2.
    assert len(prices) == 51
    assert factor == pytest.approx(1.0056797155994412)
    assert round(stored["national_dollars_per_pupil"]["nh_white"]["charged"], 1) == -623.7


def test_principal_national_mismatch_fails(frame):
    R, W, extra, sc = frame
    W.DUMP['accrual']['high']['lines'][0]['national_bn'] *= 2
    with pytest.raises(SystemExit, match='national differs'):
        A.scenario_adjustments(R, W, extra, sc)


def test_national_calibration_uses_full_frame_not_scenario(frame):
    R, W, extra, sc = frame
    all_people = A.scenario_adjustments(R, W, extra, sc)
    some = dict(cps_w=np.array([0., 20., 0., 0.]), population=20.)
    out = A.scenario_adjustments(R, W, extra, some)
    assert out['district_price_scale'] == all_people['district_price_scale']
    assert out['district_bn'] == pytest.approx(20 * .75 * 200 * 2 / 1e9)


def test_empty_national_exposure_fails(frame):
    R, W, extra, sc = frame
    R.w = np.zeros(4)
    with pytest.raises(SystemExit, match='empty national school'):
        A.scenario_adjustments(R, W, extra, sc)
