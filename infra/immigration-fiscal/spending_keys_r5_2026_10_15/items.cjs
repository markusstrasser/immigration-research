/* Candidate items only: no main-case build or adoption. Values are post-engine
 * parts by line, with explicit completion and coverage repricing. */
'use strict';
const fs=require('fs'),path=require('path');
const clone=x=>JSON.parse(JSON.stringify(x));
const fail=s=>{throw Error('[BLOCKED] spending keys: '+s);};
const sum=xs=>xs.reduce((a,b)=>a+b,0);
const FILES={13:'item13.json',14:'item14.json',15:'item15.json'};
const IDS={13:'veterans_compensation',14:'income_security_administration',15:'public_college_response'};
const read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,'derived',FILES[n]),'utf8'));

function lineParts(api,r,s,id,generation=null) {
 const p=api.correctionsPayload(),carriers=p.meta.union_completion?.carriers||{};
 const out=[];
 for(const row of r.evaluation.spending) {
  const src=carriers[row.id];
  if(row.id===id || (src?.kind==='line'&&src.side==='spending'&&src.parent_line===id)) {
   if(!Number.isFinite(row.amount_bn*row.response))fail('nonfinite line exposure '+row.id);
   out.push({line:row.id,source_line:id,population:src?'completion':'engine',...(generation?{generation}:{}),key:row.key,national_bn:row.national_bn,amount_bn:row.amount_bn*row.response});
  }
 }
 if(!out.some(x=>x.line===id))fail('source line absent '+id);
 const coverage=p.meta.coverage?.by_end[s.reading]?.decomposition?.line_parts;
 if(p.meta.coverage&&!coverage)fail('coverage lacks typed line decomposition');
 for(const row of coverage||[])if(row.source_side==='spending'&&row.source_line===id&&(!generation||row.generation===generation)) {
  if(!Number.isFinite(row.coverage_bn))fail('nonfinite coverage '+id);
  out.push({line:row.line,source_line:id,population:'coverage',generation:row.generation,key:row.source_key,amount_bn:row.coverage_bn});
 }
 return out;
}

function collegeParts(api,r,s) {
 const p=api.correctionsPayload(),carriers=p.meta.union_completion?.carriers||{};
 const selected=id=>['college','college_user_fees'].includes(id);
 const out=r.capital.components.filter(c=>selected(c.id)).map(c=>({line:c.id,source_line:c.id,population:'engine',amount_bn:c.return_bn}));
 if(out.length!==2)fail('college and fee-offset capital required');
 for(const row of r.evaluation.spending){const src=carriers[row.id];if(src?.kind==='capital'&&selected(src.parent_line))out.push({line:row.id,source_line:src.parent_line,population:'completion',amount_bn:row.amount_bn*row.response});}
 const coverage=p.meta.coverage?.by_end[s.reading]?.decomposition?.line_parts;
 if(p.meta.coverage&&!coverage)fail('coverage lacks typed capital decomposition');
 for(const row of coverage||[])if(row.source_side==='capital'&&selected(row.source_line))out.push({line:row.line,source_line:row.source_line,population:'coverage',generation:row.generation,amount_bn:row.coverage_bn});
 const component=r.capital.components.find(c=>c.id==='college');
 const rate=api.RATES[s.reading],stock=component.stock_charged_bn;
 if(!(stock>0&&rate>0&&out.every(x=>Number.isFinite(x.amount_bn))))fail('invalid college capital source');
 return {parts:out,stock,rate};
}

