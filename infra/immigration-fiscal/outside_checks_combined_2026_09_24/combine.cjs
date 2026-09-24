/* The three outside checks of 2026-09-24, run together through the explorer engine on the adopted
 * main case (profile cbo_category_lag_non_school_full, 64 specifications).
 *
 * Inputs, each read from its lane's derived files:
 *   schools   school_cost_where_enrolled_2026_09_24  variant preferred_district_and_school_level|blend
 *             (a re-priced school allocation that responds with the school step only)
 *   benefits  admin_benefit_keys_2026_09_24          package_central (preferred-key target shifts)
 *   taxes     external_benchmarks_2026_09_24         all_but_medicaid|2022 (CBO) + vs_adopted_raw_keys (OTA)
 *
 * SNAP, WIC (other_state_welfare) and cash assistance (family_and_general_assistance) are re-keyed by
 * both the benefits lane (administrative records by ethnicity) and the CBO bundle (income gradient,
 * holding the group's within-group share fixed). The combination takes the benefits lane's change on
 * those three lines and drops CBO's; the alternative is reported as a sensitivity.
 *
 * Gates (exit 1 on failure): no change reproduces main_case_bands.csv to 1e-4; each lane alone
 * reproduces its own published change to 1e-3.
 * Run from anywhere: node combine.cjs  →  derived/combined_bands.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const scaling = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "scaling_check.json"), "utf8"));
const read = (rel) => fs.readFileSync(path.join(FISCAL, rel), "utf8");
const readJson = (rel) => JSON.parse(read(rel));

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
const near = (a, b, tol) => Math.abs(a - b) < tol;
const span = (xs) => [Math.min(...xs), Math.max(...xs)];
function product(dims) {
  return Object.entries(dims).reduce(
    (acc, [name, levels]) => acc.flatMap((spec) => levels.map((v) => ({ ...spec, [name]: v }))), [{}]);
}

// The adopted main case as the school lane evaluates it (build_data.cjs cost()).
const SHARES = Engine.schoolShareBounds(model);
const GG = [scaling.composite_low, scaling.composite_high];
const MAIN_SPECS = product({
  allocation: ["personal", "shared"], normalization: ["cash", "gdp"], share: SHARES,
  school: [0.63, 0.66], gg: GG, uc: ["uninsured_use_low", "uninsured_use_high"], justice: ["use"],
});
const REPRICE = "school_reprice";
function cost(m, spec) {
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = m.receipts.reference;
  s.production.normalization = spec.normalization;
  s.count_production = true;
  s.general_government_response = spec.gg;
  s.key_override = { public_order_safety: spec.justice, medicaid_and_chip_other_medical: spec.uc };
  s.response_override = {
    education_services: spec.share * spec.school + (1 - spec.share) * 1,
    public_order_safety: 1, health_services: 1, income_security_services: 1,
    housing_community_services: 1, economic_affairs_services: 0, recreation_culture: 0,
    [REPRICE]: spec.share * spec.school,
  };
  return -Engine.evaluate(m, s).welfare_bn;
}
const band = (m) => span(MAIN_SPECS.map((spec) => cost(m, spec)));

// Model edits. Every edit conserves national totals (other_bn moves the other way).
const clone = (m) => JSON.parse(JSON.stringify(m));
function shiftKey(m, lineId, keyName, byAlloc) {
  const line = m.spending.lines.find((l) => l.id === lineId);
  if (!line) throw new Error("no spending line " + lineId);
  const key = line.keys[keyName || line.preferred_key];
  if (!key) throw new Error("no key " + lineId + "/" + keyName);
  for (const [a, v] of Object.entries(byAlloc)) { key[a].target_bn += v; key[a].other_bn -= v; }
}
function shiftReceipt(m, lineId, byAlloc) {
  const line = m.receipts.lines.find((l) => l.id === lineId);
  if (!line) throw new Error("no receipt line " + lineId);
  for (const [a, v] of Object.entries(byAlloc)) {
    const cell = line.cells[m.receipts.reference][a];
    cell.target_bn += v; cell.other_bn -= v;
  }
}
function addReprice(m, delta) {
  const cell = (d) => ({ target_bn: d, other_bn: -d, share: 0 });
  m.spending.lines.push({ id: REPRICE, family: "consumption", national_bn: 0, response_class: REPRICE,
    preferred_key: "k", alternative_key: "k", keys: { k: { personal: cell(delta.personal), shared: cell(delta.shared) } } });
}

// Lane inputs.
const EDU = model.spending.lines.find((l) => l.id === "education_services");
const schoolVariant = readJson("school_cost_where_enrolled_2026_09_24/derived/school_key_variants.json")["preferred_district_and_school_level|blend"];
const schoolDelta = {
  personal: schoolVariant.school_target_bn.personal - EDU.keys.education_mix.personal.target_bn,
  shared: schoolVariant.school_target_bn.shared - EDU.keys.education_mix.shared.target_bn,
};
const benefits = readJson("admin_benefit_keys_2026_09_24/derived/line_deltas.json").deltas.package_central;
const cbo = readJson("external_benchmarks_2026_09_24/derived/cbo_deltas.json")["all_but_medicaid|2022"];
const ota = readJson("external_benchmarks_2026_09_24/derived/ota_deltas.json").vs_adopted_raw_keys;
const OVERLAP = ["snap", "other_state_welfare", "family_and_general_assistance"];

const edits = {
  schools: (m) => addReprice(m, schoolDelta),
  benefits: (m) => { for (const [id, by] of Object.entries(benefits)) shiftKey(m, id, null, by); },
  cbo: (m, skip = []) => {
    for (const [id, by] of Object.entries(cbo.receipts)) shiftReceipt(m, id, by);
    for (const [id, byKey] of Object.entries(cbo.spending)) {
      if (skip.includes(id)) continue;
      for (const [k, by] of Object.entries(byKey)) shiftKey(m, id, k, by);
    }
  },
  ota: (m) => { for (const [id, byKey] of Object.entries(ota.spending)) for (const [k, by] of Object.entries(byKey)) shiftKey(m, id, k, by); },
};
function build(steps) {
  const m = clone(model);
  addReprice(m, { personal: 0, shared: 0 });
  const reprice = m.spending.lines.pop();
  for (const step of steps) step(m);
  if (!m.spending.lines.some((l) => l.id === REPRICE)) m.spending.lines.push(reprice);
  return m;
}

// Published values to reproduce.
const published = {};
read("main_case_2026_09_23/derived/main_case_bands.csv").trim().split("\n").slice(1).forEach((row) => {
  const [profile, variant, lo, hi] = row.split(",");
  if (variant === "adopted") published[profile] = [Number(lo), Number(hi)];
});
const adopted = published.cbo_category_lag_non_school_full;
function csvRow(rel, col, match) {
  const lines = read(rel).trim().split("\n");
  const header = lines[0].split(",");
  const rows = lines.slice(1).map((l) => l.split(","));
  return rows.filter((r) => match(Object.fromEntries(header.map((h, i) => [h, r[i]]))))
    .map((r) => Object.fromEntries(header.map((h, i) => [h, r[i]])));
}
const lanePublished = {
  schools: (() => { const r = csvRow("school_cost_where_enrolled_2026_09_24/derived/engine_school_lines.csv", null,
    (x) => x.variant === "preferred_district_and_school_level|blend")[0];
    return [Number(r.main_change_low_bn), Number(r.main_change_high_bn)]; })(),
  benefits: (() => { const r = csvRow("admin_benefit_keys_2026_09_24/derived/main_case_translation.csv", null,
    (x) => x.spec === "package_central" && x.profile === "cbo_category_lag_non_school_full")[0];
    return [Number(r.change_low_bn), Number(r.change_high_bn)]; })(),
  cbo: (() => { const rs = csvRow("external_benchmarks_2026_09_24/derived/cbo_spec_totals.csv", null,
    (x) => x.spec === "all_but_medicaid|2022");
    return [Number(rs.find((x) => x.band_end === "low").main_case_change_bn), Number(rs.find((x) => x.band_end === "high").main_case_change_bn)]; })(),
  ota: (() => { const r = csvRow("external_benchmarks_2026_09_24/derived/ota_main_case.csv", null,
    (x) => x.method === '"vs_adopted_raw_keys"' && x.profile === "cbo_category_lag_non_school_full")[0];
    return [Number(r.change_low_bn), Number(r.change_high_bn)]; })(),
};

console.log("[gates]");
const base = band(build([]));
gate("no change reproduces the adopted main case", near(base[0], adopted[0], 1e-4) && near(base[1], adopted[1], 1e-4),
  `${base[0].toFixed(4)}–${base[1].toFixed(4)} vs ${adopted[0]}–${adopted[1]}`);
const rows = [["spec", "cost_low_bn", "cost_high_bn", "change_low_bn", "change_high_bn"]];
const record = (spec, b) => { rows.push([spec, b[0].toFixed(4), b[1].toFixed(4), (b[0] - base[0]).toFixed(4), (b[1] - base[1]).toFixed(4)]); return b; };
record("adopted", base);

for (const lane of ["schools", "benefits", "cbo", "ota"]) {
  const b = record(`${lane}_alone`, band(build([edits[lane]])));
  const got = [b[0] - base[0], b[1] - base[1]];
  const want = lanePublished[lane];
  gate(`${lane} alone reproduces its lane`, near(got[0], want[0], 1e-3) && near(got[1], want[1], 1e-3),
    `${got[0].toFixed(3)} / ${got[1].toFixed(3)} vs ${want[0].toFixed(3)} / ${want[1].toFixed(3)}`);
}
const combined = record("combined_benefits_on_overlap", band(build([
  edits.schools, edits.benefits, (m) => edits.cbo(m, OVERLAP), edits.ota])));
const combinedAlt = record("combined_cbo_also_on_overlap", band(build([
  edits.schools, edits.benefits, (m) => edits.cbo(m), edits.ota])));
const taxesOnly = record("cbo_without_overlap_plus_ota", band(build([(m) => edits.cbo(m, OVERLAP), edits.ota])));

fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
fs.writeFileSync(path.join(HERE, "derived", "combined_bands.csv"), rows.map((r) => r.join(",")).join("\n") + "\n");
console.log("\n[result]");
for (const r of rows.slice(1)) console.log(`  ${r[0].padEnd(32)} ${r[1]}–${r[2]}  (${r[3]} / ${r[4]})`);
if (failures) { console.error(`FAIL: ${failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
