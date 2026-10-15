/* Item20: a common own-valuation rate, including own-priced coverage/count parts. */
"use strict";
const fs=require("fs"),path=require("path");
const clone=x=>JSON.parse(JSON.stringify(x)),sum=a=>a.reduce((x,y)=>x+y,0);
const source=JSON.parse(fs.readFileSync(path.join(__dirname,"../one_rate_2026_10_15/derived/rates.json"),"utf8"));
const results=JSON.parse(fs.readFileSync(path.join(__dirname,"../one_rate_2026_10_15/derived/results.json"),"utf8"));
const sourceCoverage=JSON.parse(fs.readFileSync(path.join(__dirname,"../coverage_bound_2026_10_14/derived/coverage_bound_oct15.json"),"utf8"));
const RATE=source.trustees_capital.flat_real_equivalent;
const id="one_rate",arms={B:{},A:{},v8:{},both_highrate:{},capital_7pct:{}};
const rateFor=(block,s)=>block.arm==="B"?RATE:block.arm==="both_highrate"?.03:block.arm==="capital_7pct"?.07:s.rate;
const fail=s=>{throw Error("[BLOCKED] one-rate v9: "+s);},cache=new Map();
function countParts(block,end){
 if(!block)return [];
 if(!block.parts_file||!block.parts_scenario)fail("count item has no typed source parts");
 if(!cache.has(block.parts_file)){
  const lines=fs.readFileSync(path.join(__dirname,"..",block.parts_file),"utf8").trimEnd().split("\n").map(s=>s.split(",")),h=lines.shift();
  if(lines.some(r=>r.length!==h.length))fail("count source CSV format changed");
  cache.set(block.parts_file,lines.map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]]))));
 }
 const out=[];
 for(const [scenario,sign]of [[block.parts_scenario,1],[block.subtract_parts_scenario,-1]])if(scenario)
  for(const p of cache.get(block.parts_file))if(p.scenario===scenario&&p.end===end)out.push({...p,delta_cost_bn:sign*Number(p.change_bn)});
 if(Math.abs(sum(out.map(p=>p.delta_cost_bn))-block.by_end[end].total_bn)>1e-8)fail("count source dollar closure");
 return out;
}
// Exactly the source evaluator's per-generation and native/reporter transfer
// rules (one_rate/evaluate.cjs:89-97), applied to new typed source amounts.
function pensionFactor(p,transfer){
 const ss=p.source_line==="social_security";
 if(!ss&&p.source_line!=="medicare")fail("unknown own pension source "+p.source_line);
 if(p.line.startsWith("native_child_"))return ss?transfer.fss:transfer.fpa;
 if(p.line.startsWith("union_completion_"))return ss?transfer.pooledSS:transfer.pooledPA;
 const factor=(ss?transfer.generationSS:transfer.generationPA)[p.generation];
 if(!Number.isFinite(factor))fail("pension generation missing "+p.generation);
 return factor;
}
function pensionRows(api,s,block,coverageOverride,meta){
 if(block.which!=="set"||!["A","both_highrate"].includes(block.arm))return [];
 const label=block.arm==="A"&&s.reading==="low"?"flat_2":"flat_3",transfer=results.transfers[label];
 const evaluate=require("../one_rate_2026_10_15/evaluate.cjs");
 // This source-owned builder also supplies flat3 at the low reading, for which
 // the source's printed both_highrate table intentionally has no separate row.
 const owned=evaluate.pensionChanges(transfer,s.reading,"set"),rows=[],gens=["G1","G2","G3plus"];
 const previous=sourceCoverage.sets.set.scenarios.central.ends[s.reading].decomposition.line_parts;
 for(const [component,delta_bn]of Object.entries(owned)){
  const ss=component.startsWith("oasdi_"),key=ss?"ss":"pa",source_line=ss?"social_security":"medicare";
  if(component.endsWith("_union"))for(const generation of gens)rows.push({component,generation,source_line,delta_bn:transfer.next[key][generation]-transfer.old[key][generation],rule:"source-owned normalized generation pension change"});
  else if(component.endsWith("_item12_coverage")){
   for(const generation of gens){const amount=sum(previous.filter(p=>p.category==="pension_accrual"&&p.source_line===source_line&&p.generation===generation).map(p=>p.coverage_bn*(pensionFactor(p,transfer)-1)));
    rows.push({component,generation,source_line,delta_bn:amount,rule:"source-owned coverage pension change by declared source generation"});}
  }else rows.push({component,delta_bn,generation:"G3plus",source_line,rule:"source-owned pensionChanges original-descendant or item10 part at this reading"});
  const got=sum(rows.filter(p=>p.component===component).map(p=>p.delta_bn));
  if(Math.abs(got-delta_bn)>1e-9)fail("source-owned pension generation closure "+component);
 }
 const current=(coverageOverride||api.POST_ENGINE.coverage)?.by_end[s.reading].decomposition?.line_parts;
 if(current){
  for(const [list,sign,origin]of [[current,1,coverageOverride?"own_coverage":"selected_v8_construction"],[previous,-1,"source_v8_coverage"]])
   for(const p of list)if(p.category==="pension_accrual")rows.push({component:"pension_coverage_price_interaction",line:p.line,source_line:p.source_line,generation:p.generation,origin,
    delta_bn:sign*p.coverage_bn*(pensionFactor(p,transfer)-1),rule:"own coverage minus source-v8 coverage at source generation transfer"});
 }
 for(const key of ["native_minor_calibration","coverage_tenure"])
  for(const p of countParts(meta[key],s.reading))if(p.category==="pension_accrual")rows.push({component:"pension_count_interaction",item:key,line:p.line,source_line:p.source_line,generation:p.generation,
   delta_bn:p.delta_cost_bn*(pensionFactor(p,transfer)-1),rule:"new selected count scenario at source generation transfer; joint-minus16 retained"});
 return rows;
}
function at(api,r,s,block,collegeParts=[],coverageOverride=null,meta={}){
 if(coverageOverride===true)fail("pass the own-coverage block, not a boolean");
 const old=s.rate,rate=rateFor(block,s),ratio=old?rate/old-1:0;
 const carriers=api.correctionsPayload().meta.union_completion?.carriers||{};
 const rows=r.capital.components.map(c=>({component:"capital_engine",line:c.id,delta_bn:c.return_bn*ratio}));
 for(const q of r.evaluation.spending)if(carriers[q.id]?.kind==="capital")rows.push({component:"capital_reporter",line:q.id,delta_bn:q.amount_bn*q.response*ratio});
 if(!coverageOverride){
  for(const q of api.POST_ENGINE.coverage?.by_end[s.reading]?.decomposition?.line_parts||[])if(q.source_side==="capital")rows.push({component:"capital_coverage",line:q.line,generation:q.generation,delta_bn:q.coverage_bn*ratio});
 }else if(old){
  const parts=coverageOverride.by_end[s.reading].decomposition?.line_parts;
  if(!parts)fail("own coverage capital decomposition absent");
  for(const q of parts)if(q.source_side==="capital")rows.push({component:"capital_own_coverage_rate_interaction",line:q.line,source_line:q.source_line,generation:q.generation,
   delta_bn:q.coverage_bn*(rate/RATE-1),rule:"own oct16 coverage priced at defaultB; only capital rate changed; alternative item15 response prices remain carried"});
 }
 for(const q of collegeParts)if(q.kind==="college_capital")rows.push({...q,component:"college_capital_interaction",delta_bn:q.delta_bn*ratio});
 const countBaseRate=coverageOverride?RATE:old;
 if(old&&countBaseRate)for(const key of ["native_minor_calibration","coverage_tenure"])
  for(const p of countParts(meta[key],s.reading))if(p.economic_class==="capital_return")rows.push({component:"capital_count_interaction",item:key,line:p.line,source_line:p.source_line,generation:p.generation,
   delta_bn:p.delta_cost_bn*(rate/countBaseRate-1),rule:coverageOverride?"own count capital priced at defaultB; target rate applied":"source-v8 count capital moved to target rate"});
 rows.push(...pensionRows(api,s,block,coverageOverride,meta));
 if(rows.some(q=>!Number.isFinite(q.delta_bn)))fail("nonfinite rate component");
 return {total_bn:sum(rows.map(x=>x.delta_bn)),parts:rows,rate};
}
function build(ctx,arm="B",which="set"){
 if(!Object.hasOwn(arms,arm))throw Error("[BLOCKED] unknown one-rate arm");
 const api=which==="cash"?ctx.B.CASH:ctx.B;
 const block={id,which,arm,flat_real_equivalent:RATE,by_end:{},source:"one_rate_2026_10_15/derived/rates.json",external_normal_costs:"imported valuations retained; see rate inventory",
  application:"per specification capital, reporter, own coverage and selected count-part revaluation; pension path stays Trustees inB",
  by_end_scope:"source-owned v8 standalone control; current v9 specification amounts require evaluateFull/postFor, including count/coverage and college interactions",
  coverage_arm_rule:"capital rate revalued on own central/DA coverage and selected count parts; alternative item15 response prices remain central carried prices",
  pension_rule:"source-owned pensionChanges plus own-minus-source coverage and selected16/17 typed accrual parts, using source generation/native/reporter transfer factors; imported public pensions/OPEB held"};
 block.pension_lineage_scope="A/3-percent arms retain the source-v8 original-descendant pension transfer at noncentral lineage options; defaultB does not change pension valuation; selected16/17 and the chosen coverage construction are repriced";
 for(const [end,i]of [["low",16],["high",11]]){
  const values=api.METHODS.map(method=>{const m=api.modelFor("central",method,api.withCentral({})),s=api.MAIN_SPECS[i];return at(api,api.evaluateFull(m,s),s,block);});
  block.by_end[end]={total_bn:sum(values.map(v=>v.total_bn))/values.length,by_method:Object.fromEntries(values.map((v,i)=>[api.METHODS[i],v])),parts:clone(values[0].parts)};
 }
 return {edits:[],parts:{},meta:{[id]:block}};
}
module.exports={RATE,source,results,rateFor,at,build,pensionFactor,countParts,registry:{id,kind:"post_engine",label:"one Trustees rate on both legs",arms,build}};
