/* Production additions retain the complete model's grid and do not mutate inputs. */
"use strict";
const assert=require("node:assert/strict"),fs=require("fs"),path=require("path");
const C=require("./v8_cells.cjs");
const model=JSON.parse(fs.readFileSync(path.join(__dirname,"_cache/split_central/model_G3plus.json"),"utf8"));
const before=JSON.stringify(model.production);
const delta={private_wtp_bn:model.production.private_wtp_bn.map(()=>0),
  induced_receipts_bn:model.production.induced_receipts_bn.map(()=>0)};
delta.private_wtp_bn[0]=0.125;delta.induced_receipts_bn[0]=-0.03125;
const got=C.applyPart(model,{edits:[],receipt_lines:[],production:delta});
assert.equal(JSON.stringify(model.production),before,"input production remains read-only");
assert.notEqual(got,model);
for(const key of Object.keys(delta)) {
  assert.equal(got.production[key].length,model.production[key].length);
  for(let i=0;i<delta[key].length;i++)assert.ok(Math.abs(got.production[key][i]-model.production[key][i]-delta[key][i])<1e-12,
    `${key}/${i}: additive change over own model base`);
}
assert.deepEqual(got.production.dims,model.production.dims);
assert.deepEqual(got.production.sampling_se_bn,model.production.sampling_se_bn);
const provenanceModel=JSON.parse(JSON.stringify(model));
provenanceModel.corrections={responses:{line_overrides:{}},retained_stack:Array.from({length:161},(_,i)=>({replicate:i,value:i/17}))};
const sourceBefore=JSON.stringify(provenanceModel),first=provenanceModel.spending.lines[0],key=Object.keys(first.keys)[0];
const step=[{side:"spending",line:first.id,key,by:{personal:.001,shared:-.001}}];
const expectedStep=C.X.Engine.applyCorrections(provenanceModel,{lines:[],receipt_lines:[],edits:step,meta:provenanceModel.corrections});
const fastStep=C.withStep(provenanceModel,step,[]);
assert.deepEqual(fastStep,expectedStep,"metadata-efficient wrapper preserves every engine model field");
assert.equal(JSON.stringify(provenanceModel),sourceBefore,"metadata-efficient wrapper preserves its full input");
assert.equal(C.withStep(provenanceModel,[],[]),provenanceModel);
const units=[0,...Array.from({length:160},(_,i)=>i%2?-1:1)];
const source={total_bn:8,se_bn:2,replicates_bn:units.map(x=>8+x),source_total_bn:20,
  source_replicates_bn:units.map(x=>20+2.5*x),source_se_bn:5,
  by_generation_replicates_bn:{G1:units.map(x=>8+x),G2:units.map(x=>5+0.5*x),G3plus:units.map(x=>7+x)}};
const sdr=xs=>Math.sqrt(4/160*xs.slice(1).reduce((t,x)=>t+(x-xs[0])**2,0));
const copies=[0.2,0.8].map(share=>C.scopePost(source,share));
assert.equal(copies.reduce((t,z)=>t+z.total_bn,0),source.total_bn);
for(let i=0;i<source.replicates_bn.length;i++)assert.ok(Math.abs(copies.reduce((t,z)=>t+z.replicates_bn[i],0)-source.replicates_bn[i])<1e-12);
for(let i=0;i<copies.length;i++) {
  assert.equal(copies[i].se_bn,source.se_bn*[0.2,0.8][i]);
  assert.ok(Math.abs(copies[i].se_bn-sdr(copies[i].replicates_bn))<1e-12);
  assert.deepEqual(copies[i].by_generation_replicates_bn,source.by_generation_replicates_bn);
  assert.deepEqual(copies[i].source_replicates_bn,source.source_replicates_bn);
  assert.equal(copies[i].source_se_bn,source.source_se_bn);
  assert.match(copies[i].uncertainty_condition,/fixed.*share/);
}
assert.equal(C.scopePost(source,-0.2).se_bn,0.4);
assert.equal(source.total_bn,8);assert.equal(source.se_bn,2);
assert.throws(()=>C.scopePost({...source,se_bn:NaN},0.2),/invalid source post SE/);
// Source weights and actual fine parent owners, including half parents, replace
// generic t1 even when a reporter has zero value on a particular raw driver.
const gens=["G1_Y_u50","G1_Y_65p","G2","G3plus"],top={G1_Y_u50:"G1",G1_Y_65p:"G1",G2:"G2",G3plus:"G3plus"};
const reporters=[{PH_SEQ:1,PPPOS:1,replicate_weights:Array(161).fill(2)},{PH_SEQ:2,PPPOS:1,replicate_weights:Array(161).fill(3)}];
const fine=[{PH_SEQ:1,PPPOS:1,omega_b:{G1_Y_u50:.5,G1_Y_65p:0,G2:.5,G3plus:0}},
 {PH_SEQ:2,PPPOS:1,omega_b:{G1_Y_u50:0,G1_Y_65p:1,G2:0,G3plus:0}}];
const allocation={components:[{driver_id:"income",raw_share:.75},{driver_id:"cash",raw_share:.25}],
 generation_shares:{G1:Array(161).fill(.775),G2:Array(161).fill(.225),G3plus:Array(161).fill(0)}};
const route={by:{personal:8,shared:4},allocations:{personal:allocation,shared:allocation}};
const drivers={income:{values:[6,0]},cash:{values:[4,4]}};
// income belongs wholly to first row: G1/G2 halves; cash weighted 40/60.
allocation.generation_shares.G1.fill(.575);allocation.generation_shares.G2.fill(.425);
const routed=C.reporterFineAmounts(reporters,drivers,route,fine,gens,top);
assert.ok(Math.abs(routed.G1_Y_u50.personal-3.4)<1e-12);
assert.ok(Math.abs(routed.G1_Y_65p.personal-1.2)<1e-12);
assert.ok(Math.abs(routed.G2.personal-3.4)<1e-12);
assert.equal(routed.G3plus.personal,0);
assert.throws(()=>C.reporterFineAmounts(reporters,{...drivers,income:{values:[0,0]}},route,fine,gens,top),/zero source driver/);
const temporary=fs.mkdtempSync(path.join(require("os").tmpdir(),"late-source-guard-"));
try {
 const file=path.join(temporary,"source.json"),bytes="{\"actual\":true}\n";
 fs.writeFileSync(file,bytes);
 const pins={"source.json":require("crypto").createHash("sha256").update(bytes).digest("hex")};
 assert.ok(Buffer.isBuffer(C.readPinned("source.json",pins,temporary)));
 assert.equal(C.readPinned("source.json",pins,temporary).toString("utf8"),bytes);
 assert.throws(()=>C.readPinned("source.json",{},temporary),/undeclared/);
 fs.writeFileSync(file,"changed bytes");
 assert.throws(()=>C.readPinned("source.json",pins,temporary),/changed admitted reporter source/);
}finally{fs.rmSync(temporary,{recursive:true,force:true});}
console.log("v8 cell production-base regression passed");
