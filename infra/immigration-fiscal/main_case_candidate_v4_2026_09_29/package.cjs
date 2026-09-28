/* Candidate v4: the operator's pending bundle run as one set, case sept29_candidate_v4 (the parent's brief of
 * 2026-09-29), not adopted. It imports candidate v3's package (../main_case_candidate_v3_2026_09_28/package.cjs, f878343)
 * unchanged, which imports v2, the first candidate and the September 27 case unchanged. Every item is an option, so each
 * can be taken alone; with every option off (OFF) the package is the September 27 case.
 *
 * The set (SET_ITEMS; CASH is the set with the pension switch off):
 *   1-5.     v3's items 1-5, unchanged (v3 options).
 *   6a.      v3's item 6a under the payroll lane's proportional rule (payroll_items "central", payroll_rule "proportional");
 *            6b stays off (row2_rule "proportional"), as the cross-lab review revised it.
 *   7.       wc "pooled_workers_compensation": v3's pooled 2019-2024 ratio on the workers_compensation line only (the review
 *            moved temporary disability and black lung out: they are ASEC disability or survivor income, not WC_VAL).
 *   pension. pension4 "payable_net": social_security = ratio_net x the group's OASDI receipts; medicare swaps its Part A
 *            share for the Part A accrual; federal_income_tax loses the tax the group's 2024 benefits carry
 *            (benefit_tax.current_receipt_bn, per allocation). Read from pension_accrual_2026_09_28/derived/summary.json at
 *            PENSION_COMMIT through git, with its hash. v3's own switch (gross, c9d0077) is blocked here.
 *   state.   state_price "central": the state-pricing lane's central package (state_priced_services_2026_09_29, ea41242).
 *            Spending: one synthetic line per re-priced line (public order and safety, health, recreation), whose group
 *            amount is sum_f S&L_f x (index_f - 1) x the parent line's key and whose response is the parent's; synthetic
 *            lines leave the parents' keys, and so the capital components keyed on them, where the lane left them.
 *            Receipts: general_sales_tax and personal_motor_vehicle move by (S&L / national) x (index - 1) x the group's
 *            amount, expanded to every incidence rule.
 *   roads.   roads "miles": the roads lane's re-key (roads_mileage_key_2026_09_29, 30b5468), its formulas re-implemented
 *            (rekey.cjs is a script, not a module) and gated against its outputs: two synthetic highway lines at the
 *            subfunction responses, gasoline taxes and personal licences re-keyed to the group's share of driver miles,
 *            and hwy_sl / hwy_fed keyed at the road key on the evaluation.
 * Beside the set: v3's items 8 (transit) and 10 (uninsured use at 0.7x), v3 options.
 *
 * Where two items touch one line, the composition is an option, so each alternative is one run (RULES holds the rules
 * chosen; each rule matters only when both of its items are on, and each item alone is its own lane):
 *   licence_rule      personal_motor_vehicle, state x roads: "index_on_miles" (the state index applied to the miles-keyed
 *                     amount), "additive" (each lane's change on the adults key), "miles_only", "index_only".
 *   sales_rule        general_sales_tax, 6a x state: "multiplicative" (the index on the 6a amount) or "additive".
 *   excise_rule       excise_selective_sales, 6a x roads: "gasoline_at_miles" (the gasoline part at the miles share, 6a's
 *                     ratio on the rest), "additive" (6a's ratio kept on the gasoline part's September 27 share),
 *                     "multiplicative" (6a's ratio on the miles-keyed gasoline too).
 *   freight_key       the road key's freight part, read from the excise line's key: "set" (after 6a) or "sept27".
 *   benefit_tax_rule  federal_income_tax, 3 x 6a x pension: "fixed" (the lane's dollars) or "proportional" (scaled by the
 *                     group's federal income tax in the set over the September 27 case's).
 *   accrual_receipts  the OASDI receipts the accrual reads, 6a x pension: "set" (v3's rule) or "sept27".
 *   part_a_rule       the Part A accrual: "fixed" (v3's rule) or "hi_scaled" (by the group's HI receipts, set over
 *                     September 27).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");
const V3 = require(path.join(__dirname, "..", "main_case_candidate_v3_2026_09_28", "package.cjs"));
const P = V3.SEPT27;
const { Engine, MODEL, FISCAL, METHODS, ALLOCS, readJson, csvRows, span, mean2, lineOf } = V3;

const HERE = __dirname;
const ROOT = V3.ROOT;
const CASE = "sept29_candidate_v4";
const LANE = "main_case_candidate_v4_2026_09_29";
const REF = MODEL.receipts.reference;
const byAlloc = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
const refAmount = (m, id) => byAlloc((a) => lineOf(m, "receipts", id).cells[REF][a].target_bn);
const withEdits = (m, edits, lines) => Engine.applyCorrections(m, { lines: lines || [], edits, meta: m.corrections });
const sha256Buf = (buf) => crypto.createHash("sha256").update(buf).digest("hex");

// ---------------------------------------------------------------------------------------------------
// Item 7: v3's pooled ratio on the workers_compensation line only.
const WC_LINE = "workers_compensation";
if (!V3.WC_LINES.includes(WC_LINE)) throw new Error(`[BLOCKED] ${V3.WC_FILE}: no ${WC_LINE} among its lines`);
function withWorkersCompOnly(m) {
  const k = lineOf(m, "spending", WC_LINE).keys[V3.WC_KEY];
  return withEdits(m, P.expand([{ side: "spending", line: WC_LINE, key: V3.WC_KEY, by: byAlloc((a) => (V3.WC[a].ratio - 1) * k[a].target_bn) }]));
}

// ---------------------------------------------------------------------------------------------------
// The pension switch at payable benefits, net of the income tax on benefits.
const PENSION_FILE = "pension_accrual_2026_09_28/derived/summary.json";
const PENSION_COMMIT = "9ea1beb";
const SS_LINE = V3.SS_LINE, MEDICARE_LINE = V3.MEDICARE_LINE, FIT_LINE = "federal_income_tax";
const OASDI_LINES = V3.OASDI_LINES, SE_LINE = V3.SE_LINE, HI_LINES = ["employee_hi", "employer_hi"];
let pensionCache = null;
function pensionNet() {
  if (pensionCache) return pensionCache;
  const rel = `infra/immigration-fiscal/${PENSION_FILE}`;
  const show = (rev) => execFileSync("git", ["-C", ROOT, "show", `${rev}:${rel}`], { maxBuffer: 1 << 26, stdio: ["ignore", "pipe", "ignore"] });
  let buf;
  try { buf = show(PENSION_COMMIT); } catch (e) { throw new Error(`[BLOCKED] ${PENSION_FILE} is not in commit ${PENSION_COMMIT}`); }
  const J = JSON.parse(buf.toString("utf8"));
  const d = J.central_decomposition, dn = J.central_decomposition_net, at = J.case_components_attrs, bt = J.benefit_tax;
  const bad = (why) => { throw new Error(`[BLOCKED] ${PENSION_FILE} at ${PENSION_COMMIT}: ${why}`); };
  if (!J.central || J.central.scenario !== "payable") bad("the central is not payable benefits");
  if (J.ends.low !== 48 || J.ends.high !== 11) bad("its ends are not 48 / 11");
  if (!(dn.low.accrual_per_tax_dollar_net === J.ratio_net && dn.high.accrual_per_tax_dollar_net === J.ratio_net)) bad("ratio_net is not the net central's ratio at both ends");
  if (d.low.part_a_accrual_bn !== d.high.part_a_accrual_bn) bad("the Part A accrual differs between the ends");
  if (Math.abs(at.part_a_share - V3.PART_A.hi_bn / V3.PART_A.total_bn) > 1e-12 || !(at.se_oasdi_share > 0 && at.se_oasdi_share < 1)) bad("Part A's share is not HI 416.3 / 1,109.8");
  const alloc = bt.current_receipt_allocation;
  if (!alloc || alloc.low !== "shared" || alloc.high !== "personal") bad("the benefit-tax receipt is not shared at the low end and personal at the high end");
  if (!ALLOCS.every((a) => Number.isFinite(bt.current_receipt_bn[a === "shared" ? "low" : "high"]))) bad("no benefit-tax receipt");
  const head = sha256Buf(show("HEAD")), work = sha256Buf(fs.readFileSync(path.join(ROOT, rel)));
  pensionCache = {
    file: PENSION_FILE, commit: PENSION_COMMIT, sha256: sha256Buf(buf), same_at_head: head === sha256Buf(buf), same_in_working_tree: work === sha256Buf(buf),
    ratio_net: J.ratio_net, part_a_accrual_bn: d.low.part_a_accrual_bn, part_a_share: at.part_a_share, se_oasdi_share: at.se_oasdi_share,
    receipt_bn: { shared: bt.current_receipt_bn.low, personal: bt.current_receipt_bn.high },
    case_bn: [J.case_bn.low, J.case_bn.high], case_on_accrual_net_bn: [J.case_on_accrual_net_bn.low, J.case_on_accrual_net_bn.high],
    delta_net_bn: [dn.low.delta_net_bn, dn.high.delta_net_bn], central: J.central, scheduled_ratio_net: J.scheduled_arm.decomposition_net.low.accrual_per_tax_dollar_net,
  };
  return pensionCache;
}
// The group's OASDI receipts on the reference rule (employee and employer OASDI plus the OASDI share of self-employment
// tax), and its HI receipts (employee and employer HI plus the rest of self-employment tax).
const oasdiOf = (m) => { const pp = pensionNet(); return byAlloc((a) => OASDI_LINES.reduce((s, id) => s + refAmount(m, id)[a], 0) + pp.se_oasdi_share * refAmount(m, SE_LINE)[a]); };
const hiOf = (m) => { const pp = pensionNet(); return byAlloc((a) => HI_LINES.reduce((s, id) => s + refAmount(m, id)[a], 0) + (1 - pp.se_oasdi_share) * refAmount(m, SE_LINE)[a]); };
// refs: {oasdi, fitScale, partAScale}, each by allocation, from the composition rules.
function withPensionNet(m, refs) {
  const pp = pensionNet();
  const ss = lineOf(m, "spending", SS_LINE), med = lineOf(m, "spending", MEDICARE_LINE);
  const ks = ss.keys[ss.preferred_key], km = med.keys[med.preferred_key];
  return withEdits(m, [
    { side: "spending", line: SS_LINE, key: ss.preferred_key, by: byAlloc((a) => pp.ratio_net * refs.oasdi[a] - ks[a].target_bn) },
    { side: "spending", line: MEDICARE_LINE, key: med.preferred_key, by: byAlloc((a) => pp.part_a_accrual_bn * refs.partAScale[a] - pp.part_a_share * km[a].target_bn) },
  ].concat(P.expand([{ side: "receipt", line: FIT_LINE, by: byAlloc((a) => -pp.receipt_bn[a] * refs.fitScale[a]) }])));
}

// ---------------------------------------------------------------------------------------------------
// State pricing: the lane's central package, read from its derived files.
const SP_DIR = "state_priced_services_2026_09_29/derived";
const SP_PACKAGE = "central_all_sl_subfunctions";
const SP_NET = csvRows(`${SP_DIR}/net_state_correction.csv`).filter((r) => r.package === SP_PACKAGE);
const SP_SPEND = csvRows(`${SP_DIR}/corrections.csv`).filter((r) => r.candidate === "True");
const SP_REC = csvRows(`${SP_DIR}/receipts_corrections.csv`).filter((r) => r.candidate === "True");
if (SP_NET.length !== 2 || SP_NET[0].functions !== SP_NET[1].functions
  || SP_NET[0].functions.split("+").sort().join() !== SP_SPEND.map((r) => r.function).sort().join()) {
  throw new Error(`[BLOCKED] ${SP_DIR}: the central package's functions are not the candidate rows of corrections.csv`);
}
const SP_TARGET = Object.fromEntries(SP_NET.map((r) => [r.end, { spending: Number(r.spending_bn), receipts: Number(r.receipts_gain_bn), net: Number(r.net_cost_bn) }]));
const SP_LINES = [...new Set(SP_SPEND.map((r) => r.line))];
const SP_SYN = Object.fromEntries(SP_LINES.map((id) => [id, `state_price_${id}`]));
// Per parent line: sum_f S&L_f x (index_f - 1), $bn at national scale; the group's part is that times the line's key.
const SP_PRE = Object.fromEntries(SP_LINES.map((id) => [id, SP_SPEND.filter((r) => r.line === id).reduce((s, r) => s + Number(r.sl_amount_bn) * (Number(r.index) - 1), 0)]));
// Per receipt line: (S&L / national) x (index - 1), the factor on the group's amount.
const SP_RECEIPT = Object.fromEntries(SP_REC.map((r) => [r.line, { factor: Number(r.sl_amount_bn) / Number(r.national_bn) * (Number(r.index) - 1),
  index: Number(r.index), sl_bn: Number(r.sl_amount_bn), national_bn: Number(r.national_bn) }]));
const SALES_LINE = "general_sales_tax", LICENCES = "personal_motor_vehicle", EXCISE = "excise_selective_sales";
if (Object.keys(SP_RECEIPT).sort().join() !== [LICENCES, SALES_LINE].sort().join()) throw new Error(`[BLOCKED] ${SP_DIR}: the receipt lines are not ${SALES_LINE} and ${LICENCES}`);
for (const [id, v] of Object.entries(SP_RECEIPT)) {
  if (Math.abs(lineOf(MODEL, "receipts", id).national_bn - v.national_bn) > 1e-9) throw new Error(`[BLOCKED] ${id}: the lane's national is not model.json's`);
}
// The evaluated key of each parent line: public order and safety takes the specification's justice key (every
// specification of the case uses "use"; specsFor() stops otherwise), the others their preferred key.
const SP_KEY = { public_order_safety: "use" };
const parentKey = (l) => SP_KEY[l.id] || l.preferred_key;
function withStatePrice(m, amounts) {
  const lines = SP_LINES.map((id) => ({ id: SP_SYN[id], family: "consumption", response_class: "service",
    label: `${id} priced where the group lives (state-pricing lane, central package; candidate)` }));
  const edits = SP_LINES.map((id) => {
    const l = lineOf(m, "spending", id), k = l.keys[parentKey(l)];
    return { side: "spending", line: SP_SYN[id], key: "k", by: byAlloc((a) => SP_PRE[id] * k[a].target_bn / l.national_bn) };
  });
  const shifts = Object.keys(SP_RECEIPT).filter((id) => amounts[id]).map((id) => ({ side: "receipt", line: id, by: byAlloc((a) => SP_RECEIPT[id].factor * amounts[id][a]) }));
  return withEdits(m, edits.concat(P.expand(shifts)), lines);
}

// ---------------------------------------------------------------------------------------------------
// Roads keyed by miles: the lane's inputs and formulas (rekey.cjs modelKeys, vmtShares, keysFor, engineRun).
const RD_DIR = "roads_mileage_key_2026_09_29/derived";
const RD_IN = readJson(`${RD_DIR}/inputs.json`);
const RD_SUM = readJson(`${RD_DIR}/summary.json`);
const RD_RATIO = RD_SUM.central_ratio;
if (RD_RATIO !== "2017_southwest" || !RD_IN.gates.length || !RD_IN.gates.every((g) => g.pass === true) || !RD_SUM.gates.every((g) => g.pass === true)) {
  throw new Error(`[BLOCKED] ${RD_DIR}: not the lane's central ratio, or a gate did not pass`);
}
const EA = "economic_affairs_services";
const RD_SYN = { sl: "roads_vmt_sl", fed: "roads_vmt_fed" };
const HWY = { sl: { subfunction: "sl_highways", capital: "hwy_sl" }, fed: { subfunction: "fed_highways", capital: "hwy_fed" } };
const HWY_N = { sl: P.SUBFUNCTIONS.find((s) => s.id === HWY.sl.subfunction).national_bn, fed: P.SUBFUNCTIONS.find((s) => s.id === HWY.fed.subfunction).national_bn };
const NIPA = RD_IN.nipa_2024;
const GAS = NIPA.federal_gasoline_bn + NIPA.sl_motor_fuel_bn * RD_IN.state_fuel.gasoline_share_of_state_motor_fuel_tax;
const LIC = NIPA.personal_motor_vehicle_licences_bn;
const FP = RD_IN.hcas_v21.passenger_share.all_levels;
const U5 = RD_IN.under5_share;
const RHO = RD_IN.nhts_driver_vmt_ratio_per_person_5plus[RD_RATIO];
if (Math.abs(lineOf(MODEL, "receipts", LICENCES).national_bn - LIC) > 1e-9) throw new Error("[BLOCKED] the licence national is not model.json's");
const vmtShare = (p) => { const g = p * (1 - U5.group) * RHO, o = (1 - p) * (1 - U5.others); return g / (g + o); };
// Keys of a model: the highway line's key (its preferred key, which the case evaluates), the per-head share
// (populationShare), the excise line's key (the consumption share) and the licence line's key (adults).
function roadKeysOf(m) {
  const ea = lineOf(m, "spending", EA), p = P.populationShare(m);
  const exc = refAmount(m, EXCISE), lic = refAmount(m, LICENCES);
  const nEx = lineOf(m, "receipts", EXCISE).national_bn, nLic = lineOf(m, "receipts", LICENCES).national_bn;
  return byAlloc((a) => ({ k_old: ea.keys[ea.preferred_key][a].target_bn / ea.national_bn, p: p[a], s_vmt: vmtShare(p[a]),
    k_cons: exc[a] / nEx, k_adults: lic[a] / nLic }));
}
// m: the model the edits apply to; kSet: its keys; k27: the keys before 6a (the excise and freight rules); ratio6:
// 6a's ratio on the excise line (1 without 6a); licences: false when the licence re-key is left out (licence_rule
// "index_only" with state pricing on).
function withRoads(m, kSet, k27, oo, licences) {
  const kc = byAlloc((a) => (oo.freight_key === "set" ? kSet[a].k_cons : k27[a].k_cons));
  const kRoad = byAlloc((a) => FP * kSet[a].s_vmt + (1 - FP) * kc[a]);
  const r6 = byAlloc((a) => kSet[a].k_cons / k27[a].k_cons);
  const gas = byAlloc((a) => {
    if (oo.excise_rule === "gasoline_at_miles") return GAS * (kSet[a].s_vmt - kSet[a].k_cons);
    if (oo.excise_rule === "additive") return GAS * (kSet[a].s_vmt - k27[a].k_cons);
    if (oo.excise_rule === "multiplicative") return GAS * (r6[a] * kSet[a].s_vmt - kSet[a].k_cons);
    throw new Error(`[BLOCKED] unknown excise rule ${oo.excise_rule}`);
  });
  const lines = [
    { id: RD_SYN.sl, family: "consumption", response_class: "service", label: "S&L highways re-keyed by vehicle miles and freight (roads lane; candidate)" },
    { id: RD_SYN.fed, family: "consumption", response_class: "service", label: "Federal highways re-keyed by vehicle miles and freight (roads lane; candidate)" },
  ];
  const edits = [
    { side: "spending", line: RD_SYN.sl, key: "k", by: byAlloc((a) => HWY_N.sl * (kRoad[a] - kSet[a].k_old)) },
    { side: "spending", line: RD_SYN.fed, key: "k", by: byAlloc((a) => HWY_N.fed * (kRoad[a] - kSet[a].k_old)) },
  ].concat(P.expand([{ side: "receipt", line: EXCISE, by: gas }].concat(licences
    ? [{ side: "receipt", line: LICENCES, by: byAlloc((a) => LIC * (kSet[a].s_vmt - kSet[a].k_adults)) }] : [])));
  return { m: withEdits(m, edits, lines), k_road: kRoad, k_cons_freight: kc, gasoline_shift: gas };
}

// ---------------------------------------------------------------------------------------------------
// Options.
const V4_FIELDS = ["wc", "pension4", "state_price", "roads", "licence_rule", "sales_rule", "excise_rule", "freight_key", "benefit_tax_rule",
  "accrual_receipts", "part_a_rule"];
const OPTION_VALUES = {
  wc: ["2024", "pooled_workers_compensation"],
  pension4: ["cash", "payable_net"],
  state_price: ["none", "central"],
  roads: ["resources", "miles"],
  licence_rule: ["index_on_miles", "additive", "miles_only", "index_only"],
  sales_rule: ["multiplicative", "additive"],
  excise_rule: ["gasoline_at_miles", "additive", "multiplicative"],
  freight_key: ["set", "sept27"],
  benefit_tax_rule: ["fixed", "proportional"],
  accrual_receipts: ["set", "sept27"],
  part_a_rule: ["fixed", "hi_scaled"],
};
// The composition rules chosen (RESULT.md, "Lines two items touch"); each alternative is one option away.
const RULES = { licence_rule: "index_on_miles", sales_rule: "multiplicative", excise_rule: "gasoline_at_miles", freight_key: "set",
  benefit_tax_rule: "fixed", accrual_receipts: "set", part_a_rule: "fixed" };
const OFF = Object.assign({}, V3.OFF, { wc: "2024", pension4: "cash", state_price: "none", roads: "resources" }, RULES);
// The set's items in the brief's order, each as the options that turn it on over OFF.
const SET_ITEMS = [
  { id: "1", name: "public housing's deficit at the tenant key", o: { housing: "tenants", internal_transfer: "public_housing_operating" } },
  { id: "2", name: "production on the account's weights", o: { production: "row4" } },
  { id: "3", name: "the IRS-matched income-tax key", o: { tax_key: "irs_2023_raked" } },
  { id: "4", name: "public housing's capital at the tenant key", o: { housing_capital: "tenants" } },
  { id: "5", name: "long-run property taxes", o: { property: "long_run" } },
  { id: "6a", name: "payroll compliance, the all-central items, proportional rule", o: { payroll_items: "central", payroll_rule: "proportional" } },
  { id: "7", name: "workers' compensation pooled over 2019-2024, workers' compensation line only", o: { wc: "pooled_workers_compensation" } },
  { id: "pension", name: "pension accrual at payable benefits, net of the tax on benefits (switch)", o: { pension4: "payable_net" } },
  { id: "state", name: "state pricing, the lane's central package", o: { state_price: "central" } },
  { id: "roads", name: "roads keyed by miles, fuel taxes and licences to match", o: { roads: "miles" } },
];
const BESIDE_ITEMS = [
  { id: "8", name: "public transit at the riders' key (v3 item 8)", o: { transit: "state_deficit", transit_capital: true } },
  { id: "10", name: "hospitals' uninsured use at 0.7x (v3 item 10)", o: { uninsured_use: "0.7x" } },
];
const SET = Object.assign({}, OFF, ...SET_ITEMS.map((it) => it.o));
const CASH = Object.assign({}, SET, { pension4: "cash" });
const offOf = (o) => Object.fromEntries(Object.keys(o).map((k) => [k, OFF[k]]));
const v4Part = (x) => Object.fromEntries(V4_FIELDS.map((k) => [k, x[k]]));
const v3Opts = (x) => Object.fromEntries(Object.entries(x).filter(([k]) => !V4_FIELDS.includes(k)));
function withCentral(o) {
  const x = Object.assign({}, SET, o || {});
  for (const k of V4_FIELDS) if (!OPTION_VALUES[k].includes(x[k])) throw new Error(`[BLOCKED] unknown ${k} ${JSON.stringify(x[k])}`);
  if (x.pension !== "cash") throw new Error("[BLOCKED] v3's pension switch (gross accrual, c9d0077) is superseded: use pension4");
  if (x.wc !== "2024" && x.workers_comp !== "2024") throw new Error("[BLOCKED] v3's three-line workers' compensation and item 7 on one line together");
  if (x.roads === "miles" && x.road !== "stationary_network") throw new Error(`[BLOCKED] roads by miles is built on the stationary network, not the road arm ${x.road}`);
  return Object.assign({}, V3.withCentral(v3Opts(x)), v4Part(x));
}
function specsFor(o) {
  const oo = withCentral(o);
  return V3.specsFor(v3Opts(oo)).map((s) => {
    const lines = Object.assign({}, s.line_responses);
    if (oo.roads === "miles") {
      if (!s.long_run) throw new Error("[BLOCKED] roads by miles takes the subfunctions' long-run responses");
      const sfr = P.subfunctionResponses(s.long_run, s.reading);
      lines[RD_SYN.sl] = sfr[HWY.sl.subfunction];
      lines[RD_SYN.fed] = sfr[HWY.fed.subfunction];
    }
    if (oo.state_price === "central") {
      if (s.justice !== SP_KEY.public_order_safety) throw new Error(`[BLOCKED] state pricing was built on public order and safety's ${SP_KEY.public_order_safety} key, not ${s.justice}`);
      // The engine holds public order and safety and health at 1 in every profile (the September 24 stateFor); recreation
      // takes its long-run blend. main_case.cjs gates every synthetic line's response against its parent's.
      lines[SP_SYN.public_order_safety] = 1;
      lines[SP_SYN.health_services] = 1;
      lines[SP_SYN.recreation_culture] = s.line_responses.recreation_culture;
    }
    return Object.assign({}, s, { line_responses: lines, case: CASE }, v4Part(oo));
  });
}
// The model of a fill-in method. The items apply in this order: v3's (1-6, and 8 beside), 7, roads, state pricing, the
// pension. The rules read two reference models: without 6a (k27, the September 27 excise, sales and OASDI amounts,
// which items 1-5 and 7 leave; main_case.cjs gates it) and without 3 and 6a (the September 27 income tax).
function modelFor(caseName, method, oo) {
  const v3o = v3Opts(oo);
  const m3 = V3.modelFor(caseName, method, v3o);
  const no6 = oo.payroll_items === "none" ? m3 : V3.modelFor(caseName, method, Object.assign({}, v3o, { payroll_items: "none" }));
  let m = oo.wc === "pooled_workers_compensation" ? withWorkersCompOnly(m3) : m3;
  const facts = {};
  const both = oo.roads === "miles" && oo.state_price === "central";
  if (oo.roads === "miles") {
    const r = withRoads(m, roadKeysOf(m), roadKeysOf(no6), oo, !(both && oo.licence_rule === "index_only"));
    facts.k_road = r.k_road; facts.k_cons_freight = r.k_cons_freight;
    m = r.m;
  }
  if (oo.state_price === "central") {
    const amounts = {
      [SALES_LINE]: oo.sales_rule === "multiplicative" ? refAmount(m, SALES_LINE) : refAmount(no6, SALES_LINE),
      [LICENCES]: both && oo.licence_rule === "miles_only" ? null
        : both && oo.licence_rule === "additive" ? refAmount(m3, LICENCES) : refAmount(m, LICENCES),
    };
    m = withStatePrice(m, amounts);
  }
  if (oo.pension4 === "payable_net") {
    const base = oo.tax_key === "cbo_2022" && oo.payroll_items === "none" ? m3
      : V3.modelFor(caseName, method, Object.assign({}, v3o, { payroll_items: "none", tax_key: "cbo_2022" }));
    const fit = refAmount(m, FIT_LINE), fit27 = refAmount(base, FIT_LINE);
    const hi = hiOf(m), hi27 = hiOf(no6);
    m = withPensionNet(m, {
      oasdi: oo.accrual_receipts === "set" ? oasdiOf(m) : oasdiOf(no6),
      fitScale: byAlloc((a) => (oo.benefit_tax_rule === "fixed" ? 1 : fit[a] / fit27[a])),
      partAScale: byAlloc((a) => (oo.part_a_rule === "fixed" ? 1 : hi[a] / hi27[a])),
    });
  }
  return Object.assign({}, m, { candidate: Object.assign({}, m.candidate, { v4: Object.assign(v4Part(oo), facts) }) });
}
// v3's evaluation, with hwy_sl and hwy_fed keyed at the road key when roads are keyed by miles (the lane's in-memory
// capital variant: a constant key per method and allocation). A capital variant that sets the component's key or drops
// it wins, as in v3. return = stock x rate x key x response, as the September 27 capitalReturn computes it.
function evaluateFull(m, spec, profile) {
  if (!V4_FIELDS.every((k) => k in spec)) throw new Error("[BLOCKED] a specification without v4's fields: build it with specsFor()");
  const t = m.candidate && m.candidate.v4;
  if (!t || V4_FIELDS.some((k) => t[k] !== spec[k])) throw new Error(`[BLOCKED] a specification for ${JSON.stringify(v4Part(spec))} on a model built for ${JSON.stringify(t && v4Part(t))}`);
  if ((spec.roads === "miles" || spec.state_price === "central") && profile && profile !== P.MAIN_PROFILE) {
    throw new Error(`[BLOCKED] the synthetic lines' responses are set for the main profile, not ${profile}`);
  }
  const r = V3.evaluateFull(m, spec, profile);
  let capital = r.capital;
  if (spec.roads === "miles" && capital.components.length) {
    const variant = spec.capital_variant ? P.CAP.variants[spec.capital_variant] : null;
    const ownKey = new Set(variant ? (variant.overrides || []).filter((o) => o.key || o.drop).map((o) => o.component) : []);
    const ids = [HWY.sl.capital, HWY.fed.capital];
    for (const id of ids) if (!ownKey.has(id) && !capital.components.some((c) => c.id === id)) throw new Error(`[BLOCKED] no capital component ${id} to re-key`);
    const key = t.k_road[spec.allocation];
    const components = capital.components.map((c) => (!ids.includes(c.id) || ownKey.has(c.id) ? c
      : Object.assign({}, c, { key, return_bn: c.stock_charged_bn * spec.rate * key * c.response })));
    capital = { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
  }
  return { evaluation: r.evaluation, capital, road_return_removed_bn: r.road_return_removed_bn, public_pay_bn: r.public_pay_bn,
    cost_bn: -r.evaluation.welfare_bn + capital.total_bn + r.public_pay_bn };
}
const cost = (m, spec, profile) => evaluateFull(m, spec, profile).cost_bn;
const bandFor = (m, profile, specs) => span(specs.map((spec) => cost(m, spec, profile)));
function evalPackage(caseName, method, o) {
  const oo = withCentral(o);
  return bandFor(modelFor(caseName, method, oo), oo.profile, specsFor(oo));
}
const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));

// The account's priced count (row-4 union headcount, the first candidate's production_row4.json populations.row4).
const COUNT_FILE = "main_case_candidate_2026_09_28/derived/production_row4.json";
const COUNT = readJson(COUNT_FILE).populations.row4;
if (Math.round(COUNT) !== 39712493) throw new Error(`[BLOCKED] ${COUNT_FILE}: the row-4 count is ${COUNT}, not 39,712,493`);

module.exports = Object.assign({}, V3, {
  HERE, ROOT, V3PKG: V3, CASE, LANE, REF, WC_LINE, PENSION_FILE, PENSION_COMMIT, FIT_LINE, HI_LINES, SP_DIR, SP_PACKAGE, SP_NET, SP_SPEND,
  SP_REC, SP_TARGET, SP_LINES, SP_SYN, SP_PRE, SP_RECEIPT, SP_KEY, SALES_LINE, LICENCES, EXCISE, RD_DIR, RD_IN, RD_SUM, RD_RATIO, EA, RD_SYN, HWY,
  HWY_N, GAS, LIC, FP, U5, RHO, V4_FIELDS, OPTION_VALUES, RULES, OFF, SET_ITEMS, BESIDE_ITEMS, SET, CASH, COUNT_FILE, COUNT,
  byAlloc, refAmount, withWorkersCompOnly, pensionNet, oasdiOf, hiOf, withPensionNet, parentKey, withStatePrice, vmtShare, roadKeysOf, withRoads,
  offOf, v4Part, v3Opts, withCentral, specsFor, modelFor, evaluateFull, cost, bandFor, evalPackage, central,
});
