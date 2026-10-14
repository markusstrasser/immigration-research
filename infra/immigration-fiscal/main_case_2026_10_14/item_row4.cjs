/* Items white_end_tax_keys and row4_frame of the v7 registry (package.cjs): the two measured residuals v6 states beside
 * its headline (ladder 298), as edit sets on the case. Both repeat the row-4 class lane's pricing of them on v6
 * (row4_class_2026_09_29/row4_oct07.cjs, which writes its files when run and exports nothing, so this module reads the
 * lane's inputs and ports its construction at the lines cited; main_case.cjs gates each item alone on v6 against the
 * lane's derived/row4_oct07.json moves at specifications 48 / 11, 1e-9, and the port's inputs against its recorded ones):
 *
 *   white_end_tax_keys  W, the lineage members priced as third-plus non-Hispanic whites (C3 x the G3-rate attriters,
 *                       meta.lineage.members.white), with their income taxes on the case's own keys instead of the
 *                       white lane's (white_replacement_2026_09_28/derived/limits_oct07.csv, arm g3_rate_mix, the
 *                       accrual basis for the set and the cash basis for the cash set; read, not recomputed):
 *                       case_w_income_tax_keys at the shared allocation, case_w_income_tax_keys_personal at the
 *                       personal, each the same at both ends. A cost move of +x is a receipt shift of -x on
 *                       federal_income_tax (response 1, no capital component keys it), expanded to every incidence
 *                       rule (row4_oct07.cjs:232-234). At another lineage option the move scales with W's count
 *                       [APPROX: the per-person move at the case's age mix, also at an age-mix arm].
 *   row4_frame          the five v4 items that summed published CPS weights where the account prices audit row 4's
 *                       39.71M (row4_class_2026_09_29/RESULT.md), on the union and on the lineage's added people, set
 *                       only where they touch the pension switch:
 *     union (the identified 39.71M; row4_oct07.cjs:185-207, unionEdits on the September 29 payload model U)
 *       owner              the owner-occupied property cell at the reference rule times (1/kappa - 1), kappa the
 *                          decomposition lane's (summary_sept29.json v4.kappas);
 *       part_a             Part A accrual at row 4 less at published weights (the Trustees arm), set only;
 *       benefit_tax        the tax on the group's benefits, published less row-4 receipt, on federal_income_tax, set only;
 *       state_index        the three state-price lines times (index ratio - 1); sales and licences by the factor change
 *                          over (1 + the published factor) (derived/row4_state_index.json);
 *       oasdi_ratio        (ratio_net at row 4, with the row-4 relative rate, less at published) x the union's OASDI
 *                          receipts, set only;
 *     lineage (the 3.04M added people; :208-231, item added_age_mix's part models at the case's counts)
 *       part_a_split       G's Part A x f_pa x the generation split's G3+ change in Part A (dPA), set only;
 *       ss_split           G's Social Security x f_ss at row 4 x the split's G3+ change (dSS), set only;
 *       ss_factor          the lineage's Social Security (G's and W's) x (f_ss at row 4 - f_ss), set only;
 *       state_index        G's state-price cells, sales and licences as the union's;
 *       owner_national_key G's owner cell x (n / n4 - 1);
 *       benefit_tax        G's tax on benefits x (the national key's ratio - 1), W's x the white lane's rule-3 ratio
 *                          less 1, set only;
 *     G = the G3+-priced members (later losses and (1 - C3) of the G3-rate attriters), W = C3 x the G3-rate attriters.
 *   The lane measures the pension components on the Trustees arm (separate funds). At item pension_tr2026's
 *   combined_funds arm, whose block has the same Part A, f_pa and Part A share but another OASDI level, oasdi_ratio
 *   scales by the arm's ratio_net over the Trustees arm's and ss_split and ss_factor by its f_ss over v6's [APPROX: the
 *   row-4 move taken as relative to the level; it differs from holding the Trustees arm's dollars by
 *   meta.row4_frame.pension_block.scaling_bn]. Any other pension block stops.
 *
 *   parts  <group>:<component>:<line>:<scenario or key>, group union_G1 | union_G2 | union_G3plus | lineage_g3plus |
 *          lineage_whites. The lane prices the union whole; here its components go to generations by the rule the
 *          case's generation split uses (generation_account_2026_09_24, convention a): owner and state_index on each
 *          generation's own cells of the September 29 generation models (they add to the union's, gated), part_a,
 *          oasdi_ratio and benefit_tax by the split's pension shares (v4_split.cjs:300-313: Part A per HI tax dollar x
 *          HI receipts, net accrual per tax dollar x OASDI receipts, each generation's tax on benefits) at each
 *          weighting, a generation's change being its row-4 share of the row-4 total less its published share of the
 *          published total. Each edit's union parts add to the lane's union formula (1e-9).
 *   edits  one cell shift per cell, receipts expanded over the incidence rules by the case's expand (as the lane does);
 *          each edit's by is its parts' sum, in order, so the parts add to it exactly.
 *
 * buildWhite / buildRow4 (ctx, arm, which) -> the edit set (package.cjs's contract). Run nothing: a module.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.join(__dirname, "..");
const V6 = require(path.join(FISCAL, "main_case_2026_10_07", "package.cjs"));
const { Engine, MODEL } = V6;
const V4 = V6.V4PKG;
const ROW4 = "row4_class_2026_09_29";
const WHITE = "white_replacement_2026_09_28";
const GEN = "generation_account_2026_09_24/derived";
const FILES = {
  state_index: `${ROW4}/derived/row4_state_index.json`, price_rekeys: `${ROW4}/derived/price_rekeys.json`,
  inputs: `${ROW4}/derived/row4_oct07_inputs.json`, oracle: `${ROW4}/derived/row4_oct07.json`,
  kappa: "main_case_decomposition_2026_09_29/derived/summary_sept29.json", limits: `${WHITE}/derived/limits_oct07.csv`,
  generations_set: `${GEN}/generation_corrections_sept29.json`, generations_cash: `${GEN}/generation_corrections_sept29_cash.json`,
};
const PORTED = `${ROW4}/row4_oct07.cjs`;
const REF = MODEL.receipts.reference;
const ALLOCS = ["personal", "shared"];
const GENS = ["G1", "G2", "G3plus"];
const SETS = ["set", "cash"];
const clone = (x) => JSON.parse(JSON.stringify(x));
const byAlloc = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
const isNum = (x) => typeof x === "number" && Number.isFinite(x);
const readText = (rel) => fs.readFileSync(path.join(FISCAL, rel), "utf8");
const readJson = (rel) => JSON.parse(readText(rel));
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const blockedIn = (item) => (why) => { throw new Error(`[BLOCKED] item ${item}: ${why}`); };
const blocked = blockedIn("row4_frame / white_end_tax_keys");
const lineOf = (m, side, id) => { const l = m[side].lines.find((x) => x.id === id); if (!l) blocked(`no ${side} line ${id}`); return l; };
const sCell = (m, id, key) => { const l = lineOf(m, "spending", id); return l.keys[key || l.preferred_key]; };
const rCell = (m, id, sc) => lineOf(m, "receipts", id).cells[sc || REF];
const amt = (cell) => byAlloc((a) => cell[a].target_bn);

// ---------------------------------------------------------------------------------------------------
// The lane's inputs (row4_oct07.cjs:42-50, :108-180), read once and checked as the lane checks them.
const SI = readJson(FILES.state_index), PR4 = readJson(FILES.price_rekeys), IN = readJson(FILES.inputs), ORACLE = readJson(FILES.oracle);
const SUMDEC = readJson(FILES.kappa);
for (const [k, x] of [["state_index", SI], ["inputs", IN]]) if (!Array.isArray(x.gates_failed) || x.gates_failed.length) blocked(`${FILES[k]} records failed gates`);
for (const [k, x] of [["price_rekeys", PR4], ["oracle", ORACLE]]) if (x.gates_failed !== 0) blocked(`${FILES[k]} records failed gates`);
const PEN = IN.pension, BTX = IN.benefit_tax;
const C0 = PEN.results.control.published, C4 = PEN.results.control.row4, A0 = PEN.results.arm.published, A4 = PEN.results.arm.row4;
const BW0 = BTX.weights.published, BW4 = BTX.weights.row4;
const PP6 = V6.correctionsPayload().meta.pension_accrual;
if (!(PP6.ratio_net === A0.ratio_net && PP6.part_a_accrual_bn === A0.part_a_bn)) blocked("v6's ratio_net and Part A are not the Trustees arm's at published weights (row4_oct07.cjs:112)");
const netOwn = (x, g, rel) => x.groups[g].per_tax_dollar * (1 - rel * x.groups[g].timing);
const fSS0 = A0.groups.G3plus.net_own_rate / C0.groups.G3plus.net_own_rate;
const fPA0 = A0.groups.G3plus.part_a_per_hi_tax_dollar / C0.groups.G3plus.part_a_per_hi_tax_dollar;
if (!(Math.abs(fSS0 - PP6.lineage_factors.f_ss) <= 1e-15 && Math.abs(fPA0 - PP6.lineage_factors.f_pa) <= 1e-15)) blocked("v6's lineage factors are not the reruns' (row4_oct07.cjs:120)");
const fSS4 = netOwn(A4, "G3plus", BW4.groups.G3plus.relative_rate) / netOwn(C4, "G3plus", BW4.groups.G3plus.relative_rate);
const fPA4 = A4.groups.G3plus.part_a_per_hi_tax_dollar / C4.groups.G3plus.part_a_per_hi_tax_dollar;
if (fPA4 !== fPA0) blocked("f_pa moves on row 4 (row4_oct07.cjs:123)");
const rn = { pub: A0.ratio_net, row4: netOwn(A4, "union", BW4.groups.union.relative_rate) };
if (Math.abs(netOwn(C4, "union", BW4.groups.union.relative_rate) - PR4.oasdi_ratio.row4) > 1e-12) blocked("v4's row-4 ratio_net is not price_rekeys.json's (row4_oct07.cjs:126)");
const partA = { pub: A0.part_a_bn, row4: A4.part_a_bn };
const btBy = byAlloc((a) => BW0.alloc[a].receipt_bn - BW4.alloc[a].receipt_bn);
if (!ALLOCS.every((a) => Math.abs(btBy[a] - PR4.benefit_tax_by[a]) <= 1e-12)) blocked("the benefit-tax move is not v4's (row4_oct07.cjs:129)");
const KAPPA = SUMDEC.v4.kappas.low.modeled_owner_property;
if (KAPPA !== PR4.kappa_owner) blocked("kappa is not price_rekeys.json's (row4_oct07.cjs:131)");
for (const line of Object.keys(SI.lines)) if (Math.abs(SI.lines[line].sp_pre_published_bn - V4.SP_PRE[line]) > 1e-6) blocked(`SP_PRE ${line} is not the package's (row4_oct07.cjs:132)`);
for (const r of ["general_sales_tax", "personal_motor_vehicle"]) if (Math.abs(SI.receipts[r].factor_published - V4.SP_RECEIPT[r].factor) > 1e-9) blocked(`receipt factor ${r} is not the package's (row4_oct07.cjs:133)`);
const SP_SYN = { public_order_safety: "state_price_public_order_safety", health_services: "state_price_health_services", recreation_culture: "state_price_recreation_culture" };
if (JSON.stringify(Object.keys(SI.lines).sort()) !== JSON.stringify(Object.keys(SP_SYN).sort())) blocked("row4_state_index.json's lines are not the three state-price parents");
const SR = ["general_sales_tax", "personal_motor_vehicle"];
const OWNER = "modeled_owner_property", FIT = "federal_income_tax";

// The generation split's inputs (row4_oct07.cjs:136-163): the September 29 generation models, convention a.
const GP = { set: readJson(FILES.generations_set), cash: readJson(FILES.generations_cash) };
const GM = Object.fromEntries(SETS.map((w) => [w, Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(readJson(`${GEN}/model_${g}.json`), GP[w].payloads.a[g])]))]));
const U4M = { set: V6.SEPT29.payloadModel(), cash: V6.SEPT29_CASH.payloadModel() };
for (const w of SETS) if (GP[w].meta.union !== V6.BASE_FILES[w]) blocked(`${FILES[`generations_${w}`]} splits ${GP[w].meta.union}, not ${V6.BASE_FILES[w]}`);
const Rg = Object.fromEntries(GENS.map((g) => [g, V4.hiOf(GM.set[g])])), Og = Object.fromEntries(GENS.map((g) => [g, V4.oasdiOf(GM.set[g])]));
const RU = V4.hiOf(U4M.set), OU = V4.oasdiOf(U4M.set);
if (!ALLOCS.every((a) => Math.abs(GENS.reduce((s, g) => s + Rg[g][a], 0) - RU[a]) <= 1e-9 && Math.abs(GENS.reduce((s, g) => s + Og[g][a], 0) - OU[a]) <= 1e-9)) {
  blocked("the generations' HI and OASDI receipts do not add to the union's (row4_oct07.cjs:142)");
}
const rho = (x, g) => x.groups[g].part_a_bn / x.groups[g].hi_tax_bn;
const Wa = (x) => byAlloc((a) => GENS.reduce((s, g) => s + rho(x, g) * Rg[g][a], 0));
const nr = (x, W, g) => netOwn(x, g, W.groups[g].relative_rate);
const Wt = (x, W) => byAlloc((a) => GENS.reduce((s, g) => s + nr(x, W, g) * Og[g][a], 0));
const Wa0 = Wa(C0), Wa4 = Wa(C4), Wt0 = Wt(C0, BW0), Wt4 = Wt(C4, BW4);
const g3PartA = (T, x, W_) => byAlloc((a) => T * rho(x, "G3plus") * Rg.G3plus[a] / W_[a]);
const g3SS = (r, x, W, W_) => byAlloc((a) => r * OU[a] * nr(x, W, "G3plus") * Og.G3plus[a] / W_[a]);
const pa0 = g3PartA(C0.part_a_bn, C0, Wa0), ss0 = g3SS(C0.ratio_net, C0, BW0, Wt0);
const pa4 = g3PartA(C4.part_a_bn, C4, Wa4), ss4 = g3SS(netOwn(C4, "union", BW4.groups.union.relative_rate), C4, BW4, Wt4);
const dPA = byAlloc((a) => pa4[a] / pa0[a] - 1), dSS = byAlloc((a) => ss4[a] / ss0[a] - 1);
const nk = byAlloc((a) => BW0.alloc[a].national_key_census_bn / BW4.alloc[a].national_key_census_bn);
// White lane rule 3 (row4_oct07.cjs:165-167): on row 4 the shared receipt and the union's relative rate move.
const kW = (BW4.alloc.shared.receipt_bn / BW0.alloc.shared.receipt_bn) * (BW0.groups.union.relative_rate / BW4.groups.union.relative_rate);
// The owner line's national key on row 4 (row4_oct07.cjs:168-172).
const ownM = rCell(MODEL, OWNER);
if (ownM.personal.target_bn !== ownM.shared.target_bn) blocked("the owner cell's share differs by allocation in model.json (row4_oct07.cjs:171)");
const sOwn = ownM.shared.target_bn / lineOf(MODEL, "receipts", OWNER).national_bn;
const yOwn = sOwn * (1 - 1 / KAPPA) / (1 - sOwn / KAPPA), nOwn = 1 / (1 - yOwn);
// The union's pension and benefit-tax totals by generation, by the split's shares (v4_split.cjs:300-313) at each weighting.
const SPLIT = {
  part_a: Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => A4.part_a_bn * rho(A4, g) * Rg[g][a] / Wa(A4)[a] - A0.part_a_bn * rho(A0, g) * Rg[g][a] / Wa(A0)[a])])),
  oasdi_ratio: Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => OU[a] * (rn.row4 * nr(A4, BW4, g) * Og[g][a] / Wt(A4, BW4)[a] - rn.pub * nr(A0, BW0, g) * Og[g][a] / Wt(A0, BW0)[a]))])),
  benefit_tax: Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => BW0.alloc[a].receipt_bn * BW0.alloc[a].by_generation_benefit_tax_bn[g] / BW0.alloc[a].group_benefit_tax_bn
    - BW4.alloc[a].receipt_bn * BW4.alloc[a].by_generation_benefit_tax_bn[g] / BW4.alloc[a].group_benefit_tax_bn)])),
};
for (const G of GENS) for (const W of [BW0, BW4]) for (const a of ALLOCS) if (!isNum(W.alloc[a].by_generation_benefit_tax_bn[G])) blocked("the benefit-tax rerun lacks a generation");
const INPUTS = { rn: { pub: rn.pub, row4: rn.row4 }, partA: clone(partA), btBy: clone(btBy), kappa_owner: KAPPA, fSS0, fSS4, fPA0, fPA4, delta_part_a: dPA, delta_ss: dSS,
  national_key_ratio: nk, white_rule3_ratio: kW, owner_national_ratio: nOwn };

// The white end's rows (row4_oct07.cjs:173-180): the file's arm g3_rate_mix, each basis and allocation the same at both ends.
const LIM = (() => {
  const [head, ...rs] = readText(FILES.limits).trim().split("\n").map((l) => l.split(","));
  return rs.map((r) => Object.fromEntries(head.map((k, i) => [k, r[i]])));
})();
const W_ARM = "g3_rate_mix", W_ITEM = { shared: "case_w_income_tax_keys", personal: "case_w_income_tax_keys_personal" }, W_BASIS = { set: "accrual", cash: "cash" };
const W_ROWS = Object.fromEntries(SETS.map((w) => [w, byAlloc((a) => {
  const rs = LIM.filter((r) => r.item === W_ITEM[a] && r.arm === W_ARM && r.basis === W_BASIS[w]);
  if (rs.length !== 2 || JSON.stringify(rs.map((r) => r.end).sort()) !== JSON.stringify(["high", "low"]) || rs[0].bn !== rs[1].bn || rs[0].per_person_usd !== rs[1].per_person_usd) {
    blocked(`${FILES.limits}: ${W_ITEM[a]} (${W_ARM}, ${W_BASIS[w]}) is not one value at both ends`);
  }
  return { bn: Number(rs[0].bn), per_person_usd: Number(rs[0].per_person_usd), count: Number(rs[0].count) };
})]));
const CASE_COUNTS = clone(V6.ITEM_DETAIL.added_age_mix.counts);
const W_CASE = CASE_COUNTS.c3 * CASE_COUNTS.g3_rate;
const nWhite = V6.correctionsPayload().meta.lineage.members.white;
if (!(Math.abs(W_CASE - nWhite) <= 1e-6)) blocked(`W's count ${W_CASE} is not the payload's members.white ${nWhite}`);
if (!SETS.every((w) => ALLOCS.every((a) => Math.abs(W_ROWS[w][a].count - nWhite) <= 5e-5))) blocked(`${FILES.limits}'s W count is not the payload's members.white (four decimals; row4_oct07.cjs:180)`);
const SOURCES_7 = { lane: WHITE, file: FILES.limits, sha256: sha256(FILES.limits), rows: { arm: W_ARM, items: W_ITEM, basis: W_BASIS }, ported: `${PORTED}:173-180, :232-234` };
const INPUT_FILES = [FILES.state_index, FILES.price_rekeys, FILES.inputs, FILES.kappa, FILES.generations_set, FILES.generations_cash].concat(GENS.map((g) => `${GEN}/model_${g}.json`));
const SOURCES_8 = { lane: ROW4, file: FILES.inputs, sha256: sha256(FILES.inputs), files: Object.fromEntries(INPUT_FILES.map((f) => [f, sha256(f)])),
  oracle: { file: FILES.oracle, sha256: sha256(FILES.oracle) }, ported: `${PORTED}:108-231` };

// ---------------------------------------------------------------------------------------------------
// The lineage's parts on item added_age_mix's part models (row4_oct07.cjs:89-98) at the context's counts.
function lineageOf(ctx) {
  const D = ctx.DETAIL && ctx.DETAIL.added_age_mix;
  if (!D || !D.counts || !D.part_models || !D.part_models.set || !D.part_models.cash) {
    blocked("the added people's G3+ and white parts come from the lineage item added_age_mix's part models and counts; a case without it has no rule here");
  }
  const { later, g3_rate, c3 } = D.counts;
  const part = (w, kind, side, id, key) => {
    const pm = D.part_models[w], get = (m) => (side === "spending" ? sCell(m, id, key) : rCell(m, id, key));
    if (kind === "G") return byAlloc((a) => later * get(pm.later)[a].target_bn + (1 - c3) * g3_rate * get(pm.g3_rate)[a].target_bn);
    return byAlloc((a) => c3 * g3_rate * get(pm.white_g3_rate)[a].target_bn);
  };
  return { D, part, counts: { later, g3_rate, c3 }, w_count: c3 * g3_rate };
}

// The cells, in order of first use: each cell's parts in order; an edit's by is their sum.
function collector() {
  const cells = new Map();
  const add = (side, line, at, name, by) => {
    const k = `${side}|${line}|${at}`;
    if (!cells.has(k)) cells.set(k, { e: side === "receipt" ? { side, line, scenario: at } : { side, line, key: at }, parts: [] });
    const c = cells.get(k);
    if (c.parts.some(([n]) => n === name)) blocked(`two parts named ${name}`);
    c.parts.push([name, { personal: by.personal, shared: by.shared }]);
  };
  const out = () => {
    const edits = [], parts = {};
    for (const { e, parts: ps } of cells.values()) {
      const j = edits.length, by = { personal: 0, shared: 0 };
      for (const [name, b] of ps) { parts[name] = { edit: j, by: b }; for (const a of ALLOCS) by[a] += b[a]; }
      edits.push(Object.assign(clone(e), { by }));
    }
    return { edits, parts };
  };
  return { add, out };
}
// A receipt shift at the reference rule, expanded to every rule as the case expands it (row4_oct07.cjs uses V6.expand).
const expandReceipt = (line, by) => V6.expand([{ side: "receipt", line, by }]);

// ---------------------------------------------------------------------------------------------------
// Item white_end_tax_keys.
function buildWhite(ctx, arm, which) {
  const block = blockedIn("white_end_tax_keys");
  if (arm) block(`no arm ${arm}`);
  const lin = lineageOf(ctx);
  // The case's count gives scale 1 exactly (the same product of the same counts).
  const scale = lin.w_count === W_CASE ? 1 : lin.w_count / W_CASE;
  const rows = W_ROWS[which];
  const move = byAlloc((a) => rows[a].bn * scale);
  const edits = expandReceipt(FIT, byAlloc((a) => -move[a]));
  const parts = Object.fromEntries(edits.map((e, j) => [`lineage_whites:income_tax_keys:${e.line}:${e.scenario}`, { edit: j, by: clone(e.by) }]));
  const rule = "W, the lineage members priced as third-plus non-Hispanic whites (C3 x the G3-rate attriters), with their income taxes on the case's own keys: the white lane's move (limits_oct07.csv, arm g3_rate_mix; case_w_income_tax_keys at the shared allocation, case_w_income_tax_keys_personal at the personal) as a receipt shift of minus the move on federal_income_tax, expanded to every incidence rule";
  const blk = {
    rule, members: "W = C3 x the G3-rate attriters (meta.lineage.members.white)", count: lin.w_count, case_count: W_CASE, scale,
    move_bn: clone(move), per_person_usd: byAlloc((a) => rows[a].per_person_usd), basis: W_BASIS[which], arm: W_ARM,
    option_rule: "[APPROX] at another lineage option the move is the file's times W's count over the case's (the per-person move at the case's age mix, also at an age-mix arm)",
    sign: "move_bn is the change in the cost to other residents (+ = dearer); the edits are minus it on the group's federal_income_tax targets",
    source: clone(SOURCES_7),
  };
  return {
    edits, parts, meta: { white_end_tax_keys: blk },
    record: { rule: "item_row4.cjs buildWhite: the white lane's move on W's income taxes as one receipt shift, expanded", parts_rule: "one part per edit, lineage_whites:income_tax_keys:federal_income_tax:<scenario>: the added people's W",
      count: lin.w_count, scale, move_bn: clone(move), basis: W_BASIS[which], source: { file: SOURCES_7.file, sha256: SOURCES_7.sha256 } },
    detail: { move_bn: clone(move), scale, count: lin.w_count },
  };
}

// ---------------------------------------------------------------------------------------------------
// Item row4_frame.
const UNION_COMPONENTS = ["owner", "part_a", "benefit_tax", "state_index", "oasdi_ratio"];
const LINEAGE_COMPONENTS = ["part_a_split", "ss_split", "ss_factor", "state_index", "owner_national_key", "benefit_tax"];
const SET_ONLY = { union: ["part_a", "benefit_tax", "oasdi_ratio"], lineage: ["part_a_split", "ss_split", "ss_factor", "benefit_tax"] };
function buildRow4(ctx, arm, which) {
  const block = blockedIn("row4_frame");
  if (arm) block(`no arm ${arm}`);
  const { B } = ctx;
  const api = which === "set" ? B : B.CASH;
  const m = api.payloadModel();
  if (!B.SEPT29 || !B.SEPT29_CASH || B.SEPT29 !== V6.SEPT29) block("the case's union is not the September 29 payload this item reads");
  // Part A, the OASDI ratio and the lineage's f_ss correct v6's pension block (item pension_tr2026's Trustees arm, on
  // which the lane measures them). A named pension_tr2026 arm with the same Part A block and another OASDI level takes
  // the OASDI components at its level (kRN, kSS) [APPROX]; any other block stops.
  let kRN = 1, kSS = 1, pensionBlock = null;
  if (which === "set") {
    const pa = B.correctionsPayload().meta.pension_accrual, lf = pa && pa.lineage_factors;
    if (!(pa && lf && pa.part_a_accrual_bn === A0.part_a_bn && lf.f_pa === PP6.lineage_factors.f_pa && pa.part_a_share === PP6.part_a_share && isNum(pa.ratio_net) && isNum(lf.f_ss))) {
      block("the case's pension block is not item pension_tr2026's (its Part A accrual, f_pa and Part A share), on which the item's Part A, OASDI-ratio and f_ss components are measured");
    }
    const ptArm = (B.ITEM_IDS || []).includes("pension_tr2026") ? (B.ITEM_ARMS || {}).pension_tr2026 || null : null;
    kRN = pa.ratio_net / A0.ratio_net; kSS = lf.f_ss / PP6.lineage_factors.f_ss;
    if ((kRN !== 1 || kSS !== 1) && !ptArm) block("the case's OASDI level is not the Trustees arm's and no pension_tr2026 arm names it");
    pensionBlock = { arm: ptArm, ratio_net: pa.ratio_net, f_ss: lf.f_ss, k_ratio_net: kRN, k_f_ss: kSS, scaling_bn: null,
      rule: ptArm ? "[APPROX] the lane measures the pension components on the Trustees arm; at this arm (the same Part A block) oasdi_ratio scales by k_ratio_net (the arm's ratio_net over the Trustees arm's) and ss_split and ss_factor by k_f_ss (the arm's f_ss over v6's): the row-4 move taken as relative to the level; scaling_bn is the change from holding the Trustees arm's dollars"
        : "the Trustees arm (separate funds), on which the lane measures the pension components" };
  }
  const U = U4M[which], G = GM[which], lin = lineageOf(ctx), part = lin.part;
  const ssKey = lineOf(m, "spending", "social_security").preferred_key, medKey = lineOf(m, "spending", "medicare").preferred_key;
  if (ssKey !== lineOf(U, "spending", "social_security").preferred_key || medKey !== lineOf(U, "spending", "medicare").preferred_key) block("the case's Social Security or Medicare key is not the union's");
  const C = collector(), add = C.add;
  const isSet = which === "set";
  let unionGap = 0, genCells = 0;
  // A union component: the lane's union amount on U and its generations' parts, which must add to it.
  const unionEdit = (side, line, at, comp, union, byGen) => {
    for (const a of ALLOCS) unionGap = Math.max(unionGap, Math.abs(GENS.reduce((t, g) => t + byGen[g][a], 0) - union[a]));
    for (const g of GENS) add(side, line, at, `union_${g}:${comp}:${line}:${at}`, byGen[g]);
  };
  const unionReceipt = (line, comp, union, byGen) => {
    const e = expandReceipt(line, union), eg = Object.fromEntries(GENS.map((g) => [g, expandReceipt(line, byGen[g])]));
    e.forEach((x, j) => unionEdit("receipt", line, x.scenario, comp, x.by, Object.fromEntries(GENS.map((g) => [g, eg[g][j].by]))));
  };
  const lineageReceipt = (group, line, comp, by) => { for (const x of expandReceipt(line, by)) add("receipt", line, x.scenario, `${group}:${comp}:${line}:${x.scenario}`, x.by); };
  // The generation models' cells add to the union's on every line the item edits (row4_oct07.cjs:99-106 for the lineage).
  const genCheck = (side, id, key) => {
    const u = side === "spending" ? sCell(U, id, key) : rCell(U, id, key), gs = GENS.map((g) => (side === "spending" ? sCell(G[g], id, key) : rCell(G[g], id, key)));
    for (const a of ALLOCS) genCells = Math.max(genCells, Math.abs(gs.reduce((t, c) => t + c[a].target_bn, 0) - u[a].target_bn));
  };
  // Union (row4_oct07.cjs:185-207).
  {
    genCheck("receipt", OWNER);
    const u = amt(rCell(U, OWNER));
    unionEdit("receipt", OWNER, REF, "owner", byAlloc((a) => -u[a] * (1 - 1 / KAPPA)), Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => -rCell(G[g], OWNER)[a].target_bn * (1 - 1 / KAPPA))])));
  }
  if (isSet) {
    genCheck("spending", "medicare");
    unionEdit("spending", "medicare", medKey, "part_a", byAlloc(() => partA.row4 - partA.pub), SPLIT.part_a);
    genCheck("receipt", FIT);
    unionReceipt(FIT, "benefit_tax", btBy, SPLIT.benefit_tax);
  }
  for (const [line, syn] of Object.entries(SP_SYN)) {
    genCheck("spending", syn, "k");
    const r = SI.lines[line].ratio;
    unionEdit("spending", syn, "k", "state_index", byAlloc((a) => sCell(U, syn, "k")[a].target_bn * (r - 1)), Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => sCell(G[g], syn, "k")[a].target_bn * (r - 1))])));
  }
  for (const id of SR) {
    genCheck("receipt", id);
    const x = SI.receipts[id], f = (c) => byAlloc((a) => (x.factor_row4 - x.factor_published) * c[a].target_bn / (1 + x.factor_published));
    unionReceipt(id, "state_index", f(rCell(U, id)), Object.fromEntries(GENS.map((g) => [g, f(rCell(G[g], id))])));
  }
  if (isSet) {
    genCheck("spending", "social_security");
    const oasdi = V4.oasdiOf(U);
    unionEdit("spending", "social_security", ssKey, "oasdi_ratio", byAlloc((a) => (rn.row4 - rn.pub) * oasdi[a] * kRN),
      Object.fromEntries(GENS.map((g) => [g, byAlloc((a) => SPLIT.oasdi_ratio[g][a] * kRN)])));
    pensionBlock.scaling_bn = byAlloc((a) => (rn.row4 - rn.pub) * oasdi[a] * (kRN - 1));
  }
  if (!(unionGap < 1e-9)) block(`${which}: the union's generation parts do not add to the lane's union amounts (${unionGap})`);
  if (!(genCells < 1e-9)) block(`${which}: the generation models' cells do not add to the union's on the lines the item edits (${genCells})`);
  // Lineage (row4_oct07.cjs:208-231).
  const G_SS = part("set", "G", "spending", "social_security"), W_SS = part("set", "W", "spending", "social_security");
  const G_PA = byAlloc((a) => part("set", "G", "spending", "medicare")[a] - (1 - PP6.part_a_share) * part("cash", "G", "spending", "medicare")[a]);
  const G_BT = byAlloc((a) => part("set", "G", "receipt", FIT)[a] - part("cash", "G", "receipt", FIT)[a]);
  const W_BT = byAlloc((a) => part("set", "W", "receipt", FIT)[a] - part("cash", "W", "receipt", FIT)[a]);
  if (isSet) {
    add("spending", "medicare", medKey, `lineage_g3plus:part_a_split:medicare:${medKey}`, byAlloc((a) => G_PA[a] * fPA0 * dPA[a]));
    add("spending", "social_security", ssKey, `lineage_g3plus:ss_split:social_security:${ssKey}`, byAlloc((a) => G_SS[a] * fSS4 * dSS[a] * kSS));
    add("spending", "social_security", ssKey, `lineage_g3plus:ss_factor:social_security:${ssKey}`, byAlloc((a) => G_SS[a] * (fSS4 - fSS0) * kSS));
    add("spending", "social_security", ssKey, `lineage_whites:ss_factor:social_security:${ssKey}`, byAlloc((a) => W_SS[a] * (fSS4 - fSS0) * kSS));
    for (const a of ALLOCS) pensionBlock.scaling_bn[a] += (G_SS[a] * fSS4 * dSS[a] + (G_SS[a] + W_SS[a]) * (fSS4 - fSS0)) * (kSS - 1);
  }
  for (const [line, syn] of Object.entries(SP_SYN)) {
    add("spending", syn, "k", `lineage_g3plus:state_index:${syn}:k`, byAlloc((a) => part(which, "G", "spending", syn, "k")[a] * (SI.lines[line].ratio - 1)));
  }
  for (const id of SR) {
    const x = SI.receipts[id], g = part(which, "G", "receipt", id);
    lineageReceipt("lineage_g3plus", id, "state_index", byAlloc((a) => (x.factor_row4 - x.factor_published) * g[a] / (1 + x.factor_published)));
  }
  add("receipt", OWNER, REF, `lineage_g3plus:owner_national_key:${OWNER}:${REF}`, byAlloc((a) => part(which, "G", "receipt", OWNER)[a] * (nOwn - 1)));
  if (isSet) {
    lineageReceipt("lineage_g3plus", FIT, "benefit_tax", byAlloc((a) => G_BT[a] * (nk[a] - 1)));
    lineageReceipt("lineage_whites", FIT, "benefit_tax", byAlloc((a) => W_BT[a] * (kW - 1)));
  }
  // The lineage's G and W parts add to its addition on every cell they read (row4_oct07.cjs:99-106): the base's lineage
  // model less the September 29 union, before v6's items.
  let worstLin = 0;
  const LB = B.ITEM_BASE;
  if (!LB || typeof LB.payloadModel !== "function") block("the case has no lineage base (ITEM_BASE) to check the added people's parts against");
  const LM = { set: LB.payloadModel(), cash: LB.CASH.payloadModel() };
  for (const w of SETS) {
    for (const [side, id, key] of [["spending", "social_security"], ["spending", "medicare"], ...Object.values(SP_SYN).map((s) => ["spending", s, "k"]), ...[OWNER, FIT, ...SR].map((r) => ["receipt", r])]) {
      const g = part(w, "G", side, id, key), x = part(w, "W", side, id, key), get = (mm) => (side === "spending" ? sCell(mm, id, key) : rCell(mm, id, key));
      for (const a of ALLOCS) worstLin = Math.max(worstLin, Math.abs(g[a] + x[a] - (get(LM[w])[a].target_bn - get(U4M[w])[a].target_bn)));
    }
  }
  if (!(worstLin < 1e-9)) block(`the lineage's G and W parts do not add to its addition on the cells the item reads (${worstLin})`);
  const { edits, parts } = C.out();
  for (const e of edits) {
    const has = e.side === "receipt" ? (m.receipts.lines.find((l) => l.id === e.line) || { cells: {} }).cells[e.scenario] : (m.spending.lines.find((l) => l.id === e.line) || { keys: {} }).keys[e.key];
    if (!has) block(`${which}: the case has no ${e.side} cell ${e.line}/${e.scenario || e.key}`);
  }
  const components = { union: UNION_COMPONENTS.filter((c) => isSet || !SET_ONLY.union.includes(c)), lineage: LINEAGE_COMPONENTS.filter((c) => isSet || !SET_ONLY.lineage.includes(c)) };
  const RULES = {
    owner: "the owner-occupied property cell at the reference rule times (1/kappa - 1): the union's share of the national key on row 4 (kappa, the decomposition lane's)",
    part_a: "Part A accrual at row 4 less at published weights (the Trustees arm), set only",
    benefit_tax: "the tax on the group's benefits at published less row-4 weights, on federal_income_tax, expanded; set only",
    state_index: "the three state-price lines times (the row-4 index ratio - 1); general sales and licences by the factor change over (1 + the published factor), expanded",
    oasdi_ratio: "(ratio_net at row 4, with the row-4 relative rate, less at published) x the union's OASDI receipts; set only",
    part_a_split: "G's Part A x f_pa x dPA (the generation split's G3+ Part A at row 4 over at published, less 1); set only",
    ss_split: "G's Social Security x f_ss at row 4 x dSS (the split's G3+ Social Security at row 4 over at published, less 1); set only",
    ss_factor: "the lineage's Social Security, G's and W's, x (f_ss at row 4 - f_ss): G3+'s own rate on row 4; set only",
    owner_national_key: "G's owner cell x (n / n4 - 1), the national key's change on row 4",
    benefit_tax_lineage: "G's tax on benefits x (the national key's ratio - 1); W's x (the white lane's rule-3 ratio - 1); set only",
  };
  const blk = {
    rule: "the five v4 items that summed published CPS weights where the account prices audit row 4's 39.71M, on the union and the lineage's added people, as the row-4 class lane prices them on v6 (row4_class_2026_09_29/row4_oct07.cjs): fixed cell shifts, receipts expanded to every incidence rule",
    components: { union: Object.fromEntries(UNION_COMPONENTS.map((c) => [c, RULES[c]])), lineage: Object.fromEntries(LINEAGE_COMPONENTS.map((c) => [c, RULES[c === "benefit_tax" ? "benefit_tax_lineage" : c]])) },
    components_applied: clone(components), set_only: clone(SET_ONLY),
    generation_rule: "the union's components by generation: owner and state_index on each generation's own cells (the September 29 generation models, convention a); part_a, oasdi_ratio and benefit_tax by the case's generation split's pension shares (generation_account_2026_09_24/v4_split.cjs:300-313: Part A per HI tax dollar x HI receipts, net accrual per tax dollar x OASDI receipts, the generations' tax on benefits) at each weighting; G = the G3+-priced added people, W the white-priced",
    values: clone(INPUTS), counts: clone(lin.counts), pension_block: clone(pensionBlock),
    sign: "each part's by is the change to the group's target on its line (spending: + = dearer; receipts: + = more paid)",
    source: clone(SOURCES_8),
  };
  return {
    edits, parts, meta: { row4_frame: blk },
    record: { rule: "item_row4.cjs buildRow4: the row-4 class lane's union and lineage edits, merged into one cell shift per cell; the union's by generation", components_applied: clone(components),
      parts_rule: "union_<G>:<component>:<line>:<scenario or key> the identified union's generations; lineage_g3plus:... and lineage_whites:... the added people's; each edit's by is its parts' sum, in order",
      source: { file: SOURCES_8.file, sha256: SOURCES_8.sha256, oracle: clone(SOURCES_8.oracle) } },
    detail: { inputs: clone(INPUTS), lineage_inputs: { G_part_a: G_PA, G_ss: G_SS, lineage_ss: byAlloc((a) => G_SS[a] + W_SS[a]), G_benefit_tax: G_BT, W_benefit_tax: W_BT },
      union_gap_bn: unionGap, generation_cells_gap_bn: genCells, lineage_split_gap_bn: worstLin, split: clone(SPLIT), counts: clone(lin.counts) },
  };
}

module.exports = { buildWhite, buildRow4, ORACLE, FILES, INPUTS, SOURCES_7, SOURCES_8, W_ROWS, W_CASE, CASE_COUNTS, UNION_COMPONENTS, LINEAGE_COMPONENTS, SET_ONLY, PORTED };
