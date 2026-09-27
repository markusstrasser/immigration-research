// Read-only structural diagnostic; these are single-specification model outputs.
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../../..');
const lane = path.join(root, 'infra/immigration-fiscal');
const source = path.join(lane, 'main_case_long_run_2026_09_27/package.cjs');
const p = require(source);
const model = p.modelFor('central', p.METHODS[0], p.withCentral({}));
const spec = p.MAIN_SPECS[0];
const rows = [1.5, 2, 2.5].map(sigma => {
  const state = p.stateFor(model, spec, p.MAIN_PROFILE);
  state.production.sigma = sigma;
  const e = p.Engine.evaluate(model, state);
  return {
    sigma, direct_fiscal_bn: e.direct_fiscal_response_bn,
    private_wtp_bn: e.private_wtp_bn, induced_receipts_bn: e.induced_receipts_bn,
    capital_return_bn: p.capitalReturn(e, spec).total_bn,
    target_balance_bn: e.target_balance_bn, normalized_gap_bn: e.normalized_gap_bn,
  };
});
if (rows.some(r => !Object.values(r).every(Number.isFinite))) {
  throw new Error('Nonfinite diagnostic output');
}
if (new Set(rows.map(r => r.direct_fiscal_bn)).size !== 1 ||
    new Set(rows.map(r => r.capital_return_bn)).size !== 1 ||
    new Set(rows.map(r => r.private_wtp_bn + r.induced_receipts_bn)).size < 2) {
  throw new Error('Audited fiscal/production interface has changed; revisit the finding');
}
console.log(JSON.stringify({
  interpretation: 'Public spending invariant to production wage scenarios; no revised headline.',
  inputs_sha256: Object.fromEntries([
    source, path.join(lane, 'assumption_explorer_2026_09_21/engine.js'),
    path.join(lane, 'matched_benefits_2026_09_19/builder.py'),
    path.join(lane, 'matched_benefits_2026_09_19/model.py'),
  ].map(f => [path.relative(root, f), crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')])),
  rows,
}, null, 2));
