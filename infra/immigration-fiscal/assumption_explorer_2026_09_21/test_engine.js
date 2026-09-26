/* Gate engine.js against rows selected from the executed exports (derived/test_vectors.json).
 * Run: node test_engine.js   (after build_model.py). Exit code 1 on any mismatch. */
"use strict";
const fs = require("fs");
const path = require("path");
const Engine = require("./engine.js");

const derived = path.join(__dirname, "derived");
const model = JSON.parse(fs.readFileSync(path.join(derived, "model.json"), "utf8"));
// The data corrections adopted on 2026-09-26 (they build on those of 2026-09-24), as the page loads them. Their
// meta.responses carry the adopted school and general-government responses, which the presets read.
const CORRECTED = path.join(__dirname, "..", "main_case_2026_09_26", "derived");
const payload = JSON.parse(fs.readFileSync(path.join(CORRECTED, "corrections.json"), "utf8"));
const RESPONSES = payload.meta.responses;
model.corrected = Engine.applyCorrections(model, payload);
// The September 24 payload stays checkable: the same model with that payload as its corrected copy.
const CORRECTED24 = path.join(__dirname, "..", "main_case_2026_09_24", "derived");
const model24 = Object.assign({}, model, {
  corrected: Engine.applyCorrections(model, JSON.parse(fs.readFileSync(path.join(CORRECTED24, "corrections.json"), "utf8"))) });
const vectors = JSON.parse(fs.readFileSync(path.join(derived, "test_vectors.json"), "utf8"));
const TOLERANCE = 1e-6;  // billions; the exports are rounded at 1e-9
let failures = 0, worst = 0;

function check(label, got, want, tolerance) {
  const gap = Math.abs(got - want);
  if (tolerance === undefined) worst = Math.max(worst, gap);
  if (!(gap <= (tolerance === undefined ? TOLERANCE : tolerance))) {
    failures += 1;
    if (failures <= 10) console.error(`MISMATCH ${label}: engine ${got} executed ${want}`);
  }
}

const scenarioKeys = Object.fromEntries(Object.entries(model.spending.scenarios).map(([k, v]) => [v, k]));

for (const row of vectors.grid) {
  const state = Engine.defaultState(model);
  Engine.PRODUCTION_DIMS.forEach((d) => { state.production[d] = row[d]; });
  state.receipt_scenario = row.receipt_scenario;
  state.spending_keys = scenarioKeys[row.spending_scenario];
  state.allocation = row.allocation;
  state.public_goods_response = row.public_goods_response;
  state.general_government_response = row.public_goods_response;  // one dimension in the executed grid
  state.service_response = row.service_response;
  state.fiscal_weight = row.fiscal_weight;
  const out = Engine.evaluate(model, state);
  check("grid welfare", out.welfare_bn, row.welfare_bn);
  check("grid direct response", out.direct_fiscal_response_bn, row.direct_fiscal_response_bn);
}

for (const c of vectors.service) {
  const state = Engine.defaultState(model);
  state.allocation = c.allocation;
  state.production.normalization = c.normalization;
  state.school_share = c.school_share;
  state.school_response = c.school_response;
  state.other_education_response = c.other_education_response;
  state.delayed_response = c.delayed_response;
  const out = Engine.evaluate(model, state);
  check(`service ${c.profile}/${c.case_id}`, out.welfare_bn, c.welfare_bn);
  check(`service effective response ${c.profile}/${c.case_id}`, out.effective_service_response, c.effective_service_response);
}

for (const a of vectors.accounts) {
  const state = Engine.defaultState(model);
  state.receipt_scenario = a.receipt_scenario;
  state.spending_keys = scenarioKeys[a.spending_scenario];
  state.allocation = a.allocation;
  const out = Engine.evaluate(model, state);
  check("accounting balance", out.target_balance_bn, a.target_balance_bn);
  check("normalized gap", out.normalized_gap_bn, a.normalized_gap_bn);
}

