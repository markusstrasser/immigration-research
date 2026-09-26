/* Inputs for propagate.py --case sept24 and each later case: the adopted main cases, specification by
 * specification, from the explorer engine.
 *
 * Writes derived/sept24/spec_costs.csv (the 64 main specifications of main_case_2026_09_24/package.cjs,
 * each costed on the September 23 frame and on the corrected model) and derived/sept24/line_targets.csv
 * (the group's target on every receipt line at the reference incidence rule and on every spending line
 * and key, before and after main_case_2026_09_24/derived/corrections.json; the synthetic correction
 * lines appear only after). Gates (exit 1, nothing written): the two sets of costs span the published
 * September 23 and September 24 bands (main_case_2026_09_24/derived/summary.json, 1e-9).
 *
 * Since 2026-09-26 it also writes derived/<case>/ for each later case in later_cases.json (case -> main-case
 * lane; sept26, CBO's one-year school response, then sept26_schools, schools at full average cost): the
 * same 64 specifications with that case's responses (engine state, read from the lane's
 * derived/corrections.json meta.responses; school_sept24 and gg_sept24 keep the September 24 values each
 * replaced), costed on the uncorrected model and on the model with that payload, and the line targets
 * before and after the payload. Gates: the mapped specifications equal that lane's package.cjs MAIN_SPECS,
 * and the costs span its uncorrected_at_adopted_responses and main_case bands (summary.json, 1e-9). The
 * files of earlier cases do not change.
 *
 * Run from anywhere: node sept24_specs.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_2026_09_24", "package.cjs"));
const P26 = require(path.join(__dirname, "..", "main_case_2026_09_26", "package.cjs"));
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

// The group's target on every executed cell of `after`, beside the uncorrected model's.
function lineTargets(after) {
  const ref = MODEL.receipts.reference;
  const rows = [];
  for (const line of after.receipts.lines) {
    const before = MODEL.receipts.lines.find((l) => l.id === line.id);
    for (const a of ALLOCS) {
      rows.push(["receipt", line.id, ref, a, before.cells[ref][a].target_bn, line.cells[ref][a].target_bn]);
    }
  }
  for (const line of after.spending.lines) {
    const before = MODEL.spending.lines.find((l) => l.id === line.id);
    for (const [key, k] of Object.entries(line.keys)) {
      for (const a of ALLOCS) {
        rows.push(["spending", line.id, key, a, before ? before.keys[key][a].target_bn : "", k[a].target_bn]);
      }
    }
  }
  return rows;
}
const targets = lineTargets(corrected);

// Later cases (later_cases.json: case -> main-case lane, one line each): responses from that lane's
// payload, each September 24 value replaced by its adopted counterpart.
const { GG24, SCHOOL24 } = P26;
const swap = (v, old, now) => (v === old[0] ? now[0] : v === old[1] ? now[1] : NaN);
const later = Object.entries(JSON.parse(fs.readFileSync(path.join(__dirname, "later_cases.json"), "utf8")))
  .map(([name, lane]) => {
    const PC = require(path.join(__dirname, "..", lane, "package.cjs"));
    const payload = readJson(`${lane}/derived/corrections.json`);
    const sum = readJson(`${lane}/derived/summary.json`);
    const R = payload.meta.responses;
    gate(`${name}: payload responses equal summary.json responses`, JSON.stringify(R) === JSON.stringify(sum.responses));
    const rows = MAIN_SPECS.map((s) => ({ ...s,
      gg: swap(s.gg, GG24, [R.general_government.low, R.general_government.high]),
      school: swap(s.school, SCHOOL24, [R.school.growth, R.school.decline]),
      school_sept24: s.school, gg_sept24: s.gg }));
    gate(`${name}: adopted responses replace the September 24 ones one for one (${lane}/package.cjs MAIN_SPECS)`,
      rows.length === PC.MAIN_SPECS.length &&
      rows.every((s, i) => Object.entries(PC.MAIN_SPECS[i]).every(([k, v]) => s[k] === v)),
      `general government ${R.general_government.low.toFixed(4)}/${R.general_government.high.toFixed(4)}, ` +
      `schools ${R.school.growth.toFixed(4)}/${R.school.decline.toFixed(4)}`);
    const model = Engine.applyCorrections(MODEL, payload);
    for (const s of rows) { s.uncorrected = cost(MODEL, s); s[name] = cost(model, s); }
    for (const [c, want] of [["uncorrected", sum.uncorrected_at_adopted_responses], [name, sum.main_case]]) {
      const b = span(rows.map((s) => s[c]));
      gate(`${name}: ${c} specifications span the published band`,
        Math.abs(b[0] - want[0]) < 1e-9 && Math.abs(b[1] - want[1]) < 1e-9, `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
    }
    return { name, rows, targets: lineTargets(model) };
  });

if (failures) { console.error(`${failures} gate(s) failed; nothing written`); process.exit(1); }
const num = (x) => (typeof x === "number" ? x.toPrecision(15) : x);
function write(dir, dims, costCols, rows, targetCols, targetRows) {
  const out = path.join(__dirname, "derived", dir);
  fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, "spec_costs.csv"), [dims.concat(costCols.map(([name]) => name)).join(",")]
    .concat(rows.map((s) => dims.map((d) => s[d]).concat(costCols.map(([, c]) => s[c].toPrecision(15))).join(",")))
    .join("\n") + "\n");
  fs.writeFileSync(path.join(out, "line_targets.csv"), [["side", "line", "key", "allocation"].concat(targetCols).join(",")]
    .concat(targetRows.map((r) => r.map(num).join(","))).join("\n") + "\n");
  console.log(`${rows.length} specifications, ${targetRows.length} line targets -> ${path.relative(FISCAL, out)}`);
}
const dims = Object.keys(MAIN_SPECS[0]);
write("sept24", dims, [["cost_sept23_bn", "sept23"], ["cost_sept24_bn", "sept24"]], specs,
  ["target_sept23_bn", "target_sept24_bn"], targets);
for (const c of later) {
  write(c.name, dims.concat(["school_sept24", "gg_sept24"]),
    [["cost_uncorrected_bn", "uncorrected"], [`cost_${c.name}_bn`, c.name]], c.rows,
    ["target_uncorrected_bn", `target_${c.name}_bn`], c.targets);
}
console.log("all gates passed");
