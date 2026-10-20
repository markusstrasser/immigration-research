"""Gates for pension_legacy.py: the pinned 2024 BEA, Z.1 and Financial Report cells parse to the values the RESULT
records, the shares and weights are sane, and a rebuild reproduces derived/ byte for byte.

Run from the repository root (a worktree drops --no-project):
  uv run --no-project python3 -m pytest infra/immigration-fiscal/pension_legacy_2026_09_30/ -q
The inputs live in the ignored _cache/; without them the tests skip (fetch with `pension_legacy.py --fetch`).
"""
from __future__ import annotations

import csv
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pension_legacy", HERE / "pension_legacy.py")
pl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pl)

pytestmark = pytest.mark.skipif(not (HERE / "_cache/Section7All_xls.xlsx").exists(), reason="inputs not fetched (_cache/)")

# $bn, 2024, as published; the RESULT quotes these
BEA = {"domestic_interest_total": 1118.870, "domestic_interest_federal": 844.262, "domestic_interest_state_local": 274.608,
       "sl_imputed_interest": 162.963, "sl_plan_monetary_interest": 69.729, "sl_plan_dividends": 46.333,
       "sl_interest_accrued_on_entitlements": 442.066, "sl_actual_employer_contributions": 214.289,
       "sl_imputed_employer_contributions": -41.578, "fed_imputed_interest": 62.006, "fed_plan_monetary_interest": 89.071,
       "fed_plan_interest_total": 151.077, "fed_actual_employer_contributions": 250.510,
       "fed_imputed_employer_contributions": -144.348, "supp_state_local_retirement": 192.994,
       "defense_comp_civilian": 132.631, "defense_comp_military": 207.101, "nondefense_comp": 267.716}
Z1 = {(2023, "FL223073045.Q"): 3125.593, (2024, "FL223073045.Q"): 3005.859, (2023, "FL224190043.Q"): 8942.670,
      (2023, "FL343073045.Q"): 1163.664, (2024, "FL343073045.Q"): 961.965, (2023, "FL344190045.Q"): 3831.670,
      (2023, "FL343069245.Q"): 2639.431}


def recorded() -> dict[str, float]:
    return {r["item"]: float(r["value_bn"]) for r in csv.DictReader(open(HERE / "derived/measured_2024.csv"))}


def test_bea_cells_parse_to_recorded_values():
    m, extra = pl.measure_bea()
    rec = recorded()
    for k, want in BEA.items():
        assert m[k][0] == pytest.approx(want, abs=5e-7), k
        assert rec[k] == pytest.approx(want, abs=5e-7), k
    assert any("actuarial liabilities" in n for n in extra["notes"]["T3.3"])
    # the pension parts of the row the case holds at zero
    assert m["sl_imputed_interest"][0] + m["fed_imputed_interest"][0] + m["fed_plan_monetary_interest"][0] == pytest.approx(314.040, abs=5e-7)
    # normal cost sits in compensation: T7.8's state-local retirement = DB normal cost + DC contributions (T7.25 line 8, 20.283)
    assert BEA["sl_actual_employer_contributions"] + BEA["sl_imputed_employer_contributions"] + 20.283 == pytest.approx(BEA["supp_state_local_retirement"], abs=1e-9)
    # S&L plan interest accrued = monetary + dividends + imputed + implied funding from holding gains (T7.24 line 30, 163.041)
    assert 69.729 + 46.333 + 162.963 + 163.041 == pytest.approx(442.066, abs=1e-9)


def test_z1_and_financial_report_parse():
    z = pl.measure_z1()
    for (y, code), want in Z1.items():
        assert z[y][code] == pytest.approx(want, abs=5e-7), (y, code)
    fr = pl.measure_fr()
    assert fr["pension_interest_fy24"] == {"civilian": 75.3, "military": 75.7, "total": 151.0}
    assert fr["opeb_end_fy24"] == {"civilian": 443.1, "military": 1297.8, "total": 1740.9}
    assert fr["opeb_interest_fy24"] == {"civilian": 12.2, "military": 33.3, "total": 45.5}
    census = pl.measure_census_counts()
    assert census[2000] == pytest.approx(20.640711) and census[2010] == pytest.approx(31.798258)
    assert round(census[1990], 1) == 13.5


