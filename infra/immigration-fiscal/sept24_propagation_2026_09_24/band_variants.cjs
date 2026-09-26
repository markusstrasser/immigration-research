/* The main case's key variants on the September 23 case and every adopted case since, for the real-costs
 * totals.
 *
 * The real-costs memo (research/immigration-real-fiscal-and-social-costs-2026-09-23.md, §7) pairs the
 * fiscal band with the social items on two crime footings and stacks a full span. It reads four variants
 * of the September 23 case from main_case_2026_09_23/derived/main_case_bands.csv: justice keyed with the
 * census ethnicity codes as recorded, the justice grid's two ends, and uncompensated care at 0.7x use.
 * The September 24 lane wrote none of them. This script evaluates them on each case with the package's
 * own evaluator (package.cjs cost(), the 64 main specifications):
 *   - raw coding and 0.7x use are executed keys (use_raw_coding, uninsured_use_07_low/high), and the
 *     payload carries every correction to them (package.cjs KEY_FAMILIES);
 *   - the grid ends and CBP held fixed are the justice lane's changes relative to its central, applied as
 *     a target shift on the use key, as main_case_2026_09_23/main_case.js applied them to the per-head key.
 *     On the adopted cases the booking correction therefore stays at its use-key value on the grid.
 *
 * Cases (--case). Every run evaluates the September 23 case (the uncorrected model at 0.59/0.84 and
 * 0.63/0.66) and the September 24 case. A later case adds its own two runs: the uncorrected model and
 * its corrections.json, both at the responses in the payload's meta.responses, never typed here.
 *   sept24          main_case_2026_09_24 (the committed run)           -> derived/
 *   sept26          main_case_2026_09_26, the one-year scenario        -> --out-dir DIR only
 *   sept26_schools  main_case_schools_full_2026_09_26, schools at full
 *                   average cost, the main case (default)              -> ../sept26_propagation_2026_09_26/derived/
 * Gates (exit 1, nothing written): every variant on the uncorrected model reproduces the September 23
 * file (1e-4, its rounding); the corrected model reproduces the adopted September 24 band (1e-9 against
 * summary.json); the payload moves raw coding and use by the same amount (1e-9). On a later case: its
 * meta.responses equal its summary.json's, and the specifications built from them equal its package's
 * MAIN_SPECS; the adopted variant reproduces the case's band and, on the uncorrected model,
 * uncorrected_at_adopted_responses (1e-9 against summary.json, 1e-4 against main_case_bands.csv); each
 * variant moves every specification by the same amount on the uncorrected and corrected model (1e-9).
 *
 * Run from anywhere: node band_variants.cjs [--case sept24|sept26|sept26_schools] [--out-dir DIR]
 *   -> DIR/band_variants.csv, DIR/band_variants.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const CASES = {
  sept24: { lane: "main_case_2026_09_24", out: path.join(__dirname, "derived") },
  sept26: { lane: "main_case_2026_09_26", out: null },
  sept26_schools: { lane: "main_case_schools_full_2026_09_26",
    out: path.join(__dirname, "..", "sept26_propagation_2026_09_26", "derived") },
};
const argv = process.argv.slice(2);
function opt(name, dflt) {
  const i = argv.indexOf(name);
  if (i < 0) return dflt;
  if (!argv[i + 1] || argv[i + 1].startsWith("--")) { console.error(`${name} needs a value`); process.exit(2); }
  return argv[i + 1];
}
const CASE = opt("--case", "sept26_schools");
if (!CASES[CASE]) { console.error(`unknown --case ${CASE}; one of ${Object.keys(CASES).join(", ")}`); process.exit(2); }
const OUT = opt("--out-dir", null) ? path.resolve(opt("--out-dir")) : CASES[CASE].out;
if (!OUT) { console.error(`--case ${CASE} writes only to --out-dir DIR`); process.exit(2); }
const LANE = CASES[CASE].lane;
const LATER = CASE !== "sept24";

const P = require(path.join(__dirname, "..", LANE, "package.cjs"));
const P24 = P.P24 || P;  // the September 24 package, which the later packages import unchanged
const { Engine, MODEL, FISCAL, CONSTANTS, cost, span, csvRows, readJson } = P;

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
if (LATER) {
  Object.assign(SOURCES, { case_corrections: `${LANE}/derived/corrections.json`, case_summary: `${LANE}/derived/summary.json`,
    case_bands: `${LANE}/derived/main_case_bands.csv` });
}
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
function specsWith(specs, change) {
  return specs.map((s) => ({ ...s,
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

const published23 = {};
csvRows(SOURCES.bands23).filter((r) => r.profile === "cbo_category_lag_non_school_full")
  .forEach((r) => { published23[r.variant] = [Number(r.cost_low_bn), Number(r.cost_high_bn)]; });
const summary24 = readJson(SOURCES.summary24);
const corrected = Engine.applyCorrections(MODEL, readJson(SOURCES.corrections));

// Runs: [name, model, specifications]. A later case's specifications are the September 24 ones with the
// responses of its meta.responses in place of 0.59/0.84 and 0.63/0.66, value for value.
const RUNS = [["sept23", MODEL, P24.MAIN_SPECS], ["sept24", corrected, P24.MAIN_SPECS]];
let payload = null, summary = null, published = null;
if (LATER) {
  console.log(`[${CASE}: ${LANE}]`);
  payload = readJson(SOURCES.case_corrections);
  summary = readJson(SOURCES.case_summary);
  const r = payload.meta.responses;
  gate("the payload's meta.responses equal the case's summary.json responses", JSON.stringify(r) === JSON.stringify(summary.responses));
  const specs = P24.MAIN_SPECS.map((s) => ({ ...s,
    gg: s.gg === P.GG24[0] ? r.general_government.low : r.general_government.high,
    school: s.school === P.SCHOOL24[0] ? r.school.growth : r.school.decline }));
  gate("the specifications at meta.responses equal the package's MAIN_SPECS", JSON.stringify(specs) === JSON.stringify(P.MAIN_SPECS),
    `general government ${r.general_government.low}/${r.general_government.high}, schools ${r.school.growth}/${r.school.decline}`);
  published = {};
  csvRows(SOURCES.case_bands).filter((x) => x.profile === P.MAIN_PROFILE)
    .forEach((x) => { published[x.variant] = [Number(x.cost_low_bn), Number(x.cost_high_bn)]; });
  RUNS.push([`${CASE}_uncorrected`, MODEL, specs], [CASE, Engine.applyCorrections(MODEL, payload), specs]);
}

const rows = [];
const bands = {};
const perSpec = {};
for (const [caseName, base, specs] of RUNS) {
  console.log(`[${caseName}]`);
  for (const [name, change, modelChange, ref] of VARIANTS) {
    const m = modelChange ? modelChange(base) : base;
    const costs = specsWith(specs, change).map((s) => cost(m, s));
    const b = span(costs);
    bands[`${caseName}|${name}`] = b;
    perSpec[`${caseName}|${name}`] = costs;
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
if (LATER) {
  const [unc, cor] = [`${CASE}_uncorrected`, CASE];
  for (const [run, key, label] of [[cor, "main_case", "adopted"], [unc, "uncorrected_at_adopted_responses", "uncorrected_at_adopted_responses"]]) {
    const b = bands[`${run}|adopted`];
    gate(`${run} reproduces ${LANE} ${key} (summary.json, 1e-9)`, near(b[0], summary[key][0], 1e-9) && near(b[1], summary[key][1], 1e-9), f4(b));
    gate(`${run} reproduces ${LANE} main_case_bands.csv ${label} (1e-4)`,
      near(b[0], published[label][0], 1e-4) && near(b[1], published[label][1], 1e-4), `${f4(b)} vs ${f4(published[label])}`);
  }
  for (const [name] of VARIANTS.slice(1)) {
    const move = (run) => perSpec[`${run}|${name}`].map((x, i) => x - perSpec[`${run}|adopted`][i]);
    const [mu, mc] = [move(unc), move(cor)];
    const gap = Math.max(...mu.map((x, i) => Math.abs(x - mc[i])));
    gate(`${name} moves every specification by the same amount on the uncorrected and corrected ${CASE} model`, gap < 1e-9,
      `max gap ${gap.toExponential(1)}`);
  }
}

if (failures) { console.error(`${failures} gate(s) failed; nothing written`); process.exit(1); }
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "band_variants.csv"), ["case,variant,cost_low_bn,cost_high_bn"]
  .concat(rows.map((r) => [r.case, r.variant, r.low.toPrecision(15), r.high.toPrecision(15)].join(","))).join("\n") + "\n");
const meta = { profile: P.MAIN_PROFILE, specifications: P.MAIN_SPECS.length, target_population: MODEL.meta.target_population,
  care_constant_bn: CONSTANTS.care.c, justice_changes_bn: JUSTICE };
if (LATER) {
  Object.assign(meta, { case: CASE, package: `${LANE}/package.cjs`, responses: payload.meta.responses,
    runs: { sept23: "uncorrected model at 0.59/0.84 and 0.63/0.66 (the September 23 case)",
      sept24: "main_case_2026_09_24 corrections at 0.59/0.84 and 0.63/0.66",
      [`${CASE}_uncorrected`]: "uncorrected model at the responses in the payload's meta.responses",
      [CASE]: `${LANE} corrections at the responses in the payload's meta.responses` } });
}
meta.sources_sha256 = Object.fromEntries(Object.values(SOURCES).map((rel) => [rel, sha(rel)]));
fs.writeFileSync(path.join(OUT, "band_variants.json"), JSON.stringify(meta, null, 1) + "\n");
console.log(`all gates passed; ${rows.length} bands -> ${path.relative(process.cwd(), path.join(OUT, "band_variants.csv"))}`);
