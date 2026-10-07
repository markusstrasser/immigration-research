/* The user-fee lane on main case v5: the fee terms the brief asks for and the key terms found beside them, priced at
 * the case's 64 specifications and its ends (48 low, 11 high in both methods), for the case (corrections.json) and its
 * cash set (corrections_cash.json).
 *
 * Engine edit. fee_lines.json's engine_lines become synthetic spending lines (national 0, key k), one edit each by
 * allocation, at response 1 at both readings (meta.responses); consumer.cjs (engine.js, model.json and the payload, no
 * package) evaluates them. Every parent line responds at 1 at every specification (gated), so the edit is first order
 * exactly. Post-engine, as the case's capital return is: the K-12 weight term (A + B s, s the specification's school
 * fraction, at the education line's response) and the capital keys by part (stock x rate x response x key change, with
 * the response and rate the consumer's own at each specification).
 *
 * Gates (each fails loudly):
 *   - consumer.cjs gives summary.json's band and cash band at the ends 48 / 11 (1e-9), and they are the specifications'
 *     lowest and highest costs;
 *   - the union reads fee_lines.py made from model.json and the payload's pre-lineage edits equal the engine's
 *     (applyCorrections on those edits), in both payloads (1e-9);
 *   - the parent lines respond at 1 at every specification of both sets: education_services, health_services,
 *     other_federal_benefits, receipt:enterprise_surplus, and the college, k12 and ent_transit_sl capital components;
 *   - each component's return is stock x rate x key x response, and its key splits into the union's part
 *     (fee_lines.json) and the lineage's edits (1e-12);
 *   - the lines at zero reproduce every specification's cost exactly; with their amounts, each set's change at every
 *     specification is the sum of the amounts at its allocation (1e-9), line by line and all together.
 * Writes derived/case_oct05.csv (per specification) and derived/case_oct05.json (terms, bands and arms at the ends).
 * Run from the repository root: node infra/immigration-fiscal/user_fee_allocation_2026_10_07/case.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.resolve(HERE, "..");
const C = require(path.join(FISCAL, "main_case_candidate_v4_2026_09_29", "consumer.cjs"));
const readJson = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const CASE = path.join(FISCAL, "main_case_2026_10_05", "derived");
const FL = readJson(path.join(HERE, "derived", "fee_lines.json"));
const SUMMARY = readJson(path.join(CASE, "summary.json"));
const SETS = { case: readJson(path.join(CASE, "corrections.json")), cash: readJson(path.join(CASE, "corrections_cash.json")) };
const BANDS = { case: SUMMARY.main_case, cash: SUMMARY.cash_set.band_bn };
const ENDS = { low: 48, high: 11 };
const ALLOCS = ["personal", "shared"];
const LINES = Object.keys(FL.engine_lines);
const FEE_LINES = ["fee_tuition", "fee_health"];
const Eng = C.loadEngine(), model = C.loadModel();
const N_EDU = model.spending.lines.find((l) => l.id === "education_services").national_bn;

const gates = [];
function gate(name, ok, detail) {
  if (!ok) throw new Error(`[BLOCKED] ${name}${detail ? ": " + detail : ""}`);
  gates.push(name);
}
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const sum = (xs) => xs.reduce((a, b) => a + b, 0);

function withLines(payload, ids, scale) {
  const p = JSON.parse(JSON.stringify(payload));
  for (const id of ids) {
    const d = FL.engine_lines[id];
    p.lines.push({ id, family: d.response_class === "household_transfer" ? "social_benefits" : "consumption",
      response_class: d.response_class, label: d.label });
    p.edits.push({ side: "spending", line: id, key: "k", by: { personal: scale * d.by.personal, shared: scale * d.by.shared } });
    p.meta.responses[id] = { low: 1, high: 1, rule: "the user-fee lane's line: its parent responds at 1 at every specification" };
  }
  return p;
}
const run = (payload) => C.evaluateAll(payload, { engine: Eng, model });
const spendingRow = (r, id) => r.evaluation.spending.find((l) => l.id === id);
const receiptRow = (r, id) => r.evaluation.receipts.find((l) => l.id === id);
const component = (r, id) => r.capital.components.find((c) => c.id === id);

// The lineage's edits on a spending line and key, by allocation.
function lineageEdits(payload, line, key) {
  const first = payload.meta.lineage.edits.first, out = { personal: 0, shared: 0 };
  for (const e of payload.edits.slice(first)) {
    if (e.side === "spending" && e.line === line && e.key === key) for (const a of ALLOCS) out[a] += e.by[a];
    if (e.side === "spending" && e.line === line && e.national_bn !== undefined) throw new Error(`[BLOCKED] a lineage scale edit on ${line}`);
  }
  return out;
}

const results = {}, perSpec = [];
for (const [name, payload] of Object.entries(SETS)) {
  const base = run(payload);
  const costs = base.map((r) => r.cost_bn);
  gate(`${name}: consumer.cjs gives summary.json's band at the ends 48 / 11 (1e-9)`,
    near(costs[ENDS.low], BANDS[name][0], 1e-9) && near(costs[ENDS.high], BANDS[name][1], 1e-9), `${costs[ENDS.low]} ${costs[ENDS.high]}`);
  gate(`${name}: the ends are the specifications' lowest and highest costs`,
    costs.every((c) => c >= costs[ENDS.low] - 1e-12 && c <= costs[ENDS.high] + 1e-12));

  // The union reads.
  const first = payload.meta.lineage.edits.first;
  const mu = Eng.applyCorrections(model, Object.assign({}, payload, { edits: payload.edits.slice(0, first) }));
  const reads = [];
  for (const [k, want] of Object.entries(FL.union_reads)) {
    const [side, rest] = k.split(":");
    for (const a of ALLOCS) {
      let got;
      if (side === "spending") {
        const [line, key] = rest.split("/");
        got = mu.spending.lines.find((l) => l.id === line).keys[key][a].target_bn;
      } else got = mu.receipts.lines.find((l) => l.id === rest).cells[model.receipts.reference][a].target_bn;
      reads.push([k, a, got, want[a]]);
    }
  }
  const bad = reads.filter(([, , got, want]) => !near(got, want, 1e-9));
  gate(`${name}: fee_lines.py's union reads equal the engine's on the pre-lineage edits (1e-9)`, !bad.length, JSON.stringify(bad));

  // Parent responses and the capital components' rule and keys.
  const K = payload.meta.capital_return, stock = (id) => K.components.find((c) => c.id === id).stock_charged_bn;
  const lin = {
    edu: lineageEdits(payload, "education_services", "education_mix"),
    college: lineageEdits(payload, "college_rekey", "k"), school: lineageEdits(payload, "school_reprice", "k"),
  };
  let respOk = true, ruleOk = true, splitOk = true;
  for (const r of base) {
    const a = r.spec.allocation;
    for (const id of ["education_services", "health_services", "other_federal_benefits"]) respOk = respOk && near(spendingRow(r, id).response, 1, 1e-12);
    respOk = respOk && near(receiptRow(r, "enterprise_surplus").response, 1, 1e-12);
    for (const id of ["college", "k12", "ent_transit_sl"]) {
      const c = component(r, id);
      respOk = respOk && near(c.response, 1, 1e-12);
      ruleOk = ruleOk && near(c.return_bn, stock(id) * K.rates[r.spec.reading] * c.key * c.response, 1e-12);
    }
    const ent = receiptRow(r, "enterprise_surplus");
    splitOk = splitOk
      && near(component(r, "college").key, FL.post_engine.college_capital.key_union[a] + (lin.edu[a] + lin.college[a]) / N_EDU, 1e-12)
      && near(component(r, "k12").key, FL.post_engine.k12_capital.key_union[a] + (lin.edu[a] + lin.school[a]) / N_EDU, 1e-12)
      && near(FL.union_reads["receipt:enterprise_surplus"][a] / ent.national_bn, FL.transit.s_ent_union[a], 1e-12)
      && near(component(r, "ent_transit_sl").key, ent.amount_bn / ent.national_bn, 1e-12);
  }
  gate(`${name}: education, health, other federal benefits, the enterprise receipt and the college, K-12 and transit capital respond at 1 at every specification`, respOk);
  gate(`${name}: each capital component's return is stock x rate x key x response`, ruleOk);
  gate(`${name}: the college and K-12 capital keys are the union's part plus the lineage's edits over the line's national, and the transit key is the receipt's, its union part the case's rekeyed share (1e-12)`, splitOk);

  // The engine edit: zero lines change nothing; each line, the fee lines and all lines add their amounts.
  const zero = run(withLines(payload, LINES, 0));
  gate(`${name}: the lines at zero reproduce every specification's cost exactly`, zero.every((r, i) => r.cost_bn === costs[i]));
  const variants = Object.fromEntries([...LINES.map((id) => [id, [id]]), ["fee", FEE_LINES], ["all", LINES]]);
  const delta = {};
  for (const [v, ids] of Object.entries(variants)) {
    const ev = run(withLines(payload, ids, 1));
    delta[v] = ev.map((r, i) => r.cost_bn - costs[i]);
    const want = ev.map((r) => sum(ids.map((id) => FL.engine_lines[id].by[r.spec.allocation])));
    gate(`${name}: engine edit ${v}: the change at every specification is the sum of its lines' amounts at the allocation (1e-9)`,
      delta[v].every((d, i) => near(d, want[i], 1e-9)), JSON.stringify(delta[v].slice(0, 3)));
  }

  // Post-engine terms.
  const post = base.map((r) => {
    const a = r.spec.allocation, s = r.spec.share, edu = spendingRow(r, "education_services").response;
    const cap = (id, d) => stock(id) * K.rates[r.spec.reading] * component(r, id).response * d;
    const weight = (wn) => { const x = FL.post_engine.key_k12_weight.by_weights[wn][a]; return (x.A + x.B * s) * edu; };
    return Object.assign({ k12_weight_bn: weight(FL.post_engine.key_k12_weight.central) },
      Object.fromEntries(Object.keys(FL.post_engine.key_k12_weight.by_weights).map((wn) => [`k12_weight_${wn}_bn`, weight(wn)])), {
      capital_college_bn: cap("college", FL.post_engine.college_capital.key_target[a] - FL.post_engine.college_capital.key_union[a]),
      capital_k12_bn: cap("k12", FL.post_engine.k12_capital.key_target[a] - FL.post_engine.k12_capital.key_union[a]),
      capital_transit_bn: cap("ent_transit_sl", FL.post_engine.transit_capital.key_shift[a]),
    });
  });

  base.forEach((r, i) => {
    const p = post[i];
    const total = delta.all[i] + p.k12_weight_bn + p.capital_college_bn + p.capital_k12_bn + p.capital_transit_bn;
    perSpec.push(Object.assign({ set: name, spec: i, allocation: r.spec.allocation, normalization: r.spec.normalization,
      share: r.spec.share, school: r.spec.school, reading: r.spec.reading, uc: r.spec.uc, base_cost_bn: costs[i] },
      Object.fromEntries(LINES.map((id) => [`${id}_bn`, delta[id][i]])),
      { engine_fee_bn: delta.fee[i], engine_all_bn: delta.all[i] }, p, { total_change_bn: total, cost_bn: costs[i] + total }));
  });

  // Terms and blocks at the ends.
  const at = {};
  for (const [end, i] of Object.entries(ENDS)) {
    const p = post[i], d = (id) => delta[id][i];
    const blocks = {
      fee_terms: d("fee"),
      education: d("fee_tuition") + d("key_higher_ed") + p.k12_weight_bn + p.capital_college_bn + p.capital_k12_bn,
      health: d("fee_health") + d("key_health"),
      pell: d("key_pell"),
      transit: d("key_transit") + p.capital_transit_bn,
    };
    blocks.total = blocks.education + blocks.health + blocks.pell + blocks.transit;
    blocks.education_and_pell = blocks.education + blocks.pell;
    at[end] = { spec: i, allocation: base[i].spec.allocation, base_cost_bn: costs[i],
      lines_bn: Object.fromEntries(LINES.map((id) => [id, d(id)])), post_engine_bn: p, blocks_bn: blocks,
      cost_with_fee_terms_bn: costs[i] + blocks.fee_terms, cost_with_all_bn: costs[i] + blocks.total };
  }
  const newCosts = perSpec.filter((r) => r.set === name).map((r) => r.cost_bn);
  results[name] = { band_bn: BANDS[name], ends: at,
    band_with_fee_terms_bn: [at.low.cost_with_fee_terms_bn, at.high.cost_with_fee_terms_bn],
    band_with_all_bn: [at.low.cost_with_all_bn, at.high.cost_with_all_bn],
    ends_hold_with_all: newCosts.every((c) => c >= newCosts[ENDS.low] - 1e-12 && c <= newCosts[ENDS.high] + 1e-12) };
}

// Arms at the ends (first order, which the gates make exact: every term enters at response 1, the capital terms at the
// ends' rates).
const H = FL.higher_ed, HL = FL.health, rate = { low: 0.02, high: 0.03 };
const arms = {
  tuition_fee_term_at_the_account_key_bn: H.fee_term_at_account_key_bn,
  health_fee_term_at_the_account_key_bn: HL.fee_term_at_account_key_bn.personal,
  tuition_ranges_bn: H.ranges_bn,
  health_ranges_bn: HL.ranges_bn,
  health_raw_meps_frame_residual_bn: HL.meps_frame_raw.personal,
  health_nipa_charges_g_residual_bn: HL.nipa_charges_g.personal,
  pell_range_bn: FL.pell.range_bn,
  transit_mode_arms_operating_bn: FL.transit.mode_arms,
  other_sales_per_001_gap_bn: FL.other_sales.per_001_gap_bn,
  lineage_per_member_scale: FL.frames.lineage_scale,
  k12_weight_at_ends_bn: Object.fromEntries(Object.entries(ENDS).map(([end, i]) => [end, Object.fromEntries(
    Object.keys(FL.post_engine.key_k12_weight.by_weights).map((wn) => [wn, results.case.ends[end].post_engine_bn[`k12_weight_${wn}_bn`]]))])),
  k12_weight_central: FL.post_engine.key_k12_weight.central,
  higher_education_dollars_by_weights_bn: Object.fromEntries(Object.entries(FL.nipa.weights).map(([wn, w]) => [wn, w.higher * N_EDU])),
  rates: rate,
};
const out = { lane: "user_fee_allocation_2026_10_07", case: "main_case_2026_10_05 (v5)", gates, sets: results, arms,
  method: "engine edit (synthetic lines at response 1 through main_case_candidate_v4_2026_09_29/consumer.cjs) plus post-engine capital and K-12 weight terms; first order is exact here (gated)" };
fs.writeFileSync(path.join(HERE, "derived", "case_oct05.json"), JSON.stringify(out, null, 1) + "\n");
const cols = Object.keys(perSpec[0]);
fs.writeFileSync(path.join(HERE, "derived", "case_oct05.csv"),
  [cols.join(","), ...perSpec.map((r) => cols.map((c) => typeof r[c] === "number" ? Number(r[c].toPrecision(12)) : r[c]).join(","))].join("\n") + "\n");
for (const [name, r] of Object.entries(results)) {
  console.log(`${name}: band ${r.band_bn.map((x) => x.toFixed(2)).join("-")}; fee terms ${r.band_with_fee_terms_bn.map((x) => x.toFixed(2)).join("-")}; all ${r.band_with_all_bn.map((x) => x.toFixed(2)).join("-")}; ends hold ${r.ends_hold_with_all}`);
  for (const end of ["low", "high"]) console.log(`  ${end}:`, JSON.stringify(Object.fromEntries(Object.entries(r.ends[end].blocks_bn).map(([k, v]) => [k, +v.toFixed(3)]))));
}
console.log(`${gates.length} gates passed`);
