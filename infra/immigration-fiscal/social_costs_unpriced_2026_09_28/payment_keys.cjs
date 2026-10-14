/* The business-security payment key is consumption, never an offending ratio. */
const fs = require("fs"), path = require("path"), assert = require("assert");
const H = __dirname, F = path.dirname(H);
const P = require(path.join(F, "main_case_2026_10_14/package.cjs"));
const meta = JSON.parse(fs.readFileSync(path.join(F, "sept24_propagation_2026_09_24/derived/oct14/band_variants.json")));
const model = P.payloadModel(), line = model.receipts.lines.find(l => l.id === "general_sales_tax");
const records = {};
for (const [end, index] of [["low",16],["high",11]]) {
  const spec = P.MAIN_SPECS[index];
  assert.strictEqual(spec.allocation, "personal");
  const scenario = P.stateFor(P.withSyntheticLines(model), spec, P.MAIN_PROFILE).receipt_scenario;
  const cell = line.cells[scenario].personal;
  assert(Math.abs(cell.target_bn + cell.other_bn - line.national_bn) < 1e-6);
  const on_case = meta.items.lineage_social_keys_on_the_case[`${end}_end`];
  if (on_case.unstated && on_case.unstated.consumption) throw new Error("[BLOCKED] current-case consumption lineage share is unstated");
  const moved = on_case.moved.includes("consumption");
  const d_over_u = moved ? on_case.shares.consumption : meta.lineage_social_keys[`${end}_end`].consumption;
  assert(Number.isFinite(d_over_u) && d_over_u >= 0);
  const union_amount = cell.target_bn / (1+d_over_u);
  records[end] = {personal_specification:index, receipt_scenario:scenario,
    union_share:union_amount/line.national_bn, lineage_share:cell.target_bn/line.national_bn,
    added_share:(cell.target_bn-union_amount)/line.national_bn, national_bn:line.national_bn,
    union_bn:union_amount, added_bn:cell.target_bn-union_amount,
    lineage_ratio_source:moved ? "meta.items.lineage_social_keys_on_the_case" : "meta.lineage_social_keys",
    rule:"Current personal general-sales-tax consumption key; current moved D/U declaration takes precedence; business pass-through premise [ASSUMPTION]"};
  assert(records[end].union_share >= 0 && records[end].lineage_share <= 1);
  assert(Math.abs((records[end].lineage_share/records[end].union_share-1)-d_over_u) < 1e-12);
}
fs.writeFileSync(path.join(H,"derived/payment_keys.json"),JSON.stringify(records,null,2)+"\n");
console.log(records);
