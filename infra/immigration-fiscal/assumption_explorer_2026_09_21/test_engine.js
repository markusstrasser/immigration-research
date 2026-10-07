/* Gate engine.js and case.js. Run: node test_engine.js   (after build_model.py). Exit code 1 on any mismatch.
 *
 * 1. engine.js against rows selected from the executed exports (derived/test_vectors.json) and the published
 *    September 20 headline spans.
 * 2. engine.js against the bands of the main-case lanes of September 23, 24 and 26, which executed it. Their states
 *    are written out below as the page loaded them before it moved to the case of 2026-10-07 (presets.json at
 *    d434f272): a regression gate on the engine, not cases the page shows.
 * 3. case.js and presets.json against the adopted main case (main_case_2026_10_07): the central preset as loaded at
 *    1e-6, every lane reading, the per-member figures, the readouts' files, the case's fail-loud guards and
 *    attribution closure. */
"use strict";
const fs = require("fs");
const path = require("path");
const Engine = require("./engine.js");
const Case = require("./case.js");

const derived = path.join(__dirname, "derived");
const read = (...parts) => JSON.parse(fs.readFileSync(path.join(...parts), "utf8"));
const model = read(derived, "model.json");
// The data corrections of 2026-09-26 (they build on those of 2026-09-24), behind the engine's data switch.
const CORRECTED = path.join(__dirname, "..", "main_case_2026_09_26", "derived");
const RESPONSES26 = read(CORRECTED, "corrections.json").meta.responses;
model.corrected = Engine.applyCorrections(model, read(CORRECTED, "corrections.json"));
// The September 24 payload stays checkable: the same model with that payload as its corrected copy.
const CORRECTED24 = path.join(__dirname, "..", "main_case_2026_09_24", "derived");
const model24 = Object.assign({}, model, { corrected: Engine.applyCorrections(model, read(CORRECTED24, "corrections.json")) });
const vectors = read(derived, "test_vectors.json");
const evidence = read(derived, "scaling_check.json");
const TOLERANCE = 1e-6;  // billions; the exports are rounded at 1e-9
const PRINTED = 5e-5 + 1e-9;  // the lanes' CSVs print four decimals: half a unit of the last digit
let failures = 0, worst = 0, adoptedChecks = 0;

function check(label, got, want, tolerance) {
  const gap = Math.abs(got - want);
  if (tolerance === undefined) worst = Math.max(worst, gap);
  if (!(gap <= (tolerance === undefined ? TOLERANCE : tolerance))) {
    failures += 1;
    if (failures <= 10) console.error(`MISMATCH ${label}: got ${got}, expected ${want}`);
  }
}
function checkSame(label, got, want) {
  if (JSON.stringify(got) !== JSON.stringify(want)) { failures += 1; console.error(`MISMATCH ${label}: ${JSON.stringify(got)}, expected ${JSON.stringify(want)}`); }
}
function checkThrows(label, fn, pattern) {
  try { fn(); } catch (error) { if (pattern.test(error.message)) return; failures += 1; console.error(`MISMATCH ${label}: threw ${error.message}`); return; }
  failures += 1; console.error(`MISMATCH ${label}: did not throw`);
}

/* ---------- 1. engine.js against the executed exports ---------- */
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

// The published September 20 headline spans fall out of the evaluator's own unresolved-range sweep.
const headline = model.meta.headline.category_service_response_sensitivity;
function span(settings) {
  return Engine.unresolvedRange(model, Object.assign(Engine.defaultState(model), settings), "welfare_bn");
}
const cbo = span({ other_education_response: 1, delayed_response: 0, school_response_band: [0.63, 0.66] });
check("headline low", cbo[0], headline.cbo_category_lag_non_school_full.min_welfare_bn);
check("headline high", cbo[1], headline.cbo_category_lag_non_school_full.max_welfare_bn);
const proportional = span({});
check("proportional low", proportional[0], headline.proportional_reference.min_welfare_bn);
check("proportional high", proportional[1], headline.proportional_reference.max_welfare_bn);

