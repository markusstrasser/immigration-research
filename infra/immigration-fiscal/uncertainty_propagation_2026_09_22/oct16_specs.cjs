/* Read-only principal values and source coefficients for the live oct16 sampling route. */
// Native-First: evaluate the immutable case and generation source models directly.
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const HERE=__dirname,FISCAL=path.dirname(HERE),ROOT=path.resolve(FISCAL,"../..");
const read=p=>JSON.parse(fs.readFileSync(path.join(FISCAL,p),"utf8"));
const fail=s=>{throw Error("[BLOCKED] oct16 sampling source: "+s);};
const CACHE=path.join(HERE,"_cache/oct16/spec_sources.json"),MANIFEST=path.join(HERE,"derived/oct16/spec_sources_manifest.json");
function loadSources(cache=CACHE,manifest=MANIFEST){
 if(!fs.existsSync(manifest))fail("source manifest missing; run sept24_specs.cjs");
 const pin=JSON.parse(fs.readFileSync(manifest,"utf8"));
 if(pin.path!==path.relative(ROOT,CACHE))fail("source cache path differs from manifest");
 if(!fs.existsSync(cache))fail("source cache missing; run sept24_specs.cjs");
 const bytes=fs.readFileSync(cache);
 if(bytes.length!==pin.bytes||crypto.createHash("sha256").update(bytes).digest("hex")!==pin.sha256)fail("source cache differs from tracked manifest");
 return JSON.parse(bytes);
}
function writeSources(){
 const bytes=Buffer.from(JSON.stringify(build(),null,1)+"\n");
 fs.mkdirSync(path.dirname(CACHE),{recursive:true});
 fs.writeFileSync(CACHE,bytes);
 writeSourceManifest(bytes);
}
function writeSourceManifest(bytes){
 fs.mkdirSync(path.dirname(MANIFEST),{recursive:true});
 fs.writeFileSync(MANIFEST,JSON.stringify({path:path.relative(ROOT,CACHE),bytes:bytes.length,
  sha256:crypto.createHash("sha256").update(bytes).digest("hex"),rebuild:"node infra/immigration-fiscal/uncertainty_propagation_2026_09_22/sept24_specs.cjs"},null,2)+"\n");
}
function pinCachedSources(){
 if(!fs.existsSync(CACHE))fail("source cache missing; cannot pin byte custody");
 writeSourceManifest(fs.readFileSync(CACHE));
}
function validateAdoption(live,payload){
 if(live.key!=="oct16"||live.lane!=="main_case_2026_10_16")fail("oct16 is not the declared adopted live case");
 if(payload.meta?.adopted!=="2026-10-20"||!payload.meta?.status?.startsWith("adopted: main case v9")||payload.meta?.v9?.stub13!==false)fail("adopted non-STUB payload required");
}
function anchorSpecs(summary,basis){
 const byMethod=summary.end_specifications?.[basis],ends=byMethod?.[0];
 if(!Array.isArray(ends)||ends.length!==2||!ends.every(Number.isInteger)||ends[0]===ends[1]
  ||!byMethod.every(row=>JSON.stringify(row)===JSON.stringify(ends)))fail("source anchors require common authoritative method ends");
 return ends;
}
function cashOracleDifferences(rows,sourceRows,name,allocation){
 if(allocation!=="personal"||sourceRows.length!==32||sourceRows.some((r,i)=>r.spec!==i||!Number.isFinite(r.cost_bn)||!Number.isFinite(r.capital_bn)))fail("cash oracle requires all32 ordered finite personal specifications");
 const differences=rows.flatMap((r,i)=>r.allocation!==allocation?[]:!Number.isFinite(r[name])||!Number.isFinite(r[`capital_${name}`])?[NaN]:[
  Math.abs(r[name]-sourceRows[i]?.cost_bn),Math.abs(r[`capital_${name}`]-sourceRows[i]?.capital_bn)]);
 if(differences.length!==64||!differences.every(Number.isFinite))fail("cash oracle requires64 finite cost/capital comparisons");
 return differences;
}
function source(r,m){
 const fw=r.state?.fiscal_weight??1,terms={};
 for(const [side,rows]of [["receipt",r.evaluation.receipts],["spending",r.evaluation.spending]])
  for(const x of rows){
   const z={cost_bn:-fw*x.effect_bn,key:x.key};
   if(side==="spending"&&x.id==="medicaid_and_chip_other_medical"){
    const base=m.spending.lines.find(l=>l.id===x.id).keys.medicaid.personal;
    z.medicaid_base_cost_bn=base.target_bn*x.response;
   }
   terms[side+":"+x.id]=z;
  }
 for(const x of r.capital.components)terms["capital:"+x.id]={cost_bn:x.return_bn,key:x.id};
 terms["production:production"]={cost_bn:-(r.evaluation.private_wtp_bn+fw*r.evaluation.induced_receipts_bn),key:"production"};
 return terms;
}
function build(){
 const payloads=Object.fromEntries(["set","cash"].map(basis=>[basis,read(`main_case_2026_10_16/derived/corrections${basis==="cash"?"_cash":""}.json`)]));
 if(process.env.UNCERTAINTY_CANDIDATE!=="1"){
  const live=read("live_case.json");
   for(const payload of Object.values(payloads))validateAdoption(live,payload);
 }
 const P=require("../main_case_2026_10_16/package.cjs"),V=require("../generation_account_2026_09_24/v9_split.cjs");
 if(process.env.UNCERTAINTY_CANDIDATE!=="1"&&P.V9.STATUS!=="adopted")fail("package literal STATUS must be adopted");
 const summary=read("main_case_2026_10_16/derived/summary.json").v9;
 const result={case:"oct16",sets:{},source_sha256:{},scope:"all personal MAIN_SPECS principal values; source coefficients evaluated at each specification; person-key shapes remain the delivered signed source kernels"};
 for(const basis of ["set","cash"]){
   const api=basis==="cash"?P.CASH:P,payload=payloads[basis];
  const src=V.sourceModels(basis,"a"),rows=[];
  for(const [spec,s]of api.MAIN_SPECS.entries()){
   const m=api.payloadModel(),r=api.evaluateFull(m,s,api.MAIN_PROFILE);
   const terms=Object.fromEntries(V.GENS.map(g=>[g,source(src.ev.evaluateFull(src.models[g],s),src.models[g])]));
   const college_sources=r.capital.components.filter(c=>['college','college_user_fees'].includes(c.id)).map(c=>({
    ...c,source_rule:api.componentsFor(null).find(x=>x.id===c.id).key}));
   const end=anchorSpecs(summary,basis).indexOf(spec);
   rows.push({spec,anchor_end:end<0?null:["low","high"][end],coordinates:s,cost_bn:r.cost_bn,capital_bn:r.capital.total_bn,source_terms:terms,
    college_sources,v9_post_engine:{parts:Object.fromEntries(['public_college_response','health_residual_key'].map(id=>[id,r.v9_post_engine.parts[id]]))}});
  }
  const band=[Math.min(...rows.map(r=>r.cost_bn)),Math.max(...rows.map(r=>r.cost_bn))];
  const expected=basis==="cash"?summary.cash_set_bn:summary.band_bn;
  if(band.some((v,i)=>Math.abs(v-expected[i])>1e-9))fail(basis+" full-precision band differs "+JSON.stringify({band,expected}));
  for(const [i,end]of ["low","high"].entries()){
   const anchors=rows.filter(r=>r.anchor_end===end);
   if(anchors.length!==1||anchors[0].coordinates.reading!==end||Math.abs(anchors[0].cost_bn-band[i])>1e-9)fail("authoritative end specification differs from principal band");
  }
  const csv=fs.readFileSync(path.join(FISCAL,"main_case_2026_10_16/derived/main_case_bands.csv"),"utf8").trim().split("\n").map(s=>s.split(",")),h=csv.shift();
  const oracle=csv.map(a=>Object.fromEntries(h.map((k,i)=>[k,a[i]]))).find(r=>r.variant===(basis==="set"?"adopted":"cash_set")&&r.profile===api.MAIN_PROFILE);
  if(!oracle||band.some((v,i)=>Math.abs(v-Number(oracle[i?"cost_high_bn":"cost_low_bn"]))>5e-5))fail("printed band oracle differs");
  const meta={items:payload.meta.items.map(({id,number,applied})=>({id,number,applied}))};
  for(const id of ['coverage','native_minor_calibration','coverage_tenure'])meta[id]={by_end:Object.fromEntries(
   ['low','high'].map(end=>[end,{total_bn:payload.meta[id].by_end[end].total_bn}]))};
  result.sets[basis]={rows,band_bn:band,population:payload.meta.population_v9,items:payload.meta.items.filter(x=>x.applied).map(x=>x.id),meta};
 }
 for(const f of ["live_case.json","main_case_2026_10_16/package.cjs","main_case_2026_10_16/derived/summary.json","main_case_2026_10_16/derived/corrections.json","main_case_2026_10_16/derived/corrections_cash.json","generation_account_2026_09_24/v9_split.cjs"])
  result.source_sha256["infra/immigration-fiscal/"+f]=crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL,f))).digest("hex");
 require("../main_case_2026_10_16/memory_guard.cjs").requireWithinBudget("oct16 uncertainty all-spec exporter");
 return result;
}
if(require.main===module){writeSources();console.log("PASS oct16 all-spec source values, set/cash bands 1e-9 and CSV 5e-5");}
module.exports={build,source,validateAdoption,cashOracleDifferences,loadSources,writeSources,anchorSpecs,pinCachedSources};
