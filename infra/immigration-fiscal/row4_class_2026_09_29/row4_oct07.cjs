// Prices the row-4 class on main case v6 (oct07) through the adopted lane's package (evaluateFull at MAIN_SPECS[48] /
// [11]; the cash set through its CASH package), alone and together, with the white end's income-tax re-key beside.
// price_rekeys.cjs's five re-keys are applied to the union's part of each v6 cell (the September 29 payload model,
// which v6's lineage and items build on), plus the lineage's inherited part: the 3.04M added people take G3+ members'
// amounts (item added_age_mix's part models), and the generation split (generation_account_2026_09_24/v4_split.cjs)
// gives G3+ the union's published-weight pension totals and state indexes by rule. Recorded, not applied: the adopted
// case is unchanged.
//   union   owner        the union's reference cell over kappa (the decomposition lane's), as on v4
//           part_a       the Trustees arm's Part A at row 4 less at published (derived/row4_oct07_inputs.json)
//           benefit_tax  the receipt at row 4 less at published (v6 carries v4's receipt)
//           state_index  the union's synthetic lines x (ratio - 1); sales and licences by the factor change (v4's)
//           oasdi_ratio  (ratio_net at row 4, with the row-4 relative rate, less ratio_net) x the union's OASDI receipts
//   lineage part_a_split G's Part A x f_pa x delta_PA: the split's union total over its row-4 shares
//           ss_split     G's Social Security x f_ss' x delta_SS; ss_factor the lineage's x (f_ss' - f_ss), G3+'s own
//                        rate at row 4
//           state_index  G's synthetic lines x (ratio - 1); G's sales and licences by the factor change
//           owner_national_key G's owner cell x (n / n4 - 1)
//           benefit_tax  G's benefit tax x (national key ratio - 1); W's by the white lane's rule-3 ratio
//   white end            W's income taxes on the case's keys (white_replacement_2026_09_28/derived/limits_oct07.csv,
//                        arm g3_rate_mix; read, not recomputed), at the case's allocation: shared at spec 48, personal
//                        at spec 11; the accrual basis for the set, the cash basis for the cash set
// G = the G3+-priced members (later losses, and the G3-rate attriters' 1 - C3), W = the white end (C3 x G3-rate).
// Gates: the inputs passed; the oracles (v6's summary.json bands, 1e-9, and its per-member base, 1e-6; 48 / 11 are the
// bands' ends and the shared / personal allocations); v6's touched cells are the lineage base's; the inputs are the payload's; the split rebuilds
// G3+'s pension cells; the lineage's parts add to its addition; the owner move is v4's times the owner response's
// ratio; W's rows are one each, at the payload's white count, and W alone moves the case by them; the positive control
// (the union edits applied to v4 reproduce derived/price_rekeys.json's moves, 1e-9).
// Writes derived/row4_oct07.csv (moves and costs, $bn, six decimals) and derived/row4_oct07.json. Run from the
// repository root after row4_oct07.py and price_rekeys.cjs:
//   node infra/immigration-fiscal/row4_class_2026_09_29/row4_oct07.cjs
"use strict";
const fs = require("fs");
const path = require("path");
const F = path.resolve(__dirname, "..");
const OUT = path.join(__dirname, "derived");
const J = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const V6 = require(path.join(F, "main_case_2026_10_07/package.cjs"));
const P4 = require(path.join(F, "main_case_2026_09_29/package.cjs"));
const { Engine, MODEL } = V6;
const V4 = V6.V4PKG;
const L = V6.ITEM_BASE;
const S6 = J(path.join(F, "main_case_2026_10_07/derived/summary.json"));
const SUMDEC = J(path.join(F, "main_case_decomposition_2026_09_29/derived/summary_sept29.json"));
const SI = J(path.join(OUT, "row4_state_index.json")), PR4 = J(path.join(OUT, "price_rekeys.json"));
const IN = J(path.join(OUT, "row4_oct07_inputs.json"));
const PEN = IN.pension, BTX = IN.benefit_tax;
const LIM = (() => {
  const [head, ...rs] = fs.readFileSync(path.join(F, "white_replacement_2026_09_28/derived/limits_oct07.csv"), "utf8").trim().split("\n").map((l) => l.split(","));
  return rs.map((r) => Object.fromEntries(head.map((k, i) => [k, r[i]])));
})();
const REF = MODEL.receipts.reference;
const ENDS = [48, 11];
const ALLOCS = ["personal", "shared"];
const GENS = ["G1", "G2", "G3plus"];
const SETS = ["set", "cash"];
const byAlloc = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
let fails = 0;
const gate = (name, ok, detail) => { console.log(`GATE ${ok ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`); if (!ok) fails++; };
const lineOf = (m, side, id) => { const l = m[side].lines.find((x) => x.id === id); if (!l) throw new Error(`no ${side} line ${id}`); return l; };
const sCell = (m, id, key) => { const l = lineOf(m, "spending", id); return l.keys[key || l.preferred_key]; };
const rCell = (m, id, sc) => lineOf(m, "receipts", id).cells[sc || REF];
const amt = (cell) => byAlloc((a) => cell[a].target_bn);
const near = (a, b, t) => Math.abs(a - b) <= t;
gate("row4_oct07_inputs.json written with every gate passed", Array.isArray(IN.gates_failed) && IN.gates_failed.length === 0);

