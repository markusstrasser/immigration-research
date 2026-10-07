/* Step 9: main case v6 (main_case_2026_10_07, case key oct07: main case v5 plus an item registry) by generation.
 *
 * --case picks the set:
 *   oct07       the case (main_case_bands.csv adopted; ends 48 / 11);
 *   oct07_cash  the cash set beside it: the pension switch off, so item pension_tr2026 does not enter it.
 * The case is the September 29 payload of the same set plus the lineage block (the lineage item's 336 edits and grid in
 * v5's cells and order) and the edit sets' edits after it (meta.items), so each generation's payload is its September 29
 * payload (derived/generation_corrections_sept29*.json) plus its v6 part (v6_split.cjs):
 *   - G3+ takes the lineage's cell edits and the production grid's change (the added people, priced at their measured
 *     age mix: item added_age_mix), and every generation row 8's edit times its lane_constants k share, as under v5;
 *   - the edit sets by v6_split.cjs RULES: national-scale edits as they are on every generation; pension_tr2026's
 *     lineage parts on G3+ and its union parts by the September 29 split's pension rule with the 2026 per-generation
 *     ratios (the pension lane's arms.csv);
 *   - every generation is evaluated at the case's responses (v5's: no item moves them).
 * Per-member figures add the added people to G3+ as under v5; their adults now follow the case's measured age mix
 * (v6_split.cjs addedAdults) [APPROX]. The change from v5 (generation_results_oct05*.csv) is taken in the payload's order:
 * the lineage item, then each edit set; the parts telescope to the change.
 *
 * Gates (exit 1, nothing written):
 *   - the September 29 generation payloads split the case's base payload (models 1e-9, grids 1e-12);
 *   - the row-8 shares add to 1 (1e-12); the item base split: G3+'s model is the package's withLineage() of its September
 *     29 model with row 8 at its share, the others their September 29 models with their share (1e-12), and the three add
 *     to the item base's payload model (ITEM_BASE, 1e-9; grid 1e-12);
 *   - every edit set: each cell shift's shares add to 1 and its amounts to the union's edit (1e-12); before each
 *     national-scale edit every generation model carries the union's national total of the line (exact);
 *   - the pension rule (the set): the September 29 split's rule reproduces each generation's social_security and Part A
 *     accrual on its September 29 models (1e-9), and the generations' changes add to the item's union parts (1e-9);
 *   - the three v6 models add to the case's payload model (1e-9; grid 1e-12);
 *   - the consumer's 64 specifications are the v6 package's; the union reproduces the case's band at its ends
 *     (main_case_bands.csv, 1e-4), its cost at every specification (per_spec.csv, the set, 1e-9) and the uncorrected
 *     model at the case's responses (1e-4); the generations add to the union in all 64 specifications, corrected and
 *     uncorrected (1e-9), and so do their capital returns and enterprise receipts; the v6 package's evaluateFull gives
 *     every model's cost here (1e-9);
 *   - the generations add to the case's full-precision band at 48 / 11 (summary.json, 1e-6);
 *   - the change from v5 by part: each generation starts at its v5 cost (generation_corrections_oct05*.json on the same
 *     models, at generation_results_oct05*.csv, 5.01e-7; v5's evaluator agrees, 1e-9) and ends at its v6 cost (1e-9); the
 *     union starts at v5's band and its parts are the case lane's (each item alone on v5 plus its interactions with the
 *     items before it, the remainder on the last; 1e-9); the generations add to the union part by part (1e-9); the
 *     lineage item moves G3+ only (G1 and G2 exactly 0);
 *   - the alternatives' splits add to the union (1e-9; split_basis_edited_line, each part on a model line split by that line
 *     rather than its split_basis, runs when a part's basis is another model line: Pell's all_cash shares); for the set
 *     under (a), row 8 on G3+ with the pension union parts
 *     by receipt shares is main_case_2026_10_07 api_check.json pattern 3's by-generation print (5e-5, its four decimals).
 * Writes generation_results_<case>.csv, generation_summary_<case>.json and generation_corrections_<case>.json. Run from
 * the repository root:
 *   node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v6.cjs [--case oct07|oct07_cash] [--out-dir DIR]
 */
"use strict";
const fs = require("fs");
const path = require("path");
const V6 = require(path.join(__dirname, "v6_split.cjs"));
const { X, V5, P6 } = V6;
const { P, Engine, MODEL, ALLOCS, byAlloc, sum } = X;

const HERE = __dirname;
const argv = process.argv.slice(2);
const arg = (name, dflt) => { const i = argv.indexOf(name); return i < 0 ? dflt : argv[i + 1]; };
const CASES = { oct07: "set", oct07_cash: "cash" };
const SEPT29 = { oct07: "sept29", oct07_cash: "sept29_cash" };
const OCT05 = { oct07: "oct05", oct07_cash: "oct05_cash" };
const CASE = arg("--case", "oct07");
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
const clone = (x) => JSON.parse(JSON.stringify(x));
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
const withEdits = (m, edits) => (edits.length ? Engine.applyCorrections(m, { lines: [], edits, meta: m.corrections }) : m);
const nationalOf = (m, side, id) => (side === "receipt" ? m.receipts : m.spending).lines.find((l) => l.id === id).national_bn;

