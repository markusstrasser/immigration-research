"""Scientific accounting, coverage and failure regressions for the public-land lane.

Run after build.py:
    uv run --no-project python3 -m pytest infra/immigration-fiscal/public_land_2026_10_24/ -q -s
"""
import importlib.util
import json
import math
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"


@pytest.fixture(scope="module")
def summary():
    return json.loads((OUT / "summary.json").read_text())


def test_source_case_contract_closes_full_capital_rate_response():
    c = json.loads((OUT / "case_contract.json").read_text())
    assert c["case_key"] == "oct16" and c["status"] == "adopted"
    assert len(c["rows"]) == 112 and len(c["totals"]) == 4
    assert all(g["pass"] for g in c["checks"])
    for total in c["totals"]:
        assert total["capital_return_bn"] == pytest.approx(total["rate_derivative_bn"], abs=1e-6)
    for r in c["rows"]:
        # A change in a key, stock or response must change the same rate derivative
        # as the case's own full evaluator, rather than a rounded prose split.
        assert r["engine_at_case_rate_bn"] == pytest.approx(
            r["stock_charged_bn"] * r["engine_key"] * r["engine_response"] * c["rate"],abs=1e-9)


def test_one_land_row_per_physical_component_and_fee_offsets():
    contract = json.loads((OUT / "case_contract.json").read_text())
    physical = pd.read_csv(OUT / "case_physical_lines.csv")
    land = pd.read_csv(OUT / "land_by_line.csv")
    expected = {r["physical_line"] for r in contract["rows"]}
    assert len(expected) == 24 and set(land.line) == expected
    assert not land.duplicated(["line","arm","end"]).any()
    for key,g in physical.groupby(["method","end","line"]):
        source = [r for r in contract["rows"] if (r["method"],r["end"],r["physical_line"]) == key]
        assert len(g)==1
        assert g.effective_key_times_response.iloc[0] == pytest.approx(sum(r["effective_key_times_response"] for r in source))
    assert not land.line.str.contains("user_fees").any()
    k12 = physical[physical.line.eq("k12")]
    assert (k12.structures_bn < k12.stock_charged_bn).all()
    assert k12.structures_bn.iloc[0] == pytest.approx(2663.9474667295713)


def test_each_conditional_ratio_finite_and_printed():
    d = pd.read_csv(OUT / "land_by_line.csv")
    assert d.mapped_land_to_structures.map(math.isfinite).all()
    for r in d[d.arm.eq("B")].itertuples():
        print(f"{r.end}/{r.line}: conditional mapped land/structures={r.mapped_land_to_structures:.6f}; {r.national_total_status}")
        assert r.mapped_land_to_structures >= 0
        if r.structures_bn > 0:
            assert r.mapped_land_to_structures == pytest.approx(r.national_mapped_value_bn/r.structures_bn)
        else:
            assert r.line.startswith("ent_other_") and r.national_mapped_value_bn==0


def test_school_input_reproduction_and_case_key_separation(summary):
    source = json.loads((HERE.parent / "school_land_2026_10_24/derived/summary.json").read_text())
    for arm in "ABC":
        reproduced = summary["school_input_reproduction"][arm]
        assert reproduced["reproduced_bn"] == pytest.approx(source["arms"][arm]["annual_charge_bn"]["case_flat_real"]["where_enrolled"],abs=1e-10)
    assert summary["school_input_reproduction"]["B"]["reproduced_bn"] == pytest.approx(2.6051560812631225)
    # $2.61bn is a benchmark on the source's own pupil share, not an adoption
    # license to replace the case's completion/count-adjusted physical key.
    rows = pd.read_csv(OUT / "land_by_line.csv")
    school = rows[rows.line.eq("k12") & rows.arm.eq("B")]
    assert (school.group_mapped_charge_case_bn > 2.6051560812631225).all()


def test_coverage_is_explicit_and_unmatched_not_silently_scaled(summary):
    coverage = pd.read_csv(OUT / "coverage.csv")
    for row in coverage.itertuples():
        print(f"{row.facility_class}: accepted sites={row.accepted_public_sites}, public inventory={row.public_universe}, inventory matches={row.public_universe_matches}, match rate={row.public_universe_match_rate}")
        if row.public_universe > 0:
            assert 0 <= row.public_universe_matches <= row.public_universe
            assert row.public_universe_match_rate == pytest.approx(row.public_universe_matches/row.public_universe)
    assert summary["complete_total_bn"] is None
    assert all(v["complete_total_bn"] is None for v in summary["totals"].values())
    assert "not identified" in summary["status"]
    assert summary["airport"]["acreage_missing"] == summary["airport"]["universe"] - summary["airport"]["acreage_recorded"]


def test_highway_mileage_covers_authoritative_frame_and_widths_ordered(summary):
    closure = pd.read_csv(OUT / "roads_mileage_closure.csv")
    assert len(closure)==714
    assert summary["roads"]["national_mileage_coverage_ratio"] == pytest.approx(1)
    road = pd.read_csv(OUT / "roads_county_acres.csv")
    assert (road.acres_width_low <= road.acres+1e-6).all()
    assert (road.acres <= road.acres_width_high+1e-6).all()
    assert road.loc[~road.bea_account_level.isin(["state_local","federal"]),"case_line"].isna().all()
    # Source rows partition spatial/mainline miles and rural-6/local summaries;
    # source_table is retained so an overlap cannot hide behind national scaling.
    low = road.source_table.str.startswith("HPMS county")
    assert ((road.functional_class[low]==7) | ((road.functional_class[low]==6) & (road.area_type[low]=="rural"))).all()


