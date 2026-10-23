"""Gates for the school-land lane. Run after build.py:

    uv run --no-project python3 -m pytest infra/immigration-fiscal/school_land_2026_10_24/ -q -s
"""
import json
import math
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
S = json.loads((OUT / "summary.json").read_text())
CASE = json.loads((HERE.parent / "main_case_2026_10_16/derived/summary.json").read_text())["v9"]
CAP = json.loads((HERE.parent / "school_capital_return_2026_09_26/derived/summary.json").read_text())


def test_match_rate_printed_and_above_threshold():
    """Floors: 70% of schools and 80% of pupils nationally, 75% of schools in CA and TX.

    Why these: below them the imputed share of acreage would pass a quarter (gated next), and the only
    measured check of the imputation (California, against parcel data) found it 26% low in sum.
    """
    m = S["matching"]
    print(f"\nmatch rate: schools {m['match_rate']:.3f}, pupils {m['pupil_match_rate']:.3f}; "
          f"CA {m['ca']['match_rate']:.3f}/{m['ca']['pupil_match_rate']:.3f}; TX {m['tx']['match_rate']:.3f}/{m['tx']['pupil_match_rate']:.3f}")
    assert m["match_rate"] >= 0.70 and m["pupil_match_rate"] >= 0.80
    assert m["ca"]["match_rate"] >= 0.75 and m["tx"]["match_rate"] >= 0.75
    a = S["acreage"]
    share = a["imputed"] / a["total"]
    print(f"imputed share of acreage {share:.3f}")
    assert share <= 0.25


def test_state_match_table_complete():
    st = pd.read_csv(OUT / "by_state.csv")
    assert len(st) == 51 and st.match_rate.between(0, 1).all()
    assert abs(st.schools.sum() - S["universe"]["non_virtual"]) == 0


def test_acreage_benchmark_error():
    v = S["validation"]
    c = v["campus_level"]
    print(f"\nCSCD campus level: n {c['n']}, median ratio {c['median_ratio']:.3f}, mean |log error| "
          f"{c['mean_abs_log_error']:.3f}, within 25% {c['share_within_25pct']:.3f}, sum ratio {c['sum_ratio']:.3f}; "
          f"CA total {v['lane_ca_total_over_cscd']:.3f}; imputed sum ratio {v['imputed']['sum_ratio']:.3f} (n {v['imputed']['n']})")
    assert c["n"] >= 5000
    assert 0.9 <= c["median_ratio"] <= 1.1
    assert c["mean_abs_log_error"] <= 0.25
    assert 0.8 <= v["lane_ca_total_over_cscd"] <= 1.2


def test_land_to_structures_ratio_finite_and_ordered():
    A, B, C = (S["arms"][k] for k in "ABC")
    for k in "ABCD":
        r = S["arms"][k]["ratio_to_k12_structures"]
        assert math.isfinite(r) and r > 0
    print(f"\nland / K-12 structures: A {A['ratio_to_k12_structures']:.3f}, B {B['ratio_to_k12_structures']:.3f}, "
          f"C {C['ratio_to_k12_structures']:.3f}")
    assert A["national_bn"] > B["national_bn"] > C["national_bn"] > 0


def test_inputs_match_the_case_and_capital_lane():
    i = S["inputs"]
    assert i["case_rate"] == CASE["one_rate"]["flat_real_equivalent"]
    assert abs(i["case_rate"] - 0.020810698764) < 1e-9
    assert i["headline_band_bn"] == CASE["band_bn"]
    assert i["pupil_share_s"] == CAP["pupil_share_s"] and abs(i["pupil_share_s"] - 0.17481) < 1e-5
    assert abs(i["k12_structures_bn"] - 2663.9) < 0.1 and abs(i["k12_capital_bn"] - 2723.9) < 0.1


def test_charge_arithmetic():
    s, rate = S["inputs"]["pupil_share_s"], S["inputs"]["case_rate"]
    for k, a in S["arms"].items():
        V, r = a["national_bn"], a["where_enrolled_ratio"]
        assert a["group_value_bn"]["pupil_share"] == pytest.approx(s * V)
        assert a["group_value_bn"]["where_enrolled"] == pytest.approx(s * V * r)
        assert a["annual_charge_bn"]["case_flat_real"]["where_enrolled"] == pytest.approx(s * V * r * rate)
        assert a["annual_charge_bn"]["omb_2003_3pct"]["pupil_share"] == pytest.approx(s * V * 0.03)
        assert a["annual_charge_bn"]["omb_2003_7pct"]["where_enrolled"] == pytest.approx(s * V * r * 0.07)


def test_school_file_adds_to_national():
    d = pd.read_csv(OUT / "schools.csv.gz", usecols=["virtual", "value_A", "value_B", "value_C", "acres_final"])
    for k in "ABC":
        assert d[f"value_{k}"].sum() / 1e9 == pytest.approx(S["arms"][k]["national_bn"], rel=1e-5)
    assert d.acres_final[~d.virtual].sum() == pytest.approx(S["acreage"]["total"], rel=1e-5)
    assert (d.value_B[d.virtual] == 0).all()


def test_group_pupils_match_the_where_enrolled_lane():
    g = S["group"]
    assert abs(g["lane_group_pupils"] / g["admin_group_pupils_weighting"] - 1) < 0.02


def test_outputs_are_lf():
    for p in OUT.glob("*"):
        if p.suffix in {".csv", ".json"}:
            assert b"\r\n" not in p.read_bytes(), p.name
