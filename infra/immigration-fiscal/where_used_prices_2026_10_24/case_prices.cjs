/* Read-only oct16 repricing sensitivities. Every scenario calls evaluateFull.
 * New correction-constant entries carry only scoped, already-responded price
 * changes. Existing fees, receipts, capital keys and every post remain intact.
 */
"use strict";
const fs=require("fs"), path=require("path"), crypto=require("crypto");
const HERE=__dirname,FISCAL=path.join(HERE,".."),REPO=path.resolve(FISCAL,"../..");
const P=require(path.join(FISCAL,"main_case_2026_10_16/package.cjs"));
const C=require(path.join(FISCAL,"main_case_2026_10_16/companions.cjs"));
const read=rel=>JSON.parse(fs.readFileSync(path.join(FISCAL,rel),"utf8"));
const csv=file=>{const rows=fs.readFileSync(file,"utf8").trimEnd().split("\n").map(r=>r.split(","));return rows.slice(1).map(r=>Object.fromEntries(rows[0].map((h,i)=>[h,r[i]])));};
const sum=a=>a.reduce((x,y)=>x+y,0),near=(a,b,t=1e-9)=>Math.abs(a-b)<t;
const gates=[];
const gate=(name,ok,detail)=>{gates.push({name,pass:!!ok,detail:String(detail)});if(!ok)throw Error("[BLOCKED] "+name+": "+detail);};
const summary=read("main_case_2026_10_16/derived/summary.json").v9;
const live=read("live_case.json");
gate("adopted oct16",P.CASE_KEY==="oct16"&&P.STATUS==="adopted"&&JSON.stringify(live).includes("oct16"),P.CASE_KEY+" "+P.STATUS);
const fee=read("user_fee_allocation_2026_10_07/derived/fee_lines.json");
const item15=read("spending_keys_r5_2026_10_15/derived/item15.json");
const college=read("where_used_prices_2026_10_24/derived/colleges.json");
const parks=read("where_used_prices_2026_10_24/derived/parks.json");
const factors=csv(path.join(HERE,"derived/college_factors.csv"));
const coverage=csv(path.join(HERE,"derived/college_finance_coverage.csv"));
const factor=(concept,scheme="case_fall",grad=2)=>{
 const rows=factors.filter(r=>r.concept===concept&&r.scheme===scheme&&+r.graduate_weight===grad);
 gate(`unique college factor ${concept}/${scheme}/${grad}`,rows.length===1,rows.length);
 gate(`valid college factor ${concept}/${scheme}/${grad}`,rows[0].status==="conditional_allocation_proxy"&&Number.isFinite(+rows[0].factor_vs_case_er_key),JSON.stringify(rows[0]));
 return +rows[0].factor_vs_case_er_key;
};
const k12Summary=read("school_capital_where_enrolled_2026_10_24/derived/summary.json");
const k12Rows=csv(path.join(FISCAL,"school_capital_where_enrolled_2026_10_24/derived/dollars.csv"));
const k12=k12Rows.find(r=>+r.start_fiscal_year===1992&&r.pre_start_arm==="a"&&r.variant==="primary"&&r.weighting==="mexican_district_share"&&r.factor==="key_consistent_A");
gate("stipulated K12 capital input unique",k12Rows.filter(r=>+r.start_fiscal_year===1992&&r.pre_start_arm==="a"&&r.variant==="primary"&&r.weighting==="mexican_district_share"&&r.factor==="key_consistent_A").length===1,JSON.stringify(k12));
// Do not add k=1.034 a second time. The primary caller's preferred school key
// and the adopted fee bridge both declare the existing operating refinement.
const schoolPreferred=P.schoolV["row6_w0.77|preferred"],schoolPlain=P.schoolV["row6_w0.77"];
const embeddedK=fee.education_key.by_allocation.personal.k;
const k12Exact=k12Summary.headline_key_consistent_A.a;
gate("K12 rounded input matches full precision",near(+k12.delta_low_bn,k12Exact.delta_low_bn,1e-6),k12Exact.delta_low_bn);
gate("K12 operating refinement already included",near(embeddedK,1.0341917412164008,1e-12)&&schoolPreferred.school_target_bn.personal>schoolPlain.school_target_bn.personal,embeddedK);
gate("primary college operating key reproduced",near(college.case_er_share_acs,fee.higher_ed.s_U_acs,1e-12)&&near(factor("er"),1,1e-12),college.case_er_share_acs);
const stockIds=new Set(["college","college_user_fees"]),parkIds=new Set(["rec_sl","rec_fed"]);
const baseRows=[];
for(const [mi,method] of P.METHODS.entries()){
 const m=P.modelFor("central",method,P.withCentral({}));
 for(const [ei,end] of ["low","high"].entries()){
  const i=summary.end_specifications.set[mi][ei],s=P.MAIN_SPECS[i],r=P.evaluateFull(m,s);
  gate(`${method}/${end} endpoint`,i===(end==="low"?16:11)&&s.reading===end&&s.allocation==="personal",i);
  const carriers=P.POST_ENGINE.union_completion.carriers;
  const cov=P.POST_ENGINE.coverage.by_end[end].decomposition.line_parts;
  const count=["native_minor_calibration","coverage_tenure"].flatMap(id=>C.countParts(P.POST_ENGINE[id],end));
  function capital(ids){
   const selected=id=>ids.has(id);
   const parts={
    engine:sum(r.capital.components.filter(c=>selected(c.id)).map(c=>c.return_bn)),
    completion:sum(r.evaluation.spending.filter(q=>carriers[q.id]?.kind==="capital"&&selected(carriers[q.id].parent_line)).map(q=>q.amount_bn*q.response)),
    college_response:ids.has("college")?sum(r.v9_post_engine.parts.public_college_response.filter(q=>q.kind==="college_capital").map(q=>q.delta_bn)):0,
    one_rate:sum(r.v9_post_engine.parts.one_rate.filter(q=>["capital_engine","capital_reporter","college_capital_interaction"].includes(q.component)&&(selected(q.line)||selected(carriers[q.line]?.parent_line))).map(q=>q.delta_bn)),
    coverage:sum(cov.filter(q=>q.source_side==="capital"&&selected(q.source_line)).map(q=>q.coverage_bn)),
    count:sum(count.filter(q=>q.source_side==="capital"&&selected(q.source_line)).map(q=>q.value_bn))
   };
   return {...parts,total_bn:sum(Object.values(parts))};
  }
  function operating(ids){
   const parts={
    engine_completion:sum(r.evaluation.spending.filter(q=>ids.has(q.id)||(carriers[q.id]?.kind==="line"&&carriers[q.id]?.side==="spending"&&ids.has(carriers[q.id].parent_line))).map(q=>q.amount_bn*q.response)),
    coverage:sum(cov.filter(q=>q.source_side==="spending"&&ids.has(q.source_line)).map(q=>q.coverage_bn)),
    count:sum(count.filter(q=>q.source_side==="spending"&&ids.has(q.source_line)).map(q=>q.value_bn))
   };
   return {...parts,total_bn:sum(Object.values(parts))};
  }
  const rate=P.RATE.rateFor(P.POST_ENGINE.one_rate,s);
  const schoolTargetDelta=Object.fromEntries(["personal","shared"].map(a=>[a,-fee.nipa.education_line_bn*fee.nipa.weights.consolidated.k12*fee.education_key.by_allocation[a].K_eff_unpriced*(embeddedK-1)]));
  const schoolNeutral=P.Engine.applyCorrections(m,{edits:[{side:"spending",line:"school_reprice",key:"k",by:schoolTargetDelta}],meta:m.corrections});
  const schoolExisting=P.evaluateFull(m,{...s,rate:0}).cost_bn-P.evaluateFull(schoolNeutral,{...s,rate:0}).cost_bn;
  gate(`${method}/${end} original-union school-only operating control`,near(schoolExisting,-schoolTargetDelta[s.allocation]*s.share*s.school,1e-8),schoolExisting);
  const cap=capital(stockIds),recCap=capital(parkIds),recSL=capital(new Set(["rec_sl"])),recFed=capital(new Set(["rec_fed"]));
  const component=r.capital.components.find(q=>q.id==="college");
  const response=item15.central_response;
  gate(`${method}/${end} item15 response`,near(response,college.case_response_reproduced,1e-12),response);
  const unionOffset=fee.higher_ed.U_capital-fee.higher_ed.U;
  const opFromCapital=(cap.total_bn/(component.stock_charged_bn*rate)-unionOffset*response)*item15.national_exposure_bn;
  const opObserved=sum(r.v9_post_engine.parts.public_college_response.filter(q=>q.kind==="college_operating").map(q=>q.after_bn));
  const addedCap=cap.coverage+cap.count;
  gate(`${method}/${end} college operating typed closure`,near(opFromCapital,opObserved+addedCap/(component.stock_charged_bn*rate)*item15.national_exposure_bn),opFromCapital);
  // The asset key prices higher education only; libraries retain their key.
  // Applying this union share to the additions is an explicit transport arm.
  const higherFraction=fee.nipa.kappa*fee.higher_ed.U/fee.higher_ed.U_capital;
  const higherCap=cap.total_bn*higherFraction;
  const oldK12Return=k12Summary.case_base.k12_return_at_one_rate_bn[end];
  const dep=k12Summary.case_base.k12_depreciation_base_bn;
  const adjustedK12Return=oldK12Return*(k12Exact.F_stock_combined/embeddedK-1);
  const adjustedK12Depreciation=dep.structures*(k12Exact.F_structures/embeddedK-1)+dep.equipment*(k12Exact.F_equipment/embeddedK-1);
  const rec=operating(new Set(["recreation_culture","state_price_recreation_culture"]));
  const recUnpriced=operating(new Set(["recreation_culture"]));
  const recParent=r.evaluation.spending.find(q=>q.id==="recreation_culture");
  // 48.901bn is reproduced from the case's adopted state-price declaration.
  // Only the matched municipal E61 fraction changes; federal and library prices
  // remain in their original components. Every population part is transported.
  const statePriceRow=csv(path.join(FISCAL,"state_priced_services_2026_09_29/derived/corrections.csv")).find(q=>q.line==="recreation_culture"&&q.function==="parks_libraries");
  const slNational=Number(statePriceRow?.sl_amount_bn);
  gate(`${method}/${end} parks SL budget`,near(slNational,48.901,1e-9),JSON.stringify(statePriceRow));
  const parkDelta=recUnpriced.total_bn*slNational/recParent.national_bn*parks.case_matched_municipal_bridge_index_delta;
  baseRows.push({method,end,specification:i,cost_bn:r.cost_bn,one_rate:rate,college_capital:cap,
   college_capital_stock_bn:component.stock_charged_bn,college_operating_bn:opFromCapital,
   college_operating_engine_completion_bn:opObserved,college_higher_capital_fraction:higherFraction,
   college_higher_capital_bn:higherCap,parks_operating:rec,parks_unpriced_operating:recUnpriced,
   parks_capital:recCap,parks_sl_capital:recSL,parks_federal_capital:recFed,
   parks_sl_stock_bn:r.capital.components.find(q=>q.id==="rec_sl").stock_charged_bn,
   parks_sl_response:r.capital.components.find(q=>q.id==="rec_sl").response,
   parks_conditional_delta_bn:parkDelta,k12_capital_stipulated_delta_bn:k12Exact[`delta_${end}_bn`],
   existing_k12_original_union_operating_price_bn:schoolExisting,
   k12_capital_existing_k_denominator_diagnostic_bn:adjustedK12Return+adjustedK12Depreciation,
   _m:m,_s:s,_r:r});
 }
}
const average=(rows,key)=>sum(rows.map(r=>r[key]))/rows.length;
for(const [ei,end] of ["low","high"].entries())gate(`${end} full canonical case`,near(average(baseRows.filter(r=>r.end===end),"cost_bn"),summary.band_bn[ei],1e-8),summary.band_bn[ei]);
const trials=[];
function evaluateTrial(row,name,delta,classification){
 gate(`${name}/${row.method}/${row.end} finite price change`,Number.isFinite(delta),delta);
 const id="where_used_scoped_price_change",m=JSON.parse(JSON.stringify(row._m));
 const cell={target_bn:delta,other_bn:-delta,share:0};
 m.spending.lines.push({id,family:"where_used_price",national_bn:0,response_class:"correction_constant",label:name,
  preferred_key:"k",alternative_key:"k",keys:{k:{personal:{...cell},shared:{...cell}}}});
 const r=P.evaluateFull(m,row._s);
 gate(`${name}/${row.method}/${row.end} canonical delta`,near(r.cost_bn-row.cost_bn,delta,1e-8),r.cost_bn-row.cost_bn);
 gate(`${name}/${row.method}/${row.end} all existing posts held`,near(r.post_engine.total_bn,row._r.post_engine.total_bn,1e-10),r.post_engine.total_bn);
 gate(`${name}/${row.method}/${row.end} tuition Pell receipts and capital held`,JSON.stringify(r.evaluation.receipts)===JSON.stringify(row._r.evaluation.receipts)&&JSON.stringify(r.capital)===JSON.stringify(row._r.capital),"unchanged original account terms");
 trials.push({scenario:name,classification,method:row.method,end:row.end,specification:row.specification,delta_bn:r.cost_bn-row.cost_bn,cost_bn:r.cost_bn});
}
for(const row of baseRows){
 const op=f=>row.college_operating_bn*(f-1),cap=f=>row.college_higher_capital_bn*(f-1);
 const grossFixedSales=f=>op(f)*(1+fee.nipa.tuition_bn/(item15.central_response*item15.national_exposure_bn));
 const park=row.parks_conditional_delta_bn,k12delta=row.k12_capital_stipulated_delta_bn;
 const cases=[
  ["existing_k12_operating_already_included",0,"included; no incremental correction"],
  ["existing_college_er_already_included",0,"included; no incremental correction"],
  ["college_operating_gross_fixed_sales_proxy",grossFixedSales(factor("responsive_gross")),"conditional gross scope/finance bridge; fee dollars fixed"],
  ["college_operating_responsive_net_proxy",op(factor("responsive_net")),"conditional scope/sales/finance bridge"],
  ["college_capital_gross_book_proxy",cap(factor("depreciable_gross")),"conditional historic-cost whole-campus asset proxy"],
  ["college_capital_responsive_assets_proxy",cap(factor("assets_responsive_proxy")),"conditional historic-cost expense-allocation asset proxy"],
  ["college_capital_net_depreciable_proxy",cap(factor("net_depreciable")),"conditional historic-cost net asset proxy"],
  ["parks_matched_municipal_proxy",park,"conditional municipal-only FY22/FY24/NIPA bridge"],
  ["parks_sl_capital_zero_allocation_bound",-row.parks_sl_capital.total_bn,"allocation bound; response held; federal unchanged"],
  ["parks_sl_capital_full_allocation_bound",row.parks_sl_stock_bn*row.one_rate*row.parks_sl_response-row.parks_sl_capital.total_bn,"allocation bound; response held; federal unchanged"],
  ["stipulated_k12_capital_input",k12delta,"stipulated sibling input; baseline caveat in RESULT"],
  ["k12_capital_existing_k_denominator_diagnostic",row.k12_capital_existing_k_denominator_diagnostic_bn,"conditional denominator diagnostic; additions share union factor"],
  ["combined_stipulated_k12_plus_municipal",k12delta+park,"conditional incomplete package; unknown capital/mix held"],
  ["combined_stipulated_k12_book_capital_municipal",k12delta+cap(factor("depreciable_gross"))+park,"conditional incomplete package; no duplicate operating factor"],
  ["combined_denominator_diagnostic_book_capital_municipal",row.k12_capital_existing_k_denominator_diagnostic_bn+cap(factor("depreciable_gross"))+park,"conditional denominator and asset diagnostics; incomplete package"],
  ["combined_with_responsive_net_proxy",k12delta+cap(factor("depreciable_gross"))+op(factor("responsive_net"))+park,"conditional construction sensitivity; not identified correction"]
 ];
 for(const [name,delta,classification] of cases)evaluateTrial(row,name,delta,classification);
 for(const scheme of ["case_fall","annual_case_state_raked"])
  for(const grad of [1,2,3])
   for(const concept of ["depreciable_gross","assets_responsive_proxy","net_depreciable"])
    evaluateTrial(row,`college_asset_arm:${scheme}:${grad}:${concept}`,cap(factor(concept,scheme,grad)),"conditional institution allocation arm");
 for(const concept of ["depreciable_gross","assets_responsive_proxy","net_depreciable"]){
  const c=coverage.find(q=>q.concept===concept);
  gate(`valid unallocated asset bound ${concept}`,c?.nonnegative_allocation_bound_valid==="True",JSON.stringify(c));
  for(const [end,key] of [["lower","factor_low_all_unallocated_to_nonmembers"],["upper","factor_high_all_unallocated_to_members"]])
   evaluateTrial(row,`college_asset_unallocated_bound:${concept}:${end}`,cap(+c[key]),"allocation bound conditional on GASB book-value proxy");
 }
}
const names=[...new Set(trials.map(r=>r.scenario))];
const bands=names.map(name=>{
 const rr=trials.filter(r=>r.scenario===name),lo=rr.filter(r=>r.end==="low"),hi=rr.filter(r=>r.end==="high");
 return {scenario:name,classification:rr[0].classification,delta_low_bn:average(lo,"delta_bn"),delta_high_bn:average(hi,"delta_bn"),cost_low_bn:average(lo,"cost_bn"),cost_high_bn:average(hi,"cost_bn")};
});
const writeCsv=(name,rows)=>{const keys=Object.keys(rows[0]);fs.writeFileSync(path.join(HERE,"derived",name),keys.join(",")+"\n"+rows.map(r=>keys.map(k=>r[k]).join(",")).join("\n")+"\n");};
writeCsv("case_scenarios.csv",bands);writeCsv("case_scenario_methods.csv",trials);
const inputs=["main_case_2026_10_16/package.cjs","main_case_2026_10_16/derived/corrections.json","main_case_2026_10_16/derived/summary.json","user_fee_allocation_2026_10_07/derived/fee_lines.json","school_capital_where_enrolled_2026_10_24/derived/summary.json","school_capital_where_enrolled_2026_10_24/derived/dollars.csv","school_cost_where_enrolled_2026_09_24/derived/school_key_variants.json"];
const hashes=Object.fromEntries(inputs.map(rel=>[path.relative(REPO,path.join(FISCAL,rel)),crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL,rel))).digest("hex")]));
fs.writeFileSync(path.join(HERE,"derived/case_prices.json"),JSON.stringify({case_key:P.CASE_KEY,adopted:false,canonical_band_bn:summary.band_bn,
 existing_k12_operating_factor:embeddedK,incremental_k12_operating_delta_bn:0,case_rows:baseRows.map(({_m,_s,_r,...r})=>r),
 stipulated_k12_capital:k12,source_hashes:hashes,scenarios:bands,gates,
 identification:{complete_where_used_package:"not identified",college_er:"already institution-weighted",college_capital:"proxy; replacement cost and functional use not identified",parks_operating:"matched municipalities measured; fiscal transport conditional",parks_capital:"not identified",k12_operating:"already included"}},null,2)+"\n");
console.log("case_prices: "+gates.length+" gates; "+bands.filter(r=>r.scenario.startsWith("combined_")).map(r=>`${r.scenario}: ${r.delta_low_bn.toFixed(4)}/${r.delta_high_bn.toFixed(4)}bn`).join("; "));
