"""V9 conservation, count-path and resource-versus-financing regressions."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import subprocess

import pandas as pd
import numpy as np
import pytest

HERE = Path(__file__).resolve().parent


def module():
    spec = importlib.util.spec_from_file_location("backcast_v9_test", HERE / "backcast.py")
    result = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = result
    spec.loader.exec_module(result)
    return result


def test_v9_cached_annual_pin_and_fail_loud_guards(tmp_path, monkeypatch):
    b = module()
    monkeypatch.setattr(b, "HERE", tmp_path)
    out = tmp_path / "derived/oct16"
    out.mkdir(parents=True)
    row = dict(concept="cost", rule="ratio", part="typed", year=2024, value_bn=1.25)
    with pytest.raises(ValueError, match="manifest missing"):
        b.verify_cached_annual(tmp_path)
    with pytest.raises(ValueError, match="duplicate annual parts full key"):
        b.write_cached_annual(pd.DataFrame([row, row]), out)
    b.write_cached_annual(pd.DataFrame([row]), out)
    cached = b.verify_cached_annual(tmp_path)
    assert cached == tmp_path / b.ANNUAL_CACHE
    assert not (out / "case_parts_annual.csv").exists()
    original = cached.read_bytes()
    cached.write_bytes(original.replace(b"1.25", b"1.26"))
    with pytest.raises(ValueError, match="differs from manifest"):
        b.verify_cached_annual(tmp_path)
    cached.unlink()
    with pytest.raises(ValueError, match="cache missing"):
        b.verify_cached_annual(tmp_path)


def test_v9_live_annual_cache_matches_tracked_receipt():
    b = module()
    assert b.verify_cached_annual() == HERE / b.ANNUAL_CACHE


def test_v9_charged_programme_sum_is_hash_seed_invariant():
    code = """
import importlib.util, sys
import pandas as pd
spec=importlib.util.spec_from_file_location('backcast_hash_test', sys.argv[1])
b=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=b
spec.loader.exec_module(b)
ids={'social_security','medicaid_and_chip_other_medical','housing_subsidies',
     'economic_affairs_services','recreation_culture'}
values={'social_security':1000.,'medicaid_and_chip_other_medical':300.,
        'housing_subsidies':.3,'economic_affairs_services':.02,'recreation_culture':.005}
categories=pd.DataFrame({'source_cells':list(values)},index=list(values))
cells={k:pd.Series([v,v/3]) for k,v in values.items()}
print([x.hex() for x in b.ordered_programme_total(cells,categories,ids)])
"""
    outputs = [subprocess.check_output([sys.executable, "-c", code, str(HERE / "backcast.py")],
                                      env={**os.environ, "PYTHONHASHSEED": str(seed)}, text=True)
               for seed in (1, 2, 123)]
    assert len(set(outputs)) == 1


def test_v9_mixed_composites_are_not_federal_tax_indices():
    result = subprocess.run(["node", "-e", """
