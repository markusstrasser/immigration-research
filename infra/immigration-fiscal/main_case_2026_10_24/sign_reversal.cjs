/* v10 sign-reversal readings. Keep every v9 CSV cell unchanged; append oct24_low and oct24_high.
 * Definition: v9's (main_case_2026_10_16/sign_reversal.cjs withCase, imported unchanged), swept on v9's package and
 * payload model (v10 adds no edits and no people), with its options.post hook pricing v9's post-engine amounts and
 * v10's items 22 and 23 (items.cjs post) at each sweep point:
 * - capital pieces' engine and completion parts follow the sweep's capital (service capital takes the service
 *   response s; enterprises take s in the enterprises_at_s variant, their response scaled with the return);
 * - coverage and count parts are fixed costs, as v9 holds item 12 and the count items;
 * - the college and health parts of items 22 and 23 are added to items 15 and 21's amounts, so v9's rule for those
 *   items (raw(s) - (1 - s) raw(0)) scales them too.
 * Run: node sign_reversal.cjs [--out-dir DIR]. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("./package.cjs"), I = P.ITEMS, V9 = P.V9_PACKAGE;
const SR = require("../main_case_2026_10_16/sign_reversal.cjs");
const S24 = require("../main_case_2026_09_24/sign_reversal.cjs");
const { Engine } = V9;
const args = process.argv.slice(2), OUT = path.resolve(args.includes("--out-dir") ? args[args.indexOf("--out-dir") + 1] : path.join(__dirname, "derived"));
const checks = [];
function gate(name, pass, detail = "") { checks.push({ name, pass: !!pass, detail }); console.log(`  ${pass ? "PASS" : "FAIL"} ${name}${detail ? `: ${detail}` : ""}`); }
const sum = (a) => a.reduce((x, y) => x + y, 0);
const pairsOf = (pkg) => S24.PAIRS.map((pair) => ({ ...pair, g: pkg.RESPONSES.general_government[pair.end === "least" ? "low" : "high"] }));
const FOLD = { college: "public_college_response", health: "health_residual_key" };
for (const id of Object.values(FOLD)) if (!SR.SCALED_ITEMS.includes(id)) throw Error(`[BLOCKED] sign_reversal: v9 no longer scales ${id}`);
let lastV10 = null;
// The post hook: v9's amounts at the sweep point plus v10's items `on` (a Set of item numbers).
const hookFor = (on) => (r, ctx) => {
  const v9add = V9.postFor(ctx.m, r.spec, undefined, { evaluation: r.ev, capital: r.adjustedCapital });
  const amounts = { ...v9add.amounts };
  let total = v9add.total_bn;
  if (on.size) {
    const atS = ctx.variant === "enterprises_at_s";
    const capital = { ...r.adjustedCapital, components: r.adjustedCapital.components.map((c) => atS && c.group === "enterprise" ? { ...c, response: c.response * r.s } : c) };
    const d = I.post(V9, { evaluation: r.ev, capital, v9_post_engine: { parts: v9add.parts } }, r.spec, on, { evaluate: V9.evaluateFull });
    for (const [id, v] of Object.entries(d.amounts)) amounts[id] = (amounts[id] || 0) + v;
    for (const q of d.rows) if (FOLD[q.part]) { amounts[q.item] -= q.delta_bn; amounts[FOLD[q.part]] = (amounts[FOLD[q.part]] || 0) + q.delta_bn; }
    total += d.total_bn;
    lastV10 = { s: r.s, variant: ctx.variant, rows: d.rows, total_bn: d.total_bn };
  }
  return { base: r.basePost, amounts, total };
};
const withV10 = (variant, f, on) => SR.withCase(V9, variant, f, true, { post: hookFor(on) });
function frozenPersonal(model, pairs) {
  const w = { least: [], most: [] };
  for (const pair of pairs) for (const prod of S24.productions(0)) for (const share of S24.SHARES) w[pair.end].push(S24.welfare(model, "personal", 0, pair, prod, share));
  return [Math.min(...w.most), Math.max(...w.least)];
}
// v9's readings(), with the hook.
function readings(on) {
  const model = V9.payloadModel(), pairs = pairsOf(V9), out = new Map();
  for (const [variant, suffix] of [["enterprises_at_1", ""], ["enterprises_at_s", "__enterprises_at_s"]]) withV10(variant, () => {
    for (const allocation of ["personal", "shared"]) out.set(`service_break_even_${allocation}${suffix}`, S24.breakEven(model, allocation, pairs));
    out.set(`frozen_services_capital_fixed_welfare_bn_cbo_preferred${suffix}`, S24.frozen(model, pairs));
    out.set(`frozen_services_capital_fixed_welfare_bn_cbo_preferred_personal${suffix}`, frozenPersonal(model, pairs));
  }, on);
  return out;
}
const started = performance.now();
const oldLines = fs.readFileSync(path.join(__dirname, "../main_case_2026_10_16/derived/sign_reversal.csv"), "utf8").trimEnd().split("\n"), oldRows = oldLines.map((l) => l.split(","));
const H = oldRows[0];
// 1. The hook with v10 off reproduces v9's printed columns (the hook prices v9's amounts as v9's own path does).
const off = readings(new Set());
for (const row of oldRows.slice(1)) {
  const got = off.get(row[0]);
  gate(`v10 items off reproduce v9 ${row[0]}`, !!got && got.every((v, i) => v.toFixed(4) === row[H.indexOf(`oct16_${i ? "high" : "low"}`)]));
}
const on = new Set(P.V10_ON), model = V9.payloadModel();
// 2. At services = 1, welfare is minus v10's full cost on every specification (reference pricing, as v9 gates).
{
  // Priced before the sweep: inside withCase, Engine.evaluate is the sweep's.
  const pm = P.payloadModel(), reference = V9.ALL_SPECS.map((spec) => P.evaluateFull(pm, spec, "proportional_reference").cost_bn);
  let gap = 0;
  withV10("enterprises_at_1", () => V9.ALL_SPECS.forEach((spec, i) => {
    const pair = { end: spec.reading === "low" ? "least" : "most", g: spec.gg, uc: spec.uc };
    const production = { ...Engine.defaultState(model).production, normalization: spec.normalization };
    const w = S24.welfare(model, spec.allocation, 1, pair, production, spec.share);
    gap = Math.max(gap, Math.abs(w + reference[i]));
  }), on);
  gate(`at services=1 welfare is minus v10 full cost on all ${V9.ALL_SPECS.length} specifications`, gap < 1e-9, gap.toExponential(2));
}
// 3. Welfare stays linear in the service response with the v10 terms.
{
  let gap = 0, n = 0;
  const prods = S24.productions(1);
  for (const variant of SR.VARIANTS) withV10(variant, () => {
    for (const allocation of ["personal", "shared"]) for (const pair of pairsOf(V9)) for (const production of [prods[0], prods.at(-1)]) for (const share of S24.SHARES) {
      const w = (s) => S24.welfare(model, allocation, s, pair, production, share);
      gap = Math.max(gap, Math.abs(w(0.37) - 0.63 * w(0) - 0.37 * w(1))); n++;
    }
  }, on);
  gate("service response remains linear with the v10 terms", gap < 1e-9, `${n} points; ${gap.toExponential(2)}`);
}
// 4. With every service frozen, no v10 engine or completion part on service capital stays charged; coverage and count
//    parts are the fixed costs. v9 zeroes items 15 and 21 at s = 0 by construction, so the fold is checked for
//    effect instead: the v10 college and health parts are nonzero there before v9's scaling, and the post total
//    excludes them.
{
  const states = (f) => { for (const allocation of ["personal", "shared"]) for (const pair of pairsOf(V9)) for (const share of S24.SHARES) f(allocation, pair, share); };
  const w0 = (allocation, pair, share) => S24.welfare(model, allocation, 0, pair, S24.productions(1)[0], share);
  const off0 = {};
  for (const variant of SR.VARIANTS) withV10(variant, () => states((a, p, sh) => { off0[[variant, a, p.end, sh]] = w0(a, p, sh); }), new Set());
  let worst = 0, at = "", n = 0, rowsChecked = 0, folded = 0, foldGap = 0;
  for (const variant of SR.VARIANTS) withV10(variant, () => states((allocation, pair, share) => {
    const w = w0(allocation, pair, share);
    if (lastV10.s !== 0) throw Error("[BLOCKED] sign_reversal gate 4: last v10 pricing not at s = 0");
    for (const q of lastV10.rows) {
      const service = SR.SERVICE_CAPITAL.has(q.piece) || (variant === "enterprises_at_s" && q.piece.startsWith("ent_"));
      if (service && (q.part === "engine" || q.part === "completion")) { rowsChecked++; if (Math.abs(q.delta_bn) > worst) { worst = Math.abs(q.delta_bn); at = `${q.item}/${q.piece}/${q.part}`; } }
    }
    const f = sum(lastV10.rows.filter((q) => FOLD[q.part]).map((q) => q.delta_bn));
    folded = Math.max(folded, Math.abs(f));
    // v10 on minus off at s = 0 is minus the v10 total less its folded parts (removed with items 15 and 21).
    foldGap = Math.max(foldGap, Math.abs((w - off0[[variant, allocation, pair.end, share]]) + (lastV10.total_bn - f)));
    n++;
  }), on);
  gate("at s = 0 no v10 engine or completion part on service capital stays charged", rowsChecked > 0 && worst < 1e-9, `${n} states, ${rowsChecked} rows; largest ${worst.toExponential(2)}bn ${at}`);
  gate("at s = 0 v10 changes welfare by its total less the folded college and health parts, which are nonzero", folded > 1e-6 && foldGap < 1e-9, `folded up to ${folded.toExponential(2)}bn; gap ${foldGap.toExponential(2)}`);
}
const values = readings(on);
gate("all eight v9 rows have finite v10 readings", oldRows.length === 9 && oldRows.slice(1).every((row) => values.get(row[0])?.every(Number.isFinite)));
const lines = [oldLines[0] + ",oct24_low,oct24_high", ...oldLines.slice(1).map((line) => line + "," + values.get(line.split(",")[0]).map((v) => v.toFixed(4)).join(","))];
gate("every v9 column and cell is unchanged, in order", lines.every((line, i) => line.startsWith(oldLines[i] + ",")));
for (const row of oldRows.slice(1)) console.log(`  [oct16 -> oct24] ${row[0]}: ${row[H.indexOf("oct16_low")]} / ${row[H.indexOf("oct16_high")]} -> ${values.get(row[0]).map((v) => v.toFixed(4)).join(" / ")}`);
if (checks.some((c) => !c.pass)) throw Error("[BLOCKED] sign_reversal gate failure; no output written");
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "sign_reversal.csv"), lines.join("\n") + "\n");
console.log(`all ${checks.length} gates passed; ${((performance.now() - started) / 1000).toFixed(1)}s; maxRSS ${process.resourceUsage().maxRSS} KiB`);
