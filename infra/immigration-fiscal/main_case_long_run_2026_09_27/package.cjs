/* The main case with long-run road and park responses, rental assistance, the return on public capital and the
 * government enterprises (BRIEF.md; decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md), as
 * importable definitions. The schools case (../main_case_schools_full_2026_09_26/package.cjs, imported unchanged,
 * $258.4885–291.9548bn) gains four things and nothing else changes:
 *
 *   1. Long-run responses for economic_affairs_services and recreation_culture
 *      (service_response_long_run_2026_09_27/derived/responses.json): each line at the amount-weighted blend of
 *      its subfunctions' finite-removal responses, the low readings at the band's low end and the high readings
 *      at its high end. The schools case held both at 0, CBO's category lag.
 *   2. Rental assistance (housing_subsidies, NIPA Table 3.13 line 4, key housing_support) at response 1, like the
 *      account's other capped means-tested transfers. It was held at 0 only because NIPA files it as a subsidy
 *      (dataset_integrity_2026_09_23/spending.md item 6). It is a household transfer in every profile.
 *   3. The return on public capital (capital_return_services_2026_09_27/derived/engine_components.json, 250ccb5):
 *      8 core and 5 road and park components, 2% at the low end and 3% at the high end.
 *   4. Government enterprises, option D (the operator's choice): the enterprise_surplus receipt responds at 1 and
 *      the return covers all government-enterprise capital (11 components keyed by that receipt). One payload
 *      edit re-keys the receipt from model.json's population share to the case's corrected one, the share the
 *      corrections give the population-keyed spending lines.
 *
 * A specification is the schools case's, in the same order and index, with more fields: `reading` ("low" where
 * general government takes its low response, else "high"), `rate` (the real return on public capital at that
 * reading; 0 turns the return off), `enterprises` (the option, "D" or "A") and `line_responses` (the two lines'
 * blended responses at that reading, housing_subsidies and "receipt:enterprise_surplus"). The engine state is the
 * September 24 package's stateFor(), which applies line_responses; the long-run lines follow them only under the
 * two long-run profiles, and the other entries apply in every profile.
 *
 * cost() = the engine's cost + the capital return, both from one evaluation (evaluateFull), so a re-keyed model
 * (for example one generation's) splits the return by its own key shares.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const P = require(path.join(__dirname, "..", "main_case_schools_full_2026_09_26", "package.cjs"));
const { P24, P26, Engine, MODEL, FISCAL, STACKS, METHODS, GG24, ALLOCS, readJson, span, mean2 } = P;

const HERE = __dirname;
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");

// ---------------------------------------------------------------------------------------------------
// Long-run responses (service_response_long_run_2026_09_27, committed bccf478).
const LR_FILE = "service_response_long_run_2026_09_27/derived/responses.json";
const LR = readJson(LR_FILE);
const LR_LINES = ["economic_affairs_services", "recreation_culture"];
const READINGS = ["low", "high"];
const RENTAL = "housing_subsidies";
const SUBFUNCTIONS = LR_LINES.flatMap((line) => LR.lines[line].subfunctions.map((sf) => Object.assign({ line }, sf)));
const SF = Object.fromEntries(SUBFUNCTIONS.map((sf) => [sf.id, sf]));
const E = LR.elasticities;
const finiteR = (b) => (1 - Math.pow(1 - LR.meta.s, b)) / LR.meta.s;
// The response lane's sensitivities (its engine.cjs, sensitivities_at_end_specifications), rule for rule, as
// subfunction responses at a reading.
const LONG_RUN_VARIANTS = {
  adopted: { label: "the response lane's readings: across states at the low end, within states at the high end, finite removal, capped at 1",
    at: (sf, reading) => sf.response[reading] },
  marginal_r_equals_b: { label: "measured responses taken as r = b instead of the finite removal (capped responses stay 1)",
    at: (sf, reading) => {
      const v = sf.response[reading];
      if (v === 1 || v === 0) return v;
      if (sf.id.includes("general_economic")) return E.administration_general_government.b;
      if (sf.id.includes("recreation")) return E.parks.across_states.b;
      return E.highways_nontoll.across_states.b;
    } },
  within_states_uncapped: { label: "within-state readings above 1 priced at the high end (highways 1.4225, parks 1.3759)",
    at: (sf, reading) => (reading !== "high" || sf.response.high !== 1 ? sf.response[reading]
      : finiteR(sf.id.includes("recreation") ? E.parks.within_states.b : E.highways_nontoll.within_states.b)) },
  federal_fixed_at_high_end: { label: "federal subfunctions held fixed at the high end too",
    at: (sf, reading) => (sf.level === "federal" ? 0 : sf.response[reading]) },
  across_states_at_high_end: { label: "S&L highways and parks at the across-state reading at the high end (no within-state reading)",
    at: (sf, reading) => {
      if (reading !== "high") return sf.response.low;
      if (["sl_highways", "sl_recreation_and_culture", "sl_transit_and_railroad"].includes(sf.id)) return sf.response.low;
      if (sf.level === "federal" && sf.response.high === 1) {
        return sf.id.includes("recreation") ? SF.sl_recreation_and_culture.response.low : SF.sl_highways.response.low;
      }
      return sf.response.high;
    } },
  held_at_zero_at_1: { label: "every subfunction held at 0 (water, space, agriculture, energy, natural resources, postal, commercial) at 1 instead",
    at: (sf, reading) => (sf.response.low === 0 && sf.response.high === 0 ? 1 : sf.response[reading]) },
};
// Subfunction responses {id: r} and the lines' blended responses at a reading. The adopted blend is the
// lane's own (responses.json lines.*.response); main_case.cjs gates that it is the blend of the subfunctions.
function subfunctionResponses(variant, reading) {
  const v = LONG_RUN_VARIANTS[variant];
  if (!v) throw new Error("unknown long-run variant " + variant);
  return Object.fromEntries(SUBFUNCTIONS.map((sf) => [sf.id, v.at(sf, reading)]));
}
function blendedResponses(variant, reading) {
  if (variant === "adopted") return Object.fromEntries(LR_LINES.map((id) => [id, LR.lines[id].response[reading]]));
  const r = subfunctionResponses(variant, reading);
  return Object.fromEntries(LR_LINES.map((id) => [id,
    SUBFUNCTIONS.filter((sf) => sf.line === id).reduce((a, sf) => a + sf.share_of_line * r[sf.id], 0)]));
}

// ---------------------------------------------------------------------------------------------------
// Profiles. The long-run profile replaces the category lag for roads and parks; the proportional reference
// keeps every service at 1. `delayed: null` marks the profiles whose two long-run lines take the
// specification's line_responses; `base` is the September 24 profile that sets everything else.
const PROFILES = {
  long_run_non_school_full: { other: 1, delayed: null, school: null, base: "cbo_category_lag_non_school_full" },
  long_run_non_school_fixed: { other: 0, delayed: null, school: null, base: "cbo_category_lag_non_school_fixed" },
  proportional_reference: { other: 1, delayed: 1, school: 1, base: "proportional_reference" },
};
const MAIN_PROFILE = "long_run_non_school_full";
// The schools case's profiles, which hold both lines at 0 (reported as variants, with the other additions on).
const OLD_PROFILES = {
  cbo_category_lag_non_school_full: Object.assign({}, P.PROFILES.cbo_category_lag_non_school_full, { base: "cbo_category_lag_non_school_full" }),
  cbo_category_lag_non_school_fixed: Object.assign({}, P.PROFILES.cbo_category_lag_non_school_fixed, { base: "cbo_category_lag_non_school_fixed" }),
};
const ALL_PROFILES = Object.assign({}, PROFILES, OLD_PROFILES);
function profileOf(profile) {
  const pr = ALL_PROFILES[profile || MAIN_PROFILE];
  if (!pr) throw new Error("unknown profile " + profile);
  return pr;
}
function stateFor(m, spec, profile) {
  const pr = profileOf(profile);
  const lineResponses = Object.assign({}, spec.line_responses || {});
  if (pr.delayed !== null) for (const id of LR_LINES) delete lineResponses[id];
  return P.stateFor(m, Object.assign({}, spec, { line_responses: lineResponses }), pr.base);
}

// ---------------------------------------------------------------------------------------------------
// The return on public capital (capital_return_services_2026_09_27/derived/engine_components.json, committed
// 250ccb5). For each component and specification, return = stock_charged_bn x rate x key x response; the key and
// the response are rules read on the evaluation of that specification, so a re-keyed evaluation (one generation's,
// say) splits every component by its own shares. The components are the lane's own: core, block (roads and
// parks) and enterprise parts. Its definition variants re-run the case with the lane's alternatives.
const CAP_FILE = "capital_return_services_2026_09_27/derived/engine_components.json";
const CAP = readJson(CAP_FILE);
const RATES = { low: 0.02, high: 0.03, reported: 0.07 };
const KEY_KINDS = ["constant", "lines_amount_over_national", "receipt_amount_over_national"];
const RESPONSE_KINDS = ["fixed", "line_response", "line_response_over_share", "long_run_subfunction", "enterprises_switch"];
const PARTS = ["core", "block", "enterprise"];
const unknownKinds = Object.keys(CAP.rule_kinds || {}).filter((k) => !KEY_KINDS.includes(k) && !RESPONSE_KINDS.includes(k));
if (!CAP.rule_kinds || unknownKinds.length) {
  throw new Error(`[BLOCKED] ${CAP_FILE}: rule kinds this package does not implement: ${unknownKinds.join(", ") || "(no rule_kinds)"}`);
}

// Government enterprises. Under "D" every enterprise responds: the enterprise_surplus receipt at 1 and the return on
// all enterprise capital; under "A" they stay out (the receipt at 0, no enterprise capital). The case's option is
// this constant, the operator's choice (2026-09-27 16:58 JST, through the parent's go-ahead), recorded in the
// payload's meta.capital_return.enterprises and gated against the options the components file allows. A file
// without the switch, or an unset option, stops the build: there is no default.
const ENTERPRISES = "D";
const ENTERPRISE_LINE = "enterprise_surplus";
const ENTERPRISE_RECEIPT = "receipt:" + ENTERPRISE_LINE;
const ENT = CAP.enterprises;
if (!ENT || !Array.isArray(ENT.allowed) || !ENT.allowed.length || !ENT.options) throw new Error(`[BLOCKED] ${CAP_FILE} has no enterprises switch`);
const ENTERPRISES_ALLOWED = ENT.allowed;
for (const o of ENTERPRISES_ALLOWED) {
  const x = ENT.options[o];
  if (!x || !x.receipt_responses || Object.keys(x.receipt_responses).join() !== ENTERPRISE_LINE
    || !Number.isFinite(x.receipt_responses[ENTERPRISE_LINE]) || !Number.isFinite(x.enterprise_component_response)) {
    throw new Error(`[BLOCKED] ${CAP_FILE}: unreadable enterprise option ${o}`);
  }
}
if (!ENTERPRISES) throw new Error("[BLOCKED] the enterprise option is not set in package.cjs");
if (!ENTERPRISES_ALLOWED.includes(ENTERPRISES)) {
  throw new Error(`[BLOCKED] enterprise option ${ENTERPRISES} is not one the components file allows (${ENTERPRISES_ALLOWED.join(", ")})`);
}
if (!MODEL.receipts.lines.some((l) => l.id === ENTERPRISE_LINE)) throw new Error("[BLOCKED] model.json has no receipt line " + ENTERPRISE_LINE);
const receiptResponseOf = (option) => ENT.options[option].receipt_responses[ENTERPRISE_LINE];

// The receipt's re-key. model.json keys enterprise_surplus by resident population (0.1202); the case's corrections
// move the population-keyed spending lines to the corrected share (0.1172, general_public_services' population
// cell) but leave every receipt. One receipt shift moves this receipt to that share, so the receipt, and every
// enterprise component keyed by it, agree with the spending lines. It is expanded to the eight incidence rules as
// every receipt shift is (main_case_2026_09_24 expand()); the case evaluates the reference rule.
const REKEY_LINE = "general_public_services";
function populationShare(m) {
  const l = m.spending.lines.find((x) => x.id === REKEY_LINE);
  return Object.fromEntries(ALLOCS.map((a) => [a, l.keys.population[a].target_bn / l.national_bn]));
}
function enterpriseRekeyShift(m) {
  const es = m.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
  const share = populationShare(m);
  return { side: "receipt", line: ENTERPRISE_LINE,
    by: Object.fromEntries(ALLOCS.map((a) => [a, es.national_bn * share[a] - es.cells[m.receipts.reference][a].target_bn])) };
}
const rekeyEdits = (m) => P.expand([enterpriseRekeyShift(m)]);

// The rules. An evaluation-keyed component takes its key from the lines (spending or receipt) of the evaluation
// passed in; the lane's own definition has no constant key. A variant may (K-12 at the pupil share).
const spendingIds = new Set(MODEL.spending.lines.map((l) => l.id).concat(P.SYN_LINES.map((l) => l.id)));
const receiptIds = new Set(MODEL.receipts.lines.map((l) => l.id));
function validate(c, where, evaluationKey) {
  const bad = (why) => { throw new Error(`[BLOCKED] ${CAP_FILE}: component ${c.id} (${where}): ${why}`); };
  if (c.lane_central_key || c.lane_central_response) bad("a lane_central_* rule; this package applies one rule set");
  if (!PARTS.includes(c.part)) bad("unknown part " + c.part);
  if (!["state_local", "federal"].includes(c.level)) bad("unknown level " + c.level);
  if (!Number.isFinite(c.stock_charged_bn) || c.stock_charged_bn < 0) bad("no charged stock");
  if (!Array.isArray(c.engine_lines)) bad("no engine_lines");
  const k = c.key || {}, r = c.response || {};
  if (!KEY_KINDS.includes(k.kind)) bad("unknown key kind " + k.kind);
  if (k.kind === "constant" && !Number.isFinite(k.value)) bad("a constant key without a value");
  if (k.kind === "lines_amount_over_national" && (!Array.isArray(k.numerator_lines) || !k.numerator_lines.length
    || !k.numerator_lines.concat([k.denominator_line]).every((id) => spendingIds.has(id)))) bad("key lines that are not spending lines");
  if (k.kind === "receipt_amount_over_national" && !receiptIds.has(k.line)) bad("key receipt that is not a receipt line: " + k.line);
  if (evaluationKey && k.kind === "constant") bad("a constant key in the lane's own definition");
  if (!RESPONSE_KINDS.includes(r.kind)) bad("unknown response kind " + r.kind);
  if (r.kind === "fixed" && !Number.isFinite(r.value)) bad("a fixed response without a value");
  if (["line_response", "line_response_over_share", "long_run_subfunction"].includes(r.kind) && !spendingIds.has(r.line)) bad("response line " + r.line);
  if (r.kind === "line_response_over_share" && !["school", "college"].includes(r.share)) bad("share " + r.share);
  if (r.kind === "long_run_subfunction" && !(SF[r.subfunction] && SF[r.subfunction].line === r.line)) bad("subfunction " + r.subfunction);
  if (r.kind === "enterprises_switch" && !ENTERPRISES_ALLOWED.every((o) => r.values && r.values[o] === ENT.options[o].enterprise_component_response)) {
    bad("enterprises_switch values that are not the options' enterprise_component_response");
  }
  // An enterprise component takes the switch, and only an enterprise component does.
  if ((c.part === "enterprise") !== (r.kind === "enterprises_switch")) bad("the enterprise part and the enterprises switch go together");
}
// The components of a definition variant (engine_components.json variants: {name: {label, overrides:
// [{component, stock_charged_bn | key | response | drop}], adds: [components]}}), or the lane's own definition.
const variantCache = new Map();
function componentsFor(variant) {
  if (!variant) return CAP.components;
  if (variantCache.has(variant)) return variantCache.get(variant);
  const v = CAP.variants && CAP.variants[variant];
  if (!v) throw new Error("[BLOCKED] engine_components.json has no capital variant " + variant);
  let comps = CAP.components.map((c) => Object.assign({}, c));
  for (const o of v.overrides || []) {
    const i = comps.findIndex((c) => c.id === o.component);
    if (i < 0) throw new Error(`[BLOCKED] variant ${variant} overrides an unknown component ${o.component}`);
    const fields = Object.keys(o).filter((f) => f !== "component");
    if (!fields.length || fields.some((f) => !["stock_charged_bn", "key", "response", "drop"].includes(f))) {
      throw new Error(`[BLOCKED] variant ${variant}: unknown override ${JSON.stringify(o)}`);
    }
    if (o.drop) { comps.splice(i, 1); continue; }
    for (const f of fields) comps[i][f] = o[f];
  }
  comps = comps.concat(v.adds || []);
  const ids = comps.map((c) => c.id);
  if (new Set(ids).size !== ids.length) throw new Error(`[BLOCKED] variant ${variant} repeats a component id`);
  for (const c of comps) validate(c, `variant ${variant}`, false);
  variantCache.set(variant, comps);
  return comps;
}
for (const c of CAP.components) validate(c, "the lane's definition", true);
for (const name of Object.keys(CAP.variants || {})) componentsFor(name);
function rowOf(evaluation, id) {
  const r = evaluation.spending.find((l) => l.id === id);
  if (!r) throw new Error(`[BLOCKED] the evaluation has no line ${id}: evaluate through evaluateFull(), which adds the correction lines`);
  return r;
}
function receiptRowOf(evaluation, id) {
  const r = evaluation.receipts.find((l) => l.id === id);
  if (!r) throw new Error(`[BLOCKED] the evaluation has no receipt line ${id}`);
  return r;
}
function keyOf(evaluation, rule) {
  if (rule.kind === "constant") return rule.value;
  if (rule.kind === "receipt_amount_over_national") {
    const r = receiptRowOf(evaluation, rule.line);
    return r.amount_bn / r.national_bn;
  }
  return rule.numerator_lines.reduce((a, id) => a + rowOf(evaluation, id).amount_bn, 0) / rowOf(evaluation, rule.denominator_line).national_bn;
}
// A long-run subfunction responds as its line does: at the specification's long-run reading when the line takes
// the specification's long-run response (the long-run profiles), at 0 when the line is held fixed (the category
// lag, or the long-run responses switched off) and at 1 when it responds in full (the proportional reference).
// An enterprise component takes the specification's enterprise option.
function responseOfRule(evaluation, spec, rule) {
  if (rule.kind === "fixed") return rule.value;
  if (rule.kind === "enterprises_switch") {
    if (!ENTERPRISES_ALLOWED.includes(spec.enterprises)) {
      throw new Error(`[BLOCKED] a specification without an allowed enterprises option (${spec.enterprises}): build specifications with specsFor()`);
    }
    return rule.values[spec.enterprises];
  }
  const r = rowOf(evaluation, rule.line).response;
  if (rule.kind === "line_response") return r;
  if (rule.kind === "line_response_over_share") return r / (rule.share === "school" ? spec.share : 1 - spec.share);
  if (spec.long_run && spec.line_responses && r === spec.line_responses[rule.line]) {
    return subfunctionResponses(spec.long_run, spec.reading)[rule.subfunction];
  }
  if (r === 0 || r === 1) return r;
  throw new Error(`[BLOCKED] ${rule.line} responds at ${r}, neither its long-run response, 0 nor 1`);
}
function capitalReturn(evaluation, spec) {
  if (spec.capital_rules !== undefined) throw new Error("capital_rules is gone: since 250ccb5 the capital lane's rules are this case's");
  if (!spec.rate) return { components: [], total_bn: 0 };
  const components = componentsFor(spec.capital_variant).map((c) => {
    const key = keyOf(evaluation, c.key);
    const response = responseOfRule(evaluation, spec, c.response);
    return { id: c.id, group: c.part, level: c.level, stock_charged_bn: c.stock_charged_bn, key, response,
      return_bn: c.stock_charged_bn * spec.rate * key * response };
  });
  return { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
}
// The capital return reads the school and college correction lines' rows (key shares and responses). A model
// without them (the uncorrected model, a generation's uncorrected model) is evaluated with them added at zero
// amounts, which leaves every amount and the cost unchanged.
const withSynthetic = new WeakMap();
function withSyntheticLines(m) {
  const missing = P.SYN_LINES.filter((l) => !m.spending.lines.some((x) => x.id === l.id));
  if (!missing.length) return m;
  if (!withSynthetic.has(m)) withSynthetic.set(m, Engine.applyCorrections(m, { lines: missing, edits: [] }));
  return withSynthetic.get(m);
}
function evaluateFull(m0, spec, profile) {
  const m = withSyntheticLines(m0);
  const evaluation = Engine.evaluate(m, stateFor(m, spec, profile));
  const capital = capitalReturn(evaluation, spec);
  return { evaluation, capital, cost_bn: -evaluation.welfare_bn + capital.total_bn };
}
const cost = (m, spec, profile) => evaluateFull(m, spec, profile).cost_bn;

// ---------------------------------------------------------------------------------------------------
// Options: every schools-case option, plus long_run (a LONG_RUN_VARIANTS key, or false for both lines at 0),
// rental (1 or 0), capital (true or false), rates ({low, high}: the return at each reading), capital_variant (a
// definition variant of engine_components.json, or null), enterprises ("D" or "A"), enterprise_receipt (the
// receipt's response; null follows the option) and enterprise_rekey (true: the receipt at the corrected
// population share).
const CENTRAL = Object.assign({}, P.CENTRAL, { long_run: "adopted", rental: 1, capital: true,
  rates: { low: RATES.low, high: RATES.high }, capital_variant: null, enterprises: ENTERPRISES, enterprise_receipt: null,
  enterprise_rekey: true });
function withCentral(o) {
  if (o && o.capital_rules !== undefined) throw new Error("capital_rules is gone: since 250ccb5 the capital lane's rules are this case's");
  const oo = P.withSchool(Object.assign({}, CENTRAL, o));
  if (!ENTERPRISES_ALLOWED.includes(oo.enterprises)) throw new Error(`[BLOCKED] enterprise option ${oo.enterprises} is not allowed`);
  return oo;
}
const receiptResponse = (oo) => (oo.enterprise_receipt === null || oo.enterprise_receipt === undefined
  ? receiptResponseOf(oo.enterprises) : oo.enterprise_receipt);
function specsFor(o) {
  const oo = withCentral(o);
  return P.specsFor(oo).map((s, i) => {
    const reading = P24.MAIN_SPECS[i].gg === GG24[0] ? "low" : "high";
    const lines = oo.long_run ? blendedResponses(oo.long_run, reading) : Object.fromEntries(LR_LINES.map((id) => [id, 0]));
    return Object.assign({}, s, { reading, rate: oo.capital ? oo.rates[reading] : 0, long_run: oo.long_run || null,
      enterprises: oo.enterprises,
      line_responses: Object.assign(lines, { [RENTAL]: oo.rental, [ENTERPRISE_RECEIPT]: receiptResponse(oo) }) },
      oo.capital_variant ? { capital_variant: oo.capital_variant } : {});
  });
}
const bandFor = (m, profile, specs) => span(specs.map((spec) => cost(m, spec, profile)));
// The corrected model of a fill-in method, as the schools case builds it, with the enterprise receipt re-keyed to
// that model's own corrected population share.
function modelFor(caseName, method, oo) {
  const m = P26.build(P26.packageShifts(STACKS[`row4+status_state_aware|${caseName}|${method}`], caseName, method, oo), oo);
  return oo.enterprise_rekey ? Engine.applyCorrections(m, { lines: [], edits: rekeyEdits(m) }) : m;
}
function evalPackage(caseName, method, o) {
  const oo = withCentral(o);
  return bandFor(modelFor(caseName, method, oo), oo.profile, specsFor(oo));
}
const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
const MAIN_SPECS = specsFor({});
const band = (m, profile) => bandFor(m, profile, MAIN_SPECS);

// ---------------------------------------------------------------------------------------------------
// Responses and the payload. meta.responses carries every response a consumer must set.
function responsesFor(o) {
  const oo = withCentral(o);
  const r = P.responsesFor(oo);
  const source = { file: LR_FILE, sha256: sha256(LR_FILE), commit: "bccf478" };
  for (const id of LR_LINES) {
    const v = oo.long_run || null;
    r[id] = {
      low: v ? blendedResponses(v, "low")[id] : 0, high: v ? blendedResponses(v, "high")[id] : 0,
      rule: `${LR.meta.rule}; the amount-weighted blend of the line's subfunctions (all share the line's key)`,
      readings: "low at the specifications where general government takes its low response (the band's low end), high elsewhere",
      profiles: "long_run_non_school_full and long_run_non_school_fixed; the proportional reference holds the line at 1",
      variant: v,
      subfunctions: LR.lines[id].subfunctions.map((sf) => ({ id: sf.id, level: sf.level, subfunction: sf.subfunction,
        national_bn: sf.national_bn, share_of_line: sf.share_of_line,
        low: v ? subfunctionResponses(v, "low")[sf.id] : 0, high: v ? subfunctionResponses(v, "high")[sf.id] : 0, basis: sf.basis })),
      source,
    };
  }
  r[RENTAL] = { low: oo.rental, high: oo.rental, key: MODEL.spending.lines.find((l) => l.id === RENTAL).preferred_key,
    rule: "household rental assistance at response 1, like the account's other capped means-tested transfers, in every profile; NIPA files it as a subsidy (Table 3.13 line 4, federal housing)",
    overlap_netted_bn: 0,
    overlap: "no double charge: NIPA's current surplus of government enterprises includes subsidies received from other levels of government (BEA glossary; MP-5), so under option D a federal payment to a public housing authority is charged here at the rental key and credited inside the enterprise_surplus receipt at the population key; the two offset except for the keys, a mismatch in the group's favour of at most $2.5bn if all of line 4 went to enterprises and about $0.2bn for public housing's operating subsidies [INFERENCE]; not netted",
    source: "dataset_integrity_2026_09_23/spending.md item 6" };
  const rr = receiptResponse(oo);
  r[ENTERPRISE_LINE] = { receipt: true, override: ENTERPRISE_RECEIPT, low: rr, high: rr, option: oo.enterprises,
    rule: `enterprise option ${oo.enterprises} (${ENT.options[oo.enterprises].label}): the enterprises' current surplus (NIPA 3.1 line 19, -$47.46bn national, net of depreciation and before interest) at this response in every profile; set as engine.js sets a receipt response, response_override["${ENTERPRISE_RECEIPT}"]`,
    key: oo.enterprise_rekey ? "the case's corrected population share (general_public_services' population cell), by the payload's re-key edits"
      : "model.json's resident_population share",
    source: `${CAP_FILE} enterprises` };
  return r;
}
const RESPONSES = responsesFor({});

// The capital return as data: every component with the rules this case applies, so a consumer computes the
// return from the payload, the engine and its own evaluation.
function capitalMeta(oo, rekey) {
  return {
    rule: "return = stock_charged_bn x rate x key x response for each component at each specification; key and response are rules on the engine's evaluation of that specification (rule_kinds). A long_run_subfunction response is the subfunction's in responses.<line>.subfunctions at the specification's reading when the line takes its long-run response, 0 when the line is held fixed and 1 when it responds in full; an enterprises_switch response is values[enterprises]",
    rates: { low: oo.rates.low, high: oo.rates.high, reported: RATES.reported },
    rate_rule: "the low rate at the specifications where general government takes its low response (the band's low end), the high rate elsewhere; 7% is reported beside the account, not in it",
    rule_kinds: CAP.rule_kinds,
    enterprises: oo.enterprises,
    enterprise_option: { allowed_by_file: ENTERPRISES_ALLOWED, label: ENT.options[oo.enterprises].label,
      receipt: ENTERPRISE_RECEIPT, receipt_response: receiptResponse(oo),
      enterprise_component_response: ENT.options[oo.enterprises].enterprise_component_response, receipt_rekey: rekey,
      chosen: "the operator, 2026-09-27 16:58 JST (the parent's go-ahead), gated against the file's allowed options",
      interest: "not added: NIPA's enterprise surplus excludes interest, which sits in the account's interest row, held at 0. BEA, Government Transactions (NIPA Methodology Paper 5, 2005), p. I-16: \"Interest received and paid are ignored in the calculation of the current surplus of government enterprises.\"" },
    departures_from_the_capital_lane: rekey ? [
      "the enterprise_surplus receipt, and with it every enterprise component's key, is re-keyed from model.json's resident-population share to the case's corrected population share by the payload's re-key edits (enterprise_option.receipt_rekey); the capital lane's row \"option D, enterprises at the spending lines' population key\" is this case before rental assistance",
    ] : [],
    variant: oo.capital_variant || null,
    components: componentsFor(oo.capital_variant).map((c) => ({ id: c.id, label: c.label, part: c.part, level: c.level,
      bea_source: c.bea_source, stock_charged_bn: c.stock_charged_bn, key: c.key, response: c.response })),
    source: { file: CAP_FILE, sha256: sha256(CAP_FILE), commit: "250ccb5", status: CAP.status || null },
  };
}

const CONGESTION_FILE = "service_response_long_run_2026_09_27/derived/net_change.json";
function correctionsPayload(o) {
  const oo = withCentral(o);
  const p = P.correctionsPayload(oo);
  if (p.edits.some((e) => e.side === "receipt" && e.line === ENTERPRISE_LINE)) throw new Error("[BLOCKED] the schools payload already edits " + ENTERPRISE_LINE);
  let edits = p.edits, rekey = null;
  if (oo.enterprise_rekey) {
    const pm = Engine.applyCorrections(MODEL, { lines: p.lines, edits: p.edits });
    const shift = enterpriseRekeyShift(pm);
    const added = P.expand([shift]);
    const es = MODEL.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
    edits = p.edits.concat(added);
    rekey = { line: ENTERPRISE_LINE, share_line: `${REKEY_LINE} (population cell)`, share: populationShare(pm),
      from_share: Object.fromEntries(ALLOCS.map((a) => [a, es.cells[MODEL.receipts.reference][a].target_bn / es.national_bn])),
      reference_edit_bn: shift.by, edits: added.length,
      rule: "one receipt shift to the corrected population share on the reference incidence rule, carried to the eight rules proportionally as every receipt shift is; the last edits of the payload" };
  }
  const cg = readJson(CONGESTION_FILE);
  return {
    meta: Object.assign({}, p.meta, {
      source: "main_case_long_run_2026_09_27/package.cjs", adopted: "2026-09-27",
      decision: "decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md",
      case: `${p.meta.case}; long-run road and park responses; rental assistance at response 1${oo.capital ? "; return on public capital at 2% / 3%" : ""}; government enterprises option ${oo.enterprises}`,
      previous: "main_case_schools_full_2026_09_26/derived/corrections.json (the same lines and edits without the enterprise receipt's re-key; roads, parks, rental assistance and the enterprise surplus at 0, no capital return)",
      responses: responsesFor(oo),
      capital_return: oo.capital ? capitalMeta(oo, rekey) : null,
      enterprise_receipt_rekey: rekey,
      beside_the_account: {
        congestion: { source: CONGESTION_FILE, sha256: sha256(CONGESTION_FILE), before_bn: cg.b1_lanes_fixed_bn,
          low_end_bn: cg.by_band_end.low.congestion_bn, high_end_bn: cg.by_band_end.high.congestion_bn,
          note: "the response lane's congestion item re-derived with the network following spending: it falls from $19.16bn as roads respond; beside the account, not in it" },
      },
    }),
    lines: p.lines, edits,
  };
}

module.exports = Object.assign({}, P, {
  HERE, PSCHOOLS: P, LR, LR_FILE, LR_LINES, READINGS, RENTAL, SUBFUNCTIONS, LONG_RUN_VARIANTS, RATES, CAP, CAP_FILE, PARTS,
  ENTERPRISES, ENTERPRISES_ALLOWED, ENTERPRISE_LINE, ENTERPRISE_RECEIPT, REKEY_LINE, PROFILES, OLD_PROFILES, ALL_PROFILES,
  MAIN_PROFILE, CENTRAL, MAIN_SPECS, RESPONSES,
  subfunctionResponses, blendedResponses, stateFor, componentsFor, keyOf, responseOfRule, capitalReturn, evaluateFull, cost,
  receiptResponseOf, populationShare, enterpriseRekeyShift, rekeyEdits,
  withCentral, specsFor, bandFor, modelFor, evalPackage, central, band, responsesFor, capitalMeta, correctionsPayload, sha256,
});
