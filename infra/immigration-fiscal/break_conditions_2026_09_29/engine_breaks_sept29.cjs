/* Break conditions on live v9 by default (--case oct16); explicit historical --case modes retain their old computations.
 * Original v4 route (main_case_2026_09_29, key sept29): the engine computations
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
 * Historical reproduction: node engine_breaks_sept29.cjs --case sept29 -> derived/c1_arms_sept29.csv, c1_min_cuts_sept29.csv,
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
 *
 * Historical --case oct14 computes v7. Its personal ends come from summary.json v7.end_specifications;
 * its item edits and receipt responses travel through the package. Historical --case options are explicit reproductions.
 * C2's lineage-arm tallies now run the case's own option payloads at those ends, rather than carry v5's shared-end tally.
 * --case oct15 (default) uses v8's whole case and independently found personal ends. Reporter carriers copy their
 * source parents' keys/responses/classes; native child production/cells remain in the full payload. Mixed-unit and
 * coverage amounts enter after engine/capital, scoped by generation for C6. C2's direct tally excludes their
 * undeclared class split explicitly; its service break-even includes the full net costs.
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
  oct14: { lane: "main_case_2026_10_14", cash: "main_case_2026_10_14/derived/corrections_cash.json" },
  oct15: { lane: "main_case_2026_10_15", cash: "main_case_2026_10_15/derived/corrections_cash.json" },
  oct16: { lane: "main_case_2026_10_16", cash: "main_case_2026_10_16/derived/corrections_cash.json" },
};
const CASE_ARG = process.argv.indexOf("--case");
const CASE = CASE_ARG > 0 ? process.argv[CASE_ARG + 1] : "oct16";
const V8PLUS = CASE === "oct15" || CASE === "oct16";
const LIVE_PERSONAL = CASE === "oct14" || V8PLUS;
// C1's exact minimal-crossing search is complete on the historical cases (oct15: 15 and 14 groups, 648,000
// evaluations). v9's item arms make 22 downward groups: on 2026-10-20 sizes 1-7 took 82.7M evaluations and
// 203,729 minimal crossings, about five times more per size. On oct16 the search is therefore complete through
// --c1-max-size arms (default 5) and lists no larger minimal crossings [SCOPE]; historical cases stay unbounded.
const C1_MAX_ARG=process.argv.indexOf("--c1-max-size");
const C1_MAX_SIZE=C1_MAX_ARG>0?Number(process.argv[C1_MAX_ARG+1]):CASE==="oct16"?5:Infinity;
if(!(C1_MAX_SIZE>=1))throw Error("[BLOCKED] --c1-max-size must be at least 1");
const C2_POSTENGINE_CLASS_RULE=process.env.C2_POSTENGINE_CLASS_RULE||"exclude_unclassified";
if(!["exclude_unclassified","stop"].includes(C2_POSTENGINE_CLASS_RULE))throw Error(`[BLOCKED] unknown C2_POSTENGINE_CLASS_RULE ${C2_POSTENGINE_CLASS_RULE}`);
if (!CASES[CASE]) throw new Error(`[BLOCKED] --case ${CASE}: not one of ${Object.keys(CASES).join(", ")}`);
const LANE = CASES[CASE].lane;
// Source metadata is enough to reject stale generations before loading the
// pricing package; full numerical closure remains checked below after loading.
let generationSourceReproduced=false;
if(CASE==="oct16"){
  const contractFile=path.join(__dirname,"derived/generation_source_contract_oct16.json");
  if(!fs.existsSync(contractFile))throw Error("[BLOCKED] final generation source replay absent; run reproduce_generation_source.cjs");
  generationSourceReproduced=require("./generation_preflight.cjs").validateReproducedSource(JSON.parse(fs.readFileSync(contractFile,"utf8")),ROOT);
  const saved=JSON.parse(fs.readFileSync(path.join(ROOT,LANE,"derived/corrections.json"),"utf8"));
  const live=JSON.parse(fs.readFileSync(path.join(ROOT,"live_case.json"),"utf8"));
  if(live.key!==CASE||live.lane!==LANE||!live.adopted||saved.meta.adopted!==live.adopted||
      !saved.meta.status?.startsWith("adopted: main case v9"))
    throw Error("[BLOCKED] oct16 source payload is not the authoritative adopted live case");
  for(const suffix of ["","_cash"]){
    const file=path.join(ROOT,"generation_account_2026_09_24/derived",`generation_corrections_${CASE}${suffix}.json`);
    if(!fs.existsSync(file))throw Error(`[BLOCKED] ${file} absent; run final generation account first`);
    require("./generation_preflight.cjs").validateGenerationPayloads(JSON.parse(fs.readFileSync(file,"utf8")).payloads,suffix?JSON.parse(fs.readFileSync(path.join(ROOT,LANE,"derived/corrections_cash.json"),"utf8")).meta:saved.meta,CASE,generationSourceReproduced);
  }
}
// oct16 runs the case's canonical cached route. Its uncached bounded route (V9_CASE_CACHE=0) builds a payload whose
// item 13 part metadata differs from derived/corrections.json (2026-10-21; costs equal), so the payload-identity
// gate below rejects it; memory is held instead by pricing the item arms in bounded children (item_arm_prices.cjs).
if(CASE==="oct16"&&process.env.V9_CASE_CACHE==="0")throw Error("[BLOCKED] oct16 needs the canonical cached case route; unset V9_CASE_CACHE");
const P = require(path.join(ROOT, LANE, "package.cjs"));
const LIN = CASE === "sept29" ? null : P.correctionsPayload().meta.lineage;   // oct05: the lineage's meta
if (CASE !== "sept29" && !(LIN && P.CASH)) throw new Error(`[BLOCKED] ${LANE}: no lineage or no cash package`);
const PC_ = LIN ? P.CASH : null;             // the cash set's package where the case's package runs one pension switch only
// An option set's band: a pension switch other than the case's runs on the cash set's package (oct05).
const stable = x => Array.isArray(x) ? x.map(stable) : x && typeof x === "object"
  ? Object.fromEntries(Object.keys(x).sort().map(k=>[k,stable(x[k])])) : x;
const optionBands=new Map();
const ratePackages=new Map();
// oct15 (round 3, R3-05): the shared allocation and the within-district school reading price items 11 and 12 under
// their own rules, as main_case.cjs prices those companions (companions.cjs adjustedRun).
const companionRule = (o) => !V8PLUS ? null : o.allocation === "shared" ? "shared" : o.school_rule === "within_district" ? "school" : null;
function companionBand(X, o, rule) {
  const COMP = require(path.join(ROOT, LANE, "companions.cjs")), specs = X.specsFor(o);
  const bands = P.METHODS.map((method) => {
    const m = X.modelFor("central", method, X.withCentral(o)), costs = specs.map((s) => COMP.adjustedRun(X, m, s, rule).cost_bn);
    return [Math.min(...costs), Math.max(...costs)];
  });
  return [0, 1].map((e) => bands.reduce((t, b) => t + b[e], 0) / bands.length);
}
function centralOf(o) {
  const cash=PC_&&o.pension4==="cash";
  if(CASE==="oct16"&&o.one_rate_arm&&!ratePackages.has(o.one_rate_arm))ratePackages.set(o.one_rate_arm,P.caseOf(P.OCT05,P.CANDIDATE,{one_rate:o.one_rate_arm}));
  const Q=CASE==="oct16"&&o.one_rate_arm?ratePackages.get(o.one_rate_arm):P,X=cash?Q.CASH:Q;
  const options=Object.fromEntries(Object.entries(o).filter(([k])=>k!=="one_rate_arm"&&(!cash||k!=="pension4")));
  const key=JSON.stringify([cash?"cash":"set",o.one_rate_arm||null,stable(X.withCentral(options))]);
  if(!optionBands.has(key)){const rule=companionRule(options);optionBands.set(key,rule?companionBand(X,options,rule):X.central(options));}
  return optionBands.get(key).slice();
}
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
const SUMMARY = readJson(`${LANE}/derived/summary.json`);
const VERSION = CASE === "oct16" ? "v9" : CASE === "oct15" ? "v8" : CASE === "oct14" ? "v7" : "v6";
const endSet = V8PLUS ? SUMMARY[VERSION].end_specifications.set[0] : SUMMARY[VERSION].end_specifications?.set;
const endCash = V8PLUS ? SUMMARY[VERSION].end_specifications.cash[0] : SUMMARY[VERSION].end_specifications?.cash;
const endNumbers = LIVE_PERSONAL ? endSet : [48, 11];
if (LIVE_PERSONAL && (!Array.isArray(endNumbers) || endNumbers.length !== 2 || !endNumbers.every(Number.isInteger))) {
  throw new Error(`[BLOCKED] ${CASE}: missing or invalid personal end specifications`);
}
if (V8PLUS && ["set", "cash"].some(b =>
  SUMMARY[VERSION].end_specifications[b].some(xs => JSON.stringify(xs) !== JSON.stringify(endNumbers)))) {
  throw new Error(`[BLOCKED] ${CASE}: method end specifications differ; the tally rule needs revision`);
}
if (LIVE_PERSONAL && JSON.stringify(endNumbers) !== JSON.stringify(endCash)) {
  throw new Error(`[BLOCKED] ${CASE}: set and cash ends differ; the shared tally end rule needs revision`);
}
const ENDS = [[`low_end_${endNumbers[0]}`, endNumbers[0]], [`high_end_${endNumbers[1]}`, endNumbers[1]]];
for (const [, i] of ENDS) {
  if (!MAIN_SPECS[i] || (LIVE_PERSONAL && MAIN_SPECS[i].allocation !== "personal")) {
    throw new Error(`[BLOCKED] ${CASE}: end specification ${i} absent or not personal`);
  }
}
if(CASE==="oct16")for(const [basis,pkg]of [["set",P],["cash",PC_]])for(const [k,method]of P.METHODS.entries()){
  const m=pkg.modelFor("central",method,pkg.withCentral({})),ss=pkg.specsFor({}),values=ss.map(s=>pkg.evaluateFull(m,s).cost_bn);
  const found=[values.indexOf(Math.min(...values)),values.indexOf(Math.max(...values))];
  if(JSON.stringify(found)!==JSON.stringify(SUMMARY.v9.end_specifications[basis][k]))throw Error(`[BLOCKED] oct16 ${basis}/${method}: re-searched ends ${found} disagree with final summary`);
}
if (process.argv.includes("--probe-only")) {
  console.log(`[probe] ${CASE}: ${MAIN_SPECS.length} specifications; ends ${endNumbers.join(" / ")}`);
  process.exit(0);
}
// Reject candidate/coverage-off generation files before the expensive C1 search.
const generationPreflightHashes=new Map();
if(V8PLUS)for(const [pkg,suffix]of [[P,""],[PC_,"_cash"]]) {
  const dir="generation_account_2026_09_24/derived",file=`${dir}/generation_corrections_${CASE}${suffix}.json`;
  const results=`${dir}/generation_results_${CASE}${suffix}.csv`;
  for(const rel of [file,results])if(!fs.existsSync(path.join(ROOT,rel)))throw Error(`[BLOCKED] ${rel} absent; run final generation account first`);
  require("./generation_preflight.cjs").validateGenerationPayloads(readJson(file).payloads,pkg.correctionsPayload().meta,CASE,generationSourceReproduced);
  for(const rel of [file,results])generationPreflightHashes.set(rel,sha256(rel));
}

// ------------------------------------------------------------------------------------------------ C1
console.log(`[C1 the account's magnitude, ${CASE}]`);
const MAIN = centralOf({});
const adopted = readCsv(`${LANE}/derived/main_case_bands.csv`).find((r) => r.profile === P.MAIN_PROFILE && r.variant === "adopted");
const [B0, B1] = CASES[CASE].band || [+adopted.cost_low_bn, +adopted.cost_high_bn];
gate(`the adopted case reproduces ($${B0.toFixed(4)}–${B1.toFixed(4)}bn)`, near(MAIN[0], B0, 1e-4) && near(MAIN[1], B1, 1e-4),
  `${MAIN[0].toFixed(4)}–${MAIN[1].toFixed(4)}`);
if (LIVE_PERSONAL) gate(`the live band equals summary.json ${VERSION}.band_bn (1e-9)`,
  MAIN.every((x, j) => near(x, SUMMARY[VERSION].band_bn[j], 1e-9)));
const M = mid(MAIN);
const LOW_CUT = 0.75 * M, HIGH_CUT = 1.25 * M;
const bands = readCsv(`${LANE}/derived/main_case_bands.csv`).filter((r) => r.profile === P.MAIN_PROFILE);
const bandRow = (v) => {
  const r = bands.find((x) => x.variant === v);
  if (!r) throw new Error(`[BLOCKED] ${LANE}/derived/main_case_bands.csv: no ${v} row`);
  return [+r.cost_low_bn, +r.cost_high_bn];
};
const currentBandRow=v=>CASE==="oct16"&&SUMMARY.v9.historical_rows.includes(P.MAIN_PROFILE+"/"+v)?null:bandRow(v);
const comps = readCsv(`${LANE}/derived/components.csv`);
const comp = (id) => comps.find((r) => r.component === id);
const PROP = comp("property_long_run"), CARE = comp("care"), MED = comp("medical");

// A long-run variant the package cannot run with v4's items (the miles key needs the long-run subfunction responses) is
// listed as blocked, not searched.
const LR_KEYS = Object.keys(P.LONG_RUN_VARIANTS).filter((k) => k !== "adopted");
const lrBlocked = [];
const lrBands = LR_KEYS.flatMap((k) => {
  try { return [[k, centralOf({ long_run: k })]]; } catch (e) { lrBlocked.push([k, e.message.split("\n")[0]]); return []; }
});
const lrMax = lrBands.reduce((a, b) => (mid(b[1]) > mid(a[1]) ? b : a));
// Engine arms: each is the alternative end of a range the case reports (main_case_bands.csv or components.csv), or an
// item of v4 turned off.
const ARMS = {
  capital_off: { dir: "down", o: { capital: false }, src: "ladder 239: no return on public capital (a convention; old band row historical on v9; inherited fixed count/coverage amounts held)", want: currentBandRow("without_capital_return") },
  school_within_district: { dir: "down", o: { school_rule: "within_district" }, src: "ladder 230/239: schools at the within-district 0.836 read over the removal", want: bandRow("school_within_district") },
  roads_parks_first_year: { dir: "down", o: { long_run: false, roads: "resources" }, src: "ladder 237: roads and parks at CBO's first-year response 0; v4's miles key needs the long-run subfunction responses, so roads are on resources here", want: null },
  enterprises_out: { dir: "down", o: { enterprises: "A" }, src: "ladder 239: government enterprises out (option A)", want: currentBandRow("enterprises_out_option_a") },
  rental_zero: { dir: "down", o: { rental: 0 }, src: "ladder 239: rental assistance at response 0", want: currentBandRow("rental_assistance_at_0") },
  pension_cash: { dir: "down", o: { pension4: "cash" }, src: "decision 2026-09-29 alternative 2: the cash set, Social Security and Medicare counted when paid (the September 27 convention)", want: bandRow("cash_set") },
  property_high_reading: { dir: "down", o: { property_reading: "high" }, src: "components.csv property_long_run: the receipt-side lane's responses at 1 everywhere, case-scaled tenant national", want: [MAIN[0] + +PROP.range_dev_low_end_lo, MAIN[1] + +PROP.range_dev_high_end_lo] },
  capital_7pct: { dir: "up", ...(CASE==="oct16"?{item:"one_rate"}:{}), o: CASE==="oct16"?{one_rate_arm:"capital_7pct"}:{ rates: { low: RATES.reported, high: RATES.reported } }, src: "ladder 238/239: capital at a private 7% return; v9 uses the declared one_rate capital_7pct arm (beside the account)", want: CASE==="oct16"?bandRow("one_rate_capital_7pct"):bandRow("capital_return_at_7pct") },
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
// R9 keeps meta.pension_accrual on published weights. Its row-4 union pension shifts stay fixed in every C3 subset.
const ROW4_UNION_PEN = { social_security: zeroBy(), medicare: zeroBy() };
const partsOf = (r, k) => Object.entries(r.parts || {}).filter(([, x]) => x.edit === k);
for (const r of ITEMS) {
  payload.edits.slice(r.edits.first, r.edits.first + r.edits.count).forEach((e, k) => {
    if (e.side !== "spending" || !(e.line in ITEM_PEN.union)) return;
    const parts = partsOf(r, k);
    if (V8PLUS && r.id === "union_completion") {
      const original=MODEL.spending.lines.find(l=>l.id===e.line);
      if (!(e.key in original.keys) || !parts.length || parts.some(([n])=>!n.startsWith("lineage_")) || !P.ALLOCS.every(a=>near(sum(parts.map(([,p])=>p.by[a])),e.by[a],1e-9))) {
        throw Error(`[BLOCKED] completion pension part ${k} lacks its own key/lineage declaration`);
      }
      return; // fixed keyed completion parts survive every dataset subset; not a new pension-switch ratio
    }
    if ("national_bn" in e || e.key !== prefKeyOf(e.line) || !parts.length || parts.some(([n]) => !/^(union|lineage)_/.test(n))
      || !P.ALLOCS.every((a) => parts.reduce((t, [, x]) => t + x.by[a], 0) === e.by[a])) {
      throw new Error(`[BLOCKED] item ${r.id}: edit ${k} on ${e.line} is not a preferred-key cell shift split exactly into union_/lineage_ parts`);
    }
    for (const [n, x] of parts) for (const a of P.ALLOCS) {
      ITEM_PEN[n.startsWith("union_") ? "union" : "lineage"][e.line][a] += x.by[a];
      if (r.id === "row4_frame" && n.startsWith("union_")) ROW4_UNION_PEN[e.line][a] += x.by[a];
    }
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
const schedAdd = (m, lineage = Boolean(LIN), v = SCHED, allocations = ENDS.map(([, i]) => MAIN_SPECS[i].allocation)) => allocations.map((a) => {
  if (!lineage) return (v.s - v.p) * oasdiOf(m, a) + (v.sa - v.pa);
  return (v.s - v.p) * (oasdiOf(m, a) - linOasdi(a))
    + (v.s / v.p - 1) * linSS(a)
    + (v.sa - v.pa) * (1 + linPA(a) / v.pa);
});
{
  // Positive control: the same rule on the September 27 payload's receipts gives the pension lane's scheduled less payable
  // (on the 2025 reports, whose values oct07's payload keeps in previous.oct05).
  const m27 = Engine.applyCorrections(MODEL, readJson("main_case_long_run_2026_09_27/derived/corrections.json"));
  const got = schedAdd(m27, false, { s: ACC.scheduled_benefits_arm.ratio_net, p: PAY25.ratio_net, sa: PA_SCHED25, pa: PAY25.part_a_accrual_bn }, ["shared", "personal"]);
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
const publishedCrossChecks={engine_arms_checked:[],engine_arms_without_published_row:[],item_arms_checked:[],item_arms_without_current_row:[],
  rule:"an arm is cross-checked against a current published case row (engine 0.01, item 5e-5). Rows the case lists in summary.json v9.historical_rows are not republished on v9, and some engine arms never had a row; those arms are priced by the case package here, item arms keep the case-plus-change 1e-9 identity, and no published cross-check exists for them"};
for (const [id, a] of Object.entries(Object.assign({}, ARMS, LISTED))) {
  a.band = centralOf(a.o);
  if(CASE==="oct16"&&Object.hasOwn(a,"want"))publishedCrossChecks[a.want?"engine_arms_checked":"engine_arms_without_published_row"].push(id);
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
if(!V8PLUS)for (const h of Object.values(HORIZON)) h.band = centralOf(h.o);
if (CASE === "oct16") {
  const FY9=require("./first_year_v9.cjs"), report=FY9.run(P,MAIN,gate);
  for(const [basis,name]of [["set","first_year_horizon"],["cash","first_year_horizon_cash"]]) {
    HORIZON[name].band=report.variants.fixed_capital[basis];
    HORIZON[name].src+="; canonical v9 firstYear; item13 off, item21 on; source-line coverage/count repricing; ends independently searched";
  }
  HORIZON.first_year_horizon_property_long_run.band=FY9.band(P,"set","fixed_capital",{...FIRST,item6_first_year:true});
  outputs["first_year_item6_oct16.json"]=JSON.stringify(report,null,2)+"\n";
}
if (CASE === "oct15") {
  const FY8 = require("./first_year_v8.cjs"), report = FY8.run(P, MAIN, gate);
  for (const [basis, name] of [["set", "first_year_horizon"], ["cash", "first_year_horizon_cash"]]) {
    HORIZON[name].band = report.variants.fixed_capital[basis];
    HORIZON[name].src += "; item9 with item6 fixed-capital multiplier; item10 parent responses and option endpoint prices; item11 without its owner property; item12 at its source lines' first-year responses, public capital and property at zero";
  }
  HORIZON.first_year_horizon_property_long_run.band = FY8.band(P,"set","fixed_capital",{...FIRST,item6_first_year:true});
  HORIZON.first_year_horizon_property_long_run.src += "; item9 with fixed-capital item6; item10 first-year parent responses; item11 with its owner property (property long-run); item12 at its source lines' responses here, public capital at zero";
  for (const mode of ["whole", "corporate_only", "off"]) for (const basis of ["set", "cash"]) {
    HORIZON[`first_year_horizon_item6_${mode}${basis === "cash" ? "_cash" : ""}`] = {band:report.variants[mode][basis],src:report.sensitivity_limit};
  }
  outputs["first_year_item6_oct15.json"] = JSON.stringify(report, null, 2) + "\n";
}
if (CASE === "oct14") {
  const FY = require("./first_year_item6.cjs"), calibration = FY.calibration();
  const opts = Object.assign({}, FIRST, { property: "none" });
  const variants = {};
  const componentRows = [["mode", "basis", "end", "line", "scope", "amount_bn", "long_run_response", "first_year_response", "cost_change_from_whole_bn"]];
  const lineIds = Object.keys(payload.meta.items.find((r) => r.id === "job_capital_taxes").responses);
  if (lineIds.length !== 4 || !lineIds.every((id) => id in payload.meta.responses)) {
    throw new Error("[BLOCKED] first-year item 6: registry does not declare the four receipt responses");
  }
  for (const mode of FY.MODES) {
    const q = FY.packages(P, mode, calibration);
    variants[mode] = { set: q.set.central(opts), cash: q.cash.central(opts) };
    for (const basis of ["set", "cash"]) {
      const api = q[basis], original = basis === "set" ? P : P.CASH;
      const pm = api.payloadModel(), om = original.payloadModel();
      const cp = api.correctionsPayload(), op = original.correctionsPayload();
      gate(`first-year ${mode} ${basis}: all cell edits and population conserved`,
        JSON.stringify(cp.edits) === JSON.stringify(op.edits) && JSON.stringify(pm.meta) === JSON.stringify(om.meta));
      let nationalGap = 0, partGap = 0;
      const x = q.built.find((b) => b.item.id === "job_capital_taxes")[basis];
      const response = cp.meta.responses;
      for (const l of pm.receipts.lines) for (const sc of pm.receipts.scenarios) for (const a of ["personal", "shared"]) {
        const cell = l.cells[sc][a], old = om.receipts.lines.find((r) => r.id === l.id).cells[sc][a];
        nationalGap = Math.max(nationalGap, Math.abs(cell.target_bn + cell.other_bn - old.target_bn - old.other_bn));
        if (lineIds.includes(l.id)) partGap = Math.max(partGap,
          Math.abs(sum(Object.values(x.detail.new_parts[`${l.id}|${sc}`]).map((p) => p[a])) - cell.target_bn));
      }
      gate(`first-year ${mode} ${basis}: national totals and five-part closure (1e-9bn)`,
        nationalGap <= 1e-9 && partGap <= 1e-9, `${nationalGap} / ${partGap}`);
      const record = cp.meta.items.find((r) => r.id === "job_capital_taxes");
      gate(`first-year ${mode} ${basis}: registry parts unchanged`,
        JSON.stringify(record.parts) === JSON.stringify(op.meta.items.find((r) => r.id === record.id).parts));
      for (const [end, i] of ENDS) {
        const spec = MAIN_SPECS[i], rd = spec.reading;
        for (const id of lineIds) {
          const parts = x.detail.new_parts[`${id}|${REF}`];
          const amounts = {
            union: sum(Object.entries(parts).filter(([p]) => p.startsWith("union_")).map(([, p]) => p.personal)),
            added: sum(Object.entries(parts).filter(([p]) => p.startsWith("lineage_")).map(([, p]) => p.personal)),
          };
          amounts.lineage = amounts.union + amounts.added;
          for (const [scope, amount] of Object.entries(amounts)) {
            const before = op.meta.responses[id][rd], after = response[id][rd];
            componentRows.push([mode, basis, end, id, scope, amount, before, after, amount * (before - after)]);
          }
        }
      }
    }
  }
  gate("item 6 whole reproduces the four existing first-year numbers (1e-4bn)",
    variants.whole.set.every((v, j) => near(v, [235.9882, 298.2884][j], 1e-4))
    && variants.whole.cash.every((v, j) => near(v, [160.8617, 223.1620][j], 1e-4)));
  const report = { calibration, population_scope: "42.75M lineage; union and added people are separately identified in component rows",
    central: MAIN, thresholds: { midpoint_bn: M, low_bn: LOW_CUT, high_bn: HIGH_CUT }, variants, components: [] };
  const keys = componentRows[0];
  report.components = componentRows.slice(1).map((r) => Object.fromEntries(keys.map((k, i) => [k, r[i]])));
  for (const mode of FY.MODES) for (const basis of ["set", "cash"]) {
    const b = variants[mode][basis];
    const delta = ENDS.map(([end]) => sum(report.components.filter((r) => r.mode === mode && r.basis === basis && r.end === end && r.scope === "lineage")
      .map((r) => r.cost_change_from_whole_bn)));
    gate(`first-year ${mode} ${basis}: engine change equals four-line receipt change (1e-9bn)`,
      b.every((v, j) => near(v - variants.whole[basis][j], delta[j], 1e-9)));
  }
  HORIZON.first_year_horizon.band = variants.fixed_capital.set;
  HORIZON.first_year_horizon.src += "; item 6 business property at 0, corporate and production at 1-alpha of long-run response [ASSUMPTION; APPROX]";
  HORIZON.first_year_horizon_cash.band = variants.fixed_capital.cash;
  HORIZON.first_year_horizon_cash.src += "; item 6 fixed-capital rule [ASSUMPTION; APPROX]";
  HORIZON.first_year_horizon_property_long_run.band = FY.packages(P, "fixed_capital", calibration).set.central(FIRST);
  HORIZON.first_year_horizon_property_long_run.src += "; item 6 fixed-capital rule (item 5 alone kept at long-run)";
  for (const mode of ["whole", "corporate_only", "off"]) for (const basis of ["set", "cash"]) {
    HORIZON[`first_year_horizon_item6_${mode}${basis === "cash" ? "_cash" : ""}`] = {
      band: variants[mode][basis], src: `item 6 ${mode}; same first-year rules; ${basis}`,
    };
  }
  report.first_year_breaks_alone = mid(variants.fixed_capital.set) < LOW_CUT;
  outputs["first_year_item6_oct14.json"] = JSON.stringify(report, null, 2) + "\n";
}
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
    const s6 = SUMMARY, comp = s6[VERSION].companions, CASH_SET = s6.cash_set.band_bn;
    const minus = (b, c) => b.map((x, j) => x - c[j]);
    for (const [id, name] of [["lineage_arm_a", "arm_a"], ["lineage_arm_c", "arm_c"], ["lineage_c3_plus_1se", "c3_plus_se"],
      ["lineage_c3_minus_1se", "c3_minus_se"]]) {
      const o = V8PLUS ? (() => {
        const x=comp[`lineage_${name}`];
        return {label:`${VERSION} lineage_${name}`,set:{band_bn:x.band_bn,change_from_the_case_bn:x.band_bn.map((v,i)=>v-MAIN[i])},cash:{band_bn:x.cash_set_bn,change_from_the_case_bn:x.cash_set_bn.map((v,i)=>v-CASH_SET[i])}};
      })() : comp.options[name];
      gate(`${id}: ${VERSION}.companions.options.${name} is the case plus its change and main_case_bands.csv's row, on the set and the cash set (1e-9; 5e-5)`,
        o.set.band_bn.every((x, j) => near(x, MAIN[j] + o.set.change_from_the_case_bn[j], 1e-9) && near(x, bandRow(`lineage_${name}`)[j], 5e-5))
        && o.cash.band_bn.every((x, j) => near(x, CASH_SET[j] + o.cash.change_from_the_case_bn[j], 1e-9) && near(x, bandRow(`lineage_${name}_cash_set`)[j], 5e-5)),
        `${o.set.band_bn.map(f4).join("–")}`);
      LINEAGE[id].by = { set: o.set.change_from_the_case_bn.slice(), cash: o.cash.change_from_the_case_bn.slice() };
      LINEAGE[id].src = `${LANE} summary.json ${VERSION}.companions.options.${name}: ${o.label.replace(/"/g, "'")}`;
    }
    const AS = require(path.join(ROOT, V8PLUS ? "main_case_2026_10_14" : LANE, "ancestry_share.cjs"));
    const SH = readJson(AS.SHARES_FILE).shares;
    const SC = { ancestry_share_low: ["g4_at_nothing", SH.G3plus.bound_low], ancestry_share_high: ["g4_at_bound", SH.G3plus.bound_high],
      ancestry_share_convention: ["convention", SH.G3plus.convention] };
    const by = {};
    for (const which of ["set", "cash"]) {
      if (V8PLUS) {
        const rs = require(path.join(ROOT, LANE,"companions.cjs")).ancestry(P,which);
        for(const [id,[scenario]]of Object.entries(SC)){
          const own=scenario==="convention"?(()=>{
            const lo=rs.find(r=>r.scenario==="g4_at_nothing"),hi=rs.find(r=>r.scenario==="g4_at_bound"),t=(SH.G3plus.convention-lo.s_g3plus)/(hi.s_g3plus-lo.s_g3plus);
            const costs=lo.costs.map((v,i)=>v+t*(hi.costs[i]-v));return {band_bn:[Math.min(...costs),Math.max(...costs)]};
          })():rs.find(r=>r.scenario===scenario);
          if(!own)throw Error(`[BLOCKED] ${CASE} ancestry scenario ${scenario} absent`);
          const base=which==="set"?MAIN:CASH_SET;
          (by[id]=by[id]||{})[which]=minus(own.band_bn,base);
          if(scenario!=="convention")gate(`${id}/${which}: case ancestry band (5e-5)`,own.band_bn.every((v,j)=>near(v,bandRow(`ancestry_share_${scenario}${which==="cash"?"_cash_set":""}`)[j],5e-5)));
        }
        continue;
      }
      const r = AS.rowsFor(P, which, { Engine }), gc = r.generation_costs;
      const count = (g3) => gc.G1.map((x, i) => x + SH.G2.central * gc.G2[i] + g3 * gc.G3plus[i] + SH.added.central * r.added_costs[i]);
      const band = (g3) => { const f = count(g3); return [Math.min(...f), Math.max(...f)]; };
      const base = which === "set" ? MAIN : CASH_SET;
      for (const [id, [scenario, g3]] of Object.entries(SC)) {
        const b = band(g3);
        if (scenario !== "convention") {
          const own = r.rows.find((x) => x.scenario === scenario), kept = comp.ancestry_share[which].rows.find((x) => x.scenario === scenario);
          const row = bandRow(`ancestry_share_${scenario}${which === "cash" ? "_cash_set" : ""}`);
          gate(`${id}, ${which}: the count at its shares is rowsFor's row (1e-9), summary.json ${VERSION}.companions' (1e-6) and main_case_bands.csv's (5e-5)`,
            b.every((x, j) => near(x, own.band_bn[j], 1e-9) && near(x, kept.band_bn[j], 1e-6) && near(x, row[j], 5e-5)), `${b.map(f4).join("–")}`);
        }
        (by[id] = by[id] || {})[which] = minus(b, base);
      }
    }
    for (const [id, [scenario]] of Object.entries(SC)) {
      LINEAGE[id].by = by[id];
      LINEAGE[id].src = scenario === "convention"
        ? `[FRAMING-SENSITIVE] ${LANE} ancestry_share.cjs rowsFor on ${VERSION} (read-only): the whole lineage counted by ancestry share, every third-plus member at the population lane's convention (${SH.G3plus.convention.toFixed(4)}), inside the bound; no ${VERSION}.companions row`
        : `[FRAMING-SENSITIVE] ${LANE} summary.json ${VERSION}.companions.ancestry_share: the whole lineage counted by ancestry share, ${scenario === "g4_at_nothing" ? "the stated bound's low end (G4+ at nothing)" : "the stated bound's high end (G4+ at its measured high bound)"}`;
    }
    for (const x of [LINEAGE.replacement_r1, LINEAGE_LISTED.replacement_r05]) x.src += `; v5 delta carried, not recomputed on ${VERSION}`;
    if (LIVE_PERSONAL) {
      // The existing v5 replacement rule (lineage_case.cjs:560-577): subtract r x added persons x its white part.
      // Reconstruct its stored per-person model exactly (partModel, :283-288; whiteOf/setUp, :318-332), then price
      // it at the live personal ends. No import of lineage_case.cjs: importing it would rewrite the preserved lane.
      const wl = readJson(`${LL}/derived/white_lines.json`);
      const own = {};
      for (const which of ["set", "cash"]) {
        const Q = which === "set" ? P.OCT05 : P.OCT05.CASH;
        const white = wl.g3plus_ages[which === "set" ? "accrual" : "cash"].low;
        const amounts = new Map(white.lines.map((l) => [`${l.side}|${l.id}`, l.amount_bn / white.population]));
        const mW = JSON.parse(JSON.stringify(Q.payloadModel()));
        for (const [side, lines] of [["receipts", mW.receipts.lines], ["spending", mW.spending.lines]]) {
          for (const line of lines) {
            const amount = amounts.get(`${side}|${line.id}`);
            if (!Number.isFinite(amount)) throw new Error(`[BLOCKED] v5 replacement: no stored white amount on ${side}|${line.id}`);
            for (const cells of Object.values(side === "receipts" ? line.cells : line.keys)) for (const a of Q.ALLOCS) {
              cells[a].target_bn = amount;
              cells[a].share = 0;
            }
          }
        }
        for (const key of ["private_wtp_bn", "induced_receipts_bn"]) mW.production[key] = mW.production[key].map(() => 0);
        const cost = (i) => Q.evaluateFull(mW, Q.MAIN_SPECS[i]).cost_bn;
        const stored = v5s.replacement.rows.find((r) => r.set === which && r.arm === LIN.arm && r.r === 1);
        gate(`replacement ${which}: the reconstructed v5 white part reproduces its stored per-person prices at its historical ends (1e-9)`,
          stored.ends.every((i, j) => near(cost(i) * 1e9, stored.w_per_person_usd[j], 1e-9)));
        gate(`replacement ${which}: v5 specifications at the live ends ${endNumbers.join(" / ")} are personal`,
          endNumbers.every((i) => Q.MAIN_SPECS[i].allocation === "personal"));
        own[which] = endNumbers.map((i) => cost(i));
      }
      const added = v5s.sets.set.arms[LIN.arm].added;
      for (const [id, ratio, group] of [["replacement_r1", 1, LINEAGE], ["replacement_r05", 0.5, LINEAGE_LISTED]]) {
        group[id].by = Object.fromEntries(["set", "cash"].map((which) => [which, own[which].map((w) => -ratio * added * w)]));
        group[id].src = `[FRAMING-SENSITIVE; APPROX: additive transfer] ${LL} lineage_case.cjs replacement rule, its stored white_lines.json per-person model rederived on v5 at matching personal specifications ${endNumbers.join(" / ")}; subtract ${ratio} x ${added} added persons x white cost. This v5 delta is transferred to v7, not a v7 replacement-child model`;
      }
    }
  }
  gate("every lineage alternative is a finite pair on both sets, in its direction at the midpoint", Object.values(Object.assign({}, LINEAGE, LINEAGE_LISTED))
    .every((x) => ["set", "cash"].every((s) => x.by[s].every(Number.isFinite) && (x.dir === "down" ? mid(x.by[s]) < 0 : mid(x.by[s]) > 0))));
}
// oct07: the items' arms (summary.json v6.arms; each the whole case with one item at that arm, package.cjs caseOf), each
// the change of its band from the case's on the set or, with cash pensions, from the cash set's; an item the cash set
// does not carry (the pension item's, set only) moves it by 0 [APPROX: additive; at most one arm per item in a
// combination]. Its direction is its set midpoint's.
const ITEM_ALTS = {};
// oct16: every arm but the set-only mixed reading is priced in bounded children on the canonical route.
const ARM_CHILD_PRICES=CASE==="oct16"?require("./item_arm_prices.cjs").priceInChildren(
  P.REGISTRY.filter(item=>P.CANDIDATE.includes(item.id)).flatMap(item=>Object.entries(item.arms||{}).filter(([,a])=>a)
    .map(([arm])=>[item.id,arm]).filter(([id,arm])=>!(id==="mixed_unit_removal"&&arm==="bounded_high_plus_pension_model"))),console.log):{};
if (ITEMS.length) {
  const s6 = SUMMARY, v6arms = V8PLUS ? Object.fromEntries(P.REGISTRY.filter(item=>P.CANDIDATE.includes(item.id)).flatMap(item=>Object.entries(item.arms||{}).filter(([,a])=>a).map(([arm,a])=>{
    const armStarted=performance.now();
    const id=`${item.id}_${arm}`,setOnly=item.id==="mixed_unit_removal"&&arm==="bounded_high_plus_pension_model";
    let b,cash;
    if(setOnly){const z=P.MIXED.get(null,"set",arm);b=[0,1].map(i=>MAIN[i]+z[["low","high"][i]]-P.POST_ENGINE.mixed_unit_removal[["low","high"][i]]);cash=s6.cash_set.band_bn;}
    else if(CASE==="oct16"){const z=ARM_CHILD_PRICES[`${item.id}:${arm}`];b=z.band_bn.slice();cash=z.cash_bn.slice();}
    else {const Q=P.caseOf(P.OCT05,P.CANDIDATE,{[item.id]:arm});b=Q.central({});cash=Q.CASH.central({});}
    // The case's source gate declares this arm idempotent once item9 is on.
    // Verify exact package parity, then represent the proven no-op as zero; a
    // four-decimal CSV must never manufacture a signed alternative here.
    if(id==="job_capital_taxes_foreign_source_removed") {
      const ok=b.every((v,i)=>near(v,MAIN[i],1e-9))&&cash.every((v,i)=>near(v,s6.cash_set.band_bn[i],1e-9));
      gate("domestic-source arm is an exact no-op with item9 on (1e-9)",ok);
      if(!ok)throw Error("[BLOCKED] domestic-source no-op does not match the exact package");
      b=MAIN.slice();cash=s6.cash_set.band_bn.slice();
    }
    if(CASE==="oct16"&&b.every((v,i)=>near(v,MAIN[i],1e-9))&&cash.every((v,i)=>near(v,s6.cash_set.band_bn[i],1e-9))){
      b=MAIN.slice();cash=s6.cash_set.band_bn.slice();
    }
    console.log(`  priced item arm ${id}; wall ${((performance.now()-armStarted)/1000).toFixed(3)}s`);
    return [id,{item:item.id,label:a.label||arm,band_bn:b,change_from_the_case_bn:b.map((v,i)=>v-MAIN[i]),cash:{band_bn:cash,change_from_the_cash_set_bn:cash.map((v,i)=>v-s6.cash_set.band_bn[i])}}];
  }))) : s6[VERSION].arms;
  for (const [id, a] of Object.entries(v6arms)) {
    const set = a.change_from_the_case_bn, cash = a.cash ? a.cash.change_from_the_cash_set_bn : [0, 0];
    const cashRow = (CASE === "oct14" && !P.REGISTRY.find((r) => r.id === a.item).cash.applies) || (V8PLUS&&id==="mixed_unit_removal_bounded_high_plus_pension_model") ? "cash_set" : `${id}_cash_set`;
    const published=currentBandRow(id),publishedCash=currentBandRow(cashRow);
    if(CASE==="oct16")publishedCrossChecks[published?"item_arms_checked":"item_arms_without_current_row"].push(id);
    gate(`item arm ${id}: its band is the case plus its change (1e-9), and current published rows (5e-5); historical rows excluded`,
      a.band_bn.every((x, j) => near(x, MAIN[j] + set[j], 1e-9) && (!published||near(x, published[j], 5e-5)))
      && (!a.cash || a.cash.band_bn.every((x, j) => near(x, s6.cash_set.band_bn[j] + cash[j], 1e-9) && (!publishedCash||near(x, publishedCash[j], 5e-5)))));
    ITEM_ALTS[id] = { item: a.item, listed:CASE==="oct16"&&id==="one_rate_capital_7pct",dir: mid(set) < 0 ? "down" : "up", by: { set, cash },
      src: `${LANE} summary.json ${VERSION}.arms ${id} (item ${a.item}): ${a.label.replace(/"/g, "'")}` };
  }
  // An arm's cash change may run against its set direction: coverage's DA-through-29 arm lowers the set and raises the
  // cash set at the low end, because once custody is not charged twice (round 3, R3-12) the missed young adults it
  // removes are net payers when benefits count as paid and net costs when promises accrue. The search assumes no
  // monotonicity (minimal_subsets.cjs), so such an arm is named here, not refused.
  const against = Object.entries(ITEM_ALTS).filter(([, x]) => (x.dir === "down" ? mid(x.by.cash) > 0 : mid(x.by.cash) < 0));
  gate("every item arm is a finite pair on both sets, its set change in its direction",
    Object.values(ITEM_ALTS).every((x) => ["set", "cash"].every((s) => x.by[s].every(Number.isFinite))
      && (x.dir === "down" ? mid(x.by.set) <= 0 : mid(x.by.set) >= 0)),
    against.length ? "cash change against the set direction: " + against.map(([id, x]) => `${id} ${x.by.cash.map(f4).join(" / ")}`).join("; ") : "");
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
   armRows.push([id, x.dir, x.listed?"item (listed alias of capital_7pct)":"item", b[0], b[1], mid(b), 100 * (mid(b) / M - 1), `"${x.src}"`]);
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
  if (!joint.has(key)) {const t0=performance.now();joint.set(key, centralOf(o));console.log(`  joint engine run ${joint.size} [${key||"none"}]; wall ${((performance.now()-t0)/1000).toFixed(3)}s`);}
  const b = joint.get(key).slice();
  for (const id of ids) if (ADD[id]) { b[0] += ADD[id].by[0]; b[1] += ADD[id].by[1]; }
  const which = o.pension4 === "cash" ? "cash" : "set";
  for (const id of ids) if (LINEAGE[id]) { b[0] += LINEAGE[id].by[which][0]; b[1] += LINEAGE[id].by[which][1]; }
  for (const id of ids) if (ITEM_ALTS[id]) { b[0] += ITEM_ALTS[id].by[which][0]; b[1] += ITEM_ALTS[id].by[which][1]; }
  return b;
}
const cutRows = [["direction", "set", "size", "cost_low_bn", "cost_high_bn", "midpoint_bn", "move_pct_of_midpoint", "minimal"]];
const searchReceipt={case:CASE,coverage:"all eligible source arms in the declared combination model; at most one lineage and one per item",
  combination_model:"Engine arms are jointly repriced. ADD amounts and delivered LINEAGE/ITEM_ALTS deltas are added to that joint band, on the selected set/cash basis. Lineage/item alternatives retain their declared additive transport approximation; subsets are not all jointly remeasured in the full engine.",directions:{}};
for (const dir of ["down", "up"]) {
  const lin = Object.keys(LINEAGE).filter((k) => LINEAGE[k].dir === dir);
  const itm = Object.keys(ITEM_ALTS).filter((k) => ITEM_ALTS[k].dir === dir&&!ITEM_ALTS[k].listed);
  const ids = Object.keys(ARMS).filter((k) => ARMS[k].dir === dir).concat(Object.keys(ADD).filter((k) => ADD[k].dir === dir)).concat(lin).concat(itm);
  const grouped=ids.filter(id=>ITEM_ALTS[id]||ARMS[id]?.item);
  const itemGroups=Object.values(grouped.reduce((by,id)=>{(by[(ITEM_ALTS[id]||ARMS[id]).item]??=[]).push(id);return by;},{}));
  const groups=ids.filter(id=>!LINEAGE[id]&&!ITEM_ALTS[id]&&!ARMS[id]?.item).map(id=>[id]).concat(lin.length?[lin]:[],itemGroups);
  const started=performance.now();
  const searched=require("./minimal_subsets.cjs").minimalCrossings(groups,subsetBand,
    b=>dir==="down"?mid(b)<LOW_CUT:mid(b)>HIGH_CUT,
    x=>console.log(`  ${dir} search size ${x.size}/${groups.length}: ${x.evaluated} evaluated, ${x.minimal_crossings} minimal, ${joint.size} joint engine runs; wall ${((performance.now()-started)/1000).toFixed(1)}s`),
    C1_MAX_SIZE);
  const minimal=searched.cuts.map(x=>({...x,set:x.set.sort((a,b)=>ids.indexOf(a)-ids.indexOf(b))}));
  searchReceipt.directions[dir]={groups,...searched.counts,proof:searched.proof};
  console.log(`  exact ${dir} search: ${ids.length} arms, ${groups.length} groups; ${searched.counts.evaluated} evaluated / ${searched.counts.eligible_nonempty_sets} eligible; ${minimal.length} minimal crossings; wall ${(performance.now()-started)/1000}s`);
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
  if(CASE==="oct16")for(const item of new Set(base.map(id=>(ARMS[id]||ITEM_ALTS[id])?.item).filter(Boolean))){
    const family=base.filter(id=>(ARMS[id]||ITEM_ALTS[id])?.item===item);
    if(family.length>1){const keep=family.reduce((a,b)=>Math.abs(mid(subsetBand([a]))-M)>=Math.abs(mid(subsetBand([b]))-M)?a:b);for(const id of family)if(id!==keep)base.splice(base.indexOf(id),1);}
  }
  for (const stack of pick.length ? [base, base.concat(pick)] : [base]) {
    const all = subsetBand(stack);
    cutRows.push([dir, "ALL:" + stack.join("+"), stack.length, all[0], all[1], mid(all), 100 * (mid(all) / M - 1), "stack"]);
  }
}
outputs[`c1_min_cuts_${CASE}.csv`] = csvText(cutRows);
if(CASE==="oct16"){searchReceipt.max_size_searched=C1_MAX_SIZE;searchReceipt.published_cross_checks=publishedCrossChecks;}
outputs[`c1_search_${CASE}.json`]=JSON.stringify(searchReceipt,null,2)+"\n";
console.log(`  thresholds: midpoint ${M.toFixed(2)}, a quarter down ${LOW_CUT.toFixed(2)}, up ${HIGH_CUT.toFixed(2)}`);

// ------------------------------------------------------------------------------------------------ C2 and C3
console.log(`[C2 taxes against benefits; C3 corrections by side, ${CASE}]`);
const p27 = readJson("main_case_long_run_2026_09_27/derived/corrections.json");
const N27 = p27.edits.length;
gate(`v4's payload opens with the September 27 payload's ${N27} edits, unchanged`,
  payload.edits.slice(0, N27).every((e, k) => JSON.stringify(e) === JSON.stringify(p27.edits[k])), `${payload.edits.length} edits in all`);
// oct05: the lineage's edits (its cells, then row 8's move) close the payload and are held in every run, after v4's items.
const LIN_FIRST = LIN ? LIN.edits.first : payload.edits.length;
const orderedEditRecords=CASE==="oct16"?payload.meta.items.filter(r=>r.applied&&r.edits):ITEMS;
if (LIN) gate(ITEMS.length ? "the lineage's edits come before the items', row 8's move last, and the items' edits close the payload in order"
  : "the lineage's edits close the payload, row 8's move last", LIN.edits.first + LIN.edits.count === ITEM_FIRST
  && LIN.edits.row8_edit_index === ITEM_FIRST - 1 && orderedEditRecords.every((r, k) => r.edits.first === (k ? orderedEditRecords[k - 1].edits.first + orderedEditRecords[k - 1].edits.count : ITEM_FIRST))
  && (orderedEditRecords.length ? orderedEditRecords[orderedEditRecords.length - 1].edits.first + orderedEditRecords[orderedEditRecords.length - 1].edits.count : ITEM_FIRST) === payload.edits.length);
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
const completionCell=(side,line,a)=>V8PLUS ? sum(payload.edits.slice(payload.meta.items.find(r=>r.id==="union_completion").edits.first,payload.meta.items.find(r=>r.id==="union_completion").edits.first+payload.meta.items.find(r=>r.id==="union_completion").edits.count).filter(e=>e.side===side&&e.line===line&&(side==="receipt"?e.scenario===REF:e.key===prefKey(line))).map(e=>e.by[a])) : 0;
const completionOasdi=a=>sum(ACC.oasdi_lines.map(id=>completionCell("receipt",id,a)))+ACC.se_oasdi_share*completionCell("receipt",ACC.se_line,a);
// oct07: the union's Medicare switch is the tail's edit plus the edit sets' union_* parts on Medicare.
const tailMed = (a) => TAIL_MED[0].by[a] + ITEM_PEN.union.medicare[a];
// oct05: the switch is rebuilt on the union's part; the lineage keeps its own accrual (its edits, held).
function pensionRebuilt(m) {
  const by = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
  const ss = by((a) => (LIN ? ACC.ratio_net * (oasdiOf(m, a) - completionOasdi(a) - linOasdi(a)) + linSS(a) + completionCell("spending","social_security",a) : ACC.ratio_net * oasdiOf(m, a)) + ROW4_UNION_PEN.social_security[a]
    - benefit(m, "social_security", a));
  const med = by((a) => {
    if (LIN) {
      const own = linMedSet(a);
      const completed=completionCell("spending","medicare",a);
      const preU = benefit(m, "medicare", a) - completed - tailMed(a) - own;
      return (1 - ACC.part_a_share) * preU + ACC.part_a_accrual_bn + ROW4_UNION_PEN.medicare[a] + own + completed - benefit(m, "medicare", a);
    }
    const pre = benefit(m, "medicare", a) - tailMed(a);
    return (1 - ACC.part_a_share) * pre + ACC.part_a_accrual_bn + ROW4_UNION_PEN.medicare[a] - benefit(m, "medicare", a);
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
if (LIVE_PERSONAL) gate(`the cash payload equals summary.json ${VERSION}.cash_set_bn (1e-9)`,
  CASH.every((x, j) => near(x, SUMMARY[VERSION].cash_set_bn[j], 1e-9)));
// The tally at scheduled benefits moves by the scheduled rule on each model's own OASDI receipts.
// oct05 adds the union alone at the case's responses (v4's payload with row 8's move): the case less it is the lineage's.
const tallyRows = [["model", "end", "spec", "direct_receipts_bn", "household_transfers_bn", "tally_bn", "scheduled_move_bn", "tally_at_scheduled_bn"]];
const tallyModels = [["case_accrual", P, m29, true], ["cash_set", PC, mCash, false],
  ["v4_items_without_dataset_corrections", P, R.base.m, true], ["v4_items_without_dataset_corrections_increments_held", P, mBase, true],
  ["uncorrected_no_v4_items", P, V8PLUS?P.withSyntheticLines(MODEL):MODEL, false]];
if(V8PLUS){
  if(C2_POSTENGINE_CLASS_RULE==="stop")throw Error("[BLOCKED] C2 post-engine receipt/transfer-class split undeclared");
  console.log("[GAP] C2 class-defined tally excludes unclassified mixed-unit/coverage net costs; service break-even includes them in full");
}
function directTally(pkg,ev,full){
  let rec=ev.classes.direct_receipts.responsive_bn,tr=ev.classes.household_transfer.responsive_bn;
  if(V8PLUS)for(const [id,src]of Object.entries(pkg.correctionsPayload().meta.union_completion.carriers))if(src.kind==="line"){
    const carrier=ev.spending.find(r=>r.id===id),parent=(src.side==="receipt"?ev.receipts:ev.spending).find(r=>r.id===src.parent_line);
    if(!carrier||!parent)throw Error(`[BLOCKED] C2 completion class lacks carrier/parent ${id}`);
    if(src.side==="receipt"&&parent.group==="direct_receipts")rec-=carrier.amount_bn*carrier.response;
    if(src.side==="spending"&&parent.response_class==="household_transfer")tr+=carrier.amount_bn*carrier.response;
  }
  if(CASE==="oct16"){
    if(!full?.v9_post_engine?.parts)throw Error("[BLOCKED] C2 v9 classified post parts absent");
    for(const parts of Object.values(full.v9_post_engine.parts))for(const p of parts){
      const line=ev.spending.find(r=>r.id===p.line);
      if(line?.response_class==="household_transfer"){
        if(!Number.isFinite(p.delta_bn))throw Error("[BLOCKED] C2 non-finite classified post amount");
        tr+=p.delta_bn;
      }
    }
  }
  return [rec,tr];
}
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
  let mU = Engine.applyCorrections(P.SEPT29.payloadModel(), { lines: V8PLUS ? payload.lines.filter(l=>l.family==="union_completion_carrier") : [], receipt_lines: itemCarriers(), edits: [payload.edits[LIN.edits.row8_edit_index]].concat(itemUnion()) });
  if(CASE==="oct16")for(const {x}of P.V9_BUILT)mU=Engine.applyCorrections(mU,{edits:x.editsAt?x.editsAt(mU,{}):x.edits,meta:mU.corrections});
  tallyModels.push(["union_at_case_responses", P, mU, "union"]);
}
for (const [lab, pkg, m, accrual] of tallyModels) {
  const sched = accrual ? schedAdd(m, accrual === true && Boolean(LIN)) : null;
  ENDS.forEach(([end, i], j) => {
    const full = pkg.evaluateFull(m, pkg.MAIN_SPECS[i]),ev=full.evaluation;
    const [rec,tr] = directTally(pkg,ev,full);
    tallyRows.push([lab, end, i, rec, tr, rec - tr, accrual ? sched[j] : "", accrual ? rec - tr - sched[j] : ""]);
  });
}
if (LIN && LIVE_PERSONAL) {
  for (const arm of ["a", "c"]) {
    const variant = P.caseOf(P.OCT05, P.CANDIDATE, {}, `arm_${arm}`), model = variant.payloadModel();
    ENDS.forEach(([end, i]) => {
      const full = variant.evaluateFull(model, variant.MAIN_SPECS[i]),ev=full.evaluation;
      const [rec,tr] = directTally(variant,ev,full);
      tallyRows.push([`lineage_arm_${arm}`, end, i, rec, tr, rec - tr, "", ""]);
    });
  }
} else if (LIN) {
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

// Clause 2: the service break-even, main_case_2026_09_24's definition inside the case through
// main_case_2026_10_16/sign_reversal.cjs's withCase, the rule's one definition (imported since 2026-10-21; this lane
// kept a copy before): rental assistance at 1, the enterprise receipts at 1 or at s, every other receipt response of
// meta.responses fixed, the union-completion carriers mapped, service capital carriers and items 21 and 15 following
// the service response, and the capital return from the same evaluation. It runs on the live case only.
const GG = P.RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG.low : GG.high }));
const generationServicePosts=new Map(),generationServiceShares=new Map();
// A generation's scoped package prices its post-engine costs as its share of the whole case's at the same sweep point:
// the union's v9 additions there, split across generations by generationParts' shares of each item at the case
// specification [APPROX: a generation's share of an item is held at the case's other line responses]. The welfare
// closure gate tests the generation parts against the union. The rule scales items 21 and 15 on these amounts.
const generationPost=(pkg)=>(r,ctx)=>{
  const plainSpec=r.spec,spec={...plainSpec};
  // generationParts re-evaluates the generation models and the union from a complete specification: take the
  // case's own specification at this reading, allocation and normalization (its line responses, justice key),
  // then the sweep's service, government, care, rate and enterprise fields. Its post amounts are therefore
  // at the case's other line responses, not the sweep's wrapper overrides [APPROX].
  const norm=ctx.st.production?.normalization;
  const matches=pkg._full.ALL_SPECS.filter(x=>x.reading===r.reading&&x.allocation===ctx.st.allocation&&x.normalization===norm),base=matches[0];
  if(!base)throw Error(`[BLOCKED] no case specification at ${r.reading}/${ctx.st.allocation}/${norm} for the generation sweep`);
  if(new Set(matches.map(x=>JSON.stringify([x.line_responses,x.justice,x.long_run]))).size!==1)
    throw Error(`[BLOCKED] case specifications at ${r.reading}/${ctx.st.allocation}/${norm} disagree on line responses`);
  Object.assign(spec,{...JSON.parse(JSON.stringify(base)),...plainSpec,normalization:norm,long_run:base.long_run});
  if(!spec.long_run)throw Error("[BLOCKED] generation sweep specification is not long-run");
  const U=pkg._full,which=U===P?"set":"cash",at=JSON.stringify([which,ctx.variant,plainSpec]);
  if(!generationServicePosts.has(at)){
    const um=U.payloadModel();
    generationServicePosts.set(at,ctx.sweep(U,um,ctx.st).added.amounts);
  }
  const shareKey=JSON.stringify([which,pkg._convention,spec]);
  if(!generationServiceShares.has(shareKey)){
    const z=require("../generation_account_2026_09_24/v9_split.cjs").generationParts(U,spec,pkg._convention);
    const ids=new Set(Object.values(z.posts).flatMap(p=>Object.keys(p)));
    generationServiceShares.set(shareKey,Object.fromEntries([...ids].map(id=>{
      const total=sum(Object.values(z.posts).map(p=>p[id]||0));
      return [id,total?Object.fromEntries(Object.entries(z.posts).map(([g,p])=>[g,(p[id]||0)/total])):null];
    })));
  }
  const shares=generationServiceShares.get(shareKey),amounts={};
  for(const [id,amount]of Object.entries(generationServicePosts.get(at))){
    if(!amount)continue;
    if(!shares[id])throw Error(`[BLOCKED] ${CASE} sweep: item ${id} moves the union (${amount}) but has no generation shares at the case specification`);
    amounts[id]=amount*shares[id][pkg._generation];
  }
  return {base:pkg.postEngine(spec),amounts,total:sum(Object.values(amounts))};
};
function withCase(pkg, variant, f) {
  if(CASE!=="oct16")throw Error(`[BLOCKED] ${CASE}: the service break-even runs on the live case only; earlier cases' outputs stay in git`);
  const SR=require("../main_case_2026_10_16/sign_reversal.cjs");
  if(SR.P!==P)throw Error("[BLOCKED] the sign-reversal rule loads another instance of the case package");
  return SR.withCase(pkg, variant, f, undefined, pkg._generation ? { post: generationPost(pkg) } : {});
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
const GEN_V8_EVALUATORS={};
for (const [lab, pkg, file, results] of [["case_accrual", P, `generation_corrections_${CASE}.json`, `generation_results_${CASE}.csv`],
  ["cash_set", PC, `generation_corrections_${CASE}_cash.json`, `generation_results_${CASE}_cash.csv`]]) {
  const missing = [file, results].filter((f) => !fs.existsSync(path.join(ROOT, GEN, f)));
  if (missing.length) {      // the generation account's split of this case is not built yet: stop, write nothing
    gate(`${lab}: the generation account's ${missing.join(" and ")} exist`, false);
    continue;
  }
  genHashes.push([`${GEN}/${file}`, sha256(`${GEN}/${file}`)], [`${GEN}/${results}`, sha256(`${GEN}/${results}`)]);
  if(V8PLUS)for(const rel of [`${GEN}/${file}`,`${GEN}/${results}`])
    if(sha256(rel)!==generationPreflightHashes.get(rel))throw Error(`[BLOCKED] generation input changed during break run: ${rel}`);
  const gp = readJson(`${GEN}/${file}`).payloads;
  const res = readCsv(`${GEN}/${results}`);
  const meta = pkg.correctionsPayload().meta;
  for (const conv of ["a", "b"]) {
    const costs = { low: 0, high: 0 }, payloadRoute = { low: 0, high: 0 };
    const scopedModels=[];
    for (const g of ["G1", "G2", "G3plus"]) {
      const raw = readJson(`${GEN}/${conv === "a" ? `model_${g}.json` : `model_b_${g}.json`}`);
      const generationMeta=V8PLUS?gp[conv][g].meta:meta;
      if(V8PLUS&&generationMeta?.generation!==g)throw Error(`[BLOCKED] scoped generation metadata absent for ${conv}/${g}`);
      const mg = Engine.applyCorrections(raw, Object.assign({}, gp[conv][g], { meta:generationMeta }));
      const row = (end) => res.find((r) => r.convention === conv && r.generation === g && r.band_end === end);
      const scoped = V8PLUS ? {...pkg,_generation:g,_convention:conv,_full:pkg,postEngine:s=>{
        const mixed=generationMeta.mixed_unit_removal.by_end[s.reading].total_bn;
        const coverage=generationMeta.coverage.by_end[s.reading].total_bn;
        if(!Number.isFinite(mixed)||!Number.isFinite(coverage))throw Error(`[BLOCKED] ${CASE} ${g} post-engine generation parts absent`);
        return mixed+coverage;
      }} : pkg;
      scopedModels.push([scoped,mg]);
      const costAt=i=>{
        const s=pkg.MAIN_SPECS[i];
        if(CASE==="oct16")return require("../generation_account_2026_09_24/v9_split.cjs").generationParts(pkg,s,conv).costs[g];
        const r=pkg.evaluateFull(mg,s);return r.cost_bn-(CASE === "oct15"?pkg.postEngine(s)-scoped.postEngine(s):0);
      };
      const lo = costAt(endNumbers[0]), hi = costAt(endNumbers[1]);
      gate(`${lab} ${conv} ${g}: the corrected model reproduces ${results} at ${endNumbers.join(" / ")} (1e-6)`,
        near(lo, +row("low").cost_bn, 1e-6) && near(hi, +row("high").cost_bn, 1e-6), `${lo.toFixed(4)} / ${hi.toFixed(4)}`);
      if(CASE==="oct16"){
        // generationParts is the producer's own route, so the gate above replays it. Price the published
        // payload by its declared consumer rule too: the inherited v8 evaluator on this generation's payload
        // model, plus that payload's v9_posts_by_spec at the same specification.
        const which=lab==="case_accrual"?"set":"cash";
        const ev8=(GEN_V8_EVALUATORS[which]??=(()=>{const G8=require("../generation_account_2026_09_24/v8_split.cjs"),L=G8.loadCase(which);return G8.evaluator(L.payload,L.api);})());
        const consumer=i=>{
          const declared=generationMeta.v9_posts_by_spec?.[i];
          if(!declared||JSON.stringify(generationMeta.v9_specs?.[i])!==JSON.stringify(pkg.MAIN_SPECS[i]))
            throw Error(`[BLOCKED] ${CASE} ${conv}/${g}: payload v9 posts/specification ${i} absent or not the case's`);
          return ev8.evaluateFull(mg,pkg.MAIN_SPECS[i]).cost_bn+sum(Object.values(declared));
        };
        const plo=consumer(endNumbers[0]),phi=consumer(endNumbers[1]);
        payloadRoute.low+=plo;payloadRoute.high+=phi;
        gate(`${lab} ${conv} ${g}: the payload's consumer rule reproduces ${results} at ${endNumbers.join(" / ")} (1e-6)`,
          near(plo, +row("low").cost_bn, 1e-6) && near(phi, +row("high").cost_bn, 1e-6), `${plo.toFixed(4)} / ${phi.toFixed(4)}`);
      }
      costs.low += lo; costs.high += hi;
      const bp = withCase(scoped, "enterprises_at_s", () => S24.breakEven(mg, "personal", PAIRS));
      const bs = withCase(scoped, "enterprises_at_s", () => S24.breakEven(mg, "shared", PAIRS));
      genRows.push([lab, conv, g, lo, hi, bp[0], bp[1], bs[0], bs[1]]);
    }
    const want = lab === "case_accrual" ? MAIN : CASH;
    gate(`${lab} ${conv}: the three generations add to the case at ${endNumbers.join(" / ")} (${V8PLUS ? "1e-9" : "1e-6"})`, near(costs.low, want[0], V8PLUS?1e-9:1e-6) && near(costs.high, want[1], V8PLUS?1e-9:1e-6),
      `${costs.low.toFixed(4)} / ${costs.high.toFixed(4)}`);
    if(CASE==="oct16")gate(`${lab} ${conv}: the payload consumer route's three generations add to the case (1e-6)`,
      near(payloadRoute.low,want[0],1e-6)&&near(payloadRoute.high,want[1],1e-6),`${payloadRoute.low.toFixed(4)} / ${payloadRoute.high.toFixed(4)}`);
    if(CASE==="oct16"){
      const whole=pkg.payloadModel(),production=S24.productions(1)[0],share=S24.SHARES[0];let gap=0;
      for(const allocation of ["personal","shared"])for(const pair of PAIRS)for(const service of [0,.37,1]){
        const full=withCase(pkg,"enterprises_at_s",()=>S24.welfare(whole,allocation,service,pair,production,share));
        const parts=sum(scopedModels.map(([Q,m])=>withCase(Q,"enterprises_at_s",()=>S24.welfare(m,allocation,service,pair,production,share))));
        gap=Math.max(gap,Math.abs(parts-full));
      }
      gate(`${lab} ${conv}: generation service-response welfare closes at0/.37/1 and both allocations (1e-9)`,gap<=1e-9,gap.toExponential(3));
    }
  }
}
outputs[`c6_generation_break_even_${CASE}.csv`] = csvText(genRows);
outputs[`c6_inputs_${CASE}.csv`] = genHashes.map((r) => r.join(",")).join("\n") + "\n";

if (failures) {
  console.error(`[BLOCKED] ${failures} gate(s) failed; nothing written`);
  process.exit(1);
}
if(CASE==="oct16")require("../main_case_2026_10_16/memory_guard.cjs").requireWithinBudget("break conditions v9");
fs.mkdirSync(OUT, { recursive: true });
for (const [name, text] of Object.entries(outputs)) fs.writeFileSync(path.join(OUT, name), text);
console.log("\n[written] " + Object.keys(outputs).join(", "));
for (const name of ["c1_min_cuts", "c2_tally", "c2_break_even", "c3_correction_split", "c6_generation_break_even"]) {
  console.log(fs.readFileSync(path.join(OUT, `${name}_${CASE}.csv`), "utf8"));
}
