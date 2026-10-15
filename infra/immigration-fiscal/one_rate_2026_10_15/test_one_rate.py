"""Rate conversion, source-schema, and accounting-contract regressions."""
import json
from pathlib import Path

import numpy as np
import pytest

import build

HERE = Path(__file__).resolve().parent


def test_perpetuity_recovers_a_constant_real_rate():
    class Economy:
        cola = np.full(301, 0.024)
        new_issue_nominal = np.full(301, (1.03 * 1.024) - 1)

        def discount(self, arm):
            return 1.0 / (1.03 * 1.024) ** (np.arange(301) - 124)

    result = build.perpetuity_equivalent(Economy())
    assert result["flat_real_equivalent"] == pytest.approx(0.03, abs=1e-14)
    assert result["annuity_factor"] == pytest.approx(1 / 0.03, abs=1e-11)


def test_flat_rate_keeps_historical_accumulation():
    economy = build.T.economy_2026(rates=True, wages=True, parameters=True)
    path, flat = economy.discount("new_issue"), economy.discount(0.03)
    np.testing.assert_array_equal(path[:126], flat[:126])
    assert path[126] != flat[126]


def test_control_matches_full_precision_and_csv_sources():
    rates = json.loads((HERE / "derived/rates.json").read_text())
    source = json.loads((build.T.OUT / "summary.json").read_text())["beside"]["all_2026_inputs_separate_funds"]
    assert "groups" not in source  # serialization regression: the summary is flat
    assert rates["arms"]["unchanged"]["ratio_net"] == pytest.approx(source["ratio_net"], abs=1e-12)
    assert rates["arms"]["unchanged"]["part_a_bn"] == pytest.approx(source["part_a_bn"], abs=1e-10)
    table = build.T.pd.read_csv(build.T.OUT / "arms.csv")
    assert "net_per_tax_dollar" in table and "net_own_rate" not in table
    for group in build.T.GROUPS:
        rows = table[(table.arm == "all_2026_inputs_separate_funds") & (table.group == group)]
        assert len(rows) == 1
        arm = rates["arms"]["unchanged"]
        net = arm["ratio_net"] if group == "union" else arm["groups"][group]["net_own_rate"]
        assert net == pytest.approx(float(rows.iloc[0].net_per_tax_dollar), abs=5.1e-10)


def test_rate_direction_on_every_generation():
    arms = json.loads((HERE / "derived/rates.json").read_text())["arms"]
    for group in build.T.GROUPS:
        low, high = [arms[k]["result_row4"]["groups"][group] for k in ("flat_2", "flat_3")]
        assert low["net_own_rate"] > high["net_own_rate"]
        assert low["part_a_bn"] > high["part_a_bn"]


def test_nonpositive_ultimate_rate_stops():
    class Economy:
        cola = np.zeros(301)
        new_issue_nominal = np.zeros(301)

        def discount(self, arm):
            return np.ones(301)

    with pytest.raises(RuntimeError, match="nonpositive ultimate real rate"):
        build.perpetuity_equivalent(Economy())


def test_full_results_close_and_include_every_population_block():
    data = json.loads((HERE / "derived/results.json").read_text())
    assert len(data["results"]) == 16
    assert all(data["gates"].values())
    population = 45230062.30075857
    for row in data["results"]:
        key = tuple(row[k] for k in ("arm", "which", "end"))
        parts = [p for p in data["components"] if tuple(p[k] for k in ("arm", "which", "end")) == key]
        assert len(parts) == 15
        assert len({p["component"] for p in parts}) == 15
        assert sum(p["delta_bn"] for p in parts) == pytest.approx(row["delta_bn"], abs=1e-9)
        assert row["cost_bn"] - row["baseline_bn"] == pytest.approx(row["delta_bn"], abs=1e-9)
        for part in parts:
            assert part["delta_per_member_usd"] == pytest.approx(part["delta_bn"] * 1e9 / population, abs=1e-9)
        if row["which"] == "cash":
            assert row["oasdi_delta_bn"] == row["part_a_delta_bn"] == 0
        if row["arm"] == "A":
            assert row["capital_delta_bn"] == 0
        if row["arm"] == "B":
            assert row["oasdi_delta_bn"] == row["part_a_delta_bn"] == 0


def test_two_leg_contrast_keeps_specification_and_changes_sign_in_cash():
    rows = json.loads((HERE / "derived/results.json").read_text())["results"]
    for which, sign in (("set", -1), ("cash", 1)):
        contrast = [r for r in rows if r["arm"].startswith("both_") and r["which"] == which]
        assert len(contrast) == 2
        assert all(r["specification"] == 11 for r in contrast)
        low, high = sorted(contrast, key=lambda r: r["real_rate"])
        assert sign * (high["cost_bn"] - low["cost_bn"]) > 0


def test_opeb_beside_is_independent_of_cash_pension_switch():
    data = json.loads((HERE / "derived/inventory_sizes.json").read_text())
    for arm in data["arms"].values():
        np.testing.assert_allclose(arm["set_delta"], arm["cash_delta"], atol=1e-9, rtol=0)


def test_serialized_outputs_use_lf_and_no_process_telemetry():
    for path in (HERE / "derived").iterdir():
        assert b"\r\n" not in path.read_bytes()
    results = json.loads((HERE / "derived/results.json").read_text())
    assert "elapsed_seconds" not in results and "max_rss_kib" not in results


def test_native_child_basis_selects_one_actual_key():
    fiscal = HERE.parent
    def selected(which, line):
        name = "corrections_cash.json" if which == "cash" else "corrections.json"
        payload = json.loads((fiscal / "main_case_2026_10_15/derived" / name).read_text())
        item = next(i for i in payload["meta"]["items"] if i["id"] == "union_completion")
        values = []
        for part_name, part in item["parts"].items():
            edit = payload["edits"][item["edits"]["first"] + part["edit"]]
            if (part_name.startswith("lineage_g3plus:observed_nonreporters:spending:")
                    and edit["line"] == line and edit["key"] == line):
                values.append(part["by"]["personal"])
        assert len(values) == 1
        return sum(values)
    results = json.loads((HERE / "derived/results.json").read_text())
    share = json.loads((fiscal / "main_case_2026_10_15/derived/corrections.json").read_text())["meta"]["pension_accrual"]["part_a_share"]
    assert results["native"]["ss"] == pytest.approx(selected("set", "social_security"), abs=1e-14)
    part_a = selected("set", "medicare") - (1 - share) * selected("cash", "medicare")
    assert results["native"]["pa"] == pytest.approx(part_a, abs=1e-14)
