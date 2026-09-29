/* The main case adopted on 2026-09-29 (candidate v4's set, adopted by the operator at 15:12 JST: "1 ok do";
 * decisions/2026-09-29-main-case-v4.md), as importable definitions with the September 27 package's API: the same export
 * names, the same function names and signatures (../main_case_long_run_2026_09_27/package.cjs). It is payload-first:
 *
 *   - The case is its payload, derived/corrections.json: candidate v4's builder (main_case_candidate_v4_2026_09_29/
 *     payload.cjs build(), at the set's options) stamped as adopted (meta.adopted, decision, status and the case text;
 *     nothing else changes). correctionsPayload() returns it, RESPONSES is its meta.responses and componentsFor(null) its
 *     meta.capital_return.components.
 *   - evaluateFull(m, spec, profile) evaluates any model: the package's own, the payload applied to model.json, the
 *     uncorrected model or a consumer's (a generation's, a cell's). withSyntheticLines(m) adds the payload's lines at
 *     zero where the model lacks them: the correction lines (the three September 24 lines and v4's five spending lines)
 *     and the receipt lines the payload splits out (housing_enterprise_surplus, tenant_occupied_property), each with its
 *     national total, every amount and every share at 0, so every line a specification's line_responses names is on the
 *     model.
 *     evaluateFull and stateFor apply it; a consumer that evaluates the engine itself evaluates
 *     Engine.evaluate(withSyntheticLines(m), stateFor(m, spec, profile)). The state takes the September 27 conventions
 *     and the specification's line responses, and the return on public capital comes from the payload's components on
 *     that evaluation, every key kind included (part_rekeyed: the parent line's key plus the correction line's amount
 *     over the part's national total).
 *   - Profiles: a correction line follows its parent line (meta.state_pricing.lines' parents and the part_rekeyed
 *     components' parent lines). Under a profile that fixes the long-run lines (the category lag at 0, the proportional
 *     reference at 1), a line whose parent is a long-run line takes that profile's response; the others keep their
 *     responses, as their parents do (public order and safety and health are at 1 in every profile). Receipt responses
 *     apply in every profile, as the enterprise receipt's always has.
 *   - Options: the September 27 options plus candidate v4's item options (ITEMS, read from the payload's
 *     meta.candidate_v4). modelFor builds a fill-in method's model with candidate v4's package; specsFor builds the
 *     specifications with it and keeps only the September 27 fields, so a specification carries no item field. At load
 *     the builder must rebuild this payload's lines, receipt lines, edits, production grid, responses and capital
 *     components from ITEMS, and MAIN_SPECS must carry meta.responses at each reading: the models, the specifications and
 *     the payload are one case. An item variant (other item options: an item off, one beside the case, the road arm)
 *     has capital rules the payload does not carry, so candidate v4's package evaluates it (evaluateFull below).
 *
 * forPayload(payload) returns the same API for another payload the builder rebuilds: the September 27 case's
 * corrections.json (every item off; generality.cjs runs the September 27 lane's own scripts on it) or the cash set's.
 * The module itself is forPayload of the adopted payload.
 */
"use strict";
const path = require("path");
const V4 = require(path.join(__dirname, "..", "main_case_candidate_v4_2026_09_29", "package.cjs"));
const B = require(path.join(__dirname, "..", "main_case_candidate_v4_2026_09_29", "payload.cjs"));
const P = V4.SEPT27;
const { Engine, MODEL, METHODS, span, mean2 } = P;

const HERE = __dirname;
const LANE = "main_case_2026_09_29";
const ADOPTED = "2026-09-29";
const DECISION = "decisions/2026-09-29-main-case-v4.md";
const clone = (x) => JSON.parse(JSON.stringify(x));

