"use strict";
function validateGenerationPayloads(gp,full,caseKey) {
  const block=s=>{throw Error(`[BLOCKED] ${caseKey} generation preflight: ${s}; run final generation account first`);};
  for(const conv of ["a","b"])for(const g of ["G1","G2","G3plus"]) {
    const meta=gp?.[conv]?.[g]?.meta;
    if(meta?.generation!==g||meta.case_key!==caseKey||meta.adopted!==full.adopted)block(`stale case/generation stamp ${conv}/${g}`);
    for(const item of ["mixed_unit_removal","coverage"])for(const end of ["low","high"])
      if(!Number.isFinite(meta[item]?.by_end?.[end]?.total_bn))block(`missing ${item} ${conv}/${g}/${end}`);
  }
  for(const conv of ["a","b"])for(const item of ["mixed_unit_removal","coverage"])for(const end of ["low","high"]) {
    const sum=["G1","G2","G3plus"].reduce((n,g)=>n+gp[conv][g].meta[item].by_end[end].total_bn,0);
    const want=full[item]?.by_end?.[end]?.total_bn;
    if(!Number.isFinite(want)||Math.abs(sum-want)>1e-9)block(`unclosed ${item} ${conv}/${end}`);
  }
}
module.exports={validateGenerationPayloads};
