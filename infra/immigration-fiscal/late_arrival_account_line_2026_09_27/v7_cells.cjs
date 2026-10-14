/* Parent's 2026-10-14 wave-2 rule: generation-tagged fixed parts split
 * inside G1 by the edited line's t1; job capital by all-wage shares when
 * the lane lacks INDUSTRY. The t1 job re-key remains a sensitivity. */
"use strict";
const V7 = require("../generation_account_2026_09_24/v7_split.cjs");
const V6 = require("../generation_account_2026_09_24/v6_split.cjs");
const { Engine, ALLOCS } = V7.X;
const clone = (x) => JSON.parse(JSON.stringify(x));
const byAlloc = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
const sum = (xs) => xs.reduce((a, b) => a + b, 0);
const blocked = (why) => { throw new Error(`[BLOCKED] oct14 G1: ${why}`); };
function layer(L, gens, top, models29, union29, opts = {}) {
  if (!L.added) return V6.layer(L, gens, top, models29, union29, opts);
  const lay = V6.layer(L.old, gens, top, models29, union29, opts);
  const parts = clone(lay.parts), items = clone(lay.items), g1 = gens.filter((g) => top[g] === "G1");
  if (!opts.jobT1 && (!opts.wages || ALLOCS.some((a) => !opts.wages[a]
    || g1.some((g) => !Number.isFinite(opts.wages[a][g]) || opts.wages[a][g] < 0)
    || Math.abs(sum(g1.map((g) => opts.wages[a][g])) - 1) >= 1e-12))) blocked("missing or invalid authorized G1 wage shares");
  const current = Object.fromEntries(gens.map((g) => [g, V6.withStep(models29[g], parts[g].edits, parts[g].receipt_lines)]));
  const target = (m, e, a) => e.side === "receipt"
    ? m.receipts.lines.find((l) => l.id === e.line).cells[e.scenario][a].target_bn
    : m.spending.lines.find((l) => l.id === e.line).keys[e.key][a].target_bn;
  for (const it of L.added) {
    const rec = { id: it.id, first: it.first, count: it.edits.length, edits: [] };
    for (const g of gens) parts[g].item_receipt_lines[it.id] = [];
    it.edits.forEach((e, j) => {
      if (e.national_bn !== undefined) blocked(`unruled national edit ${it.id}`);
      const pieces = Object.entries(it.record.parts || {}).filter(([, p]) => p.edit === j);
      if (!pieces.length || ALLOCS.some((a) => Math.abs(sum(pieces.map(([, p]) => p.by[a])) - e.by[a]) > 1e-9)) blocked(`parts do not close ${it.id}:${j}`);
      const routed = pieces.map(([name, p]) => {
        const match = name.match(/^union_(G1|G2|G3plus):/), lineage = name.startsWith("lineage_");
        if (!match && !lineage) blocked(`unknown tag ${name}`);
        const G = lineage ? "G3plus" : match[1], hits = gens.filter((g) => top[g] === G);
        let by = clone(p.by);
        const job = it.id === "job_capital_taxes" && !lineage;
        const newTarget = job && V7.P7.ITEM_DETAIL.job_capital_taxes[L.set].new_parts[`${e.line}|${e.scenario}`][`union_${G}`];
        if (job) by = byAlloc((a) => newTarget[a] - sum(hits.map((g) => target(models29[g], e, a))));
        const share = Object.fromEntries(gens.map((g) => [g, byAlloc((a) => {
          if (!hits.includes(g)) return 0;
          if (hits.length === 1) return 1;
          if (job && !opts.jobT1) return opts.wages[a][g];
          const total = sum(hits.map((h) => target(current[h], e, a)));
          if (Math.abs(total) < 1e-300) {
            if (by[a] === 0) return 1 / hits.length;
            blocked(`zero t1 for nonzero G1 ${it.id}:${e.line}`);
          }
          return target(current[g], e, a) / total;
        })]));
        const bn = Object.fromEntries(gens.map((g) => [g, byAlloc((a) => job && hits.includes(g)
          ? newTarget[a] * share[g][a] - target(models29[g], e, a) : by[a] * share[g][a]) ]));
        return { name, rule: lineage ? "lineage" : G === "G1" ? (job ? "job_wages" : "g1_t1_remainder") : "generation",
          union_bn: by, share, bn };
      });
      if (ALLOCS.some((a) => Math.abs(sum(routed.map((p) => p.union_bn[a])) - e.by[a]) > 1e-9)) blocked(`re-key does not close ${it.id}:${j}`);
      for (const p of routed) for (const a of ALLOCS) {
        if (Math.abs(sum(gens.map((g) => p.share[g][a])) - 1) >= 1e-12
          || Math.abs(sum(gens.map((g) => p.bn[g][a])) - p.union_bn[a]) >= 1e-9) blocked(`cell parts do not close ${p.name}`);
      }
      for (const g of gens) {
        const ed = Object.assign(clone(e), { by: byAlloc((a) => sum(routed.map((p) => p.bn[g][a]))) });
        parts[g].item_edits.push(ed);
        parts[g].edits.push(ed);
        current[g] = V6.withStep(current[g], [ed], []);
      }
      rec.edits.push({ edit: j, side: e.side, line: e.line, key: e.key, scenario: e.scenario, parts: routed });
    });
    items.push(rec);
  }
  return Object.assign({}, lay, { parts, items });
}
module.exports = Object.assign({}, V7, { layer, V6_LANE: V7.V7_LANE,
  P6: V6.P6, ALTERNATIVES: V6.ALTERNATIVES });
