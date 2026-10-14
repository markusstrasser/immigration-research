/* v8 extends v7 without mutating its modules or outputs. Items off return v7 itself. */
"use strict";
const fs=require("fs"),path=require("path");
const V7=require("../main_case_2026_10_14/package.cjs");
const FOREIGN=require("./item_foreign.cjs"), MIXED=require("./item_mixed.cjs"), COVER=require("./coverage.cjs");
const HERE=__dirname,LANE="main_case_2026_10_15",CASE_KEY="oct15",DECISION="decisions/2026-10-15-main-case-v8.md";
const STATUS="adopted", ADOPTED="2026-10-15";
const ITEM6_LOW_CORPORATE_RESPONSE=Number(process.env.ITEM6_LOW_CORPORATE_RESPONSE??1);
const COVERAGE=process.env.COVERAGE!=="0";
const clone=x=>JSON.parse(JSON.stringify(x));
const fail=s=>{throw Error(`[BLOCKED] v8: ${s}`);};
function addProduction(m,x,o){const fn=x.productionAt||x.productionDeltaAt,d=fn?fn(m,o):x.production_delta;if(!d)return m;
 if(JSON.stringify(d.dims)!==JSON.stringify(m.production.dims))fail("new-person production dimensions differ");
 for(const f of ["private_wtp_bn","induced_receipts_bn"]){if(d[f].length!==m.production[f].length||!d[f].every(Number.isFinite))fail(`invalid production delta ${f}`);m.production[f]=m.production[f].map((n,i)=>n+d[f][i]);}
 return m;}