// The published headline spans must fall out of the evaluator's own unresolved-range sweep.
const headline = model.meta.headline.category_service_response_sensitivity;
function span(settings) {
  const state = Object.assign(Engine.defaultState(model), settings);
  return Engine.unresolvedRange(model, state, "welfare_bn");
}
const cbo = span({ other_education_response: 1, delayed_response: 0, school_response_band: [0.63, 0.66] });
check("headline low", cbo[0], headline.cbo_category_lag_non_school_full.min_welfare_bn);
check("headline high", cbo[1], headline.cbo_category_lag_non_school_full.max_welfare_bn);
const proportional = span({});
check("proportional low", proportional[0], headline.proportional_reference.min_welfare_bn);
check("proportional high", proportional[1], headline.proportional_reference.max_welfare_bn);

// Presets as the page loads them: value_from reads a scaling_check.json field or, as responses.<path>, the adopted
// responses in the payload's meta.responses (build_ui.py resolves them the same way); dotted paths set in place.
const presets = JSON.parse(fs.readFileSync(path.join(__dirname, "presets.json"), "utf8")).presets;
const evidence = JSON.parse(fs.readFileSync(path.join(derived, "scaling_check.json"), "utf8"));
const numbers = Object.assign({}, evidence, { responses: RESPONSES });
function readValue(name) {
  const value = name.split(".").reduce((o, k) => (o == null ? undefined : o[k]), numbers);
  if (typeof value !== "number") throw new Error(`value_from names no number: ${name}`);
  return value;
}
function presetState(id, extra) {
  const state = Engine.defaultState(model);
  for (const s of presets.find((p) => p.id === id).settings || []) {
    if (!s.path) continue;
    const value = s.value_from === undefined ? s.value : Array.isArray(s.value_from) ? s.value_from.map(readValue) : readValue(s.value_from);
    const keys = s.path.split("."), last = keys.pop();
    keys.reduce((o, k) => o[k], state)[last] = JSON.parse(JSON.stringify(value));
  }
  return Object.assign(state, extra || {});
}
function costBand(state, m) {  // welfare sign flipped: the main-case lane reports cost as positive bn
  const range = Engine.unresolvedRange(m || model, state, "welfare_bn");
  return [-range[1], -range[0]];
}

// September 20 conventions still reproduce the published bands, on the data as they stood.
const sept20 = costBand(presetState("repo_central", { data_corrections: false }));
check("September 20 central low", sept20[0], -headline.cbo_category_lag_non_school_full.max_welfare_bn);
check("September 20 central high", sept20[1], -headline.cbo_category_lag_non_school_full.min_welfare_bn);

// The three profiles each main-case lane reports: the central preset, the same with non-school education fixed,
// and the proportional preset. Before 2026-09-26 the responses were the marginal rates themselves: general
// government from scaling_check.json, as the September 23 and 24 lanes read it, and schools CBO's 0.63/0.66, which
// meta.responses records as the elasticities. The proportional profile holds schools at 1.
const MARGINAL_GG = { general_government_response: evidence.composite_low, general_government_response_band: [evidence.composite_low, evidence.composite_high] };
const MARGINAL = Object.assign({ school_response: RESPONSES.school.elasticity[0], school_response_band: RESPONSES.school.elasticity.slice() }, MARGINAL_GG);
const PROFILES = [
  { label: "central", profile: "cbo_category_lag_non_school_full", state: (extra, marginal) => presetState("repo_central_gg", Object.assign({}, marginal ? MARGINAL : {}, extra)) },
  { label: "non-school education fixed", profile: "cbo_category_lag_non_school_fixed",
    state: (extra, marginal) => presetState("repo_central_gg", Object.assign({ other_education_response: 0 }, marginal ? MARGINAL : {}, extra)) },
  { label: "proportional", profile: "proportional_reference", state: (extra, marginal) => presetState("proportional", Object.assign({}, marginal ? MARGINAL_GG : {}, extra)) },
];
const ON = { data_corrections: true }, OFF = { data_corrections: false };
const PRINTED = 5e-5 + 1e-9;  // the lanes' CSVs print four decimals: half a unit of the last digit
let adoptedChecks = 0;

