"""Live v8 evidence, response-only controls, and fail-loud drift behavior."""
import importlib.util
import json
import os
import subprocess
from pathlib import Path
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("tables_oct15", HERE / "tables_oct15.py")
tables = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tables)


def test_live_pairing_ignores_annotations_and_rejects_missing_live_numbers():
    records = [{"section": "6", "column": "historical", "item": "old", "oct15": ""},
               {"section": "7", "column": "pairing_on_priced_count", "item": "published pairing (low)", "oct15": "440"}]
    assert tables.live_pairing_values(records) == {("pairing_on_priced_count", "published pairing (low)"): 440.0}
    records[1]["oct15"] = ""
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] missing or non-numeric oct15"):
        tables.live_pairing_values(records)


def test_evidence_drift_blocks_before_writing(tmp_path, monkeypatch):
    evidence = tmp_path / "input.csv"
    evidence.write_text("value\n1\n")
    monkeypatch.setattr(tables, "F", tmp_path)
    monkeypatch.setattr(tables, "INPUTS", [evidence])
    pin = tmp_path / "pins.json"
    pin.write_text(json.dumps({"inputs": tables.snapshot()}))
    monkeypatch.setattr(tables, "PINS", pin)
    evidence.write_text("value\n2\n")
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] final evidence drift"):
        tables.main()
    assert tables.snapshot()["input.csv"]["numeric_cells"] == [[0, "value", 2.0]]


def test_unknown_postengine_class_rule_blocks_before_case_loading():
    result = subprocess.run(["node", str(HERE / "engine_breaks_sept29.cjs"), "--case", "oct15", "--probe-only"],
                            env={**os.environ, "C2_POSTENGINE_CLASS_RULE": "invented"}, capture_output=True, text=True)
    assert result.returncode != 0
    assert "[BLOCKED] unknown C2_POSTENGINE_CLASS_RULE invented" in result.stderr


def comparator_fixture():
    return [{"case": "oct15", "arm": "combined_rules_only", "allocation": "personal",
             "mortality_convention": convention, "mortality_bound": bound, "basis": basis,
             "group_mortality": "whole-population" if convention == tables.MIXED_MORTALITY and group in ("mexican_origin_engine", tables.ROUGH_LINEAGE) else "own-group",
             "engine": "case" if group == "mexican_origin_engine" else "rough",
             "mixed_unit_removal_bn": 10 if group in ("mexican_origin_engine", tables.ROUGH_LINEAGE) else -5 if group == 'A1_third_plus_nh_white' else 0,
             "comparator_item11_bn": -5 if group == 'A1_third_plus_nh_white' else 0,
             "item11_paired_se_bn": 3 if group == 'A1_third_plus_nh_white' else '',
             "mixed_unit_asymmetry": "lineage measured; comparator unmeasured",
             "cost_without_item11_bn": 340 if group in ("mexican_origin_engine", tables.ROUGH_LINEAGE) else -20,
             "group": group, "end": end, "cost_bn": 350 if group in ("mexican_origin_engine", tables.ROUGH_LINEAGE) else -25 if group == 'A1_third_plus_nh_white' else -20}
            for convention, bound in tables.MORTALITY_READINGS for basis in ("accrual", "cash")
             for group in ("mexican_origin_engine", tables.ROUGH_LINEAGE, "A1_third_plus_nh_white", "A3_third_plus_nh_white_at_union_ages")
            for end in ("low", "high")]


def test_comparator_pairing_requires_explicit_case_and_mortality_labels():
    records = comparator_fixture()
    values = tables.comparator_values(records)
    assert tables.comparator_gap(values, tables.MIXED_MORTALITY, "none", "accrual", "A1_third_plus_nh_white") == [375, 375]
    # The same numeric whole-headline/own-comparator pairing cannot pass without its label.
    records[0].pop("mortality_convention")
    with pytest.raises(SystemExit, match="explicit mortality convention/bound required"):
        tables.comparator_values(records)
    records = comparator_fixture()
    records[0]["case"] = "oct14"
    with pytest.raises(SystemExit, match="comparator case must be oct15"):
        tables.comparator_values(records)
    records = comparator_fixture()
    next(r for r in records if r["group"] == tables.ROUGH_LINEAGE)["group_mortality"] = "own-group"
    with pytest.raises(SystemExit, match="mortality pairing requires explicit label 'own-group mortality'"):
        tables.comparator_values(records)


