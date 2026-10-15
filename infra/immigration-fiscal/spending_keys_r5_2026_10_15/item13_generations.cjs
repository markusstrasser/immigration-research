/* Read the existing v8 generation cells; no new demographic split is inferred.
 * a/b are generation conventions, not the two imputation methods. */
'use strict';
const fs=require('fs'),path=require('path');
const V8=require('../generation_account_2026_09_24/v8_split.cjs');
const GENS=['G1','G2','G3plus'];
const sum=xs=>xs.reduce((a,b)=>a+b,0);
const cache=new WeakMap();
const read=f=>JSON.parse(fs.readFileSync(path.join(__dirname,'../generation_account_2026_09_24/derived',f),'utf8'));
function generationRuns(api){
 if(cache.has(api))return cache.get(api);
 // Cash and set have their own scoped retiree-health and lineage corrections.
 const cash=api===require('../main_case_2026_10_15/package.cjs').CASH;
 const suffix=cash?'_cash':'',stored=read(`generation_corrections_oct15${suffix}.json`);
 const ev=V8.evaluator(api.correctionsPayload(),api),out={};
 for(const conv of ['a','b']){
  out[conv]={};
  for(const end of ['low','high'])out[conv][end]=[];
  for(const g of GENS){
   const model=api.Engine.applyCorrections(read(`model_${conv==='b'?'b_':''}${g}.json`),stored.payloads[conv][g]);
   for(const [end,i] of [['low',16],['high',11]]){
    const s=api.specsFor({allocation:'all'})[i];
    out[conv][end].push({generation:g,s,r:ev.evaluateFull(model,s)});
   }
  }
 }
 cache.set(api,out);return out;
}
function buildGenerations(measurement,api,arm,deltaParts){
 const runs=generationRuns(api),out={};
 for(const conv of ['a','b']){
  out[conv]={};
  for(const end of ['low','high']){
   const parts=runs[conv][end].flatMap(({generation:g,r,s})=>deltaParts(13,measurement,api,r,s,arm,g));
   const by_generation_bn=Object.fromEntries(GENS.map(g=>[g,sum(parts.filter(p=>p.generation===g).map(p=>p.delta_bn))]));
    const by_part=Object.fromEntries(['compensation','extension','va_medical'].map(part=>[part,Object.fromEntries(GENS.map(g=>[g,sum(parts.filter(p=>p.part===part&&p.generation===g).map(p=>p.delta_bn))]))]));
   out[conv][end]={total_bn:sum(Object.values(by_generation_bn)),by_generation_bn,by_part,parts,
    attribution:conv==='a'?'each person in own generation':'existing v8 linked-parent/minor routing',method:'canonical imputation-method mean; method-specific union totals stored separately'};
  }
 }
 return out;
}
module.exports={generationRuns,buildGenerations};
