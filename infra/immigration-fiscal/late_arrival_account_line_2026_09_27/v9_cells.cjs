/* Native-First: extend the existing fine-cell engine consumer in memory.
 * Source lines determine military placement; constructed people stay unlocated. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {requireAdopted}=require("../scripts/adoption_gate.cjs");
const V=require("../generation_account_2026_09_24/v9_split.cjs"),P=require("../main_case_2026_10_16/package.cjs");
const HERE=__dirname,ROOT=path.resolve(HERE,"../../.."),FISCAL=path.dirname(HERE);
const TOPS=["G1","G2","G3plus"],clone=x=>JSON.parse(JSON.stringify(x)),sum=xs=>xs.reduce((a,b)=>a+b,0);
const FILE=path.join(HERE,"inputs/oct16_source_hashes.json");
const fail=s=>{throw Error("[BLOCKED] oct16 late arrival: "+s);};
const sha=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const read=p=>JSON.parse(fs.readFileSync(path.join(FISCAL,p),"utf8"));
function assertClose(a,b,label,tolerance=1e-9){if(!Number.isFinite(a)||!Number.isFinite(b)||Math.abs(a-b)>tolerance)fail(`${label}: ${a} vs ${b}`);}
function requireEndSpecs(actualSpecs,actualEnds,summary,sourceSpecs){
 if(!Array.isArray(sourceSpecs)||!summary.specifications)fail("generation source lacks exact specification declaration");
 const declared=[summary.specifications.low_index,summary.specifications.high_index];
 for(const [k,i]of declared.entries())if(!Number.isInteger(i)||actualEnds[k]!==i||!sourceSpecs[i]||!require("node:util").isDeepStrictEqual(actualSpecs[actualEnds[k]],sourceSpecs[i]))fail("found end differs from exact generation specification "+(k?"high":"low"));
}
function reconcileProduction({models,canonical,gens,top,wageShares,row4Source,row4Fine,convention}){
 const budgets=[row4Source.closure_residual_max,row4Fine.closure_residual_max];
 if(budgets.some(x=>!Number.isFinite(x)||x<0||x>=1e-6))fail("row4 numerical source controls absent or failed");
 const audit={rule:"canonical generation P/F; within G1 residual by inherited personal wages; singleton G2/G3plus exact",origin:"v4_inputs.py separate3/9-cell finite-difference/quadrature normalization",budget_scope:"sum of recorded preclosure residual budgets times max(1,abs stored union); empirical numerical budget, not a theoretical error bound",generations:{}};
 for(const G of TOPS){
  const hits=gens.filter(g=>top[g]===G),weights=Object.fromEntries(hits.map(g=>[g,hits.length===1?1:wageShares[g]]));
  if(Object.values(weights).some(x=>!Number.isFinite(x)||x<0))fail("invalid production residual wage share "+G);
  assertClose(sum(Object.values(weights)),1,"production residual wages "+G,1e-12);
  audit.generations[G]={weights,fields:{}};
  for(const [field,key]of [["private_wtp_bn","P"],["induced_receipts_bn","F"]]){
   const target=canonical[G].production[field],before=target.map((_,i)=>sum(hits.map(g=>models[g].production[field][i])));
   const rawGap=target.map((v,i)=>before[i]-v);
   const cachedGap=target.map((_,i)=>sum(hits.map(g=>row4Fine.series[convention][g][key][i]))-row4Source.series[convention][G][key][i]);
   const budget=target.map((_,i)=>sum(budgets)*Math.max(1,Math.abs(sum(TOPS.map(g=>row4Source.series[convention][g][key][i])))));
   for(let i=0;i<target.length;i++){
    assertClose(rawGap[i],cachedGap[i],"production difference not the immutable row4 allocation gap "+G+field+i,1e-12);
    if(!Number.isFinite(budget[i])||Math.abs(cachedGap[i])>budget[i])fail("row4 allocation gap exceeds recorded empirical numerical budget "+G+field+i);
    for(const g of hits)models[g].production[field][i]-=rawGap[i]*weights[g];
    assertClose(sum(hits.map(g=>models[g].production[field][i])),target[i],"canonical reconciled production "+G+field+i,1e-12);
   }
   audit.generations[G].fields[field]={maximum_absolute_bn:Math.max(...rawGap.map(Math.abs)),raw_gap_bn:rawGap,cached_row4_gap_bn:cachedGap,empirical_budget_bn:budget};
  }
 }
 return audit;
}
function capture(){
 const adoption=requireAdopted("oct16");
 for(const [name,api]of [["corrections.json",P],["corrections_cash.json",P.CASH]]){
  const saved=read(`${P.LANE}/derived/${name}`);
  if(JSON.stringify(api.correctionsPayload())!==JSON.stringify(saved))fail("adopted case API and saved corrections differ "+name);
 }
 const files=new Set(Object.keys(require.cache).filter(f=>f.startsWith(ROOT+path.sep)));
 for(const lane of ["main_case_2026_10_16","generation_account_2026_09_24"]){
  const dir=path.join(FISCAL,lane,"derived");
  for(const name of fs.readdirSync(dir))if(lane.startsWith("main_case")?["corrections.json","corrections_cash.json","summary.json","main_case_bands.csv"].includes(name):name.includes("oct15")||name.includes("oct16")||/^model(_b)?_/.test(name))files.add(path.join(dir,name));
 }
 for(const lane of ["spending_keys_r5_2026_10_15","count_composition_r5_2026_10_15","consumption_tax_bases_r5_2026_10_15","one_rate_2026_10_15"]){
  const dir=path.join(FISCAL,lane,"derived");for(const name of fs.readdirSync(dir))if(fs.statSync(path.join(dir,name)).isFile())files.add(path.join(dir,name));
 }
 for(const dir of ["split_central","split_lower","split_upper"])
  for(const name of fs.readdirSync(path.join(HERE,"_cache",dir)))if(name.endsWith(".json"))files.add(path.join(HERE,"_cache",dir,name));
 files.add(path.join(HERE,"_cache/reporter_fine_oct15.json"));
 for(const rel of ["live_case.json","main_case_2026_10_16/inputs/item13_ready.json","main_case_2026_10_16/inputs/item21_ready.json","generation_account_2026_09_24/inputs/pins.json","generation_account_2026_09_24/inputs/routing.json","generation_account_2026_09_24/inputs/minor_parent_measurement_oct15.json","generation_account_2026_09_24/derived/v4_inputs.json","world_ledger_2026_09_27/inputs/oct15_source_hashes.json"])files.add(path.join(FISCAL,rel));
 for(const name of ["coverage_bound_oct15.json","coverage_bound_oct16.json","line_parts_oct16_set.csv","line_parts_oct16_cash.csv"])files.add(path.join(FISCAL,"coverage_bound_2026_10_14/derived",name));
 for(const file of ["run_cells.cjs","v8_cells.cjs","v7_cells.cjs","v9_cells.cjs"])files.add(path.join(HERE,file));
 const sha256=Object.fromEntries([...files].filter(f=>fs.statSync(f).isFile()).sort().map(f=>[path.relative(ROOT,f),sha(f)]));
 fs.mkdirSync(path.dirname(FILE),{recursive:true});
 fs.writeFileSync(FILE,JSON.stringify({case:"oct16",adoption,authority:"repository adoption declaration plus exact generation/coverage source hashes",sha256},null,1)+"\n");
 console.log(`captured ${Object.keys(sha256).length} oct16 source hashes; adopted ${adoption.adopted}, ${adoption.decision}`);
}
function verifySources(){
 const adoption=requireAdopted("oct16");
 if(!fs.existsSync(FILE))fail("missing explicit oct16 source snapshot; capture after adoption");
 const q=JSON.parse(fs.readFileSync(FILE,"utf8"));
 if(q.case!=="oct16"||JSON.stringify(q.adoption)!==JSON.stringify(adoption))fail("source snapshot adoption identity");
 for(const [rel,want]of Object.entries(q.sha256))if(!fs.existsSync(path.join(ROOT,rel))||sha(path.join(ROOT,rel))!==want)fail("changed admitted source "+rel);
 return q;
}
function preflight(caseKey,probe=false){
 const api=caseKey.endsWith("_cash")?P.CASH:P,actual=api.correctionsPayload();
 if(!actual.meta.coverage.counts_by_generation_folded)fail("case coverage integration not ready: missing folded generation counts");
 const saved=read(`${P.LANE}/derived/corrections${caseKey.endsWith("_cash")?"_cash":""}.json`);
 if(JSON.stringify(actual)!==JSON.stringify(saved))fail("case API and saved corrections differ; source publication incomplete");
 if(!probe)verifySources();
}
function cellExposure(full,row){
 const capital=full.capital.components.find(c=>c.id===(row.capital_source_line||row.line));
 if((row.side==="capital"||row.source_side==="capital"||row.economic_class==="capital_return"||row.kind?.startsWith("college")||row.component==="capital_engine"||row.component==="college_capital_interaction")&&capital)return capital.return_bn;
 const spending=full.evaluation.spending.find(c=>c.id===(row.capital_source_line||row.line));
 if(!spending)fail("source line not in fine model "+(row.capital_source_line||row.line));
 return spending.amount_bn*spending.response;
}
function routeShares(exposures,delta,label){
 if(!Object.values(exposures).every(Number.isFinite))fail("nonfinite fine exposure "+label);
 const total=sum(Object.values(exposures));
 if(total===0){if(Math.abs(delta)>1e-12)fail("nonzero amount on zero source exposure "+label);return Object.fromEntries(Object.keys(exposures).map(g=>[g,0]));}
 const shares=Object.fromEntries(Object.entries(exposures).map(([g,x])=>[g,x/total]));
 assertClose(sum(Object.values(shares)),1,"source share closure "+label,1e-12);return shares;
}
function fineRoute(row,fullByCell,hits,delta,label){
 // A declared generation with one destination needs no invented line driver.
 //21 includes conceptual native-child components, not separate engine lines.
 if(hits.length===1)return {exposures:{[hits[0]]:null},shares:{[hits[0]]:1}};
 const exposures=Object.fromEntries(hits.map(g=>[g,cellExposure(fullByCell[g],row)]));
 return {exposures,shares:routeShares(exposures,delta,label)};
}
// Typed components declared by main_case_2026_10_16/item_rate.cjs. A name
// substring or a generation ownership tag is not a population declaration.
const UNLOCATED_RATE_COMPONENTS=new Set(["capital_coverage","capital_own_coverage_rate_interaction","capital_count_interaction","pension_count_interaction","pension_coverage_price_interaction","oasdi_item12_coverage","part_a_item12_coverage"]);
const isUnlocated=row=>row.id==="coverage_repricing"||row.population==="coverage"||UNLOCATED_RATE_COMPONENTS.has(row.component);
function countPieces(block,id,end){
 const rows=P.RATE.countParts(block,end),out={};
 for(const G of TOPS){
  const hits=rows.filter(p=>p.generation===G);
  // Source's signed scenario subtraction applies identically to observed and
  // coverage columns, retaining joint-minus16 for17.
  const amounts=hits.map(p=>{const sign=p.scenario===block.parts_scenario?1:p.scenario===block.subtract_parts_scenario?-1:fail("unknown count scenario "+p.scenario);
   return {observed:sign*Number(p.observed_change_bn),coverage:sign*Number(p.coverage_change_bn)};});
  out[G]={observed:sum(amounts.map(p=>p.observed)),coverage:sum(amounts.map(p=>p.coverage))};
 }
 assertClose(sum(TOPS.map(G=>out[G].observed+out[G].coverage)),block.by_end[end].total_bn,"typed count parts "+id,1e-8);
 return out;
}
function build({cells,res,GENS,G1_CELLS,TOP,DEF,Engine,partsOf}){
 const probe=process.argv.includes("--probe"),source=probe?{authority:"[CANDIDATE PROBE]"}:verifySources();
 const which=cells.case.endsWith("_cash")?"cash":"set",api=which==="set"?P:P.CASH,payload=api.correctionsPayload();
 if(!payload.meta.coverage.counts_by_generation_folded)fail("case coverage integration not ready: missing folded generation counts");
 const selected=payload.meta.items.filter(r=>r.applied).map(r=>r.id);
 if(selected.includes("passthrough_source_tax"))fail("central may not select beside item19");
 const values=api.MAIN_SPECS.map(s=>api.evaluateFull(api.payloadModel(),s,api.MAIN_PROFILE).cost_bn);
 const ends=[values.indexOf(Math.min(...values)),values.indexOf(Math.max(...values))];
 const gen=read(`generation_account_2026_09_24/derived/generation_summary_oct16${which==="cash"?"_cash":""}.json`);
 const genPayloads=read(`generation_account_2026_09_24/derived/generation_corrections_oct16${which==="cash"?"_cash":""}.json`).payloads;
 for(const conv of ["a","b"])for(const G of TOPS)requireEndSpecs(api.MAIN_SPECS,ends,gen,genPayloads[conv][G].meta.v9_specs);
 const old=read(`generation_account_2026_09_24/derived/generation_summary_oct15${which==="cash"?"_cash":""}.json`);
 const additions=["veterans_compensation","income_security_administration","public_college_response","native_minor_calibration","coverage_tenure","consumption_tax_bases","one_rate","health_residual_key","coverage_repricing"];
 const programs=[...cells.programs,...additions];
 const inheritedProduction={};
 for(const conv of ["a","b"]){inheritedProduction[conv]={};for(const G of TOPS){
  const hits=GENS.filter(g=>TOP[g]===G),target=V.sourceModels(which,conv).models[G];inheritedProduction[conv][G]={};
  for(const key of ["private_wtp_bn","induced_receipts_bn"]){
   const differences=target.production[key].map((wanted,i)=>{const actual=sum(hits.map(g=>res[conv][g].model.production[key][i]));return {i,actual,wanted,delta:actual-wanted};});
   const sorted=differences.toSorted((a,b)=>Math.abs(b.delta)-Math.abs(a.delta));
   inheritedProduction[conv][G][key]={maximum_absolute_bn:Math.abs(sorted[0].delta),maximum_relative:Math.max(...differences.map(p=>Math.abs(p.delta)/Math.max(1,Math.abs(p.wanted)))),worst:sorted.slice(0,4)};
  }
 }}
 if(probe){fs.writeFileSync(path.join(HERE,"_cache",`oct16_production_${which}_${DEF}.json`),JSON.stringify(inheritedProduction,null,1)+"\n");console.log("[probe] inherited fine/coarse production diagnostics exported");}
 const out={case:`oct16${which==="cash"?"_cash":""}`,main:P.LANE,def:DEF,low_spec:api.MAIN_SPECS[ends[0]],high_spec:api.MAIN_SPECS[ends[1]],lo:ends[0],hi:ends[1],union_band_bn:ends.map(i=>values[i]),programs,conventions:{},v4:cells.v4,v6:{...cells.v6,payload:`${P.LANE}/derived/corrections${which==="cash"?"_cash":""}.json`},v7:cells.v7,v9:{source,selected_items:selected,item13_by_cell:[],item_posts_by_cell:[],unlocated_rule:"Coverage and all unlocated calibration/count changes stay outside identified arrival cells; inherited coverage removed before new coverage enters once.",routing:"Original source-line/capital fine-cell amounts within each declared source generation, conditional on the inherited fine allocation. Mixed-unit removal retains inherited FIT allocation."}};
 for(const conv of ["a","b"]){
  const result=out.conventions[conv]={};
  const fullBySpec={},fineModels={};
  const oldCoverageBlock=V.sourceModels(which,conv).L.payload.meta.coverage;
  const oldCoverage=read(oldCoverageBlock.file).sets[which].scenarios[oldCoverageBlock.construction];
  if(!oldCoverage.adults_by_generation)fail("inherited coverage lacks identified source adult totals");
  const first=V.generationParts(api,api.MAIN_SPECS[0],conv);
  for(const g of GENS){
   const base=res[conv][g].model,G=TOP[g],hits=GENS.filter(h=>TOP[h]===G);
   const edits=first.extra_payloads[G].edits.map(e=>{
    const select=m=>e.side==="receipt"?m.receipts.lines.find(l=>l.id===e.line)?.cells[e.scenario]:m.spending.lines.find(l=>l.id===e.line)?.keys[e.key];
    const denominator=select(V.sourceModels(which,conv).models[G]),numerator=select(base);
    if(!denominator||!numerator)fail("new engine edit lacks source "+e.line);
    const by={};for(const a of ["personal","shared"]){const d=denominator[a].target_bn,n=numerator[a].target_bn;if(d===0&&e.by[a])fail("zero engine edit source "+e.line);by[a]=d?e.by[a]*n/d:0;}
    return {...clone(e),by};
   });
   const stepped=V.withStep(base,edits);
   fineModels[g]={...stepped,production:{...stepped.production,private_wtp_bn:stepped.production.private_wtp_bn.slice(),induced_receipts_bn:stepped.production.induced_receipts_bn.slice()}};
   const covered=payload.meta.coverage.counts_by_generation_folded[G],oldCovered=(V.sourceModels(which,conv).L.payload.meta.coverage.counts_by_generation[G]||0)+(G==="G3plus"?(V.sourceModels(which,conv).L.payload.meta.coverage.counts_by_generation.added||0):0);
   const share=cells.v8.post_by_cell[conv][g].coverage.by_end.low.fixed_within_generation_share;
   const n=cells.conventions[conv][g].population-oldCovered*share;
   if(!Number.isFinite(n)||!Number.isFinite(covered)||n<=0)fail("invalid observed fine count "+g);
   const adultShare=hits.length===1?1:cells.conventions[conv][g].adults/old.conventions[conv][G].adults;
   result[g]={population:n,adults:cells.conventions[conv][g].adults-oldCoverage.adults_by_generation[G]*adultShare,population_scope:"identified roster; inherited allocated coverage removed",oct15_cost_bn:["low","high"].map(end=>cells.conventions[conv][g][end].cost_bn-cells.conventions[conv][g][end].parts.coverage),oct05_medical_parts_personal:cells.conventions[conv][g].oct05_medical_parts_personal};
  }
  for(const G of TOPS){
   const b16=payload.meta.native_minor_calibration,b17=payload.meta.coverage_tenure;
   const n0=payload.meta.coverage.counts_by_generation_folded[G];
   const covered=n0+(b16.coverage_people_change_by_generation?.[G]||0)+(b17.coverage_people_change_by_generation?.[G]||0);
   const calibrated=(b16.observed_people_change_by_generation?.[G]||0)+(b17.observed_people_change_by_generation?.[G]||0);
   result[`unlocated_coverage_${G}`]={population:covered,adults:oldCoverage.adults_by_generation[G],generation:G,population_scope:"constructed coverage; arrival age unidentified; generation source adult total retained",oct15_cost_bn:["low","high"].map(end=>{const q=V.sourceModels(which,conv).L.payload.meta.coverage.by_end[end];return (q.by_generation_bn||q.by_generation)[G];})};
   result[`unlocated_calibration_${G}`]={population:calibrated,adults:0,generation:G,population_scope:"signed observed-weight calibration change; no identified arrival placement",oct15_cost_bn:[0,0]};
  }
  const row4Source=read("generation_account_2026_09_24/derived/v4_inputs.json").production;
  const row4Fine=JSON.parse(fs.readFileSync(path.join(HERE,"_cache",`split_${DEF}`,"v4_inputs.json"),"utf8")).production;
  const wageShares=JSON.parse(fs.readFileSync(path.join(HERE,"_cache",`split_${DEF}`,"job_wages_oct15.json"),"utf8")).shares[conv].personal;
  out.v9.production_reconciliation||={};out.v9.production_reconciliation[conv]=reconcileProduction({models:fineModels,canonical:first.models,gens:GENS,top:TOP,wageShares,row4Source,row4Fine,convention:conv});
  // Check every new engine cell/allocation, including unused alternatives.
  for(const G of TOPS){
   const hits=GENS.filter(g=>TOP[g]===G),expected=first.models[G];
   for(const side of ["spending","receipts"])for(const line of expected[side].lines){
    for(const [key,by]of Object.entries(side==="spending"?line.keys:line.cells))for(const a of ["personal","shared"]){
     const actual=sum(hits.map(g=>{const l=fineModels[g][side].lines.find(q=>q.id===line.id);if(!l)fail("missing engine line "+line.id);return (side==="spending"?l.keys:l.cells)[key][a].target_bn;}));
     assertClose(actual,by[a].target_bn,"new source line "+G+line.id+key+a);
    }
   }
   for(const key of ["private_wtp_bn","induced_receipts_bn"])expected.production[key].forEach((v,j)=>assertClose(sum(hits.map(g=>fineModels[g].production[key][j])),v,"production "+G+key+j,1e-12));
  }
  // The endpoints are exported below. Interior specifications have their own
  // source-line routing and unlocated accounting; none inherits endpoint totals.
  let worstInterior=0;
  for(const [i,s]of api.MAIN_SPECS.entries())if(!ends.includes(i)){
   const full=V.generationParts(api,s,conv),fine=Object.fromEntries(GENS.map(g=>[g,V.sourceModels(which,conv).ev.evaluateFull(fineModels[g],s)]));
   const costs=Object.fromEntries(GENS.map(g=>[g,fine[g].cost_bn-(fine[g].post_engine?.coverage_bn||0)]));
   const unlocated=Object.fromEntries(TOPS.map(G=>{const q=V.sourceModels(which,conv).L.payload.meta.coverage.by_end[s.reading];return [G,(q.by_generation_bn||q.by_generation)[G]+(full.posts[G].native_minor_calibration||0)+(full.posts[G].coverage_tenure||0)];}));
   for(const row of full.rows)if(!["native_minor_calibration","coverage_tenure"].includes(row.id))for(const G of TOPS){
    const delta=row.by_generation_bn[G]||0,hits=GENS.filter(g=>TOP[g]===G);
    if(row.generation&&row.generation!==G){assertClose(delta,0,"declared generation ownership "+row.id+G);continue;}
    if(isUnlocated(row)){unlocated[G]+=delta;continue;}
    const {shares}=fineRoute(row,fine,hits,delta,row.id+"/"+G);
    for(const g of hits)costs[g]+=delta*shares[g];
   }
   for(const G of TOPS){const cost=sum(GENS.filter(g=>TOP[g]===G).map(g=>costs[g]))+unlocated[G];assertClose(cost,full.costs[G],"interior generation "+conv+G+i);worstInterior=Math.max(worstInterior,Math.abs(cost-full.costs[G]));}
   assertClose(sum(Object.values(costs))+sum(Object.values(unlocated)),values[i],"interior case "+conv+i);
  }
  out.v9.all_specification_closure||={};out.v9.all_specification_closure[conv]={count:api.MAIN_SPECS.length,tolerance_bn:1e-9,worst_interior_generation_bn:worstInterior,engine_lines_all_allocations:true,production_tolerance_bn:1e-12};
  for(const [k,i]of ends.entries()){
   const s=api.MAIN_SPECS[i],end=k===0?"low":"high",full=V.generationParts(api,s,conv),fine={};
   for(const g of GENS){
    const {_full,...q}=partsOf(fineModels[g],s,true);
    fine[g]=_full;
    const coverage=q.parts.coverage;
    result[g][end]={...q,cost_bn:q.cost_bn-coverage,parts:{...q.parts,coverage:0,...Object.fromEntries(additions.map(id=>[id,0]))}};
    const oldAlt=cells.conventions[conv][g].job_capital_t1_cost_bn;
    if(oldAlt){result[g].job_capital_t1_cost_bn||=[];result[g].job_capital_t1_cost_bn[k]=oldAlt[k]-cells.conventions[conv][g][end].cost_bn;}
   }
   for(const G of TOPS){
    const prior=V.sourceModels(which,conv).L.payload.meta.coverage.by_end[end];
    const amount=(prior.by_generation_bn||prior.by_generation)[G];
    for(const kind of ["coverage","calibration"]){const name=`unlocated_${kind}_${G}`,parts=Object.fromEntries(programs.map(id=>[id,0]));if(kind==="coverage")parts.coverage=amount;
     result[name][end]={cost_bn:kind==="coverage"?amount:0,parts};}
   }
   const add=(g,id,delta)=>{if(!Number.isFinite(delta))fail("nonfinite post "+id);result[g][end].parts[id]+=delta;result[g][end].cost_bn+=delta;};
   for(const id of ["native_minor_calibration","coverage_tenure"]){
    const parts=countPieces(payload.meta[id],id,end);
    for(const G of TOPS){assertClose(parts[G].observed+parts[G].coverage,full.posts[G][id]||0,"count generation "+id+G,1e-8);
     add(`unlocated_calibration_${G}`,id,parts[G].observed);add(`unlocated_coverage_${G}`,id,parts[G].coverage);
     out.v9.item_posts_by_cell.push({convention:conv,end,item:id,cell:`unlocated_coverage_${G}`,delta_bn:parts[G].coverage});
     out.v9.item_posts_by_cell.push({convention:conv,end,item:id,cell:`unlocated_calibration_${G}`,delta_bn:parts[G].observed});}
   }
   for(const row of full.rows){
    const id=row.id;if(["native_minor_calibration","coverage_tenure"].includes(id))continue;
    for(const G of TOPS){
     const delta=row.by_generation_bn[G]||0,hits=GENS.filter(g=>TOP[g]===G);
     if(row.generation&&row.generation!==G){assertClose(delta,0,"declared generation ownership "+id+G);continue;}
     if(isUnlocated(row)){
      add(`unlocated_coverage_${G}`,id,delta);
      out.v9.item_posts_by_cell.push({convention:conv,end,item:id,cell:`unlocated_coverage_${G}`,line:row.line||row.source_line||null,component:row.component||row.kind||null,delta_bn:delta});
      continue;
     }
     const {exposures,shares}=fineRoute(row,fine,hits,delta,id+"/"+row.line+"/"+G);
     for(const g of hits){
      const change=delta*shares[g];add(g,id,change);
      out.v9.item_posts_by_cell.push({convention:conv,end,item:id,cell:g,line:row.line,component:row.component||row.kind||null,delta_bn:change});
      if(id==="veterans_compensation"){
       const generationShare=row.delta_bn?delta/row.delta_bn:0;
       const before=row.before_bn*generationShare*shares[g],after=row.after_bn*generationShare*shares[g];
       assertClose(after-before,change,"military response/fraction "+g);
       const sourceLine=hits.length>1?fine[g].evaluation.spending.find(r=>r.id===row.line):null;
       const original=row.fraction?before/row.fraction:before;
       if(sourceLine)assertClose(original,sourceLine.amount_bn*sourceLine.response,"military original fine line "+g+row.line);
       out.v9.item13_by_cell.push({convention:conv,end,cell:g,source_line:row.source_line,line:row.line,population:row.population,part:row.part,key:row.key,fraction:row.fraction??1,response:row.response,original_line_bn:original,original_line_scope:"pre-item13 responsive line amount; assigned target and inherited response exported separately",original_target_bn:sourceLine?.amount_bn??null,inherited_response:sourceLine?.response??null,before_bn:before,after_bn:after,delta_bn:change,original_driver_bn:exposures[g],within_generation_source_share:shares[g]});
      }
     }
    }
   }
   for(const G of TOPS){
    const names=[...GENS.filter(g=>TOP[g]===G),`unlocated_coverage_${G}`,`unlocated_calibration_${G}`];
    assertClose(sum(names.map(g=>result[g][end].cost_bn)),full.costs[G],"fine plus unlocated generation closure "+conv+G+end);
    assertClose(full.costs[G],gen.conventions[conv][G].cost_bn[k],"saved generation source "+conv+G+end);
   }
   for(const [g,z]of Object.entries(result))if(g!=="union")assertClose(sum(Object.values(z[end].parts)),z[end].cost_bn,"program closure "+g+end);
   for(const g of GENS)if(result[g].job_capital_t1_cost_bn)result[g].job_capital_t1_cost_bn[k]+=result[g][end].cost_bn;
   const all=Object.entries(result).filter(([g])=>g!=="union").map(([,z])=>z);
   assertClose(sum(all.map(z=>z[end].cost_bn)),values[i],"whole-case closure "+conv+end);
   result.union||={};result.union[end]={cost_bn:values[i],parts:Object.fromEntries(programs.map(id=>[id,sum(all.map(z=>z[end].parts[id]))]))};
  }
  for(const G of TOPS){const names=[...GENS.filter(g=>TOP[g]===G),`unlocated_coverage_${G}`,`unlocated_calibration_${G}`];assertClose(sum(names.map(g=>result[g].population)),gen.conventions[conv][G].population,"generation population "+G,1e-6);assertClose(sum(names.map(g=>result[g].adults)),gen.conventions[conv][G].adults,"generation adult denominator "+G,1e-6);}
  assertClose(sum(Object.entries(result).filter(([g])=>g!=="union").map(([,r])=>r.population)),api.POPULATION_V9.with_coverage,"calibrated population",1e-6);
 }
 if(!probe)verifySources();
 return out;
}
if(require.main===module){if(process.argv[2]!=="--capture")fail("explicit --capture required");capture();}
module.exports={build,cellExposure,routeShares,fineRoute,countPieces,verifySources,capture,preflight,isUnlocated,requireEndSpecs,reconcileProduction};
