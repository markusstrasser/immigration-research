/* Reproduce the unchanged generation producer; record every file read. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const HERE=__dirname,ROOT=path.dirname(HERE),GEN=path.join(ROOT,"generation_account_2026_09_24");
const digest=b=>crypto.createHash("sha256").update(b).digest("hex");
const read=fs.readFileSync.bind(fs),write=fs.writeFileSync.bind(fs);
const arg=process.argv.indexOf("--child");
if(arg>=0){
  const key=process.argv[arg+1],out=process.argv[arg+2],inputs={};
  for(const name of ["live_case.json","main_case_2026_10_16/derived/summary.json",
      "main_case_2026_10_16/derived/corrections.json","main_case_2026_10_16/derived/corrections_cash.json"])
    inputs[name]=digest(read(path.join(ROOT,name)));
  fs.readFileSync=function(file,...args){
    const result=read(file,...args);
    if(typeof file==="string"&&path.isAbsolute(file)&&file.startsWith(ROOT+path.sep)){
      const name=path.relative(ROOT,file),sha=digest(read(file));
      if(inputs[name]&&inputs[name]!==sha)throw Error("[BLOCKED] generation input moved during run "+name);
      inputs[name]=sha;
    }
    return result;
  };
  process.argv=[process.argv[0],path.join(GEN,"run_generations_v9.cjs"),"--case",key,"--out-dir",out];
  require(path.join(GEN,"run_generations_v9.cjs"));
  for(const file of Object.keys(require.cache))if(file.startsWith(ROOT+path.sep))
    inputs[path.relative(ROOT,file)]=digest(read(file));
  write(path.join(out,`reads_${key}.json`),JSON.stringify(inputs,null,2)+"\n");
}else{
  const out=path.join(HERE,"_cache","generation_source_replay_oct16");
  fs.mkdirSync(out,{recursive:true});
  const inputs={},outputs={};
  for(const key of ["oct16","oct16_cash"]){
    const result=cp.spawnSync(process.execPath,[__filename,"--child",key,out],{stdio:"inherit",env:process.env});
    if(result.status!==0)throw Error("[BLOCKED] unchanged generation source replay failed "+key);
    const recorded=JSON.parse(read(path.join(out,`reads_${key}.json`),"utf8"));
    for(const [name,sha]of Object.entries(recorded)){
      if(inputs[name]&&inputs[name]!==sha)throw Error("[BLOCKED] generation input moved between sets "+name);
      inputs[name]=sha;
    }
    for(const kind of ["results","summary","corrections"]){
      const name=`generation_${kind}_${key}.${kind==="results"?"csv":"json"}`;
      const actual=read(path.join(GEN,"derived",name)),rebuilt=read(path.join(out,name));
      if(!actual.equals(rebuilt))throw Error("[BLOCKED] generation source replay differs "+name);
      outputs[path.relative(ROOT,path.join(GEN,"derived",name))]=digest(actual);
    }
  }
  for(const [name,sha]of Object.entries(inputs))if(digest(read(path.join(ROOT,name)))!==sha)
    throw Error("[BLOCKED] generation replay input is no longer current "+name);
  const contract={case:"oct16",producer:"generation_account_2026_09_24/run_generations_v9.cjs",
    rule:"unchanged producer byte-reproduces all six current generation files; nested adopted is inherited oct15 history",
    inputs,outputs};
  write(path.join(HERE,"derived","generation_source_contract_oct16.json"),JSON.stringify(contract,null,2)+"\n");
  console.log(`[PASS] unchanged generation source IDENTICAL 6/6; ${Object.keys(inputs).length} file-read pins`);
}