// ---------------------------------------------------------------------------------------------------
// The adopted payload: the builder's payload at the set's options, stamped. The stamps are the only change.
const CANDIDATE_TEXT = "; candidate v4, not adopted: ";
const STAMPED = ["source", "adopted", "decision", "case", "status"];
function adopt(payload) {
  const p = clone(payload);
  if (p.meta.case.split(CANDIDATE_TEXT).length !== 2) throw new Error("[BLOCKED] the builder's case text does not name the candidate once");
  p.meta.source = `${LANE}/package.cjs`;
  p.meta.adopted = ADOPTED;
  p.meta.decision = DECISION;
  p.meta.case = p.meta.case.replace(CANDIDATE_TEXT, "; v4, adopted 2026-09-29: ");
  p.meta.status = "adopted 2026-09-29 15:12 JST (the operator: \"1 ok do\"): candidate v4's set, built by main_case_candidate_v4_2026_09_29/payload.cjs build() at the set's options and returned by main_case_2026_09_29/package.cjs correctionsPayload()";
  return p;
}

// ---------------------------------------------------------------------------------------------------
// Definitions shared by every payload.
const SPEC_FIELDS = new Set(Object.keys(P.MAIN_SPECS[0]).concat(["capital_variant"]));
const stripSpec = (s) => Object.fromEntries(Object.keys(s).filter((k) => SPEC_FIELDS.has(k)).map((k) => [k, s[k]]));
const SYN_IDS = new Set(P.SYN_LINES.map((l) => l.id));
const KEY_KINDS = ["constant", "lines_amount_over_national", "receipt_amount_over_national", "part_rekeyed"];
const RESPONSE_KINDS = ["fixed", "line_response", "line_response_over_share", "long_run_subfunction", "enterprises_switch"];
const OVERRIDE_FIELDS = ["stock_charged_bn", "key", "response", "drop"];
const REBUILT = ["lines", "receipt_lines", "edits", "production"];
const ENTERPRISE_CLASS = MODEL.receipts.lines.find((l) => l.id === P.ENTERPRISE_LINE).cells[MODEL.receipts.reference].personal.response_class;
// The item options of a payload: candidate v4's items and composition rules from meta.candidate_v4, over every item off.
function optionsOf(payload) {
  const cv = payload.meta.candidate_v4;
  if (!cv) return Object.assign({}, V4.OFF);
  return Object.assign({}, V4.OFF, ...cv.items.map((it) => it.options), cv.rules);
}

