/* Native-First: evaluate the frozen case package; write only this lane's file. */
"use strict";
const fs = require('fs'), path = require('path');
const B = require('../main_case_2026_10_14/package.cjs');
const payload = B.correctionsPayload(), m = B.payloadModel();
const summary = JSON.parse(fs.readFileSync(path.join(__dirname,'../main_case_2026_10_14/derived/summary.json')));
const ids = ['general_sales_tax','excise_selective_sales','customs_duties','personal_current_transfers'];
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
const bands={}, responses={};
for(const [name,api] of [['set',B],['cash',B.CASH]]) {
  const own=api.MAIN_SPECS || B.MAIN_SPECS;
  const costs=own.map(s=>api.evaluateFull(api.payloadModel(),s,B.CENTRAL.profile).cost_bn);
  const low=costs.indexOf(Math.min(...costs)), high=costs.indexOf(Math.max(...costs));
  bands[name]=[costs[low],costs[high]];
  responses[name]=[low,high].map(i=>Object.fromEntries(api.evaluateFull(api.payloadModel(),own[i],B.CENTRAL.profile)
    .evaluation.receipts.filter(r=>ids.includes(r.id)).map(r=>[r.id,r.response])));
  endpoints[name]=[low,high];
}
const out={case:'oct14',allocation:'personal',lines,bands,responses,endpoints,lineage:L,
           child_credits:payload.meta.child_credits};
fs.mkdirSync(path.join(__dirname,'derived'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'derived/case_inputs.json'),JSON.stringify(out,null,2)+'\n');
console.log(`[case] ${bands.set.join(' / ')}; ends ${endpoints.set.join(' / ')}; lineage isolated`);
