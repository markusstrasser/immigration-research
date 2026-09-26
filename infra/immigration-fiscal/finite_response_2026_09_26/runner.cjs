/* Reproduce the adopted September 24 main case, then replace its elasticity-derived responses with
 * finite-removal responses from derived/r_values.json. Imports the main case's own package, as
 * sign_reversal.cjs does, mutates its specs in memory only, and writes derived/runs.json.
 * Run r_values.py first. Proposed sizing, not an adopted change. */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_2026_09_24", "package.cjs"));
const R = JSON.parse(fs.readFileSync(path.join(__dirname, "derived", "r_values.json"), "utf8"));

const published = P.csvRows("main_case_2026_09_24/derived/main_case_bands.csv")
  .find((r) => r.profile === "cbo_category_lag_non_school_full" && r.variant === "adopted");
const pub = [Number(published.cost_low_bn), Number(published.cost_high_bn)];
const orig = P.MAIN_SPECS.map((s) => ({ ...s }));
const row8c = P.CONSTANTS.row8.c;
function setup(o) {
  P.MAIN_SPECS.length = 0;
  for (const s of orig) P.MAIN_SPECS.push({ ...s,
    gg: o.gg ? o.gg[s.gg] : s.gg, school: o.school ? o.school[s.school] : s.school });
  P.CONSTANTS.row8.c = row8c * (o.row8 || 1);
}
const runs = {};
function run(name, o) {
  setup(o);
  const c = P.central({});
  runs[name] = { central: c, delta_vs_adopted: [c[0] - pub[0], c[1] - pub[1]], overrides: o };
  console.log(`${name.padEnd(44)} ${c[0].toFixed(4)} – ${c[1].toFixed(4)}   Δ ${(c[0] - pub[0]).toFixed(4)} / ${(c[1] - pub[1]).toFixed(4)}`);
}
console.log(`published adopted: ${pub[0]} – ${pub[1]}`);
const A = "A reproduce (stored 0.59/0.84, 0.63/0.66)";
run(A, {});
if (!(Math.abs(runs[A].central[0] - pub[0]) < 1e-4 && Math.abs(runs[A].central[1] - pub[1]) < 1e-4)) {
  console.error("[BLOCKED] reproduction of the adopted case failed"); process.exit(1);
}
const nat = "national_memo", key = "engine_population_key";
const gg = (s) => ({ 0.59: R[`gg_low_r_${s}`], 0.84: R[`gg_high_r_${s}`] });
const school = (suffix) => ({ 0.63: R[`school_r_0.63${suffix}`], 0.66: R[`school_r_0.66${suffix}`] });
run("B gg unrounded b (0.5939/0.842)", { gg: { 0.59: R.gg_low_b_unrounded, 0.84: R.gg_high_b } });
run("C gg finite r, national s", { gg: gg(nat) });
run("D gg finite r, engine key s", { gg: gg(key) });
run("E row 8 finite", { row8: R[`row8_factor_${nat}`] });
run("F school finite r, pupil share", { school: school("") });
run("G school finite r, s 0.16", { school: school("_s0.16") });
run("H school finite r, s 0.18", { school: school("_s0.18") });
run("I gg + row 8 (general government only)", { gg: gg(nat), row8: R[`row8_factor_${nat}`] });
run("J all: gg + row 8 + school", { gg: gg(nat), row8: R[`row8_factor_${nat}`], school: school("") });
setup({});
fs.writeFileSync(path.join(__dirname, "derived", "runs.json"), JSON.stringify({ published: pub, runs }, null, 1) + "\n");
console.log("[written] derived/runs.json");