def test_shares_and_weights_are_sane():
    m, extra = pl.measure_bea()
    mix = pl.function_mixes(pl.measure_aspep(), m)
    for plan, d in mix.items():
        assert sum(d.values()) == pytest.approx(1.0, abs=1e-12), plan
        assert all(w >= 0 for w in d.values())
    assert 0.45 < mix["state_local"]["education_services"] < 0.55          # teachers dominate
    assert 0.15 < mix["state_local"]["public_order_safety"] < 0.20        # police, fire, courts, corrections
    share, response = pl.group_shares()
    for g in pl.GROUPS:
        for e in ("low", "high"):
            assert all(0 < s < 0.3 for s in share[g][e].values()), (g, e)
    assert response["low"]["defense"] == 0 and response["high"]["defense"] == 0
    assert share["mexican_origin"]["low"]["education_services"] == pytest.approx(0.157111, abs=5e-7)   # rekey_line_shares_sept29
    rel, _ = pl.headcount_path(extra["population"], pl.measure_census_counts())
    assert rel[2024] == 1.0 and all(0 < rel[y] <= 1.0 + 1e-12 for y in rel if y < 2024)
    factors, weights = pl.time_factors(rel, extra["population"], pl.measure_z1())
    for (plan, arm), w in weights.items():
        if arm.startswith("vintage"):
            assert min(w.values()) >= 0
        assert 0.3 < factors[plan][arm] < 1.0, (plan, arm)


