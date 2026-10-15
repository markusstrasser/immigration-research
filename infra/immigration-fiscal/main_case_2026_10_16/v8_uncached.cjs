/* v8.caseOf's exact construction through its exported layer, without retaining
 * variant bases. G3 uses this scheduling route; v8's modules stay untouched. */
"use strict";
const V8=require("./v8_bounded_runtime.cjs").packageFor(),V7=V8.V7_PACKAGE;
const clone=x=>JSON.parse(JSON.stringify(x));
const fail=s=>{throw Error(`[BLOCKED] v8: ${s}`);};
function caseOf(B,ids,sel={},lineage){
 const REGISTRY=V8.REGISTRY,NEW_IDS=V8.NEW_IDS;
 const order=ids.map(id=>REGISTRY.findIndex(x=>x.id===id));
 if(order.some((n,i)=>n<0||(i>0&&n<=order[i-1])))fail("unknown/duplicate/out-of-order item");
 for(const [id,arm]of Object.entries(sel))if(!ids.includes(id)||!REGISTRY.find(x=>x.id===id)?.arms[arm])fail(`unknown arm ${id}:${arm}`);
 const old=ids.filter(id=>!NEW_IDS.includes(id));
 const oldSel=Object.fromEntries(Object.entries(sel).filter(([id])=>!NEW_IDS.includes(id)));
 const Q=V7.caseOf(B,old,oldSel,lineage);
 const next=ids.filter(id=>NEW_IDS.includes(id));
 if(!next.length)return Q;
 const ctx={B:Q,DETAIL:Q.ITEM_DETAIL,Engine:V7.Engine,MODEL:V7.MODEL,METHODS:V7.METHODS,readJson:V7.readJson,sha256:V7.sha256};
 const pieces=next.map(id=>({item:REGISTRY.find(x=>x.id===id),arm:sel[id]||null}));
 const identity={stamp:JSON.stringify(ids)===JSON.stringify(V8.CANDIDATE)&&!Object.keys(sel).length&&!lineage?V8.V8.STATUS:"variant"};
 const built=which=>pieces.map(b=>({...b,x:b.item.build(ctx,b.arm,which)}));
 const set=V8.forItems8(Q,built("set"),"set",identity),cash=V8.forItems8(Q.CASH,built("cash"),"cash",identity);
 return {...set,CASH:cash,CASH_PAYLOAD:cash.correctionsPayload(),OCT14:Q,OCT14_CASH:Q.CASH,ITEM_IDS:old.concat(next),ITEM_ARMS:clone(sel),ITEM_DETAIL:Q.ITEM_DETAIL,V8_IDS:next};
}
module.exports={caseOf};
