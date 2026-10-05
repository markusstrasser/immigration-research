/* Step 8: the main case of 2026-10-05 (v5, main_case_2026_10_05, adopted at 22:54 JST: the September 29 case plus the
 * descendants who no longer report Mexican origin, counted whole) by generation.
 *
 * --case picks the set:
 *   oct05       the case ($390.2940-461.2431bn at specifications 48 / 11);
 *   oct05_cash  the cash set beside it: the same lineage with the pension switch off ($307.3764-383.4093bn).
 * The case is the September 29 payload of the same set unchanged plus the lineage's edits, production and responses
 * (v5_split.cjs), so each generation's payload is its September 29 payload (derived/generation_corrections_sept29*.json,
 * which run_generations_v4.cjs writes and reproduces byte for byte) plus its v5 part:
 *   - G3+ takes the lineage's cell edits and the production grid's change: the 3.04M added people are third-plus
 *     (the case's package.cjs withLineage(), main_case_2026_10_05 RESULT "Consumers");
 *   - every generation takes audit row 8's change at the larger group (the lineage's last edit, the union's response
 *     move) times its share of the September 29 union's lane_constants k cell, per allocation;
 *   - every generation is evaluated at the case's responses, which move with the group's size.
 * Under convention (b) the added people stay in G3+ [ASSUMPTION: their parents' generation is not observed; the summary
 * gives the move had their minors followed the identified G3+'s]. Per-member figures add them to G3+ (17.38M members
 * under (a)), with adults at the identified G3+'s adult share [ASSUMPTION: the case prices them at that age mix].
 *
 * Gates (exit 1, nothing written):
 *   - the September 29 generation payloads split the case's base payload: their models add to the union's September 29
 *     model cell by cell (1e-9) and their grids to its grid (1e-12);
 *   - the row-8 shares add to 1 (1e-12) under each convention;
 *   - each generation's v5 payload gives its September 29 model with its v5 part; G3+'s is the package's own
 *     withLineage() of its September 29 model with row 8 moved to its share (1e-12, cells and grid);
 *   - under each convention the three v5 models add to the case's payload model cell by cell (1e-9) and grid (1e-12);
 *   - the consumer's 64 specifications are the v5 package's, in order;
 *   - the union reproduces the case's band at its end specifications (main_case_bands.csv, 1e-4), its cost at every
 *     specification (per_spec.csv, the set; 1e-9) and the uncorrected model at the case's responses (1e-4);
 *   - in all 64 specifications the generations add to the union, corrected and uncorrected (1e-9), and so do their
 *     capital returns (total, by level, by part) and enterprise receipts;
 *   - the v5 package's evaluateFull gives every model's cost here (1e-9);
 *   - the change from the September 29 case by part, at the end specifications (the September 29 case's too): each
 *     model starts at its September 29 cost (the union at the September 29 band, 1e-4; each generation at
 *     generation_results_sept29*.csv, 5.01e-7, half its last printed digit) and ends at its v5 cost (1e-9); the
 *     generations add to the union part by part (1e-9); the union's parts are the lineage lane's (v5_summary.json arm b:
 *     the response move with row 8, and the G3+ and white parts together, 1e-9) and, for the set, the case lane's
 *     summary.json change_at_fixed_specifications (1e-9);
 *   - the alternative's split adds to the union (1e-9); for the set under (a) it is main_case_2026_10_05 api_check.json
 *     pattern 3's by-generation print (5e-5, its four decimals).
 * Writes generation_results_<case>.csv, generation_summary_<case>.json and generation_corrections_<case>.json. Run from
 * the repository root:
 *   node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v5.cjs [--case oct05|oct05_cash] [--out-dir DIR]
 */
"use strict";
const fs = require("fs");
const path = require("path");
const V5 = require(path.join(__dirname, "v5_split.cjs"));
const { X } = V5;
const { P, Engine, MODEL, ALLOCS, byAlloc, sum } = X;

