/* Report-only v7 endpoint effects: union custody/arrest key shift, descendants held. */
const fs = require("fs"), path = require("path"), assert = require("assert");
const H = __dirname, F = path.dirname(H);
const P = require(path.join(F, "main_case_2026_10_14/package.cjs"));
const a = JSON.parse(fs.readFileSync(path.join(H, "derived/report_checks_custody.json")));
const base = P.payloadModel();
// State-price national gap is on v4 weights; v7 applies row4's price-index ratio.
const row4 = require(path.join(F, "row4_class_2026_09_29/derived/row4_state_index.json"));
function moved(delta) {
  const m = JSON.parse(JSON.stringify(base));
  const parent = m.spending.lines.find(l => l.id === "public_order_safety");
  for (const alloc of ["personal", "shared"]) {
    const k = parent.keys.use[alloc];
    k.target_bn += delta; k.other_bn -= delta;
    k.share = k.target_bn / parent.national_bn;
    assert(Math.abs(k.target_bn + k.other_bn - parent.national_bn) < 1e-9);
  }
  const pricing = m.corrections.state_pricing.lines.find(l => l.parent === parent.id);
  const sp = m.spending.lines.find(l => l.id === pricing.line);
  const d = row4.lines[parent.id].ratio * pricing.national_gap_bn * delta / parent.national_bn;
  for (const alloc of ["personal", "shared"]) {
    sp.keys.k[alloc].target_bn += d; sp.keys.k[alloc].other_bn -= d;
    sp.keys.k[alloc].share = sp.keys.k[alloc].target_bn / sp.national_bn;
  }
  const touched = new Set([parent.id, sp.id]);
  for (const l of base.spending.lines) if (!touched.has(l.id)) assert.deepStrictEqual(m.spending.lines.find(x=>x.id===l.id),l);
  assert.deepStrictEqual(m.receipts,base.receipts);
  return m;
}
const rows = [];
for (const [name, delta] of [["custody only",a.prison_raw_key_change_bn],["custody plus arrest rescaling",a.custody_and_arrests_raw_key_change_bn]]) {
  const m = moved(delta);
  for (const [end,j] of [["low",16],["high",11]]) {
    const before = P.evaluateFull(base,P.MAIN_SPECS[j],P.MAIN_PROFILE).cost_bn;
    const after = P.evaluateFull(m,P.MAIN_SPECS[j],P.MAIN_PROFILE).cost_bn;
    assert(Math.abs(before - ({low:339.5520178295269,high:423.6492607005069})[end]) < 1e-6);
    rows.push({scenario:name,end,personal_specification:j,before_bn:before,after_bn:after,delta_bn:after-before,
      population:"39.71M union changed; added descendants held at case amounts; same absolute delta on 42.75M lineage",
      assumption:"Existing central 50% arrest police and 60% criminal court shares; same national state-price gap per justice service unit"});
  }
}
fs.writeFileSync(path.join(H,"derived/report_checks_fiscal.json"),JSON.stringify(rows,null,2)+"\n");
console.log(rows);
