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
function companionPost(X,s,r,rule="central") {
 const mixed=X.POST_ENGINE.mixed_unit_removal?.by_end[s.reading],coverage=X.POST_ENGINE.coverage?.by_end[s.reading];
 const names=["G1","G2","G3plus"],by_generation=Object.fromEntries(names.map(g=>[g,{mixed_unit_removal_bn:mixed?.by_generation_bn[g==="G3plus"?"G3+":g]||0,coverage_bn:coverage?.by_generation[g]||0}]));
 const owner=rule==="first_year"?require("./item_mixed.cjs").sourceRow(X.POST_ENGINE.mixed_unit_removal.which,s.reading,"M5_owner_property").record:null;
 if(rule==="shared")for(const g of names)by_generation[g].mixed_unit_removal_bn=0;
 if(owner)names.forEach((g,i)=>by_generation[g].mixed_unit_removal_bn-=owner.by_generation_bn[i]);
 const line_parts=[];
 if(coverage&&(rule==="first_year"||rule==="school")) {
   if(!coverage.decomposition?.line_parts)throw Error("[BLOCKED] companion coverage needs source line decomposition");
   for(const g of names)by_generation[g].coverage_bn=0;
   const sp=new Map(r.evaluation.spending.map(l=>[l.id,l])),rp=new Map(r.evaluation.receipts.map(l=>[l.id,l]));
   for(const p of coverage.decomposition.line_parts){let value=p.coverage_bn,multiplier=1;
     if(rule==="school") {if(p.category==="schools")multiplier=s.school;}
     else if(p.economic_class==="capital_return")multiplier=0;
     else if(p.line==="mixed_unit_removal") {
       const i=names.indexOf(p.generation),base=mixed.by_generation_bn[p.generation==="G3plus"?"G3+":p.generation];
       if(!Number.isFinite(base)||base===0)throw Error("[BLOCKED] coverage mixed-property generation ratio undefined");
       multiplier=(base-owner.by_generation_bn[i])/base;
     } else if(p.economic_class==="fiscal_line") {
       const row=(p.source_side==="receipt"?rp:sp).get(p.source_line);
       if(!row||!Number.isFinite(p.source_response)||p.source_response<=0)throw Error(`[BLOCKED] coverage source response missing ${p.source_side}:${p.source_line}`);
       multiplier=row.response/p.source_response;
     }
     value*=multiplier;
     if(!Number.isFinite(value)||!by_generation[p.generation])throw Error("[BLOCKED] companion coverage part not routed");
     by_generation[p.generation].coverage_bn+=value;
     line_parts.push({...p,central_coverage_bn:p.coverage_bn,multiplier,coverage_bn:value});
   }
 }
 const mixed_bn=names.reduce((n,g)=>n+by_generation[g].mixed_unit_removal_bn,0),coverage_bn=names.reduce((n,g)=>n+by_generation[g].coverage_bn,0);
 const central_mixed=mixed?.total_bn||0,central_coverage=coverage?.total_bn||0;
 return {mixed_unit_removal_bn:mixed_bn,coverage_bn,delta_bn:mixed_bn+coverage_bn-central_mixed-central_coverage,by_generation,line_parts,
   rule,coverage_rule:rule==="first_year"?"source-line first-year response / central response; public-capital return and property zero; coverage's mixed-property share removed by source generation ratio; production and unclassified residuals held":rule==="school"?"school-category parts at this reading's school response; other personal-price parts held":"central personal coverage prices held",
   item11_rule:rule==="first_year"?"M5_owner_property removed by source generation":rule==="shared"?"stayers' removal consequences excluded from allocation among members":"central"};
}
function adjustedRun(X,m,s,rule) {const r=X.evaluateFull(m,s),post=companionPost(X,s,r,rule);return {...r,cost_bn:r.cost_bn+post.delta_bn,companion_post_engine:post};}
function firstYear(Q,which="set"){
 const X=which==="cash"?Q.CASH:Q,FY=require("../break_conditions_2026_09_29/first_year_item6.cjs"),c=FY.calibration();
 const o={long_run:false,rental:0,capital:false,enterprise_receipt:0,school_rule:"one_year",roads:"resources",property:"none",item6_first_year:true};
 const specs=X.specsFor(o);for(const s of specs)for(const id of ["corporate_capital","corporate_labor","remaining_production_property","other_production_taxes"]){const key=`receipt:${id}`;s.line_responses[key]*=FY.multiplier(id,"fixed_capital",c);}
 const models=Q.METHODS.map(method=>X.modelFor("central",method,X.withCentral(o)));
 const runs=models.map(m=>specs.map(s=>adjustedRun(X,m,s,"first_year"))),costs=runs.map(rs=>rs.map(r=>r.cost_bn)),ends=costs.map(v=>[v.indexOf(Math.min(...v)),v.indexOf(Math.max(...v))]);
 return {band_bn:[0,1].map(e=>costs.reduce((t,v,k)=>t+v[ends[k][e]],0)/costs.length),ends,options:o,item6_rule:"fixed_capital: business property at0; corporate and other production at labor share of long-run response",calibration:c,coverage:"source-line first-year response repricing; capital/property at zero",item11:"without M5_owner_property, by source generation",post_engine_at_ends:ends.map((ix,k)=>ix.map(i=>runs[k][i].companion_post_engine)),completion:"same observed membership; reporter parent-line carriers follow first-year responses and reporter capital/production retain source-endpoint transport [APPROX]; observed children use native cells and production"};
}
function normalShareArm(Q) {
 const source="job_capital_key_refine_2026_10_14/derived/k236.json",K2=Q.readJson(source).K2;
 const normal=.37,national=normal/(1-K2.share_of_federal),fractions=Q.correctionsPayload().meta.foreign_source_tax.fractions;
 const responses=Object.fromEntries(Object.entries(fractions).map(([part,alloc])=>[part,Object.fromEntries(Object.entries(alloc).map(([a,f])=>[a,normal/(1-f)]))]));
 const noForeign=Q.caseOf(Q.OCT05,Q.CANDIDATE.filter(id=>id!=="foreign_source_tax")),results={};
 const corporate=r=>r.evaluation.receipts.filter(l=>["corporate_capital","corporate_labor"].includes(l.id)).reduce((n,l)=>n+l.amount_bn,0)-r.evaluation.spending.filter(l=>l.response!==0&&l.id.startsWith("union_completion_")&&/corporate_(capital|labor)/.test(l.id)).reduce((n,l)=>n+l.amount_bn,0);
 for(const basis of ["set","cash"]){const X=basis==="set"?Q:Q.CASH,Y=basis==="set"?noForeign:noForeign.CASH;
  const s=X.MAIN_SPECS[11],r=X.evaluateFull(X.payloadModel(),s),old=Y.evaluateFull(Y.payloadModel(),Y.MAIN_SPECS[11]);
  let matchedCoverage=0,uniformCoverage=0;
  for(const p of X.POST_ENGINE.coverage?.by_end.high.decomposition.line_parts||[])if(p.source_side==="receipt"&&["corporate_capital","corporate_labor"].includes(p.source_line)){
    const f=fractions[`union_${p.generation}`].personal;
    matchedCoverage+=p.coverage_bn*(1/(1-f)-1);
    uniformCoverage+=p.coverage_bn*(national/normal-1);
  }
  const matchedDelta=-normal*(corporate(old)-corporate(r))+matchedCoverage,uniformDelta=-(national-normal)*corporate(r)+uniformCoverage;
  if(!near(old.cost_bn-r.cost_bn,matchedDelta-matchedCoverage))throw Error("[BLOCKED] normal-share arm does not restore the same source corporate amount");
  const lo=X.evaluateFull(X.payloadModel(),X.MAIN_SPECS[16]).cost_bn;
  results[basis]={central_band_bn:[lo,r.cost_bn],band_bn:[lo,r.cost_bn+matchedDelta],high_change_bn:matchedDelta,
    engine_high_change_bn:matchedDelta-matchedCoverage,coverage_high_change_bn:matchedCoverage,
    uniform_national_share_band_bn:[lo,r.cost_bn+uniformDelta],uniform_national_high_change_bn:uniformDelta,
    uniform_national_engine_high_change_bn:uniformDelta-uniformCoverage,uniform_national_coverage_high_change_bn:uniformCoverage};
 }
 return {beside_only:true,premise:"all foreign-source income is supernormal; domestic normal share = 0.37 / (1 - that source part's foreign fraction)",
   source,foreign_national_federal_share:K2.share_of_federal,uniform_national_normal_share:national,normal_share_by_source_part:responses,results,
   coverage_rule:"corporate source parts use their declared generation's personal foreign fraction; other coverage prices and unclassified calibration held",
   limitation:"normal/supernormal foreign-source split is unmeasured; national federal ratio and source-part ratios answer distinct transport assumptions; these are fixed-end arms, not a new headline end search"};
}
module.exports={ancestry,firstYear,partsAt,companionPost,adjustedRun,normalShareArm};
