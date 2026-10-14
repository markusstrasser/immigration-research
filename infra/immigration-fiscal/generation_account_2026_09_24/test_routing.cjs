"use strict";
const test=require("node:test"),assert=require("node:assert/strict"),path=require("path"),fs=require("fs");
const {spawnSync}=require("child_process");
const V=require("./v7_split.cjs"),A=require("./age_routing.cjs");
const clone=x=>JSON.parse(JSON.stringify(x));

test("unknown lineage-like and union-like parts fail closed",()=> {
  const L=V.loadCase("set"),it=L.added.find(it=>it.id==="child_credits");
  const [name,p]=Object.entries(it.record.parts)[0],e=it.edits[p.edit];
  assert.equal(V.routeFor("set",it,name,p,e).generation,"G1");
  for(const unknown of ["lineage_unknown:anything","union_G2:new_part",""])
    assert.throws(()=>V.routeFor("set",it,unknown,p,e),/\[BLOCKED\].*unrouted/);
});

test("changed route amount or edit identity cannot reuse a declared route",()=> {
  const L=V.loadCase("cash"),it=L.added.find(it=>it.id==="row4_frame");
  const [name,p]=Object.entries(it.record.parts)[0],e=it.edits[p.edit];
  const q=clone(p);q.by.personal+=1;
  assert.throws(()=>V.routeFor("cash",it,name,q,e),/\[BLOCKED\]/);
  assert.throws(()=>V.routeFor("cash",it,name,p,{...e,scenario:"unknown"}),/\[BLOCKED\]/);
});

test("both lineage age decompositions reconstruct the frozen cells and conserve people",()=> {
  for(const set of ["set","cash"]) {
    const L=V.loadCase(set),age=A.build(L);
    assert(age.diagnostics.cell_rebuild_gap_bn<1e-9);
    assert(age.minor_count>0 && age.minor_count<L.lineage.counts.at_g3_rate);
    assert(age.production_minor_share>=0 && age.production_minor_share<1);
    assert(age.floor_fraction>0 && age.floor_fraction<1);
    assert(Math.abs(age.adults.by_part.g3_rate+age.minor_count-L.lineage.counts.at_g3_rate)<1e-6);
  }
});

test("measurement wrapper retains a child failure",()=> {
  const p=spawnSync("uv",["run","--no-project","python3",path.join(__dirname,"measured_run.py"),process.execPath,"-e","process.exit(7)"],{encoding:"utf8"});
  assert.equal(p.status,7,p.stdout+p.stderr);
  assert.match(p.stdout,/exit=7/);
});

test("a production sensitivity cannot mutate the frozen source payload",()=> {
  const source={lines:[],edits:[],production:{dims:{},private_wtp_bn:[1],induced_receipts_bn:[2],sampling_se_bn:[null]}};
  const p=V.payloadOf(source,{edits:[],production:null,receipt_lines:[]});
  p.production.private_wtp_bn[0]=99;
  assert.equal(source.production.private_wtp_bn[0],1);
});

test("state-price principal controls pass and every generation has 161 finite indexes",()=> {
  const x=JSON.parse(fs.readFileSync(path.join(__dirname,"derived/generation_state_indexes.json"),"utf8"));
  assert.equal(x.positive_controls.length,9);
  assert(x.positive_controls.every(c=>c.pass));
  for(const conv of Object.values(x.conventions)) for(const functionName of Object.values(conv)) for(const g of Object.values(functionName)) {
    assert.equal(g.replicates.length,161);assert(g.replicates.every(Number.isFinite));
  }
});
