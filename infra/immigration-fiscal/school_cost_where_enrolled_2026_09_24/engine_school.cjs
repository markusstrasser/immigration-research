/* School step of the adopted main case, from the explorer's engine, and the same step with the
 * group's school allocation re-priced.
 *
 * The step is the staircase's "schools" step in figures_2026_09_22/build_data.cjs: the change in
 * cost when education responds at school_share x 0.63-0.66 on the education line's preferred key
 * (education_mix). Positive control: that step and the adopted main band reproduce figures.json and
 * main_case_bands.csv. figures.json is read as it stood when this lane ran (FIGURES_PIN, ea755452:
 * the September 23 band this lane prices); the figures page has since moved to the corrected
 * September 24 case and then to main case v6. The engine is linear in each line's target allocation,
 * so a re-priced school allocation enters as one extra spending line carrying (new school target -
 * education_mix target) at the school response only; the colleges step keeps the published key.
 *
 * Variants come from derived/school_key_variants.json (written by weighting.py); without it the
 * script runs the positive control alone. Run from anywhere: node engine_school.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const scaling = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "scaling_check.json"), "utf8"));
const FIGURES_PIN = "ea755452";
const figures = JSON.parse(require("child_process").execFileSync("git", ["-C", HERE, "show",
  `${FIGURES_PIN}:infra/immigration-fiscal/figures_2026_09_22/src/generated/figures.json`], { encoding: "utf8", maxBuffer: 1 << 27 }));

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
const near = (a, b, tol = 1e-6) => Math.abs(a - b) < tol;
const span = (xs) => [Math.min(...xs), Math.max(...xs)];
function product(dims) {
  return Object.entries(dims).reduce(
    (acc, [name, levels]) => acc.flatMap((spec) => levels.map((v) => ({ ...spec, [name]: v }))), [{}]);
}

const SHARES = Engine.schoolShareBounds(model);
const GG = [scaling.composite_low, scaling.composite_high];
const CBO_SCHOOLS = [0.63, 0.66];
const EDU = model.spending.lines.find((l) => l.id === "education_services");
const MAIN_DIMS = {
  allocation: ["personal", "shared"], normalization: ["cash", "gdp"], share: SHARES,
  school: CBO_SCHOOLS, gg: GG, uc: ["uninsured_use_low", "uninsured_use_high"], justice: ["use"],
};
const mainSpecs = product(MAIN_DIMS);

// build_data.cjs cost(), plus an optional re-pricing line that responds with the school part only.
const REPRICE = "school_reprice";
const REKEY = "college_rekey";
// delta: change in the education target seen by the school step; college: the same for the colleges step.
function withReprice(delta, college) {
  const m = JSON.parse(JSON.stringify(model));
  const cell = (d) => ({ target_bn: d, other_bn: -d, share: 0 });
  const line = (id, d) => ({ id, family: "consumption", national_bn: 0, response_class: id,
    preferred_key: "k", alternative_key: "k", keys: { k: { personal: cell(d.personal), shared: cell(d.shared) } } });
  m.spending.lines.push(line(REPRICE, delta));
  m.spending.lines.push(line(REKEY, college || { personal: 0, shared: 0 }));
  return m;
}
function cost(m, spec, r) {
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = m.receipts.reference;
  if (spec.normalization) s.production.normalization = spec.normalization;
  s.count_production = r.production;
  s.general_government_response = r.gg === "band" ? spec.gg : r.gg;
  s.key_override = {};
  if (spec.justice) s.key_override.public_order_safety = spec.justice;
  if (r.uc !== false && spec.uc) s.key_override.medicaid_and_chip_other_medical = spec.uc;
  const schools = r.schools === "cbo" ? spec.school : r.schools;
  s.response_override = {
    education_services: spec.share * schools + (1 - spec.share) * r.colleges,
    public_order_safety: r.police, health_services: r.health, income_security_services: r.other,
    housing_community_services: r.other, economic_affairs_services: r.delayed, recreation_culture: r.delayed,
    [REPRICE]: spec.share * schools,
    [REKEY]: (1 - spec.share) * r.colleges,
  };
  return -Engine.evaluate(m, s).welfare_bn;
}
const BEFORE = { schools: 0, colleges: 0, police: 0, health: 0, other: 0, delayed: 0, gg: 0, production: true, uc: true };
const AFTER = { ...BEFORE, schools: "cbo" };
const MAIN = { schools: "cbo", colleges: 1, police: 1, health: 1, other: 1, delayed: 0, gg: "band", production: true };

function evaluateVariant(m) {
  const steps = mainSpecs.map((spec) => cost(m, spec, AFTER) - cost(m, spec, BEFORE));
  const totals = mainSpecs.map((spec) => cost(m, spec, MAIN));
  return { steps, totals, step: span(steps), main: span(totals) };
}

console.log("\n[positive control]");
const base = evaluateVariant(withReprice({ personal: 0, shared: 0 }));
const figStep = figures.staircase.find((s) => s.id === "schools").step;
gate("school step = figures.json staircase", near(base.step[0], figStep[0], 1e-4) && near(base.step[1], figStep[1], 1e-4),
  `${base.step[0].toFixed(4)} to ${base.step[1].toFixed(4)} bn`);
gate("main case = figures.json account.main", near(base.main[0], figures.account.main[0], 1e-4) && near(base.main[1], figures.account.main[1], 1e-4),
  `${base.main[0].toFixed(4)} to ${base.main[1].toFixed(4)} bn`);
// Analytic form: step = school_share x school response x education_mix target of the allocation.
const analytic = mainSpecs.map((spec) => spec.share * spec.school * EDU.keys[EDU.preferred_key][spec.allocation].target_bn);
gate("step = share x response x education_mix target, every spec", analytic.every((a, i) => near(a, base.steps[i], 1e-9)),
  `${mainSpecs.length} specs`);
const lowSpec = mainSpecs[base.steps.indexOf(base.step[0])], highSpec = mainSpecs[base.steps.indexOf(base.step[1])];
console.log(`    low end: ${lowSpec.allocation}, share ${lowSpec.share.toFixed(6)}, response ${lowSpec.school}`);
console.log(`    high end: ${highSpec.allocation}, share ${highSpec.share.toFixed(6)}, response ${highSpec.school}`);
// Linearity: a +10bn re-pricing line moves every spec's step by share x response x 10 and the main total by the same.
const probe = evaluateVariant(withReprice({ personal: 10, shared: 10 }));
gate("re-pricing line enters the school step only, linearly", mainSpecs.every((spec, i) =>
  near(probe.steps[i] - base.steps[i], spec.share * spec.school * 10, 1e-9) &&
  near(probe.totals[i] - base.totals[i], spec.share * spec.school * 10, 1e-9)));

const out = {
  household_fraction: model.spending.lines.find((l) => l.id === "education_services").keys.education_mix.personal.target_bn /
    (EDU.national_bn * EDU.keys.education_mix.personal.share),
  education_national_bn: EDU.national_bn,
  school_share_bounds: SHARES,
  keys: EDU.keys,
  base: { step: base.step, main: base.main },
};

const variantsPath = path.join(HERE, "derived", "school_key_variants.json");
const rows = [];
if (fs.existsSync(variantsPath)) {
  const variants = JSON.parse(fs.readFileSync(variantsPath, "utf8"));
  console.log(`\n[variants] ${Object.keys(variants).length} from ${path.relative(HERE, variantsPath)}`);
  for (const [name, v] of Object.entries(variants)) {
    const delta = { personal: v.school_target_bn.personal - EDU.keys.education_mix.personal.target_bn,
      shared: v.school_target_bn.shared - EDU.keys.education_mix.shared.target_bn };
    const college = v.college_target_bn ? { personal: v.college_target_bn.personal - EDU.keys.education_mix.personal.target_bn,
      shared: v.college_target_bn.shared - EDU.keys.education_mix.shared.target_bn } : null;
    const r = evaluateVariant(withReprice(delta, college));
    // Cross-check the engine against the analytic step with the new school target.
    const ok = mainSpecs.every((spec, i) => near(r.steps[i], spec.share * spec.school * v.school_target_bn[spec.allocation], 1e-9));
    if (!ok) { failures += 1; console.log(`  FAIL analytic step for ${name}`); }
    rows.push({ variant: name, school_low_bn: r.step[0], school_high_bn: r.step[1],
      school_change_low_bn: r.step[0] - base.step[0], school_change_high_bn: r.step[1] - base.step[1],
      main_low_bn: r.main[0], main_high_bn: r.main[1],
      main_change_low_bn: r.main[0] - base.main[0], main_change_high_bn: r.main[1] - base.main[1] });
  }
  const header = Object.keys(rows[0]);
  const csv = [header.join(",")].concat(rows.map((row) => header.map((h) =>
    typeof row[h] === "number" ? row[h].toFixed(4) : row[h]).join(","))).join("\n") + "\n";
  fs.writeFileSync(path.join(HERE, "derived", "engine_school_lines.csv"), csv);
  for (const row of rows) {
    console.log(`    ${row.variant.padEnd(44)} school ${row.school_low_bn.toFixed(2)}–${row.school_high_bn.toFixed(2)}` +
      `  main ${row.main_low_bn.toFixed(2)}–${row.main_high_bn.toFixed(2)}`);
  }
}
fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
fs.writeFileSync(path.join(HERE, "derived", "engine_base.json"), JSON.stringify(out, null, 1) + "\n");
if (failures) { console.error(`FAIL: ${failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
