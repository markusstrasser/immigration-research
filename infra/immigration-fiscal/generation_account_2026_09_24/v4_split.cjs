/* v4 case (sept29): the September 29 main case's edits split by generation, for any set of models whose September 27
 * payloads add to the union's: this lane's three generations (run_generations_v4.cjs) and the late-arrival lane's nine
 * cells (its run_cells.cjs). A module: it runs nothing and writes nothing.
 *
 * The case (main_case_2026_09_29, adopted 2026-09-29 15:12 JST: candidate v4's set) is a payload: the September 27
 * corrections.json unchanged, then candidate v4's receipt lines, national-scale edits, cell edits, synthetic lines and
 * production grid (main_case_candidate_v4_2026_09_29/payload.cjs). Its cell edits are the two fill-in methods' mean
 * change from the September 27 models to v4's, beyond the scales. Every item is linear in the cells it reads except
 * roads' driver-mile share s_vmt(p), so the items applied once to the methods' mean model (the September 27 payload on
 * model.json) give the payload's edits, with s_vmt at the methods' mean (read off meta.roads_mileage_key.k_road:
 * k_road = FP s_vmt + (1 - FP) k_freight, k_freight linear). unionRun() does that and is gated against the payload.
 * The generation split applies candidate v4's own item functions (package.cjs and the v3, v2 and receipt-side modules
 * it loads, read-only) to each generation's September 27 model in the package's order, each union input replaced by
 * the generation's own:
 *   1 housing deficit    v2 splitHousing on the generation's model: the national scales, and the deficit line at the
 *                        generation's rental-key share (the item's own rule; exact);
 *   2 production         the generation's row-4 grid (v4_inputs.py: production.py's attribution on the row-4 weights);
 *   3 IRS tax key        the caller's split of the union's shift (this lane: each generation's own change in the raked
 *                        cells, tax_key_split.py, times its own stack factor, the remainder by cells, as the CBO
 *                        gradient is split);
 *   4 housing capital    nothing: the component's key is the rental line's, read on the generation's evaluation;
 *   5 owner              nothing: a response;
 *   5 tenant             receipt-side splitTenant at the generation's part of the group's contract-rent share
 *                        (v4_inputs.py: the group's rent by state split by the generations' persons in cash-rent homes);
 *   5 personal property  re-keyed to the group's vehicle share x the generation's part of the licence line (its adults
 *                        key), per allocation;
 *   6a payroll           v3 payrollShifts on the generation's model: the union's ratios on its own amounts;
 *   7 workers' comp      v4 withWorkersCompOnly on the generation's model: the union's ratio on its own key cell;
 *   roads                v4 withRoads with the generation's keys and driver-mile share: the union's s_vmt x the
 *                        generation's persons aged 5 and over over the union's (row-4 weights, v4_inputs.py: every such
 *                        person at the union's miles); the road key, the synthetic lines, gasoline and licences follow
 *                        from its own excise, adults and economic-affairs keys by the package's formulas;
 *   state                v4 withStatePrice on the generation's model: the union's indexes on its own parent keys and
 *                        receipt amounts;
 *   pension (set only)   v4 withPensionNet with generation references: the union's accrual (ratio_net x its OASDI
 *                        receipts) split by the generations' accrual per tax dollar net of the benefit tax (pension lane
 *                        at 9ea1beb: OASDI accrual per tax dollar at payable benefits x (1 - the future benefit-tax
 *                        share at the generation's own rate)) x their OASDI receipts in the account; the Part A accrual
 *                        likewise, by the generations' Part A accrual per HI tax dollar (hi_arms.csv, central row:
 *                        accrual_bn / hi_tax_bn) x their HI receipts in the account; the tax on current benefits by the
 *                        generations' 2024 benefit tax (benefit_tax.json, census-income mapping, per allocation). A cell
 *                        inside a generation (TOP) takes its generation's ratios on its own OASDI and HI receipts, and
 *                        its generation's benefit tax by its own social_security key.
 * ALTERNATIVES holds the rule beside each designed one (the sensitivities). Each generation's tail is its final model
 * less its September 27 model beyond the scales, cell by cell (payload.cjs partsOf on one model pair).
 *
 * The adopted lane's files come from V4_LANE, the one constant (main_case_2026_09_29 since it landed at 40c4ba7; the
 * candidate lane before). The set's payload is that lane's corrections.json; the cash set's is candidate v4's cash
 * payload, which the adopted lane builds its cash_set row from and does not publish itself. evaluator(payload)
 * evaluates any model at the case's 64 specifications with the candidate's package-free consumer (consumer.cjs:
 * engine.js, the payload's responses and capital rules), adding the payload's correction lines at zero where a model
 * lacks them and dropping the response of a receipt line it lacks. It also costs the per-item steps, whose partial metas
 * the adopted package cannot load. adoptedPackage(C) is the adopted package itself, which the runners gate it against
 * on every model they cost.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const FISCAL = path.resolve(__dirname, "..");
const ROOT = path.resolve(FISCAL, "..", "..");
// The adopted case's lane (landed at 40c4ba7); the candidate's until then.
const V4_LANE = "main_case_2026_09_29";
const CANDIDATE = "main_case_candidate_v4_2026_09_29";
const ADOPTED = "main_case_2026_09_29";
const V4 = require(path.join(FISCAL, CANDIDATE, "package.cjs"));
const Consumer = require(path.join(FISCAL, CANDIDATE, "consumer.cjs"));
const P = V4.SEPT27;
const { Engine, MODEL, ALLOCS, METHODS } = P;
const RS = V4.RS;
const byAlloc = V4.byAlloc;
const lineOf = V4.lineOf;
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const csvRows = P.csvRows;
const clone = (x) => JSON.parse(JSON.stringify(x));
const sum = (xs) => xs.reduce((a, b) => a + b, 0);

// The payloads of each lane that can carry the adopted case (paths under infra/immigration-fiscal). The adopted lane
// holds the set's; its cash set is candidate v4's cash payload (its summary.json v4.inputs).
const LANE_FILES = {
  [CANDIDATE]: { set: `${CANDIDATE}/derived/corrections_v4.json`, cash: `${CANDIDATE}/derived/corrections_v4_cash.json` },
  [ADOPTED]: { set: `${ADOPTED}/derived/corrections.json`, cash: `${CANDIDATE}/derived/corrections_v4_cash.json` },
};
const FIT = "federal_income_tax";
const SALES = V4.SALES_LINE, LICENCES = V4.LICENCES;
const PERSONAL = RS.PERSONAL_LINE;
// The set's composition rules (package.cjs RULES); the split is written for them and stops on any other.
const RULES = V4.RULES;

// ---------------------------------------------------------------------------------------------------
// The case: its payload, the September 27 payload it starts with, and its parts.
function loadCase(set) {
  const files = LANE_FILES[V4_LANE];
  if (!files || !files[set]) throw new Error(`[BLOCKED] ${V4_LANE}: no ${set} payload known to v4_split.cjs`);
  const rel = files[set];
  const payload = readJson(rel);
  const base = readJson("main_case_long_run_2026_09_27/derived/corrections.json");
  const n = base.edits.length;
  if (JSON.stringify(payload.lines.slice(0, base.lines.length)) !== JSON.stringify(base.lines)
    || JSON.stringify(payload.edits.slice(0, n)) !== JSON.stringify(base.edits)) {
    throw new Error(`[BLOCKED] ${rel} does not start with the September 27 lines and edits`);
  }
  const tail = payload.edits.slice(n);
  const scales = tail.filter((e) => e.national_bn !== undefined);
  const cells = tail.filter((e) => e.national_bn === undefined);
  if (tail.slice(0, scales.length).some((e) => e.national_bn === undefined)) {
    throw new Error(`[BLOCKED] ${rel}: the national-scale edits do not come first in v4's part`);
  }
  const cv = payload.meta.candidate_v4;
  if (!cv) throw new Error(`[BLOCKED] ${rel}: no meta.candidate_v4`);
  const options = V4.withCentral(Object.assign({}, V4.OFF, ...cv.items.map((it) => it.options), cv.rules));
  const want = V4.withCentral(set === "set" ? V4.SET : V4.CASH);
  if (JSON.stringify(options) !== JSON.stringify(want)) throw new Error(`[BLOCKED] ${rel}: its items are not candidate v4's ${set}`);
  for (const [k, v] of Object.entries(RULES)) if (options[k] !== v) throw new Error(`[BLOCKED] ${rel}: rule ${k} ${options[k]}, not the set's ${v}`);
  return { set, rel, payload, base, scales, cells, options, items: V4.PROPERTY_READINGS[options.property_reading],
    pension: options.pension4 === "payable_net", newLines: payload.lines.slice(base.lines.length),
    receiptLines: payload.receipt_lines || [], production: payload.production || null };
}

// ---------------------------------------------------------------------------------------------------
// The items on one model, in package.cjs modelFor's order. prm: fit_by (item 3's shift on the reference rule, by
// allocation), tenant_share, vehicle_share (by allocation), svmt(k) (the driver-mile share by allocation, given the
// model's road keys after 6a). Returns the model before the pension switch and the model after each item.
const apply = (m, edits, lines) => Engine.applyCorrections(m, { lines: lines || [], edits, meta: m.corrections });
function rekeyShares(m, id, share) {
  const l = lineOf(m, "receipts", id);
  return apply(m, m.receipts.scenarios.map((sc) => ({ side: "receipt", line: id, scenario: sc,
    by: byAlloc((a) => l.national_bn * share[a] - l.cells[sc][a].target_bn) })));
}
function chainA(m27, prm, C) {
  const o = C.options, steps = [];
  let m = V4.splitHousing(m27, V4.TRANSFERS[o.internal_transfer].bn);
  steps.push(["1", m], ["2", m]);
  m = apply(m, P.expand([{ side: "receipt", line: FIT, by: prm.fit_by }]));
  steps.push(["3", m], ["4", m]);
  m = RS.splitTenant(m, C.items.tenant.national, prm.tenant_share);
  m = rekeyShares(m, PERSONAL, prm.vehicle_share);
  steps.push(["5", m]);
  m = apply(m, P.expand(V4.payrollShifts(m, "central", o)));
  steps.push(["6a", m]);
  m = V4.withWorkersCompOnly(m);
  steps.push(["7", m]);
  const k = V4.roadKeysOf(m);
  const sv = prm.svmt(k);
  const kg = byAlloc((a) => Object.assign({}, k[a], { s_vmt: sv[a] }));
  const r = V4.withRoads(m, kg, kg, o, true);
  m = r.m;
  steps.push(["roads", m]);
  m = V4.withStatePrice(m, { [SALES]: V4.refAmount(m, SALES), [LICENCES]: V4.refAmount(m, LICENCES) });
  steps.push(["state", m]);
  return { m, steps, roads: { keys_after_6a: k, s_vmt: sv, k_road: r.k_road } };
}
// The pension switch with references {oasdi, fitScale, partAScale} (package.cjs withPensionNet).
const pensionStep = (m, refs) => V4.withPensionNet(m, refs);
const ssKey = (m) => { const l = lineOf(m, "spending", V4.SS_LINE); return byAlloc((a) => l.keys[l.preferred_key][a].target_bn); };

// ---------------------------------------------------------------------------------------------------
// A model's tail against its September 27 model: new receipt lines, cell edits beyond the scales, new lines with their
// amounts (payload.cjs partsOf on one pair).
function tailOf(m4, m27, scales) {
  const factor = {};
  for (const e of scales) {
    const l = lineOf(m27, e.side === "receipt" ? "receipts" : "spending", e.line);
    factor[`${e.side}|${e.line}`] = e.national_bn / l.national_bn;
  }
  const out = { receipt_lines: [], edits: [], lines: [] };
  const baseR = new Set(m27.receipts.lines.map((l) => l.id));
  for (const l4 of m4.receipts.lines) {
    if (!baseR.has(l4.id)) { out.receipt_lines.push(clone(l4)); continue; }
    const lb = lineOf(m27, "receipts", l4.id), s = factor[`receipt|${l4.id}`];
    for (const sc of Object.keys(l4.cells)) {
      const by = byAlloc((a) => l4.cells[sc][a].target_bn - (s === undefined ? lb.cells[sc][a].target_bn : lb.cells[sc][a].target_bn * s));
      if (ALLOCS.some((a) => by[a] !== 0)) out.edits.push({ side: "receipt", line: l4.id, scenario: sc, by });
    }
  }
  const baseS = new Set(m27.spending.lines.map((l) => l.id));
  for (const l4 of m4.spending.lines) {
    if (!baseS.has(l4.id)) {
      out.lines.push({ id: l4.id, family: l4.family, response_class: l4.response_class, label: l4.label });
      out.edits.push({ side: "spending", line: l4.id, key: "k", by: byAlloc((a) => l4.keys.k[a].target_bn) });
      continue;
    }
    const lb = lineOf(m27, "spending", l4.id), s = factor[`spending|${l4.id}`];
    for (const key of Object.keys(l4.keys)) {
      const by = byAlloc((a) => l4.keys[key][a].target_bn - (s === undefined ? lb.keys[key][a].target_bn : lb.keys[key][a].target_bn * s));
      if (ALLOCS.some((a) => by[a] !== 0)) out.edits.push({ side: "spending", line: l4.id, key, by });
    }
  }
  return out;
}
const cid = (x) => [x.side, x.line, x.side === "receipt" ? x.scenario : x.key].join("|");

// ---------------------------------------------------------------------------------------------------
// The union once, on the methods' mean model: its tail must be the payload's (gate), and it fixes the union inputs the
// generation rules split (the methods' mean driver-mile share, the OASDI receipts after 6a).
function unionRun(C) {
  const m27 = Engine.applyCorrections(MODEL, C.base);
  const fitBy = byAlloc((a) => sum(METHODS.map((x) => V4.taxEditOf("central", x, C.options.tax_key)[a])) / METHODS.length);
  const kRoad = C.payload.meta.roads_mileage_key.k_road.methods_mean;
  let sbar = null;
  const A = chainA(m27, { fit_by: fitBy, tenant_share: C.items.tenant.share, vehicle_share: byAlloc(() => C.items.personal.share),
    svmt: (k) => (sbar = byAlloc((a) => (kRoad[a] - (1 - V4.FP) * k[a].k_cons) / V4.FP)) }, C);
  const oasdi = V4.oasdiOf(A.m), hi = V4.hiOf(A.m), ks = ssKey(A.m);
  const m4 = C.pension ? pensionStep(A.m, { oasdi, fitScale: byAlloc(() => 1), partAScale: byAlloc(() => 1) }) : A.m;
  const tail = tailOf(m4, m27, C.scales);
  // Against the payload: every cell edit, receipt line and synthetic line.
  const want = new Map(C.cells.map((x) => [cid(x), x]));
  const got = new Map(tail.edits.map((x) => [cid(x), x]));
  let worst = 0;
  for (const id of new Set([...want.keys(), ...got.keys()])) {
    for (const a of ALLOCS) worst = Math.max(worst, Math.abs((got.has(id) ? got.get(id).by[a] : 0) - (want.has(id) ? want.get(id).by[a] : 0)));
  }
  let worstRl = 0;
  for (const l of C.receiptLines) {
    const g = tail.receipt_lines.find((x) => x.id === l.id);
    if (!g || g.national_bn !== l.national_bn) { worstRl = Infinity; continue; }
    for (const sc of Object.keys(l.cells)) for (const a of ALLOCS) for (const k of ["target_bn", "other_bn", "share"]) {
      worstRl = Math.max(worstRl, Math.abs(g.cells[sc][a][k] - l.cells[sc][a][k]));
    }
  }
  const sameLines = JSON.stringify(tail.lines) === JSON.stringify(C.newLines) && tail.receipt_lines.length === C.receiptLines.length;
  return { m27, m4, A, tail, fitBy, sbar, oasdi, hi, ks, worst, worstRl, sameLines, cellsCompared: new Set([...want.keys(), ...got.keys()]).size };
}

// ---------------------------------------------------------------------------------------------------
// The pension lane's generation inputs at the payload's pinned commit (package.cjs PENSION_COMMIT).
let pensionCache = null;
function pensionInputs() {
  if (pensionCache) return pensionCache;
  const pp = V4.pensionNet();
  const dir = "infra/immigration-fiscal/pension_accrual_2026_09_28/derived";
  const show = (f) => execFileSync("git", ["-C", ROOT, "show", `${pp.commit}:${dir}/${f}`], { maxBuffer: 1 << 28, stdio: ["ignore", "pipe", "ignore"] }).toString("utf8");
  const S = JSON.parse(show("summary.json"));
  const BT = JSON.parse(show("benefit_tax.json"));
  const rows = (text) => { const [h, ...r] = text.trim().split("\n"); const k = h.split(","); return r.map((x) => Object.fromEntries(x.split(",").map((v, i) => [k[i], v]))); };
  const c = S.central;
  const hi = rows(show("hi_arms.csv")).filter((r) => r.rate === c.rate && r.scenario === c.scenario && r.mortality === c.mortality
    && r.spouse === (c.spouse ? "True" : "False") && r.unauthorized === c.unauthorized);
  const gens = ["G1", "G2", "G3plus"];
  const bad = (why) => { throw new Error(`[BLOCKED] pension lane at ${pp.commit}: ${why}`); };
  if (hi.length !== 4 || !gens.concat(["union"]).every((g) => hi.some((r) => r.group === g))) bad("no single central row per group in hi_arms.csv");
  const pa = Object.fromEntries(gens.map((g) => [g, Number(hi.find((r) => r.group === g).accrual_bn)]));
  const hiTax = Object.fromEntries(gens.map((g) => [g, Number(hi.find((r) => r.group === g).hi_tax_bn)]));
  const paUnion = Number(hi.find((r) => r.group === "union").accrual_bn);
  if (Math.abs(paUnion - pp.part_a_accrual_bn) > 1e-6 || Math.abs(sum(Object.values(pa)) - paUnion) > 3e-6) bad("Part A rows are not the payload's accrual");
  const per = S.oasdi_per_tax_dollar_central_by_generation, own = S.benefit_tax.future_share_by_generation_own_rate;
  if (Math.abs(per.union * (1 - S.benefit_tax.future_share_group) - pp.ratio_net) > 1e-15) bad("ratio_net is not the union's per-tax-dollar accrual net of its future share");
  const key = BT.results[BT.central_mapping].key;
  const bt = byAlloc((a) => Object.fromEntries(gens.map((g) => [g, key[a].by_generation_benefit_tax_bn[g]])));
  if (!ALLOCS.every((a) => Math.abs(sum(gens.map((g) => bt[a][g])) - key[a].group_benefit_tax_bn[0]) < 1e-12)) bad("the benefit tax by generation does not add to the group's");
  pensionCache = { commit: pp.commit, ratio_net: pp.ratio_net, gens,
    net_ratio: Object.fromEntries(gens.map((g) => [g, per[g] * (1 - own[g])])), per_tax_dollar: Object.fromEntries(gens.map((g) => [g, per[g]])),
    future_share_own_rate: Object.fromEntries(gens.map((g) => [g, own[g]])),
    part_a: pa, part_a_union: paUnion, hi_tax: hiTax, part_a_per_hi_tax: Object.fromEntries(gens.map((g) => [g, pa[g] / hiTax[g]])),
    benefit_tax: bt, mapping: BT.central_mapping };
  return pensionCache;
}

// ---------------------------------------------------------------------------------------------------
// The split. opts: gens, top ({cell: its generation}), models27 ({g: September 27 model}), fitBy ({g: by}), tenant
// ({g: share}), persons5 ({g: persons aged 5 and over, row-4 weights}), union (unionRun's result), alt (a list of
// alternative rules, ALTERNATIVES). Every rule is linear in its generation's inputs, so cells that add to a generation
// get that generation's parts (the late-arrival lane's G1 cells add to this lane's G1).
const ALTERNATIVES = {
  tenant_national: "tenant line: the generations' persons in cash-rent homes nationally (no state rent weights)",
  vehicles_by_population: "personal property: the group's vehicle share by the generations' population shares",
  roads_by_population: "roads: the driver-mile share by the generations' population key cells (the account's corrected population "
    + "shares, the p of the union's formula; no age cut)",
  pension_union_rules: "pension: the union's ratio_net on each generation's OASDI receipts (the payload's literal rule), Part A by HI "
    + "receipts, the benefit tax by the social_security key",
  part_a_lane_shares: "pension Part A: the pension lane's Part A accruals by generation as fixed shares of the union's (its own HI tax "
    + "base, not the account's HI receipts; the same shares under both allocations)",
};
// The alternatives that move only the pension switch (none applies to the cash set).
const PENSION_ALTERNATIVES = ["pension_union_rules", "part_a_lane_shares"];
function split(C, opts) {
  const { gens, top, models27, fitBy, tenant, persons5, union } = opts;
  const alt = new Set(opts.alt || []);
  for (const x of alt) if (!ALTERNATIVES[x]) throw new Error(`unknown alternative ${x}`);
  const perGen = (f) => Object.fromEntries(gens.map((g) => [g, f(g)]));
  const total = (by) => byAlloc((a) => sum(gens.map((g) => by[g][a])));
  // Item 5, personal property: the licence line (adults key) of the September 27 models, or the population key.
  const lic = perGen((g) => (alt.has("vehicles_by_population") ? P.populationShare(models27[g]) : V4.refAmount(models27[g], LICENCES)));
  const licU = total(lic);
  const vehicle = perGen((g) => byAlloc((a) => C.items.personal.share * lic[g][a] / licU[a]));
  // Roads: the generations' persons aged 5 and over (row-4 weights), or the alternative, their population key cells.
  const w = perGen((g) => (alt.has("roads_by_population") ? P.populationShare(models27[g]) : byAlloc(() => persons5[g])));
  const W = total(w);
  const sv = perGen((g) => byAlloc((a) => union.sbar[a] * w[g][a] / W[a]));
  const A = perGen((g) => chainA(models27[g], { fit_by: fitBy[g], tenant_share: tenant[g], vehicle_share: vehicle[g], svmt: () => sv[g] }, C));
  const out = { vehicle, s_vmt: sv, fit_by: fitBy, tenant, pension: null };
  let final = perGen((g) => A[g].m);
  if (C.pension) {
    const pi = pensionInputs();
    const oasdi = perGen((g) => V4.oasdiOf(A[g].m)), hi = perGen((g) => V4.hiOf(A[g].m)), ks = perGen((g) => ssKey(A[g].m));
    const oasdiU = total(oasdi), hiU = total(hi), ksU = total(ks);
    const inTop = (T) => gens.filter((g) => top[g] === T);
    const within = (x, g) => byAlloc((a) => x[g][a] / sum(inTop(top[g]).map((h) => x[h][a])));
    let refs;
    if (alt.has("pension_union_rules")) {
      refs = perGen((g) => ({ oasdi: oasdi[g], partAScale: byAlloc((a) => hi[g][a] / hiU[a]), fitScale: byAlloc((a) => ks[g][a] / ksU[a]) }));
    } else {
      // OASDI and Part A alike: the generation's accrual per tax dollar (the pension lane's) on its own receipts in the
      // account at the allocation, normalized to the union's accrual.
      const wt = perGen((g) => byAlloc((a) => pi.net_ratio[top[g]] * oasdi[g][a]));
      const Wt = total(wt);
      const wa = perGen((g) => byAlloc((a) => pi.part_a_per_hi_tax[top[g]] * hi[g][a]));
      const Wa = total(wa);
      const paT = sum(pi.gens.map((T) => pi.part_a[T]));
      refs = perGen((g) => ({ oasdi: byAlloc((a) => oasdiU[a] * wt[g][a] / Wt[a]),
        partAScale: alt.has("part_a_lane_shares") ? byAlloc((a) => pi.part_a[top[g]] / paT * within(hi, g)[a]) : byAlloc((a) => wa[g][a] / Wa[a]),
        fitScale: byAlloc((a) => pi.benefit_tax[a][top[g]] / sum(pi.gens.map((T) => pi.benefit_tax[a][T])) * within(ks, g)[a]) }));
    }
    final = perGen((g) => pensionStep(A[g].m, refs[g]));
    out.pension = { refs, oasdi, oasdi_union: oasdiU, hi, ks };
  }
  const tails = perGen((g) => tailOf(final[g], models27[g], C.scales));
  return Object.assign(out, { A, final, tails });
}

// Gates of a split against the union: every cell edit, receipt-line cell and synthetic amount adds up; each generation
// carries exactly the union's lines. Returns the worst differences.
function additivity(C, gens, tails, union) {
  const want = new Map(union.tail.edits.map((x) => [cid(x), x]));
  const ids = new Set([...want.keys(), ...gens.flatMap((g) => tails[g].edits.map(cid))]);
  let edits = 0;
  for (const id of ids) {
    for (const a of ALLOCS) {
      const s = sum(gens.map((g) => { const x = tails[g].edits.find((y) => cid(y) === id); return x ? x.by[a] : 0; }));
      edits = Math.max(edits, Math.abs(s - (want.has(id) ? want.get(id).by[a] : 0)));
    }
  }
  let rl = 0;
  for (const l of union.tail.receipt_lines) {
    for (const sc of Object.keys(l.cells)) for (const a of ALLOCS) {
      const s = sum(gens.map((g) => tails[g].receipt_lines.find((x) => x.id === l.id).cells[sc][a].target_bn));
      rl = Math.max(rl, Math.abs(s - l.cells[sc][a].target_bn));
    }
  }
  const sameLines = gens.every((g) => JSON.stringify(tails[g].lines) === JSON.stringify(union.tail.lines)
    && tails[g].receipt_lines.map((l) => l.id).join() === union.tail.receipt_lines.map((l) => l.id).join());
  return { edits, receipt_lines: rl, sameLines, cells: ids.size };
}

// A generation's full payload: its September 27 payload, then the case's scales and its tail; its production grid.
function payloadOf(C, p27, tail, grid) {
  const p = { receipt_lines: tail.receipt_lines, lines: p27.lines.concat(tail.lines), edits: p27.edits.concat(C.scales, tail.edits) };
  if (grid) p.production = grid;
  return p;
}
function gridOf(C, series) {
  if (!C.production) return null;
  const n = C.production.private_wtp_bn.length;
  if (series.P.length !== n || series.F.length !== n) throw new Error("[BLOCKED] a generation's production series is not the case's grid");
  return { dims: C.production.dims, private_wtp_bn: series.P, induced_receipts_bn: series.F, sampling_se_bn: new Array(n).fill(null) };
}

// ---------------------------------------------------------------------------------------------------
// The evaluator: consumer.cjs on any model (the payload's correction lines at zero where the model lacks them; the
// responses of receipt lines the model lacks dropped). evaluateFull(m, spec) -> {evaluation, capital, cost_bn}; capital
// components carry the payload's part (group) and level.
function evaluator(payload) {
  const Eng = Engine;
  const specs = Consumer.specifications(Eng, MODEL, payload);
  const comps = payload.meta.capital_return.components;
  const receiptIds = Object.entries(payload.meta.responses).filter(([, e]) => e && typeof e === "object" && e.receipt === true).map(([id]) => id);
  const cache = new WeakMap();
  function prepared(m0) {
    if (cache.has(m0)) return cache.get(m0);
    const missing = payload.lines.filter((l) => !m0.spending.lines.some((x) => x.id === l.id));
    const m = missing.length ? Engine.applyCorrections(m0, { lines: missing, edits: [] }) : m0;
    const lacks = receiptIds.filter((id) => !m.receipts.lines.some((l) => l.id === id));
    const pl = lacks.length ? Object.assign({}, payload, { meta: Object.assign({}, payload.meta,
      { responses: Object.fromEntries(Object.entries(payload.meta.responses).filter(([id]) => !lacks.includes(id))) }) }) : payload;
    const r = { m, pl };
    cache.set(m0, r);
    return r;
  }
  function evaluateFull(m0, spec) {
    const { m, pl } = prepared(m0);
    const state = Consumer.stateOf(Eng, m, pl, spec);
    const evaluation = Eng.evaluate(m, state);
    const cap = Consumer.capitalOf(evaluation, payload, spec);
    const components = cap.components.map((c, i) => {
      if (comps[i].id !== c.id) throw new Error("[BLOCKED] capital components out of order");
      return Object.assign({ group: comps[i].part, level: comps[i].level }, c);
    });
    return { evaluation, state, capital: { components, total_bn: cap.total_bn }, cost_bn: -evaluation.welfare_bn + cap.total_bn };
  }
  return { specs, evaluateFull, cost: (m, spec) => evaluateFull(m, spec).cost_bn };
}

// The adopted lane's own package on the case's payload (its evaluateFull, as the case's other consumers call it), to
// cross-check evaluator() on every model a runner costs; null while V4_LANE is the candidate.
function adoptedPackage(C) {
  if (V4_LANE !== ADOPTED) return null;
  const AP = require(path.join(FISCAL, ADOPTED, "package.cjs"));
  const api = C.set === "set" ? AP : AP.forPayload(C.payload);
  if (JSON.stringify(api.correctionsPayload()) !== JSON.stringify(C.payload)) throw new Error(`[BLOCKED] ${ADOPTED}/package.cjs: its ${C.set} payload is not ${C.rel}`);
  return { source: `${ADOPTED}/package.cjs${C.set === "set" ? "" : " forPayload(cash)"}`, specs: api.MAIN_SPECS,
    cost: (m, i) => api.evaluateFull(m, api.MAIN_SPECS[i], api.MAIN_PROFILE).cost_bn };
}

// The case's own ends and band on the union (the methods' mean payload on model.json).
function bandOf(ev, m) {
  const costs = ev.specs.map((s) => ev.cost(m, s));
  const lo = costs.indexOf(Math.min(...costs)), hi = costs.indexOf(Math.max(...costs));
  return { costs, lo, hi, band: [costs[lo], costs[hi]] };
}
// The oracle: the lane's published band for the set or the cash set (four decimals), its end specifications, and the
// uncorrected model's band at the case's responses where the lane publishes one (the same for both sets).
function oracle(set) {
  if (V4_LANE === CANDIDATE) {
    const r = csvRows(`${V4_LANE}/derived/bands.csv`).find((x) => x.case === set && x.method === "mean");
    if (!r) throw new Error(`[BLOCKED] ${V4_LANE}/derived/bands.csv has no ${set} mean row`);
    return { source: `${V4_LANE}/derived/bands.csv (${set}, mean)`, specs: [Number(r.own_low_spec), Number(r.own_high_spec)],
      band: [Number(r.own_low_bn), Number(r.own_high_bn)], uncorrected: null };
  }
  if (V4_LANE === ADOPTED) {
    const variant = set === "set" ? "adopted" : "cash_set";
    const rows = csvRows(`${V4_LANE}/derived/main_case_bands.csv`).filter((x) => x.profile === P.MAIN_PROFILE);
    const r = rows.find((x) => x.variant === variant), u = rows.find((x) => x.variant === "uncorrected_at_adopted_responses");
    const S = readJson(`${V4_LANE}/derived/summary.json`);
    const ends = set === "set" ? S.end_specifications.map((x) => [x.low_end.index, x.high_end.index]) : S.cash_set.end_specifications;
    if (!r || !u || !ends.length || !ends.every((x) => x[0] === ends[0][0] && x[1] === ends[0][1])) {
      throw new Error(`[BLOCKED] ${V4_LANE}: no ${variant} and uncorrected rows in main_case_bands.csv, or the methods' ends differ`);
    }
    return { source: `${V4_LANE}/derived/main_case_bands.csv (${variant})`, specs: ends[0].map(Number),
      band: [Number(r.cost_low_bn), Number(r.cost_high_bn)], uncorrected: [Number(u.cost_low_bn), Number(u.cost_high_bn)] };
  }
  throw new Error(`[BLOCKED] no oracle rule for ${V4_LANE}`);
}
// The lane's cost at every specification, the mean of the two fill-in methods ({source, cost: Map spec -> bn}), or
// null where it publishes none for the set.
function perSpec(set) {
  const mean = (rows, col) => {
    const out = new Map();
    for (const i of [...new Set(rows.map((r) => Number(r.spec)))]) {
      const rs = rows.filter((r) => Number(r.spec) === i);
      if (rs.length !== METHODS.length || !METHODS.every((m) => rs.some((r) => r.method === m))) throw new Error(`[BLOCKED] spec ${i}: not one row per method`);
      out.set(i, sum(rs.map((r) => Number(r[col]))) / rs.length);
    }
    return out;
  };
  if (V4_LANE === CANDIDATE) {
    const col = set === "set" ? "set_cost_bn" : "cash_cost_bn";
    return { source: `${V4_LANE}/derived/per_spec.csv ${col}`, cost: mean(csvRows(`${V4_LANE}/derived/per_spec.csv`), col) };
  }
  if (V4_LANE === ADOPTED) {
    if (set !== "set") return null;
    return { source: `${V4_LANE}/derived/per_spec.csv cost_bn`, cost: mean(csvRows(`${V4_LANE}/derived/per_spec.csv`), "cost_bn") };
  }
  throw new Error(`[BLOCKED] no per-specification rule for ${V4_LANE}`);
}

// The item each response and capital component of the payload belongs to (payload.cjs RESPONSE_NOTES, capitalOf).
const RESPONSE_ITEM = { housing_enterprise_surplus: "1", modeled_owner_property: "5", tenant_occupied_property: "5", personal_property_tax: "5",
  roads_vmt_sl: "roads", roads_vmt_fed: "roads", state_price_public_order_safety: "state", state_price_health_services: "state",
  state_price_recreation_culture: "state" };
const CAPITAL_ITEM = { ent_housing_sl: "4", hwy_sl: "roads", hwy_fed: "roads" };
const ITEMS = ["1", "2", "3", "4", "5", "6a", "7", "roads", "state", "pension"];
// The payload with only the items up to and including `upto` (order ITEMS): the September 27 meta's responses and
// capital components, plus the case's for those items. Used to cost each step of a model's chain.
function metaUpTo(C, upto) {
  const k = ITEMS.indexOf(upto);
  const on = (it) => ITEMS.indexOf(it) <= k;
  const m27 = C.base.meta, m4 = C.payload.meta;
  const responses = {};
  for (const [id, e] of Object.entries(m4.responses)) {
    if (id in m27.responses) responses[id] = m27.responses[id];
    else if (!RESPONSE_ITEM[id]) throw new Error(`[BLOCKED] no item for the response ${id}`);
    else if (on(RESPONSE_ITEM[id])) responses[id] = e;
  }
  const components = m4.capital_return.components.map((c, i) => {
    const c27 = m27.capital_return.components[i];
    if (c27.id !== c.id) throw new Error("[BLOCKED] capital components out of order");
    if (JSON.stringify(c27) === JSON.stringify(c)) return c;
    if (!CAPITAL_ITEM[c.id]) throw new Error(`[BLOCKED] no item for the capital component ${c.id}`);
    return on(CAPITAL_ITEM[c.id]) ? c : c27;
  });
  const capital_return = Object.assign({}, m4.capital_return, { components });
  return Object.assign({}, C.payload, { meta: Object.assign({}, m4, { responses, capital_return }) });
}

module.exports = { V4_LANE, CANDIDATE, ADOPTED, V4, P, Engine, MODEL, ALLOCS, METHODS, FIT, ALTERNATIVES, PENSION_ALTERNATIVES, ITEMS,
  RESPONSE_ITEM, CAPITAL_ITEM, loadCase, chainA, pensionStep, tailOf, cid, unionRun, pensionInputs, split, additivity, payloadOf, gridOf,
  evaluator, adoptedPackage, bandOf, oracle, perSpec, metaUpTo, readJson, byAlloc, lineOf, sum };
