/* Native signed source export. Read-only package use; no historical output replay. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const F=path.dirname(__dirname),C=path.join(F,"main_case_2026_10_16");
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
function build({probe=false}={}){
 const summary=JSON.parse(fs.readFileSync(path.join(C,"derived/summary.json"))),P=require(path.join(C,"package.cjs"));
 const live=JSON.parse(fs.readFileSync(path.join(F,"live_case.json")));
 if(!probe&&(live.key!=="oct16"||P.V9.STATUS!=="adopted"||summary.v9.status!=="adopted"))throw Error("[BLOCKED] oct16 case is not adopted");
 const out={case:"oct16",package_status:P.V9.STATUS,summary,sets:{},pins:{}};
 for(const f of ["package.cjs","derived/summary.json","derived/corrections.json","derived/corrections_cash.json","derived/main_case_bands.csv"])
  out.pins["main_case_2026_10_16/"+f]=hash(path.join(C,f));
 for(const basis of ["set","cash"]){
  const X=basis==="cash"?P.CASH:P,B=basis==="cash"?P.OCT15.CASH:P.OCT15;
  const payload=X.correctionsPayload(),disk=JSON.parse(fs.readFileSync(path.join(C,"derived",basis==="cash"?"corrections_cash.json":"corrections.json")));
  if(!probe&&JSON.stringify(payload)!==JSON.stringify(disk))throw Error("[BLOCKED] saved/native oct16 payload mismatch");
  const model=X.payloadModel(),oldModel=B.payloadModel();
  const runs=X.MAIN_SPECS.map((s,i)=>{
   const r=X.evaluateFull(model,s),old=B.evaluateFull(oldModel,s);
   return {spec:i,reading:s.reading,cost_bn:r.cost_bn,old_cost_bn:old.cost_bn,r,old};
  });
  const costs=runs.map(x=>x.cost_bn),indices=[costs.indexOf(Math.min(...costs)),costs.indexOf(Math.max(...costs))];
  out.sets[basis]={payload,old_payload:B.correctionsPayload(),specs:runs.map(({spec,reading,cost_bn,old_cost_bn})=>({spec,reading,cost_bn,old_cost_bn})),
    endpoints:Object.fromEntries(indices.map((i,j)=>[["low","high"][j],runs[i]])),band_bn:[Math.min(...costs),Math.max(...costs)],end_specifications:indices,
    capital_rates:[...new Set(X.MAIN_SPECS.map(s=>P.RATE.rateFor(payload.meta.one_rate,s)))]};
 }
 const memory=JSON.parse(cp.execFileSync("uv",["run","--no-project","python3",path.join(C,"memory_for_pid.py"),String(process.pid),String(process.resourceUsage().maxRSS)],{encoding:"utf8"}));
 if(!memory.pass)throw Error("[BLOCKED] oct16 frame physical-footprint budget");
 for(const [f,h]of Object.entries(out.pins))if(hash(path.join(F,f))!==h)throw Error("[BLOCKED] source changed during frame export");
 return out;
}
if(require.main===module){const out=process.argv[2];if(!out)throw Error("output path required");fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(build({probe:process.argv.includes("--probe")}))+"\n");}
module.exports={build};
