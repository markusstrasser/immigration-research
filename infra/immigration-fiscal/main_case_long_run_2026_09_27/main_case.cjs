/* The main case with long-run road and park responses, rental assistance, the return on public capital and the
 * government enterprises under option D (BRIEF.md). package.cjs holds the definitions; this script runs the gates
 * and writes derived/.
 *
 * Base: the schools case (main_case_schools_full_2026_09_26, $258.4885–291.9548bn, end specifications 48 / 11),
 * reproduced exactly at the old settings before any change. The additions, each gated against its own lane:
 *   - long-run responses for economic affairs and recreation (service_response_long_run_2026_09_27);
 *   - rental assistance at response 1 (its group amount on the corrected model, at every specification);
 *   - the return on public capital and the government enterprises
 *     (capital_return_services_2026_09_27/derived/engine_components.json, 250ccb5), 2% at the low end and 3% at
 *     the high end. On that lane's premises the package reproduces its core, block and enterprise returns at every
 *     specification, its core band, its option D and option A bands, its re-keyed option D band and every
 *     definition variant's check values;
 *   - the enterprise receipt's re-key to the corrected population share (one receipt shift in the payload).
 *
 * Gates (exit 1 and nothing written on failure): the old settings reproduce the schools case at every
 * specification exactly on the re-keyed models, and its band to 1e-6; each addition alone reproduces its lane; the
 * tied specifications (reading and rate follow general government's reading) give the crossed band; the long-run
 * sensitivities reproduce the response lane's; the payload is the schools case's lines and edits plus the re-key,
 * and a path that uses only the engine, model.json and corrections.json gives the same cost at every specification
 * (1e-9); no receipt moves but the enterprise surplus.
 * Run from anywhere: node main_case.cjs [--out-dir DIR] -> derived/main_case_bands.csv, components.csv,
 * summary.json, corrections.json, per_spec.csv.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("./package.cjs");
const { PSCHOOLS: S, Engine, MODEL, HERE, ALLOCS, METHODS, CASES, CONSTANTS, LTSS_RANGE, CK_SPECS, benefitSe, CAP, PARTS,
  PROFILES, MAIN_PROFILE, LR, LR_LINES, RENTAL, SUBFUNCTIONS, LONG_RUN_VARIANTS, RATES, ENTERPRISES, ENTERPRISES_ALLOWED,
  ENTERPRISE_LINE, REKEY_LINE, gateState, gate, near, f2, csvRows, readJson, withCentral, specsFor, modelFor, evaluateFull,
  evalPackage, central, correctionsPayload, populationShare } = P;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const ex = (x) => x.toExponential(1);
// Per-specification evaluations on the adopted models (the enterprise receipt re-keyed) or on the capital lane's
// premises (the receipt at model.json's share), and each method's end specifications.
const MODELS = METHODS.map((m) => modelFor("central", m, withCentral({})));
const MODELS_LANE = METHODS.map((m) => modelFor("central", m, withCentral({ enterprise_rekey: false })));
const runs = (specs, profile, models) => (models || MODELS).map((model) => specs.map((spec) => evaluateFull(model, spec, profile)));
const costsOf = (rs) => rs.map((xs) => xs.map((r) => r.cost_bn));
const ends = (cm) => cm.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
const bandOf = (cm) => [mean(cm.map((xs) => Math.min(...xs))), mean(cm.map((xs) => Math.max(...xs)))];
// A quantity read at given end specifications in each method and averaged, [low end, high end].
const atEnds = (idx, f) => [0, 1].map((e) => mean(idx.map((ij, m) => f(m, ij[e]))));
const amount = (evaluation, id) => evaluation.spending.find((l) => l.id === id).amount_bn;
const national = (evaluation, id) => evaluation.spending.find((l) => l.id === id).national_bn;
const responseOf = (evaluation, id) => evaluation.spending.find((l) => l.id === id).response;
const capitalWhere = (r, pred) => r.capital.components.filter(pred).reduce((a, c) => a + c.return_bn, 0);
const capitalGroup = (r, part) => capitalWhere(r, (c) => c.group === part);
const byId = (r, id) => capitalWhere(r, (c) => c.id === id);
// The enterprise-surplus receipt's row and its cost (option D sets its response to 1).
const esRow = (r) => r.evaluation.receipts.find((x) => x.id === ENTERPRISE_LINE);
const esCost = (r) => -esRow(r).effect_bn;
// Every specification at the settings of one reading, and every specification at one rate.
const atReading = (list, rd) => {
  const ref = list.find((x) => x.reading === rd);
  return list.map((s) => Object.assign({}, s, { reading: rd, line_responses: ref.line_responses, rate: ref.rate }));
};
const fixedRate = (o, rate) => specsFor(Object.assign({}, o, { rates: { low: rate, high: rate } }));

const schools = readJson("main_case_schools_full_2026_09_26/derived/summary.json");
const schoolsPayload = readJson("main_case_schools_full_2026_09_26/derived/corrections.json");
const lrBand = readJson("service_response_long_run_2026_09_27/derived/candidate_band.json");
const lrPerSpec = csvRows("service_response_long_run_2026_09_27/derived/per_spec_costs.csv");
const congestion = readJson("service_response_long_run_2026_09_27/derived/net_change.json");
const CAPDIR = "capital_return_services_2026_09_27/derived";
const capSummary = readJson(`${CAPDIR}/summary.json`);
const capBands = csvRows(`${CAPDIR}/bands.csv`);
const capCombined = csvRows(`${CAPDIR}/combined_bands.csv`);
const capComponentsPerSpec = csvRows(`${CAPDIR}/per_spec_components.csv`);
const capBlockPerSpec = csvRows(`${CAPDIR}/per_spec_block.csv`);
const capGaps = csvRows(`${CAPDIR}/gaps.csv`);
const capRow = (rows, label, rate) => {
  const r = rows.find((x) => x.case === label && x.rate === rate);
  if (!r) throw new Error(`[BLOCKED] ${CAPDIR} lacks the row "${label}" at ${rate}`);
  return r;
};
const pair = (r) => [Number(r.low_bn), Number(r.high_bn)];
const endCols = (r, name) => [Number(r[`${name}_at_low_end_bn`]), Number(r[`${name}_at_high_end_bn`])];
const CASE_ENDS = CAP.band.case_end_specs;

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the schools case at the old settings]");
const OLD = { long_run: false, rental: 0, capital: false, enterprise_receipt: 0 };
// The schools case's evaluations (its cost() is -evaluate(stateFor()).welfare_bn), kept for the receipts gate.
const schoolsEvals = MODELS_LANE.map((model) => S.MAIN_SPECS.map((spec) => Engine.evaluate(model, S.stateFor(model, spec, S.MAIN_PROFILE))));
const schoolsCosts = schoolsEvals.map((xs) => xs.map((ev) => -ev.welfare_bn));
const oldRuns = runs(specsFor(OLD));
const oldCosts = costsOf(oldRuns);
gate("the schools package reproduces its published case", (() => { const c = S.central({});
  return near(c[0], schools.main_case[0], 1e-9) && near(c[1], schools.main_case[1], 1e-9); })(), f2(schools.main_case));
gate("old settings on the re-keyed models: every per-specification cost equals the schools case's exactly (both methods; the re-key alone moves nothing while the receipt is at 0)",
  oldCosts.every((xs, m) => xs.every((x, i) => x === schoolsCosts[m][i])), `${oldCosts.length} x ${oldCosts[0].length}`);
const oldBand = central(OLD);
gate("old settings: the band is the schools case's to 1e-6", near(oldBand[0], schools.main_case[0], 1e-6)
  && near(oldBand[1], schools.main_case[1], 1e-6), f2(oldBand));
const schoolsEnds = ends(schoolsCosts);
gate(`the schools case's end specifications are ${CASE_ENDS.join(" / ")} in both methods (the capital lane's case ends)`,
  schoolsEnds.every((e) => e[0] === CASE_ENDS[0] && e[1] === CASE_ENDS[1]), JSON.stringify(schoolsEnds));
const firstYear = central(Object.assign({}, OLD, { school_rule: "one_year" }));
gate("old settings with the first-year school response give the September 26 case", near(firstYear[0], schools.adopted_2026_09_26[0], 1e-9)
  && near(firstYear[1], schools.adopted_2026_09_26[1], 1e-9), f2(firstYear));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the enterprise receipt's re-key]");
const payload = correctionsPayload();
const payloadModel = Engine.applyCorrections(MODEL, { lines: payload.lines, edits: payload.edits });
const SHARE = populationShare(MODELS[0]).personal;
gate(`the corrected population share (the population cell of ${REKEY_LINE}) is one number in both methods, both allocations and the payload`,
  [...MODELS, payloadModel].every((m) => ALLOCS.every((a) => near(populationShare(m)[a], SHARE, 1e-14))), String(SHARE));
const popLines = [...new Set(schoolsPayload.edits.filter((e) => e.side === "spending" && e.key === "population").map((e) => e.line))];
const popOff = (m) => popLines.filter((id) => {
  const l = m.spending.lines.find((x) => x.id === id);
  return ALLOCS.some((a) => Math.abs(l.keys.population[a].target_bn / l.national_bn - SHARE) > 1e-8);
});
gate("every population-keyed spending line the corrections edit sits at that share (1e-8) but public_order_safety, whose population cell carries the CPS lane's shift scaled to the justice use key (the case keys that line by use)",
  popLines.length === 15 && [...MODELS, payloadModel].every((m) => JSON.stringify(popOff(m)) === JSON.stringify(["public_order_safety"])),
  `${popLines.length} lines; off the share: ${popOff(payloadModel).join(" ")}`);
const esShare = (m) => ALLOCS.map((a) => {
  const l = m.receipts.lines.find((x) => x.id === ENTERPRISE_LINE);
  return l.cells[m.receipts.reference][a].target_bn / l.national_bn;
});
const kc = capSummary.enterprises.key_consistency;
gate("the re-keyed receipt sits at that share on the reference rule (both methods and the payload); the capital lane's premises keep model.json's",
  [...MODELS, payloadModel].every((m) => esShare(m).every((x) => near(x, SHARE, 1e-15)))
  && MODELS_LANE.every((m) => esShare(m).every((x) => x === kc.receipt_key[0])) && kc.spending_population_key.every((x) => x === SHARE),
  `${SHARE.toFixed(9)} (model.json ${kc.receipt_key[0].toFixed(9)})`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: long-run responses]");
const specs = specsFor({});
const reading = specs.map((s) => s.reading);
gate("reading is low exactly where general government takes its low response", specs.every((s) =>
  (s.reading === "low") === (s.gg === P.RESPONSES.general_government.low)), `${reading.filter((r) => r === "low").length} low of 64`);
gate("the rate follows the reading (2% low, 3% high)", specs.every((s) => s.rate === RATES[s.reading]), "64 specifications");
const blendGap = worst(LR_LINES.flatMap((id) => ["low", "high"].map((r) =>
  LR.lines[id].response[r] - SUBFUNCTIONS.filter((sf) => sf.line === id).reduce((a, sf) => a + sf.share_of_line * sf.response[r], 0))));
gate("each line's response is the amount-weighted blend of its subfunctions", blendGap < 1e-12, `max |diff| ${ex(blendGap)}`);
const lrOnly = { rental: 0, capital: false, enterprise_receipt: 0 };
const lrRuns = runs(specsFor(lrOnly));
const lrCosts = costsOf(lrRuns);
const lrOnlyBand = central(lrOnly);
gate("long-run responses alone give the response lane's candidate (candidate_band.json) to 1e-6",
  near(lrOnlyBand[0], lrBand.candidate.band_bn[0], 1e-6) && near(lrOnlyBand[1], lrBand.candidate.band_bn[1], 1e-6), f2(lrOnlyBand));
gate("long-run responses alone keep the end specifications 48 / 11", ends(lrCosts).every((e) => e[0] === 48 && e[1] === 11),
  JSON.stringify(ends(lrCosts)));
const lrCsvGap = worst(METHODS.flatMap((meth, m) => lrPerSpec.filter((r) => r.method === meth).map((r) => {
  const i = Number(r.spec);
  return (lrCosts[m][i] - Number(reading[i] === "low" ? r.cost_low_bn : r.cost_high_bn)) / lrCosts[m][i];
})));
gate("long-run responses alone match the lane's per-specification costs at the tied reading", lrCsvGap < 1e-11,
  `max relative |diff| ${ex(lrCsvGap)} (the lane prints 12 significant digits)`);
// Sensitivities at the fixed end specifications, engine only: each variant's cost less the adopted responses'.
const sensGap = worst(Object.entries(lrBand.sensitivities_at_end_specifications).flatMap(([v, s]) => {
  const vc = costsOf(runs(specsFor({ rental: 0, capital: false, long_run: v, enterprise_receipt: 0 })));
  const d = atEnds(schoolsEnds, (m, i) => vc[m][i] - lrCosts[m][i]);
  return [d[0] - s.delta_bn[0], d[1] - s.delta_bn[1]];
}));
gate("the five long-run variants reproduce the response lane's sensitivities at the end specifications", sensGap < 1e-9,
  `max |diff| ${ex(sensGap)}`);

console.log("\n[gates: rental assistance]");
const rentalRuns = runs(specsFor({ long_run: false, capital: false, enterprise_receipt: 0 }));
const rentalGap = worst(rentalRuns.flatMap((xs, m) => xs.map((r, i) => r.cost_bn - oldCosts[m][i] - amount(r.evaluation, RENTAL))));
gate("rental assistance adds its group amount at every specification and method (overlap netted: 0)", rentalGap < 1e-9,
  `max |diff| ${ex(rentalGap)}`);
const rentalAmount = METHODS.map((_, m) => ALLOCS.map((a) => MODELS[m].spending.lines.find((l) => l.id === RENTAL).keys.housing_support[a].target_bn));
const rentalUncorrected = ALLOCS.map((a) => MODEL.spending.lines.find((l) => l.id === RENTAL).keys.housing_support[a].target_bn);
gate("with the receipt response set to 0 the enterprise-surplus receipt is at response 0 at every specification",
  worst(rentalRuns.flatMap((xs) => xs.map((r) => esRow(r).response))) === 0, "the schools case's setting");

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the capital return and the enterprises, on the capital lane's premises]");
const blockValuesGap = worst(CAP.components.filter((c) => c.response.kind === "long_run_subfunction").flatMap((c) => {
  const sf = SUBFUNCTIONS.find((x) => x.id === c.response.subfunction && x.line === c.response.line);
  if (!sf) return [Infinity];
  return ["low", "high"].map((r) => c.response.values[r] - sf.response[r])
    .concat([c.response.values.across_high - P.subfunctionResponses("across_states_at_high_end", "high")[sf.id]]);
}));
gate("the block components' long-run responses are the response lane's subfunctions (low, high, across-state high)",
  blockValuesGap === 0, `${CAP.components.filter((c) => c.response.kind === "long_run_subfunction").length} components`);
gate("the components file has 8 core, 5 block and 11 enterprise components", PARTS.map((p) => CAP.components.filter((c) => c.part === p).length).join("/") === "8/5/11",
  PARTS.map((p) => `${p} ${CAP.components.filter((c) => c.part === p).length}`).join(", "));
// The core components at every specification and rate (per_spec_components.csv).
const RATE_TAGS = { "2pct": 0.02, "3pct": 0.03, "7pct": 0.07 };
const coreIds = CAP.components.filter((c) => c.part === "core").map((c) => c.id).sort();
let perComponentGap = 0, perComponentRows = 0;
for (const [tag, rate] of Object.entries(RATE_TAGS)) {
  const rs = runs(fixedRate({ long_run: false, rental: 0, enterprise_receipt: 0 }, rate), MAIN_PROFILE, MODELS_LANE);
  for (const r of capComponentsPerSpec) {
    const m = METHODS.indexOf(r.method);
    perComponentGap = Math.max(perComponentGap, Math.abs(byId(rs[m][Number(r.spec)], r.component) - Number(r[`return_${tag}_bn`])));
    perComponentRows += 1;
  }
}
gate("the core components' returns at every specification and rate are the capital lane's (per_spec_components.csv, 6 decimals)",
  JSON.stringify([...new Set(capComponentsPerSpec.map((r) => r.component))].sort()) === JSON.stringify(coreIds)
  && perComponentRows === 3 * coreIds.length * 128 && perComponentGap < 1e-6, `${perComponentRows} rows, max |diff| ${ex(perComponentGap)}`);
const laneCore = central({ long_run: false, rental: 0, enterprises: "A" });
const laneCoreRow = pair(capRow(capBands, "candidate: 2% at the low end and 3% at the high end", "2pct/3pct"));
gate("the core return alone on the schools case gives the capital lane's core band (bands.csv) to 1e-6",
  near(laneCore[0], laneCoreRow[0], 1e-6) && near(laneCore[1], laneCoreRow[1], 1e-6), `${f2(laneCore)} vs ${f2(laneCoreRow)}`);
// The block at every specification, reading and rate, and the enterprise returns and the surplus under option D.
let blockGap = 0, entGap = 0, esGap = 0, blockRows = 0;
for (const rd of ["low", "high", "across_high"]) {
  const variant = rd === "across_high" ? "across_states_at_high_end" : "adopted";
  for (const [tag, rate] of Object.entries(RATE_TAGS)) {
    const rs = runs(atReading(fixedRate({ rental: 0, long_run: variant }, rate), rd === "low" ? "low" : "high"), MAIN_PROFILE, MODELS_LANE);
    for (const r of capBlockPerSpec) {
      const m = METHODS.indexOf(r.method), i = Number(r.spec);
      blockGap = Math.max(blockGap, Math.abs(capitalGroup(rs[m][i], "block") - Number(r[`block_return_${tag}_${rd}_bn`])));
      entGap = Math.max(entGap, Math.abs(capitalGroup(rs[m][i], "enterprise") - Number(r[`enterprise_return_option_D_${tag}_bn`])));
      esGap = Math.max(esGap, Math.abs(esCost(rs[m][i]) - Number(r.enterprise_surplus_move_option_D_bn)));
      blockRows += 1;
    }
  }
}
gate("the block, enterprise and surplus columns at every specification, reading and rate are the capital lane's (per_spec_block.csv)",
  blockRows === 9 * 128 && blockGap < 1e-6 && entGap < 1e-6 && esGap < 1e-9,
  `${blockRows} rows; max |diff| block ${ex(blockGap)}, enterprise returns ${ex(entGap)}, surplus ${ex(esGap)}`);
const combinedRows = {
  "option D: long-run responses + core + block + enterprises": central({ rental: 0, enterprise_rekey: false }),
  "option A: long-run responses + core + block": central({ rental: 0, enterprises: "A" }),
  "option D, enterprises at the spending lines' population key": central({ rental: 0 }),
};
for (const [label, b] of Object.entries(combinedRows)) {
  const ref = pair(capRow(capCombined, label, "2pct/3pct"));
  gate(`combined_bands.csv "${label}" to 1e-6`, near(b[0], ref[0], 1e-6) && near(b[1], ref[1], 1e-6), `${f2(b)} vs ${f2(ref)}`);
}
// Every definition variant's check values (variants.*.check_at_case_ends_bn: [spec 48, spec 11], the methods' mean).
const CHECKS = { core_2pct: ["core", "low", 0.02], core_3pct: ["core", "high", 0.03], block_2pct_low: ["block", "low", 0.02],
  block_3pct_high: ["block", "high", 0.03], enterprise_returns_option_D_2pct: ["enterprise", "low", 0.02],
  enterprise_returns_option_D_3pct: ["enterprise", "high", 0.03] };
let variantGap = 0, variantValues = 0;
const variantMissing = [];
for (const [v, def] of Object.entries(CAP.variants)) {
  const chk = def.check_at_case_ends_bn || {};
  for (const [name, [part, rd, rate]] of Object.entries(CHECKS)) {
    if (!Array.isArray(chk[name])) { variantMissing.push(`${v}/${name}`); continue; }
    const at = atReading(fixedRate({ rental: 0, capital_variant: v }, rate), rd);
    const rs = runs(CASE_ENDS.map((i) => at[i]), MAIN_PROFILE, MODELS_LANE);
    [0, 1].forEach((j) => { variantGap = Math.max(variantGap, Math.abs(mean(rs.map((xs) => capitalGroup(xs[j], part))) - chk[name][j])); });
    variantValues += 2;
  }
}
gate("every capital definition variant reproduces its check values at the case ends (core, block and enterprise parts at 2% and 3%)",
  !variantMissing.length && variantGap < 1e-9,
  `${Object.keys(CAP.variants).length} variants, ${variantValues} values, max |diff| ${ex(variantGap)}${variantMissing.length ? "; missing " + variantMissing.join(" ") : ""}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the new case]");
const newRuns = runs(specs);
const newCosts = costsOf(newRuns);
const C = central({});
const newEnds = ends(newCosts);
gate("per-specification costs reproduce the band", (() => { const b = bandOf(newCosts); return near(b[0], C[0], 1e-9) && near(b[1], C[1], 1e-9); })(), f2(C));
// The crossed set: every specification at every low setting (low readings, the low rate) for the low end and at
// every high setting for the high end.
const crossedLow = costsOf(runs(atReading(specs, "low"))), crossedHigh = costsOf(runs(atReading(specs, "high")));
const crossed = [mean(crossedLow.map((xs) => Math.min(...xs))), mean(crossedHigh.map((xs) => Math.max(...xs)))];
gate("the tied specifications give the crossed band", near(crossed[0], C[0], 1e-9) && near(crossed[1], C[1], 1e-9), `${f2(crossed)} vs ${f2(C)}`);
gate("the new case keeps the end specifications 48 / 11", newEnds.every((e) => e[0] === 48 && e[1] === 11), JSON.stringify(newEnds));
gate(`option ${ENTERPRISES} (allowed ${ENTERPRISES_ALLOWED.join("/")}): the enterprise-surplus receipt responds at 1 and every enterprise component is keyed at the corrected share and responds at 1`,
  newRuns.every((xs) => xs.every((r) => esRow(r).response === 1 && r.capital.components.filter((c) => c.group === "enterprise")
    .every((c) => near(c.key, SHARE, 1e-15) && c.response === 1))), "every specification, both methods");
const addGap = worst(newRuns.flatMap((xs, m) => xs.map((r, i) => (r.cost_bn - oldCosts[m][i])
  - (lrCosts[m][i] - oldCosts[m][i]) - (rentalRuns[m][i].cost_bn - oldCosts[m][i]) - r.capital.total_bn - esCost(r))));
gate("the additions add at every specification (engine parts, the capital return, the enterprise receipt)", addGap < 1e-9, `max |diff| ${ex(addGap)}`);
// Receipts against the schools case under option D: every line's group amount is the schools case's but the
// enterprise surplus's, which is its national amount x the corrected population share.
const receiptPairs = newRuns.flatMap((xs, m) => xs.flatMap((r, i) => r.evaluation.receipts.map((x, k) => [x, schoolsEvals[m][i].receipts[k]])));
const esAmountGap = worst(receiptPairs.filter(([x]) => x.id === ENTERPRISE_LINE).map(([x]) => x.amount_bn - x.national_bn * SHARE));
gate("every receipt line's group amount equals the schools case's except enterprise_surplus, which equals its national amount x the corrected population share (every specification and method)",
  receiptPairs.length === 2 * 64 * MODEL.receipts.lines.length && receiptPairs.every(([x, o]) => x.id === o.id)
  && receiptPairs.filter(([x]) => x.id !== ENTERPRISE_LINE).every(([x, o]) => x.amount_bn === o.amount_bn) && esAmountGap < 1e-12,
  `${receiptPairs.length} line cells; others exact; enterprise_surplus max |diff| ${ex(esAmountGap)}`);
gate("no receipt's effect moves from the schools case's but the enterprise surplus's", receiptPairs.filter(([x]) => x.id !== ENTERPRISE_LINE)
  .every(([x, o]) => x.effect_bn === o.effect_bn), "exact");
const esSchools = (m, i) => schoolsEvals[m][i].receipts.find((x) => x.id === ENTERPRISE_LINE);
// K-12: the account's school key (the case and the capital lane's own definition) against the pupil share (the
// lane's variant k12_at_pupil_share), at the end specifications.
const pupilRuns = runs(specsFor({ capital_variant: "k12_at_pupil_share" }));
const k12Diff = atEnds(newEnds, (m, i) => byId(pupilRuns[m][i], "k12") - byId(newRuns[m][i], "k12"));
const k12Keys = atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.find((c) => c.id === "k12").key);
const k12Lane = CAP.k12_keys_at_case_ends;
const k12LaneDiff = [k12Lane.spec48.return_bn["2pct"].pupil_share - k12Lane.spec48.return_bn["2pct"].account_key,
  k12Lane.spec11.return_bn["3pct"].pupil_share - k12Lane.spec11.return_bn["3pct"].account_key];
gate("the K-12 key difference at the end specifications is the capital lane's (k12_keys_at_case_ends)",
  near(k12Diff[0], k12LaneDiff[0], 1e-9) && near(k12Diff[1], k12LaneDiff[1], 1e-9), `${f2(k12Diff)} (keys ${k12Keys.map((x) => x.toFixed(6)).join(" / ")})`);
gate("with the pupil share the new case differs by the K-12 difference alone",
  worst(pupilRuns.flatMap((xs, m) => xs.map((r, i) => r.cost_bn - newCosts[m][i] - (byId(r, "k12") - byId(newRuns[m][i], "k12"))))) < 1e-9,
  "every specification");

// The change from the schools case at fixed specifications (each method's end specifications, averaged), split by
// addition in the order long-run responses, rental assistance, capital core, capital block, then the enterprises:
// the receipt's re-key, the surplus at 1 and the enterprise returns. The engine parts are each addition alone less
// the old settings; the re-key is the old settings on the re-keyed models less the schools case (0: the receipt is
// still at 0); the capital parts are the return's components on the new case by part; the surplus is the receipt's
// cost on the new case.
const moves = {
  long_run_responses: atEnds(newEnds, (m, i) => lrCosts[m][i] - oldCosts[m][i]),
  rental_assistance: atEnds(newEnds, (m, i) => rentalRuns[m][i].cost_bn - oldCosts[m][i]),
  capital_core: atEnds(newEnds, (m, i) => capitalGroup(newRuns[m][i], "core")),
  capital_block: atEnds(newEnds, (m, i) => capitalGroup(newRuns[m][i], "block")),
  enterprise_rekey: atEnds(newEnds, (m, i) => oldCosts[m][i] - schoolsCosts[m][i]),
  enterprise_surplus_receipt: atEnds(newEnds, (m, i) => esCost(newRuns[m][i])),
  capital_enterprise: atEnds(newEnds, (m, i) => capitalGroup(newRuns[m][i], "enterprise")),
  total: atEnds(newEnds, (m, i) => newCosts[m][i] - schoolsCosts[m][i]),
};
const partsSum = Object.entries(moves).filter(([k]) => k !== "total").reduce((a, [, v]) => [a[0] + v[0], a[1] + v[1]], [0, 0]);
gate("the parts of the change add to the total at the end specifications", near(partsSum[0], moves.total[0], 1e-9)
  && near(partsSum[1], moves.total[1], 1e-9), f2(partsSum));
const bandMove = [C[0] - schools.main_case[0], C[1] - schools.main_case[1]];
gate("the band move equals the move at the fixed end specifications (same ends)", near(bandMove[0], moves.total[0], 1e-9)
  && near(bandMove[1], moves.total[1], 1e-9), f2(bandMove));
const dRekeyed = capRow(capCombined, "option D, enterprises at the spending lines' population key", "2pct/3pct");
const laneCols = { long_run_responses: "long_run_move", capital_core: "core_return", capital_block: "block_return",
  enterprise_surplus_receipt: "enterprise_surplus_move", capital_enterprise: "enterprise_returns" };
const colGap = worst(Object.entries(laneCols).flatMap(([k, col]) => { const ref = endCols(dRekeyed, col); return [moves[k][0] - ref[0], moves[k][1] - ref[1]]; }));
gate("each capital-lane part of the move is that lane's re-keyed option D column (combined_bands.csv, 6 decimals)", colGap < 1e-6,
  `max |diff| ${ex(colGap)}`);
// The re-key's effect: the case against the same case with the receipt at model.json's share.
const laneShareRuns = runs(specs, MAIN_PROFILE, MODELS_LANE);
const rekeyEffect = atEnds(newEnds, (m, i) => newCosts[m][i] - laneShareRuns[m][i].cost_bn);
const laneRekeyEffect = [0, 1].map((e) => pair(dRekeyed)[e] - pair(capRow(capCombined, "option D: long-run responses + core + block + enterprises", "2pct/3pct"))[e]);
gate("the re-key lowers the case by the capital lane's difference between its re-keyed and plain option D rows (1e-6)",
  near(rekeyEffect[0], laneRekeyEffect[0], 1e-6) && near(rekeyEffect[1], laneRekeyEffect[1], 1e-6), f2(rekeyEffect));
const publicHousing = atEnds(newEnds, (m, i) => byId(newRuns[m][i], "ent_housing_sl"));
// The re-key's move of the receipt itself: the group's enterprise_surplus amount against the schools case's. It is
// an amount, not a cost: the receipt is at 0 when the re-key applies, and at response 1 it is why the surplus costs
// national x the corrected share and not national x model.json's share.
const receiptMove = atEnds(newEnds, (m, i) => esRow(newRuns[m][i]).amount_bn - esSchools(m, i).amount_bn);
const esNational = MODEL.receipts.lines.find((l) => l.id === ENTERPRISE_LINE).national_bn;
gate("the re-key moves the group's enterprise_surplus receipt by national x (corrected share - model.json's share) at both ends",
  receiptMove.every((x) => near(x, esNational * (SHARE - kc.receipt_key[0]), 1e-12)), `${receiptMove.map((x) => x.toFixed(6)).join(" / ")}`);

// Profiles: the long-run lines follow line_responses only under the long-run profiles; the rental and receipt
// responses apply in every profile; the capital return follows each profile's responses.
console.log("\n[gates: profiles]");
const profileGap = {};
const profileRuns = {};
for (const pf of ["long_run_non_school_fixed", "proportional_reference"]) {
  const base = PROFILES[pf].base;
  const sc = MODELS.map((model) => S.MAIN_SPECS.map((spec) => S.cost(model, spec, base)));
  profileRuns[pf] = runs(specs, pf);
  const lrPart = pf === "proportional_reference" ? () => 0
    : (r) => LR_LINES.reduce((a, id) => a + responseOf(r.evaluation, id) * amount(r.evaluation, id), 0);
  profileGap[pf] = worst(profileRuns[pf].flatMap((xs, m) => xs.map((r, i) =>
    r.cost_bn - sc[m][i] - amount(r.evaluation, RENTAL) - lrPart(r) - r.capital.total_bn - esCost(r))));
}
gate("long_run_non_school_fixed = its schools-case profile + the long-run lines + rental assistance + capital + the enterprise receipt, at every specification",
  profileGap.long_run_non_school_fixed < 1e-9, `max |diff| ${ex(profileGap.long_run_non_school_fixed)}`);
gate("long_run_non_school_fixed charges no college capital (colleges fixed)", profileRuns.long_run_non_school_fixed.every((xs) =>
  xs.every((r) => byId(r, "college") === 0)), "every specification");
gate("the proportional reference keeps both lines at 1 and moves by rental assistance, capital and the enterprise receipt",
  profileGap.proportional_reference < 1e-9, `max |diff| ${ex(profileGap.proportional_reference)}`);
gate("the proportional reference charges the block at response 1", profileRuns.proportional_reference.every((xs) =>
  xs.every((r) => r.capital.components.filter((c) => c.group === "block").every((c) => c.response === 1))), "every block component");
const oldProfileRuns = runs(specs, "cbo_category_lag_non_school_full");
gate("the old main profile holds both lines and the block at 0 (moves by rental assistance, the enterprise receipt and the rest of the capital)",
  worst(oldProfileRuns.flatMap((xs, m) => xs.map((r, i) => r.cost_bn - oldCosts[m][i] - amount(r.evaluation, RENTAL) - r.capital.total_bn - esCost(r)))) < 1e-9
  && oldProfileRuns.every((xs) => xs.every((r) => capitalGroup(r, "block") === 0)), "every specification");
gate("in every profile the enterprise receipt and every enterprise component respond at 1 (the proportional reference included)",
  [newRuns, profileRuns.long_run_non_school_fixed, profileRuns.proportional_reference, oldProfileRuns].every((rs) => rs.every((xs) =>
    xs.every((r) => esRow(r).response === 1 && r.capital.components.filter((c) => c.group === "enterprise").every((c) => c.response === 1)))),
  "4 profiles x 2 methods x 64 specifications");

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
// The schools case's components, on the new case.
component("tax_block", "tax block: on-books share (low/central/high) x fill-in method",
  CASES.flatMap((c) => METHODS.map((m) => [`${c}/${m}`, evalPackage(c, m, {})])));
component("income_tax", "CBO income gradients: 2018/2019/2022 data, scaled or not by the stack's factor",
  [2018, 2019, 2022].flatMap((y) => [true, false].map((s) => [`${y}${s ? "" : " unscaled"}`, central({ year: y, scaled: s })])));
component("medical", "decision 2: medical-ethnicity specifications and the MCBS 65+ bound",
  ["plain", "winsor_p999", "two_part_lognormal", "pooled_excl_2020_2021", "pooled_cpi_all_items", "pooled_year_normalized"]
    .map((s) => [s, central({ medSpec: s })]).concat([["MCBS as truth", central({ mcbs: "mcbs_as_truth" })],
      ["MCBS precision-weighted", central({ mcbs: "precision_weighted" })]]));
component("ltss", "long-term-care carve-out: extremes of the lane's 960 combinations",
  LTSS_RANGE.map((v) => [String(v), central({ ltss: v })]));
component("education", "audit row 6 weight w (0.77/0.82) x school price k (low/high)",
  ["0.77", "0.82"].flatMap((w) => ["low", "preferred", "high"].map((k) => [`w ${w} k ${k}`, central({ w, k })])));
const benSe = Object.fromEntries(benefitSe.map((r) => [r.allocation, 1.96 * Number(r.se_bn)]));
component("benefits", "benefit keys: central +/- 1.96 SE (package_se.csv)",
  [-1, 1].map((s) => [`${s > 0 ? "+" : "-"}1.96 SE`, central({ benefitsDev: { personal: s * benSe.personal, shared: s * benSe.shared } })]));
component("justice", "row 7 on 2023 arrests; booking factor Texas only or Arizona only",
  [["row 7 2023", central({ row7: "2023" })], ["booking Texas", central({ booking: "texas" })], ["booking Arizona", central({ booking: "arizona" })]]);
for (const id of Object.keys(CONSTANTS)) {
  component(id, CONSTANTS[id].label, ["lo", "hi"].map((p) => [p, central({ constants: { [id]: p } })]));
}
component("finite_removal", "general government's removal response: r = b (fixed plus constant marginal cost); engine-key population share",
  [["r = b", central({ finite: false })], ["engine population key", central({ gg_s: "engine_population_key" })]]);
component("consumption_key", "consumption key: the lane's twelve saving-and-remittance specifications",
  CK_SPECS.map((s) => [s, central({ ck: s })]));
const schoolLow = central({ school_rule: "within_district" }), schoolLowAsResponse = central({ school_rule: "within_district_as_response" });
component("school_response", "school response: within-district elasticity 0.836 read over the removal (0.8489) or taken as the response",
  [["within district, finite r", schoolLow], ["within district, r = b", schoolLowAsResponse]]);
// The school low side, reported as the schools case reports it (rows school_within_district and
// school_within_district_as_response; summary school.*). The K-12 capital return follows the school response.
const schoolRuleEnds = (rule) => {
  const o = { school_rule: rule };
  const cm = costsOf(runs(specsFor(o), MAIN_PROFILE, METHODS.map((m) => modelFor("central", m, withCentral(o)))));
  return { band: bandOf(cm), ends: ends(cm) };
};
const schoolLowEnds = schoolRuleEnds("within_district"), schoolLowAsResponseEnds = schoolRuleEnds("within_district_as_response");
gate("the school low side's per-specification runs give its bands (1e-9)", [[schoolLowEnds, schoolLow], [schoolLowAsResponseEnds, schoolLowAsResponse]]
  .every(([x, b]) => near(x.band[0], b[0], 1e-9) && near(x.band[1], b[1], 1e-9)),
  `ends ${JSON.stringify(schoolLowEnds.ends)} / ${JSON.stringify(schoolLowAsResponseEnds.ends)}`);
// The parent's scratch run of this package (2026-09-27): 295.9441–362.9891 and 293.6711–360.9801.
gate("the school low side matches the parent's scratch run (1e-4)", near(schoolLow[0], 295.9441, 1e-4) && near(schoolLow[1], 362.9891, 1e-4)
  && near(schoolLowAsResponse[0], 293.6711, 1e-4) && near(schoolLowAsResponse[1], 360.9801, 1e-4), `${f2(schoolLow)}; ${f2(schoolLowAsResponse)}`);
// New: the response lane's sensitivities, each the whole case re-run with that variant's responses (the block's
// capital takes the variant's subfunction responses).
component("long_run_response", "long-run responses: r = b; within-state uncapped; federal fixed at the high end; across-state at the high end; held-at-zero lines at 1",
  Object.keys(LONG_RUN_VARIANTS).filter((v) => v !== "adopted").map((v) => [v, central({ long_run: v })]));
component("capital_rate", "return on public capital: 2% at both ends; 3% at both ends",
  [["2% at both ends", central({ rates: { low: 0.02, high: 0.02 } })], ["3% at both ends", central({ rates: { low: 0.03, high: 0.03 } })]]);
// The capital lane's definition variants (engine_components.json variants), each re-run at every specification
// like the other components. The enterprise option is the operator's choice, not a range component: option A is
// reported beside the range.
if (!CAP.variants || !Object.keys(CAP.variants).length) throw new Error("[BLOCKED] engine_components.json carries no variants");
component("capital_definition", "return on public capital: the capital lane's definition variants (engine_components.json variants), each re-run at every specification",
  Object.keys(CAP.variants).map((v) => [v, central({ capital_variant: v })]));
const sumLo = components.reduce((s, x) => [s[0] + x.lo[0], s[1] + x.lo[1]], [0, 0]);
const sumHi = components.reduce((s, x) => [s[0] + x.hi[0], s[1] + x.hi[1]], [0, 0]);
const rangeLowEnd = [C[0] + sumLo[0], C[0] + sumHi[0]], rangeHighEnd = [C[1] + sumLo[1], C[1] + sumHi[1]];
const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
const quadrature = [C[0] - rss(components.map((x) => x.lo[0])), C[1] + rss(components.map((x) => x.hi[1]))];

// Comparisons, the other profiles and the items beside the account.
const withRow3 = central({ incomeTax: "row3" });
const noFillIn = evalPackage("central", "audit_rules_alone", {});
const uncorrectedAtResponses = P.band(MODEL);
const schoolsRows = csvRows("main_case_schools_full_2026_09_26/derived/main_case_bands.csv");
const schoolsRow = (profile, variant) => {
  const r = schoolsRows.find((x) => x.profile === profile && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] the schools case's bands lack ${profile}/${variant}`);
  return [Number(r.cost_low_bn), Number(r.cost_high_bn)];
};
const otherProfiles = {};
for (const pf of Object.keys(PROFILES).filter((x) => x !== MAIN_PROFILE)) {
  otherProfiles[pf] = { schools_case: schoolsRow(PROFILES[pf].base, "adopted"),
    uncorrected_at_adopted_responses: P.band(MODEL, pf), adopted: central({ profile: pf }) };
}
const oldProfile = { profile: "cbo_category_lag_non_school_full", schools_case: schools.main_case,
  with_rental_assistance_capital_and_enterprises: central({ profile: "cbo_category_lag_non_school_full" }) };
const withoutCapital = central({ capital: false });
const rentalAlone = central({ long_run: false, capital: false, enterprise_receipt: 0 });
const optionA = central({ enterprises: "A" });
const optionARuns = runs(specsFor({ enterprises: "A" }));
const atModelShare = central({ enterprise_rekey: false });
const rentalAt0 = combinedRows["option D, enterprises at the spending lines' population key"];
const k12Pupil = central({ capital_variant: "k12_at_pupil_share" });
const at7 = central({ rates: { low: RATES.reported, high: RATES.reported } });
const runs7 = runs(specsFor({ rates: { low: RATES.reported, high: RATES.reported } }));
// Land: the capital lane's conversion per 10% of land-to-structure value (gaps.csv: core rows, "block: " rows and
// "enterprise: " rows), priced at this case's keys and responses: each component's land stock x rate x key x
// response at the end specifications. Every component of the case's definition must have a land row of its part.
const LAND_ROW = /^((block|enterprise): )?land at 10% of the structures charged: (\S+)$/;
const landRows = capGaps.filter((r) => LAND_ROW.test(r.item));
const landPart = (r) => r.item.match(LAND_ROW)[2] || "core";
const landStock = Object.fromEntries(landRows.map((r) => [r.item.match(LAND_ROW)[3], Number(r.national_base_bn) * Number(r.fee_factor)]));
const landMissing = CAP.components.filter((c) => !landRows.some((r) => r.item.match(LAND_ROW)[3] === c.id && landPart(r) === c.part)).map((c) => c.id);
const landUnknown = Object.keys(landStock).filter((id) => !CAP.components.some((c) => c.id === id));
gate("gaps.csv has one land row for every capital component, under its part (core, block, enterprise)", landRows.length === CAP.components.length
  && !landMissing.length && !landUnknown.length, `${landRows.length} rows; missing ${landMissing.join(" ") || "none"}; unknown ${landUnknown.join(" ") || "none"}`);
const landAt = (rs, m, i, pred) => rs[m][i].capital.components.filter(pred)
  .reduce((a, c) => a + landStock[c.id] * specs[i].rate * c.key * c.response, 0);
// The lane prices its land rows at the case ends on its own premises; the enterprise rows at model.json's receipt share.
const landLaneGap = worst(landRows.flatMap((r) => {
  const id = r.item.match(LAND_ROW)[3];
  const got = atEnds([CASE_ENDS, CASE_ENDS], (m, i) => landAt(laneShareRuns, m, i, (c) => c.id === id));
  return [got[0] - Number(r.group_2pct_spec48_bn), got[1] - Number(r.group_3pct_spec11_bn)];
}));
gate("the land rows priced on the capital lane's premises are its own (gaps.csv, 2% at spec 48 and 3% at spec 11, 6 decimals)",
  landLaneGap < 1e-6, `max |diff| ${ex(landLaneGap)}`);
const land = {
  per_10pct_bn: atEnds(newEnds, (m, i) => landAt(newRuns, m, i, () => true)),
  by_part_per_10pct_bn: Object.fromEntries(PARTS.map((g) => [g, atEnds(newEnds, (m, i) => landAt(newRuns, m, i, (c) => c.group === g))])),
  note: "[GAP] BEA measures produced assets only; the capital lane's conversion per 10% of land-to-structure value (gaps.csv core, block and enterprise rows), priced at this case's keys and responses at the end specifications (2% low, 3% high; enterprise land at the corrected population share); not an estimate" };
// Rental assistance against the enterprise surplus under option D: a federal payment to a public housing authority
// is charged in housing_subsidies at the rental key and credited inside the surplus at the population key.
const rentalKey = atEnds(newEnds, (m, i) => amount(newRuns[m][i].evaluation, RENTAL) / national(newRuns[m][i].evaluation, RENTAL));
const rentalNational = national(newRuns[0][0].evaluation, RENTAL);
const overlap = { rental_key: rentalKey, population_share: SHARE, rental_national_bn: rentalNational,
  upper_bound_bn: rentalKey.map((k) => rentalNational * (SHARE - k)),
  netted_bn: 0,
  note: "no double charge: NIPA's current surplus of government enterprises includes subsidies received from other levels of government (BEA glossary; MP-5), so under option D a federal payment to a public housing authority is charged in housing_subsidies at the rental key and credited inside the enterprise_surplus receipt at the population share. They offset except for the keys, a mismatch in the group's favour: upper_bound_bn if all of the line went to enterprises; public housing's operating subsidies alone (about $5bn national [TRAINING-DATA]) make it about $0.2bn [INFERENCE]. Not netted." };
const beside = {
  rate_7pct: { band_bn: at7, return_at_end_specifications_bn: atEnds(newEnds, (m, i) => runs7[m][i].capital.total_bn),
    note: "A-4 (2003)'s private-capital rate on every component, enterprises included, reported beside the account only (operator, 2026-09-27 15:21 JST)" },
  land_per_10pct_of_land_to_structure_value: land,
  enterprises_out_option_A: { band_bn: optionA, change_at_fixed_specifications_bn: atEnds(newEnds, (m, i) => optionARuns[m][i].cost_bn - newCosts[m][i]),
    note: "option A, a labelled variant beside the range: no enterprise capital and the enterprise_surplus receipt at 0; everything else as the case" },
  rental_assistance_at_0: { band_bn: rentalAt0, note: "rental assistance at 0; public housing's capital stays (an enterprise under option D); the capital lane's re-keyed option D row" },
  congestion: { source: "service_response_long_run_2026_09_27/derived/net_change.json", sha256: P.sha256("service_response_long_run_2026_09_27/derived/net_change.json"),
    before_bn: congestion.b1_lanes_fixed_bn,
    low_end: { congestion_bn: congestion.by_band_end.low.congestion_bn, change_bn: congestion.by_band_end.low.congestion_change_bn,
      range_bn: congestion.by_band_end.low.congestion_range_bn },
    high_end: { congestion_bn: congestion.by_band_end.high.congestion_bn, change_bn: congestion.by_band_end.high.congestion_change_bn,
      range_bn: congestion.by_band_end.high.congestion_range_bn },
    note: congestion.note },
};

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the payload]");
const nSchools = schoolsPayload.edits.length;
const added = payload.edits.slice(nSchools);
const esModel = MODEL.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
const refEdit = added.find((e) => e.scenario === MODEL.receipts.reference);
gate("the payload is the schools case's lines and edits, then the enterprise receipt's re-key (one shift carried to the eight incidence rules) and nothing else",
  JSON.stringify(payload.lines) === JSON.stringify(schoolsPayload.lines)
  && JSON.stringify(payload.edits.slice(0, nSchools)) === JSON.stringify(schoolsPayload.edits)
  && added.length === MODEL.receipts.scenarios.length
  && added.every((e, j) => e.side === "receipt" && e.line === ENTERPRISE_LINE && e.scenario === MODEL.receipts.scenarios[j]),
  `${nSchools} + ${added.length} edits`);
gate("each rule's re-key edit is the reference rule's, scaled by that rule's share of the line over the reference's (expand())",
  worst(added.flatMap((e) => ALLOCS.map((a) => e.by[a] - refEdit.by[a] * esModel.cells[e.scenario][a].target_bn
    / esModel.cells[MODEL.receipts.reference][a].target_bn))) < 1e-15, "8 rules x 2 allocations");
const expectedEdit = esModel.national_bn * (kc.spending_population_key[0] - kc.receipt_key[0]);
gate("the re-key's size: national x (spending population key - receipt key), both from the capital lane's key_consistency (1e-12), under $0.5bn",
  ALLOCS.every((a) => near(refEdit.by[a], expectedEdit, 1e-12)) && Math.abs(expectedEdit) < 0.5,
  `+$${refEdit.by.personal.toFixed(6)}bn on ${esModel.national_bn}bn national`);
gate("meta.responses keeps the schools case's general-government and school responses",
  JSON.stringify(payload.meta.responses.general_government) === JSON.stringify(schoolsPayload.meta.responses.general_government)
  && JSON.stringify(payload.meta.responses.school) === JSON.stringify(schoolsPayload.meta.responses.school), "deep-equal");
gate(`meta records option ${ENTERPRISES}, the receipt at 1 and the re-key`, payload.meta.capital_return.enterprises === ENTERPRISES
  && payload.meta.responses[ENTERPRISE_LINE].low === 1 && payload.meta.responses[ENTERPRISE_LINE].high === 1
  && payload.meta.enterprise_receipt_rekey.edits === added.length
  && ALLOCS.every((a) => payload.meta.enterprise_receipt_rekey.reference_edit_bn[a] === refEdit.by[a]), "capital_return.enterprises, responses, enterprise_receipt_rekey");
// An independent path: the engine, model.json and corrections.json alone. The specification grid, the state, the
// responses and the capital return are rebuilt from meta; nothing comes from the packages.
function independentCosts(pay) {
  const fisc = path.join(HERE, "..");
  const Eng = require(path.join(fisc, "assumption_explorer_2026_09_21", "engine.js"));
  const model = JSON.parse(fs.readFileSync(path.join(fisc, "assumption_explorer_2026_09_21", "derived", "model.json"), "utf8"));
  const m = Eng.applyCorrections(model, { lines: pay.lines, edits: pay.edits });
  const R = pay.meta.responses, K = pay.meta.capital_return;
  const syn = Object.fromEntries(pay.lines.map((l) => [l.response_class, l.id]));
  const row = (ev, id) => ev.spending.find((l) => l.id === id);
  const receipt = (ev, id) => ev.receipts.find((l) => l.id === id);
  const out = [];
  for (const allocation of ["personal", "shared"]) for (const normalization of ["cash", "gdp"])
    for (const share of Eng.schoolShareBounds(model)) for (const school of [R.school.growth, R.school.decline])
      for (const [rd, gg] of [["low", R.general_government.low], ["high", R.general_government.high]])
        for (const uc of ["uninsured_use_low", "uninsured_use_high"]) {
          const s = Eng.defaultState(m);
          s.allocation = allocation; s.receipt_scenario = m.receipts.reference; s.production.normalization = normalization;
          s.count_production = true; s.general_government_response = gg;
          s.key_override = { public_order_safety: "use", medicaid_and_chip_other_medical: uc };
          s.response_override = { education_services: share * school + (1 - share), public_order_safety: 1, health_services: 1,
            income_security_services: 1, housing_community_services: 1,
            [syn.education_school_part]: share * school, [syn.education_other_part]: 1 - share, [syn.correction_constant]: 1 };
          for (const id of ["economic_affairs_services", "recreation_culture", "housing_subsidies"]) s.response_override[id] = R[id][rd];
          s.response_override[R.enterprise_surplus.override] = R.enterprise_surplus[rd];
          const ev = Eng.evaluate(m, s);
          let capital = 0;
          for (const c of K.components) {
            const k = c.key, r = c.response;
            let key, response;
            if (k.kind === "constant") key = k.value;
            else if (k.kind === "receipt_amount_over_national") key = receipt(ev, k.line).amount_bn / receipt(ev, k.line).national_bn;
            else if (k.kind === "lines_amount_over_national") key = k.numerator_lines.reduce((a, id) => a + row(ev, id).amount_bn, 0) / row(ev, k.denominator_line).national_bn;
            else throw new Error("independent path: unknown key kind " + k.kind);
            if (r.kind === "fixed") response = r.value;
            else if (r.kind === "enterprises_switch") response = r.values[K.enterprises];
            else if (r.kind === "line_response") response = row(ev, r.line).response;
            else if (r.kind === "line_response_over_share") response = row(ev, r.line).response / (r.share === "school" ? share : 1 - share);
            else if (r.kind === "long_run_subfunction") response = R[r.line].subfunctions.find((x) => x.id === r.subfunction)[rd];
            else throw new Error("independent path: unknown response kind " + r.kind);
            capital += c.stock_charged_bn * K.rates[rd] * key * response;
          }
          out.push(-ev.welfare_bn + capital);
        }
  return out;
}
const independent = independentCosts(JSON.parse(JSON.stringify(payload)));
const methodMean = specs.map((_, i) => mean(newCosts.map((xs) => xs[i])));
const indGap = worst(independent.map((x, i) => x - methodMean[i]));
gate("independent path: engine + model.json + corrections.json give the case at every specification (1e-9)",
  independent.length === 64 && indGap < 1e-9, `max |diff| ${ex(indGap)} against the two methods' mean`);
const receiptsTotal = (m) => Object.fromEntries(ALLOCS.map((a) =>
  [a, m.receipts.lines.reduce((s, l) => s + l.cells[m.receipts.reference][a].target_bn, 0)]));
const groupReceipts = Object.assign({}, schools.group_receipts_bn, { adopted_2026_09_26_schools: schools.group_receipts_bn.adopted,
  adopted: receiptsTotal(payloadModel) });
gate("the group's receipts move by the re-key alone (payload, reference rule)", ALLOCS.every((a) =>
  near(groupReceipts.adopted[a] - schools.group_receipts_bn.adopted[a], refEdit.by[a], 1e-9)), JSON.stringify(groupReceipts.adopted));
// The payload's receipt and spending edits against the uncorrected model at this case's responses (the capital
// return follows the edits through the keys; the re-key is a receipt edit).
const pBand = (edits) => P.band(Engine.applyCorrections(MODEL, { lines: payload.lines, edits }));
const recOnly = pBand(payload.edits.filter((e) => e.side === "receipt"));
const spOnly = pBand(payload.edits.filter((e) => e.side !== "receipt"));
const sides = { receipts: [recOnly[0] - uncorrectedAtResponses[0], recOnly[1] - uncorrectedAtResponses[1]],
  spending: [spOnly[0] - uncorrectedAtResponses[0], spOnly[1] - uncorrectedAtResponses[1]] };
const payloadBand = pBand(payload.edits);
gate("corrections.json reproduces the case (1e-4, the methods' edits averaged)", near(payloadBand[0], C[0], 1e-4) && near(payloadBand[1], C[1], 1e-4),
  f2(payloadBand));
gate("the two sides add to the payload's band", near(sides.receipts[0] + sides.spending[0], payloadBand[0] - uncorrectedAtResponses[0], 1e-6)
  && near(sides.receipts[1] + sides.spending[1], payloadBand[1] - uncorrectedAtResponses[1], 1e-6), `${f2(sides.receipts)} + ${f2(sides.spending)}`);

// ---------------------------------------------------------------------------------------------------
if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
const fx = (x) => x.toFixed(4);
const full = (x) => (typeof x === "number" ? String(x) : x);
const endSpecs = newEnds.map((e, m) => ({ method: METHODS[m], low_end: Object.assign({ index: e[0] }, specs[e[0]]),
  high_end: Object.assign({ index: e[1] }, specs[e[1]]) }));
const lineAtEnds = Object.fromEntries(LR_LINES.concat([RENTAL]).map((id) => [id, {
  response: atEnds(newEnds, (m, i) => responseOf(newRuns[m][i].evaluation, id)),
  group_amount_bn: atEnds(newEnds, (m, i) => amount(newRuns[m][i].evaluation, id)),
  added_bn: atEnds(newEnds, (m, i) => responseOf(newRuns[m][i].evaluation, id) * amount(newRuns[m][i].evaluation, id)) }]));
const capitalAtEnds = {
  rates: { low: RATES.low, high: RATES.high },
  total_bn: atEnds(newEnds, (m, i) => newRuns[m][i].capital.total_bn),
  by_level_bn: Object.fromEntries(["state_local", "federal"].map((lv) => [lv, atEnds(newEnds, (m, i) => capitalWhere(newRuns[m][i], (c) => c.level === lv))])),
  by_part_bn: Object.fromEntries(PARTS.map((g) => [g, atEnds(newEnds, (m, i) => capitalGroup(newRuns[m][i], g))])),
  by_component: Object.fromEntries(CAP.components.map((c) => [c.id, { label: c.label, part: c.part, level: c.level,
    stock_charged_bn: c.stock_charged_bn,
    key: atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.find((x) => x.id === c.id).key),
    response: atEnds(newEnds, (m, i) => newRuns[m][i].capital.components.find((x) => x.id === c.id).response),
    return_bn: atEnds(newEnds, (m, i) => byId(newRuns[m][i], c.id)) }])),
  k12_key: { account_key: k12Keys, pupil_share: CAP.k12_keys_at_case_ends.spec48.pupil_share, pupil_share_minus_account_bn: k12Diff,
    note: "the case and the capital lane's own definition key K-12 by the account's school key from the evaluation; the lane's variant k12_at_pupil_share uses the pupil share, which is higher, so the return is higher by pupil_share_minus_account_bn at the end specifications" },
};
fs.mkdirSync(OUT, { recursive: true });
const row = (pf, variant, b, r) => [pf, variant, fx(b[0]), fx(b[1]), r ? fx(r[0]) : "", r ? fx(r[1]) : ""].join(",");
const bandsCsv = ["profile,variant,cost_low_bn,cost_high_bn,range_low_bn,range_high_bn",
  row(MAIN_PROFILE, "first_year_response", firstYear),
  row(MAIN_PROFILE, "schools_case", schools.main_case, [schools.range.low_end[0], schools.range.high_end[1]]),
  row(MAIN_PROFILE, "uncorrected_at_adopted_responses", uncorrectedAtResponses),
  row(MAIN_PROFILE, "long_run_responses_alone", lrOnlyBand),
  row(MAIN_PROFILE, "rental_assistance_alone", rentalAlone),
  row(MAIN_PROFILE, "long_run_responses_and_capital_return_option_a", combinedRows["option A: long-run responses + core + block"]),
  row(MAIN_PROFILE, "without_capital_return", withoutCapital),
  row(MAIN_PROFILE, "school_within_district", schoolLow),
  row(MAIN_PROFILE, "school_within_district_as_response", schoolLowAsResponse),
  row(MAIN_PROFILE, "adopted", C, [rangeLowEnd[0], rangeHighEnd[1]]),
  row(MAIN_PROFILE, "enterprises_out_option_a", optionA),
  row(MAIN_PROFILE, "enterprise_receipt_at_model_json_share", atModelShare),
  row(MAIN_PROFILE, "capital_return_at_7pct", at7),
  row(MAIN_PROFILE, "rental_assistance_at_0", rentalAt0),
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
  .concat(CAP.components.map((c) => `capital_${c.id}_bn`))
  .concat(LR_LINES.concat([RENTAL]).flatMap((id) => [`response_${id}`, `group_${id}_bn`]));
const perSpec = [perHead.join(",")].concat(METHODS.flatMap((meth, m) => specs.map((s, i) => {
  const r = newRuns[m][i];
  return [meth, i, s.allocation, s.normalization, s.share, s.school, s.gg, s.uc, s.justice, s.reading, s.rate, s.enterprises,
    r.cost_bn, -r.evaluation.welfare_bn, r.capital.total_bn,
    capitalWhere(r, (c) => c.level === "state_local"), capitalWhere(r, (c) => c.level === "federal"),
    capitalGroup(r, "core"), capitalGroup(r, "block"), capitalGroup(r, "enterprise"), esRow(r).response, esRow(r).amount_bn, esCost(r)]
    .concat(CAP.components.map((c) => byId(r, c.id)))
    .concat(LR_LINES.concat([RENTAL]).flatMap((id) => [responseOf(r.evaluation, id), amount(r.evaluation, id)])).map(full).join(",");
})));
const summary = {
  lane: "main_case_long_run_2026_09_27",
  decision: "decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md",
  adopted_2026_09_23: schools.adopted_2026_09_23, adopted_2026_09_24: schools.adopted_2026_09_24,
  adopted_2026_09_26: schools.adopted_2026_09_26, adopted_2026_09_26_schools: schools.main_case,
  first_year_response: firstYear, schools_case: schools.main_case,
  uncorrected_at_adopted_responses: uncorrectedAtResponses, without_capital_return: withoutCapital,
  main_case: C, change: bandMove,
  change_at_fixed_specifications: {
    long_run_responses: moves.long_run_responses, rental_assistance: moves.rental_assistance,
    capital_core: moves.capital_core, capital_block: moves.capital_block,
    enterprise_rekey: moves.enterprise_rekey, enterprise_rekey_receipt_move: receiptMove,
    enterprise_surplus_receipt: moves.enterprise_surplus_receipt, capital_enterprise: moves.capital_enterprise,
    total: moves.total,
    of_which_public_housing: publicHousing,
    enterprise_rekey_against_model_json_share: rekeyEffect,
    note: "each method's end specifications (48 low, 11 high in both), averaged, in the order long-run responses, rental assistance, capital core, capital block, then the enterprises (the receipt's re-key, the surplus at 1, the enterprise returns). long_run_responses and rental_assistance are each addition alone less the old settings (engine, capital off); enterprise_rekey is the old settings on the re-keyed models less the schools case, 0 because the receipt is still at 0; capital_core, capital_block and capital_enterprise are the return's parts on the new case; enterprise_surplus_receipt is the receipt's cost at response 1. These parts add to total. Not in the sum: enterprise_rekey_receipt_move (the receipt's own move under the re-key, the group's enterprise_surplus amount against the schools case's; an amount, not a cost: at response 1 it is why the surplus costs national x the corrected share and not national x model.json's share), of_which_public_housing (inside capital_enterprise) and enterprise_rekey_against_model_json_share (the case less the same case with the receipt at model.json's share). change is the difference of band ends from the schools case, equal to total because the ends do not move" },
  end_specifications: endSpecs,
  lines_at_end_specifications: lineAtEnds,
  capital_at_end_specifications: capitalAtEnds,
  enterprises: { option: ENTERPRISES, allowed_by_file: ENTERPRISES_ALLOWED, receipt_response: 1,
    receipt_at_end_specifications: { group_amount_bn: atEnds(newEnds, (m, i) => esRow(newRuns[m][i]).amount_bn),
      national_bn: esModel.national_bn, cost_bn: moves.enterprise_surplus_receipt,
      move_from_the_schools_case_bn: receiptMove },
    returns_at_end_specifications_bn: moves.capital_enterprise, public_housing_return_bn: publicHousing,
    receipt_rekey: payload.meta.enterprise_receipt_rekey,
    rekey_effect_at_fixed_specifications_bn: rekeyEffect,
    option_A_band_bn: optionA, at_model_json_share_band_bn: atModelShare,
    capital_lane_rows_before_rental_assistance: Object.fromEntries(Object.entries(combinedRows).map(([k, v]) => [k, v])),
    overlap_with_rental_assistance: overlap,
    interest: "not added: NIPA's enterprise surplus excludes interest, which sits in the account's interest row, held at 0. BEA, Government Transactions (NIPA Methodology Paper 5, 2005), p. I-16: \"Interest received and paid are ignored in the calculation of the current surplus of government enterprises.\"",
    proportional_reference: "the receipt responds at 1 and every enterprise component at 1 in every profile, the proportional reference included" },
  school: { rules: P.RULES, within_district: schoolLow, within_district_as_response: schoolLowAsResponse,
    end_specifications: { average: newEnds, within_district: schoolLowEnds.ends, within_district_as_response: schoolLowAsResponseEnds.ends },
    note: "the schools case's low side on this case: every specification re-run with that school rule (the K-12 capital return follows the school response); end_specifications are [low end, high end] per fill-in method",
    sign_break_even: "derived/sign_reversal.csv (sign_reversal.cjs): schools move with the common share" },
  rental_assistance: { group_amount_by_method_bn: Object.fromEntries(METHODS.map((m, k) => [m, Object.fromEntries(ALLOCS.map((a, j) => [a, rentalAmount[k][j]]))])),
    uncorrected_group_amount_bn: Object.fromEntries(ALLOCS.map((a, j) => [a, rentalUncorrected[j]])),
    note: "the adopted corrections re-key the line (tax-records stack and administrative benefit keys), so the move is the corrected amount, not the uncorrected $7.54bn",
    overlap_netted_bn: 0 },
  responses: P.RESPONSES,
  range: { low_end: rangeLowEnd, high_end: rangeHighEnd, overall: [rangeLowEnd[0], rangeHighEnd[1]], quadrature,
    note: "every component re-runs the whole case at every specification; the band's ends are minima and maxima over the specifications; option A and 7% are beside the range, not in it" },
  other_profiles: otherProfiles, old_main_profile: oldProfile,
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn,
  each_addition: { long_run_responses_alone: lrOnlyBand, rental_assistance_alone: rentalAlone,
    long_run_responses_and_capital_return_option_a: combinedRows["option A: long-run responses + core + block"],
    long_run_responses_capital_return_and_enterprises: rentalAt0, core_return_alone_on_the_schools_case: laneCore },
  beside_the_account: beside,
  by_side_vs_uncorrected_at_adopted_responses: sides,
  group_receipts_bn: groupReceipts,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi,
    variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
};
fs.writeFileSync(path.join(OUT, "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "components.csv"), compCsv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "corrections.json"), JSON.stringify(payload, null, 1) + "\n");

console.log("\n[result]");
console.log(`  schools case                    ${f2(schools.main_case)}`);
console.log(`  long-run responses alone        ${f2(lrOnlyBand)}`);
console.log(`  without the capital return      ${f2(withoutCapital)}`);
console.log(`  option A (beside)               ${f2(optionA)}`);
console.log(`  school within district          ${f2(schoolLow)}; as the response ${f2(schoolLowAsResponse)}`);
console.log(`  main case                       ${f2(C)}  ends ${newEnds.map((e) => e.join("/")).join(", ")}`);
for (const [k, v] of Object.entries(moves)) console.log(`    change at fixed specs, ${k.padEnd(26)} ${v[0].toFixed(4)} / ${v[1].toFixed(4)}`);
console.log(`    receipt moved by the re-key ${receiptMove[0].toFixed(4)} / ${receiptMove[1].toFixed(4)}; re-key against model.json's share ${rekeyEffect[0].toFixed(4)} / ${rekeyEffect[1].toFixed(4)}; public housing ${publicHousing[0].toFixed(4)} / ${publicHousing[1].toFixed(4)}`);
console.log(`  K-12 pupil share minus account key ${f2(k12Diff)}`);
console.log(`  at 7% (beside)                  ${f2(at7)}`);
console.log(`  range                           ${rangeLowEnd[0].toFixed(1)}–${rangeHighEnd[1].toFixed(1)} (quadrature ${quadrature[0].toFixed(1)}–${quadrature[1].toFixed(1)})`);
for (const [pf, v] of Object.entries(otherProfiles)) console.log(`  ${pf.padEnd(31)} ${f2(v.schools_case)} -> ${f2(v.adopted)}`);
console.log(`  old main profile, with the additions ${f2(oldProfile.with_rental_assistance_capital_and_enterprises)}`);
for (const x of components) console.log(`    range: ${x.name.padEnd(18)} low end ${x.lo[0].toFixed(2)}..+${x.hi[0].toFixed(2)}  high end ${x.lo[1].toFixed(2)}..+${x.hi[1].toFixed(2)}`);
console.log("all gates passed");
