/* G2: fail-loud coverage receipt, generation/count closure and interaction proof. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const clone=x=>JSON.parse(JSON.stringify(x)),sum=a=>a.reduce((x,y)=>x+y,0),GENS=["G1","G2","G3plus"];
const FILE=path.join(__dirname,"../coverage_bound_2026_10_14/derived/coverage_bound_oct16.json");
const sha=b=>crypto.createHash("sha256").update(b).digest("hex");
function validateCounts(coverage){
 if(![...GENS,"added"].every(g=>Number.isFinite(coverage.counts_by_generation[g]))||Math.abs(sum(Object.values(coverage.counts_by_generation))-coverage.net_missing_people)>1e-6)throw Error("[BLOCKED] inherited four-part coverage counts absent or unclosed");
 for(const g of GENS)if(!Number.isFinite(coverage.counts_by_generation_folded?.[g])||Math.abs(coverage.counts_by_generation_folded[g]-coverage.counts_by_generation[g]-(g==="G3plus"?coverage.counts_by_generation.added:0))>1e-6)throw Error("[BLOCKED] folded coverage counts differ from declared four parts");
}
function validate(source){
 const checks=[];
 function gate(label,ok){checks.push({check:label,pass:!!ok});if(!ok)throw Error("[BLOCKED] oct16 coverage: "+label);}
 gate("case/key/allocation",source.case==="main_case_2026_10_16"&&source.key==="oct16"&&source.allocation==="personal");
 for(const which of ["set","cash"]){
  const q=source.sets?.[which];gate(which+" present",!!q);
  for(const end of ["low","high"]){
   const z=q.ends?.[end];gate(which+"/"+end+" finite exact generation closure",z&&Number.isFinite(z.total_bn)&&GENS.every(g=>Number.isFinite(z.by_generation_bn?.[g]))&&Math.abs(sum(GENS.map(g=>z.by_generation_bn[g]))-z.total_bn)<1e-9);
   const interaction=q.interactions?.[end];gate(which+"/"+end+" declared coverage delta plus exact interaction",interaction&&Number.isFinite(interaction.item15_x_item20_bn)&&Math.abs(interaction.coverage_change_bn-interaction.declared_sum_bn-interaction.item15_x_item20_bn)<1e-9);
  }
  for(const id of ["native_minor_calibration","coverage_tenure"]){
   const z=q.item_overrides?.[id];gate(which+"/"+id+" present",!!z);
   for(const end of ["low","high"])gate(which+"/"+id+"/"+end+" generation closure",Number.isFinite(z.by_end?.[end]?.total_bn)&&GENS.every(g=>Number.isFinite(z.by_end[end].by_generation_bn?.[g]))&&Math.abs(sum(GENS.map(g=>z.by_end[end].by_generation_bn[g]))-z.by_end[end].total_bn)<1e-9);
   const count=sum(GENS.map(g=>(z.observed_people_change_by_generation?.[g]||0)+(z.coverage_people_change_by_generation?.[g]||0)));
   gate(which+"/"+id+" population closure",Number.isFinite(z.population_change)&&Math.abs(count-z.population_change)<1e-6);
  }
 }
 gate("source receipt nonempty",source.source_sha256&&Object.keys(source.source_sha256).length>=6);
 for(const [relative,expected]of Object.entries(source.source_sha256))gate("principal source "+relative,sha(fs.readFileSync(path.join(__dirname,"..",relative)))===expected);
 return checks;
}
function check(P){
 const bytes=fs.readFileSync(FILE),source=JSON.parse(bytes),checks=validate(source),negative=[];
 const typed=[],transports=[];
 function typedParts(block,which,id,arm){
  if(typeof P?.csvRows!=="function")throw Error("[BLOCKED] existing case CSV reader unavailable");
  const rows=P.csvRows(block.parts_file),choose=scenario=>rows.filter(r=>r.scenario===scenario);
  const selected=choose(block.parts_scenario),subtract=block.subtract_parts_scenario?choose(block.subtract_parts_scenario):[];
  if(!selected.length||(block.subtract_parts_scenario&&!subtract.length))throw Error("[BLOCKED] selected count-part scenario absent "+id+":"+block.parts_scenario);
  for(const end of ["low","high"])for(const g of GENS){
   const value=selected.filter(r=>r.end===end&&r.generation===g).reduce((v,r)=>v+Number(r.change_bn),0)
    -subtract.filter(r=>r.end===end&&r.generation===g).reduce((v,r)=>v+Number(r.change_bn),0);
   if(Math.abs(value-block.by_end[end].by_generation_bn[g])>1e-9)throw Error("[BLOCKED] typed selected count parts do not close "+which+"/"+id+"/"+arm+"/"+end+"/"+g);
  }
  const count=sum(GENS.map(g=>(block.observed_people_change_by_generation?.[g]||0)+(block.coverage_people_change_by_generation?.[g]||0)));
  if(Math.abs(count-block.population_change)>1e-6)throw Error("[BLOCKED] selected count-part population metadata mismatch");
  typed.push({which,id,arm,parts_scenario:block.parts_scenario,subtract_parts_scenario:block.subtract_parts_scenario||null,pass:true});
 }
 for(const which of ["set","cash"]){
  for(const kind of ["missing_set","nonfinite","generation_gap"]){
   const bad={...source,sets:{...source.sets}};
   if(kind==="missing_set")delete bad.sets[which];
   else{
    const original=source.sets[which],low={...original.ends.low,by_generation_bn:{...original.ends.low.by_generation_bn}};
    bad.sets[which]={...original,ends:{...original.ends,low}};
    if(kind==="nonfinite")low.total_bn=NaN;else low.by_generation_bn.G1+=1;
   }
   let stopped=false;try{validate(bad);}catch{stopped=true;}if(!stopped)throw Error("[BLOCKED] coverage negative control passed "+kind);negative.push({which,kind,blocked:true});
  }
 }
 if(P?.COVERAGE_MODE==="repriced")for(const which of ["set","cash"]){
  const api=which==="set"?P:P.CASH,coverage=api.correctionsPayload().meta.coverage;
  if(coverage.sha256!==sha(bytes)||coverage.key!=="oct16")throw Error("[BLOCKED] package coverage source mismatch");
  validateCounts(coverage);
  for(const kind of ["missing_added_count","wrong_folded_count"]){
   const bad={...coverage,counts_by_generation:{...coverage.counts_by_generation},counts_by_generation_folded:{...coverage.counts_by_generation_folded}};
   if(kind==="missing_added_count")delete bad.counts_by_generation.added;else bad.counts_by_generation_folded.G3plus+=1;
   let stopped=false;try{validateCounts(bad);}catch{stopped=true;}if(!stopped)throw Error("[BLOCKED] inherited count regression accepted "+kind);negative.push({which,kind,blocked:true});
  }
 }
 if(P)for(const which of ["set","cash"]){
  const api=which==="set"?P:P.CASH,built=api.V9_BUILT;
  if(!built)throw Error("[BLOCKED] source registry builds unavailable for count-part regression");
  for(const arm of [null,"count_transfer"]){
   const pieces=built.map(b=>b.item.id==="coverage_tenure"?{...b,arm,x:P.R5_COUNT.build17({selectedItems:P.CANDIDATE},arm,which)}:b);
   const meta=Object.assign({},...pieces.map(b=>b.x.meta||{})),delta=(meta.coverage_tenure.population_change||0)-(api.POST_ENGINE.coverage_tenure.population_change||0);
   const population={...api.POPULATION_V9,with_coverage:api.POPULATION_V9.with_coverage+delta};
   const got=require("./coverage_integration.cjs").apply({base:api.V9_BASE,built:pieces,which,meta,population,selectedItems:P.CANDIDATE});
   if(Object.hasOwn(got.meta,"v9_arm_transport")||Object.hasOwn(got.coverageOverride,"arm_transport"))throw Error("[BLOCKED] default source arms acquired an unnecessary carry label");
   if(arm==="count_transfer"&&got.meta.coverage_tenure.parts_scenario!=="joint_count_transfer")throw Error("[BLOCKED] count-transfer arm silently selects central typed parts");
   for(const id of ["native_minor_calibration","coverage_tenure"])typedParts(got.meta[id],which,id,arm||"fixed_count");
   if(arm==="count_transfer"){
    let stopped=false;try{typedParts({...got.meta.coverage_tenure,parts_scenario:"joint"},which,"coverage_tenure","wrong_fixed_count_selector");}catch{stopped=true;}
    if(!stopped)throw Error("[BLOCKED] wrong count-transfer typed selector was accepted");
    negative.push({which,kind:"wrong_count_parts_scenario",blocked:true});
   }
   for(const g of GENS){const expected=got.coverageOverride.counts_by_generation_folded[g]+got.meta.native_minor_calibration.coverage_people_change_by_generation[g]+got.meta.coverage_tenure.coverage_people_change_by_generation[g];
    if(Math.abs(expected-got.meta.coverage_tenure.coverage_counts_by_generation[g])>1e-6)throw Error("[BLOCKED] count-transfer absolute coverage metadata mismatch");}
  }
  const saved=process.env.V9_ARM_TRANSPORT;
  try{
   const pieces=built.map(b=>b.item.id==="veterans_compensation"?{...b,arm:"unchanged"}:b),meta=Object.assign({},...pieces.map(b=>b.x.meta||{}));
   process.env.V9_ARM_TRANSPORT="carry";
   const got=require("./coverage_integration.cjs").apply({base:api.V9_BASE,built:pieces,which,meta,population:api.POPULATION_V9,selectedItems:P.CANDIDATE});
   const row=got.meta.v9_arm_transport?.by_item?.veterans_compensation;
   if(!row||row.whole_case_unchanged!==false||!got.meta.native_minor_calibration.pricing.includes("CENTRAL/default"))throw Error("[BLOCKED] nondefault source arm silently claims own coverage/count pricing");
   process.env.V9_ARM_TRANSPORT="require_own";
   let stopped=false;try{require("./coverage_integration.cjs").apply({base:api.V9_BASE,built:pieces,which,meta,population:api.POPULATION_V9,selectedItems:P.CANDIDATE});}catch(error){stopped=/own-price item-arm kernel unavailable/.test(error.message);}
   if(!stopped)throw Error("[BLOCKED] require_own accepted an unsupported item-arm kernel");
   transports.push({which,default_metadata_absent:true,nondefault13_carry_labeled:true,require_own_blocks:true});
  }finally{if(saved===undefined)delete process.env.V9_ARM_TRANSPORT;else process.env.V9_ARM_TRANSPORT=saved;}
 }
 require("./memory_guard.cjs").requireWithinBudget("v9 coverage G2");
 return {pass:true,source:"coverage_bound_2026_10_14/derived/coverage_bound_oct16.json",sha256:sha(bytes),stub13:source.stub13,checks,negative_controls:negative,typed_count_parts:typed,arm_transport_controls:transports};
}
module.exports={check,validate};
if(require.main===module){const result=check(require("./package.cjs"));fs.writeFileSync(path.join(__dirname,"derived/coverage_check.json"),JSON.stringify(result,null,2)+"\n");console.log(`coverage G2 PASS ${result.checks.length} checks; ${result.negative_controls.length} negative controls`);}
