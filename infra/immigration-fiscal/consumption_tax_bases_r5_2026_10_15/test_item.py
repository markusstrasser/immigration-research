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