const HERE = __dirname;
const argv = process.argv.slice(2);
const arg = (name, dflt) => { const i = argv.indexOf(name); return i < 0 ? dflt : argv[i + 1]; };
const CASES = { oct05: "set", oct05_cash: "cash" };
const SEPT29 = { oct05: "sept29", oct05_cash: "sept29_cash" };
const CASE = arg("--case", "oct05");
if (!CASES[CASE]) throw new Error(`--case must be one of ${Object.keys(CASES).join(", ")}`);
const GENS = ["G1", "G2", "G3plus"];
const TOP = Object.fromEntries(GENS.map((g) => [g, g]));
const CONVS = ["a", "b"];
const IN = path.join(HERE, "derived");
const OUT = path.resolve(arg("--out-dir", IN));
const load = (f) => JSON.parse(fs.readFileSync(path.join(IN, f), "utf8"));
const fails = [];
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) fails.push(label);
}
const e = (x) => x.toExponential(1);
const near = (a, b, tol) => Math.abs(a - b) < tol;
const f2 = (xs) => xs.map((x) => x.toFixed(2)).join(" – ");
const sgn = (x) => (x >= 0 ? "+" : "") + x.toFixed(2);
const cellsOf = (m) => {
  const out = new Map();
  for (const l of m.receipts.lines) for (const sc of Object.keys(l.cells)) out.set(`r|${l.id}|${sc}`, l.cells[sc]);
  for (const l of m.spending.lines) for (const k of Object.keys(l.keys)) out.set(`s|${l.id}|${k}`, l.keys[k]);
  return out;
};
const GRID = ["private_wtp_bn", "induced_receipts_bn"];
// The largest difference between a model and the sum of parts, over every cell and allocation and over the grid.
function addsTo(whole, parts) {
  const w = cellsOf(whole), ps = parts.map(cellsOf);
  let cells = ps.some((p) => p.size !== w.size) ? Infinity : 0, grid = 0;
  for (const [k, c] of w) for (const a of ALLOCS) cells = Math.max(cells, Math.abs(sum(ps.map((p) => p.get(k)[a].target_bn)) - c[a].target_bn));
  for (const k of GRID) whole.production[k].forEach((v, i) => { grid = Math.max(grid, Math.abs(sum(parts.map((m) => m.production[k][i])) - v)); });
  return { cells, grid, n: w.size };
}
function sameModel(a, b) {
  const x = cellsOf(a), y = cellsOf(b);
  let worst = x.size !== y.size ? Infinity : 0;
  for (const [k, c] of y) for (const al of ALLOCS) worst = Math.max(worst, Math.abs(x.get(k)[al].target_bn - c[al].target_bn));
  for (const k of GRID) {
    if (a.production[k].length !== b.production[k].length) worst = Infinity;
    a.production[k].forEach((v, i) => { worst = Math.max(worst, Math.abs(v - b.production[k][i])); });
  }
  return worst;
}

const L = V5.loadCase(CASES[CASE]);
console.log(`[case ${CASE}] ${L.rel}: ${L.baseRel} plus ${L.lineage.edits.count} lineage edits; outputs to ${path.relative(process.cwd(), OUT) || "."}`);

// ---------------------------------------------------------------------------------------------------
console.log("[the September 29 generation payloads]");
const G29 = load(`generation_corrections_${SEPT29[CASE]}.json`);
gate(`generation_corrections_${SEPT29[CASE]}.json splits the case's base payload, ${L.baseRel}`,
  G29.meta.case === SEPT29[CASE] && G29.meta.union === L.baseRel, G29.meta.union);
const models0 = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) => [g, load(`${c === "a" ? "model_" : "model_b_"}${g}.json`)]))]));
const models29 = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[c][g], G29.payloads[c][g])]))]));
const union29 = Engine.applyCorrections(MODEL, L.base);
for (const conv of CONVS) {
  const r = addsTo(union29, GENS.map((g) => models29[conv][g]));
  gate(`(${conv}) the September 29 generation models add to the union's September 29 model: every cell and the production grid`,
    r.cells < 1e-9 && r.grid < 1e-12, `${r.n} cells, max |diff| ${e(r.cells)} bn; grid ${e(r.grid)} bn`);
}

