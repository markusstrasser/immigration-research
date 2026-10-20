/* G4: v8 consumer calls plus explicit v9 population, generation and line routing. */
"use strict";
const fs=require("fs"),path=require("path"),P=require("./package.cjs"),V=P.V8_PACKAGE;
const records=[],sum=a=>a.reduce((x,y)=>x+y,0),clone=x=>JSON.parse(JSON.stringify(x));
process.on("uncaughtExceptionMonitor",error=>{fs.mkdirSync(path.join(__dirname,"derived"),{recursive:true});fs.writeFileSync(path.join(__dirname,"derived/api_check.json"),JSON.stringify({gate:"G4",pass:false,error:String(error),checks:records.length,records},null,1)+"\n");});
const near=(a,b,t=1e-9)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=t;
const gate=(name,ok,details=null)=>{records.push({name,pass:!!ok,details});console.log(`${ok?"PASS":"FAIL"} ${name}`);if(!ok){if(details!==null)console.log(JSON.stringify(details));throw Error(`[BLOCKED] G4 ${name}`);}};
const rejects=(name,fn,re=/BLOCKED/)=>{let stopped=false;try{fn();}catch(e){stopped=re.test(String(e));}gate(`guard ${name}`,stopped);};
function routeGenerations(parts){const out={G1:0,G2:0,G3plus:0};for(const [g,n]of Object.entries(parts)){const target=g==="added_G3plus"?"G3plus":g;if(!Object.hasOwn(out,target)||!Number.isFinite(n))throw Error(`[BLOCKED] G4 unmapped generation ${g}`);out[target]+=n;}return out;}
for(const key of Object.keys(V))gate(`v8 exported name ${key} retained`,key in P);
for(const key of ["modelFor","payloadModel","correctionsPayload","withItems","withCentral","specsFor","responsesFor","evaluateFull","viaCandidate","cost","bandFor","band","evalPackage","central","withSyntheticLines","stateFor","postFor"])gate(`callable ${key}`,typeof P[key]==="function");
gate("all three specification collections retained",[P.MAIN_SPECS,P.SHARED_SPECS,P.ALL_SPECS].every(s=>Array.isArray(s)&&s.length>0));
const OFF=P.caseOf(P.OCT05,V.CANDIDATE);
gate("new items off returns exact v8 set payload",JSON.stringify(OFF.correctionsPayload())===JSON.stringify(V.correctionsPayload()));
gate("new items off returns exact v8 cash payload",JSON.stringify(OFF.CASH.correctionsPayload())===JSON.stringify(V.CASH.correctionsPayload()));
const countData=JSON.parse(fs.readFileSync(path.join(__dirname,"../count_composition_r5_2026_10_15/derived/items.json"),"utf8"));
for(const [which,X]of [["set",P],["cash",P.CASH]]){
 const pl=X.correctionsPayload(),pm=X.payloadModel(),raw=P.Engine.applyCorrections(P.MODEL,pl);
 gate(`${which} payload applies with raw engine`,JSON.stringify(raw)===JSON.stringify(pm));
 if(P.V9.STATUS==="adopted")gate(`${which} adopted stamp (${P.V9.ADOPTED}, ${P.V9.DECISION} exists)`,pl.meta.adopted===P.V9.ADOPTED&&/^adopted: /.test(pl.meta.status)&&pl.meta.decision===P.V9.DECISION&&fs.existsSync(path.resolve(__dirname,"../../..",P.V9.DECISION)));
 else gate(`${which} candidate stamp`,pl.meta.adopted===null&&/^candidate: /.test(pl.meta.status)&&pl.meta.decision===P.V9.DECISION);
 gate(`${which} full selected registry declared for sibling routing`,JSON.stringify(pl.meta.v9.selected_items)===JSON.stringify(P.CANDIDATE));
 for(const method of P.METHODS){
  const m=X.modelFor("central",method,X.withCentral({}));
  for(const i of [16,11,0,31]){
   const s=X.MAIN_SPECS[i],r=X.evaluateFull(m,s),post=X.postFor(m,s);
   gate(`${which}/${method}/${i} viaCandidate`,near(r.cost_bn,X.viaCandidate(m,s).cost_bn));
   gate(`${which}/${method}/${i} cost`,r.cost_bn===X.cost(m,s));
   gate(`${which}/${method}/${i} v9 postFor closes`,near(sum(Object.values(post.amounts)),post.total_bn)&&near(r.v9_post_engine.total_bn,post.total_bn));
   const base=X.V9_BASE.evaluateFull(m,s);
   gate(`${which}/${method}/${i} inherited and new post route`,near(base.cost_bn+post.total_bn,r.cost_bn));
  }
 }
 for(const i of [16,11]){
  const s=X.MAIN_SPECS[i],ev=P.Engine.evaluate(pm,X.stateFor(pm,s)),ref=X.evaluateFull(pm,s),post=X.postFor(pm,s);
  gate(`${which}/${i} stateFor carrier responses`,near(ev.welfare_bn,ref.evaluation.welfare_bn));
  gate(`${which}/${i} raw engine plus declared post amounts closes`,near(-ev.welfare_bn+ref.capital.total_bn+X.V9_BASE.postEngine(s)+post.total_bn,ref.cost_bn));
  gate(`${which}/${i} retained postEngine returns full canonical post amount`,near(X.postEngine(s),ref.post_engine.total_bn));
 }
 for(const o of [{allocation:"shared"},{incomeTax:"row3",tax_key:"cbo_2022"}]){
  const cp=X.correctionsPayload(o),m=P.Engine.applyCorrections(P.MODEL,cp),b=X.bandFor(m,null,X.specsFor(o)),want=X.central(o);
  gate(`${which} options payload ${JSON.stringify(o)}`,b.every((n,i)=>near(n,want[i])),{payload:b,central:want,difference:b.map((n,i)=>n-want[i])});
 }
 rejects(`${which} payload rate guard retained`,()=>X.correctionsPayload({capital:false}),/moves the specification field rate/);
 const people=pl.meta.union_completion?.observed_records||[];
 gate(`${which} completion people available to household consumer`,people.length>0&&people.every(x=>x.PH_SEQ!==undefined||x.ph_seq!==undefined||x.household!==undefined||Array.isArray(x)),{records:people.length});
 for(const id of ["foreign_source_tax","union_completion"]){
  const rec=pl.meta.items.find(x=>x.id===id);
  gate(`${which}/${id} registry edit range`,rec&&rec.edits.count>0&&rec.edits.first+rec.edits.count<=pl.edits.length);
  gate(`${which}/${id} generation edit parts close`,Array.from({length:rec.edits.count},(_,j)=>{const e=pl.edits[rec.edits.first+j],parts=Object.entries(rec.parts).filter(([,p])=>p.edit===j);return parts.length>0&&parts.every(([name])=>/^(union_(G1|G2|G3plus):|lineage_)/.test(name))&&["personal","shared"].every(a=>near(sum(parts.map(([,p])=>p.by[a])),e.by[a]));}).every(Boolean));
 }
 for(const id of ["native_minor_calibration","coverage_tenure","health_residual_key",...(P.CANDIDATE.includes(P.PASS.id)?[P.PASS.id]:[])]){
  const block=pl.meta[id],record=pl.meta.items.find(r=>r.id===id);
  gate(`${which}/${id} post-engine registry route`,!!block&&!!record&&record.kind==="post_engine"&&record.post_engine_by_end);
  for(const end of ["low","high"]){const z=block.by_end[end],parts=z.by_generation_bn;gate(`${which}/${id}/${end} generation parts close`,parts&&near(sum(Object.values(parts)),z.total_bn),parts);const routed=routeGenerations(parts);gate(`${which}/${id}/${end} generation consumer routes descendants to G3plus`,near(sum(Object.values(routed)),z.total_bn),routed);}
 }
 for(const end of ["low","high"]){
  const a=pl.meta.native_minor_calibration.by_end[end],b=pl.meta.coverage_tenure.by_end[end],source=countData.sets[which].joint.by_end[end];
  // Base-price metadata retains the source oracle. Repriced amounts are gated separately by coverage integration.
  if(P.COVERAGE_MODE==="base")gate(`${which}/${end} selectedItems joint-minus-16, never standalone stack`,near(a.total_bn+b.total_bn,source.total_bn));
  gate(`${which}/${end} count sibling selected explicitly`,pl.meta.coverage_tenure.conditional_on_item16===true&&pl.meta.coverage_tenure.subtract_parts_scenario==="item16");
  const c=pl.meta.coverage.by_end[end],mix=pl.meta.mixed_unit_removal.by_end[end];
  gate(`${which}/${end} inherited coverage generation route`,near(sum(Object.values(c.by_generation)),c.total_bn));
  gate(`${which}/${end} inherited removal generation route`,near(sum(Object.values(mix.by_generation_bn)),mix.total_bn)&&mix.replicates_bn.length===161);
  const military=pl.meta.veterans_compensation.by_end[end],parts=military.parts;
  gate(`${which}/${end} household sees military source-line parts`,Array.isArray(parts)&&parts.length>0&&parts.every(p=>typeof p.line==="string"&&typeof p.source_line==="string"&&["engine","completion","coverage"].includes(p.population)&&Number.isFinite(p.delta_bn)));
  const grouped={};for(const p of parts)grouped[p.source_line]=(grouped[p.source_line]||0)+p.delta_bn;
  gate(`${which}/${end} household military line split closes`,near(sum(Object.values(grouped)),military.total_bn),grouped);
  if(P.STUB13)console.log(`[STUB-13] ${which}/${end} military household extension awaiting L1 STEP 2 DONE`);
  else gate(`${which}/${end} military extension reaches household consumer`,parts.some(p=>p.part==="extension")&&Object.keys(grouped).length>=3);
 }
 const pop=pl.meta.population_v9,old=pl.meta.population_v8,cal=pl.meta.native_minor_calibration,ten=pl.meta.coverage_tenure;
 gate(`${which} calibrated denominator equals declared count changes`,near(pop.with_coverage,old.with_coverage+cal.population_change+ten.population_change,1e-6));
 gate(`${which} calibrated denominator available without coverage`,Number.isFinite(pop.without_coverage)&&pop.with_coverage>pop.without_coverage);
 gate(`${which} population parts close`,near(pop.without_coverage+pop.coverage,pop.with_coverage,1e-6));
 const firstOptions={long_run:false,rental:0,capital:false,enterprise_receipt:0,school_rule:"one_year",roads:"resources",property:"none",item6_first_year:true};
 const firstSpecs=X.specsFor(firstOptions);
 for(const method of P.METHODS)for(const i of [16,11]){
  const s=firstSpecs[i],fm=X.modelFor("central",method,X.withCentral(firstOptions)),r=X.evaluateFull(fm,s),military=r.v9_post_engine.parts.veterans_compensation;
  gate(`${which}/${i} long_run false rejects steady-state item13`,!s.long_run&&r.v9_post_engine.amounts.veterans_compensation===0&&military.length>0&&military.every(p=>p.delta_bn===0&&p.response===1));
  gate(`${which}/${i} first-year military source responses`,military.every(p=>r.evaluation.spending.find(l=>l.id===p.source_line)?.response===1));
  const expected=-sum(pl.meta.veterans_compensation.by_end[s.reading].by_method[method].parts.filter(p=>p.population!=="coverage").map(p=>p.delta_bn));
  gate(`${which}/${i} first-year restoration excludes already-responsive pension`,near(sum(military.map(p=>p.first_year_restored_bn)),expected));
  const health=r.v9_post_engine.parts.health_residual_key;
  gate(`${which}/${i} item21 allocation retained in first year`,health.some(p=>p.source_line==="health_services"&&Math.abs(p.delta_bn)>1)&&health.filter(p=>Number.isFinite(p.capital_stock_delta_bn)).every(p=>p.delta_bn===0));
 }
 gate(`${which} default household basket arm`,pl.meta.consumption_tax_bases.arm==="household_joint");
 gate(`${which} item19 switch controls central selection`,P.ITEM19==="1"?pl.meta.passthrough_source_tax?.arm===P.DEFAULT_ARMS.passthrough_source_tax:!Object.hasOwn(pl.meta,"passthrough_source_tax")&&!pl.meta.items.some(x=>x.id===P.PASS.id));
 gate(`${which} default one-rate arm`,pl.meta.one_rate.arm==="B");
}
const oldHealth=P.caseOf(P.OCT05,P.CANDIDATE,{health_residual_key:"old_key"});
const offHealth=P.caseOf(P.OCT05,P.CANDIDATE.filter(id=>id!=="health_residual_key"));
for(const [which,X,Y]of [["set",oldHealth,offHealth],["cash",oldHealth.CASH,offHealth.CASH]])for(const i of [16,11]){
 gate(`${which}/${i} old-key arm reproduces complete pre21 case`,near(X.cost(X.payloadModel(),X.MAIN_SPECS[i]),Y.cost(Y.payloadModel(),Y.MAIN_SPECS[i])));
 gate(`${which}/${i} old-key source increment zero`,X.postFor(X.payloadModel(),X.MAIN_SPECS[i]).parts.health_residual_key.every(p=>p.delta_bn===0));
}
const with19=P.REGISTRY.filter(x=>P.CANDIDATE.includes(x.id)||x.id===P.PASS.id).map(x=>x.id);
const beside=P.caseOf(P.OCT05,with19);
for(const [which,X]of [["set",beside],["cash",beside.CASH]]){
 const block=X.correctionsPayload().meta.passthrough_source_tax;
 gate(`${which} beside item19 numeric-intent arm`,block.arm===P.ITEM19_ARM);
 for(const end of ["low","high"]){const z=block.by_end[end],routed=routeGenerations(z.by_generation_bn);gate(`${which} beside item19/${end} generation consumer closes`,near(sum(Object.values(routed)),z.total_bn),routed);}
 gate(`${which} optional item19 preserves v9 coverage prices`,X.correctionsPayload().meta.coverage.sha256===(which==="set"?P:P.CASH).correctionsPayload().meta.coverage.sha256);
}
for(const [name,fn]of [
 ["unknown item",()=>P.caseOf(P.OCT05,["bogus"])],
 ["duplicate item",()=>P.caseOf(P.OCT05,[P.CANDIDATE[0],P.CANDIDATE[0]])],
 ["out-of-order item",()=>P.caseOf(P.OCT05,[P.CANDIDATE[1],P.CANDIDATE[0]])],
 ["unknown arm",()=>P.caseOf(P.OCT05,P.CANDIDATE,{passthrough_source_tax:"bogus"})],
 ["arm for unselected item",()=>P.caseOf(P.OCT05,V.CANDIDATE,{coverage_tenure:"count_transfer"})],
 ["count builder requires selectedItems",()=>P.R5_COUNT.build17({},null,"set")],
 ["count builder rejects malformed selectedItems",()=>P.R5_COUNT.build17({selectedItems:"native_minor_calibration"},null,"set")],
 ["source pass-through builder requires explicit arm",()=>P.PASS.build({},null,"set")],
 ["source basket builder requires explicit arm",()=>P.BASKET.build({},null,"set")],
 ["generation consumer rejects unknown destination",()=>routeGenerations({G4:1})],
])rejects(name,fn);
const ctx={B:V,selectedItems:V.CANDIDATE.concat(["coverage_tenure"])};
for(const which of ["set","cash"]){
 const alone=P.R5_COUNT.build17(ctx,null,which).meta.coverage_tenure;
 gate(`${which} standalone tenure keeps standalone route`,alone.conditional_on_item16===false&&alone.subtract_parts_scenario===null&&["low","high"].every(e=>near(alone.by_end[e].total_bn,countData.sets[which].item17.by_end[e].total_bn)));
}
const bad=clone(P.correctionsPayload().meta.native_minor_calibration.by_end.low);bad.by_generation_bn.G1+=1;
gate("negative generation closure probe rejects corruption",!near(sum(Object.values(bad.by_generation_bn)),bad.total_bn));
require("./memory_guard.cjs").requireWithinBudget("G4");
gate("Node process passes canonical physical-footprint budget",true);
fs.mkdirSync(path.join(__dirname,"derived"),{recursive:true});
fs.writeFileSync(path.join(__dirname,"derived/api_check.json"),JSON.stringify({gate:"G4",pass:true,verdict:P.STUB13?"STUB-13: PASS":"PASS",stub13:!!P.STUB13,coverage_mode:P.COVERAGE_MODE,checks:records.length,records},null,1)+"\n");
console.log(`${P.STUB13?"[STUB-13] ":""}G4 PASS ${records.length} checks; maxRSS ${process.resourceUsage().maxRSS} KiB`);
