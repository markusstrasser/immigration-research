/* The main case's key variants on the September 23 and September 24 cases, for the real-costs totals.
 *
 * The real-costs memo (research/immigration-real-fiscal-and-social-costs-2026-09-23.md, §7) pairs the
 * fiscal band with the social items on two crime footings and stacks a full span. It reads four variants
 * of the September 23 case from main_case_2026_09_23/derived/main_case_bands.csv: justice keyed with the
 * census ethnicity codes as recorded, the justice grid's two ends, and uncompensated care at 0.7x use.
 * The September 24 lane wrote none of them. This script evaluates them on both cases with the package's
 * own evaluator (package.cjs cost(), the 64 main specifications):
 *   - raw coding and 0.7x use are executed keys (use_raw_coding, uninsured_use_07_low/high), and the
 *     payload carries every correction to them (package.cjs KEY_FAMILIES);
 *   - the grid ends and CBP held fixed are the justice lane's changes relative to its central, applied as
 *     a target shift on the use key, as main_case_2026_09_23/main_case.js applied them to the per-head key.
 *     On the September 24 case the booking correction therefore stays at its use-key value on the grid.
 * Gates (exit 1, nothing written): every variant on the uncorrected model reproduces the September 23
 * file (1e-4, its rounding); the corrected model reproduces the adopted September 24 band (1e-9 against
 * summary.json); the payload moves raw coding and use by the same amount (1e-9).
 *
 * Run from anywhere: node band_variants.cjs  ->  derived/band_variants.csv, derived/band_variants.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const P = require(path.join(__dirname, "..", "main_case_2026_09_24", "package.cjs"));
const { Engine, MODEL, FISCAL, MAIN_SPECS, CONSTANTS, cost, span, csvRows, readJson } = P;

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
const near = (a, b, tol) => Math.abs(a - b) < tol;
const f4 = (b) => `${b[0].toFixed(4)}–${b[1].toFixed(4)}`;
const sha = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");

const SOURCES = {
  corrections: "main_case_2026_09_24/derived/corrections.json",
  summary24: "main_case_2026_09_24/derived/summary.json",
  bands23: "main_case_2026_09_23/derived/main_case_bands.csv",
  justice: "cj_use_allocation_2026_09_23/derived/summary.json",
};
const cj = readJson(SOURCES.justice);
const JUSTICE = { central: cj.central.change_bn, raw_coding: cj.one_at_a_time_change_bn.scaling_raw,
  grid_low: cj.range_change_bn[0], grid_high: cj.range_change_bn[1], cbp_fixed: cj.one_at_a_time_change_bn.cbp_zero };

// A target shift on one key of a line, in both allocations, national total conserved.
function shiftKey(m, lineId, key, delta) {
  const out = JSON.parse(JSON.stringify(m));
  const line = out.spending.lines.find((l) => l.id === lineId);
  if (!line || !line.keys[key]) throw new Error(`no key ${lineId}/${key}`);
  for (const a of ["personal", "shared"]) { line.keys[key][a].target_bn += delta; line.keys[key][a].other_bn -= delta; }
  return out;
}
const RAW = { justice: "use_raw_coding" };
const UC07 = { uc: { uninsured_use_low: "uninsured_use_07_low", uninsured_use_high: "uninsured_use_07_high" } };
function specsWith(change) {
  return MAIN_SPECS.map((s) => ({ ...s,
    ...(change.justice ? { justice: change.justice } : {}),
    ...(change.uc ? { uc: change.uc[s.uc] } : {}) }));
}
const grid = (end) => (m) => shiftKey(m, "public_order_safety", "use", JUSTICE[end] - JUSTICE.central);
const VARIANTS = [
  // name, spec change, model change, September 23 row it must reproduce (null: none published)
  ["adopted", {}, null, "adopted"],
  ["justice_raw_coding", RAW, null, "adopted_justice_raw_coding"],
  ["justice_grid_low", {}, grid("grid_low"), "adopted_justice_grid_low"],
  ["justice_grid_high", {}, grid("grid_high"), "adopted_justice_grid_high"],
  ["justice_cbp_fixed", {}, grid("cbp_fixed"), "adopted_justice_cbp_fixed"],
  ["uncompensated_use_0.7", UC07, null, "adopted_uncompensated_use_0.7"],
  ["justice_grid_low_and_uncompensated_use_0.7", UC07, grid("grid_low"), null],
];
const bandOf = (m, specs) => span(specs.map((s) => cost(m, s)));

const published23 = {};
csvRows(SOURCES.bands23).filter((r) => r.profile === "cbo_category_lag_non_school_full")
  .forEach((r) => { published23[r.variant] = [Number(r.cost_low_bn), Number(r.cost_high_bn)]; });
const summary24 = readJson(SOURCES.summary24);
const corrected = Engine.applyCorrections(MODEL, readJson(SOURCES.corrections));

const rows = [];
const bands = {};
for (const [caseName, base] of [["sept23", MODEL], ["sept24", corrected]]) {
  console.log(`[${caseName}]`);
  for (const [name, change, modelChange, ref] of VARIANTS) {
    const m = modelChange ? modelChange(base) : base;
    const b = bandOf(m, specsWith(change));
    bands[`${caseName}|${name}`] = b;
    rows.push({ case: caseName, variant: name, low: b[0], high: b[1] });
    if (caseName === "sept23" && ref) {
      const want = published23[ref];
      gate(`${name} reproduces ${ref}`, near(b[0], want[0], 1e-4) && near(b[1], want[1], 1e-4), `${f4(b)} vs ${f4(want)}`);
    } else {
      console.log(`  ${name.padEnd(44)} ${f4(b)}`);
    }
  }
}
const a24 = bands["sept24|adopted"];
gate("corrected model reproduces the adopted September 24 band (summary.json)",
  near(a24[0], summary24.main_case[0], 1e-9) && near(a24[1], summary24.main_case[1], 1e-9), `${f4(a24)}`);
const shift = (c) => [0, 1].map((i) => bands[`${c}|justice_raw_coding`][i] - bands[`${c}|adopted`][i]);
const [s23, s24] = [shift("sept23"), shift("sept24")];
gate("the payload moves raw coding and use by the same amount", near(s23[0], s24[0], 1e-9) && near(s23[1], s24[1], 1e-9),
  `${s23.map((x) => x.toFixed(6)).join(" / ")} vs ${s24.map((x) => x.toFixed(6)).join(" / ")}`);

if (failures) { console.error(`${failures} gate(s) failed; nothing written`); process.exit(1); }
const out = path.join(__dirname, "derived");
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, "band_variants.csv"), ["case,variant,cost_low_bn,cost_high_bn"]
  .concat(rows.map((r) => [r.case, r.variant, r.low.toPrecision(15), r.high.toPrecision(15)].join(","))).join("\n") + "\n");
fs.writeFileSync(path.join(out, "band_variants.json"), JSON.stringify({
  profile: P.MAIN_PROFILE, specifications: MAIN_SPECS.length, target_population: MODEL.meta.target_population,
  care_constant_bn: CONSTANTS.care.c, justice_changes_bn: JUSTICE,
  sources_sha256: Object.fromEntries(Object.values(SOURCES).map((rel) => [rel, sha(rel)])),
}, null, 1) + "\n");
console.log(`all gates passed; ${rows.length} bands -> derived/band_variants.csv`);
