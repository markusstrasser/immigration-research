"""Principal-key, scope, coverage, raw-record and regression gates."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
FISCAL = HERE.parent


def load_module(name):
    spec = importlib.util.spec_from_file_location("where_used_test_" + name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(name):
    return json.loads((OUT / name).read_text())


def table(name):
    return pd.read_csv(OUT / name, dtype={"uid": str, "fips": str, "state": str})


def test_primary_college_key_and_function_bridge_match_case():
    college = read("colleges.json")
    fees = json.loads((FISCAL / "user_fee_allocation_2026_10_07/derived/fee_lines.json").read_text())
    item = json.loads((FISCAL / "spending_keys_r5_2026_10_15/derived/item15.json").read_text())
    assert college["case_er_share_acs"] == pytest.approx(fees["higher_ed"]["s_U_acs"], abs=1e-12)
    assert college["case_response_reproduced"] == pytest.approx(item["central_response"], abs=1e-12)
    assert college["operating"]["already_where_enrolled"]
    c = table("college_factors.csv")
    er = c[c.scheme.eq("case_fall") & c.graduate_weight.eq(2) & c.concept.eq("er")].iloc[0]
    assert er.factor_vs_case_er_key == pytest.approx(1, abs=1e-12)
    assert er.relative_to_simple_fte < 1  # real composition difference, already included


def test_one_primary_finance_record_hand_reconstruction():
    build = load_module("build")
    raw = build.zipped_csv(build.source(build.STAGE / "F2223_F1A.zip"), "f2223_f1a.csv", {"UNITID", "F1C011", "F1C051", "F1C061", "F1C071"})
    row = raw[raw.UNITID.eq("100654")].iloc[0]
    expected = sum(float(row[col]) for col in ["F1C011", "F1C051", "F1C061", "F1C071"])
    u = table("college_units.csv")
    actual = u[u.UNITID.eq(100654) & u.scheme.eq("case_fall")].iloc[0]
    assert actual.er == pytest.approx(expected, abs=0.01)
    assert 0 <= actual.use_share <= 1


def test_missing_applicable_finance_is_blocked_but_not_applicable_zero_is_explicit():
    build = load_module("build")
    d = pd.DataFrame({"value": ["."], "Xvalue": ["B"]})
    with pytest.raises(ValueError, match="missing applicable"):
        build.numeric(d, ["value"], flagged=True)
    d["Xvalue"] = "A"
    assert build.numeric(d, ["value"], flagged=True).value.iloc[0] == 0


def test_raked_state_degree_weights_close_including_zero_cells():
    rake = table("college_raking.csv")
    assert len(rake) == 102
    assert np.allclose(rake.case_group_fte, rake.raked_group_fte, atol=1e-6, rtol=0)
    vt = rake[rake.FIPS.eq(50)]
    assert len(vt) == 2 and vt.case_group_fte.eq(0).all()
    assert np.isfinite(rake.raked_group_fte).all()
    units = table("college_units.csv")
    for _, d in units.groupby("scheme"):
        assert d.den.gt(0).all()
        assert (d.group / d.group.sum()).sum() == pytest.approx(1)


def test_finance_coverage_and_unknown_assets_are_not_hidden_by_fte_coverage():
    coverage = table("college_finance_coverage.csv").set_index("concept")
    college = read("colleges.json")
    assert college["coverage"]["gasb_group_fte_share"] > .99
    assert coverage.loc["depreciable_gross", "covered_share"] < .90
    assert coverage.loc["depreciable_gross", "unallocated_bn"] > 90
    for concept in ["depreciable_gross", "assets_responsive_proxy", "net_depreciable"]:
        r = coverage.loc[concept]
        assert r.factor_low_all_unallocated_to_nonmembers < 1 < r.factor_high_all_unallocated_to_members
    bad = table("college_factors.csv")
    assert bad[bad.concept.eq("net_plant")].status.eq("invalid_negative_asset_values").all()
    assert read("case_prices.json")["identification"]["college_capital"].startswith("proxy;")


def test_primary_park_scope_coverage_and_accounts_close():
    parks = read("parks.json")
    c = parks["coverage"]
    assert sum(parks["national_E61_by_type_bn"].values()) == pytest.approx(c["national_ops_bn"], abs=1e-10)
    d = table("park_municipalities.csv")
    assert len(d) == c["municipalities"] == 19367
    assert not d.fips.duplicated().any() and not d.uid.duplicated().any()
    assert d.E61.sum() == pytest.approx(c["matched_ops_bn"], abs=1e-9)
    assert c["matched_share_of_sl_E61"] == pytest.approx(.51120777042657)
    assert .77 < c["mexican_origin_share"] < .79
    assert .62 < c["population_share"] < .63
    assert not parks["capital_identified"]
    assert parks["factor_within_covered_cities"] < 1 < parks["factor_vs_national_municipal_price"]


def test_new_york_uses_city_boundary_not_headquarters_county():
    d = table("park_municipalities.csv")
    ny = d[d.uid.eq("362061194805")]
    assert len(ny) == 1
    row = ny.iloc[0]
    assert row.fips == "3651000" and row["pop"] > 8_000_000
    assert row.group_amount_bn == pytest.approx(row.E61 * row.mex / row["pop"], abs=1e-12)


def test_park_state_price_principal_and_partial_budget_weights():
    parks = read("parks.json")
    states = table("park_states.csv")
    assert states.case_weight.sum() == pytest.approx(1, abs=1e-11)
    assert states.municipal_budget_fraction.between(0, 1).all()
    assert states.case_index_delta.sum() == pytest.approx(parks["case_matched_municipal_bridge_index_delta"], abs=1e-12)
    assert (states.case_weight * states.case_state_price_relative).sum() == pytest.approx(parks["case_state_index_reproduced"], abs=1e-11)
    assert parks["case_state_index_reproduced"] == pytest.approx(1.074678653, abs=1e-9)
    assert parks["case_raked_factor_on_matched_municipal_block"] == pytest.approx(.9202201001423, abs=1e-11)


def test_unmatched_parks_are_bounded_not_silently_zero():
    parks = read("parks.json")
    raw = parks["raw_2022_allocations_bn"]
    lo, hi = raw["unmatched_delta_bound"]
    assert lo < 0 < hi
    assert hi - lo == pytest.approx(parks["coverage"]["unmatched_municipal_ops_bn"])
    assert raw["all_unpriced_E61_total"] > 19
    lo, hi = raw["all_unpriced_E61_delta_bound"]
    assert hi - lo == pytest.approx(raw["all_unpriced_E61_total"])


def test_tpl_is_a_geographic_sample_and_never_a_capital_price():
    tpl = read("parks.json")["tpl_cross_check"]
    d = table("park_tpl_cities.csv")
    assert len(d) == tpl["cities"] == 89
    assert d.fips.str.fullmatch(r"\d{7}").all()
    assert "PS-prefixed" in tpl["scope"]
    assert "not asset values" in tpl["limits"]


def test_case_prices_use_full_evaluator_and_preserve_scope():
    case = read("case_prices.json")
    assert case["case_key"] == "oct16" and not case["adopted"]
    assert all(g["pass"] for g in case["gates"])
    assert len(case["gates"]) > 800
    q = table("case_scenario_methods.csv")
    baseline = case["canonical_band_bn"]
    for scenario, d in q.groupby("scenario"):
        assert len(d) == 4
        for end, target in zip(["low", "high"], baseline):
            rows = d[d.end.eq(end)]
            assert len(rows) == 2
            assert (rows.cost_bn - rows.delta_bn).mean() == pytest.approx(target, abs=1e-9)
    scenarios = table("case_scenarios.csv").set_index("scenario")
    assert scenarios.loc["existing_k12_operating_already_included", "delta_low_bn"] == 0
    assert scenarios.loc["existing_college_er_already_included", "delta_high_bn"] == 0
    assert scenarios.loc["college_capital_gross_book_proxy", "delta_low_bn"] < 0
    assert scenarios.loc["parks_matched_municipal_proxy", "delta_low_bn"] < 0
    assert case["identification"]["complete_where_used_package"] == "not identified"


def test_existing_k12_factor_is_not_added_again():
    case = read("case_prices.json")
    assert case["existing_k12_operating_factor"] == pytest.approx(1.0341917412164008, abs=1e-12)
    assert case["incremental_k12_operating_delta_bn"] == 0
    scenarios = table("case_scenarios.csv").set_index("scenario")
    assert scenarios.loc["k12_capital_existing_k_denominator_diagnostic", "delta_low_bn"] < scenarios.loc["stipulated_k12_capital_input", "delta_low_bn"]


def test_all_raw_inputs_are_available_and_pinned_including_recovery_mirrors():
    acquire = load_module("acquire")
    for name in ["sources.json", "park_sources.json"]:
        for relative, receipt in read(name).items():
            path = acquire.source(acquire.REPO / relative)
            assert acquire.sha(path) == receipt["sha256"]
    for receipt in read("acquisition.json")["files"]:
        assert acquire.sha(acquire.REPO / receipt["path"]) == receipt["sha256"]
    size = sum(p.stat().st_size for p in (HERE / "_cache").rglob("*") if p.is_file())
    assert size < 5_000_000_000


def test_source_mirror_rejects_corrupt_release_without_overwriting_raw(tmp_path, monkeypatch):
    acquire = load_module("acquire")
    monkeypatch.setattr(acquire, "REPO", tmp_path)
    monkeypatch.setattr(acquire, "HERE", tmp_path)
    original = "raw/example.csv"
    good = hashlib.sha256(b"correct release").hexdigest()
    monkeypatch.setattr(acquire, "MIRRORS", {original: ("https://example.invalid/data.csv", good)})
    mirror = tmp_path / "_cache/source_mirror"
    mirror.mkdir(parents=True)
    (mirror / "example.csv").write_bytes(b"different release")
    with pytest.raises(ValueError, match="corrupt source mirror"):
        acquire.recover_sources()
    assert not (tmp_path / original).exists()


def test_csv_outputs_are_lf_and_finite_prices():
    for path in OUT.glob("*.csv"):
        assert b"\r\n" not in path.read_bytes(), path
    prices = table("case_scenarios.csv")
    assert np.isfinite(prices[["delta_low_bn", "delta_high_bn", "cost_low_bn", "cost_high_bn"]]).all().all()