function deltaParts(number,measurement,api,r,s,arm,generation=null) {
 if(number===13){
   const medicalArm=measurement.extension?.health_bridge.arms[arm];
   const response=arm&&!medicalArm?measurement.arms[arm]:measurement.response;
  if(!Number.isFinite(response))fail('unknown veterans arm '+arm);
  const compensation=lineParts(api,r,s,measurement.line,generation).map(x=>({...x,part:'compensation',before_bn:x.amount_bn,after_bn:x.amount_bn*response,delta_bn:x.amount_bn*(response-1),response}));
  const ext=measurement.extension;
  if(!ext)fail('item13 lacks military-service extension');
  const extension=ext.lines.flatMap(src=>{
   const rows=lineParts(api,r,s,src.line,generation);
   // VA medical consumption is only a national subblock. Preserve civilian
   // OPEB and other federal/state/local consumption, including state prices.
   const parent=r.evaluation.spending.find(x=>x.id===src.line);
   if(parent.key!==src.key)fail('item13 source key changed '+src.line);
    const national=medicalArm?.national_bn??ext.health_bridge.central_national_bn;
    if(src.part==='va_medical'&&(!(national>0)||national>ext.health_bridge.federal_health_consumption))fail('invalid VA medical national mass');
    const fraction=src.fraction===1?1:national/parent.national_bn;
   if(!Number.isFinite(fraction)||fraction<0||fraction>1)fail('invalid item13 service fraction');
   const keep=arm==='unchanged'||arm==='compensation_only'?1:0;
    return rows.map(x=>({...x,part:src.part||'extension',component:src.component,fraction,national_component_bn:src.fraction===1?parent.national_bn:national,
    // before/after refer to this military subblock; the residual never moves.
    before_bn:x.amount_bn*fraction,after_bn:x.amount_bn*fraction*keep,delta_bn:x.amount_bn*fraction*(keep-1),response:keep}));
  });
  return compensation.concat(extension);
 }
 if(number===14){
  const choice=arm?measurement.arms[arm]:measurement.central;
  const ratio=choice?.by_allocation?.[s.allocation]?.share_ratio;
  if(!Number.isFinite(ratio))fail('unknown/unmeasured administration key arm '+arm);
  return lineParts(api,r,s,'income_security_services').map(x=>({...x,before_bn:x.amount_bn,after_bn:x.amount_bn*ratio,delta_bn:x.amount_bn*(ratio-1),key_ratio:ratio}));
 }
 if(number===15){
  const b=arm&&measurement.arms[arm]?measurement.arms[arm]:null;
  if(arm&&!b&&!['capital_expense_mix','capital_key_as_operating','uniform_use_ratio','unchanged'].includes(arm))fail('unknown college arm '+arm);
  const response=arm==='unchanged'?1:(b?.response??measurement.central_response);
  const cr=arm==='capital_expense_mix'?measurement.capital_expense_mix_arm.response:response;
  const c=collegeParts(api,r,s);
  const fee=JSON.parse(fs.readFileSync(path.join(__dirname,'../user_fee_allocation_2026_10_07/derived/fee_lines.json'),'utf8'));
  // Keep the observed union's operating U exact, then retain the pre-existing
  // keys of additions. Their capital key is an explicit proxy for operating use.
  const unionOffset=fee.higher_ed.U_capital-fee.higher_ed.U;
  return c.parts.flatMap(x=>{
   let use=x.amount_bn/(c.stock*c.rate);
   if(arm==='uniform_use_ratio')use*=fee.higher_ed.U/fee.higher_ed.U_capital;
   else if(arm!=='capital_key_as_operating'&&x.population==='engine'&&x.line==='college')use-=unionOffset;
   const operating=use*measurement.national_exposure_bn;
   return [
    {...x,line:'education_services:college_only',capital_source_line:x.line,source_line:'education_services',kind:'college_operating',before_bn:operating,after_bn:operating*response,delta_bn:operating*(response-1),use_share:use,response},
    {...x,kind:'college_capital',before_bn:x.amount_bn,after_bn:x.amount_bn*cr,delta_bn:x.amount_bn*(cr-1),response:cr},
   ];
  });
 }
 fail('unknown item '+number);
}

const cache=new WeakMap();
function endpointRuns(api){
 if(cache.has(api))return cache.get(api);
 const runs=Object.fromEntries(['low','high'].map(end=>[end,[]]));
 for(const method of api.METHODS){
  const m=api.modelFor('central',method,api.withCentral({})),ss=api.specsFor({allocation:'all'});
  for(const [end,i]of [['low',16],['high',11]]){
   const s=ss[i];if(s.reading!==end||s.allocation!=='personal')fail('v8 endpoint changed');
   runs[end].push({method,s,r:api.evaluateFull(m,s)});
  }
 }
 cache.set(api,runs);return runs;
}

