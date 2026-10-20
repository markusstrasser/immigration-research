/* Transport selected v9 components on the existing typed historical contract.
 * The archived v8 decomposition is a pinned input, never regenerated in place. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const HERE=__dirname,FISCAL=path.resolve(HERE,".."),LANE="main_case_2026_10_16";
const sum=a=>a.reduce((x,y)=>x+y,0),mean=a=>sum(a)/a.length,clone=x=>JSON.parse(JSON.stringify(x));
const fail=s=>{throw Error("[BLOCKED] oct16 backcast: "+s);};
const near=(a,b,s,t=1e-9)=>{if(!Number.isFinite(a)||!Number.isFinite(b)||Math.abs(a-b)>t)fail(`${s}: ${a} != ${b}`);};
function sha(p){const hash=crypto.createHash("sha256"),fd=fs.openSync(p,"r"),buffer=Buffer.alloc(1024*1024);try{let n;while((n=fs.readSync(fd,buffer,0,buffer.length,null))>0)hash.update(buffer.subarray(0,n));}finally{fs.closeSync(fd);}return hash.digest("hex");}
const read=p=>JSON.parse(fs.readFileSync(path.join(FISCAL,p),"utf8"));
const parent={school_reprice:"education_services",college_rekey:"education_services",roads_vmt_sl:"economic_affairs_services",roads_vmt_fed:"economic_affairs_services",state_price_public_order_safety:"public_order_safety",state_price_health_services:"health_services",state_price_recreation_culture:"recreation_culture"};
function retainCompositeMixedParts(data){
 for(const block of Object.values(data.concepts))for(const p of Object.values(block.v6_parts)){
  if(p.item!=="mixed_unit_removal"||!["M6_biological_children","D_added_residual"].includes(p.component))continue;
  Object.assign(p,{side:"unlocated",line:p.component,national_bn:null,parent:null,rule:"per_person",unlocated:true,
   transport_assumption:p.component==="M6_biological_children"?"Composite federal income, refundable-credit, state-tax and removed-projection change (round2.py54–58); no preserved source-category split. Held per declared union/G3+ population path.":"Transported composite Df+Dc federal-income/refundable-credit remainder (removal.py381–390; round2.py71–73); no preserved source-category split. Held per declared lineage/G3+ population path."});
  delete p.income_linked;
 }
 return data;
}
function main(outDir){
 const P=require("../main_case_2026_10_16/package.cjs"),B=P.V8_PACKAGE;
 const data=read("historical_backcast_2026_09_20/derived/case_components_oct15.json");
 for(const [rel,h]of Object.entries(data.inputs))if(sha(path.join(FISCAL,rel))!==h)fail("stale archived component input "+rel);
 const baseFile="historical_backcast_2026_09_20/derived/case_components_oct15.json";
 data.inputs[baseFile]=sha(path.join(FISCAL,baseFile));
 retainCompositeMixedParts(data);
 const summary=read(`${LANE}/derived/summary.json`),meta=P.correctionsPayload().meta;
 const selected=meta.items.filter(x=>!B.ITEM_IDS.includes(x.id)).map(x=>x.id);
 if(selected.includes("passthrough_source_tax"))fail("item19 is beside, not a selected central component");
 data.case="oct16";data.lane=LANE;data.population_v9=meta.population_v9;
 data.v9_rule="Typed selected source components, joint-minus16 tenure, own repriced coverage; original union/G1/G2 on union path, G3+ and completion on identified-G3+ path; capital stocks at fixed Trustees real rate; unlocated stays explicit.";
 data.v9_items=selected;data.resource_rate=meta.one_rate.flat_real_equivalent;
 const sourceFiles=new Set([`${LANE}/package.cjs`,`${LANE}/item_rate.cjs`,`${LANE}/derived/summary.json`,`${LANE}/derived/main_case_bands.csv`,`${LANE}/derived/corrections.json`,`${LANE}/derived/corrections_cash.json`,"historical_backcast_2026_09_20/v9_components.cjs","mixed_unit_removal_2026_10_14/round2.py","mixed_unit_removal_2026_10_14/removal.py"]);
 const countAudit={};
 for(const basis of ["set","cash"]){
  const rel=`coverage_bound_2026_10_14/derived/pricing_audit_oct15_final_routing_${basis}.json`;
  countAudit[basis]=read(rel);sourceFiles.add(rel);
 }
 function infoFor(piece,item){
  const lid=piece.source_line||piece.line,kind=piece.economic_class,accrual=piece.category==="pension_accrual";
  const carrier=meta.union_completion.carriers[piece.line];
  const capital=kind==="capital_return"||piece.side==="capital"||piece.source_side==="capital"||Object.hasOwn(piece,"capital_stock_delta_bn")||piece.kind==="college_capital"||item==="one_rate";
  const component=capital?(carrier?.parent_line||lid):null;
  const g3=piece.generation==="G3plus"||piece.generation==="G3+"||piece.population==="completion"||!!carrier||piece.line?.startsWith("native_child_");
  const unlocated=kind?.startsWith("unclassified");
   const rule=unlocated||lid==="lane_constants"?"per_person":capital?"capital":kind==="production"?"production":accrual?"accrual":"line";
  const side=unlocated?"unlocated":capital?"capital":kind==="production"?"production":piece.source_side||"spending";
  return {item,path:piece.population==="added_lineage"?"lineage":"union",side,line:lid,parent:parent[lid]||null,national_bn:null,rule,
   ...(piece.generation?{generation:piece.generation}:{}),...(g3?{population_path:"g3plus"}:{}),
   ...(capital?{component}:{}),...(Object.hasOwn(piece,"capital_stock_delta_bn")?{source_delta_stock_bn:piece.capital_stock_delta_bn,transport_rate_real:data.resource_rate}:{}),
   ...(accrual?{contributions:lid==="social_security"?"oasdi":lid==="medicare"?"hi":fail("unknown earned-pension source "+lid)}:{}),
   ...(unlocated?{unlocated:true,transport_assumption:"source-declared residual held per declared union/G3+ population; fiscal/financing classification unresolved"}:{})};
 }
 function typed(parts,piece,item,key,value,basis){
  const info=infoFor(piece,item);
  if(info.rule==="production"){
   let src=piece.source_production;
   if(!src){
    const matches=countAudit[basis].denominator_pieces.filter(p=>p.economic_class==="production"&&p.end===piece.end&&p.generation===piece.generation);
    if(!matches.length)fail("missing declared production P/F ratio");
    src=matches[0].source_production;
    for(const q of matches){near(q.source_production.private_wtp_bn/q.source_production.cost_bn,src.private_wtp_bn/src.cost_bn,"production private ratio");near(q.source_production.fiscal_weight*q.source_production.induced_receipts_bn/q.source_production.cost_bn,src.fiscal_weight*src.induced_receipts_bn/src.cost_bn,"production fiscal ratio");}
   }
   if(!Number.isFinite(src.cost_bn)||Math.abs(src.cost_bn)<1e-12)fail("production denominator");
   const privatePart=value*(-src.private_wtp_bn/src.cost_bn),fiscalPart=value*(-src.fiscal_weight*src.induced_receipts_bn/src.cost_bn);
   near(privatePart+fiscalPart,value,"declared production P/F cost closure");
   parts[key+"_private"]={value:privatePart,info:{...info,line:"private_wtp_bn",transport_assumption:"source generation-end P/F ratio, GDP path; not a new production solve"}};
   parts[key+"_receipts"]={value:fiscalPart,info:{...info,line:"induced_receipts_bn",income_linked:true}};
  }else parts[key]={value,info};
 }
 function collect(api,run,old,basis,end,block){
  const parts={},payload=api.correctionsPayload(),mm=payload.meta,post=run.v9_post_engine;
  const anchor=block.ends[end],allMeta={...block.v4_parts,...block.v5_parts,...block.v6_parts};
  function ownShare(line,side,capital=false){
   let own,denominator;
   if(capital){
    own=(anchor.v5_capital_bn[line]||0)+(anchor.v6_capital_bn.lineage[line]||0);
    own+=sum(Object.entries(allMeta).filter(([k,p])=>p.path==="lineage"&&p.rule==="capital"&&p.component===line).map(([k])=>anchor.additions_bn[k]||0));
    denominator=old.capital.components.find(c=>c.id===line)?.return_bn;
   }else{
    own=sum(Object.entries(allMeta).filter(([k,p])=>(k.startsWith("v5_")||p.path==="lineage")&&p.line===line&&p.side===side&&p.rule!=="capital").map(([k])=>anchor.additions_bn[k]||0));
    const row=old.evaluation[side==="receipt"?"receipts":"spending"].find(c=>c.id===line);
    denominator=row?(side==="receipt"?-1:1)*row.response*row.amount_bn:0;
   }
   if(!denominator){near(own,0,"zero source lineage share "+line);return 0;}
   const fraction=own/denominator;
   if(!Number.isFinite(fraction)||fraction < -1e-9||fraction>1+1e-9)fail("invalid archived lineage source share "+line+": "+fraction);
   return fraction;
  }
  function splitSource(key,value,info,fraction){
   // The archived decomposition stores fill-in-method means. Its lineage share
   // is an explicit source-share transport, not a new historical estimator.
   parts[key]={value:value*(1-fraction),info};
   if(fraction)parts[key+"_lineage"]={value:value*fraction,info:{...info,path:"lineage",population_path:"g3plus",transport_assumption:"archived method-mean lineage share of this source line/component; held historical relative composition"}};
  }
  for(const side of ["spending","receipts"]){
   const prev=new Map(old.evaluation[side].map(q=>[q.id,q]));
   for(const q of run.evaluation[side]){
    const z=prev.get(q.id),value=(side==="receipts"?-1:1)*(q.response*q.amount_bn-(z?z.response*z.amount_bn:0));
    if(Math.abs(value)<1e-15)continue;
    const carrier=mm.union_completion.carriers[q.id],lid=carrier?.parent_line||q.id;
    const info=infoFor({line:q.id,source_line:lid,source_side:side==="receipts"?"receipt":"spending",population:carrier?"completion":"engine",economic_class:carrier?.kind==="capital"?"capital_return":"fiscal_line"},"consumption_tax_bases");
    splitSource(`v6_consumption_tax_bases_union_${q.id}`,value,info,carrier?0:ownShare(lid,info.side));
   }
  }
  near(run.evaluation.private_wtp_bn,old.evaluation.private_wtp_bn,"v9 engine private unchanged");
  near(run.evaluation.induced_receipts_bn,old.evaluation.induced_receipts_bn,"v9 engine production receipts unchanged");
  near(run.capital.total_bn,old.capital.total_bn,"v9 engine capital unchanged; revaluation is post");
  for(const id of selected){
   const value=post.amounts[id]||0,rows=post.parts[id];
   if(["native_minor_calibration","coverage_tenure"].includes(id)){
    const block=mm[id];sourceFiles.add(block.parts_file);
    const pieces=P.RATE.countParts(block,end);
    for(const [i,q]of pieces.entries())typed(parts,q,id,`v6_${id}_union_${i}_${q.source_line}`,q.delta_cost_bn,basis);
    near(sum(pieces.map(q=>q.delta_cost_bn)),value,`${id} typed amount`);
   }else if(rows){
    if(mm[id]?.source)sourceFiles.add(typeof mm[id].source==="string"?mm[id].source:mm[id].source.file||fail("unidentified source file "+id));
    for(const [i,q]of rows.entries()){
     const key=`v6_${id}_union_${i}_${q.line}`;
     if(id==="health_residual_key"&&Object.hasOwn(q,"capital_stock_delta_bn"))near(q.delta_bn,q.capital_stock_delta_bn*data.resource_rate,"item21 direct stock must use live Trustees rate");
     typed(parts,q,id,key,q.delta_bn,basis);
     if(q.kind==="college_operating")parts[key].info.use_key_exempt=true;
     const engine=q.population==="engine"||q.component==="capital_engine";
     if(engine){
      const capital=parts[key].info.rule==="capital",source=capital?parts[key].info.component:q.capital_source_line||q.source_line||q.line;
      const fraction=ownShare(source,parts[key].info.side,capital||q.kind==="college_operating");
      splitSource(key,q.delta_bn,parts[key].info,fraction);
     }
    }
    near(sum(rows.map(q=>q.delta_bn)),value,`${id} dynamic source rows`);
   }else if(Math.abs(value)>1e-12)fail("selected item has no typed source rows: "+id);
  }
  // The direct source pieces above exclude coverage. Apply its own-price delta
  // once, with the full typed before/after kernels, not an aggregate remainder.
  for(const [block,sign,label]of [[mm.coverage,1,"new"],[(basis==="cash"?B.CASH:B).correctionsPayload().meta.coverage,-1,"old"]]){
   const pieces=block.by_end[end].decomposition?.line_parts;if(!pieces)fail("coverage typed kernel absent");
   for(const [i,q]of pieces.entries())typed(parts,{...q,end},"coverage_repricing",`v6_coverage_repricing_union_${label}_${i}_${q.source_line||q.line}`,sign*q.coverage_bn,basis);
  }
  near(sum(Object.entries(parts).filter(([,q])=>q.info.item==="coverage_repricing").map(([,q])=>q.value)),post.amounts.coverage_repricing,"coverage typed repricing");
  near(sum(Object.values(parts).map(q=>q.value)),run.cost_bn-old.cost_bn,"all selected typed component closure");
  return parts;
 }
 const bands=fs.readFileSync(path.join(FISCAL,LANE,"derived/main_case_bands.csv"),"utf8").trim().split("\n").map(x=>x.split(",")),header=bands.shift();
 function oracle(profile,variant){if(summary.v9.historical_rows.includes(profile+"/"+variant))return null;const rows=bands.map(r=>Object.fromEntries(header.map((k,i)=>[k,r[i]]))).filter(r=>r.profile===profile&&r.variant===variant);if(!rows.length&&variant==="cash_set"&&profile==="proportional_reference")return null;if(rows.length!==1)fail("band row "+profile+"/"+variant);return [Number(rows[0].cost_low_bn),Number(rows[0].cost_high_bn)];}
 for(const [concept,block]of Object.entries(data.concepts)){
  const metadata={},gates={};
  for(const [ei,end]of ["low","high"].entries()){
   const byMethod=[],cashTotals=[],totals=[];
   for(const [mi,method]of P.METHODS.entries()){
    const options=P.withCentral({profile:block.profile}),model=P.modelFor("central",method,options);
    const all=P.MAIN_SPECS.map(s=>P.evaluateFull(model,s,block.profile));
    const wanted=Math[end==="low"?"min":"max"](...all.map(q=>q.cost_bn)),index=all.findIndex(q=>Math.abs(q.cost_bn-wanted)<1e-10);
    if(index!==block.end_specifications[mi][end])fail(`found ${concept}/${method}/${end} end ${index} moved from archived base; reprice historical base`);
    const spec=P.MAIN_SPECS[index],baseModel=B.modelFor("central",method,B.withCentral({profile:block.profile}));
    const r=all[index],r0=B.evaluateFull(baseModel,spec,block.profile),rc=P.CASH.evaluateFull(P.CASH.modelFor("central",method,P.CASH.withCentral({profile:block.profile})),spec,block.profile),bc=B.CASH.evaluateFull(B.CASH.modelFor("central",method,B.CASH.withCentral({profile:block.profile})),spec,block.profile);
    const parts=collect(P,r,r0,"set",end,block),cash=collect(P.CASH,rc,bc,"cash",end,block);
    byMethod.push(parts);cashTotals.push(rc.cost_bn);totals.push(r.cost_bn);
    near(sum(Object.values(cash).map(q=>q.value)),rc.cost_bn-bc.cost_bn,"cash typed component closure");
   }
   const e=block.ends[end],principal=mean(totals);
   near(e.cost_bn+mean(byMethod.map(p=>sum(Object.values(p).map(q=>q.value)))),principal,"archived base plus v9 components");
   e.cost_bn=principal;
   for(const key of new Set(byMethod.flatMap(p=>Object.keys(p)))){
    const records=byMethod.map(p=>p[key]);if(records.some(q=>!q))fail("method typed shape "+key);
    e.additions_bn[key]=mean(records.map(q=>q.value));metadata[key]=records[0].info;
   }
   const setOracle=oracle(block.profile,"adopted");if(setOracle)near(principal,setOracle[ei],concept+" adopted band",1e-4);else if(concept==="net_cost_cbo_informed")fail("main adopted row is historical");
   const cashOracle=oracle(block.profile,"cash_set");if(cashOracle)near(mean(cashTotals),cashOracle[ei],concept+" cash band",1e-4);
   gates[end]={set:principal,cash:mean(cashTotals),set_component_tolerance_bn:1e-9,cash_component_tolerance_bn:1e-9,band_tolerance_bn:setOracle?1e-4:null,scope:setOracle?"live adopted profile":"native v9 alternative profile diagnostic; retained CSV row is historical and never an oracle"};
   console.log(`PASS ${concept}/${end}: set ${principal}, cash ${mean(cashTotals)}; typed closure 1e-9, bands 1e-4`);
  }
  Object.assign(block.v6_parts,metadata);block.v9_gates=gates;
 }
 for(const rel of sourceFiles)data.inputs[rel]=sha(path.join(FISCAL,rel));
 near(data.concepts.net_cost_cbo_informed.ends.low.cost_bn,summary.v9.band_bn[0],"summary set low");
 near(data.concepts.net_cost_cbo_informed.ends.high.cost_bn,summary.v9.band_bn[1],"summary set high");
 const guard=cp.spawnSync("uv",["run","--no-project","python3",path.join(HERE,"bridge_memory.py"),String(process.pid)],{cwd:path.resolve(FISCAL,"../.."),encoding:"utf8"});
 if(guard.status!==0)fail("physical memory guard: "+guard.stdout+guard.stderr);console.log(guard.stdout.trim());
 fs.mkdirSync(outDir,{recursive:true});fs.writeFileSync(path.join(outDir,"case_components_oct16.json"),JSON.stringify(data,null,1)+"\n");
}
module.exports={main,retainCompositeMixedParts};
