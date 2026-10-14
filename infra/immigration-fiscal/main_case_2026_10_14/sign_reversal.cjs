/* The sign-reversal figures of the complete account on main case v7 (the candidate: v6 plus the items of package.cjs's
 * registry), beside the September 26, September 27, September 29, October 5 and October 7 cases' (v6's columns, kept).
 *
 * v6's sign_reversal.cjs (main_case_2026_10_07) with the case added. Its six measures are kept as they are: the break-even
 * share at each allocation, and the frozen-services welfare over both allocations. Under v7's group-total rule (item
 * personal_allocation) the frozen-services welfare is also given at the personal allocation alone, two rows added after
 * v6's six (the same definition, its loop over allocations restricted; gated equal to the imported definition over both). The definition is main_case_2026_09_24/sign_reversal.cjs's, imported and
 * run unchanged, and a case enters it as v5's script enters it (Engine.evaluate wrapped while the imported functions
 * run): rental assistance at 1, the enterprise receipt and its split-out receipts at option D's 1 (or at s in the
 * __enterprises_at_s rows), every other receipt response in meta.responses fixed at its value, and the return on public
 * capital from the same evaluation at 2% / 3%; v7's four job-capital receipt responses are fixed at their values like every
 * other. Each case brings its own general-government responses; the items change none, so v7's are v6's and v5's.
 * Two columns follow the cases': allocation (personal, shared, or both for v6's frozen rows over both) and in_band,
 * true where the row is at the personal allocation, the case's group total (per_spec.csv's in_band).
 *
 * Gates: one engine; the September 26, 27 and 29 payloads share general government's responses, and this payload's are
 * the lineage payload's; each payload reproduces its case's band; at s = 1 the wrapped definition is the proportional
 * reference on this case at every specification, both allocations (welfare 1e-9, capital 1e-12); welfare stays linear in
 * s; the September 26, 27 and 29 columns print as the September 29 lane's sign_reversal.csv, the October 5 and 7 columns
 * as v6's. Exit 1 and nothing written on failure.
 * Run from anywhere: node sign_reversal.cjs [--out-dir DIR] -> derived/sign_reversal.csv
 */
"use strict";
const fs = require("fs");
const path = require("path");
const argv = process.argv.slice(2);
const P = require("./package.cjs");
const OWN = "oct14";
const S24 = require(path.join(__dirname, "..", "main_case_2026_09_24", "sign_reversal.cjs"));
const { Engine, MODEL, HERE, RENTAL, RATES, ENTERPRISES, ENTERPRISE_RECEIPT, MAIN_PROFILE, gate, near, gateState, csvRows, readJson } = P;
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
const SEPT27 = "main_case_long_run_2026_09_27";
const SEPT29 = "main_case_2026_09_29";

const payload26 = readJson("main_case_2026_09_26/derived/corrections.json");
const model26 = Engine.applyCorrections(MODEL, payload26);
const CASES = { sept27: P.SEPT29.forPayload(readJson(`${SEPT27}/derived/corrections.json`)), sept29: P.SEPT29, oct05: P.OCT05, oct07: P.OCT07, oct14: P };
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
const C = P.central({}), b5 = P.band(MODELS[OWN]);
gate(`${OWN}: the payload model reproduces the case (the methods' mean over the 32 personal specifications, 1e-9)${P.CREDITS.S.stub || P.JOBCAP.S.stub ? " [STUB inputs]" : ""}`,
  near(b5[0], C[0], 1e-9) && near(b5[1], C[1], 1e-9), `${b5[0].toFixed(4)}–${b5[1].toFixed(4)}`);