// ---------------------------------------------------------------------------------------------------
console.log("[the v5 part: the lineage on G3+, row 8 by lane_constants k share]");
const layers = {}, payloads = {}, models5 = {}, models29r = {};
for (const conv of CONVS) {
  const lay = V5.layer(L, GENS, TOP, models29[conv], union29);
  layers[conv] = lay;
  gate(`(${conv}) the row-8 shares add to 1 in both allocations`, lay.share_sum_error < 1e-12,
    `${e(lay.share_sum_error)}; ` + GENS.map((g) => `${g} ${lay.share[g].personal.toFixed(4)}/${lay.share[g].shared.toFixed(4)}`).join(", "));
  payloads[conv] = Object.fromEntries(GENS.map((g) => [g, V5.payloadOf(G29.payloads[conv][g], lay.parts[g])]));
  models5[conv] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], payloads[conv][g])]));
  models29r[conv] = Object.fromEntries(GENS.map((g) => [g, V5.withEdits(models29[conv][g], [lay.parts[g].row8])]));
  // The payload route against the package's: G3+ is withLineage() of its September 29 model with row 8 moved from the
  // whole edit to its share; the others are their September 29 models with their row-8 share.
  let worst = 0;
  for (const g of GENS) {
    const want = g === lay.g3plus
      ? V5.withEdits(L.api.withLineage(models29[conv][g]), [Object.assign({}, V5.ROW8, { by: byAlloc((a) => L.row8.by[a] * (lay.share[g][a] - 1)) })])
      : models29r[conv][g];
    worst = Math.max(worst, sameModel(models5[conv][g], want));
  }
  gate(`(${conv}) each generation's v5 payload gives its September 29 model with its part; G3+'s is the package's withLineage() with row 8 at its share`,
    worst < 1e-12, `max |diff| ${e(worst)} bn`);
}
const union5 = Engine.applyCorrections(MODEL, L.payload);
for (const conv of CONVS) {
  const r = addsTo(union5, GENS.map((g) => models5[conv][g]));
  gate(`(${conv}) the three v5 models add to the case's payload model: every cell and the production grid`,
    r.cells < 1e-9 && r.grid < 1e-12, `${r.n} cells, max |diff| ${e(r.cells)} bn; grid ${e(r.grid)} bn`);
}

// ---------------------------------------------------------------------------------------------------
console.log("[engine]");
const ev = X.evaluator(L.payload);
const specs = ev.specs;
const AP = V5.adoptedPackage(L);
const SPEC_FIELDS = ["allocation", "normalization", "share", "school", "reading", "gg", "uc"];
gate(`the consumer's 64 specifications are ${AP.source}'s, in order (allocation, normalization, school share and response, reading and general government, uninsured key)`,
  specs.length === 64 && AP.specs.length === specs.length && specs.every((s, i) => SPEC_FIELDS.every((k) => s[k] === AP.specs[i][k])));
const uFull = specs.map((s) => ev.evaluateFull(union5, s));
const uCost = uFull.map((r) => r.cost_bn);
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
const O = V5.oracle(L.set);
gate(`the corrected union reproduces the case's band at its end specifications (${O.source}, four decimals)`,
  lo === O.specs[0] && hi === O.specs[1] && near(uCost[lo], O.band[0], 1e-4) && near(uCost[hi], O.band[1], 1e-4),
  `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)} at ${lo} / ${hi}`);
const PS = V5.perSpec(L.set);
if (PS) {
  let worst = 0;
  for (const [i, c] of PS.cost) worst = Math.max(worst, Math.abs(uCost[i] - c));
  gate(`the corrected union reproduces ${PS.source} at each of its specifications (mean of the two methods)`,
    PS.cost.size === 64 && worst < 1e-9, `${PS.cost.size} specifications; max |diff| ${e(worst)} bn`);
} else console.log(`  · ${V5.V5_LANE} publishes no per-specification cost for the ${L.set} set`);
const u0Cost = specs.map((s) => ev.cost(MODEL, s));
const lo0 = u0Cost.indexOf(Math.min(...u0Cost)), hi0 = u0Cost.indexOf(Math.max(...u0Cost));
gate(`the uncorrected model at the case's responses reproduces ${O.source.replace(/ \(.*\)$/, "")} uncorrected_at_adopted_responses (1e-4)`,
  near(u0Cost[lo0], O.uncorrected[0], 1e-4) && near(u0Cost[hi0], O.uncorrected[1], 1e-4), `${u0Cost[lo0].toFixed(4)}–${u0Cost[hi0].toFixed(4)} at ${lo0} / ${hi0}`);