// ---------------------------------------------------------------- the case and its parts
const API = { set: V6, cash: V6.CASH };
const M = { set: V6.payloadModel(), cash: V6.CASH.payloadModel() };
const U4M = { set: L.SEPT29.payloadModel(), cash: L.SEPT29_CASH.payloadModel() };   // the union alone (v4's payload)
const LM = { set: L.payloadModel(), cash: L.CASH.payloadModel() };                    // v5 + the age-mix lineage
const costAt = (w, m) => ENDS.map((i) => API[w].evaluateFull(m, API[w].MAIN_SPECS[i]).cost_bn);
const base = { set: costAt("set", M.set), cash: costAt("cash", M.cash) };
gate("oracle: v6 set at specs 48 / 11 is summary.json's main_case (1e-9)", base.set.every((x, j) => near(x, S6.main_case[j], 1e-9)), base.set.map((x) => x.toFixed(6)).join(" / "));
gate("oracle: v6 cash set is summary.json's cash_set (1e-9)", base.cash.every((x, j) => near(x, S6.cash_set.band_bn[j], 1e-9)), base.cash.map((x) => x.toFixed(6)).join(" / "));
gate("the band ends are specs 48 / 11 (no other spec lower or higher)", SETS.every((w) => {
  const c = API[w].MAIN_SPECS.map((s) => API[w].evaluateFull(M[w], s).cost_bn);
  return Math.min(...c) >= base[w][0] - 1e-9 && Math.max(...c) <= base[w][1] + 1e-9;
}));
gate("specs 48 / 11 take the shared / personal allocations, set and cash", SETS.every((w) => API[w].MAIN_SPECS[48].allocation === "shared" && API[w].MAIN_SPECS[11].allocation === "personal"));
// v6's cells on the lines the class touches are the union's plus the lineage's (no v6 item edits them) except Social
// Security and Medicare, which item pension_tr2026 edits on the set.
const SP_SYN = { public_order_safety: "state_price_public_order_safety", health_services: "state_price_health_services", recreation_culture: "state_price_recreation_culture" };
const RCELLS = ["modeled_owner_property", "federal_income_tax", "general_sales_tax", "personal_motor_vehicle"];
for (const w of SETS) {
  const same = Object.values(SP_SYN).every((id) => JSON.stringify(sCell(M[w], id, "k")) === JSON.stringify(sCell(LM[w], id, "k")))
    && RCELLS.every((id) => JSON.stringify(lineOf(M[w], "receipts", id).cells) === JSON.stringify(lineOf(LM[w], "receipts", id).cells));
  gate(`${w}: v6's state-price, owner, income-tax, sales and licence cells are the lineage base's (no v6 item edits them)`, same);
}
// The lineage's parts: G (the G3+-priced members) and W (the white end), item added_age_mix's part models.
const D = V6.ITEM_DETAIL.added_age_mix;
const { later, g3_rate, c3 } = D.counts;
const part = (w, kind, side, id, key) => {
  const pm = D.part_models[w];
  const get = (m) => (side === "spending" ? sCell(m, id, key) : rCell(m, id, key));
  if (kind === "G") return byAlloc((a) => later * get(pm.later)[a].target_bn + (1 - c3) * g3_rate * get(pm.g3_rate)[a].target_bn);
  return byAlloc((a) => c3 * g3_rate * get(pm.white_g3_rate)[a].target_bn);
};
const lin = (w, side, id, key) => { const g = (m) => (side === "spending" ? sCell(m, id, key) : rCell(m, id, key)); return byAlloc((a) => g(LM[w])[a].target_bn - g(U4M[w])[a].target_bn); };
let worstPart = 0;
for (const w of SETS) {
  for (const [side, id, key] of [["spending", "social_security"], ["spending", "medicare"], ...Object.values(SP_SYN).map((s) => ["spending", s, "k"]), ...RCELLS.map((r) => ["receipt", r])]) {
    const G = part(w, "G", side, id, key), Wp = part(w, "W", side, id, key), T = lin(w, side, id, key);
    for (const a of ALLOCS) worstPart = Math.max(worstPart, Math.abs(G[a] + Wp[a] - T[a]));
  }
}
gate("the lineage's G and W parts add to its addition on every touched cell (1e-12)", worstPart < 1e-12, worstPart.toExponential(1));

