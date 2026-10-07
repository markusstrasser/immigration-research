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
 *
 * --case oct05 runs the same on main case v5 (main_case_2026_10_05, adopted 2026-10-05: v4 plus the lineage's 3.04M
 * added people, counted whole) and writes the same files with the suffix _oct05. Its package has v4's API; a pension
 * switch other than the case's is its cash set's package (P.CASH), so the cash arms run there. The lineage's edits
 * (meta.lineage.edits, after v4's) are one more item held in every C3 run, and the pension switch is rebuilt on the
 * union's part only (the lineage keeps its own accrual, each part at its own ratio). C1 adds the lineage's alternatives
 * (main_case_lineage_2026_10_05: arms a and c, C3 +- 1 SE, the ancestry-share count, the replacement child), each the
 * change of its band from the central on the set (or the cash set with cash pensions), added to the engine part
 * [APPROX: additive], at most one per combination. The scheduled-benefits item raises the lineage's accrual in the
 * union's proportion [ASSUMPTION]. C6 reads the generation account's oct05 files (G3+ carries the lineage).
 *
 * --case oct07 runs it on main case v6 (main_case_2026_10_07: v5 plus the items of its payload's meta.items) and writes
 * the suffix _oct07. Its edit sets' edits follow the lineage's and are held in every C3 run with them. The pension item
 * (the 2026 Trustees' separate-funds arm) moves the payload's ratio_net and Part A accrual and adds cell shifts on Social
 * Security and Medicare whose union_* parts join the union's switch (the tail's) and whose lineage_* parts join the
 * lineage's own accrual, so the rebuilt switch is the case's on the full payload. The case's scheduled-benefits arm stays
 * on the 2025 reports, so the scheduled rule takes the scheduled arm on the 2026 inputs instead
 * (scheduled_tr2026.py -> derived/scheduled_tr2026.json, gated to this payload); its positive control stays on the 2025
 * values (the payload's previous.oct05 and the pension lane file it pins). The union at the case's responses carries the
 * edit sets' union parts (engine_lines.cjs's rule). The lineage's alternatives are v6's own: the case lane's
 * summary.json v6.companions (arms a and c, C3 -/+ 1 SE, the ancestry-share count's stated bound) and the ancestry share
 * at the population lane's convention on v6's generation costs (the case lane's ancestry_share.cjs rowsFor, read-only),
 * each its band's change from the case on the set and from the cash set. The replacement rows, which v6 does not build,
 * are v5's changes from v5's lineage central carried to v6 [APPROX: additive; ASSUMPTION: each moves v6 as it moves v5].
 * The tally's lineage arms a and c are v5's lines moved by the case's change from v5 [APPROX]. C1 adds the items' own
 * arms (summary.json v6.arms: the 2026 inputs on combined funds, retiree health's six, the age mix at birth cohorts and
 * on rough keys), each its band's change from the case on the set or the cash set [APPROX: additive], at most one per
 * item in a combination; the stacks take each item's largest arm in their direction. C6 reads the generation account's
 * oct07 files.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const ROOT = path.join(__dirname, "..");
const CASES = {
  sept29: { lane: "main_case_2026_09_29", band: [371.4146, 434.8410], cash: "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json" },
  oct05: { lane: "main_case_2026_10_05", band: [390.2940, 461.2431], cash: "main_case_2026_10_05/derived/corrections_cash.json" },
  oct07: { lane: "main_case_2026_10_07", band: [389.0826, 461.4797], cash: "main_case_2026_10_07/derived/corrections_cash.json" },
};
const CASE_ARG = process.argv.indexOf("--case");
const CASE = CASE_ARG > 0 ? process.argv[CASE_ARG + 1] : "sept29";
if (!CASES[CASE]) throw new Error(`[BLOCKED] --case ${CASE}: not one of ${Object.keys(CASES).join(", ")}`);
const LANE = CASES[CASE].lane;
const P = require(path.join(ROOT, LANE, "package.cjs"));
const LIN = CASE === "sept29" ? null : P.correctionsPayload().meta.lineage;   // oct05: the lineage's meta
if (CASE !== "sept29" && !(LIN && P.CASH)) throw new Error(`[BLOCKED] ${LANE}: no lineage or no cash package`);
const PC_ = LIN ? P.CASH : null;             // the cash set's package where the case's package runs one pension switch only
// An option set's band: a pension switch other than the case's runs on the cash set's package (oct05).
const centralOf = (o) => (PC_ && o.pension4 === "cash"
  ? PC_.central(Object.fromEntries(Object.entries(o).filter(([k]) => k !== "pension4"))) : P.central(o));
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
console.log(`[C1 the account's magnitude, ${CASE}]`);
const MAIN = P.central({});
const [B0, B1] = CASES[CASE].band;
gate(`the adopted case reproduces ($${B0.toFixed(4)}–${B1.toFixed(4)}bn)`, near(MAIN[0], B0, 1e-4) && near(MAIN[1], B1, 1e-4),
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
// oct07: the payload's block is the 2026 arm's; the 2025 lane's file is the one its previous.oct05 pins (the 2025
// scheduled arm and the positive control below read it).
const PAY25 = ACC.previous ? ACC.previous.oct05 : ACC;
gate(`${PEN_FILE} is the payload's pinned file (${PAY25.source.commit})`, sha256(PEN_FILE) === PAY25.source.sha256);
const PEN = readJson(PEN_FILE);
const m29 = P.payloadModel();
const oasdiOf = (m, alloc) => {
  const cell = (id) => m.receipts.lines.find((l) => l.id === id).cells[REF][alloc].target_bn;
  return sum(ACC.oasdi_lines.map(cell)) + ACC.se_oasdi_share * cell(ACC.se_line);
};
// The scheduled arm: the payload's (sept29, oct05), or on oct07 the scheduled arm on the 2026 inputs, since the payload's
// stays on the 2025 reports while its ratio_net and Part A accrual moved to the 2026 arm.
const SCHED26 = ACC.previous ? readJson("break_conditions_2026_09_29/derived/scheduled_tr2026.json") : null;
if (SCHED26) {
  gate("scheduled_tr2026.json is on this payload's pension block (ratio_net, Part A accrual, the 2025 scheduled arm)",
    SCHED26.case.ratio_net === ACC.ratio_net && SCHED26.case.part_a_accrual_bn === ACC.part_a_accrual_bn
    && SCHED26.case.scheduled_benefits_arm_ratio_net === ACC.scheduled_benefits_arm.ratio_net,
    `scheduled on the 2026 inputs: net ${SCHED26.scheduled_2026.ratio_net.toFixed(6)}, Part A ${SCHED26.scheduled_2026.part_a_bn.toFixed(4)}`);
}
const PA_SCHED25 = PEN.scheduled_arm.decomposition.low.part_a_accrual_bn;
const SCHED = SCHED26 ? { s: SCHED26.scheduled_2026.ratio_net, p: ACC.ratio_net, sa: SCHED26.scheduled_2026.part_a_bn, pa: ACC.part_a_accrual_bn }
  : { s: ACC.scheduled_benefits_arm.ratio_net, p: ACC.ratio_net, sa: PA_SCHED25, pa: ACC.part_a_accrual_bn };
// oct05: the lineage's cell edits (after v4's, before row 8's move) in the set and in the cash set. Its parts carry their
// own accrual per tax dollar, so its Social Security is linSS (k x its OASDI receipts, k its own) and its Part A accrual
// its set Medicare edit less (1 - part_a_share) of its cash one.
const linEdits = (p) => (LIN ? p.edits.slice(p.meta.lineage.edits.first, p.meta.lineage.edits.row8_edit_index) : []);
const LIN_SET = linEdits(payload), LIN_CASH = LIN ? linEdits(PC_.correctionsPayload()) : [];
const prefKeyOf = (id) => MODEL.spending.lines.find((l) => l.id === id).preferred_key;
const linCell = (edits, side, line, a) => sum(edits.filter((e) => e.side === side && e.line === line && !("national_bn" in e)
  && (side === "receipt" ? e.scenario === REF : e.key === prefKeyOf(line))).map((e) => e.by[a]));
// oct07: the applied edit sets (meta.items, after the lineage's edits). Their cell shifts on Social Security and Medicare
// (the pension item's) must sit on the line's preferred key and split exactly into union_* parts, which join the
// union's switch, and lineage_* parts, which join the lineage's own accrual; every other edit is held as it is.
const ITEMS = (payload.meta.items || []).filter((r) => r.applied && r.kind === "edit_set");
const ITEM_FIRST = ITEMS.length ? ITEMS[0].edits.first : payload.edits.length;
const zeroBy = () => Object.fromEntries(P.ALLOCS.map((a) => [a, 0]));
const ITEM_PEN = { union: { social_security: zeroBy(), medicare: zeroBy() }, lineage: { social_security: zeroBy(), medicare: zeroBy() } };
const partsOf = (r, k) => Object.entries(r.parts || {}).filter(([, x]) => x.edit === k);
for (const r of ITEMS) {
  payload.edits.slice(r.edits.first, r.edits.first + r.edits.count).forEach((e, k) => {
    if (e.side !== "spending" || !(e.line in ITEM_PEN.union)) return;
    const parts = partsOf(r, k);
    if ("national_bn" in e || e.key !== prefKeyOf(e.line) || !parts.length || parts.some(([n]) => !/^(union|lineage)_/.test(n))
      || !P.ALLOCS.every((a) => parts.reduce((t, [, x]) => t + x.by[a], 0) === e.by[a])) {
      throw new Error(`[BLOCKED] item ${r.id}: edit ${k} on ${e.line} is not a preferred-key cell shift split exactly into union_/lineage_ parts`);
    }
    for (const [n, x] of parts) for (const a of P.ALLOCS) ITEM_PEN[n.startsWith("union_") ? "union" : "lineage"][e.line][a] += x.by[a];
  });
}
const linOasdi = (a) => sum(ACC.oasdi_lines.map((l) => linCell(LIN_SET, "receipt", l, a))) + ACC.se_oasdi_share * linCell(LIN_SET, "receipt", ACC.se_line, a);
const linSS = (a) => linCell(LIN_SET, "spending", "social_security", a) + ITEM_PEN.lineage.social_security[a];
const linMedSet = (a) => linCell(LIN_SET, "spending", "medicare", a) + ITEM_PEN.lineage.medicare[a];
const linPA = (a) => linMedSet(a) - (1 - ACC.part_a_share) * linCell(LIN_CASH, "spending", "medicare", a);
if (LIN) {
  gate("the lineage's accrual is its own ratio of its OASDI receipts (0.9-1) and its Part A accrual is positive", P.ALLOCS.every((a) =>
    linSS(a) / linOasdi(a) > 0.9 && linSS(a) / linOasdi(a) < 1 && linPA(a) > 0), P.ALLOCS.map((a) =>
    `${a} k ${(linSS(a) / linOasdi(a)).toFixed(4)}, Part A ${linPA(a).toFixed(4)}`).join("; "));
}
// At scheduled benefits: the union's rule on the union's OASDI receipts; the lineage's accrual (on a model that carries
// it) rises in the union's proportion [ASSUMPTION: its parts' ratios move as the union's].
const schedAdd = (m, lineage = Boolean(LIN), v = SCHED) => ENDS.map(([, i]) => {
  const a = MAIN_SPECS[i].allocation;
  if (!lineage) return (v.s - v.p) * oasdiOf(m, a) + (v.sa - v.pa);
  return (v.s - v.p) * (oasdiOf(m, a) - linOasdi(a))
    + (v.s / v.p - 1) * linSS(a)
    + (v.sa - v.pa) * (1 + linPA(a) / v.pa);
});
{
  // Positive control: the same rule on the September 27 payload's receipts gives the pension lane's scheduled less payable
  // (on the 2025 reports, whose values oct07's payload keeps in previous.oct05).
  const m27 = Engine.applyCorrections(MODEL, readJson("main_case_long_run_2026_09_27/derived/corrections.json"));
  const got = schedAdd(m27, false, { s: ACC.scheduled_benefits_arm.ratio_net, p: PAY25.ratio_net, sa: PA_SCHED25, pa: PAY25.part_a_accrual_bn });
  const lane = [PEN.scheduled_arm.case_on_accrual_net_bn.low - PEN.case_on_accrual_net_bn.low,
    PEN.scheduled_arm.case_on_accrual_net_bn.high - PEN.case_on_accrual_net_bn.high];
  gate("the scheduled-benefits rule on the September 27 receipts reproduces the pension lane's scheduled less payable (1e-6)",
    near(got[0], lane[0], 1e-6) && near(got[1], lane[1], 1e-6), `${got.map(f4).join(" / ")} vs ${lane.map(f4).join(" / ")}`);
}
const ADD = {
  care_low: { dir: "down", by: [+CARE.range_dev_low_end_lo, +CARE.range_dev_high_end_lo], src: "components.csv care: low tail of the care and household-services envelope" },
  pension_scheduled: { dir: "up", by: schedAdd(m29), src: `decision 2026-09-29 alternative 3: the accrual at scheduled benefits (net ratio ${SCHED.s.toFixed(4)} for ${SCHED.p.toFixed(4)} on the case's OASDI receipts; Part A ${SCHED.sa.toFixed(2)} for ${SCHED.pa.toFixed(2)}), beside the account`
    + (LIN ? "; the lineage's own accrual raised in the same proportion" : "") + (SCHED26 ? "; the scheduled arm on the 2026 inputs (scheduled_tr2026.py)" : "") },
  defense_gdp_share: { dir: "up", by: [60, 60], src: "groups.py conventions (ladder 253 row): defense bounded by share of GDP, about $60bn (47–72)" },
  medical_mcbs65: { dir: "up", by: [+MED.range_dev_low_end_hi, +MED.range_dev_high_end_hi], src: "components.csv medical: the MCBS 65+ bound" },
};
gate("every additive item is a finite pair", Object.values(ADD).every((a) => a.by.length === 2 && a.by.every(Number.isFinite)),
  Object.entries(ADD).map(([id, a]) => `${id} ${a.by.map(f4).join(" / ")}`).join("; "));
for (const [id, a] of Object.entries(Object.assign({}, ARMS, LISTED))) {
  a.band = centralOf(a.o);
  if (a.want) gate(`${id} reproduces its published row (0.01)`, near(a.band[0], a.want[0], 0.01) && near(a.band[1], a.want[1], 0.01),
    `${a.band[0].toFixed(2)}–${a.band[1].toFixed(2)}`);
}
// The first-year horizon: the September 27 lane's rule (main_case.cjs: long-run lines, rental assistance, capital and the
// enterprise receipt off, CBO's one-year school response), with item 5 at zero (a long-run response) and roads on
// resources; beside it, item 5 kept and the cash set.
const FIRST = { long_run: false, rental: 0, capital: false, enterprise_receipt: 0, school_rule: "one_year", roads: "resources" };
const s27 = readJson("main_case_long_run_2026_09_27/derived/summary.json");
// The rule's positive control runs on the September 29 package (oct05: its base, the lineage off).
const PB = P.BASE || P;
const fyOff = PB.central(Object.assign({}, PB.V4PKG.OFF, FIRST));
gate("the first-year rule with every v4 item off gives the September 27 lane's first_year_response (1e-9)",
  near(fyOff[0], s27.first_year_response[0], 1e-9) && near(fyOff[1], s27.first_year_response[1], 1e-9), `${fyOff[0].toFixed(4)}–${fyOff[1].toFixed(4)}`);
const HORIZON = {
  first_year_horizon: { o: Object.assign({}, FIRST, { property: "none" }), src: "P02 swap: ladder 229's first-year rule on v4, item 5 at zero (a long-run response), roads on resources" },
  first_year_horizon_property_long_run: { o: FIRST, src: "the same, item 5's long-run property response kept" },
  first_year_horizon_cash: { o: Object.assign({}, FIRST, { property: "none", pension4: "cash" }), src: "the same, pensions on cash" },
};
for (const h of Object.values(HORIZON)) h.band = centralOf(h.o);
// oct05: the lineage's alternatives (main_case_lineage_2026_10_05), each the change of its band from the central arm's,
// on the set or, with cash pensions, on the cash set: v5_bands.csv's arms a and c and replacement rows, the C3 line at
// C3 -+ 1 SE (v5_summary.json), and the ancestry-share count of the whole lineage (v5_summary.json fractional) at the
// stated bound's low end, searched, and at its high end and the population lane's convention, listed.
const LINEAGE = {};
const LINEAGE_LISTED = {};
if (LIN) {
  const LL = LIN.lane;
  const vb = readCsv(`${LL}/derived/v5_bands.csv`).filter((r) => r.arm === LIN.arm || r.arm === "a" || r.arm === "c");
  const v5s = readJson(`${LL}/derived/v5_summary.json`);
  const bandOf = (set, arm, variant) => { const r = vb.find((x) => x.set === set && x.arm === arm && x.variant === variant); return [+r.low_bn, +r.high_bn]; };
  const C0 = { set: bandOf("set", LIN.arm, "central"), cash: bandOf("cash", LIN.arm, "central") };
  const CASH_BAND = bandRow("cash_set");
  // oct07: the lineage lane's arms are v5's, so its central is v5's case and cash set (the bands' oct05 rows).
  const V5 = ITEMS.length ? { set: bandRow("oct05_case"), cash: bandRow("oct05_cash_set"), tol: 5e-5, what: "v5's case (5e-5, the bands' four decimals)" }
    : { set: MAIN, cash: CASH_BAND, tol: 5e-6, what: "the case (5e-6, its six decimals)" };
  gate(`the lineage lane's central arm is ${V5.what} and its cash set (5e-5, the bands' four)`,
    C0.set.every((x, j) => near(x, V5.set[j], V5.tol)) && C0.cash.every((x, j) => near(x, V5.cash[j], 5e-5)),
    `${C0.set.map(f4).join("–")}; ${C0.cash.map(f4).join("–")}`);
  const c3At = (set, c3) => ["low", "high"].map((e) => { const l = v5s.sets[set].arms[LIN.arm].c3_line[e]; return l.intercept_bn + l.slope_bn * c3; });
  gate("the C3 line gives the central arm at C3 on both sets (1e-6)", ["set", "cash"].every((s) => c3At(s, LIN.c3.value).every((x, j) => near(x, C0[s][j], 1e-6))));
  const frac = (set, scenario) => { const r = v5s.fractional.rows.find((x) => x.set === set && x.arm === LIN.arm && x.scenario === scenario); return [r.low_bn, r.high_bn]; };
  const delta = (f) => Object.fromEntries(["set", "cash"].map((s) => [s, f(s).map((x, j) => x - C0[s][j])]));
  const C3V = LIN.c3.value, C3SE = LIN.c3.se;
  Object.assign(LINEAGE, {
    lineage_arm_a: { dir: "down", by: delta((s) => bandOf(s, "a", "central")), src: `${LL} v5_bands.csv: arm a, the smaller count (1.81M added)` },
    lineage_c3_plus_1se: { dir: "down", by: delta((s) => c3At(s, C3V + C3SE)), src: `${LL} v5_summary.json c3_line: C3 ${C3V} + 1 SE (${C3SE})` },
    ancestry_share_low: { dir: "down", by: delta((s) => frac(s, "g4_at_nothing")), src: `[FRAMING-SENSITIVE] ${LL} v5_summary.json fractional: the whole lineage counted by ancestry share, the stated bound's low end (G4+ at nothing)` },
    ancestry_share_convention: { dir: "down", by: delta((s) => frac(s, "convention")), src: `[FRAMING-SENSITIVE] ${LL} v5_summary.json fractional: the same count, every third-plus member at the population lane's convention (0.6156), inside the bound` },
    ancestry_share_high: { dir: "down", by: delta((s) => frac(s, "g4_at_bound")), src: `[FRAMING-SENSITIVE] ${LL} v5_summary.json fractional: the same count, the stated bound's high end (G4+ at its measured high bound)` },
    replacement_r1: { dir: "down", by: delta((s) => bandOf(s, LIN.arm, "replacement_r1")), src: `[FRAMING-SENSITIVE] ${LL} v5_bands.csv: net of a native parent's replacement child, r = 1` },
    lineage_arm_c: { dir: "up", by: delta((s) => bandOf(s, "c", "central")), src: `${LL} v5_bands.csv: arm c, the larger count (4.27M added)` },
    lineage_c3_minus_1se: { dir: "up", by: delta((s) => c3At(s, C3V - C3SE)), src: `${LL} v5_summary.json c3_line: C3 ${C3V} - 1 SE (${C3SE})` },
  });
  Object.assign(LINEAGE_LISTED, {
    replacement_r05: { dir: "down", by: delta((s) => bandOf(s, LIN.arm, "replacement_r0.5")), src: `[FRAMING-SENSITIVE] ${LL} v5_bands.csv: replacement child, r = 0.5; dominated by replacement_r1` },
  });
  // oct07: v6 prices the added people at their measured ages, so v5's changes no longer apply. Each alternative with a
  // v6 counterpart takes the case lane's own (summary.json v6.companions: the count's arms a and c, C3 -/+ 1 SE and the
  // ancestry-share count's stated bound), its band's change from the case on the set and from the cash set; the
  // ancestry share at the population lane's convention is the same count on v6's generation costs (the case lane's
  // ancestry_share.cjs rowsFor, run read-only) at the convention's shares. The replacement rows have no v6 counterpart
  // (the frame the operator declined on 2026-10-05): v5's changes carried, not recomputed on v6.
  if (ITEMS.length) {
    const s6 = readJson(`${LANE}/derived/summary.json`), comp = s6.v6.companions, CASH_SET = s6.cash_set.band_bn;
    const minus = (b, c) => b.map((x, j) => x - c[j]);
    for (const [id, name] of [["lineage_arm_a", "arm_a"], ["lineage_arm_c", "arm_c"], ["lineage_c3_plus_1se", "c3_plus_se"],
      ["lineage_c3_minus_1se", "c3_minus_se"]]) {
      const o = comp.options[name];
      gate(`${id}: v6.companions.options.${name} is the case plus its change and main_case_bands.csv's row, on the set and the cash set (1e-9; 5e-5)`,
        o.set.band_bn.every((x, j) => near(x, MAIN[j] + o.set.change_from_the_case_bn[j], 1e-9) && near(x, bandRow(`lineage_${name}`)[j], 5e-5))
        && o.cash.band_bn.every((x, j) => near(x, CASH_SET[j] + o.cash.change_from_the_case_bn[j], 1e-9) && near(x, bandRow(`lineage_${name}_cash_set`)[j], 5e-5)),
        `${o.set.band_bn.map(f4).join("–")}`);
      LINEAGE[id].by = { set: o.set.change_from_the_case_bn.slice(), cash: o.cash.change_from_the_case_bn.slice() };
      LINEAGE[id].src = `${LANE} summary.json v6.companions.options.${name}: ${o.label.replace(/"/g, "'")}`;
    }
    const AS = require(path.join(ROOT, LANE, "ancestry_share.cjs"));
    const SH = readJson(AS.SHARES_FILE).shares;
    const SC = { ancestry_share_low: ["g4_at_nothing", SH.G3plus.bound_low], ancestry_share_high: ["g4_at_bound", SH.G3plus.bound_high],
      ancestry_share_convention: ["convention", SH.G3plus.convention] };
    const by = {};
    for (const which of ["set", "cash"]) {
      const r = AS.rowsFor(P, which, { Engine }), gc = r.generation_costs;
      const count = (g3) => gc.G1.map((x, i) => x + SH.G2.central * gc.G2[i] + g3 * gc.G3plus[i] + SH.added.central * r.added_costs[i]);
      const band = (g3) => { const f = count(g3); return [Math.min(...f), Math.max(...f)]; };
      const base = which === "set" ? MAIN : CASH_SET;
      for (const [id, [scenario, g3]] of Object.entries(SC)) {
        const b = band(g3);
        if (scenario !== "convention") {
          const own = r.rows.find((x) => x.scenario === scenario), kept = comp.ancestry_share[which].rows.find((x) => x.scenario === scenario);
          const row = bandRow(`ancestry_share_${scenario}${which === "cash" ? "_cash_set" : ""}`);
          gate(`${id}, ${which}: the count at its shares is rowsFor's row (1e-9), summary.json v6.companions' (1e-6) and main_case_bands.csv's (5e-5)`,
            b.every((x, j) => near(x, own.band_bn[j], 1e-9) && near(x, kept.band_bn[j], 1e-6) && near(x, row[j], 5e-5)), `${b.map(f4).join("–")}`);
        }
        (by[id] = by[id] || {})[which] = minus(b, base);
      }
    }
    for (const [id, [scenario]] of Object.entries(SC)) {
      LINEAGE[id].by = by[id];
      LINEAGE[id].src = scenario === "convention"
        ? `[FRAMING-SENSITIVE] ${LANE} ancestry_share.cjs rowsFor on v6 (read-only): the whole lineage counted by ancestry share, every third-plus member at the population lane's convention (${SH.G3plus.convention.toFixed(4)}), inside the bound; no v6.companions row`
        : `[FRAMING-SENSITIVE] ${LANE} summary.json v6.companions.ancestry_share: the whole lineage counted by ancestry share, ${scenario === "g4_at_nothing" ? "the stated bound's low end (G4+ at nothing)" : "the stated bound's high end (G4+ at its measured high bound)"}`;
    }
    for (const x of [LINEAGE.replacement_r1, LINEAGE_LISTED.replacement_r05]) x.src += "; v5 delta carried, not recomputed on v6";
  }
  gate("every lineage alternative is a finite pair on both sets, in its direction at the midpoint", Object.values(Object.assign({}, LINEAGE, LINEAGE_LISTED))
    .every((x) => ["set", "cash"].every((s) => x.by[s].every(Number.isFinite) && (x.dir === "down" ? mid(x.by[s]) < 0 : mid(x.by[s]) > 0))));
}
// oct07: the items' arms (summary.json v6.arms; each the whole case with one item at that arm, package.cjs caseOf), each
// the change of its band from the case's on the set or, with cash pensions, from the cash set's; an item the cash set
// does not carry (the pension item's, set only) moves it by 0 [APPROX: additive; at most one arm per item in a
// combination]. Its direction is its set midpoint's.
const ITEM_ALTS = {};
if (ITEMS.length) {
  const s6 = readJson(`${LANE}/derived/summary.json`), v6arms = s6.v6.arms;
  for (const [id, a] of Object.entries(v6arms)) {
    const set = a.change_from_the_case_bn, cash = a.cash ? a.cash.change_from_the_cash_set_bn : [0, 0];
    gate(`item arm ${id}: its band is the case plus its change (1e-9) and main_case_bands.csv's row (5e-5), on both sets`,
      a.band_bn.every((x, j) => near(x, MAIN[j] + set[j], 1e-9) && near(x, bandRow(id)[j], 5e-5))
      && (!a.cash || a.cash.band_bn.every((x, j) => near(x, s6.cash_set.band_bn[j] + cash[j], 1e-9) && near(x, bandRow(`${id}_cash_set`)[j], 5e-5))));
    ITEM_ALTS[id] = { item: a.item, dir: mid(set) < 0 ? "down" : "up", by: { set, cash },
      src: `${LANE} summary.json v6.arms ${id} (item ${a.item}): ${a.label.replace(/"/g, "'")}` };
  }
  gate("every item arm is a finite pair on both sets, the cash set's in its direction or zero",
    Object.values(ITEM_ALTS).every((x) => ["set", "cash"].every((s) => x.by[s].every(Number.isFinite)
      && (x.dir === "down" ? mid(x.by[s]) <= 0 : mid(x.by[s]) >= 0))));
}

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
for (const [id, x] of Object.entries(Object.assign({}, LINEAGE, LINEAGE_LISTED))) {
  const b = [MAIN[0] + x.by.set[0], MAIN[1] + x.by.set[1]];
  armRows.push([id, x.dir, id in LINEAGE_LISTED ? "lineage (listed)" : "lineage", b[0], b[1], mid(b), 100 * (mid(b) / M - 1), `"${x.src}"`]);
}
for (const [id, x] of Object.entries(ITEM_ALTS)) {
  const b = [MAIN[0] + x.by.set[0], MAIN[1] + x.by.set[1]];
  armRows.push([id, x.dir, "item", b[0], b[1], mid(b), 100 * (mid(b) / M - 1), `"${x.src}"`]);
}
outputs[`c1_arms_${CASE}.csv`] = csvText(armRows);

// Every subset of one direction's elements; the engine part is one joint run (cached by its arms), the additive part is
// added, and a lineage alternative (oct05; at most one per subset) adds its change on the set or, with cash pensions, on
// the cash set.
const joint = new Map();
function subsetBand(ids) {
  const o = {};
  const engineIds = ids.filter((id) => ARMS[id]);
  for (const id of engineIds) Object.assign(o, ARMS[id].o);
  const key = engineIds.join("+");
  if (!joint.has(key)) joint.set(key, centralOf(o));
  const b = joint.get(key).slice();
  for (const id of ids) if (ADD[id]) { b[0] += ADD[id].by[0]; b[1] += ADD[id].by[1]; }
  const which = o.pension4 === "cash" ? "cash" : "set";
  for (const id of ids) if (LINEAGE[id]) { b[0] += LINEAGE[id].by[which][0]; b[1] += LINEAGE[id].by[which][1]; }
  for (const id of ids) if (ITEM_ALTS[id]) { b[0] += ITEM_ALTS[id].by[which][0]; b[1] += ITEM_ALTS[id].by[which][1]; }
  return b;
}
const cutRows = [["direction", "set", "size", "cost_low_bn", "cost_high_bn", "midpoint_bn", "move_pct_of_midpoint", "minimal"]];
for (const dir of ["down", "up"]) {
  const lin = Object.keys(LINEAGE).filter((k) => LINEAGE[k].dir === dir);
  const itm = Object.keys(ITEM_ALTS).filter((k) => ITEM_ALTS[k].dir === dir);
  const ids = Object.keys(ARMS).filter((k) => ARMS[k].dir === dir).concat(Object.keys(ADD).filter((k) => ADD[k].dir === dir)).concat(lin).concat(itm);
  const breaks = [];
  for (let mask = 1; mask < 1 << ids.length; mask += 1) {
    const set = ids.filter((_, i) => mask & (1 << i));
    if (set.filter((id) => LINEAGE[id]).length > 1) continue;
    const items = set.filter((id) => ITEM_ALTS[id]).map((id) => ITEM_ALTS[id].item);
    if (new Set(items).size < items.length) continue;
    const b = subsetBand(set);
    const crosses = dir === "down" ? mid(b) < LOW_CUT : mid(b) > HIGH_CUT;
    if (crosses) breaks.push({ set, b });
  }
  const minimal = breaks.filter((x) => !breaks.some((y) => y !== x && y.set.length < x.set.length && y.set.every((s) => x.set.includes(s))));
  minimal.sort((x, y) => x.set.length - y.set.length || x.set.join("+").localeCompare(y.set.join("+")));
  for (const x of minimal) cutRows.push([dir, x.set.join("+"), x.set.length, x.b[0], x.b[1], mid(x.b), 100 * (mid(x.b) / M - 1), "yes"]);
  // The stack: every engine and additive alternative (oct07: and each item's arm that moves the set most); then (oct05)
  // with the lineage alternative that moves the set most.
  const pick = lin.length ? [lin.reduce((p, q) => (Math.abs(mid(LINEAGE[q].by.set)) > Math.abs(mid(LINEAGE[p].by.set)) ? q : p))] : [];
  const most = {};
  for (const id of itm) {
    const k = ITEM_ALTS[id].item;
    if (!most[k] || Math.abs(mid(ITEM_ALTS[id].by.set)) > Math.abs(mid(ITEM_ALTS[most[k]].by.set))) most[k] = id;
  }
  const base = ids.filter((id) => !LINEAGE[id] && (!ITEM_ALTS[id] || most[ITEM_ALTS[id].item] === id));
  for (const stack of pick.length ? [base, base.concat(pick)] : [base]) {
    const all = subsetBand(stack);
    cutRows.push([dir, "ALL:" + stack.join("+"), stack.length, all[0], all[1], mid(all), 100 * (mid(all) / M - 1), "stack"]);
  }
}
outputs[`c1_min_cuts_${CASE}.csv`] = csvText(cutRows);
console.log(`  thresholds: midpoint ${M.toFixed(2)}, a quarter down ${LOW_CUT.toFixed(2)}, up ${HIGH_CUT.toFixed(2)}`);

// ------------------------------------------------------------------------------------------------ C2 and C3
console.log(`[C2 taxes against benefits; C3 corrections by side, ${CASE}]`);
const p27 = readJson("main_case_long_run_2026_09_27/derived/corrections.json");
const N27 = p27.edits.length;
gate(`v4's payload opens with the September 27 payload's ${N27} edits, unchanged`,
  payload.edits.slice(0, N27).every((e, k) => JSON.stringify(e) === JSON.stringify(p27.edits[k])), `${payload.edits.length} edits in all`);
// oct05: the lineage's edits (its cells, then row 8's move) close the payload and are held in every run, after v4's items.
const LIN_FIRST = LIN ? LIN.edits.first : payload.edits.length;
if (LIN) gate(ITEMS.length ? "the lineage's edits come before the items', row 8's move last, and the items' edits close the payload in order"
  : "the lineage's edits close the payload, row 8's move last", LIN.edits.first + LIN.edits.count === ITEM_FIRST
  && LIN.edits.row8_edit_index === ITEM_FIRST - 1 && ITEMS.every((r, k) => r.edits.first === (k ? ITEMS[k - 1].edits.first + ITEMS[k - 1].edits.count : ITEM_FIRST))
  && (ITEMS.length ? ITEMS[ITEMS.length - 1].edits.first + ITEMS[ITEMS.length - 1].edits.count : ITEM_FIRST) === payload.edits.length);
const DATASET = payload.edits.slice(0, N27), TAIL = payload.edits.slice(N27, LIN_FIRST), LINT = payload.edits.slice(LIN_FIRST);
gate("the dataset corrections have only receipt and spending edits", DATASET.every((e) => (e.side === "receipt" || e.side === "spending") && e.by));
// v4's items with a subset of the dataset corrections, in the payload's order (the tail's national-scale edits scale the
// dataset edits on their lines, as in the case).
const withDataset = (keep) => Engine.applyCorrections(MODEL, { lines: payload.lines, receipt_lines: payload.receipt_lines,
  production: payload.production, edits: DATASET.filter(keep).concat(TAIL).concat(LINT), meta: payload.meta });
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
// oct07: the union's Medicare switch is the tail's edit plus the edit sets' union_* parts on Medicare.
const tailMed = (a) => TAIL_MED[0].by[a] + ITEM_PEN.union.medicare[a];
// oct05: the switch is rebuilt on the union's part; the lineage keeps its own accrual (its edits, held).
function pensionRebuilt(m) {
  const by = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
  const ss = by((a) => (LIN ? ACC.ratio_net * (oasdiOf(m, a) - linOasdi(a)) + linSS(a) : ACC.ratio_net * oasdiOf(m, a))
    - benefit(m, "social_security", a));
  const med = by((a) => {
    if (LIN) {
      const own = linMedSet(a);
      const preU = benefit(m, "medicare", a) - tailMed(a) - own;
      return (1 - ACC.part_a_share) * preU + ACC.part_a_accrual_bn + own - benefit(m, "medicare", a);
    }
    const pre = benefit(m, "medicare", a) - tailMed(a);
    return (1 - ACC.part_a_share) * pre + ACC.part_a_accrual_bn - benefit(m, "medicare", a);
  });
  const edits = [{ side: "spending", line: "social_security", key: TAIL_SS[0].key, by: ss }, { side: "spending", line: "medicare", key: TAIL_MED[0].key, by: med }];
  return { m: Engine.applyCorrections(m, { lines: [], receipt_lines: [], edits }), shift: [ss, med] };
}
const R = { base: pensionRebuilt(mBase), rec: pensionRebuilt(mRec), sp: pensionRebuilt(mSp), all: pensionRebuilt(mAll) };
gate("rebuilt on the full payload, the pension switch moves nothing (1e-9)", R.all.shift.every((x) => ALLOCS.every((a) => Math.abs(x[a]) < 1e-9)));
const cashPayload = readJson(CASES[CASE].cash);
if (PC_) gate(`the cash package's payload is ${CASES[CASE].cash}`, JSON.stringify(PC_.correctionsPayload()) === JSON.stringify(cashPayload));
const PC = PC_ || P.forPayload(cashPayload);
const mCash = PC.payloadModel();
const CASH = ENDS.map(([, i]) => PC.evaluateFull(mCash, PC.MAIN_SPECS[i]).cost_bn);
gate("the cash payload is the cash set at both ends (main_case_bands.csv cash_set, 1e-4)", CASH.every((x, j) => near(x, bandRow("cash_set")[j], 1e-4)),
  `${CASH[0].toFixed(4)}–${CASH[1].toFixed(4)}`);
// The tally at scheduled benefits moves by the scheduled rule on each model's own OASDI receipts.
// oct05 adds the union alone at the case's responses (v4's payload with row 8's move): the case less it is the lineage's.
const tallyRows = [["model", "end", "spec", "direct_receipts_bn", "household_transfers_bn", "tally_bn", "scheduled_move_bn", "tally_at_scheduled_bn"]];
const tallyModels = [["case_accrual", P, m29, true], ["cash_set", PC, mCash, false],
  ["v4_items_without_dataset_corrections", P, R.base.m, true], ["v4_items_without_dataset_corrections_increments_held", P, mBase, true],
  ["uncorrected_no_v4_items", P, MODEL, false]];
// oct07: the union also takes each applied edit set's union part, by engine_lines.cjs's rule (national-scale edits as they
// are; every edit of an item whose record states its edits are all the union's (union_only), as it is, its parts adding
// to it; other cell shifts at their union_* parts), and a union-only item's carrier receipt lines as the payload has them.
const itemUnion = () => ITEMS.flatMap((r) => payload.edits.slice(r.edits.first, r.edits.first + r.edits.count).map((e, k) => {
  if ("national_bn" in e) return e;
  const parts = partsOf(r, k);
  if (r.union_only) {
    if (parts.length && !ALLOCS.every((a) => parts.reduce((t, [, x]) => t + x.by[a], 0) === e.by[a])) {
      throw new Error(`[BLOCKED] item ${r.id}: the parts of edit ${k} do not add to it`);
    }
    return e;
  }
  if (!parts.length) throw new Error(`[BLOCKED] item ${r.id}: cell shift ${k} names no parts and the item is not union_only`);
  if (parts.some(([n]) => !/^(union|lineage)_/.test(n))) throw new Error(`[BLOCKED] item ${r.id}: parts neither union_* nor lineage_*`);
  return Object.assign({}, e, { by: Object.fromEntries(ALLOCS.map((a) => [a, parts.filter(([n]) => n.startsWith("union_")).reduce((t, [, x]) => t + x.by[a], 0)])) });
}));
const itemCarriers = () => ITEMS.flatMap((r) => {
  const ids = (r.capital && r.capital.receipt_lines) || [];
  if (ids.length && !r.union_only) throw new Error(`[BLOCKED] item ${r.id}: carrier receipt lines on an item that is not union_only`);
  return ids.map((id) => {
    const l = (payload.receipt_lines || []).filter((x) => x.id === id);
    if (l.length !== 1) throw new Error(`[BLOCKED] item ${r.id}: carrier ${id} is not one receipt line of the payload`);
    return l[0];
  });
});
if (LIN) {
  const mU = Engine.applyCorrections(P.SEPT29.payloadModel(), { lines: [], receipt_lines: itemCarriers(), edits: [payload.edits[LIN.edits.row8_edit_index]].concat(itemUnion()) });
  tallyModels.push(["union_at_case_responses", P, mU, "union"]);
}
for (const [lab, pkg, m, accrual] of tallyModels) {
  const sched = accrual ? schedAdd(m, accrual === true && Boolean(LIN)) : null;
  ENDS.forEach(([end, i], j) => {
    const ev = pkg.evaluateFull(m, pkg.MAIN_SPECS[i]).evaluation;
    const rec = ev.classes.direct_receipts.responsive_bn, tr = ev.classes.household_transfer.responsive_bn;
    tallyRows.push([lab, end, i, rec, tr, rec - tr, accrual ? sched[j] : "", accrual ? rec - tr - sched[j] : ""]);
  });
}
if (LIN) {
  // The tally at the lineage lane's arms a, b and c from its per-line costs at the arm's responses and ends
  // (lineage_lines.csv v5_bn: v4's line, the union's response move and the added people's parts), classed as the case's
  // evaluation classes each line at that end. Arm b's must be the case's tally (1e-4: the file's six decimals).
  // oct07: the lane's lines are v5's, so arm b's must be v5's tally, and arms a and c move by the case's change from v5.
  const LLINES = readCsv(`${LIN.lane}/derived/lineage_lines.csv`).filter((r) => r.set === "set");
  const V5P = ITEMS.length ? P.OCT05 : P, m5 = ITEMS.length ? V5P.payloadModel() : m29;
  for (const arm of ["a", LIN.arm, "c"]) {
    ENDS.forEach(([end, i], j) => {
      const ev = V5P.evaluateFull(m5, V5P.MAIN_SPECS[i]).evaluation;
      const direct = new Set(ev.receipts.filter((r) => r.group === "direct_receipts").map((r) => "receipt|" + r.id));
      const transfer = new Set(ev.spending.filter((r) => r.response_class === "household_transfer").map((r) => "spending|" + r.id));
      const lines = LLINES.filter((r) => r.arm === arm && r.end === ["low", "high"][j]);
      if (!lines.length || lines.some((r) => +r.spec !== i)) throw new Error(`[BLOCKED] lineage_lines.csv: arm ${arm} at ${end} is not specification ${i}`);
      const rec = -sum(lines.filter((r) => direct.has(r.item)).map((r) => +r.v5_bn));
      const tr = sum(lines.filter((r) => transfer.has(r.item)).map((r) => +r.v5_bn));
      const t = tallyRows.find((r) => r[0] === "case_accrual" && r[1] === end);
      const want = ITEMS.length ? [ev.classes.direct_receipts.responsive_bn, ev.classes.household_transfer.responsive_bn] : [t[3], t[4]];
      if (arm === LIN.arm) {
        gate(`lineage_lines.csv's arm ${arm} gives ${ITEMS.length ? "v5's" : "the case's"} tally at ${end} (1e-4)`, near(rec, want[0], 1e-4) && near(tr, want[1], 1e-4),
          `${f4(rec)} - ${f4(tr)} vs ${f4(want[0])} - ${f4(want[1])}`);
      } else if (ITEMS.length) {
        const dr = t[3] - want[0], dt = t[4] - want[1];
        tallyRows.push([`lineage_arm_${arm}`, end, i, rec + dr, tr + dt, rec + dr - (tr + dt), "", ""]);
      } else {
        tallyRows.push([`lineage_arm_${arm}`, end, i, rec, tr, rec - tr, "", ""]);
      }
    });
  }
}
outputs[`c2_tally_${CASE}.csv`] = csvText(tallyRows);

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
        near(be[0], +want[`${CASE}_low`], 1e-4) && near(be[1], +want[`${CASE}_high`], 1e-4), `${(100 * be[0]).toFixed(2)}% to ${(100 * be[1]).toFixed(2)}%`);
    }
    beRows.push([lab, variant, a, be[0], be[1]]);
  }
}
outputs[`c2_break_even_${CASE}.csv`] = csvText(beRows);

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
outputs[`c3_correction_split_${CASE}.csv`] = csvText(splitRows);

// ------------------------------------------------------------------------------------------------ C6
console.log(`[C6 generations on the ${CASE} payloads]`);
const GEN = "generation_account_2026_09_24/derived";
const genRows = [["case", "convention", "generation", "cost_low_end_bn", "cost_high_end_bn", "break_even_personal_most", "break_even_personal_least",
  "break_even_shared_most", "break_even_shared_least"]];
const genHashes = [["file", "sha256"]];
for (const [lab, pkg, file, results] of [["case_accrual", P, `generation_corrections_${CASE}.json`, `generation_results_${CASE}.csv`],
  ["cash_set", PC, `generation_corrections_${CASE}_cash.json`, `generation_results_${CASE}_cash.csv`]]) {
  const missing = [file, results].filter((f) => !fs.existsSync(path.join(ROOT, GEN, f)));
  if (missing.length) {      // the generation account's split of this case is not built yet: stop, write nothing
    gate(`${lab}: the generation account's ${missing.join(" and ")} exist`, false);
    continue;
  }
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
outputs[`c6_generation_break_even_${CASE}.csv`] = csvText(genRows);
outputs[`c6_inputs_${CASE}.csv`] = genHashes.map((r) => r.join(",")).join("\n") + "\n";

if (failures) {
  console.error(`[BLOCKED] ${failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
for (const [name, text] of Object.entries(outputs)) fs.writeFileSync(path.join(OUT, name), text);
console.log("\n[written] " + Object.keys(outputs).join(", "));
for (const name of ["c1_min_cuts", "c2_tally", "c2_break_even", "c3_correction_split", "c6_generation_break_even"]) {
  console.log(fs.readFileSync(path.join(OUT, `${name}_${CASE}.csv`), "utf8"));
}
