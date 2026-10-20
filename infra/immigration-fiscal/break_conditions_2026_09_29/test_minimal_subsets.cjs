"use strict";
const assert=require("assert/strict"),{minimalCrossings}=require("./minimal_subsets.cjs");
const {validateGenerationPayloads}=require("./generation_preflight.cjs");
const canonical=cuts=>cuts.map(c=>c.set.slice().sort().join("+")).sort();
function brute(groups,bandOf,crosses) {
  const all=[];
  function walk(i,set) {
    if(i===groups.length){if(set.length){const b=bandOf(set);if(crosses(b))all.push({set:set.slice(),b});}return;}
    walk(i+1,set);for(const id of groups[i]){set.push(id);walk(i+1,set);set.pop();}
  }
  walk(0,[]);
  return all.filter(x=>!all.some(y=>y.set.length<x.set.length&&y.set.every(id=>x.set.includes(id))));
}
let seed=912345;
const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/2**32;};
for(let trial=0;trial<80;trial++) {
  const groups=Array.from({length:6},(_,i)=>Array.from({length:1+(i%2)},(_,j)=>`${i}_${j}`));
  const weights=Object.fromEntries(groups.flat().map(id=>[id,Math.floor(random()*11)-4]));
  // A cardinality interaction deliberately makes crossing nonmonotonic.
  const band=set=>{const v=set.reduce((n,id)=>n+weights[id],0)+(set.length%3===0?-8:0);return [v,v];};
  const crosses=b=>b[0]>8;
  assert.deepEqual(canonical(minimalCrossings(groups,band,crosses).cuts),canonical(brute(groups,band,crosses)));
}
for(let trial=0;trial<40;trial++) {
  const groups=Array.from({length:7},(_,i)=>Array.from({length:1+(i%3)},(_,j)=>`${i}_${j}`));
  const weights=Object.fromEntries(groups.flat().map(id=>[id,Math.floor(random()*9)-3]));
  const band=set=>{const v=set.reduce((n,id)=>n+weights[id],0)+(set.length%2?0:-3);return [v,v];};
  const crosses=b=>b[0]>5;
  for(const cap of [1,2,3]) {
    const r=minimalCrossings(groups,band,crosses,null,cap);
    assert.deepEqual(canonical(r.cuts),canonical(brute(groups,band,crosses).filter(x=>x.set.length<=cap)));
    assert.equal(r.counts.max_size_searched,cap);assert.equal(r.counts.complete,false);assert.match(r.proof,/not enumerated/);
  }
}
assert.equal(minimalCrossings([["a"],["b"]],s=>[s.length,s.length],b=>b[0]>1).counts.complete,true);
assert.throws(()=>minimalCrossings([["a"]],()=>[0,0],()=>false,null,0),/size cap/);
const many=[Array.from({length:40},(_,i)=>`exclusive_${i}`),["independent"]];
const tested=minimalCrossings(many,set=>[set.length,set.length],b=>b[0]>1);
assert.equal(tested.cuts.length,40);
assert.equal(tested.counts.eligible_nonempty_sets,"81");
assert(tested.cuts.every(c=>c.set.includes("independent")&&c.set.length===2));
assert.throws(()=>minimalCrossings([["duplicate"],["duplicate"]],()=>[0,0],()=>false),/disjoint/);
assert.throws(()=>minimalCrossings([["id"]],()=>[NaN,0],()=>false),/finite pair/);
const full={adopted:"2026-10-15",mixed_unit_removal:{by_end:{low:{total_bn:3},high:{total_bn:6}}},coverage:{by_end:{low:{total_bn:3},high:{total_bn:6}}}};
const generation=()=>Object.fromEntries(["a","b"].map(conv=>[conv,Object.fromEntries(["G1","G2","G3plus"].map(g=>[g,{meta:{generation:g,case_key:"oct15",adopted:"2026-10-15",mixed_unit_removal:{by_end:{low:{total_bn:1},high:{total_bn:2}}},coverage:{by_end:{low:{total_bn:1},high:{total_bn:2}}}}}]))]));
validateGenerationPayloads(generation(),full,"oct15");
const missing=generation();delete missing.a.G1.meta.coverage;
assert.throws(()=>validateGenerationPayloads(missing,full,"oct15"),/missing coverage/);
const stale=generation();stale.a.G1.meta.adopted=null;
assert.throws(()=>validateGenerationPayloads(stale,full,"oct15"),/unverified inherited adoption stamp/);
const wrongCase=generation();wrongCase.a.G1.meta.case_key="oct14";
assert.throws(()=>validateGenerationPayloads(wrongCase,full,"oct15"),/stale case\/generation stamp/);
const changed=generation();changed.b.G3plus.meta.coverage.by_end.low.total_bn=2;
assert.throws(()=>validateGenerationPayloads(changed,full,"oct15"),/unclosed coverage/);
console.log("[gates] exact grouped search matches 80 brute-force nonmonotonic spaces and 120 size-capped ones; 41-arm test and fail-loud controls pass");
console.log("[gates] generation freshness/coverage/sum negative controls pass before engine work");