// ---------------------------------------------------------------- inputs
const PP6 = V6.correctionsPayload().meta.pension_accrual, PP4 = V4.pensionNet();
const C0 = PEN.results.control.published, C4 = PEN.results.control.row4, A0 = PEN.results.arm.published, A4 = PEN.results.arm.row4;
const BW0 = BTX.weights.published, BW4 = BTX.weights.row4;
gate("v6's ratio_net and Part A are the Trustees arm's at published weights (exact)", PP6.ratio_net === A0.ratio_net && PP6.part_a_accrual_bn === A0.part_a_bn);
gate("v4's ratio_net and Part A are the control's at published weights (exact)", PP4.ratio_net === C0.ratio_net && PP4.part_a_accrual_bn === C0.part_a_bn);
gate("v6's benefit-tax receipt is v4's and the rerun's published receipt (1e-12)", ALLOCS.every((a) => PP6.benefit_tax_receipt_bn[a] === PP4.receipt_bn[a]
  && near(BW0.alloc[a].receipt_bn, PP4.receipt_bn[a], 1e-12)));
gate("the pension rerun's relative rates are the benefit-tax rerun's at published weights (1e-12)", ["union", ...GENS].every((g) => near(PEN.lane_rel[g], BW0.groups[g].relative_rate, 1e-12)));
const netOwn = (x, g, rel) => x.groups[g].per_tax_dollar * (1 - rel * x.groups[g].timing);
const fSS0 = A0.groups.G3plus.net_own_rate / C0.groups.G3plus.net_own_rate;
const fPA0 = A0.groups.G3plus.part_a_per_hi_tax_dollar / C0.groups.G3plus.part_a_per_hi_tax_dollar;
gate("v6's lineage factors are the reruns' (1e-15)", near(fSS0, PP6.lineage_factors.f_ss, 1e-15) && near(fPA0, PP6.lineage_factors.f_pa, 1e-15), `${fSS0} ${fPA0}`);
const fSS4 = netOwn(A4, "G3plus", BW4.groups.G3plus.relative_rate) / netOwn(C4, "G3plus", BW4.groups.G3plus.relative_rate);
const fPA4 = A4.groups.G3plus.part_a_per_hi_tax_dollar / C4.groups.G3plus.part_a_per_hi_tax_dollar;
gate("f_pa does not move on row 4 (G3+'s Part A per HI tax dollar, exact)", fPA4 === fPA0);
const rn = { v6: { pub: A0.ratio_net, row4: netOwn(A4, "union", BW4.groups.union.relative_rate), row4_rel_held: A4.ratio_net },
  v4: { pub: C0.ratio_net, row4: netOwn(C4, "union", BW4.groups.union.relative_rate), row4_rel_held: C4.ratio_net } };
gate("v4's row-4 ratio_net is price_rekeys.json's (1e-12)", near(rn.v4.row4, PR4.oasdi_ratio.row4, 1e-12), `${rn.v4.row4}`);
const partA = { v6: { pub: A0.part_a_bn, row4: A4.part_a_bn }, v4: { pub: C0.part_a_bn, row4: C4.part_a_bn } };
const btBy = byAlloc((a) => BW0.alloc[a].receipt_bn - BW4.alloc[a].receipt_bn);
gate("the benefit-tax move is v4's (1e-12)", ALLOCS.every((a) => near(btBy[a], PR4.benefit_tax_by[a], 1e-12)));
const KAPPA = SUMDEC.v4.kappas.low.modeled_owner_property;
gate("kappa is price_rekeys.json's", KAPPA === PR4.kappa_owner);
for (const line of Object.keys(SP_SYN)) gate(`SP_PRE ${line} in the v4 rerun is the package's (1e-6)`, near(SI.lines[line].sp_pre_published_bn, V4.SP_PRE[line], 1e-6));
for (const r of ["general_sales_tax", "personal_motor_vehicle"]) gate(`receipt factor ${r} is the package's (1e-9)`, near(SI.receipts[r].factor_published, V4.SP_RECEIPT[r].factor, 1e-9));

