/* v9 companions: source-owned post parts, with transported coverage prices explicit. */
"use strict";
const fs=require("fs"),path=require("path"),OLD=require("../main_case_2026_10_15/companions.cjs");
const G=["G1","G2","G3plus","added"],sum=a=>a.reduce((x,y)=>x+y,0),near=(a,b)=>Math.abs(a-b)<1e-8;
const ROOT=path.join(__dirname,"..");
const fail=s=>{throw Error("[BLOCKED] v9 companion: "+s);};
const cache=new Map();
const modelCache=new WeakMap();
function descendantModels(X){
 if(modelCache.has(X))return modelCache.get(X);
 const B=X.OCT15,pl=JSON.parse(JSON.stringify(B.correctionsPayload())),range=pl.meta.lineage.edits;
 // Keep row8's response-calibration residual on the reporting union, exactly
 // as the established ancestry decomposition does. Remove only descendants.
 for(let i=range.first;i<range.first+range.count;i++)if(i!==range.row8_edit_index)pl.edits[i].by={personal:0,shared:0};
 for(const rec of pl.meta.items||[])for(const [name,p]of Object.entries(rec.parts||{}))if(name.startsWith("lineage_")&&!name.includes(":observed_nonreporters:")){
  const e=pl.edits[rec.edits.first+p.edit];for(const a of ["personal","shared"])e.by[a]-=p.by[a];
 }
 const old=B.payloadModel(),strippedOld=X.Engine.applyCorrections(X.MODEL,pl);
 let strippedNew=strippedOld;
 for(const {x}of X.V9_BUILT)strippedNew=X.Engine.applyCorrections(strippedNew,{edits:x.editsAt?x.editsAt(strippedNew,{}):x.edits,meta:strippedNew.corrections});
 const out={old,strippedOld,current:X.payloadModel(),strippedNew};modelCache.set(X,out);return out;
}
function deltaParts(Q,which,s,r){
 const X=which==="cash"?Q.CASH:Q,split=require("../generation_account_2026_09_24/v9_split.cjs").generationParts(X,s,"a");
 const out=Object.fromEntries(G.slice(0,3).map(g=>[g,split.costs[g]-split.old_costs[g]]));out.added=0;
 const dm=descendantModels(X),a=X.postFor(dm.current,s),b=X.postFor(dm.strippedNew,s);
 let added=0;for(const id of ["veterans_compensation","income_security_administration","public_college_response","one_rate"])added+=(a.amounts[id]||0)-(b.amounts[id]||0);
 // Item21 is additive, with declared population parts, so removing model edits
 // cannot isolate its descendants. Use its own delivered population declaration.
 added+=sum((a.parts.health_residual_key||[]).filter(p=>p.population==="added_lineage").map(p=>p.delta_bn));
 // The receipt edits also apply to native added-person cells. The matched
 // double difference isolates their actual source amount, without a headcount split.
 const E=X.OCT15.evaluateFull;
 added+=(E(dm.current,s).cost_bn-E(dm.old,s).cost_bn)-(E(dm.strippedNew,s).cost_bn-E(dm.strippedOld,s).cost_bn);
 added+=X.POST_ENGINE.passthrough_source_tax?.by_end[s.reading].by_generation_bn.added_G3plus||0;
 out.G3plus-=added;out.added=added;
 if(!near(sum(Object.values(out)),r.cost_bn-X.OCT15.evaluateFull(dm.old,s).cost_bn))fail("ancestry generation delta closure");
 return out;
}
function csv(file){if(cache.has(file))return cache.get(file);const rows=fs.readFileSync(path.join(ROOT,file),"utf8").trimEnd().split("\n").map(x=>x.split(",")),h=rows.shift(),out=rows.map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]])));cache.set(file,out);return out;}
function countParts(block,end){
 if(!block?.parts_file)return [];
 const source=csv(block.parts_file),out=[];
 for(const [scenario,sign]of [[block.parts_scenario,1],[block.subtract_parts_scenario,-1]])if(scenario)
  for(const p of source)if(p.scenario===scenario&&p.end===end)out.push({...p,value_bn:sign*Number(p.change_bn),item13_first_year_addback_bn:sign*Number(p.item13_first_year_addback_bn||0)});
 if(!near(sum(out.map(p=>p.value_bn)),block.by_end[end].total_bn))fail(`count parts do not close ${block.parts_scenario}/${end}`);
 return out;
}
function responseAt(r,p){const row=(p.source_side==="receipt"?r.evaluation.receipts:r.evaluation.spending).find(q=>q.id===p.source_line);if(!row)fail(`source response absent ${p.source_side}/${p.source_line}`);return row.response;}
function multiplier(X,s,r,p,rule,central){
 if(rule==="school")return p.category==="schools"?s.school:1;
 if(rule!=="first_year")return 1;
 if(p.economic_class==="capital_return")return 0;
 if(p.source_line==="mixed_unit_removal"){
  const mix=X.POST_ENGINE.mixed_unit_removal.by_end[s.reading],owner=require("../main_case_2026_10_15/item_mixed.cjs").sourceRow(X.POST_ENGINE.mixed_unit_removal.which,s.reading,"M5_owner_property").record;
  const i=["G1","G2","G3plus"].indexOf(p.generation),base=mix.by_generation_bn[p.generation==="G3plus"?"G3+":p.generation];
  if(!Number.isFinite(base)||base===0)fail("mixed-property ratio undefined");return (base-owner.by_generation_bn[i])/base;
 }
 if(p.economic_class!=="fiscal_line")return 1;
 const before=responseAt(central,p),after=responseAt(r,p);
 if(before===0){if(after===0)return 1;fail(`zero source response ${p.source_line}`);}return after/before;
}
function companionPost(X,s,r,rule="central"){
 const old=OLD.companionPost(X,s,r,rule),parts=[],by_item={};
 const central=X.OCT15.evaluateFull(X.OCT15.payloadModel(),X.OCT15.MAIN_SPECS[s.reading==="low"?16:11]);
 let extra=0;
 if(rule==="first_year"){
  let addback=0;
  for(const [i,p] of X.POST_ENGINE.coverage.by_end[s.reading].decomposition.line_parts.entries()){
   if(!p.item13_first_year_addback_bn)continue;
   if(p.source_side!=="spending")fail("military addback has a non-spending source");
   const v=(p.item13_first_year_addback_bn||0)*(p.source_response?responseAt(r,p)/p.source_response:1);
   if(v){addback+=v;old.by_generation[p.generation].coverage_bn+=v;old.line_parts[i].coverage_bn+=v;old.line_parts[i].item13_restored_bn=v;}
  }
  old.coverage_bn+=addback;extra+=addback;
  if(!near(sum(old.line_parts.map(p=>p.coverage_bn)),old.coverage_bn))fail("first-year restored coverage parts do not close");
  by_item.item13_coverage_first_year={addback_bn:addback,rule:"restore each signed military coverage piece before first-year source-response transport"};
 }
 for(const id of ["native_minor_calibration","coverage_tenure"]){
  const b=X.POST_ENGINE[id];if(!b)continue;
  let total=0;for(const p of countParts(b,s.reading)){const scale=multiplier(X,s,r,p,rule,central),restore=rule==="first_year"?p.item13_first_year_addback_bn:0,v=(p.value_bn+restore)*scale;total+=v;parts.push({...p,item:id,multiplier:scale,companion_bn:v});}
  by_item[id]={central_bn:b.by_end[s.reading].total_bn,companion_bn:total,rule:"source-line response transport; capital zero in first year; unclassified residuals held"};extra+=total-b.by_end[s.reading].total_bn;
 }
 const b=X.POST_ENGINE.passthrough_source_tax;
 if(b){const before=b.by_end[s.reading].total_bn,FY=require("../break_conditions_2026_09_29/first_year_item6.cjs"),scale=rule==="first_year"&&process.env.V9_FIRST_YEAR_PASS!=="held"?FY.multiplier("corporate_capital","fixed_capital",FY.calibration()):1;
  by_item.passthrough_source_tax={central_bn:before,companion_bn:before*scale,multiplier:scale,rule:rule==="first_year"?"conditional item6 fixed-capital labor-share response; V9_FIRST_YEAR_PASS=held selects unchanged source-tax response":"adopted source-tax amounts held"};extra+=before*(scale-1);
 }
 return {...old,delta_bn:old.delta_bn+extra,v9_by_item:by_item,v9_line_parts:parts,
  coverage_rule:old.coverage_rule+"; count-item source prices transported by the same rules; "+(b?"selected beside source-tax coverage increment withheld":"item19/W09 absent centrally")};
}
function adjustedRun(X,m,s,rule){const r=X.evaluateFull(m,s),post=companionPost(X,s,r,rule);return {...r,cost_bn:r.cost_bn+post.delta_bn,companion_post_engine:post};}
function firstYear(Q,which="set"){
 const X=which==="cash"?Q.CASH:Q,FY=require("../break_conditions_2026_09_29/first_year_item6.cjs"),c=FY.calibration();
 const o={long_run:false,rental:0,capital:false,enterprise_receipt:0,school_rule:"one_year",roads:"resources",property:"none",item6_first_year:true};
 const specs=X.specsFor(o);for(const s of specs)for(const id of ["corporate_capital","corporate_labor","remaining_production_property","other_production_taxes"])s.line_responses[`receipt:${id}`]*=FY.multiplier(id,"fixed_capital",c);
 const models=Q.METHODS.map(method=>X.modelFor("central",method,X.withCentral(o))),runs=models.map(m=>specs.map(s=>adjustedRun(X,m,s,"first_year"))),costs=runs.map(rs=>rs.map(r=>r.cost_bn)),ends=costs.map(v=>[v.indexOf(Math.min(...v)),v.indexOf(Math.max(...v))]);
 const military_restoration_at_ends=ends.map((ix,k)=>ix.map(i=>{
  const r=runs[k][i],post=r.companion_post_engine;
  const direct_bn=sum(r.v9_post_engine.parts.veterans_compensation.filter(p=>p.population!=="coverage").map(p=>p.first_year_restored_bn));
  const coverage_bn=post.v9_by_item.item13_coverage_first_year.addback_bn;
  const count_bn=sum(post.v9_line_parts.map(p=>p.item13_first_year_addback_bn*p.multiplier));
  return {direct_bn,coverage_bn,count_bn,total_bn:direct_bn+coverage_bn+count_bn};
 }));
 return {band_bn:[0,1].map(e=>sum(costs.map((v,k)=>v[ends[k][e]]))/costs.length),ends,options:o,
  item13_rule:"first year: no replacement veterans; all six service-earned subblocks at evaluated response1; own signed coverage/count addbacks",
  military_restoration_at_ends,
  item6_rule:"fixed_capital: business property at0; corporate and other production at labor share of long-run response",calibration:c,
  coverage:"computed from central source-line prices at first-year response ratios; military pre-item13 prices restored; capital/property zero; unclassified residuals held",
  item11:"without M5_owner_property by source generation",post_engine_at_ends:ends.map((ix,k)=>ix.map(i=>runs[k][i].companion_post_engine)),
  completion:"observed membership fixed; reporter parent-line carriers follow first-year responses; source endpoint capital/production transport retained; children use native cells",
  item19_rule:X.POST_ENGINE.passthrough_source_tax?"selected beside: conditional first-year labor-share scaling, switch V9_FIRST_YEAR_PASS=held":"absent centrally; item19 and W09 beside only",
  item20_rule:"capital absent in this reading; Trustees pension path unchanged",item21_rule:"non-military residual allocation applies at first-year line responses"};
}
function coverageLabel(Q,{rule=null}={}){
 const p=Q.correctionsPayload(),construction=p.meta.coverage?.construction||"none",lineage=p.meta.lineage?.count_option?.name||Q.LINEAGE_OPTION||"central";
 return {
  coverage:rule==="first_year"?"central oct16 item12 source prices transported by first-year line responses; no new missing-person measurement":rule==="school"?"central oct16 item12 school parts transported to this school response; remaining parts carried":
   `oct16 item12 ${construction} construction at its own source-kernel prices; those prices are carried at lineage/shared variants (${lineage})`,
  count_items_16_17:"own oct16 central count/tenure kernel carried at lineage options and DA constructions; own lineage-specific or DA-specific16/17 recalibration is not claimed",
  item15_coverage:Q.ITEM_ARMS?.public_college_response?"alternative item15 engine/reporter response rebuilt; coverage and count-item college response prices remain the central item15 kernel":"central item15 response in the own oct16 coverage/count kernel",
 };
}
function partsAt(Q,which,s,r){
 const X=which==="cash"?Q.CASH:Q,B=X.OCT15,br=B.evaluateFull(B.payloadModel(),B.MAIN_SPECS[X.MAIN_SPECS.indexOf(s)]||B.MAIN_SPECS[s.reading==="low"?16:11]);
 const old=OLD.partsAt(Q.V8_PACKAGE,which,s,br);
 const next=deltaParts(Q,which,s,r);
 for(const g of G)old[g]+=next[g]||0;
 return old;
}
function ancestry(Q,which="set"){
 const X=which==="cash"?Q.CASH:Q,B=X.OCT15,base=OLD.ancestry(Q.V8_PACKAGE,which),model=X.payloadModel(),bm=B.payloadModel();
 const old7=Q.V8_PACKAGE.OCT14,old7X=which==="cash"?old7.CASH:old7,old7m=old7X.payloadModel();
 const basis=require("../main_case_2026_10_14/ancestry_share.cjs").rowsFor(old7,which,{Engine:Q.Engine}),fullParts=[];
 const delta=X.MAIN_SPECS.map((s,i)=>{const r=X.evaluateFull(model,s),old=B.evaluateFull(bm,B.MAIN_SPECS[i]),p=deltaParts(Q,which,s,r);if(!near(sum(G.map(g=>p[g]||0)),r.cost_bn-old.cost_bn))fail("ancestry incremental generation parts fail closure");
  const seven=old7X.evaluateFull(old7m,old7X.MAIN_SPECS[i]),eight=OLD.partsAt(Q.V8_PACKAGE,which,s,old);
  eight.added+=(old.capital.total_bn-seven.capital.total_bn)-(old.evaluation.production_gain_bn-seven.evaluation.production_gain_bn);
  fullParts.push(Object.fromEntries(G.map(g=>[g,(g==="added"?basis.added_costs[i]:basis.generation_costs[g][i])+eight[g]+p[g]])));
  return p;});
 const meta=X.POST_ENGINE,popChange={G1:0,G2:0,G3plus:0,added:0};
 for(const id of ["native_minor_calibration","coverage_tenure"]){const b=meta[id];if(!b)continue;for(const g of G.slice(0,3))popChange[g]+=(b.observed_people_change_by_generation?.[g]||0)+(b.coverage_people_change_by_generation?.[g]||0);}
 return base.map(row=>{
  const shares={G1:1,G2:row.s_g2,G3plus:row.s_g3plus,added:row.s_added},costs=row.costs.map((x,i)=>x+sum(G.map(g=>shares[g]*(delta[i][g]||0)))),ends=[costs.indexOf(Math.min(...costs)),costs.indexOf(Math.max(...costs))];
  const population=row.fractional_population+sum(G.map(g=>shares[g]*popChange[g]));
  const weighted11All=X.MAIN_SPECS.map(s=>sum(G.slice(0,3).map(g=>shares[g]*(meta.mixed_unit_removal?.by_end[s.reading].by_generation_bn[g==="G3plus"?"G3+":g]||0)))),weighted11=ends.map(i=>weighted11All[i]);
  const without11=costs.map((v,i)=>v-weighted11All[i]),withoutEnds=[without11.indexOf(Math.min(...without11)),without11.indexOf(Math.max(...without11))];
  const parts=Object.fromEntries(G.map(g=>[g,ends.map(i=>fullParts[i][g])]));
  if(!ends.every((i,k)=>near(sum(G.map(g=>shares[g]*parts[g][k])),costs[i])))fail("ancestry updated endpoint parts do not close");
  return {...row,costs,ends,band_bn:ends.map(i=>costs[i]),parts_at_ends_bn:parts,
   parts_delta_at_ends_bn:Object.fromEntries(G.map(g=>[g,ends.map(i=>fullParts[i][g]-(g==="added"?basis.added_costs[i]:basis.generation_costs[g][i]))])),
   v9_parts_delta_at_ends_bn:Object.fromEntries(G.map(g=>[g,ends.map(i=>delta[i][g])])),
   fractional_population:population,per_member_usd:ends.map(i=>costs[i]*1e9/population),whole_person_band_bn:X.central({}),coverage:"central v9 coverage dollars and counts carried, generation weighted; own ancestry coverage is not remeasured",item11_rule:"generation-weighted convention: G1 at1, G2/G3+ at this ancestry row's shares",item11_weighted_at_ends_bn:weighted11,without_only_weighted_item11_band_bn:withoutEnds.map(i=>without11[i]),without_only_weighted_item11_ends:withoutEnds,without_only_weighted_item11_fixed_end_bn:ends.map((i,k)=>costs[i]-weighted11[k]),v9_delta_at_ends_bn:ends.map(i=>sum(G.map(g=>shares[g]*(delta[i][g]||0))))};
 });
}
module.exports={ancestry,firstYear,partsAt,companionPost,adjustedRun,normalShareArm:OLD.normalShareArm,countParts,deltaParts,coverageLabel};
