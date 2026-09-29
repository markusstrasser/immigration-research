/* Break conditions on the main case adopted 2026-09-29 (v4: main_case_2026_09_29, key sept29): the engine computations
 * behind RESULT.md's "v4 case (sept29)" rows for C1, C2, C3 and C6, beside engine_breaks.cjs's September 27 files, which
 * this script does not touch.
 *
 * v4 contains item 5 (long-run property taxes) and the pension accrual at payable benefits. The arms that added them
 * to the September 27 case now remove them, as engine runs of the package's item options: pension_cash (the cash set,
 * pension4 "cash") goes down and property_none (property "none", September 27's zero) goes up. Item 5's own range
 * ends are engine arms too (property_reading "high" down; "low", +3.1, is dominated by property_none and only listed).
 *
 *   C1  every combination of the case's downward alternatives (engine arms plus the care tail) and upward alternatives
 *       (engine arms plus three items priced beside the account: scheduled benefits, defense by GDP share, the MCBS 65+
 *       bound); the minimal sets that move the band's midpoint by more than a quarter. The first-year horizon (P02) is
 *       its own row: CBO's first-year school response, no long-run roads, parks, property taxes, rental assistance or
 *       capital return (the September 27 first-year rule, plus property at zero and roads on resources, since v4's
 *       miles key needs the long-run subfunction responses).
 *   C2  direct receipts minus household transfers at the end specifications (48 / 11) on the case (accrual), the cash
 *       set, v4's items without the dataset corrections and the uncorrected model; and the service break-even
 *       (clause 2) on the case and the cash set, with main_case_2026_24/sign_reversal.cjs's definition run unchanged
 *       inside a copy of main_case_2026_09_29/sign_reversal.cjs's withCase.
 *   C3  the dataset corrections (the September 27 payload's 278 edits, which open v4's payload unchanged) split by
 *       side, with v4's items (the rest of the payload, its receipt lines and production grid) held in every run.
 *   C6  each generation's cost and service break-even on the generation account's sept29 payloads (its gated
 *       generation_corrections_sept29*.json, applied to its generation models with the union's meta), the case and
 *       the cash set; their sha256 is written beside the results.
 *
 * Additive items are figures priced beside the account, not engine runs; they are marked "additive" in the outputs.
 * Run from anywhere: node engine_breaks_sept29.cjs  ->  derived/c1_arms_sept29.csv, c1_min_cuts_sept29.csv,
 * c2_tally_sept29.csv, c2_break_even_sept29.csv, c3_correction_split_sept29.csv, c6_generation_break_even_sept29.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const ROOT = path.join(__dirname, "..");
const LANE = "main_case_2026_09_29";
const P = require(path.join(ROOT, LANE, "package.cjs"));
const S24 = require(path.join(ROOT, "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, RATES, ENTERPRISES, ENTERPRISE_RECEIPT, RENTAL, MAIN_SPECS, readJson } = P;
const REF = MODEL.receipts.reference;

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const f4 = (x) => (typeof x === "number" ? x.toFixed(4) : String(x));
const csvText = (rows) => rows.map((r) => r.map(f4).join(",")).join("\n") + "\n";
const mid = (b) => (b[0] + b[1]) / 2;
const sum = (xs) => xs.reduce((a, b) => a + b, 0);
const OUT = path.join(__dirname, "derived");
const outputs = {};
// Quoted fields (labels with commas, as in components.csv) are one field; a row with another field count stops the run.
function splitCsv(line) {
  const out = [];
  let cur = "", quoted = false;
  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (quoted) {
      if (ch === '"' && line[i + 1] === '"') { cur += '"'; i += 1; } else if (ch === '"') quoted = false; else cur += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ",") { out.push(cur); cur = ""; } else cur += ch;
  }
  out.push(cur);
  return out;
}
const readCsv = (rel) => {
  const [head, ...lines] = fs.readFileSync(path.join(ROOT, rel), "utf8").trim().split("\n");
  const keys = splitCsv(head);
  return lines.map((l) => {
    const v = splitCsv(l);
    if (v.length !== keys.length) throw new Error(`[BLOCKED] ${rel}: a row with ${v.length} fields for ${keys.length} columns`);
    return Object.fromEntries(v.map((x, i) => [keys[i], x]));
  });
};
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(ROOT, rel))).digest("hex");
const ENDS = [["low_end_48", 48], ["high_end_11", 11]];

// ------------------------------------------------------------------------------------------------ C1
console.log("[C1 the account's magnitude, sept29]");
const MAIN = P.central({});
gate("the adopted case reproduces ($371.4146–434.8410bn)", near(MAIN[0], 371.4146, 1e-4) && near(MAIN[1], 434.8410, 1e-4),
  `${MAIN[0].toFixed(4)}–${MAIN[1].toFixed(4)}`);
const M = mid(MAIN);
const LOW_CUT = 0.75 * M, HIGH_CUT = 1.25 * M;
const bands = readCsv(`${LANE}/derived/main_case_bands.csv`).filter((r) => r.profile === P.MAIN_PROFILE);
const bandRow = (v) => { const r = bands.find((x) => x.variant === v); return [+r.cost_low_bn, +r.cost_high_bn]; };
const comps = readCsv(`${LANE}/derived/components.csv`);
const comp = (id) => comps.find((r) => r.component === id);
const PROP = comp("property_long_run"), CARE = comp("care"), MED = comp("medical");

// A long-run variant the package cannot run with v4's items (the miles key needs the long-run subfunction responses) is
// listed as blocked, not searched.
const LR_KEYS = Object.keys(P.LONG_RUN_VARIANTS).filter((k) => k !== "adopted");
const lrBlocked = [];
const lrBands = LR_KEYS.flatMap((k) => {
  try { return [[k, P.central({ long_run: k })]]; } catch (e) { lrBlocked.push([k, e.message.split("\n")[0]]); return []; }
});
const lrMax = lrBands.reduce((a, b) => (mid(b[1]) > mid(a[1]) ? b : a));
// Engine arms: each is the alternative end of a range the case reports (main_case_bands.csv or components.csv), or an
// item of v4 turned off.
const ARMS = {
  capital_off: { dir: "down", o: { capital: false }, src: "ladder 239: no return on public capital (a convention; main_case_bands.csv without_capital_return)", want: bandRow("without_capital_return") },
  school_within_district: { dir: "down", o: { school_rule: "within_district" }, src: "ladder 230/239: schools at the within-district 0.836 read over the removal", want: bandRow("school_within_district") },
  roads_parks_first_year: { dir: "down", o: { long_run: false, roads: "resources" }, src: "ladder 237: roads and parks at CBO's first-year response 0; v4's miles key needs the long-run subfunction responses, so roads are on resources here", want: null },
  enterprises_out: { dir: "down", o: { enterprises: "A" }, src: "ladder 239: government enterprises out (option A)", want: bandRow("enterprises_out_option_a") },
  rental_zero: { dir: "down", o: { rental: 0 }, src: "ladder 239: rental assistance at response 0", want: bandRow("rental_assistance_at_0") },
  pension_cash: { dir: "down", o: { pension4: "cash" }, src: "decision 2026-09-29 alternative 2: the cash set, Social Security and Medicare counted when paid (the September 27 convention)", want: bandRow("cash_set") },
  property_high_reading: { dir: "down", o: { property_reading: "high" }, src: "components.csv property_long_run: the receipt-side lane's responses at 1 everywhere, case-scaled tenant national", want: [MAIN[0] + +PROP.range_dev_low_end_lo, MAIN[1] + +PROP.range_dev_high_end_lo] },
  capital_7pct: { dir: "up", o: { rates: { low: RATES.reported, high: RATES.reported } }, src: "ladder 238/239: capital at a private 7% return (beside the account)", want: bandRow("capital_return_at_7pct") },
  long_run_high: { dir: "up", o: { long_run: lrMax[0] }, src: `ladder 239: long-run response variant with the largest midpoint (${lrMax[0]})`, want: null },
  property_none: { dir: "up", o: { property: "none" }, src: "item 5 off: property taxes at zero response, the September 27 convention (ladder 253, decision 2026-09-29)", want: null },
};
// Listed, not searched: dominated by property_none in the same direction.
const LISTED = {
  property_low_reading: { dir: "up", o: { property_reading: "low" }, src: "components.csv property_long_run: the receipt-side lane's low responses (dominated by property_none)", want: [MAIN[0] + +PROP.range_dev_low_end_hi, MAIN[1] + +PROP.range_dev_high_end_hi] },
};
// The pension accrual at scheduled benefits, beside the case: the payload's scheduled net ratio in place of ratio_net on
// the case's OASDI receipts (the accrual's own rule), and the pension lane's Part A accrual at scheduled benefits.
const payload = P.correctionsPayload();
const ACC = payload.meta.pension_accrual;
const PEN_FILE = "pension_accrual_2026_09_28/derived/summary.json";
gate(`${PEN_FILE} is the payload's pinned file (${ACC.source.commit})`, sha256(PEN_FILE) === ACC.source.sha256);
const PEN = readJson(PEN_FILE);
const m29 = P.payloadModel();
const oasdiOf = (m, alloc) => {
  const cell = (id) => m.receipts.lines.find((l) => l.id === id).cells[REF][alloc].target_bn;
  return sum(ACC.oasdi_lines.map(cell)) + ACC.se_oasdi_share * cell(ACC.se_line);
};
const PA_SCHED = PEN.scheduled_arm.decomposition.low.part_a_accrual_bn;
const schedAdd = (m) => ENDS.map(([, i]) => (ACC.scheduled_benefits_arm.ratio_net - ACC.ratio_net) * oasdiOf(m, MAIN_SPECS[i].allocation)
  + (PA_SCHED - ACC.part_a_accrual_bn));
{
  // Positive control: the same rule on the September 27 payload's receipts gives the pension lane's scheduled less payable.
  const m27 = Engine.applyCorrections(MODEL, readJson("main_case_long_run_2026_09_27/derived/corrections.json"));
  const got = schedAdd(m27);
  const lane = [PEN.scheduled_arm.case_on_accrual_net_bn.low - PEN.case_on_accrual_net_bn.low,
    PEN.scheduled_arm.case_on_accrual_net_bn.high - PEN.case_on_accrual_net_bn.high];
  gate("the scheduled-benefits rule on the September 27 receipts reproduces the pension lane's scheduled less payable (1e-6)",
    near(got[0], lane[0], 1e-6) && near(got[1], lane[1], 1e-6), `${got.map(f4).join(" / ")} vs ${lane.map(f4).join(" / ")}`);
}
const ADD = {
  care_low: { dir: "down", by: [+CARE.range_dev_low_end_lo, +CARE.range_dev_high_end_lo], src: "components.csv care: low tail of the care and household-services envelope" },
  pension_scheduled: { dir: "up", by: schedAdd(m29), src: "decision 2026-09-29 alternative 3: the accrual at scheduled benefits (net ratio 1.2406 for 0.9737 on the case's OASDI receipts; Part A 45.35 for 41.14), beside the account" },
  defense_gdp_share: { dir: "up", by: [60, 60], src: "groups.py conventions (ladder 253 row): defense bounded by share of GDP, about $60bn (47–72)" },
  medical_mcbs65: { dir: "up", by: [+MED.range_dev_low_end_hi, +MED.range_dev_high_end_hi], src: "components.csv medical: the MCBS 65+ bound" },
};
gate("every additive item is a finite pair", Object.values(ADD).every((a) => a.by.length === 2 && a.by.every(Number.isFinite)),
  Object.entries(ADD).map(([id, a]) => `${id} ${a.by.map(f4).join(" / ")}`).join("; "));
for (const [id, a] of Object.entries(Object.assign({}, ARMS, LISTED))) {
  a.band = P.central(a.o);
  if (a.want) gate(`${id} reproduces its published row (0.01)`, near(a.band[0], a.want[0], 0.01) && near(a.band[1], a.want[1], 0.01),
    `${a.band[0].toFixed(2)}–${a.band[1].toFixed(2)}`);
}
// The first-year horizon: the September 27 lane's rule (main_case.cjs: long-run lines, rental assistance, capital and the
// enterprise receipt off, CBO's one-year school response), with item 5 at zero (a long-run response) and roads on
// resources; beside it, item 5 kept and the cash set.
const FIRST = { long_run: false, rental: 0, capital: false, enterprise_receipt: 0, school_rule: "one_year", roads: "resources" };
const s27 = readJson("main_case_long_run_2026_09_27/derived/summary.json");
const fyOff = P.central(Object.assign({}, P.V4PKG.OFF, FIRST));
gate("the first-year rule with every v4 item off gives the September 27 lane's first_year_response (1e-9)",
  near(fyOff[0], s27.first_year_response[0], 1e-9) && near(fyOff[1], s27.first_year_response[1], 1e-9), `${fyOff[0].toFixed(4)}–${fyOff[1].toFixed(4)}`);
const HORIZON = {
  first_year_horizon: { o: Object.assign({}, FIRST, { property: "none" }), src: "P02 swap: ladder 229's first-year rule on v4, item 5 at zero (a long-run response), roads on resources" },
  first_year_horizon_property_long_run: { o: FIRST, src: "the same, item 5's long-run property response kept" },
  first_year_horizon_cash: { o: Object.assign({}, FIRST, { property: "none", pension4: "cash" }), src: "the same, pensions on cash" },
};
for (const h of Object.values(HORIZON)) h.band = P.central(h.o);

const armRows = [["arm", "direction", "kind", "cost_low_bn", "cost_high_bn", "midpoint_bn", "move_pct_of_midpoint", "source"]];
armRows.push(["adopted", "", "engine", MAIN[0], MAIN[1], M, 0, `${LANE} summary.json`]);
for (const [id, a] of Object.entries(Object.assign({}, ARMS, LISTED))) {
  armRows.push([id, a.dir, id in LISTED ? "engine (listed)" : "engine", a.band[0], a.band[1], mid(a.band), 100 * (mid(a.band) / M - 1), `"${a.src}"`]);
}
for (const [k, b] of lrBands) armRows.push([`long_run:${k}`, "variant", "engine", b[0], b[1], mid(b), 100 * (mid(b) / M - 1), `"LONG_RUN_VARIANTS ${k}"`]);
for (const [k, why] of lrBlocked) armRows.push([`long_run:${k}`, "variant", "blocked", "", "", "", "", `"${why.replace(/"/g, "'")}"`]);
for (const [id, a] of Object.entries(ADD)) {
  const b = [MAIN[0] + a.by[0], MAIN[1] + a.by[1]];
  armRows.push([id, a.dir, "additive", b[0], b[1], mid(b), 100 * (mid(b) / M - 1), `"${a.src}"`]);
}
for (const [id, h] of Object.entries(HORIZON)) armRows.push([id, "horizon", "engine", h.band[0], h.band[1], mid(h.band), 100 * (mid(h.band) / M - 1), `"${h.src}"`]);
outputs["c1_arms_sept29.csv"] = csvText(armRows);

// Every subset of one direction's elements; the engine part is one joint run (cached by its arms), the additive part is
// added.
const joint = new Map();
function subsetBand(ids) {
  const o = {};
  const engineIds = ids.filter((id) => ARMS[id]);
  for (const id of engineIds) Object.assign(o, ARMS[id].o);
  const key = engineIds.join("+");
  if (!joint.has(key)) joint.set(key, P.central(o));
  const b = joint.get(key).slice();
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
outputs["c1_min_cuts_sept29.csv"] = csvText(cutRows);
console.log(`  thresholds: midpoint ${M.toFixed(2)}, a quarter down ${LOW_CUT.toFixed(2)}, up ${HIGH_CUT.toFixed(2)}`);

// ------------------------------------------------------------------------------------------------ C2 and C3
console.log("[C2 taxes against benefits; C3 corrections by side, sept29]");
const p27 = readJson("main_case_long_run_2026_09_27/derived/corrections.json");
const N27 = p27.edits.length;
gate(`v4's payload opens with the September 27 payload's ${N27} edits, unchanged`,
  payload.edits.slice(0, N27).every((e, k) => JSON.stringify(e) === JSON.stringify(p27.edits[k])), `${payload.edits.length} edits in all`);
const DATASET = payload.edits.slice(0, N27), TAIL = payload.edits.slice(N27);
gate("the dataset corrections have only receipt and spending edits", DATASET.every((e) => (e.side === "receipt" || e.side === "spending") && e.by));
// v4's items with a subset of the dataset corrections, in the payload's order (the tail's national-scale edits scale the
// dataset edits on their lines, as in the case).
const withDataset = (keep) => Engine.applyCorrections(MODEL, { lines: payload.lines, receipt_lines: payload.receipt_lines,
  production: payload.production, edits: DATASET.filter(keep).concat(TAIL), meta: payload.meta });
const mBase = withDataset(() => false), mRec = withDataset((e) => e.side === "receipt"), mSp = withDataset((e) => e.side === "spending");
const mAll = withDataset(() => true);
gate("all the dataset corrections with v4's items is the case at both ends (1e-9)",
  ENDS.every(([, i], j) => near(P.evaluateFull(mAll, MAIN_SPECS[i]).cost_bn, MAIN[j], 1e-9)));
// The tail's edits are increments computed on the corrected model. The pension switch is a level (candidate v4
// package.cjs withPensionNet: Social Security at ratio_net x the model's OASDI receipts; Medicare with Part A's share of
// its benefits replaced by the Part A accrual, part_a_rule "fixed"), so on a subset of the dataset corrections it is
// rebuilt at that subset's receipts and benefits: a check that moves OASDI receipts moves the accrual, and a check on
// current Social Security or Part A benefits no longer reaches the case. The other items stay at their increments
// (each is proportional to a line amount or a share change; rebuilding them needs the builder).
const { ALLOCS } = P;
const TAIL_SS = TAIL.filter((e) => e.side === "spending" && e.line === "social_security");
const TAIL_MED = TAIL.filter((e) => e.side === "spending" && e.line === "medicare");
const prefKey = (id) => MODEL.spending.lines.find((l) => l.id === id).preferred_key;
gate("the tail's pension switch is one Social Security and one Medicare edit, each on the line's preferred key",
  TAIL_SS.length === 1 && TAIL_MED.length === 1 && TAIL_SS[0].key === prefKey("social_security") && TAIL_MED[0].key === prefKey("medicare"));
const benefit = (m, id, a) => { const l = m.spending.lines.find((x) => x.id === id); return l.keys[l.preferred_key][a].target_bn; };
function pensionRebuilt(m) {
  const by = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
  const ss = by((a) => ACC.ratio_net * oasdiOf(m, a) - benefit(m, "social_security", a));
  const med = by((a) => {
    const pre = benefit(m, "medicare", a) - TAIL_MED[0].by[a];
    return (1 - ACC.part_a_share) * pre + ACC.part_a_accrual_bn - benefit(m, "medicare", a);
  });
  const edits = [{ side: "spending", line: "social_security", key: TAIL_SS[0].key, by: ss }, { side: "spending", line: "medicare", key: TAIL_MED[0].key, by: med }];
  return { m: Engine.applyCorrections(m, { lines: [], receipt_lines: [], edits }), shift: [ss, med] };
}
const R = { base: pensionRebuilt(mBase), rec: pensionRebuilt(mRec), sp: pensionRebuilt(mSp), all: pensionRebuilt(mAll) };
gate("rebuilt on the full payload, the pension switch moves nothing (1e-9)", R.all.shift.every((x) => ALLOCS.every((a) => Math.abs(x[a]) < 1e-9)));
const cashPayload = readJson("main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json");
const PC = P.forPayload(cashPayload);
const mCash = PC.payloadModel();
const CASH = ENDS.map(([, i]) => PC.evaluateFull(mCash, PC.MAIN_SPECS[i]).cost_bn);
gate("the cash payload is the cash set at both ends (main_case_bands.csv cash_set, 1e-4)", CASH.every((x, j) => near(x, bandRow("cash_set")[j], 1e-4)),
  `${CASH[0].toFixed(4)}–${CASH[1].toFixed(4)}`);
// The tally at scheduled benefits moves by the scheduled rule on each model's own OASDI receipts.
const tallyRows = [["model", "end", "spec", "direct_receipts_bn", "household_transfers_bn", "tally_bn", "scheduled_move_bn", "tally_at_scheduled_bn"]];
for (const [lab, pkg, m, accrual] of [["case_accrual", P, m29, true], ["cash_set", PC, mCash, false],
  ["v4_items_without_dataset_corrections", P, R.base.m, true], ["v4_items_without_dataset_corrections_increments_held", P, mBase, true],
  ["uncorrected_no_v4_items", P, MODEL, false]]) {
  const sched = accrual ? schedAdd(m) : null;
  ENDS.forEach(([end, i], j) => {
    const ev = pkg.evaluateFull(m, pkg.MAIN_SPECS[i]).evaluation;
    const rec = ev.classes.direct_receipts.responsive_bn, tr = ev.classes.household_transfer.responsive_bn;
    tallyRows.push([lab, end, i, rec, tr, rec - tr, accrual ? sched[j] : "", accrual ? rec - tr - sched[j] : ""]);
  });
}
outputs["c2_tally_sept29.csv"] = csvText(tallyRows);

// Clause 2: the service break-even, main_case_2026_09_24's definition inside a copy of main_case_2026_09_29/
// sign_reversal.cjs's withCase (rental assistance at 1; the enterprise receipts at 1, or at s in the variant; every other
// receipt response of meta.responses fixed; the capital return from the same evaluation).
const GG = P.RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG.low : GG.high }));
const readingOf = (g) => (g === GG.low ? "low" : g === GG.high ? "high" : null);
function withCase(pkg, variant, f) {
  const enterprise = [ENTERPRISE_RECEIPT].concat(pkg.ENTERPRISE_SPLITS.map((id) => "receipt:" + id));
  const fixed = Object.entries(pkg.LINE_RESPONSES).filter(([k]) => k.startsWith("receipt:") && !enterprise.includes(k));
  const evaluate = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response;
    const reading = readingOf(st.general_government_response);
    if (!reading) throw new Error(`[BLOCKED] general government at ${st.general_government_response}, neither adopted response`);
    const atS = variant === "enterprises_at_s";
    const extra = { [RENTAL]: 1 };
    for (const k of enterprise) extra[k] = atS ? s : 1;
    for (const [k, e] of fixed) extra[k] = e[reading];
    const ev = evaluate(m, Object.assign({}, st, { response_override: Object.assign({}, st.response_override, extra) }));
    const cap = pkg.capitalReturn(ev, { share: st.school_share, reading, rate: RATES[reading], enterprises: ENTERPRISES, long_run: null });
    const ent = cap.components.filter((c) => c.group === "enterprise").reduce((a, c) => a + c.return_bn, 0);
    return Object.assign({}, ev, { welfare_bn: ev.welfare_bn - (cap.total_bn - (atS ? (1 - s) * ent : 0)) });
  };
  try { return f(); } finally { Engine.evaluate = evaluate; }
}
const pubSR = readCsv(`${LANE}/derived/sign_reversal.csv`);
const beRows = [["case", "variant", "allocation", "break_even_most_adverse", "break_even_least_adverse"]];
for (const [lab, pkg, m] of [["case_accrual", P, m29], ["cash_set", PC, mCash]]) {
  for (const variant of ["enterprises_at_1", "enterprises_at_s"]) for (const a of ["personal", "shared"]) {
    const be = withCase(pkg, variant, () => S24.breakEven(m, a, PAIRS));
    if (lab === "case_accrual") {
      const want = pubSR.find((r) => r.measure === `service_break_even_${a}${variant === "enterprises_at_s" ? "__enterprises_at_s" : ""}`);
      gate(`case break-even, ${a}, ${variant}, reproduces ${LANE} sign_reversal.csv (1e-4)`,
        near(be[0], +want.sept29_low, 1e-4) && near(be[1], +want.sept29_high, 1e-4), `${(100 * be[0]).toFixed(2)}% to ${(100 * be[1]).toFixed(2)}%`);
    }
    beRows.push([lab, variant, a, be[0], be[1]]);
  }
}
outputs["c2_break_even_sept29.csv"] = csvText(beRows);

// C3: the dataset corrections by side on v4, v4's items in every run: the pension switch rebuilt on each subset (the
// reading the RESULT quotes), and beside it every tail increment held. The tax and spending side columns split by the
// edits' side; on the rebuilt reading the receipt edits also move the accrual. The line-type columns split by the lines
// that move: taxes are the receipt edits' move with every spending line held (the held reading's tax side), spending is
// the rest of the net. oasdi_receipts_move_bn is what the dataset corrections move the OASDI receipts by; ratio_net times
// it is the accrual's follow-through (a cost move).
const splitRows = [["reading", "end", "spec", "v4_items_only_bn", "receipt_edits_only_bn", "spending_edits_only_bn", "all_edits_bn",
  "tax_side_move_bn", "spending_side_move_bn", "interaction_bn", "net_move_bn", "taxes_move_by_line_type_bn",
  "spending_move_by_line_type_bn", "oasdi_receipts_move_bn", "accrual_follow_through_bn"]];
for (const [end, i] of ENDS) {
  const c = (m) => P.evaluateFull(m, MAIN_SPECS[i]).cost_bn;
  const dO = oasdiOf(mAll, MAIN_SPECS[i].allocation) - oasdiOf(mBase, MAIN_SPECS[i].allocation);
  const taxes = c(mRec) - c(mBase);
  const rebuilt = c(R.rec.m) - c(R.base.m);
  gate(`${end}: rebuilt, the receipt edits move the cost by their taxes plus ratio_net x their OASDI move (1e-9)`,
    near(rebuilt, taxes + ACC.ratio_net * dO, 1e-9), `${rebuilt.toFixed(4)} = ${taxes.toFixed(4)} + ${(ACC.ratio_net * dO).toFixed(4)}`);
  for (const [reading, set] of [["pension_rebuilt", { u: R.base.m, r: R.rec.m, s: R.sp.m, a: R.all.m }], ["increments_held", { u: mBase, r: mRec, s: mSp, a: mAll }]]) {
    const u = c(set.u), r = c(set.r), s = c(set.s), a = c(set.a);
    splitRows.push([reading, end, i, u, r, s, a, r - u, s - u, a - u - (r - u) - (s - u), a - u, taxes, a - u - taxes, dO, ACC.ratio_net * dO]);
  }
}
splitRows.splice(1, splitRows.length - 1, ...splitRows.slice(1).sort((x, y) => (x[0] === y[0] ? 0 : x[0] === "pension_rebuilt" ? -1 : 1)));
outputs["c3_correction_split_sept29.csv"] = csvText(splitRows);

// ------------------------------------------------------------------------------------------------ C6
console.log("[C6 generations on the sept29 payloads]");
const GEN = "generation_account_2026_09_24/derived";
const genRows = [["case", "convention", "generation", "cost_low_end_bn", "cost_high_end_bn", "break_even_personal_most", "break_even_personal_least",
  "break_even_shared_most", "break_even_shared_least"]];
const genHashes = [["file", "sha256"]];
for (const [lab, pkg, file, results] of [["case_accrual", P, "generation_corrections_sept29.json", "generation_results_sept29.csv"],
  ["cash_set", PC, "generation_corrections_sept29_cash.json", "generation_results_sept29_cash.csv"]]) {
  genHashes.push([`${GEN}/${file}`, sha256(`${GEN}/${file}`)], [`${GEN}/${results}`, sha256(`${GEN}/${results}`)]);
  const gp = readJson(`${GEN}/${file}`).payloads;
  const res = readCsv(`${GEN}/${results}`);
  const meta = pkg.correctionsPayload().meta;
  for (const conv of ["a", "b"]) {
    const costs = { low: 0, high: 0 };
    for (const g of ["G1", "G2", "G3plus"]) {
      const raw = readJson(`${GEN}/${conv === "a" ? `model_${g}.json` : `model_b_${g}.json`}`);
      const mg = Engine.applyCorrections(raw, Object.assign({}, gp[conv][g], { meta }));
      const row = (end) => res.find((r) => r.convention === conv && r.generation === g && r.band_end === end);
      const lo = pkg.evaluateFull(mg, pkg.MAIN_SPECS[48]).cost_bn, hi = pkg.evaluateFull(mg, pkg.MAIN_SPECS[11]).cost_bn;
      gate(`${lab} ${conv} ${g}: the corrected model reproduces ${results} at 48 / 11 (1e-6)`,
        near(lo, +row("low").cost_bn, 1e-6) && near(hi, +row("high").cost_bn, 1e-6), `${lo.toFixed(4)} / ${hi.toFixed(4)}`);
      costs.low += lo; costs.high += hi;
      const bp = withCase(pkg, "enterprises_at_s", () => S24.breakEven(mg, "personal", PAIRS));
      const bs = withCase(pkg, "enterprises_at_s", () => S24.breakEven(mg, "shared", PAIRS));
      genRows.push([lab, conv, g, lo, hi, bp[0], bp[1], bs[0], bs[1]]);
    }
    const want = lab === "case_accrual" ? MAIN : CASH;
    gate(`${lab} ${conv}: the three generations add to the case at 48 / 11 (1e-6)`, near(costs.low, want[0], 1e-6) && near(costs.high, want[1], 1e-6),
      `${costs.low.toFixed(4)} / ${costs.high.toFixed(4)}`);
  }
}
outputs["c6_generation_break_even_sept29.csv"] = csvText(genRows);
outputs["c6_inputs_sept29.csv"] = genHashes.map((r) => r.join(",")).join("\n") + "\n";

if (failures) {
  console.error(`[BLOCKED] ${failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
for (const [name, text] of Object.entries(outputs)) fs.writeFileSync(path.join(OUT, name), text);
console.log("\n[written] " + Object.keys(outputs).join(", "));
for (const name of ["c1_min_cuts_sept29.csv", "c2_tally_sept29.csv", "c2_break_even_sept29.csv", "c3_correction_split_sept29.csv",
  "c6_generation_break_even_sept29.csv"]) console.log(fs.readFileSync(path.join(OUT, name), "utf8"));