// ---------------------------------------------------------------- the generation split's inputs (lineage layer)
const GEN = path.join(F, "generation_account_2026_09_24/derived");
const GP = { set: J(path.join(GEN, "generation_corrections_sept29.json")), cash: J(path.join(GEN, "generation_corrections_sept29_cash.json")) };
const GM = {};
for (const w of SETS) GM[w] = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(J(path.join(GEN, `model_${g}.json`)), GP[w].payloads.a[g])]));
const Rg = Object.fromEntries(GENS.map((g) => [g, V4.hiOf(GM.set[g])])), Og = Object.fromEntries(GENS.map((g) => [g, V4.oasdiOf(GM.set[g])]));
const RU = V4.hiOf(U4M.set), OU = V4.oasdiOf(U4M.set);
gate("the generations' HI and OASDI receipts add to the union's (1e-9)", ALLOCS.every((a) => near(GENS.reduce((s, g) => s + Rg[g][a], 0), RU[a], 1e-9)
  && near(GENS.reduce((s, g) => s + Og[g][a], 0), OU[a], 1e-9)));
gate("the cash generation models carry the same HI and OASDI receipts (1e-12)", GENS.every((g) => ALLOCS.every((a) => near(V4.hiOf(GM.cash[g])[a], Rg[g][a], 1e-12)
  && near(V4.oasdiOf(GM.cash[g])[a], Og[g][a], 1e-12))));
gate("the union's Social Security is ratio_net x its OASDI receipts (1e-9)", ALLOCS.every((a) => near(sCell(U4M.set, "social_security")[a].target_bn, PP4.ratio_net * OU[a], 1e-9)));
const rho = (x, g) => x.groups[g].part_a_bn / x.groups[g].hi_tax_bn;
const Wa = (x) => byAlloc((a) => GENS.reduce((s, g) => s + rho(x, g) * Rg[g][a], 0));
const nr = (x, W, g) => netOwn(x, g, W.groups[g].relative_rate);
const Wt = (x, W) => byAlloc((a) => GENS.reduce((s, g) => s + nr(x, W, g) * Og[g][a], 0));
const Wa0 = Wa(C0), Wa4 = Wa(C4), Wt0 = Wt(C0, BW0), Wt4 = Wt(C4, BW4);
const g3PartA = (T, x, W_) => byAlloc((a) => T * rho(x, "G3plus") * Rg.G3plus[a] / W_[a]);
const g3SS = (r, x, W, W_) => byAlloc((a) => r * OU[a] * nr(x, W, "G3plus") * Og.G3plus[a] / W_[a]);
const pa0 = g3PartA(C0.part_a_bn, C0, Wa0), ss0 = g3SS(C0.ratio_net, C0, BW0, Wt0);
const g3set = GM.set.G3plus, g3cash = GM.cash.G3plus;
// 1e-6: the split read hi_arms.csv, whose accrual_bn and hi_tax_bn carry six decimals (the reruns carry full precision).
gate("the split's G3+ Part A is G3+'s Medicare less its kept cash share (1e-6: hi_arms.csv's six decimals)", ALLOCS.every((a) => near(pa0[a],
  sCell(g3set, "medicare")[a].target_bn - (1 - PP4.part_a_share) * sCell(g3cash, "medicare")[a].target_bn, 1e-6)),
  ALLOCS.map((a) => pa0[a].toFixed(6)).join(" / "));
gate("the split's G3+ Social Security is G3+'s set cell (1e-9)", ALLOCS.every((a) => near(ss0[a], sCell(g3set, "social_security")[a].target_bn, 1e-9)),
  ALLOCS.map((a) => ss0[a].toFixed(6)).join(" / "));
