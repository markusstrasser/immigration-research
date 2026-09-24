"""Gates for the consumption-key lane. Run from the repository root after consumption_key.py:
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl --with pyarrow \
        --with pytest python3 -m pytest infra/immigration-fiscal/consumption_key_2026_09_24/ -q
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
DERIVED = HERE / "derived"

import consumption_key as ck  # noqa: E402
import cps_frame  # noqa: E402
import outside  # noqa: E402
import remittance  # noqa: E402


@pytest.fixture(scope="module")
def frame():
    return cps_frame.frame()


def test_current_key_reproduces_stored_share(frame):
    g = cps_frame.reproduce(frame)
    assert g["ok"], g
    assert abs(g["reproduced"] - 0.0810406073372985) < 1e-12


def test_adopted_state_rebuilds_the_adopted_targets():
    s = ck.adopted_state()
    assert abs(s["phi"] - 0.949694359) < 1e-9
    exc = s["lines"]["excise_selective_sales"]
    stored = pd.read_csv(ck.CBO_TRANSLATION).query(
        "spec == 'excise_taxes|2022' and allocation == 'personal'").reweighted_share.iloc[0]
    rebuilt = s["phi"] * (0.0810406073372985 * (exc["national"] - ck.FEDERAL_EXCISE_BN) + stored * ck.FEDERAL_EXCISE_BN)
    assert abs(rebuilt - exc["adopted"]) < 1e-6


def test_payloads_cover_every_scenario_and_allocation():
    payload = json.loads((DERIVED / "payloads.json").read_text())
    model = json.loads(ck.MODEL.read_text())
    scenarios = set(model["receipts"]["scenarios"])
    for name, spec in payload["specs"].items():
        receipt = [e for e in spec["edits"] if e["side"] == "receipt"]
        for lid in ck.LINES:
            cells = [e for e in receipt if e["line"] == lid]
            assert {e["scenario"] for e in cells} == scenarios, (name, lid)
            values = {(round(e["by"]["personal"], 12), round(e["by"]["shared"], 12)) for e in cells}
            assert len(values) == 1, (name, lid, values)
            (p, sh), = values
            assert p == sh
        rpp = [e for e in receipt if e["line"] == ck.RPP]
        assert [e["scenario"] for e in rpp] == [ck.RPP_SCENARIO], name
        spending = {e["line"] for e in spec["edits"] if e["side"] == "spending"}
        assert spending == set(ck.SPENDING_RESOURCE_LINES), name
    raw = payload["specs"]["raw"]["edits"]
    assert max(abs(v) for e in raw for v in e["by"].values()) < 1e-9


def test_receipt_edits_sum_to_the_reported_change():
    payload = json.loads((DERIVED / "payloads.json").read_text())
    table = pd.read_csv(DERIVED / "key_specs.csv").set_index("spec")
    for name, spec in payload["specs"].items():
        ref = [e for e in spec["edits"] if e["side"] == "receipt" and e["line"] in ck.LINES
               and e["scenario"] == "cbo_collective"]
        assert abs(sum(e["by"]["personal"] for e in ref) - table.loc[name, "receipts_change_bn"]) < 1e-9


def test_engine_change_equals_linear_receipt_change():
    engine = json.loads((DERIVED / "engine_summary.json").read_text())
    table = pd.read_csv(DERIVED / "key_specs.csv").set_index("spec")
    assert abs(engine["adopted_band"][0] - 200.875) < 5e-4 and abs(engine["adopted_band"][1] - 246.318) < 5e-4
    for name, s in engine["specs"].items():
        for c in s["change"]:
            assert abs(c - table.loc[name, "linear_cost_change_bn"]) < 1e-6, name


def test_corridor_calibration_is_exact(frame):
    rates = remittance.sender_rates()
    un = remittance.units(frame)
    per = remittance.per_theta(frame, un, rates, 0.5)
    flow = remittance.BANXICO_US - remittance.H2_ALLOWANCE["central"]
    theta = remittance.solve_theta(frame, un, per, flow, un["any_target"])
    sent = remittance.person_sum(frame, np.where(un["any_target"], per, 0.0))[0] * theta[0]
    assert abs(sent / 1e9 - flow) < 1e-9


def test_sender_rates_match_the_pooled_fdic_read():
    t = pd.read_csv(DERIVED / "sender_rates_pooled.csv").set_index(["group", "scope"])
    assert t.loc[("mexico_born", "all_households"), "rate_pct"] == pytest.approx(37.27, abs=0.005)
    assert t.loc[("us_born_mex_parent_G2", "no_foreign_born_member"), "rate_pct"] == pytest.approx(6.52, abs=0.005)
    assert t.loc[("us_born_mex_origin_G3plus", "all_households"), "rate_pct"] == pytest.approx(2.00, abs=0.005)


def test_itep_us_average_rows():
    t = outside.itep_table()
    assert list(t.sales_excise.round(3)) == [0.07, 0.057, 0.048, 0.039, 0.03, 0.019, 0.01]
    assert list(t.average_income) == [13600, 34700, 62200, 108100, 186800, 428800, 1889900]
