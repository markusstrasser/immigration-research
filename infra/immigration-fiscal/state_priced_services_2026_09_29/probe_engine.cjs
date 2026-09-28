/* Read the adopted main case's group shares and responses for the three lines this lane re-prices.
 * Positive control: the mean over the two methods of evaluateFull at the end specifications (48 low, 11 high)
 * reproduces the published main case, $321.819–387.370bn (main_case_long_run_2026_09_27/derived/summary.json).
 * Engine sign: a receipt enters the cost as -response x group amount, a spending line as +response x amount.
 * Run: node probe_engine.cjs [--out-dir DIR] -> derived/engine_lines.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_long_run_2026_09_27", "package.cjs"));
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(__dirname, "derived"));
const LINES = ["public_order_safety", "health_services", "general_public_services", "housing_community_services",
  "recreation_culture"];
// Receipt lines this lane re-prices by state (S&L taxes keyed at a national rate) or documents as already state-keyed.
const RECEIPTS = ["general_sales_tax", "excise_selective_sales", "personal_motor_vehicle", "state_local_income_tax",
  "other_personal_tax", "modeled_owner_property", "personal_property_tax", "remaining_production_property",
  "other_production_taxes", "personal_current_transfers", "customs_duties"];

const summary = JSON.parse(fs.readFileSync(path.join(P.HERE, "derived", "summary.json"), "utf8"));
const specs = P.specsFor({});
const ends = summary.end_specifications.map((e) => [e.low_end.index, e.high_end.index]);
const models = P.METHODS.map((m) => P.modelFor("central", m, P.withCentral({})));
const runs = models.map((m, i) => ends[i].map((j) => P.evaluateFull(m, specs[j])));
const band = [0, 1].map((k) => runs.reduce((a, r) => a + r[k].cost_bn, 0) / runs.length);
if (Math.abs(band[0] - summary.main_case[0]) > 1e-6 || Math.abs(band[1] - summary.main_case[1]) > 1e-6) {
  throw new Error(`[BLOCKED] main case not reproduced: ${band} vs ${summary.main_case}`);
}
const lines = {};
for (const id of LINES) {
  const rows = runs.flatMap((r) => r.map((x) => x.evaluation.spending.find((l) => l.id === id)));
  const shares = rows.map((l) => l.amount_bn / l.national_bn);
  if (Math.max(...shares) - Math.min(...shares) > 1e-12) throw new Error(`${id}: share varies across end specs`);
  lines[id] = { key: rows[0].key, national_bn: rows[0].national_bn, group_bn: rows[0].amount_bn, share: shares[0],
    response_low: runs[0][0].evaluation.spending.find((l) => l.id === id).response,
    response_high: runs[0][1].evaluation.spending.find((l) => l.id === id).response };
}
// Receipt shares differ by allocation (low end shared, high end personal) and by method. The band is the mean over
// the two methods, and a correction is linear in the share, so the mean share applies; per-method shares are kept.
const receipts = {};
for (const id of RECEIPTS) {
  const at = (k) => {
    const rows = runs.map((r) => r[k].evaluation.receipts.find((l) => l.id === id));
    const responses = rows.map((l) => l.response);
    if (Math.max(...responses) !== Math.min(...responses)) throw new Error(`${id}: response varies across methods`);
    const shares = rows.map((l) => l.amount_bn / l.national_bn);
    return { key: rows[0].key, national_bn: rows[0].national_bn, response: responses[0], shares,
      share: shares.reduce((a, b) => a + b, 0) / shares.length };
  };
  const lo = at(0), hi = at(1);
  receipts[id] = { key: lo.key, national_bn: lo.national_bn, share_low: lo.share, share_high: hi.share,
    share_low_by_method: lo.shares, share_high_by_method: hi.shares, response_low: lo.response, response_high: hi.response };
}
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "engine_lines.json"), JSON.stringify({
  source: "main_case_long_run_2026_09_27/package.cjs evaluateFull, adopted models (central), end specifications",
  end_specifications: ends, band_reproduced_bn: band, lines, receipts }, null, 1) + "\n");
console.log(JSON.stringify({ lines, receipts }, null, 1), band);
