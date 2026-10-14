/* Explicit sequential v8 attribution, preserving the measured base profiles.
 * Source keys identify amounts, not national counterfactual age profiles for
 * completion or coverage. These assumptions change attribution, never totals.
 */
"use strict";
function sourceParts(result, carriers = {}) {
  const out = { receipts_by_line: {}, spending_by_line: {}, production_bn: 0, public_capital_bn: result.capital.total_bn };
  const add = (side, line, amount) => { const basket = out[`${side}_by_line`]; basket[line] = (basket[line] || 0) + amount; };
  for (const r of result.evaluation.receipts) add("receipts", r.id, -r.effect_bn);
  for (const r of result.evaluation.spending) {
    const c = -r.effect_bn, source = carriers[r.id];
    if (!source) add("spending", r.id, c);
    else if (source.kind === "line") add(source.side === "receipt" ? "receipts" : "spending", source.parent_line, c);
    else if (source.kind === "capital") out.public_capital_bn += c;
    else if (source.kind === "production") out.production_bn += c;
    else throw Error(`[BLOCKED] unknown union-completion carrier kind ${source.kind}`);
  }
  out.production_bn -= result.evaluation.private_wtp_bn + result.evaluation.induced_receipts_bn;
  return out;
}
function difference(after, before) {
  return Object.fromEntries(Object.keys(after).map(key => [key, typeof after[key] === "number" ? after[key] - before[key]
    : Object.fromEntries([...new Set([...Object.keys(after[key]), ...Object.keys(before[key])])].map(line =>
      [line, (after[key][line] || 0) - (before[key][line] || 0)]))]));
}
const partsSum = parts => Object.values(parts).reduce((s, x) => s + (typeof x === "number" ? x : Object.values(x).reduce((a, b) => a + b, 0)), 0);
function coverageParts(row) {
  const d = row.decomposition;
  if (!d || !Array.isArray(d.line_parts)) throw Error("[BLOCKED] v8 coverage requires typed source-side decomposition");
  const out = {receipts_by_line: {}, spending_by_line: {},
    production_bn: -d.production.P_bn - d.production.F_bn,
    public_capital_bn: Object.values(d.capital_by_level_bn).reduce((a, b) => a + b, 0),
    post_engine_bn: d.unclassified_bn};
  for (const part of d.line_parts.filter(p => p.economic_class === "fiscal_line")) {
    const side = {receipt: "receipts", spending: "spending"}[part.source_side];
    if (!side || !part.source_line || !Number.isFinite(part.coverage_bn))
      throw Error("[BLOCKED] coverage fiscal source part has no side/line/finite amount");
    const basket = out[`${side}_by_line`];
    basket[part.source_line] = (basket[part.source_line] || 0) + part.coverage_bn;
  }
  const fiscal = [out.receipts_by_line, out.spending_by_line].reduce((sum, basket) =>
    sum + Object.values(basket).reduce((a, b) => a + b, 0), 0);
  if (!Number.isFinite(d.classified_fiscal_line_bn) || Math.abs(fiscal - d.classified_fiscal_line_bn) > 1e-9)
    throw Error("[BLOCKED] coverage fiscal source lines do not match their typed subtotal");
  if (!Number.isFinite(partsSum(out)) || Math.abs(partsSum(out) - row.total_bn) > 1e-9)
    throw Error("[BLOCKED] coverage typed source-side parts do not close");
  return out;
}
function build(api, cash, ends, gate) {
  const live = cash ? api.CASH : api, base = cash ? api.OCT14.CASH : api.OCT14;
  const payload = live.correctionsPayload(), meta = payload.meta;
  const ids = ["foreign_source_tax", "union_completion", "mixed_unit_removal", "coverage"];
  if (meta.items.some(item => item.id === "item6_low_corporate_response" && item.applied))
    throw Error("[BLOCKED] v8 attribution needs a distinct step for nondefault item6_low_corporate_response");
  const records = ids.map(id => meta.items.find(x => x.id === id && x.applied));
  if (records.some(x => !x)) throw Error("[BLOCKED] v8 attribution requires all four final items");
  gate("v8: coverage is final, with explicit set/cash source prices", !meta.coverage.stub);
  const n0 = meta.lineage.counts.lineage_population;
  const population = meta.population_v8.with_coverage;
  const count = { union_completion: meta.union_completion.counts.total, coverage: meta.coverage.net_missing_people };
  gate("v8: completion and coverage people close the counted frame (1e-6 persons)",
    Math.abs(n0 + count.union_completion + count.coverage - population) < 1e-6);
  for (const item of records.filter(x => x.edits.count)) {
    const off = payload.edits.slice(item.edits.first, item.edits.first + item.edits.count)
      .flatMap((edit, k) => edit.by ? ["personal", "shared"].map(a => Math.abs(
        Object.values(item.parts).filter(p => p.edit === k).reduce((s, p) => s + p.by[a], 0) - edit.by[a])) : []);
    gate(`v8: ${item.id} generation/lineage parts reproduce every edit (1e-9)`, Math.max(0, ...off) < 1e-9);
  }
  for (const id of ["mixed_unit_removal", "coverage"]) {
    for (const [end, row] of Object.entries(meta[id].by_end)) {
      const parts = row.by_generation_bn || row.by_generation;
      gate(`v8: ${id} ${end} generation parts add (1e-9)`,
        parts && Math.abs(Object.values(parts).reduce((s, x) => s + x, 0) - row.total_bn) < 1e-9);
    }
  }
  const foreign = records[0], changes = {}, source_parts = {};
  for (const [end, i] of ends) {
    const spec = live.MAIN_SPECS[i], full = live.evaluateFull(live.payloadModel(), spec);
    const baseFull = base.evaluateFull(base.payloadModel(), base.MAIN_SPECS[i]), baseCost = baseFull.cost_bn;
    const edits = payload.edits.slice(foreign.edits.first, foreign.edits.first + foreign.edits.count);
    const receiptDelta = edits.filter(e => e.side === "receipt" && e.scenario === live.MODEL.receipts.reference)
      .reduce((s, e) => s - spec.line_responses[`receipt:${e.line}`] * e.by[spec.allocation], 0);
    const foreignModel = api.Engine.applyCorrections(base.payloadModel(), {edits, meta: base.correctionsPayload().meta});
    const foreignFull = base.evaluateFull(foreignModel, base.MAIN_SPECS[i]), foreignCost = foreignFull.cost_bn;
    const f = foreignCost - baseCost;
    gate(`v8: ${end} item9 independently equals its responsive receipt edits (1e-9)`, Math.abs(f - receiptDelta) < 1e-9);
    // Item10 includes signed reporter carriers, native child line edits, native
    // production arrays and the credit interaction. All enter the package's
    // payloadModel route; a carrier-only sum misses its native children.
    const post = meta.mixed_unit_removal.by_end[spec.reading].total_bn + meta.coverage.by_end[spec.reading].total_bn;
    const completion = full.cost_bn - post - foreignCost;
    changes[end] = { foreign_source_tax: f, union_completion: completion,
      mixed_unit_removal: meta.mixed_unit_removal.by_end[spec.reading].total_bn,
      coverage: meta.coverage.by_end[spec.reading].total_bn };
    source_parts[end] = { foreign_source_tax: difference(sourceParts(foreignFull), sourceParts(baseFull)),
      union_completion: difference(sourceParts(full, meta.union_completion.carriers), sourceParts(foreignFull)),
      mixed_unit_removal: { post_engine_bn: changes[end].mixed_unit_removal },
      coverage: coverageParts(meta.coverage.by_end[spec.reading]) };
    for (const id of ids) gate(`v8: ${end} ${id} source-side line/production/capital parts close (1e-9)`,
      Math.abs(partsSum(source_parts[end][id]) - changes[end][id]) < 1e-9);
    const total = Object.values(changes[end]).reduce((s, x) => s + x, 0);
    gate(`v8: ${end} sequential items reproduce the whole case (1e-9)`, Math.abs(baseCost + total - full.cost_bn) < 1e-9,
      `${baseCost} + ${total} = ${full.cost_bn}`);
  }
  return { ids, changes, source_parts, count, base_population: n0, population,
    coverage_execution: "Coverage remains an additive post-engine item; source_parts expose its typed fiscal lines, capital return and signed P/F production split. Only its explicit unclassified remainder stays in post_engine_bn; source classification does not apply the coverage amount a second time.",
    coverage_production_rule: meta.coverage.production_split,
    rule: "sequential [ASSUMPTION]: measured base profiles held; item9 and item11 on receipt factor, item10 and item12 on use factor; no new age transport. At national profile completion and coverage counts cost the base's NNN per person, so the shared comparator includes every counted member. At group profile each own line group equals the exact item change." };
}
module.exports = { build, coverageParts };
