/* Oct16 native band/resource contract; historical keyed rows are read, never rebuilt. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const F=path.dirname(__dirname),hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
function build(out){
 const lane=path.join(F,"debt_legacy_2026_09_23"),debt=path.join(lane,"derived/oct16"),
  receipt=JSON.parse(fs.readFileSync(path.join(debt,"native_frame_manifest.json"))),
  artifact=receipt.artifact;
 if(artifact.path!=="_cache/oct16/native_frame.json")throw Error("[BLOCKED] unexpected native frame cache path");
 const cache=path.join(lane,artifact.path);
 if(!fs.existsSync(cache)||fs.statSync(cache).size!==artifact.bytes||hash(cache)!==artifact.sha256)throw Error("[BLOCKED] native frame cache missing/stale; rebuild debt oct16");
 const frame=JSON.parse(fs.readFileSync(cache)),
  flow=JSON.parse(fs.readFileSync(path.join(debt,"current_flow_contract.json")));
 for(const [p,h]of Object.entries(frame.pins))if(hash(path.join(F,p))!==h)throw Error("[BLOCKED] stale oct16 debt frame "+p);
 if(frame.summary.v9.status!=="adopted")throw Error("[BLOCKED] oct16 not adopted");
 if(JSON.parse(fs.readFileSync(path.join(F,"live_case.json"))).key!=="oct16"||frame.package_status!=="adopted")throw Error("[BLOCKED] live case/package adoption mismatch");
 const population=frame.sets.set.payload.meta.population_v9,rate=frame.sets.set.payload.meta.one_rate.flat_real_equivalent;
 if(!Number.isFinite(rate)||!["set","cash"].every(b=>frame.sets[b].capital_rates.length===1&&frame.sets[b].capital_rates[0]===rate))throw Error("[BLOCKED] expected one capital rate");
 const meta={case:"oct16",package:"main_case_2026_10_16/package.cjs",population_v9:population,
  target_population:population.with_coverage,capital_return:{rates:{low:rate,high:rate},rule:"one Trustees flat-equivalent rate"},
  items:frame.sets.set.payload.meta.v9,
  post_engine:frame.sets.set.payload.meta,union_completion:frame.sets.set.payload.meta.union_completion,
  selected_items:frame.sets.set.payload.meta.v9.selected_items,
  sources_sha256:{...frame.pins,"debt_legacy_2026_09_23/derived/oct16/native_frame_manifest.json":hash(path.join(debt,"native_frame_manifest.json")),"debt_legacy_2026_09_23/derived/oct16/current_flow_contract.json":hash(path.join(debt,"current_flow_contract.json"))},
  social_transport:"source-key quantities; own native calibration and conditional tenure; capital rate actual Trustees equivalent"};
 const funding={};
 for(const [j,end]of ["low","high"].entries()){
  const cash=frame.sets.cash.endpoints[end].r,set=frame.sets.set.endpoints[end].r;
  const total=kind=>flow.financing_totals_bn[`cash|${end}|central|${kind}`]||0;
  const capital=total("resource_cost"),privateP=-total("private_production"),H=cash.cost_bn-capital+privateP;
  const family=Object.fromEntries(cash.evaluation.spending.map(x=>[x.id,x.family]));
  const carriers=frame.sets.cash.payload.meta.union_completion.carriers;
  const sourceFamily=id=>family[id]||(carriers[id]?family[carriers[id].parent_line]:null);
  let removed=-cash.evaluation.spending.filter(x=>x.family==="consumption"||
   (carriers[x.id]?.side==="spending"&&sourceFamily(x.id)==="consumption")).reduce((s,x)=>s+x.effect_bn,0);
  const pl=frame.sets.cash.payload.meta;
  const coverage=pl.coverage.by_end[end].decomposition.line_parts;
  removed+=coverage.filter(x=>x.source_side==="spending"&&family[x.source_line]==="consumption").reduce((s,x)=>s+x.coverage_bn,0);
  for(const [item,parts]of Object.entries(cash.v9_post_engine.parts))if(item!=="one_rate")
   removed+=parts.filter(x=>x.kind!=="college_capital"&&family[x.source_line]==="consumption").reduce((s,x)=>s+x.delta_bn,0);
  // Count/tenure monetary parts are exported separately by the debt consumer.
  // The Python social route adds their source consumption changes once.
  funding[end]={accounting_basis:"national_accounts",current_H_bn:H,capital_return_bn:capital,
   net_accrual_timing_bridge_bn:set.cost_bn-cash.cost_bn,private_wtp_bn:privateP,
   cash_cost_bn:cash.cost_bn,set_cost_bn:set.cost_bn,justice_key:"case",
   government_consumption_removed_bn:removed,
   government_consumption_national_bn:cash.evaluation.spending.filter(x=>x.family==="consumption").reduce((s,x)=>s+x.national_bn,0),
   government_consumption_parts_bn:{engine_and_completion_and_coverage_and_spending_rules:removed},
   timing_rule:"conditional current resources include explicitly unlocated cash and displaced aid; no observed borrowing claim",
   displaced_aid_bn:total("displaced_beneficiaries"),coverage_unclassified_bn:0};
  for(const basis of ["set","cash"])if(Math.abs(frame.sets[basis].endpoints[end].cost_bn-flow.bands_bn[basis][j])>1e-9)throw Error("[BLOCKED] native/flow band mismatch");
 }
 meta.social_resource_account={ends:funding,raw_coded_low_end:null,closure_tolerance_bn:1e-9};
 meta.raw_coded_low_scope="not recomputed for oct16; historical matched-justice diagnostic omitted";
 fs.mkdirSync(out,{recursive:true});
 fs.writeFileSync(path.join(out,"band_variants.json"),JSON.stringify(meta,null,1)+"\n");
 fs.writeFileSync(path.join(out,"band_variants.csv"),"case,variant,cost_low_bn,cost_high_bn\n"+
  ["set","cash"].map(b=>[b==="set"?"oct16":"oct16_cash_set","adopted",...flow.bands_bn[b]].join(",")).join("\n")+"\n");
 console.log("PASS oct16 native/flow set/cash bands; resource split is a definition",flow.bands_bn);
}
if(require.main===module)build(process.argv[2]||path.join(__dirname,"derived/oct16"));
module.exports={build};
