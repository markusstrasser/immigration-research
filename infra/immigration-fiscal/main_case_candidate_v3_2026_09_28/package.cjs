/* Candidate v3, the bundled next-case revision: case sept28_candidate_v3 (BRIEF.md, 0a83245), not adopted. It builds on
 * candidate v2's package (../main_case_candidate_v2_2026_09_28/package.cjs, 08d9a86), imported unchanged, which imports
 * the first candidate and the September 27 case unchanged. Every item is an option, so each can be taken alone. With every
 * option off (OFF) the package is the September 27 case; with items 1-3 only (V2SET) it is candidate v2.
 *
 *   1-3. v2's items, unchanged: housing "tenants" with the operating subsidy consolidated, production "row4", tax_key
 *        "irs_2023_raked".
 *   4.   housing_capital "tenants": public housing's capital (ent_housing_sl) keyed like its deficit, by the rental line's
 *        evaluated key, through the capital lane's own rule (its variant public_housing_at_rental_assistance_key). A
 *        capital variant that sets that component's key itself wins.
 *   5.   property "long_run": the receipt-side lane's items (receipt_side_long_run_2026_09_28/items.cjs, 8d1840a), applied
 *        by its own itemModel() and itemOverrides(): owner-occupied property tax at the long-run owner response, the
 *        tenant-occupied tax split out of business property at the rent key and the renter response, personal property
 *        re-keyed to vehicles at 1. property_reading "low" and "high" are the lane's range ends (all_low, all_high).
 *   6a.  payroll_items "central": the payroll-compliance lane's `all` central items (payroll_compliance_2026_09_28, 89ee79d,
 *        derived/items.json), applied as its price.cjs applies them: each receipt line's group amount on the reference
 *        incidence rule moves by (ratio - 1) x that amount, expanded to every executed rule by the package's expand(), and
 *        applied with the engine's applyCorrections. payroll_rule "within_group" takes the calibrated within-group ratio
 *        (r_cal, the lane's headline); "proportional" takes the calibrated raw-share ratio (r_cal_raw, its sensitivity).
 *   6b.  row2_rule "within_group": audit row 2 carried through CBO's re-key by the within-group rule instead of in
 *        proportion to raw shares. Row 2 removed moves the group's amount by (r(without) / r(c) - 1) x the amount under each
 *        rule, c the tax block's case (r(central) = 1, row2_r_route); the swap is the difference of the two removals.
 *   7.   workers_comp "pooled_2019_2024": the workers_comp key's group amounts times the pooled 2019-2024 relative use over
 *        2024's, per allocation (backcast_pandemic_measured_2026_09_28, cbaddcf, derived/ratio_vs_2024.csv).
 *   8.   transit: NIPA 3.8 line 14 (S&L public transit) leaves the enterprise receipt and becomes its own receipt line,
 *        keyed by the enterprise line's key times the group's relative transit use (derived/transit_key.json, this lane):
 *        "state_deficit" (commuter shares weighted by each state's transit deficit), "commuters" (national commuter
 *        counts), and the deficit-weighted key with NHTS 2017's all-trip adjustments. Its capital (ent_transit_sl) takes
 *        the line's key when transit_capital is true. The rest of the enterprise line keeps every cell's fraction, so its
 *        key and every other enterprise component's key hold.
 *   9.   pension "accrual" (a switch, "cash" by default): the social_security line's group amount becomes the OASDI accrual
 *        ratio times the candidate's own group OASDI receipts (employee plus employer OASDI plus the OASDI share of
 *        self-employment tax) on the reference rule; the medicare line swaps its Part A share for the lane's Part A
 *        accrual. Both read at build time from pension_accrual_2026_09_28/derived/summary.json at PENSION_COMMIT, through
 *        git (the working tree may hold a later draft), with its hash.
 *   10.  uninsured_use "0.7x" (a switch, "equal" by default; the brief's addendum): the Medicaid line's uc key, which adds
 *        the under-charged part of the group's uncompensated care at equal hospital use (uncompensated_care_2026_09_23),
 *        takes the same key's 0.7x-use arm. The engine model carries both arms and the case's corrections move every key
 *        of the line alike, so the switch changes the specification's key, not the model.
 *
 * congestionCuts() lists every lane cut main_case.cjs prices, so road_congestion.py and main_case.cjs read one
 * definition. rangeComponents() is v2's outer-range components plus this candidate's item ranges; a component that
 * belongs to an item contributes nothing on a base without that item.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");
const V2 = require(path.join(__dirname, "..", "main_case_candidate_v2_2026_09_28", "package.cjs"));
const RS = require(path.join(__dirname, "..", "receipt_side_long_run_2026_09_28", "items.cjs"));
const P = V2.SEPT27;
const { Engine, MODEL, FISCAL, METHODS, ALLOCS, ENTERPRISE_LINE, ENTERPRISE_RECEIPT, readJson, csvRows, span, mean2 } = V2;
if (RS.K !== P) throw new Error("[BLOCKED] the receipt-side items load another copy of the September 27 package");

const HERE = __dirname;
const ROOT = path.resolve(FISCAL, "..", "..");
const CASE = "sept28_candidate_v3";
const LANE = "main_case_candidate_v3_2026_09_28";
const REF = MODEL.receipts.reference;
const lineOf = (m, side, id) => m[side].lines.find((l) => l.id === id);
const scaleCells = (cells, f) => { for (const c of cells) { c.target_bn *= f; c.other_bn *= f; } };
const receiptCells = (l) => Object.values(l.cells).flatMap((k) => ALLOCS.map((a) => k[a]));
const withMeta = (m, edits) => Engine.applyCorrections(m, { lines: [], edits, meta: m.corrections });

// ---------------------------------------------------------------------------------------------------
// Item 4: public housing's capital at the rental key, by the capital lane's own rule.
const HOUSING_CAPITAL = "ent_housing_sl";
const HOUSING_CAPITAL_VARIANT = "public_housing_at_rental_assistance_key";
const HCV = P.CAP.variants[HOUSING_CAPITAL_VARIANT];
if (!HCV || (HCV.adds || []).length || (HCV.overrides || []).length !== 1 || HCV.overrides[0].component !== HOUSING_CAPITAL
  || !HCV.overrides[0].key || Object.keys(HCV.overrides[0]).length !== 2) {
  throw new Error(`[BLOCKED] ${P.CAP_FILE}: ${HOUSING_CAPITAL_VARIANT} is not one key override of ${HOUSING_CAPITAL}`);
}
const HOUSING_CAPITAL_KEY = HCV.overrides[0].key;

// ---------------------------------------------------------------------------------------------------
// Item 5: the receipt-side lane's items, its central reading and its two range ends (probe.cjs all_low, all_high).
const PROPERTY_READINGS = {
  central: RS.CENTRAL_ITEMS,
  low: { owner: RS.RESPONSES.owner.low, tenant: Object.assign({}, RS.CENTRAL_ITEMS.tenant, { r: RS.RESPONSES.renter.low }),
    personal: RS.CENTRAL_ITEMS.personal },
  high: { owner: RS.RESPONSES.owner.high, tenant: Object.assign({}, RS.CENTRAL_ITEMS.tenant, { r: RS.RESPONSES.renter.high,
    national: RS.TENANT_NATIONAL.case_scaled }), personal: RS.CENTRAL_ITEMS.personal },
};
const PROPERTY_LINES = [RS.OWNER_LINE, RS.BUSINESS_LINE, RS.TENANT_LINE, RS.PERSONAL_LINE];

// ---------------------------------------------------------------------------------------------------
// Item 6: the payroll-compliance lane's ratios.
const PAYROLL_FILE = "payroll_compliance_2026_09_28/derived/items.json";
const PAY = readJson(PAYROLL_FILE);
if (JSON.stringify(PAY.meta.methods) !== JSON.stringify(METHODS)) throw new Error(`[BLOCKED] ${PAYROLL_FILE} was built for other fill-in methods`);
const PAYROLL_READINGS = ["central", "low_cost_central_case", "high_cost_central_case"];
const PAYROLL_FIELDS = { within_group: "r_cal", proportional: "r_cal_raw" };
const ROW2 = PAY.items.row2_r_route;
for (const r of PAYROLL_READINGS) {
  if (!PAY.items.all[r] || PAY.items.all[r].row2_case !== "central") throw new Error(`[BLOCKED] ${PAYROLL_FILE}: no all/${r} at row 2's central case`);
}
for (const c of ["without", "low", "high"]) {
  if (!ROW2[c] || ROW2[c].row2_case !== "central" || Object.keys(ROW2[c].lines).join() !== Object.keys(ROW2.without.lines).join()) {
    throw new Error(`[BLOCKED] ${PAYROLL_FILE}: row2_r_route/${c} is not on row 2's central case with the same lines`);
  }
}
const ratioOk = (x) => Number.isFinite(x) && x > 0.5 && x < 1.5;
for (const v of [...PAYROLL_READINGS.map((r) => PAY.items.all[r]), ROW2.without, ROW2.low, ROW2.high]) {
  for (const [id, byA] of Object.entries(v.lines)) {
    if (!MODEL.receipts.lines.some((l) => l.id === id)) throw new Error(`[BLOCKED] ${PAYROLL_FILE}: ${id} is not a receipt line`);
    if (!ALLOCS.every((a) => ratioOk(byA[a].r_cal) && ratioOk(byA[a].r_cal_raw))) throw new Error(`[BLOCKED] ${PAYROLL_FILE}: ${id} has an unreadable ratio`);
  }
}
const TAX_BLOCK_CASES = ["low", "central", "high"];
// The receipt shifts of item 6 on a model of the tax block's case caseName, both parts read on the same amounts.
function payrollShifts(m, caseName, oo) {
  const shifts = [];
  const amount = (id, a) => lineOf(m, "receipts", id).cells[REF][a].target_bn;
  if (oo.payroll_items !== "none") {
    const f = PAYROLL_FIELDS[oo.payroll_rule];
    for (const [id, byA] of Object.entries(PAY.items.all[oo.payroll_items].lines)) {
      shifts.push({ side: "receipt", line: id, by: Object.fromEntries(ALLOCS.map((a) => [a, (byA[a][f] - 1) * amount(id, a)])) });
    }
  }
  if (oo.row2_rule === "within_group") {
    if (!TAX_BLOCK_CASES.includes(caseName)) throw new Error(`[BLOCKED] no row 2 route for the tax block's case ${caseName}`);
    for (const [id, byA] of Object.entries(ROW2.without.lines)) {
      const q = (a, f) => byA[a][f] / (caseName === "central" ? 1 : ROW2[caseName].lines[id][a][f]);
      shifts.push({ side: "receipt", line: id, by: Object.fromEntries(ALLOCS.map((a) => [a, (q(a, "r_cal_raw") - q(a, "r_cal")) * amount(id, a)])) });
    }
  }
  return shifts;
}
const PAYROLL_LINES = [...new Set(Object.keys(PAY.items.all.central.lines).concat(Object.keys(ROW2.without.lines)))];

// ---------------------------------------------------------------------------------------------------
// Item 7: workers' compensation pooled over 2019-2024.
const WC_FILE = "backcast_pandemic_measured_2026_09_28/derived/ratio_vs_2024.csv";
const WC_KEY = "workers_comp";
const WC_ROWS = csvRows(WC_FILE).filter((r) => r.key === WC_KEY);
const WC = Object.fromEntries(ALLOCS.map((a) => {
  const rs = WC_ROWS.filter((r) => r.allocation === a);
  const one = (col) => { const xs = [...new Set(rs.map((r) => r[col]))]; if (xs.length !== 1) throw new Error(`[BLOCKED] ${WC_FILE}: ${a} ${col} differs across years`); return xs[0]; };
  if (rs.length !== 5) throw new Error(`[BLOCKED] ${WC_FILE}: ${rs.length} ${WC_KEY} rows for ${a}, not the five earlier years`);
  const pooled = Number(one("pooled_2019_2024_relative_use")), u24 = Number(one("relative_use_2024"));
  return [a, { ratio: pooled / u24, pooled, relative_use_2024: u24, lines: one("account_lines").split(";"),
    account_2024_bn: Number(one("account_2024_bn")), account_2024_change_if_pooled_bn: Number(one("account_2024_change_if_pooled_bn")) }];
}));
const WC_LINES = WC.personal.lines;
const WC_MODEL_LINES = MODEL.spending.lines.filter((l) => l.preferred_key === WC_KEY).map((l) => l.id).sort();
if (WC.shared.lines.join() !== WC_LINES.join() || WC_LINES.slice().sort().join() !== WC_MODEL_LINES.join()
  || !ALLOCS.every((a) => WC[a].ratio > 0 && WC[a].ratio < 1.5)) {
  throw new Error(`[BLOCKED] ${WC_FILE}: its ${WC_KEY} lines (${WC_LINES}) are not model.json's (${WC_MODEL_LINES}) or its ratios are unreadable`);
}
function withWorkersComp(m) {
  const shifts = WC_LINES.map((id) => { const k = lineOf(m, "spending", id).keys[WC_KEY];
    return { side: "spending", line: id, key: WC_KEY, by: Object.fromEntries(ALLOCS.map((a) => [a, (WC[a].ratio - 1) * k[a].target_bn])) }; });
  return withMeta(m, P.expand(shifts));
}

// ---------------------------------------------------------------------------------------------------
// Item 8: public transit's deficit and capital at a riders' key.
const TK_FILE = `${LANE}/derived/transit_key.json`;
if (!fs.existsSync(path.join(FISCAL, TK_FILE))) throw new Error(`[BLOCKED] ${TK_FILE} is missing: run transit_key.py first`);
const TK = readJson(TK_FILE);
if (!Array.isArray(TK.gates) || !TK.gates.length || !TK.gates.every((g) => g.pass)) throw new Error(`[BLOCKED] ${TK_FILE}: its gates did not all pass`);
const RU_DEFICIT = TK.state_weighted.ru_state_weighted.value;
const TRANSIT_RU = {
  state_deficit: RU_DEFICIT,
  commuters: TK.acs.national.ru.value,
  state_deficit_all_trips_within: RU_DEFICIT * TK.nhts_2017.adjustment_all_trips_over_commute.value,
  state_deficit_all_trips_cross: RU_DEFICIT * TK.nhts_2017.cross_survey_adjustment_all_trips_over_same_year_acs_commute.value,
};
if (!Object.values(TRANSIT_RU).every((x) => Number.isFinite(x) && x > 0.3 && x < 2)) throw new Error(`[BLOCKED] ${TK_FILE}: unreadable relative uses`);
const ESV_TRANSIT = csvRows(V2.ESV_FILE).find((r) => r.nipa_3_8_lines === "l14");
const TRANSIT_CAPITAL = "ent_transit_sl";
if (!ESV_TRANSIT || ESV_TRANSIT.nipa_3_8_group !== "public transit" || ESV_TRANSIT.components !== TRANSIT_CAPITAL) {
  throw new Error(`[BLOCKED] ${V2.ESV_FILE} has no NIPA 3.8 line 14 public transit row with its capital component`);
}
const TRANSIT_SURPLUS = Number(ESV_TRANSIT.current_surplus_2024_bn);
const tc = P.CAP.components.find((c) => c.id === TRANSIT_CAPITAL);
if (!(TRANSIT_SURPLUS < 0) || !tc || tc.key.kind !== "receipt_amount_over_national" || tc.key.line !== ENTERPRISE_LINE) {
  throw new Error(`[BLOCKED] ${P.CAP_FILE}: ${TRANSIT_CAPITAL} is not keyed by the enterprise receipt`);
}
const TRANSIT_LINE = "transit_enterprise_surplus";
const TRANSIT_RECEIPT = "receipt:" + TRANSIT_LINE;
const TRANSIT_CAPITAL_KEY = { kind: "receipt_amount_over_national", line: TRANSIT_LINE };
function splitTransit(m0, ru) {
  const m = Engine.clone(m0);
  const e = lineOf(m, "receipts", ENTERPRISE_LINE);
  if (lineOf(m, "receipts", TRANSIT_LINE)) throw new Error("[BLOCKED] the transit line is split already");
  const national = TRANSIT_SURPLUS, eNat = e.national_bn;
  if (!(Math.abs(eNat - national) > 1) || !(ru > 0)) throw new Error(`[BLOCKED] transit split of ${national} from ${eNat} at ${ru}`);
  // Public transit at the enterprise cell's own fraction times the relative use, in every incidence rule.
  const cells = Object.fromEntries(m.receipts.scenarios.map((sc) => [sc, Object.fromEntries(ALLOCS.map((a) => {
    const share = (e.cells[sc][a].target_bn / eNat) * ru;
    return [a, { direct: false, key: "transit_riders", response_class: "public_asset", share, target_bn: share * national, other_bn: (1 - share) * national }];
  }))]));
  // The enterprise line without public transit: every cell keeps its fraction.
  scaleCells(receiptCells(e), (eNat - national) / eNat);
  e.national_bn = eNat - national;
  m.receipts.lines.push({ id: TRANSIT_LINE, national_bn: national, cells });
  return m;
}

// ---------------------------------------------------------------------------------------------------
// Item 9: pension accrual, read from the pension lane's committed summary.
const PENSION_FILE = "pension_accrual_2026_09_28/derived/summary.json";
const PENSION_COMMIT = "c9d0077";
const PART_A = { hi_bn: 416.3, total_bn: 1109.8 };
const SS_LINE = "social_security", MEDICARE_LINE = "medicare";
const OASDI_LINES = ["employee_oasdi", "employer_oasdi"], SE_LINE = "self_employment_oasdi_hi";
let pensionCache = null;
function pension() {
  if (pensionCache) return pensionCache;
  if (!PENSION_COMMIT) throw new Error("[BLOCKED] no pension lane commit is pinned");
  let buf;
  try {
    buf = execFileSync("git", ["-C", ROOT, "show", `${PENSION_COMMIT}:infra/immigration-fiscal/${PENSION_FILE}`], { maxBuffer: 1 << 26, stdio: ["ignore", "pipe", "ignore"] });
  } catch (e) { throw new Error(`[BLOCKED] ${PENSION_FILE} is not in commit ${PENSION_COMMIT}`); }
  const J = JSON.parse(buf.toString("utf8"));
  const d = J.central_decomposition, at = J.case_components_attrs;
  const same = (k) => d.low[k] === d.high[k];
  if (!d || !at || !same("accrual_per_tax_dollar") || !same("part_a_accrual_bn") || J.ends.low !== 48 || J.ends.high !== 11
    || Math.abs(at.part_a_share - PART_A.hi_bn / PART_A.total_bn) > 1e-12 || !(at.se_oasdi_share > 0 && at.se_oasdi_share < 1)) {
    throw new Error(`[BLOCKED] ${PENSION_FILE} at ${PENSION_COMMIT}: not one central ratio and Part A accrual, or Part A's share is not HI 416.3 / 1,109.8`);
  }
  pensionCache = { file: PENSION_FILE, commit: PENSION_COMMIT, sha256: crypto.createHash("sha256").update(buf).digest("hex"),
    ratio: d.low.accrual_per_tax_dollar, part_a_accrual_bn: d.low.part_a_accrual_bn, part_a_share: at.part_a_share,
    se_oasdi_share: at.se_oasdi_share, central: J.central, lane_delta_bn: [d.low.delta_bn, d.high.delta_bn], decomposition: d,
    case_bn: [J.case_bn.low, J.case_bn.high], central_on_accrual_bn: [J.central_on_accrual_bn.low, J.central_on_accrual_bn.high] };
  return pensionCache;
}
// The group's OASDI receipts on the reference rule: employee and employer OASDI plus the OASDI share of self-employment tax.
function oasdiReceipts(m) {
  const pp = pension();
  const t = (id, a) => lineOf(m, "receipts", id).cells[REF][a].target_bn;
  return Object.fromEntries(ALLOCS.map((a) => [a, OASDI_LINES.reduce((s, id) => s + t(id, a), 0) + pp.se_oasdi_share * t(SE_LINE, a)]));
}
function withPension(m) {
  const pp = pension();
  const oasdi = oasdiReceipts(m);
  const ss = lineOf(m, "spending", SS_LINE), med = lineOf(m, "spending", MEDICARE_LINE);
  const ks = ss.keys[ss.preferred_key], km = med.keys[med.preferred_key];
  return withMeta(m, [
    { side: "spending", line: SS_LINE, key: ss.preferred_key, by: Object.fromEntries(ALLOCS.map((a) => [a, pp.ratio * oasdi[a] - ks[a].target_bn])) },
    { side: "spending", line: MEDICARE_LINE, key: med.preferred_key, by: Object.fromEntries(ALLOCS.map((a) => [a, pp.part_a_accrual_bn - pp.part_a_share * km[a].target_bn])) },
  ]);
}

// ---------------------------------------------------------------------------------------------------
// Item 10: hospitals' uninsured use at 0.7 times the average, the uc key's own 0.7x arm.
const MEDICAID_LINE = "medicaid_and_chip_other_medical";
const UC_FILE = "uncompensated_care_2026_09_23/derived/summary.json";
const UC = readJson(UC_FILE);
const UC_07 = { uninsured_use_low: "uninsured_use_07_low", uninsured_use_high: "uninsured_use_07_high" };
const UC_KEYS = lineOf(MODEL, "spending", MEDICAID_LINE).keys;
if (!UC_KEYS.medicaid || !Object.entries(UC_07).every(([a, b]) => UC_KEYS[a] && UC_KEYS[b])
  || !["inside_undercharged_bn_use_1.0", "inside_undercharged_bn_use_0.7"].every((k) => Array.isArray(UC[k]) && UC[k].length === 2)) {
  throw new Error(`[BLOCKED] ${MEDICAID_LINE} lacks the uninsured-use keys, or ${UC_FILE} their under-charged amounts`);
}

// ---------------------------------------------------------------------------------------------------
// Options.
const V3_FIELDS = ["housing_capital", "property", "property_reading", "payroll_items", "payroll_rule", "row2_rule", "workers_comp", "transit",
  "transit_capital", "pension", "uninsured_use"];
const OPTION_VALUES = {
  housing_capital: ["enterprise", "tenants"],
  property: ["none", "long_run"],
  property_reading: Object.keys(PROPERTY_READINGS),
  payroll_items: ["none", ...PAYROLL_READINGS],
  payroll_rule: Object.keys(PAYROLL_FIELDS),
  row2_rule: ["proportional", "within_group"],
  workers_comp: ["2024", "pooled_2019_2024"],
  transit: ["population", ...Object.keys(TRANSIT_RU)],
  transit_capital: [true, false],
  pension: ["cash", "accrual"],
  uninsured_use: ["equal", "0.7x"],
};
const V3_ON = { housing_capital: "tenants", property: "long_run", property_reading: "central", payroll_items: "central", payroll_rule: "within_group",
  row2_rule: "within_group", workers_comp: "pooled_2019_2024", transit: "state_deficit", transit_capital: true, pension: "cash", uninsured_use: "equal" };
const V3_OFF = { housing_capital: "enterprise", property: "none", property_reading: "central", payroll_items: "none", payroll_rule: "within_group",
  row2_rule: "proportional", workers_comp: "2024", transit: "population", transit_capital: true, pension: "cash", uninsured_use: "equal" };
const CANDIDATE = Object.assign({}, V2.CANDIDATE, V3_ON);
const ACCRUAL = Object.assign({}, CANDIDATE, { pension: "accrual" });
const USE07 = Object.assign({}, CANDIDATE, { uninsured_use: "0.7x" });
const OFF = Object.assign({}, V2.OFF, V3_OFF);
const V2SET = Object.assign({}, V2.CANDIDATE, V3_OFF);
// The items in the brief's order, each as the options that turn it on over OFF.
const ITEMS = [
  { id: "1", name: "public housing's deficit at the tenant key", o: { housing: "tenants", internal_transfer: "public_housing_operating" } },
  { id: "2", name: "production on the account's weights", o: { production: "row4" } },
  { id: "3", name: "the IRS-matched income-tax key", o: { tax_key: "irs_2023_raked" } },
  { id: "4", name: "public housing's capital at the tenant key", o: { housing_capital: "tenants" } },
  { id: "5", name: "long-run property taxes", o: { property: "long_run" } },
  { id: "6a", name: "payroll compliance: the all-central items, calibrated within-group rule", o: { payroll_items: "central" } },
  { id: "6b", name: "payroll compliance: row 2 through CBO's re-key by the within-group rule", o: { row2_rule: "within_group" } },
  { id: "7", name: "workers' compensation pooled over 2019-2024", o: { workers_comp: "pooled_2019_2024" } },
  { id: "8", name: "public transit at the riders' key (state-deficit weighted), deficit and capital", o: { transit: "state_deficit" } },
  { id: "9", name: "pension accrual (switch)", o: { pension: "accrual" } },
  { id: "10", name: "hospitals' uninsured use at 0.7x the average (switch)", o: { uninsured_use: "0.7x" } },
];
// Items off by default, taken beside the candidate: they are not in the candidate's option set.
const SWITCHES = ["9", "10"];
const v2Part = (x) => Object.fromEntries(Object.entries(x).filter(([k]) => !V3_FIELDS.includes(k)));
const v3Part = (x) => Object.fromEntries(V3_FIELDS.map((k) => [k, x[k]]));
function withCentral(o) {
  const x = Object.assign({}, CANDIDATE, o || {});
  for (const k of V3_FIELDS) if (!OPTION_VALUES[k].includes(x[k])) throw new Error(`[BLOCKED] unknown ${k} ${JSON.stringify(x[k])}`);
  return Object.assign({}, V2.withCentral(v2Part(x)), v3Part(x));
}
function specsFor(o) {
  const oo = withCentral(o);
  const over = oo.property === "long_run" ? RS.itemOverrides(PROPERTY_READINGS[oo.property_reading]) : {};
  return V2.specsFor(v2Part(oo)).map((s) => {
    const lines = Object.assign({}, s.line_responses, over);
    if (oo.transit !== "population") lines[TRANSIT_RECEIPT] = s.line_responses[ENTERPRISE_RECEIPT];
    const uc = oo.uninsured_use === "0.7x" ? UC_07[s.uc] : s.uc;
    if (!uc) throw new Error(`[BLOCKED] no 0.7x-use arm of the uc key ${s.uc}`);
    return Object.assign({}, s, { line_responses: lines, case: CASE, uc }, v3Part(oo));
  });
}
function modelFor(caseName, method, oo) {
  let m = V2.modelFor(caseName, method, v2Part(oo));
  if (oo.property === "long_run") m = RS.itemModel(m, PROPERTY_READINGS[oo.property_reading]);
  const shifts = payrollShifts(m, caseName, oo);
  if (shifts.length) m = withMeta(m, P.expand(shifts));
  if (oo.workers_comp === "pooled_2019_2024") m = withWorkersComp(m);
  if (oo.transit !== "population") m = splitTransit(m, TRANSIT_RU[oo.transit]);
  if (oo.pension === "accrual") m = withPension(m);
  return Object.assign({}, m, { candidate: Object.assign({}, m.candidate, { v3: v3Part(oo) }) });
}
// Items 4 and 8 re-key capital components on the evaluation; a capital variant that sets the component's key (or drops
// it) wins. return = stock x rate x key x response, as the September 27 capitalReturn computes it.
function rekeyCapital(r, spec) {
  const rules = {};
  if (spec.housing_capital === "tenants") rules[HOUSING_CAPITAL] = HOUSING_CAPITAL_KEY;
  if (spec.transit !== "population" && spec.transit_capital) rules[TRANSIT_CAPITAL] = TRANSIT_CAPITAL_KEY;
  if (!Object.keys(rules).length || !r.capital.components.length) return r.capital;
  const variant = spec.capital_variant ? P.CAP.variants[spec.capital_variant] : null;
  const ownKey = new Set(variant ? (variant.overrides || []).filter((o) => o.key || o.drop).map((o) => o.component) : []);
  for (const id of Object.keys(rules)) {
    if (!ownKey.has(id) && !r.capital.components.some((c) => c.id === id)) throw new Error(`[BLOCKED] no capital component ${id} to re-key`);
  }
  const components = r.capital.components.map((c) => {
    if (!rules[c.id] || ownKey.has(c.id)) return c;
    const key = P.keyOf(r.evaluation, rules[c.id]);
    return Object.assign({}, c, { key, return_bn: c.stock_charged_bn * spec.rate * key * c.response });
  });
  return { components, total_bn: components.reduce((a, c) => a + c.return_bn, 0) };
}
function evaluateFull(m, spec, profile) {
  if (!V3_FIELDS.every((k) => k in spec)) throw new Error("[BLOCKED] a specification without v3's fields: build it with specsFor()");
  const t = m.candidate && m.candidate.v3;
  if (!t || V3_FIELDS.some((k) => t[k] !== spec[k])) throw new Error(`[BLOCKED] a specification for ${JSON.stringify(v3Part(spec))} on a model built for ${JSON.stringify(t)}`);
  const r = V2.evaluateFull(m, spec, profile);
  const capital = rekeyCapital(r, spec);
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
const MAIN_SPECS = specsFor({});

// ---------------------------------------------------------------------------------------------------
// The range: v2's components plus the items' own ranges. A variant's options may depend on the base, so an item's
// component moves nothing on a base without the item.
const onlyIf = (field, off, o) => (base) => (base[field] === off ? {} : o);
function rangeComponents() {
  const v = (label, o) => ({ v: label, o, caseName: "central", methods: METHODS });
  return V2.rangeComponents().concat([
    { name: "property_long_run", label: "long-run property taxes: the receipt-side lane's low responses, and 1 everywhere with the case-scaled tenant national",
      variants: [v("low responses", onlyIf("property", "none", { property_reading: "low" })),
        v("1 everywhere, case-scaled tenant national", onlyIf("property", "none", { property_reading: "high" }))] },
    { name: "payroll_compliance", label: "payroll compliance: the lane's low-cost and high-cost readings at row 2's central shares",
      variants: [v("low-cost readings", onlyIf("payroll_items", "none", { payroll_items: "low_cost_central_case" })),
        v("high-cost readings", onlyIf("payroll_items", "none", { payroll_items: "high_cost_central_case" }))] },
    { name: "transit_key", label: "transit riders' key: national commuter counts; the deficit-weighted key with NHTS 2017's all-trip adjustments",
      variants: ["commuters", "state_deficit_all_trips_within", "state_deficit_all_trips_cross"].map((t) => v(t, onlyIf("transit", "population", { transit: t }))) },
  ]);
}
function variantRuns(base, variant) {
  const o = typeof variant.o === "function" ? variant.o(base) : variant.o;
  const oo = withCentral(Object.assign({}, base, o));
  const specs = specsFor(oo);
  return { specs, runs: variant.methods.map((meth) => { const m = modelFor(variant.caseName, meth, oo); return specs.map((s) => evaluateFull(m, s, oo.profile)); }) };
}
// Every lane cut main_case.cjs prices: the road arm at the fixed end specifications on the candidate, v2 and the
// September 27 case (with factorial ranges), and every range variant's band ends on each base (central only).
function congestionCuts(bases) {
  const cuts = new Map();
  const add = (c, factorial) => cuts.set(c, (cuts.get(c) || false) || factorial);
  for (const base of [CANDIDATE, V2SET, OFF]) for (const a of V2.ROAD_ARM) {
    const { specs, runs } = variantRuns(base, { o: { road: a.road, long_run: a.long_run }, caseName: "central", methods: METHODS });
    V2.endCuts(specs, runs, V2.fixedEnds(runs)).forEach((c) => add(c, true));
  }
  for (const base of bases || rangeBases()) for (const comp of rangeComponents()) for (const variant of [{ o: {}, caseName: "central", methods: METHODS }, ...comp.variants]) {
    const { specs, runs } = variantRuns(base, variant);
    V2.endCuts(specs, runs, V2.endsOf(specs, runs)).forEach((c) => add(c, false));
  }
  return [...cuts].map(([cut, factorial]) => ({ cut, factorial })).sort((a, b) => a.cut - b.cut);
}
// The bases the range is computed on: the candidate with each switch off and on, v2 and the September 27 case.
const rangeBases = () => [CANDIDATE, ACCRUAL, V2SET, OFF, USE07];
const sha256 = P.sha256;

module.exports = Object.assign({}, V2, {
  HERE, ROOT, V2PKG: V2, RS, CASE, LANE, REF, HOUSING_CAPITAL, HOUSING_CAPITAL_VARIANT, HOUSING_CAPITAL_KEY, PROPERTY_READINGS, PROPERTY_LINES,
  PAYROLL_FILE, PAY, PAYROLL_READINGS, PAYROLL_FIELDS, ROW2, PAYROLL_LINES, WC_FILE, WC_KEY, WC, WC_LINES, TK_FILE, TK, TRANSIT_RU,
  ESV_TRANSIT, TRANSIT_SURPLUS, TRANSIT_CAPITAL, TRANSIT_LINE, TRANSIT_RECEIPT, TRANSIT_CAPITAL_KEY, PENSION_FILE, PENSION_COMMIT,
  PART_A, SS_LINE, MEDICARE_LINE, OASDI_LINES, SE_LINE, MEDICAID_LINE, UC_FILE, UC, UC_07, V3_FIELDS, OPTION_VALUES, V3_ON, V3_OFF,
  CANDIDATE, ACCRUAL, USE07, OFF, V2SET, ITEMS, SWITCHES, MAIN_SPECS, lineOf, payrollShifts, withWorkersComp, splitTransit, pension, oasdiReceipts, withPension, v2Part, v3Part, withCentral,
  specsFor, modelFor, rekeyCapital, evaluateFull, cost, bandFor, evalPackage, central, rangeComponents, variantRuns, congestionCuts,
  rangeBases, sha256,
});