const pa4 = g3PartA(C4.part_a_bn, C4, Wa4), ss4 = g3SS(rn.v4.row4, C4, BW4, Wt4);
const dPA = byAlloc((a) => pa4[a] / pa0[a] - 1), dSS = byAlloc((a) => ss4[a] / ss0[a] - 1);
const nk = byAlloc((a) => BW0.alloc[a].national_key_census_bn / BW4.alloc[a].national_key_census_bn);
// White lane rule 3 (rekey_sept29.py receipt_per_rel_benefit): W's tax on benefits = the shared receipt / the engine
// union's cash Social Security / REL_UNION x 1.0 x W's benefits; on row 4 the receipt and REL_UNION move.
const kW = (BW4.alloc.shared.receipt_bn / BW0.alloc.shared.receipt_bn) * (BW0.groups.union.relative_rate / BW4.groups.union.relative_rate);
// owner: national key on row 4 (the decomposition lane's kappa = (u / n) / (u4 / n4), u - u4 = n - n4, s = u / n)
const ownM = rCell(MODEL, "modeled_owner_property");
const sOwn = ownM.shared.target_bn / lineOf(MODEL, "receipts", "modeled_owner_property").national_bn;
gate("the owner cell's share is the same at both allocations in model.json", ownM.personal.target_bn === ownM.shared.target_bn, sOwn.toFixed(6));
const yOwn = sOwn * (1 - 1 / KAPPA) / (1 - sOwn / KAPPA), nOwn = 1 / (1 - yOwn);
// The white end: W's move to the case's income-tax keys, as limits_oct07.csv gives it ($bn of cost, + = dearer), at the
// case's allocation for each end.
const W_ITEM = { 48: "case_w_income_tax_keys", 11: "case_w_income_tax_keys_personal" }, W_END = { 48: "low", 11: "high" }, W_BASIS = { set: "accrual", cash: "cash" };
const wRows = Object.fromEntries(SETS.map((w) => [w, ENDS.map((i) => LIM.filter((r) => r.item === W_ITEM[i] && r.arm === "g3_rate_mix" && r.basis === W_BASIS[w] && r.end === W_END[i]))]));
gate("limits_oct07.csv has one W row for each set and end", SETS.every((w) => wRows[w].every((rs) => rs.length === 1)));
const wMove = Object.fromEntries(SETS.map((w) => [w, wRows[w].map((rs) => Number(rs[0].bn))]));
const nWhite = V6.correctionsPayload().meta.lineage.members.white;
gate("W's count in limits_oct07.csv is the payload's white count (the file's four decimals)", SETS.every((w) => wRows[w].every((rs) => near(Number(rs[0].count), nWhite, 5e-5))), nWhite.toFixed(4));

// ---------------------------------------------------------------- the edits
const E = (side, line, keyOrSc, by) => (side === "receipt" ? { side, line, scenario: keyOrSc || REF, by } : { side, line, key: keyOrSc, by });
const apply = (m, edits) => Engine.applyCorrections(m, { lines: [], edits });
function unionEdits(c) {    // c: {U (union-only model), partA, rn, expand}
  const ssKey = lineOf(c.U, "spending", "social_security").preferred_key, medKey = lineOf(c.U, "spending", "medicare").preferred_key;
  const oasdi = V4.oasdiOf(c.U);
  return {
    owner: { set_only: false, apply(m) {
      const x = Engine.clone(m), l = lineOf(x, "receipts", "modeled_owner_property"), u = amt(rCell(c.U, "modeled_owner_property"));
      for (const a of ALLOCS) l.cells[REF][a].target_bn -= u[a] * (1 - 1 / KAPPA);
      return x;
    } },
    part_a: { set_only: true, apply: (m) => apply(m, [E("spending", "medicare", medKey, byAlloc(() => c.partA.row4 - c.partA.pub))]) },
    benefit_tax: { set_only: true, apply: (m) => apply(m, c.expand([{ side: "receipt", line: "federal_income_tax", by: btBy }])) },
    state_index: { set_only: false, apply(m) {
      const edits = Object.entries(SP_SYN).map(([line, syn]) => E("spending", syn, "k", byAlloc((a) => sCell(c.U, syn, "k")[a].target_bn * (SI.lines[line].ratio - 1))));
      const shifts = ["general_sales_tax", "personal_motor_vehicle"].map((id) => {
        const x = SI.receipts[id], u = rCell(c.U, id);
        return { side: "receipt", line: id, by: byAlloc((a) => (x.factor_row4 - x.factor_published) * u[a].target_bn / (1 + x.factor_published)) };
      });
      return apply(m, edits.concat(c.expand(shifts)));
    } },
    oasdi_ratio: { set_only: true, apply: (m) => apply(m, [E("spending", "social_security", ssKey, byAlloc((a) => (c.rn.row4 - c.rn.pub) * oasdi[a]))]) },
    oasdi_ratio_rate_held: { set_only: true, apply: (m) => apply(m, [E("spending", "social_security", ssKey, byAlloc((a) => (c.rn.row4_rel_held - c.rn.pub) * oasdi[a]))]) },
  };
}
// The lineage layer (v6 only): G's and W's parts read on the set or the cash set's part models.
const ssKey6 = lineOf(M.set, "spending", "social_security").preferred_key, medKey6 = lineOf(M.set, "spending", "medicare").preferred_key;
const G_PA = byAlloc((a) => part("set", "G", "spending", "medicare")[a] - (1 - PP6.part_a_share) * part("cash", "G", "spending", "medicare")[a]);
const G_SS = part("set", "G", "spending", "social_security"), LIN_SS = lin("set", "spending", "social_security");
const G_BT = byAlloc((a) => part("set", "G", "receipt", "federal_income_tax")[a] - part("cash", "G", "receipt", "federal_income_tax")[a]);
const W_BT = byAlloc((a) => part("set", "W", "receipt", "federal_income_tax")[a] - part("cash", "W", "receipt", "federal_income_tax")[a]);
gate("the lineage's Social Security on v6 is the lineage base's x f_ss (item pension_tr2026's lineage part, 1e-12)", ALLOCS.every((a) =>
  near(sCell(M.set, "social_security")[a].target_bn - sCell(U4M.set, "social_security")[a].target_bn - (A0.ratio_net - C0.ratio_net) * OU[a], LIN_SS[a] * fSS0, 1e-12)));
