/* Export the live cash/set trust-fund block from the authoritative v7 engine.
 * Native-First: call the existing package rather than duplicate its calculations.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("../main_case_2026_10_14/package.cjs");
const E = P.Engine;
const load = name => JSON.parse(fs.readFileSync(path.join(__dirname, "../main_case_2026_10_14/derived", name)));
const payload = load("corrections.json"), cashPayload = load("corrections_cash.json");
const setModel = E.applyCorrections(P.MODEL, payload), cashModel = E.applyCorrections(P.MODEL, cashPayload);
const summary = load("summary.json");
const rows = {};
const programmes = {};
function amount(ev, side, id) {
  const hits = ev[side === "receipt" ? "receipts" : "spending"].filter(x => x.id === id);
  if (hits.length !== 1) throw new Error(`[BLOCKED] ${side}/${id}: ${hits.length} lines`);
  return hits[0].amount_bn;
}
for (const [j, end] of ["low", "high"].entries()) {
  const spec = P.MAIN_SPECS[summary.v7.end_specifications.set[j]];
  const set = P.evaluateFull(setModel, spec), cash = P.evaluateFull(cashModel, spec);
  const gap = set.cost_bn - cash.cost_bn;
  if (Math.abs(gap - (summary.v7.band_bn[j] - summary.v7.cash_set_bn[j])) > 1e-9)
    throw new Error("[BLOCKED] pension increment differs from live case");
  const payroll = ["employee_oasdi", "employer_oasdi", "employee_hi", "employer_hi", "self_employment_oasdi_hi"]
    .reduce((s, id) => s + amount(cash.evaluation, "receipt", id), 0);
  const cashBenefits = amount(cash.evaluation, "spending", "social_security")
    + payload.meta.pension_accrual.part_a_share * amount(cash.evaluation, "spending", "medicare");
  const hiAccrual = amount(set.evaluation, "spending", "medicare") - amount(cash.evaluation, "spending", "medicare")
    + payload.meta.pension_accrual.part_a_share * amount(cash.evaluation, "spending", "medicare");
  rows[end] = { payroll_bn: payroll, cash_benefits_bn: cashBenefits, accrual_bn: gap,
    hi_payout_fraction: hiAccrual / (hiAccrual + amount(set.evaluation, "spending", "social_security")),
    trust_cost_bn: cashBenefits + gap - payroll, set_cost_bn: set.cost_bn, cash_cost_bn: cash.cost_bn };
  const nationals = new Map(P.withSyntheticLines(setModel).spending.lines.map(l=>[l.id,l.national_bn]));
  programmes[end] = set.evaluation.spending.filter(l=>l.response>0 && nationals.get(l.id)>0)
    .map(l=>({id:l.id,national_bn:nationals.get(l.id),response:l.response}));
  const education = programmes[end].find(l=>l.id==="education_services");
  const schoolWeight = payload.meta.user_fees.k12_weight.w_K;
  if (!(schoolWeight>0 && schoolWeight<1) || !education) throw new Error("[BLOCKED] education receipt split contract");
  programmes[end] = programmes[end].filter(l=>l.id!=="education_services").concat([
    {id:"education_k12",national_bn:education.national_bn*schoolWeight,response:education.response},
    {id:"education_college_other",national_bn:education.national_bn*(1-schoolWeight),response:education.response}
  ]);
  const splitTotal = programmes[end].filter(l=>l.id.startsWith("education_") && l.id!=="education_benefits")
    .reduce((s,l)=>s+l.national_bn*l.response,0);
  if (Math.abs(splitTotal-education.national_bn*education.response)>1e-9)
    throw new Error("[BLOCKED] responding education budget split does not close");
}
const i = process.argv.indexOf("--out-dir");
const out = i > 0 ? path.resolve(process.argv[i + 1]) : path.join(__dirname, "derived/oct14");
fs.mkdirSync(out, {recursive:true});
fs.writeFileSync(path.join(out, "p7_trust_inputs.json"), JSON.stringify({
  case:"oct14", rows, programmes,
  rule:"gross 2024 payroll receipts, cash OASDI and Part A benefits, and the complete net pension increment (including benefit-tax adjustment); all three travel together",
  sources:["main_case_2026_10_14/derived/corrections.json", "main_case_2026_10_14/derived/corrections_cash.json", "main_case_2026_10_14/derived/summary.json"]
}, null, 1) + "\n");
console.log("[p7 trust]", rows);
