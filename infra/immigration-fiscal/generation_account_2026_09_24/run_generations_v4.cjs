/* Step 7: the main case of 2026-09-29 (candidate v4's set, adopted at 15:12 JST) by generation.
 *
 * --case picks the set:
 *   sept29       the case: pension accrual at payable benefits, net of the tax on benefits ($371.4146-434.8410bn at
 *                specifications 48 / 11);
 *   sept29_cash  the cash set beside it: the same items with the pension switch off ($294.7011-361.8175bn).
 * The case is the September 27 payload unchanged plus candidate v4's part (v4_split.cjs), so each generation's payload
 * is its September 27 payload (derived/generation_corrections.json, which run_generations.cjs --case sept27 writes and
 * reproduces byte for byte), the case's national-scale edits, and its own v4 tail from v4_split.cjs; its production
 * grid is its row-4 attribution (v4_inputs.py). The September 27 steps, files and cases are untouched: this step reads
 * their outputs and writes only *_<case> files.
 * Item 3 (the IRS-matched income-tax key) is the union's stack factor x the national line x the raked share change, per
 * fill-in method. It is split as run_generations.cjs splits the CBO gradient: each generation's own change in the raked
 * cells (tax_key_split.py) times its own stack factor on the line (its cell after the stack over before), the
 * non-additive remainder spread by the cells after the stack, per method; then the methods averaged, as the payload
 * averages them.
 *
 * Gates (exit 1, nothing written):
 *   - the union's items on the methods' mean model reproduce the payload's v4 part cell by cell (1e-9 bn) and its
 *     receipt lines (1e-12), with the same synthetic lines;
 *   - the September 27 generation payloads add to the September 27 corrections.json cell by cell (1e-9), and their
 *     models to the union's September 27 model;
 *   - item 3's generation shifts add to the union's per method and averaged (1e-12); the production grids add to the
 *     payload's (1e-12);
 *   - under each convention the generations' v4 tails add to the union's cell by cell (1e-9), receipt-line cells (1e-12),
 *     and carry the same lines; each generation's payload gives the model its item chain built (1e-9);
 *   - the union reproduces the case's band at its end specifications against the lane's published band (1e-4, the
 *     band's four decimals) and its per-specification costs (1e-9, mean of the two methods); the specifications are the
 *     September 27 package's, in order;
 *   - in all 64 specifications the generations' costs add to the union's, corrected and uncorrected (1e-9), and so do
 *     their capital returns (total, by level, by part) and enterprise receipts;
 *   - the change from the September 27 case by item, in the package's order, at the end specifications: each model's
 *     steps start at its September 27 cost (the union at the September 27 band, 1e-4; each generation at
 *     generation_results.csv, 5.01e-7, half its last printed digit) and end at its case cost (1e-9); the
 *     generations add to the union item by item (1e-9);
 *   - every alternative rule's split adds to the union's (1e-9).
 * Writes generation_results_<case>.csv, generation_summary_<case>.json and generation_corrections_<case>.json.
 * Per-member figures use the row-4 headcounts (v4_inputs.py), the case's basis. Run from the repository root:
 *   node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v4.cjs [--case sept29|sept29_cash] [--out-dir DIR]
 */
"use strict";
const fs = require("fs");
const path = require("path");
const X = require(path.join(__dirname, "v4_split.cjs"));
const { V4, P, Engine, MODEL, ALLOCS, METHODS, byAlloc, sum, cid } = X;

const HERE = __dirname;
const argv = process.argv.slice(2);
const arg = (name, dflt) => { const i = argv.indexOf(name); return i < 0 ? dflt : argv[i + 1]; };
const CASES = { sept29: "set", sept29_cash: "cash" };
const CASE = arg("--case", "sept29");
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

const C = X.loadCase(CASES[CASE]);
console.log(`[case ${CASE}] ${C.rel}; outputs to ${path.relative(process.cwd(), OUT) || "."}`);

// ---------------------------------------------------------------------------------------------------
console.log("[the union's v4 part]");
const U = X.unionRun(C);
gate("the union's items on the methods' mean model reproduce the payload's v4 part: every cell edit, receipt line and synthetic line",
  U.worst < 1e-9 && U.worstRl < 1e-12 && U.sameLines, `${U.cellsCompared} cells; max |diff| ${e(U.worst)} bn, receipt lines ${e(U.worstRl)}`);

