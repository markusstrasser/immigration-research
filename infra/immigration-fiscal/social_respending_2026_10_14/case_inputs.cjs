/* Frozen-v7 current-dollar fiscal saving, with a union projection at the same
 * responses. Native-First: use the case's existing engine, no second fiscal model.
 * Writes only this lane. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("../main_case_2026_10_14/package.cjs");
const HERE = __dirname;
const clone = x => JSON.parse(JSON.stringify(x));
const payload = P.CASH.correctionsPayload();
const summary = JSON.parse(fs.readFileSync(path.join(HERE, "../main_case_2026_10_14/derived/summary.json")));
const near = (a,b) => { if(Math.abs(a-b)>1e-9) throw Error(`[BLOCKED] fiscal control ${a} != ${b}`); };
// Project the existing case onto its identified members: exclude the declared
// lineage block and each explicitly declared lineage part of subsequent edits.
// Keep national totals and v7 response rules fixed: this is a contribution,
// not a newly optimized case without the added descendants.
const union = clone(payload), L = payload.meta.lineage.edits;
union.edits = clone(payload.edits);
for (const item of payload.meta.items) {
  if (!item.edits || !item.parts) continue;
  for (const [name,part] of Object.entries(item.parts)) {
    if (!name.startsWith("lineage_")) continue;
    const e = union.edits[item.edits.first+part.edit];
    if (!e || !e.by) throw Error(`[BLOCKED] undeclared lineage edit ${name}`);
    for(const a of ["personal","shared"]) e.by[a] -= part.by[a];
  }
}
union.edits.splice(L.first,L.count);
const baseRel = P.V6_PACKAGE.BASE_FILES.cash;
union.production = clone(P.readJson(baseRel).production);
delete union.meta.lineage;
const q = P.CASH, rows=[];
for(const [basis,p] of [["lineage",payload],["identified_union_at_case_responses",union]]) {
  const m = P.Engine.applyCorrections(P.MODEL,p);
  for(const [end,i] of [["low",16],["high",11]]) {
    const r=q.evaluateFull(m,q.MAIN_SPECS[i],q.MAIN_PROFILE), e=r.evaluation;
    if(basis==="lineage") {
      near(r.cost_bn,summary.cash_set.band_bn[end==="low"?0:1]);
      near(r.capital.total_bn,summary.capital_at_end_specifications.total_bn[end==="low"?0:1]);
    }
    const H = -e.direct_fiscal_response_bn-e.induced_receipts_bn;
    near(H,r.cost_bn-r.capital.total_bn+e.private_wtp_bn);
    const service=e.spending.filter(x=>x.family==="consumption");
    rows.push({population_basis:basis,end,specification:i,cash_set_cost_bn:r.cost_bn,
      capital_return_bn:r.capital.total_bn,private_wtp_bn:e.private_wtp_bn,
      induced_receipts_bn:e.induced_receipts_bn,current_budget_saving_bn:H,
      government_consumption_removed_bn:-service.reduce((s,x)=>s+x.effect_bn,0),
      government_consumption_national_bn:service.reduce((s,x)=>s+x.national_bn,0)});
  }
}
fs.mkdirSync(path.join(HERE,"derived"),{recursive:true});
fs.writeFileSync(path.join(HERE,"derived/case_inputs.json"),JSON.stringify({
  source:"frozen main_case_2026_10_14/package.cjs CASH; personal specs 16/11",
  H_rule:"H=-direct_fiscal_response-induced_receipts=cash_set_cost-capital_return+private_wtp; accrued benefit promises and capital return finance no current spending; private WTP is not a budget saving",
  union_rule:"declared lineage edit block and lineage_* item parts excluded; base production restored; full-case national totals, specifications and response rules held fixed; contribution, not standalone removal case",
  funding_accounting_basis:"national_accounts",
  lineage:payload.meta.lineage.counts,rows,gates:{frozen_cash_band:true,capital_return:true,budget_identity:true}
},null,2)+"\n");
console.log(rows);
