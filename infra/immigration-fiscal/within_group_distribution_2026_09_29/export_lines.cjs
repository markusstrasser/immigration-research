/* Step 1: the adopted September 27 case, line by line, for each generation at the case's two band ends.
 *
 * Reads read-only: the case's package (main_case_long_run_2026_09_27/package.cjs), the generation account's
 * uncorrected models (generation_account_2026_09_24/derived/model_{G1,G2,G3plus}.json, convention (a): everyone
 * in their own generation) and its corrections payloads (derived/generation_corrections.json, which already end
 * with each generation's enterprise re-key edits). Each generation's corrected model is evaluated with the
 * package's evaluateFull() at the union's low and high ends (specifications found as run_generations.cjs finds
 * them: the minimum and maximum of the corrected union's cost over MAIN_SPECS).
 *
 * For every generation and end it writes each receipt and spending line (key, allocation, amount, response and
 * its cost to other residents), the production term (P, F and the specification's production dimensions) and
 * the 24 capital-return components with their key rules. households.py distributes these within each
 * generation over persons.
 * Gates (exit 1): the corrected union reproduces $321.8194 / $387.3701bn; each generation's rows sum to its
 * evaluateFull() cost and to generation_results.csv (1e-6 bn); the three generations sum to the union (1e-9 bn).
 * Writes _cache/lines.json. Run from the repository root:
 *   node infra/immigration-fiscal/within_group_distribution_2026_09_29/export_lines.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");
const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const P = require(path.join(FISCAL, "main_case_long_run_2026_09_27", "package.cjs"));
const { Engine, MODEL, MAIN_SPECS } = P;
const GEN = path.join(FISCAL, "generation_account_2026_09_24", "derived");
const GENS = ["G1", "G2", "G3plus"];
const read = (f) => JSON.parse(fs.readFileSync(f, "utf8"));
const CAP = read(path.join(FISCAL, "capital_return_services_2026_09_27/derived/engine_components.json"));
const capRule = Object.fromEntries(CAP.components.map((c) => [c.id, c.key]));
let fails = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) fails += 1;
}

const corrections = read(path.join(FISCAL, "main_case_long_run_2026_09_27/derived/corrections.json"));
const unionModel = Engine.applyCorrections(MODEL, corrections);
const uCost = MAIN_SPECS.map((s) => P.evaluateFull(unionModel, s).cost_bn);
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
gate("the corrected union reproduces the adopted case", Math.abs(uCost[lo] - 321.8194) < 1e-4 && Math.abs(uCost[hi] - 387.3701) < 1e-4,
  `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)} at specifications ${lo} / ${hi} (0-based)`);

const pay = read(path.join(GEN, "generation_corrections.json")).payloads.a;
const results = fs.readFileSync(path.join(GEN, "generation_results.csv"), "utf8").trim().split("\n");
const head = results[0].split(",");
const published = {};
for (const row of results.slice(1)) {
  const r = Object.fromEntries(row.split(",").map((v, i) => [head[i], v]));
  if (r.convention === "a") published[`${r.generation}|${r.band_end}`] = Number(r.cost_bn);
}

function dump(m, spec) {
  const full = P.evaluateFull(m, spec);
  const state = P.stateFor(P.withSyntheticLines ? P.withSyntheticLines(m) : m, spec);
  const ev = full.evaluation, fw = state.fiscal_weight;
  const rows = [];
  for (const r of ev.receipts) {
    rows.push({ side: "receipt", id: r.id, key: r.key, scenario: state.receipt_scenario, group: r.group,
      response_class: r.response_class, amount_bn: r.amount_bn, response: r.response, cost_bn: -fw * r.effect_bn });
  }
  for (const r of ev.spending) {
    rows.push({ side: "spending", id: r.id, key: r.key, group: r.group, response_class: r.response_class,
      amount_bn: r.amount_bn, response: r.response, cost_bn: -fw * r.effect_bn });
  }
  const capital = full.capital.components.map((c) => ({ id: c.id, part: c.group, level: c.level, rule: capRule[c.id],
    key: c.key, response: c.response, cost_bn: c.return_bn }));
  const production = { dims: state.production, count: state.count_production, fiscal_weight: fw,
    private_wtp_bn: ev.private_wtp_bn, induced_receipts_bn: ev.induced_receipts_bn,
    cost_bn: -(ev.private_wtp_bn + fw * ev.induced_receipts_bn) };
  const sum = rows.reduce((a, r) => a + r.cost_bn, 0) + capital.reduce((a, c) => a + c.cost_bn, 0) + production.cost_bn;
  return { cost_bn: full.cost_bn, sum_bn: sum, allocation: state.allocation, receipt_scenario: state.receipt_scenario,
    rows, capital, production };
}

const out = { meta: { case: "main_case_long_run_2026_09_27", convention: "a", spec_index: { low: lo, high: hi },
  specs: { low: MAIN_SPECS[lo], high: MAIN_SPECS[hi] } }, union: {}, generations: {} };
for (const [end, i] of [["low", lo], ["high", hi]]) {
  out.union[end] = dump(unionModel, MAIN_SPECS[i]);
  gate(`union ${end}: rows sum to the cost`, Math.abs(out.union[end].sum_bn - out.union[end].cost_bn) < 1e-9,
    `${out.union[end].sum_bn.toFixed(6)} vs ${out.union[end].cost_bn.toFixed(6)}`);
}
for (const g of GENS) {
  const m0 = read(path.join(GEN, `model_${g}.json`));
  const m1 = Engine.applyCorrections(m0, pay[g]);
  out.generations[g] = {};
  for (const [end, i] of [["low", lo], ["high", hi]]) {
    const d = dump(m1, MAIN_SPECS[i]);
    out.generations[g][end] = d;
    gate(`${g} ${end}: rows sum to evaluateFull() and to generation_results.csv`,
      Math.abs(d.sum_bn - d.cost_bn) < 1e-9 && Math.abs(d.cost_bn - published[`${g}|${end}`]) < 1e-6,
      `${d.cost_bn.toFixed(6)} vs ${published[`${g}|${end}`]}`);
  }
}
for (const end of ["low", "high"]) {
  const s = GENS.reduce((a, g) => a + out.generations[g][end].cost_bn, 0);
  gate(`${end}: the three generations add to the union`, Math.abs(s - out.union[end].cost_bn) < 1e-9, `${s.toFixed(6)}`);
}
fs.mkdirSync(path.join(HERE, "_cache"), { recursive: true });
fs.writeFileSync(path.join(HERE, "_cache", "lines.json"), JSON.stringify(out, null, 1) + "\n");
if (fails) { console.log(`✗ ${fails} gate(s) failed`); process.exit(1); }
console.log("  ✓ all export gates passed");
