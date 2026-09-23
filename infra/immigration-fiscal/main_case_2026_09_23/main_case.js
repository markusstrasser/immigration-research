/* Adopted main case of the complete annual account (operator decision, 2026-09-23).
 *
 * Runs the explorer's evaluator (assumption_explorer_2026_09_21/engine.js, gated against the
 * executed grid by test_engine.js) on its executed model, first reproducing the three published
 * service-response bands exactly, then applying the three adopted changes:
 *   1. general government responds at 0.59-0.84 (scaling_check.json composite_low/high), not zero;
 *   2. public order and safety keyed by use (cj_use_allocation_2026_09_23 central key set);
 *   3. the under-charged part of uncompensated hospital care keyed to uninsured use
 *      (uncompensated_care_2026_09_23, equal use; the 0.7x-use arm is a sensitivity).
 * Changes 2 and 3 move target allocations inside the account (national totals conserved); both
 * sit on lines with response 1 in every published profile. Run: node main_case.js
 */
"use strict";
const fs = require("fs");
const path = require("path");

const FISCAL = path.join(__dirname, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const scaling = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "scaling_check.json"), "utf8"));
const cj = JSON.parse(fs.readFileSync(path.join(FISCAL, "cj_use_allocation_2026_09_23", "derived", "summary.json"), "utf8"));
const uc = JSON.parse(fs.readFileSync(path.join(FISCAL, "uncompensated_care_2026_09_23", "derived", "summary.json"), "utf8"));

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}

const PROFILES = {
  cbo_category_lag_non_school_fixed: { other_education_response: 0, delayed_response: 0, school_response_band: [0.63, 0.66] },
  cbo_category_lag_non_school_full: { other_education_response: 1, delayed_response: 0, school_response_band: [0.63, 0.66] },
  proportional_reference: {},
};
const published = model.meta.headline.category_service_response_sensitivity;

function span(m, settings, extra) {
  const state = Object.assign(Engine.defaultState(m), settings, extra || {});
  return Engine.unresolvedRange(m, state, "welfare_bn");
}

// Shift a line's target allocation by delta (bn) in both allocations, conserving the national total.
function shifted(m, lineId, delta) {
  const out = JSON.parse(JSON.stringify(m));
  const line = out.spending.lines.find((l) => l.id === lineId);
  if (!line) throw new Error("no line " + lineId);
  const key = line.keys[line.preferred_key];
  ["personal", "shared"].forEach((a) => {
    key[a].target_bn += delta; key[a].other_bn -= delta;
  });
  return out;
}

console.log("\n[positive controls: published bands]");
for (const [name, settings] of Object.entries(PROFILES)) {
  const got = span(model, settings);
  const want = [published[name].min_welfare_bn, published[name].max_welfare_bn];
  gate(name, Math.abs(got[0] - want[0]) < 1e-6 && Math.abs(got[1] - want[1]) < 1e-6,
    `${got[0].toFixed(3)} to ${got[1].toFixed(3)}`);
}
const ppos = model.spending.lines.find((l) => l.id === "public_order_safety").keys.population.personal.target_bn;
gate("public order and safety per head = justice lane reference", Math.abs(ppos - cj.central.target_bn + cj.central.change_bn) < 1e-6,
  `${ppos.toFixed(6)} bn`);
gate("general-government responses read", scaling.composite_low === 0.59 && scaling.composite_high === 0.84,
  `${scaling.composite_low} / ${scaling.composite_high}`);

const GG = { low: scaling.composite_low, high: scaling.composite_high };
const JUSTICE = { central: cj.central.change_bn, raw_coding: cj.one_at_a_time_change_bn.scaling_raw,
  grid_low: cj.range_change_bn[0], grid_high: cj.range_change_bn[1], cbp_fixed: cj.one_at_a_time_change_bn.cbp_zero };
const UC_INSIDE = { equal_low: uc["inside_undercharged_bn_use_1.0"][0], equal_high: uc["inside_undercharged_bn_use_1.0"][1],
  use07_low: uc["inside_undercharged_bn_use_0.7"][0], use07_high: uc["inside_undercharged_bn_use_0.7"][1] };

function adoptedModel(justice, ucInside) {
  return shifted(shifted(model, "public_order_safety", justice), "medicaid_and_chip_other_medical", ucInside);
}

