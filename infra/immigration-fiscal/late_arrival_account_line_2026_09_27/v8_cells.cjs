/* Aggregate P7/v8 ownership first, then the declared within-G1 t1/wage split.
 * All resulting cells close to the authoritative generation model; no tag
 * inference substitutes for the generation lane's exact routing contract. */
"use strict";
const V8=require("../generation_account_2026_09_24/v8_split.cjs"),Fine7=require("./v7_cells.cjs");
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {Engine,ALLOCS,byAlloc}=V8.X,clone=x=>JSON.parse(JSON.stringify(x)),sum=xs=>xs.reduce((a,b)=>a+b,0);
const TOPS=["G1","G2","G3plus"],zero=()=>Object.fromEntries(ALLOCS.map(a=>[a,0]));
const fail=s=>{throw Error(`[BLOCKED] oct15 G1: ${s}`);};
const sha=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
function readPinned(rel,pins,root=path.resolve(__dirname,"..")) {
 const file=path.join(root,rel),expected=pins[rel];
 if(!expected||!fs.existsSync(file))fail(`undeclared or missing reporter source ${rel}`);
 const bytes=fs.readFileSync(file),actual=crypto.createHash("sha256").update(bytes).digest("hex");
 if(actual!==expected)fail(`changed admitted reporter source ${rel}`);
 // Keep binary sources as bytes: verifying a ZIP/parquet/NPZ hash does not
 // require a large lossy UTF-8 conversion. Text consumers decode explicitly.
 return bytes;
}
function reporterFineAmounts(reporters,drivers,route,fine,gens,top) {
 const out=Object.fromEntries(gens.map(g=>[g,zero()]));
 if(reporters.length!==fine.length)fail("fine/reporter record coverage");
 const lookup=new Map(fine.map(r=>[`${r.PH_SEQ}|${r.PPPOS}`,r]));
 if(lookup.size!==fine.length)fail("duplicate fine reporter identity");
 fine=reporters.map(r=>lookup.get(`${r.PH_SEQ}|${r.PPPOS}`));
 if(fine.some(r=>!r)||new Set(reporters.map(r=>`${r.PH_SEQ}|${r.PPPOS}`)).size!==reporters.length)fail("missing or duplicate carrier reporter identity");
 for(let i=0;i<reporters.length;i++)if(reporters[i].PH_SEQ!==fine[i].PH_SEQ||reporters[i].PPPOS!==fine[i].PPPOS||
   reporters[i].replicate_weights.length!==161||reporters[i].replicate_weights.some(x=>!Number.isFinite(x))||
   Math.abs(sum(gens.map(g=>fine[i].omega_b[g]))-1)>1e-12)fail("fine/reporter identity or partition");
 for(const a of ALLOCS) {
   const own=route.allocations[a],shares=Object.fromEntries(gens.map(g=>[g,0]));
   if(!own||!Array.isArray(own.components))fail(`missing reporter components ${a}`);
   if(!Number.isFinite(route.by[a]))fail(`invalid reporter part amount ${a}`);
   if(route.by[a]===0)continue;
   for(const component of own.components) {
     const values=drivers[component.driver_id]?.values;
     if(!values||values.length!==reporters.length||values.some(x=>!Number.isFinite(x))||!Number.isFinite(component.raw_share))fail("invalid reporter source driver");
     const weighted=values.map((x,i)=>x*reporters[i].replicate_weights[0]),den=sum(weighted);
     if(!den&&component.raw_share)fail("nonzero reporter component on zero source driver");
     for(const g of gens)shares[g]+=den?component.raw_share*sum(weighted.map((x,i)=>x*fine[i].omega_b[g]))/den:0;
   }
   if(Math.abs(sum(Object.values(shares))-1)>1e-12)fail(`reporter fine share closure ${a}`);
   for(const G of TOPS) {
     const fineShare=sum(gens.filter(g=>top[g]===G).map(g=>shares[g]));
     if(Math.abs(fineShare-own.generation_shares[G][0])>1e-12)fail(`reporter coarse/fine share ${G}/${a}`);
   }
   for(const g of gens)out[g][a]=route.by[a]*shares[g];
 }
 return out;
}
function reporterFine(L,gens,top,opts) {
 if(opts.convention!=="b")return {cells:new Map(),provenance:null,population:null};
 const finePath=path.join(__dirname,"_cache/reporter_fine_oct15.json"),rawPath=path.join(__dirname,"../within_group_distribution_2026_09_29/derived/reporter_b_routes.json");
 const pins=JSON.parse(require("../world_ledger_2026_09_27/v8_snapshot.cjs")
   .read("infra/immigration-fiscal/generation_account_2026_09_24/inputs/pins.json"));
 const fine=JSON.parse(fs.readFileSync(finePath,"utf8")),raw=JSON.parse(readPinned("within_group_distribution_2026_09_29/derived/reporter_b_routes.json",pins).toString("utf8"));
 readPinned("within_group_distribution_2026_09_29/reporter_b_routes.py",pins);
 if(!raw.source_sha256||!Object.keys(raw.source_sha256).length)fail("missing reporter source graph");
 for(const [rel,hash]of Object.entries(raw.source_sha256)) {
   if(pins[rel]!==hash)fail(`reporter graph not admitted ${rel}`);
   readPinned(rel,pins);
 }
 for(const [p,hash]of Object.entries(fine.source_sha256))if(sha(p)!==hash)fail(`changed fine reporter source ${p}`);
 const reading=opts.arrivalReading||"central",records=fine.readings[reading];
 if(!records)fail(`undeclared reporter arrival reading ${reading}`);
 const cells=new Map(),routes=raw.sets[L.set]?.routes;
 const source=L.added.find(it=>it.id==="union_completion"),carriers=L.payload.meta.union_completion.carriers;
 const expected=Object.entries(source.record.parts).filter(([name,p])=>name.startsWith("union_G3plus:")&&carriers[source.edits[p.edit].line]);
 if(!routes||expected.length!==Object.keys(routes).length)fail("reporter carrier part coverage");
 for(const [name,p]of expected) {
   const route=routes[name],e=source.edits[p.edit];
   if(!route||route.part_edit!==p.edit||route.global_edit!==source.first+p.edit||JSON.stringify(route.by)!==JSON.stringify(p.by)||
     id(route.cell)!==id(e))fail(`reporter carrier source changed ${name}`);
   const amounts=reporterFineAmounts(raw.reporters,raw.driver_pool,route,records,gens,top),key=id(e);
   if(!cells.has(key))cells.set(key,Object.fromEntries(gens.map(g=>[g,zero()])));
   for(const g of gens)for(const a of ALLOCS)cells.get(key)[g][a]+=amounts[g][a];
 }
 const population=Object.fromEntries(gens.map(g=>[g,{population:sum(records.map(r=>r.people*r.omega_b[g])),
   adults:sum(records.filter(r=>r.A_AGE>=18).map(r=>r.people*r.omega_b[g]))}]));
 return {cells,population,provenance:{rule:"Exact raw carrier drivers and completed NAS(b) reporter owners; original P7 union mapping frozen",arrival_reading:reading,
   fine_routes_sha256:sha(finePath),carrier_routes_sha256:sha(rawPath),parts:expected.length,reporters:records.length,
   modeled_source_anchors:expected.flatMap(([name])=>ALLOCS.filter(a=>routes[name].allocations[a].ownership?.kind==="modeled_source_anchor")
     .map(a=>({part:name,allocation:a,ownership:clone(routes[name].allocations[a].ownership)})))}};
}
function entries(m) {
 const out=[];
 for(const l of m.spending.lines)for(const [key,cells]of Object.entries(l.keys))out.push({side:"spending",line:l.id,key,cells});
 for(const l of m.receipts.lines)for(const [scenario,cells]of Object.entries(l.cells))out.push({side:"receipt",line:l.id,scenario,cells});
 return out;
}
const id=e=>`${e.side}|${e.line}|${e.key||e.scenario}`;
// models29 already carries its own v4 production. payloadOf adds a layer delta
// to that complete base grid; an empty base would drop production or stop.
const applyPart=(m,part)=>Engine.applyCorrections(m,V8.payloadOf({lines:[],receipt_lines:[],edits:[],production:m.production},part));
function scopePost(source,share) {
 if(!Number.isFinite(share))fail("nonfinite fixed within-generation post share");
 if(!Number.isFinite(source.total_bn)||(source.replicates_bn&&(!Array.isArray(source.replicates_bn)||!source.replicates_bn.every(Number.isFinite))))fail("nonfinite source post amount or replicate");
 if(source.se_bn!==undefined&&(!Number.isFinite(source.se_bn)||source.se_bn<0))fail("invalid source post SE");
 const z=clone(source);
 z.total_bn*=share;
 if(z.replicates_bn)z.replicates_bn=z.replicates_bn.map(v=>v*share);
 if(z.se_bn!==undefined)z.se_bn*=Math.abs(share);
 z.fixed_within_generation_share=share;
 z.uncertainty_condition="conditional on fixed within-generation allocation share; source uncertainty carried as reported; share uncertainty unidentified";
 return z;
}
function aggregate(models,hits) {
 const m=clone(models[hits[0]]),maps=hits.map(g=>new Map(entries(models[g]).map(e=>[id(e),e])));
 for(const e of entries(m))for(const a of ALLOCS) {
   const national=e.cells[a].target_bn+e.cells[a].other_bn;
   e.cells[a].target_bn=sum(maps.map(q=>q.get(id(e)).cells[a].target_bn));
   e.cells[a].share=sum(maps.map(q=>q.get(id(e)).cells[a].share));
   e.cells[a].other_bn=national-e.cells[a].target_bn;
 }
 for(const k of ["private_wtp_bn","induced_receipts_bn"])m.production[k]=m.production[k].map((_,i)=>sum(hits.map(g=>models[g].production[k][i])));
 m.meta.target_population=sum(hits.map(g=>models[g].meta.target_population));
 return m;
}
function layer(L,gens,top,models29,union29,opts={}) {
 const selector=process.env.LATE_V8_POST_SPLIT||"t1_population";
 if(selector!=="t1_population")fail(`unknown post split ${selector}`);
 const groups=Object.fromEntries(TOPS.map(G=>[G,gens.filter(g=>top[g]===G)]));
 if(groups.G1.length!==7||groups.G2.length!==1||groups.G3plus.length!==1)fail("expected seven G1 cells plus G2/G3plus");
 if(!opts.populations||gens.some(g=>!Number.isFinite(opts.populations[g])||opts.populations[g]<=0))fail("missing row4 cell headcounts");
 const coarse=Object.fromEntries(TOPS.map(G=>[G,aggregate(models29,groups[G])]));
 const authoritative=V8.layer(L,TOPS,Object.fromEntries(TOPS.map(g=>[g,g])),coarse,union29,{...opts,convention:opts.convention||"a"});
 const old=Fine7.layer(L.old,gens,top,models29,union29,{...opts,withStep:V8.withStep}),parts=clone(old.parts);
 for(const g of gens)parts[g].lines=clone(L.newLines);
 const current=Object.fromEntries(gens.map(g=>[g,applyPart(models29[g],parts[g])]));
 const reporter=reporterFine(L,gens,top,opts);
 const routes=[];
 for(const G of TOPS) {
   const hits=groups[G],want=applyPart(coarse[G],authoritative.parts[G]);
   const maps=hits.map(g=>new Map(entries(current[g]).map(e=>[id(e),e])));
   for(const e of entries(want)) {
     const by=zero(),share={};
     const exact=reporter.cells.get(id(e)),reporterTotal=byAlloc(a=>exact?sum(hits.map(g=>exact[g][a])):0);
     for(const a of ALLOCS) {
       const have=sum(maps.map(q=>q.get(id(e)).cells[a].target_bn));by[a]=e.cells[a].target_bn-have;
       const job=e.side==="receipt"&&["corporate_capital","corporate_labor","remaining_production_property","other_production_taxes"].includes(e.line);
       for(let i=0;i<hits.length;i++) {
         const g=hits[i];share[g]||=zero();
         share[g][a]=hits.length===1?1:job&&!opts.jobT1?opts.wages[a][g]:have?maps[i].get(id(e)).cells[a].target_bn/have:Math.abs(by[a]-reporterTotal[a])<1e-12?1/hits.length:fail(`nonzero residual delta on zero t1 ${id(e)}`);
       }
       if(Math.abs(sum(hits.map(g=>share[g][a]))-1)>=1e-12)fail(`share closure ${id(e)}`);
     }
     if(ALLOCS.some(a=>by[a]!==0)||exact) {
       for(const g of hits)parts[g].edits.push({...Object.fromEntries(Object.entries(e).filter(([k])=>k!=="cells")),by:Object.fromEntries(ALLOCS.map(a=>[a,(by[a]-reporterTotal[a])*share[g][a]+(exact?.[g][a]||0)]))});
       routes.push({generation:G,cell:id(e),by,share,reporter_exact:exact?Object.fromEntries(hits.map(g=>[g,exact[g]])):null,
         rule:"observed reporter carriers by actual raw driver and parent/relative fine cell; remaining aggregate delta by within G1 t1/job wages"});
     }
   }
   for(const k of ["private_wtp_bn","induced_receipts_bn"]) {
     const delta=want.production[k].map((v,i)=>v-sum(hits.map(g=>current[g].production[k][i])));
     for(const g of hits){parts[g].production||={};const old=parts[g].production[k]||delta.map(()=>0);
       parts[g].production[k]=old.map((v,i)=>v+delta[i]*(hits.length===1?1:opts.wages.personal[g]));}
   }
   const fineAfter=Object.fromEntries(hits.map(g=>[g,applyPart(models29[g],parts[g])]));
   const target=g=>fineAfter[g].receipts.lines.find(l=>l.id==="federal_income_tax").cells[fineAfter[g].receipts.reference].personal.target_bn;
   const total=sum(hits.map(target)),population=sum(hits.map(g=>opts.populations[g]));
   for(const g of hits) {
     const meta=clone(authoritative.parts[G].meta);meta.generation=G;meta.late_cell=g;
     meta.within_generation_post_rule="[APPROX] mixed removal by corrected federal income-tax t1; coverage by cell population; arrival-age coverage unmeasured";
     for(const item of ["mixed_unit_removal","coverage"])if(meta[item]) {
       const share=hits.length===1?1:item==="mixed_unit_removal"?(total?target(g)/total:fail("zero G1 income-tax t1")):opts.populations[g]/population;
       for(const end of ["low","high"])meta[item].by_end[end]=scopePost(meta[item].by_end[end],share);
     }
     parts[g].meta=meta;
   }
 }
 return {...old,parts,items:old.items,within_g1_routes:routes,reporter_fine_provenance:reporter.provenance,reporter_fine_population:reporter.population,post_split:selector};
}
module.exports={...V8,layer,applyPart,scopePost,readPinned,reporterFineAmounts,reporterFine,V6_LANE:V8.V8_LANE,P6:Fine7.P6,ALTERNATIVES:Fine7.ALTERNATIVES};
