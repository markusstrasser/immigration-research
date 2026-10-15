/* Native-First: inspect the adopted package; never rebuild or write its lane. */
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const P = require("../main_case_2026_10_15/package.cjs");
const HERE = __dirname, FISCAL = path.dirname(HERE);
const LINES = ["general_sales_tax", "excise_selective_sales", "customs_duties"];
const GENS = ["G1", "G2", "G3plus"];
const mean = a => a.reduce((s,n)=>s+n,0)/a.length;
const source = rel => ({path:rel,sha256:crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL,rel))).digest("hex")});
function snapshot() {
  const out = {population:P.POPULATION_V8, methods:P.METHODS, baseline:{}, lines:{},
    sources:["main_case_2026_10_15/derived/corrections.json", "main_case_2026_10_15/derived/corrections_cash.json",
      "main_case_2026_10_15/package.cjs", "job_capital_taxes_2026_10_14/derived/wages_by_industry.csv"].map(source)};
  for(const which of ["set","cash"]) {
    const X = which==="set"?P:P.CASH, m = X.payloadModel();
    const costs = P.METHODS.map(method => {
      const mm=X.modelFor("central",method,X.withCentral({}));
      return X.MAIN_SPECS.map(s=>X.cost(mm,s));
    });
    const ends=costs.map(v=>[v.indexOf(Math.min(...v)),v.indexOf(Math.max(...v))]);
    const band=[0,1].map(e=>mean(costs.map((v,i)=>v[ends[i][e]])));
    const want=which==="set"?[365.791930,455.981785]:[281.752564,371.942418];
    if(band.some((v,i)=>Math.abs(v-want[i])>1e-6))throw Error("[BLOCKED] v8 unchanged gate "+which);
    if(!ends.every(e=>e[0]===16&&e[1]===11))throw Error("[BLOCKED] v8 end indices changed");
    out.baseline[which]={band_bn:band,end_specifications:ends};
    out.lines[which]={};
    for(const id of LINES) {
      const l=m.receipts.lines.find(l=>l.id===id), c=l.cells[m.receipts.reference].personal;
      const carriers=Object.entries(m.corrections.union_completion?.carriers||{}).filter(([,v])=>v.side==="receipt"&&v.parent_line===id);
      const amounts=Object.fromEntries(carriers.map(([k])=>[k,m.spending.lines.find(l=>l.id===k).keys]));
      const coverage=Object.fromEntries(["low","high"].map(end=>[end,
        GENS.map(g=>X.POST_ENGINE.coverage.by_end[end].decomposition.line_parts.filter(p=>p.source_side==="receipt"&&p.source_line===id&&p.generation===g).reduce((s,p)=>s+p.coverage_bn,0))]));
      out.lines[which][id]={national_bn:l.national_bn,engine_target_bn:c.target_bn,engine_share:c.share,
        direct:c.direct,key:c.key,carriers:amounts,coverage_cost_by_generation_bn:coverage};
    }
    const op=m.receipts.lines.find(l=>l.id==="other_production_taxes");
    out.baseline[which].job_production_share=op.cells[m.receipts.reference].personal.target_bn/op.national_bn;
    out.baseline[which].item6=m.corrections.job_capital_taxes;
  }
  return out;
}
if(require.main===module) {
  const out=snapshot();
  fs.mkdirSync(path.join(HERE,"derived"),{recursive:true});
  fs.writeFileSync(path.join(HERE,"derived/case_snapshot.json"),JSON.stringify(out,null,2)+"\n");
  console.log("v8 unchanged set "+out.baseline.set.band_bn.map(n=>n.toFixed(9)).join(" / "));
  console.log("v8 unchanged cash "+out.baseline.cash.band_bn.map(n=>n.toFixed(9)).join(" / "));
}
module.exports={snapshot,LINES};