const rows = [];
function record(profile, variant, lo, hi) {
  // lo/hi are welfare (negative = cost); report cost as positive bn, least costly first.
  rows.push({ profile, variant, cost_low_bn: -hi, cost_high_bn: -lo });
}
for (const [name, settings] of Object.entries(PROFILES)) {
  const base = span(model, settings);
  record(name, "published", base[0], base[1]);
  record(name, "gg_0.59", ...span(model, settings, { general_government_response: GG.low }));
  record(name, "gg_0.84", ...span(model, settings, { general_government_response: GG.high }));
  record(name, "justice_by_use_central", ...span(adoptedModel(JUSTICE.central, 0), settings));
  record(name, "uncompensated_inside_equal_use", span(adoptedModel(0, UC_INSIDE.equal_high), settings)[0],
    span(adoptedModel(0, UC_INSIDE.equal_low), settings)[1]);
  // Adopted: envelope over the general-government range and the uncompensated-care range.
  const least = span(adoptedModel(JUSTICE.central, UC_INSIDE.equal_low), settings, { general_government_response: GG.low });
  const most = span(adoptedModel(JUSTICE.central, UC_INSIDE.equal_high), settings, { general_government_response: GG.high });
  record(name, "adopted", most[0], least[1]);
  // Sensitivities on the adopted case.
  for (const [label, j] of [["justice_raw_coding", JUSTICE.raw_coding], ["justice_grid_low", JUSTICE.grid_low],
    ["justice_grid_high", JUSTICE.grid_high], ["justice_cbp_fixed", JUSTICE.cbp_fixed]]) {
    const a = span(adoptedModel(j, UC_INSIDE.equal_low), settings, { general_government_response: GG.low });
    const b = span(adoptedModel(j, UC_INSIDE.equal_high), settings, { general_government_response: GG.high });
    record(name, "adopted_" + label, b[0], a[1]);
  }
  const u1 = span(adoptedModel(JUSTICE.central, UC_INSIDE.use07_low), settings, { general_government_response: GG.low });
  const u2 = span(adoptedModel(JUSTICE.central, UC_INSIDE.use07_high), settings, { general_government_response: GG.high });
  record(name, "adopted_uncompensated_use_0.7", u2[0], u1[1]);
}

// Gate: adopted = published shifted by the three deltas (response 1 on both moved lines).
const main = rows.filter((r) => r.profile === "cbo_category_lag_non_school_full");
const pub = main.find((r) => r.variant === "published"), ad = main.find((r) => r.variant === "adopted");
const ggLine = model.spending.lines.find((l) => l.id === "general_public_services").keys.population.personal.target_bn;
const expectLow = pub.cost_low_bn + GG.low * ggLine + JUSTICE.central + UC_INSIDE.equal_low;
const expectHigh = pub.cost_high_bn + GG.high * ggLine + JUSTICE.central + UC_INSIDE.equal_high;
gate("adopted main band = published + deltas", Math.abs(ad.cost_low_bn - expectLow) < 1e-6 && Math.abs(ad.cost_high_bn - expectHigh) < 1e-6,
  `${ad.cost_low_bn.toFixed(2)} to ${ad.cost_high_bn.toFixed(2)} bn`);

const target = model.meta.target_population;
const out = path.join(__dirname, "derived");
fs.mkdirSync(out, { recursive: true });
const header = "profile,variant,cost_low_bn,cost_high_bn,per_member_low,per_member_high";
const csv = [header].concat(rows.map((r) => [r.profile, r.variant, r.cost_low_bn.toFixed(4), r.cost_high_bn.toFixed(4),
  (r.cost_low_bn * 1e9 / target).toFixed(0), (r.cost_high_bn * 1e9 / target).toFixed(0)].join(","))).join("\n") + "\n";
fs.writeFileSync(path.join(out, "main_case_bands.csv"), csv);
fs.writeFileSync(path.join(out, "inputs.json"), JSON.stringify({ general_government_response: GG,
  general_government_target_bn: ggLine, justice_change_bn: JUSTICE, uncompensated_inside_bn: UC_INSIDE,
  target_population: target }, null, 1) + "\n");
console.log("\n" + csv);
if (failures) { console.error(`FAIL: ${failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
