/* The main case adopted on 2026-10-05 (v5; decisions/2026-10-05-main-case-v5.md): the v4 case (main_case_2026_09_29)
 * plus the descendants of Mexican immigrants whom the account misses because they no longer report Mexican origin
 * (main_case_lineage_2026_10_05, arm b: 3.04M added people on the account's frame, a lineage of 42.75M, counted whole).
 * It has the September 29 package's API: the same export names, functions and signatures
 * (../main_case_2026_09_29/package.cjs), so a consumer moves from sept29 to oct05 by changing the lane it reads.
 *
 *   - The case is its payload, derived/corrections.json: the v4 payload with the lineage lane's payload addition merged
 *     in (merge()) and stamped as adopted (adoptLineage()). The merge appends the addition's cell edits (the added
 *     people's amounts in every engine cell, then one edit for audit row 8's change at the larger group) to v4's edits,
 *     takes its production grid (the union's plus the added G3+ members') and its meta.responses (the group-size
 *     responses at the larger group's share), writes the long-run capital components' values at those responses, and
 *     records the lineage population in meta.lineage. Nothing else in v4's payload changes. The cash set's payload, built
 *     the same way on the v4 cash set, is CASH_PAYLOAD (derived/corrections_cash.json); CASH is its package.
 *   - forCase(base, payload) returns the API for a merged payload on a September 29-style package (forPayload()'s
 *     API). Given the base's own payload (the lineage off) it is the base's case: generality.cjs runs the September 29
 *     lane's own scripts on it and gets that lane's files byte for byte.
 *   - Models. modelFor() builds a fill-in method's model with the base's package and adds the lineage's edits and its
 *     production; a model whose production is the v4 payload's takes the merged grid, any other adds the difference.
 *     The lineage's amounts are the case's at every option [ASSUMPTION for variants: an option that changes the union's
 *     data does not change the added people's amounts]; an option that changes a line's national total scales the
 *     added people's amount on it, and a part split off a line takes that line's key (followNationals()). Without
 *     finite removal for general government (finite false or "school") row 8's factor is 1 whatever the group's size,
 *     so the row-8 edit is left out. A different pension switch is the other set: its lineage is the cash payload's,
 *     through CASH.
 *   - Responses. Only the group-size responses move (meta.lineage.responses_changed); every other entry is v4's
 *     (gated). A specification's reading moves by this rule (moveSpec):
 *       general government: the case's reading becomes v5's; 0 and 1 stay; without finite removal for it (the
 *         September 24 elasticities, r = b) it stays; any other reading (the engine population key) moves by the
 *         case's change [first order];
 *       the long-run lines, the road lines and recreation's state price: re-derived at v5's subfunction responses for
 *         whichever long-run variant the specification names (longRunAt(), the September 27 package's variants
 *         re-implemented on the subfunction table and s, gated equal to that package at v4's); 0 and 1 stay;
 *       the long-run property receipts: the case's reading becomes v5's; 1 stays; any other (the receipt-side lane's
 *         low reading) moves by the case's change [first order].
 *     The return on public capital takes the long-run subfunction responses at v5 the same way (moveCapital()).
 *   - evaluateFull(m, spec, profile) evaluates any model as the September 29 package does: the payload's lines at zero
 *     where the model lacks them (withSyntheticLines), the September 27 state conventions, the payload's capital
 *     components. An item variant (other item options) goes to candidate v4's package at its moved specification
 *     (viaCandidate()), with the road capital keyed on the evaluation (candidate v4 keys it at a road key computed
 *     before the lineage's edits) and the long-run capital responses moved after.
 *
 * Run nothing: this is a module. main_case.cjs gates it.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const V4P = require(path.join(__dirname, "..", "main_case_2026_09_29", "package.cjs"));
const P27 = V4P.SEPT27;
const V4 = V4P.V4PKG;
const { Engine, MODEL, FISCAL, METHODS, span, mean2 } = V4P;

const HERE = __dirname;
const LANE = "main_case_2026_10_05";
const ADOPTED = "2026-10-05";
const DECISION = "decisions/2026-10-05-main-case-v5.md";
const LINEAGE_LANE = "main_case_lineage_2026_10_05";
const LINEAGE_FILES = { set: `${LINEAGE_LANE}/derived/lineage_payload.json`, cash: `${LINEAGE_LANE}/derived/lineage_payload_cash.json` };
const POPULATION_FILE = `${LINEAGE_LANE}/derived/population.json`;
const BASE_FILES = { set: "main_case_2026_09_29/derived/corrections.json", cash: "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json" };
const STAMPED = ["source", "adopted", "decision", "case", "status", "lineage"];
const READINGS = ["low", "high"];
const LR_LINES = P27.LR_LINES;
const ROADS = { roads_vmt_sl: "sl_highways", roads_vmt_fed: "fed_highways" };
const REC_PRICE = "state_price_recreation_culture";
const PROPERTY = ["modeled_owner_property", "tenant_occupied_property"];
const clone = (x) => JSON.parse(JSON.stringify(x));
const readRel = (rel) => fs.readFileSync(path.join(FISCAL, rel), "utf8");
const readJson = (rel) => JSON.parse(readRel(rel));
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const blocked = (why) => { throw new Error("[BLOCKED] " + why); };
const isNum = (x) => typeof x === "number" && Number.isFinite(x);
// Production grids agree dimension by dimension (engine.js applyCorrections' test; model.json lists the dimensions in
// another order than the payloads).
const sameDims = (a, b) => {
  const ka = Object.keys(a).sort(), kb = Object.keys(b).sort();
  return JSON.stringify(ka) === JSON.stringify(kb) && ka.every((k) => JSON.stringify(a[k]) === JSON.stringify(b[k]));
};

// ---------------------------------------------------------------------------------------------------
// The September 27 package's long-run variants, on any subfunction table {id: {low, high}} and group share s. At v4's
// table and s they are that package's subfunctionResponses() exactly (gated at load below).
const E = P27.LR.elasticities;
const SUBS = P27.SUBFUNCTIONS;
function longRunAt(table, s) {
  const finiteR = (b) => (1 - Math.pow(1 - s, b)) / s;
  const r = (sf) => table[sf.id];
  const at = {
    adopted: (sf, reading) => r(sf)[reading],
    marginal_r_equals_b: (sf, reading) => {
      const v = r(sf)[reading];
      if (v === 1 || v === 0) return v;
      if (sf.id.includes("general_economic")) return E.administration_general_government.b;
      if (sf.id.includes("recreation")) return E.parks.across_states.b;
      return E.highways_nontoll.across_states.b;
    },
    within_states_uncapped: (sf, reading) => (reading !== "high" || r(sf).high !== 1 ? r(sf)[reading]
      : finiteR(sf.id.includes("recreation") ? E.parks.within_states.b : E.highways_nontoll.within_states.b)),
    federal_fixed_at_high_end: (sf, reading) => (sf.level === "federal" ? 0 : r(sf)[reading]),
    across_states_at_high_end: (sf, reading) => {
      if (reading !== "high") return r(sf).low;
      if (["sl_highways", "sl_recreation_and_culture", "sl_transit_and_railroad"].includes(sf.id)) return r(sf).low;
      if (sf.level === "federal" && r(sf).high === 1) return sf.id.includes("recreation") ? table.sl_recreation_and_culture.low : table.sl_highways.low;
      return r(sf).high;
    },
    held_at_zero_at_1: (sf, reading) => (r(sf).low === 0 && r(sf).high === 0 ? 1 : r(sf)[reading]),
  };
  if (JSON.stringify(Object.keys(at)) !== JSON.stringify(Object.keys(P27.LONG_RUN_VARIANTS))) blocked("the long-run variants are not the September 27 package's");
  function subfunctionResponses(variant, reading) {
    if (!at[variant]) blocked("unknown long-run variant " + variant);
    return Object.fromEntries(SUBS.map((sf) => [sf.id, at[variant](sf, reading)]));
  }
  return { subfunctionResponses };
}
const tableOf = (R) => Object.fromEntries(LR_LINES.flatMap((line) => R[line].subfunctions.map((x) => [x.id, { low: x.low, high: x.high }])));
// The case's change for one reading: the case's v4 value becomes v5's; 0 and 1 stay; any other value moves by the
// case's change (first order).
function moveLeaf(v4, v5, value) {
  if (!isNum(v4) || !isNum(v5) || !isNum(value)) blocked(`a group-size response that is not a number (${v4}, ${v5}, ${value})`);
  if (value === v4) return v5;
  if (value === 0 || value === 1) return value;
  return value + (v5 - v4);
}

// ---------------------------------------------------------------------------------------------------
// The payloads. merge() adds the lineage lane's payload addition to the payload it builds on; adoptLineage() stamps it.
const POP = readJson(POPULATION_FILE);
const GROUP_PATHS = new Set(["general_government.low", "general_government.high", "general_government.s", "row8_factor",
  ...LR_LINES.flatMap((l) => [`${l}.low`, `${l}.high`]), ...Object.keys(ROADS).flatMap((l) => [`${l}.low`, `${l}.high`]),
  `${REC_PRICE}.low`, `${REC_PRICE}.high`, ...PROPERTY.flatMap((l) => [`${l}.low`, `${l}.high`])]);
const SUB_FIELDS = new Set(["low", "high"]);
// The leaves of two responses objects that differ, as paths; subfunction entries are matched by id.
function responseDiffs(a, b) {
  const out = [];
  const walk = (x, y, p) => {
    if (Array.isArray(x) || Array.isArray(y)) {
      if (!Array.isArray(x) || !Array.isArray(y) || x.length !== y.length) { out.push(p); return; }
      x.forEach((e, i) => walk(e, y[i], `${p}[${e && e.id ? e.id : i}]`));
      return;
    }
    if (x && y && typeof x === "object" && typeof y === "object") {
      const kx = Object.keys(x), ky = Object.keys(y);
      if (JSON.stringify(kx) !== JSON.stringify(ky)) { out.push(p + " (keys)"); return; }
      for (const k of kx) walk(x[k], y[k], p ? `${p}.${k}` : k);
      return;
    }
    if (x !== y) out.push(p);
  };
  walk(a, b, "");
  return out;
}
const allowedDiff = (p) => GROUP_PATHS.has(p) || LR_LINES.some((l) => {
  const m = p.match(/^([a-z_]+)\.subfunctions\[([a-z_]+)\]\.([a-z_]+)$/);
  return m && m[1] === l && SUB_FIELDS.has(m[3]);
});
const longRunComponents = (K) => K.components.filter((c) => c.response.kind === "long_run_subfunction");
function merge(basePayload, addition, which) {
  if (!BASE_FILES[which]) blocked("no base payload " + which);
  if (addition.meta.builds_on !== BASE_FILES[which]) blocked(`the lineage payload builds on ${addition.meta.builds_on}, not ${BASE_FILES[which]}`);
  if (JSON.stringify(basePayload) !== JSON.stringify(readJson(BASE_FILES[which]))) blocked(`the base payload is not ${BASE_FILES[which]}`);
  const p = clone(basePayload), meta = addition.meta;
  const prod = addition.production;
  if (!sameDims(prod.dims, p.production.dims) || JSON.stringify(prod.sampling_se_bn) !== JSON.stringify(p.production.sampling_se_bn)
    || ["private_wtp_bn", "induced_receipts_bn"].some((k) => prod[k].length !== p.production[k].length)) {
    blocked("the lineage production grid is not the base's grid with new P and F");
  }
  const bad = responseDiffs(p.meta.responses, meta.responses).filter((x) => !allowedDiff(x));
  if (bad.length) blocked(`the lineage payload changes responses that do not depend on the group's size: ${bad.join(", ")}`);
  // The capital rules are v4's; only the long-run components' values (their readings) move, and they must be the
  // subfunction responses meta.responses carries.
  const K4 = p.meta.capital_return, KL = clone(meta.capital_return);
  const table5 = tableOf(meta.responses);
  for (const c of longRunComponents(KL)) {
    const v = c.response.values, t = table5[c.response.subfunction];
    if (!v || !t || v.low !== t.low || v.high !== t.high) blocked(`capital component ${c.id}: its values are not meta.responses' ${c.response.subfunction}`);
  }
  const strip = (K) => clone(K).components.map((c) => { if (c.response.kind === "long_run_subfunction") delete c.response.values; return c; });
  if (JSON.stringify(strip(K4)) !== JSON.stringify(strip(KL)) || JSON.stringify(Object.assign({}, K4, { components: null })) !== JSON.stringify(Object.assign({}, KL, { components: null }))) {
    blocked("the lineage payload's capital rules are not the base's");
  }
  for (const c of longRunComponents(K4)) {
    const v = KL.components.find((x) => x.id === c.id).response.values;
    c.response.values = Object.fromEntries(Object.keys(c.response.values).map((k) => [k, v[k]]));
  }
  p.meta.responses = clone(meta.responses);
  const n4 = p.edits.length;
  p.edits = p.edits.concat(clone(addition.edits));
  p.production.private_wtp_bn = prod.private_wtp_bn.slice();
  p.production.induced_receipts_bn = prod.induced_receipts_bn.slice();
  const L = meta.lineage, last = addition.edits[addition.edits.length - 1];
  if (!(last.side === "spending" && last.line === "lane_constants" && last.key === "k" && last.by.personal === L.row8_edit_bn && last.by.shared === L.row8_edit_bn)) {
    blocked("the lineage payload's last edit is not audit row 8's change");
  }
  p.meta.lineage = {
    lane: LINEAGE_LANE, payload: LINEAGE_FILES[which], builds_on: meta.builds_on, arm: L.arm, source_arm: L.source_arm, rho: L.rho,
    generation: "G3plus",
    counts: { added: L.added, at_g3_rate: L.g3_rate, later_losses: L.later, lineage_population: L.population, account_union: POP.meta.account_union,
      identified_g3plus: POP.meta.g3_account },
    c3: { value: L.c3.value, se: L.c3.se, label: L.c3.label, measure: L.c3.measure, source: L.c3.source, override: L.c3.override },
    members: { g3plus: L.m_g3plus, white: L.m_white,
      rule: "later losses priced as identified G3+ members; G3-rate attriters at (1 - C3) G3+ member + C3 third-plus non-Hispanic white at the G3+'s ages: m_G = later + (1 - C3) x at_g3_rate G3+ members, m_W = C3 x at_g3_rate whites" },
    frame_factor: L.frame_factor, s: { v4: basePayload.meta.responses.general_government.s, v5: L.s },
    k_metro: L.k_metro,
    edits: { first: n4, count: addition.edits.length, row8_edit_index: n4 + addition.edits.length - 1, row8_edit_bn: L.row8_edit_bn },
    production: "the union's grid plus the added G3+ members' P and F (whites carry none)",
    responses_changed: L.responses_changed, g3plus_model: L.g3plus_model, white: L.white,
  };
  return p;
}
function adoptLineage(p0, which) {
  const p = clone(p0);
  if (p.meta.lineage.counts.added <= 0) blocked("a lineage payload with nobody added");
  const lin = p.meta.lineage, M = (x) => (x / 1e6).toFixed(4);
  p.meta.source = `${LANE}/package.cjs`;
  p.meta.adopted = ADOPTED;
  p.meta.decision = DECISION;
  p.meta.case = `${p.meta.case}; v5, adopted ${ADOPTED}: plus ${M(lin.counts.added)}M descendants who no longer report Mexican origin (arm ${lin.arm}, `
    + `lineage ${M(lin.counts.lineage_population)}M, counted whole): ${M(lin.counts.later_losses)}M later losses as identified G3+ members and `
    + `${M(lin.counts.at_g3_rate)}M G3-rate attriters at (1 - C3) G3+ + C3 third-plus whites, C3 ${lin.c3.value}`;
  p.meta.status = which === "set"
    ? `adopted ${ADOPTED} (decisions/2026-10-05-main-case-v5.md): the v4 case plus the lineage line, merged by ${LANE}/package.cjs from ${BASE_FILES.set} and ${LINEAGE_FILES.set}`
    : `the cash set of the case adopted ${ADOPTED} (the pension switch off): ${BASE_FILES.cash} plus ${LINEAGE_FILES.cash}, merged by ${LANE}/package.cjs`;
  return p;
}

// ---------------------------------------------------------------------------------------------------
// The API for a merged payload on a September 29-style package.
const S4 = P27.LR.meta.s;
function forCase(base, payload0) {
  const payload = clone(payload0);
  const p4 = base.correctionsPayload();
  const R4 = p4.meta.responses, R5 = payload.meta.responses;
  for (const k of ["lines", "receipt_lines"]) if (JSON.stringify(payload[k]) !== JSON.stringify(p4[k])) blocked(`the payload's ${k} are not the base's`);
  const n4 = p4.edits.length;
  if (payload.edits.length < n4 || JSON.stringify(payload.edits.slice(0, n4)) !== JSON.stringify(p4.edits)) blocked("the payload's first edits are not the base's");
  const ADD = payload.edits.slice(n4);
  const lin = payload.meta.lineage || null;
  if ((ADD.length > 0) !== !!lin) blocked("lineage edits without meta.lineage, or the reverse");
  const ROW8 = lin ? lin.edits.row8_edit_index - n4 : -1;
  if (lin && (lin.edits.first !== n4 || lin.edits.count !== ADD.length)) blocked("meta.lineage.edits does not locate the lineage's edits");
  const prod4 = p4.production, prod5 = payload.production;
  const sameProd = JSON.stringify(prod5) === JSON.stringify(prod4);
  if (!sameProd && (JSON.stringify(prod5.dims) !== JSON.stringify(prod4.dims) || JSON.stringify(prod5.sampling_se_bn) !== JSON.stringify(prod4.sampling_se_bn))) {
    blocked("the payload's production grid is not the base's with new P and F");
  }
  const DP = sameProd ? null : Object.fromEntries(["private_wtp_bn", "induced_receipts_bn"].map((k) => [k, prod5[k].map((v, i) => v - prod4[k][i])]));
  const badR = responseDiffs(R4, R5).filter((x) => !allowedDiff(x));
  if (badR.length) blocked(`the payload changes responses that do not depend on the group's size: ${badR.join(", ")}`);
  const K4 = p4.meta.capital_return, K5 = payload.meta.capital_return;
  const keyless = (K) => clone(K).components.map((c) => { if (c.response.kind === "long_run_subfunction") delete c.response.values; return c; });
  if (JSON.stringify(keyless(K4)) !== JSON.stringify(keyless(K5))) blocked("the payload's capital rules are not the base's");
  if (R4.general_government.s !== S4) blocked("the base's group share is not the long-run lane's");
  const LR4 = longRunAt(tableOf(R4), S4), LR5 = longRunAt(tableOf(R5), R5.general_government.s);
  const GG4 = R4.general_government, GG5 = R5.general_government;
  const subfunctionResponses = (variant, reading) => LR5.subfunctionResponses(variant, reading);
  function blendedResponses(variant, reading) {
    if (variant === "adopted") return Object.fromEntries(LR_LINES.map((id) => [id, R5[id][reading]]));
    const r = subfunctionResponses(variant, reading);
    return Object.fromEntries(LR_LINES.map((id) => [id, SUBS.filter((sf) => sf.line === id).reduce((a, sf) => a + sf.share_of_line * r[sf.id], 0)]));
  }
  const blended4 = (variant, reading) => (variant === "adopted" ? Object.fromEntries(LR_LINES.map((id) => [id, R4[id][reading]])) : P27.blendedResponses(variant, reading));
  const ggFinite = (oo) => !oo || oo.finite === "all" || oo.finite === "gg";

  // A line response at a specification's reading, moved to v5.
  function lineResponse(k, v, s) {
    const rd = s.reading;
    if (LR_LINES.includes(k) || k in ROADS || k === REC_PRICE) {
      if (!s.long_run) return v;
      const id = k === REC_PRICE ? "recreation_culture" : k;
      const was = k in ROADS ? LR4.subfunctionResponses(s.long_run, rd)[ROADS[k]] : blended4(s.long_run, rd)[id];
      const now = k in ROADS ? subfunctionResponses(s.long_run, rd)[ROADS[k]] : blendedResponses(s.long_run, rd)[id];
      if (v === was) return now;
      if (v === 0 || v === 1) return v;
      blocked(`${k} responds at ${v} under long-run variant ${s.long_run}, neither its reading ${was} nor 0 or 1`);
    }
    if (PROPERTY.some((id) => k === "receipt:" + id)) return moveLeaf(R4[k.slice(8)][rd], R5[k.slice(8)][rd], v);
    return v;
  }
  function moveSpec(s, oo) {
    if (!READINGS.includes(s.reading)) blocked("a specification without a reading");
    const x = Object.assign({}, s);
    if ("gg" in s) x.gg = ggFinite(oo) ? moveLeaf(GG4[s.reading], GG5[s.reading], s.gg) : s.gg;
    if (s.line_responses) x.line_responses = Object.fromEntries(Object.entries(s.line_responses).map(([k, v]) => [k, lineResponse(k, v, s)]));
    return x;
  }

  // ---------------------------------------------------------------------------------------------------
  // Capital: the payload's components (v4's rules; the long-run values are v5's readings), and the long-run subfunction
  // responses at v5.
  const K5byId = new Map(K5.components.map((c) => [c.id, c])), K4byId = new Map(K4.components.map((c) => [c.id, c]));
  function componentsFor(variant) {
    return base.componentsFor(variant).map((c) => {
      const a = K4byId.get(c.id), b = K5byId.get(c.id);
      if (!a || !b || JSON.stringify(c.response) !== JSON.stringify(a.response) || JSON.stringify(a.response) === JSON.stringify(b.response)) return c;
      return Object.assign({}, c, { response: clone(b.response) });
    });
  }
  const ruleOf = (variant, id) => {
    const c = base.componentsFor(variant).find((x) => x.id === id) || P27.componentsFor(variant).find((x) => x.id === id);
    if (!c) blocked(`no capital rule for component ${id}`);
    return c.response;
  };
  function moveCapital(evaluation, spec, r) {
    if (!r.components.length || !spec.long_run) return r;
    let moved = false;
    const components = r.components.map((c) => {
      const rule = ruleOf(spec.capital_variant, c.id);
      if (rule.kind !== "long_run_subfunction") return c;
      const row = evaluation.spending.find((l) => l.id === rule.line);
      if (!row) blocked(`the evaluation has no line ${rule.line}`);
      if (!(spec.line_responses && row.response === spec.line_responses[rule.line])) return c;
      const was = LR4.subfunctionResponses(spec.long_run, spec.reading)[rule.subfunction];
      if (c.response !== was) blocked(`capital component ${c.id} responds at ${c.response}, not its long-run reading ${was}`);
      const now = subfunctionResponses(spec.long_run, spec.reading)[rule.subfunction];
      if (now === c.response) return c;
      moved = true;
      return Object.assign({}, c, { response: now, return_bn: c.stock_charged_bn * spec.rate * c.key * now });
    });
    if (!moved) return r;
    return { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
  }
  const capitalReturn = (evaluation, spec) => moveCapital(evaluation, spec, base.capitalReturn(evaluation, spec));
  function responseOfRule(evaluation, spec, rule) {
    const r = P27.responseOfRule(evaluation, spec, rule);
    if (rule.kind !== "long_run_subfunction" || !spec.long_run) return r;
    const row = evaluation.spending.find((l) => l.id === rule.line);
    if (!(spec.line_responses && row.response === spec.line_responses[rule.line])) return r;
    return subfunctionResponses(spec.long_run, spec.reading)[rule.subfunction];
  }
  function capitalMeta(oo) {
    return Object.assign(clone(K5), { rates: { low: oo.rates.low, high: oo.rates.high, reported: P27.RATES.reported }, enterprises: oo.enterprises,
      variant: oo.capital_variant || null,
      components: componentsFor(oo.capital_variant).map((c) => ({ id: c.id, label: c.label, part: c.part, level: c.level,
        bea_source: c.bea_source, stock_charged_bn: c.stock_charged_bn, key: c.key, response: c.response })) });
  }

  // ---------------------------------------------------------------------------------------------------
  // Models: the base's, plus the lineage.
  const ITEMS = base.ITEMS, ITEM_KEYS = Object.keys(ITEMS);
  function lineageEdits(oo) {
    if (!ADD.length && sameProd) return null;
    if (oo && oo.pension4 !== undefined && oo.pension4 !== ITEMS.pension4) {
      blocked(`the lineage here is priced with the pension switch ${ITEMS.pension4}; with ${oo.pension4} use that set's case (P.CASH)`);
    }
    return ggFinite(oo) ? ADD : ADD.filter((_, i) => i !== ROW8);
  }
  const hasCell = (m, e) => (e.side === "receipt" ? m.receipts.lines.some((l) => l.id === e.line && l.cells[e.scenario])
    : m.spending.lines.some((l) => l.id === e.line && l.keys[e.key]));
  const sameArrays = (a, b) => a.length === b.length && a.every((v, i) => v === b[i]);
  // An option can change a line's national total, split a part of a line off into a new line (item 8's transit split),
  // or leave out a line the case's items add (an item off: the split receipts merge back into their lines, the
  // correction lines go). The added people keep their key, the case's amount over the national, on every line: their
  // amount scales with a line's national, a part split off a line takes that line's key, and a line an option leaves
  // out takes their amount on it along (its part of a merged line is priced at that line's key, through the scaling)
  // [ASSUMPTION: the added people's keys are the case's under every option]. Only the payload's own lines may go.
  const lineId = (side, id) => `${side === "receipt" || side === "receipts" ? "receipt" : "spending"}:${id}`;
  const nationalsOf = (m) => new Map(m.spending.lines.map((l) => [lineId("spending", l.id), l.national_bn])
    .concat(m.receipts.lines.map((l) => [lineId("receipt", l.id), l.national_bn])));
  const REMOVABLE = new Set(base.PAYLOAD_LINES.map((l) => lineId("spending", l.id)).concat(base.PAYLOAD_RECEIPT_LINES.map((id) => lineId("receipt", id))));
  let N_CASE = null;
  const caseNationals = () => N_CASE || (N_CASE = nationalsOf(base.modelFor("central", METHODS[0], base.withCentral({}))));
  const scaled = (e, f) => Object.assign({}, e, { by: Object.fromEntries(Object.entries(e.by).map(([a, v]) => [a, v * f])) });
  function followNationals(edits, m) {
    const N0 = caseNationals(), N = nationalsOf(m);
    const changed = [...N.keys()].filter((k) => N0.has(k) && N.get(k) !== N0.get(k));
    const added = [...N.keys()].filter((k) => !N0.has(k));
    const gone = [...N0.keys()].filter((k) => !N.has(k));
    if (!changed.length && !added.length && !gone.length) return edits;
    const of = (e) => lineId(e.side, e.line);
    if (edits.some((e) => !e.by || Object.keys(e).some((f) => !["by", "key", "line", "scenario", "side"].includes(f)))) blocked("a lineage edit that is not a cell shift");
    const lost = gone.filter((k) => !REMOVABLE.has(k));
    if (lost.length) blocked(`an option leaves out ${lost.join(", ")}, which the case's payload does not add`);
    const out = edits.filter((e) => !gone.includes(of(e))).map((e) => {
      if (!changed.includes(of(e))) return e;
      if (!(N0.get(of(e)) !== 0)) blocked(`an option moves ${of(e)}'s national total from 0`);
      return scaled(e, N.get(of(e)) / N0.get(of(e)));
    });
    for (const s of added) {
      const parents = changed.filter((k) => k.split(":")[0] === s.split(":")[0] && Math.abs(N.get(k) + N.get(s) - N0.get(k)) < 1e-6);
      if (parents.length !== 1) blocked(`the line ${s} an option adds is not split off exactly one line`);
      const from = edits.filter((e) => of(e) === parents[0]);
      if (from.some((e) => e.side !== "receipt")) blocked(`${s} is split off a spending line; the added people's key on it is not defined`);
      for (const e of from) out.push(Object.assign(scaled(e, N.get(s) / N0.get(parents[0])), { line: s.slice("receipt:".length) }));
    }
    return out;
  }
  function withLineage(m, oo) {
    const edits0 = lineageEdits(oo);
    if (!edits0) return m;
    const edits = followNationals(edits0, m);
    const missing = edits.filter((e) => !hasCell(m, e));
    if (missing.length) blocked(`the model lacks ${missing.length} cells the lineage adds to (${missing.slice(0, 3).map((e) => `${e.side}/${e.line}`).join(", ")}): build it with the case's lines`);
    let production;
    if (!sameProd) {
      if (!sameDims(m.production.dims, prod5.dims)) blocked("the model's production grid is not the case's");
      production = ["private_wtp_bn", "induced_receipts_bn", "sampling_se_bn"].every((k) => sameArrays(m.production[k], prod4[k])) ? clone(prod5)
        : { dims: clone(m.production.dims), private_wtp_bn: m.production.private_wtp_bn.map((v, i) => v + DP.private_wtp_bn[i]),
          induced_receipts_bn: m.production.induced_receipts_bn.map((v, i) => v + DP.induced_receipts_bn[i]), sampling_se_bn: m.production.sampling_se_bn.slice() };
    }
    const out = Engine.applyCorrections(m, { edits, production, meta: m.corrections });
    if (!("corrections" in m)) delete out.corrections;
    return out;
  }
  const modelFor = (caseName, method, oo) => withLineage(base.modelFor(caseName, method, oo), oo);
  const payloadModel = () => Engine.applyCorrections(MODEL, payload);

  // ---------------------------------------------------------------------------------------------------
  // Specifications and evaluation.
  const FULL = new WeakMap();
  function specsFor(o) {
    const oo = base.withCentral(o);
    const stripped = base.specsFor(o), full = V4.specsFor(oo);
    if (stripped.length !== full.length || stripped.some((s, i) => JSON.stringify(s) !== JSON.stringify(V4P.stripSpec(full[i])))) {
      blocked("the base package's specifications are not candidate v4's stripped");
    }
    return stripped.map((s, i) => { const x = moveSpec(s, oo); FULL.set(x, moveSpec(full[i], oo)); return x; });
  }
  const itemsOfModel = (m) => (m.candidate ? Object.assign({}, m.candidate, m.candidate.v3 || {}, m.candidate.v4 || {}) : null);
  const sameItems = (x) => ITEM_KEYS.every((k) => !(k in x) || x[k] === ITEMS[k]);
  // Candidate v4 keys the road capital (hwy_sl, hwy_fed) at a road key it computes when it builds the model, before the
  // lineage's edits; the case keys a part_rekeyed component on the evaluation (base.keyOf), which counts the added
  // people's road amounts. The two agree exactly without the lineage (main_case.cjs gates the route on the case).
  function rekeyParts(evaluation, spec, cap) {
    if (spec.roads !== "miles" || !cap.components.length) return cap;
    const rules = new Map(base.componentsFor(spec.capital_variant).map((c) => [c.id, c.key]));
    let moved = false;
    const components = cap.components.map((c) => {
      const rule = rules.get(c.id);
      if (!rule || rule.kind !== "part_rekeyed") return c;
      const key = base.keyOf(evaluation, rule);
      if (key === c.key) return c;
      moved = true;
      return Object.assign({}, c, { key, return_bn: c.stock_charged_bn * spec.rate * key * c.response });
    });
    return moved ? { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) } : cap;
  }
  // The item variants' route: candidate v4's evaluateFull at the moved specification, then the road keys and the
  // long-run capital responses moved to the case's.
  function viaCandidate(m0, spec, profile) {
    const full = FULL.get(spec);
    if (!full) blocked("a specification specsFor() did not build");
    const r = V4.evaluateFull(m0, full, profile);
    const capital = moveCapital(r.evaluation, full, rekeyParts(r.evaluation, full, r.capital));
    return { evaluation: r.evaluation, capital, cost_bn: capital === r.capital ? r.cost_bn : r.cost_bn + (capital.total_bn - r.capital.total_bn) };
  }
  function evaluateFull(m0, spec, profile) {
    const full = FULL.get(spec), tag = itemsOfModel(m0);
    if ((full && !sameItems(full)) || (tag && !sameItems(tag))) {
      if (!full) blocked("a model built for other item options than the case's, with a specification specsFor() did not build for them");
      return viaCandidate(m0, spec, profile);
    }
    const m = base.withSyntheticLines(m0);
    const evaluation = Engine.evaluate(m, base.stateFor(m, spec, profile));
    const capital = capitalReturn(evaluation, spec);
    return { evaluation, capital, cost_bn: -evaluation.welfare_bn + capital.total_bn };
  }
  const cost = (m, spec, profile) => evaluateFull(m, spec, profile).cost_bn;
  const bandFor = (m, profile, specs) => span(specs.map((spec) => cost(m, spec, profile)));
  function evalPackage(caseName, method, o) {
    const oo = base.withCentral(o);
    return bandFor(modelFor(caseName, method, oo), oo.profile, specsFor(oo));
  }
  const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
  const MAIN_SPECS = specsFor({});
  const band = (m, profile) => bandFor(m, profile, MAIN_SPECS);

  // The line responses meta.responses sets, in the base's order, from this payload.
  const LINE_RESPONSES = Object.fromEntries(Object.keys(base.LINE_RESPONSES).map((k) => {
    const e = k.startsWith("receipt:") ? R5[k.slice(8)] : R5[k];
    if (!e || (k.startsWith("receipt:") && (e.receipt !== true || e.override !== k))) blocked(`meta.responses has no entry for ${k}`);
    return [k, clone(e)];
  }));
  for (const s of MAIN_SPECS) {
    const keys = Object.keys(s.line_responses), want = Object.keys(LINE_RESPONSES);
    if (keys.length !== want.length || keys.some((k, i) => k !== want[i] || s.line_responses[k] !== LINE_RESPONSES[k][s.reading])) {
      blocked(`a specification's line responses are not meta.responses at its ${s.reading} reading`);
    }
    if (s.gg !== GG5[s.reading]) blocked(`a specification's general government is not meta.responses at its ${s.reading} reading`);
  }

  // Responses at an option set: the base's, with the group-size entries moved as the specifications move.
  function responsesFor(o) {
    const oo = base.withCentral(o);
    const r = clone(base.responsesFor(o));
    const fin = ggFinite(oo);
    if (r.general_government && fin) {
      for (const rd of READINGS) r.general_government[rd] = moveLeaf(GG4[rd], GG5[rd], r.general_government[rd]);
      if (isNum(r.general_government.s)) r.general_government.s = moveLeaf(GG4.s, GG5.s, r.general_government.s);
    }
    if (isNum(r.row8_factor) && fin) r.row8_factor = moveLeaf(R4.row8_factor, R5.row8_factor, r.row8_factor);
    for (const line of LR_LINES) {
      const e = r[line];
      if (!e || !e.variant) continue;
      for (const rd of READINGS) {
        const was = blended4(e.variant, rd)[line], now = blendedResponses(e.variant, rd)[line];
        if (e[rd] === was) e[rd] = now; else if (e[rd] !== 0 && e[rd] !== 1) blocked(`responses ${line}.${rd} is not its long-run reading`);
        const sf4 = LR4.subfunctionResponses(e.variant, rd), sf5 = subfunctionResponses(e.variant, rd);
        for (const x of e.subfunctions || []) {
          if (x[rd] === sf4[x.id]) x[rd] = sf5[x.id]; else if (x[rd] !== 0 && x[rd] !== 1) blocked(`responses ${line} ${x.id}.${rd} is not its long-run reading`);
        }
      }
    }
    const variantOf = r[LR_LINES[0]] && r[LR_LINES[0]].variant;
    for (const [id, sub] of Object.entries(ROADS)) {
      if (!r[id] || !variantOf) continue;
      for (const rd of READINGS) {
        const was = LR4.subfunctionResponses(variantOf, rd)[sub], now = subfunctionResponses(variantOf, rd)[sub];
        if (r[id][rd] === was) r[id][rd] = now; else if (r[id][rd] !== 0 && r[id][rd] !== 1) blocked(`responses ${id}.${rd} is not its long-run reading`);
      }
    }
    if (r[REC_PRICE] && variantOf) for (const rd of READINGS) {
      const was = blended4(variantOf, rd).recreation_culture, now = blendedResponses(variantOf, rd).recreation_culture;
      if (r[REC_PRICE][rd] === was) r[REC_PRICE][rd] = now;
    }
    for (const id of PROPERTY) if (r[id]) for (const rd of READINGS) r[id][rd] = moveLeaf(R4[id][rd], R5[id][rd], r[id][rd]);
    return r;
  }
  if (JSON.stringify(responsesFor({})) !== JSON.stringify(R5)) blocked("responsesFor({}) is not meta.responses");

  // The payload itself, or, with options, the base's payload of that variant with the lineage added.
  function correctionsPayload(o) {
    if (!o || !Object.keys(o).length) return clone(payload);
    const oo = base.withCentral(o);
    const p = base.correctionsPayload(o);
    const edits = lineageEdits(oo);
    if (!edits) return p;
    p.edits = p.edits.concat(clone(followNationals(edits, Engine.applyCorrections(MODEL, p))));
    if (!sameProd) {
      p.production = ["private_wtp_bn", "induced_receipts_bn", "sampling_se_bn"].every((k) => sameArrays(p.production[k], prod4[k])) ? clone(prod5)
        : Object.assign({}, p.production, { private_wtp_bn: p.production.private_wtp_bn.map((v, i) => v + DP.private_wtp_bn[i]),
          induced_receipts_bn: p.production.induced_receipts_bn.map((v, i) => v + DP.induced_receipts_bn[i]) });
    }
    p.meta.responses = responsesFor(o);
    p.meta.lineage = Object.assign(clone(lin), { note: "the lineage's amounts at the case's options, scaled with any line total the options change (package.cjs followNationals()); the group-size responses moved by package.cjs moveSpec()'s rule" });
    return p;
  }

  return Object.assign({}, base, {
    MAIN_SPECS, RESPONSES: clone(R5), LINE_RESPONSES, specsFor, responsesFor, subfunctionResponses, blendedResponses, responseOfRule,
    componentsFor, capitalReturn, capitalMeta, evaluateFull, cost, bandFor, band, evalPackage, central, modelFor, payloadModel,
    correctionsPayload, moveSpec, withLineage, viaCandidate, LINEAGE_EDITS: clone(ADD), LINEAGE_META: lin ? clone(lin) : null, BASE: base,
  });
}

// ---------------------------------------------------------------------------------------------------
// Load-time checks: the re-implemented long-run variants are the September 27 package's at v4.
{
  const LR4 = longRunAt(tableOf(V4P.RESPONSES), S4);
  for (const v of Object.keys(P27.LONG_RUN_VARIANTS)) for (const rd of READINGS) {
    const a = LR4.subfunctionResponses(v, rd), b = P27.subfunctionResponses(v, rd);
    if (SUBS.some((sf) => a[sf.id] !== b[sf.id])) blocked(`longRunAt() is not the September 27 package's ${v} at the ${rd} reading`);
  }
}
const ADDITION = { set: readJson(LINEAGE_FILES.set), cash: readJson(LINEAGE_FILES.cash) };
for (const which of ["set", "cash"]) {
  const L = ADDITION[which].meta.lineage;
  if (L.arm !== POP.meta.central_arm || L.c3.value !== POP.c3.value || L.c3.override || ADDITION[which].meta.status.startsWith("TEST RUN")) {
    blocked(`${LINEAGE_FILES[which]}: not the central arm at population.json's C3, or a test run`);
  }
}
const CASH4 = V4P.forPayload(readJson(BASE_FILES.cash));
const PAYLOAD = adoptLineage(merge(V4P.correctionsPayload(), ADDITION.set, "set"), "set");
const CASH_PAYLOAD = adoptLineage(merge(CASH4.correctionsPayload(), ADDITION.cash, "cash"), "cash");
const CASH = Object.assign(forCase(CASH4, CASH_PAYLOAD), { HERE, LANE });

module.exports = Object.assign(forCase(V4P, PAYLOAD), {
  HERE, LANE, ADOPTED, DECISION, STAMPED, LINEAGE_LANE, LINEAGE_FILES, POPULATION_FILE, BASE_FILES, GROUP_PATHS: [...GROUP_PATHS],
  SEPT29: V4P, SEPT29_CASH: CASH4, CASH, CASH_PAYLOAD, ADDITION, POP,
  forCase, merge, adoptLineage, longRunAt, moveLeaf, responseDiffs, tableOf, sha256,
});
