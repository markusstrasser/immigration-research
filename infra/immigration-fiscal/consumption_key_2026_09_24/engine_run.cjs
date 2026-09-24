/* Engine run for the consumption-key lane (proposed, not adopted).
 *
 * Composes each specification's receipt and spending edits (derived/payloads.json, written by
 * consumption_key.py) after the adopted corrections (main_case_2026_09_24/derived/corrections.json)
 * and evaluates the main case with the engine. The band functions are replicated from
 * main_case_2026_09_24/package.cjs rather than imported, because loading package.cjs rewrites that
 * lane's derived/stack_line_deltas.json when the CPS lane cache exists.
 *
 * Run from the repository root: node infra/immigration-fiscal/consumption_key_2026_09_24/engine_run.cjs
 * Writes derived/engine_bands.csv and derived/engine_summary.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const MODEL = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const scaling = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "scaling_check.json"), "utf8"));
const ADOPTED = JSON.parse(fs.readFileSync(path.join(FISCAL, "main_case_2026_09_24", "derived", "corrections.json"), "utf8"));
const PAYLOADS = JSON.parse(fs.readFileSync(path.join(HERE, "derived", "payloads.json"), "utf8"));
const ADOPTED_BAND = [200.875, 246.318];  // main_case_2026_09_24/RESULT.md, adopted 2026-09-24

// ---- replicated from package.cjs (same names, same arithmetic) ----
const span = (xs) => [Math.min(...xs), Math.max(...xs)];
function product(dims) {
  return Object.entries(dims).reduce(
    (acc, [name, levels]) => acc.flatMap((spec) => levels.map((v) => ({ ...spec, [name]: v }))), [{}]);
}
const SHARES = Engine.schoolShareBounds(MODEL);
const GG = [scaling.composite_low, scaling.composite_high];
const MAIN_SPECS = product({
  allocation: ["personal", "shared"], normalization: ["cash", "gdp"], share: SHARES,
  school: [0.63, 0.66], gg: GG, uc: ["uninsured_use_low", "uninsured_use_high"], justice: ["use"],
});
const SYN = { school: "school_reprice", college: "college_rekey", constants: "lane_constants" };
const PROFILES = {
  cbo_category_lag_non_school_full: { other: 1, delayed: 0, school: null },
  cbo_category_lag_non_school_fixed: { other: 0, delayed: 0, school: null },
  proportional_reference: { other: 1, delayed: 1, school: 1 },
};
const MAIN_PROFILE = "cbo_category_lag_non_school_full";
// package.cjs cost(), with the receipt scenario as a parameter (package.cjs fixes the reference).
function cost(m, spec, profile, scenario) {
  const pr = PROFILES[profile || MAIN_PROFILE];
  const school = pr.school === null ? spec.school : pr.school;
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = scenario || m.receipts.reference;
  s.production.normalization = spec.normalization;
  s.count_production = true;
  s.general_government_response = spec.gg;
  s.key_override = { public_order_safety: spec.justice, medicaid_and_chip_other_medical: spec.uc };
  s.response_override = {
    education_services: spec.share * school + (1 - spec.share) * pr.other,
    public_order_safety: 1, health_services: 1, income_security_services: 1,
    housing_community_services: 1, economic_affairs_services: pr.delayed, recreation_culture: pr.delayed,
    [SYN.school]: spec.share * school, [SYN.college]: (1 - spec.share) * pr.other, [SYN.constants]: 1,
  };
  return -Engine.evaluate(m, s).welfare_bn;
}
const band = (m, profile, scenario) => span(MAIN_SPECS.map((spec) => cost(m, spec, profile, scenario)));
const byAllocation = (m, profile, scenario) => Object.fromEntries(["personal", "shared"].map((a) =>
  [a, span(MAIN_SPECS.filter((s) => s.allocation === a).map((spec) => cost(m, spec, profile, scenario)))]));

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}

const adoptedModel = Engine.applyCorrections(MODEL, ADOPTED);
const base = band(adoptedModel);
console.log("[gate] adopted payload, no lane edits");
gate("main case reproduces $200.875-246.318bn", Math.abs(base[0] - ADOPTED_BAND[0]) < 5e-4 && Math.abs(base[1] - ADOPTED_BAND[1]) < 5e-4,
  `${base[0].toFixed(3)} / ${base[1].toFixed(3)}`);
const baseAlloc = byAllocation(adoptedModel);
gate("low end is the shared allocation, high end personal", Math.abs(baseAlloc.shared[0] - base[0]) < 1e-9
  && Math.abs(baseAlloc.personal[1] - base[1]) < 1e-9);

const scenarios = MODEL.receipts.scenarios;
const profiles = Object.keys(PROFILES);
const baseBands = {};
for (const pr of profiles) for (const sc of scenarios) baseBands[`${pr}|${sc}`] = band(adoptedModel, pr, sc);

const rows = [];
const summary = { adopted_band: base, specs: {} };
for (const [name, spec] of Object.entries(PAYLOADS.specs)) {
  const m = Engine.applyCorrections(MODEL, { meta: PAYLOADS.meta, lines: ADOPTED.lines, edits: ADOPTED.edits.concat(spec.edits) });
  // Receipt-only payload isolates the spending-resource edits' effect.
  const mReceipts = Engine.applyCorrections(MODEL, { meta: PAYLOADS.meta, lines: ADOPTED.lines,
    edits: ADOPTED.edits.concat(spec.edits.filter((e) => e.side === "receipt")) });
  for (const pr of profiles) {
    for (const sc of scenarios) {
      const b = band(m, pr, sc);
      const b0 = baseBands[`${pr}|${sc}`];
      rows.push({ spec: name, family: spec.family, profile: pr, receipt_scenario: sc, low_bn: b[0], high_bn: b[1],
        change_low_bn: b[0] - b0[0], change_high_bn: b[1] - b0[1] });
    }
  }
  const main = band(m);
  const mainReceipts = band(mReceipts);
  const alloc = byAllocation(m);
  const prop = band(m, "proportional_reference");
  const propReceipts = band(mReceipts, "proportional_reference");
  const propBase = baseBands[`proportional_reference|${MODEL.receipts.reference}`];
  summary.specs[name] = {
    family: spec.family, band: main, change: [main[0] - base[0], main[1] - base[1]],
    shared: alloc.shared, personal: alloc.personal,
    spending_resource_edits_main_case: [main[0] - mainReceipts[0], main[1] - mainReceipts[1]],
    spending_resource_edits_proportional_reference: [prop[0] - propReceipts[0], prop[1] - propReceipts[1]],
    proportional_reference_change: [prop[0] - propBase[0], prop[1] - propBase[1]],
  };
}

// Coverage: the lane's edits move the main case by the same amount under every receipt scenario
// (the four lines carry one target in all of them; remaining_production_property is indirect).
for (const name of Object.keys(PAYLOADS.specs)) {
  const mc = rows.filter((r) => r.spec === name && r.profile === MAIN_PROFILE);
  const lo = mc.map((r) => r.change_low_bn), hi = mc.map((r) => r.change_high_bn);
  summary.specs[name].scenario_change_spread = [Math.max(...lo) - Math.min(...lo), Math.max(...hi) - Math.min(...hi)];
}
const maxSpread = Math.max(...Object.values(summary.specs).flatMap((s) => s.scenario_change_spread));
gate("each specification moves every receipt scenario alike", maxSpread < 1e-6, `max spread ${maxSpread.toExponential(2)} $bn`);
const spendMax = Math.max(...Object.values(summary.specs).flatMap((s) => s.spending_resource_edits_main_case.map(Math.abs)));
gate("spending edits on resource keys carry no weight in the main case", spendMax < 1e-9, `max ${spendMax.toExponential(2)} $bn`);

const header = Object.keys(rows[0]);
fs.writeFileSync(path.join(HERE, "derived", "engine_bands.csv"),
  [header.join(",")].concat(rows.map((r) => header.map((k) => typeof r[k] === "number" ? r[k].toFixed(6) : r[k]).join(","))).join("\n") + "\n");
fs.writeFileSync(path.join(HERE, "derived", "engine_summary.json"), JSON.stringify(summary, null, 1) + "\n");

console.log("\n[main case] $bn a year, low (shared) / high (personal); change against the adopted band");
for (const [name, s] of Object.entries(summary.specs)) {
  console.log(`  ${name.padEnd(40)} ${s.band[0].toFixed(3)} / ${s.band[1].toFixed(3)}   ${s.change[0] >= 0 ? "+" : ""}${s.change[0].toFixed(3)} / ${s.change[1] >= 0 ? "+" : ""}${s.change[1].toFixed(3)}   proportional-reference spending edits ${s.spending_resource_edits_proportional_reference[0].toFixed(3)} / ${s.spending_resource_edits_proportional_reference[1].toFixed(3)}`);
}
if (failures) { console.error(`${failures} gate(s) failed`); process.exit(1); }
