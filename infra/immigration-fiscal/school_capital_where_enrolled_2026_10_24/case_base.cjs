/* The adopted main case's (oct16) K-12 capital return to the group, by population part, at its end specifications.
   Read-only on the case. Writes the JSON named by argv[2] (build.py passes derived/case_base.json). */
"use strict";
const fs=require("fs"),path=require("path");
const FISCAL=path.join(__dirname,"..");
const P=require(path.join(FISCAL,"main_case_2026_10_16/package.cjs"));
const C=require(path.join(FISCAL,"main_case_2026_10_16/companions.cjs"));
const out=process.argv[2];
if(!out)throw Error("[BLOCKED] usage: node case_base.cjs <out.json>");
const live=JSON.parse(fs.readFileSync(path.join(FISCAL,"live_case.json"),"utf8"));
if(JSON.stringify(live).indexOf("oct16")<0)throw Error("[BLOCKED] live_case.json does not declare oct16");
if(P.CASE_KEY!=="oct16"||P.STATUS!=="adopted")throw Error("[BLOCKED] package is not the adopted oct16 case");
const K12=new Set(["k12","k12_user_fees"]),sum=a=>a.reduce((x,y)=>x+y,0),near=(a,b,t)=>Math.abs(a-b)<=t;
const summary=JSON.parse(fs.readFileSync(path.join(FISCAL,"main_case_2026_10_16/derived/summary.json"),"utf8")).v9;
const ends=summary.end_specifications.set; // [[low,high] per method]
const gates=[];const gate=(name,ok,detail)=>{gates.push({name,pass:!!ok,detail:String(detail)});if(!ok)throw Error("[BLOCKED] case_base gate "+name+": "+detail);};
const rows=[];
P.METHODS.forEach((method,mi)=>{
 const m=P.modelFor("central",method,P.withCentral({}));
 const mp=P.modelFor("central",method,P.withCentral({capital_variant:"k12_at_pupil_share"}));
 const pupilSpecs=P.specsFor({capital_variant:"k12_at_pupil_share"});
 ["low","high"].forEach((end,ei)=>{
  const i=ends[mi][ei],s=P.MAIN_SPECS[i],r=P.evaluateFull(m,s);
  gate(`${method}/${end} reading`,s.reading===end,s.reading);
  const r1=P.RATE.rateFor(P.POST_ENGINE.one_rate,s);
  const engine=r.capital.components.filter(c=>K12.has(c.id));
  const engine_bn=sum(engine.map(c=>c.return_bn));
  const stock=engine[0].stock_charged_bn;
  gate(`${method}/${end} one stock`,engine.every(c=>c.stock_charged_bn===stock&&c.response===1),JSON.stringify(engine));
  const completion=r.evaluation.spending.filter(l=>/^union_completion_k12/.test(l.id));
  const completion_bn=sum(completion.map(l=>l.amount_bn*l.response));
  // Coverage (item 12) and count parts (items 16, 17) are already priced at the one rate:
  // their one_rate interaction components are zero (checked below).
  const cov=P.POST_ENGINE.coverage.by_end[end].decomposition.line_parts.filter(q=>q.category==="capital"&&K12.has(q.source_line));
  const coverage_bn=sum(cov.map(q=>q.coverage_bn));
  const count={};
  for(const id of ["native_minor_calibration","coverage_tenure"])count[id]=sum(C.countParts(P.POST_ENGINE[id],end).filter(q=>q.category==="capital"&&K12.has(q.source_line)).map(q=>q.value_bn));
  const oneParts=(r.v9_post_engine.parts.one_rate||[]).filter(p=>/k12/.test(p.line||""));
  const byComp={};for(const p of oneParts)byComp[p.component]=(byComp[p.component]||0)+p.delta_bn;
  gate(`${method}/${end} coverage and count parts carry no rate interaction`,near(byComp.capital_own_coverage_rate_interaction||0,0,1e-12)&&near(byComp.capital_count_interaction||0,0,1e-12),JSON.stringify(byComp));
  const scaled=(engine_bn+completion_bn)*r1/s.rate;
  gate(`${method}/${end} one-rate deltas reproduce the rescaling`,near((byComp.capital_engine||0)+(byComp.capital_reporter||0),scaled-(engine_bn+completion_bn),1e-9),
   `${(byComp.capital_engine||0)+(byComp.capital_reporter||0)} vs ${scaled-(engine_bn+completion_bn)}`);
  const total=scaled+coverage_bn+count.native_minor_calibration+count.coverage_tenure;
  const rp=P.evaluateFull(mp,pupilSpecs[i]);
  const pupilKey=rp.capital.components.filter(c=>c.id==="k12").map(c=>c.key)[0];
  rows.push({method,end,specification:i,spec_rate:s.rate,one_rate:r1,stock_charged_bn:stock,
   engine_keys:Object.fromEntries(engine.map(c=>[c.id,c.key])),engine_return_at_spec_rate_bn:engine_bn,
   completion_lines:Object.fromEntries(completion.map(l=>[l.id,{amount_bn:l.amount_bn,response:l.response}])),
   completion_return_at_spec_rate_bn:completion_bn,coverage_capital_k12_bn:coverage_bn,count_capital_k12_bn:count,
   k12_return_at_one_rate_bn:total,effective_key:total/(stock*r1),pupil_share_key_variant:pupilKey,case_cost_bn:r.cost_bn});
 });
});
const band=summary.band_bn;
fs.writeFileSync(out,JSON.stringify({case_key:P.CASE_KEY,lane:P.LANE,status:P.STATUS,band_bn:band,end_specifications:ends,rows,gates},null,1)+"\n");
console.log("case_base: "+rows.map(r=>`${r.method}/${r.end} K-12 return ${r.k12_return_at_one_rate_bn.toFixed(4)}bn`).join("; "));
