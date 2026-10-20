/* Oct16 full-spec source bridge. The inherited exporter supplies its checked
 * household-placement scaffold in memory; no historical file is regenerated. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const FISCAL=path.resolve(__dirname,".."),GENS=["G1","G2","G3plus"],ENDS=["low","high"];
const SIDES=["receipt","spending","capital","production","post_engine"];
const sum=a=>a.reduce((x,y)=>x+y,0),clone=x=>JSON.parse(JSON.stringify(x));
const fail=s=>{throw Error("[BLOCKED] oct16 household export: "+s);};
const file=f=>path.join(FISCAL,f),read=f=>JSON.parse(fs.readFileSync(file(f),"utf8"));
const signatures=new Map();
const signature=(f,fresh=false)=>{if(fresh||!signatures.has(f))signatures.set(f,{file:f,sha256:crypto.createHash("sha256").update(fs.readFileSync(file(f))).digest("hex")});return signatures.get(f);};
function check(label,actual,expected,tolerance=1e-9){if(!Number.isFinite(actual)||Math.abs(actual-expected)>tolerance)fail(`${label}: ${actual} vs ${expected}`);}
function validateAtom(r){
  if(!GENS.includes(r.generation)||!Number.isFinite(r.cost_bn)||!r.item||!r.line||!r.source_line||!r.source_side||!r.population)
    fail("incomplete typed source atom "+JSON.stringify(r));
  if(!SIDES.includes(r.source_side)||
     !["engine","completion","native","observed","coverage","original_union","added_lineage"].includes(r.population))
    fail("unknown typed source route "+JSON.stringify(r));
  return r;
}
function population(line,declared){
  if(declared)return declared;
  if(line?.startsWith("union_completion_"))return "completion";
  if(line?.startsWith("native_child_"))return "native";
  return "engine";
}
function sideOf(row,block){
  // Source21 declares side directly. Preserve its authoritative declaration
  // before consulting legacy source_side and inferred legacy component types.
  const declared=row.side!==undefined?row.side:row.source_side;
  if(declared!==undefined){
    if(!SIDES.includes(declared))fail("unknown declared source side "+JSON.stringify(declared));
    return declared;
  }
  if(row.kind==="college_capital"||row.component?.startsWith("capital_"))return "capital";
  if(block?.some(c=>c.id===row.line))return "capital";
  return "spending";
}
function rowsOf(ev){
  return ev.evaluation.receipts.map(r=>({...r,source_side:"receipt"}))
    .concat(ev.evaluation.spending.map(r=>({...r,source_side:"spending"})));
}
function countRows(api,item,end){
  const block=api.correctionsPayload().meta[item];if(!block)return [];
  const raw=fs.readFileSync(file(block.parts_file),"utf8").trimEnd().split("\n").map(s=>s.split(",")),head=raw.shift();
  if(raw.some(r=>r.length!==head.length))fail("typed count CSV schema changed");
  const rows=raw.map(r=>Object.fromEntries(head.map((h,i)=>[h,r[i]]))),selected=[];
  for(const [scenario,sign]of [[block.parts_scenario,1],[block.subtract_parts_scenario,-1]])if(scenario)
    for(const r of rows)if(r.scenario===scenario&&r.end===end)selected.push({...r,sign});
  check(item+" selected count-source closure",sum(selected.map(r=>r.sign*Number(r.change_bn))),block.by_end[end].total_bn,1e-8);
  return selected.flatMap((r,index)=>{
    const sign=r.sign;
    return [["observed",Number(r.observed_change_bn)],["coverage",Number(r.coverage_change_bn)]]
      .filter(([,v])=>v!==0).map(([where,value])=>({...r,item,source_piece:`${block.parts_file}:${block.parts_scenario}:${index}:${where}`,
        population:where,cost_bn:sign*value,source:{...signature(block.parts_file),scenario:block.parts_scenario,
          subtract_scenario:block.subtract_parts_scenario||null,rule:"selected scenario minus declared predecessor; observed and coverage kept separate"}}));
  });
}
function coverageRows(prior,current,end){
  if(JSON.stringify(prior.by_end[end].decomposition)===JSON.stringify(current.by_end[end].decomposition))return [];
  const result=[];
  for(const [block,sign,origin]of [[current,1,"current"],[prior,-1,"scaffold"]]){
    const parts=block.by_end[end].decomposition?.line_parts;
    if(!parts)fail(origin+" coverage lacks typed line decomposition");
    parts.forEach((r,index)=>{if(r.coverage_bn!==0)result.push({...r,
      ...(r.economic_class==="unclassified_residual"?{source_line:r.line,source_side:"post_engine",
        source_typing_rule:"declared unclassified_residual retained as unlocated coverage; no household driver inferred"}:{}),
      item:"coverage_repricing",population:"coverage",
      cost_bn:sign*r.coverage_bn,source_piece:`${origin}:${index}`,source:{...signature(block.file),origin,rule:"current own-price coverage minus inherited coverage"}});});
  }
  return result;
}
function finalCoverageCounts(payload){
  const c=payload.meta.coverage,q=c.counts_by_generation_folded||Object.fromEntries(GENS.map(g=>[g,c.counts_by_generation[g]+(g==="G3plus"?(c.counts_by_generation.added||0):0)]));
  const out=Object.fromEntries(GENS.map(g=>[g,q[g]]));
  for(const id of ["native_minor_calibration","coverage_tenure"])for(const g of GENS)out[g]+=payload.meta[id]?.coverage_people_change_by_generation?.[g]||0;
  if(Object.values(out).some(v=>!Number.isFinite(v)))fail("missing final coverage generation source counts");
  return out;
}
function bridge(base,api,allocation,{controlItem=null,finalApi=api,selectedIds=null}={}){
  const V=require("../generation_account_2026_09_24/v9_split.cjs"),payload=api.correctionsPayload();
  const control=controlItem!==null;
  const candidates=allocation==="shared"?finalApi.ALL_SPECS:finalApi.MAIN_SPECS;
  const scope=candidates.map((s,i)=>({s,i})).filter(x=>x.s.allocation===allocation);
  const sharedRemoval=(s,g)=>{
    if(allocation!=="shared")return 0;
    const z=payload.meta.mixed_unit_removal.by_end[s.reading];
    if(!g)return z.total_bn;
    const parts=z.by_generation_bn||z.by_generation;
    return parts[g]??parts[g==="G3plus"?"G3+":g];
  };
  const cost=s=>finalApi.evaluateFull(finalApi.payloadModel(),s,finalApi.MAIN_PROFILE).cost_bn-sharedRemoval(s);
  const scores=scope.map(x=>cost(x.s));
  const found=[scope[scores.indexOf(Math.min(...scores))].i,scope[scores.indexOf(Math.max(...scores))].i];
  if(JSON.stringify(found)!==JSON.stringify(ENDS.map(e=>base.meta.spec_index[e])))fail("source scaffold and final found ends differ; final="+JSON.stringify(found)+", scaffold="+JSON.stringify(base.meta.spec_index)+"; extend scaffold specification input before exporting");
  const originalCoverage=clone(base.meta.coverage),which=base.meta.basis;
  const payloadFile=`main_case_2026_10_16/derived/corrections${which==="cash"?"_cash":""}.json`;
  if(!control&&JSON.stringify(payload)!==JSON.stringify(read(payloadFile)))fail(which+" package differs from stored final corrections payload");
  const csv=fs.readFileSync(file("main_case_2026_10_16/derived/main_case_bands.csv"),"utf8").trimEnd().split("\n").map(s=>s.split(",")),head=csv.shift();
  const bandRows=csv.map(r=>Object.fromEntries(head.map((h,i)=>[h,r[i]])));
  const variant=allocation==="shared"?(which==="set"?"shared_allocation":"shared_allocation_cash_set"):(which==="set"?"adopted":"cash_set");
  const oracle=bandRows.find(r=>r.profile===api.MAIN_PROFILE&&r.variant===variant);
  if(!oracle)fail("final case band oracle missing "+variant);
  if(!control){
    check(which+" final low band",Math.min(...scores),Number(oracle.cost_low_bn),1e-4);
    check(which+" final high band",Math.max(...scores),Number(oracle.cost_high_bn),1e-4);
  }
  base.meta.case="main_case_2026_10_16";
  base.meta.population_v9=clone(payload.meta.population_v9||payload.meta.population_v8);
  base.meta.final_coverage=clone(payload.meta.coverage);
  base.meta.final_coverage.counts_by_generation_final=finalCoverageCounts(payload);
  base.meta.final_coverage.net_missing_people_final=sum(Object.values(base.meta.final_coverage.counts_by_generation_final));
  const finalCovered=base.meta.population_v9.with_coverage-base.meta.population_v9.without_coverage;
  check("final missing-person population",base.meta.final_coverage.net_missing_people_final,finalCovered,1e-6);
  base.meta.final_coverage.population_rule="population_v9.with_coverage minus without_coverage; retained .coverage field may describe the inherited source construction";
  base.meta.v9={scaffold_case:"main_case_2026_10_15",scaffold_rule:"Fresh full-specification inherited source evaluation; old bytes never rewritten; apply every v9_parts row once after baseline placement",
    selected_items:selectedIds||payload.meta.v9?.selected_items||api.ITEM_IDS,control_item:controlItem,
    active_calibration:!!payload.meta.native_minor_calibration,
    control_selection:control?{api:"main_case_2026_10_16/package.cjs caseOf(OCT05, inherited v8 selected ids + chosen new item)",
      fixed_final_specifications:clone(base.meta.spec_index),source_item:controlItem,source_coverage_rule:"partial registry preserves delivered v8 coverage prices; count-source parts enter once on their own source kernel"}:null,
    record_factors:{...signature("count_composition_r5_2026_10_15/derived/native_person_factors.parquet"),active:!!payload.meta.native_minor_calibration,
      cells:signature("count_composition_r5_2026_10_15/derived/native_calibration.csv"),
      replicates:signature("count_composition_r5_2026_10_15/derived/native_calibration_replicates.json"),
      record_key:["PH_SEQ","PPPOS"],central_field:"central_member_factor",
      builder:signature("count_composition_r5_2026_10_15/native_measure.py"),policy:"preserve_CPS_Hispanic_total; fixed identities/rosters; apply source central_member_factor and calibrated replicates; ranking weights declared by household consumer"},
    effective_capital_rate:payload.meta.one_rate?.flat_real_equivalent||null,
    effective_capital_rate_by_end:Object.fromEntries(ENDS.map((end,k)=>[end,payload.meta.one_rate?.flat_real_equivalent||candidates[found[k]].rate])),
    source_payload:signature(payloadFile),band_oracle:{...signature("main_case_2026_10_16/derived/main_case_bands.csv"),variant,tolerance_bn:1e-4,checked:!control},
    scaffold_source_payload:signature(`main_case_2026_10_15/derived/corrections${which==="cash"?"_cash":""}.json`),
    scaffold_source_generation:signature(`generation_account_2026_09_24/derived/generation_results_oct15${which==="cash"?"_cash":""}.csv`),
    scaffold_export_source:signature("within_group_distribution_2026_09_29/export_lines.cjs"),
    scaffold_bridge_source:signature("within_group_distribution_2026_09_29/export_oct16.cjs"),
    source_generation:signature(`generation_account_2026_09_24/derived/generation_results_oct16${which==="cash"?"_cash":""}.csv`),
    parts_rule:"fiscal source prices at the complete selected specification; count observed/coverage atoms and dynamic post components remain separate",
    count_location_rule:"Observed calibration stays on existing rosters. Constructed coverage remains unlocated; no fictitious age/household allocation. Generation totals do not identify age bands.",
    controls_rule:control?"full source standalone item on inherited v8 selected registry at fixed final case endpoints; actual source evaluator and exact typed source bridge are the oracle":"conditional item toggles in this decomposition are allocation controls; separate --control-item exports rebuild standalone source item selections at the same fixed final endpoints",
    final_unlocated_scope:"Constructed coverage only; any observed count-source residual without a household driver must remain a separate explicitly unlocated calibration amount",
    post_signatures:{},final_unlocated_cost_bn:{}};
  for(const [k,end]of ENDS.entries()){
    const spec=candidates[found[k]],none=controlItem==="none",split=none?{
      costs:Object.fromEntries(GENS.map(g=>[g,base.generations[g][end].cost_bn+sharedRemoval(spec,g)])),rows:[],
      total_bn:api.evaluateFull(api.payloadModel(),spec,api.MAIN_PROFILE).cost_bn
    }:V.generationParts(api,spec,"a"),all=[];
    const post=none?{amounts:{}}:api.postFor(api.payloadModel(),spec,api.MAIN_PROFILE);
    const add=r=>{validateAtom(r);if(r.cost_bn!==0)all.push(r);};
    // The only central new engine edits are the selected household basket. Read
    // actual evaluated source amounts rather than scaling the old total.
    if(!none)for(const g of GENS){
      const after=rowsOf(split.evaluations[g]),before=base.generations[g][end].rows;
      for(const r of after){
        const old=before.find(q=>q.side===r.source_side&&q.id===r.id);
        if(!old)fail("new engine line lacks inherited placement source "+r.id);
        const state=split.evaluations[g].state||api.stateFor(split.models[g],spec,api.MAIN_PROFILE);
        const value=-state.fiscal_weight*r.effect_bn-old.cost_bn;
        if(value!==0)add({item:"consumption_tax_bases",line:r.id,source_line:payload.meta.union_completion.carriers[r.id]?.parent_line||r.id,
          source_side:r.source_side,source_key:r.key,population:population(r.id),generation:g,cost_bn:value,
          source_piece:`engine:${r.source_side}:${r.id}:${g}`,rule:"actual selected engine evaluation minus inherited source line at identical specification"});
      }
    }
    for(const item of ["native_minor_calibration","coverage_tenure"])for(const r of countRows(api,item,end))add(r);
    for(const r of coverageRows(originalCoverage,payload.meta.coverage,end))add(r);
    const expanded=new Set(["native_minor_calibration","coverage_tenure","coverage_repricing"]);
    const basket=payload.meta.consumption_tax_bases?.by_end[end];
    if(basket?.line_parts){
      expanded.add("consumption_tax_bases");
      if(post.amounts.consumption_tax_bases)for(const [index,r]of basket.line_parts.entries()){
        const source=originalCoverage.by_end[end].decomposition.line_parts.find(q=>q.source_side==="receipt"&&q.source_line===r.line&&q.generation===r.generation);
        if(!source)fail("standalone basket coverage lacks declared receipt source "+r.line);
        add({...r,item:"consumption_tax_bases",source_line:r.line,source_side:"receipt",source_key:source.source_key,
          population:"coverage",cost_bn:r.delta_cost_bn,source_piece:`basket:coverage:${index}`,rule:"source item's declared missed-person receipt ratio at this end/generation"});
      }
    }
    for(const r of split.rows){
      if(expanded.has(r.id))continue;
      for(const g of GENS){
        const value=r.by_generation_bn[g];if(value===0)continue;
        const sourceSide=sideOf(r,base.generations[g][end].capital);
        const carrier=payload.meta.union_completion.carriers[r.line];
        const cover=r.component?.includes("coverage")?originalCoverage.by_end[end].decomposition.line_parts.find(q=>q.line===r.line&&q.generation===g&&q.source_side===sourceSide):null;
        const sourceLine=r.source_line||cover?.source_line||carrier?.parent_line||r.line;
        const baseRow=base.generations[g][end].rows.find(q=>q.id===r.line)||base.generations[g][end].rows.find(q=>q.side===sourceSide&&q.id===sourceLine);
        const driverLine=r.capital_source_line||r.line;
        const capital=base.generations[g][end].capital.find(c=>c.id===driverLine||c.id===sourceLine);
        add({...r,item:r.id,line:r.line,source_line:sourceLine,source_side:sourceSide,
          source_key:r.key||cover?.source_key||baseRow?.key||null,population:r.component?.includes("coverage")?"coverage":population(r.line,r.population),generation:g,cost_bn:value,
          source_driver:{line:driverLine,side:r.kind==="college_operating"?"capital":sourceSide,
            ...(capital?{capital_component:capital.id,capital_rule:capital.rule,capital_key:capital.key}:{}),
            ...(payload.meta.union_completion.carriers[driverLine]?{completion_carrier:payload.meta.union_completion.carriers[driverLine]}:{})},
          source_piece:`post:${r.id}:${all.length}:${g}`,rule:r.rule});
      }
    }
    // postFor's zero amounts need an explicit signature too, so no new item can
    // vanish unnoticed when producer fields change.
    for(const [item,total]of Object.entries(post.amounts)){
      const atoms=all.filter(r=>r.item===item&& !r.source_piece.startsWith("engine:"));
      check(`${which}/${end}/${item} typed post closure`,sum(atoms.map(r=>r.cost_bn)),total,1e-8);
    }
    base.meta.v9.post_signatures[end]={amounts:post.amounts,typed_items:[...new Set(all.map(r=>r.item))].sort()};
    let aggregate=0;
    for(const g of GENS){
      const target=split.costs[g]-sharedRemoval(spec,g),block=base.generations[g][end],parts=all.filter(r=>r.generation===g);
      block.v9_target_cost_bn=target;block.v9_parts=parts;
      check(`${which}/${end}/${g} full source bridge`,block.cost_bn+sum(parts.map(r=>r.cost_bn)),target);
      aggregate+=target;
    }
    base.union[end].v9_parts=all;
    const target=split.total_bn-sharedRemoval(spec);
    base.union[end].v9_target_cost_bn=target;
    check(`${which}/${end} generation closure`,aggregate,target);
    check(`${which}/${end} full union bridge`,base.union[end].cost_bn+sum(all.map(r=>r.cost_bn)),target);
    const coverage=sum(all.filter(r=>r.population==="coverage").map(r=>r.cost_bn));
    base.meta.v9.final_unlocated_cost_bn[end]=sum(GENS.map(g=>base.generations[g][end].post_engine.coverage||0))+coverage;
  }
  return base;
}
function write({set,cash,allocation,atomicWrite}){
  require("../scripts/adoption_gate.cjs").requireAdopted("oct16");
  const P=require("../main_case_2026_10_16/package.cjs");
  for(const [which,base,api]of [["set",set,P],["cash",cash,P.CASH]]){
    const out=bridge(base,api,allocation),destination=path.join(__dirname,"_cache/oct16",allocation==="shared"?"shared_allocation":"",which==="set"?"lines.json":"lines_cash.json");
    require("../main_case_2026_10_16/memory_guard.cjs").requireWithinBudget("oct16 household export "+which);
    fs.mkdirSync(path.dirname(destination),{recursive:true});atomicWrite(destination,JSON.stringify(out,null,1)+"\n");
    console.log(`  ✓ oct16 ${which} ${allocation} source bridge: ${ENDS.map(e=>out.union[e].v9_target_cost_bn).join(" / ")}bn`);
  }
}
module.exports={bridge,write,countRows,coverageRows,validateAtom,finalCoverageCounts,signature,sideOf};
