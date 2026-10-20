/* Actual oct16 eligible source exposures, before the nonresponse sensitivity.
 * All amounts below are response-weighted; coverage remains unlocated/fixed.
 */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const P=require("../main_case_2026_10_16/package.cjs");
const F=path.resolve(__dirname,".."),records={},hashes={};
const caseSummary=P.readJson("main_case_2026_10_16/derived/summary.json");
if(caseSummary.v9.status!=='adopted')throw Error('[BLOCKED] oct16 production exposures require the adopted case');
for(const file of ["main_case_2026_10_16/derived/corrections.json","main_case_2026_10_16/derived/corrections_cash.json",
  "main_case_2026_10_16/derived/summary.json","count_composition_r5_2026_10_15/derived/native_person_factors.parquet",
  "count_composition_r5_2026_10_15/derived/line_parts_set.csv","count_composition_r5_2026_10_15/derived/line_parts_cash.csv"])
  hashes[file]=crypto.createHash("sha256").update(fs.readFileSync(path.join(F,file))).digest("hex");
for(const [which,api] of [["set",P],["cash",P.CASH]]){
  const payload=api.correctionsPayload(),meta=payload.meta;
  for(const id of ['native_minor_calibration','coverage_tenure']){
    const file=meta[id].parts_file;
    hashes[file]=crypto.createHash('sha256').update(fs.readFileSync(path.join(F,file))).digest('hex');
  }
  const saved=P.readJson(`main_case_2026_10_16/derived/corrections${which==="cash"?"_cash":""}.json`);
  if(JSON.stringify(payload)!==JSON.stringify(saved)||meta.coverage.stub)throw Error("[BLOCKED] oct16 payload not final/matching");
  const model=api.payloadModel(),costs=api.MAIN_SPECS.map(s=>api.evaluateFull(model,s).cost_bn);
  const ends=[costs.indexOf(Math.min(...costs)),costs.indexOf(Math.max(...costs))];
  const wanted=which==="cash"?caseSummary.cash_set.band_bn:caseSummary.main_case;
  records[which]={};
  for(const [j,end] of ["low","high"].entries()){
    const s=api.MAIN_SPECS[ends[j]],r=api.evaluateFull(model,s),lines={};
    if(Math.abs(r.cost_bn-wanted[j])>1e-9)throw Error("[BLOCKED] oct16 exposure exact case gate");
    const oracle=api.csvRows("main_case_2026_10_16/derived/main_case_bands.csv").find(q=>
      q.variant===(which==="cash"?"cash_set":"adopted")&&q.profile===api.MAIN_PROFILE);
    if(!oracle||Math.abs(r.cost_bn-Number(oracle[`cost_${end}_bn`]))>5e-5)throw Error("[BLOCKED] oct16 external band gate");
    const add=(side,id,amount)=>{
      const key=side+"|"+id;
      if(!lines[key])lines[key]={side,id,amount_bn:0,response:1,exposure:"response-weighted source dollars"};
      lines[key].amount_bn+=amount;
    };
    for(const row of r.evaluation.receipts)add("receipt",row.id,row.amount_bn*row.response);
    for(const row of r.evaluation.spending){
      const c=meta.union_completion.carriers[row.id];
      if(!c)add("spending",row.id,row.amount_bn*row.response);
      else if(c.kind==="line")add(c.side,c.parent_line,(c.side==="receipt"?-1:1)*row.amount_bn*row.response);
    }
    // Military response0 and partial administration are routed on their own
    // existing source cells. College operating changes retain their source key.
    for(const id of Object.values(P.SPEND.IDS))
      for(const row of r.v9_post_engine.parts[id]||[])if(row.population!=="coverage"&&row.kind!=="college_capital"
        &&row.side!=='capital'&&row.source_side!=='capital'&&row.economic_class!=='capital_return')
        add("spending",row.source_line||row.line,row.delta_bn);
    for(const id of ["native_minor_calibration","coverage_tenure"])
      for(const row of P.RATE.countParts(meta[id],end))if(row.economic_class==="fiscal_line"){
        const delta=Number(row.observed_change_bn)*(row.scenario===meta[id].subtract_parts_scenario?-1:1);
        add(row.source_side,row.source_line,(row.source_side==="receipt"?-1:1)*delta);
      }
    records[which][end]={specification:ends[j],case_bn:r.cost_bn,lines,fixed_post_engine:r.post_engine,population:meta.population_v9};
  }
}
const out={case_key:"oct16",source_hashes:hashes,records,coverage_reweighted:false,mixed_unit_reweighted:false,
  rule:"Response-weighted own source cells, observed calibration and completion; military/partial-administration/college source changes applied once. Constructed coverage, mixed-unit construction, capital and production fixed. Source-key ratio transport remains a first-order assumption."};
const memory=JSON.parse(require('child_process').execFileSync('uv',['run','--no-project','python3',
  path.join(F,'main_case_2026_10_16/memory_for_pid.py'),String(process.pid),String(process.resourceUsage().maxRSS)],{encoding:'utf8'}));
if(!memory.pass)throw Error('[BLOCKED] nonresponse exposures physical footprint exceeds shared budget');
fs.writeFileSync(path.join(__dirname,"derived/v9_exposures.json"),JSON.stringify(out,null,1)+"\n");
console.log("oct16 exposure set/cash ends, own source cells and external band gates pass");
