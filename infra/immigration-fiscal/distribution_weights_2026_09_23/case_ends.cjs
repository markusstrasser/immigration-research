/* The amounts distribute.py splits out of a main case's direct fiscal response A at each band end.
 *
 * September 27 (main_case_long_run_2026_09_27) needs two splits the band file does not carry:
 *   - the return on public capital, an imputed resource cost, total and by level (federal, state and local);
 *   - the capped programs, rental assistance (housing_subsidies) and LIHEAP (energy_assistance): the group's amount
 *     times its response. Their slots go to eligible households without the group, so distribute.py charges them to
 *     eligible non-recipients instead of the budget.
 * TANF-type aid (family_and_general_assistance) is recorded for reference; it stays with the budget.
 * Methods are averaged at their own end specifications, as the case lane does.
 *
 * Gates (exit 1, nothing written): the band equals summary.json's main_case (1e-9) and main_case_bands.csv's
 * adopted row (1e-4); the capital return equals summary.json's capital_at_end_specifications, in total and by level
 * (1e-9); rental assistance equals lines_at_end_specifications.housing_subsidies.added_bn (1e-9); both capped lines
 * respond at 1 at every end specification.
 *
 * Run from anywhere: node case_ends.cjs [--case sept27] [--out-dir DIR] -> derived/case_ends_<case>.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.resolve(__dirname, "..");
const CASES = { sept27: "main_case_long_run_2026_09_27" };
const argv = process.argv.slice(2);
const opt = (name, dflt) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : dflt);
const CASE = opt("--case", Object.keys(CASES).slice(-1)[0]);
if (!CASES[CASE]) throw new Error(`[BLOCKED] unknown case ${CASE}`);
const LANE = CASES[CASE];
const OUT = path.resolve(opt("--out-dir", path.join(__dirname, "derived")));

const P = require(path.join(FISCAL, LANE, "package.cjs"));
const { METHODS } = P;
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
let failed = 0;
const gate = (name, ok, detail) => {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
  if (!ok) failed += 1;
};
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(...xs.map(Math.abs));

const CAPPED = { housing_subsidies: "rental assistance", energy_assistance: "LIHEAP" };
const BLOCK_GRANT = "family_and_general_assistance";
const summary = readJson(`${LANE}/derived/summary.json`);
const bandsText = fs.readFileSync(path.join(FISCAL, LANE, "derived/main_case_bands.csv"), "utf8").trim().split("\n");
const adoptedRow = bandsText.map((l) => l.split(",")).find((r) => r[0] === P.MAIN_PROFILE && r[1] === "adopted");
if (!adoptedRow) throw new Error(`[BLOCKED] ${LANE} main_case_bands.csv has no ${P.MAIN_PROFILE}/adopted row`);

console.log(`[${CASE}: ${LANE}, profile ${P.MAIN_PROFILE}]`);
const models = METHODS.map((m) => P.modelFor("central", m, P.withCentral({})));
const runs = models.map((m) => P.MAIN_SPECS.map((s) => P.evaluateFull(m, s, P.MAIN_PROFILE)));
const costs = runs.map((xs) => xs.map((r) => r.cost_bn));
const ends = costs.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
const at = (e, f) => mean(ends.map((ij, m) => f(runs[m][ij[e]])));
const row = (r, id) => {
  const x = r.evaluation.spending.find((l) => l.id === id);
  if (!x) throw new Error(`[BLOCKED] the evaluation has no line ${id}`);
  return x;
};
const level = (r, lv) => r.capital.components.filter((c) => c.level === lv).reduce((a, c) => a + c.return_bn, 0);
const END = ["low", "high"].map((name, e) => ({ name,
  cost_bn: at(e, (r) => r.cost_bn),
  capital_return_bn: at(e, (r) => r.capital.total_bn),
  capital_return_by_level_bn: { state_local: at(e, (r) => level(r, "state_local")), federal: at(e, (r) => level(r, "federal")) },
  capped_bn: Object.fromEntries(Object.keys(CAPPED).map((id) => [id, at(e, (r) => row(r, id).response * row(r, id).amount_bn)])),
  block_grant_bn: { [BLOCK_GRANT]: at(e, (r) => row(r, BLOCK_GRANT).response * row(r, BLOCK_GRANT).amount_bn) } }));

const band = END.map((x) => x.cost_bn);
gate("the band equals summary.json main_case (1e-9)", worst(band.map((x, j) => x - summary.main_case[j])) < 1e-9,
  band.map((x) => x.toFixed(4)).join("/"));
gate("the band equals main_case_bands.csv's adopted row (1e-4, the file's rounding)",
  worst(band.map((x, j) => x - Number(adoptedRow[2 + j]))) < 1e-4, `ends ${JSON.stringify(ends)}`);
const cap = summary.capital_at_end_specifications;
gate("the capital return equals capital_at_end_specifications, in total and by level (1e-9)",
  worst(END.flatMap((x, j) => [x.capital_return_bn - cap.total_bn[j], x.capital_return_by_level_bn.state_local - cap.by_level_bn.state_local[j],
    x.capital_return_by_level_bn.federal - cap.by_level_bn.federal[j]])) < 1e-9,
  END.map((x) => `${x.capital_return_bn.toFixed(4)} (federal ${x.capital_return_by_level_bn.federal.toFixed(4)})`).join(" / "));
gate("rental assistance equals lines_at_end_specifications.housing_subsidies.added_bn (1e-9)",
  worst(END.map((x, j) => x.capped_bn.housing_subsidies - summary.lines_at_end_specifications.housing_subsidies.added_bn[j])) < 1e-9,
  END.map((x) => x.capped_bn.housing_subsidies.toFixed(4)).join(" / "));
const responses = ends.flatMap((ij, m) => ij.flatMap((i) => Object.keys(CAPPED).map((id) => row(runs[m][i], id).response)));
gate("both capped lines respond at 1 at every end specification", responses.every((r) => r === 1), `${responses.length} rows`);
if (failed) {
  console.error(`${failed} gate(s) failed; nothing written`);
  process.exit(1);
}
const out = { case: CASE, lane: LANE, profile: P.MAIN_PROFILE,
  rule: "each fill-in method's end specifications of the case, averaged; capped programs = the group's amount x response",
  capped_lines: CAPPED, block_grant_line: BLOCK_GRANT,
  inputs: Object.fromEntries([`${LANE}/derived/summary.json`, `${LANE}/derived/main_case_bands.csv`, `${LANE}/package.cjs`]
    .map((rel) => [rel, sha256(rel)])),
  end_specifications: ends.map((ij, m) => ({ method: METHODS[m], low: ij[0], high: ij[1] })),
  ends: Object.fromEntries(END.map(({ name, ...x }) => [name, x])) };
fs.mkdirSync(OUT, { recursive: true });
const file = path.join(OUT, `case_ends_${CASE}.json`);
fs.writeFileSync(file, JSON.stringify(out, null, 1) + "\n");
const rel = path.relative(FISCAL, file);
console.log(`wrote ${rel.startsWith("..") ? file : rel}`);
