/* The lineage's count and C3 as case options (package.cjs caseOf(base, ids, arms, lineage)): main case v5's lineage
 * addition rebuilt at another arm of the count (population.json: floor, a, b, c) or at another C3, by the lineage lane's
 * own route (main_case_lineage_2026_10_05/lineage_case.cjs, committed d3b7e6e6: augmented() and payloadFor()), with the
 * group-size responses at the arm's share of the population and metro factor (responsesAt()). lineage_case.cjs runs at
 * load and writes into its lane, so the route is copied here: its lines 135-224 (the responses, their formulas and
 * gates), 293-335 (the G3+ member and the white per person, setUp()), 348-361 (augmented()) and 647-685 (payloadFor()),
 * with the inputs passed in where that file reads its globals.
 *
 *   OPTIONS          the named options: arm_a and arm_c (the count's arms, 1.81M and 4.27M added people) and
 *                    c3_minus_se and c3_plus_se (C3 0.5567 -/+ its SE 0.2457, at arm b's counts). C3 does not move the
 *                    group's share (lineage_case.cjs c3_line), so a C3 option keeps arm b's responses and row 8 edit.
 *   optionOf(B, name, tools)  the option on base B (a v5-style module: POP, SEPT29, SEPT29_CASH, ADDITION, BASE_FILES,
 *                    csvRows): {name, label, arm, A (the arm's counts), C3, c3, m_g3plus, m_white, additions: {set,
 *                    cash}, meta}; additions are the lineage lane's payload additions at the option, in its format
 *                    (B.ADDITION's), their meta.source and meta.status naming this module and the option.
 *   additionsAt(B, arm, c3, tools)  the same additions for any arm and C3; at v5's arm and C3 they are B.ADDITION, byte
 *                    for byte as JSON (gated on every build), so the route is v5's.
 *
 * Gates (thrown as [BLOCKED]): the response formulas at v4's share give the stored responses (lineage_case.cjs's gates,
 * its tolerances); the G3+ model has the union's cells and grid; every line has a white amount; the additions at v5's
 * count and C3 are v5's exactly. main_case.cjs gates each option's case against the lineage lane's stored arm bands and
 * C3 lines. Run nothing: a module.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const FISCAL = path.join(__dirname, "..");
const HERE_LANE = path.basename(__dirname);
const LINEAGE_LANE = "main_case_lineage_2026_10_05";
const ROUTE = { file: `${LINEAGE_LANE}/lineage_case.cjs`, commit: "d3b7e6e6" };
const FILES = {
  r_values: "finite_response_2026_09_26/derived/r_values.json",
  long_run: "service_response_long_run_2026_09_27/derived/responses.json",
  housing: "receipt_side_long_run_2026_09_28/derived/housing.json",
  counties: "receipt_side_long_run_2026_09_28/derived/counties.csv",
  white: `${LINEAGE_LANE}/derived/white_lines.json`,
};
const GEN = "generation_account_2026_09_24/derived";
const SETS = { set: { gen: "generation_corrections_sept29.json", white: "accrual" }, cash: { gen: "generation_corrections_sept29_cash.json", white: "cash" } };
const WHITE_AGES = "g3plus_ages";
const ROW8_C = 2.0;   // main_case_2026_09_24/package.cjs CONSTANTS.row8.c, gated below
const ALLOCS = ["personal", "shared"];
const ENDS = ["low", "high"];
const OPTIONS = {
  arm_a: { arm: "a", label: "the count's arm a: the fourth-plus generation lost at the third generation's rate, no later losses (1.81M added)" },
  arm_c: { arm: "c", label: "the count's arm c: losses compounding at rho 0.5 past the third generation (4.27M added)" },
  c3_minus_se: { c3_se: -1, label: "C3 one standard error below the central, 0.5567 - 0.2457, at arm b's counts" },
  c3_plus_se: { c3_se: 1, label: "C3 one standard error above the central, 0.5567 + 0.2457, at arm b's counts" },
};
const clone = (x) => JSON.parse(JSON.stringify(x));
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const blocked = (why) => { throw new Error("[BLOCKED] lineage_count: " + why); };
const check = (name, ok, detail) => { if (!ok) blocked(`${name}${detail ? ` (${detail})` : ""}`); };

// ---------------------------------------------------------------------------------------------------
// lineage_case.cjs lines 135-224: the group-size responses, each its stored v4 value plus the change of its formula
// between the v4 share and the option's, so the v4 share gives the stored values exactly.
function routeOf(B) {
  const RV = readJson(FILES.r_values), LR = readJson(FILES.long_run), HOUSING = readJson(FILES.housing);
  const COUNTIES = B.csvRows(FILES.counties);
  const R4 = B.SEPT29.correctionsPayload().meta.responses;
  const S4 = B.POP.meta.s_v4;
  const rFin = (b, s) => (1 - Math.pow(1 - s, b)) / s;
  const cap1 = (x) => Math.min(x, 1);
  const ggOf = (s) => ({ low: (RV.state_local_bn * rFin(RV.b_admin, s) + RV.federal_tax_bn * rFin(RV.b_fin, s)) / RV.total_bn,
    high: rFin(RV.b_admin, s) });
  const row8Of = (s) => (rFin(RV.b_all, s) - rFin(RV.b_admin, s)) / (RV.b_all - RV.b_admin);
  const HWY = LR.elasticities.highways_nontoll, PARKS = LR.elasticities.parks, B_ADMIN = LR.elasticities.administration_general_government.b;
  // service_response_long_run_2026_09_27/build.py RULES, subfunction by subfunction.
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
    if (!R) blocked("unknown subfunction rule " + rule);
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
  check("audit row 8's constant is the September 24 package's 2.0", B.SEPT29.CONSTANTS && B.SEPT29.CONSTANTS.row8 && B.SEPT29.CONSTANTS.row8.c === ROW8_C);
  check("general government: r_values.py's formula at s_v4 gives meta.responses (low, high; 1e-14)",
    Math.abs(AT_V4.gg.low - R4.general_government.low) < 1e-14 && Math.abs(AT_V4.gg.high - R4.general_government.high) < 1e-14
    && R4.general_government.s === S4, `${AT_V4.gg.low} / ${AT_V4.gg.high}`);
  check("audit row 8's factor at s_v4 is meta.responses.row8_factor (1e-14)", Math.abs(AT_V4.row8 - R4.row8_factor) < 1e-14, `${AT_V4.row8}`);
  check("every long-run subfunction has build.py's rule, and the rules at the lane's s give its stored responses (1e-14)",
    LR.meta.s === S4 && SUBS.every((x) => SF_RULE[x.id] && ENDS.every((e) => Math.abs(AT_V4.sf[x.id][e] - x.response[e]) < 1e-14))
    && Object.keys(SF_RULE).length === SUBS.length, `${SUBS.length} subfunctions`);
  // build.py blends with Python's sum (compensated since 3.12), so a line's response is its stored blend plus the
  // change of this blend.
  const blendOf = (line, sf) => LR.lines[line].subfunctions.reduce((a, x) => a + x.national_bn * sf[x.id], 0) / LR.lines[line].national_bn;
  const stored = Object.fromEntries(SUBS.map((x) => [x.id, x.response]));
  const STORED_BLEND = Object.fromEntries(LR_LINES.map((line) => [line, Object.fromEntries(ENDS.map((e) =>
    [e, blendOf(line, Object.fromEntries(SUBS.map((x) => [x.id, stored[x.id][e]])))]))]));
  check("the line blends of the stored subfunction responses are meta.responses' and the response lane's line responses (2e-16)",
    LR_LINES.every((line) => ENDS.every((e) => Math.abs(STORED_BLEND[line][e] - R4[line][e]) < 2e-16 && R4[line][e] === LR.lines[line].response[e])));
  check("meta.responses' subfunctions are the response lane's (exact)", LR_LINES.every((line) => R4[line].subfunctions.every((x) => {
    const y = stored[x.id];
    return y && x.low === y.low && x.high === y.high;
  })));
  check("the property formula on counties.csv gives housing.json's owner and renter responses and the payload's (5e-6: six-decimal inputs)",
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
  return { R4, LR_LINES, responsesAt, files: FILES };
}

// ---------------------------------------------------------------------------------------------------
// lineage_case.cjs lines 275-335: cells, the corrected G3+ model (convention a) and the whites per person, by set.
function cellsOf(m) {
  const out = [];
  for (const l of m.receipts.lines) for (const sc of Object.keys(l.cells)) out.push({ side: "receipt", line: l.id, scenario: sc, cell: l.cells[sc] });
  for (const l of m.spending.lines) for (const k of Object.keys(l.keys)) out.push({ side: "spending", line: l.id, key: k, cell: l.keys[k] });
  return out;
}
const cellId = (c) => `${c.side}|${c.line}|${c.side === "receipt" ? c.scenario : c.key}`;
const WSIDE = { receipt: "receipts", spending: "spending" };
function setOf(B, Engine, which) {
  const S = SETS[which], rel = B.BASE_FILES[which], pkg = which === "set" ? B.SEPT29 : B.SEPT29_CASH;
  const U = pkg.payloadModel();
  check(`${which}: the base's September 29 package is ${rel}`, JSON.stringify(pkg.correctionsPayload()) === JSON.stringify(readJson(rel)));
  const gp = readJson(`${GEN}/${S.gen}`);
  check(`${which}: ${S.gen} splits ${rel}`, gp.meta.union === rel, gp.meta.union);
  const G = Engine.applyCorrections(readJson(`${GEN}/model_G3plus.json`), gp.payloads.a.G3plus);
  check(`${which}: the G3+ model has the union's cells and production grid`, JSON.stringify(cellsOf(G).map(cellId)) === JSON.stringify(cellsOf(U).map(cellId))
    && JSON.stringify(G.production.dims) === JSON.stringify(U.production.dims));
  const WL = readJson(FILES.white);
  check(`${which}: white_lines.json's central age structure is the identified G3+'s`, WL.meta.central === WHITE_AGES);
  const wl = WL[WHITE_AGES][S.white];
  const W = new Map(wl.low.lines.map((l) => [`${l.side}|${l.id}`, l.amount_bn / wl.low.population]));
  const missing = [...U.receipts.lines.map((l) => `receipts|${l.id}`), ...U.spending.lines.map((l) => `spending|${l.id}`)].filter((k) => !W.has(k));
  check(`${which}: every line of the model has a white amount (white_lines.json ${WHITE_AGES} ${S.white})`,
    !missing.length && W.size === U.receipts.lines.length + U.spending.lines.length, missing.join(", "));
  return { name: which, S, rel, U, G, gCells: new Map(cellsOf(G).map((c) => [cellId(c), c.cell])), wpp: (c) => W.get(`${WSIDE[c.side]}|${c.line}`) };
}

// lineage_case.cjs augmented() and payloadFor(): the addition at counts A, C3 and responses R.
function additionOf(B, X, route, arm, A, c3) {
  const POP = B.POP, NG = POP.meta.g3_account, C3 = c3.value, R4 = route.R4;
  const R = route.responsesAt(A.s, A.k_metro);
  const mG = A.later + (1 - C3) * A.g3_rate, mW = C3 * A.g3_rate;
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
  const base = readJson(X.rel).meta;
  const responses = clone(base.responses);
  responses.general_government.low = R.gg.low; responses.general_government.high = R.gg.high; responses.general_government.s = R.s;
  responses.row8_factor = R.row8;
  for (const line of route.LR_LINES) {
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
      source: `${LINEAGE_LANE}/lineage_case.cjs`,
      status: "candidate v5, not adopted: the v4 case plus the lineage line",
      builds_on: X.rel,
      apply: "Engine.applyCorrections(Engine.applyCorrections(MODEL, builds_on payload), this payload); evaluate with this meta's "
        + "responses in place of the v4 payload's (specification gg and line_responses at each reading) and capital_return "
        + "(components of kind long_run_subfunction take response.values[reading]); lineage_case.cjs specAt() and capitalAt() do this",
      case: `v4 (${X.rel}) plus ${(A.added / 1e6).toFixed(4)}M lineage persons (arm ${arm}): ${(A.later / 1e6).toFixed(4)}M later losses as `
        + `identified G3+ members and ${(A.g3_rate / 1e6).toFixed(4)}M G3-rate attriters at (1 - C3) G3+ + C3 whites, C3 ${C3}`,
      lineage: { arm, source_arm: A.source_arm, rho: A.rho, added: A.added, g3_rate: A.g3_rate, later: A.later, population: A.population,
        c3, m_g3plus: mG, m_white: mW, frame_factor: POP.meta.frame_factor, s: R.s, k_metro: R.k_metro,
        row8_edit_bn: d8, g3plus_model: `${GEN}/model_G3plus.json + ${X.S.gen} payloads.a.G3plus`,
        white: `${LINEAGE_LANE}/derived/white_lines.json (${WHITE_AGES}, ${X.S.white})`,
        responses_changed: ["general_government", "row8_factor", ...route.LR_LINES, "roads_vmt_sl", "roads_vmt_fed", "state_price_recreation_culture",
          "modeled_owner_property", "tenant_occupied_property", "capital_return long_run_subfunction values"] },
      responses, capital_return: capital,
    },
    edits,
    production,
  };
}

// ---------------------------------------------------------------------------------------------------
// Each base's route and set models are built once; the additions at v5's arm and C3 must be v5's on every base.
const MEMO = new WeakMap();
function memoOf(B, Engine) {
  if (!MEMO.has(B)) {
    const route = routeOf(B);
    const X = { set: setOf(B, Engine, "set"), cash: setOf(B, Engine, "cash") };
    const POP = B.POP, arm = POP.meta.central_arm;
    for (const w of ["set", "cash"]) {
      const v5 = additionOf(B, X[w], route, arm, POP.arms[arm], POP.c3);
      check(`${w}: the addition at v5's arm (${arm}) and C3 (${POP.c3.value}) is v5's (${B.LINEAGE_FILES[w]}), byte for byte as JSON`,
        JSON.stringify(v5) === JSON.stringify(B.ADDITION[w]));
    }
    MEMO.set(B, { route, X, options: new Map() });
  }
  return MEMO.get(B);
}
function additionsAt(B, arm, c3, tools) {
  const M = memoOf(B, tools.Engine), A = B.POP.arms[arm];
  if (!A) blocked(`population.json has no arm ${arm} (${Object.keys(B.POP.arms).join(", ")})`);
  return { set: additionOf(B, M.X.set, M.route, arm, A, c3), cash: additionOf(B, M.X.cash, M.route, arm, A, c3) };
}
// The option, or null at v5's arm and C3 (the case itself).
function optionOf(B, name, tools) {
  const o = OPTIONS[name];
  if (!o) blocked(`no lineage option ${name} (${Object.keys(OPTIONS).join(", ")})`);
  const M = memoOf(B, tools.Engine);
  if (M.options.has(name)) return M.options.get(name);
  const POP = B.POP, arm = o.arm || POP.meta.central_arm, A = POP.arms[arm];
  if (!A) blocked(`population.json has no arm ${arm}`);
  const C3 = o.c3_se ? POP.c3.value + o.c3_se * POP.c3.se : POP.c3.value;
  const c3 = o.c3_se ? Object.assign(clone(POP.c3), { value: C3,
    label: `${POP.c3.label}, ${o.c3_se > 0 ? "plus" : "minus"} one SE (${POP.c3.value} ${o.c3_se > 0 ? "+" : "-"} ${POP.c3.se})` }) : clone(POP.c3);
  if (arm === POP.meta.central_arm && C3 === POP.c3.value) blocked(`option ${name} is v5's arm and C3: the case itself`);
  const additions = additionsAt(B, arm, c3, tools);
  const meta = { name, label: o.label, arm, source_arm: A.source_arm, added: A.added, g3_rate: A.g3_rate, later: A.later, population: A.population,
    c3: C3, c3_central: POP.c3.value, c3_se: POP.c3.se, s: additions.set.meta.lineage.s, k_metro: A.k_metro,
    row8_edit_bn: additions.set.meta.lineage.row8_edit_bn, m_g3plus: additions.set.meta.lineage.m_g3plus, m_white: additions.set.meta.lineage.m_white,
    rule: "the lineage lane's addition (lineage_case.cjs augmented() and payloadFor()) at the option's counts and C3, with the 19 group-size responses, row 8's edit and the long-run capital values at the arm's share s and metro factor; C3 does not move s",
    route: clone(ROUTE), module: `${HERE_LANE}/lineage_count.cjs` };
  for (const w of ["set", "cash"]) {
    additions[w].meta.source = `${HERE_LANE}/lineage_count.cjs (${ROUTE.file}'s route)`;
    additions[w].meta.status = `lineage option ${name}, not adopted: ${o.label}`;
  }
  const out = { name, label: o.label, arm, A, C3, c3, m_g3plus: meta.m_g3plus, m_white: meta.m_white, additions, meta };
  M.options.set(name, out);
  return out;
}

module.exports = { OPTIONS, ROUTE, FILES, optionOf, additionsAt };