// ---------------------------------------------------------------------------------------------------
console.log("[the September 27 generation payloads]");
const G27 = load("generation_corrections.json");
const union27 = "main_case_long_run_2026_09_27/derived/corrections.json";
gate(`generation_corrections.json splits ${union27}, the case's first ${C.base.edits.length} edits`, G27.meta.union === union27);
const models0 = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) => [g, load(`${c === "a" ? "model_" : "model_b_"}${g}.json`)]))]));
const models27 = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[c][g], G27.payloads[c][g])]))]));
const cellsOf = (m) => {
  const out = new Map();
  for (const l of m.receipts.lines) for (const sc of Object.keys(l.cells)) out.set(`r|${l.id}|${sc}`, l.cells[sc]);
  for (const l of m.spending.lines) for (const k of Object.keys(l.keys)) out.set(`s|${l.id}|${k}`, l.keys[k]);
  return out;
};
for (const conv of CONVS) {
  const want = new Map(C.base.edits.map((x) => [cid(x), x]));
  const ids = new Set([...want.keys(), ...GENS.flatMap((g) => G27.payloads[conv][g].edits.map(cid))]);
  let worst = 0;
  for (const id of ids) {
    for (const a of ALLOCS) {
      const s = sum(GENS.map((g) => sum(G27.payloads[conv][g].edits.filter((y) => cid(y) === id).map((y) => y.by[a]))));
      worst = Math.max(worst, Math.abs(s - sum(C.base.edits.filter((y) => cid(y) === id).map((y) => y.by[a]))));
    }
  }
  const u = cellsOf(U.m27), gs = GENS.map((g) => cellsOf(models27[conv][g]));
  let worstM = 0;
  for (const [k, c] of u) for (const a of ALLOCS) worstM = Math.max(worstM, Math.abs(sum(gs.map((x) => x.get(k)[a].target_bn)) - c[a].target_bn));
  gate(`(${conv}) the September 27 generation payloads add to its corrections.json cell by cell, and their models to the union's`,
    worst < 1e-9 && worstM < 1e-9, `${ids.size} cells, max |diff| ${e(worst)} bn; model cells ${e(worstM)} bn`);
}

// ---------------------------------------------------------------------------------------------------
console.log("[item 3: the IRS-matched income-tax key]");
const stackGen = load("stack_by_generation.json");
const TK = load("tax_key_by_generation.json");
const FITN = X.lineOf(MODEL, "receipts", X.FIT).national_bn;
gate("tax_key_by_generation.json is the payload's key change on model.json's line", TK.meta.line === X.FIT && TK.meta.national_bn === FITN
  && C.options.tax_key === "irs_2023_raked" && TK.meta.variant === V4.TAX_KEYS[C.options.tax_key]
  && ALLOCS.every((a) => TK.union[a] === V4.TAX.share_change[TK.meta.variant][a]), `${TK.meta.variant}, national ${FITN}`);
const REF = MODEL.receipts.reference;
// run_generations.cjs scaledSplit ("own"): each generation's change times its own stack factor, the remainder by cells.
let fitResidual = 0;
function scaledSplit(unionBy, deltas, gm, gp) {
  const out = Object.fromEntries(GENS.map((g) => [g, {}]));
  for (const a of ALLOCS) {
    const t1 = {}, part = {};
    for (const g of GENS) {
      const t0 = X.lineOf(gm[g], "receipts", X.FIT).cells[REF][a].target_bn;
      t1[g] = t0 + ((gp[g].receipts && gp[g].receipts[X.FIT] && gp[g].receipts[X.FIT][a]) || 0);
      part[g] = deltas[g][a] * (t0 === 0 ? 1 : t1[g] / t0);
    }
    const T = sum(GENS.map((g) => t1[g])), resid = unionBy[a] - sum(GENS.map((g) => part[g]));
    fitResidual = Math.max(fitResidual, Math.abs(resid));
    for (const g of GENS) out[g][a] = part[g] + resid * t1[g] / T;
  }
  return out;
}
const fitBy = {}, fitProp = {};
let worstFit = 0;
for (const conv of CONVS) {
  const deltas = Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => FITN * TK[conv][g][a])]));
  const per = METHODS.map((m) => {
    const ub = V4.taxEditOf("central", m, C.options.tax_key);
    const s = scaledSplit(ub, deltas, models0[conv], stackGen.payloads[m][conv]);
    worstFit = Math.max(worstFit, ...ALLOCS.map((a) => Math.abs(sum(GENS.map((g) => s[g][a])) - ub[a])));
    return s;
  });
  fitBy[conv] = Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => sum(per.map((s) => s[g][a])) / per.length)]));
  worstFit = Math.max(worstFit, ...ALLOCS.map((a) => Math.abs(sum(GENS.map((g) => fitBy[conv][g][a])) - U.fitBy[a])));
  // The alternative: the union's shift by the generations' September 27 amounts on the line.
  const amt = Object.fromEntries(GENS.map((g) => [g, V4.refAmount(models27[conv][g], X.FIT)]));
  fitProp[conv] = Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => U.fitBy[a] * amt[g][a] / sum(GENS.map((h) => amt[h][a])))]));
}
gate("item 3: the generations' shifts add to the union's in each fill-in method and in the methods' mean", worstFit < 1e-12,
  `max |diff| ${e(worstFit)} bn; non-additive remainder spread by cells, max ${fitResidual.toFixed(4)} bn; union `
  + ALLOCS.map((a) => `${a} ${U.fitBy[a].toFixed(4)}`).join(", ") + "; (a) " + GENS.map((g) => `${g} ${fitBy.a[g].personal.toFixed(4)}`).join(", "));

