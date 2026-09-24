/* Inputs for propagate.py --case sept24: the adopted September 24 main case, specification by
 * specification, from the explorer engine.
 *
 * Writes derived/sept24/spec_costs.csv (the 64 main specifications of main_case_2026_09_24/package.cjs,
 * each costed on the September 23 frame and on the corrected model) and derived/sept24/line_targets.csv
 * (the group's target on every receipt line at the reference incidence rule and on every spending line
 * and key, before and after main_case_2026_09_24/derived/corrections.json; the synthetic correction
 * lines appear only after). Gates (exit 1, nothing written): the two sets of costs span the published
 * September 23 and September 24 bands (main_case_2026_09_24/derived/summary.json, 1e-9).
 *
 * Run from anywhere: node sept24_specs.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_2026_09_24", "package.cjs"));
const { Engine, MODEL, FISCAL, MAIN_SPECS, ALLOCS, cost, span, readJson } = P;

const corrected = Engine.applyCorrections(MODEL, readJson("main_case_2026_09_24/derived/corrections.json"));
const summary = readJson("main_case_2026_09_24/derived/summary.json");
let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}

const specs = MAIN_SPECS.map((s) => ({ ...s, sept23: cost(MODEL, s), sept24: cost(corrected, s) }));
for (const [c, want] of [["sept23", summary.adopted_2026_09_23], ["sept24", summary.main_case]]) {
  const b = span(specs.map((s) => s[c]));
  gate(`${c} specifications span the published band`, Math.abs(b[0] - want[0]) < 1e-9 && Math.abs(b[1] - want[1]) < 1e-9,
    `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
}

const ref = MODEL.receipts.reference;
const targets = [];
for (const line of corrected.receipts.lines) {
  const before = MODEL.receipts.lines.find((l) => l.id === line.id);
  for (const a of ALLOCS) {
    targets.push(["receipt", line.id, ref, a, before.cells[ref][a].target_bn, line.cells[ref][a].target_bn]);
  }
}
for (const line of corrected.spending.lines) {
  const before = MODEL.spending.lines.find((l) => l.id === line.id);
  for (const [key, k] of Object.entries(line.keys)) {
    for (const a of ALLOCS) {
      targets.push(["spending", line.id, key, a, before ? before.keys[key][a].target_bn : "", k[a].target_bn]);
    }
  }
}

if (failures) { console.error(`${failures} gate(s) failed; nothing written`); process.exit(1); }
const out = path.join(__dirname, "derived", "sept24");
fs.mkdirSync(out, { recursive: true });
const dims = Object.keys(MAIN_SPECS[0]);
fs.writeFileSync(path.join(out, "spec_costs.csv"), [dims.concat(["cost_sept23_bn", "cost_sept24_bn"]).join(",")]
  .concat(specs.map((s) => dims.map((d) => s[d]).concat([s.sept23.toPrecision(15), s.sept24.toPrecision(15)]).join(",")))
  .join("\n") + "\n");
fs.writeFileSync(path.join(out, "line_targets.csv"), ["side,line,key,allocation,target_sept23_bn,target_sept24_bn"]
  .concat(targets.map((r) => r.map((x) => (typeof x === "number" ? x.toPrecision(15) : x)).join(","))).join("\n") + "\n");
console.log(`all gates passed; ${specs.length} specifications, ${targets.length} line targets -> ${path.relative(FISCAL, out)}`);
