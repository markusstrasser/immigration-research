/* The LTSS re-key on the adopted main case, through the explorer's evaluator.
 *
 * Rebuilds main_case_2026_09_23's adopted band (general government 0.59-0.84, justice by use,
 * uncompensated care by use) and gates it against that lane's main_case_bands.csv. Then shifts the
 * Medicaid line's target allocation by this lane's change (derived/effects.csv, national total
 * conserved) and, for the joint case, the five medical lines by the medical-ethnicity lane's
 * changes (translation_account.csv) with the Medicaid line replaced by the joint figure
 * (derived/combined.csv). Reports cost to other residents in $bn a year (positive = cost).
 * Run from the repo root: node infra/immigration-fiscal/ltss_share_2026_09_23/main_case_effect.js
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const inputs = JSON.parse(fs.readFileSync(path.join(FISCAL, "main_case_2026_09_23", "derived", "inputs.json"), "utf8"));

function csv(file) {
  const [head, ...rows] = fs.readFileSync(file, "utf8").trim().split("\n");
  const keys = head.split(",");
  return rows.map((r) => {
    const cells = r.match(/("([^"]|"")*"|[^,]*)(,|$)/g).map((c) => c.replace(/,$/, "").replace(/^"|"$/g, ""));
    return Object.fromEntries(keys.map((k, i) => [k, cells[i]]));
  });
}

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}

const MAIN = { other_education_response: 1, delayed_response: 0, school_response_band: [0.63, 0.66] };

function shifted(m, deltas) {
  const out = JSON.parse(JSON.stringify(m));
  for (const [id, delta] of Object.entries(deltas)) {
    const line = out.spending.lines.find((l) => l.id === id);
    if (!line) throw new Error("no line " + id);
    const key = line.keys[line.preferred_key];
    ["personal", "shared"].forEach((a) => { key[a].target_bn += delta; key[a].other_bn -= delta; });
  }
  return out;
}

// Adopted band: envelope over general government 0.59/0.84 and uncompensated care low/high.
function adopted(extra) {
  const lo = Object.assign({ public_order_safety: inputs.justice_change_bn.central,
    medicaid_and_chip_other_medical: inputs.uncompensated_inside_bn.equal_low }, {});
  const hi = Object.assign({ public_order_safety: inputs.justice_change_bn.central,
    medicaid_and_chip_other_medical: inputs.uncompensated_inside_bn.equal_high }, {});
  for (const [id, d] of Object.entries(extra || {})) { lo[id] = (lo[id] || 0) + d; hi[id] = (hi[id] || 0) + d; }
  const least = Engine.unresolvedRange(shifted(model, lo), Object.assign(Engine.defaultState(model), MAIN,
    { general_government_response: inputs.general_government_response.low }), "welfare_bn");
  const most = Engine.unresolvedRange(shifted(model, hi), Object.assign(Engine.defaultState(model), MAIN,
    { general_government_response: inputs.general_government_response.high }), "welfare_bn");
  return [-least[1], -most[0]];
}

const bands = csv(path.join(FISCAL, "main_case_2026_09_23", "derived", "main_case_bands.csv"));
const pub = bands.find((r) => r.profile === "cbo_category_lag_non_school_full" && r.variant === "adopted");
const base = adopted();
gate("adopted main case reproduces", Math.abs(base[0] - +pub.cost_low_bn) < 1e-3 && Math.abs(base[1] - +pub.cost_high_bn) < 1e-3,
  `${base[0].toFixed(2)} to ${base[1].toFixed(2)} bn`);

const eff = csv(path.join(HERE, "derived", "effects.csv"));
const comb = csv(path.join(HERE, "derived", "combined.csv"));
const ta = csv(path.join(FISCAL, "medical_ethnicity_pooled_2026_09_23", "derived", "translation_account.csv"));
const rows = [];
function record(label, deltas) {
  const b = adopted(deltas);
  rows.push({ label, low: b[0], high: b[1], shift_low: b[0] - base[0], shift_high: b[1] - base[1] });
}
for (const e of eff) record("ltss: " + e.variant, { medicaid_and_chip_other_medical: +e.total });
const LINES = ["medicaid_and_chip_other_medical", "medicare", "health_services", "military_medical", "veterans_other"];
for (const c of comb) {
  const deltas = {};
  for (const id of LINES) {
    const r = ta.find((x) => x.spec === c.spec && x.line === id);
    deltas[id] = +r.delta_bn;
  }
  record("medical-ethnicity lane alone: " + c.spec, Object.assign({}, deltas));
  deltas.medicaid_and_chip_other_medical += +c.ltss_change_bn + +c.remainder_ratio_adjustment_bn;
  record("joint with medical-ethnicity lane: " + c.spec, deltas);
}
const central = rows.find((r) => r.label === "ltss: central");
gate("Medicaid line responds one for one", Math.abs(central.shift_low - +eff[0].total) < 1e-6 && Math.abs(central.shift_high - +eff[0].total) < 1e-6,
  `${central.shift_low.toFixed(3)} / ${central.shift_high.toFixed(3)} bn`);
const header = "variant,cost_low_bn,cost_high_bn,shift_low_bn,shift_high_bn";
const out = [header].concat(rows.map((r) => [JSON.stringify(r.label), r.low.toFixed(4), r.high.toFixed(4),
  r.shift_low.toFixed(4), r.shift_high.toFixed(4)].join(","))).join("\n") + "\n";
fs.writeFileSync(path.join(HERE, "derived", "main_case_effect.csv"), out);
console.log(out);
if (failures) { console.error(`FAIL: ${failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
