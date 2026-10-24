"""Checks on the lane's derived outputs (run financing_shares.py and rate_model.py first).

    uv run --no-project python3 -m pytest infra/immigration-fiscal/public_capital_rate_2026_10_24/ -q
"""
import csv
import json
from pathlib import Path

DER = Path(__file__).resolve().parent / "derived"
RM = json.loads((DER / "rate_model.json").read_text())
FIN = json.loads((DER / "financing_shares.json").read_text())
BOUND = RM["theta_pairing"]["bound"]
LINES = list(csv.DictReader(open(DER / "line_deltas.csv")))
RC = RM["r_c"]


def d_of(f, s, d_tax, d_bond, d_fed):
    return f * d_fed + (1 - f) * ((1 - s) * d_tax + s * d_bond)


def test_financing_checks_pass_and_shares_add_to_census_debt():
    assert all(c["pass"] for c in FIN["checks"])
    s24 = FIN["stocks_bn"]["2024"]
    measured = sum(FIN["debt_to_stock_fy2024"][n] * s24[n] for n in FIN["debt_to_stock_fy2024"])
    resid = FIN["levels"]["state_local"]["debt_share_of_nonfederal_stock"] * FIN["residual_base_bn"]
    assert abs(measured + resid - FIN["census_debt_fy2024_bn"]) < 1e-6


def test_contract_covers_every_line_and_level():
    keys = {r["line"] for r in LINES}
    assert set(BOUND["level_by_component"]) == keys
    assert set(BOUND["level_by_component"].values()) <= set(BOUND["rate_by_level_by_end"])
    assert {"state_local", "state_local_hwy", "federal"} <= set(BOUND["rate_by_level_by_end"])
    for r in LINES:  # the CSV's level column is the contract's
        assert r["level"] == BOUND["level_by_component"][r["line"]]
    for lv, (lo, hi) in BOUND["rate_by_level_by_end"].items():
        assert RC < hi < lo <= BOUND["rate_by_level_by_end"]["federal"][0] + 1e-12, lv


def test_existing_keys_keep_their_meaning():
    assert BOUND["rate_state_local_by_end"] == BOUND["rate_by_level_by_end"]["state_local"]
    assert BOUND["rate_state_local_highways_by_end"] == BOUND["rate_by_level_by_end"]["state_local_hwy"]
    assert BOUND["rate_federal_by_end"] == BOUND["rate_by_level_by_end"]["federal"]
    assert BOUND["theta_by_end"] == [1.0, 0.0]


def test_rates_follow_from_the_financing_shares():
    d_tax, d_bond, d_fed = RM["d_tax"][1], 0.33, RM["d_federal"][1]
    r_i = {"low": RM["r_i_candidates"]["grr_all_capital_pretax_2024"], "high": RM["r_i_candidates"]["baa_real_2024"]}
    for lv, v in FIN["levels"].items():
        d = d_of(v["federal_share"], v["debt_share_of_nonfederal_stock"], d_tax, d_bond, d_fed)
        for i, end in enumerate(("low", "high")):
            assert abs(BOUND["rate_by_level_by_end"][lv][i] - (RC + d * (r_i[end] - RC))) < 1e-12, lv


def test_bound_band_from_the_contract():
    # line returns at r_c (rounded to 4 decimals in the CSV) priced at each level's bound rate add to the band's rate leg
    ret = {}
    for r in LINES:
        if r["scenario"].startswith("central"):
            ret[(r["end"], r["line"])] = float(r["return_at_2081_bn"])
    for i, end in enumerate(("low", "high")):
        rd = sum(v * (BOUND["rate_by_level_by_end"][BOUND["level_by_component"][k]][i] / RC - 1)
                 for (e, k), v in ret.items() if e == end)
        assert abs(rd - BOUND["set"]["rate_delta_bn"][i]) < 0.01


def test_premises_reproduce_the_first_pass_and_the_revision():
    p = BOUND["financing_premises"]
    assert [round(x, 3) for x in p["first_pass"]["set"]] == [380.949, 440.406]
    assert [round(x, 3) for x in p["first_pass"]["cash"]] == [297.316, 356.773]
    assert p["c_revised"]["set"] == BOUND["set"]["band_bn"]
    # cash moves by the same dollars as the set
    for k, v in p.items():
        assert abs((v["set"][0] - v["cash"][0]) - (380.949 - 297.316)) < 1e-3, k
