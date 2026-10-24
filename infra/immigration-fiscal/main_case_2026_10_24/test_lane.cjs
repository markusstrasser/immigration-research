/* Unit tests for the v10 items and package wiring (fast; the whole-case gates live in main_case.cjs). */
"use strict";
const fs = require("fs"), path = require("path"), assert = require("assert");
const P = require("./package.cjs"), I = P.ITEMS, V9 = P.V9_PACKAGE;
const tmp = path.join(__dirname, "_cache/test_land");
let n = 0;
const test = (name, fn) => { fn(); n++; console.log("  ✓ " + name); };
const writeLand = (dir, head, rows) => { fs.mkdirSync(path.join(dir, "derived"), { recursive: true }); fs.writeFileSync(path.join(dir, "derived/land_by_line.csv"), [head, ...rows].join("\n") + "\n"); };

test("item 25 is off and pending when V10_LAND_LANE is unset", () => {
  if (process.env.V10_LAND_LANE) return;
  assert.strictEqual(I.LAND, null); assert.deepStrictEqual(P.V10_PENDING, ["public_land"]); assert(!P.CANDIDATE.includes("public_land"));
});
test("a land lane without a K-12 group_ratio stops", () => {
  writeLand(path.join(tmp, "a"), "line,value_central_bn,value_low_bn,value_high_bn", ["k12,1,0.5,2", "rec_sl,3,2,4"]);
  assert.throws(() => I.loadLand(path.join(tmp, "a")), /K-12 group_ratio/);
});
test("group_ratio per value variant, defaulting to the central ratio and to 1 off K-12", () => {
  writeLand(path.join(tmp, "b"), "line,value_central_bn,value_low_bn,value_high_bn,group_ratio,group_ratio_low", ["k12,1,0.5,2,1.2,1.1", "rec_sl,3,2,4,,"]);
  const L = I.loadLand(path.join(tmp, "b"));
  assert.deepStrictEqual(L.lines.k12.group_ratio, { central: 1.2, low: 1.1, high: 1.2 });
  assert.deepStrictEqual(L.lines.rec_sl.group_ratio, { central: 1, low: 1, high: 1 });
});
test("a non-numeric land value stops", () => {
  writeLand(path.join(tmp, "c"), "line,value_central_bn,value_low_bn,value_high_bn,group_ratio", ["k12,x,0.5,2,1"]);
  assert.throws(() => I.loadLand(path.join(tmp, "c")), /not numeric/);
});
test("rate levels: hwy_sl alone takes the highway blend", () => {
  assert.strictEqual(I.levelOf({ id: "hwy_sl", level: "state_local" }), "state_local_highways");
  assert.strictEqual(I.levelOf({ id: "hwy_fed", level: "federal" }), "federal");
  assert.strictEqual(I.levelOf({ id: "k12", level: "state_local" }), "state_local");
  assert.throws(() => I.levelOf({ id: "x", level: "county" }), /unknown capital level/);
});
test("item 22 rates are the bound's, theta 1 low and 0 high", () => {
  const b = JSON.parse(fs.readFileSync(path.join(__dirname, "../public_capital_rate_2026_10_24/derived/rate_model.json"), "utf8")).theta_pairing.bound;
  assert.deepStrictEqual(I.RATES, { state_local: b.rate_state_local_by_end, state_local_highways: b.rate_state_local_highways_by_end, federal: b.rate_federal_by_end });
});
test("item 23 applies the corrected divisor (embedded k)", () => {
  const k = I.constants.k12;
  assert(Math.abs(k.embedded_k - 1.0341917412164008) < 1e-15);
  assert(Math.abs(k.applied_factors.stock_combined - k.F_stock_combined / k.embedded_k) < 1e-15);
  // where_used_prices RESULT: the sibling's denominator 0.9541966043 times the embedded k is 0.9868222477.
  assert(Math.abs(0.9541966043 * k.embedded_k - 0.9868222477) < 1e-9);
});
test("items off returns the adopted v9 module itself", () => { assert.strictEqual(P.caseOf(P.OCT05, V9.CANDIDATE), V9); });
test("v10 items must follow v9 items in order", () => {
  assert.throws(() => P.caseOf(P.OCT05, V9.CANDIDATE.concat(["where_used_prices", "capital_rate_theta_bound"])), /out of order/);
  assert.throws(() => P.caseOf(P.OCT05, ["capital_rate_theta_bound"].concat(V9.CANDIDATE)), /follow v9/);
});
test("item 25 selected without a land lane stops", () => {
  if (I.LAND) return;
  const s = V9.MAIN_SPECS[16], m = V9.payloadModel(), r = V9.evaluateFull(m, s);
  assert.throws(() => I.post(V9, r, s, new Set([25]), { land: null }), /without a land lane/);
});
test("candidate status and key", () => { assert.strictEqual(P.STATUS, "candidate"); assert.strictEqual(P.CASE_KEY, "oct24"); assert.strictEqual(P.CASH.STATUS, "candidate"); });
test("one evaluation: v10 cost is v9 cost plus the v10 post terms", () => {
  const s = P.MAIN_SPECS[11], m = P.payloadModel(), a = P.evaluateFull(m, s), b = V9.evaluateFull(m, s);
  assert(Math.abs(a.cost_bn - b.cost_bn - a.v10_post_engine.total_bn) < 1e-9);
  assert(Math.abs(P.postEngine(s) - a.post_engine.total_bn) < 1e-9);
  assert.strictEqual(typeof P.withSyntheticLines, "function"); assert.strictEqual(typeof P.stateFor, "function");
});
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`test_lane: ${n} passed`);
