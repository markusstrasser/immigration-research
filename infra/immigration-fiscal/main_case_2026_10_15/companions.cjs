/* Companion calculations on the complete v8 account. */
"use strict";
const fs=require("fs"),path=require("path"),AS=require("../main_case_2026_10_14/ancestry_share.cjs");
const G=["G1","G2","G3plus","added"];
const near=(a,b)=>Math.abs(a-b)<1e-8;
function partsAt(Q,which,s,r){const X=which==="cash"?Q.CASH:Q,pl=X.correctionsPayload(),parts=Object.fromEntries(G.map(g=>[g,0]));
 for(const rec of X.V8_ITEMS){for(const [name,p] of Object.entries(rec.parts||{})){const e=pl.edits[rec.edits.first+p.edit];if(e.national_bn!==undefined)throw Error("[BLOCKED] ancestry national-scale rule missing");
   const row=(e.side==="receipt"?r.evaluation.receipts:r.evaluation.spending).find(l=>l.id===e.line);
   if(!row)throw Error(`[BLOCKED] ancestry part line missing ${e.line}`);
   const active=e.side==="receipt"?e.scenario===Q.MODEL.receipts.reference:e.key===row.key;
   if(!active)continue;
   const gen=name.startsWith("lineage_")?"added":name.match(/^union_(G1|G2|G3plus):/)?.[1];
   if(!gen)throw Error(`[BLOCKED] ancestry part rule missing ${name}`);
   parts[gen]+=(e.side==="receipt"?-1:1)*p.by[s.allocation]*row.response;
 }}
 const m=pl.meta.mixed_unit_removal?.by_end[s.reading];if(m)for(const g of G.slice(0,3))parts[g]+=m.by_generation_bn[g==="G3plus"?"G3+":g];
 const c=pl.meta.coverage?.by_end[s.reading];if(c)for(const g of G.slice(0,3))parts[g]+=c.by_generation[g];
 return parts;
}
function ancestry(Q,which="set"){
 const X=which==="cash"?Q.CASH:Q,B=Q.OCT14, BX=which==="cash"?B.CASH:B;
 const old=AS.rowsFor(B,which,{Engine:Q.Engine}),m=X.payloadModel(),bm=BX.payloadModel();
 const changes=X.MAIN_SPECS.map(s=>{const r=X.evaluateFull(m,s),b=BX.evaluateFull(bm,BX.MAIN_SPECS[X.MAIN_SPECS.indexOf(s)]),ps=partsAt(Q,which,s,r);const d=r.cost_bn-b.cost_bn;
   // Native child cells also change public-capital keys and carry their own
   // production grid. These are the observed nonreporters, in the added block.
   ps.added+=(r.capital.total_bn-b.capital.total_bn)-(r.evaluation.production_gain_bn-b.evaluation.production_gain_bn);
   if(!near(Object.values(ps).reduce((a,b)=>a+b,0),d))throw Error(`[BLOCKED] ancestry new generation parts fail closure ${Object.values(ps).reduce((a,b)=>a+b,0)} vs ${d}`);
   return ps;});
 const completion=X.correctionsPayload().meta.union_completion,coverage=X.POST_ENGINE.coverage;
 return old.rows.map(row=>{const shares={G1:1,G2:row.s_g2,G3plus:row.s_g3plus,added:row.s_added};
  const costs=row.costs.map((n,i)=>n+G.reduce((t,g)=>t+shares[g]*changes[i][g],0)),ends=[costs.indexOf(Math.min(...costs)),costs.indexOf(Math.max(...costs))];
  const population=row.fractional_population+completion.counts.reporters*shares.G3plus+completion.counts.nonreporters*shares.added+(coverage?Object.entries(coverage.counts_by_generation).reduce((t,[g,n])=>t+(shares[g]??shares.added)*n,0):0);
  const parts=Object.fromEntries(G.map(g=>[g,ends.map(i=>(g==="added"?old.added_costs[i]:old.generation_costs[g][i])+changes[i][g])]));
  if(!ends.every((i,e)=>near(G.reduce((n,g)=>n+shares[g]*parts[g][e],0),costs[i])))throw Error("[BLOCKED] ancestry current end-parts do not close");
  const whole=old.case_costs.map((n,i)=>n+G.reduce((t,g)=>t+changes[i][g],0));
  return {...row,band_bn:ends.map(i=>costs[i]),ends,costs,fractional_population:population,per_member_usd:ends.map(i=>costs[i]*1e9/population),whole_person_band_bn:[Math.min(...whole),Math.max(...whole)],parts_at_ends_bn:parts,coverage:"central coverage generation dollars and counts carried, weighted by ancestry shares",completion_rule:"reporters at G3plus ancestry share; observed nonreporters at added-person ancestry share",parts_delta_at_ends_bn:Object.fromEntries(G.map(g=>[g,ends.map(i=>changes[i][g])]))};
 });
}
function firstYear(Q,which="set"){
 const X=which==="cash"?Q.CASH:Q,FY=require("../break_conditions_2026_09_29/first_year_item6.cjs"),c=FY.calibration();
 const o={long_run:false,rental:0,capital:false,enterprise_receipt:0,school_rule:"one_year",roads:"resources",property:"none",item6_first_year:true};
 const specs=X.specsFor(o);for(const s of specs)for(const id of ["corporate_capital","corporate_labor","remaining_production_property","other_production_taxes"]){const key=`receipt:${id}`;s.line_responses[key]*=FY.multiplier(id,"fixed_capital",c);}
 const models=Q.METHODS.map(method=>X.modelFor("central",method,X.withCentral(o)));
 const costs=models.map(m=>specs.map(s=>X.cost(m,s))),ends=costs.map(v=>[v.indexOf(Math.min(...v)),v.indexOf(Math.max(...v))]);
 return {band_bn:[0,1].map(e=>costs.reduce((t,v,k)=>t+v[ends[k][e]],0)/costs.length),ends,options:o,item6_rule:"fixed_capital: business property at0; corporate and other production at labor share of long-run response",calibration:c,coverage:"carried from central prices",item11:"carried as brief directs; only D changes across lineage options",completion:"same observed membership; reporter parent-line carriers follow first-year responses and reporter capital/production retain source-endpoint transport [APPROX]; observed children use native cells and production"};
}
module.exports={ancestry,firstYear,partsAt};
