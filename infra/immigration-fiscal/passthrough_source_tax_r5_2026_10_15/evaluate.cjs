"use strict";
const fs=require("fs"),path=require("path");
const P=require("../main_case_2026_10_15/package.cjs"),I=require("./item.cjs");
const data=JSON.parse(fs.readFileSync(path.join(__dirname,"derived/item.json"),"utf8"));
const baseline=JSON.parse(fs.readFileSync(path.join(__dirname,"derived/v8.json"),"utf8"));
const mean=xs=>xs.reduce((a,b)=>a+b,0)/xs.length;
const rows=[];
for(const which of ["set","cash"]){
  const Q=which==="set"?P:P.CASH;
  const models=P.METHODS.map(method=>Q.modelFor("central",method,Q.withCentral({})));
  for(const [i,end] of ["low","high"].entries()){
    const spec=Q.MAIN_SPECS[[16,11][i]],without=mean(models.map(m=>Q.evaluateFull(m,spec).cost_bn));
    if(Math.abs(without-baseline.baseline[which][i])>1e-9)throw Error("[BLOCKED] baseline changed");
    for(const arm of Object.keys(data.arms)){
      const component=I.build({B:P},arm,which),delta=component.meta[I.id].by_end[end].total_bn;
      const withItem=mean(models.map(m=>Q.evaluateFull(m,spec).cost_bn+delta));
      if(Math.abs(withItem-without-delta)>1e-9)throw Error("[BLOCKED] item toggle mismatch");
      rows.push({which,end,arm,without_bn:without,with_bn:withItem,delta_cost_bn:withItem-without});
      console.log(`${which} ${end} ${arm} without=${without.toFixed(9)} with=${withItem.toFixed(9)} change=${(withItem-without).toFixed(9)}`);
    }
  }
}
fs.writeFileSync(path.join(__dirname,"derived/evaluations.json"),JSON.stringify(rows,null,2)+"\n");
