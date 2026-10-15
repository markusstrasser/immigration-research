/* Native-First: existing package.CASH / Engine evaluators; scratch historical probe only.
 * No producer CLI/live-case guard is modified or bypassed. No lane output is written.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");
const LANE = __dirname;
const ROOT = path.resolve(LANE, "../../..");
const args = process.argv.slice(2);
if (!args.includes("--historical-probe")) throw Error("[BLOCKED] explicit --historical-probe required");
const outIndex = args.indexOf("--out-dir");
if (outIndex < 0 || !args[outIndex+1]) throw Error("[BLOCKED] --out-dir required; historical probes never publish lane outputs");
const OUT = fs.realpathSync(args[outIndex+1]);
if (OUT === ROOT || OUT.startsWith(ROOT + path.sep)) throw Error("[BLOCKED] historical --out-dir must be outside the repository");
const caseIndex=args.indexOf("--case"), CASE=caseIndex<0?"oct14":args[caseIndex+1];
if(CASE!=="oct14") { liveCash(CASE); process.exit(0); }
const pins = JSON.parse(fs.readFileSync(path.join(LANE, "pins.json")))["oct14"];
const sources = [];
const sha = (b) => crypto.createHash("sha256").update(b).digest("hex");
const show = (commit, rel) => {
  // Generation payloads exceed Node's default 1MiB output buffer. Bound the
  // reader explicitly and fail on a transport error before parsing truncated bytes.
  const body = execFileSync("git", ["-C", ROOT, "show", `${commit}:${rel}`], {maxBuffer:256*1024*1024});
  sources.push({ commit, path: rel, sha256: sha(body) });
  return body.toString("utf8");
};
const readJson = (commit, rel) => JSON.parse(show(commit, rel));
const caseRel = "infra/immigration-fiscal/main_case_2026_10_14";
const genRel = "infra/immigration-fiscal/generation_account_2026_09_24/derived";
const summary = readJson(pins.main_case, `${caseRel}/derived/summary.json`);
const packagePath = path.join(ROOT, caseRel, "package.cjs");
if (sha(fs.readFileSync(packagePath)) !== sha(Buffer.from(show(pins.main_case, `${caseRel}/package.cjs`))))
  throw Error("[BLOCKED] current v7 package differs from pinned source");
const SET = require(packagePath), CASH = SET.CASH;
const engine = SET.Engine;
const raw = Object.fromEntries(["G1", "G2", "G3plus"].map(g => [g, readJson(pins.generation, `${genRel}/model_${g}.json`)]));
const results = {};
const checks = [];
function gate(name, value, tolerance=1e-9) {
  if (!(Number.isFinite(value) && Math.abs(value) <= tolerance)) throw Error(`[BLOCKED] ${name}: ${value} > ${tolerance}`);
  checks.push({ name, error_bn: Math.abs(value), tolerance_bn: tolerance });
}
function cells(P, model, result, spec, generation, end, i) {
  const ev = result.evaluation, scenario = P.stateFor(model, spec, P.MAIN_PROFILE).receipt_scenario;
  const base = { case: "oct14", band_end: end, spec: i, allocation: spec.allocation, generation };
  const rows = [];
  const put = (side, line, key, amount_bn, response, effect_bn) => rows.push({ ...base, side, line, key, amount_bn, response, effect_bn });
  for (const x of ev.spending) put("spending", x.id, x.key, x.amount_bn, x.response, x.effect_bn);
  for (const x of ev.receipts) put("receipt", x.id, `${scenario}:${x.key}`, x.amount_bn, x.response, x.effect_bn);
  for (const c of result.capital.components) {
    const amount = c.stock_charged_bn*spec.rate*c.key;
    gate(`capital ${generation} ${end} ${c.id}`, amount*c.response-c.return_bn);
    put("capital", `capital_${c.id}`, "", amount, c.response, -c.return_bn);
  }
  put("total", "direct_fiscal", "", 0, 0, -ev.direct_fiscal_response_bn);
  put("total", "capital_return", "", 0, 0, result.capital.total_bn);
  put("total", "production", "", 0, 0, -(ev.private_wtp_bn+ev.induced_receipts_bn));
  put("total", "cost", "", 0, 0, result.cost_bn);
  return rows;
}
for (const [basis, P] of [["set",SET], ["cash",CASH]]) {
  const correction = readJson(pins.generation, `${genRel}/generation_corrections_oct14${basis==="cash"?"_cash":""}.json`);
  const generationResults = show(pins.generation, `${genRel}/generation_results_oct14${basis==="cash"?"_cash":""}.csv`);
  const model = P.payloadModel();
  const groupModels = Object.fromEntries(Object.entries(raw).map(([g,m]) => [g, engine.applyCorrections(m, correction.payloads.a[g])]));
  const evaluations = P.MAIN_SPECS.map(s => P.evaluateFull(model,s,P.MAIN_PROFILE));
  const groupEvaluations = P.MAIN_SPECS.map(s => Object.fromEntries(Object.entries(groupModels).map(([g,m]) => [g,P.evaluateFull(m,s,P.MAIN_PROFILE)])));
  evaluations.forEach((r,i) => gate(`${basis} generation union spec${i}`, Object.values(groupEvaluations[i]).reduce((a,x)=>a+x.cost_bn,0)-r.cost_bn));
  const costs = evaluations.map(r=>r.cost_bn), lo=costs.indexOf(Math.min(...costs)), hi=costs.indexOf(Math.max(...costs));
  const want = summary.v7.end_specifications[basis];
  if (lo!==want[0] || hi!==want[1]) throw Error(`[BLOCKED] ${basis} endpoints differ from principal summary`);
  const oracle = basis==="cash"?summary.v7.cash_set_bn:summary.v7.band_bn;
  gate(`${basis} exact low oracle`,costs[lo]-oracle[0],1e-6);
  gate(`${basis} exact high oracle`,costs[hi]-oracle[1],1e-6);
  const lines=[], unionLines=[], specs=[];
  for(const [end,i] of [["low",lo],["high",hi]]) {
    const spec=P.MAIN_SPECS[i], r=evaluations[i], ev=r.evaluation;
    const total=-r.cost_bn, A=ev.direct_fiscal_response_bn-r.capital.total_bn;
    gate(`${basis} P+A+F ${end}`, total-A-ev.private_wtp_bn-ev.induced_receipts_bn);
    specs.push({ ...spec, case:"adopted_2026_10_14", band_end:end, spec_id:i,
      A_bn:A,P_bn:ev.private_wtp_bn,F_bn:ev.induced_receipts_bn,welfare_bn:total,cost_bn:r.cost_bn,
      engine_A_bn:ev.direct_fiscal_response_bn,capital_total_bn:r.capital.total_bn });
    unionLines.push(...cells(P,model,r,spec,"union",end,i));
    for(const [g,x] of Object.entries(groupEvaluations[i])) lines.push(...cells(P,groupModels[g],x,spec,g,end,i));
  }
  results[basis]={lines,union_lines:unionLines,specs,generation_results_csv:generationResults,
    payload:P.correctionsPayload(),oracle_bn:oracle,ends:[lo,hi]};
}
for(const [file] of Object.entries(require.cache)) {
  // This new runner is not a module loaded by the historical case package.
  // Validate the package's dependency bytes, not the runner's later source.
  if(file===__filename) continue;
  if(!file.startsWith(ROOT+path.sep)) continue;
  const rel=path.relative(ROOT,file), pinned=Buffer.from(show(pins.main_case,rel));
  if(sha(fs.readFileSync(file))!==sha(pinned)) throw Error(`[BLOCKED] package dependency changed: ${rel}`);
}
const winnerMeta=readJson(pins.winners,`${pins.dirs.winners}/inputs.json`);
const debt=winnerMeta.case.debt_files || winnerMeta.case.debt;
const debtRel=`infra/immigration-fiscal/debt_legacy_2026_09_23/derived/${winnerMeta.case.debt_dir}`;
const debtLines=show(debt,`${debtRel}/federal_split_2024_lines.csv`);
const debtSummary=readJson(debt,`${debtRel}/summary.json`);
const output={mode:"historical_probe",case:"oct14",package_set:"cash",results,checks,
  winner_meta:winnerMeta,debt_lines_csv:debtLines,
  induced_receipts_federal_share:debtSummary.induced_receipts_federal_share_2024,
  sources};
fs.writeFileSync(path.join(OUT,"pension-cash-cells.json"),JSON.stringify(output,null,2)+"\n");
console.log(JSON.stringify({ verdict:"PASS",ends:results.cash.ends,cash_oracle_bn:results.cash.oracle_bn,
  checks:checks.length,source_files:sources.length }));

function liveCash(caseKey) {
  const pins=JSON.parse(fs.readFileSync(path.join(LANE,"pins.json")))[caseKey];
  if(!pins)throw Error(`[BLOCKED] no source pins for case ${caseKey}`);
  const caseDir=pins.case_lane || `infra/immigration-fiscal/main_case_${pins.model.replace("adopted_","")}`;
  const sourceRows=[],seen=new Set(),checks=[];
  const hash=body=>crypto.createHash("sha256").update(body).digest("hex");
  const read=(rel,commit)=>{
    const body=commit?execFileSync("git",["-C",ROOT,"show",`${commit}:${rel}`],{maxBuffer:256*1024*1024}):fs.readFileSync(path.join(ROOT,rel));
    if(commit&&!body.equals(fs.readFileSync(path.join(ROOT,rel))))throw Error(`[BLOCKED] source differs from pinned ${commit}:${rel}`);
    const key=`${commit||"sha256"}:${rel}`;
    if(!seen.has(key)){sourceRows.push({commit:commit||null,path:rel,sha256:hash(body)});seen.add(key);}
    return body.toString("utf8");
  };
  const gate=(name,error,tolerance=1e-9)=>{
    if(!Number.isFinite(error)||Math.abs(error)>tolerance)throw Error(`[BLOCKED] ${name}: ${error}`);
    checks.push({name,error_bn:Math.abs(error),tolerance_bn:tolerance});
  };
  const summary=JSON.parse(read(`${caseDir}/derived/summary.json`,pins.main_case));
  const P0=require(path.join(ROOT,caseDir,"package.cjs"));
  const split=require("../generation_account_2026_09_24/v8_split.cjs");
  const {capitalAmount}=require("./capital_amount.cjs");
  const genDir=pins.dirs?.generation||"infra/immigration-fiscal/generation_account_2026_09_24/derived";
  const genFile=name=>pins.files?.generation?.[name]||name;
  const raw=Object.fromEntries(["G1","G2","G3plus"].map(g=>[g,JSON.parse(read(`${genDir}/model_${g}.json`,pins.generation))]));
  const principal=summary.v9 || summary.v8;
  if(!principal)throw Error("[BLOCKED] case has no principal end specification contract");
  const results={};
  for(const [basis,P] of [["set",P0],["cash",P0.CASH]]) {
    const suffix=basis==="cash"?"_cash":"";
    const corrFile=genFile("generation_corrections.json").replace(/\.json$/,`${suffix}.json`);
    const resultFile=genFile("generation_results.csv").replace(/\.csv$/,`${suffix}.csv`);
    const corr=JSON.parse(read(`${genDir}/${corrFile}`,pins.generation));
    const generationResults=read(`${genDir}/${resultFile}`,pins.generation);
    const payload=P.correctionsPayload(),model=P.payloadModel(),ev=split.evaluator(payload,P);
    const models=Object.fromEntries(Object.entries(raw).map(([g,m])=>[g,P.Engine.applyCorrections(m,corr.payloads.a[g])]));
    const evaluations=P.MAIN_SPECS.map(s=>P.evaluateFull(model,s,P.MAIN_PROFILE));
    const groupEvals=P.MAIN_SPECS.map(s=>Object.fromEntries(Object.entries(models).map(([g,m])=>[g,ev.evaluateFull(m,s)])));
    const costs=evaluations.map(r=>r.cost_bn),lo=costs.indexOf(Math.min(...costs)),hi=costs.indexOf(Math.max(...costs));
    const listed=principal.end_specifications[basis],ends=Array.isArray(listed[0])?listed[0]:listed;
    if(lo!==ends[0]||hi!==ends[1])throw Error("[BLOCKED] cash producer end specifications differ from case");
    const oracle=basis==="cash"?principal.cash_set_bn:principal.band_bn;
    gate(`${basis} low oracle`,costs[lo]-oracle[0],1e-6);gate(`${basis} high oracle`,costs[hi]-oracle[1],1e-6);
    const lines=[],unionLines=[],specs=[];
    function cells(m,r,s,g,end,i) {
      const rows=[],base={case:caseKey,band_end:end,spec:i,allocation:s.allocation,generation:g};
      const put=(side,line,key,amount_bn,response,effect_bn)=>rows.push({...base,side,line,key,amount_bn,response,effect_bn});
      const scenario=P.stateFor(m,s,P.MAIN_PROFILE).receipt_scenario;
      for(const x of r.evaluation.spending)put("spending",x.id,x.key,x.amount_bn,x.response,x.effect_bn);
      for(const x of r.evaluation.receipts)put("receipt",x.id,`${scenario}:${x.key}`,x.amount_bn,x.response,x.effect_bn);
      for(const c of r.capital.components)put("capital",`capital_${c.id}`,"",capitalAmount(c,payload.meta.capital_return,s.reading),c.response,-c.return_bn);
      put("post_engine","mixed_unit_removal","",r.post_engine.mixed_unit_removal_bn,1,-r.post_engine.mixed_unit_removal_bn);
      let coveredProduction=0;
      payload.meta.coverage.by_end[end].decomposition.line_parts.forEach((part,index)=>{
        const amount=g==="union"||part.generation===g?part.coverage_bn:0;
        if(part.economic_class==="production"){coveredProduction+=amount;return;}
        put("coverage",`coverage_${index}_${part.generation}_${part.line}`,"",amount,1,-amount);
      });
      put("total","direct_fiscal","",0,0,-r.evaluation.direct_fiscal_response_bn);
      put("total","capital_return","",0,0,r.capital.total_bn);
      put("total","post_engine","",0,0,r.post_engine.total_bn);
      put("total","production","",0,0,-r.evaluation.private_wtp_bn-r.evaluation.induced_receipts_bn+coveredProduction);
      put("total","cost","",0,0,r.cost_bn);
      const fiscal=rows.filter(x=>x.side!=="total").reduce((a,x)=>a-x.effect_bn,0);
      gate(`${basis} cells close ${g} ${end}`,fiscal+rows.find(x=>x.side==="total"&&x.line==="production").effect_bn-r.cost_bn);
      return rows;
    }
    for(const [end,i] of [["low",lo],["high",hi]]) {
      const s=P.MAIN_SPECS[i],r=evaluations[i],coverage=payload.meta.coverage.by_end[end].decomposition.production;
      const p=r.evaluation.private_wtp_bn+coverage.P_bn,f=r.evaluation.induced_receipts_bn+coverage.F_bn;
      const a=-r.cost_bn-p-f;
      specs.push({...s,case:pins.model,band_end:end,spec_id:i,A_bn:a,P_bn:p,F_bn:f,welfare_bn:-r.cost_bn,cost_bn:r.cost_bn,
        engine_A_bn:r.evaluation.direct_fiscal_response_bn,capital_total_bn:r.capital.total_bn});
      unionLines.push(...cells(model,r,s,"union",end,i));
      for(const [g,x]of Object.entries(groupEvals[i]))lines.push(...cells(models[g],x,s,g,end,i));
      gate(`${basis} generations close ${end}`,Object.values(groupEvals[i]).reduce((a,x)=>a+x.cost_bn,0)-r.cost_bn);
    }
    results[basis]={lines,union_lines:unionLines,specs,generation_results_csv:generationResults,payload,oracle_bn:oracle,ends:[lo,hi]};
  }
  // Capture the package's complete admitted raw/dependency graph as exact hashes.
  // The existing snapshot verifies ignored data against their producer's pins.
  if(caseKey==="oct15") {
    const graph=require("./v8_snapshot.cjs").verify();
    for(const rel of Object.keys(graph.sha256).sort())if(!rel.startsWith("infra/immigration-fiscal/world_ledger_2026_09_27/"))read(rel);
  }
  for(const file of Object.keys(require.cache).sort()) {
    if(file.startsWith(ROOT+path.sep)&&file!==__filename)read(path.relative(ROOT,file));
  }
  const output={mode:"exact_package_cash",case:caseKey,package_set:"cash",results,checks,
    financing_status:`[BLOCKED: no ${caseKey} federal split] debt beside is excluded from readings`,sources:sourceRows};
  fs.writeFileSync(path.join(OUT,"pension-cash-cells.json"),JSON.stringify(output,null,2)+"\n");
  console.log(JSON.stringify({verdict:"PASS",case:caseKey,ends:results.cash.ends,cash_oracle_bn:results.cash.oracle_bn,checks:checks.length,source_files:sourceRows.length}));
}
