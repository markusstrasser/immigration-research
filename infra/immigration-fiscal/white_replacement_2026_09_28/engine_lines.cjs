// Dump of the live adopted case at its own ends, methods averaged: every receipt and spending line (national,
// group amount, response, effect), the scalars, and the capital-return components.
// Cases (first argument): none = oct14 (live v7); explicit sept27 is the archived September 27 library route.
// "sept29" = the v4 case adopted 2026-09-29 -> derived/engine_lines_sept29.json; "sept29_cash" = its cash set (pension
// switch off) -> derived/engine_lines_sept29_cash.json. The sept29 files are the input of rekey_sept29.py.
// "oct05" = the v5 case adopted 2026-10-05 (main_case_2026_10_05: v4 plus the lineage, 42.75M members)
// -> derived/engine_lines_oct05.json; "oct05_cash" = its cash set (the package's CASH) -> engine_lines_oct05_cash.json;
// "oct05_union" / "oct05_union_cash" = the identified union at v5's responses: the base's (v4) models plus audit row 8's
// change only (the lineage's last edit), evaluated at v5's specifications -> engine_lines_oct05_union[_cash].json.
// rekey_sept29.py --case oct05 reads all four: the union dumps are the 39.71M the CPS keys see, and the full dump
// less the union dump is the added people's amount on every line, their capital return and production term.
// "oct07" = main case v6 (main_case_2026_10_07: v5 plus the items of meta.items) and "oct07_cash" its cash set;
// "oct07_union" / "oct07_union_cash" = the identified union at v6: the base's models, row 8's change and every
// applied edit set's union part, in payload order (itemUnionEdits), with a union-only item's carrier receipt lines.
// Without the items the union dump would leave their union parts in the full dump less the union dump, where
// rekey_sept29.py books them as the added people's.
// Those oct07 files are preserved. Their computed route is now oct14 / oct14_cash / oct14_union / oct14_union_cash:
// v7's own personal ends, allocation item skipped only when it has zero edits, every edit set split by named parts.
"use strict";
const fs = require("fs");
const path = require("path");
const FISCAL = path.resolve(__dirname, "..");
const CASES = {
  sept27: { lane: "main_case_long_run_2026_09_27", options: {}, out: "engine_lines.json" },
  sept29: { lane: "main_case_2026_09_29", options: {}, out: "engine_lines_sept29.json" },
  sept29_cash: { lane: "main_case_2026_09_29", options: { pension4: "cash" }, out: "engine_lines_sept29_cash.json" },
  oct05: { lane: "main_case_2026_10_05", options: {}, out: "engine_lines_oct05.json" },
  oct05_cash: { lane: "main_case_2026_10_05", pkg: (p) => p.CASH, options: {}, out: "engine_lines_oct05_cash.json" },
  oct05_union: { lane: "main_case_2026_10_05", options: {}, union: true, out: "engine_lines_oct05_union.json" },
  oct05_union_cash: { lane: "main_case_2026_10_05", pkg: (p) => p.CASH, options: {}, union: true, out: "engine_lines_oct05_union_cash.json" },
  oct14: { lane: "main_case_2026_10_14", options: {}, out: "engine_lines_oct14.json" },
  oct14_cash: { lane: "main_case_2026_10_14", pkg: (p) => p.CASH, options: {}, out: "engine_lines_oct14_cash.json" },
  oct14_union: { lane: "main_case_2026_10_14", options: {}, union: true, out: "engine_lines_oct14_union.json" },
  oct14_union_cash: { lane: "main_case_2026_10_14", pkg: (p) => p.CASH, options: {}, union: true, out: "engine_lines_oct14_union_cash.json" },
  oct15: { lane: "main_case_2026_10_15", options: {}, out: "engine_lines_oct15.json" },
  oct15_cash: { lane: "main_case_2026_10_15", pkg: (p) => p.CASH, options: {}, out: "engine_lines_oct15_cash.json" },
  oct15_union: { lane: "main_case_2026_10_15", options: {}, union: true, out: "engine_lines_oct15_union.json" },
  oct15_union_cash: { lane: "main_case_2026_10_15", pkg: (p) => p.CASH, options: {}, union: true, out: "engine_lines_oct15_union_cash.json" },
};
const CASE = CASES[process.argv[2] || "oct15"];
if (!CASE) throw new Error(`[BLOCKED] unknown case ${process.argv[2]}: one of ${Object.keys(CASES).join(", ")}`);
const P0 = require(path.join(FISCAL, CASE.lane, "package.cjs"));
const P = CASE.pkg ? CASE.pkg(P0) : P0;
const oo = P.withCentral(CASE.options);
const specs = P.specsFor(oo);
// The union's part of each applied edit set in the payload's meta.items (v6; none before), in payload order:
//   a national-scale edit {side, line, national_bn} as it is: it scales every cell of its line by the same factor in
//     either model, since the union model's national totals are the case's (gated below), so on the union model it
//     moves the union's own cells only;
//   every edit of an item whose record states that its edits are all the union's (union_only, its reason), as it is;
//     its parts then name the item's terms, not a split between the union and the added people;
//   another cell shift with named parts: the sum of the parts named union_* (the parts must add to the edit exactly and
//     be named union_* or lineage_*; the lineage_* parts are the added people's, in the case less the union).
// A union-only item's carrier receipt lines (its record's capital.receipt_lines) go into the union model as the payload
// has them; the union model must then carry them as the case's model does (gated below).
function itemUnionEdits() {
  const p = P.correctionsPayload();
  const out = [], carriers = [];
  for (const r of p.meta.items || []) {
    // The comparator library retains its observed 39.71M base. Completion's
    // own-record prices and post-engine terms travel in the full-minus-base overlay.
    if (CASE.lane === "main_case_2026_10_15" && ["union_completion", "mixed_unit_removal", "coverage"].includes(r.id)) continue;
    if (r.kind === "lineage" || !r.applied) continue;    // the lineage item's edits are the lineage's (the overlay)
    if (r.kind === "allocation" && r.edits && r.edits.count === 0) continue;
    if (r.id === "item6_low_corporate_response" && r.kind === "response" && r.edits?.count === 0) continue;
    if (r.kind !== "edit_set" || !r.edits) throw new Error(`[BLOCKED] item ${r.id}: an applied item of kind ${r.kind} without edits`);
    const edits = p.edits.slice(r.edits.first, r.edits.first + r.edits.count);
    if (edits.length !== r.edits.count) throw new Error(`[BLOCKED] item ${r.id}: its edits are not in the payload`);
    const ids = (r.capital && r.capital.receipt_lines) || [];
    if (ids.length && !r.union_only) throw new Error(`[BLOCKED] item ${r.id}: carrier receipt lines on an item that is not union_only`);
    for (const id of ids) {
      const l = (p.receipt_lines || []).filter((x) => x.id === id);
      if (l.length !== 1) throw new Error(`[BLOCKED] item ${r.id}: carrier ${id} is not one receipt line of the payload`);
      carriers.push(l[0]);
    }
    edits.forEach((e, k) => {
      if (e.national_bn !== undefined) { out.push(e); return; }
      const parts = Object.entries(r.parts || {}).filter(([, x]) => x.edit === k);
      if (r.union_only) {
        if (parts.length && !["personal", "shared"].every((a) => parts.reduce((t, [, x]) => t + x.by[a], 0) === e.by[a])) {
          throw new Error(`[BLOCKED] item ${r.id}: the parts of edit ${k} do not add to it`);
        }
        out.push(e);
        return;
      }
      if (!parts.length) throw new Error(`[BLOCKED] item ${r.id}: cell shift ${k} names no parts and the item is not union_only`);
      const odd = parts.filter(([n]) => !/^(union|lineage)_/.test(n));
      if (odd.length) throw new Error(`[BLOCKED] item ${r.id}: parts ${odd.map(([n]) => n).join(", ")} are neither union_* nor lineage_*`);
      const sum = (f) => Object.fromEntries(["personal", "shared"].map((a) => [a, parts.filter(([n]) => f(n)).reduce((t, [, x]) => t + x.by[a], 0)]));
      const all = sum(() => true);
      if (!["personal", "shared"].every((a) => Math.abs(all[a] - e.by[a]) <= 1e-12)) throw new Error(`[BLOCKED] item ${r.id}: the parts of edit ${k} do not add to it (1e-12bn)`);
      out.push(Object.assign({}, e, { by: sum((n) => n.startsWith("union_")) }));
    });
  }
  return { edits: out, carriers };
}
const ITEM_UNION = CASE.union ? itemUnionEdits() : { edits: [], carriers: [] };
// The identified union at v5's responses: the base's model, audit row 8's change (the lineage's last edit, the union's
// own response move) and nothing of the added people's cells or production; on v6 also each item's union part.
function unionOnly(method) {
  const L = P.LINEAGE_META;
  const row8 = P.LINEAGE_EDITS[L.edits.row8_edit_index - L.edits.first];
  if (L.edits.row8_edit_index !== L.edits.first + L.edits.count - 1 || P.LINEAGE_EDITS.length !== L.edits.count
    || !(row8.side === "spending" && row8.line === "lane_constants" && row8.by.shared === L.edits.row8_edit_bn)) {
    throw new Error("[BLOCKED] the lineage's last edit is not audit row 8's change");
  }
  const m = P.BASE.modelFor("central", method, oo);
  const out = P.Engine.applyCorrections(m, Object.assign({ edits: [row8].concat(ITEM_UNION.edits), meta: m.corrections },
    ITEM_UNION.carriers.length ? { receipt_lines: ITEM_UNION.carriers } : {}));
  if (!("corrections" in m)) delete out.corrections;
  if (ITEM_UNION.edits.length || ITEM_UNION.carriers.length) {
    // The union model's national totals must be the case's, line by line (the scale edits then scale alike), and its
    // carriers the case model's, cell by cell (their keys are the union's alone).
    const full = P.modelFor("central", method, oo);
    const nat = (x) => JSON.stringify(["spending", "receipts"].map((s) => x[s].lines.filter(l => !l.id.startsWith("union_completion_")).map((l) => [l.id, l.national_bn])));
    if (nat(out) !== nat(full)) throw new Error(`[BLOCKED] ${method}: the union model's national totals are not the case's`);
    const car = (x) => JSON.stringify(ITEM_UNION.carriers.map((c) => x.receipts.lines.find((l) => l.id === c.id)));
    if (car(out) !== car(full)) throw new Error(`[BLOCKED] ${method}: the union model's carrier lines are not the case model's`);
  }
  return CASE.lane === "main_case_2026_10_15" ? P.withSyntheticLines(out) : out;
}
const models = P.METHODS.map((m) => (CASE.union ? unionOnly(m) : P.modelFor("central", m, oo)));
const summary = JSON.parse(fs.readFileSync(path.join(FISCAL, CASE.lane, "derived", "summary.json"), "utf8"));
const isV8 = CASE.lane === "main_case_2026_10_15";
const isV7 = isV8 || CASE.lane === "main_case_2026_10_14";
const declared = isV7 ? summary[isV8 ? "v8" : "v7"].end_specifications[CASE.pkg ? "cash" : "set"] : null;
const ends = isV8 ? declared[0] : declared;
if (isV8 && JSON.stringify(declared[0]) !== JSON.stringify(declared[1])) throw Error("[BLOCKED] comparator methods have different ends");
const ENDS = isV7 ? { low: ends[0], high: ends[1] } : { low: 48, high: 11 };
const specAt = (idx) => {
  if (!Number.isInteger(idx)) throw new Error(`[BLOCKED] case end ${idx} is not an integer specification index`);
  const s = specs[idx];  // v7 preserves v6's numbering 0–31 for the personal specifications
  if (!s || (isV7 && s.allocation !== "personal")) throw new Error(`[BLOCKED] case end ${idx} is not a personal specification`);
  return s;
};
const out = {};
for (const [end, idx] of Object.entries(ENDS)) {
  const acc = {}, cap = {};
  let cost = 0, capTotal = 0, pop = 0, res = 0, welfare = 0;
  const post_engine = { mixed_unit_removal_bn: 0, coverage_bn: 0, total_bn: 0 };
  models.forEach((m) => {
    const r = P.evaluateFull(m, specAt(idx));
    const ev = r.evaluation;
    const k = models.length;
    const post = r.post_engine || { total_bn: 0 };
    cost += (r.cost_bn - (CASE.union && isV8 ? post.total_bn : 0)) / k;
    if (!CASE.union) for (const key of Object.keys(post_engine)) post_engine[key] += (post[key] || 0) / k;
    capTotal += r.capital.total_bn / k; welfare += ev.welfare_bn / k;
    pop += m.meta.target_population / k; res += m.meta.resident_population / k;
    for (const side of ["receipts", "spending"]) for (const l of ev[side]) {
      const key = side + "|" + l.id;
      const selection = isV8 ? require('./dump_selection.cjs').selectionFor(side, l, m) : {};
      if (isV8 && Object.values(selection).some(v => typeof v !== 'string')) throw Error(`[BLOCKED] ${key}: no selected key/scenario`);
      if (acc[key] && isV8 && Object.entries(selection).some(([name, value]) => acc[key][name] !== value)) throw Error(`[BLOCKED] ${key}: methods select different key/scenario`);
      acc[key] = acc[key] || { side, id: l.id, ...selection, national_bn: 0, amount_bn: 0, response: 0, effect_bn: 0 };
      acc[key].national_bn += l.national_bn / k; acc[key].amount_bn += l.amount_bn / k;
      acc[key].response += l.response / k; acc[key].effect_bn += l.effect_bn / k;
    }
    for (const s of Object.keys(ev)) if (!["receipts", "spending"].includes(s) && typeof ev[s] === "number") {
      acc["scalar|" + s] = acc["scalar|" + s] || { side: "scalar", id: s, effect_bn: 0 };
      acc["scalar|" + s].effect_bn += ev[s] / k;
    }
    for (const c of r.capital.components) {
      cap[c.id] = cap[c.id] || { id: c.id, stock_charged_bn: c.stock_charged_bn, key: 0, response: c.response, return_bn: 0 };
      cap[c.id].key += c.key / k; cap[c.id].return_bn += c.return_bn / k;
    }
  });
  const orderedLines = Object.values(acc);
  if (isV8) orderedLines.sort((a, b) => (a.side + '|' + a.id).localeCompare(b.side + '|' + b.id));
  out[end] = { spec: idx, allocation: specAt(idx).allocation, rate: specAt(idx).rate, cost_bn: cost, capital_bn: capTotal, welfare_bn: welfare,
    target_population: isV8 && !CASE.union ? P.POPULATION_V8.with_coverage : pop,
    resident_population: res, lines: orderedLines, capital: Object.values(cap), ...(isV8 ? {post_engine} : {}) };
}
fs.writeFileSync(path.join(__dirname, "derived", CASE.out), JSON.stringify(out, null, 1) + "\n");
for (const [end, o] of Object.entries(out)) console.log(`${end}: spec ${o.spec} cost ${o.cost_bn.toFixed(2)} capital ${o.capital_bn.toFixed(2)}`);
