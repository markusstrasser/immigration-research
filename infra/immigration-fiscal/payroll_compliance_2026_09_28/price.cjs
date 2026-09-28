/* Price the payroll-compliance items in the adopted September 27 case at specifications 48 and 11 (the band's
 * ends), with both fill-in methods averaged.
 *
 * Item A is audit row 2, already in the case: the case against the same stack without the audit's rules
 * (`row4+status_state_aware|alone|<method>`, the CPS lane's full cache) and against the on-books lane's low and
 * high shares (the package's own low and high stacks). Every other item (compliance.py, derived/items.json) moves
 * each receipt line's group amount on the reference incidence rule by (r - 1) x that amount, expanded to the other
 * executed rules as every receipt shift is (the package's expand()), and applied with the engine's
 * applyCorrections, which moves other residents' amount by the opposite: national totals hold. An item is applied
 * to the package's model for its row2_case (the combined item's ends sit on the low and high stacks).
 *
 * Each item is priced four ways: with r, this lane's rule (CBO's between-group distribution fixed, the item moving
 * the group's shares inside CBO's income groups); with r_raw, the ratio of raw shares, which is how the package
 * carries a stack through CBO's re-key (cboShifts scales it by the stack's factor); and each calibrated to the
 * case's flag, weights and keys (r_cal, r_cal_raw; compliance.py, derived/calibration.csv). row2_r_route prices row
 * 2 itself every way, for comparison with the package's stacks.
 *
 * Gates, each stopping with [BLOCKED] before anything is written:
 *   - the package reproduces the adopted band (main_case_long_run_2026_09_27/derived/summary.json) at 48 and 11,
 *     and the probe's replica (engine state plus capital return) equals evaluateFull;
 *   - the 64 specifications hold 32 distinct costs, 48 = 52 and 11 = 15, and the band's ends are 48 and 11;
 *   - the vendored central stacks equal the CPS lane's full cache, and a model built here from a stack payload
 *     costs what the package's modelFor costs;
 *   - every item edit holds national totals: in each executed receipt cell the group's amount moves by `by` and
 *     other residents' by -`by`, and each line's national total is unchanged;
 *   - items.json was built for the package's fill-in methods, and the calibrated raw route for row 2 removed moves
 *     the direct receipts at 48 and 11 as the package's own stacks do, within 2%.
 *
 *     node infra/immigration-fiscal/payroll_compliance_2026_09_28/price.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const HERE = __dirname;
const FISCAL = path.resolve(HERE, "..");
const P = require(path.join(FISCAL, "main_case_long_run_2026_09_27", "package.cjs"));
const { Engine, MODEL, METHODS, ALLOCS, STACKS, P26, MAIN_SPECS, MAIN_PROFILE, stateFor, capitalReturn, evaluateFull,
  modelFor, withCentral, expand, rekeyEdits } = P;

const OUT = path.join(HERE, "derived");
const ITEMS = JSON.parse(fs.readFileSync(path.join(OUT, "items.json"), "utf8"));
const SUMMARY = path.join(FISCAL, "main_case_long_run_2026_09_27", "derived", "summary.json");
const FULL = path.join(FISCAL, "cps_imputation_keys_2026_09_23", "_cache", "onbooks_lane_line_deltas.json");
const VENDORED = path.join(FISCAL, "main_case_2026_09_24", "derived", "stack_line_deltas.json");
const END = { low: 48, high: 11 };
const REF = MODEL.receipts.reference;
const sha = (p) => crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const mean = (a) => a.reduce((x, y) => x + y, 0) / a.length;
const rel = (p) => path.relative(path.resolve(FISCAL, "..", ".."), p);

const gates = [];
function gate(name, ok, detail) { gates.push({ gate: name, pass: Boolean(ok), detail }); }
function stop() {
  const failed = gates.filter((g) => !g.pass);
  if (!failed.length) return;
  for (const g of failed) console.log(`[BLOCKED] gate ${g.gate}: ${g.detail}`);
  process.exit(1);
}

// ------------------------------------------------------------------------------------------ the case
const oo = withCentral({});
function modelFromPayload(payload, method) {
  const m = P26.build(P26.packageShifts(payload, "central", method, oo), oo);
  return oo.enterprise_rekey ? Engine.applyCorrections(m, { lines: [], edits: rekeyEdits(m) }) : m;
}
const cost = (m, i) => evaluateFull(m, MAIN_SPECS[i], MAIN_PROFILE).cost_bn;
function costWith(model, spec, overrides) {
  const state = stateFor(model, spec, MAIN_PROFILE);
  state.response_override = Object.assign({}, state.response_override, overrides);
  const evaluation = Engine.evaluate(model, state);
  return -evaluation.welfare_bn + capitalReturn(evaluation, spec).total_bn;
}
const models = Object.fromEntries(METHODS.map((m) => [m, modelFor("central", m, oo)]));
const adopted = JSON.parse(fs.readFileSync(SUMMARY, "utf8")).main_case;
const at = (ms, i) => mean(METHODS.map((m) => cost(ms[m], i)));
const c48 = at(models, END.low), c11 = at(models, END.high);
const replica = [END.low, END.high].map((i) => mean(METHODS.map((m) => costWith(models[m], MAIN_SPECS[i], {}))));
gate("package_reproduces_the_adopted_band", Math.abs(c48 - adopted[0]) < 1e-9 && Math.abs(c11 - adopted[1]) < 1e-9
  && Math.abs(replica[0] - c48) < 1e-9 && Math.abs(replica[1] - c11) < 1e-9,
  `specification 48 ${c48.toFixed(6)} and 11 ${c11.toFixed(6)} ($bn, fill-in methods averaged) against summary.json ` +
  `${adopted.map((x) => x.toFixed(6)).join(" / ")}; the probe's replica ${replica.map((x) => x.toFixed(6)).join(" / ")}`);
const all64 = MAIN_SPECS.map((_, i) => at(models, i));
const distinct = new Set(all64.map((x) => x.toFixed(9)));
const lo = all64.indexOf(Math.min(...all64)), hi = all64.indexOf(Math.max(...all64));
gate("specifications_hold_32_distinct_costs", distinct.size === 32 && Math.abs(all64[48] - all64[52]) < 1e-9
  && Math.abs(all64[11] - all64[15]) < 1e-9 && all64[lo] === all64[48] && all64[hi] === all64[11],
  `${distinct.size} distinct costs over ${all64.length} specifications; the band's ends are specifications ${lo} and ${hi}` +
  ` (48 = 52: ${all64[52].toFixed(6)}; 11 = 15: ${all64[15].toFixed(6)}); allocations ${MAIN_SPECS[48].allocation} / ` +
  `${MAIN_SPECS[11].allocation}`);
const full = JSON.parse(fs.readFileSync(FULL, "utf8"));
const vend = JSON.parse(fs.readFileSync(VENDORED, "utf8"));
const same = ["low", "central", "high"].every((c) => METHODS.every((m) =>
  JSON.stringify(STACKS[`row4+status_state_aware|${c}|${m}`]) === JSON.stringify(full[`row4+status_state_aware|${c}|${m}`])));
const rebuilt = METHODS.map((m) => [END.low, END.high].map((i) => cost(modelFromPayload(STACKS[`row4+status_state_aware|central|${m}`], m), i)));
gate("stacks_are_the_cps_lanes_and_models_rebuild", same && vend.source_sha256 === sha(FULL)
  && METHODS.every((m, k) => Math.abs(rebuilt[k][0] - cost(models[m], END.low)) < 1e-9
    && Math.abs(rebuilt[k][1] - cost(models[m], END.high)) < 1e-9),
  `the vendored low, central and high stacks equal ${rel(FULL)} (sha256 ${sha(FULL).slice(0, 12)}, the vendored copy's ` +
  `recorded source); a model built from the central payload costs what modelFor costs at 48 and 11`);
stop();

// ------------------------------------------------------------------------------------------ helpers
const receiptLines = Object.keys(ITEMS.items.all.central.lines);
function amounts(ms, i) {
  // The group's amount on each receipt line at a specification, fill-in methods averaged.
  const spec = MAIN_SPECS[i];
  const per = METHODS.map((m) => Object.fromEntries(evaluateFull(ms[m], spec, MAIN_PROFILE).evaluation.receipts
    .map((r) => [r.id, r.amount_bn])));
  return Object.fromEntries(Object.keys(per[0]).map((id) => [id, mean(per.map((x) => x[id]))]));
}
function withItem(base, lines, field) {
  // Receipt shifts of (r - 1) x the group's reference amount, expanded to every executed rule, applied.
  const shifts = Object.entries(lines).map(([id, byA]) => {
    const cell = base.receipts.lines.find((l) => l.id === id).cells[REF];
    return { side: "receipt", line: id, by: Object.fromEntries(ALLOCS.map((a) => [a, (byA[a][field] - 1) * cell[a].target_bn])) };
  });
  const edits = expand(shifts);
  const m = Engine.applyCorrections(base, { lines: [], edits });
  // National totals hold: each edited cell's group amount moves by `by` and other residents' by -`by`.
  let worst = 0;
  for (const e of edits) {
    const b = base.receipts.lines.find((l) => l.id === e.line), a = m.receipts.lines.find((l) => l.id === e.line);
    worst = Math.max(worst, Math.abs(a.national_bn - b.national_bn));
    for (const al of ALLOCS) {
      const cb = b.cells[e.scenario][al], ca = a.cells[e.scenario][al];
      worst = Math.max(worst, Math.abs(ca.target_bn - cb.target_bn - e.by[al]), Math.abs(ca.other_bn - cb.other_bn + e.by[al]),
        Math.abs(ca.target_bn + ca.other_bn - cb.target_bn - cb.other_bn));
    }
  }
  return { m, worst, edits: edits.length };
}

// ------------------------------------------------------------------------------------------ pricing
const base48 = amounts(models, END.low), base11 = amounts(models, END.high);
const rows = [];
const lineRows = [];
function record(item, variant, rule, row2Case, ms, note) {
  const k48 = at(ms, END.low), k11 = at(ms, END.high);
  const costs = MAIN_SPECS.map((_, i) => at(ms, i));
  const a48 = amounts(ms, END.low), a11 = amounts(ms, END.high);
  rows.push({ item, variant, rule, row2_case: row2Case, cost_48_bn: k48, cost_11_bn: k11, change_48_bn: k48 - c48,
    change_11_bn: k11 - c11, band_min_bn: Math.min(...costs), band_max_bn: Math.max(...costs),
    distinct_specifications: new Set(costs.map((x) => x.toFixed(9))).size, note });
  for (const id of receiptLines) {
    lineRows.push({ item, variant, rule, line: id, group_48_bn: a48[id], change_48_bn: a48[id] - base48[id],
      group_11_bn: a11[id], change_11_bn: a11[id] - base11[id] });
  }
}
record("case", "adopted", "package", "central", models, "the adopted case");
// Item A: audit row 2, already in the case.
const alone = Object.fromEntries(METHODS.map((m) => [m, modelFromPayload(full[`row4+status_state_aware|alone|${m}`], m)]));
record("row2", "without", "package", "alone", alone,
  "the same stack without the audit's rules: full compliance for the imputed unauthorized");
const caseModels = { central: models };
for (const c of ["low", "high"]) {
  caseModels[c] = Object.fromEntries(METHODS.map((m) => [m, modelFor(c, m, oo)]));
  record("row2", c, "package", c, caseModels[c], `the on-books lane's ${c} shares`);
}
// Items from compliance.py, by this lane's rule (r) and by the package's stack convention (r_raw).
const RULES = { r: "theta", r_raw: "stack_factor", r_cal: "theta_calibrated", r_cal_raw: "stack_factor_calibrated" };
gate("items_built_for_the_package_methods", JSON.stringify(ITEMS.meta.methods) === JSON.stringify(METHODS),
  `items.json methods ${(ITEMS.meta.methods || ["none recorded"]).join(", ")}; the package's ${METHODS.join(", ")}`);
stop();
let worst = 0, nEdits = 0;
for (const [item, variants] of Object.entries(ITEMS.items)) {
  for (const [variant, v] of Object.entries(variants)) {
    for (const [field, rule] of Object.entries(RULES)) {
      const ms = {};
      for (const m of METHODS) {
        const x = withItem(caseModels[v.row2_case][m], v.lines, field);
        ms[m] = x.m;
        worst = Math.max(worst, x.worst);
        nEdits += x.edits;
      }
      record(item, variant, rule, v.row2_case, ms, "");
    }
  }
}
gate("item_edits_hold_national_totals", worst < 1e-9,
  `${nEdits} receipt-cell edits over every item, variant and fill-in method; the largest departure of group + other ` +
  `from its value before the edit, or of the moves from +by / -by, is ${worst.toExponential(1)}bn`);
const direct = new Set(MODEL.receipts.lines.filter((l) => l.cells[REF].shared.direct).map((l) => l.id));
const receiptsMoved = (item, variant, rule, col) => lineRows.filter((r) => r.item === item && r.variant === variant
  && r.rule === rule && direct.has(r.line)).reduce((x, r) => x + r[col], 0);
const cmp = ["change_48_bn", "change_11_bn"].map((col) => [receiptsMoved("row2", "without", "package", col),
  receiptsMoved("row2_r_route", "without", "stack_factor_calibrated", col)]);
gate("calibrated_route_reproduces_row_2", cmp.every(([a, b]) => Math.abs(b / a - 1) < 0.02),
  `direct receipts moved by removing row 2, package stacks against this lane's calibrated raw route: ` +
  cmp.map(([a, b]) => `${a.toFixed(3)} / ${b.toFixed(3)}`).join(" at 48, ") + " at 11 ($bn)");
stop();

// ------------------------------------------------------------------------------------------ outputs
const csv = (rs, cols) => [cols.join(",")].concat(rs.map((r) => cols.map((c) => {
  const v = r[c];
  if (typeof v === "number") return Number.isInteger(v) ? String(v) : v.toFixed(6);
  return /[",]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v);
}).join(","))).join("\n") + "\n";
fs.writeFileSync(path.join(OUT, "pricing.csv"), csv(rows, ["item", "variant", "rule", "row2_case", "cost_48_bn", "cost_11_bn",
  "change_48_bn", "change_11_bn", "band_min_bn", "band_max_bn", "distinct_specifications", "note"]));
fs.writeFileSync(path.join(OUT, "pricing_lines.csv"), csv(lineRows, ["item", "variant", "rule", "line", "group_48_bn",
  "change_48_bn", "group_11_bn", "change_11_bn"]));
const modelAmounts = Object.fromEntries(MODEL.receipts.lines.filter((l) => receiptLines.includes(l.id)).map((l) =>
  [l.id, { key: l.cells[REF].shared.key, national_bn: l.national_bn, direct: l.cells[REF].shared.direct,
    model_json_shared_bn: l.cells[REF].shared.target_bn, model_json_personal_bn: l.cells[REF].personal.target_bn }]));
fs.writeFileSync(path.join(OUT, "pricing.json"), JSON.stringify({
  gates, specifications: { low_end: END.low, high_end: END.high, low_allocation: MAIN_SPECS[END.low].allocation,
    high_allocation: MAIN_SPECS[END.high].allocation },
  inputs: { items: sha(path.join(OUT, "items.json")), summary: sha(SUMMARY), full_cache: sha(FULL), vendored: sha(VENDORED) },
  model_json_lines: modelAmounts, rows }, null, 1) + "\n");
for (const g of gates) console.log(`  ✓ ${g.gate}: ${g.detail.slice(0, 160)}`);
for (const r of rows) {
  console.log(`${(r.item + " " + r.variant + " " + r.rule).padEnd(44)} ${r.cost_48_bn.toFixed(2)} / ${r.cost_11_bn.toFixed(2)}  ` +
    `(${r.change_48_bn >= 0 ? "+" : ""}${r.change_48_bn.toFixed(2)} / ${r.change_11_bn >= 0 ? "+" : ""}${r.change_11_bn.toFixed(2)})`);
}
