/* Read-only v7 engine snapshot: cash rows and oracle costs for the person adapter.
 * Run: node infra/immigration-fiscal/union_completion_2026_10_14/snapshot.cjs
 */
"use strict";
const fs = require("fs"), path = require("path");
const fiscal = path.dirname(__dirname);
const P = require(path.join(fiscal, "main_case_2026_10_14/package.cjs"));
const read = (p) => JSON.parse(fs.readFileSync(path.join(fiscal, p), "utf8"));
const lines = read("within_group_distribution_2026_09_29/_cache/oct14/lines.json");
const pay = read("generation_account_2026_09_24/derived/generation_corrections_oct14_cash.json").payloads.a;
const summary = read("main_case_2026_10_14/derived/summary.json");
const cash = JSON.parse(JSON.stringify(lines));
const ends = ["low", "high"];
for (let j = 0; j < 2; j++) {
  const end = ends[j], spec = P.MAIN_SPECS[summary.v7.end_specifications.cash[j]];
  if (spec.allocation !== "personal") throw Error("[BLOCKED] nonpersonal end");
  const u = P.CASH.evaluateFull(P.CASH.payloadModel(), spec, P.MAIN_PROFILE);
  cash.union[end].cost_bn = u.cost_bn;
  if (Math.abs(u.cost_bn - summary.cash_set.band_bn[j]) > 1e-9) throw Error("[BLOCKED] cash oracle");
  for (const g of ["G1", "G2", "G3plus"]) {
    const m = P.Engine.applyCorrections(read(`generation_account_2026_09_24/derived/model_${g}.json`), pay[g]);
    const ev = P.CASH.evaluateFull(m, spec, P.MAIN_PROFILE);
    const state = P.CASH.stateFor(m, spec, P.MAIN_PROFILE);
    const rows = [ ...ev.evaluation.receipts.map(r => ({...r, side: "receipt"})),
      ...ev.evaluation.spending.map(r => ({...r, side: "spending"})) ];
    cash.generations[g][end].rows = rows.map(r => ({...r, scenario: state.receipt_scenario,
      cost_bn: -state.fiscal_weight * r.effect_bn}));
    cash.generations[g][end].cost_bn = ev.cost_bn;
    // The exporter gates capital and production identical between sets; verify again.
    const cap = ev.capital.components.reduce((s, c) => s + c.return_bn, 0);
    const stored = cash.generations[g][end].capital.reduce((s, c) => s + c.cost_bn, 0);
    if (Math.abs(cap - stored) > 1e-12) throw Error("[BLOCKED] cash capital differs");
    const prod = -(ev.evaluation.private_wtp_bn + state.fiscal_weight * ev.evaluation.induced_receipts_bn);
    if (Math.abs(prod - cash.generations[g][end].production.cost_bn) > 1e-12) throw Error("[BLOCKED] cash production differs");
  }
  const sum = ["G1", "G2", "G3plus"].reduce((s, g) => s + cash.generations[g][end].cost_bn, 0);
  if (Math.abs(sum - u.cost_bn) > 1e-9) throw Error("[BLOCKED] cash generations do not close");
}
fs.mkdirSync(path.join(__dirname, "_cache/set/oct14"), {recursive: true});
fs.mkdirSync(path.join(__dirname, "_cache/cash/oct14"), {recursive: true});
fs.writeFileSync(path.join(__dirname, "_cache/set/oct14/lines.json"), JSON.stringify(lines, null, 1) + "\n");
fs.writeFileSync(path.join(__dirname, "_cache/cash/oct14/lines.json"), JSON.stringify(cash, null, 1) + "\n");
console.log("PASS: frozen v7 set/cash snapshots, personal 16 / 11");
