/* Reprice corrected v8 without writing or modifying any upstream lane.
 * Fixed age and own-record profile transfers are the case's existing contracts.
 */
"use strict";
const fs=require("fs"),path=require("path");
const F=path.resolve(__dirname,".."), P=require("../main_case_2026_10_15/package.cjs");
const read=f=>JSON.parse(fs.readFileSync(path.join(F,f),"utf8"));
const fail=s=>{throw Error(`[BLOCKED] one-rate evaluator: ${s}`);};
const check=(s,v)=>{if(!v)fail(s);};
const near=(a,b,t=1e-9)=>Math.abs(a-b)<=t;
const sum=a=>a.reduce((x,y)=>x+y,0), GENS=["G1","G2","G3plus"];
const lines=read("within_group_distribution_2026_09_29/_cache/oct14/lines.json");
check("pre-v8 historical basis is oct14",lines.meta.key==="oct14"||lines.meta.case_key==="oct14"||JSON.stringify(lines.meta).includes("main_case_2026_10_14"));
const cover=read("coverage_bound_2026_10_14/derived/coverage_bound_oct15.json");
const input=read("row4_class_2026_09_29/derived/row4_oct07_inputs.json");
const BW4=input.benefit_tax.weights.row4;
const row=(block,id,side="spending")=>{const a=block.rows.filter(r=>r.id===id&&r.side===side);check(`unique ${side}/${id}`,a.length===1);return a[0];};
const pa=lines.meta.pension_accrual, orig=lines.meta.lineage.pension_bn.low;
const payload=P.correctionsPayload(), cashPayload=P.CASH.correctionsPayload();
const unionRec=p=>p.meta.items.find(i=>i.id==="union_completion");
function childAmount(p,id){const rec=unionRec(p),key=P.payloadModel().spending.lines.find(l=>l.id===id)?.preferred_key;
 check(`native child preferred key ${id}`,typeof key==="string");
 return sum(Object.entries(rec.parts).filter(([name,v])=>{
  const e=p.edits[rec.edits.first+v.edit];return name.startsWith("lineage_g3plus:observed_nonreporters:spending:")&&e.line===id&&e.key===key;
}).map(([,v])=>v.by.personal));}
const native={ss:childAmount(payload,"social_security"),pa:childAmount(payload,"medicare")-(1-pa.part_a_share)*childAmount(cashPayload,"medicare")};
const priceText=fs.readFileSync(path.join(F,"union_completion_2026_10_14/derived/pricing_lines.csv"),"utf8").trim().split("\n");
const header=priceText.shift().split(",");
const pricing=priceText.map(l=>Object.fromEntries(l.split(",").map((v,i)=>[header[i],v])));
function reporter(end,id){return sum(pricing.filter(r=>r.basis==="set"&&r.end===end&&r.line===id&&r.category==="pension_accrual").map(r=>Number(r.central_bn)));}
const sourceUnion=lines.union.low;
const O={},H={};
for(const g of GENS){const b=lines.generations[g].low;
 O[g]=sum(pa.oasdi_lines.map(id=>row(b,id,"receipt").amount_bn))+pa.se_oasdi_share*row(b,pa.se_line,"receipt").amount_bn;
 H[g]=sum(pa.hi_lines.map(id=>row(b,id,"receipt").amount_bn))+(1-pa.se_oasdi_share)*row(b,pa.se_line,"receipt").amount_bn;
}
// G3 receipt rows contain original descendants. Remove the lineage's own
// receipts; generation split normalization is on the identified union only.
O.G3plus-=orig.oasdi_receipts_bn;
// HI lineage amount is read from the lineage edits, before later receipt items.
const L=P.OCT07.LINEAGE_EDITS;
const linReceipt=id=>sum(L.filter(e=>e.side==="receipt"&&e.line===id&&e.scenario===P.MODEL.receipts.reference).map(e=>e.by.personal));
H.G3plus-=sum(pa.hi_lines.map(linReceipt))+(1-pa.se_oasdi_share)*linReceipt(pa.se_line);
const OU=sum(Object.values(O));
function nr(x,g){const a=x.groups[g];return a.per_tax_dollar*(1-BW4.groups[g].relative_rate*a.timing);}
function split(x){const n=Object.fromEntries(GENS.map(g=>[g,nr(x,g)])),h=Object.fromEntries(GENS.map(g=>[g,x.groups[g].part_a_per_hi_tax_dollar]));
 const sn=sum(GENS.map(g=>n[g]*O[g])),sh=sum(GENS.map(g=>h[g]*H[g]));
 return {unionSS:nr(x,"union")*OU,unionPA:x.part_a_bn,
 ss:Object.fromEntries(GENS.map(g=>[g,nr(x,"union")*OU*n[g]*O[g]/sn])),
 pa:Object.fromEntries(GENS.map(g=>[g,x.part_a_bn*h[g]*H[g]/sh]))};}
