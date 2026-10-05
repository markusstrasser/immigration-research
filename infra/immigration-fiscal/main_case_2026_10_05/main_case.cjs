/* The main case adopted on 2026-10-05 (v5; decisions/2026-10-05-main-case-v5.md), written to the September 29 lane's
 * output contract (main_case_2026_09_29/derived: main_case_bands.csv, components.csv, per_spec.csv, summary.json and
 * corrections.json here; sign_reversal.cjs writes sign_reversal.csv). package.cjs holds the definitions; this script
 * runs the gates and writes derived/.
 *
 * Every September 29 file, column, row name and key is kept, with v5's value where the quantity is defined on v5. The
 * rows and keys that record how earlier cases were built keep the September 29 lane's values (history): the September
 * 27 case and its additions, the schools case, the first-year response, v4's items, the earlier adopted bands, the
 * capital lane's rows before rental assistance and the congestion item. One block moves: change_at_fixed_specifications
 * holds v5's change from the September 29 case, by part of the lineage line, so the September 29 case's own parts (v4's
 * items and the September 27 case's) sit under change_at_fixed_specifications.sept29_case. Added: the band rows
 * sept29_case and sept29_cash_set; the keys adopted_2026_09_29 and v5; each_addition.lineage; derived/corrections_cash.json.
 *
 * Gates (exit 1 and nothing written on failure):
 *   G1  the band is the lineage lane's (main_case_lineage_2026_10_05/derived/v5_summary.json, arm b): the set and the
 *       cash set, the two methods' mean, with the end specifications 48 / 11 in both methods (1e-9); the payload models
 *       give the methods' mean at every specification (1e-9), as does consumer.cjs (engine.js, model.json and the payload,
 *       no package); the merged payload's model is the v4 payload's model with the lineage payload applied after it,
 *       exactly;
 *   and the payload is the v4 payload with the lineage addition merged in and the adoption stamps, nothing else; the
 *       lineage population in meta.lineage is population.json's arm b and C3; only the group-size responses differ from
 *       v4's; the specifications carry meta.responses; the profiles hold each correction line with its parent; general
 *       government at 0 moves only its line and its capital; the v4 case re-derives through SEPT29 and the history rows
 *       are the September 29 lane's; the lineage line's parts (the union's response move, the G3+ members, the whites)
 *       add to the change from v4 and match the lineage lane's.
 * Run from anywhere: node main_case.cjs [--out-dir DIR] -> derived/main_case_bands.csv, components.csv, per_spec.csv,
 * summary.json, corrections.json, corrections_cash.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("./package.cjs");
const Consumer = require(path.join(__dirname, "..", "main_case_candidate_v4_2026_09_29", "consumer.cjs"));
const { Engine, MODEL, FISCAL, HERE, ALLOCS, METHODS, CAP, PARTS, PROFILES, MAIN_PROFILE, LR_LINES, RENTAL, RATES, ENTERPRISES,
  ENTERPRISES_ALLOWED, ENTERPRISE_LINE, V4PKG: V4, gateState, gate, near, f2, csvRows, readJson, withCentral, specsFor, modelFor,
  evaluateFull, evalPackage, central, correctionsPayload, populationShare, sha256 } = P;
const P4 = P.SEPT29, PC = P.CASH, PC4 = P.SEPT29_CASH;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const SEPT29 = "main_case_2026_09_29";
const LINEAGE = P.LINEAGE_LANE;
const CAND = "main_case_candidate_v4_2026_09_29";
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const ex = (x) => x.toExponential(1);
const fx = (x) => x.toFixed(4);

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

// ---------------------------------------------------------------------------------------------------
console.log("[G1: the lineage lane's bands]");
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
bandGates("the set", C, newCosts, newEnds, linSet);
const cashModels = METHODS.map((m) => PC.modelFor("central", m, PC.withCentral({})));
const cashRuns = runs(PC.MAIN_SPECS, MAIN_PROFILE, cashModels, PC);
const cashCosts = costsOf(cashRuns);
const cashEnds = ends(cashCosts);
const Ccash = PC.central({});
bandGates("the cash set", Ccash, cashCosts, cashEnds, linCash);
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
const cashPayload = PC.correctionsPayload();
const SPEC_FIELDS = ["allocation", "normalization", "share", "school", "gg", "uc", "reading"];
for (const [name, pl, want, sp] of [["corrections.json", payload, meanSet, specs], ["corrections_cash.json", cashPayload, meanCash, PC.MAIN_SPECS]]) {
  const independent = Consumer.evaluateAll(JSON.parse(JSON.stringify(pl)), { engine: Engine, model: MODEL });
  const g = worst(independent.map((x, i) => x.cost_bn - want[i]));
  gate(`consumer.cjs (engine.js, model.json and ${name}, no package) gives the methods' mean at every specification (1e-9): it reads gg, the line responses and the long-run subfunctions from meta.responses`,
    independent.length === 64 && independent.every((x, i) => SPEC_FIELDS.every((f) => x.spec[f] === sp[i][f])) && g < 1e-9, `max |diff| ${ex(g)}`);
}
// The merge is the lineage lane's apply rule: the v4 payload, then the lineage payload.
const twoStep = Engine.applyCorrections(Engine.applyCorrections(MODEL, payload29), P.ADDITION.set);
const merged = P.payloadModel();
const strip = (m) => JSON.stringify(Object.assign({}, m, { corrections: null }));
gate("the merged payload's model is model.json with the v4 payload and then the lineage payload applied (lineage lane meta.apply), exactly",
  strip(merged) === strip(twoStep) && strip(PC.payloadModel()) === strip(Engine.applyCorrections(Engine.applyCorrections(MODEL, cash29), P.ADDITION.cash)));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the payload and the specifications]");
const metaKeys29 = Object.keys(payload29.meta);
const changed = Object.keys(payload.meta).filter((k) => JSON.stringify(payload.meta[k]) !== JSON.stringify(payload29.meta[k]));
const longRun = (K) => K.components.filter((c) => c.response.kind === "long_run_subfunction").map((c) => c.id);
const capMoved = payload.meta.capital_return.components.filter((c, i) => JSON.stringify(c) !== JSON.stringify(payload29.meta.capital_return.components[i])).map((c) => c.id);
const n29 = payload29.edits.length;
gate(`corrections.json is the September 29 corrections.json with the lineage payload merged in: its edits appended, its P and F, its responses, the long-run capital values at them, meta.lineage and the stamps (${P.STAMPED.join(", ")}); lines, receipt lines and every other meta key identical`,
  JSON.stringify(Object.keys(payload)) === JSON.stringify(Object.keys(payload29))
  && JSON.stringify(Object.keys(payload.meta)) === JSON.stringify(metaKeys29.concat(["lineage"]))
  && ["lines", "receipt_lines"].every((k) => JSON.stringify(payload[k]) === JSON.stringify(payload29[k]))
  && JSON.stringify(payload.edits) === JSON.stringify(payload29.edits.concat(P.ADDITION.set.edits))
  && JSON.stringify(payload.production.dims) === JSON.stringify(payload29.production.dims)
  && JSON.stringify(payload.production.sampling_se_bn) === JSON.stringify(payload29.production.sampling_se_bn)
  && ["private_wtp_bn", "induced_receipts_bn"].every((k) => JSON.stringify(payload.production[k]) === JSON.stringify(P.ADDITION.set.production[k]))
  && JSON.stringify(payload.meta.responses) === JSON.stringify(P.ADDITION.set.meta.responses)
  && JSON.stringify(changed.sort()) === JSON.stringify(["adopted", "capital_return", "case", "decision", "lineage", "responses", "source", "status"])
  && JSON.stringify(capMoved) === JSON.stringify(longRun(payload29.meta.capital_return)),
  `${payload.edits.length} edits (${n29} + ${P.ADDITION.set.edits.length}); meta changed: ${changed.join(", ")}; capital values moved: ${capMoved.join(", ")}`);
gate(`meta: adopted ${P.ADOPTED}, decision ${P.DECISION}, no "not adopted" left in the case text or status`, payload.meta.adopted === P.ADOPTED
  && payload.meta.decision === P.DECISION && !/not adopted/.test(payload.meta.case) && !/not adopted/.test(payload.meta.status));
const L = payload.meta.lineage, A = POP.arms[ARM];
gate("meta.lineage: the arm, counts, members, C3 and its source are population.json's and the lineage payload's (exact); the added people are G3+, counted whole",
  L.arm === ARM && L.generation === "G3plus" && L.counting.rule === P.COUNTING && P.COUNTING === "whole" && L.counts.added === A.added && L.counts.at_g3_rate === A.g3_rate && L.counts.later_losses === A.later
  && L.counts.lineage_population === A.population && L.counts.account_union === POP.meta.account_union
  && L.c3.value === POP.c3.value && L.c3.se === POP.c3.se && L.c3.label === POP.c3.label && L.c3.source === POP.c3.source && L.c3.override === false
  && L.members.g3plus === P.ADDITION.set.meta.lineage.m_g3plus && L.members.white === P.ADDITION.set.meta.lineage.m_white
  && L.edits.first === n29 && L.edits.count === P.ADDITION.set.edits.length && L.s.v5 === A.s && L.k_metro === A.k_metro,
  `${(L.counts.added / 1e6).toFixed(4)}M added (${(L.counts.at_g3_rate / 1e6).toFixed(4)}M at the G3 rate, ${(L.counts.later_losses / 1e6).toFixed(4)}M later), lineage ${(L.counts.lineage_population / 1e6).toFixed(4)}M; C3 ${L.c3.value} (SE ${L.c3.se}), ${L.c3.source}`);
gate("the cash payload is the cash set's v4 payload with the cash lineage payload merged in, the same way, and the same lineage population",
  JSON.stringify(cashPayload.edits) === JSON.stringify(cash29.edits.concat(P.ADDITION.cash.edits))
  && JSON.stringify(cashPayload.meta.responses) === JSON.stringify(P.ADDITION.cash.meta.responses)
  && JSON.stringify(cashPayload.meta.lineage.counts) === JSON.stringify(L.counts) && JSON.stringify(cashPayload.meta.lineage.c3) === JSON.stringify(L.c3));
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
const total = part((m, i) => newCosts[m][i] - v4Costs[m][i]);
const unionMove = part((m, i) => unionCosts[m][i] - v4Costs[m][i]);
const members = part((m, i) => newCosts[m][i] - unionCosts[m][i]);
const linG3 = linSet.of_which_g3plus_part_bn, linW = linSet.of_which_white_part_bn, linU = linSet.of_which_union_response_move_bn;
gate("the parts add to the change from v4 (1e-9), which is the band move (the same ends)",
  [0, 1].every((e) => near(unionMove[e] + members[e], total[e], 1e-9) && near(total[e], C[e] - C4[e], 1e-9)), `${f2(unionMove)} + ${f2(members)} = ${f2(total)}`);
gate("the union's move and the added people's part are the lineage lane's (of_which_union_response_move_bn; of_which_g3plus_part_bn + of_which_white_part_bn; 1e-9)",
  [0, 1].every((e) => near(unionMove[e], linU[e], 1e-9) && near(members[e], linG3[e] + linW[e], 1e-9)),
  `G3+ members ${f2(linG3)}, whites ${f2(linW)}`);
const cashTotal = [0, 1].map((e) => Ccash[e] - C4cash[e]);
gate("the cash set's change from v4's cash set is the lineage lane's cash change (1e-9)",
  [0, 1].every((e) => near(cashTotal[e], linCash.change_from_v4_bn[e], 1e-9)), f2(cashTotal));

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
const k12Diff = atEnds(newEnds, (m, i) => byId(pupilRuns[m][i], "k12") - byId(newRuns[m][i], "k12"));
const k12Keys = atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.find((c) => c.id === "k12").key);
gate("with the pupil share the case differs by the K-12 difference alone", worst(pupilRuns.flatMap((xs, m) => xs.map((r, i) =>
  r.cost_bn - newCosts[m][i] - (byId(r, "k12") - byId(newRuns[m][i], "k12"))))) < 1e-9, "every specification");
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

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the uncorrected model at the adopted responses]");
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
const zeroPayload = { lines: payload.lines, edits: [], meta: payload.meta,
  receipt_lines: payload.receipt_lines.map((l) => Object.assign({}, l, { national_bn: 0, cells: Object.fromEntries(Object.entries(l.cells)
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
gate("gaps.csv has one land row for every capital component of the payload, under its part", landRows.length === COMPONENTS.length
  && COMPONENTS.every((c) => landRows.some((r) => r.item.match(LAND_ROW)[3] === c.id && landPart(r) === c.part)), `${landRows.length} rows`);
const landAt = (rs, m, i, pred) => rs[m][i].capital.components.filter(pred).reduce((a, c) => a + landStock[c.id] * specs[i].rate * c.key * c.response, 0);
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
const groupReceipts = Object.assign({}, s29.group_receipts_bn, { adopted: receiptsTotal(payloadModel), adopted_2026_09_29: s29.group_receipts_bn.adopted });

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
const PER = (x) => x * 1e9 / L.counts.lineage_population;
const summary = {
  lane: P.LANE,
  decision: P.DECISION,
  adopted_2026_09_23: s29.adopted_2026_09_23, adopted_2026_09_24: s29.adopted_2026_09_24,
  adopted_2026_09_26: s29.adopted_2026_09_26, adopted_2026_09_26_schools: s29.adopted_2026_09_26_schools,
  adopted_2026_09_27: s29.adopted_2026_09_27,
  adopted_2026_09_29: s29.main_case,
  first_year_response: s29.first_year_response, schools_case: s29.schools_case,
  uncorrected_at_adopted_responses: uncorrectedAtResponses, without_capital_return: withoutCapital,
  main_case: C,
  cash_set: { band_bn: Ccash, by_method_bn: Object.fromEntries(METHODS.map((m, k) => [m, ownBands(cashCosts)[k]])), end_specifications: cashEnds,
    change_from_main_case_bn: [Ccash[0] - C[0], Ccash[1] - C[1]], change_from_the_september_29_cash_set_bn: cashTotal,
    note: `the set with the pension switch off (pension4 "cash"): social security and Medicare's Part A at the group's current benefits instead of the accrual at payable benefits net of the tax on benefits; the payload is derived/corrections_cash.json (${P.BASE_FILES.cash} with ${P.LINEAGE_FILES.cash} merged in)` },
  change: [C[0] - C4[0], C[1] - C4[1]],
  change_at_fixed_specifications: {
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
      note: "these components re-run the union's data with the added people's amounts at the case's, so each deviates as on the September 29 case (within $0.001bn); range_ends_move_if_proportional_bn is how far the range's low and high ends would move had the added people's amounts moved in proportion to the union's (the added share of each component's deviation), an indication of the omission, not a bound" } },
  other_profiles: otherProfiles, old_main_profile: oldProfile,
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn,
  each_addition: Object.assign({}, s29.each_addition, { lineage: C }),
  beside_the_account: {
    rate_7pct: { band_bn: at7, return_at_end_specifications_bn: atEnds(newEnds, (m, i) => runs7[m][i].capital.total_bn), note: s29.beside_the_account.rate_7pct.note },
    land_per_10pct_of_land_to_structure_value: land,
    enterprises_out_option_A: { band_bn: optionA, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => optionARuns[m][i].cost_bn - newCosts[m][i]),
      note: s29.beside_the_account.enterprises_out_option_A.note },
    rental_assistance_at_0: { band_bn: rentalAt0, note: s29.beside_the_account.rental_assistance_at_0.note },
    congestion: Object.assign({}, s29.beside_the_account.congestion, { not_recomputed_v5: "the September 27 figure, carried by the September 29 lane; not recomputed with the added people" }),
    transit_at_riders_key_item_8: { band_bn: with8, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => runs8[m][i].cost_bn - newCosts[m][i]),
      options: beside8.o, note: `${beside8.name}: beside the case (candidate v4's BESIDE_ITEMS), not in it` },
    uninsured_use_0_7x_item_10: { band_bn: with10, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => runs10[m][i].cost_bn - newCosts[m][i]),
      options: beside10.o, note: `${beside10.name}: beside the case (candidate v4's BESIDE_ITEMS), not in it` },
  },
  by_side_vs_uncorrected_at_adopted_responses: sides,
  group_receipts_bn: groupReceipts,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi, variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
  v4: s29.v4,
  v5: {
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
};
fs.writeFileSync(path.join(OUT, "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "components.csv"), compCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "corrections.json"), JSON.stringify(payload, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "corrections_cash.json"), JSON.stringify(cashPayload, null, 1) + "\n");

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
for (const [v, d] of Object.entries(lineageByVariant)) console.log(`    lineage under ${v.padEnd(40)} ${f2(d)}`);
for (const x of components) console.log(`    range: ${x.name.padEnd(18)} low end ${x.lo[0].toFixed(2)}..+${x.hi[0].toFixed(2)}  high end ${x.lo[1].toFixed(2)}..+${x.hi[1].toFixed(2)}`);
console.log("all gates passed");
