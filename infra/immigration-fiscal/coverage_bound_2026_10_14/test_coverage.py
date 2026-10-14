"""Negative controls for corrupt generation data, metadata, and cohort eligibility."""
import copy
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import coverage_bound as C
from export_pricing import validate_metadata
from source_tables import load, parse_row


def inputs():
    with C.GEN.open() as stream:
        rows = list(csv.DictReader(stream))
    return rows, json.loads(C.SUMMARY.read_text())


def test_principal_generation_positive_control():
    rows, summary = inputs()
    assert len(C.validate_generation_rows(rows, summary)) == 6


def test_duplicate_generation_blocks():
    rows, summary = inputs()
    rows.append(copy.deepcopy(rows[0]))
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] duplicate generation row"):
        C.validate_generation_rows(rows, summary)


@pytest.mark.parametrize("field,value", [("cost_bn", "nan"), ("cost_bn", "inf"), ("population", "nan"),
                                          ("population", "-inf"), ("population", "0"), ("population", "-1")])
def test_nonfinite_or_nonpositive_generation_blocks(field, value):
    rows, summary = inputs()
    rows[0][field] = value
    with pytest.raises(SystemExit, match=r"\[BLOCKED\]"):
        C.validate_generation_rows(rows, summary)


def test_generation_allocation_blocks():
    rows, summary = inputs()
    rows[0]["allocation"] = "shared"
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] mismatched generation allocation"):
        C.validate_generation_rows(rows, summary)


def test_generation_specification_blocks():
    rows, summary = inputs()
    summary["v7"]["end_specifications"]["set"] = [48, 11]
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] mismatched case specifications"):
        C.validate_generation_rows(rows, summary)


@pytest.mark.parametrize("field,value", [("allocation", "shared"), ("spec_index", {"low": 48, "high": 11}),
                                         ("case", "main_case_2026_10_07")])
def test_pricing_metadata_blocks(field, value):
    path = C.ROOT / "infra/immigration-fiscal/within_group_distribution_2026_09_29/_cache/oct14/lines.json"
    meta = json.loads(path.read_text())["meta"]
    meta[field] = value
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] mismatched"):
        validate_metadata(meta)


def test_later_births_postarrivals_and_nonhispanic_are_excluded():
    rates, base = load()
    data = {"age": np.array([0, 3, 4, 25, 25, 25]), "sex": np.ones(6, dtype=int),
            "generation": np.array([1, 2, 2, 0, 0, 1]), "arrival": np.array([0, 0, 0, 28, 26, 0]),
            "hispanic": np.array([True, True, True, True, True, False])}
    f, af = C.factors(data, rates, base)
    assert np.array_equal(f[[0, 1, 3, 5]], np.zeros(4))
    assert f[2] != 0  # age4's possible March2020 birth is modelled explicitly
    assert f[4] > 0
    assert not af.any()
    post, _ = C.factors(data, rates, base, arrival_arm="post_rate")
    assert post[3] > 0


def test_already_adjusted_children_use_residual_da():
    rates, base = load()
    r = C.rate_at(0, 1, rates, base)
    assert r == base[(0, 4, 1)]["da_middle"] / base[(0, 4, 1)]["base_hispanic"] - 1
    assert r < 0.01  # rejects reapplication of the original >7% child omission


def test_source_parser_rejects_missing_se():
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] coverage table row shape"):
        parse_row("Hispanic or Latino 94.2 0.1 -4.99", "Hispanic or Latino")


def test_output_interface_and_closure():
    path = Path(__file__).resolve().parent / "derived/coverage_bound.json"
    payload = json.loads(path.read_text())
    assert '"bound_bn"' not in path.read_text()
    assert '"case_with_bound_bn"' not in path.read_text()
    for end in C.ENDS:
        central = payload["scenarios"]["central"]
        assert abs(sum(p["coverage_bn"] for p in central["parts"][end].values())
                   - payload["ends"][end]["coverage_bn"]) < C.TOL


def test_public_output_finite():
    payload = json.loads((Path(__file__).resolve().parent / "derived/coverage_bound.json").read_text())
    for scenario in payload["scenarios"].values():
        for end in scenario["ends"].values():
            assert all(np.isfinite(end[k]) for k in ("coverage_bn", "case_with_coverage_bn", "cps_replicate_se_bn"))
