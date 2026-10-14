/* Explicit pre-review snapshot. Rebuild only after final generation outputs exist.
 * Module-only unless invoked directly; every read rejects unknown or changed bytes. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const HERE=__dirname,ROOT=path.resolve(HERE,"../../.."),FILE=path.join(HERE,"inputs/oct15_source_hashes.json");
const sha=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
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
  return record;
}
function capture() {
  const P=require("../main_case_2026_10_15/package.cjs");
  require("../generation_account_2026_09_24/v8_split.cjs");
  const G="infra/immigration-fiscal/generation_account_2026_09_24/derived/";
  const files=Object.keys(require.cache).filter(f=>f.startsWith(ROOT+path.sep));
  const GEN=path.join(ROOT,"infra/immigration-fiscal/generation_account_2026_09_24");
  for(const name of fs.readdirSync(path.join(GEN,"derived")))if(/\.(json|csv)$/.test(name))files.push(path.join(GEN,"derived",name));
  for(const name of ["routing.json","pins.json"])files.push(path.join(GEN,"inputs",name));
  for(const name of ["generation_corrections_oct15.json","generation_corrections_oct15_cash.json",
    "generation_results_oct15.csv","generation_results_oct15_cash.csv","generation_summary_oct15.json",
    "generation_summary_oct15_cash.json",...['G1','G2','G3plus'].flatMap(g=>[`model_${g}.json`,`model_b_${g}.json`])])files.push(path.join(ROOT,G,name));
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
  fs.writeFileSync(FILE,JSON.stringify({case:"oct15",provenance:"[WORKTREE INPUT]",sha256},null,1)+"\n");
  console.log(`[WORKTREE INPUT] oct15 snapshot: ${Object.keys(sha256).length} exact input hashes`);
}
if(require.main===module){if(process.argv[2]!=="--capture")throw Error("[BLOCKED] explicit --capture required");capture();}
module.exports={read,verify};
