/* Oct16-only consumer. Preserve all frozen oct15 files and split declarations. */
"use strict";
const fs=require("fs"),path=require("path"),V8=require("./v8_split.cjs");
const {Engine,MODEL,sum}=V8.X,GENS=["G1","G2","G3plus"],clone=x=>JSON.parse(JSON.stringify(x));
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),"utf8"));
const fail=s=>{throw Error("[BLOCKED] oct16 generation: "+s);};
const cache=new Map();
function sourceModels(which,conv){
 const key=which+"|"+conv;if(cache.has(key))return cache.get(key);
 const source=read(`derived/generation_corrections_oct15${which==="cash"?"_cash":""}.json`);
 const L=V8.loadCase(which),ev=V8.evaluator(L.payload,L.api);
 const models=Object.fromEntries(GENS.map(g=>[g,Engine.applyCorrections(read(`derived/${conv==="a"?"model_":"model_b_"}${g}.json`),source.payloads[conv][g])]));
 const out={models,ev,L,source};cache.set(key,out);return out;
}
function generationParts(api,s,convention="a"){
 const p=api.correctionsPayload();
 const which=["native_minor_calibration","coverage_tenure","passthrough_source_tax","one_rate","consumption_tax_bases","veterans_compensation","income_security_administration","public_college_response","health_residual_key"]
  .map(id=>p.meta[id]?.which).find(v=>v==="set"||v==="cash")||"set";
 const src=sourceModels(which,convention),old=src.L.api.payloadModel(),newModels={},evaluations={};
 const es=p.edits.slice(src.L.payload.edits.length);
 const extraPayloads={};
 for(const g of GENS){
  const edits=es.map(e=>{
   const select=(m)=>e.side==="receipt"?m.receipts.lines.find(l=>l.id===e.line)?.cells[e.scenario]:m.spending.lines.find(l=>l.id===e.line)?.keys[e.key];
   const source=select(old),target=select(src.models[g]);
   if(!source||!target)fail("new edit lacks a declared existing source "+e.line);
   const by={};for(const a of ["personal","shared"]){if(source[a].target_bn===0&&e.by[a])fail("zero edit denominator "+e.line);by[a]=source[a].target_bn?e.by[a]*target[a].target_bn/source[a].target_bn:0;}
   return {...clone(e),by};
  });
  extraPayloads[g]={edits};
  newModels[g]=V8.withStep(src.models[g],edits);
  evaluations[g]=src.ev.evaluateFull(newModels[g],s);
 }
 const union=api.payloadModel(),post=api.postFor(union,s,api.MAIN_PROFILE),posts=Object.fromEntries(GENS.map(g=>[g,{}])),rows=[];
 const put=(id,values,row={})=>{if(Math.abs(sum(Object.values(values))-row.delta_bn)>1e-9)fail("new post parts do not close "+id);
  for(const g of GENS)posts[g][id]=(posts[g][id]||0)+values[g];rows.push({id,...row,by_generation_bn:values});};
 function shares(row){
  if(row.generation)return Object.fromEntries(GENS.map(g=>[g,g===row.generation?1:0]));
  const line=row.capital_source_line||row.line;
  const values=Object.fromEntries(GENS.map(g=>{
   const r=evaluations[g];
   const capital=r.capital.components.find(c=>c.id===line);
   const spending=r.evaluation.spending.find(c=>c.id===line);
   const value=(row.kind?.startsWith("college")||row.component==="capital_engine"||row.component==="college_capital_interaction")&&capital?capital.return_bn:spending?spending.amount_bn*spending.response:NaN;
   return [g,value];
  }));
  const total=sum(Object.values(values));if(!Number.isFinite(total)||(total===0&&row.delta_bn!==0))fail("no source generation driver "+line);
  return Object.fromEntries(GENS.map(g=>[g,total?values[g]/total:g==="G3plus"?1:0]));
 }
 for(const [id,total] of Object.entries(post.amounts)){
  if(["native_minor_calibration","coverage_tenure","passthrough_source_tax","consumption_tax_bases"].includes(id)){
   if(total===0)continue;
   const z=p.meta[id].by_end[s.reading],parts=z.by_generation_bn||z.by_generation;
   if(!parts)fail("missing exact declared generation parts "+id);
   const scoped=Object.fromEntries(GENS.map(g=>[g,parts[g]||0]));
   if(parts.added_G3plus)scoped.G3plus+=parts.added_G3plus;
   put(id,scoped,{delta_bn:total,rule:"item's declared generation parts; added_G3plus belongs to G3plus"});continue;
  }
  if(id==="coverage_repricing"){
   const coverage=p.meta.coverage?.by_end[s.reading],previous=src.L.payload.meta.coverage.by_end[s.reading];
   const current=coverage?.by_generation_bn||coverage?.by_generation,prior=previous.by_generation_bn||previous.by_generation;
   if(!current)fail("repriced coverage generation metadata absent");
   put(id,Object.fromEntries(GENS.map(g=>[g,current[g]-prior[g]])),{delta_bn:total,rule:"own-price item12 generation delta"});continue;
  }
  let parts=post.parts[id]||[];
  if(id==="health_residual_key"&&convention==="b"){
   const source=p.meta[id].by_generation.b[s.reading].parts,selected=parts;
   parts=selected.map(row=>{
    if(row.population!=="original_union")return row;
    const q=source.find(q=>q.line===row.line&&q.population===row.population&&q.generation===row.generation&&q.part===row.part);
    if(!q)fail("item21 convention-b source part absent "+row.line+"/"+row.generation);
    const rate=row.effective_capital_rate;
    if(Number.isFinite(q.capital_stock_delta_bn)){
     const before_bn=q.capital_stock_before_bn*rate,delta_bn=q.capital_stock_delta_bn*rate;
     return {...row,...q,effective_capital_rate:rate,before_bn,after_bn:before_bn+delta_bn,delta_bn};
    }
    return {...row,...q};
   });
  }
  if(!parts.length){if(Math.abs(total)>1e-12)fail("undeclared post generation route "+id);continue;}
  for(const row of parts){
   const sh=shares(row);put(id,Object.fromEntries(GENS.map(g=>[g,row.delta_bn*sh[g]])),{...row,rule:"existing source line/capital amount shares at this specification"});
  }
 }
 const old_costs=Object.fromEntries(GENS.map(g=>[g,src.ev.evaluateFull(src.models[g],s).cost_bn]));
 const costs=Object.fromEntries(GENS.map(g=>[g,evaluations[g].cost_bn+sum(Object.values(posts[g]))]));
 const actual=api.evaluateFull(union,s,api.MAIN_PROFILE).cost_bn;
 if(Math.abs(sum(Object.values(costs))-actual)>1e-9)fail(`generation cost closure ${sum(Object.values(costs))-actual}; spec ${s.reading}/${s.allocation}; engine ${sum(GENS.map(g=>evaluations[g].cost_bn))}; old ${sum(Object.values(old_costs))}; post ${post.total_bn}; union ${actual}; edits ${es.length}`);
 return {which,convention,models:newModels,extra_payloads:extraPayloads,evaluations,posts,rows,costs,old_costs,total_bn:actual};
}
module.exports={...V8,GENS,sourceModels,generationParts};