const L = V6.loadCase(CASES[CASE]);
console.log(`[case ${CASE}] ${L.rel}: ${L.baseRel} plus ${L.lineage.edits.count} lineage edits (item ${L.lineageItem}) and `
  + `${L.items.map((it) => `${it.edits.length} of item ${it.id}`).join(", ") || "no edit set"}; outputs to ${path.relative(process.cwd(), OUT) || "."}`);

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
// The set's pension rule is checked on the generations' Part A accrual, which needs the cash set's September 29 models.
const G29c = L.set === "set" ? load("generation_corrections_sept29_cash.json") : null;
const models29c = G29c ? Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[c][g], G29c.payloads[c][g])]))])) : null;

// ---------------------------------------------------------------------------------------------------
console.log("[the v6 part: the lineage block on G3+ and row 8 by share, then the edit sets by rule]");
const layers = {}, payloads = {}, modelsL = {}, models6 = {}, models29r = {};
const unionL = (L.set === "set" ? P6.ITEM_BASE : P6.ITEM_BASE.CASH).payloadModel();
const union6 = Engine.applyCorrections(MODEL, L.payload);
for (const conv of CONVS) {
  const lay = V6.layer(L, GENS, TOP, models29[conv], union29);
  layers[conv] = lay;
  gate(`(${conv}) the row-8 shares add to 1 in both allocations`, lay.share_sum_error < 1e-12,
    `${e(lay.share_sum_error)}; ` + GENS.map((g) => `${g} ${lay.share[g].personal.toFixed(4)}/${lay.share[g].shared.toFixed(4)}`).join(", "));
  payloads[conv] = Object.fromEntries(GENS.map((g) => [g, V6.payloadOf(G29.payloads[conv][g], lay.parts[g])]));
  modelsL[conv] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g],
    V6.payloadOf(G29.payloads[conv][g], { edits: lay.parts[g].lineage_edits, production: lay.parts[g].production }))]));
  models6[conv] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], payloads[conv][g])]));
  models29r[conv] = Object.fromEntries(GENS.map((g) => [g, V5.withEdits(models29[conv][g], [lay.parts[g].row8])]));
  // The item base split against the package's: G3+ is withLineage() (the lineage item's edits) of its September 29 model
  // with row 8 moved from the whole edit to its share; the others are their September 29 models with their row-8 share.
  let worst = 0;
  for (const g of GENS) {
    const want = g === lay.g3plus
      ? V5.withEdits(L.api.withLineage(models29[conv][g]), [Object.assign({}, V5.ROW8, { by: byAlloc((a) => L.row8.by[a] * (lay.share[g][a] - 1)) })])
      : models29r[conv][g];
    worst = Math.max(worst, sameModel(modelsL[conv][g], want));
  }
  gate(`(${conv}) each generation's item-base payload gives its September 29 model with its part; G3+'s is the package's withLineage() with row 8 at its share`,
    worst < 1e-12, `max |diff| ${e(worst)} bn`);
  const rL = addsTo(unionL, GENS.map((g) => modelsL[conv][g]));
  gate(`(${conv}) the three item-base models add to the item base's payload model (ITEM_BASE: v5 with item ${L.lineageItem})`,
    rL.cells < 1e-9 && rL.grid < 1e-12, `${rL.n} cells, max |diff| ${e(rL.cells)} bn; grid ${e(rL.grid)} bn`);
  // The edit sets: shares and amounts, and the national totals each national-scale edit scales from.
  let shareErr = 0, amountErr = 0, finite = true, natGap = 0, nNat = 0;
  for (const it of lay.items) for (const x of it.edits) {
    if (!x.parts) continue;
    const want = L.items.find((y) => y.id === it.id).edits[x.edit].by;
    for (const a of ALLOCS) {
      for (const p of x.parts) {
        shareErr = Math.max(shareErr, Math.abs(sum(GENS.map((g) => p.share[g][a])) - 1));
        finite = finite && GENS.every((g) => Number.isFinite(p.share[g][a]));
      }
      amountErr = Math.max(amountErr, Math.abs(sum(x.parts.flatMap((p) => GENS.map((g) => p.bn[g][a]))) - want[a]));
    }
  }
  {
    let mU = unionL, mG = Object.fromEntries(GENS.map((g) => [g, modelsL[conv][g]]));
    let k = 0;
    for (const it of L.items) {
      // An item's carriers enter with its edits.
      mU = V6.withStep(mU, [], it.receipt_lines);
      for (const g of GENS) mG[g] = V6.withStep(mG[g], [], lay.parts[g].item_receipt_lines[it.id]);
      for (const ed of it.edits) {
        if (ed.national_bn !== undefined) {
          nNat += 1;
          for (const g of GENS) natGap = Math.max(natGap, Math.abs(nationalOf(mG[g], ed.side, ed.line) - nationalOf(mU, ed.side, ed.line)));
        }
        mU = withEdits(mU, [ed]);
        for (const g of GENS) mG[g] = withEdits(mG[g], [lay.parts[g].item_edits[k]]);
        k += 1;
      }
    }
    for (const g of GENS) amountErr = Math.max(amountErr, sameModel(mG[g], models6[conv][g]));
    amountErr = Math.max(amountErr, sameModel(mU, union6));
  }
  gate(`(${conv}) the edit sets by rule: each cell shift's shares add to 1 and its parts' amounts to the union's edit; applied one by one they give the v6 models`,
    finite && shareErr < 1e-12 && amountErr < 1e-12, `shares ${e(shareErr)}; amounts and models ${e(amountErr)} bn`);
  {
    // The carriers' amounts are a dollar's fractions, below the cell gates' tolerance: their shares are checked relative.
    const cs = lay.items.flatMap((it) => it.carriers || []);
    let sh = 0, val = 0;
    for (const c of cs) for (const a of ALLOCS) {
      sh = Math.max(sh, Math.abs(sum(GENS.map((g) => c.share[g][a])) - 1));
      val = Math.max(val, Math.abs(sum(GENS.map((g) => c.value[g][a])) - c.union_value[a]) / Math.max(Math.abs(c.union_value[a]), 1e-300));
    }
    if (cs.length) {
      gate(`(${conv}) the items' carriers by their parent lines: shares add to 1 and the models' key values to the union's (1e-12 relative)`,
        sh < 1e-12 && val < 1e-12, `${cs.map((c) => `${c.id} by ${c.parent}`).join(", ")}; shares ${e(sh)}, values ${e(val)}`);
    }
  }
  gate(`(${conv}) before each national-scale edit every generation model carries the union's national total of its line (exact)`,
    natGap === 0, `${nNat} edits, max |diff| ${natGap}`);
  if (lay.pension) {
    const S = lay.pension, PI = S.inputs, PA = L.payload.meta.pension_accrual;
    let ss = 0, pa = 0, dss = 0, dpa = 0;
    const it = L.items.find((y) => y.record.parts && y.record.parts.union_oasdi);
    const parts = it.record.parts;
    for (const a of ALLOCS) {
      for (const g of GENS) {
        const l29 = X.lineOf(models29[conv][g], "spending", "social_security"), m29 = X.lineOf(models29[conv][g], "spending", "medicare");
        const mc29 = X.lineOf(models29c[conv][g], "spending", "medicare");
        ss = Math.max(ss, Math.abs(S.ss_old[g][a] - l29.keys[l29.preferred_key][a].target_bn));
        pa = Math.max(pa, Math.abs(S.part_a_old[g][a] - (m29.keys[m29.preferred_key][a].target_bn - (1 - PA.part_a_share) * mc29.keys[mc29.preferred_key][a].target_bn)));
      }
      dss = Math.max(dss, Math.abs(sum(GENS.map((g) => S.ss_new[g][a] - S.ss_old[g][a])) - parts.union_oasdi.by[a]));
      dpa = Math.max(dpa, Math.abs(sum(GENS.map((g) => S.part_a_new[g][a] - S.part_a_old[g][a])) - parts.union_part_a.by[a]));
    }
    gate(`(${conv}) the September 29 split's pension rule reproduces each generation's social_security and Part A accrual on its September 29 models (1e-9)`,
      ss < 1e-9 && pa < 1e-9, `social_security ${e(ss)} bn, Part A ${e(pa)} bn`);
    gate(`(${conv}) with the 2026 ratios (${PI.file}, arm ${PI.arm}: G1 ×${PI.f_net.G1.toFixed(5)}, G2 ×${PI.f_net.G2.toFixed(5)}, G3+ ×${PI.f_net.G3plus.toFixed(5)}) the generations' changes add to the item's union parts (1e-9)`,
      dss < 1e-9 && dpa < 1e-9, `OASDI ${e(dss)} bn, Part A ${e(dpa)} bn`);
  }
}
for (const conv of CONVS) {
  const r = addsTo(union6, GENS.map((g) => models6[conv][g]));
  gate(`(${conv}) the three v6 models add to the case's payload model: every cell and the production grid`,
    r.cells < 1e-9 && r.grid < 1e-12, `${r.n} cells, max |diff| ${e(r.cells)} bn; grid ${e(r.grid)} bn`);
}

