/* Candidate v10: the adopted v9 case (oct16) plus four post-engine public-capital items, 22-25.

v10 adds no engine edits and no people. Each item is a post-engine term derived inside the run it prices
(items.cjs), so every specification, method, allocation and reading carries its own amount. Item 25 (land) reads
per-line values from the lane named by V10_LAND_LANE and is off, listed as pending, when that is unset.

API: the v9 case API with evaluateFull/viaCandidate/cost/bandFor/band/evalPackage/central/postEngine wrapped;
postFor returns the v10 additions only (postFor9 the v9 additions), as each case layer's postFor does. */
"use strict";
const fs = require("fs"), path = require("path");
const HERE = __dirname, LANE = "main_case_2026_10_24", CASE_KEY = "oct24";
const DECISION = null, STATUS = "candidate", ADOPTED = null;
if (STATUS !== "candidate") throw Error("[BLOCKED] v10: this lane builds a candidate only");
const V9 = require("../main_case_2026_10_16/package.cjs");
const I = require("./items.cjs");
const clone = (x) => JSON.parse(JSON.stringify(x)), sum = (a) => a.reduce((x, y) => x + y, 0);
const fail = (s) => { throw Error("[BLOCKED] v10: " + s); };

const LABELS = {
  22: "capital rate bounded over theta (low theta = 1 at GRR, high theta = 0 at Baa) on every line item 20 prices",
  23: "K-12 capital where enrolled, divisor 0.9868 with the embedded preferred school price k",
  24: "where-used prices: matched municipal parks and the covered-college gross-book capital proxy",
  25: "land under public capital at each end's item 22 rate, read from V10_LAND_LANE",
};
const NEW_IDS = I.ORDER.map((n) => I.IDS[n]);
const NUMBER = Object.fromEntries(I.ORDER.map((n) => [I.IDS[n], n]));
const ACTIVE_NEW = I.ORDER.filter((n) => n !== 25 || I.LAND).map((n) => I.IDS[n]);
const CANDIDATE = V9.CANDIDATE.concat(ACTIVE_NEW);
const REGISTRY = V9.REGISTRY.concat(I.ORDER.map((n) => ({ id: I.IDS[n], kind: "post_engine", label: LABELS[n], arms: {}, number: n })));

function records(on, land) {
  return I.ORDER.filter((n) => on.has(n)).map((n) => ({
    id: I.IDS[n], kind: "post_engine", label: LABELS[n], number: n, applied: true, arm: null, arms: {},
    edits: { first: null, count: 0 }, parts: {},
    post_engine: "derived per run in main_case_2026_10_24/items.cjs post(); evaluateFull carries it as post_engine." + I.IDS[n] + "_bn and v10_post_engine.parts." + I.IDS[n],
    ...(n === 25 ? { land_lane: land?.dir || null, land_file: land?.file || null } : {}),
  }));
}