/* ---------- 2. engine.js against the earlier main-case lanes ---------- */
function costBand(state, m) {  // welfare sign flipped: the main-case lanes report cost as positive bn
  const range = Engine.unresolvedRange(m || model, state, "welfare_bn");
  return [-range[1], -range[0]];
}
// The September 26 central case and proportional benchmark as the page loaded them, at September 26's responses.
function sept26(kind, extra) {
  const s = Engine.defaultState(model), R = RESPONSES26;
  Object.assign(s, { data_corrections: true, general_government_response: R.general_government.low,
    general_government_response_band: [R.general_government.low, R.general_government.high] });
  s.key_override.public_order_safety = "use";
  s.key_override.medicaid_and_chip_other_medical = "uninsured_use_low";
  s.key_band.medicaid_and_chip_other_medical = ["uninsured_use_low", "uninsured_use_high"];
  if (kind === "central") Object.assign(s, { school_response: R.school.growth, school_response_band: [R.school.growth, R.school.decline], other_education_response: 1, delayed_response: 0 });
  return Object.assign(s, extra || {});
}
// Before 2026-09-26 the responses were the marginal rates themselves: general government from scaling_check.json, as
// the September 23 and 24 lanes read it, and schools CBO's 0.63/0.66, which meta.responses records as the
// elasticities. The proportional profile holds schools at 1.
const MARGINAL_GG = { general_government_response: evidence.composite_low, general_government_response_band: [evidence.composite_low, evidence.composite_high] };
const MARGINAL = Object.assign({ school_response: RESPONSES26.school.elasticity[0], school_response_band: RESPONSES26.school.elasticity.slice() }, MARGINAL_GG);
const PROFILES = [
  { label: "central", profile: "cbo_category_lag_non_school_full", state: (extra, marginal) => sept26("central", Object.assign({}, marginal ? MARGINAL : {}, extra)) },
  { label: "non-school education fixed", profile: "cbo_category_lag_non_school_fixed",
    state: (extra, marginal) => sept26("central", Object.assign({ other_education_response: 0 }, marginal ? MARGINAL : {}, extra)) },
  { label: "proportional", profile: "proportional_reference", state: (extra, marginal) => sept26("proportional", Object.assign({}, marginal ? MARGINAL_GG : {}, extra)) },
];
const ON = { data_corrections: true }, OFF = { data_corrections: false };

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
const inputs = read(MAIN, "inputs.json");
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
// September 26 (main_case_2026_09_26): the case, and with the corrections off the uncorrected model at its responses.
for (const p of PROFILES) {
  checkBand(`September 26 ${p.label}`, result[`sept26/${p.profile}`] = costBand(p.state(ON)), bands26, `${p.profile}/adopted`, "main_case_2026_09_26");
  checkBand(`Uncorrected at the adopted responses, ${p.label}`, result[`uncorrected/${p.profile}`] = costBand(p.state(OFF)), bands26,
    `${p.profile}/uncorrected_at_adopted_responses`, "main_case_2026_09_26");
}

// Attribution is exhaustive: Shapley effects sum to the total difference, the data switch included.
const from = Engine.defaultState(model);
const to = Object.assign(Engine.defaultState(model), { service_response: 0.5, public_goods_response: 1, count_production: false });
to.production.sigma = 1.5;
const parts = Engine.attribute(model, from, to, ["service_response", "public_goods_response", "count_production", "production.sigma"], "welfare_bn");
check("engine attribution closure", parts.reduce((s, p) => s + p.effect_bn, 0), Engine.evaluate(model, to).welfare_bn - Engine.evaluate(model, from).welfare_bn);
const on26 = sept26("central", ON), off26 = sept26("central", { data_corrections: false, general_government_response: 0.84 });
const dataParts = Engine.attribute(model, on26, off26, ["data_corrections", "general_government_response"], "welfare_bn");
check("engine attribution closure with the data switch", dataParts.reduce((s, p) => s + p.effect_bn, 0),
  Engine.evaluate(model, off26).welfare_bn - Engine.evaluate(model, on26).welfare_bn);

