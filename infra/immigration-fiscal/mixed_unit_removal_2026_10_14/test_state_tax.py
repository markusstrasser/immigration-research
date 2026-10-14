"""Independent source/kernel probes and mixed-return conservation checks."""
import json
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

import state_tax as st


def pair():
    zeros = np.zeros(2)
    d = pd.DataFrame({x: zeros.copy() for x in [
        "STATETAX_A", "SEMP_VAL", "FRSE_VAL", "DIV_VAL", "INT_VAL", "CAP_VAL",
        "RNT_VAL", "PNSN_VAL", "ANN_VAL", "SS_VAL", "UC_VAL"]})
    d["WSAL_VAL"], d["A_AGE"], d["GESTFIPS"] = [70000, 30000], [40, 39], [6, 6]
    d["STATETAX_A"] = [4000, 0]
    R = pd.DataFrame({"row": [0], "spouse": [1], "status": ["joint"], "depfiler": [False]})
    for label in ["all", "non"]:
        for key in ["n", "k13", "k17", "keitc"]:
            R[f"{key}_{label}"] = 0.0
    W = np.repeat(np.array([[2.0], [5.0]]), 161, axis=1)
    model = {"receipts": {"lines": [{"id": "state_local_income_tax", "national_bn": 100.0}]}}
    return d, R, W, model


def test_local_kernel_has_head_of_household_and_credit_identity():
    d, R, _, _ = pair()
    own = np.array([1])
    counts = {"n": np.array([1]), "k13": np.array([1]), "k17": np.array([1]), "keitc": np.array([1])}
    out = st.run_taxsim(st.taxsim_frame(d, R, own=own, dep_counts=counts))
    params = json.loads((st.LANE / "inputs/state_parameters_2024.json").read_text())["Federal"]
    hoh = [p["value"] for p in params if p["description"].strip().lower()
           == "standard deduction for head of household filers"]
    assert len(hoh) == 1
    assert out.v13.iloc[0] == hoh[0]
    assert out.actc.iloc[0] >= 0 and out.v25.iloc[0] >= 0
    # This kernel's named ACTC and EITC recover tax before refundable credits.
    assert out.fiitax.iloc[0] + out.actc.iloc[0] + out.v25.iloc[0] >= -0.011


def test_survivor_uses_own_income_and_is_head_spouse_symmetric():
    d, R, _, _ = pair()
    first = st.taxsim_frame(d, R, own=np.array([1]), label="non")
    R["row"], R["spouse"] = [1], [0]
    second = st.taxsim_frame(d, R, own=np.array([1]), label="non")
    pd.testing.assert_frame_equal(first, second)
    assert first.pwages.iloc[0] == 30000
    assert first.swages.iloc[0] == 0 and first.sage.iloc[0] == 0
    assert np.max(np.abs(st.run_taxsim(first).siitax - st.run_taxsim(second).siitax)) < 1e-9


def test_survivor_zero_income_does_not_keep_departing_income():
    d, R, _, _ = pair()
    d.loc[1, "WSAL_VAL"] = 0
    result = st.run_taxsim(st.taxsim_frame(d, R, own=np.array([1]), label="non"))
    assert result.v10.iloc[0] == 0
    assert max(result.siitax.iloc[0], 0) == 0


def test_state_bracket_tax_matches_primary_workbook_without_typed_rates():
    params = json.loads((st.LANE / "inputs/state_parameters_2024.json").read_text())["CA"]
    values = {p["parameter"]: p["value"] for p in params}
    # Independent integration of the Census workbook's original 2024 schedule.
    edges = np.array([float(x) for x in values["CUTOFF1"].split()])
    rates = np.array([float(x) for x in values["TAXRAT"].split()])
    taxable = 50000 - values["STD1"]
    expected = sum(rates[i] * np.clip(taxable - edges[i - 1], 0, edges[i] - edges[i - 1])
                   for i in range(1, len(edges)))
    out = st.run_taxsim(pd.DataFrame({"year": [2024], "mstat": [1], "statefip": [6],
                                      "pwages": [50000], "page": [40]}))
    assert out.staxbc.iloc[0] == pytest.approx(expected, abs=.011)


def test_compute_preserves_source_and_survivor_own_weights():
    d, R, W, model = pair()
    result = st.compute(d, R, None, None, W, np.array([True, False]), np.array([0, -1]),
                        np.array([False, False]), {"central": np.ones(2)}, model, civ=np.ones(2, bool))
    assert result["M2"].shape == (3, 161)
    details = result["details"]
    assert details["original_nonmember_positive_cps_bn"] == 0
    original = st.run_taxsim(st.taxsim_frame(d, R)).siitax.iloc[0]
    survivor = st.run_taxsim(st.taxsim_frame(d, R, own=np.array([1]), label="non")).siitax.iloc[0]
    expected = 100.0 * max(survivor, 0) / max(original, 0) * 5.0 / 2.0
    assert result["M2"][0, 0] == pytest.approx(expected, abs=1e-9)
    assert details["gates"]["state_calibration_closure_bn"] < 1e-6
    assert details["gates"]["generation_closure_bn"] < 1e-6
    assert details["union_se_bn"] == 0
    assert details["recommended_adopt"] is False


