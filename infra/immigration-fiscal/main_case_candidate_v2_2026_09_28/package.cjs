/* The next main-case candidate, revised after its attack: case sept28_candidate_v2 (BRIEF.md, 08b1b7d), not adopted.
 * It builds on the first candidate's package (../main_case_candidate_2026_09_28/package.cjs, c313b53), imported
 * unchanged, which imports the September 27 case unchanged. Every item is an option, so each can be taken alone:
 *
 *   1. housing: "tenants". Public housing's enterprise deficit (NIPA 3.8 line 13, housing and urban renewal, -$40.298bn
 *      in 2024) leaves the enterprise line and becomes its own receipt line, keyed by the rental-assistance key (the
 *      rental line's evaluated key, kh), not the population key (ke). The $5.258bn operating subsidy stays consolidated
 *      (internal_transfer "public_housing_operating"): the rental line and the housing line both lose it, and with one
 *      key on both legs that moves nothing. The rest of the enterprise line keeps its key, so the enterprise capital key
 *      does not move. "population" is the September 27 reading; with the subsidy consolidated it is the first candidate's
 *      item 1 (+$0.22bn), reported beside.
 *   2. production: "row4". The first candidate's item 2, unchanged (its derived/production_row4.json).
 *   3. tax_key: "irs_2023_raked". The federal income-tax key matched to IRS 2023 AGI bins, raked with CBO's groups
 *      (tax_key_heldout_2026_09_28, aec08a4): share_change.irs_2023_raked_with_cbo_groups from its translation_inputs.json,
 *      applied as its ends.cjs applies it (a receipt edit of stack factor x national x share change, expanded to every
 *      incidence rule), with the stack factor of the tax-block case being run.
 *
 * Beside the range: public_pay ("unchanged_workforce", the first candidate's reading; "counterfactual_low_share" and
 * "counterfactual_high_share", the charge on the workforce the account's own responses leave, attack section 4d) and
 * the road arm (road: "replacement", "fixed_stock", and the upward cases "construction_year_effects" and
 * "construction_land", in which the road stock and its lanes respond like highway construction; derived/road_stock.json).
 *
 * The congestion item beside the account, at any lane cut the lane uses, comes from road_congestion.py; laneCut() and
 * congestionCuts() here define the cuts, so the Python step and main_case.cjs read one definition. rangeComponents() is
 * the September 27 case's outer-range components, as descriptors.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const C1 = require(path.join(__dirname, "..", "main_case_candidate_2026_09_28", "package.cjs"));
const P = C1.SEPT27;
const { Engine, MODEL, FISCAL, METHODS, ALLOCS, RENTAL, ENTERPRISE_LINE, ENTERPRISE_RECEIPT, LR, ROAD_LINE, ROAD_SUBFUNCTIONS,
  ROAD_COMPONENTS, DEPRECIATION, LINE_NATIONAL, LONG_RUN_VARIANTS, readJson, csvRows, span, mean2 } = C1;

const HERE = __dirname;
const CASE = "sept28_candidate_v2";
const LANE = "main_case_candidate_v2_2026_09_28";

// ---------------------------------------------------------------------------------------------------
// Item 1: public housing's deficit, split out and keyed by its tenants.
const ESV_FILE = "capital_return_services_2026_09_27/derived/enterprise_surplus_vs_return.csv";
const ESV = csvRows(ESV_FILE);
const ESV_HOUSING = ESV.find((r) => r.nipa_3_8_lines === "l13");
if (!ESV_HOUSING || ESV_HOUSING.nipa_3_8_group !== "housing and urban renewal") throw new Error(`[BLOCKED] ${ESV_FILE} has no NIPA 3.8 line 13`);
const HOUSING_SURPLUS = Number(ESV_HOUSING.current_surplus_2024_bn);
const E_NATIONAL = MODEL.receipts.lines.find((l) => l.id === ENTERPRISE_LINE).national_bn;
const H_NATIONAL = MODEL.spending.lines.find((l) => l.id === RENTAL).national_bn;
const ESV_TOTAL = ESV.reduce((a, r) => a + Number(r.current_surplus_2024_bn), 0);
if (!(HOUSING_SURPLUS < 0) || Math.abs(ESV_TOTAL - E_NATIONAL) > 1e-9) {
  throw new Error(`[BLOCKED] ${ESV_FILE}: its groups (${ESV_TOTAL}) are not the enterprise line (${E_NATIONAL})`);
}
const HOUSING_LINE = "housing_enterprise_surplus";
const HOUSING_RECEIPT = "receipt:" + HOUSING_LINE;
const HOUSING_KEYS = ["population", "tenants"];
const TRANSFERS = C1.TRANSFERS;
const scaleCells = (cells, f) => { for (const c of cells) { c.target_bn *= f; c.other_bn *= f; } };
const spendingCells = (l) => Object.values(l.keys).flatMap((k) => ALLOCS.map((a) => k[a]));
const receiptCells = (l) => Object.values(l.cells).flatMap((k) => ALLOCS.map((a) => k[a]));
// The split. The model passed in carries the September 27 lines (no consolidation yet); a new model is returned.
function splitHousing(m0, transfer) {
  if (!(transfer >= 0 && transfer < H_NATIONAL)) throw new Error(`[BLOCKED] internal transfer ${transfer}`);
  const m = Engine.clone(m0);
  const h = m.spending.lines.find((l) => l.id === RENTAL), e = m.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
  if (m.receipts.lines.some((l) => l.id === HOUSING_LINE)) throw new Error("[BLOCKED] the housing line is split already");
  if (h.national_bn !== H_NATIONAL || e.national_bn !== E_NATIONAL) throw new Error("[BLOCKED] the split starts from the September 27 lines");
  // The rental line, the operating subsidy consolidated: every cell keeps its fraction.
  scaleCells(spendingCells(h), (h.national_bn - transfer) / h.national_bn);
  h.national_bn -= transfer;
  // The enterprise line without public housing: every cell keeps its fraction, so its key (and the enterprise capital
  // key, receipt amount over national) stays.
  scaleCells(receiptCells(e), (e.national_bn - HOUSING_SURPLUS) / e.national_bn);
  e.national_bn -= HOUSING_SURPLUS;
  // Public housing's deficit, the subsidy consolidated, at the rental line's preferred key (the key the case evaluates;
  // main_case.cjs gates it), in every incidence rule.
  const national = HOUSING_SURPLUS - transfer;
  const hk = h.keys[h.preferred_key];
  const cell = (a) => {
    const f = hk[a].target_bn / h.national_bn;
    return { direct: false, key: h.preferred_key, response_class: "public_asset", share: f, target_bn: f * national, other_bn: (1 - f) * national };
  };
  m.receipts.lines.push({ id: HOUSING_LINE, national_bn: national,
    cells: Object.fromEntries(m.receipts.scenarios.map((sc) => [sc, { personal: cell("personal"), shared: cell("shared") }])) });
  return m;
}
// A synthetic internal transfer of `bn` to housing authorities on both of the split model's legs (the rental line and
// the housing line), each cell at its own fraction, not consolidated: the control for item 1's rule.
function withHousingTransfer(m0, bn) {
  const m = Engine.clone(m0);
  const h = m.spending.lines.find((l) => l.id === RENTAL), x = m.receipts.lines.find((l) => l.id === HOUSING_LINE);
  if (!x) throw new Error("[BLOCKED] no housing line: split the model first");
  scaleCells(spendingCells(h), (h.national_bn + bn) / h.national_bn);
  scaleCells(receiptCells(x), (x.national_bn + bn) / x.national_bn);
  h.national_bn += bn;
  x.national_bn += bn;
  return m;
}

// ---------------------------------------------------------------------------------------------------
// Item 3: the federal income-tax key matched to IRS 2023.
const TAX_FILE = "tax_key_heldout_2026_09_28/derived/translation_inputs.json";
const TAX = readJson(TAX_FILE);
const TAX_KEYS = { cbo_2022: null, irs_2023_raked: "irs_2023_raked_with_cbo_groups" };
const TAX_LINE = TAX.line;
if (TAX_LINE !== "federal_income_tax" || !TAX.share_change || !TAX.share_change[TAX_KEYS.irs_2023_raked]
  || Math.abs(MODEL.receipts.lines.find((l) => l.id === TAX_LINE).national_bn - TAX.national_bn) > 1e-9) {
  throw new Error(`[BLOCKED] ${TAX_FILE}: not the federal income-tax line of model.json, or no raked share change`);
}
const stackOf = (caseName, method) => P.stackFactor(P.STACKS[`row4+status_state_aware|${caseName}|${method}`], "receipt", TAX_LINE);
function taxEditOf(caseName, method, name) {
  const v = TAX.share_change[TAX_KEYS[name]];
  const stack = stackOf(caseName, method);
  if (!stack || ALLOCS.some((a) => !Number.isFinite(stack[a]) || !Number.isFinite(v[a]))) throw new Error(`[BLOCKED] no stack factor for ${caseName} / ${method}`);
  return Object.fromEntries(ALLOCS.map((a) => [a, stack[a] * TAX.national_bn * v[a]]));
}
function withTaxKey(m, caseName, method, name) {
  if (!(name in TAX_KEYS)) throw new Error(`[BLOCKED] unknown tax key ${name}`);
  if (TAX_KEYS[name] === null) return m;
  const by = taxEditOf(caseName, method, name);
  return Engine.applyCorrections(m, { lines: [], edits: P.expand([{ side: "receipt", line: TAX_LINE, by }]) });
}

// ---------------------------------------------------------------------------------------------------
// The road arm. The first candidate's three cases, plus the upward cases: the road stock (depreciation and the road
// capital return) and its lanes respond like highway construction across states. Construction's slope replaces the
// operations slope where the reading uses it, S&L highways at the low end; the high end is capped at 1 either way.
const STOCK_FILE = `${LANE}/derived/road_stock.json`;
if (!fs.existsSync(path.join(FISCAL, STOCK_FILE))) throw new Error(`[BLOCKED] ${STOCK_FILE} is missing: run road_stock.py first`);
const STOCK = readJson(STOCK_FILE);
if (!Array.isArray(STOCK.gates) || !STOCK.gates.length || !STOCK.gates.every((g) => g.passed)) throw new Error(`[BLOCKED] ${STOCK_FILE}: its gates did not all pass`);
const ROAD_CASES = Object.assign({}, Object.fromEntries(Object.entries(C1.ROAD_CASES).map(([k, v]) => [k, Object.assign({ v1: k, stock: null }, v)])), {
  construction_year_effects: { v1: "stationary_network", stock: STOCK.stock_responses_low_end.construction_year_effects, operations: 1,
    depreciation: 1, return: 1, lanes: "network follows the stock",
    label: "an upward stock: depreciation, the road capital return and lanes respond like highway construction across states (0.792, year effects)" },
  construction_land: { v1: "stationary_network", stock: STOCK.stock_responses_low_end.construction_land, operations: 1,
    depreciation: 1, return: 1, lanes: "network follows the stock",
    label: "an upward stock: depreciation, the road capital return and lanes respond like highway construction across states with a land control (0.758)" },
});
// The stock's response by road subfunction at a reading: construction's r for S&L highways at the low end, the operations
// response elsewhere (federal highways are fixed at the low end; every highway is capped at 1 at the high end).
function stockResponses(road, variant, reading) {
  const r = P.subfunctionResponses(variant, reading);
  const c = ROAD_CASES[road];
  if (!c.stock) return r;
  if (variant !== "adopted") throw new Error(`[BLOCKED] the upward road cases are built on the adopted responses, not ${variant}`);
  return Object.assign({}, r, reading === "low" ? { sl_highways: c.stock } : {});
}
// The line response the stock adds: depreciation at the stock's response instead of the operations response.
const stockIncrement = (road, variant, reading) => {
  const rs = stockResponses(road, variant, reading), ro = P.subfunctionResponses(variant, reading);
  return ROAD_SUBFUNCTIONS.reduce((a, sf) => a + DEPRECIATION[sf] * (rs[sf] - ro[sf]), 0) / LINE_NATIONAL;
};
// The highway response the lanes follow (S&L and federal highways weighted by national amount, the bridge's h).
const ROAD_SFS = LR.lines[ROAD_LINE].subfunctions.filter((s) => ROAD_SUBFUNCTIONS.includes(s.id));
const ROAD_SF_NATIONAL = ROAD_SFS.reduce((a, s) => a + s.national_bn, 0);
function lanesResponse(road, variant, reading) {
  const c = ROAD_CASES[road];
  if (c.lanes === "network fixed (bound)") return 0;
  const r = c.stock ? stockResponses(road, variant, reading) : P.subfunctionResponses(variant, reading);
  return ROAD_SFS.reduce((a, s) => a + s.national_bn * r[s.id], 0) / ROAD_SF_NATIONAL;
}
// The lane cut at an evaluated specification: kappa h k, with k the group's key share of the economic-affairs line.
function laneCut(spec, evaluation) {
  const l = evaluation.spending.find((x) => x.id === ROAD_LINE);
  return lanesResponse(spec.road, spec.long_run, spec.reading) * (l.amount_bn / l.national_bn);
}

// ---------------------------------------------------------------------------------------------------
// Public pay (beside the range). The charge is the first candidate's (production_row4.json public_pay, at the
// specification's production and normalization); the counterfactual readings charge it on the public workforce the
// account's own responses leave: charge x (1 - removal share), the removal share of government consumption read two
// ways (attack section 4d): all consumption lines (low share), or without defense and with the school rows (high share).
// A uniform removal share across skill groups is the approximation.
const PUBLIC_PAY = ["unchanged_workforce", "counterfactual_low_share", "counterfactual_high_share"];
const FAMILY = Object.fromEntries(MODEL.spending.lines.map((l) => [l.id, l.family]));
const SCHOOL_ROWS = [P.SYN.school, P.SYN.college];
function removalShares(evaluation) {
  const sp = evaluation.spending;
  const cons = sp.filter((l) => FAMILY[l.id] === "consumption");
  const nat = cons.reduce((a, l) => a + l.national_bn, 0);
  const natNoDefense = cons.filter((l) => l.id !== "defense").reduce((a, l) => a + l.national_bn, 0);
  const removed = -cons.reduce((a, l) => a + l.effect_bn, 0);
  const school = -sp.filter((l) => SCHOOL_ROWS.includes(l.id)).reduce((a, l) => a + l.effect_bn, 0);
  return { low: removed / nat, high: (removed + school) / natNoDefense };
}
function publicPay(spec, evaluation) {
  if (!spec.public_pay) return 0;
  const charge = C1.publicPayOf(spec.production, spec.normalization);
  if (spec.public_pay === "unchanged_workforce") return charge;
  const sh = removalShares(evaluation);
  return charge * (1 - (spec.public_pay === "counterfactual_low_share" ? sh.low : sh.high));
}

// ---------------------------------------------------------------------------------------------------
const CANDIDATE = { production: "row4", housing: "tenants", internal_transfer: "public_housing_operating", tax_key: "irs_2023_raked",
  road: "stationary_network", public_pay: false };
const OFF = { production: "published", housing: "population", internal_transfer: "none", tax_key: "cbo_2022",
  road: "stationary_network", public_pay: false };
// The first candidate, in this package's options (its road arm and public pay aside).
const V1 = { production: "row4", housing: "population", internal_transfer: "public_housing_operating", tax_key: "cbo_2022",
  road: "stationary_network", public_pay: false };
// The first candidate's options for a v2 option set: under the tenant key the subsidy is consolidated on the split
// lines, not by the first candidate's consolidate().
const v1Options = (oo) => Object.assign({}, oo, { road: ROAD_CASES[oo.road].v1, public_pay: false,
  internal_transfer: oo.housing === "tenants" ? "none" : oo.internal_transfer });
function withCentral(o) {
  const x = Object.assign({}, CANDIDATE, o || {});
  if (!HOUSING_KEYS.includes(x.housing)) throw new Error(`[BLOCKED] unknown housing key ${x.housing}`);
  if (!(x.tax_key in TAX_KEYS)) throw new Error(`[BLOCKED] unknown tax key ${x.tax_key}`);
  if (!ROAD_CASES[x.road]) throw new Error(`[BLOCKED] unknown road case ${x.road}`);
  if (x.public_pay !== false && !PUBLIC_PAY.includes(x.public_pay)) throw new Error(`[BLOCKED] unknown public-pay reading ${x.public_pay}`);
  if (x.housing === "tenants" && !["none", "public_housing_operating"].includes(x.internal_transfer)) {
    throw new Error(`[BLOCKED] under the tenant key the consolidated transfer is public housing's operating subsidy, not ${x.internal_transfer}`);
  }
  const oo = C1.withCentral(v1Options(x));
  if (ROAD_CASES[x.road].stock && oo.long_run !== "adopted") throw new Error("[BLOCKED] the upward road cases need the adopted long-run responses");
  return Object.assign({}, oo, { housing: x.housing, internal_transfer: x.internal_transfer, tax_key: x.tax_key, road: x.road,
    public_pay: x.public_pay });
}
function specsFor(o) {
  const oo = withCentral(o);
  const road = ROAD_CASES[oo.road];
  return C1.specsFor(v1Options(oo)).map((s) => {
    const lines = Object.assign({}, s.line_responses);
    if (road.stock) lines[ROAD_LINE] = s.line_responses[ROAD_LINE] + stockIncrement(oo.road, s.long_run, s.reading);
    if (oo.housing === "tenants") lines[HOUSING_RECEIPT] = s.line_responses[ENTERPRISE_RECEIPT];
    return Object.assign({}, s, { line_responses: lines, case: CASE, housing: oo.housing, internal_transfer: oo.internal_transfer,
      tax_key: oo.tax_key, road: oo.road, public_pay: oo.public_pay });
  });
}
function modelFor(caseName, method, oo) {
  let m = C1.modelFor(caseName, method, v1Options(oo));
  if (oo.housing === "tenants") m = splitHousing(m, TRANSFERS[oo.internal_transfer].bn);
  m = withTaxKey(m, caseName, method, oo.tax_key);
  return Object.assign({}, m, { candidate: Object.assign({}, m.candidate, { housing: oo.housing, tax_key: oo.tax_key }) });
}
const tagOf = (m, k, dflt) => (m.candidate && m.candidate[k]) || dflt;
// cost = the first candidate's (engine + capital return, road cases) with the upward stock's road return, + public pay.
function evaluateFull(m, spec, profile) {
  const road = ROAD_CASES[spec.road];
  if (!road || !HOUSING_KEYS.includes(spec.housing) || !(spec.tax_key in TAX_KEYS)) {
    throw new Error("[BLOCKED] a specification without v2's fields: build it with specsFor()");
  }
  if (spec.housing !== tagOf(m, "housing", "population") || spec.tax_key !== tagOf(m, "tax_key", "cbo_2022")) {
    throw new Error(`[BLOCKED] a ${spec.housing} / ${spec.tax_key} specification on a ${tagOf(m, "housing", "population")} / ${tagOf(m, "tax_key", "cbo_2022")} model`);
  }
  const pr = P.ALL_PROFILES[profile || P.MAIN_PROFILE];
  if (road.stock && (!pr || pr.delayed !== null)) throw new Error(`[BLOCKED] the road arm applies where roads take their long-run response, not under ${profile}`);
  const r = C1.evaluateFull(m, Object.assign({}, spec, { road: road.v1, public_pay: false }), profile);
  let capital = r.capital;
  if (road.stock) {
    const ids = Object.values(ROAD_COMPONENTS);
    const rs = stockResponses(spec.road, spec.long_run, spec.reading), ro = P.subfunctionResponses(spec.long_run, spec.reading);
    const sfOf = Object.fromEntries(Object.entries(ROAD_COMPONENTS).map(([sf, id]) => [id, sf]));
    const components = r.capital.components.map((c) => {
      if (!ids.includes(c.id)) return c;
      const sf = sfOf[c.id];
      if (c.response !== ro[sf]) throw new Error(`[BLOCKED] ${c.id} responds at ${c.response}, not its subfunction's ${ro[sf]}`);
      const response = rs[sf];
      return Object.assign({}, c, { response, return_bn: c.stock_charged_bn * spec.rate * c.key * response });
    });
    capital = { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
  }
  const pay = publicPay(spec, r.evaluation);
  return { evaluation: r.evaluation, capital, road_return_removed_bn: r.road_return_removed_bn, public_pay_bn: pay,
    cost_bn: -r.evaluation.welfare_bn + capital.total_bn + pay };
}
const cost = (m, spec, profile) => evaluateFull(m, spec, profile).cost_bn;
const bandFor = (m, profile, specs) => span(specs.map((spec) => cost(m, spec, profile)));
function evalPackage(caseName, method, o) {
  const oo = withCentral(o);
  return bandFor(modelFor(caseName, method, oo), oo.profile, specsFor(oo));
}
const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
const MAIN_SPECS = specsFor({});
const band = (m, profile) => bandFor(m, profile, MAIN_SPECS);

// ---------------------------------------------------------------------------------------------------
// The specifications. The 64 hold 32 distinct ones (the school dimension has been overridden to full cost since
// 2026-09-26); every statistic across specifications uses the first of each pair.
const specKey = (s) => JSON.stringify(s);
function distinctSpecs(specs) {
  const seen = new Map();
  specs.forEach((s, i) => { const k = specKey(s); if (!seen.has(k)) seen.set(k, i); });
  return [...seen.values()];
}

// ---------------------------------------------------------------------------------------------------
// The September 27 case's outer-range components (its main_case.cjs), as descriptors: each variant is an option set, a
// tax-block case and the methods it runs on.
function rangeComponents() {
  const benSe = Object.fromEntries(C1.benefitSe.map((r) => [r.allocation, 1.96 * Number(r.se_bn)]));
  const v = (label, o, caseName, methods) => ({ v: label, o: o || {}, caseName: caseName || "central", methods: methods || METHODS });
  const comps = [
    ["tax_block", "tax block: on-books share (low/central/high) x fill-in method",
      C1.CASES.flatMap((c) => METHODS.map((m) => v(`${c}/${m}`, {}, c, [m])))],
    ["income_tax", "CBO income gradients: 2018/2019/2022 data, scaled or not by the stack's factor",
      [2018, 2019, 2022].flatMap((y) => [true, false].map((sc) => v(`${y}${sc ? "" : " unscaled"}`, { year: y, scaled: sc })))],
    ["medical", "decision 2: medical-ethnicity specifications and the MCBS 65+ bound",
      ["plain", "winsor_p999", "two_part_lognormal", "pooled_excl_2020_2021", "pooled_cpi_all_items", "pooled_year_normalized"]
        .map((sp) => v(sp, { medSpec: sp })).concat([v("MCBS as truth", { mcbs: "mcbs_as_truth" }), v("MCBS precision-weighted", { mcbs: "precision_weighted" })])],
    ["ltss", "long-term-care carve-out: extremes of the lane's 960 combinations", C1.LTSS_RANGE.map((x) => v(String(x), { ltss: x }))],
    ["education", "audit row 6 weight w (0.77/0.82) x school price k (low/high)",
      ["0.77", "0.82"].flatMap((w) => ["low", "preferred", "high"].map((k) => v(`w ${w} k ${k}`, { w, k })))],
    ["benefits", "benefit keys: central +/- 1.96 SE (package_se.csv)",
      [-1, 1].map((sg) => v(`${sg > 0 ? "+" : "-"}1.96 SE`, { benefitsDev: { personal: sg * benSe.personal, shared: sg * benSe.shared } }))],
    ["justice", "row 7 on 2023 arrests; booking factor Texas only or Arizona only",
      [v("row 7 2023", { row7: "2023" }), v("booking Texas", { booking: "texas" }), v("booking Arizona", { booking: "arizona" })]],
  ];
  for (const id of Object.keys(C1.CONSTANTS)) comps.push([id, C1.CONSTANTS[id].label, ["lo", "hi"].map((p) => v(p, { constants: { [id]: p } }))]);
  comps.push(
    ["finite_removal", "general government's removal response: r = b (fixed plus constant marginal cost); engine-key population share",
      [v("r = b", { finite: false }), v("engine population key", { gg_s: "engine_population_key" })]],
    ["consumption_key", "consumption key: the lane's twelve saving-and-remittance specifications", C1.CK_SPECS.map((sp) => v(sp, { ck: sp }))],
    ["school_response", "school response: within-district elasticity 0.836 read over the removal (0.8489) or taken as the response",
      [v("within district, finite r", { school_rule: "within_district" }), v("within district, r = b", { school_rule: "within_district_as_response" })]],
    ["long_run_response", "long-run responses: r = b; within-state uncapped; federal fixed at the high end; across-state at the high end; held-at-zero lines at 1",
      Object.keys(LONG_RUN_VARIANTS).filter((x) => x !== "adopted").map((x) => v(x, { long_run: x }))],
    ["capital_rate", "return on public capital: 2% at both ends; 3% at both ends",
      [v("2% at both ends", { rates: { low: 0.02, high: 0.02 } }), v("3% at both ends", { rates: { low: 0.03, high: 0.03 } })]],
    ["capital_definition", "return on public capital: the capital lane's definition variants (engine_components.json variants), each re-run at every specification",
      Object.keys(C1.CAP.variants).map((x) => v(x, { capital_variant: x }))],
  );
  return comps.map(([name, label, variants]) => ({ name, label, variants }));
}
// A variant's evaluations on a base: per method, every specification.
function variantRuns(base, variant) {
  const oo = withCentral(Object.assign({}, base, variant.o));
  const specs = specsFor(oo);
  return { specs, runs: variant.methods.map((meth) => { const m = modelFor(variant.caseName, meth, oo); return specs.map((s) => evaluateFull(m, s, oo.profile)); }) };
}
// Each method's end specifications (the first of equal costs, over the distinct specifications).
function endsOf(specs, runs) {
  const idx = distinctSpecs(specs);
  return runs.map((xs) => {
    let lo = idx[0], hi = idx[0];
    for (const i of idx) { if (xs[i].cost_bn < xs[lo].cost_bn) lo = i; if (xs[i].cost_bn > xs[hi].cost_bn) hi = i; }
    return [lo, hi];
  });
}
// The lane cut at a band end, as the congestion bridge reads it: the two methods' cuts averaged (the bridge's k is the
// methods' mean key). idx gives each method's [low end, high end] specification.
function endCuts(specs, runs, idx) {
  return [0, 1].map((e) => runs.reduce((a, xs, k) => a + laneCut(specs[idx[k][e]], xs[idx[k][e]].evaluation), 0) / runs.length);
}
const ENDS = [48, 11];
const fixedEnds = (runs) => runs.map(() => ENDS);
// The road arm the lane reports: each road case at the adopted responses, and the stationary network at every long-run
// variant (the range component read jointly with congestion).
const ROAD_ARM = [...Object.keys(ROAD_CASES).map((road) => ({ road, long_run: "adopted" })),
  ...Object.keys(LONG_RUN_VARIANTS).filter((x) => x !== "adopted").map((x) => ({ road: "stationary_network", long_run: x }))];
// Every lane cut main_case.cjs prices: the road arm at the fixed end specifications on the candidate and on the
// September 27 case (with factorial ranges), and every range variant's band ends on the candidate, the first candidate
// and the September 27 case (central only).
function congestionCuts() {
  const cuts = new Map();
  const add = (c, factorial) => cuts.set(c, (cuts.get(c) || false) || factorial);
  for (const base of [CANDIDATE, OFF]) for (const a of ROAD_ARM) {
    const { specs, runs } = variantRuns(base, { o: { road: a.road, long_run: a.long_run }, caseName: "central", methods: METHODS });
    endCuts(specs, runs, fixedEnds(runs)).forEach((c) => add(c, true));
  }
  for (const base of [CANDIDATE, V1, OFF]) for (const comp of rangeComponents()) for (const variant of [{ o: {}, caseName: "central", methods: METHODS }, ...comp.variants]) {
    const { specs, runs } = variantRuns(base, variant);
    endCuts(specs, runs, endsOf(specs, runs)).forEach((c) => add(c, false));
  }
  return [...cuts].map(([cut, factorial]) => ({ cut, factorial })).sort((a, b) => a.cut - b.cut);
}

module.exports = Object.assign({}, C1, {
  HERE, V1PKG: C1, SEPT27: P, CASE, LANE, ESV_FILE, HOUSING_SURPLUS, E_NATIONAL, H_NATIONAL, HOUSING_LINE, HOUSING_RECEIPT,
  HOUSING_KEYS, TAX_FILE, TAX, TAX_KEYS, TAX_LINE, STOCK_FILE, STOCK, ROAD_CASES, ROAD_ARM, ENDS, PUBLIC_PAY, FAMILY, SCHOOL_ROWS,
  CANDIDATE, OFF, V1, MAIN_SPECS,
  splitHousing, withHousingTransfer, stackOf, taxEditOf, withTaxKey, stockResponses, stockIncrement, lanesResponse, laneCut,
  removalShares, publicPay, v1Options, withCentral, specsFor, modelFor, evaluateFull, cost, bandFor, evalPackage, central, band,
  specKey, distinctSpecs, rangeComponents, variantRuns, endsOf, endCuts, fixedEnds, congestionCuts,
});
