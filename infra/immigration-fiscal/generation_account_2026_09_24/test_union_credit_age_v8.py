"""Actual-age owner differences and fail-before-publication regression gates."""
import ast
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import union_credit_age_v8 as U


def test_actual_adult_dependent_and_minor_head_keep_source_owners():
    # Eligible dependent age20 is an adult; age16 claimant stays a minor.
    state = dict(d=pd.DataFrame({"A_AGE": [16, 20, 10]}), drows=np.array([1, 2]),
                 ri=np.array([0, 0]), dmem=np.array([True, True]), dgen=np.array([1, 1]),
                 R=pd.DataFrame({"gen_h": [1]}), h=np.array([0]), n_mem=np.array([2]),
                 owner={k: np.array([[0.], [1.], [0.]]) for k in ["A_actc", "B_eitc", "C_status", "Cr_status"]},
                 comp_ruled={k: np.array([8.]) for k in ["A_actc", "B_eitc", "C_status", "Cr_status"]},
                 side={"A_actc": "spending", "B_eitc": "spending", "C_status": "receipts", "Cr_status": "receipts"},
                 keep_of=lambda *_: np.array([1.]),
                 account=lambda amount, _: np.array([amount.sum()] * 161))
    result = U.capture_age(state, list(state["owner"]))
    assert result["spending"]["G2_adult"] == [4.] * 161
    assert result["spending"]["G2_minor"] == [12.] * 161
    assert result["receipts"]["G2_adult"] == [-4.] * 161
    assert result["receipts"]["G2_minor"] == [-12.] * 161


def test_source_capture_is_bounded_to_two_arms():
    function = next(n for n in ast.parse(U.SOURCE.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "compute")
    adapter = U.Capture()
    function = adapter.visit(function)
    assert (adapter.matches, adapter.loops) == (1, 1)
    compile(ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[])), str(U.SOURCE), "exec")


def test_missing_or_stale_arrays_fail():
    with pytest.raises(ValueError, match="credit161"):
        U.finite161([0.] * 160)
    with pytest.raises(ValueError, match="credit161"):
        U.finite161([float("nan")] * 161)
    with pytest.raises(ValueError, match="stale"):
        U.check_sources({str(Path(U.__file__)): "bad-sha"})


def test_failed_budget_never_replaces_output(tmp_path):
    target = tmp_path / "actual.json"
    target.write_text("previous valid bytes")
    result = dict(source_sha256={}, expanded_minus_canonical={
        side: {cell: [0.] * 161 for cell in U.CELLS} for side in ("receipts", "spending")})
    def reject(_):
        raise RuntimeError("[BLOCKED] physical footprint")
    with pytest.raises(RuntimeError, match="physical"):
        U.publish(result, target, reject)
    assert target.read_text() == "previous valid bytes"
    result["expanded_minus_canonical"]["receipts"]["G2_adult"] = [0.] * 160
    with pytest.raises(ValueError, match="credit161"):
        U.publish(result, target)
    assert target.read_text() == "previous valid bytes"
    result["source_sha256"] = {str(Path(U.__file__)): "stale"}
    with pytest.raises(ValueError, match="stale"):
        U.publish(result, target)
    assert target.read_text() == "previous valid bytes"
