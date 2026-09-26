/* The sign-reversal figures of the complete account on the main case adopted 2026-09-26.
 *
 * The definition is main_case_2026_09_24/sign_reversal.cjs's, imported: ordinary service budgets
 * respond at a common share s, defense and existing interest stay fixed, general government responds
 * at its adopted response whatever s is, transfers and direct receipts respond fully; CBO incidence
 * rules and preferred keys. On this case general government responds at the finite-removal 0.6000
 * (least adverse end) and 0.8504 (most adverse end), and the package is this lane's corrections
 * payload. The school part responds at s like every other service, so the school responses do not
 * enter; s is itself a response, not an elasticity.
 * Gate: the September 24 columns reproduce from the imported definition before anything changes.
 * Run from anywhere: node sign_reversal.cjs  ->  derived/sign_reversal.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("./package.cjs");
const S24 = require(path.join(__dirname, "..", "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, HERE, gate, near, gateState, csvRows, correctionsPayload, RESPONSES } = P;

const pairs26 = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? RESPONSES.general_government.low : RESPONSES.general_government.high }));
const model24 = Engine.applyCorrections(MODEL, P.SEPT24);
const model26 = Engine.applyCorrections(MODEL, correctionsPayload());

console.log("[gates]");
const pub = csvRows("main_case_2026_09_24/derived/sign_reversal.csv");
const want = csvRows("main_case_2026_09_26/derived/main_case_bands.csv").find((r) => r.profile === P.MAIN_PROFILE && r.variant === "adopted");
const b = P.band(model26);
gate("the payload reproduces the adopted main case", near(b[0], +want.cost_low_bn, 1e-4) && near(b[1], +want.cost_high_bn, 1e-4),
  `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
const rows = [["measure", "sept24_low", "sept24_high", "sept26_low", "sept26_high"]];
for (const allocation of ["personal", "shared"]) {
  const b24 = S24.breakEven(model24, allocation);
  const p = pub.find((r) => r.measure === `service_break_even_${allocation}`);
  gate(`break-even, ${allocation}: September 24 reproduces`, near(b24[0], +p.sept24_low, 1e-4) && near(b24[1], +p.sept24_high, 1e-4),
    `${(100 * b24[0]).toFixed(2)}–${(100 * b24[1]).toFixed(2)}%`);
  const b26 = S24.breakEven(model26, allocation, pairs26);
  rows.push([`service_break_even_${allocation}`, b24[0], b24[1], b26[0], b26[1]]);
  // The move split: the new payload at the September 24 responses, and the new responses on the
  // September 24 payload.
  const pay = S24.breakEven(model26, allocation), resp = S24.breakEven(model24, allocation, pairs26);
  rows.push([`service_break_even_${allocation}__corrections_only`, b24[0], b24[1], pay[0], pay[1]]);
  rows.push([`service_break_even_${allocation}__responses_only`, b24[0], b24[1], resp[0], resp[1]]);
}
const f24 = S24.frozen(model24), f26 = S24.frozen(model26, pairs26);
const pf = pub.find((r) => r.measure === "frozen_services_capital_fixed_welfare_bn_cbo_preferred");
gate("frozen services: September 24 reproduces", near(f24[0], +pf.sept24_low, 1e-4) && near(f24[1], +pf.sept24_high, 1e-4),
  `${f24[0].toFixed(2)} to ${f24[1].toFixed(2)}`);
rows.push(["frozen_services_capital_fixed_welfare_bn_cbo_preferred", f24[0], f24[1], f26[0], f26[1]]);
fs.writeFileSync(path.join(HERE, "derived", "sign_reversal.csv"),
  rows.map((r) => r.map((x) => (typeof x === "number" ? x.toFixed(4) : x)).join(",")).join("\n") + "\n");

console.log("\n[result]");
for (const r of rows.slice(1)) {
  const pct = r[0].startsWith("service");
  const fmt = (x) => (pct ? `${(100 * x).toFixed(1)}%` : x.toFixed(1));
  console.log(`  ${r[0].padEnd(56)} Sept 24 ${fmt(r[1])} to ${fmt(r[2])}   Sept 26 ${fmt(r[3])} to ${fmt(r[4])}`);
}
if (gateState.failures) { console.error(`FAIL: ${gateState.failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