const capWhere = (r, pred) => r.capital.components.filter(pred).reduce((a, c) => a + c.return_bn, 0);
const receiptCost = (r, id) => { const x = r.evaluation.receipts.find((y) => y.id === id); return x ? -x.effect_bn : 0; };
const capRow = (r) => ({ cost_bn: r.cost_bn, capital_total_bn: r.capital.total_bn,
  capital_state_local_bn: capWhere(r, (c) => c.level === "state_local"), capital_federal_bn: capWhere(r, (c) => c.level === "federal"),
  capital_core_bn: capWhere(r, (c) => c.group === "core"), capital_block_bn: capWhere(r, (c) => c.group === "block"),
  capital_enterprise_bn: capWhere(r, (c) => c.group === "enterprise"),
  enterprise_surplus_receipt_bn: receiptCost(r, P.ENTERPRISE_LINE), housing_enterprise_surplus_receipt_bn: receiptCost(r, "housing_enterprise_surplus") });
const res = {};
for (const conv of CONVS) {
  res[conv] = {};
  for (const g of GENS) {
    const full = specs.map((s) => ev.evaluateFull(models5[conv][g], s));
    res[conv][g] = { full, corrected: full.map((r) => r.cost_bn), uncorrected: specs.map((s) => ev.cost(models0[conv][g], s)) };
  }
  for (const [kind, ref] of [["corrected", uCost], ["uncorrected", u0Cost]]) {
    const worst = Math.max(...specs.map((_, i) => Math.abs(sum(GENS.map((g) => res[conv][g][kind][i])) - ref[i])));
    gate(`(${conv}) ${kind}: the three generations add to the union in all ${specs.length} specifications`, worst < 1e-9, `max |diff| ${e(worst)} bn`);
  }
  let worstCap = 0;
  specs.forEach((_, i) => {
    const u = capRow(uFull[i]), parts = GENS.map((g) => capRow(res[conv][g].full[i]));
    for (const k of Object.keys(u)) worstCap = Math.max(worstCap, Math.abs(sum(parts.map((x) => x[k])) - u[k]));
  });
  gate(`(${conv}) the generations' capital return (total, by level, by part) and enterprise receipts add to the union's in all specifications`,
    worstCap < 1e-9, `max |diff| ${e(worstCap)} bn`);
}
{
  let worst = 0;
  specs.forEach((_, i) => {
    worst = Math.max(worst, Math.abs(AP.cost(union5, i) - uCost[i]), Math.abs(AP.cost(MODEL, i) - u0Cost[i]));
    for (const conv of CONVS) for (const g of GENS) {
      worst = Math.max(worst, Math.abs(AP.cost(models5[conv][g], i) - res[conv][g].corrected[i]),
        Math.abs(AP.cost(models0[conv][g], i) - res[conv][g].uncorrected[i]));
    }
  });
  gate(`${AP.source} evaluateFull gives every model's cost here (union and generations, corrected and uncorrected, all specifications)`,
    worst < 1e-9, `max |diff| ${e(worst)} bn`);
}

// ---------------------------------------------------------------------------------------------------
// The change from the September 29 case by part, at the case's end specifications (the September 29 case's too): the
// September 29 model at the September 29 specification; the same model at v5's (the responses that move with the
// group's size); plus its row-8 share; plus the added people (G3+ only). The parts telescope to the v5 cost.
console.log("[change from the September 29 case, by part]");
const ev29 = X.evaluator(L.base);
const specs29 = ev29.specs;
const O29 = X.oracle(L.set);
gate(`the September 29 case's specifications are this case's but for the group-size responses, and its ends are the same (${O29.source})`,
  specs29.length === specs.length && specs29.every((s, i) => SPEC_FIELDS.filter((k) => k !== "gg").every((k) => s[k] === specs[i][k]))
  && O29.specs[0] === lo && O29.specs[1] === hi, `ends ${O29.specs.join(" / ")}`);
