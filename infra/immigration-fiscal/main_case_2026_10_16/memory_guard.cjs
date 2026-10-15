/* Node uses the same physical-footprint definition and limit as Python lanes. */
"use strict";
const path=require("path"),{spawnSync}=require("child_process");
function requireWithinBudget(label="Node process"){
 const rss=process.resourceUsage().maxRSS;
 const child=spawnSync("uv",["run","--no-project","python3",path.join(__dirname,"memory_for_pid.py"),String(process.pid),String(rss)],{encoding:"utf8",maxBuffer:1<<20,env:{...process.env,PYTHONDONTWRITEBYTECODE:"1"}});
 if(child.status!==0)throw Error(`[BLOCKED] ${label}: principal memory probe failed: ${child.stderr||child.error||child.signal||child.status}`);
 let result;try{result=JSON.parse(child.stdout);}catch(e){throw Error(`[BLOCKED] ${label}: invalid principal memory measurement: ${e}`);}
 if(!Number.isFinite(result.peak_bytes)||result.peak_bytes<=0||!Number.isFinite(result.limit_bytes)||typeof result.pass!=="boolean"||result.pass!==(result.peak_bytes<=result.limit_bytes))throw Error(`[BLOCKED] ${label}: inconsistent principal memory measurement`);
 console.log(`[resources] ${label}: ${result.metric}=${result.peak_bytes} bytes; process.resourceUsage().maxRSS=${rss} KiB (diagnostic)`);
 if(!result.pass)throw Error(`[BLOCKED] ${label}: peak ${result.metric} ${(result.peak_bytes/1e9).toFixed(3)} GB exceeds ${(result.limit_bytes/1e9).toFixed(1)} GB budget`);
 return result;
}
module.exports={requireWithinBudget};
