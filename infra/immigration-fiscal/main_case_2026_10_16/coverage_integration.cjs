/* Source-owned coverage adapter. Only the full new registry uses v9 prices;
 * standalone gates retain the declared v8 context. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const clone=x=>JSON.parse(JSON.stringify(x)),sum=a=>a.reduce((x,y)=>x+y,0);
// Item19 has no adopted missing-person increment and is beside the central.
// Coverage/count repricing must not depend on selecting this optional tax arm.
const required=["veterans_compensation","income_security_administration","public_college_response","native_minor_calibration","coverage_tenure","consumption_tax_bases","one_rate"];
function apply({base,built,which,meta,population,selectedItems}){
 if(!required.every(id=>selectedItems.includes(id)))return {meta,population,coverageOverride:null};
 const file=path.join(__dirname,"../coverage_bound_2026_10_14/derived/coverage_bound_oct16.json");
 if(!fs.existsSync(file))throw Error("[BLOCKED] oct16 coverage file missing; build coverage_oct16.py");
 const bytes=fs.readFileSync(file),source=JSON.parse(bytes),root=source.sets[which];
 require("./coverage_check.cjs").validate(source);
 const health=built.find(b=>b.item.id==="health_residual_key"),healthArm=health?(health.arm||"central"):"off";
 let data=healthArm==="central"?root:healthArm==="off"?root.without_item21:root.item21_arm_overrides?.[healthArm];
 if(!data)throw Error("[BLOCKED] own item21 coverage/count arm absent "+healthArm);
 if(healthArm!=="central"){
  const armBytes=fs.readFileSync(path.join(__dirname,"..",data.file));
  if(crypto.createHash("sha256").update(armBytes).digest("hex")!==data.sha256)throw Error("[BLOCKED] item21 arm kernel receipt mismatch "+healthArm);
  data=JSON.parse(armBytes);
 }
 if(source.key!=="oct16"||source.case!=="main_case_2026_10_16"||!data)throw Error("[BLOCKED] oct16 coverage identity");
 const scenario=base.POST_ENGINE.coverage?.construction||"central",q=data.scenarios[scenario];
 if(!q)throw Error("[BLOCKED] oct16 coverage scenario absent "+scenario);
 const old=base.POST_ENGINE.coverage;
 const mode=process.env.V9_ARM_TRANSPORT||"carry";
 if(!["carry","require_own"].includes(mode))throw Error("[BLOCKED] unknown V9_ARM_TRANSPORT");
 const centralArms={veterans_compensation:null,income_security_administration:null,public_college_response:null,consumption_tax_bases:"household_joint"};
 const held=built.filter(b=>Object.hasOwn(centralArms,b.item.id)&&(b.arm||null)!==centralArms[b.item.id]);
 if(held.length&&mode==="require_own")throw Error("[BLOCKED] own-price item-arm kernel unavailable for "+held.map(b=>`${b.item.id}:${b.arm}`).join(", ")+"; V9_ARM_TRANSPORT=carry explicitly carries central coverage/count prices");
 const transport={mode,central_item_arm_prices:true,
  count_kernel_scope:"items16/17 use the central/default source-arm signed-price kernel; nondefault13/14/15/18/21 arms and noncentral lineage/DA options carry those count-item prices",
  by_item:Object.fromEntries(held.map(b=>[b.item.id,{selected_arm:b.arm,central_arm:centralArms[b.item.id],
   observed_channels:"selected source arm on observed engine and completion amounts",
   coverage_channels:"central/default-arm item12 prices carried; not own prices for this selected item arm",
   count_channels:"central/default-arm item16/17 kernel carried",
   central_item12_source_delta_bn:Object.fromEntries(["low","high"].map(end=>[end,data.declared_item12_deltas_bn[end][b.item.id]])),
   exposure_scope:"central source-price diagnostic only; not a full16/17 interaction bound or selected-arm minus-central estimate",
   whole_case_unchanged:b.item.id==="veterans_compensation"&&b.arm==="unchanged"?false:null}]))};
 const override={...clone(old),file:"coverage_bound_2026_10_14/derived/coverage_bound_oct16.json",
  sha256:crypto.createHash("sha256").update(bytes).digest("hex"),key:"oct16",case:"main_case_2026_10_16",which,
  construction:scenario,by_end:Object.fromEntries(["low","high"].map(end=>[end,{...clone(old.by_end[end]),...clone(q.ends[end])}])),net_missing_people:sum(Object.values(q.implied_net_missing_people)),
  counts_by_generation:clone(q.implied_net_missing_people),
  counts_by_generation_folded:Object.fromEntries(["G1","G2","G3plus"].map(g=>[g,q.implied_net_missing_people[g]+(g==="G3plus"?q.implied_net_missing_people.added:0)])),
  pricing:"own oct16 signed piece prices before item16/17; source declaration deltas and interactions in file",
  stub:source.stub13,interactions:clone(data.interactions)};
 if(!["G1","G2","G3plus","added"].every(g=>Number.isFinite(override.counts_by_generation[g]))||Math.abs(sum(Object.values(override.counts_by_generation))-override.net_missing_people)>1e-6)throw Error("[BLOCKED] inherited four-part coverage counts do not close");
 const changed=clone(meta);
 if(held.length){changed.v9_arm_transport=transport;override.arm_transport=clone(transport);}
 changed.coverage=override;
 const countArm=built.find(b=>b.item.id==="coverage_tenure")?.arm;
 for(const id of ["native_minor_calibration","coverage_tenure"]){
  const replacement=clone(data.item_overrides[id]);
  if(id==="coverage_tenure"&&countArm==="count_transfer"){
   const a=data.count_scenarios.joint_count_transfer,b=data.count_scenarios.item16;
   for(const end of ["low","high"]){
    replacement.by_end[end]={total_bn:a[end].total_bn-b[end].total_bn,by_generation_bn:Object.fromEntries(["G1","G2","G3plus"].map(g=>[g,a[end].by_generation_bn[g]-b[end].by_generation_bn[g]]))};
   }
    replacement.parts_scenario="joint_count_transfer";
   // Source builder owns all count-transfer population metadata.
   for(const key of ["population_change","coverage_people_change_by_generation"])replacement[key]=clone(meta[id][key]);
  }
  changed[id]={...clone(meta[id]),...replacement,which,source_v8_by_end:clone(meta[id].by_end)};
  if(held.length)changed[id].pricing+="; CENTRAL/default source-arm kernel carried under the selected nondefault source arm";
  if(countArm==="count_transfer"){
   const prior=id==="coverage_tenure"?changed.native_minor_calibration.coverage_people_change_by_generation:{};
   changed[id].coverage_counts_by_generation=Object.fromEntries(["G1","G2","G3plus"].map(g=>[g,
    override.counts_by_generation_folded[g]+(prior?.[g]||0)+(changed[id].coverage_people_change_by_generation?.[g]||0)]));
  }
 }
 return {meta:changed,population,coverageOverride:override};
}
module.exports={apply,check:P=>require("./coverage_check.cjs").check(P)};