// ---------------------------------------------------------------------------------------------------
console.log("[engine]");
const ev = V6.evaluator(L.payload, L.api);
const specs = ev.specs;
const AP = V6.adoptedPackage(L);
const SPEC_FIELDS = ["allocation", "normalization", "share", "school", "reading", "gg", "uc"];
gate(`the consumer's 64 specifications are ${AP.source}'s, in order (allocation, normalization, school share and response, reading and general government, uninsured key)`,
  specs.length === 64 && AP.specs.length === specs.length && specs.every((s, i) => SPEC_FIELDS.every((k) => s[k] === AP.specs[i][k])));
const uFull = specs.map((s) => ev.evaluateFull(union6, s));
const uCost = uFull.map((r) => r.cost_bn);
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
const O = V6.oracle(L.set);
gate(`the corrected union reproduces the case's band at its end specifications (${O.source}, four decimals)`,
  lo === O.specs[0] && hi === O.specs[1] && near(uCost[lo], O.band[0], 1e-4) && near(uCost[hi], O.band[1], 1e-4),
  `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)} at ${lo} / ${hi}`);
const PS = V6.perSpec(L.set);
if (PS) {
  let worst = 0;
  for (const [i, c] of PS.cost) worst = Math.max(worst, Math.abs(uCost[i] - c));
  gate(`the corrected union reproduces ${PS.source} at each of its specifications (mean of the two methods)`,
    PS.cost.size === 64 && worst < 1e-9, `${PS.cost.size} specifications; max |diff| ${e(worst)} bn`);
} else console.log(`  · ${V6.V6_LANE} publishes no per-specification cost for the ${L.set} set`);
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
    const full = specs.map((s) => ev.evaluateFull(models6[conv][g], s));
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
  const band = [lo, hi].map((i) => sum(GENS.map((g) => res[conv][g].corrected[i])));
  gate(`(${conv}) the generations add to the case's band at specifications ${lo} / ${hi} (${O.full.source}, 1e-6)`,
    lo === O.specs[0] && hi === O.specs[1] && near(band[0], O.full.band[0], 1e-6) && near(band[1], O.full.band[1], 1e-6),
    `${band.map((x) => x.toFixed(6)).join(" / ")} against ${O.full.band.map((x) => x.toFixed(6)).join(" / ")}`);
}
{
  let worst = 0;
  specs.forEach((_, i) => {
    worst = Math.max(worst, Math.abs(AP.cost(union6, i) - uCost[i]), Math.abs(AP.cost(MODEL, i) - u0Cost[i]));
    for (const conv of CONVS) for (const g of GENS) {
      worst = Math.max(worst, Math.abs(AP.cost(models6[conv][g], i) - res[conv][g].corrected[i]),
        Math.abs(AP.cost(models0[conv][g], i) - res[conv][g].uncorrected[i]));
    }
  });
  gate(`${AP.source} evaluateFull gives every model's cost here (union and generations, corrected and uncorrected, all specifications)`,
    worst < 1e-9, `max |diff| ${e(worst)} bn`);
}

