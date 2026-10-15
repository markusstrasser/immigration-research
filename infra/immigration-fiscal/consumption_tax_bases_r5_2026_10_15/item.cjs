/* Item 18 declaration. Default central is deliberately unavailable, not zero.
 * Explicit conditional arms use the case edit-set and post-engine conventions.
 * Native-First: existing Engine.applyCorrections and evaluateFull.
 */
"use strict";
const fs=require("fs"),path=require("path");
const HERE=__dirname, ID="consumption_tax_bases";
const read=()=>JSON.parse(fs.readFileSync(path.join(HERE,"derived/item.json"),"utf8"));
const clone=x=>JSON.parse(JSON.stringify(x));
const fail=s=>{throw Error("[BLOCKED] item18: "+s);};
function build(ctx,arm,which) {
  const input=read();
  if(!arm||!Object.hasOwn(input.arms,arm))fail("complete central is unidentified; choose an explicit conditional arm");
  if(!["set","cash"].includes(which))fail("unknown accounting set");
  const chosen=input.arms[arm],X=which==="set"?ctx.B:ctx.B.CASH;
  if(!X||typeof X.payloadModel!=="function")fail("case API absent");
  const ratios=chosen.receipt_ratios;
  const editsAt=m=>{
    const edits=[];
    for(const [id,ratio] of Object.entries(ratios)) {
      if(!Number.isFinite(ratio)||ratio<0)fail("invalid line ratio "+id);
      const line=m.receipts.lines.find(l=>l.id===id);
      if(!line)fail("missing receipt "+id);
      for(const scenario of m.receipts.scenarios) {
        const by={};
        for(const a of ["personal","shared"]) {
          const cell=line.cells[scenario][a];
          if(cell.key!=="consumption"||!cell.direct)fail("receipt is no longer direct consumption: "+id);
          by[a]=cell.target_bn*(ratio-1);
        }
        edits.push({side:"receipt",line:id,scenario,by});
      }
      // Item10 reporter effects are signed spending carriers, not receipt cells.
      for(const [carrier,source] of Object.entries(m.corrections?.union_completion?.carriers||{})) {
        if(source.side!=="receipt"||source.parent_line!==id)continue;
        const row=m.spending.lines.find(l=>l.id===carrier);
        if(!row)fail("reporter carrier absent "+carrier);
        for(const key of Object.keys(row.keys))edits.push({side:"spending",line:carrier,key,
          by:Object.fromEntries(["personal","shared"].map(a=>[a,row.keys[key][a].target_bn*(ratio-1)]))});
      }
    }
    return edits;
  };
  const by_end={};
  for(const end of ["low","high"]) {
    const line_parts=[];
    for(const p of X.POST_ENGINE.coverage?.by_end[end].decomposition?.line_parts||[]) {
      if(p.source_side!=="receipt"||!Object.hasOwn(ratios,p.source_line))continue;
      line_parts.push({line:p.source_line,generation:p.generation,source:"coverage",source_cost_bn:p.coverage_bn,
        ratio:ratios[p.source_line],delta_cost_bn:p.coverage_bn*(ratios[p.source_line]-1)});
    }
    const by_generation_bn={G1:0,G2:0,G3plus:0};
    for(const p of line_parts){if(!Object.hasOwn(by_generation_bn,p.generation))fail("coverage generation absent");by_generation_bn[p.generation]+=p.delta_cost_bn;}
    by_end[end]={total_bn:line_parts.reduce((s,p)=>s+p.delta_cost_bn,0),by_generation_bn,line_parts};
  }
  const m=X.payloadModel(),edits=editsAt(m);
  const parts=Object.fromEntries(edits.map((e,i)=>[`${e.side}:${e.line}:${e.scenario||e.key}`,{edit:i,by:clone(e.by),source_arm:arm}]));
  return {edits,editsAt,parts,meta:{[ID]:{id:ID,arm,which,by_end,application:"post_engine_fixed_amount_by_reading",
    identification_status:input.identification_status,assumptions:chosen.assumptions,limits:chosen.limits,
    item11:"held; no complete mixed-unit basket correction identified"}},
    record:{applied_after_engine:true,source:"consumption_tax_bases_r5_2026_10_15/derived/item.json",conditional:true},
    detail:{receipt_ratios:ratios,national_totals:"held by opposing target/other shifts",item10:"signed carriers moved in all scenarios"}};
}
function registry() {return {id:ID,kind:"post_engine",label:"consumption-tax bases (conditional arms only)",arms:clone(read().arms),build};}
module.exports={ID,build,registry};
