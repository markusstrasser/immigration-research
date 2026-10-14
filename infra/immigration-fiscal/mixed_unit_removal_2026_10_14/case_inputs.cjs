/* Native-First: evaluate the frozen case package; write only this lane's file. */
"use strict";
const fs = require('fs'), path = require('path');
const B = require('../main_case_2026_10_14/package.cjs');
const payload = B.correctionsPayload(), m = B.payloadModel();
const summary = JSON.parse(fs.readFileSync(path.join(__dirname,'../main_case_2026_10_14/derived/summary.json')));
const ids = ['general_sales_tax','excise_selective_sales','customs_duties','personal_current_transfers'];
const extraReceipts=['modeled_owner_property','federal_income_tax','state_local_income_tax'];
const extraSpending=['snap','housing_subsidies','energy_assistance','wic'];
const L = payload.meta.lineage, first=L.edits.first, last=first+L.edits.count;
const unionValues = payload.edits.map((e,i)=>(i>=first && i<last)?0:
  e.side==='receipt' && ids.includes(e.line)?e.by.personal:0);
for(const item of payload.meta.items) {
  if(!item.edits || !item.parts) continue;
  for(const [name,p] of Object.entries(item.parts)) {
    const i=item.edits.first+p.edit;
    if(i>=first && i<last) continue;
    if(ids.includes(payload.edits[i].line) && (name.startsWith('lineage_') || name.startsWith('added_'))) unionValues[i]-=p.by.personal;
  }
}
const lines={};
for(const id of ids) {
  const base=B.MODEL.receipts.lines.find(x=>x.id===id);
  const current=m.receipts.lines.find(x=>x.id===id);
  const reference=B.MODEL.receipts.reference;
  const union=base.cells[reference].personal.target_bn+payload.edits.reduce((t,e,i)=>
    t+(e.side==='receipt' && e.line===id && e.scenario===reference?unionValues[i]:0),0);
  const full=current.cells[reference].personal.target_bn;
  if(!(union>0 && full>=union)) throw Error(`[BLOCKED] ${id} union target ${union}, full ${full}`);
  lines[id]={national_bn:base.national_bn, union_target_bn:union, lineage_target_bn:full-union, full_target_bn:full};
}
const endpoints={};
for(const [name,api] of [['set',B],['cash',B.CASH]]) {
  endpoints[name]=summary.v7.end_specifications[name] || summary.v7.end_specifications;
}
// Both bases use specification indices 16 / 11. Confirm against stored band;
// never use a hard-coded monetary headline as the check's oracle.
const bands={}, responses={}, evaluated={};
for(const [name,api] of [['set',B],['cash',B.CASH]]) {
  const own=api.MAIN_SPECS || B.MAIN_SPECS;
  const costs=own.map(s=>api.evaluateFull(api.payloadModel(),s,B.CENTRAL.profile).cost_bn);
  const low=costs.indexOf(Math.min(...costs)), high=costs.indexOf(Math.max(...costs));
  bands[name]=[costs[low],costs[high]];
  evaluated[name]=[low,high].map(i=>{
    const q=api.evaluateFull(api.payloadModel(),own[i],B.CENTRAL.profile).evaluation;
    return {spec:i, specification:own[i],receipts:q.receipts.filter(r=>extraReceipts.includes(r.id)),
      spending:q.spending.filter(r=>extraSpending.includes(r.id))};
  });
  responses[name]=[low,high].map(i=>Object.fromEntries(api.evaluateFull(api.payloadModel(),own[i],B.CENTRAL.profile)
    .evaluation.receipts.filter(r=>ids.includes(r.id)).map(r=>[r.id,r.response])));
  endpoints[name]=[low,high];
}
// Trace union and added parts on every new key from the frozen edit registry.
const resourceLines={};
for(const [side,wanted] of [['receipt',extraReceipts],['spending',extraSpending]]) {
  for(const id of wanted) {
    const field=side==='receipt'?'receipts':'spending';
    const base=B.MODEL[field].lines.find(x=>x.id===id); if(!base) continue;
    const current=m[field].lines.find(x=>x.id===id);
    const key=side==='receipt'?B.MODEL.receipts.reference:base.preferred_key;
    const cell=side==='receipt'?base.cells[key].personal:base.keys[key].personal;
    const full=side==='receipt'?current.cells[key].personal:current.keys[key].personal;
    let union=cell.target_bn;
    for(let i=0;i<payload.edits.length;i++) {
      const e=payload.edits[i];
      if(e.side!==side || e.line!==id || (side==='receipt'?e.scenario:e.key)!==key || (i>=first&&i<last)) continue;
      union+=e.by.personal;
      for(const item of payload.meta.items) for(const [n,p] of Object.entries(item.parts||{})) {
        if(item.edits.first+p.edit===i && (n.startsWith('lineage_')||n.startsWith('added_'))) union-=p.by.personal;
      }
    }
    resourceLines[id]={side,key,national_bn:base.national_bn,union_target_bn:union,
      full_target_bn:full.target_bn,lineage_target_bn:full.target_bn-union};
    if(!(union>0)) throw Error(`[BLOCKED] resource line ${id} has no positive union target`);
  }
}
const out={case:'oct14',allocation:'personal',lines,resourceLines,bands,responses,evaluated,endpoints,lineage:L,
           child_credits:payload.meta.child_credits};
fs.mkdirSync(path.join(__dirname,'derived'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'derived/case_inputs.json'),JSON.stringify(out,null,2)+'\n');
console.log(`[case] ${bands.set.join(' / ')}; ends ${endpoints.set.join(' / ')}; lineage isolated`);
