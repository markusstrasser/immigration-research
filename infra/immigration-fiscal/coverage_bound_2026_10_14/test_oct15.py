"""Regressions for explicit base receipts and population-specific new drivers."""
import copy
import csv
import json
from pathlib import Path

import numpy as np
import pytest

import coverage_oct15 as V
import coverage_final_routing as R
from coverage_final_routing import observed_snapshot
from export_pricing import profile_call
from national_keys import full_key
from test_national_keys import snapshot, piece


def test_new_members_do_not_enter_baseline_driver_restriction():
    s = snapshot()
    s["original_gens"] = copy.deepcopy(s["gens"])
    s["gens"]["G1"][2] = True
    v, _, _ = full_key(s, piece("oasdi", "taxes", [1., 3.]), "low")
    np.testing.assert_array_equal(v, [1., 3., 5., 7.])


def test_completion_parent_has_its_own_records_and_national_extension():
    s = snapshot()
    s["reporter"] = np.array([False, False, True, False])
    src = dict(kind="line", side="receipt", parent_line="oasdi")
    s["lines"]["meta"]["union_completion"] = dict(carriers={"new_payroll": src})
    p = dict(g="G1", id="new_payroll", cat="taxes", bn=1., x=np.array([0., 0., 5.]),
             completion_source=src, observed_population="reporter")
    v, _, _ = full_key(s, p, "low")
    np.testing.assert_array_equal(v, [1., 3., 5., 7.])
    p["completion_source"] = dict(src, parent_line="hi")
    with pytest.raises(SystemExit, match="changed completion source"):
        full_key(s, p, "low")


def test_cash_social_security_uses_benefit_driver():
    s = snapshot()
    s["lines"]["meta"]["basis"] = "cash"
    v, _, _ = full_key(s, piece("social_security", "transfers", [4., 0.]), "low")
    np.testing.assert_array_equal(v, [4., 0., 2., 1.])


def test_reporter_job_mass_is_principal_national_receipt_not_member_mass():
    s = snapshot()
    s["reporter"] = np.array([False, False, True, False])
    src = dict(kind="line", side="receipt", parent_line="corporate_capital")
    s["lines"]["meta"]["union_completion"] = dict(carriers={"job": src})
    s["completion_jobs"] = {"corporate": np.array([0., 0., 2., 0.])}
    s["completion_national_mass"] = {"corporate": 137.}
    p = dict(g="G1", id="job", cat="taxes", bn=1., x=np.array([0., 0., 2.]),
             completion_source=src, observed_population="reporter")
    _, _, mass = full_key(s, p, "low")
    assert mass == 137.
    assert mass != s["completion_jobs"]["corporate"] @ s["w_id"]
    s["completion_national_mass"]["corporate"] = float("nan")
    with pytest.raises(SystemExit, match="principal national driver mass"):
        full_key(s, p, "low")


def test_native_child_driver_requires_principal_own_age_cell():
    s = snapshot()
    s["d"]["PH_SEQ"] = [1, 2, 3, 4]
    s["d"]["PPPOS"] = [1, 1, 1, 1]
    s["nonreporter"] = np.array([False, False, True, False])
    s["lines"]["meta"]["child_pricing"] = {"records": [{"PH_SEQ": 3, "PPPOS": 1, "ends": {
        "low": {"rows": [dict(side="receipt", id="oasdi", key="payroll", cost_bn=2.)]}}}]}
    p = dict(g="G1", id="native_child_receipt_oasdi", cat="taxes", bn=60., x=np.array([0., 0., 2.]),
             full_driver=np.array([0., 0., 2., 0.]),
             native_child_source=dict(kind="rows", parent="oasdi", side="receipt", key="payroll"))
    v, _, _ = full_key(s, p, "low")
    np.testing.assert_array_equal(v, [0., 0., 2., 0.])
    p["full_driver"][2] = 3.
    with pytest.raises(SystemExit, match="differs from principal own-age prices"):
        full_key(s, p, "low")


def test_missing_frozen_base_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(V, "BASE", tmp_path)
    with pytest.raises(SystemExit, match="missing frozen oct15 BASE"):
        V.validate_frozen()


