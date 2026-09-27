/* Candidate v2, sept28_candidate_v2 (BRIEF.md, 08b1b7d): gates, then derived/. package.cjs holds the definitions;
 * road_stock.py writes the construction slopes the upward road cases read, road_congestion.py the congestion item at
 * every lane cut this script looks up.
 *
 * Bases, reproduced exactly before anything changes: the September 27 case (main_case_long_run_2026_09_27,
 * $321.8194–387.3701bn, end specifications 48 / 11) and the first candidate (main_case_candidate_2026_09_28, c313b53,
 * $323.6827–388.6981bn), each at every specification against its committed per_spec.csv. Then each item alone on the
 * September 27 case, each gated to move only its named lines by exactly its own amount:
 *   1. public housing's deficit keyed by its tenants: housing_subsidies, enterprise_surplus and the new
 *      housing_enterprise_surplus alone move, by r_e ke H - r_x kx (H - T) - r_h kh T, which is (ke - kh) H with every
 *      response at 1; the consolidation of T moves nothing under this key; the first candidate's population-key reading
 *      is reported beside;
 *   2. production on the row-4 weights: no line moves; the cost moves by minus the change in P + F;
 *   3. the IRS-matched income-tax key: federal_income_tax alone moves, by the tax lane's own per-method change.
 * The items add exactly. The internal-transfer controls: today a $1bn transfer moves the case by kh - ke; on v2 by 0,
 * and by (r_x - r_h) kh when the two legs' responses differ (so the v2 test is not an identity); the first candidate's
 * after-gate holds on the population key too, so it is kept as a unit test of its two helpers.
 * Beside the range: public pay on the account's own counterfactual workforce, the road arm (replacement, a fixed stock
 * and the two upward construction cases, each with the congestion item at its lane cut) and the housing capital at the
 * tenant key. An independent path (engine, model.json, the September 27 corrections.json, the NIPA 3.8 housing line, T,
 * the row-4 grid and the tax lane's own per-method change) gives v2 at every specification.
 * The outer range re-runs the September 27 components on each base; every component is also read jointly with the
 * congestion item at its band ends' lane cut (the dependent-pieces placement rule).
 * Statistics across specifications use the 32 distinct specifications (48 = 52 and 11 = 15 in every field).
 * Comparisons are at the fixed specifications 48 and 11, never as a difference of band ends.
 * Run from anywhere, after road_stock.py and road_congestion.py: node main_case.cjs [--out-dir DIR] -> derived/
 * fixed_specs.csv, candidate_bands.csv, ends.csv, components.csv, per_spec.csv, road_arm.csv, crossings.csv, summary.json.
 * Gates exit 1 and nothing is written on failure.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const C = require("./package.cjs");
const C1 = C.V1PKG;
const S = C.SEPT27;
const { MODEL, HERE, FISCAL, METHODS, ALLOCS, RENTAL, ENTERPRISE_LINE, ROAD_LINE, ROAD_COMPONENTS, ROAD_CASES, LONG_RUN_VARIANTS,
  TRANSFERS, PROD, HOUSING_SURPLUS, E_NATIONAL, H_NATIONAL, HOUSING_LINE, TAX, TAX_KEYS, TAX_LINE, STOCK, ROAD_ARM, ENDS,
  CANDIDATE, OFF, V1, gateState, gate, near, f2, csvRows, readJson, withCentral, specsFor, modelFor, evaluateFull,
  withHousingTransfer, taxEditOf, removalShares, endCuts, endsOf, fixedEnds, distinctSpecs, specKey, rangeComponents,
  variantRuns, publicPayOf, withProduction, consolidate, withSyntheticTransfer } = C;
const Engine = C.Engine;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => xs.reduce((a, x) => Math.max(a, Math.abs(x)), 0);
const ex = (x) => x.toExponential(1);
const fx = (x) => x.toFixed(4);
const r2 = (x) => Math.round(x * 100) / 100;
const full = (x) => (typeof x === "number" ? String(x) : x);
// A quantity at the fixed end specifications, each method's value averaged: [spec 48, spec 11].
const atEnds = (f) => ENDS.map((i) => mean(METHODS.map((_, m) => f(m, i))));
const row = (r, side, id) => r.evaluation[side].find((l) => l.id === id);
const keyOf = (r, side, id) => row(r, side, id).amount_bn / row(r, side, id).national_bn;
const withOff = (x) => Object.assign({}, OFF, x);
const withCand = (x) => Object.assign({}, CANDIDATE, x);
const withV1 = (x) => Object.assign({}, V1, x);
const SEPT27_DIR = "main_case_long_run_2026_09_27/derived";
const V1_DIR = "main_case_candidate_2026_09_28/derived";
const s27 = readJson(`${SEPT27_DIR}/summary.json`);
const s1 = readJson(`${V1_DIR}/summary.json`);
const desc = (s) => `${s.allocation}/${s.normalization}/share ${s.share.toFixed(4)}/gg ${s.gg.toFixed(4)}/${s.uc.replace("uninsured_use_", "use ")}/${(100 * s.rate).toFixed(0)}%`;

// Every option set, each method's model, every specification.
function runsOf(o, profile) {
  const oo = withCentral(o);
  const specs = specsFor(oo);
  const runs = METHODS.map((meth) => { const m = modelFor("central", meth, oo); return specs.map((s) => evaluateFull(m, s, profile)); });
  return { specs, runs, costs: runs.map((xs) => xs.map((r) => r.cost_bn)), idx: distinctSpecs(specs), keys: specs.map(specKey) };
}
// The band: each method's minimum and maximum over the distinct specifications (the first of equal costs), averaged.
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

// ---------------------------------------------------------------------------------------------------
const SETS = {
  sept27: OFF,
  item1: withOff({ housing: "tenants", internal_transfer: "public_housing_operating" }),
  item1_unconsolidated: withOff({ housing: "tenants", internal_transfer: "none" }),
  item1_population_key: withOff({ internal_transfer: "public_housing_operating" }),
  item2: withOff({ production: "row4" }),
  item3: withOff({ tax_key: "irs_2023_raked" }),
  v1: V1,
  candidate: CANDIDATE,
  candidate_unconsolidated: withCand({ internal_transfer: "none" }),
  housing_capital_tenants: withCand({ capital_variant: "public_housing_at_rental_assistance_key" }),
  sept27_housing_capital_tenants: withOff({ capital_variant: "public_housing_at_rental_assistance_key" }),
  pay_unchanged_workforce: withCand({ public_pay: "unchanged_workforce" }),
  pay_counterfactual_low_share: withCand({ public_pay: "counterfactual_low_share" }),
  pay_counterfactual_high_share: withCand({ public_pay: "counterfactual_high_share" }),
  v1_pay_unchanged_workforce: withV1({ public_pay: "unchanged_workforce" }),
  v1_pay_counterfactual_low_share: withV1({ public_pay: "counterfactual_low_share" }),
  v1_pay_counterfactual_high_share: withV1({ public_pay: "counterfactual_high_share" }),
};
const ROAD_MOVES = Object.keys(ROAD_CASES).filter((rc) => rc !== "stationary_network");
for (const rc of ROAD_MOVES) { SETS[`road_${rc}`] = withCand({ road: rc }); SETS[`sept27_road_${rc}`] = withOff({ road: rc }); }
const PAYS = ["unchanged_workforce", "counterfactual_low_share", "counterfactual_high_share"];
const X = Object.fromEntries(Object.entries(SETS).map(([k, o]) => [k, runsOf(o)]));
const diff = (a, b) => X[a].costs.map((xs, m) => xs.map((x, i) => x - X[b].costs[m][i]));
const movesOf = (a, b, lines, comps, tol, production) => X[a].runs.flatMap((xs, m) => xs.map((r, i) => onlyMoves(r, X[b].runs[m][i], lines, comps, tol, production))).flat();
const B = Object.fromEntries(Object.keys(X).map((k) => [k, bandOf(X[k])]));
const E = Object.fromEntries(Object.keys(X).map((k) => [k, endsOf(X[k].specs, X[k].runs)]));
const at4811 = (ends) => ends.every((e) => e[0] === 48 && e[1] === 11);

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the September 27 case and the first candidate]");
const own27 = METHODS.map((meth) => {
  const oo = S.withCentral({});
  const m = S.modelFor("central", meth, oo);
  return S.specsFor(oo).map((s) => S.evaluateFull(m, s).cost_bn);
});
const own1 = METHODS.map((meth) => {
  const oo = C1.withCentral(C1.CANDIDATE);
  const m = C1.modelFor("central", meth, oo);
  return C1.specsFor(oo).map((s) => C1.evaluateFull(m, s).cost_bn);
});
const same = (a, b) => a.length === b.length && a.every((xs, m) => xs.length === b[m].length && xs.every((x, i) => x === b[m][i]));
gate("the September 27 package reproduces its published case (1e-9)", (() => { const c = S.central({});
  return near(c[0], s27.main_case[0], 1e-9) && near(c[1], s27.main_case[1], 1e-9); })(), f2(s27.main_case));
gate("with every item off, v2 is the September 27 case at every specification exactly (both methods)", same(X.sept27.costs, own27), "2 x 64");
const per27 = csvRows(`${SEPT27_DIR}/per_spec.csv`);
gate("...and its committed per_spec.csv exactly", per27.length === 128 && per27.every((r) =>
  Number(r.cost_bn) === X.sept27.costs[METHODS.indexOf(r.method)][Number(r.spec)]), "128 rows");
gate("the September 27 band and end specifications 48 / 11", near(B.sept27[0], s27.main_case[0], 1e-9) && near(B.sept27[1], s27.main_case[1], 1e-9)
  && at4811(E.sept27), f2(B.sept27));
gate("with the first candidate's options, v2 is the first candidate at every specification exactly (its own package, both methods)",
  same(X.v1.costs, own1), "2 x 64");
const per1 = csvRows(`${V1_DIR}/per_spec.csv`);
const d1pop = diff("item1_population_key", "sept27");
gate("...and its committed per_spec.csv exactly (candidate cost and item 1)", per1.length === 128 && per1.every((r) => {
  const m = METHODS.indexOf(r.method), i = Number(r.spec);
  return Number(r.candidate_cost_bn) === X.v1.costs[m][i] && Number(r.item1_bn) === d1pop[m][i];
}), "128 rows");
gate("the first candidate's band and end specifications 48 / 11 (its summary.json, 1e-9)", near(B.v1[0], s1.candidate[0], 1e-9)
  && near(B.v1[1], s1.candidate[1], 1e-9) && at4811(E.v1), f2(B.v1));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the specifications]");
const twinOf = (x, i) => x.keys.findIndex((t, j) => j !== i && t === x.keys[i]);
const specsOk = Object.values(X).every((x) => x.idx.length === 32 && x.specs.length === 64
  && x.keys.every((key, i) => { const t = twinOf(x, i); return t >= 0 && x.keys.filter((u) => u === key).length === 2
    && x.costs.every((xs) => xs[i] === xs[t]); })
  && twinOf(x, 48) === 52 && twinOf(x, 11) === 15 && x.idx.includes(48) && x.idx.includes(11));
gate("in every option set the 64 specifications are 32 distinct ones, each twice, identical in every field and in cost; 48 = 52 and 11 = 15",
  specsOk, `${Object.keys(X).length} option sets`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 1, public housing's deficit keyed by its tenants]");
const T = TRANSFERS.public_housing_operating.bn, H = HOUSING_SURPLUS;
const d1 = diff("item1", "sept27");
const legs = (m, i) => {
  const o = X.sept27.runs[m][i], r = X.item1.runs[m][i];
  const e = row(o, "receipts", ENTERPRISE_LINE), x = row(r, "receipts", HOUSING_LINE), h = row(r, "spending", RENTAL);
  return { e, x, h, ke: e.amount_bn / e.national_bn, kx: x.amount_bn / x.national_bn, kh: h.amount_bn / h.national_bn };
};
const f1Gap = worst(METHODS.flatMap((_, m) => X.item1.specs.map((s, i) => { const l = legs(m, i);
  return d1[m][i] - (l.e.response * l.ke * H - l.x.response * l.kx * (H - T) - l.h.response * l.kh * T); })));
gate("item 1 moves the cost by r_e ke H - r_x kx (H - T) - r_h kh T at every specification (1e-9)", f1Gap < 1e-9, `max |diff| ${ex(f1Gap)}`);
const kGap = worst(METHODS.flatMap((_, m) => X.item1.specs.map((s, i) => { const l = legs(m, i); return l.kx - l.kh; })));
const kSame = METHODS.every((_, m) => X.item1.specs.every((s, i) => { const l = legs(m, i);
  return l.x.key === l.h.key && l.x.response === l.e.response && l.x.response === l.h.response; }));
gate("the housing line carries the rental line's evaluated key (name, and share to 1e-15) and the enterprise receipt's response, which is the rental line's",
  kSame && kGap < 1e-15, `key ${legs(0, 48).x.key}, |kx - kh| ${ex(kGap)}, response ${legs(0, 48).x.response}`);
const f1Simple = worst(METHODS.flatMap((_, m) => X.item1.specs.map((s, i) => { const l = legs(m, i); return d1[m][i] - (l.ke - l.kh) * H; })));
gate("with every response at 1 that is (ke - kh) H = -(ke - kh) x $40.298bn (1e-9)", f1Simple < 1e-9, `max |diff| ${ex(f1Simple)}`);
const d1Ends = atEnds((m, i) => d1[m][i]);
gate("item 1 at 48 / 11 is the attack's section 1 expectation, -$1.69bn at both ends", r2(d1Ends[0]) === -1.69 && r2(d1Ends[1]) === -1.69, f2(d1Ends));
const dT = diff("item1", "item1_unconsolidated"), dTc = diff("candidate", "candidate_unconsolidated");
gate("under the tenant key the consolidation of T moves nothing (every specification, both methods, on the September 27 case and on v2, 1e-9)",
  worst(dT.flat()) < 1e-9 && worst(dTc.flat()) < 1e-9, `max |diff| ${ex(Math.max(worst(dT.flat()), worst(dTc.flat())))}`);
const m1 = movesOf("item1", "sept27", [`spending:${RENTAL}`, `receipts:${ENTERPRISE_LINE}`, `receipts:${HOUSING_LINE}`], [], 1e-12, false);
gate("item 1 moves no other line, no capital component (1e-12, so the enterprise capital key holds) and not production", m1.length === 0, m1.slice(0, 5).join(" ") || "exact");
const natOk = X.item1.runs.every((xs) => xs.every((r) => near(row(r, "spending", RENTAL).national_bn, H_NATIONAL - T, 1e-12)
  && near(row(r, "receipts", ENTERPRISE_LINE).national_bn, E_NATIONAL - H, 1e-12) && near(row(r, "receipts", HOUSING_LINE).national_bn, H - T, 1e-12)));
const keepGap = worst(METHODS.flatMap((_, m) => X.item1.specs.flatMap((s, i) => [
  keyOf(X.item1.runs[m][i], "spending", RENTAL) - keyOf(X.sept27.runs[m][i], "spending", RENTAL),
  keyOf(X.item1.runs[m][i], "receipts", ENTERPRISE_LINE) - keyOf(X.sept27.runs[m][i], "receipts", ENTERPRISE_LINE)])));
gate("national totals: housing_subsidies less T, enterprise_surplus less H, the housing line H - T; both old lines keep their keys (1e-15)",
  natOk && keepGap < 1e-15, `${RENTAL} ${H_NATIONAL} -> ${(H_NATIONAL - T).toFixed(6)}, ${ENTERPRISE_LINE} ${E_NATIONAL} -> ${(E_NATIONAL - H).toFixed(3)}, `
  + `${HOUSING_LINE} ${(H - T).toFixed(6)}; key |diff| ${ex(keepGap)}`);

// The internal-transfer controls.
const costWith = (m, specs, profile) => specs.map((s) => evaluateFull(m, s, profile).cost_bn);
const m27 = METHODS.map((meth) => modelFor("central", meth, withCentral(OFF)));
const synth27 = m27.map((m) => withSyntheticTransfer(m, 1));
const todayGap = worst(METHODS.flatMap((_, m) => X.sept27.specs.map((s, i) => {
  const r = X.sept27.runs[m][i];
  return costWith(synth27[m], [s])[0] - r.cost_bn - (keyOf(r, "spending", RENTAL) - keyOf(r, "receipts", ENTERPRISE_LINE));
})));
gate("control, today: a synthetic $1bn on both legs moves the September 27 case by kh - ke at every specification (1e-9)", todayGap < 1e-9, `max |diff| ${ex(todayGap)}`);
const noCap = specsFor(withOff({ capital: false }));
const today48 = METHODS.map((_, m) => costWith(synth27[m], [noCap[48]])[0] - costWith(m27[m], [noCap[48]])[0]);
gate("...the audit's positive control: at specification 48, capital off, it lowers the cost by $40.75–43.19 million (3db388d section 7)",
  near(Math.min(...today48.map(Math.abs)), 0.04075, 5e-6) && near(Math.max(...today48.map(Math.abs)), 0.04319, 5e-6) && today48.every((x) => x < 0),
  today48.map((x) => (1000 * x).toFixed(4) + "m").join(" / "));
const splitControls = [
  ["main profile", SETS.item1, undefined],
  ["long_run_non_school_fixed", SETS.item1, "long_run_non_school_fixed"],
  ["proportional reference", SETS.item1, "proportional_reference"],
  ["v2's production and tax key", CANDIDATE, undefined],
];
const splitGaps = {};
for (const [label, o, profile] of splitControls) {
  const oo = withCentral(o), specs = specsFor(oo);
  splitGaps[label] = worst(METHODS.flatMap((meth) => {
    const m = modelFor("central", meth, oo);
    const a = costWith(m, specs, profile), b = costWith(withHousingTransfer(m, 1), specs, profile);
    return a.map((x, i) => b[i] - x);
  }));
  gate(`control, v2: a synthetic $1bn on the split legs (rental line and housing line) moves the case by 0 (${label}, every specification, 1e-9)`,
    splitGaps[label] < 1e-9, `max |diff| ${ex(splitGaps[label])}`);
}
// The v2 control is not an identity: with the two legs at different responses (the enterprise receipt, and so the housing
// line, at 0.37; the rental line at 1) the same $1bn moves the case by (r_x - r_h) kh.
const o37 = withCentral(withOff({ housing: "tenants", internal_transfer: "public_housing_operating", enterprise_receipt: 0.37 }));
const specs37 = specsFor(o37);
const sens37 = METHODS.map((meth) => {
  const m = modelFor("central", meth, o37);
  return specs37.map((s) => { const r = evaluateFull(m, s), q = evaluateFull(withHousingTransfer(m, 1), s);
    const x = row(r, "receipts", HOUSING_LINE), h = row(r, "spending", RENTAL);
    return { move: q.cost_bn - r.cost_bn, want: x.response * (x.amount_bn / x.national_bn) * -1 + h.response * (h.amount_bn / h.national_bn) }; });
});
const sensGap = worst(sens37.flat().map((z) => z.move - z.want));
const sens48 = mean(sens37.map((xs) => xs[48].move));
gate("...and it is not an identity: with the housing line at 0.37 and the rental line at 1 the $1bn moves the case by (r_h - r_x) kh (every specification, 1e-9)",
  sensGap < 1e-9 && Math.abs(sens48) > 0.01, `spec 48 ${(1000 * sens48).toFixed(2)}m per $1bn; max |diff| ${ex(sensGap)}`);
// The first candidate's after-gate: it holds even on the population key, where a transfer crosses at kh - ke, so it tests
// consolidate() against withSyntheticTransfer(), not the keys.
const idGaps = {};
for (const [label, o] of [["September 27 case, population key", OFF], ["first candidate", V1]]) {
  const oo = withCentral(o), specs = specsFor(oo);
  idGaps[label] = worst(METHODS.flatMap((meth) => {
    const base = withProduction(S.modelFor("central", meth, oo), oo.production);
    const a = costWith(consolidate(base, T), specs), b = costWith(consolidate(withSyntheticTransfer(base, 1), T + 1), specs);
    return a.map((x, i) => b[i] - x);
  }));
}
gate("the first candidate's after-gate is an identity: consolidate(withSyntheticTransfer(m, 1), T + 1) = consolidate(m, T) on the population key too (1e-9); kept as a unit test of the two helpers",
  Object.values(idGaps).every((g) => g < 1e-9), Object.entries(idGaps).map(([k, g]) => `${k} ${ex(g)}`).join(", "));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 2, production on the row-4 weights]");
const dims = Engine.PRODUCTION_DIMS;
const pubGap = worst(["private_wtp_bn", "induced_receipts_bn"].flatMap((k) => PROD.grid.published[k].map((x, i) => x - MODEL.production[k][i])));
gate("the file's published grid is model.json's (P and F, 3,888 cells, within 2e-9: both are rounded)", pubGap < 2e-9, `max |diff| ${ex(pubGap)}`);
const refIndex = (normalization) => Engine.productionIndex(MODEL, Object.assign({}, MODEL.production.reference, { normalization }));
const pf = (name, normalization) => PROD.grid[name].private_wtp_bn[refIndex(normalization)] + PROD.grid[name].induced_receipts_bn[refIndex(normalization)];
gate("the reference cells are the file's reference rows (GDP index 1716, cash 1230)", ["cash", "gdp"].every((n) =>
  refIndex(n) === PROD.reference.row4[n].index && Math.abs(pf("row4", n) - PROD.reference.row4[n].P_plus_F_bn) < 2e-9), dims.join(","));
const d2 = diff("item2", "sept27");
const d2Gap = worst(METHODS.flatMap((_, m) => X.item2.runs[m].map((r, i) => d2[m][i]
  + (r.evaluation.production_gain_bn - X.sept27.runs[m][i].evaluation.production_gain_bn))));
gate("item 2 moves the cost by minus the change in P + F at every specification (1e-9)", d2Gap < 1e-9, `max |diff| ${ex(d2Gap)}`);
const m2 = movesOf("item2", "sept27", [], [], 0, true);
gate("item 2 moves no line, no capital component", m2.length === 0, m2.slice(0, 5).join(" ") || "exact");
const d2Ends = atEnds((m, i) => d2[m][i]);
gate("item 2 at 48 / 11 is the first candidate's +1.642719 / +1.107389 (production_row4.json)",
  near(d2Ends[0], PROD.cost_change_at_reference_bn.gdp, 1e-9) && near(d2Ends[1], PROD.cost_change_at_reference_bn.cash, 1e-9), f2(d2Ends));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 3, the federal income-tax key matched to IRS 2023]");
const TR_FILE = "tax_key_heldout_2026_09_28/derived/main_case_translation.json";
const TR = readJson(TR_FILE);
const TV = TAX_KEYS.irs_2023_raked;
const d3 = diff("item3", "sept27");
const m3 = movesOf("item3", "sept27", [`receipts:${TAX_LINE}`], [], 0, false);
gate("item 3 moves no other line, no capital component and not production", m3.length === 0, m3.slice(0, 5).join(" ") || "exact");
const by = METHODS.map((meth) => taxEditOf("central", meth, "irs_2023_raked"));
const editGap = worst(METHODS.flatMap((_, m) => X.item3.specs.map((s, i) => row(X.item3.runs[m][i], "receipts", TAX_LINE).amount_bn
  - row(X.sept27.runs[m][i], "receipts", TAX_LINE).amount_bn - by[m][s.allocation])));
gate(`the group's federal income tax moves by stack factor x $${TAX.national_bn}bn x share change at every specification (1e-12)`, editGap < 1e-12,
  METHODS.map((meth, m) => `${meth.replace("b_", "")} ${fx(by[m].personal)} / ${fx(by[m].shared)}`).join("; "));
const d3Gap = worst(METHODS.flatMap((_, m) => X.item3.specs.map((s, i) => { const r = row(X.item3.runs[m][i], "receipts", TAX_LINE);
  return d3[m][i] + r.response * (r.amount_bn - row(X.sept27.runs[m][i], "receipts", TAX_LINE).amount_bn); })));
gate("the cost falls by the receipt's response times the edit at every specification (1e-9)", d3Gap < 1e-9, `max |diff| ${ex(d3Gap)}`);
const tlGap = worst(METHODS.flatMap((meth, m) => [d3[m][48] + TR.methods[meth].variants[TV].union_tax_change_bn.shared,
  d3[m][11] + TR.methods[meth].variants[TV].union_tax_change_bn.personal]));
gate("per method at 48 (shared) and 11 (personal) it is the tax lane's union_tax_change_bn (main_case_translation.json, 1e-9)", tlGap < 1e-9, `max |diff| ${ex(tlGap)}`);
const d3Ends = atEnds((m, i) => d3[m][i]);
gate("at 48 / 11 it is the tax lane's change at the case ends, -3.200535 / -3.096568 (1e-9)",
  near(d3Ends[0], TR.variants[TV].change_at_case_ends_bn.low, 1e-9) && near(d3Ends[1], TR.variants[TV].change_at_case_ends_bn.high, 1e-9), f2(d3Ends));
gate("item 3 alone gives the tax lane's band on the September 27 case (1e-9)",
  near(B.item3[0], TR.variants[TV].band.low, 1e-9) && near(B.item3[1], TR.variants[TV].band.high, 1e-9), f2(B.item3));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the items together]");
const addGap = worst(METHODS.flatMap((_, m) => X.candidate.costs[m].map((x, i) => x - X.sept27.costs[m][i] - d1[m][i] - d2[m][i] - d3[m][i])));
gate("v2 - September 27 = item 1 + item 2 + item 3 at every specification (1e-9)", addGap < 1e-9, `max |diff| ${ex(addGap)}`);
const addV1 = worst(METHODS.flatMap((_, m) => X.v1.costs[m].map((x, i) => x - X.sept27.costs[m][i] - d1pop[m][i] - d2[m][i])));
gate("the first candidate - September 27 = its item 1 + item 2 at every specification (1e-9)", addV1 < 1e-9, `max |diff| ${ex(addV1)}`);
const mC = movesOf("candidate", "sept27", [`spending:${RENTAL}`, `receipts:${ENTERPRISE_LINE}`, `receipts:${HOUSING_LINE}`, `receipts:${TAX_LINE}`], [], 1e-12, true);
gate("v2 moves only the named lines, P and F (capital 1e-12)", mC.length === 0, mC.slice(0, 5).join(" ") || "exact");
gate("v2 keeps the end specifications 48 / 11 in both methods (over the 32 distinct)", at4811(E.candidate), JSON.stringify(E.candidate));
const CB = C.central({});
gate("v2's per-specification costs give the package's band (central(), 1e-9)", near(CB[0], B.candidate[0], 1e-9) && near(CB[1], B.candidate[1], 1e-9), f2(CB));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: public pay on the account's own workforce]");
const payOf = (k, m, i) => X[k].runs[m][i].public_pay_bn;
for (const [base, prefix] of [["candidate", "pay_"], ["v1", "v1_pay_"]]) {
  let gap = 0, formula = 0;
  const moves = [];
  for (const p of PAYS) {
    const k = prefix + p, d = diff(k, base);
    gap = Math.max(gap, worst(METHODS.flatMap((_, m) => d[m].map((x, i) => x - payOf(k, m, i)))));
    formula = Math.max(formula, worst(METHODS.flatMap((_, m) => X[k].specs.map((s, i) => {
      const charge = publicPayOf(s.production, s.normalization);
      const sh = removalShares(X[k].runs[m][i].evaluation);
      const want = p === "unchanged_workforce" ? charge : charge * (1 - (p === "counterfactual_low_share" ? sh.low : sh.high));
      return payOf(k, m, i) - want;
    }))));
    moves.push(...movesOf(k, base, [], [], 0, false));
  }
  gate(`public pay on ${base === "v1" ? "the first candidate" : "v2"}: each reading adds its charge, charge x (1 - removal share), and moves no line (1e-12)`,
    gap < 1e-12 && formula < 1e-12 && moves.length === 0, `max |diff| ${ex(gap)}, formula ${ex(formula)}${moves.length ? " " + moves.slice(0, 3).join(" ") : ""}`);
}
const shares = (k) => { const lo = atEnds((m, i) => removalShares(X[k].runs[m][i].evaluation).low);
  const hi = atEnds((m, i) => removalShares(X[k].runs[m][i].evaluation).high);
  return [0, 1].map((e) => ({ low: lo[e], high: hi[e] })); };
const shV1 = shares("v1"), shV2 = shares("candidate");
const payAt = (k) => atEnds((m, i) => payOf(k, m, i));
const pct = (x) => r2(100 * x);
gate("the attack's section 4 on the first candidate: removal shares 8.96 / 11.43% (48) and 9.63 / 12.27% (11); charge 13.6085 / 8.9520 on the unchanged workforce, 12.05–12.39 / 7.85–8.09 on the counterfactual one",
  pct(shV1[0].low) === 8.96 && pct(shV1[0].high) === 11.43 && pct(shV1[1].low) === 9.63 && pct(shV1[1].high) === 12.27
  && fx(payAt("v1_pay_unchanged_workforce")[0]) === "13.6085" && fx(payAt("v1_pay_unchanged_workforce")[1]) === "8.9520"
  && r2(payAt("v1_pay_counterfactual_high_share")[0]) === 12.05 && r2(payAt("v1_pay_counterfactual_low_share")[0]) === 12.39
  && r2(payAt("v1_pay_counterfactual_high_share")[1]) === 7.85 && r2(payAt("v1_pay_counterfactual_low_share")[1]) === 8.09,
  `48: ${PAYS.map((p) => fx(payAt("v1_pay_" + p)[0])).join(" / ")}; 11: ${PAYS.map((p) => fx(payAt("v1_pay_" + p)[1])).join(" / ")}`);
gate("v2 leaves the removal shares and so every public-pay reading where the first candidate has them (1e-12): items 1-3 touch no consumption line",
  PAYS.every((p) => [0, 1].every((e) => near(payAt("pay_" + p)[e], payAt("v1_pay_" + p)[e], 1e-12))) && [0, 1].every((e) =>
    near(shV1[e].low, shV2[e].low, 1e-15) && near(shV1[e].high, shV2[e].high, 1e-15)), "3 readings x 2 ends");

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the road arm]");
const RC_FILE = `${C.LANE}/derived/road_congestion.json`;
if (!fs.existsSync(path.join(FISCAL, RC_FILE))) {
  console.error(`[BLOCKED] ${RC_FILE} is missing: run road_congestion.py first`);
  process.exit(1);
}
const RC = readJson(RC_FILE);
const pkgFile = `${C.LANE}/package.cjs`;
gate("road_congestion.json: all its gates passed, and it was priced from this package.cjs and road_stock.json (sha256)",
  Array.isArray(RC.gates) && RC.gates.length > 0 && RC.gates.every((g) => g.passed) && RC.meta.sources[pkgFile] === C.sha256(pkgFile)
  && RC.meta.sources[C.STOCK_FILE] === C.sha256(C.STOCK_FILE), `${RC.gates.length} gates, ${RC.rows.length} cuts`);
const CONG = new Map(RC.rows.map((r) => [r.lane_cut, r]));
const missing = new Set();
const congAt = (cut) => { const r = CONG.get(cut); if (!r) { missing.add(cut); return { congestion_central_bn: NaN }; } return r; };
const roadGaps = ROAD_MOVES.map((rc) => { const a = diff(`road_${rc}`, "candidate"), b = diff(`sept27_road_${rc}`, "sept27");
  return worst(METHODS.flatMap((_, m) => a[m].map((x, i) => x - b[m][i]))); });
gate("each road case moves v2 exactly as it moves the September 27 case (every specification, 1e-9): the arm does not interact with items 1-3",
  worst(roadGaps) < 1e-9, ROAD_MOVES.map((rc, k) => `${rc} ${ex(roadGaps[k])}`).join(", "));
const roadV1 = { replacement: "road_replacement_bn", fixed_stock: "road_fixed_stock_bn" };
gate("replacement and a fixed stock move the September 27 case as in the first candidate (its per_spec.csv, 1e-12)",
  Object.entries(roadV1).every(([rc, col]) => { const d = diff(`sept27_road_${rc}`, "sept27");
    return per1.every((r) => Math.abs(Number(r[col]) - d[METHODS.indexOf(r.method)][Number(r.spec)]) < 1e-12); }), "2 cases x 128");
const mRoad = ROAD_MOVES.flatMap((rc) => movesOf(`road_${rc}`, "candidate", [`spending:${ROAD_LINE}`], Object.values(ROAD_COMPONENTS), 0, false));
gate("every road case moves only economic_affairs_services and the road capital components", mRoad.length === 0, mRoad.slice(0, 5).join(" ") || "exact");
const upEnds = Object.fromEntries(["construction_year_effects", "construction_land"].map((rc) => [rc, atEnds((m, i) => diff(`road_${rc}`, "candidate")[m][i])]));
gate("the upward cases add the attack's +$0.90bn / +$0.44bn at spec 48 (section 3b) and nothing at 11 (1e-12)",
  r2(upEnds.construction_year_effects[0]) === 0.9 && r2(upEnds.construction_land[0]) === 0.44
  && Math.abs(upEnds.construction_year_effects[1]) < 1e-12 && Math.abs(upEnds.construction_land[1]) < 1e-12,
  `${f2(upEnds.construction_year_effects)}; ${f2(upEnds.construction_land)}`);
const ci = STOCK.construction;
gate("a fixed stock (response 0) lies outside construction's across-state interval (year effects, land control)",
  ci.year_effects.ci95[0] > 0 && ci.land.ci95[0] > 0,
  `b ${ci.year_effects.b.toFixed(3)} (${ci.year_effects.ci95.map((x) => x.toFixed(3)).join("–")}), land ${ci.land.b.toFixed(3)} (${ci.land.ci95.map((x) => x.toFixed(3)).join("–")})`);
// The arm on v2: each road case at the adopted responses and the stationary network at each long-run variant, the account
// at the fixed specifications and the congestion item at the same specifications' lane cut (road_congestion.json).
const roadSets = ROAD_ARM.map((a) => ({ a, x: a.long_run === "adopted"
  ? (a.road === "stationary_network" ? X.candidate : X[`road_${a.road}`]) : runsOf(withCand({ road: a.road, long_run: a.long_run })) }));
const cut0 = endCuts(X.candidate.specs, X.candidate.runs, fixedEnds(X.candidate.runs));
const cong0 = cut0.map((c) => congAt(c).congestion_central_bn);
const acc0 = atEnds((m, i) => X.candidate.costs[m][i]);
const roadGrid = roadSets.map(({ a, x }) => {
  const cut = endCuts(x.specs, x.runs, fixedEnds(x.runs));
  const cg = cut.map(congAt);
  const acc = atEnds((m, i) => x.costs[m][i]);
  const central = cg.map((r) => r.congestion_central_bn);
  return { road_case: a.road, long_run: a.long_run, label: a.long_run === "adopted" ? ROAD_CASES[a.road].label : LONG_RUN_VARIANTS[a.long_run].label,
    lanes: ROAD_CASES[a.road].lanes, lane_cut: cut, account_bn: acc, account_change_bn: [acc[0] - acc0[0], acc[1] - acc0[1]],
    congestion_bn: central, congestion_range_bn: cg.map((r) => [r.factorial_min_bn, r.factorial_max_bn]),
    congestion_change_bn: [central[0] - cong0[0], central[1] - cong0[1]],
    net_change_bn: [acc[0] - acc0[0] + central[0] - cong0[0], acc[1] - acc0[1] + central[1] - cong0[1]],
    road_return_removed_bn: atEnds((m, i) => x.runs[m][i].road_return_removed_bn), band_bn: bandOf(x), end_specifications: endsOf(x.specs, x.runs) };
});
const gridAt = (rc, v) => roadGrid.find((g) => g.road_case === rc && g.long_run === v);
const cg27 = s27.beside_the_account.congestion;
gate("stationary network: the congestion item is the September 27 case's beside the account (the bridge's 10 digits, 1e-8)",
  near(cong0[0], cg27.low_end.congestion_bn, 1e-8) && near(cong0[1], cg27.high_end.congestion_bn, 1e-8), `${fx(cong0[0])} / ${fx(cong0[1])}`);
gate("replacement and a fixed stock keep the lanes: cut 0 and the lanes-fixed B1 (net_change.json before_bn, 1e-9)",
  ["replacement", "fixed_stock"].every((rc) => gridAt(rc, "adopted").lane_cut.every((c) => c === 0)
    && gridAt(rc, "adopted").congestion_bn.every((c) => near(c, cg27.before_bn, 1e-9))), fx(cg27.before_bn));
gate("the upward cases' lanes follow the stock: a deeper cut than the stationary network's at 48, the same cut at 11",
  ["construction_year_effects", "construction_land"].every((rc) => gridAt(rc, "adopted").lane_cut[0] > cut0[0] && gridAt(rc, "adopted").lane_cut[1] === cut0[1]),
  ["construction_year_effects", "construction_land"].map((rc) => gridAt(rc, "adopted").lane_cut.map((c) => c.toFixed(5)).join("/")).join("; ") + ` (stationary ${cut0.map((c) => c.toFixed(5)).join("/")})`);
gate("every road-arm cut has a factorial range in road_congestion.json", roadGrid.every((g) => g.congestion_range_bn.every((r) => Number.isFinite(r[0]) && Number.isFinite(r[1]))),
  `${roadGrid.length} rows`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: an independent path]");
// The engine, model.json, the September 27 corrections.json, the NIPA 3.8 housing line (the capital lane's table), T,
// production_row4.json's row-4 grid and the tax lane's own per-method change, averaged; the specification grid, state,
// responses and capital return are rebuilt from the payload's meta.
function independentCosts(pay, grid, transfer, housing, taxBy) {
  const Eng = require(path.join(FISCAL, "assumption_explorer_2026_09_21", "engine.js"));
  const model = JSON.parse(fs.readFileSync(path.join(FISCAL, "assumption_explorer_2026_09_21", "derived", "model.json"), "utf8"));
  const m = Eng.applyCorrections(model, { lines: pay.lines, edits: pay.edits });
  m.production.private_wtp_bn = grid.private_wtp_bn;
  m.production.induced_receipts_bn = grid.induced_receipts_bn;
  const hl = m.spending.lines.find((l) => l.id === "housing_subsidies"), el = m.receipts.lines.find((l) => l.id === "enterprise_surplus");
  const tl = m.receipts.lines.find((l) => l.id === "federal_income_tax");
  const fh = (hl.national_bn - transfer) / hl.national_bn, fe = (el.national_bn - housing) / el.national_bn;
  for (const k of Object.values(hl.keys)) for (const a of ["personal", "shared"]) { k[a].target_bn *= fh; k[a].other_bn *= fh; }
  for (const k of Object.values(el.cells)) for (const a of ["personal", "shared"]) { k[a].target_bn *= fe; k[a].other_bn *= fe; }
  hl.national_bn -= transfer; el.national_bn -= housing;
  const nat = housing - transfer;
  const cells = Object.fromEntries(["personal", "shared"].map((a) => { const f = hl.keys[hl.preferred_key][a].target_bn / hl.national_bn;
    return [a, { direct: false, key: hl.preferred_key, response_class: "public_asset", share: f, target_bn: f * nat, other_bn: (1 - f) * nat }]; }));
  m.receipts.lines.push({ id: "housing_enterprise_surplus", national_bn: nat, cells: Object.fromEntries(m.receipts.scenarios.map((sc) => [sc, cells])) });
  for (const a of ["personal", "shared"]) { tl.cells[m.receipts.reference][a].target_bn += taxBy[a]; tl.cells[m.receipts.reference][a].other_bn -= taxBy[a]; }
  const Rp = pay.meta.responses, Kp = pay.meta.capital_return;
  const syn = Object.fromEntries(pay.lines.map((l) => [l.response_class, l.id]));
  const rowOf = (ev, id) => ev.spending.find((l) => l.id === id);
  const receipt = (ev, id) => ev.receipts.find((l) => l.id === id);
  const out = [];
  for (const allocation of ["personal", "shared"]) for (const normalization of ["cash", "gdp"])
    for (const share of Eng.schoolShareBounds(model)) for (const school of [Rp.school.growth, Rp.school.decline])
      for (const [rd, gg] of [["low", Rp.general_government.low], ["high", Rp.general_government.high]])
        for (const uc of ["uninsured_use_low", "uninsured_use_high"]) {
          const s = Eng.defaultState(m);
          s.allocation = allocation; s.receipt_scenario = m.receipts.reference; s.production.normalization = normalization;
          s.count_production = true; s.general_government_response = gg;
          s.key_override = { public_order_safety: "use", medicaid_and_chip_other_medical: uc };
          s.response_override = { education_services: share * school + (1 - share), public_order_safety: 1, health_services: 1,
            income_security_services: 1, housing_community_services: 1,
            [syn.education_school_part]: share * school, [syn.education_other_part]: 1 - share, [syn.correction_constant]: 1 };
          for (const id of ["economic_affairs_services", "recreation_culture", "housing_subsidies"]) s.response_override[id] = Rp[id][rd];
          s.response_override[Rp.enterprise_surplus.override] = Rp.enterprise_surplus[rd];
          s.response_override["receipt:housing_enterprise_surplus"] = Rp.enterprise_surplus[rd];
          const ev = Eng.evaluate(m, s);
          let capital = 0;
          for (const c of Kp.components) {
            const k = c.key, r = c.response;
            let key, response;
            if (k.kind === "constant") key = k.value;
            else if (k.kind === "receipt_amount_over_national") key = receipt(ev, k.line).amount_bn / receipt(ev, k.line).national_bn;
            else if (k.kind === "lines_amount_over_national") key = k.numerator_lines.reduce((a, id) => a + rowOf(ev, id).amount_bn, 0) / rowOf(ev, k.denominator_line).national_bn;
            else throw new Error("independent path: unknown key kind " + k.kind);
            if (r.kind === "fixed") response = r.value;
            else if (r.kind === "enterprises_switch") response = r.values[Kp.enterprises];
            else if (r.kind === "line_response") response = rowOf(ev, r.line).response;
            else if (r.kind === "line_response_over_share") response = rowOf(ev, r.line).response / (r.share === "school" ? share : 1 - share);
            else if (r.kind === "long_run_subfunction") response = Rp[r.line].subfunctions.find((x) => x.id === r.subfunction)[rd];
            else throw new Error("independent path: unknown response kind " + r.kind);
            capital += c.stock_charged_bn * Kp.rates[rd] * key * response;
          }
          out.push(-ev.welfare_bn + capital);
        }
  return out;
}
const payload27 = readJson(`${SEPT27_DIR}/corrections.json`);
const esv = csvRows(C.ESV_FILE).find((r) => r.nipa_3_8_lines === "l13");
const taxMean = Object.fromEntries(ALLOCS.map((a) => [a, mean(METHODS.map((meth) => TR.methods[meth].variants[TV].union_tax_change_bn[a]))]));
const independent = independentCosts(payload27, PROD.grid.row4, T, Number(esv.current_surplus_2024_bn), taxMean);
const methodMean = X.candidate.specs.map((_, i) => mean(X.candidate.costs.map((xs) => xs[i])));
const indGap = worst(independent.map((x, i) => x - methodMean[i]));
gate("independent path: engine + model.json + the September 27 corrections.json + H + T + the row-4 grid + the tax lane's change give v2 at every specification (1e-9)",
  independent.length === 64 && indGap < 1e-9, `max |diff| ${ex(indGap)} against the two methods' mean`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[range]");
// The September 27 components on a base, each variant re-run at every specification. Account only: a variant's band
// (each method's ends over the distinct specifications, averaged) less the base's. Jointly: the same with the congestion
// item at each band end's lane cut added on both sides (the dependent-pieces placement rule). fixedAcc and fixedCut keep
// the fixed-specification reading (48 / 11) the attack used for the long-run component.
function rangeOn(base) {
  const b = variantRuns(base, { o: {}, caseName: "central", methods: METHODS });
  const bEnds = endsOf(b.specs, b.runs);
  const Cb = bandAt(b, bEnds);
  const congB = endCuts(b.specs, b.runs, bEnds).map((c) => congAt(c).congestion_central_bn);
  const comps = rangeComponents().map((comp) => {
    const devs = comp.variants.map((variant) => {
      const x = variantRuns(base, variant);
      const ends = endsOf(x.specs, x.runs);
      const band = bandAt(x, ends);
      const cong = endCuts(x.specs, x.runs, ends).map((c) => congAt(c).congestion_central_bn);
      return { v: variant.v, ends, band, d: [band[0] - Cb[0], band[1] - Cb[1]], congestion_change: [cong[0] - congB[0], cong[1] - congB[1]],
        j: [band[0] + cong[0] - Cb[0] - congB[0], band[1] + cong[1] - Cb[1] - congB[1]],
        fixedAcc: [0, 1].map((e) => mean(x.runs.map((xs) => xs[ENDS[e]].cost_bn))), fixedCut: endCuts(x.specs, x.runs, fixedEnds(x.runs)) };
    });
    const lohi = (f) => ({ lo: [0, 1].map((e) => Math.min(0, ...devs.map((x) => f(x)[e]))), hi: [0, 1].map((e) => Math.max(0, ...devs.map((x) => f(x)[e]))) });
    return Object.assign({ name: comp.name, label: comp.label, devs }, lohi((x) => x.d), { joint: lohi((x) => x.j) });
  });
  const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
  const outer = (lo, hi) => {
    const sl = comps.reduce((s, x) => [s[0] + lo(x)[0], s[1] + lo(x)[1]], [0, 0]), sh = comps.reduce((s, x) => [s[0] + hi(x)[0], s[1] + hi(x)[1]], [0, 0]);
    const low_end = [Cb[0] + sl[0], Cb[0] + sh[0]], high_end = [Cb[1] + sl[1], Cb[1] + sh[1]];
    return { low_end, high_end, overall: [low_end[0], high_end[1]], quadrature: [Cb[0] - rss(comps.map((x) => lo(x)[0])), Cb[1] + rss(comps.map((x) => hi(x)[1]))] };
  };
  return Object.assign({ band: Cb, base: b, base_ends: bEnds, congestion_at_ends: congB, components: comps },
    outer((x) => x.lo, (x) => x.hi), { joint: outer((x) => x.joint.lo, (x) => x.joint.hi) });
}
const range27 = rangeOn(OFF), rangeV1 = rangeOn(V1), rangeC = rangeOn(CANDIDATE);
const rangeGap = (r, want) => worst(["low_end", "high_end", "overall", "quadrature"].flatMap((k) => [r[k][0] - want[k][0], r[k][1] - want[k][1]]));
gate("on the September 27 case the components reproduce its published range (low end, high end, overall, quadrature; 1e-9)",
  rangeGap(range27, s27.range) < 1e-9 && range27.components.length === s27.components.length
  && range27.components.every((x, k) => x.name === s27.components[k].name), `${range27.components.length} components, max |diff| ${ex(rangeGap(range27, s27.range))}`);
gate("on the first candidate they reproduce its published range (summary.json range.candidate, 1e-9)",
  rangeGap(rangeV1, s1.range.candidate) < 1e-9, `max |diff| ${ex(rangeGap(rangeV1, s1.range.candidate))}`);
gate("the base bands are the packages' (1e-9)", [[range27, B.sept27], [rangeV1, B.v1], [rangeC, B.candidate]].every(([r, b]) =>
  near(r.band[0], b[0], 1e-9) && near(r.band[1], b[1], 1e-9)), "3 bases");
// The attack's recipe (probe_item45.cjs section 5c): the long-run component alone, its variants at the fixed
// specifications, with the congestion change at their cut; the other components account only.
function attackJoint(r) {
  const lr = r.components.find((x) => x.name === "long_run_response");
  const baseAcc = [0, 1].map((e) => mean(r.base.runs.map((xs) => xs[ENDS[e]].cost_bn)));
  const baseCong = endCuts(r.base.specs, r.base.runs, fixedEnds(r.base.runs)).map((c) => congAt(c).congestion_central_bn);
  const jf = lr.devs.map((x) => [0, 1].map((e) => x.fixedAcc[e] - baseAcc[e] + congAt(x.fixedCut[e]).congestion_central_bn - baseCong[e]));
  const dLow = Math.min(0, ...jf.map((x) => x[0])) - lr.lo[0], dHigh = Math.max(0, ...jf.map((x) => x[1])) - lr.hi[1];
  return { overall: [r.overall[0] + dLow, r.overall[1] + dHigh], moves: [dLow, dHigh], variants: lr.devs.map((x, k) => ({ v: x.v, fixed_joint_bn: jf[k] })) };
}
const attackV1 = attackJoint(rangeV1), attackC = attackJoint(rangeC);
gate("the attack's joint reading of the long-run component on the first candidate, $260.6094–434.2178bn (section 3d, from 4-decimal csv values; 2e-3)",
  near(attackV1.overall[0], 260.6094, 2e-3) && near(attackV1.overall[1], 434.2178, 2e-3), `${fx(attackV1.overall[0])}–${fx(attackV1.overall[1])}`);
const lrComp = (r) => r.components.find((x) => x.name === "long_run_response");
gate("the stationary network at each long-run variant is the range component's variant band on v2 (1e-9)",
  lrComp(rangeC).devs.every((x) => { const g = gridAt("stationary_network", x.v); return g && near(g.band_bn[0] - rangeC.band[0], x.d[0], 1e-9) && near(g.band_bn[1] - rangeC.band[1], x.d[1], 1e-9); }),
  `${lrComp(rangeC).devs.length} variants`);
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
const FIXED = [
  ["item1_tenant_key", "1. public housing's deficit keyed by its tenants, the $" + T.toFixed(6) + "bn operating subsidy consolidated", fixed("item1"), "in v2"],
  ["item1_tenant_key_unconsolidated", "1. the same, the operating subsidy not consolidated (under this key it moves nothing)", fixed("item1_unconsolidated"), "beside"],
  ["item1_population_key", "1. the first candidate's reading: the population key, the operating subsidy consolidated", fixed("item1_population_key"), "beside"],
  ["item2_production_row4", "2. production on the account's row-4 weights", fixed("item2"), "in v2"],
  ["item3_tax_key_irs_2023_raked", "3. the federal income-tax key matched to IRS 2023, raked with CBO's groups", fixed("item3"), "in v2"],
  ["items_1_to_3_candidate_v2", "items 1-3 together: candidate v2", fixed("candidate"), "v2"],
  ["first_candidate", "the first candidate (c313b53)", fixed("v1"), "reference"],
  ["housing_capital_tenant_key_on_sept27", "public housing's capital at the rental-assistance key, on the September 27 case", fixed("sept27_housing_capital_tenants"), "range variant"],
  ["housing_capital_tenant_key_on_v2", "public housing's capital at the rental-assistance key, on v2 (change from v2)", fixed("housing_capital_tenants", "candidate"), "range variant"],
  ...PAYS.map((p) => [`public_pay_${p}_on_v2`, `public pay, ${p.replace(/_/g, " ")}, on v2 (change from v2)`, fixed(`pay_${p}`, "candidate"), "beside"]),
  ...PAYS.map((p) => [`public_pay_${p}_on_first_candidate`, `public pay, ${p.replace(/_/g, " ")}, on the first candidate (change from it)`, fixed(`v1_pay_${p}`, "v1"), "beside"]),
  ...ROAD_MOVES.map((rc) => [`road_${rc}_on_v2`, `road arm, ${ROAD_CASES[rc].label} (account only; change from v2)`, fixed(`road_${rc}`, "candidate"), "beside"]),
];
const fixedCsv = ["item,label,placement,old_spec48_bn,new_spec48_bn,change_spec48_bn,old_spec11_bn,new_spec11_bn,change_spec11_bn"]
  .concat(FIXED.map(([k, label, v, place]) => [k, `"${label}"`, place, fx(v.old[0]), fx(v.new[0]), fx(v.change[0]), fx(v.old[1]), fx(v.new[1]), fx(v.change[1])].join(",")));

// Ends and runner-ups over the 32 distinct specifications.
const ENDS_OF = ["sept27", "v1", "item1", "item1_population_key", "item2", "item3", "candidate", "housing_capital_tenants",
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

// The internal transfers that cross differently keyed legs: the cost change per $1bn paid from a spending line into an
// enterprise's current surplus (MP-5: the surplus includes subsidies received from other levels of government), at the
// evaluated keys and responses, in $ million.
const perBn = (k, pay, rec) => atEnds((m, i) => { const r = X[k].runs[m][i], a = row(r, "spending", pay), b = row(r, "receipts", rec);
  return 1000 * (a.response * a.amount_bn / a.national_bn - b.response * b.amount_bn / b.national_bn); });
const legAt = (k, side, id) => { const r = X[k].runs[0][48], x = row(r, side, id);
  return `${id} (${x.key}, ${fx(atEnds((m, i) => keyOf(X[k].runs[m][i], side, id))[0])}; response ${x.response})`; };
const CROSSINGS = [
  { transfer: "public housing's operating subsidy (HUD Public Housing Fund to housing authorities; $5.258bn FY2024)",
    before: perBn("sept27", RENTAL, ENTERPRISE_LINE), after: perBn("candidate", RENTAL, HOUSING_LINE),
    paying: legAt("candidate", "spending", RENTAL), receiving_before: legAt("sept27", "receipts", ENTERPRISE_LINE), receiving_after: legAt("candidate", "receipts", HOUSING_LINE),
    status: "no longer crosses: consolidated, and both legs are at the rental key and response 1" },
  { transfer: "other federal housing subsidies paid to housing authorities as landlords (Section 8 inside NIPA 3.13 line 4; unpublished detail)",
    before: perBn("sept27", RENTAL, ENTERPRISE_LINE), after: perBn("candidate", RENTAL, HOUSING_LINE),
    paying: legAt("candidate", "spending", RENTAL), receiving_before: legAt("sept27", "receipts", ENTERPRISE_LINE), receiving_after: legAt("candidate", "receipts", HOUSING_LINE),
    status: "no longer crosses where it lands in NIPA 3.8 line 13 (housing and urban renewal), now at the rental key" },
  { transfer: "federal operating subsidies to state and local mass transit (NIPA 3.13 line 7, federal 'Other', $24.627bn in 2024, footnote: largely railroads, mass transit and the FCIC)",
    before: perBn("sept27", "other_subsidies", ENTERPRISE_LINE), after: perBn("candidate", "other_subsidies", ENTERPRISE_LINE),
    paying: legAt("candidate", "spending", "other_subsidies"), receiving_before: legAt("sept27", "receipts", ENTERPRISE_LINE), receiving_after: legAt("candidate", "receipts", ENTERPRISE_LINE),
    status: "still crosses: the paying leg is a business subsidy held at response 0, the transit surplus sits in enterprise_surplus at the population key and response 1; the amount is not published separately [UNVERIFIED]" },
  { transfer: "federal subsidies to the Federal Crop Insurance Corporation (same NIPA 3.13 line 7)",
    before: perBn("sept27", "other_subsidies", ENTERPRISE_LINE), after: perBn("candidate", "other_subsidies", ENTERPRISE_LINE),
    paying: legAt("candidate", "spending", "other_subsidies"), receiving_before: legAt("sept27", "receipts", ENTERPRISE_LINE), receiving_after: legAt("candidate", "receipts", ENTERPRISE_LINE),
    status: "[UNVERIFIED] crosses only if the FCIC is a federal enterprise whose surplus includes the subsidy (MP-5 names subsidies from other levels of government)" },
];
const crossCsv = ["transfer,paying_leg,receiving_leg_sept27,receiving_leg_v2,sept27_spec48_m_per_bn,sept27_spec11_m_per_bn,v2_spec48_m_per_bn,v2_spec11_m_per_bn,status"]
  .concat(CROSSINGS.map((x) => [`"${x.transfer}"`, `"${x.paying}"`, `"${x.receiving_before}"`, `"${x.receiving_after}"`, x.before[0].toFixed(2), x.before[1].toFixed(2),
    x.after[0].toFixed(2), x.after[1].toFixed(2), `"${x.status}"`].join(",")));

const roadCsv = ["road_case,long_run_variant,lanes,lane_cut_spec48,lane_cut_spec11,account_spec48_bn,account_spec11_bn,account_change_spec48_bn,account_change_spec11_bn,"
  + "congestion_spec48_bn,congestion_spec11_bn,congestion_change_spec48_bn,congestion_change_spec11_bn,net_change_spec48_bn,net_change_spec11_bn,"
  + "congestion_spec48_min_bn,congestion_spec48_max_bn,congestion_spec11_min_bn,congestion_spec11_max_bn,road_return_removed_spec48_bn,road_return_removed_spec11_bn,band_low_bn,band_high_bn,end_specifications"]
  .concat(roadGrid.map((g) => [g.road_case, g.long_run, `"${g.lanes}"`, g.lane_cut[0].toFixed(8), g.lane_cut[1].toFixed(8)].concat([...g.account_bn, ...g.account_change_bn,
    ...g.congestion_bn, ...g.congestion_change_bn, ...g.net_change_bn, ...g.congestion_range_bn[0], ...g.congestion_range_bn[1], ...g.road_return_removed_bn, ...g.band_bn].map(fx),
    [`"${g.end_specifications.map((e) => e.join("/")).join(" ")}"`]).join(",")));

const compCsv = ["component,label,v2_low_end_lo,v2_low_end_hi,v2_high_end_lo,v2_high_end_hi,v2_joint_low_end_lo,v2_joint_low_end_hi,v2_joint_high_end_lo,v2_joint_high_end_hi,"
  + "v1_low_end_lo,v1_low_end_hi,v1_high_end_lo,v1_high_end_hi,v1_joint_low_end_lo,v1_joint_low_end_hi,v1_joint_high_end_lo,v1_joint_high_end_hi,"
  + "sept27_low_end_lo,sept27_low_end_hi,sept27_high_end_lo,sept27_high_end_hi,sept27_joint_low_end_lo,sept27_joint_low_end_hi,sept27_joint_high_end_lo,sept27_joint_high_end_hi"]
  .concat(rangeC.components.map((x, k) => { const y = rangeV1.components[k], z = range27.components[k];
    const cols = (c) => [c.lo[0], c.hi[0], c.lo[1], c.hi[1], c.joint.lo[0], c.joint.hi[0], c.joint.lo[1], c.joint.hi[1]].map(fx);
    return [x.name, `"${x.label}"`, ...cols(x), ...cols(y), ...cols(z)].join(","); }));

const bandsRows = [
  ["sept27_case", "the September 27 case (adopted)", B.sept27, range27],
  ["first_candidate", "the first candidate (c313b53)", B.v1, rangeV1],
  ["item1_tenant_key_alone", "item 1 alone", B.item1],
  ["item1_tenant_key_unconsolidated_alone", "item 1 without consolidating the operating subsidy (beside)", B.item1_unconsolidated],
  ["item1_population_key_alone", "the first candidate's item 1 alone (beside)", B.item1_population_key],
  ["item2_production_row4_alone", "item 2 alone", B.item2],
  ["item3_tax_key_alone", "item 3 alone", B.item3],
  ["candidate_v2", "candidate v2: items 1-3", B.candidate, rangeC],
  ["v2_housing_capital_tenant_key", "v2 with public housing's capital at the rental key (a range variant)", B.housing_capital_tenants],
  ...PAYS.map((p) => [`v2_public_pay_${p}`, `v2 with public pay, ${p.replace(/_/g, " ")} (beside)`, B[`pay_${p}`]]),
  ...ROAD_MOVES.map((rc) => [`v2_road_${rc}`, `v2, road arm at ${rc.replace(/_/g, " ")}, account only (beside)`, B[`road_${rc}`]]),
];
const bandsCsv = ["case,label,cost_low_bn,cost_high_bn,outer_account_low_bn,outer_account_high_bn,outer_joint_low_bn,outer_joint_high_bn,"
  + "quadrature_account_low_bn,quadrature_account_high_bn,quadrature_joint_low_bn,quadrature_joint_high_bn"]
  .concat(bandsRows.map(([k, label, b, r]) => [k, `"${label}"`, fx(b[0]), fx(b[1])].concat(r
    ? [r.overall[0], r.overall[1], r.joint.overall[0], r.joint.overall[1], r.quadrature[0], r.quadrature[1], r.joint.quadrature[0], r.joint.quadrature[1]].map(fx)
    : ["", "", "", "", "", "", "", ""]).join(",")));

const perHead = ["method", "spec", "twin", "allocation", "normalization", "share", "reading", "gg", "uc", "rate", "sept27_cost_bn", "first_candidate_cost_bn",
  "v2_cost_bn", "item1_bn", "item1_population_key_bn", "item2_bn", "item3_bn", "rental_key", "enterprise_key", "housing_line_key", "housing_line_response",
  "tax_edit_bn", "P_plus_F_sept27_bn", "P_plus_F_v2_bn", "public_pay_counterfactual_low_share_bn", "public_pay_counterfactual_high_share_bn"];
const perSpec = [perHead.join(",")].concat(METHODS.flatMap((meth, m) => X.candidate.idx.map((i) => { const s = X.candidate.specs[i], r = X.candidate.runs[m][i];
  const x = row(r, "receipts", HOUSING_LINE);
  return [meth, i, twinOf(X.candidate, i), s.allocation, s.normalization, s.share, s.reading, s.gg, s.uc, s.rate, X.sept27.costs[m][i], X.v1.costs[m][i],
    X.candidate.costs[m][i], d1[m][i], d1pop[m][i], d2[m][i], d3[m][i], keyOf(r, "spending", RENTAL), keyOf(r, "receipts", ENTERPRISE_LINE),
    x.amount_bn / x.national_bn, x.response, by[m][s.allocation], X.sept27.runs[m][i].evaluation.production_gain_bn, r.evaluation.production_gain_bn,
    payOf("pay_counterfactual_low_share", m, i), payOf("pay_counterfactual_high_share", m, i)].map(full).join(","); })));

const compOut = (r) => r.components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi, joint_lo: x.joint.lo, joint_hi: x.joint.hi,
  variants: Object.fromEntries(x.devs.map((d) => [d.v, { account_bn: d.d, joint_bn: d.j, congestion_change_bn: d.congestion_change,
    end_specifications: d.ends.map((e) => e.join("/")).join(" ") }])) }));
const rangeOut = (r) => ({ band: r.band, low_end: r.low_end, high_end: r.high_end, overall: r.overall, quadrature: r.quadrature,
  congestion_at_band_ends_bn: r.congestion_at_ends, joint: r.joint });
const inputs = [C.ESV_FILE, C.TAX_FILE, TR_FILE, C.PRODUCTION_FILE, C.STOCK_FILE, RC_FILE, `${SEPT27_DIR}/corrections.json`, `${SEPT27_DIR}/summary.json`,
  `${SEPT27_DIR}/per_spec.csv`, `${V1_DIR}/summary.json`, `${V1_DIR}/per_spec.csv`, pkgFile, "main_case_candidate_2026_09_28/package.cjs",
  "main_case_long_run_2026_09_27/package.cjs"];
const summary = {
  lane: C.LANE, case: C.CASE, status: "candidate, not adopted (BRIEF.md, 08b1b7d)",
  imports: "main_case_candidate_2026_09_28/package.cjs (c313b53), which imports main_case_long_run_2026_09_27/package.cjs; neither edited",
  sept27_case: B.sept27, first_candidate: B.v1, candidate_v2: B.candidate, candidate_v2_end_specifications: E.candidate,
  at_fixed_specifications: Object.fromEntries(FIXED.map(([k, label, v, place]) => [k, Object.assign({ label, placement: place }, v)])),
  item1: { housing_surplus_bn: H, transfer_bn: T, enterprise_national_bn: [E_NATIONAL, E_NATIONAL - H], rental_national_bn: [H_NATIONAL, H_NATIONAL - T],
    housing_line_national_bn: H - T, change_at_fixed_specs_bn: d1Ends, population_key_reading_bn: atEnds((m, i) => d1pop[m][i]),
    keys_at_fixed_specs: { rental: atEnds((m, i) => keyOf(X.candidate.runs[m][i], "spending", RENTAL)), enterprise: atEnds((m, i) => keyOf(X.sept27.runs[m][i], "receipts", ENTERPRISE_LINE)) },
    control_today_spec48_capital_off_bn: today48, control_v2_max_bn: splitGaps, control_v2_at_response_0_37_spec48_bn: sens48,
    first_candidate_after_gate_identity_max_bn: idGaps,
    source: { nipa_3_8_line_13: "housing and urban renewal, current surplus 2024 (capital_return_services_2026_09_27/derived/enterprise_surplus_vs_return.csv, from NIPA Section 3 T30800-A)",
      transfer: TRANSFERS.public_housing_operating } },
  item2: { change_bn: PROD.cost_change_at_reference_bn, change_at_fixed_specs_bn: d2Ends },
  item3: { line: TAX_LINE, national_bn: TAX.national_bn, share_change: TAX.share_change[TV], edit_by_method_bn: Object.fromEntries(METHODS.map((meth, m) => [meth, by[m]])),
    change_at_fixed_specs_bn: d3Ends, tax_lane_band_on_sept27: TR.variants[TV].band },
  public_pay: { removal_shares: { v2: shV2, first_candidate: shV1 },
    at_fixed_specs_bn: Object.fromEntries(PAYS.map((p) => [p, { v2: payAt(`pay_${p}`), first_candidate: payAt(`v1_pay_${p}`) }])),
    bands_bn: Object.fromEntries(PAYS.map((p) => [p, B[`pay_${p}`]])), end_specifications: Object.fromEntries(PAYS.map((p) => [p, E[`pay_${p}`]])),
    approximation: "a uniform removal share across skill groups: the account's removal share of government consumption, all consumption lines (low share) or without defense and with the school rows (high share)" },
  road_arm: { grid: roadGrid, stationary_congestion_bn: cong0, b1_lanes_fixed_bn: RC.b1_lanes_fixed_bn,
    construction: { year_effects: ci.year_effects, land: ci.land, stock_responses_low_end: STOCK.stock_responses_low_end, operations: STOCK.operations_across_states } },
  crossings: CROSSINGS,
  ends: endRows,
  range: { sept27: rangeOut(range27), first_candidate: rangeOut(rangeV1), candidate_v2: rangeOut(rangeC),
    attack_recipe: { first_candidate: attackV1, candidate_v2: attackC },
    note: "account: the September 27 components re-run on each base at every specification; joint: each variant's change in the account plus the congestion item at its band ends' lane cut (the dependent-pieces placement rule); attack_recipe: the long-run component alone at the fixed specifications 48 / 11 (probe_item45.cjs section 5c)" },
  components: { candidate_v2: compOut(rangeC), first_candidate: compOut(rangeV1), sept27: compOut(range27) },
  specifications: { total: 64, distinct: 32, twins: "48 = 52 and 11 = 15 (the school dimension has been overridden to full cost since 2026-09-26)" },
  inputs: Object.fromEntries(inputs.map((f) => [f, C.sha256(f)])),
};
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "fixed_specs.csv"), fixedCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "candidate_bands.csv"), bandsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "ends.csv"), endsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "components.csv"), compCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "road_arm.csv"), roadCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "crossings.csv"), crossCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");

console.log("\n[result]");
for (const [k, , b, r] of bandsRows) console.log(`  ${k.padEnd(40)} ${f2(b)}${r ? `   outer ${f2(r.overall)}, joint ${f2(r.joint.overall)}` : ""}`);
for (const [k, , v] of FIXED) console.log(`    ${k.padEnd(44)} 48: ${fx(v.old[0])} -> ${fx(v.new[0])} (${v.change[0] >= 0 ? "+" : ""}${fx(v.change[0])})   11: ${fx(v.old[1])} -> ${fx(v.new[1])} (${v.change[1] >= 0 ? "+" : ""}${fx(v.change[1])})`);
for (const g of roadGrid) console.log(`  road ${g.road_case.padEnd(26)} ${g.long_run.padEnd(28)} account ${f2(g.account_change_bn)}  congestion ${f2(g.congestion_bn)} (${f2(g.congestion_change_bn)})  net ${f2(g.net_change_bn)}`);
for (const x of CROSSINGS) console.log(`  crossing: ${x.transfer.slice(0, 60)}... ${x.before.map((v) => v.toFixed(2)).join(" / ")} -> ${x.after.map((v) => v.toFixed(2)).join(" / ")} $m per $1bn`);
for (const r of endRows.filter((z) => ["sept27", "v1", "candidate"].includes(z.set))) console.log(`  ends ${r.set.padEnd(10)} ${r.method.padEnd(24)} low ${r.low} (next ${r.low_runner_up} +${fx(r.low_margin)}), high ${r.high} (next ${r.high_runner_up} -${fx(r.high_margin)})`);
console.log(`  attack's recipe (long-run only, fixed specs): first candidate ${f2(attackV1.overall)}; v2 ${f2(attackC.overall)}`);
console.log("all gates passed");
