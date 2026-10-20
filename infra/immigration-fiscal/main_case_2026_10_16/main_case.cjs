/* G1, v9 payloads and tables. No upstream file is written. */
"use strict";
const fs=require("fs"),path=require("path"),P=require("./package.cjs"),V=P.V8_PACKAGE;
const HERE=__dirname,OLD=path.join(HERE,"../main_case_2026_10_15/derived");
const args=process.argv.slice(2),OUT=path.resolve(args.includes("--out-dir")?args[args.indexOf("--out-dir")+1]:path.join(HERE,"derived"));
const BASE_ONLY=args.includes("--base-only"),started=performance.now();
let phaseStarted=started;
const phase=name=>{const now=performance.now();console.log(`[TIMING] previous_phase_seconds=${((now-phaseStarted)/1000).toFixed(3)}; next=${name}`);phaseStarted=now;};
const clone=x=>JSON.parse(JSON.stringify(x)),sum=a=>a.reduce((x,y)=>x+y,0),mean=a=>sum(a)/a.length;
const read=f=>JSON.parse(fs.readFileSync(path.join(OLD,f),"utf8"));
const checks=[],near=(a,b,e=1e-9)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=e;
const gate=(name,ok,details=null)=>{checks.push({name,pass:!!ok,details});if(!ok)throw Error("[BLOCKED] G1 "+name+" "+JSON.stringify(details));};
const write=(file,x)=>fs.writeFileSync(path.join(OUT,file),typeof x==="string"?x:JSON.stringify(x,null,1)+"\n");
const csv=rows=>rows.map(row=>row.map(x=>{const s=String(x??"");return /[",\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;}).join(",")).join("\n")+"\n";
function parse(text){return text.trimEnd().split("\n").map(line=>{const r=[];let s="",q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){s+='"';i++;}else q=!q;}else if(c===","&&!q){r.push(s);s="";}else s+=c;}r.push(s);return r;});}
function run(Q,which="set",o={},all=false,rule=null){
 const X=which==="cash"?Q.CASH:Q,ss=X.specsFor(all?{...o,allocation:"all"}:o),numbered=X.specsFor({...o,allocation:"all"});
 const models=P.METHODS.map(method=>X.modelFor("central",method,X.withCentral(o)));
 const runs=models.map(m=>ss.map(s=>rule?require("./companions.cjs").adjustedRun(X,m,s,rule):X.evaluateFull(m,s,o.profile)));
 const costs=runs.map(a=>a.map(r=>r.cost_bn)),indexes=costs.map(a=>[a.indexOf(Math.min(...a)),a.indexOf(Math.max(...a))]);
 const ends=indexes.map(ix=>ix.map(i=>numbered.findIndex(s=>JSON.stringify(s)===JSON.stringify(ss[i]))));
 gate("valid "+which+" end specification numbers",ends.every(a=>a.every(i=>i>=0&&i<64)));
 return {specs:ss,models,runs,costs,indexes,band:[0,1].map(e=>mean(costs.map((a,k)=>a[indexes[k][e]]))),ends};
}
fs.mkdirSync(OUT,{recursive:true});
phase("G1 source controls");
const payload=P.correctionsPayload(),cashPayload=P.CASH.correctionsPayload(),old=read("summary.json");
const OFF=P.caseOf(P.OCT05,V.CANDIDATE),base=run(OFF),bc=run(OFF,"cash");
gate("items off v8 payloads exactly",JSON.stringify(OFF.correctionsPayload())===JSON.stringify(read("corrections.json"))&&JSON.stringify(OFF.CASH.correctionsPayload())===JSON.stringify(read("corrections_cash.json")));
gate("items off v8 bands exactly",base.band.every((x,i)=>x===old.v8.band_bn[i])&&bc.band.every((x,i)=>x===old.v8.cash_set_bn[i]));
const oldRows=parse(fs.readFileSync(path.join(OLD,"per_spec.csv"),"utf8")),oldHeader=oldRows.shift();
const oldModels=Object.fromEntries(P.METHODS.map(method=>[method,OFF.modelFor("central",method,OFF.withCentral({}))]));
for(const row of oldRows){const method=row[oldHeader.indexOf("method")],i=+row[oldHeader.indexOf("spec")];gate("v8 per_spec "+method+"/"+i,String(OFF.cost(oldModels[method],OFF.ALL_SPECS[i]))===row[oldHeader.indexOf("cost_bn")]);}
const r=run(P),rc=run(P,"cash"),all=run(P,"set",{},true),allc=run(P,"cash",{},true);
gate("64 specifications retained",P.MAIN_SPECS.length===32&&P.SHARED_SPECS.length===32&&P.ALL_SPECS.length===64);
gate("ends agree across methods",[r,rc].every(x=>x.ends.every(es=>JSON.stringify(es)===JSON.stringify(x.ends[0]))),{set:r.ends,cash:rc.ends});
for(const [which,X,rr]of [["set",P,r],["cash",P.CASH,rc]])for(let i=0;i<rr.specs.length;i++)gate(which+" payload/method mean "+i,near(X.cost(X.payloadModel(),rr.specs[i]),mean(rr.costs.map(a=>a[i]))));
const active=P.NEW_IDS.filter(id=>P.CANDIDATE.includes(id)),changes={},standaloneChanges={},alone={};
for(const id of P.NEW_IDS){
 const Q=P.caseOf(P.OCT05,V.CANDIDATE.concat(id)),a=run(Q),b=run(Q,"cash");
 alone[id]={Q,set:a,cash:b};standaloneChanges[id]={set:a.band.map((v,i)=>v-base.band[i]),cash:b.band.map((v,i)=>v-bc.band[i])};
 if(active.includes(id))changes[id]=standaloneChanges[id];
 for(const [which,X]of [["set",Q],["cash",Q.CASH]])for(const rec of X.V9_ITEMS)for(let j=0;j<rec.edits.count;j++){
  const e=X.correctionsPayload().edits[rec.edits.first+j],parts=Object.values(rec.parts||{}).filter(p=>p.edit===j);
  gate(id+"/"+which+" edit "+j+" parts",parts.length>0&&["personal","shared"].every(a=>near(sum(parts.map(p=>p.by[a])),e.by[a])));
 }
}
const spend=JSON.parse(fs.readFileSync(path.join(HERE,"../spending_keys_r5_2026_10_15/derived/case_changes.json"),"utf8"));
for(const row of spend.rows.filter(x=>[13,14,15,21].includes(x.item)&&x.arm===(x.item===13&&P.STUB13?"compensation_only":"central"))){const i=row.end==="low"?0:1;gate("source item"+row.item+" "+row.which+"/"+row.end,near(changes[row.id][row.which][i],row.change_bn,1e-6),{actual:changes[row.id][row.which][i],expected:row.change_bn});}
const health=JSON.parse(fs.readFileSync(path.join(HERE,"../spending_keys_r5_2026_10_15/derived/item21_case_changes.json"),"utf8"));
for(const which of ["set","cash"])for(const [i,end]of ["low","high"].entries()){
 const row=health.rows.find(x=>x.case==="standalone_v8"&&x.which===which&&x.end===end&&x.arm==="central");
 gate("source item21 explicit oracle "+which+"/"+end,row&&near(changes.health_residual_key[which][i],row.change_bn,1e-6),row);
}
const counts=JSON.parse(fs.readFileSync(path.join(HERE,"../count_composition_r5_2026_10_15/derived/items.json"),"utf8"));
for(const which of ["set","cash"])for(const [id,key]of [["native_minor_calibration","item16"],["coverage_tenure","item17"]])for(const [i,e]of ["low","high"].entries())gate("source "+id+" "+which+"/"+e,near(changes[id][which][i],counts.sets[which][key].by_end[e].total_bn,1e-6));
const joint=P.caseOf(P.OCT05,V.CANDIDATE.concat(["native_minor_calibration","coverage_tenure"]));
for(const which of ["set","cash"]){const out=run(joint,which).band,bb=which==="set"?base.band:bc.band;for(const [i,e]of ["low","high"].entries())gate("source16+17 joint "+which+"/"+e,near(out[i]-bb[i],counts.sets[which].joint.by_end[e].total_bn,1e-6));}
for(const which of ["set","cash"])for(let i=0;i<2;i++){
 gate("source18 "+which+"/"+i,near(changes.consumption_tax_bases[which][i],.263314888,1e-6));
 gate("source19 beside oracle "+which+"/"+i,near(standaloneChanges.passthrough_source_tax[which][i],[-3.368256915,-.673876887][i],1e-6));
 const want=which==="set"?[367.375434,436.282039]:[283.336067,352.242672];
 gate("source20 armB "+which+"/"+i,near(alone.one_rate[which].band[i],want[i],1e-6));
}
const interactions={total:{},pairs:{},higher_order:{}};
for(const which of ["set","cash"]){const b=which==="set"?base.band:bc.band,full=which==="set"?r.band:rc.band;interactions.total[which]=full.map((v,i)=>v-b[i]-sum(active.map(id=>changes[id][which][i])));}
phase("exact pair interactions");
for(let i=0;i<active.length;i++)for(let j=i+1;j<active.length;j++){
 const ids=[active[i],active[j]],Q=P.caseOf(P.OCT05,V.CANDIDATE.concat(ids)),out={};
 for(const which of ["set","cash"]){const band=run(Q,which).band,b=which==="set"?base.band:bc.band;out[which]=band.map((v,e)=>v-b[e]-sum(ids.map(id=>changes[id][which][e])));}
 interactions.pairs[ids.join("+")]=out;
}
for(const which of ["set","cash"])interactions.higher_order[which]=interactions.total[which].map((v,e)=>v-sum(Object.values(interactions.pairs).map(p=>p[which][e])));
const own=P.payloadModel(),previous=V.payloadModel();
for(const side of ["spending","receipts"])for(const l of previous[side].lines)gate("national "+side+"/"+l.id,own[side].lines.find(n=>n.id===l.id)?.national_bn===l.national_bn);
const pop=P.POPULATION_V9;
gate("calibrated population",near(pop.with_coverage,counts.population_v8+counts.sets.set.joint.population_change,1e-6),pop);
gate("population parts add to denominator",near(pop.without_coverage+pop.coverage,pop.with_coverage,1e-6),pop);
const companions={},armTransports={},bands={adopted:r.band,cash_set:rc.band,oct15_case:base.band,oct15_cash_set:bc.band};
const remember=(name,Q=P,o={},rule=null)=>{const a=run(Q,"set",o,false,rule),b=run(Q,"cash",o,false,rule);const out={band_bn:a.band,cash_set_bn:b.band,ends:a.ends,cash_ends:b.ends,population:Q.POPULATION_V9||Q.POPULATION_V8,...require("./companions.cjs").coverageLabel(Q,{rule})};companions[name]=out;bands[name]=a.band;bands[name+"_cash_set"]=b.band;return out;};
if(!BASE_ONLY){
 phase("lineage and companion rebuilds");
 for(const name of ["arm_a","arm_c","c3_minus_se","c3_plus_se"]){phase("lineage "+name);remember("lineage_"+name,P.caseOf(P.OCT05,P.CANDIDATE,{},name));}
 remember("shared_allocation",P,{allocation:"shared"},"shared");remember("school_within_district",P,{school_rule:"within_district"},"school");
 const C=require("./companions.cjs"),aset=C.ancestry(P,"set"),acash=C.ancestry(P,"cash");
 for(const a of aset){const c=acash.find(z=>z.scenario===a.scenario);companions["ancestry_share_"+a.scenario]={...a,cash_set_bn:c.band_bn,cash:c};bands["ancestry_share_"+a.scenario]=a.band_bn;bands["ancestry_share_"+a.scenario+"_cash_set"]=c.band_bn;}
 companions.first_year={...C.firstYear(P,"set"),cash:C.firstYear(P,"cash")};bands.first_year_v9=companions.first_year.band_bn;bands.first_year_v9_cash_set=companions.first_year.cash.band_bn;
 for(const [which,row]of [["set",companions.first_year],["cash",companions.first_year.cash]])gate("first-year ends searched in both methods "+which,row.ends.length===P.METHODS.length&&row.ends.every(a=>a.length===2&&a.every(i=>i>=0&&i<P.MAIN_SPECS.length)));
 for(const arm of ["da_middle_0_17","da_middle"]){const Q=P.caseOf(P.OCT05,P.CANDIDATE,{coverage:arm});remember("coverage_"+arm,Q);}
 phase("new-item arms");
 for(const item of P.REGISTRY.filter(x=>P.NEW_IDS.includes(x.id)))for(const arm of Object.keys(item.arms||{})){
  phase("arm "+item.id+"/"+arm);
  const ids=P.REGISTRY.filter(x=>P.CANDIDATE.includes(x.id)||x.id===item.id).map(x=>x.id);
  const Q=P.caseOf(P.OCT05,ids,{[item.id]:arm}),name=item.id+"_"+arm;
  bands[name]=Q.central({});bands[name+"_cash_set"]=Q.CASH.central({});
  armTransports[name]=Q.correctionsPayload().meta.v9_arm_transport||{coverage:"own central kernel; see item-specific rate and source transport metadata",count_items:"central16/17 kernel carried across source arms"};
 }
}
const legalFormPair=BASE_ONLY?null:require("./legal_form_pair.cjs").build(P,{run,gate});
if(legalFormPair)for(const [name,row]of Object.entries(legalFormPair.readings)){bands["item6_legal_form_pair_"+name]=row.set.band_bn;bands["item6_legal_form_pair_"+name+"_cash_set"]=row.cash.band_bn;}
const components=clone(old.components);
if(!BASE_ONLY){phase("inherited range variants");for(const c of P.V4PKG.rangeComponents()){
 phase("range "+c.name);
 const values=Object.fromEntries(c.variants.map(v=>{const o=typeof v.o==="function"?v.o(P.withCentral({})):v.o;const bs=v.methods.map(method=>P.evalPackage(v.caseName,method,o));return [v.v,[0,1].map(e=>mean(bs.map(a=>a[e]))-r.band[e])];}));
 const oldc=components.find(x=>x.name===c.name),next={name:c.name,label:c.label,lo:[0,1].map(e=>Math.min(0,...Object.values(values).map(a=>a[e]))),hi:[0,1].map(e=>Math.max(0,...Object.values(values).map(a=>a[e]))),variants:values};if(oldc)Object.assign(oldc,next);else components.push(next);
}}
const range={...clone(old.range),low_end:[r.band[0]+sum(components.map(c=>c.lo[0])),r.band[0]+sum(components.map(c=>c.hi[0]))],high_end:[r.band[1]+sum(components.map(c=>c.lo[1])),r.band[1]+sum(components.map(c=>c.hi[1]))],note:BASE_ONLY?"Historical v8 component ranges in base-only build":"Inherited variants repriced through v9 dynamic evaluator; source post-item transport documented"};range.overall=[range.low_end[0],range.high_end[1]];
const table=parse(fs.readFileSync(path.join(OLD,"main_case_bands.csv"),"utf8")),head=table.shift(),historicalRows=[];
for(const row of table){const name=row[1],b=bands[name];if(row[0]===P.MAIN_PROFILE&&b){row[2]=b[0].toFixed(4);row[3]=b[1].toFixed(4);if(name==="adopted"){row[4]=BASE_ONLY?"":range.overall[0].toFixed(4);row[5]=BASE_ONLY?"":range.overall[1].toFixed(4);}}else historicalRows.push(row[0]+"/"+name);}
for(const [name,b]of Object.entries(bands))if(!table.some(row=>row[0]===P.MAIN_PROFILE&&row[1]===name))table.push([P.MAIN_PROFILE,name,b[0].toFixed(4),b[1].toFixed(4),"",""]);
head.push("v9_price_scope");
for(const row of table){const key=row[1].replace(/_cash_set$/,""),transport=armTransports[key];row.push(historicalRows.includes(row[0]+"/"+row[1])?"historical v8 row; see summary.v9.historical_rows":transport?JSON.stringify(transport):companions[key]?.coverage||"current v9 central source-kernel prices; see summary.v9");}
const newCols=["oct15_cost_bn",...active.map(id=>"item_"+id+"_bn"),"items_v9_interaction_bn","post_engine_v9_total_bn","effective_capital_rate","population_v9","v9_cost_per_member_usd"];
const perRows=oldRows.map(row=>{
 const method=row[oldHeader.indexOf("method")],mi=P.METHODS.indexOf(method),i=+row[oldHeader.indexOf("spec")],s=P.ALL_SPECS[i],rr=all.runs[mi][i],oldCost=+row[oldHeader.indexOf("cost_bn")];
 const vals={cost_bn:rr.cost_bn,engine_cost_bn:-rr.evaluation.welfare_bn,capital_total_bn:rr.capital.total_bn};
 for(const c of rr.capital.components)vals["capital_"+c.id+"_bn"]=c.return_bn;
 for(const l of rr.evaluation.spending){vals["response_"+l.id]=l.response;vals["group_"+l.id+"_bn"]=l.amount_bn;}
 for(const [name,pred]of Object.entries({state_local:c=>c.level==="state_local",federal:c=>c.level==="federal",core:c=>c.group==="core",block:c=>c.group==="block",enterprise:c=>c.group==="enterprise"}))vals["capital_"+name+"_bn"]=sum(rr.capital.components.filter(pred).map(c=>c.return_bn));
 gate("per_spec accounting "+method+"/"+i,near(rr.cost_bn,-rr.evaluation.welfare_bn+rr.capital.total_bn+rr.post_engine.total_bn));
 const ds=active.map(id=>alone[id].Q.cost(alone[id].set.models[mi],alone[id].Q.ALL_SPECS[i])-oldCost);
 return oldHeader.map((h,j)=>h in vals?String(vals[h]):row[j]).concat([oldCost,...ds,rr.cost_bn-oldCost-sum(ds),rr.v9_post_engine.total_bn,P.RATE.rateFor(P.POST_ENGINE.one_rate,s),pop.with_coverage,rr.cost_bn*1e9/pop.with_coverage]);
});
const summary=clone(old);Object.assign(summary,{lane:P.LANE,decision:P.DECISION,main_case:r.band,cash_set:{...old.cash_set,band_bn:rc.band},components,range});
summary.v9={status:P.STATUS,adopted:P.ADOPTED,stub13:P.STUB13,item19_central:P.ITEM19==="1",selected_items:P.CANDIDATE,beside:{item6_legal_form_pair:legalFormPair,item19_standalone_on_v8:standaloneChanges.passthrough_source_tax},coverage_mode:P.COVERAGE_MODE,case_key:P.CASE_KEY,base:"oct15",band_bn:r.band,cash_set_bn:rc.band,end_specifications:{set:r.ends,cash:rc.ends},population:pop,per_member_usd:{set:r.band.map(v=>v*1e9/pop.with_coverage),cash:rc.band.map(v=>v*1e9/pop.with_coverage)},per_member_without_coverage_people_usd:{set:r.band.map(v=>v*1e9/pop.without_coverage),cash:rc.band.map(v=>v*1e9/pop.without_coverage)},change_by_item:changes,interactions,companions,arm_transports:armTransports,item_parts:{set:P.V9_ITEMS,cash:P.CASH.V9_ITEMS},coverage:payload.meta.coverage,one_rate:payload.meta.one_rate,historical_rows:historicalRows,historical_keys:"v4-v8 blocks remain historical; current whole-case results are in v9; retained old band rows are identified above",base_only:BASE_ONLY};
gate("item changes plus interactions close",["set","cash"].every(which=>[0,1].every(e=>near(sum(active.map(id=>changes[id][which][e]))+interactions.total[which][e],(which==="set"?r.band[e]-base.band[e]:rc.band[e]-bc.band[e])))));
if(P.COVERAGE_MODE==="repriced"){const cov=require("./coverage_integration.cjs");if(cov.check)gate("coverage oct16 source gate",cov.check(P));}
write("summary.json",summary);write("corrections.json",payload);write("corrections_cash.json",cashPayload);write("main_case_bands.csv",csv([head,...table]));write("per_spec.csv",csv([oldHeader.concat(newCols),...perRows]));
const ch=parse(fs.readFileSync(path.join(OLD,"components.csv"),"utf8"))[0];write("components.csv",csv([ch,...components.map(c=>[c.name,c.label,c.lo[0].toFixed(4),c.hi[0].toFixed(4),c.lo[1].toFixed(4),c.hi[1].toFixed(4)])]));
// Inputs and historical schemas remain inspectable; their byte provenance is explicit.
for(const f of fs.readdirSync(OLD).filter(f=>!fs.existsSync(path.join(OUT,f))&&!['contract.json','generality.json','api_check.json','g1.json','coverage_check.json','sign_reversal.csv','lineage_addition.json'].includes(f)))write(f,fs.readFileSync(path.join(OLD,f),"utf8"));
for(const f of ["lineage_payload.json","lineage_payload_cash.json"]){const x=read(f);x.v9={case_key:P.CASE_KEY,population:pop,new_items:active,corrections:f.includes("cash")?"corrections_cash.json":"corrections.json",rule:"original lineage construction retained as historical; full edits and post amounts in current corrections payload"};write(f,x);}
write("g1.json",{pass:true,stub13:P.STUB13,coverage_mode:P.COVERAGE_MODE,band:r.band,cash:rc.band,changes,interactions,ends:{set:r.ends,cash:rc.ends},checks});
console.log(JSON.stringify({G1:"PASS",stub13:P.STUB13,coverage:P.COVERAGE_MODE,set:r.band,cash:rc.band,population:pop,maxRSS_KiB:process.resourceUsage().maxRSS,elapsed_seconds:(performance.now()-started)/1000}));
require("./memory_guard.cjs").requireWithinBudget("G1 main case");