const bridge=require(process.argv[1]);
const fs=require('fs');
const before=JSON.parse(fs.readFileSync(process.argv[2]));
const data=bridge.retainCompositeMixedParts(JSON.parse(JSON.stringify(before)));
for(const [name,block] of Object.entries(data.concepts)){
 for(const [key,p] of Object.entries(block.v6_parts)){
  if(!['M6_biological_children','D_added_residual'].includes(p.component))continue;
  const old=before.concepts[name].v6_parts[key];
  if(p.rule!=='per_person'||p.side!=='unlocated'||!p.unlocated||p.income_linked||p.path!==old.path||p.population_path!==old.population_path)throw Error(key);
 }
 if(JSON.stringify(block.ends)!==JSON.stringify(before.concepts[name].ends))throw Error('anchor changed');
}
console.log('composite source classes and 2024 anchors preserved');
""", str(HERE / "v9_components.cjs"), str(HERE / "derived/case_components_oct15.json")],
        check=True, capture_output=True, text=True)
    assert "anchors preserved" in result.stdout


def test_v9_typed_components_close_and_only_selected_items_enter():
    data = json.loads((HERE / "derived/case_components_oct16.json").read_text())
    summary = json.loads((HERE.parent / "main_case_2026_10_16/derived/summary.json").read_text())["v9"]
    assert "passthrough_source_tax" not in data["v9_items"]
    assert "health_residual_key" in data["v9_items"]
    assert data["resource_rate"] == pytest.approx(0.020810698764237804, abs=1e-15)
    block = data["concepts"]["net_cost_cbo_informed"]
    for i, end in enumerate(("low", "high")):
        row = block["ends"][end]
        amount = row["base_bn"] + sum(row["additions_bn"].values()) + sum(row["capital_bn"].values()) \
            + sum(row["v5_capital_bn"].values()) + sum(sum(x.values()) for x in row["v6_capital_bn"].values())
        assert abs(amount - summary["band_bn"][i]) < 1e-9
        assert abs(block["v9_gates"][end]["cash"] - summary["cash_set_bn"][i]) < 1e-9
    metadata = block["v6_parts"]
    for item in data["v9_items"]:
        # The selected basket's direct engine receipt change is its typed part;
        # its missed-person change lives in the own coverage kernel only.
        assert any(p["item"] == item for p in metadata.values()), item
    assert any(p["item"] == "coverage_repricing" for p in metadata.values())
    assert all(p.get("contributions") in ("oasdi", "hi") for p in metadata.values() if p["rule"] == "accrual")
    assert all(p.get("component") for p in metadata.values() if p["rule"] == "capital")
    assert any(p["item"] == "one_rate" and p["path"] == "lineage" for p in metadata.values())
    assert any(p["item"] == "health_residual_key" and p["rule"] == "capital"
               and p["component"] == "health_sl" and p["path"] == "lineage" for p in metadata.values())
    for key, p in metadata.items():
        if p["item"] == "health_residual_key" and "source_delta_stock_bn" in p:
            assert p["transport_rate_real"] == data["resource_rate"]
            # Metadata is finalized at the high end; the bridge checks each
            # method/end before aggregation, including its own low-end stock.
            assert block["ends"]["high"]["additions_bn"][key] == pytest.approx(p["source_delta_stock_bn"] * data["resource_rate"], abs=1e-9)
    for p in metadata.values():
        if p["line"] == "lane_constants":
            assert p["rule"] == "per_person"
        if p.get("component") in ("M6_biological_children", "D_added_residual"):
            assert p["rule"] == "per_person" and p["unlocated"] and p["side"] == "unlocated"


def test_v9_calibrated_count_changes_follow_their_component_paths(tmp_path, monkeypatch):
    b = module()
    lane = tmp_path / b.OCT16_LANE / "derived"
    lane.mkdir(parents=True)
    summary = dict(v5=dict(lineage=dict(counts=dict(account_union=8e6, added=2e6, lineage_population=10e6))),
                   v9=dict(population=dict(with_coverage=12.7e6), per_member_usd=dict(set=[10000., 20000.])))
    meta = dict(union_completion=dict(counts=dict(reporters=1e6, nonreporters=1e6)),
                coverage=dict(counts_by_generation=dict(G1=.2e6, G2=.4e6, G3plus=.4e6, added=0.),
                              counts_by_generation_folded=dict(G1=.2e6, G2=.4e6, G3plus=.4e6)),
                native_minor_calibration=dict(observed_people_change_by_generation=dict(G1=0., G2=-.1e6, G3plus=-.2e6)),
                coverage_tenure=dict(observed_people_change_by_generation=dict(G1=0., G2=0., G3plus=0.)),
                population_v9=dict(with_coverage=12.7e6))
    (lane / "summary.json").write_text(json.dumps(summary))
    (lane / "corrections.json").write_text(json.dumps(dict(meta=meta)))
    monkeypatch.setattr(b, "FISCAL", tmp_path)
    annual = pd.DataFrame(dict(group_millions=[.5, 1.], g3plus_millions_cps=[.2, 1.]), index=[2010, 2024])
    for i, name in enumerate(b.PER_LINEAGE_MEMBER["oct16"]):
        for rule in ("ratio", "income"):
            annual[f"{name}__{rule}"] = [50., 127. * (i + 1)]
    b.per_lineage_member(annual, "oct16")
    assert annual.loc[2010, "lineage_millions"] == pytest.approx(5.09)
    assert annual.loc[2024, "lineage_millions"] == pytest.approx(12.7)
    meta["population_v9"]["with_coverage"] += 1.
    (lane / "corrections.json").write_text(json.dumps(dict(meta=meta)))
    with pytest.raises(ValueError, match="population_v9 disagree"):
        b.per_lineage_member(annual, "oct16")


def test_new_enterprise_rows_require_unique_archived_national_anchor():
    b = module()
    data = json.loads((HERE / "derived/case_components_oct16.json").read_text())
    assert b.declared_national_anchor(data, "receipt", "enterprise_surplus") == pytest.approx(-7.162)
    assert b.declared_national_anchor(data, "receipt", "housing_enterprise_surplus") == pytest.approx(-45.555811)
    with pytest.raises(ValueError, match="absent or ambiguous"):
        b.declared_national_anchor(data, "receipt", "unknown")
    data["concepts"]["net_cost_cbo_informed"]["v6_parts"]["conflict"] = dict(
        line="enterprise_surplus", side="receipt", national_bn=1.)
    with pytest.raises(ValueError, match="absent or ambiguous"):
        b.declared_national_anchor(data, "receipt", "enterprise_surplus")


def test_repeated_typed_parts_reuse_source_cells_without_aliasing(monkeypatch):
    b = module()
    calls = []
    def source(_book, reference):
        calls.append(reference)
        return pd.Series(10000., index=b.YEARS)
    monkeypatch.setattr(b, "line", source)
    info = dict(line="foo", side="spending", national_bn=None, parent=None, rule="line")
    data = dict(concepts=dict(main=dict(v6_parts=dict(a=info, b=info))))
    categories = pd.DataFrame(dict(source_cells=["T30100-A:1"], national_bn=[10.]), index=["foo"])
    result = b.v4_series(data, None, None, pd.Series(1., index=b.YEARS), categories, {}, "v6")
    assert calls == ["T30100-A:1"]
    assert result["a"].eq(1.).all() and result["b"].eq(1.).all()
    result["a"].iloc[0] = 0.
    assert result["b"].eq(1.).all()


def test_ordered_path_sum_matches_series_sum_and_rejects_misalignment():
    b = module()
    rng = np.random.default_rng(76)
    paths = [pd.Series(row, index=b.YEARS) for row in rng.normal(size=(100, len(b.YEARS)))]
    pd.testing.assert_series_equal(b.sum_paths(paths), sum(paths), check_exact=True)
    original = paths[0].copy()
    combined = b.sum_paths(paths)
    combined.iloc[0] = 100.
    pd.testing.assert_series_equal(paths[0], original, check_exact=True)
    with pytest.raises(ValueError, match="indices differ"):
        b.sum_paths([paths[0], paths[1].iloc[::-1]])


def test_v9_real_yield_sensitivity_changes_both_ends_and_keeps_resource_anchors():
    table = pd.read_csv(HERE / "derived/oct16/round2_annual.csv")
    summary = json.loads((HERE.parent / "main_case_2026_10_16/derived/summary.json").read_text())["v9"]
    for i, end in enumerate(("low", "high")):
        subset = table[table.concept.eq(f"net_cost_cbo_informed_oct16_{end}") & table.rule.eq("ratio")].set_index(["scenario", "year"])
        live = subset.loc[("live_fixed_resource_rates", 2024), "cost_bn"]
        sensitivity = subset.loc[("financing_cost_dfii10_floor0_beside", 2024), "cost_bn"]
        assert abs(live - summary["band_bn"][i]) < 1e-4
        assert abs(sensitivity - live) > 1.


