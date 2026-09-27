/* The receipt-side long-run lane (BRIEF.md, 2b85073): gates, then derived/. Loads the adopted September 27 package
 * unchanged (through items.cjs) and reads housing.py's derived/housing.json.
 *
 *   1. Trace: every direct:false receipt line at specifications 48 and 11 (both fill-in methods averaged), and what the
 *      production term's induced receipts F contain, from the module's own export
 *      (full_account_benefits_2026_09_20/derived/upstream_replay/scenarios.csv) and the engine's production grid.
 *   2. The owner-occupied property tax at the derived long-run response (central, low, high); beside, the short run
 *      (assessment caps binding, and every roll following the market) and the capital-tax view.
 *   3. The tenant-occupied housing tax split out of the capital-keyed business property line, keyed by rent.
 *   4. Business property, other production taxes, business transfers and corporate taxes: F's channel; nothing moves
 *      in the case; beside, the use-key and module-cell sensitivities.
 *   5. One rule, both sides: every line of both sides with its base, whether that base scales with population in the
 *      long run and the response the rule implies; the defense bound beside.
 * Each item alone at 48 and 11, then together; the band over the 32 distinct specifications (48 = 52, 11 = 15).
 * Gates: the replica reproduces evaluateFull and the committed per_spec.csv at every specification and method; each
 * item moves only its named lines; re-keys and the split hold national totals and move other residents' share by the
 * opposite amount; items add; the correction-constant route gives the split's cost; F is the module's labor-tax gain;
 * the one-rule table carries every line once and its effects are the items'.
 * Exit 1 and nothing written on failure. Run from anywhere, after housing.py: node probe.cjs [--out-dir DIR] ->
 * derived/probe.json, derived/trace.csv, derived/items.csv, derived/one_rule.csv.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const I = require("./items.cjs");
const { K, H, HERE, OWNER_LINE, BUSINESS_LINE, TENANT_LINE, PERSONAL_LINE, RESPONSES, TENANT_NATIONAL, KEYS, CENTRAL_ITEMS,
  NONE, only, itemModel, itemOverrides, evaluateWith, MODELS, line, receiptCells } = I;
const { Engine, MODEL, ALLOCS, METHODS, MAIN_SPECS, MAIN_PROFILE, evaluateFull, gate, near, gateState, csvRows, readJson } = K;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
const ENDS = [48, 11];
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const f4 = (x) => x.toFixed(4);
// The first index of each distinct specification (48 before 52, 11 before 15).
const distinct = MAIN_SPECS.map((s, i) => i).filter((i) => MAIN_SPECS.findIndex((s) => JSON.stringify(s) === JSON.stringify(MAIN_SPECS[i])) === i);

console.log("[gates: the replica]");
const s27 = readJson("main_case_long_run_2026_09_27/derived/summary.json");
const perSpec = csvRows("main_case_long_run_2026_09_27/derived/per_spec.csv");
let replicaGap = 0, committedGap = 0, committedN = 0;
const base = MODELS.map((m, k) => MAIN_SPECS.map((spec, i) => {
  const full = evaluateFull(m, spec, MAIN_PROFILE), mine = evaluateWith(m, spec, {});
  replicaGap = Math.max(replicaGap, Math.abs(full.cost_bn - mine.cost_bn));
  const row = perSpec.find((r) => r.method === METHODS[k] && +r.spec === i);
  if (row) { committedGap = Math.max(committedGap, Math.abs(+row.cost_bn - mine.cost_bn)); committedN += 1; }
  return mine;
}));
gate("the replica reproduces evaluateFull at all 64 specifications, both methods (1e-9)", replicaGap < 1e-9, `max |diff| ${replicaGap.toExponential(1)}`);
gate("the replica reproduces the committed per_spec.csv (128 rows, 1e-9)", committedN === 128 && committedGap < 1e-9, `${committedN} rows, max |diff| ${committedGap.toExponential(1)}`);
gate("64 specifications hold 32 distinct ones; 48 = 52 and 11 = 15", distinct.length === 32
  && JSON.stringify(MAIN_SPECS[48]) === JSON.stringify(MAIN_SPECS[52]) && JSON.stringify(MAIN_SPECS[11]) === JSON.stringify(MAIN_SPECS[15]),
  `${distinct.length} distinct`);
const atEnd = (runs) => ENDS.map((i) => mean(runs.map((xs) => xs[i].cost_bn)));
const baseEnds = atEnd(base);
const bandOf = (runs) => [0, 1].map((e) => mean(runs.map((xs) => (e ? Math.max : Math.min)(...distinct.map((i) => xs[i].cost_bn)))));
const baseBand = bandOf(base);
gate("the adopted case at 48 / 11 is $321.8194–387.3701bn, its band's ends", near(baseEnds[0], 321.8194, 1e-4) && near(baseEnds[1], 387.3701, 1e-4)
  && near(baseBand[0], baseEnds[0], 1e-9) && near(baseBand[1], baseEnds[1], 1e-9), `${f4(baseEnds[0])} / ${f4(baseEnds[1])}`);

// ---------------------------------------------------------------------------------------------------
// Item 1: the trace.
console.log("\n[item 1: the zero]");
const FLAG = { file: "full_account_2026_09_20/welfare.py (response_pools, capital_category)", commit: "0ab245f",
  copied: "assumption_explorer_2026_09_21/build_model.py (CAPITAL_CATEGORIES), 02c9996" };
const lineAt = (runs, side, id) => ENDS.map((i) => {
  const rows = runs.map((xs) => xs[i].evaluation[side].find((l) => l.id === id));
  return { amount: mean(rows.map((r) => r.amount_bn)), response: mean(rows.map((r) => r.response)),
    effect: mean(rows.map((r) => r.effect_bn)), share: mean(rows.map((r) => r.amount_bn / r.national_bn)), key: rows[0].key,
    national: rows[0].national_bn, cls: rows[0].response_class || rows[0].group };
});
const traceIds = MODEL.receipts.lines.filter((l) => !l.cells[MODEL.receipts.reference].shared.direct).map((l) => l.id);
const trace = traceIds.map((id) => {
  const [a, b] = lineAt(base, "receipts", id);
  const c = line(MODEL, id).cells[MODEL.receipts.reference].shared;
  return { id, national_bn: a.national, key: a.key, response_class: c.response_class, response_48: a.response, response_11: b.response,
    group_48_bn: a.amount, group_11_bn: b.amount, flag: ["modeled_owner_property", "personal_property_tax", "corporate_labor"].includes(id)
      ? `household class, zeroed as a capital category: ${FLAG.file} ${FLAG.commit}; ${FLAG.copied}`
      : `class ${c.response_class} is not a direct class: ${FLAG.file} ${FLAG.commit}; ${FLAG.copied}` };
});
gate("every direct:false receipt is at response 0 but the enterprise surplus (option D, 1)", trace.every((t) =>
  (t.id === "enterprise_surplus" ? t.response_48 === 1 && t.response_11 === 1 : t.response_48 === 0 && t.response_11 === 0)),
  trace.map((t) => `${t.id} ${t.response_48}`).join(", "));
// F: the module's export at the reference production cell, each normalization; the engine's grid across retention.
const MODULE_FILE = "full_account_benefits_2026_09_20/derived/upstream_replay/scenarios.csv";
const scen = csvRows(MODULE_FILE);
const ref = MODEL.production.reference;
const cellOf = (norm, adj, ret) => scen.find((r) => r.proxy === ref.proxy && r.split === ref.split && r.normalization === norm
  && +r.labor_share === ref.labor_share && +r.sigma === ref.sigma && +r.capital_adjustment === adj && +r.labor_supply_elasticity === ref.labor_supply_elasticity
  && +r.capital_tax_retention === ret && r.tax_classification_transport === "source_split");
const fParts = ENDS.map((i) => {
  const norm = MAIN_SPECS[i].normalization, c1 = cellOf(norm, 1, 1), c0 = cellOf(norm, 1, 0), a0 = cellOf(norm, 0, 1);
  const F = mean(base.map((xs) => xs[i].evaluation.induced_receipts_bn)), P = mean(base.map((xs) => xs[i].evaluation.private_wtp_bn));
  return { spec: i, normalization: norm, F_bn: F, P_bn: P, labor_tax_bn: +c1.labor_tax_gain_estimate / 1e9, capital_tax_bn: +c1.capital_tax_gain_estimate / 1e9,
    capital_income_following_group_bn: +c1.opportunity_income_estimate / 1e9, capital_tax_at_retention_0_bn: +c0.capital_tax_gain_estimate / 1e9,
    output_fall_full_adjustment: 1 - +c1.output_without_over_with, output_fall_capital_fixed: 1 - +a0.output_without_over_with };
});
for (const p of fParts) {
  gate(`spec ${p.spec} (${p.normalization}): F is the module's labor-tax gain and its capital-tax gain is 0 (1e-6)`,
    near(p.F_bn, p.labor_tax_bn, 1e-6) && p.capital_tax_bn === 0, `F ${f4(p.F_bn)}, labor ${f4(p.labor_tax_bn)}, capital ${p.capital_tax_bn}`);
}
const pr = MODEL.production, D = Engine.PRODUCTION_DIMS;
const idx = (p) => D.reduce((i, d) => i * pr.dims[d].length + pr.dims[d].findIndex((v) => v === p[d] || Math.abs(v - p[d]) < 1e-9), 0);
let invGap = 0;
const invariance = ["gdp", "cash"].map((norm) => {
  const at = (ret, exc) => { const j = idx(Object.assign({}, ref, { normalization: norm, capital_tax_retention: ret, excluded_capital_owner_share: exc }));
    return { P: pr.private_wtp_bn[j], F: pr.induced_receipts_bn[j] }; };
  const r1 = at(1, 0), r0 = at(0, 0), rh = at(0.5, 0), x0 = at(0, 1);
  invGap = Math.max(invGap, Math.abs(r1.P + r1.F - r0.P - r0.F), Math.abs(r1.P + r1.F - rh.P - rh.F));
  return { normalization: norm, P_plus_F: r1.P + r1.F, F_retention_1: r1.F, F_retention_0: r0.F, P_retention_0: r0.P,
    P_plus_F_retention_0_owners_excluded: x0.P + x0.F };
});
gate("P + F is invariant to capital-tax retention (0, 0.5, 1) at full adjustment with owners included (1e-8: the grid is stored to 1e-9)", invGap < 1e-8,
  invariance.map((v) => `${v.normalization} ${f4(v.P_plus_F)}`).join(", "));

// ---------------------------------------------------------------------------------------------------
// Items 2, 3 and the personal-property row: each alone, then together.
console.log("\n[items]");
const runsWith = (items) => MODELS.map((m0) => { const m = itemModel(m0, items), o = itemOverrides(items);
  return MAIN_SPECS.map((spec) => evaluateWith(m, spec, o)); });
// Every line but the named ones keeps amount, response and effect exactly; P, F and the capital return are unchanged.
function onlyMoves(a, b, ids) {
  let bad = [];
  for (let k = 0; k < a.length; k++) for (const i of distinct) {
    const ea = a[k][i].evaluation, eb = b[k][i].evaluation;
    for (const side of ["receipts", "spending"]) for (const l of ea[side]) {
      if (ids.includes(l.id)) continue;
      const r = eb[side].find((x) => x.id === l.id);
      if (!r || r.amount_bn !== l.amount_bn || r.response !== l.response || r.effect_bn !== l.effect_bn) bad.push(l.id);
    }
    const extra = eb.receipts.filter((x) => !ea.receipts.some((l) => l.id === x.id) && !ids.includes(x.id));
    if (extra.length || ea.private_wtp_bn !== eb.private_wtp_bn || ea.induced_receipts_bn !== eb.induced_receipts_bn
      || a[k][i].capital.total_bn !== b[k][i].capital.total_bn) bad.push("production, capital or an unnamed line");
  }
  return [...new Set(bad)];
}
const SETS = {
  owner: { items: only("owner"), lines: [OWNER_LINE] },
  owner_low: { items: only("owner", RESPONSES.owner.low), lines: [OWNER_LINE] },
  owner_high: { items: only("owner", RESPONSES.owner.high), lines: [OWNER_LINE] },
  owner_short_run: { items: only("owner", RESPONSES.owner.short_run), lines: [OWNER_LINE] },
  owner_short_run_market: { items: only("owner", RESPONSES.owner.short_run_market), lines: [OWNER_LINE] },
  owner_capital_tax_view: { items: only("owner", RESPONSES.owner.capital_tax_view), lines: [OWNER_LINE] },
  owner_cdg: { items: only("owner", H.owner.r_lr_cdg.mid), lines: [OWNER_LINE] },
  owner_probe_079: { items: only("owner", 0.79), lines: [OWNER_LINE] },
  tenant: { items: only("tenant"), lines: [BUSINESS_LINE, TENANT_LINE] },
  tenant_low: { items: only("tenant", Object.assign({}, CENTRAL_ITEMS.tenant, { r: RESPONSES.renter.low })), lines: [BUSINESS_LINE, TENANT_LINE] },
  tenant_high: { items: only("tenant", Object.assign({}, CENTRAL_ITEMS.tenant, { r: 1 })), lines: [BUSINESS_LINE, TENANT_LINE] },
  tenant_case_scaled: { items: only("tenant", Object.assign({}, CENTRAL_ITEMS.tenant, { national: TENANT_NATIONAL.case_scaled })), lines: [BUSINESS_LINE, TENANT_LINE] },
  tenant_rekey_only: { items: only("tenant", Object.assign({}, CENTRAL_ITEMS.tenant, { r: 0 })), lines: [BUSINESS_LINE, TENANT_LINE] },
  personal: { items: only("personal"), lines: [PERSONAL_LINE] },
  all: { items: CENTRAL_ITEMS, lines: [OWNER_LINE, BUSINESS_LINE, TENANT_LINE, PERSONAL_LINE] },
  all_low: { items: { owner: RESPONSES.owner.low, tenant: Object.assign({}, CENTRAL_ITEMS.tenant, { r: RESPONSES.renter.low }), personal: CENTRAL_ITEMS.personal },
    lines: [OWNER_LINE, BUSINESS_LINE, TENANT_LINE, PERSONAL_LINE] },
  all_high: { items: { owner: 1, tenant: Object.assign({}, CENTRAL_ITEMS.tenant, { r: 1, national: TENANT_NATIONAL.case_scaled }), personal: CENTRAL_ITEMS.personal },
    lines: [OWNER_LINE, BUSINESS_LINE, TENANT_LINE, PERSONAL_LINE] },
};
const RUNS = Object.fromEntries(Object.entries(SETS).map(([name, x]) => [name, runsWith(x.items)]));
for (const [name, x] of Object.entries(SETS)) {
  const bad = onlyMoves(base, RUNS[name], x.lines);
  gate(`${name}: only ${x.lines.join(", ")} move; production and the capital return are unchanged`, !bad.length, bad.join(", ") || "");
}
// National totals and the opposite move, on the models themselves (every scenario, every rule).
function nationalGate(name, m0, m1, ids) {
  let gap = 0, opp = 0;
  const tot = (m) => m.receipts.lines.reduce((a, l) => a + l.national_bn, 0);
  gap = Math.abs(tot(m0) - tot(m1));
  for (const sc of m0.receipts.scenarios) for (const a of ALLOCS) {
    const sum = (m, f) => ids.map((id) => line(m, id)).filter(Boolean).reduce((s, l) => s + f(l.cells[sc][a]), 0);
    const dT = sum(m1, (c) => c.target_bn) - sum(m0, (c) => c.target_bn), dO = sum(m1, (c) => c.other_bn) - sum(m0, (c) => c.other_bn);
    opp = Math.max(opp, Math.abs(dT + dO));
  }
  gate(`${name}: national receipts unchanged and other residents move by the opposite amount in every scenario and rule (1e-9)`,
    gap < 1e-9 && opp < 1e-9, `national ${gap.toExponential(1)}, target + other ${opp.toExponential(1)}`);
}
for (const [k, m0] of MODELS.entries()) {
  nationalGate(`tenant split (${METHODS[k]})`, m0, itemModel(m0, only("tenant")), [BUSINESS_LINE, TENANT_LINE]);
  nationalGate(`personal re-key (${METHODS[k]})`, m0, itemModel(m0, only("personal")), [PERSONAL_LINE]);
}
const effects = Object.fromEntries(Object.keys(SETS).map((name) => [name, ENDS.map((i, e) => atEnd(RUNS[name])[e] - baseEnds[e])]));
const addGap = Math.max(...[0, 1].map((e) => Math.abs(effects.all[e] - effects.owner[e] - effects.tenant[e] - effects.personal[e])));
gate("the three items add exactly at 48 and 11 (1e-9)", addGap < 1e-9, `${addGap.toExponential(1)}`);
// Each item's change is its own arithmetic: -r x amount on the group.
const tenantGroup = TENANT_NATIONAL.bea * KEYS.rent;
const personalOld = lineAt(base, "receipts", PERSONAL_LINE).map((x) => x.amount);
const expected = { tenant: [0, 1].map(() => -RESPONSES.renter.central * tenantGroup),
  personal: [0, 1].map(() => -1 * line(MODEL, PERSONAL_LINE).national_bn * KEYS.vehicles) };
for (const name of ["tenant", "personal"]) {
  gate(`${name}: the change is -r x the group's re-keyed amount (1e-9)`, [0, 1].every((e) => near(effects[name][e], expected[name][e], 1e-9)),
    `${f4(effects[name][0])} / ${f4(effects[name][1])}`);
}
const ownerAmt = lineAt(base, "receipts", OWNER_LINE).map((x) => x.amount);
gate("owner: the change is -r x the line's amount at each end (1e-9)", [0, 1].every((e) => near(effects.owner[e], -RESPONSES.owner.central * ownerAmt[e], 1e-9)),
  `${f4(effects.owner[0])} / ${f4(effects.owner[1])}`);
// The payload route: the tenant item as a correction-constant spending line (the schema the case already uses for lane
// constants) gives the split's cost at every specification.
const credit = RESPONSES.renter.central * tenantGroup;
let routeGap = 0;
MODELS.forEach((m0, k) => {
  const m = Engine.applyCorrections(m0, { meta: m0.corrections, lines: [{ id: "tenant_property_credit", family: "correction",
    response_class: "correction_constant", label: "tenant-occupied property tax at the renter key and long-run response" }],
    edits: [{ side: "spending", line: "tenant_property_credit", key: "k", by: { personal: -credit, shared: -credit } }] });
  for (const i of distinct) routeGap = Math.max(routeGap, Math.abs(evaluateWith(m, MAIN_SPECS[i], {}).cost_bn - RUNS.tenant[k][i].cost_bn));
});
gate("the tenant item as a correction constant gives the split's cost at all 32 specifications (1e-9)", routeGap < 1e-9, routeGap.toExponential(1));

// Bands over the distinct specifications, and where the ends fall.
const endsAt = (runs) => runs.map((xs) => [distinct.reduce((b, i) => (xs[i].cost_bn < xs[b].cost_bn ? i : b), distinct[0]),
  distinct.reduce((b, i) => (xs[i].cost_bn > xs[b].cost_bn ? i : b), distinct[0])]);
const bands = Object.fromEntries(Object.keys(SETS).map((n) => [n, { band: bandOf(RUNS[n]), ends: endsAt(RUNS[n]) }]));
gate("with all items on, the band's ends stay at specifications 48 and 11", bands.all.ends.every((e) => e[0] === 48 && e[1] === 11),
  JSON.stringify(bands.all.ends));

// ---------------------------------------------------------------------------------------------------
// Item 4, beside the case: the business taxes on the capital that serves the group's jobs.
const wageShare = lineAt(base, "receipts", "employer_hi").map((x) => x.share);
const BUSINESS_TAXES = { c_and_i_property: line(MODEL, BUSINESS_LINE).national_bn - TENANT_NATIONAL.bea,
  other_production_taxes: line(MODEL, "other_production_taxes").national_bn,
  corporate: line(MODEL, "corporate_capital").national_bn + line(MODEL, "corporate_labor").national_bn };
const businessTotal = Object.values(BUSINESS_TAXES).reduce((a, b) => a + b, 0);
const item4 = {
  use_key_at_1_bn: wageShare.map((w) => -w * businessTotal),
  module_cell_retention_0_owners_excluded_bn: fParts.map((p, e) => -(invariance.find((v) => v.normalization === p.normalization).P_plus_F_retention_0_owners_excluded
    - invariance.find((v) => v.normalization === p.normalization).P_plus_F)),
  wage_share: wageShare, business_taxes_bn: BUSINESS_TAXES,
};

// ---------------------------------------------------------------------------------------------------
// Item 5: every line set by convention.
const DEFENSE = lineAt(base, "spending", "defense");
const defenseBound = fParts.map((p) => ({ capital_fixed_bn: p.output_fall_capital_fixed * DEFENSE[0].national, full_adjustment_bn: p.output_fall_full_adjustment * DEFENSE[0].national,
  output_fall_capital_fixed: p.output_fall_capital_fixed, output_fall_full_adjustment: p.output_fall_full_adjustment }));
const GREEN_BOOK = { source: "DoD, National Defense Budget Estimates for FY 2025 (Green Book), Table 7-7, % of GDP, National Defense column",
  fy1986: 6.0, fy2000: 2.9, fy2010: 4.7, fy2024: 3.2, fy2024_note: "an estimate in the FY 2025 edition" };
const zero = [0, 0];
// Every line whose response a convention sets (0, or a class default), with its base, whether that base scales with
// population in the long run, and the response the long-run rule implies. [base, scales, rule response, effect, note]
const EXPLICIT = {
  [`receipt:${OWNER_LINE}`]: ["owner-occupied homes: structures and land", "structures yes; land stays, its price falls",
    `${f4(RESPONSES.owner.central)} (${f4(RESPONSES.owner.low)}-1)`, effects.owner, "item 2"],
  [`receipt:${BUSINESS_LINE}`]: ["rental housing and business property", "rental structures yes (item 3); business capital inside the production module",
    `tenant part ${f4(RESPONSES.renter.central)} at the rent key; rest 0`, effects.tenant, "item 3; the rest is item 4"],
  [`receipt:${PERSONAL_LINE}`]: ["household personal property (vehicles, boats)", "yes: the group's own durables", "1 at the vehicle key", effects.personal,
    "re-keyed from capital ownership"],
  "receipt:corporate_capital": ["corporate profits", "business capital follows the group's jobs (full adjustment)", "0: F's channel at retention 1", zero, "item 4"],
  "receipt:corporate_labor": ["corporate profits, labor's incidence", "as above", "0: F's channel at retention 1", zero, "item 4"],
  "receipt:other_production_taxes": ["business licenses, severance and other production taxes", "as above", "0: F's channel at retention 1", zero, "item 4"],
  "receipt:business_current_transfers": ["business transfers, fines and settlements", "not a tax on capital", "0", zero, "item 4"],
  "receipt:government_asset_income": ["interest, dividends, rents and royalties on public assets", "no: fixed assets and resources", "0", zero, "unchanged"],
  "receipt:enterprise_surplus": ["government enterprises' current surplus", "yes (option D)", "1", zero, "already 1"],
  "spending:defense": ["national defense", "no: set by threats, not population (share of GDP 6.0% 1986, 2.9% 2000, 4.7% 2010, 3.2% 2024)",
    "0", zero, "GDP-share bound beside the case"],
  "spending:general_public_services": ["general government", "partly, measured across states", "0.60 / 0.85 (finite removal)", zero, "already measured"],
  "spending:economic_affairs_services": ["roads, transport, economic administration, agriculture, energy, space and other economic affairs",
    "by subfunction: long-run where residents drive spending, 0 where they do not", "0.38 / 0.64 (the case's blend)", zero, "already long-run"],
  "spending:recreation_culture": ["parks, recreation and culture", "yes, measured across states", "0.86 / 1 (the case's)", zero, "already long-run"],
  "spending:domestic_interest": ["interest on the existing debt", "no: the stock is legacy", "0", zero,
    "the group's part of past deficits is a stock question (historical back-cast, debt legacy lane)"],
  "spending:foreign_interest": ["interest paid to foreign holders", "no: external key, nothing on residents", "0", zero, "unchanged"],
  "spending:agricultural_subsidies": ["farm programs", "no: acreage and commodities", "0", zero, "unchanged"],
  "spending:transport_subsidies": ["transit and rail operating subsidies", "weakly, with riders", "0 (at most +$0.03bn)", zero, "immaterial"],
  "spending:other_subsidies": ["other business subsidies", "no: paid to included owners", "0", zero, "the account's rule for subsidies to included owners"],
  "spending:housing_subsidies": ["rental assistance", "yes", "1", zero, "already 1"],
};
// Every other line keeps its class default, which the rule confirms. [base, scales, rule response]
const CLASS_RULES = {
  "receipt:personal_income": ["the group's own income", "yes: the group's own income", "1 (class default)"],
  "receipt:household_direct": ["the group's own payroll, purchases and household taxes", "yes: the group's own income and spending", "1 (class default)"],
  "receipt:foreign": ["receipts from abroad", "no: nothing on residents", "0"],
  "receipt:rounding": ["source rounding", "not applicable", "0"],
  "spending:household_transfer": ["benefits paid to the group", "yes: paid per recipient", "1 (class default)"],
  "spending:service": ["services the group uses", "yes: charged by use, or measured (schools at full cost)", "the case's response"],
  "spending:foreign": ["payments abroad", "no: external key, nothing on residents", "0"],
  "spending:rounding": ["source rounding", "not applicable", "0"],
  "spending:education_school_part": ["the case's school repricing", "as adopted", "as adopted"],
  "spending:education_other_part": ["the case's college re-key", "as adopted", "as adopted"],
  "spending:correction_constant": ["the case's lane constants", "as adopted", "as adopted"],
};
const oneRule = [];
const usedExplicit = new Set();
for (const [side, evSide] of [["receipt", "receipts"], ["spending", "spending"]]) {
  for (const l of base[0][ENDS[0]].evaluation[evSide]) {
    const x = lineAt(base, evSide, l.id);
    const explicit = EXPLICIT[`${side}:${l.id}`];
    const rule = explicit || CLASS_RULES[`${side}:${x[0].cls}`];
    if (!rule) throw new Error(`[BLOCKED] no rule for ${side} line ${l.id} (class ${x[0].cls})`);
    if (explicit) usedExplicit.add(`${side}:${l.id}`);
    oneRule.push({ side, id: l.id, national_bn: x[0].national, key: x[0].key, group_48_bn: x[0].amount, group_11_bn: x[1].amount,
      response_48: x[0].response, response_11: x[1].response, base: rule[0], scales_with_population: rule[1], rule_response: rule[2],
      effect_48_bn: explicit ? explicit[3][0] : 0, effect_11_bn: explicit ? explicit[3][1] : 0, note: explicit ? explicit[4] : "class default" });
  }
}
const nLines = MODEL.receipts.lines.length + base[0][ENDS[0]].evaluation.spending.length;
gate("the one-rule table carries every line of both sides once, and every named line exists", oneRule.length === nLines
  && new Set(oneRule.map((r) => `${r.side}:${r.id}`)).size === nLines && usedExplicit.size === Object.keys(EXPLICIT).length,
  `${oneRule.length} rows of ${nLines}; ${usedExplicit.size} of ${Object.keys(EXPLICIT).length} named`);
const ruleEffect = [0, 1].map((e) => oneRule.reduce((a, r) => a + (e ? r.effect_11_bn : r.effect_48_bn), 0));
gate("the one-rule table's effects are the items' together (1e-9)", [0, 1].every((e) => near(ruleEffect[e], effects.all[e], 1e-9)),
  `${f4(ruleEffect[0])} / ${f4(ruleEffect[1])}`);

// ---------------------------------------------------------------------------------------------------
if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
const num = (x) => (typeof x === "number" ? f4(x) : x);
const csv = (rows) => rows.map((r) => r.map((x) => { const s = String(num(x)); return /[",]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; }).join(",")).join("\n") + "\n";
fs.writeFileSync(path.join(OUT, "trace.csv"), csv([["line", "national_bn", "key", "response_class", "response_48", "response_11", "group_48_bn", "group_11_bn", "flag"]]
  .concat(trace.map((t) => [t.id, t.national_bn, t.key, t.response_class, t.response_48, t.response_11, t.group_48_bn, t.group_11_bn, t.flag]))));
fs.writeFileSync(path.join(OUT, "items.csv"), csv([["set", "cost_48_bn", "cost_11_bn", "change_48_bn", "change_11_bn", "band_low_bn", "band_high_bn"]]
  .concat([["adopted", baseEnds[0], baseEnds[1], 0, 0, baseBand[0], baseBand[1]]])
  .concat(Object.keys(SETS).map((n) => [n, baseEnds[0] + effects[n][0], baseEnds[1] + effects[n][1], effects[n][0], effects[n][1], bands[n].band[0], bands[n].band[1]]))));
fs.writeFileSync(path.join(OUT, "one_rule.csv"), csv([["side", "line", "national_bn", "key", "group_48_bn", "group_11_bn", "response_48", "response_11", "base",
  "scales_with_population", "rule_response", "effect_48_bn", "effect_11_bn", "note"]].concat(oneRule.map((r) => [r.side, r.id, r.national_bn, r.key, r.group_48_bn, r.group_11_bn,
  r.response_48, r.response_11, r.base, r.scales_with_population, r.rule_response, r.effect_48_bn, r.effect_11_bn, r.note]))));
const round = (x) => (typeof x === "number" ? +x.toFixed(6) : Array.isArray(x) ? x.map(round) : x && typeof x === "object"
  ? Object.fromEntries(Object.entries(x).map(([k, v]) => [k, round(v)])) : x);
const summary = round({
  adopted: { ends_48_11: baseEnds, band: baseBand },
  responses: RESPONSES, tenant_national_bn: TENANT_NATIONAL, keys: KEYS,
  items: Object.fromEntries(Object.keys(SETS).map((n) => [n, { change_48_11: effects[n], ends_48_11: [0, 1].map((e) => baseEnds[e] + effects[n][e]),
    band: bands[n].band }])),
  item1: { flag: FLAG, F: fParts, retention: invariance },
  item4: item4, defense_bound: defenseBound, green_book: GREEN_BOOK,
});
fs.writeFileSync(path.join(OUT, "probe.json"), JSON.stringify(summary, null, 1) + "\n");

console.log("\n[result] cost at 48 / 11, change");
for (const n of ["owner", "owner_low", "owner_high", "owner_short_run", "owner_short_run_market", "owner_capital_tax_view", "tenant",
  "tenant_case_scaled", "personal", "all", "all_low", "all_high"]) {
  console.log(`  ${n.padEnd(20)} ${f4(baseEnds[0] + effects[n][0])} / ${f4(baseEnds[1] + effects[n][1])}   (${f4(effects[n][0])} / ${f4(effects[n][1])})   band ${f4(bands[n].band[0])}–${f4(bands[n].band[1])}`);
}
console.log(`  item 4 beside: use key at 1 ${f4(item4.use_key_at_1_bn[0])} / ${f4(item4.use_key_at_1_bn[1])}; module cell ${f4(item4.module_cell_retention_0_owners_excluded_bn[0])} / ${f4(item4.module_cell_retention_0_owners_excluded_bn[1])}`);
console.log(`  defense bound beside: ${defenseBound.map((d) => `${f4(d.capital_fixed_bn)}–${f4(d.full_adjustment_bn)}`).join(" / ")}`);
console.log("all gates passed");
