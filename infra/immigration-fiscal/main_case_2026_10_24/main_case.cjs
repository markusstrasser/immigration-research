/* Candidate v10: gates, bands, per-item changes, companions and payloads. No upstream file is written. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("./package.cjs"), V9 = P.V9_PACKAGE, I = P.ITEMS, C = require("../main_case_2026_10_16/companions.cjs");
const HERE = __dirname, FISCAL = path.join(HERE, ".."), OLD = path.join(FISCAL, "main_case_2026_10_16/derived");
const args = process.argv.slice(2), OUT = path.resolve(args.includes("--out-dir") ? args[args.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
const started = performance.now();
const sum = (a) => a.reduce((x, y) => x + y, 0), mean = (a) => sum(a) / a.length;
const near = (a, b, e = 1e-9) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= e;
const checks = [];
const gate = (name, ok, details = null) => { checks.push({ name, pass: !!ok, details }); if (!ok) throw Error("[BLOCKED] v10 " + name + " " + JSON.stringify(details)); };
const readJ = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const write = (file, x) => fs.writeFileSync(path.join(OUT, file), typeof x === "string" ? x : JSON.stringify(x, null, 1) + "\n");
const csv = (rows) => rows.map((row) => row.map((x) => { const s = String(x ?? ""); return /[",\n]/.test(s) ? '"' + s.replaceAll('"', '""') + '"' : s; }).join(",")).join("\n") + "\n";
const parse = (text) => text.trimEnd().split("\n").map((line) => { const r = []; let s = "", q = false; for (let i = 0; i < line.length; i++) { const c = line[i]; if (c === '"') { if (q && line[i + 1] === '"') { s += '"'; i++; } else q = !q; } else if (c === "," && !q) { r.push(s); s = ""; } else s += c; } r.push(s); return r; });
const phase = (name) => console.log(`[TIMING] ${((performance.now() - started) / 1000).toFixed(1)}s ${name}`);

// One band: per method min/max over the reading's specifications, mean across methods (v9 main_case.cjs run()).
function run(Q, which = "set", o = {}, all = false, rule = null) {
  const X = which === "cash" ? Q.CASH : Q, ss = X.specsFor(all ? { ...o, allocation: "all" } : o), numbered = X.specsFor({ ...o, allocation: "all" });
  const models = P.METHODS.map((method) => X.modelFor("central", method, X.withCentral(o)));
  const runs = models.map((m) => ss.map((s) => rule ? C.adjustedRun(X, m, s, rule) : X.evaluateFull(m, s, o.profile)));
  const costs = runs.map((a) => a.map((r) => r.cost_bn)), indexes = costs.map((a) => [a.indexOf(Math.min(...a)), a.indexOf(Math.max(...a))]);
  const ends = indexes.map((ix) => ix.map((i) => numbered.findIndex((s) => JSON.stringify(s) === JSON.stringify(ss[i]))));
  gate("valid " + which + " end specification numbers", ends.every((a) => a.every((i) => i >= 0 && i < 64)));
  return { specs: ss, models, runs, costs, indexes, band: [0, 1].map((e) => mean(costs.map((a, k) => a[indexes[k][e]]))), ends };
}
const pair = (Q, o = {}, rule = null) => { const a = run(Q, "set", o, false, rule), b = run(Q, "cash", o, false, rule); return { band_bn: a.band, cash_set_bn: b.band, ends: a.ends, cash_ends: b.ends }; };
const diff = (a, b) => a.map((v, i) => v - b[i]);
fs.mkdirSync(OUT, { recursive: true });

phase("items off: v9 reproduces");
const v9sum = JSON.parse(fs.readFileSync(path.join(OLD, "summary.json"), "utf8")).v9;
const OFF = P.caseOf(P.OCT05, V9.CANDIDATE);
gate("items off is the v9 case", OFF.CASE_KEY === "oct16" && OFF.STATUS === "adopted" && !OFF.V10_IDS);
const oldJSON = (f) => JSON.stringify(JSON.parse(fs.readFileSync(path.join(OLD, f), "utf8")));
gate("items off v9 payloads exactly", JSON.stringify(OFF.correctionsPayload()) === oldJSON("corrections.json") && JSON.stringify(OFF.CASH.correctionsPayload()) === oldJSON("corrections_cash.json"));
const base = run(OFF), bc = run(OFF, "cash");
gate("items off v9 bands exactly", base.band.every((x, i) => x === v9sum.band_bn[i]) && bc.band.every((x, i) => x === v9sum.cash_set_bn[i]), { set: base.band, cash: bc.band });
gate("items off v9 end specifications", JSON.stringify(base.ends) === JSON.stringify(v9sum.end_specifications.set) && JSON.stringify(bc.ends) === JSON.stringify(v9sum.end_specifications.cash));
const oldRows = parse(fs.readFileSync(path.join(OLD, "per_spec.csv"), "utf8")), oldHeader = oldRows.shift();
const offModels = Object.fromEntries(P.METHODS.map((method) => [method, OFF.modelFor("central", method, OFF.withCentral({}))]));
let perSpecChecked = 0;
for (const row of oldRows) { const method = row[oldHeader.indexOf("method")], i = +row[oldHeader.indexOf("spec")]; gate("v9 per_spec " + method + "/" + i, String(OFF.cost(offModels[method], OFF.ALL_SPECS[i])) === row[oldHeader.indexOf("cost_bn")]); perSpecChecked++; }
gate("v9 per_spec rows checked", perSpecChecked === 128, perSpecChecked);

phase("v10 joint");
const r = run(P), rc = run(P, "cash"), all = run(P, "set", {}, true), allc = run(P, "cash", {}, true);
gate("candidate identity", P.STATUS === "candidate" && P.CASE_KEY === "oct24" && JSON.stringify(P.V10_IDS) === JSON.stringify(P.ACTIVE_NEW));
gate("64 specifications retained", P.MAIN_SPECS.length === 32 && P.SHARED_SPECS.length === 32 && P.ALL_SPECS.length === 64);
gate("ends agree across methods", [r, rc].every((x) => x.ends.every((es) => JSON.stringify(es) === JSON.stringify(x.ends[0]))), { set: r.ends, cash: rc.ends });
for (const [which, X, rr] of [["set", P, r], ["cash", P.CASH, rc]]) for (let i = 0; i < rr.specs.length; i++) gate(which + " payload/method mean " + i, near(X.cost(X.payloadModel(), rr.specs[i]), mean(rr.costs.map((a) => a[i]))));
gate("v10 adds no edits", P.correctionsPayload().edits.length === OFF.correctionsPayload().edits.length && P.CASH.correctionsPayload().edits.length === OFF.CASH.correctionsPayload().edits.length);
for (const [X, Y] of [[P, OFF], [P.CASH, OFF.CASH]]) gate("v10 payload model is v9's", JSON.stringify(X.payloadModel()) === JSON.stringify(Y.payloadModel()));
// Accounting on every specification and method: v10 cost = v9 cost + v10 post terms.
for (const [which, X, Y, rr] of [["set", P, OFF, all], ["cash", P.CASH, OFF.CASH, allc]]) rr.runs.forEach((a, mi) => a.forEach((q, i) => {
  const v9 = Y.evaluateFull(rr.models[mi], rr.specs[i]);
  gate(`${which} accounting ${mi}/${i}`, near(q.cost_bn, v9.cost_bn + q.v10_post_engine.total_bn) && near(q.post_engine.total_bn, v9.post_engine.total_bn + q.v10_post_engine.total_bn)
    && near(X.postFor(rr.models[mi], rr.specs[i]).total_bn, q.v10_post_engine.total_bn) && near(sum(Object.values(q.v10_post_engine.amounts)), q.v10_post_engine.total_bn));
}));
const endFresh = { set: r.ends, cash: rc.ends, same_as_v9: JSON.stringify(r.ends) === JSON.stringify(v9sum.end_specifications.set) && JSON.stringify(rc.ends) === JSON.stringify(v9sum.end_specifications.cash) };

phase("standalone items and oracles");
const changes = {}, alone = {};
for (const id of P.ACTIVE_NEW) {
  const Q = P.caseOf(P.OCT05, V9.CANDIDATE.concat(id)), a = run(Q), b = run(Q, "cash");
  alone[id] = { Q, set: a, cash: b };
  changes[id] = { set: diff(a.band, base.band), cash: diff(b.band, bc.band), ends: { set: a.ends, cash: b.ends } };
}
// Item 22. The rate lane's own construction, replicated from its inputs, must reproduce its band; the in-run
// construction must close to the lane's total capital at the case rate. Their difference is reported, not hidden.
const RM = readJ("public_capital_rate_2026_10_24/derived/rate_model.json"), RCHK = readJ("main_case_2026_10_16/derived/rate_check.json");
const B = RM.theta_pairing.bound, RC = I.RC, V8R = { low: 0.02, high: 0.03 };
const FED = new Set(["pos_fed", "health_fed", "health_fed_user_fees", "gps_fed", "hwy_fed", "air_fed", "rec_fed"]);
const laneLevel = (k) => FED.has(k) || k.endsWith("_fed") ? "federal" : k === "hwy_sl" ? "state_local_highways" : "state_local";
const replica = { lines: {}, rate_delta_bn: [], cap_bn: [] };
["low", "high"].forEach((e, i) => {
  const ratio = RC / V8R[e] - 1, acc = {};
  for (const p of v9sum.one_rate.by_end[e].by_method.b_hotdeck_union_matched.parts) { const k = p.component === "capital_engine" ? p.line : p.component; acc[k] = (acc[k] || 0) + p.delta_bn / ratio * (1 + ratio); }
  const cap = (RCHK.arms.capital_7pct.set[i] - RCHK.arms.B.set[i]) / (0.07 / RC - 1), scale = cap / sum(Object.values(acc));
  replica.lines[e] = Object.fromEntries(Object.entries(acc).map(([k, v]) => [k, v * scale]));
  replica.cap_bn.push(cap);
  replica.rate_delta_bn.push(sum(Object.entries(replica.lines[e]).map(([k, v]) => v * (I.RATES[laneLevel(k)][i] / RC - 1))));
});
for (const which of ["set", "cash"]) for (const i of [0, 1]) gate(`item22 lane replica ${which}/${i}`, near(RCHK.arms.B[which][i] + replica.rate_delta_bn[i], B[which].band_bn[i], 1e-6), { replica: RCHK.arms.B[which][i] + replica.rate_delta_bn[i], lane: B[which].band_bn[i] });
const inRun = { capital_at_case_rate_bn: [], by_level_at_case_rate_bn: [], rate_delta_bn: [] };
for (const [i, e] of ["low", "high"].entries()) {
  const k = base.indexes[0][i], s = base.specs[k], levels = {}; let capital = 0, delta = 0;
  for (const [mi, m] of base.models.entries()) {
    const q = base.runs[mi][k], cp = I.capitalPieces(OFF, q, s);
    for (const p of cp.pieces) { levels[p.level] = (levels[p.level] || 0) + p.at_r20_bn / 2; capital += p.at_r20_bn / 2; delta += p.at_r20_bn * (I.RATES[p.level][i] / RC - 1) / 2; }
  }
  inRun.capital_at_case_rate_bn.push(capital); inRun.by_level_at_case_rate_bn.push(levels); inRun.rate_delta_bn.push(delta);
  gate("item22 in-run capital closes to the 7% arm " + e, near(capital, replica.cap_bn[i], 1e-9), { capital, lane: replica.cap_bn[i] });
  for (const which of ["set", "cash"]) gate(`item22 standalone is the in-run rate delta ${which}/${e}`, near(changes.capital_rate_theta_bound[which][i], delta, 1e-9));
}
const laneByLevel = ["low", "high"].map((e) => { const o = {}; for (const [k, v] of Object.entries(replica.lines[e])) o[laneLevel(k)] = (o[laneLevel(k)] || 0) + v; return o; });
const item22Oracle = { lane_band_bn: { set: B.set.band_bn, cash: B.cash.band_bn }, lane_rate_delta_bn: B.set.rate_delta_bn, in_run_rate_delta_bn: inRun.rate_delta_bn,
  in_run_minus_lane_bn: diff(inRun.rate_delta_bn, B.set.rate_delta_bn), capital_at_case_rate_bn: inRun.capital_at_case_rate_bn,
  by_level_at_case_rate_bn: { in_run: inRun.by_level_at_case_rate_bn, lane: laneByLevel },
  reason: "the rate lane splits capital by line from v8-standalone one_rate parts and books union-completion (capital_reporter) and coverage (capital_coverage) capital as separate lines at the plain state/local rate; the in-run construction keeps each piece on its parent line, so highway and federal completion, coverage and count capital take the highway and federal rates. Totals agree to 1e-9." };
// Item 23 and 24 oracles: where_used_prices case_scenarios.csv (case rate, oct16).
const scen = Object.fromEntries(parse(fs.readFileSync(path.join(FISCAL, "where_used_prices_2026_10_24/derived/case_scenarios.csv"), "utf8")).slice(1).map((q) => [q[0], [+q[2], +q[3]]]));
const k12 = scen.k12_capital_existing_k_denominator_diagnostic, parks = scen.parks_matched_municipal_proxy, college = scen.college_capital_gross_book_proxy, combo = scen.combined_denominator_diagnostic_book_capital_municipal;
for (const which of ["set", "cash"]) for (const i of [0, 1]) {
  gate(`item23 oracle ${which}/${i}`, near(changes.k12_capital_where_enrolled[which][i], k12[i], 1e-6), { got: changes.k12_capital_where_enrolled[which][i], want: k12[i] });
  gate(`item24 oracle ${which}/${i}`, near(changes.where_used_prices[which][i], parks[i] + college[i], 1e-6), { got: changes.where_used_prices[which][i], want: parks[i] + college[i] });
  gate(`items 23+24 corrected partial sum ${which}/${i}`, near(changes.k12_capital_where_enrolled[which][i] + changes.where_used_prices[which][i], combo[i], 1e-6));
}
const partsAtEnds = (Q, rr) => [0, 1].map((e) => { const out = {}; rr.runs.forEach((a, mi) => { const d = a[rr.indexes[mi][e]].v10_post_engine; for (const [id, rows] of Object.entries(d.parts)) for (const q of rows) { const key = id + ":" + (q.part || q.line); out[key] = (out[key] || 0) + q.delta_bn / rr.runs.length; } }); return out; });
const item23Parts = partsAtEnds(null, alone.k12_capital_where_enrolled.set), item24Parts = partsAtEnds(null, alone.where_used_prices.set);
for (const i of [0, 1]) {
  gate("item23 return/depreciation parts " + i, near(item23Parts[i]["k12_capital_where_enrolled:return"], 0.450560, 5e-7) && near(item23Parts[i]["k12_capital_where_enrolled:depreciation"], 0.092055, 5e-7), item23Parts[i]);
  gate("item24 parts " + i, near(item24Parts[i]["where_used_prices:parks_matched_municipal"], parks[i], 1e-6) && near(item24Parts[i]["where_used_prices:college_gross_book_capital"], college[i], 1e-6), item24Parts[i]);
}

phase("pairs and order dependence");
const interactions = { total: {}, pairs: {} };
for (const which of ["set", "cash"]) { const b = which === "set" ? base.band : bc.band, full = which === "set" ? r.band : rc.band; interactions.total[which] = full.map((v, i) => v - b[i] - sum(P.ACTIVE_NEW.map((id) => changes[id][which][i]))); }
for (let i = 0; i < P.ACTIVE_NEW.length; i++) for (let j = i + 1; j < P.ACTIVE_NEW.length; j++) {
  const ids = [P.ACTIVE_NEW[i], P.ACTIVE_NEW[j]], Q = P.caseOf(P.OCT05, V9.CANDIDATE.concat(ids)), out = {};
  for (const which of ["set", "cash"]) { const band = run(Q, which).band, b = which === "set" ? base.band : bc.band; out[which] = band.map((v, e) => v - b[e] - sum(ids.map((id) => changes[id][which][e]))); }
  interactions.pairs[ids.join("+")] = out;
}
interactions.higher_order = Object.fromEntries(["set", "cash"].map((w) => [w, interactions.total[w].map((v, e) => v - sum(Object.values(interactions.pairs).map((p) => p[w][e])))]));
gate("item changes plus interactions close", ["set", "cash"].every((w) => [0, 1].every((e) => near(sum(P.ACTIVE_NEW.map((id) => changes[id][w][e])) + interactions.total[w][e], (w === "set" ? r.band[e] - base.band[e] : rc.band[e] - bc.band[e])))));

phase("item 25 mechanism against the r1 land lane");
const R1 = path.join(FISCAL, "land_price_rule_2026_10_24");
const r1rows = Object.fromEntries(parse(fs.readFileSync(path.join(R1, "derived/land_by_line.csv"), "utf8")).map((q, i, a) => i ? Object.fromEntries(a[0].map((h, j) => [h, q[j]])) : null).filter(Boolean).map((q) => [q.line, q]));
// The r1 file publishes no line-level group_ratio; K-12's effective ratio is recovered from the lane's own
// coefficient column (not ours), so the test still checks our in-run coefficient independently.
const k12Ratio = (variant, end) => { const q = r1rows.k12; return +q[`charge_${variant}_${end}_bn`] / (+q[`value_${variant}_bn`] * +q["coef_" + end] * RC); };
const ratios = Object.fromEntries(["central", "low", "high"].map((v) => [v, k12Ratio(v, "low")]));
gate("r1 K-12 group ratio is one number per value variant across ends", Object.keys(ratios).every((v) => near(k12Ratio(v, "high"), ratios[v], 1e-9)), ratios);
const landR1 = I.loadLand(R1, { group_ratio_override: { k12: ratios } });
const landTest = { lane: landR1.dir, k12_group_ratio_by_value_variant: ratios, lines: {}, max_abs_error_bn: 0 };
for (const [e, end] of ["low", "high"].entries()) {
  const got = {};
  base.runs.forEach((a, mi) => { const k = base.indexes[mi][e], d = I.post(OFF, a[k], base.specs[k], new Set([25]), { land: landR1 }); for (const q of d.parts.public_land) for (const [col, key] of [["central", "delta_bn"], ["low", "low_value_bn"], ["high", "high_value_bn"]]) got[q.line + ":" + col] = (got[q.line + ":" + col] || 0) + q[key] / base.runs.length; });
  for (const [line, q] of Object.entries(r1rows)) for (const col of ["central", "low", "high"]) {
    const want = +q[`charge_${col}_${end}_bn`], have = got[line + ":" + col], err = Math.abs(have - want);
    landTest.lines[`${line}:${col}:${end}`] = { r1_bn: want, mechanism_bn: have, error_bn: have - want };
    landTest.max_abs_error_bn = Math.max(landTest.max_abs_error_bn, err);
    gate(`item25 mechanism ${line}/${col}/${end}`, err <= 1e-6, { want, have });
  }
}
gate("item25 off by default", !I.LAND === !process.env.V10_LAND_LANE && (I.LAND ? true : !P.ACTIVE_NEW.includes("public_land")));

phase("companions");
const pop = V9.POPULATION_V9, companions = {};
for (const name of ["arm_a", "arm_c", "c3_minus_se", "c3_plus_se"]) { phase("lineage " + name); companions["lineage_" + name] = pair(P.caseOf(P.OCT05, P.CANDIDATE, {}, name)); }
phase("shared allocation"); companions.shared_allocation = pair(P, { allocation: "shared" }, "shared");
phase("school within district"); companions.school_within_district = pair(P, { school_rule: "within_district" }, "school");
phase("first year"); { const a = C.firstYear(P, "set"), b = C.firstYear(P, "cash"); companions.first_year = { band_bn: a.band_bn, cash_set_bn: b.band_bn, ends: a.ends, cash_ends: b.ends }; }
for (const arm of ["da_middle_0_17", "da_middle"]) { phase("coverage " + arm); companions["coverage_" + arm] = pair(P.caseOf(P.OCT05, P.CANDIDATE, { coverage: arm })); }
for (const arm of ["population", "no_ethnicity", "plain_pooled"]) { phase("item21 " + arm); const Q = P.caseOf(P.OCT05, P.CANDIDATE, { health_residual_key: arm }); const name = "health_residual_key_" + arm, v9b = Q.V9_API.central({});
  const row = parse(fs.readFileSync(path.join(OLD, "main_case_bands.csv"), "utf8")).find((q) => q[1] === name);
  gate("v9 item21 arm reproduces " + arm, row && near(v9b[0], +row[2], 5e-5) && near(v9b[1], +row[3], 5e-5), { v9b, row: row?.slice(0, 4) });
  companions[name] = { band_bn: Q.central({}), cash_set_bn: Q.CASH.central({}), v9_band_bn_recomputed: v9b }; }
for (const [name, c] of Object.entries(companions)) { const v = v9sum.companions[name]?.band_bn || c.v9_band_bn_recomputed || null; c.v9_band_bn = v; c.change_from_v9_bn = v ? diff(c.band_bn, v) : null; }
const pending = {
  ancestry_share: "not recomputed: ancestry rows weight each generation's cost by its ancestry share, and the v10 post terms carry no generation split yet (capital pieces would need v9_split generation parts per capital component); v9's values are not carried",
  public_land: P.V10_PENDING.includes("public_land") ? "item 25 off: V10_LAND_LANE unset; the land figure is under rework in land_price_rule_r2_2026_10_24" : null,
};

phase("outputs");
const payload = P.correctionsPayload(), cashPayload = P.CASH.correctionsPayload();
const endParts = (rr) => [0, 1].map((e) => { const out = {}; rr.runs.forEach((a, mi) => { const d = a[rr.indexes[mi][e]].v10_post_engine; for (const [id, v] of Object.entries(d.amounts)) out[id] = (out[id] || 0) + v / rr.runs.length; }); return out; });
const summary = { lane: P.LANE, case_key: P.CASE_KEY, status: P.STATUS, decision: P.DECISION, base: "oct16",
  v10: { status: P.STATUS, case_key: P.CASE_KEY, selected_items: P.CANDIDATE, new_items: P.ACTIVE_NEW, pending_items: P.V10_PENDING, land_lane: P.V10.land_lane,
    band_bn: r.band, cash_set_bn: rc.band, v9_band_bn: base.band, v9_cash_set_bn: bc.band, change_from_v9_bn: { set: diff(r.band, base.band), cash: diff(rc.band, bc.band) },
    end_specifications: endFresh, population: pop, per_member_usd: { set: r.band.map((v) => v * 1e9 / pop.with_coverage), cash: rc.band.map((v) => v * 1e9 / pop.with_coverage) },
    change_by_item: changes, interactions, post_terms_at_ends_bn: { set: endParts(r), cash: endParts(rc) },
    item22: item22Oracle, item23: { applied_factors: I.constants.k12.applied_factors, embedded_k: I.constants.k12.embedded_k, parts_at_ends_bn: item23Parts },
    item24: { constants: { parks: I.constants.parks, college: I.constants.college }, parts_at_ends_bn: item24Parts },
    item25_mechanism_test: landTest, rates_by_end: I.RATES, case_rate: RC, companions, pending },
  checks: checks.length };
write("summary.json", summary); write("corrections.json", payload); write("corrections_cash.json", cashPayload);
const items = P.ACTIVE_NEW;
const head = ["which", "method", "spec", "reading", "allocation", "v9_cost_bn", ...items.map((id) => "item_" + id + "_bn"), "post_engine_v10_total_bn", "cost_bn", ...items.map((id) => "standalone_" + id + "_bn"), "v10_order_dependence_bn"];
const rows = [];
for (const [which, rr, Y] of [["set", all, OFF], ["cash", allc, OFF.CASH]]) rr.runs.forEach((a, mi) => a.forEach((q, i) => {
  const s = rr.specs[i], v9 = q.cost_bn - q.v10_post_engine.total_bn;
  const st = items.map((id) => { const X = which === "cash" ? alone[id].Q.CASH : alone[id].Q; return X.cost(rr.models[mi], s) - v9; });
  rows.push([which, P.METHODS[mi], i, s.reading, s.allocation, v9, ...items.map((id) => q.v10_post_engine.amounts[id]), q.v10_post_engine.total_bn, q.cost_bn, ...st, q.v10_post_engine.total_bn - sum(st)]);
}));
write("per_spec.csv", csv([head, ...rows]));
write("checks.json", { pass: true, count: checks.length, checks: checks.map(({ name, pass }) => ({ name, pass })) });
console.log(JSON.stringify({ v10: "PASS", set: r.band, cash: rc.band, ends: endFresh, checks: checks.length, maxRSS_MiB: process.resourceUsage().maxRSS / 1024, seconds: (performance.now() - started) / 1000 }));
