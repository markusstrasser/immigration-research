/* Live oct14 generation split; set and cash. Uses the frozen September 29
 * generation inputs and v7_split.cjs. Every model cell, production cell, cost
 * and capital component must add to the case (1e-9; grid 1e-12). Nothing is
 * written on failure. Historical case files are inputs and remain unchanged.
 * node .../run_generations_v7.cjs [--case oct14|oct14_cash] [--out-dir DIR] */
"use strict";
const fs = require("fs"), path = require("path");
const V7 = require("./v7_split.cjs");
const { X, P7 } = V7;
const { Engine, MODEL, ALLOCS, byAlloc, sum } = X;
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i < 0 ? d : argv[i + 1]; };
const CASE = arg("--case", "oct14");
const set = { oct14: "set", oct14_cash: "cash" }[CASE];
if (!set) throw new Error("[BLOCKED] --case must be oct14 or oct14_cash");
const IN = path.join(__dirname, "derived"), OUT = path.resolve(arg("--out-dir", IN));
const load = (name) => JSON.parse(fs.readFileSync(path.join(IN, name), "utf8"));
const GENS = ["G1", "G2", "G3plus"], CONVS = ["a", "b"], TOP = Object.fromEntries(GENS.map((g) => [g, g]));
const L = V7.loadCase(set), suffix = set === "set" ? "" : "_cash";
const G29 = load(`generation_corrections_sept29${suffix}.json`);
const fails = [], checks = [];
function gate(label, ok, detail) {
  checks.push({ check: label, pass: ok, detail });
  console.log(`${ok ? "✓" : "✗"} ${label}${detail === undefined ? "" : `: ${detail}`}`);
  if (!ok) fails.push(label);
}
const cells = (m) => new Map(m.receipts.lines.flatMap((l) => Object.entries(l.cells).map(([k, c]) => [`receipt:${l.id}:${k}`, c]))
  .concat(m.spending.lines.flatMap((l) => Object.entries(l.keys).map(([k, c]) => [`spending:${l.id}:${k}`, c]))));
function addsTo(u, ms) {
  const uc = cells(u), cs = ms.map(cells);
  let gap = cs.some((c) => c.size !== uc.size) ? Infinity : 0;
  let grid = ms.some((m) => JSON.stringify(m.production.dims) !== JSON.stringify(u.production.dims)
    || ["private_wtp_bn", "induced_receipts_bn"].some((k) => m.production[k].length !== u.production[k].length)) ? Infinity : 0;
  for (const [k, c] of uc) for (const a of ALLOCS) gap = Math.max(gap, Math.abs(sum(cs.map((p) => p.get(k)?.[a].target_bn ?? NaN)) - c[a].target_bn));
  for (const k of ["private_wtp_bn", "induced_receipts_bn"]) u.production[k].forEach((v, i) => {
    grid = Math.max(grid, Math.abs(sum(ms.map((m) => m.production[k][i])) - v));
  });
  return { gap, grid };
}
gate("September 29 generation payload declares the case's base", G29.meta.union === L.baseRel, G29.meta.union);
const union29 = Engine.applyCorrections(MODEL, L.base), union = Engine.applyCorrections(MODEL, L.payload);
const models0 = {}, models29 = {}, models = {}, layers = {}, payloads = {};
for (const conv of CONVS) {
  models0[conv] = Object.fromEntries(GENS.map((g) => [g, load(`${conv === "a" ? "model_" : "model_b_"}${g}.json`)]));
  models29[conv] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], G29.payloads[conv][g])]));
  const r29 = addsTo(union29, Object.values(models29[conv]));
  gate(`${conv}: base models add cell by cell and on the production grid`, r29.gap < 1e-9 && r29.grid < 1e-12, JSON.stringify(r29));
  const lay = V7.layer(L, GENS, TOP, models29[conv], union29);
  layers[conv] = lay;
  payloads[conv] = Object.fromEntries(GENS.map((g) => [g, V7.payloadOf(G29.payloads[conv][g], lay.parts[g])]));
  models[conv] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], payloads[conv][g])]));
  const r = addsTo(union, Object.values(models[conv]));
  gate(`${conv}: v7 models add cell by cell and on the production grid`, r.gap < 1e-9 && r.grid < 1e-12, JSON.stringify(r));
  let shares = 0, amount = 0;
  for (const it of lay.items) for (const ed of it.edits) for (const p of ed.parts || []) for (const a of ALLOCS) {
    shares = Math.max(shares, Math.abs(sum(GENS.map((g) => p.share[g][a])) - 1));
    amount = Math.max(amount, Math.abs(sum(GENS.map((g) => p.bn[g][a])) - p.union_bn[a]));
  }
  gate(`${conv}: split shares and amounts close`, shares < 1e-12 && amount < 1e-9, `${shares} / ${amount}`);
}
const ev = V7.evaluator(L.payload, L.api), specs = ev.specs, AP = V7.adoptedPackage(L), O = V7.oracle(set);
const FIELDS = ["allocation", "normalization", "share", "school", "reading", "gg", "uc"];
gate("32 personal specifications agree with the package", specs.length === 32 && AP.specs.length === 32
  && specs.every((s, i) => s.allocation === "personal" && FIELDS.every((k) => JSON.stringify(s[k]) === JSON.stringify(AP.specs[i][k]))));