// ---------------------------------------------------------------------------------------------------
// The change from v5 by part, at the case's end specifications (v5's too): each model at its v5 payload; then the item
// base (the lineage item: the added people re-valued on G3+); then each edit set in the payload's order. The parts
// telescope to the v6 cost.
console.log("[change from v5 (oct05), by item]");
const CP = V6.caseParts(L.set);
const G05 = load(`generation_corrections_${OCT05[CASE]}.json`);
const V5_REL = V5.V5_FILES[L.set];
gate(`generation_corrections_${OCT05[CASE]}.json is v5's split of ${V5_REL}, on the same models`,
  G05.meta.case === OCT05[CASE] && G05.meta.union === V5_REL && G05.meta.builds_on === `generation_account_2026_09_24/derived/generation_corrections_${SEPT29[CASE]}.json`,
  `${G05.meta.union}; builds on ${G05.meta.builds_on}`);
const v5Payload = X.readJson(V5_REL);
const union5 = Engine.applyCorrections(MODEL, v5Payload);
const ev5 = X.evaluator(v5Payload);
const models5 = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[c][g], G05.payloads[c][g])]))]));
for (const conv of CONVS) {
  const r = addsTo(union5, GENS.map((g) => models5[conv][g]));
  gate(`(${conv}) v5's generation models add to v5's payload model`, r.cells < 1e-9 && r.grid < 1e-12, `max |diff| ${e(r.cells)} bn; grid ${e(r.grid)} bn`);
}
gate(`v5's ends are this case's (${CP.source.split(" ")[0]})`, ev5.specs.length === specs.length
  && ev5.specs.every((s, i) => SPEC_FIELDS.every((k) => s[k] === specs[i][k])), "the same 64 specifications");
