// Probe: the Sept 27 case with the group's owner-occupied property tax responding like the long-run capital
// the case already charges (0.79 = highway construction's cross-state scaling, 1 = the housing stock follows
// households). Read-only: loads the adopted package, changes one receipt response, compares at specs 48 / 11.
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const K = require(path.join(ROOT, "main_case_long_run_2026_09_27/package.cjs"));
const { Engine, METHODS, MAIN_SPECS, MAIN_PROFILE, stateFor, capitalReturn, evaluateFull, modelFor, withCentral } = K;

const models = METHODS.map((m) => modelFor("central", m, withCentral({})));
function costWith(model, spec, overrides) {
  const state = stateFor(model, spec, MAIN_PROFILE);
  state.response_override = Object.assign({}, state.response_override, overrides);
  const evaluation = Engine.evaluate(model, state);
  return -evaluation.welfare_bn + capitalReturn(evaluation, spec).total_bn;
}
const rows = [];
const mean = (a) => a.reduce((x, y) => x + y, 0) / a.length;
for (const i of [48, 11]) {
  const spec = MAIN_SPECS[i];
  const base = mean(models.map((m) => evaluateFull(m, spec, MAIN_PROFILE).cost_bn));
  const replica = mean(models.map((m) => costWith(m, spec, {})));
  if (Math.abs(base - replica) > 1e-9) throw new Error(`[BLOCKED] replica ${replica} != package ${base} at spec ${i}`);
  const row = { spec: i, adopted_bn: base.toFixed(4) };
  for (const r of [0.79, 1]) {
    row[`owner_property_at_${r}`] = mean(models.map((m) => costWith(m, spec, { "receipt:modeled_owner_property": r }))).toFixed(4);
    row[`owner_and_business_property_at_${r}`] = mean(models.map((m) => costWith(m, spec, {
      "receipt:modeled_owner_property": r, "receipt:remaining_production_property": r,
      "receipt:personal_property_tax": r }))).toFixed(4);
  }
  rows.push(row);
  console.log(JSON.stringify(row));
}
require("fs").writeFileSync(path.join(__dirname, "derived", "probe.json"), JSON.stringify(rows, null, 1) + "\n");
