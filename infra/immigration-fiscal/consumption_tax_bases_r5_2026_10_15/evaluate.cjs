/* Evaluate adopted v8 with/without each item18 arm; never build a v9 case. */
"use strict";
const fs=require("fs"),path=require("path");
const P=require("../main_case_2026_10_15/package.cjs"),I=require("./item.cjs");
const HERE=__dirname,mean=a=>a.reduce((s,n)=>s+n,0)/a.length;
const close=(a,b)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<1e-9;
const fail=s=>{throw Error("[BLOCKED] item18 evaluate: "+s);};
function apply(X,m,built){return P.Engine.applyCorrections(m,{lines:[],receipt_lines:[],edits:built.editsAt(m),meta:m.corrections});}
function evaluate() {
  const source=JSON.parse(fs.readFileSync(path.join(HERE,"derived/item.json"),"utf8"));
  const arms=Object.keys(source.arms),records=[],payloads={};
  for(const which of ["set","cash"]) {
    const X=which==="set"?P:P.CASH,models=P.METHODS.map(method=>X.modelFor("central",method,X.withCentral({})));
    const base=models.map(m=>X.MAIN_SPECS.map(s=>X.cost(m,s)));
    const band=[0,1].map(e=>mean(base.map(v=>e?Math.max(...v):Math.min(...v))));
    const want=which==="set"?[365.791930,455.981785]:[281.752564,371.942418];
    if(band.some((n,i)=>Math.abs(n-want[i])>1e-6))fail("v8 unchanged gate "+which);
    console.log("v8 unchanged "+which+" "+band.map(n=>n.toFixed(9)).join(" / "));
    payloads[which]={};
    for(const arm of arms) {
      const built=I.build({B:P},arm,which);
      payloads[which][arm]={...built};delete payloads[which][arm].editsAt;
      const values=models.map((m,k)=>{
        const changed=apply(X,m,built);
        for(const id of Object.keys(source.arms[arm].receipt_ratios)) {
          const old=m.receipts.lines.find(l=>l.id===id),now=changed.receipts.lines.find(l=>l.id===id);
          if(old.national_bn!==now.national_bn)fail("national line changed "+id);
          for(const sc of m.receipts.scenarios)for(const a of ["personal","shared"]) {
            const x=old.cells[sc][a],y=now.cells[sc][a];
            if(!close(x.target_bn+x.other_bn,y.target_bn+y.other_bn))fail("national cell conservation "+id);
          }
        }
        return X.MAIN_SPECS.map((s,i)=>{
          const r=X.evaluateFull(changed,s),post=built.meta[I.ID].by_end[s.reading].total_bn;
          return {cost:r.cost_bn+post,base:base[k][i],post,engine:r.cost_bn-base[k][i]};
        });
      });
      const endix=values.map(v=>[v.findIndex(x=>x.cost===Math.min(...v.map(x=>x.cost))),v.findIndex(x=>x.cost===Math.max(...v.map(x=>x.cost)))]);
      for(const [e,end] of ["low","high"].entries()) {
        const runs=values.map((v,k)=>v[endix[k][e]]),cost=mean(runs.map(r=>r.cost)),delta=cost-band[e];
        const row={arm,which,end,baseline_bn:band[e],cost_bn:cost,delta_bn:delta,
          delta_per_member_usd:delta*1e9/source.population.with_coverage,
          engine_delta_bn:mean(runs.map(r=>r.engine)),coverage_delta_bn:mean(runs.map(r=>r.post)),
          end_indices:endix.map(ix=>ix[e]),item11_delta_bn:null};
        if(!close(row.delta_bn,row.engine_delta_bn+row.coverage_delta_bn))fail("delta parts do not close");
        records.push(row);
        console.log(`${which} ${arm} ${end} delta ${delta.toFixed(9)}bn`);
      }
    }
  }
  const out={identification_status:source.identification_status,central_delta_bn:null,population:source.population,records};
  fs.writeFileSync(path.join(HERE,"derived/evaluation.json"),JSON.stringify(out,null,2)+"\n");
  fs.writeFileSync(path.join(HERE,"derived/item_payloads.json"),JSON.stringify(payloads,null,2)+"\n");
  const header=["arm","which","end","baseline_bn","cost_bn","delta_bn","delta_per_member_usd","engine_delta_bn","coverage_delta_bn","item11_delta_bn","end_indices"];
  fs.writeFileSync(path.join(HERE,"derived/evaluation.csv"),[header.join(","),...records.map(r=>header.map(h=>h==="end_indices"?r[h].join(";"):r[h]??"").join(","))].join("\n")+"\n");
  return out;
}
if(require.main===module)evaluate();
module.exports={evaluate,apply};
