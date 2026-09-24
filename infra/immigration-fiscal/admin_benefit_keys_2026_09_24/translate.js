/* Translate the re-keyed union dollars into the adopted main case.
 *
 * Reads derived/line_deltas.json (compare.py): per specification or package, the change in the
 * union's dollars on each account line by allocation. Shifts the explorer model's preferred key on
 * that line (national totals conserved: other_bn moves the other way) and recomputes the adopted
 * bands exactly as main_case_2026_09_23/main_case.js does, as the CPS imputation lane's
 * main_case_translate.js does. Gate: with zero deltas the published adopted bands reproduce to
 * 1e-4 bn for all three profiles.
 * Writes derived/main_case_translation.csv.
 * Run from the repo root: node infra/immigration-fiscal/admin_benefit_keys_2026_09_24/translate.js
 */
"use strict";
const fs = require("fs");
const path = require("path");

const FISCAL = path.join(__dirname, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const inputs = JSON.parse(fs.readFileSync(path.join(FISCAL, "main_case_2026_09_23", "derived", "inputs.json"), "utf8"));
const deltas = JSON.parse(fs.readFileSync(path.join(__dirname, "derived", "line_deltas.json"), "utf8")).deltas;
const publishedCsv = fs.readFileSync(path.join(FISCAL, "main_case_2026_09_23", "derived", "main_case_bands.csv"), "utf8");

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
function shiftPreferred(m, lineId, byAlloc) {
  const out = JSON.parse(JSON.stringify(m));
  const line = out.spending.lines.find((l) => l.id === lineId);
  if (!line) throw new Error("no spending line " + lineId);
  const key = line.keys[line.preferred_key];
  for (const [a, v] of Object.entries(byAlloc)) {
    if (!(a in key)) throw new Error("no allocation " + a + " on " + lineId);
    key[a].target_bn += v; key[a].other_bn -= v;
  }
  return out;
}
function applyDeltas(m, d) {
  let out = m;
  for (const [lineId, byAlloc] of Object.entries(d)) out = shiftPreferred(out, lineId, byAlloc);
  return out;
}
function adoptedBand(m, settings) {
  const withAdopted = (uc) => shiftPreferred(shiftPreferred(m, "public_order_safety", { personal: JUSTICE, shared: JUSTICE }),
    "medicaid_and_chip_other_medical", { personal: uc, shared: uc });
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
const rows = ["spec,profile,cost_low_bn,cost_high_bn,change_low_bn,change_high_bn"];
for (const [profile, settings] of Object.entries(PROFILES)) {
  const base = adoptedBand(model, settings);
  const ok = Math.abs(base[0] - published[profile][0]) < 1e-4 && Math.abs(base[1] - published[profile][1]) < 1e-4;
  console.log(`[gate] ${profile}: ${base[0].toFixed(4)}-${base[1].toFixed(4)} vs published ${published[profile][0]}-${published[profile][1]} ${ok ? "ok" : "FAIL"}`);
  if (!ok) failures += 1;
  rows.push(["published", profile, base[0].toFixed(4), base[1].toFixed(4), "0", "0"].join(","));
  for (const [spec, d] of Object.entries(deltas)) {
    const band = adoptedBand(applyDeltas(model, d), settings);
    rows.push([spec, profile, band[0].toFixed(4), band[1].toFixed(4), (band[0] - base[0]).toFixed(4), (band[1] - base[1]).toFixed(4)].join(","));
    if (profile === "cbo_category_lag_non_school_full" && spec.startsWith("package_")) {
      console.log(`[main] ${spec}: ${band[0].toFixed(1)}-${band[1].toFixed(1)} (change ${(band[0] - base[0]).toFixed(2)} / ${(band[1] - base[1]).toFixed(2)})`);
    }
  }
}
fs.writeFileSync(path.join(__dirname, "derived", "main_case_translation.csv"), rows.join("\n") + "\n");
if (failures) { console.error("FAIL: published adopted bands not reproduced"); process.exit(1); }
console.log("all gates passed");