if(!Number.isFinite(ITEM6_LOW_CORPORATE_RESPONSE)||ITEM6_LOW_CORPORATE_RESPONSE<0||ITEM6_LOW_CORPORATE_RESPONSE>1) fail("invalid ITEM6_LOW_CORPORATE_RESPONSE");
if(STATUS==="adopted"&&!fs.existsSync(path.resolve(HERE,"../../..",DECISION))) fail("adoption requires decision file");
const NEW=[
 {id:"foreign_source_tax",kind:"edit_set",label:"domestic-source corporate tax",arms:{},build:FOREIGN.build},
 {id:"union_completion",kind:"edit_set",label:"complete observed membership",arms:{broad_report:{label:"broad reporters"},all_age_extrapolation:{label:"all-age extrapolation"}},build:(ctx,arm,which)=>require("./item_union.cjs").build(ctx,arm,which)},
 {id:"mixed_unit_removal",kind:"post_engine",label:"bounded unified removal",arms:MIXED.ARMS,build:MIXED.build},
 {id:"coverage",kind:"post_engine",label:"coverage people and cost",arms:{da_middle:{},da_low:{},da_high:{},pes_only:{}},build:(ctx,arm,which)=>({edits:[],parts:{},meta:{coverage:COVER.get(which,arm||"central")}})},
 {id:"item6_low_corporate_response",kind:"response",label:"item6 low corporate-response parameter",arms:{},build:(ctx,arm,which)=>({edits:[],parts:{},meta:{item6_low_corporate_response:{value:ITEM6_LOW_CORPORATE_RESPONSE,default:1}},responses:Object.fromEntries(FOREIGN.LINES.map(id=>[id,{...ctx.B.correctionsPayload().meta.responses[id],low:ITEM6_LOW_CORPORATE_RESPONSE}]))})},
];
const NEW_IDS=NEW.map(x=>x.id), REGISTRY=V7.REGISTRY.concat(NEW);
const CANDIDATE=V7.CANDIDATE.concat(NEW_IDS.filter(id=>(id!=="coverage"||COVERAGE)&&(id!=="item6_low_corporate_response"||ITEM6_LOW_CORPORATE_RESPONSE!==1)));
// New-item arms share the same immutable v7 construction. Reusing that case
// avoids rebuilding its hundreds of historical edits; custom bases never cache.
const baseCases=new Map();
function layer(base,built,which,identity) {
 const p0=base.correctionsPayload(), EDITS=[],RECORDS=[],META={},SP=[],RP=[],RESP={};
 for(const b of built)if(b.x.productionDeltaAt&&!b.x.productionAt)b.x.productionAt=b.x.productionDeltaAt;
 const itemOptions=o=>({...o,foreign_source_tax:built.some(b=>b.item.id==="foreign_source_tax"),...(built.some(b=>b.item.id==="item6_low_corporate_response")?{item6_low_corporate_response:ITEM6_LOW_CORPORATE_RESPONSE}:{})});
 let at=base.payloadModel();
 for(const b of built){const x=b.x;if(x.editsAt){const ps=x.partsAt?x.partsAt(at,itemOptions({})):null;x.edits=x.editsAt(at,itemOptions({}));if(ps)x.parts=ps;else for(let j=0;j<x.edits.length;j++){const parts=Object.values(x.parts||{}).filter(p=>p.edit===j);if(parts.length===1)parts[0].by=clone(x.edits[j].by);}}
   if(x.productionAt)x.production_delta=x.productionAt(at,itemOptions({}));
   at=addProduction(V7.Engine.applyCorrections(at,{lines:x.spending_lines||[],receipt_lines:x.receipt_lines||[],edits:x.edits,meta:at.corrections}),x,itemOptions({}));}
 for(const {item,arm,x} of built) {
   const n=p0.edits.length+EDITS.length;
   const r={id:item.id,kind:item.kind,label:item.label,applied:true,arm:arm||null,arms:clone(item.arms),edits:{first:n,count:x.edits.length},parts:clone(x.parts||{}),meta_changed:Object.keys(x.meta||{}),...(x.record||{})};
   if(item.kind==="post_engine"){const z=x.meta[item.id];r.post_engine_by_end=clone(z.by_end);r.by_generation_bn=Object.fromEntries(Object.entries(z.by_end).map(([end,v])=>[end,clone(v.by_generation_bn||v.by_generation)]));}
   if(x.production_delta){r.production_delta=clone(x.production_delta);r.production_generation="G3plus";r.production_population="observed nonreporting children";}
   RECORDS.push(r); EDITS.push(...clone(x.edits)); Object.assign(META,clone(x.meta));
   SP.push(...clone(x.spending_lines||[]));RP.push(...clone(x.receipt_lines||[]));
   for(const [id,v] of Object.entries(x.responses||{})) RESP[id]=clone(v);
 }
 const payload=clone(p0);
 payload.edits.push(...clone(EDITS));
 if(built.some(b=>b.x.production_delta||b.x.productionAt))payload.production=clone(at.production);
 if(SP.length) payload.lines=(payload.lines||[]).concat(clone(SP));
 if(RP.length) payload.receipt_lines=(payload.receipt_lines||[]).concat(clone(RP));
 Object.assign(payload.meta,META,{source:`${LANE}/package.cjs`,adopted:identity.stamp==="adopted"?ADOPTED:null,decision:DECISION,status:`${identity.stamp}: main case v8; ${NEW_IDS.filter(id=>META[id]).join(", ")}`,case:`${p0.meta.case}; v8 ${identity.stamp}`});
 payload.meta.items=(payload.meta.items||[]).concat(clone(RECORDS));
 payload.meta.responses={...payload.meta.responses,...clone(RESP)};
 const completion=META.union_completion;
 const carrierEntries=Object.entries(completion?.carriers||{});
 const completionCount=completion?.counts?.total??completion?.people_added??completion?.count??0;
 const oldPop=p0.meta.lineage.counts.lineage_population;
 const population=oldPop+completionCount+(META.coverage?.net_missing_people||0);
 payload.meta.population_v8={without_coverage:oldPop+completionCount,with_coverage:population,completion:completionCount,coverage:META.coverage?.net_missing_people||0};
 function apply(m,options) {
   let out=m;
   for(const {x} of built) {
     const edits=x.editsAt?x.editsAt(out,itemOptions(options)):x.edits;
     out=V7.Engine.applyCorrections(out,{lines:(x.spending_lines||[]).filter(l=>!out.spending.lines.some(z=>z.id===l.id)),receipt_lines:(x.receipt_lines||[]).filter(l=>!out.receipts.lines.some(z=>z.id===l.id)),edits,meta:out.corrections});
     out=addProduction(out,x,itemOptions(options));
   }
   return out;
 }
 const payloadModel=()=>V7.Engine.applyCorrections(V7.MODEL,payload);
 const withResponses=s=>{const out=s;out.line_responses={...s.line_responses};for(const [id,r] of Object.entries(RESP)) out.line_responses[r.receipt?`receipt:${id}`:id]=r[out.reading];return out;};
 const specsFor=o=>base.specsFor(o).map(withResponses);
 const post=(spec)=> (META.mixed_unit_removal?.by_end[spec.reading].total_bn||0)+(META.coverage?.by_end[spec.reading].total_bn||0);
 function evaluated(fn,m,s,profile) {
   if(!m.candidate&&m.corrections?.v8_model_candidate)m={...m,candidate:clone(m.corrections.v8_model_candidate)};
   let r=fn(m,s,profile);
   if(carrierEntries.length){const ev=r.evaluation;let delta=0;
     const spending=new Map(ev.spending.map(l=>[l.id,l])),receipts=new Map(ev.receipts.map(l=>[l.id,l]));
     for(const [id,src] of carrierEntries){
       let response=s.line_responses[id];
       if(src.kind==="line"){
         const parent=(src.side==="receipt"?receipts:spending).get(src.parent_line);
         if(!parent){if(require("./item_union.cjs").inactiveParent(m,src.side,src.parent_line)){response=0;}else fail(`union carrier ${id} parent absent`);}
         else {
         const selected=src.side==="receipt"?m.receipts.reference:parent.key;
         response=selected===src.parent_key?parent.response:0;
         }
       }
       if(!Number.isFinite(response))fail(`union carrier ${id} lacks response`);
       const row=spending.get(id);if(!row)fail(`union carrier ${id} absent`);
       const d=(response-row.response)*row.amount_bn;row.response=response;row.effect_bn=-response*row.amount_bn;
       ev.classes[row.group].responsive_bn+=d;delta+=d;
     }
     if(Math.abs(ev.welfare_bn-ev.private_wtp_bn-ev.direct_fiscal_response_bn-ev.induced_receipts_bn)>1e-8)fail("carrier response repair requires fiscal_weight1");
     ev.direct_fiscal_response_bn-=delta;ev.welfare_bn-=delta;
     ev.effective_service_response=ev.classes.service.assigned_bn?ev.classes.service.responsive_bn/ev.classes.service.assigned_bn:0;
     ev.per_target_person=ev.welfare_bn*1e9/m.meta.target_population;ev.per_other_resident=ev.welfare_bn*1e9/(m.meta.resident_population-m.meta.target_population);
     r={...r,evaluation:ev,cost_bn:r.cost_bn+delta};
   }
   const d=post(s);
   return {...r,cost_bn:r.cost_bn+d,post_engine:{mixed_unit_removal_bn:META.mixed_unit_removal?.by_end[s.reading].total_bn||0,coverage_bn:META.coverage?.by_end[s.reading].total_bn||0,total_bn:d}};
 }
 const evaluateFull=(m,s,p)=>evaluated(base.evaluateFull,m,s,p), viaCandidate=(m,s,p)=>evaluated(base.viaCandidate,m,s,p);
 const modelFor=(name,method,o)=>apply(base.modelFor(name,method,o),o);
 const cost=(m,s,p)=>evaluateFull(m,s,p).cost_bn;
 const bandFor=(m,p,ss)=>V7.span(ss.map(s=>cost(m,s,p)));
 const evalPackage=(name,method,o)=>{const oo=base.withCentral(o||{});return bandFor(modelFor(name,method,oo),oo.profile,specsFor(o));};
 const central=o=>V7.mean2(...V7.METHODS.map(method=>evalPackage("central",method,o)));
 const MAIN_SPECS=specsFor({}),SHARED_SPECS=specsFor({allocation:"shared"}),ALL_SPECS=specsFor({allocation:"all"});
 function correctionsPayload(o) {
   if(o&&Object.keys(o).length){
     const bp=base.correctionsPayload(o),out=clone(bp),edits=[];let m=V7.Engine.applyCorrections(V7.MODEL,bp);
     const typed=base.modelFor("central",V7.METHODS[0],base.withCentral(o));
     if(typed.candidate)m.candidate=clone(typed.candidate);
     const recs=clone(RECORDS);
     for(let i=0;i<built.length;i++){const x=built[i].x,e=x.editsAt?x.editsAt(m,itemOptions(o)):x.edits;
       if(x.partsAt)recs[i].parts=clone(x.partsAt(m,itemOptions(o)));
       recs[i].edits.first=bp.edits.length+edits.length;
       recs[i].edits.count=e.length;
       for(let j=0;j<e.length;j++){const parts=Object.values(recs[i].parts||{}).filter(p=>p.edit===j);for(const a of ["personal","shared"]){const sum=parts.reduce((s,p)=>s+p.by[a],0);if(parts.length===1)parts[0].by[a]=e[j].by[a];else if(sum!==0)for(const p of parts)p.by[a]*=e[j].by[a]/sum;}}
       if(x.productionAt)recs[i].production_delta=clone(x.productionAt(m,itemOptions(o)));
       edits.push(...clone(e));m=addProduction(V7.Engine.applyCorrections(m,{lines:x.spending_lines||[],receipt_lines:x.receipt_lines||[],edits:e,meta:m.corrections}),x,itemOptions(o));
     }
     out.edits=bp.edits.concat(edits);out.meta={...bp.meta,...clone(META),source:`${LANE}/package.cjs`,adopted:null,decision:DECISION,status:"variant: v8 option payload",case:`${bp.meta.case}; v8 option payload`,items:(bp.meta.items||[]).concat(recs),responses:{...bp.meta.responses,...clone(RESP)},population_v8:clone(payload.meta.population_v8)};
     if(typed.candidate)out.meta.v8_model_candidate=clone(typed.candidate);
     if(built.some(b=>b.x.production_delta||b.x.productionAt))out.production=clone(m.production);
     out.lines=(bp.lines||[]).concat(clone(SP));out.receipt_lines=(bp.receipt_lines||[]).concat(clone(RP));
     return out;
   }
   return clone(payload);
 }
 const withSyntheticLines=m=>{const mm=base.withSyntheticLines(m);return V7.Engine.applyCorrections(mm,{lines:SP.filter(l=>!mm.spending.lines.some(z=>z.id===l.id)),receipt_lines:RP.filter(l=>!mm.receipts.lines.some(z=>z.id===l.id)),edits:[],meta:mm.corrections});};
 const stateFor=(m,s,profile)=>{const st=base.stateFor(m,s,profile);if(carrierEntries.length){const ev=V7.Engine.evaluate(m,st),spending=new Map(ev.spending.map(l=>[l.id,l])),receipts=new Map(ev.receipts.map(l=>[l.id,l]));for(const [id,src] of carrierEntries)if(src.kind==="line"){const parent=(src.side==="receipt"?receipts:spending).get(src.parent_line);if(!parent){if(require("./item_union.cjs").inactiveParent(m,src.side,src.parent_line)){st.response_override[id]=0;continue;}fail(`union carrier ${id} parent absent`);}const key=src.side==="receipt"?m.receipts.reference:parent.key;st.response_override[id]=key===src.parent_key?parent.response:0;}}return st;};
 return {...base,HERE,LANE,CASE_KEY,DECISION,STATUS:identity.stamp,ADOPTED:identity.stamp==="adopted"?ADOPTED:null,payloadModel,correctionsPayload,modelFor,withItems:(m,o)=>apply(base.withItems(m,o),o),withSyntheticLines,stateFor,specsFor,evaluateFull,viaCandidate,cost,bandFor,band:(m,p)=>bandFor(m,p,MAIN_SPECS),evalPackage,central,MAIN_SPECS,SHARED_SPECS,ALL_SPECS,RESPONSES:clone(payload.meta.responses),LINE_RESPONSES:{...base.LINE_RESPONSES,...RESP},responsesFor:o=>({...base.responsesFor(o),...clone(RESP)}),CASE_ITEMS:base.CASE_ITEMS.concat(RECORDS),ITEM_EDITS:base.ITEM_EDITS.concat(EDITS),V8_ITEMS:RECORDS,V8_EDITS:EDITS,POST_ENGINE:META,POPULATION_V8:payload.meta.population_v8,postEngine:post};
}
function caseOf(B,ids,sel={},lineage) {
 const order=ids.map(id=>REGISTRY.findIndex(x=>x.id===id));
 if(order.some((n,i)=>n<0||(i>0&&n<=order[i-1]))) fail("unknown/duplicate/out-of-order item");
 for(const [id,arm] of Object.entries(sel)) if(!ids.includes(id)||!REGISTRY.find(x=>x.id===id)?.arms[arm]) fail(`unknown arm ${id}:${arm}`);
 const old=ids.filter(id=>!NEW_IDS.includes(id));
 const oldSel=Object.fromEntries(Object.entries(sel).filter(([id])=>!NEW_IDS.includes(id))),cacheKey=JSON.stringify([old,oldSel,lineage||null]);
 let Q=B===V7.OCT05?baseCases.get(cacheKey):null;
 if(!Q){Q=V7.caseOf(B,old,oldSel,lineage);if(B===V7.OCT05)baseCases.set(cacheKey,Q);}
 const next=ids.filter(id=>NEW_IDS.includes(id));
 if(!next.length) return Q;
 const ctx={B:Q,DETAIL:Q.ITEM_DETAIL,Engine:V7.Engine,MODEL:V7.MODEL,METHODS:V7.METHODS,readJson:V7.readJson,sha256:V7.sha256};
 const pieces=next.map(id=>{const item=NEW.find(x=>x.id===id),arm=sel[id]||null;return {item,arm};});
 const identity={stamp:JSON.stringify(ids)===JSON.stringify(CANDIDATE)&&!Object.keys(sel).length&&!lineage?STATUS:"variant"};
 const built=which=>pieces.map(b=>({...b,x:b.item.build(ctx,b.arm,which)}));
 const set=layer(Q,built("set"),"set",identity), cash=layer(Q.CASH,built("cash"),"cash",identity);
 return {...set,CASH:cash,CASH_PAYLOAD:cash.correctionsPayload(),OCT14:Q,OCT14_CASH:Q.CASH,ITEM_IDS:old.concat(next),ITEM_ARMS:clone(sel),ITEM_DETAIL:Q.ITEM_DETAIL,V8_IDS:next};
}
const CASE=caseOf(V7.OCT05,CANDIDATE);
module.exports={...V7,...CASE,V7_PACKAGE:V7,REGISTRY,CANDIDATE,NEW_IDS,caseOf,forItems8:layer,FOREIGN,MIXED,COVER,COVERAGE,ITEM6_LOW_CORPORATE_RESPONSE,V8:{HERE,LANE,CASE_KEY,DECISION,STATUS,ADOPTED}};
