/* The live declaration and the consumed package jointly authorize adoption. */
"use strict";
const fs=require("fs"),path=require("path");
const cp=require("child_process");
function requireAdopted(key,{livePath=path.join(__dirname,"../live_case.json"),packageApi}={}){
 const fail=s=>{throw Error("[BLOCKED] adoption: "+s);};
 if(!fs.existsSync(livePath))fail("live declaration missing");
 const live=JSON.parse(fs.readFileSync(livePath,"utf8"));
 if(live.key!==key)fail(`live key ${live.key} does not match consumed case ${key}`);
 if(!live.lane||!live.adopted||!live.decision)fail("live declaration incomplete");
 const packagePath=path.resolve(path.dirname(livePath),live.lane,"package.cjs");
 const loaded=packageApi||JSON.parse(cp.execFileSync(process.execPath,["-e",
  'const api=require(process.argv[1]);process.stdout.write(JSON.stringify(api.V9||api));',packagePath],
  {env:{...process.env,FISCAL_ADOPTION_ONLY:"1"},encoding:"utf8"}));
 const api=loaded.V9||loaded;
 if(api.STATUS!=="adopted")fail("consumed package STATUS is not adopted");
 if(api.CASE_KEY!==key||api.LANE!==live.lane)fail("consumed package case/lane identity differs from live declaration");
 if(api.ADOPTED!==live.adopted||api.DECISION!==live.decision)fail("package adoption metadata differs from live declaration");
 return {key,adopted:live.adopted,decision:live.decision};
}
module.exports={requireAdopted};
if(require.main===module)process.stdout.write(JSON.stringify(requireAdopted(process.argv[2],
 process.argv[3]?{livePath:process.argv[3]}:{}))+"\n");
