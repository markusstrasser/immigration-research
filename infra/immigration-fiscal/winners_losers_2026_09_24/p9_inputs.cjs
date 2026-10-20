/* Native oct16 inputs: complete typed source classes, canonical v9 evaluator. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const FISCAL=path.join(__dirname,"..");
const ROOT=path.resolve(FISCAL,"../.."),PREFIX="infra/immigration-fiscal/";
const required=["winners_losers_2026_09_24/specs.cjs","winners_losers_2026_09_24/p9_inputs.cjs",
 "winners_losers_2026_09_24/derived/oct14/fiscal_specs.csv",
 ...["package.cjs","derived/corrections.json","derived/corrections_cash.json","derived/summary.json","derived/main_case_bands.csv","derived/per_spec.csv"].map(s=>"main_case_2026_10_16/"+s),
 ...["current_flow_contract.json","current_flow_source_parts_2024.csv"].map(s=>"debt_legacy_2026_09_23/derived/oct16/"+s),
 "debt_legacy_2026_09_23/derived/oct14/federal_shares_by_year.csv"];
const requireOk=(ok,s)=>{if(!ok)throw Error(`[BLOCKED] oct16 inputs: ${s}`);};
let SOURCE_PINS={};
function checkPins(){
 const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,"inputs/p9_pins_oct16.json"),"utf8"));
 requireOk(manifest.case==="oct16"&&manifest.sha256,"missing oct16 SHA256 manifest");
 for(const rel of required)requireOk(/^[a-f0-9]{64}$/.test(manifest.sha256[PREFIX+rel]||""),`principal source not pinned: ${rel}`);
 // The Python incidence runner checks its complete manifest. This producer
 // verifies its own principal inputs and sources; concurrent Python edits are
 // outside this route's dependency set and cannot invalidate an export.
 for(const source of required){
   const rel=PREFIX+source,hash=manifest.sha256[rel];
   const absolute=path.resolve(ROOT,rel);requireOk(absolute.startsWith(ROOT+path.sep),`source outside root: ${rel}`);
   requireOk(crypto.createHash("sha256").update(fs.readFileSync(absolute)).digest("hex")===hash,`source changed: ${rel}`);
 }
 SOURCE_PINS=Object.fromEntries(required.map(rel=>[rel,{sha256:manifest.sha256[PREFIX+rel]}]));
 return SOURCE_PINS;
}
const load=rel=>JSON.parse(fs.readFileSync(path.join(FISCAL,rel)));
function csv(rel){const lines=fs.readFileSync(path.join(FISCAL,rel),"utf8").trimEnd().split("\n").map(line=>{const r=[];let s="",q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){s+='"';i++;}else q=!q;}else if(c===","&&!q){r.push(s);s="";}else s+=c;}r.push(s);return r;});const h=lines.shift();return lines.map(row=>Object.fromEntries(h.map((k,i)=>[k,row[i]])));}
function decomposition(pkg,model,spec){const full=pkg.evaluateFull(model,spec),c=model.corrections.coverage?.by_end[spec.reading]?.decomposition,p=c?.production||{P_bn:0,F_bn:0},post=full.post_engine?.total_bn||0;
 return {cost_bn:full.cost_bn,A_bn:full.evaluation.direct_fiscal_response_bn-full.capital.total_bn-post-p.P_bn-p.F_bn,
 P_bn:full.evaluation.private_wtp_bn+p.P_bn,F_bn:full.evaluation.induced_receipts_bn+p.F_bn,
 capital_bn:full.capital.total_bn,post_engine:full.post_engine||{total_bn:0}};}
function main(){
 checkPins();
 const P=require("../main_case_2026_10_16/package.cjs"),E=P.Engine;
 const payload=load("main_case_2026_10_16/derived/corrections.json"),cashPayload=load("main_case_2026_10_16/derived/corrections_cash.json"),summary=load("main_case_2026_10_16/derived/summary.json");
 const setModel=E.applyCorrections(P.MODEL,payload),cashModel=E.applyCorrections(P.MODEL,cashPayload);
 const debt=load("debt_legacy_2026_09_23/derived/oct16/current_flow_contract.json"),source=csv("debt_legacy_2026_09_23/derived/oct16/current_flow_source_parts_2024.csv");
 requireOk(debt.case==="oct16"&&debt.gates.every(g=>g.passed),"debt contract is not passing oct16");
 const shares=new Map(csv("debt_legacy_2026_09_23/derived/oct14/federal_shares_by_year.csv").filter(r=>r.convention==="central"&&r.year==="2024").map(r=>[r.line,Number(r.federal_share)]));
 const rows={},programmes={},detailed={},gates=[],netTiming={},nontrustTimingBridge={},timingBridgeParts={},timingBridge={};
 function sourceAmount(full,pl,parent,side){let amount=full.evaluation[side==="receipt"?"receipts":"spending"].find(l=>l.id===parent)?.amount_bn||0;
   for(const l of full.evaluation.spending){const s=pl.meta.union_completion.carriers[l.id];if(s?.kind==="line"&&s.side===side&&s.parent_line===parent)amount+=(side==="receipt"?-1:1)*l.amount_bn*l.response;}
   const end=full.evaluation._reading,basis=pl===cashPayload?"cash":"set";
   for(const p of pl.meta.coverage.by_end[end].decomposition.line_parts)if(p.economic_class==="fiscal_line"&&p.source_side===side&&p.source_line===parent)amount+=(side==="receipt"?-1:1)*p.coverage_bn;
   // Coverage is already repriced above. These are only the new noncoverage
   // native/count source deltas, at this accounting set's own prices.
   for(const p of source)if(p.basis===basis&&p.end===end&&p.convention==="central"&&p.side==="v9_item"&&p.item!=="coverage_repricing"&&p.source_side===side&&p.source_line===parent)
     amount+=(side==="receipt"?-1:1)*Number(p.responsive_bn);
   return amount;
 }
 for(const [j,end] of ["low","high"].entries()){
   const spec=P.MAIN_SPECS[summary.v9.end_specifications.set[0][j]],set=P.evaluateFull(setModel,spec),cash=P.CASH.evaluateFull(cashModel,spec);
   set.evaluation._reading=cash.evaluation._reading=end;
   const gap=set.cost_bn-cash.cost_bn;
   requireOk(Math.abs(gap-(summary.v9.band_bn[j]-summary.v9.cash_set_bn[j]))<1e-9,"set/cash pension increment differs");
   requireOk(Math.abs(set.cost_bn-debt.bands_bn.set[j])<1e-9&&Math.abs(cash.cost_bn-debt.bands_bn.cash[j])<1e-9,"debt/case totals differ");
   for(const basis of ["set","cash"]){const typed=source.filter(r=>r.basis===basis&&r.end===end&&r.convention==="central");const total=typed.reduce((s,r)=>s+Number(r.responsive_bn),0);requireOk(Math.abs(total-debt.bands_bn[basis][j])<1e-6,`typed ${basis}/${end} closure`);gates.push({basis,end,total_bn:total,case_bn:debt.bands_bn[basis][j],gap_bn:total-debt.bands_bn[basis][j]});}
   const typedSet=source.filter(r=>r.basis==="set"&&r.end===end&&r.convention==="central");
   const fundAccrual=typedSet.filter(r=>r.financing==="pension_accrual").reduce((s,r)=>s+Number(r.responsive_bn),0);
   const bridgeParts=typedSet.filter(r=>r.financing==="unlocated"&&r.id.endsWith(":set_minus_cash"));
   requireOk(bridgeParts.length>=1&&bridgeParts.every(r=>r.id==="net_profile_calibration:set_minus_cash"||r.source_line==="net_profile_calibration"),`nontrust timing source changed ${end}`);
   const bridge=bridgeParts.reduce((s,r)=>s+Number(r.responsive_bn),0);
   requireOk(Math.abs(fundAccrual+bridge-gap)<1e-9,`trust accrual plus explicit nontrust timing bridge ${end}`);
   netTiming[end]=gap;nontrustTimingBridge[end]=bridge;timingBridgeParts[end]=bridgeParts;
   timingBridge[end]={net_set_minus_cash_bn:gap,nontrust_timing_bridge_bn:bridge,trust_accrual_bn:fundAccrual,source:"coverage:net_profile_calibration:set_minus_cash"};
   gates.push({kind:"trust_timing",end,fund_accrual_bn:fundAccrual,nontrust_timing_bridge_bn:bridge,net_set_minus_cash_bn:gap,gap_bn:fundAccrual+bridge-gap});
   const payroll=["employee_oasdi","employer_oasdi","employee_hi","employer_hi","self_employment_oasdi_hi"].reduce((s,id)=>s+sourceAmount(cash,cashPayload,id,"receipt"),0);
   const cashBenefits=sourceAmount(cash,cashPayload,"social_security","spending")+payload.meta.pension_accrual.part_a_share*sourceAmount(cash,cashPayload,"medicare","spending");
   const hiAccrual=sourceAmount(set,payload,"medicare","spending")-sourceAmount(cash,cashPayload,"medicare","spending")+payload.meta.pension_accrual.part_a_share*sourceAmount(cash,cashPayload,"medicare","spending");
   rows[end]={payroll_bn:payroll,cash_benefits_bn:cashBenefits,accrual_bn:fundAccrual,hi_payout_fraction:hiAccrual/(hiAccrual+sourceAmount(set,payload,"social_security","spending")),trust_cost_bn:cashBenefits+fundAccrual-payroll,set_cost_bn:set.cost_bn,cash_cost_bn:cash.cost_bn};
   const national=new Map(P.withSyntheticLines(setModel).spending.lines.map(l=>[l.id,l.national_bn]));
   const spending=new Map(set.evaluation.spending.map(l=>[l.id,l]));
   const priced=set.evaluation.spending.filter(l=>l.response>0&&(national.get(l.id)>0||l.amount_bn!==0)).filter(l=>{const c=payload.meta.union_completion.carriers[l.id];return !c||(c.kind==="line"&&c.side==="spending");});
   detailed[end]=[];
   for(const l of priced){const carrier=payload.meta.union_completion.carriers[l.id],parent=carrier?.parent_line||l.id;
     let funding=shares.get(parent);const typed=source.filter(r=>r.basis==="set"&&r.end===end&&r.convention==="central"&&r.id.replace(/:set_minus_cash$/,"")===l.id&&["spending","reporter_carrier"].includes(r.side));
     const denom=typed.filter(r=>r.federal_bn!=="").reduce((s,r)=>s+Number(r.responsive_bn),0),fed=typed.reduce((s,r)=>s+Number(r.federal_bn),0);
     if(Math.abs(denom)>1e-12)funding=fed/denom;
     if(["school_reprice","college_rekey"].includes(parent))funding=shares.get("education_services");
     const unlocated=!(funding>=0&&funding<=1);
     requireOk(!unlocated||!(national.get(l.id)>0),`national programme government absent ${l.id}`);
     const slices=parent==="education_services"?[["education_k12",payload.meta.user_fees.k12_weight.w_K],["education_college_other",1-payload.meta.user_fees.k12_weight.w_K]]:[[parent,1]];
     for(const [id,fraction] of slices){const slOnly=["education_k12","education_college_other","school_reprice","college_rekey","public_order_safety"].includes(id),fedOnly=["social_security","medicare","ssi","snap","refundable_tax_credits"].includes(id);
       const authority=slOnly?0:fedOnly?1:unlocated?null:funding;
       detailed[end].push({id,source_id:l.id,source_side:"spending",source_parent:parent,national_bn:(national.get(l.id)||0)*fraction,response:l.response,amount_bn:l.amount_bn*l.response*fraction,
         federal_share:unlocated?null:funding,state_local_bn:unlocated?null:l.amount_bn*l.response*fraction*(1-funding),jurisdiction:{federal:authority,state_local:authority===null?null:1-authority},
         financing_unlocated:unlocated,jurisdiction_basis:slOnly?"state-local service delivery; funding retains grants":fedOnly?"federal programme authority":"source-classified debt funding; unlocated composite stays explicit"});
     }
   }
   for(const l of priced){const sum=detailed[end].filter(r=>r.source_id===l.id).reduce((s,r)=>s+r.amount_bn,0),expected=l.amount_bn*l.response;
     requireOk(Math.abs(sum-expected)<1e-9,`programme source closure ${end}/${l.id}`);
     gates.push({kind:"programme",end,source_id:l.id,total_bn:sum,source_bn:expected,gap_bn:sum-expected});}
   const school=detailed[end].filter(l=>l.source_id==="education_services").reduce((s,l)=>s+l.amount_bn,0);
   requireOk(Math.abs(school-spending.get("education_services").amount_bn*spending.get("education_services").response)<1e-9,"education split closure");
   // Recipient keys price national responding programmes. Military replacement
   // removes service-earned national subblocks, while the means-tested pension
   // remains. Item15 changes the net college consumption block, not tuition/Pell.
   const military=set.v9_post_engine.parts.veterans_compensation.filter(p=>p.population==="engine");
   for(const p of military){
     const row=detailed[end].find(r=>r.source_id===p.source_line&&r.national_bn>0);
     requireOk(row,`military national programme absent ${p.source_line}`);
     const national=p.part==="compensation"?p.national_bn:p.national_component_bn;
     const delta=national*(p.response-1);
     const beforeNational=row.national_bn*row.response;
     const beforeFederal=beforeNational*row.jurisdiction.federal;
     row.response+=delta/row.national_bn;
     requireOk(row.response>=-1e-12&&row.response<=1,`military programme response ${p.source_line}`);
     row.response=Math.max(0,row.response);
     const responding=row.national_bn*row.response;
     // Every removed military subblock is federal. Preserve the civilian
     // state/local health mass instead of reducing it proportionally.
     if(responding>1e-12){
       const federal=(beforeFederal+delta)/responding;
       requireOk(federal>=-1e-12&&federal<=1+1e-12,`military national jurisdiction ${p.source_line}`);
       row.jurisdiction={federal:Math.max(0,Math.min(1,federal)),state_local:1-Math.max(0,Math.min(1,federal))};
     }
     row.response_basis="v9 equal-cost military replacement; service subblock response0, pension retained";
   }
   const college=set.v9_post_engine.parts.public_college_response.find(p=>p.population==="engine"&&p.kind==="college_operating"&&p.capital_source_line==="college");
   requireOk(college&&college.use_share>0,"college national response source absent");
   const collegeRow=detailed[end].find(r=>r.id==="education_college_other"&&r.source_id==="education_services");
   collegeRow.response+=college.delta_bn/college.use_share/collegeRow.national_bn;
   requireOk(collegeRow.response>=0&&collegeRow.response<=1,"college national response invalid");
   collegeRow.response_basis="v9 net college consumption block response; tuition and Pell unchanged";
   // Preserve every signed new spending source amount separately. These carry
   // no new national budget mass: count/calibration does not create a programme.
   for(const p of typedSet.filter(p=>p.side==="v9_item"&&p.item!=="coverage_repricing"&&p.source_side==="spending")){
     const parent=p.source_line,template=detailed[end].find(r=>r.source_parent===parent);
     const located=p.federal_bn!==""&&p.state_local_bn!=="",value=Number(p.responsive_bn);
     const funding=located&&Math.abs(value)>1e-12?Number(p.federal_bn)/value:null;
     const authority=template?.jurisdiction||{federal:null,state_local:null};
     detailed[end].push({id:template?.id||parent,source_id:p.id,source_side:"spending",source_parent:parent,
       national_bn:0,response:1,amount_bn:value,federal_share:funding,state_local_bn:located?Number(p.state_local_bn):null,
       jurisdiction:authority,financing_unlocated:!located,jurisdiction_basis:"v9 signed source adjustment; national programme mass held",item:p.item});
   }
   programmes[end]=detailed[end].filter(l=>l.national_bn>0);
 }
 checkPins();
 const i=process.argv.indexOf("--out-dir"),out=i>0?path.resolve(process.argv[i+1]):path.join(__dirname,"derived/oct16");fs.mkdirSync(out,{recursive:true});
 const write=(name,data)=>fs.writeFileSync(path.join(out,name),JSON.stringify(data,null,1)+"\n");
 write("p7_trust_inputs.json",{case:"oct16",rows,programmes,debt_contract:debt,gates,source_pins:SOURCE_PINS,
   net_timing:netTiming,nontrust_timing_bridge:nontrustTimingBridge,nontrust_timing_bridge_parts:timingBridgeParts,
   timing_bridge:timingBridge,
   timing_rule:"fund accrual is the principal typed pension_accrual sum; net case timing additionally includes coverage net_profile_calibration:set_minus_cash, which stays unlocated and is never added to trust financing",
   rule:"complete gross payroll/cash OASDI-HI plus source-side reporter and coverage parts; fund accrual from typed pension_accrual rows only"});
 write("p8_programmes.json",{case:"oct16",programmes:Object.fromEntries(Object.entries(detailed).map(([end,rs])=>[end,rs.filter(r=>r.jurisdiction.federal!==null)])),
   unlocated_programmes:Object.fromEntries(Object.entries(detailed).map(([end,rs])=>[end,rs.filter(r=>r.jurisdiction.federal===null)])),source_classifications:source.filter(r=>r.convention==="central"),source_pins:SOURCE_PINS,
   rule:"programme authority for recipient keys; actual case funding from typed debt current-flow parts; frozen oct14 national shares supply unchanged national programme keys only"});
 console.log("[oct16 inputs] all case/debt/programme gates passed",rows);
}
module.exports={checkPins,decomposition,main};
if(require.main===module)main();