// ---------------------------------------------------------------------------------------------------
console.log("[v4 inputs]");
const VI = load("v4_inputs.json");
gate("v4_inputs.json is this lane's three generations", JSON.stringify(VI.meta.generations) === JSON.stringify(GENS));
const grids = {};
let worstGrid = 0;
for (const conv of CONVS) {
  grids[conv] = Object.fromEntries(GENS.map((g) => [g, X.gridOf(C, VI.production.series[conv][g])]));
  for (const k of ["private_wtp_bn", "induced_receipts_bn"]) {
    C.production[k].forEach((v, i) => { worstGrid = Math.max(worstGrid, Math.abs(sum(GENS.map((g) => grids[conv][g][k][i])) - v)); });
  }
}
gate("the generations' row-4 production grids add to the payload's in every scenario, both conventions", worstGrid < 1e-12, `max |diff| ${e(worstGrid)} bn`);

// ---------------------------------------------------------------------------------------------------
console.log("[the split]");
const inputsFor = (conv, alt) => ({ gens: GENS, top: TOP, models27: models27[conv], union: U,
  fitBy: alt.includes("fit_by_amount") ? fitProp[conv] : fitBy[conv],
  tenant: alt.includes("tenant_national") ? VI.tenant_share.national[conv] : VI.tenant_share.rule[conv],
  persons5: Object.fromEntries(GENS.map((g) => [g, VI.headcount[conv][g].persons_5plus])),
  alt: alt.filter((x) => x !== "fit_by_amount" && x !== "tenant_national") });
const S = {}, payloads = {}, models1 = {};
for (const conv of CONVS) {
  S[conv] = X.split(C, inputsFor(conv, []));
  const add = X.additivity(C, GENS, S[conv].tails, U);
  gate(`(${conv}) the generations' v4 tails add to the union's: cell edits, receipt-line cells, the same lines`,
    add.edits < 1e-9 && add.receipt_lines < 1e-12 && add.sameLines, `${add.cells} cells; max |diff| ${e(add.edits)} bn, receipt lines ${e(add.receipt_lines)}`);
  payloads[conv] = Object.fromEntries(GENS.map((g) => [g, X.payloadOf(C, G27.payloads[conv][g], S[conv].tails[g], grids[conv][g])]));
  models1[conv] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(models0[conv][g], payloads[conv][g])]));
  let worst = 0;
  for (const g of GENS) {
    const a1 = cellsOf(models1[conv][g]), b1 = cellsOf(S[conv].final[g]);
    if (a1.size !== b1.size) worst = Infinity;
    for (const [k, c] of b1) for (const a of ALLOCS) worst = Math.max(worst, Math.abs(a1.get(k)[a].target_bn - c[a].target_bn));
  }
  gate(`(${conv}) each generation's payload gives the model its item chain built`, worst < 1e-9, `max |diff| ${e(worst)} bn`);
}

