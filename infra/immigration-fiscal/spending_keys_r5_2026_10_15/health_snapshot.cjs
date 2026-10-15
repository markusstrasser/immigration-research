/* Read-only principal v8 prices for item21; output stays in this lane. */
'use strict';
const fs=require('fs'),path=require('path');
const P=require('../main_case_2026_10_15/package.cjs');
const I=require('./items.cjs');
const G=require('./item13_generations.cjs');
const out={population:P.correctionsPayload().meta.population_v8,sets:{}};
const base='generation_account_2026_09_24/derived/';
const read=f=>JSON.parse(fs.readFileSync(path.join(__dirname,'..',base,f),'utf8'));
const cell=m=>m.spending.lines.filter(x=>x.id==='health_services'||x.id==='state_price_health_services');
out.source={models:{},stack:read('stack_by_generation.json').payloads,medical:read('correction_rules.json').rules.medical.health_services,age_detail:{...P.ITEM_DETAIL.added_age_mix,part_models:undefined},age_parts:{},references:{}};
const raw=require('../main_case_2026_10_15/item_union.cjs').optionRates(P,{},true);
out.source.unit_models=raw.unit_models.map(q=>({band:q.band,...Object.fromEntries(['g3','white'].map(k=>[k,Object.fromEntries(['set','cash'].map(w=>[w,cell(q[k][w])]))]))}));
for(const c of ['a','b'])out.source.models[c]=Object.fromEntries(['G1','G2','G3plus'].map(g=>[g,cell(read(`model_${c==='b'?'b_':''}${g}.json`))]));
for(const w of ['set','cash']){
 const gp=read(`generation_corrections_sept29${w==='cash'?'_cash':''}.json`);
 out.source.references[w]={};
 for(const c of ['a','b'])out.source.references[w][c]=Object.fromEntries(['G1','G2','G3plus'].map(g=>[g,cell(P.Engine.applyCorrections(read(`model_${c==='b'?'b_':''}${g}.json`),gp.payloads[c][g]))]));
 out.source.age_parts[w]=Object.fromEntries(Object.entries(P.ITEM_DETAIL.added_age_mix.part_models[w]).map(([k,m])=>[k,cell(m)]));
}
const selected=r=>({cost_bn:r.cost_bn,spending:r.evaluation.spending.filter(q=>q.id.includes('health')),capital:r.capital.components.filter(q=>q.id.includes('health'))});
for(const which of ['set','cash']){
 const api=which==='cash'?P.CASH:P,p=api.correctionsPayload();
 out.sets[which]={payload:p,ends:Object.fromEntries(Object.entries(I.endpointRuns(api)).map(([end,runs])=>[end,runs.map(q=>({method:q.method,s:q.s,...selected(q.r)}))])),generations:{}};
 for(const [conv,ends]of Object.entries(G.generationRuns(api)))out.sets[which].generations[conv]=Object.fromEntries(Object.entries(ends).map(([end,runs])=>[end,runs.map(q=>({generation:q.generation,...selected(q.r)}))]));
}
fs.writeFileSync(path.join(__dirname,'derived/item21_snapshot.json'),JSON.stringify(out,null,2)+'\n');
console.log('item21 v8 price snapshot written');
