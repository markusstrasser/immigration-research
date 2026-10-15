/* Preserve v7's lineage_addition schema as explicitly marked history; add v8 counts, current costs and a
 * decomposition by original descendants, newly observed nonreporters and the reporting union. Custom-count
 * cases follow v7's own lineage_count/rebase/item route, then this lane's forItems8 layer. No old lane is written.
 * The reporting-union intercept holds the adopted mixed-unit term and coverage construction, and does not
 * claim a new survey run or a fresh response calibration for the completed union. */
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const P = require("./package.cjs"), V8 = P.V8_PACKAGE, V7 = P.V7_PACKAGE, B = P.OCT05;
const { removeObservedChildren } = require("./sign_reversal.cjs");
const { Engine, MODEL, METHODS } = P, POP = B.POP;
const TOOLS = { OCT05: B, Engine, MODEL, METHODS, readJson: B.readJson, sha256: B.sha256 };
const clone = x => JSON.parse(JSON.stringify(x)), mean = xs => xs.reduce((a, b) => a + b, 0) / xs.length;
const sub = (a, b) => a.map((v, i) => v - b[i]);
const worst = xs => Math.max(0, ...xs.map(Math.abs));
const per = (cost, persons) => cost.map(x => x * 1e9 / persons);
const oldFile = path.join(__dirname, "../main_case_2026_10_15/derived/lineage_addition.json");
const old = JSON.parse(fs.readFileSync(oldFile, "utf8"));
const sha = file => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const GATES = [];
function gate(name, pass, detail = "") { GATES.push({ name, pass: !!pass, detail }); console.log(`  ${pass ? "PASS" : "FAIL"} ${name}${detail ? `: ${detail}` : ""}`); }
const argv = process.argv.slice(2), flag = k => argv.includes(k) ? argv[argv.indexOf(k) + 1] : null;
const OUT = path.resolve(flag("--out") || path.join(__dirname, "derived/lineage_addition.json"));
if (!OUT.startsWith(__dirname + path.sep)) throw Error("[BLOCKED] lineage output must stay in v8's lane");
const payload = P.correctionsPayload(), coverage = payload.meta.coverage || null, completion = payload.meta.union_completion;
if (coverage?.stub) console.log("[STUB] lineage_addition uses temporary coverage prices");
const AB = POP.arms[POP.meta.central_arm];
const V6_IDS = new Set(V7.V6_PACKAGE.REGISTRY.map(x => x.id));
const v6Items = V7.REGISTRY.filter(x => V6_IDS.has(x.id));
const newer = V8.REGISTRY.filter(x => V8.NEW_IDS.includes(x.id) && P.CANDIDATE.includes(x.id));
const at = { case: { s: AB.s, k_metro: AB.k_metro }, union: { s: POP.meta.s_v4, k_metro: 1 } };
function option(where, name, later, g3) {
  const id = `${where}_${name}`, Bx = Object.create(B);
  const A = { ...clone(AB), source_arm: `${AB.source_arm}, v8 decomposition ${id}`, later, g3_rate: g3, added: later + g3,
    population: POP.meta.account_union + later + g3, added_cps: null, ...at[where] };
  Bx.POP = { ...POP, arms: { ...POP.arms, [id]: A } };
  const c3 = clone(POP.c3), additions = V8.COUNT.additionsAt(Bx, id, c3, TOOLS);
  for (const w of ["set", "cash"]) {
    const add = additions[w], n5 = B.ADDITION[w].edits.length;
    if (add.edits.length === n5 - 1 && add.meta.lineage.row8_edit_bn === 0) add.edits.push({ side: "spending", line: "lane_constants", key: "k", by: { personal: 0, shared: 0 } });
    if (add.edits.length !== n5) throw Error(`[BLOCKED] ${id} lineage edit frame differs from v5`);
    add.meta.source = "main_case_2026_10_16/lineage_addition.cjs";
    add.meta.status = `v9 decomposition variant ${id}, not adopted`;
  }
  const L = additions.set.meta.lineage;
  const meta = { name: id, label: id, arm: id, source_arm: A.source_arm, added: A.added, g3_rate: A.g3_rate, later: A.later,
    population: A.population, c3: c3.value, s: L.s, k_metro: L.k_metro, row8_edit_bn: L.row8_edit_bn, m_g3plus: L.m_g3plus,
    m_white: L.m_white, module: "main_case_2026_10_16/lineage_addition.cjs" };
  return { name: id, label: id, arm: id, A, C3: c3.value, c3, m_g3plus: L.m_g3plus, m_white: L.m_white, additions, meta };
}
function caseAt(opt) {
  const lin = v6Items.find(it => it.kind === "lineage");
  const linBuilt = P.checkLineage(lin, lin.build({ B, LINEAGE_OPTION: opt, ...TOOLS }, null), B, opt.additions);
  linBuilt.option = opt;
  const L = P.rebase(B, linBuilt), ctx6 = { B: L, LINEAGE_ITEM: lin.id, ...TOOLS };
  const built = v6Items.map(item => item.kind === "lineage" ? { item, arm: null, lineage: linBuilt }
    : { item, arm: null, set: P.checkBuilt(item, item.build(ctx6, null, "set"), L, "set"),
      cash: item.cash.applies ? P.checkBuilt(item, item.build(ctx6, null, "cash"), L.CASH, "cash") : null });
  const detail = Object.fromEntries(built.map(b => [b.item.id, b.item.kind === "lineage" ? b.lineage.detail : { set: b.set.detail, cash: b.cash ? b.cash.detail : null }]));
  const set6 = P.forItems(L, built, "set", false, opt), cash6 = P.forItems(L.CASH, built, "cash", false, opt);
  const Q6 = Object.assign(set6, { CASH: cash6, CASH_PAYLOAD: cash6.correctionsPayload(), OCT05: B, OCT05_CASH: B.CASH, ITEM_BASE: L,
    ITEM_IDS: built.map(b => b.item.id), ITEM_ARMS: {}, LINEAGE_ITEM: lin.id, ITEM_DETAIL: detail, LINEAGE_OPTION: opt.name, LINEAGE_OPTION_META: clone(opt.meta) });
  const Q7 = V7.caseOn(Q6, V7.NEW_IDS, {}, "variant", opt.name);
  const ctx = { B: Q7, DETAIL: Q7.ITEM_DETAIL, Engine, MODEL, METHODS, readJson: P.readJson, sha256: P.sha256 };
  const added = w => newer.map(item => ({ item, arm: null, x: item.build(ctx, null, w) }));
  const set8=V8.forItems8(Q7, added("set"), "set", { stamp: "variant" }),cash8=V8.forItems8(Q7.CASH, added("cash"), "cash", { stamp: "variant" });
  const Q8=Object.assign(set8,{CASH:cash8});
  const Q9=P.caseOn9(Q8,P.NEW_IDS.filter(id=>P.CANDIDATE.includes(id)),{},"variant",opt.name);
  return {set:Q9,cash:Q9.CASH};
}
function endCosts(pkg, ends) {
  const models = METHODS.map(method => pkg.modelFor("central", method, pkg.withCentral({})));
  return ends.map(index => mean(models.map(model => pkg.evaluateFull(model, pkg.MAIN_SPECS[index], P.MAIN_PROFILE).cost_bn)));
}
function endsOf(pkg) {
  const per = METHODS.map(method => {
    const model = pkg.modelFor("central", method, pkg.withCentral({}));
    return pkg.MAIN_SPECS.map(spec => pkg.evaluateFull(model, spec, P.MAIN_PROFILE).cost_bn);
  });
  const indices = per.map(row => [row.indexOf(Math.min(...row)), row.indexOf(Math.max(...row))]);
  if (!indices.every(row => JSON.stringify(row) === JSON.stringify(indices[0]))) throw Error("[BLOCKED] lineage methods have different endpoints");
  return indices[0];
}
const ENDS = { set: endsOf(P), cash: endsOf(P.CASH) };
const prices = pair => Object.fromEntries(["set", "cash"].map(w => [w, endCosts(pair[w], ENDS[w])]));
const whole = prices({ set: P, cash: P.CASH }), opts = {};
if(argv.includes("--probe-central")){
  const rebuilt=caseAt(option("case","both",AB.later,AB.g3_rate));
  for(const w of ["set","cash"]){
    const current=w==="set"?P:P.CASH,variant=rebuilt[w];
    const got=endCosts(variant,ENDS[w]);
    gate(`${w} custom canonical counts preserve current case`,worst(sub(got,whole[w]))<1e-9,JSON.stringify({current:whole[w],rebuilt:got}));
    if(worst(sub(got,whole[w]))>=1e-9){
      for(const i of ENDS[w]){
        const spec=current.MAIN_SPECS[i],a=current.evaluateFull(current.payloadModel(),spec),b=variant.evaluateFull(variant.payloadModel(),spec);
        console.log(JSON.stringify({which:w,specification:i,payload_model_gap_bn:b.cost_bn-a.cost_bn,current_post:a.v9_post_engine.amounts,variant_post:b.v9_post_engine.amounts}));
      }
    }
  }
  console.log(`[resources] process.resourceUsage().maxRSS=${process.resourceUsage().maxRSS} KiB`);
  process.exit(GATES.some(g=>!g.pass)?1:0);
}
for (const where of ["case", "union"]) {
  opts[where] = {};
  const laterShare = AB.later / AB.added;
  for (const [name, later, g3] of [["later", AB.later, 0], ["g3_rate", 0, AB.g3_rate], ["both", AB.later, AB.g3_rate], ["later_twice", 2 * AB.later, 0],
    ["tiny", 1e-5 * laterShare, 1e-5 * (1 - laterShare)], ["half_tiny", 0.5e-5 * laterShare, 0.5e-5 * (1 - laterShare)]]) {
    console.log(`[decompose ${where}/${name}]`);
    opts[where][name] = prices(caseAt(option(where, name, later, g3)));
  }
}
const nonreporters = Object.fromEntries(["set", "cash"].map(w => {
  const pkg = w === "set" ? P : P.CASH, models = METHODS.map(method => pkg.modelFor("central", method, pkg.withCentral({})));
  const removals = models.map(model => removeObservedChildren(pkg, model));
  gate(`${w} observed nonreporters have native cells and production`, removals.every(removal => removal.parts.length > 0));
  const costs = ENDS[w].map(index => mean(models.map(model => {
    const removed = removals[models.indexOf(model)];
    return pkg.evaluateFull(model, pkg.MAIN_SPECS[index], P.MAIN_PROFILE).cost_bn
      - pkg.evaluateFull(removed.model, pkg.MAIN_SPECS[index], P.MAIN_PROFILE).cost_bn;
  })));
  return [w, costs];
}));
const creditsFile = path.join(__dirname, "../union_completion_2026_10_14/derived/credits_interaction.json");
const credits = JSON.parse(fs.readFileSync(creditsFile, "utf8")).results;
const nonreporterCredit = credits.one_us_parent_plus_observed.delta_bn - credits.one_us_parent.delta_bn;
const countParts = { original_reporting_union: AB.population - AB.added, completed_reporters: completion.counts.reporters,
  original_later: AB.later, original_g3_rate: AB.g3_rate, observed_nonreporter_later: completion.counts.observed_later,
  observed_nonreporter_g3_rate: completion.counts.observed_g3_rate, coverage: coverage?.net_missing_people || 0,
  native_minor_observed_change: Object.values(payload.meta.native_minor_calibration?.observed_people_change_by_generation||{}).reduce((a,b)=>a+b,0),
  native_minor_coverage_change: Object.values(payload.meta.native_minor_calibration?.coverage_people_change_by_generation||{}).reduce((a,b)=>a+b,0),
  tenure_coverage_change: Object.values(payload.meta.coverage_tenure?.coverage_people_change_by_generation||{}).reduce((a,b)=>a+b,0) };