function partsAt(m29, m29r, m5) {
  return Object.fromEntries([["low", lo], ["high", hi]].map(([end, i]) => {
    const sept29 = ev29.cost(m29, specs29[i]), atV5 = ev.cost(m29, specs[i]), withRow8 = ev.cost(m29r, specs[i]), oct05 = ev.cost(m5, specs[i]);
    return [end, { sept29_bn: sept29, responses_bn: atV5 - sept29, row8_bn: withRow8 - atV5, response_move_bn: withRow8 - sept29,
      lineage_bn: oct05 - withRow8, oct05_bn: oct05, change_bn: oct05 - sept29 }];
  }));
}
const PARTS = ["sept29_bn", "responses_bn", "row8_bn", "response_move_bn", "lineage_bn", "oct05_bn", "change_bn"];
const chain = { union: partsAt(union29, V5.withEdits(union29, [L.row8]), union5) };
const rows29 = P.csvRows(`generation_account_2026_09_24/derived/generation_results_${SEPT29[CASE]}.csv`);
let worstStart = Math.max(Math.abs(chain.union.low.sept29_bn - O29.band[0]), Math.abs(chain.union.high.sept29_bn - O29.band[1]));
let worstGen29 = 0, worstEnd = Math.max(Math.abs(chain.union.low.oct05_bn - uCost[lo]), Math.abs(chain.union.high.oct05_bn - uCost[hi])), worstAdd = 0;
for (const conv of CONVS) {
  chain[conv] = {};
  for (const g of GENS) {
    chain[conv][g] = partsAt(models29[conv][g], models29r[conv][g], models5[conv][g]);
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      worstEnd = Math.max(worstEnd, Math.abs(chain[conv][g][end].oct05_bn - res[conv][g].corrected[i]));
      const r29 = rows29.find((r) => r.convention === conv && r.generation === g && r.band_end === end);
      worstGen29 = Math.max(worstGen29, Math.abs(chain[conv][g][end].sept29_bn - Number(r29.cost_bn)));
    }
  }
  for (const end of ["low", "high"]) for (const k of PARTS) {
    worstAdd = Math.max(worstAdd, Math.abs(sum(GENS.map((g) => chain[conv][g][end][k])) - chain.union[end][k]));
  }
}
gate(`the parts start at the September 29 case (the union at ${O29.source}, 1e-4; each generation at generation_results_${SEPT29[CASE]}.csv, `
  + "5.01e-7: half its last printed digit) and end at this case's cost (1e-9)", worstStart < 1e-4 && worstGen29 < 5.01e-7 && worstEnd < 1e-9,
`union ${e(worstStart)}, generations ${e(worstGen29)}, ends ${e(worstEnd)} bn`);
gate("the generations' parts add to the union's, both conventions, both ends", worstAdd < 1e-9, `max |diff| ${e(worstAdd)} bn`);
const LP = V5.lineageParts(L.set);
{
  const ends = ["low", "high"];
  const g = (k) => ends.map((end, j) => [chain.union[end][k], j]);
  const worst = Math.max(...g("response_move_bn").map(([v, j]) => Math.abs(v - LP.union_response_move_bn[j])),
    ...g("lineage_bn").map(([v, j]) => Math.abs(v - LP.g3plus_part_bn[j] - LP.white_part_bn[j])),
    ...g("change_bn").map(([v, j]) => Math.abs(v - LP.change_bn[j])));
  gate(`the union's parts are the lineage lane's (${LP.source}: the response move with row 8; the G3+ and white parts together; the change)`,
    JSON.stringify(LP.ends) === JSON.stringify([lo, hi]) && worst < 1e-9, `max |diff| ${e(worst)} bn`);
  if (L.set === "set") {
    const CF = X.readJson(`${V5.V5_LANE}/derived/summary.json`).change_at_fixed_specifications;
    const w2 = Math.max(...ends.map((end, j) => Math.max(Math.abs(chain.union[end].response_move_bn - CF.union_response_move[j]),
      Math.abs(chain.union[end].lineage_bn - CF.g3plus_members[j] - CF.whites[j]), Math.abs(chain.union[end].change_bn - CF.total[j]))));
    gate(`the union's parts are ${V5.V5_LANE}/derived/summary.json change_at_fixed_specifications`, w2 < 1e-9, `max |diff| ${e(w2)} bn`);
  }
}

