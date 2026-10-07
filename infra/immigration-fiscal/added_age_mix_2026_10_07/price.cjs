/* Main case v5's lineage line with the added people at a measured age mix (added_age_mix_2026_10_07).
 *
 * v5 (main_case_lineage_2026_10_05, arm b) prices the 3.04M added persons at the identified third-plus's age mix:
 * m_G = later + (1 - C3) g3 identified G3+ members and m_W = C3 g3 third-plus whites (W) at the G3+'s ages. Here the
 * two parts take their own mixes (age_mix.py): the G3-rate persons (g3) theirs, the later losses theirs, and the white
 * end of the G3-rate blend sits at the G3-rate persons' mix, as v5 puts it at theirs. Per mix:
 *   G3+ member  central route "keys": the lineage lane's G1 (the corrected G3+ model per member) with each cell times
 *               f = sum_b (pi'_b / pi_b) T_b / sum_b T_b, T the engine's own key for that cell and allocation by age band
 *               (g3_age_keys.py). On the set the pension rule's three lines take the profile of what the rule puts in
 *               them (OASDI receipts for Social Security; HI receipts for Medicare's Part A accrual; benefits for the
 *               tax on benefits). The production grid follows the wage key. Cross-check route "rough": every cell of a
 *               line times the white lane's rough re-key factor for the line (band_lines.py);
 *   W           white_lines.py's per-person line amounts at the mix, in every cell of the line (band_lines.py).
 * The case at arm b's responses is linear in the parts (the lineage lane's gate), so
 *   v5' = union at the new responses + later x G(mix_later) + (1 - C3) g3 x G(mix_g3) + C3 g3 x W(mix_g3).
 * Counts, C3 and the responses are v5's: only the ages move.
 *
 * Lines 65-380 of main_case_lineage_2026_10_05/lineage_case.cjs (commit d3b7e6e6) are copied below verbatim, from
 * "use strict" to costFromLines: inputs, the group-size responses and their gates, evaluateAt, the part models and
 * setUp(). One line differs: LANE names the lineage lane, whose derived/ inputs are read, never written (OUT, the same
 * text, is this lane's derived/). Its gates run as in the lineage lane.
 *
 * Gates (derived/gates_price.json; a failed gate writes nothing else):
 *   - the copied setup's gates (the v4 reproduction at zero added persons, the G3+ model against generation_results,
 *     whites against the white lane, the responses at the v4 share);
 *   - positive control: at the identified mix (every factor 1, W from band_lines.json) the route gives v5's band
 *     (v5_summary.json arm b, 390.29 / 461.24 on the set) and its parts (+18.88 / +26.40, G3+ and white parts) to 1e-6,
 *     on both sets, and the identified mix's W per person equals the lineage lane's W1 in every cell (exact);
 *   - the end specifications of every reading are reported; the band is quoted at 48 / 11 (v5's ends) and beside at
 *     each reading's own minimum and maximum.
 * Writes derived/price_bands.csv, derived/price_summary.json (per-mix per-person costs at the ends, the unit bands for
 * summarize.py) and derived/gates_price.json. Run from the repository root after band_lines.py:
 *   node infra/immigration-fiscal/added_age_mix_2026_10_07/price.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.resolve(HERE, "..");
const LANE = "main_case_lineage_2026_10_05";   // the lineage lane: inputs read from its derived/, never written
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

// ===================================================================================================
// This lane: the added people at measured age mixes.
const BL = JSON.parse(fs.readFileSync(path.join(OUT, "band_lines.json"), "utf8"));
const MIX = JSON.parse(fs.readFileSync(path.join(OUT, "age_mix.json"), "utf8"));
const AK = JSON.parse(fs.readFileSync(path.join(OUT, "g3_age_keys.json"), "utf8"));
const V5 = readJson(`${LANE}/derived/v5_summary.json`);
const BASIS = { set: "accrual", cash: "cash" };
const A = POP.arms[CENTRAL];
const PI0 = MIX.meta.identified;
const READINGS = Object.keys(MIX.readings).filter((r) => r !== "flat");
const UNIT = Object.keys(BL.mixes).filter((m) => m.startsWith("band|"));
const ROUTES = ["keys", "rough"];
gate("age_mix.json is on arm b's split and C3 (exact)", MIX.meta.arm === CENTRAL && MIX.meta.g3_rate === A.g3_rate
  && MIX.meta.later === A.later && MIX.meta.c3 === C3, `${A.g3_rate.toFixed(1)} + ${A.later.toFixed(1)}, C3 ${C3}`);
gate("band_lines.json holds every reading's two mixes, the identified mix (age_mix.json's) and 17 unit bands",
  READINGS.every((r) => BL.mixes[`${r}|g3_rate`] && BL.mixes[`${r}|later`]) && UNIT.length === 17
  && JSON.stringify(BL.mixes.identified.pi) === JSON.stringify(PI0)
  && READINGS.every((r) => JSON.stringify(BL.mixes[`${r}|g3_rate`].pi) === JSON.stringify(MIX.readings[r].g3_rate)));
const lineKey = (c) => `${WSIDE[c.side]}|${c.line}`;
// The engine-key route: each G3+ cell moves by f = sum_b rho_b T_b / sum_b T_b, rho = pi' / pi (g3_age_keys.py).
function profileOf(c, a, cell) {
  if (c.side === "spending" && AK.line_keys[c.line]) return AK.line_keys[c.line][a];
  const key = c.side === "receipt" ? cell.key : c.key;
  const p = AK.keys[c.side][a][key];
  if (!p) throw new Error(`[BLOCKED] no age profile for ${c.side} ${c.line} key ${key}`);
  return p;
}
const ageFactor = (T, rho) => {
  const den = T.reduce((s, x) => s + x, 0);
  return den === 0 ? 1 : T.reduce((s, x, b) => s + rho[b] * x, 0) / den;
};
const ZERO_PROFILE = [];
// The set's pension rule (v4, meta.pension_accrual) rewrites three G3+ lines from the cash set's: Social Security is
// ratio_net x the group's OASDI receipts, Medicare swaps its Part A share for an accrual on HI receipts, and federal
// income tax loses the tax on benefits. Their cells take the age profile of what they now hold:
//   social_security   the OASDI receipts: employee + employer OASDI (wage_oasdi) + se_oasdi_share x self-employment;
//   medicare          (1 - part_a_share) x the cash cell on its key, the rest on the HI receipts (wage, the rest of SE);
//   federal_income_tax the cash cell on its key, the change on the social_security (benefits) key.
const PENSION = P.correctionsPayload().meta.pension_accrual;
const GCASH = Engine.applyCorrections(readJson(`${GEN}/model_G3plus.json`),
  readJson(`${GEN}/generation_corrections_sept29_cash.json`).payloads.a.G3plus);
const gcashCells = new Map(cellsOf(GCASH).map((c) => [cellId(c), c.cell]));
const prof = (T) => { const s = T.reduce((a, x) => a + x, 0); return T.map((x) => x / s); };
const comb = (parts) => parts[0][1].map((_, b) => parts.reduce((a, [amt, T]) => a + amt * prof(T)[b], 0));
function pensionProfile(X, c, a, cell) {
  const rc = (line) => X.gCells.get(`receipt|${line}|cbo_collective`)[a];
  const rp = (line) => AK.keys.receipt[a][rc(line).key];
  const se = rc("self_employment_oasdi_hi").target_bn;
  if (c.line === "social_security") {
    return comb([[rc("employee_oasdi").target_bn, rp("employee_oasdi")], [rc("employer_oasdi").target_bn, rp("employer_oasdi")],
      [PENSION.se_oasdi_share * se, rp("self_employment_oasdi_hi")]]);
  }
  const cash = gcashCells.get(cellId(c))[a].target_bn;
  if (c.line === "medicare") {
    const keep = (1 - PENSION.part_a_share) * cash;
    const hi = [[rc("employee_hi").target_bn, rp("employee_hi")], [rc("employer_hi").target_bn, rp("employer_hi")],
      [(1 - PENSION.se_oasdi_share) * se, rp("self_employment_oasdi_hi")]];
    const hiT = hi.reduce((s, [amt]) => s + amt, 0);
    return comb([[keep, AK.keys.spending[a][c.key]], ...hi.map(([amt, T]) => [(cell.target_bn - keep) * amt / hiT, T])]);
  }
  return comb([[cash, AK.keys.receipt[a][cell.key]], [cell.target_bn - cash, AK.keys.spending[a].social_security]]);
}
const PENSION_LINES = new Set(["social_security", "medicare", "federal_income_tax"]);
function g3ModelKeys(X, mix) {
  const rho = BL.mixes[mix].pi.map((p, b) => p / PI0[b]);
  const fp = ageFactor(AK.production, rho);
  return partModel(X.U, (c, a) => {
    const cell = X.gCells.get(cellId(c))[a];
    const T = X.name === "set" && PENSION_LINES.has(c.line) ? pensionProfile(X, c, a, cell) : profileOf(c, a, cell);
    if (T.every((x) => x === 0) && Math.abs(cell.target_bn) > 1e-9) ZERO_PROFILE.push(`${c.side} ${c.line} ${a}: ${cell.target_bn}`);
    return cell.target_bn / NG * ageFactor(T, rho);
  }, { private_wtp_bn: X.G.production.private_wtp_bn.map((x) => x / NG * fp),
    induced_receipts_bn: X.G.production.induced_receipts_bn.map((x) => x / NG * fp) });
}
// The rough-key route (cross-check): the white lane's rough re-key factors per line (band_lines.py), every cell alike.
function g3ModelRough(X, mix) {
  const g = BL.mixes[mix].g3x[BASIS[X.name]];
  const missing = cellsOf(X.U).filter((c) => !(lineKey(c) in g.factors));
  if (missing.length) throw new Error(`[BLOCKED] ${mix}: no factor for ${missing[0].line}`);
  const fp = g.production_factor;
  return partModel(X.U, (c, a) => X.gCells.get(cellId(c))[a].target_bn / NG * g.factors[lineKey(c)],
    { private_wtp_bn: X.G.production.private_wtp_bn.map((x) => x / NG * fp),
      induced_receipts_bn: X.G.production.induced_receipts_bn.map((x) => x / NG * fp) });
}
{
  const gs = Engine.applyCorrections(readJson(`${GEN}/model_G3plus.json`), readJson(`${GEN}/generation_corrections_sept29.json`).payloads.a.G3plus);
  const differ = [...new Set(cellsOf(gs).filter((c) => ALLOCS.some((a) => Math.abs(c.cell[a].target_bn
    - gcashCells.get(cellId(c))[a].target_bn) > 1e-12)).map((c) => c.line))].sort();
  gate("the set's and the cash set's G3+ models differ only in the pension rule's three lines", JSON.stringify(differ)
    === JSON.stringify([...PENSION_LINES].sort()), differ.join(", "));
  const pay = [...new Set(cellsOf(gs).filter((c) => c.side === "receipt" && /oasdi|_hi$/.test(c.line)).flatMap((c) =>
    ALLOCS.map((a) => `${c.line}|${a}|${c.cell[a].target_bn}`)))];
  gate("the payroll receipt cells are the same in every receipt scenario (the pension profile reads cbo_collective)",
    pay.length === 5 * ALLOCS.length, `${pay.length} distinct line x allocation amounts`);
}
const g3Model = (X, mix, route) => (route === "keys" ? g3ModelKeys : g3ModelRough)(X, mix);
function wModel(X, mix) {
  const w = BL.mixes[mix].white[BASIS[X.name]].lines;
  return partModel(X.U, (c) => w[lineKey(c)], zeroGrid(X.U));
}
const cellsEqual = (m1, m2) => {
  const a = cellsOf(m1), b = cellsOf(m2);
  return a.length === b.length && a.every((c, i) => cellId(c) === cellId(b[i])
    && ALLOCS.every((al) => c.cell[al].target_bn === b[i].cell[al].target_bn));
};

const priceOut = { meta: { source: "added_age_mix_2026_10_07/price.cjs", arm: CENTRAL, c3: C3, g3_rate: A.g3_rate, later: A.later,
  added: A.added, population: A.population, central_route: "keys",
  routes: { keys: "the engine's own G3+ keys by age band (g3_age_keys.py), cell by cell and allocation by allocation",
    rough: "the white lane's rough re-key factors per line (band_lines.py): cross-check" },
  rule: "v5' = union at arm b's responses + later x G(mix_later) + (1 - C3) g3 x G(mix_g3) + C3 g3 x W(mix_g3)" }, sets: {} };
const bandRows = [];
for (const name of Object.keys(SETS)) {
  const X = setUp(name);
  const { pkg, specs } = X;
  const R = responsesAt(A.s, A.k_metro);
  const sp = specs.map((s) => specAt(s, R));
  const ALL = specs.map((_, i) => i);
  const run = (model, idx) => idx.map((i) => evaluateAt(pkg, model, sp[i], R).cost_bn);
  const pu = run(withRow8(X, R), ALL);
  const MIXES = ["identified", ...READINGS.flatMap((r) => [`${r}|g3_rate`, `${r}|later`])];
  const G = Object.fromEntries(ROUTES.map((rt) => [rt, Object.fromEntries(MIXES.map((m) => [m, run(g3Model(X, m, rt), ALL)]))]));
  const W = Object.fromEntries(MIXES.map((m) => [m, run(wModel(X, m), ALL)]));
  gate(`${name}: the identified mix's G3+ member (both routes) and W are the lineage lane's G1 and W1, cell for cell (exact)`,
    ROUTES.every((rt) => cellsEqual(g3Model(X, "identified", rt), X.G1)
      && JSON.stringify(g3Model(X, "identified", rt).production) === JSON.stringify(X.G1.production))
    && cellsEqual(wModel(X, "identified"), X.W1));
  const v5 = V5.sets[name].arms[CENTRAL];
  const [lo, hi] = v5.ends;
  const caseAt = (rt, m3, mL) => ALL.map((i) => pu[i] + A.later * G[rt][mL][i] + (1 - C3) * A.g3_rate * G[rt][m3][i]
    + C3 * A.g3_rate * W[m3][i]);
  const flat = caseAt("keys", "identified", "identified");
  const gPart = [lo, hi].map((i) => (A.later + (1 - C3) * A.g3_rate) * G.keys.identified[i]);
  const wPart = [lo, hi].map((i) => C3 * A.g3_rate * W.identified[i]);
  const worst = Math.max(Math.abs(flat[lo] - v5.band_bn[0]), Math.abs(flat[hi] - v5.band_bn[1]),
    ...[0, 1].map((j) => Math.abs(gPart[j] - v5.of_which_g3plus_part_bn[j])), ...[0, 1].map((j) => Math.abs(wPart[j] - v5.of_which_white_part_bn[j])),
    ...[0, 1].map((j) => Math.abs(flat[[lo, hi][j]] - V5.sets[name].v4.band_bn[j] - v5.change_from_v4_bn[j])));
  gate(`${name}: at the identified mix the route gives v5's band, its change from v4 and its G3+ and white parts (1e-6)`, worst < 1e-6,
    `${flat[lo].toFixed(6)} / ${flat[hi].toFixed(6)} vs ${v5.band_bn.map((x) => x.toFixed(6)).join(" / ")}; max |diff| ${ex(worst)}`);
  gate(`${name}: at the identified mix the ends are v5's 48 / 11`,
    flat.indexOf(Math.min(...flat)) === lo && flat.indexOf(Math.max(...flat)) === hi && lo === 48 && hi === 11);
  const S = { v5_band_bn: v5.band_bn, ends: [lo, hi], union_at_new_responses_bn: [pu[lo], pu[hi]], readings: {}, per_person: {},
    unit_bands: {} };
  const perPerson = (rt, mix) => ({ g3plus_member_usd: [G[rt][mix][lo] * 1e9, G[rt][mix][hi] * 1e9],
    white_usd: [W[mix][lo] * 1e9, W[mix][hi] * 1e9] });
  for (const rt of ROUTES) {
    S.readings[rt] = {};
    S.per_person[rt] = { identified: perPerson(rt, "identified") };
    for (const r of READINGS) {
      const m3 = `${r}|g3_rate`, mL = `${r}|later`;
      const c = caseAt(rt, m3, mL);
      const oLo = c.indexOf(Math.min(...c)), oHi = c.indexOf(Math.max(...c));
      const part = (i) => ({ g3_rate_bn: (1 - C3) * A.g3_rate * (G[rt][m3][i] - G[rt].identified[i]) + C3 * A.g3_rate * (W[m3][i] - W.identified[i]),
        later_bn: A.later * (G[rt][mL][i] - G[rt].identified[i]) });
      S.readings[rt][r] = { band_bn: [c[lo], c[hi]], change_bn: [c[lo] - flat[lo], c[hi] - flat[hi]], own_ends: [oLo, oHi],
        own_band_bn: [c[oLo], c[oHi]], change_by_part_bn: [part(lo), part(hi)],
        added_per_person_usd: [(c[lo] - pu[lo]) * 1e9 / A.added, (c[hi] - pu[hi]) * 1e9 / A.added],
        per_member_usd: [c[lo] * 1e9 / A.population, c[hi] * 1e9 / A.population] };
      S.per_person[rt][m3] = perPerson(rt, m3);
      S.per_person[rt][mL] = perPerson(rt, mL);
      bandRows.push({ set: name, route: rt, reading: r, low_bn: c[lo], high_bn: c[hi], change_low_bn: c[lo] - flat[lo],
        change_high_bn: c[hi] - flat[hi], g3_rate_part_low_bn: part(lo).g3_rate_bn, g3_rate_part_high_bn: part(hi).g3_rate_bn,
        later_part_low_bn: part(lo).later_bn, later_part_high_bn: part(hi).later_bn, own_low_spec: oLo, own_high_spec: oHi,
        own_low_bn: c[oLo], own_high_bn: c[oHi] });
    }
    S.unit_bands[rt] = Object.fromEntries(UNIT.map((u) => [u, { g3plus_member_bn: run(g3Model(X, u, rt), [lo, hi]) }]));
  }
  S.unit_bands.white = Object.fromEntries(UNIT.map((u) => [u, run(wModel(X, u), [lo, hi])]));
  bandRows.push({ set: name, route: "both", reading: "flat (v5)", low_bn: flat[lo], high_bn: flat[hi], change_low_bn: 0, change_high_bn: 0,
    g3_rate_part_low_bn: 0, g3_rate_part_high_bn: 0, later_part_low_bn: 0, later_part_high_bn: 0,
    own_low_spec: lo, own_high_spec: hi, own_low_bn: flat[lo], own_high_bn: flat[hi] });
  // The engine-key route is linear in the mix (the factors are), so the unit bands give any mix's G3+ member exactly.
  const lin = (mix) => [0, 1].map((j) => UNIT.reduce((s, u, k) => s + BL.mixes[mix].pi[k] * S.unit_bands.keys[u].g3plus_member_bn[j], 0));
  const worstLin = Math.max(...MIXES.flatMap((m) => [0, 1].map((j) => Math.abs(lin(m)[j] - G.keys[m][[lo, hi][j]]) * 1e9)));
  gate(`${name}: the engine-key route is linear in the mix: the unit bands give every mix's G3+ member ($1e-6 a person)`, worstLin < 1e-6,
    `max |diff| $${ex(worstLin)}`);
  const wl = (mix) => [0, 1].map((j) => UNIT.reduce((s, u, k) => s + BL.mixes[mix].pi[k] * S.unit_bands.white[u][j], 0));
  S.white_unit_band_residual_usd = MIXES.map((m) => ({ mix: m, residual: [0, 1].map((j) => (wl(m)[j] - W[m][[lo, hi][j]]) * 1e9) }));
  priceOut.sets[name] = S;
}
gate("no G3+ cell with an amount has an all-zero age profile", ZERO_PROFILE.length === 0, ZERO_PROFILE.slice(0, 3).join("; "));
stop();
fs.mkdirSync(OUT, { recursive: true });
const cols = Object.keys(bandRows[0]);
fs.writeFileSync(path.join(OUT, "price_bands.csv"), [cols.join(","), ...bandRows.map((r) => cols.map((k) =>
  typeof r[k] === "number" && !Number.isInteger(r[k]) ? r[k].toFixed(9) : r[k]).join(","))].join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "price_summary.json"), JSON.stringify(priceOut, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "gates_price.json"), JSON.stringify({ gates: GATES }, null, 1) + "\n");
for (const r of bandRows) console.log(`  ${r.set} ${r.route.padEnd(5)} ${r.reading.padEnd(26)} ${r.low_bn.toFixed(2)} / ${r.high_bn.toFixed(2)}  change ${r.change_low_bn.toFixed(2)} / ${r.change_high_bn.toFixed(2)}  (G3-rate ${r.g3_rate_part_low_bn.toFixed(2)} / ${r.g3_rate_part_high_bn.toFixed(2)}, later ${r.later_part_low_bn.toFixed(2)} / ${r.later_part_high_bn.toFixed(2)})  own ends ${r.own_low_spec} / ${r.own_high_spec}`);
