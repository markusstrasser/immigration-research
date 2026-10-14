"use strict";
// Item 11: source rows are deltas on v7, whose item-5b edits remain applied.
// Apply this declared fixed amount after the engine, at spec.reading.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const ROOT = path.resolve(__dirname, "../../.."), SOURCE = "infra/immigration-fiscal/mixed_unit_removal_2026_10_14";
const FILES = { summary: `${SOURCE}/derived/round2_summary.json`, replicates: `${SOURCE}/derived/round2_replicates.csv`, results: `${SOURCE}/derived/round2_results.csv` };
const PINS = { summary: "acbb2ba55a6f1fdf4f2a66c2e236608bdaebd24090f7b814333417c7ed3bbc01", replicates: "008472495fd84072c67b9cd5091001b5533aa7c5d0769b51f324b3603c1d0e40", results: "e0a3409898a52948c2d4ffdd9d0d6060380f7aef1fc2aa99dff6d62a28a958e4" };
const sha = (p) => crypto.createHash("sha256").update(fs.readFileSync(path.join(ROOT, p))).digest("hex");
const fail = (s) => { throw Error(`[BLOCKED] mixed_unit_removal: ${s}`); };
const clone = (x) => JSON.parse(JSON.stringify(x));
const near = (a, b, eps = 1e-9) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= eps;
const GENS = ["G1", "G2", "G3+"], READINGS = ["low", "high"];
const S = { lane: SOURCE, files: Object.fromEntries(Object.entries(FILES).map(([k, p]) => [k, { path: p, sha256: sha(p) }])) };
for (const [key, value] of Object.entries(S.files)) if (value.sha256 !== PINS[key]) fail(`source hash changed: ${value.path}`);
const DATA = JSON.parse(fs.readFileSync(path.join(ROOT, FILES.summary), "utf8"));
// This CSV contains only unquoted identifiers and finite numeric columns.
const csv = fs.readFileSync(path.join(ROOT, FILES.replicates), "utf8").trimEnd().split("\n").map((s) => s.replace(/\r$/, "").split(","));
const head = csv.shift();
if (head.join(",") !== ["method", "end", "component", "generation", ...Array.from({ length: 161 }, (_, i) => `r${i}`)].join(",")) fail("replicate schema changed");
const REPLICATES = new Map();
for (const row of csv) {
  if (row.length !== head.length) fail("replicate CSV field count changed");
  const key = row.slice(0, 4).join("|"), v = row.slice(4).map(Number);
  if (REPLICATES.has(key) || !v.every(Number.isFinite)) fail(`duplicate/nonfinite replicate row ${key}`);
  REPLICATES.set(key, v);
}
const sdr = (v) => Math.sqrt(4 / 160 * v.slice(1).reduce((s, n) => s + (n - v[0]) ** 2, 0));
const sum = (rows) => Array.from({ length: 161 }, (_, r) => rows.reduce((s, row) => s + row[r], 0));
function sourceRow(which, reading, component) {
  const found = DATA.results.filter((r) => r.method === which && r.end === reading && r.component === component);
  if (found.length !== 1) fail(`source row ${which}/${reading}/${component} missing or duplicate`);
  const record = found[0];
  const byGeneration = GENS.map((g) => {
    const v = REPLICATES.get([which, reading, component, g].join("|"));
    if (!v) fail(`replicate generation ${g} missing for ${component}`);
    return v.slice();
  });
  const stack = sum(byGeneration);
  if (!near(stack[0], record.bn) || !near(sdr(stack), record.se_bn)) fail(`${component} total/SE mismatch`);
  byGeneration.forEach((v, g) => {
    if (!near(v[0], record.by_generation_bn[g]) || !near(sdr(v), record.by_generation_se_bn[g])) fail(`${component} generation ${GENS[g]} mismatch`);
  });
  if (!near(record.by_generation_bn.reduce((a, b) => a + b, 0), record.bn)) fail(`${component} generation parts do not close`);
  return { record, byGeneration, stack };
}
const MEMBER = DATA.membership;
const CENTRAL_ADDED_G3 = MEMBER.remaining_added_g3_priced_count + MEMBER.roster_g3_priced_count;
const CENTRAL_RESIDUAL_G3 = MEMBER.remaining_added_g3_priced_count;
const ARMS = {
  off: { label: "v7 child-credit removal convention; no item-11 delta" },
  bounded_low: { label: "bounded low removal at both readings" },
  bounded_high: { label: "bounded high removal at both readings" },
  bounded_high_plus_pension_model: { label: "bounded high plus pension family model; set only" },
};
function countsOf(option) {
  if (option == null || option === "central") return { added_g3: CENTRAL_ADDED_G3, c3: null, source: "source central counts" };
  let p = option;
  if (typeof option === "string") {
    const V7 = require("../main_case_2026_10_14/package.cjs");
    const q = V7.caseOf(V7.V6_PACKAGE.OCT05, V7.CANDIDATE, {}, option);
    p = q.correctionsPayload().meta.lineage;
  }
  if (typeof p.correctionsPayload === "function") p = p.correctionsPayload().meta.lineage;
  if (p.meta && p.meta.lineage) p = p.meta.lineage;
  if (p.lineage) p = p.lineage;
  const counts = p.counts || p;
  const n = p.added_g3 ?? p.added_g3plus_priced ?? p.members?.g3plus ?? (Number.isFinite(counts.later) && Number.isFinite(counts.g3_rate) && Number.isFinite(counts.c3) ? counts.later + (1 - counts.c3) * counts.g3_rate : NaN);
  const c3 = typeof p.c3 === "object" ? p.c3.value : p.c3 ?? counts.c3 ?? null;
  if (!(Number.isFinite(n) && n >= 0)) fail("option has no finite nonnegative added-G3 count");
  return { added_g3: n, c3, source: "option lineage" };
}
function get(option = null, which = "set", arm = null, settings = {}) {
  if (!["set", "cash"].includes(which)) fail(`unknown set ${which}`);
  if (arm != null && !Object.hasOwn(ARMS, arm)) fail(`unknown arm ${arm}`);
  if (which === "cash" && arm === "bounded_high_plus_pension_model") fail("pension model is set only");
  const counts = countsOf(option);
  const scaling = settings.scaling || process.env.ITEM11_D_SCALING || "added_g3_ratio";
  let scale;
  if (scaling === "added_g3_ratio") scale = counts.added_g3 / CENTRAL_ADDED_G3;
  else if (scaling === "residual_g3_ratio") {
    const centralC3 = MEMBER.roster_white_priced_count / MEMBER.latent_third_rate_roster;
    const c3 = counts.c3 == null ? centralC3 : counts.c3;
    const roster = MEMBER.latent_later_loss_roster + (1 - c3) * MEMBER.latent_third_rate_roster;
    const residual = counts.added_g3 - roster;
    if (!(residual >= 0)) fail("option residual G3 count is negative");
    scale = residual / CENTRAL_RESIDUAL_G3;
  } else fail(`unknown D scaling ${scaling}`);
  const by_end = {};
  for (const reading of READINGS) {
    const component = arm === "off" ? `bounded_${reading}` : arm || `bounded_${reading}`;
    const base = sourceRow(which, reading, component), d = sourceRow(which, reading, "D_added_residual");
    const byGeneration = base.byGeneration.map((v, g) => v.map((n, r) => arm === "off" ? 0 : n + d.byGeneration[g][r] * (scale - 1)));
    const stack = sum(byGeneration), gens = Object.fromEntries(GENS.map((g, i) => [g, byGeneration[i][0]]));
    by_end[reading] = { total_bn: stack[0], se_bn: sdr(stack), by_generation_bn: gens,
      by_generation_se_bn: Object.fromEntries(GENS.map((g, i) => [g, sdr(byGeneration[i])])),
      replicates_bn: stack, by_generation_replicates_bn: Object.fromEntries(GENS.map((g, i) => [g, byGeneration[i]])),
      source_component: arm === "off" ? null : component, envelope_arm: arm === "off" ? null : base.record.arm,
      D_added_residual_bn: arm === "off" ? 0 : d.stack[0] * scale };
  }
  return { id: "mixed_unit_removal", which, arm: arm || "central", application: "post_engine_fixed_amount_by_reading",
    low: by_end.low.total_bn, high: by_end.high.total_bn, by_end, source: clone(S),
    generation_aliases: { G3plus: "G3+" },
    replacement_rule: DATA.replacement_rule,
    D_scaling: { rule: scaling, scale, option_added_g3: counts.added_g3, central_added_g3: CENTRAL_ADDED_G3,
      central_residual_g3: CENTRAL_RESIDUAL_G3, only_component_scaled: "D_added_residual", white_amount_bn: 0,
      replicate_rule: "apply the full-sample count ratio to each signed source replicate; option-specific roster count replicates are not regenerated" },
    caveat: "Source rows are v7 deltas, including the one item-5b subtraction and all selected latent health/SNAP interactions. Preserve v7 child_credits. All source policy/calibration assumptions held." };
}
function build(ctx, arm, which) {
  const detail = ctx.DETAIL?.added_age_mix;
  const lineage = detail?.counts ? { counts: detail.counts } : ctx.B?.correctionsPayload().meta.lineage;
  if (!lineage) fail("build context has no authoritative lineage counts");
  const value = get(lineage, which, arm);
  return { edits: [], parts: {}, meta: { mixed_unit_removal: value }, detail: value,
    record: { applied_after_engine: true, total_bn: { low: value.low, high: value.high }, source: clone(S), replacement_rule: value.replacement_rule } };
}
// Validate both methods and all covariance stacks at module load.
for (const w of ["set", "cash"]) for (const reading of READINGS) sourceRow(w, reading, `bounded_${reading}`);
module.exports = { get, build, S, ARMS, GENS, READINGS, CENTRAL_ADDED_G3, CENTRAL_RESIDUAL_G3, countsOf, sdr };
