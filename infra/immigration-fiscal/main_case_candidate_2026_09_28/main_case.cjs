/* The candidate revision sept28_candidate (BRIEF.md, e003ea1): gates, then derived/. package.cjs holds the definitions;
 * production_row4.py writes the production grid and the public-pay charge they read, road_congestion.py the congestion
 * item at every long-run road response.
 *
 * Base: the September 27 case (main_case_long_run_2026_09_27, $321.8194–387.3701bn, end specifications 48 / 11),
 * reproduced exactly before anything changes. Then each item alone on that case, each gated to move only its own
 * lines by exactly its own amount:
 *   1. transfer consolidation: the rental line and the enterprise surplus alone move, by r_e ke T - r_h kh T; the
 *      audit's synthetic $1bn moves today's case by kh - ke and the consolidated case by 0 (1e-9);
 *   2. production on the row-4 weights: no line moves; the cost moves by -(P + F)'s change at the specification's
 *      normalization;
 *   3. the road arm: economic_affairs_services' response and the road capital components alone move; each physical
 *      case is then run at every long-run variant with the congestion item beside it at the same highway response;
 *   4. public pay (beside the range): nothing moves; the cost rises by the charge.
 * Items 1-3 together add exactly, at every specification. An independent path (engine, model.json, the September 27
 * corrections.json and the candidate's two data inputs) gives the candidate at every specification.
 * Comparisons are at the fixed specifications 48 (low end) and 11 (high end), never as a difference of band ends.
 * The outer range re-runs the September 27 components on the candidate; on the September 27 case they reproduce its
 * published range first.
 * Run from anywhere, after production_row4.py and road_congestion.py: node main_case.cjs [--out-dir DIR] ->
 * derived/candidate_bands.csv, fixed_specs.csv, components.csv, per_spec.csv, road_arm.csv, summary.json.
 * Gates exit 1 and nothing is written on failure.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const C = require("./package.cjs");
const S = C.SEPT27;
const { Engine, MODEL, HERE, METHODS, CASES, CONSTANTS, LTSS_RANGE, CK_SPECS, benefitSe, CAP, LONG_RUN_VARIANTS, RENTAL,
  ENTERPRISE_LINE, ROAD_LINE, ROAD_COMPONENTS, ROAD_SUBFUNCTIONS, ROAD_CASES, DEPRECIATION, LINE_NATIONAL, TRANSFERS, PROD,
  CANDIDATE, OFF, gateState, gate, near, f2, csvRows, readJson, withCentral, specsFor, modelFor, evaluateFull, evalPackage,
  withProduction, consolidate, withSyntheticTransfer, depreciationCut, congestionOf, publicPayOf } = C;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const ex = (x) => x.toExponential(1);
const ENDS = [48, 11];
// A quantity at the fixed end specifications, each method's value averaged: [spec 48, spec 11].
const atEnds = (f) => ENDS.map((i) => mean(METHODS.map((_, m) => f(m, i))));
const runsOf = (o, profile, models) => {
  const oo = withCentral(o);
  const specs = specsFor(oo);
  return METHODS.map((meth, k) => {
    const m = models ? models[k] : modelFor("central", meth, oo);
    return specs.map((s) => evaluateFull(m, s, profile));
  });
};
const costsOf = (rs) => rs.map((xs) => xs.map((r) => r.cost_bn));
const bandOf = (cm) => [mean(cm.map((xs) => Math.min(...xs))), mean(cm.map((xs) => Math.max(...xs)))];
const endsOf = (cm) => cm.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
const row = (r, side, id) => r.evaluation[side].find((l) => l.id === id);
const keyOf = (r, side, id) => row(r, side, id).amount_bn / row(r, side, id).national_bn;
const withOff = (x) => Object.assign({}, OFF, x);
const withCand = (x) => Object.assign({}, CANDIDATE, x);
const SEPT27_DIR = "main_case_long_run_2026_09_27/derived";
const s27 = readJson(`${SEPT27_DIR}/summary.json`);

// Every line but the named ones keeps its amount, response and effect exactly; the capital components but the named
// ones keep their return (to tol); P and F are unchanged unless production moves.
function onlyMoves(a, b, lines, comps, tol, production) {
  const sides = ["spending", "receipts"];
  const bad = [];
  for (const side of sides) a.evaluation[side].forEach((x, k) => {
    const y = b.evaluation[side][k];
    if (x.id !== y.id) bad.push(`order ${x.id}`);
    else if (!lines.includes(`${side}:${x.id}`) && (x.amount_bn !== y.amount_bn || x.response !== y.response || x.effect_bn !== y.effect_bn)) bad.push(`${side}:${x.id}`);
  });
  a.capital.components.forEach((x, k) => {
    const y = b.capital.components[k];
    if (x.id !== y.id) bad.push(`order ${x.id}`);
    else if (!comps.includes(x.id) && Math.abs(x.return_bn - y.return_bn) > tol) bad.push(`capital:${x.id}`);
  });
  if (!production && (a.evaluation.private_wtp_bn !== b.evaluation.private_wtp_bn || a.evaluation.induced_receipts_bn !== b.evaluation.induced_receipts_bn)) bad.push("production");
  return bad;
}

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the September 27 case]");
const SETS = {
  sept27: OFF,
  item1: withOff({ internal_transfer: "public_housing_operating" }),
  item1_bound: withOff({ internal_transfer: "all_of_line_4" }),
  item2: withOff({ production: "row4" }),
  item3_replacement: withOff({ road: "replacement" }),
  item3_fixed_stock: withOff({ road: "fixed_stock" }),
  item4_public_pay: withOff({ public_pay: true }),
  candidate: CANDIDATE,
  candidate_road_replacement: withCand({ road: "replacement" }),
  candidate_road_fixed_stock: withCand({ road: "fixed_stock" }),
  candidate_public_pay: withCand({ public_pay: true }),
  candidate_transfer_bound: withCand({ internal_transfer: "all_of_line_4" }),
};
const R = Object.fromEntries(Object.entries(SETS).map(([k, o]) => [k, runsOf(o)]));
const K = Object.fromEntries(Object.entries(R).map(([k, rs]) => [k, costsOf(rs)]));
const B = Object.fromEntries(Object.entries(K).map(([k, cm]) => [k, bandOf(cm)]));
const own27 = METHODS.map((meth) => {
  const oo = S.withCentral({});
  const m = S.modelFor("central", meth, oo);
  return S.specsFor(oo).map((s) => S.evaluateFull(m, s).cost_bn);
});
gate("the September 27 package reproduces its published case", (() => { const c = S.central({});
  return near(c[0], s27.main_case[0], 1e-9) && near(c[1], s27.main_case[1], 1e-9); })(), f2(s27.main_case));
gate("with every item off, the candidate package is the September 27 case at every specification exactly (both methods)",
  K.sept27.every((xs, m) => xs.every((x, i) => x === own27[m][i])), `${K.sept27.length} x ${K.sept27[0].length}`);
const per27 = csvRows(`${SEPT27_DIR}/per_spec.csv`);
gate("...and its committed per_spec.csv costs exactly", per27.length === 128 && per27.every((r) =>
  Number(r.cost_bn) === K.sept27[METHODS.indexOf(r.method)][Number(r.spec)]), "128 rows");
gate("the September 27 band and end specifications 48 / 11", near(B.sept27[0], s27.main_case[0], 1e-9) && near(B.sept27[1], s27.main_case[1], 1e-9)
  && endsOf(K.sept27).every((e) => e[0] === 48 && e[1] === 11), f2(B.sept27));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 2, production on the row-4 weights]");
const dims = Engine.PRODUCTION_DIMS;
const pubGap = worst(["private_wtp_bn", "induced_receipts_bn"].flatMap((k) => PROD.grid.published[k].map((x, i) => x - MODEL.production[k][i])));
gate("the file's published grid is model.json's (P and F, 3,888 cells, within 2e-9: both are rounded)", pubGap < 2e-9, `max |diff| ${ex(pubGap)}`);
const refIndex = (normalization) => Engine.productionIndex(MODEL, Object.assign({}, MODEL.production.reference, { normalization }));
const pf = (name, normalization) => PROD.grid[name].private_wtp_bn[refIndex(normalization)] + PROD.grid[name].induced_receipts_bn[refIndex(normalization)];
gate("the reference cells are the file's reference rows (GDP index 1716, cash 1230)", ["cash", "gdp"].every((n) =>
  refIndex(n) === PROD.reference.row4[n].index && Math.abs(pf("row4", n) - PROD.reference.row4[n].P_plus_F_bn) < 2e-9), dims.join(","));
const d2 = K.item2.map((xs, m) => xs.map((x, i) => x - K.sept27[m][i]));
const d2Gap = worst(R.item2.flatMap((xs, m) => xs.map((r, i) => d2[m][i]
  + (r.evaluation.production_gain_bn - R.sept27[m][i].evaluation.production_gain_bn))));
gate("item 2 moves the cost by minus the change in P + F at every specification", d2Gap < 1e-9, `max |diff| ${ex(d2Gap)}`);
const d2Rows = R.item2.flatMap((xs, m) => xs.map((r, i) => onlyMoves(r, R.sept27[m][i], [], [], 0, true))).flat();
gate("item 2 moves no line, no capital component", d2Rows.length === 0, d2Rows.slice(0, 5).join(" ") || "exact");
const d2Ends = atEnds((m, i) => d2[m][i]);
gate("item 2 at the fixed specifications is the probe's +1.642719 / +1.107389 (production_row4.json)",
  near(d2Ends[0], PROD.cost_change_at_reference_bn.gdp, 1e-9) && near(d2Ends[1], PROD.cost_change_at_reference_bn.cash, 1e-9), f2(d2Ends));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 1, transfer consolidation]");
const T = TRANSFERS.public_housing_operating.bn;
const m27 = METHODS.map((meth) => modelFor("central", meth, withCentral(OFF)));
const specs27 = specsFor(OFF);
const costWith = (m, specs, profile) => specs.map((s) => evaluateFull(m, s, profile).cost_bn);
// Today: a synthetic $1bn on both legs moves the case by kh - ke (each leg's own attributed fraction).
const synth = m27.map((m) => withSyntheticTransfer(m, 1));
const todayGap = worst(METHODS.flatMap((_, m) => specs27.map((s, i) => {
  const r = R.sept27[m][i];
  const kh = keyOf(r, "spending", RENTAL), ke = keyOf(r, "receipts", ENTERPRISE_LINE);
  return costWith(synth[m], [s])[0] - r.cost_bn - (kh - ke);
})));
gate("today the synthetic $1bn moves the case by kh - ke at every specification (both legs at 1)", todayGap < 1e-9, `max |diff| ${ex(todayGap)}`);
const noCap = specsFor(withOff({ capital: false }));
const today48 = METHODS.map((_, m) => costWith(synth[m], [noCap[48]])[0] - costWith(m27[m], [noCap[48]])[0]);
gate("the audit's positive control: at specification 48, capital off, it lowers the cost by $40.75–43.19 million (3db388d section 7)",
  near(Math.min(...today48.map(Math.abs)), 0.04075, 5e-6) && near(Math.max(...today48.map(Math.abs)), 0.04319, 5e-6) && today48.every((x) => x < 0),
  today48.map((x) => (1000 * x).toFixed(4) + "m").join(" / "));
// After the fix: consolidating the transfer (T + the synthetic $1bn) leaves the case exactly where consolidating T does,
// in every profile, with the receipt at a response other than 1, and on the candidate's production.
const controlCases = [
  ["main profile", OFF, undefined],
  ["long_run_non_school_fixed", OFF, "long_run_non_school_fixed"],
  ["proportional reference", OFF, "proportional_reference"],
  ["enterprise receipt at 0.37", withOff({ enterprise_receipt: 0.37 }), undefined],
  ["candidate production and responses", CANDIDATE, undefined],
];
for (const [label, o, profile] of controlCases) {
  const oo = withCentral(o), specs = specsFor(oo);
  const gap = worst(METHODS.flatMap((meth) => {
    const base = withProduction(S.modelFor("central", meth, oo), oo.production);
    const a = costWith(consolidate(base, T), specs, profile);
    const b = costWith(consolidate(withSyntheticTransfer(base, 1), T + 1), specs, profile);
    return a.map((x, i) => b[i] - x);
  }));
  gate(`after consolidation the synthetic $1bn moves the case by 0 (${label}, every specification, 1e-9)`, gap < 1e-9, `max |diff| ${ex(gap)}`);
}
const d1 = K.item1.map((xs, m) => xs.map((x, i) => x - K.sept27[m][i]));
const d1Gap = worst(R.item1.flatMap((xs, m) => xs.map((r, i) => {
  const o = R.sept27[m][i];
  const h = row(o, "spending", RENTAL), e = row(o, "receipts", ENTERPRISE_LINE);
  return d1[m][i] - (e.response * keyOf(o, "receipts", ENTERPRISE_LINE) * T - h.response * keyOf(o, "spending", RENTAL) * T);
})));
gate("item 1 moves the cost by r_e ke T - r_h kh T at every specification", d1Gap < 1e-9, `max |diff| ${ex(d1Gap)}`);
const d1Rows = R.item1.flatMap((xs, m) => xs.map((r, i) => onlyMoves(r, R.sept27[m][i], [`spending:${RENTAL}`, `receipts:${ENTERPRISE_LINE}`], [], 1e-12, false))).flat();
gate("item 1 moves no other line and no capital component (1e-12)", d1Rows.length === 0, d1Rows.slice(0, 5).join(" ") || "exact");
const keyGap = worst(R.item1.flatMap((xs, m) => xs.flatMap((r, i) => [keyOf(r, "spending", RENTAL) - keyOf(R.sept27[m][i], "spending", RENTAL),
  keyOf(r, "receipts", ENTERPRISE_LINE) - keyOf(R.sept27[m][i], "receipts", ENTERPRISE_LINE)])));
const nat0 = { h: MODEL.spending.lines.find((l) => l.id === RENTAL).national_bn, e: MODEL.receipts.lines.find((l) => l.id === ENTERPRISE_LINE).national_bn };
const natOk = R.item1.every((xs) => xs.every((r) => near(row(r, "spending", RENTAL).national_bn, nat0.h - T, 1e-12)
  && near(row(r, "receipts", ENTERPRISE_LINE).national_bn, nat0.e - T, 1e-12)));
gate("both legs lose T nationally and keep their keys (1e-15)", natOk && keyGap < 1e-15,
  `T = ${T} bn; ${RENTAL} ${nat0.h} -> ${nat0.h - T}, ${ENTERPRISE_LINE} ${nat0.e} -> ${nat0.e - T}; key |diff| ${ex(keyGap)}`);
const d1b = K.item1_bound.map((xs, m) => xs.map((x, i) => x - K.sept27[m][i]));
const d1bEnds = atEnds((m, i) => d1b[m][i]);
const bound27 = s27.enterprises.overlap_with_rental_assistance.upper_bound_bn;
gate("the bound, all of line 4, is the September 27 overlap bound (summary enterprises.overlap_with_rental_assistance)",
  near(d1bEnds[0], bound27[0], 1e-9) && near(d1bEnds[1], bound27[1], 1e-9), f2(d1bEnds));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 3, the road arm]");
const roadIds = Object.values(ROAD_COMPONENTS);
const d3 = {};
for (const rc of ["replacement", "fixed_stock"]) {
  const key = `item3_${rc}`;
  d3[rc] = K[key].map((xs, m) => xs.map((x, i) => x - K.sept27[m][i]));
  const gap = worst(R[key].flatMap((xs, m) => xs.map((r, i) => {
    const o = R.sept27[m][i];
    const ea = row(o, "spending", ROAD_LINE), eaNew = row(r, "spending", ROAD_LINE);
    const roadReturn = o.capital.components.filter((c) => roadIds.includes(c.id)).reduce((a, c) => a + c.return_bn, 0);
    return d3[rc][m][i] - (-ea.amount_bn * (ea.response - eaNew.response) - roadReturn);
  })));
  gate(`${rc}: the cost falls by the road capital return and, in a fixed stock, the road depreciation no longer saved (1e-9)`, gap < 1e-9, `max |diff| ${ex(gap)}`);
  const rows = R[key].flatMap((xs, m) => xs.map((r, i) => onlyMoves(r, R.sept27[m][i], [`spending:${ROAD_LINE}`], roadIds, 0, false))).flat();
  gate(`${rc}: no other line, no other capital component moves`, rows.length === 0, rows.slice(0, 5).join(" ") || "exact");
}
const cutGap = worst(R.item3_fixed_stock.flatMap((xs, m) => xs.map((r, i) => {
  const s = specs27[i];
  const want = ROAD_SUBFUNCTIONS.reduce((a, sf) => a + DEPRECIATION[sf] * S.subfunctionResponses("adopted", s.reading)[sf], 0) / LINE_NATIONAL;
  return (row(R.sept27[m][i], "spending", ROAD_LINE).response - row(r, "spending", ROAD_LINE).response) - want;
})));
gate("fixed stock: the line's response falls by the road depreciation at the road response over the line's national total", cutGap < 1e-12,
  `cut ${depreciationCut("adopted", "low").toFixed(6)} low, ${depreciationCut("adopted", "high").toFixed(6)} high`);
gate("replacement: the line's response does not move", R.item3_replacement.every((xs, m) => xs.every((r, i) =>
  row(r, "spending", ROAD_LINE).response === row(R.sept27[m][i], "spending", ROAD_LINE).response)), "every specification");
// The congestion bridge was computed at the September 27 ends; it carries to the candidate if the road key and the road
// response there are the bridge's.
const bridge = csvRows(C.CONGESTION_FILE);
// The highway response of a long-run variant at a reading: S&L and federal highways weighted by national amount (the bridge's h).
const roadSfs = C.LR.lines[ROAD_LINE].subfunctions.filter((s) => ROAD_SUBFUNCTIONS.includes(s.id));
const hOf = (v, rd) => { const r = S.subfunctionResponses(v, rd);
  return roadSfs.reduce((a, s) => a + s.national_bn * r[s.id], 0) / roadSfs.reduce((a, s) => a + s.national_bn, 0); };
const eaKey = atEnds((m, i) => keyOf(R.candidate[m][i], "spending", ROAD_LINE));
const bridgeOk = ["low", "high"].every((rd, e) => {
  const b = bridge.find((x) => x.band_end === rd && x.variant === "network follows spending" && x.geography === "uniform (account key)");
  return near(Number(b.key_share), eaKey[e], 1e-9) && near(Number(b.highway_response), hOf("adopted", rd), 1e-9);
});
gate("the congestion bridge's road key and highway response are the candidate's at 48 / 11 (1e-9)", bridgeOk,
  `key ${eaKey.map((x) => x.toFixed(9)).join(" / ")}`);
const cong27 = s27.beside_the_account.congestion;
gate("stationary network: congestion is the September 27 case's beside the account (the bridge's 10 digits, 1e-8)",
  near(congestionOf("stationary_network", "low").congestion_bn, cong27.low_end.congestion_bn, 1e-8)
  && near(congestionOf("stationary_network", "high").congestion_bn, cong27.high_end.congestion_bn, 1e-8), `${cong27.low_end.congestion_bn.toFixed(4)} / ${cong27.high_end.congestion_bn.toFixed(4)}`);
gate("fixed lanes: congestion is the lanes-fixed B1, $19.16bn (net_change.json b1_lanes_fixed_bn, 1e-8)",
  ["low", "high"].every((rd) => near(congestionOf("fixed_stock", rd).congestion_bn, cong27.before_bn, 1e-8)
    && near(congestionOf("replacement", rd).congestion_bn, cong27.before_bn, 1e-8)), cong27.before_bn.toFixed(4));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 4, public pay]");
const d4 = K.item4_public_pay.map((xs, m) => xs.map((x, i) => x - K.sept27[m][i]));
const d4Gap = worst(d4.flatMap((xs) => xs.map((x, i) => x - publicPayOf("published", specs27[i].normalization))));
gate("public pay adds the charge at the specification's normalization (1e-12)", d4Gap < 1e-12, `max |diff| ${ex(d4Gap)}`);
const d4Rows = R.item4_public_pay.flatMap((xs, m) => xs.map((r, i) => onlyMoves(r, R.sept27[m][i], [], [], 0, false))).flat();
gate("public pay moves no line and no capital component", d4Rows.length === 0, d4Rows.slice(0, 5).join(" ") || "exact");

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: items together]");
const dC = (key) => K[key].map((xs, m) => xs.map((x, i) => x - K.sept27[m][i]));
const addGap = (key, parts) => worst(dC(key).flatMap((xs, m) => xs.map((x, i) => x - parts.reduce((a, p) => a + p(m, i), 0))));
const p1 = (m, i) => d1[m][i], p2 = (m, i) => d2[m][i];
const payRow4 = (m, i) => publicPayOf("row4", specs27[i].normalization);
const together = {
  candidate: addGap("candidate", [p1, p2]),
  candidate_road_replacement: addGap("candidate_road_replacement", [p1, p2, (m, i) => d3.replacement[m][i]]),
  candidate_road_fixed_stock: addGap("candidate_road_fixed_stock", [p1, p2, (m, i) => d3.fixed_stock[m][i]]),
  candidate_public_pay: addGap("candidate_public_pay", [p1, p2, payRow4]),
  candidate_transfer_bound: addGap("candidate_transfer_bound", [(m, i) => d1b[m][i], p2]),
};
gate("items 1-3 and the variants add exactly on the candidate, every specification (1e-9)", worst(Object.values(together)) < 1e-9,
  Object.entries(together).map(([k, v]) => `${k.replace("candidate_", "")} ${ex(v)}`).join(", "));
const candEnds = endsOf(K.candidate);
gate("the candidate keeps the end specifications 48 / 11 in both methods", candEnds.every((e) => e[0] === 48 && e[1] === 11), JSON.stringify(candEnds));
const CB = C.central({});
gate("the candidate's per-specification costs give its band", near(CB[0], B.candidate[0], 1e-9) && near(CB[1], B.candidate[1], 1e-9), f2(CB));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the road arm at every long-run response]");
// The arm: each physical case (ROAD_CASES) at each long-run variant, the account on the candidate at the fixed
// specifications and the congestion item beside it at the same highway response (road_congestion.py; lanes follow
// spending in the stationary network and stay, the B1, in the other two cases).
const RC_FILE = "main_case_candidate_2026_09_28/derived/road_congestion.json";
if (!fs.existsSync(path.join(C.FISCAL, RC_FILE))) {
  console.error(`[BLOCKED] ${RC_FILE} is missing: run road_congestion.py first`);
  process.exit(1);
}
const RC = readJson(RC_FILE);
gate("road_congestion.json: all its gates passed", Array.isArray(RC.gates) && RC.gates.length > 0 && RC.gates.every((g) => g.passed), `${RC.gates.length} gates`);
const VARS = Object.keys(LONG_RUN_VARIANTS);
gate("its highway responses (every variant, both readings) and road keys are the package's at 48 / 11 (1e-15)",
  VARS.every((v) => ["low", "high"].every((rd) => near(RC.highway_response[v][rd], hOf(v, rd), 1e-15)))
  && near(RC.key.low, eaKey[0], 1e-15) && near(RC.key.high, eaKey[1], 1e-15), `${VARS.length} variants`);
const rcRow = (v, rd) => RC.rows.find((x) => x.variant === v && x.reading === rd);
gate("its adopted rows are the bridge's (1e-8) and its B1 the September 27 case's before_bn (1e-9)",
  ["low", "high"].every((rd) => near(rcRow("adopted", rd).congestion_central_bn, congestionOf("stationary_network", rd).congestion_bn, 1e-8))
  && near(RC.b1_lanes_fixed_bn, cong27.before_bn, 1e-9), `${rcRow("adopted", "low").congestion_central_bn.toFixed(4)} / ${rcRow("adopted", "high").congestion_central_bn.toFixed(4)}`);
const congestionAt = (rc, v, rd) => (ROAD_CASES[rc].lanes === "network follows spending"
  ? { central: rcRow(v, rd).congestion_central_bn, range: [rcRow(v, rd).factorial_min_bn, rcRow(v, rd).factorial_max_bn] }
  : { central: RC.b1_lanes_fixed_bn, range: RC.b1_factorial_bn });
const acc0 = atEnds((m, i) => K.candidate[m][i]);
const cong0 = ["low", "high"].map((rd) => congestionAt("stationary_network", "adopted", rd).central);
const roadGrid = [];
for (const rc of Object.keys(ROAD_CASES)) for (const v of VARS) {
  const rs = runsOf(withCand({ road: rc, long_run: v }));
  const cm = costsOf(rs);
  const acc = atEnds((m, i) => cm[m][i]);
  const cg = ["low", "high"].map((rd) => congestionAt(rc, v, rd));
  roadGrid.push({ road_case: rc, long_run: v, costs: cm, band_bn: bandOf(cm), end_specifications: endsOf(cm), account_bn: acc,
    account_change_bn: [acc[0] - acc0[0], acc[1] - acc0[1]], congestion_bn: cg.map((x) => x.central), congestion_range_bn: cg.map((x) => x.range),
    congestion_change_bn: [cg[0].central - cong0[0], cg[1].central - cong0[1]],
    net_change_bn: [acc[0] - acc0[0] + cg[0].central - cong0[0], acc[1] - acc0[1] + cg[1].central - cong0[1]],
    road_return_removed_bn: atEnds((m, i) => rs[m][i].road_return_removed_bn) });
}
const gridAt = (rc, v) => roadGrid.find((x) => x.road_case === rc && x.long_run === v);
const sameCosts = (a, b) => a.every((xs, m) => xs.every((x, i) => x === b[m][i]));
gate("the arm at the adopted responses is the candidate and its two road cases, at every specification exactly",
  sameCosts(gridAt("stationary_network", "adopted").costs, K.candidate) && sameCosts(gridAt("replacement", "adopted").costs, K.candidate_road_replacement)
  && sameCosts(gridAt("fixed_stock", "adopted").costs, K.candidate_road_fixed_stock), "3 cases x 128");
// The candidate's range (rangeOn below): its long_run_response component re-runs each variant at every specification.
const rangeC = rangeOn(CANDIDATE);
const lrComp = (base) => base.components.find((x) => x.name === "long_run_response");
gate("the stationary network at each variant is the range component long_run_response's variant band (1e-9)",
  VARS.filter((v) => v !== "adopted").every((v) => { const d = lrComp(rangeC).devs.find((x) => x.v === v).d, b = gridAt("stationary_network", v).band_bn;
    return near(b[0] - B.candidate[0], d[0], 1e-9) && near(b[1] - B.candidate[1], d[1], 1e-9); }), `${VARS.length - 1} variants`);
gate("every case keeps a lower account than the stationary network where it keeps the road capital (each variant, both ends)",
  VARS.every((v) => ["replacement", "fixed_stock"].every((rc) => [0, 1].every((e) => gridAt(rc, v).account_bn[e] <= gridAt("stationary_network", v).account_bn[e] + 1e-12))),
  "replacement and fixed stock below the stationary network");
gate("congestion with lanes fixed is the B1 in both fixed-lane cases, at least the stationary network's", roadGrid.every((x) =>
  ROAD_CASES[x.road_case].lanes === "network follows spending" || x.congestion_bn.every((c) => c === RC.b1_lanes_fixed_bn))
  && VARS.every((v) => [0, 1].every((e) => gridAt("stationary_network", v).congestion_bn[e] <= RC.b1_lanes_fixed_bn + 1e-12)), `B1 ${RC.b1_lanes_fixed_bn.toFixed(4)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: an independent path]");
// The engine, model.json, the September 27 corrections.json, the internal transfer and production_row4.json's row-4
// grid; the specification grid, state, responses and capital return are rebuilt from the payload's meta.
function independentCosts(pay, grid, transfer) {
  const fisc = path.join(HERE, "..");
  const Eng = require(path.join(fisc, "assumption_explorer_2026_09_21", "engine.js"));
  const model = JSON.parse(fs.readFileSync(path.join(fisc, "assumption_explorer_2026_09_21", "derived", "model.json"), "utf8"));
  const m = Eng.applyCorrections(model, { lines: pay.lines, edits: pay.edits });
  m.production.private_wtp_bn = grid.private_wtp_bn;
  m.production.induced_receipts_bn = grid.induced_receipts_bn;
  const hl = m.spending.lines.find((l) => l.id === "housing_subsidies"), el = m.receipts.lines.find((l) => l.id === "enterprise_surplus");
  const fh = (hl.national_bn - transfer) / hl.national_bn, fe = (el.national_bn - transfer) / el.national_bn;
  for (const k of Object.values(hl.keys)) for (const a of ["personal", "shared"]) { k[a].target_bn *= fh; k[a].other_bn *= fh; }
  for (const k of Object.values(el.cells)) for (const a of ["personal", "shared"]) { k[a].target_bn *= fe; k[a].other_bn *= fe; }
  hl.national_bn -= transfer; el.national_bn -= transfer;
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
const independent = independentCosts(payload27, PROD.grid.row4, T);
const methodMean = specs27.map((_, i) => mean(K.candidate.map((xs) => xs[i])));
const indGap = worst(independent.map((x, i) => x - methodMean[i]));
gate("independent path: engine + model.json + the September 27 corrections.json + T + the row-4 grid give the candidate at every specification (1e-9)",
  independent.length === 64 && indGap < 1e-9, `max |diff| ${ex(indGap)} against the two methods' mean`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[range]");
// The September 27 components (its main_case.cjs), each variant re-run on a base case at every specification.
function rangeOn(base) {
  const centralOn = (o) => C.central(Object.assign({}, base, o));
  const Cb = centralOn({});
  const comps = [];
  const component = (name, label, variants) => {
    const devs = variants.map(([v, b]) => ({ v, d: [b[0] - Cb[0], b[1] - Cb[1]] }));
    comps.push({ name, label, devs,
      lo: [Math.min(0, ...devs.map((x) => x.d[0])), Math.min(0, ...devs.map((x) => x.d[1]))],
      hi: [Math.max(0, ...devs.map((x) => x.d[0])), Math.max(0, ...devs.map((x) => x.d[1]))] });
  };
  component("tax_block", "tax block: on-books share (low/central/high) x fill-in method",
    CASES.flatMap((c) => METHODS.map((m) => [`${c}/${m}`, evalPackage(c, m, base)])));
  component("income_tax", "CBO income gradients: 2018/2019/2022 data, scaled or not by the stack's factor",
    [2018, 2019, 2022].flatMap((y) => [true, false].map((sc) => [`${y}${sc ? "" : " unscaled"}`, centralOn({ year: y, scaled: sc })])));
  component("medical", "decision 2: medical-ethnicity specifications and the MCBS 65+ bound",
    ["plain", "winsor_p999", "two_part_lognormal", "pooled_excl_2020_2021", "pooled_cpi_all_items", "pooled_year_normalized"]
      .map((sp) => [sp, centralOn({ medSpec: sp })]).concat([["MCBS as truth", centralOn({ mcbs: "mcbs_as_truth" })],
        ["MCBS precision-weighted", centralOn({ mcbs: "precision_weighted" })]]));
  component("ltss", "long-term-care carve-out: extremes of the lane's 960 combinations", LTSS_RANGE.map((v) => [String(v), centralOn({ ltss: v })]));
  component("education", "audit row 6 weight w (0.77/0.82) x school price k (low/high)",
    ["0.77", "0.82"].flatMap((w) => ["low", "preferred", "high"].map((k) => [`w ${w} k ${k}`, centralOn({ w, k })])));
  const benSe = Object.fromEntries(benefitSe.map((r) => [r.allocation, 1.96 * Number(r.se_bn)]));
  component("benefits", "benefit keys: central +/- 1.96 SE (package_se.csv)",
    [-1, 1].map((sg) => [`${sg > 0 ? "+" : "-"}1.96 SE`, centralOn({ benefitsDev: { personal: sg * benSe.personal, shared: sg * benSe.shared } })]));
  component("justice", "row 7 on 2023 arrests; booking factor Texas only or Arizona only",
    [["row 7 2023", centralOn({ row7: "2023" })], ["booking Texas", centralOn({ booking: "texas" })], ["booking Arizona", centralOn({ booking: "arizona" })]]);
  for (const id of Object.keys(CONSTANTS)) component(id, CONSTANTS[id].label, ["lo", "hi"].map((p) => [p, centralOn({ constants: { [id]: p } })]));
  component("finite_removal", "general government's removal response: r = b (fixed plus constant marginal cost); engine-key population share",
    [["r = b", centralOn({ finite: false })], ["engine population key", centralOn({ gg_s: "engine_population_key" })]]);
  component("consumption_key", "consumption key: the lane's twelve saving-and-remittance specifications", CK_SPECS.map((sp) => [sp, centralOn({ ck: sp })]));
  component("school_response", "school response: within-district elasticity 0.836 read over the removal (0.8489) or taken as the response",
    [["within district, finite r", centralOn({ school_rule: "within_district" })], ["within district, r = b", centralOn({ school_rule: "within_district_as_response" })]]);
  component("long_run_response", "long-run responses: r = b; within-state uncapped; federal fixed at the high end; across-state at the high end; held-at-zero lines at 1",
    Object.keys(LONG_RUN_VARIANTS).filter((v) => v !== "adopted").map((v) => [v, centralOn({ long_run: v })]));
  component("capital_rate", "return on public capital: 2% at both ends; 3% at both ends",
    [["2% at both ends", centralOn({ rates: { low: 0.02, high: 0.02 } })], ["3% at both ends", centralOn({ rates: { low: 0.03, high: 0.03 } })]]);
  component("capital_definition", "return on public capital: the capital lane's definition variants (engine_components.json variants), each re-run at every specification",
    Object.keys(CAP.variants).map((v) => [v, centralOn({ capital_variant: v })]));
  const sumLo = comps.reduce((s, x) => [s[0] + x.lo[0], s[1] + x.lo[1]], [0, 0]);
  const sumHi = comps.reduce((s, x) => [s[0] + x.hi[0], s[1] + x.hi[1]], [0, 0]);
  const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
  const lowEnd = [Cb[0] + sumLo[0], Cb[0] + sumHi[0]], highEnd = [Cb[1] + sumLo[1], Cb[1] + sumHi[1]];
  return { band: Cb, components: comps, low_end: lowEnd, high_end: highEnd, overall: [lowEnd[0], highEnd[1]],
    quadrature: [Cb[0] - rss(comps.map((x) => x.lo[0])), Cb[1] + rss(comps.map((x) => x.hi[1]))] };
}
const range27 = rangeOn(OFF);
const rangeGap = worst(["low_end", "high_end", "overall", "quadrature"].flatMap((k) => [range27[k][0] - s27.range[k][0], range27[k][1] - s27.range[k][1]]));
gate("on the September 27 case the components reproduce its published range (low end, high end, overall, quadrature; 1e-9)",
  rangeGap < 1e-9 && range27.components.length === s27.components.length
  && range27.components.every((x, k) => x.name === s27.components[k].name), `${range27.components.length} components, max |diff| ${ex(rangeGap)}`);
// The road arm as one more component: its two other cases re-run at every specification.
const roadComponent = { lo: [0, 1].map((e) => Math.min(0, B.candidate_road_replacement[e] - B.candidate[e], B.candidate_road_fixed_stock[e] - B.candidate[e])),
  hi: [0, 1].map((e) => Math.max(0, B.candidate_road_replacement[e] - B.candidate[e], B.candidate_road_fixed_stock[e] - B.candidate[e])) };
const withRoadOverall = [rangeC.overall[0] + roadComponent.lo[0], rangeC.overall[1] + roadComponent.hi[1]];

// ---------------------------------------------------------------------------------------------------
if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
const fx = (x) => x.toFixed(4);
const full = (x) => (typeof x === "number" ? String(x) : x);
// Old -> new at the fixed specifications, each method's value averaged.
const fixed = (key, baseKey) => {
  const base = baseKey || "sept27";
  const o = atEnds((m, i) => K[base][m][i]), n = atEnds((m, i) => K[key][m][i]);
  return { old: o, new: n, change: [n[0] - o[0], n[1] - o[1]] };
};
const FIXED = [
  ["item1_transfer_consolidation", "1. transfer consolidation, public housing's operating subsidies ($" + T.toFixed(6) + "bn)", fixed("item1"), true],
  ["item1_bound_all_of_line_4", "1. bound: all of line 4 consolidated ($" + TRANSFERS.all_of_line_4.bn + "bn), beside", fixed("item1_bound"), false],
  ["item2_production_row4", "2. production on the account's row-4 weights", fixed("item2"), true],
  ["item3_road_replacement", "3. road arm: replacement adjustment (beside the range)", fixed("item3_replacement"), false],
  ["item3_road_fixed_stock", "3. road arm: a fixed stock (beside the range)", fixed("item3_fixed_stock"), false],
  ["items_1_to_3_candidate", "items 1-3 together: the candidate (road arm at the stationary network, its September 27 setting)", fixed("candidate"), true],
  ["candidate_road_replacement", "the candidate, road arm at replacement adjustment", fixed("candidate_road_replacement"), false],
  ["candidate_road_fixed_stock", "the candidate, road arm at a fixed stock", fixed("candidate_road_fixed_stock"), false],
  ["item4_public_pay_on_sept27", "4. public pay on the September 27 case (published production), beside", fixed("item4_public_pay"), false],
  ["item4_public_pay_on_candidate", "4. public pay on the candidate (row-4 production), beside", fixed("candidate_public_pay", "candidate"), false],
];
const fixedCsv = ["item,label,in_candidate_band,old_spec48_bn,new_spec48_bn,change_spec48_bn,old_spec11_bn,new_spec11_bn,change_spec11_bn"]
  .concat(FIXED.map(([k, label, v, inBand]) => [k, `"${label}"`, inBand ? "yes" : "no", fx(v.old[0]), fx(v.new[0]), fx(v.change[0]),
    fx(v.old[1]), fx(v.new[1]), fx(v.change[1])].join(",")));
// The road arm: the account at the fixed specifications and the congestion item beside it (road_congestion.json at
// full precision), changes against the candidate (the stationary network at the adopted responses).
const road = Object.fromEntries(Object.keys(ROAD_CASES).map((rc) => {
  const g = gridAt(rc, "adopted");
  return [rc, { label: ROAD_CASES[rc].label, lanes: ROAD_CASES[rc].lanes, band_bn: g.band_bn, account_at_fixed_specs_bn: g.account_bn,
    account_change_bn: g.account_change_bn,
    depreciation_cut: ["low", "high"].map((rd) => (ROAD_CASES[rc].depreciation ? 0 : depreciationCut("adopted", rd))),
    road_return_removed_bn: g.road_return_removed_bn,
    congestion_bn: g.congestion_bn, congestion_range_bn: g.congestion_range_bn, congestion_change_bn: g.congestion_change_bn,
    account_plus_congestion_change_bn: g.net_change_bn }];
}));
const roadEnvelope = [Math.min(...Object.values(road).map((x) => x.band_bn[0])), Math.max(...Object.values(road).map((x) => x.band_bn[1]))];
// The long-run response varied with its congestion (the stationary network): each variant's account change and the
// congestion change at its highway response, at the fixed specifications.
const lrJoint = VARS.filter((v) => v !== "adopted").map((v) => { const g = gridAt("stationary_network", v);
  return { variant: v, label: LONG_RUN_VARIANTS[v].label, account_change_bn: g.account_change_bn, congestion_change_bn: g.congestion_change_bn,
    net_change_bn: g.net_change_bn, highway_response: ["low", "high"].map((rd) => RC.highway_response[v][rd]) }; });
const spanOf = (f) => [0, 1].map((e) => [Math.min(0, ...lrJoint.map((x) => f(x)[e])), Math.max(0, ...lrJoint.map((x) => f(x)[e]))]);
const lrJointSpan = { account_bn: spanOf((x) => x.account_change_bn), net_bn: spanOf((x) => x.net_change_bn) };
const roadCsv = ["road_case,long_run_variant,account_spec48_bn,account_spec11_bn,account_change_spec48_bn,account_change_spec11_bn,"
  + "congestion_low_end_bn,congestion_high_end_bn,congestion_change_low_end_bn,congestion_change_high_end_bn,net_change_spec48_bn,"
  + "net_change_spec11_bn,congestion_low_end_min_bn,congestion_low_end_max_bn,congestion_high_end_min_bn,congestion_high_end_max_bn,"
  + "road_return_removed_spec48_bn,road_return_removed_spec11_bn,band_low_bn,band_high_bn,end_specifications"]
  .concat(roadGrid.map((g) => [g.road_case, g.long_run].concat([...g.account_bn, ...g.account_change_bn, ...g.congestion_bn,
    ...g.congestion_change_bn, ...g.net_change_bn, ...g.congestion_range_bn[0], ...g.congestion_range_bn[1], ...g.road_return_removed_bn,
    ...g.band_bn].map(fx), [`"${g.end_specifications.map((e) => e.join("/")).join(" ")}"`]).join(",")));
const publicPay = {
  on_candidate_at_fixed_specs_bn: atEnds((m, i) => R.candidate_public_pay[m][i].public_pay_bn),
  on_sept27_at_fixed_specs_bn: atEnds((m, i) => R.item4_public_pay[m][i].public_pay_bn),
  band_with_public_pay_bn: B.candidate_public_pay,
  definition: PROD.public_pay.definition, public_share_of_incumbent_earnings: PROD.public_pay.public_share_of_incumbent_earnings,
  by_skill_row4: { gdp: PROD.public_pay.row4.gdp.charge_by_skill_bn, cash: PROD.public_pay.row4.cash.charge_by_skill_bn },
  by_level_row4: { gdp: PROD.public_pay.row4.gdp.charge_by_level_bn, cash: PROD.public_pay.row4.cash.charge_by_level_bn },
  note: "beside the range, not in it (BRIEF.md item 4): public employers pay the production model's wage change on their payroll; positive raises the group's cost. Specification 48 is GDP-normalized, 11 cash-normalized" };
const bandsRows = [
  ["sept27_case", "the September 27 case (adopted)", B.sept27, s27.range.overall],
  ["item1_transfer_consolidation_alone", "item 1 alone", B.item1],
  ["item1_bound_all_of_line_4_alone", "item 1's bound alone (beside)", B.item1_bound],
  ["item2_production_row4_alone", "item 2 alone", B.item2],
  ["item3_road_replacement_alone", "road arm: replacement adjustment alone (beside)", B.item3_replacement],
  ["item3_road_fixed_stock_alone", "road arm: a fixed stock alone (beside)", B.item3_fixed_stock],
  ["item4_public_pay_on_sept27", "public pay on the September 27 case (beside)", B.item4_public_pay],
  ["candidate", "the candidate: items 1-3 (road arm at the stationary network)", B.candidate, rangeC.overall],
  ["candidate_road_replacement", "the candidate, road arm at replacement adjustment (beside)", B.candidate_road_replacement],
  ["candidate_road_fixed_stock", "the candidate, road arm at a fixed stock (beside)", B.candidate_road_fixed_stock],
  ["candidate_road_arm_in_the_range", "the candidate if the road arm entered the band: envelope of the three road cases", roadEnvelope, withRoadOverall],
  ["candidate_public_pay", "the candidate with public pay (beside)", B.candidate_public_pay],
  ["candidate_transfer_bound", "the candidate with all of line 4 consolidated (beside)", B.candidate_transfer_bound],
];
const bandsCsv = ["case,label,cost_low_bn,cost_high_bn,outer_range_low_bn,outer_range_high_bn"]
  .concat(bandsRows.map(([k, label, b, r]) => [k, `"${label}"`, fx(b[0]), fx(b[1]), r ? fx(r[0]) : "", r ? fx(r[1]) : ""].join(",")));
const compCsv = ["component,label,candidate_low_end_lo,candidate_low_end_hi,candidate_high_end_lo,candidate_high_end_hi,sept27_low_end_lo,sept27_low_end_hi,sept27_high_end_lo,sept27_high_end_hi"]
  .concat(rangeC.components.map((x, k) => { const y = range27.components[k];
    return [x.name, `"${x.label}"`, fx(x.lo[0]), fx(x.hi[0]), fx(x.lo[1]), fx(x.hi[1]), fx(y.lo[0]), fx(y.hi[0]), fx(y.lo[1]), fx(y.hi[1])].join(","); }));
const perHead = ["method", "spec", "allocation", "normalization", "reading", "sept27_cost_bn", "candidate_cost_bn",
  "item1_bn", "item1_bound_bn", "item2_bn", "road_replacement_bn", "road_fixed_stock_bn", "public_pay_on_candidate_bn",
  "rental_key", "enterprise_key", "P_plus_F_sept27_bn", "P_plus_F_candidate_bn"];
const perSpec = [perHead.join(",")].concat(METHODS.flatMap((meth, m) => specs27.map((s, i) => [meth, i, s.allocation, s.normalization, s.reading,
  K.sept27[m][i], K.candidate[m][i], d1[m][i], d1b[m][i], d2[m][i], d3.replacement[m][i], d3.fixed_stock[m][i],
  K.candidate_public_pay[m][i] - K.candidate[m][i], keyOf(R.sept27[m][i], "spending", RENTAL), keyOf(R.sept27[m][i], "receipts", ENTERPRISE_LINE),
  R.sept27[m][i].evaluation.production_gain_bn, R.candidate[m][i].evaluation.production_gain_bn].map(full).join(","))));
const summary = {
  lane: "main_case_candidate_2026_09_28", case: C.CASE, status: "candidate, not adopted (BRIEF.md, e003ea1)",
  imports: "main_case_long_run_2026_09_27/package.cjs (committed f3031ab, 7e94324)",
  sept27_case: B.sept27, candidate: B.candidate, candidate_end_specifications: candEnds,
  at_fixed_specifications: Object.fromEntries(FIXED.map(([k, label, v, inBand]) => [k, Object.assign({ label, in_candidate_band: inBand }, v)])),
  item1: { transfer_bn: T, source: TRANSFERS.public_housing_operating, hud: C.HUD, bound_bn: TRANSFERS.all_of_line_4.bn,
    control_today_spec48_capital_off_bn: today48, rule: "the transfer leaves both legs before keying: housing_subsidies and enterprise_surplus lose it nationally and every cell keeps its attributed fraction (package.cjs consolidate())",
    unpublished: "NIPA Handbook ch. 12: Section 8 estimates are by type of landlord, state and local enterprises included, from unpublished detail; that part is not in the amount and is bounded by all of line 4" },
  item2: { populations: PROD.populations, row4_factors: PROD.row4_factors, reference: PROD.reference, change_bn: PROD.cost_change_at_reference_bn },
  road_arm: road, road_arm_envelope_band_bn: roadEnvelope,
  road_arm_long_run_response_with_congestion: { variants: lrJoint, span_at_fixed_specifications: lrJointSpan,
    note: "stationary network: each long-run variant re-run at every specification (account) with the congestion item at its highway response (road_congestion.json); changes against the candidate, [spec 48, spec 11]; span entries are [low end, high end] x [lo, hi]" },
  road_arm_grid: roadGrid.map((g) => ({ road_case: g.road_case, long_run: g.long_run, account_bn: g.account_bn, account_change_bn: g.account_change_bn,
    congestion_bn: g.congestion_bn, congestion_change_bn: g.congestion_change_bn, net_change_bn: g.net_change_bn, band_bn: g.band_bn,
    end_specifications: g.end_specifications })),
  public_pay: publicPay,
  range: { candidate: { low_end: rangeC.low_end, high_end: rangeC.high_end, overall: rangeC.overall, quadrature: rangeC.quadrature },
    sept27_reproduced: { overall: range27.overall, quadrature: range27.quadrature },
    road_arm_as_a_component: { lo: roadComponent.lo, hi: roadComponent.hi, overall_with_it: withRoadOverall },
    note: "the September 27 components re-run on the candidate at every specification; the road arm, the transfer bound and public pay are beside it" },
  components: rangeC.components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi, variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
  inputs: { production: { file: C.PRODUCTION_FILE, sha256: C.sha256(C.PRODUCTION_FILE) },
    depreciation: { file: C.BLOCK_FILE, sha256: C.sha256(C.BLOCK_FILE), values_bn: DEPRECIATION },
    congestion: { file: C.CONGESTION_FILE, sha256: C.sha256(C.CONGESTION_FILE) },
    road_congestion: { file: RC_FILE, sha256: C.sha256(RC_FILE) },
    sept27_payload: { file: `${SEPT27_DIR}/corrections.json`, sha256: C.sha256(`${SEPT27_DIR}/corrections.json`) } },
};
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "candidate_bands.csv"), bandsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "fixed_specs.csv"), fixedCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "components.csv"), compCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "road_arm.csv"), roadCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");

console.log("\n[result]");
for (const [k, label, b] of bandsRows) console.log(`  ${k.padEnd(36)} ${f2(b)}`);
for (const [k, , v] of FIXED) console.log(`    ${k.padEnd(32)} 48: ${fx(v.old[0])} -> ${fx(v.new[0])} (${v.change[0] >= 0 ? "+" : ""}${fx(v.change[0])})   11: ${fx(v.old[1])} -> ${fx(v.new[1])} (${v.change[1] >= 0 ? "+" : ""}${fx(v.change[1])})`);
for (const [rc, v] of Object.entries(road)) console.log(`  road ${rc.padEnd(20)} account ${f2(v.account_change_bn)}  congestion ${v.congestion_bn.map(fx).join(" / ")} (${f2(v.congestion_change_bn)})  net ${f2(v.account_plus_congestion_change_bn)}`);
for (const x of lrJoint) console.log(`  long-run ${x.variant.padEnd(26)} account ${f2(x.account_change_bn)}  congestion ${f2(x.congestion_change_bn)}  net ${f2(x.net_change_bn)}`);
console.log(`  long-run response at 48 / 11, account only: [${lrJointSpan.account_bn.map(f2).join("] [")}]; with congestion: [${lrJointSpan.net_bn.map(f2).join("] [")}]`);
console.log(`  public pay on the candidate at 48 / 11: ${f2(publicPay.on_candidate_at_fixed_specs_bn)}`);
console.log(`  outer range: sept27 ${f2(range27.overall)}; candidate ${f2(rangeC.overall)} (quadrature ${f2(rangeC.quadrature)}); with the road arm ${f2(withRoadOverall)}`);
console.log("all gates passed");
