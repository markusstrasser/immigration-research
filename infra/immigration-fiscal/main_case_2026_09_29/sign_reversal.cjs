/* The sign-reversal figures of the complete account on the main case of 2026-09-29, beside the September 26 and
 * September 27 cases' (the September 27 lane's columns, kept).
 *
 * The definition is main_case_2026_09_24/sign_reversal.cjs's, imported and run unchanged: ordinary service budgets
 * respond at a common share s (roads and parks included, so s replaces their long-run responses; the school part and
 * every correction line too), defense and existing interest stay fixed, general government responds at its adopted
 * response whatever s is, transfers and direct receipts respond fully; CBO incidence rules and preferred keys. Welfare
 * is linear in s, so the break-even share is w(0) / (w(0) - w(1)).
 *
 * A case enters inside the definition's engine evaluation as the September 27 lane's sign_reversal.cjs enters it
 * (Engine.evaluate wrapped while the imported functions run), read from its payload through package.cjs forPayload():
 *   - rental assistance (housing_subsidies) at 1, a transfer;
 *   - the enterprise_surplus receipt at option D's 1, with every receipt the payload splits out of the enterprise line
 *     (public housing's deficit, housing_enterprise_surplus);
 *   - every other receipt response in meta.responses at its value, fixed whatever s the service budgets take (the
 *     long-run property taxes, as the receipt-side lane's sign_reversal.cjs holds them);
 *   - the return on public capital from that same evaluation (package.cjs capitalReturn, the payload's components), 2%
 *     at the least adverse end and 3% at the most adverse.
 * The variant rows (__enterprises_at_s) put the enterprise receipts and the enterprise capital at s as well. On the
 * September 27 payload this is that lane's own wrap, so its columns reproduce.
 *
 * Gates: one engine; the three payloads share general government's responses; each payload reproduces its case's band;
 * at s = 1 the wrapped definition is the proportional reference on this case at every specification (welfare 1e-9,
 * capital 1e-12); welfare stays linear in s; the September 26 and 27 columns print as the September 27 lane's
 * sign_reversal.csv. Exit 1 and nothing written on failure.
 * Run from anywhere (after main_case.cjs): node sign_reversal.cjs [--out-dir DIR] -> derived/sign_reversal.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("./package.cjs");
const S24 = require(path.join(__dirname, "..", "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, HERE, RENTAL, RATES, ENTERPRISES, ENTERPRISE_RECEIPT, MAIN_PROFILE, gate, near, gateState, csvRows, readJson } = P;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
const SEPT27 = "main_case_long_run_2026_09_27";

const payload26 = readJson("main_case_2026_09_26/derived/corrections.json");
const model26 = Engine.applyCorrections(MODEL, payload26);
const CASES = { sept27: P.forPayload(readJson(`${SEPT27}/derived/corrections.json`)), sept29: P };
const MODELS = Object.fromEntries(Object.entries(CASES).map(([k, pkg]) => [k, pkg.payloadModel()]));
const GG = P.RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG.low : GG.high }));
const readingOf = (g) => (g === GG.low ? "low" : g === GG.high ? "high" : null);
const VARIANTS = ["enterprises_at_1", "enterprises_at_s"];

// A case inside the imported definition. While f runs, Engine.evaluate adds the case's fixed responses to the
// definition's state and subtracts the capital return computed from the same evaluation. The state carries what the
// return needs: the school fraction (school_share), s (service_response) and the end (general government's response).
let last = null;
function withCase(pkg, variant, f) {
  if (!VARIANTS.includes(variant)) throw new Error("unknown variant " + variant);
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
    const capital = cap.total_bn - (atS ? (1 - s) * ent : 0);
    last = Object.assign({}, ev, { welfare_bn: ev.welfare_bn - capital, engine_welfare_bn: ev.welfare_bn, capital_return_bn: capital });
    return last;
  };
  try { return f(); } finally { Engine.evaluate = evaluate; }
}

console.log("[gates]");
gate("one engine: the imported definition evaluates through the package's Engine object", P.P24.Engine === Engine, "main_case_2026_09_24/package.cjs");
gate("general government's adopted responses are the same on the September 26, September 27 and this payload",
  [payload26.meta.responses.general_government, CASES.sept27.RESPONSES.general_government].every((g) => g.low === GG.low && g.high === GG.high),
  `${GG.low.toFixed(4)} / ${GG.high.toFixed(4)}`);
for (const [name, lane] of [["sept27", SEPT27], ["sept29", "main_case_2026_09_29"]]) {
  const want = csvRows(`${lane}/derived/main_case_bands.csv`).find((r) => r.profile === MAIN_PROFILE && r.variant === "adopted");
  const b = CASES[name].band(MODELS[name]);
  gate(`${name}: the payload model reproduces the case at the adopted responses (${lane} main_case_bands.csv adopted, 1e-4)`,
    !!want && near(b[0], +want.cost_low_bn, 1e-4) && near(b[1], +want.cost_high_bn, 1e-4), `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
}
// At s = 1 every service, the school part, roads, parks, the correction lines and every capital component respond in
// full: the wrapped definition must be the proportional reference at each specification, with that specification's
// production.
const model29 = MODELS.sept29;
const reference = P.MAIN_SPECS.map((spec) => P.evaluateFull(model29, spec, "proportional_reference"));
let refGap = 0, refCapGap = 0;
withCase(P, "enterprises_at_1", () => P.MAIN_SPECS.forEach((spec, i) => {
  const pair = { end: readingOf(spec.gg) === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
  const production = Object.assign({}, Engine.defaultState(model29).production, { normalization: spec.normalization });
  const w = S24.welfare(model29, spec.allocation, 1, pair, production, spec.share);
  refGap = Math.max(refGap, Math.abs(w + reference[i].cost_bn));
  refCapGap = Math.max(refCapGap, Math.abs(last.capital_return_bn - reference[i].capital.total_bn));
}));
gate("at s = 1 the wrapped definition is this case's proportional reference at every specification (welfare 1e-9, capital 1e-12)",
  P.MAIN_SPECS.every((s) => s.justice === "use") && refGap < 1e-9 && refCapGap < 1e-12,
  `max |diff| welfare ${refGap.toExponential(1)}, capital ${refCapGap.toExponential(1)}`);
let linGap = 0, linN = 0;
const prods = S24.productions(1);
for (const variant of VARIANTS) withCase(P, variant, () => {
  for (const allocation of ["personal", "shared"]) for (const pair of PAIRS) for (const prod of prods.slice(0, 3).concat(prods.slice(-3)))
    for (const share of S24.SHARES) {
      const w = (s) => S24.welfare(model29, allocation, s, pair, prod, share);
      linGap = Math.max(linGap, Math.abs(w(0.37) - (0.63 * w(0) + 0.37 * w(1))));
      linN += 1;
    }
});
gate("welfare is linear in s on this case with the capital return, in both variants", linGap < 1e-9, `${linN} points, max |diff| ${linGap.toExponential(1)}`);

// The rows: the September 26 columns from the imported definition on the September 26 payload; each case's columns
// from the wrapped definition on its payload model.
const pub27 = csvRows(`${SEPT27}/derived/sign_reversal.csv`);
const pairs26 = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? payload26.meta.responses.general_government.low
  : payload26.meta.responses.general_government.high }));
const NAMES = Object.keys(CASES);
const rows = [["measure", "sept26_low", "sept26_high"].concat(NAMES.flatMap((n) => [`${n}_low`, `${n}_high`]))];
const fx = (x) => x.toFixed(4);
function measure(label, at26, f) {
  const vals = [at26].concat(NAMES.map((n) => f(CASES[n], MODELS[n])));
  const p = pub27.find((r) => r.measure === label);
  gate(`${label}: the September 26 and September 27 columns print as the September 27 lane's sign_reversal.csv`,
    !!p && fx(vals[0][0]) === p.sept26_low && fx(vals[0][1]) === p.sept26_high && fx(vals[1][0]) === p.sept27_low && fx(vals[1][1]) === p.sept27_high,
    `${fx(vals[1][0])} / ${fx(vals[1][1])}; this case ${fx(vals[2][0])} / ${fx(vals[2][1])}`);
  rows.push([label].concat(vals.flat()));
}
for (const allocation of ["personal", "shared"]) {
  const b26 = S24.breakEven(model26, allocation, pairs26);
  measure(`service_break_even_${allocation}`, b26, (pkg, m) => withCase(pkg, "enterprises_at_1", () => S24.breakEven(m, allocation, PAIRS)));
  measure(`service_break_even_${allocation}__enterprises_at_s`, b26, (pkg, m) => withCase(pkg, "enterprises_at_s", () => S24.breakEven(m, allocation, PAIRS)));
}
const f26 = S24.frozen(model26, pairs26);
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred", f26, (pkg, m) => withCase(pkg, "enterprises_at_1", () => S24.frozen(m, PAIRS)));
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred__enterprises_at_s", f26, (pkg, m) => withCase(pkg, "enterprises_at_s", () => S24.frozen(m, PAIRS)));

if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "sign_reversal.csv"), rows.map((r) => r.map((x) => (typeof x === "number" ? fx(x) : x)).join(",")).join("\n") + "\n");

console.log("\n[result]");
for (const r of rows.slice(1)) {
  const pct = r[0].startsWith("service");
  const fmt = (x) => (pct ? `${(100 * x).toFixed(1)}%` : x.toFixed(1));
  console.log(`  ${r[0].padEnd(72)} Sept 26 ${fmt(r[1])} to ${fmt(r[2])}   Sept 27 ${fmt(r[3])} to ${fmt(r[4])}   Sept 29 ${fmt(r[5])} to ${fmt(r[6])}`);
}
console.log("all gates passed");
