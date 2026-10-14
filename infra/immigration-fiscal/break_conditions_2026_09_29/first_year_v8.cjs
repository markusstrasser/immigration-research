/* v8 first-year response-only probes. Item 9 shares item 6's multiplier;
 * completion carriers follow their parents, while mixed-unit and coverage dollars
 * remain in full. Source endpoint completion prices use the case's fixed-capital
 * option in every sensitivity mode, so mode differences isolate responses. */
"use strict";
const FY = require("./first_year_item6.cjs");
const IDS = ["corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes"];
const FIRST = {long_run:false,rental:0,capital:false,enterprise_receipt:0,school_rule:"one_year",roads:"resources",property:"none",item6_first_year:true};
const near = (a,b) => Math.abs(a-b) <= 1e-9;
const sum = xs => xs.reduce((a,b)=>a+b,0);
const block = s => {throw Error(`[BLOCKED] first-year v8: ${s}`);};
function run(P, MAIN, gate) {
 const c=FY.calibration(), variants={}, components=[], checks=[];
 const check=(label,ok)=>{checks.push({label,pass:ok});gate(label,ok);};
 const principal=P.readJson(`${P.LANE}/derived/summary.json`).v8;
 const ends=principal.end_specifications.set[0];
 if(!Array.isArray(ends)||ends.length!==2||!ends.every(Number.isInteger)
    ||["set","cash"].some(b=>principal.end_specifications[b].some(xs=>JSON.stringify(xs)!==JSON.stringify(ends))))
   block("set/cash methods must declare the same pair of personal ends");
 const scope = (name) => name.startsWith("union_") ? "union" : name.startsWith("lineage_") ? "added" : block(`unrouted part ${name}`);
 for(const basis of ["set","cash"]){
  const X=basis==="set"?P:P.CASH, payload=X.correctionsPayload();
  const models=P.METHODS.map(method=>X.modelFor("central",method,X.withCentral(FIRST)));
  const originalSpecs=X.specsFor(FIRST);
  if(!IDS.every(id=>Number.isFinite(originalSpecs[0].line_responses[`receipt:${id}`])))block("four receipt responses missing");
  for(const mode of FY.MODES){
   const specs=X.specsFor(FIRST);
   for(const s of specs)for(const id of IDS)s.line_responses[`receipt:${id}`]*=FY.multiplier(id,mode,c);
   const costs=models.map(m=>specs.map(s=>X.evaluateFull(m,s).cost_bn));
   const band=[0,1].map(e=>sum(costs.map(xs=>e?Math.max(...xs):Math.min(...xs)))/costs.length);
   (variants[mode]??={})[basis]=band;
   for(const reading of ["low","high"]){
     const i=ends[reading==="low"?0:1], s=originalSpecs[i], after=specs[i];
    const deltas=[];
    for(const m of models){
     const beforeRun=X.evaluateFull(m,s), afterRun=X.evaluateFull(m,after);
     let delta=0;
     for(const id of IDS){
      const receipt=beforeRun.evaluation.receipts.find(l=>l.id===id);
      const old=s.line_responses[`receipt:${id}`], now=after.line_responses[`receipt:${id}`];
      delta+=receipt.amount_bn*(old-now);
      const carriers=Object.entries(payload.meta.union_completion.carriers).filter(([,src])=>src.side==="receipt"&&src.parent_line===id&&src.parent_key===m.receipts.reference);
      for(const [carrier]of carriers){const row=beforeRun.evaluation.spending.find(l=>l.id===carrier);if(row)delta+=-row.amount_bn*(old-now);}
     }
     check(`${mode}/${basis}/${reading} engine response closure`,near(afterRun.cost_bn-beforeRun.cost_bn,delta));
     check(`${mode}/${basis}/${reading} post-engine items unchanged`,JSON.stringify(beforeRun.post_engine)===JSON.stringify(afterRun.post_engine));
     deltas.push(delta);
    }
    const pm=models[0], ev=X.evaluateFull(pm,s).evaluation;
    for(const id of IDS){
     const receipt=ev.receipts.find(l=>l.id===id), old=s.line_responses[`receipt:${id}`], now=after.line_responses[`receipt:${id}`];
     const detail=P.ITEM_DETAIL.job_capital_taxes[basis].new_parts[`${id}|${pm.receipts.reference}`];
     const amounts={union:0,added:0};
     for(const [name,part]of Object.entries(detail))amounts[scope(name)]+=part.personal;
     const foreign=payload.meta.items.find(r=>r.id==="foreign_source_tax");
     for(const [name,part]of Object.entries(foreign.parts)){const edit=payload.edits[foreign.edits.first+part.edit];if(edit.line===id&&edit.scenario===pm.receipts.reference)amounts[scope(name)]+=part.by.personal;}
     const completion=payload.meta.items.find(r=>r.id==="union_completion");
     for(const [name,part]of Object.entries(completion.parts)){const edit=payload.edits[completion.edits.first+part.edit];if(edit.side==="receipt"&&edit.line===id&&edit.scenario===pm.receipts.reference)amounts[scope(name)]+=part.by.personal;}
     check(`${mode}/${basis}/${reading}/${id} receipt parts close`,near(sum(Object.values(amounts)),receipt.amount_bn));
     for(const [carrier,src]of Object.entries(payload.meta.union_completion.carriers))if(src.side==="receipt"&&src.parent_line===id&&src.parent_key===pm.receipts.reference){const row=ev.spending.find(l=>l.id===carrier);if(row)amounts.union-=row.amount_bn;}
     amounts.lineage=amounts.union+amounts.added;
      for(const [sc,amount]of Object.entries(amounts))components.push({mode,basis,end:`${reading}_end_${i}`,line:id,scope:sc,amount_bn:amount,long_run_response:old,first_year_response:now,cost_change_from_whole_bn:amount*(old-now)});
    }
   }
  }
 }
 const midpoint=sum(MAIN)/2, report={calibration:c,central:MAIN,population_scope:P.POPULATION_V8,
  thresholds:{midpoint_bn:midpoint,low_bn:0.75*midpoint,high_bn:1.25*midpoint},variants,components,checks,
  options:FIRST,first_year_rules:"item9 with item6; item10 present in full with parent responses and fixed-capital source endpoint prices; items11/12 full post-engine",
  sensitivity_limit:"whole/corporate_only/off hold completion's fixed-capital endpoint prices; response-only sensitivities [APPROX]"};
 report.first_year_breaks_alone=sum(variants.fixed_capital.set)/2<report.thresholds.low_bn;
  const own=principal.companions?.first_year;
 if(!own?.band_bn||!own?.cash?.band_bn)block("case first-year companions absent; wait for the complete case run");
 check("first-year set/cash match case companion (1e-9)",["set","cash"].every(b=>variants.fixed_capital[b].every((x,i)=>near(x,b==="set"?own.band_bn[i]:own.cash.band_bn[i]))));
 return report;
}
function band(P,basis,mode,options){
 const X=basis==="cash"?P.CASH:P,c=FY.calibration(),specs=X.specsFor(options);
 for(const s of specs)for(const id of IDS)s.line_responses[`receipt:${id}`]*=FY.multiplier(id,mode,c);
 return P.mean2(...P.METHODS.map(method=>X.bandFor(X.modelFor("central",method,X.withCentral(options)),null,specs)));
}
module.exports={run,band,FIRST,IDS};