const LINEAGE = {
  part_a: { set_only: true, apply: (m) => apply(m, [E("spending", "medicare", medKey6, byAlloc((a) => G_PA[a] * fPA0 * dPA[a]))]) },
  ss_split: { set_only: true, apply: (m) => apply(m, [E("spending", "social_security", ssKey6, byAlloc((a) => G_SS[a] * fSS4 * dSS[a]))]) },
  ss_factor: { set_only: true, apply: (m) => apply(m, [E("spending", "social_security", ssKey6, byAlloc((a) => LIN_SS[a] * (fSS4 - fSS0)))]) },
  state_index: { set_only: false, apply(m, w) {
    const edits = Object.entries(SP_SYN).map(([line, syn]) => E("spending", syn, "k", byAlloc((a) => part(w, "G", "spending", syn, "k")[a] * (SI.lines[line].ratio - 1))));
    const shifts = ["general_sales_tax", "personal_motor_vehicle"].map((id) => {
      const x = SI.receipts[id], g = part(w, "G", "receipt", id);
      return { side: "receipt", line: id, by: byAlloc((a) => (x.factor_row4 - x.factor_published) * g[a] / (1 + x.factor_published)) };
    });
    return apply(m, edits.concat(V6.expand(shifts)));
  } },
  owner: { set_only: false, apply: (m, w) => apply(m, [E("receipt", "modeled_owner_property", REF, byAlloc((a) => part(w, "G", "receipt", "modeled_owner_property")[a] * (nOwn - 1)))]) },
  benefit_tax_g: { set_only: true, apply: (m) => apply(m, V6.expand([{ side: "receipt", line: "federal_income_tax", by: byAlloc((a) => G_BT[a] * (nk[a] - 1)) }])) },
  benefit_tax_w: { set_only: true, apply: (m) => apply(m, V6.expand([{ side: "receipt", line: "federal_income_tax", by: byAlloc((a) => W_BT[a] * (kW - 1)) }])) },
};
// The white end: a cost move of +x is a receipt shift of -x on an income-tax line (response 1, no capital component
// keys it), at the shared allocation for spec 48 and the personal one for spec 11.
const WHITE = { set_only: false, apply: (m, w) => apply(m, V6.expand([{ side: "receipt", line: "federal_income_tax", by: { shared: -wMove[w][0], personal: -wMove[w][1] } }])) };

// ---------------------------------------------------------------- positive control: the union edits on v4
{
  const P = P4, U = Engine.applyCorrections(P.MODEL, P.correctionsPayload());
  const CASH4 = J(path.join(F, "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json"));
  const PC = P.forPayload(CASH4), UC = Engine.applyCorrections(P.MODEL, CASH4);
  const ed = unionEdits({ U, partA: partA.v4, rn: rn.v4, expand: P.expand });
  const b4 = { set: ENDS.map((i) => P.evaluateFull(U, P.MAIN_SPECS[i]).cost_bn), cash: ENDS.map((i) => PC.evaluateFull(UC, PC.MAIN_SPECS[i]).cost_bn) };
  let worst = 0;
  for (const n of ["owner", "part_a", "benefit_tax", "state_index", "oasdi_ratio"]) {
    for (const [w, pk, m0] of [["set", P, U], ["cash", PC, UC]]) {
      const m = ed[n].set_only && w === "cash" ? m0 : ed[n].apply(m0);
      const mv = ENDS.map((i, j) => pk.evaluateFull(m, pk.MAIN_SPECS[i]).cost_bn - b4[w][j]);
      worst = Math.max(worst, ...mv.map((x, j) => Math.abs(x - PR4.rows[n][w].move[j])));
    }
  }
  gate("positive control: the union edits on v4 reproduce price_rekeys.json's moves (1e-9)", worst < 1e-9, worst.toExponential(2));
}

