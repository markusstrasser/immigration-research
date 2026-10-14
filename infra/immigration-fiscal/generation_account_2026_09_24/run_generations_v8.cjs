/* Live oct15 generation split; set and cash. Uses the frozen September 29
 * generation inputs and v8_split.cjs. Every model cell, production cell, cost
 * and capital component must add to the case (1e-9; grid 1e-12). Nothing is
 * written on failure. Historical case files are inputs and remain unchanged.
 * node .../run_generations_v8.cjs [--case oct15|oct15_cash] [--out-dir DIR] */
"use strict";
const fs = require("fs"), path = require("path");
const { publish } = require("./atomic_file_v8.cjs");
const V7 = require("./v8_split.cjs");
const { X, P7 } = V7;
const { Engine, MODEL, ALLOCS, byAlloc, sum } = X;
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i < 0 ? d : argv[i + 1]; };
const CASE = arg("--case", "oct15");
const set = { oct15: "set", oct15_cash: "cash" }[CASE];
if (!set) throw new Error("[BLOCKED] --case must be oct15 or oct15_cash");
const IN = path.join(__dirname, "derived"), OUT = path.resolve(arg("--out-dir", IN));
const fixesArg=arg("--fixes",V7.FIXES.join(","));
const fixes=fixesArg==="none"?[]:fixesArg.split(",");
const parentFile=path.join(__dirname,"inputs/minor_parent_measurement_oct15.json");
const parentMeasurement=fs.existsSync(parentFile)?JSON.parse(fs.readFileSync(parentFile,"utf8")):null;
const centralMinorScale=parentMeasurement?.central_share ?? 1;
const minorScale=Number(arg("--minor-scale",String(centralMinorScale)));
const productionRule=arg("--production-rule","aumann_shapley");
if(!["aumann_shapley","labour_income"].includes(productionRule)) throw new Error("[BLOCKED] unknown production rule");
const centralPolicy=JSON.stringify([...fixes].sort())===JSON.stringify([...V7.FIXES].sort())
  && minorScale===centralMinorScale && productionRule==="aumann_shapley";
if(!centralPolicy && (argv.indexOf("--out-dir")<0 || OUT===IN))
  throw new Error("[BLOCKED] non-central routing requires --out-dir outside canonical derived outputs");
const policy={fixes,minor_scale:minorScale,production_rule:productionRule,central:centralPolicy,
  parent_measurement:parentMeasurement?"inputs/minor_parent_measurement_oct15.json":"phase1_wholly_G2_base"};
const load = (name) => JSON.parse(fs.readFileSync(path.join(IN, name), "utf8"));
const GENS = ["G1", "G2", "G3plus"], CONVS = ["a", "b"], TOP = Object.fromEntries(GENS.map((g) => [g, g]));
const L = V7.loadCase(set), suffix = set === "set" ? "" : "_cash";
if(L.payload.meta.adopted && !parentMeasurement) throw new Error("[BLOCKED] final generation requires measured minor-parent routing");
const G29 = load(`generation_corrections_sept29${suffix}.json`);
const fails = [], checks = [];
function gate(label, ok, detail) {
  checks.push({ check: label, pass: ok, detail });
  console.log(`${ok ? "✓" : "✗"} ${label}${detail === undefined ? "" : `: ${detail}`}`);
  if (!ok) fails.push(label);
}
const cells = (m) => new Map(m.receipts.lines.flatMap((l) => Object.entries(l.cells).map(([k, c]) => [`receipt:${l.id}:${k}`, c]))
  .concat(m.spending.lines.flatMap((l) => Object.entries(l.keys).map(([k, c]) => [`spending:${l.id}:${k}`, c]))));