function repricing(rates,label){
 const control=rates.arms.unchanged.result_row4;
 const source=rates.arms[label];check(`${label} has row4 run`,!!source?.result_row4);
 const x=source.result_row4,old=split(control),next=split(x),rounding_residue={ss:{},pa:{}};
 // The inherited split reads nine-decimal arms.csv ratios. Preserve its
 // frozen rounding residue when computing the new-minus-old valuation.
 for(const g of GENS){const p=lines.generations[g].low.pension;
  for(const [k,total] of [["ss",p.accrual_bn-(g==="G3plus"?orig.accrual:0)],["pa",p.part_a_accrual_bn-(g==="G3plus"?orig.part_a:0)]]){
   const residue=total-old[k][g];check(`frozen split rounding ${k}/${g}`,Math.abs(residue)<1e-6);
   rounding_residue[k][g]=residue;old[k][g]=total;next[k][g]+=residue;
  }
 }
 const fss=nr(x,"G3plus")/nr(control,"G3plus"),fpa=x.groups.G3plus.part_a_per_hi_tax_dollar/control.groups.G3plus.part_a_per_hi_tax_dollar;
 const pooledSS0=old.ss.G3plus+orig.accrual,pooledSS1=next.ss.G3plus+orig.accrual*fss;
 const pooledPA0=old.pa.G3plus+orig.part_a,pooledPA1=next.pa.G3plus+orig.part_a*fpa;
 check("old union SS closes",near(old.unionSS,row(sourceUnion,"social_security").amount_bn-orig.accrual,1e-8));
 check("old union Part A closes",near(old.unionPA,pa.part_a_accrual_bn+pa.row4_union_bn.low.part_a,1e-8));
 check("pooled G3 SS closes",near(pooledSS0,lines.generations.G3plus.low.pension.accrual_bn,1e-7));
 check(`pooled G3 Part A closes ${pooledPA0} vs ${lines.generations.G3plus.low.pension.part_a_accrual_bn}; H ${JSON.stringify(H)}`,near(pooledPA0,lines.generations.G3plus.low.pension.part_a_accrual_bn,1e-7));
 return {old,next,fss,fpa,rounding_residue,pooledSS:pooledSS1/pooledSS0,pooledPA:pooledPA1/pooledPA0,
   generationSS:Object.fromEntries(GENS.map(g=>[g,g==="G3plus"?pooledSS1/pooledSS0:next.ss[g]/old.ss[g]])),
   generationPA:Object.fromEntries(GENS.map(g=>[g,g==="G3plus"?pooledPA1/pooledPA0:next.pa[g]/old.pa[g]]))};
}
function coverage(which,end){return cover.sets[which].scenarios.central.ends[end].decomposition;}
function capitalOf(ev,end,which){const c=payload.meta.union_completion.carriers;
 const reporter=sum(ev.evaluation.spending.filter(r=>c[r.id]?.kind==="capital").map(r=>-r.effect_bn));
 const dec=coverage(which,end),cov=sum(Object.values(dec.capital_by_level_bn));
 return {engine:ev.capital.total_bn,reporter,coverage:cov};}
