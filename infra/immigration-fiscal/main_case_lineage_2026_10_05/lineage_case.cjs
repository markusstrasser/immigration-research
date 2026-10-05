/* Candidate main case v5 (not adopted): the adopted v4 case (main_case_2026_09_29, $371.4146-434.8410bn; cash set
 * $294.7011-361.8175bn) plus the lineage line, the descendants of Mexican immigrants whom the account misses because
 * they no longer report Mexican origin (operator, 2026-10-05: the headline describes the whole population Mexican
 * immigration produced; leaving out descendants the survey cannot see is a convention-driven zero).
 *
 * Who is added (population.py -> derived/population.json): the identity-loss correction of the self-identified
 * third-plus on the account's frame, by arm (a: G4+ at the G3 rate; b, central: one measured further step, held; c:
 * compounding, rho 0.5; the floor beside), split into G3-rate attriters and later losses by the measured generation
 * split. Every added person counts whole, as the union counts mixed-ancestry identifiers.
 *
 * How they are priced, under the case's own rules:
 *   later losses        as identified G3+ members, convention (a) (each person in their own generation): the
 *                       generation account's corrected G3+ model (model_G3plus.json + generation_corrections_sept29
 *                       payloads.a.G3plus) per member, every engine cell and the production grid;
 *   G3-rate attriters   G3+ - C3 x (G3+ - W) = (1 - C3) x G3+ + C3 x W, line by line, W being third-plus non-Hispanic
 *                       whites under the v4 rules (white_lines.py: the white lane's sept29 rough re-key) per person,
 *                       in every cell of its line, at the identified G3+'s age structure: C3 closes gaps matched by
 *                       age and sex, and the attriters are assumed to have identified G3+'s age mix (whites at their
 *                       own ages are a row beside). Whites carry no production term and none of the engine's
 *                       union-only corrections. C3 is SPLIT_C3's central entry, imported in population.py.
 * So the added people are m_G = later + (1 - C3) g3 G3+ members and m_W = C3 g3 whites.
 *
 * The engine on the augmented group (the faithful route). The union's corrected model (the v4 payload on model.json,
 * the methods' mean) takes the added persons' amounts as cell edits (Engine.applyCorrections moves them out of other
 * residents, so national totals hold) and their production grid, and is evaluated at the 64 specifications with every
 * group-size response recomputed at the augmented group:
 *   - finite removal r = [1 - (1 - s)^b] / s at s = (40.896574m + added) / 340.110988m: general government (low and
 *     high, finite_response_2026_09_26 r_values.py), audit row 8's factor (one edit on lane_constants:
 *     2.0 x (f - f_v4)), the long-run road and park subfunctions (service_response_long_run_2026_09_27 build.py's
 *     rules, capped at 1) and their line blends, roads_vmt_sl/fed, state_price_recreation_culture and the capital
 *     components keyed long_run_subfunction;
 *   - the long-run owner and tenant property responses (receipt_side_long_run_2026_09_28 housing.py): each metro's
 *     group share times 1 + added / the ACS proxy group, the added persons living where the group lives [ASSUMPTION].
 * Each response is its stored v4 value plus the change of its formula from the v4 share to the augmented share, so zero
 * added persons give the v4 responses bit for bit; the formulas are gated against the stored values at the v4 share.
 * The capital return is the package's capitalReturn rule with the long_run_subfunction responses at the augmented share
 * (gated equal to the package's at v4, component by component). The engine is linear in cell amounts at given
 * responses, so the case splits exactly into the union at the new responses, the G3+ part and the white part (gated).
 *
 * Gates (derived/gates.json, with population.py's and white_lines.py's; a failed gate writes nothing else):
 *   - zero added persons reproduce v4 exactly: the set and the cash set at all 64 specifications (the package's own
 *     evaluateFull, 0 difference), the published bands (5e-5, four decimals) and the per-specification methods' mean;
 *   - the corrected G3+ model reproduces generation_results_sept29(_cash).csv convention (a) G3plus cost and per member
 *     ($8,548.89 / $11,739.52; 5e-7 bn, half the CSV's last digit);
 *   - the recomputed responses equal the stored ones at the v4 share (1e-14; property 5e-6, its six-decimal inputs);
 *   - the augmented model equals the sum of its parts at every specification (1e-9), and per-line parts add to the
 *     totals; printed parts add to printed totals (controlled rounding);
 *   - the payload addition, applied by a consumer to the v4 payload model with its meta's responses and capital values,
 *     gives the same band.
 *
 * Two framing sensitivities for mixed ancestry (team-lead, 2026-10-05), beside the whole-person central:
 *   replacement   without the immigration a native parent of a mixed descendant would likely have had a child anyway,
 *                 with another native: the band net of r x W x added persons, r 1 and 0.5, W the same third-plus white
 *                 per person (at the identified G3+'s ages, at the arm's responses) as the C3 blend uses;
 *   fractional    the people-conserving lineage count (lineage_cost_2026_09_19 per_capita, TFR/2): every member counts
 *                 by their share of Mexican-immigrant ancestry (fractional.py -> derived/fractional_shares.json), each
 *                 generation's share priced at that generation's cost per member. The three generation models
 *                 (convention a, corrected) are evaluated at the arm's responses; they add to the union at every
 *                 specification (gate), and with every share at 1 the count gives the whole-person band (gate).
 * Writes derived/v5_bands.csv, v5_summary.json, lineage_lines.csv, lineage_lines_printed.csv, lineage_payload.json,
 * lineage_payload_cash.json, fractional_lineage.csv and gates.json. Run from the repository root after population.py,
 * white_lines.py and fractional.py:
 *   node infra/immigration-fiscal/main_case_lineage_2026_10_05/lineage_case.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.resolve(HERE, "..");
const LANE = path.basename(HERE);
const OUT = path.join(HERE, "derived");
const P = require(path.join(FISCAL, "main_case_2026_09_29", "package.cjs"));
const { Engine, MODEL } = P;
const PROFILE = P.MAIN_PROFILE;
const read = (rel) => fs.readFileSync(path.join(FISCAL, rel), "utf8");
const readJson = (rel) => JSON.parse(read(rel));
const clone = (x) => JSON.parse(JSON.stringify(x));
const sum = (xs) => xs.reduce((a, b) => a + b, 0);
const ALLOCS = ["personal", "shared"];
const ENDS = ["low", "high"];

const GATES = [];
function gate(name, ok, detail) {
  GATES.push({ gate: name, passed: !!ok, detail: detail || "" });
  console.log(`  ${ok ? "✓" : "✗"} ${name}${detail ? " — " + detail : ""}`);
}
const ex = (x) => x.toExponential(1);
const stop = () => {
  const failed = GATES.filter((g) => !g.passed);
  if (failed.length) {
    console.log(`✗ ${failed.length} gate(s) failed, nothing written: ${failed.map((g) => g.gate).join("; ")}`);
    process.exit(1);
  }
};

// ---------------------------------------------------------------------------------------------------
// Inputs.
const POP = readJson(`${LANE}/derived/population.json`);
const WL = readJson(`${LANE}/derived/white_lines.json`);
const SH = readJson(`${LANE}/derived/fractional_shares.json`).shares;
const GENS = ["G1", "G2", "G3plus"];
const RV = readJson("finite_response_2026_09_26/derived/r_values.json");
const LR = readJson("service_response_long_run_2026_09_27/derived/responses.json");
const HOUSING = readJson("receipt_side_long_run_2026_09_28/derived/housing.json");
const COUNTIES = P.csvRows("receipt_side_long_run_2026_09_28/derived/counties.csv");
const GEN = "generation_account_2026_09_24/derived";
const BANDS = Object.fromEntries(P.csvRows("main_case_2026_09_29/derived/main_case_bands.csv")
  .filter((r) => r.profile === PROFILE).map((r) => [r.variant, [Number(r.cost_low_bn), Number(r.cost_high_bn)]]));
const CASH_REL = "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json";
const SET_REL = "main_case_2026_09_29/derived/corrections.json";
const SETS = {
  set: { label: "the case (pension accrual)", pkg: P, payloadRel: SET_REL, gen: "generation_corrections_sept29.json",
    results: "generation_results_sept29.csv", white: "accrual", band: "adopted" },
  cash: { label: "the cash set (pension switch off)", pkg: P.forPayload(readJson(CASH_REL)), payloadRel: CASH_REL,
    gen: "generation_corrections_sept29_cash.json", results: "generation_results_sept29_cash.csv", white: "cash", band: "cash_set" },
};
const C3 = POP.c3.value;
const NG = POP.meta.g3_account;
const WHITE_AGES = "g3plus_ages";   // whites' per-age rates at the identified G3+'s age structure (white_lines.py)
const ARMS = Object.keys(POP.arms);
const CENTRAL = POP.meta.central_arm;
const ROW8_C = 2.0;   // main_case_2026_09_24/package.cjs CONSTANTS.row8.c, gated below

console.log(`[inputs] C3 ${C3} (${POP.c3.label}); arms ${ARMS.join(", ")}, central ${CENTRAL}; G3+ members ${NG.toFixed(3)}`);
const STATUS = POP.c3.override ? "TEST RUN (C3 from --c3-override, not SPLIT_C3): not for use" : "candidate v5, not adopted";
if (POP.c3.override) console.log(`[OVERRIDE] population.json carries a test C3 (${C3}); every output is marked a test run`);
gate("audit row 8's constant is the September 24 package's 2.0", P.CONSTANTS && P.CONSTANTS.row8 && P.CONSTANTS.row8.c === ROW8_C);
gate("the adopted package's payload is main_case_2026_09_29/derived/corrections.json, byte for byte as JSON",
  JSON.stringify(P.correctionsPayload()) === JSON.stringify(readJson(SET_REL)));

// ---------------------------------------------------------------------------------------------------
// Group-size responses. Each is its stored v4 value plus the change of its formula between the v4 share and the
// augmented one, so zero added persons give the stored values exactly.
const R4 = P.correctionsPayload().meta.responses;
const S4 = POP.meta.s_v4;
const rFin = (b, s) => (1 - Math.pow(1 - s, b)) / s;
const cap1 = (x) => Math.min(x, 1);
const ggOf = (s) => ({ low: (RV.state_local_bn * rFin(RV.b_admin, s) + RV.federal_tax_bn * rFin(RV.b_fin, s)) / RV.total_bn,
  high: rFin(RV.b_admin, s) });
const row8Of = (s) => (rFin(RV.b_all, s) - rFin(RV.b_admin, s)) / (RV.b_all - RV.b_admin);
const HWY = LR.elasticities.highways_nontoll, PARKS = LR.elasticities.parks, B_ADMIN = LR.elasticities.administration_general_government.b;
// service_response_long_run_2026_09_27/build.py RULES, subfunction by subfunction (gated at the lane's s below).
const SF_RULE = {
  fed_highways: "fed_highways", fed_air: "fed_highways", fed_transit_and_railroad: "fed_highways", fed_water: "zero",
  fed_space: "zero", fed_general_economic_and_labor_affairs: "fed_admin", fed_agriculture: "zero", fed_energy: "zero",
  fed_natural_resources: "zero", fed_postal_service: "zero", sl_highways: "highways", sl_transit_and_railroad: "highways",
  sl_general_economic_and_labor_affairs: "admin", sl_agriculture: "zero", sl_energy: "zero", sl_natural_resources: "zero",
  sl_other_commercial_activities: "zero", fed_recreation_and_culture: "fed_parks", sl_recreation_and_culture: "parks",
};
function sfRuleAt(rule, s) {
  const hw = { low: cap1(rFin(HWY.across_states.b, s)), high: cap1(rFin(HWY.within_states.b, s)) };
  const pk = { low: cap1(rFin(PARKS.across_states.b, s)), high: cap1(rFin(PARKS.within_states.b, s)) };
  const ad = rFin(B_ADMIN, s);
  const R = {
    highways: { low: hw.low, high: hw.high, across_high: hw.low }, parks: { low: pk.low, high: pk.high, across_high: pk.low },
    fed_highways: { low: 0, high: hw.high, across_high: hw.low }, fed_parks: { low: 0, high: pk.high, across_high: pk.low },
    admin: { low: ad, high: ad, across_high: ad }, fed_admin: { low: 0, high: ad, across_high: ad }, zero: { low: 0, high: 0, across_high: 0 },
  }[rule];
  if (!R) throw new Error("[BLOCKED] unknown subfunction rule " + rule);
  return R;
}
const LR_LINES = Object.keys(LR.lines);
const SUBS = LR_LINES.flatMap((line) => LR.lines[line].subfunctions.map((x) => Object.assign({ line }, x)));
// The property price fall (housing.py): r = 1 - land + min(1 - (1 - s_metro)^(1 / (1 + e)), land), weighted by the
// group's owner tax (owner) and its rent (tenant).
const CTY = COUNTIES.map((c) => ({ owner: Number(c.group_owner_tax), rent: Number(c.group_rent), land: Number(c.land_share),
  e: Number(c.elasticity), s: Number(c.metro_group_share) }));
function propertyOf(k) {
  let ow = 0, rw = 0, o = 0, t = 0;
  for (const c of CTY) {
    const sm = Math.min(k * c.s, 1);
    const r = 1 - c.land + Math.min(1 - Math.pow(1 - sm, 1 / (1 + c.e)), c.land);
    o += c.owner * r; ow += c.owner; t += c.rent * r; rw += c.rent;
  }
  return { owner: o / ow, tenant: t / rw };
}
const PROP1 = propertyOf(1);
const AT_V4 = { gg: ggOf(S4), row8: row8Of(S4), sf: Object.fromEntries(SUBS.map((x) => [x.id, sfRuleAt(SF_RULE[x.id], S4)])) };

console.log("[responses: the formulas at the v4 share]");
gate("general government: r_values.py's formula at s_v4 gives meta.responses (low, high; 1e-14)",
  Math.abs(AT_V4.gg.low - R4.general_government.low) < 1e-14 && Math.abs(AT_V4.gg.high - R4.general_government.high) < 1e-14
  && R4.general_government.s === S4, `${AT_V4.gg.low} / ${AT_V4.gg.high}`);
gate("audit row 8's factor at s_v4 is meta.responses.row8_factor (1e-14)", Math.abs(AT_V4.row8 - R4.row8_factor) < 1e-14, `${AT_V4.row8}`);
gate("every long-run subfunction has build.py's rule, and the rules at the lane's s give its stored responses (1e-14)",
  LR.meta.s === S4 && SUBS.every((x) => SF_RULE[x.id] && ENDS.every((e) => Math.abs(AT_V4.sf[x.id][e] - x.response[e]) < 1e-14))
  && Object.keys(SF_RULE).length === SUBS.length, `${SUBS.length} subfunctions`);
// build.py blends with Python's sum (compensated since 3.12), so the line's response is its stored blend plus the
// change of this blend; the blend of the stored subfunction responses matches the stored one to rounding.
const blendOf = (line, sf) => LR.lines[line].subfunctions.reduce((a, x) => a + x.national_bn * sf[x.id], 0) / LR.lines[line].national_bn;
const stored = Object.fromEntries(SUBS.map((x) => [x.id, x.response]));
const STORED_BLEND = Object.fromEntries(LR_LINES.map((line) => [line, Object.fromEntries(ENDS.map((e) =>
  [e, blendOf(line, Object.fromEntries(SUBS.map((x) => [x.id, stored[x.id][e]])))]))]));
gate("the line blends of the stored subfunction responses are meta.responses' and the response lane's line responses (2e-16)",
  LR_LINES.every((line) => ENDS.every((e) => Math.abs(STORED_BLEND[line][e] - R4[line][e]) < 2e-16 && R4[line][e] === LR.lines[line].response[e])),
  LR_LINES.map((line) => ENDS.map((e) => ex(STORED_BLEND[line][e] - R4[line][e])).join(" / ")).join("; "));
gate("meta.responses' subfunctions are the response lane's (exact)", LR_LINES.every((line) => R4[line].subfunctions.every((x) => {
  const y = stored[x.id];
  return y && x.low === y.low && x.high === y.high;
})));
gate("the property formula on counties.csv gives housing.json's owner and renter responses and the payload's (5e-6: six-decimal inputs)",
  Math.abs(PROP1.owner - HOUSING.owner.r_lr_metro) < 5e-6 && Math.abs(PROP1.tenant - HOUSING.renter.r_lr_metro) < 5e-6
  && R4.modeled_owner_property.low === HOUSING.owner.r_lr_metro && R4.tenant_occupied_property.low === HOUSING.renter.r_lr_metro,
  `${PROP1.owner.toFixed(7)} / ${PROP1.tenant.toFixed(7)}`);

function responsesAt(s, kMetro) {
  const gg = ggOf(s), row8 = row8Of(s), prop = propertyOf(kMetro);
  const sf = Object.fromEntries(SUBS.map((x) => {
    const now = sfRuleAt(SF_RULE[x.id], s), v4 = AT_V4.sf[x.id];
    return [x.id, { low: x.response.low + (now.low - v4.low), high: x.response.high + (now.high - v4.high),
      across_high: v4.across_high + (now.across_high - v4.across_high) }];
  }));
  const lines = Object.fromEntries(LR_LINES.map((line) => [line, Object.fromEntries(ENDS.map((e) =>
    [e, R4[line][e] + (blendOf(line, Object.fromEntries(SUBS.map((x) => [x.id, sf[x.id][e]]))) - STORED_BLEND[line][e])]))]));
  return {
    s, k_metro: kMetro,
    gg: { low: R4.general_government.low + (gg.low - AT_V4.gg.low), high: R4.general_government.high + (gg.high - AT_V4.gg.high) },
    row8: R4.row8_factor + (row8 - AT_V4.row8),
    sf, lines,
    owner: R4.modeled_owner_property.low + (prop.owner - PROP1.owner),
    tenant: R4.tenant_occupied_property.low + (prop.tenant - PROP1.tenant),
  };
}
// The specification line responses that follow a group-size response; every other entry is checked unchanged.
const FOLLOWS = {
  economic_affairs_services: (R, rd) => R.lines.economic_affairs_services[rd],
  recreation_culture: (R, rd) => R.lines.recreation_culture[rd],
  roads_vmt_sl: (R, rd) => R.sf.sl_highways[rd],
  roads_vmt_fed: (R, rd) => R.sf.fed_highways[rd],
  state_price_recreation_culture: (R, rd) => R.lines.recreation_culture[rd],
  "receipt:modeled_owner_property": (R) => R.owner,
  "receipt:tenant_occupied_property": (R) => R.tenant,
};
function specAt(spec, R) {
  const rd = spec.reading;
  if (spec.gg !== R4.general_government[rd]) throw new Error(`[BLOCKED] a specification whose gg is not the ${rd} reading's`);
  const lr = {};
  for (const [k, v] of Object.entries(spec.line_responses)) lr[k] = FOLLOWS[k] ? FOLLOWS[k](R, rd) : v;
  return Object.assign({}, spec, { gg: R.gg[rd], line_responses: lr });
}
const RV4 = responsesAt(S4, 1);

// ---------------------------------------------------------------------------------------------------
// Evaluation: the package's engine state, and its capital rule with the long-run subfunctions at R.
function capitalAt(pkg, evaluation, spec, R) {
  if (spec.capital_rules !== undefined) throw new Error("capital_rules is gone");
  if (!spec.rate) return { components: [], total_bn: 0 };
  const components = pkg.componentsFor(spec.capital_variant).map((c) => {
    if (c.key.kind === "constant") throw new Error("[BLOCKED] a constant capital key is not linear in the group's amounts");
    const key = pkg.keyOf(evaluation, c.key);
    let response;
    if (c.response.kind === "long_run_subfunction") {
      const r = evaluation.spending.find((l) => l.id === c.response.line).response;
      if (spec.long_run && spec.line_responses && r === spec.line_responses[c.response.line]) {
        if (spec.long_run !== "adopted") throw new Error("[BLOCKED] a long-run variant other than the adopted one");
        response = R.sf[c.response.subfunction][spec.reading];
      } else if (!spec.long_run || r === 0 || r === 1) response = r;
      else throw new Error(`[BLOCKED] ${c.response.line} responds at ${r}`);
    } else response = pkg.responseOfRule(evaluation, spec, c.response);
    return { id: c.id, group: c.part, level: c.level, stock_charged_bn: c.stock_charged_bn, key, response,
      return_bn: c.stock_charged_bn * spec.rate * key * response };
  });
  return { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
}
function evaluateAt(pkg, m0, spec, R) {
  const m = pkg.withSyntheticLines(m0);
  const evaluation = Engine.evaluate(m, pkg.stateFor(m, spec, PROFILE));
  const capital = capitalAt(pkg, evaluation, spec, R);
  return { evaluation, capital, cost_bn: -evaluation.welfare_bn + capital.total_bn };
}

// ---------------------------------------------------------------------------------------------------
// Models: cells, the G3+ per-member model, the white per-person amounts, and the augmented group.
function cellsOf(m) {
  const out = [];
  for (const l of m.receipts.lines) for (const sc of Object.keys(l.cells)) out.push({ side: "receipt", line: l.id, scenario: sc, cell: l.cells[sc] });
  for (const l of m.spending.lines) for (const k of Object.keys(l.keys)) out.push({ side: "spending", line: l.id, key: k, cell: l.keys[k] });
  return out;
}
const cellId = (c) => `${c.side}|${c.line}|${c.side === "receipt" ? c.scenario : c.key}`;
// A model with the template's structure whose group amounts are fn(cell) per allocation and whose production is prod.
function partModel(template, fn, prod) {
  const m = clone(template);
  for (const c of cellsOf(m)) for (const a of ALLOCS) { c.cell[a].target_bn = fn(c, a); c.cell[a].share = 0; }
  m.production.private_wtp_bn = prod.private_wtp_bn.slice();
  m.production.induced_receipts_bn = prod.induced_receipts_bn.slice();
  return m;
}
const zeroGrid = (m) => ({ private_wtp_bn: m.production.private_wtp_bn.map(() => 0), induced_receipts_bn: m.production.induced_receipts_bn.map(() => 0) });
const WSIDE = { receipt: "receipts", spending: "spending" };

function setUp(name) {
  const S = SETS[name];
  const pkg = S.pkg;
  const U = pkg.payloadModel();
  const specs = pkg.MAIN_SPECS;
  console.log(`[${name}: ${S.label}]`);
  gate(`${name}: the package's payload is ${S.payloadRel}`, JSON.stringify(pkg.correctionsPayload()) === JSON.stringify(readJson(S.payloadRel)));
  gate(`${name}: 64 specifications, every one at the case's responses`, specs.length === 64
    && specs.every((s) => JSON.stringify(specAt(s, RV4)) === JSON.stringify(s)));
  // G3+, convention (a).
  const gp = readJson(`${GEN}/${S.gen}`);
  gate(`${name}: ${S.gen} splits ${S.payloadRel}`, gp.meta.union === S.payloadRel, gp.meta.union);
  const G = Engine.applyCorrections(readJson(`${GEN}/model_G3plus.json`), gp.payloads.a.G3plus);
  const sameCells = JSON.stringify(cellsOf(G).map(cellId)) === JSON.stringify(cellsOf(U).map(cellId));
  const sameGrid = JSON.stringify(G.production.dims) === JSON.stringify(U.production.dims);
  gate(`${name}: the G3+ model has the union's cells and production grid`, sameCells && sameGrid);
  // The three corrected generation models (convention a), for the fractional count, and each one's part of the union's
  // lane-constants cell, which carries row 8's edit at a new group size.
  const GM = Object.fromEntries(GENS.map((g) => [g, g === "G3plus" ? G : Engine.applyCorrections(readJson(`${GEN}/model_${g}.json`), gp.payloads.a[g])]));
  const kCell = (m) => m.spending.lines.find((l) => l.id === "lane_constants").keys.k;
  const kShare = Object.fromEntries(GENS.map((g) => [g, Object.fromEntries(ALLOCS.map((a) => [a, kCell(GM[g])[a].target_bn / kCell(U)[a].target_bn]))]));
  const kSum = Math.max(...ALLOCS.map((a) => Math.abs(sum(GENS.map((g) => kShare[g][a])) - 1)));
  gate(`${name}: the generation models' lane-constants cells add to the union's (1e-12)`, kSum < 1e-12, ex(kSum));
  // Whites per person by line: at the identified G3+'s ages (central) and at their own (beside).
  const whiteOf = (ages) => {
    const wl = WL[ages][S.white];
    const W = new Map(wl.low.lines.map((l) => [`${l.side}|${l.id}`, l.amount_bn / wl.low.population]));
    const missing = [...U.receipts.lines.map((l) => `receipts|${l.id}`), ...U.spending.lines.map((l) => `spending|${l.id}`)].filter((k) => !W.has(k));
    gate(`${name}: every line of the model has a white amount (white_lines.json ${ages} ${S.white})`,
      !missing.length && W.size === U.receipts.lines.length + U.spending.lines.length, missing.join(", ") || `${W.size} lines`);
    return (c) => W.get(`${WSIDE[c.side]}|${c.line}`);
  };
  gate(`${name}: white_lines.json's central age structure is the identified G3+'s`, WL.meta.central === WHITE_AGES);
  const wpp = whiteOf(WHITE_AGES), wppOwn = whiteOf("own");
  // Per-person parts: one G3+ member, one white.
  const gCells = new Map(cellsOf(G).map((c) => [cellId(c), c.cell]));
  const G1 = partModel(U, (c, a) => gCells.get(cellId(c))[a].target_bn / NG,
    { private_wtp_bn: G.production.private_wtp_bn.map((x) => x / NG), induced_receipts_bn: G.production.induced_receipts_bn.map((x) => x / NG) });
  const W1 = partModel(U, (c) => wpp(c), zeroGrid(U));
  const W1own = partModel(U, (c) => wppOwn(c), zeroGrid(U));
  return { name, S, pkg, U, specs, G, G1, W1, W1own, gCells, wpp, GM, kShare };
}

// Each generation's cost at every specification at responses R, with its part of row 8's edit.
function generationCosts(X, R, sp) {
  const d8 = ROW8_C * (R.row8 - R4.row8_factor);
  return Object.fromEntries(GENS.map((g) => {
    const m = d8 === 0 ? X.GM[g] : Engine.applyCorrections(X.GM[g], { edits: [{ side: "spending", line: "lane_constants", key: "k",
      by: { personal: d8 * X.kShare[g].personal, shared: d8 * X.kShare[g].shared } }] });
    return [g, sp.map((s) => evaluateAt(X.pkg, m, s, R).cost_bn)];
  }));
}

// The augmented model: the union plus m_G G3+ members and m_W whites as cell edits, the production grid, and audit row
// 8's change on lane_constants.
function augmented(X, mG, mW, R) {
  const edits = cellsOf(X.U).map((c) => {
    const e = { side: c.side, line: c.line, by: {} };
    if (c.side === "receipt") e.scenario = c.scenario; else e.key = c.key;
    for (const a of ALLOCS) e.by[a] = mG * X.gCells.get(cellId(c))[a].target_bn / NG + mW * X.wpp(c);
    return e;
  });
  const d8 = ROW8_C * (R.row8 - R4.row8_factor);
  if (d8 !== 0) edits.push({ side: "spending", line: "lane_constants", key: "k", by: { personal: d8, shared: d8 } });
  const production = { dims: clone(X.U.production.dims),
    private_wtp_bn: X.U.production.private_wtp_bn.map((v, i) => v + mG * X.G.production.private_wtp_bn[i] / NG),
    induced_receipts_bn: X.U.production.induced_receipts_bn.map((v, i) => v + mG * X.G.production.induced_receipts_bn[i] / NG),
    sampling_se_bn: X.U.production.sampling_se_bn.slice() };
  return { edits, production, row8_edit_bn: d8 };
}
const withRow8 = (X, R) => {
  const d8 = ROW8_C * (R.row8 - R4.row8_factor);
  return d8 === 0 ? X.U : Engine.applyCorrections(X.U, { edits: [{ side: "spending", line: "lane_constants", key: "k", by: { personal: d8, shared: d8 } }] });
};

// ---------------------------------------------------------------------------------------------------
const lineRows = (r) => {
  const out = new Map();
  for (const l of r.evaluation.receipts) out.set(`receipt|${l.id}`, -l.effect_bn);      // cost to others: receipts lost
  for (const l of r.evaluation.spending) out.set(`spending|${l.id}`, -l.effect_bn);     // spending saved enters negative
  for (const c of r.capital.components) out.set(`capital|${c.id}`, c.return_bn);
  out.set("production|gain", -(r.evaluation.private_wtp_bn + r.evaluation.induced_receipts_bn));
  return out;
};
// Sign: cost = -welfare + capital = -(P + direct + F) + capital; direct = sum(receipt effects) - sum(spending amounts x
// response), so a receipt line costs -effect and a spending line costs +response x amount = -effect (effect_bn is
// -response x amount).
function costFromLines(rows) { return sum([...rows.values()]); }

const results = {};
const summaries = {};
for (const name of Object.keys(SETS)) {
  const X = setUp(name);
  const { pkg, U, specs } = X;
  // Zero added persons: v4.
  const v4 = specs.map((s) => pkg.evaluateFull(U, s));
  const mine = specs.map((s) => evaluateAt(pkg, U, specAt(s, RV4), RV4));
  const worst0 = Math.max(...specs.map((_, i) => Math.abs(mine[i].cost_bn - v4[i].cost_bn)));
  const worstCap = Math.max(...specs.map((_, i) => Math.max(...v4[i].capital.components.map((c, j) =>
    Math.abs(c.return_bn - mine[i].capital.components[j].return_bn) + (c.id === mine[i].capital.components[j].id ? 0 : Infinity)))));
  gate(`${name}: at zero added persons this lane's evaluation is the package's evaluateFull at all 64 specifications, cost and every capital component`,
    worst0 === 0 && worstCap === 0, `max |diff| ${worst0} / ${worstCap}`);
  const zeroAug = Engine.applyCorrections(U, augmented(X, 0, 0, RV4));
  const zc = specs.map((s) => evaluateAt(pkg, zeroAug, specAt(s, RV4), RV4).cost_bn);
  const worstZ = Math.max(...specs.map((_, i) => Math.abs(zc[i] - v4[i].cost_bn)));
  const v4c = v4.map((r) => r.cost_bn);
  const lo4 = v4c.indexOf(Math.min(...v4c)), hi4 = v4c.indexOf(Math.max(...v4c));
  gate(`${name}: the augmented model with zero added persons reproduces v4 at all 64 specifications (0 difference) and the published ${X.S.band} band (5e-5) at 48 / 11`,
    worstZ === 0 && lo4 === 48 && hi4 === 11 && Math.abs(v4c[lo4] - BANDS[X.S.band][0]) < 5e-5 && Math.abs(v4c[hi4] - BANDS[X.S.band][1]) < 5e-5,
    `${v4c[lo4].toFixed(4)} / ${v4c[hi4].toFixed(4)}; max |diff| ${worstZ}`);
  if (name === "set") {
    const ps = P.csvRows("main_case_2026_09_29/derived/per_spec.csv");
    const methods = [...new Set(ps.map((r) => r.method))];
    let w = 0;
    specs.forEach((_, i) => { w = Math.max(w, Math.abs(v4c[i] - sum(methods.map((m) => Number(ps.find((r) => r.method === m && Number(r.spec) === i).cost_bn))) / methods.length)); });
    gate("set: the union reproduces per_spec.csv's methods' mean at every specification (1e-9)", methods.length === 2 && w < 1e-9, `max |diff| ${ex(w)}`);
  }
  // G3+ per member, convention (a).
  const gr = P.csvRows(`${GEN}/${X.S.results}`).filter((r) => r.convention === "a" && r.generation === "G3plus");
  const gEnd = { low: pkg.evaluateFull(X.G, specs[48]).cost_bn, high: pkg.evaluateFull(X.G, specs[11]).cost_bn };
  const g1End = { low: evaluateAt(pkg, X.G1, specAt(specs[48], RV4), RV4).cost_bn * NG, high: evaluateAt(pkg, X.G1, specAt(specs[11], RV4), RV4).cost_bn * NG };
  const okG = ENDS.every((e) => {
    const row = gr.find((r) => r.band_end === e);
    return Math.abs(gEnd[e] - Number(row.cost_bn)) < 5e-7 && Math.abs(g1End[e] - gEnd[e]) < 1e-9
      && Math.abs(gEnd[e] * 1e9 / Number(row.population) - Number(row.per_member_usd)) < 5e-6 && Math.abs(Number(row.population) - NG) < 1e-6;
  });
  gate(`${name}: the corrected G3+ model reproduces ${X.S.results} (a) G3plus cost and per member, and one member scaled back gives it (1e-9)`, okG,
    ENDS.map((e) => `${gEnd[e].toFixed(6)}bn, $${(gEnd[e] * 1e9 / NG).toFixed(2)}`).join(" / "));

  // Whites in the engine: at the case's responses their lines cost what the white lane's run29 gives (its net budget);
  // the capital return follows the case's component rules on their amounts, where the lane used simplified keys.
  const whiteRecon = {};
  let worstW = 0;
  for (const [ages, model] of [[WHITE_AGES, X.W1], ["own", X.W1own]]) {
    whiteRecon[ages] = {};
    for (const [end, i] of [["low", 48], ["high", 11]]) {
      const r = evaluateAt(pkg, model, specAt(specs[i], RV4), RV4);
      const lane = WL[ages][X.S.white][end];
      worstW = Math.max(worstW, Math.abs((r.cost_bn - r.capital.total_bn) * lane.population - lane.net_budget_bn));
      whiteRecon[ages][end] = { lines_usd: (r.cost_bn - r.capital.total_bn) * 1e9, capital_case_rules_usd: r.capital.total_bn * 1e9,
        capital_lane_keys_usd: lane.capital_lane_keys_bn * 1e9 / lane.population, cost_case_rules_usd: r.cost_bn * 1e9,
        cost_lane_usd: lane.cost_bn * 1e9 / lane.population };
    }
  }
  gate(`${name}: whites' lines in the engine at the case's responses give the white lane's net budget at both ends and both age structures (1e-9 bn)`,
    worstW < 1e-9, `max |diff| ${ex(worstW)} bn`);

  // The generations at v4: they add to the union at every specification and give generation_results' costs.
  const gen4 = generationCosts(X, RV4, specs);
  const worstG4 = Math.max(...specs.map((_, i) => Math.abs(sum(GENS.map((g) => gen4[g][i])) - v4c[i])));
  const genRows = P.csvRows(`${GEN}/${X.S.results}`).filter((r) => r.convention === "a");
  const worstGR = Math.max(...genRows.map((r) => Math.abs(gen4[r.generation][r.band_end === "low" ? 48 : 11] - Number(r.cost_bn))));
  gate(`${name}: the three generation models add to v4 at all 64 specifications (1e-9) and give ${X.S.results}'s convention (a) costs (5e-7)`,
    worstG4 < 1e-9 && worstGR < 5e-7 && genRows.length === 6, `${ex(worstG4)} / ${ex(worstGR)}`);
  results[name] = { v4: { gen: gen4, cost: v4c } };
  summaries[name] = { v4: { band_bn: [v4c[48], v4c[11]], ends: [lo4, hi4] }, g3_member_usd: ENDS.map((e) => gEnd[e] * 1e9 / NG),
    white_reconciliation_per_person_at_v4: whiteRecon, arms: {} };
  for (const arm of ARMS) {
    const A = POP.arms[arm];
    const R = responsesAt(A.s, A.k_metro);
    const mG = A.later + (1 - C3) * A.g3_rate, mW = C3 * A.g3_rate;
    const sp = specs.map((s) => specAt(s, R));
    const add = augmented(X, mG, mW, R);
    const M = Engine.applyCorrections(U, add);
    const full = sp.map((s) => evaluateAt(pkg, M, s, R));
    const cost = full.map((r) => r.cost_bn);
    const lo = cost.indexOf(Math.min(...cost)), hi = cost.indexOf(Math.max(...cost));
    // Parts: the union at the new responses (with row 8), mG G3+ members, mW whites.
    const U8 = withRow8(X, R);
    const pu = sp.map((s) => evaluateAt(pkg, U8, s, R));
    const pg = sp.map((s) => evaluateAt(pkg, X.G1, s, R));
    const pw = sp.map((s) => evaluateAt(pkg, X.W1, s, R));
    const pwo = sp.map((s) => evaluateAt(pkg, X.W1own, s, R));
    const worstParts = Math.max(...sp.map((_, i) => Math.abs(pu[i].cost_bn + mG * pg[i].cost_bn + mW * pw[i].cost_bn - cost[i])));
    gate(`${name} ${arm}: the augmented model is the union at the new responses + m_G G3+ members + m_W whites at all 64 specifications (1e-9)`,
      worstParts < 1e-9, `max |diff| ${ex(worstParts)}`);
    const gen = generationCosts(X, R, sp);
    const worstGen = Math.max(...sp.map((_, i) => Math.abs(sum(GENS.map((g) => gen[g][i])) - pu[i].cost_bn)));
    gate(`${name} ${arm}: the generation models at the new responses add to the union at all 64 specifications (1e-9)`,
      worstGen < 1e-9, ex(worstGen));
    // Line by line at the ends.
    const lines = {};
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      const v4r = lineRows(v4[i]), ur = lineRows(pu[i]), gr1 = lineRows(pg[i]), wr = lineRows(pw[i]), ar = lineRows(full[i]);
      const keys = [...ar.keys()];
      const rows = keys.map((k) => ({ item: k, v4_bn: v4r.get(k) || 0, union_response_move_bn: (ur.get(k) || 0) - (v4r.get(k) || 0),
        g3_part_bn: mG * (gr1.get(k) || 0), white_part_bn: mW * (wr.get(k) || 0), v5_bn: ar.get(k) }));
      const w1 = Math.max(...rows.map((r) => Math.abs(r.v4_bn + r.union_response_move_bn + r.g3_part_bn + r.white_part_bn - r.v5_bn)));
      const w2 = Math.abs(costFromLines(ar) - cost[i]) + Math.abs(costFromLines(v4r) - v4c[i]);
      gate(`${name} ${arm} ${end}: each line's v4 + response move + G3+ part + white part is its v5 amount, and the lines add to the costs (1e-9)`,
        w1 < 1e-9 && w2 < 1e-9 && keys.length === v4r.size, `lines ${ex(w1)}, totals ${ex(w2)}`);
      lines[end] = rows;
    }
    results[name][arm] = { R, mG, mW, cost, lo, hi, add, pu, pg, pw, pwo, full, lines, sp, gen };
    // Linear in C3 at the arm's responses: v5(C3) = intercept + slope x C3 (C3 0: attriters cost what G3+ members cost).
    const c3Line = [lo, hi].map((i) => {
      const at0 = pu[i].cost_bn + (A.later + A.g3_rate) * pg[i].cost_bn;
      return { intercept_bn: at0, slope_bn: A.g3_rate * (pw[i].cost_bn - pg[i].cost_bn) };
    });
    // The fallback route the brief names: v4 plus the added people priced per line at v4's responses (no group-size
    // response move). The gap is what evaluating the augmented group adds.
    const postEngine = ENDS.map((e, j) => v4c[[48, 11][j]] + mG * g1End[e] / NG + mW * whiteRecon[WHITE_AGES][e].cost_case_rules_usd / 1e9);
    summaries[name].arms[arm] = {
      added: A.added, g3_rate: A.g3_rate, later: A.later, m_g3plus: mG, m_white: mW, population: A.population,
      band_bn: [cost[lo], cost[hi]], ends: [lo, hi], per_member_usd: [cost[lo] * 1e9 / A.population, cost[hi] * 1e9 / A.population],
      change_from_v4_bn: [cost[lo] - v4c[48], cost[hi] - v4c[11]],
      of_which_union_response_move_bn: [pu[lo].cost_bn - v4c[lo], pu[hi].cost_bn - v4c[hi]],
      of_which_g3plus_part_bn: [mG * pg[lo].cost_bn, mG * pg[hi].cost_bn],
      of_which_white_part_bn: [mW * pw[lo].cost_bn, mW * pw[hi].cost_bn],
      added_per_person_usd: [(cost[lo] - pu[lo].cost_bn) * 1e9 / A.added, (cost[hi] - pu[hi].cost_bn) * 1e9 / A.added],
      g3plus_member_usd: [pg[lo].cost_bn * 1e9, pg[hi].cost_bn * 1e9], white_person_usd: [pw[lo].cost_bn * 1e9, pw[hi].cost_bn * 1e9],
      white_person_own_ages_usd: [pwo[lo].cost_bn * 1e9, pwo[hi].cost_bn * 1e9],
      g3_rate_attriter_usd: [(1 - C3) * pg[lo].cost_bn * 1e9 + C3 * pw[lo].cost_bn * 1e9, (1 - C3) * pg[hi].cost_bn * 1e9 + C3 * pw[hi].cost_bn * 1e9],
      c3_line: { rule: "v5 = intercept_bn + slope_bn x C3 at the arm's responses and ends (C3 does not move s)", low: c3Line[0], high: c3Line[1] },
      route: { rule: "post_engine_bn: v4 + m_G G3+ members + m_W whites per line at v4's responses; gap_bn = this lane's band - post_engine_bn",
        post_engine_bn: postEngine, gap_bn: [cost[lo] - postEngine[0], cost[hi] - postEngine[1]] },
      responses: { s: R.s, k_metro: R.k_metro, general_government: R.gg, row8_factor: R.row8, owner_property: R.owner, tenant_property: R.tenant,
        economic_affairs_services: R.lines.economic_affairs_services, recreation_culture: R.lines.recreation_culture,
        sl_highways: R.sf.sl_highways, sl_recreation_and_culture: R.sf.sl_recreation_and_culture },
      row8_edit_bn: add.row8_edit_bn,
    };
    const wl = Math.max(...[0, 1].map((j) => Math.abs(c3Line[j].intercept_bn + c3Line[j].slope_bn * C3 - cost[[lo, hi][j]])));
    gate(`${name} ${arm}: the C3 line at the central C3 is the band (1e-9)`, wl < 1e-9, ex(wl));
  }
}
stop();

// ---------------------------------------------------------------------------------------------------
// Sensitivities: linear recombinations of the parts at each arm's responses (the ends held at the arm's own).
function recombine(name, arm, mG, mW, prodOff, ownAges) {
  const r = results[name][arm];
  const pw = ownAges ? r.pwo : r.pw;
  return [r.lo, r.hi].map((i) => r.pu[i].cost_bn + mG * r.pg[i].cost_bn + mW * pw[i].cost_bn
    + (prodOff ? prodOff * lineRows(r.pg[i]).get("production|gain") : 0));
}
const sensRows = [];
for (const name of Object.keys(SETS)) {
  for (const arm of ARMS) {
    const A = POP.arms[arm], r = results[name][arm];
    const central = recombine(name, arm, r.mG, r.mW, 0);
    const w = Math.max(Math.abs(central[0] - r.cost[r.lo]), Math.abs(central[1] - r.cost[r.hi]));
    gate(`${name} ${arm}: the recombination at the central reproduces the augmented band (1e-9)`, w < 1e-9, ex(w));
    const variants = [["central", r.mG, r.mW, 0, `C3 ${C3} (${POP.c3.label}); the measured generation split`]];
    for (const [label, e] of Object.entries(POP.c3.every_entry)) {
      if (e.c3 === C3 && label === POP.c3.label) continue;
      variants.push([`c3_${label}`, A.later + (1 - e.c3) * A.g3_rate, e.c3 * A.g3_rate, 0, `C3 ${e.c3} (${label})`]);
    }
    variants.push(["c3_zero", A.later + A.g3_rate, 0, 0, "C3 0: every added person costs what an identified G3+ member costs"]);
    variants.push(["c3_one", A.later, A.g3_rate, 0, "C3 1: G3-rate attriters cost what third-plus whites cost"]);
    variants.push(["attriters_keep_production", r.mG, r.mW, r.mW, "G3-rate attriters keep the whole G3+ production term (whites carry none)"]);
    variants.push(["white_own_ages", r.mG, r.mW, 0, "the white end at whites' own ages (the white lane's A1, ladder 263's central) instead of "
      + "at the identified G3+'s ages", true]);
    const fw = POP.fractional_ancestry.hidden_third_generation;
    variants.push(["fractional_ancestry", fw * r.mG, fw * r.mW, 0,
      `added persons counted at ${fw.toFixed(4)} each (a quarter per Mexico-born grandparent, the hidden third generation's cells; responses at the whole-person share)`]);
    for (const [variant, mG, mW, prodOff, rule, ownAges] of variants) {
      const b = recombine(name, arm, mG, mW, prodOff, ownAges);
      const pop = variant === "fractional_ancestry" ? POP.meta.account_union + fw * A.added : A.population;
      sensRows.push({ set: name, arm, variant, low_bn: b[0], high_bn: b[1], change_low_bn: b[0] - summaries[name].v4.band_bn[0],
        change_high_bn: b[1] - summaries[name].v4.band_bn[1], population: pop, per_member_low_usd: b[0] * 1e9 / pop,
        per_member_high_usd: b[1] * 1e9 / pop, m_g3plus: mG, m_white: mW, rule });
    }
  }
}

// [FRAMING-SENSITIVE] Replacement: the band net of r x W x added persons, W the C3 blend's third-plus white per person
// at the arm's responses, at every specification (the band is the minimum and maximum over the 64).
const replacementRows = [];
for (const name of Object.keys(SETS)) for (const arm of ARMS) {
  const A = POP.arms[arm], r = results[name][arm], v4b = summaries[name].v4.band_bn;
  for (const rr of [1, 0.5]) {
    const net = r.sp.map((_, i) => r.cost[i] - rr * A.added * r.pw[i].cost_bn);
    const lo = net.indexOf(Math.min(...net)), hi = net.indexOf(Math.max(...net));
    const w = [r.pw[lo].cost_bn * 1e9, r.pw[hi].cost_bn * 1e9];
    const row = { set: name, arm, variant: `replacement_r${rr}`, low_bn: net[lo], high_bn: net[hi], change_low_bn: net[lo] - v4b[0],
      change_high_bn: net[hi] - v4b[1], population: A.population, per_member_low_usd: net[lo] * 1e9 / A.population,
      per_member_high_usd: net[hi] * 1e9 / A.population, m_g3plus: r.mG, m_white: r.mW,
      rule: `[FRAMING-SENSITIVE] net of ${rr} x W x ${(A.added / 1e6).toFixed(4)}M added persons; W $${w.map((x) => Math.round(x)).join(" / ")} per person `
        + `(third-plus non-Hispanic whites at the identified G3+'s ages, the C3 blend's W); specifications ${lo} / ${hi}` };
    sensRows.push(row);
    replacementRows.push({ set: name, arm, r: rr, ends: [lo, hi], w_per_person_usd: w,
      deduction_bn: [rr * A.added * r.pw[lo].cost_bn, rr * A.added * r.pw[hi].cost_bn], band_bn: [net[lo], net[hi]],
      lineage_line_net_bn: [net[lo] - v4b[0], net[hi] - v4b[1]], per_member_usd: [row.per_member_low_usd, row.per_member_high_usd] });
  }
}

// [FRAMING-SENSITIVE] Fractional, the people-conserving lineage count: every generation at its ancestry share
// (fractional.py), the added persons at theirs, each priced at its generation's cost at the arm's responses.
const FR_SCEN = [
  ["central", { G2: SH.G2.central, G3plus: SH.G3plus.central },
    "G2 measured, unknown other parents at the co-resident mean; G3+ at the identified third-generation children's mix (population lane convention)"],
  ["g2_low", { G2: SH.G2.low, G3plus: SH.G3plus.central }, "G2's unknown ancestors at nothing"],
  ["g2_high", { G2: SH.G2.high, G3plus: SH.G3plus.central }, "G2's unknown ancestors at their full weight"],
  ["g3plus_seen_low", { G2: SH.G2.central, G3plus: SH.G3plus.seen_low },
    "G3+ at the strict quarter-per-grandparent mix of members whose grandparents are seen, applied to all"],
  ["g3plus_seen_high", { G2: SH.G2.central, G3plus: SH.G3plus.seen_high },
    "G3+ at the high bound of members whose grandparents are seen, applied to all"],
  ["bound_low", { G2: SH.G2.low, G3plus: SH.G3plus.low }, "every unknown ancestor at nothing"],
  ["bound_high", { G2: SH.G2.high, G3plus: SH.G3plus.high }, "every unknown ancestor at its full weight"],
];
const fracRows = [];
let fracWhole = 0, fracAttr = 0;
for (const name of Object.keys(SETS)) for (const arm of ["v4", ...ARMS]) {
  const r = results[name][arm];
  const added = arm === "v4" ? 0 : POP.arms[arm].added;
  const addedCost = arm === "v4" ? r.cost.map(() => 0) : r.cost.map((c, i) => c - r.pu[i].cost_bn);
  const count = (sh, sAdded) => r.cost.map((_, i) => r.gen.G1[i] + sh.G2 * r.gen.G2[i] + sh.G3plus * r.gen.G3plus[i] + sAdded * addedCost[i]);
  const whole = count({ G2: 1, G3plus: 1 }, 1);
  fracWhole = Math.max(fracWhole, ...whole.map((x, i) => Math.abs(x - r.cost[i])));
  if (arm !== "v4") {
    const fw = POP.fractional_ancestry.hidden_third_generation;
    const att = count({ G2: 1, G3plus: 1 }, fw);
    const s = sensRows.find((x) => x.set === name && x.arm === arm && x.variant === "fractional_ancestry");
    fracAttr = Math.max(fracAttr, Math.abs(att[r.lo] - s.low_bn), Math.abs(att[r.hi] - s.high_bn));
  }
  for (const [scenario, sh, rule] of FR_SCEN) {
    const f = count(sh, SH.added.central);
    const lo = f.indexOf(Math.min(...f)), hi = f.indexOf(Math.max(...f));
    const pop = SH.G1.population + sh.G2 * SH.G2.population + sh.G3plus * SH.G3plus.population + SH.added.central * added;
    fracRows.push({ set: name, arm, scenario, s_g2: sh.G2, s_g3plus: sh.G3plus, s_added: arm === "v4" ? 0 : SH.added.central,
      fractional_population: pop, low_bn: f[lo], high_bn: f[hi], spec_low: lo, spec_high: hi,
      per_member_low_usd: f[lo] * 1e9 / pop, per_member_high_usd: f[hi] * 1e9 / pop,
      whole_person_low_bn: Math.min(...r.cost), whole_person_high_bn: Math.max(...r.cost),
      g1_bn_at_ends: `${r.gen.G1[lo].toFixed(4)} / ${r.gen.G1[hi].toFixed(4)}`, g2_bn_at_ends: `${r.gen.G2[lo].toFixed(4)} / ${r.gen.G2[hi].toFixed(4)}`,
      g3plus_bn_at_ends: `${r.gen.G3plus[lo].toFixed(4)} / ${r.gen.G3plus[hi].toFixed(4)}`,
      added_bn_at_ends: `${addedCost[lo].toFixed(4)} / ${addedCost[hi].toFixed(4)}`, rule: `[FRAMING-SENSITIVE] ${rule}` });
  }
}
gate("fractional count, positive control: every share at 1 gives the whole-person cost at every specification, v4 and every arm (1e-9)",
  fracWhole < 1e-9, ex(fracWhole));
gate("fractional count at whole union members and the added persons' mix reproduces the attriter-only fractional_ancestry row (1e-9)",
  fracAttr < 1e-9, ex(fracAttr));

// The C3 recombinations hold each arm's ends; confirm the ends do not move under the extremes.
for (const name of Object.keys(SETS)) for (const arm of ARMS) {
  const r = results[name][arm], A = POP.arms[arm];
  for (const [mG, mW, pw] of [[A.later + A.g3_rate, 0, r.pw], [A.later, A.g3_rate, r.pw], [r.mG, r.mW, r.pwo], [A.later, A.g3_rate, r.pwo]]) {
    const c = r.sp.map((_, i) => r.pu[i].cost_bn + mG * r.pg[i].cost_bn + mW * pw[i].cost_bn);
    const ok = c.indexOf(Math.min(...c)) === r.lo && c.indexOf(Math.max(...c)) === r.hi;
    gate(`${name} ${arm}: the band's ends stay at specifications ${r.lo} / ${r.hi} with C3 at 0 and at 1 and with whites at their own ages`, ok);
  }
}
for (const name of Object.keys(SETS)) for (const arm of ARMS) {
  const r = results[name][arm];
  gate(`${name} ${arm}: the v5 band's ends are v4's, specifications 48 / 11`, r.lo === 48 && r.hi === 11, `${r.lo} / ${r.hi}`);
}

// ---------------------------------------------------------------------------------------------------
// The payload addition (central arm), and a consumer's evaluation from the payload alone.
function payloadFor(name, arm) {
  const X = SETS[name], r = results[name][arm], A = POP.arms[arm];
  const base = readJson(X.payloadRel).meta;
  const responses = clone(base.responses);
  const R = r.R;
  responses.general_government.low = R.gg.low; responses.general_government.high = R.gg.high; responses.general_government.s = R.s;
  responses.row8_factor = R.row8;
  for (const line of LR_LINES) {
    responses[line].low = R.lines[line].low; responses[line].high = R.lines[line].high;
    for (const x of responses[line].subfunctions) { x.low = R.sf[x.id].low; x.high = R.sf[x.id].high; }
  }
  responses.roads_vmt_sl.low = R.sf.sl_highways.low; responses.roads_vmt_sl.high = R.sf.sl_highways.high;
  responses.roads_vmt_fed.low = R.sf.fed_highways.low; responses.roads_vmt_fed.high = R.sf.fed_highways.high;
  responses.state_price_recreation_culture.low = R.lines.recreation_culture.low; responses.state_price_recreation_culture.high = R.lines.recreation_culture.high;
  for (const [id, v] of [["modeled_owner_property", R.owner], ["tenant_occupied_property", R.tenant]]) { responses[id].low = v; responses[id].high = v; }
  const capital = clone(base.capital_return);
  for (const c of capital.components) if (c.response.kind === "long_run_subfunction") c.response.values = clone(R.sf[c.response.subfunction]);
  return {
    meta: {
      source: `${LANE}/lineage_case.cjs`,
      status: POP.c3.override ? STATUS : "candidate v5, not adopted: the v4 case plus the lineage line",
      builds_on: X.payloadRel,
      apply: "Engine.applyCorrections(Engine.applyCorrections(MODEL, builds_on payload), this payload); evaluate with this meta's "
        + "responses in place of the v4 payload's (specification gg and line_responses at each reading) and capital_return "
        + "(components of kind long_run_subfunction take response.values[reading]); lineage_case.cjs specAt() and capitalAt() do this",
      case: `v4 (${X.payloadRel}) plus ${(A.added / 1e6).toFixed(4)}M lineage persons (arm ${arm}): ${(A.later / 1e6).toFixed(4)}M later losses as `
        + `identified G3+ members and ${(A.g3_rate / 1e6).toFixed(4)}M G3-rate attriters at (1 - C3) G3+ + C3 whites, C3 ${C3}`,
      lineage: { arm, source_arm: A.source_arm, rho: A.rho, added: A.added, g3_rate: A.g3_rate, later: A.later, population: A.population,
        c3: POP.c3, m_g3plus: r.mG, m_white: r.mW, frame_factor: POP.meta.frame_factor, s: R.s, k_metro: R.k_metro,
        row8_edit_bn: r.add.row8_edit_bn, g3plus_model: `${GEN}/model_G3plus.json + ${X.gen} payloads.a.G3plus`,
        white: `${LANE}/derived/white_lines.json (${WHITE_AGES}, ${X.white})`,
        responses_changed: ["general_government", "row8_factor", ...LR_LINES, "roads_vmt_sl", "roads_vmt_fed", "state_price_recreation_culture",
          "modeled_owner_property", "tenant_occupied_property", "capital_return long_run_subfunction values"] },
      responses, capital_return: capital,
    },
    edits: r.add.edits,
    production: r.add.production,
  };
}
// A consumer: the payload's meta only (no R object from this script).
function consumerBand(name, payload) {
  const X = SETS[name];
  const m = Engine.applyCorrections(Engine.applyCorrections(MODEL, readJson(X.payloadRel)), payload);
  const resp = payload.meta.responses;
  const values = Object.fromEntries(payload.meta.capital_return.components.filter((c) => c.response.kind === "long_run_subfunction")
    .map((c) => [c.response.subfunction, c.response.values]));
  const R = { sf: Object.fromEntries(SUBS.map((x) => [x.id, values[x.id] || { low: NaN, high: NaN }])) };
  const lineValue = (k, rd) => {
    const id = k.startsWith("receipt:") ? k.slice(8) : k;
    return resp[id][rd];
  };
  const costs = X.pkg.MAIN_SPECS.map((s) => {
    const lr = Object.fromEntries(Object.keys(s.line_responses).map((k) => [k, lineValue(k, s.reading)]));
    const spec = Object.assign({}, s, { gg: resp.general_government[s.reading], line_responses: lr });
    return evaluateAt(X.pkg, m, spec, R).cost_bn;
  });
  return [Math.min(...costs), Math.max(...costs)];
}
const payloads = { set: payloadFor("set", CENTRAL), cash: payloadFor("cash", CENTRAL) };
for (const name of Object.keys(payloads)) {
  const b = consumerBand(name, JSON.parse(JSON.stringify(payloads[name])));
  const r = results[name][CENTRAL];
  gate(`${name}: a consumer applying the payload addition to the v4 payload model with its meta gets the v5 band (1e-9)`,
    Math.abs(b[0] - r.cost[r.lo]) < 1e-9 && Math.abs(b[1] - r.cost[r.hi]) < 1e-9, `${b[0].toFixed(4)} / ${b[1].toFixed(4)}`);
}

// ---------------------------------------------------------------------------------------------------
// Line table and the printed table (controlled rounding: parts add to the printed totals).
const GROUP_OF = (item) => {
  if (item.startsWith("capital|")) return "capital return";
  if (item === "production|gain") return "production gain";
  return item.startsWith("receipt|") ? "receipts" : "spending";
};
const lineCsv = [];
for (const name of Object.keys(SETS)) for (const arm of ARMS) for (const end of ENDS) {
  for (const row of results[name][arm].lines[end]) {
    lineCsv.push({ set: name, arm, end, spec: end === "low" ? results[name][arm].lo : results[name][arm].hi, item: row.item, group: GROUP_OF(row.item),
      v4_bn: row.v4_bn, union_response_move_bn: row.union_response_move_bn, g3plus_part_bn: row.g3_part_bn, white_part_bn: row.white_part_bn,
      lineage_bn: row.union_response_move_bn + row.g3_part_bn + row.white_part_bn, v5_bn: row.v5_bn });
  }
}
// Controlled rounding (largest remainder) of values to `d` decimals so that they add to the rounded total.
function controlled(values, total, d) {
  const f = Math.pow(10, d);
  const target = Math.round(total * f);
  const floors = values.map((v) => Math.floor(v * f));
  let short = target - sum(floors);
  const order = values.map((v, i) => [v * f - floors[i], i]).sort((a, b) => b[0] - a[0] || a[1] - b[1]);
  const out = floors.slice();
  if (short < 0 || short > values.length) throw new Error("[BLOCKED] controlled rounding cannot reach the total");
  for (let j = 0; j < short; j++) out[order[j][1]] += 1;
  return out.map((x) => x / f);
}
const printed = [];
let printFails = 0, totalFails = 0;
for (const name of Object.keys(SETS)) for (const arm of ARMS) for (const end of ENDS) {
  const rows = lineCsv.filter((r) => r.set === name && r.arm === arm && r.end === end);
  const groups = [...new Set(rows.map((r) => r.group))];
  const parts = groups.flatMap((g) => [["union response move", "union_response_move_bn"], ["G3+ members", "g3plus_part_bn"], ["whites", "white_part_bn"]]
    .map(([who, k]) => [`${g}: ${who}`, sum(rows.filter((r) => r.group === g).map((r) => r[k]))]));
  const total = sum(rows.map((r) => r.lineage_bn));
  const r = results[name][arm];
  const want = end === "low" ? r.cost[r.lo] - summaries[name].v4.band_bn[0] : r.cost[r.hi] - summaries[name].v4.band_bn[1];
  if (Math.abs(total - want) > 1e-9) totalFails += 1;
  const rounded = controlled(parts.map((p) => p[1]), total, 1);
  parts.forEach(([part, v], j) => printed.push({ set: name, arm, end, part, lineage_bn: v, printed_bn: rounded[j] }));
  printed.push({ set: name, arm, end, part: "total", lineage_bn: total, printed_bn: Math.round(total * 10) / 10 });
  if (Math.abs(sum(rounded) - Math.round(total * 10) / 10) > 1e-9) printFails += 1;
}
gate("every lineage table's lines add to the band's change from v4 (1e-9)", totalFails === 0, `${totalFails} failures`);
gate("every printed lineage table's parts add to its printed total (one decimal, controlled rounding)", printFails === 0, `${printed.length} rows`);
stop();

// ---------------------------------------------------------------------------------------------------
// Writes.
fs.mkdirSync(OUT, { recursive: true });
const csv = (rows) => {
  const head = Object.keys(rows[0]);
  const cell = (v) => (typeof v === "number" ? v.toFixed(6) : /[",]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v));
  return [head.join(","), ...rows.map((r) => head.map((k) => cell(r[k])).join(","))].join("\n") + "\n";
};
const bandRows = [];
for (const name of Object.keys(SETS)) {
  const v4b = summaries[name].v4.band_bn;
  bandRows.push({ set: name, arm: "v4", variant: "adopted v4", low_bn: v4b[0], high_bn: v4b[1], change_low_bn: 0, change_high_bn: 0,
    population: POP.meta.account_union, per_member_low_usd: v4b[0] * 1e9 / POP.meta.account_union, per_member_high_usd: v4b[1] * 1e9 / POP.meta.account_union,
    m_g3plus: 0, m_white: 0, rule: "main_case_2026_09_29 (the union only)" });
  for (const r of sensRows.filter((x) => x.set === name)) bandRows.push(r);
}
fs.writeFileSync(path.join(OUT, "v5_bands.csv"), csv(bandRows));
fs.writeFileSync(path.join(OUT, "lineage_lines.csv"), csv(lineCsv));
fs.writeFileSync(path.join(OUT, "lineage_lines_printed.csv"), csv(printed));
fs.writeFileSync(path.join(OUT, "lineage_payload.json"), JSON.stringify(payloads.set, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "lineage_payload_cash.json"), JSON.stringify(payloads.cash, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "fractional_lineage.csv"), csv(fracRows));
const prior = ["gates_population.json", "gates_white.json", "gates_fractional.json"].flatMap((f) => readJson(`${LANE}/derived/${f}`).gates.map((g) => Object.assign({ step: f.replace(/^gates_|\.json$/g, "") }, g)));
fs.writeFileSync(path.join(OUT, "gates.json"), JSON.stringify({ passed: prior.concat(GATES).every((g) => g.passed),
  count: prior.length + GATES.length, gates: prior.concat(GATES.map((g) => Object.assign({ step: "engine" }, g))) }, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "v5_summary.json"), JSON.stringify({
  meta: { source: `${LANE}/lineage_case.cjs`, status: STATUS, central_arm: CENTRAL, c3: POP.c3, profile: PROFILE,
    population: POP.meta, fractional_ancestry: POP.fractional_ancestry, fractional_shares: SH,
    note: "low / high are the band's ends, specifications 48 (shared allocation) / 11 (personal); every arm's ends are v4's (gate)" },
  sets: summaries,
  replacement: { rule: "[FRAMING-SENSITIVE] the band net of r x W x added persons (a native parent's replacement child); W the C3 blend's "
    + "third-plus non-Hispanic white per person at the arm's responses; band = min / max over the 64 specifications", rows: replacementRows },
  fractional: { rule: "[FRAMING-SENSITIVE] the people-conserving lineage count (lineage_cost_2026_09_19 per_capita, TFR/2): each "
    + "generation at its share of Mexican-immigrant ancestry, priced at that generation's cost at the arm's responses; band = min / max "
    + "over the 64 specifications; derived/fractional_lineage.csv", rows: fracRows } }, null, 1) + "\n");

console.log("[results] $bn a year at specifications 48 / 11; per member on the lineage population");
for (const name of Object.keys(SETS)) {
  const s = summaries[name];
  console.log(`  ${name}: v4 ${s.v4.band_bn.map((x) => x.toFixed(4)).join(" / ")}; G3+ member $${s.g3_member_usd.map((x) => x.toFixed(2)).join(" / ")}`);
  for (const arm of ARMS) {
    const a = s.arms[arm];
    console.log(`    ${arm}: +${(a.added / 1e6).toFixed(3)}M -> ${a.band_bn.map((x) => x.toFixed(4)).join(" / ")} (change ${a.change_from_v4_bn.map((x) => "+" + x.toFixed(3)).join(" / ")}; `
      + `responses ${a.of_which_union_response_move_bn.map((x) => x.toFixed(3)).join(" / ")}, G3+ ${a.of_which_g3plus_part_bn.map((x) => x.toFixed(3)).join(" / ")}, `
      + `white ${a.of_which_white_part_bn.map((x) => x.toFixed(3)).join(" / ")}); $${a.per_member_usd.map((x) => Math.round(x)).join(" / ")} per member`);
  }
}
console.log(`  ✓ all ${GATES.length} engine gates passed`);
module.exports = { specAt, capitalAt, evaluateAt, responsesAt, payloadFor };