def test_rebuild_reproduces_derived(tmp_path):
    run = subprocess.run([sys.executable, str(HERE / "pension_legacy.py"), "--case", "sept29", "--out-dir", str(tmp_path)],
                         capture_output=True, text=True, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"})
    assert run.returncode == 0, run.stderr[-2000:]
    names = sorted(p.name for p in (HERE / "derived").iterdir() if p.is_file())   # later cases sit in derived/<case>/
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    assert [n for n in names if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()] == []
    for n in names:
        assert b"\r\n" not in (HERE / "derived" / n).read_bytes(), n


@pytest.mark.parametrize("corruption", ["published_count", "response", "nonfinite", "duplicate"])
def test_group_export_rejects_wrong_frame_or_line(corruption, monkeypatch, tmp_path):
    with pl.GROUP_LINES.open() as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    group = "A1_third_plus_nh_white"
    target = next(r for r in rows if r["group"] == group and r["basis"] == "accrual"
                  and r["end"] == "low" and r["line"] == "education_services")
    if corruption == "published_count":
        population = next(r for r in rows if r["group"] == group and r["basis"] == "accrual"
                          and r["end"] == "low" and r["line"] == "population")
        population["amount_bn"] = "40900000"
    elif corruption == "response":
        target["response"] = "0"
    elif corruption == "nonfinite":
        target["amount_bn"] = "nan"
    else:
        rows.append(target.copy())
    path = tmp_path / "group_lines.csv"
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    monkeypatch.setattr(pl, "GROUP_LINES", path)
    with pytest.raises(ValueError, match=r"\[BLOCKED\]"):
        pl.group_shares()


def test_same_keys_pension_gap_uses_row4_and_differs_from_engine():
    share, _ = pl.group_shares()
    # Source anchors independently reconstructed from the current row-4 CPS/MEPS export.
    rows = list(csv.DictReader(open(HERE / "derived/summary.csv")))
    def interest(group, end):
        return float(next(r["interest_total_bn"] for r in rows
                          if r["arm"] == "adopted" and r["group"] == group and r["end"] == end))
    for end in ("low", "high"):
        assert share["A1_third_plus_nh_white"][end]["education_services"] < 0.103
        assert interest("mexican_origin_rough_minus_A1_white", end) == pytest.approx(
            interest("mexican_origin_rough", end) - interest("A1_third_plus_nh_white", end), abs=2e-6)
        assert interest("mexican_origin_minus_A1_white", end) > interest("mexican_origin_rough_minus_A1_white", end)
    assert interest("mexican_origin_rough_minus_A1_white", "low") == pytest.approx(4.8918, abs=0.0001)
    assert interest("mexican_origin_rough_minus_A1_white", "high") == pytest.approx(4.6828, abs=0.0001)


def test_live_population_uses_authoritative_lineage_count():
    import json
    payload = json.loads((pl.FISCAL / "main_case_2026_10_15/derived/corrections.json").read_text())
    try:
        pl.use_case("oct15")
        expected = payload["meta"]["population_v8"]["with_coverage"]
        assert pl.POPULATION == expected
        baseline = payload["meta"]["lineage"]["counts"]["lineage_population"]
        assert expected > baseline
        pl.group_shares()  # Rejects any comparator slice on the old population frame.
    finally:
        pl.use_case("sept29")


def test_service_carriers_follow_selected_parent_key_even_at_zero_response():
    lines = {"defense": {"side": "spending", "key": "population", "response": 0},
             "selected": {"national_bn": 0, "response": 0},
             "inactive": {"national_bn": 0, "response": 0}}
    common = {"kind": "line", "side": "spending", "parent_line": "defense"}
    carriers = {"selected": {**common, "parent_key": "population"},
                "inactive": {**common, "parent_key": "wages"}}
    assert pl.service_carrier_amount("defense", lines, {"selected": 2, "inactive": 999}, carriers) == 2


def test_service_carrier_rejects_missing_amount_or_wrong_response():
    lines = {"education_services": {"side": "spending", "key": "education_mix", "response": 1},
             "carrier": {"national_bn": 0, "response": 1}}
    carriers = {"carrier": {"kind": "line", "side": "spending", "parent_line": "education_services",
                            "parent_key": "education_mix"}}
    with pytest.raises(ValueError, match="missing selected"):
        pl.service_carrier_amount("education_services", lines, {}, carriers)
    lines["carrier"]["response"] = 0
    with pytest.raises(ValueError, match="parent response"):
        pl.service_carrier_amount("education_services", lines, {"carrier": 2}, carriers)


def test_receipt_carrier_uses_scenario_and_restores_economic_sign():
    lines = {"enterprise_surplus": {"side": "receipts", "scenario": "cbo_collective", "response": 1},
             "carrier": {"national_bn": 0, "response": 1}}
    carriers = {"carrier": {"kind": "line", "side": "receipt", "parent_line": "enterprise_surplus",
                             "parent_key": "cbo_collective"}}
    assert pl.service_carrier_amount("enterprise_surplus", lines, {"carrier": -.2}, carriers) == .2
    lines["enterprise_surplus"]["scenario"] = "population"
    with pytest.raises(ValueError, match="key/scenario is absent"):
        pl.service_carrier_amount("enterprise_surplus", lines, {"carrier": -.2}, carriers)


def test_every_carrier_keeps_parent_service_and_resource_nature(monkeypatch):
    carriers = {"line": {"kind": "line", "side": "spending", "parent_line": "state_price_health_services", "parent_key": "population"},
                "capital": {"kind": "capital", "parent_line": "health_sl"},
                "production": {"kind": "production", "parent_line": "production"},
                "education_fee": {"kind": "capital", "parent_line": "k12_user_fees"},
                "health_fee": {"kind": "capital", "parent_line": "health_fed_user_fees"}}
    lines = {key: {"amount_bn": .25, "response": 1.} for key in carriers}
    lines["state_price_health_services"] = {"key": "population"}
    monkeypatch.setattr(pl, "COMPLETION_CARRIERS", carriers)
    monkeypatch.setattr(pl, "SERVICE_ATTRIBUTIONS", [])
    pl.completion_attribution("low", lines)
    assert len(pl.SERVICE_ATTRIBUTIONS) == 5
    assert [row[4] for row in pl.SERVICE_ATTRIBUTIONS] == ["health_services", "health_services", "private_production", "education_services", "health_services"]
    assert [row[-1] for row in pl.SERVICE_ATTRIBUTIONS] == [True, False, False, False, False]
    del lines["capital"]
    with pytest.raises(ValueError, match="parent/kind/amount"):
        pl.completion_attribution("high", lines)


def test_defense_stock_bridge_adds_people_and_does_not_repeat_native_amount():
    counts = {"baseline_account_union": 100., "baseline_lineage_population": 130.,
              "reporters": 10., "nonreporters": 5.}
    population = {"completion": 15., "coverage": 2., "without_coverage": 145., "with_coverage": 147.}
    # Baseline raw price=.2bn/person. Native children already add1bn to the full raw amount.
    result = pl.defense_stock_bridge(counts, population, 20., 26., 27., 1.)
    assert result["completion_raw_bn"] == 3.
    assert result["coverage_raw_bn"] == .4
    assert result["additional_stock_raw_bn"] == pytest.approx(2.4, abs=1e-12)
    assert result["stock_raw_bn"] == pytest.approx(29.4, abs=1e-12)
    with pytest.raises(ValueError, match="baseline/native bridge"):
        pl.defense_stock_bridge(counts, population, 20., 26., 27., 0.)
    with pytest.raises(ValueError, match="population bridge"):
        pl.defense_stock_bridge(counts, {**population, "with_coverage": 147.000002}, 20., 26., 27., 1.)


def test_live_stock_comparisons_reject_case_rough_engine_pairing(monkeypatch):
    assert pl.comparison_tags("mexican_origin_rough_minus_A1_white") == ["comparison", "rough", "rough"]
    assert pl.comparison_tags("case_minus_rough_bridge") == ["bridge", "case", "rough"]
    with pytest.raises(ValueError, match="unrecognized live pension comparison"):
        pl.comparison_tags("mexican_origin_minus_A1_white")
    monkeypatch.setattr(pl.COMPARISON, "engine_for", lambda group: "case" if group == "mexican_origin_rough" else "rough")
    with pytest.raises(SystemExit, match="different engine tags"):
        pl.comparison_tags("mexican_origin_rough_minus_A1_white")


def test_coverage_composition_and_zero_response_keep_household_prices(tmp_path):
    import json
    lane = tmp_path / "coverage"
    base = lane / "inputs/oct15_base"
    base.mkdir(parents=True)
    (lane / "derived").mkdir()
    household = {"meta": {"case": "main_case_2026_10_15", "basis": "set"}, "generations": {}}
    for gen in ("G1", "G2", "G3plus"):
        household["generations"][gen] = {"low": {"rows": [
            {"id": "defense", "side": "spending", "key": "population", "amount_bn": 20.}]}}
    (base / "lines.json").write_text(json.dumps(household))
    (base / "generation_results.csv").write_text("convention,generation,band_end,population\n"
        + "".join(f"a,{gen},low,100\n" for gen in household["generations"]))
    (base / "manifest.json").write_text(json.dumps({"files": [
        {"name": name, "sha256": pl.sha(base / name)} for name in ("lines.json", "generation_results.csv")]}))
    prices = {gen: {"0-4": {"net_missing_people": 10., "by_end": {"low":
             {"coverage_bn": 1., "per_member_usd": 1e8}}}} for gen in household["generations"]}
    scenario = {"by_generation_age_band": prices,
        "implied_net_missing_people_by_age_band": {g: {"0-4": 10.} for g in prices},
        "ends": {"low": {"decomposition": {"total_cost_bn": 3., "line_parts": [
            {"source_line": "education_services", "source_side": "spending", "economic_class": "fiscal_line", "coverage_bn": 3.}]}}}}
    raw = {"key": "oct15", "sets": {"set": {"scenarios": {"central": scenario}}}}
    source = lane / "derived/coverage.json"
    source.write_text(json.dumps(raw))
    coverage = {"net_missing_people": 30., "which": "set", "file": "coverage/derived/coverage.json",
        "sha256": pl.sha(source), "construction": "central", "by_end": {"low": {"total_bn": 3.}}}
    lines = {"defense": {"side": "spending", "response": 0},
             "education_services": {"side": "spending", "response": .5}}
    amounts = pl.coverage_service_amounts(coverage, "low", lines, list(lines), source_root=tmp_path)
    assert amounts == {"defense": 6., "education_services": 6.}
    prices["G2"]["0-4"]["by_end"]["low"]["per_member_usd"] += 1000
    source.write_text(json.dumps(raw))
    coverage["sha256"] = pl.sha(source)
    with pytest.raises(ValueError, match="age-price mismatch"):
        pl.coverage_service_amounts(coverage, "low", lines, list(lines), source_root=tmp_path)


def test_v9_va_split_preserves_state_health_and_total_before_response(monkeypatch):
    """VA is a federal health subblock; state-price overlays stay civilian."""
    monkeypatch.setattr(pl, "v9_military_fraction", lambda: ({}, .5))
    mixes = {"federal_civilian": {"health_services": .2, "education_services": .8},
             "state_local": {"health_services": .3, "education_services": .7}}
    result = pl.v9_function_mixes(mixes)
    assert result["state_local"]["health_services"] == .3
    assert result["state_local"]["health_services_va"] == 0
    assert result["federal_civilian"]["health_services"] == 0
    assert result["federal_civilian"]["health_services_va"] == .1
    assert result["federal_civilian"]["health_services_federal_other"] == .1
    # Raw health .12 plus state-price overlay .02: federal service excludes the overlay.
    federal_other = (.14-.02-.5*.12)/(1-.5)
    before = .1*.12+.1*federal_other
    after = .1*federal_other
    assert before == pytest.approx(.2*.12, abs=1e-15)
    assert before-after == pytest.approx(.1*.12, abs=1e-15)


def test_v9_raw_health_restores_only_the_declared_military_subblock(monkeypatch):
    monkeypatch.setattr(pl, "v9_military_fraction", lambda: ({"central_national_bn": 20.}, .5))
    lines = {"health_services": {"national_bn": 100.}}
    assert pl.v9_raw_health(8., "health_services", lines) == 10.
    assert pl.v9_raw_health(8., "state_price_health_services", lines) == 8.
    lines["health_services"]["national_bn"] = 10.
    with pytest.raises(ValueError, match="military factor"):
        pl.v9_raw_health(8., "health_services", lines)


def test_v9_service_export_fails_loud_on_absent_or_changed_source(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(pl, "GROUP_LINES", tmp_path / "group_lines_oct16.csv")
    monkeypatch.setattr(pl, "FISCAL", tmp_path)
    with pytest.raises(ValueError, match="raw-service/typed-part"):
        pl.v9_service_sources()
    source = tmp_path / "service_parts_oct16.json"
    dep = tmp_path / "source.py"
    dep.write_text("first source\n")
    rows = [dict(group=group, end=end, basis="accrual", raw_lines=[], parts=[])
            for group in pl.GROUP_SOURCES.values() for end in ("low", "high")]
    source.write_text(json.dumps(dict(case="oct16", runs=rows, source_sha256={dep.name: pl.sha(dep)})))
    assert len(pl.v9_service_sources()) == 8
    dep.write_text("changed source\n")
    with pytest.raises(ValueError, match="stale pension service source"):
        pl.v9_service_sources()


def test_v9_college_operating_routes_without_capital_or_va_double_application(monkeypatch):
    group = "A1_third_plus_nh_white"
    parts = [dict(item="15", source_line="education_services", kind="college_operating", delta_bn=-2.),
             dict(item="15", source_line="college", kind="college_capital", delta_bn=-100.),
             dict(item="14", source_line="income_security_services", kind="administration", delta_bn=-1.),
             dict(item="13", source_line="health_services", kind="va_medical", delta_bn=-99.)]
    monkeypatch.setattr(pl, "V9_SERVICE_RUNS", {(group, "low"): {"parts": parts}})
    monkeypatch.setattr(pl, "V9_SERVICE_PARTS", [])
    monkeypatch.setattr(pl, "v9_military_fraction", lambda: ({}, .5))
    lines = {"education_services": {"national_bn": 100.}, "income_security_services": {"national_bn": 50.}}
    shares = {"education_services": .2, "income_security_services": .1,
              "health_services": .14, "health_services_va": .12}
    pl.v9_service_adjustments(group, "low", lines, shares)
    assert shares["education_services"] == pytest.approx(.18, abs=1e-15)
    assert shares["income_security_services"] == pytest.approx(.08, abs=1e-15)
    assert shares["health_services"] == .14
    assert shares["health_services_va"] == .12
    excluded = next(p for p in pl.V9_SERVICE_PARTS if p["kind"] == "college_capital")
    assert excluded["delta_capital_excluded_bn"] == -100.
    assert excluded["employee_service"] is False


def test_v9_item21_uses_non_va_key_and_state_overlay_without_capital(monkeypatch):
    parts = [dict(source_line="health_services", population="original_union", delta_bn=1.25),
             dict(source_line="health_services", population="coverage", delta_bn=.75),
             dict(source_line="state_price_health_services", population="original_union", delta_bn=2.5),
             dict(source_line="state_price_health_services", population="coverage", delta_bn=.5),
             dict(source_line="health_sl", delta_bn=100.)]
    interactions = {k: {"by_end": {"low": {"total_bn": v}}} for k, v in
                    (("native_minor_calibration", 1.), ("coverage_tenure", 1.))}
    metadata = {"health_residual_key": {"by_end": {"low": {"parts": parts, "total_bn": 105.}},
                                      "count_interactions": interactions}}
    count = [dict(line="item21:health", source_line="health_services", change_bn=.5),
             dict(line="item21:overlay", source_line="state_price_health_services", change_bn=.7),
             dict(line="item21:capital", source_line="health_sl", change_bn=1.6,
                  economic_class="capital_return", source_capital_rate=.02, capital_rate=.04)]
    monkeypatch.setattr(pl, "V9_META", metadata)
    monkeypatch.setattr(pl, "V9_SERVICE_PARTS", [])
    monkeypatch.setattr(pl, "v9_military_fraction", lambda: ({"central_national_bn": 20.}, .5))
    lines = {"health_services": {"national_bn": 100.}}
    shares = {"health_services": .14, "health_services_va": .12, "health_services_federal_other": .12}
    pl.v9_health_residual_adjustment("mexican_origin", "low", lines, shares, count)
    assert shares["health_services_va"] == .12
    assert shares["health_services_federal_other"] == pytest.approx(.12+2.5/80, abs=1e-15)
    assert shares["health_services"] == pytest.approx(.14+2.5/80+3.7/306.539, abs=1e-15)
    assert pl.V9_SERVICE_PARTS[-1]["capital_employee_service"] is False
    parts[-1]["delta_bn"] = 101.
    with pytest.raises(ValueError, match="item21 source parts"):
        pl.v9_health_residual_adjustment("mexican_origin", "low", lines, shares, count)


def test_v9_state_price_overlay_does_not_enter_federal_employee_health(monkeypatch):
    group = "A1_third_plus_nh_white"
    monkeypatch.setattr(pl, "V9_SERVICE_RUNS", {(group, "low"): {"parts": []}})
    monkeypatch.setattr(pl, "V9_SERVICE_PARTS", [])
    monkeypatch.setattr(pl, "v9_military_fraction", lambda: ({}, .5))
    lines = {"education_services": {"national_bn": 100.}, "income_security_services": {"national_bn": 50.}}
    shares = {"education_services": .2, "income_security_services": .1,
              "health_services": .14, "health_services_va": .12, "_health_state_price": .02}
    pl.v9_service_adjustments(group, "low", lines, shares)
    assert shares["health_services_federal_other"] == pytest.approx(.12, abs=1e-15)
    assert shares["health_services"] == .14
    assert shares["health_services_va"] == .12


def test_v9_live_outputs_keep_booked_values_and_separate_service_keys():
    import json
    live = HERE / "derived/oct16"
    assert (live / "measured_2024.csv").read_bytes() == (HERE / "derived/oct15/measured_2024.csv").read_bytes()
    payload = json.loads((pl.FISCAL / "main_case_2026_10_16/derived/corrections.json").read_text())
    rules = json.loads((live / "service_rules.json").read_text())
    assert rules["population"] == payload["meta"]["population_v9"]["with_coverage"]
    assert all(r["response"] == 0 for r in rules["va_medical"])
    rows = list(csv.DictReader((live / "group_shares.csv").open()))
    assert {float(r["response"]) for r in rows if r["line"] == "health_services_va"} == {0.}
    assert {float(r["response"]) for r in rows if r["line"] == "health_services_federal_other"} == {1.}
    changes = [r for r in rules["operating_adjustments"] if r["kind"] == "item21_non_va_health"]
    assert {(r["group"], r["end"]) for r in changes} == {
        (g, e) for g in ("mexican_origin", "mexican_origin_rough") for e in ("low", "high")}
    assert all(not r["va_key_changed"] and not r["capital_employee_service"] for r in changes)
