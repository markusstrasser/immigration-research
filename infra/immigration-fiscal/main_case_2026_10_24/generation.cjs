/* Generation split of the v10 post terms, and v9's two structural ancestry-share readings on v10.

Routing (the rule generation_account_2026_09_24/v9_split.cjs applies to item 20's parts): a sub-row with a typed
generation (coverage, count and health parts) goes to that generation; an engine or college capital sub-row is
split by that capital component's return in each generation's evaluation; a completion carrier or a spending-line
sub-row by that line's amount times response. As v9's companions.cjs deltaParts does, the descendants ("added") are
the difference between the case model and the model with the lineage descendants removed, item 21's health parts
excepted, which enter through their declared added_lineage population; that amount leaves G3plus.

Ancestry: v9's rows weight each generation's cost by its ancestry share (G1 1, G2 s_g2, G3plus s_g3plus, added
s_added). v10 adds no people, so each row's population is v9's and its cost on specification i is v9's cost plus the
share-weighted v10 terms. v9's per-specification ancestry costs are read from the adopted v9 summary (the items-off
gates in main_case.cjs show the v9 module reproduces that summary's bands); the v10 increments are computed here. */
"use strict";
const fs = require("fs"), path = require("path");
const SPLIT = require("../generation_account_2026_09_24/v9_split.cjs");
const G = ["G1", "G2", "G3plus"], sum = (a) => a.reduce((x, y) => x + y, 0);
const fail = (s) => { throw Error("[BLOCKED] v10 generation: " + s); };
const V9SUM = JSON.parse(fs.readFileSync(path.join(__dirname, "../main_case_2026_10_16/derived/summary.json"), "utf8")).v9;
const SCENARIOS = ["g4_at_nothing", "g4_at_bound"];

// As main_case_2026_10_16/companions.cjs descendantModels (not exported there): v9's payload model with the lineage
// descendants' edits removed, row 8's response-calibration residual kept on the reporting union.
const modelCache = new WeakMap();
function descendantModels(X) {
  if (modelCache.has(X)) return modelCache.get(X);
  const B = X.OCT15, pl = JSON.parse(JSON.stringify(B.correctionsPayload())), range = pl.meta.lineage.edits;
  for (let i = range.first; i < range.first + range.count; i++) if (i !== range.row8_edit_index) pl.edits[i].by = { personal: 0, shared: 0 };
  for (const rec of pl.meta.items || []) for (const [name, p] of Object.entries(rec.parts || {})) if (name.startsWith("lineage_") && !name.includes(":observed_nonreporters:")) {
    const e = pl.edits[rec.edits.first + p.edit]; for (const a of ["personal", "shared"]) e.by[a] -= p.by[a];
  }
  let stripped = X.Engine.applyCorrections(X.MODEL, pl);
  for (const { x } of X.V9_BUILT) stripped = X.Engine.applyCorrections(stripped, { edits: x.editsAt ? x.editsAt(stripped, {}) : x.edits, meta: stripped.corrections });
  const out = { current: X.payloadModel(), stripped };
  modelCache.set(X, out);
  return out;
}

function sharesFor(row, evaluations) {
  if (row.generation) { if (!G.includes(row.generation)) fail("unknown generation " + row.generation); return Object.fromEntries(G.map((g) => [g, g === row.generation ? 1 : 0])); }
  const capital = ["capital_engine", "college_capital_interaction"].includes(row.component);
  const line = capital ? row.capital_source_line || row.line : row.line;
  const values = Object.fromEntries(G.map((g) => {
    const r = evaluations[g];
    if (capital) { const c = r.capital.components.find((q) => q.id === line); return [g, c ? c.return_bn : NaN]; }
    const q = r.evaluation.spending.find((x) => x.id === line); return [g, q ? q.amount_bn * q.response : NaN];
  }));
  const total = sum(Object.values(values));
  if (!Number.isFinite(total) || (total === 0 && row.delta_bn !== 0)) fail("no generation driver for " + row.component + "/" + line);
  return Object.fromEntries(G.map((g) => [g, total ? values[g] / total : g === "G3plus" ? 1 : 0]));
}

/* v10 post terms on specification s of case Q (set or cash), by generation: {G1, G2, G3plus, added}, adding to the
   v10 post total on Q's payload model. `items` restricts to those item ids (default all). */
function split(Q, which, s, items = null) {
  const Xv = which === "cash" ? Q.CASH : Q, X9 = Xv.V9_API;
  const dm = descendantModels(X9), keep = (q) => !items || items.includes(q.item);
  const now = Xv.evaluateFull(dm.current, s).v10_post_engine, rows = now.rows.filter(keep);
  const evaluations = SPLIT.generationParts(X9, s, "a").evaluations;
  const out = { G1: 0, G2: 0, G3plus: 0, added: 0 };
  for (const q of rows) { const sh = sharesFor(q, evaluations); for (const g of G) out[g] += q.delta_bn * sh[g]; }
  const before = Xv.evaluateFull(dm.stripped, s).v10_post_engine.rows.filter(keep);
  const notHealth = (a) => sum(a.filter((q) => q.part !== "health").map((q) => q.delta_bn));
  out.added = notHealth(rows) - notHealth(before) + sum(rows.filter((q) => q.part === "health" && q.population === "added_lineage").map((q) => q.delta_bn));
  out.G3plus -= out.added;
  const total = sum(rows.map((q) => q.delta_bn));
  if (Math.abs(sum(Object.values(out)) - total) > 1e-9) fail("generation parts do not close");
  return { ...out, total_bn: total };
}

/* v9's two structural ancestry readings with the v10 terms. */
function ancestry(Q, which = "set") {
  const Xv = which === "cash" ? Q.CASH : Q;
  const deltas = Xv.MAIN_SPECS.map((s) => split(Q, which, s));
  return SCENARIOS.map((scenario) => {
    const v9 = V9SUM.companions["ancestry_share_" + scenario], row = which === "cash" ? v9.cash : v9;
    if (!row?.costs || row.costs.length !== Xv.MAIN_SPECS.length) fail("v9 ancestry row lacks per-specification costs " + scenario + "/" + which);
    if (!row.ends.every((i, e) => row.costs[i] === row.band_bn[e])) fail("v9 ancestry costs do not reproduce its band " + scenario + "/" + which);
    const shares = { G1: 1, G2: v9.s_g2, G3plus: v9.s_g3plus, added: v9.s_added };
    const add = deltas.map((d) => sum(Object.keys(shares).map((g) => shares[g] * d[g])));
    const costs = row.costs.map((c, i) => c + add[i]), ends = [costs.indexOf(Math.min(...costs)), costs.indexOf(Math.max(...costs))];
    const population = v9.fractional_population;
    return { scenario, label: v9.label, s_g2: v9.s_g2, s_g3plus: v9.s_g3plus, s_added: v9.s_added, fractional_population: population,
      band_bn: ends.map((i) => costs[i]), ends, costs, per_member_usd: ends.map((i) => costs[i] * 1e9 / population),
      v9_band_bn: row.band_bn, v9_ends: row.ends, change_from_v9_bn: ends.map((i, e) => costs[i] - row.band_bn[e]),
      v10_delta_at_ends_bn: ends.map((i) => add[i]), v10_parts_at_ends_bn: Object.fromEntries(Object.keys(shares).map((g) => [g, ends.map((i) => deltas[i][g])])),
      rule: "v9 per-specification ancestry costs plus the ancestry-share-weighted v10 terms by generation; population unchanged (v10 adds no people)" };
  });
}
module.exports = { split, ancestry, descendantModels, sharesFor, SCENARIOS };
