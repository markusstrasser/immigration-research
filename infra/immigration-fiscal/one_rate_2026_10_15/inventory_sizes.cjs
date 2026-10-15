"use strict";
const path=require("path");
const P=require(path.resolve("infra/immigration-fiscal/main_case_2026_10_15/package.cjs"));
const out={baseline:{set:P.central({}),cash:P.CASH.central({})},arms:{}};
for(const arm of ["rho_one","rho_high"]){
  const Q=P.caseOf(P.OCT05,P.CANDIDATE,{retiree_health:arm});
  out.arms[arm]={set:Q.central({}),cash:Q.CASH.central({})};
  for(const b of ["set","cash"])
    out.arms[arm][`${b}_delta`]=out.arms[arm][b].map((n,i)=>n-out.baseline[b][i]);
}
console.log(JSON.stringify(out,null,2));
