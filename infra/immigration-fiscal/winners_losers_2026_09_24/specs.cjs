/* The adopted main case, specification by specification, split into the engine's three terms.
 *
 * For a case (--case, default sept27) this evaluates the explorer engine at each of the 64
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
 *                          (main_case_schools_full_2026_09_26: schools at full average cost, response 1);
 *   --case sept27          adopted_2026_09_26_schools and adopted_2026_09_27 (main_case_long_run_2026_09_27:
 *                          long-run road and park responses, rental assistance at 1, every government
 *                          enterprise and the return on public capital);
 *   --case sept29          adopted_2026_09_27 (its lane's package, at its band variant sept27_case in SEPT29_LANE's
 *                          main_case_bands.csv) and adopted_2026_09_29 (SEPT29_LANE: candidate v4, adopted
 *                          2026-09-29), written to derived/sept29/ beside the default files;
 *   --case oct05           adopted_2026_09_29 (its lane's package, at its band variant sept29_case in OCT05_LANE's
 *                          main_case_bands.csv) and adopted_2026_10_05 (OCT05_LANE: main case v5, adopted 2026-10-05,
 *                          the lineage counted whole), written to derived/oct05/;
 *   --case oct07           adopted_2026_10_05 (its lane's package, at its band variant oct05_case in OCT07_LANE's
 *                          main_case_bands.csv) and adopted_2026_10_07 (OCT07_LANE: main case v6, v5 plus the items in
 *                          its payload's meta.items), written to derived/oct07/.
 * A payload's line responses are the meta.responses entries with a low and a high other than general government
 * (a receipt under its override id): four on September 27, thirteen on September 29.
 * The specification grid and responses come from the packages, whose MAIN_SPECS carry the responses
 * of their payload's meta.responses (gated). Each model's engine state is its package's stateFor(), the
 * one definition (main_case_2026_09_24/package.cjs; the September 27 package adds the long-run lines,
 * rental assistance and the enterprise receipt through the specification's line_responses). The engine
 * is run here because the packages' cost() returns the total only; a gate proves every specification's
 * cost against cost().
 *
 * The return on public capital (from September 27) is a post-engine term: the package's evaluateFull()
 * keys it on the same evaluation. It is an imputed resource cost of the budgets that hold the capital, so
 * it is part of the direct fiscal response: A = the engine's A - the return, welfare = the engine's welfare
 * - the return, and P and F do not move. Its columns (engine_A_bn, capital_*_bn) and the specification's
 * reading, rate, enterprise option and line responses (response_<line>) are written for that case only.
 *
 * At the two band ends (the lowest- and highest-cost specifications, the first of a tie) it also writes
 * each account line's responsive effect, for the federal/state-local split in winners_losers.py; from
 * September 27 each capital component is a line capital_<id> on side capital_return, its id from the
 * payload's meta.capital_return (amount = the group's keyed stock times the rate, effect = -amount x
 * response). There is no total line, so the lines add to A; the totals are fiscal_specs.csv's columns.
 *
 * Gates (exit 1 on failure, nothing written): both bands reproduce the case's main_case_bands.csv to
 * 1e-4, and the case's uncorrected model its uncorrected_at_adopted_responses row where the file has one;
 * every specification's cost equals the package's cost() to 1e-9; welfare = P + A + F in every
 * specification; P + F depends on the normalization only; the specifications' responses are the
 * payloads'; the line effects add to fiscal_specs.csv's A_bn at both band ends (1e-6), and a case with a
 * capital return writes exactly its payload's components. A case with a capital return also matches its
 * lane's per_spec.csv (the mean of the two fill-in methods) in cost, engine cost and every capital column
 * at every specification.
 * Run: node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs [--case sept26_schools] [--out-dir DIR]
 * (default output: derived/, the file names winners_losers.py reads; a case with its own directory, derived/<out>).
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const SEPT29_LANE = "main_case_2026_09_29";
const OCT05_LANE = "main_case_2026_10_05";
const OCT07_LANE = "main_case_2026_10_07";
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
  sept27: { lane: "main_case_long_run_2026_09_27", models: (P) => [
    ["adopted_2026_09_26_schools", "main_case_schools_full_2026_09_26", "schools_case", P.PSCHOOLS],
    ["adopted_2026_09_27", "main_case_long_run_2026_09_27", "adopted", P]] },
  sept29: { lane: SEPT29_LANE, out: "sept29", models: (P) => [
    ["adopted_2026_09_27", "main_case_long_run_2026_09_27", "sept27_case", P.SEPT27],
    ["adopted_2026_09_29", SEPT29_LANE, "adopted", P]] },
  oct05: { lane: OCT05_LANE, out: "oct05", models: (P) => [
    ["adopted_2026_09_29", SEPT29_LANE, "sept29_case", P.SEPT29],
    ["adopted_2026_10_05", OCT05_LANE, "adopted", P]] },
  oct07: { lane: OCT07_LANE, out: "oct07", models: (P) => [
    ["adopted_2026_10_05", OCT05_LANE, "oct05_case", P.OCT05],
    ["adopted_2026_10_07", OCT07_LANE, "adopted", P]] },
};
const opt = (name, fallback) => {
  const i = process.argv.indexOf(name);
  return i > 0 ? process.argv[i + 1] : fallback;
};
const CASE = opt("--case", "sept27");
if (!CASES[CASE]) {
  console.error(`unknown case ${CASE}; one of ${Object.keys(CASES).join(", ")}`);
  process.exit(2);
}
const OUT = path.resolve(opt("--out-dir", path.join(HERE, "derived", CASES[CASE].out || "")));
const P = require(path.join(FISCAL, CASES[CASE].lane, "package.cjs"));
const { Engine, MODEL } = P;
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

// A model's evaluation at a specification: its package's engine state, and the return on public capital
// where the package has one (evaluateFull keys it on the same evaluation).
function evaluate(pkg, m, spec) {
  if (pkg.evaluateFull) {
    const full = pkg.evaluateFull(m, spec);
    return { r: full.evaluation, capital: full.capital };
  }
  return { r: Engine.evaluate(m, pkg.stateFor(m, spec)), capital: null };
}
const CAPITAL_PARTS = ["core", "block", "enterprise"];
const LEVEL_COLUMN = { federal: "capital_federal_bn", state_local: "capital_state_local_bn" };
// The capital columns of one evaluation, named as the case lane's per_spec.csv names them.
function capitalColumns(capital) {
  const out = { capital_total_bn: capital.total_bn, capital_state_local_bn: 0, capital_federal_bn: 0 };
  for (const p of CAPITAL_PARTS) out[`capital_${p}_bn`] = 0;
  for (const c of capital.components) {
    out[LEVEL_COLUMN[c.level]] += c.return_bn;
    out[`capital_${c.group}_bn`] += c.return_bn;
  }
  return out;
}
// A specification's fields as CSV cells: line_responses become response_<line> (a receipt as
// response_receipt_<id>), as in the case lane's per_spec.csv.
function specFields(spec) {
  const { line_responses: lr, ...rest } = spec;
  if (!lr) return rest;
  return Object.assign(rest, Object.fromEntries(Object.entries(lr).map(([id, v]) => [`response_${id.replace(":", "_")}`, v])));
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
    const cap = payload.meta.capital_return;
    if (cap) {
      // Line and receipt responses at the specification's reading, and the rate of the return. The line responses
      // are exactly the meta.responses entries with a low and a high other than general government.
      const ids = JSON.stringify(Object.entries(r)
        .filter(([k, v]) => v && typeof v === "object" && "low" in v && "high" in v && k !== "general_government")
        .map(([k, v]) => v.override || k).sort());
      const want = (s, id) => (id.startsWith("receipt:") ? r[id.slice(8)].low : r[id][s.reading]);
      gate(`${caseName}: every specification's line responses and rate are the payload's meta`, specs.every((s) =>
        JSON.stringify(Object.keys(s.line_responses).sort()) === ids && Object.entries(s.line_responses).every(([id, v]) => v === want(s, id))
        && s.rate === cap.rates[s.reading] && s.enterprises === cap.enterprises), `${JSON.parse(ids).length} line responses`);
    }
  }
  const results = specs.map((spec) => Object.assign({ spec }, evaluate(pkg, m, spec)));
  const capOf = (x) => (x.capital ? x.capital.total_bn : 0);
  const costs = results.map((x) => -x.r.welfare_bn + capOf(x));
  const lo = Math.min(...costs), hi = Math.max(...costs);
  const want = published[variant];
  gate(`${caseName}: band reproduces main_case_bands.csv (${variant})`,
    Math.abs(lo - want[0]) < 1e-4 && Math.abs(hi - want[1]) < 1e-4,
    `${lo.toFixed(4)}–${hi.toFixed(4)} vs ${want[0]}–${want[1]}`);
  const vsPackage = Math.max(...results.map(({ spec }, i) => Math.abs(costs[i] - pkg.cost(m, spec))));
  gate(`${caseName}: every specification's cost equals the package's cost()`, vsPackage < 1e-9,
    `max |gap| ${vsPackage.toExponential(2)}`);
  if (variant === "adopted" && published.uncorrected_at_adopted_responses) {
    const unc = specs.map((spec) => pkg.cost(MODEL, spec));
    const w = published.uncorrected_at_adopted_responses;
    gate(`${caseName}: the uncorrected model reproduces uncorrected_at_adopted_responses`,
      Math.abs(Math.min(...unc) - w[0]) < 1e-4 && Math.abs(Math.max(...unc) - w[1]) < 1e-4,
      `${Math.min(...unc).toFixed(4)}–${Math.max(...unc).toFixed(4)} vs ${w[0]}–${w[1]}`);
  }
  if (results.some((x) => x.capital)) {
    // The case lane's per_spec.csv holds each fill-in method's run; the payload model is their mean.
    const per = csvRows(path.join(FISCAL, payloadLane, "derived", "per_spec.csv"));
    const cols = ["cost_bn", "engine_cost_bn", "capital_total_bn", "capital_state_local_bn", "capital_federal_bn",
      ...CAPITAL_PARTS.map((p) => `capital_${p}_bn`)];
    let worst = 0, n = 0;
    results.forEach((x, i) => {
      const got = Object.assign({ cost_bn: costs[i], engine_cost_bn: -x.r.welfare_bn }, capitalColumns(x.capital));
      const lane = per.filter((p) => Number(p.spec) === i);
      n += lane.length;
      for (const c of cols) worst = Math.max(worst, Math.abs(got[c] - lane.reduce((a, p) => a + Number(p[c]), 0) / lane.length));
    });
    gate(`${caseName}: cost, engine cost and capital columns equal per_spec.csv's method mean at every specification`,
      n === 2 * specs.length && worst < 1e-6, `${n} method rows; max |gap| ${worst.toExponential(2)}`);
  }
  let maxId = 0;
  const pf = {};
  results.forEach(({ spec, r, capital }, i) => {
    const cap = capital ? capital.total_bn : 0;
    const welfare = r.welfare_bn - cap, A = r.direct_fiscal_response_bn - cap;
    maxId = Math.max(maxId, Math.abs(welfare - (r.private_wtp_bn + A + r.induced_receipts_bn)));
    const key = spec.normalization;
    pf[key] = pf[key] || new Set();
    pf[key].add((r.private_wtp_bn + r.induced_receipts_bn).toFixed(9));
    rows.push(Object.assign({
      case: caseName, spec_id: i, ...specFields(spec), cost_bn: -welfare, welfare_bn: welfare,
      A_bn: A, P_bn: r.private_wtp_bn, F_bn: r.induced_receipts_bn,
      band_end: costs[i] === lo ? "low" : costs[i] === hi ? "high" : "",
    }, capital ? Object.assign({ engine_A_bn: r.direct_fiscal_response_bn }, capitalColumns(capital)) : {}));
  });
  gate(`${caseName}: welfare = P + A + F in all 64 specifications`, maxId < 1e-9, `max |gap| ${maxId.toExponential(2)}`);
  gate(`${caseName}: P + F depends on the normalization only`, Object.values(pf).every((s) => s.size === 1),
    Object.entries(pf).map(([k, s]) => `${k} ${[...s].join("/")}`).join("; "));
  // Line effects at the two band ends; each capital component as a line capital_<id> on side capital_return,
  // its id from the payload's meta.capital_return (no total line: the lines add to A, and the totals are
  // fiscal_specs.csv's capital_*_bn columns).
  for (const [end, target] of [["low", lo], ["high", hi]]) {
    const hit = results[costs.indexOf(target)];
    for (const l of hit.r.receipts) {
      lineRows.push({ case: caseName, end, side: "receipt", line: l.id, amount_bn: l.amount_bn, response: l.response, effect_bn: l.effect_bn });
    }
    for (const l of hit.r.spending) {
      lineRows.push({ case: caseName, end, side: "spending", line: l.id, amount_bn: l.amount_bn, response: l.response, effect_bn: l.effect_bn });
    }
    if (hit.capital) {
      const ids = payload.meta.capital_return.components.map((c) => c.id);
      gate(`${caseName} ${end}: the capital components are the payload's meta.capital_return components`,
        JSON.stringify(hit.capital.components.map((c) => c.id)) === JSON.stringify(ids), `${ids.length} components`);
      for (const c of hit.capital.components) {
        const amount = c.stock_charged_bn * hit.spec.rate * c.key;
        lineRows.push({ case: caseName, end, side: "capital_return", line: `capital_${c.id}`, amount_bn: amount, response: c.response, effect_bn: -c.return_bn });
      }
    }
    // The lines, capital included, add to fiscal_specs.csv's A_bn at every specification of the band end.
    const sum = lineRows.filter((x) => x.case === caseName && x.end === end).reduce((s, x) => s + x.effect_bn, 0);
    const ends = rows.filter((x) => x.case === caseName && x.band_end === end);
    const gap = Math.max(...ends.map((x) => Math.abs(sum - x.A_bn)));
    gate(`${caseName} ${end}: line effects add to fiscal_specs A_bn`, ends.length > 0 && gap < 1e-6,
      `${sum.toFixed(6)} vs ${ends.map((x) => x.A_bn.toFixed(6)).join(", ")}; max |gap| ${gap.toExponential(2)}`);
  }
}

// Columns: every row's keys in order of first appearance; a row without one (the previous case's rows
// lack the September 27 columns) leaves the cell empty.
function writeCsv(file, list) {
  const keys = [...new Set(list.flatMap((r) => Object.keys(r)))];
  const fmt = (v) => (v === undefined || v === null ? "" : typeof v === "number" ? (Number.isInteger(v) ? String(v) : v.toPrecision(15)) : String(v));
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
