/* Native oct15 inputs: source-side carriers, coverage and separate set/cash packages. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const FISCAL=path.join(__dirname,"..");
const SOURCE_PINS={
 "winners_losers_2026_09_24/derived/oct14/fiscal_specs.csv":{commit:"2204a2bc0996c3a614262cca55842d0027134417",sha256:"ad7b25de45d395da5fc50eaf3ce0750171ae8afe70364176b0500d9c048e3797"},
 "main_case_2026_10_15/package.cjs":{commit:"d1a24d47d8f17dc6f95bf2b0e431ed7507f52a92",sha256:"083236226e594247bfe095c6cdf0c71f6bb0ca73b405f5da98568ac8c95b90d6"},
 "main_case_2026_10_15/derived/corrections.json":{commit:"d1a24d47d8f17dc6f95bf2b0e431ed7507f52a92",sha256:"d18a185bc0733c47172929ca34ffec9cfc39258239bf41085dd469d73669ad68"},
 "main_case_2026_10_15/derived/corrections_cash.json":{commit:"d1a24d47d8f17dc6f95bf2b0e431ed7507f52a92",sha256:"9af66b4c6a87ddb96d22c208364cd6798d23411590252bbe9520f3019b6446ea"},
 "main_case_2026_10_15/derived/summary.json":{commit:"d1a24d47d8f17dc6f95bf2b0e431ed7507f52a92",sha256:"1d999c666d68696ed2728b9e6fd48c44ab85371e875e3e6f1b16d0b16971013a"},
 "main_case_2026_10_15/derived/main_case_bands.csv":{commit:"d1a24d47d8f17dc6f95bf2b0e431ed7507f52a92",sha256:"fe8fe05bfdeb29f4f4b996bf5e515fcfc172b6094d96c10e67f7cf0840d34ba2"},
 "main_case_2026_10_15/derived/per_spec.csv":{commit:"d1a24d47d8f17dc6f95bf2b0e431ed7507f52a92",sha256:"56b9a3c3ef7c558aee0ffb68e75d9afea1b5df6081cc97898cce00833cce642f"},
 "debt_legacy_2026_09_23/derived/oct15/current_flow_contract.json":{commit:"5a8502c942ed580913f5bf5cd511189ca0c4f1ce",sha256:"153a822a907862ba03ed1c32a50c92c9b5286a9c4961960cd69f90d367c26ec5"},
 "debt_legacy_2026_09_23/derived/oct15/current_flow_source_parts_2024.csv":{commit:"5a8502c942ed580913f5bf5cd511189ca0c4f1ce",sha256:"b4d4595ef1840dc13245e92acc248a6d1333cde9bc012b47241d170a8c104177"},
 "debt_legacy_2026_09_23/derived/oct14/federal_shares_by_year.csv":{commit:"6b1250b9959b692a63d124c579b87c4e86c33015",sha256:"dabcfcef303bafd251191002b69220c36d7eab6dc07134368094ffdb85d44149"}
};
const requireOk=(ok,s)=>{if(!ok)throw Error(`[BLOCKED] oct15 inputs: ${s}`);};
function checkPins(){for(const [rel,pin] of Object.entries(SOURCE_PINS))requireOk(crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL,rel))).digest("hex")===pin.sha256,`source changed: ${rel}`);}
checkPins();
const P=require("../main_case_2026_10_15/package.cjs"),E=P.Engine;
const load=rel=>JSON.parse(fs.readFileSync(path.join(FISCAL,rel)));
function csv(rel){const lines=fs.readFileSync(path.join(FISCAL,rel),"utf8").trimEnd().split("\n").map(line=>{const r=[];let s="",q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){s+='"';i++;}else q=!q;}else if(c===","&&!q){r.push(s);s="";}else s+=c;}r.push(s);return r;});const h=lines.shift();return lines.map(row=>Object.fromEntries(h.map((k,i)=>[k,row[i]])));}
function decomposition(pkg,model,spec){const full=pkg.evaluateFull(model,spec),c=model.corrections.coverage?.by_end[spec.reading]?.decomposition,p=c?.production||{P_bn:0,F_bn:0},post=full.post_engine?.total_bn||0;
 return {cost_bn:full.cost_bn,A_bn:full.evaluation.direct_fiscal_response_bn-full.capital.total_bn-post-p.P_bn-p.F_bn,
 P_bn:full.evaluation.private_wtp_bn+p.P_bn,F_bn:full.evaluation.induced_receipts_bn+p.F_bn,
 capital_bn:full.capital.total_bn,post_engine:full.post_engine||{total_bn:0}};}
function financingDelta(X,B,index,basis,end,source){
 const xm=X.payloadModel(),bm=B.payloadModel(),x=X.evaluateFull(xm,X.MAIN_SPECS[index]),b=B.evaluateFull(bm,B.MAIN_SPECS[index]);
 const typed=source.filter(r=>r.basis===basis&&r.end===end&&r.convention==="central"),parts=[];
 const groups={cash_bn:{fed:0,sl:0},resource_cost_bn:{fed:0,sl:0},accrual_bn:0,displaced_bn:0,unlocated_bn:0,private_production_bn:0};
 function book(value,rs,label){if(Math.abs(value)<1e-12)return;const denominator=rs.reduce((s,r)=>s+Number(r.responsive_bn),0);
   if(Math.abs(denominator)<1e-12){groups.unlocated_bn+=value;parts.push({label,responsive_bn:value,financing:"unlocated",reason:"no identified nonzero source payer"});return;}
   for(const r of rs){const amount=value*Number(r.responsive_bn)/denominator,fin=r.financing;
     const fed=r.federal_bn===""?null:value*Number(r.federal_bn)/denominator,sl=r.state_local_bn===""?null:value*Number(r.state_local_bn)/denominator;
     if(fin==="cash"||fin==="resource_cost"){const key=fin==="cash"?"cash_bn":"resource_cost_bn";groups[key].fed+=fed;groups[key].sl+=sl;}
     else if(fin==="pension_accrual")groups.accrual_bn+=amount;
     else if(fin==="displaced_beneficiaries")groups.displaced_bn+=amount;
     else if(fin==="private_production")groups.private_production_bn+=amount;
     else {requireOk(fin==="unlocated",`unknown source financing ${fin}`);groups.unlocated_bn+=amount;}
     parts.push({label,responsive_bn:amount,federal_bn:fed,state_local_bn:sl,financing:fin});
   }
 }
 // Native child constants are embedded in lane_constants, while their debt
 // source explicitly withholds a government. Recover their exact engine edits.
 function constantAmount(pkg){const pl=pkg.correctionsPayload(),item=pl.meta.items.find(it=>it.id==="union_completion");return item?Object.values(item.parts).reduce((s,p)=>{if(!Number.isInteger(p.edit))return s;const edit=pl.edits[item.edits.first+p.edit];return s+(edit.side==="spending"&&edit.line==="lane_constants"?p.by.personal:0);},0):0;}
 const constantDelta=constantAmount(X)-constantAmount(B);
 for(const side of ["receipt","spending"]){const field=side==="receipt"?"receipts":"spending",xmrows=new Map(x.evaluation[field].map(r=>[r.id,r])),bmrows=new Map(b.evaluation[field].map(r=>[r.id,r]));
   for(const id of new Set([...xmrows.keys(),...bmrows.keys()])){let value=-((xmrows.get(id)?.effect_bn||0)-(bmrows.get(id)?.effect_bn||0));if(side==="spending"&&id==="lane_constants")value-=constantDelta;
     const rs=typed.filter(r=>r.id.replace(/:set_minus_cash$/,"")===id&&(r.side===side||(side==="spending"&&r.side==="reporter_carrier")));
     book(value,rs,`${side}:${id}`);
   }
 }
 if(constantDelta)book(constantDelta,typed.filter(r=>r.side==="native_child_constant"),"native_child_constant");
 const oldcaps=new Map(b.capital.components.map(r=>[r.id,r.return_bn]));
 for(const c of x.capital.components)book(c.return_bn-(oldcaps.get(c.id)||0),typed.filter(r=>r.side==="capital_return"&&r.id===c.id),`capital:${c.id}`);
 const xd=decomposition(X,xm,X.MAIN_SPECS[index]),bd=decomposition(B,bm,B.MAIN_SPECS[index]);
 // Engine induced receipts, exclusive of coverage's separately typed pieces.
 book(-(x.evaluation.induced_receipts_bn-b.evaluation.induced_receipts_bn),typed.filter(r=>r.side==="production"&&r.id==="induced_receipts_F"),"production:induced_F");
 const mixed=(xm.corrections.mixed_unit_removal?.by_end[end].total_bn||0)-(bm.corrections.mixed_unit_removal?.by_end[end].total_bn||0);
 book(mixed,typed.filter(r=>r.side==="post_engine"),"mixed_unit_removal");
 const cov=(xm.corrections.coverage?.by_end[end].total_bn||0)-(bm.corrections.coverage?.by_end[end].total_bn||0);
 book(cov,typed.filter(r=>r.side==="coverage"),"coverage");
 // Private production is outside financing. Coverage's P was already included
 // with its source pieces; add only the engine production change here.
 groups.private_production_bn-=x.evaluation.private_wtp_bn-b.evaluation.private_wtp_bn;
 const total=groups.cash_bn.fed+groups.cash_bn.sl+groups.resource_cost_bn.fed+groups.resource_cost_bn.sl+groups.accrual_bn+groups.displaced_bn+groups.unlocated_bn+groups.private_production_bn;
 requireOk(Math.abs(total-(xd.cost_bn-bd.cost_bn))<1e-6,`isolated financing closure ${basis}/${end}: ${total} vs ${xd.cost_bn-bd.cost_bn}`);
 return {...groups,total_bn:total,parts,rule:"native isolated source deltas at this endpoint; full oct15 typed-debt source government/timing ratios transported; no unlocated fallback"};
}
function main(){
 checkPins();
 const payload=load("main_case_2026_10_15/derived/corrections.json"),cashPayload=load("main_case_2026_10_15/derived/corrections_cash.json"),summary=load("main_case_2026_10_15/derived/summary.json");
 const setModel=E.applyCorrections(P.MODEL,payload),cashModel=E.applyCorrections(P.MODEL,cashPayload);
 const debt=load("debt_legacy_2026_09_23/derived/oct15/current_flow_contract.json"),source=csv("debt_legacy_2026_09_23/derived/oct15/current_flow_source_parts_2024.csv");
 requireOk(debt.case==="oct15"&&debt.gates.every(g=>g.passed),"debt contract is not passing oct15");
 const shares=new Map(csv("debt_legacy_2026_09_23/derived/oct14/federal_shares_by_year.csv").filter(r=>r.convention==="central"&&r.year==="2024").map(r=>[r.line,Number(r.federal_share)]));
 const rows={},programmes={},detailed={},gates=[],netTiming={},nontrustTimingBridge={},timingBridgeParts={},timingBridge={};
 function sourceAmount(full,pl,parent,side){let amount=full.evaluation[side==="receipt"?"receipts":"spending"].find(l=>l.id===parent)?.amount_bn||0;
   for(const l of full.evaluation.spending){const s=pl.meta.union_completion.carriers[l.id];if(s?.kind==="line"&&s.side===side&&s.parent_line===parent)amount+=(side==="receipt"?-1:1)*l.amount_bn*l.response;}
   for(const p of pl.meta.coverage.by_end[full.evaluation._reading].decomposition.line_parts)if(p.economic_class==="fiscal_line"&&p.source_side===side&&p.source_line===parent)amount+=(side==="receipt"?-1:1)*p.coverage_bn;
   return amount;
 }
 for(const [j,end] of ["low","high"].entries()){
   const spec=P.MAIN_SPECS[summary.v8.end_specifications.set[0][j]],set=P.evaluateFull(setModel,spec),cash=P.CASH.evaluateFull(cashModel,spec);
   set.evaluation._reading=cash.evaluation._reading=end;
   const gap=set.cost_bn-cash.cost_bn;
   requireOk(Math.abs(gap-(summary.v8.band_bn[j]-summary.v8.cash_set_bn[j]))<1e-9,"set/cash pension increment differs");
   requireOk(Math.abs(set.cost_bn-debt.bands_bn.set[j])<1e-9&&Math.abs(cash.cost_bn-debt.bands_bn.cash[j])<1e-9,"debt/case totals differ");
   for(const basis of ["set","cash"]){const typed=source.filter(r=>r.basis===basis&&r.end===end&&r.convention==="central");const total=typed.reduce((s,r)=>s+Number(r.responsive_bn),0);requireOk(Math.abs(total-debt.bands_bn[basis][j])<1e-6,`typed ${basis}/${end} closure`);gates.push({basis,end,total_bn:total,case_bn:debt.bands_bn[basis][j],gap_bn:total-debt.bands_bn[basis][j]});}
   const typedSet=source.filter(r=>r.basis==="set"&&r.end===end&&r.convention==="central");
   const fundAccrual=typedSet.filter(r=>r.financing==="pension_accrual").reduce((s,r)=>s+Number(r.responsive_bn),0);
   const bridgeParts=typedSet.filter(r=>r.financing==="unlocated"&&r.id.endsWith(":set_minus_cash"));
   requireOk(bridgeParts.length===1&&bridgeParts[0].side==="coverage"&&bridgeParts[0].id==="net_profile_calibration:set_minus_cash",`nontrust timing source changed ${end}`);
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
   programmes[end]=detailed[end].filter(l=>l.national_bn>0);
   for(const l of priced){const sum=detailed[end].filter(r=>r.source_id===l.id).reduce((s,r)=>s+r.amount_bn,0),expected=l.amount_bn*l.response;
     requireOk(Math.abs(sum-expected)<1e-9,`programme source closure ${end}/${l.id}`);
     gates.push({kind:"programme",end,source_id:l.id,total_bn:sum,source_bn:expected,gap_bn:sum-expected});}
   const school=detailed[end].filter(l=>l.source_id==="education_services").reduce((s,l)=>s+l.amount_bn,0);
   requireOk(Math.abs(school-spending.get("education_services").amount_bn*spending.get("education_services").response)<1e-9,"education split closure");
 }
 const i=process.argv.indexOf("--out-dir"),out=i>0?path.resolve(process.argv[i+1]):path.join(__dirname,"derived/oct15");fs.mkdirSync(out,{recursive:true});
 const write=(name,data)=>fs.writeFileSync(path.join(out,name),JSON.stringify(data,null,1)+"\n");
 write("p7_trust_inputs.json",{case:"oct15",rows,programmes,debt_contract:debt,gates,source_pins:SOURCE_PINS,
   net_timing:netTiming,nontrust_timing_bridge:nontrustTimingBridge,nontrust_timing_bridge_parts:timingBridgeParts,
   timing_bridge:timingBridge,
   timing_rule:"fund accrual is the principal typed pension_accrual sum; net case timing additionally includes coverage net_profile_calibration:set_minus_cash, which stays unlocated and is never added to trust financing",
   rule:"complete gross payroll/cash OASDI-HI plus source-side reporter and coverage parts; fund accrual from typed pension_accrual rows only"});
 write("p8_programmes.json",{case:"oct15",programmes:Object.fromEntries(Object.entries(detailed).map(([end,rs])=>[end,rs.filter(r=>r.jurisdiction.federal!==null)])),
   unlocated_programmes:Object.fromEntries(Object.entries(detailed).map(([end,rs])=>[end,rs.filter(r=>r.jurisdiction.federal===null)])),source_classifications:source.filter(r=>r.convention==="central"),source_pins:SOURCE_PINS,
   rule:"programme authority for recipient keys; actual case funding from typed debt current-flow parts; frozen oct14 national shares supply unchanged national programme keys only"});
 if(!process.argv.includes("--skip-item-effects")){
   const items=["foreign_source_tax","union_completion","mixed_unit_removal","coverage"],baseIds=P.V7_PACKAGE.CANDIDATE,base=P.caseOf(P.V7_PACKAGE.OCT05,baseIds),effects={case:"oct15",rule:"isolated additions to v7 at adopted oct15 specs; joint minus sum is interaction",source_pins:SOURCE_PINS,items:{},base:{},joint:{},interaction:{}};
   const packs=Object.fromEntries(items.map(id=>[id,P.caseOf(P.V7_PACKAGE.OCT05,baseIds.concat(id))]));
   for(const basis of ["set","cash"]){effects.base[basis]={};effects.joint[basis]={};effects.interaction[basis]={};
     for(const [j,end] of ["low","high"].entries()){const index=summary.v8.end_specifications[basis][0][j],B=basis==="set"?base:base.CASH,Q=basis==="set"?P:P.CASH;
       const baseline=decomposition(B,B.payloadModel(),B.MAIN_SPECS[index]),full=decomposition(Q,Q.payloadModel(),Q.MAIN_SPECS[index]);effects.base[basis][end]=baseline;effects.joint[basis][end]={};effects.interaction[basis][end]={};
       for(const field of ["cost_bn","A_bn","P_bn","F_bn","capital_bn"])effects.joint[basis][end][field]=full[field]-baseline[field];
       for(const id of items){const X=basis==="set"?packs[id]:packs[id].CASH,z=decomposition(X,X.payloadModel(),X.MAIN_SPECS[index]);effects.items[id]??={};effects.items[id][basis]??={};effects.items[id][basis][end]={};for(const field of ["cost_bn","A_bn","P_bn","F_bn","capital_bn"])effects.items[id][basis][end][field]=z[field]-baseline[field];effects.items[id][basis][end].financing=financingDelta(X,B,index,basis,end,source);}
       for(const field of ["cost_bn","A_bn","P_bn","F_bn","capital_bn"])effects.interaction[basis][end][field]=effects.joint[basis][end][field]-items.reduce((sum,id)=>sum+effects.items[id][basis][end][field],0);
       effects.joint[basis][end].financing=financingDelta(Q,B,index,basis,end,source);
       const jf=effects.joint[basis][end].financing,interaction={};
       for(const field of ["cash_bn","resource_cost_bn"]){interaction[field]={};for(const government of ["fed","sl"])interaction[field][government]=jf[field][government]-items.reduce((sum,id)=>sum+effects.items[id][basis][end].financing[field][government],0);}
       for(const field of ["accrual_bn","displaced_bn","unlocated_bn","private_production_bn","total_bn"])interaction[field]=jf[field]-items.reduce((sum,id)=>sum+effects.items[id][basis][end].financing[field],0);
       effects.interaction[basis][end].financing=interaction;
       for(const id of items)requireOk(Math.abs(effects.items[id][basis][end].cost_bn-summary.v8.change_by_item[id][basis][j])<1e-6,`isolated ${id}/${basis}/${end} source parity`);
     }
   }
   effects.parts={mixed_unit_removal:payload.meta.mixed_unit_removal,coverage:payload.meta.coverage};write("p8_item_effects.json",effects);
 }
 console.log("[oct15 inputs] all case/debt/programme gates passed",rows);
}
module.exports={SOURCE_PINS,checkPins,decomposition};
if(require.main===module)main();
