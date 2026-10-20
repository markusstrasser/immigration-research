/* Source-preserving oct16 cells. New typed post parts keep their fiscal signs,
 * service parents and exact generation amounts; no whole-case scaling. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {execFileSync}=require("child_process");
const {semanticHash,sourceRecordId}=require("./source_identity.cjs");
const {relocatedRecord}=require("../scripts/historical_paths.cjs");
const HERE=__dirname,ROOT=path.resolve(HERE,"../../.."),FISCAL=path.dirname(HERE);
const GENS=["G1","G2","G3plus"],sum=xs=>xs.reduce((a,b)=>a+b,0);
const read=f=>JSON.parse(fs.readFileSync(f,"utf8"));
const sha=f=>crypto.createHash("sha256").update(fs.readFileSync(relocatedRecord(f))).digest("hex");
const snapshot=read(path.join(HERE,"inputs/oct16_source_hashes.json"));
function verify(){for(const [rel,want]of Object.entries(snapshot.sha256))if(sha(path.join(ROOT,rel))!==want)throw Error("[BLOCKED] changed oct16 input "+rel);}
verify();
const begin=process.hrtime.bigint();
const P0=require("../main_case_2026_10_16/package.cjs"),V9=require("../generation_account_2026_09_24/v9_split.cjs");
const {countParts}=require("../main_case_2026_10_16/item_rate.cjs"),{capitalAmount}=require("./capital_amount.cjs");
const principal=read(path.join(FISCAL,"main_case_2026_10_16/derived/summary.json")).v9;
// Winners' set-basis A/P/F at the end specifications (a snapshot input, hash-checked by verify()).
const winnersSpecs=(()=>{const [head,...rows]=fs.readFileSync(path.join(FISCAL,"winners_losers_2026_09_24/derived/oct16/fiscal_specs.csv"),"utf8").trim().split("\n").map(l=>l.split(","));
 const at=Object.fromEntries(head.map((h,k)=>[h,k])),out=new Map();
 for(const r of rows){if(r.length!==head.length)throw Error("[BLOCKED] winners fiscal_specs row width");out.set(Number(r[at.spec_id]),{A_bn:Number(r[at.A_bn]),P_bn:Number(r[at.P_bn]),F_bn:Number(r[at.F_bn])});}
 return out;})();
const collegeResponse=read(path.join(FISCAL,"spending_keys_r5_2026_10_15/derived/item15.json")).central_response;
console.log("[timing] v9_import_seconds="+Number(process.hrtime.bigint()-begin)/1e9);
const checks=[],results={};
function gate(name,error,tolerance=1e-9){if(!Number.isFinite(error)||Math.abs(error)>tolerance)throw Error(`[BLOCKED] ${name}: ${error}`);checks.push({name,error_bn:Math.abs(error),tolerance_bn:tolerance});}
for(const [basis,P]of [["set",P0],["cash",P0.CASH]]){
 const payload=P.correctionsPayload(),registry=payload.meta.capital_return,ends=principal.end_specifications[basis][0],oracle=basis==="set"?principal.band_bn:principal.cash_set_bn;
 const lines=[],unionLines=[],specs=[];
 for(const [j,end]of ["low","high"].entries()){
  const i=ends[j],s=P.MAIN_SPECS[i],split=V9.generationParts(P,s),full=P.evaluateFull(P.payloadModel(),s,P.MAIN_PROFILE);
  gate(`${basis}/${end} principal`,full.cost_bn-oracle[j]);
  const originalParts=payload.meta.coverage.by_end[end].decomposition.line_parts;
  const extra=[];
  // New count parts are the source's joint-minus16 definition, not stacked arms.
   for(const id of ["native_minor_calibration","coverage_tenure"]){
    const occurrences=new Map();
   for(const q of countParts(payload.meta[id],end)){
     const identity=[q.scenario,q.end,q.generation,q.line,q.source_line,q.source_side,q.category,q.level,q.source_key,q.population,q.pricing,q.economic_class];
     // Source CSV declarations are not unique. Preserve their within-identity
     // source occurrence, before filtering zeros; unrelated rows cannot shift it.
     const {id:atom,occurrence}=sourceRecordId(identity,occurrences);
    if(q.delta_cost_bn===0)continue;
    let response=Number(q.source_response);
    if(q.source_side==="capital"){
     const component=split.evaluations[q.generation].capital.components.find(c=>c.id===q.source_line);
     if(!component)throw Error("[BLOCKED] count source capital has no component "+q.source_line);
     response=component.response*(q.source_line==="college"?collegeResponse:1);
    }
    const sign=q.delta_cost_bn/Number(q.change_bn);
    gate("count observed/coverage parts "+q.line,sign*(Number(q.observed_change_bn)+Number(q.coverage_change_bn))-q.delta_cost_bn);
     for(const [recipient_scope,cost]of [["counted",sign*Number(q.observed_change_bn)],["constructed_coverage",sign*Number(q.coverage_change_bn)]])if(cost!==0)
      extra.push({...q,line:`v9_${id}_${atom}_${recipient_scope}_${q.line}`,source_occurrence:occurrence,coverage_bn:cost,source_response:response,recipient_scope,
      economic_class:q.economic_class.startsWith("unclassified_")?"unclassified_residual":q.economic_class});
    }
   }
   for(const q of split.rows){
   if(["coverage_repricing","native_minor_calibration","coverage_tenure"].includes(q.id))continue;
   let source_line=q.source_line||q.line,source_side=q.source_side||q.side||"spending";
   if(q.id==="one_rate"||q.kind==="college_capital"||source_side==="capital"){
    source_side="capital";
    if(q.component==="capital_reporter")source_line=payload.meta.union_completion.carriers[q.line].parent_line;
    else if(q.component==="college_capital_interaction"||q.kind==="college_capital")source_line="college";
   }
   if(!source_line)throw Error("[BLOCKED] missing v9 source parent "+q.id);
     const identity=[q.id,q.component,q.kind,q.item,q.line,q.source_line,q.capital_source_line,q.generation,q.population,q.profile,q.part,q.origin,q.key,source_side];
    const atom=semanticHash(identity);
    for(const g of GENS)if(q.by_generation_bn[g]!==0){
     let source_response=1;
     if(source_side==="capital"){
      const component=split.evaluations[g].capital.components.find(c=>c.id===source_line);
      if(!component)throw Error("[BLOCKED] post source capital has no component "+source_line);
      source_response=component.response;
     }
     extra.push({...q,line:`v9_${q.id}_${atom}_${g}`,generation:g,source_line,source_side,
      source_response,recipient_scope:"counted",economic_class:source_side==="capital"?"capital_return":"fiscal_line",coverage_bn:q.by_generation_bn[g]});
    }
  }
   if(new Set(extra.map(q=>q.line)).size!==extra.length){
    const seen=new Set(),duplicate=extra.find(q=>seen.has(q.line)||!seen.add(q.line));
    throw Error("[BLOCKED] duplicate typed source atom identity "+JSON.stringify(extra.filter(q=>q.line===duplicate.line)));
   }
   const parts=[...originalParts,...extra];
  // Extra source rows reuse the explicit source-cell valuation contract; no
  // part is concealed in an unclassified whole-v9 residual.
  payload.meta.coverage.by_end[end].decomposition.line_parts=parts;
  const perGen={};
  for(const g of GENS){
   const r=split.evaluations[g],m=split.models[g],ev=r.evaluation,scenario=P.stateFor(m,s,P.MAIN_PROFILE).receipt_scenario;
   const rows=[],base={case:"oct16",band_end:end,spec:i,allocation:s.allocation,generation:g};
   const put=(side,line,key,amount_bn,response,effect_bn)=>rows.push({...base,side,line,key,amount_bn,response,effect_bn});
   for(const q of ev.spending)put("spending",q.id,q.key,q.amount_bn,q.response,q.effect_bn);
   for(const q of ev.receipts)put("receipt",q.id,`${scenario}:${q.key}`,q.amount_bn,q.response,q.effect_bn);
   for(const c of r.capital.components)put("capital",`capital_${c.id}`,"",capitalAmount(c,registry,s.reading),c.response,-c.return_bn);
   put("post_engine","mixed_unit_removal","",r.post_engine.mixed_unit_removal_bn,1,-r.post_engine.mixed_unit_removal_bn);
   let addedProduction=0;
   parts.forEach((q,k)=>{const cost=q.generation===g?q.coverage_bn:0;
    if(q.economic_class==="production"){addedProduction+=cost;return;}
    put("coverage",`coverage_${k}_${q.generation}_${q.line}`,"",cost,1,-cost);});
   const production=-ev.private_wtp_bn-ev.induced_receipts_bn+addedProduction;
   put("total","direct_fiscal","",0,0,-ev.direct_fiscal_response_bn);
   put("total","capital_return","",0,0,r.capital.total_bn);
   put("total","post_engine","",0,0,split.posts[g]?sum(Object.values(split.posts[g]))+r.post_engine.total_bn:0);
   put("total","production","",0,0,production);
   put("total","cost","",0,0,split.costs[g]);
   gate(`${basis}/${end}/${g} typed cells close`,sum(rows.filter(q=>q.side!=="total").map(q=>-q.effect_bn))+production-split.costs[g]);
   perGen[g]=rows;lines.push(...rows);
  }
  const first=perGen.G1;
  for(let k=0;k<first.length;k++){
   const q={...first[k],generation:"union"};
   for(const column of ["amount_bn","effect_bn"])q[column]=sum(GENS.map(g=>perGen[g][k][column]));
   unionLines.push(q);
  }
  gate(`${basis}/${end} generation closure`,sum(GENS.map(g=>split.costs[g]))-full.cost_bn);
  const coverage=payload.meta.coverage.by_end[end].decomposition.production;
  // Rule (2026-10-20 review F5): the count/tenure production parts of items 16/17 have no measured split between
  // private gains (P) and induced receipts (F). As in the winners lane they stay in A as one unlocated carrier;
  // P and F are the engine's terms plus the coverage block's own P/F. Until then they were split by an unpinned
  // oct14 union_completion cache, which moved about $0.03bn from A to F. The cells keep the parts typed.
  const p=full.evaluation.private_wtp_bn+coverage.P_bn,f=full.evaluation.induced_receipts_bn+coverage.F_bn;
  if(basis==="set"){
   const w=winnersSpecs.get(i);
   if(!w)throw Error("[BLOCKED] winners fiscal_specs lacks end specification "+i);
   gate(`${basis}/${end} P equals winners`,p-w.P_bn);gate(`${basis}/${end} F equals winners`,f-w.F_bn);
   gate(`${basis}/${end} A equals winners`,(-full.cost_bn-p-f)-w.A_bn);
  }
  specs.push({...s,case:"adopted_2026_10_16",band_end:end,spec_id:i,A_bn:-full.cost_bn-p-f,P_bn:p,F_bn:f,welfare_bn:-full.cost_bn,cost_bn:full.cost_bn,
   engine_A_bn:full.evaluation.direct_fiscal_response_bn,capital_total_bn:full.capital.total_bn});
  console.log(`[timing] ${basis}/${end} exported; elapsed_seconds=${Number(process.hrtime.bigint()-begin)/1e9}`);
 }
 const suffix=basis==="cash"?"_cash":"";
 const generationResults=fs.readFileSync(path.join(FISCAL,`generation_account_2026_09_24/derived/generation_results_oct16${suffix}.csv`),"utf8");
 results[basis]={lines,union_lines:unionLines,specs,generation_results_csv:generationResults,payload,oracle_bn:oracle,ends};
}
verify();
const sources=Object.entries({...snapshot.sha256,[path.relative(ROOT,__filename)]:sha(__filename)}).map(([file,sha256])=>({commit:null,path:file,sha256}));
const output={mode:"exact_package_cash",case:"oct16",package_set:"cash",results,checks,sources,
 financing_status:"[BLOCKED: no oct16 federal split] debt beside is excluded from readings",
 provenance:"[WORKTREE INPUT] before/after source SHA256; typed source post parts carried by original service class"};
const target=process.argv[2];if(!target)throw Error("[BLOCKED] explicit output file required");
fs.writeFileSync(target,JSON.stringify(output,null,2)+"\n");
const memory=JSON.parse(execFileSync("uv",["run","--no-project","python3",path.join(FISCAL,"main_case_2026_10_16/memory_for_pid.py"),String(process.pid),String(process.resourceUsage().maxRSS)],{encoding:"utf8"}));
if(!memory.pass)throw Error("[BLOCKED] v9 cell physical memory limit exceeded "+memory.peak_bytes);
console.log("[memory] "+JSON.stringify(memory));
console.log(JSON.stringify({status:"PASS",checks:checks.length,peak_rss_bytes:process.resourceUsage().maxRSS*1024,seconds:Number(process.hrtime.bigint()-begin)/1e9}));
