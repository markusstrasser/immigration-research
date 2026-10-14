"""Credit ownership regression checks, including cross-generation mixed returns."""
import gc
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("credit_routing", HERE / "credit_routing.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)


def test_linked_child_moves_dollars_and_claimant_weight_together():
    owner = np.array([[1, 0, 0], [0, 1, 0]], float)
    delta = C.transfer_owner(owner, np.array([0]), np.array([1]), np.array([0]),
                             np.array([True]), np.array([True, True]))
    got = C.weighted_delta(np.array([100.]), delta, np.array([[2., 3.]]))
    np.testing.assert_array_equal(got, [[-200., -300.], [200., 300.], [0., 0.]])
    np.testing.assert_array_equal(got.sum(axis=0), [0., 0.])


def test_childless_eitc_does_not_move():
    owner = np.array([[1, 0, 0], [0, 1, 0]], float)
    delta = C.transfer_owner(owner, np.array([0]), np.array([1]), np.array([0]),
                             np.array([False]), np.array([True, True]))
    assert not delta.any()


def test_nonmember_dependent_portion_preserves_union():
    owner = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]], float)
    delta = C.transfer_owner(owner, np.array([0]), np.array([1, 2]), np.array([0, 0]),
                             np.array([True, True]), np.array([True, True, False]))
    np.testing.assert_array_equal(delta[:, 0], [-.5, .5, 0.])


def test_nonmember_claimant_boundary_is_owned_by_item5b():
    owner = np.array([[0, 0, 0], [0, 1, 0]], float)
    delta = C.transfer_owner(owner, np.array([0]), np.array([1]), np.array([0]),
                             np.array([True]), np.array([False, True]))
    assert not delta.any()


def test_r6_keeps_joint_old_and_new_child_owners_on_mixed_return():
    owner_a = np.array([[0.], [.5], [.5]])
    locals_ = {"R":pd.DataFrame({"n_mem":[2]}), "drows":np.array([1,2]), "ri":np.array([0,0]),
               "dmem":np.array([True,True]), "dgen":np.array([1,2]),
               "owner":{"A_actc":owner_a}, "comp_ruled":{"A_actc":np.array([200.])},
               "side":{"A_actc":"spending"}, "keep_of":lambda *a:np.ones(1),
               "account":lambda x,k:np.full(161,x.sum())}
    source = {"parts":{f"A_spending_{g}":{"term":"A", "side":"spending", "generation":g,
                                         "bn":0. if g=="G1" else 100., "line":"refundable_tax_credits"}
                        for g in C.GENS}}
    omega_b = np.array([[1.,0.,0.],[1.,0.,0.],[0.,1.,0.]])
    parts, shifts = C.route_r6(locals_,{"b":omega_b},source)
    got = {x["part"]:x["per_generation_bn"] for x in parts}
    assert got["A_spending_G2"] == {"G1":100.,"G2":0.,"G3plus":0.}
    assert got["A_spending_G3plus"] == {"G1":0.,"G2":100.,"G3plus":0.}
    assert shifts == {"G1":{"bn":100.,"se_bn":0.},"G2":{"bn":0.,"se_bn":0.},"G3plus":{"bn":-100.,"se_bn":0.}}


def test_output_conserves_frozen_union_for_every_method_scenario_and_part():
    out = json.loads((HERE / "derived/credit_routing.json").read_text())
    original = json.loads((HERE.parent / "mixed_unit_credits_2026_10_14/derived/item.json").read_text())
    for method in C.METHODS:
        for conv in "ab":
            by = out["base"][method][conv]
            assert abs(sum(v["spending"]["refundable_tax_credits"]["personal"] for v in by.values())) < 1e-9
            scenarios = by["G1"]["receipt"]["federal_income_tax"]["personal"]
            assert len(scenarios) == 8
            for sc in scenarios:
                assert abs(sum(v["receipt"]["federal_income_tax"]["personal"][sc] for v in by.values())) < 1e-9
    assert {v["part"] for v in out["r6_b_parts"]} == set(original["parts"])
    for part in out["r6_b_parts"]:
        assert abs(sum(part["per_generation_bn"].values())-original["parts"][part["part"]]["bn"]) < 1e-9
    assert all(g["passed"] for g in out["gates"])
    assert sum(g["name"].endswith("source_positive_control") for g in out["gates"]) == 13


def test_source_cache_preserves_array_bytes_and_rejects_stale_or_corrupt_data(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "CACHE", tmp_path)
    directory = tmp_path / "source_replay"
    directory.mkdir()
    data = directory / "statistics.npz"
    values = np.array([[np.nextafter(1., 2.), -0.], [2.3, -4.7]])
    np.savez(data, sample=values)
    metadata = {"pins": {"source": "original"}, "data_sha256": C.sha(data)}
    (directory / "statistics.json").write_text(json.dumps(metadata))
    saved, arrays = C.read_source_statistics(metadata["pins"])
    assert saved == metadata
    assert arrays["sample"].tobytes() == values.tobytes()
    with pytest.raises(RuntimeError, match="provenance mismatch"):
        C.read_source_statistics({"source": "changed"})
    data.write_bytes(data.read_bytes() + b"corrupt")
    with pytest.raises(RuntimeError, match="provenance mismatch"):
        C.read_source_statistics(metadata["pins"])


def test_failed_source_subprocess_cannot_publish_credit_output(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(C, "OUT", tmp_path / "derived")
    monkeypatch.setattr(C, "pins", dict)
    def failed(command, *, check):
        assert check
        assert command[-1] == "--source-replay"
        raise C.subprocess.CalledProcessError(7, command)
    monkeypatch.setattr(C.subprocess, "run", failed)
    with pytest.raises(C.subprocess.CalledProcessError) as failure:
        C.main()
    assert failure.value.returncode == 7
    assert not C.OUT.exists()
    assert not (C.CACHE / "sufficient_statistics.json").exists()


def verify_actual_reads():
    """Pre-rerun proof: projected frames and blocked weights equal old reads."""
    reps = [f"pwwgt{i}" for i in range(161)]
    for path in (HERE.parent / "cps_imputation_keys_2026_09_23/_cache/asec25_lane.parquet",
                 HERE.parent / "external_benchmarks_2026_09_24/_cache/cps25_frame.parquet"):
        old = pd.read_parquet(path)
        expected = old.drop(columns=reps[1:])
        projected = C.frame_without_replicates(path, reps)
        assert expected.equals(projected)
        assert expected.dtypes.equals(projected.dtypes)
        weights = C.replicate_weights(path, reps)
        rebuilt = pd.DataFrame(weights, columns=reps, index=old.index)
        assert old[reps].equals(rebuilt)
        assert old[reps].dtypes.equals(rebuilt.dtypes)
        assert weights.flags.f_contiguous
        print(f"[equal-read] {path.name}: frame and all 161 weights equal; dtypes equal", flush=True)
        del old, expected, projected, weights, rebuilt
        gc.collect()
    print(f"[equal-read] peak_footprint_bytes={C.require_within_budget('read equality')}", flush=True)


if __name__ == "__main__":
    verify_actual_reads()
