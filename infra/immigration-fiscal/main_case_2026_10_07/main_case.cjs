/* Main case v6, adopted 2026-10-07 (decisions/2026-10-07-main-case-v6.md): main case v5
 * (main_case_2026_10_05) plus the items of package.cjs's registry, written to v5's output contract
 * (main_case_2026_10_05/derived: main_case_bands.csv, components.csv, per_spec.csv, summary.json, corrections.json and
 * corrections_cash.json here; sign_reversal.cjs writes sign_reversal.csv). package.cjs holds the definitions; this
 * script runs the gates and writes derived/.
 *
 * The script is v5's main_case.cjs with the items added: with --items none (the case with no item) it runs v5's code
 * and must write v5's files byte for byte (zero_items.cjs checks it). With items, every v5 file, column, row name and
 * key is kept, with v6's value where the quantity is defined on v6. The rows and keys that record how earlier cases
 * were built keep v5's values (history), and v5's own block (summary.json v5) is history too. One block moves, as on
 * October 5: change_at_fixed_specifications holds v6's change from v5, by item, part and interaction, so v5's (the
 * lineage line's parts, with the September 29 case's under them) sits under change_at_fixed_specifications.oct05_case.
 * Added: the band rows oct05_case and oct05_cash_set and, for every arm of every applied item, the case at that arm
 * (<item>_<arm>, and <item>_<arm>_cash_set where the item enters the cash set), and the companion readings
 * (lineage_<option> and ancestry_share_<scenario>, each with _cash_set: the lineage at the count's arms a and c and at
 * C3 -/+ 1 SE, package.cjs caseOf's fourth argument and lineage_count.cjs, and the count by share of Mexican-immigrant
 * ancestry, ancestry_share.cjs; summary.json v6.companions); the summary keys adopted_2026_10_05,
 * cash_set.change_from_the_october_5_cash_set_bn, each_addition.<item>, range.items_at_the_case_data,
 * beside_the_account.congestion.not_recomputed_v6, group_receipts_bn.adopted_2026_10_05 and v6; per_spec.csv's columns
 * oct05_cost_bn, item_<id>_bn and items_interaction_bn; meta.items in both payloads; with a lineage item,
 * derived/lineage_payload.json and lineage_payload_cash.json (its additions, which meta.lineage.payload names).
 *
 * Gates (exit 1 and nothing written on failure). With items, v5's gates that compare the case with the lineage lane
 * run on v5, and:
 *   G1  v5 re-derives (its package gives v5's per_spec.csv cost at every specification and method, its band and cash
 *       set, exactly); the set is v5 plus the items' change at every one of the 64 specifications, the methods' mean
 *       (1e-9), the change being consumer.cjs on v6's payload less consumer.cjs on v5's, and the cash set likewise; the
 *       ends are found by the methods (each method's own minimum and maximum over the 64); each item alone on v5 is
 *       its source lane's band, set and cash set, with the same ends (1e-9; retiree_health's consumer run is the
 *       lane's own route at all 64 specifications, exactly; added_age_mix's parts, run one part model at a time as the
 *       lane prices them, add to its change at every specification); the pairwise interactions are run, the pension
 *       item's with the lineage item equal to its rebuilt edits' move, and what the pairs leave is zero; the payload
 *       models give the methods' mean (1e-9), and so does consumer.cjs (engine.js, model.json and the payload, no
 *       package); v6's payload model is model.json with the September 29 payload, the lineage addition and the edit
 *       sets' edits applied in turn, exactly;
 *   and the payload is v5's with the lineage item's edits and grid in the lineage's place, the edit sets' edits after
 *       the lineage's, their meta changes and the stamps, nothing else; meta.items locates each item; the pension and
 *       retiree-health blocks read back on the payload models; every arm row is consumer.cjs's band on its payload, and
 *       each arm alone on v5 is its source lane's; each lineage option with no item is the lineage lane's stored v5
 *       value (its arm's band, or arm b's C3 line), and the case at it is consumer.cjs's band, ends 48/11; the count by
 *       ancestry share on v5 is the lineage lane's rows (1e-9).
 * Run from anywhere: node main_case.cjs [--out-dir DIR] [--items none | id,id] -> derived/main_case_bands.csv,
 * components.csv, per_spec.csv, summary.json, corrections.json, corrections_cash.json (and the lineage payloads).
 * --items needs --out-dir.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const argv = process.argv.slice(2);
const PKG = require("./package.cjs");
// --items none: the case with no item (v5's code and files); --items a,b: those items; by default the candidate's.
const ITEMS_ARG = argv.includes("--items") ? argv[argv.indexOf("--items") + 1] : null;
if (ITEMS_ARG !== null && !argv.includes("--out-dir")) throw new Error("[BLOCKED] --items needs --out-dir: its files are not this lane's");
const P = ITEMS_ARG === null ? PKG : PKG.caseOf(PKG.OCT05, ITEMS_ARG === "none" ? [] : ITEMS_ARG.split(","));
const ON = P.CASE_ITEMS.length > 0;
const Consumer = require(path.join(__dirname, "..", "main_case_candidate_v4_2026_09_29", "consumer.cjs"));
const AS = require("./ancestry_share.cjs");
const { Engine, MODEL, FISCAL, HERE, ALLOCS, METHODS, CAP, PARTS, PROFILES, MAIN_PROFILE, LR_LINES, RENTAL, RATES, ENTERPRISES,
  ENTERPRISES_ALLOWED, ENTERPRISE_LINE, V4PKG: V4, gateState, gate, near, f2, csvRows, readJson, withCentral, specsFor, modelFor,
  evaluateFull, evalPackage, central, correctionsPayload, populationShare, sha256 } = P;
const P4 = P.SEPT29, PC = P.CASH, PC4 = P.SEPT29_CASH;
const B5 = P.OCT05, B5C = P.OCT05_CASH;
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const SEPT29 = "main_case_2026_09_29";
const LINEAGE = P.LINEAGE_LANE;
const CAND = "main_case_candidate_v4_2026_09_29";
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const ex = (x) => x.toExponential(1);
const fx = (x) => x.toFixed(4);
const clone = (x) => JSON.parse(JSON.stringify(x));

const MODELS = METHODS.map((m) => modelFor("central", m, withCentral({})));
const MODELS_LANE = METHODS.map((m) => modelFor("central", m, withCentral({ enterprise_rekey: false })));
const runs = (specs, profile, models, pkg) => (models || MODELS).map((model) => specs.map((spec) => (pkg || P).evaluateFull(model, spec, profile)));
const costsOf = (rs) => rs.map((xs) => xs.map((r) => r.cost_bn));
const ends = (cm) => cm.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
const bandOf = (cm) => [mean(cm.map((xs) => Math.min(...xs))), mean(cm.map((xs) => Math.max(...xs)))];
const atEnds = (idx, f) => [0, 1].map((e) => mean(idx.map((ij, m) => f(m, ij[e]))));
const lineOf = (evaluation, id) => evaluation.spending.find((l) => l.id === id);
const amount = (evaluation, id) => lineOf(evaluation, id).amount_bn;
const national = (evaluation, id) => lineOf(evaluation, id).national_bn;
const responseOf = (evaluation, id) => lineOf(evaluation, id).response;
const receiptOf = (r, id) => r.evaluation.receipts.find((x) => x.id === id);
const capitalWhere = (r, pred) => r.capital.components.filter(pred).reduce((a, c) => a + c.return_bn, 0);
const capitalGroup = (r, part) => capitalWhere(r, (c) => c.group === part);
const byId = (r, id) => capitalWhere(r, (c) => c.id === id);
const esRow = (r) => receiptOf(r, ENTERPRISE_LINE);
const esCost = (r) => -esRow(r).effect_bn;

const s29 = readJson(`${SEPT29}/derived/summary.json`);
const bands29 = csvRows(`${SEPT29}/derived/main_case_bands.csv`);
const ps29 = csvRows(`${SEPT29}/derived/per_spec.csv`);
const payload29 = readJson(`${SEPT29}/derived/corrections.json`);
const cash29 = readJson(`${CAND}/derived/corrections_v4_cash.json`);
const lin = readJson(`${LINEAGE}/derived/v5_summary.json`);
const POP = P.POP;
const ARM = POP.meta.central_arm;
const linSet = lin.sets.set.arms[ARM], linCash = lin.sets.cash.arms[ARM];
const CAPDIR = "capital_return_services_2026_09_27/derived";
const capGaps = csvRows(`${CAPDIR}/gaps.csv`);
const COMPONENTS = P.componentsFor(null);
const row29 = (profile, variant) => {
  const r = bands29.find((x) => x.profile === profile && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] the September 29 bands lack ${profile}/${variant}`);
  return r;
};
// v6: the base's files (v5), read only with items.
const OCT05 = "main_case_2026_10_05";
const s5 = ON ? readJson(`${OCT05}/derived/summary.json`) : null;
const bands5 = ON ? csvRows(`${OCT05}/derived/main_case_bands.csv`) : null;
const ps5 = ON ? csvRows(`${OCT05}/derived/per_spec.csv`) : null;
const payload5 = ON ? readJson(`${OCT05}/derived/corrections.json`) : null;
const cashPayload5 = ON ? readJson(`${OCT05}/derived/corrections_cash.json`) : null;
const row5 = (profile, variant) => {
  const r = bands5.find((x) => x.profile === profile && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] v5's bands lack ${profile}/${variant}`);
  return r;
};
const APPLIED = ON ? P.CASE_ITEMS.filter((r) => r.applied) : [];
const APPLIED_CASH = ON ? PC.CASE_ITEMS.filter((r) => r.applied) : [];
const N5 = ON ? payload5.edits.length : 0, N5C = ON ? cashPayload5.edits.length : 0;
const editsOf = (r) => P.ITEM_EDITS.slice(r.edits.first - N5, r.edits.first - N5 + r.edits.count);
// The base the edit sets build on (v5, or v5 with the lineage item's addition), and v5's own addition.
const IB = P.ITEM_BASE, IBC = IB.CASH, LIN_ITEM = ON ? P.LINEAGE_ITEM : null;
const ADD5 = ON ? B5.ADDITION : P.ADDITION;
const inCash = (id) => APPLIED_CASH.some((r) => r.id === id);
const payload = correctionsPayload();
const cashPayload = PC.correctionsPayload();

// ---------------------------------------------------------------------------------------------------
console.log(ON ? "[G1: v5 and the items' change]" : "[G1: the lineage lane's bands]");
const specs = P.MAIN_SPECS;
const newRuns = runs(specs);
const newCosts = costsOf(newRuns);
const newEnds = ends(newCosts);
const C = central({});
const ownBands = (cm) => cm.map((xs) => [Math.min(...xs), Math.max(...xs)]);
function bandGates(name, band, cm, endIdx, want) {
  gate(`${name}: the two methods' mean is the lineage lane's arm ${ARM} band (v5_summary.json, 1e-9)`,
    [0, 1].every((e) => near(band[e], want.band_bn[e], 1e-9)), `${f2(band)} against ${f2(want.band_bn)}`);
  gate(`${name}: the end specifications are 48 / 11 in both methods, as the lineage lane's`,
    endIdx.every((e) => e[0] === 48 && e[1] === 11) && want.ends[0] === 48 && want.ends[1] === 11,
    METHODS.map((m, k) => `${m} ${f2(ownBands(cm)[k])}`).join("; "));
}
if (!ON) bandGates("the set", C, newCosts, newEnds, linSet);
const cashModels = METHODS.map((m) => PC.modelFor("central", m, PC.withCentral({})));
const cashRuns = runs(PC.MAIN_SPECS, MAIN_PROFILE, cashModels, PC);
const cashCosts = costsOf(cashRuns);
const cashEnds = ends(cashCosts);
const Ccash = PC.central({});
if (!ON) bandGates("the cash set", Ccash, cashCosts, cashEnds, linCash);
// v6: the base is v5, and the case is v5 plus the items' change at every specification.
let baseModels = null, baseRuns = null, baseCosts = null, C5 = null, C5cash = null, change = null, cashChange = null, aloneCosts = null;
let alone = null, pairs = null, residual = null, cashResidual = null, agePartsAt = null, c5 = null, cc5 = null, baseCash = null, baseCashRuns = null;
const consumerCosts = (pl) => Consumer.evaluateAll(JSON.parse(JSON.stringify(pl)), { engine: Engine, model: MODEL }).map((x) => x.cost_bn);
const withEdits = (pl, edits) => Object.assign(JSON.parse(JSON.stringify(pl)), { edits: pl.edits.concat(JSON.parse(JSON.stringify(edits))) });
const spanOf = (xs) => [Math.min(...xs), Math.max(...xs)];
const caseRuns = (Q, set) => { const X = set === "cash" ? Q.CASH : Q; return runs(X.MAIN_SPECS, MAIN_PROFILE, METHODS.map((m) => X.modelFor("central", m, X.withCentral({}))), X); };
if (ON) {
  baseModels = METHODS.map((m) => B5.modelFor("central", m, B5.withCentral({})));
  baseRuns = runs(specs, MAIN_PROFILE, baseModels, B5);
  baseCosts = costsOf(baseRuns);
  C5 = B5.central({});
  C5cash = B5C.central({});
  baseCashRuns = caseRuns(B5, "cash");
  baseCash = costsOf(baseCashRuns);
  gate("the base is v5: its package gives v5's per_spec.csv cost at every specification and method, and v5's band and cash set (summary.json), exactly",
    METHODS.every((meth, k) => specs.every((_, i) => String(baseCosts[k][i]) === ps5.find((r) => r.method === meth && Number(r.spec) === i).cost_bn))
    && C5[0] === s5.main_case[0] && C5[1] === s5.main_case[1] && C5cash[0] === s5.cash_set.band_bn[0] && C5cash[1] === s5.cash_set.band_bn[1],
    `${f2(C5)}; cash ${f2(C5cash)}`);
  gate("the base's specifications are v5's, and its payloads are v5's derived files", JSON.stringify(B5.MAIN_SPECS) === JSON.stringify(specs)
    && JSON.stringify(B5.correctionsPayload()) === JSON.stringify(payload5) && JSON.stringify(B5C.correctionsPayload()) === JSON.stringify(cashPayload5));
  c5 = consumerCosts(payload5); cc5 = consumerCosts(cashPayload5);
  const c6 = consumerCosts(payload), cc6 = consumerCosts(cashPayload);
  change = c6.map((x, i) => x - c5[i]);
  cashChange = cc6.map((x, i) => x - cc5[i]);
  const atSpec = specs.map((_, i) => mean(newCosts.map((xs, m) => xs[i] - baseCosts[m][i])));
  const g = worst(atSpec.map((x, i) => x - change[i]));
  gate("the set is v5 plus the items' change at every one of the 64 specifications (the methods' mean; the change is consumer.cjs on v6's payload less on v5's; 1e-9)",
    specs.length === 64 && g < 1e-9, `max |diff| ${ex(g)}; change ${f2(spanOf(change))} over the specifications`);
  const cg = worst(PC.MAIN_SPECS.map((_, i) => mean(cashCosts.map((xs, m) => xs[i] - baseCash[m][i])) - cashChange[i]));
  gate("the cash set is v5's plus the cash items' change at every specification (consumer.cjs on v6's cash payload less on v5's, 1e-9)",
    cg < 1e-9, `max |diff| ${ex(cg)}; change ${f2(spanOf(cashChange))}`);
  gate("the ends, found by the methods: each method's minimum and maximum over the 64 specifications are 48 and 11, in the set and the cash set (v5's are too)",
    newEnds.every((e) => e[0] === 48 && e[1] === 11) && ends(baseCosts).every((e) => e[0] === 48 && e[1] === 11) && cashEnds.every((e) => e[0] === 48 && e[1] === 11),
    METHODS.map((m, k) => `${m} ${f2(ownBands(newCosts)[k])} at ${newEnds[k].join("/")}`).join("; "));
  gate("the band is v5's plus the change at the end specifications (1e-9), and the consumer's band (1e-9); the cash set likewise",
    [0, 1].every((e) => near(C[e], C5[e] + mean(newEnds.map((ij) => change[ij[e]])), 1e-9) && near(C[e], spanOf(c6)[e], 1e-9)
      && near(Ccash[e], C5cash[e] + mean(cashEnds.map((ij) => cashChange[ij[e]])), 1e-9) && near(Ccash[e], spanOf(cc6)[e], 1e-9)), `${f2(C)} = ${f2(C5)} + change`);

  // Each item alone on v5: through the package and through consumer.cjs on its payloads; its bands are its source lane's.
  alone = APPLIED.map((r) => {
    const Q = PKG.caseOf(B5, [r.id]), qc = inCash(r.id);
    const rs = caseRuns(Q, "set"), crs = qc ? caseRuns(Q, "cash") : null;
    return { r, rc: PC.CASE_ITEMS.find((x) => x.id === r.id), Q, runs: rs, costs: costsOf(rs), cashRuns: crs, cashCosts: crs ? costsOf(crs) : null,
      consumer: consumerCosts(Q.correctionsPayload()), cashConsumer: qc ? consumerCosts(Q.CASH_PAYLOAD) : null };
  });
  aloneCosts = alone.map((x) => x.costs);
  for (const x of alone) {
    const id = x.r.id, d = x.consumer.map((v, i) => v - c5[i]);
    const pg = worst(specs.map((_, i) => mean(x.costs.map((xs, m) => xs[i] - baseCosts[m][i])) - d[i]));
    const b = bandOf(x.costs), e = ends(x.costs);
    gate(`item ${id} alone: the package's set is v5's plus consumer.cjs's change at every specification (1e-9); its band is its source lane's (${x.r.source.lane} ${x.r.source_arm}, 1e-9) with the ends ${x.r.source_band_specs.join("/")}`,
      pg < 1e-9 && [0, 1].every((j) => near(b[j], x.r.source_band_bn[j], 1e-9)) && e.every((ij) => ij[0] === x.r.source_band_specs[0] && ij[1] === x.r.source_band_specs[1]),
      `${f2(b)} against ${f2(x.r.source_band_bn)}; max |diff| ${ex(pg)}`);
    if (x.cashCosts) {
      const dc = x.cashConsumer.map((v, i) => v - cc5[i]);
      const pc = worst(PC.MAIN_SPECS.map((_, i) => mean(x.cashCosts.map((xs, m) => xs[i] - baseCash[m][i])) - dc[i]));
      const want = x.r.kind === "lineage" ? x.r.source_cash_band_bn : x.rc.source_band_bn, wantEnds = x.r.kind === "lineage" ? x.r.source_cash_band_specs : x.rc.source_band_specs;
      const bc = bandOf(x.cashCosts), ec = ends(x.cashCosts);
      gate(`item ${id} alone, cash set: the package is v5's plus consumer.cjs's change at every specification (1e-9); its band is its source lane's (1e-9) with the ends ${wantEnds.join("/")}`,
        pc < 1e-9 && [0, 1].every((j) => near(bc[j], want[j], 1e-9)) && ec.every((ij) => ij[0] === wantEnds[0] && ij[1] === wantEnds[1]),
        `${f2(bc)} against ${f2(want)}; max |diff| ${ex(pc)}`);
    }
  }
  const byId_ = (id) => alone.find((x) => x.r.id === id);
  if (byId_("retiree_health")) {
    // The lane's own route: consumer.cjs on v5's payloads with its stored edits appended (case_opeb.cjs runOf).
    const x = byId_("retiree_health"), K = readJson(PKG.OPEB.files.case);
    const lane = consumerCosts(withEdits(payload5, K.arms[x.r.source_arm].case.edits));
    const laneCash = consumerCosts(withEdits(cashPayload5, K.arms[x.r.source_arm].cash.edits));
    gate("item retiree_health alone is the lane's central arm at all 64 specifications on both sets: consumer.cjs on its payloads gives the lane's route (v5's payloads with its stored edits) exactly",
      lane.every((v, i) => v === x.consumer[i]) && laneCash.every((v, i) => v === x.cashConsumer[i]), `${f2(spanOf(lane))}; cash ${f2(spanOf(laneCash))}`);
  }
  if (byId_("added_age_mix")) {
    // The lane's route: one part model at a time (price.cjs caseAt), here through v5's evaluation; its parts at the ends
    // are the lane's change_by_part_bn and its change the lane's change_bn.
    const x = byId_("added_age_mix"), D = P.ITEM_DETAIL.added_age_mix, { later, g3_rate, c3 } = D.counts;
    agePartsAt = {};
    for (const [w, api, ch, src] of [["set", B5, x.consumer.map((v, i) => v - c5[i]), { change: x.r.source_change_bn, parts: x.r.source_change_by_part_bn }],
      ["cash", B5C, x.cashConsumer.map((v, i) => v - cc5[i]), { change: x.r.source_cash_change_bn, parts: x.r.source_cash_change_by_part_bn }]]) {
      const pm = D.part_models[w], sp = api.MAIN_SPECS;
      const cost = Object.fromEntries(Object.entries(pm).map(([k, m]) => [k, sp.map((s) => api.evaluateFull(m, s).cost_bn)]));
      const dG = (k) => sp.map((_, i) => cost[k][i] - cost.identified[i]), dW = sp.map((_, i) => cost.white_g3_rate[i] - cost.white_identified[i]);
      const g3G = dG("g3_rate"), lG = dG("later");
      const parts = {
        g3_rate: sp.map((_, i) => (1 - c3) * g3_rate * g3G[i] + c3 * g3_rate * dW[i]), later: sp.map((_, i) => later * lG[i]),
        g3plus_members: sp.map((_, i) => later * lG[i] + (1 - c3) * g3_rate * g3G[i]), whites: sp.map((_, i) => c3 * g3_rate * dW[i]),
      };
      const sumGap = worst(sp.map((_, i) => parts.g3_rate[i] + parts.later[i] - ch[i]));
      const endGap = worst([0, 1].flatMap((j) => { const i = j ? 11 : 48; return [ch[i] - src.change[j], parts.g3_rate[i] - src.parts[j].g3_rate_bn, parts.later[i] - src.parts[j].later_bn]; }));
      gate(`item added_age_mix alone (${w}): the parts, each part model run on its own as the lane prices them, add to consumer.cjs's change at every one of the 64 specifications (1e-9), and at the ends give the lane's change and its G3-rate and later parts (1e-9)`,
        sumGap < 1e-9 && endGap < 1e-9, `max |diff| ${ex(sumGap)} / ${ex(endGap)}; at the ends G3-rate ${f2([parts.g3_rate[48], parts.g3_rate[11]])}, later ${f2([parts.later[48], parts.later[11]])}`);
      agePartsAt[w] = { parts, worst_sum_gap_bn: sumGap, worst_end_gap_bn: endGap };
    }
  }
  if (byId_("user_fees")) {
    // The lane's route: every part but transit at each of its 64 specifications (case_oct05.csv: total_change_bn less
    // key_transit_bn and capital_transit_bn), and at its ends (case_oct05.json); the folded terms, the carriers and the
    // re-keyed capital read back on the item's own runs.
    const x = byId_("user_fees"), D = P.ITEM_DETAIL.user_fees, rc = x.rc;
    const d = x.consumer.map((v, i) => v - c5[i]), dc = x.cashConsumer.map((v, i) => v - cc5[i]);
    const g = worst(d.map((v, i) => v - D.set.per_spec_change_bn[i])), gc = worst(dc.map((v, i) => v - D.cash.per_spec_change_bn[i]));
    gate("item user_fees alone is the lane's every part but transit at all 64 specifications on both sets: consumer.cjs's change is case_oct05.csv's total_change_bn less key_transit_bn and capital_transit_bn (1e-9; the file keeps 12 digits)",
      g < 1e-9 && gc < 1e-9, `max |diff| ${ex(g)} / ${ex(gc)}`);
    const want = x.r.source_change_bn, wantC = rc.source_change_bn;
    gate(`item user_fees alone at the ends 48 / 11 changes the set by ${want.map((v) => v.toFixed(6)).join(" / ")} and the cash set by ${wantC.map((v) => v.toFixed(6)).join(" / ")}: case_oct05.json's engine lines without key_transit plus k12_weight_bn, capital_college_bn and capital_k12_bn (1e-6, as the brief asks; met to ${ex(Math.max(...[0, 1].map((e) => Math.max(Math.abs(d[[48, 11][e]] - want[e]), Math.abs(dc[[48, 11][e]] - wantC[e])))))}), and 48 / 11 stay the lowest and highest costs`,
      [0, 1].every((e) => near(d[[48, 11][e]], want[e], 1e-6) && near(dc[[48, 11][e]], wantC[e], 1e-6))
      && JSON.stringify([x.consumer, x.cashConsumer].map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))])) === "[[48,11],[48,11]]",
      `set ${f2([d[48], d[11]])}, cash ${f2([dc[48], dc[11]])}`);
    // The K-12 weight's two parts at row 6's lines' responses are the lane's A + B s at the education line's response.
    const AB = D.set.A_B;
    let wGap = 0;
    for (const xs of x.runs) xs.forEach((r, i) => {
      const s = specs[i], ab = AB[s.allocation], ev = r.evaluation;
      const folded = (ab.A + ab.B) * responseOf(ev, "school_reprice") + ab.A * responseOf(ev, "college_rekey");
      wGap = Math.max(wGap, Math.abs(folded - (ab.A + ab.B * s.share) * responseOf(ev, "education_services")));
    });
    gate("the K-12 weight as row 6's re-blend: its school part A + B at school_reprice's response and its other part A at college_rekey's give the lane's (A + B s) x the education line's response at every specification and method (1e-12; the school response is 1)",
      wGap < 1e-12 && specs.every((s) => s.school === 1), `max |diff| ${ex(wGap)}`);
    // The carriers respond at 0, add nothing, and their amounts are below a dollar; the re-keyed keys are v5's plus the
    // lane's key change (college, k12) and v5's (health) on both sets.
    const carriers = rc.capital.receipt_lines.concat(x.r.capital.receipt_lines);
    let carrierOk = true, keyGap = 0;
    for (const [xr, br] of [[x.runs, baseRuns], [x.cashRuns, baseCashRuns]]) xr.forEach((xs, m) => xs.forEach((r, i) => {
      for (const id of carriers) { const row = receiptOf(r, id); carrierOk = carrierOk && row && row.response === 0 && row.effect_bn === 0 && Math.abs(row.amount_bn) < 1e-9; }
      for (const c of COMPONENTS.filter((y) => y.of_component)) {
        const k = (rr, id) => (rr.capital.components.find((y) => y.id === id) || { key: 0 }).key;
        const dk = D.set.delta[c.of_component] ? D.set.delta[c.of_component][specs[i].allocation] : 0;
        keyGap = Math.max(keyGap, Math.abs(k(r, c.of_component) + k(r, c.id) - k(br[m][i], c.of_component) - dk));
      }
    }));
    gate("item user_fees's carriers respond at 0 and add nothing at every specification, method and set (their amounts below a dollar), and each re-keyed component with its offset has v5's key plus the lane's key change (college and k12; 0 for health_sl and health_fed), 1e-12",
      carrierOk && keyGap < 1e-12, `${carriers.length / 2} carriers; max key |diff| ${ex(keyGap)}`);
  }
  // Interactions: every pair of items on v5, and what the pairs leave of the case's change.
  const aloneChange = (x, set) => (set === "cash" ? (x.cashConsumer ? x.cashConsumer.map((v, i) => v - cc5[i]) : specs.map(() => 0)) : x.consumer.map((v, i) => v - c5[i]));
  pairs = [];
  for (let a = 0; a < alone.length; a += 1) for (let b = a + 1; b < alone.length; b += 1) {
    const X = alone[a], Y = alone[b], Q = PKG.caseOf(B5, [X.r.id, Y.r.id]);
    const pc = consumerCosts(Q.correctionsPayload()), pcc = consumerCosts(Q.CASH_PAYLOAD);
    const ax = aloneChange(X), ay = aloneChange(Y), axc = aloneChange(X, "cash"), ayc = aloneChange(Y, "cash");
    pairs.push({ ids: [X.r.id, Y.r.id], Q, set: pc.map((v, i) => v - c5[i] - ax[i] - ay[i]), cash: pcc.map((v, i) => v - cc5[i] - axc[i] - ayc[i]) });
  }
  residual = change.map((v, i) => v - alone.reduce((s, x) => s + aloneChange(x)[i], 0) - pairs.reduce((s, q) => s + q.set[i], 0));
  cashResidual = cashChange.map((v, i) => v - alone.reduce((s, x) => s + aloneChange(x, "cash")[i], 0) - pairs.reduce((s, q) => s + q.cash[i], 0));
  const pairOf = (a, b) => pairs.find((q) => q.ids[0] === a && q.ids[1] === b);
  const p12 = pairOf("pension_tr2026", "retiree_health");
  if (p12) gate("pension_tr2026 and retiree_health add with no interaction at every specification, set and cash (1e-9): they edit different lines and no capital key reads social security or Medicare",
    worst(p12.set) < 1e-9 && worst(p12.cash) < 1e-9, `max |interaction| ${ex(worst(p12.set))} / ${ex(worst(p12.cash))}`);
  const p13 = pairOf("pension_tr2026", "added_age_mix");
  if (p13) {
    // The pension item's edits rebuilt on the age-mix base move by (f - 1) x the added people's change in Social
    // Security and Part A; the two lines respond at 1 on their keys, so that move is the interaction.
    const e13 = p13.Q.ITEM_EDITS, e5 = alone.find((x) => x.r.id === "pension_tr2026").Q.ITEM_EDITS;
    const want = specs.map((s) => e13.reduce((t, e, k) => t + e.by[s.allocation] - e5[k].by[s.allocation], 0));
    const resp = newRuns.every((xs) => xs.every((r) => ["social_security", "medicare"].every((id) => { const row = lineOf(r.evaluation, id); return row.response === 1 && row.key === id; })));
    gate("pension_tr2026 with added_age_mix: the interaction is the pension edits' move between v5's added people and the age mix's ((f - 1) x their Social Security and Part A), at every specification (1e-9); the cash set has none",
      resp && worst(p13.set.map((v, i) => v - want[i])) < 1e-9 && worst(p13.cash) < 1e-9, `${f2(spanOf(p13.set))}; max |diff| ${ex(worst(p13.set.map((v, i) => v - want[i])))}`);
  }
  const p4 = pairs.filter((q) => q.ids.includes("user_fees"));
  if (p4.length) gate(`user_fees adds to each other item with no interaction at every specification, set and cash (1e-9): its edits are fixed amounts on lines the others scale or leave alone, its carriers cancel its own move of the capital keys on the model it applies to, and its terms are the union's, so the added people's amounts and the other items' do not enter them`,
    p4.every((q) => worst(q.set) < 1e-9 && worst(q.cash) < 1e-9), p4.map((q) => `${q.ids.join(" x ")} ${ex(worst(q.set))} / ${ex(worst(q.cash))}`).join("; "));
  gate("what the pairs leave of the case's change is zero at every specification, set and cash (1e-9): no three-way interaction",
    worst(residual) < 1e-9 && worst(cashResidual) < 1e-9, `max ${ex(worst(residual))} / ${ex(worst(cashResidual))}; pairs ${pairs.map((q) => `${q.ids.join(" x ")} ${f2([q.set[48], q.set[11]])}, cash ${f2([q.cash[48], q.cash[11]])}`).join("; ")}`);
}
const methodMean = (cm) => specs.map((_, i) => mean(cm.map((xs) => xs[i])));
const meanSet = methodMean(newCosts), meanCash = methodMean(cashCosts);
const payloadCosts = specs.map((s) => evaluateFull(P.payloadModel(), s).cost_bn);
const cashPayloadCosts = PC.MAIN_SPECS.map((s) => PC.evaluateFull(PC.payloadModel(), s).cost_bn);
const pmGap = worst(payloadCosts.map((x, i) => x - meanSet[i])), pmcGap = worst(cashPayloadCosts.map((x, i) => x - meanCash[i]));
gate("the payload model (engine.js + model.json + corrections.json) gives the methods' mean at every specification, and the band (1e-9)",
  payloadCosts.length === 64 && pmGap < 1e-9 && near(Math.min(...payloadCosts), C[0], 1e-9) && near(Math.max(...payloadCosts), C[1], 1e-9), `max |diff| ${ex(pmGap)}`);
gate("the cash set's payload model gives the cash set's methods' mean at every specification, and its band (1e-9)",
  pmcGap < 1e-9 && near(Math.min(...cashPayloadCosts), Ccash[0], 1e-9) && near(Math.max(...cashPayloadCosts), Ccash[1], 1e-9), `max |diff| ${ex(pmcGap)}`);
const SPEC_FIELDS = ["allocation", "normalization", "share", "school", "gg", "uc", "reading"];
for (const [name, pl, want, sp] of [["corrections.json", payload, meanSet, specs], ["corrections_cash.json", cashPayload, meanCash, PC.MAIN_SPECS]]) {
  const independent = Consumer.evaluateAll(JSON.parse(JSON.stringify(pl)), { engine: Engine, model: MODEL });
  const g = worst(independent.map((x, i) => x.cost_bn - want[i]));
  gate(`consumer.cjs (engine.js, model.json and ${name}, no package) gives the methods' mean at every specification (1e-9): it reads gg, the line responses and the long-run subfunctions from meta.responses`,
    independent.length === 64 && independent.every((x, i) => SPEC_FIELDS.every((f) => x.spec[f] === sp[i][f])) && g < 1e-9, `max |diff| ${ex(g)}`);
}
// The merge is the lineage lane's apply rule: the v4 payload, then the lineage payload.
const twoStep = Engine.applyCorrections(Engine.applyCorrections(MODEL, payload29), ADD5.set);
const merged = ON ? B5.payloadModel() : P.payloadModel();
const strip = (m) => JSON.stringify(Object.assign({}, m, { corrections: null }));
gate(`${ON ? "the base: v5's" : "the merged"} payload's model is model.json with the v4 payload and then the lineage payload applied (lineage lane meta.apply), exactly`,
  strip(merged) === strip(twoStep) && strip(ON ? B5C.payloadModel() : PC.payloadModel()) === strip(Engine.applyCorrections(Engine.applyCorrections(MODEL, cash29), ADD5.cash)));
if (ON) {
  const after = (m, edits, rl) => (edits.length || rl.length ? Engine.applyCorrections(m, { receipt_lines: rl, edits }) : m);
  const three = (base, add, edits, rl) => after(Engine.applyCorrections(Engine.applyCorrections(MODEL, base), add), edits, rl || []);
  gate(`v6's payload models are model.json with the September 29 payloads, the lineage addition (${LIN_ITEM ? `item ${LIN_ITEM}'s` : "v5's"}) and the edit sets' edits and carrier lines applied in turn, exactly`,
    strip(P.payloadModel()) === strip(three(payload29, IB.ADDITION.set, P.ITEM_EDITS, P.ITEM_RECEIPT_LINES))
    && strip(PC.payloadModel()) === strip(three(cash29, IB.ADDITION.cash, PC.ITEM_EDITS, PC.ITEM_RECEIPT_LINES))
    && strip(IB.payloadModel()) === strip(three(payload29, IB.ADDITION.set, [])) && strip(IBC.payloadModel()) === strip(three(cash29, IB.ADDITION.cash, [])),
    `${P.ITEM_EDITS.length} set edits, ${PC.ITEM_EDITS.length} cash edits after the lineage's; ${P.ITEM_RECEIPT_LINES.length} carrier lines`);
}

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the payload and the specifications]");
// v5's payload gates run on v5's payload: the payload itself with no item, the base's with items.
const pv5 = ON ? payload5 : payload, cv5 = ON ? cashPayload5 : cashPayload, S5 = ON ? B5 : P;
const metaKeys29 = Object.keys(payload29.meta);
const changed = Object.keys(pv5.meta).filter((k) => JSON.stringify(pv5.meta[k]) !== JSON.stringify(payload29.meta[k]));
const longRun = (K) => K.components.filter((c) => c.response.kind === "long_run_subfunction").map((c) => c.id);
const capMoved = pv5.meta.capital_return.components.filter((c, i) => JSON.stringify(c) !== JSON.stringify(payload29.meta.capital_return.components[i])).map((c) => c.id);
const n29 = payload29.edits.length;
gate(`${ON ? "the base: v5's " : ""}corrections.json is the September 29 corrections.json with the lineage payload merged in: its edits appended, its P and F, its responses, the long-run capital values at them, meta.lineage and the stamps (${S5.STAMPED.join(", ")}); lines, receipt lines and every other meta key identical`,
  JSON.stringify(Object.keys(pv5)) === JSON.stringify(Object.keys(payload29))
  && JSON.stringify(Object.keys(pv5.meta)) === JSON.stringify(metaKeys29.concat(["lineage"]))
  && ["lines", "receipt_lines"].every((k) => JSON.stringify(pv5[k]) === JSON.stringify(payload29[k]))
  && JSON.stringify(pv5.edits) === JSON.stringify(payload29.edits.concat(ADD5.set.edits))
  && JSON.stringify(pv5.production.dims) === JSON.stringify(payload29.production.dims)
  && JSON.stringify(pv5.production.sampling_se_bn) === JSON.stringify(payload29.production.sampling_se_bn)
  && ["private_wtp_bn", "induced_receipts_bn"].every((k) => JSON.stringify(pv5.production[k]) === JSON.stringify(ADD5.set.production[k]))
  && JSON.stringify(pv5.meta.responses) === JSON.stringify(ADD5.set.meta.responses)
  && JSON.stringify(changed.sort()) === JSON.stringify(["adopted", "capital_return", "case", "decision", "lineage", "responses", "source", "status"])
  && JSON.stringify(capMoved) === JSON.stringify(longRun(payload29.meta.capital_return)),
  `${pv5.edits.length} edits (${n29} + ${ADD5.set.edits.length}); meta changed: ${changed.join(", ")}; capital values moved: ${capMoved.join(", ")}`);
gate(`${ON ? "the base: " : ""}meta: adopted ${S5.ADOPTED}, decision ${S5.DECISION}, no "not adopted" left in the case text or status`, pv5.meta.adopted === S5.ADOPTED
  && pv5.meta.decision === S5.DECISION && !/not adopted/.test(pv5.meta.case) && !/not adopted/.test(pv5.meta.status));
const L = payload.meta.lineage, A = POP.arms[ARM];
gate("meta.lineage: the arm, counts, members, C3 and its source are population.json's and the lineage payload's (exact); the added people are G3+, counted whole",
  L.arm === ARM && L.generation === "G3plus" && L.counting.rule === P.COUNTING && P.COUNTING === "whole" && L.counts.added === A.added && L.counts.at_g3_rate === A.g3_rate && L.counts.later_losses === A.later
  && L.counts.lineage_population === A.population && L.counts.account_union === POP.meta.account_union
  && L.c3.value === POP.c3.value && L.c3.se === POP.c3.se && L.c3.label === POP.c3.label && L.c3.source === POP.c3.source && L.c3.override === false
  && L.members.g3plus === P.ADDITION.set.meta.lineage.m_g3plus && L.members.white === P.ADDITION.set.meta.lineage.m_white
  && L.edits.first === n29 && L.edits.count === P.ADDITION.set.edits.length && L.s.v5 === A.s && L.k_metro === A.k_metro,
  `${(L.counts.added / 1e6).toFixed(4)}M added (${(L.counts.at_g3_rate / 1e6).toFixed(4)}M at the G3 rate, ${(L.counts.later_losses / 1e6).toFixed(4)}M later), lineage ${(L.counts.lineage_population / 1e6).toFixed(4)}M; C3 ${L.c3.value} (SE ${L.c3.se}), ${L.c3.source}`);
gate(`${ON ? "the base: v5's " : ""}cash payload is the cash set's v4 payload with the cash lineage payload merged in, the same way, and the same lineage population`,
  JSON.stringify(cv5.edits) === JSON.stringify(cash29.edits.concat(ADD5.cash.edits))
  && JSON.stringify(cv5.meta.responses) === JSON.stringify(ADD5.cash.meta.responses)
  && JSON.stringify(cv5.meta.lineage.counts) === JSON.stringify(L.counts) && JSON.stringify(cv5.meta.lineage.c3) === JSON.stringify(L.c3));
let itemMetaKeys = [];
if (ON) {
  // v6's payloads: v5's first edits (the September 29 payload's), then the lineage block in its place (the lineage
  // item's edits at v5's cells, when it applies, with its grid), then the edit sets' edits, their meta and the stamps.
  const metaKeys = (recs) => recs.filter((r) => r.kind === "edit_set").flatMap((r) => r.meta_changed);
  itemMetaKeys = [...new Set(metaKeys(APPLIED))].sort();
  const diffKeys = (a, b) => Object.keys(a.meta).filter((k) => JSON.stringify(a.meta[k]) !== JSON.stringify(b.meta[k])).sort();
  const cellsSeq = (es) => es.map((e) => [e.side, e.line, e.key, e.scenario].join("|"));
  function framed(pl, pl5, base29, add5, addI, itemEdits, recs, itemLines, itemComps) {
    const n = base29.edits.length, k = add5.edits.length, added = metaKeys(recs).filter((x) => !(x in pl5.meta));
    const changed = diffKeys(pl, pl5), want = [...new Set(P.STAMPED.concat(metaKeys(recs), LIN_ITEM ? ["lineage"] : [], itemComps.length ? ["capital_return"] : []))].sort();
    // An item's capital: its carrier lines after the payload's receipt lines, its components after the payload's.
    const K = clone(pl.meta.capital_return), K5 = pl5.meta.capital_return;
    K.components = K.components.slice(0, K5.components.length);
    const ok = JSON.stringify(Object.keys(pl)) === JSON.stringify(Object.keys(pl5))
      && JSON.stringify(pl.lines) === JSON.stringify(pl5.lines) && JSON.stringify(pl.receipt_lines) === JSON.stringify(pl5.receipt_lines.concat(itemLines))
      && JSON.stringify(K) === JSON.stringify(K5) && JSON.stringify(pl.meta.capital_return.components.slice(K5.components.length)) === JSON.stringify(itemComps)
      && JSON.stringify(Object.keys(pl.meta)) === JSON.stringify(Object.keys(pl5.meta).concat(added, ["items"]))
      && JSON.stringify(pl.edits.slice(0, n)) === JSON.stringify(pl5.edits.slice(0, n)) && JSON.stringify(pl.edits.slice(n, n + k)) === JSON.stringify(addI.edits)
      && JSON.stringify(cellsSeq(addI.edits)) === JSON.stringify(cellsSeq(add5.edits)) && JSON.stringify(addI.edits[k - 1]) === JSON.stringify(add5.edits[k - 1])
      && JSON.stringify(pl.edits.slice(n + k)) === JSON.stringify(itemEdits) && pl5.edits.length === n + k
      && JSON.stringify(Object.keys(pl.production)) === JSON.stringify(Object.keys(pl5.production))
      && ["dims", "sampling_se_bn"].every((x) => JSON.stringify(pl.production[x]) === JSON.stringify(pl5.production[x]))
      && ["private_wtp_bn", "induced_receipts_bn"].every((x) => JSON.stringify(pl.production[x]) === JSON.stringify(addI.production[x]))
      && (LIN_ITEM !== null || (JSON.stringify(addI) === JSON.stringify(add5) && JSON.stringify(pl.production) === JSON.stringify(pl5.production)))
      && JSON.stringify(changed) === JSON.stringify(want);
    return { ok, detail: `${pl.edits.length} edits (${n} + ${k} lineage${LIN_ITEM ? ` from item ${LIN_ITEM}` : ""} + ${itemEdits.length}); meta changed: ${changed.join(", ")}` };
  }
  const fs6 = framed(payload, payload5, payload29, ADD5.set, IB.ADDITION.set, P.ITEM_EDITS, APPLIED, P.ITEM_RECEIPT_LINES, P.ITEM_COMPONENTS);
  gate(`corrections.json is v5's with ${LIN_ITEM ? `item ${LIN_ITEM}'s lineage edits (v5's cells, v5's order, v5's row 8 edit) and grid in the lineage's place, ` : ""}the edit sets' edits after the lineage's, their meta (${itemMetaKeys.join(", ")}), the items' carrier lines after the receipt lines and capital components after the components (${P.ITEM_COMPONENTS.map((c) => c.id).join(", ") || "none"}), and the stamps (${P.STAMPED.join(", ")}); lines, the grid's dimensions and SEs and every other meta key identical`,
    fs6.ok, fs6.detail);
  const fsC = framed(cashPayload, cashPayload5, cash29, ADD5.cash, IB.ADDITION.cash, PC.ITEM_EDITS, APPLIED_CASH, PC.ITEM_RECEIPT_LINES, PC.ITEM_COMPONENTS);
  gate("corrections_cash.json is v5's cash payload built the same way with the cash items", fsC.ok, fsC.detail);
  // The adopted case (every registry item, no arm) takes v5's stamp form; any other item set is a variant.
  const AD = P.ADOPTED, DECISION_FILE = path.resolve(FISCAL, "..", "..", P.DECISION);
  gate(AD ? `meta, both payloads: adopted ${AD}, decision ${P.DECISION} (the file exists), v5's status form ("adopted ${AD} (...)" and "the cash set of the case adopted ${AD} (...)"), and the case text names v6 adopted`
    : `meta, both payloads: a variant (adopted null), decision ${P.DECISION}, status "variant: ...", and the case text names it a variant of v6`,
    (!AD || fs.existsSync(DECISION_FILE)) && [[payload, payload5, `adopted ${AD} (${P.DECISION}): `], [cashPayload, cashPayload5, `the cash set of the case adopted ${AD} (the pension switch off): `]]
      .every(([pl, b, st]) => pl.meta.adopted === (AD || null) && pl.meta.decision === P.DECISION && pl.meta.source === `${P.LANE}/package.cjs`
        && (AD ? pl.meta.status.startsWith(st) && pl.meta.case.startsWith(`${b.meta.case}; v6, adopted ${AD}: `)
          : pl.meta.status.startsWith("variant: ") && pl.meta.case.startsWith(`${b.meta.case}; a variant of v6 (adopted `))),
    AD ? `${path.relative(path.resolve(FISCAL, "..", ".."), DECISION_FILE)} ${fs.existsSync(DECISION_FILE) ? "exists" : "MISSING"}` : "variant");
  // meta.lineage: v5's, but for the payload files and the lineage item's keys; its edits keep their place.
  const lineageAsV5 = (pl, pl5, w) => {
    if (!LIN_ITEM) return JSON.stringify(pl.meta.lineage) === JSON.stringify(pl5.meta.lineage);
    const x = clone(pl.meta.lineage), extra = Object.keys(x).filter((k) => !(k in pl5.meta.lineage));
    if (x.payload !== PKG.LINEAGE_PAYLOADS[w] || !extra.length) return false;
    for (const k of extra) delete x[k];
    x.payload = pl5.meta.lineage.payload;
    return JSON.stringify(x) === JSON.stringify(pl5.meta.lineage);
  };
  gate(`meta.lineage is v5's${LIN_ITEM ? ` but for payload (this lane's derived/lineage_payload*.json) and item ${LIN_ITEM}'s keys (${Object.keys(payload.meta.lineage).filter((k) => !(k in payload5.meta.lineage)).join(", ")})` : ""}: the lineage's edits keep their place (first 416, count 336, row 8 at 751) and the edit sets' follow them`,
    lineageAsV5(payload, payload5, "set") && lineageAsV5(cashPayload, cashPayload5, "cash")
    && L.edits.first + L.edits.count === N5 && L.edits.row8_edit_index === N5 - 1, `row 8 at ${L.edits.row8_edit_index}; ${payload.edits.length} edits`);
  // meta.items: every registry item named, in order; the lineage item locating the lineage block, each applied edit set
  // its edits (which run to the end), its parts adding to them.
  function locates(pl, n, itemEdits) {
    let at = n, ok = true;
    for (const r of pl.meta.items) {
      if (!r.applied) { ok = ok && typeof r.why === "string" && !r.edits; continue; }
      if (r.kind === "lineage") { ok = ok && JSON.stringify(r.lineage_edits) === JSON.stringify(pl.meta.lineage.edits) && !r.edits; continue; }
      const es = itemEdits.slice(r.edits.first - n, r.edits.first - n + r.edits.count);
      ok = ok && r.edits.first === at && JSON.stringify(pl.edits.slice(r.edits.first, r.edits.first + r.edits.count)) === JSON.stringify(es);
      at += r.edits.count;
      const sums = es.map(() => ({ personal: 0, shared: 0 }));
      for (const part of Object.values(r.parts)) for (const a of ALLOCS) sums[part.edit][a] += part.by[a];
      ok = ok && (!Object.keys(r.parts).length || es.every((e, k) => !e.by || ALLOCS.every((a) => sums[k][a] === e.by[a])));
    }
    return ok && at === pl.edits.length && JSON.stringify(pl.meta.items.map((r) => r.id)) === JSON.stringify(P.ITEM_IDS);
  }
  gate("meta.items: both payloads name the items in registry order; the lineage item locates the lineage block, each applied edit set's {first, count} its edits, which run to the end, and its parts add to them exactly",
    locates(payload, N5, P.ITEM_EDITS) && locates(cashPayload, N5C, PC.ITEM_EDITS),
    payload.meta.items.map((r) => `${r.id} ${!r.applied ? "not applied" : r.edits ? `edits ${r.edits.first}-${r.edits.first + r.edits.count - 1}` : `lineage edits ${r.lineage_edits.first}-${r.lineage_edits.first + r.lineage_edits.count - 1}`}`).join("; "));
  if (APPLIED.some((r) => r.id === "pension_tr2026")) {
    // The pension block reads back on the payload models: the union's social_security is ratio_net x its OASDI receipts
    // and its Part A is part_a_accrual_bn; the added people's are the lineage base's times f_ss and f_pa.
    const PA = payload.meta.pension_accrual, PA5 = payload5.meta.pension_accrual, f = PA.lineage_factors;
    const REF = MODEL.receipts.reference;
    const amt = (m, id) => { const l = m.spending.lines.find((x) => x.id === id); return Object.fromEntries(ALLOCS.map((a) => [a, l.keys[l.preferred_key][a].target_bn])); };
    const rec = (m, id) => Object.fromEntries(ALLOCS.map((a) => [a, m.receipts.lines.find((x) => x.id === id).cells[REF][a].target_bn]));
    const m4 = P4.payloadModel(), m5 = IB.payloadModel(), m6 = P.payloadModel(), m4c = PC4.payloadModel(), m5c = IBC.payloadModel();
    const oasdi = Object.fromEntries(ALLOCS.map((a) => [a, PA.oasdi_lines.reduce((s, id) => s + rec(m4, id)[a], 0) + PA.se_oasdi_share * rec(m4, PA.se_line)[a]]));
    const ss = [m4, m5, m6].map((m) => amt(m, "social_security")), mc = [m4, m5, m6].map((m) => amt(m, "medicare"));
    const mcc = [m4c, m5c].map((m) => amt(m, "medicare"));
    const linSS = (a) => ss[1][a] - ss[0][a], linPA = (a) => (mc[1][a] - mc[0][a]) - (1 - PA.part_a_share) * (mcc[1][a] - mcc[0][a]);
    const unionSS = (a) => ss[2][a] - f.f_ss * linSS(a);
    const unionPA = (a) => mc[2][a] - ((mc[1][a] - mc[0][a]) + (f.f_pa - 1) * linPA(a)) - (1 - PA.part_a_share) * mcc[0][a];
    const g1 = Math.max(...ALLOCS.map((a) => Math.abs(unionSS(a) - PA.ratio_net * oasdi[a]))), g2 = Math.max(...ALLOCS.map((a) => Math.abs(unionPA(a) - PA.part_a_accrual_bn)));
    const r = APPLIED.find((x) => x.id === "pension_tr2026");
    const keep = Object.keys(PA5).filter((k) => !["ratio_net", "part_a_accrual_bn", "source", "scheduled_benefits_arm"].includes(k));
    gate("meta.pension_accrual: ratio_net and part_a_accrual_bn are the source arm's; v5's other keys unchanged, its source kept under source.builds_on and previous.oct05; the scheduled-benefits arm flagged as on the 2025 reports",
      PA.ratio_net === r.ratio_net.oct07 && PA.part_a_accrual_bn === r.part_a_accrual_bn.oct07 && PA5.ratio_net === r.ratio_net.oct05
      && keep.every((k) => JSON.stringify(PA[k]) === JSON.stringify(PA5[k])) && JSON.stringify(Object.keys(PA).slice(0, Object.keys(PA5).length)) === JSON.stringify(Object.keys(PA5))
      && JSON.stringify(PA.source.builds_on) === JSON.stringify(PA5.source) && JSON.stringify(PA.previous.oct05.source) === JSON.stringify(PA5.source)
      && PA.scheduled_benefits_arm.ratio_net === PA5.scheduled_benefits_arm.ratio_net && /not recomputed on the 2026 inputs/.test(PA.scheduled_benefits_arm.note)
      && PA.source.sha256 === sha256(PA.source.file) && PA.source.case_sha256 === sha256(PA.source.case_file),
      `ratio_net ${PA5.ratio_net} -> ${PA.ratio_net}; Part A ${PA5.part_a_accrual_bn} -> ${PA.part_a_accrual_bn}bn`);
    gate(`the pension block reads back on the payload model: the union's social_security is ratio_net x its OASDI receipts and its Part A is part_a_accrual_bn; the added people's are ${LIN_ITEM ? "the lineage base's" : "v5's"} times f_ss and f_pa (1e-9)`,
      g1 < 1e-9 && g2 < 1e-9, `max |diff| ${ex(g1)} / ${ex(g2)}; f_ss ${f.f_ss}, f_pa ${f.f_pa}`);
  }
  if (APPLIED.some((r) => r.id === "retiree_health")) {
    // Each edited line's national total is the lineage base's plus the item's change, and every cell of the line scales
    // with it (engine.js scaleLine), on both payload models; meta.retiree_health is one block on both payloads.
    const D = P.ITEM_DETAIL.retiree_health.set, RH = payload.meta.retiree_health;
    // The payload models through this item's edits (a later item's cell shifts move cells of the same lines).
    const upTo = (Q, mB, n0) => { const r = Q.CASE_ITEMS.find((x) => x.id === "retiree_health"); return Engine.applyCorrections(mB, { edits: Q.ITEM_EDITS.slice(0, r.edits.first - n0 + r.edits.count) }); };
    let natGap = 0, cellsSame = true, nCells = 0;
    for (const [m6, mB] of [[upTo(P, IB.payloadModel(), N5), IB.payloadModel()], [upTo(PC, IBC.payloadModel(), N5C), IBC.payloadModel()]]) {
      for (const id of D.lines) {
        const a = m6.spending.lines.find((l) => l.id === id), b = mB.spending.lines.find((l) => l.id === id), f = a.national_bn / b.national_bn;
        natGap = Math.max(natGap, Math.abs(a.national_bn - b.national_bn - D.delta[id]));
        for (const k of Object.keys(b.keys)) for (const al of ALLOCS) { cellsSame = cellsSame && a.keys[k][al].target_bn === b.keys[k][al].target_bn * f; nCells += 1; }
      }
    }
    gate("meta.retiree_health and the payload models: each of the item's lines has the lineage base's national total plus its change (1e-9) and every cell scaled with it (exact), on both sets; the block is the same on both payloads, with mu, rho and the military care of its arm",
      natGap < 1e-9 && cellsSame && JSON.stringify(RH) === JSON.stringify(cashPayload.meta.retiree_health) && RH.arm === "central"
        && near(RH.inputs.mu, 1.813, 5e-4) && near(RH.inputs.rho, 1.1995, 5e-5) && near(RH.inputs.military_retiree_purchased_care_bn, 19.80, 5e-3),
      `${D.lines.length} lines, ${nCells} cells; national change ${RH.national_change_bn.total.toFixed(3)}bn; mu ${RH.inputs.mu.toFixed(4)}, rho ${RH.inputs.rho.toFixed(4)}, military ${RH.inputs.military_retiree_purchased_care_bn.toFixed(2)}bn`);
  }
  if (LIN_ITEM === "added_age_mix") {
    // The lineage block is v5's plus the age-mix deltas of the part models, cell by cell, on both sets (exact); the
    // under-20 shares are age_mix.json's.
    const D = P.ITEM_DETAIL.added_age_mix, { later, g3_rate, c3 } = D.counts, AM = payload.meta.lineage.age_mix;
    const cellMap = (m) => new Map(PKG.AGE_MIX.cellsOf(m).map((c) => [PKG.AGE_MIX.cellId(c), c.cell]));
    let exact = true;
    for (const w of ["set", "cash"]) {
      const pm = Object.fromEntries(Object.entries(D.part_models[w]).map(([k, m]) => [k, cellMap(m)]));
      const a5 = ADD5[w].edits, aI = IB.ADDITION[w].edits;
      for (let k = 0; k < a5.length - 1; k += 1) {
        const e = a5[k], id = `${e.side}|${e.line}|${e.side === "receipt" ? e.scenario : e.key}`;
        for (const al of ALLOCS) {
          const g = pm.identified.get(id)[al].target_bn, wi = pm.white_identified.get(id)[al].target_bn;
          const d = later * (pm.later.get(id)[al].target_bn - g) + (1 - c3) * g3_rate * (pm.g3_rate.get(id)[al].target_bn - g) + c3 * g3_rate * (pm.white_g3_rate.get(id)[al].target_bn - wi);
          exact = exact && aI[k].by[al] === e.by[al] + d;
        }
      }
    }
    const MIX = readJson(PKG.AGE_MIX.FILES.age_mix), u20 = (pi) => MIX.meta.bands.reduce((s, b, k) => s + (Number(b.split(/[-+]/)[0]) < 20 ? pi[k] : 0), 0);
    gate("the lineage block is v5's plus later x (G_L - G) + (1 - C3) g3 x (G_3 - G) + C3 g3 x (W_3 - W) in every cell, set and cash (exact); meta.lineage.age_mix's under-20 shares are age_mix.json's (45.4% G3-rate, 61.5% later, 46.7% identified)",
      exact && AM.reading === "cross_section_2007_2026" && AM.route === "keys" && AM.under_20_share.identified === u20(MIX.meta.identified)
        && AM.under_20_share.g3_rate === u20(MIX.readings[AM.reading].g3_rate) && AM.under_20_share.later === u20(MIX.readings[AM.reading].later)
        && [[AM.under_20_share.g3_rate, 45.4], [AM.under_20_share.later, 61.5], [AM.under_20_share.identified, 46.7]].every(([x, w]) => (100 * x).toFixed(1) === w.toFixed(1)),
      `under 20: G3-rate ${(100 * AM.under_20_share.g3_rate).toFixed(2)}%, later ${(100 * AM.under_20_share.later).toFixed(2)}%, identified ${(100 * AM.under_20_share.identified).toFixed(2)}%`);
  }
}
gate("RESPONSES is meta.responses and componentsFor(null) is meta.capital_return.components (deep-equal, key order)",
  JSON.stringify(P.RESPONSES) === JSON.stringify(payload.meta.responses) && JSON.stringify(COMPONENTS) === JSON.stringify(payload.meta.capital_return.components));
const diffs = P.responseDiffs(payload29.meta.responses, payload.meta.responses);
gate("only the group-size responses differ from v4's: general government (and its s), row 8's factor, the long-run lines and their subfunctions, the road lines, recreation's state price and the long-run property receipts",
  diffs.length > 0 && diffs.every((p) => P.GROUP_PATHS.includes(p) || /^(economic_affairs_services|recreation_culture)\.subfunctions\[[a-z_]+\]\.(low|high)$/.test(p)),
  `${diffs.length} values: ${diffs.join(", ")}`);
const P24_FIELDS = Object.keys(P.P24.MAIN_SPECS[0]);
const EXTRA = ["reading", "rate", "long_run", "enterprises", "line_responses"];
gate("the specifications carry only the September 24 fields and reading, rate, long_run, enterprises and line_responses, in the September 29 order",
  specs.every((s) => Object.keys(s).every((k) => P24_FIELDS.includes(k) || EXTRA.includes(k)))
  && JSON.stringify(Object.keys(specs[0])) === JSON.stringify(Object.keys(P4.MAIN_SPECS[0])), Object.keys(specs[0]).join(" "));
gate("reading is low exactly where general government takes its low response; the rate follows the reading (2% low, 3% high)",
  specs.every((s) => (s.reading === "low") === (s.gg === P.RESPONSES.general_government.low) && s.rate === RATES[s.reading]),
  `${specs.filter((s) => s.reading === "low").length} low of 64`);
const lrKeys = Object.keys(P.LINE_RESPONSES);
gate(`each specification's line responses are meta.responses at its reading: ${lrKeys.length} entries, in meta's order`,
  specs.every((s) => JSON.stringify(Object.keys(s.line_responses)) === JSON.stringify(lrKeys) && lrKeys.every((k) => s.line_responses[k] === P.LINE_RESPONSES[k][s.reading])),
  lrKeys.join(" "));
const movedKeys = lrKeys.filter((k) => specs.some((s, i) => s.line_responses[k] !== P4.MAIN_SPECS[i].line_responses[k]));
gate("the specifications are the September 29 case's but for general government and the group-size line responses (every other field and line response identical)",
  specs.every((s, i) => Object.keys(s).every((k) => ["gg", "line_responses"].includes(k) || s[k] === P4.MAIN_SPECS[i][k])
    && lrKeys.every((k) => movedKeys.includes(k) || s.line_responses[k] === P4.MAIN_SPECS[i].line_responses[k]))
  && movedKeys.every((k) => ["economic_affairs_services", "recreation_culture", "roads_vmt_sl", "roads_vmt_fed", "state_price_recreation_culture",
    "receipt:modeled_owner_property", "receipt:tenant_occupied_property"].includes(k)), `moved: ${movedKeys.join(", ")}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: profiles]");
const FOLLOW = P.FOLLOW_LR;
const OTHER_FOLLOWERS = P.PAYLOAD_LINES.map((l) => l.id).filter((id) => P.PARENT[id] && !FOLLOW.includes(id));
const receiptKeys = lrKeys.filter((k) => k.startsWith("receipt:"));
const profileRuns = {};
for (const pf of ["long_run_non_school_fixed", "proportional_reference", "cbo_category_lag_non_school_full"]) profileRuns[pf] = runs(specs, pf);
const every = (rs, f) => rs.every((xs) => xs.every((r, i) => f(r, specs[i])));
gate(`proportional reference: roads, parks and the correction lines that follow them (${FOLLOW.join(", ")}) respond at 1, and so does the block`,
  every(profileRuns.proportional_reference, (r) => LR_LINES.concat(FOLLOW).every((id) => responseOf(r.evaluation, id) === 1)
    && r.capital.components.filter((c) => c.group === "block").every((c) => c.response === 1)), "2 methods x 64 specifications");
gate("category lag (the old main profile): roads, parks, their correction lines and the block at 0",
  every(profileRuns.cbo_category_lag_non_school_full, (r) => LR_LINES.concat(FOLLOW).every((id) => responseOf(r.evaluation, id) === 0)
    && capitalGroup(r, "block") === 0), "2 methods x 64 specifications");
gate("long_run_non_school_fixed: roads, parks and their correction lines take the specification's responses, as in the main profile; no college capital",
  every(profileRuns.long_run_non_school_fixed, (r, s) => LR_LINES.concat(FOLLOW).every((id) => responseOf(r.evaluation, id) === s.line_responses[id])
    && byId(r, "college") === 0), "2 methods x 64 specifications");
gate(`every profile: ${OTHER_FOLLOWERS.join(", ")} respond as their parents (${OTHER_FOLLOWERS.map((id) => P.PARENT[id]).join(", ")}), and every receipt response is the specification's`,
  [newRuns].concat(Object.values(profileRuns)).every((rs) => every(rs, (r, s) => OTHER_FOLLOWERS.every((id) => responseOf(r.evaluation, id) === responseOf(r.evaluation, P.PARENT[id]))
    && receiptKeys.every((k) => receiptOf(r, k.slice("receipt:".length)).response === s.line_responses[k]))), "4 profiles x 2 methods x 64 specifications");
gate("main profile: every correction line responds as the specification sets it and the road lines as their subfunctions (sl_highways, fed_highways) at v5",
  every(newRuns, (r, s) => P.PAYLOAD_LINES.filter((l) => P.PARENT[l.id]).every((l) => responseOf(r.evaluation, l.id) === s.line_responses[l.id])
    && COMPONENTS.filter((c) => c.key.kind === "part_rekeyed").every((c) => s.line_responses[c.key.correction_line] === P.subfunctionResponses(s.long_run, s.reading)[c.response.subfunction])));
gate("main profile: every long-run capital component takes its subfunction's v5 response from meta.responses",
  every(newRuns, (r, s) => r.capital.components.filter((c) => COMPONENTS.find((x) => x.id === c.id).response.kind === "long_run_subfunction").every((c) => {
    const rule = COMPONENTS.find((x) => x.id === c.id).response;
    return c.response === P.RESPONSES[rule.line].subfunctions.find((x) => x.id === rule.subfunction)[s.reading];
  })));
gate("in every profile the enterprise components respond at 1",
  [newRuns].concat(Object.values(profileRuns)).every((rs) => every(rs, (r) => r.capital.components.filter((c) => c.group === "enterprise").every((c) => c.response === 1))));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: general government held at 0]");
const GG_LINE = "general_public_services";
const ggCapitalIds = COMPONENTS.filter((c) => c.response.line === GG_LINE).map((c) => c.id);
gate(`the capital components that take ${GG_LINE}'s response are gps_sl and gps_fed, by line_response`,
  JSON.stringify(ggCapitalIds) === JSON.stringify(["gps_sl", "gps_fed"]) && COMPONENTS.filter((c) => ggCapitalIds.includes(c.id)).every((c) => c.response.kind === "line_response"));
const ggFixedSpecs = specs.map((s) => Object.assign({}, s, { gg: 0 }));
const ggFixedRuns = runs(ggFixedSpecs);
const ggFixedCosts = costsOf(ggFixedRuns);
const ggFixed = bandOf(ggFixedCosts);
const ggOperating = (r) => responseOf(r.evaluation, GG_LINE) * amount(r.evaluation, GG_LINE);
const ggCapital = (r) => capitalWhere(r, (c) => ggCapitalIds.includes(c.id));
gate("general government at 0: its line and its capital respond at 0; every other line, receipt, capital component and production term is the case's exactly",
  ggFixedRuns.every((xs, m) => xs.every((r, i) => {
    const a = newRuns[m][i];
    return responseOf(r.evaluation, GG_LINE) === 0 && ggCapital(r) === 0
      && r.evaluation.spending.every((l, k) => l.id === a.evaluation.spending[k].id && (l.id === GG_LINE || l.effect_bn === a.evaluation.spending[k].effect_bn))
      && r.evaluation.receipts.every((x, k) => x.id === a.evaluation.receipts[k].id && x.effect_bn === a.evaluation.receipts[k].effect_bn)
      && r.capital.components.every((c, k) => c.id === a.capital.components[k].id && (ggCapitalIds.includes(c.id) || c.return_bn === a.capital.components[k].return_bn))
      && r.evaluation.private_wtp_bn === a.evaluation.private_wtp_bn && r.evaluation.induced_receipts_bn === a.evaluation.induced_receipts_bn;
  })), "2 methods x 64 specifications");
const ggOperatingAtEnds = atEnds(newEnds, (m, i) => ggOperating(newRuns[m][i]));
const ggCapitalAtEnds = atEnds(newEnds, (m, i) => ggCapital(newRuns[m][i]));
gate("general government at 0 keeps the end specifications; its band is the case's less the operating effect and the gps return there (1e-9)",
  ends(ggFixedCosts).every((e, m) => e[0] === newEnds[m][0] && e[1] === newEnds[m][1])
  && [0, 1].every((e) => near(ggFixed[e], C[e] - ggOperatingAtEnds[e] - ggCapitalAtEnds[e], 1e-9)),
  `${f2(ggFixed)}: operating ${f2(ggOperatingAtEnds)}, capital ${f2(ggCapitalAtEnds)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[history: the September 29 case and the rows it carried]");
const v4Models = METHODS.map((m) => P4.modelFor("central", m, P4.withCentral({})));
const v4Runs = runs(P4.MAIN_SPECS, MAIN_PROFILE, v4Models, P4);
const v4CashRuns = ON ? runs(PC4.MAIN_SPECS, MAIN_PROFILE, METHODS.map((m) => PC4.modelFor("central", m, PC4.withCentral({}))), PC4) : null;
const v4Costs = costsOf(v4Runs);
const C4 = P4.central({}), C4cash = PC4.central({});
gate("the September 29 case re-derives through SEPT29 exactly: its band, the cash set's, and per_spec.csv's cost at every specification and method",
  C4[0] === s29.main_case[0] && C4[1] === s29.main_case[1] && C4cash[0] === s29.cash_set.band_bn[0] && C4cash[1] === s29.cash_set.band_bn[1]
  && METHODS.every((meth, k) => specs.every((_, i) => String(v4Costs[k][i]) === ps29.find((r) => r.method === meth && Number(r.spec) === i).cost_bn)),
  `${f2(C4)}; cash ${f2(C4cash)}`);
const HISTORY_ROWS = ["first_year_response", "schools_case", "sept27_case", "long_run_responses_alone", "rental_assistance_alone",
  "long_run_responses_and_capital_return_option_a"];
const histValue = { first_year_response: s29.first_year_response, schools_case: s29.schools_case, sept27_case: s29.adopted_2026_09_27,
  long_run_responses_alone: s29.each_addition.long_run_responses_alone, rental_assistance_alone: s29.each_addition.rental_assistance_alone,
  long_run_responses_and_capital_return_option_a: s29.each_addition.long_run_responses_and_capital_return_option_a };
gate("the September 29 lane's history rows print its summary.json values, and its adopted and cash_set rows print the September 29 case",
  HISTORY_ROWS.every((v) => { const r = row29(MAIN_PROFILE, v); return r.cost_low_bn === fx(histValue[v][0]) && r.cost_high_bn === fx(histValue[v][1]); })
  && row29(MAIN_PROFILE, "adopted").cost_low_bn === fx(C4[0]) && row29(MAIN_PROFILE, "adopted").cost_high_bn === fx(C4[1])
  && row29(MAIN_PROFILE, "cash_set").cost_low_bn === fx(C4cash[0]) && row29(MAIN_PROFILE, "cash_set").cost_high_bn === fx(C4cash[1]));
if (ON) gate("v5's band rows print the base: its adopted and cash_set rows are the base's band and cash set, and its history rows are the September 29 lane's",
  row5(MAIN_PROFILE, "adopted").cost_low_bn === fx(C5[0]) && row5(MAIN_PROFILE, "adopted").cost_high_bn === fx(C5[1])
  && row5(MAIN_PROFILE, "cash_set").cost_low_bn === fx(C5cash[0]) && row5(MAIN_PROFILE, "cash_set").cost_high_bn === fx(C5cash[1])
  && HISTORY_ROWS.map((v) => [v, v]).concat([["sept29_case", "adopted"], ["sept29_cash_set", "cash_set"]]).every(([v, w]) =>
    ["cost_low_bn", "cost_high_bn", "range_low_bn", "range_high_bn"].every((k) => row5(MAIN_PROFILE, v)[k] === row29(MAIN_PROFILE, w)[k])));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the lineage line, from the September 29 case]");
// At each method's end specifications (48 low, 11 high in both cases): v5 less v4, split into the union's move at the
// larger group (v4's model with audit row 8's change, at v5's specifications) and the added people.
const row8Edit = P.LINEAGE_EDITS[P.LINEAGE_EDITS.length - 1];
gate("the lineage's last edit is audit row 8's change on lane_constants (meta.lineage.edits.row8_edit_bn)",
  row8Edit.line === "lane_constants" && row8Edit.key === "k" && row8Edit.by.personal === L.edits.row8_edit_bn && row8Edit.by.shared === L.edits.row8_edit_bn, String(L.edits.row8_edit_bn));
const unionModels = v4Models.map((m) => Engine.applyCorrections(m, { edits: [row8Edit], meta: m.corrections }));
const unionCosts = costsOf(runs(specs, MAIN_PROFILE, unionModels));
const v4Ends = ends(v4Costs);
gate("v4 and v5 have the same end specifications in both methods (48 / 11)", JSON.stringify(v4Ends) === JSON.stringify(newEnds), JSON.stringify(newEnds));
const part = (f) => atEnds(newEnds, (m, i) => f(m, i));
// With items the lineage line is v5's (the base less v4); the items' change from v5 follows.
const lineCosts = ON ? baseCosts : newCosts, Cline = ON ? C5 : C;
const total = part((m, i) => lineCosts[m][i] - v4Costs[m][i]);
const unionMove = part((m, i) => unionCosts[m][i] - v4Costs[m][i]);
const members = part((m, i) => lineCosts[m][i] - unionCosts[m][i]);
const linG3 = linSet.of_which_g3plus_part_bn, linW = linSet.of_which_white_part_bn, linU = linSet.of_which_union_response_move_bn;
gate(`${ON ? "the base: " : ""}the parts add to the change from v4 (1e-9), which is the band move (the same ends)`,
  [0, 1].every((e) => near(unionMove[e] + members[e], total[e], 1e-9) && near(total[e], Cline[e] - C4[e], 1e-9)), `${f2(unionMove)} + ${f2(members)} = ${f2(total)}`);
gate(`${ON ? "the base: " : ""}the union's move and the added people's part are the lineage lane's (of_which_union_response_move_bn; of_which_g3plus_part_bn + of_which_white_part_bn; 1e-9)`,
  [0, 1].every((e) => near(unionMove[e], linU[e], 1e-9) && near(members[e], linG3[e] + linW[e], 1e-9)),
  `G3+ members ${f2(linG3)}, whites ${f2(linW)}`);
const cashTotal = [0, 1].map((e) => Ccash[e] - C4cash[e]);
const cashLine = ON ? [0, 1].map((e) => C5cash[e] - C4cash[e]) : cashTotal;
gate(`${ON ? "the base: " : ""}the cash set's change from v4's cash set is the lineage lane's cash change (1e-9)`,
  [0, 1].every((e) => near(cashLine[e], linCash.change_from_v4_bn[e], 1e-9)), f2(cashLine));
let itemsTotal = null, itemParts = null;
if (ON) {
  console.log("\n[gates: the items' change, from v5]");
  const ch5 = s5.change_at_fixed_specifications;
  gate("the base: the lineage line's parts are v5's summary.json change_at_fixed_specifications (1e-9)", [0, 1].every((e) => near(unionMove[e], ch5.union_response_move[e], 1e-9)
    && near(members[e], ch5.g3plus_members[e] + ch5.whites[e], 1e-9) && near(total[e], ch5.total[e], 1e-9)), `${f2(total)}`);
  itemsTotal = part((m, i) => newCosts[m][i] - baseCosts[m][i]);
  gate("the items' change at the end specifications is the band's move from v5 (1e-9; the ends do not move)",
    [0, 1].every((e) => near(itemsTotal[e], C[e] - C5[e], 1e-9)), f2(itemsTotal));
  // Each item alone on v5, by part at the end specifications, for the set and (where it enters) the cash set:
  //   cell shifts      each part's amount at the end's allocation times its line's response there;
  //   national scale   each line's amount move times its response, and the capital return's move; split into the
  //                    union's share (v4's cells) and the added people's, the line scaling both;
  //   lineage          the part models, run one at a time (G3-rate and later; G3+ members and whites).
  const byParts = (x, set) => {
    const xr = set === "cash" ? x.cashRuns : x.runs, br = set === "cash" ? baseCashRuns : baseRuns, rec = (set === "cash" ? x.Q.CASH : x.Q).CASE_ITEMS[0];
    const total_ = part((m, i) => xr[m][i].cost_bn - br[m][i].cost_bn);
    if (x.r.kind === "lineage") {
      const A_ = agePartsAt[set].parts;
      return { total: total_, parts: { g3_rate: part((m, i) => A_.g3_rate[i]), later: part((m, i) => A_.later[i]) },
        members: { g3plus_members: part((m, i) => A_.g3plus_members[i]), whites: part((m, i) => A_.whites[i]) } };
    }
    if (Object.keys(rec.parts).length) {
      const es = (set === "cash" ? x.Q.CASH : x.Q).ITEM_EDITS;
      const parts = Object.fromEntries(Object.entries(rec.parts).map(([n, p]) => [n,
        part((m, i) => p.by[specs[i].allocation] * lineOf(xr[m][i].evaluation, es[p.edit].line).response)]));
      // An item's capital components with the components they offset: their move from v5 (the cell shifts' move of the
      // keys included).
      if (rec.capital) for (const id of rec.capital.components) {
        const of = COMPONENTS.find((c) => c.id === id).of_component;
        const name = rec.capital_components && rec.capital_components[of] ? rec.capital_components[of].part : `capital_${of}`;
        parts[name] = part((m, i) => byId(xr[m][i], of) + byId(xr[m][i], id) - byId(br[m][i], of));
      }
      return { total: total_, parts };
    }
    const D = P.ITEM_DETAIL[x.r.id][set], v4r = set === "cash" ? v4CashRuns : v4Runs;
    const move = (m, i, l) => (amount(xr[m][i].evaluation, l) - amount(br[m][i].evaluation, l)) * responseOf(xr[m][i].evaluation, l);
    const share = (m, i, l, rs) => amount(rs[m][i].evaluation, l) * D.delta[l] / national(br[m][i].evaluation, l) * responseOf(xr[m][i].evaluation, l);
    const parts = Object.fromEntries(D.lines.map((l) => [l, part((m, i) => move(m, i, l))]));
    parts.capital_return = part((m, i) => xr[m][i].capital.total_bn - br[m][i].capital.total_bn);
    const union = part((m, i) => D.lines.reduce((t, l) => t + share(m, i, l, v4r), 0));
    const lineage = part((m, i) => D.lines.reduce((t, l) => t + share(m, i, l, br) - share(m, i, l, v4r), 0));
    return { total: total_, parts, split: { union, lineage, capital_return: parts.capital_return } };
  };
  itemParts = alone.map((x) => Object.assign({ id: x.r.id, kind: x.r.kind, alone: null }, { set: byParts(x, "set"), cash: x.cashRuns ? byParts(x, "cash") : null }));
  for (const x of itemParts) x.alone = x.set.total;
  const gapOf = (b) => Math.max(...[0, 1].map((e) => Math.max(Math.abs(Object.values(b.parts).reduce((a, v) => a + v[e], 0) - b.total[e]),
    b.split ? Math.abs(b.split.union[e] + b.split.lineage[e] + b.split.capital_return[e] - b.total[e]) : 0,
    b.members ? Math.abs(b.members.g3plus_members[e] + b.members.whites[e] - b.total[e]) : 0)));
  const partGap = Math.max(...itemParts.map((x) => Math.max(gapOf(x.set), x.cash ? gapOf(x.cash) : 0)));
  gate(`each item's parts at the end specifications add to its change alone, set and cash (1e-9; max |diff| ${ex(partGap)}): cell shifts at their lines' responses, and an item's capital components with the components they offset (no other capital key reads the shifted lines); each national-scale line's move at its response plus the capital return's, and their union and added-people split; the lineage parts run one part model at a time`,
    partGap < 1e-9,
    itemParts.map((x) => `${x.id}: ${Object.entries(x.set.parts).filter(([, v]) => Math.abs(v[0]) + Math.abs(v[1]) > 5e-3).map(([n, v]) => `${n} ${f2(v)}`).join(", ")}`).join("; "));
}

// ---------------------------------------------------------------------------------------------------
console.log("\n[range]");
const dev = (b) => [b[0] - C[0], b[1] - C[1]];
const components = [];
function component(name, label, variants) {
  const devs = variants.map(([v, b]) => ({ v, d: dev(b) }));
  const lo = [Math.min(0, ...devs.map((x) => x.d[0])), Math.min(0, ...devs.map((x) => x.d[1]))];
  const hi = [Math.max(0, ...devs.map((x) => x.d[0])), Math.max(0, ...devs.map((x) => x.d[1]))];
  components.push({ name, label, lo, hi, devs });
}
const base = withCentral({});
const RANGE = V4.rangeComponents();
const skipped = [];
for (const comp of RANGE) {
  const variants = comp.variants.map((v) => ({ v, o: typeof v.o === "function" ? v.o(base) : v.o }));
  if (variants.every((x) => !Object.keys(x.o).length && x.v.caseName === "central" && x.v.methods.length === METHODS.length)) { skipped.push(comp.name); continue; }
  component(comp.name, comp.label, variants.map(({ v, o }) => {
    const bs = v.methods.map((meth) => evalPackage(v.caseName, meth, o));
    return [v.v, [mean(bs.map((b) => b[0])), mean(bs.map((b) => b[1]))]];
  }));
}
gate(`the range's components are the September 29 case's (names, labels, variants), and every one moves the case but ${skipped.join(", ") || "none"} (an item beside the case)`,
  JSON.stringify(skipped) === JSON.stringify(s29.v4.range_components_skipped) && components.length === s29.components.length
  && components.every((c, k) => c.name === s29.components[k].name && c.label === s29.components[k].label
    && JSON.stringify(c.devs.map((d) => d.v).sort()) === JSON.stringify(Object.keys(s29.components[k].variants).sort())), `${components.length} components`);
const sumLo = components.reduce((s, x) => [s[0] + x.lo[0], s[1] + x.lo[1]], [0, 0]);
const sumHi = components.reduce((s, x) => [s[0] + x.hi[0], s[1] + x.hi[1]], [0, 0]);
const rangeLowEnd = [C[0] + sumLo[0], C[0] + sumHi[0]], rangeHighEnd = [C[1] + sumLo[1], C[1] + sumHi[1]];
const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
const quadrature = [C[0] - rss(components.map((x) => x.lo[0])), C[1] + rss(components.map((x) => x.hi[1]))];
// The components that re-run the union's data (fill-in cases, tax keys, medical and benefit estimates, ...): the added
// people's amounts stay the case's, so these deviate as on the September 29 case (within $0.001bn, the interactions
// with the larger group's responses). Had the added people's amounts moved in proportion to the union's, each would be
// larger by the added share (indicative, not a bound).
const atCaseData = components.filter((c, k) => c.devs.every((d) => {
  const w = s29.components[k].variants[d.v];
  return Math.abs(d.d[0] - w[0]) < 1e-3 && Math.abs(d.d[1] - w[1]) < 1e-3;
})).map((c) => c.name);
const addedShare = L.counts.added / L.counts.account_union;
const atCaseDataMove = [addedShare * components.filter((c) => atCaseData.includes(c.name)).reduce((a, c) => a + c.lo[0], 0),
  addedShare * components.filter((c) => atCaseData.includes(c.name)).reduce((a, c) => a + c.hi[1], 0)];
// Variants whose own reading of a group-size response moves at first order, or keeps v4's group (package.cjs moveSpec).
const FIRST_ORDER = {
  "finite_removal/engine population key": "general government's response and row 8's factor at the engine key's group share: moved by the case's change (first order)",
  "property_long_run/low responses": "the receipt-side lane's low property readings: moved by the case's change (first order)",
  "school_response/within district, finite r": "the within-district school response at v4's pupil share (the added people's pupils are not in it)",
  "school_response/within district, r = b": "the within-district elasticity as the response (does not depend on the group's size)",
  "capital_definition/k12_at_pupil_share": "K-12 capital keyed at v4's pupil share, a constant (the added people's pupils are not in it)",
};
// v6: every component re-runs the case with the items' edits at the case's (package.cjs withItems). A component then
// deviates as on v5 unless a variant's end moves to a specification of the other allocation, where the item's amount
// differs. The pension item's union part is Delta ratio_net x the case's OASDI receipts; a variant that re-keys those
// receipts would take Delta ratio_net x its own, so the approximation there is Delta ratio_net x the receipts' move.
let itemsAtCaseData = null;
if (ON) {
  const asOn5 = components.filter((c, k) => c.devs.every((d) => {
    const w = s5.components[k].variants[d.v];
    return Math.abs(d.d[0] - w[0]) < 1e-3 && Math.abs(d.d[1] - w[1]) < 1e-3;
  })).map((c) => c.name);
  const moved = components.map((c, k) => [c.name, Math.max(...c.devs.flatMap((d) => [0, 1].map((e) => Math.abs(d.d[e] - s5.components[k].variants[d.v][e]))))]);
  itemsAtCaseData = { components_as_on_v5: asOn5, deviation_change_from_v5_bn: Object.fromEntries(moved),
    note: "each component's largest change, over its variants and both ends, of its deviation from the case against v5's; a component is listed as on v5 when every deviation is within $0.001bn" };
  const PA = payload.meta.pension_accrual;
  if (APPLIED.some((r) => r.id === "pension_tr2026")) {
    const dRatio = PA.ratio_net - PA.previous.oct05.ratio_net, REF = MODEL.receipts.reference;
    const rec = (m, id) => m.receipts.lines.find((l) => l.id === id).cells[REF];
    const oasdiOf = (m) => Object.fromEntries(ALLOCS.map((a) => [a, PA.oasdi_lines.reduce((s, id) => s + rec(m, id)[a].target_bn, 0) + PA.se_oasdi_share * rec(m, PA.se_line)[a].target_bn]));
    const caseOasdi = new Map(METHODS.map((meth) => [meth, oasdiOf(P.BASE.modelFor("central", meth, P.BASE.withCentral({})))]));
    const VARS = RANGE.flatMap((comp) => comp.variants.map((v) => [`${comp.name}/${v.v}`, v.caseName, typeof v.o === "function" ? v.o(base) : v.o, v.methods]))
      .concat([["audit_row3_instead_of_cbo_income_tax", "central", { incomeTax: "row3", tax_key: "cbo_2022" }, METHODS], ["no_fill_in_correction", "central", {}, ["audit_rules_alone"]]]);
    const byVariant = {};
    for (const [label, caseName, o, methods] of VARS) {
      const errs = methods.map((meth) => {
        const x = oasdiOf(P.BASE.modelFor(caseName, meth, P.BASE.withCentral(o)));
        const c = caseOasdi.get(meth) || oasdiOf(P.BASE.payloadModel());
        return Math.max(...ALLOCS.map((a) => Math.abs(dRatio * (x[a] - c[a]))));
      });
      byVariant[label] = Math.max(...errs);
    }
    const worstOf = Object.entries(byVariant).sort((a, b) => b[1] - a[1]);
    itemsAtCaseData.pension_tr2026_at_the_case_receipts = { delta_ratio_net: dRatio, worst_bn: worstOf[0][1], worst_variant: worstOf[0][0],
      over_0_001_bn: Object.fromEntries(worstOf.filter(([, x]) => x >= 1e-3)),
      note: "the union's OASDI receipts in each variant's v4 model against the case's, times Delta ratio_net: how far the item's static union part is from the rule's at that variant's receipts, at either allocation (the item's lineage and Part A parts do not depend on the union's receipts)" };
  }
}

// ---------------------------------------------------------------------------------------------------
console.log("\n[variants]");
// The item variants' route: candidate v4's evaluateFull at the moved specification, then the road capital keyed on the
// evaluation and the long-run capital at v5 (package.cjs viaCandidate). On the case's own options it is the case.
const viaGap = worst(MODELS.flatMap((m, k) => specs.map((s, i) => P.viaCandidate(m, s).cost_bn - newCosts[k][i])));
const viaCashGap = worst(cashModels.flatMap((m, k) => PC.MAIN_SPECS.map((s, i) => PC.viaCandidate(m, s).cost_bn - cashCosts[k][i])));
gate("candidate v4's route, which the item variants take (property, payroll, the income-tax key, items 8 and 10), gives the case and the cash set at the case's own options at every specification and method (1e-9): the added people's road key and long-run capital included",
  viaGap < 1e-9 && viaCashGap < 1e-9, `max |diff| ${ex(viaGap)} / ${ex(viaCashGap)}`);
// Options that change a line's national total or split a part of a line off: the added people keep the case's key,
// their amount over the line's national, on every line, and a split part takes its line's (package.cjs followNationals).
const beside8 = V4.BESIDE_ITEMS.find((it) => it.id === "8"), beside10 = V4.BESIDE_ITEMS.find((it) => it.id === "10");
const RATES7 = { rates: { low: RATES.reported, high: RATES.reported } };
const ROW_OPTIONS = [["without_capital_return", "central", { capital: false }], ["school_within_district", "central", { school_rule: "within_district" }],
  ["school_within_district_as_response", "central", { school_rule: "within_district_as_response" }], ["enterprises_out_option_a", "central", { enterprises: "A" }],
  ["enterprise_receipt_at_model_json_share", "central", { enterprise_rekey: false }], ["capital_return_at_7pct", "central", RATES7],
  ["rental_assistance_at_0", "central", { rental: 0 }], ["k12_capital_at_pupil_share", "central", { capital_variant: "k12_at_pupil_share" }],
  ["audit_row3_instead_of_cbo_income_tax", "central", { incomeTax: "row3", tax_key: "cbo_2022" }], ["no_fill_in_correction", "central", {}, ["audit_rules_alone"]],
  ["transit_at_riders_key_item_8", "central", beside8.o], ["uninsured_use_0_7x_item_10", "central", beside10.o]]
  .concat(V4.rangeComponents().flatMap((comp) => comp.variants.map((v) => [`range ${comp.name}/${v.v}`, v.caseName,
    typeof v.o === "function" ? v.o(base) : v.o, v.methods])));
const natOf = (m) => new Map(m.spending.lines.map((l) => ["spending:" + l.id, l.national_bn]).concat(m.receipts.lines.map((l) => ["receipt:" + l.id, l.national_bn])));
const N_CASE = natOf(P4.modelFor("central", METHODS[0], P4.withCentral({})));
const structural = [...new Set(ROW_OPTIONS.flatMap(([label, caseName, o, methods]) => (methods || METHODS).filter((meth) => {
  const n = natOf(P4.modelFor(caseName, meth, P4.withCentral(o)));
  return [...n].some(([k, v]) => N_CASE.get(k) !== v);
}).map(() => label)))];
const STRUCTURAL = ["transit_at_riders_key_item_8", "range property_long_run/1 everywhere, case-scaled tenant national"];
gate(`the options that change a line's national total or add a line are item 8 (the transit split) and the property range's case-scaled tenant national, of ${ROW_OPTIONS.length} this lane runs`,
  JSON.stringify(structural.slice().sort()) === JSON.stringify(STRUCTURAL.slice().sort()), structural.join("; "));
const cellsOf = (m) => {
  const out = new Map();
  for (const l of m.receipts.lines) for (const [sc, c] of Object.entries(l.cells)) for (const a of ALLOCS) out.set(`receipt:${l.id}|${sc}|${a}`, c[a].target_bn);
  for (const l of m.spending.lines) for (const [k, c] of Object.entries(l.keys)) for (const a of ALLOCS) out.set(`spending:${l.id}|${k}|${a}`, c[a].target_bn);
  return out;
};
const addedKeys = (m5, m4) => { const n = natOf(m5), c5 = cellsOf(m5), c4 = cellsOf(m4);
  return new Map([...c5].filter(([k]) => c4.has(k) && n.get(k.split("|")[0]) !== 0).map(([k, v]) => [k, (v - c4.get(k)) / n.get(k.split("|")[0])])); };
const SPLIT_PARENT = { "receipt:transit_enterprise_surplus": "receipt:enterprise_surplus" };
let keyGap = 0, keyCells = 0;
for (const label of STRUCTURAL) {
  const [, caseName, o] = ROW_OPTIONS.find((x) => x[0] === label);
  METHODS.forEach((meth, k) => {
    const caseKeys = addedKeys(MODELS[k], v4Models[k]);
    const keys = addedKeys(modelFor(caseName, meth, withCentral(o)), P4.modelFor(caseName, meth, P4.withCentral(o)));
    for (const [cell, x] of keys) {
      const [line, ...rest] = cell.split("|");
      const want = caseKeys.get([SPLIT_PARENT[line] || line, ...rest].join("|"));
      if (want === undefined) continue;
      keyGap = Math.max(keyGap, Math.abs(x - want));
      keyCells += 1;
    }
  });
}
gate("under those two options the added people's key (their amount over the line's national) is the case's in every cell, the transit part taking the enterprise surplus's (1e-12)",
  keyGap < 1e-12 && keyCells > 0, `${keyCells} cells, max |diff| ${ex(keyGap)}`);
const schoolRuleEnds = (rule) => {
  const o = { school_rule: rule };
  const cm = costsOf(runs(specsFor(o), MAIN_PROFILE, METHODS.map((m) => modelFor("central", m, withCentral(o)))));
  return { band: bandOf(cm), ends: ends(cm) };
};
const schoolLow = central({ school_rule: "within_district" }), schoolLowAsResponse = central({ school_rule: "within_district_as_response" });
const schoolLowEnds = schoolRuleEnds("within_district"), schoolLowAsResponseEnds = schoolRuleEnds("within_district_as_response");
gate("the school low side's per-specification runs give its bands (1e-9)", [[schoolLowEnds, schoolLow], [schoolLowAsResponseEnds, schoolLowAsResponse]]
  .every(([x, b]) => near(x.band[0], b[0], 1e-9) && near(x.band[1], b[1], 1e-9)), `ends ${JSON.stringify(schoolLowEnds.ends)} / ${JSON.stringify(schoolLowAsResponseEnds.ends)}`);
const withRow3 = central({ incomeTax: "row3", tax_key: "cbo_2022" });
const noFillIn = evalPackage("central", "audit_rules_alone", {});
const uncorrectedAtResponses = P.band(MODEL);
const otherProfiles = {};
for (const pf of Object.keys(PROFILES).filter((x) => x !== MAIN_PROFILE)) {
  otherProfiles[pf] = { schools_case: s29.other_profiles[pf].schools_case, uncorrected_at_adopted_responses: P.band(MODEL, pf), adopted: central({ profile: pf }) };
}
const oldProfile = { profile: "cbo_category_lag_non_school_full", schools_case: s29.old_main_profile.schools_case,
  with_rental_assistance_capital_and_enterprises: central({ profile: "cbo_category_lag_non_school_full" }) };
const withoutCapital = central({ capital: false });
const optionA = central({ enterprises: "A" });
const optionARuns = runs(specsFor({ enterprises: "A" }));
const atModelShare = central({ enterprise_rekey: false });
const rentalAt0 = central({ rental: 0 });
const pupilRuns = runs(specsFor({ capital_variant: "k12_at_pupil_share" }));
const k12Pupil = bandOf(costsOf(pupilRuns));
gate("K-12 at the pupil share: per-specification runs give central()'s band (1e-9)", (() => { const b = central({ capital_variant: "k12_at_pupil_share" });
  return near(b[0], k12Pupil[0], 1e-9) && near(b[1], k12Pupil[1], 1e-9); })());
// The K-12 capital: k12 and any item component that offsets it (item user_fees's k12_user_fees, which the pupil share drops).
const K12_IDS = COMPONENTS.filter((c) => c.id === "k12" || c.of_component === "k12").map((c) => c.id);
const k12Of = (r) => K12_IDS.reduce((t, id) => t + byId(r, id), 0);
const k12Diff = atEnds(newEnds, (m, i) => k12Of(pupilRuns[m][i]) - k12Of(newRuns[m][i]));
const k12Keys = atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.filter((c) => K12_IDS.includes(c.id)).reduce((t, c) => t + c.key, 0));
gate(`with the pupil share the case differs by the K-12 difference alone (${K12_IDS.join(" and ")})`, worst(pupilRuns.flatMap((xs, m) => xs.map((r, i) =>
  r.cost_bn - newCosts[m][i] - (k12Of(r) - k12Of(newRuns[m][i]))))) < 1e-9
  && pupilRuns.every((xs) => xs.every((r) => K12_IDS.slice(1).every((id) => !r.capital.components.some((c) => c.id === id)))), "every specification");
const at7 = central({ rates: { low: RATES.reported, high: RATES.reported } });
const runs7 = runs(specsFor({ rates: { low: RATES.reported, high: RATES.reported } }));
const with8 = central(beside8.o), with10 = central(beside10.o);
const withRuns = (o) => runs(specsFor(o), MAIN_PROFILE, METHODS.map((m) => modelFor("central", m, withCentral(o))));
const runs8 = withRuns(beside8.o), runs10 = withRuns(beside10.o);
// The specification-level variants through the payload model and the specifications alone (no package model): the
// payload-first route a consumer takes (sept24_propagation band_variants.cjs).
const pmBand = (sp) => [Math.min(...sp.map((s) => evaluateFull(P.payloadModel(), s).cost_bn)), Math.max(...sp.map((s) => evaluateFull(P.payloadModel(), s).cost_bn))];
const specChecks = [["without_capital_return", withoutCapital, specsFor({ capital: false })], ["enterprises_out_option_a", optionA, specsFor({ enterprises: "A" })],
  ["capital_return_at_7pct", at7, specsFor({ rates: { low: RATES.reported, high: RATES.reported } })], ["general_government_fixed", ggFixed, ggFixedSpecs],
  ["k12_capital_at_pupil_share", k12Pupil, specsFor({ capital_variant: "k12_at_pupil_share" })]];
const specGap = worst(specChecks.flatMap(([, b, sp]) => { const x = pmBand(sp); return [x[0] - b[0], x[1] - b[1]]; }));
gate("the specification-level variants on the payload model give the methods' bands (1e-9): without the capital return, option A, 7%, general government at 0, K-12 at the pupil share",
  specGap < 1e-9, `max |diff| ${ex(specGap)}`);
// What the lineage adds under each variant row: v5 less the September 29 row (beside, for consumers; not a gate).
const VARIANT_ROWS = { uncorrected_at_adopted_responses: uncorrectedAtResponses, without_capital_return: withoutCapital, school_within_district: schoolLow,
  school_within_district_as_response: schoolLowAsResponse, adopted: C, cash_set: Ccash, enterprises_out_option_a: optionA,
  enterprise_receipt_at_model_json_share: atModelShare, capital_return_at_7pct: at7, rental_assistance_at_0: rentalAt0,
  general_government_fixed: ggFixed, k12_capital_at_pupil_share: k12Pupil, audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn };
const lineageByVariant = Object.fromEntries(Object.entries(VARIANT_ROWS).map(([v, b]) => {
  const r = row29(MAIN_PROFILE, v);
  return [v, [b[0] - Number(r.cost_low_bn), b[1] - Number(r.cost_high_bn)]];
}));
// v6: the same rows on the base, unrounded, and what the items add under each; the item arms, each the base with the
// arm's edits in place of its item's.
let BASE_ROWS = null, itemsByVariant = null, feesUnderSchool = null;
const armRows = [];
if (ON) {
  BASE_ROWS = { uncorrected_at_adopted_responses: B5.band(MODEL), without_capital_return: B5.central({ capital: false }),
    school_within_district: B5.central({ school_rule: "within_district" }), school_within_district_as_response: B5.central({ school_rule: "within_district_as_response" }),
    adopted: C5, cash_set: C5cash, enterprises_out_option_a: B5.central({ enterprises: "A" }), enterprise_receipt_at_model_json_share: B5.central({ enterprise_rekey: false }),
    capital_return_at_7pct: B5.central(RATES7), rental_assistance_at_0: B5.central({ rental: 0 }),
    general_government_fixed: bandOf(costsOf(runs(ggFixedSpecs, MAIN_PROFILE, baseModels, B5))),
    k12_capital_at_pupil_share: B5.central({ capital_variant: "k12_at_pupil_share" }),
    audit_row3_instead_of_cbo_income_tax: B5.central({ incomeTax: "row3", tax_key: "cbo_2022" }), no_fill_in_correction: B5.evalPackage("central", "audit_rules_alone", {}) };
  gate("the base's variant rows print as v5's main_case_bands.csv rows (fx), every one", Object.keys(VARIANT_ROWS).every((v) => {
    const r = row5(MAIN_PROFILE, v);
    return JSON.stringify(Object.keys(BASE_ROWS)) === JSON.stringify(Object.keys(VARIANT_ROWS)) && r.cost_low_bn === fx(BASE_ROWS[v][0]) && r.cost_high_bn === fx(BASE_ROWS[v][1]);
  }), `${Object.keys(BASE_ROWS).length} rows`);
  itemsByVariant = Object.fromEntries(Object.entries(VARIANT_ROWS).map(([v, b]) => [v, [b[0] - BASE_ROWS[v][0], b[1] - BASE_ROWS[v][1]]]));
  // Item user_fees under the school low side (a school response r below 1): its folded terms respond at their lines'
  // responses; the lane's own form holds the engine lines at 1 and writes the K-12 weight (A + B s)(s r + 1 - s).
  if (APPLIED.some((r) => r.id === "user_fees")) {
    const Qf = alone.find((x) => x.r.id === "user_fees").Q, D = P.ITEM_DETAIL.user_fees.set, ENG = PKG.FEES.TAKEN.lines;
    feesUnderSchool = Object.fromEntries(["within_district", "within_district_as_response"].map((rule) => {
      const o = { school_rule: rule }, sp = specsFor(o);
      const qM = METHODS.map((m) => Qf.modelFor("central", m, Qf.withCentral(o))), bM = METHODS.map((m) => B5.modelFor("central", m, B5.withCentral(o)));
      const base = [], folded = [], lane = [];
      METHODS.forEach((_, k) => {
        base.push([]); folded.push([]); lane.push([]);
        sp.forEach((s) => {
          const rb = B5.evaluateFull(bM[k], s), rq = Qf.evaluateFull(qM[k], s), a = s.allocation, ab = D.A_B[a];
          const resp = (id) => (rb.capital.components.find((c) => c.id === id) || { response: 0 }).response;
          const cap = Object.entries(D.delta).reduce((t, [id, dl]) => t + COMPONENTS.find((c) => c.id === id).stock_charged_bn * s.rate * resp(id) * dl[a], 0);
          const form = ENG.reduce((t, id) => t + D.partBy[id][a], 0) + (ab.A + ab.B * s.share) * responseOf(rb.evaluation, "education_services") + cap;
          base[k].push(rb.cost_bn); folded[k].push(rq.cost_bn); lane[k].push(rb.cost_bn + form);
        });
      });
      const bb = bandOf(base), bf = bandOf(folded), bl = bandOf(lane);
      return [rule, { school_response: [...new Set(sp.map((s) => s.school))], base_band_bn: bb, folded_band_bn: bf, lane_form_band_bn: bl,
        item_change_bn: [bf[0] - bb[0], bf[1] - bb[1]], lane_form_change_bn: [bl[0] - bb[0], bl[1] - bb[1]], folded_less_lane_form_bn: [bf[0] - bl[0], bf[1] - bl[1]] }];
    }));
  }
  // Every arm of every applied item: the case with that item at the arm and the others as they are (package.cjs caseOf
  // with {item: arm}), through the package and consumer.cjs; and the arm alone on v5, whose record carries its source
  // lane's band.
  for (const r of APPLIED) for (const [name, arm] of Object.entries(r.arms)) {
    const Q = PKG.caseOf(B5, P.ITEM_IDS, Object.assign({}, P.ITEM_ARMS, { [r.id]: name }));
    const cm = costsOf(caseRuns(Q, "set")), band = bandOf(cm), armEnds = ends(cm);
    const cc = consumerCosts(Q.correctionsPayload());
    const Qa = PKG.caseOf(B5, [r.id], { [r.id]: name }), ra = Qa.CASE_ITEMS[0], ca = consumerCosts(Qa.correctionsPayload());
    const endsOf = (xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))];
    const sourceOk = (xs, want, wantEnds) => [0, 1].every((e) => near(spanOf(xs)[e], want[e], 1e-9)) && JSON.stringify(endsOf(xs)) === JSON.stringify(wantEnds);
    gate(`arm ${r.id}_${name} (${ra.source_arm}): the case at the arm is consumer.cjs's band on its payload (1e-9), ends 48/11 in both methods; the arm alone on v5 is its source lane's band (1e-9), with its ends`,
      [0, 1].every((e) => near(band[e], spanOf(cc)[e], 1e-9)) && armEnds.every((ij) => ij[0] === 48 && ij[1] === 11) && sourceOk(ca, ra.source_band_bn, ra.source_band_specs),
      `${f2(band)} (case ${f2([band[0] - C[0], band[1] - C[1]])}); alone ${f2(spanOf(ca))} against ${f2(ra.source_band_bn)}`);
    let cash = null;
    if (inCash(r.id)) {
      const ccc = consumerCosts(Q.CASH_PAYLOAD), cca = consumerCosts(Qa.CASH_PAYLOAD), rca = Qa.CASH.CASE_ITEMS[0];
      const want = r.kind === "lineage" ? ra.source_cash_band_bn : rca.source_band_bn, wantEnds = r.kind === "lineage" ? ra.source_cash_band_specs : rca.source_band_specs;
      gate(`arm ${r.id}_${name}, cash set: the arm alone on v5 is its source lane's cash band (1e-9), with its ends; the case's cash set at the arm keeps the ends 48/11`,
        sourceOk(cca, want, wantEnds) && JSON.stringify(endsOf(ccc)) === "[48,11]", `${f2(spanOf(ccc))}; alone ${f2(spanOf(cca))} against ${f2(want)}`);
      cash = { band: spanOf(ccc), change_from_the_cash_set_bn: [spanOf(ccc)[0] - Ccash[0], spanOf(ccc)[1] - Ccash[1]], alone_band_bn: spanOf(cca), source_band_bn: want };
    }
    const aloneCentral = bandOf(alone.find((x) => x.r.id === r.id).costs);
    armRows.push({ item: r.id, name, row: `${r.id}_${name}`, label: arm.label, source_arm: ra.source_arm, band, ends: armEnds,
      change_from_the_case_bn: [band[0] - C[0], band[1] - C[1]], change_from_v5_bn: [band[0] - C5[0], band[1] - C5[1]],
      alone_band_bn: spanOf(ca), alone_change_from_the_item_bn: [spanOf(ca)[0] - aloneCentral[0], spanOf(ca)[1] - aloneCentral[1]], source_band_bn: ra.source_band_bn, cash });
  }
}
// The companion readings the record quotes beside the case (CLAUDE.md's headline list, FAQ 19), on this case: the
// lineage at the count's arms a and c and at C3 -/+ 1 SE (lineage options: package.cjs caseOf's fourth argument,
// lineage_count.cjs), each the whole case at the option through the package and consumer.cjs, and the count by share of
// Mexican-immigrant ancestry (ancestry_share.cjs). With no item each option is the lineage lane's stored v5 value (its
// arm's band, or arm b's C3 line at the option's C3), and the ancestry count on v5 is the lineage lane's rows. Item
// added_age_mix enters an option at arm b's measured mixes [ASSUMPTION]; its size there is the case at the option less
// the case at the option without it. The school response 0.836 is the row school_within_district, above.
const companionRows = [];
let companions = null;
if (ON) {
  const withoutLin = P.ITEM_IDS.filter((id) => id !== LIN_ITEM);
  const armsWithout = Object.fromEntries(Object.entries(P.ITEM_ARMS).filter(([k]) => k !== LIN_ITEM));
  const endsOf = (xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))];
  const minus = (a, b) => [a[0] - b[0], a[1] - b[1]];
  const options = {};
  for (const [name, o] of Object.entries(PKG.LINEAGE_OPTIONS)) {
    const Z = PKG.caseOf(B5, [], {}, name), opt = Z.LINEAGE_OPTION_META;
    const Q = PKG.caseOf(B5, P.ITEM_IDS, P.ITEM_ARMS, name);
    const Q3 = LIN_ITEM ? PKG.caseOf(B5, withoutLin, armsWithout, name) : null;
    const byArm = opt.c3 === POP.c3.value;
    const stored = (which) => {
      const A = lin.sets[which].arms[opt.arm];
      if (byArm) return { band: A.band_bn, ends: A.ends };
      const l = A.c3_line;
      return { band: [l.low.intercept_bn + l.low.slope_bn * opt.c3, l.high.intercept_bn + l.high.slope_bn * opt.c3], ends: A.ends };
    };
    const sets = {};
    for (const which of ["set", "cash"]) {
      const cz = consumerCosts(which === "set" ? Z.correctionsPayload() : Z.CASH_PAYLOAD), want = stored(which);
      gate(`lineage option ${name}, ${which === "set" ? "the set" : "the cash set"}: with no item the case at the option is the lineage lane's v5 value (${byArm ? `arm ${opt.arm}'s band` : `arm ${opt.arm}'s C3 line at C3 ${opt.c3.toFixed(4)}`}, v5_summary.json; 1e-9) with its ends`,
        [0, 1].every((e) => near(spanOf(cz)[e], want.band[e], 1e-9)) && JSON.stringify(endsOf(cz)) === JSON.stringify(want.ends),
        `${f2(spanOf(cz))} against ${f2(want.band)}`);
      const X = which === "set" ? Q : Q.CASH;
      const cq = consumerCosts(which === "set" ? Q.correctionsPayload() : Q.CASH_PAYLOAD), cm = costsOf(caseRuns(Q, which)), band = bandOf(cm);
      gate(`lineage option ${name}, ${which === "set" ? "the set" : "the cash set"}: the case at the option (every item) is consumer.cjs's band on its payload (1e-9), ends 48/11 in both methods; its payload is a variant`,
        [0, 1].every((e) => near(band[e], spanOf(cq)[e], 1e-9)) && ends(cm).every((ij) => ij[0] === 48 && ij[1] === 11) && X.correctionsPayload().meta.adopted === null
        && X.correctionsPayload().meta.status.startsWith("variant: ") && X.correctionsPayload().meta.lineage.count_option.name === name,
        `${f2(band)}; ${f2(spanOf(cq))}`);
      const c3 = Q3 ? spanOf(consumerCosts(which === "set" ? Q3.correctionsPayload() : Q3.CASH_PAYLOAD)) : null;
      const at = which === "set" ? C : Ccash, at5 = which === "set" ? C5 : C5cash;
      sets[which] = { band_bn: band, ends: ends(cm)[0], per_member_usd: band.map((x) => x * 1e9 / opt.population),
        change_from_the_case_bn: minus(band, at), v5_at_option_band_bn: spanOf(cz), items_change_at_option_bn: minus(band, spanOf(cz)),
        items_change_at_the_case_bn: minus(at, at5), age_mix_at_option_bn: c3 ? minus(spanOf(cq), c3) : null, without_age_mix_band_bn: c3 };
    }
    options[name] = { label: o.label, arm: opt.arm, source_arm: opt.source_arm, c3: opt.c3, added: opt.added, g3_rate: opt.g3_rate, later: opt.later,
      lineage_population: opt.population, s: opt.s, row8_edit_bn: opt.row8_edit_bn, set: sets.set, cash: sets.cash };
    companionRows.push([`lineage_${name}`, sets.set.band_bn], [`lineage_${name}_cash_set`, sets.cash.band_bn]);
  }
  // The count by ancestry share: on v5 the lineage lane's rows; on this case; and without the lineage item for its size.
  const Q3c = LIN_ITEM ? PKG.caseOf(B5, withoutLin, armsWithout) : null;
  const shares = {};
  for (const which of ["set", "cash"]) {
    const v5 = AS.rowsFor(B5, which, { Engine }), v6 = AS.rowsFor(P, which, { Engine }), w3 = Q3c ? AS.rowsFor(Q3c, which, { Engine }) : null;
    for (const r of v5.rows) {
      const want = lin.fractional.rows.find((x) => x.set === which && x.arm === ARM && x.scenario === r.scenario);
      gate(`the count by ancestry share, ${r.scenario}, ${which === "set" ? "the set" : "the cash set"}: on v5 it is the lineage lane's row (v5_summary.json fractional, arm ${ARM}; 1e-9), its ends and fractional population`,
        !!want && near(r.band_bn[0], want.low_bn, 1e-9) && near(r.band_bn[1], want.high_bn, 1e-9) && r.ends[0] === want.spec_low && r.ends[1] === want.spec_high
        && near(r.fractional_population, want.fractional_population, 1e-6), `${f2(r.band_bn)} at ${r.ends.join("/")}`);
    }
    const strip = (r) => { const x = Object.assign({}, r); delete x.costs; return x; };
    shares[which] = { rows: v6.rows.map((r) => Object.assign(strip(r), {
        v5_band_bn: v5.rows.find((x) => x.scenario === r.scenario).band_bn,
        change_from_v5_bn: minus(r.band_bn, v5.rows.find((x) => x.scenario === r.scenario).band_bn),
        age_mix_bn: w3 ? minus(r.band_bn, w3.rows.find((x) => x.scenario === r.scenario).band_bn) : null })),
      outer_span_bn: [v6.rows.find((r) => r.scenario === "g4_at_nothing").band_bn[0], v6.rows.find((r) => r.scenario === "g4_at_bound").band_bn[1]],
      v5_outer_span_bn: [v5.rows.find((r) => r.scenario === "g4_at_nothing").band_bn[0], v5.rows.find((r) => r.scenario === "g4_at_bound").band_bn[1]],
      pension_split_sensitivity: v6.pension_sensitivity, added_people: v6.added_people, row8_edit_bn: v6.row8_edit_bn };
    for (const r of v6.rows) companionRows.push([`ancestry_share_${r.scenario}${which === "cash" ? "_cash_set" : ""}`, r.band_bn]);
  }
  const c3Span = (which) => [Math.min(...["c3_minus_se", "c3_plus_se"].map((n) => options[n][which].band_bn[0])), Math.max(...["c3_minus_se", "c3_plus_se"].map((n) => options[n][which].band_bn[1]))];
  companions = {
    rule: "the readings the record quotes beside the case, on v6: the lineage at the count's arms a and c and at C3 -/+ 1 SE (lineage options, package.cjs caseOf's fourth argument and lineage_count.cjs: the whole case at the option, every item rebuilt on the option's lineage), the count by share of Mexican-immigrant ancestry (ancestry_share.cjs), and the school response 0.836 (the row school_within_district); rows lineage_<option>, ancestry_share_<scenario> and their _cash_set in main_case_bands.csv",
    age_mix: "[ASSUMPTION] item added_age_mix enters each lineage option with the mixes the age-mix lane measured on arm b's counts (it priced arm b only): the G3-rate persons at the G3-rate mix and the later losses at the later-loss mix, at the option's counts and C3; age_mix_at_option_bn is its size there (the case at the option less the case at the option without it). In the ancestry count it is part of the added people's cost, at s_added; age_mix_bn is its size",
    options,
    c3_plus_minus_1se_bn: { set: c3Span("set"), cash: c3Span("cash"), rule: "C3 + 1 SE's low end to C3 - 1 SE's high end (the record's form for v5)" },
    ancestry_share: Object.assign({ rules: AS.RULES, route: AS.ROUTE, shares_file: AS.SHARES_FILE }, shares),
    school_within_district: { row: "school_within_district", band_bn: schoolLow, note: "the low side with the within-district school response 0.836: set only, as v5's" },
    not_built: [],
  };
}

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the uncorrected model at the adopted responses]");
const MODEL_SYN = P.withSyntheticLines(MODEL);
const addedLines = (side) => MODEL_SYN[side].lines.slice(MODEL[side].lines.length);
const zeroCells = (cells) => Object.values(cells).every((c) => ALLOCS.every((a) => c[a].target_bn === 0 && c[a].other_bn === 0 && c[a].share === 0));
// An item's carrier lines come after the payload's receipt lines, at zero amounts and shares with their national totals
// kept, so their components' keys read 0.
const CARRIER_IDS = P.ITEM_RECEIPT_LINES.map((l) => l.id);
const carrierNational = new Map(P.ITEM_RECEIPT_LINES.map((l) => [l.id, l.national_bn]));
gate(`withSyntheticLines(model.json) appends the payload's 8 spending lines and 2 receipt lines at zero (national, amounts and shares 0)${CARRIER_IDS.length ? `, then the items' ${CARRIER_IDS.length} carrier lines at zero amounts and shares (their national totals kept)` : ""}, and leaves the rest of the model as it was`,
  JSON.stringify(addedLines("spending").map((l) => l.id)) === JSON.stringify(P.PAYLOAD_LINES.map((l) => l.id))
  && JSON.stringify(addedLines("receipts").map((l) => l.id)) === JSON.stringify(P.PAYLOAD_RECEIPT_LINES.concat(CARRIER_IDS))
  && addedLines("spending").every((l) => l.national_bn === 0 && zeroCells(l.keys))
  && addedLines("receipts").every((l) => l.national_bn === (carrierNational.has(l.id) ? carrierNational.get(l.id) : 0) && zeroCells(l.cells))
  && ["spending", "receipts"].every((side) => JSON.stringify(MODEL_SYN[side].lines.slice(0, MODEL[side].lines.length)) === JSON.stringify(MODEL[side].lines))
  && JSON.stringify(MODEL_SYN.production) === JSON.stringify(MODEL.production),
  `${addedLines("spending").length} spending, ${addedLines("receipts").length} receipt lines`);
const ucProfiles = [MAIN_PROFILE].concat(Object.keys(otherProfiles), [oldProfile.profile]);
let ucRows = true, ucResponses = true, ucDirect = 0, ucN = 0;
for (const pf of ucProfiles) specs.forEach((s) => {
  const r = evaluateFull(MODEL, s, pf);
  const direct = Engine.evaluate(P.withSyntheticLines(MODEL), P.stateFor(MODEL, s, pf));
  ucDirect = Math.max(ucDirect, Math.abs(direct.welfare_bn - r.evaluation.welfare_bn));
  for (const [k, v] of Object.entries(s.line_responses)) {
    const row = k.startsWith("receipt:") ? receiptOf(r, k.slice("receipt:".length)) : lineOf(r.evaluation, k);
    if (!row) ucRows = false;
    else if (pf === MAIN_PROFILE && row.response !== v) ucResponses = false;
  }
  if (!addedLines("spending").every((l) => lineOf(r.evaluation, l.id).amount_bn === 0)
    || !addedLines("receipts").every((l) => receiptOf(r, l.id).amount_bn === 0)) ucRows = false;
  ucN += 1;
});
gate("the uncorrected model evaluates at every specification in every profile: each line_responses entry has its engine row (the added lines at amount 0), and in the main profile each row takes the specification's response",
  ucRows && ucResponses, `${ucProfiles.length} profiles x ${specs.length} specifications`);
gate("Engine.evaluate(withSyntheticLines(m), stateFor(m, spec, profile)) is evaluateFull's evaluation on the uncorrected model (exact)", ucDirect === 0, `${ucN} evaluations`);
const zeroPayload = { lines: payload.lines, edits: [], meta: payload.meta,
  receipt_lines: payload.receipt_lines.map((l) => Object.assign({}, l, { national_bn: carrierNational.has(l.id) ? carrierNational.get(l.id) : 0, cells: Object.fromEntries(Object.entries(l.cells)
    .map(([sc, c]) => [sc, Object.fromEntries(ALLOCS.map((a) => [a, Object.assign({}, c[a], { target_bn: 0, other_bn: 0, share: 0 })]))])) })) };
const ucIndependent = Consumer.evaluateAll(JSON.parse(JSON.stringify(zeroPayload)), { engine: Engine, model: MODEL });
const ucPackage = specs.map((s) => evaluateFull(MODEL, s).cost_bn);
const ucGap = worst(ucIndependent.map((x, i) => x.cost_bn - ucPackage[i]));
gate("consumer.cjs on model.json with the payload's lines at zero gives the package's uncorrected cost at every specification (1e-9), and its span is uncorrected_at_adopted_responses",
  ucIndependent.length === specs.length && ucIndependent.every((x, i) => SPEC_FIELDS.every((f) => x.spec[f] === specs[i][f]))
  && ucGap < 1e-9 && near(Math.min(...ucPackage), uncorrectedAtResponses[0], 1e-9) && near(Math.max(...ucPackage), uncorrectedAtResponses[1], 1e-9),
  `max |diff| ${ex(ucGap)}; ${f2(uncorrectedAtResponses)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the enterprises, the re-key and the land rows]");
const SHARE = populationShare(MODELS[0]).personal;
const payloadModel = P.payloadModel();
const SHARE4 = populationShare(v4Models[0]).personal;
gate("the corrected population share is one number in both methods, both allocations and the payload model; the lineage raises it from v4's",
  [...MODELS, payloadModel].every((m) => ALLOCS.every((a) => near(populationShare(m)[a], SHARE, 1e-14))) && SHARE > SHARE4, `${SHARE} (v4 ${SHARE4})`);
gate(`option ${ENTERPRISES}: the enterprise receipt and public housing's deficit respond at 1, every enterprise component at 1, keyed at the corrected share but public housing's capital (the rental line's key)`,
  newRuns.every((xs) => xs.every((r) => esRow(r).response === 1 && P.ENTERPRISE_SPLITS.every((id) => receiptOf(r, id).response === 1)
    && r.capital.components.filter((c) => c.group === "enterprise").every((c) => c.response === 1
      && (c.id === "ent_housing_sl" ? near(c.key, amount(r.evaluation, RENTAL) / national(r.evaluation, RENTAL), 1e-15) : near(c.key, SHARE, 1e-14))))),
  "every specification, both methods");
const laneShareRuns = runs(specs, MAIN_PROFILE, MODELS_LANE);
const rekeyEffect = atEnds(newEnds, (m, i) => newCosts[m][i] - laneShareRuns[m][i].cost_bn);
const publicHousing = atEnds(newEnds, (m, i) => byId(newRuns[m][i], "ent_housing_sl"));
const es29 = s29.enterprises.receipt_at_end_specifications;
const schoolsEs = [0, 1].map((e) => es29.group_amount_bn[e] - es29.move_from_the_schools_case_bn[e]);
const esAmount = atEnds(newEnds, (m, i) => esRow(newRuns[m][i]).amount_bn);
const esNat = payloadModel.receipts.lines.find((l) => l.id === ENTERPRISE_LINE).national_bn;
const esModel = MODEL.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
const kc = readJson(`${CAPDIR}/summary.json`).enterprises.key_consistency;
const moveRekey = [0, 1].map(() => esNat * (SHARE - kc.receipt_key[0]));
const moveSplit = [0, 1].map(() => (esNat - esModel.national_bn) * kc.receipt_key[0]);
const receiptMove = [0, 1].map((e) => esAmount[e] - schoolsEs[e]);
gate("the enterprise receipt's move from the schools case is the re-key at the corrected share (the lineage's included) plus item 1's split of public housing (1e-9)",
  [0, 1].every((e) => near(receiptMove[e], moveRekey[e] + moveSplit[e], 1e-9)) && near(esNat, esModel.national_bn - V4.HOUSING_SURPLUS, 1e-9),
  `${fx(receiptMove[0])} = re-key ${fx(moveRekey[0])} + split ${fx(moveSplit[0])}`);
const LAND_ROW = /^((block|enterprise): )?land at 10% of the structures charged: (\S+)$/;
const landRows = capGaps.filter((r) => LAND_ROW.test(r.item));
const landPart = (r) => r.item.match(LAND_ROW)[2] || "core";
const landStock = Object.fromEntries(landRows.map((r) => [r.item.match(LAND_ROW)[3], Number(r.national_base_bn) * Number(r.fee_factor)]));
// An item's capital component re-keys the stock of the component it offsets, so the land under that stock takes its key too.
const LAND_OF = Object.fromEntries(COMPONENTS.map((c) => [c.id, c.of_component || c.id]));
gate(`gaps.csv has one land row for every capital component of the payload, under its part${COMPONENTS.some((c) => c.of_component) ? " (an item's offset component the row of the component it offsets)" : ""}`,
  landRows.length === COMPONENTS.filter((c) => !c.of_component).length
  && COMPONENTS.every((c) => landRows.some((r) => r.item.match(LAND_ROW)[3] === LAND_OF[c.id] && landPart(r) === c.part)), `${landRows.length} rows`);
const landAt = (rs, m, i, pred) => rs[m][i].capital.components.filter(pred).reduce((a, c) => a + landStock[LAND_OF[c.id]] * specs[i].rate * c.key * c.response, 0);
const land = {
  per_10pct_bn: atEnds(newEnds, (m, i) => landAt(newRuns, m, i, () => true)),
  by_part_per_10pct_bn: Object.fromEntries(PARTS.map((g) => [g, atEnds(newEnds, (m, i) => landAt(newRuns, m, i, (c) => c.group === g))])),
  note: s29.beside_the_account.land_per_10pct_of_land_to_structure_value.note };
const rentalKey = atEnds(newEnds, (m, i) => amount(newRuns[m][i].evaluation, RENTAL) / national(newRuns[m][i].evaluation, RENTAL));
const rentalNational = national(newRuns[0][0].evaluation, RENTAL);
const overlap = Object.assign({}, s29.enterprises.overlap_with_rental_assistance, { rental_key: rentalKey, population_share: SHARE, rental_national_bn: rentalNational,
  upper_bound_bn: rentalKey.map((k) => rentalNational * (SHARE - k)) });
const rentalAmount = METHODS.map((_, m) => ALLOCS.map((a) => MODELS[m].spending.lines.find((l) => l.id === RENTAL).keys.housing_support[a].target_bn));
const rentalUncorrected = ALLOCS.map((a) => MODEL.spending.lines.find((l) => l.id === RENTAL).keys.housing_support[a].target_bn);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the payload's sides]");
const uc = uncorrectedAtResponses;
const pBand = (part) => P.band(Engine.applyCorrections(MODEL, part));
const payloadBand = pBand(payload);
const recOnly = pBand({ lines: payload.lines, receipt_lines: payload.receipt_lines, edits: payload.edits.filter((e) => e.side === "receipt") });
const spOnly = pBand({ lines: payload.lines, edits: payload.edits.filter((e) => e.side !== "receipt") });
const prodOnly = pBand({ lines: payload.lines, edits: [], production: payload.production });
const sides = { receipts: [recOnly[0] - uc[0], recOnly[1] - uc[1]], spending: [spOnly[0] - uc[0], spOnly[1] - uc[1]],
  production: [prodOnly[0] - uc[0], prodOnly[1] - uc[1]] };
gate("corrections.json reproduces the case (1e-9)", near(payloadBand[0], C[0], 1e-9) && near(payloadBand[1], C[1], 1e-9), f2(payloadBand));
gate("the three sides (receipts, spending, the production grid) add to the payload's band less the uncorrected band (1e-6)",
  [0, 1].every((e) => near(sides.receipts[e] + sides.spending[e] + sides.production[e], payloadBand[e] - uc[e], 1e-6)),
  `${f2(sides.receipts)} + ${f2(sides.spending)} + ${f2(sides.production)}`);
const receiptsTotal = (m) => Object.fromEntries(ALLOCS.map((a) => [a, m.receipts.lines.reduce((s, l) => s + l.cells[m.receipts.reference][a].target_bn, 0)]));
const groupReceipts = ON ? Object.assign({}, s5.group_receipts_bn, { adopted: receiptsTotal(payloadModel), adopted_2026_10_05: s5.group_receipts_bn.adopted })
  : Object.assign({}, s29.group_receipts_bn, { adopted: receiptsTotal(payloadModel), adopted_2026_09_29: s29.group_receipts_bn.adopted });

// ---------------------------------------------------------------------------------------------------
if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
const full = (x) => (typeof x === "number" ? String(x) : x);
const endSpecs = newEnds.map((e, m) => ({ method: METHODS[m], low_end: Object.assign({ index: e[0] }, specs[e[0]]),
  high_end: Object.assign({ index: e[1] }, specs[e[1]]) }));
const LINE_IDS = LR_LINES.concat([RENTAL], P.PAYLOAD_LINES.map((l) => l.id).filter((id) => P.PARENT[id]));
const lineAtEnds = Object.fromEntries(LINE_IDS.map((id) => [id, {
  response: atEnds(newEnds, (m, i) => responseOf(newRuns[m][i].evaluation, id)),
  group_amount_bn: atEnds(newEnds, (m, i) => amount(newRuns[m][i].evaluation, id)),
  added_bn: atEnds(newEnds, (m, i) => responseOf(newRuns[m][i].evaluation, id) * amount(newRuns[m][i].evaluation, id)) }]));
const receiptsAtEnds = Object.fromEntries(receiptKeys.map((k) => k.slice("receipt:".length)).map((id) => [id, {
  response: atEnds(newEnds, (m, i) => receiptOf(newRuns[m][i], id).response),
  group_amount_bn: atEnds(newEnds, (m, i) => receiptOf(newRuns[m][i], id).amount_bn),
  national_bn: receiptOf(newRuns[0][0], id).national_bn,
  effect_bn: atEnds(newEnds, (m, i) => receiptOf(newRuns[m][i], id).effect_bn) }]));
const capitalAtEnds = {
  rates: { low: RATES.low, high: RATES.high },
  total_bn: atEnds(newEnds, (m, i) => newRuns[m][i].capital.total_bn),
  by_level_bn: Object.fromEntries(["state_local", "federal"].map((lv) => [lv, atEnds(newEnds, (m, i) => capitalWhere(newRuns[m][i], (c) => c.level === lv))])),
  by_part_bn: Object.fromEntries(PARTS.map((g) => [g, atEnds(newEnds, (m, i) => capitalGroup(newRuns[m][i], g))])),
  by_component: Object.fromEntries(COMPONENTS.map((c) => [c.id, { label: c.label, part: c.part, level: c.level,
    stock_charged_bn: c.stock_charged_bn,
    key: atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.find((x) => x.id === c.id).key),
    response: atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.find((x) => x.id === c.id).response),
    return_bn: atEnds(newEnds, (m, i) => byId(newRuns[m][i], c.id)) }])),
  k12_key: { account_key: k12Keys, pupil_share: CAP.k12_keys_at_case_ends.spec48.pupil_share, pupil_share_minus_account_bn: k12Diff,
    note: "the case keys K-12 by the account's school key from the evaluation, which counts the added people; the capital lane's variant k12_at_pupil_share uses its pupil share, a constant measured on the identified group without them" },
};
fs.mkdirSync(OUT, { recursive: true });
const row = (pf, variant, b, r) => [pf, variant, fx(b[0]), fx(b[1]), r ? fx(r[0]) : "", r ? fx(r[1]) : ""].join(",");
const history = (pf, variant, as) => { const r = row29(pf, variant); return [pf, as || variant, r.cost_low_bn, r.cost_high_bn, r.range_low_bn, r.range_high_bn].join(","); };
const bandsCsv = ["profile,variant,cost_low_bn,cost_high_bn,range_low_bn,range_high_bn",
  history(MAIN_PROFILE, "first_year_response"),
  history(MAIN_PROFILE, "schools_case"),
  history(MAIN_PROFILE, "sept27_case"),
  history(MAIN_PROFILE, "adopted", "sept29_case"),
  row(MAIN_PROFILE, "uncorrected_at_adopted_responses", uncorrectedAtResponses),
  history(MAIN_PROFILE, "long_run_responses_alone"),
  history(MAIN_PROFILE, "rental_assistance_alone"),
  history(MAIN_PROFILE, "long_run_responses_and_capital_return_option_a"),
  row(MAIN_PROFILE, "without_capital_return", withoutCapital),
  row(MAIN_PROFILE, "school_within_district", schoolLow),
  row(MAIN_PROFILE, "school_within_district_as_response", schoolLowAsResponse),
  row(MAIN_PROFILE, "adopted", C, [rangeLowEnd[0], rangeHighEnd[1]]),
  row(MAIN_PROFILE, "cash_set", Ccash),
  history(MAIN_PROFILE, "cash_set", "sept29_cash_set"),
  row(MAIN_PROFILE, "enterprises_out_option_a", optionA),
  row(MAIN_PROFILE, "enterprise_receipt_at_model_json_share", atModelShare),
  row(MAIN_PROFILE, "capital_return_at_7pct", at7),
  row(MAIN_PROFILE, "rental_assistance_at_0", rentalAt0),
  row(MAIN_PROFILE, "general_government_fixed", ggFixed),
  row(MAIN_PROFILE, "k12_capital_at_pupil_share", k12Pupil),
  row(MAIN_PROFILE, "audit_row3_instead_of_cbo_income_tax", withRow3),
  row(MAIN_PROFILE, "no_fill_in_correction", noFillIn),
  history(oldProfile.profile, "schools_case"),
  row(oldProfile.profile, "with_rental_assistance_capital_and_enterprises", oldProfile.with_rental_assistance_capital_and_enterprises)]
  .concat(Object.entries(otherProfiles).flatMap(([pf, v]) => [history(pf, "schools_case"),
    row(pf, "uncorrected_at_adopted_responses", v.uncorrected_at_adopted_responses), row(pf, "adopted", v.adopted)]));
// v6: v5's band and cash set as history rows (v5's own row strings, its range included), and the item arms.
if (ON) {
  const history5 = (pf, variant, as) => { const r = row5(pf, variant); return [pf, as, r.cost_low_bn, r.cost_high_bn, r.range_low_bn, r.range_high_bn].join(","); };
  const after = (variant) => { const k = bandsCsv.findIndex((l) => l.startsWith(`${MAIN_PROFILE},${variant},`)); if (k < 0) throw new Error(`[BLOCKED] no row ${variant}`); return k + 1; };
  bandsCsv.splice(after("sept29_case"), 0, history5(MAIN_PROFILE, "adopted", "oct05_case"));
  bandsCsv.splice(after("sept29_cash_set"), 0, history5(MAIN_PROFILE, "cash_set", "oct05_cash_set"));
  bandsCsv.splice(after("no_fill_in_correction"), 0, ...armRows.flatMap((a) => [row(MAIN_PROFILE, a.row, a.band)]
    .concat(a.cash ? [row(MAIN_PROFILE, `${a.row}_cash_set`, a.cash.band)] : [])), ...companionRows.map(([v, b]) => row(MAIN_PROFILE, v, b)));
}
const compCsv = ["component,label,range_dev_low_end_lo,range_dev_low_end_hi,range_dev_high_end_lo,range_dev_high_end_hi"]
  .concat(components.map((x) => [x.name, `"${x.label}"`, fx(x.lo[0]), fx(x.hi[0]), fx(x.lo[1]), fx(x.hi[1])].join(",")));
const perHead = ["method", "spec", "allocation", "normalization", "share", "school", "gg", "uc", "justice", "reading", "rate", "enterprises",
  "cost_bn", "engine_cost_bn", "capital_total_bn", "capital_state_local_bn", "capital_federal_bn",
  "capital_core_bn", "capital_block_bn", "capital_enterprise_bn",
  "response_receipt_enterprise_surplus", "group_enterprise_surplus_bn", "enterprise_surplus_receipt_cost_bn"]
  .concat(COMPONENTS.filter((c) => !c.of_component).map((c) => `capital_${c.id}_bn`))
  .concat(LR_LINES.concat([RENTAL]).flatMap((id) => [`response_${id}`, `group_${id}_bn`]))
  .concat(ON ? ["oct05_cost_bn"].concat(APPLIED.map((r) => `item_${r.id}_bn`), ["items_interaction_bn"]) : [])
  .concat(COMPONENTS.filter((c) => c.of_component).map((c) => `capital_${c.id}_bn`));
const perSpec = [perHead.join(",")].concat(METHODS.flatMap((meth, m) => specs.map((s, i) => {
  const r = newRuns[m][i];
  return [meth, i, s.allocation, s.normalization, s.share, s.school, s.gg, s.uc, s.justice, s.reading, s.rate, s.enterprises,
    r.cost_bn, -r.evaluation.welfare_bn, r.capital.total_bn,
    capitalWhere(r, (c) => c.level === "state_local"), capitalWhere(r, (c) => c.level === "federal"),
    capitalGroup(r, "core"), capitalGroup(r, "block"), capitalGroup(r, "enterprise"), esRow(r).response, esRow(r).amount_bn, esCost(r)]
    .concat(COMPONENTS.filter((c) => !c.of_component).map((c) => byId(r, c.id)))
    .concat(LR_LINES.concat([RENTAL]).flatMap((id) => [responseOf(r.evaluation, id), amount(r.evaluation, id)]))
    .concat(ON ? [baseCosts[m][i]].concat(aloneCosts.map((cm) => cm[m][i] - baseCosts[m][i]),
      [newCosts[m][i] - baseCosts[m][i] - aloneCosts.reduce((t, cm) => t + cm[m][i] - baseCosts[m][i], 0)]) : [])
    .concat(COMPONENTS.filter((c) => c.of_component).map((c) => byId(r, c.id))).map(full).join(",");
})));
const PER = (x) => x * 1e9 / L.counts.lineage_population;
const atEnd = (xs) => [xs[48], xs[11]];
// Item user_fees: what it leaves out (the added people, item retiree_health's line totals), its capital at the ends and
// its school low side.
function feesBlock() {
  const x = alone.find((y) => y.r.id === "user_fees"), D = P.ITEM_DETAIL.user_fees.set, U = payload.meta.user_fees;
  const RH = APPLIED.some((r) => r.id === "retiree_health") ? P.ITEM_DETAIL.retiree_health.set : null;
  const nat = (id) => MODEL.spending.lines.find((l) => l.id === id).national_bn;
  // Item retiree_health moves the education and health lines' national totals; the item's key terms are shares of those
  // lines' dollars (its fee terms and Pell are dollars of their own), so carrying the move would scale the key terms.
  const scaleOf = (id) => (RH && id in RH.delta ? RH.delta[id] / nat(id) : 0);
  const keyTermsAt = (i) => { const a = specs[i].allocation, ab = D.A_B[a];
    return { education: scaleOf("education_services") * (D.partBy.key_higher_ed[a] + ab.A + ab.B * specs[i].share), health: scaleOf("health_services") * D.partBy.key_health[a] }; };
  const notCarried = [48, 11].map((i) => { const t = keyTermsAt(i); return t.education + t.health; });
  const capAt = (id) => atEnds(newEnds, (m, i) => byId(newRuns[m][i], id));
  return {
    lane_change_at_ends_bn: { set: x.r.source_change_bn, cash: x.rc.source_change_bn, rule: x.r.source_rule },
    alone_change_at_ends_bn: { set: [x.consumer[48] - c5[48], x.consumer[11] - c5[11]], cash: [x.cashConsumer[48] - cc5[48], x.cashConsumer[11] - cc5[11]] },
    capital_at_end_specifications_bn: Object.fromEntries(COMPONENTS.filter((c) => c.of_component).map((c) => [c.of_component, {
      component_bn: capAt(c.of_component), offset_bn: capAt(c.id), together_bn: [0, 1].map((e) => capAt(c.of_component)[e] + capAt(c.id)[e]) }])),
    added_people_at_union_terms_bn: U.union_only.added_people_at_union_terms_bn,
    retiree_health_line_totals_not_carried_bn: RH ? { at_end_specifications_bn: notCarried,
      scale: { education_services: scaleOf("education_services"), health_services: scaleOf("health_services"), other_federal_benefits: scaleOf("other_federal_benefits") },
      note: `[APPROX] the item's amounts are the lane's on v5's line totals; item retiree_health moves those totals (education ${(100 * scaleOf("education_services")).toFixed(2)}%, health ${(100 * scaleOf("health_services")).toFixed(2)}%), and the key terms (key_higher_ed, the K-12 weight, key_health) are shares of the lines' dollars, so carrying the move would add this; the fee terms and Pell are dollars of their own and would not move` } : null,
    school_low_side: Object.assign(feesUnderSchool, { note: "the folded terms respond at their lines' responses: key_higher_ed and fee_tuition at the education line's s r + 1 - s, the K-12 weight at row 6's s r (A + B) + (1 - s) A; the lane's form holds its engine lines at 1 and writes (A + B s)(s r + 1 - s); the capital is the same in both" }),
  };
}
function v6Block() {
  const byAllocation = (ch) => Object.fromEntries(ALLOCS.map((a) => [a, spanOf(ch.filter((_, i) => specs[i].allocation === a))]));
  const cashBand = (x) => (x.cashCosts ? bandOf(x.cashCosts) : null);
  return {
    status: P.ADOPTED ? `adopted ${P.ADOPTED} (${P.DECISION}): the payloads carry adopted "${P.ADOPTED}" and v5's status form` : `a variant of v6, not adopted: the payloads carry adopted null and status "variant: ..."`,
    case_key: P.CASE_KEY,
    base: { lane: OCT05, payload: `${OCT05}/derived/corrections.json`, cash: `${OCT05}/derived/corrections_cash.json`, edits: N5, cash_edits: N5C,
      band_bn: C5, cash_set_bn: C5cash, end_specifications: [48, 11],
      lineage: LIN_ITEM ? { item: LIN_ITEM, payload: PKG.LINEAGE_PAYLOADS.set, cash: PKG.LINEAGE_PAYLOADS.cash,
        rule: "the lineage item's additions replace v5's in place (v5's merge(), adoptLineage() and forCase() on the September 29 payloads; package.cjs rebase()), and the edit sets build on that base" }
        : "v5's (main_case_lineage_2026_10_05 arm b)" },
    items: P.CASE_ITEMS.map((r) => {
      const c = PC.CASE_ITEMS.find((x) => x.id === r.id), x = alone.find((y) => y.r.id === r.id);
      return { id: r.id, label: r.label, kind: r.kind, source: r.source, source_arm: r.source_arm || null, applied: r.applied,
        edits: r.edits || null, lineage_edits: r.lineage_edits || null, meta_changed: r.meta_changed || [],
        cash: c.applied ? { applied: true, edits: c.edits || null, lineage_edits: c.lineage_edits || null } : { applied: false, why: c.why },
        arms: Object.keys(r.arms || {}), factors: r.factors || null,
        alone_on_v5: x ? { band_bn: bandOf(x.costs), cash_set_bn: cashBand(x) || C5cash, source_band_bn: r.source_band_bn,
          source_cash_band_bn: r.kind === "lineage" ? r.source_cash_band_bn : (c.applied ? c.source_band_bn : null) } : null };
    }),
    per_member_usd: { set: C.map(PER), cash: Ccash.map(PER), population: L.counts.lineage_population },
    change_from_the_october_5_case_bn: [C[0] - C5[0], C[1] - C5[1]],
    change_from_the_october_5_cash_set_bn: [Ccash[0] - C5cash[0], Ccash[1] - C5cash[1]],
    change_at_every_specification: { by_allocation_bn: byAllocation(change), span_bn: spanOf(change),
      cash: { by_allocation_bn: byAllocation(cashChange), span_bn: spanOf(cashChange) },
      note: "the methods' mean change from v5 at each of the 64 specifications (consumer.cjs on v6's payload less on v5's); the package's runs equal it at every specification (1e-9)" },
    interactions: Object.fromEntries(pairs.map((q) => [q.ids.join("_x_"), { at_end_specifications_bn: atEnd(q.set), cash_at_end_specifications_bn: atEnd(q.cash),
      span_bn: spanOf(q.set), cash_span_bn: spanOf(q.cash) }]).concat([["remainder", { at_end_specifications_bn: atEnd(residual), cash_at_end_specifications_bn: atEnd(cashResidual),
      span_bn: spanOf(residual), cash_span_bn: spanOf(cashResidual) }]])),
    interactions_note: "each pair run alone on v5 (consumer.cjs), less v5 and the two items' own changes; remainder is the case's change less every item's and every pair's (zero: no three-way term). pension_tr2026 with added_age_mix is the pension edits' move from v5's added people to the age mix's, (f - 1) x their Social Security and Part A; retiree_health with added_age_mix is the line changes times the age mix's move in the group's shares of the service lines; user_fees with every other item is zero (fixed amounts on the union, carriers that cancel its own move of the capital keys on the model it applies to)",
    items_by_variant_row_bn: itemsByVariant,
    arms: Object.fromEntries(armRows.map((a) => [a.row, { item: a.item, arm: a.name, source_arm: a.source_arm, label: a.label, band_bn: a.band,
      end_specifications: a.ends, change_from_the_case_bn: a.change_from_the_case_bn, change_from_v5_bn: a.change_from_v5_bn,
      alone_on_v5_band_bn: a.alone_band_bn, alone_change_from_the_item_bn: a.alone_change_from_the_item_bn, source_band_bn: a.source_band_bn,
      cash: a.cash ? { band_bn: a.cash.band, change_from_the_cash_set_bn: a.cash.change_from_the_cash_set_bn, alone_on_v5_band_bn: a.cash.alone_band_bn,
        source_band_bn: a.cash.source_band_bn } : null }])),
    arms_note: "each arm is the whole case with that item at the arm and the others as they are (package.cjs caseOf with {item: arm}); alone_on_v5 is the arm on v5 by itself, which is its source lane's band",
    ...(companions ? { companions } : {}),
    ...(feesUnderSchool ? { user_fees: feesBlock() } : {}),
    ...(agePartsAt ? { lineage_item_parts: Object.fromEntries(["set", "cash"].map((w) => [w, Object.assign(Object.fromEntries(Object.entries(agePartsAt[w].parts)
      .map(([k, xs]) => [k, atEnd(xs)])), { worst_sum_gap_bn: agePartsAt[w].worst_sum_gap_bn, worst_end_gap_bn: agePartsAt[w].worst_end_gap_bn })])) } : {}),
    slots: P.SLOTS,
    payload: { file: "derived/corrections.json", cash: "derived/corrections_cash.json", stamped: P.STAMPED,
      from: { set: [`${OCT05}/derived/corrections.json (its first ${payload29.edits.length} edits)`, LIN_ITEM ? `the lineage block: ${PKG.LINEAGE_PAYLOADS.set} (item ${LIN_ITEM})` : `the lineage block: ${P.LINEAGE_FILES.set}`, "package.cjs REGISTRY: the edit sets' edits, appended"],
        cash: [`${OCT05}/derived/corrections_cash.json (its first ${cash29.edits.length} edits)`, LIN_ITEM ? `the lineage block: ${PKG.LINEAGE_PAYLOADS.cash} (item ${LIN_ITEM})` : `the lineage block: ${P.LINEAGE_FILES.cash}`, `package.cjs REGISTRY: the cash edit sets' edits${PC.ITEM_EDITS.length ? "" : " (none)"}`] },
      built_by: `${P.LANE}/package.cjs caseOf(), rebase(), forItems()` },
    variants_rule: "an option leaves the fixed-amount items' edits (pension_tr2026, user_fees) at the case's, as it leaves the added people's amounts (package.cjs withItems, which stops on an option that changes the national total of a line such an item edits, against the case's totals at that item's step, or turns the pension switch off); retiree_health's edits are the option's own national totals plus the item's change (editsAt); user_fees's carriers are computed on the option's model, so its capital re-keys hold under every option, and an option that re-keys a component it offsets (the pupil share) drops that offset; a lineage item's added people follow v5's rule (followNationals); range.items_at_the_case_data measures what the fixed amounts leave out for the pension item",
    history: "first_year_response, schools_case, sept27_case, sept29_case, oct05_case, sept29_cash_set, oct05_cash_set, adopted_2026_09_2x and adopted_2026_10_05, the three September 27 additions, each_addition's earlier entries, change_at_fixed_specifications.oct05_case, the schools_case rows of the other profiles, enterprises.capital_lane_rows_before_rental_assistance, enterprises.interest, beside_the_account.congestion, group_receipts_bn's earlier entries and the v4 and v5 blocks are v5's values (its summary.json and main_case_bands.csv)",
    inputs: Object.fromEntries([`${OCT05}/derived/summary.json`, `${OCT05}/derived/main_case_bands.csv`, `${OCT05}/derived/per_spec.csv`,
      `${OCT05}/derived/corrections.json`, `${OCT05}/derived/corrections_cash.json`]
      .concat(P.REGISTRY.filter((it) => APPLIED.some((r) => r.id === it.id)).flatMap((it) => Object.values(it.source.files)))
      .concat(companions ? Object.values(PKG.COUNT.FILES).concat([`${LINEAGE}/derived/v5_summary.json`, AS.SHARES_FILE, AS.PENSION_ARMS],
        ["model_G1.json", "model_G2.json", "model_G3plus.json", "generation_corrections_sept29.json", "generation_corrections_sept29_cash.json"].map((f) => `generation_account_2026_09_24/derived/${f}`))
        .filter((f, k, xs) => xs.indexOf(f) === k) : [])
      .concat(["assumption_explorer_2026_09_21/engine.js", "assumption_explorer_2026_09_21/derived/model.json"]).map((f) => [f, sha256(f)])),
  };
}
const summary = {
  lane: P.LANE,
  decision: P.DECISION,
  adopted_2026_09_23: s29.adopted_2026_09_23, adopted_2026_09_24: s29.adopted_2026_09_24,
  adopted_2026_09_26: s29.adopted_2026_09_26, adopted_2026_09_26_schools: s29.adopted_2026_09_26_schools,
  adopted_2026_09_27: s29.adopted_2026_09_27,
  adopted_2026_09_29: s29.main_case,
  ...(ON ? { adopted_2026_10_05: s5.main_case } : {}),
  first_year_response: s29.first_year_response, schools_case: s29.schools_case,
  uncorrected_at_adopted_responses: uncorrectedAtResponses, without_capital_return: withoutCapital,
  main_case: C,
  cash_set: { band_bn: Ccash, by_method_bn: Object.fromEntries(METHODS.map((m, k) => [m, ownBands(cashCosts)[k]])), end_specifications: cashEnds,
    change_from_main_case_bn: [Ccash[0] - C[0], Ccash[1] - C[1]], change_from_the_september_29_cash_set_bn: cashTotal,
    ...(ON ? { change_from_the_october_5_cash_set_bn: [Ccash[0] - C5cash[0], Ccash[1] - C5cash[1]] } : {}),
    note: ON ? `the set with the pension switch off (pension4 "cash"): social security and Medicare's Part A at the group's current benefits instead of the accrual at payable benefits net of the tax on benefits, so no Trustees path enters it; the payload is derived/corrections_cash.json (${OCT05}/derived/corrections_cash.json with ${LIN_ITEM ? `item ${LIN_ITEM}'s lineage block in place of v5's (derived/lineage_payload_cash.json), ` : ""}${PC.ITEM_EDITS.length ? `the cash edit sets' ${PC.ITEM_EDITS.length} edits after the lineage's` : "no edit set"}, the stamps and meta.items)`
      : `the set with the pension switch off (pension4 "cash"): social security and Medicare's Part A at the group's current benefits instead of the accrual at payable benefits net of the tax on benefits; the payload is derived/corrections_cash.json (${P.BASE_FILES.cash} with ${P.LINEAGE_FILES.cash} merged in)` },
  change: ON ? [C[0] - C5[0], C[1] - C5[1]] : [C[0] - C4[0], C[1] - C4[1]],
  change_at_fixed_specifications: ON ? {
    items: Object.fromEntries(itemParts.map((x) => {
      const sum = (prefix) => { const ps = Object.entries(x.set.parts).filter(([n]) => n.startsWith(prefix)); return ps.length ? [0, 1].map((e) => ps.reduce((a, [, v]) => a + v[e], 0)) : null; };
      return [x.id, Object.assign({ total: x.set.total, parts: x.set.parts }, sum("union_") ? { union: sum("union_"), lineage: sum("lineage_") || [0, 0] } : {},
        x.set.split ? { union: x.set.split.union, lineage: x.set.split.lineage, capital_return: x.set.split.capital_return } : {},
        x.set.members ? { members: x.set.members } : {}, x.cash ? { cash: x.cash } : {})];
    })),
    interactions: Object.fromEntries(pairs.map((q) => [q.ids.join("_x_"), atEnd(q.set)]).concat([["remainder", atEnd(residual)]])),
    total: itemsTotal,
    note: `v6's change from v5 at each method's end specifications (48 low, 11 high in both cases), averaged, by item: an item's total is the case with that item alone on v5 less v5, and its parts are, for cell shifts, each part's amount at the end's allocation times its line's response; for national-scale edits, each line's amount move times its response and the capital return's move (union and lineage then split them by the union's and the added people's cells); for the lineage item, its part models run one at a time (G3-rate and later persons; members by G3+ members and whites). Union and lineage group the parts of the identified 39.71M and of the 3.04M added people. The items' totals and the pairs' interactions (each pair alone on v5 less its two items) add to total, which is change because the ends do not move; cash holds the same for the cash set. oct05_case holds v5's own change from the September 29 case, by part of the lineage line, with the September 29 case's under oct05_case.sept29_case`,
    oct05_case: s5.change_at_fixed_specifications } : {
    union_response_move: unionMove, g3plus_members: linG3, whites: linW, total,
    note: `the change from the September 29 case at each method's end specifications (48 low, 11 high in both cases), averaged, by part of the lineage line: union_response_move is v4's model with audit row 8's change evaluated at v5's group-size responses less v4; g3plus_members and whites are the added people (${(L.members.g3plus / 1e6).toFixed(4)}M priced as identified G3+ members, ${(L.members.white / 1e6).toFixed(4)}M as third-plus non-Hispanic whites at the G3+'s ages), split as the lineage lane splits them (${LINEAGE}/derived/v5_summary.json). The parts add to total, which is change because the ends do not move. sept29_case holds the September 29 case's own change from the September 27 case, by v4 item, with the September 27 case's parts under sept29_case.sept27_case`,
    sept29_case: s29.change_at_fixed_specifications },
  end_specifications: endSpecs,
  lines_at_end_specifications: lineAtEnds,
  receipts_at_end_specifications: receiptsAtEnds,
  capital_at_end_specifications: capitalAtEnds,
  enterprises: { option: ENTERPRISES, allowed_by_file: ENTERPRISES_ALLOWED, receipt_response: 1,
    receipt_at_end_specifications: { group_amount_bn: esAmount, national_bn: esNat, cost_bn: atEnds(newEnds, (m, i) => esCost(newRuns[m][i])),
      move_from_the_schools_case_bn: receiptMove, of_which_rekey_bn: moveRekey, of_which_public_housing_split_bn: moveSplit },
    returns_at_end_specifications_bn: atEnds(newEnds, (m, i) => capitalGroup(newRuns[m][i], "enterprise")), public_housing_return_bn: publicHousing,
    receipt_rekey: payload.meta.enterprise_receipt_rekey,
    rekey_effect_at_fixed_specifications_bn: rekeyEffect,
    option_A_band_bn: optionA, at_model_json_share_band_bn: atModelShare,
    capital_lane_rows_before_rental_assistance: s29.enterprises.capital_lane_rows_before_rental_assistance,
    overlap_with_rental_assistance: overlap,
    interest: s29.enterprises.interest,
    proportional_reference: s29.enterprises.proportional_reference,
    public_housing: s29.enterprises.public_housing },
  school: { rules: P.RULES, within_district: schoolLow, within_district_as_response: schoolLowAsResponse,
    end_specifications: { average: newEnds, within_district: schoolLowEnds.ends, within_district_as_response: schoolLowAsResponseEnds.ends },
    note: "the schools case's low side on this case: every specification re-run with that school rule (the K-12 capital return follows the school response); the within-district response is read at v4's pupil share, without the added people's pupils; end_specifications are [low end, high end] per fill-in method",
    sign_break_even: s29.school.sign_break_even },
  rental_assistance: { group_amount_by_method_bn: Object.fromEntries(METHODS.map((m, k) => [m, Object.fromEntries(ALLOCS.map((a, j) => [a, rentalAmount[k][j]]))])),
    uncorrected_group_amount_bn: Object.fromEntries(ALLOCS.map((a, j) => [a, rentalUncorrected[j]])),
    note: `${s29.rental_assistance.note}; the corrected amount includes the added people's`,
    overlap_netted_bn: 0 },
  responses: P.RESPONSES,
  range: { low_end: rangeLowEnd, high_end: rangeHighEnd, overall: [rangeLowEnd[0], rangeHighEnd[1]], quadrature,
    note: `every component re-runs the whole case, the added people included, at every specification; the band's ends are minima and maxima over the specifications; option A, 7% and items 8 and 10 are beside the range, not in it. The components are the September 29 case's; ${skipped.join(", ")} moves nothing (item 8 is beside the case). The added people's own amounts are the case's in every variant (package.cjs); first_order lists the variants whose own group-size reading is moved at first order or kept at v4's group`,
    first_order: FIRST_ORDER,
    at_the_case_data: { components: atCaseData, added_share: addedShare, range_ends_move_if_proportional_bn: atCaseDataMove,
      note: "these components re-run the union's data with the added people's amounts at the case's, so each deviates as on the September 29 case (within $0.001bn); range_ends_move_if_proportional_bn is how far the range's low and high ends would move had the added people's amounts moved in proportion to the union's (the added share of each component's deviation), an indication of the omission, not a bound" },
    ...(ON ? { items_at_the_case_data: itemsAtCaseData } : {}) },
  other_profiles: otherProfiles, old_main_profile: oldProfile,
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn,
  each_addition: ON ? Object.assign({}, s5.each_addition, Object.fromEntries(APPLIED.map((r, k) => [r.id, bandOf(aloneCosts[k])])))
    : Object.assign({}, s29.each_addition, { lineage: C }),
  beside_the_account: {
    rate_7pct: { band_bn: at7, return_at_end_specifications_bn: atEnds(newEnds, (m, i) => runs7[m][i].capital.total_bn), note: s29.beside_the_account.rate_7pct.note },
    land_per_10pct_of_land_to_structure_value: land,
    enterprises_out_option_A: { band_bn: optionA, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => optionARuns[m][i].cost_bn - newCosts[m][i]),
      note: s29.beside_the_account.enterprises_out_option_A.note },
    rental_assistance_at_0: { band_bn: rentalAt0, note: s29.beside_the_account.rental_assistance_at_0.note },
    congestion: ON ? Object.assign({}, s5.beside_the_account.congestion, { not_recomputed_v6: "the September 27 figure, carried by the September 29 and October 5 lanes; the items do not reprice it" })
      : Object.assign({}, s29.beside_the_account.congestion, { not_recomputed_v5: "the September 27 figure, carried by the September 29 lane; not recomputed with the added people" }),
    transit_at_riders_key_item_8: { band_bn: with8, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => runs8[m][i].cost_bn - newCosts[m][i]),
      options: beside8.o, note: `${beside8.name}: beside the case (candidate v4's BESIDE_ITEMS), not in it` },
    uninsured_use_0_7x_item_10: { band_bn: with10, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => runs10[m][i].cost_bn - newCosts[m][i]),
      options: beside10.o, note: `${beside10.name}: beside the case (candidate v4's BESIDE_ITEMS), not in it` },
  },
  by_side_vs_uncorrected_at_adopted_responses: sides,
  group_receipts_bn: groupReceipts,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi, variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
  v4: s29.v4,
  v5: ON ? s5.v5 : {
    adopted: "2026-10-05, the operator (whole people, arm b), through the parent's brief",
    lineage_lane: LINEAGE,
    lineage: L,
    per_member_usd: { set: C.map(PER), cash: Ccash.map(PER), population: L.counts.lineage_population },
    change_from_the_september_29_case_bn: total,
    lineage_by_variant_row_bn: lineageByVariant,
    payload: { file: "derived/corrections.json", cash: "derived/corrections_cash.json", stamped: P.STAMPED,
      from: { set: [P.BASE_FILES.set, P.LINEAGE_FILES.set], cash: [P.BASE_FILES.cash, P.LINEAGE_FILES.cash] }, merged_by: `${P.LANE}/package.cjs merge(), adoptLineage()` },
    variants_rule: "an option that changes the union's data leaves the added people's amounts at the case's; an option that changes a line's national total scales the added people's amount on it, and a part split off a line takes that line's key (package.cjs followNationals: item 8's transit split and the property range's case-scaled tenant national, gated); candidate v4's route (item options) keys the road capital on the evaluation, as the case does (package.cjs viaCandidate, gated equal to the case at its own options)",
    group_size_rule: "a specification's reading moves as package.cjs moveSpec() sets: the case's v4 reading becomes v5's; 0 and 1 stay; general government without finite removal stays; the long-run lines, road lines and recreation's state price are re-derived for the specification's long-run variant at v5's subfunction responses; any other reading moves by the case's change (first order)",
    history: "first_year_response, schools_case, sept27_case, sept29_case, sept29_cash_set, adopted_2026_09_2x, the three September 27 additions, each_addition's earlier entries, change_at_fixed_specifications.sept29_case, the schools_case rows of the other profiles, enterprises.capital_lane_rows_before_rental_assistance, enterprises.interest, beside_the_account.congestion and the v4 block are the September 29 lane's values (its summary.json and main_case_bands.csv)",
    inputs: Object.fromEntries([`${SEPT29}/derived/summary.json`, `${SEPT29}/derived/main_case_bands.csv`, `${SEPT29}/derived/per_spec.csv`, `${SEPT29}/derived/corrections.json`,
      `${CAND}/derived/corrections_v4_cash.json`, P.LINEAGE_FILES.set, P.LINEAGE_FILES.cash, P.POPULATION_FILE, `${LINEAGE}/derived/v5_summary.json`,
      "assumption_explorer_2026_09_21/engine.js", "assumption_explorer_2026_09_21/derived/model.json"].map((f) => [f, sha256(f)])),
  },
  ...(ON ? { v6: v6Block() } : {}),
};
fs.writeFileSync(path.join(OUT, "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "components.csv"), compCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "corrections.json"), JSON.stringify(payload, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "corrections_cash.json"), JSON.stringify(cashPayload, null, 1) + "\n");
// A lineage item's additions, in the lineage lane's payload format: meta.lineage.payload names these files.
if (LIN_ITEM) {
  fs.writeFileSync(path.join(OUT, "lineage_payload.json"), JSON.stringify(IB.ADDITION.set, null, 1) + "\n");
  fs.writeFileSync(path.join(OUT, "lineage_payload_cash.json"), JSON.stringify(IB.ADDITION.cash, null, 1) + "\n");
}

console.log("\n[result]");
console.log(`  September 29 case               ${f2(C4)}`);
console.log(`  main case                       ${f2(C)}  ends ${newEnds.map((e) => e.join("/")).join(", ")}; $${C.map((x) => Math.round(PER(x))).join(" / ")} per member`);
console.log(`  cash set                        ${f2(Ccash)}`);
console.log(`    change: union response move ${f2(unionMove)}, G3+ members ${f2(linG3)}, whites ${f2(linW)}, total ${f2(total)}`);
console.log(`  without the capital return      ${f2(withoutCapital)}`);
console.log(`  option A (beside)               ${f2(optionA)}`);
console.log(`  at 7% (beside)                  ${f2(at7)}`);
console.log(`  general government at 0         ${f2(ggFixed)}`);
console.log(`  uncorrected at the responses    ${f2(uncorrectedAtResponses)}`);
console.log(`  range                           ${rangeLowEnd[0].toFixed(1)}–${rangeHighEnd[1].toFixed(1)} (quadrature ${quadrature[0].toFixed(1)}–${quadrature[1].toFixed(1)})`);
console.log(`    at the case's data: ${atCaseData.join(", ")}; ends ${f2(atCaseDataMove)} had the added people moved in proportion`);
for (const [pf, v] of Object.entries(otherProfiles)) console.log(`  ${pf.padEnd(31)} ${f2(v.adopted)}`);
console.log(`  old main profile                ${f2(oldProfile.with_rental_assistance_capital_and_enterprises)}`);
if (!ON) for (const [v, d] of Object.entries(lineageByVariant)) console.log(`    lineage under ${v.padEnd(40)} ${f2(d)}`);
for (const x of components) console.log(`    range: ${x.name.padEnd(18)} low end ${x.lo[0].toFixed(2)}..+${x.hi[0].toFixed(2)}  high end ${x.lo[1].toFixed(2)}..+${x.hi[1].toFixed(2)}`);
if (ON) {
  console.log(`  v5 (the base)                   ${f2(C5)}; cash ${f2(C5cash)}`);
  console.log(`  v6 less v5                      ${f2([C[0] - C5[0], C[1] - C5[1]])}; at every specification ${ALLOCS.map((a) => `${a} ${f2(spanOf(change.filter((_, i) => specs[i].allocation === a)))}`).join(", ")}`);
  console.log(`  cash set less v5's               ${f2([Ccash[0] - C5cash[0], Ccash[1] - C5cash[1]])}`);
  for (const x of itemParts) console.log(`    item ${x.id}: ${f2(x.alone)}${x.cash ? `, cash ${f2(x.cash.total)}` : ""} = ${Object.entries(x.set.parts).filter(([, v]) => Math.abs(v[0]) + Math.abs(v[1]) > 5e-3).map(([n, v]) => `${n} ${f2(v)}`).join(" + ")}`);
  for (const q of pairs) console.log(`    interaction ${q.ids.join(" x ")}: ${f2(atEnd(q.set))}; cash ${f2(atEnd(q.cash))}`);
  for (const a of armRows) console.log(`  arm ${a.row.padEnd(34)} ${f2(a.band)} (from the case ${f2(a.change_from_the_case_bn)})${a.cash ? `; cash ${f2(a.cash.band)} (${f2(a.cash.change_from_the_cash_set_bn)})` : ""}`);
  if (companions) {
    for (const [n, o] of Object.entries(companions.options)) {
      console.log(`  lineage ${n.padEnd(11)} ${f2(o.set.band_bn)} (from the case ${f2(o.set.change_from_the_case_bn)}; v5 at the option ${f2(o.set.v5_at_option_band_bn)}; age mix ${f2(o.set.age_mix_at_option_bn)}); cash ${f2(o.cash.band_bn)}`);
    }
    for (const w of ["set", "cash"]) for (const r of companions.ancestry_share[w].rows) {
      console.log(`  ancestry share, ${w} ${r.scenario.padEnd(13)} ${f2(r.band_bn)} at ${r.ends.join("/")} (v5 ${f2(r.v5_band_bn)}; age mix ${f2(r.age_mix_bn)})`);
    }
  }
  for (const [v, d] of Object.entries(itemsByVariant)) console.log(`    items under ${v.padEnd(42)} ${f2(d)}`);
  if (itemsAtCaseData.pension_tr2026_at_the_case_receipts) console.log(`  pension item at the case's receipts: worst ${itemsAtCaseData.pension_tr2026_at_the_case_receipts.worst_bn.toFixed(4)}bn (${itemsAtCaseData.pension_tr2026_at_the_case_receipts.worst_variant})`);
}
console.log("all gates passed");
