/* Step 1: an adopted main case, line by line, for each generation at the case's two band ends.
 *
 * --case sept27 (historical): the September 27 case. Reads read-only: the case's package
 * (main_case_long_run_2026_09_27/package.cjs), the generation account's uncorrected models
 * (generation_account_2026_09_24/derived/model_{G1,G2,G3plus}.json, convention (a): everyone in their own generation)
 * and its corrections payloads (derived/generation_corrections.json, which already end with each generation's
 * enterprise re-key edits). Each generation's corrected model is evaluated with the package's evaluateFull() at the
 * union's low and high ends (specifications found as run_generations.cjs finds them: the minimum and maximum of the
 * corrected union's cost over MAIN_SPECS).
 *
 * --case sept29: the main case adopted on 2026-09-29 (SEPT29_LANE, candidate v4's set), on the generation account's
 * v4 split (derived/generation_corrections_sept29.json, run_generations_v4.cjs), evaluated with the adopted package at
 * its main profile. The cash set beside it (the pension switch off: candidate v4's cash payload and the generation
 * account's generation_corrections_sept29_cash.json) is evaluated at the same specifications, so that the switch's
 * lines split into their parts: social_security is the accrual; medicare is its benefits less the Part A share plus
 * the Part A accrual; federal_income_tax is the cash set's less the tax on benefits. Two more splits for households.py:
 * each road line (roads_vmt_*) into its driver-mile, freight and old-key pieces (candidate v4's withRoads: the line is
 * the highway national x (FP s_vmt + (1 - FP) k_cons - k_old)); and each part-rekeyed capital component into its parent
 * line's part and its correction line's part (the adopted package's keyOf). Writes _cache/sept29/lines.json.
 *
 * --case oct05: the main case adopted on 2026-10-05 (v5, main_case_2026_10_05: the v4 case plus the lineage, the 3.04M
 * descendants who no longer report Mexican origin), on the generation account's v5 split
 * (derived/generation_corrections_oct05.json, run_generations_v5.cjs: the lineage's edits and production on G3+). It
 * runs as sept29, with three differences:
 *   - the cash set is the case lane's own corrections_cash.json, through the package's CASH (gated equal to the file);
 *   - the generation summary carries no road parameters, so each generation's driver-mile share s_vmt and pre-roads
 *     consumption key k_cons are solved from its own model's road and excise cells (candidate v4's withRoads formula
 *     on the state-local road line), gated on the federal line (1e-9) and, for G1 and G2, which the lineage leaves
 *     alone, against the September 29 summary's s_vmt (1e-9);
 *   - meta.lineage carries the added people's counts and the lineage's production term at each end: the case's union
 *     term less the September 29 union's at the same specification, gated equal to G3+'s change, with G1 and G2
 *     unchanged (1e-9). households.py places the added people and spreads that term.
 * Writes _cache/oct05/lines.json.
 *
 * --case oct07: main case v6 (main_case_2026_10_07: v5 plus the edit sets in its meta.items), on the generation account's
 * v6 split (derived/generation_corrections_oct07*.json, run_generations_v6.cjs). It runs as oct05. The pension gates take
 * v6's ratio_net and Part A accrual, and count with the lineage's own the edit sets' parts that the generation account
 * puts on the added people (rule lineage in generation_summary_oct07.json items.split: pension_tr2026's lineage parts);
 * a part on the added people on any line but the two pension lines stops the export. meta.routes lists the items' parts
 * whose split basis (splits.split_basis) is another line than the one they edit, each generation's amount from the
 * generation summary (gated to be the payload's basis and to add to the union's part); households.py spreads them as
 * that line. The union and the cash set are also gated at the case's full-precision band (its summary.json, 1e-6).
 * Writes _cache/oct07/lines.json.
 *
 * --case oct14 (historical): main case v7, on the generation account's oct14 split. MAIN_SPECS is the
 * 32 personal specifications, with its ends checked against summary.json v7.end_specifications. The adopted and
 * cash_set rows of main_case_bands.csv are the oracle. R7's job-capital lineage receipt parts and R6's credit lineage
 * parts are carried in G3+'s own lines, separately from the pension gate's lineage parts. Writes _cache/oct14/lines.json.
 *
 * --case oct16 (default): the live v9 source bridge. Builds the inherited oct15 placement scaffold in memory, then
 * export_oct16.cjs adds dynamic full-specification source atoms and calibrated count/rate metadata. Original
 * cost_bn stays the baseline; v9_target_cost_bn and v9_parts supply the final cost. Writes only _cache/oct16/.
 *
 * Every case reads capRule, each capital component's key rule, from the case's payload (meta.capital_return
 * components); on September 27 it must equal the capital lane's engine_components.json, whose rules the committed
 * outputs used.
 *
 * For every generation and end it writes each receipt and spending line (key, allocation, amount, response and
 * its cost to other residents), the production term (P, F and the specification's production dimensions) and
 * the 24 capital-return components with their key rules. households.py distributes these within each
 * generation over persons.
 * Gates (exit 1): the corrected union reproduces the case's band (September 27: $321.8194 / $387.3701bn; September 29:
 * $371.4146 / $434.8410bn and its cash set $294.7011 / $361.8175bn); each generation's rows sum to its evaluateFull()
 * cost and to the generation account's results file (1e-6 bn); the three generations sum to the union (1e-9 bn).
 * September 29 adds: the set and the cash set differ only in the three pension lines; the parts add to the payload's
 * union amounts (the accrual ratio_net x OASDI receipts, the Part A accrual, the tax on benefits; 1e-9 bn); the road
 * pieces' implied freight key is the generation's excise share before the gasoline shift (1e-9); the part-rekeyed
 * shares add to the component's key (1e-12).
 * Writes _cache/lines.json (September 27), or _cache/<case>/lines.json for a later case. Run from the repository root:
 *   node infra/immigration-fiscal/within_group_distribution_2026_09_29/export_lines.cjs [--case oct16]
 */
"use strict";
const fs = require("fs");
const crypto = require("crypto");
const path = require("path");
const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const SEPT29_LANE = "main_case_2026_09_29";
const CASES = {
  sept27: { lane: "main_case_long_run_2026_09_27", genCorrections: "generation_corrections.json",
    genResults: "generation_results.csv", band: [321.8194, 387.3701], out: "lines.json" },
  sept29: { lane: SEPT29_LANE, genCorrections: "generation_corrections_sept29.json",
    genResults: "generation_results_sept29.csv", band: [371.4146, 434.8410], out: "sept29/lines.json",
    cash: { payload: "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json",
      genCorrections: "generation_corrections_sept29_cash.json", genResults: "generation_results_sept29_cash.csv",
      band: [294.7011, 361.8175] },
    summary: "generation_summary_sept29.json" },
  // package: the cash set's package (default: the package's forPayload() of the cash payload); lineage: the case adds
  // the lineage on G3+ (meta.lineage).
  oct05: { lane: "main_case_2026_10_05", genCorrections: "generation_corrections_oct05.json",
    genResults: "generation_results_oct05.csv", band: [390.2940, 461.2431], out: "oct05/lines.json",
    cash: { payload: "main_case_2026_10_05/derived/corrections_cash.json", package: "CASH",
      genCorrections: "generation_corrections_oct05_cash.json", genResults: "generation_results_oct05_cash.csv",
      band: [307.3764, 383.4093] },
    summary: "generation_summary_oct05.json", lineage: true },
  // items: the case adds edit sets (meta.items), split by the generation account (its summary's items.split).
  oct07: { lane: "main_case_2026_10_07", genCorrections: "generation_corrections_oct07.json",
    genResults: "generation_results_oct07.csv", band: [389.0826, 461.4797], out: "oct07/lines.json",
    cash: { payload: "main_case_2026_10_07/derived/corrections_cash.json", package: "CASH",
      genCorrections: "generation_corrections_oct07_cash.json", genResults: "generation_results_oct07_cash.csv",
      band: [307.3994, 385.3641] },
    summary: "generation_summary_oct07.json", lineage: true, items: true },
  oct14: { lane: "main_case_2026_10_14", genCorrections: "generation_corrections_oct14.json",
    genResults: "generation_results_oct14.csv", out: "oct14/lines.json",
    cash: { payload: "main_case_2026_10_14/derived/corrections_cash.json", package: "CASH",
      genCorrections: "generation_corrections_oct14_cash.json", genResults: "generation_results_oct14_cash.csv" },
    summary: "generation_summary_oct14.json", lineage: true, items: true, live: true },
  oct15: { lane: "main_case_2026_10_15", genCorrections: "generation_corrections_oct15.json",
    genResults: "generation_results_oct15.csv", out: "oct15/lines.json",
    cash: { payload: "main_case_2026_10_15/derived/corrections_cash.json", package: "CASH",
      genCorrections: "generation_corrections_oct15_cash.json", genResults: "generation_results_oct15_cash.csv" },
    summary: "generation_summary_oct15.json", lineage: true, items: true, live: true, v8: true },
};
const argv = process.argv.slice(2);
const REQUESTED_CASE = argv.includes("--case") ? argv[argv.indexOf("--case") + 1] : "oct16";
if (REQUESTED_CASE === "oct16") require("../scripts/adoption_gate.cjs").requireAdopted("oct16");
if (argv.includes("--control-item")) {
  if(REQUESTED_CASE!=="oct16")throw Error("[BLOCKED] --control-item is oct16 only");
  require("./export_controls_oct16.cjs").run(argv);
  process.exit(0);
}
// Oct16 retains the thoroughly checked source-placement scaffold in memory, then
// adds its full-specification typed changes. No historical export is rewritten.
const CASE = REQUESTED_CASE === "oct16" ? "oct15" : REQUESTED_CASE;
if (!CASES[CASE]) throw new Error(`--case must be one of ${Object.keys(CASES).join(", ")}`);
const C = CASES[CASE];
const ALLOCATION = argv.includes("--allocation") ? argv[argv.indexOf("--allocation") + 1] : "personal";
if (!["personal", "shared"].includes(ALLOCATION) || (ALLOCATION === "shared" && !C.live)) {
  throw new Error("[BLOCKED] --allocation shared is the oct14 companion; allocation must be personal or shared");
}
C.shared = ALLOCATION === "shared";
if (C.shared) C.out = `${CASE}/shared_allocation/lines.json`;
if (C.live) {
  const csv = fs.readFileSync(path.join(FISCAL, C.lane, "derived/main_case_bands.csv"), "utf8").trim().split("\n");
  const head = csv.shift().split(",");
  const rows = csv.map((line) => Object.fromEntries(line.split(",").map((v, i) => [head[i], v])));
  const bandOf = (variant) => {
    const r = rows.find((x) => x.profile === "long_run_non_school_full" && x.variant === variant);
    if (!r) throw new Error(`[BLOCKED] ${C.lane}: no main_case_bands.csv row ${variant}`);
    const b = [Number(r.cost_low_bn), Number(r.cost_high_bn)];
    if (!b.every(Number.isFinite)) throw new Error(`[BLOCKED] ${variant}: invalid band`);
    return b;
  };
  C.band = bandOf(C.shared ? "shared_allocation" : "adopted");
  C.cash.band = bandOf(C.shared ? "shared_allocation_cash_set" : "cash_set");
}
const V4 = CASE !== "sept27";   // the v4 rules: sept29 and every case built on it
const P = require(path.join(FISCAL, C.lane, "package.cjs"));
const { Engine, MODEL } = P;
// ALL_SPECS keeps v6's original numbering; a shared companion filters it rather than renumbering 32–63.
const MAIN_SPECS = C.shared ? P.ALL_SPECS : P.MAIN_SPECS;
const PROFILE = V4 ? P.MAIN_PROFILE : undefined;
const GEN = path.join(FISCAL, "generation_account_2026_09_24", "derived");
const GENS = ["G1", "G2", "G3plus"];
const read = (f) => JSON.parse(fs.readFileSync(f, "utf8"));
let fails = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) fails += 1;
}

