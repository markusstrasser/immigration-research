"use strict";
const test=require("node:test"),assert=require("node:assert/strict"),G=require("./native_parent_gradients_v8.cjs");
const fs=require("fs"),path=require("path"),os=require("os");
const {requireAdopted}=require("../scripts/adoption_gate.cjs");
test("native source bounds choose a feasible whole-person direction",()=> {
 assert.equal(G.direction(100,100),-1);assert.equal(G.direction(100,0),1);
 assert.throws(()=>G.direction(100,101),/invalid source/);
});
test("native perturbation preserves all other bands and caller input",()=> {
 const counts={g3_rate:Array(17).fill(3),later:Array(17).fill(0)},before=JSON.stringify(counts);
 const changed=G.perturb(counts,"g3_rate",2,-1);
 assert.equal(changed.g3_rate[2],2);assert.equal(changed.g3_rate[3],3);
 assert.equal(JSON.stringify(counts),before);
});
test("full-cost derivative signs and conservation reject a third-party spill",()=> {
 const base={G1:100,G2:50,G3plus:70},changed={G1:100,G2:50.00002,G3plus:69.99998};
 const slope=G.slope(base,changed,1);G.requireConservation(slope);
 assert(slope.G2>0&&slope.G3plus<0);
 assert.throws(()=>G.requireConservation({...slope,G1:.01}),/nonconserving derivative/);
});
test("a superseded live key stops before numerical work or output publication",()=> {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"native-stale-adoption-"));
 try {
  const livePath=path.join(dir,"live_case.json");fs.writeFileSync(livePath,JSON.stringify({key:"future"}));
  assert.throws(()=>G.run({adoptionOptions:{livePath}}),/live key future does not match consumed case oct15/);
 } finally {fs.rmSync(dir,{recursive:true,force:true});}
});
test("candidate package blocks and matching adopted metadata authorizes the case",()=> {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"native-adoption-"));
 try {
  const livePath=path.join(dir,"live_case.json"),declaration={key:"oct15",lane:"case",adopted:"2026-10-15",decision:"decisions/case.md"};
  fs.writeFileSync(livePath,JSON.stringify(declaration));
  assert.throws(()=>G.run({adoptionOptions:{livePath,packageApi:{STATUS:"candidate"}}}),/STATUS is not adopted/);
  assert.deepEqual(requireAdopted("oct15",{livePath,packageApi:{STATUS:"adopted",ADOPTED:declaration.adopted,DECISION:declaration.decision,CASE_KEY:"oct15",LANE:"case"}}),
   {key:"oct15",adopted:declaration.adopted,decision:declaration.decision});
 } finally {fs.rmSync(dir,{recursive:true,force:true});}
});
