/* The complete account as the figures evaluate it: the explorer's engine on its executed model and on
 * that model with the data corrections adopted on 2026-09-24, one cost() per evaluation, the main
 * case's unresolved dimensions and the published bands the gates compare against. build_data.cjs
 * (the figures page) and proto_data.cjs (the prototypes page) both load it, so every figure runs on
 * one definition of the account.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const scaling = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "scaling_check.json"), "utf8"));
// The data corrections adopted on 2026-09-24 (dataset audit and outside checks) as the engine's cell
// edits, written by main_case_2026_09_24/main_case.cjs after its gates; the gates below check that
// the corrected model reproduces the published bands.
const MAIN_CASE = path.join(FISCAL, "main_case_2026_09_24");
const corrections = JSON.parse(fs.readFileSync(path.join(MAIN_CASE, "derived", "corrections.json"), "utf8"));
const MODELS = {
  base: model,
  taxes: Engine.applyCorrections(model, { lines: corrections.lines, edits: corrections.edits.filter((e) => e.side === "receipt") }),
  adopted: Engine.applyCorrections(model, corrections),
};
// The correction lines by response class (engine.js); cost() sets their responses explicitly.
const CORR = Object.fromEntries(corrections.lines.map((l) => [l.response_class, l.id]));
if (!CORR.education_school_part || !CORR.education_other_part || !CORR.correction_constant) {
  throw new Error("corrections.json lacks a correction line class");
}

let failureCount = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failureCount += 1;
}
const failures = () => failureCount;
const near = (a, b, tol = 1e-6) => Math.abs(a - b) < tol;
const round = (x, d = 4) => Math.round(x * 10 ** d) / 10 ** d;

/* RFC 4180 reader: several lane files quote fields that contain commas. */
function readCsv(file) {
  const text = fs.readFileSync(file, "utf8");
  const rows = [];
  let row = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; } else quoted = false;
      } else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); rows.push(row); row = []; field = "";
    } else field += c;
  }
  if (field !== "" || row.length) { row.push(field); rows.push(row); }
  const [head, ...body] = rows.filter((r) => !(r.length === 1 && r[0] === ""));
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}

function product(dims) {
  return Object.entries(dims).reduce(
    (acc, [name, levels]) => acc.flatMap((spec) => levels.map((v) => ({ ...spec, [name]: v }))),
    [{}],
  );
}
const span = (xs) => [Math.min(...xs), Math.max(...xs)];

/* ---------------------------------------------------------------- complete account ---------- */

const SHARES = Engine.schoolShareBounds(model);
const GG = [scaling.composite_low, scaling.composite_high];
const CBO_SCHOOLS = [0.63, 0.66];
const serviceLines = model.spending.lines.filter((l) => l.response_class === "service").map((l) => l.id).sort();
gate("service lines are the seven the figures set", JSON.stringify(serviceLines) === JSON.stringify([
  "economic_affairs_services", "education_services", "health_services", "housing_community_services",
  "income_security_services", "public_order_safety", "recreation_culture"]), serviceLines.join(" "));

/* One evaluation. spec: allocation, normalization, share, school, gg, uc, justice, receipts,
 * production. r: responses by service family; schools may be "cbo" (take spec.school). m: one of
 * MODELS. */
function cost(spec, r, m = MODELS.base) {
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = spec.receipts || model.receipts.reference;
  if (spec.production) Object.assign(s.production, spec.production);
  if (spec.normalization) s.production.normalization = spec.normalization;
  s.count_production = r.production;
  s.general_government_response = r.gg === "band" ? spec.gg : r.gg;
  s.key_override = {};
  if (spec.justice) s.key_override.public_order_safety = spec.justice;
  if (r.uc !== false && spec.uc) s.key_override.medicaid_and_chip_other_medical = spec.uc;
  const schools = r.schools === "cbo" ? spec.school : r.schools;
  s.response_override = {
    education_services: spec.share * schools + (1 - spec.share) * r.colleges,
    public_order_safety: r.police,
    health_services: r.health,
    income_security_services: r.other,
    housing_community_services: r.other,
    economic_affairs_services: r.delayed,
    recreation_culture: r.delayed,
    // The correction lines (absent from the base model): the school price at the school response,
    // the college re-key at the college response, correction constants in full.
    [CORR.education_school_part]: spec.share * schools,
    [CORR.education_other_part]: (1 - spec.share) * r.colleges,
    [CORR.correction_constant]: 1,
  };
  return -Engine.evaluate(m, s).welfare_bn; // positive = cost to other US residents
}

const bands = readCsv(path.join(MAIN_CASE, "derived", "main_case_bands.csv"));
const band = (profile, variant) => {
  const row = bands.find((b) => b.profile === profile && b.variant === variant);
  if (!row) throw new Error(`no band ${profile} / ${variant}`);
  return [Number(row.cost_low_bn), Number(row.cost_high_bn)];
};
const MAIN = band("cbo_category_lag_non_school_full", "adopted");
const FIXED_COLLEGES = band("cbo_category_lag_non_school_fixed", "adopted");
const PROPORTIONAL = band("proportional_reference", "adopted");
const BEFORE = band("cbo_category_lag_non_school_full", "adopted_2026_09_23");  // before the corrections
const BY_SIDE = JSON.parse(fs.readFileSync(path.join(MAIN_CASE, "derived", "summary.json"), "utf8")).by_side;

// The main case's unresolved dimensions: its published band is the envelope over these.
const MAIN_DIMS = {
  allocation: ["personal", "shared"], normalization: ["cash", "gdp"], share: SHARES,
  school: CBO_SCHOOLS, gg: GG, uc: ["uninsured_use_low", "uninsured_use_high"], justice: ["use"],
};
const mainSpecs = product(MAIN_DIMS);

/* Explorer presets as its page and test_engine.js load them: value_from read from scaling_check.json,
 * dotted paths set in place. The model carries the corrected data for presets that switch them on. */
const presets = JSON.parse(fs.readFileSync(path.join(EXPLORER, "presets.json"), "utf8")).presets;
const presetModel = Object.assign(Engine.clone(model), { corrected: MODELS.adopted });
function presetState(id, extra) {
  const preset = presets.find((p) => p.id === id);
  if (!preset) throw new Error(`no preset ${id}`);
  const state = Engine.defaultState(presetModel);
  for (const s of preset.settings || []) {
    if (!s.path) continue;
    const value = s.value_from === undefined ? s.value
      : Array.isArray(s.value_from) ? s.value_from.map((k) => scaling[k]) : scaling[s.value_from];
    const keys = s.path.split("."), last = keys.pop();
    keys.reduce((o, k) => o[k], state)[last] = JSON.parse(JSON.stringify(value));
  }
  return Object.assign(state, extra || {});
}
// Cost to other residents (positive) over the preset's unresolved dimensions.
function presetCost(id, extra) {
  const range = Engine.unresolvedRange(presetModel, presetState(id, extra), "welfare_bn");
  return [-range[1], -range[0]];
}

module.exports = {
  fs, path, HERE, FISCAL, EXPLORER, MAIN_CASE, Engine, model, scaling, corrections, MODELS, CORR,
  gate, failures, near, round, readCsv, product, span, SHARES, GG, CBO_SCHOOLS, cost, band, MAIN,
  FIXED_COLLEGES, PROPORTIONAL, BEFORE, BY_SIDE, MAIN_DIMS, mainSpecs, presets, presetModel, presetState,
  presetCost,
};
