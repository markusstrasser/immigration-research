/* A payload consumer with no package: engine.js, model.json and a corrections payload give the case's 64
 * specifications, their engine states, capital returns and costs. It generalizes the September 27 lane's independent
 * path (main_case_long_run_2026_09_27/main_case.cjs, independentCosts) to what candidate v4's payload adds:
 *   - new receipt lines, national-scale edits and a production grid, which engine.js applies;
 *   - every line and receipt response in meta.responses: an entry with receipt true sets its override, and an entry
 *     named for a spending line of the corrected model sets that line's response, at the specification's reading;
 *   - the capital return's key kinds, part_rekeyed included (a part of a parent line re-keyed by a correction line:
 *     the parent's amount over its national total plus the correction line's amount over the part's national total).
 * The case's fixed conventions are the September 24 stateFor's (main_case_2026_09_24/package.cjs): receipts on the
 * reference incidence rule; public order and safety keyed by use and the Medicaid line by the specification's uninsured
 * key; public order and safety, health, income security and housing and community services at response 1; education
 * at the school fraction's response and the rest at 1; the three correction lines by class.
 *
 * evaluateAll(payload, {engine, model}) returns [{spec, state, evaluation, capital, cost_bn}] in the case's order:
 * allocation x normalization x school fraction x school response x reading x uninsured key. cost = -welfare + capital.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const FISCAL = path.resolve(__dirname, "..");
const loadEngine = () => require(path.join(FISCAL, "assumption_explorer_2026_09_21", "engine.js"));
const loadModel = () => JSON.parse(fs.readFileSync(path.join(FISCAL, "assumption_explorer_2026_09_21", "derived", "model.json"), "utf8"));
const UC_KEYS = ["uninsured_use_low", "uninsured_use_high"];
const SYN_CLASSES = ["education_school_part", "education_other_part", "correction_constant"];
const KEY_KINDS = ["constant", "receipt_amount_over_national", "lines_amount_over_national", "part_rekeyed"];
const RESPONSE_KINDS = ["fixed", "enterprises_switch", "line_response", "line_response_over_share", "long_run_subfunction"];

function specifications(Eng, model, payload) {
  const R = payload.meta.responses, out = [];
  for (const allocation of ["personal", "shared"]) for (const normalization of ["cash", "gdp"])
    for (const share of Eng.schoolShareBounds(model)) for (const school of [R.school.growth, R.school.decline])
      for (const [reading, gg] of [["low", R.general_government.low], ["high", R.general_government.high]])
        for (const uc of UC_KEYS) out.push({ allocation, normalization, share, school, reading, gg, uc });
  return out;
}

// The responses meta.responses sets at a reading: {"receipt:<id>" | <spending line id>: response}.
function lineResponses(m, payload, reading) {
  const out = {};
  const spending = new Set(m.spending.lines.map((l) => l.id)), receipts = new Set(m.receipts.lines.map((l) => l.id));
  for (const [id, e] of Object.entries(payload.meta.responses)) {
    if (!e || typeof e !== "object") continue;
    if (e.receipt === true) {
      if (!receipts.has(id) || e.override !== "receipt:" + id) throw new Error(`[BLOCKED] meta.responses.${id}: not a receipt line's override`);
      if (!Number.isFinite(e[reading])) throw new Error(`[BLOCKED] meta.responses.${id} has no ${reading} response`);
      out[e.override] = e[reading];
    } else if (spending.has(id)) {
      if (!Number.isFinite(e[reading])) throw new Error(`[BLOCKED] meta.responses.${id} has no ${reading} response`);
      out[id] = e[reading];
    }
  }
  return out;
}

function stateOf(Eng, m, payload, spec) {
  const syn = {};
  for (const c of SYN_CLASSES) {
    const ls = payload.lines.filter((l) => l.response_class === c);
    if (ls.length !== 1) throw new Error(`[BLOCKED] the payload has ${ls.length} correction lines of class ${c}, not one`);
    syn[c] = ls[0].id;
  }
  const s = Eng.defaultState(m);
  s.allocation = spec.allocation; s.receipt_scenario = m.receipts.reference; s.production.normalization = spec.normalization;
  s.count_production = true; s.general_government_response = spec.gg;
  s.key_override = { public_order_safety: "use", medicaid_and_chip_other_medical: spec.uc };
  s.response_override = { education_services: spec.share * spec.school + (1 - spec.share), public_order_safety: 1, health_services: 1,
    income_security_services: 1, housing_community_services: 1,
    [syn.education_school_part]: spec.share * spec.school, [syn.education_other_part]: 1 - spec.share, [syn.correction_constant]: 1 };
  Object.assign(s.response_override, lineResponses(m, payload, spec.reading));
  return s;
}

function capitalOf(ev, payload, spec) {
  const K = payload.meta.capital_return, R = payload.meta.responses;
  // Every case adopted since September 27 carries its capital return ($37–61bn on v6); such a payload without it is
  // incomplete, not a no-capital case (red team, 2026-10-08). Generation payloads and earlier cases carry no such stamp.
  if (payload.meta.adopted && payload.meta.adopted >= "2026-09-27" && !(K && K.components && K.components.length)) {
    throw new Error(`[BLOCKED] the payload adopted ${payload.meta.adopted} has no meta.capital_return components`);
  }
  if (!K) return { components: [], total_bn: 0 };
  const row = (id) => { const r = ev.spending.find((l) => l.id === id); if (!r) throw new Error(`[BLOCKED] no spending line ${id}`); return r; };
  const receipt = (id) => { const r = ev.receipts.find((l) => l.id === id); if (!r) throw new Error(`[BLOCKED] no receipt line ${id}`); return r; };
  const components = K.components.map((c) => {
    const k = c.key, r = c.response;
    if (!KEY_KINDS.includes(k.kind) || !RESPONSE_KINDS.includes(r.kind)) throw new Error(`[BLOCKED] ${c.id}: unknown rule kind ${k.kind} / ${r.kind}`);
    let key, response;
    if (k.kind === "constant") key = k.value;
    else if (k.kind === "receipt_amount_over_national") key = receipt(k.line).amount_bn / receipt(k.line).national_bn;
    else if (k.kind === "lines_amount_over_national") key = k.numerator_lines.reduce((a, id) => a + row(id).amount_bn, 0) / row(k.denominator_line).national_bn;
    else key = row(k.parent_line).amount_bn / row(k.parent_line).national_bn + row(k.correction_line).amount_bn / k.part_national_bn;
    if (r.kind === "fixed") response = r.value;
    else if (r.kind === "enterprises_switch") response = r.values[K.enterprises];
    else if (r.kind === "line_response") response = row(r.line).response;
    else if (r.kind === "line_response_over_share") response = row(r.line).response / (r.share === "school" ? spec.share : 1 - spec.share);
    else response = R[r.line].subfunctions.find((x) => x.id === r.subfunction)[spec.reading];
    return { id: c.id, key, response, return_bn: c.stock_charged_bn * K.rates[spec.reading] * key * response };
  });
  return { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
}

function evaluateAll(payload, opts) {
  const Eng = (opts && opts.engine) || loadEngine(), model = (opts && opts.model) || loadModel();
  const m = Eng.applyCorrections(model, payload);
  return specifications(Eng, model, payload).map((spec) => {
    const state = stateOf(Eng, m, payload, spec);
    const evaluation = Eng.evaluate(m, state);
    const capital = capitalOf(evaluation, payload, spec);
    return { spec, state, evaluation, capital, cost_bn: -evaluation.welfare_bn + capital.total_bn };
  });
}

module.exports = { FISCAL, UC_KEYS, SYN_CLASSES, KEY_KINDS, RESPONSE_KINDS, loadEngine, loadModel, specifications, lineResponses, stateOf,
  capitalOf, evaluateAll };
