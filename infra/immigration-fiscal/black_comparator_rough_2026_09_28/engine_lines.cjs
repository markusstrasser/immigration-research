// Read-only dump of an adopted case at specs 48 / 11, methods averaged: every receipt and spending line (national,
// group amount, response, effect), the scalars, and the capital-return components.
// Cases (first argument): none = the September 27 case -> derived/engine_lines.json, the input of rekey.py;
// "sept29" = the v4 case adopted 2026-09-29 -> derived/engine_lines_sept29.json; "sept29_cash" = its cash set (pension
// switch off) -> derived/engine_lines_sept29_cash.json. The sept29 files are the input of rekey_sept29.py.
// "oct05" = the v5 case adopted 2026-10-05 (main_case_2026_10_05: v4 plus the lineage, 42.75M members)
// -> derived/engine_lines_oct05.json; "oct05_cash" = its cash set (the package's CASH) -> engine_lines_oct05_cash.json;
// "oct05_union" / "oct05_union_cash" = the identified union at v5's responses: the base's (v4) models plus audit row 8's
// change only (the lineage's last edit), evaluated at v5's specifications -> engine_lines_oct05_union[_cash].json.
// rekey_sept29.py --case oct05 reads all four: the union dumps are the 39.71M the CPS keys see, and the full dump
// less the union dump is the added people's amount on every line, their capital return and production term.
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
};
const CASE = CASES[process.argv[2] || "sept27"];
if (!CASE) throw new Error(`[BLOCKED] unknown case ${process.argv[2]}: one of ${Object.keys(CASES).join(", ")}`);
const P0 = require(path.join(FISCAL, CASE.lane, "package.cjs"));
const P = CASE.pkg ? CASE.pkg(P0) : P0;
const oo = P.withCentral(CASE.options);
const specs = P.specsFor(oo);
// The identified union at v5's responses: the base's model, audit row 8's change (the lineage's last edit, the union's
// own response move) and nothing of the added people's cells or production.
function unionOnly(method) {
  const L = P.LINEAGE_META;
  const row8 = P.LINEAGE_EDITS[L.edits.row8_edit_index - L.edits.first];
  if (L.edits.row8_edit_index !== L.edits.first + L.edits.count - 1 || P.LINEAGE_EDITS.length !== L.edits.count
    || !(row8.side === "spending" && row8.line === "lane_constants" && row8.by.shared === L.edits.row8_edit_bn)) {
    throw new Error("[BLOCKED] the lineage's last edit is not audit row 8's change");
  }
  const m = P.BASE.modelFor("central", method, oo);
  const out = P.Engine.applyCorrections(m, { edits: [row8], meta: m.corrections });
  if (!("corrections" in m)) delete out.corrections;
  return out;
}
const models = P.METHODS.map((m) => (CASE.union ? unionOnly(m) : P.modelFor("central", m, oo)));
const ENDS = { low: 48, high: 11 };
const out = {};
for (const [end, idx] of Object.entries(ENDS)) {
  const acc = {}, cap = {};
  let cost = 0, capTotal = 0, pop = 0, res = 0, welfare = 0;
  models.forEach((m) => {
    const r = P.evaluateFull(m, specs[idx]);
    const ev = r.evaluation;
    const k = models.length;
    cost += r.cost_bn / k; capTotal += r.capital.total_bn / k; welfare += ev.welfare_bn / k;
    pop += m.meta.target_population / k; res += m.meta.resident_population / k;
    for (const side of ["receipts", "spending"]) for (const l of ev[side]) {
      const key = side + "|" + l.id;
      acc[key] = acc[key] || { side, id: l.id, national_bn: 0, amount_bn: 0, response: 0, effect_bn: 0 };
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
  out[end] = { spec: idx, rate: specs[idx].rate, cost_bn: cost, capital_bn: capTotal, welfare_bn: welfare,
    target_population: pop, resident_population: res, lines: Object.values(acc), capital: Object.values(cap) };
}
fs.writeFileSync(path.join(__dirname, "derived", CASE.out), JSON.stringify(out, null, 1) + "\n");
for (const [end, o] of Object.entries(out)) console.log(`${end}: spec ${o.spec} cost ${o.cost_bn.toFixed(2)} capital ${o.capital_bn.toFixed(2)}`);
