/* A copy of pension_accrual_2026_09_28/case_lines.cjs (9ea1beb) that writes here: it re-reads the September 27 case's
 * pension lines on today's engine and checks that they are the ones the pension lane's case.json and case_lines.csv
 * froze. Engine.js changed after the lane's last run (db5840f6, "Engine takes new receipt lines and scale edits"), so
 * that lane's own gate (pension_accrual.gate_inputs) stopped on the engine's hash until ec59a377 refreshed it; this
 * check is what lets pension_tr2026.py read the lane's frozen case. Changed from the copy: OUT, the two output names and
 * the comparison at the end; the evaluation is the original's.
 *
 * Gates (each stops with [BLOCKED]):
 *   1. the package chain, the engine and model.json are byte-identical to git HEAD, before and after the run;
 *   2. evaluateFull at specifications 48 and 11, averaged over the two fill-in methods, reproduces the case in
 *      main_case_long_run_2026_09_27/derived/summary.json ($321.82-387.37bn) to 1e-9;
 *   3. 48 and 11 are each method's cheapest and dearest specifications;
 *   4. (added) the lines equal the pension lane's derived/case_lines.csv byte for byte and its case.json per-method
 *      costs exactly, and every frozen file but engine.js still has the hash case.json recorded (since ec59a377,
 *      engine.js too).
 *
 * Writes derived/case_lines_now.csv and derived/case_now.json.
 *
 * Run from the repository root: node infra/immigration-fiscal/pension_tr2026_2026_10_06/case_lines_check.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.resolve(HERE, "..");
const ROOT = path.resolve(FISCAL, "..", "..");
const OUT = path.join(HERE, "derived");
const CASE_LANE = "main_case_long_run_2026_09_27";
const FROZEN = [
  `${CASE_LANE}/package.cjs`, `${CASE_LANE}/derived/summary.json`, `${CASE_LANE}/derived/corrections.json`,
  "main_case_schools_full_2026_09_26/package.cjs", "main_case_2026_09_26/package.cjs", "main_case_2026_09_24/package.cjs",
  "main_case_2026_09_24/derived/stack_line_deltas.json",
  "assumption_explorer_2026_09_21/engine.js", "assumption_explorer_2026_09_21/derived/model.json",
].map((f) => `infra/immigration-fiscal/${f}`);

const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex");
const tracked = (rel) => {
  try { execFileSync("git", ["-C", ROOT, "ls-files", "--error-unmatch", rel], { stdio: "ignore" }); return true; } catch (e) { return false; }
};
// A tracked file must equal git HEAD. model.json is derived and ignored (the explorer's .gitignore); gate 2's
// reproduction of the case pins it, and it must not change during the run.
function frozenCheck(when, earlier) {
  const rows = FROZEN.map((rel) => {
    const work = sha(fs.readFileSync(path.join(ROOT, rel)));
    if (!tracked(rel)) {
      const prev = earlier && earlier.find((r) => r.file === rel);
      return { file: rel, tracked: false, sha256: work, same: !prev || prev.sha256 === work };
    }
    const head = sha(execFileSync("git", ["-C", ROOT, "show", `HEAD:${rel}`], { maxBuffer: 1 << 30 }));
    return { file: rel, tracked: true, sha256: head, same: head === work };
  });
  const bad = rows.filter((r) => !r.same);
  if (bad.length) throw new Error(`[BLOCKED] ${when}: changed: ${bad.map((r) => r.file).join(", ")}`);
  return rows;
}

const before = frozenCheck("before import");
const P = require(path.join(FISCAL, CASE_LANE, "package.cjs"));
const summary = JSON.parse(fs.readFileSync(path.join(FISCAL, CASE_LANE, "derived", "summary.json"), "utf8"));

const oo = P.withCentral({});
const specs = P.specsFor(oo);
const models = P.METHODS.map((m) => P.modelFor("central", m, oo));
const ENDS = { low: 48, high: 11 };
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;

// Gate 3: 48 and 11 are each method's ends.
const costs = models.map((m) => specs.map((s) => P.evaluateFull(m, s).cost_bn));
costs.forEach((xs, i) => {
  const lo = xs.indexOf(Math.min(...xs)), hi = xs.indexOf(Math.max(...xs));
  if (lo !== ENDS.low || hi !== ENDS.high) throw new Error(`[BLOCKED] ${P.METHODS[i]}: ends ${lo}/${hi}, not 48/11`);
});
// Gate 2: the case.
const caseBn = [mean(costs.map((xs) => xs[ENDS.low])), mean(costs.map((xs) => xs[ENDS.high]))];
const gap = caseBn.map((v, i) => Math.abs(v - summary.main_case[i]));
if (Math.max(...gap) > 1e-9) throw new Error(`[BLOCKED] the case ${caseBn} is not summary.json's ${summary.main_case}`);

const RECEIPTS = ["employee_oasdi", "employer_oasdi", "self_employment_oasdi_hi", "employee_hi", "employer_hi",
  "medicare_supplementary_premiums", "federal_income_tax"];
// The net switch drops the group's share of the Census FEDTAX_BC key that its 2024 benefits carry (benefit_tax.py),
// which holds only while the case keys federal income tax by that key ("federal_liability").
const KEYED = { federal_income_tax: "federal_liability" };
const SPENDING = ["social_security", "railroad_retirement", "medicare"];
const header = ["method", "end", "spec", "allocation", "side", "line", "national_bn", "amount_bn", "response", "effect_bn"];
const rows = [header.join(",")];
const perMethod = [];
models.forEach((m, i) => {
  for (const [end, idx] of Object.entries(ENDS)) {
    const s = specs[idx];
    const r = P.evaluateFull(m, s);
    const ev = r.evaluation;
    for (const id of RECEIPTS) {
      const x = ev.receipts.find((l) => l.id === id);
      if (!x) throw new Error("[BLOCKED] no receipt line " + id);
      if (KEYED[id] && x.key !== KEYED[id]) throw new Error(`[BLOCKED] ${id} is keyed by ${x.key}, not ${KEYED[id]}`);
      rows.push([P.METHODS[i], end, idx, s.allocation, "receipt", id, x.national_bn, x.amount_bn, x.response, x.effect_bn].join(","));
    }
    for (const id of SPENDING) {
      const x = ev.spending.find((l) => l.id === id);
      if (!x) throw new Error("[BLOCKED] no spending line " + id);
      if (x.response !== 1) throw new Error(`[BLOCKED] ${id} responds at ${x.response}, not 1`);
      rows.push([P.METHODS[i], end, idx, s.allocation, "spending", id, x.national_bn, x.amount_bn, x.response, x.effect_bn].join(","));
    }
    perMethod.push({ method: P.METHODS[i], end, spec: idx, allocation: s.allocation, cost_bn: r.cost_bn,
      engine_cost_bn: -ev.welfare_bn, capital_bn: r.capital.total_bn, target_population: m.meta.target_population,
      resident_population: m.meta.resident_population });
  }
});

const after = frozenCheck("after the run", before);
// Gate 4: the pension lane's frozen lines and costs, on today's engine.
const LANE_DIR = path.join(FISCAL, "pension_accrual_2026_09_28", "derived");
const text = rows.join("\n") + "\n";
const laneCase = JSON.parse(fs.readFileSync(path.join(LANE_DIR, "case.json"), "utf8"));
if (fs.readFileSync(path.join(LANE_DIR, "case_lines.csv"), "utf8") !== text) {
  throw new Error("[BLOCKED] today's case lines differ from the pension lane's derived/case_lines.csv");
}
const sameCosts = laneCase.per_method.length === perMethod.length && laneCase.per_method.every((r, i) => Object.keys(r).every((k) => r[k] === perMethod[i][k]));
if (!sameCosts || laneCase.case_bn.low !== caseBn[0] || laneCase.case_bn.high !== caseBn[1]) {
  throw new Error("[BLOCKED] today's per-method costs differ from the pension lane's case.json");
}
const hashMoved = after.filter((r) => { const f = laneCase.frozen_files.find((x) => x.file === r.file); return !f || f.sha256 !== r.sha256; }).map((r) => r.file);
// engine.js alone moved until ec59a377 (2026-10-07) refreshed case.json's engine hash; nothing moves since.
if (!["", "infra/immigration-fiscal/assumption_explorer_2026_09_21/engine.js"].includes(hashMoved.join())) {
  throw new Error(`[BLOCKED] frozen files changed since the pension lane's case.json: ${hashMoved.join(", ")}`);
}
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "case_lines_now.csv"), text);
fs.writeFileSync(path.join(OUT, "case_now.json"), JSON.stringify({
  case_lane: CASE_LANE, ends: ENDS, case_bn: { low: caseBn[0], high: caseBn[1] },
  summary_main_case_bn: summary.main_case, max_abs_gap_bn: Math.max(...gap), methods: P.METHODS, per_method: perMethod,
  frozen_files: after.map(({ file, tracked, sha256 }) => ({ file, tracked, sha256 })),
  gates: { unchanged_before: before.every((r) => r.same), unchanged_after: after.every((r) => r.same),
    case_reproduced_1e9: true, ends_48_11: true, lane_case_lines_identical: true, lane_per_method_costs_identical: true },
  hash_moved_since_lane_case_json: hashMoved,
}, null, 1) + "\n");
console.log(`[gate] package chain, engine and model.json identical to HEAD before and after (${after.length} files)`);
console.log(`[gate] 48 / 11 are both methods' ends; case ${caseBn.map((v) => v.toFixed(4)).join(" / ")} = summary.json (max gap ${Math.max(...gap).toExponential(1)})`);
console.log(`[gate] the pension lane's case_lines.csv and per-method costs reproduce on today's engine; hash moved: ${hashMoved.join(", ")}`);
console.log(`[written] ${path.relative(ROOT, OUT)}/case_lines_now.csv, case_now.json`);
