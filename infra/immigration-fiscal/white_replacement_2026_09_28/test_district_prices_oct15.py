"""The raw-vintage parity check is build(); these verify the scenario adapter."""
import numpy as np
import pytest

import district_prices_oct15 as D


@pytest.fixture
def prices():
    return {"states": [dict(state_fips=6, hispanic_minus_all_charged=200.,
                            nh_white_minus_all_charged=-100., black_minus_all_charged=300.),
                       dict(state_fips=50, hispanic_minus_all_charged=0.,
                            nh_white_minus_all_charged=0., black_minus_all_charged=0.)]}


def test_child_takes_own_race_and_state(prices):
    # White adult's Hispanic child and Black child carry their own prices.
    states, races = [6, 6, 6, 50], ["nh_white", "hispanic", "black", "black"]
    pupils, weights = [0., .75, .5, 1.], [10., 20., 30., 40.]
    assert D.adjustment_bn(states, races, pupils, weights, prices) == pytest.approx(7500 / 1e9)
    reps = np.array([weights, np.array(weights) * .5]).T
    assert np.allclose(D.adjustment_bn(states, races, pupils, reps, prices), [7500 / 1e9, 3750 / 1e9])


def test_zero_unmeasured_race_is_explicit(prices):
    assert D.per_pupil_rates([6], ["nh_other"], prices)[0] == 0


@pytest.mark.parametrize("states,races", [([99], ["black"]), ([6], ["unknown"]), ([6, 6], ["black"])])
def test_unknown_inputs_fail(states, races, prices):
    with pytest.raises(SystemExit, match="BLOCKED"):
        D.per_pupil_rates(states, races, prices)


def test_probabilities_cannot_be_dollar_exposure(prices):
    with pytest.raises(SystemExit, match="invalid pupil probability"):
        D.adjustment_bn([6], ["nh_white"], [20000], [1], prices)


def test_real_output_keeps_ledger_state_parity():
    import pandas as pd
    stored = D.load()
    D.validate_ledger(pd.DataFrame(stored["states"]))
    assert stored["counts"] == dict(joined=13639, dropped_missing=395, dropped_implausible=97, kept=13147)
    assert stored["national_dollars_per_pupil"]["hispanic"]["raw"] == pytest.approx(473.8804391016793)
    assert stored["national_dollars_per_pupil"]["nh_white"]["raw"] == pytest.approx(-624.6240094310522)
    assert round(stored["national_dollars_per_pupil"]["hispanic"]["charged"], 1) == 473.8
    assert round(stored["national_dollars_per_pupil"]["nh_white"]["charged"], 1) == -623.7
