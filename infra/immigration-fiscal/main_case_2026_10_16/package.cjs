/* Candidate v9: immutable v8 base, source-owned builders, explicit post-engine routing. */
"use strict";
const fs=require("fs"),path=require("path");
const HERE=__dirname,LANE="main_case_2026_10_16",CASE_KEY="oct16";
const DECISION="decisions/2026-10-16-main-case-v9.md",STATUS="adopted",ADOPTED="2026-10-20";
if(STATUS==="adopted"&&!fs.existsSync(path.resolve(HERE,"../../..",DECISION)))throw Error("[BLOCKED] v9: adoption requires decision file");
// The adoption gate uses a separate child, so this projection cannot poison a consumer's module cache.
if(process.env.FISCAL_ADOPTION_ONLY==="1"){
 module.exports={V9:{HERE,LANE,CASE_KEY,DECISION,STATUS,ADOPTED}};
 return;
}
const V8=require("../main_case_2026_10_15/package.cjs");
const USE_CASE_CACHE=process.env.V9_CASE_CACHE!=="0",v8CaseOf=USE_CASE_CACHE?V8.caseOf:require("./v8_uncached.cjs").caseOf;
const V8_RUNTIME_BASE=USE_CASE_CACHE?V8:require("./v8_bounded_runtime.cjs").packageFor();
const SPEND=require("../spending_keys_r5_2026_10_15/items.cjs");
const COUNT_ITEMS=require("../count_composition_r5_2026_10_15/items.cjs");
const BASKET=require("../consumption_tax_bases_r5_2026_10_15/item.cjs");
const PASS=require("../passthrough_source_tax_r5_2026_10_15/item.cjs");
const RATE=require("./item_rate.cjs");
const COVERAGE_MODE=process.env.V9_COVERAGE||"repriced";
const clone=x=>JSON.parse(JSON.stringify(x)),sum=a=>a.reduce((x,y)=>x+y,0);
const PRINCIPAL_LINEAGE=V8.correctionsPayload().meta.lineage;
const meanNumbers=a=>sum(a)/a.length;
const fail=s=>{throw Error("[BLOCKED] v9: "+s);};
if(!["base","repriced"].includes(COVERAGE_MODE))fail("unknown V9_COVERAGE");
if(!["candidate","adopted"].includes(STATUS))fail("unknown V9_STATUS");
const NEW=SPEND.REGISTRY.filter(x=>x.number!==21).concat(COUNT_ITEMS.REGISTRY,[BASKET.registry(),{id:PASS.id,kind:PASS.kind,label:"pass-through source taxes",arms:PASS.arms(),build:PASS.build},RATE.registry],SPEND.REGISTRY.filter(x=>x.number===21));
const NEW_IDS=NEW.map(x=>x.id),REGISTRY=V8.REGISTRY.concat(NEW);
if(NEW_IDS.includes("health_residual_key")){
 const receipt=path.join(HERE,"inputs/item21_ready.json");
 if(!fs.existsSync(receipt))fail("item21 readiness receipt absent; run source_check first");
 const ready=JSON.parse(fs.readFileSync(receipt,"utf8"));
 for(const [relative,expected]of Object.entries(ready.hashes||{}))if(require("crypto").createHash("sha256").update(fs.readFileSync(path.join(HERE,"..",relative))).digest("hex")!==expected)fail("item21 readiness source changed "+relative);
 if(ready.completion_marker!=="ITEM21_READY"||Object.keys(ready.hashes||{}).length!==6)fail("item21 readiness receipt incomplete");
}
const ITEM19=process.env.ITEM19||"0";
if(!["0","1"].includes(ITEM19))fail("ITEM19 must be 0 (beside) or 1 (conditional central)");
const CANDIDATE=V8.CANDIDATE.concat(NEW_IDS.filter(id=>ITEM19==="1"||id!==PASS.id));
require("./readiness.cjs").requireItem13();
const STUB13=process.env.ITEM13_PHASE==="step1";
const ITEM19_ARM=process.env.ITEM19_ARM||"foreign_full_ftc_individual_tangible_normal";
const ITEM18_CARRIER_MODE=process.env.ITEM18_CARRIER_MODE||"source_evaluator";
if(!["source_evaluator","declared_carriers"].includes(ITEM18_CARRIER_MODE))fail("unknown ITEM18_CARRIER_MODE");
const DEFAULT_ARMS={...(STUB13?{veterans_compensation:"compensation_only"}:{}),consumption_tax_bases:"household_joint",passthrough_source_tax:ITEM19_ARM,one_rate:"B"};
const cache=new Map();
const buildCache=new WeakMap();
function withDeclaredCoverageParts(api,which){
 const p=api.correctionsPayload(),c=p.meta.coverage;
 if(!c||["low","high"].every(e=>c.by_end[e].decomposition))return api;
 const canonical=(which==="cash"?V8.CASH:V8).correctionsPayload().meta.coverage;
 const filled=clone(c);
 for(const end of ["low","high"])if(!filled.by_end[end].decomposition)filled.by_end[end].decomposition=clone(canonical.by_end[end].decomposition);
 filled.source_parts_transport="[DEGRADED] source alternative supplies no typed decomposition; canonical source pieces carried for builder only; final oct16 own-price kernel replaces them";
 return {...api,POST_ENGINE:{...api.POST_ENGINE,coverage:filled},correctionsPayload:o=>{const q=api.correctionsPayload(o);q.meta.coverage=clone(filled);return q;}};
}
function layer(base,built,which,identity){
 const p0=base.correctionsPayload(),edits=[],records=[],meta={};
 const builderView=withDeclaredCoverageParts(base,which);
 const sourceP=builderView.correctionsPayload();
 const sourceApi={...builderView,correctionsPayload:()=>sourceP};
 let mm=base.payloadModel();
 for(const {item,arm,x} of built){
  const es=x.editsAt?x.editsAt(mm,{}):x.edits;
  const first=p0.edits.length+edits.length;
  const parts=x.partsAt?x.partsAt(mm,{}):clone(x.parts||{});
  for(const p of Object.values(parts))if(Number.isInteger(p.edit)&&es[p.edit])p.by=clone(es[p.edit].by);
  const record={id:item.id,kind:item.kind,label:item.label,applied:true,arm:arm||null,arms:clone(item.arms||{}),edits:{first,count:es.length},parts,...clone(x.record||{})};
  if(x.meta?.[item.id]?.by_end)record.post_engine_by_end=clone(x.meta[item.id].by_end);
  records.push(record);edits.push(...clone(es));Object.assign(meta,clone(x.meta||{}));
  mm=V8.Engine.applyCorrections(mm,{edits:es,meta:mm.corrections});
 }
 const oldPop=clone(p0.meta.population_v8);
 const countChange=sum(built.map(b=>b.x.meta?.[b.item.id]?.population_change||0));
 const coverageCountChange=sum(built.map(b=>sum(Object.values(b.x.meta?.[b.item.id]?.coverage_people_change_by_generation||{}))));
 let population={...oldPop,without_coverage:oldPop.without_coverage+countChange-coverageCountChange,with_coverage:oldPop.with_coverage+countChange,native_minor_calibration:meta.native_minor_calibration?.population_change||0,tenure:meta.coverage_tenure?.population_change||0};
 let coverageOverride=null;
 if(COVERAGE_MODE==="repriced"&&built.length){
  const integration=require("./coverage_integration.cjs");
  const out=integration.apply({base,built,which,meta,population,selectedItems:identity.ids});
  if(!out||!out.meta||!out.population)fail("invalid coverage integration");
  Object.assign(meta,out.meta);population=out.population;coverageOverride=out.coverageOverride;
 }
 population.coverage=population.with_coverage-population.without_coverage;
 const stamp=identity.stamp;
 const payloadFor=o=>{
  const bp=base.correctionsPayload(o),out=clone(bp),ee=[],rr=clone(records);let m=V8.Engine.applyCorrections(V8.MODEL,bp);
  for(let i=0;i<built.length;i++){
   const x=built[i].x,e=x.editsAt?x.editsAt(m,o||{}):x.edits;
   rr[i].edits={first:bp.edits.length+ee.length,count:e.length};
   if(x.partsAt)rr[i].parts=x.partsAt(m,o||{});
   for(const p of Object.values(rr[i].parts||{}))if(Number.isInteger(p.edit)&&e[p.edit])p.by=clone(e[p.edit].by);
   ee.push(...clone(e));m=V8.Engine.applyCorrections(m,{edits:e,meta:m.corrections});
  }
  out.edits=bp.edits.concat(ee);
  Object.assign(out.meta,clone(meta),{source:LANE+"/package.cjs",decision:DECISION,adopted:stamp==="adopted"?ADOPTED:null,status:stamp+": main case v9",case:bp.meta.case+"; v9 "+stamp,population_v9:clone(population),items:(bp.meta.items||[]).concat(rr),v9:{coverage_mode:COVERAGE_MODE,stub13:STUB13,selected_items:identity.ids,default_arms:DEFAULT_ARMS,post_engine_rule:"evaluateFull or postFor; method-specific spending and specification-specific capital"}});
  return out;
 };
 if(meta.health_residual_key)meta.health_residual_key.parent_transport={allocation:"delivered personal original-union/completion donor prices carried under shared specifications; own household donor calibration not measured",lineage:"source own-age profiles held; each added-lineage profile follows its declared count/C3 mass",coverage_count:"source-owned arm-specific signed coverage/count increments; central count kernel carried under lineage/DA options"};
 const payload=payloadFor();
 function apply(m,o){
  // modelFor's inherited incremental route does not carry v8's carrier index.
  // Source item18 needs that index to edit reporter receipts as well as originals.
  let out={...m,corrections:{...m.corrections,union_completion:clone(p0.meta.union_completion)}};
  for(const {x}of built)out=V8.Engine.applyCorrections(out,{edits:x.editsAt?x.editsAt(out,o||{}):x.edits,meta:out.corrections});return out;
 }
 function postAdditions(m,s,p,r){
  const amounts={},parts={};
  for(const {item,arm,x}of built){
   const block=meta[item.id];if(!block)continue;
   if(item.id==="one_rate")continue;
   if(Object.hasOwn(SPEND.IDS,13)&&Object.values(SPEND.IDS).includes(item.id)){
    const n=Number(Object.keys(SPEND.IDS).find(n=>SPEND.IDS[n]===item.id));
    let priceRun=r,priceSpec=s;
    if(n===21)priceSpec={...s,health_residual_rate:s.rate?(meta.one_rate?RATE.rateFor(meta.one_rate,s):s.rate):0};
    if(n===15&&!s.rate){
     priceSpec={...s,rate:base.RATES[s.reading]};
     priceRun={...r,capital:base.capitalReturn(r.evaluation,priceSpec)};
    }
    let rows=SPEND.deltaParts(n,x.detail,sourceApi,priceRun,priceSpec,arm);
    if(n===21){
     const principal=PRINCIPAL_LINEAGE,current=p0.meta.lineage;
     const masses=l=>({lineage_later_g3:l.counts.later_losses,lineage_g3_rate_g3:l.counts.at_g3_rate*(1-l.c3.value),lineage_g3_rate_white:l.counts.at_g3_rate*l.c3.value});
     const before=masses(principal),after=masses(current);
     rows=rows.map(q=>{
      if(q.population!=="added_lineage")return q;
      if(!Object.hasOwn(before,q.profile)||!(before[q.profile]>0))fail("item21 lineage profile absent "+q.profile);
      const factor=after[q.profile]/before[q.profile],out={...q,lineage_count_factor:factor,lineage_rule:"source own-age profile held; each declared lineage part follows its own count/C3 mass"};
      for(const key of ["delta_bn","change_bn","before_bn","after_bn","capital_stock_delta_bn","capital_stock_before_bn"])if(Number.isFinite(q[key]))out[key]=q[key]*factor;
      return out;
     });
    }
    // The inherited specs encode an explicit long_run:false request as null.
    if(n===13&&!s.long_run)rows=rows.map(q=>({...q,after_bn:q.before_bn,delta_bn:0,response:1,first_year_restored_bn:-q.delta_bn,horizon_rule:"first year: removed entitlements stop; no replacement veterans yet"}));
    if(n===15&&!s.rate)rows=rows.map(q=>q.kind==="college_capital"?{...q,before_bn:0,after_bn:0,delta_bn:0}:q);
    if(coverageOverride)rows=rows.filter(q=>q.population!=="coverage");
    amounts[item.id]=sum(rows.map(q=>q.delta_bn));parts[item.id]=rows;
   }else amounts[item.id]=block.by_end?.[s.reading]?.total_bn||0;
  }
  if(coverageOverride){
   amounts.coverage_repricing=coverageOverride.by_end[s.reading].total_bn-(base.POST_ENGINE.coverage?.by_end[s.reading].total_bn||0);
   // The repriced coverage kernel already applies receipt ratios once.
   if(Object.hasOwn(amounts,"consumption_tax_bases"))amounts.consumption_tax_bases=0;
  }
  if(meta.one_rate){const z=RATE.at(sourceApi,r,s,meta.one_rate,parts.public_college_response||[],coverageOverride,meta);amounts.one_rate=z.total_bn;parts.one_rate=z.parts;}
  return {amounts,parts,total_bn:sum(Object.values(amounts))};
 }
 const evaluate=(fn,m,s,p)=>{const r=fn(m,s,p),d=postAdditions(m,s,p,r);return {...r,cost_bn:r.cost_bn+d.total_bn,post_engine:{...r.post_engine,...Object.fromEntries(Object.entries(d.amounts).map(([k,v])=>[k+"_bn",v])),total_bn:(r.post_engine?.total_bn||0)+d.total_bn},v9_post_engine:d};};
 const evaluateFull=(m,s,p)=>evaluate(base.evaluateFull,m,s,p),viaCandidate=(m,s,p)=>evaluate(base.viaCandidate,m,s,p);
 const modelFor=(name,method,o)=>apply(base.modelFor(name,method,o),o);
 const payloadModel=()=>V8.Engine.applyCorrections(V8.MODEL,payload);
 const cost=(m,s,p)=>evaluateFull(m,s,p).cost_bn;
 // Preserve the inherited specification identity. Item20 replaces its economic
 // rate through a typed post-engine revaluation, rather than changing v5's key.
 const specsFor=o=>base.specsFor(o);
 const MAIN_SPECS=specsFor({}),SHARED_SPECS=specsFor({allocation:"shared"}),ALL_SPECS=specsFor({allocation:"all"});
 const bandFor=(m,p,ss)=>V8.span(ss.map(s=>cost(m,s,p)));
 const evalPackage=(name,method,o)=>{const oo=base.withCentral(o||{});return bandFor(modelFor(name,method,oo),oo.profile,specsFor(o));};
 const central=o=>V8.mean2(...V8.METHODS.map(method=>evalPackage("central",method,o)));
 return {...base,HERE,LANE,CASE_KEY,DECISION,STATUS:stamp,ADOPTED:stamp==="adopted"?ADOPTED:null,correctionsPayload:payloadFor,payloadModel,modelFor,withItems:(m,o)=>apply(base.withItems(m,o),o),evaluateFull,viaCandidate,cost,bandFor,band:(m,p)=>bandFor(m,p,MAIN_SPECS),evalPackage,central,specsFor,MAIN_SPECS,SHARED_SPECS,ALL_SPECS,CASE_ITEMS:base.CASE_ITEMS.concat(records),ITEM_EDITS:base.ITEM_EDITS.concat(edits),V9_ITEMS:records,V9_EDITS:edits,POST_ENGINE:{...base.POST_ENGINE,...meta},POPULATION_V9:population,postFor:(m,s,p,r)=>postAdditions(m,s,p,r||base.evaluateFull(m,s,p)),postEngine:s=>evaluateFull(payloadModel(),s).post_engine.total_bn,OCT15:base,V9_BASE:base,V9_BUILT:built};
}
function caseOf(B,ids,selection={},lineage){
 const order=ids.map(id=>REGISTRY.findIndex(x=>x.id===id));
 if(order.some((n,i)=>n<0||(i&&n<=order[i-1])))fail("unknown/duplicate/out-of-order item");
 for(const [id,arm]of Object.entries(selection))if(!ids.includes(id)||!REGISTRY.find(x=>x.id===id)?.arms[arm])fail("unknown arm "+id+":"+arm);
 const old=ids.filter(id=>!NEW_IDS.includes(id)),sel=Object.fromEntries(Object.entries(selection).filter(([id])=>!NEW_IDS.includes(id)));
 const key=JSON.stringify([old,sel,lineage||null]);let base=USE_CASE_CACHE&&B===V8.OCT05?cache.get(key):null;
 if(!base){base=B===V8.OCT05&&JSON.stringify(old)===JSON.stringify(V8.CANDIDATE)&&!Object.keys(sel).length&&!lineage?V8_RUNTIME_BASE:v8CaseOf(B,old,sel,lineage);if(USE_CASE_CACHE&&B===V8.OCT05)cache.set(key,base);}
 const next=ids.filter(id=>NEW_IDS.includes(id));if(!next.length)return base;
 return caseOn9(base,next,selection,undefined,lineage);
}
function caseOn9(base,next,selection={},stamp,lineage){
 const ids=(base.ITEM_IDS||V8.CANDIDATE).filter(id=>!NEW_IDS.includes(id)).concat(next);
 const setView=withDeclaredCoverageParts(base,"set"),cashView=withDeclaredCoverageParts(base.CASH,"cash");
 const buildBase=setView===base&&cashView===base.CASH?base:{...setView,CASH:cashView};
 const ctx={B:buildBase,DETAIL:base.ITEM_DETAIL,Engine:V8.Engine,MODEL:V8.MODEL,METHODS:V8.METHODS,readJson:V8.readJson,sha256:V8.sha256,selectedItems:ids};
 let memo=buildCache.get(base);if(!memo){memo=new Map();buildCache.set(base,memo);}
 const pieces=which=>next.map(id=>{
  const item=NEW.find(x=>x.id===id),arm=selection[id]||DEFAULT_ARMS[id]||null;if(!item)fail("unknown new item "+id);
  const k=JSON.stringify([id,arm,which,id==="coverage_tenure"&&ids.includes("native_minor_calibration")]);
  if(!memo.has(k)){
   let x;
   if(id==="veterans_compensation"&&base!==V8){
    // The producer's generation builder is pinned to canonical v8 generation
    // models. Reprice its own delivered line bridge on the variant's model;
    // retain the canonical generation split as an explicit transport only.
    x=clone(item.build({...ctx,B:V8},arm,which));
    const api=which==="cash"?cashView:setView,block=x.meta[id];
    for(const end of ["low","high"]){
     const runs=SPEND.endpointRuns(api)[end],rows=runs.map(({r,s})=>SPEND.deltaParts(13,x.detail,api,r,s,arm));
     const total=meanNumbers(rows.map(a=>sum(a.map(q=>q.delta_bn)))),prior=block.by_end[end].total_bn;
     block.by_end[end].total_bn=total;
     block.by_end[end].parts=rows[0].map((q,j)=>({...q,delta_bn:meanNumbers(rows.map(a=>a[j].delta_bn))}));
     block.by_end[end].by_method=Object.fromEntries(runs.map((q,j)=>[q.method,{total_bn:sum(rows[j].map(p=>p.delta_bn)),parts:rows[j]}]));
     if(block.by_end[end].by_generation_bn)for(const g of Object.keys(block.by_end[end].by_generation_bn))block.by_end[end].by_generation_bn[g]*=prior?total/prior:0;
    }
    block.generation_transport="canonical source generation proportions scaled to variant totals; v9 generation evaluator supplies its own line routing";
   }else x=item.build(ctx,arm,which);
   if(id==="passthrough_source_tax")x=require("./item_passthrough_options.cjs").reprice(x,base);
   if(id==="consumption_tax_bases"&&ITEM18_CARRIER_MODE==="source_evaluator"){
    // Source evaluator's modelFor route lacks corrections.union_completion:
    // it evaluates no reporter edits, despite declaring them in the payload.
    // Make the same policy explicit on EVERY route; the alternative is a switch.
    const sourceEdits=x.edits,original=x.editsAt,keep=e=>!e.line.startsWith("union_completion_");
    x={...x,edits:sourceEdits.filter(keep),editsAt:(m,o)=>original(m,o).filter(keep),parts:Object.fromEntries(sourceEdits.filter(keep).map((e,i)=>[`${e.side}:${e.line}:${e.scenario||e.key}`,{edit:i,by:clone(e.by),source_arm:arm}]))};
    x.meta=clone(x.meta);x.meta[id].reporter_carrier_policy="source_evaluator: held as its executed oracle; ITEM18_CARRIER_MODE=declared_carriers applies source-declared reporter edits";
    x.meta[id].source_declared_reporter_edits=sourceEdits.filter(e=>!keep(e));
   }
   memo.set(k,x);
  }
  return {item,arm,x:memo.get(k)};
 });
 const identity={stamp:stamp||(JSON.stringify(ids)===JSON.stringify(CANDIDATE)&&!Object.keys(selection).length&&!lineage?STATUS:"variant"),ids};
 const set=layer(base,pieces("set"),"set",identity),cash=layer(base.CASH,pieces("cash"),"cash",identity);
 return {...set,CASH:cash,CASH_PAYLOAD:cash.correctionsPayload(),ITEM_IDS:ids,ITEM_ARMS:clone(selection),V9_IDS:next};
}
const CASE=caseOf(V8.OCT05,process.env.V9_NEW_ITEMS==="0"?V8.CANDIDATE:CANDIDATE);
module.exports={...V8,...CASE,V8_PACKAGE:V8,OCT15:V8,REGISTRY,CANDIDATE,NEW_IDS,DEFAULT_ARMS,caseOf,caseOn9,forItems9:layer,COVERAGE_MODE,STUB13,SPEND,R5_COUNT:COUNT_ITEMS,BASKET,PASS,RATE,ITEM19,ITEM19_ARM,ITEM18_CARRIER_MODE,V9:{HERE,LANE,CASE_KEY,DECISION,STATUS,ADOPTED}};
