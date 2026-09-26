/* The main case adopted on 2026-09-26, run once through the explorer engine.
 *
 * Base: the September 24 case (main_case_2026_09_24, $200.8752–246.3184bn), reproduced to 1e-4
 * through its own package before any change. Adopted together by the operator on 2026-09-26
 * (decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md):
 *   227  finite-removal responses: general government 0.6000/0.8504, schools 0.6522/0.6813, audit
 *        row 8 at 0.949 of its increment (finite_response_2026_09_26);
 *   225  the consumption key corrected for saving and remittances, spec both_corridor_net_h2
 *        (consumption_key_2026_09_24).
 * package.cjs holds the definitions. How each change enters:
 * - The responses replace the September 24 specifications' 0.59/0.84 and 0.63/0.66 value for value;
 *   every profile and every range variant uses them. The shelter constant stays keyed to 0.59/0.84
 *   (it would move by about -$0.002bn; finite_response_2026_09_26 RESULT).
 * - Row 8's change is one more shift on the constants line: 2.0 x (0.949 - 1).
 * - The consumption key's edits are that lane's, in dollars, measured on the September 24 central
 *   case (stack factor phi 0.9497). Range variants with another tax stack keep those dollars; the
 *   gates report how far phi moves across the stacks.
 * - The range adds two components: the functional form of the removal (r = b under a fixed cost
 *   plus a constant marginal cost; the engine key's population share; pupil shares 0.16 and 0.18),
 *   and the consumption key across its lane's twelve saving-and-remittance specifications.
 *
 * Gates (exit 1 on failure): the September 24 case and its payload reproduce; each change alone and
 * both together reproduce the two lanes' own runs; the payload reproduces the new case.
 * Run from anywhere: node main_case.cjs -> derived/main_case_bands.csv, components.csv, changes.csv,
 * summary.json and, only when every gate passes, corrections.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("./package.cjs");
const { P24, Engine, MODEL, HERE, ALLOCS, SYN, PROFILES, MAIN_PROFILE, CASES, METHODS, STACKS, CONSTANTS, LTSS_RANGE,
  CK, CK_SPECS, R, gateState, gate, near, f2, csvRows, readJson, both, mean2, bandFor, specsFor, evalPackage, central,
  correctionsPayload, responsesFor, benefitSe } = P;

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the September 24 case]");
const pub24 = {};
csvRows("main_case_2026_09_24/derived/main_case_bands.csv").forEach((r) => {
  if (r.variant === "adopted") pub24[r.profile] = [Number(r.cost_low_bn), Number(r.cost_high_bn)];
});
const base = P24.central({});
gate("the September 24 package reproduces its adopted case", near(base[0], pub24[MAIN_PROFILE][0], 1e-4)
  && near(base[1], pub24[MAIN_PROFILE][1], 1e-4), `${base[0].toFixed(4)}–${base[1].toFixed(4)}`);
gate("the September 24 corrections.json is its package's payload",
  JSON.stringify(P24.correctionsPayload()) === JSON.stringify(P.SEPT24), "deep-equal");
const uncorrected24 = P24.band(MODEL);
const sales = MODEL.receipts.lines.find((l) => l.id === "general_sales_tax");
const salesEdit = P.SEPT24.edits.find((e) => e.side === "receipt" && e.line === "general_sales_tax" && e.scenario === MODEL.receipts.reference);
const phiAdopted = (sales.cells[MODEL.receipts.reference].personal.target_bn + salesEdit.by.personal)
  / sales.cells[MODEL.receipts.reference].personal.target_bn;
gate("the consumption key's phi is the September 24 payload's factor on sales tax", near(phiAdopted, CK.meta.phi, 1e-9),
  `${phiAdopted.toFixed(9)} vs ${CK.meta.phi.toFixed(9)}`);
// How far phi moves across the tax stacks, which the key's dollars do not follow (reported, not gated).
const phis = CASES.flatMap((c) => METHODS.map((m) => {
  const shifts = P24.packageShifts(STACKS[`row4+status_state_aware|${c}|${m}`], c, m, P24.CENTRAL);
  const d = shifts.filter((s) => s.side === "receipt" && s.line === "general_sales_tax").reduce((a, s) => a + s.by.personal, 0);
  const t0 = sales.cells[MODEL.receipts.reference].personal.target_bn;
  return (t0 + d) / t0;
}));
console.log(`  (phi on sales tax across the six stacks: ${Math.min(...phis).toFixed(4)}–${Math.max(...phis).toFixed(4)})`);

console.log("\n[gates: each change alone and together reproduce their lanes]");
const runs = readJson("finite_response_2026_09_26/derived/runs.json").runs;
const runC = (name) => { if (!runs[name]) throw new Error("no run " + name); return runs[name].central; };
const alone = {};
function check(label, o, want, tol) {
  const got = central(o);
  alone[label] = [got[0] - base[0], got[1] - base[1]];
  gate(`${label} reproduces`, near(got[0], want[0], tol) && near(got[1], want[1], tol),
    `${got[0].toFixed(4)}–${got[1].toFixed(4)} vs ${want[0].toFixed(4)}–${want[1].toFixed(4)}`);
  return got;
}
check("general government finite, with row 8 (run I)", { ck: null, finite: "gg" }, runC("I gg + row 8 (general government only)"), 1e-4);
check("schools finite (run F)", { ck: null, finite: "school" }, runC("F school finite r, pupil share"), 1e-4);
check("schools finite at s 0.16 (run G)", { ck: null, finite: "school", school_s: "_s0.16" }, runC("G school finite r, s 0.16"), 1e-4);
check("schools finite at s 0.18 (run H)", { ck: null, finite: "school", school_s: "_s0.18" }, runC("H school finite r, s 0.18"), 1e-4);
check("finite removal (run J)", { ck: null }, runC("J all: gg + row 8 + school"), 1e-4);
check("consumption key (run L)", { finite: false }, runC("L consumption key alone (ladder 225)"), 1e-3);
const ckSummary = readJson("consumption_key_2026_09_24/derived/engine_summary.json");
for (const spec of CK_SPECS) {
  const got = central({ finite: false, ck: spec }), want = ckSummary.specs[spec].band;
  gate(`consumption key ${spec} reproduces its lane`, near(got[0], want[0], 1e-3) && near(got[1], want[1], 1e-3),
    `${got[0].toFixed(3)}–${got[1].toFixed(3)} vs ${want[0].toFixed(3)}–${want[1].toFixed(3)}`);
}
const C = check("both (run K)", {}, runC("K all finite + consumption key"), 1e-3);

// ---------------------------------------------------------------------------------------------------
console.log("\n[package]");
console.log(`  central: ${C[0].toFixed(2)}–${C[1].toFixed(2)} (change ${(C[0] - base[0]).toFixed(2)} / ${(C[1] - base[1]).toFixed(2)})`);
const dev = (b) => [b[0] - C[0], b[1] - C[1]];
const components = [];
function component(name, label, variants) {
  const devs = variants.map(([v, b]) => ({ v, d: dev(b) }));
  const lo = [Math.min(0, ...devs.map((x) => x.d[0])), Math.min(0, ...devs.map((x) => x.d[1]))];
  const hi = [Math.max(0, ...devs.map((x) => x.d[0])), Math.max(0, ...devs.map((x) => x.d[1]))];
  components.push({ name, label, lo, hi, devs });
}
// The September 24 components, on the new case.
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
// The two new components.
component("finite_removal", "removal response: r = b (fixed plus constant marginal cost); engine-key population share; pupil share 0.16 or 0.18",
  [["r = b", central({ finite: false })], ["engine population key", central({ gg_s: "engine_population_key" })],
    ["pupil share 0.16", central({ school_s: "_s0.16" })], ["pupil share 0.18", central({ school_s: "_s0.18" })]]);
component("consumption_key", "consumption key: the lane's twelve saving-and-remittance specifications",
  CK_SPECS.map((s) => [s, central({ ck: s })]));
const sumLo = components.reduce((s, x) => [s[0] + x.lo[0], s[1] + x.lo[1]], [0, 0]);
const sumHi = components.reduce((s, x) => [s[0] + x.hi[0], s[1] + x.hi[1]], [0, 0]);
const rangeLowEnd = [C[0] + sumLo[0], C[0] + sumHi[0]], rangeHighEnd = [C[1] + sumLo[1], C[1] + sumHi[1]];
const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
const quadrature = [C[0] - rss(components.map((x) => x.lo[0])), C[1] + rss(components.map((x) => x.hi[1]))];

// Comparisons and the other two service profiles.
const withRow3 = central({ incomeTax: "row3" });
const noFillIn = evalPackage("central", "audit_rules_alone", {});
const uncorrectedAtResponses = P.band(MODEL);
const otherProfiles = {};
for (const profile of Object.keys(PROFILES).filter((x) => x !== MAIN_PROFILE)) {
  const b24 = P24.central({ profile });
  gate(`${profile}: the September 24 package reproduces its band`, near(b24[0], pub24[profile][0], 1e-4) && near(b24[1], pub24[profile][1], 1e-4),
    `${b24[0].toFixed(4)}–${b24[1].toFixed(4)}`);
  otherProfiles[profile] = { sept23: P24.band(MODEL, profile), sept24: b24, uncorrected_at_adopted_responses: P.band(MODEL, profile),
    adopted: central({ profile }) };
}
// The changes on the September 24 case, alone and added.
const changes = {
  general_government: alone["general government finite, with row 8 (run I)"],
  schools: alone["schools finite (run F)"],
  finite_removal: alone["finite removal (run J)"],
  consumption_key: alone["consumption key (run L)"],
};
const added = [base[0] + changes.finite_removal[0] + changes.consumption_key[0], base[1] + changes.finite_removal[1] + changes.consumption_key[1]];

// The package by side, against the uncorrected model at the adopted responses: receipt edits against
// spending edits (the synthetic lines included). The responses themselves act on spending.
const payload = correctionsPayload();
const pBand = (edits) => P.band(Engine.applyCorrections(MODEL, { lines: payload.lines, edits }));
const payloadBand = pBand(payload.edits);
gate("corrections.json reproduces the adopted case", near(payloadBand[0], C[0], 1e-4) && near(payloadBand[1], C[1], 1e-4), f2(payloadBand));
const recOnly = pBand(payload.edits.filter((e) => e.side === "receipt"));
const spOnly = pBand(payload.edits.filter((e) => e.side !== "receipt"));
const sides = { receipts: [recOnly[0] - uncorrectedAtResponses[0], recOnly[1] - uncorrectedAtResponses[1]],
  spending: [spOnly[0] - uncorrectedAtResponses[0], spOnly[1] - uncorrectedAtResponses[1]] };
gate("the two sides add to the package", near(sides.receipts[0] + sides.spending[0], C[0] - uncorrectedAtResponses[0], 1e-6)
  && near(sides.receipts[1] + sides.spending[1], C[1] - uncorrectedAtResponses[1], 1e-6), `${f2(sides.receipts)} + ${f2(sides.spending)}`);
const unit = P.band(Engine.applyCorrections(MODEL, { lines: payload.lines,
  edits: payload.edits.concat([{ side: "spending", line: SYN.constants, key: "k", by: both(1) }]) }));
gate("a unit constant moves both ends by 1", near(unit[0] - payloadBand[0], 1, 1e-9) && near(unit[1] - payloadBand[1], 1, 1e-9),
  f2([unit[0] - payloadBand[0], unit[1] - payloadBand[1]]));
// The group's receipts on the reference incidence rule, all lines, for the back-cast.
const receiptsTotal = (m) => Object.fromEntries(ALLOCS.map((a) =>
  [a, m.receipts.lines.reduce((s, l) => s + l.cells[m.receipts.reference][a].target_bn, 0)]));
const groupReceipts = { adopted_2026_09_23: receiptsTotal(MODEL),
  adopted_2026_09_24: receiptsTotal(Engine.applyCorrections(MODEL, P.SEPT24)),
  adopted: receiptsTotal(Engine.applyCorrections(MODEL, payload)) };

// ---------------------------------------------------------------------------------------------------
const fx = (x) => x.toFixed(4);
fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
const bandsCsv = ["profile,variant,cost_low_bn,cost_high_bn,range_low_bn,range_high_bn",
  `${MAIN_PROFILE},adopted_2026_09_23,${fx(uncorrected24[0])},${fx(uncorrected24[1])},,`,
  `${MAIN_PROFILE},adopted_2026_09_24,${fx(base[0])},${fx(base[1])},,`,
  `${MAIN_PROFILE},uncorrected_at_adopted_responses,${fx(uncorrectedAtResponses[0])},${fx(uncorrectedAtResponses[1])},,`,
  `${MAIN_PROFILE},finite_removal_only,${fx(base[0] + changes.finite_removal[0])},${fx(base[1] + changes.finite_removal[1])},,`,
  `${MAIN_PROFILE},consumption_key_only,${fx(base[0] + changes.consumption_key[0])},${fx(base[1] + changes.consumption_key[1])},,`,
  `${MAIN_PROFILE},adopted,${fx(C[0])},${fx(C[1])},${fx(rangeLowEnd[0])},${fx(rangeHighEnd[1])}`,
  `${MAIN_PROFILE},audit_row3_instead_of_cbo_income_tax,${fx(withRow3[0])},${fx(withRow3[1])},,`,
  `${MAIN_PROFILE},no_fill_in_correction,${fx(noFillIn[0])},${fx(noFillIn[1])},,`]
  .concat(Object.entries(otherProfiles).flatMap(([pf, v]) => [
    `${pf},adopted_2026_09_23,${fx(v.sept23[0])},${fx(v.sept23[1])},,`,
    `${pf},adopted_2026_09_24,${fx(v.sept24[0])},${fx(v.sept24[1])},,`,
    `${pf},uncorrected_at_adopted_responses,${fx(v.uncorrected_at_adopted_responses[0])},${fx(v.uncorrected_at_adopted_responses[1])},,`,
    `${pf},adopted,${fx(v.adopted[0])},${fx(v.adopted[1])},,`]));
fs.writeFileSync(path.join(HERE, "derived", "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
const compCsv = ["component,label,range_dev_low_end_lo,range_dev_low_end_hi,range_dev_high_end_lo,range_dev_high_end_hi"]
  .concat(components.map((x) => [x.name, `"${x.label}"`, fx(x.lo[0]), fx(x.hi[0]), fx(x.lo[1]), fx(x.hi[1])].join(",")));
fs.writeFileSync(path.join(HERE, "derived", "components.csv"), compCsv.join("\n") + "\n");
const changesCsv = ["change,on_sept24_low_bn,on_sept24_high_bn"]
  .concat(Object.entries(changes).map(([k, v]) => `${k},${fx(v[0])},${fx(v[1])}`))
  .concat([`both,${fx(C[0] - base[0])},${fx(C[1] - base[1])}`]);
fs.writeFileSync(path.join(HERE, "derived", "changes.csv"), changesCsv.join("\n") + "\n");
const summary = {
  adopted_2026_09_23: uncorrected24, adopted_2026_09_24: base, uncorrected_at_adopted_responses: uncorrectedAtResponses,
  main_case: C, change: [C[0] - base[0], C[1] - base[1]],
  responses: responsesFor(P.CENTRAL),
  range: { low_end: rangeLowEnd, high_end: rangeHighEnd, overall: [rangeLowEnd[0], rangeHighEnd[1]], quadrature },
  other_profiles: otherProfiles,
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn,
  changes, changes_added: added, interaction_total: [C[0] - added[0], C[1] - added[1]],
  consumption_key_phi: { adopted: CK.meta.phi, across_stacks: [Math.min(...phis), Math.max(...phis)] },
  by_side_vs_uncorrected_at_adopted_responses: sides,
  group_receipts_bn: groupReceipts,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi,
    variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
};
fs.writeFileSync(path.join(HERE, "derived", "summary.json"), JSON.stringify(summary, null, 1) + "\n");
if (!gateState.failures) fs.writeFileSync(path.join(HERE, "derived", "corrections.json"), JSON.stringify(payload, null, 1) + "\n");

console.log("\n[result]");
console.log(`  adopted 2026-09-24          ${base[0].toFixed(2)}–${base[1].toFixed(2)}`);
console.log(`  adopted 2026-09-26          ${C[0].toFixed(2)}–${C[1].toFixed(2)}  (change ${(C[0] - base[0]).toFixed(2)} / ${(C[1] - base[1]).toFixed(2)})`);
for (const [k, v] of Object.entries(changes)) console.log(`    alone: ${k.padEnd(20)} ${v[0].toFixed(2)} / ${v[1].toFixed(2)}`);
console.log(`  range, low end              ${rangeLowEnd[0].toFixed(1)}–${rangeLowEnd[1].toFixed(1)}`);
console.log(`  range, high end             ${rangeHighEnd[0].toFixed(1)}–${rangeHighEnd[1].toFixed(1)}`);
console.log(`  spreads in quadrature       ${quadrature[0].toFixed(1)}–${quadrature[1].toFixed(1)}`);
for (const [pf, v] of Object.entries(otherProfiles)) console.log(`  ${pf.padEnd(34)} ${v.sept24.map((x) => x.toFixed(2)).join("–")} -> ${v.adopted.map((x) => x.toFixed(2)).join("–")}`);
console.log(`  no fill-in correction       ${noFillIn[0].toFixed(2)}–${noFillIn[1].toFixed(2)}`);
console.log(`  with audit row 3 instead    ${withRow3[0].toFixed(2)}–${withRow3[1].toFixed(2)}`);
console.log(`  uncorrected at the responses ${uncorrectedAtResponses[0].toFixed(2)}–${uncorrectedAtResponses[1].toFixed(2)}`);
console.log(`  taxes ${f2(sides.receipts)}   keyed spending ${f2(sides.spending)} (against the uncorrected model at the responses)`);
for (const x of components) console.log(`    range: ${x.name.padEnd(16)} low end ${x.lo[0].toFixed(2)}..+${x.hi[0].toFixed(2)}  high end ${x.lo[1].toFixed(2)}..+${x.hi[1].toFixed(2)}`);
if (gateState.failures) { console.error(`FAIL: ${gateState.failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