// ---------------------------------------------------------------------------------------------------
console.log("[engine]");
const ev = X.evaluator(C.payload);
const specs = ev.specs;
const S27 = P.MAIN_SPECS;
const SPEC_FIELDS = ["allocation", "normalization", "share", "school", "reading", "gg", "uc"];
gate("the consumer's 64 specifications are the September 27 package's, in order (allocation, normalization, school share and response, "
  + "reading and general government, uninsured key)", specs.length === S27.length && specs.every((s, i) => SPEC_FIELDS.every((k) => s[k] === S27[i][k])));
const unionModel = Engine.applyCorrections(MODEL, C.payload);
const uFull = specs.map((s) => ev.evaluateFull(unionModel, s));
const uCost = uFull.map((r) => r.cost_bn);
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
const O = X.oracle(C.set);
gate(`the corrected union reproduces the case's band at its end specifications (${O.source}, four decimals)`,
  lo === O.specs[0] && hi === O.specs[1] && near(uCost[lo], O.band[0], 1e-4) && near(uCost[hi], O.band[1], 1e-4),
  `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)} at ${lo} / ${hi}`);
const PS = X.perSpec(C.set);
if (PS) {
  let worst = 0;
  for (const [i, c] of PS.cost) worst = Math.max(worst, Math.abs(uCost[i] - c));
  gate(`the corrected union reproduces ${PS.source} at each of its specifications (mean of the two methods)`,
    PS.cost.size > 0 && worst < 1e-9, `${PS.cost.size} specifications; max |diff| ${e(worst)} bn`);
} else console.log(`  · ${X.V4_LANE} publishes no per-specification cost for the ${C.set} set`);
const u0Cost = specs.map((s) => ev.cost(MODEL, s));
const lo0 = u0Cost.indexOf(Math.min(...u0Cost)), hi0 = u0Cost.indexOf(Math.max(...u0Cost));
if (O.uncorrected) {
  gate(`the uncorrected model at the case's responses reproduces ${O.source.replace(/ \(.*\)$/, "")} uncorrected_at_adopted_responses (1e-4)`,
    near(u0Cost[lo0], O.uncorrected[0], 1e-4) && near(u0Cost[hi0], O.uncorrected[1], 1e-4), `${u0Cost[lo0].toFixed(4)}–${u0Cost[hi0].toFixed(4)} at ${lo0} / ${hi0}`);
} else console.log(`  · the uncorrected model at the case's responses: ${u0Cost[lo0].toFixed(4)}–${u0Cost[hi0].toFixed(4)} at ${lo0} / ${hi0}`);
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
    const full = specs.map((s) => ev.evaluateFull(models1[conv][g], s));
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
// The adopted lane's own package on every model costed here, as its other consumers call it (V4_LANE = ADOPTED only).
const AP = X.adoptedPackage(C);
if (AP) {
  gate(`${AP.source}: its specifications are the consumer's`, AP.specs.length === specs.length
    && AP.specs.every((s, i) => SPEC_FIELDS.every((k) => s[k] === specs[i][k])));
  let worst = 0;
  specs.forEach((_, i) => {
    worst = Math.max(worst, Math.abs(AP.cost(unionModel, i) - uCost[i]), Math.abs(AP.cost(MODEL, i) - u0Cost[i]));
    for (const conv of CONVS) for (const g of GENS) {
      worst = Math.max(worst, Math.abs(AP.cost(models1[conv][g], i) - res[conv][g].corrected[i]),
        Math.abs(AP.cost(models0[conv][g], i) - res[conv][g].uncorrected[i]));
    }
  });
  gate(`${AP.source} evaluateFull gives every model's cost here (union and generations, corrected and uncorrected, all specifications)`,
    worst < 1e-9, `max |diff| ${e(worst)} bn`);
} else console.log(`  · cross-check against the adopted lane's package skipped: v4_split.cjs V4_LANE is ${X.V4_LANE}`);

// ---------------------------------------------------------------------------------------------------
// The change from the September 27 case by item, in the package's order, at the case's end specifications (also the
// September 27 case's). Step 0 is the September 27 model on the September 27 payload's meta; each later step is the
// model after that item, costed with the responses and capital keys of the items up to it (v4_split.cjs metaUpTo), the
// row-4 grid from item 2 on. The steps telescope to the case's cost.
console.log("[change from the September 27 case, by item]");
const ev27 = X.evaluator(C.base);
const evUpTo = Object.fromEntries(X.ITEMS.map((it) => [it, X.evaluator(X.metaUpTo(C, it))]));
const withGrid = (m, grid) => (grid ? Object.assign({}, m, { production: Object.assign({}, m.production, {
  private_wtp_bn: grid.private_wtp_bn, induced_receipts_bn: grid.induced_receipts_bn, sampling_se_bn: grid.sampling_se_bn }) }) : m);