def test_comparator_rejects_mixed_engines_and_undeclared_item11():
    records = comparator_fixture()
    next(r for r in records if r["group"] == tables.ROUGH_LINEAGE)["engine"] = "case"
    with pytest.raises(SystemExit, match="different engine tags"):
        tables.comparator_values(records)
    records = comparator_fixture()
    next(r for r in records if r["group"] == tables.ROUGH_LINEAGE).pop("mixed_unit_asymmetry")
    with pytest.raises(SystemExit, match="explicit mixed-unit asymmetry required"):
        tables.comparator_values(records)


def test_bridge_closes_at_every_mortality_bound_and_rejects_incomplete_parts():
    values = tables.comparator_values(comparator_fixture())
    parts = [{"case": "oct15", "arm": "combined_rules_only", "basis": basis, "end": end,
              "case_engine": "case", "rough_engine": "rough", "mortality_convention": mortality,
              "mortality_bound": bound, "side": "spending", "line": "source",
              "case_bn": 350, "rough_bn": 350, "case_minus_rough_bn": 0}
             for mortality, bound in tables.MORTALITY_READINGS for basis in ("accrual", "cash") for end in ("low", "high")]
    assert set(tables.bridge_values(parts, values)) == {(mortality, bound, basis, end)
        for mortality, bound in tables.MORTALITY_READINGS for basis in ("accrual", "cash") for end in ("low", "high")}
    with pytest.raises(SystemExit, match="missing itemized bridge"):
        tables.bridge_values(parts[:-1], values)
    values[tables.OWN_MORTALITY, "low", "accrual", "mexican_origin_engine", "low"] += 1
    with pytest.raises(SystemExit, match="itemized bridge closure"):
        tables.bridge_values(parts, values)


def test_comparator_missing_bound_or_duplicate_fails():
    records = comparator_fixture()
    with pytest.raises(SystemExit, match="missing comparator row"):
        tables.comparator_values(records[:-1])
    with pytest.raises(SystemExit, match="duplicate comparator row"):
        tables.comparator_values([*records, records[0]])


@pytest.mark.parametrize("got,want", [(float("nan"), 1), (1, float("inf"))])
def test_nonfinite_principal_or_calculation_cannot_pass_tolerance(got, want):
    with pytest.raises(SystemExit, match="non-finite value"):
        tables.check("principal", got, want, 1e-9)


def test_first_year_rejects_method_end_mismatch_before_pricing():
    script = """
const FY=require(process.argv[1]);
const P={LANE:'unused',readJson:()=>({v8:{end_specifications:{set:[[16,11],[15,11]],cash:[[16,11],[16,11]]}}})};
try { FY.run(P,[350,430],()=>{}); process.exit(2); }
catch(e) { console.error(e.message); process.exit(1); }
"""
    result = subprocess.run(["node", "-e", script, str(HERE / "first_year_v8.cjs")], capture_output=True, text=True)
    assert result.returncode == 1
    assert "[BLOCKED] first-year v8: set/cash methods must declare the same pair of personal ends" in result.stderr


