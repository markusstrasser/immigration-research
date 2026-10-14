/* Execute live routing variants in one process. Only the runner module is
 * reloaded: immutable case/source caches stay shared, avoiding repeated native
 * unit-band compilation. Each run retains every gate and output boundary.
 * Native-First: Node require cache and an explicit JSON argv list. */
"use strict";
const fs=require("fs");
const plan=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
if(!Array.isArray(plan)||!plan.length)throw Error("[BLOCKED] empty routing plan");
const runner=require.resolve("./run_generations_v8.cjs");
for(const args of plan) {
 if(!Array.isArray(args)||!args.every(a=>typeof a==="string"))throw Error("[BLOCKED] routing plan args");
 process.argv=[process.execPath,runner,...args];
 delete require.cache[runner];
 require(runner);
}
