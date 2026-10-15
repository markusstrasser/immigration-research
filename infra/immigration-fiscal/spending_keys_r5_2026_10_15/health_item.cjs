/* Item 21's source-owned, post-engine adapter. Measurement is rebuilt in this
 * lane; this module never imports or writes a main-case build. */
'use strict';
const fs=require('fs'),path=require('path');
const ID='health_residual_key',NUMBER=21,GENS=['G1','G2','G3plus'];
const SOURCE='spending_keys_r5_2026_10_15/derived/item21.json';
const clone=x=>JSON.parse(JSON.stringify(x));
const sum=xs=>xs.reduce((a,b)=>a+b,0);
const fail=s=>{throw Error('[BLOCKED] item21 adapter: '+s);};
const read=()=>JSON.parse(fs.readFileSync(path.join(__dirname,'derived/item21.json'),'utf8'));
const CAPITAL_SOURCE='capital_return_services_2026_09_27/derived/engine_components.json';
let healthStocks;
function equipmentStocks(){
 if(healthStocks)return healthStocks;
 const source=JSON.parse(fs.readFileSync(path.join(__dirname,'..',CAPITAL_SOURCE),'utf8'));
 const one=(rows,id)=>{
  const found=rows.filter(p=>p.id===id);
  if(found.length!==1||!(found[0].stock_charged_bn>0))fail('principal capital stock missing '+id);
  return found[0].stock_charged_bn;
 };
 healthStocks={structures:one(source.components,'health_sl'),equipment:one(source.variants.equipment_and_software.adds,'eq_health_sl')};
 return healthStocks;
}
function selected(measurement,arm,which,end,convention='a'){
 const name=arm||'central';
 if(!['set','cash'].includes(which))fail('explicit accounting_set required');
 if(!['low','high'].includes(end))fail('unknown reading '+end);
 if(!['a','b'].includes(convention))fail('unknown generation convention '+convention);
 const source=measurement.arms?.[name]?.sets?.[which];
 if(!source)fail('unknown/unmeasured arm or set '+name+'/'+which);
 const generation=source.by_generation?.[convention]?.[end];
 const block=convention==='a'?source.by_end?.[end]:generation;
 const parts=Array.isArray(block)?block:block?.parts;
 if(!Array.isArray(parts))fail('source parts absent '+name+'/'+which+'/'+end+'/'+convention);
 return {name,source,block,parts,generation};
}
function effectiveRate(r,s){
 if(Object.hasOwn(s,'health_residual_rate')){
  if(!Number.isFinite(s.health_residual_rate)||s.health_residual_rate<0)fail('invalid explicit capital rate');
  return s.health_residual_rate;
 }
 if(s.rate===undefined||s.rate===null)return 0;
 if(!Number.isFinite(s.rate)||s.rate<0)fail('invalid specification capital rate');
 return s.rate;
}
function whichOf(measurement,api){
 if(measurement.accounting_set)return measurement.accounting_set;
 if(api?.HEALTH_RESIDUAL_ACCOUNTING_SET)return api.HEALTH_RESIDUAL_ACCOUNTING_SET;
 fail('accounting_set absent; use buildItem detail or an explicit source view');
}
function normalizePart(row,rate,sourceRate,oldKey){
 if(!row||typeof row!=='object'||!row.line||!row.population)fail('part lacks line or population');
 if(!GENS.includes(row.generation))fail('part lacks source generation '+row.line);
 const out=clone(row),base=Object.hasOwn(row,'delta_bn')?row.delta_bn:row.change_bn;
 if(!Number.isFinite(base))fail('nonfinite source delta '+row.line);
 out.delta_bn=base;
 if(Object.hasOwn(row,'capital_stock_delta_bn')){
  if(!Number.isFinite(row.capital_stock_delta_bn))fail('nonfinite capital stock delta '+row.line);
  out.source_delta_bn=base;out.effective_capital_rate=rate;
  out.delta_bn=row.capital_stock_delta_bn*rate;
  if(Object.hasOwn(row,'capital_stock_before_bn'))out.before_bn=row.capital_stock_before_bn*rate;
  else if(Number.isFinite(row.before_bn)){
   const oldRate=row.source_rate??sourceRate;
   if(!(Number.isFinite(oldRate)&&oldRate>0))fail('capital before amount lacks source_rate '+row.line);
   out.before_bn=row.before_bn*rate/oldRate;
  }
  if(Number.isFinite(out.before_bn))out.after_bn=out.before_bn+out.delta_bn;
 }else if(row.side==='capital'||row.source_side==='capital'||row.economic_class==='capital_return'){
  fail('capital part lacks capital_stock_delta_bn '+row.line);
 }
 if(Number.isFinite(out.before_bn)&&Number.isFinite(out.after_bn)
    &&Math.abs(out.after_bn-out.before_bn-out.delta_bn)>1e-9)fail('part before/after closure '+row.line);
 if(oldKey&&(Math.abs(out.delta_bn)>1e-9||Math.abs(row.capital_stock_delta_bn||0)>1e-9))fail('old-key arm changes '+row.line);
 out.change_bn=out.delta_bn;
 return out;
}
function equipmentParts(parts,api,r){
 const selected=(r.capital?.components||[]).filter(p=>p.id==='eq_health_sl');
 if(!selected.length)return [];
 if(selected.length!==1)fail('duplicate equipment capital component');
 const component=selected[0],health=r.evaluation?.spending?.find(p=>p.id==='health_services');
 if(!health||health.key!=='health_other')fail('equipment variant requires selected health_other key');
 const stocks=equipmentStocks(),ratio=stocks.equipment/stocks.structures;
 if(Math.abs(component.stock_charged_bn-stocks.equipment)>1e-9)fail('equipment variant stock differs from principal source');
 if(!(health.national_bn>0)||!Number.isFinite(component.key)||!Number.isFinite(component.response)
    ||Math.abs(component.key-health.amount_bn/health.national_bn)>1e-9||Math.abs(component.response-health.response)>1e-9)
  fail('equipment variant key or response differs from health line');
 const carriers=api.correctionsPayload?.().meta?.union_completion?.carriers||{};
 const eqReporters=Object.entries(carriers).filter(([,p])=>p.kind==='capital'&&p.parent_line==='eq_health_sl');
 const hasReporter=eqReporters.some(([id])=>r.evaluation.spending.some(p=>p.id===id));
 if(eqReporters.length&&!hasReporter)fail('declared health equipment reporter carrier absent from evaluation');
 const selectedParts=parts.filter(p=>p.source_line==='health_sl'&&p.population!=='coverage'
  &&(p.population==='original_union'||p.population==='added_lineage'
    ||(p.population==='completion'&&(p.profile==='native_nonreporters'||(hasReporter&&p.profile==='reporters')))));
 if(!selectedParts.some(p=>p.population==='original_union'))fail('equipment variant lacks source union stock parts');
 return selectedParts.map(p=>{
  if(!Number.isFinite(p.capital_stock_delta_bn))fail('equipment variant source lacks stock delta');
  const out={...clone(p),line:p.line.replace('health_sl','eq_health_sl'),source_line:'eq_health_sl',
   part:'sl_health_equipment_capital',source_component:'health_sl',equipment_variant:true,stock_ratio:ratio,
   capital_source:CAPITAL_SOURCE,
   scope:hasReporter?'equipment sensitivity: union, added lineage, native nonreporters and declared equipment reporter carrier; coverage held'
    :'equipment sensitivity: union, added lineage and native nonreporters only; reporter and coverage held because source has no equipment carrier'};
  for(const field of ['capital_stock_before_bn','capital_stock_delta_bn','donor_before_bn','donor_after_bn','before_bn','after_bn','delta_bn','change_bn','source_delta_bn'])
   if(Number.isFinite(p[field]))out[field]=p[field]*ratio;
  return out;
 });
}
function deltaParts(number,measurement,api,r,s,arm=null,generation=null,convention='a'){
 if(number!==NUMBER)fail('wrong item number');
 const which=whichOf(measurement,api),choice=selected(measurement,arm,which,s.reading,convention);
 const rate=effectiveRate(r,s),sourceRate=choice.block?.source_rate??measurement.rates?.[s.reading]??api.RATES?.[s.reading];
 const parts=choice.parts.map(p=>normalizePart(p,rate,sourceRate,choice.name==='old_key'));
 parts.push(...equipmentParts(parts,api,r));
 if(generation!==null&&!GENS.includes(generation))fail('unknown requested generation '+generation);
 return generation===null?parts:parts.filter(p=>p.generation===generation);
}
function aggregate(parts){
 const total_bn=sum(parts.map(p=>p.delta_bn));
 const group=field=>Object.fromEntries([...new Set(parts.map(p=>p[field]??'unspecified'))].map(value=>[value,sum(parts.filter(p=>(p[field]??'unspecified')===value).map(p=>p.delta_bn))]));
 const by_generation_bn=Object.fromEntries(GENS.map(g=>[g,sum(parts.filter(p=>p.generation===g).map(p=>p.delta_bn))]));
 if(Math.abs(sum(Object.values(by_generation_bn))-total_bn)>1e-9)fail('generation closure');
 return {total_bn,by_generation_bn,by_population_bn:group('population'),by_part_bn:group('part'),parts};
}
function buildFromMeasurement(measurement,ctx,arm=null,which='set'){
 if(!['set','cash'].includes(which))fail('unknown accounting set');
 const api=which==='cash'?ctx.B.CASH:ctx.B;
 if(!api||!Array.isArray(api.METHODS)||!api.METHODS.length)fail('source case methods absent');
 const detail={...clone(measurement),accounting_set:which};
 const by_end={},by_generation={a:{},b:{}},ss=api.specsFor({allocation:'all'});
 for(const [end,i]of [['low',16],['high',11]]){
  const spec=ss[i];
  if(!spec||spec.reading!==end||spec.allocation!=='personal')fail('source endpoint changed '+end);
  const parts=deltaParts(NUMBER,detail,api,{},spec,arm),a=aggregate(parts);
  by_end[end]={...a,by_method:Object.fromEntries(api.METHODS.map(m=>[m,clone(a)])),
   method_rule:'Health key is identical across source imputation methods; source-owned parts repeated exactly.'};
  for(const convention of ['a','b']){
   const rows=deltaParts(NUMBER,detail,api,{},spec,arm,null,convention);
   const g=aggregate(rows);
   if(Math.abs(g.total_bn-a.total_bn)>1e-9)fail('generation convention total differs '+convention+'/'+end);
   by_generation[convention][end]={...g,method:'canonical imputation-method mean; health source parts method invariant'};
  }
 }
 const block={id:ID,number:NUMBER,which,arm:arm||'central',by_end,by_generation,
  low:by_end.low.total_bn,high:by_end.high.total_bn,status:measurement.status,
  application:'post_engine_by_reading; donor-key parts method invariant; capital stock changes take explicit live rate',
  source:SOURCE,coverage_rule:'population=coverage is a separate item12 price piece; parent own-coverage integration replaces it once',
  count_interactions:clone(selected(measurement,arm,which,'low').source.count_interactions||{}),
  transport:measurement.transport||'Source-measured donor-only residual-key replacement; distinct union, added-lineage, completion and coverage pieces.'};
 return {edits:[],parts:{},detail,meta:{[ID]:block},record:{applied_after_engine:true,
  total_bn:{low:block.low,high:block.high},parts_by_line:Object.fromEntries(['low','high'].map(e=>[e,clone(by_end[e].parts)])),adoption:'parent only'}};
}
function buildItem(number,ctx,arm=null,which='set'){
 if(number!==NUMBER)fail('wrong item number');
 return buildFromMeasurement(read(),ctx,arm,which);
}
const registry={id:ID,number:NUMBER,kind:'post_engine',label:'health residual payer key',
 get arms(){return Object.fromEntries(Object.keys(read().arms||{}).filter(x=>x!=='central').map(x=>[x,{label:x.replaceAll('_',' ')}]));},
 build:(ctx,arm,which)=>buildItem(NUMBER,ctx,arm,which)};
module.exports={ID,NUMBER,GENS,SOURCE,read,selected,effectiveRate,normalizePart,equipmentStocks,equipmentParts,aggregate,deltaParts,buildFromMeasurement,buildItem,registry};