// ---------------------------------------------------------------- price on v6
const UE = unionEdits({ U: U4M.set, partA: partA.v6, rn: rn.v6, expand: V6.expand });
// the cash set's union edits read the cash union model for the both-sets edits (its cells equal the set's on those lines)
const UEc = unionEdits({ U: U4M.cash, partA: partA.v6, rn: rn.v6, expand: V6.expand });
gate("the cash union model's owner, state-price, sales and licence cells are the set's", Object.values(SP_SYN).every((id) => JSON.stringify(sCell(U4M.set, id, "k")) === JSON.stringify(sCell(U4M.cash, id, "k")))
  && ["modeled_owner_property", "general_sales_tax", "personal_motor_vehicle"].every((id) => JSON.stringify(rCell(U4M.set, id)) === JSON.stringify(rCell(U4M.cash, id))));
const ALL = {};
for (const [k, v] of Object.entries(UE)) ALL[`U_${k}`] = { set: v, cash: UEc[k] };
for (const [k, v] of Object.entries(LINEAGE)) ALL[`L_${k}`] = { set: v, cash: v };
ALL.white = { set: WHITE, cash: WHITE };
function run(names) {
  const out = {};
  for (const w of SETS) {
    let m = M[w];
    for (const n of names) { const r = ALL[n][w]; if (!(r.set_only && w === "cash")) m = r.apply(m, w); }
    const c = costAt(w, m);
    out[w] = { cost: c, move: c.map((x, j) => x - base[w][j]) };
  }
  return out;
}
const UNION = ["U_owner", "U_part_a", "U_benefit_tax", "U_state_index", "U_oasdi_ratio"];
const LINE = ["L_part_a", "L_ss_split", "L_ss_factor", "L_state_index", "L_owner", "L_benefit_tax_g", "L_benefit_tax_w"];
const rows = {};
for (const n of Object.keys(ALL)) rows[n] = run([n]);
rows.union_joint = run(UNION);
rows.lineage_joint = run(LINE);
rows.row4_class = run(UNION.concat(LINE));
rows.combined = run(UNION.concat(LINE, ["white"]));
// owner: the cell-shift route (engine.js applyCorrections, other residents moved) gives the same cost as v4's direct form
{
  const u = amt(rCell(U4M.set, "modeled_owner_property"));
  const viaEdit = SETS.map((w) => costAt(w, apply(M[w], [E("receipt", "modeled_owner_property", REF, byAlloc((a) => -u[a] * (1 - 1 / KAPPA)))])));
  gate("owner: the cell-shift route gives v4's direct form (1e-12)", SETS.every((w, k) => viaEdit[k].every((x, j) => near(x, rows.U_owner[w].cost[j], 1e-12))));
}
// owner: the union's cell and kappa are v4's, so the move is v4's times the owner line's response, v6's over v4's
const ownerResponse = (api, m, i) => api.evaluateFull(m, api.MAIN_SPECS[i]).evaluation.receipts.find((l) => l.id === "modeled_owner_property").response;
const U4 = Engine.applyCorrections(P4.MODEL, P4.correctionsPayload());
const ownerResp = { v6: ENDS.map((i) => ownerResponse(V6, M.set, i)), v4: ENDS.map((i) => ownerResponse(P4, U4, i)) };
gate("owner: the move is v4's times the owner line's response, v6's over v4's (1e-9 relative)", ENDS.every((_, j) =>
  near(rows.U_owner.set.move[j] / PR4.rows.owner.set.move[j], ownerResp.v6[j] / ownerResp.v4[j], 1e-9)),
  ownerResp.v6.map((x, j) => `${x.toFixed(6)} / ${ownerResp.v4[j].toFixed(6)}`).join("; "));
gate("the white end alone moves the case by limits_oct07.csv's amounts at the case's allocation (1e-9)",
  SETS.every((w) => rows.white[w].move.every((x, j) => near(x, wMove[w][j], 1e-9))), SETS.map((w) => rows.white[w].move.map((x) => x.toFixed(6)).join(" / ")).join("; "));
// Joint minus the sum of its parts, $bn: the engine is linear in cell amounts at given responses.
const sumOf = (ns, w) => ENDS.map((_, j) => ns.reduce((s, n) => s + rows[n][w].move[j], 0));
const inter = (joint, ns) => Object.fromEntries(SETS.map((w) => [w, rows[joint][w].move.map((x, j) => x - sumOf(ns, w)[j])]));
const interactions = { union: inter("union_joint", UNION), lineage: inter("lineage_joint", LINE), row4_class: inter("row4_class", UNION.concat(LINE)),
  row4_class_and_white_end: inter("combined", ["row4_class", "white"]) };
const POP = S6.v6.per_member_usd.population;
const perMember = (r) => Object.fromEntries(SETS.map((w) => [w, r[w].cost.map((x) => x * 1e9 / POP)]));
const pmBase = perMember({ set: { cost: base.set }, cash: { cost: base.cash } });
gate("per member of the lineage, the base is summary.json's v6.per_member_usd (1e-6)", SETS.every((w) => pmBase[w].every((x, j) => near(x, S6.v6.per_member_usd[w][j], 1e-6))),
  SETS.map((w) => pmBase[w].map((x) => x.toFixed(2)).join(" / ")).join("; "));