function buildItem(number,ctx,arm=null,which='set') {
 if(!['set','cash'].includes(which))fail('unknown accounting set');
 const api=which==='cash'?ctx.B.CASH:ctx.B;
 if(!api)fail('missing case API');
 const measurement=read(number),runs=endpointRuns(api),by_end={},parts={};
 for(const end of ['low','high']){
  const all=runs[end].map(({method,r,s})=>({method,parts:deltaParts(number,measurement,api,r,s,arm)}));
  const totals=all.map(x=>sum(x.parts.map(p=>p.delta_bn)));
  const averaged=all[0].parts.map((part,i)=>{
   if(!all.every(x=>x.parts[i]?.line===part.line&&x.parts[i]?.population===part.population))fail('method part schemas differ');
   const out=clone(part);
   for(const field of ['amount_bn','before_bn','after_bn','delta_bn','use_share'])if(Number.isFinite(part[field]))out[field]=sum(all.map(x=>x.parts[i][field]))/all.length;
   return out;
  });
  by_end[end]={total_bn:sum(totals)/totals.length,parts:averaged,
   by_method:Object.fromEntries(all.map((x,i)=>[x.method,{total_bn:totals[i],parts:x.parts}]))};
  parts[end]=clone(averaged);
 }
 const block={id:IDS[number],number,which,arm:arm||'central',application:'post_engine_by_method_and_reading; total_bn is the canonical method mean',
  by_end,low:by_end.low.total_bn,high:by_end.high.total_bn,status:measurement.status,
  transport:number===15?'Exact original union U plus additions recovered from typed capital keys (operating proxy); fees and Pell held fixed.':number===14?'Measured/declared component key-ratio transported to existing line, completion and coverage prices.':'Existing veterans benefit-dollar key split by VA FY2024 shares.',
  source:'spending_keys_r5_2026_10_15/derived/'+FILES[number]};
 if(number===13){
  block.by_generation=require('./item13_generations.cjs').buildGenerations(measurement,api,arm,deltaParts);
  for(const end of ['low','high']){
   block.by_end[end].by_generation_bn=clone(block.by_generation.a[end].by_generation_bn);
    block.by_end[end].by_part=Object.fromEntries(['compensation','extension','va_medical'].map(part=>[part,sum(block.by_end[end].parts.filter(p=>p.part===part).map(p=>p.delta_bn))]));
   for(const conv of ['a','b']){
    const gen=block.by_generation[conv][end];
    if(Math.abs(gen.total_bn-block.by_end[end].total_bn)>1e-9)fail('item13 generation mean does not close '+conv+'/'+end);
    for(const p of block.by_end[end].parts){
     const selected=gen.parts.filter(q=>q.part===p.part&&q.line===p.line&&q.population===p.population&&(!p.generation||q.generation===p.generation));
     for(const f of ['before_bn','after_bn','delta_bn'])if(Math.abs(sum(selected.map(q=>q[f]))-p[f])>1e-9)fail('item13 generation line closure '+conv+'/'+p.line+'/'+f);
    }
   }
  }
  block.transport='Accepted compensation FY composition plus service-contingent lines at response0; health consumption only its source-bridged VA national subblock. Generation conventions a/b are distinct from imputation methods; generation amounts are canonical method means.';
 }
 return {edits:[],parts:{},meta:{[IDS[number]]:block},detail:measurement,
  record:{applied_after_engine:true,total_bn:{low:block.low,high:block.high},parts_by_line:parts,adoption:'parent only'}};
}
const REGISTRY=[13,14,15].map(number=>({id:IDS[number],kind:'post_engine',number,label:IDS[number].replaceAll('_',' '),
  get arms(){const m=read(number),names=Object.keys(m.arms);if(number===13)names.push(...Object.keys(m.extension.health_bridge.arms));if(number===15)names.push('capital_expense_mix','capital_key_as_operating','uniform_use_ratio','unchanged');return Object.fromEntries(names.map(id=>[id,{label:id.replaceAll('_',' ')}]));},
 build:(ctx,arm,which)=>buildItem(number,ctx,arm,which)}));
function postEngineFor(built,reading,method){
 const block=Object.values(built.meta)[0],end=block.by_end[reading];
 if(!end)fail('unknown reading');
 if(method==='method_mean')return end.total_bn;
 if(!end.by_method[method])fail('explicit source method required');
 return end.by_method[method].total_bn;
}
module.exports={REGISTRY,buildItem,deltaParts,lineParts,collegeParts,endpointRuns,postEngineFor,IDS};
