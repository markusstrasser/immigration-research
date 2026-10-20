"""Zero calibration must preserve the actual source capacity row and valuation."""
import csv
import json
from pathlib import Path
import importlib.util
import pytest
import sys
import types

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v9_transport_test',HERE/'v9_transport.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def test_pairing_uses_own_transport_despite_foreign_module(monkeypatch):
    spec = importlib.util.spec_from_file_location("social_totals_test", HERE / "v9_totals.py")
    totals = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(totals)
    foreign = types.ModuleType("v9_transport")
    foreign.build_roads = lambda *_: pytest.fail("foreign transport must not run")
    monkeypatch.setitem(sys.modules, "v9_transport", foreign)
    monkeypatch.syspath_prepend(str(m.FISCAL / "world_ledger_2026_09_27"))
    own = totals.load_transport()
    assert Path(own.__file__).resolve() == (HERE / "v9_transport.py").resolve()
    assert own.build_roads is not foreign.build_roads


def test_live_metadata_has_only_live_rate_and_item_registry():
    bands = json.loads((HERE / "derived/oct16/band_variants.json").read_text())
    source = json.loads((m.FISCAL / "main_case_2026_10_16/derived/corrections.json").read_text())["meta"]
    assert bands["package"] == "main_case_2026_10_16/package.cjs"
    assert bands["capital_return"]["rates"] == dict.fromkeys(("low", "high"), source["one_rate"]["flat_real_equivalent"])
    assert bands["selected_items"] == source["v9"]["selected_items"]
    assert bands["items"] == source["v9"]
    assert bands["target_population"] == source["population_v9"]["with_coverage"]
    assert "population_v8" not in bands
    doc = json.loads((HERE / "derived/oct16/real_costs_totals.json").read_text())
    assert doc["target_population_m"] == source["population_v9"]["with_coverage"]/1e6
    for key in ("congestion_by_band_end_bn", "social_items_in_the_social_rows", "beside_the_central_total"):
        assert key not in doc and key in doc["inherited_oct15"]
    assert all("v8 fiscal account" not in r["note"] and "v8 current" not in r["note"]
               for r in csv.DictReader((HERE / "derived/oct16/real_costs_totals.csv").open()))


def test_live_social_frame_consumes_declared_calibration_once():
    spec = importlib.util.spec_from_file_location("social_totals_frame_test", HERE / "v9_totals.py")
    totals = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(totals)
    spec = importlib.util.spec_from_file_location("social_rows_frame_test", HERE / "real_costs_totals.py")
    rows = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rows)
    previous = json.loads((HERE / "derived/oct15/band_variants.json").read_text())
    payload = json.loads((m.FISCAL / "main_case_2026_10_16/derived/corrections.json").read_text())
    result = totals.added_social(previous, payload, rows)
    source = payload["meta"]["population_v9"]
    assert result["native_calibration"]["located_people"] == pytest.approx(source["without_coverage"], abs=.01)
    assert result["people"]["calibrated_complete"] == source["with_coverage"]


@pytest.mark.parametrize('valuation,rate',[('uniform','0'),('VSLY','0'),('VSLY','0.03')])
@pytest.mark.parametrize('arm',['multivehicle_only','all_density'])
def test_zero_key_change_keeps_source_crash_amount(valuation,rate,arm):
    rows=list(csv.DictReader((m.FISCAL/'social_respending_2026_10_14/derived/conditional_stacks.csv').open()))
    source=next(r for r in rows if r['end']=='low' and r['spending_denominator']=='PCE'
                and r['mortality_valuation']==valuation and r['real_discount_rate']==rate
                and r['crash_arm']==arm and r['volunteering_proxy']=='primary_food'
                and r['displacement']=='1.0' and r['market_demand_arm']=='False'
                and r['pm_crash_recipient_boundary']=='lineage_exchangeable')
    old=json.loads((m.FISCAL/'service_response_long_run_2026_09_27/derived/net_change_oct15.json').read_text())
    cut=old['by_band_end']['low']['lane_cut']
    got=m.crash_at_new_capacity(source,{'pairing_by_end':{'low':{'lane_cut':cut,'before_lane_cut':cut}}})
    assert abs(got-float(source['crash_replacement_bn']))<1e-9