const corrections = read(path.join(FISCAL, C.lane, "derived/corrections.json"));
// Each capital component's key rule, from the case's payload. The committed September 27 outputs used the capital
// lane's rules, which that payload carries unchanged.
const capRule = Object.fromEntries(corrections.meta.capital_return.components.map((c) => [c.id, c.key]));
if (!V4) {
  const CAP = read(path.join(FISCAL, "capital_return_services_2026_09_27/derived/engine_components.json"));
  gate("the payload's capital key rules are the capital lane's (engine_components.json)",
    JSON.stringify(capRule) === JSON.stringify(Object.fromEntries(CAP.components.map((c) => [c.id, c.key]))),
    `${Object.keys(capRule).length} components`);
} else {
  gate("the adopted package's payload is its derived/corrections.json", JSON.stringify(P.correctionsPayload()) === JSON.stringify(corrections));
}
const unionModel = V4 ? P.payloadModel() : Engine.applyCorrections(MODEL, corrections);
// v8's shared companion excludes item 11 (the stayers' consequences of a removal belong to the removal total, not to
// a rule for sharing the group's total among its members); one definition: the case's companions.adjustedRun.
const COMP = C.v8 && C.shared ? require(path.join(FISCAL, C.lane, "companions.cjs")) : null;
const unionCost = (api, m, s) => COMP ? COMP.adjustedRun(api, m, s, "shared").cost_bn : api.evaluateFull(m, s, PROFILE).cost_bn;
const uCost = MAIN_SPECS.map((s) => unionCost(P, unionModel, s));
const indices = MAIN_SPECS.map((s, i) => i).filter((i) => !C.live || MAIN_SPECS[i].allocation === ALLOCATION);
const lo = indices.reduce((a, i) => uCost[i] < uCost[a] ? i : a), hi = indices.reduce((a, i) => uCost[i] > uCost[a] ? i : a);
gate("the corrected union reproduces the adopted case", Math.abs(uCost[lo] - C.band[0]) < 1e-4 && Math.abs(uCost[hi] - C.band[1]) < 1e-4,
  `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)} at specifications ${lo} / ${hi} (0-based)`);
// oct07: the case's full-precision band (its summary.json), as well as the pinned four decimals.
const FULL = C.items ? read(path.join(FISCAL, C.lane, "derived/summary.json")) : null;
const VERSION = FULL && (C.v8 ? FULL.v8 : FULL.v7);
const endsOf = (which) => C.v8 ? VERSION.end_specifications[which][0] : VERSION.end_specifications[which];
const sharedEnds = which => C.v8 ? VERSION.companions.shared_allocation[which === "set" ? "ends" : "cash_ends"][0]
  : which === "set" ? VERSION.companions.shared_allocation.ends : VERSION.companions.shared_allocation.cash.ends;
const sharedBand = which => C.v8 ? VERSION.companions.shared_allocation[which === "set" ? "band_bn" : "cash_set_bn"]
  : which === "set" ? VERSION.companions.shared_allocation.band_bn : VERSION.companions.shared_allocation.cash.band_bn;
if (FULL) {
  const band = C.shared ? sharedBand("set") : FULL.main_case;
  const ends = C.shared ? sharedEnds("set") : C.live ? endsOf("set") : null;
  if (C.live) gate(`the ${ALLOCATION} band's 32 specifications and ends match the case summary`,
    indices.length === 32 && JSON.stringify([lo, hi]) === JSON.stringify(ends));
  gate(`the corrected union is the case's full-precision band (${C.lane}/derived/summary.json main_case, 1e-6)`,
    Math.abs(uCost[lo] - band[0]) < 1e-6 && Math.abs(uCost[hi] - band[1]) < 1e-6,
    `${uCost[lo].toFixed(6)} / ${uCost[hi].toFixed(6)} against ${band.map((v) => v.toFixed(6)).join(" / ")}`);
}

function resultsOf(file) {
  const results = fs.readFileSync(path.join(GEN, file), "utf8").trim().split("\n");
  const head = results[0].split(",");
  const out = {};
  for (const row of results.slice(1)) {
    const r = Object.fromEntries(row.split(",").map((v, i) => [head[i], v]));
    if (r.convention === "a") out[`${r.generation}|${r.band_end}`] = Number(r.cost_bn);
  }
  return out;
}
const pay = read(path.join(GEN, C.genCorrections)).payloads.a;
const published = resultsOf(C.genResults);
const apiPayloads = new Map([[P, pay]]);
const v8Evaluator = C.v8 ? require("../generation_account_2026_09_24/v8_split.cjs").evaluator : null;
function withoutChildren(model, payload, sourcePayload = corrections) {
  if (!C.v8 || !payload.meta.union_completion.production_delta) return model;
  // Registry offsets locate edits in the union's payload, not in a generation's independently built edit stack.
  const it = sourcePayload.meta.items.find(i=>i.id==="union_completion");
  const edits = Object.entries(it.parts).filter(([n])=>n.startsWith("lineage_g3plus:observed_nonreporters:"))
    .map(([,p])=>({...sourcePayload.edits[it.edits.first+p.edit],by:Object.fromEntries(Object.entries(p.by).map(([a,v])=>[a,-v]))}));
  let m = Engine.applyCorrections(model,{edits,meta:model.corrections});
  const delta = payload.meta.union_completion.production_delta;
  m = JSON.parse(JSON.stringify(m));
  for (const key of ["private_wtp_bn","induced_receipts_bn"]) m.production[key] = m.production[key].map((v,i)=>v-delta[key][i]);
  return m;
}

