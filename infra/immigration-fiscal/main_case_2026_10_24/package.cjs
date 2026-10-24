/* Candidate v10: the adopted v9 case (oct16) plus post-engine public-capital items 22 and 23 in the band; item 24
beside it (not identified) and item 25 (land) off.

v10 adds no engine edits and no people. Each item is a post-engine term derived inside the run it prices
(items.cjs), so every specification, method, allocation and reading carries its own amount. Item 24 is selectable
(caseOf with its id) and is reported as a companion. Item 25 reads per-line values from the lane named by
V10_LAND_LANE and is off, listed as pending, when that is unset.

API: the v9 case API with evaluateFull/viaCandidate/cost/bandFor/band/evalPackage/central/postEngine wrapped;
postFor returns the v10 additions only (postFor9 the v9 additions), as each case layer's postFor does.

Payload contract (correctionsPayload): meta.adopted null, meta.source this package, meta.status "candidate: ...".
With item 22 on, meta.one_rate has no flat_real_equivalent (a flat-rate reader must fail, not price at item 20's
rate); meta.v10.rates gives level_by_component and rate_by_level_by_end. Each new meta.items record carries
post_engine_by_end {low, high}: {total_bn, parts (by line, method mean), by_method: {total_bn, parts, rows}} at
the end specifications 16 / 11, where rows are the routable sub-rows of items.cjs post(). */
"use strict";
const fs = require("fs"), path = require("path");
const HERE = __dirname, LANE = "main_case_2026_10_24", CASE_KEY = "oct24";
const DECISION = null, STATUS = "candidate", ADOPTED = null;
if (STATUS !== "candidate") throw Error("[BLOCKED] v10: this lane builds a candidate only");
const V9 = require("../main_case_2026_10_16/package.cjs");
const I = require("./items.cjs");
const clone = (x) => JSON.parse(JSON.stringify(x)), sum = (a) => a.reduce((x, y) => x + y, 0), mean = (a) => sum(a) / a.length;
const fail = (s) => { throw Error("[BLOCKED] v10: " + s); };

const LABELS = {
  22: "capital rate bounded over theta (low theta = 1 at GRR, high theta = 0 at Baa) on every line item 20 prices, at the rate lane's level per component",
  23: "K-12 capital where enrolled, divisor 0.9868 with the embedded preferred school price k",
  24: "where-used prices (beside, not identified): matched municipal parks and the covered-college gross-book capital proxy",
  25: "land under public capital at each end's item 22 rate, read from V10_LAND_LANE",
};
const NEW_IDS = I.ORDER.map((n) => I.IDS[n]);
const NUMBER = Object.fromEntries(I.ORDER.map((n) => [I.IDS[n], n]));
const ACTIVE_NEW = I.ORDER.filter((n) => !I.BESIDE.includes(n) && (n !== 25 || I.LAND)).map((n) => I.IDS[n]);
const BESIDE_IDS = I.BESIDE.map((n) => I.IDS[n]);
const CANDIDATE = V9.CANDIDATE.concat(ACTIVE_NEW);
const REGISTRY = V9.REGISTRY.concat(I.ORDER.map((n) => ({ id: I.IDS[n], kind: "post_engine", label: LABELS[n], arms: {}, number: n, beside: I.BESIDE.includes(n) })));
const END_SPECS = { low: 16, high: 11 };

/* post_engine_by_end for each selected item, at the end specifications in both methods (v9 records' shape). */
function byEnd(X, on, land) {
  const out = Object.fromEntries([...on].map((n) => [I.IDS[n], {}]));
  for (const [end, i] of Object.entries(END_SPECS)) {
    const s = X.MAIN_SPECS[i], per = {};
    for (const method of V9.METHODS) per[method] = I.post(X, X.evaluateFull(X.modelFor("central", method, X.withCentral({})), s), s, on, { land, evaluate: X.evaluateFull });
    for (const id of Object.keys(out)) {
      const lines = {};
      for (const method of V9.METHODS) for (const q of per[method].parts[id]) { const k = q.line || q.part; lines[k] = lines[k] || { ...q, delta_bn: 0 }; lines[k].delta_bn += q.delta_bn / V9.METHODS.length; }
      out[id][end] = { total_bn: mean(V9.METHODS.map((m) => per[m].amounts[id])), specification: i, parts: Object.values(lines),
        by_method: Object.fromEntries(V9.METHODS.map((m) => [m, { total_bn: per[m].amounts[id], parts: per[m].parts[id], rows: per[m].rows.filter((q) => q.item === id) }])) };
    }
  }
  return out;
}
function records(on, land, peb) {
  return I.ORDER.filter((n) => on.has(n)).map((n) => ({
    id: I.IDS[n], kind: "post_engine", label: LABELS[n], number: n, applied: true, beside: I.BESIDE.includes(n), arm: null, arms: {},
    edits: { first: null, count: 0 }, parts: {}, post_engine_by_end: peb ? peb[I.IDS[n]] : null,
    post_engine: "derived per run in main_case_2026_10_24/items.cjs post(); evaluateFull carries it as post_engine." + I.IDS[n] + "_bn and v10_post_engine.{amounts,parts,rows}." + I.IDS[n],
    ...(n === 25 ? { land_lane: land?.dir || null, land_file: land?.file || null } : {}),
  }));
}
const RATES_META = { level_by_component: I.LEVEL_BY_COMPONENT, rate_by_level_by_end: I.RATES, end_index: { low: 0, high: 1 }, case_rate: I.RC, theta_by_end: I.BOUND.theta_by_end, source: I.RATE_SOURCE,
  variant_level_by_component: I.VARIANT_LEVEL, on_parent_components: I.ON_PARENT,
  rule: "item 22 reprices every capital piece item 20 prices at 2.0810698764% to rate_by_level_by_end[level_by_component[component]][end]; the nine components the inherited range variants add take variant_level_by_component (their source's declared level, equal to their parent's); completion, coverage, college, count and health sub-rows take their parent component's level; any other unmapped component stops the build" };

