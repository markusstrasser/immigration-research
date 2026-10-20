"""Actual credit covariance and age-owner contracts for the oct15 sidecar."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import json

import credit_routing as C
import numpy as np
import pandas as pd
import pytest


def test_actual_age_ownership_keeps_adult_student_and_minor_distinct():
    d = pd.DataFrame({"A_AGE":[40,18,16]})
    own = np.array([[0,1,0],[0,1,0],[0,1,0]],float)
    cells = C.age_ownership(d,{"a":own})["a_age"]
    delta = C.transfer_owner(cells,np.array([0]),np.array([1,2]),np.array([0,0]),
                             np.array([True,True]),np.ones(3,bool))
    assert np.array_equal(delta[:,0],[0,0,-.5,.5,0,0])
    assert np.array_equal(delta.reshape(3,2,1).sum(axis=1),np.zeros((3,1)))


def test_mean_161_keeps_cross_method_covariance():
    drift = np.r_[0.,np.ones(160)]
    spend = {C.METHODS[0]:{"a":np.stack([drift,-drift,np.zeros(161)])},
             C.METHODS[1]:{"a":np.stack([-drift,drift,np.zeros(161)])}}
    receipt = {"a":np.zeros((3,161))}
    line = {"_reference":"s", "cells":{"s":{"personal":{"target_bn":1.}}}}
    out = C.mean_credit_replicates(spend,receipt,line,["s"],["a"])
    assert C.sdr(spend[C.METHODS[0]]["a"][0]) == 2
    assert C.sdr(out["a"]["G1"]["s"]) == 0


def test_r6_actual_age_assigns_d_receipt_to_member_spouse():
    # The nonmember head's record must not receive the member spouse's D tax.
    own = np.array([[0,0,0,0,0,0],[0,0,1,0,0,0]],float)
    local = {"R":pd.DataFrame({"n_mem":[0],"spouse":[1]}),
             "drows":np.array([],int),"ri":np.array([],int),"dmem":np.array([],bool),
             "dgen":np.array([],int),"h":np.array([0]),"dm1":np.array([True]),"dm2":np.array([False]),
             "owner":{"D_receipts":np.array([[0],[1],[0]],float)},
             "comp_ruled":{"D_receipts":np.array([20.])},"side":{"D_receipts":"receipts"},
             "keep_of":lambda *args:np.ones(1),"account":lambda x,k:np.full(161,x.sum())}
    source = {"parts":{"D_receipt_G2":{"term":"D","side":"receipt","generation":"G2","bn":-20.}}}
    out = C.route_r6_age(local,{"a_age":own},source)["a_age"]["D_receipt_G2"]
    assert out["G2_adult"] == [-20.]*161
    assert sum(np.asarray(v) for v in out.values()).tolist() == [-20.]*161


def test_failed_replicate_source_cannot_publish(tmp_path,monkeypatch):
    monkeypatch.setattr(C,"CACHE",tmp_path/"cache")
    monkeypatch.setattr(C,"OUT",tmp_path/"derived")
    monkeypatch.setattr(C,"pins",dict)
    monkeypatch.setattr(sys,"argv",["credit_routing.py","--export-oct15-replicates","--refresh"])
    def fail(command,*,check):
        assert check and "--source-replay" in command
        raise C.subprocess.CalledProcessError(7,command)
    monkeypatch.setattr(C.subprocess,"run",fail)
    with pytest.raises(C.subprocess.CalledProcessError):
        C.main()
    assert not C.OUT.exists()
    assert not (C.CACHE/"sufficient_statistics_oct15.json").exists()


def test_cache_rejects_old_schema_corruption_and_missing_real_replicates(tmp_path,monkeypatch):
    monkeypatch.setattr(C,"OUT",tmp_path)
    (tmp_path/"credit_routing.json").write_text("frozen source")
    out = {"replicate_contract":C.OUTPUT_VERSION,
           "meta":{"frozen_credit_routing_sha256":C.sha(tmp_path/"credit_routing.json")},
           "r6_age_parts_edit_bn":{},"mean_base_credit_spending_bn":{},
           "mean_base_credit_net_cost_bn":{},"base_credit_receipt_edit_bn":{}}
    for conv in ("a","b","a_age","b_age"):
        cells = C.AGE_CELLS if conv.endswith("_age") else C.GENS
        out["mean_base_credit_spending_bn"][conv] = {g:[0.]*161 for g in cells}
        out["mean_base_credit_net_cost_bn"][conv] = {g:{"s":[0.]*161} for g in cells}
        out["base_credit_receipt_edit_bn"][conv] = {g:{"s":[0.]*161} for g in cells}
    saved = {"pins":{},"replicate_contract":C.OUTPUT_VERSION,"output":out,"output_sha256":C.output_digest(out)}
    assert C.export_cache_valid(saved,{})
    saved["replicate_contract"] = 1
    assert not C.export_cache_valid(saved,{})
    saved["replicate_contract"] = C.OUTPUT_VERSION
    out["mean_base_credit_spending_bn"]["a"]["G1"][0] = 1
    assert not C.export_cache_valid(saved,{})  # Payload SHA rejects unrecorded changes.
    out["mean_base_credit_spending_bn"]["a"]["G1"].pop()
    saved["output_sha256"] = C.output_digest(out)
    assert not C.export_cache_valid(saved,{})  # Even a fresh SHA cannot admit 160-only data.


def test_source_contract_rejects_changed_source_algorithm(tmp_path, monkeypatch):
    directory = tmp_path
    pins = {"generation_account_2026_09_24/credit_routing.py": "recorded-producer", "source.py": "source-bytes"}
    metadata = {"pins": pins, "data_sha256": "recorded-statistics"}
    source = C.ast.parse(Path(C.__file__).read_text())
    route = next(n for n in source.body if isinstance(n, C.ast.FunctionDef) and n.name == "route_r6")
    contract = {"producer_sha256": pins["generation_account_2026_09_24/credit_routing.py"],
                "data_sha256": metadata["data_sha256"], "source_functions": ["route_r6"],
                "source_constants": {"GENS": list(C.GENS), "AGE_CELLS": list(C.AGE_CELLS), "REPLICATE_VERSION": C.REPLICATE_VERSION},
                "source_algorithms_sha256": C.hashlib.sha256(C.ast.dump(route, include_attributes=False).encode()).hexdigest()}
    (directory / "algorithm_contract.json").write_text(json.dumps(contract))
    assert C.source_algorithm_cache_valid(metadata,pins,directory)
    assert not C.source_algorithm_cache_valid(metadata, {**pins, "source.py": "changed-source"}, directory)
    parse = C.ast.parse
    def changed(text):
        tree = parse(text)
        route = next(n for n in tree.body if isinstance(n,C.ast.FunctionDef) and n.name=="route_r6")
        route.body.append(C.ast.Return(value=C.ast.Constant(value=0)))
        return tree
    monkeypatch.setattr(C.ast,"parse",changed)
    assert not C.source_algorithm_cache_valid(metadata,pins,directory)