function selectedPost(api, spec, generation) {
  if (!C.v8) return {};
  const meta = api.correctionsPayload().meta;
  return Object.fromEntries(["mixed_unit_removal", "coverage"].filter(k => meta[k]).map(k => {
    const end = meta[k].by_end[spec.reading];
    const parts = end.by_generation_bn || end.by_generation;
    const value = generation ? parts[generation === "G3plus" ? (Object.hasOwn(parts, "G3plus") ? "G3plus" : "G3+") : generation] : end.total_bn;
    if (!Number.isFinite(value)) throw Error(`[BLOCKED] ${k}: no declared ${generation || "union"} amount`);
    return [k, value];
  }));
}
function dump(m, spec, api = P, generation = null, personal = false) {
  const full = C.v8 && generation ? v8Evaluator(apiPayloads.get(api)[generation], api).evaluateFull(m, spec)
    : api.evaluateFull(m, spec, PROFILE);
  const state = full.state || (V4 ? api.stateFor(m, spec, PROFILE) : api.stateFor(api.withSyntheticLines ? api.withSyntheticLines(m) : m, spec));
  const post = selectedPost(api, spec, generation);
  if (COMP && !personal && Object.hasOwn(post, "mixed_unit_removal")) post.mixed_unit_removal = 0;
  const cost = full.cost_bn - (full.post_engine?.total_bn || 0) + Object.values(post).reduce((s,v)=>s+v,0);
  const ev = full.evaluation, fw = state.fiscal_weight;
  const rows = [];
  for (const r of ev.receipts) {
    rows.push({ side: "receipt", id: r.id, key: r.key, scenario: state.receipt_scenario, group: r.group,
      response_class: r.response_class, amount_bn: r.amount_bn, response: r.response, cost_bn: -fw * r.effect_bn });
  }
  for (const r of ev.spending) {
    rows.push({ side: "spending", id: r.id, key: r.key, group: r.group, response_class: r.response_class,
      amount_bn: r.amount_bn, response: r.response, cost_bn: -fw * r.effect_bn });
  }
  const capital = full.capital.components.map((c) => ({ id: c.id, part: c.group, level: c.level, rule: capRule[c.id],
    key: c.key, response: c.response, cost_bn: c.return_bn }));
  if (V4) {
    // A part-rekeyed component's key is its parent line's share plus its correction line's amount over the part's
    // national total (the adopted package's keyOf); households.py spreads the return in those two parts.
    for (const c of capital) {
      if (c.rule.kind !== "part_rekeyed") continue;
      const parent = ev.spending.find((l) => l.id === c.rule.parent_line), part = ev.spending.find((l) => l.id === c.rule.correction_line);
      c.shares = { parent: parent.amount_bn / parent.national_bn, part: part.amount_bn / c.rule.part_national_bn };
      if (Math.abs(c.shares.parent + c.shares.part - c.key) > 1e-12) throw new Error(`[BLOCKED] ${c.id}: its two parts do not add to its key`);
    }
  }
  const production = { dims: state.production, count: state.count_production, fiscal_weight: fw,
    private_wtp_bn: ev.private_wtp_bn, induced_receipts_bn: ev.induced_receipts_bn,
    cost_bn: -(ev.private_wtp_bn + fw * ev.induced_receipts_bn) };
  const sum = rows.reduce((a, r) => a + r.cost_bn, 0) + capital.reduce((a, c) => a + c.cost_bn, 0) + production.cost_bn
    + Object.values(post).reduce((s,v)=>s+v,0);
  return { cost_bn: cost, sum_bn: sum, allocation: state.allocation, receipt_scenario: state.receipt_scenario,
    rows, capital, production, post_engine: post };
}

function childPricing(api, payload) {
  if (!C.v8 || !payload.meta.union_completion.production_delta) return null;
  const source = require("../main_case_2026_10_15/item_union.cjs");
  const units = source.optionRates(P.OCT14,{foreign_source_tax:true},true).unit_models;
  const basis = api === P ? "set" : "cash", base = basis === "set" ? P.OCT14 : P.OCT14.CASH;
  const rec = base.correctionsPayload().meta.items.find(r=>r.id==="child_credits"), bp = base.correctionsPayload();
  const detail = P.ITEM_DETAIL.added_age_mix.counts, c3=payload.meta.union_completion.c3;
  const den = detail.later+(1-c3)*detail.g3_rate;
  const componentFile="school_enrollment_2026_09_20/derived/updated_account_components.csv";
  const componentRows=fs.readFileSync(path.join(FISCAL,componentFile),"utf8").trim().split("\n").map(r=>r.split(","));
  const componentHead=componentRows.shift();
  const components=componentRows.map(r=>Object.fromEntries(componentHead.map((k,i)=>[k,r[i]])));
  const schoolShare=Object.fromEntries(["personal","shared"].map(allocation=>{
    const values=["school","P"].map(component=>components.filter(r=>r.allocation===allocation &&
      r.group==="national_civilian" && r.component===component));
    if(values.some(r=>r.length!==1)) throw Error("[BLOCKED] native education lacks unique national school/P declaration");
    const [ns,np]=values.map(r=>Number(r[0].spending_bn));
    if(!(ns>0 && np>0)) throw Error("[BLOCKED] native education national school/P masses are invalid");
    return [allocation,ns/(ns+np)];
  }));
  function educationSchool(model, evaluated) {
    const row=evaluated.rows.find(r=>r.side==="spending" && r.id==="education_services");
    if(row.key==="school_operating") return row.cost_bn;
    if(row.key!=="education_mix") throw Error(`[BLOCKED] native education category split has no declared key ${row.key}`);
    const line=model.spending.lines.find(r=>r.id===row.id),a=evaluated.allocation;
    const mix=line.keys.education_mix[a].target_bn, school=line.keys.school_operating[a].target_bn*schoolShare[a];
    if(mix===0) {
      if(school!==0 || row.cost_bn!==0) throw Error("[BLOCKED] native education zero mix has nonzero component");
      return 0;
    }
    return row.cost_bn*school/mix;
  }
  const records=[];
  for (const person of payload.meta.union_completion.observed_records.filter(r=>r.observed_nonreporter)) {
    const gWeight=person.economic_class==="g3_rate"?1-c3:1, whiteWeight=1-gWeight;
    const g0=units[person.age_band].g3[basis], white=units[person.age_band].white[basis];
    const creditEdits=Object.entries(rec.parts).filter(([n])=>n.startsWith("lineage_g3plus:")).map(([,part])=>({
      ...bp.edits[rec.edits.first+part.edit],by:Object.fromEntries(Object.entries(part.by).map(([a,v])=>[a,-v/den]))}));
    const g=Engine.applyCorrections(g0,{edits:creditEdits,meta:g0.corrections});
    const ends={};
    for(const [end,i] of [["low",lo],["high",hi]]) {
      const spec=JSON.parse(JSON.stringify(MAIN_SPECS[i]));
      for(const id of Object.keys(payload.meta.union_completion.carriers)) delete spec.line_responses[id];
      const a=dump(g,spec,base),b=dump(white,spec,base);
      ends[end]={rows:a.rows.map((r,j)=>({...r,amount_bn:gWeight*r.amount_bn+whiteWeight*b.rows[j].amount_bn,cost_bn:gWeight*r.cost_bn+whiteWeight*b.rows[j].cost_bn})),
        capital:a.capital.map((r,j)=>({...r,cost_bn:gWeight*r.cost_bn+whiteWeight*b.capital[j].cost_bn})),
        production_bn:gWeight*a.production.cost_bn+whiteWeight*b.production.cost_bn};
      const education=ends[end].rows.find(r=>r.side==="spending" && r.id==="education_services");
      const schools=gWeight*educationSchool(g,a)+whiteWeight*educationSchool(white,b);
      education.category_cost_bn={schools,education_other:education.cost_bn-schools};
    }
    records.push({...person,ends});
  }
  return {basis,source:"native transformed own-age G3/white unit models, projection removed before selected specification",
    education_category_source:{file:componentFile,sha256:crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL,componentFile))).digest("hex"),
      rule:"education_mix school component = school_operating target x national school/(school+P); residual is P",school_share:schoolShare},records};
}

function statePriceParts(payload, generation, evaluated) {
  const route=payload.meta.added_state_price_routing;
  if(!route) return [];
  if(!payload.meta.coverage || payload.meta.coverage.stub) throw Error("[BLOCKED] added-state route requires real coverage");
  const sourceFile="generation_account_2026_09_24/derived/generation_state_indexes.json";
  const indexes=read(path.join(FISCAL,sourceFile)).conventions.a;
  const allocation=evaluated.allocation, result=[];
  for(const change of route.changes) {
    const e=change.edit;
    const row=evaluated.rows.find(r=>r.side===e.side && r.id===e.line &&
      (e.side==="receipt"?r.scenario===e.scenario:r.key===e.key));
    if(!row) continue; // An inactive receipt scenario contributes no cost at this end.
    const sources=change.charge_sources.filter(r=>r.allocation===allocation);
    if(sources.length!==1) throw Error("[BLOCKED] added-state change lacks unique allocation source");
    const source=sources[0], charges=source.identified_charges, added=source.added_charges;
    const population=source.added_charges_by_population;
    if(!population || Object.keys(population).sort().join(",")!=="latent,native")
      throw Error("[BLOCKED] added-state source lacks latent/native decomposition");
    const amounts={identified:0,latent:0,native:0};
    const oldDen=GENS.reduce((s,g)=>s+charges[g],0), den=GENS.reduce((s,g)=>s+charges[g]+added[g],0);
    if(!(oldDen>0 && den>0)) throw Error("[BLOCKED] invalid added-state normalization masses");
    const functions=source.functions || [{function:source.function,sl_amount_bn:source.factor}];
    for(const item of functions) {
      const values=Object.fromEntries(GENS.map(g=>[g,indexes[item.function][g].replicates[0]]));
      const oldMean=GENS.reduce((s,g)=>s+charges[g]*values[g],0)/oldDen;
      const mean=GENS.reduce((s,g)=>s+charges[g]*values[g]+added[g]*values.G3plus,0)/den;
      amounts.identified+=item.sl_amount_bn*charges[generation]*(oldMean-mean);
      for(const name of ["latent","native"]) amounts[name]+=item.sl_amount_bn*population[name][generation]*(values.G3plus-mean);
    }
    for(const g of GENS) if(Math.abs(population.latent[g]+population.native[g]-added[g])>1e-12)
      throw Error("[BLOCKED] added-state population charges do not reproduce added mass");
    const delta=change.by_generation[generation][allocation];
    gate(`${generation} ${e.side} ${e.line}: identified/latent/native state deltas reproduce generation change (1e-9 bn)`,
      Math.abs(Object.values(amounts).reduce((s,v)=>s+v,0)-delta)<1e-9);
    const coefficient=(e.side==="receipt"?-1:1)*evaluated.production.fiscal_weight*row.response;
    result.push({edit:e,source_cell:source.source_cell,charge_source:source,amount_bn:delta,
      cost_bn:delta*coefficient,amount_by_population:amounts,
      cost_by_population:Object.fromEntries(Object.entries(amounts).map(([k,v])=>[k,v*coefficient])),
      indexes_source:{file:sourceFile,sha256:crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL,sourceFile))).digest("hex")},
      rule:route.rule});
  }
  return result;
}

