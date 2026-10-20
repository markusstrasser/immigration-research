"""Live-case population and worktree provenance regressions."""
import json
from types import SimpleNamespace

import numpy as np
import pandas as pd

import winners_losers as wl


def test_observed_calibration_applies_once_and_holds_latent_addition(monkeypatch):
    import p9_calibration
    d = pd.DataFrame(dict(target=[True, True, True], target_oct14=[True, True, False],
        pw=[8., 18., 22.5], pw_production=[10., 20., 30.], PH_SEQ=[1, 2, 3], PPPOS=[1, 1, 1],
        PRCITSHP=[1, 1, 1], PEMNTVTY=[57, 57, 57], PEFNTVTY=[57, 57, 57], PRDTHSP=[1, 1, 1]))
    payload = dict(meta=dict(lineage=dict(counts=dict(added=15.)),
        union_completion=dict(observed_records=[dict(PH_SEQ=3, PPPOS=1)]),
        population_v9=dict(without_coverage=63.5, with_coverage=67.5, coverage=4.)))
    monkeypatch.setattr(wl, "CASE", dict(case="oct16", population_key="population_v9"))
    monkeypatch.setattr(wl, "read_input", lambda key: json.dumps(payload).encode())
    monkeypatch.setattr(wl, "row4_group_weights", lambda *args: (np.array([10., 20., 30.]), {}))
    monkeypatch.setattr(wl, "age_band_factors", lambda *args: (np.array([1.5, 1.5, 1.]), {}))
    monkeypatch.setattr(p9_calibration, "observed_factors", lambda frame: np.array([.8, .9, .75]))
    weights, info = wl.completed_group_weights(SimpleNamespace(), d)
    np.testing.assert_allclose(weights, [13., 28., 22.5])
    assert info["members_m"] == 63.5 / 1e6
    assert info["coverage_unlocated_m"] == 4. / 1e6


def test_live_case_and_population_contract_are_explicit():
    assert wl.parse_args([]).case == "oct16"
    assert wl.RUNNABLE == ("oct16",)
    assert wl.CASES["oct16"]["population_key"] == "population_v9"
    assert wl.CASES["oct16"]["prev"] == "oct15"
