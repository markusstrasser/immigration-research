/* Read-only v7 inventory. Union intercept uses the frozen lineage_addition.cjs
 * affine-count construction at the lineage's responses; national budgets hold. */
"use strict";
const fs=require('fs'), path=require('path'), crypto=require('crypto');
const F=path.resolve(__dirname,'..'), P=require(path.join(F,'main_case_2026_10_14/package.cjs'));
const V4=require(path.join(F,'main_case_candidate_v4_2026_09_29/package.cjs'));
const B=P.OCT05, POP=B.POP, {Engine,MODEL,METHODS}=P;
const TOOLS={OCT05:B,Engine,MODEL,METHODS,readJson:B.readJson,sha256:B.sha256};
const REG=new Map(P.REGISTRY.map(x=>[x.id,x]));
const V6IDS=new Set(P.V6_PACKAGE.REGISTRY.map(x=>x.id));
const clone=x=>JSON.parse(JSON.stringify(x));
const AB=POP.arms[POP.meta.central_arm], GATES=[];
function gate(name,ok,detail=null){GATES.push({name,pass:!!ok,detail});if(!ok)throw Error('[BLOCKED] '+name+' '+JSON.stringify(detail));}
function variant(name,later,g3){
 const Bx=Object.create(B), A=Object.assign(clone(AB),{source_arm:name,later,g3_rate:g3,added:later+g3,population:POP.meta.account_union+later+g3,added_cps:null});
 Bx.POP=Object.assign({},POP,{arms:Object.assign({},POP.arms,{[name]:A})});
 const additions=P.COUNT.additionsAt(Bx,name,clone(POP.c3),TOOLS), L=additions.set.meta.lineage;
 const opt={name,label:name,arm:name,A,C3:POP.c3.value,c3:clone(POP.c3),m_g3plus:L.m_g3plus,m_white:L.m_white,additions,
  meta:{name,label:name,arm:name,source_arm:name,added:A.added,g3_rate:g3,later,population:A.population,c3:POP.c3.value,s:L.s,k_metro:L.k_metro,m_g3plus:L.m_g3plus,m_white:L.m_white}};
 const items=P.V6_PACKAGE.CANDIDATE.map(id=>REG.get(id)),lin=items.find(it=>it.kind==='lineage');
 const lb=P.checkLineage(lin,lin.build(Object.assign({B,LINEAGE_OPTION:opt},TOOLS),null),B,opt.additions);lb.option=opt;
 const rebased=P.rebase(B,lb),ctx=Object.assign({B:rebased,LINEAGE_ITEM:lin.id},TOOLS);
 const built=items.map(item=>item.kind==='lineage'?{item,arm:null,lineage:lb}:{item,arm:null,set:P.checkBuilt(item,item.build(ctx,null,'set'),rebased,'set'),cash:item.cash.applies?P.checkBuilt(item,item.build(ctx,null,'cash'),rebased,'cash'):null});
 const set=P.forItems(rebased,built,'set',false,opt),cash=P.forItems(rebased.CASH,built,'cash',false,opt);
 const detail=Object.fromEntries(built.map(b=>[b.item.id,b.item.kind==='lineage'?b.lineage.detail:{set:b.set.detail,cash:b.cash?b.cash.detail:null}]));
 const q=Object.assign(set,{CASH:cash,CASH_PAYLOAD:cash.correctionsPayload(),OCT05:B,ITEM_BASE:rebased,ITEM_IDS:built.map(b=>b.item.id),ITEM_ARMS:{},LINEAGE_ITEM:lin.id,ITEM_DETAIL:detail,LINEAGE_OPTION:name,LINEAGE_OPTION_META:clone(opt.meta)});
 return P.caseOn(q,P.CANDIDATE.filter(id=>!V6IDS.has(id)),{},'variant',name);
}
const later=variant('bizserv_later',AB.later,0),g3=variant('bizserv_g3',0,AB.g3_rate);
const oracle=JSON.parse(fs.readFileSync(path.join(F,'main_case_2026_10_14/derived/lineage_addition.json')));
const main=JSON.parse(fs.readFileSync(path.join(F,'main_case_2026_10_14/derived/summary.json')));
const meta=P.correctionsPayload().meta, out=[];
function affine(a,b,c){return a+b-c;}
for(const method of METHODS){
 const preRoad=V4.modelFor('central',method,V4.withCentral({roads:V4.OFF.roads}));
 const directUnionRoadKeys=V4.roadKeysOf(preRoad).personal;
 const models=[P,later,g3].map(q=>q.modelFor('central',method,q.withCentral({})));
 for(const [end,index] of [['low',16],['high',11]]){
  const runs=[P,later,g3].map((q,i)=>q.evaluateFull(models[i],q.MAIN_SPECS[index],P.MAIN_PROFILE));
  const [full,l,g]=runs;
  const sum=(side,id,field)=>affine(l[side].find(x=>x.id===id)[field],g[side].find(x=>x.id===id)[field],full[side].find(x=>x.id===id)[field]);
  const spending=full.evaluation.spending.map(row=>{
   const a=l.evaluation.spending.find(x=>x.id===row.id),b=g.evaluation.spending.find(x=>x.id===row.id);
   gate(`spending national fixed ${method} ${end} ${row.id}`,Math.abs(row.national_bn-a.national_bn)<1e-9&&Math.abs(row.national_bn-b.national_bn)<1e-9);
   const union=affine(a.amount_bn,b.amount_bn,row.amount_bn);
   return Object.assign({},row,{union_amount_bn:union,union_charge_bn:union*row.response,lineage_charge_bn:row.amount_bn*row.response,added_charge_bn:(row.amount_bn-union)*row.response});
  });
  const capital=full.capital.components.map(row=>{
   const a=l.capital.components.find(x=>x.id===row.id),b=g.capital.components.find(x=>x.id===row.id);
   gate(`capital fixed ${method} ${end} ${row.id}`,Math.abs(row.stock_charged_bn-a.stock_charged_bn)<1e-9&&Math.abs(row.stock_charged_bn-b.stock_charged_bn)<1e-9&&row.response===a.response&&row.response===b.response);
   return Object.assign({},row,{union_key:affine(a.key,b.key,row.key),union_return_bn:affine(a.return_bn,b.return_bn,row.return_bn),key_rule:meta.capital_return.components.find(x=>x.id===row.id).key,response_rule:meta.capital_return.components.find(x=>x.id===row.id).response});
  });
  const receipts=full.evaluation.receipts.map(row=>{const a=l.evaluation.receipts.find(x=>x.id===row.id),b=g.evaluation.receipts.find(x=>x.id===row.id);return Object.assign({},row,{union_amount_bn:affine(a.amount_bn,b.amount_bn,row.amount_bn)});});
  out.push({method,end,index,spec:clone(P.MAIN_SPECS[index]),direct_union_road_keys:directUnionRoadKeys,cost_bn:full.cost_bn,union_at_case_responses_bn:affine(l.cost_bn,g.cost_bn,full.cost_bn),spending,capital,receipts});
 }
}
for(const [e,end] of ['low','high'].entries()){
 const xs=out.filter(x=>x.end===end),mean=field=>xs.reduce((a,x)=>a+x[field],0)/xs.length;
 gate(`positive control v7 ${end}`,Math.abs(mean('cost_bn')-oracle.set.case_bn[e])<1e-9);
 gate(`positive control union intercept ${end}`,Math.abs(mean('union_at_case_responses_bn')-oracle.set.union_at_case_responses_bn[e])<1e-9);
}
const inputFiles=['main_case_2026_10_14/derived/corrections.json','main_case_2026_10_14/derived/summary.json','main_case_2026_10_14/derived/lineage_addition.json','main_case_2026_10_14/package.cjs','main_case_2026_10_14/lineage_addition.cjs'];
const hashes=Object.fromEntries(inputFiles.map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(path.join(F,f))).digest('hex')]));
fs.mkdirSync(path.join(__dirname,'derived'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'derived/inventory.json'),JSON.stringify({case:'oct14',frame:{union:POP.meta.account_union,lineage:AB.population,union_response:'held at lineage case responses'},added_wage_shares:P.ITEM_DETAIL.job_capital_taxes.set.wage_share,meta,responses:meta.responses,runs:out,gates:GATES,inputs_sha256:hashes},null,2)+'\n');
const esc=x=>'"'+String(x??'').replaceAll('"','""')+'"';
const rows=[['type','id','method','end','key','response','national_or_stock_bn','union_charge_bn','lineage_charge_bn']];
for(const r of out){for(const x of r.spending)rows.push(['spending',x.id,r.method,r.end,x.key,x.response,x.national_bn,x.union_charge_bn,x.lineage_charge_bn]);for(const x of r.capital)rows.push(['capital',x.id,r.method,r.end,JSON.stringify(x.key_rule),x.response,x.stock_charged_bn,x.union_return_bn,x.return_bn]);}
fs.writeFileSync(path.join(__dirname,'derived/inventory.csv'),rows.map(x=>x.map(esc).join(',')).join('\n')+'\n');
console.log(`PASS ${GATES.length} gates; v7 and union intercept reproduced; inventory written`);