function addsTo(u, ms) {
  const uc = cells(u), cs = ms.map(cells);
  let gap = cs.some((c) => c.size !== uc.size) ? Infinity : 0;
  let grid = ms.some((m) => JSON.stringify(m.production.dims) !== JSON.stringify(u.production.dims)
    || ["private_wtp_bn", "induced_receipts_bn"].some((k) => m.production[k].length !== u.production[k].length)) ? Infinity : 0;
  for (const [k, c] of uc) for (const a of ALLOCS) gap = Math.max(gap, Math.abs(sum(cs.map((p) => p.get(k)?.[a].target_bn ?? NaN)) - c[a].target_bn));
  for (const k of ["private_wtp_bn", "induced_receipts_bn"]) u.production[k].forEach((v, i) => {
    grid = Math.max(grid, Math.abs(sum(ms.map((m) => m.production[k][i])) - v));
  });
  return { gap, grid };
}
gate("September 29 generation payload declares the case's base", G29.meta.union === L.baseRel, G29.meta.union);
const union29 = Engine.applyCorrections(MODEL, L.base), union = Engine.applyCorrections(MODEL, L.payload);
const models0 = {}, models29 = {}, models = {}, layers = {}, payloads = {};
for (const conv of CONVS) {
  models0[conv] = Object.fromEntries(GENS.map((g) => [g, load(`${conv === "a" ? "model_" : "model_b_"}${g}.json`)]));
  models29[conv] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], G29.payloads[conv][g])]));
  const r29 = addsTo(union29, Object.values(models29[conv]));
  gate(`${conv}: base models add cell by cell and on the production grid`, r29.gap < 1e-9 && r29.grid < 1e-12, JSON.stringify(r29));
  const lay = V7.layer(L, GENS, TOP, models29[conv], union29,{convention:conv,fixes,minorScale});
  layers[conv] = lay;
  payloads[conv] = Object.fromEntries(GENS.map((g) => [g, V7.payloadOf(G29.payloads[conv][g], lay.parts[g])]));
  models[conv] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], payloads[conv][g])]));
  if(productionRule==="labour_income") {
    const shares=load("generation_state_indexes.json").labour_income_shares;
    const n=Engine.PRODUCTION_DIMS.slice(1).reduce((v,d)=>v*union.production.dims[d].length,1);
    for(const g of GENS) {
      const prod=payloads[conv][g].production;
      for(const k of ["private_wtp_bn","induced_receipts_bn"]) {
        prod[k]=union29.production[k].map((v,i)=>v*shares[union.production.dims.proxy[Math.floor(i/n)]][conv][g][0]+
          (lay.parts[g].production?.[k][i] || 0));
      }
      models[conv][g]=Engine.applyCorrections(models0[conv][g],payloads[conv][g]);
    }
  }
  const r = addsTo(union, Object.values(models[conv]));
  gate(`${conv}: v8 models add cell by cell and on the production grid`, r.gap < 1e-9 && r.grid < 1e-12, JSON.stringify(r));
  let shares = 0, amount = 0;
  for (const it of lay.items) for (const ed of it.edits) for (const p of ed.parts || []) for (const a of ALLOCS) {
    shares = Math.max(shares, Math.abs(sum(GENS.map((g) => p.share[g][a])) - 1));
    amount = Math.max(amount, Math.abs(sum(GENS.map((g) => p.bn[g][a])) - p.union_bn[a]));
  }
  gate(`${conv}: split shares and amounts close`, shares < 1e-12 && amount < 1e-9, `${shares} / ${amount}`);
}
const ev = V7.evaluator(L.payload, L.api), specs = ev.specs, AP = V7.adoptedPackage(L), O = V7.oracle(set);
const FIELDS = ["allocation", "normalization", "share", "school", "reading", "gg", "uc"];
gate("32 personal specifications agree with the package", specs.length === 32 && AP.specs.length === 32
  && specs.every((s, i) => s.allocation === "personal" && FIELDS.every((k) => JSON.stringify(s[k]) === JSON.stringify(AP.specs[i][k]))));
