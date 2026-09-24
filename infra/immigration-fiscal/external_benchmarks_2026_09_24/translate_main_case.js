/* Translate target-dollar changes on account lines into the adopted main case.
 *
 * Input JSON: {method: {receipts: {line: {personal, shared}}, spending: {line: {key: {personal, shared}}}}}.
 * Receipt changes move the cbo_collective cell; spending changes move the named key. National totals
 * are conserved (other_bn moves the other way). The adopted bands are recomputed exactly as
 * main_case_2026_09_23/main_case.js does, following cps_imputation_keys_2026_09_23/main_case_translate.js.
 * Gate: with no change the published adopted bands reproduce to 1e-4 bn, else exit 1.
 * Run: node translate_main_case.js deltas.json out.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");

const FISCAL = path.join(__dirname, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const inputs = JSON.parse(fs.readFileSync(path.join(FISCAL, "main_case_2026_09_23", "derived", "inputs.json"), "utf8"));
const publishedCsv = fs.readFileSync(path.join(FISCAL, "main_case_2026_09_23", "derived", "main_case_bands.csv"), "utf8");
if (process.argv.length < 4) { console.error("usage: node translate_main_case.js deltas.json out.csv"); process.exit(2); }
const deltas = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const OUT_PATH = process.argv[3];

const PROFILES = {
  cbo_category_lag_non_school_fixed: { other_education_response: 0, delayed_response: 0, school_response_band: [0.63, 0.66] },
  cbo_category_lag_non_school_full: { other_education_response: 1, delayed_response: 0, school_response_band: [0.63, 0.66] },
  proportional_reference: {},
};
const GG = inputs.general_government_response;
const JUSTICE = inputs.justice_change_bn.central;
const UC = inputs.uncompensated_inside_bn;

function span(m, settings, extra) {
  const state = Object.assign(Engine.defaultState(m), settings, extra || {});
  return Engine.unresolvedRange(m, state, "welfare_bn");
}
function shiftedPreferred(m, lineId, delta) {
  const out = JSON.parse(JSON.stringify(m));
  const line = out.spending.lines.find((l) => l.id === lineId);
  const key = line.keys[line.preferred_key];
  ["personal", "shared"].forEach((a) => { key[a].target_bn += delta; key[a].other_bn -= delta; });
  return out;
}
function applyDeltas(m, d) {
  const out = JSON.parse(JSON.stringify(m));
  for (const [id, byAlloc] of Object.entries(d.receipts || {})) {
    const line = out.receipts.lines.find((l) => l.id === id);
    if (!line) throw new Error("no receipt line " + id);
    for (const [a, v] of Object.entries(byAlloc)) {
      const cell = line.cells.cbo_collective[a];
      cell.target_bn += v; cell.other_bn -= v;
    }
  }
  for (const [id, byKey] of Object.entries(d.spending || {})) {
    const line = out.spending.lines.find((l) => l.id === id);
    if (!line) throw new Error("no spending line " + id);
    for (const [key, byAlloc] of Object.entries(byKey)) {
      if (!line.keys[key]) throw new Error("no key " + id + "/" + key);
      for (const [a, v] of Object.entries(byAlloc)) {
        line.keys[key][a].target_bn += v; line.keys[key][a].other_bn -= v;
      }
    }
  }
  return out;
}
function adoptedBand(m, settings) {
  const withAdopted = (uc) => shiftedPreferred(shiftedPreferred(m, "public_order_safety", JUSTICE), "medicaid_and_chip_other_medical", uc);
  const least = span(withAdopted(UC.equal_low), settings, { general_government_response: GG.low });
  const most = span(withAdopted(UC.equal_high), settings, { general_government_response: GG.high });
  return [-least[1], -most[0]];  // cost low, cost high
}

const published = {};
publishedCsv.trim().split("\n").slice(1).forEach((row) => {
  const [profile, variant, lo, hi] = row.split(",");
  if (variant === "adopted") published[profile] = [Number(lo), Number(hi)];
});
let failures = 0;
const rows = ["method,profile,cost_low_bn,cost_high_bn,change_low_bn,change_high_bn"];
for (const [profile, settings] of Object.entries(PROFILES)) {
  const base = adoptedBand(model, settings);
  const ok = Math.abs(base[0] - published[profile][0]) < 1e-4 && Math.abs(base[1] - published[profile][1]) < 1e-4;
  console.log(`[gate] ${profile}: ${base[0].toFixed(4)}-${base[1].toFixed(4)} vs published ${published[profile][0]}-${published[profile][1]} ${ok ? "ok" : "FAIL"}`);
  if (!ok) failures += 1;
  for (const [method, d] of Object.entries(deltas)) {
    const band = adoptedBand(applyDeltas(model, d), settings);
    rows.push([JSON.stringify(method), profile, band[0].toFixed(4), band[1].toFixed(4),
               (band[0] - base[0]).toFixed(4), (band[1] - base[1]).toFixed(4)].join(","));
  }
}
fs.writeFileSync(OUT_PATH, rows.join("\n") + "\n");
if (failures) { console.error("FAIL: published adopted bands not reproduced"); process.exit(1); }
console.log("all gates passed");
