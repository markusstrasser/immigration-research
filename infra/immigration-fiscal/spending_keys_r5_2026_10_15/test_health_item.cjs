'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const H=require('./health_item.cjs');
const clone=x=>JSON.parse(JSON.stringify(x));
function fixture(){
 const measurement={status:'fixture',rates:{low:.02,high:.03},arms:{}};
 for(const arm of ['central','population','old_key']){
  const sets={};
  for(const which of ['set','cash']){
   const by_end={},by_generation={a:{},b:{}};
   for(const end of ['low','high']){
    const factor=arm==='old_key'?0:(which==='cash'?2:1),rate=measurement.rates[end];
    const parts=[
     {line:'health_services',source_line:'health_services',population:'original_union',generation:'G1',part:'residual',before_bn:10,after_bn:10+factor,delta_bn:factor},
     {line:'health_services',source_line:'health_services',population:'added_lineage',generation:'G3plus',part:'g3_priced',before_bn:2,after_bn:2+factor/2,delta_bn:factor/2},
     {line:'union_completion_health_services',source_line:'health_services',population:'completion',generation:'G3plus',part:'reporter',delta_bn:factor/4},
     {line:'health_services',source_line:'health_services',population:'coverage',generation:'G2',part:'residual',delta_bn:factor/8},
     {line:'health_sl',source_line:'health_sl',population:'original_union',generation:'G1',part:'capital',side:'capital',source_rate:rate,capital_stock_delta_bn:3*factor,before_bn:100*rate,after_bn:103*factor*rate+(factor?0:100*rate),delta_bn:3*factor*rate},
    ];
    parts[4].after_bn=parts[4].before_bn+parts[4].delta_bn;
    by_end[end]={source_rate:rate,parts};by_generation.a[end]={parts:clone(parts)};
    by_generation.b[end]={parts:parts.map(p=>({...p,generation:p.generation==='G1'?'G2':p.generation}))};
   }
   sets[which]={by_end,by_generation,count_interactions:{item16:{low:.1,high:.2}}};
  }
  measurement.arms[arm]={sets};
 }
 const specs=Array.from({length:17},()=>({reading:'high',allocation:'personal',rate:.03}));
 specs[16]={reading:'low',allocation:'personal',rate:.02};
 const api={METHODS:['method_a','method_b'],RATES:measurement.rates,specsFor:()=>clone(specs)};
 return {measurement,api,ctx:{B:{...api,CASH:api}}};
}
test('source population pieces close independently across methods, generations and sets',()=>{
 const {measurement,ctx}=fixture();
 for(const which of ['set','cash']){
  const built=H.buildFromMeasurement(measurement,ctx,null,which),block=built.meta[H.ID];
  assert.equal(built.detail.accounting_set,which);
  for(const end of ['low','high']){
   const q=block.by_end[end];
   assert.deepEqual(Object.keys(q.by_population_bn).sort(),['added_lineage','completion','coverage','original_union']);
   assert.deepEqual(q.by_method.method_a.parts,q.by_method.method_b.parts);
   assert.equal(block.by_generation.a[end].total_bn,block.by_generation.b[end].total_bn);
   assert.equal(Object.values(q.by_generation_bn).reduce((a,b)=>a+b,0),q.total_bn);
  }
  assert.deepEqual(block.count_interactions,{item16:{low:.1,high:.2}});
 }
});
test('live capital rate changes only capital; zero disables capital explicitly',()=>{
 const {measurement,api}=fixture(),m={...measurement,accounting_set:'set'};
 const source=H.deltaParts(21,m,api,{}, {reading:'low',rate:.02},null);
 const next=H.deltaParts(21,m,api,{}, {reading:'low',rate:.02,health_residual_rate:.05},null);
 assert.ok(Math.abs(next[4].delta_bn-.15)<1e-12);assert.equal(next[4].before_bn,5);assert.equal(next[4].after_bn,5.15);
 assert.deepEqual(next.slice(0,4),source.slice(0,4));
 const disabled=H.deltaParts(21,m,api,{}, {reading:'low'},null);
 assert.equal(disabled[4].delta_bn,0);assert.equal(disabled[4].before_bn,0);
});
test('old-key arm is exactly zero at source and alternative rates',()=>{
 const {measurement,ctx,api}=fixture();
 assert.equal(H.buildFromMeasurement(measurement,ctx,'old_key','set').meta[H.ID].low,0);
 for(const rate of [0,.02,.07]){
  const parts=H.deltaParts(21,{...measurement,accounting_set:'cash'},api,{}, {reading:'high',health_residual_rate:rate},'old_key');
  assert.ok(parts.every(p=>p.delta_bn===0));
 }
 measurement.arms.old_key.sets.set.by_end.low.parts[0].delta_bn=.01;
 assert.throws(()=>H.buildFromMeasurement(measurement,ctx,'old_key','set'),/BLOCKED/);
});
test('missing principal declarations fail without method, set, arm or capital fallback',()=>{
 const {measurement,api}=fixture();
 assert.throws(()=>H.deltaParts(21,measurement,api,{}, {reading:'low',rate:.02}),/accounting_set/);
 assert.throws(()=>H.deltaParts(21,{...measurement,accounting_set:'set'},api,{}, {reading:'low',rate:.02},'unknown'),/unknown\/unmeasured/);
 const bad=clone(measurement);delete bad.arms.central.sets.set.by_end.low.parts[4].capital_stock_delta_bn;
 assert.throws(()=>H.deltaParts(21,{...bad,accounting_set:'set'},api,{}, {reading:'low',rate:.02}),/capital part lacks/);
 assert.throws(()=>H.deltaParts(21,{...measurement,accounting_set:'set'},api,{}, {reading:'low',rate:NaN}),/capital rate/);
});
test('generation selection retains independently measured convention b routing',()=>{
 const {measurement,api}=fixture(),m={...measurement,accounting_set:'set'},s={reading:'low',rate:.02};
 assert.ok(H.deltaParts(21,m,api,{},s,null,'G1','a').length>0);
 assert.equal(H.deltaParts(21,m,api,{},s,null,'G1','b').length,0);
 assert.throws(()=>H.deltaParts(21,m,api,{},s,null,'unknown'),/requested generation/);
});
function equipmentRun(){
 const stock=H.equipmentStocks().equipment;
 return {capital:{components:[{id:'eq_health_sl',stock_charged_bn:stock,key:.1,response:1}]},
  evaluation:{spending:[{id:'health_services',key:'health_other',national_bn:300,amount_bn:30,response:1}]}};
}
test('equipment sensitivity adds only selected population stock parts at the live rate',()=>{
 const {measurement,api}=fixture(),m={...measurement,accounting_set:'set'},s={reading:'low',rate:.02,health_residual_rate:.05};
 const source=measurement.arms.central.sets.set.by_end.low.parts,stock=source[4];
 for(const [population,profile,generation]of [
  ['added_lineage','lineage_later_g3','G3plus'],['completion','native_nonreporters','G3plus'],
  ['completion','reporters','G3plus'],['coverage','identified','G2']])source.push({...clone(stock),population,profile,generation});
 const central=H.deltaParts(21,m,api,{capital:{components:[]}},s),next=H.deltaParts(21,m,api,equipmentRun(),s);
 assert.deepEqual(next.filter(p=>!p.equipment_variant),central);
 const eq=next.filter(p=>p.equipment_variant),ratio=H.equipmentStocks().equipment/H.equipmentStocks().structures;
 assert.equal(eq.length,3);assert.ok(eq.every(p=>p.source_line==='eq_health_sl'));
 assert.ok(eq.every(p=>p.delta_bn===3*.05*ratio));
 assert.deepEqual(eq.map(p=>p.population),['original_union','added_lineage','completion']);
 assert.ok(eq.every(p=>p.scope.includes('reporter and coverage held')));
 assert.equal(next.filter(p=>p.equipment_variant&&p.profile==='reporters').length,0);
 const generation=H.deltaParts(21,m,api,equipmentRun(),s,null,'G1');
 assert.equal(generation.filter(p=>p.equipment_variant).length,1);
});
test('equipment old-key control stays zero and wrong key/stock declarations fail',()=>{
 const {measurement,api}=fixture(),m={...measurement,accounting_set:'set'},s={reading:'low',rate:.02};
 const run=equipmentRun(),old=H.deltaParts(21,m,api,run,s,'old_key');
 assert.ok(old.every(p=>p.delta_bn===0));
 const wrongKey=clone(run);wrongKey.evaluation.spending[0].key='population';
 assert.throws(()=>H.deltaParts(21,m,api,wrongKey,s),/selected health_other/);
 const wrongStock=clone(run);wrongStock.capital.components[0].stock_charged_bn+=1;
 assert.throws(()=>H.deltaParts(21,m,api,wrongStock,s),/principal source/);
 const wrongShare=clone(run);wrongShare.capital.components[0].key=.2;
 assert.throws(()=>H.deltaParts(21,m,api,wrongShare,s),/key or response/);
 const declared={...api,correctionsPayload:()=>({meta:{union_completion:{carriers:{eq_reporter:{kind:'capital',parent_line:'eq_health_sl'}}}}})};
 assert.throws(()=>H.deltaParts(21,m,declared,run,s),/carrier absent/);
});
test('v9 reporting baseline is frozen principal rather than the live price-context total',()=>{
 const E=require('./health_evaluate.cjs'),rate=.020810698764237804;
 const pin={schema:1,source_summary:'principal/summary.json',source_summary_sha256:'a'.repeat(64),
  selected_items:['coverage','native_minor_calibration','coverage_tenure','one_rate'],
  fixed_ends:{set:[[16,11],[16,11]],cash:[[16,11],[16,11]]},
  one_rate:{id:'one_rate',arm:'B',flat_real_equivalent:rate},
  sets:{set:{low:344.02328615247666,high:412.55507412763035},cash:{low:260.39059043224427,high:328.922378407397}}};
 const runs={low:[{s:{rate:.02},r:{cost_bn:-123}}],high:[{s:{rate:.03},r:{cost_bn:999}}]};
 const api={POST_ENGINE:{one_rate:pin.one_rate}};
 assert.deepEqual(E.reportingBaseline('v9_base','set',runs,pin,api),pin.sets.set);
 assert.deepEqual(E.reportingBaseline('v9_base','cash',runs,pin,api),pin.sets.cash);
 assert.deepEqual(E.reportingBaseline('standalone_v8','set',runs,pin,api),{low:-123,high:999});
 const stale={POST_ENGINE:{one_rate:{...pin.one_rate,flat_real_equivalent:rate+.001}}};
 assert.throws(()=>E.reportingBaseline('v9_base','set',runs,pin,stale),/differs from frozen principal/);
 const wrong=clone(pin);wrong.selected_items.push(H.ID);
 assert.throws(()=>E.reportingBaseline('v9_base','set',runs,wrong,api),/contains item21/);
});