/* Wrap one (set or cash) v9 API with the selected v10 items. */
function wrapOne(X, on, stamp, land) {
  const recs = records(on, land);
  const post = (m, s, p, r) => I.post(X, r || X.evaluateFull(m, s, p), s, on, { land, evaluate: X.evaluateFull });
  const evaluate = (fn, m, s, p) => {
    const r = fn(m, s, p), d = I.post(X, r, s, on, { land, evaluate: X.evaluateFull });
    return { ...r, cost_bn: r.cost_bn + d.total_bn,
      post_engine: { ...r.post_engine, ...Object.fromEntries(Object.entries(d.amounts).map(([k, v]) => [k + "_bn", v])), total_bn: (r.post_engine?.total_bn || 0) + d.total_bn },
      v10_post_engine: d };
  };
  const evaluateFull = (m, s, p) => evaluate(X.evaluateFull, m, s, p), viaCandidate = (m, s, p) => evaluate(X.viaCandidate, m, s, p);
  const cost = (m, s, p) => evaluateFull(m, s, p).cost_bn;
  const bandFor = (m, p, ss) => V9.span(ss.map((s) => cost(m, s, p)));
  const evalPackage = (name, method, o) => { const oo = X.withCentral(o || {}); return bandFor(X.modelFor(name, method, oo), oo.profile, X.specsFor(o)); };
  const central = (o) => V9.mean2(...V9.METHODS.map((method) => evalPackage("central", method, o)));
  const correctionsPayload = (o) => {
    const q = X.correctionsPayload(o);
    q.meta.items = (q.meta.items || []).concat(clone(recs));
    q.meta.v10 = { lane: LANE + "/package.cjs", case_key: CASE_KEY, status: stamp + ": main case v10", decision: DECISION,
      selected_items: I.ORDER.filter((n) => on.has(n)).map((n) => I.IDS[n]), pending: on.has(25) ? [] : [I.IDS[25]],
      land_lane: on.has(25) ? land.dir : null, rates_by_end: I.RATES, case_rate: I.RC, constants: I.constants,
      post_engine_rule: "v10 adds no edits and no people; evaluateFull adds items.cjs post() per run; postFor returns the v10 additions, postFor9 the v9 additions; population_v9 is the denominator" };
    q.meta.status = stamp + ": main case v10";
    return q;
  };
  return { ...X, HERE, LANE, CASE_KEY, DECISION, STATUS: stamp, ADOPTED, correctionsPayload, evaluateFull, viaCandidate, cost, bandFor,
    band: (m, p) => bandFor(m, p, X.MAIN_SPECS), evalPackage, central, postFor: post, postFor9: X.postFor,
    postEngine: (s) => evaluateFull(X.payloadModel(), s).post_engine.total_bn, V10_ITEMS: recs, V10_ON: [...on].sort(), V9_API: X };
}
function wrap(X, on, stamp, land = I.LAND) {
  if (!on.size) return X;
  if (on.has(25) && !land) fail("item 25 selected without V10_LAND_LANE");
  const set = wrapOne(X, on, stamp, land), cash = wrapOne(X.CASH, on, stamp, land);
  return { ...set, CASH: cash, CASH_PAYLOAD: cash.correctionsPayload(), ITEM_IDS: (X.ITEM_IDS || V9.CANDIDATE).concat([...on].sort().map((n) => I.IDS[n])), V10_IDS: [...on].sort().map((n) => I.IDS[n]) };
}
function caseOf(B, ids, selection = {}, lineage, { land = I.LAND } = {}) {
  const old = ids.filter((id) => !NEW_IDS.includes(id)), next = ids.filter((id) => NEW_IDS.includes(id));
  if (next.some((id, i) => i && NEW_IDS.indexOf(id) <= NEW_IDS.indexOf(next[i - 1]))) fail("v10 items out of order");
  if (ids.indexOf(next[0]) >= 0 && ids.slice(ids.indexOf(next[0])).some((id) => !NEW_IDS.includes(id))) fail("v10 items must follow v9 items");
  // The v9 module is its own adopted case; rebuilding it would repeat v9's item builds.
  const base = B === V9.OCT05 && JSON.stringify(old) === JSON.stringify(V9.CANDIDATE) && !Object.keys(selection).length && !lineage ? V9 : V9.caseOf(B, old, selection, lineage);
  const exact = JSON.stringify(ids) === JSON.stringify(CANDIDATE) && !Object.keys(selection).length && !lineage && land === I.LAND;
  return wrap(base, new Set(next.map((id) => NUMBER[id])), exact ? STATUS : "variant", land);
}
const CASE = caseOf(V9.OCT05, CANDIDATE);
module.exports = { ...V9, ...CASE, V9_PACKAGE: V9, REGISTRY, CANDIDATE, NEW_IDS, ACTIVE_NEW, V10_PENDING: I.LAND ? [] : [I.IDS[25]], caseOf, wrap, ITEMS: I,
  V10: { HERE, LANE, CASE_KEY, DECISION, STATUS, ADOPTED, land_lane: I.LAND?.dir || null } };