function forPayload(payload0) {
  const payload = clone(payload0);
  const meta = payload.meta;
  if (!meta || !meta.responses || !meta.capital_return) {
    throw new Error("[BLOCKED] a payload without meta.responses and meta.capital_return: this package evaluates the September 27 case and its successors");
  }
  const ITEMS = optionsOf(payload);
  const rebuilt = B.build(ITEMS).payload;
  const differs = REBUILT.filter((k) => JSON.stringify(rebuilt[k]) !== JSON.stringify(payload[k]))
    .concat(["responses", "capital_return"].filter((k) => JSON.stringify(rebuilt.meta[k]) !== JSON.stringify(meta[k])));
  if (differs.length) {
    throw new Error(`[BLOCKED] candidate v4's builder at the payload's item options does not rebuild its ${differs.join(", ")}: the package's models would not be this payload's`);
  }
  const R = meta.responses, K = meta.capital_return;
  const LINES = payload.lines;
  const RECEIPT_LINES = (payload.receipt_lines || []).map((l) => l.id);
  const NEW_LINES = LINES.filter((l) => !SYN_IDS.has(l.id)).map((l) => l.id);
  const spendingIds = new Set(MODEL.spending.lines.map((l) => l.id).concat(LINES.map((l) => l.id)));
  const receiptIds = new Set(MODEL.receipts.lines.map((l) => l.id).concat(RECEIPT_LINES));
  if (!LINES.filter((l) => SYN_IDS.has(l.id)).every((l, i) => JSON.stringify(l) === JSON.stringify(P.SYN_LINES[i]))) {
    throw new Error("[BLOCKED] the payload's first correction lines are not the September 24 package's three");
  }

  // The correction lines' parents, from the payload: state pricing's lines and the part_rekeyed components.
  const PARENT = {};
  for (const x of (meta.state_pricing && meta.state_pricing.lines) || []) PARENT[x.line] = x.parent;
  for (const c of K.components) if (c.key.kind === "part_rekeyed") PARENT[c.key.correction_line] = c.key.parent_line;
  const orphans = NEW_LINES.filter((id) => !PARENT[id] || !MODEL.spending.lines.some((l) => l.id === PARENT[id]));
  if (orphans.length || Object.keys(PARENT).some((id) => !NEW_LINES.includes(id))) {
    throw new Error(`[BLOCKED] correction lines without one parent spending line in the payload: ${orphans.join(", ") || Object.keys(PARENT).join(", ")}`);
  }
  const FOLLOW_LR = NEW_LINES.filter((id) => P.LR_LINES.includes(PARENT[id]));
  // Receipt lines the payload splits out of the enterprise line (its response class): they respond as that receipt does.
  const receiptLineOf = (id) => (payload.receipt_lines || []).find((l) => l.id === id);
  const ENTERPRISE_SPLITS = RECEIPT_LINES.filter((id) => receiptLineOf(id).cells[MODEL.receipts.reference].personal.response_class === ENTERPRISE_CLASS);
  // The line responses meta.responses sets: {spec key: entry}.
  const LINE_RESPONSES = {};
  for (const [id, e] of Object.entries(R)) {
    if (!e || typeof e !== "object") continue;
    if (e.receipt === true) {
      if (e.override !== "receipt:" + id || !receiptIds.has(id)) throw new Error(`[BLOCKED] meta.responses.${id}: not a receipt line's override`);
      LINE_RESPONSES[e.override] = e;
    } else if (spendingIds.has(id)) LINE_RESPONSES[id] = e;
  }

  // ---------------------------------------------------------------------------------------------------
  // The capital return: the payload's components (a definition variant's overrides and additions applied to them).
  const unknownKinds = Object.keys(K.rule_kinds || {}).filter((k) => !KEY_KINDS.includes(k) && !RESPONSE_KINDS.includes(k));
  if (!K.rule_kinds || unknownKinds.length) throw new Error(`[BLOCKED] meta.capital_return: rule kinds this package does not implement: ${unknownKinds.join(", ") || "(no rule_kinds)"}`);
  const ENT = P.CAP.enterprises;
  function validate(c, where) {
    const bad = (why) => { throw new Error(`[BLOCKED] capital component ${c.id} (${where}): ${why}`); };
    if (!P.PARTS.includes(c.part)) bad("unknown part " + c.part);
    if (!["state_local", "federal"].includes(c.level)) bad("unknown level " + c.level);
    if (!Number.isFinite(c.stock_charged_bn) || c.stock_charged_bn < 0) bad("no charged stock");
    const k = c.key || {}, r = c.response || {};
    if (!KEY_KINDS.includes(k.kind)) bad("unknown key kind " + k.kind);
    if (k.kind === "constant" && !Number.isFinite(k.value)) bad("a constant key without a value");
    if (k.kind === "lines_amount_over_national" && (!Array.isArray(k.numerator_lines) || !k.numerator_lines.length
      || !k.numerator_lines.concat([k.denominator_line]).every((id) => spendingIds.has(id)))) bad("key lines that are not spending lines");
    if (k.kind === "receipt_amount_over_national" && !receiptIds.has(k.line)) bad("key receipt that is not a receipt line: " + k.line);
    if (k.kind === "part_rekeyed" && (!spendingIds.has(k.parent_line) || !spendingIds.has(k.correction_line) || !(k.part_national_bn > 0))) {
      bad("a part_rekeyed key without a parent line, a correction line and a positive part total");
    }
    if (!RESPONSE_KINDS.includes(r.kind)) bad("unknown response kind " + r.kind);
    if (r.kind === "fixed" && !Number.isFinite(r.value)) bad("a fixed response without a value");
    if (["line_response", "line_response_over_share", "long_run_subfunction"].includes(r.kind) && !spendingIds.has(r.line)) bad("response line " + r.line);
    if (r.kind === "line_response_over_share" && !["school", "college"].includes(r.share)) bad("share " + r.share);
    if (r.kind === "long_run_subfunction" && !P.SUBFUNCTIONS.some((sf) => sf.id === r.subfunction && sf.line === r.line)) bad("subfunction " + r.subfunction);
    if (r.kind === "enterprises_switch" && !P.ENTERPRISES_ALLOWED.every((o) => r.values && r.values[o] === ENT.options[o].enterprise_component_response)) {
      bad("enterprises_switch values that are not the options' enterprise_component_response");
    }
    if ((c.part === "enterprise") !== (r.kind === "enterprises_switch")) bad("the enterprise part and the enterprises switch go together");
  }
  for (const c of K.components) validate(c, "the payload's definition");
  if (!P.ENTERPRISES_ALLOWED.includes(K.enterprises)) throw new Error(`[BLOCKED] meta.capital_return.enterprises ${K.enterprises} is not an allowed option`);
  const variantCache = new Map();
  function componentsFor(variant) {
    if (!variant) return K.components;
    if (variantCache.has(variant)) return variantCache.get(variant);
    const v = P.CAP.variants && P.CAP.variants[variant];
    if (!v) throw new Error("[BLOCKED] engine_components.json has no capital variant " + variant);
    let comps = K.components.map((c) => Object.assign({}, c));
    for (const o of v.overrides || []) {
      const i = comps.findIndex((c) => c.id === o.component);
      if (i < 0) throw new Error(`[BLOCKED] variant ${variant} overrides an unknown component ${o.component}`);
      const fields = Object.keys(o).filter((f) => f !== "component");
      if (!fields.length || fields.some((f) => !OVERRIDE_FIELDS.includes(f))) throw new Error(`[BLOCKED] variant ${variant}: unknown override ${JSON.stringify(o)}`);
      if (o.drop) { comps.splice(i, 1); continue; }
      for (const f of fields) comps[i][f] = o[f];
    }
    comps = comps.concat(v.adds || []);
    const ids = comps.map((c) => c.id);
    if (new Set(ids).size !== ids.length) throw new Error(`[BLOCKED] variant ${variant} repeats a component id`);
    for (const c of comps) validate(c, `variant ${variant}`);
    variantCache.set(variant, comps);
    return comps;
  }
  for (const name of Object.keys(P.CAP.variants || {})) componentsFor(name);
  const rowOf = (evaluation, id) => {
    const r = evaluation.spending.find((l) => l.id === id);
    if (!r) throw new Error(`[BLOCKED] the evaluation has no line ${id}: evaluate through evaluateFull(), which adds the correction lines`);
    return r;
  };
  function keyOf(evaluation, rule) {
    if (rule.kind !== "part_rekeyed") return P.keyOf(evaluation, rule);
    const parent = rowOf(evaluation, rule.parent_line), part = rowOf(evaluation, rule.correction_line);
    return parent.amount_bn / parent.national_bn + part.amount_bn / rule.part_national_bn;
  }
  function capitalReturn(evaluation, spec) {
    if (spec.capital_rules !== undefined) throw new Error("capital_rules is gone: since 250ccb5 the capital lane's rules are this case's");
    if (!spec.rate) return { components: [], total_bn: 0 };
    const components = componentsFor(spec.capital_variant).map((c) => {
      const key = keyOf(evaluation, c.key);
      const response = P.responseOfRule(evaluation, spec, c.response);
      return { id: c.id, group: c.part, level: c.level, stock_charged_bn: c.stock_charged_bn, key, response,
        return_bn: c.stock_charged_bn * spec.rate * key * response };
    });
    return { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
  }

  // ---------------------------------------------------------------------------------------------------
  // The engine state and the evaluation, on any model. The payload's receipt lines at zero: national 0 and every
  // cell's target, other and share 0, the incidence rule's key and response class kept.
  const ZERO_RECEIPT_LINES = (payload.receipt_lines || []).map((l) => Object.assign(clone(l), { national_bn: 0,
    cells: Object.fromEntries(Object.entries(l.cells).map(([sc, cell]) => [sc, Object.fromEntries(Object.entries(cell)
      .map(([a, c]) => [a, Object.assign({}, c, { target_bn: 0, other_bn: 0, share: 0 })]))])) }));
  const withLines = new WeakMap();
  function withSyntheticLines(m) {
    const lines = LINES.filter((l) => !m.spending.lines.some((x) => x.id === l.id));
    const receiptLines = ZERO_RECEIPT_LINES.filter((l) => !m.receipts.lines.some((x) => x.id === l.id));
    if (!lines.length && !receiptLines.length) return m;
    if (!withLines.has(m)) withLines.set(m, Engine.applyCorrections(m, { lines, receipt_lines: receiptLines, edits: [] }));
    return withLines.get(m);
  }
  function profileOf(profile) {
    const pr = P.ALL_PROFILES[profile || P.MAIN_PROFILE];
    if (!pr) throw new Error("unknown profile " + profile);
    return pr;
  }
  function stateFor(m0, spec, profile) {
    const pr = profileOf(profile);
    const m = withSyntheticLines(m0);
    const lr = Object.assign({}, spec.line_responses || {});
    if (pr.delayed !== null) for (const id of FOLLOW_LR) if (id in lr) lr[id] = pr.delayed;
    return P.stateFor(m, Object.assign({}, spec, { line_responses: lr }), profile);
  }
  // An item variant (options whose item fields differ from the payload's: another item set, candidate v4's road arm or
  // public pay) has capital rules and terms the payload does not describe, so candidate v4's package evaluates it, on
  // the model modelFor() built for it and the specification specsFor() built for it (FULL keeps the candidate's
  // specification of each specification specsFor() returns). A model built for other items, met without that
  // specification (a copy of it, or a consumer's own), stops the evaluation.
  const FULL = new WeakMap();
  const ITEM_KEYS = Object.keys(ITEMS);
  const sameItems = (x) => ITEM_KEYS.every((k) => !(k in x) || x[k] === ITEMS[k]);
  const itemsOfModel = (m) => (m.candidate ? Object.assign({}, m.candidate, m.candidate.v3 || {}, m.candidate.v4 || {}) : null);
  function evaluateFull(m0, spec, profile) {
    const full = FULL.get(spec), tag = itemsOfModel(m0);
    if ((full && !sameItems(full)) || (tag && !sameItems(tag))) {
      if (!full) throw new Error("[BLOCKED] a model built for other item options than the case's, with a specification specsFor() did not build for them");
      const r = V4.evaluateFull(m0, full, profile);
      return { evaluation: r.evaluation, capital: r.capital, cost_bn: r.cost_bn };
    }
    const m = withSyntheticLines(m0);
    const evaluation = Engine.evaluate(m, stateFor(m, spec, profile));
    const capital = capitalReturn(evaluation, spec);
    return { evaluation, capital, cost_bn: -evaluation.welfare_bn + capital.total_bn };
  }
  const cost = (m, spec, profile) => evaluateFull(m, spec, profile).cost_bn;

  // ---------------------------------------------------------------------------------------------------
  // Options, specifications and models.
  const CENTRAL = Object.assign({}, P.CENTRAL, ITEMS);
  function withCentral(o) {
    if (o && o.capital_rules !== undefined) throw new Error("capital_rules is gone: since 250ccb5 the capital lane's rules are this case's");
    return V4.withCentral(Object.assign({}, ITEMS, o || {}));
  }
  const specsFor = (o) => V4.specsFor(withCentral(o)).map((s) => { const x = stripSpec(s); FULL.set(x, s); return x; });
  function modelFor(caseName, method, oo) {
    const missing = Object.keys(ITEMS).filter((k) => !(k in oo));
    if (missing.length) throw new Error(`[BLOCKED] options without ${missing.join(", ")}: build them with withCentral()`);
    return V4.modelFor(caseName, method, oo);
  }
  const bandFor = (m, profile, specs) => span(specs.map((spec) => cost(m, spec, profile)));
  function evalPackage(caseName, method, o) {
    const oo = withCentral(o);
    return bandFor(modelFor(caseName, method, oo), oo.profile, specsFor(oo));
  }
  const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
  const MAIN_SPECS = specsFor({});
  const band = (m, profile) => bandFor(m, profile, MAIN_SPECS);
  const payloadModel = () => Engine.applyCorrections(MODEL, payload);

  // Payload-first: the specifications carry meta.responses at their reading, every entry and nothing else, and the rate
  // of meta.capital_return.
  for (const s of MAIN_SPECS) {
    const keys = Object.keys(s.line_responses);
    const want = Object.keys(LINE_RESPONSES);
    if (keys.length !== want.length || keys.some((k, i) => k !== want[i] || s.line_responses[k] !== LINE_RESPONSES[k][s.reading])) {
      throw new Error(`[BLOCKED] a specification's line responses are not meta.responses at its ${s.reading} reading`);
    }
    if (s.rate !== K.rates[s.reading] || s.enterprises !== K.enterprises) throw new Error("[BLOCKED] a specification's rate or enterprise option is not meta.capital_return's");
  }

  // ---------------------------------------------------------------------------------------------------
  // Responses and the payload.
  const RESPONSES = clone(R);
  function responsesFor(o) {
    const oo = withCentral(o);
    const r = P.responsesFor(oo);
    const specs = specsFor(oo);
    const at = (rd) => specs.find((s) => s.reading === rd).line_responses;
    for (const [id, e] of Object.entries(R)) {
      if (id in r) continue;
      if (!e || typeof e !== "object" || !((e.receipt === true ? e.override : id) in LINE_RESPONSES)) { r[id] = clone(e); continue; }
      const k = e.receipt === true ? e.override : id;
      r[id] = Object.assign(clone(e), { low: at("low")[k], high: at("high")[k] });
    }
    return r;
  }
  if (JSON.stringify(responsesFor({})) !== JSON.stringify(R)) throw new Error("[BLOCKED] responsesFor({}) is not meta.responses");
  // The capital return as data at an option set: the payload's, with that set's rates, option and definition variant.
  function capitalMeta(oo) {
    return Object.assign(clone(K), { rates: { low: oo.rates.low, high: oo.rates.high, reported: P.RATES.reported }, enterprises: oo.enterprises,
      variant: oo.capital_variant || null,
      components: componentsFor(oo.capital_variant).map((c) => ({ id: c.id, label: c.label, part: c.part, level: c.level,
        bea_source: c.bea_source, stock_charged_bn: c.stock_charged_bn, key: c.key, response: c.response })) });
  }
  // The payload itself, or, with item options, the builder's payload of that variant of the case (not adopted; options
  // that move a specification field have no payload and the builder stops).
  function correctionsPayload(o) {
    if (!o || !Object.keys(o).length) return clone(payload);
    return clone(B.build(Object.assign({}, ITEMS, o)).payload);
  }

  return Object.assign({}, P, {
    HERE, LANE, SEPT27: P, V4PKG: V4, BUILDER: B, ITEMS, CENTRAL, PARENT, FOLLOW_LR, ENTERPRISE_SPLITS, PAYLOAD_LINES: clone(LINES),
    PAYLOAD_RECEIPT_LINES: RECEIPT_LINES.slice(), ZERO_RECEIPT_LINES: clone(ZERO_RECEIPT_LINES), LINE_RESPONSES: clone(LINE_RESPONSES),
    KEY_KINDS, RESPONSE_KINDS,
    MAIN_SPECS, RESPONSES,
    stateFor, componentsFor, keyOf, capitalReturn, evaluateFull, cost, withSyntheticLines, payloadModel,
    withCentral, specsFor, bandFor, modelFor, evalPackage, central, band, responsesFor, capitalMeta, correctionsPayload,
    forPayload, adopt,
  });
}

const PAYLOAD = adopt(B.build(V4.SET).payload);
module.exports = Object.assign(forPayload(PAYLOAD), { ADOPTED, DECISION, STAMPED, CANDIDATE_TEXT, optionsOf, stripSpec });
