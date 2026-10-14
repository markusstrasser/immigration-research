/* oct15: P7 routing retained, followed by exact declared v8 parts. Module only.
 * New post-engine costs are scoped in each generation payload; uncorrected
 * models receive none. Coverage-on costs never reprice the frozen base input. */
"use strict";
const fs=require("fs"),path=require("path");
const V7=require("./v7_split.cjs"), Consumer=require("../main_case_candidate_v4_2026_09_29/consumer.cjs");
const {X}=V7,{Engine,MODEL,ALLOCS,byAlloc,sum,readJson}=X;
const V8_LANE="main_case_2026_10_15", P8=require(`../${V8_LANE}/package.cjs`);
const clone=x=>JSON.parse(JSON.stringify(x));
const blocked=s=>{throw Error(`[BLOCKED] oct15 split: ${s}`);};
const local=p=>JSON.parse(fs.readFileSync(path.join(__dirname,p),"utf8"));
const ROUTES=local("inputs/routing.json");
const GENS=["G1","G2","G3plus"],IDS=["foreign_source_tax","union_completion","mixed_unit_removal","coverage"];
const genValue=(values,g)=>values[g]??values[g==="G3plus"?"G3+":g];
function stringLeaves(value) {
 return typeof value==="string"?[value]:value&&typeof value==="object"?Object.values(value).flatMap(stringLeaves):[];
}
function withStep(m,edits,receiptLines=[]) {
 if(!edits.length&&!receiptLines.length)return m;
 // Engine.applyCorrections overwrites corrections with payload.meta after its
 // clone. Do not clone the 1.4MB provenance object that it immediately discards.
 return Engine.applyCorrections({...m,corrections:{}},{lines:[],receipt_lines:receiptLines,edits,meta:m.corrections});
}
function padSynthetic(api,m) {
 if(!Object.hasOwn(m,"corrections"))return api.withSyntheticLines(m);
 // Padding only creates zero carriers; preserve the caller's complete metadata
 // after padding. Real-model parity tests and independent API costs gate this.
 const out=api.withSyntheticLines({...m,corrections:{}});
 out.corrections=m.corrections;return out;
}
function reporterPopulation(L) {
 const measured=local("inputs/minor_parent_measurement_oct15.json").reporter_assignment_b;
 const source=L.payload.meta.union_completion.observed_records.filter(r=>!r.observed_nonreporter);
 const byId=new Map(source.map(r=>[`${r.PH_SEQ}|${r.PPPOS}`,r]));
 if(byId.size!==source.length||measured.length!==source.length)blocked("reporter parent assignment record coverage");
 const counts=Object.fromEntries(GENS.map(g=>[g,0]));
 for(const r of measured) {
   const id=`${r.PH_SEQ}|${r.PPPOS}`,s=byId.get(id);
   if(!s||s.age!==r.A_AGE||Math.abs(s.people-r.people)>1e-6||r.omega.length!==3||
      r.omega.some(v=>!Number.isFinite(v)||v<0)||Math.abs(sum(r.omega)-1)>1e-12)
     blocked(`reporter parent assignment differs from case record ${id}`);
   GENS.forEach((g,i)=>counts[g]+=r.people*r.omega[i]);byId.delete(id);
 }
 if(byId.size)blocked("unassigned observed reporter");
 return counts;
}
const reporterCache=new Map();
function reporterRoutes(L) {
 if(reporterCache.has(L.set))return reporterCache.get(L.set);
 const file=path.join(__dirname,"..","within_group_distribution_2026_09_29/derived/reporter_b_routes.json");
 if(!fs.existsSync(file))blocked("missing measured reporter parent-driver routes");
 const all=JSON.parse(fs.readFileSync(file,"utf8")),routes=all.sets[L.set].routes;
 if(!all.source_sha256||!Object.keys(all.source_sha256).length)blocked("reporter routes have no declared source hash graph");
 const crypto=require("crypto");
 for(const [rel,sha] of Object.entries(all.source_sha256)) {
   const got=crypto.createHash("sha256").update(fs.readFileSync(path.resolve(__dirname,"..",rel))).digest("hex");
   if(got!==sha)blocked(`stale reporter driver source ${rel}`);
 }
 const it=L.added.find(i=>i.id==="union_completion");
 const expected=Object.entries(it.record.parts).filter(([name,p])=>routeFor(L.set,it,name,p,it.edits[p.edit]).component==="source_part");
 if(JSON.stringify(Object.keys(routes).sort())!==JSON.stringify(expected.map(([name])=>name).sort()))
   blocked("reporter driver routes do not cover exactly the declared parts");
 for(const [name,p] of expected) {
   const r=routes[name],e=it.edits[p.edit];
   if(r.part_edit!==p.edit||r.global_edit!==it.first+p.edit||JSON.stringify(r.by)!==JSON.stringify(p.by)||
      JSON.stringify(r.cell)!==JSON.stringify(Object.fromEntries(Object.entries(e).filter(([k])=>k!=="by"))))
     blocked(`changed reporter driver declaration ${name}`);
   for(const a of ALLOCS) {
     const b=r.allocations[a].by_generation_bn,s=r.allocations[a].generation_shares;
     if(!GENS.every(g=>b[g].length===161&&b[g].every(Number.isFinite)&&s[g].length===161&&s[g].every(Number.isFinite)))
       blocked(`incomplete reporter driver replicate stack ${name}/${a}`);
     for(let i=0;i<161;i++)if(Math.abs(sum(GENS.map(g=>b[g][i]))-p.by[a])>1e-9||Math.abs(sum(GENS.map(g=>s[g][i]))-1)>1e-12||
       GENS.some(g=>Math.abs(b[g][i]-p.by[a]*s[g][i])>1e-9))
       blocked(`nonconserving reporter driver replicate ${name}/${a}/${i}`);
   }
 }
 reporterCache.set(L.set,routes);return routes;
}
function routeFor(set,it,name,p,e) {
 const r=ROUTES.oct15.sets[set]?.[`${it.id}|${name}`];
 if(!r||r.edit!==p.edit||JSON.stringify(r.by)!==JSON.stringify(p.by)||
   JSON.stringify(r.cell)!==JSON.stringify(Object.fromEntries(Object.entries(e).filter(([k])=>k!=="by")))||
   !GENS.includes(r.generation)||!["union","g3","white"].includes(r.kind)) blocked(`unrouted, unknown or changed part ${it.id}|${name}`);
 return r;
}
function loadCase(set) {
 const old=V7.loadCase(set),rel=`${V8_LANE}/derived/corrections${set==="cash"?"_cash":""}.json`;
 const payload=readJson(rel),api=set==="set"?P8:P8.CASH;
 if(JSON.stringify(payload)!==JSON.stringify(api.correctionsPayload())) blocked(`${rel} differs from the case package`);
 const n=old.payload.edits.length,previous=old.records.length;
 if(JSON.stringify(payload.edits.slice(0,n))!==JSON.stringify(old.payload.edits)||
   JSON.stringify(payload.meta.items.slice(0,previous))!==JSON.stringify(old.records)) blocked("v8 changed inherited v7 edits or records");
 if(JSON.stringify(payload.receipt_lines)!==JSON.stringify(old.payload.receipt_lines)) blocked("v8 changed receipt lines without a declared rule");
 if(JSON.stringify(payload.lines.slice(0,old.payload.lines.length))!==JSON.stringify(old.payload.lines)) blocked("v8 changed inherited spending carriers");
 let at=n;const added=[],post=[];
 for(const r of payload.meta.items.slice(previous)) {
   if(!IDS.includes(r.id)||!r.applied||r.edits.first!==at) blocked(`undeclared item ${r.id}`);
   if(r.kind==="post_engine") {
     if(!["mixed_unit_removal","coverage"].includes(r.id)||r.edits.count!==0||Object.keys(r.parts).length) blocked(`unknown post-engine item ${r.id}`);
     const q=payload.meta[r.id]; if(!q||q.stub) blocked(`missing or stub ${r.id}`);
     for(const end of ["low","high"]) {
       const z=q.by_end[end],values=z.by_generation_bn||z.by_generation;
       if(!Number.isFinite(z.total_bn)||!values||!GENS.every(g=>Number.isFinite(genValue(values,g)))||
         Math.abs(sum(GENS.map(g=>genValue(values,g)))-z.total_bn)>1e-9) blocked(`${r.id}/${end} generation closure`);
     }
     post.push(r.id);continue;
   }
   if(r.kind!=="edit_set"||r.edits.count<=0) blocked(`unknown edit item ${r.id}`);
   const it={id:r.id,record:r,first:at,edits:payload.edits.slice(at,at+r.edits.count),receipt_lines:[]};
   added.push(it);at+=r.edits.count;
 }
 if(at!==payload.edits.length) blocked("registry does not cover all edits");
 const routes=ROUTES.oct15;
 const production=payload.meta.union_completion.production_delta;
 const sameDims=(a,b)=>a&&b&&Object.keys(a).length===Object.keys(b).length&&Engine.PRODUCTION_DIMS.every(k=>JSON.stringify(a[k])===JSON.stringify(b[k]));
 if(!production||JSON.stringify(production)!==JSON.stringify(routes.production[set])||production.generation!=="G3plus"||production.population!=="added"||!sameDims(production.dims,old.payload.production.dims)) blocked("undeclared child production delta");
 for(const field of ["private_wtp_bn","induced_receipts_bn"]) if(payload.production[field].some((v,i)=>Math.abs(v-old.payload.production[field][i]-production[field][i])>1e-12)) blocked(`uncovered production change ${field}`);
 const names=added.flatMap(it=>Object.keys(it.record.parts).map(name=>`${it.id}|${name}`)).sort();
 if(JSON.stringify(names)!==JSON.stringify(Object.keys(routes.sets[set]).sort())) blocked("exact declared part coverage differs");
 for(const it of added) for(const [name,p] of Object.entries(it.record.parts)) routeFor(set,it,name,p,it.edits[p.edit]);
 const lines=payload.lines.slice(old.payload.lines.length);
 if(JSON.stringify(lines)!==JSON.stringify(routes.lines[set])) blocked("undeclared new carrier definitions");
 if(JSON.stringify(payload.meta.union_completion.carriers)!==JSON.stringify(routes.carriers[set])) blocked("undeclared carrier selectors");
 return {...old,rel,payload,api,records:payload.meta.items,items:old.items.concat(added),added,post,old,newLines:lines};
}
function layer(L,gens,top,models29,union29,opts={}) {
 if(gens.length!==3||!GENS.every(G=>gens.filter(g=>top[g]===G).length===1)) blocked("v8 layer requires the three aggregate generations; subcells need their own declared split");
 const hit=G=>gens.find(g=>top[g]===G),conv=opts.convention||"a",fixes=new Set(opts.fixes===undefined?V7.FIXES:opts.fixes);
 const parentPath=path.join(__dirname,"inputs/minor_parent_measurement_oct15.json");
 const minorScale=opts.minorScale===undefined?(fs.existsSync(parentPath)?JSON.parse(fs.readFileSync(parentPath,"utf8")).central_share:1):opts.minorScale;
 const lay=V7.layer(L.old,gens,top,models29,union29,{...opts,minorScale}),parts=clone(lay.parts),items=clone(lay.items);
 const native=L.payload.meta.union_completion,delta=native.production_delta;
 const needMinor=conv==="b"&&fixes.has("minors");
 const minor=needMinor?completionMinor(L,opts.nativeG2Counts):null;
 const reporters=needMinor?reporterRoutes(L):null,reporterAdjustments=[];
 for(const g of gens) {
   parts[g].lines=clone(L.newLines);
   parts[g].meta={...clone(L.payload.meta),generation:top[g],case_key:"oct15"};
   for(const id of L.post) for(const end of ["low","high"]) {
     const z=parts[g].meta[id].by_end[end],values=z.by_generation_bn||z.by_generation;
     z.source_total_bn=z.total_bn;
     z.total_bn=genValue(values,top[g]);
     if(z.by_generation_replicates_bn) {
       z.source_replicates_bn=clone(z.replicates_bn);z.source_se_bn=z.se_bn;
       z.replicates_bn=clone(genValue(z.by_generation_replicates_bn,top[g]));
       z.se_bn=genValue(z.by_generation_se_bn,top[g]);
       if(!Number.isFinite(z.se_bn))blocked(`missing scoped ${id} SE ${top[g]}`);
     }
   }
   for(const f of ["private_wtp_bn","induced_receipts_bn"]) {
     if(!parts[g].production) parts[g].production=Object.fromEntries(["private_wtp_bn","induced_receipts_bn"].map(k=>[k,L.dp[k].map(()=>0)]));
     parts[g].production[f]=parts[g].production[f].map((v,i)=>v+(top[g]==="G3plus"?delta[f][i]:0)+
       (needMinor?(top[g]==="G2"?1:top[g]==="G3plus"?-1:0)*minor.production[f][i]:0));
   }
 }
 for(const it of L.added) {
   const rec={id:it.id,first:it.first,count:it.edits.length,edits:[]};
   it.edits.forEach((e,j)=> {
     const pieces=Object.entries(it.record.parts).filter(([,p])=>p.edit===j);
     if(!pieces.length||ALLOCS.some(a=>Math.abs(sum(pieces.map(([,p])=>p.by[a]))-e.by[a])>1e-9)) blocked(`${it.id}/${j} parts do not close`);
     const routed=pieces.map(([name,p])=> {
       const r=routeFor(L.set,it,name,p,e),by=clone(p.by),g=hit(r.generation);
       const bn=Object.fromEntries(gens.map(h=>[h,byAlloc(()=>0)]));bn[g]=clone(by);
       if(it.id==="foreign_source_tax"&&r.kind==="union") {
         // R7: item 6 rekeys convention b's job-capital cells. Transport item 9's
         // foreign fraction on those same generation-specific union amounts.
         const source=V7.P7.ITEM_DETAIL.job_capital_taxes[L.set].new_parts[`${e.line}|${e.scenario}`][`union_${r.generation}`];
         const job=lay.items.find(x=>x.id==="job_capital_taxes").edits.find(x=>x.line===e.line&&x.scenario===e.scenario);
         const own=job.parts.find(x=>x.route?.kind==="union"&&x.route.generation===r.generation);
         if(!own) blocked(`no R7 job-capital owner ${name}`);
         const old=models29[g].receipts.lines.find(l=>l.id===e.line).cells[e.scenario];
         for(const a of ALLOCS) {const amount=old[a].target_bn+own.bn[g][a];
           if(!source[a]&&by[a]) blocked(`zero corporate source ${name}`);
           by[a]=source[a]?by[a]*amount/source[a]:0;bn[g][a]=by[a];}
       }
       if(needMinor&&it.id==="union_completion"&&r.component==="observed_nonreporters") {
         const amounts=minor.cells.get(`${e.side}|${e.line}|${e.scenario||e.key}`);
         if(!amounts) blocked(`missing native minor cell ${name}`);
         for(const a of ALLOCS) {const move=amounts[a];bn[hit("G2")][a]=move;bn[g][a]=by[a]-move;}
       }
       if(reporters&&it.id==="union_completion"&&r.component==="source_part") {
         const profile=reporters[name],replicates=Object.fromEntries(gens.map(h=>[h,byAlloc(a=>profile.allocations[a].by_generation_bn[top[h]])]));
         for(const h of gens)for(const a of ALLOCS)bn[h][a]=replicates[h][a][0];
         reporterAdjustments.push({part:name,edit:clone(e),by_generation:replicates});
       }
       const share=Object.fromEntries(gens.map(h=>[h,byAlloc(a=>by[a]===0?(h===g?1:0):bn[h][a]/by[a])]));
       return {name,rule:"declared",route:r,union_bn:by,bn,share};
     });
     if(ALLOCS.some(a=>Math.abs(sum(routed.map(p=>p.union_bn[a]))-e.by[a])>1e-9)) blocked(`rekeyed ${it.id}/${j} parts do not close`);
     for(const g of gens) {const ed={...clone(e),by:byAlloc(a=>sum(routed.map(p=>p.bn[g][a])))};parts[g].edits.push(ed);parts[g].item_edits.push(ed);}
     rec.edits.push({edit:j,side:e.side,line:e.line,key:e.key,scenario:e.scenario,parts:routed});
   });items.push(rec);
 }
 const stateAdded=fixes.has("state_prices")&&L.payload.meta.coverage&& !L.payload.meta.coverage.stub
   ?addedStateRouting(L,gens,top,models29,parts,items,lay,conv,minorScale):null;
 if(stateAdded)for(const g of gens)parts[g].meta.added_state_price_routing={...clone(stateAdded),generation:top[g]};
 if(reporters)for(const g of gens)parts[g].meta.reporter_parent_routing={generation:top[g],
   source:"within_group_distribution_2026_09_29/derived/reporter_b_routes.json",parts:Object.keys(reporters).length,
   rule:"new reporter minors follow completed observed parent/relative assignments on every declared source driver; original union retains P7 parent vintage"};
 return {...lay,parts,items,added_state_price_routing:stateAdded,reporter_replicate_adjustments:reporterAdjustments};
}