function childCostMetadata(exported) {
  const records=exported.meta.child_pricing?.records || [];
  if(!records.length) return;
  for(const end of ["low","high"]) {
    for(const record of records) {
      const block=record.ends[end];
      block.base_cost_bn=block.rows.reduce((s,r)=>s+r.cost_bn,0)+block.capital.reduce((s,r)=>s+r.cost_bn,0)+block.production_bn;
      block.state_price_cost_bn=0;
    }
    const generation=exported.generations.G3plus[end];
    let extra=0;
    for(const part of generation.added_state_prices || []) {
      const cost=part.cost_by_population.native;
      if(cost===0) continue;
      const [side,id,key]=part.source_cell.split("|");
      const amounts=records.map(record=>{
        const row=record.ends[end].rows.find(r=>r.side===side && r.id===id);
        if(!row || (side==="receipt"?row.scenario:row.key)!==key) throw Error("[BLOCKED] native state unit metadata lacks selected source row");
        return row.amount_bn;
      });
      const denominator=records.reduce((s,r,i)=>s+r.people*amounts[i],0);
      if(!(denominator>0) || amounts.some(v=>v<0)) throw Error("[BLOCKED] native state unit metadata has invalid mass");
      records.forEach((record,i)=>{record.ends[end].state_price_cost_bn+=cost*amounts[i]/denominator;});
      extra+=cost;
    }
    for(const record of records) {
      const block=record.ends[end];
      block.cost_bn=block.base_cost_bn+block.state_price_cost_bn;
      block.state_price_rule="central convention(a) household native component: exact selected source amount / observed native source mass";
    }
    const base=records.reduce((s,r)=>s+r.people*r.ends[end].base_cost_bn,0);
    const state=records.reduce((s,r)=>s+r.people*r.ends[end].state_price_cost_bn,0);
    gate(`${exported.meta.basis} native ${end}: per-record base/state unit metadata conserves principal components (1e-9 bn)`,
      Math.abs(base-(generation.cost_bn-generation.before_native_children.cost_bn))<1e-9 && Math.abs(state-extra)<1e-9);
  }
}

function addedStateTargetMetadata(exported) {
  const source={...exported.meta.coverage_added_cost_bn}, delta={};
  for(const end of ["low","high"]) {
    let identified=0,latent=0,native=0;
    for(const g of GENS) for(const part of exported.generations[g][end].added_state_prices || []) {
      const costs=part.cost_by_population;
      if(Object.keys(costs).sort().join(",")!=="identified,latent,native" || Object.values(costs).some(v=>!Number.isFinite(v)))
        throw Error("[BLOCKED] final added-state target has invalid population costs");
      gate(`${exported.meta.basis} ${g} ${end} ${part.edit.line}: final target subtotal closes (1e-9 bn)`,
        Math.abs(costs.identified+costs.latent+costs.native-part.cost_bn)<1e-9);
      identified+=costs.identified;latent+=costs.latent;native+=costs.native;
    }
    delta[end]=latent+native;
    gate(`${exported.meta.basis} ${end}: identified offset balances final added state reallocation (1e-9 bn)`,
      Math.abs(identified+delta[end])<1e-9);
    exported.meta.coverage_added_cost_bn[end]=source[end]+delta[end];
    gate(`${exported.meta.basis} ${end}: final added target preserves source plus declared state delta (1e-9 bn)`,
      Number.isFinite(source[end]) && Math.abs(exported.meta.coverage_added_cost_bn[end]-source[end]-delta[end])<1e-9);
  }
  exported.meta.coverage_added_source_cost_bn=source;
  exported.meta.coverage_added_state_reallocation_bn=delta;
  exported.meta.coverage_added_source_cost_source=exported.meta.coverage_added_cost_source;
  exported.meta.coverage_added_state_reallocation_source={
    file:`generation_account_2026_09_24/derived/${exported.meta.basis==="set"?C.genCorrections:C.cash.genCorrections}`,
    declaration:"payloads.a.{generation}.meta.added_state_price_routing; active selected end response",
    rule:"sum active latent + native state costs; identified offset balances, no post-engine coverage included",
    convention:"a",spec_index:exported.meta.spec_index};
  exported.meta.coverage_added_cost_source=exported.meta.coverage_added_source_cost_source+" + declared active latent/native state reallocation";
}

const out = { meta: { case: C.lane, convention: "a", spec_index: { low: lo, high: hi },
  specs: { low: MAIN_SPECS[lo], high: MAIN_SPECS[hi] } }, union: {}, generations: {} };
if (C.live) out.meta.allocation = ALLOCATION;
if (C.v8) {
  out.meta.basis = "set";
  out.meta.union_completion = corrections.meta.union_completion;
  out.meta.coverage = corrections.meta.coverage || null;
  out.meta.mixed_unit_removal = corrections.meta.mixed_unit_removal;
  if (COMP) out.meta.shared_post_engine_rule = "shared companion: item 11 (mixed_unit_removal) excluded from every " +
    "generation and the union (companions.adjustedRun); coverage at central personal prices; the personal-ends oracle keeps item 11";
  out.meta.population_v8 = corrections.meta.population_v8;
  const lineage = read(path.join(FISCAL,C.lane,"derived/lineage_addition.json")).v8;
  if (!lineage) throw Error("[BLOCKED] v8 lineage addition contract absent");
  out.meta.coverage_added_cost_bn = Object.fromEntries(["low","high"].map((end,i)=>[end,lineage.set.all_nonreporting_descendants.cost_bn[i]]));
  out.meta.coverage_added_cost_source = `${C.lane}/derived/lineage_addition.json v8.set.all_nonreporting_descendants.cost_bn`;
  out.meta.child_pricing = childPricing(P, corrections);
}
if (C.items) {
  // The items' carriers (an item's capital: receipt lines whose share keys its offset components) and the parent line
  // its meta splits each by (splits.split_basis); households.py spreads an offset's return as that line.
  out.meta.carriers = {};
  for (const r of corrections.meta.items.filter((x) => x.applied && x.capital)) for (const id of r.capital.receipt_lines) {
    const basis = (r.meta_changed || []).map((k) => corrections.meta[k] && corrections.meta[k].splits && corrections.meta[k].splits.split_basis)
      .find((S) => S && S[id]);
    if (!basis) throw new Error(`[BLOCKED] item ${r.id}: carrier ${id} has no split_basis in its meta`);
    out.meta.carriers[id] = { item: r.id, parent_line: basis[id] };
  }
}
for (const [end, i] of [["low", lo], ["high", hi]]) {
  out.union[end] = dump(unionModel, MAIN_SPECS[i]);
  gate(`union ${end}: rows sum to the cost`, Math.abs(out.union[end].sum_bn - out.union[end].cost_bn) < 1e-9,
    `${out.union[end].sum_bn.toFixed(6)} vs ${out.union[end].cost_bn.toFixed(6)}`);
}
const models = {};
for (const g of GENS) {
  const m0 = read(path.join(GEN, `model_${g}.json`));
  const m1 = Engine.applyCorrections(m0, pay[g]);
  models[g] = { m0, m1 };
  out.generations[g] = {};
  for (const [end, i] of [["low", lo], ["high", hi]]) {
    const d = dump(m1, MAIN_SPECS[i], P, g);
    if(C.v8 && pay[g].meta.added_state_price_routing) d.added_state_prices=statePriceParts(pay[g],g,d);
    if (C.v8 && g === "G3plus" && pay[g].meta.union_completion.production_delta) {
      d.before_native_children = dump(withoutChildren(m1,pay[g]),MAIN_SPECS[i],P,g);
    }
    out.generations[g][end] = d;
    // The generation result file reports personal ends. Keep its oracle on the shared companion's input model too.
    const publishedCost = C.shared
      ? dump(m1, P.MAIN_SPECS[endsOf("set")[end === "low" ? 0 : 1]], P, g, true).cost_bn : d.cost_bn;
    gate(`${g} ${end}: rows sum to their evaluateFull(); the model at the published ends matches ${C.genResults}`,
      Math.abs(d.sum_bn - d.cost_bn) < 1e-9 && Math.abs(publishedCost - published[`${g}|${end}`]) < 1e-6,
      `${d.cost_bn.toFixed(6)} at this end; published ${publishedCost.toFixed(6)} vs ${published[`${g}|${end}`]}`);
  }
}
for (const end of ["low", "high"]) {
  const s = GENS.reduce((a, g) => a + out.generations[g][end].cost_bn, 0);
  gate(`${end}: the three generations add to the union`, Math.abs(s - out.union[end].cost_bn) < 1e-9, `${s.toFixed(6)}`);
}

