/* Candidate v4, sept29_candidate_v4: the pending bundle as one set. Gates, then derived/. package.cjs holds the
 * definitions.
 *
 * Gates (each prints; any failure exits 1 and writes nothing):
 *   base     every item off is the September 27 case at all 64 specifications (its own package and its committed
 *            per_spec.csv, exactly) and its band at 48 / 11 (summary.json, 1e-9);
 *   specs    every option set has 32 distinct specifications, each twice with equal cost, 48 = 52 and 11 = 15;
 *   v3       items 1-5, 6a (proportional), v3's three-line item 7, 8, 10 and v3's candidate reproduce v3's
 *            derived/summary.json at_fixed_specifications at 48 / 11 (1e-6; its fixed_specs.csv prints 4 decimals);
 *   7        workers' compensation only: response x (ratio - 1) x the line's amount at every specification (1e-9);
 *   pension  alone, the pension lane's case_on_accrual_net_bn (1e-6); social_security, medicare and federal income
 *            tax at their formulas at every specification (1e-9);
 *   state    alone, net_state_correction.csv's central package, its spending and receipt parts and each line (1e-8);
 *            each synthetic line at its formula (1e-12) and its parent's response (exact);
 *   roads    alone, the roads lane's summary.json cost change and its four parts (6-decimal file, 1e-6) and keys.csv's
 *            road key and miles share (1e-6);
 *   lines    each item alone moves exactly its named lines, capital components and production terms (the scan below);
 *            the set moves only their union;
 *   national every line's national total is the September 27 case's but the split lines named below, which sum to their
 *            old totals less the consolidated subsidy; every executed cell's group + other is its national (1e-9);
 *   rules    in the set, each overlapping line sits at its chosen rule's formula at every specification (1e-9);
 *   sums     the line contributions sum to each cost (1e-9), and the line interactions to the set's interaction.
 * Comparisons are at the fixed specifications 48 and 11, the two fill-in methods averaged, as v3 reports them.
 * Run from anywhere: node main_case.cjs [--out-dir DIR] -> derived/ bands.csv, per_spec.csv, attribution.csv,
 * pairwise.csv, line_interactions.csv, overlaps.csv, summary.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const C = require("./package.cjs");
const V3 = C.V3PKG;
const S = C.SEPT27;
const { METHODS, ALLOCS, FISCAL, HERE, SET_ITEMS, BESIDE_ITEMS, OFF, SET, CASH, RULES, OPTION_VALUES, SP_SYN, SP_LINES, RD_SYN, HWY, EXCISE,
  LICENCES, SALES_LINE, FIT_LINE, SS_LINE, MEDICARE_LINE, WC_LINE, gateState, gate, near, f2, csvRows, readJson, distinctSpecs, specKey, endsOf,
  withCentral, specsFor, modelFor, evaluateFull, offOf, lineOf } = C;
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => xs.reduce((a, x) => Math.max(a, Math.abs(x)), 0);
const ex = (x) => x.toExponential(1);
const fx = (x) => x.toFixed(4);
const f6 = (x) => x.toFixed(6);
const full = (x) => (typeof x === "number" ? String(x) : x);
const ENDS = [48, 11];
const atEnds = (f) => ENDS.map((i) => mean(METHODS.map((_, m) => f(m, i))));
const row = (r, side, id) => r.evaluation[side].find((l) => l.id === id);
const comp = (r, id) => r.capital.components.find((c) => c.id === id);
const pp = C.pensionNet();

// ---------------------------------------------------------------------------------------------------
// Option sets: each method's model and every specification.
function runsOf(o) {
  const oo = withCentral(o);
  const specs = specsFor(oo);
  const models = METHODS.map((meth) => modelFor("central", meth, oo));
  const runs = models.map((m) => specs.map((s) => evaluateFull(m, s)));
  return { o, specs, models, runs, costs: runs.map((xs) => xs.map((r) => r.cost_bn)), idx: distinctSpecs(specs), keys: specs.map(specKey) };
}
const IDS = SET_ITEMS.map((it) => it.id);
const CASH_IDS = IDS.filter((id) => id !== "pension");
const itemOf = (id) => SET_ITEMS.concat(BESIDE_ITEMS).find((it) => it.id === id);
const withOff = (...os) => Object.assign({}, OFF, ...os);
const SETS = { sept27: OFF, set: SET, cash: CASH };
for (const it of SET_ITEMS.concat(BESIDE_ITEMS)) SETS[`alone_${it.id}`] = withOff(it.o);
for (const id of IDS) SETS[`set_minus_${id}`] = Object.assign({}, SET, offOf(itemOf(id).o));
for (const id of CASH_IDS) SETS[`cash_minus_${id}`] = Object.assign({}, CASH, offOf(itemOf(id).o));
for (const it of BESIDE_ITEMS) { SETS[`set_plus_${it.id}`] = Object.assign({}, SET, it.o); SETS[`cash_plus_${it.id}`] = Object.assign({}, CASH, it.o); }
IDS.forEach((a, i) => IDS.slice(i + 1).forEach((b) => { SETS[`pair_${a}_${b}`] = withOff(itemOf(a).o, itemOf(b).o); }));
// v3's own rows: its three-line item 7 and its candidate (items 1-8, 6a and 6b within-group), in this package's options.
SETS.v3_item7_three_lines = withOff({ workers_comp: "pooled_2019_2024" });
SETS.v3_candidate = Object.assign({}, OFF, V3.CANDIDATE);
// Each composition rule's alternatives, on the set and on the cash set (the pension rules on the set only).
const PENSION_RULES = ["benefit_tax_rule", "accrual_receipts", "part_a_rule"];
const ALTS = [];
for (const [field, chosen] of Object.entries(RULES)) for (const v of OPTION_VALUES[field]) if (v !== chosen) {
  ALTS.push({ field, value: v, base: "set" });
  SETS[`set_${field}_${v}`] = Object.assign({}, SET, { [field]: v });
  if (!PENSION_RULES.includes(field)) { ALTS.push({ field, value: v, base: "cash" }); SETS[`cash_${field}_${v}`] = Object.assign({}, CASH, { [field]: v }); }
}
const X = Object.fromEntries(Object.entries(SETS).map(([k, o]) => [k, runsOf(o)]));
const fixedChange = (a, b) => atEnds((m, i) => X[a].costs[m][i] - X[b].costs[m][i]);
const fixedCost = (a) => atEnds((m, i) => X[a].costs[m][i]);
const diff = (a, b) => X[a].costs.map((xs, m) => xs.map((x, i) => x - X[b].costs[m][i]));
const B = Object.fromEntries(Object.keys(X).map((k) => [k, fixedCost(k)]));
const E = Object.fromEntries(Object.keys(X).map((k) => [k, endsOf(X[k].specs, X[k].runs)]));

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the September 27 case]");
const SEPT27_DIR = "main_case_long_run_2026_09_27/derived";
const s27 = readJson(`${SEPT27_DIR}/summary.json`);
const own27 = METHODS.map((meth) => { const oo = S.withCentral({}); const m = S.modelFor("central", meth, oo); return S.specsFor(oo).map((s) => S.evaluateFull(m, s).cost_bn); });
const same = (a, b) => a.length === b.length && a.every((xs, m) => xs.length === b[m].length && xs.every((x, i) => x === b[m][i]));
gate("with every item off, v4 is the September 27 case at every specification exactly (its own package, both methods)", same(X.sept27.costs, own27), "2 x 64");
const per27 = csvRows(`${SEPT27_DIR}/per_spec.csv`);
gate("...and its committed per_spec.csv exactly", per27.length === 128 && per27.every((r) => Number(r.cost_bn) === X.sept27.costs[METHODS.indexOf(r.method)][Number(r.spec)]), "128 rows");
const at4811 = (ends) => ends.every((e) => e[0] === 48 && e[1] === 11);
gate("its band at 48 / 11 is summary.json's main_case (1e-9), and 48 / 11 are both methods' ends", near(B.sept27[0], s27.main_case[0], 1e-9)
  && near(B.sept27[1], s27.main_case[1], 1e-9) && at4811(E.sept27), f2(B.sept27));

console.log("\n[gates: the specifications]");
const twinOf = (x, i) => x.keys.findIndex((t, j) => j !== i && t === x.keys[i]);
const specsOk = Object.values(X).every((x) => x.idx.length === 32 && x.specs.length === 64
  && x.keys.every((key, i) => { const t = twinOf(x, i); return t >= 0 && x.keys.filter((u) => u === key).length === 2 && x.costs.every((xs) => xs[i] === xs[t]); })
  && twinOf(x, 48) === 52 && twinOf(x, 11) === 15);
gate("in every option set the 64 specifications are 32 distinct ones, each twice with equal cost; 48 = 52 and 11 = 15", specsOk, `${Object.keys(X).length} option sets`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: v3's items reproduce v3]");
const V3_DIR = "main_case_candidate_v3_2026_09_28/derived";
const v3s = readJson(`${V3_DIR}/summary.json`).at_fixed_specifications;
const v3csv = Object.fromEntries(csvRows(`${V3_DIR}/fixed_specs.csv`).map((r) => [r.item, r]));
const V3_ROWS = [["item1", "alone_1"], ["item2", "alone_2"], ["item3", "alone_3"], ["item4", "alone_4"], ["item5", "alone_5"],
  ["item6a_proportional_rule", "alone_6a"], ["item7", "v3_item7_three_lines"], ["item8", "alone_8"], ["item10", "alone_10"], ["candidate_switch_off", "v3_candidate"]];
const v3Gaps = V3_ROWS.map(([key, set]) => {
  const d = fixedChange(set, "sept27"), n = fixedCost(set), w = v3s[key], c = v3csv[key];
  return { key, set, d, json: worst([d[0] - w.change[0], d[1] - w.change[1], n[0] - w.new[0], n[1] - w.new[1]]),
    csv: worst([d[0] - Number(c.change_spec48_bn), d[1] - Number(c.change_spec11_bn), n[0] - Number(c.new_spec48_bn), n[1] - Number(c.new_spec11_bn)]) };
});
gate("items 1-5, 6a (proportional), v3's three-line 7, 8, 10 and v3's candidate reproduce v3's summary.json at_fixed_specifications (change and new at 48 / 11, 1e-6) and its 4-decimal fixed_specs.csv (5e-5)",
  v3Gaps.every((g) => g.json < 1e-6 && g.csv <= 5e-5 + 1e-12), `max |diff| json ${ex(worst(v3Gaps.map((g) => g.json)))}, csv ${ex(worst(v3Gaps.map((g) => g.csv)))}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: item 7 on workers' compensation only]");
const d7 = diff("alone_7", "sept27");
const f7 = worst(METHODS.flatMap((_, m) => X.alone_7.specs.map((s, i) => {
  const r = row(X.sept27.runs[m][i], "spending", WC_LINE);
  if (r.key !== C.WC_KEY) throw new Error(`[BLOCKED] ${WC_LINE} is evaluated at ${r.key}, not ${C.WC_KEY}`);
  return d7[m][i] - r.response * (C.WC[s.allocation].ratio - 1) * r.amount_bn; })));
const d7three = diff("v3_item7_three_lines", "alone_7");
const f7rest = worst(METHODS.flatMap((_, m) => X.alone_7.specs.map((s, i) => d7three[m][i] - C.WC_LINES.filter((id) => id !== WC_LINE)
  .reduce((a, id) => { const r = row(X.sept27.runs[m][i], "spending", id); return a + r.response * (C.WC[s.allocation].ratio - 1) * r.amount_bn; }, 0))));
gate("item 7 moves the cost by the line's response x (ratio - 1) x its amount, and v3's three-line item by the same on the other two lines (every specification, 1e-9)",
  f7 < 1e-9 && f7rest < 1e-9, `max |diff| ${ex(f7)}, ${ex(f7rest)}; ${f2(fixedChange("alone_7", "sept27"))} against v3's parent hand split -0.95 / -0.73`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the pension switch at payable benefits, net]");
const dP = fixedChange("alone_pension", "sept27"), nP = fixedCost("alone_pension");
gate(`alone it gives the pension lane's payable central (${pp.file} at ${pp.commit}, case_on_accrual_net_bn, 1e-6; HEAD and working tree identical)`,
  near(nP[0], pp.case_on_accrual_net_bn[0], 1e-6) && near(nP[1], pp.case_on_accrual_net_bn[1], 1e-6) && near(dP[0], pp.delta_net_bn[0], 1e-6)
  && near(dP[1], pp.delta_net_bn[1], 1e-6) && pp.same_at_head && pp.same_in_working_tree && near(pp.case_bn[0], s27.main_case[0], 1e-9) && near(pp.case_bn[1], s27.main_case[1], 1e-9),
  `${f2(nP)} (change ${f2(dP)}) against ${f2(pp.case_on_accrual_net_bn)}; printed $399.10 / $460.98bn`);
const fP = worst(["alone_pension", "set"].flatMap((k) => METHODS.flatMap((_, m) => X[k].specs.flatMap((s, i) => {
  const r = X[k].runs[m][i], a = s.allocation, cashK = k === "set" ? "cash" : "sept27", c = X[cashK].runs[m][i];
  const rec = (x, id) => row(x, "receipts", id).amount_bn;
  const oasdi = rec(r, "employee_oasdi") + rec(r, "employer_oasdi") + pp.se_oasdi_share * rec(r, "self_employment_oasdi_hi");
  return [row(r, "spending", SS_LINE).amount_bn - pp.ratio_net * oasdi,
    row(r, "spending", MEDICARE_LINE).amount_bn - ((1 - pp.part_a_share) * row(c, "spending", MEDICARE_LINE).amount_bn + pp.part_a_accrual_bn),
    rec(r, FIT_LINE) - (rec(c, FIT_LINE) - pp.receipt_bn[a])];
}))));
gate("social_security = ratio_net x the group's OASDI receipts; medicare = (1 - Part A share) x cash + Part A accrual; federal income tax = cash less the benefit-tax receipt of the allocation (alone and in the set, every specification, 1e-9)",
  fP < 1e-9, `ratio_net ${pp.ratio_net.toFixed(6)}, Part A $${pp.part_a_accrual_bn.toFixed(4)}bn, receipt $${pp.receipt_bn.shared.toFixed(4)} / $${pp.receipt_bn.personal.toFixed(4)}bn; max |diff| ${ex(fP)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: state pricing]");
const spParts = (k) => atEnds((m, i) => SP_LINES.reduce((a, id) => a - row(X[k].runs[m][i], "spending", SP_SYN[id]).effect_bn, 0));
const spRec = (k) => atEnds((m, i) => [SALES_LINE, LICENCES].reduce((a, id) => a + row(X[k].runs[m][i], "receipts", id).effect_bn - row(X.sept27.runs[m][i], "receipts", id).effect_bn, 0));
const dS = fixedChange("alone_state", "sept27"), sSp = spParts("alone_state"), sRc = spRec("alone_state");
const T = C.SP_TARGET;
// The lane's CSVs print 10 significant digits (state_price.py, float_format "%.10g"), so the recomputation from its
// printed S&L amounts and indexes differs from its printed totals by up to the half-units of those digits, carried
// through the formula at the evaluated shares, plus the totals' own half-unit. That bound is the tolerance.
const hu = (v) => (v === 0 ? 0 : 0.5 * Math.pow(10, Math.floor(Math.log10(Math.abs(v))) - 9));
const spBound = (e) => {
  const r0 = X.alone_state.runs.map((xs) => xs[ENDS[e]]);
  const share = (side, id) => mean(r0.map((r) => { const l = row(r, side, id); return l.amount_bn / l.national_bn; }));
  const resp = (side, id) => row(r0[0], side, id).response;
  const spend = C.SP_SPEND.reduce((a, r) => a + share("spending", r.line) * resp("spending", r.line)
    * (Number(r.sl_amount_bn) * hu(Number(r.index)) + hu(Number(r.sl_amount_bn)) * Math.abs(Number(r.index) - 1)), 0);
  const recs = C.SP_REC.reduce((a, r) => a + share("receipts", r.line) * resp("receipts", r.line)
    * (Number(r.sl_amount_bn) * hu(Number(r.index)) + hu(Number(r.sl_amount_bn)) * Math.abs(Number(r.index) - 1)), 0);
  const t = T[e ? "high" : "low"];
  return { spending: spend + hu(t.spending), receipts: recs + hu(t.receipts), net: spend + recs + hu(t.net) };
};
const spB = [spBound(0), spBound(1)];
const spGap = [0, 1].map((e) => { const t = T[e ? "high" : "low"]; return { net: dS[e] - t.net, spending: sSp[e] - t.spending, receipts: sRc[e] - t.receipts }; });
gate("alone it gives the lane's central package: net, spending and receipt gain at both ends (net_state_correction.csv, within the rounding of its printed inputs)",
  [0, 1].every((e) => ["net", "spending", "receipts"].every((k) => Math.abs(spGap[e][k]) <= spB[e][k])),
  `net ${f6(dS[0])} / ${f6(dS[1])} against ${T.low.net} / ${T.high.net}; |diff| ${ex(Math.abs(spGap[0].net))} / ${ex(Math.abs(spGap[1].net))}, `
  + `rounding bound ${ex(spB[0].net)} / ${ex(spB[1].net)}; spending ${f6(sSp[0])} / ${f6(sSp[1])}; receipts ${f6(sRc[0])} / ${f6(sRc[1])}`);
const perLine = SP_LINES.map((id) => {
  const got = atEnds((m, i) => -row(X.alone_state.runs[m][i], "spending", SP_SYN[id]).effect_bn);
  const want = [0, 1].map((e) => C.SP_SPEND.filter((r) => r.line === id).reduce((a, r) => a + Number(e ? r.correction_high_bn : r.correction_low_bn), 0));
  return { id, got, want, gap: worst([got[0] - want[0], got[1] - want[1]]) };
});
const recLine = [SALES_LINE, LICENCES].map((id) => {
  const got = atEnds((m, i) => row(X.alone_state.runs[m][i], "receipts", id).effect_bn - row(X.sept27.runs[m][i], "receipts", id).effect_bn);
  const r = C.SP_REC.find((x) => x.line === id);
  return { id, got, want: [Number(r.receipt_gain_low_bn), Number(r.receipt_gain_high_bn)], gap: worst([got[0] - Number(r.receipt_gain_low_bn), got[1] - Number(r.receipt_gain_high_bn)]) };
});
gate("each re-priced line is the lane's correction at both ends (corrections.csv, receipts_corrections.csv, 1e-8)", perLine.concat(recLine).every((x) => x.gap < 1e-8),
  perLine.concat(recLine).map((x) => `${x.id} ${f6(x.got[0])}/${f6(x.got[1])}`).join("; "));
const spForm = worst(["alone_state", "set", "cash"].flatMap((k) => METHODS.flatMap((_, m) => X[k].specs.flatMap((s, i) => {
  const r = X[k].runs[m][i];
  return SP_LINES.flatMap((id) => { const p = row(r, "spending", id), y = row(r, "spending", SP_SYN[id]);
    return [y.amount_bn - C.SP_PRE[id] * p.amount_bn / p.national_bn, y.response === p.response ? 0 : Infinity,
      p.key === C.parentKey(lineOf(C.MODEL, "spending", id)) ? 0 : Infinity]; });
}))));
gate("every synthetic line is sum_f S&L_f (index_f - 1) x its parent's evaluated key (1e-12) at its parent's response (exact), alone and in both sets, every specification",
  spForm < 1e-12, `max |diff| ${ex(spForm)}`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: roads keyed by miles]");
const RS = C.RD_SUM.by_ratio[C.RD_RATIO];
const dR = fixedChange("alone_roads", "sept27");
const rdParts = {
  opex_bn: atEnds((m, i) => [RD_SYN.sl, RD_SYN.fed].reduce((a, id) => a - row(X.alone_roads.runs[m][i], "spending", id).effect_bn, 0)),
  capital_bn: atEnds((m, i) => [HWY.sl.capital, HWY.fed.capital].reduce((a, id) => a + comp(X.alone_roads.runs[m][i], id).return_bn - comp(X.sept27.runs[m][i], id).return_bn, 0)),
  gasoline_bn: atEnds((m, i) => row(X.alone_roads.runs[m][i], "receipts", EXCISE).effect_bn - row(X.sept27.runs[m][i], "receipts", EXCISE).effect_bn),
  licences_bn: atEnds((m, i) => row(X.alone_roads.runs[m][i], "receipts", LICENCES).effect_bn - row(X.sept27.runs[m][i], "receipts", LICENCES).effect_bn),
};
gate(`alone it gives the roads lane's cost change and its four parts (${C.RD_DIR}/summary.json by_ratio.${C.RD_RATIO}, 6-decimal file, 1e-6)`,
  [0, 1].every((e) => Math.abs(dR[e] - RS.cost_change_bn[e]) <= 1e-6) && Object.keys(rdParts).every((k) => [0, 1].every((e) => Math.abs(rdParts[k][e] - RS[k][e]) <= 1e-6)),
  `${f6(dR[0])} / ${f6(dR[1])} against ${RS.cost_change_bn.join(" / ")}; ${Object.entries(rdParts).map(([k, v]) => `${k} ${f6(v[0])}/${f6(v[1])}`).join(", ")}`);
const keysCsv = csvRows(`${C.RD_DIR}/keys.csv`).filter((r) => r.nhts_ratio === C.RD_RATIO);
const keyGap = worst(METHODS.flatMap((meth, m) => ALLOCS.flatMap((a) => {
  const t = X.alone_roads.models[m].candidate.v4, k = C.roadKeysOf(X.sept27.models[m])[a], r = keysCsv.find((x) => x.method === meth && x.allocation === a);
  return [t.k_road[a] - Number(r.road_key_group), k.s_vmt - Number(r.vmt_share_group), k.k_cons - Number(r.consumption_share), k.k_old - Number(r.old_key_resources), k.k_adults - Number(r.adults_key)];
})));
gate("the keys are the lane's keys.csv (road key, miles share, consumption, resources and adults keys; 6 decimals, 1e-6)", keyGap <= 1e-6 && keysCsv.length === 4, `max |diff| ${ex(keyGap)}`);
const rdResp = worst(["alone_roads", "set", "cash"].flatMap((k) => METHODS.flatMap((_, m) => X[k].specs.flatMap((s, i) => {
  const r = X[k].runs[m][i], sfr = S.subfunctionResponses(s.long_run, s.reading), t = X[k].models[m].candidate.v4;
  return [row(r, "spending", RD_SYN.sl).response - sfr[HWY.sl.subfunction], row(r, "spending", RD_SYN.fed).response - sfr[HWY.fed.subfunction],
    comp(r, HWY.sl.capital).key - t.k_road[s.allocation], comp(r, HWY.fed.capital).key - t.k_road[s.allocation],
    comp(r, HWY.sl.capital).response - sfr[HWY.sl.subfunction], comp(r, HWY.fed.capital).response - sfr[HWY.fed.subfunction]];
}))));
gate("the synthetic highway lines take the subfunctions' responses and hwy_sl / hwy_fed the road key (alone and in both sets, every specification, exact)", rdResp === 0, `max |diff| ${ex(rdResp)}`);

// ---------------------------------------------------------------------------------------------------
// The scan: what each item moves alone, against the September 27 case, at every specification and method. A line is
// moved when its amount, response, effect or national differs (exactly), or it exists in one run only; a capital
// component when its return differs by more than 1e-12 (item 1 rescales the enterprise line, whose key then carries
// float noise); production when P or F differs.
function moves(a, b) {
  const out = new Set();
  X[a].runs.forEach((xs, m) => xs.forEach((r, i) => {
    const o = X[b].runs[m][i];
    for (const side of ["spending", "receipts"]) {
      const A = new Map(r.evaluation[side].map((x) => [x.id, x])), Bm = new Map(o.evaluation[side].map((x) => [x.id, x]));
      for (const id of new Set([...A.keys(), ...Bm.keys()])) {
        const x = A.get(id), y = Bm.get(id);
        if (!x || !y || x.amount_bn !== y.amount_bn || x.response !== y.response || x.effect_bn !== y.effect_bn || x.national_bn !== y.national_bn) out.add(`${side}:${id}`);
      }
    }
    const cb = new Map(o.capital.components.map((c) => [c.id, c]));
    for (const c of r.capital.components) { const d = cb.get(c.id); if (!d || Math.abs(c.return_bn - d.return_bn) > 1e-12) out.add(`capital:${c.id}`); }
    for (const c of o.capital.components) if (!r.capital.components.some((x) => x.id === c.id)) out.add(`capital:${c.id}`);
    if (r.evaluation.private_wtp_bn !== o.evaluation.private_wtp_bn) out.add("production:P");
    if (r.evaluation.induced_receipts_bn !== o.evaluation.induced_receipts_bn) out.add("production:F");
    if (r.public_pay_bn !== o.public_pay_bn) out.add("public_pay");
  }));
  return [...out].sort();
}
const rec = (ids) => ids.map((id) => `receipts:${id}`), sp = (ids) => ids.map((id) => `spending:${id}`);
const NAMED = {
  1: [...sp([C.RENTAL]), ...rec([C.ENTERPRISE_LINE, C.HOUSING_LINE])],
  2: ["production:F", "production:P"],
  3: rec([FIT_LINE]),
  4: [`capital:${C.HOUSING_CAPITAL}`],
  5: rec(C.PROPERTY_LINES),
  "6a": rec(Object.keys(C.PAY.items.all.central.lines)),
  7: sp([WC_LINE]),
  pension: [...sp([SS_LINE, MEDICARE_LINE]), ...rec([FIT_LINE])],
  state: [...sp(Object.values(SP_SYN)), ...rec([SALES_LINE, LICENCES])],
  roads: [...sp(Object.values(RD_SYN)), ...rec([EXCISE, LICENCES]), `capital:${HWY.sl.capital}`, `capital:${HWY.fed.capital}`],
  8: [...rec([C.ENTERPRISE_LINE, C.TRANSIT_LINE]), `capital:${C.TRANSIT_CAPITAL}`],
  10: sp([C.MEDICAID_LINE]),
};
const TOUCH = Object.fromEntries(SET_ITEMS.concat(BESIDE_ITEMS).map((it) => [it.id, moves(`alone_${it.id}`, "sept27")]));
const touchBad = Object.entries(TOUCH).filter(([id, xs]) => xs.join() !== NAMED[id].slice().sort().join());
gate("each item alone moves exactly its named lines, capital components and production terms (every specification, both methods)", touchBad.length === 0,
  touchBad.map(([id, xs]) => `${id}: ${xs.join(" ")}`).join("; ") || `${Object.keys(TOUCH).length} items`);
const UNION = new Set(IDS.flatMap((id) => TOUCH[id]));
const setMoves = moves("set", "sept27"), cashMoves = moves("cash", "sept27");
gate("the set and the cash set move only the union of their items' lines", setMoves.every((x) => UNION.has(x)) && cashMoves.every((x) => CASH_IDS.some((id) => TOUCH[id].includes(x))),
  `${setMoves.length} and ${cashMoves.length} lines moved; union ${UNION.size}`);
// Lines two or more set items move directly.
const SHARED = [...UNION].filter((x) => IDS.filter((id) => TOUCH[id].includes(x)).length > 1).map((x) => ({ line: x, items: IDS.filter((id) => TOUCH[id].includes(x)) }));

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: national totals]");
const nationals = (m) => Object.fromEntries(["spending", "receipts"].flatMap((side) => m[side].lines.map((l) => [`${side}:${l.id}`, l.national_bn])));
const SYN_IDS = new Set([...Object.values(SP_SYN), ...Object.values(RD_SYN)].map((id) => `spending:${id}`));
const SPLIT = new Set([`spending:${C.RENTAL}`, `receipts:${C.ENTERPRISE_LINE}`, `receipts:${C.HOUSING_LINE}`, `receipts:${C.TRANSIT_LINE}`,
  `receipts:${C.RS.BUSINESS_LINE}`, `receipts:${C.RS.TENANT_LINE}`]);
const TR = C.TRANSFERS.public_housing_operating.bn;
function cellGaps(m) {
  const g = new Map();
  for (const l of m.spending.lines) for (const [k, key] of Object.entries(l.keys)) for (const al of ALLOCS) g.set(`spending:${l.id}|${k}|${al}`, key[al].target_bn + key[al].other_bn - l.national_bn);
  for (const l of m.receipts.lines) for (const [sc, cell] of Object.entries(l.cells)) for (const al of ALLOCS) g.set(`receipts:${l.id}|${sc}|${al}`, cell[al].target_bn + cell[al].other_bn - l.national_bn);
  return g;
}
let natRows = 0;
const natGap = worst(Object.keys(X).flatMap((k) => X[k].models.flatMap((m, j) => {
  const a = nationals(X.sept27.models[j]), b = nationals(m), oo = X[k].o;
  const out = Object.keys(b).filter((id) => !SPLIT.has(id) && !SYN_IDS.has(id)).map((id) => (id in a ? b[id] - a[id] : Infinity));
  for (const id of SYN_IDS) if (id in b) out.push(b[id]);
  const t = oo.housing === "tenants" ? TR : 0;
  out.push((b[`spending:${C.RENTAL}`]) - (a[`spending:${C.RENTAL}`] - t));
  out.push((b[`receipts:${C.ENTERPRISE_LINE}`] + (b[`receipts:${C.HOUSING_LINE}`] || 0) + (b[`receipts:${C.TRANSIT_LINE}`] || 0)) - (a[`receipts:${C.ENTERPRISE_LINE}`] - t));
  out.push(b[`receipts:${C.RS.BUSINESS_LINE}`] + (b[`receipts:${C.RS.TENANT_LINE}`] || 0) - a[`receipts:${C.RS.BUSINESS_LINE}`]);
  // Every executed cell keeps its partition: group + other - national is the September 27 cell's (model.json's foreign
  // and corporate cells do not partition by design), and 0 on a new line.
  const g27 = cellGaps(X.sept27.models[j]);
  for (const [id, g] of cellGaps(m)) { out.push(g27.has(id) ? g - g27.get(id) : g); natRows++; }
  return out;
})));
gate("national totals: every line but the split lines is the September 27 case's; the synthetic lines are 0; the split lines sum to their old lines less the consolidated subsidy; every executed cell's group + other less its national is the September 27 cell's, 0 on a new line (every option set and method, 1e-9)",
  natGap < 1e-9, `max |diff| ${ex(natGap)} over ${natRows} cells; national changes only on the split lines of item 1 (${C.RENTAL} -$${TR}bn; ${C.ENTERPRISE_LINE} split into ${C.HOUSING_LINE}), item 5 (${C.RS.BUSINESS_LINE} split into ${C.RS.TENANT_LINE}) and item 8 beside (${C.TRANSIT_LINE})`);

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: the overlapping lines at their rules, in the set]");
// Keys read from the models: the set's, and without 6a (the September 27 amounts on these lines; gated here).
const ruleGap = [];
for (const k of ["set", "cash"]) X[k].models.forEach((m, j) => {
  const m27 = X.sept27.models[j], k27 = C.roadKeysOf(m27);
  const no6 = C.V3PKG.modelFor("central", METHODS[j], C.v3Opts(Object.assign(withCentral(X[k].o), { payroll_items: "none" })));
  const amt = (mm, id) => C.refAmount(mm, id);
  const pay = C.PAY.items.all.central.lines;
  const t = m.candidate.v4;
  for (const a of ALLOCS) {
    const s27 = k27[a];
    // Without 6a the three lines are the September 27 case's (items 1-5 and 7 leave them).
    for (const id of [EXCISE, SALES_LINE, LICENCES, "employee_oasdi", "employer_oasdi", "self_employment_oasdi_hi"]) ruleGap.push(amt(no6, id)[a] - amt(m27, id)[a]);
    const r6 = (id) => pay[id][a].r_cal_raw;
    const sVmt = s27.s_vmt;  // the miles share reads the per-head share, which no item moves
    const nEx = lineOf(m27, "receipts", EXCISE).national_bn;
    // licences: the state index on the miles-keyed amount.
    ruleGap.push(amt(m, LICENCES)[a] - C.LIC * sVmt * C.SP_RECEIPT[LICENCES].index);
    // general sales: 6a's ratio and the state index both on the September 27 amount.
    ruleGap.push(amt(m, SALES_LINE)[a] - amt(m27, SALES_LINE)[a] * r6(SALES_LINE) * C.SP_RECEIPT[SALES_LINE].index);
    // excise: 6a's ratio on the non-gasoline part, the gasoline part at the miles share.
    ruleGap.push(amt(m, EXCISE)[a] - (r6(EXCISE) * s27.k_cons * (nEx - C.GAS) + sVmt * C.GAS));
    // the road key's freight part at the set's consumption key (6a's ratio on the September 27 key).
    ruleGap.push(t.k_road[a] - (C.FP * sVmt + (1 - C.FP) * r6(EXCISE) * s27.k_cons));
    if (k === "set") {
      // federal income tax: the cash set's (item 3's shift, 6a's ratio on it) less the fixed benefit-tax receipt.
      ruleGap.push(amt(m, FIT_LINE)[a] - (amt(X.cash.models[j], FIT_LINE)[a] - pp.receipt_bn[a]));
      ruleGap.push(amt(X.cash.models[j], FIT_LINE)[a] - ((amt(m27, FIT_LINE)[a] + C.taxEditOf("central", METHODS[j], "irs_2023_raked")[a]) * r6(FIT_LINE)));
    }
  }
});
gate("in the set and the cash set, at every allocation and method: licences = LIC x s_vmt x the state index; general sales = the September 27 amount x 6a's ratio x the state index; excise = 6a's ratio x k_cons x (national - gasoline) + s_vmt x gasoline; the road key's freight part at 6a's consumption key; federal income tax = (September 27 + item 3's shift) x 6a's ratio - the benefit-tax receipt (1e-9)",
  worst(ruleGap) < 1e-9, `max |diff| ${ex(worst(ruleGap))} over ${ruleGap.length} checks`);

// ---------------------------------------------------------------------------------------------------
// Line contributions to the cost: receipts and spending -effect, capital its return, production -(P + F), public pay.
function contributions(r) {
  const c = new Map();
  for (const l of r.evaluation.receipts) c.set(`receipts:${l.id}`, -l.effect_bn);
  for (const l of r.evaluation.spending) c.set(`spending:${l.id}`, -l.effect_bn);
  for (const k of r.capital.components) c.set(`capital:${k.id}`, k.return_bn);
  c.set("production:P", -r.evaluation.private_wtp_bn);
  c.set("production:F", -r.evaluation.induced_receipts_bn);
  c.set("public_pay", r.public_pay_bn);
  return c;
}
const sumGap = worst(Object.keys(X).flatMap((k) => X[k].runs.flatMap((xs) => [48, 11].map((i) => [...contributions(xs[i]).values()].reduce((a, b) => a + b, 0) - xs[i].cost_bn))));
const contribAt = (k) => { const out = new Map(); METHODS.forEach((_, m) => [48, 11].forEach((i, e) => { for (const [id, v] of contributions(X[k].runs[m][i])) {
  if (!out.has(id)) out.set(id, [0, 0]); out.get(id)[e] += v / METHODS.length; } })); return out; };
const lineChange = (k, base) => { const a = contribAt(k), b = contribAt(base); const ids = new Set([...a.keys(), ...b.keys()]);
  return new Map([...ids].map((id) => [id, [0, 1].map((e) => (a.get(id) || [0, 0])[e] - (b.get(id) || [0, 0])[e])])); };
function lineInteractions(setKey, ids) {
  const total = lineChange(setKey, "sept27"), parts = Object.fromEntries(ids.map((id) => [id, lineChange(`alone_${id}`, "sept27")]));
  return [...total.keys()].map((line) => {
    const t = total.get(line), alone = ids.map((id) => (parts[id].get(line) || [0, 0]));
    const sum = [0, 1].map((e) => alone.reduce((a, x) => a + x[e], 0));
    return { line, items: ids.filter((id) => TOUCH[id].includes(line)), change: t, sum_alone: sum, interaction: [t[0] - sum[0], t[1] - sum[1]] };
  }).filter((x) => x.items.length || Math.abs(x.change[0]) > 0 || Math.abs(x.change[1]) > 0);
}
const LI = { set: lineInteractions("set", IDS), cash: lineInteractions("cash", CASH_IDS) };
const aloneSum = (ids) => [0, 1].map((e) => ids.reduce((a, id) => a + fixedChange(`alone_${id}`, "sept27")[e], 0));
const joint = { set: fixedChange("set", "sept27"), cash: fixedChange("cash", "sept27") };
const inter = { set: [0, 1].map((e) => joint.set[e] - aloneSum(IDS)[e]), cash: [0, 1].map((e) => joint.cash[e] - aloneSum(CASH_IDS)[e]) };
const liSum = (k) => [0, 1].map((e) => LI[k].reduce((a, x) => a + x.interaction[e], 0));
gate("line contributions sum to each cost at 48 / 11 (every option set and method), and the line interactions to each set's interaction (1e-9)",
  sumGap < 1e-9 && ["set", "cash"].every((k) => worst([liSum(k)[0] - inter[k][0], liSum(k)[1] - inter[k][1]]) < 1e-9),
  `max |diff| ${ex(sumGap)}; interaction set ${f2(inter.set)}, cash ${f2(inter.cash)}`);

// ---------------------------------------------------------------------------------------------------
if (gateState.failures) {
  console.error(`[BLOCKED] ${gateState.failures} gate(s) failed; nothing written`);
  process.exit(1);
}

// Attribution: each item alone on the September 27 case, its marginal in the full set (the set less the set without it),
// and the difference; the same on the cash set. Pairwise interactions on the September 27 case locate the non-additivity.
const attribution = IDS.map((id) => {
  const alone = fixedChange(`alone_${id}`, "sept27"), marg = fixedChange("set", `set_minus_${id}`);
  const margC = id === "pension" ? null : fixedChange("cash", `cash_minus_${id}`);
  return { id, name: itemOf(id).name, alone, marginal_set: marg, interaction_set: [marg[0] - alone[0], marg[1] - alone[1]],
    marginal_cash: margC, interaction_cash: margC ? [margC[0] - alone[0], margC[1] - alone[1]] : null };
});
const pairs = [];
IDS.forEach((a, i) => IDS.slice(i + 1).forEach((b) => {
  const d = fixedChange(`pair_${a}_${b}`, "sept27"), da = fixedChange(`alone_${a}`, "sept27"), db = fixedChange(`alone_${b}`, "sept27");
  pairs.push({ a, b, interaction: [d[0] - da[0] - db[0], d[1] - da[1] - db[1]] });
}));
const pairSum = (ids) => [0, 1].map((e) => pairs.filter((p) => ids.includes(p.a) && ids.includes(p.b)).reduce((s, p) => s + p.interaction[e], 0));
const higher = { set: [0, 1].map((e) => inter.set[e] - pairSum(IDS)[e]), cash: [0, 1].map((e) => inter.cash[e] - pairSum(CASH_IDS)[e]) };

// The rules: each alternative's set against the chosen set, at 48 / 11.
const ruleRows = ALTS.map((a) => ({ field: a.field, value: a.value, chosen: RULES[a.field], base: a.base,
  cost: fixedCost(`${a.base}_${a.field}_${a.value}`), change: fixedChange(`${a.base}_${a.field}_${a.value}`, a.base) }));
const ruleOf = (field, value, base) => ruleRows.find((r) => r.field === field && r.value === value && r.base === base);
// Group amounts on the overlapping lines in the set, and each item's change to them alone (48 / 11, methods averaged).
const lineAmt = (k, side, id) => atEnds((m, i) => { const r = row(X[k].runs[m][i], side, id); return r ? r.amount_bn : 0; });
const ch = (k, side, id) => { const a = lineAmt(k, side, id), b = lineAmt("sept27", side, id); return [a[0] - b[0], a[1] - b[1]]; };
const pr = (x) => `${fx(x[0])} / ${fx(x[1])}`;
const rr = (id) => C.PAY.items.all.central.lines[id];
const rrs = (id) => `${rr(id).personal.r_cal_raw.toFixed(4)} personal, ${rr(id).shared.r_cal_raw.toFixed(4)} shared`;
const OVERLAPS = [
  { line: "receipts:personal_motor_vehicle", items: ["state", "roads"], kind: "both move the line",
    does: { state: `x the state index ${C.SP_RECEIPT[LICENCES].index.toFixed(4)} on the group's amount (California's vehicle licence fee)`,
      roads: "re-keyed from the adults key to the group's share of driver miles" },
    rule: "licence_rule", why: "the index is a price and the miles share a quantity: price x quantity. The index weights states by the group's adults, so it assumes the group's miles are spread across states like its adults" },
  { line: "receipts:general_sales_tax", items: ["6a", "state"], kind: "both move the line",
    does: { "6a": `x 6a's ratio (${rrs(SALES_LINE)}: the group's measured consumption scaled for misreported income)`, state: `x the state index ${C.SP_RECEIPT[SALES_LINE].index.toFixed(4)} (Texas, Arizona and others tax sales above the US rate)` },
    rule: "sales_rule", why: "the ratio corrects the quantity (consumption) and the index the rate per dollar: both multiply" },
  { line: "receipts:excise_selective_sales", items: ["6a", "roads"], kind: "both move the line",
    does: { "6a": `x 6a's ratio (${rrs(EXCISE)}) on the whole line`, roads: `the gasoline part ($${C.GAS.toFixed(3)}bn of $${lineOf(C.MODEL, "receipts", EXCISE).national_bn}bn) re-keyed from the consumption key to the miles share` },
    rule: "excise_rule", why: "the miles share is measured driving, not income-based consumption, so 6a's income-misreporting ratio has nothing to scale on the gasoline part; it stays on the rest" },
  { line: "road key (freight part) -> spending:roads_vmt_sl, roads_vmt_fed, capital:hwy_sl, hwy_fed", items: ["6a", "roads"], kind: "roads reads a key 6a moves",
    does: { "6a": `raises the group's consumption key (read from the excise line) by its ratio (${rrs(EXCISE)})`, roads: `keys freight's ${(100 * (1 - C.FP)).toFixed(1)}% of highway cost at the consumption key` },
    rule: "freight_key", why: "one consumption key across the account: if the group consumes 6a's ratio more, it also buys that much more of what freight hauls" },
  { line: "receipts:federal_income_tax", items: ["3", "6a", "pension"], kind: "all three move the line",
    does: { 3: "adds the IRS-matched key's shift (stack factor x national x share change)", "6a": `x 6a's ratio (${rrs(FIT_LINE)}), applied after item 3 (v3's order)`,
      pension: `drops the tax the group's 2024 benefits carry ($${pp.receipt_bn.shared.toFixed(3)}bn shared, $${pp.receipt_bn.personal.toFixed(3)}bn personal)` },
    rule: "benefit_tax_rule", why: "the brief's re-pin drops the lane's measured dollars; the lane measured them on the Census key, and neither item 3 (a re-key by AGI bin) nor 6a says how much of its change falls on benefits" },
  { line: "OASDI receipts -> spending:social_security", items: ["6a", "pension"], kind: "the accrual reads receipts 6a moves",
    does: { "6a": `moves employee and employer OASDI (x ${rrs("employee_oasdi")}) and self-employment tax (x ${rrs(C.SE_LINE)})`, pension: "sets social_security to ratio_net x the group's OASDI receipts" },
    rule: "accrual_receipts", why: "payroll tax buys the accrual, so the accrual follows the receipts the set itself books (v3's rule)" },
  { line: "HI receipts -> spending:medicare (Part A accrual)", items: ["6a", "pension"], kind: "a read the switch does not make",
    does: { "6a": "moves employee and employer HI and self-employment tax", pension: "swaps Part A's cash share for the lane's Part A accrual, a fixed amount" },
    rule: "part_a_rule", why: "the lane's Part A accrual comes from its lifetime model of covered workers, not from the case's HI receipts (v3's rule)" },
];
const overlapRows = OVERLAPS.map((o) => {
  const [side, id] = o.line.includes(" ") ? [null, null] : o.line.split(":");
  const alts = ruleRows.filter((r) => r.field === o.rule);
  return Object.assign({}, o, {
    set_amount: side ? lineAmt("set", side, id) : null, sept27_amount: side ? lineAmt("sept27", side, id) : null,
    item_changes: side ? Object.fromEntries(o.items.map((it) => [it, ch(`alone_${it}`, side, id)])) : null,
    set_change: side ? ch("set", side, id) : null,
    line_interaction: side ? (LI.set.find((x) => x.line === o.line) || { interaction: [0, 0] }).interaction : null,
    chosen: RULES[o.rule], alternatives: alts.map((r) => ({ value: r.value, base: r.base, cost: r.cost, change: r.change })) });
});
// Item 3 x 6a on the federal income tax (v3's order, no option): the additive alternative is the pairwise interaction away.
const i36 = pairs.find((p) => p.a === "3" && p.b === "6a").interaction;

// Beside: items 8 and 10 on the set and the cash set.
const beside = BESIDE_ITEMS.map((it) => ({ id: it.id, name: it.name, alone: fixedChange(`alone_${it.id}`, "sept27"),
  on_set: fixedChange(`set_plus_${it.id}`, "set"), on_cash: fixedChange(`cash_plus_${it.id}`, "cash") }));
// Beside: state pricing on the S&L capital of the three re-priced lines, if that capital were priced by the same index as
// the lines' S&L spending (the lane priced current spending only). S&L totals: the POS functions that split NIPA's S&L
// POS (the corrections row, not its per-prisoner part), health's and recreation's S&L amounts.
const SL_TOTAL = {
  public_order_safety: C.SP_SPEND.concat(csvRows(`${C.SP_DIR}/corrections.csv`).filter((r) => r.function === "corrections"))
    .filter((r) => r.line === "public_order_safety" && r.function !== "corrections_per_inmate").reduce((a, r) => a + Number(r.sl_amount_bn), 0),
  health_services: Number(C.SP_SPEND.find((r) => r.line === "health_services").sl_amount_bn),
  recreation_culture: Number(C.SP_SPEND.find((r) => r.line === "recreation_culture").sl_amount_bn),
};
const SL_CAPITAL = { public_order_safety: "pos_sl", health_services: "health_sl", recreation_culture: "rec_sl" };
const stateCapitalOf = (k, ids) => atEnds((m, i) => ids.reduce((a, id) => a + comp(X[k].runs[m][i], SL_CAPITAL[id]).return_bn * C.SP_PRE[id] / SL_TOTAL[id], 0));
const stateCapital = (k) => stateCapitalOf(k, SP_LINES);
// Beside: lines item 5 makes live at a nonzero response that the state-pricing lane left national because they sat at
// response 0 (its receipts_corrections.csv notes). No state index exists for them.
const gapLines = [C.RS.TENANT_LINE, C.RS.PERSONAL_LINE].map((id) => ({ id, amount: lineAmt("set", "receipts", id),
  effect: atEnds((m, i) => row(X.set.runs[m][i], "receipts", id).effect_bn), response: atEnds((m, i) => row(X.set.runs[m][i], "receipts", id).response) }));

// Bands, ends and per member.
const perMember = (bn) => bn * 1e9 / C.COUNT;
const bandRows = [["sept27", "the September 27 case (adopted)"], ["set", "candidate v4: the set with the pension switch (payable, net)"],
  ["cash", "candidate v4: the cash set (pension switch off)"], ["set_plus_8", "the set with item 8 (beside)"], ["set_plus_10", "the set with item 10 (beside)"],
  ["cash_plus_8", "the cash set with item 8 (beside)"], ["cash_plus_10", "the cash set with item 10 (beside)"]];
const endsInfo = (k) => METHODS.map((meth, m) => {
  const x = X[k], c = x.costs[m];
  const up = x.idx.slice().sort((a, b) => c[a] - c[b] || a - b), down = x.idx.slice().sort((a, b) => c[b] - c[a] || a - b);
  return { method: meth, low: up[0], low_cost: c[up[0]], low_runner_up: up[1], low_margin: c[up[1]] - c[up[0]],
    high: down[0], high_cost: c[down[0]], high_runner_up: down[1], high_margin: c[down[0]] - c[down[1]] };
});
const ownBand = (k) => [0, 1].map((e) => mean(E[k].map((ends, m) => X[k].costs[m][ends[e]])));

// ---------------------------------------------------------------------------------------------------
// Outputs.
const bandsCsv = ["case,label,method,spec48_bn,spec11_bn,per_member_spec48_usd,per_member_spec11_usd,own_low_spec,own_high_spec,own_low_bn,own_high_bn"];
for (const [k, label] of bandRows) {
  METHODS.forEach((meth, m) => bandsCsv.push([k, `"${label}"`, meth, fx(X[k].costs[m][48]), fx(X[k].costs[m][11]), perMember(X[k].costs[m][48]).toFixed(0),
    perMember(X[k].costs[m][11]).toFixed(0), E[k][m][0], E[k][m][1], fx(X[k].costs[m][E[k][m][0]]), fx(X[k].costs[m][E[k][m][1]])].join(",")));
  const ob = ownBand(k);
  bandsCsv.push([k, `"${label}"`, "mean", fx(B[k][0]), fx(B[k][1]), perMember(B[k][0]).toFixed(0), perMember(B[k][1]).toFixed(0),
    at4811(E[k]) ? 48 : "", at4811(E[k]) ? 11 : "", fx(ob[0]), fx(ob[1])].join(","));
}
const pair2 = (x) => (x ? [fx(x[0]), fx(x[1])] : ["", ""]);
const attrCsv = ["item,label,alone_spec48_bn,alone_spec11_bn,marginal_in_set_spec48_bn,marginal_in_set_spec11_bn,interaction_in_set_spec48_bn,interaction_in_set_spec11_bn,"
  + "marginal_in_cash_spec48_bn,marginal_in_cash_spec11_bn,interaction_in_cash_spec48_bn,interaction_in_cash_spec11_bn"]
  .concat(attribution.map((a) => [a.id, `"${a.name}"`, ...pair2(a.alone), ...pair2(a.marginal_set), ...pair2(a.interaction_set), ...pair2(a.marginal_cash), ...pair2(a.interaction_cash)].join(",")))
  .concat([["sum_alone", "\"sum of the items alone\"", ...pair2(aloneSum(IDS)), "", "", "", "", ...pair2(aloneSum(CASH_IDS)), "", ""].join(","),
    ["joint", "\"the set's change from the September 27 case (set; cash set)\"", ...pair2(joint.set), "", "", "", "", ...pair2(joint.cash), "", ""].join(","),
    ["interaction_total", "\"joint less the sum alone (set; cash set)\"", ...pair2(inter.set), "", "", "", "", ...pair2(inter.cash), "", ""].join(","),
    ["interaction_pairwise", "\"sum of the pairwise interactions on the September 27 case\"", ...pair2(pairSum(IDS)), "", "", "", "", ...pair2(pairSum(CASH_IDS)), "", ""].join(","),
    ["interaction_higher_order", "\"total less the pairwise sum\"", ...pair2(higher.set), "", "", "", "", ...pair2(higher.cash), "", ""].join(",")]);
const pairCsv = ["item_a,item_b,interaction_spec48_bn,interaction_spec11_bn"].concat(pairs.map((p) => [p.a, p.b, f6(p.interaction[0]), f6(p.interaction[1])].join(",")));
const liCsv = ["set,line,items_moving_it,change_spec48_bn,change_spec11_bn,sum_of_items_alone_spec48_bn,sum_of_items_alone_spec11_bn,interaction_spec48_bn,interaction_spec11_bn"]
  .concat(["set", "cash"].flatMap((k) => LI[k].map((x) => [k, x.line, x.items.join("+"), f6(x.change[0]), f6(x.change[1]), f6(x.sum_alone[0]), f6(x.sum_alone[1]),
    f6(x.interaction[0]), f6(x.interaction[1])].join(","))));
const ovCsv = ["line,items,kind,rule,value,chosen,base,set_cost_spec48_bn,set_cost_spec11_bn,change_from_chosen_spec48_bn,change_from_chosen_spec11_bn"];
for (const o of overlapRows) {
  for (const base of ["set", "cash"]) {
    if (PENSION_RULES.includes(o.rule) && base === "cash") continue;
    ovCsv.push([`"${o.line}"`, o.items.join("+"), `"${o.kind}"`, o.rule, o.chosen, "yes", base, fx(B[base][0]), fx(B[base][1]), fx(0), fx(0)].join(","));
    for (const a of o.alternatives.filter((x) => x.base === base)) ovCsv.push([`"${o.line}"`, o.items.join("+"), `"${o.kind}"`, o.rule, a.value, "no", base,
      fx(a.cost[0]), fx(a.cost[1]), fx(a.change[0]), fx(a.change[1])].join(","));
  }
}
for (const base of ["set", "cash"]) ovCsv.push(["\"receipts:federal_income_tax\"", "3+6a", "\"6a's ratio after item 3's shift (v3's order)\"", "item3_6a_order", "ratio_on_rekeyed_amount", "yes", base,
  fx(B[base][0]), fx(B[base][1]), fx(0), fx(0)].join(","), ["\"receipts:federal_income_tax\"", "3+6a", "\"6a's ratio after item 3's shift (v3's order)\"", "item3_6a_order",
  "additive", "no", base, fx(B[base][0] - i36[0]), fx(B[base][1] - i36[1]), fx(-i36[0]), fx(-i36[1])].join(","));

const ITEM_COLS = IDS.concat(BESIDE_ITEMS.map((it) => it.id));
const perHead = ["method", "spec", "twin", "allocation", "normalization", "share", "reading", "gg", "uc", "rate", "sept27_cost_bn", "set_cost_bn", "cash_cost_bn",
  "set_plus_8_bn", "set_plus_10_bn", "cash_plus_8_bn", "cash_plus_10_bn", ...ITEM_COLS.map((id) => `alone_${id}_change_bn`), ...IDS.map((id) => `marginal_in_set_${id}_bn`),
  "road_key", "state_price_spending_bn", "licences_amount_bn", "social_security_bn", "federal_income_tax_bn"];
const perSpec = [perHead.join(",")].concat(METHODS.flatMap((meth, m) => X.set.idx.map((i) => {
  const s = X.set.specs[i], r = X.set.runs[m][i];
  return [meth, i, twinOf(X.set, i), s.allocation, s.normalization, s.share, s.reading, s.gg, s.uc, s.rate, X.sept27.costs[m][i], X.set.costs[m][i], X.cash.costs[m][i],
    X.set_plus_8.costs[m][i], X.set_plus_10.costs[m][i], X.cash_plus_8.costs[m][i], X.cash_plus_10.costs[m][i],
    ...ITEM_COLS.map((id) => X[`alone_${id}`].costs[m][i] - X.sept27.costs[m][i]), ...IDS.map((id) => X.set.costs[m][i] - X[`set_minus_${id}`].costs[m][i]),
    X.set.models[m].candidate.v4.k_road[s.allocation], SP_LINES.reduce((a, id) => a - row(r, "spending", SP_SYN[id]).effect_bn, 0),
    row(r, "receipts", LICENCES).amount_bn, row(r, "spending", SS_LINE).amount_bn, row(r, "receipts", FIT_LINE).amount_bn].map(full).join(",");
})));

const inputs = [C.PENSION_FILE, `${C.SP_DIR}/net_state_correction.csv`, `${C.SP_DIR}/corrections.csv`, `${C.SP_DIR}/receipts_corrections.csv`,
  `${C.RD_DIR}/inputs.json`, `${C.RD_DIR}/summary.json`, `${C.RD_DIR}/keys.csv`, `${V3_DIR}/summary.json`, `${V3_DIR}/fixed_specs.csv`,
  `${SEPT27_DIR}/summary.json`, `${SEPT27_DIR}/per_spec.csv`, C.COUNT_FILE, `${C.LANE}/package.cjs`, "main_case_candidate_v3_2026_09_28/package.cjs",
  "main_case_candidate_v2_2026_09_28/package.cjs", "main_case_candidate_2026_09_28/package.cjs", "main_case_long_run_2026_09_27/package.cjs",
  "receipt_side_long_run_2026_09_28/items.cjs", C.PAYROLL_FILE, C.WC_FILE, "assumption_explorer_2026_09_21/engine.js"];
const summary = {
  lane: C.LANE, case: C.CASE, status: "candidate, not adopted (the parent's brief, 2026-09-29)",
  imports: "main_case_candidate_v3_2026_09_28/package.cjs (f878343), which imports v2, the first candidate and main_case_long_run_2026_09_27/package.cjs; none edited",
  count: { value: C.COUNT, file: C.COUNT_FILE, key: "populations.row4" },
  bands: Object.fromEntries(bandRows.map(([k, label]) => [k, { label, at_48_11_bn: B[k], per_member_usd: B[k].map(perMember),
    by_method: Object.fromEntries(METHODS.map((meth, m) => [meth, [X[k].costs[m][48], X[k].costs[m][11]]])),
    own_ends: E[k], own_band_bn: ownBand(k), ends: endsInfo(k) }])),
  items: SET_ITEMS.map((it) => ({ id: it.id, name: it.name, options: it.o })), beside_items: BESIDE_ITEMS.map((it) => ({ id: it.id, name: it.name, options: it.o })),
  rules_chosen: RULES,
  attribution: { items: attribution, sum_alone: { set: aloneSum(IDS), cash: aloneSum(CASH_IDS) }, joint, interaction: inter, pairwise_sum: { set: pairSum(IDS), cash: pairSum(CASH_IDS) },
    higher_order: higher, pairs },
  line_interactions: LI, touch: TOUCH, shared_lines: SHARED,
  overlaps: overlapRows, item3_6a_order: { rule: "6a's ratio applies after item 3's shift (v3's order)", additive_alternative_change_bn: [-i36[0], -i36[1]] },
  rules: ruleRows, beside: { items: beside, state_price_on_sl_capital_bn: { set: stateCapital("set"), cash: stateCapital("cash"), sl_totals_bn: SL_TOTAL,
    by_line_set: Object.fromEntries(SP_LINES.map((id) => [id, stateCapitalOf("set", [id])])),
    rule: "sum over the three lines of the S&L capital return x (sum_f S&L_f (index_f - 1)) / the line's S&L total; not in the set" }, item5_lines_not_state_priced: gapLines },
  gates_reproduced: { v3_rows: v3Gaps, state: { per_line: perLine, receipts: recLine }, roads_parts: rdParts, pension: { alone_bn: nP, change_bn: dP } },
  pension: Object.assign({}, pp),
  inputs: Object.fromEntries(inputs.map((f) => [f, C.sha256(f)])),
};
fs.mkdirSync(OUT, { recursive: true });
const write = (name, lines) => fs.writeFileSync(path.join(OUT, name), lines.join("\n") + "\n");
write("bands.csv", bandsCsv);
write("attribution.csv", attrCsv);
write("pairwise.csv", pairCsv);
write("line_interactions.csv", liCsv);
write("overlaps.csv", ovCsv);
write("per_spec.csv", perSpec);
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(summary, null, 1) + "\n");

console.log("\n[result]");
for (const [k] of bandRows) console.log(`  ${k.padEnd(14)} ${f2(B[k])}  per member $${perMember(B[k][0]).toFixed(0)} / $${perMember(B[k][1]).toFixed(0)}  ends ${E[k].map((e) => e.join("/")).join(" ")}  own ${f2(ownBand(k))}`);
for (const a of attribution) console.log(`  ${a.id.padEnd(8)} alone ${f2(a.alone)}  marginal ${f2(a.marginal_set)}  interaction ${f2(a.interaction_set)}  cash ${a.marginal_cash ? f2(a.marginal_cash) : "-"}`);
console.log(`  sum alone ${f2(aloneSum(IDS))} joint ${f2(joint.set)} interaction ${f2(inter.set)} (pairwise ${f2(pairSum(IDS))}, higher ${f2(higher.set)})`);
console.log(`  cash: sum alone ${f2(aloneSum(CASH_IDS))} joint ${f2(joint.cash)} interaction ${f2(inter.cash)} (pairwise ${f2(pairSum(CASH_IDS))}, higher ${f2(higher.cash)})`);
for (const p of pairs.filter((q) => Math.abs(q.interaction[0]) > 1e-9 || Math.abs(q.interaction[1]) > 1e-9)) console.log(`  pair ${p.a} x ${p.b}: ${f6(p.interaction[0])} / ${f6(p.interaction[1])}`);
for (const x of LI.set.filter((y) => Math.abs(y.interaction[0]) > 1e-9 || Math.abs(y.interaction[1]) > 1e-9)) console.log(`  line ${x.line} [${x.items.join("+")}]: ${f6(x.interaction[0])} / ${f6(x.interaction[1])}`);
for (const r of ruleRows) console.log(`  rule ${r.base} ${r.field}=${r.value} (chosen ${r.chosen}): ${f6(r.change[0])} / ${f6(r.change[1])}`);
console.log(`  3 x 6a order: additive alternative ${f6(-i36[0])} / ${f6(-i36[1])}`);
for (const b of beside) console.log(`  beside ${b.id}: alone ${f2(b.alone)} on set ${f2(b.on_set)} on cash ${f2(b.on_cash)}`);
console.log(`  beside: state pricing on S&L capital ${f2(stateCapital("set"))}; item 5 lines ${gapLines.map((g) => `${g.id} effect ${f2(g.effect)}`).join("; ")}`);
console.log(`  shared lines: ${SHARED.map((s) => `${s.line} [${s.items.join("+")}]`).join("; ")}`);
console.log("all gates passed");