const STEPS = [L.lineageItem].concat(L.items.map((it) => it.id));
const ALL_ITEMS = L.records.map((r) => r.id);
// Each step's models: the lineage item's are the item-base models; each edit set adds its edits on every model.
const stepModels = Object.fromEntries(CONVS.map((conv) => {
  const seq = [Object.fromEntries(GENS.map((g) => [g, modelsL[conv][g]]))];
  let k = 0;
  for (const it of L.items) {
    const prev = seq[seq.length - 1];
    const n = it.edits.length, part = (g) => layers[conv].parts[g];
    seq.push(Object.fromEntries(GENS.map((g) => [g, V6.withStep(prev[g], part(g).item_edits.slice(k, k + n), part(g).item_receipt_lines[it.id])])));
    k += n;
  }
  return [conv, seq];
}));
const unionSeq = [unionL];
for (const it of L.items) unionSeq.push(V6.withStep(unionSeq[unionSeq.length - 1], it.edits, it.receipt_lines));
const chain = {};
function chainOf(m5, seq) {
  return Object.fromEntries([["low", lo], ["high", hi]].map(([end, i]) => {
    const c = [ev.cost(m5, specs[i])].concat(seq.map((m) => ev.cost(m, specs[i])));
    const out = { oct05_bn: c[0] };
    STEPS.forEach((id, j) => { out[`${id}_bn`] = c[j + 1] - c[j]; });
    out.oct07_bn = c[c.length - 1];
    out.change_bn = c[c.length - 1] - c[0];
    return [end, out];
  }));
}
chain.union = chainOf(union5, unionSeq);
const PARTS = ["oct05_bn"].concat(STEPS.map((id) => `${id}_bn`), ["oct07_bn", "change_bn"]);
const rows05 = P.csvRows(`generation_account_2026_09_24/derived/generation_results_${OCT05[CASE]}.csv`);
let worstStart = Math.max(Math.abs(chain.union.low.oct05_bn - CP.v5[0]), Math.abs(chain.union.high.oct05_bn - CP.v5[1]));
let worstGen05 = 0, worstEv5 = 0, worstAdd = 0, worstOthers = 0;
let worstEnd = Math.max(Math.abs(chain.union.low.oct07_bn - uCost[lo]), Math.abs(chain.union.high.oct07_bn - uCost[hi]), sameModel(unionSeq[unionSeq.length - 1], union6));
for (const conv of CONVS) {
  chain[conv] = {};
  for (const g of GENS) {
    const seq = stepModels[conv].map((s) => s[g]);
    chain[conv][g] = chainOf(models5[conv][g], seq);
    worstEnd = Math.max(worstEnd, sameModel(seq[seq.length - 1], models6[conv][g]));
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      worstEnd = Math.max(worstEnd, Math.abs(chain[conv][g][end].oct07_bn - res[conv][g].corrected[i]));
      const r05 = rows05.find((r) => r.convention === conv && r.generation === g && r.band_end === end);
      worstGen05 = Math.max(worstGen05, Math.abs(chain[conv][g][end].oct05_bn - Number(r05.cost_bn)));
      worstEv5 = Math.max(worstEv5, Math.abs(chain[conv][g][end].oct05_bn - ev5.cost(models5[conv][g], specs[i])));
      if (g !== "G3plus") worstOthers = Math.max(worstOthers, Math.abs(chain[conv][g][end][`${L.lineageItem}_bn`]));
    }
  }
  for (const end of ["low", "high"]) for (const k of PARTS) {
    worstAdd = Math.max(worstAdd, Math.abs(sum(GENS.map((g) => chain[conv][g][end][k])) - chain.union[end][k]));
  }
}
gate(`the parts start at v5 (the union at ${CP.source.split(" ")[0]} adopted_2026_10_05 or the v5 cash set, 1e-9; each generation at `
  + `generation_results_${OCT05[CASE]}.csv, 5.01e-7, and at v5's evaluator, 1e-9) and end at this case's models and cost (1e-9)`,
  worstStart < 1e-9 && worstGen05 < 5.01e-7 && worstEv5 < 1e-9 && worstEnd < 1e-9,
  `union ${e(worstStart)}, generations ${e(worstGen05)} (v5 evaluator ${e(worstEv5)}), ends ${e(worstEnd)} bn`);
gate("the generations' parts add to the union's, both conventions, both ends", worstAdd < 1e-9, `max |diff| ${e(worstAdd)} bn`);
gate(`the lineage item (${L.lineageItem}) moves G3+ only: G1's and G2's parts are 0`, worstOthers === 0, `max |part| ${worstOthers}`);
{
  // Each step against the case lane: the item alone on v5 plus its interactions with the items before it in this order;
  // the remainder (no three-way term on v5's case) goes with the last step.
  let worst = 0;
  const missing = [];
  STEPS.forEach((id, j) => {
    const alone = CP.alone[id];
    if (!alone) { missing.push(`${id} alone`); return; }
    const want = [0, 1].map((k) => alone[k]);
    for (const prev of STEPS.slice(0, j)) {
      const x = CP.pair(prev, id);
      if (!x) { missing.push(`${prev} x ${id}`); continue; }
      for (const k of [0, 1]) want[k] += x[k];
    }
    if (j === STEPS.length - 1) {
      if (!CP.remainder) missing.push("remainder"); else for (const k of [0, 1]) want[k] += CP.remainder[k];
    }
    for (const [k, end] of [[0, "low"], [1, "high"]]) worst = Math.max(worst, Math.abs(chain.union[end][`${id}_bn`] - want[k]));
  });
  const ch = [chain.union.low.change_bn, chain.union.high.change_bn];
  worst = Math.max(worst, ...[0, 1].map((k) => Math.abs(ch[k] - CP.change[k])));
  gate(`the union's parts are the case lane's (${CP.source}: each item alone on v5 plus its interactions with the steps before it)`,
    !missing.length && worst < 1e-9, missing.length ? `missing ${missing.join(", ")}` : `max |diff| ${e(worst)} bn`);
  const LP = CP.lineage_item_parts;
  const lin = [chain.union.low[`${L.lineageItem}_bn`], chain.union.high[`${L.lineageItem}_bn`]];
  const w2 = Math.max(...[0, 1].map((k) => Math.abs(lin[k] - LP.g3plus_members[k] - LP.whites[k])), ...[0, 1].map((k) => Math.abs(lin[k] - LP.g3_rate[k] - LP.later[k])));
  gate(`the lineage item's step is the case lane's v6.lineage_item_parts (G3+ members and whites; G3-rate persons and later losses)`, w2 < 1e-9, `max |diff| ${e(w2)} bn`);
}

