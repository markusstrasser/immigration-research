"""Observable item contracts: identity, conservation, source roles and explicit gaps."""
from pathlib import Path
import json
import subprocess

import pandas as pd
import pytest

import assemble

HERE = Path(__file__).resolve().parent


def test_unidentified_central_never_becomes_zero():
    item = json.loads((HERE / "derived/item.json").read_text())
    assert item["central"] is None
    result = subprocess.run(["node", "-e", "const I=require(process.argv[1]);try{I.build({},null,'set');process.exit(2)}catch(e){if(!String(e).includes('central is unidentified'))throw e}",
                             str(HERE / "item.cjs")], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_every_engine_arm_preserves_nationals_and_reporter_carrier_parts():
    code = r"""
const P=require(process.argv[1]),I=require(process.argv[2]);
const input=require(process.argv[3]);
for(const which of ['set','cash'])for(const arm of Object.keys(input.arms)){
 const X=which==='set'?P:P.CASH,m=X.payloadModel(),b=I.build({B:P},arm,which);
 const out=P.Engine.applyCorrections(m,{lines:[],receipt_lines:[],edits:b.edits,meta:m.corrections});
 for(const side of ['receipts','spending'])for(const old of m[side].lines){
   const now=out[side].lines.find(l=>l.id===old.id);
   if(now.national_bn!==old.national_bn)throw Error('national changed');
   for(const key of Object.keys(old.cells||old.keys))for(const a of ['personal','shared']){
    const x=(old.cells||old.keys)[key][a],y=(now.cells||now.keys)[key][a];
    if(Math.abs(x.target_bn+x.other_bn-y.target_bn-y.other_bn)>1e-8)throw Error('cell closure');
   }
 }
 for(const [name,p] of Object.entries(b.parts))for(const a of ['personal','shared'])if(p.by[a]!==b.edits[p.edit].by[a])throw Error('parts');
 const edited=new Set(b.edits.filter(e=>e.side==='spending').map(e=>e.line));
 for(const [id,src] of Object.entries(m.corrections.union_completion.carriers))if(src.side==='receipt'&&Object.hasOwn(input.arms[arm].receipt_ratios,src.parent_line)&&!edited.has(id))throw Error('carrier skipped');
 for(const x of Object.values(b.meta[I.ID].by_end))if(Math.abs(x.total_bn-Object.values(x.by_generation_bn).reduce((a,b)=>a+b,0))>1e-9)throw Error('post generation closure');
 if(arm==='off'&&(b.edits.length||Object.values(b.meta[I.ID].by_end).some(x=>x.total_bn!==0)))throw Error('identity');
}
"""
    result = subprocess.run(["node", "-e", code, str(HERE.parent / "main_case_2026_10_15/package.cjs"),
                             str(HERE / "item.cjs"), str(HERE / "derived/item.json")], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_state_pool_normalization_and_group_denominator():
    # Removing 20% of both groups cannot change incidence; a member-only
    # exemption does. This catches denominator-free subtraction.
    t = pd.DataFrame([{"arm":a,"snap_source":"cps_reported","group":"union_completed","state_fips":1,
                       "group_share_state":v} for a,v in [("full",.2),("same",.2),("member_only",.1)]])
    taxes = pd.Series({1:1.0})
    assert assemble.basket_factor(t,taxes,"same") == 1
    assert assemble.basket_factor(t,taxes,"member_only") == .5
    with pytest.raises(ValueError,match="basket states"):
        assemble.basket_factor(t,pd.Series({2:1.0}),"same")


def test_unmapped_housing_cannot_enter_industry_key_as_zero():
    wages = pd.DataFrame([{"cell":"known","allocation":"personal"}])
    with pytest.raises(ValueError,match="unmapped purchaser"):
        assemble.producer_share([{"kind":"intermediate","key":"HS"}],wages,{})


def test_joint_does_not_grocery_exempt_business_twice():
    item=json.loads((HERE / "derived/item.json").read_text())
    b=item["measurement"]["sales_crosscheck_business_fraction"]
    h=item["measurement"]["basket_factors"]["joint"]
    business=item["arms"]["business_sales_crosscheck"]["receipt_ratios"]["general_sales_tax"]
    joint=item["arms"]["joint_sales_customs_household"]["receipt_ratios"]["general_sales_tax"]
    assert abs(joint-business-(1-b)*(h-1))<1e-12
    assert item["item11"].startswith("held explicitly")
    assert set(item["measurement"]["ce_basket_factors"]) == {"grocery", "snap", "joint"}


def test_evaluation_identity_and_complete_account_delta_closure():
    out=json.loads((HERE / "derived/evaluation.json").read_text())
    assert out["central_delta_bn"] is None
    assert len([r for r in out["records"] if r["arm"]=="off"]) == 4
    for row in out["records"]:
        assert abs(row["delta_bn"]-row["engine_delta_bn"]-row["coverage_delta_bn"])<1e-9
        assert row["item11_delta_bn"] is None
        if row["arm"]=="off":
            assert row["delta_bn"] == 0
        assert row["end_indices"] == ([16,16] if row["end"]=="low" else [11,11])


def test_sales_proxy_uses_item6_business_base_and_preserves_old_diagnostic():
    snapshot = json.loads((HERE / "derived/case_snapshot.json").read_text())
    source = json.loads((HERE.parent / "job_capital_taxes_2026_10_14/derived/item.json").read_text())
    otp = source["other_production_line"]
    base = otp["national_bn"]-sum(otp["residential_parts_bn"].values())-otp["mining_part_bn"]
    for which in ("set", "cash"):
        row = snapshot["baseline"][which]
        target = row["job_production_base"]["target_bn"]
        assert row["job_production_base"]["business_base_bn"] == otp["base_bn"]
        assert row["job_production_share"] == pytest.approx(target/base, abs=1e-12)
        assert row["whole_line_share_superseded"] == target/otp["national_bn"]
        assert row["job_production_share"] > row["whole_line_share_superseded"]
    item = json.loads((HERE / "derived/item.json").read_text())
    assert item["arms"]["whole_line_share_superseded"]["status"] == "SUPERSEDED_DIAGNOSTIC"
    assert item["measurement"]["sales_production_share"] == snapshot["baseline"]["set"]["job_production_share"]


def test_mining_assumptions_keep_customs_fixed_and_response_zero():
    item = json.loads((HERE / "derived/item.json").read_text())
    result = json.loads((HERE / "derived/evaluation.json").read_text())
    by_arm = {name: [r for r in result["records"] if r["arm"] == name] for name in item["arms"]}
    customs = item["arms"]["business_customs_carried"]["receipt_ratios"]["customs_duties"]
    for percent in (5, 8):
        assumption = item["measurement"]["sales_mining_assumptions"][str(percent)]
        assert assumption["mining_response"] == 0
        assert assumption["taxable_business_purchase_fraction"] == percent/100
        name = "business_sales_mining_"+str(percent)
        assert item["arms"][name]["label"].startswith("[ASSUMPTION]")
        assert item["arms"][name+"_customs"]["receipt_ratios"]["customs_duties"] == customs
        for sales, pair, duty, base in zip(by_arm[name], by_arm[name+"_customs"],
                                           by_arm["business_customs_carried"], by_arm["business_sales_crosscheck"]):
            assert pair["delta_bn"]-sales["delta_bn"] == pytest.approx(duty["delta_bn"], abs=1e-9)
            assert sales["delta_bn"] > base["delta_bn"]


def test_round6_unchanged_household_customs_and_superseded_diagnostic():
    result = json.loads((HERE / "derived/evaluation.json").read_text())
    item = json.loads((HERE / "derived/item.json").read_text())
    assert len(result["records"]) == 4*len(item["arms"])
    assert result["evaluation_coverage"]["runs_per_arm"] == 128
    expected = {"household_joint": 0.263314888, "whole_line_share_superseded": 12.291257388,
                "business_customs_carried": -0.233461615, "business_customs_final_zero": 0.938013542,
                "business_customs_final_one": -12.125218779}
    for row in result["records"]:
        if row["arm"] in expected:
            assert row["delta_bn"] == pytest.approx(expected[row["arm"]], abs=1e-9)
