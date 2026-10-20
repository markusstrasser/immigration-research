/* Principal v8 item declarations for the oct16 signed person-price replay. */
"use strict";
const fs=require("fs"),path=require("path");
const B=require("../main_case_2026_10_15/package.cjs"),S=require("../spending_keys_r5_2026_10_15/items.cjs"),T=require("../consumption_tax_bases_r5_2026_10_15/item.cjs");
const read=p=>JSON.parse(fs.readFileSync(path.join(__dirname,"..",p),"utf8"));
function build(){
 const sets={};
 const military=read("spending_keys_r5_2026_10_15/derived/item13.json");
 require("./readiness.cjs").requireItem13();
 const stub13=process.env.ITEM13_PHASE==="step1";
 for(const which of ["set","cash"]){
  const api=which==="set"?B:B.CASH,posts={};
  for(const n of [14,15])Object.assign(posts,S.buildItem(n,{B},null,which).meta);
  if(military.extension)Object.assign(posts,S.buildItem(13,{B},stub13?"compensation_only":null,which).meta);
  Object.assign(posts,T.build({B},"household_joint",which).meta);
  const ends={};
  for(const end of ["low","high"]){
   const r=api.evaluateFull(api.payloadModel(),api.MAIN_SPECS[end==="low"?16:11],api.MAIN_PROFILE);
   ends[end]={capital:r.capital.components,coverage:api.POST_ENGINE.coverage.by_end[end]};
  }
  sets[which]={posts,ends};
 }
 return {sets,military:{...military,extension:stub13?{...military.extension,lines:[]}:military.extension},stub13,
  rate:read("one_rate_2026_10_15/derived/rates.json").trustees_capital.flat_real_equivalent};
}
module.exports={build};
if(require.main===module)process.stdout.write(JSON.stringify(build())+"\n");
