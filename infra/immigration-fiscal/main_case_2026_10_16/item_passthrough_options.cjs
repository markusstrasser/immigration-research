/* Reuse the source item's dollar coefficients and sufficient wage-key vectors.
 * This is job_keys.py:132's declared union + G3/white lineage-rate composition,
 * evaluated at the supplied case's already-built lineage wage rates. */
"use strict";
const fs=require("fs"),path=require("path"),clone=x=>JSON.parse(JSON.stringify(x));
const file="passthrough_source_tax_r5_2026_10_15/derived/job_keys.json";
const source=JSON.parse(fs.readFileSync(path.join(__dirname,"..",file),"utf8"));
const snapshot=JSON.parse(fs.readFileSync(path.join(__dirname,"../passthrough_source_tax_r5_2026_10_15/derived/v8.json"),"utf8"));
const forms={owner_federal_s_corporation:"3",owner_federal_partnership:"4",owner_federal_sole_proprietor:"5"};
const fail=s=>{throw Error("[BLOCKED] pass-through option: "+s);};
const sum=a=>a.reduce((x,y)=>x+y,0),close=(a,b)=>Math.abs(a-b)<1e-12;
function reprice(built,base){
 const wage=base.correctionsPayload().meta.job_capital_taxes?.lineage?.wage_share;
 if(!wage||!Number.isFinite(wage.g3plus?.personal)||!Number.isFinite(wage.whites?.personal))fail("case lacks declared G3/white wage rates");
 // core.py:142-143 divides each lineage wage share by a fixed source group
 // denominator. Recover that same denominator from its pinned canonical rate.
 const current={G3plus:source.lineage_rates.G3plus*wage.g3plus.personal/snapshot.lineage_rates.g3plus.personal,
  white:source.lineage_rates.white*wage.whites.personal/snapshot.lineage_rates.whites.personal};
 const same=["G3plus","white"].every(g=>close(current[g],source.lineage_rates[g]));
 // Canonical numbers and serialized source material stay byte-for-byte owned
 // by the producer; the source's own standalone gate remains the positive control.
 if(same)return built;
 const mode=process.env.V9_PASS_OPTION||"reprice";
 if(!["reprice","held"].includes(mode))fail("unknown V9_PASS_OPTION");
 const out=clone(built),block=out.meta.passthrough_source_tax;
 block.lineage_option={mode,source_rates:clone(source.lineage_rates),case_rates:clone(current),source:file,
  rule:"source dollar coefficient times the source's union + case G3/white wage-rate sufficient-statistic composition; observed union and completion keys held"};
 if(mode==="held"){
  block.lineage_option.held_added_cost_bn=Object.fromEntries(["low","high"].map(end=>[end,block.by_end[end].by_generation_bn.added_G3plus]));
  return out;
 }
 for(const end of ["low","high"]){
  const row=block.by_end[end],rep=Array(161).fill(0),before=row.total_bn;
  for(const part of row.parts_by_line){
   const form=forms[part.line],key=(part.naics.includes("+")?source.pooled_shares:source.shares)[part.naics]?.[form];
   if(!key||key.lineage.length!==161||!close(key.lineage[0],part.lineage_key))fail(`source key identity ${part.line}/${part.naics}`);
   const original=key.union[0]+sum(["G3plus","white"].map(g=>source.lineage_rates[g]*key[g][0]));
   if(!close(original,part.lineage_key))fail("canonical sufficient statistic differs from item source");
   if(part.lineage_key===0){if(part.base_cost_bn!==0)fail("zero source coefficient denominator");continue;}
   const coefficient=part.base_cost_bn/part.lineage_key;
   const next=key.union.map((v,i)=>v+sum(["G3plus","white"].map(g=>current[g]*key[g][i])));
   const totalRatio=(next[0]+part.completion_key)/(part.lineage_key+part.completion_key);
   for(const name of ["source_receipt_cost_bn","replacement_receipt_cost_bn","state_source_cost_bn"])part[name]*=totalRatio;
   part.source_lineage_key=part.lineage_key;part.lineage_key=next[0];
   part.base_cost_bn=coefficient*next[0];part.total_bn=part.base_cost_bn+part.completion_cost_bn;
   for(let i=0;i<161;i++)rep[i]+=coefficient*next[i]+part.completion_cost_bn;
  }
  row.total_bn=sum(row.parts_by_line.map(p=>p.total_bn));
  row.by_generation_bn.added_G3plus=row.total_bn-sum(["G1","G2","G3plus"].map(g=>row.by_generation_bn[g]));
  row.cps_conditional_se_bn=Math.sqrt(4/160*sum(rep.slice(1).map(v=>(v-rep[0])**2)));
  row.lineage_option_delta_bn=row.total_bn-before;
  if(Math.abs(row.total_bn-sum(Object.values(row.by_generation_bn)))>1e-9||Math.abs(row.total_bn-rep[0])>1e-9)fail("option line/generation/replicate closure");
 }
 return out;
}
module.exports={reprice};
