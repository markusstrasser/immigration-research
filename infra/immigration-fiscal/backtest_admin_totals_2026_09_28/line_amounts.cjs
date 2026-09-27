/* The September 27 case's group dollars on the lines this back-test's keys drive, at specifications 48 (low end,
 * shared allocation) and 11 (high end, personal), averaged over the two fill-in methods as the package's `central`
 * does. Read-only: requires main_case_long_run_2026_09_27/package.cjs unchanged. Writes derived/line_amounts.json.
 * Run from the repository root:
 *   node infra/immigration-fiscal/backtest_admin_totals_2026_09_28/line_amounts.cjs
 */
"use strict";
const path = require("path");
const fs = require("fs");
const P = require(path.join(__dirname, "..", "main_case_long_run_2026_09_27", "package.cjs"));
const LINES = ["refundable_tax_credits", "ssi", "social_security", "railroad_retirement",
  "medicaid_and_chip_other_medical"];
const ENDS = { low: 48, high: 11 };
const oo = P.withCentral({});
const specs = P.specsFor(oo);
const out = { package: "main_case_long_run_2026_09_27/package.cjs", methods: P.METHODS, ends: ENDS, lines: {} };
for (const id of LINES) out.lines[id] = { amount_bn: {}, national_bn: {}, keys: {} };
const models = P.METHODS.map((meth) => P.modelFor("central", meth, oo));
for (const [end, i] of Object.entries(ENDS)) {
  const evals = models.map((m) => P.evaluateFull(m, specs[i]));
  out[`cost_${end}_bn`] = evals.reduce((a, r) => a + r.cost_bn, 0) / evals.length;
  for (const id of LINES) {
    const rows = evals.map((r) => r.evaluation.spending.find((l) => l.id === id));
    out.lines[id].amount_bn[end] = rows.reduce((a, l) => a + l.amount_bn, 0) / rows.length;
    out.lines[id].national_bn[end] = rows.reduce((a, l) => a + l.national_bn, 0) / rows.length;
  }
}
for (const id of LINES) {
  const ls = models.map((m) => m.spending.lines.find((l) => l.id === id));
  for (const key of Object.keys(ls[0].keys)) {
    out.lines[id].keys[key] = {};
    for (const a of P.ALLOCS) {
      out.lines[id].keys[key][a] = {
        target_bn: ls.reduce((s, l) => s + l.keys[key][a].target_bn, 0) / ls.length,
        other_bn: ls.reduce((s, l) => s + l.keys[key][a].other_bn, 0) / ls.length,
      };
    }
  }
}
fs.writeFileSync(path.join(__dirname, "derived", "line_amounts.json"), JSON.stringify(out, null, 1) + "\n");
console.log(JSON.stringify(out, null, 1));
