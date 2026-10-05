/* The sign-reversal figures of the complete account on the main case of 2026-10-05 (v5), beside the September 26,
 * September 27 and September 29 cases' (the September 29 lane's columns, kept).
 *
 * The definition is main_case_2026_09_24/sign_reversal.cjs's, imported and run unchanged, and a case enters it as the
 * September 29 lane's sign_reversal.cjs enters it (Engine.evaluate wrapped while the imported functions run): rental
 * assistance at 1, the enterprise receipt and its split-out receipts at option D's 1 (or at s in the
 * __enterprises_at_s rows), every other receipt response in meta.responses fixed at its value, and the return on
 * public capital from the same evaluation at 2% / 3%. One change: each case brings its own general-government
 * responses. v5's group is the larger one (meta.lineage), so its finite-removal responses are its own; the definition's
 * two ends take each case's (the September 29 script gates one pair for every payload, which v5 does not share).
 *
 * Gates: one engine; the September 26, 27 and 29 payloads share general government's responses, and this payload's
 * are the lineage payload's; each payload reproduces its case's band; at s = 1 the wrapped definition is the
 * proportional reference on this case at every specification (welfare 1e-9, capital 1e-12); welfare stays linear in s;
 * the September 26, 27 and 29 columns print as the September 29 lane's sign_reversal.csv. Exit 1 and nothing written
 * on failure.
 * Run from anywhere: node sign_reversal.cjs [--out-dir DIR] -> derived/sign_reversal.csv
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
const SEPT29 = "main_case_2026_09_29";

const payload26 = readJson("main_case_2026_09_26/derived/corrections.json");
const model26 = Engine.applyCorrections(MODEL, payload26);
const CASES = { sept27: P.SEPT29.forPayload(readJson(`${SEPT27}/derived/corrections.json`)), sept29: P.SEPT29, oct05: P };
const MODELS = Object.fromEntries(Object.entries(CASES).map(([k, pkg]) => [k, pkg.payloadModel()]));
const ggOf = (pkg) => pkg.RESPONSES.general_government;
const pairsOf = (gg) => S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? gg.low : gg.high }));
const readingOf = (gg, g) => (g === gg.low ? "low" : g === gg.high ? "high" : null);
const VARIANTS = ["enterprises_at_1", "enterprises_at_s"];

// A case inside the imported definition (the September 29 lane's wrap, with the case's own general-government pair).
let last = null;
function withCase(pkg, variant, f) {
  if (!VARIANTS.includes(variant)) throw new Error("unknown variant " + variant);
  const gg = ggOf(pkg);
  const enterprise = [ENTERPRISE_RECEIPT].concat(pkg.ENTERPRISE_SPLITS.map((id) => "receipt:" + id));
  const fixed = Object.entries(pkg.LINE_RESPONSES).filter(([k]) => k.startsWith("receipt:") && !enterprise.includes(k));
  const evaluate = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response;
    const reading = readingOf(gg, st.general_government_response);
    if (!reading) throw new Error(`[BLOCKED] general government at ${st.general_government_response}, neither of the case's responses`);
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
const GG4 = ggOf(CASES.sept29), GG5 = ggOf(P);
gate("general government's responses are the same on the September 26, September 27 and September 29 payloads",
  [payload26.meta.responses.general_government, ggOf(CASES.sept27)].every((g) => g.low === GG4.low && g.high === GG4.high),
  `${GG4.low.toFixed(4)} / ${GG4.high.toFixed(4)}`);
gate("this payload's general-government responses are the lineage payload's (the larger group's s), and differ from September 29's",
  JSON.stringify(GG5) === JSON.stringify(P.ADDITION.set.meta.responses.general_government) && GG5.low !== GG4.low && GG5.high !== GG4.high
  && GG5.s === P.correctionsPayload().meta.lineage.s.v5, `${GG5.low.toFixed(4)} / ${GG5.high.toFixed(4)} at s ${GG5.s.toFixed(4)}`);
for (const [name, lane] of [["sept27", SEPT27], ["sept29", SEPT29]]) {
  const want = csvRows(`${lane}/derived/main_case_bands.csv`).find((r) => r.profile === MAIN_PROFILE && r.variant === "adopted");
  const b = CASES[name].band(MODELS[name]);
  gate(`${name}: the payload model reproduces the case at the adopted responses (${lane} main_case_bands.csv adopted, 1e-4)`,
    !!want && near(b[0], +want.cost_low_bn, 1e-4) && near(b[1], +want.cost_high_bn, 1e-4), `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
}
const C = P.central({}), b5 = P.band(MODELS.oct05);
gate("oct05: the payload model reproduces the case (the methods' mean, 1e-9)", near(b5[0], C[0], 1e-9) && near(b5[1], C[1], 1e-9),
  `${b5[0].toFixed(4)}–${b5[1].toFixed(4)}`);
// At s = 1 every service, the school part, roads, parks, the correction lines and every capital component respond in
// full: the wrapped definition must be the proportional reference at each specification, with its production.
const model5 = MODELS.oct05;
const reference = P.MAIN_SPECS.map((spec) => P.evaluateFull(model5, spec, "proportional_reference"));
let refGap = 0, refCapGap = 0;
withCase(P, "enterprises_at_1", () => P.MAIN_SPECS.forEach((spec, i) => {
  const pair = { end: readingOf(GG5, spec.gg) === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
  const production = Object.assign({}, Engine.defaultState(model5).production, { normalization: spec.normalization });
  const w = S24.welfare(model5, spec.allocation, 1, pair, production, spec.share);
  refGap = Math.max(refGap, Math.abs(w + reference[i].cost_bn));
  refCapGap = Math.max(refCapGap, Math.abs(last.capital_return_bn - reference[i].capital.total_bn));
}));
gate("at s = 1 the wrapped definition is this case's proportional reference at every specification (welfare 1e-9, capital 1e-12)",
  P.MAIN_SPECS.every((s) => s.justice === "use") && refGap < 1e-9 && refCapGap < 1e-12,
  `max |diff| welfare ${refGap.toExponential(1)}, capital ${refCapGap.toExponential(1)}`);
let linGap = 0, linN = 0;
const prods = S24.productions(1);
for (const variant of VARIANTS) withCase(P, variant, () => {
  for (const allocation of ["personal", "shared"]) for (const pair of pairsOf(GG5)) for (const prod of prods.slice(0, 3).concat(prods.slice(-3)))
    for (const share of S24.SHARES) {
      const w = (s) => S24.welfare(model5, allocation, s, pair, prod, share);
      linGap = Math.max(linGap, Math.abs(w(0.37) - (0.63 * w(0) + 0.37 * w(1))));
      linN += 1;
    }
});
gate("welfare is linear in s on this case with the capital return, in both variants", linGap < 1e-9, `${linN} points, max |diff| ${linGap.toExponential(1)}`);

// The rows: the September 26 columns from the imported definition on the September 26 payload; each case's columns
// from the wrapped definition on its payload model, at its own general-government pair.
const pub29 = csvRows(`${SEPT29}/derived/sign_reversal.csv`);
const pairs26 = pairsOf(payload26.meta.responses.general_government);
const NAMES = Object.keys(CASES);
const rows = [["measure", "sept26_low", "sept26_high"].concat(NAMES.flatMap((n) => [`${n}_low`, `${n}_high`]))];
const fx = (x) => x.toFixed(4);
function measure(label, at26, f) {
  const vals = [at26].concat(NAMES.map((n) => f(CASES[n], MODELS[n], pairsOf(ggOf(CASES[n])))));
  const p = pub29.find((r) => r.measure === label);
  gate(`${label}: the September 26, 27 and 29 columns print as the September 29 lane's sign_reversal.csv`,
    !!p && ["sept26", "sept27", "sept29"].every((n, k) => fx(vals[k][0]) === p[`${n}_low`] && fx(vals[k][1]) === p[`${n}_high`]),
    `Sept 29 ${fx(vals[2][0])} / ${fx(vals[2][1])}; this case ${fx(vals[3][0])} / ${fx(vals[3][1])}`);
  rows.push([label].concat(vals.flat()));
}
for (const allocation of ["personal", "shared"]) {
  const b26 = S24.breakEven(model26, allocation, pairs26);
  measure(`service_break_even_${allocation}`, b26, (pkg, m, pairs) => withCase(pkg, "enterprises_at_1", () => S24.breakEven(m, allocation, pairs)));
  measure(`service_break_even_${allocation}__enterprises_at_s`, b26, (pkg, m, pairs) => withCase(pkg, "enterprises_at_s", () => S24.breakEven(m, allocation, pairs)));
}
const f26 = S24.frozen(model26, pairs26);
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred", f26, (pkg, m, pairs) => withCase(pkg, "enterprises_at_1", () => S24.frozen(m, pairs)));
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred__enterprises_at_s", f26, (pkg, m, pairs) => withCase(pkg, "enterprises_at_s", () => S24.frozen(m, pairs)));
gate("the rows are the September 29 lane's, in its order", JSON.stringify(rows.slice(1).map((r) => r[0])) === JSON.stringify(pub29.map((r) => r.measure)));

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
  console.log(`  ${r[0].padEnd(72)} Sept 29 ${fmt(r[5])} to ${fmt(r[6])}   Oct 5 ${fmt(r[7])} to ${fmt(r[8])}`);
}
console.log("all gates passed");