def test_native_education_categories_require_principal_amounts_and_closure():
    s = snapshot()
    s["d"]["PH_SEQ"], s["d"]["PPPOS"] = [1, 2, 3, 4], [1, 1, 1, 1]
    s["nonreporter"] = np.array([False, False, True, False])
    row = dict(side="spending", id="education_services", key="school_part", cost_bn=2.,
               category_cost_bn={"schools": 1.5, "education_other": .5})
    s["lines"]["meta"]["child_pricing"] = {"records": [{"PH_SEQ": 3, "PPPOS": 1,
        "ends": {"low": {"rows": [row]}}}]}
    p = dict(g="G1", id="native_school", cat="schools", bn=45., x=np.array([0., 0., 1.5]),
             full_driver=np.array([0., 0., 1.5, 0.]), native_child_source=dict(kind="rows",
             parent="education_services", side="spending", key="school_part", category="schools"))
    np.testing.assert_array_equal(full_key(s, p, "low")[0], [0., 0., 1.5, 0.])
    row["category_cost_bn"]["education_other"] = .6
    with pytest.raises(SystemExit, match="education category cost closure"):
        full_key(s, p, "low")


def test_final_state_piece_retains_latent_mass_source_and_population_cost():
    s = snapshot()
    s["gens"] = {"G3plus": s["gens"]["G1"]}
    s["lines"]["generations"] = {"G3plus": s["lines"]["generations"]["G1"]}
    s["f_rec"] = np.array([2., 2., 1., 1.])
    source = dict(population="latent", source_cell="spending|economic_affairs_services|economic",
                  edit={"side": "spending", "line": "state_price_public_order_safety", "key": "population"},
                  key="economic", category="other_shared", category_share=1., charge_source="principal state shares", rule="joint normalization",
                  indexes_source="principal state indexes")
    part = {k: v for k, v in source.items() if k not in ("population", "key", "category", "category_share")}
    part["cost_by_population"] = {"identified": 1., "latent": 2., "native": 0.}
    s["lines"]["generations"]["G3plus"]["low"]["added_state_prices"] = [part]
    p = dict(g="G3plus", id="added_state_latent", cat="other_shared", bn=2., x=np.array([.5, 1., 0.]),
             full_driver=np.array([.5, 1., 0., 0.]), state_price_source=source)
    np.testing.assert_array_equal(full_key(s, p, "low")[0], [.5, 1., 0., 0.])
    part["cost_by_population"]["latent"] = 3.
    with pytest.raises(SystemExit, match="population cost differs"):
        full_key(s, p, "low")


@pytest.mark.parametrize("category,share,driver", [
    ("justice_per_head", .4, [.5, .5, 0., 0.]), ("justice_use", .6, [0., .5, 0., 0.])])
def test_final_state_justice_uses_principal_category_not_nonexistent_use_key(category, share, driver):
    s = snapshot()
    s["gens"] = {"G3plus": s["gens"]["G1"]}
    s["lines"]["generations"] = {"G3plus": s["lines"]["generations"]["G1"]}
    s["f_rec"] = np.array([2., 2., 1., 1.])
    s["per_head_factor"] = np.array([1., 1., 2.])
    s["use_parts"] = {"per_head": [0., 0., 10.], "custody": [0., 0., 10.],
                      "arrest_like_custody": [0., 0., 15.], "ice_interior": [0., 0., 5.]}
    source = dict(population="latent", source_cell="spending|public_order_safety|population",
                  edit={"side": "spending", "line": "state_price_public_order_safety", "key": "population"},
                  key="population", category=category, category_share=share, charge_source="principal state shares",
                  rule="joint normalization", indexes_source="principal indexes")
    part = {k: v for k, v in source.items() if k not in ("population", "key", "category", "category_share")}
    part["cost_by_population"] = {"identified": 1., "latent": 2., "native": 0.}
    s["lines"]["generations"]["G3plus"]["low"]["added_state_prices"] = [part]
    p = dict(g="G3plus", id="added_state_latent", cat=category, bn=2.*share, x=np.asarray(driver)[:3],
             full_driver=np.asarray(driver), state_price_source=source)
    np.testing.assert_array_equal(full_key(s, p, "low")[0], driver)
    source["category_share"] += .1
    with pytest.raises(SystemExit, match="source category share mismatch"):
        full_key(s, p, "low")


