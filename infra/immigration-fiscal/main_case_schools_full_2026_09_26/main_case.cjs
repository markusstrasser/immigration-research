/* The main case adopted on 2026-09-26, second decision that day: the September 26 case with schools
 * charged at their full average cost per pupil, a school response of 1
 * (decisions/2026-09-26-main-case-schools-full-cost.md).
 *
 * Base: the September 26 case (main_case_2026_09_26, $200.9180–245.6949bn), reproduced to 1e-4 through
 * its own package before any change. It stays as the one-year budget scenario. package.cjs holds the
 * definitions; only the school response changes (0.6522/0.6813 -> 1). The payload's edits are the
 * September 26 edits, and meta.responses.school changes.
 *
 * The range takes the September 26 components on the new case, with two changes:
 * - the finite-removal component keeps general government's functional form only (r = b; the engine
 *   key's population share): at a response of 1 schools save 1 under any functional form or pupil share;
 * - a school-response component: the within-district elasticity 0.836 read over the removal (0.8489) or
 *   taken as the response (0.836). No measured response above 1 is priced, so its upper side is 0.
 *
 * Gates (exit 1 on failure): the September 26 case, its payload and its other profiles reproduce; the
 * school option equals editing the specifications' school field directly; the proportional reference,
 * which already charged schools at 1, does not move; the payload's edits equal September 26's and
 * reproduce the new case; the group's receipts do not move.
 * Run from anywhere: node main_case.cjs -> derived/main_case_bands.csv, components.csv, summary.json and,
 * only when every gate passes, corrections.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("./package.cjs");
const { P26, Engine, MODEL, HERE, ALLOCS, PROFILES, MAIN_PROFILE, CASES, METHODS, STACKS, CONSTANTS, LTSS_RANGE,
  CK_SPECS, gateState, gate, near, f2, csvRows, readJson, mean2, bandFor, evalPackage, central, correctionsPayload,
  responsesFor, benefitSe, MAIN_SPECS, band } = P;

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the September 26 case]");
const rows26 = csvRows("main_case_2026_09_26/derived/main_case_bands.csv");
const row26 = (profile, variant) => {
  const r = rows26.find((x) => x.profile === profile && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] main_case_2026_09_26 bands lack ${profile}/${variant}`);
  return r;
};
const pair = (r) => [Number(r.cost_low_bn), Number(r.cost_high_bn)];
const pub26 = Object.fromEntries(Object.keys(PROFILES).map((pf) => [pf, pair(row26(pf, "adopted"))]));
const old = P26.central({});
gate("the September 26 package reproduces its adopted case", near(old[0], pub26[MAIN_PROFILE][0], 1e-4)
  && near(old[1], pub26[MAIN_PROFILE][1], 1e-4), f2(old));
const oneYear = central({ school_rule: "one_year" });
gate("this package's one-year rule is the September 26 case", near(oneYear[0], old[0], 1e-9) && near(oneYear[1], old[1], 1e-9), f2(oneYear));
const pay26 = readJson("main_case_2026_09_26/derived/corrections.json");
gate("the September 26 corrections.json is its package's payload", JSON.stringify(P26.correctionsPayload()) === JSON.stringify(pay26), "deep-equal");
for (const profile of Object.keys(PROFILES).filter((x) => x !== MAIN_PROFILE)) {
  const b = P26.central({ profile });
  gate(`${profile}: the September 26 package reproduces its band`, near(b[0], pub26[profile][0], 1e-4) && near(b[1], pub26[profile][1], 1e-4), f2(b));
}

console.log("\n[gates: the new case]");
const C = central({});
// An independent path: the September 26 specifications with their school field edited directly.
const direct = mean2(...METHODS.map((m) => {
  const oo = Object.assign({}, P26.CENTRAL);
  const shifts = P26.packageShifts(STACKS[`row4+status_state_aware|central|${m}`], "central", m, oo);
  return bandFor(P26.build(shifts, oo), oo.profile, P26.MAIN_SPECS.map((s) => Object.assign({}, s, { school: 1 })));
}));
gate("the school option equals editing the specifications directly", near(C[0], direct[0], 1e-9) && near(C[1], direct[1], 1e-9),
  `${f2(C)} vs ${f2(direct)}`);
const prop = central({ profile: "proportional_reference" });
gate("the proportional reference, which charged schools at 1 already, does not move",
  near(prop[0], pub26.proportional_reference[0], 1e-4) && near(prop[1], pub26.proportional_reference[1], 1e-4), f2(prop));
const low = central({ school_rule: "within_district" });
const lowAsResponse = central({ school_rule: "within_district_as_response" });
gate("the case rises with the school response (0.836 < 0.8489 < 1)", lowAsResponse[0] < low[0] && low[0] < C[0]
  && lowAsResponse[1] < low[1] && low[1] < C[1], `${f2(lowAsResponse)} < ${f2(low)} < ${f2(C)}`);
// The school line at full cost, and the part of it each lower response leaves unfunded.
const noSchools = P26.central({ school_response: [0, 0] });
const schoolLine = [C[0] - noSchools[0], C[1] - noSchools[1]];
const unfunded = { one_year: [C[0] - old[0], C[1] - old[1]], within_district: [C[0] - low[0], C[1] - low[1]],
  within_district_as_response: [C[0] - lowAsResponse[0], C[1] - lowAsResponse[1]] };

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
// The September 26 components, on the new case.
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
component("school_response", "school response: within-district elasticity 0.836 read over the removal (0.8489) or taken as the response",
  [["within district, finite r", low], ["within district, r = b", lowAsResponse]]);
const sumLo = components.reduce((s, x) => [s[0] + x.lo[0], s[1] + x.lo[1]], [0, 0]);
const sumHi = components.reduce((s, x) => [s[0] + x.hi[0], s[1] + x.hi[1]], [0, 0]);
const rangeLowEnd = [C[0] + sumLo[0], C[0] + sumHi[0]], rangeHighEnd = [C[1] + sumLo[1], C[1] + sumHi[1]];
const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
const quadrature = [C[0] - rss(components.map((x) => x.lo[0])), C[1] + rss(components.map((x) => x.hi[1]))];

// Comparisons and the other two service profiles.
const withRow3 = central({ incomeTax: "row3" });
const noFillIn = evalPackage("central", "audit_rules_alone", {});
const uncorrectedAtResponses = band(MODEL);
const otherProfiles = {};
for (const profile of Object.keys(PROFILES).filter((x) => x !== MAIN_PROFILE)) {
  otherProfiles[profile] = { sept23: pair(row26(profile, "adopted_2026_09_23")), sept24: pair(row26(profile, "adopted_2026_09_24")),
    sept26: pub26[profile], uncorrected_at_adopted_responses: band(MODEL, profile), adopted: central({ profile }) };
}

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the payload]");
const payload = correctionsPayload();
gate("the payload's lines and edits are September 26's", JSON.stringify(payload.lines) === JSON.stringify(pay26.lines)
  && JSON.stringify(payload.edits) === JSON.stringify(pay26.edits), "deep-equal");
gate("meta.responses: schools 1/1, general government September 26's", payload.meta.responses.school.growth === 1
  && payload.meta.responses.school.decline === 1
  && JSON.stringify(payload.meta.responses.general_government) === JSON.stringify(pay26.meta.responses.general_government),
  JSON.stringify(payload.meta.responses.school));
const pBand = (edits) => band(Engine.applyCorrections(MODEL, { lines: payload.lines, edits }));
const payloadBand = pBand(payload.edits);
gate("corrections.json reproduces the adopted case", near(payloadBand[0], C[0], 1e-4) && near(payloadBand[1], C[1], 1e-4), f2(payloadBand));
const recOnly = pBand(payload.edits.filter((e) => e.side === "receipt"));
const spOnly = pBand(payload.edits.filter((e) => e.side !== "receipt"));
const sides = { receipts: [recOnly[0] - uncorrectedAtResponses[0], recOnly[1] - uncorrectedAtResponses[1]],
  spending: [spOnly[0] - uncorrectedAtResponses[0], spOnly[1] - uncorrectedAtResponses[1]] };
gate("the two sides add to the package", near(sides.receipts[0] + sides.spending[0], C[0] - uncorrectedAtResponses[0], 1e-6)
  && near(sides.receipts[1] + sides.spending[1], C[1] - uncorrectedAtResponses[1], 1e-6), `${f2(sides.receipts)} + ${f2(sides.spending)}`);
const receiptsTotal = (m) => Object.fromEntries(ALLOCS.map((a) =>
  [a, m.receipts.lines.reduce((s, l) => s + l.cells[m.receipts.reference][a].target_bn, 0)]));
const s26 = readJson("main_case_2026_09_26/derived/summary.json");
const groupReceipts = Object.assign({}, s26.group_receipts_bn, { adopted_2026_09_26: s26.group_receipts_bn.adopted,
  adopted: receiptsTotal(Engine.applyCorrections(MODEL, payload)) });
gate("the group's receipts do not move (the school response is spending)", ALLOCS.every((a) =>
  near(groupReceipts.adopted[a], s26.group_receipts_bn.adopted[a], 1e-9)), JSON.stringify(groupReceipts.adopted));

// ---------------------------------------------------------------------------------------------------
const fx = (x) => x.toFixed(4);
fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
const range26 = row26(MAIN_PROFILE, "adopted");
const bandsCsv = ["profile,variant,cost_low_bn,cost_high_bn,range_low_bn,range_high_bn",
  `${MAIN_PROFILE},adopted_2026_09_23,${row26(MAIN_PROFILE, "adopted_2026_09_23").cost_low_bn},${row26(MAIN_PROFILE, "adopted_2026_09_23").cost_high_bn},,`,
  `${MAIN_PROFILE},adopted_2026_09_24,${row26(MAIN_PROFILE, "adopted_2026_09_24").cost_low_bn},${row26(MAIN_PROFILE, "adopted_2026_09_24").cost_high_bn},,`,
  `${MAIN_PROFILE},adopted_2026_09_26,${fx(old[0])},${fx(old[1])},${range26.range_low_bn},${range26.range_high_bn}`,
  `${MAIN_PROFILE},uncorrected_at_adopted_responses,${fx(uncorrectedAtResponses[0])},${fx(uncorrectedAtResponses[1])},,`,
  `${MAIN_PROFILE},school_within_district,${fx(low[0])},${fx(low[1])},,`,
  `${MAIN_PROFILE},school_within_district_as_response,${fx(lowAsResponse[0])},${fx(lowAsResponse[1])},,`,
  `${MAIN_PROFILE},adopted,${fx(C[0])},${fx(C[1])},${fx(rangeLowEnd[0])},${fx(rangeHighEnd[1])}`,
  `${MAIN_PROFILE},audit_row3_instead_of_cbo_income_tax,${fx(withRow3[0])},${fx(withRow3[1])},,`,
  `${MAIN_PROFILE},no_fill_in_correction,${fx(noFillIn[0])},${fx(noFillIn[1])},,`]
  .concat(Object.entries(otherProfiles).flatMap(([pf, v]) => [
    `${pf},adopted_2026_09_23,${fx(v.sept23[0])},${fx(v.sept23[1])},,`,
    `${pf},adopted_2026_09_24,${fx(v.sept24[0])},${fx(v.sept24[1])},,`,
    `${pf},adopted_2026_09_26,${fx(v.sept26[0])},${fx(v.sept26[1])},,`,
    `${pf},uncorrected_at_adopted_responses,${fx(v.uncorrected_at_adopted_responses[0])},${fx(v.uncorrected_at_adopted_responses[1])},,`,
    `${pf},adopted,${fx(v.adopted[0])},${fx(v.adopted[1])},,`]));
fs.writeFileSync(path.join(HERE, "derived", "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
const compCsv = ["component,label,range_dev_low_end_lo,range_dev_low_end_hi,range_dev_high_end_lo,range_dev_high_end_hi"]
  .concat(components.map((x) => [x.name, `"${x.label}"`, fx(x.lo[0]), fx(x.hi[0]), fx(x.lo[1]), fx(x.hi[1])].join(",")));
fs.writeFileSync(path.join(HERE, "derived", "components.csv"), compCsv.join("\n") + "\n");
const summary = {
  adopted_2026_09_23: s26.adopted_2026_09_23, adopted_2026_09_24: s26.adopted_2026_09_24, adopted_2026_09_26: old,
  uncorrected_at_adopted_responses: uncorrectedAtResponses,
  main_case: C, change: [C[0] - old[0], C[1] - old[1]],
  responses: responsesFor({}),
  school: {
    rules: P.RULES, one_year: old, within_district: low, within_district_as_response: lowAsResponse,
    school_line_at_full_cost: schoolLine, unfunded_by_rule: unfunded,
    sign_break_even: "unchanged: main_case_2026_09_26/derived/sign_reversal.csv (schools move with the common share)",
  },
  range: { low_end: rangeLowEnd, high_end: rangeHighEnd, overall: [rangeLowEnd[0], rangeHighEnd[1]], quadrature },
  other_profiles: otherProfiles,
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn,
  by_side_vs_uncorrected_at_adopted_responses: sides,
  group_receipts_bn: groupReceipts,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi,
    variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
};
fs.writeFileSync(path.join(HERE, "derived", "summary.json"), JSON.stringify(summary, null, 1) + "\n");
if (!gateState.failures) fs.writeFileSync(path.join(HERE, "derived", "corrections.json"), JSON.stringify(payload, null, 1) + "\n");

console.log("\n[result]");
console.log(`  adopted 2026-09-26 (one year)   ${old[0].toFixed(2)}–${old[1].toFixed(2)}`);
console.log(`  schools at full average cost    ${C[0].toFixed(2)}–${C[1].toFixed(2)}  (change ${(C[0] - old[0]).toFixed(2)} / ${(C[1] - old[1]).toFixed(2)})`);
console.log(`  low side, within district       ${low[0].toFixed(2)}–${low[1].toFixed(2)}  (0.836 as the response: ${lowAsResponse[0].toFixed(2)}–${lowAsResponse[1].toFixed(2)})`);
console.log(`  school line at full cost        ${schoolLine[0].toFixed(2)} / ${schoolLine[1].toFixed(2)}`);
for (const [k, v] of Object.entries(unfunded)) console.log(`    unfunded at ${k.padEnd(28)} ${v[0].toFixed(2)} / ${v[1].toFixed(2)}`);
console.log(`  range, low end                  ${rangeLowEnd[0].toFixed(1)}–${rangeLowEnd[1].toFixed(1)}`);
console.log(`  range, high end                 ${rangeHighEnd[0].toFixed(1)}–${rangeHighEnd[1].toFixed(1)}`);
console.log(`  spreads in quadrature           ${quadrature[0].toFixed(1)}–${quadrature[1].toFixed(1)}`);
for (const [pf, v] of Object.entries(otherProfiles)) console.log(`  ${pf.padEnd(34)} ${v.sept26.map((x) => x.toFixed(2)).join("–")} -> ${v.adopted.map((x) => x.toFixed(2)).join("–")}`);
console.log(`  no fill-in correction           ${noFillIn[0].toFixed(2)}–${noFillIn[1].toFixed(2)}`);
console.log(`  with audit row 3 instead        ${withRow3[0].toFixed(2)}–${withRow3[1].toFixed(2)}`);
console.log(`  uncorrected at the responses    ${uncorrectedAtResponses[0].toFixed(2)}–${uncorrectedAtResponses[1].toFixed(2)}`);
for (const x of components) console.log(`    range: ${x.name.padEnd(16)} low end ${x.lo[0].toFixed(2)}..+${x.hi[0].toFixed(2)}  high end ${x.lo[1].toFixed(2)}..+${x.hi[1].toFixed(2)}`);
if (gateState.failures) { console.error(`FAIL: ${gateState.failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
