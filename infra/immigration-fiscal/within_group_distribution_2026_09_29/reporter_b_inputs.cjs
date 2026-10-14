/* Read-only raw selector/part inventory for reporter convention(b) ownership. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const HERE=__dirname,FISCAL=path.dirname(HERE),P=require("../main_case_2026_10_15/package.cjs");
const read=f=>JSON.parse(fs.readFileSync(path.join(FISCAL,f),"utf8"));
const sha=f=>crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL,f))).digest("hex");
const pins={};
function atomicWrite(file,data){const temporary=`${file}.tmp-${process.pid}`;try{fs.writeFileSync(temporary,data);fs.renameSync(temporary,file);}finally{if(fs.existsSync(temporary))fs.unlinkSync(temporary);}}
function input(f){pins[f]=sha(f);return read(f);}
const output={contract:"oct15 reporter raw selector inventory",sets:{}};
const ORIGINAL=require("../main_case_2026_10_14/package.cjs");
pins["main_case_2026_10_14/package.cjs"]=sha("main_case_2026_10_14/package.cjs");
pins["main_case_2026_10_15/item_union.cjs"]=sha("main_case_2026_10_15/item_union.cjs");
const frozenFile="within_group_distribution_2026_09_29/inputs/reporter_b_base_models.json";
const frozen=fs.existsSync(path.join(FISCAL,frozenFile))?input(frozenFile):{contract:"frozen oct15 BASE(a) parent cells, native and added-state increments removed",sets:{},source_provenance:{}};
for(const [basis,suffix] of [["set",""],["cash","_cash"]]) {
  const payload=input(`main_case_2026_10_15/derived/corrections${suffix}.json`);
  const item=payload.meta.items.find(r=>r.id==="union_completion");
  if(!item) throw Error("[BLOCKED] no union completion registry");
  const carriers=payload.meta.union_completion.carriers,parts={};
  for(const [name,part] of Object.entries(item.parts)) {
    const edit=payload.edits[item.edits.first+part.edit];
    if(!Object.hasOwn(carriers,edit.line)) continue;
    if(edit.side!=="spending" || edit.key!=="k" || !name.startsWith("union_G3plus:"))
      throw Error(`[BLOCKED] unknown reporter raw part ${name}`);
    parts[name]={route_id:`union_completion|${name}`,part_edit:part.edit,global_edit:item.edits.first+part.edit,
      cell:Object.fromEntries(Object.entries(edit).filter(([k])=>k!=="by")),by:part.by,carrier:edit.line,
      selector:carriers[edit.line],response:payload.meta.responses[edit.line]};
  }
  if(Object.keys(parts).length!==Object.keys(carriers).length ||
      new Set(Object.values(parts).map(r=>r.carrier)).size!==Object.keys(carriers).length)
    throw Error("[BLOCKED] reporter part/carrier cardinality mismatch");
  const signature=crypto.createHash("sha256").update(JSON.stringify({carriers,parts,
    records:payload.meta.union_completion.observed_records})).digest("hex");
  const originalParent=(basis==="set"?ORIGINAL:ORIGINAL.CASH).payloadModel();
  for(const part of Object.values(parts)) {
    const src=part.selector;
    if(src.kind!=="line" || !src.extrapolated_key) continue;
    const parent=byLine(originalParent,src.side,src.parent_line);
    if(!parent || !src.source_keys.length) throw Error("[BLOCKED] extrapolated carrier lacks authoritative source anchor");
    const preferred=src.side==="receipt"?originalParent.receipts.reference:parent.preferred_key;
    const source_key=src.source_keys.includes(preferred)?preferred:src.source_keys[0];
    const declaration={side:src.side,parent_line:src.parent_line,preferred_key:preferred,source_keys:src.source_keys,source_key};
    part.source_anchor={...declaration,declaration_sha256:crypto.createHash("sha256").update(JSON.stringify(declaration)).digest("hex")};
  }
  let receipt,spending;
  if(frozen.sets[basis]) {
    const saved=frozen.sets[basis];
    if(saved.raw_case_signature!==signature) throw Error("[BLOCKED] frozen BASE model differs from current raw reporter declaration");
    ({receipt,spending}=saved);
  } else {
  const splitFile=`generation_account_2026_09_24/derived/generation_corrections_oct15${suffix}.json`;
  const split=input(splitFile).payloads.a.G3plus;
  const modelFile="generation_account_2026_09_24/derived/model_G3plus.json";
  const original=input(modelFile);
  if(split.meta.coverage && !split.meta.coverage.stub) throw Error("[BLOCKED] initial reporter parent freeze requires BASE generation payload");
  let model=P.Engine.applyCorrections(original,split);
  const reverse=Object.entries(item.parts).filter(([name])=>name.startsWith("lineage_g3plus:observed_nonreporters:"))
    .map(([,part])=>({...payload.edits[item.edits.first+part.edit],
      by:Object.fromEntries(Object.entries(part.by).map(([a,v])=>[a,-v]))}));
  model=P.Engine.applyCorrections(model,{edits:reverse,meta:model.corrections});
  const state=split.meta.added_state_price_routing;
  if(state) model=P.Engine.applyCorrections(model,{edits:state.changes.map(r=>({...r.edit,
    by:Object.fromEntries(Object.entries(r.by_generation.G3plus).map(([a,v])=>[a,-v]))})),meta:model.corrections});
  receipt=Object.fromEntries(model.receipts.lines.map(r=>[r.id,{national_bn:r.national_bn,cells:r.cells}]));
  spending=Object.fromEntries(model.spending.lines.map(r=>[r.id,{national_bn:r.national_bn,keys:r.keys}]));
  frozen.sets[basis]={receipt,spending,raw_case_signature:signature};
  frozen.source_provenance[splitFile]=pins[splitFile];frozen.source_provenance[modelFile]=pins[modelFile];
  }
  output.sets[basis]={parts,carriers,receipt,spending,observed_records:payload.meta.union_completion.observed_records,
    case_payload_sha256:pins[`main_case_2026_10_15/derived/corrections${suffix}.json`]};
}
if(!fs.existsSync(path.join(FISCAL,frozenFile))) {
  fs.mkdirSync(path.dirname(path.join(FISCAL,frozenFile)),{recursive:true});
  atomicWrite(path.join(FISCAL,frozenFile),JSON.stringify(frozen,null,1)+"\n");
}
for(const key of Object.keys(pins)) if(key.startsWith("generation_account_2026_09_24/derived/")) delete pins[key];
pins[frozenFile]=sha(frozenFile);
pins["within_group_distribution_2026_09_29/reporter_b_inputs.cjs"]=sha("within_group_distribution_2026_09_29/reporter_b_inputs.cjs");
for(const [f,value] of Object.entries(pins)) if(sha(f)!==value) throw Error(`[BLOCKED] source changed during raw inventory: ${f}`);
output.source_sha256=pins;
fs.mkdirSync(path.join(HERE,"derived"),{recursive:true});
atomicWrite(path.join(HERE,"derived/reporter_b_inputs.json"),JSON.stringify(output,null,1)+"\n");
console.log(`✓ reporter raw selector inventory: ${Object.keys(output.sets.set.parts).length} set / ${Object.keys(output.sets.cash.parts).length} cash parts`);
function byLine(m,side,id){return m[side==="receipt"?"receipts":"spending"].lines.find(r=>r.id===id);}
