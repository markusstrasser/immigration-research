"""Paired budget counterflows and live source rows must close independently."""
import gzip
import json

import numpy as np
import pandas as pd

import p7_frames as p7
from p8_social import amounts, normalized, SOURCE_REL


def test_round3_rows_close_and_keep_paired_pm_flows_separate():
    from pathlib import Path
    data = json.loads((Path(__file__).resolve().parent.parent / SOURCE_REL).read_text())
    rows = amounts(data)
    env = data["v8_social_environment"]
    for end in ("low", "high"):
        assert abs(sum(v[end] for v in rows.values()) - env["current_social_by_end_bn"][end]) < 1e-9
        assert rows["pm25_respending"][end] < 0 < rows["pm25_government_side"][end]
        neither = amounts(data, "neither_budget_side")
        assert abs(neither["pm25_respending"][end]) < 1e-12
        assert abs(neither["pm25_government_side"][end]) < 1e-12
    adapted = normalized(data)
    assert len(adapted["lineage_social_rows"]["rows"]) == len(rows)
    matched = amounts(data, "matched_justice_footing")
    assert matched["variant_fiscal_justice"]["high"] == 0.
    legacy = amounts(data, "government_legacy_response")
    assert "variant_unlocated" not in legacy
    assert legacy["pm25_government_side"]["low"] > 0


def test_budget_counterflows_do_not_inherit_historical_consumption_bounds():
    from p8_social import uncertainty_ratio
    for item in ("pm25_respending", "pm25_government_side"):
        assert uncertainty_ratio({}, item, "low", {}, None) == 1.
        assert uncertainty_ratio({}, item, "high", {}, None) == 1.


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
