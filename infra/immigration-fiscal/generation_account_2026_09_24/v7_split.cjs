/* oct14 split: v6's designed R1–R4 split, followed by the v7 registry parts.
 * R5 uses only MAIN_SPECS (personal, numbering retained). R6–R9 route union_<G>:
 * to G and lineage_* to G3+. No guessed within-generation split is admitted.
 * Job-capital targets are re-keyed on the supplied models (R7), including
 * convention b; its recorded shifts were built on convention a.
 * Module only; no outputs. */
"use strict";
const path = require("path");
const V6 = require("./v6_split.cjs");
const { X } = V6;
const { Engine, MODEL, ALLOCS, byAlloc, sum, readJson } = X;
const V7_LANE = "main_case_2026_10_14";
const P7 = require(path.join(__dirname, "..", V7_LANE, "package.cjs"));
const V7_FILES = { set: `${V7_LANE}/derived/corrections.json`, cash: `${V7_LANE}/derived/corrections_cash.json` };
const clone = (x) => JSON.parse(JSON.stringify(x));
const blocked = (why) => { throw new Error(`[BLOCKED] oct14 split: ${why}`); };
const TAG = /^union_(G1|G2|G3plus):/;
const ITEMS = new Set(["personal_allocation", "child_credits", "job_capital_taxes", "white_end_tax_keys", "row4_frame"]);
function loadCase(set) {
  const old = V6.loadCase(set), rel = V7_FILES[set];
  if (!rel) blocked(`no ${set} payload`);
  const payload = readJson(rel), api = set === "set" ? P7 : P7.CASH;
  if (JSON.stringify(payload) !== JSON.stringify(api.correctionsPayload())) blocked(`${rel} differs from the case package`);
  for (const key of ["lines", "receipt_lines", "production"]) {
    if (JSON.stringify(payload[key]) !== JSON.stringify(old.payload[key])) blocked(`v7 changed ${key}; no split rule`);
  }
  const n = old.payload.edits.length;
  if (JSON.stringify(payload.edits.slice(0, n)) !== JSON.stringify(old.payload.edits)) blocked("v7 does not start with v6's edits");
  if (JSON.stringify(payload.meta.lineage) !== JSON.stringify(old.payload.meta.lineage)) blocked("v7 changed the lineage block");
  const records = payload.meta.items;
  const previous = old.records.length;
  if (JSON.stringify(records.slice(0, previous)) !== JSON.stringify(old.records)) blocked("v7 changed the v6 registry records");
  let at = n;
  const added = [];
  for (const r of records.slice(previous)) {
    if (!ITEMS.has(r.id)) blocked(`item ${r.id} has no authorized split rule`);
    if (r.kind === "allocation") {
      if (r.id !== "personal_allocation" || (r.edits && r.edits.count !== 0)) blocked(`unknown allocation item ${r.id}`);
      continue;
    }
    if (r.kind !== "edit_set" || !r.applied || !r.edits || r.edits.first !== at || !(r.edits.count > 0)) blocked(`invalid edit record ${r.id}`);
    const edits = payload.edits.slice(at, at + r.edits.count);
    added.push({ id: r.id, record: r, first: at, edits, receipt_lines: [] });
    at += r.edits.count;
  }
  if (at !== payload.edits.length) blocked("registry does not cover all v7 edits");
  if (payload.meta.allocation.group_total !== "personal" || api.MAIN_SPECS.length !== 32) blocked("case allocation is not 32 personal specifications");
  return Object.assign({}, old, { rel, payload, api, records, items: old.items.concat(added), added, old });
}
function layer(L, gens, top, models29, union29, opts) {
  const lay = V6.layer(L.old, gens, top, models29, union29, opts);
  const parts = clone(lay.parts), record = clone(lay.items);
  const current = Object.fromEntries(gens.map((g) => [g, V6.withStep(models29[g], parts[g].edits, parts[g].receipt_lines)]));
  for (const it of L.added) {
    const rec = { id: it.id, first: it.first, count: it.edits.length, edits: [] };
    for (const g of gens) parts[g].item_receipt_lines[it.id] = [];
    it.edits.forEach((e, j) => {
      if (e.national_bn !== undefined) blocked(`new item ${it.id} has a national-scale edit with no rule`);
      const pieces = Object.entries(it.record.parts || {}).filter(([, p]) => p.edit === j);
      if (!pieces.length) blocked(`item ${it.id} edit ${j} has no parts`);
      if (ALLOCS.some((a) => Math.abs(sum(pieces.map(([, p]) => p.by[a])) - e.by[a]) > 1e-9)) blocked(`item ${it.id} edit ${j} parts do not close`);
      const routed = pieces.map(([name, p]) => {
        const match = name.match(TAG), lineage = name.startsWith("lineage_");
        if (!match && !lineage) blocked(`item ${it.id} part ${name} has no rule`);
        const G = lineage ? "G3plus" : match[1], hits = gens.filter((g) => top[g] === G);
        if (hits.length !== 1) blocked(`item ${it.id} part ${name}: ${hits.length} ${G} cells; need an authoritative within-generation split`);
        const g = hits[0];
        let by = clone(p.by);
        if (it.id === "job_capital_taxes" && !lineage) {
          const targets = P7.ITEM_DETAIL.job_capital_taxes[L.set].new_parts[`${e.line}|${e.scenario}`][`union_${G}`];
          const old = models29[g].receipts.lines.find((l) => l.id === e.line).cells[e.scenario];
          by = byAlloc((a) => targets[a] - old[a].target_bn);
        }
        const share = Object.fromEntries(gens.map((h) => [h, byAlloc(() => h === g ? 1 : 0)]));
        return { name, rule: lineage ? "lineage" : "generation", union_bn: by, share,
          bn: Object.fromEntries(gens.map((h) => [h, byAlloc((a) => h === g ? by[a] : 0)])) };
      });
      if (ALLOCS.some((a) => Math.abs(sum(routed.map((p) => p.union_bn[a])) - e.by[a]) > 1e-9)) {
        blocked(`item ${it.id} edit ${j}: re-keyed generation parts do not add to the case's edit`);
      }
      for (const g of gens) {
        const ed = Object.assign(clone(e), { by: byAlloc((a) => sum(routed.map((p) => p.bn[g][a]))) });
        parts[g].item_edits.push(ed);
        parts[g].edits.push(ed);
        current[g] = V6.withStep(current[g], [ed], []);
      }
      rec.edits.push({ edit: j, side: e.side, line: e.line, key: e.key, scenario: e.scenario, parts: routed });
    });
    record.push(rec);
  }
  return Object.assign({}, lay, { parts, items: record });
}
function evaluator(payload, api) {
  const ev = V6.evaluator(payload, api);
  const specs = ev.specs.filter((s) => s.allocation === payload.meta.allocation.group_total);
  return Object.assign({}, ev, { specs });
}
function adoptedPackage(L) {
  return { source: `${V7_LANE}/package.cjs${L.set === "cash" ? " CASH" : ""}`, specs: L.api.MAIN_SPECS,
    cost: (m, i) => L.api.evaluateFull(m, L.api.MAIN_SPECS[i], L.api.MAIN_PROFILE).cost_bn };
}
function oracle(set) {
  const S = readJson(`${V7_LANE}/derived/summary.json`).v7;
  const rows = X.P.csvRows(`${V7_LANE}/derived/main_case_bands.csv`);
  const variant = set === "set" ? "adopted" : "cash_set";
  const r = rows.find((x) => x.variant === variant && x.profile === P7.MAIN_PROFILE);
  const ends = S.end_specifications.by_method[set];
  if (!r || !ends.length || !ends.every((x) => x[0] === ends[0][0] && x[1] === ends[0][1])) blocked("case band/ends are missing or disagree across methods");
  return { source: `${V7_LANE}/derived/main_case_bands.csv (${variant})`, specs: ends[0],
    band: [Number(r.cost_low_bn), Number(r.cost_high_bn)],
    full: { source: `${V7_LANE}/derived/summary.json v7`, band: set === "set" ? S.band_bn : S.cash_set_bn } };
}
function perSpec(set) {
  if (set !== "set") return null;
  const rows = X.P.csvRows(`${V7_LANE}/derived/per_spec.csv`).filter((r) => r.in_band === "true" || r.in_band === "1");
  const out = new Map();
  for (const i of [...new Set(rows.map((r) => Number(r.spec)))]) {
    const rs = rows.filter((r) => Number(r.spec) === i);
    if (rs.length !== X.METHODS.length || !X.METHODS.every((m) => rs.some((r) => r.method === m))) blocked(`spec ${i}: not one row per method`);
    out.set(i, sum(rs.map((r) => Number(r.cost_bn))) / rs.length);
  }
  return { source: `${V7_LANE}/derived/per_spec.csv cost_bn (in_band)`, cost: out };
}
module.exports = { V7_LANE, V7_FILES, P7, X, loadCase, layer, evaluator, adoptedPackage, oracle, perSpec,
  payloadOf: V6.payloadOf, withStep: V6.withStep, addedAdults: V6.addedAdults,
  ALTERNATIVES: V6.ALTERNATIVES };