def test_cpu_profile_cannot_mask_failed_gate(tmp_path):
    def blocked():
        raise SystemExit(7)
    with pytest.raises(SystemExit) as stop:
        profile_call(blocked, tmp_path / "cpu.prof")
    assert stop.value.code == 7
    assert (tmp_path / "cpu.prof").exists()


def test_same_total_wrong_generation_csv_blocks():
    rows = [dict(convention="a", generation=g, band_end=end, allocation="personal", cost_bn=str(2+i), population="100")
            for i, end in enumerate(V.ENDS) for g in V.GENS]
    full = {"case": "oct15", "set": "set", "conventions": {"a": {
        g: {"cost_bn": [2., 3.], "population": 100.} for g in V.GENS}}}
    summary = {"v8": {"band_bn": [6., 9.], "end_specifications": {"set": [[16, 11], [16, 11]]},
                       "population": {"without_coverage": 300.}}}
    assert V.validate_generations(rows, full, summary, "set") == [6., 9.]
    rows[0]["cost_bn"], rows[1]["cost_bn"] = "1", "3"
    with pytest.raises(SystemExit, match="generation CSV/full precision cost mismatch"):
        V.validate_generations(rows, full, summary, "set")


def test_base_revision_roundoff_ceiling_preserves_shapes_and_declarations():
    assert V.same_numeric({"cost": [1.0], "key": "school_part"}, {"cost": [1.0+1e-15], "key": "school_part"})
    assert not V.same_numeric({"cost": [1.0]}, {"cost": [1.0+1e-10]})
    assert not V.same_numeric([1.0], [1.0, 0.0])
    assert not V.same_numeric({"key": "school_part"}, {"key": "P_part"})


def test_final_observed_kernel_removes_only_declared_coverage_after_gates(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "BASE", tmp_path)
    (tmp_path / "lines.json").write_text(json.dumps({"meta": {"coverage_added_cost_bn": {e: 4. for e in V.ENDS}}}))
    declared = {g: float(i+1) for i, g in enumerate(V.GENS)}
    s = {"lines": {"meta": {"basis": "set", "coverage_added_state_reallocation_bn": {e: 0. for e in V.ENDS},
        "coverage_added_source_cost_bn": {e: 4. for e in V.ENDS}, "coverage_added_cost_bn": {e: 4. for e in V.ENDS},
        "coverage": {"by_end": {e: {"by_generation": declared, "total_bn": 6.}
            for e in V.ENDS}}},
        "generations": {g: {e: {"cost_bn": 10.+declared[g], "sum_bn": 10.+declared[g],
            "post_engine": {"coverage": declared[g], "mixed_unit_removal": -.5}}
            for e in V.ENDS} for g in V.GENS},
        "union": {e: {"cost_bn": 36., "sum_bn": 36., "post_engine": {"coverage": 6.}}
            for e in V.ENDS}}, "residual": {e: {g: 2.+declared[g] for g in V.GENS} for e in V.ENDS}}
    observed_snapshot(s)
    for end in V.ENDS:
        assert s["lines"]["union"][end]["cost_bn"] == 30.
        assert s["lines"]["meta"]["coverage"]["by_end"][end]["total_bn"] == 6.
        for generation in V.GENS:
            assert s["residual"][end][generation] == 2.
            assert s["lines"]["generations"][generation][end]["cost_bn"] == 10.
            assert s["lines"]["generations"][generation][end]["post_engine"]["mixed_unit_removal"] == -.5
    s["lines"]["meta"]["coverage"]["stub"] = True
    with pytest.raises(SystemExit, match="real coverage metadata"):
        observed_snapshot(s)


def test_final_calibration_cannot_erase_nonzero_added_state_amount(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "BASE", tmp_path)
    (tmp_path / "lines.json").write_text(json.dumps({"meta": {"coverage_added_cost_bn": {e: 4. for e in V.ENDS}}}))
    state = {"cost_by_population": {"identified": -1., "latent": .8, "native": .2}}
    s = {"lines": {"meta": {"basis": "set", "coverage": {"by_end": {}},
        "coverage_added_source_cost_bn": {e: 4. for e in V.ENDS},
        "coverage_added_state_reallocation_bn": {e: 1. for e in V.ENDS},
        "coverage_added_cost_bn": {e: 4. for e in V.ENDS}},
        "generations": {g: {e: {"added_state_prices": [state] if g == "G3plus" else []}
            for e in V.ENDS} for g in V.GENS}}}
    with pytest.raises(SystemExit, match="erases declared state allocation"):
        observed_snapshot(s)


