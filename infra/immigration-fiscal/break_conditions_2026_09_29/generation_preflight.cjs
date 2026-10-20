"use strict";
function validateReproducedSource(contract,root,read=require("fs").readFileSync) {
  const crypto=require("crypto"),path=require("path");
  const block=s=>{throw Error(`[BLOCKED] oct16 generation source replay: ${s}`);};
  if(contract?.case!=="oct16"||contract.producer!=="generation_account_2026_09_24/run_generations_v9.cjs")block("missing exact producer contract");
  const expected=["oct16","oct16_cash"].flatMap(key=>["results","summary","corrections"].map(kind=>
    `generation_account_2026_09_24/derived/generation_${kind}_${key}.${kind==="results"?"csv":"json"}`));
  if(expected.some(name=>!contract.outputs?.[name])||Object.keys(contract.outputs||{}).length!==6)block("six reproduced outputs required");
  for(const name of [contract.producer,"main_case_2026_10_16/package.cjs","main_case_2026_10_16/derived/corrections.json","main_case_2026_10_16/derived/corrections_cash.json"])
    if(!contract.inputs?.[name])block("missing principal input "+name);
  for(const [name,sha]of Object.entries({...contract.inputs,...contract.outputs})){
    const actual=crypto.createHash("sha256").update(read(path.join(root,name))).digest("hex");
    if(actual!==sha)block("input/output bytes changed "+name);
  }
  return true;
}
function validateGenerationPayloads(gp,full,caseKey,reproduced=false) {
  const block=s=>{throw Error(`[BLOCKED] ${caseKey} generation preflight: ${s}; run final generation account first`);};
  for(const conv of ["a","b"])for(const g of ["G1","G2","G3plus"]) {
    const meta=gp?.[conv]?.[g]?.meta;
    if(meta?.generation!==g||meta.case_key!==caseKey)block(`stale case/generation stamp ${conv}/${g}`);
    if(meta.adopted!==full.adopted&&!(caseKey==="oct16"&&reproduced&&
       meta.case_lane==="main_case_2026_10_16"&&/^generation_corrections_oct15(_cash)?\.json$/.test(meta.source_v8||"")))
      block(`unverified inherited adoption stamp ${conv}/${g}`);
    for(const item of ["mixed_unit_removal","coverage"])for(const end of ["low","high"])
      if(!Number.isFinite(meta[item]?.by_end?.[end]?.total_bn))block(`missing ${item} ${conv}/${g}/${end}`);
   if(caseKey==="oct16"&&(!Array.isArray(meta.v9_posts_by_spec)||!Array.isArray(meta.v9_specs)||meta.v9_posts_by_spec.length!==meta.v9_specs.length))block(`missing v9 per-spec post routing ${conv}/${g}`);
  }
  for(const conv of ["a","b"])for(const item of ["mixed_unit_removal","coverage"])for(const end of ["low","high"]) {
    const sum=["G1","G2","G3plus"].reduce((n,g)=>{
      const m=gp[conv][g].meta;let value=m[item].by_end[end].total_bn;
      if(caseKey==="oct16"&&item==="coverage"){
        const i=m.v9_specs.findIndex(s=>s.allocation==="personal"&&s.reading===end);
        const delta=m.v9_posts_by_spec[i]?.coverage_repricing;
        if(!Number.isFinite(delta))block(`missing coverage reprice ${conv}/${g}/${end}`);
        value+=delta;
      }
      return n+value;
    },0);
    const want=full[item]?.by_end?.[end]?.total_bn;
    if(!Number.isFinite(want)||Math.abs(sum-want)>1e-9)block(`unclosed ${item} ${conv}/${end}`);
  }
}
module.exports={validateGenerationPayloads,validateReproducedSource};