/* Wrap one (set or cash) v9 API with the selected v10 items. */
function wrapOne(X, on, stamp, land, ids) {
  let peb = null;
  const recs = () => records(on, land, peb || (peb = byEnd(X, on, land)));
  const evaluate = (fn, m, s, p) => {
    const r = fn(m, s, p), d = I.post(X, r, s, on, { land, evaluate: X.evaluateFull });
    return { ...r, cost_bn: r.cost_bn + d.total_bn,
      post_engine: { ...r.post_engine, ...Object.fromEntries(Object.entries(d.amounts).map(([k, v]) => [k + "_bn", v])), total_bn: (r.post_engine?.total_bn || 0) + d.total_bn },
      v10_post_engine: d };
  };
  const post = (m, s, p, r) => I.post(X, r || X.evaluateFull(m, s, p), s, on, { land, evaluate: X.evaluateFull });
  const evaluateFull = (m, s, p) => evaluate(X.evaluateFull, m, s, p), viaCandidate = (m, s, p) => evaluate(X.viaCandidate, m, s, p);
  const cost = (m, s, p) => evaluateFull(m, s, p).cost_bn;
  const bandFor = (m, p, ss) => V9.span(ss.map((s) => cost(m, s, p)));
  const evalPackage = (name, method, o) => { const oo = X.withCentral(o || {}); return bandFor(X.modelFor(name, method, oo), oo.profile, X.specsFor(o)); };
  const central = (o) => V9.mean2(...V9.METHODS.map((method) => evalPackage("central", method, o)));
  const correctionsPayload = (o) => {
    const q = X.correctionsPayload(o), rr = recs();
    q.meta.items = (q.meta.items || []).concat(clone(rr));
    Object.assign(q.meta, { source: LANE + "/package.cjs", decision: DECISION, adopted: stamp === "adopted" ? ADOPTED : null, status: stamp + ": main case v10", case: q.meta.case + "; v10 " + stamp });
    if (on.has(22)) {
      delete q.meta.one_rate.flat_real_equivalent;
      q.meta.one_rate.v10 = "item 22 replaces this block's single rate: capital is priced at meta.v10.rates (rate_by_level_by_end by level_by_component); flat_real_equivalent is removed so that a flat-rate reader stops";
    }
    q.meta.v10 = { lane: LANE + "/package.cjs", case_key: CASE_KEY, status: stamp + ": main case v10", decision: DECISION, adopted: q.meta.adopted,
      selected_items: ids,
      new_items: I.ORDER.filter((n) => on.has(n)).map((n) => I.IDS[n]), beside: BESIDE_IDS, pending: on.has(25) ? [] : [I.IDS[25]],
      land_lane: on.has(25) ? land.dir : null, rates: on.has(22) ? RATES_META : null, constants: I.constants,
      post_engine_rule: "v10 adds no edits and no people; evaluateFull adds items.cjs post() per run; postFor returns the v10 additions, postFor9 the v9 additions; postEngine(s) the complete post total; population_v9 is the denominator" };
    return q;
  };
  return { ...X, HERE, LANE, CASE_KEY, DECISION, STATUS: stamp, ADOPTED: stamp === "adopted" ? ADOPTED : null, correctionsPayload, evaluateFull, viaCandidate, cost, bandFor,
    band: (m, p) => bandFor(m, p, X.MAIN_SPECS), evalPackage, central, postFor: post, postFor9: X.postFor,
    postEngine: (s) => evaluateFull(X.payloadModel(), s).post_engine.total_bn, V10_ITEMS: recs, V10_ON: [...on].sort(), V9_API: X };
}
function wrap(X, on, stamp, land = I.LAND) {
  if (!on.size) return X;
  if (on.has(25) && !land) fail("item 25 selected without V10_LAND_LANE");
  const ids = (X.ITEM_IDS || V9.CANDIDATE).concat([...on].sort().map((n) => I.IDS[n]));
  const set = wrapOne(X, on, stamp, land, ids), cash = wrapOne(X.CASH, on, stamp, land, ids);
  let cashPayload = null;
  const out = { ...set, CASH: cash, ITEM_IDS: ids, V10_IDS: [...on].sort().map((n) => I.IDS[n]) };
  // v9 exposes CASH_PAYLOAD eagerly; v10's records evaluate the ends, so it is computed on first read.
  Object.defineProperty(out, "CASH_PAYLOAD", { enumerable: true, get: () => cashPayload || (cashPayload = cash.correctionsPayload()) });
  return out;
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
// Copy descriptors, so the lazy CASH_PAYLOAD getter is not evaluated at load.
module.exports = Object.defineProperties({ ...V9 }, Object.getOwnPropertyDescriptors(CASE));
Object.assign(module.exports, { V9_PACKAGE: V9, REGISTRY, CANDIDATE, NEW_IDS, ACTIVE_NEW, BESIDE_IDS, END_SPECS, V10_PENDING: I.LAND ? [] : [I.IDS[25]], caseOf, wrap, ITEMS: I,
  V10: { HERE, LANE, CASE_KEY, DECISION, STATUS, ADOPTED, land_lane: I.LAND?.dir || null } });