// ---------------------------------------------------------------------------------------------------
// The added people's cost on G3+ in v6: G3+'s model less the same model without the lineage block's cell edits and
// grid, with the items' parts but their lineage parts (and the national-scale edits on the identified cells only).
console.log("[the added people]");
function withoutLineage(conv) {
  const lay = layers[conv], g = lay.g3plus;
  const edits = [];
  let k = 0;
  for (const it of lay.items) for (const x of it.edits) {
    const ed = lay.parts[g].item_edits[k];
    k += 1;
    if (!x.parts) { edits.push(ed); continue; }
    const by = byAlloc((a) => sum(x.parts.filter((p) => p.rule !== "lineage").map((p) => p.bn[g][a])));
    edits.push(Object.assign({}, ed, { by }));
  }
  // The carriers by parent line are the identified G3+'s: no item's carrier has a part on the added people.
  return V6.withStep(models29r[conv][g], edits, lay.parts[g].receipt_lines);
}
const added = {};
for (const conv of CONVS) {
  const g = layers[conv].g3plus, m = withoutLineage(conv);
  added[conv] = Object.fromEntries([["low", lo], ["high", hi]].map(([end, i]) => [end, { identified_g3plus_bn: ev.cost(m, specs[i]),
    added_people_bn: res[conv][g].corrected[i] - ev.cost(m, specs[i]) }]));
}
console.log(`  · (a) the added people cost ${["low", "high"].map((k) => added.a[k].added_people_bn.toFixed(2)).join(" / ")} bn; the identified G3+ `
  + `${["low", "high"].map((k) => added.a[k].identified_g3plus_bn.toFixed(2)).join(" / ")} bn`);

// ---------------------------------------------------------------------------------------------------
// The alternatives to the designed rules: row 8 all on G3+ (as under v5), the pension union parts by receipt shares, and
// the parts split by their edited line instead of their split_basis.
console.log("[alternative rules]");
const sensitivities = {};
const runAlt = (names) => {
  const out = { rules: names.map((n) => V6.ALTERNATIVES[n]) };
  let worstAlt = 0;
  for (const conv of CONVS) {
    const lay = V6.layer(L, GENS, TOP, models29[conv], union29, { alt: names });
    const m = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], V6.payloadOf(G29.payloads[conv][g], lay.parts[g]))]));
    worstAlt = Math.max(worstAlt, addsTo(union6, GENS.map((g) => m[g])).cells);
    out[conv] = Object.fromEntries(GENS.map((g) => {
      const c = [ev.cost(m[g], specs[lo]), ev.cost(m[g], specs[hi])];
      return [g, { cost_bn: c, move_bn: [c[0] - res[conv][g].corrected[lo], c[1] - res[conv][g].corrected[hi]] }];
    }));
    console.log(`  · ${names.join(" + ")}: (${conv}) ` + GENS.map((g) => `${g} ${out[conv][g].move_bn.map((v) => (v >= 0 ? "+" : "") + v.toFixed(4)).join(" / ")}`).join("; "));
  }
  return { out, worstAlt };
};
// v6: a part split by its meta's split_basis on another line than it edits (user_fees's Pell) gets the edited line beside it.
const basisMoved = layers.a.items.some((x) => x.edits.some((y) => (y.parts || []).some((q) => q.rule === "parent_line" && q.parent !== y.line
  && !(L.payload.lines || []).some((l) => l.id === y.line))));
const ALT_RUNS = [["row8_on_g3plus"]].concat(layers.a.pension ? [["pension_receipt_shares"], ["row8_on_g3plus", "pension_receipt_shares"]] : [],
  basisMoved ? [["split_basis_edited_line"]] : []);