/* ---------- 3. case.js and presets.json against the adopted main case ---------- */
const CASE = path.join(__dirname, "..", "main_case_2026_10_07", "derived");
const payloads = { accrual: read(CASE, "corrections.json"), cash: read(CASE, "corrections_cash.json") };
const caseModel = read(derived, "model.json");
const C = Case.create(caseModel, payloads), R = C.responses;
const summary = read(CASE, "summary.json");
const presetsFile = read(__dirname, "presets.json"), PRESETS = presetsFile.presets;
const byId = Object.fromEntries(PRESETS.map((p) => [p.id, p]));
const numbers = Object.assign({}, evidence, { responses: R });
function readValue(name) {
  const value = name.split(".").reduce((o, k) => (o == null ? undefined : o[k]), numbers);
  if (typeof value !== "number") throw new Error(`value_from names no number: ${name}`);
  return value;
}
function valueOf(s) { return s.value_from === undefined ? s.value : Array.isArray(s.value_from) ? s.value_from.map(readValue) : readValue(s.value_from); }
function setPath(state, p, v) {  // a null value removes the field, as for a band a preset drops
  const keys = p.split("."), last = keys.pop(), o = keys.reduce((x, k) => x[k], state);
  if (v === null) delete o[last]; else o[last] = JSON.parse(JSON.stringify(v));
}
function presetState(p) {  // as ui.js loads a preset: the case's defaults, the base's settings, then its own
  const s = C.defaultState();
  for (const x of (p.extends ? byId[p.extends].settings : []).concat(p.settings || [])) if (x.path) setPath(s, x.path, valueOf(x));
  return s;
}
const caseBand = (s) => { const r = C.range(s, "welfare_bn"); return [-r[1], -r[0]]; };
function fieldOf(node, dotted) { return dotted.split(".").reduce((o, k) => (o == null ? undefined : o[k]), node); }
function checkFull(label, band, want) {
  if (!Array.isArray(want) || want.length !== 2) { failures += 1; console.error(`MISMATCH ${label}: no band in the lane's file`); return; }
  check(`${label} low`, band[0], want[0]); check(`${label} high`, band[1], want[1]); adoptedChecks += 1;
}

const centrals = PRESETS.filter((p) => p.central);
checkSame("exactly one central preset", centrals.length, 1);
const CENTRAL = presetState(centrals[0]), loaded = caseBand(CENTRAL);
checkFull(`central preset ${centrals[0].id} as loaded vs summary.json main_case`, loaded, summary.main_case);
checkSame("central preset's general-government responses as loaded",
  [CENTRAL.general_government_response, CENTRAL.general_government_response_band], [R.general_government.low, [R.general_government.low, R.general_government.high]]);
checkSame("central preset's school response and readings as loaded", [CENTRAL.school_response, CENTRAL.reading, CENTRAL.reading_band], [R.school.growth, "low", ["low", "high"]]);

