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
 * September 29 (SEPT29_LANE, candidate v4 adopted) also replaces the engine's production grid (row-4 weights), which
 * moves the private term P and the induced receipts F, never A. For a case whose corrections.json carries a production
 * grid the file gains a `production` block: at each end, the engine's P and F on the case's grid, P and F on
 * model.json's grid (the earlier cases') at the same production cell, the cell's normalization, and the engine's A (its
 * direct response less the capital return). distribute.py moves A by the case's change less the production change and
 * gates the result against that A. Two more September 29 splits: public housing's enterprise deficit (the receipt line
 * housing_enterprise_surplus, at the rental line's key) is capped like rental assistance where the model has it, and
 * the pension accrual (the case less its cash set, a `pension_accrual` block) is recorded at each end, as the debt lane
 * books both (displaced beneficiaries; an accrual never financed today).
 *
 * Gates (exit 1, nothing written): the band equals summary.json's main_case (1e-9) and main_case_bands.csv's
 * adopted row (1e-4); the capital return equals summary.json's capital_at_end_specifications, in total and by level
 * (1e-9); rental assistance equals lines_at_end_specifications.housing_subsidies.added_bn (1e-9); both capped lines
 * respond at 1 at every end specification. With a production grid: every method's end specification reads the same
 * production cell at each end, P and F there are the payload's grid values and model.json's (exact), and
 * cost = -(P + F) - A at each end (1e-9).
 *
 * Run from anywhere: node case_ends.cjs [--case sept27|sept29] [--out-dir DIR] -> derived/case_ends_<case>.json
 * (the default case is sept27, whose file the evidence map's readers take).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.resolve(__dirname, "..");
const SEPT29_LANE = "main_case_2026_09_29";
const CASES = { sept27: "main_case_long_run_2026_09_27", sept29: SEPT29_LANE };
const DEFAULT_CASE = "sept27";
const argv = process.argv.slice(2);
const opt = (name, dflt) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : dflt);
const CASE = opt("--case", DEFAULT_CASE);
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
// September 29 splits public housing's enterprise deficit out of the enterprise surplus: a receipt line at the rental
// line's key. Public housing is rationed like rental assistance, so where the model has the line it is capped too
// (its cost is -effect, the group's share of the deficit at its response).
const CAPPED_RECEIPTS = { housing_enterprise_surplus: "public housing" };
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
const row = (r, id, side = "spending") => {
  const x = r.evaluation[side].find((l) => l.id === id);
  if (!x) throw new Error(`[BLOCKED] the evaluation has no ${side} line ${id}`);
  return x;
};
const cappedReceipts = Object.keys(CAPPED_RECEIPTS).filter((id) => runs[0][0].evaluation.receipts.some((l) => l.id === id));
const cappedLines = { ...CAPPED, ...Object.fromEntries(cappedReceipts.map((id) => [id, CAPPED_RECEIPTS[id]])) };
// A capped line's cost: a spending line's amount at its response; a receipt line's -effect.
const cappedCost = (r, id) => (id in CAPPED ? row(r, id).response * row(r, id).amount_bn : -row(r, id, "receipts").effect_bn);
const level = (r, lv) => r.capital.components.filter((c) => c.level === lv).reduce((a, c) => a + c.return_bn, 0);
const END = ["low", "high"].map((name, e) => ({ name,
  cost_bn: at(e, (r) => r.cost_bn),
  capital_return_bn: at(e, (r) => r.capital.total_bn),
  capital_return_by_level_bn: { state_local: at(e, (r) => level(r, "state_local")), federal: at(e, (r) => level(r, "federal")) },
  capped_bn: Object.fromEntries(Object.keys(cappedLines).map((id) => [id, at(e, (r) => cappedCost(r, id))])),
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
const responses = ends.flatMap((ij, m) => ij.flatMap((i) => Object.keys(cappedLines)
  .map((id) => row(runs[m][i], id, id in CAPPED ? "spending" : "receipts").response)));
gate(`every capped line (${Object.keys(cappedLines).join(", ")}) responds at 1 at every end specification`,
  responses.every((r) => r === 1), `${responses.length} rows`);
for (const id of cappedReceipts) {
  const rec = summary.receipts_at_end_specifications[id];
  gate(`${id}'s capped cost is -receipts_at_end_specifications.${id}.effect_bn (1e-9)`,
    worst(END.map((x, j) => x.capped_bn[id] + rec.effect_bn[j])) < 1e-9, END.map((x) => x.capped_bn[id].toFixed(4)).join(" / "));
}

// A payload that replaces the production grid: at each end, P and F on the case's grid and on model.json's at the
// production cell of the end specification (every method's end must read one cell), and the engine's A.
const PAYLOAD_REL = `${LANE}/derived/corrections.json`;
const payload = readJson(PAYLOAD_REL);
let production = null;
if (payload.production) {
  const { Engine, MODEL } = P;
  production = { rule: "the case's production grid (corrections.json production) moves P and F only: at each end, P and F "
    + "on the case's grid and on model.json's at the end specification's production cell, and A = the engine's direct "
    + "response less the capital return; cost = -(P + F) - A", grid: payload.meta.production || null, ends: {} };
  ["low", "high"].forEach((name, e) => {
    const cells = ends.map((ij, m) => P.stateFor(models[m], P.MAIN_SPECS[ij[e]], P.MAIN_PROFILE).production);
    gate(`${name} end: every method's end specification reads one production cell`,
      cells.every((c) => JSON.stringify(c) === JSON.stringify(cells[0])), JSON.stringify(cells[0]));
    const index = Engine.productionIndex(MODEL, cells[0]);
    const caseP = at(e, (r) => r.evaluation.private_wtp_bn), caseF = at(e, (r) => r.evaluation.induced_receipts_bn);
    gate(`${name} end: P and F are the payload grid's at that cell (exact)`,
      caseP === payload.production.private_wtp_bn[index] && caseF === payload.production.induced_receipts_bn[index],
      `cell ${index}: P ${caseP}, F ${caseF}`);
    const A = at(e, (r) => r.evaluation.direct_fiscal_response_bn - r.capital.total_bn);
    gate(`${name} end: cost = -(P + F) - A (1e-9)`, Math.abs(END[e].cost_bn + caseP + caseF + A) < 1e-9);
    production.ends[name] = { normalization: cells[0].normalization, cell_index: index,
      case: { P_bn: caseP, F_bn: caseF }, model_json: { P_bn: MODEL.production.private_wtp_bn[index], F_bn: MODEL.production.induced_receipts_bn[index] },
      A_bn: A };
  });
}
// A payload with the pension switch (September 29): the accrual is the case less its cash set at the end specifications
// (social security and Medicare at the accrual, federal income tax net of the tax on benefits). It sits inside A; it is
// not financed today, so distribute.py reports it apart from the cash part of the fiscal channel.
let pensionAccrual = null;
if (payload.meta.pension_accrual) {
  const item = summary.change_at_fixed_specifications.item_pension, cash = summary.cash_set;
  gate("the pension accrual is change_at_fixed_specifications.item_pension, the case less its cash set (1e-9)",
    JSON.stringify(cash.end_specifications) === JSON.stringify(ends) && worst(item.map((x, j) => x + cash.change_from_main_case_bn[j])) < 1e-9,
    item.map((x) => x.toFixed(4)).join(" / "));
  pensionAccrual = { rule: "the case less its cash set at the end specifications (summary.json cash_set, the pension switch off), "
    + "change_at_fixed_specifications.item_pension; a cost inside A", ends: { low: item[0], high: item[1] } };
}
if (failed) {
  console.error(`${failed} gate(s) failed; nothing written`);
  process.exit(1);
}
const out = { case: CASE, lane: LANE, profile: P.MAIN_PROFILE,
  rule: "each fill-in method's end specifications of the case, averaged; capped programs = the group's amount x response",
  capped_lines: cappedLines, block_grant_line: BLOCK_GRANT,
  inputs: Object.fromEntries([`${LANE}/derived/summary.json`, `${LANE}/derived/main_case_bands.csv`, `${LANE}/package.cjs`,
    ...(production ? [PAYLOAD_REL] : [])].map((rel) => [rel, sha256(rel)])),
  end_specifications: ends.map((ij, m) => ({ method: METHODS[m], low: ij[0], high: ij[1] })),
  ends: Object.fromEntries(END.map(({ name, ...x }) => [name, x])) };
if (production) out.production = production;
if (pensionAccrual) out.pension_accrual = pensionAccrual;
fs.mkdirSync(OUT, { recursive: true });
const file = path.join(OUT, `case_ends_${CASE}.json`);
fs.writeFileSync(file, JSON.stringify(out, null, 1) + "\n");
const rel = path.relative(FISCAL, file);
console.log(`wrote ${rel.startsWith("..") ? file : rel}`);
