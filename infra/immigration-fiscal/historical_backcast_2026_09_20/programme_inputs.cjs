/* Native-First: evaluate the live package; case_components defines the union split. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("../main_case_2026_10_14/package.cjs");
const out = path.join(__dirname, "derived/p7");
const full = P.payloadModel();
const summary = JSON.parse(fs.readFileSync(path.join(__dirname, "../main_case_2026_10_14/derived/summary.json")));
const data = {};
for (const [end, i] of [["low", 16], ["high", 11]]) {
  const spec = P.MAIN_SPECS[i];
  if (spec.allocation !== "personal") throw Error("[BLOCKED] programme allocation");
  data[end] = {};
  for (const [population, model] of [["lineage", full]]) {
    const r = P.evaluateFull(model, spec);
    const accounted = -r.evaluation.spending.reduce((a, x) => a + x.effect_bn, 0)
      - r.evaluation.receipts.reduce((a, x) => a + x.effect_bn, 0)
      - r.evaluation.private_wtp_bn - r.evaluation.induced_receipts_bn + r.capital.total_bn;
    if (Math.abs(accounted - r.cost_bn) > 1e-9) throw Error("[BLOCKED] engine lines do not close");
    if (population === "lineage" && Math.abs(r.cost_bn - summary.v7.band_bn[end === "low" ? 0 : 1]) > 1e-6)
      throw Error("[BLOCKED] programme input differs from live case");
    data[end][population] = { specification: i, spec, cost_bn: r.cost_bn,
      spending: r.evaluation.spending, receipts: r.evaluation.receipts,
      medicaid_coverage_fraction: model.spending.lines.find(x => x.id === "medicaid_and_chip_other_medical")
        .keys.medicaid.personal.target_bn / r.evaluation.spending.find(x => x.id === "medicaid_and_chip_other_medical").amount_bn,
      production_private_bn: r.evaluation.private_wtp_bn,
      production_receipts_bn: r.evaluation.induced_receipts_bn, capital: r.capital };
  }
}
fs.mkdirSync(out, {recursive: true});
fs.writeFileSync(path.join(out, "programme_inputs.json"), JSON.stringify(data, null, 2) + "\n");
console.log("PASS full/union engine line closure and v7 anchors");