def test_charge_rates_totals_and_geographic_sensitivity(summary):
    d = pd.read_csv(OUT / "land_by_line.csv")
    for r in d.itertuples():
        assert r.group_mapped_charge_case_bn == pytest.approx(r.national_mapped_value_bn*r.effective_key_times_response*r.where_enrolled_factor*summary["case_rate"],abs=1e-8)
    for (end,arm),g in d.groupby(["end","arm"]):
        s = summary["totals"][end+"_"+arm]
        assert g.group_mapped_charge_case_bn.sum() == pytest.approx(s["mapped_charge_case_bn"])
        assert g.group_mapped_charge_242pct_bn.sum() == pytest.approx(s["mapped_charge_case_bn"]*0.0242/summary["case_rate"])
        assert g.group_mapped_charge_7pct_bn.sum() == pytest.approx(s["mapped_charge_case_bn"]*0.07/summary["case_rate"])
        removed = summary["variants"][end+"_"+arm+"_without_manhattan_sf_dc"]
        assert 0 <= removed <= s["mapped_charge_case_bn"]
    county = pd.read_csv(OUT / "county_concentration.csv")
    assert summary["top10_county_share_B"] == pytest.approx(county.head(10).value_B_bn.sum()/county.value_B_bn.sum())
    assert 0 < summary["top10_county_share_B"] <= 1


def test_empty_or_unlocated_class_preserved_without_source_price_crash():
    spec=importlib.util.spec_from_file_location("public_land_test_valuation", HERE / "valuation.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    records=pd.DataFrame({"record_id":["not-located"],"tract":[None],"acres":[1.0],"site_acres":[1.0]})
    for subset in [records,records.iloc[:0]]:
        priced=mod.price_sites(subset,None,None)
        assert len(priced)==len(subset) and not priced.priced.any()
        assert priced.value_A.isna().all()


def test_outputs_lf_and_no_nonfinite_json():
    for path in OUT.iterdir():
        if path.suffix in [".csv",".json"]:
            assert b"\r\n" not in path.read_bytes(),path.name
        if path.suffix==".json":
            json.loads(path.read_text(),parse_constant=lambda x:pytest.fail(f"nonfinite JSON {path.name}: {x}"))


def load_source_module(name):
    import sys
    if str(HERE) not in sys.path:
        sys.path.insert(0,str(HERE))
    spec=importlib.util.spec_from_file_location("public_land_test_"+name,HERE/(name+".py"))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def test_arcgis_success_http_code_cannot_hide_429_or_truncated_pages():
    acquire=load_source_module("acquire_footprints")
    acquire.validate_arcgis_page({"features":[{},{}]},2)
    with pytest.raises(RuntimeError,match="BLOCKED"):
        acquire.validate_arcgis_page({"error":{"code":429,"message":"large geometry quota"}},2)
    with pytest.raises(RuntimeError,match="BLOCKED"):
        acquire.validate_arcgis_page({"features":[{}]},2)


def test_primary_owner_code_drift_is_blocked():
    road=load_source_module("roads")
    codes={code:label for code,(_,label) in road.OWNER_CODES.items()}
    road.validate_owner_codes(codes)
    changed={**codes,40:"Private instrumentality"}
    with pytest.raises((RuntimeError,ValueError),match="BLOCKED"):
        road.validate_owner_codes(changed)
    with pytest.raises((RuntimeError,ValueError),match="BLOCKED"):
        road.parse_owner_codes("not an ownership code table")


def test_hospital_military_label_does_not_discard_nondefense_va():
    u=load_source_module("universes")
    assert u.hospital_scope("GOVERNMENT - FEDERAL","MILITARY","https://www.va.gov/find-locations/")[0]=="eligible"
    assert u.hospital_scope("GOVERNMENT - FEDERAL","MILITARY","https://tricare.mil/mtf/")[0]=="defense_excluded"
    assert u.hospital_scope("GOVERNMENT - FEDERAL","MILITARY","https://example.org/")[0]=="federal_scope_unresolved"


def test_highway_bea_scope_includes_tribal_and_excludes_defense():
    road=load_source_module("roads")
    assert road.case_line_for(50,"non_toll_or_unreported")=="hwy_sl"
    assert road.case_line_for(70,"non_toll_or_unreported")=="hwy_fed"
    for owner in [72,73,74]:
        assert road.case_line_for(owner,"non_toll_or_unreported")==""


def test_park_geometry_repairs_overlap_and_unmatched_area_disclosed(summary):
    fp=json.loads((OUT/"footprint_sources.json").read_text())
    park=fp["park_tract_split"]
    assert 0<park["union_intersected_acres"]<=park["raw_intersected_acres"]<=park["source_geometry_acres"]
    assert park["overlap_acres_removed"] == pytest.approx(park["raw_intersected_acres"]-park["union_intersected_acres"])
    assert 0<park["matched_sites"]<=park["site_count"]
    assert fp["padus"]["query_count"]==fp["padus"]["count"]
    assert fp["padus"]["zero_buffer_fallback_records"]==len(fp["padus"]["zero_buffer_fallback_details"])
    assert summary["parks"]==park
