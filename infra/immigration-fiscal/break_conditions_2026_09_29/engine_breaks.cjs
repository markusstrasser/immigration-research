/* Break conditions on the adopted case (main_case_long_run_2026_09_27): the engine computations behind
 * RESULT.md's C1, C2, C3 and C6 rows.
 *
 *   C1  every combination of the case's own downward alternatives (engine arms plus two additive candidates) and
 *       upward alternatives (engine arms plus three additive items priced beside the account); the minimal sets
 *       that move the band's midpoint by more than a quarter.
 *   C2  the group's direct receipts minus its household transfers at the end specifications (48 / 11), corrected
 *       and uncorrected, and the same tally with Social Security and Part A on accrual (ladder 257, additive).
 *   C3  the dataset corrections split by side: receipt edits alone, spending edits alone, both.
 *   C6  the service-response break-even of each generation, on the generation account's uncorrected models
 *       (generation_account_2026_09_24/derived/model_*.json), with main_case_2026_09_24/sign_reversal.cjs's
 *       definition run unchanged inside a copy of main_case_long_run_2026_09_27/sign_reversal.cjs's withCase.
 *
 * Additive items are ladder figures, not engine runs; they are marked "additive" in the outputs.
 * Run from anywhere: node engine_breaks.cjs  ->  derived/c1_arms.csv, c1_min_cuts.csv, c2_tally.csv,
 * c3_correction_split.csv, c6_generation_break_even.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
const P = require(path.join(ROOT, "main_case_long_run_2026_09_27", "package.cjs"));
const S24 = require(path.join(ROOT, "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, RATES, RESPONSES, ENTERPRISES, ENTERPRISE_RECEIPT, RENTAL, MAIN_SPECS } = P;

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const f4 = (x) => (typeof x === "number" ? x.toFixed(4) : String(x));
const csvText = (rows) => rows.map((r) => r.map(f4).join(",")).join("\n") + "\n";
const mid = (b) => (b[0] + b[1]) / 2;
const OUT = path.join(__dirname, "derived");
const outputs = {};
const readCsv = (rel) => {
  const [head, ...lines] = fs.readFileSync(path.join(ROOT, rel), "utf8").trim().split("\n");
  const keys = head.split(",");
  return lines.map((l) => Object.fromEntries(l.split(",").map((v, i) => [keys[i], v])));
};

// ------------------------------------------------------------------------------------------------ C1
console.log("[C1 the account's magnitude]");
const MAIN = P.central({});
gate("the adopted case reproduces ($321.8194–387.3701bn)", near(MAIN[0], 321.8194, 1e-4) && near(MAIN[1], 387.3701, 1e-4),
  `${MAIN[0].toFixed(4)}–${MAIN[1].toFixed(4)}`);
const M = mid(MAIN);
const LOW_CUT = 0.75 * M, HIGH_CUT = 1.25 * M;

// Engine arms: each is the alternative end of a range the case itself reports (main_case_bands.csv or components.csv).
const LR_KEYS = Object.keys(P.LONG_RUN_VARIANTS).filter((k) => k !== "adopted");
const lrBands = LR_KEYS.map((k) => [k, P.central({ long_run: k })]);
const lrMax = lrBands.reduce((a, b) => (mid(b[1]) > mid(a[1]) ? b : a));
const ARMS = {
  capital_off: { dir: "down", o: { capital: false }, src: "ladder 239: no return on public capital (a convention; main_case_bands.csv 288.02–331.68)", want: [288.02, 331.68] },
  school_within_district: { dir: "down", o: { school_rule: "within_district" }, src: "ladder 230/239: schools at the within-district 0.836 read over the removal", want: [295.94, 362.99] },
  roads_parks_first_year: { dir: "down", o: { long_run: false }, src: "ladder 237: roads and parks at CBO's first-year response 0", want: null },
  enterprises_out: { dir: "down", o: { enterprises: "A" }, src: "ladder 239: government enterprises out (option A)", want: [304.63, 364.37] },
  rental_zero: { dir: "down", o: { rental: 0 }, src: "ladder 239: rental assistance at response 0", want: [317.29, 382.84] },
  capital_7pct: { dir: "up", o: { rates: { low: RATES.reported, high: RATES.reported } }, src: "ladder 238/239: capital at a private 7% return (beside the account)", want: [406.31, 461.62] },
  long_run_high: { dir: "up", o: { long_run: lrMax[0] }, src: `ladder 239: long-run response variant with the largest midpoint (${lrMax[0]})`, want: null },
};
// Additive items: ladder figures at the two ends, not engine runs.
const ADD = {
  property_tax_response: { dir: "down", by: [-27.19, -27.19], src: "ladder 253: property taxes respond like the capital they pay for (candidate, not adopted)" },
  care_low: { dir: "down", by: [-9.2, -9.2], src: "components.csv care: low tail of the care and household-services envelope" },
  pension_accrual_payable: { dir: "up", by: [399.1 - 321.8194, 461.0 - 387.3701], src: "ladder 257: Social Security and Part A on accrual at payable benefits (beside the account)" },
  defense_gdp_share: { dir: "up", by: [60, 60], src: "groups.py conventions (ladder 253 row): defense bounded by share of GDP, about $60bn (47–72)" },
  medical_mcbs65: { dir: "up", by: [11.5091, 11.5073], src: "components.csv medical: the MCBS 65+ bound" },
};
for (const [id, a] of Object.entries(ARMS)) {
  a.band = P.central(a.o);
  if (a.want) gate(`${id} reproduces its published row (0.01)`, near(a.band[0], a.want[0], 0.01) && near(a.band[1], a.want[1], 0.01),
    `${a.band[0].toFixed(2)}–${a.band[1].toFixed(2)}`);
}
const armRows = [["arm", "direction", "kind", "cost_low_bn", "cost_high_bn", "midpoint_bn", "move_pct_of_midpoint", "source"]];
armRows.push(["adopted", "", "engine", MAIN[0], MAIN[1], M, 0, "main_case_long_run_2026_09_27 summary.json"]);
for (const [id, a] of Object.entries(ARMS)) armRows.push([id, a.dir, "engine", a.band[0], a.band[1], mid(a.band), 100 * (mid(a.band) / M - 1), `"${a.src}"`]);
for (const [k, b] of lrBands) armRows.push([`long_run:${k}`, "variant", "engine", b[0], b[1], mid(b), 100 * (mid(b) / M - 1), `"LONG_RUN_VARIANTS ${k}"`]);
for (const [id, a] of Object.entries(ADD)) {
  const b = [MAIN[0] + a.by[0], MAIN[1] + a.by[1]];
  armRows.push([id, a.dir, "additive", b[0], b[1], mid(b), 100 * (mid(b) / M - 1), `"${a.src}"`]);
}
outputs["c1_arms.csv"] = csvText(armRows);

// Every subset of one direction's elements; the engine part is one joint run, the additive part is added.
function subsetBand(ids) {
  const o = {};
  for (const id of ids) if (ARMS[id]) Object.assign(o, ARMS[id].o);
  const b = P.central(o);
  for (const id of ids) if (ADD[id]) { b[0] += ADD[id].by[0]; b[1] += ADD[id].by[1]; }
  return b;
}
const cutRows = [["direction", "set", "size", "cost_low_bn", "cost_high_bn", "midpoint_bn", "move_pct_of_midpoint", "minimal"]];
for (const dir of ["down", "up"]) {
  const ids = Object.keys(ARMS).filter((k) => ARMS[k].dir === dir).concat(Object.keys(ADD).filter((k) => ADD[k].dir === dir));
  const breaks = [];
  for (let mask = 1; mask < 1 << ids.length; mask += 1) {
    const set = ids.filter((_, i) => mask & (1 << i));
    const b = subsetBand(set);
    const crosses = dir === "down" ? mid(b) < LOW_CUT : mid(b) > HIGH_CUT;
    if (crosses) breaks.push({ set, b });
  }
  const minimal = breaks.filter((x) => !breaks.some((y) => y !== x && y.set.length < x.set.length && y.set.every((s) => x.set.includes(s))));
  minimal.sort((x, y) => x.set.length - y.set.length || x.set.join("+").localeCompare(y.set.join("+")));
  for (const x of minimal) cutRows.push([dir, x.set.join("+"), x.set.length, x.b[0], x.b[1], mid(x.b), 100 * (mid(x.b) / M - 1), "yes"]);
  const all = subsetBand(ids);
  cutRows.push([dir, "ALL:" + ids.join("+"), ids.length, all[0], all[1], mid(all), 100 * (mid(all) / M - 1), "stack"]);
}
outputs["c1_min_cuts.csv"] = csvText(cutRows);
console.log(`  thresholds: midpoint ${M.toFixed(2)}, a quarter down ${LOW_CUT.toFixed(2)}, up ${HIGH_CUT.toFixed(2)}`);

// ------------------------------------------------------------------------------------------------ C2 and C3
console.log("[C2 taxes against benefits; C3 corrections by side]");
const payload = P.correctionsPayload();
const m27 = Engine.applyCorrections(MODEL, payload);
const ENDS = [["low_end_48", 48], ["high_end_11", 11]];
const tallyRows = [["model", "end", "spec", "direct_receipts_bn", "household_transfers_bn", "tally_bn", "accrual_move_bn", "tally_on_accrual_bn"]];
const ACCRUAL = ADD.pension_accrual_payable.by;
for (const [lab, m] of [["corrected", m27], ["uncorrected", MODEL]]) ENDS.forEach(([end, i], j) => {
  const ev = P.evaluateFull(m, MAIN_SPECS[i]).evaluation;
  const rec = ev.classes.direct_receipts.responsive_bn, tr = ev.classes.household_transfer.responsive_bn;
  tallyRows.push([lab, end, i, rec, tr, rec - tr, ACCRUAL[j], rec - tr - ACCRUAL[j]]);
});
gate("specs 48 and 11 are the case's ends", near(P.evaluateFull(m27, MAIN_SPECS[48]).cost_bn, MAIN[0], 1e-4)
  && near(P.evaluateFull(m27, MAIN_SPECS[11]).cost_bn, MAIN[1], 1e-4));
outputs["c2_tally.csv"] = csvText(tallyRows);

const bySide = (side) => Engine.applyCorrections(MODEL, { lines: payload.lines, edits: payload.edits.filter((e) => e.side === side) });
const mRec = bySide("receipt"), mSp = bySide("spending");
gate("the payload has only receipt and spending edits", payload.edits.every((e) => e.side === "receipt" || e.side === "spending"),
  `${payload.edits.length} edits`);
const splitRows = [["end", "spec", "uncorrected_bn", "receipt_edits_only_bn", "spending_edits_only_bn", "all_edits_bn",
  "tax_side_move_bn", "spending_side_move_bn", "interaction_bn", "net_move_bn"]];
for (const [end, i] of ENDS) {
  const c = (m) => P.evaluateFull(m, MAIN_SPECS[i]).cost_bn;
  const u = c(MODEL), r = c(mRec), s = c(mSp), a = c(m27);
  splitRows.push([end, i, u, r, s, a, r - u, s - u, a - u - (r - u) - (s - u), a - u]);
}
outputs["c3_correction_split.csv"] = csvText(splitRows);

// ------------------------------------------------------------------------------------------------ C6
console.log("[C6 generation break-even]");
// A copy of main_case_long_run_2026_09_27/sign_reversal.cjs withCase("enterprises_at_s"), the variant the case quotes.
const GG = RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG.low : GG.high }));
const readingOf = (g) => (g === GG.low ? "low" : g === GG.high ? "high" : null);
function atS(f) {
  const evaluate = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response;
    const reading = readingOf(st.general_government_response);
    if (!reading) throw new Error("[BLOCKED] general government response is neither adopted value");
    const ev = evaluate(m, Object.assign({}, st, { response_override: Object.assign({}, st.response_override, { [RENTAL]: 1, [ENTERPRISE_RECEIPT]: s }) }));
    const cap = P.capitalReturn(ev, { share: st.school_share, reading, rate: RATES[reading], enterprises: ENTERPRISES, long_run: null });
    const enterprise = cap.components.filter((c) => c.group === "enterprise").reduce((a, c) => a + c.return_bn, 0);
    return Object.assign({}, ev, { welfare_bn: ev.welfare_bn - (cap.total_bn - (1 - s) * enterprise) });
  };
  try { return f(); } finally { Engine.evaluate = evaluate; }
}
const pub = readCsv("main_case_long_run_2026_09_27/derived/sign_reversal.csv");
const want = (a) => pub.find((r) => r.measure === `service_break_even_${a}__enterprises_at_s`);
for (const a of ["personal", "shared"]) {
  const be = atS(() => S24.breakEven(m27, a, PAIRS));
  gate(`union break-even, ${a}, reproduces sign_reversal.csv (1e-4)`, near(be[0], +want(a).sept27_low, 1e-4) && near(be[1], +want(a).sept27_high, 1e-4),
    `${(100 * be[0]).toFixed(2)}–${(100 * be[1]).toFixed(2)}%`);
}
const GEN = readCsv("generation_account_2026_09_24/derived/generation_results.csv");
const genRows = [["convention", "generation", "uncorrected_cost_low_end_bn", "uncorrected_cost_high_end_bn", "correction_low_end_bn",
  "correction_high_end_bn", "break_even_personal_most", "break_even_personal_least", "break_even_shared_most", "break_even_shared_least"]];
// breakEven returns [most adverse, least adverse] (main_case_2026_09_24/sign_reversal.cjs:56-63); the header followed
// the other order until 2026-09-29, found by the v4 rerun.
for (const conv of ["a", "b"]) for (const g of ["G1", "G2", "G3plus"]) {
  const file = path.join(ROOT, "generation_account_2026_09_24", "derived", conv === "a" ? `model_${g}.json` : `model_b_${g}.json`);
  const raw = JSON.parse(fs.readFileSync(file, "utf8"));
  // The payload's three correction lines, empty, as evaluateFull's withSyntheticLines adds them: the definition
  // calls Engine.evaluate directly and the capital return keys read those lines.
  const mg = Engine.applyCorrections(raw, { lines: payload.lines.filter((l) => !raw.spending.lines.some((x) => x.id === l.id)), edits: [] });
  const row = (end) => GEN.find((r) => r.convention === conv && r.generation === g && r.band_end === end);
  const lo = P.evaluateFull(mg, MAIN_SPECS[48]).cost_bn, hi = P.evaluateFull(mg, MAIN_SPECS[11]).cost_bn;
  gate(`${conv} ${g}: the uncorrected model reproduces generation_results.csv at 48 / 11 (1e-3)`,
    near(lo, +row("low").uncorrected_same_spec_bn, 1e-3) && near(hi, +row("high").uncorrected_same_spec_bn, 1e-3), `${lo.toFixed(3)} / ${hi.toFixed(3)}`);
  const bp = atS(() => S24.breakEven(mg, "personal", PAIRS)), bs = atS(() => S24.breakEven(mg, "shared", PAIRS));
  genRows.push([conv, g, lo, hi, +row("low").correction_bn, +row("high").correction_bn, bp[0], bp[1], bs[0], bs[1]]);
}
outputs["c6_generation_break_even.csv"] = csvText(genRows);

if (failures) {
  console.error(`[BLOCKED] ${failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
for (const [name, text] of Object.entries(outputs)) fs.writeFileSync(path.join(OUT, name), text);
console.log("\n[written] " + Object.keys(outputs).join(", "));
console.log(fs.readFileSync(path.join(OUT, "c1_min_cuts.csv"), "utf8"));
console.log(fs.readFileSync(path.join(OUT, "c2_tally.csv"), "utf8"));
console.log(fs.readFileSync(path.join(OUT, "c3_correction_split.csv"), "utf8"));
console.log(fs.readFileSync(path.join(OUT, "c6_generation_break_even.csv"), "utf8"));
