/* Source controls and v9 rate-arm accounting, with the selected joint count contract. */
"use strict";
const fs=require("fs"),path=require("path"),P=require("./package.cjs"),R=require("./item_rate.cjs");
const sum=a=>a.reduce((x,y)=>x+y,0),checks=[],start=performance.now();
function gate(check,pass,detail){checks.push({check,pass:!!pass,detail});if(!pass)throw Error("[BLOCKED] rate check: "+check+" "+JSON.stringify(detail));}
const near=(a,b,t=1e-9)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<t;
const csvCache=new Map();
function rawCountRows(file){if(!csvCache.has(file)){const rows=fs.readFileSync(path.join(__dirname,"..",file),"utf8").trimEnd().split("\n").map(x=>x.split(",")),h=rows.shift();csvCache.set(file,rows.map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]]))));}return csvCache.get(file);}
function sourceFactor(p,t){const ss=p.source_line==="social_security";return p.line.startsWith("native_child_")?(ss?t.fss:t.fpa):p.line.startsWith("union_completion_")?(ss?t.pooledSS:t.pooledPA):(ss?t.generationSS:t.generationPA)[p.generation];}
const rows={};
for(const arm of ["B","A","both_highrate"]){
 const Q=P.caseOf(P.OCT05,P.V8_PACKAGE.CANDIDATE.concat(["one_rate"]),{one_rate:arm});
 for(const which of ["set","cash"]){
  const X=which==="set"?Q:Q.CASH;
  for(const [end,i]of [["low",16],["high",11]]){
   const want=R.results.results.find(r=>r.arm===arm&&r.which===which&&r.end===end);
   if(!want)continue;
   const got=sum(P.METHODS.map(method=>X.evaluateFull(X.modelFor("central",method,X.withCentral({})),X.MAIN_SPECS[i]).cost_bn))/P.METHODS.length;
   gate(`source-owned ${arm}/${which}/${end}`,near(got,want.cost_bn,1e-6),{got,want:want.cost_bn});
  }
 }
}
for(const arm of ["B","A","v8","both_highrate","capital_7pct"]){
 const Q=P.caseOf(P.OCT05,P.CANDIDATE,{one_rate:arm}),entry={};
 for(const which of ["set","cash"]){
  const X=which==="set"?Q:Q.CASH,m=X.payloadModel(),runs=[16,11].map(i=>X.evaluateFull(m,X.MAIN_SPECS[i]));
  entry[which]=runs.map(r=>r.cost_bn);
  for(const [end,k]of [["low",0],["high",1]]){
   const r=runs[k],parts=r.v9_post_engine.parts.one_rate,of=component=>sum(parts.filter(p=>p.component===component).map(p=>p.delta_bn));
   gate(`${arm}/${which}/${end} component closure`,near(sum(parts.map(p=>p.delta_bn)),r.v9_post_engine.amounts.one_rate));
   if(P.COVERAGE_MODE==="repriced"){
    const spec=X.MAIN_SPECS[k?11:16],target=R.rateFor(X.POST_ENGINE.one_rate,spec),cap=X.POST_ENGINE.coverage.by_end[end].decomposition.line_parts.filter(p=>p.source_side==="capital");
    gate(`${arm}/${which}/${end} own coverage rate`,near(of("capital_own_coverage_rate_interaction"),sum(cap.map(p=>p.coverage_bn))*(target/R.RATE-1)));
    if(arm!=="B")gate(`${arm}/${which}/${end} coverage included`,Math.abs(of("capital_own_coverage_rate_interaction"))>1e-6);
    const a=X.POST_ENGINE.native_minor_calibration,b=X.POST_ENGINE.coverage_tenure;
    gate(`${arm}/${which}/${end} joint count source contract`,a.parts_file===b.parts_file&&b.parts_scenario==="joint"&&b.subtract_parts_scenario===a.parts_scenario);
    const joint=rawCountRows(b.parts_file).filter(p=>p.scenario==="joint"&&p.end===end);
    const capitalJoint=sum(joint.filter(p=>p.economic_class==="capital_return").map(p=>Number(p.change_bn)))*(target/R.RATE-1);
    gate(`${arm}/${which}/${end} count capital equals joint, not standalone stack`,near(of("capital_count_interaction"),capitalJoint));
    if(which==="set"&&["A","both_highrate"].includes(arm)){
     const t=R.results.transfers[arm==="A"&&end==="low"?"flat_2":"flat_3"];
     const pensionJoint=sum(joint.filter(p=>p.category==="pension_accrual").map(p=>Number(p.change_bn)*(sourceFactor(p,t)-1)));
     gate(`${arm}/${end} count pension equals joint, not standalone stack`,near(of("pension_count_interaction"),pensionJoint));
    }
   }
   if(which==="cash")gate(`${arm}/${end} cash has no pension revaluation`,parts.every(p=>!p.component.startsWith("pension_")&&!p.component.startsWith("oasdi_")&&!p.component.startsWith("part_a_")));
   else if(["A","both_highrate"].includes(arm)){
    gate(`${arm}/${end} count pension interaction included`,Math.abs(of("pension_count_interaction"))>1e-6);
    const ids=new Set(parts.filter(p=>p.component==="pension_count_interaction").map(p=>p.item));
    gate(`${arm}/${end} selected16 and conditional17 both routed`,ids.has("native_minor_calibration")&&ids.has("coverage_tenure"));
   }
   if(arm==="B"&&P.COVERAGE_MODE==="repriced")gate(`${which}/${end} defaultB retains kernel rate`,of("capital_own_coverage_rate_interaction")===0&&of("capital_count_interaction")===0);
  }
 }
 rows[arm]=entry;
}
const transfer=R.results.transfers.flat_3;
gate("native child uses own G3 factor, not pooled reporter factor",R.pensionFactor({line:"native_child_spending_social_security",source_line:"social_security",generation:"G3plus"},transfer)===transfer.fss);
gate("reporter uses pooled source factor",R.pensionFactor({line:"union_completion_social_security_social_security",source_line:"social_security",generation:"G3plus"},transfer)===transfer.pooledSS);
const output={case:P.CASE_KEY,stub13:P.STUB13,coverage_mode:P.COVERAGE_MODE,checks,arms:rows,
 residuals:{imported_public_pensions_and_opeb:"held at booked valuations",item15_alternative_coverage:"central response prices carried; capital rate itself revalued",lineage_and_DA_count_items:"central16/17 source kernel carried across options",noncentral_lineage_flat_rate_pension:"source-v8 original-descendant pension transfer held in A/3-percent arms; defaultB pension unchanged"}};
const outIndex=process.argv.indexOf("--out"),out=path.resolve(outIndex<0?path.join(__dirname,"derived/rate_check.json"):process.argv[outIndex+1]);
if(!out.startsWith(__dirname+path.sep))throw Error("[BLOCKED] rate check output must stay in v9 lane");
fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(output,null,1)+"\n");
console.log(JSON.stringify({checks:checks.length,arms:rows,elapsed_seconds:(performance.now()-start)/1000,max_rss_kib:process.resourceUsage().maxRSS}));
