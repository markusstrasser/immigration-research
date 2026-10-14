/* Read v7's live housing cells; split the added people using its own part models. */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("../main_case_2026_10_14/package.cjs");
const m = P.payloadModel(), cp = P.correctionsPayload();
const detail = P.ITEM_DETAIL.added_age_mix, pm = detail.part_models.set;
const {later, g3_rate, c3} = detail.counts;
const ref = m.receipts.reference;
const cell = (model, id) => model.receipts.lines.find(x => x.id === id).cells[ref].personal;
const out = {gates: [], lines: {}};
const k = cp.meta.items.find(x => x.id === "row4_frame");
const row4Edits = cp.edits.slice(k.edits.first, k.edits.first + k.edits.count);
for (const id of ["modeled_owner_property", "tenant_occupied_property"]) {
  const c = cell(m, id), national = c.target_bn + c.other_bn;
  const gp = later * cell(pm.later, id).target_bn + (1-c3)*g3_rate*cell(pm.g3_rate,id).target_bn;
  const wp = c3*g3_rate*cell(pm.white_g3_rate,id).target_bn;
  let extra = 0;
  for (const [name, part] of Object.entries(k.parts)) {
    if (name.endsWith(`:${id}:${ref}`) && name.startsWith("lineage_")) extra += part.by.personal;
  }
  // Item 8 is the only later edit of these housing lines. The invariant below
  // catches future changes rather than silently pricing them as unchanged.
  const U = P.SEPT29.payloadModel(), uc = cell(U,id);
  let unionExtra = 0;
  for (const [name, part] of Object.entries(k.parts)) {
    if (name.endsWith(`:${id}:${ref}`) && name.startsWith("union_")) unionExtra += part.by.personal;
  }
  const union = uc.target_bn + unionExtra;
  const added = gp+wp+extra;
  const gap = Math.abs(union+added-c.target_bn);
  if (!(gap < 1e-9)) throw new Error(`[BLOCKED] housing parts ${id}: ${gap}`);
  out.gates.push({name:`${id} union plus added closes live v7`,passed:true,gap_bn:gap});
  out.lines[id] = {national_bn:national, union_target_bn:union, added_target_bn:added,
    union_share:union/national,lineage_share:c.target_bn/national,
    response:cp.meta.responses[id],key:c.key};
}
fs.writeFileSync(path.join(__dirname,"derived/housing_keys.json"),JSON.stringify(out,null,2)+"\n");
console.log(JSON.stringify(out,null,2));
