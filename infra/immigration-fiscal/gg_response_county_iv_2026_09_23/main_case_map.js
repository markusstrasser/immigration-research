/* Map the lane's local elasticity into the adopted main case (proposal only; the operator adopts).
 *
 * Gate A: main_case_2026_09_23/main_case.js runs to "all gates passed". It runs under
 *   no_write_hook.js, so nothing is written into that lane; each write it attempts is compared
 *   with the file on disk and must be identical (its published outputs are current).
 * Gate B: this evaluator, which repeats main_case.js's "adopted" construction on the explorer's
 *   engine (assumption_explorer_2026_09_21/engine.js) and executed model, reproduces the adopted
 *   main band $203.207-249.640bn at general-government responses 0.59 / 0.84.
 * Then, if derived/estimates_summary.json exists (estimate.py), each elasticity it lists is put in
 * place of the cross-state state-local administration elasticity in scaling_check.py's composite:
 *   low(b)  = (state_local * b + federal_tax_financial * b_financial) / total general public service
 *   high(b) = b
 * with b_financial the cross-state financial-administration elasticity (0.789), unchanged. The main
 * case is evaluated at low(b) with the low uncompensated-care key and at high(b) with the high one,
 * as main_case.js builds its adopted band. Output: derived/main_case_map.csv, derived/main_case_gates.json.
 * Run from the repository root: node infra/immigration-fiscal/gg_response_county_iv_2026_09_23/main_case_map.js
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const MAIN = path.join(FISCAL, "main_case_2026_09_23");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const cj = JSON.parse(fs.readFileSync(path.join(FISCAL, "cj_use_allocation_2026_09_23", "derived", "summary.json"), "utf8"));
const uc = JSON.parse(fs.readFileSync(path.join(FISCAL, "uncompensated_care_2026_09_23", "derived", "summary.json"), "utf8"));
const gates = JSON.parse(fs.readFileSync(path.join(HERE, "derived", "gates.json"), "utf8"));

const results = [];
function gate(label, ok, detail) {
  results.push({ gate: label, pass: !!ok, detail });
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? ": " + detail : ""}`);
}

// Gate A
const report = path.join(HERE, "_cache", "main_case_writes.jsonl");
fs.mkdirSync(path.join(HERE, "_cache"), { recursive: true });
if (fs.existsSync(report)) fs.unlinkSync(report);
const run = spawnSync(process.execPath, ["-r", path.join(HERE, "no_write_hook.js"), path.join(MAIN, "main_case.js")],
  { env: Object.assign({}, process.env, { NO_WRITE_ROOT: MAIN, NO_WRITE_REPORT: report }), encoding: "utf8" });
const writes = fs.existsSync(report) ? fs.readFileSync(report, "utf8").trim().split("\n").filter(Boolean).map(JSON.parse) : [];
gate("main_case.js reports all gates passed", run.status === 0 && /all gates passed/.test(run.stdout),
  `exit ${run.status}`);
gate("main_case.js outputs on disk are current", writes.length === 2 && writes.every((w) => w.identical),
  writes.map((w) => `${path.basename(w.path)} ${w.identical ? "identical" : "DIFFERS"}`).join(", "));

// Gate B: the adopted construction, main profile.
const MAIN_PROFILE = { other_education_response: 1, delayed_response: 0, school_response_band: [0.63, 0.66] };
function span(m, extra) {
  const state = Object.assign(Engine.defaultState(m), MAIN_PROFILE, extra || {});
  return Engine.unresolvedRange(m, state, "welfare_bn");
}
function shifted(m, lineId, delta) {
  const out = JSON.parse(JSON.stringify(m));
  const line = out.spending.lines.find((l) => l.id === lineId);
  const key = line.keys[line.preferred_key];
  ["personal", "shared"].forEach((a) => { key[a].target_bn += delta; key[a].other_bn -= delta; });
  return out;
}
const J = cj.central.change_bn;
const UC = [uc["inside_undercharged_bn_use_1.0"][0], uc["inside_undercharged_bn_use_1.0"][1]];
const lowModel = shifted(shifted(model, "public_order_safety", J), "medicaid_and_chip_other_medical", UC[0]);
const highModel = shifted(shifted(model, "public_order_safety", J), "medicaid_and_chip_other_medical", UC[1]);
function band(ggLow, ggHigh) {
  const least = span(lowModel, { general_government_response: ggLow });
  const most = span(highModel, { general_government_response: ggHigh });
  return [-least[1], -most[0]];
}
const adopted = band(0.59, 0.84);
gate("evaluator reproduces adopted main band", Math.abs(adopted[0] - 203.207) < 5e-4 && Math.abs(adopted[1] - 249.640) < 5e-4,
  `${adopted[0].toFixed(3)} to ${adopted[1].toFixed(3)} bn`);
const ggLine = model.spending.lines.find((l) => l.id === "general_public_services").keys.population.personal.target_bn;
const slope = band(0.60, 0.60)[0] - band(0.59, 0.59)[0];
gate("band is linear in the response, slope = general-government target", Math.abs(slope / 0.01 - ggLine) < 1e-6,
  `${(slope / 0.01).toFixed(4)} bn per unit response vs line ${ggLine.toFixed(4)}`);

const sc = gates.scaling_check;
function composite(b) {
  return { low: (sc.state_local_bn * b + sc.federal_tax_financial_bn * sc.financial_admin_elasticity) / sc.total_bn, high: b };
}
const control = composite(sc.admin_elasticity);
gate("composite positive control (cross-state 0.842)", Math.abs(control.low - sc.composite_low_unrounded) < 1e-12,
  `low ${control.low.toFixed(4)}, high ${control.high.toFixed(4)}`);

const failed = results.filter((r) => !r.pass);
fs.writeFileSync(path.join(HERE, "derived", "main_case_gates.json"), JSON.stringify({ gates: results,
  adopted_band_bn: adopted, general_government_target_bn: ggLine }, null, 1) + "\n");
if (failed.length) { console.error(`[BLOCKED] ${failed.length} gate(s) failed`); process.exit(1); }
console.log("all main-case gates passed");

const summaryPath = path.join(HERE, "derived", "estimates_summary.json");
if (!fs.existsSync(summaryPath)) { console.log("no estimates_summary.json yet: gates only"); process.exit(0); }
const summary = JSON.parse(fs.readFileSync(summaryPath, "utf8"));
// main_case_low/high follow the adopted construction (low composite with the low uncompensated-care key,
// high composite with the high one); for a negative elasticity the "high" composite is the smaller, so
// band_min/band_max give the ordered band.
const rows = [["label", "elasticity", "composite_low", "composite_high", "main_case_low_bn", "main_case_high_bn",
  "band_min_bn", "band_max_bn", "change_vs_adopted_low_bn", "change_vs_adopted_high_bn"]];
function push(label, b, cl, ch, lo, hi) {
  rows.push([label, b, cl, ch, lo.toFixed(3), hi.toFixed(3), Math.min(lo, hi).toFixed(3), Math.max(lo, hi).toFixed(3),
    (lo - adopted[0]).toFixed(3), (hi - adopted[1]).toFixed(3)]);
}
function add(label, b) {
  const c = composite(b);
  const [lo, hi] = band(c.low, c.high);
  push(label, b.toFixed(4), c.low.toFixed(4), c.high.toFixed(4), lo, hi);
}
push("adopted (rounded composite 0.59/0.84)", sc.admin_elasticity.toFixed(4), "0.59", "0.84", adopted[0], adopted[1]);
const zero = band(0, 0);
push("general government fixed (response 0)", "", "0", "0", zero[0], zero[1]);
add("cross-state 0.842 unrounded", sc.admin_elasticity);
for (const item of summary.map_points) add(item.label, item.elasticity);
fs.writeFileSync(path.join(HERE, "derived", "main_case_map.csv"), rows.map((r) => r.join(",")).join("\n") + "\n");
console.log(rows.map((r) => r.join(",")).join("\n"));