// September 23 (main_case_2026_09_23): the uncorrected data at the marginal rates. Checked to its CSV and to the lane's
// own identity at full precision: published band + GG response x GG amount + justice change + uncompensated-care
// change, from its inputs.json.
const MAIN = path.join(__dirname, "..", "main_case_2026_09_23", "derived");
function readBands(dir) {
  const bands = {};
  fs.readFileSync(path.join(dir, "main_case_bands.csv"), "utf8").trim().split("\n").slice(1).forEach((line) => {
    const [profile, variant, low, high] = line.split(",");
    bands[`${profile}/${variant}`] = [Number(low), Number(high)];
  });
  return bands;
}
const bands23 = readBands(MAIN), bands24 = readBands(CORRECTED24), bands26 = readBands(CORRECTED);
const inputs = JSON.parse(fs.readFileSync(path.join(MAIN, "inputs.json"), "utf8"));
function checkBand(label, band, bands, key, lane) {
  if (!bands[key]) { failures += 1; console.error(`MISMATCH ${label}: ${lane} has no band ${key}`); return; }
  check(`${label} low vs ${lane} ${key}`, band[0], bands[key][0], PRINTED);
  check(`${label} high vs ${lane} ${key}`, band[1], bands[key][1], PRINTED);
  adoptedChecks += 1;
}
const result = {};
for (const p of PROFILES) {
  const band = result[`sept23/${p.profile}`] = costBand(p.state(OFF, true));
  const published = headline[p.profile], gg = inputs.general_government_response, ggBn = inputs.general_government_target_bn;
  const j = inputs.justice_change_bn.central, uc = inputs.uncompensated_inside_bn;
  checkBand(`September 23 ${p.label}`, band, bands23, `${p.profile}/adopted`, "main_case_2026_09_23");
  check(`September 23 ${p.label} low vs lane identity`, band[0], -published.max_welfare_bn + gg.low * ggBn + j + uc.equal_low);
  check(`September 23 ${p.label} high vs lane identity`, band[1], -published.min_welfare_bn + gg.high * ggBn + j + uc.equal_high);
}

// September 24 (main_case_2026_09_24): its payload at the marginal rates, the case adopted that day.
for (const p of PROFILES) {
  checkBand(`September 24 ${p.label}`, result[`sept24/${p.profile}`] = costBand(p.state(ON, true), model24), bands24, `${p.profile}/adopted`, "main_case_2026_09_24");
}

// September 26 (main_case_2026_09_26), with the switch set explicitly: the adopted case, and with the corrections off
// the uncorrected model at the adopted responses, the gate for the uncorrected model.
for (const p of PROFILES) {
  checkBand(`September 26 ${p.label}`, result[`sept26/${p.profile}`] = costBand(p.state(ON)), bands26, `${p.profile}/adopted`, "main_case_2026_09_26");
  checkBand(`Uncorrected at the adopted responses, ${p.label}`, result[`uncorrected/${p.profile}`] = costBand(p.state(OFF)), bands26,
    `${p.profile}/uncorrected_at_adopted_responses`, "main_case_2026_09_26");
}

// Presets as loaded, with no override: the page's central case and the proportional benchmark carry the corrections
// and the adopted responses, and reproduce main_case_2026_09_26; the September 20 case has the corrections off;
// every other convention runs on the corrected data.
function checkSwitch(label, got, want) {
  if (got !== want) { failures += 1; console.error(`MISMATCH ${label}: data_corrections is ${got}, expected ${want}`); }
}
function checkSame(label, got, want) {
  if (JSON.stringify(got) !== JSON.stringify(want)) { failures += 1; console.error(`MISMATCH ${label}: ${JSON.stringify(got)}, expected ${JSON.stringify(want)}`); }
}
const central = presets.filter((p) => p.central);
checkSwitch("exactly one central preset", central.length, 1);
const loaded = costBand(presetState(central[0].id));
checkBand(`central preset ${central[0].id} as loaded`, loaded, bands26, "cbo_category_lag_non_school_full/adopted", "main_case_2026_09_26");
checkBand("proportional preset as loaded", costBand(presetState("proportional")), bands26, "proportional_reference/adopted", "main_case_2026_09_26");
for (const p of presets) checkSwitch(`preset ${p.id} as loaded`, presetState(p.id).data_corrections, p.id !== "repo_central");
const GG = [RESPONSES.general_government.low, RESPONSES.general_government.high], SCHOOL = [RESPONSES.school.growth, RESPONSES.school.decline];
for (const id of [central[0].id, "proportional"]) {
  const s = presetState(id);
  checkSame(`${id} general-government responses as loaded`, [s.general_government_response, s.general_government_response_band], [GG[0], GG]);
  if (id !== "proportional") checkSame(`${id} school responses as loaded`, [s.school_response, s.school_response_band], [SCHOOL[0], SCHOOL]);
}