function byItem(m27, steps, final, grid) {
  const at = (i) => {
    const out = { sept27_bn: ev27.cost(m27, specs[i]) };
    let prev = out.sept27_bn;
    const models = Object.fromEntries(steps);
    for (const it of X.ITEMS) {
      const k = X.ITEMS.indexOf(it);
      const m = it === "pension" ? final : models[it];
      const c = evUpTo[it].cost(withGrid(m, k >= X.ITEMS.indexOf("2") ? grid : null), specs[i]);
      out[`${it}_bn`] = c - prev;
      prev = c;
    }
    out.sept29_bn = prev;
    out.change_bn = prev - out.sept27_bn;
    return out;
  };
  return { low: at(lo), high: at(hi) };
}
const unionGrid = C.production ? { private_wtp_bn: C.production.private_wtp_bn, induced_receipts_bn: C.production.induced_receipts_bn,
  sampling_se_bn: C.production.sampling_se_bn } : null;
const uFinal = C.pension ? X.pensionStep(U.A.m, { oasdi: U.oasdi, fitScale: byAlloc(() => 1), partAScale: byAlloc(() => 1) }) : U.A.m;
const chain = { union: byItem(U.m27, U.A.steps, uFinal, unionGrid) };
const band27 = P.csvRows("main_case_long_run_2026_09_27/derived/main_case_bands.csv").find((x) => x.profile === P.MAIN_PROFILE && x.variant === "adopted");
const rows27 = P.csvRows("generation_account_2026_09_24/derived/generation_results.csv");
let worstEnd = 0, worst27 = 0, worstAdd = 0;
worst27 = Math.max(Math.abs(chain.union.low.sept27_bn - Number(band27.cost_low_bn)), Math.abs(chain.union.high.sept27_bn - Number(band27.cost_high_bn)));
worstEnd = Math.max(Math.abs(chain.union.low.sept29_bn - uCost[lo]), Math.abs(chain.union.high.sept29_bn - uCost[hi]));
let worstGen27 = 0;
for (const conv of CONVS) {
  chain[conv] = {};
  for (const g of GENS) {
    chain[conv][g] = byItem(models27[conv][g], S[conv].A[g].steps, S[conv].final[g], grids[conv][g]);
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      worstEnd = Math.max(worstEnd, Math.abs(chain[conv][g][end].sept29_bn - res[conv][g].corrected[i]));
      const r27 = rows27.find((r) => r.convention === conv && r.generation === g && r.band_end === end);
      worstGen27 = Math.max(worstGen27, Math.abs(chain[conv][g][end].sept27_bn - Number(r27.cost_bn)));
    }
  }
  for (const end of ["low", "high"]) {
    for (const k of Object.keys(chain.union[end])) {
      worstAdd = Math.max(worstAdd, Math.abs(sum(GENS.map((g) => chain[conv][g][end][k])) - chain.union[end][k]));
    }
  }
}
gate("the steps start at the September 27 case (the union at main_case_bands.csv adopted, 1e-4; each generation at generation_results.csv, "
  + "5.01e-7: half its last printed digit) and end at this case's cost (1e-9)", worst27 < 1e-4 && worstGen27 < 5.01e-7 && worstEnd < 1e-9,
`union ${e(worst27)}, generations ${e(worstGen27)}, ends ${e(worstEnd)} bn`);
gate("the generations' changes add to the union's item by item, both conventions, both ends", worstAdd < 1e-9, `max |diff| ${e(worstAdd)} bn`);

// ---------------------------------------------------------------------------------------------------
// Alternatives to the designed rules, each re-run through the split and costed at the ends.
console.log("[alternative rules]");
const ALTS = Object.assign({ fit_by_amount: "item 3: the union's shift by the generations' September 27 amounts on the federal income-tax line" },
  X.ALTERNATIVES);
