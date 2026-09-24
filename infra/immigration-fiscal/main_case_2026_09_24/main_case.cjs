/* The main case adopted on 2026-09-24, run once through the explorer engine.
 *
 * Base: main_case_2026_09_23 (profile cbo_category_lag_non_school_full, 64 specifications; the low end
 * is the shared allocation, the high end the personal one), reproduced to 1e-4 before any change.
 *
 * Adopted by the operator on 2026-09-24 (decisions/2026-09-24-main-case-audit-and-outside-checks.md):
 *   1  the dataset audit as one package (dataset_integrity_2026_09_23), its row 6 run through the engine
 *      and its row 3 replaced by CBO's income-tax gradient;
 *   2  the pooled-MEPS medical figure jointly with the long-term-care carve-out, in place of audit row 5;
 *   3  care and household services (care_household_services_2026_09_23);
 *   5  migrant-shelter keying (migrant_shelter_costs_2026_09_23);
 *   6  the outside checks of 2026-09-24: schools priced where the group enrolls, CBO's income gradients,
 *      Treasury's EITC shares, benefit keys from administrative records and the booking correction.
 * Beside the account and not in these figures: the debt legacy (decision 4), victims' harm, audit
 * rows 11 and 12.
 *
 * How each change enters. Every model edit conserves national totals (other_bn moves the other way).
 * - Tax block: the CPS imputation lane's stack of audit rows 2, 13 and 4 and the state-aware status
 *   flag, as line deltas (derived/stack_line_deltas.json, a vendored subset of that lane's
 *   _cache/onbooks_lane_line_deltas.json; drift-checked whenever the cache is present). Central: the
 *   mean of the two fill-in methods at the on-books lane's central share. Range: the six case x method
 *   stacks. Audit row 3 is not in the stack; CBO's income-tax gradient replaces it.
 * - Frame: this script uses combine.cjs's overrides (justice "use", Medicaid uninsured_use_low/high).
 *   The CPS and long-term-care lanes translated on preferred keys plus the adopted justice and
 *   uncompensated-care shifts, so a shift on medicaid/medicaid also moves both uninsured-use keys, and
 *   the stack's public_order_safety/population shift (the use key's per-head part, scaled by the CPS
 *   lane) moves the use key. Gate: each stack alone reproduces the CPS lane's published change.
 * - Ratio-type changes rescale the group's key dollars on a line: CBO's gradients, the benefit keys,
 *   the medical-ethnicity ratios, the school price and re-blend. On top of the stack each is multiplied
 *   by its key's stack factor (the group's target after the stack over the target before).
 * - Replacement-type changes set the group's charge on named dollars: the long-term-care carve-out (the
 *   stack's change on those dollars is removed), premium tax credits (the stack already leaves them
 *   alone) and Treasury's EITC share (measured against the audit's SSN rule).
 * - Overlaps: CBO's income-tax gradient replaces audit row 3; the benefit keys replace CBO on SNAP, WIC
 *   and cash assistance; the medical-ethnicity ratios replace CBO's Medicare gradient; the booking
 *   factor multiplies audit row 7's 2024 arrest ratio.
 * - Lane figures with no line in common with any other change enter as one synthetic line at
 *   response 1: audit rows 8, 9 and 10 and its small items, shelter, care.
 * - Ranges: the tax block's six stacks and each other component's variants, summed as independent
 *   bounds at each band end, as dataset_integrity_2026_09_23/synthesis.py sums the audit's rows.
 *
 * Gates (exit 1 on failure): the adopted case reproduces; every component alone reproduces its lane.
 * Run from anywhere: node main_case.cjs  ->  derived/main_case_bands.csv, components.csv, summary.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const {
  Engine, MODEL, FISCAL, HERE, ALLOCS, SYN, MEDICAID, MAIN_SPECS, PROFILES, MAIN_PROFILE, CASES, METHODS, STACKS, CENTRAL, CONSTANTS, BOOKING, LTSS_CENTRAL, LTSS_RANGE, gateState, gate, near, span, f2, csvRows, read, readJson, both, scale, plus, cost, band, build, correctionsPayload, stackShifts, stackFactor, cboShifts, row3Shifts, otaShifts, row1Shifts, medicalShifts, educationShifts, minusT0, benefitShifts, justiceShifts, constantShifts, bookingRow, packageShifts, evalPackage, mean2, central, mts, schoolV, schoolLines, ltssMain, benefitSe,
} = require("./package.cjs");

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the adopted case and each change alone]");
const published = {};
csvRows("main_case_2026_09_23/derived/main_case_bands.csv").forEach((r) => {
  if (r.variant === "adopted") published[r.profile] = [Number(r.cost_low_bn), Number(r.cost_high_bn)];
});
const adopted = published.cbo_category_lag_non_school_full;
const base = band(build([]));
gate("no change reproduces the adopted main case", near(base[0], adopted[0], 1e-4) && near(base[1], adopted[1], 1e-4),
  `${base[0].toFixed(4)}–${base[1].toFixed(4)} vs ${adopted[0]}–${adopted[1]}`);
const change = (shifts) => { const b = band(build(shifts)); return [b[0] - base[0], b[1] - base[1]]; };
const alone = {};
function check(name, shifts, want, tol, detail) {
  const got = change(shifts);
  alone[name] = got;
  gate(`${name} alone reproduces ${detail}`, near(got[0], want[0], tol) && near(got[1], want[1], tol), `${f2(got)} vs ${f2(want)}`);
  return got;
}
const cpsLane = csvRows("cps_imputation_keys_2026_09_23/derived/status_combination_onbooks_lane.csv")
  .filter((r) => r.share_type === "origin" && r.arm === "row4+status_state_aware");
for (const c of CASES) for (const m of METHODS) {
  const want = ["shared", "personal"].map((a) => Number(cpsLane.find((r) => r.case === c && r.method === m && r.allocation === a).change_bn));
  check(`stack ${c}/${m}`, stackShifts(STACKS[`row4+status_state_aware|${c}|${m}`]), want, 2e-3, "the CPS lane's change");
}
const cboSpec = csvRows("external_benchmarks_2026_09_24/derived/cbo_spec_totals.csv").filter((r) => r.spec === "all_but_medicaid|2022");
check("CBO bundle 2022 (no skips)", cboShifts(2022, null, { skip: [], scaled: false }),
  ["low", "high"].map((e) => Number(cboSpec.find((r) => r.band_end === e).main_case_change_bn)), 1e-3, "the benchmarks lane");
const otaPub = csvRows("external_benchmarks_2026_09_24/derived/ota_main_case.csv")
  .find((r) => r.method === "vs_adopted_raw_keys" && r.profile === "cbo_category_lag_non_school_full");
check("Treasury EITC shares vs raw keys", otaShifts("vs_adopted_raw_keys"), [Number(otaPub.change_low_bn), Number(otaPub.change_high_bn)], 1e-3, "the benchmarks lane");
check("audit row 1", row1Shifts(), [mts.ptc_effect_on_main_case_bn, mts.ptc_effect_on_main_case_bn], 1e-6, "the audit's -14.23");
for (const spec of ["winsor_p995", "plain", "two_part_lognormal", "pooled_excl_2020_2021"]) {
  const r = ltssMain.find((x) => x.variant === "joint with medical-ethnicity lane: " + spec);
  check(`decision 2 joint ${spec}`, medicalShifts(null, spec), [Number(r.shift_low_bn), Number(r.shift_high_bn)], 1e-3, "the LTSS lane's engine run");
}
const schoolRow = (v) => { const r = schoolLines.find((x) => x.variant === v); return [Number(r.main_change_low_bn), Number(r.main_change_high_bn)]; };
check("row 6 whole line (w 0.77)", [
  { side: "spending", line: SYN.school, key: "k", by: minusT0(schoolV["row6_w0.77_whole_line"].school_target_bn) },
  { side: "spending", line: SYN.college, key: "k", by: minusT0(schoolV["row6_w0.77_whole_line"].college_target_bn) }],
  schoolRow("row6_w0.77_whole_line"), 1e-3, "the school lane");
check("row 6 school step with k (w 0.82)", [
  { side: "spending", line: SYN.school, key: "k", by: minusT0(schoolV["row6_w0.82|preferred"].school_target_bn) }],
  schoolRow("row6_w0.82|preferred"), 1e-3, "the school lane");
check("schools k on the adopted key", [
  { side: "spending", line: SYN.school, key: "k", by: minusT0(schoolV["preferred_district_and_school_level|blend"].school_target_bn) }],
  schoolRow("preferred_district_and_school_level|blend"), 1e-3, "the school lane");
const benPub = csvRows("admin_benefit_keys_2026_09_24/derived/main_case_translation.csv")
  .find((r) => r.spec === "package_central" && r.profile === "cbo_category_lag_non_school_full");
check("benefit keys (central)", benefitShifts(null), [Number(benPub.change_low_bn), Number(benPub.change_high_bn)], 1e-3, "the benefits lane");
const bk = bookingRow(BOOKING.central);
check("booking factor", justiceShifts(null, "central"), [bk, bk], 1e-6, "the crime lane");
check("audit row 7", justiceShifts("2024", null), [1.12, 1.12], 1e-6, "the audit's +1.12");
check("unit constant line", [{ side: "spending", line: SYN.constants, key: "k", by: both(1) }], [1, 1], 1e-9, "a response of 1");

// ---------------------------------------------------------------------------------------------------
console.log("\n[package]");
const C = central({});
console.log(`  central: ${C[0].toFixed(2)}–${C[1].toFixed(2)} (change ${(C[0] - base[0]).toFixed(2)} / ${(C[1] - base[1]).toFixed(2)})`);
const dev = (b) => [b[0] - C[0], b[1] - C[1]];
const components = [];
function component(name, label, variants) {
  const devs = variants.map(([v, b]) => ({ v, d: dev(b) }));
  const lo = [Math.min(0, ...devs.map((x) => x.d[0])), Math.min(0, ...devs.map((x) => x.d[1]))];
  const hi = [Math.max(0, ...devs.map((x) => x.d[0])), Math.max(0, ...devs.map((x) => x.d[1]))];
  components.push({ name, label, lo, hi, devs });
}
component("tax_block", "tax block: on-books share (low/central/high) x fill-in method",
  CASES.flatMap((c) => METHODS.map((m) => [`${c}/${m}`, evalPackage(c, m, CENTRAL)])));
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
const sumLo = components.reduce((s, x) => [s[0] + x.lo[0], s[1] + x.lo[1]], [0, 0]);
const sumHi = components.reduce((s, x) => [s[0] + x.hi[0], s[1] + x.hi[1]], [0, 0]);
const rangeLowEnd = [C[0] + sumLo[0], C[0] + sumHi[0]], rangeHighEnd = [C[1] + sumLo[1], C[1] + sumHi[1]];
// The same spreads combined as independent (root of the sum of squares), for context only.
const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
const quadrature = [C[0] - rss(components.map((x) => x.lo[0])), C[1] + rss(components.map((x) => x.hi[1]))];

// Comparisons: the audit's own row 3 in place of CBO's income tax; lane figures simply added.
const withRow3 = central({ incomeTax: "row3" });
// The other two service profiles of the September 23 lane, on the new case (central only).
const otherProfiles = {};
for (const profile of Object.keys(PROFILES).filter((x) => x !== MAIN_PROFILE)) {
  const b0 = band(build([]), profile);
  const want = published[profile];
  gate(`${profile}: no change reproduces the September 23 band`, near(b0[0], want[0], 1e-4) && near(b0[1], want[1], 1e-4),
    `${b0[0].toFixed(4)}–${b0[1].toFixed(4)}`);
  otherProfiles[profile] = { sept23: b0, adopted: central({ profile }) };
}
// Sensitivity: no fill-in correction (audit row 13 at zero), the audit's rules alone in the stack.
const noFillIn = evalPackage("central", "audit_rules_alone", CENTRAL);
const stackCentral = mean2(...METHODS.map((m) => { const s = check(`stack central/${m} (again)`, stackShifts(STACKS[`row4+status_state_aware|central|${m}`]),
  alone[`stack central/${m}`], 1e-9, "itself"); return s; }));
const aloneParts = {
  stack: stackCentral,
  cbo: change(cboShifts(2022, null, { scaled: false })),
  ota_over_audit: change(otaShifts("vs_audit_package_ssn_rule")),
  row1: alone["audit row 1"],
  medical: alone["decision 2 joint winsor_p995"],
  education: mean2(change(educationShifts(null, "0.77", "preferred")), change(educationShifts(null, "0.82", "preferred"))),
  benefits: alone["benefit keys (central)"],
  justice: change(justiceShifts("2024", "central")),
  constants: change(constantShifts(null)),
};
const added = Object.values(aloneParts).reduce((s, x) => [s[0] + x[0], s[1] + x[1]], [base[0], base[1]]);
// The package split by side: taxes (receipt shifts) against keyed spending (spending and synthetic lines).
const bySide = (keep) => mean2(...METHODS.map((m) => {
  const p = STACKS[`row4+status_state_aware|central|${m}`];
  const b = band(build(packageShifts(p, "central", m, CENTRAL).filter(keep)));
  return [b[0] - base[0], b[1] - base[1]];
}));
const sides = { receipts: bySide((x) => x.side === "receipt"), spending: bySide((x) => x.side !== "receipt") };
// The group's receipts on the reference incidence rule, all lines, before and after the package: the
// back-cast (historical_backcast_2026_09_20) splits each 2024 anchor into receipts and charged spending.
const receiptsTotal = (m) => Object.fromEntries(ALLOCS.map((a) =>
  [a, m.receipts.lines.reduce((s, l) => s + l.cells[m.receipts.reference][a].target_bn, 0)]));
const receiptsAfter = METHODS.map((meth) => receiptsTotal(build(packageShifts(STACKS[`row4+status_state_aware|central|${meth}`],
  "central", meth, CENTRAL)))).reduce((a, b) => ({ personal: (a.personal + b.personal) / 2, shared: (a.shared + b.shared) / 2 }));
const groupReceipts = { adopted_2026_09_23: receiptsTotal(MODEL), adopted: receiptsAfter };
// The engine's corrections payload, which the explorer and the figures page load: one net edit per cell.
const payload = correctionsPayload();
const payloadBand = band(Engine.applyCorrections(MODEL, payload));
gate("corrections.json reproduces the adopted case", near(payloadBand[0], C[0], 1e-4) && near(payloadBand[1], C[1], 1e-4), f2(payloadBand));
const payloadTaxes = band(Engine.applyCorrections(MODEL, { lines: payload.lines, edits: payload.edits.filter((e) => e.side === "receipt") }));
gate("its receipt edits reproduce the receipts side", near(payloadTaxes[0] - base[0], sides.receipts[0], 1e-4)
  && near(payloadTaxes[1] - base[1], sides.receipts[1], 1e-4), f2([payloadTaxes[0] - base[0], payloadTaxes[1] - base[1]]));
gate("the two sides add to the package", near(sides.receipts[0] + sides.spending[0], C[0] - base[0], 1e-6)
  && near(sides.receipts[1] + sides.spending[1], C[1] - base[1], 1e-6), `${f2(sides.receipts)} + ${f2(sides.spending)}`);

// ---------------------------------------------------------------------------------------------------
fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
const bandsCsv = ["profile,variant,cost_low_bn,cost_high_bn,range_low_bn,range_high_bn",
  `cbo_category_lag_non_school_full,adopted_2026_09_23,${base[0].toFixed(4)},${base[1].toFixed(4)},,`,
  `cbo_category_lag_non_school_full,adopted,${C[0].toFixed(4)},${C[1].toFixed(4)},${rangeLowEnd[0].toFixed(4)},${rangeHighEnd[1].toFixed(4)}`,
  `cbo_category_lag_non_school_full,audit_row3_instead_of_cbo_income_tax,${withRow3[0].toFixed(4)},${withRow3[1].toFixed(4)},,`,
  `cbo_category_lag_non_school_full,no_fill_in_correction,${noFillIn[0].toFixed(4)},${noFillIn[1].toFixed(4)},,`,
  `cbo_category_lag_non_school_full,lane_figures_added,${added[0].toFixed(4)},${added[1].toFixed(4)},,`]
  .concat(Object.entries(otherProfiles).flatMap(([pf, v]) => [
    `${pf},adopted_2026_09_23,${v.sept23[0].toFixed(4)},${v.sept23[1].toFixed(4)},,`,
    `${pf},adopted,${v.adopted[0].toFixed(4)},${v.adopted[1].toFixed(4)},,`]));
fs.writeFileSync(path.join(HERE, "derived", "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
const compCsv = ["component,label,range_dev_low_end_lo,range_dev_low_end_hi,range_dev_high_end_lo,range_dev_high_end_hi"]
  .concat(components.map((x) => [x.name, `"${x.label}"`, x.lo[0].toFixed(4), x.hi[0].toFixed(4), x.lo[1].toFixed(4), x.hi[1].toFixed(4)].join(",")));
fs.writeFileSync(path.join(HERE, "derived", "components.csv"), compCsv.join("\n") + "\n");
const aloneCsv = ["change,alone_on_adopted_low_bn,alone_on_adopted_high_bn"]
  .concat(Object.entries(aloneParts).map(([k, v]) => `${k},${v[0].toFixed(4)},${v[1].toFixed(4)}`));
fs.writeFileSync(path.join(HERE, "derived", "alone_on_adopted.csv"), aloneCsv.join("\n") + "\n");
const summary = {
  adopted_2026_09_23: base, main_case: C, change: [C[0] - base[0], C[1] - base[1]],
  range: { low_end: rangeLowEnd, high_end: rangeHighEnd, overall: [rangeLowEnd[0], rangeHighEnd[1]], quadrature },
  other_profiles: otherProfiles,
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn, lane_figures_added: added,
  interaction_total: [C[0] - added[0], C[1] - added[1]],
  by_side: sides,
  group_receipts_bn: groupReceipts,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi,
    variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
  alone_on_adopted: aloneParts,
};
fs.writeFileSync(path.join(HERE, "derived", "summary.json"), JSON.stringify(summary, null, 1) + "\n");
// Pages load the payload directly, so it is written only when every gate so far has passed.
if (!gateState.failures) fs.writeFileSync(path.join(HERE, "derived", "corrections.json"), JSON.stringify(payload, null, 1) + "\n");

console.log("\n[result]");
console.log(`  adopted 2026-09-23          ${base[0].toFixed(2)}–${base[1].toFixed(2)}`);
console.log(`  adopted 2026-09-24          ${C[0].toFixed(2)}–${C[1].toFixed(2)}  (change ${(C[0] - base[0]).toFixed(2)} / ${(C[1] - base[1]).toFixed(2)})`);
console.log(`  range, low end              ${rangeLowEnd[0].toFixed(1)}–${rangeLowEnd[1].toFixed(1)}`);
console.log(`  range, high end             ${rangeHighEnd[0].toFixed(1)}–${rangeHighEnd[1].toFixed(1)}`);
console.log(`  spreads in quadrature       ${quadrature[0].toFixed(1)}–${quadrature[1].toFixed(1)}`);
for (const [pf, v] of Object.entries(otherProfiles)) console.log(`  ${pf.padEnd(34)} ${v.sept23.map((x) => x.toFixed(2)).join("–")} -> ${v.adopted.map((x) => x.toFixed(2)).join("–")}`);
console.log(`  no fill-in correction       ${noFillIn[0].toFixed(2)}–${noFillIn[1].toFixed(2)}`);
console.log(`  with audit row 3 instead    ${withRow3[0].toFixed(2)}–${withRow3[1].toFixed(2)}`);
console.log(`  taxes ${f2(sides.receipts)}   keyed spending ${f2(sides.spending)}`);
console.log(`  lane figures added          ${added[0].toFixed(2)}–${added[1].toFixed(2)}  (interactions ${(C[0] - added[0]).toFixed(2)} / ${(C[1] - added[1]).toFixed(2)})`);
for (const [k, v] of Object.entries(aloneParts)) console.log(`    alone: ${k.padEnd(16)} ${v[0].toFixed(2)} / ${v[1].toFixed(2)}`);
for (const x of components) console.log(`    range: ${x.name.padEnd(12)} low end ${x.lo[0].toFixed(2)}..+${x.hi[0].toFixed(2)}  high end ${x.lo[1].toFixed(2)}..+${x.hi[1].toFixed(2)}`);
if (gateState.failures) { console.error(`FAIL: ${gateState.failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
