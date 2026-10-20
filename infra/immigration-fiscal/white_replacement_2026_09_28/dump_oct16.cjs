// Exact v9 full evaluator; observed-base leaf is the immutable v8 observed union.
// This makes every Mexican-specific change an inspectable full-minus-base overlay.
'use strict';
const fs=require('fs'),path=require('path');
const P=require('../main_case_2026_10_16/package.cjs');
const summary=require('../main_case_2026_10_16/derived/summary.json');
const lanes=[__dirname,path.resolve(__dirname,'../black_comparator_rough_2026_09_28')];
const selection=require('./dump_selection.cjs').selectionFor;
function classifyResources(X,r,s){
 const meta=X.correctionsPayload().meta,parts=[];
 const add=(origin,economic_class,value_bn)=>parts.push({origin,economic_class,value_bn});
 for(const q of meta.coverage?.by_end[s.reading]?.decomposition?.line_parts||[])
  if(['capital_return','production'].includes(q.economic_class))add('coverage',q.economic_class,q.coverage_bn);
 for(const q of r.v9_post_engine.parts.public_college_response||[])
  if(q.kind==='college_capital')add('15','capital_return',q.delta_bn);
 for(const q of r.v9_post_engine.parts.health_residual_key||[])
  if(q.side==='capital'||q.source_side==='capital'||q.economic_class==='capital_return')add('21','capital_return',q.delta_bn);
 if(meta.one_rate.arm!=='B')throw Error('[BLOCKED] comparator typed-resource route supports selected TrusteesB only');
 add('20','capital_return',r.v9_post_engine.amounts.one_rate||0);
 for(const id of ['native_minor_calibration','coverage_tenure']){
  const block=meta[id];if(!block)continue;
  const rows=X.csvRows(block.parts_file);
  for(const [scenario,sign] of [[block.parts_scenario,1],[block.subtract_parts_scenario,-1]])if(scenario)
   for(const q of rows)if(q.scenario===scenario&&q.end===s.reading&&['capital_return','production'].includes(q.economic_class))
    add(id,q.economic_class,sign*Number(q.change_bn));
 }
 return {capital_bn:parts.filter(p=>p.economic_class==='capital_return').reduce((s,p)=>s+p.value_bn,0),
  production_gain_bn:-parts.filter(p=>p.economic_class==='production').reduce((s,p)=>s+p.value_bn,0),parts};
}
for(const [suffix,X,basis] of [['',P,'set'],['_cash',P.CASH,'cash']]){
 const declared=summary.v9.end_specifications[basis];
 if(JSON.stringify(declared[0])!==JSON.stringify(declared[1]))throw Error('[BLOCKED] comparator method ends differ');
 const models=X.METHODS.map(method=>X.modelFor('central',method,X.withCentral({})));
 const full={},base=JSON.parse(fs.readFileSync(path.join(__dirname,`derived/engine_lines_oct15_union${suffix}.json`),'utf8'));
 for(const [i,end] of ['low','high'].entries()){
  const idx=declared[0][i],spec=X.specsFor({})[idx];
  if(spec.allocation!=='personal'||base[end].spec!==idx)throw Error('[BLOCKED] observed baseline end changed; re-export its own specification');
  const out={spec:idx,allocation:spec.allocation,rate:spec.rate,cost_bn:0,capital_bn:0,welfare_bn:0,
   target_population:X.POPULATION_V9.with_coverage,resident_population:0,lines:[],capital:[],post_engine:{},v9_parts:{},v9_classified:{capital_bn:0,production_gain_bn:0,parts:[]}};
  const lines=new Map(),capital=new Map();
  models.forEach(m=>{
   const r=X.evaluateFull(m,spec),ev=r.evaluation,n=models.length;
   out.cost_bn+=r.cost_bn/n;out.capital_bn+=r.capital.total_bn/n;out.welfare_bn+=ev.welfare_bn/n;
   out.resident_population+=m.meta.resident_population/n;
   for(const [k,v] of Object.entries(r.post_engine))out.post_engine[k]=(out.post_engine[k]||0)+v/n;
   for(const [k,v] of Object.entries(r.v9_post_engine.amounts))out.v9_parts[k]=(out.v9_parts[k]||0)+v/n;
   const classified=classifyResources(X,r,spec);
   out.v9_classified.capital_bn+=classified.capital_bn/n;
   out.v9_classified.production_gain_bn+=classified.production_gain_bn/n;
   out.v9_classified.parts.push(...classified.parts.map(q=>({...q,value_bn:q.value_bn/n})));
   for(const side of ['receipts','spending'])for(const l of ev[side]){
    const key=side+'|'+l.id,old=lines.get(key)||{side,id:l.id,...selection(side,l,m),national_bn:0,amount_bn:0,response:0,effect_bn:0};
    for(const k of ['national_bn','amount_bn','response','effect_bn'])old[k]+=l[k]/n;lines.set(key,old);
   }
   for(const [k,v] of Object.entries(ev))if(typeof v==='number'){
    const key='scalar|'+k,old=lines.get(key)||{side:'scalar',id:k,effect_bn:0};old.effect_bn+=v/n;lines.set(key,old);
   }
   for(const c of r.capital.components){const old=capital.get(c.id)||{...c,key:0,return_bn:0};old.key+=c.key/n;old.return_bn+=c.return_bn/n;capital.set(c.id,old);}
  });
  out.lines=[...lines.values()].sort((a,b)=>(a.side+'|'+a.id).localeCompare(b.side+'|'+b.id));out.capital=[...capital.values()];
  const old=new Map(base[end].lines.filter(l=>l.side!=='scalar').map(l=>[l.side+'|'+l.id,l]));
  for(const l of out.lines.filter(l=>l.side!=='scalar')){
   const b=old.get(l.side+'|'+l.id);
   if(!b||Math.abs(b.national_bn-l.national_bn)>1e-10||Math.abs(b.response-l.response)>1e-12)throw Error('[BLOCKED] v9 changes observed-base line schema/response: '+l.id);
  }
  out.post_engine.v9_additions_bn=out.post_engine.total_bn-(out.post_engine.mixed_unit_removal_bn||0)-(out.post_engine.coverage_bn||0);
  full[end]=out;
 }
 for(const lane of lanes){
  fs.writeFileSync(path.join(lane,`derived/engine_lines_oct16${suffix}.json`),JSON.stringify(full,null,1)+'\n');
  fs.writeFileSync(path.join(lane,`derived/engine_lines_oct16_union${suffix}.json`),JSON.stringify(base,null,1)+'\n');
 }
}
require('../main_case_2026_10_16/memory_guard.cjs').requireWithinBudget('v9 comparator dumps');
