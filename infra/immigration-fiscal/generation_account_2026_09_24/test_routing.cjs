"use strict";
const test=require("node:test"),assert=require("node:assert/strict"),path=require("path"),fs=require("fs");
const {spawnSync}=require("child_process");
const V=require("./v7_split.cjs"),A=require("./age_routing.cjs");
const clone=x=>JSON.parse(JSON.stringify(x));

test("atomic output keeps published bytes on serialization failure and until rename",()=> {
  const dir=fs.mkdtempSync(path.join(require("os").tmpdir(),"gen-publish-"));
  const file=path.join(dir,"out.json"),{publish}=require("./atomic_file_v8.cjs");
  try {
    fs.writeFileSync(file,"old\n");
    assert.throws(()=>publish(file,()=>{ throw Error("serialization failed"); }),/serialization failed/);
    assert.equal(fs.readFileSync(file,"utf8"),"old\n");
    publish(file,()=>{assert.equal(fs.readFileSync(file,"utf8"),"old\n");return "new\n";});
    assert.equal(fs.readFileSync(file,"utf8"),"new\n");
    assert.deepEqual(fs.readdirSync(dir),["out.json"]);
  } finally {fs.rmSync(dir,{recursive:true,force:true});}
});

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

test("v8 declarations reject unknown owners and changed source cells",()=> {
  const W=require("./v8_split.cjs"),L=W.loadCase("set"),it=L.added.find(i=>i.id==="union_completion");
  const [name,p]=Object.entries(it.record.parts)[0],e=it.edits[p.edit];
  assert.equal(W.routeFor("set",it,name,p,e).generation,"G3plus");
  assert.throws(()=>W.routeFor("set",it,"lineage_g3plus:undeclared",p,e),/\[BLOCKED\].*unrouted/);
  assert.throws(()=>W.routeFor("set",it,name,p,{...e,line:"unknown_carrier"}),/\[BLOCKED\]/);
});

test("post-engine changes are added once and excluded from uncorrected models",()=> {
  const W=require("./v8_split.cjs"),L=W.loadCase("set"),E=W.evaluator(L.payload,L.api);
  const cp=JSON.parse(fs.readFileSync(path.join(__dirname,"derived/generation_corrections_oct15.json"),"utf8"));
  const spec=E.specs[16],results=["G1","G2","G3plus"].map(g=> {
    const base=JSON.parse(fs.readFileSync(path.join(__dirname,`derived/model_${g}.json`),"utf8"));
    const zero=E.evaluateFull(base,spec);assert.equal(zero.post_engine.total_bn,0);
    return E.evaluateFull(W.X.Engine.applyCorrections(base,cp.payloads.a[g]),spec);
  });
  const union=E.evaluateFull(W.X.Engine.applyCorrections(W.X.MODEL,L.payload),spec);
  assert(Math.abs(results.reduce((s,r)=>s+r.cost_bn,0)-union.cost_bn)<1e-9);
  assert(Math.abs(results.reduce((s,r)=>s+r.post_engine.total_bn,0)-union.post_engine.total_bn)<1e-9);
  for(const g of ["G1","G2","G3plus"]) {
    const z=cp.payloads.a[g].meta.mixed_unit_removal.by_end.low;
    const variance=4/160*z.replicates_bn.slice(1).reduce((v,n)=>v+(n-z.replicates_bn[0])**2,0);
    assert(Math.abs(Math.sqrt(variance)-z.se_bn)<1e-9);
    assert.equal(z.source_total_bn,L.payload.meta.mixed_unit_removal.by_end.low.total_bn);
  }
});

test("non-central policies cannot overwrite canonical output, even with explicit out-dir",()=> {
  for(const args of [["--fixes","none"],["--production-rule","labour_income","--out-dir",path.join(__dirname,"derived")]]) {
    const p=spawnSync(process.execPath,[path.join(__dirname,"run_generations_v8.cjs"),...args],{encoding:"utf8"});
    assert.notEqual(p.status,0,p.stdout+p.stderr);
    assert.match(p.stderr,/non-central routing requires --out-dir/);
  }
});

test("new reporter minors follow their measured parent destinations and conserve people",()=> {
  const W=require("./v8_split.cjs"),L=W.loadCase("set"),counts=W.reporterPopulation(L);
  const source=L.payload.meta.union_completion.observed_records.filter(r=>!r.observed_nonreporter);
  assert(Math.abs(Object.values(counts).reduce((s,v)=>s+v,0)-source.reduce((s,r)=>s+r.people,0))<1e-6);
  assert(counts.G1>12000 && counts.G2>135000);
  assert.throws(()=>W.reporterPopulation({...L,payload:{meta:{union_completion:{observed_records:source.slice(1)}}}}),/\[BLOCKED\].*record coverage/);
});

test("capital-reference guard handles quoted source notes without parsing JSON strings",()=> {
  const W=require("./v8_split.cjs");
  const values=W.stringLeaves({note:'BEA says "enterprise surplus"',components:[{key:{parent_line:"carrier"}}]});
  assert(values.includes('BEA says "enterprise surplus"'));
  assert(values.includes("carrier"));
});

test("metadata-efficient steps and zero padding exactly match the original engine on real final models",()=> {
  const W=require("./v8_split.cjs");
  for(const [basis,suffix] of [["set",""],["cash","_cash"]]) {
    const Q=basis==="set"?W.P8:W.P8.CASH;
    const cp=JSON.parse(fs.readFileSync(path.join(__dirname,`derived/generation_corrections_oct15${suffix}.json`)));
    for(const c of ["a","b"])for(const g of ["G1","G2","G3plus"]) {
      const base=JSON.parse(fs.readFileSync(path.join(__dirname,`derived/model_${c==="b"?"b_":""}${g}.json`)));
      const m=W.X.Engine.applyCorrections(base,cp.payloads[c][g]),before=JSON.stringify(m);
      assert.deepEqual(W.padSynthetic(Q,m),Q.withSyntheticLines(m));
      const e={side:"spending",line:"union_completion_health_services_health_other",key:"k",by:{personal:.1,shared:-.2}};
      assert.deepEqual(W.withStep(m,[e]),W.X.Engine.applyCorrections(m,{lines:[],receipt_lines:[],edits:[e],meta:m.corrections}));
      assert.equal(JSON.stringify(m),before);
    }
  }
});
