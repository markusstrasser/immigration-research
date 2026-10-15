/* Independent item21 oracle: unchanged v8 and v9 with item21 excluded, fixed
 * personal specifications 16/11. No main-case outputs or sources are written. */
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const H=require('./health_item.cjs');
const V9_PIN='inputs/item21_v9_base.json';
const sum=a=>a.reduce((x,y)=>x+y,0),mean=a=>sum(a)/a.length;
const fail=s=>{throw Error('[BLOCKED] item21 oracle: '+s);};
const clone=x=>JSON.parse(JSON.stringify(x));
function endpointRuns(api){
 const out={low:[],high:[]},specs=api.specsFor({allocation:'all'});
 for(const method of api.METHODS){
  const m=api.modelFor('central',method,api.withCentral({}));
  for(const [end,i]of [['low',16],['high',11]]){
   const s=specs[i];
   if(s.reading!==end||s.allocation!=='personal')fail('fixed endpoint changed');
   out[end].push({method,s,r:api.evaluateFull(m,s)});
  }
 }
 return out;
}
function rateFor(api,s){
 const b=api.POST_ENGINE?.one_rate;
 if(!b)return s.rate??0;
 if(b.arm==='B'){
  if(!(Number.isFinite(b.flat_real_equivalent)&&b.flat_real_equivalent>=0))fail('principal common rate absent');
  return b.flat_real_equivalent;
 }
 if(b.arm==='capital_7pct')return .07;
 if(b.arm==='both_highrate')return .03;
 if(['A','v8'].includes(b.arm))return s.rate??0;
 fail('unknown one-rate source arm '+b.arm);
}
function validatePinnedV9Base(pin){
 if(pin?.schema!==1||!Array.isArray(pin.selected_items)||pin.selected_items.includes(H.ID)
  ||!['coverage','native_minor_calibration','coverage_tenure','one_rate'].every(id=>pin.selected_items.includes(id)))
  fail('frozen principal v9 identity is absent or contains item21');
 if(!/^[a-f0-9]{64}$/.test(pin.source_summary_sha256||'')||!pin.source_summary)fail('frozen principal summary provenance absent');
 for(const which of ['set','cash']){
  if(!Array.isArray(pin.fixed_ends?.[which])||!pin.fixed_ends[which].length
   ||pin.fixed_ends[which].some(p=>JSON.stringify(p)!=='[16,11]'))fail('frozen principal fixed endpoints changed');
  if(!['low','high'].every(end=>Number.isFinite(pin.sets?.[which]?.[end])))fail('frozen principal totals absent '+which);
 }
 if(!pin.one_rate||pin.one_rate.id!=='one_rate')fail('frozen principal rate declaration absent');
 return pin;
}
function pinnedV9Base(){
 // This is a historical input. A rerun must never reconstruct it from outputs
 // that may already contain item21 or another own-coverage kernel.
 return validatePinnedV9Base(JSON.parse(fs.readFileSync(path.join(__dirname,V9_PIN),'utf8')));
}
function reportingBaseline(name,which,runs,pin,api){
 if(name==='standalone_v8')return Object.fromEntries(['low','high'].map(end=>[end,mean(runs[end].map(q=>q.r.cost_bn))]));
 if(name!=='v9_base')fail('unknown reporting baseline '+name);
 validatePinnedV9Base(pin);
 for(const end of ['low','high'])for(const {s}of runs[end]){
  const principalRate=rateFor({POST_ENGINE:{one_rate:pin.one_rate}},s),liveRate=rateFor(api,s);
  if(Math.abs(principalRate-liveRate)>1e-12)fail('live item21 capital rate differs from frozen principal '+which+'/'+end);
 }
 return clone(pin.sets[which]);
}
function assertHealthMethodInvariant(runs){
 for(const end of ['low','high']){
  const selected=r=>[
   ...r.evaluation.spending.filter(p=>p.id==='health_services'||p.id==='state_price_health_services')
    .map(p=>({id:p.id,key:p.key,amount:p.amount_bn,response:p.response})),
   ...r.capital.components.filter(p=>p.id.includes('health')).map(p=>({id:p.id,key:p.key,amount:p.return_bn,response:p.response})),
  ];
  const rows=runs[end].map(q=>selected(q.r));
  if(rows.some(a=>a.length!==rows[0].length))fail('health method schema differs');
  for(const a of rows.slice(1))for(let i=0;i<a.length;i++){
   if(a[i].id!==rows[0][i].id||typeof a[i].key!==typeof rows[0][i].key)fail('health method source identity differs');
   for(const f of ['amount','response'])if(Math.abs(a[i][f]-rows[0][i][f])>1e-9)fail('health source is not method invariant '+end+'/'+a[i].id+'/'+f);
  }
 }
}
function importCases(){
 const P=require('../main_case_2026_10_15/package.cjs');
 // Importing the API must not first build the default full v9 (which includes
 // item21 and an own-coverage file). The following case explicitly excludes it.
 const previous=process.env.V9_NEW_ITEMS;
 process.env.V9_NEW_ITEMS='0';
 let V9;
 try{V9=require('../main_case_2026_10_16/package.cjs');}
 finally{if(previous===undefined)delete process.env.V9_NEW_ITEMS;else process.env.V9_NEW_ITEMS=previous;}
 const ids=V9.CANDIDATE.filter(id=>id!==H.ID);
 const base=V9.caseOf(V9.OCT05,ids);
 if(base.ITEM_IDS?.includes(H.ID))fail('v9 baseline contains item21');
 return {P,base,V9};
}
function evaluate(options={}){
 const measurement=options.measurement||H.read(),cases=options.cases||importCases();
 const pin=validatePinnedV9Base(options.v9Pin||pinnedV9Base());
 const {P,base}=cases,rows=[],parts=[],payloads={},baseline={},gates=[];
 if(JSON.stringify(base.ITEM_IDS)!==JSON.stringify(pin.selected_items))fail('live price-context selected items differ from frozen principal');
 const stored=JSON.parse(fs.readFileSync(path.join(__dirname,'../main_case_2026_10_15/derived/summary.json'),'utf8')).v8;
 for(const [name,root]of [['standalone_v8',P],['v9_base',base]]){
  baseline[name]={};payloads[name]={};
  for(const which of ['set','cash']){
   const api=which==='cash'?root.CASH:root,runs=endpointRuns(api);
   assertHealthMethodInvariant(runs);
   const before=reportingBaseline(name,which,runs,pin,api);
   baseline[name][which]=before;payloads[name][which]={};
   if(name==='standalone_v8'){
    const expected=which==='set'?stored.band_bn:stored.cash_set_bn;
    for(const [i,end]of ['low','high'].entries())if(Math.abs(before[end]-expected[i])>1e-9)fail('unchanged v8 oracle differs '+which+'/'+end);
   }
   for(const arm of Object.keys(measurement.arms)){
    const built=H.buildFromMeasurement(measurement,{B:root},arm==='central'?null:arm,which);
    const detail=built.detail,by_end={};
    for(const end of ['low','high']){
     const perMethod=runs[end].map(({method,r,s})=>{
      const rate=rateFor(api,s),spec={...s,health_residual_rate:rate};
      const pp=H.deltaParts(21,detail,api,r,spec,arm==='central'?null:arm);
      const summary=H.aggregate(pp);
      return {method,rate,...summary};
     });
     const change=mean(perMethod.map(q=>q.total_bn));
     if(arm==='old_key'&&Math.abs(change)>1e-9)fail('old-key arm changes '+name+'/'+which+'/'+end);
     if(perMethod.some(q=>Math.abs(q.total_bn-change)>1e-9))fail('item21 method invariance lost');
     const summary=H.aggregate(perMethod[0].parts);
     by_end[end]={...summary,by_method:Object.fromEntries(perMethod.map(q=>[q.method,q]))};
     const row={case:name,which,arm,end,specification:end==='low'?16:11,before_bn:before[end],change_bn:change,after_bn:before[end]+change,
      baseline_source:name==='v9_base'?V9_PIN:'verified live v8 principal',
      original_union_bn:summary.by_population_bn.original_union||0,added_lineage_bn:summary.by_population_bn.added_lineage||0,
      completion_bn:summary.by_population_bn.completion||0,coverage_bn:summary.by_population_bn.coverage||0,
      capital_rate:perMethod[0].rate};
     rows.push(row);
     for(const p of summary.parts)parts.push({case:name,which,arm,end,...p});
    }
    payloads[name][which][arm]={by_end,count_interactions:clone(built.meta[H.ID].count_interactions)};
   }
  }
 }
 gates.push({gate:'unchanged v8 canonical source, both accounting sets and 16/11',pass:true});
 gates.push({gate:'health source and item21 are imputation-method invariant',pass:true});
 gates.push({gate:'old-key arm changes no case, set, endpoint or line',pass:true});
 gates.push({gate:'generation and population parts close at every reported endpoint',pass:true});
 gates.push({gate:'v9 before/after uses frozen principal totals; live item21 common rate matches frozen principal',pass:true});
 const sourceNames=['health_item.cjs','health_evaluate.cjs','health_residual.py','health_ratios.py','derived/item21.json',V9_PIN];
 const source_hashes=Object.fromEntries(sourceNames.map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,f))).digest('hex')]));
 return {item:21,id:H.ID,baseline,rows,payloads,parts,gates,source_hashes,
  v9_baseline:{item21_excluded:true,selected_items:clone(pin.selected_items),source:V9_PIN,
   source_summary:pin.source_summary,source_summary_sha256:pin.source_summary_sha256,
   fixed_ends:clone(pin.fixed_ends),one_rate:{id:pin.one_rate.id,arm:pin.one_rate.arm,flat_real_equivalent:pin.one_rate.flat_real_equivalent},
   reporting_totals:'Frozen prior principal v9, with its own coverage/count replacement; never reconstructed on rerun.',
   price_context:'Live case API excluding21 supplies direct item21 price and matching common rate only; its total is not the reporting baseline.',
   scope:'Direct item21 price added to frozen prior principal v9 at fixed16/11; coverage and count interactions remain separately reported. This is not a full optimized-case inclusion/exclusion difference.'},
  limits:['Fixed 16/11 personal endpoints; no fresh endpoint optimization.',
   'Count interactions remain separate from source item21; parent case integration owns their application.',
   'Alternative source arms retain their own measured source population/coverage prices; full v9 arm-specific coverage/count kernels require separate parent outputs.']};
}
function csv(rows){
 if(!rows.length)return '';
 const keys=[...new Set(rows.flatMap(r=>Object.keys(r)))],cell=v=>{
  const s=typeof v==='object'&&v!==null?JSON.stringify(v):String(v??'');
  return /[",\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;
 };
 return [keys,...rows.map(r=>keys.map(k=>r[k]))].map(a=>a.map(cell).join(',')).join('\n')+'\n';
}
function main(){
 const args=process.argv.slice(2);
 if(args.length&&!(args.length===2&&args[0]==='--out-dir'))fail('usage: node health_evaluate.cjs [--out-dir PATH]');
 const result=evaluate();
 if(args.length){
  const out=path.resolve(args[1]);fs.mkdirSync(out,{recursive:true});
  fs.writeFileSync(path.join(out,'item21_case_changes.json'),JSON.stringify(result,null,2)+'\n');
  fs.writeFileSync(path.join(out,'item21_arms.csv'),csv(result.rows));
  fs.writeFileSync(path.join(out,'item21_parts.csv'),csv(result.parts));
 }else process.stdout.write(JSON.stringify(result,null,2)+'\n');
 console.error('PASS item21: unchanged v8, old-key zero, distinct population/generation pieces, live capital rate; both sets at 16/11');
}
if(require.main===module)main();
module.exports={evaluate,endpointRuns,rateFor,validatePinnedV9Base,pinnedV9Base,reportingBaseline,assertHealthMethodInvariant,csv};
