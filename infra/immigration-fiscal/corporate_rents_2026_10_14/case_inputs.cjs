/* Read-only frozen-v7 consumer and positive control. Writes only this lane. */
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const HERE = __dirname, FISCAL = path.dirname(HERE);
const read = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const gates = [];
function gate(name, ok, detail) {
  gates.push({ name, passed: !!ok, detail });
  if (!ok) throw Error(`[BLOCKED] ${name}: ${detail}`);
}
const ROOT = path.resolve(HERE,"../../..");
for (const x of read(path.join(HERE,"inputs/pins.json")).files.filter(x=>x.root==="repo")) {
  const digest=crypto.createHash("sha256").update(fs.readFileSync(path.join(ROOT,x.path))).digest("hex");
  gate(`frozen upstream pin: ${x.path}`,digest===x.sha256,digest);
}
const P = require(path.join(FISCAL, "main_case_2026_10_14/package.cjs"));
const mean = (a) => a.reduce((s, x) => s + x, 0) / a.length;
const S = read(path.join(FISCAL, "main_case_2026_10_14/derived/summary.json"));
const L = read(path.join(FISCAL, "main_case_2026_10_14/derived/lineage_addition.json"));
const payload = P.correctionsPayload(), J = payload.meta.job_capital_taxes;
const corporate = J.lines.corporate;
gate("v7 adopted, personal, ends 16/11", S.v7.case_key === "oct14" && !J.stub
  && S.v7.end_specifications.set.join() === "16,11", S.v7.end_specifications);
for (const [api, expected, basis] of [[P, S.v7.band_bn, "set"], [P.CASH, S.v7.cash_set_bn, "cash"]]) {
  const actual = api.central();
  gate(`${basis}: live package positive control vs frozen central (1e-9bn)`,
    actual.every((v, i) => Math.abs(v - expected[i]) < 1e-9), actual);
}
const parts = P.ITEM_DETAIL.job_capital_taxes.set.new_parts;
const amounts = Object.fromEntries(Object.keys(parts["corporate_capital|cbo_collective"]).map(k =>
  [k, corporate.model_lines.reduce((v, id) => v + parts[`${id}|cbo_collective`][k].personal, 0)]));
const unionCorporate = Object.entries(amounts).filter(([k]) => k.startsWith("union_")).reduce((v, [, x]) => v + x, 0);
const lineageCorporate = Object.values(amounts).reduce((v, x) => v + x, 0);
gate("corporate generations conserve union (1e-9bn)", Math.abs(unionCorporate - corporate.group_bn.personal) < 1e-9, unionCorporate);
gate("corporate parts conserve lineage (1e-9bn)", Math.abs(lineageCorporate - corporate.group_after_bn.personal) < 1e-9, lineageCorporate);
gate("corporate key times national reproduces union (1e-9bn)", Math.abs(corporate.key_share.personal * corporate.national_bn - unionCorporate) < 1e-9, corporate.national_bn);
gate("production residence-capital term remains zero", J.production.capital_tax_term_bn === 0, J.production);
const fixedControl = S.v7.arms.job_capital_taxes_normal_return_share;
const fixedControlBand = fixedControl.band_bn || fixedControl.set_bn;
gate("normal-return arm field present", Array.isArray(fixedControlBand), Object.keys(fixedControl));
const normal = corporate.response.high;
gate("existing fixed-rent phi=1 arm closes (1e-9bn)",
  Math.abs(fixedControlBand[0] - S.v7.band_bn[0] - (1-normal)*lineageCorporate) < 1e-9
  && Math.abs(fixedControlBand[1] - S.v7.band_bn[1]) < 1e-9, fixedControlBand);

// Customs is a pure consumption-key line; sales is state-priced and excises include fuel re-keying.
// The central methods differ. Reconstruct added people's own consumption cells, never flat-scale.
const A = P.ITEM_DETAIL.added_age_mix, n = A.counts, pm = A.part_models.set;
const cell = (m) => m.receipts.lines.find(l => l.id === "customs_duties").cells.cbo_collective.personal;
const addedCustoms = n.later * cell(pm.later).target_bn
  + n.g3_rate * ((1-n.c3)*cell(pm.g3_rate).target_bn + n.c3*cell(pm.white_g3_rate).target_bn);
const consumption = P.METHODS.map(method => {
  const c = cell(P.modelFor("central", method, P.withCentral({})));
  const national = c.target_bn + c.other_bn;
  const union = c.target_bn - addedCustoms;
  gate(`${method}: consumption member + other closes national (1e-9bn)`, Math.abs(union + addedCustoms + c.other_bn - national) < 1e-9, national);
  gate(`${method}: consumption key nonnegative and conserves shares (1e-12)`,
    union >= 0 && c.other_bn >= 0 && Math.abs(union/national + addedCustoms/national + c.other_bn/national-1) < 1e-12, union/national);
  return { method, national_bn: national, union: union/national, lineage: c.target_bn/national, added: addedCustoms/national };
});
const counts = payload.meta.lineage.counts;
gate("population conservation (1e-6 persons)", Math.abs(counts.account_union + counts.added - counts.lineage_population) < 1e-6, counts);
const paths = ["main_case_2026_10_14/derived/summary.json", "main_case_2026_10_14/derived/corrections.json",
  "main_case_2026_10_14/derived/lineage_addition.json", "job_capital_taxes_2026_10_14/derived/items.csv",
  "job_capital_taxes_2026_10_14/derived/item.json", "consumption_key_2026_09_24/derived/summary.json"];
const out = {
  rule: "one change at frozen v7 personal specifications 16/11; consumption proxy = customs consumption cells, methods averaged; added persons rebuilt at own ages",
  baseline_lineage_bn: S.v7.band_bn, baseline_lineage_cash_bn: S.v7.cash_set_bn,
  baseline_union_bn: L.set.union_at_case_responses_bn,
  baseline_union_cash_bn: L.cash.union_at_case_responses_bn,
  union_baseline_rule: "the union at frozen v7 lineage responses, not the different union-only removal responses",
  population: { union: counts.account_union, added: counts.added, lineage: counts.lineage_population },
  corporate: { national_bn: corporate.national_bn, normal_share: normal, union_bn: unionCorporate, lineage_bn: lineageCorporate, parts_bn: amounts },
  consumption: { by_method: consumption, union: mean(consumption.map(x=>x.union)), lineage: mean(consumption.map(x=>x.lineage)),
    note: "Proxy for proportional market rents; neither a measured corporate-rent elasticity nor a US-only corporate sales share. Customs was chosen to avoid state price/fuel keys." },
  source_hashes: Object.fromEntries(paths.map(p=>[p, crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL,p))).digest("hex")])),
  gates,
};
fs.mkdirSync(path.join(HERE,"derived"), { recursive: true });
fs.writeFileSync(path.join(HERE,"derived/case_inputs.json"), JSON.stringify(out,null,2)+"\n");
console.log(`PASS: ${gates.length} frozen-v7 controls; corporate union/lineage ${unionCorporate}/${lineageCorporate}; consumption ${out.consumption.union}/${out.consumption.lineage}`);
