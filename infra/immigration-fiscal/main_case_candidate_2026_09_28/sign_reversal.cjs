/* The sign-reversal figures of the candidate (sept28_candidate), beside the September 27 case's.
 *
 * The definition is main_case_2026_09_24/sign_reversal.cjs's, imported and run unchanged: ordinary service budgets
 * respond at a common share s (roads and parks included, so s replaces their long-run responses), defense and existing
 * interest stay fixed, general government responds at its adopted response whatever s is, transfers and direct receipts
 * respond fully; CBO incidence rules and preferred keys. The break-even share is w(0) / (w(0) - w(1)) over the whole
 * production grid with private capital adjusted; the frozen-services row holds private capital fixed.
 *
 * The September 27 case's additions enter inside the definition's engine evaluation as in
 * main_case_long_run_2026_09_27/sign_reversal.cjs (withCase, re-implemented here because that script runs and writes
 * when it is loaded): rental assistance at 1, the enterprise receipt at 1 (or s in the __enterprises_at_s rows), and the
 * return on public capital from the same evaluation, 2% at the least adverse end and 3% at the most adverse.
 *
 * Models, each the September 27 payload (its committed corrections.json) with the candidate's items: item 1 alone (the
 * transfer consolidated, package.cjs consolidate()), item 2 alone (the row-4 production grid over all 3,888 cells) and
 * the candidate (both). The road arm does not enter: the definition sets roads at s, which replaces the physical cases.
 * Public pay, beside the range, is priced at the reference production cell only and is not carried over the grid.
 *
 * Gates: the September 27 columns reproduce its committed sign_reversal.csv (1e-4) and its payload is the package's; each
 * model at the adopted responses gives the candidate package's band for its items (1e-9); at s = 1 the wrapped definition
 * is the proportional reference on the candidate at every specification (welfare 1e-9, capital 1e-12); welfare is
 * linear in s on the candidate in both variants. Exit 1 and nothing written on failure.
 * Run from anywhere: node sign_reversal.cjs [--out-dir DIR] -> derived/sign_reversal.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const C = require("./package.cjs");
const S24 = require(path.join(__dirname, "..", "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, HERE, RENTAL, RATES, RESPONSES, ENTERPRISES, ENTERPRISE_RECEIPT, TRANSFERS, OFF, CANDIDATE, gate, near,
  gateState, csvRows, readJson, withProduction, consolidate, specsFor, withCentral, bandFor, central } = C;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const PAYLOAD_FILE = "main_case_long_run_2026_09_27/derived/corrections.json";
const payload27 = readJson(PAYLOAD_FILE);
const model27 = Engine.applyCorrections(MODEL, payload27);
const T = TRANSFERS.public_housing_operating.bn;
// The four models and the option sets whose band each must give.
const MODELS = {
  sept27: { model: withProduction(model27, "published"), o: OFF },
  item1: { model: consolidate(withProduction(model27, "published"), T), o: Object.assign({}, OFF, { internal_transfer: "public_housing_operating" }) },
  item2: { model: withProduction(model27, "row4"), o: Object.assign({}, OFF, { production: "row4" }) },
  candidate: { model: consolidate(withProduction(model27, "row4"), T), o: CANDIDATE },
};
const GG = RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG.low : GG.high }));
const readingOf = (g) => (g === GG.low ? "low" : g === GG.high ? "high" : null);
const VARIANTS = ["enterprises_at_1", "enterprises_at_s"];

// The September 27 case inside the imported definition (its sign_reversal.cjs withCase, line for line).
let last = null;
function withCase(variant, f) {
  if (!VARIANTS.includes(variant)) throw new Error("unknown variant " + variant);
  const evaluate = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response;
    const reading = readingOf(st.general_government_response);
    if (!reading) throw new Error(`[BLOCKED] general government at ${st.general_government_response}, neither adopted response`);
    const atS = variant === "enterprises_at_s";
    const ev = evaluate(m, Object.assign({}, st, { response_override: Object.assign({}, st.response_override,
      { [RENTAL]: 1, [ENTERPRISE_RECEIPT]: atS ? s : 1 }) }));
    const cap = C.capitalReturn(ev, { share: st.school_share, reading, rate: RATES[reading], enterprises: ENTERPRISES, long_run: null });
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
  const b = bandFor(x.model, undefined, specsFor(x.o)), want = central(x.o);
  gate(`${name}: the payload model at the adopted responses gives the package's band (1e-9)`, near(b[0], want[0], 1e-9) && near(b[1], want[1], 1e-9),
    `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
}
// At s = 1 every service, the school part, roads, parks and every capital component respond in full: the wrapped
// definition must be the proportional reference on the candidate at each specification, with its row-4 production.
const mC = MODELS.candidate.model;
const specsC = specsFor(withCentral(CANDIDATE));
const reference = specsC.map((spec) => C.evaluateFull(mC, spec, "proportional_reference"));
let refGap = 0, refCapGap = 0;
withCase("enterprises_at_1", () => specsC.forEach((spec, i) => {
  const pair = { end: readingOf(spec.gg) === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
  const production = Object.assign({}, Engine.defaultState(mC).production, { normalization: spec.normalization });
  const w = S24.welfare(mC, spec.allocation, 1, pair, production, spec.share);
  refGap = Math.max(refGap, Math.abs(w + reference[i].cost_bn));
  refCapGap = Math.max(refCapGap, Math.abs(last.capital_return_bn - reference[i].capital.total_bn));
}));
gate("at s = 1 the wrapped definition is the proportional reference on the candidate at every specification (welfare 1e-9, capital 1e-12)",
  specsC.every((s) => s.justice === "use") && refGap < 1e-9 && refCapGap < 1e-12,
  `max |diff| welfare ${refGap.toExponential(1)}, capital ${refCapGap.toExponential(1)}`);
let linGap = 0, linN = 0;
const prods = S24.productions(1);
for (const variant of VARIANTS) withCase(variant, () => {
  for (const allocation of ["personal", "shared"]) for (const pair of PAIRS) for (const prod of prods.slice(0, 3).concat(prods.slice(-3)))
    for (const share of S24.SHARES) {
      const w = (s) => S24.welfare(mC, allocation, s, pair, prod, share);
      linGap = Math.max(linGap, Math.abs(w(0.37) - (0.63 * w(0) + 0.37 * w(1))));
      linN += 1;
    }
});
gate("welfare is linear in s on the candidate with the capital return, in both variants", linGap < 1e-9, `${linN} points, max |diff| ${linGap.toExponential(1)}`);

const pub27 = csvRows("main_case_long_run_2026_09_27/derived/sign_reversal.csv");
const NAMES = Object.keys(MODELS);
const rows = [["measure"].concat(NAMES.flatMap((n) => [`${n}_low`, `${n}_high`]))];
const measure = (label, f) => {
  const vals = NAMES.map((n) => f(MODELS[n].model));
  const p = pub27.find((r) => r.measure === label);
  gate(`${label}: the September 27 column reproduces its committed csv (1e-4)`, !!p && near(vals[0][0], +p.sept27_low, 1e-4) && near(vals[0][1], +p.sept27_high, 1e-4),
    p ? `${vals[0][0].toFixed(4)} / ${vals[0][1].toFixed(4)}` : "row missing");
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
  console.log(`  ${r[0].padEnd(72)} ${NAMES.map((n, k) => `${n} ${fmt(r[1 + 2 * k])} to ${fmt(r[2 + 2 * k])}`).join("   ")}`);
}
console.log("all gates passed");
