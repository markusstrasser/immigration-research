/* Capture source completion custody; validate subsequently consumed bytes. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const HERE=__dirname,F=path.join(HERE,".."),sha=b=>crypto.createHash("sha256").update(b).digest("hex");
const read=p=>fs.readFileSync(path.join(F,p));
const readyFile=path.join(HERE,"inputs/item13_ready.json");
const source="spending_keys_r5_2026_10_15/derived/item13.json";
const ready={completion_marker:"L1 STEP 3 DONE",item13_source:source,item13_sha256:sha(read(source)),scope:"final source bridge accepted for candidate build; adoption remains null"};
require("./readiness.cjs").requireItem13();
if(JSON.stringify(JSON.parse(fs.readFileSync(readyFile,"utf8")))!==JSON.stringify(ready))throw Error("[BLOCKED] final item13 source changed after captured readiness");
const healthFiles=["health_item.cjs","derived/item21.json","derived/item21_coverage.json","derived/item21_v9_coverage.json","derived/item21_v9_count_parts.csv","derived/item21_case_changes.json"].map(p=>"spending_keys_r5_2026_10_15/"+p);
const healthReadyFile=path.join(HERE,"inputs/item21_ready.json"),healthReady={completion_marker:"ITEM21_READY",hashes:Object.fromEntries(healthFiles.map(p=>[p,sha(read(p))]))};
if(!fs.existsSync(healthReadyFile))throw Error("[BLOCKED] item21 captured readiness receipt absent");
if(JSON.stringify(JSON.parse(fs.readFileSync(healthReadyFile,"utf8")))!==JSON.stringify(healthReady))throw Error("[BLOCKED] item21 source changed after captured readiness");
const files=[
 "main_case_2026_10_15/package.cjs","main_case_2026_10_15/derived/summary.json","main_case_2026_10_15/derived/corrections.json","main_case_2026_10_15/derived/corrections_cash.json",
 "spending_keys_r5_2026_10_15/items.cjs","spending_keys_r5_2026_10_15/item13_generations.cjs",source,"spending_keys_r5_2026_10_15/derived/item14.json","spending_keys_r5_2026_10_15/derived/item15.json","spending_keys_r5_2026_10_15/derived/case_changes.json",
 "count_composition_r5_2026_10_15/items.cjs","count_composition_r5_2026_10_15/derived/items.json","count_composition_r5_2026_10_15/derived/line_parts_set.csv","count_composition_r5_2026_10_15/derived/line_parts_cash.csv",
 "consumption_tax_bases_r5_2026_10_15/item.cjs","consumption_tax_bases_r5_2026_10_15/evaluate.cjs","consumption_tax_bases_r5_2026_10_15/derived/item.json","consumption_tax_bases_r5_2026_10_15/derived/evaluation.json",
 "passthrough_source_tax_r5_2026_10_15/item.cjs","passthrough_source_tax_r5_2026_10_15/derived/item.json","passthrough_source_tax_r5_2026_10_15/derived/job_keys.json","passthrough_source_tax_r5_2026_10_15/derived/v8.json","passthrough_source_tax_r5_2026_10_15/derived/w09.json",
 "one_rate_2026_10_15/evaluate.cjs","one_rate_2026_10_15/derived/rates.json","one_rate_2026_10_15/derived/results.json","coverage_bound_2026_10_14/derived/coverage_bound_oct15.json",
].concat(healthFiles);
const hashes=Object.fromEntries(files.map(p=>[p,sha(read(p))]));
const report={pass:true,readiness:ready,hashes,source18_contract:{modelFor_corrections_index_absent:true,evaluator:"consumption_tax_bases_r5_2026_10_15/evaluate.cjs:8",default:"source_evaluator",alternative:"declared_carriers"},source19_contract:{default_numeric_intent:"foreign_full_ftc_individual_tangible_normal",literal_brief_name:"foreign_full_ftc_immediate_individual"}};
fs.mkdirSync(path.join(HERE,"derived"),{recursive:true});fs.writeFileSync(path.join(HERE,"derived/source_checks.json"),JSON.stringify(report,null,1)+"\n");
console.log(`PASS source custody ${files.length} files; final13 captured; maxRSS ${process.resourceUsage().maxRSS} KiB`);
require("./memory_guard.cjs").requireWithinBudget("source custody");