for (const [name, lane] of [["oct05", "main_case_2026_10_05"], ["oct07", "main_case_2026_10_07"]]) {
  const want = readJson(`${lane}/derived/summary.json`).main_case, b = CASES[name].band(MODELS[name]);
  gate(`${name}: the payload model reproduces its band (${lane} summary.json, 1e-9), and the items change no general-government response`,
    near(b[0], want[0], 1e-9) && near(b[1], want[1], 1e-9) && JSON.stringify(ggOf(P)) === JSON.stringify(ggOf(CASES[name])), `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
}
// At s = 1 every service, the school part, roads, parks, the correction lines and every capital component respond in
// full: the wrapped definition must be the proportional reference at each specification, with its production.
const model5 = MODELS[OWN];
const reference = P.ALL_SPECS.map((spec) => P.evaluateFull(model5, spec, "proportional_reference"));
let refGap = 0, refCapGap = 0;
withCase(P, "enterprises_at_1", () => P.ALL_SPECS.forEach((spec, i) => {
  const pair = { end: readingOf(GG5, spec.gg) === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
  const production = Object.assign({}, Engine.defaultState(model5).production, { normalization: spec.normalization });
  const w = S24.welfare(model5, spec.allocation, 1, pair, production, spec.share);
  refGap = Math.max(refGap, Math.abs(w + reference[i].cost_bn));
  refCapGap = Math.max(refCapGap, Math.abs(last.capital_return_bn - reference[i].capital.total_bn));
}));
gate("at s = 1 the wrapped definition is this case's proportional reference at every one of the 64 specifications, both allocations (welfare 1e-9, capital 1e-12)",
  P.ALL_SPECS.length === 64 && P.ALL_SPECS.every((s) => s.justice === "use") && refGap < 1e-9 && refCapGap < 1e-12,
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
const pub6 = csvRows("main_case_2026_10_07/derived/sign_reversal.csv");
const pairs26 = pairsOf(payload26.meta.responses.general_government);
const NAMES = Object.keys(CASES);
const rows = [["measure", "sept26_low", "sept26_high"].concat(NAMES.flatMap((n) => [`${n}_low`, `${n}_high`]), ["allocation", "in_band"])];
// A row's allocation from its measure: service_break_even_<allocation>[__...], the frozen rows' _personal, else both.
const allocationOf = (label) => (/^service_break_even_(personal|shared)(__|$)/.test(label) ? label.match(/^service_break_even_(personal|shared)/)[1]
  : /_personal(__|$)/.test(label) ? "personal" : "both");
const fx = (x) => x.toFixed(4);
function measure(label, at26, f) {
  const vals = [at26].concat(NAMES.map((n) => f(CASES[n], MODELS[n], pairsOf(ggOf(CASES[n])))));
  const p = pub29.find((r) => r.measure === label), q = pub6.find((r) => r.measure === label);
  if (p || q) {
    gate(`${label}: the September 26, 27 and 29 columns print as the September 29 lane's sign_reversal.csv`,
      !!p && ["sept26", "sept27", "sept29"].every((n, k) => fx(vals[k][0]) === p[`${n}_low`] && fx(vals[k][1]) === p[`${n}_high`]),
      `Sept 29 ${fx(vals[2][0])} / ${fx(vals[2][1])}`);
    gate(`${label}: the October 5 and 7 columns print as v6's sign_reversal.csv`, !!q && ["oct05", "oct07"].every((n) => {
      const k = NAMES.indexOf(n) + 1;
      return fx(vals[k][0]) === q[`${n}_low`] && fx(vals[k][1]) === q[`${n}_high`];
    }), `v6 ${fx(vals[NAMES.indexOf("oct07") + 1][0])} / ${fx(vals[NAMES.indexOf("oct07") + 1][1])}; v7 ${fx(vals[NAMES.indexOf("oct14") + 1][0])} / ${fx(vals[NAMES.indexOf("oct14") + 1][1])}`);
  }
  const allocation = allocationOf(label);
  rows.push([label].concat(vals.flat(), [allocation, allocation === "personal" ? "true" : "false"]));
}
// The frozen-services welfare with the imported definition's loop over allocations restricted (v7's group total is
// the personal allocation's).
function frozenAt(m, pairs, allocations) {
  const w = { least: [], most: [] };
  for (const allocation of allocations) for (const pair of pairs) for (const prod of S24.productions(0)) for (const share of S24.SHARES) {
    w[pair.end].push(S24.welfare(m, allocation, 0, pair, prod, share));
  }
  return [Math.min(...w.most), Math.max(...w.least)];
}
{
  let gap = 0;
  for (const n of NAMES) for (const variant of VARIANTS) withCase(CASES[n], variant, () => {
    const pairs = pairsOf(ggOf(CASES[n])), a = frozenAt(MODELS[n], pairs, ["personal", "shared"]), b = S24.frozen(MODELS[n], pairs);
    gap = Math.max(gap, Math.abs(a[0] - b[0]), Math.abs(a[1] - b[1]));
  });
  gate("the restricted loop over both allocations is the imported frozen() exactly, on every case and in both variants", gap === 0, `${NAMES.length} cases`);
}
for (const allocation of ["personal", "shared"]) {
  const b26 = S24.breakEven(model26, allocation, pairs26);
  measure(`service_break_even_${allocation}`, b26, (pkg, m, pairs) => withCase(pkg, "enterprises_at_1", () => S24.breakEven(m, allocation, pairs)));
  measure(`service_break_even_${allocation}__enterprises_at_s`, b26, (pkg, m, pairs) => withCase(pkg, "enterprises_at_s", () => S24.breakEven(m, allocation, pairs)));
}
const f26 = S24.frozen(model26, pairs26);
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred", f26, (pkg, m, pairs) => withCase(pkg, "enterprises_at_1", () => S24.frozen(m, pairs)));
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred__enterprises_at_s", f26, (pkg, m, pairs) => withCase(pkg, "enterprises_at_s", () => S24.frozen(m, pairs)));
const f26p = frozenAt(model26, pairs26, ["personal"]);
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred_personal", f26p, (pkg, m, pairs) => withCase(pkg, "enterprises_at_1", () => frozenAt(m, pairs, ["personal"])));
measure("frozen_services_capital_fixed_welfare_bn_cbo_preferred_personal__enterprises_at_s", f26p, (pkg, m, pairs) => withCase(pkg, "enterprises_at_s", () => frozenAt(m, pairs, ["personal"])));
gate("the rows are the September 29 lane's (and v6's), in its order, then the two personal-allocation frozen rows; the case's rows (in_band) are the four at the personal allocation",
  JSON.stringify(rows.slice(1, 7).map((r) => r[0])) === JSON.stringify(pub29.map((r) => r.measure)) && JSON.stringify(pub6.map((r) => r.measure)) === JSON.stringify(pub29.map((r) => r.measure))
  && rows.length === 9 && JSON.stringify(rows.slice(1).map((r) => r[r.length - 2])) === JSON.stringify(["personal", "personal", "shared", "shared", "both", "both", "personal", "personal"])
  && rows.slice(1).filter((r) => r[r.length - 1] === "true").length === 4,
  rows.slice(1).map((r) => `${r[0]}: ${r[r.length - 2]}`).join("; "));

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
  console.log(`  ${r[0].padEnd(82)} Oct 7 ${fmt(r[9])} to ${fmt(r[10])}   Oct 14 ${fmt(r[11])} to ${fmt(r[12])}`);
}
console.log("all gates passed");
