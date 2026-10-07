/* Item added_age_mix of the v6 registry (package.cjs), a lineage item: main case v5's 3.04M added people priced at
 * their measured age mix (added_age_mix_2026_10_07, committed 21d9a21d; its RESULT.md sections 1-4), on v5's own
 * lineage route (main_case_lineage_2026_10_05/lineage_case.cjs augmented()).
 *
 * v5's addition prices every added person at the identified third-plus's ages: its amount in each engine cell is
 * m_G x G + m_W x W, with G a corrected G3+ member (the G3+ model over its members), W a third-plus non-Hispanic white
 * at the G3+'s ages, m_G = later + (1 - C3) g3 and m_W = C3 g3. Here the two count parts take their own mixes
 * (age_mix.json): the G3-rate persons (g3) theirs and the later losses theirs, the white end of the G3-rate blend at
 * the G3-rate persons' mix, as price.cjs prices them. The addition's cell edits and its production grid are v5's plus
 *   later x (G_L - G) + (1 - C3) g3 x (G_3 - G) + C3 g3 x (W_3 - W),
 * so the identified mix gives v5's addition exactly (gated); row 8's edit, the counts, C3 and the group-size responses
 * stay v5's. G_x is price.cjs's G3+ member at mix x: each cell times f = sum_b (pi'_b / pi_b) T_b / sum_b T_b, T the
 * engine's own key for the cell and allocation by five-year band (g3_age_keys.json); on the set the pension rule's
 * three lines take the profile of what the rule puts in them, and the production grid follows the wage key. The rough
 * route (an arm) takes the white lane's rough re-key factor per line instead. W_x is white_lines.py's white at mix x
 * (band_lines.json).
 *
 * Copied from added_age_mix_2026_10_07/price.cjs (commit 21d9a21d), lines 245-261 (cellsOf, cellId, partModel,
 * zeroGrid, WSIDE), 370-435 (lineKey, profileOf, ageFactor, prof, comb, pensionProfile, PENSION_LINES, g3ModelKeys,
 * g3ModelRough) and 448-451 (wModel), with the inputs they read passed in (X, AK, BL, PI0, PENSION, GCASH) in place of
 * price.cjs's globals; the gates of price.cjs that check those inputs run here.
 *
 * build(ctx, arm) returns { additions: {set, cash}, lineage_meta, record, detail }: the two additions in the lineage
 * lane's payload format (v5's ADDITION with new by values and production arrays), what package.cjs adds to
 * meta.lineage, what meta.items carries, and the per-person part models (G at the three mixes, W at two) that
 * main_case.cjs evaluates for the parts. At a lineage option (ctx.LINEAGE_OPTION, lineage_count.cjs: another arm of the
 * count or another C3) the counts, C3 and the addition the deltas add to are the option's, and the two parts keep the
 * mixes measured on arm b's counts [ASSUMPTION: the age-mix lane priced arm b only]. Run nothing: a module.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.join(__dirname, "..");
const LANE = "added_age_mix_2026_10_07";
const COMMIT = "21d9a21d";
const GEN = "generation_account_2026_09_24/derived";
const FILES = {
  age_mix: `${LANE}/derived/age_mix.json`, band_lines: `${LANE}/derived/band_lines.json`, age_keys: `${LANE}/derived/g3_age_keys.json`,
  price_summary: `${LANE}/derived/price_summary.json`, summary: `${LANE}/derived/summary.json`,
};
const GEN_FILES = { model: `${GEN}/model_G3plus.json`, set: `${GEN}/generation_corrections_sept29.json`, cash: `${GEN}/generation_corrections_sept29_cash.json` };
const WHITE_FILE = "main_case_lineage_2026_10_05/derived/white_lines.json";
const WHITE_AGES = "g3plus_ages";
const CENTRAL = { reading: "cross_section_2007_2026", route: "keys" };
const ARMS = {
  cohort_at_birth: { reading: "cohort_at_birth", route: "keys", source_arm: "keys/cohort_at_birth",
    label: "the cohort reading: each band at the child-stage loss rate of the cohorts born in it (the report at birth persists), which the within-cohort table does not support" },
  rough_keys: { reading: "cross_section_2007_2026", route: "rough", source_arm: "rough/cross_section_2007_2026",
    label: "the central mix on the rough-key route: every cell of a line times the white lane's rough re-key factor for the line (band_lines.py), which gives one age profile to both allocations" },
};
const ALLOCS = ["personal", "shared"];
const BASIS = { set: "accrual", cash: "cash" };
const clone = (x) => JSON.parse(JSON.stringify(x));
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const blocked = (why) => { throw new Error("[BLOCKED] item added_age_mix: " + why); };

// ---------------------------------------------------------------------------------------------------
// From price.cjs (21d9a21d), lines 245-261.
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

// From price.cjs, lines 370-435 and 448-451; its globals AK, BL, PI0, PENSION and gcashCells are passed in as I.
const lineKey = (c) => `${WSIDE[c.side]}|${c.line}`;
// The engine-key route: each G3+ cell moves by f = sum_b rho_b T_b / sum_b T_b, rho = pi' / pi (g3_age_keys.py).
function profileOf(I, c, a, cell) {
  if (c.side === "spending" && I.AK.line_keys[c.line]) return I.AK.line_keys[c.line][a];
  const key = c.side === "receipt" ? cell.key : c.key;
  const p = I.AK.keys[c.side][a][key];
  if (!p) blocked(`no age profile for ${c.side} ${c.line} key ${key}`);
  return p;
}
const ageFactor = (T, rho) => {
  const den = T.reduce((s, x) => s + x, 0);
  return den === 0 ? 1 : T.reduce((s, x, b) => s + rho[b] * x, 0) / den;
};
// The set's pension rule (v4, meta.pension_accrual) rewrites three G3+ lines from the cash set's: Social Security is
// ratio_net x the group's OASDI receipts, Medicare swaps its Part A share for an accrual on HI receipts, and federal
// income tax loses the tax on benefits. Their cells take the age profile of what they now hold.
const prof = (T) => { const s = T.reduce((a, x) => a + x, 0); return T.map((x) => x / s); };
const comb = (parts) => parts[0][1].map((_, b) => parts.reduce((a, [amt, T]) => a + amt * prof(T)[b], 0));
function pensionProfile(I, X, c, a, cell) {
  const rc = (line) => X.gCells.get(`receipt|${line}|cbo_collective`)[a];
  const rp = (line) => I.AK.keys.receipt[a][rc(line).key];
  const se = rc("self_employment_oasdi_hi").target_bn;
  if (c.line === "social_security") {
    return comb([[rc("employee_oasdi").target_bn, rp("employee_oasdi")], [rc("employer_oasdi").target_bn, rp("employer_oasdi")],
      [I.PENSION.se_oasdi_share * se, rp("self_employment_oasdi_hi")]]);
  }
  const cash = I.gcashCells.get(cellId(c))[a].target_bn;
  if (c.line === "medicare") {
    const keep = (1 - I.PENSION.part_a_share) * cash;
    const hi = [[rc("employee_hi").target_bn, rp("employee_hi")], [rc("employer_hi").target_bn, rp("employer_hi")],
      [(1 - I.PENSION.se_oasdi_share) * se, rp("self_employment_oasdi_hi")]];
    const hiT = hi.reduce((s, [amt]) => s + amt, 0);
    return comb([[keep, I.AK.keys.spending[a][c.key]], ...hi.map(([amt, T]) => [(cell.target_bn - keep) * amt / hiT, T])]);
  }
  return comb([[cash, I.AK.keys.receipt[a][cell.key]], [cell.target_bn - cash, I.AK.keys.spending[a].social_security]]);
}
const PENSION_LINES = new Set(["social_security", "medicare", "federal_income_tax"]);
function g3ModelKeys(I, X, mix) {
  const rho = I.BL.mixes[mix].pi.map((p, b) => p / I.PI0[b]);
  const fp = ageFactor(I.AK.production, rho);
  return partModel(X.U, (c, a) => {
    const cell = X.gCells.get(cellId(c))[a];
    const T = X.name === "set" && PENSION_LINES.has(c.line) ? pensionProfile(I, X, c, a, cell) : profileOf(I, c, a, cell);
    if (T.every((x) => x === 0) && Math.abs(cell.target_bn) > 1e-9) I.ZERO_PROFILE.push(`${c.side} ${c.line} ${a}: ${cell.target_bn}`);
    return cell.target_bn / X.NG * ageFactor(T, rho);
  }, { private_wtp_bn: X.G.production.private_wtp_bn.map((x) => x / X.NG * fp),
    induced_receipts_bn: X.G.production.induced_receipts_bn.map((x) => x / X.NG * fp) });
}
// The rough-key route (cross-check): the white lane's rough re-key factors per line (band_lines.py), every cell alike.
function g3ModelRough(I, X, mix) {
  const g = I.BL.mixes[mix].g3x[BASIS[X.name]];
  const missing = cellsOf(X.U).filter((c) => !(lineKey(c) in g.factors));
  if (missing.length) blocked(`${mix}: no factor for ${missing[0].line}`);
  const fp = g.production_factor;
  return partModel(X.U, (c, a) => X.gCells.get(cellId(c))[a].target_bn / X.NG * g.factors[lineKey(c)],
    { private_wtp_bn: X.G.production.private_wtp_bn.map((x) => x / X.NG * fp),
      induced_receipts_bn: X.G.production.induced_receipts_bn.map((x) => x / X.NG * fp) });
}
const g3Model = (I, X, mix, route) => (route === "keys" ? g3ModelKeys : g3ModelRough)(I, X, mix);
function wModel(I, X, mix) {
  const w = I.BL.mixes[mix].white[BASIS[X.name]].lines;
  return partModel(X.U, (c) => w[lineKey(c)], zeroGrid(X.U));
}

// ---------------------------------------------------------------------------------------------------
const cellMap = (m) => new Map(cellsOf(m).map((c) => [cellId(c), c.cell]));
const pct = (x) => `${(100 * x).toFixed(1)}%`;
const under20 = (bands, pi) => bands.reduce((s, b, k) => s + (Number(b.split(/[-+]/)[0]) < 20 ? pi[k] : 0), 0);
const sameDims = (a, b) => JSON.stringify(Object.keys(a).sort()) === JSON.stringify(Object.keys(b).sort())
  && Object.keys(a).every((k) => JSON.stringify(a[k]) === JSON.stringify(b[k]));

function build(ctx, arm) {
  const { B, Engine } = ctx;
  const sel = arm ? ARMS[arm] : CENTRAL;
  if (!sel) blocked(`no arm ${arm} (${Object.keys(ARMS).join(", ")})`);
  const POP = B.POP, ARM = POP.meta.central_arm, A5 = POP.arms[ARM], C35 = POP.c3.value, NG = POP.meta.g3_account;
  const MIX = readJson(FILES.age_mix), BL = readJson(FILES.band_lines), AK = readJson(FILES.age_keys), WL = readJson(WHITE_FILE);
  const PS = readJson(FILES.price_summary);
  if (!(MIX.meta.arm === ARM && MIX.meta.g3_rate === A5.g3_rate && MIX.meta.later === A5.later && MIX.meta.c3 === C35 && !POP.c3.override)) {
    blocked("age_mix.json is not on v5's arm, counts and C3 (population.json)");
  }
  // A lineage option (lineage_count.cjs, package.cjs caseOf's fourth argument) brings its counts, C3 and addition; the
  // two parts keep the mixes measured on arm b's counts [ASSUMPTION: the age-mix lane priced arm b only].
  const OPT = ctx.LINEAGE_OPTION || null;
  const A = OPT ? OPT.A : A5, C3 = OPT ? OPT.C3 : C35, ADD = OPT ? OPT.additions : B.ADDITION;
  const PI0 = MIX.meta.identified;
  const m3 = `${sel.reading}|g3_rate`, mL = `${sel.reading}|later`;
  if (JSON.stringify(BL.mixes.identified.pi) !== JSON.stringify(PI0) || !BL.mixes[m3] || !BL.mixes[mL]
    || JSON.stringify(BL.mixes[m3].pi) !== JSON.stringify(MIX.readings[sel.reading].g3_rate) || JSON.stringify(BL.mixes[mL].pi) !== JSON.stringify(MIX.readings[sel.reading].later)) {
    blocked(`band_lines.json does not hold age_mix.json's identified mix and the ${sel.reading} mixes`);
  }
  if (PS.meta.arm !== ARM || PS.meta.c3 !== C35 || !PS.sets.set.readings[sel.route][sel.reading]) blocked(`price_summary.json has no ${sel.route} ${sel.reading} reading on v5's arm`);
  const PENSION = B.SEPT29.correctionsPayload().meta.pension_accrual;
  const G0 = readJson(GEN_FILES.model);
  const GP = { set: readJson(GEN_FILES.set), cash: readJson(GEN_FILES.cash) };
  const GM = { set: Engine.applyCorrections(G0, GP.set.payloads.a.G3plus), cash: Engine.applyCorrections(G0, GP.cash.payloads.a.G3plus) };
  const gcashCells = cellMap(GM.cash);
  {
    // price.cjs's gate: the set's and cash set's G3+ models differ only in the pension rule's three lines.
    const differ = [...new Set(cellsOf(GM.set).filter((c) => ALLOCS.some((a) => Math.abs(c.cell[a].target_bn
      - gcashCells.get(cellId(c))[a].target_bn) > 1e-12)).map((c) => c.line))].sort();
    if (JSON.stringify(differ) !== JSON.stringify([...PENSION_LINES].sort())) blocked(`the set's and cash set's G3+ models differ in ${differ.join(", ")}`);
  }
  const I = { AK, BL, PI0, PENSION, gcashCells, ZERO_PROFILE: [] };
  const mG = A.later + (1 - C3) * A.g3_rate, mW = C3 * A.g3_rate;
  const additions = {}, detail = { reading: sel.reading, route: sel.route, counts: { later: A.later, g3_rate: A.g3_rate, c3: C3 }, part_models: {} };
  const deltaWorst = {};
  for (const which of ["set", "cash"]) {
    const base = which === "set" ? B.SEPT29 : B.SEPT29_CASH;
    if (GP[which].meta.union !== B.BASE_FILES[which]) blocked(`${GEN_FILES[which]} does not split ${B.BASE_FILES[which]}`);
    const U = base.payloadModel();
    const X = { name: which, U, G: GM[which], gCells: cellMap(GM[which]), NG };
    if (JSON.stringify(cellsOf(X.G).map(cellId)) !== JSON.stringify(cellsOf(U).map(cellId)) || JSON.stringify(X.G.production.dims) !== JSON.stringify(U.production.dims)) {
      blocked(`${which}: the G3+ model lacks the union's cells or production grid`);
    }
    // v5's addition (at a lineage option, the option's), rebuilt from the G3+ cells and the whites (the lineage lane's
    // augmented()): it must be that addition exactly.
    const add5 = ADD[which], cells = cellsOf(U);
    const wl = WL[WHITE_AGES][BASIS[which]];
    const W = new Map(wl.low.lines.map((l) => [`${l.side}|${l.id}`, l.amount_bn / wl.low.population]));
    const w = (c) => W.get(`${WSIDE[c.side]}|${c.line}`);
    if (add5.meta.lineage.m_g3plus !== mG || add5.meta.lineage.m_white !== mW) blocked(`${which}: v5's m_G and m_W are not later + (1 - C3) g3 and C3 g3`);
    const row8 = add5.edits[add5.edits.length - 1];
    const rebuilt = cells.map((c) => {
      const e = { side: c.side, line: c.line, by: {} };
      if (c.side === "receipt") e.scenario = c.scenario; else e.key = c.key;
      for (const a of ALLOCS) e.by[a] = mG * X.gCells.get(cellId(c))[a].target_bn / NG + mW * w(c);
      return e;
    });
    if (JSON.stringify(rebuilt.concat([row8])) !== JSON.stringify(add5.edits) || row8.line !== "lane_constants") blocked(`${which}: v5's addition does not rebuild from the G3+ cells and the whites exactly`);
    const prod5 = ["private_wtp_bn", "induced_receipts_bn"].every((k) => JSON.stringify(U.production[k].map((v, i) => v + mG * X.G.production[k][i] / NG)) === JSON.stringify(add5.production[k]));
    if (!prod5 || !sameDims(add5.production.dims, U.production.dims)) blocked(`${which}: v5's addition's production grid does not rebuild exactly`);
    // The part models at the identified mix are v5's G3+ member and white, cell for cell (exact).
    const Gid = g3Model(I, X, "identified", "keys"), Wid = wModel(I, X, "identified");
    const gidCells = cellMap(Gid), widCells = cellMap(Wid);
    if (!cells.every((c) => ALLOCS.every((a) => gidCells.get(cellId(c))[a].target_bn === X.gCells.get(cellId(c))[a].target_bn / NG && widCells.get(cellId(c))[a].target_bn === w(c)))) {
      blocked(`${which}: at the identified mix the G3+ member and the white are not v5's exactly`);
    }
    if (sel.route === "rough") {
      const rid = cellMap(g3Model(I, X, "identified", "rough"));
      if (!cells.every((c) => ALLOCS.every((a) => rid.get(cellId(c))[a].target_bn === gidCells.get(cellId(c))[a].target_bn))) {
        blocked(`${which}: the rough route at the identified mix is not v5's G3+ member`);
      }
    }
    const G3 = g3Model(I, X, m3, sel.route), GL = g3Model(I, X, mL, sel.route), W3 = wModel(I, X, m3);
    const g3c = cellMap(G3), glc = cellMap(GL), w3c = cellMap(W3);
    let worst = 0;
    const edits = cells.map((c, k) => {
      const e = clone(add5.edits[k]), id = cellId(c);
      for (const a of ALLOCS) {
        const g = gidCells.get(id)[a].target_bn, wi = widCells.get(id)[a].target_bn;
        const d = A.later * (glc.get(id)[a].target_bn - g) + (1 - C3) * A.g3_rate * (g3c.get(id)[a].target_bn - g) + C3 * A.g3_rate * (w3c.get(id)[a].target_bn - wi);
        worst = Math.max(worst, Math.abs(d));
        e.by[a] = add5.edits[k].by[a] + d;
      }
      return e;
    });
    deltaWorst[which] = worst;
    const production = clone(add5.production);
    for (const k of ["private_wtp_bn", "induced_receipts_bn"]) {
      production[k] = add5.production[k].map((v, i) => v + A.later * (GL.production[k][i] - Gid.production[k][i])
        + (1 - C3) * A.g3_rate * (G3.production[k][i] - Gid.production[k][i]));
    }
    const add = clone(add5);
    add.edits = edits.concat([clone(row8)]);
    add.production = production;
    add.meta.source = "main_case_2026_10_07/item_age_mix.cjs (package.cjs item added_age_mix)";
    add.meta.status = `v6 item added_age_mix${arm ? ` at arm ${arm}` : ""}: ${OPT ? `the lineage at option ${OPT.name}` : B.LINEAGE_FILES[which]} with the added people at the ${sel.reading} mix (${sel.route} route)`;
    add.meta.case = `${add5.meta.case}; the added people at their measured age mix (${LANE}, ${sel.reading}, ${sel.route} route)`;
    additions[which] = add;
    detail.part_models[which] = { identified: Gid, g3_rate: G3, later: GL, white_identified: Wid, white_g3_rate: W3 };
  }
  if (I.ZERO_PROFILE.length) blocked(`a G3+ cell with an amount has an all-zero age profile (${I.ZERO_PROFILE.slice(0, 3).join("; ")})`);
  const bands = MIX.meta.bands;
  const shares = { identified: under20(bands, PI0), g3_rate: under20(bands, MIX.readings[sel.reading].g3_rate), later: under20(bands, MIX.readings[sel.reading].later) };
  const src = (which) => PS.sets[which].readings[sel.route][sel.reading];
  const files = Object.fromEntries(Object.entries(FILES).map(([k, f]) => [k, { file: f, sha256: sha256(f) }]));
  const ageMix = {
    item: "added_age_mix", arm: arm || null,
    measured: "basic monthly CPS 1994-2026 (IPUMS-CPS, months in sample 1 and 5): identity loss by age for G3anc and G4anc, the 2007-26 cross-section central",
    reading: sel.reading, route: sel.route,
    rule: "each count part at its own mix: the G3-rate persons and the later losses priced as G3+ members at their mixes, the white end of the G3-rate blend at the G3-rate persons' mix; counts, C3 and the group-size responses are v5's, so only the ages move (meta.members' 'at the G3+'s ages' holds for the identified mix only)",
    route_rule: sel.route === "keys"
      ? "the engine's own keys by five-year band (g3_age_keys.json): each G3+ cell times f = sum_b (pi'_b / pi_b) T_b / sum_b T_b; the set's Social Security, Medicare and federal income tax cells take the profile of what the pension rule puts in them; production follows the wage key"
      : "the white lane's rough re-key factor per line (band_lines.json g3x), every cell of a line alike",
    under_20_share: Object.assign({}, shares, { printed: `${pct(shares.g3_rate)} of the G3-rate persons and ${pct(shares.later)} of the later losses are under 20, against ${pct(shares.identified)} of the identified third-plus` }),
    bands, mixes: { identified: PI0, g3_rate: MIX.readings[sel.reading].g3_rate, later: MIX.readings[sel.reading].later },
    edits: "the 335 cell edits and the production grid are v5's addition (the identified mix) plus later x (G_L - G) + (1 - C3) g3 x (G_3 - G) + C3 g3 x (W_3 - W); row 8's edit is v5's",
    replaces: { set: B.LINEAGE_FILES.set, cash: B.LINEAGE_FILES.cash },
    source: { lane: LANE, commit: COMMIT, files, white: WHITE_FILE, g3plus_model: `${GEN_FILES.model} + ${GEN_FILES.set} / ${GEN_FILES.cash} payloads.a.G3plus` },
  };
  const atOption = OPT ? { option: OPT.name, label: OPT.label, counts: { later: A.later, g3_rate: A.g3_rate, c3: C3 },
    assumption: "[ASSUMPTION] the option's two parts take the mixes the age-mix lane measured on arm b's counts (it priced arm b only): the G3-rate persons the G3-rate mix, the later losses the later-loss mix; the deltas are those per-person mixes at the option's counts and C3" } : null;
  if (OPT) { ageMix.count_option = clone(atOption); ageMix.replaces = { set: `the addition at lineage option ${OPT.name}`, cash: `the addition at lineage option ${OPT.name}` }; }
  const record = {
    reading: sel.reading, route: sel.route, source_arm: `${sel.route}/${sel.reading}`,
    rule: "item_age_mix.cjs: v5's addition plus the age-mix deltas, rebuilt on the September 29 payloads by v5's merge(), adoptLineage() and forCase()",
    counts: { later: A.later, g3_rate: A.g3_rate, c3: C3 }, under_20_share: shares,
    source_band_bn: src("set").band_bn, source_change_bn: src("set").change_bn, source_change_by_part_bn: src("set").change_by_part_bn,
    source_cash_band_bn: src("cash").band_bn, source_cash_change_bn: src("cash").change_bn, source_cash_change_by_part_bn: src("cash").change_by_part_bn,
    source_band_specs: src("set").own_ends, source_cash_band_specs: src("cash").own_ends,
    largest_cell_delta_bn: deltaWorst,
  };
  if (OPT) record.count_option = clone(atOption);
  return { additions, lineage_meta: { age_mix: ageMix }, record, detail };
}

module.exports = { build, ARMS, CENTRAL, FILES, LANE, COMMIT, cellsOf, cellId };