if (C.lineage) {
  // The lineage (meta.lineage): the added people's counts, and the lineage's production term at each end, the case's
  // union term less the September 29 union's at the same specification. The generation account puts all of it on G3+.
  console.log("[lineage: the added people's production term]");
  const L = corrections.meta.lineage, P29 = P.SEPT29;
  const prodOf = (m, spec) => {
    const e = P29.evaluateFull(m, spec, PROFILE).evaluation;
    return -(e.private_wtp_bn + P29.stateFor(m, spec, PROFILE).fiscal_weight * e.induced_receipts_bn);
  };
  const pay29 = read(path.join(GEN, CASES.sept29.genCorrections)).payloads.a;
  out.meta.lineage = { counts: L.counts, members: L.members, c3: L.c3.value, production_bn: {} };
  // oct07: the added people's measured age mix (the case's item added_age_mix), which households.py places them at.
  if (L.age_mix) out.meta.lineage.age_mix = { item: L.age_mix.item, reading: L.age_mix.reading, bands: L.age_mix.bands, mixes: L.age_mix.mixes };
  for (const [end, i] of [["low", lo], ["high", hi]]) {
    const s29 = P29.MAIN_SPECS[i];
    gate(`${end}: the September 29 specification ${i} has the case's production dimensions`,
      JSON.stringify(P29.stateFor(P29.payloadModel(), s29, PROFILE).production) === JSON.stringify(out.union[end].production.dims));
    const child = out.generations.G3plus[end].before_native_children;
    const childProduction = child ? out.generations.G3plus[end].production.cost_bn-child.production.cost_bn : 0;
    const dU = out.union[end].production.cost_bn - prodOf(P29.payloadModel(), s29)-childProduction;
    const dG = GENS.map((g) => out.generations[g][end].production.cost_bn - prodOf(Engine.applyCorrections(models[g].m0, pay29[g]), s29)
      -(g==="G3plus"?childProduction:0));
    gate(`${end}: the lineage's production term is all on G3+, which moves by the union's change; G1 and G2 do not move (1e-9 bn)`,
      Math.abs(dG[2] - dU) < 1e-9 && Math.abs(dG[0]) < 1e-9 && Math.abs(dG[1]) < 1e-9, `${dU.toFixed(6)} bn`);
    out.meta.lineage.production_bn[end] = dU;
  }
}

