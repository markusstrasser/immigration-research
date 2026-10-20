"""Paired budget counterflows and live source rows must close independently."""
import gzip
import json

import numpy as np
import pandas as pd
import pytest

import p7_frames as p7
from p8_social import amounts, normalized, SOURCE_REL


def test_round3_rows_close_and_keep_paired_pm_flows_separate():
    from pathlib import Path
    data = json.loads((Path(__file__).resolve().parent.parent / SOURCE_REL).read_text())
    rows = amounts(data)
    from p8_social import environment
    env = environment(data)
    for end in ("low", "high"):
        assert abs(sum(v[end] for v in rows.values()) - env["current_social_by_end_bn"][end]) < 1e-9
        assert rows["pm25_respending"][end] < 0 < rows["pm25_government_side"][end]
        neither = amounts(data, "neither_budget_side")
        assert abs(neither["pm25_respending"][end]) < 1e-12
        assert abs(neither["pm25_government_side"][end]) < 1e-12
    adapted = normalized(data)
    assert len(adapted["lineage_social_rows"]["rows"]) == len(rows)
    # The v9 producer does not publish this v8 justice companion. Check its
    # retained historical contract separately; never substitute it into v9.
    historical = json.loads((Path(__file__).resolve().parent.parent /
        "sept24_propagation_2026_09_24/derived/oct15/real_costs_totals.json").read_text())
    matched = amounts(historical, "matched_justice_footing")
    assert matched["variant_fiscal_justice"]["high"] == 0.
    with pytest.raises(KeyError, match="matched_justice_footing"):
        amounts(data, "matched_justice_footing")
    legacy = amounts(data, "government_legacy_response")
    assert "variant_unlocated" not in legacy
    assert legacy["pm25_government_side"]["low"] > 0


def test_budget_counterflows_do_not_inherit_historical_consumption_bounds():
    from p8_social import uncertainty_ratio
    for item in ("pm25_respending", "pm25_government_side"):
        assert uncertainty_ratio({}, item, "low", {}, None) == 1.
        assert uncertainty_ratio({}, item, "high", {}, None) == 1.


def test_live_v9_declaration_uses_explicit_inherited_namespace():
    from pathlib import Path
    from p8_social import producer_declaration, uncertainty_ratio
    data = json.loads((Path(__file__).resolve().parent.parent / SOURCE_REL).read_text())
    declaration = data["inherited_oct15"]["social_items_in_the_social_rows"]
    assert "social_items_in_the_social_rows" not in data
    adapted = normalized(data)
    assert adapted["social_items_in_the_social_rows"] == declaration
    assert {r["item"] for r in declaration["items"]} <= set(amounts(data))
    row = next(r for r in declaration["items"] if r["item"] == "school_disruption")
    assert uncertainty_ratio(data, row["item"], "low", {}, None) == row["low_bn"] / row["central_bn"]
    assert "social_items_in_the_social_rows" not in data
    # A top-level decoy cannot replace the producer's required v9 namespace.
    data["social_items_in_the_social_rows"] = declaration
    del data["inherited_oct15"]["social_items_in_the_social_rows"]
    with pytest.raises(RuntimeError, match="BLOCKED.*social producer declaration"):
        normalized(data)
    with pytest.raises(RuntimeError, match="BLOCKED.*social producer declaration"):
        producer_declaration(data)


def test_transport_removes_observed_member_without_losing_signed_state_dollars():
    d = pd.DataFrame(dict(other=[False, True, True, True], st=[1, 1, 2, 2]))
    x = np.array([100., 50., -20., 30.])
    got = p7.transport(x, np.ones(4), np.array([0., 1., .5, .5]), d,
                       source_other=np.ones(4, bool))
    np.testing.assert_array_equal(got, [0., 150., -40., 60.])


def test_cut_gzip_has_no_clock_or_filename_and_reproduces(tmp_path):
    from p8_phase_b import write
    table = pd.DataFrame(dict(a=[1., 2.], b=["x", "y"]))
    write(table, "one.csv.gz", tmp_path)
    write(table, "two.csv.gz", tmp_path)
    assert (tmp_path / "one.csv.gz").read_bytes() == (tmp_path / "two.csv.gz").read_bytes()
    assert gzip.decompress((tmp_path / "one.csv.gz").read_bytes()) == b"a,b\n1,x\n2,y\n"
