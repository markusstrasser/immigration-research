/* The sign-reversal figures of the September 27 case with this lane's candidate items on (BRIEF.md, "Give the sign
 * break-even with the candidate items on").
 *
 * The definition is main_case_2026_09_24/sign_reversal.cjs's, imported and run unchanged: ordinary service budgets
 * respond at a common share s, defense and existing interest stay fixed, general government responds at its adopted
 * response whatever s is, transfers and direct receipts respond fully; CBO incidence rules and preferred keys. The
 * break-even share is w(0) / (w(0) - w(1)). The September 27 case's additions enter inside the definition's engine
 * evaluation as its own sign_reversal.cjs adds them (withCase, re-implemented here, since that script runs and writes
 * when it is loaded): rental assistance at 1, the enterprise receipt at 1 (or s in the __enterprises_at_s rows), and
 * the return on public capital from the same evaluation. The items add their receipt responses to the same state:
 * they are long-run receipt responses, fixed whatever s the service budgets take.
 *
 * Models: the September 27 payload (its committed corrections.json), and the same with each item (items.cjs) alone
 * and with all three. Gates: the September 27 column reproduces its committed sign_reversal.csv (1e-4); each model at
 * the adopted responses gives the probe's band for its items (1e-9); at s = 1 the wrapped definition is the
 * proportional reference with the items (welfare 1e-9, capital 1e-12); welfare is linear in s. Exit 1 and nothing
 * written on failure. Run from anywhere, after probe.cjs: node sign_reversal.cjs [--out-dir DIR] ->
 * derived/sign_reversal.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const I = require("./items.cjs");
const { K, HERE, FISCAL, CENTRAL_ITEMS, only, itemModel, itemOverrides, evaluateWith } = I;
const S24 = require(path.join(FISCAL, "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, MAIN_SPECS, RENTAL, RATES, RESPONSES, ENTERPRISES, ENTERPRISE_RECEIPT, gate, near, gateState, csvRows, readJson } = K;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const PAYLOAD_FILE = "main_case_long_run_2026_09_27/derived/corrections.json";
const payload27 = readJson(PAYLOAD_FILE);
const model27 = Engine.applyCorrections(MODEL, payload27);
const probe = JSON.parse(fs.readFileSync(path.join(HERE, "derived", "probe.json"), "utf8"));
const SETS = { sept27: { items: only("owner", null), band: probe.adopted.band }, owner: { items: only("owner"), band: probe.items.owner.band },
  tenant: { items: only("tenant"), band: probe.items.tenant.band }, personal: { items: only("personal"), band: probe.items.personal.band },
  all: { items: CENTRAL_ITEMS, band: probe.items.all.band } };
const NAMES = Object.keys(SETS);
const MODELS = Object.fromEntries(NAMES.map((n) => [n, { model: itemModel(model27, SETS[n].items), overrides: itemOverrides(SETS[n].items) }]));
const GG = RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG.low : GG.high }));
const readingOf = (g) => (g === GG.low ? "low" : g === GG.high ? "high" : null);
const VARIANTS = ["enterprises_at_1", "enterprises_at_s"];
const distinct = MAIN_SPECS.map((s, i) => i).filter((i) => MAIN_SPECS.findIndex((s) => JSON.stringify(s) === JSON.stringify(MAIN_SPECS[i])) === i);

let last = null;
function withCase(variant, extra, f) {
  if (!VARIANTS.includes(variant)) throw new Error("unknown variant " + variant);
  const evaluate = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response;
    const reading = readingOf(st.general_government_response);
    if (!reading) throw new Error(`[BLOCKED] general government at ${st.general_government_response}, neither adopted response`);
    const atS = variant === "enterprises_at_s";
    const ev = evaluate(m, Object.assign({}, st, { response_override: Object.assign({}, st.response_override,
      { [RENTAL]: 1, [ENTERPRISE_RECEIPT]: atS ? s : 1 }, extra) }));
    const cap = K.capitalReturn(ev, { share: st.school_share, reading, rate: RATES[reading], enterprises: ENTERPRISES, long_run: null });
    const enterprise = cap.components.filter((c) => c.group === "enterprise").reduce((a, c) => a + c.return_bn, 0);
    const capital = cap.total_bn - (atS ? (1 - s) * enterprise : 0);
    last = Object.assign({}, ev, { welfare_bn: ev.welfare_bn - capital, engine_welfare_bn: ev.welfare_bn, capital_return_bn: capital });
    return last;
  };
  try { return f(); } finally { Engine.evaluate = evaluate; }
}

console.log("[gates]");
gate("one engine: the imported definition evaluates through the package's Engine object", K.P24.Engine === Engine, "main_case_2026_09_24/package.cjs");
gate("the September 27 payload file is its package's payload", JSON.stringify(payload27) === JSON.stringify(K.correctionsPayload()), PAYLOAD_FILE);
for (const n of NAMES) {
  const { model, overrides } = MODELS[n];
  const costs = distinct.map((i) => evaluateWith(model, MAIN_SPECS[i], overrides).cost_bn);
  const b = [Math.min(...costs), Math.max(...costs)];
  gate(`${n}: the payload model at the adopted responses gives the probe's band (1e-6)`, near(b[0], SETS[n].band[0], 1e-6) && near(b[1], SETS[n].band[1], 1e-6),
    `${b[0].toFixed(4)}–${b[1].toFixed(4)} (probe.json is rounded to 1e-6)`);
}
// At s = 1 the wrapped definition is the proportional reference with every item at each specification.
const all = MODELS.all;
// The references are evaluated before the engine is wrapped.
const references = MAIN_SPECS.map((spec) => evaluateWith(all.model, spec, all.overrides, "proportional_reference"));
let refGap = 0, refCapGap = 0;
withCase("enterprises_at_1", all.overrides, () => MAIN_SPECS.forEach((spec, i) => {
  const reference = references[i];
  const pair = { end: readingOf(spec.gg) === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
  const production = Object.assign({}, Engine.defaultState(all.model).production, { normalization: spec.normalization });
  const w = S24.welfare(all.model, spec.allocation, 1, pair, production, spec.share);
  refGap = Math.max(refGap, Math.abs(w + reference.cost_bn));
  refCapGap = Math.max(refCapGap, Math.abs(last.capital_return_bn - reference.capital.total_bn));
}));
gate("at s = 1 the wrapped definition is the proportional reference with all items at every specification (welfare 1e-9, capital 1e-12)",
  MAIN_SPECS.every((s) => s.justice === "use") && refGap < 1e-9 && refCapGap < 1e-12,
  `max |diff| welfare ${refGap.toExponential(1)}, capital ${refCapGap.toExponential(1)}`);
let linGap = 0, linN = 0;
const prods = S24.productions(1);
for (const variant of VARIANTS) withCase(variant, all.overrides, () => {
  for (const allocation of ["personal", "shared"]) for (const pair of PAIRS) for (const prod of prods.slice(0, 3).concat(prods.slice(-3)))
    for (const share of S24.SHARES) {
      const w = (s) => S24.welfare(all.model, allocation, s, pair, prod, share);
      linGap = Math.max(linGap, Math.abs(w(0.37) - (0.63 * w(0) + 0.37 * w(1))));
      linN += 1;
    }
});
gate("welfare is linear in s with all items, in both variants", linGap < 1e-9, `${linN} points, max |diff| ${linGap.toExponential(1)}`);

const pub27 = csvRows("main_case_long_run_2026_09_27/derived/sign_reversal.csv");
const rows = [["measure"].concat(NAMES.flatMap((n) => [`${n}_low`, `${n}_high`]))];
const measure = (label, f) => {
  const vals = NAMES.map((n) => f(MODELS[n]));
  const p = pub27.find((r) => r.measure === label);
  gate(`${label}: the September 27 column reproduces its committed csv (1e-4)`, !!p && near(vals[0][0], +p.sept27_low, 1e-4) && near(vals[0][1], +p.sept27_high, 1e-4),
    p ? `${vals[0][0].toFixed(4)} / ${vals[0][1].toFixed(4)}` : "row missing");
  rows.push([label].concat(vals.flat()));
};
for (const allocation of ["personal", "shared"]) {
  measure(`service_break_even_${allocation}`, (x) => withCase("enterprises_at_1", x.overrides, () => S24.breakEven(x.model, allocation, PAIRS)));
  measure(`service_break_even_${allocation}__enterprises_at_s`, (x) => withCase("enterprises_at_s", x.overrides, () => S24.breakEven(x.model, allocation, PAIRS)));
}
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred", (x) => withCase("enterprises_at_1", x.overrides, () => S24.frozen(x.model, PAIRS)));
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred__enterprises_at_s", (x) => withCase("enterprises_at_s", x.overrides, () => S24.frozen(x.model, PAIRS)));

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
