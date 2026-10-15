/* Explicit pre-review snapshot. Rebuild only after final generation outputs exist.
 * Module-only unless invoked directly; every read rejects unknown or changed bytes. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {execFileSync}=require("child_process");
const HERE=__dirname,ROOT=path.resolve(HERE,"../../.."),FILE=path.join(HERE,"inputs/oct15_source_hashes.json");
const sha=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
function committed(rel,commit) {
  const body=execFileSync("git",["-C",ROOT,"show",`${commit}:${rel}`],{maxBuffer:256*1024*1024});
  if(!fs.existsSync(path.join(ROOT,rel))||!fs.readFileSync(path.join(ROOT,rel)).equals(body))
    throw Error(`[BLOCKED] pin does not match file: ${commit}:${rel}`);
}
function verifyPins(record) {
  const pins=JSON.parse(fs.readFileSync(path.join(HERE,"pins.json"),"utf8")).oct15;
  for(const [rel] of Object.entries(record.sha256)) {
    if(rel.startsWith("infra/immigration-fiscal/world_ledger_2026_09_27/"))continue;
    const commit=rel.startsWith("infra/immigration-fiscal/main_case_2026_10_15/")?pins.main_case:pins.generation;
    // The admitted raw graph includes ignored files: their authoritative hashes
    // are checked by the generation input manifest below, not invented git blobs.
    const tracked=execFileSync("git",["-C",ROOT,"ls-files","--",rel]).toString().trim();
    if(tracked)committed(rel,commit);
  }
  return pins;
}
function read(rel) {
  if(!fs.existsSync(FILE))throw Error("[BLOCKED] missing explicit oct15 SHA256 snapshot; capture only after final case/generation readiness");
  const record=JSON.parse(fs.readFileSync(FILE,"utf8"));
  if(record.case!=="oct15"||record.provenance!=="[WORKTREE INPUT]")throw Error("[BLOCKED] invalid oct15 snapshot");
  const f=path.join(ROOT,rel),want=record.sha256[rel];
  if(!want||!fs.existsSync(f)||sha(f)!==want)throw Error(`[BLOCKED] missing, unknown or changed oct15 snapshot input ${rel}`);
  return fs.readFileSync(f,"utf8");
}
function verify() {
  if(!fs.existsSync(FILE))throw Error("[BLOCKED] missing explicit oct15 SHA256 snapshot; capture only after final case/generation readiness");
  const record=JSON.parse(fs.readFileSync(FILE,"utf8"));
  for(const rel of Object.keys(record.sha256))read(rel);
  verifyPins(record);
  return record;
}
function generationOutputs(directory,caseKey) {
  const names=[`generation_corrections_${caseKey}.json`,`generation_corrections_${caseKey}_cash.json`,
    `generation_results_${caseKey}.csv`,`generation_results_${caseKey}_cash.csv`,
    `generation_summary_${caseKey}.json`,`generation_summary_${caseKey}_cash.json`,
    ...['G1','G2','G3plus'].flatMap(g=>[`model_${g}.json`,`model_b_${g}.json`])];
  return names.map(name=>{
    const file=path.join(directory,name);
    if(!fs.existsSync(file))throw Error(`[BLOCKED] missing selected generation input ${file}`);
    return file;
  });
}
function capture() {
  const P=require("../main_case_2026_10_15/package.cjs");
  require("../generation_account_2026_09_24/v8_split.cjs");
  const files=Object.keys(require.cache).filter(f=>f.startsWith(ROOT+path.sep));
  const GEN=path.join(ROOT,"infra/immigration-fiscal/generation_account_2026_09_24");
  files.push(...generationOutputs(path.join(GEN,"derived"),"oct15"));
  for(const name of ["routing.json","pins.json"])files.push(path.join(GEN,"inputs",name));
  const admitted=JSON.parse(fs.readFileSync(path.join(GEN,"inputs/pins.json"),"utf8"));
  for(const [rel,want] of Object.entries(admitted)) {
    const file=path.join(ROOT,"infra/immigration-fiscal",rel);
    if(typeof want!=="string"||sha(file)!==want)throw Error(`[BLOCKED] generation admitted source changed ${rel}`);
    files.push(file);
  }
  const C=path.join(ROOT,"infra/immigration-fiscal/main_case_2026_10_15");
  for(const name of fs.readdirSync(path.join(C,"derived")))files.push(path.join(C,"derived",name));
  for(const [which,api] of [["set",P],["cash",P.CASH]]){
    const payload=api.correctionsPayload(),meta=payload.meta;
    if(!meta.coverage||meta.coverage.stub)throw Error("[BLOCKED] cannot snapshot absent or stub coverage");
    const saved=JSON.parse(fs.readFileSync(path.join(C,"derived",`corrections${which==="cash"?"_cash":""}.json`),"utf8"));
    if(JSON.stringify(payload)!==JSON.stringify(saved))throw Error(`[BLOCKED] ${which} saved case payload differs from current API`);
    if(meta.coverage?.file)files.push(path.join(ROOT,"infra/immigration-fiscal",meta.coverage.file));
  }
  const sha256=Object.fromEntries([...new Set(files)].sort().map(f=>[path.relative(ROOT,f),sha(f)]));
  const record={case:"oct15",provenance:"[WORKTREE INPUT]",sha256};
  const pins=verifyPins(record);
  record.authority="[COMMITTED INPUT]";
  record.commits={main_case:pins.main_case,generation:pins.generation};
  fs.writeFileSync(FILE,JSON.stringify(record,null,1)+"\n");
  console.log(`[WORKTREE INPUT] oct15 snapshot: ${Object.keys(sha256).length} exact input hashes`);
}
if(require.main===module){if(process.argv[2]!=="--capture")throw Error("[BLOCKED] explicit --capture required");capture();}
module.exports={read,verify,generationOutputs};
