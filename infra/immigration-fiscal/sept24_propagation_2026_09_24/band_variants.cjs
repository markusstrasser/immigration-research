/* The main case's key variants on the September 23 case and every adopted case since, for the real-costs
 * totals.
 *
 * The real-costs memo (research/immigration-real-fiscal-and-social-costs-2026-09-23.md, §7) pairs the
 * fiscal band with the social items on two crime footings and stacks a full span. It reads four variants
 * of the September 23 case from main_case_2026_09_23/derived/main_case_bands.csv: justice keyed with the
 * census ethnicity codes as recorded, the justice grid's two ends, and uncompensated care at 0.7x use.
 * The September 24 lane wrote none of them. This script evaluates them on each case with the package's
 * own evaluator (package.cjs cost(), the 64 main specifications):
 *   - raw coding and 0.7x use are executed keys (use_raw_coding, uninsured_use_07_low/high), and the
 *     payload carries every correction to them (package.cjs KEY_FAMILIES);
 *   - the grid ends and CBP held fixed are the justice lane's changes relative to its central, applied as
 *     a target shift on the use key, as main_case_2026_09_23/main_case.js applied them to the per-head key.
 *     On the adopted cases the booking correction therefore stays at its use-key value on the grid.
 *
 * Cases (--case). Every run evaluates the September 23 case (the uncorrected model at 0.59/0.84 and
 * 0.63/0.66) and the September 24 case. A later case adds its own two runs: the uncorrected model and
 * its corrections.json, both at the responses in the payload's meta.responses, never typed here.
 *   sept24          main_case_2026_09_24 (the committed run)           -> derived/
 *   sept26          main_case_2026_09_26, the one-year scenario        -> --out-dir DIR only
 *   sept26_schools  main_case_schools_full_2026_09_26, schools at full
 *                   average cost                                       -> ../sept26_propagation_2026_09_26/derived/
 *   sept27          main_case_long_run_2026_09_27, the September 27    -> ../sept27_propagation_2026_09_27/derived/
 *                   case (default)
 *   sept29          main_case_2026_09_29, the main case adopted        -> derived/sept29/
 *                   2026-09-29 (candidate v4)
 * From September 27 a specification also carries its reading, the two long-run lines' responses, rental
 * assistance, the enterprise receipt's response and the rate of the return on public capital, all from
 * meta.responses and meta.capital_return; cost() is the package's evaluateFull() cost, the engine's cost
 * plus the capital return keyed on the same evaluation, so a variant that moves a key moves the return
 * with it. Two more runs of the corrected model sit beside the case, never in its band: the return at the
 * reported 7% on every component, and option A (enterprises out), each built with the package's
 * specsFor() switch as the case lane builds them.
 * Gates (exit 1, nothing written): every variant on the uncorrected model reproduces the September 23
 * file (1e-4, its rounding); the corrected model reproduces the adopted September 24 band (1e-9 against
 * summary.json); the payload moves raw coding and use by the same amount (1e-9). On a later case: its
 * meta.responses equal its summary.json's, and the specifications built from them equal its package's
 * MAIN_SPECS; the adopted variant reproduces the case's band and, on the uncorrected model,
 * uncorrected_at_adopted_responses (1e-9 against summary.json, 1e-4 against main_case_bands.csv); each
 * variant moves every specification by the same amount on the uncorrected and corrected model (1e-9).
 * From September 27 the 7% and option A runs reproduce summary.json's beside_the_account bands (1e-9) and
 * main_case_bands.csv's capital_return_at_7pct and enterprises_out_option_a rows (1e-4).
 *
 * September 29 (v4). A specification's line_responses are rebuilt from every entry of meta.responses (13 entries:
 * the four above, four more receipt overrides and five correction lines), not from three named ones. Two things
 * are new:
 *   - State prices follow the justice key. The payload prices public order and safety at the states' price level
 *     with a correction line whose group amount is national_gap_bn x the parent line's key share on its evaluated
 *     key (meta.state_pricing). A justice variant evaluates the parent on another key (raw coding) or moves its use
 *     key (the grid ends, CBP held fixed), so it re-prices that line on the variant's key, as the rule states
 *     (statePriced). Gates: the rule rebuilds the payload's amounts on the case's own key (1e-9); each variant then
 *     moves the corrected model by the uncorrected model's move plus the re-pricing's own effect (1e-9). The
 *     alternative, the line held at the case's key, is written beside as <variant>_state_price_held.
 *   - The cash set runs beside the case, never in its band: the payload with the pension switch off (the
 *     adopted lane reads the candidate's corrections_v4_cash.json, main_case.cjs), costed through the package's
 *     forPayload() of it. Gates: its responses, capital rules and state pricing equal the case payload's; its
 *     adopted variant reproduces summary.json's cash_set band (1e-9) and main_case_bands.csv's cash_set row (1e-4).
 *
 * October 5 (v5, oct05: main_case_2026_10_05 -> derived/oct05/). The payload is the September 29 payload plus the
 * lineage's cell edits (meta.lineage: the 3.04M descendants who no longer report Mexican origin, priced at G3+ members'
 * and third-plus whites' amounts in every engine cell). Three things are new:
 *   - The cash set is that lane's own derived/corrections_cash.json, costed through the package's CASH (forPayload()
 *     of it would cost the lineage at v4's long-run capital responses). Gate: CASH's payload is the file.
 *   - State prices with the lineage. The added people's state-price amount is the lineage's edit on the line (priced on
 *     their G3+ and white cells), not national_gap_bn x their key share. statePriced() therefore re-prices the union's
 *     part by the rule and scales the added people's own amount by their own amount on the evaluated key over theirs
 *     on the parent key [ASSUMPTION]. Gate: on the case's key it rebuilds the payload's line (1e-9).
 *   - A variant that picks another key (raw coding, uncompensated care at 0.7x use) moves the added people's own cells
 *     on that key, so the corrected model no longer moves as the uncorrected one does. The gate splits the move: the
 *     September 29 payload (P.SEPT29), evaluated at the case's specifications as a gate-only run, moves every
 *     specification as the uncorrected model does (1e-9, the old gate), and the case moves by that plus the lineage's
 *     own move, which is its edits on the variant's key less those on the case's key, times the line's response, plus
 *     the return on the capital keyed on that line (1e-9). The lineage's own move at the band ends goes to the JSON.
 *   - The added people's share of the engine keys the social rows scale with (meta.lineage_social_keys), at the band
 *     ends' specifications: the justice key of each end's footing, the uninsured-use key, the road key (hwy_sl's key on
 *     the evaluation), the consumption key, the K-12 operating key, the adults key and the head count. Each is the
 *     added people's amount over the union's (the September 29 payload's) on the same key. real_costs_totals.py
 *     prices the added people's social rows with them.
 *
 * Run from anywhere: node band_variants.cjs [--case sept24|sept26|sept26_schools|sept27|sept29|oct05] [--out-dir DIR]
 *   -> DIR/band_variants.csv, DIR/band_variants.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const CASES = {
  sept24: { lane: "main_case_2026_09_24", out: path.join(__dirname, "derived") },
  sept26: { lane: "main_case_2026_09_26", out: null },
  sept26_schools: { lane: "main_case_schools_full_2026_09_26",
    out: path.join(__dirname, "..", "sept26_propagation_2026_09_26", "derived") },
  sept27: { lane: "main_case_long_run_2026_09_27",
    out: path.join(__dirname, "..", "sept27_propagation_2026_09_27", "derived") },
  // cash: the cash set's payload, which the adopted lane's main_case.cjs reads from the candidate lane.
  sept29: { lane: "main_case_2026_09_29", out: path.join(__dirname, "derived", "sept29"),
    cash: "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json" },
  // cashPackage: the package that costs the cash set (default: the package's forPayload() of the cash payload).
  oct05: { lane: "main_case_2026_10_05", out: path.join(__dirname, "derived", "oct05"),
    cash: "main_case_2026_10_05/derived/corrections_cash.json", cashPackage: (pkg) => pkg.CASH },
};
const argv = process.argv.slice(2);
function opt(name, dflt) {
  const i = argv.indexOf(name);
  if (i < 0) return dflt;
  if (!argv[i + 1] || argv[i + 1].startsWith("--")) { console.error(`${name} needs a value`); process.exit(2); }
  return argv[i + 1];
}
const CASE = opt("--case", "sept27");
if (!CASES[CASE]) { console.error(`unknown --case ${CASE}; one of ${Object.keys(CASES).join(", ")}`); process.exit(2); }
const OUT = opt("--out-dir", null) ? path.resolve(opt("--out-dir")) : CASES[CASE].out;
if (!OUT) { console.error(`--case ${CASE} writes only to --out-dir DIR`); process.exit(2); }
const LANE = CASES[CASE].lane;
const LATER = CASE !== "sept24";

const P = require(path.join(__dirname, "..", LANE, "package.cjs"));
const P24 = P.P24 || P;  // the September 24 package, which the later packages import unchanged
const { Engine, MODEL, FISCAL, CONSTANTS, cost, span, csvRows, readJson } = P;

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
const near = (a, b, tol) => Math.abs(a - b) < tol;
// JSON with every object's keys sorted: specifications compare by value, whatever order built them.
const canon = (x) => JSON.stringify(x, (k, v) => (v && typeof v === "object" && !Array.isArray(v)
  ? Object.fromEntries(Object.keys(v).sort().map((kk) => [kk, v[kk]])) : v));
const f4 = (b) => `${b[0].toFixed(4)}–${b[1].toFixed(4)}`;
const sha = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");

const SOURCES = {
  corrections: "main_case_2026_09_24/derived/corrections.json",
  summary24: "main_case_2026_09_24/derived/summary.json",
  bands23: "main_case_2026_09_23/derived/main_case_bands.csv",
  justice: "cj_use_allocation_2026_09_23/derived/summary.json",
};
if (LATER) {
  Object.assign(SOURCES, { case_corrections: `${LANE}/derived/corrections.json`, case_summary: `${LANE}/derived/summary.json`,
    case_bands: `${LANE}/derived/main_case_bands.csv` });
}
if (CASES[CASE].cash) SOURCES.cash_corrections = CASES[CASE].cash;
const cj = readJson(SOURCES.justice);
const JUSTICE = { central: cj.central.change_bn, raw_coding: cj.one_at_a_time_change_bn.scaling_raw,
  grid_low: cj.range_change_bn[0], grid_high: cj.range_change_bn[1], cbp_fixed: cj.one_at_a_time_change_bn.cbp_zero };

// A target shift on one key of a line, in both allocations, national total conserved.
function shiftKey(m, lineId, key, delta) {
  const out = JSON.parse(JSON.stringify(m));
  const line = out.spending.lines.find((l) => l.id === lineId);
  if (!line || !line.keys[key]) throw new Error(`no key ${lineId}/${key}`);
  for (const a of ["personal", "shared"]) { line.keys[key][a].target_bn += delta; line.keys[key][a].other_bn -= delta; }
  return out;
}
const RAW = { justice: "use_raw_coding" };
const UC07 = { uc: { uninsured_use_low: "uninsured_use_07_low", uninsured_use_high: "uninsured_use_07_high" } };
function specsWith(specs, change) {
  return specs.map((s) => ({ ...s,
    ...(change.justice ? { justice: change.justice } : {}),
    ...(change.uc ? { uc: change.uc[s.uc] } : {}) }));
}
// State-priced correction lines (September 29 on; meta.state_pricing.lines on the model the payload corrected): each
// line's group amount is national_gap_bn x its parent's key share on the parent's evaluated key. statePriced(m,
// parent, key) re-prices the lines of that parent on `key` of model m, in both allocations; other residents' amount
// moves the other way, as a payload edit moves it. A model without such lines (every case before September 29, and
// every uncorrected model) comes back unchanged.
const JUSTICE_LINE = "public_order_safety";
// A model that carries the lineage (October 5 on; meta.lineage names its payload file): the lineage's edits, the case's
// or the cash set's. Every other model: null.
function lineageEditsOf(m) {
  const lin = m.corrections && m.corrections.lineage;
  if (!lin) return null;
  for (const pkg of [P, P.CASH]) if (pkg && pkg.LINEAGE_META && pkg.LINEAGE_META.payload === lin.payload) return pkg.LINEAGE_EDITS;
  throw new Error(`[BLOCKED] state pricing: no package has the lineage payload ${lin.payload}`);
}
const editsOn = (edits, line, key, a) => edits.filter((e) => e.side === "spending" && e.line === line && e.key === key).reduce((s, e) => s + e.by[a], 0);
function statePriced(m, parent, key) {
  const lines = ((m.corrections && m.corrections.state_pricing) || {}).lines || [];
  const mine = lines.filter((l) => l.parent === parent);
  if (!mine.length) return m;
  const out = JSON.parse(JSON.stringify(m));
  const p = out.spending.lines.find((l) => l.id === parent);
  if (!p || !p.keys[key]) throw new Error(`[BLOCKED] state pricing: no key ${parent}/${key}`);
  const L = lineageEditsOf(m);
  for (const sp of mine) {
    const line = out.spending.lines.find((l) => l.id === sp.line);
    if (!line || !line.keys.k || !Number.isFinite(sp.national_gap_bn)) throw new Error(`[BLOCKED] state pricing: unreadable line ${sp.line}`);
    for (const a of ["personal", "shared"]) {
      // With the lineage the rule prices the union's part; the added people keep their own state-price amount (the
      // lineage's edit on the line, priced on their G3+ and white cells), scaled by their own amount on the evaluated key
      // over theirs on the line's parent key [ASSUMPTION: their price gap per unit of justice service holds].
      const own = L ? (ln, k) => editsOn(L, ln, k, a) : null;
      const next = !L ? sp.national_gap_bn * p.keys[key][a].target_bn / p.national_bn
        : sp.national_gap_bn * (p.keys[key][a].target_bn - own(parent, key)) / p.national_bn + own(sp.line, "k") * own(parent, key) / own(parent, sp.parent_key);
      line.keys.k[a].other_bn -= next - line.keys.k[a].target_bn;
      line.keys.k[a].target_bn = next;
    }
  }
  return out;
}
// The justice variants re-price the state-priced justice line on the key they evaluate (the payload's rule).
const onKey = (key, change) => (m) => statePriced(change ? change(m) : m, JUSTICE_LINE, key);
const grid = (end) => (m) => shiftKey(m, "public_order_safety", "use", JUSTICE[end] - JUSTICE.central);
const VARIANTS = [
  // name, spec change, model change, September 23 row it must reproduce (null: none published)
  ["adopted", {}, null, "adopted"],
  ["justice_raw_coding", RAW, onKey(RAW.justice), "adopted_justice_raw_coding"],
  ["justice_grid_low", {}, onKey("use", grid("grid_low")), "adopted_justice_grid_low"],
  ["justice_grid_high", {}, onKey("use", grid("grid_high")), "adopted_justice_grid_high"],
  ["justice_cbp_fixed", {}, onKey("use", grid("cbp_fixed")), "adopted_justice_cbp_fixed"],
  ["uncompensated_use_0.7", UC07, null, "adopted_uncompensated_use_0.7"],
  ["justice_grid_low_and_uncompensated_use_0.7", UC07, onKey("use", grid("grid_low")), null],
];
// Beside a state-priced run, each justice variant with the justice line held at the case's key (the alternative).
const HELD = [
  ["justice_raw_coding", RAW, null],
  ["justice_grid_low", {}, grid("grid_low")],
  ["justice_grid_high", {}, grid("grid_high")],
  ["justice_cbp_fixed", {}, grid("cbp_fixed")],
  ["justice_grid_low_and_uncompensated_use_0.7", UC07, grid("grid_low")],
];

const published23 = {};
csvRows(SOURCES.bands23).filter((r) => r.profile === "cbo_category_lag_non_school_full")
  .forEach((r) => { published23[r.variant] = [Number(r.cost_low_bn), Number(r.cost_high_bn)]; });
const summary24 = readJson(SOURCES.summary24);
const corrected = Engine.applyCorrections(MODEL, readJson(SOURCES.corrections));

// Every line and receipt response in meta.responses at a reading, keyed as stateFor takes them: a receipt entry sets
// its override ("receipt:<id>"), an entry named for a spending line of the payload's model sets that line. On
// September 27 that is the two long-run lines, rental assistance and the enterprise receipt; on September 29 also
// v4's four receipt overrides and five correction lines. general_government is the specifications' gg; any other
// entry with a reading that names no line stops the run.
function lineResponsesAt(r, spendingIds, reading) {
  const out = {};
  for (const [id, e] of Object.entries(r)) {
    if (!e || typeof e !== "object" || id === "general_government") continue;
    if (e.receipt === true) {
      if (e.override !== `receipt:${id}`) throw new Error(`[BLOCKED] meta.responses.${id}: override ${e.override}`);
      out[e.override] = e[reading];
    } else if (spendingIds.has(id)) out[id] = e[reading];
    else if ("low" in e || "high" in e) throw new Error(`[BLOCKED] meta.responses.${id} has a reading but names no line`);
  }
  for (const [id, v] of Object.entries(out)) if (!Number.isFinite(v)) throw new Error(`[BLOCKED] meta.responses: ${id} has no ${reading} response`);
  return out;
}

// Runs: [name, model, specifications, cost function]. A later case's specifications are the September 24 ones with
// the responses of its meta.responses in place of 0.59/0.84 and 0.63/0.66, value for value.
const RUNS = [["sept23", MODEL, P24.MAIN_SPECS], ["sept24", corrected, P24.MAIN_SPECS]];
let payload = null, summary = null, published = null, cashPayload = null;
if (LATER) {
  console.log(`[${CASE}: ${LANE}]`);
  payload = readJson(SOURCES.case_corrections);
  summary = readJson(SOURCES.case_summary);
  const r = payload.meta.responses;
  const cap = payload.meta.capital_return || null;   // September 27 on
  gate("the payload's meta.responses equal the case's summary.json responses", JSON.stringify(r) === JSON.stringify(summary.responses));
  const spendingIds = new Set(MODEL.spending.lines.map((l) => l.id).concat((payload.lines || []).map((l) => l.id)));
  const specs = P24.MAIN_SPECS.map((s) => {
    const low = s.gg === P.GG24[0];
    const spec = { ...s, gg: low ? r.general_government.low : r.general_government.high,
      school: s.school === P.SCHOOL24[0] ? r.school.growth : r.school.decline };
    if (!cap) return spec;
    const reading = low ? "low" : "high";
    return { ...spec, reading, rate: cap.rates[reading], long_run: r[P.LR_LINES[0]].variant, enterprises: cap.enterprises,
      line_responses: lineResponsesAt(r, spendingIds, reading) };
  });
  gate("the specifications at meta.responses equal the package's MAIN_SPECS", canon(specs) === canon(P.MAIN_SPECS),
    `general government ${r.general_government.low}/${r.general_government.high}, schools ${r.school.growth}/${r.school.decline}` +
    (cap ? `; long-run lines, rental assistance, the enterprise receipt and the capital return (${cap.rates.low}/${cap.rates.high}, option ${cap.enterprises}) from meta` : ""));
  published = {};
  csvRows(SOURCES.case_bands).filter((x) => x.profile === P.MAIN_PROFILE)
    .forEach((x) => { published[x.variant] = [Number(x.cost_low_bn), Number(x.cost_high_bn)]; });
  const corrected = Engine.applyCorrections(MODEL, payload);
  RUNS.push([`${CASE}_uncorrected`, MODEL, specs], [CASE, corrected, specs]);
  if (cap) {
    // Beside the case, never in its band: the reported rate on every component, and option A. The package's
    // own switches build their specifications (main_case.cjs runs7 and optionARuns).
    const rate = cap.rates.reported;
    const specs7 = P.specsFor({ rates: { low: rate, high: rate } });
    gate(`the ${rate} specifications differ from the case's in the rate alone`,
      canon(specs7) === canon(specs.map((s) => ({ ...s, rate }))));
    RUNS.push([`${CASE}_capital_at_7pct`, corrected, specs7], [`${CASE}_enterprises_out_option_a`, corrected, P.specsFor({ enterprises: "A" })]);
  }
  const sp = (payload.meta.state_pricing || {}).lines || [];
  if (sp.length) {
    // The rule, read on the case's own key, rebuilds the payload's state-priced lines.
    const rebuilt = statePriced(corrected, JUSTICE_LINE, "use");
    let gap = 0;
    for (const l of sp.filter((x) => x.parent === JUSTICE_LINE)) {
      const [a, b] = [corrected, rebuilt].map((mm) => mm.spending.lines.find((x) => x.id === l.line).keys.k);
      for (const al of ["personal", "shared"]) gap = Math.max(gap, Math.abs(a[al].target_bn - b[al].target_bn), Math.abs(a[al].other_bn - b[al].other_bn));
    }
    gate(`state pricing: national_gap_bn x ${JUSTICE_LINE}'s use-key share rebuilds the payload's justice line (1e-9)`, gap < 1e-9,
      `${sp.filter((x) => x.parent === JUSTICE_LINE).map((x) => x.line).join(", ")}; max |diff| ${gap.toExponential(1)}`);
    const keyLines = new Set(P.componentsFor(null).flatMap((c) => [c.key.line, c.key.parent_line, c.key.correction_line,
      c.key.denominator_line, c.response.line].concat(c.key.numerator_lines || [])));
    gate("no capital component is keyed on, or responds as, a state-priced line", sp.every((l) => !keyLines.has(l.line)));
  }
  if (CASES[CASE].cash) {
    // Beside the case, never in its band: the cash set (the pension switch off), through the package's forPayload().
    cashPayload = readJson(SOURCES.cash_corrections);
    for (const k of ["responses", "capital_return", "state_pricing"]) {
      gate(`the cash set's payload has the case payload's meta.${k}`, JSON.stringify(cashPayload.meta[k]) === JSON.stringify(payload.meta[k]));
    }
    const PC = CASES[CASE].cashPackage ? CASES[CASE].cashPackage(P) : P.forPayload(cashPayload);
    if (CASES[CASE].cashPackage) gate("the package's cash set (CASH) has the cash set's payload, exactly", canon(PC.correctionsPayload()) === canon(cashPayload));
    gate("the cash set's specifications are the case's", canon(PC.MAIN_SPECS) === canon(specs));
    RUNS.push([`${CASE}_cash_set`, Engine.applyCorrections(MODEL, cashPayload), specs, PC.cost]);
  }
  if (payload.meta.lineage) {
    // October 5 on: the September 29 payload at the case's specifications, a gate-only run (never written). The case's
    // payload is it with the lineage's edits appended.
    const p29 = P.SEPT29.correctionsPayload(), n29 = p29.edits.length;
    gate("the case's payload is the September 29 payload with the lineage's edits appended (meta.lineage.edits)",
      canon(payload.edits.slice(0, n29)) === canon(p29.edits) && payload.edits.length === n29 + P.LINEAGE_EDITS.length
        && canon(payload.edits.slice(n29)) === canon(P.LINEAGE_EDITS) && payload.meta.lineage.edits.first === n29,
      `${n29} + ${P.LINEAGE_EDITS.length} edits`);
    RUNS.push([`${CASE}_sept29_payload`, Engine.applyCorrections(MODEL, p29), specs, null, true]);
  }
}

// The justice line's state-price re-pricing, one specification: the change in each state-priced line's group amount
// times its response. It is the whole of a re-priced variant's extra move when no capital component reads the line.
function repricing(base, m, spec) {
  const sp = ((base.corrections && base.corrections.state_pricing) || {}).lines || [];
  return sp.filter((l) => l.parent === JUSTICE_LINE).reduce((acc, l) => {
    const t = (mm) => mm.spending.lines.find((x) => x.id === l.line).keys.k[spec.allocation].target_bn;
    if (!Number.isFinite(spec.line_responses[l.line])) throw new Error(`[BLOCKED] no response for ${l.line}`);
    return acc + (t(m) - t(base)) * spec.line_responses[l.line];
  }, 0);
}
const hasStatePrice = (m) => (((m.corrections && m.corrections.state_pricing) || {}).lines || []).some((l) => l.parent === JUSTICE_LINE);

// October 5 on (meta.lineage). lineageBy: the lineage's edits on one spending cell, summed.
const lineageMoves = {};
let lineageKeys = null;
const lineageBy = (line, key, allocation) => P.LINEAGE_EDITS
  .filter((e) => e.side === "spending" && e.line === line && e.key === key).reduce((a, e) => a + e.by[allocation], 0);
// The lineage's own move under a variant at one specification, from its edits: for each line whose key the variant
// changes, the edits on the new key less those on the case's key, times the line's response and the fiscal weight; plus
// the return on each capital component whose key is lines over a national that reads the line (stock x rate x response
// x the key's move).
function lineageOwnMove(m5, modelChange, change, spec) {
  const [vs] = specsWith([spec], change);
  const a = P.evaluateFull(m5, spec), v = P.evaluateFull(modelChange ? modelChange(m5) : m5, vs);
  const fw = P.stateFor(P.withSyntheticLines(m5), spec, P.MAIN_PROFILE).fiscal_weight;
  const moved = {};
  let own = 0;
  for (const row of v.evaluation.spending) {
    const r0 = a.evaluation.spending.find((x) => x.id === row.id);
    if (row.key === r0.key) continue;
    if (row.response !== r0.response) throw new Error(`[BLOCKED] ${row.id}: the variant moves its response`);
    moved[row.id] = lineageBy(row.id, row.key, spec.allocation) - lineageBy(row.id, r0.key, spec.allocation);
    own += fw * row.response * moved[row.id];
  }
  const rules = new Map(P.componentsFor(spec.capital_variant).map((c) => [c.id, c.key]));
  for (const c of v.capital.components) {
    const k = rules.get(c.id);
    if (!k || k.kind !== "lines_amount_over_national") continue;
    const d = k.numerator_lines.reduce((acc, l) => acc + (moved[l] || 0), 0);
    if (!d) continue;
    own += c.stock_charged_bn * spec.rate * c.response * d / v.evaluation.spending.find((x) => x.id === k.denominator_line).national_bn;
  }
  return own;
}
// The added people's share of the keys the social rows scale with, at one specification: the lineage model's amount
// over the September 29 payload's, less 1, on each key at the specification's allocation (the road key is hwy_sl's on
// each evaluation; the consumption key is the general sales tax at the specification's receipt scenario).
function lineageSocialKeys(m5, m4, spec) {
  const cell = (m, line, key) => m.spending.lines.find((l) => l.id === line).keys[key][spec.allocation].target_bn;
  const ratio = (line, key) => cell(m5, line, key) / cell(m4, line, key) - 1;
  const road = (m) => P.evaluateFull(m, spec).capital.components.find((c) => c.id === "hwy_sl").key;
  const sc = P.stateFor(P.withSyntheticLines(m5), spec, P.MAIN_PROFILE).receipt_scenario;
  const rcell = (m) => m.receipts.lines.find((l) => l.id === "general_sales_tax").cells[sc][spec.allocation].target_bn;
  return { receipt_scenario: sc,
    justice_use: ratio("public_order_safety", "use"), justice_use_raw_coding: ratio("public_order_safety", "use_raw_coding"),
    uninsured_use: ratio("medicaid_and_chip_other_medical", spec.uc), road: road(m5) / road(m4) - 1,
    consumption: rcell(m5) / rcell(m4) - 1, pupils: ratio("education_services", "school_operating"),
    adults: ratio("public_order_safety", "adults") };
}

const rows = [];
const bands = {};
const perSpec = {};
const extra = {};   // a re-priced variant's move beyond its held alternative, by specification
for (const [caseName, base, specs, costOf, gateOnly] of RUNS) {
  console.log(`[${caseName}]${gateOnly ? " (gate only, not written)" : ""}`);
  const price = costOf || cost;
  for (const [name, change, modelChange, ref] of VARIANTS) {
    const m = modelChange ? modelChange(base) : base;
    const costs = specsWith(specs, change).map((s) => price(m, s));
    const b = span(costs);
    bands[`${caseName}|${name}`] = b;
    perSpec[`${caseName}|${name}`] = costs;
    if (!gateOnly) rows.push({ case: caseName, variant: name, low: b[0], high: b[1] });
    if (caseName === "sept23" && ref) {
      const want = published23[ref];
      gate(`${name} reproduces ${ref}`, near(b[0], want[0], 1e-4) && near(b[1], want[1], 1e-4), `${f4(b)} vs ${f4(want)}`);
    } else {
      console.log(`  ${name.padEnd(44)} ${f4(b)}`);
    }
    if (hasStatePrice(base) && modelChange) extra[`${caseName}|${name}`] = specsWith(specs, change).map((s) => repricing(base, m, s));
  }
  if (!hasStatePrice(base)) continue;
  for (const [name, change, modelChange] of HELD) {
    const m = modelChange ? modelChange(base) : base;
    const costs = specsWith(specs, change).map((s) => price(m, s));
    const b = span(costs), held = `${name}_state_price_held`;
    bands[`${caseName}|${held}`] = b;
    perSpec[`${caseName}|${held}`] = costs;
    if (!gateOnly) rows.push({ case: caseName, variant: held, low: b[0], high: b[1] });
    console.log(`  ${held.padEnd(44)} ${f4(b)}`);
    const gap = Math.max(...costs.map((x, i) => Math.abs(perSpec[`${caseName}|${name}`][i] - x - extra[`${caseName}|${name}`][i])));
    gate(`${caseName}: ${name} re-priced less held is the justice line's re-pricing alone, at every specification (1e-9)`, gap < 1e-9,
      `max |diff| ${gap.toExponential(1)}`);
  }
}
const a24 = bands["sept24|adopted"];
gate("corrected model reproduces the adopted September 24 band (summary.json)",
  near(a24[0], summary24.main_case[0], 1e-9) && near(a24[1], summary24.main_case[1], 1e-9), `${f4(a24)}`);
const shift = (c) => [0, 1].map((i) => bands[`${c}|justice_raw_coding`][i] - bands[`${c}|adopted`][i]);
const [s23, s24] = [shift("sept23"), shift("sept24")];
gate("the payload moves raw coding and use by the same amount", near(s23[0], s24[0], 1e-9) && near(s23[1], s24[1], 1e-9),
  `${s23.map((x) => x.toFixed(6)).join(" / ")} vs ${s24.map((x) => x.toFixed(6)).join(" / ")}`);
if (LATER) {
  const [unc, cor] = [`${CASE}_uncorrected`, CASE];
  for (const [run, key, label] of [[cor, "main_case", "adopted"], [unc, "uncorrected_at_adopted_responses", "uncorrected_at_adopted_responses"]]) {
    const b = bands[`${run}|adopted`];
    gate(`${run} reproduces ${LANE} ${key} (summary.json, 1e-9)`, near(b[0], summary[key][0], 1e-9) && near(b[1], summary[key][1], 1e-9), f4(b));
    gate(`${run} reproduces ${LANE} main_case_bands.csv ${label} (1e-4)`,
      near(b[0], published[label][0], 1e-4) && near(b[1], published[label][1], 1e-4), `${f4(b)} vs ${f4(published[label])}`);
  }
  const L29 = payload.meta.lineage ? `${CASE}_sept29_payload` : null;
  const [, m5, specs5] = RUNS.find((r) => r[0] === cor);
  for (const [name, change, modelChange] of VARIANTS.slice(1)) {
    // A re-priced justice variant moves the corrected model by its state-price re-pricing more (September 29 on).
    const move = (run) => perSpec[`${run}|${name}`].map((x, i) => x - perSpec[`${run}|adopted`][i] - ((extra[`${run}|${name}`] || [])[i] || 0));
    const [mu, mc] = [move(unc), move(cor)];
    const beyond = extra[`${cor}|${name}`] ? ", beyond the justice line's state-price re-pricing" : "";
    if (!L29) {
      const gap = Math.max(...mu.map((x, i) => Math.abs(x - mc[i])));
      gate(`${name} moves every specification by the same amount on the uncorrected and corrected ${CASE} model` + beyond, gap < 1e-9, `max gap ${gap.toExponential(1)}`);
      continue;
    }
    // October 5 on: the September 29 payload moves as the uncorrected model does; the lineage adds its own cells' move.
    const m29 = move(L29);
    const gap29 = Math.max(...mu.map((x, i) => Math.abs(x - m29[i])));
    gate(`${name} moves every specification by the same amount on the uncorrected model and the September 29 payload at the ${CASE} specifications` + beyond,
      gap29 < 1e-9, `max gap ${gap29.toExponential(1)}`);
    const own = specs5.map((s) => lineageOwnMove(m5, modelChange, change, s));
    const gapL = Math.max(...mc.map((x, i) => Math.abs(x - m29[i] - own[i])));
    gate(`${name} moves the ${CASE} model by that plus the lineage's own move: its edits on the variant's key less the case's key, times the response, and the capital keyed on that line (1e-9)`,
      gapL < 1e-9, `max gap ${gapL.toExponential(1)}; own move ${Math.min(...own).toFixed(4)} to ${Math.max(...own).toFixed(4)}bn`);
    lineageMoves[name] = own;
  }
  if (L29) {
    // The band ends of the case, and the added people's share of the social rows' keys there.
    const costs = perSpec[`${cor}|adopted`];
    const lo = costs.indexOf(Math.min(...costs)), hi = costs.indexOf(Math.max(...costs));
    const ends = summary.end_specifications;
    gate(`the ${CASE} band's end specifications are the case's in both fill-in methods (summary.json end_specifications)`,
      Array.isArray(ends) && ends.length === 2 && ends.every((e) => e.low_end.index === lo && e.high_end.index === hi), `${lo} / ${hi}`);
    const m29model = RUNS.find((r) => r[0] === L29)[1];
    const c = payload.meta.lineage.counts;
    lineageKeys = { rule: "the added people's amount over the union's (the September 29 payload's) on the key a social row scales with, at the band end's specification",
      head_count: c.added / c.account_union };
    for (const [end, i] of [["low_end", lo], ["high_end", hi]]) {
      lineageKeys[end] = Object.assign({ specification: i, allocation: specs5[i].allocation, uc: specs5[i].uc, justice: specs5[i].justice },
        lineageSocialKeys(m5, m29model, specs5[i]));
    }
    for (const [name, own] of Object.entries(lineageMoves)) lineageMoves[name] = { low_end_bn: own[lo], high_end_bn: own[hi], range_bn: [Math.min(...own), Math.max(...own)] };
  }
  if (cashPayload) {
    const b = bands[`${CASE}_cash_set|adopted`], want = summary.cash_set.band_bn;
    gate(`${CASE}_cash_set reproduces ${LANE} cash_set (summary.json, 1e-9)`, near(b[0], want[0], 1e-9) && near(b[1], want[1], 1e-9), f4(b));
    gate(`${CASE}_cash_set reproduces ${LANE} main_case_bands.csv cash_set (1e-4)`,
      near(b[0], published.cash_set[0], 1e-4) && near(b[1], published.cash_set[1], 1e-4), `${f4(b)} vs ${f4(published.cash_set)}`);
  }
  if (payload.meta.capital_return) {
    for (const [run, key, row] of [[`${CASE}_capital_at_7pct`, "rate_7pct", "capital_return_at_7pct"],
      [`${CASE}_enterprises_out_option_a`, "enterprises_out_option_A", "enterprises_out_option_a"]]) {
      const b = bands[`${run}|adopted`], want = summary.beside_the_account[key].band_bn;
      gate(`${run} reproduces ${LANE} beside_the_account.${key} (summary.json, 1e-9)`, near(b[0], want[0], 1e-9) && near(b[1], want[1], 1e-9), f4(b));
      gate(`${run} reproduces ${LANE} main_case_bands.csv ${row} (1e-4)`,
        near(b[0], published[row][0], 1e-4) && near(b[1], published[row][1], 1e-4), `${f4(b)} vs ${f4(published[row])}`);
    }
  }
}

if (failures) { console.error(`${failures} gate(s) failed; nothing written`); process.exit(1); }
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "band_variants.csv"), ["case,variant,cost_low_bn,cost_high_bn"]
  .concat(rows.map((r) => [r.case, r.variant, r.low.toPrecision(15), r.high.toPrecision(15)].join(","))).join("\n") + "\n");
const meta = { profile: P.MAIN_PROFILE, specifications: P.MAIN_SPECS.length, target_population: MODEL.meta.target_population,
  care_constant_bn: CONSTANTS.care.c, justice_changes_bn: JUSTICE };
if (LATER) {
  Object.assign(meta, { case: CASE, package: `${LANE}/package.cjs`, responses: payload.meta.responses,
    runs: { sept23: "uncorrected model at 0.59/0.84 and 0.63/0.66 (the September 23 case)",
      sept24: "main_case_2026_09_24 corrections at 0.59/0.84 and 0.63/0.66",
      [`${CASE}_uncorrected`]: "uncorrected model at the responses in the payload's meta.responses",
      [CASE]: `${LANE} corrections at the responses in the payload's meta.responses` } });
  if (payload.meta.capital_return) {
    Object.assign(meta.runs, {
      [CASE]: `${LANE} corrections at the responses in meta.responses, plus the return on public capital in meta.capital_return (package evaluateFull)`,
      [`${CASE}_uncorrected`]: "uncorrected model at the responses in meta.responses, plus the return on public capital keyed on its own evaluation",
      [`${CASE}_capital_at_7pct`]: `beside the case, never in its band: the return at the reported ${payload.meta.capital_return.rates.reported} on every component (package specsFor rates)`,
      [`${CASE}_enterprises_out_option_a`]: "beside the case, never in its band: option A, no enterprise capital and the enterprise_surplus receipt at 0 (package specsFor enterprises A)" });
    meta.capital_return = { rates: payload.meta.capital_return.rates, enterprises: payload.meta.capital_return.enterprises };
  }
  if (hasStatePrice(Engine.applyCorrections(MODEL, payload))) {
    meta.state_price_justice = {
      rule: `each justice variant re-prices the state-priced correction line of ${JUSTICE_LINE} on the key it evaluates: national_gap_bn x the parent's target on that key over its national total (meta.state_pricing.rule, "on its evaluated key"); raw coding on use_raw_coding, the grid ends and CBP held fixed on the shifted use key`,
      alternative: "<variant>_state_price_held: the line held at the case's use-key amount",
      lines: payload.meta.state_pricing.lines.filter((l) => l.parent === JUSTICE_LINE) };
  }
  if (cashPayload) {
    meta.runs[`${CASE}_cash_set`] = `beside the case, never in its band: the cash set (the pension switch off), ${CASES[CASE].cash}, which ${LANE}/main_case.cjs ` +
      (CASES[CASE].cashPackage ? "writes, costed through the package's CASH" : "reads, costed through the package's forPayload() of it");
  }
  if (lineageKeys) {
    meta.lineage = {
      counts: payload.meta.lineage.counts, arm: payload.meta.lineage.arm, counting: payload.meta.lineage.counting.rule,
      gate_only_run: `${CASE}_sept29_payload: the September 29 payload (P.SEPT29) at the case's specifications, never written`,
      variant_rule: "a variant that picks another key moves the case by the September 29 payload's move (the uncorrected model's) plus the lineage's own move: its edits on the variant's key less the case's key, times the line's response, plus the capital keyed on the line",
      own_move_bn: lineageMoves };
    meta.lineage_social_keys = lineageKeys;
  }
}
meta.sources_sha256 =Object.fromEntries(Object.values(SOURCES).map((rel) => [rel, sha(rel)]));
fs.writeFileSync(path.join(OUT, "band_variants.json"), JSON.stringify(meta, null, 1) + "\n");
console.log(`all gates passed; ${rows.length} bands -> ${path.relative(process.cwd(), path.join(OUT, "band_variants.csv"))}`);
