"""Gates for the school-level price lane."""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"


def test_summary_exists_and_gates():
    s = json.loads((OUT / "summary.json").read_text())
    assert 0.9 < s["national_k_hispanic"] < 1.2
    assert 0.8 < s["national_k_white"] < 1.1
    assert 0.9 < s["hispanic_weighted_state_k"] < 1.2
    assert s["checks"]["schools_with_hispanic_gt_total"] == 0
    assert s["checks"]["schools_with_white_gt_total"] == 0
    assert s["checks"]["schools_with_negative_pp"] == 0
    assert 0.2 < s["checks"]["hispanic_share_of_members"] < 0.35


def test_state_table():
    d = pd.read_csv(OUT / "state_k.csv")
    assert len(d) >= 50
    assert d["k_hispanic"].between(0.5, 1.5).all()
    assert d["members"].sum() > 40_000_000


def test_district_table():
    d = pd.read_csv(OUT / "district_k.csv")
    assert len(d) > 1000
    assert d["k_within"].between(0.5, 1.5).all()
    assert d["hispanic"].sum() > 5_000_000


def test_state_elasticity():
    d = pd.read_csv(OUT / "state_elasticity.csv")
    assert len(d) >= 80
    pw = d[d.weighting.eq("pupil_weighted")]
    assert pw["beta"].between(0.4, 1.3).all()
    for state in ("CA", "TX", "AZ"):
        row = pw[pw.state.eq(state)].iloc[0]
        assert 0.8 < row.beta < 1.0
    s = json.loads((OUT / "state_elasticity_summary.json").read_text())
    assert 0.8 < s["national_pupil_weighted_beta"] < 1.0
    assert 0.8 < s["hispanic_weighted_state_beta"] < 1.0


def test_merge_totals():
    d = pd.read_csv(HERE / "_cache" / "school_merge.csv", dtype={"NCESSCH": str})
    assert len(d) > 80_000
    assert d["member"].sum() > 40_000_000
    assert d["hispanic"].sum() > 10_000_000
    assert (d["hispanic"] <= d["total"]).all()
