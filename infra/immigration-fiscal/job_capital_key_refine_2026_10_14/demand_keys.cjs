/* Read the case's general consumption carrier; keep the consumption-lane basis. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("../main_case_2026_10_14/package.cjs");
const share = pkg => {
  const m = pkg.payloadModel();
  const c = m.receipts.lines.find(x => x.id === "personal_current_transfers").cells[m.receipts.reference].personal;
  if (c.key !== "consumption") throw Error("[BLOCKED] demand carrier is no longer consumption");
  return c.target_bn / (c.target_bn + c.other_bn);
};
const union = share(P.SEPT29), lineage = share(P);
const out = {union_live: union, lineage_live: lineage, added_demand_share: lineage-union,
  carrier: "personal_current_transfers", rule: "general consumption carrier, not selective/general sales tax-specific adjustments",
  gates: [{name: "finite demand and positive added share", passed: [union,lineage].every(x=>Number.isFinite(x)&&x>0&&x<1)&&lineage>union}]};
if (!out.gates.every(x=>x.passed)) throw Error("[BLOCKED] demand shares");
fs.writeFileSync(path.join(__dirname,"derived/demand_keys.json"),JSON.stringify(out,null,2)+"\n");
console.log(JSON.stringify(out));
