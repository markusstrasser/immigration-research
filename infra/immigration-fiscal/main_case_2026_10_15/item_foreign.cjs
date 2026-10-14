/* Item 9: domestic-source corporate tax on each model, national totals unchanged. */
"use strict";
const V7 = require("../main_case_2026_10_14/package.cjs");
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const F = path.join(__dirname,"..");
const SOURCE = "job_capital_key_refine_2026_10_14/derived/summary.json";
const clone = x => JSON.parse(JSON.stringify(x));
const sha = f => crypto.createHash("sha256").update(fs.readFileSync(path.join(F,f))).digest("hex");
const read = f => JSON.parse(fs.readFileSync(path.join(F,f),"utf8"));
const LINES = ["corporate_capital","corporate_labor"];
const ALLOCS = ["personal","shared"];
function build(ctx, arm, which) {
  if (arm) throw Error("[BLOCKED] foreign_source_tax has no arm");
  const Q=ctx.B, api=which==="cash"?Q.CASH:Q, m=api.payloadModel();
  const original=V7.JOBCAP.blockOf(null), domestic=V7.JOBCAP.blockOf("foreign_source_removed");
  const D=Q.ITEM_DETAIL.job_capital_taxes[which];
  if (!D) throw Error("[BLOCKED] foreign_source_tax requires job_capital_taxes");
  const fractions = Object.fromEntries(V7.JOBCAP.PARTS.map(p=>[p,Object.fromEntries(ALLOCS.map(a=>{
    const old=p.startsWith("union_")?original.by_generation[p.slice(6)].corporate[a]:original.factor[p==="lineage_g3plus"?"G3plus":"white_nh"].corporate[a]*original.lines.corporate.national_bn;
    const now=p.startsWith("union_")?domestic.by_generation[p.slice(6)].corporate[a]:domestic.factor[p==="lineage_g3plus"?"G3plus":"white_nh"].corporate[a]*domestic.lines.corporate.national_bn;
    return [a,Q.ITEM_ARMS?.job_capital_taxes==="foreign_source_removed"?0:old===0?0:1-now/old];
  }))]));
  const edits=[],parts={}, totals={};
  for(const id of LINES) for(const sc of m.receipts.scenarios) {
    const line=m.receipts.lines.find(l=>l.id===id), k=`${id}|${sc}`, j=edits.length;
    const by={personal:0,shared:0}; totals[k]={};
    for(const a of ALLOCS) totals[k][a]=line.cells[sc][a].target_bn+line.cells[sc][a].other_bn;
    for(const p of V7.JOBCAP.PARTS) {
      const d=Object.fromEntries(ALLOCS.map(a=>[a,-D.new_parts[k][p][a]*fractions[p][a]]));
      parts[`${p}:${id}:${sc}`]={edit:j,by:d};
      for(const a of ALLOCS) by[a]+=d[a];
    }
    edits.push({side:"receipt",line:id,scenario:sc,by});
  }
  function editsAt(mm) {return edits.map(e=>{
    const l=mm.receipts.lines.find(l=>l.id===e.line),c=l.cells[e.scenario],k=`${e.line}|${e.scenario}`;
    return {...e,by:Object.fromEntries(ALLOCS.map(a=>{const total=c[a].target_bn+c[a].other_bn;
      if(totals[k][a]===0){if(total!==0)throw Error("[BLOCKED] zero corporate scenario acquired a nonzero base");return [a,0];}
      return [a,e.by[a]*total/totals[k][a]];}))};
  });}
  const oracle=read(SOURCE).arms.K2_foreign_source_removed;
  return {edits,editsAt,parts,meta:{foreign_source_tax:{rule:"Remove US residence tax on foreign-source income from item 6's corporate source tax; each generation and added-person part takes its domestic-source fraction on the model's own cell total. National totals hold; state tax fixed.",foreign_source_ty2021_bn:59.280288,fractions,source:{file:SOURCE,sha256:sha(SOURCE)},conditional_se:oracle}},record:{source:{file:SOURCE,sha256:sha(SOURCE)},fractions},detail:{fractions}};
}
module.exports={build,LINES,SOURCE};
