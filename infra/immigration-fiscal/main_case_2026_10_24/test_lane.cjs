/* Unit tests for the v10 items and package wiring (fast; the whole-case gates live in main_case.cjs). */
"use strict";
const fs = require("fs"), path = require("path"), assert = require("assert"), crypto = require("crypto");
const P = require("./package.cjs"), I = P.ITEMS, V9 = P.V9_PACKAGE;
const FISCAL = path.join(__dirname, ".."), ROOT = path.resolve(FISCAL, "../..");
const tmp = path.join(__dirname, "_cache/test_lane");
let n = 0;
const test = (name, fn) => { fn(); n++; console.log("  ✓ " + name); };
const writeLand = (dir, head, rows) => { fs.mkdirSync(path.join(dir, "derived"), { recursive: true }); fs.writeFileSync(path.join(dir, "derived/land_by_line.csv"), [head, ...rows].join("\n") + "\n"); };
const R2_HEAD = "line,value_central_bn,group_weighted_value_central_bn,value_low_bn,group_weighted_value_low_bn,value_high_bn,group_weighted_value_high_bn";
const rateFile = path.join(ROOT, I.RATE_SOURCE.file), rateModel = JSON.parse(fs.readFileSync(rateFile, "utf8"));

test("item 25 is off and pending when V10_LAND_LANE is unset", () => {
  if (process.env.V10_LAND_LANE) return;
  assert.strictEqual(I.LAND, null); assert.deepStrictEqual(P.V10_PENDING, ["public_land"]); assert(!P.CANDIDATE.includes("public_land"));
});
test("item 24 is beside: listed, not in the candidate", () => {
  assert.deepStrictEqual(I.BESIDE, [24]); assert.deepStrictEqual(P.BESIDE_IDS, ["where_used_prices"]);
  assert(!P.CANDIDATE.includes("where_used_prices")); assert.deepStrictEqual(P.ACTIVE_NEW, ["capital_rate_theta_bound", "k12_capital_where_enrolled"]);
});
test("r2 land schema: group ratio per variant is group_weighted_value_<v>_bn / value_<v>_bn", () => {
  writeLand(path.join(tmp, "r2"), R2_HEAD, ["k12,2,3,1,1.2,4,8", "rec_sl,5,5,4,2,6,9"]);
  const L = I.loadLand(path.join(tmp, "r2"));
  assert.deepStrictEqual(L.lines.k12.group_ratio, { central: 1.5, low: 1.2, high: 2 });
  assert.deepStrictEqual(L.lines.rec_sl.group_ratio, { central: 1, low: 0.5, high: 1.5 });
  assert.deepStrictEqual(L.lines.k12, { central: 2, low: 1, high: 4, group_ratio: L.lines.k12.group_ratio });
});
test("a line without a group-weighted value for any variant stops", () => {
  writeLand(path.join(tmp, "nohigh"), R2_HEAD, ["k12,2,3,1,1.2,4,8", "rec_sl,5,5,4,2,6,"]);
  assert.throws(() => I.loadLand(path.join(tmp, "nohigh")), /group_weighted_value_high_bn for rec_sl/);
  writeLand(path.join(tmp, "r1"), "line,value_central_bn,value_low_bn,value_high_bn", ["k12,1,0.5,2"]);
  assert.throws(() => I.loadLand(path.join(tmp, "r1")), /group_weighted_value_central_bn for k12/);
});
test("the r1 lane loads only with an explicit per-line ratio override", () => {
  const L = I.loadLand(path.join(tmp, "r1"), { group_ratio_override: { k12: { central: 1.3, low: 1.1, high: 1.4 } } });
  assert.deepStrictEqual(L.lines.k12.group_ratio, { central: 1.3, low: 1.1, high: 1.4 });
});
test("a non-numeric or nonpositive land value stops", () => {
  writeLand(path.join(tmp, "c"), R2_HEAD, ["k12,x,3,1,1.2,4,8"]);
  assert.throws(() => I.loadLand(path.join(tmp, "c")), /not numeric/);
  writeLand(path.join(tmp, "d"), R2_HEAD, ["k12,2,0,1,1.2,4,8"]);
  assert.throws(() => I.loadLand(path.join(tmp, "d")), /bad land group ratio/);
});
test("item 22 levels and rates are the rate file's, read as published", () => {
  const b = rateModel.theta_pairing.bound;
  assert.deepStrictEqual(I.LEVEL_BY_COMPONENT, b.level_by_component); assert.deepStrictEqual(I.RATES, b.rate_by_level_by_end);
  assert.strictEqual(I.RATE_SOURCE.sha256, crypto.createHash("sha256").update(fs.readFileSync(rateFile)).digest("hex"));
  assert.strictEqual(I.RC, rateModel.r_c);
  for (const id of Object.keys(b.level_by_component)) assert.strictEqual(I.levelOf({ id, level: "ignored" }), b.level_by_component[id]);
});
test("an unmapped capital component stops", () => {
  assert.throws(() => I.levelOf({ id: "not_a_component", level: "state_local" }), /unmapped by the rate lane: not_a_component/);
});
test("the rate lane's map covers the central components; sub-row components ride on their parent", () => {
  const ids = V9.capitalMeta(V9.withCentral({})).components.map((c) => c.id);
  const lane = Object.keys(rateModel.theta_pairing.bound.level_by_component);
  for (const id of ids) assert(lane.includes(id), "central component unmapped: " + id);
  for (const id of lane.filter((x) => !ids.includes(x))) assert(I.ON_PARENT.includes(id), "lane maps a component v10 never prices: " + id);
});
test("range-variant components take their declared level, equal to their parent's", () => {
  for (const [id, parent] of Object.entries(I.VARIANT_PARENT)) {
    const level = I.levelOf({ id });
    assert(level === "state_local" || level === "federal", id);
    if (parent) assert.strictEqual(level, I.LEVEL_BY_COMPONENT[parent], id);
  }
  assert.strictEqual(I.levelOf({ id: "eq_gps_fed" }), "federal"); assert.strictEqual(I.levelOf({ id: "eq_income_security_sl" }), "state_local");
});
test("the rate-file reader items.cjs runs at load stops on a missing key, a level without a rate, or a moved bound", () => {
  const variants = {
    no_levels: [(m) => { delete m.theta_pairing.bound.level_by_component; }, /publishes no theta_pairing.bound.level_by_component/],
    no_rates: [(m) => { delete m.theta_pairing.bound.rate_by_level_by_end; }, /publishes no theta_pairing.bound.rate_by_level_by_end/],
    level_without_rate: [(m) => { m.theta_pairing.bound.level_by_component.k12 = "county"; }, /component k12 maps to level county/],
    bad_pair: [(m) => { m.theta_pairing.bound.rate_by_level_by_end.federal = [0.03]; }, /bad rate pair for level federal/],
    theta_swapped: [(m) => { m.theta_pairing.bound.theta_by_end = [0, 1]; }, /theta 1 low/],
    case_rate_moved: [(m) => { m.r_c += 1e-6; }, /not item 20's rate/],
  };
  assert.deepStrictEqual(I.readRateModel(rateModel).RATES, I.RATES);
  for (const [name, [edit, re]] of Object.entries(variants)) {
    const m = JSON.parse(JSON.stringify(rateModel)); edit(m);
    assert.throws(() => I.readRateModel(m), re, name);
  }
});
test("item 22 at one specification equals its pieces priced from the rate file", () => {
  const b = rateModel.theta_pairing.bound;
  for (const [i, e] of [[16, 0], [11, 1]]) {
    const r = P.evaluateFull(P.payloadModel(), P.MAIN_SPECS[i]), d = r.v10_post_engine;
    const want = d.capital_pieces.reduce((t, p) => t + p.at_r20_bn * (b.rate_by_level_by_end[b.level_by_component[p.id]][e] / rateModel.r_c - 1), 0);
    assert(Math.abs(d.amounts.capital_rate_theta_bound - want) < 1e-9, `${i}: ${d.amounts.capital_rate_theta_bound} vs ${want}`);
  }
});
test("item 23's divisor is the school lane's account denominator times the embedded k", () => {
  const k = I.constants.k12, school = JSON.parse(fs.readFileSync(path.join(FISCAL, "school_capital_where_enrolled_2026_10_24/derived/summary.json"), "utf8"));
  assert(Math.abs(k.embedded_k - 1.0341917412164008) < 1e-15);
  assert(Math.abs(k.applied_factors.stock_combined - k.F_stock_combined / k.embedded_k) < 1e-15);
  // where_used_prices RESULT prints the corrected current-price denominator 0.9868222477 (10 digits).
  assert(Math.abs(school.r_embedded_account * k.embedded_k - 0.9868222477) < 5e-11, String(school.r_embedded_account * k.embedded_k));
});
test("items off returns the adopted v9 module itself", () => { assert.strictEqual(P.caseOf(P.OCT05, V9.CANDIDATE), V9); });
test("v10 items must follow v9 items in order", () => {
  assert.throws(() => P.caseOf(P.OCT05, V9.CANDIDATE.concat(["k12_capital_where_enrolled", "capital_rate_theta_bound"])), /out of order/);
  assert.throws(() => P.caseOf(P.OCT05, ["capital_rate_theta_bound"].concat(V9.CANDIDATE)), /follow v9/);
});
test("item 25 selected without a land lane stops", () => {
  if (I.LAND) return;
  const s = V9.MAIN_SPECS[16], m = V9.payloadModel(), r = V9.evaluateFull(m, s);
  assert.throws(() => I.post(V9, r, s, new Set([25]), { land: null }), /without a land lane/);
});
test("candidate status, key and payload stamp", () => {
  assert.strictEqual(P.STATUS, "candidate"); assert.strictEqual(P.CASE_KEY, "oct24"); assert.strictEqual(P.CASH.STATUS, "candidate");
  const meta = P.correctionsPayload().meta;
  assert.strictEqual(meta.adopted, null); assert.strictEqual(meta.source, "main_case_2026_10_24/package.cjs"); assert.match(meta.status, /^candidate: /);
  assert(!("flat_real_equivalent" in meta.one_rate)); assert.deepStrictEqual(meta.v10.rates.level_by_component, I.LEVEL_BY_COMPONENT);
});
test("raw engine route: v9's welfare plus capital plus every post term is v10's cost", () => {
  const s = P.MAIN_SPECS[11], m = P.payloadModel(), ref = P.evaluateFull(m, s), ev = P.Engine.evaluate(P.withSyntheticLines(m), P.stateFor(m, s));
  const raw = -ev.welfare_bn + ref.capital.total_bn + P.V9_BASE.postEngine(s) + P.postFor9(m, s).total_bn + P.postFor(m, s).total_bn;
  assert(Math.abs(raw - ref.cost_bn) < 1e-9, `${raw} vs ${ref.cost_bn}`);
});
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`test_lane: ${n} passed`);
