/* The adopted main case, specification by specification, split into the engine's three terms.
 *
 * For a case (--case, default sept26_schools) this evaluates the explorer engine at each of the 64
 * main-case specifications of the case and of the case before it, and writes the direct fiscal
 * response A, the private production term P and the induced receipts F. welfare = P + A + F, and the
 * cost to other residents is -welfare. winners_losers.py puts A + F in the fiscal channel and P in the
 * wage channel.
 *
 * Each model is the explorer model plus its case's corrections payload (none for September 23), at
 * the specifications of its case's package.cjs; the model names are the case column of
 * fiscal_specs.csv:
 *   --case sept24          adopted_2026_09_23 and adopted_2026_09_24 (main_case_2026_09_24), both at
 *                          general government 0.59/0.84 and schools 0.63/0.66;
 *   --case sept26          adopted_2026_09_24 and adopted_2026_09_26 (main_case_2026_09_26: the
 *                          finite-removal responses and the consumption key);
 *   --case sept26_schools  adopted_2026_09_26 and adopted_2026_09_26_schools
 *                          (main_case_schools_full_2026_09_26: schools at full average cost, response 1).
 * The specification grid and responses come from the packages, whose MAIN_SPECS carry the responses
 * of their payload's meta.responses (gated). The engine is run here because the packages' cost()
 * returns the total only; a gate proves this lane's engine state against cost() at every specification.
 *
 * At the two band ends (the lowest- and highest-cost specifications, the first of a tie) it also writes
 * each account line's responsive effect, for the federal/state-local split in winners_losers.py.
 *
 * Gates (exit 1 on failure, nothing written): both bands reproduce the case's main_case_bands.csv to
 * 1e-4; every specification's cost equals the package's cost() to 1e-9; welfare = P + A + F in every
 * specification; P + F depends on the normalization only; the specifications' responses are the
 * payloads'.
 * Run: node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs [--case sept24] [--out-dir DIR]
 * (default output: derived/, the file names winners_losers.py reads).
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
// case -> its main-case lane, and its two models in the order written: [name, payload lane or null for
// the explorer model, variant in the lane's main_case_bands.csv, the package whose MAIN_SPECS it uses].
const CASES = {
  sept24: { lane: "main_case_2026_09_24", models: (P) => [
    ["adopted_2026_09_23", null, "adopted_2026_09_23", P],
    ["adopted_2026_09_24", "main_case_2026_09_24", "adopted", P]] },
  sept26: { lane: "main_case_2026_09_26", models: (P) => [
    ["adopted_2026_09_24", "main_case_2026_09_24", "adopted_2026_09_24", P.P24],
    ["adopted_2026_09_26", "main_case_2026_09_26", "adopted", P]] },
  sept26_schools: { lane: "main_case_schools_full_2026_09_26", models: (P) => [
    ["adopted_2026_09_26", "main_case_2026_09_26", "adopted_2026_09_26", P.P26],
    ["adopted_2026_09_26_schools", "main_case_schools_full_2026_09_26", "adopted", P]] },
};
const opt = (name, fallback) => {
  const i = process.argv.indexOf(name);
  return i > 0 ? process.argv[i + 1] : fallback;
};
const CASE = opt("--case", "sept26_schools");
if (!CASES[CASE]) {
  console.error(`unknown case ${CASE}; one of ${Object.keys(CASES).join(", ")}`);
  process.exit(2);
}
const OUT = path.resolve(opt("--out-dir", path.join(HERE, "derived")));
const P = require(path.join(FISCAL, CASES[CASE].lane, "package.cjs"));
const { Engine, MODEL, SYN } = P;
const PR = P.PROFILES[P.MAIN_PROFILE];
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
function csvRows(file) {
  const [head, ...rows] = fs.readFileSync(file, "utf8").trim().split("\n");
  const keys = head.split(",");
  return rows.map((r) => Object.fromEntries(r.split(",").map((c, i) => [keys[i], c])));
}

// The package's cost() state for the main profile, evaluated in full (A, P, F and the lines).
function evaluate(m, spec) {
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = m.receipts.reference;
  s.production.normalization = spec.normalization;
  s.count_production = true;
  s.general_government_response = spec.gg;
  s.key_override = { public_order_safety: spec.justice, medicaid_and_chip_other_medical: spec.uc };
  s.response_override = {
    education_services: spec.share * spec.school + (1 - spec.share) * PR.other,
    public_order_safety: 1, health_services: 1, income_security_services: 1,
    housing_community_services: 1, economic_affairs_services: PR.delayed, recreation_culture: PR.delayed,
    [SYN.school]: spec.share * spec.school, [SYN.college]: (1 - spec.share) * PR.other, [SYN.constants]: 1,
  };
  return Engine.evaluate(m, s);
}

const published = {};
for (const r of csvRows(path.join(FISCAL, CASES[CASE].lane, "derived", "main_case_bands.csv"))) {
  if (r.profile === P.MAIN_PROFILE) published[r.variant] = [Number(r.cost_low_bn), Number(r.cost_high_bn)];
}

const rows = [];
const lineRows = [];
console.log(`[specifications] case ${CASE} (${CASES[CASE].lane})`);
for (const [caseName, payloadLane, variant, pkg] of CASES[CASE].models(P)) {
  const payload = payloadLane && readJson(`${payloadLane}/derived/corrections.json`);
  const m = payload ? Engine.applyCorrections(MODEL, payload) : MODEL;
  const specs = pkg.MAIN_SPECS;
  if (payload && payload.meta.responses) {
    const r = payload.meta.responses;
    gate(`${caseName}: the package's responses are the payload's meta.responses`,
      JSON.stringify(pkg.RESPONSES) === JSON.stringify(r));
    gate(`${caseName}: every specification carries the payload's responses`, specs.every((s) =>
      [r.general_government.low, r.general_government.high].includes(s.gg)
      && [r.school.growth, r.school.decline].includes(s.school)));
  }
  const results = specs.map((spec) => ({ spec, r: evaluate(m, spec) }));
  const costs = results.map((x) => -x.r.welfare_bn);
  const lo = Math.min(...costs), hi = Math.max(...costs);
  const want = published[variant];
  gate(`${caseName}: band reproduces main_case_bands.csv (${variant})`,
    Math.abs(lo - want[0]) < 1e-4 && Math.abs(hi - want[1]) < 1e-4,
    `${lo.toFixed(4)}–${hi.toFixed(4)} vs ${want[0]}–${want[1]}`);
  const vsPackage = Math.max(...results.map(({ spec }, i) => Math.abs(costs[i] - P.cost(m, spec))));
  gate(`${caseName}: every specification's cost equals the package's cost()`, vsPackage < 1e-9,
    `max |gap| ${vsPackage.toExponential(2)}`);
  let maxId = 0;
  const pf = {};
  results.forEach(({ spec, r }, i) => {
    maxId = Math.max(maxId, Math.abs(r.welfare_bn - (r.private_wtp_bn + r.direct_fiscal_response_bn + r.induced_receipts_bn)));
    const key = spec.normalization;
    pf[key] = pf[key] || new Set();
    pf[key].add((r.private_wtp_bn + r.induced_receipts_bn).toFixed(9));
    rows.push({
      case: caseName, spec_id: i, ...spec, cost_bn: -r.welfare_bn, welfare_bn: r.welfare_bn,
      A_bn: r.direct_fiscal_response_bn, P_bn: r.private_wtp_bn, F_bn: r.induced_receipts_bn,
      band_end: costs[i] === lo ? "low" : costs[i] === hi ? "high" : "",
    });
  });
  gate(`${caseName}: welfare = P + A + F in all 64 specifications`, maxId < 1e-9, `max |gap| ${maxId.toExponential(2)}`);
  gate(`${caseName}: P + F depends on the normalization only`, Object.values(pf).every((s) => s.size === 1),
    Object.entries(pf).map(([k, s]) => `${k} ${[...s].join("/")}`).join("; "));
  // Line effects at the two band ends.
  for (const [end, target] of [["low", lo], ["high", hi]]) {
    const hit = results.find((x) => -x.r.welfare_bn === target);
    for (const l of hit.r.receipts) {
      lineRows.push({ case: caseName, end, side: "receipt", line: l.id, amount_bn: l.amount_bn, response: l.response, effect_bn: l.effect_bn });
    }
    for (const l of hit.r.spending) {
      lineRows.push({ case: caseName, end, side: "spending", line: l.id, amount_bn: l.amount_bn, response: l.response, effect_bn: l.effect_bn });
    }
    const sum = lineRows.filter((x) => x.case === caseName && x.end === end).reduce((s, x) => s + x.effect_bn, 0);
    gate(`${caseName} ${end}: line effects add to A`, Math.abs(sum - hit.r.direct_fiscal_response_bn) < 1e-8,
      `${sum.toFixed(6)} vs ${hit.r.direct_fiscal_response_bn.toFixed(6)}`);
  }
}

function writeCsv(file, list) {
  const keys = Object.keys(list[0]);
  const fmt = (v) => (typeof v === "number" ? (Number.isInteger(v) ? String(v) : v.toPrecision(15)) : String(v));
  fs.writeFileSync(file, [keys.join(",")].concat(list.map((r) => keys.map((k) => fmt(r[k])).join(","))).join("\n") + "\n");
}
if (failures) {
  console.log(`[BLOCKED] ${failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
writeCsv(path.join(OUT, "fiscal_specs.csv"), rows);
writeCsv(path.join(OUT, "fiscal_lines_band_ends.csv"), lineRows);
console.log(`wrote ${path.relative(process.cwd(), OUT) || "."}/fiscal_specs.csv (${rows.length} rows) and fiscal_lines_band_ends.csv (${lineRows.length} rows)`);