const f4 = (x) => (x >= 0 ? "+" : "") + x.toFixed(4);
for (const [n, r] of Object.entries(rows)) {
  console.log(`${n.padEnd(26)} set ${r.set.cost.map((x) => x.toFixed(4)).join(" / ")} (${r.set.move.map(f4).join(" / ")}); cash ${r.cash.cost.map((x) => x.toFixed(4)).join(" / ")} (${r.cash.move.map(f4).join(" / ")})`);
}
for (const [k, v] of Object.entries(interactions)) console.log(`interaction ${k}: set ${v.set.map((x) => x.toExponential(2)).join(" / ")}; cash ${v.cash.map((x) => x.toExponential(2)).join(" / ")}`);
if (fails) { console.error(`[BLOCKED] ${fails} gate(s) failed; nothing written`); process.exit(1); }

const f6 = (v) => { if (v === "") return ""; const s = v.toFixed(6); return s === "-0.000000" ? "0.000000" : s; };
const CSV_ROWS = [
  ["union", "owner", "U_owner"], ["union", "part_a", "U_part_a"], ["union", "benefit_tax", "U_benefit_tax"],
  ["union", "state_index", "U_state_index"], ["union", "oasdi_ratio", "U_oasdi_ratio"], ["union", "joint", "union_joint"],
  ["lineage", "part_a_split", "L_part_a"], ["lineage", "ss_split", "L_ss_split"], ["lineage", "ss_factor", "L_ss_factor"],
  ["lineage", "state_index", "L_state_index"], ["lineage", "owner_national_key", "L_owner"],
  ["lineage", "benefit_tax_g3plus", "L_benefit_tax_g"], ["lineage", "benefit_tax_white", "L_benefit_tax_w"], ["lineage", "joint", "lineage_joint"],
  ["row4_class", "joint", "row4_class"], ["white_end", "income_tax_keys_at_case_allocation", "white"],
  ["row4_class_and_white_end", "joint", "combined"],
];
const csv = [["layer", "item", "set_move_48", "set_move_11", "set_cost_48", "set_cost_11", "cash_move_48", "cash_move_11", "cash_cost_48", "cash_cost_11"].join(",")];
csv.push(["case", "base", 0, 0, ...base.set, 0, 0, ...base.cash].map((v) => (typeof v === "number" ? f6(v) : v)).join(","));
for (const [layer, item, n] of CSV_ROWS) {
  const r = rows[n];
  csv.push([layer, item, ...r.set.move, ...r.set.cost, ...r.cash.move, ...r.cash.cost].map((v) => (typeof v === "number" ? f6(v) : v)).join(","));
}
for (const [layer, v] of Object.entries(interactions)) csv.push([layer, "interaction", ...v.set, "", "", ...v.cash, "", ""].map((x) => (typeof x === "number" ? f6(x) : x)).join(","));
fs.writeFileSync(path.join(OUT, "row4_oct07.csv"), csv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "row4_oct07.json"), JSON.stringify({
  base, rows: Object.fromEntries(CSV_ROWS.map(([, , n]) => [n, rows[n]])), interactions,
  beside: { oasdi_ratio_rate_held: rows.U_oasdi_ratio_rate_held },
  white_end: { file: "white_replacement_2026_09_28/derived/limits_oct07.csv", arm: "g3_rate_mix", items: W_ITEM, basis: W_BASIS, count: nWhite, move_bn: wMove },
  per_member_usd: { population: POP, base: pmBase, row4_class: perMember(rows.row4_class), combined: perMember(rows.combined) },
  inputs: { rn, partA, btBy, kappa_owner: KAPPA, owner_response: ownerResp, fSS0, fSS4, fPA0, fPA4, delta_part_a: dPA, delta_ss: dSS, national_key_ratio: nk, white_rule3_ratio: kW,
    owner_national_ratio: nOwn, G_part_a: G_PA, G_ss: G_SS, lineage_ss: LIN_SS, G_benefit_tax: G_BT, W_benefit_tax: W_BT, R_hi: Rg, O_oasdi: Og,
    g3_split: { part_a_pub: pa0, part_a_row4: pa4, ss_pub: ss0, ss_row4: ss4 } },
  gates_failed: fails }, null, 1) + "\n");
console.log(`[written] ${path.relative(path.resolve(F, "..", ".."), OUT)}/row4_oct07.csv, row4_oct07.json`);
