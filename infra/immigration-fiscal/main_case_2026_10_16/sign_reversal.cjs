/* v9 sign-reversal readings. Keep every v8 CSV cell unchanged; append oct16_low and oct16_high.
 * Definition: S24's welfare/breakEven/frozen, with v7's rental, receipt and capital rules. Union-completion
 * real-line carriers follow the evaluated parent key and response; endpoint carriers select their reading.
 * Item 11 and coverage are fixed costs after the engine and enter welfare with the opposite sign.
 * Run: node sign_reversal.cjs [--out-dir DIR]. No old lane is written. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("./package.cjs");
const S24 = require("../main_case_2026_09_24/sign_reversal.cjs");
const { Engine } = P;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(__dirname, "derived"));
if (OUT !== path.join(__dirname, "derived") && !OUT.startsWith(__dirname + path.sep)) throw Error("[BLOCKED] sign_reversal output must stay inside v8's lane");
const oldFile = path.join(__dirname, "../main_case_2026_10_15/derived/sign_reversal.csv");
const oldLines = fs.readFileSync(oldFile, "utf8").trimEnd().split("\n"), oldRows = oldLines.map(l => l.split(","));
const oldHeader = oldRows[0], values = new Map();
const checks = [];
function gate(name, pass, detail = "") {
  checks.push({ name, pass: !!pass, detail });
  console.log(`  ${pass ? "PASS" : "FAIL"} ${name}${detail ? `: ${detail}` : ""}`);
}
const near = (a, b, eps = 1e-9) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) < eps;
const pairsOf = pkg => S24.PAIRS.map(pair => ({ ...pair, g: pkg.RESPONSES.general_government[pair.end === "least" ? "low" : "high"] }));
// One removal definition for this script and lineage_addition.cjs. meta.items identifies the actual native cells
// and the production array added by item10; reversing them leaves the joint membership-credit edits in place.
function removeObservedChildren(pkg, model, suppliedPayload) {
  const pl = suppliedPayload || pkg.correctionsPayload();
  const rec = pl.meta.items.find(item => item.id === "union_completion");
  const parts = Object.entries(rec?.parts || {}).filter(([name]) => name.startsWith("lineage_g3plus:observed_nonreporters:"));
  if (!rec || !parts.length || !rec.production_delta) throw Error("[BLOCKED] observed nonreporters lack native item parts or production delta");
  const edits = parts.map(([name, part]) => {
    const source = pl.edits[rec.edits.first + part.edit];
    if (!source?.by) throw Error(`[BLOCKED] native child part ${name} has no cell shift`);
    return { ...source, by: Object.fromEntries(["personal", "shared"].map(a => [a, -part.by[a]])) };
  });
  const stripped = Engine.applyCorrections(model, { edits, meta: model.corrections });
  const production = rec.production_delta;
  if (JSON.stringify(stripped.production.dims) !== JSON.stringify(production.dims)) throw Error("[BLOCKED] child-removal production dimensions differ");
  for (const field of ["private_wtp_bn", "induced_receipts_bn"]) {
    if (stripped.production[field].length !== production[field].length) throw Error("[BLOCKED] child-removal production grid length differs");
    stripped.production[field] = stripped.production[field].map((v, i) => v - production[field][i]);
  }
  return { model: stripped, parts, record: rec, edits };
}
module.exports = { removeObservedChildren };
let last = null;
function withCase(pkg, variant, f) {
  const gg = pkg.RESPONSES.general_government;
  const carriers = pkg.correctionsPayload().meta.union_completion?.carriers || {};
  const carrierEntries = Object.entries(carriers);
  const enterprise = [P.ENTERPRISE_RECEIPT, ...pkg.ENTERPRISE_SPLITS.map(id => `receipt:${id}`)];
  const fixedReceipts = Object.entries(pkg.LINE_RESPONSES).filter(([k]) => k.startsWith("receipt:") && !enterprise.includes(k));
  const evaluate = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response, reading = st.general_government_response === gg.low ? "low" : st.general_government_response === gg.high ? "high" : null;
    if (!reading) throw Error("[BLOCKED] sign_reversal general-government response has no case reading");
    const atS = variant === "enterprises_at_s", extra = { [P.RENTAL]: 1 };
    for (const id of enterprise) extra[id] = atS ? s : 1;
    for (const [id, response] of fixedReceipts) extra[id] = response[reading];
    for (const [id, src] of carrierEntries) if (src.kind !== "line") extra[id] = src.end === reading ? 1 : 0;
    let state = { ...st, response_override: { ...st.response_override, ...extra } };
    let ev = evaluate(m, state);
    const receiptRows = new Map(ev.receipts.map(row => [row.id, row]));
    const spendingRows = new Map(ev.spending.map(row => [row.id, row]));
    for (const [id, src] of carrierEntries) if (src.kind === "line") {
      const parent = (src.side === "receipt" ? receiptRows : spendingRows).get(src.parent_line);
      if (!parent) throw Error(`[BLOCKED] sign_reversal missing carrier parent ${src.parent_line}`);
      const key = src.side === "receipt" ? state.receipt_scenario : parent.key;
      extra[id] = key === src.parent_key ? parent.response : 0;
    }
    if (carrierEntries.length) {
      state = { ...st, response_override: { ...st.response_override, ...extra } };
      ev = evaluate(m, state);
    }
    const cap = pkg.capitalReturn(ev, { share: st.school_share, reading, rate: P.RATES[reading], enterprises: P.ENTERPRISES, long_run: null });
    const ent = cap.components.filter(c => c.group === "enterprise").reduce((a, c) => a + c.return_bn, 0);
    const capital = cap.total_bn - (atS ? (1 - s) * ent : 0);
    const spec={allocation:st.allocation,reading,share:st.school_share,school:st.service_response,gg:st.general_government_response,uc:st.uncompensated_care_response,rate:pkg.RATES[reading],enterprises:pkg.ENTERPRISES,long_run:null};
    const basePost=pkg.OCT15?pkg.OCT15.postEngine(spec):(pkg.postEngine?pkg.postEngine(spec):0);
    const adjustedCapital=atS?{...cap,total_bn:capital,components:cap.components.map(c=>c.group==="enterprise"?{...c,return_bn:c.return_bn*s}:c)}:cap;
    const added=pkg.postFor?pkg.postFor(m,spec,undefined,{evaluation:ev,capital:adjustedCapital}):{total_bn:0};
    const post=basePost+added.total_bn;
    last = { ...ev, welfare_bn: ev.welfare_bn - capital - post, engine_welfare_bn: ev.welfare_bn, capital_return_bn: capital, post_engine_bn: post };
    return last;
  };
  try { return f(); } finally { Engine.evaluate = evaluate; }
}
function frozenPersonal(model, pairs) {
  const w = { least: [], most: [] };
  for (const pair of pairs) for (const prod of S24.productions(0)) for (const share of S24.SHARES) w[pair.end].push(S24.welfare(model, "personal", 0, pair, prod, share));
  return [Math.min(...w.most), Math.max(...w.least)];
}
function readings(pkg) {
  const model = pkg.payloadModel(), pairs = pairsOf(pkg), out = new Map();
  for (const [variant, suffix] of [["enterprises_at_1", ""], ["enterprises_at_s", "__enterprises_at_s"]]) withCase(pkg, variant, () => {
    for (const allocation of ["personal", "shared"]) out.set(`service_break_even_${allocation}${suffix}`, S24.breakEven(model, allocation, pairs));
    out.set(`frozen_services_capital_fixed_welfare_bn_cbo_preferred${suffix}`, S24.frozen(model, pairs));
    out.set(`frozen_services_capital_fixed_welfare_bn_cbo_preferred_personal${suffix}`, frozenPersonal(model, pairs));
  });
  return out;
}
if (require.main === module) {
const payload = P.correctionsPayload();
if (payload.meta.coverage?.stub) console.log("[STUB] sign_reversal uses temporary coverage prices");
const zero = P.V8_PACKAGE, zeroReadings = readings(zero);
gate("one engine: imported definition and v8 use the same Engine", P.P24.Engine === Engine);
for (const row of oldRows.slice(1)) {
  const got = zeroReadings.get(row[0]);
   gate(`new items OFF reproduces v8 ${row[0]}`, !!got && got.every((v, i) => v.toFixed(4) === row[oldHeader.indexOf(`oct15_${i ? "high" : "low"}`)]));
}
const model = P.payloadModel(), gg = P.RESPONSES.general_government;
const reference = P.ALL_SPECS.map(spec => P.evaluateFull(model, spec, "proportional_reference"));
let refGap = 0, capGap = 0, postGap = 0;
withCase(P, "enterprises_at_1", () => P.ALL_SPECS.forEach((spec, i) => {
  const pair = { end: spec.reading === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
  const production = { ...Engine.defaultState(model).production, normalization: spec.normalization };
  const welfare = S24.welfare(model, spec.allocation, 1, pair, production, spec.share);
  refGap = Math.max(refGap, Math.abs(welfare + reference[i].cost_bn));
  capGap = Math.max(capGap, Math.abs(last.capital_return_bn - reference[i].capital.total_bn));
  postGap = Math.max(postGap, Math.abs(last.post_engine_bn - reference[i].post_engine.total_bn));
}));
gate("at services=1 welfare is minus v8 proportional-reference full cost on all 64 specifications", refGap < 1e-9, refGap.toExponential(2));
gate("capital is the full package's capital, and post-engine cost enters welfare negatively", capGap < 1e-12 && postGap < 1e-12, `${capGap} / ${postGap}`);
let linearGap = 0, points = 0;
const prods = S24.productions(1);
for (const variant of ["enterprises_at_1", "enterprises_at_s"]) withCase(P, variant, () => {
  for (const allocation of ["personal", "shared"]) for (const pair of pairsOf(P)) for (const production of prods.slice(0, 3).concat(prods.slice(-3))) for (const share of S24.SHARES) {
    const w = s => S24.welfare(model, allocation, s, pair, production, share);
    linearGap = Math.max(linearGap, Math.abs(w(0.37) - 0.63 * w(0) - 0.37 * w(1))); points++;
  }
});
gate("service response remains linear with mapped carriers and fixed item11/coverage", linearGap < 1e-9, `${points} points; ${linearGap.toExponential(2)}`);
const removed = removeObservedChildren(P, model, payload);
gate("observed children are native cell parts and production, without endpoint child carriers", removed.parts.length > 0 && !Object.values(payload.meta.union_completion.carriers).some(source => source.kind === "nonreporters"), `${removed.parts.length} native cell parts`);
let childGap = 0, childSlope = 0, childPoints = 0;
for (const variant of ["enterprises_at_1", "enterprises_at_s"]) withCase(P, variant, () => {
  for (const allocation of ["personal", "shared"]) for (const pair of pairsOf(P)) for (const share of S24.SHARES) {
    const production = S24.productions(1)[0], changes = [];
    for (const s of [0, 0.37]) {
      const fullWelfare = S24.welfare(model, allocation, s, pair, production, share), full = last;
      const withoutWelfare = S24.welfare(removed.model, allocation, s, pair, production, share), without = last;
      const receiptRows = new Map(full.receipts.map(row => [row.id, row]));
      const spendingRows = new Map(full.spending.map(row => [row.id, row]));
      let nativeFiscal = 0;
      for (const [, part] of removed.parts) {
        const edit = payload.edits[removed.record.edits.first + part.edit];
        const row = (edit.side === "receipt" ? receiptRows : spendingRows).get(edit.line);
        if (!row) throw Error(`[BLOCKED] sign child comparison missing native row ${edit.line}`);
        const selected = edit.side === "receipt" ? model.receipts.reference : row.key;
        if (selected === (edit.scenario || edit.key)) nativeFiscal += (edit.side === "receipt" ? 1 : -1) * row.response * part.by[allocation];
      }
      const nativeProduction = full.private_wtp_bn + full.induced_receipts_bn - without.private_wtp_bn - without.induced_receipts_bn;
      const capital = full.capital_return_bn - without.capital_return_bn;
      const actual = fullWelfare - withoutWelfare, direct = nativeFiscal + nativeProduction - capital-(full.post_engine_bn-without.post_engine_bn);
      childGap = Math.max(childGap, Math.abs(actual - direct)); changes.push(actual); childPoints++;
    }
    childSlope = Math.max(childSlope, Math.abs(changes[1] - changes[0]));
  }
});
gate("at services=0 and0.37 removing children equals native fiscal plus P/F minus public capital", childGap < 1e-9, `${childPoints} comparisons; max gap ${childGap.toExponential(2)}`);
gate("observed-child sign contribution changes with service response, rather than a fixed endpoint charge", childSlope > 1e-6, `largest change ${childSlope.toExponential(2)}bn`);
for (const [key, value] of readings(P)) values.set(key, value);
gate("all eight v7 row names have finite v8 readings", oldRows.length === 9 && oldRows.slice(1).every(row => values.get(row[0])?.every(Number.isFinite)));
const lines = [oldLines[0] + ",oct16_low,oct16_high", ...oldLines.slice(1).map(line => line + "," + values.get(line.split(",")[0]).map(v => v.toFixed(4)).join(","))];
gate("every v7 column and cell is unchanged, in order", lines.every((line, i) => line.startsWith(oldLines[i] + ",")));
if (checks.some(c => !c.pass)) throw Error("[BLOCKED] sign_reversal gate failure; no output written");
require("./memory_guard.cjs").requireWithinBudget("sign reversal");
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "sign_reversal.csv"), lines.join("\n") + "\n");
console.log(`[resources] process.resourceUsage().maxRSS=${process.resourceUsage().maxRSS} KiB`);
console.log("all gates passed");
}
