/* Read-only transfer-conservation test and alternative highway constructions. */
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const crypto = require("crypto");
const fiscal = path.resolve(__dirname, "..");
const packageFile = path.join(fiscal, "main_case_long_run_2026_09_27/package.cjs");
const P = require(packageFile);
const rows = [];
for (const method of P.METHODS) {
  const options = P.withCentral({capital: false});
  const model = P.modelFor("central", method, options);
  const spec = P.specsFor(options)[48];
  const before = P.evaluateFull(model, spec, P.MAIN_PROFILE);
  const a = spec.allocation;
  const housing = before.evaluation.spending.find(l => l.id === "housing_subsidies");
  const enterprise = before.evaluation.receipts.find(l => l.id === "enterprise_surplus");
  const kh = housing.amount_bn / housing.national_bn;
  const ke = enterprise.amount_bn / enterprise.national_bn;
  const clone = JSON.parse(JSON.stringify(model));
  const h = clone.spending.lines.find(l => l.id === "housing_subsidies");
  const e = clone.receipts.lines.find(l => l.id === "enterprise_surplus");
  h.national_bn += 1;
  h.keys[h.preferred_key][a].target_bn += kh;
  h.keys[h.preferred_key][a].other_bn += 1 - kh;
  e.national_bn += 1;
  e.cells[clone.receipts.reference][a].target_bn += ke;
  e.cells[clone.receipts.reference][a].other_bn += 1 - ke;
  const change = P.evaluateFull(clone, spec, P.MAIN_PROFILE).cost_bn - before.cost_bn;
  assert(Math.abs(change - (kh - ke)) < 1e-9, "Unexpected transfer mechanism");
  rows.push({method, spec: 48, capital: false, housing_key: kh, enterprise_key: ke,
    added_internal_transfer_national_bn: 1, cost_change_bn: change,
    invariant: Math.abs(change) < 1e-9});
}
const inputs = [packageFile, "service_response_long_run_2026_09_27/derived/responses.json",
  "service_response_long_run_2026_09_27/derived/candidate_band.json"].map(p => path.resolve(fiscal, p));
const r = JSON.parse(fs.readFileSync(inputs[1]));
const c = JSON.parse(fs.readFileSync(inputs[2]));
const s = r.meta.s;
const k = c.group_amounts_at_end_specifications_bn.low.economic_affairs_services / r.lines.economic_affairs_services.national_bn;
const b = r.elasticities.highways_nontoll.across_states.b;
const C = r.lines.economic_affairs_services.subfunctions.find(x => x.id === "sl_highways").national_bn;
console.log(JSON.stringify({rows, highway: {national_bn: C, population_share: s, resource_share: k,
  elasticity: b, implemented_bn: C*k*(1-(1-s)**b)/s,
  population_power_law_bn: C*(1-(1-s)**b), resource_power_law_bn: C*(1-(1-k)**b)},
  source_sha256: Object.fromEntries(inputs.map(p => [path.relative(fiscal, p),
    crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex")]))}, null, 2));
