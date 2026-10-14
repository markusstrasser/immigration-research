/* v8 first-year response-only probes. Item 9 shares item 6's multiplier;
 * completion carriers follow their parents. Item11 drops owner property; item12
 * follows its source lines' first-year responses. Source endpoint completion prices use the case's fixed-capital
 * option in every sensitivity mode, so mode differences isolate responses. */
"use strict";
const FY = require("./first_year_item6.cjs");
const IDS = ["corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes"];
const FIRST = {long_run:false,rental:0,capital:false,enterprise_receipt:0,school_rule:"one_year",roads:"resources",property:"none",item6_first_year:true};
const near = (a,b) => Math.abs(a-b) <= 1e-9;
const sum = xs => xs.reduce((a,b)=>a+b,0);
const block = s => {throw Error(`[BLOCKED] first-year v8: ${s}`);};
function postAt(X, s, r, options=FIRST) {
 const central=X.POST_ENGINE, mix=central.mixed_unit_removal?.by_end[s.reading], cov=central.coverage?.by_end[s.reading];
 const property=options.property==="none"?require("../main_case_2026_10_15/item_mixed.cjs").sourceRow(central.mixed_unit_removal.which,s.reading,"M5_owner_property").record:null;
 const names=["G1","G2","G3plus"],by_generation=Object.fromEntries(names.map((g,i)=>[g,{
   mixed_unit_removal_bn:(mix?.by_generation_bn[g==="G3plus"?"G3+":g]||0)-(property?.by_generation_bn[i]||0),coverage_bn:0}]));
 const parts=[];
 if(cov) {
  if(!cov.decomposition?.line_parts)block("coverage line decomposition absent");
  for(const p of cov.decomposition.line_parts){let factor=1;
   if(p.economic_class==="capital_return")factor=options.capital===false?0:1;
   else if(p.line==="mixed_unit_removal"&&property){const g=p.generation==="G3plus"?"G3+":p.generation,old=mix.by_generation_bn[g],i=names.indexOf(p.generation);if(!Number.isFinite(old)||!old)block("mixed-property coverage ratio undefined");factor=1-property.by_generation_bn[i]/old;}
   else if(p.economic_class==="fiscal_line"){
    const side=p.source_side==="receipt"?r.evaluation.receipts:r.evaluation.spending,row=side.find(l=>l.id===p.source_line);
    if(!row||!Number.isFinite(p.source_response)||p.source_response<=0)block(`coverage source response missing ${p.source_line}`);
    factor=row.response/p.source_response;
   }
   if(!by_generation[p.generation]||!Number.isFinite(factor*p.coverage_bn))block("unrouted coverage part");
   by_generation[p.generation].coverage_bn+=factor*p.coverage_bn;
   parts.push({...p,central_coverage_bn:p.coverage_bn,multiplier:factor,coverage_bn:factor*p.coverage_bn});
  }
 }
 const mixed_bn=sum(Object.values(by_generation).map(v=>v.mixed_unit_removal_bn)),coverage_bn=sum(Object.values(by_generation).map(v=>v.coverage_bn));
 return {mixed_unit_removal_bn:mixed_bn,coverage_bn,by_generation,line_parts:parts,
   delta_bn:mixed_bn+coverage_bn-(mix?.total_bn||0)-(cov?.total_bn||0)};
}
function costAt(X,m,s,options=FIRST) {const r=X.evaluateFull(m,s),post=postAt(X,s,r,options);return {...r,cost_bn:r.cost_bn+post.delta_bn,companion_post_engine:post};}
function run(P, MAIN, gate) {
 const c=FY.calibration(), variants={}, components=[], checks=[],post_components=[];
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
   const costs=models.map(m=>specs.map(s=>costAt(X,m,s).cost_bn));
   const band=[0,1].map(e=>sum(costs.map(xs=>e?Math.max(...xs):Math.min(...xs)))/costs.length);
   (variants[mode]??={})[basis]=band;
   for(const reading of ["low","high"]){
     const i=ends[reading==="low"?0:1], s=originalSpecs[i], after=specs[i];
    const deltas=[];
    for(const m of models){
     const beforeRun=costAt(X,m,s), afterRun=costAt(X,m,after);
     let delta=0;
     for(const id of IDS){
      const receipt=beforeRun.evaluation.receipts.find(l=>l.id===id);
      const old=s.line_responses[`receipt:${id}`], now=after.line_responses[`receipt:${id}`];
      delta+=receipt.amount_bn*(old-now);
      const carriers=Object.entries(payload.meta.union_completion.carriers).filter(([,src])=>src.side==="receipt"&&src.parent_line===id&&src.parent_key===m.receipts.reference);
      for(const [carrier]of carriers){const row=beforeRun.evaluation.spending.find(l=>l.id===carrier);if(row)delta+=-row.amount_bn*(old-now);}
     }
     const postDelta=afterRun.companion_post_engine.delta_bn-beforeRun.companion_post_engine.delta_bn;
     check(`${mode}/${basis}/${reading} engine plus repriced coverage response closure`,near(afterRun.cost_bn-beforeRun.cost_bn,delta+postDelta));
     check(`${mode}/${basis}/${reading} owner-property exclusion fixed across response modes`,near(beforeRun.companion_post_engine.mixed_unit_removal_bn,afterRun.companion_post_engine.mixed_unit_removal_bn));
     deltas.push(delta);
    }
    const pm=models[0], ev=X.evaluateFull(pm,s).evaluation;
    const beforePost=postAt(X,s,X.evaluateFull(pm,s)),afterPost=postAt(X,after,X.evaluateFull(pm,after));
    post_components.push({mode,basis,end:`${reading}_end_${i}`,cost_change_from_whole_bn:afterPost.coverage_bn-beforePost.coverage_bn,by_generation:afterPost.by_generation});
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
  thresholds:{midpoint_bn:midpoint,low_bn:0.75*midpoint,high_bn:1.25*midpoint},variants,components,post_components,checks,
  options:FIRST,first_year_rules:"item9 with item6; item10 parent responses and fixed-capital source endpoint prices; item11 without M5_owner_property by generation; item12 source-line responses, capital/property zero, production and unclassified residuals held",
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
 return P.mean2(...P.METHODS.map(method=>{const m=X.modelFor("central",method,X.withCentral(options)),values=specs.map(s=>costAt(X,m,s,options).cost_bn);return [Math.min(...values),Math.max(...values)];}));
}
module.exports={run,band,FIRST,IDS,postAt,costAt};
if(require.main===module) {
 const fs=require("fs"),path=require("path"),P=require("../main_case_2026_10_15/package.cjs");
 const principal=P.readJson(`${P.LANE}/derived/summary.json`).v8,main=P.central({});
 if(!main.every((n,i)=>near(n,principal.band_bn[i])))block("saved whole case is stale");
 const report=run(P,main,(label,ok)=>{if(!ok)block(label);});
 const destination=path.join(__dirname,"derived/first_year_item6_oct15.json"),temporary=destination+".tmp";
 fs.writeFileSync(temporary,JSON.stringify(report,null,2)+"\n");fs.renameSync(temporary,destination);
 console.log(`first-year v8 PASS ${report.checks.length} checks; set ${report.variants.fixed_capital.set.join(" / ")}; cash ${report.variants.fixed_capital.cash.join(" / ")}; maxRSS ${process.resourceUsage().maxRSS} KiB`);
}