if (V4) {
  const V = P.V4PKG;
  const PA = corrections.meta.pension_accrual;
  const SUM = read(path.join(GEN, C.summary));
  if (C.v8) {
    out.meta.population_rounding = SUM.population_rounding;
    if (out.meta.population_rounding?.generation !== "G1" || !Number.isFinite(out.meta.population_rounding.people)) {
      throw Error("[BLOCKED] missing principal G1 population rounding declaration");
    }
  }
  const ALLOC = { low: MAIN_SPECS[lo].allocation, high: MAIN_SPECS[hi].allocation };
  // oct07: the generation account's G3+ members and adults (the added people's adults at their age mix), which
  // households.py's placement must reproduce.
  if (C.items) {
    const G3 = SUM.conventions.a.G3plus;
    out.meta.lineage.generation_g3plus = { population: G3.population, adults: G3.adults, source: `generation_account_2026_09_24/derived/${C.summary}` };
    if (C.v8 && out.meta.coverage) {
      const coverage=out.meta.coverage, file=path.join(FISCAL,coverage.file);
      if(coverage.stub || crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex")!==coverage.sha256)
        throw Error("[BLOCKED] household observed adult target requires principal live coverage counts");
      const source=read(file).sets[coverage.which].scenarios[coverage.construction];
      const population=source.implied_net_missing_people.G3plus, adults=source.adults_by_generation.G3plus;
      if(!Number.isFinite(population) || !Number.isFinite(adults) ||
         Math.abs(population-coverage.counts_by_generation.G3plus)>1e-6)
        throw Error("[BLOCKED] household coverage population/adult source mismatch");
      out.meta.lineage.complete_generation_g3plus={...out.meta.lineage.generation_g3plus};
      Object.assign(out.meta.lineage.generation_g3plus,{population:G3.population-population,adults:G3.adults-adults,
        coverage_excluded:{population,adults,file:coverage.file,sha256:coverage.sha256,
          declaration:`sets.${coverage.which}.scenarios.${coverage.construction}.implied_net_missing_people/adults_by_generation.G3plus`,
          rule:"observed household placement excludes coverage people; coverage remains its separate unlocated block"}});
      gate("observed G3+ placement target plus unlocated coverage reconstruct complete generation counts",
        Math.abs(out.meta.lineage.generation_g3plus.population+population-G3.population)<1e-6 &&
        Math.abs(out.meta.lineage.generation_g3plus.adults+adults-G3.adults)<1e-6);
    }
    // The items' parts whose split basis (the item's splits.split_basis) is a line other than the one they edit, with
    // each generation's amount of the part (the generation account's items.split, convention a): households.py spreads
    // each part's share of its line as the basis line (splits.household_person).
    console.log("[items: the parts split by another line]");
    const basisOf = (id, name) => (corrections.meta.items.find((x) => x.id === id).meta_changed || [])
      .map((k) => corrections.meta[k] && corrections.meta[k].splits && corrections.meta[k].splits.split_basis).find((S) => S && S[name]);
    out.meta.routes = [];
    let nParts = 0, addGap = 0;
    for (const it of SUM.items.split.a) for (const x of it.edits) for (const p of x.parts || []) {
      if (p.rule !== "parent_line") continue;
      const S = basisOf(it.id, p.name);
      if (!S || S[p.name] !== p.parent) {
        throw new Error(`[BLOCKED] ${it.id} ${p.name}: the generation account split it by ${p.parent}, the payload's split_basis says ${S ? S[p.name] : "nothing"}`);
      }
      nParts += 1;
      for (const a of ["personal", "shared"]) addGap = Math.max(addGap, Math.abs(GENS.reduce((s, g) => s + p.bn[g][a], 0) - p.union_bn[a]));
      if (p.parent === x.line) continue;
      for (const g of GENS) for (const end of ["low", "high"]) {
        const r = out.generations[g][end].rows.find((y) => y.side === x.side && y.id === x.line);
        const b = out.generations[g][end].rows.find((y) => y.side === "spending" && y.id === p.parent);
        if (x.side !== "spending" || !r || r.key !== x.key || !b || Math.abs(r.cost_bn - r.response * r.amount_bn) > 1e-12) {
          throw new Error(`[BLOCKED] ${it.id} ${p.name}: ${g} ${end} has no spending row ${x.line} at key ${x.key} costing its response x amount, or no basis row ${p.parent}`);
        }
      }
      out.meta.routes.push({ item: it.id, part: p.name, side: x.side, line: x.line, key: x.key, basis: p.parent, union_bn: p.union_bn, bn: p.bn });
    }
    gate(`the items' ${nParts} parts split by a basis line are split by the payload's split_basis, and their generations add to the union's part (1e-12 bn)`,
      nParts > 0 && addGap < 1e-12, `${out.meta.routes.length} on another line than their own: ${out.meta.routes.map((r) => `${r.part} (${r.line} as ${r.basis})`).join(", ")}; max |diff| ${addGap.toExponential(1)}`);
  }
  gate("the payload's OASDI lines are candidate v4's", JSON.stringify(PA.oasdi_lines) === JSON.stringify(V.OASDI_LINES), PA.oasdi_lines.join(", "));
  out.meta.pension_accrual = { ratio_net: PA.ratio_net, part_a_share: PA.part_a_share, se_oasdi_share: PA.se_oasdi_share,
    part_a_accrual_bn: PA.part_a_accrual_bn, benefit_tax_receipt_bn: PA.benefit_tax_receipt_bn, oasdi_lines: PA.oasdi_lines,
    hi_lines: V.HI_LINES, se_line: PA.se_line };
  out.meta.roads = { highway_national_bn: V.HWY_N, passenger_share: V.FP, gasoline_bn: V.GAS, reference_scenario: V.REF };

  // The cash set at the same specifications: the pension switch's parts.
  console.log("[cash set: the pension switch's parts]");
  const cashPayload = read(path.join(FISCAL, C.cash.payload));
  const PC = C.cash.package ? P[C.cash.package] : P.forPayload(cashPayload);
  if (C.cash.package) {
    gate(`the package's cash set (${C.cash.package}) has the cash payload, exactly`, JSON.stringify(PC.correctionsPayload()) === JSON.stringify(cashPayload));
  }
  const uCash = [lo, hi].map((i) => unionCost(PC, PC.payloadModel(), MAIN_SPECS[i]));
  if (C.live) gate(`the ${ALLOCATION} cash set's ends match the case summary`,
    JSON.stringify([lo, hi]) === JSON.stringify(C.shared ? sharedEnds("cash") : endsOf("cash")));
  gate("the cash set's union reproduces its band at the same specifications (1e-4)",
    Math.abs(uCash[0] - C.cash.band[0]) < 1e-4 && Math.abs(uCash[1] - C.cash.band[1]) < 1e-4, `${uCash[0].toFixed(7)} / ${uCash[1].toFixed(7)}`);
  if (FULL) {
    const band = C.shared ? sharedBand("cash") : FULL.cash_set.band_bn;
    gate(`the cash set's union is its full-precision band (${C.lane}/derived/summary.json cash_set.band_bn, 1e-6)`,
      Math.abs(uCash[0] - band[0]) < 1e-6 && Math.abs(uCash[1] - band[1]) < 1e-6,
      `${uCash[0].toFixed(6)} / ${uCash[1].toFixed(6)} against ${band.map((v) => v.toFixed(6)).join(" / ")}`);
  }
  out.meta.cash_set = { payload: C.cash.payload, cost_bn: { low: uCash[0], high: uCash[1] } };
  const payCash = read(path.join(GEN, C.cash.genCorrections)).payloads.a;
  apiPayloads.set(PC, payCash);
  const cashResults = resultsOf(C.cash.genResults);
  const PENSION = new Set(["receipt|federal_income_tax", "spending|social_security", "spending|medicare"]);
  const tot = { accrual: [0, 0], part_a: [0, 0], benefit_tax: [0, 0] };
  const cashSum = [0, 0];
  const cashExport = C.v8 ? JSON.parse(JSON.stringify(out)) : null;
  if (cashExport) {
    cashExport.meta.basis = "cash";
    cashExport.meta.union_completion = cashPayload.meta.union_completion;
    cashExport.meta.coverage = cashPayload.meta.coverage || null;
    cashExport.meta.mixed_unit_removal = cashPayload.meta.mixed_unit_removal;
    const lineage = read(path.join(FISCAL,C.lane,"derived/lineage_addition.json")).v8;
    cashExport.meta.coverage_added_cost_bn = Object.fromEntries(["low","high"].map((end,i)=>[end,lineage.cash.all_nonreporting_descendants.cost_bn[i]]));
    cashExport.meta.coverage_added_cost_source = `${C.lane}/derived/lineage_addition.json v8.cash.all_nonreporting_descendants.cost_bn`;
    cashExport.meta.child_pricing = childPricing(PC, cashPayload);
    for (const record of out.meta.child_pricing?.records || []) {
      const cashRecord=cashExport.meta.child_pricing.records.find(r=>r.PH_SEQ===record.PH_SEQ&&r.PPPOS===record.PPPOS);
      for(const end of ["low","high"]) {
        const setMed=record.ends[end].rows.find(r=>r.side==="spending"&&r.id==="medicare");
        const cashMed=cashRecord.ends[end].rows.find(r=>r.side==="spending"&&r.id==="medicare");
        record.ends[end].part_a_accrual_cost_bn=setMed.cost_bn-(1-corrections.meta.pension_accrual.part_a_share)*cashMed.cost_bn;
      }
    }
    for (const [end,i] of [["low",lo],["high",hi]]) cashExport.union[end] = dump(PC.payloadModel(), MAIN_SPECS[i], PC);
  }
  for (const g of GENS) {
    const mc = Engine.applyCorrections(models[g].m0, payCash[g]);
    for (const [j, [end, i]] of [["low", lo], ["high", hi]].entries()) {
      const fc = PC.evaluateFull(mc, MAIN_SPECS[i], PROFILE);
      const cashDump = dump(mc, MAIN_SPECS[i], PC, g);
      if(C.v8 && payCash[g].meta.added_state_price_routing) cashDump.added_state_prices=statePriceParts(payCash[g],g,cashDump);
      cashSum[j] += cashDump.cost_bn;
      if (cashExport) cashExport.generations[g][end] = cashDump;
      if (cashExport && g === "G3plus" && payCash[g].meta.union_completion.production_delta) {
        cashDump.before_native_children = dump(withoutChildren(mc,payCash[g],cashPayload),MAIN_SPECS[i],PC,g);
      }
      const setRows = out.generations[g][end].rows;
      const cashRows = fc.evaluation.receipts.map((r) => ["receipt", r]).concat(fc.evaluation.spending.map((r) => ["spending", r]));
      const byId = new Map(cashRows.map(([side, r]) => [`${side}|${r.id}`, r]));
      const moved = setRows.filter((r) => { const c = byId.get(`${r.side}|${r.id}`); return !c || c.key !== r.key || Math.abs(c.amount_bn - r.amount_bn) > 1e-12; })
        .map((r) => `${r.side}|${r.id}`);
      const capSame = fc.capital.components.every((c, q) => Math.abs(c.return_bn - out.generations[g][end].capital[q].cost_bn) < 1e-12);
      const prodSame = fc.evaluation.private_wtp_bn === out.generations[g][end].production.private_wtp_bn
        && fc.evaluation.induced_receipts_bn === out.generations[g][end].production.induced_receipts_bn;
      gate(`${g} ${end}: the set and the cash set differ only in the three pension lines`,
        moved.filter(k => !C.v8 || !k.startsWith("spending|union_completion_")).length === 3
          && moved.every((k) => PENSION.has(k) || (C.v8 && k.startsWith("spending|union_completion_")))
          && capSame && prodSame && byId.size === setRows.length,
        moved.join(", "));
      const publishedCash = C.shared ? dump(mc, P.MAIN_SPECS[endsOf("cash")[j]], PC, g, true).cost_bn : cashDump.cost_bn;
      gate(`${g} ${end}: the cash model at the published ends matches ${C.cash.genResults} (1e-6 bn)`,
        Math.abs(publishedCash - cashResults[`${g}|${end}`]) < 1e-6, `${publishedCash.toFixed(6)} vs ${cashResults[`${g}|${end}`]}`);
      const setOf = (side, id) => setRows.find((r) => r.side === side && r.id === id);
      const ss = setOf("spending", "social_security"), med = setOf("spending", "medicare"), fit = setOf("receipt", "federal_income_tax");
      const medCash = byId.get("spending|medicare").amount_bn, fitCash = byId.get("receipt|federal_income_tax").amount_bn;
      const pension = { accrual_bn: ss.amount_bn, medicare_benefits_bn: (1 - PA.part_a_share) * medCash,
        part_a_accrual_bn: med.amount_bn - (1 - PA.part_a_share) * medCash, fit_cash_bn: fitCash, benefit_tax_bn: fitCash - fit.amount_bn,
        keys: { social_security: ss.key, medicare: med.key, federal_income_tax: fit.key } };
      out.generations[g][end].pension = pension;
      if (out.generations[g][end].before_native_children) {
        const sr=out.generations[g][end].before_native_children.rows, cr=cashDump.before_native_children.rows;
        const r=(rows,side,id)=>rows.find(r=>r.side===side&&r.id===id).amount_bn;
        const mc=r(cr,"spending","medicare"),fitc=r(cr,"receipt","federal_income_tax");
        out.generations[g][end].before_native_children.pension={...pension,accrual_bn:r(sr,"spending","social_security"),
          medicare_benefits_bn:(1-PA.part_a_share)*mc,part_a_accrual_bn:r(sr,"spending","medicare")-(1-PA.part_a_share)*mc,
          fit_cash_bn:fitc,benefit_tax_bn:fitc-r(sr,"receipt","federal_income_tax")};
        cashDump.before_native_children.pension=out.generations[g][end].before_native_children.pension;
      }
      tot.accrual[j] += pension.accrual_bn;
      tot.part_a[j] += pension.part_a_accrual_bn;
      tot.benefit_tax[j] += pension.benefit_tax_bn;
    }
  }
  for (const [j, end] of ["low", "high"].entries()) {
    const a = ALLOC[end];
    const rows = out.union[end].rows;
    const amt = (id) => rows.find((r) => r.side === "receipt" && r.id === id).amount_bn;
    const oasdi = PA.oasdi_lines.reduce((s, id) => s + amt(id), 0) + PA.se_oasdi_share * amt(PA.se_line);
    gate(`${end}: the three generations' cash sets add to the union's (1e-9 bn)`, Math.abs(cashSum[j] - uCash[j]) < 1e-9, `${cashSum[j].toFixed(6)}`);
    if (!C.lineage) {
      gate(`${end}: the generations' accruals add to ratio_net x the union's OASDI receipts (1e-9 bn)`,
        Math.abs(tot.accrual[j] - PA.ratio_net * oasdi) < 1e-9, `${tot.accrual[j].toFixed(6)} vs ${(PA.ratio_net * oasdi).toFixed(6)}`);
      gate(`${end}: the generations' Part A accruals add to part_a_accrual_bn (1e-9 bn)`, Math.abs(tot.part_a[j] - PA.part_a_accrual_bn) < 1e-9,
        `${tot.part_a[j].toFixed(6)}`);
      gate(`${end}: the generations' tax on benefits adds to benefit_tax_receipt_bn.${a} (1e-9 bn)`,
        Math.abs(tot.benefit_tax[j] - PA.benefit_tax_receipt_bn[a]) < 1e-9, `${tot.benefit_tax[j].toFixed(6)}`);
      continue;
    }
    // oct05: the payload's pension figures are the September 29 union's. The lineage adds its own parts, priced on the
    // G3+ and white cells (the whites' accrual per OASDI dollar is not ratio_net). Gates: the generations' parts add to
    // the union's, read on the union's set and cash models the same way; the union's less the lineage's own (its edits
    // on the evaluated keys) are the payload's figures (1e-9 bn).
    const spec = MAIN_SPECS[[lo, hi][j]];
    const ue = P.evaluateFull(unionModel, spec, PROFILE).evaluation, uc = PC.evaluateFull(PC.payloadModel(), spec, PROFILE).evaluation;
    const row = (ev, side, id) => ev[side === "receipt" ? "receipts" : "spending"].find((r) => r.id === id);
    const sc = P.stateFor(unionModel, spec, PROFILE).receipt_scenario;
    const lin = (edits, side, id, key) => edits.filter((e) => e.side === side && e.line === id && (side === "receipt" ? e.scenario === key : e.key === key))
      .reduce((s, e) => s + e.by[a], 0);
    const union = { accrual: row(ue, "spending", "social_security").amount_bn,
      part_a: row(ue, "spending", "medicare").amount_bn - (1 - PA.part_a_share) * row(uc, "spending", "medicare").amount_bn,
      benefit_tax: row(uc, "receipt", "federal_income_tax").amount_bn - row(ue, "receipt", "federal_income_tax").amount_bn };
    const LS = P.LINEAGE_EDITS, LC = PC.LINEAGE_EDITS;
    let linOasdi = PA.oasdi_lines.reduce((s, id) => s + lin(LS, "receipt", id, sc), 0) + PA.se_oasdi_share * lin(LS, "receipt", PA.se_line, sc);
    const own = { accrual: lin(LS, "spending", "social_security", row(ue, "spending", "social_security").key),
      part_a: lin(LS, "spending", "medicare", row(ue, "spending", "medicare").key) - (1 - PA.part_a_share) * lin(LC, "spending", "medicare", row(uc, "spending", "medicare").key),
      benefit_tax: lin(LC, "receipt", "federal_income_tax", sc) - lin(LS, "receipt", "federal_income_tax", sc) };
    if (C.v8 && out.generations.G3plus[end].before_native_children) {
      const set = out.generations.G3plus[end], cash = cashExport.generations.G3plus[end];
      const delta = (d,side,id) => d.rows.find(r=>r.side===side&&r.id===id).amount_bn-d.before_native_children.rows.find(r=>r.side===side&&r.id===id).amount_bn;
      linOasdi += PA.oasdi_lines.reduce((s,id)=>s+delta(set,"receipt",id),0)+PA.se_oasdi_share*delta(set,"receipt",PA.se_line);
      own.accrual += delta(set,"spending","social_security");
      own.part_a += delta(set,"spending","medicare")-(1-PA.part_a_share)*delta(cash,"spending","medicare");
      own.benefit_tax += delta(cash,"receipt","federal_income_tax")-delta(set,"receipt","federal_income_tax");
      console.log(`[native pension ${end}]`,JSON.stringify({native_ss:delta(set,"spending","social_security"),native_med:delta(set,"spending","medicare"),native_cash_med:delta(cash,"spending","medicare"),native_set_fit:delta(set,"receipt","federal_income_tax"),native_cash_fit:delta(cash,"receipt","federal_income_tax"),native_oasdi:PA.oasdi_lines.reduce((s,id)=>s+delta(set,"receipt",id),0)+PA.se_oasdi_share*delta(set,"receipt",PA.se_line)}));
    }
    // oct07: the edit sets' parts that the generation account puts on the added people (its rule lineage, all on G3+)
    // are the lineage's own too; the payload's ratio_net and Part A accrual (v6's) price the rest.
    const items = { accrual: 0, part_a: 0, benefit_tax: 0 };
    const row4Union = { accrual: 0, part_a: 0, benefit_tax: 0 };
    // R8 changes FIT in both sets, by different amounts. Their difference is part of the lineage's benefit-tax
    // difference; read the actual set/cash item parts at this receipt scenario, not the inherited PA metadata.
    const itemLineageFit = (payload, id) => {
      const it = payload.meta.items.find((r) => r.id === id && r.applied);
      if (!it) return 0;
      return Object.entries(it.parts || {}).filter(([name, p]) => {
        const e = payload.edits[it.edits.first + p.edit];
        return name.startsWith("lineage_") && e.side === "receipt" && e.line === "federal_income_tax" && e.scenario === sc;
      }).reduce((s, [, p]) => s + p.by[a], 0);
    };
    if (C.live) {
      const whiteBenefitTax = itemLineageFit(cashPayload, "white_end_tax_keys") - itemLineageFit(corrections, "white_end_tax_keys");
      own.benefit_tax += whiteBenefitTax;
      items.benefit_tax += whiteBenefitTax;
    }
    if (C.items) {
      for (const it of SUM.items.split.a) for (const x of it.edits) for (const p of x.parts || []) {
        const r = row(ue, x.side, x.line);
        const active = r && (x.side === "receipt" ? x.scenario === sc : x.key === r.key);
        const pensionComponent = x.side === "spending" ? { social_security: "accrual", medicare: "part_a" }[x.line]
          : x.line === "federal_income_tax" ? "benefit_tax" : null;
        // R9: subtract its union pension parts before checking the inherited published-weight PA oracle.
        // The added-people parts are already subtracted as lineage own amounts below.
        if (C.live && it.id === "row4_frame" && p.name.startsWith("union_") && active && pensionComponent) {
          row4Union[pensionComponent] += (x.side === "receipt" ? -1 : 1) * p.union_bn[a];
        }
        if (p.rule !== "lineage" && !(C.v8 && p.rule === "declared" && ["g3", "white"].includes(p.route?.kind))) continue;
        // R7 receipt shifts and R6's added-people credit parts already sit on G3+'s evaluated lines.
        // They take those lines' household split; they never enter the pension subtraction below.
        const jobReceipt = ["job_capital_taxes", "foreign_source_tax"].includes(it.id) && x.side === "receipt"
          && ["corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes"].includes(x.line)
          && /^(lineage_g3plus|lineage_whites):/.test(p.name);
        const creditPart = it.id === "child_credits" && /^lineage_g3plus:/.test(p.name)
          && ((x.side === "receipt" && x.line === "federal_income_tax")
            || (x.side === "spending" && x.line === "refundable_tax_credits"));
        const whiteFit = it.id === "white_end_tax_keys" && /^lineage_whites:income_tax_keys:federal_income_tax:/.test(p.name)
          && x.side === "receipt" && x.line === "federal_income_tax";
        const component = p.name.split(":")[1];
        const row4Part = it.id === "row4_frame" && /^(lineage_g3plus|lineage_whites):/.test(p.name)
          && ((x.side === "receipt" && component === "benefit_tax" && x.line === "federal_income_tax")
            || (x.side === "receipt" && component === "owner_national_key" && x.line === "modeled_owner_property")
            || (component === "state_index" && ((x.side === "receipt" && ["general_sales_tax", "personal_motor_vehicle"].includes(x.line))
              || (x.side === "spending" && ["state_price_public_order_safety", "state_price_health_services", "state_price_recreation_culture"].includes(x.line)))));
        const completionPart = C.v8 && it.id === "union_completion"
          && /^lineage_g3plus:observed_nonreporters:(receipt|spending):/.test(p.name);
        if (C.live && (jobReceipt || creditPart || whiteFit || row4Part || completionPart)) {
          if (!r || !GENS.every((g) => Math.abs(p.bn[g][a] - (g === "G3plus" ? p.union_bn[a] : 0)) < 1e-12)) {
            throw new Error(`[BLOCKED] ${it.id} ${p.name}: its lineage part is not wholly on G3+`);
          }
          if (active && it.id === "row4_frame" && pensionComponent === "benefit_tax") {
            own.benefit_tax -= p.union_bn[a];
            items.benefit_tax -= p.union_bn[a];
          }
          if (active) {
            out.meta.lineage.non_pension_parts = out.meta.lineage.non_pension_parts || {};
            (out.meta.lineage.non_pension_parts[end] = out.meta.lineage.non_pension_parts[end] || [])
              .push({ item: it.id, part: p.name, side: x.side, line: x.line, amount_bn: p.union_bn[a], rule: "G3plus own-line household split" });
          }
          continue;
        }
        const k = x.side === "spending" ? { social_security: "accrual", medicare: "part_a" }[x.line] : undefined;
        const row4Pension = it.id !== "row4_frame" || (x.line === "social_security" && ["ss_split", "ss_factor"].includes(component))
          || (x.line === "medicare" && component === "part_a_split");
        if (!k || !row4Pension || x.key !== row(ue, "spending", x.line).key) {
          throw new Error(`[BLOCKED] ${it.id} ${p.name}: a part on the added people on ${x.side} ${x.line} (${x.key}), which the pension gates do not count`);
        }
        items[k] += p.union_bn[a];
        own[k] += p.union_bn[a];
      }
    }
    const want = { accrual: PA.ratio_net * (oasdi - linOasdi), part_a: PA.part_a_accrual_bn, benefit_tax: PA.benefit_tax_receipt_bn[a] };
    for (const k of ["accrual", "part_a", "benefit_tax"]) {
      gate(`${end}: the generations' ${k} adds to the union's (its set and cash models, 1e-9 bn)`, Math.abs(tot[k][j] - union[k]) < 1e-9,
        `${tot[k][j].toFixed(6)} vs ${union[k].toFixed(6)}`);
      gate(`${end}: the union's ${k} less the lineage's own (${own[k].toFixed(6)}${C.items ? `, the items' ${items[k].toFixed(6)} in it` : ""}) is the `
        + `${C.items ? "payload's" : "September 29 payload's"}${C.live ? ", after taking out R9's union part" : ""} (1e-9 bn)`,
        Math.abs(union[k] - own[k] - row4Union[k] - want[k]) < 1e-9,
        `${(union[k] - own[k]).toFixed(6)} less R9 union ${row4Union[k].toFixed(6)} vs ${want[k].toFixed(6)}`);
    }
    if (C.live) {
      out.meta.pension_accrual.row4_union_bn = out.meta.pension_accrual.row4_union_bn || {};
      out.meta.pension_accrual.row4_union_bn[end] = row4Union;
    }
    out.meta.lineage.pension_bn = Object.assign(out.meta.lineage.pension_bn || {},
      { [end]: Object.assign({ oasdi_receipts_bn: linOasdi }, own, C.items ? { items_bn: items } : {}) });
  }
  if (cashExport) {
    // Copy the metadata computed by pension/road gates, then retain cash method's own payload blocks.
    cashExport.meta.lineage = JSON.parse(JSON.stringify(out.meta.lineage));
    cashExport.meta.pension_accrual = JSON.parse(JSON.stringify(out.meta.pension_accrual));
    cashExport.meta.roads = out.meta.roads;
    cashExport.meta.routes = out.meta.routes;
    for (const g of GENS) for (const end of ["low", "high"]) {
      cashExport.generations[g][end].pension = out.generations[g][end].pension;
    }
    out.meta.cash_export = cashExport;
  }

  // Roads: each generation's road line in its three pieces, with the driver-mile share from the generation account.
  console.log("[road lines: driver-mile, freight and old-key pieces]");
  const EXCISE = "excise_selective_sales", EA = "economic_affairs_services";
  // oct05: the summary carries no road parameters; s_vmt is solved from the model's state-local road line and excise
  // cell (road = N (FP s + (1 - FP) k - k_old), excise = k (X - GAS) + GAS s), and the federal line's gate below checks it.
  const SUM29 = C.lineage ? read(path.join(GEN, CASES.sept29.summary)) : null;
  function solvedSvmt(m1, a) {
    const ea = m1.spending.lines.find((l) => l.id === EA), ex = m1.receipts.lines.find((l) => l.id === EXCISE);
    const road = m1.spending.lines.find((l) => l.id === "roads_vmt_sl").keys.k[a].target_bn;
    const kOld = ea.keys[ea.preferred_key][a].target_bn / ea.national_bn, X = ex.national_bn, E = ex.cells[V.REF][a].target_bn;
    return (road / V.HWY_N.sl + kOld - (1 - V.FP) * E / (X - V.GAS)) / (V.FP - (1 - V.FP) * V.GAS / (X - V.GAS));
  }
  if (C.lineage) {
    for (const g of GENS.filter((x) => x !== "G3plus")) for (const a of ["personal", "shared"]) {
      const s = solvedSvmt(models[g].m1, a), want = SUM29.rules.parameters.a[g].s_vmt[a];
      gate(`${g} ${a}: s_vmt solved from the model is the September 29 summary's (1e-9; the lineage leaves ${g} alone)`,
        Math.abs(s - want) < 1e-9, `${s.toFixed(12)} vs ${want.toFixed(12)}`);
    }
    out.meta.lineage.s_vmt_g3plus = Object.fromEntries(["personal", "shared"].map((a) => [a, solvedSvmt(models.G3plus.m1, a)]));
    out.meta.lineage.s_vmt_g3plus_sept29 = SUM29.rules.parameters.a.G3plus.s_vmt;
  }
  for (const g of GENS) {
    const m1 = models[g].m1;
    const ea = m1.spending.lines.find((l) => l.id === EA), ex = m1.receipts.lines.find((l) => l.id === EXCISE);
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      const a = MAIN_SPECS[i].allocation;
      const svmt = C.lineage ? solvedSvmt(m1, a) : SUM.rules.parameters.a[g].s_vmt[a];
      const kOld = ea.keys[ea.preferred_key][a].target_bn / ea.national_bn;
      // The final excise cell carries the gasoline shift GAS (s_vmt - k_cons) on the pre-roads cell k_cons x national.
      const kCons = (ex.cells[V.REF][a].target_bn - V.GAS * svmt) / (ex.national_bn - V.GAS);
      const rows = out.generations[g][end].rows;
      const eaRow = rows.find((r) => r.side === "spending" && r.id === EA);
      const roads = {};
      for (const [lvl, id] of [["sl", "roads_vmt_sl"], ["fed", "roads_vmt_fed"]]) {
        const r = rows.find((x) => x.side === "spending" && x.id === id);
        const N = V.HWY_N[lvl];
        const pieces = { driver_miles_bn: N * V.FP * svmt, old_key_bn: -N * kOld };
        pieces.freight_bn = r.amount_bn - pieces.driver_miles_bn - pieces.old_key_bn;
        const implied = pieces.freight_bn / (N * (1 - V.FP));
        gate(`${g} ${end} ${id}: the freight piece's key is the generation's excise share before the gasoline shift (1e-9)`,
          Math.abs(implied - kCons) < 1e-9, `${implied.toFixed(12)} vs ${kCons.toFixed(12)}`);
        roads[id] = Object.assign(pieces, { freight_key: ex.cells[V.REF][a].key || null, old_key: ea.preferred_key, s_vmt: svmt });
      }
      gate(`${g} ${end}: economic_affairs_services is evaluated at its preferred key`, eaRow.key === ea.preferred_key, `${eaRow.key}`);
      out.generations[g][end].roads = roads;
    }
  }
  if (C.v8 && out.generations.G3plus.low.before_native_children) {
    const m1=withoutChildren(models.G3plus.m1,pay.G3plus);
    for(const [end,i] of [["low",lo],["high",hi]]) {
      const before=out.generations.G3plus[end].before_native_children,a=MAIN_SPECS[i].allocation;
      const svmt=solvedSvmt(m1,a),ea=m1.spending.lines.find(l=>l.id===EA),ex=m1.receipts.lines.find(l=>l.id===EXCISE);
      const kOld=ea.keys[ea.preferred_key][a].target_bn/ea.national_bn;
      before.roads={};
      for(const [lvl,id] of [["sl","roads_vmt_sl"],["fed","roads_vmt_fed"]]) {
        const row=before.rows.find(r=>r.id===id),N=V.HWY_N[lvl],driver=N*V.FP*svmt,old=-N*kOld;
        before.roads[id]={driver_miles_bn:driver,old_key_bn:old,freight_bn:row.amount_bn-driver-old,
          freight_key:ex.cells[V.REF][a].key||null,old_key:ea.preferred_key,s_vmt:svmt};
      }
      out.meta.cash_export.generations.G3plus[end].before_native_children.roads=before.roads;
    }
  }
}
if (fails) { console.log(`✗ ${fails} gate(s) failed`); process.exit(1); }
if (C.v8) {
  for (const [basis, api, payloads] of [["set", P, pay], ["cash", P.CASH, apiPayloads.get(P.CASH)]]) {
    let gap = 0;
    for (const spec of MAIN_SPECS.filter(s=>s.allocation===ALLOCATION)) {
      const total = GENS.reduce((sum,g)=>sum+dump(Engine.applyCorrections(models[g].m0,payloads[g]),spec,api,g).cost_bn,0);
      gap = Math.max(gap,Math.abs(total-dump(api.payloadModel(),spec,api).cost_bn));
    }
    gate(`${basis}: all 32 specification generation splits add to the case (1e-9 bn)`,gap<1e-9,`max |gap| ${gap.toExponential(1)}`);
  }
  if (fails) process.exit(1);
}
if(C.v8) {
  addedStateTargetMetadata(out);
  addedStateTargetMetadata(out.meta.cash_export);
  childCostMetadata(out);
  childCostMetadata(out.meta.cash_export);
  if(fails) process.exit(1);
}
function atomicWrite(file,data){const temporary=`${file}.tmp-${process.pid}`;try{fs.writeFileSync(temporary,data);fs.renameSync(temporary,file);}finally{if(fs.existsSync(temporary))fs.unlinkSync(temporary);}}
if (REQUESTED_CASE === "oct16") {
  const cashExport = out.meta.cash_export;
  for (const g of GENS) for (const end of ["low","high"]) cashExport.generations[g][end].roads = out.generations[g][end].roads;
  delete out.meta.cash_export;
  require("./export_oct16.cjs").write({set:out,cash:cashExport,allocation:ALLOCATION,atomicWrite});
  process.exit(0);
}
fs.mkdirSync(path.dirname(path.join(HERE, "_cache", C.out)), { recursive: true });
if (C.v8) {
  const cashExport = out.meta.cash_export;
  for (const g of GENS) for (const end of ["low","high"]) cashExport.generations[g][end].roads = out.generations[g][end].roads;
  delete out.meta.cash_export;
  atomicWrite(path.join(HERE, "_cache", C.out), JSON.stringify(out, null, 1) + "\n");
  atomicWrite(path.join(HERE, "_cache", C.out.replace("lines.json", "lines_cash.json")), JSON.stringify(cashExport, null, 1) + "\n");
} else atomicWrite(path.join(HERE, "_cache", C.out), JSON.stringify(out, null, 1) + "\n");
console.log("  ✓ all export gates passed");
