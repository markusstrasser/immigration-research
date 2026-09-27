/* The next main-case revision as a candidate, not adopted: case sept28_candidate (BRIEF.md, e003ea1). The September 27
 * case (../main_case_long_run_2026_09_27/package.cjs, imported unchanged, $321.8194–387.3701bn) takes the two fixes its
 * decision queued, a road arm and one labelled variant. Nothing else changes.
 *
 *   1. Transfer consolidation (conceptual audit 3db388d section 7). A federal operating subsidy to a public housing
 *      authority sits on the rental line (housing_subsidies, keyed by housing support) and, under option D, inside the
 *      enterprise surplus as revenue (keyed by population). consolidate() takes the transfer out of both legs before
 *      keying: both lines' national totals fall by it and every cell keeps its attributed fraction, so the capital
 *      return's receipt key does not move. The amount is public housing's operating subsidy, HUD's FY2024 obligations
 *      (TRANSFERS). Section 8 paid to housing authorities as landlords is unpublished (NIPA Handbook ch. 12); all of
 *      line 4 bounds it.
 *   2. Production on the account's row-4 weights (conceptual audit ffcce20 section C): every production cell from
 *      derived/production_row4.json (production_row4.py, gated cell by cell against model.json on the published
 *      weights).
 *   3. The road arm (ladder entry 239; the September 27 decision's "joint road scenario"). Operations, depreciation, the
 *      road capital return and lane capacity move together under three physical cases (ROAD_CASES): the smaller
 *      stationary network (the September 27 case), replacement adjustment and a fixed stock. The congestion item beside
 *      the account follows the lanes (congestionOf()).
 *   4. Public pay, a labelled variant beside the range (adversarial audit 61b4eac section 1): public employers pay the
 *      production model's wage change on their payroll, skill group by skill group (production_row4.json public_pay).
 *
 * Options: every September 27 option, plus production ("row4" | "published"), internal_transfer (a TRANSFERS key),
 * road (a ROAD_CASES key) and public_pay (true | false). CANDIDATE is the candidate; OFF is the September 27 case.
 * A specification is the September 27 case's, in the same order and index, with those four fields added.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_long_run_2026_09_27", "package.cjs"));
const { Engine, MODEL, FISCAL, METHODS, ALLOCS, RENTAL, ENTERPRISE_LINE, LR, readJson, csvRows, span, mean2 } = P;

const HERE = __dirname;
const CASE = "sept28_candidate";

// ---------------------------------------------------------------------------------------------------
// Item 2: the production grid on the row-4 weights. A missing or ungated file stops the build.
const PRODUCTION_FILE = "main_case_candidate_2026_09_28/derived/production_row4.json";
if (!fs.existsSync(path.join(FISCAL, PRODUCTION_FILE))) {
  throw new Error(`[BLOCKED] ${PRODUCTION_FILE} is missing: run production_row4.py first`);
}
const PROD = readJson(PRODUCTION_FILE);
if (!Array.isArray(PROD.gates) || !PROD.gates.length || !PROD.gates.every((g) => g.passed)) {
  throw new Error(`[BLOCKED] ${PRODUCTION_FILE}: its gates did not all pass`);
}
if (JSON.stringify(PROD.grid.dims) !== JSON.stringify(Engine.PRODUCTION_DIMS.reduce((o, d) => Object.assign(o, { [d]: MODEL.production.dims[d] }), {}))) {
  throw new Error(`[BLOCKED] ${PRODUCTION_FILE}: its grid is not model.json's`);
}
const PRODUCTIONS = ["row4", "published"];
for (const name of PRODUCTIONS) {
  const g = PROD.grid[name];
  if (!g || ["private_wtp_bn", "induced_receipts_bn", "sampling_se_bn"].some((k) => !Array.isArray(g[k]) || g[k].length !== MODEL.production.private_wtp_bn.length)) {
    throw new Error(`[BLOCKED] ${PRODUCTION_FILE}: an incomplete ${name} grid`);
  }
}
// The model with a production grid. "published" leaves model.json's arrays; the tag lets evaluateFull() check that a
// specification's production is its model's.
function withProduction(m, name) {
  if (!PRODUCTIONS.includes(name)) throw new Error(`[BLOCKED] unknown production ${name}`);
  const production = name === "published" ? m.production : Object.assign({}, m.production, {
    private_wtp_bn: PROD.grid.row4.private_wtp_bn, induced_receipts_bn: PROD.grid.row4.induced_receipts_bn,
    sampling_se_bn: PROD.grid.row4.sampling_se_bn });
  return Object.assign({}, m, { production, candidate: Object.assign({}, m.candidate, { production: name }) });
}
const productionOf = (m) => (m.candidate && m.candidate.production) || "published";

// ---------------------------------------------------------------------------------------------------
// Item 1: the internal transfer. HUD, FY2026 Congressional Justification, Public Housing Fund, "Summary of resources by
// program", FY2024 obligations (thousands): Public Housing Formula Grants (Operating Expenses) 5,232,640; Shortfall
// Prevention 25,171 (_cache/hud/2026_CJ_Program_PH_Fund.pdf, p. 4-2).
const HUD = { operating_formula_obligations_2024_thousands: 5232640, shortfall_prevention_obligations_2024_thousands: 25171,
  source: "https://www.hud.gov/sites/dfiles/CFO/documents/2026_CJ_Program_PH_Fund.pdf, p. 4-2 (Summary of resources by program, 2024 obligations)" };
const LINE4 = MODEL.spending.lines.find((l) => l.id === RENTAL).national_bn;
const TRANSFERS = {
  none: { bn: 0, label: "not consolidated (the September 27 case)" },
  public_housing_operating: { bn: (HUD.operating_formula_obligations_2024_thousands + HUD.shortfall_prevention_obligations_2024_thousands) / 1e6,
    label: "public housing's operating subsidies: HUD FY2024 obligations, operating formula grants plus shortfall prevention",
    source: HUD.source },
  all_of_line_4: { bn: LINE4, label: "the bound: all of NIPA Table 3.13 line 4 (federal housing subsidies) paid to government enterprises" },
};
// Consolidation: the transfer leaves both legs, the rental line and the enterprise surplus. Each line's national total
// falls by it, and every cell (every allocation rule, incidence rule and allocation) keeps its attributed fraction of
// its line and its share of its base. A new model; the one passed in is not touched.
function scaleLine(cells, factor) {
  for (const c of cells) { c.target_bn *= factor; c.other_bn *= factor; }
}
const spendingCells = (l) => Object.values(l.keys).flatMap((k) => ALLOCS.map((a) => k[a]));
const receiptCells = (l) => Object.values(l.cells).flatMap((k) => ALLOCS.map((a) => k[a]));
function consolidate(m0, bn) {
  if (!(bn >= 0)) throw new Error(`[BLOCKED] internal transfer ${bn}`);
  if (bn === 0) return m0;
  const m = Engine.clone(m0);
  const h = m.spending.lines.find((l) => l.id === RENTAL), e = m.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
  if (bn > h.national_bn) throw new Error(`[BLOCKED] an internal transfer of ${bn} exceeds ${RENTAL}'s ${h.national_bn}`);
  scaleLine(spendingCells(h), (h.national_bn - bn) / h.national_bn);
  scaleLine(receiptCells(e), (e.national_bn - bn) / e.national_bn);
  h.national_bn -= bn;
  e.national_bn -= bn;
  m.candidate = Object.assign({}, m0.candidate, { internal_transfer_bn: bn });
  return m;
}
// The audit's positive control: a synthetic internal transfer of `bn` on both legs, each cell taking its own attributed
// fraction (conceptual_audit_2026_09_27/probe_fiscal.cjs adds it to the evaluated cells alone).
function withSyntheticTransfer(m0, bn) {
  const m = Engine.clone(m0);
  const h = m.spending.lines.find((l) => l.id === RENTAL), e = m.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
  scaleLine(spendingCells(h), (h.national_bn + bn) / h.national_bn);
  scaleLine(receiptCells(e), (e.national_bn + bn) / e.national_bn);
  h.national_bn += bn;
  e.national_bn += bn;
  return m;
}

// ---------------------------------------------------------------------------------------------------
// Item 3: the road arm. The road subfunctions of economic_affairs_services and their capital components; each
// subfunction's depreciation sits inside its consumption (capital_return_services_2026_09_27 RESULT section 7, "The
// highway line, checked"), charged basis (S&L less toll facilities).
const ROAD_LINE = "economic_affairs_services";
const ROAD_COMPONENTS = { sl_highways: "hwy_sl", fed_highways: "hwy_fed" };
const ROAD_SUBFUNCTIONS = Object.keys(ROAD_COMPONENTS);
const BLOCK_FILE = "capital_return_services_2026_09_27/derived/block_components.csv";
const BLOCK = csvRows(BLOCK_FILE);
const DEPRECIATION = Object.fromEntries(ROAD_SUBFUNCTIONS.map((sf) => {
  const r = BLOCK.find((x) => x.subfunction === sf && x.component === ROAD_COMPONENTS[sf]);
  if (!r || !Number.isFinite(Number(r.depreciation_2024_charged_basis_bn))) throw new Error(`[BLOCKED] ${BLOCK_FILE} has no depreciation for ${sf}`);
  return [sf, Number(r.depreciation_2024_charged_basis_bn)];
}));
const LINE_NATIONAL = LR.lines[ROAD_LINE].national_bn;
for (const sf of ROAD_SUBFUNCTIONS) {
  const x = LR.lines[ROAD_LINE].subfunctions.find((s) => s.id === sf);
  if (!x || !(DEPRECIATION[sf] > 0 && DEPRECIATION[sf] < x.national_bn)) throw new Error(`[BLOCKED] ${sf}: depreciation is not inside its consumption`);
}
if (MODEL.spending.lines.find((l) => l.id === ROAD_LINE).national_bn !== LINE_NATIONAL) throw new Error(`[BLOCKED] ${ROAD_LINE}: responses.json and model.json disagree on the national total`);
// operations, depreciation and return: 1 responds at the road's long-run response, 0 does not. lanes: the congestion
// bridge's case (service_response_long_run_2026_09_27/congestion.py): the network follows spending (kappa 1) or stays.
const ROAD_CASES = {
  stationary_network: { operations: 1, depreciation: 1, return: 1, lanes: "network follows spending",
    label: "a smaller stationary network: operations, depreciation, the capital return and lanes all follow the long-run road response (the September 27 case)" },
  replacement: { operations: 1, depreciation: 1, return: 0, lanes: "network fixed (bound)",
    label: "replacement adjustment: worn road capital is not replaced (depreciation follows the response) while the stock in place keeps its return and its lanes" },
  fixed_stock: { operations: 1, depreciation: 0, return: 0, lanes: "network fixed (bound)",
    label: "a fixed stock: only operations follow the response; depreciation, the capital return and lanes stay" },
};
// The line response less its road subfunctions' depreciation at their long-run responses (the fixed stock).
function depreciationCut(variant, reading) {
  const r = P.subfunctionResponses(variant, reading);
  return ROAD_SUBFUNCTIONS.reduce((a, sf) => a + DEPRECIATION[sf] * r[sf], 0) / LINE_NATIONAL;
}
const CONGESTION_FILE = "service_response_long_run_2026_09_27/derived/congestion_bridge.csv";
const CONGESTION = csvRows(CONGESTION_FILE);
function congestionOf(road, reading) {
  const c = ROAD_CASES[road];
  const r = CONGESTION.find((x) => x.band_end === reading && x.variant === c.lanes && x.geography === "uniform (account key)");
  if (!r) throw new Error(`[BLOCKED] ${CONGESTION_FILE} has no row ${reading} / ${c.lanes}`);
  return { congestion_bn: Number(r.congestion_central_bn), range_bn: [Number(r.factorial_min_bn), Number(r.factorial_max_bn)] };
}

// ---------------------------------------------------------------------------------------------------
// Item 4: public pay at the case's production cell, by the specification's production and normalization.
function publicPayOf(production, normalization) {
  const x = PROD.public_pay[production] && PROD.public_pay[production][normalization];
  if (!x || !Number.isFinite(x.charge_bn)) throw new Error(`[BLOCKED] no public-pay charge for ${production} / ${normalization}`);
  return x.charge_bn;
}

// ---------------------------------------------------------------------------------------------------
const CANDIDATE = { production: "row4", internal_transfer: "public_housing_operating", road: "stationary_network", public_pay: false };
const OFF = { production: "published", internal_transfer: "none", road: "stationary_network", public_pay: false };
function withCentral(o) {
  const oo = P.withCentral(Object.assign({}, CANDIDATE, o || {}));
  if (!PRODUCTIONS.includes(oo.production)) throw new Error(`[BLOCKED] unknown production ${oo.production}`);
  if (!TRANSFERS[oo.internal_transfer]) throw new Error(`[BLOCKED] unknown internal transfer ${oo.internal_transfer}`);
  if (!ROAD_CASES[oo.road]) throw new Error(`[BLOCKED] unknown road case ${oo.road}`);
  if (typeof oo.public_pay !== "boolean") throw new Error(`[BLOCKED] public_pay must be true or false`);
  if (oo.road !== "stationary_network" && !oo.long_run) throw new Error("[BLOCKED] the road arm needs the long-run responses");
  return oo;
}
function specsFor(o) {
  const oo = withCentral(o);
  const road = ROAD_CASES[oo.road];
  return P.specsFor(oo).map((s) => {
    const lines = Object.assign({}, s.line_responses);
    if (road.depreciation === 0) lines[ROAD_LINE] = s.line_responses[ROAD_LINE] - depreciationCut(s.long_run, s.reading);
    return Object.assign({}, s, { line_responses: lines, case: CASE, production: oo.production,
      internal_transfer: oo.internal_transfer, road: oo.road, public_pay: oo.public_pay });
  });
}
function modelFor(caseName, method, oo) {
  return consolidate(withProduction(P.modelFor(caseName, method, oo), oo.production), TRANSFERS[oo.internal_transfer].bn);
}
// cost = the September 27 cost (engine + capital return) - the road capital the road case keeps + public pay.
function evaluateFull(m, spec, profile) {
  const road = ROAD_CASES[spec.road];
  if (!road || !PRODUCTIONS.includes(spec.production)) throw new Error("[BLOCKED] a specification without the candidate's fields: build it with specsFor()");
  if (spec.production !== productionOf(m)) throw new Error(`[BLOCKED] a ${spec.production} specification on a ${productionOf(m)} model`);
  const pr = P.ALL_PROFILES[profile || P.MAIN_PROFILE];
  if (road !== ROAD_CASES.stationary_network && (!pr || pr.delayed !== null)) {
    throw new Error(`[BLOCKED] the road arm applies where roads take their long-run response, not under ${profile}`);
  }
  const r = P.evaluateFull(m, spec, profile);
  const pay = spec.public_pay ? publicPayOf(spec.production, spec.normalization) : 0;
  if (road.return) return { evaluation: r.evaluation, capital: r.capital, road_return_removed_bn: 0, public_pay_bn: pay, cost_bn: r.cost_bn + pay };
  const ids = Object.values(ROAD_COMPONENTS);
  const removed = r.capital.components.filter((c) => ids.includes(c.id)).reduce((a, c) => a + c.return_bn, 0);
  const components = r.capital.components.map((c) => (ids.includes(c.id) ? Object.assign({}, c, { response: 0, return_bn: 0 }) : c));
  const capital = { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
  return { evaluation: r.evaluation, capital, road_return_removed_bn: removed, public_pay_bn: pay,
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

module.exports = Object.assign({}, P, {
  HERE, SEPT27: P, CASE, PRODUCTION_FILE, PROD, PRODUCTIONS, HUD, TRANSFERS, ROAD_LINE, ROAD_COMPONENTS, ROAD_SUBFUNCTIONS,
  BLOCK_FILE, DEPRECIATION, LINE_NATIONAL, ROAD_CASES, CONGESTION_FILE, CANDIDATE, OFF, MAIN_SPECS,
  withProduction, productionOf, consolidate, withSyntheticTransfer, depreciationCut, congestionOf, publicPayOf,
  withCentral, specsFor, modelFor, evaluateFull, cost, bandFor, evalPackage, central, band,
});
