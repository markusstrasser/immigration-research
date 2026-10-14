/* Main case v7, the candidate (decisions/2026-10-14-main-case-v7.md, which the parent writes): main case v6
 * (main_case_2026_10_07, adopted 2026-10-07) plus items personal_allocation, child_credits, job_capital_taxes,
 * white_end_tax_keys and row4_frame (package.cjs), written to v6's output contract (main_case_2026_10_07/derived: main_case_bands.csv, components.csv,
 * per_spec.csv, summary.json, corrections.json, corrections_cash.json and the lineage payloads here; sign_reversal.cjs
 * writes sign_reversal.csv). package.cjs holds the definitions; this script runs the gates and writes derived/.
 *
 * Every v6 file, column, row name and key is kept, with v7's value where the quantity is defined on v7. The rows and
 * keys that record how earlier cases were built keep v6's values (history), and v6's own block (summary.json v6) is
 * history too. One block moves, as on October 5 and 7: change_at_fixed_specifications holds v7's change from v6, by
 * item, part and interaction, so v6's (the items' change from v5, with v5's under it) sits under
 * change_at_fixed_specifications.oct07_case. Added: the band rows oct07_case and oct07_cash_set; <item>_alone (each new
 * item alone on v6, at v6's allocation rule for the edit sets); the arms of item job_capital_taxes
 * (job_capital_taxes_<arm>, with _cash_set); shared_allocation (with _cash_set); per_spec.csv's columns in_band,
 * oct07_cost_bn, item_<id>_bn for each edit set and items_v7_interaction_bn, last; the summary block v7
 * and the keys adopted_2026_10_07, cash_set.change_from_the_october_7_cash_set_bn, each_addition.<item>,
 * group_receipts_bn.adopted_2026_10_07 and beside_the_account.congestion.not_recomputed_v7.
 *
 * The case's band is the minimum and maximum over the 32 personal specifications (0-31 in v6's numbering), each fill-in
 * method's, averaged; per_spec.csv carries all 64 per method with in_band marking the 32. Items child_credits and
 * job_capital_taxes read their worker lanes' derived/item.json (sources.cjs; both lanes have delivered); items
 * white_end_tax_keys and row4_frame port the row-4 class lane's pricing (item_row4.cjs). A gate that reads a stub prints
 * [STUB], and so do the result lines.
 *
 * Gates (exit 1 and nothing written on failure):
 *   G1  v6 re-derives (its package gives v6's per_spec.csv cost at every specification and method, its band and cash
 *       set, exactly; its payloads are v6's files); the case at all 64 specifications is v6 plus the items' change, the
 *       methods' mean (1e-9), the change being consumer.cjs on v7's payload less consumer.cjs on v6's, and the cash set
 *       likewise; v6 at the personal allocation is the review's $405.786-461.480bn at 16 / 11; the ends are found by the
 *       methods over the 32 case specifications, set and cash; each new item alone on v6 matches its source lane
 *       (child_credits: its net plus the added people's term at every personal specification and nothing at the
 *       shared ones; job_capital_taxes: the four lines' targets are the lane's amounts, national totals hold, its
 *       change is minus the responses times the amounts' move, and gates 4(a) and 4(b) on a control keyed at the
 *       case's own wage key; white_end_tax_keys and row4_frame: the row-4 class lane's moves at 48 / 11, row4_oct07.json,
 *       and its recorded inputs; personal_allocation: v6's costs at the personal specifications exactly); each pair's
 *       interaction is run and what the pairs leave is zero; the payload models give the methods' mean (1e-9), so does consumer.cjs, and
 *       v7's payload model is v6's with the items' edits applied, exactly; the four new responses are in every case
 *       specification; the production module's capital-tax term is 0 at every case specification's production cell.
 * Run from anywhere: node main_case.cjs [--out-dir DIR] -> derived/main_case_bands.csv, components.csv, per_spec.csv,
 * summary.json, corrections.json, corrections_cash.json, lineage_payload.json, lineage_payload_cash.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const argv = process.argv.slice(2);
const PKG = require("./package.cjs");
const P = PKG;
const Consumer = require(path.join(__dirname, "..", "main_case_candidate_v4_2026_09_29", "consumer.cjs"));
const AS = require("./ancestry_share.cjs");
const { Engine, MODEL, FISCAL, HERE, ALLOCS, METHODS, CAP, PARTS, PROFILES, MAIN_PROFILE, LR_LINES, RENTAL, RATES, ENTERPRISES,
  ENTERPRISES_ALLOWED, ENTERPRISE_LINE, V4PKG: V4, gateState, gate, near, f2, csvRows, readJson, withCentral, specsFor, modelFor,
  evaluateFull, evalPackage, central, correctionsPayload, populationShare, sha256 } = P;
const P4 = P.SEPT29, PC = P.CASH, PC4 = P.SEPT29_CASH;
const B6 = P.OCT07, B6C = P.OCT07_CASH, B5 = P.OCT05;
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
const SRC = { child_credits: PKG.CREDITS.S, job_capital_taxes: PKG.JOBCAP.S };
const SRC7 = { white_end_tax_keys: PKG.ROW4.SOURCES_7, row4_frame: PKG.ROW4.SOURCES_8 };
const STUB = Object.values(SRC).some((s) => s.stub);
const ST = (id) => (SRC[id] && SRC[id].stub ? "[STUB] " : "");
const STALL = STUB ? "[STUB] " : "";

const SEPT29 = "main_case_2026_09_29";
const LINEAGE = P.LINEAGE_LANE;
const CAND = "main_case_candidate_v4_2026_09_29";
const OCT05 = "main_case_2026_10_05";
const OCT07 = "main_case_2026_10_07";
const NEW = PKG.NEW_IDS;
const V6CAND = PKG.V6_PACKAGE.CANDIDATE.slice();
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const ex = (x) => x.toExponential(1);
const fx = (x) => x.toFixed(4);
const clone = (x) => JSON.parse(JSON.stringify(x));
const minus = (a, b) => [a[0] - b[0], a[1] - b[1]];
const spanOf = (xs) => [Math.min(...xs), Math.max(...xs)];
const endsOf = (xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))];

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
const consumerCosts = (pl) => Consumer.evaluateAll(JSON.parse(JSON.stringify(pl)), { engine: Engine, model: MODEL }).map((x) => x.cost_bn);

const s29 = readJson(`${SEPT29}/derived/summary.json`);
const bands29 = csvRows(`${SEPT29}/derived/main_case_bands.csv`);
const ps29 = csvRows(`${SEPT29}/derived/per_spec.csv`);
const payload29 = readJson(`${SEPT29}/derived/corrections.json`);
const cash29 = readJson(`${CAND}/derived/corrections_v4_cash.json`);
const POP = P.POP;
const CAPDIR = "capital_return_services_2026_09_27/derived";
const capGaps = csvRows(`${CAPDIR}/gaps.csv`);
const COMPONENTS = P.componentsFor(null);
const s6 = readJson(`${OCT07}/derived/summary.json`);
const bands6 = csvRows(`${OCT07}/derived/main_case_bands.csv`);
const bandsRaw6 = fs.readFileSync(path.join(FISCAL, OCT07, "derived", "main_case_bands.csv"), "utf8").trim().split("\n");
const ps6 = csvRows(`${OCT07}/derived/per_spec.csv`);
const payload6 = readJson(`${OCT07}/derived/corrections.json`);
const cashPayload6 = readJson(`${OCT07}/derived/corrections_cash.json`);
const row29 = (profile, variant) => {
  const r = bands29.find((x) => x.profile === profile && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] the September 29 bands lack ${profile}/${variant}`);
  return r;
};
const row6 = (profile, variant) => {
  const r = bands6.find((x) => x.profile === profile && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] v6's bands lack ${profile}/${variant}`);
  return r;
};
const rawRow6 = (profile, variant) => {
  const r = bandsRaw6.find((l) => l.startsWith(`${profile},${variant},`));
  if (!r) throw new Error(`[BLOCKED] v6's bands lack ${profile}/${variant}`);
  return r;
};
const APPLIED = P.V7_ITEMS.filter((r) => r.applied);
const APPLIED_CASH = PC.V7_ITEMS.filter((r) => r.applied);
const EDIT_SETS = APPLIED.filter((r) => r.kind === "edit_set");
const N6 = payload6.edits.length, N6C = cashPayload6.edits.length;
const payload = correctionsPayload();
const cashPayload = PC.correctionsPayload();
const L = payload.meta.lineage;
const REF = MODEL.receipts.reference;
const JC_LINES = PKG.JOBCAP.LINES;

// ---------------------------------------------------------------------------------------------------
console.log(`[G1: v6 and the items' change]${STUB ? " [STUB inputs: see RESULT.md]" : ""}`);
for (const [id, s] of Object.entries(SRC)) console.log(`  ${s.stub ? "[STUB]" : "[DATA]"} item ${id}: ${s.file} (sha256 ${s.sha256.slice(0, 12)}); lane verdict: ${s.verdict || "none"}`);
const ALL = P.ALL_SPECS, specs = P.MAIN_SPECS, SHARED = P.SHARED_SPECS;
const IN_BAND = ALL.map((s) => s.allocation === "personal");
const NP = specs.length;
const strip7 = (s) => { const x = clone(s); for (const id of JC_LINES) delete x.line_responses[`receipt:${id}`]; return x; };
gate("the case's specifications are v6's personal ones (0-31) and SHARED_SPECS v6's shared ones (32-63), in v6's numbering; ALL_SPECS is all 64",
  ALL.length === 64 && NP === 32 && SHARED.length === 32 && IN_BAND.every((b, i) => b === (i < 32))
  && specs.every((s, i) => JSON.stringify(s) === JSON.stringify(ALL[i])) && SHARED.every((s, j) => JSON.stringify(s) === JSON.stringify(ALL[32 + j])),
  `${NP} personal, ${SHARED.length} shared`);
gate("ALL_SPECS are v6's 64 specifications with item job_capital_taxes's four receipt responses added to line_responses (every other field and line response identical)",
  ALL.every((s, i) => JSON.stringify(strip7(s)) === JSON.stringify(B6.MAIN_SPECS[i])), "64 specifications");
const allRuns = runs(ALL);
const allCosts = costsOf(allRuns);
const newRuns = allRuns.map((xs) => xs.slice(0, NP)), newCosts = allCosts.map((xs) => xs.slice(0, NP));
const newEnds = ends(newCosts);
const C = central({});
const cashModels = METHODS.map((m) => PC.modelFor("central", m, PC.withCentral({})));
const cashAllRuns = runs(PC.ALL_SPECS, MAIN_PROFILE, cashModels, PC);
const cashAllCosts = costsOf(cashAllRuns);
const cashRuns = cashAllRuns.map((xs) => xs.slice(0, NP)), cashCosts = cashAllCosts.map((xs) => xs.slice(0, NP));
const cashEnds = ends(cashCosts);
const Ccash = PC.central({});
const ownBands = (cm) => cm.map((xs) => [Math.min(...xs), Math.max(...xs)]);
gate("central() is the methods' mean of each method's minimum and maximum over the 32 case specifications, set and cash (1e-9)",
  [0, 1].every((e) => near(C[e], bandOf(newCosts)[e], 1e-9) && near(Ccash[e], bandOf(cashCosts)[e], 1e-9)), `${f2(C)}; cash ${f2(Ccash)}`);

// The base: v6.
const baseModels = METHODS.map((m) => B6.modelFor("central", m, B6.withCentral({})));
const baseAllRuns = runs(B6.MAIN_SPECS, MAIN_PROFILE, baseModels, B6);
const baseAllCosts = costsOf(baseAllRuns);
const baseCosts = baseAllCosts.map((xs) => xs.slice(0, NP));
const C6 = B6.central({}), C6cash = B6C.central({});
const baseCashAllRuns = runs(B6C.MAIN_SPECS, MAIN_PROFILE, METHODS.map((m) => B6C.modelFor("central", m, B6C.withCentral({}))), B6C);
const baseCashAll = costsOf(baseCashAllRuns), baseCash = baseCashAll.map((xs) => xs.slice(0, NP));
gate("the base is v6: its package gives v6's per_spec.csv cost at every one of the 128 rows, and v6's band and cash set (summary.json), exactly",
  METHODS.every((meth, k) => B6.MAIN_SPECS.every((_, i) => String(baseAllCosts[k][i]) === ps6.find((r) => r.method === meth && Number(r.spec) === i).cost_bn))
  && B6.MAIN_SPECS.length === 64 && C6[0] === s6.main_case[0] && C6[1] === s6.main_case[1] && C6cash[0] === s6.cash_set.band_bn[0] && C6cash[1] === s6.cash_set.band_bn[1],
  `${f2(C6)}; cash ${f2(C6cash)}`);
gate("the base's payloads are v6's derived files, its stamps v6's (adopted 2026-10-07)", JSON.stringify(B6.correctionsPayload()) === JSON.stringify(payload6)
  && JSON.stringify(B6C.correctionsPayload()) === JSON.stringify(cashPayload6) && payload6.meta.adopted === "2026-10-07");
const c6 = consumerCosts(payload6), cc6 = consumerCosts(cashPayload6);
const c7 = consumerCosts(payload), cc7 = consumerCosts(cashPayload);
const change = c7.map((x, i) => x - c6[i]), cashChange = cc7.map((x, i) => x - cc6[i]);
const atSpec = ALL.map((_, i) => mean(allCosts.map((xs, m) => xs[i] - baseAllCosts[m][i])));
const g1 = worst(atSpec.map((x, i) => x - change[i]));
gate(`${STALL}the case at all 64 specifications is v6 plus the items' change (the methods' mean; the change is consumer.cjs on v7's payload less on v6's; 1e-9)`,
  g1 < 1e-9, `max |diff| ${ex(g1)}; change ${f2(spanOf(change.slice(0, NP)))} at the personal specifications, ${f2(spanOf(change.slice(NP)))} at the shared`);
const cg = worst(PC.ALL_SPECS.map((_, i) => mean(cashAllCosts.map((xs, m) => xs[i] - baseCashAll[m][i])) - cashChange[i]));
gate(`${STALL}the cash set is v6's plus the cash items' change at every specification (consumer.cjs on v7's cash payload less on v6's, 1e-9)`, cg < 1e-9,
  `max |diff| ${ex(cg)}; change ${f2(spanOf(cashChange.slice(0, NP)))} personal`);
const v6Personal = bandOf(baseCosts), v6PersonalEnds = ends(baseCosts), v6PersonalCash = bandOf(baseCash), v6PersonalCashEnds = ends(baseCash);
gate("v6 at the personal allocation is the review's $405.786-461.480bn, ends 16 / 11 in both methods (the v6 assumption review, item 1; 3 decimals)",
  v6Personal[0].toFixed(3) === "405.786" && v6Personal[1].toFixed(3) === "461.480" && v6PersonalEnds.every((e) => e[0] === 16 && e[1] === 11),
  `${f2(v6Personal)} at ${v6PersonalEnds.map((e) => e.join("/")).join(", ")}; cash ${f2(v6PersonalCash)} at ${v6PersonalCashEnds.map((e) => e.join("/")).join(", ")}`);
const sameEnds = (x) => x.every((e) => e[0] === x[0][0] && e[1] === x[0][1]);
gate(`${STALL}the ends, found by the methods: each method's minimum and maximum over the 32 case specifications, the same in both methods, set and cash`,
  sameEnds(newEnds) && sameEnds(cashEnds) && newEnds.every((e) => e[0] < NP && e[1] < NP),
  `set ${METHODS.map((m, k) => `${m} ${f2(ownBands(newCosts)[k])} at ${newEnds[k].join("/")}`).join("; ")}; cash at ${cashEnds.map((e) => e.join("/")).join(", ")}`);
const ENDS = newEnds[0], CASH_ENDS = cashEnds[0];
gate(`${STALL}the band is v6's personal costs plus the change at the end specifications (1e-9), and consumer.cjs's band over the personal specifications (meta.allocation.group_total) (1e-9); the cash set likewise`,
  [0, 1].every((e) => near(C[e], mean(newEnds.map((ij, m) => baseCosts[m][ij[e]] + change[ij[e]])), 1e-9) && near(C[e], spanOf(c7.filter((_, i) => IN_BAND[i]))[e], 1e-9)
    && near(Ccash[e], mean(cashEnds.map((ij, m) => baseCash[m][ij[e]] + cashChange[ij[e]])), 1e-9) && near(Ccash[e], spanOf(cc7.filter((_, i) => IN_BAND[i]))[e], 1e-9)),
  `${f2(C)} at ${ENDS.join("/")}; cash ${f2(Ccash)} at ${CASH_ENDS.join("/")}`);

// Each new item alone on v6 (the edit sets at v6's allocation rule, all 64; personal_allocation picks the 32).
const caseRuns = (Q, set) => { const X = set === "cash" ? Q.CASH : Q; return runs(X.MAIN_SPECS, MAIN_PROFILE, METHODS.map((m) => X.modelFor("central", m, X.withCentral({}))), X); };
const alone = APPLIED.map((r) => {
  const Q = PKG.caseOf(B5, V6CAND.concat([r.id]));
  const rs = caseRuns(Q, "set"), crs = caseRuns(Q, "cash");
  const out = { r, rc: PC.V7_ITEMS.find((x) => x.id === r.id), costs: costsOf(rs), cashCosts: costsOf(crs), nSpecs: Q.MAIN_SPECS.length,
    consumer: consumerCosts(Q.correctionsPayload()), cashConsumer: consumerCosts(Q.CASH_PAYLOAD), edits: Q.V7_EDITS, cashEdits: Q.CASH.V7_EDITS,
    payloadEdits: Q.correctionsPayload().edits.length, metaKeys: Object.keys(Q.correctionsPayload().meta), adopted: Q.correctionsPayload().meta.adopted,
    status: Q.correctionsPayload().meta.status };
  if (r.id === "job_capital_taxes") {
    out.runs = rs; out.cashRuns = crs; out.payloadModel = Q.payloadModel(); out.cashPayloadModel = Q.CASH.payloadModel(); out.detail = Q.ITEM_DETAIL.job_capital_taxes;
    out.record = Q.V7_ITEMS.find((x) => x.id === r.id); out.recordCash = Q.CASH.V7_ITEMS.find((x) => x.id === r.id);
  }
  if (["child_credits", "white_end_tax_keys", "row4_frame"].includes(r.id)) {
    out.runs = rs; out.cashRuns = crs; out.record = Q.V7_ITEMS.find((x) => x.id === r.id); out.recordCash = Q.CASH.V7_ITEMS.find((x) => x.id === r.id);
  }
  return out;
});
const aloneOf = (id) => alone.find((x) => x.r.id === id);
const aloneChange = (x, set) => (set === "cash" ? x.cashConsumer.map((v, i) => v - cc6[i]) : x.consumer.map((v, i) => v - c6[i]));
for (const x of alone) {
  if (x.r.kind !== "edit_set") continue;
  const d = aloneChange(x), dc = aloneChange(x, "cash");
  const pg = worst(ALL.map((_, i) => mean(x.costs.map((xs, m) => xs[i] - baseAllCosts[m][i])) - d[i]));
  const pc = worst(ALL.map((_, i) => mean(x.cashCosts.map((xs, m) => xs[i] - baseCashAll[m][i])) - dc[i]));
  gate(`${ST(x.r.id)}item ${x.r.id} alone: the package is v6 plus consumer.cjs's change at every one of the 64 specifications, set and cash (1e-9); its payload is a variant`,
    x.nSpecs === 64 && pg < 1e-9 && pc < 1e-9 && x.adopted === null && /^variant: /.test(x.status), `max |diff| ${ex(pg)} / ${ex(pc)}; change ${f2(spanOf(d))}`);
}
{
  // personal_allocation alone: v6's edits and costs, the 32 personal specifications, meta.allocation added.
  const x = aloneOf("personal_allocation");
  const same = x.costs.every((xs, m) => xs.length === NP && xs.every((v, i) => v === baseCosts[m][i])) && x.cashCosts.every((xs, m) => xs.every((v, i) => v === baseCash[m][i]));
  gate("item personal_allocation alone: v6's costs at the 32 personal specifications exactly, set and cash; no edit beyond v6's; meta.allocation added",
    same && x.payloadEdits === N6 && x.edits.length === 0 && x.metaKeys.includes("allocation") && near(bandOf(x.costs)[0], v6Personal[0], 1e-12) && near(bandOf(x.costs)[1], v6Personal[1], 1e-12),
    `${f2(bandOf(x.costs))}; cash ${f2(bandOf(x.cashCosts))}`);
}
let creditsCheck = null;
if (aloneOf("child_credits")) {
  // The lane's net at every personal specification, nothing at the shared ones; the lines respond at 1.
  const x = aloneOf("child_credits"), I = SRC.child_credits.data, NET = PKG.CREDITS.R.net + (PKG.CREDITS.LINEAGE ? P.ITEM_DETAIL.child_credits.set.lineage.scale * PKG.CREDITS.R.byGen.G3plus : 0);
  const d = aloneChange(x), dc = aloneChange(x, "cash");
  const gp = worst(d.map((v, i) => (IN_BAND[i] ? v - NET : v))), gc = worst(dc.map((v, i) => (IN_BAND[i] ? v - NET : v)));
  const lines = [...new Set(I.edits.map((e) => `${e.side}|${e.line}`))];
  const respOk = x.runs.concat(x.cashRuns).every((xs) => xs.every((r) => lines.every((k) => {
    const [side, id] = k.split("|");
    return (side === "receipt" ? receiptOf(r, id) : lineOf(r.evaluation, id)).response === 1;
  })));
  gate(`${ST("child_credits")}item child_credits alone is its source lane: the change is ${PKG.CREDITS.LINEAGE ? "the lane's net_bn plus the added people's G3+ term" : "the lane's net_bn"} ${NET.toFixed(6)} at every personal specification and 0 at every shared one, set and cash (1e-9), its lines (${lines.join(", ")}) at response 1 throughout`,
    gp < 1e-9 && gc < 1e-9 && respOk, `max |diff| ${ex(gp)} / ${ex(gc)}`);
  creditsCheck = { net_bn: NET, union_net_bn: PKG.CREDITS.R.net, added_people: PKG.CREDITS.LINEAGE, worst_gap_bn: Math.max(gp, gc), lines, reading: I.reading || null };
}
let jobcapCheck = null;
if (aloneOf("job_capital_taxes")) {
  const x = aloneOf("job_capital_taxes"), D = x.detail;
  const m6 = B6.payloadModel(), m7 = x.payloadModel, mc6 = B6C.payloadModel(), mc7 = x.cashPayloadModel;
  // The targets on the four lines are the lane's job-capital amounts (the parts' new amounts), at every scenario.
  let tgap = 0, natSame = true, cellTot = 0;
  for (const [mA, mB, det] of [[m7, m6, D.set], [mc7, mc6, D.cash]]) {
    for (const l of mB.receipts.lines) {
      const a = mA.receipts.lines.find((y) => y.id === l.id);
      natSame = natSame && a.national_bn === l.national_bn;
      for (const sc of Object.keys(l.cells)) for (const al of ALLOCS) cellTot = Math.max(cellTot, Math.abs(a.cells[sc][al].target_bn + a.cells[sc][al].other_bn - l.cells[sc][al].target_bn - l.cells[sc][al].other_bn));
    }
    for (const l of mB.spending.lines) natSame = natSame && mA.spending.lines.find((y) => y.id === l.id).national_bn === l.national_bn;
    for (const id of JC_LINES) for (const sc of mB.receipts.scenarios) for (const al of ALLOCS) {
      const want = PKG.JOBCAP.PARTS.reduce((t, p) => t + det.new_parts[`${id}|${sc}`][p][al], 0);
      tgap = Math.max(tgap, Math.abs(mA.receipts.lines.find((y) => y.id === id).cells[sc][al].target_bn - want));
    }
  }
  gate(`${ST("job_capital_taxes")}item job_capital_taxes: on both payload models the four lines' targets are the job-capital amounts at every scenario and allocation (1e-9); every line's national total and every receipt cell's total (target plus other) are v6's (exact / 1e-9)`,
    tgap < 1e-9 && natSame && cellTot < 1e-9, `max |diff| ${ex(tgap)}; cell totals ${ex(cellTot)}`);
  // Each corporate scenario's total is the group's corporate key times the corporate national: the cells share it.
  const blk = PKG.JOBCAP.CENTRAL, W = D.set.wage_share;
  let kgap = 0;
  for (const sc of m7.receipts.scenarios) for (const al of ALLOCS) {
    const got = ["corporate_capital", "corporate_labor"].reduce((t, id) => t + m7.receipts.lines.find((y) => y.id === id).cells[sc][al].target_bn, 0);
    const want = blk.lines.corporate.group_bn[al] + (W.g3plus[al] * blk.factor.G3plus.corporate[al] + W.whites[al] * blk.factor.white_nh.corporate[al]) * blk.lines.corporate.national_bn;
    kgap = Math.max(kgap, Math.abs(got - want));
  }
  gate(`${ST("job_capital_taxes")}item job_capital_taxes: at every scenario the two corporate lines hold the union's corporate group_bn plus the added people's (their wage shares times the G3plus and white_nh factors times the corporate national), whatever the scenario's split of the two lines (1e-9)`,
    kgap < 1e-9, `max |diff| ${ex(kgap)}; added people's wage share ${f2([W.g3plus.personal, W.whites.personal]).replace(" / ", " (G3+) / ")} (whites), personal`);
  // On v6 the four lines respond at 0 at every specification (indirect receipts, no override), so the item's change at
  // each specification is minus each line's new response times its new amount there.
  const zero6 = baseAllRuns.concat(baseCashAllRuns).every((xs) => xs.every((r) => JC_LINES.every((id) => receiptOf(r, id).response === 0)));
  gate("on v6 the four lines respond at 0 at every specification, set and cash (the engine's default for indirect receipts; v6 sets no override)", zero6, "2 sets x 2 methods x 64 specifications");
  const d = aloneChange(x);
  const rmove = ALL.map((s, i) => mean(x.runs.map((xs) => -JC_LINES.reduce((t, id) => { const row = receiptOf(xs[i], id); return t + row.response * row.amount_bn; }, 0))));
  const rg = worst(d.map((v, i) => v - rmove[i]));
  const respSet = x.runs.every((xs) => xs.every((r, i) => JC_LINES.every((id) => receiptOf(r, id).response === ALL[i].line_responses[`receipt:${id}`]
    && near(receiptOf(r, id).amount_bn, m7.receipts.lines.find((y) => y.id === id).cells[REF][ALL[i].allocation].target_bn, 1e-9))));
  gate(`${ST("job_capital_taxes")}item job_capital_taxes alone: at every one of the 64 specifications each line takes the specification's response on the job-capital amount at ${REF}, and the change is minus their sum (1e-9); P, F and the capital return do not move`,
    rg < 1e-9 && respSet && x.runs.every((xs, m) => xs.every((r, i) => r.evaluation.private_wtp_bn === baseAllRuns[m][i].evaluation.private_wtp_bn
      && r.evaluation.induced_receipts_bn === baseAllRuns[m][i].evaluation.induced_receipts_bn && r.capital.total_bn === baseAllRuns[m][i].capital.total_bn)),
    `max |diff| ${ex(rg)}; change ${f2(spanOf(d.slice(0, NP)))} personal, ${f2(spanOf(d.slice(NP)))} shared`);
  // Gate 4(a), a control on the item's mechanics (gate-only, not a published arm): every group, the union and the added
  // people, keyed at its share of the case's own wage key (corporate_labor's cells at the reference rule) with every
  // factor 1, and the four lines at response 1 (item_job_capital.cjs CEILING), alone on v6. The change at every
  // specification must be minus the whole group's share of the wage key times the three lines' national total.
  const NAT3 = blk.lines.corporate.national_bn + blk.lines.other_production_taxes.national_bn + blk.lines.business_property.national_bn;
  const Qc = PKG.caseOn(B6, ["job_capital_taxes"], { job_capital_taxes: PKG.JOBCAP.CEILING }, "variant", null);
  const ctlRuns = caseRuns(Qc, "set"), ctlCashRuns = caseRuns(Qc, "cash");
  const shareOfWage = (m) => { const c = m.receipts.lines.find((y) => y.id === "corporate_labor").cells[REF]; return Object.fromEntries(ALLOCS.map((a) => [a, c[a].target_bn / (c[a].target_bn + c[a].other_bn)])); };
  const whole = shareOfWage(m6), wholeCash = shareOfWage(mc6);
  const ctlChange = (rs, br) => Qc.MAIN_SPECS.map((s, i) => mean(rs.map((xs, m) => xs[i].cost_bn - br[m][i].cost_bn)));
  const ctl = ctlChange(ctlRuns, baseAllRuns), ctlCash = ctlChange(ctlCashRuns, baseCashAllRuns);
  const ctlGap = Math.max(worst(ctl.map((v, i) => v + whole[Qc.MAIN_SPECS[i].allocation] * NAT3)), worst(ctlCash.map((v, i) => v + wholeCash[Qc.MAIN_SPECS[i].allocation] * NAT3)));
  const ctlResp = ctlRuns.concat(ctlCashRuns).every((xs) => xs.every((r) => JC_LINES.every((id) => receiptOf(r, id).response === 1)));
  gate(`${ST("job_capital_taxes")}gate 4(a), a control (not an arm): every group keyed at its share of the case's own wage key (corporate_labor at ${REF}; ${f2([whole.personal, whole.shared]).replace(" / ", " personal / ")} shared), every factor 1, the four lines at response 1: alone on v6 the change at every one of the 64 specifications is minus that share times the three lines' national ${NAT3.toFixed(6)}, set and cash (1e-9)`,
    Math.abs(NAT3 - 1082.388297) < 1e-6 && ctlGap < 1e-9 && ctlResp && Qc.MAIN_SPECS.length === 64, `max |diff| ${ex(ctlGap)}; ${(-whole.personal * NAT3).toFixed(6)} personal, ${(-whole.shared * NAT3).toFixed(6)} shared`);
  // Gate 4(b), cross-lane: the control's union part at specification 11 (personal) is minus the lane's union plain wage
  // share times the national (the lane gates the Sept 27 probe's own form on its frame, -86.848983 / -80.976701).
  const pws = blk.lines.corporate.plain_wage_share;
  const det = Qc.ITEM_DETAIL.job_capital_taxes.set;
  const unionAt = (runsK, i) => mean(runsK.map((xs) => -JC_LINES.reduce((t, id) => t + receiptOf(xs[i], id).response
    * ["union_G1", "union_G2", "union_G3plus"].reduce((u, pn) => u + det.new_parts[`${id}|${REF}`][pn][Qc.MAIN_SPECS[i].allocation], 0), 0)));
  const union11 = unionAt(ctlRuns, 11), union48 = unionAt(ctlRuns, 48);
  gate(`${ST("job_capital_taxes")}gate 4(b), cross-lane: the control's union part at specification 11 is minus the lane's union plain_wage_share.personal (${pws.personal}) times ${NAT3.toFixed(6)} (1e-6); the lines' plain wage shares agree`,
    Qc.MAIN_SPECS[11].allocation === "personal" && Qc.MAIN_SPECS[48].allocation === "shared" && Math.abs(union11 + pws.personal * NAT3) < 1e-6
    && ["other_production_taxes", "business_property"].every((g) => ALLOCS.every((a) => blk.lines[g].plain_wage_share[a] === pws[a])),
    `${union11.toFixed(6)} at 11; ${union48.toFixed(6)} at 48 (shared, beside)`);
  // The case's wage key against the Sept 27 probe's employer_hi share: a number to report, not a scaling factor.
  const probe = readJson("receipt_side_long_run_2026_09_28/derived/probe.json"), it4 = probe.item4;
  const wageKeyRatio = { personal: pws.personal / it4.wage_share[1], shared: pws.shared / it4.wage_share[0] };
  jobcapCheck = {
    control: { rule: "gate 4(a), a control and not a published arm: every group (the union and the added people) keyed at its share of the case's own wage key (corporate_labor at cbo_collective on the case's payload), every factor 1, the four lines at response 1, alone on v6; its change at every specification is minus the whole group's share times the three lines' national total (1e-9)",
      whole_group_wage_share: whole, whole_group_wage_share_cash: wholeCash, change_bn: { personal: -whole.personal * NAT3, shared: -whole.shared * NAT3 }, worst_gap_bn: ctlGap },
    cross_lane: { rule: "gate 4(b): the control's union part at specification 11 is minus the lane's union plain_wage_share.personal times the three lines' national (1e-6); the lane gates the probe's own form on its frame",
      union_at_11_bn: union11, union_at_48_shared_bn: union48, plain_wage_share: pws, lane_own_frame_gates_bn: { shared: -86.848983, personal: -80.976701 } },
    wage_key_ratio: { rule: "the case's wage key (the union's share of corporate_labor at cbo_collective on the September 29 payload) over the Sept 27 probe's employer_hi share: a number, not a scaling factor",
      personal: wageKeyRatio.personal, shared: wageKeyRatio.shared, case_wage_share: pws, probe_wage_share: { shared: it4.wage_share[0], personal: it4.wage_share[1] } },
    total_national_bn: NAT3, worst_target_gap_bn: tgap, worst_response_gap_bn: rg };
}
// Items white_end_tax_keys and row4_frame alone on v6: the row-4 class lane's moves at its specifications 48 / 11
// (row4_oct07.json, the methods' mean, 1e-9), set and cash; row4_frame's union and lineage parts at the lane's
// union_joint and lineage_joint (1e-9); the port's inputs are the lane's recorded ones.
let row4Check = null;
{
  const O = PKG.ROW4.ORACLE, E2 = [48, 11];
  const moveAt = (x, set) => E2.map((i) => mean((set === "cash" ? x.cashCosts : x.costs).map((xs, m) => xs[i] - (set === "cash" ? baseCashAll : baseAllCosts)[m][i])));
  const partsAt = (x, set, prefix) => {
    const rec = set === "cash" ? x.recordCash : x.record, xr = set === "cash" ? x.cashRuns : x.runs, es = set === "cash" ? x.cashEdits : x.edits;
    return E2.map((i) => mean(xr.map((xs) => Object.entries(rec.parts).filter(([n]) => n.startsWith(prefix)).reduce((t, [, p]) => {
      const e = es[p.edit], s = B6.MAIN_SPECS[i];
      if (e.side === "spending") return t + p.by[s.allocation] * lineOf(xs[i].evaluation, e.line).response;
      return t + (e.scenario === REF ? -p.by[s.allocation] * receiptOf(xs[i], e.line).response : 0);
    }, 0))));
  };
  const out = {};
  for (const [id, row] of [["white_end_tax_keys", "white"], ["row4_frame", "row4_class"]]) {
    const x = aloneOf(id);
    if (!x) continue;
    const mv = { set: moveAt(x, "set"), cash: moveAt(x, "cash") };
    const g = Math.max(...["set", "cash"].flatMap((w) => [0, 1].map((e) => Math.abs(mv[w][e] - O.rows[row][w].move[e]))));
    gate(`item ${id} alone on v6 is the row-4 class lane's ${row} row at its specifications 48 / 11 (row4_oct07.json; the methods' mean), set and cash (1e-9)`,
      x.nSpecs === 64 && g < 1e-9, `${f2(mv.set)}; cash ${f2(mv.cash)}; max |diff| ${ex(g)}`);
    out[id] = { at_48_11_bn: mv.set, cash_at_48_11_bn: mv.cash, lane_row: row, worst_gap_bn: g };
    if (id === "row4_frame") {
      const layers = { union_: "union_joint", lineage_: "lineage_joint" };
      let lg = 0;
      const lv = {};
      for (const [prefix, r] of Object.entries(layers)) for (const w of ["set", "cash"]) {
        const v = partsAt(x, w, prefix);
        lv[`${r}_${w}`] = v;
        lg = Math.max(lg, ...[0, 1].map((e) => Math.abs(v[e] - O.rows[r][w].move[e])));
      }
      gate(`item row4_frame alone on v6: its union_ parts are the lane's union_joint and its lineage_ parts its lineage_joint at 48 / 11, set and cash (1e-9)`,
        lg < 1e-9, `union ${f2(lv.union_joint_set)}, lineage ${f2(lv.lineage_joint_set)}; max |diff| ${ex(lg)}`);
      out[id].layers_bn = lv;
    }
  }
  // The port's inputs: the lane's recorded values (row4_oct07.json inputs), exactly; the added people's at the case's counts (1e-12).
  const D = P.ITEM_DETAIL.row4_frame.set, want = (k) => (k === "rn" ? { pub: O.inputs.rn.v6.pub, row4: O.inputs.rn.v6.row4 } : k === "partA" ? O.inputs.partA.v6 : O.inputs[k]);
  const dev = (a, b) => (typeof a === "number" ? Math.abs(a - b) : Math.max(...Object.keys(a).map((k) => dev(a[k], b[k]))));
  const inGap = Math.max(...Object.keys(D.inputs).map((k) => dev(D.inputs[k], want(k)))), linGap = Math.max(...Object.keys(D.lineage_inputs).map((k) => dev(D.lineage_inputs[k], O.inputs[k])));
  gate(`item row4_frame's inputs are the lane's recorded ones (row4_oct07.json inputs: ${Object.keys(D.inputs).join(", ")}; exact), and the added people's parts at the case's counts (${Object.keys(D.lineage_inputs).join(", ")}; 1e-12)`,
    inGap === 0 && linGap < 1e-12 && D.union_gap_bn < 1e-9 && D.generation_cells_gap_bn < 1e-9 && D.lineage_split_gap_bn < 1e-9, `inputs ${ex(inGap)}; lineage ${ex(linGap)}; union by generation ${ex(D.union_gap_bn)}`);
  row4Check = Object.assign(out, { inputs: D.inputs, generation_split: D.split, counts: D.counts, white: P.ITEM_DETAIL.white_end_tax_keys.set,
    rule: "each item alone on v6 (all 64 specifications, v6's allocation rule) reproduces the row-4 class lane's row at its specifications 48 / 11; on v7 both ends are personal, so item white_end_tax_keys takes the personal figure at both" });
}
// Interactions: each pair of edit sets on v6, and what the pairs leave of the case's change.
const pairs = [];
for (let a = 0; a < EDIT_SETS.length; a += 1) for (let b = a + 1; b < EDIT_SETS.length; b += 1) {
  const X = aloneOf(EDIT_SETS[a].id), Y = aloneOf(EDIT_SETS[b].id), Q = PKG.caseOf(B5, V6CAND.concat([X.r.id, Y.r.id]));
  const pc = consumerCosts(Q.correctionsPayload()), pcc = consumerCosts(Q.CASH_PAYLOAD);
  const ax = aloneChange(X), ay = aloneChange(Y), axc = aloneChange(X, "cash"), ayc = aloneChange(Y, "cash");
  pairs.push({ ids: [X.r.id, Y.r.id], set: pc.map((v, i) => v - c6[i] - ax[i] - ay[i]), cash: pcc.map((v, i) => v - cc6[i] - axc[i] - ayc[i]) });
}
const residual = change.map((v, i) => v - EDIT_SETS.reduce((s, r) => s + aloneChange(aloneOf(r.id))[i], 0) - pairs.reduce((s, q) => s + q.set[i], 0));
const cashResidual = cashChange.map((v, i) => v - EDIT_SETS.reduce((s, r) => s + aloneChange(aloneOf(r.id), "cash")[i], 0) - pairs.reduce((s, q) => s + q.cash[i], 0));
for (const q of pairs) {
  gate(`${STALL}${q.ids.join(" and ")} add with no interaction at every specification, set and cash (1e-9): at fixed responses the cost is linear in the cells they shift, and item job_capital_taxes re-keys lines the others do not edit`,
    worst(q.set) < 1e-9 && worst(q.cash) < 1e-9, `max |interaction| ${ex(worst(q.set))} / ${ex(worst(q.cash))}`);
}
gate(`${STALL}what the items and the pairs leave of the case's change is zero at every specification, set and cash (1e-9): personal_allocation picks specifications and moves no cost`,
  worst(residual) < 1e-9 && worst(cashResidual) < 1e-9, `max ${ex(worst(residual))} / ${ex(worst(cashResidual))}`);

const methodMean = (cm) => cm[0].map((_, i) => mean(cm.map((xs) => xs[i])));
const meanAll = methodMean(allCosts), meanCashAll = methodMean(cashAllCosts);
const payloadCosts = ALL.map((s) => evaluateFull(P.payloadModel(), s).cost_bn);
const cashPayloadCosts = PC.ALL_SPECS.map((s) => PC.evaluateFull(PC.payloadModel(), s).cost_bn);
const pmGap = worst(payloadCosts.map((x, i) => x - meanAll[i])), pmcGap = worst(cashPayloadCosts.map((x, i) => x - meanCashAll[i]));
gate("the payload model (engine.js + model.json + corrections.json) gives the methods' mean at every one of the 64 specifications, and the band over the 32 personal ones (1e-9)",
  payloadCosts.length === 64 && pmGap < 1e-9 && near(Math.min(...payloadCosts.slice(0, NP)), C[0], 1e-9) && near(Math.max(...payloadCosts.slice(0, NP)), C[1], 1e-9), `max |diff| ${ex(pmGap)}`);
gate("the cash set's payload model gives the cash set's methods' mean at every specification, and its band (1e-9)",
  pmcGap < 1e-9 && near(Math.min(...cashPayloadCosts.slice(0, NP)), Ccash[0], 1e-9) && near(Math.max(...cashPayloadCosts.slice(0, NP)), Ccash[1], 1e-9), `max |diff| ${ex(pmcGap)}`);
const SPEC_FIELDS = ["allocation", "normalization", "share", "school", "gg", "uc", "reading"];
for (const [name, pl, want, sp] of [["corrections.json", payload, meanAll, ALL], ["corrections_cash.json", cashPayload, meanCashAll, PC.ALL_SPECS]]) {
  const independent = Consumer.evaluateAll(JSON.parse(JSON.stringify(pl)), { engine: Engine, model: MODEL });
  const g = worst(independent.map((x, i) => x.cost_bn - want[i]));
  const lrOk = independent.every((x, i) => JC_LINES.every((id) => x.evaluation.receipts.find((y) => y.id === id).response === sp[i].line_responses[`receipt:${id}`]));
  gate(`consumer.cjs (engine.js, model.json and ${name}, no package) gives the methods' mean at every one of its 64 specifications (1e-9): it reads gg, the line responses (item job_capital_taxes's four among them) and the long-run subfunctions from meta.responses; the band takes the ${pl.meta.allocation.group_total} ones (meta.allocation)`,
    independent.length === 64 && independent.every((x, i) => SPEC_FIELDS.every((f) => x.spec[f] === sp[i][f])) && g < 1e-9 && lrOk && pl.meta.allocation.group_total === "personal", `max |diff| ${ex(g)}`);
}
const strip = (m) => JSON.stringify(Object.assign({}, m, { corrections: null }));
{
  const after = (m, edits) => (edits.length ? Engine.applyCorrections(m, { edits }) : m);
  gate("v7's payload models are v6's payload models with the v7 items' edits applied after v6's, exactly; v6's are model.json with the September 29 payloads, the lineage addition, v6's edit sets and carriers",
    strip(P.payloadModel()) === strip(after(B6.payloadModel(), P.V7_EDITS)) && strip(PC.payloadModel()) === strip(after(B6C.payloadModel(), PC.V7_EDITS))
    && P.ITEM_EDITS.length === B6.ITEM_EDITS.length + P.V7_EDITS.length && JSON.stringify(P.ITEM_EDITS.slice(0, B6.ITEM_EDITS.length)) === JSON.stringify(B6.ITEM_EDITS),
    `${P.V7_EDITS.length} set edits, ${PC.V7_EDITS.length} cash edits after v6's ${N6} / ${N6C}`);
}

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the payload and the specifications]");
{
  // v7's payload: v6's with the v7 edit sets' edits after v6's, their meta keys before items, item 6's responses after
  // v6's, meta.items extended, and the stamps.
  const metaNew = ["allocation", "child_credits", "job_capital_taxes", "white_end_tax_keys", "row4_frame"].filter((k) => k in payload.meta);
  function framed(pl, pl6, edits, recs) {
    const keys6 = Object.keys(pl6.meta), want = keys6.filter((k) => k !== "items").concat(metaNew, ["items"]);
    const changed = keys6.filter((k) => JSON.stringify(pl.meta[k]) !== JSON.stringify(pl6.meta[k])).sort();
    const respOk = JSON.stringify(Object.keys(pl.meta.responses)) === JSON.stringify(Object.keys(pl6.meta.responses).concat(JC_LINES))
      && Object.keys(pl6.meta.responses).every((k) => JSON.stringify(pl.meta.responses[k]) === JSON.stringify(pl6.meta.responses[k]));
    const ok = JSON.stringify(Object.keys(pl)) === JSON.stringify(Object.keys(pl6)) && ["lines", "receipt_lines", "production"].every((k) => JSON.stringify(pl[k]) === JSON.stringify(pl6[k]))
      && JSON.stringify(pl.edits.slice(0, pl6.edits.length)) === JSON.stringify(pl6.edits) && JSON.stringify(pl.edits.slice(pl6.edits.length)) === JSON.stringify(edits)
      && JSON.stringify(Object.keys(pl.meta)) === JSON.stringify(want) && respOk
      && JSON.stringify(changed) === JSON.stringify(["adopted", "case", "decision", "items", "responses", "source", "status"].sort())
      && JSON.stringify(pl.meta.items.slice(0, pl6.meta.items.length)) === JSON.stringify(pl6.meta.items) && JSON.stringify(pl.meta.items.slice(pl6.meta.items.length)) === JSON.stringify(recs);
    return { ok, detail: `${pl.edits.length} edits (${pl6.edits.length} + ${edits.length}); meta changed: ${changed.join(", ")}; added: ${metaNew.join(", ")}` };
  }
  const f7 = framed(payload, payload6, P.V7_EDITS, P.V7_ITEMS), f7c = framed(cashPayload, cashPayload6, PC.V7_EDITS, PC.V7_ITEMS);
  gate(`corrections.json is v6's with the v7 edit sets' edits after v6's, meta.${metaNew.join(", meta.")} before meta.items, item job_capital_taxes's four responses after v6's in meta.responses, meta.items extended and the stamps (${P.STAMPED.join(", ")}); lines, receipt lines, the production grid and every other meta key identical`,
    f7.ok, f7.detail);
  gate("corrections_cash.json is v6's cash payload built the same way with the cash items", f7c.ok, f7c.detail);
  // The stamps: the candidate (STATUS "candidate") or the adopted case (STATUS "adopted", the decision file exists).
  const ST7 = PKG.V7.STATUS, DEC = PKG.V7.DECISION_FILE, exists = fs.existsSync(DEC);
  const stampOk = [[payload, payload6, "set"], [cashPayload, cashPayload6, "cash"]].every(([pl, b, w]) => pl.meta.decision === P.DECISION && pl.meta.source === `${P.LANE}/package.cjs`
    && (ST7 === "adopted"
      ? pl.meta.adopted === P.V7.ADOPTED && exists && pl.meta.status.startsWith(w === "set" ? `adopted ${P.V7.ADOPTED} (${P.DECISION}): ` : `the cash set of the case adopted ${P.V7.ADOPTED} (the pension switch off): `)
        && pl.meta.case.startsWith(`${b.meta.case}; v7, adopted ${P.V7.ADOPTED}: `)
      : pl.meta.adopted === null && pl.meta.status.startsWith("candidate: main case v7, not adopted") && pl.meta.case.startsWith(`${b.meta.case}; v7, the candidate (not adopted): `)));
  gate(ST7 === "adopted" ? `meta, both payloads: adopted ${P.V7.ADOPTED}, decision ${P.DECISION} (the file exists), the adopted status form, the case text names v7 adopted`
    : `meta, both payloads: the candidate (STATUS "candidate", adopted null), decision ${P.DECISION}, status "candidate: main case v7, not adopted ...", the case text names the candidate; adoption is the package's STATUS switch, allowed only once the decision file exists`,
    stampOk && (ST7 !== "adopted" || exists) && P.ADOPTED === (ST7 === "adopted" ? P.V7.ADOPTED : null) && P.STATUS === ST7,
    `${path.relative(path.resolve(FISCAL, "..", ".."), DEC)} ${exists ? "exists" : "not written yet"}`);
  gate("meta.lineage is v6's: the lineage's edits keep their place (first 416, count 336, row 8 at 751) and v6's item edits follow them, then v7's",
    JSON.stringify(payload.meta.lineage) === JSON.stringify(payload6.meta.lineage) && JSON.stringify(cashPayload.meta.lineage) === JSON.stringify(cashPayload6.meta.lineage)
    && L.edits.first === 416 && L.edits.count === 336 && L.edits.row8_edit_index === 751, `${payload.edits.length} edits`);
  // meta.items: v6's records unchanged, then v7's, locating their edits (which run to the end), parts adding exactly.
  function locates(pl, n, recs) {
    let at = n, ok = true;
    for (const r of recs) {
      if (!r.applied) { ok = ok && typeof r.why === "string"; continue; }
      ok = ok && r.edits && r.edits.first === at;
      const es = pl.edits.slice(r.edits.first, r.edits.first + r.edits.count);
      at += r.edits.count;
      const sums = es.map(() => ({ personal: 0, shared: 0 }));
      for (const part of Object.values(r.parts || {})) for (const a of ALLOCS) sums[part.edit][a] += part.by[a];
      ok = ok && (!Object.keys(r.parts || {}).length || es.every((e, k) => !e.by || ALLOCS.every((a) => sums[k][a] === e.by[a])));
    }
    return ok && at === pl.edits.length;
  }
  gate(`meta.items: both payloads name v6's items, then ${NEW.join(", ")}; each applied v7 item's {first, count} locates its edits, which run to the end (personal_allocation's count 0), and its parts add to them exactly`,
    locates(payload, N6, payload.meta.items.slice(payload6.meta.items.length)) && locates(cashPayload, N6C, cashPayload.meta.items.slice(cashPayload6.meta.items.length))
    && JSON.stringify(payload.meta.items.map((r) => r.id)) === JSON.stringify(P.ITEM_IDS) && JSON.stringify(P.ITEM_IDS) === JSON.stringify(PKG.CANDIDATE),
    payload.meta.items.slice(payload6.meta.items.length).map((r) => `${r.id} edits ${r.edits.first}-${r.edits.first + r.edits.count - 1}`).join("; "));
  const A = payload.meta.allocation;
  gate("meta.allocation: group_total personal, the reason, what the shared allocation is kept for, the source record and the decision; the same block in both payloads",
    A && A.group_total === "personal" && typeof A.reason === "string" && typeof A.shared_kept_for === "string" && A.source.record === "research/immigration-v6-assumption-review-2026-10-14.md"
    && A.source.decision === P.DECISION && JSON.stringify(A) === JSON.stringify(cashPayload.meta.allocation), A ? A.rule.slice(0, 90) : "missing");
  for (const id of ["child_credits", "job_capital_taxes"]) {
    const b = payload.meta[id];
    gate(`${ST(id)}meta.${id}: its source file and sha256 (${SRC[id].file}), stub ${SRC[id].stub}; the same block in both payloads`,
      b && b.source.file === SRC[id].file && b.source.sha256 === sha256(SRC[id].file) && b.stub === SRC[id].stub && JSON.stringify(b.source) === JSON.stringify(cashPayload.meta[id].source),
      `${SRC[id].file}`);
  }
  for (const [id, src] of Object.entries(SRC7)) {
    const b = payload.meta[id], files = Object.assign({ [src.file]: src.sha256 }, src.files || {}, src.oracle ? { [src.oracle.file]: src.oracle.sha256 } : {});
    gate(`meta.${id}: its source files and their sha256 (${Object.keys(files).length} files, ${src.lane}); the same block in both payloads`,
      b && JSON.stringify(b.source) === JSON.stringify(src) && Object.entries(files).every(([f, h]) => sha256(f) === h) && JSON.stringify(b.source) === JSON.stringify(cashPayload.meta[id].source),
      Object.keys(files).slice(0, 3).join(", "));
  }
}
gate("RESPONSES is meta.responses and componentsFor(null) is meta.capital_return.components (deep-equal, key order)",
  JSON.stringify(P.RESPONSES) === JSON.stringify(payload.meta.responses) && JSON.stringify(COMPONENTS) === JSON.stringify(payload.meta.capital_return.components));
const without4 = (r) => Object.fromEntries(Object.entries(r).filter(([k]) => !JC_LINES.includes(k)));
const diffs = P.responseDiffs(payload29.meta.responses, without4(payload.meta.responses));
const diffs6 = P.responseDiffs(payload29.meta.responses, payload6.meta.responses);
gate("without item job_capital_taxes's four entries, meta.responses differs from v4's only in the group-size responses, as v6's does (the same paths): general government (and its s), row 8's factor, the long-run lines and their subfunctions, the road lines, recreation's state price and the long-run property receipts",
  diffs.length > 0 && JSON.stringify(diffs) === JSON.stringify(diffs6) && diffs.every((p) => P.GROUP_PATHS.includes(p) || /^(economic_affairs_services|recreation_culture)\.subfunctions\[[a-z_]+\]\.(low|high)$/.test(p))
  && JSON.stringify(without4(payload.meta.responses)) === JSON.stringify(payload6.meta.responses), `${diffs.length} values: ${diffs.join(", ")}`);
{
  const R = payload.meta.responses, JB = PKG.JOBCAP.CENTRAL.lines;
  const want = { corporate_capital: JB.corporate.response, corporate_labor: JB.corporate.response, remaining_production_property: JB.business_property.response, other_production_taxes: { low: 1, high: 1 } };
  const rd = PKG.JOBCAP.showReadings;
  gate(`${ST("job_capital_taxes")}the four new responses: receipt true, override "receipt:<line>", low and high the lane's readings (corporate ${rd(JB.corporate.response)}, business property r_b ${rd(JB.business_property.response)}, other production taxes 1), both payloads`,
    JC_LINES.every((id) => R[id] && R[id].receipt === true && R[id].override === `receipt:${id}` && R[id].low === want[id].low && R[id].high === want[id].high
      && JSON.stringify(R[id]) === JSON.stringify(cashPayload.meta.responses[id])), JC_LINES.map((id) => `${id} ${rd(want[id])}`).join(", "));
}
const P24_FIELDS = Object.keys(P.P24.MAIN_SPECS[0]);
const EXTRA = ["reading", "rate", "long_run", "enterprises", "line_responses"];
gate("the specifications carry only the September 24 fields and reading, rate, long_run, enterprises and line_responses, in the September 29 order",
  ALL.every((s) => Object.keys(s).every((k) => P24_FIELDS.includes(k) || EXTRA.includes(k)))
  && JSON.stringify(Object.keys(ALL[0])) === JSON.stringify(Object.keys(P4.MAIN_SPECS[0])), Object.keys(ALL[0]).join(" "));
gate("reading is low exactly where general government takes its low response; the rate follows the reading (2% low, 3% high)",
  ALL.every((s) => (s.reading === "low") === (s.gg === P.RESPONSES.general_government.low) && s.rate === RATES[s.reading]),
  `${ALL.filter((s) => s.reading === "low").length} low of 64`);
const lrKeys = Object.keys(P.LINE_RESPONSES);
gate(`each specification's line responses are meta.responses at its reading: ${lrKeys.length} entries, in meta's order, item job_capital_taxes's four last, in every case specification (and the shared ones)`,
  ALL.every((s) => JSON.stringify(Object.keys(s.line_responses)) === JSON.stringify(lrKeys) && lrKeys.every((k) => s.line_responses[k] === P.LINE_RESPONSES[k][s.reading]))
  && JSON.stringify(lrKeys.slice(-4)) === JSON.stringify(JC_LINES.map((id) => `receipt:${id}`))
  && PC.ALL_SPECS.every((s, i) => JSON.stringify(s) === JSON.stringify(ALL[i])), lrKeys.slice(-4).join(" "));
const movedKeys = lrKeys.filter((k) => ALL.some((s, i) => s.line_responses[k] !== P4.MAIN_SPECS[i].line_responses[k]));
gate("the specifications are the September 29 case's but for general government, the group-size line responses and item job_capital_taxes's four (every other field and line response identical)",
  ALL.every((s, i) => Object.keys(s).every((k) => ["gg", "line_responses"].includes(k) || s[k] === P4.MAIN_SPECS[i][k])
    && lrKeys.every((k) => movedKeys.includes(k) || s.line_responses[k] === P4.MAIN_SPECS[i].line_responses[k]))
  && movedKeys.every((k) => ["economic_affairs_services", "recreation_culture", "roads_vmt_sl", "roads_vmt_fed", "state_price_recreation_culture",
    "receipt:modeled_owner_property", "receipt:tenant_occupied_property"].concat(JC_LINES.map((id) => `receipt:${id}`)).includes(k)), `moved: ${movedKeys.join(", ")}`);
// The production module's capital-tax term at every case specification's production cell: 0, so the four lines'
// response counts nothing twice.
const MODULE_FILE = "full_account_benefits_2026_09_20/derived/upstream_replay/scenarios.csv";
const scen = csvRows(MODULE_FILE);
const prodRef = MODEL.production.reference;
let capTerm = null;
{
  const cellOf = (st) => scen.filter((r) => r.proxy === st.proxy && r.split === st.split && r.normalization === st.normalization
    && +r.labor_share === st.labor_share && +r.sigma === st.sigma && +r.capital_adjustment === st.capital_adjustment
    && +r.labor_supply_elasticity === st.labor_supply_elasticity && +r.capital_tax_retention === st.capital_tax_retention && r.tax_classification_transport === "source_split");
  const pr = P.payloadModel().production, D = Engine.PRODUCTION_DIMS;
  const idx = (p) => D.reduce((i, d) => i * pr.dims[d].length + pr.dims[d].findIndex((v) => v === p[d] || Math.abs(v - p[d]) < 1e-9), 0);
  let ok = true, nCells = 0, invGap = 0;
  const states = new Map();
  for (const pf of [MAIN_PROFILE].concat(Object.keys(PROFILES).filter((x) => x !== MAIN_PROFILE))) for (const s of ALL) {
    const st = P.stateFor(MODELS[0], s, pf).production;
    ok = ok && st.capital_adjustment === 1 && st.capital_tax_retention === 1 && st.excluded_capital_owner_share === 0;
    states.set(JSON.stringify(st), st);
  }
  const terms = [...states.values()].map((st) => {
    const rows = cellOf(st);
    nCells += 1;
    const at = (ret) => { const j = idx(Object.assign({}, st, { capital_tax_retention: ret })); return pr.private_wtp_bn[j] + pr.induced_receipts_bn[j]; };
    invGap = Math.max(invGap, Math.abs(at(1) - at(0)), Math.abs(at(1) - at(0.5)));
    return { normalization: st.normalization, rows: rows.length, capital_tax_gain_bn: rows.length === 1 ? +rows[0].capital_tax_gain_estimate / 1e9 : null };
  });
  capTerm = { states: terms, retention: 1, capital_adjustment: 1, excluded_capital_owner_share: 0, p_plus_f_invariance_gap_bn: invGap, module: MODULE_FILE };
  gate("the production module's capital-tax term is 0 at every case and shared specification in every profile: each production cell has capital_adjustment 1, capital_tax_retention 1 and no excluded owners, and the module's capital_tax_gain_estimate there is exactly 0; P + F on the payload's grid does not move with retention (1e-8), so item job_capital_taxes counts nothing twice",
    ok && terms.every((t) => t.rows === 1 && t.capital_tax_gain_bn === 0) && invGap < 1e-8, `${nCells} production cells: ${terms.map((t) => `${t.normalization} ${t.capital_tax_gain_bn}`).join(", ")}; P + F gap ${ex(invGap)}`);
}
gate("no capital component's key reads item job_capital_taxes's four lines (the receipt keys are the carriers'), so setting their responses after the variants' route moves nothing else",
  COMPONENTS.every((c) => !(c.key && c.key.line && JC_LINES.includes(c.key.line))), `${COMPONENTS.length} components`);

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
    && r.capital.components.filter((c) => c.group === "block").every((c) => c.response === 1)), "2 methods x 32 specifications");
gate("category lag (the old main profile): roads, parks, their correction lines and the block at 0",
  every(profileRuns.cbo_category_lag_non_school_full, (r) => LR_LINES.concat(FOLLOW).every((id) => responseOf(r.evaluation, id) === 0)
    && capitalGroup(r, "block") === 0), "2 methods x 32 specifications");
gate("long_run_non_school_fixed: roads, parks and their correction lines take the specification's responses, as in the main profile; no college capital",
  every(profileRuns.long_run_non_school_fixed, (r, s) => LR_LINES.concat(FOLLOW).every((id) => responseOf(r.evaluation, id) === s.line_responses[id])
    && byId(r, "college") === 0), "2 methods x 32 specifications");
gate(`every profile: ${OTHER_FOLLOWERS.join(", ")} respond as their parents (${OTHER_FOLLOWERS.map((id) => P.PARENT[id]).join(", ")}), and every receipt response is the specification's, item job_capital_taxes's four included`,
  [newRuns].concat(Object.values(profileRuns)).every((rs) => every(rs, (r, s) => OTHER_FOLLOWERS.every((id) => responseOf(r.evaluation, id) === responseOf(r.evaluation, P.PARENT[id]))
    && receiptKeys.every((k) => receiptOf(r, k.slice("receipt:".length)).response === s.line_responses[k]))), "4 profiles x 2 methods x 32 specifications");
gate("main profile: every correction line responds as the specification sets it and the road lines as their subfunctions (sl_highways, fed_highways)",
  every(newRuns, (r, s) => P.PAYLOAD_LINES.filter((l) => P.PARENT[l.id]).every((l) => responseOf(r.evaluation, l.id) === s.line_responses[l.id])
    && COMPONENTS.filter((c) => c.key.kind === "part_rekeyed").every((c) => s.line_responses[c.key.correction_line] === P.subfunctionResponses(s.long_run, s.reading)[c.response.subfunction])));
gate("main profile: every long-run capital component takes its subfunction's response from meta.responses",
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
  })), "2 methods x 32 specifications");
const ggOperatingAtEnds = atEnds(newEnds, (m, i) => ggOperating(newRuns[m][i]));
const ggCapitalAtEnds = atEnds(newEnds, (m, i) => ggCapital(newRuns[m][i]));
gate("general government at 0 keeps the end specifications; its band is the case's less the operating effect and the gps return there (1e-9)",
  ends(ggFixedCosts).every((e, m) => e[0] === newEnds[m][0] && e[1] === newEnds[m][1])
  && [0, 1].every((e) => near(ggFixed[e], C[e] - ggOperatingAtEnds[e] - ggCapitalAtEnds[e], 1e-9)),
  `${f2(ggFixed)}: operating ${f2(ggOperatingAtEnds)}, capital ${f2(ggCapitalAtEnds)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[history: the September 29 case, v6's rows]");
const v4Models = METHODS.map((m) => P4.modelFor("central", m, P4.withCentral({})));
const v4Runs = runs(P4.MAIN_SPECS, MAIN_PROFILE, v4Models, P4);
const v4Costs = costsOf(v4Runs);
const C4 = P4.central({}), C4cash = PC4.central({});
gate("the September 29 case re-derives through SEPT29 exactly: its band, the cash set's, and per_spec.csv's cost at every specification and method",
  C4[0] === s29.main_case[0] && C4[1] === s29.main_case[1] && C4cash[0] === s29.cash_set.band_bn[0] && C4cash[1] === s29.cash_set.band_bn[1]
  && METHODS.every((meth, k) => P4.MAIN_SPECS.every((_, i) => String(v4Costs[k][i]) === ps29.find((r) => r.method === meth && Number(r.spec) === i).cost_bn)),
  `${f2(C4)}; cash ${f2(C4cash)}`);
const HISTORY_ROWS = ["first_year_response", "schools_case", "sept27_case", "sept29_case", "oct05_case", "long_run_responses_alone", "rental_assistance_alone",
  "long_run_responses_and_capital_return_option_a", "sept29_cash_set", "oct05_cash_set"];
gate("v6's band rows print the base: its adopted and cash_set rows are v6's band and cash set, and its history rows are kept as v6 printed them",
  row6(MAIN_PROFILE, "adopted").cost_low_bn === fx(C6[0]) && row6(MAIN_PROFILE, "adopted").cost_high_bn === fx(C6[1])
  && row6(MAIN_PROFILE, "cash_set").cost_low_bn === fx(C6cash[0]) && row6(MAIN_PROFILE, "cash_set").cost_high_bn === fx(C6cash[1])
  && HISTORY_ROWS.every((v) => !!rawRow6(MAIN_PROFILE, v)), `${HISTORY_ROWS.length} history rows`);
const cashTotal = [0, 1].map((e) => Ccash[e] - C4cash[e]);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the items' change, from v6]");
// The change from v6 at the band's ends: personal_allocation moves v6's ends (48 low, 11 high) to the personal ones
// (16, 11); at v7's end specifications each edit set alone on v6, by part; the pairs' interactions.
const part = (f) => atEnds(newEnds, (m, i) => f(m, i));
const allocMove = minus(v6Personal, C6), allocMoveCash = minus(v6PersonalCash, C6cash);
const itemsTotal = part((m, i) => newCosts[m][i] - baseCosts[m][i]);
gate("the change from v6 is personal_allocation's move of the ends plus the items' change at v7's end specifications (1e-9), set and cash",
  [0, 1].every((e) => near(C[e] - C6[e], allocMove[e] + itemsTotal[e] + (mean(newEnds.map((ij, m) => baseCosts[m][ij[e]])) - v6Personal[e]), 1e-9))
  && [0, 1].every((e) => near(Ccash[e] - C6cash[e], allocMoveCash[e] + atEnds(cashEnds, (m, i) => cashCosts[m][i] - baseCash[m][i])[e]
    + (mean(cashEnds.map((ij, m) => baseCash[m][ij[e]])) - v6PersonalCash[e]), 1e-9)),
  `allocation ${f2(allocMove)} + items ${f2(itemsTotal)}`);
function partsOf(x, set) {
  const xr = set === "cash" ? x.cashRuns : x.runs, rec = set === "cash" ? x.recordCash || PC.V7_ITEMS.find((r) => r.id === x.r.id) : x.record || P.V7_ITEMS.find((r) => r.id === x.r.id);
  const es = set === "cash" ? x.cashEdits : x.edits, br = set === "cash" ? baseCashAllRuns : baseAllRuns, ix = set === "cash" ? cashEnds : newEnds;
  const at = (f) => atEnds(ix, f);
  const total = at((m, i) => xr[m][i].cost_bn - br[m][i].cost_bn);
  if (x.r.id === "job_capital_taxes") {
    // The four lines responded at 0 on v6 (gated), so each part's change is minus the line's new response times the
    // part's new amount at the reference scenario, summed over the lines; by line as well.
    const det = set === "cash" ? x.detail.cash : x.detail.set;
    const partAt = (pname, ids) => at((m, i) => -ids.reduce((t, id) => t + receiptOf(xr[m][i], id).response * det.new_parts[`${id}|${REF}`][pname][ALL[i].allocation], 0));
    const parts = Object.fromEntries(PKG.JOBCAP.PARTS.map((pn) => [pn, partAt(pn, JC_LINES)]));
    const byLine = Object.fromEntries(Object.entries(PKG.JOBCAP.GROUPS).map(([g, ids]) => [g, [0, 1].map((e) => PKG.JOBCAP.PARTS.reduce((t, pn) => t + partAt(pn, ids)[e], 0))]));
    return { total, parts, by_line: byLine, rule: "minus each line's response times the part's job-capital amount at the reference scenario (the lines responded at 0 on v6)" };
  }
  // A cell shift's part at an end: + its amount times the line's response (spending), - that (receipt, at the
  // evaluation's scenario only).
  const parts = Object.fromEntries(Object.entries(rec.parts).map(([n, p]) => {
    const e = es[p.edit];
    return [n, at((m, i) => {
      const s = ALL[i];
      if (e.side === "spending") return p.by[s.allocation] * lineOf(xr[m][i].evaluation, e.line).response;
      return e.scenario === REF ? -p.by[s.allocation] * receiptOf(xr[m][i], e.line).response : 0;
    })];
  }).filter(([, v]) => v[0] !== 0 || v[1] !== 0));
  return { total, parts };
}
const itemParts = EDIT_SETS.map((r) => {
  const x = aloneOf(r.id);
  if (!x.runs) { x.runs = null; }
  return { id: r.id, set: partsOf(x, "set"), cash: partsOf(x, "cash") };
});
const gapOf = (b) => Math.max(...[0, 1].map((e) => Math.abs(Object.values(b.parts).reduce((a, v) => a + v[e], 0) - b.total[e])));
const partGap = Math.max(...itemParts.map((x) => Math.max(gapOf(x.set), gapOf(x.cash))));
gate(`${STALL}each edit set's parts at the end specifications add to its change alone, set and cash (1e-9; max |diff| ${ex(partGap)}): cell shifts at their lines' responses (receipts at ${REF})`,
  partGap < 1e-9, itemParts.map((x) => `${x.id} ${f2(x.set.total)}`).join("; "));
const groupSum = (parts, prefix) => { const ps = Object.entries(parts).filter(([n]) => n.startsWith(prefix)); return ps.length ? [0, 1].map((e) => ps.reduce((a, [, v]) => a + v[e], 0)) : [0, 0]; };
// A union part's generation: union_<G>:<...> (every v7 edit set's union parts: child_credits's by lane part and
// scenario, job_capital_taxes's by line and scenario, row4_frame's by component, line and cell).
const GEN_IDS = ["G1", "G2", "G3plus"];
const genOf = (n) => GEN_IDS.find((g) => n === `union_${g}` || n.startsWith(`union_${g}:`)) || null;
const genSum = (parts, g) => groupSum(Object.fromEntries(Object.entries(parts).filter(([n]) => genOf(n) === g)), "");
const byGeneration = (parts) => Object.fromEntries(GEN_IDS.map((g) => [g, genSum(parts, g)]));
const genGap = Math.max(...itemParts.flatMap((x) => [x.set, x.cash].map((b) => Math.max(...[0, 1].map((e) =>
  Math.abs(GEN_IDS.reduce((t, g) => t + genSum(b.parts, g)[e], 0) - groupSum(b.parts, "union_")[e]))))));
gate(`${STALL}every union part of each edit set has a generation (union_<G> or union_<G>:...), and the generations add to the union's change, set and cash (1e-9; max |diff| ${ex(genGap)})`,
  itemParts.every((x) => [x.set, x.cash].every((b) => Object.keys(b.parts).filter((n) => n.startsWith("union_")).every((n) => genOf(n) !== null))) && genGap < 1e-9,
  itemParts.map((x) => `${x.id} ${GEN_IDS.map((g) => `${g} ${f2(genSum(x.set.parts, g))}`).join(", ")}`).join("; "));
{
  const jc = itemParts.find((x) => x.id === "job_capital_taxes");
  const lineGap = Math.max(...[jc.set, jc.cash].map((b) => Math.max(...[0, 1].map((e) => Math.abs(Object.values(b.by_line).reduce((t, v) => t + v[e], 0) - b.total[e])))));
  gate(`${ST("job_capital_taxes")}item job_capital_taxes's change by line adds to its change, set and cash (1e-9; max |diff| ${ex(lineGap)})`,
    lineGap < 1e-9, Object.entries(jc.set.by_line).map(([g, v]) => `${g} ${f2(v)}`).join(", "));
  // The union's part at each end is minus the lane's central at that end's reading and allocation.
  const LC = PKG.JOBCAP.CENTRAL.central_bn;
  const unionOf = (b) => groupSum(b.parts, "union_");
  const wantOf = (ix) => atEnds(ix, (m, i) => -LC[ALL[i].reading][ALL[i].allocation]);
  const cGap = Math.max(...[[jc.set, newEnds], [jc.cash, cashEnds]].flatMap(([b, ix]) => [0, 1].map((e) => Math.abs(unionOf(b)[e] - wantOf(ix)[e]))));
  gate(`${ST("job_capital_taxes")}item job_capital_taxes's union part at each end is minus the lane's central_bn at the end's reading and allocation, set and cash (1e-9; max |diff| ${ex(cGap)})`,
    cGap < 1e-9, `${f2(unionOf(jc.set))} against the lane's ${f2(wantOf(newEnds))}`);
}
const atEnd = (xs) => [xs[ENDS[0]], xs[ENDS[1]]];

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
const atCaseData = components.filter((c, k) => c.devs.every((d) => {
  const w = s29.components[k].variants[d.v];
  return Math.abs(d.d[0] - w[0]) < 1e-3 && Math.abs(d.d[1] - w[1]) < 1e-3;
})).map((c) => c.name);
const addedShare = L.counts.added / L.counts.account_union;
const atCaseDataMove = [addedShare * components.filter((c) => atCaseData.includes(c.name)).reduce((a, c) => a + c.lo[0], 0),
  addedShare * components.filter((c) => atCaseData.includes(c.name)).reduce((a, c) => a + c.hi[1], 0)];
const FIRST_ORDER = s6.range.first_order;
const asOn6 = components.filter((c, k) => c.devs.every((d) => {
  const w = s6.components[k].variants[d.v];
  return Math.abs(d.d[0] - w[0]) < 1e-3 && Math.abs(d.d[1] - w[1]) < 1e-3;
})).map((c) => c.name);
const movedFrom6 = components.map((c, k) => [c.name, Math.max(...c.devs.flatMap((d) => [0, 1].map((e) => Math.abs(d.d[e] - s6.components[k].variants[d.v][e]))))]);
const itemsAtCaseData = { components_as_on_v6: asOn6, deviation_change_from_v6_bn: Object.fromEntries(movedFrom6),
  note: "each component's largest change, over its variants and both ends, of its deviation from the case against v6's; a component is listed as on v6 when every deviation is within $0.001bn. The low end is now specification 16 (personal), so a component whose deviation differs between the allocations moves; item job_capital_taxes re-keys every variant's model (editsAt), item child_credits's fixed amounts stay the case's",
  oct07_case: s6.range.items_at_the_case_data };

// ---------------------------------------------------------------------------------------------------
console.log("\n[variants]");
// The item variants' route: candidate v4's evaluateFull at the moved specification, then the road capital, the
// long-run capital and item job_capital_taxes's four receipt responses set after it (package.cjs fixReceipts). On the
// case's own options it is the case.
const viaGap = worst(MODELS.flatMap((m, k) => ALL.map((s, i) => P.viaCandidate(m, s).cost_bn - allCosts[k][i])));
const viaCashGap = worst(cashModels.flatMap((m, k) => PC.ALL_SPECS.map((s, i) => PC.viaCandidate(m, s).cost_bn - cashAllCosts[k][i])));
const viaRows = MODELS.every((m) => ALL.every((s, i) => { const r = P.viaCandidate(m, s); return JC_LINES.every((id) => receiptOf(r, id).response === s.line_responses[`receipt:${id}`]); }));
gate("candidate v4's route, which the item variants take (property, payroll, the income-tax key, items 8 and 10), with the four receipt responses set after it, gives the case and the cash set at the case's own options at every one of the 64 specifications and method (1e-9)",
  viaGap < 1e-9 && viaCashGap < 1e-9 && viaRows, `max |diff| ${ex(viaGap)} / ${ex(viaCashGap)}`);
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
{
  // Under those two options the four re-keyed lines hold the job-capital amounts on the option's cell totals (editsAt).
  let jgap = 0, n = 0;
  const blk = PKG.JOBCAP.CENTRAL, W = P.ITEM_DETAIL.job_capital_taxes.set.wage_share;
  for (const label of STRUCTURAL) {
    const [, caseName, o] = ROW_OPTIONS.find((x) => x[0] === label);
    for (const meth of METHODS) {
      const m = modelFor(caseName, meth, withCentral(o));
      for (const id of JC_LINES) {
        const g = PKG.JOBCAP.GROUP_OF[id], l = m.receipts.lines.find((y) => y.id === id);
        const N = PKG.JOBCAP.GROUPS[g].reduce((t, x) => t + m.receipts.lines.find((y) => y.id === x).national_bn, 0);
        for (const sc of m.receipts.scenarios) for (const a of ALLOCS) {
          const T = l.cells[sc][a].target_bn + l.cells[sc][a].other_bn;
          const want = (blk.lines[g].group_bn[a] + (W.g3plus[a] * blk.factor.G3plus[g][a] + W.whites[a] * blk.factor.white_nh[g][a]) * blk.lines[g].national_bn) * T / N;
          jgap = Math.max(jgap, Math.abs(l.cells[sc][a].target_bn - want)); n += 1;
        }
      }
    }
  }
  gate(`${ST("job_capital_taxes")}under those two options item job_capital_taxes re-keys the option's own cells (editsAt): every target is the job-capital amount on the option's cell totals (1e-9)`,
    jgap < 1e-9 && n > 0, `${n} cells, max |diff| ${ex(jgap)}`);
}
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
const K12_IDS = COMPONENTS.filter((c) => c.id === "k12" || c.of_component === "k12").map((c) => c.id);
const k12Of = (r) => K12_IDS.reduce((t, id) => t + byId(r, id), 0);
const k12Diff = atEnds(newEnds, (m, i) => k12Of(pupilRuns[m][i]) - k12Of(newRuns[m][i]));
const k12Keys = atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.filter((c) => K12_IDS.includes(c.id)).reduce((t, c) => t + c.key, 0));
gate(`with the pupil share the case differs by the K-12 difference alone (${K12_IDS.join(" and ")})`, worst(pupilRuns.flatMap((xs, m) => xs.map((r, i) =>
  r.cost_bn - newCosts[m][i] - (k12Of(r) - k12Of(newRuns[m][i]))))) < 1e-9
  && pupilRuns.every((xs) => xs.every((r) => K12_IDS.slice(1).every((id) => !r.capital.components.some((c) => c.id === id)))), "every specification");
const at7 = central(RATES7);
const runs7 = runs(specsFor(RATES7));
const with8 = central(beside8.o), with10 = central(beside10.o);
const withRuns = (o) => runs(specsFor(o), MAIN_PROFILE, METHODS.map((m) => modelFor("central", m, withCentral(o))));
const runs8 = withRuns(beside8.o), runs10 = withRuns(beside10.o);
const pmBand = (sp) => [Math.min(...sp.map((s) => evaluateFull(P.payloadModel(), s).cost_bn)), Math.max(...sp.map((s) => evaluateFull(P.payloadModel(), s).cost_bn))];
const specChecks = [["without_capital_return", withoutCapital, specsFor({ capital: false })], ["enterprises_out_option_a", optionA, specsFor({ enterprises: "A" })],
  ["capital_return_at_7pct", at7, specsFor(RATES7)], ["general_government_fixed", ggFixed, ggFixedSpecs],
  ["k12_capital_at_pupil_share", k12Pupil, specsFor({ capital_variant: "k12_at_pupil_share" })]];
const specGap = worst(specChecks.flatMap(([, b, sp]) => { const x = pmBand(sp); return [x[0] - b[0], x[1] - b[1]]; }));
gate("the specification-level variants on the payload model give the methods' bands (1e-9): without the capital return, option A, 7%, general government at 0, K-12 at the pupil share",
  specGap < 1e-9, `max |diff| ${ex(specGap)}`);
const VARIANT_ROWS = { uncorrected_at_adopted_responses: uncorrectedAtResponses, without_capital_return: withoutCapital, school_within_district: schoolLow,
  school_within_district_as_response: schoolLowAsResponse, adopted: C, cash_set: Ccash, enterprises_out_option_a: optionA,
  enterprise_receipt_at_model_json_share: atModelShare, capital_return_at_7pct: at7, rental_assistance_at_0: rentalAt0,
  general_government_fixed: ggFixed, k12_capital_at_pupil_share: k12Pupil, audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn };
// The same rows on v6, unrounded, and what v7's items add under each.
const BASE_ROWS = { uncorrected_at_adopted_responses: B6.band(MODEL), without_capital_return: B6.central({ capital: false }),
  school_within_district: B6.central({ school_rule: "within_district" }), school_within_district_as_response: B6.central({ school_rule: "within_district_as_response" }),
  adopted: C6, cash_set: C6cash, enterprises_out_option_a: B6.central({ enterprises: "A" }), enterprise_receipt_at_model_json_share: B6.central({ enterprise_rekey: false }),
  capital_return_at_7pct: B6.central(RATES7), rental_assistance_at_0: B6.central({ rental: 0 }),
  general_government_fixed: bandOf(costsOf(runs(B6.MAIN_SPECS.map((s) => Object.assign({}, s, { gg: 0 })), MAIN_PROFILE, baseModels, B6)).map((xs) => xs.filter((_, i) => true))),
  k12_capital_at_pupil_share: B6.central({ capital_variant: "k12_at_pupil_share" }),
  audit_row3_instead_of_cbo_income_tax: B6.central({ incomeTax: "row3", tax_key: "cbo_2022" }), no_fill_in_correction: B6.evalPackage("central", "audit_rules_alone", {}) };
gate("the base's variant rows print as v6's main_case_bands.csv rows (fx), every one", Object.keys(VARIANT_ROWS).every((v) => {
  const r = row6(MAIN_PROFILE, v);
  return JSON.stringify(Object.keys(BASE_ROWS)) === JSON.stringify(Object.keys(VARIANT_ROWS)) && r.cost_low_bn === fx(BASE_ROWS[v][0]) && r.cost_high_bn === fx(BASE_ROWS[v][1]);
}), `${Object.keys(BASE_ROWS).length} rows`);
const itemsByVariant = Object.fromEntries(Object.entries(VARIANT_ROWS).map(([v, b]) => [v, minus(b, BASE_ROWS[v])]));

// Every arm of every applied item, v6's and v7's: the whole case with that item at the arm (package.cjs caseOf).
const armRows = [];
const caseCash = (Q) => { const cm = costsOf(caseRuns(Q, "cash")); return { band: bandOf(cm), ends: ends(cm) }; };
const armItems = PKG.V6_PACKAGE.CANDIDATE.map((id) => PKG.REGISTRY.find((it) => it.id === id)).concat(NEW.map((id) => PKG.REGISTRY.find((it) => it.id === id)));
let armPT = null;
for (const it of armItems) for (const [name, arm] of Object.entries(it.arms || {})) {
  const Q = PKG.caseOf(B5, PKG.CANDIDATE, { [it.id]: name });
  if (it.id === "pension_tr2026" && name === "combined_funds") armPT = Q;
  const cm = costsOf(caseRuns(Q, "set")), band = bandOf(cm), armEnds = ends(cm);
  const cc = consumerCosts(Q.correctionsPayload()).filter((_, i) => IN_BAND[i]);
  const ccc = consumerCosts(Q.CASH_PAYLOAD).filter((_, i) => IN_BAND[i]);
  const cash = caseCash(Q);
  const tag = NEW.includes(it.id) ? ST(it.id) : STALL;
  gate(`${tag}arm ${it.id}_${name}: the case at the arm is consumer.cjs's band over its payload's personal specifications (1e-9), the same ends in both methods, set and cash; its payload is a variant`,
    [0, 1].every((e) => near(band[e], spanOf(cc)[e], 1e-9) && near(cash.band[e], spanOf(ccc)[e], 1e-9)) && sameEnds(armEnds) && sameEnds(cash.ends)
    && Q.correctionsPayload().meta.adopted === null && /^variant: /.test(Q.correctionsPayload().meta.status),
    `${f2(band)} at ${armEnds[0].join("/")} (case ${f2(minus(band, C))}); cash ${f2(cash.band)}`);
  const v6arm = V6_ARM_ROW(it.id, name);
  armRows.push({ item: it.id, name, row: `${it.id}_${name}`, label: arm.label, source_arm: arm.source_arm || name, band, ends: armEnds,
    change_from_the_case_bn: minus(band, C), on_v6_band_bn: v6arm ? v6arm.band_bn : null, change_from_v6_arm_bn: v6arm ? minus(band, v6arm.band_bn) : null,
    cash: { band: cash.band, ends: cash.ends, change_from_the_cash_set_bn: minus(cash.band, Ccash), on_v6_band_bn: v6arm && v6arm.cash ? v6arm.cash.band_bn : null },
    has_cash_row: NEW.includes(it.id) || !!(s6.v6.arms[`${it.id}_${name}`] && s6.v6.arms[`${it.id}_${name}`].cash) });
}
function V6_ARM_ROW(id, name) { return s6.v6.arms[`${id}_${name}`] || null; }
// Item row4_frame at pension_tr2026's combined_funds arm (item_row4.cjs's pension rule): the case's parts, oasdi_ratio's
// scaled by the arm's ratio_net over the Trustees arm's and ss_split's and ss_factor's by its f_ss over v6's [APPROX].
{
  const r8 = (Q) => Q.correctionsPayload().meta.items.find((r) => r.id === "row4_frame");
  const c8 = r8(PKG), a8 = armPT ? r8(armPT) : null, pb = armPT ? armPT.correctionsPayload().meta.row4_frame.pension_block : null;
  const kOf = (n) => (/:oasdi_ratio:/.test(n) ? pb.k_ratio_net : /:(ss_split|ss_factor):/.test(n) ? pb.k_f_ss : 1);
  let worst = Infinity, scal = null;
  if (a8 && pb && JSON.stringify(Object.keys(a8.parts)) === JSON.stringify(Object.keys(c8.parts))) {
    worst = 0; scal = { personal: 0, shared: 0 };
    for (const [n, p] of Object.entries(c8.parts)) for (const a of ALLOCS) {
      worst = Math.max(worst, Math.abs(a8.parts[n].by[a] - p.by[a] * kOf(n)));
      scal[a] += a8.parts[n].by[a] - p.by[a];
    }
  }
  const pb0 = payload.meta.row4_frame.pension_block;
  gate("[APPROX] item row4_frame at pension_tr2026's combined_funds arm: the case's parts, oasdi_ratio's times k_ratio_net (the arm's ratio_net over the Trustees arm's) and ss_split's and ss_factor's times k_f_ss (its f_ss over v6's), the rest unchanged (1e-12); the parts' change is scaling_bn (1e-12); at the case both factors are 1",
    worst < 1e-12 && ALLOCS.every((a) => Math.abs(scal[a] - pb.scaling_bn[a]) < 1e-12) && pb.arm === "combined_funds" && pb0.k_ratio_net === 1 && pb0.k_f_ss === 1 && pb0.arm === null,
    pb ? `k ${pb.k_ratio_net.toFixed(6)} / ${pb.k_f_ss.toFixed(6)}; scaling ${ALLOCS.map((a) => pb.scaling_bn[a].toFixed(6)).join(" / ")}bn; max |diff| ${ex(worst)}` : "no arm");
  row4Check.at_combined_funds = pb ? { pension_block: clone(pb), worst_part_gap_bn: worst } : null;
}

// The companion readings on v7: the lineage at the count's arms a and c and at C3 -/+ 1 SE (caseOf's fourth argument,
// every item rebuilt on the option's lineage), the count by ancestry share (ancestry_share.cjs), the school low side
// (the row school_within_district) and the shared allocation (32-63).
const companionRows = [];
const options = {};
for (const [name, o] of Object.entries(PKG.LINEAGE_OPTIONS)) {
  const Q = PKG.caseOf(B5, PKG.CANDIDATE, {}, name), Q6 = Q.OCT07;
  const opt = Q.LINEAGE_OPTION_META;
  const sets = {};
  for (const which of ["set", "cash"]) {
    const X = which === "set" ? Q : Q.CASH, X6 = which === "set" ? Q6 : Q6.CASH;
    const cq = consumerCosts(X.correctionsPayload()).filter((_, i) => IN_BAND[i]), cm = costsOf(caseRuns(Q, which)), band = bandOf(cm);
    const c6x = consumerCosts(X6.correctionsPayload()), v6at = spanOf(c6x);
    gate(`${STALL}lineage option ${name}, ${which === "set" ? "the set" : "the cash set"}: the case at the option (every item, the v7 items rebuilt on the option's lineage) is consumer.cjs's band over its payload's personal specifications (1e-9), the same ends in both methods; its payload is a variant; v6 at the option is v6's stored companion (summary.json v6.companions, 1e-9)`,
      [0, 1].every((e) => near(band[e], spanOf(cq)[e], 1e-9)) && sameEnds(ends(cm)) && X.correctionsPayload().meta.adopted === null
      && X.correctionsPayload().meta.status.startsWith("variant: ") && X.correctionsPayload().meta.lineage.count_option.name === name
      && [0, 1].every((e) => near(v6at[e], s6.v6.companions.options[name][which].band_bn[e], 1e-9)),
      `${f2(band)} at ${ends(cm)[0].join("/")}; v6 at the option ${f2(v6at)}`);
    const at = which === "set" ? C : Ccash, at6 = which === "set" ? C6 : C6cash;
    sets[which] = { band_bn: band, ends: ends(cm)[0], per_member_usd: band.map((x) => x * 1e9 / opt.population),
      change_from_the_case_bn: minus(band, at), v6_at_option_band_bn: v6at, v6_at_option_ends: endsOf(c6x), items_change_at_option_bn: minus(band, v6at),
      items_change_at_the_case_bn: minus(at, at6) };
  }
  options[name] = { label: o.label, arm: opt.arm, source_arm: opt.source_arm, c3: opt.c3, added: opt.added, g3_rate: opt.g3_rate, later: opt.later,
    lineage_population: opt.population, s: opt.s, row8_edit_bn: opt.row8_edit_bn, set: sets.set, cash: sets.cash };
  companionRows.push([`lineage_${name}`, sets.set.band_bn], [`lineage_${name}_cash_set`, sets.cash.band_bn]);
}
const shares = {};
for (const which of ["set", "cash"]) {
  const v7 = AS.rowsFor(P, which, { Engine });
  const v6rows = s6.v6.companions.ancestry_share[which].rows;
  const strip_ = (r) => { const x = Object.assign({}, r); delete x.costs; return x; };
  shares[which] = { rows: v7.rows.map((r) => Object.assign(strip_(r), { v6_band_bn: v6rows.find((x) => x.scenario === r.scenario).band_bn,
      change_from_v6_bn: minus(r.band_bn, v6rows.find((x) => x.scenario === r.scenario).band_bn) })),
    outer_span_bn: [v7.rows.find((r) => r.scenario === "g4_at_nothing").band_bn[0], v7.rows.find((r) => r.scenario === "g4_at_bound").band_bn[1]],
    v6_outer_span_bn: s6.v6.companions.ancestry_share[which].outer_span_bn,
    pension_split_sensitivity: v7.pension_sensitivity, added_people: v7.added_people, row8_edit_bn: v7.row8_edit_bn };
  for (const r of v7.rows) companionRows.push([`ancestry_share_${r.scenario}${which === "cash" ? "_cash_set" : ""}`, r.band_bn]);
}
gate(`${STALL}the count by ancestry share on v7: its rows have their own ends among the 32 case specifications, set and cash; the union's generations with their parts add to the union's model with the same edits (ancestry_share.cjs, 1e-9)`,
  ["set", "cash"].every((w) => shares[w].rows.every((r) => r.ends.every((i) => i >= 0 && i < NP))), ["set", "cash"].map((w) => shares[w].rows.map((r) => `${w} ${r.scenario} ${f2(r.band_bn)} at ${r.ends.join("/")}`).join("; ")).join("; "));
const sharedCm = costsOf(allRuns.map((xs) => xs.slice(NP))), sharedCashCm = costsOf(cashAllRuns.map((xs) => xs.slice(NP)));
const sharedBand = central({ allocation: "shared" }), sharedCash = PC.central({ allocation: "shared" });
const sharedEnds = ends(sharedCm).map((e) => e.map((i) => i + NP)), sharedCashEnds = ends(sharedCashCm).map((e) => e.map((i) => i + NP));
gate("the shared allocation (32-63): central({allocation: \"shared\"}) is the methods' band over the 32 shared specifications, set and cash (1e-9), the same ends in both methods",
  [0, 1].every((e) => near(sharedBand[e], bandOf(sharedCm)[e], 1e-9) && near(sharedCash[e], bandOf(sharedCashCm)[e], 1e-9)) && sameEnds(sharedEnds) && sameEnds(sharedCashEnds),
  `${f2(sharedBand)} at ${sharedEnds[0].join("/")}; cash ${f2(sharedCash)} at ${sharedCashEnds[0].join("/")}`);
companionRows.push(["shared_allocation", sharedBand], ["shared_allocation_cash_set", sharedCash]);
const c3Span = (which) => [Math.min(...["c3_minus_se", "c3_plus_se"].map((n) => options[n][which].band_bn[0])), Math.max(...["c3_minus_se", "c3_plus_se"].map((n) => options[n][which].band_bn[1]))];
const companions = {
  rule: "the readings the record quotes beside the case, on v7: the lineage at the count's arms a and c and at C3 -/+ 1 SE (lineage options, package.cjs caseOf's fourth argument: the whole case at the option, every item rebuilt on the option's lineage, item job_capital_taxes's added people at the option's own cells), the count by share of Mexican-immigrant ancestry (ancestry_share.cjs), the school response 0.836 (the row school_within_district) and the shared allocation (specifications 32-63); rows lineage_<option>, ancestry_share_<scenario>, shared_allocation and their _cash_set in main_case_bands.csv",
  age_mix: s6.v6.companions.age_mix,
  options,
  c3_plus_minus_1se_bn: { set: c3Span("set"), cash: c3Span("cash"), rule: "C3 + 1 SE's low end to C3 - 1 SE's high end (the record's form)" },
  ancestry_share: Object.assign({ rules: AS.RULES, route: AS.ROUTE, shares_file: AS.SHARES_FILE }, shares),
  school_within_district: { row: "school_within_district", band_bn: schoolLow, ends: schoolLowEnds.ends[0], note: "the low side with the within-district school response 0.836: set only, as v6's" },
  shared_allocation: { rows: ["shared_allocation", "shared_allocation_cash_set"], band_bn: sharedBand, ends: sharedEnds[0], cash: { band_bn: sharedCash, ends: sharedCashEnds[0] },
    per_member_usd: sharedBand.map((x) => x * 1e9 / L.counts.lineage_population),
    rule: "the case at the shared allocation (specifications 32-63, v6's numbering): for distribution inside the group and comparisons between groups, where both sides share alike; item child_credits is 0 there (personal cells only), item job_capital_taxes prices the shared cells; not the group total (meta.allocation)" },
  not_built: [],
};

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the uncorrected model at the case's responses]");
const MODEL_SYN = P.withSyntheticLines(MODEL);
const addedLines = (side) => MODEL_SYN[side].lines.slice(MODEL[side].lines.length);
const zeroCells = (cells) => Object.values(cells).every((c) => ALLOCS.every((a) => c[a].target_bn === 0 && c[a].other_bn === 0 && c[a].share === 0));
const CARRIER_IDS = P.ITEM_RECEIPT_LINES.map((l) => l.id);
const carrierNational = new Map(P.ITEM_RECEIPT_LINES.map((l) => [l.id, l.national_bn]));
gate(`withSyntheticLines(model.json) appends the payload's 8 spending lines and 2 receipt lines at zero, then the items' ${CARRIER_IDS.length} carrier lines at zero amounts and shares (their national totals kept), and leaves the rest of the model as it was`,
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
gate("the uncorrected model evaluates at every case specification in every profile: each line_responses entry has its engine row (the added lines at amount 0), and in the main profile each row takes the specification's response (item job_capital_taxes's four lines at their uncorrected cells)",
  ucRows && ucResponses, `${ucProfiles.length} profiles x ${specs.length} specifications`);
gate("Engine.evaluate(withSyntheticLines(m), stateFor(m, spec, profile)) is evaluateFull's evaluation on the uncorrected model (exact)", ucDirect === 0, `${ucN} evaluations`);
const zeroPayload = { lines: payload.lines, edits: [], meta: payload.meta,
  receipt_lines: payload.receipt_lines.map((l) => Object.assign({}, l, { national_bn: carrierNational.has(l.id) ? carrierNational.get(l.id) : 0, cells: Object.fromEntries(Object.entries(l.cells)
    .map(([sc, c]) => [sc, Object.fromEntries(ALLOCS.map((a) => [a, Object.assign({}, c[a], { target_bn: 0, other_bn: 0, share: 0 })]))])) })) };
const ucIndependent = Consumer.evaluateAll(JSON.parse(JSON.stringify(zeroPayload)), { engine: Engine, model: MODEL }).filter((_, i) => IN_BAND[i]);
const ucPackage = specs.map((s) => evaluateFull(MODEL, s).cost_bn);
const ucGap = worst(ucIndependent.map((x, i) => x.cost_bn - ucPackage[i]));
gate("consumer.cjs on model.json with the payload's lines at zero gives the package's uncorrected cost at every case specification (1e-9), and its span is uncorrected_at_adopted_responses",
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
  "every case specification, both methods");
const laneShareRuns = runs(specs, MAIN_PROFILE, MODELS_LANE);
const rekeyEffect = atEnds(newEnds, (m, i) => newCosts[m][i] - laneShareRuns[m][i].cost_bn);
const publicHousing = atEnds(newEnds, (m, i) => byId(newRuns[m][i], "ent_housing_sl"));
const es29 = s29.enterprises.receipt_at_end_specifications;
const esAmount = atEnds(newEnds, (m, i) => esRow(newRuns[m][i]).amount_bn);
const esNat = payloadModel.receipts.lines.find((l) => l.id === ENTERPRISE_LINE).national_bn;
const esModel = MODEL.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
const kc = readJson(`${CAPDIR}/summary.json`).enterprises.key_consistency;
const moveRekey = [0, 1].map(() => esNat * (SHARE - kc.receipt_key[0]));
const moveSplit = [0, 1].map(() => (esNat - esModel.national_bn) * kc.receipt_key[0]);
const schoolsEsAt = (a) => es29.group_amount_bn[a === "shared" ? 0 : 1] - es29.move_from_the_schools_case_bn[a === "shared" ? 0 : 1];
const receiptMove = [0, 1].map((e) => esAmount[e] - (es29.group_amount_bn[e] - es29.move_from_the_schools_case_bn[e]));
gate("the enterprise receipt is the corrected share times its national total at every case specification (the re-key, the lineage's included, and item 1's split of public housing; 1e-9)",
  newRuns.every((xs) => xs.every((r) => near(esRow(r).amount_bn, SHARE * esNat, 1e-9))) && near(esNat, esModel.national_bn - V4.HOUSING_SURPLUS, 1e-9),
  `${fx(SHARE * esNat)} of ${fx(esNat)}`);
const LAND_ROW = /^((block|enterprise): )?land at 10% of the structures charged: (\S+)$/;
const landRows = capGaps.filter((r) => LAND_ROW.test(r.item));
const landPart = (r) => r.item.match(LAND_ROW)[2] || "core";
const landStock = Object.fromEntries(landRows.map((r) => [r.item.match(LAND_ROW)[3], Number(r.national_base_bn) * Number(r.fee_factor)]));
const LAND_OF = Object.fromEntries(COMPONENTS.map((c) => [c.id, c.of_component || c.id]));
gate("gaps.csv has one land row for every capital component of the payload, under its part (an item's offset component the row of the component it offsets)",
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
const pBand = (part_) => P.band(Engine.applyCorrections(MODEL, part_));
const payloadBand = pBand(payload);
const recOnly = pBand({ lines: payload.lines, receipt_lines: payload.receipt_lines, edits: payload.edits.filter((e) => e.side === "receipt") });
const spOnly = pBand({ lines: payload.lines, edits: payload.edits.filter((e) => e.side !== "receipt") });
const prodOnly = pBand({ lines: payload.lines, edits: [], production: payload.production });
const sides = { receipts: minus(recOnly, uc), spending: minus(spOnly, uc), production: minus(prodOnly, uc) };
gate("corrections.json reproduces the case (1e-9)", near(payloadBand[0], C[0], 1e-9) && near(payloadBand[1], C[1], 1e-9), f2(payloadBand));
gate("the three sides (receipts, spending, the production grid) add to the payload's band less the uncorrected band (1e-6)",
  [0, 1].every((e) => near(sides.receipts[e] + sides.spending[e] + sides.production[e], payloadBand[e] - uc[e], 1e-6)),
  `${f2(sides.receipts)} + ${f2(sides.spending)} + ${f2(sides.production)}`);
const receiptsTotal = (m) => Object.fromEntries(ALLOCS.map((a) => [a, m.receipts.lines.reduce((s, l) => s + l.cells[m.receipts.reference][a].target_bn, 0)]));
const groupReceipts = Object.assign({}, s6.group_receipts_bn, { adopted: receiptsTotal(payloadModel), adopted_2026_10_07: s6.group_receipts_bn.adopted });

// The lineage's additions, in the lineage lane's payload format, as v6 writes them (meta.lineage.payload names v6's
// copies, which these equal byte for byte).
const IB = P.ITEM_BASE;
const LINEAGE_FILES = { "lineage_payload.json": JSON.stringify(IB.ADDITION.set, null, 1) + "\n", "lineage_payload_cash.json": JSON.stringify(IB.ADDITION.cash, null, 1) + "\n" };
gate("the lineage payloads are the case's lineage additions (its item base's), and equal v6's derived files byte for byte",
  Object.entries(LINEAGE_FILES).every(([f, t]) => t === fs.readFileSync(path.join(FISCAL, OCT07, "derived", f), "utf8")) && P.LINEAGE_ITEM === "added_age_mix",
  Object.keys(LINEAGE_FILES).join(", "));

// ---------------------------------------------------------------------------------------------------
if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
const full = (x) => (typeof x === "number" ? String(x) : x);
const endSpecs = newEnds.map((e, m) => ({ method: METHODS[m], low_end: Object.assign({ index: e[0] }, specs[e[0]]), high_end: Object.assign({ index: e[1] }, specs[e[1]]) }));
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
const keep6 = (pf, variant) => rawRow6(pf, variant);
const renamed6 = (pf, variant, as) => { const c = rawRow6(pf, variant).split(","); c[1] = as; return c.join(","); };
const v6Arm = new Set(Object.keys(s6.v6.arms));
const armLine = (a) => [row(MAIN_PROFILE, a.row, a.band)].concat(a.has_cash_row ? [row(MAIN_PROFILE, `${a.row}_cash_set`, a.cash.band)] : []);
const aloneRows = alone.flatMap((x) => [row(MAIN_PROFILE, `${x.r.id}_alone`, bandOf(x.costs)), row(MAIN_PROFILE, `${x.r.id}_alone_cash_set`, bandOf(x.cashCosts))]);
const bandsCsv = ["profile,variant,cost_low_bn,cost_high_bn,range_low_bn,range_high_bn",
  keep6(MAIN_PROFILE, "first_year_response"),
  keep6(MAIN_PROFILE, "schools_case"),
  keep6(MAIN_PROFILE, "sept27_case"),
  keep6(MAIN_PROFILE, "sept29_case"),
  keep6(MAIN_PROFILE, "oct05_case"),
  renamed6(MAIN_PROFILE, "adopted", "oct07_case"),
  row(MAIN_PROFILE, "uncorrected_at_adopted_responses", uncorrectedAtResponses),
  keep6(MAIN_PROFILE, "long_run_responses_alone"),
  keep6(MAIN_PROFILE, "rental_assistance_alone"),
  keep6(MAIN_PROFILE, "long_run_responses_and_capital_return_option_a"),
  row(MAIN_PROFILE, "without_capital_return", withoutCapital),
  row(MAIN_PROFILE, "school_within_district", schoolLow),
  row(MAIN_PROFILE, "school_within_district_as_response", schoolLowAsResponse),
  row(MAIN_PROFILE, "adopted", C, [rangeLowEnd[0], rangeHighEnd[1]]),
  row(MAIN_PROFILE, "cash_set", Ccash),
  keep6(MAIN_PROFILE, "sept29_cash_set"),
  keep6(MAIN_PROFILE, "oct05_cash_set"),
  renamed6(MAIN_PROFILE, "cash_set", "oct07_cash_set"),
  row(MAIN_PROFILE, "enterprises_out_option_a", optionA),
  row(MAIN_PROFILE, "enterprise_receipt_at_model_json_share", atModelShare),
  row(MAIN_PROFILE, "capital_return_at_7pct", at7),
  row(MAIN_PROFILE, "rental_assistance_at_0", rentalAt0),
  row(MAIN_PROFILE, "general_government_fixed", ggFixed),
  row(MAIN_PROFILE, "k12_capital_at_pupil_share", k12Pupil),
  row(MAIN_PROFILE, "audit_row3_instead_of_cbo_income_tax", withRow3),
  row(MAIN_PROFILE, "no_fill_in_correction", noFillIn)]
  .concat(armRows.filter((a) => v6Arm.has(a.row)).flatMap(armLine))
  .concat(companionRows.filter(([v]) => !v.startsWith("shared_allocation")).map(([v, b]) => row(MAIN_PROFILE, v, b)))
  .concat(aloneRows, armRows.filter((a) => !v6Arm.has(a.row)).flatMap(armLine), companionRows.filter(([v]) => v.startsWith("shared_allocation")).map(([v, b]) => row(MAIN_PROFILE, v, b)))
  .concat([keep6(oldProfile.profile, "schools_case"),
    row(oldProfile.profile, "with_rental_assistance_capital_and_enterprises", oldProfile.with_rental_assistance_capital_and_enterprises)])
  .concat(Object.entries(otherProfiles).flatMap(([pf, v]) => [keep6(pf, "schools_case"),
    row(pf, "uncorrected_at_adopted_responses", v.uncorrected_at_adopted_responses), row(pf, "adopted", v.adopted)]));
const compCsv = ["component,label,range_dev_low_end_lo,range_dev_low_end_hi,range_dev_high_end_lo,range_dev_high_end_hi"]
  .concat(components.map((x) => [x.name, `"${x.label}"`, fx(x.lo[0]), fx(x.hi[0]), fx(x.lo[1]), fx(x.hi[1])].join(",")));
// per_spec.csv: v6's columns with v7's values at all 64 specifications per method; v6's item columns (its items'
// change from v5) as v6 printed them; then in_band and the v7 columns.
const head6 = fs.readFileSync(path.join(FISCAL, OCT07, "derived", "per_spec.csv"), "utf8").split("\n")[0].split(",");
const V6_ITEM_COLS = ["oct05_cost_bn"].concat(PKG.V6_PACKAGE.CANDIDATE.map((id) => `item_${id}_bn`), ["items_interaction_bn"]);
const offsetCols = COMPONENTS.filter((c) => c.of_component).map((c) => `capital_${c.id}_bn`);
const NEW_COLS = ["in_band", "oct07_cost_bn"].concat(EDIT_SETS.map((r) => `item_${r.id}_bn`), ["items_v7_interaction_bn"]);
const perHead = head6.concat(NEW_COLS);
const aloneAll = EDIT_SETS.map((r) => aloneOf(r.id).costs);
const perSpec = [perHead.join(",")].concat(METHODS.flatMap((meth, m) => ALL.map((s, i) => {
  const r = allRuns[m][i], r6 = ps6.find((x) => x.method === meth && Number(x.spec) === i);
  const vals = {
    method: meth, spec: i, allocation: s.allocation, normalization: s.normalization, share: s.share, school: s.school, gg: s.gg, uc: s.uc, justice: s.justice,
    reading: s.reading, rate: s.rate, enterprises: s.enterprises, cost_bn: r.cost_bn, engine_cost_bn: -r.evaluation.welfare_bn, capital_total_bn: r.capital.total_bn,
    capital_state_local_bn: capitalWhere(r, (c) => c.level === "state_local"), capital_federal_bn: capitalWhere(r, (c) => c.level === "federal"),
    capital_core_bn: capitalGroup(r, "core"), capital_block_bn: capitalGroup(r, "block"), capital_enterprise_bn: capitalGroup(r, "enterprise"),
    response_receipt_enterprise_surplus: esRow(r).response, group_enterprise_surplus_bn: esRow(r).amount_bn, enterprise_surplus_receipt_cost_bn: esCost(r),
  };
  for (const c of COMPONENTS) vals[`capital_${c.id}_bn`] = byId(r, c.id);
  for (const id of LR_LINES.concat([RENTAL])) { vals[`response_${id}`] = responseOf(r.evaluation, id); vals[`group_${id}_bn`] = amount(r.evaluation, id); }
  for (const k of V6_ITEM_COLS) vals[k] = r6[k];
  vals.in_band = IN_BAND[i] ? "true" : "false";
  vals.oct07_cost_bn = baseAllCosts[m][i];
  EDIT_SETS.forEach((it, k) => { vals[`item_${it.id}_bn`] = aloneAll[k][m][i] - baseAllCosts[m][i]; });
  vals.items_v7_interaction_bn = allCosts[m][i] - baseAllCosts[m][i] - aloneAll.reduce((t, cm) => t + cm[m][i] - baseAllCosts[m][i], 0);
  const missing = perHead.filter((h) => !(h in vals));
  if (missing.length) throw new Error(`[BLOCKED] per_spec.csv: no value for ${missing.join(", ")}`);
  return perHead.map((h) => full(vals[h])).join(",");
})));
const PER = (x) => x * 1e9 / L.counts.lineage_population;
// The v7 block.
const changeByItem = {
  personal_allocation: { band_bn: allocMove, cash_bn: allocMoveCash, ends: { v6: [48, 11], v6_personal: v6PersonalEnds[0] },
    rule: "v6 read at its 32 personal specifications less v6 read at all 64: the low end moves from specification 48 (shared) to 16 (personal); the high end stays at 11 (personal)" },
};
for (const x of itemParts) {
  changeByItem[x.id] = { at_end_specifications_bn: x.set.total, parts: x.set.parts, union: groupSum(x.set.parts, "union_"), lineage: groupSum(x.set.parts, "lineage_"),
    cash: { at_end_specifications_bn: x.cash.total, parts: x.cash.parts, union: groupSum(x.cash.parts, "union_"), lineage: groupSum(x.cash.parts, "lineage_"),
      by_generation: byGeneration(x.cash.parts), ...(x.cash.by_line ? { by_line: x.cash.by_line } : {}) },
    by_generation: byGeneration(x.set.parts), ...(x.set.by_line ? { by_line: x.set.by_line } : {}) };
}
const endMove = [0, 1].map((e) => mean(newEnds.map((ij, m) => baseCosts[m][ij[e]])) - v6Personal[e]);
const v7Block = {
  status: P.ADOPTED ? `adopted ${P.ADOPTED} (${P.DECISION})` : `the candidate: the payloads carry adopted null and status "candidate: main case v7, not adopted ..."; package.cjs STATUS is the switch (the decision file must exist before "adopted")`,
  stub: STUB ? { items: Object.entries(SRC).filter(([, s]) => s.stub).map(([k]) => k), note: "[STUB] the items read invented stub files (sources.cjs LANES), not the worker lanes' measurements: no figure here is a result" } : false,
  case_key: P.CASE_KEY,
  base: { lane: OCT07, payload: `${OCT07}/derived/corrections.json`, cash: `${OCT07}/derived/corrections_cash.json`, edits: N6, cash_edits: N6C,
    band_bn: C6, cash_set_bn: C6cash, end_specifications: [48, 11], personal_band_bn: v6Personal, personal_cash_set_bn: v6PersonalCash, personal_end_specifications: v6PersonalEnds[0] },
  band_bn: C, cash_set_bn: Ccash,
  end_specifications: { set: ENDS, cash: CASH_ENDS, by_method: { set: newEnds, cash: cashEnds } },
  per_member_usd: { set: C.map(PER), cash: Ccash.map(PER), population: L.counts.lineage_population },
  change_from_the_october_7_case_bn: minus(C, C6),
  change_from_the_october_7_cash_set_bn: minus(Ccash, C6cash),
  change_by_item: changeByItem,
  interactions: Object.fromEntries(pairs.map((q) => [q.ids.join("_x_"), { at_end_specifications_bn: atEnd(q.set), cash_at_end_specifications_bn: [q.cash[CASH_ENDS[0]], q.cash[CASH_ENDS[1]]],
    span_bn: spanOf(q.set), cash_span_bn: spanOf(q.cash) }]).concat([["remainder", { at_end_specifications_bn: atEnd(residual), cash_at_end_specifications_bn: [cashResidual[CASH_ENDS[0]], cashResidual[CASH_ENDS[1]]],
    span_bn: spanOf(residual), cash_span_bn: spanOf(cashResidual) }]])),
  end_move_bn: endMove,
  change_rule: "v7 less v6 at the band's ends = personal_allocation (v6's band read at the 32 personal specifications less at all 64) + each edit set alone on v6 at v7's end specifications + the pairs' interactions (zero) + end_move_bn (v6 at v7's end specifications less v6's personal band: zero while the ends stay 16 / 11)",
  items: P.V7_ITEMS.map((r) => ({ id: r.id, label: r.label, kind: r.kind, source: r.source, applied: r.applied, edits: r.edits || null, meta_changed: r.meta_changed || [],
    cash: PC.V7_ITEMS.find((x) => x.id === r.id).applied, arms: Object.keys(r.arms || {}), stub: r.stub === undefined ? null : r.stub,
    alone_on_v6: (() => { const x = aloneOf(r.id); return { band_bn: bandOf(x.costs), cash_set_bn: bandOf(x.cashCosts), specifications: x.nSpecs }; })() })),
  child_credits: creditsCheck ? Object.assign({ by_generation_bn: PKG.CREDITS.R.byGen }, creditsCheck) : null,
  job_capital_taxes: jobcapCheck ? Object.assign({ responses: Object.fromEntries(JC_LINES.map((id) => [id, { low: payload.meta.responses[id].low, high: payload.meta.responses[id].high }])),
    lineage_wage_share: P.ITEM_DETAIL.job_capital_taxes.set.wage_share, production_capital_tax_term: capTerm }, jobcapCheck) : null,
  row4_class: row4Check,
  change_at_every_specification: { personal_bn: spanOf(change.slice(0, NP)), shared_bn: spanOf(change.slice(NP)), cash: { personal_bn: spanOf(cashChange.slice(0, NP)), shared_bn: spanOf(cashChange.slice(NP)) },
    note: "the methods' mean change from v6 at each specification (consumer.cjs on v7's payload less on v6's); the package's runs equal it at every specification (1e-9)" },
  items_by_variant_row_bn: itemsByVariant,
  arms: Object.fromEntries(armRows.map((a) => [a.row, { item: a.item, arm: a.name, source_arm: a.source_arm, label: a.label, band_bn: a.band, end_specifications: a.ends,
    change_from_the_case_bn: a.change_from_the_case_bn, on_v6_band_bn: a.on_v6_band_bn, change_from_v6_arm_bn: a.change_from_v6_arm_bn,
    cash: { band_bn: a.cash.band, end_specifications: a.cash.ends, change_from_the_cash_set_bn: a.cash.change_from_the_cash_set_bn, on_v6_band_bn: a.cash.on_v6_band_bn } }])),
  arms_note: "each arm is the whole case with that item at the arm and the others as they are (package.cjs caseOf with {item: arm}); on_v6_band_bn is v6's row for v6's arms",
  companions,
  variants_rule: "an option leaves the fixed amounts of items child_credits, white_end_tax_keys and row4_frame at the case's (package.cjs forItems7, which stops on an option that changes the national total of a line they edit), as v6 leaves its fixed-amount items'; a lineage option rebuilds their added people's parts at its counts; item job_capital_taxes re-keys every model (editsAt), so the four lines hold the job-capital amounts on the option's cell totals; candidate v4's route (the item variants) takes the four receipt responses after it (package.cjs fixReceipts, gated equal to the engine's route at the case's own options)",
  payload: { file: "derived/corrections.json", cash: "derived/corrections_cash.json", stamped: P.STAMPED,
    from: { set: [`${OCT07}/derived/corrections.json`, "package.cjs REGISTRY: the v7 edit sets' edits, appended"], cash: [`${OCT07}/derived/corrections_cash.json`, "package.cjs REGISTRY: the v7 edit sets' edits, appended"] },
    lineage_payloads: { set: "derived/lineage_payload.json", cash: "derived/lineage_payload_cash.json", note: `v6's lineage additions, byte for byte (meta.lineage.payload still names ${OCT07}'s copies)` },
    built_by: `${P.LANE}/package.cjs caseOf(), caseOn(), forItems7()` },
  history: "first_year_response, schools_case, sept27_case, sept29_case, oct05_case, oct07_case, sept29_cash_set, oct05_cash_set, oct07_cash_set, adopted_2026_09_2x, adopted_2026_10_05 and adopted_2026_10_07, the three September 27 additions, each_addition's earlier entries, change_at_fixed_specifications.oct07_case, the schools_case rows of the other profiles, enterprises.capital_lane_rows_before_rental_assistance, enterprises.interest, beside_the_account.congestion, group_receipts_bn's earlier entries, per_spec.csv's v6 item columns and the v4, v5 and v6 blocks are v6's values (its summary.json, main_case_bands.csv and per_spec.csv)",
  inputs: Object.fromEntries([`${OCT07}/derived/summary.json`, `${OCT07}/derived/main_case_bands.csv`, `${OCT07}/derived/per_spec.csv`, `${OCT07}/derived/corrections.json`,
    `${OCT07}/derived/corrections_cash.json`, SRC.child_credits.file, SRC.job_capital_taxes.file, "receipt_side_long_run_2026_09_28/derived/probe.json", MODULE_FILE,
    SRC7.white_end_tax_keys.file, SRC7.row4_frame.oracle.file, ...Object.keys(SRC7.row4_frame.files),
    "generation_account_2026_09_24/derived/generation_corrections_sept29.json", "generation_account_2026_09_24/derived/generation_corrections_sept29_cash.json",
    "assumption_explorer_2026_09_21/engine.js", "assumption_explorer_2026_09_21/derived/model.json"].map((f) => [f, sha256(f)])),
};
const summary = {
  lane: P.LANE,
  decision: P.DECISION,
  adopted_2026_09_23: s6.adopted_2026_09_23, adopted_2026_09_24: s6.adopted_2026_09_24,
  adopted_2026_09_26: s6.adopted_2026_09_26, adopted_2026_09_26_schools: s6.adopted_2026_09_26_schools,
  adopted_2026_09_27: s6.adopted_2026_09_27, adopted_2026_09_29: s6.adopted_2026_09_29, adopted_2026_10_05: s6.adopted_2026_10_05,
  adopted_2026_10_07: s6.main_case,
  first_year_response: s6.first_year_response, schools_case: s6.schools_case,
  uncorrected_at_adopted_responses: uncorrectedAtResponses, without_capital_return: withoutCapital,
  main_case: C,
  cash_set: { band_bn: Ccash, by_method_bn: Object.fromEntries(METHODS.map((m, k) => [m, ownBands(cashCosts)[k]])), end_specifications: cashEnds,
    change_from_main_case_bn: minus(Ccash, C), change_from_the_september_29_cash_set_bn: cashTotal,
    change_from_the_october_5_cash_set_bn: s6.cash_set.change_from_the_october_5_cash_set_bn, change_from_the_october_7_cash_set_bn: minus(Ccash, C6cash),
    note: `the set with the pension switch off (pension4 "cash"), at the personal allocation: social security and Medicare's Part A at the group's current benefits instead of the accrual at payable benefits net of the tax on benefits; the payload is derived/corrections_cash.json (${OCT07}/derived/corrections_cash.json with the cash edit sets' ${PC.V7_EDITS.length} edits after v6's, item job_capital_taxes's responses, the stamps and meta.items)` },
  change: minus(C, C6),
  change_at_fixed_specifications: {
    items: changeByItem,
    interactions: Object.fromEntries(pairs.map((q) => [q.ids.join("_x_"), atEnd(q.set)]).concat([["remainder", atEnd(residual)]])),
    total: minus(C, C6),
    note: `v7's change from v6: personal_allocation moves v6's ends from 48 (shared) / 11 to the personal allocation's 16 / 11 (v6 read at the 32 personal specifications less at all 64); each edit set's change is the item alone on v6 at v7's end specifications (${ENDS.join(" low, ")} high in both methods), averaged, by part (each cell shift's amount at the end's allocation times its line's response; receipts at ${REF}); union_* parts are the identified 39.71M's by generation, lineage_* the 3.04M added people's. The items, the pair's interaction and end_move_bn add to total. oct07_case holds v6's own change from v5, by item, with v5's under oct07_case.oct05_case`,
    oct07_case: s6.change_at_fixed_specifications },
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
    capital_lane_rows_before_rental_assistance: s6.enterprises.capital_lane_rows_before_rental_assistance,
    overlap_with_rental_assistance: overlap,
    interest: s6.enterprises.interest,
    proportional_reference: s6.enterprises.proportional_reference,
    public_housing: s6.enterprises.public_housing },
  school: { rules: P.RULES, within_district: schoolLow, within_district_as_response: schoolLowAsResponse,
    end_specifications: { average: newEnds, within_district: schoolLowEnds.ends, within_district_as_response: schoolLowAsResponseEnds.ends },
    note: "the schools case's low side on this case: every case specification re-run with that school rule (the K-12 capital return follows the school response); the within-district response is read at v4's pupil share, without the added people's pupils; end_specifications are [low end, high end] per fill-in method",
    sign_break_even: s6.school.sign_break_even },
  rental_assistance: { group_amount_by_method_bn: Object.fromEntries(METHODS.map((m, k) => [m, Object.fromEntries(ALLOCS.map((a, j) => [a, rentalAmount[k][j]]))])),
    uncorrected_group_amount_bn: Object.fromEntries(ALLOCS.map((a, j) => [a, rentalUncorrected[j]])),
    note: s6.rental_assistance.note, overlap_netted_bn: 0 },
  responses: P.RESPONSES,
  range: { low_end: rangeLowEnd, high_end: rangeHighEnd, overall: [rangeLowEnd[0], rangeHighEnd[1]], quadrature,
    note: `every component re-runs the whole case, the added people included, at every case specification (the 32 personal ones); the band's ends are minima and maxima over them; option A, 7% and items 8 and 10 are beside the range, not in it. The components are the September 29 case's; ${skipped.join(", ")} moves nothing (item 8 is beside the case). The added people's own amounts are the case's in every variant but on item job_capital_taxes's four lines, which every variant re-keys; first_order lists the variants whose own group-size reading is moved at first order or kept at v4's group`,
    first_order: FIRST_ORDER,
    at_the_case_data: { components: atCaseData, added_share: addedShare, range_ends_move_if_proportional_bn: atCaseDataMove, note: s6.range.at_the_case_data.note },
    items_at_the_case_data: itemsAtCaseData },
  other_profiles: otherProfiles, old_main_profile: oldProfile,
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn,
  each_addition: Object.assign({}, s6.each_addition, Object.fromEntries(alone.map((x) => [x.r.id, bandOf(x.costs)]))),
  beside_the_account: {
    rate_7pct: { band_bn: at7, return_at_end_specifications_bn: atEnds(newEnds, (m, i) => runs7[m][i].capital.total_bn), note: s6.beside_the_account.rate_7pct.note },
    land_per_10pct_of_land_to_structure_value: land,
    enterprises_out_option_A: { band_bn: optionA, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => optionARuns[m][i].cost_bn - newCosts[m][i]),
      note: s6.beside_the_account.enterprises_out_option_A.note },
    rental_assistance_at_0: { band_bn: rentalAt0, note: s6.beside_the_account.rental_assistance_at_0.note },
    congestion: Object.assign({}, s6.beside_the_account.congestion, { not_recomputed_v7: "the September 27 figure, carried since; v7's items do not reprice it" }),
    transit_at_riders_key_item_8: { band_bn: with8, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => runs8[m][i].cost_bn - newCosts[m][i]),
      options: beside8.o, note: `${beside8.name}: beside the case (candidate v4's BESIDE_ITEMS), not in it` },
    uninsured_use_0_7x_item_10: { band_bn: with10, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => runs10[m][i].cost_bn - newCosts[m][i]),
      options: beside10.o, note: `${beside10.name}: beside the case (candidate v4's BESIDE_ITEMS), not in it` },
  },
  by_side_vs_uncorrected_at_adopted_responses: sides,
  group_receipts_bn: groupReceipts,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi, variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
  v4: s6.v4,
  v5: s6.v5,
  v6: s6.v6,
  v7: v7Block,
};
fs.writeFileSync(path.join(OUT, "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "components.csv"), compCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "corrections.json"), JSON.stringify(payload, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "corrections_cash.json"), JSON.stringify(cashPayload, null, 1) + "\n");
for (const [f, text] of Object.entries(LINEAGE_FILES)) fs.writeFileSync(path.join(OUT, f), text);

console.log(`\n[result]${STUB ? " [STUB: invented inputs, not a result]" : ""}`);
console.log(`  ${STALL}main case v7                 ${f2(C)}  ends ${ENDS.join("/")}; $${C.map((x) => Math.round(PER(x))).join(" / ")} per member`);
console.log(`  ${STALL}cash set                     ${f2(Ccash)}  ends ${CASH_ENDS.join("/")}`);
console.log(`  v6                              ${f2(C6)}; cash ${f2(C6cash)}`);
console.log(`  v6 at the personal allocation   ${f2(v6Personal)} (move ${f2(allocMove)}); cash ${f2(v6PersonalCash)}`);
for (const x of itemParts) console.log(`  ${ST(x.id)}item ${x.id}: ${f2(x.set.total)}; cash ${f2(x.cash.total)}`);
for (const q of pairs) console.log(`  interaction ${q.ids.join(" x ")}: ${f2(atEnd(q.set))}`);
console.log(`  ${STALL}shared allocation            ${f2(sharedBand)}; cash ${f2(sharedCash)}`);
for (const a of armRows) console.log(`  ${NEW.includes(a.item) ? ST(a.item) : ""}arm ${a.row.padEnd(34)} ${f2(a.band)} (from the case ${f2(a.change_from_the_case_bn)})`);
for (const [n, o] of Object.entries(options)) console.log(`  lineage ${n.padEnd(11)} ${f2(o.set.band_bn)}; cash ${f2(o.cash.band_bn)}`);
for (const w of ["set", "cash"]) for (const r of shares[w].rows) console.log(`  ancestry share, ${w} ${r.scenario.padEnd(13)} ${f2(r.band_bn)} at ${r.ends.join("/")}`);
console.log(`  school low side                 ${f2(schoolLow)}`);
console.log(`  range                           ${rangeLowEnd[0].toFixed(1)}–${rangeHighEnd[1].toFixed(1)} (quadrature ${quadrature[0].toFixed(1)}–${quadrature[1].toFixed(1)})`);
console.log("all gates passed");