let worstAlts = 0;
for (const names of ALT_RUNS) {
  const r = runAlt(names);
  sensitivities[names.join("+")] = r.out;
  worstAlts = Math.max(worstAlts, r.worstAlt);
}
gate("each alternative's split adds to the case's payload model cell by cell", worstAlts < 1e-9, `max |diff| ${e(worstAlts)} bn`);
if (L.set === "set") {
  const A = X.readJson(`${V6.V6_LANE}/derived/api_check.json`);
  const chk = A.patterns.flatMap((p) => p.checks).find((c) => /with the edit sets' edits by the rule/.test(c.check));
  const printed = chk && chk.detail.match(/at specifications 48 \/ 11: (.*)$/);
  const got = printed ? Object.fromEntries(printed[1].split("; ").map((s) => { const [g, a, , b] = s.split(" "); return [g, [Number(a), Number(b)]]; })) : null;
  const both = sensitivities["row8_on_g3plus+pension_receipt_shares"];
  const worst = got && both ? Math.max(...GENS.map((g) => Math.max(...[0, 1].map((j) => Math.abs(both.a[g].cost_bn[j] - got[g][j]))))) : Infinity;
  gate(`(a) row 8 on G3+ with the pension union parts by receipt shares is ${V6.V6_LANE}/derived/api_check.json pattern 3's split at specifications 48 / 11 (5e-5, four decimals)`,
    lo === 48 && hi === 11 && worst < 5e-5, got ? `max |diff| ${e(worst)} bn` : "pattern 3's print not found");
}

// ---------------------------------------------------------------------------------------------------
// Results.
const VI = load("v4_inputs.json");
const H = VI.headcount;
const lin = L.lineage;
const nAdded = lin.counts.added;
const AA = V6.addedAdults(lin, H.a.G3plus.adults / H.a.G3plus.population);
const unionPop = H.union.population + nAdded, unionAdults = H.union.adults + AA.adults;
gate("the headcounts: the union's row-4 count plus the added people is the case's lineage (1e-3 persons; meta.lineage.counts)",
  near(unionPop, lin.counts.lineage_population, 1e-3) && near(H.a.G3plus.population, lin.counts.identified_g3plus, 1e-3),
  `${unionPop.toFixed(1)} = ${H.union.population.toFixed(1)} + ${nAdded.toFixed(1)}`);
console.log(`  · the added people's adults at their measured age mix: ${Math.round(AA.adults).toLocaleString("en-US")} (share ${AA.adult_share.toFixed(4)}; `
  + `theta ${AA.theta.toFixed(4)}), against ${Math.round(AA.v5_rule_adults).toLocaleString("en-US")} at the identified G3+'s share (v5's rule)`);
const headOf = (conv, g) => ({ population: H[conv][g].population + (g === "G3plus" ? nAdded : 0), adults: H[conv][g].adults + (g === "G3plus" ? AA.adults : 0) });
const perHead = (bn, n) => bn * 1e9 / n;
// Under (b) the added people stay in G3+. Had their minors followed the identified G3+'s, the move to G2 would be about
// the added people's cost times the identified G3+'s fall from (a) to (b) (an indication, not a bound).
const bIndication = Object.fromEntries([["low", lo], ["high", hi]].map(([end, i]) => {
  const ca = ev.cost(withoutLineage("a"), specs[i]), cb = ev.cost(withoutLineage("b"), specs[i]);
  const share = (ca - cb) / ca, cost = added.b[end].added_people_bn;
  return [end, { identified_g3plus_a_bn: ca, identified_g3plus_b_bn: cb, share_moving: share, added_people_bn: cost, move_to_g2_bn: cost * share }];
}));
const rows = [];
const summary = {
  case: CASE, set: L.set, lane: V6.V6_LANE, payload: L.rel, status: L.payload.meta.status, adopted: L.payload.meta.adopted,
  builds_on: { payload: L.baseRel, generation_payloads: `generation_account_2026_09_24/derived/generation_corrections_${SEPT29[CASE]}.json`,
    v5_generation_payloads: `generation_account_2026_09_24/derived/generation_corrections_${OCT05[CASE]}.json` },
  oracle: O, responses: L.payload.meta.responses, low_spec: specs[lo], high_spec: specs[hi],
  specifications: { low: specs[lo], high: specs[hi], low_index: lo, high_index: hi },
  union: { cost_bn: [uCost[lo], uCost[hi]], uncorrected_bn: [u0Cost[lo], u0Cost[hi]], uncorrected_own_ends_bn: [u0Cost[lo0], u0Cost[hi0]],
    population: unionPop, adults: unionAdults, per_member_usd: [perHead(uCost[lo], unionPop), perHead(uCost[hi], unionPop)],
    per_adult_usd: [perHead(uCost[lo], unionAdults), perHead(uCost[hi], unionAdults)] },
  headcount_basis: "row-4 weights (v4_inputs.py headcount), the union's 39,712,493, plus the case's 3,039,720 added people in G3+ (meta.lineage.counts.added) "
    + "under both conventions; their adults at the case's measured age mix (meta.lineage.age_mix: each count part at its own mix, the 15-19 band's "
    + "adults at the identified G3+'s share of it) [APPROX]",
  added_adults: AA,
  lineage: { item: L.lineageItem, arm: lin.arm, counting: lin.counting.rule, added: nAdded, at_g3_rate: lin.counts.at_g3_rate, later_losses: lin.counts.later_losses,
    added_adults: AA.adults, adult_share: AA.adult_share, members: { g3plus: lin.members.g3plus, white: lin.members.white }, c3: lin.c3,
    age_mix: { reading: lin.age_mix.reading, route: lin.age_mix.route, under_20_share: lin.age_mix.under_20_share },
    row8_edit_bn: lin.edits.row8_edit_bn, row8_shares: Object.fromEntries(CONVS.map((c) => [c, layers[c].share])) },
  items: { order: STEPS, all: ALL_ITEMS, records: L.records.map((r) => ({ id: r.id, kind: r.kind, applied: r.applied, source: r.source, arm: r.arm || null,
    edits: r.edits || null, why: r.why || null })),
    split: Object.fromEntries(CONVS.map((c) => [c, layers[c].items])),
    pension: layers.a.pension ? Object.fromEntries(CONVS.map((c) => {
      const S = layers[c].pension;
      return [c, { inputs: S.inputs, oasdi_bn: S.oasdi, hi_bn: S.hi, social_security_old_bn: S.ss_old, social_security_new_bn: S.ss_new,
        part_a_old_bn: S.part_a_old, part_a_new_bn: S.part_a_new }];
    })) : null },
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
      oct05_cost_bn: [ch.low.oct05_bn, ch.high.oct05_bn], change_from_oct05_bn: [ch.low.change_bn, ch.high.change_bn],
      by_item_bn: Object.fromEntries(STEPS.map((id) => [id, [ch.low[`${id}_bn`], ch.high[`${id}_bn`]]])),
      added_people_bn: g === layers[conv].g3plus ? [added[conv].low.added_people_bn, added[conv].high.added_people_bn] : [0, 0],
    };
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      const cr = capRow(r.full[i]);
      const row = { convention: conv, generation: g, band_end: end, allocation: specs[i].allocation, cost_bn: at(i),
        uncorrected_same_spec_bn: r.uncorrected[i], correction_bn: at(i) - r.uncorrected[i], population: h.population, adults: h.adults,
        per_member_usd: perHead(at(i), h.population), per_adult_usd: perHead(at(i), h.adults), capital_return_bn: cr.capital_total_bn,
        enterprise_surplus_receipt_bn: cr.enterprise_surplus_receipt_bn, housing_enterprise_surplus_receipt_bn: cr.housing_enterprise_surplus_receipt_bn,
        oct05_cost_bn: ch[end].oct05_bn, change_from_oct05_bn: ch[end].change_bn };
      // One column per item in the registry's order (0 where the item does not enter this set), then the added people.
      for (const id of ALL_ITEMS) row[`${id}_bn`] = STEPS.includes(id) ? ch[end][`${id}_bn`] : 0;
      row.added_people_bn = g === layers[conv].g3plus ? added[conv][end].added_people_bn : 0;
      rows.push(row);
    }
  }
}
summary.change_from_oct05_by_item = Object.assign({ parts: PARTS, specifications: { low: lo, high: hi },
  rule: "at the end specifications, which are v5's: oct05_bn is each model at its v5 payload (generation_corrections_oct05*.json); "
    + `${L.lineageItem}_bn the item base less it (the lineage block re-valued on G3+); each edit set's part its edits on the models before `
    + "it, in the payload's order; oct07_bn = oct05_bn + the parts; change_bn = oct07_bn - oct05_bn. A part is the item's change given "
    + "the items before it, so the case lane's interactions sit with the later item" }, chain);
