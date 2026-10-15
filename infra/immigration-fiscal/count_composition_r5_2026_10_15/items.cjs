/* v9 item adapters. Parent packages these once; this file never builds v9. */
"use strict";
const fs=require("fs"),path=require("path");
const clone=x=>JSON.parse(JSON.stringify(x));
function values(which){
  if(!["set","cash"].includes(which))throw Error("[BLOCKED] unknown accounting set");
  return JSON.parse(fs.readFileSync(path.join(__dirname,"derived/items.json"),"utf8")).sets[which];
}
function difference(a,b){
  const out={};
  for(const end of ["low","high"]){
    const aa=a.by_end[end],bb=b?.by_end[end];
    out[end]={total_bn:aa.total_bn-(bb?.total_bn||0),by_generation_bn:{}};
    for(const g of ["G1","G2","G3plus"])out[end].by_generation_bn[g]=aa.by_generation_bn[g]-(bb?.by_generation_bn[g]||0);
    if(Math.abs(Object.values(out[end].by_generation_bn).reduce((x,y)=>x+y,0)-out[end].total_bn)>1e-9)throw Error("[BLOCKED] item generation closure");
  }
  return out;
}
function build16(ctx,arm,which="set"){
  if(arm)throw Error("[BLOCKED] item16 arm not declared");
  const d=values(which),r=d.item16;
  return {edits:[],parts:{},meta:{native_minor_calibration:{which,by_end:difference(r),
    observed_people_change_by_generation:clone(r.observed_people_change_by_generation),
    coverage_people_change_by_generation:clone(r.coverage_people_change_by_generation),
    population_change:r.population_change,parts_file:`count_composition_r5_2026_10_15/derived/line_parts_${which}.csv`,parts_scenario:"item16",
    scope:r.scope,status:"conditional survey-weight measurement; parent decides adoption"}}};
}
function build17(ctx,arm,which="set"){
  if(arm&&arm!=="count_transfer")throw Error("[BLOCKED] unknown item17 arm");
  // Registry builders construct all items against the SAME base context.
  // Selection therefore must be explicit; base.meta cannot detect a sibling.
  if(!Array.isArray(ctx.selectedItems))throw Error("[BLOCKED] item17 requires ctx.selectedItems from the parent registry");
  const d=values(which),prior=ctx.selectedItems.includes("native_minor_calibration");
  const scenario=prior?(arm?"joint_count_transfer":"joint"):(arm?"item17_count_transfer":"item17");
  const r=d[scenario],before=prior?d.item16:null;
  return {edits:[],parts:{},meta:{coverage_tenure:{which,by_end:difference(r,before),
    population_change:r.population_change-(before?.population_change||0),
    coverage_people_change_by_generation:Object.fromEntries(["G1","G2","G3plus"].map(g=>[g,r.coverage_people_change_by_generation[g]-(before?.coverage_people_change_by_generation[g]||0)])),
    parts_file:`count_composition_r5_2026_10_15/derived/line_parts_${which}.csv`,parts_scenario:scenario,
    subtract_parts_scenario:prior?"item16":null,conditional_on_item16:!!prior,
    scope:r.scope,status:"conditional tenure transfer; parent decides adoption"}}};
}
const REGISTRY=[
  {id:"native_minor_calibration",kind:"post_engine",label:"ACS native-minor weight calibration",arms:{},build:build16},
  {id:"coverage_tenure",kind:"post_engine",label:"missed-person tenure composition",arms:{count_transfer:{}},build:build17},
];
module.exports={REGISTRY,build16,build17,difference};