// Attribution must be exhaustive: Shapley effects sum to the total difference.
const from = Engine.defaultState(model);
const to = Object.assign(Engine.defaultState(model), { service_response: 0.5, public_goods_response: 1, count_production: false });
to.production.sigma = 1.5;
const paths = ["service_response", "public_goods_response", "count_production", "production.sigma"];
const parts = Engine.attribute(model, from, to, paths, "welfare_bn");
check("attribution closure", parts.reduce((s, p) => s + p.effect_bn, 0),
  Engine.evaluate(model, to).welfare_bn - Engine.evaluate(model, from).welfare_bn);
// The data switch attributes like any other control.
const on = presetState("repo_central_gg", ON), off = presetState("repo_central_gg", { ...OFF, general_government_response: 0.84 });
const dataParts = Engine.attribute(model, on, off, ["data_corrections", "general_government_response"], "welfare_bn");
check("attribution closure with the data switch", dataParts.reduce((s, p) => s + p.effect_bn, 0),
  Engine.evaluate(model, off).welfare_bn - Engine.evaluate(model, on).welfare_bn);

// applyCorrections keeps every edited cell's base: target / share is the same before and after.
let baseChecks = 0;
for (const side of ["receipts", "spending"]) {
  model[side].lines.forEach((line) => {
    const fixed = model.corrected[side].lines.find((l) => l.id === line.id);
    for (const [k, cell] of Object.entries(side === "receipts" ? line.cells : line.keys)) {
      const after = (side === "receipts" ? fixed.cells : fixed.keys)[k];
      for (const a of ["personal", "shared"]) {
        if (!cell[a].share || after[a].target_bn === cell[a].target_bn) continue;
        check(`share base ${line.id}/${k}/${a}`, after[a].target_bn / after[a].share, cell[a].target_bn / cell[a].share, 1e-6);
        baseChecks += 1;
      }
    }
  });
}
if (baseChecks < 400) { failures += 1; console.error(`MISMATCH share-base checks: only ${baseChecks} edited cells`); }

const counts = `${vectors.grid.length} grid rows, ${vectors.service.length} service cases, ${vectors.accounts.length} accounting cases`;
if (failures) { console.error(`FAIL: ${failures} mismatches over ${counts}; worst gap ${worst}`); process.exit(1); }
const bn = (b) => `${b[0].toFixed(4)} to ${b[1].toFixed(4)} bn`, MAIN_PROFILE = "cbo_category_lag_non_school_full";
console.log(`PASS: ${counts}, 4 headline bounds, September 20 central preset, ${adoptedChecks} adopted bands ` +
  `(central: September 23 ${bn(result[`sept23/${MAIN_PROFILE}`])}; September 24 ${bn(result[`sept24/${MAIN_PROFILE}`])}; ` +
  `September 26 ${bn(result[`sept26/${MAIN_PROFILE}`])}, as loaded ${bn(loaded)}; uncorrected at the adopted responses ` +
  `${bn(result[`uncorrected/${MAIN_PROFILE}`])}), data switch on every preset as loaded (off only for repo_central), adopted responses ` +
  `as loaded, attribution closure, ${baseChecks} corrected shares on their base; worst gap ${worst.toExponential(2)} bn`);
