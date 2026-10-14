/* G1 and case files. All outputs stay in this lane. */
"use strict";
const fs=require("fs"),path=require("path");
const P=require("./package.cjs"),V=P.V7_PACKAGE;
const COMP=require("./companions.cjs");
const HERE=__dirname,OLD=path.join(HERE,"../main_case_2026_10_14/derived");
const args=process.argv.slice(2),OUT=path.resolve(args.includes("--out-dir")?args[args.indexOf("--out-dir")+1]:path.join(HERE,"derived"));
const BASE_ONLY=args.includes("--base-only");
const clone=x=>JSON.parse(JSON.stringify(x)), read=f=>JSON.parse(fs.readFileSync(path.join(OLD,f),"utf8"));
const mean=xs=>xs.reduce((a,b)=>a+b,0)/xs.length, diff=(a,b)=>a.map((v,i)=>v-b[i]);
const gate=(name,ok,detail="")=>{console.log(`${stub?"[STUB] ":""}${ok?"PASS":"FAIL"} ${name} ${detail}`);if(!ok)throw Error(`[BLOCKED] ${name}`);};
const near=(a,b,e=1e-9)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=e;
const write=(file,x)=>fs.writeFileSync(path.join(OUT,file),typeof x==="string"?x:JSON.stringify(x,null,1)+"\n");
const csv=rows=>rows.map(row=>row.map(x=>{const s=String(x??"");return /[",\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;}).join(",")).join("\n")+"\n";
function parse(text){return text.trimEnd().split("\n").map(line=>{const r=[];let s="",q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){s+='"';i++;}else q=!q;}else if(c===","&&!q){r.push(s);s="";}else s+=c;}r.push(s);return r;});}
function run(Q,which="set",o={},all=false){const X=which==="cash"?Q.CASH:Q,ss=X.specsFor(all?{...o,allocation:"all"}:o),numbered=X.specsFor({...o,allocation:"all"}); const models=P.METHODS.map(method=>X.modelFor("central",method,X.withCentral(o)));
 const rs=models.map(m=>ss.map(s=>X.evaluateFull(m,s,o.profile))),cs=rs.map(xs=>xs.map(r=>r.cost_bn));
 const indexes=cs.map(xs=>[xs.indexOf(Math.min(...xs)),xs.indexOf(Math.max(...xs))]);
 const ends=indexes.map(ix=>ix.map(i=>numbered.findIndex(s=>s.allocation===ss[i].allocation&&s.normalization===ss[i].normalization&&s.share===ss[i].share&&s.school===ss[i].school&&s.reading===ss[i].reading&&s.uc===ss[i].uc)));
 gate(`valid ${which} specification numbers`,ends.every(es=>es.every(i=>i>=0&&i<64)));
 return {specs:ss,models,runs:rs,costs:cs,indexes,band:[0,1].map(e=>mean(cs.map((xs,k)=>xs[indexes[k][e]]))),ends};
}
const payload=P.correctionsPayload(),cashPayload=P.CASH.correctionsPayload();
const stub=!!payload.meta.coverage?.stub;
console.log(`[G1 v8${stub?" STUB coverage":""}]`);
const OFF=P.caseOf(P.OCT05,V.CANDIDATE);
gate("items off: v7 payloads exactly",JSON.stringify(OFF.correctionsPayload())===JSON.stringify(read("corrections.json"))&&JSON.stringify(OFF.CASH.correctionsPayload())===JSON.stringify(read("corrections_cash.json")));
gate("default corporate-response parameter reproduces v7",P.ITEM6_LOW_CORPORATE_RESPONSE===1||process.env.ITEM6_LOW_CORPORATE_RESPONSE!==undefined);
const old=read("summary.json"),r=run(P),rc=run(P,"cash"),base=run(OFF),bc=run(OFF,"cash"),all=run(P,"set",{},true),allc=run(P,"cash",{},true);
gate("items off: v7 set and cash bands exactly",base.band.every((x,i)=>x===old.main_case[i])&&bc.band.every((x,i)=>x===old.cash_set.band_bn[i]));
gate("32 personal, 32 shared, all 64",P.MAIN_SPECS.length===32&&P.SHARED_SPECS.length===32&&P.ALL_SPECS.length===64);
gate("ends found independently in both methods, set and cash",[r,rc].every(x=>x.ends.every(es=>es[0]===x.ends[0][0]&&es[1]===x.ends[0][1])),JSON.stringify({set:r.ends,cash:rc.ends}));
gate("payload model and method mean agree",[P,P.CASH].every((X,k)=>{const z=k?rc:r;return z.specs.every((s,i)=>near(X.cost(X.payloadModel(),s),mean(z.costs.map(xs=>xs[i]))));}));
const oldRows=parse(fs.readFileSync(path.join(OLD,"per_spec.csv"),"utf8")),oldHeader=oldRows.shift();
const oldModels=Object.fromEntries(P.METHODS.map(method=>[method,OFF.modelFor("central",method,OFF.withCentral({}))]));
for(const row of oldRows){const method=row[oldHeader.indexOf("method")],spec=+row[oldHeader.indexOf("spec")];gate(`v7 per_spec ${method}/${spec}`,String(OFF.cost(oldModels[method],OFF.ALL_SPECS[spec]))===row[oldHeader.indexOf("cost_bn")]);}
const active=P.NEW_IDS.filter(id=>P.CANDIDATE.includes(id)),changes={},alone={};
for(const id of active){const Q=P.caseOf(P.OCT05,V.CANDIDATE.concat([id]));const a=run(Q),ac=run(Q,"cash");alone[id]={Q,set:a,cash:ac}; changes[id]={set:diff(a.band,base.band),cash:diff(ac.band,bc.band)};
 for(const which of ["set","cash"]){const X=which==="set"?Q:Q.CASH;for(const rec of X.V8_ITEMS){for(let j=0;j<rec.edits.count;j++){const e=X.V8_EDITS[j],ps=Object.values(rec.parts||{}).filter(p=>p.edit===j);if(ps.length)gate(`${id}/${which} edit ${j} parts close`,["personal","shared"].every(a=>near(ps.reduce((s,p)=>s+p.by[a],0),e.by[a])));}}}
}
if(alone.foreign_source_tax){const source=P.readJson(P.FOREIGN.SOURCE).arms.K2_foreign_source_removed;for(const [i,end] of ["low","high"].entries()){gate(`item9 K2 ${end} lineage exact`,near(changes.foreign_source_tax.set[i],source[end].lineage.delta_net_cost_bn,1e-6));const Q=alone.foreign_source_tax.Q,s=Q.MAIN_SPECS[[16,11][i]],parts=COMP.partsAt(Q,"set",s,Q.evaluateFull(Q.payloadModel(),s));gate(`item9 K2 ${end} union exact`,near(parts.G1+parts.G2+parts.G3plus,source[end].union.delta_net_cost_bn,1e-6));}}
if(P.CANDIDATE.includes("foreign_source_tax")){for(const keepItem9 of [true,false]){const ids=keepItem9?P.CANDIDATE:P.CANDIDATE.filter(id=>id!=="foreign_source_tax"),Q=P.caseOf(P.OCT05,ids,{job_capital_taxes:"foreign_source_removed"});for(const which of ["set","cash"]){const got=run(Q,which).band,want=which==="set"?r.band:rc.band;gate(`domestic-source removal commutes ${which} item9=${keepItem9}`,got.every((n,i)=>near(n,want[i])));}}}
if(alone.mixed_unit_removal) for(const [i,end] of ["low","high"].entries())for(const which of ["set","cash"]){const want=P.MIXED.get(null,which)[end];gate(`item11 ${which}/${end} exact`,near(changes.mixed_unit_removal[which][i],want,1e-6));}
const item10=payload.meta.union_completion;
if(item10){for(const [which,want] of [["set",[2.893,3.755]],["cash",[2.031,2.893]]])for(let i=0;i<2;i++){gate(`item10 ${which}/${i} source printed precision`,Math.abs(changes.union_completion[which][i]-want[i])<0.0006,changes.union_completion[which][i].toFixed(6));const X=which==="set"?alone.union_completion.Q:alone.union_completion.Q.CASH;gate(`item10 ${which}/${i} exact source file`,near(changes.union_completion[which][i],X.correctionsPayload().meta.union_completion.source_delta_bn[i].estimate,1e-6));}gate("item10 exact 5b interaction",near(item10.credit_interaction_bn,require("./item_union.cjs").CREDIT.results.one_us_parent_plus_observed.delta_bn,1e-12));}
if(payload.meta.coverage){console.log(`${stub?"[STUB] ":""}coverage source ${payload.meta.coverage.file}`);for(const which of ["set","cash"]){const X=which==="set"?P:P.CASH,c=X.POST_ENGINE.coverage;gate(`${stub?"[STUB] ":""}coverage ${which} source/generation closure`,["low","high"].every(e=>near(Object.values(c.by_end[e].by_generation).reduce((a,b)=>a+b,0),c.by_end[e].total_bn)));}}
if(payload.meta.coverage&&!stub){
 // The coverage lane pinned the candidate's base. Adoption changes only the stamp (meta.adopted, status, case), so the
 // pin reads an adopted base's stamp back to the candidate form; any other difference still fails the pin.
 const code='const P=require(process.argv[1]),c=require("crypto"); const neutral=X=>{const pl=X.correctionsPayload(),m=pl.meta;if(m.adopted!==null){if(!m.status.startsWith("adopted: ")||!m.case.endsWith("; v8 adopted"))throw Error("unexpected adopted stamp");m.adopted=null;m.status="candidate"+m.status.slice(7);m.case=m.case.slice(0,-7)+"candidate";}return pl;}; const sha=X=>c.createHash("sha256").update(JSON.stringify(neutral(X),null,1)+"\\n").digest("hex"); console.log(JSON.stringify({set:sha(P),cash:sha(P.CASH),maxRSS:process.resourceUsage().maxRSS}));';
 const child=require("child_process").spawnSync(process.execPath,["-e",code,path.join(HERE,"package.cjs")],{env:{...process.env,COVERAGE:"0"},encoding:"utf8",maxBuffer:1024*1024});
 gate("live coverage base reconstruction exits cleanly",child.status===0,child.stderr||"");
 const hashes=JSON.parse(child.stdout);gate("coverage base reconstruction memory budget",hashes.maxRSS*1024<2.5e9);
 for(const which of ["set","cash"]){const c=(which==="set"?P:P.CASH).POST_ENGINE.coverage,rr=which==="set"?r:rc;gate(`live coverage ${which} pins the current base payload`,c.base_payload_sha256_by_set?.[which]===hashes[which]);gate(`live coverage ${which} source case totals close`,["low","high"].every((e,i)=>near(c.by_end[e].source_case_with_coverage_bn,rr.band[i])));}
}
const own=P.payloadModel(),before=V.payloadModel();for(const side of ["spending","receipts"])for(const l of before[side].lines){const n=own[side].lines.find(x=>x.id===l.id);gate(`national ${side}/${l.id} holds`,n&&n.national_bn===l.national_bn);}
const interaction={}; for(const which of ["set","cash"]){const full=which==="set"?r:rc,bb=which==="set"?base:bc;interaction[which]=diff(diff(full.band,bb.band),[0,1].map(i=>active.reduce((s,id)=>s+changes[id][which][i],0)));}
const pairs={};for(let i=0;i<active.length;i++)for(let j=i+1;j<active.length;j++){const ids=[active[i],active[j]],Q=P.caseOf(P.OCT05,V.CANDIDATE.concat(ids));pairs[ids.join("+")]={};for(const which of ["set","cash"]){const b=run(Q,which).band,bb=which==="set"?base.band:bc.band;pairs[ids.join("+")][which]=diff(diff(b,bb),[0,1].map(e=>ids.reduce((s,id)=>s+changes[id][which][e],0)));}}
const pop=P.POPULATION_V8;gate("new people used in all per-member figures",pop.without_coverage>42752212&&pop.with_coverage>=pop.without_coverage,JSON.stringify(pop));
const companions={},bands={};const remember=(name,Q=P,o={})=>{const a=run(Q,"set",o),b=run(Q,"cash",o);const out={band_bn:a.band,cash_set_bn:b.band,ends:a.ends,cash_ends:b.ends,coverage:"carried from central prices",item11:"unchanged except D_added_residual scaled with option added-G3 count",population:Q.POPULATION_V8,per_member_usd:a.band.map(v=>v*1e9/Q.POPULATION_V8.with_coverage)};companions[name]=out;bands[name]=a.band;bands[name+"_cash_set"]=b.band;return out;};
if(!BASE_ONLY){for(const name of ["arm_a","arm_c","c3_minus_se","c3_plus_se"]){console.log(`[PHASE] lineage ${name}`);const Q=P.caseOf(P.OCT05,P.CANDIDATE,{},name);remember(`lineage_${name}`,Q);}
remember("shared_allocation",P,{allocation:"shared"});remember("school_within_district",P,{school_rule:"within_district"});}
const options={without_capital_return:{capital:false},school_within_district_as_response:{school_rule:"within_district_as_response"},enterprises_out_option_a:{enterprises:"A"},enterprise_receipt_at_model_json_share:{enterprise_rekey:false},capital_return_at_7pct:{rates:{low:P.RATES.reported,high:P.RATES.reported}},rental_assistance_at_0:{rental:0},k12_capital_at_pupil_share:{capital_variant:"k12_at_pupil_share"},audit_row3_instead_of_cbo_income_tax:{incomeTax:"row3",tax_key:"cbo_2022"}};
if(!BASE_ONLY)for(const [name,o] of Object.entries(options)){console.log(`[PHASE] option ${name}`);bands[name]=P.central(o);}
if(BASE_ONLY)bands.without_capital_return=P.central({capital:false});
bands.general_government_fixed=P.mean2(...P.METHODS.map(method=>{const m=P.modelFor("central",method,P.withCentral({}));return P.bandFor(m,null,P.MAIN_SPECS.map(s=>({...s,gg:0})));}));
bands.no_fill_in_correction=P.evalPackage("central","audit_rules_alone",{});bands.adopted=r.band;bands.cash_set=rc.band;
for(const [id,x] of Object.entries(alone)){bands[id+"_alone"]=x.set.band;bands[id+"_alone_cash_set"]=x.cash.band;}
if(!BASE_ONLY)for(const item of P.REGISTRY){for(const arm of Object.keys(item.arms||{})){if(item.id==="coverage"&& !P.CANDIDATE.includes("coverage"))continue;console.log(`${stub?"[STUB] ":""}[PHASE] item arm ${item.id}/${arm}`);if(item.id==="mixed_unit_removal"&&arm==="bounded_high_plus_pension_model"){const z=P.MIXED.get(null,"set",arm);bands[`${item.id}_${arm}`]=[0,1].map(i=>r.band[i]+z[["low","high"][i]]-P.POST_ENGINE.mixed_unit_removal[["low","high"][i]]);continue;}const Q=P.caseOf(P.OCT05,P.CANDIDATE,{[item.id]:arm});bands[`${item.id}_${arm}`]=Q.central({});bands[`${item.id}_${arm}_cash_set`]=Q.CASH.central({});}}
let components=clone(old.components),range=clone(old.range);
if(!BASE_ONLY){
 console.log("[PHASE] ancestry and first-year companions");const aset=COMP.ancestry(P,"set"),acash=COMP.ancestry(P,"cash");
 for(const a of aset){const c=acash.find(x=>x.scenario===a.scenario),name=`ancestry_share_${a.scenario}`;companions[name]={...a,cash_set_bn:c.band_bn,cash:c};bands[name]=a.band_bn;bands[name+"_cash_set"]=c.band_bn;}
 companions.first_year={...COMP.firstYear(P,"set"),cash:COMP.firstYear(P,"cash")};bands.first_year_v8=companions.first_year.band_bn;bands.first_year_v8_cash_set=companions.first_year.cash.band_bn;
 components=[];
 for(const c of P.V4PKG.rangeComponents()){console.log(`[PHASE] range ${c.name}`);
   const variants=c.variants.map(v=>({v,o:typeof v.o==="function"?v.o(P.withCentral({})):v.o}));
   if(variants.every(({v,o})=>!Object.keys(o).length&&v.caseName==="central"&&v.methods.length===P.METHODS.length))continue;
   const values=Object.fromEntries(variants.map(({v,o})=>{const bs=v.methods.map(method=>P.evalPackage(v.caseName,method,o));const b=[0,1].map(e=>mean(bs.map(a=>a[e])));return [v.v,diff(b,r.band)];}));
   const lo=[0,1].map(e=>Math.min(0,...Object.values(values).map(x=>x[e]))),hi=[0,1].map(e=>Math.max(0,...Object.values(values).map(x=>x[e])));
   components.push({name:c.name,label:c.label,lo,hi,variants:values});
 }
 const low=[0,1].map(e=>r.band[e]+components.reduce((t,c)=>t+c.lo[e],0)),high=[0,1].map(e=>r.band[e]+components.reduce((t,c)=>t+c.hi[e],0));
 range={...range,low_end:[low[0],high[0]],high_end:[low[1],high[1]],overall:[low[0],high[1]],quadrature:[r.band[0]-Math.sqrt(components.reduce((t,c)=>t+c.lo[0]**2,0)),r.band[1]+Math.sqrt(components.reduce((t,c)=>t+c.hi[1]**2,0))],note:"v8 reruns every inherited range variant; coverage and bounded mixed-unit source dollars carried as stated. Reporter capital/production use declared source-endpoint transport; observed children use native cells and production."};
}
// Keep v7's input-only and historical rows; every retained row's provenance is explicit below.
const table=parse(fs.readFileSync(path.join(OLD,"main_case_bands.csv"),"utf8")),header=table.shift(),historicalRows=[];
for(const row of table){const name=row[1];let b=bands[name];if(row[0]!==P.MAIN_PROFILE){if(name==="adopted"||name==="with_rental_assistance_capital_and_enterprises")b=P.central({profile:row[0]});else b=null;}if(b){row[2]=b[0].toFixed(4);row[3]=b[1].toFixed(4);if(name==="adopted"){row[4]=BASE_ONLY?"":range.overall[0].toFixed(4);row[5]=BASE_ONLY?"":range.overall[1].toFixed(4);}}else historicalRows.push(`${row[0]}/${name}`);}
for(const [name,b] of Object.entries(bands))if(!table.some(row=>row[0]===P.MAIN_PROFILE&&row[1]===name))table.push([P.MAIN_PROFILE,name,b[0].toFixed(4),b[1].toFixed(4),"",""]);
table.push([P.MAIN_PROFILE,"oct14_case",...base.band.map(x=>x.toFixed(4)),"",""] ,[P.MAIN_PROFILE,"oct14_cash_set",...bc.band.map(x=>x.toFixed(4)),"",""]);
const newCols=["oct14_cost_bn",...active.map(id=>`item_${id}_bn`),"items_v8_interaction_bn","post_engine_mixed_unit_removal_bn","post_engine_coverage_bn","post_engine_total_bn","production_private_wtp_bn","production_induced_receipts_bn"];
const perRows=oldRows.map(row=>{const method=row[oldHeader.indexOf("method")],mi=P.METHODS.indexOf(method),i=+row[oldHeader.indexOf("spec")];const oldCost=+row[oldHeader.indexOf("cost_bn")],rr=all.runs[mi][i],cost=rr.cost_bn;
 const capital=pred=>rr.capital.components.filter(pred).reduce((t,c)=>t+c.return_bn,0),vals={cost_bn:cost,engine_cost_bn:-rr.evaluation.welfare_bn,capital_total_bn:rr.capital.total_bn,capital_state_local_bn:capital(c=>c.level==="state_local"),capital_federal_bn:capital(c=>c.level==="federal"),capital_core_bn:capital(c=>c.group==="core"),capital_block_bn:capital(c=>c.group==="block"),capital_enterprise_bn:capital(c=>c.group==="enterprise")};
 for(const c of rr.capital.components)vals[`capital_${c.id}_bn`]=c.return_bn;
 const es=rr.evaluation.receipts.find(l=>l.id===P.ENTERPRISE_LINE);vals.response_receipt_enterprise_surplus=es.response;vals.group_enterprise_surplus_bn=es.amount_bn;vals.enterprise_surplus_receipt_cost_bn=-es.effect_bn;
 for(const l of rr.evaluation.spending){vals[`response_${l.id}`]=l.response;vals[`group_${l.id}_bn`]=l.amount_bn;}
 row=oldHeader.map((h,j)=>h in vals?String(vals[h]):row[j]);
 gate(`per_spec accounting ${method}/${i}`,near(cost,vals.engine_cost_bn+vals.capital_total_bn+rr.post_engine.total_bn));
 const ds=active.map(id=>{const x=alone[id],X=x.Q;return X.cost(x.set.models[mi],X.ALL_SPECS[i])-oldCost;});return row.concat([oldCost,...ds,cost-oldCost-ds.reduce((a,b)=>a+b,0),rr.post_engine.mixed_unit_removal_bn,rr.post_engine.coverage_bn,rr.post_engine.total_bn,rr.evaluation.private_wtp_bn,rr.evaluation.induced_receipts_bn]);});
const summary=clone(old);Object.assign(summary,{lane:P.LANE,decision:P.DECISION,main_case:r.band,without_capital_return:bands.without_capital_return,cash_set:{...old.cash_set,band_bn:rc.band},responses:payload.meta.responses});
summary.components=components;summary.range=range;
summary.end_specifications=P.METHODS.map((method,k)=>({method,low_end:{index:r.ends[k][0],...r.specs[r.indexes[k][0]]},high_end:{index:r.ends[k][1],...r.specs[r.indexes[k][1]]}}));
const atEnds=f=>[0,1].map(e=>mean(r.runs.map((rs,k)=>f(rs[r.indexes[k][e]]))));
for(const [id,x] of Object.entries(summary.lines_at_end_specifications)){x.response=atEnds(z=>z.evaluation.spending.find(l=>l.id===id).response);x.group_amount_bn=atEnds(z=>z.evaluation.spending.find(l=>l.id===id).amount_bn);x.added_bn=atEnds(z=>{const l=z.evaluation.spending.find(l=>l.id===id);return l.response*l.amount_bn;});}
for(const [id,x] of Object.entries(summary.receipts_at_end_specifications)){x.response=atEnds(z=>z.evaluation.receipts.find(l=>l.id===id).response);x.group_amount_bn=atEnds(z=>z.evaluation.receipts.find(l=>l.id===id).amount_bn);x.effect_bn=atEnds(z=>z.evaluation.receipts.find(l=>l.id===id).effect_bn);}
summary.capital_at_end_specifications.total_bn=atEnds(z=>z.capital.total_bn);
const capEnds=summary.capital_at_end_specifications;
for(const level of Object.keys(capEnds.by_level_bn))capEnds.by_level_bn[level]=atEnds(z=>z.capital.components.filter(c=>c.level===level).reduce((t,c)=>t+c.return_bn,0));
for(const part of Object.keys(capEnds.by_part_bn))capEnds.by_part_bn[part]=atEnds(z=>z.capital.components.filter(c=>c.group===part).reduce((t,c)=>t+c.return_bn,0));
for(const [id,c] of Object.entries(capEnds.by_component))for(const field of ["key","response","return_bn"])c[field]=atEnds(z=>{const current=z.capital.components.find(x=>x.id===id);if(!current)throw Error(`[BLOCKED] missing capital summary component ${id}`);return current[field];});
capEnds.k12_key.account_key=atEnds(z=>z.capital.components.filter(c=>["k12","k12_user_fees"].includes(c.id)).reduce((t,c)=>t+c.key,0));
capEnds.k12_key.pupil_share_minus_account_bn=capEnds.k12_key.account_key.map((key,e)=>capEnds.by_component.k12.stock_charged_bn*[P.RATES.low,P.RATES.high][e]*(capEnds.k12_key.pupil_share-key));
for(const field of ["by_level_bn","by_part_bn"])gate(`capital summary ${field} closes`,[0,1].every(e=>near(Object.values(capEnds[field]).reduce((t,a)=>t+a[e],0),capEnds.total_bn[e])));
gate("capital summary components close",[0,1].every(e=>near(Object.values(capEnds.by_component).reduce((t,c)=>t+c.return_bn[e],0),capEnds.total_bn[e])));
summary.group_receipts_bn.adopted=Object.fromEntries(["personal","shared"].map(a=>[a,own.receipts.lines.reduce((t,l)=>t+l.cells[own.receipts.reference][a].target_bn,0)]));
summary.v8={status:P.STATUS,stub,case_key:P.CASE_KEY,base:"oct14",band_bn:r.band,cash_set_bn:rc.band,end_specifications:{set:r.ends,cash:rc.ends},population:pop,per_member_usd:{set:r.band.map(v=>v*1e9/pop.with_coverage),cash:rc.band.map(v=>v*1e9/pop.with_coverage)},per_member_without_coverage_people_usd:{set:r.band.map(v=>v*1e9/pop.without_coverage),cash:rc.band.map(v=>v*1e9/pop.without_coverage)},change_by_item:changes,interactions:{total:interaction,pairs},companions,item_parts:{set:P.V8_ITEMS,cash:P.CASH.V8_ITEMS},coverage:payload.meta.coverage||null,mixed_unit_removal:payload.meta.mixed_unit_removal||null,union_completion:item10||null,historical_rows:historicalRows,historical_keys:"v4-v7 blocks and all top-level keys not explicitly recomputed remain historical v7 records; read v8 for candidate quantities",ITEM6_LOW_CORPORATE_RESPONSE:P.ITEM6_LOW_CORPORATE_RESPONSE};
gate("reported item deltas plus interactions close the case",["set","cash"].every(which=>[0,1].every(e=>near(active.reduce((s,id)=>s+changes[id][which][e],0)+interaction[which][e],(which==="set"?r.band[e]-base.band[e]:rc.band[e]-bc.band[e])))));
fs.mkdirSync(OUT,{recursive:true});write("summary.json",summary);write("corrections.json",payload);write("corrections_cash.json",cashPayload);write("main_case_bands.csv",csv([header,...table]));write("per_spec.csv",csv([oldHeader.concat(newCols),...perRows]));
for(const f of ["lineage_payload.json","lineage_payload_cash.json"])write(f,fs.readFileSync(path.join(OLD,f),"utf8"));
const ch=parse(fs.readFileSync(path.join(OLD,"components.csv"),"utf8"))[0];write("components.csv",csv([ch,...components.map(c=>[c.name,c.label,c.lo[0].toFixed(4),c.hi[0].toFixed(4),c.lo[1].toFixed(4),c.hi[1].toFixed(4)])]));
write("g1.json",{pass:true,stub,band:r.band,cash:rc.band,changes,interactions:interaction,ends:{set:r.ends,cash:rc.ends}});
console.log(`${stub?"[STUB] ":""}v8 ${r.band.join(" / ")}; cash ${rc.band.join(" / ")}; population ${pop.with_coverage}; maxRSS ${process.resourceUsage().maxRSS} KiB`);
console.log("all gates passed");