const sensitivities = {};
let worstAlt = 0;
for (const [name, label] of Object.entries(ALTS)) {
  if (X.PENSION_ALTERNATIVES.includes(name) && !C.pension) continue;
  sensitivities[name] = { rule: label };
  for (const conv of CONVS) {
    const s = X.split(C, inputsFor(conv, [name]));
    const add = X.additivity(C, GENS, s.tails, U);
    worstAlt = Math.max(worstAlt, add.edits, add.sameLines ? 0 : Infinity);
    sensitivities[name][conv] = Object.fromEntries(GENS.map((g) => {
      const m = Engine.applyCorrections(models0[conv][g], X.payloadOf(C, G27.payloads[conv][g], s.tails[g], grids[conv][g]));
      const c = [ev.cost(m, specs[lo]), ev.cost(m, specs[hi])];
      return [g, { cost_bn: c, move_bn: [c[0] - res[conv][g].corrected[lo], c[1] - res[conv][g].corrected[hi]] }];
    }));
  }
  const x = sensitivities[name].a;
  console.log(`  · ${name}: (a) ` + GENS.map((g) => `${g} ${x[g].move_bn.map((v) => (v >= 0 ? "+" : "") + v.toFixed(3)).join(" / ")}`).join("; "));
}
gate("every alternative rule's split adds to the union's cell by cell, with the same lines", worstAlt < 1e-9, `max |diff| ${e(worstAlt)} bn`);

// ---------------------------------------------------------------------------------------------------
// Results.
const H = VI.headcount;
const perHead = (bn, n) => bn * 1e9 / n;
const rows = [];
const summary = {
  case: CASE, set: C.set, lane: X.V4_LANE, payload: C.rel, oracle: O,
  responses: C.payload.meta.responses, low_spec: specs[lo], high_spec: specs[hi],
  specifications: { low: specs[lo], high: specs[hi], low_index: lo, high_index: hi },
  union: { cost_bn: [uCost[lo], uCost[hi]], uncorrected_bn: [u0Cost[lo], u0Cost[hi]], uncorrected_own_ends_bn: [u0Cost[lo0], u0Cost[hi0]],
    population: H.union.population, adults: H.union.adults, per_member_usd: [perHead(uCost[lo], H.union.population), perHead(uCost[hi], H.union.population)] },
  headcount_basis: "row-4 weights (v4_inputs.py headcount): the case's per-member basis, the union's 39,712,493",
  conventions: {},
};
for (const conv of CONVS) {
  summary.conventions[conv] = {};
  for (const g of GENS) {
    const r = res[conv][g], h = H[conv][g];
    const at = (i) => r.corrected[i];
    summary.conventions[conv][g] = {
      population: h.population, adults: h.adults,
      cost_bn: [at(lo), at(hi)], own_span_bn: [Math.min(...r.corrected), Math.max(...r.corrected)],
      per_member_usd: [perHead(at(lo), h.population), perHead(at(hi), h.population)],
      per_adult_usd: [perHead(at(lo), h.adults), perHead(at(hi), h.adults)],
      uncorrected_cost_bn: [r.uncorrected[lo], r.uncorrected[hi]], correction_bn: [at(lo) - r.uncorrected[lo], at(hi) - r.uncorrected[hi]],
      sept27_cost_bn: [chain[conv][g].low.sept27_bn, chain[conv][g].high.sept27_bn],
      change_from_sept27_bn: [chain[conv][g].low.change_bn, chain[conv][g].high.change_bn],
    };
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      const cr = capRow(r.full[i]);
      rows.push({ convention: conv, generation: g, band_end: end, allocation: specs[i].allocation, cost_bn: at(i),
        uncorrected_same_spec_bn: r.uncorrected[i], correction_bn: at(i) - r.uncorrected[i], population: h.population, adults: h.adults,
        per_member_usd: perHead(at(i), h.population), per_adult_usd: perHead(at(i), h.adults), capital_return_bn: cr.capital_total_bn,
        enterprise_surplus_receipt_bn: cr.enterprise_surplus_receipt_bn, housing_enterprise_surplus_receipt_bn: cr.housing_enterprise_surplus_receipt_bn,
        sept27_cost_bn: chain[conv][g][end].sept27_bn, change_from_sept27_bn: chain[conv][g][end].change_bn });
    }
  }
}
summary.change_from_sept27_by_item = Object.assign({ items: X.ITEMS, specifications: { low: lo, high: hi },
  rule: "sequential in candidate v4's order (package.cjs modelFor): each step is the model after the item, costed with the responses and "
    + "capital keys of the items up to it and the row-4 grid from item 2 on; the parts add to change_bn. Item 2's part is the production "
    + "grid, item 4's the housing capital key; the pension part is zero in the cash set" }, chain);
