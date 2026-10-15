"use strict";
const fs=require("fs"),path=require("path"),P=require("../main_case_2026_10_15/package.cjs"),I=require("./items.cjs");
const data=JSON.parse(fs.readFileSync(path.join(__dirname,"derived/items.json"),"utf8"));
const rows=[];
for(const [basis,X] of [["set",P],["cash",P.CASH]]){
  const baseline=[0,0];
  for(const method of P.METHODS){
    const model=X.modelFor("central",method,X.withCentral({}));
    [16,11].forEach((spec,i)=>{baseline[i]+=X.evaluateFull(model,X.MAIN_SPECS[spec]).cost_bn/P.METHODS.length;});
  }
  baseline.forEach((n,i)=>{if(Math.abs(n-data.v8_unchanged[basis][i])>1e-6)throw Error(`[BLOCKED] unchanged v8 ${basis}/${i}: ${n}`);});
  const a=I.build16({B:X},null,basis).meta.native_minor_calibration;
  const b=I.build17({B:X,selectedItems:["coverage_tenure"]},null,basis).meta.coverage_tenure;
  const joint=I.build17({B:X,selectedItems:["native_minor_calibration","coverage_tenure"]},null,basis).meta.coverage_tenure;
  for(const [i,end] of ["low","high"].entries()){
    const delta16=a.by_end[end].total_bn,delta17=b.by_end[end].total_bn;
    const deltaJoint=delta16+joint.by_end[end].total_bn;
    if(Math.abs(deltaJoint-data.sets[basis].joint.by_end[end].total_bn)>1e-9)throw Error("[BLOCKED] joint item interaction");
    for(const [scenario,delta] of [["unchanged",0],["item16",delta16],["item17",delta17],["joint",deltaJoint]]){
      const value=baseline[i]+delta;
      rows.push({basis,end,scenario,baseline_bn:baseline[i],change_bn:delta,result_bn:value});
      console.log(`${basis} ${end} ${scenario}: ${value.toFixed(9)}bn change ${delta.toFixed(9)}bn`);
    }
  }
}
fs.writeFileSync(path.join(__dirname,"derived/evaluation.json"),JSON.stringify({v8_unchanged_gate:true,post_engine_item_closure_1e_9:true,rows},null,2)+"\n");