def test_departing_unauthorized_flag_does_not_shrink_legal_survivor():
    d, R, W, model = pair()
    args = (d, R, None, None, W, np.array([True, False]), np.array([0, -1]))
    normal = st.compute(*args, np.array([False, False]), {"central": np.array([.2, 1])}, model,
                        civ=np.ones(2, bool))
    flagged = st.compute(*args, np.array([True, False]), {"central": np.array([.2, 1])}, model,
                         civ=np.ones(2, bool))
    assert flagged["details"]["surviving_positive_calibrated_cps_bn"] == normal["details"]["surviving_positive_calibrated_cps_bn"]


def test_malformed_kernel_output_blocks(monkeypatch):
    monkeypatch.setattr(st.subprocess, "run", lambda *a, **k: SimpleNamespace(
        returncode=0, stdout="taxsimid,siitax\n1,0\n", stderr=""))
    with pytest.raises(RuntimeError, match="incomplete"):
        st.run_taxsim(pd.DataFrame({"year": [2024], "mstat": [1]}))


def test_nonzero_exit_blocks_even_if_output_looks_successful(monkeypatch):
    monkeypatch.setattr(st.subprocess, "run", lambda *a, **k: SimpleNamespace(
        returncode=1, stdout="taxsimid,siitax,fiitax,v25,actc,staxbc\n1,0,0,0,0,0\n", stderr=""))
    with pytest.raises(RuntimeError, match="exit 1"):
        st.run_taxsim(pd.DataFrame({"year": [2024], "mstat": [1]}))


def test_arbitrary_new_survivor_registry_needs_no_original_return():
    d, _, _, _ = pair()
    k = {x: np.zeros(2) for x in ["n", "k13", "k17", "keitc"]}
    f = st.taxsim_frame(d, None, own=np.array([0, 1]), dep_counts=k)
    assert list(f.pwages) == [70000, 30000]
    assert list(f.mstat) == [1, 1]


def test_transferred_child_changes_continuing_return_with_census_residual():
    d, R, _, model = pair()
    extra = d.iloc[[1]].copy()
    extra["WSAL_VAL"], extra["STATETAX_A"] = 100000, 5000
    d = pd.concat([d, extra], ignore_index=True)
    extraR = R.copy()
    extraR["row"], extraR["spouse"], extraR["status"] = 2, -1, "single"
    R = pd.concat([R, extraR], ignore_index=True)
    after = R.copy()
    after["row"], after["spouse"], after["status"] = [1, 2], [-1, -1], ["single", "hoh"]
    k = {x: np.array([0., 1.]) for x in ["n", "k13", "k17", "keitc"]}
    for key, value in k.items():
        after[f"{key}_all"] = value
    result = st.compute(d, R, None, None, np.ones((3, 161)), np.array([True, False, False]),
                        np.array([0, -1, -1]), np.zeros(3, bool), {"central": np.ones(3)}, model,
                        civ=np.ones(3, bool), refiling={"own": np.array([1, 2]), "dep_counts": k,
                                                     "R": after, "owner": np.array([[1, 1], [0, 0], [0, 0]])})
    assert result["details"]["additional_continuing_returns"] == 1
    assert result["remaining_state_liability"][1] < 5000
    assert result["remaining_state_live"].all()
    assert result["remaining_state_own"].tolist() == [1, 2]
    assert result["details"]["gates"]["generation_closure_bn"] < 1e-6


def test_shared_canonical_care_inputs_are_forwarded(monkeypatch):
    d, R, W, model = pair()
    before = st.taxsim_frame(d, R)
    after = st.taxsim_frame(d, R, own=np.array([1]), label="non")
    before["childcare"], after["childcare"] = 125.0, 25.0
    seen = []
    original = st.run_taxsim
    def record(frame):
        seen.append(frame.copy())
        return original(frame)
    monkeypatch.setattr(st, "run_taxsim", record)
    st.compute(d, R, None, None, W, np.array([True, False]), np.array([0, -1]),
               np.zeros(2, bool), {"central": np.ones(2)}, model, civ=np.ones(2, bool),
               refiling={"own": np.array([1]), "before_input": before, "after_input": after})
    assert seen[0].childcare.iloc[0] == 125.0
    assert seen[1].childcare.iloc[0] == 25.0