def test_first_year_response_controls_and_postengine_closure():
    report = json.loads((tables.D / "first_year_item6_oct15.json").read_text())
    case = json.loads((tables.CASE / "summary.json").read_text())["v8"]
    assert all(row["pass"] for row in report["checks"])
    for basis in ("set", "cash"):
        principal = case["companions"]["first_year"]
        expected = principal["band_bn"] if basis == "set" else principal["cash"]["band_bn"]
        assert report["variants"]["fixed_capital"][basis] == pytest.approx(expected, abs=1e-9, rel=0)
        for mode in ("fixed_capital", "whole", "corporate_only", "off"):
            for end in (f"low_end_{case['end_specifications']['set'][0][0]}",
                        f"high_end_{case['end_specifications']['set'][0][1]}"):
                rows = [r for r in report["components"] if r["mode"] == mode and r["basis"] == basis and r["end"] == end]
                for scope in ("union", "added", "lineage"):
                    cells = [r for r in rows if r["scope"] == scope]
                    assert len(cells) == 4
                    for row in cells:
                        if mode == "whole":
                            factor = 1
                        elif mode == "off" or row["line"] == "remaining_production_property":
                            factor = 0
                        elif mode == "corporate_only":
                            factor = int(row["line"].startswith("corporate_"))
                        else:
                            factor = report["calibration"]["first_year_multiplier"]
                        assert row["first_year_response"] == pytest.approx(row["long_run_response"] * factor, abs=1e-12)
                moves = {s: sum(r["cost_change_from_whole_bn"] for r in rows if r["scope"] == s)
                         for s in ("union", "added", "lineage")}
                assert moves["lineage"] == pytest.approx(moves["union"] + moves["added"], abs=1e-9, rel=0)
                i = 0 if end.startswith("low") else 1
                post = next(r for r in report["post_components"] if r["mode"] == mode and r["basis"] == basis and r["end"] == end)
                assert report["variants"][mode][basis][i] - report["variants"]["whole"][basis][i] == pytest.approx(moves["lineage"]+post["cost_change_from_whole_bn"], abs=1e-9, rel=0)
    assert report["thresholds"]["low_bn"] == pytest.approx(0.75 * sum(case["band_bn"]) / 2, abs=1e-9)
    assert report["first_year_breaks_alone"] == (sum(report["variants"]["fixed_capital"]["set"])/2 < report["thresholds"]["low_bn"])


def test_tables_use_final_first_year_verdict():
    report = json.loads((tables.D / "first_year_item6_oct15.json").read_text())
    conclusions = {r["id"]: r for r in tables.rows(tables.D / "conclusions_oct15.csv")}
    clause = "First-year horizon breaks C1 alone" if report["first_year_breaks_alone"] else "First-year horizon does not break C1 alone"
    assert clause in conclusions["C1"]["break_condition"]
    premise = next(r for r in tables.rows(tables.D / "common_mode_oct15.csv") if r["premise_id"] == "P02")
    assert clause in premise["effect_if_swapped"]


def test_generation_parts_add_to_final_case():
    case = json.loads((tables.CASE / "summary.json").read_text())["v8"]
    records = tables.rows(tables.D / "c6_generation_break_even_oct15.csv")
    for basis, key in (("case_accrual", "band_bn"), ("cash_set", "cash_set_bn")):
        for convention in ("a", "b"):
            selected = [r for r in records if r["case"] == basis and r["convention"] == convention]
            assert {r["generation"] for r in selected} == {"G1", "G2", "G3plus"}
            for i, field in enumerate(("cost_low_end_bn", "cost_high_end_bn")):
                assert sum(float(r[field]) for r in selected) == pytest.approx(case[key][i], abs=2e-4, rel=0)


def test_c8_reports_all_source_mortality_bounds():
    records = tables.rows(tables.D / "c8_comparisons_oct15.csv")
    assert len(records) == 24
    assert {r["case"] for r in records} == {"oct15"}
    assert {(r["mortality_convention"], r["mortality_bound"]) for r in records} == set(tables.MORTALITY_READINGS)
    for row in records:
        assert row["lineage_engine"] == row["comparator_engine"] == "rough"
        assert float(row["lineage_minus_comparator_bn"]) == pytest.approx(
            float(row["lineage_cost_bn"]) - float(row["comparator_cost_bn"]), abs=1e-9, rel=0)
        assert float(row["lineage_minus_comparator_without_item11_bn"]) == pytest.approx(
            float(row["lineage_minus_comparator_bn"]) - float(row["mixed_unit_removal_bn"]), abs=1e-9, rel=0)
        assert row["mixed_unit_asymmetry"]
    conclusions = {r["id"]: r for r in tables.rows(tables.D / "conclusions_oct15.csv")}
    assert "matched local-white reading GAP" in conclusions["C8"]["status_on_v8"]
    assert all(label in conclusions["C8"]["reading_on_v8"] for label in (tables.MIXED_MORTALITY, tables.OWN_MORTALITY))
