/* Candidate v10: gates, bands, per-item changes, companions, v9's output files and payloads. No upstream file is
written. Reads derived/ancestry.json (ancestry.cjs) for the ancestry-share companions.
Run: node main_case.cjs [--out-dir DIR]. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("./package.cjs"), V9 = P.V9_PACKAGE, I = P.ITEMS, C = require("../main_case_2026_10_16/companions.cjs");
const HERE = __dirname, FISCAL = path.join(HERE, ".."), OLD = path.join(FISCAL, "main_case_2026_10_16/derived");
const args = process.argv.slice(2), OUT = path.resolve(args.includes("--out-dir") ? args[args.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
const started = performance.now();
const clone = (x) => JSON.parse(JSON.stringify(x)), sum = (a) => a.reduce((x, y) => x + y, 0), mean = (a) => sum(a) / a.length;
const near = (a, b, e = 1e-9) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= e;
const checks = [];
const gate = (name, ok, details = null) => { checks.push({ name, pass: !!ok, details }); if (!ok) throw Error("[BLOCKED] v10 " + name + " " + JSON.stringify(details)); };
const readJ = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const write = (file, x) => fs.writeFileSync(path.join(OUT, file), typeof x === "string" ? x : JSON.stringify(x, null, 1) + "\n");
const csv = (rows) => rows.map((row) => row.map((x) => { const s = String(x ?? ""); return /[",\n]/.test(s) ? '"' + s.replaceAll('"', '""') + '"' : s; }).join(",")).join("\n") + "\n";
const parse = (text) => text.trimEnd().split("\n").map((line) => { const r = []; let s = "", q = false; for (let i = 0; i < line.length; i++) { const c = line[i]; if (c === '"') { if (q && line[i + 1] === '"') { s += '"'; i++; } else q = !q; } else if (c === "," && !q) { r.push(s); s = ""; } else s += c; } r.push(s); return r; });
const phase = (name) => console.log(`[TIMING] ${((performance.now() - started) / 1000).toFixed(1)}s ${name}`);
const ID = { 22: I.IDS[22], 23: I.IDS[23], 24: I.IDS[24], 25: I.IDS[25] };

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
const diff = (a, b) => a.map((v, i) => v - b[i]);
const companions = {}, bands = {};
function remember(name, Q, o = {}, rule = null) {
  const a = run(Q, "set", o, false, rule), b = run(Q, "cash", o, false, rule);
  companions[name] = { band_bn: a.band, cash_set_bn: b.band, ends: a.ends, cash_ends: b.ends, population: Q.POPULATION_V9, ...C.coverageLabel(Q, { rule }) };
  bands[name] = a.band; bands[name + "_cash_set"] = b.band;
  return companions[name];
}
fs.mkdirSync(OUT, { recursive: true });

phase("items off: v9 reproduces");
const v9file = JSON.parse(fs.readFileSync(path.join(OLD, "summary.json"), "utf8")), v9sum = v9file.v9;
const OFF = P.caseOf(P.OCT05, V9.CANDIDATE);
gate("items off is the v9 case", OFF === V9 && OFF.CASE_KEY === "oct16" && OFF.STATUS === "adopted" && !OFF.V10_IDS);
const oldJSON = (f) => JSON.stringify(JSON.parse(fs.readFileSync(path.join(OLD, f), "utf8")));
gate("items off v9 payloads exactly", JSON.stringify(OFF.correctionsPayload()) === oldJSON("corrections.json") && JSON.stringify(OFF.CASH.correctionsPayload()) === oldJSON("corrections_cash.json"));
const base = run(OFF), bc = run(OFF, "cash");
gate("items off v9 bands exactly", base.band.every((x, i) => x === v9sum.band_bn[i]) && bc.band.every((x, i) => x === v9sum.cash_set_bn[i]), { set: base.band, cash: bc.band });
gate("items off v9 end specifications", JSON.stringify(base.ends) === JSON.stringify(v9sum.end_specifications.set) && JSON.stringify(bc.ends) === JSON.stringify(v9sum.end_specifications.cash));
const oldRows = parse(fs.readFileSync(path.join(OLD, "per_spec.csv"), "utf8")), oldHeader = oldRows.shift();
const offModels = Object.fromEntries(P.METHODS.map((method) => [method, OFF.modelFor("central", method, OFF.withCentral({}))]));
for (const row of oldRows) { const method = row[oldHeader.indexOf("method")], i = +row[oldHeader.indexOf("spec")]; gate("v9 per_spec " + method + "/" + i, String(OFF.cost(offModels[method], OFF.ALL_SPECS[i])) === row[oldHeader.indexOf("cost_bn")]); }
gate("v9 per_spec rows checked", oldRows.length === 128, oldRows.length);

phase("v10 joint");
const r = run(P), rc = run(P, "cash"), all = run(P, "set", {}, true), allc = run(P, "cash", {}, true);
gate("candidate identity", P.STATUS === "candidate" && P.CASE_KEY === "oct24" && JSON.stringify(P.V10_IDS) === JSON.stringify([...P.ACTIVE_NEW].sort((a, b) => P.NEW_IDS.indexOf(a) - P.NEW_IDS.indexOf(b))) && !P.CANDIDATE.includes(ID[24]));
gate("64 specifications retained", P.MAIN_SPECS.length === 32 && P.SHARED_SPECS.length === 32 && P.ALL_SPECS.length === 64);
gate("ends agree across methods", [r, rc].every((x) => x.ends.every((es) => JSON.stringify(es) === JSON.stringify(x.ends[0]))), { set: r.ends, cash: rc.ends });
for (const [which, X, rr] of [["set", P, r], ["cash", P.CASH, rc]]) for (let i = 0; i < rr.specs.length; i++) gate(which + " payload/method mean " + i, near(X.cost(X.payloadModel(), rr.specs[i]), mean(rr.costs.map((a) => a[i]))));
const payload = P.correctionsPayload(), cashPayload = P.CASH.correctionsPayload();
gate("v10 adds no edits", payload.edits.length === OFF.correctionsPayload().edits.length && cashPayload.edits.length === OFF.CASH.correctionsPayload().edits.length);
for (const [X, Y] of [[P, OFF], [P.CASH, OFF.CASH]]) gate("v10 payload model is v9's", JSON.stringify(X.payloadModel()) === JSON.stringify(Y.payloadModel()));
// Accounting on every specification and method: v10 cost = v9 cost + v10 post terms; sub-rows add to each amount.
for (const [which, X, Y, rr] of [["set", P, OFF, all], ["cash", P.CASH, OFF.CASH, allc]]) rr.runs.forEach((a, mi) => a.forEach((q, i) => {
  const v9 = Y.evaluateFull(rr.models[mi], rr.specs[i]), d = q.v10_post_engine;
  gate(`${which} accounting ${mi}/${i}`, near(q.cost_bn, v9.cost_bn + d.total_bn) && near(q.post_engine.total_bn, v9.post_engine.total_bn + d.total_bn)
    && near(X.postFor(rr.models[mi], rr.specs[i]).total_bn, d.total_bn) && near(sum(Object.values(d.amounts)), d.total_bn) && near(sum(d.rows.map((x) => x.delta_bn)), d.total_bn));
}));
const endFresh = { set: r.ends, cash: rc.ends, same_as_v9: JSON.stringify(r.ends) === JSON.stringify(v9sum.end_specifications.set) && JSON.stringify(rc.ends) === JSON.stringify(v9sum.end_specifications.cash) };

phase("payload contract");
for (const [which, pl] of [["set", payload], ["cash", cashPayload]]) {
  gate(`${which} candidate stamp`, pl.meta.adopted === null && pl.meta.source === P.LANE + "/package.cjs" && /^candidate: main case v10$/.test(pl.meta.status) && pl.meta.decision === null && pl.meta.v10.adopted === null);
  gate(`${which} flat rate removed`, !Object.hasOwn(pl.meta.one_rate, "flat_real_equivalent") && typeof pl.meta.one_rate.v10 === "string");
  gate(`${which} rates published`, JSON.stringify(pl.meta.v10.rates.level_by_component) === JSON.stringify(I.LEVEL_BY_COMPONENT) && JSON.stringify(pl.meta.v10.rates.rate_by_level_by_end) === JSON.stringify(I.RATES));
  gate(`${which} selected items`, JSON.stringify(pl.meta.v10.selected_items) === JSON.stringify(P.CANDIDATE));
  for (const id of P.ACTIVE_NEW) { const rec = pl.meta.items.find((x) => x.id === id); gate(`${which}/${id} post_engine_by_end`, rec && ["low", "high"].every((e) => Number.isFinite(rec.post_engine_by_end?.[e]?.total_bn) && near(sum(Object.values(rec.post_engine_by_end[e].by_method).map((m) => m.total_bn)) / P.METHODS.length, rec.post_engine_by_end[e].total_bn))); }
}

phase("standalone items and oracles");
const changes = {}, alone = {};
for (const id of [...P.ACTIVE_NEW, ID[24]]) {
  const Q = P.caseOf(P.OCT05, V9.CANDIDATE.concat(id)), a = run(Q), b = run(Q, "cash");
  alone[id] = { Q, set: a, cash: b };
  changes[id] = { set: diff(a.band, base.band), cash: diff(b.band, bc.band), ends: { set: a.ends, cash: b.ends } };
}
const besideChanges = { [ID[24]]: changes[ID[24]] }; delete changes[ID[24]];
// Item 22: the in-run capital at the case rate must close to v9's 7%-arm capital at both ends (independent of items.cjs:
// v9's rate_check prices the 7% arm through item 20's own code).
const RCHK = readJ("main_case_2026_10_16/derived/rate_check.json"), RC = I.RC;
const inRun = { capital_at_case_rate_bn: [], by_level_at_case_rate_bn: [], rate_delta_bn: [] };
for (const [i, e] of ["low", "high"].entries()) {
  const k = base.indexes[0][i], s = base.specs[k], levels = {}; let capital = 0, delta = 0;
  for (const [mi] of base.models.entries()) {
    const cp = I.capitalPieces(OFF, base.runs[mi][k], s);
    for (const p of cp.pieces) { levels[p.level] = (levels[p.level] || 0) + p.at_r20_bn / 2; capital += p.at_r20_bn / 2; delta += p.at_r20_bn * (I.RATES[p.level][i] / RC - 1) / 2; }
  }
  const sevenPct = (RCHK.arms.capital_7pct.set[i] - RCHK.arms.B.set[i]) / (0.07 / RC - 1);
  inRun.capital_at_case_rate_bn.push(capital); inRun.by_level_at_case_rate_bn.push(levels); inRun.rate_delta_bn.push(delta);
  gate("item22 in-run capital closes to the 7% arm " + e, near(capital, sevenPct, 1e-9), { capital, sevenPct });
}
const item22Detail = { capital_at_case_rate_bn: inRun.capital_at_case_rate_bn, by_level_at_case_rate_bn: inRun.by_level_at_case_rate_bn, rate_delta_at_ends_bn: inRun.rate_delta_bn,
  rates: { level_by_component: I.LEVEL_BY_COMPONENT, rate_by_level_by_end: I.RATES, source: I.RATE_SOURCE },
  independent_check: "check_item22.py recomputes item 22 on every specification from per_spec*.csv capital pieces and rate_model.json, without items.cjs" };
// Items 23 and 24: where_used_prices case_scenarios.csv (case rate, oct16), an independent path through the school
// lane's case_base and the where-used lane's own parks and college construction.
const scen = Object.fromEntries(parse(fs.readFileSync(path.join(FISCAL, "where_used_prices_2026_10_24/derived/case_scenarios.csv"), "utf8")).slice(1).map((q) => [q[0], [+q[2], +q[3]]]));
const k12 = scen.k12_capital_existing_k_denominator_diagnostic, parks = scen.parks_matched_municipal_proxy, college = scen.college_capital_gross_book_proxy;
for (const which of ["set", "cash"]) for (const i of [0, 1]) {
  gate(`item23 oracle ${which}/${i}`, near(changes[ID[23]][which][i], k12[i], 1e-6), { got: changes[ID[23]][which][i], want: k12[i] });
  gate(`item24 oracle ${which}/${i}`, near(besideChanges[ID[24]][which][i], parks[i] + college[i], 1e-6), { got: besideChanges[ID[24]][which][i], want: parks[i] + college[i] });
}
const partsAtEnds = (rr) => [0, 1].map((e) => { const out = {}; rr.runs.forEach((a, mi) => { const d = a[rr.indexes[mi][e]].v10_post_engine; for (const [id, rows] of Object.entries(d.parts)) for (const q of rows) { const key = id + ":" + (q.part || q.line); out[key] = (out[key] || 0) + q.delta_bn / rr.runs.length; } }); return out; });
const item23Parts = partsAtEnds(alone[ID[23]].set), item24Parts = partsAtEnds(alone[ID[24]].set);
const SCHOOL = readJ("school_capital_where_enrolled_2026_10_24/derived/summary.json");
for (const i of [0, 1]) {
  // The school lane's own return and depreciation at its uncorrected divisor, moved to the embedded k: F/r - 1 -> F/k - 1.
  gate("item23 return/depreciation parts " + i, near(item23Parts[i][ID[23] + ":return"], 0.450560, 5e-7) && near(item23Parts[i][ID[23] + ":depreciation"], 0.092055, 5e-7), item23Parts[i]);
  gate("item24 parts " + i, near(item24Parts[i][ID[24] + ":parks_matched_municipal"], parks[i], 1e-6) && near(item24Parts[i][ID[24] + ":college_gross_book_capital"], college[i], 1e-6), item24Parts[i]);
}
gate("item23 divisor is the school lane's embedded relative times k", near(SCHOOL.r_embedded_account * I.constants.k12.embedded_k, 0.9868222477, 1e-9), SCHOOL.r_embedded_account);

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

phase("item 25 loader and mechanism (r1 charges, r2 schema)");
const R1 = path.join(FISCAL, "land_price_rule_2026_10_24"), R2 = path.join(FISCAL, "land_price_rule_r2_2026_10_24");
const rowsOf = (dir) => Object.fromEntries(parse(fs.readFileSync(path.join(dir, "derived/land_by_line.csv"), "utf8")).map((q, i, a) => i ? Object.fromEntries(a[0].map((h, j) => [h, q[j]])) : null).filter(Boolean).map((q) => [q.line, q]));
const r1rows = rowsOf(R1), r2rows = rowsOf(R2);
// r1 publishes no group ratios: K-12's is recovered from the lane's own coefficient column (not ours), every other line is 1.
const k12Ratio = (variant, end) => { const q = r1rows.k12; return +q[`charge_${variant}_${end}_bn`] / (+q[`value_${variant}_bn`] * +q["coef_" + end] * RC); };
const ratios = Object.fromEntries(["central", "low", "high"].map((v) => [v, k12Ratio(v, "low")]));
gate("r1 K-12 group ratio is one number per value variant across ends", Object.keys(ratios).every((v) => near(k12Ratio(v, "high"), ratios[v], 1e-9)), ratios);
let r1Rejected = false; try { I.loadLand(R1); } catch (e) { r1Rejected = /group_weighted_value_central_bn/.test(String(e)); }
gate("item25 loader stops on a lane without group-weighted values (r1)", r1Rejected);
const landR1 = I.loadLand(R1, { group_ratio_override: Object.fromEntries(Object.keys(r1rows).map((l) => [l, l === "k12" ? ratios : 1])) });
const landR2 = I.loadLand(R2);
for (const [line, q] of Object.entries(r2rows)) for (const v of ["central", "low", "high"]) gate(`item25 r2 ratio ${line}/${v}`, near(landR2.lines[line].group_ratio[v], +q[`group_weighted_value_${v}_bn`] / +q[`value_${v}_bn`], 1e-12));
const landTest = { lane: landR1.dir, k12_group_ratio_by_value_variant: ratios, r2_lane: landR2.dir, r2_group_ratio: Object.fromEntries(Object.entries(landR2.lines).map(([l, v]) => [l, v.group_ratio])), lines: {}, max_abs_error_bn: 0 };
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

phase("companions");
const pop = V9.POPULATION_V9;
for (const name of ["arm_a", "arm_c", "c3_minus_se", "c3_plus_se"]) { phase("lineage " + name); remember("lineage_" + name, P.caseOf(P.OCT05, P.CANDIDATE, {}, name)); }
phase("shared allocation"); remember("shared_allocation", P, { allocation: "shared" }, "shared");
phase("school within district"); remember("school_within_district", P, { school_rule: "within_district" }, "school");
phase("first year"); { const a = C.firstYear(P, "set"), b = C.firstYear(P, "cash"); companions.first_year = { band_bn: a.band_bn, cash_set_bn: b.band_bn, ends: a.ends, cash_ends: b.ends, population: P.POPULATION_V9, item20_rule: a.item20_rule, v10_rule: "items 22 and 23's return are zero (no capital return in this reading); item 23's depreciation is taken at the matched long-run K-12 key, moved by the education response ratio", ...C.coverageLabel(P, { rule: "first_year" }) }; bands.first_year_v10 = a.band_bn; bands.first_year_v10_cash_set = b.band_bn; }
for (const arm of ["da_middle_0_17", "da_middle"]) { phase("coverage " + arm); remember("coverage_" + arm, P.caseOf(P.OCT05, P.CANDIDATE, { coverage: arm })); }
for (const arm of ["population", "no_ethnicity", "plain_pooled"]) {
  phase("item21 " + arm); const Q = P.caseOf(P.OCT05, P.CANDIDATE, { health_residual_key: arm }), name = "health_residual_key_" + arm, v9b = Q.V9_API.central({});
  const row = parse(fs.readFileSync(path.join(OLD, "main_case_bands.csv"), "utf8")).find((q) => q[1] === name);
  gate("v9 item21 arm reproduces " + arm, row && near(v9b[0], +row[2], 5e-5) && near(v9b[1], +row[3], 5e-5), { v9b, row: row?.slice(0, 4) });
  companions[name] = { band_bn: Q.central({}), cash_set_bn: Q.CASH.central({}), v9_band_bn_recomputed: v9b, population: Q.POPULATION_V9, ...C.coverageLabel(Q) };
  bands[name] = companions[name].band_bn; bands[name + "_cash_set"] = companions[name].cash_set_bn;
}
// Item 24 beside: where-used prices, not identified. The case with item 24 added, its parts at the v10 rates.
phase("where-used prices beside");
{
  const Q = P.caseOf(P.OCT05, P.CANDIDATE.concat(ID[24])), c = remember("where_used_prices_beside", Q);
  const qa = run(Q), parts = partsAtEnds(qa);
  c.change_from_v10_bn = { set: diff(c.band_bn, r.band), cash: diff(c.cash_set_bn, rc.band) };
  c.parts_at_ends_bn = [0, 1].map((e) => ({ parks_matched_municipal: parts[e][ID[24] + ":parks_matched_municipal"], college_gross_book_capital: parts[e][ID[24] + ":college_gross_book_capital"] }));
  c.standalone_on_v9_bn = besideChanges[ID[24]];
  c.status = "not identified, beside: where_used_prices_2026_10_24 RESULT verdict ('neither is a complete national estimate or an adopted change'); held off the band under the same standard as item 25";
  // Year one: the parks base's coverage and count parts follow the recreation response ratio; capital is zero.
  const fy = C.firstYear(Q, "set"), fyc = C.firstYear(Q, "cash");
  c.first_year = { band_bn: fy.band_bn, cash_set_bn: fyc.band_bn, change_from_v10_first_year_bn: { set: diff(fy.band_bn, companions.first_year.band_bn), cash: diff(fyc.band_bn, companions.first_year.cash_set_bn) }, ends: fy.ends };
  // Direct check at the year-one ends, both methods: the parks part follows the recreation response (zero if it is zero).
  const X9 = Q.V9_API, fySpecs = X9.specsFor(fy.options);
  c.first_year.parks_at_ends = P.METHODS.map((method, mi) => fy.ends[mi].map((idx) => {
    const s = fySpecs[idx], m = X9.modelFor("central", method, X9.withCentral(fy.options)), q = X9.evaluateFull(m, s), d = I.post(X9, q, s, new Set([22, 24]));
    const resp = q.evaluation.spending.find((x) => x.id === "recreation_culture").response, park = d.parts[ID[24]][0].delta_bn;
    const transported = d.rows.filter((x) => x.item === ID[24] && ["parks_coverage", "parks_count"].includes(x.part));
    gate(`where-used year one ${method}/${idx}: parks follow the recreation response`, !s.long_run && (resp !== 0 || Math.abs(park) < 1e-12) && transported.every((x) => resp !== 0 || x.delta_bn === 0) && d.parts[ID[24]][1].delta_bn === 0, { resp, park });
    return { specification: idx, recreation_response: resp, parks_bn: park, college_bn: d.parts[ID[24]][1].delta_bn };
  }));
}
phase("ancestry share (derived/ancestry.json)");
const ANC = JSON.parse(fs.readFileSync(path.join(OUT, "ancestry.json"), "utf8"));
gate("ancestry built on this rate file", ANC.rate_source.sha256 === I.RATE_SOURCE.sha256 && JSON.stringify(ANC.selected_items) === JSON.stringify(P.CANDIDATE), { ancestry: ANC.rate_source, here: I.RATE_SOURCE });
for (const row of ANC.set) {
  const cash = ANC.cash.find((z) => z.scenario === row.scenario);
  companions["ancestry_share_" + row.scenario] = { ...row, cash_set_bn: cash.band_bn, cash, population: row.fractional_population };
  bands["ancestry_share_" + row.scenario] = row.band_bn; bands["ancestry_share_" + row.scenario + "_cash_set"] = cash.band_bn;
}
for (const [name, c] of Object.entries(companions)) { const v = v9sum.companions[name]?.band_bn || c.v9_band_bn_recomputed || null; c.v9_band_bn = v; c.change_from_v9_bn = v ? diff(c.band_bn, v) : null; }
const pending = {
  public_land: P.V10_PENDING.includes(ID[25]) ? "item 25 off: V10_LAND_LANE unset; the r2 land figure is not identified (land_price_rule_r2_2026_10_24)" : null,
  rate_lane_variant_components: `the rate lane's level_by_component omits the ${Object.keys(I.VARIANT_LEVEL).length} components the inherited range variants add (${Object.keys(I.VARIANT_LEVEL).join(", ")}); v10 prices them at their source's declared level, equal to their parent's, until the lane maps them`,
};

phase("inherited range variants");
const components = clone(v9file.components);
for (const c of P.V4PKG.rangeComponents()) {
  const values = Object.fromEntries(c.variants.map((v) => { const o = typeof v.o === "function" ? v.o(P.withCentral({})) : v.o; const bs = v.methods.map((method) => P.evalPackage(v.caseName, method, o)); return [v.v, [0, 1].map((e) => mean(bs.map((a) => a[e])) - r.band[e])]; }));
  const oldc = components.find((x) => x.name === c.name), next = { name: c.name, label: c.label, lo: [0, 1].map((e) => Math.min(0, ...Object.values(values).map((a) => a[e]))), hi: [0, 1].map((e) => Math.max(0, ...Object.values(values).map((a) => a[e]))), variants: values };
  if (oldc) Object.assign(oldc, next); else components.push(next);
}
const range = { ...clone(v9file.range), low_end: [r.band[0] + sum(components.map((c) => c.lo[0])), r.band[0] + sum(components.map((c) => c.hi[0]))], high_end: [r.band[1] + sum(components.map((c) => c.lo[1])), r.band[1] + sum(components.map((c) => c.hi[1]))], note: "Inherited variants repriced through the v10 evaluator (items 22 and 23 derived in each variant's runs)" };
range.overall = [range.low_end[0], range.high_end[1]];

phase("outputs");
bands.adopted = r.band; bands.cash_set = rc.band; bands.oct16_case = base.band; bands.oct16_cash_set = bc.band;
const table = parse(fs.readFileSync(path.join(OLD, "main_case_bands.csv"), "utf8")), head = table.shift(), carried = [];
for (const row of table) {
  const name = row[1], b = bands[name];
  if (row[0] === P.MAIN_PROFILE && b) { row[2] = b[0].toFixed(4); row[3] = b[1].toFixed(4); if (name === "adopted") { row[4] = range.overall[0].toFixed(4); row[5] = range.overall[1].toFixed(4); } row.push(companions[name.replace(/_cash_set$/, "")]?.coverage || "v10 (oct24) value; see summary.v10"); }
  else { carried.push(row[0] + "/" + name); row.push(row[6]?.startsWith("historical") ? row[6] : "v9 (oct16) value carried; v10 items not applied; see summary.v10.carried_rows"); }
}
for (const [name, b] of Object.entries(bands)) if (!table.some((row) => row[0] === P.MAIN_PROFILE && row[1] === name)) table.push([P.MAIN_PROFILE, name, b[0].toFixed(4), b[1].toFixed(4), "", "", "", companions[name.replace(/_cash_set$/, "")]?.coverage || "v10 (oct24) value; see summary.v10"]);
head.push("v10_price_scope");
const endParts = (rr) => [0, 1].map((e) => { const out = {}; rr.runs.forEach((a, mi) => { const d = a[rr.indexes[mi][e]].v10_post_engine; for (const [id, v] of Object.entries(d.amounts)) out[id] = (out[id] || 0) + v / rr.runs.length; }); return out; });
const summary = clone(v9file);
Object.assign(summary, { lane: P.LANE, decision: P.DECISION, main_case: r.band, cash_set: { ...v9file.cash_set, band_bn: rc.band }, components, range });
summary.v10 = { status: P.STATUS, adopted: P.ADOPTED, case_key: P.CASE_KEY, base: "oct16", selected_items: P.CANDIDATE, new_items: P.ACTIVE_NEW, pending_items: P.V10_PENDING, land_lane: P.V10.land_lane,
  beside: { where_used_prices: companions.where_used_prices_beside, item19_and_item6_legal_form_pair: "v9's beside readings (summary.v9.beside) carried; v10 items not applied" },
  band_bn: r.band, cash_set_bn: rc.band, v9_band_bn: base.band, v9_cash_set_bn: bc.band, change_from_v9_bn: { set: diff(r.band, base.band), cash: diff(rc.band, bc.band) },
  end_specifications: endFresh, population: pop,
  per_member_usd: { set: r.band.map((v) => v * 1e9 / pop.with_coverage), cash: rc.band.map((v) => v * 1e9 / pop.with_coverage) },
  per_member_without_coverage_people_usd: { set: r.band.map((v) => v * 1e9 / pop.without_coverage), cash: rc.band.map((v) => v * 1e9 / pop.without_coverage) },
  change_by_item: changes, interactions, post_terms_at_ends_bn: { set: endParts(r), cash: endParts(rc) },
  item_parts: { set: payload.meta.items.filter((x) => P.NEW_IDS.includes(x.id)).map(({ post_engine_by_end, ...x }) => ({ ...x, post_engine_by_end: Object.fromEntries(Object.entries(post_engine_by_end).map(([e, z]) => [e, { total_bn: z.total_bn, parts: z.parts }])) })) },
  item22: item22Detail, item23: { applied_factors: I.constants.k12.applied_factors, embedded_k: I.constants.k12.embedded_k, parts_at_ends_bn: item23Parts },
  item24_beside: { constants: { parks: I.constants.parks, college: I.constants.college }, standalone_parts_at_ends_bn: item24Parts },
  item25_mechanism_test: landTest, coverage: payload.meta.coverage ? { carried_from_v9: true, construction: payload.meta.coverage.construction, by_end_total_bn: Object.fromEntries(["low", "high"].map((e) => [e, payload.meta.coverage.by_end[e].total_bn])) } : null,
  one_rate: { replaced_by: "meta.v10.rates", rates: payload.meta.v10.rates, item20_arm: payload.meta.one_rate.arm, rule: "item 20 prices capital at 2.0810698764%; item 22 reprices each piece to its level's rate at each end" },
  rates_by_end: I.RATES, case_rate: RC, companions, pending, carried_rows: carried,
  historical_keys: "v4-v9 blocks remain historical; current whole-case results are in v10; band rows carried from v9 are listed in carried_rows" };
write("summary.json", summary); write("corrections.json", payload); write("corrections_cash.json", cashPayload);
write("main_case_bands.csv", csv([head, ...table]));
write("components.csv", csv([parse(fs.readFileSync(path.join(OLD, "components.csv"), "utf8"))[0], ...components.map((c) => [c.name, c.label, c.lo[0].toFixed(4), c.hi[0].toFixed(4), c.lo[1].toFixed(4), c.hi[1].toFixed(4)])]));
for (const f of ["lineage_payload.json", "lineage_payload_cash.json"]) { const x = JSON.parse(fs.readFileSync(path.join(OLD, f), "utf8")); x.v10 = { case_key: P.CASE_KEY, population: pop, new_items: P.ACTIVE_NEW, corrections: f.includes("cash") ? "corrections_cash.json" : "corrections.json", rule: "v10 adds no people and no edits; the lineage construction is v9's; v10 post amounts are in the current corrections payload" }; write(f, x); }
// per_spec: v9's columns recomputed where the run gives them (v9's own appended columns describe the v9 layer and are
// carried), then v10's columns. Set in per_spec.csv, cash in per_spec_cash.csv.
const comps = P.capitalMeta(P.withCentral({})).components.map((c) => c.id);
const levels = Object.keys(I.RATES);
const SPEC_FIELDS = oldHeader.slice(oldHeader.indexOf("spec") + 1, oldHeader.indexOf("cost_bn"));
const newCols = ["oct16_cost_bn", ...P.ACTIVE_NEW.map((id) => "item_" + id + "_bn"), "items_v10_interaction_bn", "post_engine_v10_total_bn", ...P.ACTIVE_NEW.map((id) => "standalone_" + id + "_bn"),
  "where_used_prices_beside_bn", "capital_case_rate_total_bn", ...comps.map((c) => "capital_case_rate_" + c + "_bn"), ...levels.map((l) => "rate_" + l), "v10_cost_per_member_usd"];
function perSpec(which, rr, Y) {
  const X = which === "cash" ? P.CASH : P, oldRowsW = which === "set" ? oldRows : null;
  const out = [];
  rr.runs.forEach((a, mi) => a.forEach((q, i) => {
    const s = rr.specs[i], method = P.METHODS[mi], vals = { cost_bn: q.cost_bn, engine_cost_bn: -q.evaluation.welfare_bn, capital_total_bn: q.capital.total_bn };
    for (const c of q.capital.components) vals["capital_" + c.id + "_bn"] = c.return_bn;
    for (const l of q.evaluation.spending) { vals["response_" + l.id] = l.response; vals["group_" + l.id + "_bn"] = l.amount_bn; }
    for (const [name, pred] of Object.entries({ state_local: (c) => c.level === "state_local", federal: (c) => c.level === "federal", core: (c) => c.group === "core", block: (c) => c.group === "block", enterprise: (c) => c.group === "enterprise" })) vals["capital_" + name + "_bn"] = sum(q.capital.components.filter(pred).map((c) => c.return_bn));
    gate(`${which} per_spec accounting ${method}/${i}`, near(q.cost_bn, -q.evaluation.welfare_bn + q.capital.total_bn + q.post_engine.total_bn));
    const d = q.v10_post_engine, v9cost = q.cost_bn - d.total_bn;
    const st = P.ACTIVE_NEW.map((id) => { const Z = which === "cash" ? alone[id].Q.CASH : alone[id].Q; return Z.cost(rr.models[mi], s) - v9cost; });
    const wu = I.post(Y, Y.evaluateFull(rr.models[mi], s), s, new Set([22, 24])).amounts[ID[24]];
    const piece = Object.fromEntries((d.capital_pieces || []).map((p) => [p.id, p.at_r20_bn]));
    const old = oldRowsW ? oldRowsW.find((row) => row[oldHeader.indexOf("method")] === method && +row[oldHeader.indexOf("spec")] === i) : null;
    if (oldRowsW) gate(`per_spec v10 cost minus v10 terms is v9's ${method}/${i}`, !!old && near(+old[oldHeader.indexOf("cost_bn")], v9cost, 1e-9));
    // Specification descriptors from the run's own spec (the cash file has no v9 row to carry them).
    const desc = { method, spec: String(i) };
    for (const h of SPEC_FIELDS) { if (!(h in s)) throw Error("[BLOCKED] v10 per_spec: spec has no field " + h); desc[h] = String(s[h]); }
    if (old) gate(`per_spec descriptors are v9's ${method}/${i}`, Object.entries(desc).every(([h, v]) => old[oldHeader.indexOf(h)] === v));
    Object.assign(vals, desc);
    const base9 = oldHeader.map((h, j) => h in vals ? String(vals[h]) : old ? old[j] : "");
    out.push(base9.concat([v9cost, ...P.ACTIVE_NEW.map((id) => d.amounts[id]), d.total_bn - sum(st), d.total_bn, ...st, wu, d.capital_at_case_rate_bn,
      ...comps.map((c) => piece[c] ?? 0), ...levels.map((l) => s.rate ? I.RATES[l][s.reading === "low" ? 0 : 1] : 0), q.cost_bn * 1e9 / pop.with_coverage]));
  }));
  return out;
}
write("per_spec.csv", csv([oldHeader.concat(newCols), ...perSpec("set", all, OFF)]));
write("per_spec_cash.csv", csv([oldHeader.concat(newCols), ...perSpec("cash", allc, OFF.CASH)]));
write("checks.json", { pass: true, count: checks.length, rate_source: I.RATE_SOURCE, checks: checks.map(({ name, pass }) => ({ name, pass })) });
console.log(JSON.stringify({ v10: "PASS", set: r.band, cash: rc.band, ends: endFresh, checks: checks.length, maxRSS_MiB: process.resourceUsage().maxRSS / 1024, seconds: (performance.now() - started) / 1000 }));