// ---------------------------------------------------------------------------------------------------
// The alternative to the designed rule: row 8 all on G3+, as the package's withLineage() puts it on the model it is given.
console.log("[alternative rules]");
const sensitivities = {};
{
  const name = "row8_on_g3plus";
  sensitivities[name] = { rule: V5.ALTERNATIVES[name] };
  let worstAlt = 0;
  for (const conv of CONVS) {
    const lay = V5.layer(L, GENS, TOP, models29[conv], union29, { alt: [name] });
    const m = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], V5.payloadOf(G29.payloads[conv][g], lay.parts[g]))]));
    const r = addsTo(union5, GENS.map((g) => m[g]));
    worstAlt = Math.max(worstAlt, r.cells);
    sensitivities[name][conv] = Object.fromEntries(GENS.map((g) => {
      const c = [ev.cost(m[g], specs[lo]), ev.cost(m[g], specs[hi])];
      return [g, { cost_bn: c, move_bn: [c[0] - res[conv][g].corrected[lo], c[1] - res[conv][g].corrected[hi]] }];
    }));
    const x = sensitivities[name][conv];
    console.log(`  · ${name}: (${conv}) ` + GENS.map((g) => `${g} ${x[g].move_bn.map((v) => (v >= 0 ? "+" : "") + v.toFixed(4)).join(" / ")}`).join("; "));
  }
  gate("the alternative's split adds to the case's payload model cell by cell", worstAlt < 1e-9, `max |diff| ${e(worstAlt)} bn`);
  if (L.set === "set") {
    const A = X.readJson(`${V5.V5_LANE}/derived/api_check.json`);
    const chk = A.patterns.flatMap((p) => p.checks).find((c) => /with the lineage's edits and production on G3\+ \(withLineage\)/.test(c.check));
    const printed = chk && chk.detail.match(/at specifications 48 \/ 11: (.*)$/);
    const got = printed ? Object.fromEntries(printed[1].split("; ").map((s) => { const [g, a, , b] = s.split(" "); return [g, [Number(a), Number(b)]]; })) : null;
    const worst = got ? Math.max(...GENS.map((g) => Math.max(...[0, 1].map((j) => Math.abs(sensitivities[name].a[g].cost_bn[j] - got[g][j]))))) : Infinity;
    gate(`(a) the alternative is ${V5.V5_LANE}/derived/api_check.json pattern 3's split at specifications 48 / 11 (5e-5, four decimals)`,
      lo === 48 && hi === 11 && worst < 5e-5, got ? `max |diff| ${e(worst)} bn` : "pattern 3's print not found");
  }
}

// ---------------------------------------------------------------------------------------------------
// Results.
const VI = load("v4_inputs.json");
const H = VI.headcount;
const lin = L.lineage;
const added = lin.counts.added;
const adultShare = H.a.G3plus.adults / H.a.G3plus.population;
const addedAdults = added * adultShare;
const unionPop = H.union.population + added, unionAdults = H.union.adults + addedAdults;
gate("the headcounts: the union's row-4 count plus the added people is the case's lineage (1e-3 persons; meta.lineage.counts)",
  near(unionPop, lin.counts.lineage_population, 1e-3) && near(H.a.G3plus.population, lin.counts.identified_g3plus, 1e-3),
  `${unionPop.toFixed(1)} = ${H.union.population.toFixed(1)} + ${added.toFixed(1)}`);
