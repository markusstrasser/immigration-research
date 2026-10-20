/* One full-source item control per process, reusing only the freshly checked
 * oct16 central export's explicitly unchanged inherited placement scaffold. */
"use strict";
const fs=require("fs"),path=require("path"),X=require("./export_oct16.cjs");
const fail=s=>{throw Error("[BLOCKED] oct16 household control: "+s);};
function selection(P,item){
  const eligible=P.NEW_IDS.filter(id=>P.CANDIDATE.includes(id));
  if(item!=="none"&&!eligible.includes(item))fail("--control-item must be none or a selected central new item: "+eligible.join(", "));
  const inherited=P.OCT15.CANDIDATE,ids=item==="none"?[...inherited]:inherited.concat(item);
  return {api:item==="none"?P.OCT15:P.caseOf(P.OCT05,ids),ids};
}
function validateSnapshot(base,which,allocation){
  if(base.meta.case!=="main_case_2026_10_16"||base.meta.basis!==which||base.meta.allocation!==allocation||base.meta.v9?.control_item!==null)
    fail("a fresh central export for this set/allocation is required before controls");
  for(const key of ["source_payload","source_generation","scaffold_source_payload","scaffold_source_generation","scaffold_export_source","scaffold_bridge_source"]){
    const old=base.meta.v9[key];
    if(!old?.file||!old.sha256||X.signature(old.file,true).sha256!==old.sha256)fail("stale central scaffold source "+key);
  }
  return base;
}
function atomicWrite(destination,data){const temporary=destination+`.tmp-${process.pid}`;try{fs.writeFileSync(temporary,data);fs.renameSync(temporary,destination);}finally{if(fs.existsSync(temporary))fs.unlinkSync(temporary);}}
function run(argv=process.argv.slice(2)){
  require("../scripts/adoption_gate.cjs").requireAdopted("oct16");
  const arg=(name,fallback)=>argv.includes(name)?argv[argv.indexOf(name)+1]:fallback;
  const item=arg("--control-item",null),allocation=arg("--allocation","personal");
  if(!item||!["personal","shared"].includes(allocation))fail("provide --control-item and --allocation personal|shared");
  const P=require("../main_case_2026_10_16/package.cjs"),chosen=selection(P,item);
  const directory=path.join(__dirname,"_cache/oct16",allocation==="shared"?"shared_allocation":"");
  for(const [which,name,api,finalApi]of [["set","lines.json",chosen.api,P],["cash","lines_cash.json",chosen.api.CASH,P.CASH]]){
    const base=validateSnapshot(JSON.parse(fs.readFileSync(path.join(directory,name),"utf8")),which,allocation);
    const out=X.bridge(base,api,allocation,{controlItem:item,finalApi,selectedIds:chosen.ids});
    require("../main_case_2026_10_16/memory_guard.cjs").requireWithinBudget("oct16 household source control "+item+" "+which);
    const destination=path.join(directory,"controls",item,name);
    fs.mkdirSync(path.dirname(destination),{recursive:true});atomicWrite(destination,JSON.stringify(out,null,1)+"\n");
    console.log(`oct16 full-source ${item} ${which}/${allocation}: ${["low","high"].map(e=>out.union[e].v9_target_cost_bn).join(" / ")}bn`);
  }
}
if(require.main===module)run();
module.exports={selection,validateSnapshot,run};