// Every state the case lane ran too: the central preset with stated changes, against summary.json at full precision
// or the bands CSV at its printed precision.
const bandsCase = readBands(CASE), lane = presetsFile.lane_readings, laneStates = [];
for (const row of lane.rows) {
  const s = JSON.parse(JSON.stringify(CENTRAL));
  Object.entries(row.changes).forEach(([p, v]) => setPath(s, p, v));
  laneStates.push(s);
  const band = caseBand(s);
  if (row.field) checkFull(`lane reading ${row.label} vs summary.json ${row.field}`, band, fieldOf(summary, row.field));
  else checkBand(`lane reading ${row.label}`, band, bandsCase, `long_run_non_school_full/${row.csv_variant}`, "main_case_2026_10_07");
}
// A preset that is a lane reading is gated as one: the cash set and the proportional benchmark.
const canon = (v) => Array.isArray(v) ? `[${v.map(canon).join(",")}]` : v && typeof v === "object"
  ? `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${canon(v[k])}`).join(",")}}` : JSON.stringify(v);
for (const id of ["cash_set", "proportional"]) {
  checkSame(`preset ${id} is a lane reading`, laneStates.some((s) => canon(s) === canon(presetState(byId[id]))), true);
}
// Per-member figures divide by the lineage the case counts.
const perMember = summary.v6.per_member_usd;
check("lineage population", C.lineage_population, perMember.population);
const cashBand = caseBand(Object.assign(JSON.parse(JSON.stringify(CENTRAL)), { benefits: "cash" }));
[["set", loaded], ["cash", cashBand]].forEach(([k, band]) => band.forEach((x, i) => check(`per member, ${k} ${i ? "high" : "low"}`, x * 1e9 / C.lineage_population, perMember[k][i])));

// Every preset loads and evaluates to a finite band; its paths exist in the case's state.
const known = new Set(Object.keys(C.defaultState()).concat(["school_response_band", "general_government_response_band", "reading_band"]));
for (const p of PRESETS) {
  for (const x of p.settings || []) if (x.path && !known.has(x.path.split(".")[0])) { failures += 1; console.error(`MISMATCH preset ${p.id}: unknown path ${x.path}`); }
  const band = caseBand(presetState(p));
  if (!band.every(Number.isFinite)) { failures += 1; console.error(`MISMATCH preset ${p.id}: band ${band}`); }
}

// Readouts: the lane file holds the band, and a CSV readout's file is on this case.
for (const r of presetsFile.readouts) {
  if (r.source.csv) {
    const rows = {};
    const [head, ...lines] = fs.readFileSync(path.join(__dirname, "..", r.source.csv), "utf8").trim().split("\n");
    const cols = head.split(",");
    lines.forEach((line) => { const cells = line.split(","); rows[cells[0]] = [Number(cells[cols.indexOf("cost_low_bn")]), Number(cells[cols.indexOf("cost_high_bn")])]; });
    [r.source.arm, r.source.cash_arm].forEach((arm) => { if (!rows[arm] || !rows[arm].every(Number.isFinite)) { failures += 1; console.error(`MISMATCH readout ${r.id}: no arm ${arm}`); } });
    check(`readout ${r.id}: its file's adopted low`, rows[r.source.adopted_arm][0], summary.main_case[0], PRINTED);
    check(`readout ${r.id}: its file's adopted high`, rows[r.source.adopted_arm][1], summary.main_case[1], PRINTED);
  } else {
    const node = read(__dirname, "..", r.source.json), band = fieldOf(node, r.source.path);
    if (!(Array.isArray(band) && band.length === 2 && band.every(Number.isFinite)) || typeof fieldOf(node, r.source.rule_path) !== "string") {
      failures += 1; console.error(`MISMATCH readout ${r.id}: no band at ${r.source.path} or rule at ${r.source.rule_path}`);
    }
  }
}

// Attribution over the case's own fields closes exactly.
const away = Object.assign(JSON.parse(JSON.stringify(CENTRAL)), { benefits: "cash", long_run: 0, capital: "private", enterprises: "A", service_response: 0.5, general_government_response: 0.84 });
away.production.sigma = caseModel.production.dims.sigma[0];
const casePaths = ["benefits", "long_run", "capital", "enterprises", "service_response", "general_government_response", "production.sigma"];
const caseParts = C.attribute(CENTRAL, away, casePaths, "welfare_bn");
check("case attribution closure", caseParts.reduce((s, p) => s + p.effect_bn, 0), C.evaluate(away).welfare_bn - C.evaluate(CENTRAL).welfare_bn, 1e-9);
checkSame("case attribution covers every changed field", caseParts.length, casePaths.length);

