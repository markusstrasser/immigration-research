/* New oct16 outputs only. Node maxRSS is diagnostic; physical footprint gates. */
"use strict";
const fs=require("fs"),path=require("path"),V=require("./v9_split.cjs"),P=require("../main_case_2026_10_16/package.cjs");
const argv=process.argv.slice(2),arg=(k,d)=>argv.includes(k)?argv[argv.indexOf(k)+1]:d;
const CASE=arg("--case","oct16"),which=CASE==="oct16"?"set":CASE==="oct16_cash"?"cash":null;
if(!which)throw Error("[BLOCKED] --case must be oct16 or oct16_cash");
const api=which==="set"?P:P.CASH,OUT=path.resolve(arg("--out-dir",path.join(__dirname,"derived"))),start=performance.now();
const all=api.MAIN_SPECS.map(s=>api.evaluateFull(api.payloadModel(),s,api.MAIN_PROFILE).cost_bn),ends=[all.indexOf(Math.min(...all)),all.indexOf(Math.max(...all))];
const summary={case:CASE,set:which,lane:P.LANE,payload:`${P.LANE}/derived/corrections${which==="cash"?"_cash":""}.json`,specifications:{low_index:ends[0],high_index:ends[1]},union:{cost_bn:ends.map(i=>all[i]),population:api.POPULATION_V9.with_coverage},conventions:{},routing:{selected_items:P.CANDIDATE,new_posts:"declared selected16/17 generation parts; optional19 routes added_G3plus only when selected beside; other line/capital sources follow existing generation source amounts at each specification"},gates:{all_specifications_close:true}};
const rows=[],payloads={};
for(const convention of ["a","b"]){
 const values=api.MAIN_SPECS.map(s=>V.generationParts(api,s,convention));
 const frozen=JSON.parse(fs.readFileSync(path.join(__dirname,`derived/generation_summary_oct15${which==="cash"?"_cash":""}.json`),"utf8"));
 summary.conventions[convention]={};payloads[convention]={};
 for(const g of V.GENS){
  const h=frozen.conventions[convention][g];let population=h.population;
  for(const id of ["native_minor_calibration","coverage_tenure"]){const z=api.POST_ENGINE[id];population+=(z?.observed_people_change_by_generation?.[g]||0)+(z?.coverage_people_change_by_generation?.[g]||0);}
  summary.conventions[convention][g]={population,adults:h.adults,cost_bn:ends.map(i=>values[i].costs[g]),own_span_bn:[Math.min(...values.map(v=>v.costs[g])),Math.max(...values.map(v=>v.costs[g]))]};
  const prior=JSON.parse(fs.readFileSync(path.join(__dirname,`derived/generation_corrections_oct15${which==="cash"?"_cash":""}.json`),"utf8")).payloads[convention][g];
  const unionMeta=api.correctionsPayload().meta,scoped={};
  for(const id of P.NEW_IDS){
   if(!unionMeta[id])continue;scoped[id]=JSON.parse(JSON.stringify(unionMeta[id]));
   if(scoped[id].by_end)for(const [k,end]of ["low","high"].entries()){
    const z=scoped[id].by_end[end];z.source_total_bn=z.total_bn;z.total_bn=values[ends[k]].posts[g][id]||0;
    if(z.by_generation_bn){z.source_by_generation_bn=z.by_generation_bn;z.by_generation_bn=Object.fromEntries(V.GENS.map(h=>[h,h===g?z.total_bn:0]));}
   }
  }
  payloads[convention][g]={...prior,edits:prior.edits.concat(values[0].extra_payloads[g].edits),
   meta:{...prior.meta,...scoped,items:unionMeta.items,case_key:"oct16",case_lane:P.LANE,generation:g,
    v9_posts_by_spec:values.map(v=>v.posts[g]),v9_cost_bn_by_spec:values.map(v=>v.costs[g]),
    v9_specs:api.MAIN_SPECS,source_v8:`generation_corrections_oct15${which==="cash"?"_cash":""}.json`,
    consumer_rule:"Engine.applyCorrections to original generation model; evaluate inherited v8 engine/capital/post amounts then add v9_posts_by_spec[spec]. Values include exactly the selected new post-engine items."}};
  ends.forEach((i,k)=>rows.push({convention,generation:g,band_end:k===0?"low":"high",specification:i,allocation:"personal",cost_bn:values[i].costs[g],population,adults:h.adults,per_member_usd:values[i].costs[g]*1e9/population,per_adult_usd:values[i].costs[g]*1e9/h.adults}));
 }
 const gap=V.X.sum(V.GENS.map(g=>summary.conventions[convention][g].population))-api.POPULATION_V9.with_coverage;
 if(Math.abs(gap)>1e-6)throw Error("[BLOCKED] oct16 generation population closure "+gap);
}
const peak=process.resourceUsage().maxRSS*1024;
require("../main_case_2026_10_16/memory_guard.cjs").requireWithinBudget("oct16 generation "+which);
fs.mkdirSync(OUT,{recursive:true});const h=Object.keys(rows[0]);
fs.writeFileSync(path.join(OUT,`generation_results_${CASE}.csv`),[h.join(","),...rows.map(r=>h.map(k=>r[k]).join(","))].join("\n")+"\n");
fs.writeFileSync(path.join(OUT,`generation_summary_${CASE}.json`),JSON.stringify(summary,null,1)+"\n");
fs.writeFileSync(path.join(OUT,`generation_corrections_${CASE}.json`),JSON.stringify({meta:{case:CASE,source:"run_generations_v9.cjs",layout:"full inherited oct15 generation payload plus new engine edits and scoped new post amounts by specification; use generationParts for live evaluation"},payloads},null,1)+"\n");
console.log(`${CASE} PASS ${summary.union.cost_bn.join(" / ")}bn; elapsed ${(performance.now()-start)/1000}s; peakRSS ${peak/1e6}MB`);
