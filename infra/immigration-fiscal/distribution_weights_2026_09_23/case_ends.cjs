/* Live main case v9 (oct16) at its personal band ends.
 * Complete package evaluation carries every spending/receipt edit and response.
 * Capital return, capped programs and the set-minus-cash accrual are exported
 * alongside the engine's A, P and F. The preceding v8 grid is read as frozen
 * provenance, never rerun. Gates compare the band to summary.json (1e-9), the
 * adopted CSV row (1e-4), v9's personal set/cash ends, and cost = -(P+F)-A.
 * Earlier derived case files are frozen.
 * Run: node case_ends.cjs [--case oct16] [--out-dir DIR]
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
let phaseStarted = process.hrtime.bigint();
const timedPhase = (phase) => {
  const now = process.hrtime.bigint();
  console.log(`[timing] ${phase}_s=${(Number(now - phaseStarted) / 1e9).toFixed(3)}`);
  phaseStarted = now;
};

const FISCAL = path.resolve(__dirname, "..");
const OCT15_LANE = "main_case_2026_10_15";
const OCT16_LANE = "main_case_2026_10_16";
const CASES = { oct16: OCT16_LANE };
// The preceding adopted case's frozen production grid, compared at the live case's cells.
const PREVIOUS_GRID = { oct16: OCT15_LANE };
const DEFAULT_CASE = "oct16";
const argv = process.argv.slice(2);
const opt = (name, dflt) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : dflt);
const CASE = opt("--case", DEFAULT_CASE);
if (!CASES[CASE]) throw new Error(`[BLOCKED] unknown case ${CASE}`);
const LANE = CASES[CASE];
const OUT = path.resolve(opt("--out-dir", path.join(__dirname, "derived")));

const P = require(path.join(FISCAL, LANE, "package.cjs"));
timedPhase("case_package_import");
const { METHODS } = P;
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
let failed = 0;
const gate = (name, ok, detail) => {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
  if (!ok) failed += 1;
};
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(...xs.map(Math.abs));

const CAPPED = { housing_subsidies: "rental assistance", energy_assistance: "LIHEAP" };
// September 29 splits public housing's enterprise deficit out of the enterprise surplus: a receipt line at the rental
// line's key. Public housing is rationed like rental assistance, so where the model has the line it is capped too
// (its cost is -effect, the group's share of the deficit at its response).
const CAPPED_RECEIPTS = { housing_enterprise_surplus: "public housing" };
const BLOCK_GRANT = "family_and_general_assistance";
const summary = readJson(`${LANE}/derived/summary.json`);
const live=summary.v9;
const countParts=require("../main_case_2026_10_16/item_rate.cjs").countParts;
const REPORTER_SOURCE="union_completion_2026_10_14/_cache/set/oct14/lines.json";
const reporterSource=readJson(REPORTER_SOURCE);
const currentPayload=readJson(`${LANE}/derived/corrections.json`);
const healthResidualId=require("../spending_keys_r5_2026_10_15/items.cjs").IDS[21];
if(!healthResidualId||!currentPayload.meta.items.some(x=>x.id===healthResidualId&&x.applied!==false))throw Error("[BLOCKED] oct16 selected item21 health residual missing");
const coverageMeta=currentPayload.meta.coverage;
const coverageFile=coverageMeta?.file;
if(coverageMeta && (coverageMeta.stub||sha256(coverageFile)!==coverageMeta.sha256))throw Error("[BLOCKED] missing/stale live coverage decomposition");
const coverageAt=end=> {
  if(!coverageMeta)return {capital_by_level_bn:{federal:0,state_local:0},production:{P_bn:0,F_bn:0},unclassified_bn:0};
  const q=coverageMeta.by_end[end].decomposition;
  if(!q||!Object.values(q.capital_by_level_bn).every(Number.isFinite)||![q.production.P_bn,q.production.F_bn,q.unclassified_bn].every(Number.isFinite))throw Error("[BLOCKED] coverage class/level decomposition missing");
  return q;
};
const bandsText = fs.readFileSync(path.join(FISCAL, LANE, "derived/main_case_bands.csv"), "utf8").trim().split("\n");
const adoptedRow = bandsText.map((l) => l.split(",")).find((r) => r[0] === P.MAIN_PROFILE && r[1] === "adopted");
if (!adoptedRow) throw new Error(`[BLOCKED] ${LANE} main_case_bands.csv has no ${P.MAIN_PROFILE}/adopted row`);

console.log(`[${CASE}: ${LANE}, profile ${P.MAIN_PROFILE}]`);
const models = METHODS.map((m) => P.modelFor("central", m, P.withCentral({})));
timedPhase("set_models_and_source_checks");
const runs = models.map((m) => P.MAIN_SPECS.map((s) => P.evaluateFull(m, s, P.MAIN_PROFILE)));
timedPhase("set_specifications");
const costs = runs.map((xs) => xs.map((r) => r.cost_bn));
const ends = costs.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
gate("the live case uses personal specifications and the v9 found set ends", P.MAIN_SPECS.length === 32
  && P.MAIN_SPECS.every((s) => s.allocation === "personal")
  && JSON.stringify(ends) === JSON.stringify(live.end_specifications.set), JSON.stringify(ends));
const at = (e, f) => mean(ends.map((ij, m) => f(runs[m][ij[e]])));
const row = (r, id, side = "spending") => {
  const x = r.evaluation[side].find((l) => l.id === id);
  if (!x) throw new Error(`[BLOCKED] the evaluation has no ${side} line ${id}`);
  return x;
};
const cappedReceipts = Object.keys(CAPPED_RECEIPTS).filter((id) => runs[0][0].evaluation.receipts.some((l) => l.id === id));
const cappedLines = { ...CAPPED, ...Object.fromEntries(cappedReceipts.map((id) => [id, CAPPED_RECEIPTS[id]])) };
// A capped line's cost: a spending line's amount at its response; a receipt line's -effect.
const completionCost=(r,id)=>r.evaluation.spending.filter(l=>P.POST_ENGINE.union_completion.carriers[l.id]?.parent_line===id).reduce((v,l)=>v-l.effect_bn,0);
const reporterCapital=(r,lv)=>r.evaluation.spending.filter(l=> {
  const src=P.POST_ENGINE.union_completion.carriers[l.id];
  if(src?.kind!=="capital")return false;
  const parent=currentPayload.meta.capital_return.components.find(c=>c.id===src.parent_line);
  if(!parent)throw Error(`[BLOCKED] reporter capital ${l.id} has no declared source level`);
  return !lv||parent.level===lv;
}).reduce((v,l)=>v-l.effect_bn,0);
const reporterProduction=(r,end)=> {
  const cost=completionCost(r,"production"),source=reporterSource.generations.G3plus[end].production;
  const den=source.private_wtp_bn+source.induced_receipts_bn;
  if(!den&&cost)throw Error("[BLOCKED] zero reporter production denominator");
  return {P_bn:den?-cost*source.private_wtp_bn/den:0,F_bn:den?-cost*source.induced_receipts_bn/den:0,cost_bn:cost,
    rule:"reporter combined production carrier split at its source endpoint P/F share [ASSUMPTION: source share transport]"};
};
const cappedCost = (r, id) => (id in CAPPED ? row(r, id).response * row(r, id).amount_bn : -row(r, id, "receipts").effect_bn)+completionCost(r,id);
const countAt=end=> {
 const parts=["native_minor_calibration","coverage_tenure"].flatMap(id=>countParts(currentPayload.meta[id],end));
 let P_bn=0,F_bn=0,cost_bn=0;
 for(const q of parts)if(q.economic_class==="production"){
  const src=reporterSource.generations[q.generation][end].production,den=src.private_wtp_bn+src.induced_receipts_bn;
  if(!den&&q.delta_cost_bn)throw Error("[BLOCKED] count production source denominator zero");
  P_bn-=q.delta_cost_bn*src.private_wtp_bn/den;F_bn-=q.delta_cost_bn*src.induced_receipts_bn/den;cost_bn+=q.delta_cost_bn;
 }
 return {parts,P_bn,F_bn,cost_bn,unclassified_bn:parts.filter(q=>q.economic_class.startsWith("unclassified_")).reduce((v,q)=>v+q.delta_cost_bn,0),
  rule:"typed count source changes, joint-minus16; production split at each source generation endpoint P/F ratio [ASSUMPTION]"};
};
const cappedAddition=(end,id)=>countAt(end).parts.filter(q=>q.source_line===id).reduce((v,q)=>v+q.delta_cost_bn,0)
 +coverageAt(end).line_parts.filter(q=>q.source_line===id).reduce((v,q)=>v+q.coverage_bn,0);
const level = (r, lv) => r.capital.components.filter((c) => c.level === lv).reduce((a, c) => a + c.return_bn, 0);
// Engine fields retain their source-rate coordinates. Apply the actual typed
// post-engine capital parts, including count16/17 and college15, once.
const componentLevel=id=>{const c=currentPayload.meta.capital_return.components.find(c=>c.id===id);if(!c)throw Error("[BLOCKED] unclassified capital component "+id);return c.level;};
const capitalChanges=(r,end,lv)=> {
 const rows=[];
 let healthStock=0,healthDelta=0;
 for(const [id,parts]of Object.entries(r.v9_post_engine.parts))for(const q of parts){
  if(id==="public_college_response"&&q.kind==="college_capital")rows.push({...q,level:componentLevel("college")});
  if(id===healthResidualId&&(q.side==="capital"||q.source_side==="capital"||q.economic_class==="capital_return")){
   if(!Number.isFinite(q.capital_stock_delta_bn))throw Error("[BLOCKED] source21 capital lacks a typed stock change");
   healthStock+=q.capital_stock_delta_bn;healthDelta+=q.delta_bn;
   rows.push({...q,level:componentLevel(q.source_line||q.line)});
  }
  if(id==="one_rate"&&q.component.startsWith("capital_engine"))rows.push({...q,level:componentLevel(q.line)});
  if(id==="one_rate"&&q.component==="capital_reporter")rows.push({...q,level:componentLevel(P.POST_ENGINE.union_completion.carriers[q.line].parent_line)});
  if(id==="one_rate"&&q.component==="college_capital_interaction")rows.push({...q,level:componentLevel("college")});
  if(id==="one_rate"&&q.component.includes("health")&&q.component.includes("capital")&&!q.component.includes("coverage")&&!q.component.includes("count")){
   rows.push({...q,level:componentLevel(q.source_line||q.line)});healthDelta+=q.delta_bn;
  }
 }
 if(Math.abs(healthDelta-healthStock*currentPayload.meta.one_rate.flat_real_equivalent)>1e-9)throw Error("[BLOCKED] source21 capital plus rate interaction differs from the declared actual capital rate");
 for(const id of ["native_minor_calibration","coverage_tenure"])for(const q of countParts(currentPayload.meta[id],end))if(q.economic_class==="capital_return")rows.push({...q,delta_bn:q.delta_cost_bn});
 return rows.filter(q=>!lv||q.level===lv).reduce((v,q)=>v+q.delta_bn,0);
};
const END = ["low", "high"].map((name, e) => ({ name,
  source_post_parts_by_method:Object.fromEntries(ends.map((ij,m)=>[METHODS[m],runs[m][ij[e]].v9_post_engine])),
  cost_bn: at(e, (r) => r.cost_bn),
  capital_return_bn: at(e, (r) => r.capital.total_bn+reporterCapital(r)+capitalChanges(r,name))+Object.values(coverageAt(name).capital_by_level_bn).reduce((s,v)=>s+v,0),
  capital_engine_bn:at(e,r=>r.capital.total_bn),reporter_capital_bn:at(e,r=>reporterCapital(r)),
  capital_return_by_level_bn: Object.fromEntries(["state_local","federal"].map(lv=>[lv,at(e,r=>level(r,lv)+reporterCapital(r,lv)+capitalChanges(r,name,lv))+coverageAt(name).capital_by_level_bn[lv]])),
  capped_bn: Object.fromEntries(Object.keys(cappedLines).map((id) => [id, at(e, (r) => cappedCost(r, id))+cappedAddition(name,id)])),
  block_grant_bn: { [BLOCK_GRANT]: at(e, (r) => row(r, BLOCK_GRANT).response * row(r, BLOCK_GRANT).amount_bn+completionCost(r,BLOCK_GRANT)) },
  post_engine_bn:at(e,r=>r.post_engine.total_bn),
  coverage_bn:at(e,r=>r.post_engine.coverage_bn+(r.post_engine.coverage_repricing_bn||0)),mixed_unit_removal_bn:at(e,r=>r.post_engine.mixed_unit_removal_bn),
  coverage_decomposition:coverageAt(name),count_decomposition:countAt(name),unclassified_cost_bn:coverageAt(name).unclassified_bn+countAt(name).unclassified_bn }));

const band = END.map((x) => x.cost_bn);
gate("resource totals close across levels and include source-side reporter/coverage capital",END.every(x=>Math.abs(x.capital_return_bn-x.capital_return_by_level_bn.federal-x.capital_return_by_level_bn.state_local)<1e-9));
if(coverageMeta) gate("coverage class/level decomposition closes the post-engine amount",END.every(x=> {
 const q=x.coverage_decomposition;
 return Math.abs(Object.values(q.capital_by_level_bn).reduce((s,v)=>s+v,0)+q.classified_fiscal_line_bn+q.unclassified_bn-q.production.P_bn-q.production.F_bn-x.coverage_bn)<1e-9;
}));
gate("the band equals summary.json main_case (1e-9)", worst(band.map((x, j) => x - summary.main_case[j])) < 1e-9,
  band.map((x) => x.toFixed(4)).join("/"));
gate("the band equals main_case_bands.csv's adopted row (1e-4, the file's rounding)",
  worst(band.map((x, j) => x - Number(adoptedRow[2 + j]))) < 1e-4, `ends ${JSON.stringify(ends)}`);
// v8's inherited by-level summary fields are historical. Its per-spec rows
// are recomputed for the live case and carry every capital component.
const perSpec=P.csvRows(`${LANE}/derived/per_spec.csv`);
const cap={total_bn:[0,1].map(e=>mean(ends.map((ij,m)=>Number(perSpec.find(r=>r.method===METHODS[m]&&+r.spec===ij[e]).capital_total_bn)))),by_level_bn:Object.fromEntries(["state_local","federal"].map(lv=>[lv,[0,1].map(e=>mean(ends.map((ij,m)=> {
  const row=perSpec.find(r=>r.method===METHODS[m]&&+r.spec===ij[e]);
  if(!row)throw Error("[BLOCKED] no live per-spec capital row");
  return currentPayload.meta.capital_return.components.filter(c=>c.level===lv).reduce((v,c)=>v+Number(row[`capital_${c.id}_bn`]),0);
})))]))};
gate("source-coordinate engine capital equals live per-spec columns, total and level (1e-9)",
  worst(END.flatMap((x, j) => [x.capital_engine_bn - cap.total_bn[j], ...["state_local","federal"].map(lv=>at(j,r=>level(r,lv))-cap.by_level_bn[lv][j])])) < 1e-9,
  END.map((x) => `${x.capital_return_bn.toFixed(4)} (federal ${x.capital_return_by_level_bn.federal.toFixed(4)})`).join(" / "));
gate("rental assistance equals lines_at_end_specifications.housing_subsidies.added_bn (1e-9)",
  worst(END.map((x, j) => x.capped_bn.housing_subsidies - cappedAddition(x.name,"housing_subsidies")-summary.lines_at_end_specifications.housing_subsidies.added_bn[j]-at(j,r=>completionCost(r,"housing_subsidies")))) < 1e-9,
  END.map((x) => x.capped_bn.housing_subsidies.toFixed(4)).join(" / "));
const responses = ends.flatMap((ij, m) => ij.flatMap((i) => Object.keys(cappedLines)
  .map((id) => row(runs[m][i], id, id in CAPPED ? "spending" : "receipts").response)));
gate(`every capped line (${Object.keys(cappedLines).join(", ")}) responds at 1 at every end specification`,
  responses.every((r) => r === 1), `${responses.length} rows`);
for (const id of cappedReceipts) {
  const rec = summary.receipts_at_end_specifications[id];
  gate(`${id}'s capped cost is -receipts_at_end_specifications.${id}.effect_bn (1e-9)`,
    worst(END.map((x, j) => x.capped_bn[id] - cappedAddition(x.name,id)+rec.effect_bn[j]-at(j,r=>completionCost(r,id)))) < 1e-9, END.map((x) => x.capped_bn[id].toFixed(4)).join(" / "));
}

// A payload that replaces the production grid: at each end, P and F on the case's grid and on model.json's at the
// production cell of the end specification (every method's end must read one cell), and the engine's A.
const PAYLOAD_REL = `${LANE}/derived/corrections.json`;
const payload = readJson(PAYLOAD_REL);
const PREVIOUS_REL = PREVIOUS_GRID[CASE] ? `${PREVIOUS_GRID[CASE]}/derived/corrections.json` : null;
let production = null;
if (payload.production) {
  const { Engine, MODEL } = P;
  const previous = PREVIOUS_REL ? readJson(PREVIOUS_REL).production : null;
  if (previous) {
    gate(`the case's production grid has ${PREVIOUS_REL}'s cells`, Object.keys(previous.dims).length===Object.keys(payload.production.dims).length
      && Engine.PRODUCTION_DIMS.every(k=>JSON.stringify(previous.dims[k])===JSON.stringify(payload.production.dims[k]))
      && ["private_wtp_bn", "induced_receipts_bn"].every((k) => previous[k].length === payload.production[k].length));
  }
  production = { rule: "the case's production grid (corrections.json production) moves P and F only: at each end, P and F "
    + "on the case's grid and on model.json's at the end specification's production cell, and A = the engine's direct "
    + "response less the capital return; cost = -(P + F) - A", grid: payload.meta.production || null, ends: {} };
  ["low", "high"].forEach((name, e) => {
    const cells = ends.map((ij, m) => P.stateFor(models[m], P.MAIN_SPECS[ij[e]], P.MAIN_PROFILE).production);
    gate(`${name} end: every method's end specification reads one production cell`,
      cells.every((c) => JSON.stringify(c) === JSON.stringify(cells[0])), JSON.stringify(cells[0]));
    const index = Engine.productionIndex(MODEL, cells[0]);
    const engineP = at(e, (r) => r.evaluation.private_wtp_bn), engineF = at(e, (r) => r.evaluation.induced_receipts_bn);
    const rp={P_bn:at(e,r=>reporterProduction(r,name).P_bn),F_bn:at(e,r=>reporterProduction(r,name).F_bn)};
    const cov=coverageAt(name),count=countAt(name),caseP=engineP+rp.P_bn+cov.production.P_bn+count.P_bn,caseF=engineF+rp.F_bn+cov.production.F_bn+count.F_bn;
    gate(`${name} end: P and F are the payload grid's at that cell (exact)`,
      engineP === payload.production.private_wtp_bn[index] && engineF === payload.production.induced_receipts_bn[index],
      `cell ${index}: P ${caseP}, F ${caseF}`);
    const A = at(e, (r) => r.evaluation.direct_fiscal_response_bn - r.capital.total_bn-r.post_engine.total_bn+reporterProduction(r,name).cost_bn)-cov.production.P_bn-cov.production.F_bn+count.cost_bn;
    gate(`${name} end: cost = -(P + F) - A (1e-9)`, Math.abs(END[e].cost_bn + caseP + caseF + A) < 1e-9);
    production.ends[name] = { normalization: cells[0].normalization, cell_index: index,
      case: { P_bn: caseP, F_bn: caseF }, engine_grid:{P_bn:engineP,F_bn:engineF},reporter:rp,coverage:cov.production,count:{P_bn:count.P_bn,F_bn:count.F_bn,rule:count.rule},
      model_json: { P_bn: MODEL.production.private_wtp_bn[index], F_bn: MODEL.production.induced_receipts_bn[index] },
      A_bn: A };
    if (previous) production.ends[name].previous = { lane: PREVIOUS_GRID[CASE], P_bn: previous.private_wtp_bn[index], F_bn: previous.induced_receipts_bn[index] };
  });
}
// A payload with the pension switch (September 29): the accrual is the case less its cash set at the end specifications
// (social security and Medicare at the accrual, federal income tax net of the tax on benefits). It sits inside A; it is
// not financed today, so distribute.py reports it apart from the cash part of the fiscal channel.
let pensionAccrual = null;
if (payload.meta.pension_accrual) {
  const cashModels=METHODS.map(m=>P.CASH.modelFor("central",m,P.CASH.withCentral({})));
  timedPhase("set_decomposition_and_cash_models");
  const cashRuns=cashModels.map(m=>P.CASH.MAIN_SPECS.map(s=>P.CASH.evaluateFull(m,s,P.MAIN_PROFILE)));
  timedPhase("cash_specifications");
  const cashCosts=cashRuns.map(rs=>rs.map(r=>r.cost_bn));
  const cashEnds=cashCosts.map(xs=>[xs.indexOf(Math.min(...xs)),xs.indexOf(Math.max(...xs))]);
  const cashBand=[0,1].map(e=>mean(cashEnds.map((ij,m)=>cashCosts[m][ij[e]])));
  const cash={band_bn:cashBand,end_specifications:cashEnds,change_from_main_case_bn:cashBand.map((v,j)=>v-band[j])};
  const item=band.map((v,j)=>v-cash.band_bn[j]);
  gate("the cash band and ends are v9's personal cash set (1e-9)",
    JSON.stringify(cash.end_specifications) === JSON.stringify(live.end_specifications.cash)
    && worst(cash.band_bn.map((x, j) => x - live.cash_set_bn[j])) < 1e-9);
  gate("the pension accrual is the case less its cash set (cash_set at the case's end specifications; its band is the case's "
    + "plus change_from_main_case_bn, 1e-9)", JSON.stringify(cash.end_specifications) === JSON.stringify(ends)
    && worst(cash.band_bn.map((x, j) => x - band[j] - cash.change_from_main_case_bn[j])) < 1e-9, item.map((x) => x.toFixed(4)).join(" / "));
  pensionAccrual = { rule: "v9 set less independently evaluated cash at the same personal ends; includes coverage's set-minus-cash price difference; a cost inside A", ends: { low: item[0], high: item[1] } };
}
if (failed) {
  console.error(`${failed} gate(s) failed; nothing written`);
  process.exit(1);
}
const out = { case: CASE, lane: LANE, profile: P.MAIN_PROFILE,
  population:currentPayload.meta.population_v9,effective_capital_rate:currentPayload.meta.one_rate.flat_real_equivalent,
  selected_source_classification:currentPayload.meta.items.filter(x=>P.V9_ITEMS.some(v=>v.id===x.id)&&x.applied!==false).map(x=>({id:x.id,scope:"source standalone controls; actual full-spec dynamic parts in ends.source_post_parts_by_method",parts:x.parts_by_line||x.post_engine_by_end||x.parts||{},source:currentPayload.meta[x.id]})),
  rule: "each fill-in method's end specifications of the case, averaged; capped programs = the group's amount x response",
  capped_lines: cappedLines, block_grant_line: BLOCK_GRANT,
  inputs: Object.fromEntries([`${LANE}/derived/summary.json`, `${LANE}/derived/main_case_bands.csv`, `${LANE}/package.cjs`,
    REPORTER_SOURCE,...(coverageFile?[coverageFile]:[]),currentPayload.meta.native_minor_calibration.parts_file,
    ...(production ? [PAYLOAD_REL,`${LANE}/derived/corrections_cash.json`,`${LANE}/derived/per_spec.csv`] : []), ...(production && PREVIOUS_REL ? [PREVIOUS_REL] : [])].map((rel) => [rel, sha256(rel)])),
  end_specifications: ends.map((ij, m) => ({ method: METHODS[m], low: ij[0], high: ij[1] })),
  ends: Object.fromEntries(END.map(({ name, ...x }) => [name, x])) };
if (production) out.production = production;
if (pensionAccrual) out.pension_accrual = pensionAccrual;
const outputBytes=Buffer.from(JSON.stringify(out,null,1)+"\n");
const memory=JSON.parse(require("child_process").execFileSync("uv",["run","--no-project","python3",path.join(FISCAL,"main_case_2026_10_16/memory_for_pid.py"),String(process.pid),String(process.resourceUsage().maxRSS)],{encoding:"utf8"}));
if(!memory.pass)throw Error("[BLOCKED] distribution endpoint physical footprint exceeds budget");
console.log("[memory] "+JSON.stringify(memory));
fs.mkdirSync(OUT, { recursive: true });
const file = path.join(OUT, `case_ends_${CASE}.json`);
fs.writeFileSync(file, outputBytes);
const rel = path.relative(FISCAL, file);
console.log(`wrote ${rel.startsWith("..") ? file : rel}`);