// The case refuses a payload pair that is not one adopted case.
const tamper = (fn) => { const p = JSON.parse(JSON.stringify(payloads)); fn(p); return p; };
checkThrows("guard: cash set with other responses", () => Case.create(caseModel, tamper((p) => { p.cash.meta.responses.general_government.low += 0.01; })), /\[BLOCKED\] the cash set differs/);
checkThrows("guard: no capital components", () => Case.create(caseModel, tamper((p) => { p.accrual.meta.capital_return.components = []; })), /\[BLOCKED\].*no meta.capital_return components/);
checkThrows("guard: two adoptions", () => Case.create(caseModel, tamper((p) => { p.cash.meta.adopted = "2026-10-05"; })), /\[BLOCKED\] the two payloads are not one adopted case/);

// applyCorrections keeps every edited cell's base: target / share moves only with the line's national total. A cell
// whose national amount is zero has no base, and an edit there gives the group part of nothing: it must stay zero.
// One such cell is known, in the case's payload: the added descendants' edit (edit 521, in meta.lineage's edits)
// carries +0.4474bn of corporate tax borne by labor to the all-capital rule, under which that line is zero nationally
// (others take −0.4474bn). The reference rule is unaffected, and the page counts the line only when the reader moves the
// indirect-receipt response off 0 under that rule. Reported to the case lane on 2026-10-08; any other such cell fails.
const ZERO_CELL_KNOWN = new Set(["main case receipts/corporate_labor/corporate_all_capital", "cash set receipts/corporate_labor/corporate_all_capital"]);
let baseChecks = 0;
function checkBases(label, before, after) {
  let n = 0;
  for (const side of ["receipts", "spending"]) {
    before[side].lines.forEach((line) => {
      const fixed = after[side].lines.find((l) => l.id === line.id), scale = line.national_bn ? fixed.national_bn / line.national_bn : 1;
      for (const [k, cell] of Object.entries(side === "receipts" ? line.cells : line.keys)) {
        const edited = (side === "receipts" ? fixed.cells : fixed.keys)[k], where = `${label} ${side}/${line.id}/${k}`;
        for (const a of ["personal", "shared"]) {
          if (cell[a].target_bn === 0 && cell[a].other_bn === 0) {
            if (edited[a].target_bn !== 0 && !ZERO_CELL_KNOWN.has(where)) { failures += 1; console.error(`MISMATCH ${where}/${a}: an edit on a zero national amount (${edited[a].target_bn} bn)`); }
            continue;
          }
          if (!cell[a].share || edited[a].target_bn === cell[a].target_bn) continue;
          check(`${where}/${a} share base`, edited[a].target_bn / edited[a].share, scale * cell[a].target_bn / cell[a].share, 1e-6);
          n += 1;
        }
      }
    });
  }
  if (n < 400) { failures += 1; console.error(`MISMATCH ${label} share-base checks: only ${n} edited cells`); }
  baseChecks += n;
}
checkBases("September 26", model, model.corrected);
checkBases("main case", caseModel, C.models.accrual);
checkBases("cash set", caseModel, C.models.cash);

const counts = `${vectors.grid.length} grid rows, ${vectors.service.length} service cases, ${vectors.accounts.length} accounting cases`;
if (failures) { console.error(`FAIL: ${failures} mismatches over ${counts}; worst gap ${worst}`); process.exit(1); }
const bn = (b) => `${b[0].toFixed(4)} to ${b[1].toFixed(4)} bn`;
console.log(`PASS: ${counts}, 4 headline bounds, ${adoptedChecks} lane bands (earlier lanes' central: September 23 ` +
  `${bn(result["sept23/cbo_category_lag_non_school_full"])}, September 24 ${bn(result["sept24/cbo_category_lag_non_school_full"])}, ` +
  `September 26 ${bn(result["sept26/cbo_category_lag_non_school_full"])}); main case as loaded ${bn(loaded)}, cash set ${bn(cashBand)}, ` +
  `${lane.rows.length} lane readings, ${PRESETS.length} presets, ${presetsFile.readouts.length} readouts, per-member figures, ` +
  `attribution closure, 3 case guards, ${baseChecks} corrected shares on their base; worst gap ${worst.toExponential(2)} bn`);