const headOf = (conv, g) => ({ population: H[conv][g].population + (g === "G3plus" ? added : 0), adults: H[conv][g].adults + (g === "G3plus" ? addedAdults : 0) });
const perHead = (bn, n) => bn * 1e9 / n;
const pair = (x) => [x.low, x.high];
// Under (b) the added people stay in G3+. Had their minors followed the identified G3+'s, the move to G2 would be about
// the added people's cost times the identified G3+'s fall from (a) to (b) at v5's responses (an indication, not a bound).
const bIndication = Object.fromEntries([["low", lo], ["high", hi]].map(([end, i]) => {
  const ca = ev.cost(models29r.a.G3plus, specs[i]), cb = ev.cost(models29r.b.G3plus, specs[i]);
  const share = (ca - cb) / ca, lineage = chain.b.G3plus[end].lineage_bn;
  return [end, { identified_g3plus_a_bn: ca, identified_g3plus_b_bn: cb, share_moving: share, lineage_bn: lineage, move_to_g2_bn: lineage * share }];
}));
const rows = [];
const summary = {
  case: CASE, set: L.set, lane: V5.V5_LANE, payload: L.rel, builds_on: { payload: L.baseRel, generation_payloads: `generation_account_2026_09_24/derived/generation_corrections_${SEPT29[CASE]}.json` },
  oracle: O, responses: L.payload.meta.responses, low_spec: specs[lo], high_spec: specs[hi],
  specifications: { low: specs[lo], high: specs[hi], low_index: lo, high_index: hi },
  union: { cost_bn: [uCost[lo], uCost[hi]], uncorrected_bn: [u0Cost[lo], u0Cost[hi]], uncorrected_own_ends_bn: [u0Cost[lo0], u0Cost[hi0]],
    population: unionPop, adults: unionAdults, per_member_usd: [perHead(uCost[lo], unionPop), perHead(uCost[hi], unionPop)],
    per_adult_usd: [perHead(uCost[lo], unionAdults), perHead(uCost[hi], unionAdults)] },
  headcount_basis: "row-4 weights (v4_inputs.py headcount), the union's 39,712,493, plus the case's 3,039,720 added people in G3+ (meta.lineage.counts.added) "
    + "under both conventions; their adults at the identified G3+'s adult share (convention a) [ASSUMPTION: the case prices them at the identified G3+'s age mix]",
  lineage: { arm: lin.arm, counting: lin.counting.rule, added, at_g3_rate: lin.counts.at_g3_rate, later_losses: lin.counts.later_losses,
    added_adults: addedAdults, adult_share: adultShare, members: { g3plus: lin.members.g3plus, white: lin.members.white }, c3: lin.c3,
    row8_edit_bn: lin.edits.row8_edit_bn, row8_shares: Object.fromEntries(CONVS.map((c) => [c, layers[c].share])) },
  conventions: {},
};
for (const conv of CONVS) {
  summary.conventions[conv] = {};
  for (const g of GENS) {
    const r = res[conv][g], h = headOf(conv, g), ch = chain[conv][g];
    const at = (i) => r.corrected[i];
    summary.conventions[conv][g] = {
      population: h.population, adults: h.adults,
      cost_bn: [at(lo), at(hi)], own_span_bn: [Math.min(...r.corrected), Math.max(...r.corrected)],
      per_member_usd: [perHead(at(lo), h.population), perHead(at(hi), h.population)],
      per_adult_usd: [perHead(at(lo), h.adults), perHead(at(hi), h.adults)],
      uncorrected_cost_bn: [r.uncorrected[lo], r.uncorrected[hi]], correction_bn: [at(lo) - r.uncorrected[lo], at(hi) - r.uncorrected[hi]],
      sept29_cost_bn: [ch.low.sept29_bn, ch.high.sept29_bn], change_from_sept29_bn: [ch.low.change_bn, ch.high.change_bn],
      response_move_bn: [ch.low.response_move_bn, ch.high.response_move_bn], lineage_bn: [ch.low.lineage_bn, ch.high.lineage_bn],
    };
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      const cr = capRow(r.full[i]);
      rows.push({ convention: conv, generation: g, band_end: end, allocation: specs[i].allocation, cost_bn: at(i),
        uncorrected_same_spec_bn: r.uncorrected[i], correction_bn: at(i) - r.uncorrected[i], population: h.population, adults: h.adults,
        per_member_usd: perHead(at(i), h.population), per_adult_usd: perHead(at(i), h.adults), capital_return_bn: cr.capital_total_bn,
        enterprise_surplus_receipt_bn: cr.enterprise_surplus_receipt_bn, housing_enterprise_surplus_receipt_bn: cr.housing_enterprise_surplus_receipt_bn,
        sept29_cost_bn: ch[end].sept29_bn, change_from_sept29_bn: ch[end].change_bn, response_move_bn: ch[end].response_move_bn,
        lineage_bn: ch[end].lineage_bn });
    }
  }
}
summary.change_from_sept29_by_part = Object.assign({ parts: PARTS, specifications: { low: lo, high: hi },
  rule: "at the end specifications, which are the September 29 case's: sept29_bn is the September 29 model at the September 29 "
    + "specification; responses_bn the same model at v5's (the group-size responses move); row8_bn its share of audit row 8's change; "
    + "response_move_bn their sum (the union's response move); lineage_bn the added people (G3+ only); oct05_bn = sept29_bn + "
    + "response_move_bn + lineage_bn; change_bn = oct05_bn - sept29_bn" }, chain);
