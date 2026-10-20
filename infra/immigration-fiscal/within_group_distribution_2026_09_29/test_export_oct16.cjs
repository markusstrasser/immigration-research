/* Deterministic source-contract negatives; does not execute any case producer. */
"use strict";
const assert=require("node:assert/strict"),fs=require("fs"),path=require("path");
const X=require("./export_oct16.cjs"),sum=a=>a.reduce((s,v)=>s+v,0);
const C=require("./export_controls_oct16.cjs");
const root=path.join(__dirname,"_cache");
fs.mkdirSync(root,{recursive:true});
const scratch=fs.mkdtempSync(path.join(root,"oct16-contract-"));
const relative=name=>path.relative(path.resolve(__dirname,".."),path.join(scratch,name));
try{
  const name="counts.csv",csv=["scenario,end,generation,line,source_line,source_side,category,economic_class,source_key,observed_change_bn,coverage_change_bn,change_bn",
    "joint,low,G2,health_services,health_services,spending,health,fiscal_line,health_consumption,2,-2,0",
    "item16,low,G2,health_services,health_services,spending,health,fiscal_line,health_consumption,1,-1,0"];
  fs.writeFileSync(path.join(scratch,name),csv.join("\n")+"\n");
  const block={parts_file:relative(name),parts_scenario:"joint",subtract_parts_scenario:"item16",by_end:{low:{total_bn:0}}};
  const api={correctionsPayload:()=>({meta:{coverage_tenure:block}})};
  const parts=X.countRows(api,"coverage_tenure","low");
  assert.equal(sum(parts.map(r=>r.cost_bn)),0);
  assert.equal(sum(parts.filter(r=>r.population==="observed").map(r=>r.cost_bn)),1);
  assert.equal(sum(parts.filter(r=>r.population==="coverage").map(r=>r.cost_bn)),-1);
  assert.equal(parts.length,4,"zero-net atoms retain their separate population changes and subtraction sign");
  assert.ok(parts.every(r=>r.generation==="G2"&&r.source_line==="health_services"&&r.source_key==="health_consumption"));
  block.by_end.low.total_bn=1;
  assert.throws(()=>X.countRows(api,"coverage_tenure","low"),/selected count-source closure/);
  block.by_end.low.total_bn=0;
  const source=relative(name),make=value=>({file:source,by_end:{low:{decomposition:{line_parts:[{line:"health_services",source_line:"health_services",source_side:"spending",generation:"G2",coverage_bn:value}]}}}});
  const coverage=X.coverageRows(make(10),make(7),"low");
  assert.equal(sum(coverage.map(r=>r.cost_bn)),-3);
  assert.ok(coverage.every(r=>r.population==="coverage"));
  assert.deepEqual(coverage.map(r=>r.source.origin),["current","scaffold"]);
  assert.deepEqual(X.coverageRows(make(7),make(7),"low"),[],"identical source coverage contributes no phantom control rows");
  const sparse=value=>({file:source,by_end:{low:{decomposition:{line_parts:[{end:"low",generation:"G1",line:"lane_residual",economic_class:"unclassified_residual",level:"unclassified",coverage_bn:value}]}}}});
  const residual=X.coverageRows(sparse(-0.10738761585266496),sparse(0),"low")[0];
  assert.equal(residual.source_line,"lane_residual");assert.equal(residual.source_side,"post_engine");assert.equal(residual.population,"coverage");
  assert.equal(residual.cost_bn,0.10738761585266496);assert.equal(X.validateAtom(residual),residual);
  const unknown=sparse(1);unknown.by_end.low.decomposition.line_parts[0].economic_class="unknown_class";
  assert.throws(()=>X.validateAtom(X.coverageRows(sparse(0),unknown,"low")[0]),/incomplete typed source atom/,
    "missing source fields are normalized only for the source-declared residual class");
  const countsPayload={meta:{coverage:{counts_by_generation:{G1:10,G2:20,G3plus:30,added:4}},native_minor_calibration:{coverage_people_change_by_generation:{G2:-1}},coverage_tenure:{coverage_people_change_by_generation:{G3plus:2}},
    population_v9:{with_coverage:1000,without_coverage:935,coverage:64}}};
  const originalCounts=JSON.stringify(countsPayload);
  assert.deepEqual(X.finalCoverageCounts(countsPayload),{G1:10,G2:19,G3plus:36});
  assert.equal(sum(Object.values(X.finalCoverageCounts(countsPayload))),countsPayload.meta.population_v9.with_coverage-countsPayload.meta.population_v9.without_coverage,
    "final count follows with-minus-without, despite a retained stale coverage scalar");
  assert.equal(JSON.stringify(countsPayload),originalCounts,"source four-part counts and source population are read-only");
  const foldedPayload=structuredClone(countsPayload);
  foldedPayload.meta.coverage.counts_by_generation_folded={G1:10,G2:20,G3plus:34};
  assert.deepEqual(X.finalCoverageCounts(foldedPayload),{G1:10,G2:19,G3plus:36},"pre-folded added count must never be stacked again");
  const calls=[],old={CANDIDATE:["old1","old2"]},mock={NEW_IDS:["new1","passthrough_source_tax"],CANDIDATE:["old1","old2","new1"],OCT15:old,OCT05:{},caseOf:(b,ids)=>{assert.equal(b,mock.OCT05);calls.push(ids);return {ids};}};
  assert.equal(C.selection(mock,"none").api,old,"none preserves exact inherited source API");
  assert.deepEqual(C.selection(mock,"new1").ids,["old1","old2","new1"]);
  assert.deepEqual(calls,[["old1","old2","new1"]]);
  assert.deepEqual(old.CANDIDATE,["old1","old2"],"one-item control preserves inherited selected registry");
  assert.throws(()=>C.selection(mock,"passthrough_source_tax"),/selected central new item/,"item19 remains beside");
  assert.throws(()=>C.selection(mock,"unknown"),/selected central new item/);
  assert.throws(()=>C.validateSnapshot({meta:{}},"set","personal"),/fresh central export/);
  const keys=["source_payload","source_generation","scaffold_source_payload","scaffold_source_generation","scaffold_export_source","scaffold_bridge_source"];
  const snapshot={meta:{case:"main_case_2026_10_16",basis:"set",allocation:"personal",v9:{control_item:null,
    ...Object.fromEntries(keys.map(k=>[k,{...X.signature(source)}]))}}};
  assert.equal(C.validateSnapshot(snapshot,"set","personal"),snapshot);
  for(const key of keys){
    const stale=structuredClone(snapshot);stale.meta.v9[key].sha256="stale";
    assert.throws(()=>C.validateSnapshot(stale,"set","personal"),new RegExp("stale central scaffold source "+key));
    const missing=structuredClone(snapshot);delete missing.meta.v9[key];
    assert.throws(()=>C.validateSnapshot(missing,"set","personal"),new RegExp("stale central scaffold source "+key));
  }
  for(const [field,value]of [["case","old-case"],["basis","cash"],["allocation","shared"]]){
    const wrong=structuredClone(snapshot);wrong.meta[field]=value;
    assert.throws(()=>C.validateSnapshot(wrong,"set","personal"),/fresh central export/);
  }
  const nestedControl=structuredClone(snapshot);nestedControl.meta.v9.control_item="new1";
  assert.throws(()=>C.validateSnapshot(nestedControl,"set","personal"),/fresh central export/,"a control cannot replace the central source scaffold");
  // Same-process cache must not turn changed source bytes into a valid receipt.
  fs.appendFileSync(path.join(scratch,name),"changed-source-bytes\n");
  assert.throws(()=>C.validateSnapshot(snapshot,"set","personal"),/stale central scaffold source source_payload/);
  const atom={item:"one_rate",line:"college",source_line:"college",source_side:"capital",population:"engine",generation:"G2",cost_bn:1};
  assert.equal(X.sideOf({side:"capital",source_side:"spending",line:"health_sl"},[]),"capital","source21 explicit side precedes legacy hints");
  assert.equal(X.sideOf({side:"spending",line:"health_services"},[{id:"health_services"}]),"spending","declared spending precedes inferred capital");
  assert.equal(X.sideOf({source_side:"receipt"},[]),"receipt","legacy explicit source_side remains supported");
  assert.equal(X.sideOf({kind:"college_capital"},[]),"capital","legacy college inference remains supported");
  for(const side of ["unknown",null,""])assert.throws(()=>X.sideOf({side,source_side:"capital"},[]),/unknown declared source side/);
  assert.throws(()=>X.sideOf({source_side:"unknown"},[]),/unknown declared source side/);
  for(const population of ["original_union","added_lineage","completion"]){
    const health={...atom,item:"health_residual_key",line:"health_sl",source_line:"health_sl",population,
      ...(population==="completion"?{profile:"native_nonreporters"}:{})};
    assert.equal(X.validateAtom(health),health,"source21 population/profile declarations remain inspectable");
  }
  assert.equal(X.validateAtom(atom),atom);
  for(const field of ["item","line","source_line","source_side","population","generation"]){const bad={...atom};delete bad[field];assert.throws(()=>X.validateAtom(bad),/incomplete typed source atom/);}
  assert.throws(()=>X.validateAtom({...atom,cost_bn:NaN}),/incomplete typed source atom/);
  assert.throws(()=>X.validateAtom({...atom,generation:"G4"}),/incomplete typed source atom/);
  assert.throws(()=>X.validateAtom({...atom,source_side:"unspecified"}),/unknown typed source route/);
  assert.throws(()=>X.validateAtom({...atom,population:"unspecified"}),/unknown typed source route/);
  console.log("oct16 export contracts PASS: signed source atoms, standalone selection, four-count closure, cached-byte drift and snapshot/route negatives");
}finally{fs.rmSync(scratch,{recursive:true,force:true});}