const full = specs.map((s) => ev.evaluateFull(union, s)), uCost = full.map((r) => r.cost_bn);
const undefinedReporterCarriers=["health_services","military_medical","veterans_other","other_state_benefits"]
  .map(id=>`union_completion_${id}_veterans`);
gate("four zero-mass extrapolated reporter keys have zero effect at every specification",full.every(r=> {
  const rows=r.evaluation.spending.filter(x=>undefinedReporterCarriers.includes(x.id));
  return rows.length===4&&rows.every(x=>x.response===0&&x.effect_bn===0);
}));
gate("consumer response overrides agree with every package specification", full.every((r, i) =>
  Object.entries(AP.specs[i].line_responses).every(([k, v]) =>
    L.payload.meta.union_completion.carriers[k]?.kind === "line" || r.state.response_override[k] === v)));
const uncorrected = specs.map((s) => ev.cost(MODEL, s));
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost)), ends = [lo, hi];
gate("case ends and published band", ends.every((i, k) => i === O.specs[k] && Math.abs(uCost[i] - O.band[k]) < 1e-4), ends.join(" / "));
gate("case full-precision band", ends.every((i, k) => Math.abs(uCost[i] - O.full.band[k]) < 1e-9), ends.map((i) => uCost[i]).join(" / "));
const PS = V7.perSpec(set);
if (PS) gate("every published personal specification", PS.cost.size === 32 && [...PS.cost].every(([i, c]) => Math.abs(uCost[i] - c) < 1e-9));
const res = {};
let packageGap = 0;
for (let i = 0; i < specs.length; i++) packageGap = Math.max(packageGap, Math.abs(AP.cost(union, i) - uCost[i]), Math.abs(AP.cost(MODEL, i) - uncorrected[i]));
for (const conv of CONVS) {
  res[conv] = Object.fromEntries(GENS.map((g) => {
    const all = specs.map((s) => ev.evaluateFull(models[conv][g], s));
    return [g, { full: all, cost: all.map((r) => r.cost_bn), uncorrected: specs.map((s) => ev.cost(models0[conv][g], s)) }];
  }));
  let gap = 0, cap = 0;
  specs.forEach((s, i) => {
    for (const kind of ["cost", "uncorrected"]) gap = Math.max(gap, Math.abs(sum(GENS.map((g) => res[conv][g][kind][i])) - (kind === "cost" ? uCost[i] : uncorrected[i])));
    full[i].capital.components.forEach((c, j) => { cap = Math.max(cap, Math.abs(sum(GENS.map((g) => res[conv][g].full[i].capital.components[j].return_bn)) - c.return_bn)); });
    for (const g of GENS) packageGap = Math.max(packageGap, Math.abs(AP.cost(models[conv][g], i) - res[conv][g].cost[i]), Math.abs(AP.cost(models0[conv][g], i) - res[conv][g].uncorrected[i]));
  });
  gate(`${conv}: generations add at every specification, corrected and uncorrected; every capital component`, gap < 1e-9 && cap < 1e-9, `${gap} / ${cap}`);
}
gate("package and independent consumer agree for all models/specifications", packageGap < 1e-9, packageGap);
if (set === "set") {
  // Retain the inherited P7 source positive control. It writes no historical
  // case output; the new split has its own independent 32-spec closure above.
  const OLD=require("./v7_split.cjs"),oldEv=OLD.evaluator(L.old.payload,L.old.api),oldO=OLD.oracle(set);
  const A = X.readJson(`${OLD.V7_LANE}/derived/api_check.json`);
  const chk = A.patterns.flatMap((p) => p.checks).find((c) => /with the edit sets' edits by the rule/.test(c.check));
  const printed = chk && chk.detail.match(/at specifications (\d+) \/ (\d+): (.*)$/);
  const got = printed ? Object.fromEntries(printed[3].split("; ").map((s) => {
    const [g, a, , b] = s.split(" "); return [g, [Number(a), Number(b)]];
  })) : null;
  const alt = OLD.layer(L.old, GENS, TOP, models29.a, union29, { fixes:[], alt: ["row8_on_g3plus", "pension_receipt_shares"] });
  const altModels = GENS.map((g) => Engine.applyCorrections(models0.a[g], OLD.payloadOf(G29.payloads.a[g], alt.parts[g])));
  const r = addsTo(Engine.applyCorrections(MODEL,L.old.payload), altModels);
  gate("G4 pattern 3 reference: row 8 on G3+, pension union by receipts; split still closes", r.gap < 1e-9 && r.grid < 1e-12
    && chk?.pass === true && got && Number(printed[1]) === oldO.specs[0] && Number(printed[2]) === oldO.specs[1]
    && GENS.every((g, j) => oldO.specs.every((i, k) => Math.abs(oldEv.cost(altModels[j], oldEv.specs[i]) - got[g][k]) < 5e-5)));
}
// The G3-rate pricing-class minor assignment is an explicit approximation.
const H = load("v4_inputs.json").headcount, lin = L.lineage;
const AA = V7.addedAdults(lin, H.a.G3plus.adults / H.a.G3plus.population);
const completion=L.payload.meta.union_completion,coverage=L.payload.meta.coverage;
const reporterCounts=V7.reporterPopulation(L),reporterTotal=sum(Object.values(reporterCounts));
const extraAdults=sum(completion.observed_records.filter(r=>r.age>=18).map(r=>r.people));
const coverageSource=coverage?loadCoverage(coverage):null;
function loadCoverage(c) {
  const crypto=require("crypto"),file=path.join(__dirname,"..",c.file),bytes=fs.readFileSync(file);
  if(crypto.createHash("sha256").update(bytes).digest("hex")!==c.sha256) throw Error("[BLOCKED] coverage source hash changed");
  const src=JSON.parse(bytes),q=src.sets[set].scenarios[c.construction];
  if(!q.adults_by_generation||!GENS.every(g=>Number.isFinite(q.adults_by_generation[g]))) throw Error("[BLOCKED] coverage lacks adult counts for generation denominators");
  return q;
}
const coverageAdults=coverageSource?sum(Object.values(coverageSource.adults_by_generation)):0;
const population=L.payload.meta.population_v8.with_coverage, adults=H.union.adults+AA.adults+extraAdults+coverageAdults;
const sourceRoundingPeople=lin.counts.lineage_population-(H.union.population+lin.counts.added);
gate("frozen row4 count rounding is below one ten-thousandth of a person",Math.abs(sourceRoundingPeople)<1e-4,sourceRoundingPeople);
gate("headcount equals the case lineage plus completion and coverage", Math.abs(population-(H.union.population+lin.counts.added+completion.counts.total+(coverage?.net_missing_people||0)))<1e-3,population);
const per = (bn, n) => bn * 1e9 / n;
const summary = { case: CASE, set, lane: V7.V7_LANE, payload: L.rel, status: L.payload.meta.status, adopted: L.payload.meta.adopted,
  policy,parent_measurement:parentMeasurement,
  post_engine:{coverage:L.payload.meta.coverage||null,mixed_unit_removal:L.payload.meta.mixed_unit_removal},
  builds_on: { payload: L.baseRel, generation_payloads: `generation_account_2026_09_24/derived/generation_corrections_sept29${suffix}.json` },
  oracle: O, responses: L.payload.meta.responses, low_spec: specs[lo], high_spec: specs[hi],
  specifications: { low: specs[lo], high: specs[hi], low_index: lo, high_index: hi },
  union: { cost_bn: ends.map((i) => uCost[i]), uncorrected_bn: ends.map((i) => uncorrected[i]), population, adults,
    per_member_usd: ends.map((i) => per(uCost[i], population)), per_adult_usd: ends.map((i) => per(uCost[i], adults)) },
  added_adults: AA, lineage: lin, population_rounding:{generation:"G1",people:sourceRoundingPeople,rule:"case rounds only the Mexico-born union frame; reconcile its preserved four-decimal count to the full-precision generation weights"}, items: { order: L.items.map((it) => it.id), all: L.records.map((r) => r.id), records: L.records,
    split: Object.fromEntries(CONVS.map((c) => [c, layers[c].items])) }, conventions: {}, gates: { failed: fails, checks } };
const rows = [];
for (const conv of CONVS) {
  summary.conventions[conv] = {};
  for (const g of GENS) {
    const moved=conv==="b" && fixes.includes("minors")?layers[conv].age_routing.minor_count*minorScale:0;
    const extraMoved=conv==="b" && fixes.includes("minors")?parentMeasurement.native_observed_children.g2_equivalents.estimate:0;
    const reporterMove=conv==="b" && fixes.includes("minors")?reporterCounts[g]-(g==="G3plus"?reporterTotal:0):0;
    const extra=completion.counts.by_generation[g]+reporterMove+(g==="G2"?extraMoved:g==="G3plus"?-extraMoved:0);
    const h = { population: H[conv][g].population + (g==="G1"?sourceRoundingPeople:0) + extra +(coverage?.counts_by_generation?.[g]||0) + (g === "G3plus" ? lin.counts.added-moved : g==="G2"?moved:0), adults: H[conv][g].adults + (g === "G3plus" ? AA.adults+extraAdults : 0)+(coverageSource?.adults_by_generation?.[g]||0) };
    const r = res[conv][g], c = ends.map((i) => r.cost[i]);
    summary.conventions[conv][g] = Object.assign({}, h, { cost_bn: c, own_span_bn: [Math.min(...r.cost), Math.max(...r.cost)],
      uncorrected_cost_bn: ends.map((i) => r.uncorrected[i]), correction_bn: ends.map((i) => r.cost[i] - r.uncorrected[i]),
      per_member_usd: c.map((v) => per(v, h.population)), per_adult_usd: c.map((v) => per(v, h.adults)),
      production:ends.map(i=>Object.fromEntries(["private_wtp_bn","induced_receipts_bn","production_gain_bn"].map(k=>[k,r.full[i].evaluation[k]]))) });
    ends.forEach((i, k) => {
      const receipts = r.full[i].evaluation.receipts;
      const receiptCost = (id) => -(receipts.find((x) => x.id === id)?.effect_bn || 0);
      rows.push({ convention: conv, generation: g, band_end: k === 0 ? "low" : "high", allocation: specs[i].allocation, cost_bn: r.cost[i],
        fixes:fixes.join("|"),minor_scale:minorScale,production_rule:productionRule,central_policy:centralPolicy,
        uncorrected_same_spec_bn: r.uncorrected[i], correction_bn: r.cost[i] - r.uncorrected[i], population: h.population, adults: h.adults,
        per_member_usd: per(r.cost[i], h.population), per_adult_usd: per(r.cost[i], h.adults), capital_return_bn: r.full[i].capital.total_bn,
        enterprise_surplus_receipt_bn: receiptCost(X.P.ENTERPRISE_LINE), housing_enterprise_surplus_receipt_bn: receiptCost("housing_enterprise_surplus"),
        mixed_unit_removal_bn:r.full[i].post_engine.mixed_unit_removal_bn,coverage_bn:r.full[i].post_engine.coverage_bn });
    });
  }
}
summary.routing={fixes,minor_scale:minorScale,production_rule:productionRule,contract:"inputs/routing.json",age:layers.b.age_routing,
  observed_reporter_parent_counts_b:reporterCounts,existing_union_parent_vintage:"P7_frozen; completed parent assignment applies to new reporter and native records only",
  reporter_parent_driver_limit:{carriers:undefinedReporterCarriers,zero_mass_policy:"source_anchor",
    rule:"four personal alternative-key amounts are extrapolated by the case and have no observed reporter driver mass; exact source-anchor ownership is an assumption; all four have zero effect in all32 current specifications, set and cash"},
  added_state_prices:Object.fromEntries(CONVS.map(c=>[c,layers[c].added_state_price_routing])),
  state_diagnostics:Object.fromEntries(CONVS.map(c=>[c,layers[c].state_diagnostics])),
  adjustments:Object.fromEntries(CONVS.map(c=>[c,layers[c].routing_adjustments]))};
summary.state_price_conditional_se={};
summary.state_price_replicate_delta_bn={};
summary.reporter_parent_replicate_delta_bn={};
summary.reporter_parent_conditional_se_bn={};
for(const conv of CONVS) {
  const S=layers[conv].state_diagnostics;
  if(!S) continue;
  summary.state_price_conditional_se[conv]={};
  summary.state_price_replicate_delta_bn[conv]={};
  let linearGap=0;
  for(const g of GENS) summary.state_price_conditional_se[conv][g]=ends.map(i=> {
    const m=models[conv][g], s=specs[i], base=res[conv][g].cost[i];
    const net=Array(161).fill(0), one=[];
    for(const r of S.replicate_adjustments) {
      const shifted=V7.withStep(m,[Object.assign({},r.edit,{by:byAlloc(a=>a==="personal"?1:0)})],[]);
      const slope=ev.cost(shifted,s)-base, v=r.by_generation[g].personal;
      for(let j=0;j<161;j++) net[j]+=slope*(v[j]-v[0]);
      one.push(Object.assign({},r.edit,{by:byAlloc(a=>a==="personal"?v[1]-v[0]:0)}));
    }
    linearGap=Math.max(linearGap,Math.abs(ev.cost(V7.withStep(m,one,[]),s)-base-net[1]));
    if(!summary.state_price_replicate_delta_bn[conv][g])summary.state_price_replicate_delta_bn[conv][g]=[];
    summary.state_price_replicate_delta_bn[conv][g].push(net);
    return Math.sqrt(4/160*sum(net.slice(1).map(v=>v*v)));
  });
  gate(`${conv}: state-price replicate propagation is linear at fixed keys/responses`,linearGap<1e-9,linearGap);
}
for(const conv of CONVS) {
  summary.reporter_parent_replicate_delta_bn[conv]={};
  summary.reporter_parent_conditional_se_bn[conv]={};
  let linearGap=0;
  for(const g of GENS)summary.reporter_parent_conditional_se_bn[conv][g]=ends.map(i=> {
    const m=models[conv][g],s=specs[i],base=res[conv][g].cost[i],net=Array(161).fill(0),one=[],other=[],controls=new Set();
    const selected=res[conv][g].full[i],rows=new Map(selected.evaluation.spending.map(r=>[r.id,r]));
    const capitalStrings=new Set(V7.stringLeaves(L.payload.meta.capital_return));
    for(const r of layers[conv].reporter_replicate_adjustments) {
      const v=r.by_generation[g].personal;
      if(v.every(x=>x===v[0]))continue;
      const row=rows.get(r.edit.line),carrier=L.payload.meta.union_completion.carriers[r.edit.line];
      if(r.edit.side!=="spending"||r.edit.key!=="k"||!row||!carrier||capitalStrings.has(r.edit.line))
        throw Error(`[BLOCKED] reporter cost derivative lacks a declared independent spending carrier ${r.edit.line}`);
      // Engine.evaluate: spending contributes -fiscal_weight*response*target.
      // These zero-national carriers are absent from public-capital key formulas.
      const slope=selected.state.fiscal_weight*row.response;
      const unit=Object.assign({},r.edit,{by:byAlloc(a=>a==="personal"?1:0)});
      const control=`${carrier.kind}|${carrier.side||"fixed"}|${row.response===0?"inactive":"active"}`;
      if(!controls.has(control)) {
        linearGap=Math.max(linearGap,Math.abs(ev.cost(V7.withStep(m,[unit],[]),s)-base-slope));
        controls.add(control);
      }
      for(let j=0;j<161;j++)net[j]+=slope*(v[j]-v[0]);
      one.push(Object.assign({},r.edit,{by:byAlloc(a=>a==="personal"?v[1]-v[0]:0)}));
      other.push(Object.assign({},r.edit,{by:byAlloc(a=>a==="personal"?v[80]-v[0]:0)}));
    }
    linearGap=Math.max(linearGap,Math.abs(ev.cost(V7.withStep(m,one,[]),s)-base-net[1]),
      Math.abs(ev.cost(V7.withStep(m,other,[]),s)-base-net[80]));
    if(!summary.reporter_parent_replicate_delta_bn[conv][g])summary.reporter_parent_replicate_delta_bn[conv][g]=[];
    summary.reporter_parent_replicate_delta_bn[conv][g].push(net);
    return Math.sqrt(4/160*sum(net.slice(1).map(v=>v*v)));
  });
  const gap=Math.max(...ends.flatMap((_,k)=>Array.from({length:161},(_,j)=>
    Math.abs(sum(GENS.map(g=>summary.reporter_parent_replicate_delta_bn[conv][g][k][j]))))));
  gate(`${conv}: observed reporter routing replicates are linear and preserve the fixed source total`,linearGap<1e-9&&gap<1e-9,`${linearGap} / ${gap}`);
}
gate("both convention headcounts conserve the lineage and adults",CONVS.every(c=>
  Math.abs(sum(GENS.map(g=>summary.conventions[c][g].population))-population)<1e-6 &&
  Math.abs(sum(GENS.map(g=>summary.conventions[c][g].adults))-adults)<1e-6));
summary.g2_adults_alone={formula:"G2(a) - [G1(b) - G1(a)] (cost allocation residual; not a measured age cell)",
  cost_bn:ends.map((i,k)=>res.a.G2.cost[i]-(res.b.G1.cost[i]-res.a.G1.cost[i])),
  population:H.a.G2.adults,production_rule:productionRule};
gate("G2 adults residual identity",summary.g2_adults_alone.cost_bn.every((v,k)=>Math.abs(v-
  (summary.conventions.a.G2.cost_bn[k]-(summary.conventions.b.G1.cost_bn[k]-summary.conventions.a.G1.cost_bn[k])))<1e-9));
if (fails.length) { console.error(`[BLOCKED] ${fails.length} gates failed; nothing written`); process.exit(1); }
fs.mkdirSync(OUT, { recursive: true });
const header = Object.keys(rows[0]);
publish(path.join(OUT, `generation_results_${CASE}.csv`), () => [header.join(","), ...rows.map((r) => header.map((k) => typeof r[k] === "number" && k!=="minor_scale" ? r[k].toFixed(6) : r[k]).join(","))].join("\n") + "\n");
publish(path.join(OUT, `generation_summary_${CASE}.json`), () => JSON.stringify(summary, null, 1) + "\n");
publish(path.join(OUT, `generation_corrections_${CASE}.json`), () => JSON.stringify({ meta: { source: "generation_account_2026_09_24/run_generations_v8.cjs",
  case: CASE, case_lane: V7.V7_LANE, union: L.rel, status: L.payload.meta.status, builds_on: summary.builds_on.generation_payloads,
   layout: "September 29 generation payload plus declared v6/v7/v8 routes and zero-sum P7 routing adjustments; apply responses, capital_return and scoped post-engine mixed_unit_removal and coverage",
   policy,routing:{fixes,minor_scale:minorScale,production_rule:productionRule,contract:"inputs/routing.json",
     parent_rule:parentMeasurement?"observed linked-parent share under frame convention b; unlinked stay in own generation; sampling-only SDR uncertainty":"phase1 BASE wholly-G2 approximation"},
   items: summary.items.order }, payloads }) + "\n");
console.log(`case ${CASE}: ${summary.union.cost_bn.join(" / ")} bn; all ${checks.length} gates passed`);