const full = specs.map((s) => ev.evaluateFull(union, s)), uCost = full.map((r) => r.cost_bn);
gate("consumer response overrides agree with every package specification", full.every((r, i) =>
  Object.entries(AP.specs[i].line_responses).every(([k, v]) => r.state.response_override[k] === v)));
const uncorrected = specs.map((s) => ev.cost(MODEL, s));
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost)), ends = [lo, hi];
gate("case ends and published band", ends.every((i, k) => i === O.specs[k] && Math.abs(uCost[i] - O.band[k]) < 1e-4), ends.join(" / "));
gate("case full-precision band", ends.every((i, k) => Math.abs(uCost[i] - O.full.band[k]) < 1e-9), ends.map((i) => uCost[i]).join(" / "));
const PS = V7.perSpec(set);
if (PS) gate("every published personal specification", PS.cost.size === 32 && [...PS.cost].every(([i, c]) => Math.abs(uCost[i] - c) < 1e-9));
const res = {};
let packageGap = 0;
for (let i = 0; i < specs.length; i++) packageGap = Math.max(packageGap, Math.abs(AP.cost(union, i) - uCost[i]), Math.abs(AP.cost(MODEL, i) - uncorrected[i]));
for (const conv of CONVS) {
  res[conv] = Object.fromEntries(GENS.map((g) => {
    const all = specs.map((s) => ev.evaluateFull(models[conv][g], s));
    return [g, { full: all, cost: all.map((r) => r.cost_bn), uncorrected: specs.map((s) => ev.cost(models0[conv][g], s)) }];
  }));
  let gap = 0, cap = 0;
  specs.forEach((s, i) => {
    for (const kind of ["cost", "uncorrected"]) gap = Math.max(gap, Math.abs(sum(GENS.map((g) => res[conv][g][kind][i])) - (kind === "cost" ? uCost[i] : uncorrected[i])));
    full[i].capital.components.forEach((c, j) => { cap = Math.max(cap, Math.abs(sum(GENS.map((g) => res[conv][g].full[i].capital.components[j].return_bn)) - c.return_bn)); });
    for (const g of GENS) packageGap = Math.max(packageGap, Math.abs(AP.cost(models[conv][g], i) - res[conv][g].cost[i]), Math.abs(AP.cost(models0[conv][g], i) - res[conv][g].uncorrected[i]));
  });
  gate(`${conv}: generations add at every specification, corrected and uncorrected; every capital component`, gap < 1e-9 && cap < 1e-9, `${gap} / ${cap}`);
}
gate("package and independent consumer agree for all models/specifications", packageGap < 1e-9, packageGap);
if (set === "set") {
  const A = X.readJson(`${V7.V7_LANE}/derived/api_check.json`);
  const chk = A.patterns.flatMap((p) => p.checks).find((c) => /with the edit sets' edits by the rule/.test(c.check));
  const printed = chk && chk.detail.match(/at specifications (\d+) \/ (\d+): (.*)$/);
  const got = printed ? Object.fromEntries(printed[3].split("; ").map((s) => {
    const [g, a, , b] = s.split(" "); return [g, [Number(a), Number(b)]];
  })) : null;
  const alt = V7.layer(L, GENS, TOP, models29.a, union29, { alt: ["row8_on_g3plus", "pension_receipt_shares"] });
  const altModels = GENS.map((g) => Engine.applyCorrections(models0.a[g], V7.payloadOf(G29.payloads.a[g], alt.parts[g])));
  const r = addsTo(union, altModels);
  gate("G4 pattern 3 reference: row 8 on G3+, pension union by receipts; split still closes", r.gap < 1e-9 && r.grid < 1e-12
    && chk?.pass === true && got && Number(printed[1]) === lo && Number(printed[2]) === hi
    && GENS.every((g, j) => ends.every((i, k) => Math.abs(ev.cost(altModels[j], specs[i]) - got[g][k]) < 5e-5)));
}
// Same row-4 headcounts and measured added-age mix as v6; the added people stay on G3+.
const H = load("v4_inputs.json").headcount, lin = L.lineage;
const AA = V7.addedAdults(lin, H.a.G3plus.adults / H.a.G3plus.population);
const population = H.union.population + lin.counts.added, adults = H.union.adults + AA.adults;
gate("headcount equals the case lineage", Math.abs(population - lin.counts.lineage_population) < 1e-3, population);
const per = (bn, n) => bn * 1e9 / n;
const summary = { case: CASE, set, lane: V7.V7_LANE, payload: L.rel, status: L.payload.meta.status, adopted: L.payload.meta.adopted,
  builds_on: { payload: L.baseRel, generation_payloads: `generation_account_2026_09_24/derived/generation_corrections_sept29${suffix}.json` },
  oracle: O, responses: L.payload.meta.responses, low_spec: specs[lo], high_spec: specs[hi],
  specifications: { low: specs[lo], high: specs[hi], low_index: lo, high_index: hi },
  union: { cost_bn: ends.map((i) => uCost[i]), uncorrected_bn: ends.map((i) => uncorrected[i]), population, adults,
    per_member_usd: ends.map((i) => per(uCost[i], population)), per_adult_usd: ends.map((i) => per(uCost[i], adults)) },
  added_adults: AA, lineage: lin, items: { order: L.items.map((it) => it.id), all: L.records.map((r) => r.id), records: L.records,
    split: Object.fromEntries(CONVS.map((c) => [c, layers[c].items])) }, conventions: {}, gates: { failed: fails, checks } };
const rows = [];
for (const conv of CONVS) {
  summary.conventions[conv] = {};
  for (const g of GENS) {
    const h = { population: H[conv][g].population + (g === "G3plus" ? lin.counts.added : 0), adults: H[conv][g].adults + (g === "G3plus" ? AA.adults : 0) };
    const r = res[conv][g], c = ends.map((i) => r.cost[i]);
    summary.conventions[conv][g] = Object.assign({}, h, { cost_bn: c, own_span_bn: [Math.min(...r.cost), Math.max(...r.cost)],
      uncorrected_cost_bn: ends.map((i) => r.uncorrected[i]), correction_bn: ends.map((i) => r.cost[i] - r.uncorrected[i]),
      per_member_usd: c.map((v) => per(v, h.population)), per_adult_usd: c.map((v) => per(v, h.adults)) });
    ends.forEach((i, k) => {
      const receipts = r.full[i].evaluation.receipts;
      const receiptCost = (id) => -(receipts.find((x) => x.id === id)?.effect_bn || 0);
      rows.push({ convention: conv, generation: g, band_end: k === 0 ? "low" : "high", allocation: specs[i].allocation, cost_bn: r.cost[i],
        uncorrected_same_spec_bn: r.uncorrected[i], correction_bn: r.cost[i] - r.uncorrected[i], population: h.population, adults: h.adults,
        per_member_usd: per(r.cost[i], h.population), per_adult_usd: per(r.cost[i], h.adults), capital_return_bn: r.full[i].capital.total_bn,
        enterprise_surplus_receipt_bn: receiptCost(X.P.ENTERPRISE_LINE), housing_enterprise_surplus_receipt_bn: receiptCost("housing_enterprise_surplus") });
    });
  }
}
if (fails.length) { console.error(`[BLOCKED] ${fails.length} gates failed; nothing written`); process.exit(1); }
fs.mkdirSync(OUT, { recursive: true });
const header = Object.keys(rows[0]);
fs.writeFileSync(path.join(OUT, `generation_results_${CASE}.csv`), [header.join(","), ...rows.map((r) => header.map((k) => typeof r[k] === "number" ? r[k].toFixed(6) : r[k]).join(","))].join("\n") + "\n");
fs.writeFileSync(path.join(OUT, `generation_summary_${CASE}.json`), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, `generation_corrections_${CASE}.json`), JSON.stringify({ meta: { source: "generation_account_2026_09_24/run_generations_v7.cjs",
  case: CASE, case_lane: V7.V7_LANE, union: L.rel, status: L.payload.meta.status, builds_on: summary.builds_on.generation_payloads,
  layout: "September 29 generation payload plus v6 R1–R4 and v7 tagged parts; apply with case meta.responses and capital_return",
  items: summary.items.order }, payloads }) + "\n");
console.log(`case ${CASE}: ${summary.union.cost_bn.join(" / ")} bn; all ${checks.length} gates passed`);