summary.rules = {
  lineage: "the added people (meta.lineage: m_G identified-G3+ members and m_W third-plus whites at G3+ ages, every engine cell, and the "
    + "production grid's change) go on G3+ under both conventions, as the case's package.cjs withLineage() adds them",
  row8: "audit row 8's change at the larger group (the lineage's last edit, the union's response move) times each generation's share of "
    + "the September 29 union's lane_constants k cell, per allocation (main_case_lineage_2026_10_05 lineage_case.cjs generationCosts)",
  responses: "every generation at the case's responses (the payload's meta.responses), which move with the group's size",
  convention_b: "[ASSUMPTION] the added people stay in G3+ under (b): their parents' generation is not observed. b_rule_indication "
    + "gives the move had their minors followed the identified G3+'s",
};
summary.b_rule_indication = Object.assign({ rule: "the added people's cost (lineage_bn) times the identified G3+'s fall from (a) to (b) at v5's "
  + "responses ((a - b) / a, the share of its cost that (b) sends to G2 with the minors of second-generation parents): an indication of "
  + "the move from G3+ to G2 under (b), not a bound; the union is unchanged" }, bIndication);
summary.alternatives = V5.ALTERNATIVES;
summary.sensitivities = sensitivities;
summary.gates = { failed: fails.slice() };

if (fails.length) {
  console.log(`✗ ${fails.length} gate(s) failed, nothing written: ${fails.join("; ")}`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
const header = Object.keys(rows[0]);
fs.writeFileSync(path.join(OUT, `generation_results_${CASE}.csv`),
  [header.join(","), ...rows.map((r) => header.map((k) => (typeof r[k] === "number" ? r[k].toFixed(6) : r[k])).join(","))].join("\n") + "\n");
fs.writeFileSync(path.join(OUT, `generation_summary_${CASE}.json`), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, `generation_corrections_${CASE}.json`), JSON.stringify({
  meta: { source: "generation_account_2026_09_24/run_generations_v5.cjs", case: CASE, case_lane: V5.V5_LANE, union: L.rel,
    builds_on: summary.builds_on.generation_payloads,
    layout: "convention -> generation -> engine corrections payload (receipt_lines, lines, edits, production); each is the generation's "
      + "September 29 payload (generation_corrections_sept29*.json), then its v5 part: on G3+ the lineage's cell edits (the added people) "
      + "and the production grid's change; on every generation audit row 8's change times its lane_constants k share. Apply with the "
      + "union's meta (responses, capital_return). The three models add to the union's payload model cell by cell" },
  payloads }) + "\n");

console.log(`[results] net cost to other residents at the case's ends ($bn a year; low = ${specs[lo].allocation}, high = ${specs[hi].allocation})`);
console.log(`  union ${f2(summary.union.cost_bn)}; per member $${summary.union.per_member_usd.map((x) => Math.round(x)).join("–$")} (${(unionPop / 1e6).toFixed(2)}M)`);
for (const conv of CONVS) {
  console.log(`  convention (${conv})`);
  for (const g of GENS) {
    const c = summary.conventions[conv][g];
    console.log(`    ${g.padEnd(7)} ${f2(c.cost_bn)}  (September 29 ${f2(c.sept29_cost_bn)}; response move ${c.response_move_bn.map(sgn).join(" / ")}, `
      + `lineage ${c.lineage_bn.map(sgn).join(" / ")}); per member $${c.per_member_usd.map((x) => Math.round(x)).join("–$")} (${(c.population / 1e6).toFixed(2)}M), `
      + `per adult $${c.per_adult_usd.map((x) => Math.round(x)).join("–$")}`);
  }
}
console.log(`  (b) indication, the added minors with the identified G3+'s move: ${["low", "high"].map((k) => sgn(bIndication[k].move_to_g2_bn)).join(" / ")} bn from G3+ to G2`);
console.log("  ✓ all generation-run gates passed");
