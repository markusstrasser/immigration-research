/* The sign-reversal figures of the complete account on the main case of 2026-09-27.
 *
 * The definition is main_case_2026_09_24/sign_reversal.cjs's, imported and run unchanged: ordinary service budgets
 * respond at a common share s (roads and parks included, so s replaces their long-run responses; the school part
 * too), defense and existing interest stay fixed, general government responds at its adopted response whatever s
 * is (0.6000 at the least adverse end, 0.8504 at the most adverse), transfers and direct receipts respond fully;
 * CBO incidence rules and preferred keys. Welfare is linear in s, so the break-even share is w(0) / (w(0) - w(1)).
 *
 * This case adds three things inside the definition's own engine evaluation (Engine.evaluate is wrapped while
 * the imported functions run, as capital_return_services_2026_09_27/spec_lines.cjs wraps it):
 *   - rental assistance (housing_subsidies) at 1, a transfer;
 *   - the enterprise_surplus receipt at option D's 1;
 *   - the return on public capital from that same evaluation (package.cjs capitalReturn), 2% at the least adverse
 *     end and 3% at the most adverse. Every component follows its rule: line-response components move with their
 *     line's s (the roads and parks subfunctions too), offices with general government's response, and the
 *     enterprise components stay at D's 1.
 * The variant rows (__enterprises_at_s) put the enterprise receipt and the enterprise capital at s as well.
 *
 * Gates: the September 26 columns reproduce from the imported definition before anything changes; this case's
 * payload reproduces the case at the adopted responses; at s = 1 the wrapped definition is the proportional
 * reference at every specification (engine and capital return); welfare stays linear in s.
 * Run from anywhere: node sign_reversal.cjs  ->  derived/sign_reversal.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("./package.cjs");
const S24 = require(path.join(__dirname, "..", "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, HERE, RENTAL, RATES, RESPONSES, ENTERPRISES, ENTERPRISE_RECEIPT, MAIN_SPECS, gate, near, gateState,
  csvRows, readJson } = P;

const payload26 = readJson("main_case_2026_09_26/derived/corrections.json");
const model26 = Engine.applyCorrections(MODEL, payload26);
const model27 = Engine.applyCorrections(MODEL, P.correctionsPayload());
const GG = RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG.low : GG.high }));
const readingOf = (g) => (g === GG.low ? "low" : g === GG.high ? "high" : null);
const VARIANTS = ["enterprises_at_1", "enterprises_at_s"];

// This case inside the imported definition. While f runs, Engine.evaluate adds rental assistance at 1 and the
// enterprise receipt (1, or s in the variant) to the definition's state, and subtracts the capital return computed
// from the same evaluation. The state carries what the return needs: the school fraction (school_share), s
// (service_response) and the end (general government's response).
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
    const cap = P.capitalReturn(ev, { share: st.school_share, reading, rate: RATES[reading], enterprises: ENTERPRISES, long_run: null });
    const enterprise = cap.components.filter((c) => c.group === "enterprise").reduce((a, c) => a + c.return_bn, 0);
    const capital = cap.total_bn - (atS ? (1 - s) * enterprise : 0);
    last = Object.assign({}, ev, { welfare_bn: ev.welfare_bn - capital, engine_welfare_bn: ev.welfare_bn, capital_return_bn: capital });
    return last;
  };
  try { return f(); } finally { Engine.evaluate = evaluate; }
}

console.log("[gates]");
gate("general government's adopted responses are the September 26 case's", GG.low === payload26.meta.responses.general_government.low
  && GG.high === payload26.meta.responses.general_government.high, `${GG.low.toFixed(4)} / ${GG.high.toFixed(4)}`);
gate("one engine: the imported definition evaluates through the same Engine object", P.P24.Engine === Engine, "main_case_2026_09_24/package.cjs");
const want = csvRows("main_case_long_run_2026_09_27/derived/main_case_bands.csv").find((r) => r.profile === P.MAIN_PROFILE && r.variant === "adopted");
const b27 = P.band(model27);
gate("the payload reproduces the case at the adopted responses (main_case_bands.csv adopted, 1e-4)",
  near(b27[0], +want.cost_low_bn, 1e-4) && near(b27[1], +want.cost_high_bn, 1e-4), `${b27[0].toFixed(4)}–${b27[1].toFixed(4)}`);
// At s = 1 every service, the school part, roads, parks and every capital component respond in full: the wrapped
// definition must be the proportional reference at each specification, with that specification's production.
const reference = MAIN_SPECS.map((spec) => P.evaluateFull(model27, spec, "proportional_reference"));
let refGap = 0, refCapGap = 0;
withCase("enterprises_at_1", () => MAIN_SPECS.forEach((spec, i) => {
  const pair = { end: readingOf(spec.gg) === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
  const production = Object.assign({}, Engine.defaultState(model27).production, { normalization: spec.normalization });
  const w = S24.welfare(model27, spec.allocation, 1, pair, production, spec.share);
  refGap = Math.max(refGap, Math.abs(w + reference[i].cost_bn));
  refCapGap = Math.max(refCapGap, Math.abs(last.capital_return_bn - reference[i].capital.total_bn));
}));
gate("at s = 1 the wrapped definition is the proportional reference at every specification (welfare 1e-9, capital 1e-12)",
  MAIN_SPECS.every((s) => s.justice === "use") && refGap < 1e-9 && refCapGap < 1e-12,
  `max |diff| welfare ${refGap.toExponential(1)}, capital ${refCapGap.toExponential(1)}`);
// Welfare is linear in s with the capital return and in both variants, so the break-even formula holds.
let linGap = 0, linN = 0;
const prods = S24.productions(1);
for (const variant of VARIANTS) withCase(variant, () => {
  for (const allocation of ["personal", "shared"]) for (const pair of PAIRS) for (const prod of prods.slice(0, 3).concat(prods.slice(-3)))
    for (const share of S24.SHARES) {
      const w = (s) => S24.welfare(model27, allocation, s, pair, prod, share);
      linGap = Math.max(linGap, Math.abs(w(0.37) - (0.63 * w(0) + 0.37 * w(1))));
      linN += 1;
    }
});
gate("welfare is linear in s with the capital return, in both variants", linGap < 1e-9, `${linN} points, max |diff| ${linGap.toExponential(1)}`);

// The September 26 columns: the imported definition on the September 26 payload, reproduced before anything else.
const pub26 = csvRows("main_case_2026_09_26/derived/sign_reversal.csv");
const pairs26 = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? payload26.meta.responses.general_government.low
  : payload26.meta.responses.general_government.high }));
const rows = [["measure", "sept26_low", "sept26_high", "sept27_low", "sept27_high"]];
for (const allocation of ["personal", "shared"]) {
  const b26 = S24.breakEven(model26, allocation, pairs26);
  const p = pub26.find((r) => r.measure === `service_break_even_${allocation}`);
  gate(`break-even, ${allocation}: September 26 reproduces`, near(b26[0], +p.sept26_low, 1e-4) && near(b26[1], +p.sept26_high, 1e-4),
    `${(100 * b26[0]).toFixed(2)}–${(100 * b26[1]).toFixed(2)}%`);
  const main = withCase("enterprises_at_1", () => S24.breakEven(model27, allocation, PAIRS));
  const atS = withCase("enterprises_at_s", () => S24.breakEven(model27, allocation, PAIRS));
  rows.push([`service_break_even_${allocation}`, b26[0], b26[1], main[0], main[1]]);
  rows.push([`service_break_even_${allocation}__enterprises_at_s`, b26[0], b26[1], atS[0], atS[1]]);
}
const f26 = S24.frozen(model26, pairs26);
const pf = pub26.find((r) => r.measure === "frozen_services_capital_fixed_welfare_bn_cbo_preferred");
gate("frozen services: September 26 reproduces", near(f26[0], +pf.sept26_low, 1e-4) && near(f26[1], +pf.sept26_high, 1e-4),
  `${f26[0].toFixed(2)} to ${f26[1].toFixed(2)}`);
const f27 = withCase("enterprises_at_1", () => S24.frozen(model27, PAIRS));
const f27s = withCase("enterprises_at_s", () => S24.frozen(model27, PAIRS));
rows.push(["frozen_services_capital_fixed_welfare_bn_cbo_preferred", f26[0], f26[1], f27[0], f27[1]]);
rows.push(["frozen_services_capital_fixed_welfare_bn_cbo_preferred__enterprises_at_s", f26[0], f26[1], f27s[0], f27s[1]]);

if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
fs.writeFileSync(path.join(HERE, "derived", "sign_reversal.csv"),
  rows.map((r) => r.map((x) => (typeof x === "number" ? x.toFixed(4) : x)).join(",")).join("\n") + "\n");

console.log("\n[result]");
for (const r of rows.slice(1)) {
  const pct = r[0].startsWith("service");
  const fmt = (x) => (pct ? `${(100 * x).toFixed(1)}%` : x.toFixed(1));
  console.log(`  ${r[0].padEnd(72)} Sept 26 ${fmt(r[1])} to ${fmt(r[2])}   Sept 27 ${fmt(r[3])} to ${fmt(r[4])}`);
}
console.log("all gates passed");