summary.added_people = Object.assign({ rule: "G3+'s v6 model less the same model without the lineage block's cell edits and grid, with every item's "
  + "parts but their lineage parts: the added people's cost, the items' parts on them included" }, added);
summary.rules = {
  lineage: "the added people (meta.lineage: the lineage item's edits in every engine cell, and the production grid's change) go on G3+ under "
    + "both conventions, as the case's package.cjs withLineage() adds them",
  row8: "audit row 8's change at the larger group (the lineage block's last edit) times each generation's share of the September 29 union's "
    + "lane_constants k cell, per allocation (v5's rule)",
  items: Object.fromEntries(L.items.map((it) => [it.id, Object.fromEntries(
    [...new Set(layers.a.items.find((x) => x.id === it.id).edits.flatMap((x) => (x.parts ? x.parts.map((p) => `${p.name}: ${p.rule}`) : [`national-scale: as_is`])))]
      .map((s) => s.split(": ")).map(([k, r]) => [k, `${r}: ${V6.RULE_TEXT[r]}`]))])),
  responses: "every generation at the case's responses (the payload's meta.responses, v5's)",
  convention_b: "[ASSUMPTION] the added people stay in G3+ under (b): their parents' generation is not observed. b_rule_indication "
    + "gives the move had their minors followed the identified G3+'s",
};
summary.b_rule_indication = Object.assign({ rule: "the added people's cost under (b) times the identified G3+'s fall from (a) to (b) (its cost "
  + "without the added people, (a - b) / a): an indication of the move from G3+ to G2 under (b), not a bound; the union is unchanged" }, bIndication);
summary.alternatives = Object.fromEntries(Object.keys(sensitivities).flatMap((k) => k.split("+")).map((k) => [k, V6.ALTERNATIVES[k]]));
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
  meta: { source: "generation_account_2026_09_24/run_generations_v6.cjs", case: CASE, case_lane: V6.V6_LANE, union: L.rel,
    status: L.payload.meta.status, builds_on: summary.builds_on.generation_payloads,
    layout: "convention -> generation -> engine corrections payload (receipt_lines, lines, edits, production); each is the generation's "
      + "September 29 payload (generation_corrections_sept29*.json), then its v6 part: on G3+ the lineage block's cell edits (the added "
      + "people, item " + L.lineageItem + ") and the production grid's change; on every generation audit row 8's change times its "
      + "lane_constants k share; then the edit sets' edits in the payload's order by v6_split.cjs RULES (national-scale edits as they are; "
      + "cell shifts split by their parts' rules). Apply with the union's meta (responses, capital_return). The three models add to the "
      + "union's payload model cell by cell",
    items: STEPS },
  payloads }) + "\n");

console.log(`[results] net cost to other residents at the case's ends ($bn a year; low = ${specs[lo].allocation}, high = ${specs[hi].allocation})`);
console.log(`  union ${f2(summary.union.cost_bn)}; per member $${summary.union.per_member_usd.map((x) => Math.round(x)).join("–$")} (${(unionPop / 1e6).toFixed(2)}M)`);
for (const conv of CONVS) {
  console.log(`  convention (${conv})`);
  for (const g of GENS) {
    const c = summary.conventions[conv][g];
    console.log(`    ${g.padEnd(7)} ${f2(c.cost_bn)}  (v5 ${f2(c.oct05_cost_bn)}; ${STEPS.map((id) => `${id} ${c.by_item_bn[id].map(sgn).join(" / ")}`).join(", ")}); `
      + `per member $${c.per_member_usd.map((x) => Math.round(x)).join("–$")} (${(c.population / 1e6).toFixed(2)}M), per adult $${c.per_adult_usd.map((x) => Math.round(x)).join("–$")}`);
  }
}
console.log(`  (b) indication, the added minors with the identified G3+'s move: ${["low", "high"].map((k) => sgn(bIndication[k].move_to_g2_bn)).join(" / ")} bn from G3+ to G2`);
console.log("  ✓ all generation-run gates passed");
