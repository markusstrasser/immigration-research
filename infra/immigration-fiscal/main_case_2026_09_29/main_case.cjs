/* The main case adopted on 2026-09-29 (candidate v4's set; decisions/2026-09-29-main-case-v4.md), written to the
 * September 27 lane's output contract (main_case_long_run_2026_09_27/derived: main_case_bands.csv, components.csv,
 * per_spec.csv, summary.json and corrections.json here; sign_reversal.cjs writes sign_reversal.csv). package.cjs holds
 * the definitions; this script runs the gates and writes derived/.
 *
 * Every September 27 file, column, row name and key is kept, with v4's value where the quantity is defined on v4. The
 * rows and keys that record how the September 27 case was built from the schools case keep that lane's values, read
 * from its summary.json and re-derived through this package on its payload (history): first_year_response,
 * schools_case, long_run_responses_alone, rental_assistance_alone, long_run_responses_and_capital_return_option_a,
 * each_addition's September 27 entries, the capital lane's rows before rental assistance and the congestion item. One
 * block moves: change_at_fixed_specifications holds v4's change from the September 27 case, item by item, so the
 * September 27 case's own parts sit under change_at_fixed_specifications.sept27_case. RESULT.md lists every row and key
 * by kind; contract.cjs checks the files against the September 27 lane's.
 *
 * Added: the band rows sept27_case and cash_set; the keys adopted_2026_09_27, cash_set, receipts_at_end_specifications
 * and v4; v4's correction lines in lines_at_end_specifications; v4's items in each_addition; the range components of
 * items 5 and 6a (candidate v3's rangeComponents(); transit's moves nothing here, item 8 being beside); items 8 and 10
 * beside the account; the production side in by_side_vs_uncorrected_at_adopted_responses.
 *
 * Gates (exit 1 and nothing written on failure):
 *   G1  the band is candidate v4's (main_case_candidate_v4_2026_09_29/derived/summary.json bands, bands.csv): the set and
 *       the cash set, the two methods' mean and each method, with the end specifications 48 / 11 in both methods (1e-9);
 *       the payload models (the set's and the cash set's) give the methods' mean at every specification (1e-9), as does
 *       consumer.cjs (engine.js, model.json and the payload, no package); the package's evaluation is candidate v4's
 *       package's at every specification.
 *   and the payload is corrections_v4.json with the adoption stamps alone changed; RESPONSES, componentsFor(null) and the
 *       specifications carry its meta; a specification has no field beyond the September 27 ones; the profiles hold each
 *       correction line with its parent; general government at 0 moves only its line and its capital; v4's items, added in
 *       the brief's order, add up to the change from the September 27 case, and each item alone is the candidate's
 *       attribution; the history rows are the September 27 lane's and re-derive through this package on its payload.
 * Run from anywhere: node main_case.cjs [--out-dir DIR] -> derived/main_case_bands.csv, components.csv, per_spec.csv,
 * summary.json, corrections.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const P = require("./package.cjs");
const Consumer = require(path.join(__dirname, "..", "main_case_candidate_v4_2026_09_29", "consumer.cjs"));
const { Engine, MODEL, FISCAL, HERE, ALLOCS, METHODS, CAP, PARTS, PROFILES, MAIN_PROFILE, LR_LINES, RENTAL, RATES, ENTERPRISES,
  ENTERPRISES_ALLOWED, ENTERPRISE_LINE, V4PKG: V4, gateState, gate, near, f2, csvRows, readJson, withCentral, specsFor, modelFor,
  evaluateFull, evalPackage, central, correctionsPayload, populationShare } = P;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const CAND = "main_case_candidate_v4_2026_09_29";
const SEPT27 = "main_case_long_run_2026_09_27";
const SCHOOLS = "main_case_schools_full_2026_09_26";
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const ex = (x) => x.toExponential(1);
const fx = (x) => x.toFixed(4);
const pair = (f) => [f(0), f(1)];

const MODELS = METHODS.map((m) => modelFor("central", m, withCentral({})));
const MODELS_LANE = METHODS.map((m) => modelFor("central", m, withCentral({ enterprise_rekey: false })));
const runs = (specs, profile, models) => (models || MODELS).map((model) => specs.map((spec) => evaluateFull(model, spec, profile)));
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

const cand = readJson(`${CAND}/derived/summary.json`);
const candBands = csvRows(`${CAND}/derived/bands.csv`);
const candText = fs.readFileSync(path.join(FISCAL, CAND, "derived", "corrections_v4.json"), "utf8");
const candPayload = JSON.parse(candText);
const cashPayload = readJson(`${CAND}/derived/corrections_v4_cash.json`);
const s27 = readJson(`${SEPT27}/derived/summary.json`);
const payload27 = readJson(`${SEPT27}/derived/corrections.json`);
const schools = readJson(`${SCHOOLS}/derived/summary.json`);
const schoolsRows = csvRows(`${SCHOOLS}/derived/main_case_bands.csv`);
const CAPDIR = "capital_return_services_2026_09_27/derived";
const capGaps = csvRows(`${CAPDIR}/gaps.csv`);
const P27 = P.forPayload(payload27);
const PC = P.forPayload(cashPayload);
const COMPONENTS = P.componentsFor(null);

// ---------------------------------------------------------------------------------------------------
console.log("[G1: candidate v4's bands]");
const specs = P.MAIN_SPECS;
const newRuns = runs(specs);
const newCosts = costsOf(newRuns);
const newEnds = ends(newCosts);
const C = central({});
const CB = cand.bands;
const ownBands = (cm) => cm.map((xs) => [Math.min(...xs), Math.max(...xs)]);
const printed = (caseName) => { const r = candBands.find((x) => x.case === caseName && x.method === "mean"); return [r.spec48_bn, r.spec11_bn]; };
function bandGates(name, band, cm, endIdx, want, print) {
  gate(`${name}: the two methods' mean is candidate v4's (summary.json bands.${want === CB.set ? "set" : "cash"}, 1e-9) and prints as its bands.csv (${print.join(" / ")})`,
    [0, 1].every((e) => near(band[e], want.at_48_11_bn[e], 1e-9) && near(band[e], want.own_band_bn[e], 1e-9) && fx(band[e]) === print[e]), f2(band));
  gate(`${name}: each method's band is the candidate's (1e-9), at the end specifications 48 / 11 in both methods`,
    endIdx.every((e) => e[0] === 48 && e[1] === 11) && METHODS.every((m, k) => [0, 1].every((e) => near(ownBands(cm)[k][e], want.by_method[m][e], 1e-9))),
    METHODS.map((m, k) => `${m} ${f2(ownBands(cm)[k])}`).join("; "));
}
bandGates("the set", C, newCosts, newEnds, CB.set, printed("set"));
const CASH_O = { pension4: "cash" };
const cashCosts = costsOf(runs(specsFor(CASH_O), MAIN_PROFILE, METHODS.map((m) => modelFor("central", m, withCentral(CASH_O)))));
const cashEnds = ends(cashCosts);
const Ccash = central(CASH_O);
bandGates("the cash set", Ccash, cashCosts, cashEnds, CB.cash, printed("cash"));
gate("the cash set's payload (corrections_v4_cash.json) builds the same package band as the pension switch off", near(PC.central({})[0], Ccash[0], 1e-12)
  && near(PC.central({})[1], Ccash[1], 1e-12), f2(PC.central({})));
const methodMean = (cm) => specs.map((_, i) => mean(cm.map((xs) => xs[i])));
const meanSet = methodMean(newCosts), meanCash = methodMean(cashCosts);
const payloadCosts = specs.map((s) => evaluateFull(P.payloadModel(), s).cost_bn);
const cashPayloadCosts = PC.MAIN_SPECS.map((s) => PC.evaluateFull(PC.payloadModel(), s).cost_bn);
const pmGap = worst(payloadCosts.map((x, i) => x - meanSet[i])), pmcGap = worst(cashPayloadCosts.map((x, i) => x - meanCash[i]));
gate("the payload model (engine.js + model.json + corrections.json) gives the methods' mean at every specification, and the band (1e-9)",
  payloadCosts.length === 64 && pmGap < 1e-9 && near(Math.min(...payloadCosts), C[0], 1e-9) && near(Math.max(...payloadCosts), C[1], 1e-9), `max |diff| ${ex(pmGap)}`);
gate("the cash set's payload model gives the cash set's methods' mean at every specification, and its band (1e-9)",
  pmcGap < 1e-9 && near(Math.min(...cashPayloadCosts), Ccash[0], 1e-9) && near(Math.max(...cashPayloadCosts), Ccash[1], 1e-9), `max |diff| ${ex(pmcGap)}`);
const payload = correctionsPayload();
const independent = Consumer.evaluateAll(JSON.parse(JSON.stringify(payload)), { engine: Engine, model: MODEL });
const indGap = worst(independent.map((x, i) => x.cost_bn - meanSet[i]));
gate("consumer.cjs (engine.js, model.json and corrections.json, no package) gives the methods' mean at every specification (1e-9)",
  independent.length === 64 && independent.every((x, i) => ["allocation", "normalization", "share", "school", "gg", "uc", "reading"].every((f) => x.spec[f] === specs[i][f]))
  && indGap < 1e-9, `max |diff| ${ex(indGap)}`);
const specs4 = V4.specsFor(withCentral({}));
const candGap = worst(MODELS.flatMap((m, k) => specs4.map((s, i) => V4.evaluateFull(m, s).cost_bn - newCosts[k][i])));
gate("the package's evaluation equals candidate v4's package's at every specification, both methods (1e-12)", candGap < 1e-12, `max |diff| ${ex(candGap)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the payload and the specifications]");
const metaKeys = Object.keys(candPayload.meta);
const stampsChanged = P.STAMPED.filter((k) => payload.meta[k] !== candPayload.meta[k]);
gate(`corrections.json is the candidate's corrections_v4.json with the adoption stamps alone changed (meta ${P.STAMPED.join(", ")}); lines, receipt lines, edits and production grid identical`,
  JSON.stringify(Object.keys(payload)) === JSON.stringify(Object.keys(candPayload)) && JSON.stringify(Object.keys(payload.meta)) === JSON.stringify(metaKeys)
  && ["lines", "receipt_lines", "edits", "production"].every((k) => JSON.stringify(payload[k]) === JSON.stringify(candPayload[k]))
  && metaKeys.filter((k) => !P.STAMPED.includes(k)).every((k) => JSON.stringify(payload.meta[k]) === JSON.stringify(candPayload.meta[k]))
  && stampsChanged.length === P.STAMPED.length, `${payload.lines.length} lines, ${payload.receipt_lines.length} receipt lines, ${payload.edits.length} edits; changed ${stampsChanged.join(", ")}`);
gate(`meta: adopted ${P.ADOPTED}, decision ${P.DECISION}, no "not adopted" left in the case text`, payload.meta.adopted === P.ADOPTED
  && payload.meta.decision === P.DECISION && !/not adopted/.test(payload.meta.case) && !/not adopted/.test(payload.meta.status));
gate("RESPONSES is meta.responses and componentsFor(null) is meta.capital_return.components (deep-equal, key order)",
  JSON.stringify(P.RESPONSES) === JSON.stringify(payload.meta.responses) && JSON.stringify(COMPONENTS) === JSON.stringify(payload.meta.capital_return.components));
const P24_FIELDS = Object.keys(P.P24.MAIN_SPECS[0]);
const EXTRA = ["reading", "rate", "long_run", "enterprises", "line_responses"];
gate("the specifications carry only the September 24 fields and reading, rate, long_run, enterprises and line_responses (uncertainty_propagation_2026_09_22/sept24_specs.cjs:104), in the September 27 order",
  specs.every((s) => Object.keys(s).every((k) => P24_FIELDS.includes(k) || EXTRA.includes(k)))
  && JSON.stringify(Object.keys(specs[0])) === JSON.stringify(Object.keys(P27.MAIN_SPECS[0])), Object.keys(specs[0]).join(" "));
gate("reading is low exactly where general government takes its low response; the rate follows the reading (2% low, 3% high)",
  specs.every((s) => (s.reading === "low") === (s.gg === P.RESPONSES.general_government.low) && s.rate === RATES[s.reading]),
  `${specs.filter((s) => s.reading === "low").length} low of 64`);
const lrKeys = Object.keys(P.LINE_RESPONSES);
gate(`each specification's line responses are meta.responses at its reading: ${lrKeys.length} entries, in meta's order`,
  specs.every((s) => JSON.stringify(Object.keys(s.line_responses)) === JSON.stringify(lrKeys) && lrKeys.every((k) => s.line_responses[k] === P.LINE_RESPONSES[k][s.reading])),
  lrKeys.join(" "));
gate("the specifications are the September 27 case's but for the line responses the payload adds (every other field identical)",
  specs.every((s, i) => Object.keys(s).every((k) => k === "line_responses" || s[k] === P27.MAIN_SPECS[i][k])
    && Object.keys(P27.MAIN_SPECS[i].line_responses).every((k) => s.line_responses[k] === P27.MAIN_SPECS[i].line_responses[k])));

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
gate("main profile: every correction line responds as the specification sets it and the road lines as their subfunctions (sl_highways, fed_highways)",
  every(newRuns, (r, s) => P.PAYLOAD_LINES.filter((l) => P.PARENT[l.id]).every((l) => responseOf(r.evaluation, l.id) === s.line_responses[l.id])
    && COMPONENTS.filter((c) => c.key.kind === "part_rekeyed").every((c) => s.line_responses[c.key.correction_line] === P.subfunctionResponses(s.long_run, s.reading)[c.response.subfunction])));
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
console.log("\n[history: the September 27 lane's rows, re-derived through this package on its payload]");
const OLD = { long_run: false, rental: 0, capital: false, enterprise_receipt: 0 };
const hist = {
  main_case: [s27.main_case, P27.central({})],
  first_year_response: [s27.first_year_response, P27.central(Object.assign({}, OLD, { school_rule: "one_year" }))],
  long_run_responses_alone: [s27.each_addition.long_run_responses_alone, P27.central({ rental: 0, capital: false, enterprise_receipt: 0 })],
  rental_assistance_alone: [s27.each_addition.rental_assistance_alone, P27.central({ long_run: false, capital: false, enterprise_receipt: 0 })],
  long_run_responses_and_capital_return_option_a: [s27.each_addition.long_run_responses_and_capital_return_option_a, P27.central({ rental: 0, enterprises: "A" })],
};
for (const [k, [want, got]] of Object.entries(hist)) {
  gate(`${k}: the September 27 lane's value (summary.json) re-derives exactly`, got[0] === want[0] && got[1] === want[1], f2(want));
}
const bands27 = csvRows(`${SEPT27}/derived/main_case_bands.csv`);
const row27 = (profile, variant) => bands27.find((r) => r.profile === profile && r.variant === variant);
gate("the September 27 lane's band rows print its summary.json values (first_year_response, schools_case, adopted and the three additions)",
  [["first_year_response", s27.first_year_response], ["schools_case", s27.schools_case], ["adopted", s27.main_case],
    ["long_run_responses_alone", hist.long_run_responses_alone[0]], ["rental_assistance_alone", hist.rental_assistance_alone[0]],
    ["long_run_responses_and_capital_return_option_a", hist.long_run_responses_and_capital_return_option_a[0]]]
    .every(([v, b]) => { const r = row27(MAIN_PROFILE, v); return r && r.cost_low_bn === fx(b[0]) && r.cost_high_bn === fx(b[1]); }));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: v4's items, from the September 27 case]");
const OFF = V4.OFF;
const ITEMS = V4.SET_ITEMS;
// A case's cost at this case's end specifications (each method's), averaged over the methods.
function endCosts(o) {
  const oo = withCentral(o), sp = specsFor(oo);
  const per = METHODS.map((meth, k) => { const m = modelFor("central", meth, oo); return newEnds[k].map((i) => evaluateFull(m, sp[i], oo.profile).cost_bn); });
  return [0, 1].map((e) => mean(per.map((x) => x[e])));
}
const cumulative = [OFF].concat(ITEMS.map((_, k) => Object.assign({}, OFF, ...ITEMS.slice(0, k + 1).map((it) => it.o))));
const cumCosts = cumulative.map(endCosts);
const steps = ITEMS.map((it, k) => [cumCosts[k + 1][0] - cumCosts[k][0], cumCosts[k + 1][1] - cumCosts[k][1]]);
const totalMove = [cumCosts[ITEMS.length][0] - cumCosts[0][0], cumCosts[ITEMS.length][1] - cumCosts[0][1]];
gate("with every item off the package is the September 27 case at these end specifications (its main_case, 1e-9)",
  near(cumCosts[0][0], s27.main_case[0], 1e-9) && near(cumCosts[0][1], s27.main_case[1], 1e-9), f2(cumCosts[0]));
gate("with every item on it is this case (1e-9)", near(cumCosts[ITEMS.length][0], C[0], 1e-9) && near(cumCosts[ITEMS.length][1], C[1], 1e-9), f2(cumCosts[ITEMS.length]));
const stepSum = steps.reduce((a, s) => [a[0] + s[0], a[1] + s[1]], [0, 0]);
gate("the items, added in the brief's order, add to the change from the September 27 case (1e-9), which is the band move (same ends)",
  near(stepSum[0], totalMove[0], 1e-9) && near(stepSum[1], totalMove[1], 1e-9) && near(totalMove[0], C[0] - s27.main_case[0], 1e-9)
  && near(totalMove[1], C[1] - s27.main_case[1], 1e-9), f2(totalMove));
const alone = ITEMS.map((it) => { const c = endCosts(Object.assign({}, OFF, it.o)); return [c[0] - cumCosts[0][0], c[1] - cumCosts[0][1]]; });
const aloneGap = worst(ITEMS.flatMap((it, k) => { const a = cand.attribution.items.find((x) => x.id === it.id); return a ? [alone[k][0] - a.alone[0], alone[k][1] - a.alone[1]] : [Infinity]; }));
gate("each item alone at the end specifications is the candidate's attribution (summary.json attribution.items alone, 1e-9)", aloneGap < 1e-9, `max |diff| ${ex(aloneGap)}`);
const itemKey = (it) => `item_${it.id}`;
const eachItem = Object.fromEntries(ITEMS.map((it) => [itemKey(it), central(Object.assign({}, OFF, it.o))]));

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
const n27 = s27.components.length;
gate(`the range's first ${n27} components are the September 27 case's (names, labels, variants; candidate v2's descriptors of its main_case.cjs)`,
  RANGE.slice(0, n27).every((c, k) => c.name === s27.components[k].name && c.label === s27.components[k].label
    && JSON.stringify(c.variants.map((v) => v.v).sort()) === JSON.stringify(Object.keys(s27.components[k].variants).sort())), `${RANGE.length} components in all`);
const skipped = [];
for (const comp of RANGE) {
  const variants = comp.variants.map((v) => ({ v, o: typeof v.o === "function" ? v.o(base) : v.o }));
  if (variants.every((x) => !Object.keys(x.o).length && x.v.caseName === "central" && x.v.methods.length === METHODS.length)) { skipped.push(comp.name); continue; }
  component(comp.name, comp.label, variants.map(({ v, o }) => {
    const bs = v.methods.map((meth) => evalPackage(v.caseName, meth, o));
    return [v.v, [mean(bs.map((b) => b[0])), mean(bs.map((b) => b[1]))]];
  }));
}
gate(`every range component moves the case, but ${skipped.join(", ") || "none"} (an item beside the case)`, JSON.stringify(skipped) === JSON.stringify(["transit_key"])
  && components.length === RANGE.length - 1);
const sumLo = components.reduce((s, x) => [s[0] + x.lo[0], s[1] + x.lo[1]], [0, 0]);
const sumHi = components.reduce((s, x) => [s[0] + x.hi[0], s[1] + x.hi[1]], [0, 0]);
const rangeLowEnd = [C[0] + sumLo[0], C[0] + sumHi[0]], rangeHighEnd = [C[1] + sumLo[1], C[1] + sumHi[1]];
const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
const quadrature = [C[0] - rss(components.map((x) => x.lo[0])), C[1] + rss(components.map((x) => x.hi[1]))];

// ---------------------------------------------------------------------------------------------------
console.log("\n[variants]");
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
const schoolsRow = (profile, variant) => {
  const r = schoolsRows.find((x) => x.profile === profile && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] the schools case's bands lack ${profile}/${variant}`);
  return [Number(r.cost_low_bn), Number(r.cost_high_bn)];
};
const otherProfiles = {};
for (const pf of Object.keys(PROFILES).filter((x) => x !== MAIN_PROFILE)) {
  otherProfiles[pf] = { schools_case: schoolsRow(PROFILES[pf].base, "adopted"), uncorrected_at_adopted_responses: P.band(MODEL, pf), adopted: central({ profile: pf }) };
}
gate("the other profiles' schools_case values are the September 27 lane's", Object.keys(otherProfiles).every((pf) =>
  JSON.stringify(otherProfiles[pf].schools_case) === JSON.stringify(s27.other_profiles[pf].schools_case)));
const oldProfile = { profile: "cbo_category_lag_non_school_full", schools_case: schools.main_case,
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
const k12Diff = atEnds(newEnds, (m, i) => byId(pupilRuns[m][i], "k12") - byId(newRuns[m][i], "k12"));
const k12Keys = atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.find((c) => c.id === "k12").key);
gate("with the pupil share the case differs by the K-12 difference alone", worst(pupilRuns.flatMap((xs, m) => xs.map((r, i) =>
  r.cost_bn - newCosts[m][i] - (byId(r, "k12") - byId(newRuns[m][i], "k12"))))) < 1e-9, "every specification");
const at7 = central({ rates: { low: RATES.reported, high: RATES.reported } });
const runs7 = runs(specsFor({ rates: { low: RATES.reported, high: RATES.reported } }));
const beside8 = V4.BESIDE_ITEMS.find((it) => it.id === "8"), beside10 = V4.BESIDE_ITEMS.find((it) => it.id === "10");
const with8 = central(beside8.o), with10 = central(beside10.o);
const withRuns = (o) => runs(specsFor(o), MAIN_PROFILE, METHODS.map((m) => modelFor("central", m, withCentral(o))));
const runs8 = withRuns(beside8.o), runs10 = withRuns(beside10.o);
gate("items 8 and 10 beside the case give the candidate's set_plus_8 and set_plus_10 bands (1e-9)", [[with8, CB.set_plus_8], [with10, CB.set_plus_10]]
  .every(([b, w]) => near(b[0], w.at_48_11_bn[0], 1e-9) && near(b[1], w.at_48_11_bn[1], 1e-9)), `${f2(with8)}; ${f2(with10)}`);
// The payload-first evaluation against candidate v4's package, variant by variant: every range variant and every
// main-profile variant row (candidate v4's package blocks the other profiles).
const v4Band = (o, caseName, methods) => { const bs = (methods || METHODS).map((meth) => V4.evalPackage(caseName || "central", meth, o));
  return [mean(bs.map((b) => b[0])), mean(bs.map((b) => b[1]))]; };
const checks = [["without_capital_return", withoutCapital, { capital: false }], ["enterprises_out_option_a", optionA, { enterprises: "A" }],
  ["enterprise_receipt_at_model_json_share", atModelShare, { enterprise_rekey: false }], ["capital_return_at_7pct", at7, { rates: { low: RATES.reported, high: RATES.reported } }],
  ["rental_assistance_at_0", rentalAt0, { rental: 0 }], ["k12_capital_at_pupil_share", k12Pupil, { capital_variant: "k12_at_pupil_share" }],
  ["audit_row3_instead_of_cbo_income_tax", withRow3, { incomeTax: "row3", tax_key: "cbo_2022" }], ["school_within_district", schoolLow, { school_rule: "within_district" }],
  ["school_within_district_as_response", schoolLowAsResponse, { school_rule: "within_district_as_response" }], ["cash_set", Ccash, CASH_O]]
  .map(([name, b, o]) => [name, b, v4Band(o)]).concat([["no_fill_in_correction", noFillIn, V4.evalPackage("central", "audit_rules_alone", {})]])
  .concat(components.flatMap((x) => x.devs.map((d) => {
    const comp = RANGE.find((c) => c.name === x.name), v = comp.variants.find((y) => y.v === d.v);
    return [`${x.name}/${d.v}`, [C[0] + d.d[0], C[1] + d.d[1]], v4Band(typeof v.o === "function" ? v.o(base) : v.o, v.caseName, v.methods)];
  })));
const v4Gap = worst(checks.flatMap(([, b, w]) => [b[0] - w[0], b[1] - w[1]]));
gate("every variant row and range variant equals candidate v4's package's band (1e-9): the payload-first evaluation is the candidate's under every option",
  v4Gap < 1e-9, `${checks.length} bands, max |diff| ${ex(v4Gap)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the uncorrected model at the adopted responses]");
// model.json has none of the payload's lines. withSyntheticLines adds them at zero, so every line a specification names
// is on the model in every profile, and the engine run a consumer makes itself is evaluateFull's. (On the September 27
// payload the uncorrected rows are that lane's: generality.cjs reproduces its files byte for byte.)
const MODEL_SYN = P.withSyntheticLines(MODEL);
const addedLines = (side) => MODEL_SYN[side].lines.slice(MODEL[side].lines.length);
const zeroCells = (cells) => Object.values(cells).every((c) => ALLOCS.every((a) => c[a].target_bn === 0 && c[a].other_bn === 0 && c[a].share === 0));
gate("withSyntheticLines(model.json) appends the payload's 8 spending lines and 2 receipt lines at zero (national, amounts and shares 0) and leaves the rest of the model as it was",
  JSON.stringify(addedLines("spending").map((l) => l.id)) === JSON.stringify(P.PAYLOAD_LINES.map((l) => l.id))
  && JSON.stringify(addedLines("receipts").map((l) => l.id)) === JSON.stringify(P.PAYLOAD_RECEIPT_LINES)
  && addedLines("spending").every((l) => l.national_bn === 0 && zeroCells(l.keys)) && addedLines("receipts").every((l) => l.national_bn === 0 && zeroCells(l.cells))
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
// An independent route: consumer.cjs (engine.js and a payload, no package) with the payload's lines at zero, no edits,
// no production grid and the case's meta: model.json with nothing moved, at the case's responses and capital rules.
const zeroPayload = { lines: payload.lines, edits: [], meta: payload.meta,
  receipt_lines: payload.receipt_lines.map((l) => Object.assign({}, l, { national_bn: 0, cells: Object.fromEntries(Object.entries(l.cells)
    .map(([sc, c]) => [sc, Object.fromEntries(ALLOCS.map((a) => [a, Object.assign({}, c[a], { target_bn: 0, other_bn: 0, share: 0 })]))])) })) };
const ucIndependent = Consumer.evaluateAll(JSON.parse(JSON.stringify(zeroPayload)), { engine: Engine, model: MODEL });
const ucPackage = specs.map((s) => evaluateFull(MODEL, s).cost_bn);
const ucGap = worst(ucIndependent.map((x, i) => x.cost_bn - ucPackage[i]));
gate("consumer.cjs on model.json with the payload's lines at zero gives the package's uncorrected cost at every specification (1e-9), and its span is uncorrected_at_adopted_responses",
  ucIndependent.length === specs.length && ucIndependent.every((x, i) => ["allocation", "normalization", "share", "school", "gg", "uc", "reading"].every((f) => x.spec[f] === specs[i][f]))
  && ucGap < 1e-9 && near(Math.min(...ucPackage), uncorrectedAtResponses[0], 1e-9) && near(Math.max(...ucPackage), uncorrectedAtResponses[1], 1e-9),
  `max |diff| ${ex(ucGap)}; ${f2(uncorrectedAtResponses)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the enterprises, the re-key and the land rows]");
const SHARE = populationShare(MODELS[0]).personal;
const payloadModel = P.payloadModel();
gate("the corrected population share is one number in both methods, both allocations and the payload model",
  [...MODELS, payloadModel].every((m) => ALLOCS.every((a) => near(populationShare(m)[a], SHARE, 1e-14))), String(SHARE));
gate(`option ${ENTERPRISES}: the enterprise receipt and public housing's deficit respond at 1, every enterprise component at 1, keyed at the corrected share but public housing's capital (the rental line's key)`,
  newRuns.every((xs) => xs.every((r) => esRow(r).response === 1 && P.ENTERPRISE_SPLITS.every((id) => receiptOf(r, id).response === 1)
    && r.capital.components.filter((c) => c.group === "enterprise").every((c) => c.response === 1
      && (c.id === "ent_housing_sl" ? near(c.key, amount(r.evaluation, RENTAL) / national(r.evaluation, RENTAL), 1e-15) : near(c.key, SHARE, 1e-15))))),
  "every specification, both methods");
const laneShareRuns = runs(specs, MAIN_PROFILE, MODELS_LANE);
const rekeyEffect = atEnds(newEnds, (m, i) => newCosts[m][i] - laneShareRuns[m][i].cost_bn);
const publicHousing = atEnds(newEnds, (m, i) => byId(newRuns[m][i], "ent_housing_sl"));
const es27 = s27.enterprises.receipt_at_end_specifications;
const schoolsEs = [0, 1].map((e) => es27.group_amount_bn[e] - es27.move_from_the_schools_case_bn[e]);
const esAmount = atEnds(newEnds, (m, i) => esRow(newRuns[m][i]).amount_bn);
const esNat = payloadModel.receipts.lines.find((l) => l.id === ENTERPRISE_LINE).national_bn;
const esModel = MODEL.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
const kc = readJson(`${CAPDIR}/summary.json`).enterprises.key_consistency;
// The receipt's move from the schools case: the re-key (national x (corrected - model.json's share)) and item 1's split.
const moveRekey = [0, 1].map(() => esNat * (SHARE - kc.receipt_key[0]));
const moveSplit = [0, 1].map(() => (esNat - esModel.national_bn) * kc.receipt_key[0]);
const receiptMove = [0, 1].map((e) => esAmount[e] - schoolsEs[e]);
gate("the enterprise receipt's move from the schools case is the re-key at the corrected share plus item 1's split of public housing (1e-9)",
  [0, 1].every((e) => near(receiptMove[e], moveRekey[e] + moveSplit[e], 1e-9)) && near(esNat, esModel.national_bn - V4.HOUSING_SURPLUS, 1e-9),
  `${fx(receiptMove[0])} = re-key ${fx(moveRekey[0])} + split ${fx(moveSplit[0])}`);
// Land: the capital lane's conversion per 10% of land-to-structure value, priced at this case's keys and responses.
const LAND_ROW = /^((block|enterprise): )?land at 10% of the structures charged: (\S+)$/;
const landRows = capGaps.filter((r) => LAND_ROW.test(r.item));
const landPart = (r) => r.item.match(LAND_ROW)[2] || "core";
const landStock = Object.fromEntries(landRows.map((r) => [r.item.match(LAND_ROW)[3], Number(r.national_base_bn) * Number(r.fee_factor)]));
gate("gaps.csv has one land row for every capital component of the payload, under its part", landRows.length === COMPONENTS.length
  && COMPONENTS.every((c) => landRows.some((r) => r.item.match(LAND_ROW)[3] === c.id && landPart(r) === c.part)), `${landRows.length} rows`);
const landAt = (rs, m, i, pred) => rs[m][i].capital.components.filter(pred).reduce((a, c) => a + landStock[c.id] * specs[i].rate * c.key * c.response, 0);
const land = {
  per_10pct_bn: atEnds(newEnds, (m, i) => landAt(newRuns, m, i, () => true)),
  by_part_per_10pct_bn: Object.fromEntries(PARTS.map((g) => [g, atEnds(newEnds, (m, i) => landAt(newRuns, m, i, (c) => c.group === g))])),
  note: "[GAP] BEA measures produced assets only; the capital lane's conversion per 10% of land-to-structure value (gaps.csv core, block and enterprise rows), priced at this case's keys and responses at the end specifications (2% low, 3% high; highways at the road key, public housing at the rental line's key, the other enterprise land at the corrected population share); not an estimate" };
const rentalKey = atEnds(newEnds, (m, i) => amount(newRuns[m][i].evaluation, RENTAL) / national(newRuns[m][i].evaluation, RENTAL));
const rentalNational = national(newRuns[0][0].evaluation, RENTAL);
const overlap = { rental_key: rentalKey, population_share: SHARE, rental_national_bn: rentalNational,
  upper_bound_bn: rentalKey.map((k) => rentalNational * (SHARE - k)),
  netted_bn: 0,
  note: "item 1 consolidates public housing's federal operating subsidy ($5.258bn, HUD FY2024) out of both legs and keys public housing's deficit (housing_enterprise_surplus) by the rental line's key, so that transfer no longer meets two keys. Other federal payments to housing authorities stay in housing_subsidies at the rental key and, under option D, inside the rest of the enterprise surplus at the population share: upper_bound_bn if all of the line went to enterprises. Not netted." };
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
const groupReceipts = Object.assign({}, s27.group_receipts_bn, { adopted: receiptsTotal(payloadModel), adopted_2026_09_27: s27.group_receipts_bn.adopted });

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
    note: "the case keys K-12 by the account's school key from the evaluation; the capital lane's variant k12_at_pupil_share uses the pupil share, which is higher, so the return is higher by pupil_share_minus_account_bn at the end specifications" },
};
fs.mkdirSync(OUT, { recursive: true });
const row = (pf, variant, b, r) => [pf, variant, fx(b[0]), fx(b[1]), r ? fx(r[0]) : "", r ? fx(r[1]) : ""].join(",");
const bandsCsv = ["profile,variant,cost_low_bn,cost_high_bn,range_low_bn,range_high_bn",
  row(MAIN_PROFILE, "first_year_response", s27.first_year_response),
  row(MAIN_PROFILE, "schools_case", schools.main_case, [schools.range.low_end[0], schools.range.high_end[1]]),
  row(MAIN_PROFILE, "sept27_case", s27.main_case, [s27.range.low_end[0], s27.range.high_end[1]]),
  row(MAIN_PROFILE, "uncorrected_at_adopted_responses", uncorrectedAtResponses),
  row(MAIN_PROFILE, "long_run_responses_alone", s27.each_addition.long_run_responses_alone),
  row(MAIN_PROFILE, "rental_assistance_alone", s27.each_addition.rental_assistance_alone),
  row(MAIN_PROFILE, "long_run_responses_and_capital_return_option_a", s27.each_addition.long_run_responses_and_capital_return_option_a),
  row(MAIN_PROFILE, "without_capital_return", withoutCapital),
  row(MAIN_PROFILE, "school_within_district", schoolLow),
  row(MAIN_PROFILE, "school_within_district_as_response", schoolLowAsResponse),
  row(MAIN_PROFILE, "adopted", C, [rangeLowEnd[0], rangeHighEnd[1]]),
  row(MAIN_PROFILE, "cash_set", Ccash),
  row(MAIN_PROFILE, "enterprises_out_option_a", optionA),
  row(MAIN_PROFILE, "enterprise_receipt_at_model_json_share", atModelShare),
  row(MAIN_PROFILE, "capital_return_at_7pct", at7),
  row(MAIN_PROFILE, "rental_assistance_at_0", rentalAt0),
  row(MAIN_PROFILE, "general_government_fixed", ggFixed),
  row(MAIN_PROFILE, "k12_capital_at_pupil_share", k12Pupil),
  row(MAIN_PROFILE, "audit_row3_instead_of_cbo_income_tax", withRow3),
  row(MAIN_PROFILE, "no_fill_in_correction", noFillIn),
  row(oldProfile.profile, "schools_case", oldProfile.schools_case),
  row(oldProfile.profile, "with_rental_assistance_capital_and_enterprises", oldProfile.with_rental_assistance_capital_and_enterprises)]
  .concat(Object.entries(otherProfiles).flatMap(([pf, v]) => [row(pf, "schools_case", v.schools_case),
    row(pf, "uncorrected_at_adopted_responses", v.uncorrected_at_adopted_responses), row(pf, "adopted", v.adopted)]));
const compCsv = ["component,label,range_dev_low_end_lo,range_dev_low_end_hi,range_dev_high_end_lo,range_dev_high_end_hi"]
  .concat(components.map((x) => [x.name, `"${x.label}"`, fx(x.lo[0]), fx(x.hi[0]), fx(x.lo[1]), fx(x.hi[1])].join(",")));
const perHead = ["method", "spec", "allocation", "normalization", "share", "school", "gg", "uc", "justice", "reading", "rate", "enterprises",
  "cost_bn", "engine_cost_bn", "capital_total_bn", "capital_state_local_bn", "capital_federal_bn",
  "capital_core_bn", "capital_block_bn", "capital_enterprise_bn",
  "response_receipt_enterprise_surplus", "group_enterprise_surplus_bn", "enterprise_surplus_receipt_cost_bn"]
  .concat(COMPONENTS.map((c) => `capital_${c.id}_bn`))
  .concat(LR_LINES.concat([RENTAL]).flatMap((id) => [`response_${id}`, `group_${id}_bn`]));
const perSpec = [perHead.join(",")].concat(METHODS.flatMap((meth, m) => specs.map((s, i) => {
  const r = newRuns[m][i];
  return [meth, i, s.allocation, s.normalization, s.share, s.school, s.gg, s.uc, s.justice, s.reading, s.rate, s.enterprises,
    r.cost_bn, -r.evaluation.welfare_bn, r.capital.total_bn,
    capitalWhere(r, (c) => c.level === "state_local"), capitalWhere(r, (c) => c.level === "federal"),
    capitalGroup(r, "core"), capitalGroup(r, "block"), capitalGroup(r, "enterprise"), esRow(r).response, esRow(r).amount_bn, esCost(r)]
    .concat(COMPONENTS.map((c) => byId(r, c.id)))
    .concat(LR_LINES.concat([RENTAL]).flatMap((id) => [responseOf(r.evaluation, id), amount(r.evaluation, id)])).map(full).join(",");
})));
const stepsObj = Object.fromEntries(ITEMS.map((it, k) => [itemKey(it), steps[k]]));
const summary = {
  lane: P.LANE,
  decision: P.DECISION,
  adopted_2026_09_23: s27.adopted_2026_09_23, adopted_2026_09_24: s27.adopted_2026_09_24,
  adopted_2026_09_26: s27.adopted_2026_09_26, adopted_2026_09_26_schools: s27.adopted_2026_09_26_schools,
  adopted_2026_09_27: s27.main_case,
  first_year_response: s27.first_year_response, schools_case: s27.schools_case,
  uncorrected_at_adopted_responses: uncorrectedAtResponses, without_capital_return: withoutCapital,
  main_case: C,
  cash_set: { band_bn: Ccash, by_method_bn: Object.fromEntries(METHODS.map((m, k) => [m, ownBands(cashCosts)[k]])), end_specifications: cashEnds,
    change_from_main_case_bn: [Ccash[0] - C[0], Ccash[1] - C[1]],
    note: "the set with the pension switch off (pension4 \"cash\"): social security and Medicare's Part A at the group's current benefits instead of the accrual at payable benefits net of the tax on benefits; the payload is main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json" },
  change: [C[0] - s27.main_case[0], C[1] - s27.main_case[1]],
  change_at_fixed_specifications: Object.assign({}, stepsObj, {
    total: totalMove,
    note: `the change from the September 27 case at each method's end specifications (48 low, 11 high in both), averaged, by v4 item added in the brief's order (${ITEMS.map((it) => it.id).join(", ")}): each part is the case with that item and the ones before it less the case with the ones before it (package.cjs options over candidate v4's OFF). The parts add to total, which is change because the ends do not move. Each item alone is in each_addition; the items' interactions are in the candidate lane (derived/attribution.csv). sept27_case holds the September 27 case's own change from the schools case, by its additions` ,
    sept27_case: s27.change_at_fixed_specifications }),
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
    capital_lane_rows_before_rental_assistance: s27.enterprises.capital_lane_rows_before_rental_assistance,
    overlap_with_rental_assistance: overlap,
    interest: s27.enterprises.interest,
    proportional_reference: "the receipt, public housing's deficit and every enterprise component respond at 1 in every profile, the proportional reference included",
    public_housing: "item 1 splits public housing's deficit (NIPA 3.8 line 13, -$40.298bn national, less the $5.258bn operating subsidy) out of the enterprise line into its own receipt, housing_enterprise_surplus, at the rental line's key; item 4 keys public housing's capital (ent_housing_sl) the same way. The enterprise line's national is national_bn; move_from_the_schools_case_bn is the re-key plus that split" },
  school: { rules: P.RULES, within_district: schoolLow, within_district_as_response: schoolLowAsResponse,
    end_specifications: { average: newEnds, within_district: schoolLowEnds.ends, within_district_as_response: schoolLowAsResponseEnds.ends },
    note: "the schools case's low side on this case: every specification re-run with that school rule (the K-12 capital return follows the school response); end_specifications are [low end, high end] per fill-in method",
    sign_break_even: "derived/sign_reversal.csv (sign_reversal.cjs): schools move with the common share" },
  rental_assistance: { group_amount_by_method_bn: Object.fromEntries(METHODS.map((m, k) => [m, Object.fromEntries(ALLOCS.map((a, j) => [a, rentalAmount[k][j]]))])),
    uncorrected_group_amount_bn: Object.fromEntries(ALLOCS.map((a, j) => [a, rentalUncorrected[j]])),
    note: `the corrections re-key the line (tax-records stack and administrative benefit keys) and item 1 takes public housing's operating subsidy out of it (national ${MODEL.spending.lines.find((l) => l.id === RENTAL).national_bn} to ${rentalNational}), so the move is the corrected amount, not the uncorrected $${rentalUncorrected[0].toFixed(2)}bn`,
    overlap_netted_bn: 0 },
  responses: P.RESPONSES,
  range: { low_end: rangeLowEnd, high_end: rangeHighEnd, overall: [rangeLowEnd[0], rangeHighEnd[1]], quadrature,
    note: `every component re-runs the whole case at every specification; the band's ends are minima and maxima over the specifications; option A, 7% and items 8 and 10 are beside the range, not in it. The components are the September 27 case's and candidate v3's item ranges for items 5 and 6a; ${skipped.join(", ")} moves nothing (item 8 is beside the case); v4's items 7, pension, state and roads carry no range component` },
  other_profiles: otherProfiles, old_main_profile: oldProfile,
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn,
  each_addition: Object.assign({}, s27.each_addition, eachItem),
  beside_the_account: {
    rate_7pct: { band_bn: at7, return_at_end_specifications_bn: atEnds(newEnds, (m, i) => runs7[m][i].capital.total_bn),
      note: "A-4 (2003)'s private-capital rate on every component, enterprises included, reported beside the account only (operator, 2026-09-27 15:21 JST)" },
    land_per_10pct_of_land_to_structure_value: land,
    enterprises_out_option_A: { band_bn: optionA, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => optionARuns[m][i].cost_bn - newCosts[m][i]),
      note: "option A, a labelled variant beside the range: no enterprise capital, and the enterprise_surplus receipt and public housing's deficit at 0; everything else as the case" },
    rental_assistance_at_0: { band_bn: rentalAt0, note: "rental assistance at 0 on this case; public housing's deficit and capital stay (enterprises under option D)" },
    congestion: Object.assign({}, s27.beside_the_account.congestion, { not_recomputed: "the September 27 figure (the payload's meta.candidate_v4.not_recomputed): derived with roads on economic_affairs_services' key, before v4 keyed roads by vehicle miles" }),
    transit_at_riders_key_item_8: { band_bn: with8, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => runs8[m][i].cost_bn - newCosts[m][i]),
      options: beside8.o, note: `${beside8.name}: beside the case (candidate v4's BESIDE_ITEMS), not in it` },
    uninsured_use_0_7x_item_10: { band_bn: with10, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => runs10[m][i].cost_bn - newCosts[m][i]),
      options: beside10.o, note: `${beside10.name}: beside the case (candidate v4's BESIDE_ITEMS), not in it` },
  },
  by_side_vs_uncorrected_at_adopted_responses: sides,
  group_receipts_bn: groupReceipts,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi, variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
  v4: {
    adopted: "2026-09-29 15:12 JST, the operator (\"1 ok do\"), through the parent's brief",
    candidate_lane: CAND,
    items: ITEMS.map((it) => ({ id: it.id, name: it.name, options: it.o })),
    beside_items: V4.BESIDE_ITEMS.map((it) => ({ id: it.id, name: it.name, options: it.o })),
    rules: V4.RULES,
    payload: { file: "derived/corrections.json", from: `${CAND}/derived/corrections_v4.json`, from_sha256: sha256(`${CAND}/derived/corrections_v4.json`),
      stamped: P.STAMPED, builder: `${CAND}/payload.cjs build()` },
    correction_lines: Object.fromEntries(Object.entries(P.PARENT).map(([id, parent]) => [id, { parent, follows_long_run_profiles: FOLLOW.includes(id) }])),
    enterprise_splits: P.ENTERPRISE_SPLITS,
    items_alone_at_fixed_specifications_bn: Object.fromEntries(ITEMS.map((it, k) => [itemKey(it), alone[k]])),
    history: "first_year_response, schools_case, adopted_2026_09_2x, each_addition's September 27 entries, change_at_fixed_specifications.sept27_case, enterprises.capital_lane_rows_before_rental_assistance and beside_the_account.congestion are the September 27 lane's values (its summary.json), re-derived through this package on its payload where they are bands",
    range_components_skipped: skipped,
    inputs: Object.fromEntries([`${CAND}/derived/summary.json`, `${CAND}/derived/bands.csv`, `${CAND}/derived/corrections_v4.json`, `${CAND}/derived/corrections_v4_cash.json`,
      `${SEPT27}/derived/summary.json`, `${SEPT27}/derived/corrections.json`, `${SCHOOLS}/derived/summary.json`, `${SCHOOLS}/derived/main_case_bands.csv`,
      "assumption_explorer_2026_09_21/engine.js", "assumption_explorer_2026_09_21/derived/model.json"].map((f) => [f, sha256(f)])),
  },
};
fs.writeFileSync(path.join(OUT, "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "components.csv"), compCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "corrections.json"), JSON.stringify(payload, null, 1) + "\n");

console.log("\n[result]");
console.log(`  September 27 case               ${f2(s27.main_case)}`);
console.log(`  main case                       ${f2(C)}  ends ${newEnds.map((e) => e.join("/")).join(", ")}`);
console.log(`  cash set                        ${f2(Ccash)}`);
for (const [k, v] of Object.entries(stepsObj)) console.log(`    change at fixed specs, ${k.padEnd(14)} ${v[0].toFixed(4)} / ${v[1].toFixed(4)}`);
console.log(`  without the capital return      ${f2(withoutCapital)}`);
console.log(`  option A (beside)               ${f2(optionA)}`);
console.log(`  at 7% (beside)                  ${f2(at7)}`);
console.log(`  general government at 0         ${f2(ggFixed)}`);
console.log(`  uncorrected at the responses    ${f2(uncorrectedAtResponses)}`);
console.log(`  range                           ${rangeLowEnd[0].toFixed(1)}–${rangeHighEnd[1].toFixed(1)} (quadrature ${quadrature[0].toFixed(1)}–${quadrature[1].toFixed(1)})`);
for (const [pf, v] of Object.entries(otherProfiles)) console.log(`  ${pf.padEnd(31)} ${f2(v.adopted)}`);
console.log(`  old main profile                ${f2(oldProfile.with_rental_assistance_capital_and_enterprises)}`);
for (const x of components) console.log(`    range: ${x.name.padEnd(18)} low end ${x.lo[0].toFixed(2)}..+${x.hi[0].toFixed(2)}  high end ${x.lo[1].toFixed(2)}..+${x.hi[1].toFixed(2)}`);
console.log("all gates passed");
