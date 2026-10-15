"use strict";
// v9 registry-compatible post-engine component. Parent selects/adopts an arm.
const fs=require("fs"),path=require("path");
const id="passthrough_source_tax";
const read=()=>JSON.parse(fs.readFileSync(path.join(__dirname,"derived/item.json"),"utf8"));
function build(ctx,arm,which){
  if(!["set","cash"].includes(which))throw Error("[BLOCKED] item19 accounting set required");
  const data=read();
  if(!arm||!Object.hasOwn(data.arms,arm))throw Error("[BLOCKED] item19 has no identified central: select an explicit arm");
  const selected=data.arms[arm];
  for(const end of ["low","high"]){
    const v=selected.by_end[end];
    if(!Number.isFinite(v.total_bn)||Math.abs(v.parts_by_line.reduce((s,p)=>s+p.total_bn,0)-v.total_bn)>1e-9)
      throw Error("[BLOCKED] item19 parts do not close");
  }
  return {edits:[],parts:{},meta:{[id]:{id,which,arm,by_end:selected.by_end,
    config:selected.config,interactions:data.interactions,population_scope:selected.by_end.low.population_scope,
    status:data.status}},record:{conditional:true,central_identified:false}};
}
module.exports={id,kind:"post_engine",build,arms:()=>Object.fromEntries(Object.keys(read().arms).map(k=>[k,{label:k}]))};
