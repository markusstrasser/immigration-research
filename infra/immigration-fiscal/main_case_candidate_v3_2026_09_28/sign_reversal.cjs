/* The sign-reversal figures of candidate v3 (sept28_candidate_v3), with the pension switch off and on, beside the
 * September 27 case's and candidate v2's, re-derived.
 *
 * The definition is main_case_2026_09_24/sign_reversal.cjs's, imported and run unchanged: ordinary service budgets
 * respond at a common share s (roads and parks included, so s replaces their long-run responses), defense and existing
 * interest stay fixed, general government responds at its adopted response whatever s is, transfers and direct receipts
 * respond fully; CBO incidence rules and preferred keys. The break-even share is w(0) / (w(0) - w(1)) over the whole
 * production grid with private capital adjusted; the frozen-services row holds private capital fixed.
 *
 * The September 27 case's additions enter inside the definition's engine evaluation as in v2's sign_reversal.cjs
 * (withCase, re-implemented here, since the adopted script runs and writes when it is loaded): rental assistance at 1,
 * the enterprise receipt at 1 (or s in the __enterprises_at_s rows), and the return on public capital from the same
 * evaluation, 2% at the least adverse end and 3% at the most adverse. v3 adds to that list: the split-out transit
 * deficit is an enterprise receipt, so it responds with the enterprise receipt (1, or s), as v2's housing line does; the
 * property items' receipt responses are long-run responses, fixed whatever s the service budgets take (the receipt-side
 * lane's sign_reversal.cjs); and the capital return re-keys public housing's and transit's capital as the package does.
 *
 * Models, each the September 27 payload (its committed corrections.json) with items: v2 (as v2's sign_reversal.cjs builds
 * it), the candidate (v2 plus items 5-8, each applied with package.cjs's own functions on the payload model, whose
 * amounts are the two fill-in methods' mean) and the candidate with the pension switch on. The road arm does not enter,
 * nor does item 10 (uninsured use at 0.7x, a switch): the definition's end pairs fix the Medicaid line's uc key.
 *
 * Gates: the September 27 and v2 columns reproduce v2's committed sign_reversal.csv (1e-4); each model at the adopted
 * responses gives the package's band for its options (1e-9); at s = 1 the wrapped definition is the proportional
 * reference on the candidate at every specification, switch off and on (welfare 1e-9, capital 1e-12); welfare is linear
 * in s. Exit 1 and nothing written on failure.
 * Run from anywhere: node sign_reversal.cjs [--out-dir DIR] -> derived/sign_reversal.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const C = require("./package.cjs");
const S24 = require(path.join(__dirname, "..", "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, HERE, ALLOCS, METHODS, RENTAL, RATES, RESPONSES, ENTERPRISES, ENTERPRISE_RECEIPT, HOUSING_LINE, HOUSING_RECEIPT,
  TRANSIT_LINE, TRANSIT_RECEIPT, TAX_LINE, TRANSFERS, PROPERTY_READINGS, OFF, V2SET, CANDIDATE, ACCRUAL, gate, near, gateState, csvRows,
  readJson, withProduction, splitHousing, taxEditOf, payrollShifts, withWorkersComp, splitTransit, withPension, rekeyCapital, v3Part,
  specsFor, withCentral, bandFor, central, evaluateFull, RS } = C;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const PAYLOAD_FILE = "main_case_long_run_2026_09_27/derived/corrections.json";
const payload27 = readJson(PAYLOAD_FILE);
const model27 = Engine.applyCorrections(MODEL, payload27);
const T = TRANSFERS.public_housing_operating.bn;
// Item 3 on the payload model: the methods' edits averaged, expanded to every incidence rule (v2's sign_reversal.cjs).
const taxBy = Object.fromEntries(ALLOCS.map((a) => [a, METHODS.reduce((s, meth) => s + taxEditOf("central", meth, "irs_2023_raked")[a], 0) / METHODS.length]));
// The payload model with an option set's items, built with the package's functions in modelFor's order.
function build(o) {
  const oo = withCentral(o);
  let m = withProduction(model27, oo.production);
  if (oo.housing === "tenants") m = splitHousing(m, TRANSFERS[oo.internal_transfer].bn);
  if (oo.tax_key === "irs_2023_raked") m = Engine.applyCorrections(m, { lines: [], edits: C.expand([{ side: "receipt", line: TAX_LINE, by: taxBy }]) });
  if (oo.property === "long_run") m = RS.itemModel(m, PROPERTY_READINGS[oo.property_reading]);
  const shifts = payrollShifts(m, "central", oo);
  if (shifts.length) m = Engine.applyCorrections(m, { lines: [], edits: C.expand(shifts), meta: m.corrections });
  if (oo.workers_comp === "pooled_2019_2024") m = withWorkersComp(m);
  if (oo.transit !== "population") m = splitTransit(m, C.TRANSIT_RU[oo.transit]);
  if (oo.pension === "accrual") m = withPension(m);
  return { oo, model: Object.assign({}, m, { candidate: { production: oo.production, housing: oo.housing, tax_key: oo.tax_key, v3: v3Part(oo) } }) };
}
const MODELS = { sept27: build(OFF), v2: build(V2SET), candidate: build(CANDIDATE), accrual: build(ACCRUAL) };
const GG = RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG.low : GG.high }));
const readingOf = (g) => (g === GG.low ? "low" : g === GG.high ? "high" : null);
const VARIANTS = ["enterprises_at_1", "enterprises_at_s"];

// The September 27 case inside the imported definition (v2's withCase, with v3's lines, receipt responses and capital).
let last = null;
function withCase(variant, f) {
  if (!VARIANTS.includes(variant)) throw new Error("unknown variant " + variant);
  const evaluate = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response;
    const reading = readingOf(st.general_government_response);
    if (!reading) throw new Error(`[BLOCKED] general government at ${st.general_government_response}, neither adopted response`);
    const v3 = m.candidate && m.candidate.v3;
    if (!v3) throw new Error("[BLOCKED] a model without v3's options");
    const atS = variant === "enterprises_at_s";
    const extra = { [RENTAL]: 1, [ENTERPRISE_RECEIPT]: atS ? s : 1 };
    if (m.receipts.lines.some((l) => l.id === HOUSING_LINE)) extra[HOUSING_RECEIPT] = atS ? s : 1;
    if (m.receipts.lines.some((l) => l.id === TRANSIT_LINE)) extra[TRANSIT_RECEIPT] = atS ? s : 1;
    if (v3.property === "long_run") Object.assign(extra, RS.itemOverrides(PROPERTY_READINGS[v3.property_reading]));
    const ev = evaluate(m, Object.assign({}, st, { response_override: Object.assign({}, st.response_override, extra) }));
    const spec = Object.assign({ share: st.school_share, reading, rate: RATES[reading], enterprises: ENTERPRISES, long_run: null }, v3);
    const cap = rekeyCapital({ evaluation: ev, capital: C.capitalReturn(ev, spec) }, spec);
    const enterprise = cap.components.filter((c) => c.group === "enterprise").reduce((a, c) => a + c.return_bn, 0);
    const capital = cap.total_bn - (atS ? (1 - s) * enterprise : 0);
    last = Object.assign({}, ev, { welfare_bn: ev.welfare_bn - capital, engine_welfare_bn: ev.welfare_bn, capital_return_bn: capital });
    return last;
  };
  try { return f(); } finally { Engine.evaluate = evaluate; }
}

console.log("[gates]");
gate("one engine: the imported definition evaluates through the package's Engine object", C.P24 && C.P24.Engine === Engine, "main_case_2026_09_24/package.cjs");
gate("the September 27 payload file is its package's payload", JSON.stringify(payload27) === JSON.stringify(C.correctionsPayload()), PAYLOAD_FILE);
gate("general government's adopted responses are the payload's", GG.low === payload27.meta.responses.general_government.low
  && GG.high === payload27.meta.responses.general_government.high, `${GG.low.toFixed(4)} / ${GG.high.toFixed(4)}`);
for (const [name, x] of Object.entries(MODELS)) {
  const b = bandFor(x.model, undefined, specsFor(x.oo)), want = central(x.oo);
  gate(`${name}: the payload model at the adopted responses gives the package's band (1e-9)`, near(b[0], want[0], 1e-9) && near(b[1], want[1], 1e-9),
    `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
}
// At s = 1 every service, the school part, roads, parks and every capital component respond in full: the wrapped
// definition must be the proportional reference on the candidate at each specification, switch off and on.
for (const name of ["candidate", "accrual"]) {
  const x = MODELS[name];
  const specs = specsFor(x.oo);
  const reference = specs.map((spec) => evaluateFull(x.model, spec, "proportional_reference"));
  let refGap = 0, refCapGap = 0;
  withCase("enterprises_at_1", () => specs.forEach((spec, i) => {
    const pair = { end: readingOf(spec.gg) === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
    const production = Object.assign({}, Engine.defaultState(x.model).production, { normalization: spec.normalization });
    const w = S24.welfare(x.model, spec.allocation, 1, pair, production, spec.share);
    refGap = Math.max(refGap, Math.abs(w + reference[i].cost_bn));
    refCapGap = Math.max(refCapGap, Math.abs(last.capital_return_bn - reference[i].capital.total_bn));
  }));
  gate(`at s = 1 the wrapped definition is the proportional reference on the ${name} at every specification (welfare 1e-9, capital 1e-12)`,
    specs.every((s) => s.justice === "use") && refGap < 1e-9 && refCapGap < 1e-12,
    `max |diff| welfare ${refGap.toExponential(1)}, capital ${refCapGap.toExponential(1)}`);
}
let linGap = 0, linN = 0;
const prods = S24.productions(1);
for (const name of ["candidate", "accrual"]) for (const variant of VARIANTS) withCase(variant, () => {
  const mV = MODELS[name].model;
  for (const allocation of ["personal", "shared"]) for (const pair of PAIRS) for (const prod of prods.slice(0, 3).concat(prods.slice(-3)))
    for (const share of S24.SHARES) {
      const w = (s) => S24.welfare(mV, allocation, s, pair, prod, share);
      linGap = Math.max(linGap, Math.abs(w(0.37) - (0.63 * w(0) + 0.37 * w(1))));
      linN += 1;
    }
});
gate("welfare is linear in s on the candidate, switch off and on, with the capital return, in both variants", linGap < 1e-9, `${linN} points, max |diff| ${linGap.toExponential(1)}`);

const pubV2 = csvRows("main_case_candidate_v2_2026_09_28/derived/sign_reversal.csv");
const NAMES = Object.keys(MODELS);
const rows = [["measure"].concat(NAMES.flatMap((n) => [`${n}_low`, `${n}_high`]))];
const measure = (label, f) => {
  const vals = NAMES.map((n) => f(MODELS[n].model));
  const p = pubV2.find((r) => r.measure === label);
  gate(`${label}: the September 27 and v2 columns reproduce v2's committed sign_reversal.csv (1e-4)`,
    !!p && near(vals[0][0], +p.sept27_low, 1e-4) && near(vals[0][1], +p.sept27_high, 1e-4) && near(vals[1][0], +p.v2_low, 1e-4) && near(vals[1][1], +p.v2_high, 1e-4),
    p ? `${vals[0][0].toFixed(4)} / ${vals[0][1].toFixed(4)}; ${vals[1][0].toFixed(4)} / ${vals[1][1].toFixed(4)}` : "row missing");
  rows.push([label].concat(vals.flat()));
};
for (const allocation of ["personal", "shared"]) {
  measure(`service_break_even_${allocation}`, (m) => withCase("enterprises_at_1", () => S24.breakEven(m, allocation, PAIRS)));
  measure(`service_break_even_${allocation}__enterprises_at_s`, (m) => withCase("enterprises_at_s", () => S24.breakEven(m, allocation, PAIRS)));
}
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred", (m) => withCase("enterprises_at_1", () => S24.frozen(m, PAIRS)));
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred__enterprises_at_s", (m) => withCase("enterprises_at_s", () => S24.frozen(m, PAIRS)));

if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "sign_reversal.csv"),
  rows.map((r) => r.map((x) => (typeof x === "number" ? x.toFixed(4) : x)).join(",")).join("\n") + "\n");

console.log("\n[result]");
for (const r of rows.slice(1)) {
  const pct = r[0].startsWith("service");
  const fmt = (x) => (pct ? `${(100 * x).toFixed(2)}%` : x.toFixed(2));
  console.log(`  ${r[0].padEnd(72)}\n    ${NAMES.map((n, k) => `${n} ${fmt(r[1 + 2 * k])} to ${fmt(r[2 + 2 * k])}`).join("   ")}`);
}
console.log("all gates passed");