def test_signed_age_bands_close_and_added_stays_separate():
    data = dict(age=np.array([17, 18, 81]), generation=np.array([0, 1, 2]),
                weights=np.array([[3.], [4.], [5.]]), added_weights=np.array([[0.], [0.], [2.]]))
    got = V.missing_age_bands(data, np.array([-.1, .2, .3]), np.array([0., 0., -.1]))
    assert got["G1"]["15-19"] == pytest.approx(-.3)
    assert got["G2"]["15-19"] == pytest.approx(.8)
    assert got["G3plus"]["80+"] == pytest.approx(1.5)
    assert got["added"]["80+"] == pytest.approx(-.2)


def test_decomposition_conserves_cost_and_excludes_imputed_capital_from_cash():
    data = {"weights": np.ones((2, 1)), "added_weights": np.zeros((2, 1)),
            "base_piece_prices": np.array([[5., 0.], [-5., 0.], [8., 0.], [1., 0.]]),
            "other_piece_prices": np.array([[.5, 0.]])}
    pieces = [dict(end="low", generation="G1", line=str(i), source_line=str(i), source_side="spending",
                   category="test", level="federal" if i == 0 else "unclassified", economic_class=kind)
              for i, kind in enumerate(("capital_return", "production", "fiscal_line", "unclassified_post_engine"))]
    pieces[1]["source_production"] = dict(cost_bn=-5., private_wtp_bn=2., induced_receipts_bn=3., fiscal_weight=1.)
    audit = {"denominator_pieces": pieces, "other_pieces": [dict(end="low", generation="G1", line="calibration", population="identified")]}
    got = V.decompose(data, np.array([1., 0.]), np.zeros(2), audit, "low", 9.5, "cash", "generation_ratio")
    assert got["capital_by_level_bn"]["federal"] == 5.
    assert got["production"]["P_bn"] == 2.
    assert got["production"]["F_bn"] == 3.
    assert got["unclassified_bn"] == 1.5
    assert got["classified_cash_fiscal_bn"] == 5.
    assert got["total_cost_bn"] == 9.5
    with pytest.raises(SystemExit, match="economic decomposition closure"):
        V.decompose(data, np.array([1., 0.]), np.zeros(2), audit, "low", 10., "cash", "generation_ratio")


def test_published_oct15_has_own_set_cash_prices_and_all_constructions():
    file = Path(__file__).resolve().parent / "derived/coverage_bound_oct15.json"
    if not file.exists():
        pytest.skip("coverage file withheld pending actual upstream base gates")
    output = json.loads(file.read_text())
    assert output["key"] == "oct15"
    assert set(output["base_payload_sha256_by_set"]) == {"set", "cash"}
    for basis in ("set", "cash"):
        q = output["sets"][basis]
        assert set(q["scenarios"]) == set(V.DEFINITIONS)
        assert q["scenarios"]["central"]["implied_net_missing_people"]["added"] == 0
        for scenario in q["scenarios"].values():
            assert set(scenario["adults_by_generation"]) == set(V.GENS)
            for end in V.ENDS:
                e = scenario["ends"][end]
                assert abs(sum(e["by_generation"].values())-e["total_bn"]) < 1e-9
        for e in q["ends"].values():
            for generation in V.GENS:
                assert abs(e["adult_cost_by_generation_bn"][generation]
                           + e["minor_cost_by_generation_bn"][generation]
                           - e["by_generation"][generation]) < 1e-9
            d = e["decomposition"]
            assert abs(sum(d["capital_by_level_bn"].values()) + d["classified_fiscal_line_bn"]
                       + d["unclassified_bn"] - d["production"]["P_bn"] - d["production"]["F_bn"]
                       - e["total_bn"]) < 1e-9
    assert output["sets"]["set"]["ends"]["low"]["coverage_bn"] != output["sets"]["cash"]["ends"]["low"]["coverage_bn"]
