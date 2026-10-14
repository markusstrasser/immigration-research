/* G4: executable consumer calls, new population and generation routing. */
"use strict";
const fs=require("fs"),path=require("path"),P=require("./package.cjs"),V=P.V7_PACKAGE;
const records=[];
const gate=(name,ok,details=null)=>{records.push({name,pass:!!ok,details});console.log(`${ok?"PASS":"FAIL"} ${name}`);if(!ok)throw Error(`[BLOCKED] G4 ${name}`);};
const near=(a,b,t=1e-9)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=t;
const checks=["modelFor","payloadModel","correctionsPayload","withItems","withCentral","specsFor","responsesFor","evaluateFull","viaCandidate","cost","bandFor","band","evalPackage","central","withSyntheticLines","stateFor"];
for(const key of Object.keys(V))gate(`v7 exported name ${key} retained`,key in P);
for(const key of checks)gate(`callable ${key}`,typeof P[key]==="function");
for(const [which,X] of [["set",P],["cash",P.CASH]]){
 const pl=X.correctionsPayload(),pm=X.payloadModel(),raw=P.Engine.applyCorrections(P.MODEL,pl);
 gate(`${which} payload applies with raw engine`,JSON.stringify(raw)===JSON.stringify(pm));
 if(P.V8.STATUS==="adopted")gate(`${which} adopted stamp (${P.V8.ADOPTED}, ${P.V8.DECISION} exists)`,pl.meta.adopted===P.V8.ADOPTED&&/^adopted: /.test(pl.meta.status)&&pl.meta.decision===P.V8.DECISION&&fs.existsSync(path.resolve(__dirname,"../../..",P.V8.DECISION)));
 else gate(`${which} candidate stamp`,pl.meta.adopted===null&&/^candidate: /.test(pl.meta.status));
 for(const method of P.METHODS){const m=X.modelFor("central",method,X.withCentral({}));for(const i of [16,11,0,31]){const s=X.MAIN_SPECS[i],r=X.evaluateFull(m,s);gate(`${which}/${method}/${i} viaCandidate`,near(r.cost_bn,X.viaCandidate(m,s).cost_bn));gate(`${which}/${method}/${i} cost`,r.cost_bn===X.cost(m,s));}}
 for(const i of [16,11]){const s=X.MAIN_SPECS[i],ev=P.Engine.evaluate(pm,X.stateFor(pm,s));const ref=X.evaluateFull(pm,s);gate(`${which}/${i} stateFor carrier responses`,near(ev.welfare_bn,ref.evaluation.welfare_bn));const cap=ref.capital.total_bn;gate(`${which}/${i} declared post-engine amounts close`,near(-ev.welfare_bn+cap+X.postEngine(s),ref.cost_bn));}
 for(const o of [{allocation:"shared"},{incomeTax:"row3",tax_key:"cbo_2022"}]){const cp=X.correctionsPayload(o),m=P.Engine.applyCorrections(P.MODEL,cp),b=X.bandFor(m,null,X.specsFor(o)),want=X.central(o);gate(`${which} options payload ${JSON.stringify(o)}`,b.every((n,i)=>near(n,want[i])));}
 let upstreamRateGuard=false,ownRateGuard=false;try{(which==="set"?V:V.CASH).correctionsPayload({capital:false});}catch(e){upstreamRateGuard=/moves the specification field rate/.test(String(e));}try{X.correctionsPayload({capital:false});}catch(e){ownRateGuard=/moves the specification field rate/.test(String(e));}gate(`${which} payload rate guard retained from v7`,upstreamRateGuard&&ownRateGuard);
 const people=pl.meta.union_completion?.observed_records||[];gate(`${which} completion people available to household consumer`,people.length>0&&people.every(x=>x.PH_SEQ!==undefined||x.ph_seq!==undefined||x.household!==undefined||Array.isArray(x)),{records:people.length});
 for(const id of ["foreign_source_tax","union_completion"]){const rec=pl.meta.items.find(x=>x.id===id);gate(`${which}/${id} registry range`,rec&&rec.edits.count>0&&rec.edits.first+rec.edits.count<=pl.edits.length);for(let j=0;j<rec.edits.count;j++){const e=pl.edits[rec.edits.first+j],parts=Object.entries(rec.parts).filter(([,p])=>p.edit===j);gate(`${which}/${id}/${j} generation and lineage routing`,parts.length>0&&parts.every(([name])=>/^(union_(G1|G2|G3plus):|lineage_)/.test(name))&&["personal","shared"].every(a=>near(parts.reduce((n,[,p])=>n+p.by[a],0),e.by[a])));}}
 const mix=pl.meta.mixed_unit_removal;for(const e of ["low","high"]){const z=mix.by_end[e];gate(`${which} generation post-engine closure ${e}`,near(Object.values(z.by_generation_bn).reduce((a,b)=>a+b,0),z.total_bn)&&z.replicates_bn.length===161);if(pl.meta.coverage){const c=pl.meta.coverage;console.log(`${c.stub?"[STUB] ":""}coverage consumer ${which}/${e}`);gate(`${c.stub?"[STUB] ":""}${which} coverage generation closure ${e}`,near(Object.values(c.by_end[e].by_generation).reduce((a,b)=>a+b,0),c.by_end[e].total_bn));}}
 gate(`${which} lineage denominator includes completion and coverage`,near(pl.meta.population_v8.with_coverage,pl.meta.lineage.counts.lineage_population+pl.meta.union_completion.counts.total+(pl.meta.coverage?.net_missing_people||0),1e-6));
}
for(const [name,fn] of [["unknown item",()=>P.caseOf(P.OCT05,["bogus"])],["duplicate item",()=>P.caseOf(P.OCT05,[P.CANDIDATE[0],P.CANDIDATE[0]])],["unknown arm",()=>P.caseOf(P.OCT05,P.CANDIDATE,{mixed_unit_removal:"bogus"})]]){let stopped=false;try{fn();}catch(e){stopped=/BLOCKED/.test(String(e));}gate(`guard ${name}`,stopped);}
if(P.POST_ENGINE.coverage&&!P.POST_ENGINE.coverage.stub){
 const C=require("./companions.cjs"),saved=JSON.parse(fs.readFileSync(path.join(__dirname,"derived/summary.json"),"utf8")).v8;
 for(const [basis,X] of [["set",P],["cash",P.CASH]]){
  const fy=C.firstYear(P,basis),want=basis==="set"?saved.companions.first_year.band_bn:saved.companions.first_year.cash.band_bn;
  gate(`${basis} first-year own post-engine repricing`,fy.band_bn.every((n,i)=>near(n,want[i])));
  for(const pair of fy.post_engine_at_ends)for(const post of pair){
   gate(`${basis} first-year generation post parts close`,near(Object.values(post.by_generation).reduce((n,g)=>n+g.mixed_unit_removal_bn+g.coverage_bn,0),post.mixed_unit_removal_bn+post.coverage_bn));
   gate(`${basis} first-year coverage capital/property zero`,post.line_parts.filter(p=>p.economic_class==="capital_return"||p.source_side==="receipt"&&/property/.test(p.source_line)).every(p=>p.coverage_bn===0));
  }
  const m=X.payloadModel(),s=X.MAIN_SPECS[16],r=X.evaluateFull(m,s),shared=C.companionPost(X,s,r,"shared"),school=C.companionPost(X,{...s,school:.836},r,"school");
  gate(`${basis} shared excludes removal item11`,shared.mixed_unit_removal_bn===0&&near(shared.coverage_bn,X.POST_ENGINE.coverage.by_end.low.total_bn));
  gate(`${basis} school coverage follows its response`,school.line_parts.every(p=>near(p.coverage_bn,p.central_coverage_bn*(p.category==="schools"?.836:1))));
 }
 const fake={POST_ENGINE:{mixed_unit_removal:{which:"set",by_end:{low:{total_bn:0,by_generation_bn:{}}}},coverage:{by_end:{low:{total_bn:1,by_generation:{G1:1},decomposition:{line_parts:[{generation:"G1",economic_class:"fiscal_line",source_side:"spending",source_line:"missing",coverage_bn:1}]}}}}}};
 let stopped=false;try{C.companionPost(fake,{reading:"low"},{evaluation:{receipts:[],spending:[]}},"first_year");}catch(e){stopped=/BLOCKED/.test(String(e));}gate("guard companion source repricing cannot silently carry missing source",stopped);
}
fs.writeFileSync(path.join(__dirname,"derived/api_check.json"),JSON.stringify({gate:"G4",pass:true,checks:records.length,records},null,1)+"\n");
console.log(`G4 PASS ${records.length} checks; maxRSS ${process.resourceUsage().maxRSS} KiB`);