summary.rules = {
  text: Object.assign({ "3": "each generation's own change in the raked cells (tax_key_split.py) x its own stack factor on the line, the remainder "
      + "by cells after the stack, per fill-in method, then the methods' mean (run_generations.cjs scaledSplit, as the CBO gradient)",
  "1": "v2 splitHousing on each generation's model (the deficit at its rental-key share)", "2": "row-4 attribution (v4_inputs.py)",
  "4": "the component's key on each generation's evaluation", "5_tenant": "the group's contract-rent share by state split by the generations' "
      + "persons in cash-rent homes (v4_inputs.py)", "5_personal": "the group's vehicle share x the generation's part of the licence line",
  "6a_7_state": "the union's ratios and indexes on each generation's own amounts and keys (package functions)",
  roads: "the union's methods'-mean driver-mile share x the generation's persons aged 5 and over over the union's (row-4 weights)",
  pension: "the union's accrual split by the generations' net OASDI accrual per tax dollar x their OASDI receipts; Part A by their Part A "
      + "accrual per HI tax dollar x their HI receipts; the benefit tax by their 2024 benefit tax (pension lane at 9ea1beb); convention (b) "
      + "takes convention (a)'s ratios and shares" }),
  alternatives: ALTS,
  parameters: Object.fromEntries(CONVS.map((conv) => [conv, Object.fromEntries(GENS.map((g) => [g, {
    fit_by_bn: fitBy[conv][g], tenant_share: VI.tenant_share.rule[conv][g], vehicle_share: S[conv].vehicle[g], s_vmt: S[conv].s_vmt[g],
    under5_share: VI.under5_share[conv][g], persons_5plus: VI.headcount[conv][g].persons_5plus,
    pension_refs: S[conv].pension ? S[conv].pension.refs[g] : null }]))])),
  union: { fit_by_bn: U.fitBy, s_vmt: U.sbar, oasdi_bn: U.oasdi, pension: C.pension ? X.pensionInputs() : null },
  item3_scaling_remainder_max_bn: fitResidual,
};
summary.sensitivities = sensitivities;
summary.not_computed = {
  state_generation_indexes: "state pricing by each generation's own state mix (the design's alternative) is not computed: the union's indexes "
    + "on each generation's keys are the payload's rule",
  ledger_bridge: "compare_ledger.py's bridge to the September 19 ledger stays on the September 27 run",
};
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
  meta: { source: "generation_account_2026_09_24/run_generations_v4.cjs", case: CASE, case_lane: X.V4_LANE, union: C.rel,
    layout: "convention -> generation -> engine corrections payload (receipt_lines, lines, edits, production); each is the generation's "
      + "September 27 payload (generation_corrections.json), the case's national-scale edits and its v4 tail; apply with the union's "
      + "meta (responses, capital_return). The three add to the union's payload cell by cell, the scales aside" },
  payloads }) + "\n");

console.log(`[results] net cost to other residents at the case's ends ($bn a year; low = ${specs[lo].allocation}, high = ${specs[hi].allocation})`);
console.log(`  union ${f2(summary.union.cost_bn)}; per member $${summary.union.per_member_usd.map((x) => Math.round(x)).join("–$")}`);
for (const conv of CONVS) {
  console.log(`  convention (${conv})`);
  for (const g of GENS) {
    const c = summary.conventions[conv][g];
    console.log(`    ${g.padEnd(7)} ${f2(c.cost_bn)}  (September 27 ${f2(c.sept27_cost_bn)}; change ${c.change_from_sept27_bn.map((x) => (x >= 0 ? "+" : "") + x.toFixed(2)).join(" / ")}); `
      + `per member $${c.per_member_usd.map((x) => Math.round(x)).join("–$")}, per adult $${c.per_adult_usd.map((x) => Math.round(x)).join("–$")}`);
  }
}
console.log("[change from the September 27 case by item] $bn, low / high");
const fi = (x, k) => ["low", "high"].map((end) => (x[end][k] >= 0 ? "+" : "") + x[end][k].toFixed(2)).join("/");
for (const [label, x] of [["union", chain.union], ...CONVS.flatMap((conv) => GENS.map((g) => [`(${conv}) ${g}`, chain[conv][g]]))]) {
  console.log(`    ${label.padEnd(12)} ` + X.ITEMS.map((it) => `${it} ${fi(x, `${it}_bn`)}`).join(", "));
}
console.log("  ✓ all generation-run gates passed");
