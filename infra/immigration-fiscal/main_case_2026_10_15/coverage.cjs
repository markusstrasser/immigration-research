"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const F=path.join(__dirname,".."), FILE="coverage_bound_2026_10_14/derived/coverage_bound_oct15.json";
const STUB=path.join(__dirname,"_stub/coverage_bound_oct15.json");
const clone=x=>JSON.parse(JSON.stringify(x));
function get(which="set",arm="central") {
 if(!["set","cash"].includes(which))throw Error("[BLOCKED] unknown coverage accounting set");
 const live=fs.existsSync(path.join(F,FILE)),file=live?path.join(F,FILE):STUB;
 if(!fs.existsSync(file)) throw Error("[BLOCKED] coverage input and explicit stub are absent");
 const raw=JSON.parse(fs.readFileSync(file,"utf8"));
 if(live && raw.key!=="oct15") throw Error("[BLOCKED] coverage file is not oct15");
 if(live && which==="cash" && !raw.sets?.cash && !raw.cash) throw Error("[BLOCKED] live coverage file lacks explicit cash prices; set prices cannot silently substitute");
 const q=raw.sets?.[which]||raw[which]||raw;
 if(q.gates!==undefined){const passed=Array.isArray(q.gates)?q.gates.every(g=>g.pass===true):q.gates&&Object.values(q.gates).every(v=>v===true);if(!passed)throw Error("[BLOCKED] coverage source reports a failed gate");}
 const sc=q.scenarios?.[arm]||(arm==="central"?q:null);
 if(!sc) throw Error(`[BLOCKED] coverage arm ${arm} unavailable in ${file}`);
 const counts=clone(sc.implied_net_missing_people||q.implied_net_missing_people||raw.implied_net_missing_people);
 if(!counts) throw Error("[BLOCKED] coverage input lacks people by generation");
 if(!["G1","G2","G3plus"].every(g=>Object.hasOwn(counts,g))||Object.keys(counts).some(g=>!["G1","G2","G3plus","added"].includes(g))) throw Error("[BLOCKED] coverage count keys must be generations only; a total would double-count people");
 const by_end={};
 for(const end of ["low","high"]) {
   const e=sc.ends?.[end]||sc.by_end?.[end];
   const p=e?.by_generation||sc.parts?.[end];
   const total=e?.total_bn??e?.coverage_bn;
   if(!Number.isFinite(total)||!p) throw Error(`[BLOCKED] coverage ${which}/${end} lacks total or generation parts`);
   const gens=Object.fromEntries(["G1","G2","G3plus"].map(g=>[g,typeof p[g]==="number"?p[g]:p[g]?.coverage_bn]));
   if(!Object.values(gens).every(Number.isFinite)||Math.abs(Object.values(gens).reduce((a,b)=>a+b,0)+(p.added?.coverage_bn||0)-total)>1e-9) throw Error("[BLOCKED] coverage generation closure");
   by_end[end]={total_bn:total,by_generation:gens,construction:arm};
   // These are coverage-only source parts, so companions can carry them at
   // central prices without mistaking the source's whole-case total for theirs.
   for(const key of ["decomposition","cps_replicate_se_bn","adult_cost_by_generation_bn","minor_cost_by_generation_bn","adult_minor_uncertainty_rule"])if(e[key]!==undefined)by_end[end][key]=clone(e[key]);
   if(e.case_with_coverage_bn!==undefined)by_end[end].source_case_with_coverage_bn=e.case_with_coverage_bn;
   if(e.decomposition&&(!Number.isFinite(e.decomposition.total_cost_bn)||Math.abs(e.decomposition.total_cost_bn-total)>1e-9))throw Error("[BLOCKED] coverage source decomposition does not close");
 }
 if(!Object.values(counts).every(Number.isFinite)) throw Error("[BLOCKED] coverage count nonfinite");
 return {stub:!live,file:live?FILE:"main_case_2026_10_15/_stub/coverage_bound_oct15.json",sha256:crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex"),which,construction:arm,by_end,counts_by_generation:counts,net_missing_people:Object.values(counts).reduce((a,b)=>a+b,0),cash_rule:live?(q.cash_rule||raw.cash_rule||"source file"):"[STUB] v7 set prices carried to cash until parent supplies cash prices",companion_rule:"carried from central; no own-price coverage rerun",...(raw.base_payload_sha256_by_set?{base_payload_sha256_by_set:clone(raw.base_payload_sha256_by_set)}:{}),...(raw.specifications?{source_specifications:clone(raw.specifications)}:{}),...(raw.case?{source_case:raw.case}:{}),...(raw.production_split?{production_split:raw.production_split}:{}),...(raw.limitations?{source_limitations:clone(raw.limitations)}:{})};
}
module.exports={get,FILE};
