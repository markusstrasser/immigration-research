/* Beside only: source-owned item19 and W09 dollars evaluated over v9 specs.
 * Adding their deltas is a naive pair, not a solved legal-form counterfactual. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const sum=a=>a.reduce((x,y)=>x+y,0),mean=a=>sum(a)/a.length;
function build(P,{run,gate}){
 const file=path.join(__dirname,"../passthrough_source_tax_r5_2026_10_15/derived/w09.json");
 const bytes=fs.readFileSync(file),source=JSON.parse(bytes);
 const ids=P.CANDIDATE.filter(id=>id!==P.PASS.id);
 const taxIds=P.REGISTRY.filter(x=>ids.includes(x.id)||x.id===P.PASS.id).map(x=>x.id);
 const B=P.caseOf(P.OCT05,ids),T=P.caseOf(P.OCT05,taxIds);
 const readings=Object.fromEntries(["item19","w09_frozen","w09_extension","naive_pair_frozen","naive_pair_extension"].map(k=>[k,{}]));
 const sourceParts={};
 for(const which of ["set","cash"]){
  const X=which==="cash"?B.CASH:B,Y=which==="cash"?T.CASH:T;
  const base=run(B,which),tax=run(T,which);
  sourceParts[which]=source[which];
  for(const [i,end]of ["low","high"].entries()){
   const z=source[which][end];
   gate(`W09 ${which}/${end} source extension closes`,Math.abs(z.union_and_v6_descendants_bn+z.completion_G3_profile_proxy_bn+z.coverage_generation_profile_proxy_bn-z.total_bn)<1e-9);
   gate(`W09 ${which}/${end} frozen source oracle`,Math.abs(z.union_and_v6_descendants_bn-[3.2952991232200546,1.2192606755914202][i])<1e-9);
   gate(`W09 ${which}/${end} extension source oracle`,Math.abs(z.total_bn-[3.4038730196547764,1.2594330172722672][i])<1e-9);
  }
  for(const [name,out]of Object.entries(readings)){
   const pair=name.startsWith("naive_pair"),hasTax=pair||name==="item19";
   const rr=hasTax?tax:base,api=hasTax?Y:X;
   const amount=s=>name==="item19"?0:source[which][s.reading][name.endsWith("frozen")?"union_and_v6_descendants_bn":"total_bn"];
   const costs=rr.costs.map(a=>a.map((v,i)=>v+amount(rr.specs[i])));
   const indexes=costs.map(a=>[a.indexOf(Math.min(...a)),a.indexOf(Math.max(...a))]);
   const band=[0,1].map(e=>mean(costs.map((a,k)=>a[indexes[k][e]])));
   const numbered=api.specsFor({allocation:"all"});
   const ends=indexes.map(ix=>ix.map(i=>numbered.findIndex(s=>JSON.stringify(s)===JSON.stringify(rr.specs[i]))));
   const parts=[0,1].map(e=>{
    const item19=hasTax?mean(indexes.map((ix,k)=>tax.costs[k][ix[e]]-base.costs[k][ix[e]])):0;
    const w09=mean(indexes.map(ix=>amount(rr.specs[ix[e]])));
    const baseline=mean(indexes.map((ix,k)=>base.costs[k][ix[e]]));
    gate(`legal-form ${name}/${which}/${e} exact parts closure`,Math.abs(baseline+item19+w09-band[e])<1e-9);
    return {item19_bn:item19,w09_bn:w09,sum_bn:item19+w09,baseline_at_selected_ends_bn:baseline};
   });
   out[which]={band_bn:band,delta_from_v9_without_item19_bn:band.map((v,i)=>v-base.band[i]),ends,parts_at_ends:parts};
  }
 }
 return {label:"item 6 legal-form pair",central:false,naive_pair:true,jointly_solved:false,
  item19_arm:P.ITEM19_ARM,source:"passthrough_source_tax_r5_2026_10_15/derived/w09.json",sha256:crypto.createHash("sha256").update(bytes).digest("hex"),
  rule:"Each delivered post-engine arm is evaluated on every v9 personal specification in both methods, set and cash; ends are searched again. Pair means source19 + W09 dollars, not a jointly solved legal-form/owner counterfactual.",
  coverage:"v9 central own-price coverage/count kernel carried. W09 frozen covers its original union and descendants. W09 extension carries its delivered item10 G3-profile and item12 generation-profile dollar proxies unchanged; no own-v9 legal-form re-key of16/17 or missing people is identified.",
  source_parts:sourceParts,readings};
}
module.exports={build};