const counts = { parts: countParts, reporting_union_without_coverage: P.POPULATION_V9.without_coverage-(AB.added+completion.counts.nonreporters),
  reporting_union: P.POPULATION_V9.with_coverage-(AB.added+completion.counts.nonreporters),
  nonreporting_descendants: AB.added + completion.counts.nonreporters, without_coverage: P.POPULATION_V9.without_coverage,
  with_coverage: P.POPULATION_V9.with_coverage, coverage_by_generation: coverage?.counts_by_generation || {} };
gate("new people parts close to both population denominators", Math.abs(counts.reporting_union_without_coverage + counts.nonreporting_descendants - counts.without_coverage) < 1e-6 && Math.abs(counts.reporting_union + counts.nonreporting_descendants - counts.with_coverage) < 1e-6);
const out = {};
for (const w of ["set", "cash"]) {
  const C = whole[w], K = opts.case, N = opts.union;
  // v5 blocks a payload with literally nobody added. Approach zero on its original later/G3 mixture, at
  // 1e-5 and half as many people. The extrapolated limit and measured convergence are reported explicitly.
  const intercept = K.half_tiny[w].map((x, i) => 2 * x - K.tiny[w][i]);
  const ownIntercept = N.half_tiny[w].map((x, i) => 2 * x - N.tiny[w][i]);
  const check = sub(K.tiny[w], K.half_tiny[w]), ownCheck = sub(N.tiny[w], N.half_tiny[w]);
  const curvature = K.both[w].map((x, i) => x - K.later[w][i] - K.g3_rate[w][i] + intercept[i]);
  const oldAffineCheck = sub(K.later[w].map((x, i) => 2 * x - K.later_twice[w][i]), K.later[w].map((x, i) => x + K.g3_rate[w][i] - K.both[w][i]));
  gate(`${w} custom both-count route equals current v9`, worst(sub(K.both[w], C)) < 1e-9, worst(sub(K.both[w], C)).toExponential(2));
  gate(`${w} zero-descendant limit converges within 1e-9bn at both response calibrations`, worst(check) < 1e-9 && worst(ownCheck) < 1e-9, `${worst(check)} / ${worst(ownCheck)}`);
  // Two-factor Shapley split assigns half the measured nonlinearity to each original descendant part.
  const later = C.map((x, i) => 0.5 * (K.later[w][i] - intercept[i] + x - K.g3_rate[w][i]));
  const g3 = C.map((x, i) => 0.5 * (K.g3_rate[w][i] - intercept[i] + x - K.later[w][i]));
  const original = later.map((x, i) => x + g3[i]);
  const newNonreporter = nonreporters[w].map(x => x + nonreporterCredit);
  const reportingAtCase = sub(intercept, newNonreporter);
  const allAdded = original.map((x, i) => x + newNonreporter[i]);
  gate(`${w} reporting union plus original and observed nonreporters closes to full v9`, worst(C.map((x, i) => x - reportingAtCase[i] - allAdded[i])) < 1e-9);
  out[w] = { case_bn: C, end_specifications: ENDS[w], per_member_usd: per(C, counts.with_coverage), per_member_without_coverage_people_usd: per(C, counts.without_coverage),
    original_descendants: { later: { persons: AB.later, cost_bn: later, per_person_usd: per(later, AB.later) }, g3_rate: { persons: AB.g3_rate, cost_bn: g3, per_person_usd: per(g3, AB.g3_rate) },
      source: "main_case_2026_10_07/lineage_count.cjs additionsAt, v7 custom-count rebase, v8 forItems8 and v9 caseOn9 with every active item rebuilt",
      added_cost_bn: original, addition_including_original_response_move_bn: sub(C, ownIntercept),
      two_factor_interaction_bn: curvature, old_affine_intercept_disagreement_bn: oldAffineCheck,
      parts_rule: "two-factor Shapley values: each original descendant part receives half its measured interaction with the other",
      zero_limit: { people: [1e-5, 0.5e-5], method: "twice half-tiny minus tiny; v5 refuses a literal zero-added payload", observed_tiny_half_tiny_change_bn: check, original_union_response_change_bn: ownCheck, tolerance_bn: 1e-9 },
      union_response_move_bn: sub(intercept, ownIntercept), intercept_at_case_responses_bn: intercept, intercept_at_original_union_responses_bn: ownIntercept,
      intercept_people_rule: "old nonreporting descendants excluded; newly observed reporters and nonreporters, coverage, and adopted mixed-unit boundary construction held" },
    observed_nonreporters: { persons: completion.counts.nonreporters, later_persons: completion.counts.observed_later, g3_rate_persons: completion.counts.observed_g3_rate,
      native_part_prefix: "lineage_g3plus:observed_nonreporters:", source: completion.source,
      native_engine_cost_bn: nonreporters[w], source_carrier_cost_bn: nonreporters[w],
      extraction_rule: "full-model cost less cost after reversing observed-nonreporter native cell parts and their P/F production arrays; public-capital change included; source_carrier_cost_bn retained as an alias of native_engine_cost_bn",
      incremental_crossing_credits_bn: nonreporterCredit, cost_bn: newNonreporter, per_person_usd: per(newNonreporter, completion.counts.nonreporters) },
    reporting_union_at_case_responses: { persons: counts.reporting_union, cost_bn: reportingAtCase, per_member_usd: per(reportingAtCase, counts.reporting_union),
      rule: "zero-original-descendant limit less observed-nonreporter native full-engine cost and their measured incremental crossing credits; coverage and adopted item11 terms held; case responses, not a freshly calibrated completed-union removal" },
    all_nonreporting_descendants: { persons: counts.nonreporting_descendants, cost_bn: allAdded, per_person_usd: per(allAdded, counts.nonreporting_descendants) },
    post_engine: Object.fromEntries(["mixed_unit_removal","coverage",...P.NEW_IDS].map(id=>[id,(w === "set" ? P : P.CASH).correctionsPayload().meta[id]||null])) };
}
if (GATES.some(g => !g.pass)) throw Error("[BLOCKED] lineage decomposition gates failed; no output written");
const result = clone(old);
Object.assign(result.meta, { history_case: "oct15", history_rule: "Every pre-existing v8 path is retained history; current v9 quantities live only in v9", current_case: "oct16" });
result.v9 = { meta: { lane: "main_case_2026_10_16", status: payload.meta.status, stub: !!coverage?.stub, counts, end_specifications: ENDS,
  evaluated_payload_json_sha256: crypto.createHash("sha256").update(JSON.stringify(payload)).digest("hex"),
  source_files: { v8_lineage_addition: { file: "main_case_2026_10_15/derived/lineage_addition.json", sha256: sha(oldFile) }, observed_nonreporter_crossing_credits: { file: "union_completion_2026_10_14/derived/credits_interaction.json", sha256: sha(creditsFile) } },
  approximation: "The completed reporting-union amount is an accounting decomposition at case responses; observed-nonreporter crossing credits use the source's one_us_parent_plus_observed minus one_us_parent measurement. Item11's adopted survivor boundary and central coverage construction stay fixed, including the documented overlap approximation. No completed-union own-response or new mixed-unit source run is claimed." },
  set: out.set, cash: out.cash, gates: GATES };
require("./memory_guard.cjs").requireWithinBudget("lineage addition");
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(result, null, 1) + "\n");
console.log(`[resources] process.resourceUsage().maxRSS=${process.resourceUsage().maxRSS} KiB`);
console.log(`[${GATES.length} gates pass] wrote ${OUT}`);