function addedStateRouting(L,gens,top,models29,parts,items,lay,conv,minorScale) {
 // Geography of unobserved descendants is not directly observed. Use G3+'s
 // state weights as the declared proxy, preserve the case total by centering
 // identified and added charges together, and retain all 161 joint indexes.
 const V4=X.V4,S=JSON.parse(fs.readFileSync(path.join(__dirname,"derived/generation_state_indexes.json"),"utf8"));
 const ix=S.conventions[conv],AGE=require("./age_routing.cjs"),byCell=new Map(),populationCells={latent:new Map(),native:new Map()};
 const add=(e,g,by,population="latent")=> {const id=AGE.id(e);
   for(const cells of [byCell,populationCells[population]]) {
     if(!cells.has(id))cells.set(id,Object.fromEntries(gens.map(h=>[h,byAlloc(()=>0)])));
     for(const a of ALLOCS)cells.get(id)[g][a]+=by[a];}
 };
 const hit=G=>gens.find(g=>top[g]===G),age=lay.age_routing;
 for(const e of L.cells) {
   const moved=byAlloc(a=>conv==="b"&&lay.fixes.includes("minors")?age.cells[AGE.id(e)][a].move_minor*minorScale:0);
   add(e,hit("G2"),moved);add(e,hit("G3plus"),byAlloc(a=>e.by[a]-moved[a]));
 }
 for(const it of items) for(const ed of it.edits) for(const p of ed.parts||[]) {
   if(!(p.rule==="lineage" || (p.route && p.route.kind!=="union") || p.route?.component==="observed_nonreporters"))continue;
   const e=L.items.find(x=>x.id===it.id)?.edits[ed.edit];if(!e)blocked(`no state lineage source ${it.id}/${ed.edit}`);
   for(const g of gens)add(e,g,p.bn[g],p.route?.component==="observed_nonreporters"?"native":"latent");
 }
 const changes=[];
 const centered=(charges,added,functionName,factor)=> {
   const den=sum(gens.map(g=>charges[g]+added[g]));if(!den)blocked(`zero added-state charge ${functionName}`);
   return Array.from({length:161},(_,r)=> {
     const oldDen=sum(Object.values(charges));if(!oldDen)blocked(`zero old-state charge ${functionName}`);
     const oldMean=sum(gens.map(g=>charges[g]*ix[functionName][top[g]].replicates[r]))/oldDen;
     const proxy=ix[functionName].G3plus.replicates[r];
     const mean=sum(gens.map(g=>charges[g]*ix[functionName][top[g]].replicates[r]+added[g]*proxy))/den;
     return Object.fromEntries(gens.map(g=>[g,factor*(charges[g]*(oldMean-mean)+added[g]*(proxy-mean))]));
   });
 };
 const apply=(e,reps,sources)=> {
   const gap=Math.max(...Array.from({length:161},(_,r)=>Math.abs(sum(gens.map(g=>reps[g].personal[r])))));
   if(gap>=1e-9)blocked(`nonconserving added state price ${e.line}: ${gap}`);
   const values=Object.fromEntries(gens.map(g=>[g,byAlloc(a=>reps[g][a][0])]));
   for(const g of gens)parts[g].edits.push({...clone(e),by:values[g]});
   lay.state_diagnostics.replicate_adjustments.push({edit:e,by_generation:reps});
   changes.push({cell:AGE.id(e),edit:e,by_generation:values,charge_sources:sources,replicate_closure_gap_bn:gap});
 };
 for(const line of V4.SP_LINES) {
   const rows=V4.SP_SPEND.filter(r=>r.line===line),reps=Object.fromEntries(gens.map(g=>[g,byAlloc(()=>Array(161).fill(0))])),sources=[];
   for(const a of ALLOCS) {
     const source=models29[gens[0]].spending.lines.find(l=>l.id===line),key=V4.SP_KEY[line]||source.preferred_key;
     const charges=Object.fromEntries(gens.map(g=>[g,models29[g].spending.lines.find(l=>l.id===line).keys[key][a].target_bn/source.national_bn]));
     const added=Object.fromEntries(gens.map(g=>[g,(byCell.get(`spending|${line}|${key}`)?.[g][a]||0)/source.national_bn]));
     sources.push({allocation:a,source_cell:`spending|${line}|${key}`,identified_charges:charges,added_charges:added,
       added_charges_by_population:Object.fromEntries(Object.entries(populationCells).map(([name,cells])=>[name,Object.fromEntries(gens.map(g=>[g,(cells.get(`spending|${line}|${key}`)?.[g][a]||0)/source.national_bn]))])),
       functions:rows.map(r=>({function:r.function,sl_amount_bn:Number(r.sl_amount_bn)})),proxy:"G3plus",indexes:"derived/generation_state_indexes.json"});
     for(const row of rows) {const values=centered(charges,added,row.function,Number(row.sl_amount_bn));
       for(const g of gens)for(let r=0;r<161;r++)reps[g][a][r]+=values[r][g];}
   }apply({side:"spending",line:V4.SP_SYN[line],key:"k"},reps,sources);
 }
 for(const line of Object.keys(V4.SP_RECEIPT)) for(const scenario of Object.keys(models29[gens[0]].receipts.lines.find(l=>l.id===line).cells)) {
   const info=V4.SP_RECEIPT[line],reps=Object.fromEntries(gens.map(g=>[g,byAlloc(()=>Array(161).fill(0))])),sources=[];
   for(const a of ALLOCS) {
     const charges=Object.fromEntries(gens.map(g=>[g,models29[g].receipts.lines.find(l=>l.id===line).cells[scenario][a].target_bn/(1+info.factor)]));
     const added=Object.fromEntries(gens.map(g=>[g,(byCell.get(`receipt|${line}|${scenario}`)?.[g][a]||0)/(1+info.factor)]));
     sources.push({allocation:a,source_cell:`receipt|${line}|${scenario}`,identified_charges:charges,added_charges:added,
       added_charges_by_population:Object.fromEntries(Object.entries(populationCells).map(([name,cells])=>[name,Object.fromEntries(gens.map(g=>[g,(cells.get(`receipt|${line}|${scenario}`)?.[g][a]||0)/(1+info.factor)]))])),
       function:line,factor:info.sl_bn/info.national_bn,proxy:"G3plus",indexes:"derived/generation_state_indexes.json"});
     const values=centered(charges,added,line,info.sl_bn/info.national_bn);
     for(const g of gens)reps[g][a]=values.map(v=>v[g]);
   }apply({side:"receipt",line,scenario},reps,sources);
 }
 return {rule:"[ASSUMPTION] G3plus state weights proxy for added geography; joint centering preserves adopted case total",changes,
   credit_limit:"Unobserved descendants lack individual tax-unit/dependent links for R6; age-key lineage credit allocation retained. Observed completion children follow their native source credit projection."};
}
const minorCache=new Map();
function completionMinor(L,override) {
 if(!override&&minorCache.has(L.set))return minorCache.get(L.set);
 const C=L.payload.meta.union_completion;
 const measurement=JSON.parse(fs.readFileSync(path.join(__dirname,"inputs/minor_parent_measurement_oct15.json"),"utf8"));
 const observed=measurement.native_observed_children;
 const counts=Object.fromEntries(["g3_rate","later"].map(kind=>[kind,observed.by_rate_class[kind].by_age_band.map((b,i)=> {
   const n=override?.[kind]?.[i] ?? b.g2_equivalents.estimate;
   if(!Number.isFinite(n)||n<0||n>b.persons.estimate+1e-9)blocked(`invalid native ${kind} G2 count at band ${i}`);
   return n;
 })]));
 if(Math.abs(observed.persons.estimate-sum(C.nonreporter_age_counts.g3_rate)-sum(C.nonreporter_age_counts.later))>1e-6)
   blocked("native minor parent measurement/source count mismatch");
 if(C.observed_records.some(r=>r.observed_nonreporter&&r.age>=18)) blocked("native completion minor route requires observed children only");
 const bundle=require("../main_case_2026_10_15/item_union.cjs").optionRates(P8.OCT14,{foreign_source_tax:true},true);
 if(!bundle.unit_models||bundle.unit_models.length!==17) blocked("native minor split lacks 17 source unit bands");
 const cells=new Map(),production=Object.fromEntries(["private_wtp_bn","induced_receipts_bn"].map(f=>[f,C.production_delta[f].map(()=>0)]));
 for(let b=0;b<17;b++) for(const [kind,n] of [["g3",(1-C.c3)*counts.g3_rate[b]+counts.later[b]],["white",C.c3*counts.g3_rate[b]]]) {
   const m=bundle.unit_models[b][kind][L.set];
   for(const side of ["spending","receipt"]) for(const l of m[side==="spending"?"spending":"receipts"].lines) for(const [key,cs] of Object.entries(side==="spending"?l.keys:l.cells)) {
     const id=`${side}|${l.id}|${key}`;if(!cells.has(id))cells.set(id,byAlloc(()=>0));
     for(const a of ALLOCS)cells.get(id)[a]+=n*cs[a].target_bn;
   }
   for(const f of Object.keys(production)) for(let i=0;i<production[f].length;i++)production[f][i]+=n*m.production[f][i];
 }
 const p=L.old.payload,it=p.meta.items.find(i=>i.id==="child_credits"),d=V7.P7.ITEM_DETAIL.added_age_mix.counts;
 const denominator=d.later+(1-C.c3)*d.g3_rate,gPeople=(1-C.c3)*sum(counts.g3_rate)+sum(counts.later);
 for(const [name,part] of Object.entries(it.parts)) if(name.startsWith("lineage_g3plus:")) {
   const e=p.edits[it.edits.first+part.edit],id=`${e.side}|${e.line}|${e.scenario||e.key}`;
   if(!cells.has(id))cells.set(id,byAlloc(()=>0));
   for(const a of ALLOCS)cells.get(id)[a]-=gPeople*part.by[a]/denominator;
 }
 const out={cells,production};if(!override)minorCache.set(L.set,out);return out;
}
function payloadOf(p,part) {
 const out=V7.payloadOf(p,part);out.lines=out.lines.concat(clone(part.lines||[]));
 if(part.meta) out.meta=clone(part.meta);return out;
}
function evaluator(payload,api) {
 const ev=V7.evaluator(payload,api),cache=new WeakMap();
 function prepared(m) {if(!cache.has(m))cache.set(m,padSynthetic(api,m));return cache.get(m);}
 function evaluateFull(m0,s) {
   const m=prepared(m0),raw=ev.evaluateFull(m,s),state=clone(raw.state);
   for(const [id,src] of Object.entries(payload.meta.union_completion.carriers)) if(src.kind==="line") {
     const row=(src.side==="receipt"?raw.evaluation.receipts:raw.evaluation.spending).find(r=>r.id===src.parent_line);
     if(!row) blocked(`carrier ${id} has no selected parent`);
     const key=src.side==="receipt"?m.receipts.reference:row.key;
     state.response_override[id]=key===src.parent_key?row.response:0;
   }
   const evaluation=Engine.evaluate(m,state),cap=Consumer.capitalOf(evaluation,payload,s);
   const capital={...cap,components:cap.components.map((c,i)=>({...c,group:payload.meta.capital_return.components[i].part,level:payload.meta.capital_return.components[i].level}))};
   const meta=m0.corrections||{},post_engine={};
   for(const id of ["mixed_unit_removal","coverage"]) post_engine[`${id}_bn`]=meta[id]?.by_end?.[s.reading]?.total_bn||0;
   post_engine.total_bn=sum(Object.values(post_engine));
   return {evaluation,state,capital,post_engine,cost_bn:-evaluation.welfare_bn+capital.total_bn+post_engine.total_bn};
 }
 return {...ev,evaluateFull,cost:(m,s)=>evaluateFull(m,s).cost_bn};
}
function adoptedPackage(L) {
 const prepared=new WeakMap();
 return {source:`${V8_LANE}/package.cjs + generation-scoped post-engine amounts`,specs:L.api.MAIN_SPECS,cost:(m,i)=> {
   if(!prepared.has(m))prepared.set(m,L.api.withSyntheticLines(m));
   const s=L.api.MAIN_SPECS[i],r=L.api.evaluateFull(prepared.get(m),s,L.api.MAIN_PROFILE);
   const own=["mixed_unit_removal","coverage"].reduce((v,id)=>v+(m.corrections?.[id]?.by_end?.[s.reading]?.total_bn||0),0);
   return r.cost_bn-r.post_engine.total_bn+own;
 }};
}
function oracle(set) {
 const S=readJson(`${V8_LANE}/derived/summary.json`).v8,r=X.P.csvRows(`${V8_LANE}/derived/main_case_bands.csv`).find(r=>r.variant===(set==="set"?"adopted":"cash_set")&&r.profile===P8.MAIN_PROFILE);
 const ends=S.end_specifications[set];
 if(!r||!ends.length||!ends.every(x=>JSON.stringify(x)===JSON.stringify(ends[0]))) blocked("case band/end missing or methods disagree");
 return {source:`${V8_LANE}/derived/main_case_bands.csv`,specs:ends[0],band:[+r.cost_low_bn,+r.cost_high_bn],full:{source:`${V8_LANE}/derived/summary.json v8`,band:set==="set"?S.band_bn:S.cash_set_bn}};
}
function perSpec(set) {
 if(set!=="set")return null;
 const rows=X.P.csvRows(`${V8_LANE}/derived/per_spec.csv`).filter(r=>r.in_band==="true"||r.in_band==="1"),cost=new Map();
 for(const i of new Set(rows.map(r=>+r.spec))) {const rs=rows.filter(r=>+r.spec===i);if(rs.length!==X.METHODS.length)blocked(`spec ${i} method count`);cost.set(i,sum(rs.map(r=>+r.cost_bn))/rs.length);}
 return {source:`${V8_LANE}/derived/per_spec.csv`,cost};
}
module.exports={...V7,V8_LANE,V7_LANE:V8_LANE,P8,P7:P8,loadCase,layer,routeFor,reporterPopulation,reporterRoutes,stringLeaves,withStep,padSynthetic,payloadOf,evaluator,adoptedPackage,oracle,perSpec};
