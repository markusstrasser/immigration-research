/* Candidate v3, sept28_candidate_v3 (BRIEF.md, 0a83245): gates, then derived/. package.cjs holds the definitions;
 * transit_key.py writes the riders' key it reads, road_congestion.py the congestion item at every lane cut this script
 * looks up, sign_reversal.cjs the sign break-even.
 *
 * Bases, reproduced exactly before anything changes: with every item off, the September 27 case at every specification
 * (its own package and its committed per_spec.csv); with items 1-3 on, candidate v2 (its own package and its committed
 * per_spec.csv). Then each item alone on the September 27 case, gated against its own lane and to move only its named
 * lines, with national totals held:
 *   4.  public housing's capital: the capital lane's variant public_housing_at_rental_assistance_key at every
 *       specification, and v2's reported companion;
 *   5.  long-run property taxes: the receipt-side lane's own evaluation path (items.cjs evaluateWith) at every
 *       specification, its probe.json at 48 / 11, and its two range ends;
 *   6a. the payroll items: the payroll lane's pricing.json (all / central / theta_calibrated; the readings; the
 *       proportional sensitivity, stack_factor_calibrated);
 *   6b. row 2's rule: pricing.json's row2_r_route / without, theta_calibrated less stack_factor_calibrated;
 *   7.  workers' compensation: the formula at every specification, and the ratio against the pandemic lane's own change
 *       on model.json's amounts (the lane priced the September 20 cells; the difference is the case's corrections);
 *   8.  transit: the formula at every specification (deficit and capital), the key as the enterprise key times the
 *       relative use, the enterprise key and every other enterprise component held;
 *   9.  pension accrual (switch): the pension lane's +121.9 / +116.3 on the September 27 case, the social_security line
 *       at the ratio times the group's OASDI receipts and the medicare line at its Part A swap.
 *   10. uninsured use at 0.7x (switch): the uncompensated-care lane's under-charged amounts at 0.7x less at equal use
 *       (its summary.json, the published-figures back-test's frozen consequence) at 48 / 11; the Medicaid line's keys
 *       tied to those amounts, and their 0.7x arms carrying the case's corrections; the Medicaid line alone moving, by
 *       its response times the key change, on the September 27 case and on the candidate.
 * Then the items together (the candidate, each switch off and on), their sum against the joint total, sequential
 * attribution in the brief's order and in reverse, ends and runner-ups over the 32 distinct specifications, public pay,
 * the road arm with congestion, and the outer range on each base (account only and jointly with congestion, the
 * dependent-pieces placement rule), which reproduces the September 27 and v2 ranges before it is read on the candidate.
 * Comparisons are at the fixed specifications 48 and 11, never as a difference of band ends.
 * Run from anywhere, after transit_key.py, uninsured_use_slope.py and road_congestion.py: node main_case.cjs [--out-dir DIR] -> derived/
 * fixed_specs.csv, attribution.csv, candidate_bands.csv, ends.csv, components.csv, per_spec.csv, road_arm.csv,
 * summary.json. Gates exit 1 and nothing is written on failure.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const C = require("./package.cjs");
const V2 = C.V2PKG;
const S = C.SEPT27;
const RS = C.RS;
const { MODEL, HERE, FISCAL, METHODS, ALLOCS, RENTAL, ENTERPRISE_LINE, ROAD_LINE, ROAD_COMPONENTS, ROAD_CASES, LONG_RUN_VARIANTS, ENDS,
  HOUSING_LINE, TAX_LINE, TRANSFERS, HOUSING_SURPLUS, E_NATIONAL, H_NATIONAL, HOUSING_CAPITAL, HOUSING_CAPITAL_VARIANT, PROPERTY_LINES,
  PROPERTY_READINGS, PAY, ROW2, WC, WC_KEY, WC_LINES, TRANSIT_RU, TRANSIT_LINE, TRANSIT_SURPLUS, TRANSIT_CAPITAL, SS_LINE, MEDICARE_LINE,
  ITEMS, SWITCHES, OFF, V2SET, CANDIDATE, ACCRUAL, USE07, MEDICAID_LINE, UC, UC_07, UC_FILE, gateState, gate, near, f2, csvRows, readJson,
  withCentral, specsFor, modelFor, evaluateFull, removalShares, endCuts, endsOf, fixedEnds, distinctSpecs, specKey, rangeComponents, variantRuns,
  oasdiReceipts, pension } = C;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => xs.reduce((a, x) => Math.max(a, Math.abs(x)), 0);
const ex = (x) => x.toExponential(1);
const fx = (x) => x.toFixed(4);
const full = (x) => (typeof x === "number" ? String(x) : x);
// A quantity at the fixed end specifications, each method's value averaged: [spec 48, spec 11].
const atEnds = (f) => ENDS.map((i) => mean(METHODS.map((_, m) => f(m, i))));
const row = (r, side, id) => r.evaluation[side].find((l) => l.id === id);
const keyOf = (r, side, id) => row(r, side, id).amount_bn / row(r, side, id).national_bn;
const withOff = (x) => Object.assign({}, OFF, x);
const withCand = (x) => Object.assign({}, CANDIDATE, x);
const SEPT27_DIR = "main_case_long_run_2026_09_27/derived";
const V2_DIR = "main_case_candidate_v2_2026_09_28/derived";
const s27 = readJson(`${SEPT27_DIR}/summary.json`);
const s2 = readJson(`${V2_DIR}/summary.json`);
const desc = (s) => `${s.allocation}/${s.normalization}/share ${s.share.toFixed(4)}/gg ${s.gg.toFixed(4)}/${s.uc.replace("uninsured_use_", "use ")}/${(100 * s.rate).toFixed(0)}%`;

// Every option set, each method's model, every specification.
function runsOf(o, profile) {
  const oo = withCentral(o);
  const specs = specsFor(oo);
  const models = METHODS.map((meth) => modelFor("central", meth, oo));
  const runs = models.map((m) => specs.map((s) => evaluateFull(m, s, profile)));
  return { specs, models, runs, costs: runs.map((xs) => xs.map((r) => r.cost_bn)), idx: distinctSpecs(specs), keys: specs.map(specKey) };
}
const bandAt = (x, ends) => [0, 1].map((e) => mean(x.runs.map((xs, k) => xs[ends[k][e]].cost_bn)));
const bandOf = (x) => bandAt(x, endsOf(x.specs, x.runs));

// Every line but the named ones keeps its amount, response and effect exactly (lines are matched by id, so a split line
// counts as named or as a failure); the capital components but the named ones keep their return (to tol); P and F are
// unchanged unless production moves.
function onlyMoves(a, b, lines, comps, tol, production) {
  const bad = [];
  for (const side of ["spending", "receipts"]) {
    const A = new Map(a.evaluation[side].map((x) => [x.id, x])), Bm = new Map(b.evaluation[side].map((x) => [x.id, x]));
    for (const id of new Set([...A.keys(), ...Bm.keys()])) {
      if (lines.includes(`${side}:${id}`)) continue;
      const x = A.get(id), y = Bm.get(id);
      if (!x || !y) bad.push(`${side}:${id} (in one run only)`);
      else if (x.amount_bn !== y.amount_bn || x.response !== y.response || x.effect_bn !== y.effect_bn) bad.push(`${side}:${id}`);
    }
  }
  const cb = new Map(b.capital.components.map((c) => [c.id, c]));
  if (a.capital.components.length !== b.capital.components.length) bad.push("capital components");
  for (const c of a.capital.components) {
    const d = cb.get(c.id);
    if (!d) bad.push(`capital:${c.id} (in one run only)`);
    else if (!comps.includes(c.id) && Math.abs(c.return_bn - d.return_bn) > tol) bad.push(`capital:${c.id}`);
  }
  if (!production && (a.evaluation.private_wtp_bn !== b.evaluation.private_wtp_bn || a.evaluation.induced_receipts_bn !== b.evaluation.induced_receipts_bn)) bad.push("production");
  return bad;
}
// National totals of a model's lines, by side and id.
const nationals = (m) => Object.fromEntries(["spending", "receipts"].flatMap((side) => m[side].lines.map((l) => [`${side}:${l.id}`, l.national_bn])));

// ---------------------------------------------------------------------------------------------------
// The candidate's items in the brief's order; with the pension switch last ("switch on"). Item 10, the other switch, is
// read alone and last on each of the two.
const ORDER = ITEMS.filter((it) => !SWITCHES.includes(it.id));
const ON_ORDER = ORDER.concat(ITEMS.filter((it) => it.id === "9"));
const ITEM10 = ITEMS.find((it) => it.id === "10");
const cum = (items) => Object.assign({}, OFF, ...items.map((it) => it.o));
const SETS = { sept27: OFF, v2: V2SET, candidate: CANDIDATE, accrual: ACCRUAL, use07: USE07, use07_accrual: Object.assign({}, ACCRUAL, ITEM10.o) };
for (const it of ITEMS) SETS[`item${it.id}`] = withOff(it.o);
ORDER.forEach((_, j) => { SETS[`fwd_${j}`] = cum(ORDER.slice(0, j + 1)); SETS[`rev_${j}`] = cum(ORDER.slice(j)); });
ON_ORDER.forEach((_, j) => { SETS[`rev_on_${j}`] = cum(ON_ORDER.slice(j)); });
Object.assign(SETS, {
  item4_capital_variant: withOff({ capital_variant: HOUSING_CAPITAL_VARIANT }),
  item5_low: withOff({ property: "long_run", property_reading: "low" }),
  item5_high: withOff({ property: "long_run", property_reading: "high" }),
  item6: withOff({ payroll_items: "central", row2_rule: "within_group" }),
  item6a_proportional: withOff({ payroll_items: "central", payroll_rule: "proportional" }),
  item6a_low_cost: withOff({ payroll_items: "low_cost_central_case" }),
  item6a_high_cost: withOff({ payroll_items: "high_cost_central_case" }),
  item8_deficit_only: withOff({ transit: "state_deficit", transit_capital: false }),
  item8_commuters_deficit_only: withOff({ transit: "commuters", transit_capital: false }),
  candidate_proportional: withCand({ payroll_rule: "proportional", row2_rule: "proportional" }),
  candidate_transit_commuters: withCand({ transit: "commuters" }),
  accrual_on_sept27_v2: Object.assign({}, V2SET, { pension: "accrual" }),
});
for (const t of Object.keys(TRANSIT_RU)) if (t !== "state_deficit") SETS[`item8_${t}`] = withOff({ transit: t });
const PAYS = V2.PUBLIC_PAY;
for (const p of PAYS) { SETS[`pay_${p}`] = withCand({ public_pay: p }); SETS[`v2_pay_${p}`] = Object.assign({}, V2SET, { public_pay: p }); }
const ROAD_MOVES = Object.keys(ROAD_CASES).filter((rc) => rc !== "stationary_network");
for (const rc of ROAD_MOVES) { SETS[`road_${rc}`] = withCand({ road: rc }); SETS[`v2_road_${rc}`] = Object.assign({}, V2SET, { road: rc }); }
const X = Object.fromEntries(Object.entries(SETS).map(([k, o]) => [k, runsOf(o)]));
const diff = (a, b) => X[a].costs.map((xs, m) => xs.map((x, i) => x - X[b].costs[m][i]));
const movesOf = (a, b, lines, comps, tol, production) => X[a].runs.flatMap((xs, m) => xs.map((r, i) => onlyMoves(r, X[b].runs[m][i], lines, comps, tol, production))).flat();
const B = Object.fromEntries(Object.keys(X).map((k) => [k, bandOf(X[k])]));
const E = Object.fromEntries(Object.keys(X).map((k) => [k, endsOf(X[k].specs, X[k].runs)]));
const at4811 = (ends) => ends.every((e) => e[0] === 48 && e[1] === 11);
const fixedChange = (a, b) => atEnds((m, i) => X[a].costs[m][i] - X[b].costs[m][i]);

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the September 27 case and candidate v2]");
const own27 = METHODS.map((meth) => {
  const oo = S.withCentral({});
  const m = S.modelFor("central", meth, oo);
  return S.specsFor(oo).map((s) => S.evaluateFull(m, s).cost_bn);
});
const ownV2 = METHODS.map((meth) => {
  const oo = V2.withCentral(V2.CANDIDATE);
  const m = V2.modelFor("central", meth, oo);
  return V2.specsFor(oo).map((s) => V2.evaluateFull(m, s).cost_bn);
});
const same = (a, b) => a.length === b.length && a.every((xs, m) => xs.length === b[m].length && xs.every((x, i) => x === b[m][i]));
gate("with every item off, v3 is the September 27 case at every specification exactly (its own package, both methods)", same(X.sept27.costs, own27), "2 x 64");
const per27 = csvRows(`${SEPT27_DIR}/per_spec.csv`);
gate("...and its committed per_spec.csv exactly", per27.length === 128 && per27.every((r) =>
  Number(r.cost_bn) === X.sept27.costs[METHODS.indexOf(r.method)][Number(r.spec)]), "128 rows");
gate("the September 27 band and end specifications 48 / 11 (summary.json, 1e-9)", near(B.sept27[0], s27.main_case[0], 1e-9)
  && near(B.sept27[1], s27.main_case[1], 1e-9) && at4811(E.sept27), f2(B.sept27));
gate("with items 1-3 on, v3 is candidate v2 at every specification exactly (its own package, both methods)", same(X.v2.costs, ownV2), "2 x 64");
const perV2 = csvRows(`${V2_DIR}/per_spec.csv`);
gate("...and its committed per_spec.csv exactly (v2 cost at the 32 distinct specifications)", perV2.length === 64 && perV2.every((r) =>
  Number(r.v2_cost_bn) === X.v2.costs[METHODS.indexOf(r.method)][Number(r.spec)]), "64 rows");
gate("candidate v2's band and end specifications 48 / 11 (its summary.json, 1e-9)", near(B.v2[0], s2.candidate_v2[0], 1e-9)
  && near(B.v2[1], s2.candidate_v2[1], 1e-9) && at4811(E.v2), f2(B.v2));

console.log("\n[gates: the specifications]");
const twinOf = (x, i) => x.keys.findIndex((t, j) => j !== i && t === x.keys[i]);
const specsOk = Object.values(X).every((x) => x.idx.length === 32 && x.specs.length === 64
  && x.keys.every((key, i) => { const t = twinOf(x, i); return t >= 0 && x.keys.filter((u) => u === key).length === 2
    && x.costs.every((xs) => xs[i] === xs[t]); })
  && twinOf(x, 48) === 52 && twinOf(x, 11) === 15 && x.idx.includes(48) && x.idx.includes(11));
gate("in every option set the 64 specifications are 32 distinct ones, each twice, identical in every field and in cost; 48 = 52 and 11 = 15",
  specsOk, `${Object.keys(X).length} option sets`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: items 1-3 alone are v2's]");
const v2Fixed = s2.at_fixed_specifications;
for (const [id, key] of [["1", "item1_tenant_key"], ["2", "item2_production_row4"], ["3", "item3_tax_key_irs_2023_raked"]]) {
  const d = fixedChange(`item${id}`, "sept27");
  gate(`item ${id} alone at 48 / 11 is v2's ${key} (its summary.json, 1e-9)`, near(d[0], v2Fixed[key].change[0], 1e-9) && near(d[1], v2Fixed[key].change[1], 1e-9), f2(d));
}

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 4, public housing's capital at the tenant key]");
const d4 = diff("item4", "sept27");
const d4v = worst(METHODS.flatMap((_, m) => d4[m].map((x, i) => x - (X.item4_capital_variant.costs[m][i] - X.sept27.costs[m][i]))));
gate(`item 4 moves the cost as the capital lane's variant ${HOUSING_CAPITAL_VARIANT} does, at every specification (1e-12)`, d4v < 1e-12, `max |diff| ${ex(d4v)}`);
const comp = (r, id) => r.capital.components.find((c) => c.id === id);
const k4 = worst(METHODS.flatMap((_, m) => X.item4.specs.map((s, i) => comp(X.item4.runs[m][i], HOUSING_CAPITAL).key - keyOf(X.item4.runs[m][i], "spending", RENTAL))));
gate("the component's key is the rental line's evaluated key at every specification (1e-15)", k4 < 1e-15, `max |diff| ${ex(k4)}`);
const m4 = movesOf("item4", "sept27", [], [HOUSING_CAPITAL], 0, false);
gate("item 4 moves no line and no other capital component (exactly)", m4.length === 0, m4.slice(0, 5).join(" ") || "exact");
const d4e = atEnds((m, i) => d4[m][i]), cmp4 = v2Fixed.housing_capital_tenant_key_on_sept27.change;
gate("item 4 at 48 / 11 is v2's housing-capital companion on the September 27 case (its summary.json, 1e-9)", near(d4e[0], cmp4[0], 1e-9) && near(d4e[1], cmp4[1], 1e-9), f2(d4e));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 5, long-run property taxes]");
const PROBE = readJson("receipt_side_long_run_2026_09_28/derived/probe.json");
const specs27 = S.specsFor(S.withCentral({}));
const lanePath = (items) => RS.MODELS.map((m0) => { const m = RS.itemModel(m0, items), o = RS.itemOverrides(items);
  return specs27.map((s) => RS.evaluateWith(m, s, o).cost_bn); });
const lane5 = { item5: lanePath(PROPERTY_READINGS.central), item5_low: lanePath(PROPERTY_READINGS.low), item5_high: lanePath(PROPERTY_READINGS.high) };
const g5 = Object.fromEntries(Object.entries(lane5).map(([k, c]) => [k, worst(c.flatMap((xs, m) => xs.map((x, i) => x - X[k].costs[m][i])))]));
gate("item 5 and its two range ends are the receipt-side lane's own evaluation (items.cjs itemModel + itemOverrides + evaluateWith) at every specification (1e-9)",
  Object.values(g5).every((g) => g < 1e-9), Object.entries(g5).map(([k, g]) => `${k} ${ex(g)}`).join(", "));
const d5 = { item5: fixedChange("item5", "sept27"), item5_low: fixedChange("item5_low", "sept27"), item5_high: fixedChange("item5_high", "sept27") };
const probe5 = { item5: PROBE.items.all.change_48_11, item5_low: PROBE.items.all_low.change_48_11, item5_high: PROBE.items.all_high.change_48_11 };
gate("at 48 / 11 they are the lane's probe.json all, all_low and all_high (6-decimal file, 1e-6)",
  Object.keys(d5).every((k) => near(d5[k][0], probe5[k][0], 1e-6) && near(d5[k][1], probe5[k][1], 1e-6)), Object.keys(d5).map((k) => `${k} ${f2(d5[k])}`).join("; "));
const m5 = ["item5", "item5_low", "item5_high"].flatMap((k) => movesOf(k, "sept27", PROPERTY_LINES.map((id) => `receipts:${id}`), [], 0, false));
gate("item 5 moves only the four property lines, no capital component and not production", m5.length === 0, m5.slice(0, 5).join(" ") || "exact");
const nat5 = X.item5.models.every((m, k) => { const a = nationals(X.sept27.models[k]), b = nationals(m);
  return near(b[`receipts:${RS.BUSINESS_LINE}`] + b[`receipts:${RS.TENANT_LINE}`], a[`receipts:${RS.BUSINESS_LINE}`], 1e-9)
    && b[`receipts:${RS.OWNER_LINE}`] === a[`receipts:${RS.OWNER_LINE}`] && b[`receipts:${RS.PERSONAL_LINE}`] === a[`receipts:${RS.PERSONAL_LINE}`]; });
gate("national totals: business property less the tenant line, owner and personal property unchanged (1e-9)", nat5,
  `tenant line $${X.item5.models[0].receipts.lines.find((l) => l.id === RS.TENANT_LINE).national_bn.toFixed(6)}bn`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 6, payroll compliance]");
const PRICING = readJson("payroll_compliance_2026_09_28/derived/pricing.json");
const priced = (item, variant, rule) => { const r = PRICING.rows.find((x) => x.item === item && x.variant === variant && x.rule === rule);
  if (!r) throw new Error(`[BLOCKED] pricing.json has no ${item}/${variant}/${rule}`); return [r.change_48_bn, r.change_11_bn]; };
const lane6 = {
  item6a: priced("all", "central", "theta_calibrated"),
  item6a_low_cost: priced("all", "low_cost_central_case", "theta_calibrated"),
  item6a_high_cost: priced("all", "high_cost_central_case", "theta_calibrated"),
  item6a_proportional: priced("all", "central", "stack_factor_calibrated"),
};
const r2w = priced("row2_r_route", "without", "theta_calibrated"), r2p = priced("row2_r_route", "without", "stack_factor_calibrated");
// Row 2 costs r2w under the within-group rule and r2p under the proportional one (both calibrated removals); the swap is the difference.
lane6.item6b = [r2p[0] - r2w[0], r2p[1] - r2w[1]];
const d6 = Object.fromEntries(Object.keys(lane6).map((k) => [k, fixedChange(k, "sept27")]));
gate("items 6a (and its readings and proportional sensitivity) and 6b at 48 / 11 are the payroll lane's pricing.json (1e-9)",
  Object.keys(lane6).every((k) => near(d6[k][0], lane6[k][0], 1e-9) && near(d6[k][1], lane6[k][1], 1e-9)),
  Object.keys(lane6).map((k) => `${k} ${f2(d6[k])}`).join("; "));
const d6j = fixedChange("item6", "sept27");
gate("6a and 6b together add (both read on the same amounts, 1e-12 at 48 / 11)", near(d6j[0], d6.item6a[0] + d6.item6b[0], 1e-12)
  && near(d6j[1], d6.item6a[1] + d6.item6b[1], 1e-12), f2(d6j));
const lines6a = Object.keys(PAY.items.all.central.lines).map((id) => `receipts:${id}`);
const lines6b = Object.keys(ROW2.without.lines).map((id) => `receipts:${id}`);
const m6 = [...movesOf("item6a", "sept27", lines6a, [], 0, false), ...movesOf("item6b", "sept27", lines6b, [], 0, false)];
gate("6a moves only its receipt lines, 6b only row 2's; no capital component, not production", m6.length === 0, m6.slice(0, 5).join(" ") || "exact");
const nat6 = ["item6a", "item6b", "item6"].every((k) => X[k].models.every((m, j) => { const a = nationals(X.sept27.models[j]), b = nationals(m);
  return Object.keys(a).every((id) => a[id] === b[id]); }));
const cellSum = worst(["item6a", "item6b", "item6"].flatMap((k) => X[k].models.flatMap((m, j) => m.receipts.lines.flatMap((l) => {
  const o = X.sept27.models[j].receipts.lines.find((x) => x.id === l.id);
  return Object.keys(l.cells).flatMap((sc) => ALLOCS.map((al) => l.cells[sc][al].target_bn + l.cells[sc][al].other_bn - o.cells[sc][al].target_bn - o.cells[sc][al].other_bn));
}))));
gate("national totals: every receipt line's national and every executed cell's group + other are unchanged (1e-9)", nat6 && cellSum < 1e-9, `max |diff| ${ex(cellSum)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 7, workers' compensation pooled]");
const d7 = diff("item7", "sept27");
const f7 = worst(METHODS.flatMap((_, m) => X.item7.specs.map((s, i) => d7[m][i] - WC_LINES.reduce((a, id) => {
  const r = row(X.sept27.runs[m][i], "spending", id);
  if (r.key !== WC_KEY) throw new Error(`[BLOCKED] ${id} is evaluated at ${r.key}, not ${WC_KEY}`);
  return a + r.response * (WC[s.allocation].ratio - 1) * r.amount_bn; }, 0))));
gate("item 7 moves the cost by the lines' response x (ratio - 1) x the group's amount at every specification (1e-9)", f7 < 1e-9, `max |diff| ${ex(f7)}`);
const mj = MODEL.spending.lines;
const wcModel = Object.fromEntries(ALLOCS.map((a) => [a, WC_LINES.reduce((s, id) => s + mj.find((l) => l.id === id).keys[WC_KEY][a].target_bn, 0)]));
// ratio_vs_2024.csv prints 10 significant digits, so the comparison is relative, at 1e-8.
const rel8 = (a, b) => Math.abs(a - b) <= 1e-8 * Math.abs(b);
gate("the ratio reproduces the pandemic lane's own change on its amounts, which are model.json's (csv precision, 1e-8 relative)", ALLOCS.every((a) =>
  rel8(WC[a].account_2024_bn, wcModel[a]) && rel8((WC[a].ratio - 1) * WC[a].account_2024_bn, WC[a].account_2024_change_if_pooled_bn)),
  ALLOCS.map((a) => `${a} ${WC[a].ratio.toFixed(6)} x ${WC[a].account_2024_bn.toFixed(4)} -> ${WC[a].account_2024_change_if_pooled_bn.toFixed(4)} ` +
    `(|diff| ${ex(Math.abs(WC[a].account_2024_bn - wcModel[a]))}, ${ex(Math.abs((WC[a].ratio - 1) * WC[a].account_2024_bn - WC[a].account_2024_change_if_pooled_bn))})`).join("; "));
const m7 = movesOf("item7", "sept27", WC_LINES.map((id) => `spending:${id}`), [], 0, false);
gate("item 7 moves only the three workers_comp lines, no capital component, not production", m7.length === 0, m7.slice(0, 5).join(" ") || "exact");
const nat7 = X.item7.models.every((m, j) => { const a = nationals(X.sept27.models[j]), b = nationals(m); return Object.keys(a).every((id) => a[id] === b[id]); });
gate("national totals hold on every line", nat7, "exact");
const wc48 = atEnds((m, i) => WC_LINES.reduce((a, id) => a + row(X.sept27.runs[m][i], "spending", id).amount_bn, 0));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 8, public transit at the riders' key]");
const T8 = TRANSIT_SURPLUS;
const f8 = (k, ru) => { const d = diff(k, "sept27");
  return worst(METHODS.flatMap((_, m) => X[k].specs.map((s, i) => {
    const o = X.sept27.runs[m][i], r = X[k].runs[m][i];
    const e = row(o, "receipts", ENTERPRISE_LINE), t = row(r, "receipts", TRANSIT_LINE);
    const ke = e.amount_bn / e.national_bn;
    const c0 = comp(o, TRANSIT_CAPITAL);
    const capital = s.transit_capital ? c0.stock_charged_bn * s.rate * ke * (ru - 1) * c0.response : 0;
    return d[m][i] - (ke * T8 * (e.response - t.response * ru) + capital);
  }))); };
const f8s = Object.fromEntries([["item8", TRANSIT_RU.state_deficit], ["item8_deficit_only", TRANSIT_RU.state_deficit],
  ["item8_commuters", TRANSIT_RU.commuters], ["item8_commuters_deficit_only", TRANSIT_RU.commuters]].map(([k, ru]) => [k, f8(k, ru)]));
gate("item 8 moves the cost by k_e T (r_e - r_t ru) plus stock x rate x k_e (ru - 1) x response at every specification, capital on and off (1e-9)",
  Object.values(f8s).every((g) => g < 1e-9), Object.entries(f8s).map(([k, g]) => `${k} ${ex(g)}`).join(", "));
const k8 = worst(["item8", "item8_commuters"].flatMap((k) => METHODS.flatMap((_, m) => X[k].specs.flatMap((s, i) => {
  const r = X[k].runs[m][i], o = X.sept27.runs[m][i], ru = TRANSIT_RU[s.transit];
  return [keyOf(r, "receipts", TRANSIT_LINE) - ru * keyOf(o, "receipts", ENTERPRISE_LINE), keyOf(r, "receipts", ENTERPRISE_LINE) - keyOf(o, "receipts", ENTERPRISE_LINE),
    row(r, "receipts", TRANSIT_LINE).response - row(r, "receipts", ENTERPRISE_LINE).response, comp(r, TRANSIT_CAPITAL).key - keyOf(r, "receipts", TRANSIT_LINE)];
}))));
gate("the transit line's key is ru x the enterprise key and the capital's key is the line's; the enterprise key and response hold (1e-15)", k8 < 1e-15, `max |diff| ${ex(k8)}`);
const m8 = movesOf("item8", "sept27", [`receipts:${ENTERPRISE_LINE}`, `receipts:${TRANSIT_LINE}`], [TRANSIT_CAPITAL], 1e-12, false);
gate("item 8 moves only the enterprise and transit receipts and the transit capital (other enterprise components 1e-12)", m8.length === 0, m8.slice(0, 5).join(" ") || "exact");
const nat8 = worst(X.item8.models.flatMap((m, j) => { const a = nationals(X.sept27.models[j]), b = nationals(m);
  return [b[`receipts:${ENTERPRISE_LINE}`] + b[`receipts:${TRANSIT_LINE}`] - a[`receipts:${ENTERPRISE_LINE}`], b[`receipts:${TRANSIT_LINE}`] - T8]; }));
gate("national totals: the enterprise line less the transit line's $66.69bn deficit, the two summing to the old line (1e-9)", nat8 < 1e-9,
  `${ENTERPRISE_LINE} ${E_NATIONAL} -> ${(E_NATIONAL - T8).toFixed(3)}, ${TRANSIT_LINE} ${T8}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 9, pension accrual (switch)]");
const PP = pension();
const d9 = fixedChange("item9", "sept27");
gate(`switched on over the September 27 case it gives the pension lane's change (${PP.file} at ${PP.commit}, central, 1e-6)`,
  near(d9[0], PP.lane_delta_bn[0], 1e-6) && near(d9[1], PP.lane_delta_bn[1], 1e-6), `${f2(d9)} against ${f2(PP.lane_delta_bn)}`);
gate("the lane was priced on this September 27 case (its case_bn, 1e-9)", near(PP.case_bn[0], s27.main_case[0], 1e-9) && near(PP.case_bn[1], s27.main_case[1], 1e-9), f2(PP.case_bn));
const f9 = worst(["item9", "accrual", "accrual_on_sept27_v2"].flatMap((k) => METHODS.flatMap((_, m) => X[k].specs.flatMap((s, i) => {
  const r = X[k].runs[m][i], oasdi = oasdiReceipts(X[k].models[m])[s.allocation];
  const base = X[k === "item9" ? "sept27" : k === "accrual" ? "candidate" : "v2"].runs[m][i];
  const ss = row(r, "spending", SS_LINE), med = row(r, "spending", MEDICARE_LINE), med0 = row(base, "spending", MEDICARE_LINE);
  const rec = (id) => row(r, "receipts", id).amount_bn;
  return [ss.amount_bn - PP.ratio * oasdi, oasdi - (rec("employee_oasdi") + rec("employer_oasdi") + PP.se_oasdi_share * rec("self_employment_oasdi_hi")),
    med.amount_bn - ((1 - PP.part_a_share) * med0.amount_bn + PP.part_a_accrual_bn)];
}))));
gate("social_security = ratio x the group's OASDI receipts (employee + employer + OASDI share of self-employment) and medicare = (1 - Part A share) x cash + Part A accrual, on each base (1e-9)",
  f9 < 1e-9, `ratio ${PP.ratio.toFixed(6)}, Part A accrual $${PP.part_a_accrual_bn.toFixed(4)}bn, max |diff| ${ex(f9)}`);
const m9 = movesOf("item9", "sept27", [`spending:${SS_LINE}`, `spending:${MEDICARE_LINE}`], [], 0, false);
gate("the switch moves only social_security and medicare", m9.length === 0, m9.slice(0, 5).join(" ") || "exact");

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 10, uninsured use at 0.7x (switch)]");
// The lane's arrays run [low, high] by the offset share, as the uc keys do; specification 48 takes the low key, 11 the high.
const UC_ENDS = ["uninsured_use_low", "uninsured_use_high"];
const ucAdd = (use) => UC[`inside_undercharged_bn_use_${use}`];
const lane10 = [0, 1].map((e) => ucAdd("0.7")[e] - ucAdd("1.0")[e]);
const medKeys = (m) => m.spending.lines.find((l) => l.id === MEDICAID_LINE).keys;
const k0 = medKeys(MODEL);
const tie = worst(ALLOCS.flatMap((a) => UC_ENDS.flatMap((k, e) => [k0[k][a].target_bn - k0.medicaid[a].target_bn - ucAdd("1.0")[e],
  k0[UC_07[k]][a].target_bn - k0.medicaid[a].target_bn - ucAdd("0.7")[e]])));
gate(`the Medicaid line's uc keys add the uncompensated-care lane's under-charged amounts, at equal use and at 0.7x (${UC_FILE}, 1e-9)`, tie < 1e-9,
  `equal ${f2(ucAdd("1.0"))}, 0.7x ${f2(ucAdd("0.7"))}; max |diff| ${ex(tie)}`);
const carry = worst(["sept27", "candidate"].flatMap((k) => X[k].models.flatMap((m) => ALLOCS.flatMap((a) => UC_ENDS.map((uc) => {
  const kk = medKeys(m);
  return (kk[UC_07[uc]][a].target_bn - kk[uc][a].target_bn) - (k0[UC_07[uc]][a].target_bn - k0[uc][a].target_bn); })))));
gate("the case's corrections move the 0.7x arms as they move the keys the case uses (September 27 and candidate models, 1e-9)", carry < 1e-9, `max |diff| ${ex(carry)}`);
gate("the switch changes the specification's key, not the model (item 10's models are the September 27 models)",
  X.item10.models.every((m, j) => JSON.stringify(m.spending) === JSON.stringify(X.sept27.models[j].spending)
    && JSON.stringify(m.receipts) === JSON.stringify(X.sept27.models[j].receipts)), "exact");
const d10 = fixedChange("item10", "sept27");
gate("switched on over the September 27 case it gives the lane's 0.7x less equal-use under-charged amount at 48 / 11 (the back-test's frozen consequence, 1e-9)",
  X.sept27.specs[48].uc === UC_ENDS[0] && X.sept27.specs[11].uc === UC_ENDS[1] && near(d10[0], lane10[0], 1e-9) && near(d10[1], lane10[1], 1e-9),
  `${f2(d10)} against ${f2(lane10)}`);
const f10 = worst([["item10", "sept27"], ["use07", "candidate"], ["use07_accrual", "accrual"]].flatMap(([k, b]) => METHODS.flatMap((_, m) => X[k].specs.flatMap((s, i) => {
  const r = row(X[k].runs[m][i], "spending", MEDICAID_LINE), o = row(X[b].runs[m][i], "spending", MEDICAID_LINE);
  return [X[k].costs[m][i] - X[b].costs[m][i] - r.response * (r.amount_bn - o.amount_bn), r.key === UC_07[X[b].specs[i].uc] ? 0 : Infinity];
}))));
gate("at every specification, alone and on the candidate with the pension switch off and on, the cost moves by the Medicaid line's response x its change, at the uc key's 0.7x arm (1e-9)",
  f10 < 1e-9, `max |diff| ${ex(f10)}`);
const m10 = [...movesOf("item10", "sept27", [`spending:${MEDICAID_LINE}`], [], 0, false), ...movesOf("use07", "candidate", [`spending:${MEDICAID_LINE}`], [], 0, false)];
gate("the switch moves only the Medicaid line, no capital component and not production (alone and on the candidate)", m10.length === 0, m10.slice(0, 5).join(" ") || "exact");
const SLOPE_FILE = `${C.LANE}/derived/uninsured_use_slope.json`;
if (!fs.existsSync(path.join(FISCAL, SLOPE_FILE))) {
  console.error(`[BLOCKED] ${SLOPE_FILE} is missing: run uninsured_use_slope.py first`);
  process.exit(1);
}
const SLOPE = readJson(SLOPE_FILE);
gate("uninsured_use_slope.json: all its gates passed, on the back-test's files as they stand (sha256)", Array.isArray(SLOPE.gates) && SLOPE.gates.length > 0
  && SLOPE.gates.every((g) => g.passed) && Object.entries(SLOPE.meta.sources).every(([f, h]) => C.sha256(f) === h), `${SLOPE.gates.length} gates`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the items together]");
const LINES_ALL = [`spending:${RENTAL}`, `receipts:${ENTERPRISE_LINE}`, `receipts:${HOUSING_LINE}`, `receipts:${TAX_LINE}`,
  ...PROPERTY_LINES.map((id) => `receipts:${id}`), ...lines6a, ...lines6b, ...WC_LINES.map((id) => `spending:${id}`), `receipts:${TRANSIT_LINE}`];
const mC = movesOf("candidate", "sept27", LINES_ALL, [HOUSING_CAPITAL, TRANSIT_CAPITAL], 1e-12, true);
gate("the candidate moves only the items' named lines, P and F, and the two re-keyed capital components (others 1e-12)", mC.length === 0, mC.slice(0, 5).join(" ") || "exact");
const mA = movesOf("accrual", "candidate", [`spending:${SS_LINE}`, `spending:${MEDICARE_LINE}`], [], 0, false);
gate("the switch on the candidate moves only social_security and medicare", mA.length === 0, mA.slice(0, 5).join(" ") || "exact");
const natC = worst(X.candidate.models.flatMap((m, j) => { const a = nationals(X.sept27.models[j]), b = nationals(m);
  const split = new Set([`spending:${RENTAL}`, `receipts:${ENTERPRISE_LINE}`, `receipts:${HOUSING_LINE}`, `receipts:${TRANSIT_LINE}`,
    `receipts:${RS.BUSINESS_LINE}`, `receipts:${RS.TENANT_LINE}`]);
  const T = TRANSFERS.public_housing_operating.bn;
  return Object.keys(a).filter((id) => !split.has(id)).map((id) => b[id] - a[id]).concat([
    b[`spending:${RENTAL}`] - (H_NATIONAL - T),
    b[`receipts:${ENTERPRISE_LINE}`] + b[`receipts:${HOUSING_LINE}`] + b[`receipts:${TRANSIT_LINE}`] - (E_NATIONAL - T),
    b[`receipts:${RS.BUSINESS_LINE}`] + b[`receipts:${RS.TENANT_LINE}`] - a[`receipts:${RS.BUSINESS_LINE}`]]); }));
gate("national totals in the candidate: every line as in the September 27 case, the split lines summing to their old lines less the consolidated subsidy (1e-9)",
  natC < 1e-9, `max |diff| ${ex(natC)}`);
const CB = C.central({});
gate("the candidate's per-specification costs give the package's band (central(), 1e-9)", near(CB[0], B.candidate[0], 1e-9) && near(CB[1], B.candidate[1], 1e-9), f2(CB));
gate("the forward and reverse chains end at the candidate (identical option sets)", JSON.stringify(SETS[`fwd_${ORDER.length - 1}`]) === JSON.stringify(withOff(Object.assign({}, ...ORDER.map((it) => it.o))))
  && same(X[`fwd_${ORDER.length - 1}`].costs, X.candidate.costs) && same(X.rev_0.costs, X.candidate.costs) && same(X.rev_on_0.costs, X.accrual.costs), "exact");

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: public pay and the road arm]");
const payOf = (k, m, i) => X[k].runs[m][i].public_pay_bn;
const payGap = worst(PAYS.flatMap((p) => METHODS.flatMap((_, m) => X[`pay_${p}`].specs.map((s, i) => payOf(`pay_${p}`, m, i) - payOf(`v2_pay_${p}`, m, i)))));
const shGap = worst(METHODS.flatMap((_, m) => X.candidate.specs.flatMap((s, i) => { const a = removalShares(X.candidate.runs[m][i].evaluation), b = removalShares(X.v2.runs[m][i].evaluation);
  return [a.low - b.low, a.high - b.high]; })));
gate("the candidate leaves the removal shares and every public-pay reading where v2 has them (1e-12): items 4-9 touch no consumption line", payGap < 1e-12 && shGap < 1e-15,
  `max |diff| pay ${ex(payGap)}, shares ${ex(shGap)}`);
const RC_FILE = `${C.LANE}/derived/road_congestion.json`;
if (!fs.existsSync(path.join(FISCAL, RC_FILE))) {
  console.error(`[BLOCKED] ${RC_FILE} is missing: run road_congestion.py first`);
  process.exit(1);
}
const RC = readJson(RC_FILE);
const pkgFile = `${C.LANE}/package.cjs`;
gate("road_congestion.json: all its gates passed, and it was priced from this package.cjs, its transit key and the pension summary it reads (sha256)",
  Array.isArray(RC.gates) && RC.gates.length > 0 && RC.gates.every((g) => g.passed) && RC.meta.sources[pkgFile] === C.sha256(pkgFile)
  && RC.meta.sources[C.TK_FILE] === C.sha256(C.TK_FILE) && RC.meta.pension_summary.sha256 === PP.sha256 && RC.meta.pension_summary.commit === PP.commit,
  `${RC.gates.length} gates, ${RC.rows.length} cuts`);
const CONG = new Map(RC.rows.map((r) => [r.lane_cut, r]));
const missing = new Set();
const congAt = (cut) => { const r = CONG.get(cut); if (!r) { missing.add(cut); return { congestion_central_bn: NaN }; } return r; };
const roadGaps = ROAD_MOVES.map((rc) => { const a = diff(`road_${rc}`, "candidate"), b = diff(`v2_road_${rc}`, "v2");
  return worst(METHODS.flatMap((_, m) => a[m].map((x, i) => x - b[m][i]))); });
gate("each road case moves the candidate exactly as it moves v2 (every specification, 1e-9): the arm does not interact with items 4-8",
  worst(roadGaps) < 1e-9, ROAD_MOVES.map((rc, k) => `${rc} ${ex(roadGaps[k])}`).join(", "));
const roadSets = V2.ROAD_ARM.map((a) => ({ a, x: a.long_run === "adopted"
  ? (a.road === "stationary_network" ? X.candidate : X[`road_${a.road}`]) : runsOf(withCand({ road: a.road, long_run: a.long_run })) }));
const cut0 = endCuts(X.candidate.specs, X.candidate.runs, fixedEnds(X.candidate.runs));
const cong0 = cut0.map((c) => congAt(c).congestion_central_bn);
const acc0 = atEnds((m, i) => X.candidate.costs[m][i]);
const roadGrid = roadSets.map(({ a, x }) => {
  const cut = endCuts(x.specs, x.runs, fixedEnds(x.runs));
  const cg = cut.map(congAt);
  const acc = atEnds((m, i) => x.costs[m][i]);
  const centralC = cg.map((r) => r.congestion_central_bn);
  return { road_case: a.road, long_run: a.long_run, label: a.long_run === "adopted" ? ROAD_CASES[a.road].label : LONG_RUN_VARIANTS[a.long_run].label,
    lanes: ROAD_CASES[a.road].lanes, lane_cut: cut, account_bn: acc, account_change_bn: [acc[0] - acc0[0], acc[1] - acc0[1]],
    congestion_bn: centralC, congestion_range_bn: cg.map((r) => [r.factorial_min_bn, r.factorial_max_bn]),
    congestion_change_bn: [centralC[0] - cong0[0], centralC[1] - cong0[1]],
    net_change_bn: [acc[0] - acc0[0] + centralC[0] - cong0[0], acc[1] - acc0[1] + centralC[1] - cong0[1]],
    road_return_removed_bn: atEnds((m, i) => x.runs[m][i].road_return_removed_bn), band_bn: bandOf(x), end_specifications: endsOf(x.specs, x.runs) };
});
const v2Grid = s2.road_arm.grid;
const gridGap = worst(roadGrid.flatMap((g) => { const h = v2Grid.find((x) => x.road_case === g.road_case && x.long_run === g.long_run);
  return h ? [g.lane_cut[0] - h.lane_cut[0], g.lane_cut[1] - h.lane_cut[1], g.congestion_bn[0] - h.congestion_bn[0], g.congestion_bn[1] - h.congestion_bn[1],
    g.account_change_bn[0] - h.account_change_bn[0], g.account_change_bn[1] - h.account_change_bn[1]] : [Infinity]; }));
gate("the road arm on the candidate is v2's (lane cuts, congestion and account changes, its summary.json, 1e-9)", gridGap < 1e-9, `${roadGrid.length} rows, max |diff| ${ex(gridGap)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[range]");
// v2's rangeOn, on this package: every component re-run on a base at every specification; account only, and jointly with
// the congestion item at each band end's lane cut (the dependent-pieces placement rule).
function rangeOn(base) {
  const b = variantRuns(base, { o: {}, caseName: "central", methods: METHODS });
  const bEnds = endsOf(b.specs, b.runs);
  const Cb = bandAt(b, bEnds);
  const congB = endCuts(b.specs, b.runs, bEnds).map((c) => congAt(c).congestion_central_bn);
  const comps = rangeComponents().map((cmp) => {
    const devs = cmp.variants.map((variant) => {
      const x = variantRuns(base, variant);
      const ends = endsOf(x.specs, x.runs);
      const band = bandAt(x, ends);
      const cong = endCuts(x.specs, x.runs, ends).map((c) => congAt(c).congestion_central_bn);
      return { v: variant.v, ends, band, d: [band[0] - Cb[0], band[1] - Cb[1]], congestion_change: [cong[0] - congB[0], cong[1] - congB[1]],
        j: [band[0] + cong[0] - Cb[0] - congB[0], band[1] + cong[1] - Cb[1] - congB[1]] };
    });
    const lohi = (f) => ({ lo: [0, 1].map((e) => Math.min(0, ...devs.map((x) => f(x)[e]))), hi: [0, 1].map((e) => Math.max(0, ...devs.map((x) => f(x)[e]))) });
    return Object.assign({ name: cmp.name, label: cmp.label, devs }, lohi((x) => x.d), { joint: lohi((x) => x.j) });
  });
  const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
  const outer = (lo, hi) => {
    const sl = comps.reduce((s, x) => [s[0] + lo(x)[0], s[1] + lo(x)[1]], [0, 0]), sh = comps.reduce((s, x) => [s[0] + hi(x)[0], s[1] + hi(x)[1]], [0, 0]);
    const low_end = [Cb[0] + sl[0], Cb[0] + sh[0]], high_end = [Cb[1] + sl[1], Cb[1] + sh[1]];
    return { low_end, high_end, overall: [low_end[0], high_end[1]], quadrature: [Cb[0] - rss(comps.map((x) => lo(x)[0])), Cb[1] + rss(comps.map((x) => hi(x)[1]))] };
  };
  return Object.assign({ band: Cb, base_ends: bEnds, congestion_at_ends: congB, components: comps },
    outer((x) => x.lo, (x) => x.hi), { joint: outer((x) => x.joint.lo, (x) => x.joint.hi) });
}
const range27 = rangeOn(OFF), rangeV2 = rangeOn(V2SET), rangeC = rangeOn(CANDIDATE), rangeA = rangeOn(ACCRUAL), rangeU = rangeOn(USE07);
const NV2 = V2.rangeComponents().length;
const rangeGap = (r, want) => worst(["low_end", "high_end", "overall", "quadrature"].flatMap((k) => [r[k][0] - want[k][0], r[k][1] - want[k][1]]));
// On a base without the items their components re-run the base itself: zero, up to the joint reading's float cancellation.
const newZero = (r) => r.components.slice(NV2).every((x) => x.devs.every((d) => d.d[0] === 0 && d.d[1] === 0 && Math.abs(d.j[0]) < 1e-12 && Math.abs(d.j[1]) < 1e-12));
const newWorst = (r) => worst(r.components.slice(NV2).flatMap((x) => x.devs.flatMap((d) => [...d.d, ...d.j])));
gate("on the September 27 case v2's components reproduce its published range (1e-9) and this candidate's item components move nothing",
  rangeGap(range27, s27.range) < 1e-9 && s27.components.length === NV2 && range27.components.slice(0, NV2).every((x, k) => x.name === s27.components[k].name) && newZero(range27),
  `${NV2} + ${range27.components.length - NV2} components, max |diff| ${ex(rangeGap(range27, s27.range))}; item components ${ex(newWorst(range27))}`);
const jointGap = (r, want) => worst(["low_end", "high_end", "overall", "quadrature"].flatMap((k) => [r.joint[k][0] - want.joint[k][0], r.joint[k][1] - want.joint[k][1]]));
gate("on v2 they reproduce its published range, account only and jointly with congestion (summary.json range.candidate_v2, 1e-9); the item components move nothing",
  rangeGap(rangeV2, s2.range.candidate_v2) < 1e-9 && jointGap(rangeV2, s2.range.candidate_v2) < 1e-9 && newZero(rangeV2),
  `max |diff| account ${ex(rangeGap(rangeV2, s2.range.candidate_v2))}, joint ${ex(jointGap(rangeV2, s2.range.candidate_v2))}; item components ${ex(newWorst(rangeV2))}`);
gate("the base bands are the option sets' bands (1e-9)", [[range27, B.sept27], [rangeV2, B.v2], [rangeC, B.candidate], [rangeA, B.accrual], [rangeU, B.use07]].every(([r, b]) =>
  near(r.band[0], b[0], 1e-9) && near(r.band[1], b[1], 1e-9)), "5 bases");
gate("every lane cut the range and the road arm need is priced in road_congestion.json", missing.size === 0, missing.size ? `${missing.size} missing` : `${CONG.size} cuts`);

// ---------------------------------------------------------------------------------------------------
if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
// Old -> new at the fixed specifications, each method's value averaged.
const fixed = (key, baseKey) => {
  const o = atEnds((m, i) => X[baseKey || "sept27"].costs[m][i]), n = atEnds((m, i) => X[key].costs[m][i]);
  return { old: o, new: n, change: [n[0] - o[0], n[1] - o[1]] };
};
// The attribution: each item alone on the September 27 case, and in sequence in the brief's order and in reverse, with
// the pension switch off (items 1-8) and on (item 9 last in the order, first in reverse). Item 10 stands outside the
// sums: alone (first in reverse) and last on the candidate, pension switch off and on.
const stepF = (j, sets) => (j === 0 ? fixedChange(sets[0], "sept27") : fixedChange(sets[j], sets[j - 1]));
const fwdSets = ORDER.map((_, j) => `fwd_${j}`), revSets = ORDER.map((_, j) => `rev_${j}`), revOnSets = ON_ORDER.map((_, j) => `rev_on_${j}`);
const attribution = ON_ORDER.map((it, j) => {
  const alone = fixedChange(`item${it.id}`, "sept27");
  const on = j === ORDER.length ? fixedChange("accrual", "candidate") : stepF(j, fwdSets);
  const rev = j < ORDER.length ? (j === ORDER.length - 1 ? fixedChange(revSets[j], "sept27") : fixedChange(revSets[j], revSets[j + 1])) : null;
  const revOn = j === ON_ORDER.length - 1 ? fixedChange(revOnSets[j], "sept27") : fixedChange(revOnSets[j], revOnSets[j + 1]);
  return { id: it.id, name: it.name, alone, forward: j < ORDER.length ? on : null, reverse: rev, forward_on: on, reverse_on: revOn };
});
const sumOf = (f, n) => [0, 1].map((e) => attribution.slice(0, n).reduce((s, a) => s + f(a)[e], 0));
const joint = fixedChange("candidate", "sept27"), jointOn = fixedChange("accrual", "sept27");
const sums = { alone_off: sumOf((a) => a.alone, ORDER.length), alone_on: sumOf((a) => a.alone, ON_ORDER.length),
  forward_off: sumOf((a) => a.forward, ORDER.length), reverse_off: sumOf((a) => a.reverse, ORDER.length),
  forward_on: sumOf((a) => a.forward_on, ON_ORDER.length), reverse_on: sumOf((a) => a.reverse_on, ON_ORDER.length) };
const alone10 = fixedChange("item10", "sept27");
const attr10 = { id: ITEM10.id, name: ITEM10.name, alone: alone10, forward: fixedChange("use07", "candidate"), reverse: alone10,
  forward_on: fixedChange("use07_accrual", "accrual"), reverse_on: alone10 };
const joint10 = fixedChange("use07", "sept27"), joint10On = fixedChange("use07_accrual", "sept27");
const chainGap = worst([...[0, 1].map((e) => sums.forward_off[e] - joint[e]), ...[0, 1].map((e) => sums.reverse_off[e] - joint[e]),
  ...[0, 1].map((e) => sums.forward_on[e] - jointOn[e]), ...[0, 1].map((e) => sums.reverse_on[e] - jointOn[e])]);
if (chainGap > 1e-9) { console.error(`[BLOCKED] the sequential steps do not add to the joint change (${ex(chainGap)})`); process.exit(1); }

const FIXED = [
  ...ITEMS.map((it) => [`item${it.id}`, `${it.id}. ${it.name}, alone`, fixed(`item${it.id}`), SWITCHES.includes(it.id) ? "switch" : "candidate item"]),
  ["candidate_switch_off", "the candidate: items 1-8 (pension switch off, cash)", fixed("candidate"), "candidate"],
  ["candidate_switch_on", "the candidate with the pension switch on (accrual)", fixed("accrual"), "candidate"],
  ["candidate_use07", "the candidate with the uninsured-use switch on (0.7x), pension switch off", fixed("use07"), "candidate"],
  ["candidate_use07_accrual", "the candidate with both switches on", fixed("use07_accrual"), "candidate"],
  ["item10_on_candidate", "10 on the candidate (change from it)", fixed("use07", "candidate"), "switch"],
  ["item10_on_accrual", "10 on the candidate with the pension switch on (change from it)", fixed("use07_accrual", "accrual"), "switch"],
  ["candidate_v2", "candidate v2 (items 1-3)", fixed("v2"), "reference"],
  ["item6_both_parts", "6a + 6b together, alone", fixed("item6"), "candidate item"],
  ["item6a_proportional_rule", "6a under the payroll lane's proportional rule (r_cal_raw), row 2 as in the case: the sensitivity", fixed("item6a_proportional"), "sensitivity"],
  ["item6a_low_cost_readings", "6a at the lane's low-cost readings (row 2 central)", fixed("item6a_low_cost"), "range variant"],
  ["item6a_high_cost_readings", "6a at the lane's high-cost readings (row 2 central)", fixed("item6a_high_cost"), "range variant"],
  ["candidate_proportional_rule", "the candidate with item 6 under the proportional rule (6a at r_cal_raw, 6b off; change from the candidate)", fixed("candidate_proportional", "candidate"), "sensitivity"],
  ["item5_low", "5 at the receipt-side lane's low responses", fixed("item5_low"), "range variant"],
  ["item5_high", "5 at 1 everywhere with the case-scaled tenant national", fixed("item5_high"), "range variant"],
  ["item4_capital_lane_variant", "4 through the capital lane's variant (the gate's reference)", fixed("item4_capital_variant"), "reference"],
  ["item8_deficit_only", "8, the deficit alone (capital at the enterprise key)", fixed("item8_deficit_only"), "part"],
  ...Object.keys(TRANSIT_RU).filter((t) => t !== "state_deficit").map((t) => [`item8_${t}`, `8 at the ${t.replace(/_/g, " ")} key (${TRANSIT_RU[t].toFixed(4)})`, fixed(`item8_${t}`), "range variant"]),
  ["item8_commuters_deficit_only", "8 at the commuters key, the deficit alone: the brief's estimate", fixed("item8_commuters_deficit_only"), "brief's estimate"],
  ["candidate_transit_commuters", "the candidate with transit at the commuters key (change from the candidate)", fixed("candidate_transit_commuters", "candidate"), "range variant"],
  ["accrual_on_v2", "the pension switch on v2 (change from v2)", fixed("accrual_on_sept27_v2", "v2"), "switch"],
  ...PAYS.map((p) => [`public_pay_${p}`, `public pay, ${p.replace(/_/g, " ")}, on the candidate (change from it)`, fixed(`pay_${p}`, "candidate"), "beside"]),
  ...ROAD_MOVES.map((rc) => [`road_${rc}`, `road arm, ${ROAD_CASES[rc].label} (account only; change from the candidate)`, fixed(`road_${rc}`, "candidate"), "beside"]),
];
const fixedCsv = ["item,label,placement,old_spec48_bn,new_spec48_bn,change_spec48_bn,old_spec11_bn,new_spec11_bn,change_spec11_bn"]
  .concat(FIXED.map(([k, label, v, place]) => [k, `"${label}"`, place, fx(v.old[0]), fx(v.new[0]), fx(v.change[0]), fx(v.old[1]), fx(v.new[1]), fx(v.change[1])].join(",")));
const pair = (x) => (x ? [fx(x[0]), fx(x[1])] : ["", ""]);
const attrCsv = ["item,label,alone_spec48_bn,alone_spec11_bn,forward_spec48_bn,forward_spec11_bn,reverse_spec48_bn,reverse_spec11_bn,forward_on_spec48_bn,forward_on_spec11_bn,reverse_on_spec48_bn,reverse_on_spec11_bn"]
  .concat(attribution.map((a) => [a.id, `"${a.name}"`, ...pair(a.alone), ...pair(a.forward), ...pair(a.reverse), ...pair(a.forward_on), ...pair(a.reverse_on)].join(",")))
  .concat([["sum", "\"sum of the steps\"", ...pair(sums.alone_off), ...pair(sums.forward_off), ...pair(sums.reverse_off), ...pair(sums.forward_on), ...pair(sums.reverse_on)].join(","),
    ["sum_with_switch", "\"sum of the items alone, switch included\"", ...pair(sums.alone_on), "", "", "", "", "", "", "", ""].join(","),
    ["joint", "\"the joint change (switch off; switch on)\"", ...pair(joint), ...pair(joint), ...pair(joint), ...pair(jointOn), ...pair(jointOn)].join(","),
    [attr10.id, `"${attr10.name}: outside the sums; forward = last on the candidate, reverse = alone"`, ...pair(attr10.alone), ...pair(attr10.forward),
      ...pair(attr10.reverse), ...pair(attr10.forward_on), ...pair(attr10.reverse_on)].join(","),
    ["joint_with_10", "\"the joint change with item 10 (pension switch off; on)\"", "", "", ...pair(joint10), ...pair(joint10), ...pair(joint10On), ...pair(joint10On)].join(",")]);

// Ends and runner-ups over the 32 distinct specifications.
const ENDS_OF = ["sept27", "v2", "candidate", "accrual", "use07", "use07_accrual", ...ITEMS.map((it) => `item${it.id}`), "candidate_proportional", "candidate_transit_commuters",
  ...PAYS.map((p) => `pay_${p}`), ...ROAD_MOVES.map((rc) => `road_${rc}`)];
const endRows = ENDS_OF.flatMap((k) => METHODS.map((meth, m) => {
  const x = X[k], c = x.costs[m];
  const up = x.idx.slice().sort((a, b) => c[a] - c[b] || a - b), down = x.idx.slice().sort((a, b) => c[b] - c[a] || a - b);
  return { set: k, method: meth, low: up[0], low_cost: c[up[0]], low_runner_up: up[1], low_margin: c[up[1]] - c[up[0]],
    high: down[0], high_cost: c[down[0]], high_runner_up: down[1], high_margin: c[down[0]] - c[down[1]],
    low_desc: desc(x.specs[up[0]]), low_runner_up_desc: desc(x.specs[up[1]]), high_desc: desc(x.specs[down[0]]), high_runner_up_desc: desc(x.specs[down[1]]),
    low_twin: twinOf(x, up[0]), high_twin: twinOf(x, down[0]) };
}));
const endsCsv = ["set,method,low_spec,low_twin,low_spec_fields,low_cost_bn,low_runner_up,low_runner_up_fields,low_margin_bn,high_spec,high_twin,high_spec_fields,high_cost_bn,high_runner_up,high_runner_up_fields,high_margin_bn"]
  .concat(endRows.map((r) => [r.set, r.method, r.low, r.low_twin, `"${r.low_desc}"`, fx(r.low_cost), r.low_runner_up, `"${r.low_runner_up_desc}"`, fx(r.low_margin),
    r.high, r.high_twin, `"${r.high_desc}"`, fx(r.high_cost), r.high_runner_up, `"${r.high_runner_up_desc}"`, fx(r.high_margin)].join(",")));

// The federal transit operating subsidy crossing (v2's crossings.csv): $ million per $1bn paid from other_subsidies into
// the transit surplus, at the evaluated keys and responses.
const perBn = (k, rec) => atEnds((m, i) => { const r = X[k].runs[m][i], a = row(r, "spending", "other_subsidies"), b = row(r, "receipts", rec);
  return 1000 * (a.response * a.amount_bn / a.national_bn - b.response * b.amount_bn / b.national_bn); });
const crossing = { transfer: "federal operating subsidies to S&L mass transit (NIPA 3.13 line 7, federal 'Other'; unpublished transit part)",
  sept27_m_per_bn: perBn("sept27", ENTERPRISE_LINE), candidate_m_per_bn: perBn("candidate", TRANSIT_LINE),
  status: "still crosses: the paying leg is a business subsidy at response 0; the receiving leg is now the transit line at the riders' key and response 1" };

const roadCsv = ["road_case,long_run_variant,lanes,lane_cut_spec48,lane_cut_spec11,account_spec48_bn,account_spec11_bn,account_change_spec48_bn,account_change_spec11_bn,"
  + "congestion_spec48_bn,congestion_spec11_bn,congestion_change_spec48_bn,congestion_change_spec11_bn,net_change_spec48_bn,net_change_spec11_bn,"
  + "congestion_spec48_min_bn,congestion_spec48_max_bn,congestion_spec11_min_bn,congestion_spec11_max_bn,road_return_removed_spec48_bn,road_return_removed_spec11_bn,band_low_bn,band_high_bn,end_specifications"]
  .concat(roadGrid.map((g) => [g.road_case, g.long_run, `"${g.lanes}"`, g.lane_cut[0].toFixed(8), g.lane_cut[1].toFixed(8)].concat([...g.account_bn, ...g.account_change_bn,
    ...g.congestion_bn, ...g.congestion_change_bn, ...g.net_change_bn, ...g.congestion_range_bn[0], ...g.congestion_range_bn[1], ...g.road_return_removed_bn, ...g.band_bn].map(fx),
    [`"${g.end_specifications.map((e) => e.join("/")).join(" ")}"`]).join(",")));

const RANGES = [["candidate", rangeC], ["accrual", rangeA], ["v2", rangeV2], ["sept27", range27], ["use07", rangeU]];
const compCsv = ["component,label," + RANGES.map(([n]) => ["low_end_lo", "low_end_hi", "high_end_lo", "high_end_hi", "joint_low_end_lo", "joint_low_end_hi", "joint_high_end_lo", "joint_high_end_hi"]
  .map((c) => `${n}_${c}`).join(",")).join(",")]
  .concat(rangeC.components.map((x, k) => [x.name, `"${x.label}"`, ...RANGES.flatMap(([, r]) => { const c = r.components[k];
    return [c.lo[0], c.hi[0], c.lo[1], c.hi[1], c.joint.lo[0], c.joint.hi[0], c.joint.lo[1], c.joint.hi[1]].map(fx); })].join(",")));

const bandsRows = [
  ["sept27_case", "the September 27 case (adopted)", B.sept27, range27],
  ["candidate_v2", "candidate v2: items 1-3", B.v2, rangeV2],
  ["candidate_v3_cash", "candidate v3: items 1-8, pension switch off (cash)", B.candidate, rangeC],
  ["candidate_v3_accrual", "candidate v3 with the pension switch on (accrual)", B.accrual, rangeA],
  ["candidate_v3_use07", "candidate v3 with the uninsured-use switch on (0.7x), pension switch off", B.use07, rangeU],
  ["candidate_v3_use07_accrual", "candidate v3 with both switches on", B.use07_accrual],
  ...ITEMS.map((it) => [`item${it.id}_alone`, `item ${it.id} alone`, B[`item${it.id}`]]),
  ["candidate_proportional_rule", "the candidate, item 6 under the proportional rule (sensitivity)", B.candidate_proportional],
  ["candidate_transit_commuters", "the candidate, transit at the commuters key (range variant)", B.candidate_transit_commuters],
  ...PAYS.map((p) => [`candidate_public_pay_${p}`, `the candidate with public pay, ${p.replace(/_/g, " ")} (beside)`, B[`pay_${p}`]]),
  ...ROAD_MOVES.map((rc) => [`candidate_road_${rc}`, `the candidate, road arm at ${rc.replace(/_/g, " ")}, account only (beside)`, B[`road_${rc}`]]),
];
const bandsCsv = ["case,label,cost_low_bn,cost_high_bn,outer_account_low_bn,outer_account_high_bn,outer_joint_low_bn,outer_joint_high_bn,"
  + "quadrature_account_low_bn,quadrature_account_high_bn,quadrature_joint_low_bn,quadrature_joint_high_bn"]
  .concat(bandsRows.map(([k, label, b, r]) => [k, `"${label}"`, fx(b[0]), fx(b[1])].concat(r
    ? [r.overall[0], r.overall[1], r.joint.overall[0], r.joint.overall[1], r.quadrature[0], r.quadrature[1], r.joint.quadrature[0], r.joint.quadrature[1]].map(fx)
    : ["", "", "", "", "", "", "", ""]).join(",")));

const perHead = ["method", "spec", "twin", "allocation", "normalization", "share", "reading", "gg", "uc", "rate", "sept27_cost_bn", "v2_cost_bn",
  "v3_cash_cost_bn", "v3_accrual_cost_bn", "v3_use07_cost_bn", ...ITEMS.map((it) => `item${it.id}_bn`), "enterprise_key", "transit_key", "rental_key", "housing_capital_key",
  "transit_capital_bn", "group_oasdi_receipts_bn", "social_security_cash_bn", "social_security_accrual_bn", "medicare_cash_bn", "medicare_accrual_bn",
  "medicaid_equal_use_bn", "medicaid_use07_bn"];
const dItem = Object.fromEntries(ITEMS.map((it) => [it.id, diff(`item${it.id}`, "sept27")]));
const perSpec = [perHead.join(",")].concat(METHODS.flatMap((meth, m) => X.candidate.idx.map((i) => {
  const s = X.candidate.specs[i], r = X.candidate.runs[m][i], a = X.accrual.runs[m][i], u = X.use07.runs[m][i];
  return [meth, i, twinOf(X.candidate, i), s.allocation, s.normalization, s.share, s.reading, s.gg, s.uc, s.rate, X.sept27.costs[m][i], X.v2.costs[m][i],
    X.candidate.costs[m][i], X.accrual.costs[m][i], X.use07.costs[m][i], ...ITEMS.map((it) => dItem[it.id][m][i]), keyOf(r, "receipts", ENTERPRISE_LINE),
    keyOf(r, "receipts", TRANSIT_LINE), keyOf(r, "spending", RENTAL), comp(r, HOUSING_CAPITAL).key, comp(r, TRANSIT_CAPITAL).return_bn,
    oasdiReceipts(X.candidate.models[m])[s.allocation], row(r, "spending", SS_LINE).amount_bn, row(a, "spending", SS_LINE).amount_bn,
    row(r, "spending", MEDICARE_LINE).amount_bn, row(a, "spending", MEDICARE_LINE).amount_bn, row(r, "spending", MEDICAID_LINE).amount_bn,
    row(u, "spending", MEDICAID_LINE).amount_bn].map(full).join(",");
})));

const compOut = (r) => r.components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi, joint_lo: x.joint.lo, joint_hi: x.joint.hi,
  variants: Object.fromEntries(x.devs.map((d) => [d.v, { account_bn: d.d, joint_bn: d.j, congestion_change_bn: d.congestion_change,
    end_specifications: d.ends.map((e) => e.join("/")).join(" ") }])) }));
const rangeOut = (r) => ({ band: r.band, low_end: r.low_end, high_end: r.high_end, overall: r.overall, quadrature: r.quadrature,
  congestion_at_band_ends_bn: r.congestion_at_ends, joint: r.joint });
const inputs = [C.TK_FILE, RC_FILE, C.PAYROLL_FILE, "payroll_compliance_2026_09_28/derived/pricing.json", C.WC_FILE,
  "receipt_side_long_run_2026_09_28/items.cjs", "receipt_side_long_run_2026_09_28/derived/housing.json", "receipt_side_long_run_2026_09_28/derived/probe.json",
  C.ESV_FILE, C.TAX_FILE, C.STOCK_FILE, `${SEPT27_DIR}/summary.json`, `${SEPT27_DIR}/per_spec.csv`, `${V2_DIR}/summary.json`, `${V2_DIR}/per_spec.csv`,
  pkgFile, "main_case_candidate_v2_2026_09_28/package.cjs", "main_case_candidate_2026_09_28/package.cjs", "main_case_long_run_2026_09_27/package.cjs",
  UC_FILE, SLOPE_FILE, ...Object.keys(SLOPE.meta.sources)];
const DEF = PROBE.defense_bound[0];
const summary = {
  lane: C.LANE, case: C.CASE, status: "candidate, not adopted (BRIEF.md, 0a83245)",
  imports: "main_case_candidate_v2_2026_09_28/package.cjs (08d9a86), which imports the first candidate and main_case_long_run_2026_09_27/package.cjs; none edited",
  sept27_case: B.sept27, candidate_v2: B.v2, candidate_v3_cash: B.candidate, candidate_v3_accrual: B.accrual,
  candidate_v3_use07: B.use07, candidate_v3_use07_accrual: B.use07_accrual,
  end_specifications: { candidate_v3_cash: E.candidate, candidate_v3_accrual: E.accrual, candidate_v3_use07: E.use07, candidate_v3_use07_accrual: E.use07_accrual },
  at_fixed_specifications: Object.fromEntries(FIXED.map(([k, label, v, place]) => [k, Object.assign({ label, placement: place }, v)])),
  attribution: { items: attribution, sums, joint_off: joint, joint_on: jointOn,
    interaction_off_bn: [joint[0] - sums.alone_off[0], joint[1] - sums.alone_off[1]], interaction_on_bn: [jointOn[0] - sums.alone_on[0], jointOn[1] - sums.alone_on[1]],
    item10: attr10, joint_with_item10_off: joint10, joint_with_item10_on: joint10On,
    item10_interaction_bn: { off: [0, 1].map((e) => attr10.forward[e] - attr10.alone[e]), on: [0, 1].map((e) => attr10.forward_on[e] - attr10.alone[e]) } },
  item4: { component: HOUSING_CAPITAL, key_rule: C.HOUSING_CAPITAL_KEY, capital_lane_variant: HOUSING_CAPITAL_VARIANT },
  item5: { readings: PROPERTY_READINGS, lane_probe_48_11: probe5 },
  item6: { ratios_file: C.PAYROLL_FILE, fields: C.PAYROLL_FIELDS, lane_pricing_48_11: lane6 },
  item7: { ratio: Object.fromEntries(ALLOCS.map((a) => [a, WC[a].ratio])), lines: WC_LINES, lane_change_on_model_json_bn: Object.fromEntries(ALLOCS.map((a) => [a, WC[a].account_2024_change_if_pooled_bn])),
    lane_amount_model_json_bn: wcModel, case_amount_at_fixed_specs_bn: wc48 },
  item8: { relative_use: TRANSIT_RU, transit_surplus_bn: T8, capital_component: TRANSIT_CAPITAL, key_file: C.TK_FILE, crossing },
  item9: { file: PP.file, commit: PP.commit, sha256: PP.sha256, ratio: PP.ratio, part_a_accrual_bn: PP.part_a_accrual_bn, part_a_share: PP.part_a_share,
    se_oasdi_share: PP.se_oasdi_share, central: PP.central, lane_delta_bn: PP.lane_delta_bn,
    unpriced: "interest on the group's existing (already accrued) pension liability: the switch replaces cash with the normal cost only (the lane's RESULT, 'Interest on the group's existing pension liability is not charged')" },
  item10: { line: MEDICAID_LINE, keys: UC_07, file: UC_FILE, sha256: C.sha256(UC_FILE),
    undercharged_bn: { equal_use: ucAdd("1.0"), use_07: ucAdd("0.7") }, lane_change_48_11_bn: lane10,
    evidence: { backtest: "backtest_published_2026_09_28 (340c8a6), check 3: CMS S-10 FY2023", slope_file: SLOPE_FILE, fits: SLOPE.fits } },
  defense: { response: 0, gdp_share_bound_bn: [DEF.capital_fixed_bn, DEF.full_adjustment_bn], source: "receipt_side_long_run_2026_09_28/derived/probe.json defense_bound (FAQ 2)" },
  public_pay: { at_fixed_specs_bn: Object.fromEntries(PAYS.map((p) => [p, atEnds((m, i) => payOf(`pay_${p}`, m, i))])), bands_bn: Object.fromEntries(PAYS.map((p) => [p, B[`pay_${p}`]])) },
  road_arm: { grid: roadGrid, stationary_congestion_bn: cong0, b1_lanes_fixed_bn: RC.b1_lanes_fixed_bn },
  ends: endRows,
  range: { candidate_v3_cash: rangeOut(rangeC), candidate_v3_accrual: rangeOut(rangeA), candidate_v2: rangeOut(rangeV2), sept27: rangeOut(range27),
    candidate_v3_use07: rangeOut(rangeU),
    note: "account: v2's components plus the items' ranges, re-run on each base at every specification; joint: each variant's change in the account plus the congestion item at its band ends' lane cut (the dependent-pieces placement rule)" },
  components: { candidate_v3_cash: compOut(rangeC), candidate_v3_accrual: compOut(rangeA), candidate_v2: compOut(rangeV2), sept27: compOut(range27),
    candidate_v3_use07: compOut(rangeU) },
  specifications: { total: 64, distinct: 32, twins: "48 = 52 and 11 = 15" },
  inputs: Object.fromEntries(inputs.map((f) => [f, C.sha256(f)])),
};
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "fixed_specs.csv"), fixedCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "attribution.csv"), attrCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "candidate_bands.csv"), bandsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "ends.csv"), endsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "components.csv"), compCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "road_arm.csv"), roadCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");

console.log("\n[result]");
for (const [k, , b, r] of bandsRows.slice(0, 5)) console.log(`  ${k.padEnd(24)} ${f2(b)}   outer ${f2(r.overall)}, joint ${f2(r.joint.overall)}, quadrature ${f2(r.quadrature)}`);
for (const [k, , v] of FIXED) console.log(`    ${k.padEnd(36)} 48: ${fx(v.old[0])} -> ${fx(v.new[0])} (${v.change[0] >= 0 ? "+" : ""}${fx(v.change[0])})   11: ${fx(v.old[1])} -> ${fx(v.new[1])} (${v.change[1] >= 0 ? "+" : ""}${fx(v.change[1])})`);
for (const a of attribution) console.log(`  item ${a.id.padEnd(3)} alone ${f2(a.alone)}  fwd ${a.forward ? f2(a.forward) : "-"}  rev ${a.reverse ? f2(a.reverse) : "-"}  fwd(on) ${f2(a.forward_on)}  rev(on) ${f2(a.reverse_on)}`);
console.log(`  sum alone ${f2(sums.alone_off)} vs joint ${f2(joint)}; with switch ${f2(sums.alone_on)} vs ${f2(jointOn)}`);
console.log(`  item 10  alone ${f2(attr10.alone)}  on the candidate ${f2(attr10.forward)}  with the pension switch ${f2(attr10.forward_on)}; joint with 10 ${f2(joint10)} / ${f2(joint10On)}`);
for (const r of endRows.filter((z) => ["candidate", "accrual", "use07", "use07_accrual"].includes(z.set))) console.log(`  ends ${r.set.padEnd(13)} ${r.method.padEnd(24)} low ${r.low} (next ${r.low_runner_up} +${fx(r.low_margin)}), high ${r.high} (next ${r.high_runner_up} -${fx(r.high_margin)})`);
console.log(`  crossing (transit subsidy) ${crossing.sept27_m_per_bn.map((v) => v.toFixed(2)).join(" / ")} -> ${crossing.candidate_m_per_bn.map((v) => v.toFixed(2)).join(" / ")} $m per $1bn`);
console.log("all gates passed");
