"use strict";
// Read-only live v8 evaluation and narrow source-tax parts. No case is built.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const P=require("../main_case_2026_10_15/package.cjs");
const HERE=__dirname, F=path.join(HERE,".."), ends=["low","high"], specs=[16,11];
const mean=xs=>xs.reduce((a,b)=>a+b,0)/xs.length;
const meta=P.correctionsPayload().meta;
const out={baseline:{},population:meta.population_v8,parts:{},by_end:{},
  methods:P.METHODS,specifications:specs,lineage_rates:meta.job_capital_taxes.lineage.wage_share};
const parts=P.ITEM_DETAIL.job_capital_taxes.set.new_parts;
const foreign=meta.foreign_source_tax.fractions;
out.parts=Object.fromEntries(P.JOBCAP.PARTS.map(g=>[g,["corporate_capital","corporate_labor"].reduce((s,id)=>
  s+parts[`${id}|cbo_collective`][g].personal*(1-foreign[g].personal),0)]));
for(const which of ["set","cash"]){
  const Q=which==="set"?P:P.CASH;
  const models=P.METHODS.map(method=>Q.modelFor("central",method,Q.withCentral({})));
  out.baseline[which]=[];out.by_end[which]={};
  for(let i=0;i<2;i++){
    const end=ends[i],s=Q.MAIN_SPECS[specs[i]],runs=models.map(m=>Q.evaluateFull(m,s));
    out.baseline[which].push(mean(runs.map(r=>r.cost_bn)));
    const completion=mean(runs.map(r=>r.evaluation.spending.filter(l=>
      l.id.startsWith("union_completion_corporate_")&&l.response!==0).reduce((a,l)=>a+l.effect_bn,0)));
    const coverage=Q.POST_ENGINE.coverage.by_end[end].decomposition.line_parts.filter(l=>
      ["corporate_capital","corporate_labor"].includes(l.line));
    out.by_end[which][end]={completion_corporate_receipts_bn:completion,
      coverage_corporate_cost_by_generation_bn:Object.fromEntries(["G1","G2","G3plus"].map(g=>
        [g,coverage.filter(l=>l.generation===g).reduce((a,l)=>a+l.coverage_bn,0)]))};
    if(models.some(m=>Q.evaluateFull(m,s).evaluation.production?.capital_tax_term_bn))throw Error("capital tax term is nonzero");
  }
}
const expected={set:[365.791930255485,455.981784588979],cash:[281.752563676073,371.942418009567]};
for(const which of ["set","cash"])for(let i=0;i<2;i++)if(Math.abs(out.baseline[which][i]-expected[which][i])>1e-6)throw Error("[BLOCKED] v8 unchanged gate");
const files=["main_case_2026_10_15/package.cjs","main_case_2026_10_15/item_foreign.cjs",
  "main_case_2026_10_15/derived/corrections.json","main_case_2026_10_15/derived/corrections_cash.json",
  "job_capital_taxes_2026_10_14/derived/item.json","job_capital_taxes_2026_10_14/derived/case_keys.json",
  "job_capital_key_refine_2026_10_14/derived/core.json","job_capital_key_refine_2026_10_14/inputs/k1_pins.json",
  "coverage_bound_2026_10_14/derived/coverage_bound_oct15.json","main_case_2026_10_15/derived/union_people.json"];
out.sources=Object.fromEntries(files.map(f=>[f,crypto.createHash("sha256").update(fs.readFileSync(path.join(F,f))).digest("hex")]));
fs.mkdirSync(path.join(HERE,"derived"),{recursive:true});
fs.writeFileSync(path.join(HERE,"derived/v8.json"),JSON.stringify(out,null,2)+"\n");
console.log(JSON.stringify({baseline:out.baseline,population:out.population,gate:"v8 unchanged PASS"}));
