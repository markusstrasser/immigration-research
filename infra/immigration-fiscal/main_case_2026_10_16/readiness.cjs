/* Captured source custody is mandatory; no worker-session fallback. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
function requireItem13({here=__dirname}={}){
 const fail=s=>{throw Error("[BLOCKED] v9 item13: "+s);};
 const file=path.join(here,"inputs/item13_ready.json");
 if(!fs.existsSync(file))fail("captured readiness receipt absent");
 const ready=JSON.parse(fs.readFileSync(file,"utf8"));
 const source="spending_keys_r5_2026_10_15/derived/item13.json";
 if(ready.completion_marker!=="L1 STEP 3 DONE"||ready.item13_source!==source)fail("captured readiness receipt incomplete");
 const input=path.join(here,"..",source);
 if(!fs.existsSync(input))fail("captured readiness source absent");
 const hash=crypto.createHash("sha256").update(fs.readFileSync(input)).digest("hex");
 if(ready.item13_sha256!==hash)fail("captured readiness is stale; source custody changed");
 return ready;
}
module.exports={requireItem13};
