/* Gate engine.js against rows selected from the executed exports (derived/test_vectors.json).
 * Run: node test_engine.js   (after build_model.py). Exit code 1 on any mismatch. */
"use strict";
const fs = require("fs");
const path = require("path");
const Engine = require("./engine.js");

const derived = path.join(__dirname, "derived");
const model = JSON.parse(fs.readFileSync(path.join(derived, "model.json"), "utf8"));
const vectors = JSON.parse(fs.readFileSync(path.join(derived, "test_vectors.json"), "utf8"));
const TOLERANCE = 1e-6;  // billions; the exports are rounded at 1e-9
let failures = 0, worst = 0;

function check(label, got, want) {
  const gap = Math.abs(got - want);
  worst = Math.max(worst, gap);
  if (!(gap <= TOLERANCE)) {
    failures += 1;
    if (failures <= 10) console.error(`MISMATCH ${label}: engine ${got} executed ${want}`);
  }
}

const scenarioKeys = Object.fromEntries(Object.entries(model.spending.scenarios).map(([k, v]) => [v, k]));

for (const row of vectors.grid) {
  const state = Engine.defaultState(model);
  Engine.PRODUCTION_DIMS.forEach((d) => { state.production[d] = row[d]; });
  state.receipt_scenario = row.receipt_scenario;
  state.spending_keys = scenarioKeys[row.spending_scenario];
  state.allocation = row.allocation;
  state.public_goods_response = row.public_goods_response;
  state.service_response = row.service_response;
  state.fiscal_weight = row.fiscal_weight;
  const out = Engine.evaluate(model, state);
  check("grid welfare", out.welfare_bn, row.welfare_bn);
  check("grid direct response", out.direct_fiscal_response_bn, row.direct_fiscal_response_bn);
}

for (const c of vectors.service) {
  const state = Engine.defaultState(model);
  state.allocation = c.allocation;
  state.production.normalization = c.normalization;
  state.school_share = c.school_share;
  state.school_response = c.school_response;
  state.other_education_response = c.other_education_response;
  state.delayed_response = c.delayed_response;
  const out = Engine.evaluate(model, state);
  check(`service ${c.profile}/${c.case_id}`, out.welfare_bn, c.welfare_bn);
  check(`service effective response ${c.profile}/${c.case_id}`, out.effective_service_response, c.effective_service_response);
}

for (const a of vectors.accounts) {
  const state = Engine.defaultState(model);
  state.receipt_scenario = a.receipt_scenario;
  state.spending_keys = scenarioKeys[a.spending_scenario];
  state.allocation = a.allocation;
  const out = Engine.evaluate(model, state);
  check("accounting balance", out.target_balance_bn, a.target_balance_bn);
  check("normalized gap", out.normalized_gap_bn, a.normalized_gap_bn);
}

// The published headline spans must fall out of the evaluator's own unresolved-range sweep.
const headline = model.meta.headline.category_service_response_sensitivity;
function span(settings) {
  const state = Object.assign(Engine.defaultState(model), settings);
  return Engine.unresolvedRange(model, state, "welfare_bn");
}
const cbo = span({ other_education_response: 1, delayed_response: 0, school_response_band: [0.63, 0.66] });
check("headline low", cbo[0], headline.cbo_category_lag_non_school_full.min_welfare_bn);
check("headline high", cbo[1], headline.cbo_category_lag_non_school_full.max_welfare_bn);
const proportional = span({});
check("proportional low", proportional[0], headline.proportional_reference.min_welfare_bn);
check("proportional high", proportional[1], headline.proportional_reference.max_welfare_bn);

// Attribution must be exhaustive: Shapley effects sum to the total difference.
const from = Engine.defaultState(model);
const to = Object.assign(Engine.defaultState(model), { service_response: 0.5, public_goods_response: 1, count_production: false });
to.production.sigma = 1.5;
const paths = ["service_response", "public_goods_response", "count_production", "production.sigma"];
const parts = Engine.attribute(model, from, to, paths, "welfare_bn");
check("attribution closure", parts.reduce((s, p) => s + p.effect_bn, 0),
  Engine.evaluate(model, to).welfare_bn - Engine.evaluate(model, from).welfare_bn);

const counts = `${vectors.grid.length} grid rows, ${vectors.service.length} service cases, ${vectors.accounts.length} accounting cases`;
if (failures) { console.error(`FAIL: ${failures} mismatches over ${counts}; worst gap ${worst}`); process.exit(1); }
console.log(`PASS: ${counts}, 4 headline bounds, attribution closure; worst gap ${worst.toExponential(2)} bn`);
