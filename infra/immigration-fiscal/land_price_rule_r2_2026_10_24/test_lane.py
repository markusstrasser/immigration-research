"""Checks on the r2 land charge's outputs (read derived/ only; never rebuild)."""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
R1 = HERE.parent / "land_price_rule_2026_10_24" / "derived"


def load():
    return json.loads((D / "summary.json").read_text()), pd.read_csv(D / "land_by_line.csv")


def test_lines_add_to_total():
    s, by = load()
    for k in ["central", "low", "high"]:
        for i, end in enumerate(["low", "high"]):
            assert abs(by[f"charge_{k}_{end}_bn"].sum() - s[k]["case"][i]) < 1e-9
            for rn in ["theta0", "theta0489", "theta1", "bound"]:
                assert abs(by[f"{rn}_{k}_{end}_bn"].sum() - s[k][rn][i]) < 1e-9


def test_r1_reproduced():
    s, by = load()
    r1 = json.loads((R1 / "summary.json").read_text())["central"]["case_rate_bn"]
    assert all(abs(a - b) < 1e-9 for a, b in zip(s["r1_reproduced_case_rate_bn"], r1))
    for i, end in enumerate(["low", "high"]):
        assert abs(by[f"charge_r1_{end}_bn"].sum() - r1[i]) < 1e-9


def test_changes_chain_closes():
    s, _ = load()
    c = pd.read_csv(D / "changes_from_r1.csv")
    cum = c[c.cumulative]
    assert list(cum.step.str[0]) == [str(i) for i in range(len(cum))]
    for end in ["low", "high"]:
        assert abs(cum[f"delta_{end}_bn"].sum() + cum[f"case_rate_{end}_bn"].iloc[0] - cum[f"case_rate_{end}_bn"].iloc[-1]) < 1e-9
    last = cum.iloc[-1]
    assert abs(last.case_rate_low_bn - s["central"]["case"][0]) < 1e-9
    assert abs(last.case_rate_high_bn - s["central"]["case"][1]) < 1e-9


def test_range_brackets_central():
    s, _ = load()
    for rn in ["case", "theta0", "theta0489", "theta1", "bound"]:
        for i in range(2):
            assert 0 < s["low"][rn][i] <= s["central"][rn][i] <= s["high"][rn][i]


def test_rates_ordered():
    s, _ = load()
    r = s["rates"]
    assert r["theta0"]["state_local"] < r["theta0489"]["state_local"] < r["theta1"]["state_local"]
    assert r["case"]["state_local"] < r["theta0"]["state_local"]
    for rn in ["theta0", "theta0489", "theta1"]:
        for i in range(2):
            assert s["central"]["case"][i] < s["central"][rn][i]


def test_water_only_removes():
    s, by = load()
    assert (by.water_acres_removed >= 0).all()
    assert abs(by.water_acres_removed.sum() - s["checks"]["park_water_acres_removed"]) < 1e-6
    step = pd.read_csv(D / "changes_from_r1.csv").set_index("step").loc["1_water"]
    assert step.delta_low_bn <= 0 and step.delta_high_bn <= 0


def test_r2_fixes_named_in_review():
    """The four review findings: no constant 0.65 acreage-share factor, water clipped, keying not all 1."""
    s, _ = load()
    f = pd.read_csv(D / "factors.csv").set_index("factor")
    assert f.loc["englobo_lot_share_s", "central"] == 0.65  # used as an acreage share inside the residual
    assert "residual" in open(HERE / "build.py").read()
    assert s["checks"]["park_water_acres_removed"] > 0
    ch = s["changes_from_r1_case_rate_bn"]
    assert next(r for r in ch if r["step"] == "5_location")["delta_high_bn"] != 0


def test_screen_reported():
    s, _ = load()
    sc = s["screen"]
    for k in ["precision", "stability", "influence", "data_quality"]:
        assert isinstance(sc[k]["passes"], bool)
    assert s["status"].startswith("identified") == sc["passes"]


def test_factors_sourced():
    f = pd.read_csv(D / "factors.csv")
    assert not f.source.str.contains("TODO").any()
    assert f.source.str.len().gt(20).all()


def test_bound_is_theta1_low_theta0_high():
    """The adopted rate reading: the low end at θ = 1, the high end at θ = 0, hwy_sl at the highway rate."""
    s, by = load()
    rm = json.loads((HERE.parent / "public_capital_rate_2026_10_24" / "derived" / "rate_model.json").read_text())["theta_pairing"]["bound"]
    b = s["rates"]["bound"]
    assert b["state_local"] == rm["rate_state_local_by_end"] and b["federal"] == rm["rate_federal_by_end"]
    assert b["state_local_hwy"] == rm["rate_state_local_highways_by_end"]
    # the bound prices each line at its own financing level; per line, charge = case charge × line rate / case rate
    rbl, lvl = rm["rate_by_level_by_end"], rm["level_by_component"]
    assert b["by_line"] == {c: rbl[l] for c, l in lvl.items()}
    rc = s["rates"]["case"]["state_local"]
    for _, r in by.iterrows():
        for i, end in enumerate(["low", "high"]):
            want = r[f"charge_central_{end}_bn"] * b["by_line"][r.line][i] / rc
            assert abs(r[f"bound_central_{end}_bn"] - want) < 1e-9, (r.line, end)
    hw = by.set_index("line").loc["hwy_sl"]
    ratio = hw.theta1_central_low_bn / hw.charge_central_low_bn
    assert abs(ratio - b["state_local_hwy"][0] / s["rates"]["case"]["state_local"]) < 1e-9
    assert s["screen"]["rate"] == "bound"
