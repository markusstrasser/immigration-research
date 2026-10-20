/* Live oct16 first-year probes: canonical companion evaluator, own end search. */
"use strict";
const FY=require("./first_year_item6.cjs");
const IDS=["corporate_capital","corporate_labor","remaining_production_property","other_production_taxes"];
const FIRST={long_run:false,rental:0,capital:false,enterprise_receipt:0,school_rule:"one_year",roads:"resources",property:"none",item6_first_year:true};
const sum=xs=>xs.reduce((a,b)=>a+b,0),near=(a,b)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=1e-9;
const fail=s=>{throw Error("[BLOCKED] first-year v9: "+s);};
// The companion post-engine object carries ~2,600 line rows per end (1.7 MB). Publishing it whole for all
// 32 ends made this file 79 MB (oct15: 85 KB, which stored only by_generation). Keep every scalar and summary
// field; replace each row list by its row count, the signed sum of its value field and the sha256 of its
// canonical JSON, so the rows stay rederivable from the case's companions.cjs and checkable against it.
const ROW_LISTS={line_parts:"coverage_bn",v9_line_parts:"companion_bn"};
function compactPost(post){
 const crypto=require("crypto"),out={};
 for(const [k,v]of Object.entries(post)){
  if(!(k in ROW_LISTS)){out[k]=v;continue;}
  if(!Array.isArray(v))fail(`post-engine ${k} is not a row list`);
  const field=ROW_LISTS[k],values=v.map(r=>r[field]);
  if(!values.every(Number.isFinite))fail(`post-engine ${k}.${field} has a non-finite row`);
  out[k]={rows:v.length,value_field:field,sum_bn:sum(values),sha256:crypto.createHash("sha256").update(JSON.stringify(v)).digest("hex")};
 }
 return out;
}
function evaluate(P,basis,mode,options=FIRST){
 const X=basis==="cash"?P.CASH:P,C=require("../main_case_2026_10_16/companions.cjs"),c=FY.calibration();
 const specs=X.specsFor(options),models=P.METHODS.map(method=>X.modelFor("central",method,X.withCentral(options)));
 for(const s of specs)for(const id of IDS){
  const key=`receipt:${id}`;if(!Number.isFinite(s.line_responses?.[key]))fail("missing response "+key);
  s.line_responses[key]*=FY.multiplier(id,mode,c);
 }
 const runs=models.map(m=>specs.map(s=>C.adjustedRun(X,m,s,"first_year"))),costs=runs.map(rs=>rs.map(r=>r.cost_bn));
 const ends=costs.map(v=>[v.indexOf(Math.min(...v)),v.indexOf(Math.max(...v))]);
 const band=[0,1].map(e=>sum(costs.map((v,k)=>v[ends[k][e]]))/costs.length);
 return {X,specs,models,runs,costs,ends,band};
}
function run(P,MAIN,gate){
 const principal=P.readJson(`${P.LANE}/derived/summary.json`).v9;
 if(!principal?.companions?.first_year)fail("case first-year companion absent");
 const checks=[],variants={},ends={},components=[],post_components=[],c=FY.calibration();
 const check=(label,ok)=>{checks.push({label,pass:!!ok});gate(label,ok);};
 for(const basis of ["set","cash"]){
  const C=require("../main_case_2026_10_16/companions.cjs"),canonical=C.firstYear(P,basis);
  const own=basis==="set"?principal.companions.first_year:principal.companions.first_year.cash;
  check(`${basis}: canonical firstYear matches final case (1e-9)`,canonical.band_bn.every((v,i)=>near(v,own.band_bn[i])));
  const whole=evaluate(P,basis,"whole");
  for(const mode of FY.MODES){
   const r=mode==="whole"?whole:evaluate(P,basis,mode);
   (variants[mode]??={})[basis]=r.band;(ends[mode]??={})[basis]=r.ends;
   if(mode==="fixed_capital")check(`${basis}: independently searched fixed-capital band and ends match firstYear`,
    r.band.every((v,i)=>near(v,canonical.band_bn[i]))&&JSON.stringify(r.ends)===JSON.stringify(canonical.ends));
   for(let k=0;k<r.runs.length;k++)for(let e=0;e<2;e++){
    const i=r.ends[k][e],spec=r.specs[i],at=r.runs[k][i],before=whole.runs[k][i];
    const details=at.v9_post_engine;
    if(!details?.amounts||!Object.hasOwn(details.amounts,"health_residual_key"))fail("selected item21 absent from first-year evaluator");
    check(`${mode}/${basis}/${k}/${e}: item13 off in first year`,near(details.amounts.veterans_compensation,0));
    check(`${mode}/${basis}/${k}/${e}: zero capital`,near(at.capital.total_bn,0)&&near(details.amounts.one_rate,0));
    const fiscal=before.evaluation.welfare_bn-at.evaluation.welfare_bn;
    const delta=at.cost_bn-before.cost_bn;
    const post=delta-fiscal;
    // Independent of the cost difference: the engine part rebuilt from the four receipt lines' attributed
    // amounts times their response change, net of completion carriers on those parents (first_year_v8's rule).
    const fresh=r.X.specsFor(FIRST)[i],m=r.models[k],carriers=r.X.correctionsPayload().meta.union_completion.carriers;
    let rebuilt=0;const receipts={};
    for(const id of IDS){
     const key=`receipt:${id}`,old=whole.specs[i].line_responses[key],now=spec.line_responses[key],base=fresh.line_responses[key];
     check(`${mode}/${basis}/${k}/${e}/${id}: whole and mode responses are the calibrated multipliers (1e-12)`,
      Math.abs(old-base*FY.multiplier(id,"whole",c))<=1e-12&&Math.abs(now-base*FY.multiplier(id,mode,c))<=1e-12);
     const row=before.evaluation.receipts.find(l=>l.id===id);
     if(!row||!Number.isFinite(row.amount_bn))fail("receipt row absent "+id);
     rebuilt+=row.amount_bn*(old-now);
     for(const [carrier,src]of Object.entries(carriers))if(src.side==="receipt"&&src.parent_line===id&&src.parent_key===m.receipts.reference){
      const c2=before.evaluation.spending.find(l=>l.id===carrier);if(c2)rebuilt-=c2.amount_bn*(old-now);
     }
     receipts[id]={amount_bn:row.amount_bn,whole_response:old,mode_response:now};
    }
    check(`${mode}/${basis}/${k}/${e}: engine change rebuilt from receipt amounts and responses (1e-9)`,near(fiscal,rebuilt));
    check(`${mode}/${basis}/${k}/${e}: non-engine change is post-engine, capital and companion terms (1e-9)`,
     near(post,(at.post_engine.total_bn-before.post_engine.total_bn)+(at.capital.total_bn-before.capital.total_bn)
      +(at.companion_post_engine.delta_bn-before.companion_post_engine.delta_bn)));
    check(`${mode}/${basis}/${k}/${e}: owner-property exclusion fixed across response modes (1e-9)`,
     near(before.companion_post_engine.mixed_unit_removal_bn,at.companion_post_engine.mixed_unit_removal_bn));
    components.push({mode,basis,method:P.METHODS[k],end:e?"high":"low",spec:i,allocation:spec.allocation,
     engine_cost_change_from_whole_bn:fiscal,total_cost_change_from_whole_bn:delta,receipts,
     source:"canonical adjustedRun; same specification for both response modes"});
    post_components.push({mode,basis,method:P.METHODS[k],end:e?"high":"low",spec:i,cost_change_from_whole_bn:post,
     item13_bn:details.amounts.veterans_compensation,item21_bn:details.amounts.health_residual_key,
     post_engine:compactPost(at.companion_post_engine)});
    const cp=at.companion_post_engine;
    check(`${mode}/${basis}/${k}/${e}: coverage line parts close to the coverage total (1e-9)`,
     near(sum(cp.line_parts.map(p=>p.coverage_bn)),cp.coverage_bn));
    check(`${mode}/${basis}/${k}/${e}: count-item line parts close to their item totals (1e-9)`,
     ["native_minor_calibration","coverage_tenure"].every(id=>!cp.v9_by_item[id]||near(sum(cp.v9_line_parts.filter(p=>p.item===id).map(p=>p.companion_bn)),cp.v9_by_item[id].companion_bn)));
   }
  }
 }
 const midpoint=sum(MAIN)/2;
 return {case:"oct16",central:MAIN,population_scope:P.POPULATION_V9,calibration:FY.calibration(),
  thresholds:{midpoint_bn:midpoint,low_bn:.75*midpoint,high_bn:1.25*midpoint},variants,ends,components,post_components,checks,
  options:FIRST,first_year_rules:"canonical v9 firstYear/adjustedRun; item13 off, item21 on; zero capital; source-line coverage/count transport; all specification ends re-searched",
  sensitivity_limit:"whole/corporate_only/off hold completion fixed-capital source prices; response-only sensitivities [APPROX]",
  first_year_breaks_alone:sum(variants.fixed_capital.set)/2<.75*midpoint};
}
function band(P,basis,mode,options=FIRST){return evaluate(P,basis,mode,options).band;}
module.exports={run,band,evaluate,FIRST,IDS};
if(require.main===module){
 const fs=require("fs"),path=require("path"),P=require("../main_case_2026_10_16/package.cjs");
 const report=run(P,P.central({}),(label,ok)=>{if(!ok)fail(label);});
 require("../main_case_2026_10_16/memory_guard.cjs").requireWithinBudget("break first-year v9");
 fs.writeFileSync(path.join(__dirname,"derived/first_year_item6_oct16.json"),JSON.stringify(report,null,2)+"\n");
 console.log(`[PASS] first-year v9 ${report.checks.length} checks: ${report.variants.fixed_capital.set.join(" / ")} set; ${report.variants.fixed_capital.cash.join(" / ")} cash`);
}
