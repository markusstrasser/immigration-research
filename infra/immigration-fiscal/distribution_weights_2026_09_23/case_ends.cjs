/* Live main case v8 (oct15) at its personal band ends.
 * Complete package evaluation carries every spending/receipt edit and response.
 * Capital return, capped programs and the set-minus-cash accrual are exported
 * alongside the engine's A, P and F. The preceding v6 grid is read as frozen
 * provenance, never rerun. Gates compare the band to summary.json (1e-9), the
 * adopted CSV row (1e-4), v8's personal set/cash ends, and cost = -(P+F)-A.
 * Earlier derived case files are frozen.
 * Run: node case_ends.cjs [--case oct15] [--out-dir DIR]
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.resolve(__dirname, "..");
const OCT14_LANE = "main_case_2026_10_14";
const OCT15_LANE = "main_case_2026_10_15";
const CASES = { oct15: OCT15_LANE };
// The preceding adopted case's frozen production grid, compared at the live case's cells.
const PREVIOUS_GRID = { oct15: OCT14_LANE };
const DEFAULT_CASE = "oct15";
const argv = process.argv.slice(2);
const opt = (name, dflt) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : dflt);
const CASE = opt("--case", DEFAULT_CASE);
if (!CASES[CASE]) throw new Error(`[BLOCKED] unknown case ${CASE}`);
const LANE = CASES[CASE];
const OUT = path.resolve(opt("--out-dir", path.join(__dirname, "derived")));

const P = require(path.join(FISCAL, LANE, "package.cjs"));
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
const REPORTER_SOURCE="union_completion_2026_10_14/_cache/set/oct14/lines.json";
const reporterSource=readJson(REPORTER_SOURCE);
const currentPayload=readJson(`${LANE}/derived/corrections.json`);
const coverageMeta=currentPayload.meta.coverage;
const coverageFile=coverageMeta?.file;
const coverageSource=coverageFile?readJson(coverageFile):null;
if(coverageMeta && (coverageMeta.stub||sha256(coverageFile)!==coverageMeta.sha256))throw Error("[BLOCKED] missing/stale live coverage decomposition");
const coverageAt=end=> {
  if(!coverageMeta)return {capital_by_level_bn:{federal:0,state_local:0},production:{P_bn:0,F_bn:0},unclassified_bn:0};
  const q=coverageSource.sets.set.scenarios[coverageMeta.construction].ends[end].decomposition;
  if(!q||!Object.values(q.capital_by_level_bn).every(Number.isFinite)||![q.production.P_bn,q.production.F_bn,q.unclassified_bn].every(Number.isFinite))throw Error("[BLOCKED] coverage class/level decomposition missing");
  return q;
};
const bandsText = fs.readFileSync(path.join(FISCAL, LANE, "derived/main_case_bands.csv"), "utf8").trim().split("\n");
const adoptedRow = bandsText.map((l) => l.split(",")).find((r) => r[0] === P.MAIN_PROFILE && r[1] === "adopted");
if (!adoptedRow) throw new Error(`[BLOCKED] ${LANE} main_case_bands.csv has no ${P.MAIN_PROFILE}/adopted row`);

console.log(`[${CASE}: ${LANE}, profile ${P.MAIN_PROFILE}]`);
const models = METHODS.map((m) => P.modelFor("central", m, P.withCentral({})));
const runs = models.map((m) => P.MAIN_SPECS.map((s) => P.evaluateFull(m, s, P.MAIN_PROFILE)));
const costs = runs.map((xs) => xs.map((r) => r.cost_bn));
const ends = costs.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
gate("the live case uses personal specifications and the v8 set ends", P.MAIN_SPECS.length === 32
  && P.MAIN_SPECS.every((s) => s.allocation === "personal")
  && JSON.stringify(ends) === JSON.stringify(summary.v8.end_specifications.set), JSON.stringify(ends));
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
const level = (r, lv) => r.capital.components.filter((c) => c.level === lv).reduce((a, c) => a + c.return_bn, 0);
const END = ["low", "high"].map((name, e) => ({ name,
  cost_bn: at(e, (r) => r.cost_bn),
  capital_return_bn: at(e, (r) => r.capital.total_bn+reporterCapital(r))+Object.values(coverageAt(name).capital_by_level_bn).reduce((s,v)=>s+v,0),
  capital_engine_bn:at(e,r=>r.capital.total_bn),reporter_capital_bn:at(e,r=>reporterCapital(r)),
  capital_return_by_level_bn: { state_local: at(e, (r) => level(r, "state_local")+reporterCapital(r,"state_local"))+coverageAt(name).capital_by_level_bn.state_local, federal: at(e, (r) => level(r, "federal")+reporterCapital(r,"federal"))+coverageAt(name).capital_by_level_bn.federal },
  capped_bn: Object.fromEntries(Object.keys(cappedLines).map((id) => [id, at(e, (r) => cappedCost(r, id))])),
  block_grant_bn: { [BLOCK_GRANT]: at(e, (r) => row(r, BLOCK_GRANT).response * row(r, BLOCK_GRANT).amount_bn+completionCost(r,BLOCK_GRANT)) },
  post_engine_bn:at(e,r=>r.post_engine.total_bn),
  coverage_bn:at(e,r=>r.post_engine.coverage_bn),mixed_unit_removal_bn:at(e,r=>r.post_engine.mixed_unit_removal_bn),
  coverage_decomposition:coverageAt(name),unclassified_cost_bn:coverageAt(name).unclassified_bn }));

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
const cap={total_bn:summary.capital_at_end_specifications.total_bn,by_level_bn:Object.fromEntries(["state_local","federal"].map(lv=>[lv,[0,1].map(e=>mean(ends.map((ij,m)=> {
  const row=perSpec.find(r=>r.method===METHODS[m]&&+r.spec===ij[e]);
  if(!row)throw Error("[BLOCKED] no live per-spec capital row");
  return currentPayload.meta.capital_return.components.filter(c=>c.level===lv).reduce((v,c)=>v+Number(row[`capital_${c.id}_bn`]),0);
})))]))};
gate("the capital return equals capital_at_end_specifications, in total and by level (1e-9)",
  worst(END.flatMap((x, j) => [x.capital_engine_bn - cap.total_bn[j], x.capital_return_by_level_bn.state_local - at(j,r=>reporterCapital(r,"state_local"))-x.coverage_decomposition.capital_by_level_bn.state_local-cap.by_level_bn.state_local[j],
    x.capital_return_by_level_bn.federal - at(j,r=>reporterCapital(r,"federal"))-x.coverage_decomposition.capital_by_level_bn.federal-cap.by_level_bn.federal[j]])) < 1e-9,
  END.map((x) => `${x.capital_return_bn.toFixed(4)} (federal ${x.capital_return_by_level_bn.federal.toFixed(4)})`).join(" / "));
gate("rental assistance equals lines_at_end_specifications.housing_subsidies.added_bn (1e-9)",
  worst(END.map((x, j) => x.capped_bn.housing_subsidies - summary.lines_at_end_specifications.housing_subsidies.added_bn[j]-at(j,r=>completionCost(r,"housing_subsidies")))) < 1e-9,
  END.map((x) => x.capped_bn.housing_subsidies.toFixed(4)).join(" / "));
const responses = ends.flatMap((ij, m) => ij.flatMap((i) => Object.keys(cappedLines)
  .map((id) => row(runs[m][i], id, id in CAPPED ? "spending" : "receipts").response)));
gate(`every capped line (${Object.keys(cappedLines).join(", ")}) responds at 1 at every end specification`,
  responses.every((r) => r === 1), `${responses.length} rows`);
for (const id of cappedReceipts) {
  const rec = summary.receipts_at_end_specifications[id];
  gate(`${id}'s capped cost is -receipts_at_end_specifications.${id}.effect_bn (1e-9)`,
    worst(END.map((x, j) => x.capped_bn[id] + rec.effect_bn[j]-at(j,r=>completionCost(r,id)))) < 1e-9, END.map((x) => x.capped_bn[id].toFixed(4)).join(" / "));
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
    const cov=coverageAt(name),caseP=engineP+rp.P_bn+cov.production.P_bn,caseF=engineF+rp.F_bn+cov.production.F_bn;
    gate(`${name} end: P and F are the payload grid's at that cell (exact)`,
      engineP === payload.production.private_wtp_bn[index] && engineF === payload.production.induced_receipts_bn[index],
      `cell ${index}: P ${caseP}, F ${caseF}`);
    const A = at(e, (r) => r.evaluation.direct_fiscal_response_bn - r.capital.total_bn-r.post_engine.total_bn+reporterProduction(r,name).cost_bn)-cov.production.P_bn-cov.production.F_bn;
    gate(`${name} end: cost = -(P + F) - A (1e-9)`, Math.abs(END[e].cost_bn + caseP + caseF + A) < 1e-9);
    production.ends[name] = { normalization: cells[0].normalization, cell_index: index,
      case: { P_bn: caseP, F_bn: caseF }, engine_grid:{P_bn:engineP,F_bn:engineF},reporter:rp,coverage:cov.production,
      model_json: { P_bn: MODEL.production.private_wtp_bn[index], F_bn: MODEL.production.induced_receipts_bn[index] },
      A_bn: A };
    if (previous) production.ends[name].previous = { lane: PREVIOUS_GRID[CASE], P_bn: previous.private_wtp_bn[index], F_bn: previous.induced_receipts_bn[index] };
  });
}
// A payload with the pension switch (September 29): the accrual is the case less its cash set at the end specifications
// (social security and Medicare at the accrual, federal income tax net of the tax on benefits). It sits inside A; it is
// not financed today, so distribute.py reports it apart from the cash part of the fiscal channel.
let pensionAccrual = null;
if (payload.meta.pension_accrual && summary.change_at_fixed_specifications.item_pension) {
  const item = summary.change_at_fixed_specifications.item_pension, cash = summary.cash_set;
  gate("the pension accrual is change_at_fixed_specifications.item_pension, the case less its cash set (1e-9)",
    JSON.stringify(cash.end_specifications) === JSON.stringify(ends) && worst(item.map((x, j) => x + cash.change_from_main_case_bn[j])) < 1e-9,
    item.map((x) => x.toFixed(4)).join(" / "));
  pensionAccrual = { rule: "the case less its cash set at the end specifications (summary.json cash_set, the pension switch off), "
    + "change_at_fixed_specifications.item_pension; a cost inside A", ends: { low: item[0], high: item[1] } };
} else if (payload.meta.pension_accrual) {
  const cashModels=METHODS.map(m=>P.CASH.modelFor("central",m,P.CASH.withCentral({})));
  const cashRuns=cashModels.map(m=>P.CASH.MAIN_SPECS.map(s=>P.CASH.evaluateFull(m,s,P.MAIN_PROFILE)));
  const cashCosts=cashRuns.map(rs=>rs.map(r=>r.cost_bn));
  const cashEnds=cashCosts.map(xs=>[xs.indexOf(Math.min(...xs)),xs.indexOf(Math.max(...xs))]);
  const cashBand=[0,1].map(e=>mean(cashEnds.map((ij,m)=>cashCosts[m][ij[e]])));
  const cash={band_bn:cashBand,end_specifications:cashEnds,change_from_main_case_bn:cashBand.map((v,j)=>v-band[j])};
  const item=band.map((v,j)=>v-cash.band_bn[j]);
  gate("the cash band and ends are v8's personal cash set (1e-9)",
    JSON.stringify(cash.end_specifications) === JSON.stringify(summary.v8.end_specifications.cash)
    && worst(cash.band_bn.map((x, j) => x - summary.v8.cash_set_bn[j])) < 1e-9);
  gate("the pension accrual is the case less its cash set (cash_set at the case's end specifications; its band is the case's "
    + "plus change_from_main_case_bn, 1e-9)", JSON.stringify(cash.end_specifications) === JSON.stringify(ends)
    && worst(cash.band_bn.map((x, j) => x - band[j] - cash.change_from_main_case_bn[j])) < 1e-9, item.map((x) => x.toFixed(4)).join(" / "));
  pensionAccrual = { rule: "v8 set less independently evaluated cash at the same personal ends; includes coverage's set-minus-cash price difference; a cost inside A", ends: { low: item[0], high: item[1] } };
}
if (failed) {
  console.error(`${failed} gate(s) failed; nothing written`);
  process.exit(1);
}
const out = { case: CASE, lane: LANE, profile: P.MAIN_PROFILE,
  rule: "each fill-in method's end specifications of the case, averaged; capped programs = the group's amount x response",
  capped_lines: cappedLines, block_grant_line: BLOCK_GRANT,
  inputs: Object.fromEntries([`${LANE}/derived/summary.json`, `${LANE}/derived/main_case_bands.csv`, `${LANE}/package.cjs`,
    REPORTER_SOURCE,...(coverageFile?[coverageFile]:[]),
    ...(production ? [PAYLOAD_REL,`${LANE}/derived/corrections_cash.json`,`${LANE}/derived/per_spec.csv`] : []), ...(production && PREVIOUS_REL ? [PREVIOUS_REL] : [])].map((rel) => [rel, sha256(rel)])),
  end_specifications: ends.map((ij, m) => ({ method: METHODS[m], low: ij[0], high: ij[1] })),
  ends: Object.fromEntries(END.map(({ name, ...x }) => [name, x])) };
if (production) out.production = production;
if (pensionAccrual) out.pension_accrual = pensionAccrual;
fs.mkdirSync(OUT, { recursive: true });
const file = path.join(OUT, `case_ends_${CASE}.json`);
fs.writeFileSync(file, JSON.stringify(out, null, 1) + "\n");
const rel = path.relative(FISCAL, file);
console.log(`wrote ${rel.startsWith("..") ? file : rel}`);
