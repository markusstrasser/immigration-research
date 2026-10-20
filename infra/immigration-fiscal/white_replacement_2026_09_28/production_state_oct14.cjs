// Read the adopted package; never rebuild or write the frozen case.
const fs = require('fs');
const path = require('path');
const P = require('../main_case_2026_10_16/package.cjs');
const summary = require('../main_case_2026_10_16/derived/summary.json');
const oo = P.withCentral({});
const specs = P.specsFor(oo);
const out = {};
for (const [i, end] of ['low', 'high'].entries()) {
  const spec = summary.v9.end_specifications.set[0][i];
  if (spec !== summary.v9.end_specifications.set[1][i]) throw Error('[BLOCKED] method-specific comparator ends');
  const states = P.METHODS.map(method => P.stateFor(P.modelFor('central', method, oo), specs[spec]).production);
  if (JSON.stringify(states[0]) !== JSON.stringify(states[1])) throw Error('[BLOCKED] production methods use different cells');
  out[end] = {spec, ...states[0]};
}
fs.writeFileSync(path.join(__dirname, 'derived/production_state_oct16.json'), JSON.stringify(out, null, 2) + '\n');
console.log('[PASS] adopted production cells exported read-only');