function pensionChanges(t,end,which){
 const d={oasdi_union:0,oasdi_original_descendants:0,oasdi_item10_reporters:0,oasdi_item10_native_children:0,oasdi_item12_coverage:0,
 part_a_union:0,part_a_original_descendants:0,part_a_item10_reporters:0,part_a_item10_native_children:0,part_a_item12_coverage:0};
 if(which==="cash")return d;
 d.oasdi_union=t.next.unionSS-t.old.unionSS;
 d.part_a_union=t.next.unionPA-t.old.unionPA;
 d.oasdi_original_descendants=orig.accrual*(t.fss-1);d.part_a_original_descendants=orig.part_a*(t.fpa-1);
 d.oasdi_item10_reporters=reporter(end,"social_security")*(t.pooledSS-1);
 d.part_a_item10_reporters=reporter(end,"medicare")*(t.pooledPA-1);
 d.oasdi_item10_native_children=native.ss*(t.fss-1);d.part_a_item10_native_children=native.pa*(t.fpa-1);
 for(const p of coverage(which,end).line_parts){
   if(p.category!=="pension_accrual")continue;
   check(`known coverage accrual source ${p.source_line}`,["social_security","medicare"].includes(p.source_line));
   let factor;
   if(p.line.startsWith("native_child_"))factor=p.source_line==="social_security"?t.fss:t.fpa;
   else if(p.line.startsWith("union_completion_"))factor=p.source_line==="social_security"?t.pooledSS:t.pooledPA;
   else factor=p.source_line==="social_security"?t.generationSS[p.generation]:t.generationPA[p.generation];
   check(`coverage pension ${p.line}`,Number.isFinite(factor));
   d[p.source_line==="social_security"?"oasdi_item12_coverage":"part_a_item12_coverage"]+=p.coverage_bn*(factor-1);
 }
 return d;
}
function writeCsv(file,rows){const h=Object.keys(rows[0]);const enc=x=>{const s=String(x??"");return /[,"\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};fs.writeFileSync(file,[h.join(","),...rows.map(r=>h.map(k=>enc(r[k])).join(","))].join("\n")+"\n");}
function build(rates){const results=[],components=[],baselines=[];
 const arms=[{arm:"unchanged",rate:null},{arm:"A",rate:null},{arm:"B",rate:null},
 {arm:"both_lowrate",rate:.02,spec:11},{arm:"both_highrate",rate:.03,spec:11}];
 const transfers=Object.fromEntries(["unchanged","flat_2","flat_3"].map(k=>[k,repricing(rates,k)]));
 for(const which of ["set","cash"]){const api=which==="set"?P:P.CASH;
  for(const end of ["low","high"]){const ix=end==="low"?16:11,sp=api.MAIN_SPECS[ix],oldRate=end==="low"?.02:.03;
   const evaluated=P.METHODS.map(method=>{const m=api.modelFor("central",method,api.withCentral({}));return api.evaluateFull(m,sp,P.MAIN_PROFILE);});
   const base=sum(evaluated.map(r=>r.cost_bn))/evaluated.length;
   const capital=Object.fromEntries(["engine","reporter","coverage"].map(k=>[k,sum(evaluated.map(r=>capitalOf(r,end,which)[k]))/evaluated.length]));
   baselines.push({which,end,specification:ix,cost_bn:base,capital});
   for(const a of arms){if(a.spec!==undefined&&a.spec!==ix)continue;
    const rate=a.arm==="B"?rates.trustees_capital.flat_real_equivalent:a.rate??oldRate;
    const label=a.arm==="A"?(end==="low"?"flat_2":"flat_3"):a.arm.startsWith("both_")?(rate===.02?"flat_2":"flat_3"):"unchanged";
    const ds=pensionChanges(transfers[label],end,which);
    ds.retiree_health_external=0;ds.public_pensions_external=0;
    for(const [k,v]of Object.entries(capital))ds[`capital_${k}`]=v*(rate/oldRate-1);
    const delta=sum(Object.values(ds)),total=base+delta;
    const oasdi=sum(Object.entries(ds).filter(([k])=>k.startsWith("oasdi_")).map(([,v])=>v));
    const partA=sum(Object.entries(ds).filter(([k])=>k.startsWith("part_a_")).map(([,v])=>v));
    const cap=sum(Object.entries(ds).filter(([k])=>k.startsWith("capital_")).map(([,v])=>v));
    check("component closure",near(oasdi+partA+cap,delta));
    const result={arm:a.arm,which,end,specification:ix,real_rate:rate,baseline_bn:base,oasdi_delta_bn:oasdi,part_a_delta_bn:partA,
      capital_delta_bn:cap,delta_bn:delta,cost_bn:total,per_member_usd:total*1e9/payload.meta.population_v8.with_coverage,
      delta_per_member_usd:delta*1e9/payload.meta.population_v8.with_coverage};
    results.push(result);for(const [component,delta_bn]of Object.entries(ds))components.push({arm:a.arm,which,end,specification:ix,component,delta_bn,delta_per_member_usd:delta_bn*1e9/payload.meta.population_v8.with_coverage});
    if(a.arm==="unchanged")check("unchanged delta zero",delta===0);
   }
  }
 }
 const expected=read("main_case_2026_10_15/derived/summary.json").v8;
 for(const b of baselines){const want=(b.which==="set"?expected.band_bn:expected.cash_set_bn)[b.end==="low"?0:1];check("unchanged v8 end 1e-6",near(b.cost_bn,want,1e-6));}
 for(const b of baselines.filter(b=>b.which==="set"))check("frozen corrected-v8 baseline",near(b.cost_bn,b.end==="low"?365.791930255:455.981784589,1e-6));
 return {results,components,baselines,native,original_descendants:orig,transfers,
   method:"Additive revaluation of the existing accrual amounts, preserving the case's normalized generation split and fixed G3/white age profiles; item10 reporter own-record profile shares and item12 coverage profiles retain their source calibration. B/D, current benefit taxes and all other amounts are fixed.",
   basis:{pre_v8:"within_group_distribution_2026_09_29/_cache/oct14/lines.json",scope:"historical pre-v8 generation and original-descendant split, used only for pension valuation coefficients",external_accruals:"retiree health and public pension normal costs are external booked inputs; this account does not compute their present values"},
   gates:{unchanged_v8_ends:true,component_closure:true,union_and_pooled_generation_closure:true}};
}
module.exports={build,repricing,pensionChanges,native};
if(require.main===module){const arg=n=>{const i=process.argv.indexOf(n);return i<0?null:process.argv[i+1];};
 const ratePath=arg("--rates")||path.join(__dirname,"derived/rates.json"),out=arg("--out")||path.join(__dirname,"derived");
 const started=performance.now(),r=build(JSON.parse(fs.readFileSync(ratePath,"utf8")));fs.mkdirSync(out,{recursive:true});
 fs.writeFileSync(path.join(out,"results.json"),JSON.stringify(r,null,2)+"\n");writeCsv(path.join(out,"arms.csv"),r.results);writeCsv(path.join(out,"components.csv"),r.components);
 console.log(JSON.stringify({rows:r.results.length,gates:r.gates,elapsed_seconds:(performance.now()-started)/1000,max_rss_kib:process.resourceUsage().maxRSS}));}
