/* Why the group costs what it costs: the September 27 main case ($321.8194–387.3701bn) in four additive parts at
 * its two end specifications (48, the low end; 11, the high end):
 *
 *   1. shared            the account's own headcount at national per-capita taxes and service use;
 *   2. age structure     from national ages to the group's, holding national per-age taxes and use;
 *   3. taxes at given ages          the group's receipts profile against the national one;
 *   4. service use at given ages    the group's spending profile against the national one.
 *
 * Parts 2-4 are an exact Shapley split over three factors, each either national (N) or the group's (G):
 * A the age distribution, R the receipts profile by age, U the service-use profile by age. Every one of the
 * eight states is a copy of the case's corrected union model (corrections.json applied to model.json) with the
 * group's amounts replaced line by line, evaluated through the package's evaluateFull() (the engine at the
 * specification's responses plus the return on public capital, whose components key off the state's own line
 * amounts). State NNN is part 1; state GGG is the case itself.
 *
 * Amounts. For a line whose key has a per-person vector (profiles.py), on the row-4 frame the case's stack uses:
 *   T_GG = union total; T_GN = sum_b n_G(b) x national key per person in b; T_NG = sum_b N_G pi_nat(b) x union key
 *   per person in b; T_NN = N_G x national key per person. The uncorrected amount at a state is the model's
 *   uncorrected cell times the state's key share over the published share. The case's corrections (every lane in
 *   corrections.json, 278 edits) are the group's own measurements, so they enter only where the line's profile is
 *   the group's: amount(alpha, G) = kappa x uncorrected(alpha, G), kappa = corrected / uncorrected(G, G) (the
 *   correction scales with the group's own per-age profile); amount(alpha, N) = uncorrected(alpha, N).
 * Lines held instead (no age or profile effect by construction): per-head keys (population, resident_population:
 * general government, defense, interest, recreation, housing and community, the enterprise surplus by its re-key)
 * at the case's corrected amount in every state; external and zero-response lines at the case's amounts (they
 * carry no cost at the specification's responses). Special keys:
 *   public_order_safety/use   per-head parts per head; the arrest-, court- and custody-keyed parts follow the
 *                             national arrest profile by age (FBI CIUS 2024 Table 38) with a group relative risk
 *                             calibrated to the case's administrative amount (indirect standardization);
 *   Medicaid/uninsured_use_*  the MEPS Medicaid key plus the uncompensated-care arm g x (s - k) x n at the arm that
 *                             sets the key (keys.py), recomputed from the state's own key totals;
 *   school_reprice            the group's school correction, scaled with its school-key profile, 0 at U = N;
 *   college_rekey             the group's education re-key, scaled with its education-mix profile, 0 at U = N;
 *   lane_constants            audit row 8 (unallocable state-local spending, a per-head item) in every state; the
 *                             rest (care work, shelter, rows 9-10, small items) the group's own, 0 at U = N;
 *   production (P + F)        goes with the receipts factor: 0 at R = N (a slice with national per-age earnings is
 *                             a proportional slice of labor, which moves no factor price under the model's constant
 *                             returns with capital adjusting), and scaled by the group's earnings (wage key) at A = N.
 *
 * Gates (exit 1): corrections.json is the package's payload; (b) the union reproduces the case at both ends
 * (1e-9) and the ends are specifications 48 and 11; the published-frame key shares reproduce model.json's
 * uncorrected cells for every standardized line (to the nine decimals model.json stores), including the justice and uninsured keys;
 * state GGG equals the union line by line and in cost; per-head lines' kappa is 1 within 1e-4; per-line
 * contributions add to each state's cost (1e-9); (a) parts 1-4 add to the case at both ends in every order
 * (1e-9; brief tolerance $0.1bn); (c) twice the average residents cost twice part 1 (1e-9).
 * Outputs: derived/decomposition.csv, decomposition_lines.csv, states.csv, summary.json. Run from the repository
 * root: node infra/immigration-fiscal/main_case_decomposition_2026_09_29/decompose.cjs [--out-dir DIR] [--case KEY]
 *
 * Cases (--case). sept27, the default: the September 27 case above, whose outputs keep their names. sept29: the main
 * case adopted on 2026-09-29 (v4, main_case_2026_09_29, its corrections.json through its package); sept29_cash: its
 * cash set (candidate v4's corrections_v4_cash.json through the same package's forPayload). Their outputs carry the key
 * (decomposition_sept29.csv, ...), and they read profiles_sept29.py's keys beside profiles.py's. v4's parts take these
 * rules (RESULT.md, "v4 case (sept29)"); a September 27 payload has none of them:
 *   pension accrual       social_security is the payload's ratio_net x the OASDI receipts at the state's ages and
 *                         receipts profile (the payload's own rule, read at every state): it moves with A and R, never
 *                         with U. medicare keeps its Parts B and D share on the medicare key (U) and carries the Part A
 *                         accrual scaled by covered workers (positive_fica_worker; A and R). federal_income_tax keeps
 *                         its key (R) less the tax on current Social Security benefits, on the benefit key at the
 *                         receipts profile: the payload's dollars at R = G, the national rate (the pension lane's
 *                         current_rate_nation) on the national line at R = N;
 *   property taxes        item 5's responsive receipts on their own keys: owner-occupied on the account's CPS key,
 *                         tenant-occupied on ACS contract rent, personal on ACS household vehicles (profiles_sept29.py);
 *   housing_enterprise_surplus  public housing's deficit follows housing_subsidies, the rental line that keys it (U);
 *   state_price_*         the parent line's amount at the group's profile times the line's ratio to it; 0 at U = N;
 *   roads_vmt_*           the group's persons aged 5 and over across ages (the roads lane's miles are per person 5+),
 *                         0 at U = N;
 *   national-scale edits  a scaled line's uncorrected amount is model.json's cell times the payload's scale.
 * oct05: the main case adopted on 2026-10-05 (v5, main_case_2026_10_05, its corrections.json through its package);
 * oct05_cash: its cash set (corrections_cash.json through the package's CASH). v5 is v4 plus the 3.04M people the lineage
 * adds (meta.lineage.counts.added), whose amounts are its edits (meta.lineage.edits). v4's rules apply, and these
 * (RESULT.md, "v5 case (oct05)"):
 *   the added people  placed at the identified G3+'s ages (profiles_oct05.py), each at the union's per-person key in
 *                     its age bin: every row-4 union key vector is scaled by (union + added) / union in each bin. The
 *                     lineage's measured amounts enter through kappa, as the corrections do. The published frame stays
 *                     model.json's (its key shares are gated);
 *   justice           the added people's keyed parts at the union's relative risk theta;
 *   pension accrual   social_security at one ratio for the whole group, the case's amount over its OASDI receipts; the
 *                     lineage's Part A accrual is its set amount less (1 - part_a_share) x its cash amount, and its tax
 *                     on current benefits its cash income tax less its set income tax (the two payloads' lineage edits
 *                     differ on these three lines only, gated);
 *   finite removal    the linearity note doubles v5's group share (meta.lineage.s.v5).
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const argv = process.argv.slice(2);
const argOf = (name, dflt) => { const i = argv.indexOf(name); return i < 0 ? dflt : argv[i + 1]; };
const CASES = {
  sept27: { lane: "main_case_long_run_2026_09_27", suffix: "" },
  sept29: { lane: "main_case_2026_09_29", suffix: "_sept29" },
  sept29_cash: { lane: "main_case_2026_09_29", suffix: "_sept29_cash", payload: "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json" },
  oct05: { lane: "main_case_2026_10_05", suffix: "_oct05", lineage: true },
  oct05_cash: { lane: "main_case_2026_10_05", suffix: "_oct05_cash", lineage: true, cash: "main_case_2026_10_05/derived/corrections_cash.json" },
};
const CASE_KEY = argOf("--case", "sept27");
const CASE_DEF = CASES[CASE_KEY];
if (!CASE_DEF) throw new Error(`[BLOCKED] unknown case ${CASE_KEY}: ${Object.keys(CASES).join(", ")}`);
const P0 = require(path.join(FISCAL, CASE_DEF.lane, "package.cjs"));
const P = CASE_DEF.payload ? P0.forPayload(P0.readJson(CASE_DEF.payload)) : CASE_DEF.cash ? P0.CASH : P0;
const { Engine, MODEL, readJson } = P;
const IN = path.join(HERE, "derived");
const OUT = path.resolve(argOf("--out-dir", IN));
const SUFFIX = CASE_DEF.suffix;

const fails = [];
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) fails.push(label);
}
const sum = (xs) => xs.reduce((a, b) => a + b, 0);
const rel = (a, b) => Math.abs(a - b) / Math.max(Math.abs(b), 1e-12);
const MEMBERS = MODEL.meta.target_population;  // the case's per-member denominator, 40,896,574
const REF = MODEL.receipts.reference;

// ---------------------------------------------------------------------------------------------------
// The case.
const CORR_FILE = CASE_DEF.payload || CASE_DEF.cash || `${CASE_DEF.lane}/derived/corrections.json`;
const CORR = readJson(CORR_FILE);
const CASE_SUMMARY = readJson(`${CASE_DEF.lane}/derived/summary.json`);
const CASE = CASE_KEY.endsWith("_cash") ? CASE_SUMMARY.cash_set.band_bn : CASE_SUMMARY.main_case;
console.log(CASE_KEY === "sept27" ? "[case]" : `[case ${CASE_KEY}]`);
gate(CASE_KEY === "sept27" ? "corrections.json is main_case_long_run_2026_09_27's payload" : `${CORR_FILE} is the package's payload`,
  JSON.stringify(P.correctionsPayload()) === JSON.stringify(CORR), `${CORR.lines.length} lines, ${CORR.edits.length} edits`);
const UNION = Engine.applyCorrections(MODEL, CORR);
const SPECS = P.MAIN_SPECS;
const unionCost = SPECS.map((s) => P.evaluateFull(UNION, s).cost_bn);
const LO = unionCost.indexOf(Math.min(...unionCost)), HI = unionCost.indexOf(Math.max(...unionCost));
gate("(b) the corrected union reproduces the case at both ends", rel(unionCost[LO], CASE[0]) < 1e-12 && rel(unionCost[HI], CASE[1]) < 1e-12,
  `${unionCost[LO].toFixed(4)} / ${unionCost[HI].toFixed(4)} vs ${CASE[0].toFixed(4)} / ${CASE[1].toFixed(4)}`);
gate("the ends are specifications 48 (low) and 11 (high)", LO === 48 && HI === 11, `${LO} / ${HI}`);
const ENDS = [["low", LO], ["high", HI]];

// ---------------------------------------------------------------------------------------------------
// Age profiles (profiles.py).
function readCsv(file) {
  const [head, ...rows] = fs.readFileSync(file, "utf8").trim().split("\n");
  const keys = head.split(",");
  return rows.map((r) => { const c = r.split(","); return Object.fromEntries(keys.map((k, i) => [k, c[i]])); });
}
const BINS = {};
for (const file of ["age_bins.csv"].concat(SUFFIX ? ["age_bins_sept29.csv"] : [])) {
  for (const r of readCsv(path.join(IN, file))) {
    const t = ((BINS[r.weights] ||= {})[r.allocation] ||= {})[r.key] ||= { union: [], national: [], bins: [] };
    t.union.push(Number(r.union)); t.national.push(Number(r.national)); t.bins.push(Number(r.bin));
  }
}
const EDGES = BINS.published.both["extra|pop"].bins;
for (const [w, byA] of Object.entries(BINS)) for (const [a, byK] of Object.entries(byA)) for (const [k, t] of Object.entries(byK)) {
  if (t.bins.length !== EDGES.length) throw new Error(`[BLOCKED] ${w}/${a}/${k}: ${t.bins.length} bins, not ${EDGES.length} (a key in both profile files?)`);
}
// v5: the lineage's added people at the identified G3+'s ages (profiles_oct05.py), each at the union's per-person key in
// its age bin. Only the row-4 frame, the one the case's stack uses, takes them; the published frame stays model.json's.
const LINEAGE = CASE_DEF.lineage ? (() => {
  const L = CORR.meta.lineage, rows = readCsv(path.join(IN, "g3plus_ages_oct05.csv"));
  if (rows.map((r) => Number(r.bin)).join() !== EDGES.join()) throw new Error("[BLOCKED] g3plus_ages_oct05.csv is not in the age bins");
  const g3 = rows.map((r) => Number(r.g3plus)), G3 = sum(g3), M = L.counts.added;
  const pop4 = BINS.row4.both["extra|pop"].union.slice();
  const added = g3.map((x) => M * x / G3);
  const scale = pop4.map((p, b) => (p + added[b]) / p);
  for (const byK of Object.values(BINS.row4)) for (const t of Object.values(byK)) t.union = t.union.map((x, b) => x * scale[b]);
  return { L, M, G3, pop4, added, scale };
})() : null;
const POP = { published: BINS.published.both["extra|pop"], row4: BINS.row4.both["extra|pop"] };
const ARREST = readCsv(path.join(IN, "arrest_profile.csv")).map((r) => Number(r.share));
const FRAME = Object.fromEntries(Object.entries(POP).map(([w, p]) => [w, { NG: sum(p.union), NC: sum(p.national) }]));
const HF = FRAME.published.NC / MODEL.meta.resident_population;  // the account's household fraction on spending
if (LINEAGE) {
  const c = LINEAGE.L.counts;
  gate("v5: the ages' G3+ is the payload's identified_g3plus (1e-6 persons)", Math.abs(LINEAGE.G3 - c.identified_g3plus) < 1e-6,
    `${LINEAGE.G3.toFixed(6)} vs ${c.identified_g3plus}`);
  gate("v5: the row-4 frame held the account's union, and now holds the lineage (1e-3 persons)",
    Math.abs(sum(LINEAGE.pop4) - c.account_union) < 1e-3 && Math.abs(FRAME.row4.NG - c.lineage_population) < 1e-3,
    `${sum(LINEAGE.pop4).toFixed(4)} + ${LINEAGE.M.toFixed(4)} = ${FRAME.row4.NG.toFixed(4)} vs ${c.lineage_population}`);
}

// Key totals at the four (age, profile) states on a frame.
function stateTotals(u, n, pop) {
  const NG = sum(pop.union), NC = sum(pop.national), V = sum(n);
  return {
    V, T: {
      GG: sum(u),
      GN: sum(n.map((x, b) => pop.union[b] * x / pop.national[b])),
      NG: sum(u.map((x, b) => NG * pop.national[b] / NC * x / pop.union[b])),
      NN: NG * V / NC,
    },
  };
}
function keyTotals(weights, allocation, name) {
  const k = (BINS[weights][allocation] || {})[name];
  if (!k) return null;
  return stateTotals(k.union, k.national, POP[weights]);
}

// ---------------------------------------------------------------------------------------------------
// Justice: the use key (cj_use_allocation_2026_09_23, its central split).
const CJ = readJson("cj_use_allocation_2026_09_23/derived/summary.json").central;
const CJROWS = Object.fromEntries(readCsv(path.join(FISCAL, "cj_use_allocation_2026_09_23/derived/central_split.csv"))
  .map((r) => [r.component, Number(r.national_bn)]));
if (!(CJ.police_key === "half" && CJ.court_criminal_share === 0.6 && CJ.cbp_border === "per_head")) {
  throw new Error("[BLOCKED] the justice lane's central split changed: police half, courts 60% criminal, CBP per head expected");
}
const PH = CJROWS.fire + CJROWS.police_cbp + CJROWS.police_ice_border + 0.5 * CJROWS.police_non_border + 0.4 * CJROWS.law_courts;
const NP = 0.5 * CJROWS.police_non_border + 0.6 * CJROWS.law_courts + CJROWS.prisons + CJROWS.police_ice_interior;
const POS = MODEL.spending.lines.find((l) => l.id === "public_order_safety");
gate("the justice components add to the public-order line", Math.abs(PH + NP - POS.national_bn) < 1e-5,
  `per head ${PH.toFixed(3)} + keyed ${NP.toFixed(3)} = ${(PH + NP).toFixed(3)} vs ${POS.national_bn}`);
const JUSTICE_PROFILES = {
  arrests: ARREST,  // national arrests by age, all offenses (CIUS 2024 Table 38)
  flat_18_64: (() => {  // the key's own base for the custody split: persons 18-64, flat
    const p = POP.published.national.map((x, b) => (EDGES[b] >= 18 && EDGES[b] <= 64 ? x : 0));
    return p.map((x) => x / sum(p));
  })(),
};
// Key-unit totals (share = T / national) of the use key at the four states on a frame. The keyed parts are the
// group's administrative amount at G (held fixed across weight sets, as the stack holds them) and the national
// profile times a relative risk theta at the group's profile.
function justiceTotals(weights, profile, groupKeyed) {
  const pop = POP[weights], NG = sum(pop.union), NC = sum(pop.national);
  const perPerson = profile.map((a, b) => NP * a / pop.national[b]);
  const atGroupAges = sum(perPerson.map((j, b) => j * pop.union[b]));
  const theta = groupKeyed / atGroupAges;
  const ph = PH * NG / NC;
  return { V: POS.national_bn, theta, T: { GG: ph + groupKeyed, GN: ph + atGroupAges, NG: ph + theta * NP * NG / NC, NN: (PH + NP) * NG / NC } };
}
// v5: the added people's keyed parts at the union's relative risk (theta held on the row-4 frame).
function lineageKeyed(weights, profile, groupKeyed) {
  if (!LINEAGE || weights !== "row4") return groupKeyed;
  const pop = POP.row4, perPerson = profile.map((x, b) => NP * x / pop.national[b]);
  return groupKeyed * sum(perPerson.map((j, b) => j * pop.union[b])) / sum(perPerson.map((j, b) => j * LINEAGE.pop4[b]));
}

// ---------------------------------------------------------------------------------------------------
// Uncompensated care inside the Medicaid line (uncompensated_care_2026_09_23; keys.py's arms).
const UC = readJson("uncompensated_care_2026_09_23/derived/summary.json");
const OFFSETS = [
  { year: 2013, total_uc: 84.9 - 8.1 - 2.1, programs: { medicaid: 13.5, medicare: 8.0, state_local: 9.8 + 7.3 + 3.0 + 1.5 + 0.1 } },
  { year: 2017, total_uc: 42.4 - 10.3 - 2.3, programs: { medicaid: 9.8, state_local: 9.9 + 1.3 } },
];
const ARMS = OFFSETS.flatMap((o) => ["health_other", "per_head"].flatMap((sl) =>
  [UC.aha_national_bn, UC.aha_national_bn * UC.uplift_2024].map((n) => ({ year: o.year, sl, n, o }))));
const MEDICAID = "medicaid_and_chip_other_medical";
const lineOf = (id) => MODEL.spending.lines.find((l) => l.id === id);
// Arm value g x (s - k) x n from a state's uninsured person-years share and its program key shares.
function armValue(arm, s, kg) {
  const off = sum(Object.values(arm.o.programs));
  const g = off / arm.o.total_uc;
  const k = sum(Object.entries(arm.o.programs).map(([p, v]) => v / off * kg[p === "state_local" ? arm.sl : p]));
  return g * (s - k) * arm.n;
}

// ---------------------------------------------------------------------------------------------------
// The plan: every line's amount at each (age, profile) state for one specification.
const SYN_IDS = new Set(P.SYN_LINES.map((l) => l.id));
const ROW8 = P.CONSTANTS.row8.c * P.RESPONSES.row8_factor;
const unionLine = (side, id) => (side === "receipt" ? UNION.receipts.lines : UNION.spending.lines).find((l) => l.id === id);
// A national-scale edit's factor on a line's uncorrected cell: 1 on every line the payload does not scale (every line of
// a September 27 payload).
const natScale = (side, id) => unionLine(side, id).national_bn / (side === "receipt" ? MODEL.receipts.lines : MODEL.spending.lines)
  .find((l) => l.id === id).national_bn;
const uncorrectedCell = (side, id, key, a) => {
  const cell = side === "receipt" ? MODEL.receipts.lines.find((l) => l.id === id).cells[REF][a] : lineOf(id).keys[key][a];
  const f = natScale(side, id);
  return f === 1 ? cell : Object.assign({}, cell, { target_bn: cell.target_bn * f });
};

// v4's parts (see the header). A September 27 payload has no receipt lines, correction lines beyond the three, national
// scales or accrual, so none of this moves its plan.
const IS_V4 = Array.isArray(CORR.receipt_lines);
const ACCRUAL = CORR.meta.pension_accrual || null;
const STATE_PRICE_PARENT = Object.fromEntries(((CORR.meta.state_pricing || {}).lines || []).map((x) => [x.line, x.parent]));
const ROAD_LINES = new Set(P.componentsFor(null).filter((c) => c.key.kind === "part_rekeyed").map((c) => c.key.correction_line));
const HOUSING_ENTERPRISE = "housing_enterprise_surplus", RENTAL_LINE = "housing_subsidies";
const V4_KEYS = { tenant_occupied_property: "receipt|renter_contract_rent", personal_property_tax: "receipt|household_vehicles" };
const PENSION_FILE = "pension_accrual_2026_09_28/derived/summary.json";
const PENSION = ACCRUAL ? readJson(PENSION_FILE) : null;
let RATIO_NATIONAL = null;
if (IS_V4) {
  gate("v4's correction lines are the state-price and road lines", CORR.lines.filter((l) => !SYN_IDS.has(l.id))
    .every((l) => STATE_PRICE_PARENT[l.id] || ROAD_LINES.has(l.id)), CORR.lines.map((l) => l.id).join(", "));
  gate("v4's receipt lines are public housing's deficit and tenant-occupied property",
    CORR.receipt_lines.map((l) => l.id).sort().join() === [HOUSING_ENTERPRISE, "tenant_occupied_property"].sort().join());
}
if (ACCRUAL) {
  const sha = require("crypto").createHash("sha256").update(fs.readFileSync(path.join(FISCAL, PENSION_FILE))).digest("hex");
  gate(`${PENSION_FILE} is the payload's pinned file (${ACCRUAL.source.commit})`, sha === ACCRUAL.source.sha256, sha.slice(0, 16));
  const gross = PENSION.central_decomposition.low.accrual_per_tax_dollar;
  gate("ratio_net is the central's gross ratio net of the group's share of future benefits taxed",
    Math.abs(gross * (1 - PENSION.benefit_tax.future_share_group) - ACCRUAL.ratio_net) < 1e-12, `${gross} x (1 - ${PENSION.benefit_tax.future_share_group})`);
  // The sensitivity's national money's worth [INFERENCE: a bridge]: the group's gross ratio times the national-to-group
  // ratio at trust-fund rates on scheduled benefits (the lane's national check, all 2024 taxpayers 15+, against the
  // group's arm at the same rates), net of the national share of future benefits returned as benefit tax.
  const nat = readJson("pension_accrual_2026_09_28/derived/national_prediction.json").oasdi_15_61.national_per_tax_dollar_ratio_route;
  const arm = fs.readFileSync(path.join(FISCAL, "pension_accrual_2026_09_28/derived/oasdi_arms.csv"), "utf8").trim().split("\n")
    .map((l) => l.split(",")).find((c) => c.slice(0, 7).join() === "individual_age_adjusted,EAN,tf,general,True,scheduled,note151_long_run");
  RATIO_NATIONAL = { ratio_net: gross * (nat / Number(arm[9])) * (1 - PENSION.benefit_tax.future_share_national_timing),
    inputs: { group_gross_central: gross, national_trust_fund_scheduled: nat, group_trust_fund_scheduled: Number(arm[9]),
      national_future_share_taxed: PENSION.benefit_tax.future_share_national_timing, group_future_share_taxed: PENSION.benefit_tax.future_share_group } };
}
// v5: the lineage's edits, the set's and the cash set's. A line's lineage amount is the sum of its edits at an allocation
// (receipts at the reference incidence rule).
const LINEAGE_EDITS = LINEAGE ? { set: P0.LINEAGE_EDITS, cash: P0.CASH.LINEAGE_EDITS } : null;
const lineageAmount = (which, side, id, key, a) => sum(LINEAGE_EDITS[which].filter((e) => e.side === side && e.line === id
  && (side === "receipt" ? e.scenario === REF : e.key === key)).map((e) => e.by[a]));
if (LINEAGE) {
  const E = LINEAGE.L.edits;
  gate(`v5: ${CORR_FILE}'s last ${E.count} edits are the package's lineage edits (meta.lineage.edits), row 8's last`,
    E.first + E.count === CORR.edits.length && JSON.stringify(CORR.edits.slice(E.first)) === JSON.stringify(P.LINEAGE_EDITS)
    && E.row8_edit_index === CORR.edits.length - 1 && CORR.edits[E.row8_edit_index].line === P.SYN.constants, `${E.first} + ${E.count}`);
  const S = LINEAGE_EDITS.set, C = LINEAGE_EDITS.cash;
  const differ = [...new Set(S.flatMap((e, i) => (Object.keys(e.by).some((k) => e.by[k] !== C[i].by[k]) ? [e.line] : [])))].sort();
  gate("v5: the set's and the cash set's lineage edits are the same cells and differ on the three accrual lines only",
    S.length === C.length && S.every((e, i) => e.side === C[i].side && e.line === C[i].line && e.key === C[i].key && e.scenario === C[i].scenario)
    && differ.join() === "federal_income_tax,medicare,social_security", differ.join(", "));
}

function planFor(spec, opts) {
  const o = Object.assign({ frame: "row4", justice: "arrests", corrections: "ratio" }, opts || {});
  const a = spec.allocation, W = o.frame;
  const ev = P.evaluateFull(UNION, spec).evaluation;
  const rows = [], checks = [];
  // An uncorrected-amount function U(state) on the frame, from the model's uncorrected cell and a key-totals object.
  function scaledOn(cell, pub, frame, label) {
    const sharePub = pub.T.GG / pub.V;
    // model.json stores shares to nine decimals.
    checks.push({ label, ok: Math.abs(sharePub - cell.share) <= 5e-10, detail: `${sharePub} vs ${cell.share}` });
    return (state) => cell.target_bn * (frame.T[state] / frame.V) / sharePub;
  }
  const withCorrections = (U, A) => {
    const kappa = A / U("GG");
    const amount = (alpha, pi) => {
      if (o.corrections === "none") return U(alpha + pi);
      if (alpha === "G" && pi === "G") return A;
      if (pi === "N") return U(alpha + "N");
      return o.corrections === "ratio" ? kappa * U(alpha + "G") : U(alpha + "G") + (A - U("GG"));
    };
    return { kappa, amount };
  };
  // Profile scalers for the synthetic lines and production (the group's own profile across ages, frame W).
  const ratioOf = (allocation, name) => { const t = keyTotals(W, allocation, name); return (alpha) => (alpha === "G" ? 1 : t.T.NG / t.T.GG); };
  const schoolRatio = ratioOf(a, "spending|school_operating"), mixRatio = ratioOf(a, "spending|education_mix");
  const wageRatio = ratioOf("personal", "receipt|wage");
  const edu = { school: keyTotals(W, a, "spending|school_operating"), mix: keyTotals(W, a, "spending|education_mix") };
  // v4's road lines: the group's persons aged 5 and over at national ages over its own (frame W).
  const fivePlus = (() => {
    const p = POP[W], NG = sum(p.union), NC = sum(p.national);
    const g = sum(p.union.filter((_, b) => EDGES[b] >= 5)), n = NG * sum(p.national.filter((_, b) => EDGES[b] >= 5)) / NC;
    return (alpha) => (alpha === "G" ? 1 : n / g);
  })();
  const accrualFacts = {};

  for (const [side, list] of [["receipt", ev.receipts], ["spending", ev.spending]]) {
    for (const r of list) {
      const row = { side, id: r.id, key: r.key, response: r.response, A: r.amount_bn };
      if (SYN_IDS.has(r.id)) {
        row.cls = "synthetic";
        if (o.corrections === "none") row.amount = () => (r.id === P.SYN.constants ? ROW8 : 0);
        else if (r.id === P.SYN.school) row.amount = (alpha, pi) => (pi === "N" ? 0 : r.amount_bn * schoolRatio(alpha));
        else if (r.id === P.SYN.college) row.amount = (alpha, pi) => (pi === "N" ? 0 : r.amount_bn * mixRatio(alpha));
        else row.amount = (alpha, pi) => (pi === "N" ? ROW8 : r.amount_bn);
      } else if (r.key === "external" || r.key === "none") {
        row.cls = "zero"; row.amount = () => r.amount_bn;
        if (r.amount_bn !== 0) throw new Error(`[BLOCKED] ${r.id} has an external key and a non-zero amount`);
      } else if (r.key === "population" || r.key === "resident_population") {
        row.cls = "per_head";
        // The case's corrected per-head amount is the row-4 frame's; the published frame is model.json's.
        const U0 = uncorrectedCell(side, r.id, r.key, a).target_bn;
        const perHead = W === "row4" ? r.amount_bn : (r.id === P.ENTERPRISE_LINE
          ? unionLine("receipt", r.id).national_bn * (lineOf(P.REKEY_LINE).keys.population[a].target_bn / lineOf(P.REKEY_LINE).national_bn)
          : U0);
        row.amount = () => perHead;
        if (side === "spending" && r.key === "population") {
          const t = keyTotals("row4", a, "spending|population"), tp = keyTotals("published", a, "spending|population");
          row.kappa = r.amount_bn / (U0 * (t.T.GG / t.V) / (tp.T.GG / tp.V));
        }
      } else if (r.response === 0) {
        row.cls = "held_zero_response"; row.amount = () => r.amount_bn;
      } else if (side === "spending" && r.id === "public_order_safety" && r.key === "use") {
        row.cls = "justice";
        const cell = uncorrectedCell(side, r.id, r.key, a);
        const pubPh = PH * FRAME.published.NG / FRAME.published.NC;
        const groupKeyed = cell.share * POS.national_bn - pubPh;  // the group's administrative keyed parts, key units
        const prof = JUSTICE_PROFILES[o.justice];
        const pub = justiceTotals("published", prof, groupKeyed), fr = justiceTotals(W, prof, lineageKeyed(W, prof, groupKeyed));
        const U = scaledOn(cell, pub, fr, `${r.id}/${r.key}`);
        Object.assign(row, withCorrections(U, r.amount_bn), { theta: fr.theta });
      } else if (side === "spending" && r.id === MEDICAID && r.key.startsWith("uninsured_use")) {
        row.cls = "uninsured";
        const cell = uncorrectedCell(side, r.id, r.key, a);
        const medCell = uncorrectedCell(side, r.id, "medicaid", a);
        const program = (id, name) => {
          const l = lineOf(id), c = l.keys[l.preferred_key].personal;
          return { cell: c, national: l.national_bn, pub: keyTotals("published", "personal", name), fr: keyTotals(W, "personal", name) };
        };
        const progs = { medicaid: program(MEDICAID, "spending|medicaid"), medicare: program("medicare", "spending|medicare"),
          health_other: program("health_services", "spending|health_other") };
        const py = { pub: keyTotals("published", "personal", "extra|exposure_py"), fr: keyTotals(W, "personal", "extra|exposure_py") };
        const frameOf = (w) => FRAME[w];
        // kg for a frame and state: each program's uncorrected personal cell at the state over its national line;
        // per head: 0.120245 (keys.py) scaled by the frame's headcount share.
        const kgAt = (which, state) => {
          const kg = {};
          for (const [p, x] of Object.entries(progs)) {
            const t = x[which];
            kg[p] = x.cell.target_bn * (t.T[state] / t.V) / (x.pub.T.GG / x.pub.V) / x.national;
          }
          const f = frameOf(which === "pub" ? "published" : W);
          kg.per_head = 0.120245 * (f.NG / f.NC) / (FRAME.published.NG / FRAME.published.NC);
          return kg;
        };
        const sAt = (which, state) => py[which].T[state] / py[which].V;
        // The arm that sets the key: argmin (low) or argmax (high) of the published union's arms.
        const pubArms = ARMS.map((arm) => armValue(arm, sAt("pub", "GG"), kgAt("pub", "GG")));
        const pick = r.key.endsWith("_low") ? pubArms.indexOf(Math.min(...pubArms)) : pubArms.indexOf(Math.max(...pubArms));
        const medPub = keyTotals("published", a, "spending|medicaid"), medFr = keyTotals(W, a, "spending|medicaid");
        const Umed = scaledOn(medCell, medPub, medFr, `${r.id}/medicaid`);
        checks.push({ label: `${r.id}/${r.key} arm`, ok: Math.abs(medCell.target_bn + pubArms[pick] - cell.target_bn) < 1e-6,
          detail: `${(medCell.target_bn + pubArms[pick]).toFixed(9)} vs ${cell.target_bn.toFixed(9)}` });
        const U = (state) => Umed(state) + armValue(ARMS[pick], sAt("fr", state), kgAt("fr", state));
        Object.assign(row, withCorrections(U, r.amount_bn), { arm: { year: ARMS[pick].year, sl: ARMS[pick].sl, n: ARMS[pick].n } });
      } else if (STATE_PRICE_PARENT[r.id]) {
        row.cls = "state_price"; row.parent = STATE_PRICE_PARENT[r.id];  // its amounts read the parent's row, below
      } else if (ROAD_LINES.has(r.id)) {
        row.cls = "roads_vmt";
        row.amount = (alpha, pi) => (pi === "N" ? 0 : r.amount_bn * fivePlus(alpha));
      } else if (r.id === HOUSING_ENTERPRISE) {
        row.cls = "follows_rental"; row.factor = "U";  // its amounts read the rental line's row, below
      } else if (IS_V4 && V4_KEYS[r.id]) {
        // An ACS key (profiles_sept29.py): the national line on the national per-age profile; kappa carries the
        // measured share over the frame's standardized one.
        row.cls = "profile_acs"; row.key = V4_KEYS[r.id].split("|")[1];
        const fr = keyTotals(W, a, V4_KEYS[r.id]), national = unionLine(side, r.id).national_bn;
        const U = (state) => national * fr.T[state] / fr.V;
        Object.assign(row, withCorrections(U, r.amount_bn), { U });
      } else {
        const name = `${side}|${r.key}`;
        const pub = keyTotals("published", a, name), fr = keyTotals(W, a, name);
        if (!pub) throw new Error(`[BLOCKED] no age profile for ${side}/${r.id}/${r.key} (response ${r.response})`);
        row.cls = "profile";
        const cell = uncorrectedCell(side, r.id, r.key, a);
        const U = scaledOn(cell, pub, fr, `${r.id}/${r.key}`);
        Object.assign(row, withCorrections(U, r.amount_bn), { U });
      }
      rows.push(row);
    }
  }
  // v4's rows that read other rows.
  const rowOf = (id) => rows.find((x) => x.id === id);
  for (const row of rows) {
    if (row.cls === "state_price") {
      const parent = rowOf(row.parent), A0 = parent.amount("G", "G");
      row.amount = (alpha, pi) => (pi === "N" ? 0 : row.A * parent.amount(alpha, "G") / A0);
    } else if (row.cls === "follows_rental") {
      const hs = rowOf(RENTAL_LINE), f = unionLine("receipt", row.id).national_bn / unionLine("spending", RENTAL_LINE).national_bn;
      row.amount = (alpha, pi) => f * hs.amount(alpha, pi);
      checks.push({ label: `${row.id} is its national over ${RENTAL_LINE}'s times ${RENTAL_LINE}'s amount`,
        ok: Math.abs(row.amount("G", "G") - row.A) < 1e-9, detail: `${row.amount("G", "G")} vs ${row.A}` });
    }
  }
  if (ACCRUAL) {
    if (o.corrections === "none") throw new Error("[BLOCKED] the accrual reads the corrected receipts: no corrections-off run on v4");
    const ss = rowOf("social_security"), med = rowOf("medicare"), fit = rowOf("federal_income_tax");
    const oasdi = ACCRUAL.oasdi_lines.map(rowOf), se = rowOf(ACCRUAL.se_line), hi = ["employee_hi", "employer_hi"].map(rowOf);
    const share = ACCRUAL.se_oasdi_share, sA = ACCRUAL.part_a_share;
    const oasdiAt = (alpha, rho) => sum(oasdi.map((x) => x.amount(alpha, rho))) + share * se.amount(alpha, rho);
    const hiAt = (alpha, rho) => sum(hi.map((x) => x.amount(alpha, rho))) + (1 - share) * se.amount(alpha, rho);
    // v5: the lineage's own amounts on the accrual lines. Social Security takes one ratio for the whole group, the
    // case's amount over its OASDI receipts; the lineage's Part A accrual is its set Medicare less its Parts B and D
    // ((1 - part_a_share) x its cash Medicare); its tax on current benefits is its cash income tax less its set one.
    const lin = LINEAGE ? (() => {
      const at = (which, row) => lineageAmount(which, row.side, row.id, row.key, a);
      const oasdiLin = sum(oasdi.map((x) => at("set", x))) + share * at("set", se), oasdiGG = oasdiAt("G", "G");
      const x = { social_security_bn: at("set", ss), oasdi_receipts_bn: oasdiLin, ratio_group: ss.A / oasdiGG,
        medicare_set_bn: at("set", med), medicare_cash_bn: at("cash", med), income_tax_set_bn: at("set", fit), income_tax_cash_bn: at("cash", fit) };
      Object.assign(x, { ratio_lineage: x.social_security_bn / oasdiLin, part_a_accrual_bn: x.medicare_set_bn - (1 - sA) * x.medicare_cash_bn,
        benefit_tax_bn: x.income_tax_cash_bn - x.income_tax_set_bn });
      const union29 = ACCRUAL.ratio_net * (oasdiGG - oasdiLin);
      checks.push({ label: "v5: the September 29 union's Social Security is ratio_net x its OASDI receipts (the case less the lineage)",
        ok: Math.abs(ss.A - x.social_security_bn - union29) < 1e-9, detail: `${ss.A - x.social_security_bn} vs ${union29}` });
      checks.push({ label: "v5: the lineage's Part A accrual and tax on current benefits are positive", ok: x.part_a_accrual_bn > 0 && x.benefit_tax_bn > 0,
        detail: `${x.part_a_accrual_bn}, ${x.benefit_tax_bn}` });
      return x;
    })() : null;
    // Social Security: ratio_net x the OASDI receipts of the state's ages and receipts profile (factor R).
    const ratioGroup = lin ? lin.ratio_group : ACCRUAL.ratio_net;
    const ratioAt = (rho) => (rho === "N" && o.accrual === "national_ratio" ? RATIO_NATIONAL.ratio_net : ratioGroup);
    Object.assign(ss, { cls: "accrual", factor: "R", kappa: undefined });
    ss.amount = (alpha, rho) => ratioAt(rho) * oasdiAt(alpha, rho);
    // Medicare: Parts B and D on the medicare key at the use profile, the Part A accrual at the ages and receipts
    // profile, scaled by covered workers (Part A turns on insured status, not on the tax paid) or, as the alternative,
    // by the HI receipts.
    const PA = ACCRUAL.part_a_accrual_bn + (lin ? lin.part_a_accrual_bn : 0);
    const covered = keyTotals(W, a, "receipt|positive_fica_worker");
    const partA = (alpha, rho) => PA * (o.part_a === "hi_scaled" ? hiAt(alpha, rho) / hiAt("G", "G") : covered.T[alpha + rho] / covered.T.GG);
    const cashMed = withCorrections(med.U, (med.A - PA) / (1 - sA));
    Object.assign(med, { cls: "medicare_accrual", kappa: cashMed.kappa });
    med.at = (alpha, rho, ups) => (1 - sA) * cashMed.amount(alpha, ups) + partA(alpha, rho);
    med.amount = (alpha, pi) => med.at(alpha, pi, pi);
    // Federal income tax: its key at the receipts profile, less the tax on current Social Security benefits (the benefit
    // key): the payload's dollars at R = G; at R = N the national rate on the national line.
    const btKey = keyTotals(W, a, "spending|social_security"), BT = ACCRUAL.benefit_tax_receipt_bn[a] + (lin ? lin.benefit_tax_bn : 0);
    const btNational = PENSION.benefit_tax.current_rate_nation * lineOf("social_security").national_bn;
    const bt = (alpha, rho) => (rho === "G" ? BT * btKey.T[alpha + "G"] / btKey.T.GG : btNational * btKey.T[alpha + "N"] / btKey.V);
    const cashFit = withCorrections(fit.U, fit.A + BT);
    Object.assign(fit, { cls: "income_tax_less_benefit_tax", kappa: cashFit.kappa });
    fit.amount = (alpha, rho) => cashFit.amount(alpha, rho) - bt(alpha, rho);
    for (const [row, v] of [[ss, ss.amount("G", "G")], [med, med.at("G", "G", "G")], [fit, fit.amount("G", "G")]]) {
      checks.push({ label: `${row.id}: the accrual rule reproduces the case's amount`, ok: Math.abs(v - row.A) < 1e-9, detail: `${v} vs ${row.A}` });
    }
    Object.assign(accrualFacts, { benefit_tax_national_bn: btNational, part_a_scaler: o.part_a === "hi_scaled" ? "hi_receipts" : "positive_fica_worker",
      oasdi_bn: Object.fromEntries(["NN", "GN", "NG", "GG"].map((s) => [s, oasdiAt(s[0], s[1])])),
      part_a_bn: Object.fromEntries(["NN", "GN", "NG", "GG"].map((s) => [s, partA(s[0], s[1])])),
      benefit_tax_bn: Object.fromEntries(["NN", "GN", "NG", "GG"].map((s) => [s, bt(s[0], s[1])])),
      medicare_cash_kappa: cashMed.kappa, income_tax_cash_kappa: cashFit.kappa }, lin ? { lineage: Object.assign(lin, {
      group_part_a_accrual_bn: PA, group_benefit_tax_bn: BT }) } : {});
  }
  // A row that reads other rows returns the case's own amount at the group's state, as withCorrections does (its
  // formula there is gated above to 1e-9).
  for (const row of rows) {
    if (!["state_price", "follows_rental", "accrual", "medicare_accrual", "income_tax_less_benefit_tax"].includes(row.cls)) continue;
    const f = row.amount, g = row.at;
    row.amount = (alpha, pi) => (alpha === "G" && pi === "G" ? row.A : f(alpha, pi));
    if (g) row.at = (alpha, rho, ups) => (alpha === "G" && rho === "G" && ups === "G" ? row.A : g(alpha, rho, ups));
  }
  // Education: the school part of the line's key at each state (for the line split only).
  const schoolFraction = (alpha, pi) => {
    const st = alpha + (pi === "N" ? "N" : "G");
    return edu.school.T[st] / edu.mix.T[st];
  };
  const production = (alpha, rho) => (rho === "N" ? 0 : wageRatio(alpha));
  return { spec, a, rows, checks, production, schoolFraction, opts: o, accrual: accrualFacts };
}

// ---------------------------------------------------------------------------------------------------
// States.
const STATES = ["N", "G"].flatMap((A) => ["N", "G"].flatMap((R) => ["N", "G"].map((U) => A + R + U)));
function stateModel(plan, st) {
  const [alpha, rho, ups] = st;
  const m = Engine.clone(UNION);
  const ri = new Map(m.receipts.lines.map((l, i) => [l.id, i])), si = new Map(m.spending.lines.map((l, i) => [l.id, i]));
  for (const row of plan.rows) {
    // A row's profile factor is its side's (R for receipts, U for spending) unless it names another; the Medicare
    // accrual reads both.
    const v = row.at ? row.at(alpha, rho, ups) : row.amount(alpha, (row.factor || (row.side === "receipt" ? "R" : "U")) === "R" ? rho : ups);
    if (row.side === "receipt") m.receipts.lines[ri.get(row.id)].cells[REF][plan.a].target_bn = v;
    else m.spending.lines[si.get(row.id)].keys[row.key][plan.a].target_bn = v;
  }
  const f = plan.production(alpha, rho);
  m.production.private_wtp_bn = UNION.production.private_wtp_bn.map((x) => x * f);
  m.production.induced_receipts_bn = UNION.production.induced_receipts_bn.map((x) => x * f);
  return m;
}

// Line groups for the split of parts 3 and 4.
const GROUPS = {
  income_taxes: ["federal_income_tax", "state_local_income_tax", "other_personal_tax"],
  payroll_taxes: ["employee_oasdi", "employee_hi", "self_employment_oasdi_hi", "employer_oasdi", "employer_hi",
    "other_domestic_social_contributions", "medicare_supplementary_premiums"],
  consumption_taxes: ["general_sales_tax", "excise_selective_sales", "customs_duties", "personal_current_transfers"],
  other_receipts: ["personal_motor_vehicle", "personal_property_tax", "corporate_capital", "corporate_labor", "modeled_owner_property",
    "remaining_production_property", "other_production_taxes", "rest_world_tax_contributions", "government_asset_income",
    "business_current_transfers", "rest_world_current_transfers", "source_rounding"],
  medicaid: [MEDICAID],
  justice: ["public_order_safety"],
  refundable_credits: ["refundable_tax_credits"],
  social_security_medicare: ["social_security", "railroad_retirement", "medicare", "pension_guaranty"],
  health_veterans: ["health_services", "veterans_pension_disability", "veterans_readjustment", "veterans_other",
    "veterans_life_insurance", "military_medical"],
  cash_food_housing_benefits: ["income_security_services", "snap", "ssi", "family_and_general_assistance", "other_state_welfare",
    "energy_assistance", "unemployment", "other_federal_benefits", "housing_subsidies", "workers_compensation",
    "temporary_disability", "black_lung", "employment_training"],
  roads_economic_affairs: ["economic_affairs_services", "agricultural_subsidies", "transport_subsidies", "other_subsidies"],
  per_head_government_and_enterprises: ["general_public_services", "recreation_culture", "housing_community_services",
    "other_state_benefits", "defense", "domestic_interest", "foreign_interest", "foreign_territory_social_benefits",
    "other_foreign_current_transfers", "enterprise_surplus"],
  care_shelter_audit_constants: [P.SYN.constants],
};
if (IS_V4) {
  // Item 5's responsive property taxes in a group of their own; v4's new lines with their parents.
  GROUPS.property_taxes = ["modeled_owner_property", "tenant_occupied_property", "personal_property_tax"];
  GROUPS.other_receipts = GROUPS.other_receipts.filter((id) => !GROUPS.property_taxes.includes(id));
  GROUPS.cash_food_housing_benefits.push(HOUSING_ENTERPRISE);
  GROUPS.roads_economic_affairs.push(...ROAD_LINES);
  for (const [line, parent] of Object.entries(STATE_PRICE_PARENT)) GROUPS[Object.keys(GROUPS).find((g) => GROUPS[g].includes(parent))].push(line);
}
const GROUP_OF = {};
for (const [g, ids] of Object.entries(GROUPS)) for (const id of ids) GROUP_OF[id] = g;
const CAPITAL_GROUP = (c) => {
  if (c.id === "k12") return "schools";
  if (c.id === "college") return "colleges_other_education";
  if (c.part === "enterprise") return "per_head_government_and_enterprises";
  const line = c.key.numerator_lines ? c.key.numerator_lines[0] : c.key.parent_line || c.key.line;
  return GROUP_OF[line];
};
const GROUP_NAMES = ["income_taxes", "payroll_taxes", "consumption_taxes", "production_term", "other_receipts", "schools",
  "colleges_other_education", "medicaid", "justice", "refundable_credits", "social_security_medicare", "health_veterans",
  "cash_food_housing_benefits", "roads_economic_affairs", "per_head_government_and_enterprises", "care_shelter_audit_constants"];
if (IS_V4) GROUP_NAMES.splice(GROUP_NAMES.indexOf("production_term"), 0, "property_taxes");

function evaluateState(plan, st) {
  const m = stateModel(plan, st);
  const full = P.evaluateFull(m, plan.spec);
  const ev = full.evaluation;
  const g = Object.fromEntries(GROUP_NAMES.map((n) => [n, 0]));
  const add = (name, v) => { if (!(name in g)) throw new Error("[BLOCKED] no group " + name); g[name] += v; };
  for (const r of ev.receipts) add(GROUP_OF[r.id] || "unmapped", -r.effect_bn);
  const sf = plan.schoolFraction(st[0], st[2]);
  for (const s of ev.spending) {
    const c = -s.effect_bn;
    if (s.id === "education_services") { add("schools", c * sf); add("colleges_other_education", c * (1 - sf)); }
    else if (s.id === P.SYN.school) add("schools", c);
    else if (s.id === P.SYN.college || s.id === "education_benefits") add("colleges_other_education", c);
    else add(GROUP_OF[s.id] || "unmapped", c);
  }
  add("production_term", -(ev.private_wtp_bn + ev.induced_receipts_bn));  // fiscal weight 1 (the package's state)
  const comps = P.componentsFor(plan.spec.capital_variant);
  for (const c of full.capital.components) add(CAPITAL_GROUP(comps.find((x) => x.id === c.id)), c.return_bn);
  const zeroResponse = { receipts: sum(ev.receipts.filter((x) => x.response === 0).map((x) => x.amount_bn)),
    spending: sum(ev.spending.filter((x) => x.response === 0).map((x) => x.amount_bn)) };
  const parts = { receipts_bn: -sum(ev.receipts.map((x) => x.effect_bn)), operating_bn: -sum(ev.spending.map((x) => x.effect_bn)),
    production_bn: -(ev.private_wtp_bn + ev.induced_receipts_bn), capital_bn: full.capital.total_bn };
  return { cost: full.cost_bn, groups: g, model: m, full, zeroResponse, parts };
}

// ---------------------------------------------------------------------------------------------------
// Orders and the Shapley mean.
const FACTORS = ["A", "R", "U"];
const PART_OF = { A: "age_structure", R: "taxes_at_given_ages", U: "service_use_at_given_ages" };
const ORDERS = [["A", "R", "U"], ["A", "U", "R"], ["R", "A", "U"], ["R", "U", "A"], ["U", "A", "R"], ["U", "R", "A"]];
const stateOf = (on) => FACTORS.map((f) => (on[f] ? "G" : "N")).join("");
function decompose(values) {  // values: {state: number or {group: number}}
  const isNum = typeof values.NNN === "number";
  const minus = (x, y) => (isNum ? x - y : Object.fromEntries(Object.keys(x).map((k) => [k, x[k] - y[k]])));
  const plus = (x, y) => (isNum ? x + y : Object.fromEntries(Object.keys(x).map((k) => [k, x[k] + y[k]])));
  const times = (x, c) => (isNum ? x * c : Object.fromEntries(Object.keys(x).map((k) => [k, x[k] * c])));
  const byOrder = {};
  const shapley = {};
  for (const order of ORDERS) {
    const on = {}, parts = {};
    let prev = "NNN";
    for (const f of order) { on[f] = true; const next = stateOf(on); parts[f] = minus(values[next], values[prev]); prev = next; }
    byOrder[order.join("-")] = parts;
    for (const f of FACTORS) shapley[f] = shapley[f] === undefined ? times(parts[f], 1 / ORDERS.length) : plus(shapley[f], times(parts[f], 1 / ORDERS.length));
  }
  return { shared: values.NNN, byOrder, shapley };
}

function runEnd(spec, opts) {
  const plan = planFor(spec, opts);
  const out = {};
  for (const st of STATES) out[st] = evaluateState(plan, st);
  return { plan, states: out };
}

// ---------------------------------------------------------------------------------------------------
// Main run.
console.log("[decomposition]");
const main = {};
for (const [end, i] of ENDS) {
  const r = runEnd(SPECS[i]);
  main[end] = r;
  const bad = r.plan.checks.filter((c) => !c.ok);
  gate(`${end} end: published-frame key shares reproduce model.json's uncorrected cells (${r.plan.checks.length} checks)`, !bad.length,
    bad.map((c) => `${c.label}: ${c.detail}`).join("; "));
  const ggg = r.states.GGG;
  const u = P.evaluateFull(UNION, SPECS[i]);
  const sameLines = u.evaluation.receipts.every((x, k) => ggg.full.evaluation.receipts[k].amount_bn === x.amount_bn)
    && u.evaluation.spending.every((x, k) => ggg.full.evaluation.spending[k].amount_bn === x.amount_bn);
  gate(`${end} end: state GGG is the union, line by line and in cost`, sameLines && Math.abs(ggg.cost - u.cost_bn) < 1e-9,
    `${ggg.cost.toFixed(6)} vs ${u.cost_bn.toFixed(6)}`);
  const ph = r.plan.rows.filter((x) => x.kappa !== undefined && x.cls === "per_head");
  gate(`${end} end: per-head lines' corrected amounts are the row-4 frame's (kappa within 1e-4 of 1)`,
    ph.every((x) => Math.abs(x.kappa - 1) < 1e-4), ph.map((x) => `${x.id} ${x.kappa.toFixed(7)}`).join(", "));
  const worstSum = Math.max(...STATES.map((st) => Math.abs(sum(Object.values(r.states[st].groups)) - r.states[st].cost)));
  gate(`${end} end: line-group contributions add to each state's cost`, worstSum < 1e-9, `worst ${worstSum.toExponential(1)}`);
}

// Parts.
const costs = Object.fromEntries(ENDS.map(([end]) => [end, Object.fromEntries(STATES.map((st) => [st, main[end].states[st].cost]))]));
const groupVals = Object.fromEntries(ENDS.map(([end]) => [end, Object.fromEntries(STATES.map((st) => [st, main[end].states[st].groups]))]));
const D = Object.fromEntries(ENDS.map(([end]) => [end, decompose(costs[end])]));
const DG = Object.fromEntries(ENDS.map(([end]) => [end, decompose(groupVals[end])]));
for (const [end] of ENDS) {
  const total = costs[end].GGG, target = CASE[end === "low" ? 0 : 1];
  const worst = Math.max(...Object.values(D[end].byOrder).map((p) => Math.abs(D[end].shared + p.A + p.R + p.U - target)));
  const sh = D[end].shapley;
  gate(`(a) ${end} end: parts 1-4 add to the case in all six orders and in the Shapley mean`,
    worst < 1e-9 && Math.abs(D[end].shared + sh.A + sh.R + sh.U - target) < 1e-9, `worst ${worst.toExponential(1)}; case ${total.toFixed(4)}`);
}

// (c) Twice the average residents.
console.log("[linearity]");
const linearity = {};
for (const [end, i] of ENDS) {
  const plan = main[end].plan, spec = SPECS[i];
  const m = stateModel(plan, "NNN");
  const ri = new Map(m.receipts.lines.map((l, k) => [l.id, k])), si = new Map(m.spending.lines.map((l, k) => [l.id, k]));
  for (const row of plan.rows) {
    if (row.side === "receipt") m.receipts.lines[ri.get(row.id)].cells[REF][plan.a].target_bn *= 2;
    else m.spending.lines[si.get(row.id)].keys[row.key][plan.a].target_bn *= 2;
  }
  const c2 = P.evaluateFull(m, spec).cost_bn;
  gate(`(c) ${end} end: twice the average residents cost twice part 1`, Math.abs(c2 - 2 * D[end].shared) < 1e-9,
    `${c2.toFixed(6)} vs 2 x ${D[end].shared.toFixed(6)}`);
  linearity[end] = { part1_bn: D[end].shared, twice_bn: c2 };
}
// What the engine holds fixed that is not linear in substance: finite-removal responses computed at the case's s.
const R26 = readJson("finite_response_2026_09_26/derived/r_values.json");
const LRJ = P.LR;
const rOf = (b, s) => (1 - Math.pow(1 - s, b)) / s;
// v5 doubles its own group share; v4's is the memo's.
if (LINEAGE) gate("v5: the lineage's v4 group share is the finite-removal memo's s", LINEAGE.L.s.v4 === R26.s_national_memo,
  `${LINEAGE.L.s.v4} vs ${R26.s_national_memo}; v5 ${LINEAGE.L.s.v5}`);
const S0 = LINEAGE ? LINEAGE.L.s.v5 : R26.s_national_memo;
{
  for (const [end, i] of ENDS) {
    const spec = SPECS[i], reading = spec.reading;
    const b = reading === "low" ? R26.gg_low_b_unrounded : R26.gg_high_b;
    const gg2 = rOf(b, 2 * S0);
    // Long-run subfunctions whose reading is a finite removal (strictly between 0 and 1) are re-read at 2s.
    const E = LRJ.elasticities;
    const bFor = (sf) => (sf.id.includes("general_economic") ? E.administration_general_government.b
      : sf.id.includes("recreation") ? E.parks.across_states.b : E.highways_nontoll.across_states.b);
    const reread = {};
    for (const line of P.LR_LINES) {
      reread[line] = sum(LRJ.lines[line].subfunctions.map((sf) => {
        const v = sf.response[reading];
        if (v === 0 || v === 1) return sf.share_of_line * v;
        if (sf.id.includes("general_economic")) return sf.share_of_line * rOf(R26.gg_high_b, 2 * S0);  // administration, b 0.842
        return sf.share_of_line * rOf(bFor(sf), 2 * S0);
      }));
    }
    const nn = main[end].states.NNN.full.evaluation;
    const amt = (id) => nn.spending.find((x) => x.id === id).amount_bn;
    const resp = (id) => nn.spending.find((x) => x.id === id).response;
    const dGG = 2 * amt("general_public_services") * (gg2 - resp("general_public_services"));
    const dLR = sum(P.LR_LINES.map((id) => 2 * amt(id) * (reread[id] - resp(id))));
    linearity[end].finite_removal_at_2s = {
      s: S0, general_government_response: [resp("general_public_services"), gg2], general_government_change_bn: dGG,
      long_run_responses: Object.fromEntries(P.LR_LINES.map((id) => [id, [resp(id), reread[id]]])), long_run_change_bn: dLR,
      note: "engine operating lines only; the capital return's long-run subfunction responses and row 8's finite factor are not re-read",
    };
  }
}

// ---------------------------------------------------------------------------------------------------
// Sensitivities: the justice profile flat over 18-64, corrections as fixed dollars, part 1 at 40.90M.
console.log("[sensitivities]");
const sens = {};
// v4: no corrections-off run (its payload's edits carry the accrual and the items, not only the dataset corrections; the
// cash set is decomposed as its own case); the accrual's two alternative rules instead.
const SENS = [["justice_flat_18_64", { justice: "flat_18_64" }], ["corrections_fixed_dollars", { corrections: "fixed" }]]
  .concat(IS_V4 ? [] : [["corrections_off", { corrections: "none" }]])
  .concat(ACCRUAL ? [["accrual_national_ratio", { accrual: "national_ratio" }], ["part_a_hi_scaled", { part_a: "hi_scaled" }]] : []);
for (const [name, opts] of SENS) {
  sens[name] = {};
  for (const [end, i] of ENDS) {
    const r = runEnd(SPECS[i], opts);
    const d = decompose(Object.fromEntries(STATES.map((st) => [st, r.states[st].cost])));
    sens[name][end] = { shared: d.shared, age_structure: d.shapley.A, taxes_at_given_ages: d.shapley.R, service_use_at_given_ages: d.shapley.U,
      total: r.states.GGG.cost };
    if (name === "corrections_off") {
      // The case's corrections enter only where a profile is the group's: their share of each part.
      sens[name][end].corrections_contribution = { age_structure: D[end].shapley.A - d.shapley.A,
        taxes_at_given_ages: D[end].shapley.R - d.shapley.R, service_use_at_given_ages: D[end].shapley.U - d.shapley.U };
      const dg = decompose(Object.fromEntries(STATES.map((st) => [st, r.states[st].groups])));
      sens[name][end].corrections_contribution_by_group = Object.fromEntries(FACTORS.map((f) => [PART_OF[f],
        Object.fromEntries(GROUP_NAMES.map((g) => [g, DG[end].shapley[f][g] - dg.shapley[f][g]]))]));
      gate(`${name} ${end}: part 1 is unchanged without the corrections`, Math.abs(d.shared - D[end].shared) < 1e-9);
    } else {
      gate(`${name} ${end}: parts add to the case`, Math.abs(d.shared + d.shapley.A + d.shapley.R + d.shapley.U - CASE[end === "low" ? 0 : 1]) < 1e-9);
    }
  }
}
// v5's added people are counted on the account's frame (row 4) only, so part 1 has no published-count reading.
sens.part1_at_published_count = LINEAGE ? { not_computed: "the lineage's added people are counted on the account's frame (audit row 4) only" } : {};
for (const [end, i] of LINEAGE ? [] : ENDS) {
  const r = planFor(SPECS[i], { frame: "published" });
  const c = P.evaluateFull(stateModel(r, "NNN"), SPECS[i]).cost_bn;
  sens.part1_at_published_count[end] = { part1_bn: c, part1_row4_bn: D[end].shared, difference_bn: c - D[end].shared };
}

// ---------------------------------------------------------------------------------------------------
// Outputs.
fs.mkdirSync(OUT, { recursive: true });
const f6 = (x) => (Math.abs(x) < 5e-13 ? 0 : x).toFixed(6);
// Per member: the September 27 outputs divide by the record's 40,896,574, as they were written; v4's divide by the
// 39,712,493 people the account prices (the row-4 union, this lane's finding, which the decision of 2026-09-29 adopts).
// v5's divide by the lineage's 42,752,213, the row-4 union plus the added people.
const PER_MEMBER = SUFFIX ? FRAME.row4.NG : MEMBERS;
if (SUFFIX && !LINEAGE) gate("v4's per-member count is the account's 39,712,493 (the row-4 union)", Math.round(PER_MEMBER) === 39712493, PER_MEMBER.toFixed(2));
if (LINEAGE) gate("v5's per-member count is the lineage's 42,752,213 (the row-4 union plus the added people)",
  Math.round(PER_MEMBER) === 42752213 && Math.abs(PER_MEMBER - LINEAGE.L.counts.lineage_population) < 1e-3, PER_MEMBER.toFixed(2));
const perMember = (bn) => Math.round(bn * 1e9 / PER_MEMBER);
const lines = [["part", "order", "low_bn", "high_bn", "per_member_low", "per_member_high", "share_of_total", "share_low", "share_high"].join(",")];
const shareRow = (lo, hi) => [f6((lo + hi) / (CASE[0] + CASE[1])), f6(lo / CASE[0]), f6(hi / CASE[1])];
const row = (part, order, lo, hi) => lines.push([part, order, f6(lo), f6(hi), perMember(lo), perMember(hi), ...shareRow(lo, hi)].join(","));
row("shared", "all", D.low.shared, D.high.shared);
for (const f of FACTORS) {
  for (const order of ORDERS) {
    const k = order.join("-");
    row(PART_OF[f], k, D.low.byOrder[k][f], D.high.byOrder[k][f]);
  }
  row(PART_OF[f], "shapley", D.low.shapley[f], D.high.shapley[f]);
}
row("total", "all", costs.low.GGG, costs.high.GGG);
fs.writeFileSync(path.join(OUT, `decomposition${SUFFIX}.csv`), lines.join("\n") + "\n");

const gl = [["part", "line_group", "low_bn", "high_bn"].join(",")];
for (const g of GROUP_NAMES) gl.push(["shared", g, f6(DG.low.shared[g]), f6(DG.high.shared[g])].join(","));
for (const f of FACTORS) for (const g of GROUP_NAMES) gl.push([PART_OF[f], g, f6(DG.low.shapley[f][g]), f6(DG.high.shapley[f][g])].join(","));
for (const g of GROUP_NAMES) gl.push(["total", g, f6(groupVals.low.GGG[g]), f6(groupVals.high.GGG[g])].join(","));
fs.writeFileSync(path.join(OUT, `decomposition_lines${SUFFIX}.csv`), gl.join("\n") + "\n");
for (const [end] of ENDS) {
  for (const f of FACTORS) {
    const s = sum(Object.values(DG[end].shapley[f]));
    gate(`${end} end: the ${PART_OF[f]} line groups add to the part`, Math.abs(s - D[end].shapley[f]) < 1e-9, `${s.toFixed(6)}`);
  }
}

const sl = [["state", "age", "receipts", "use", "low_bn", "high_bn"].join(",")];
for (const st of STATES) sl.push([st, st[0], st[1], st[2], f6(costs.low[st]), f6(costs.high[st])].join(","));
fs.writeFileSync(path.join(OUT, `states${SUFFIX}.csv`), sl.join("\n") + "\n");

const round = (x) => (typeof x === "number" ? Number(x.toPrecision(12)) : x);
const deep = (o) => JSON.parse(JSON.stringify(o, (k, v) => round(v)));
const lineTable = Object.fromEntries(ENDS.map(([end]) => [end, main[end].plan.rows.map((r) => ({
  side: r.side, id: r.id, key: r.key, class: r.cls, response: r.response, corrected_bn: r.A,
  kappa: r.kappa === undefined ? null : r.kappa, theta: r.theta === undefined ? null : r.theta, arm: r.arm || null,
  amounts_bn: Object.fromEntries(["NN", "GN", "NG", "GG"].map((s) => [s, r.amount(s[0], s[1])])),
}))]));
const summary = {
  lane: "main_case_decomposition_2026_09_29",
  case: Object.assign({ lane: CASE_DEF.lane, bn: CASE, ends: { low: LO, high: HI } }, SUFFIX ? { key: CASE_KEY, payload: CORR_FILE } : {}),
  members: PER_MEMBER,
  frame: { published: FRAME.published, row4: FRAME.row4, household_fraction: HF,
    note: "row4: the stack's audit row 4 weights; the case's per-head lines are charged at this union count" },
  parts: Object.fromEntries(ENDS.map(([end]) => [end, { shared: D[end].shared, shapley: Object.fromEntries(FACTORS.map((f) => [PART_OF[f], D[end].shapley[f]])),
    by_order: Object.fromEntries(Object.entries(D[end].byOrder).map(([k, v]) => [k, Object.fromEntries(FACTORS.map((f) => [PART_OF[f], v[f]]))])) }])),
  states_bn: costs,
  production: Object.fromEntries(ENDS.map(([end]) => [end, {
    group_P_plus_F_bn: main[end].states.GGG.full.evaluation.private_wtp_bn + main[end].states.GGG.full.evaluation.induced_receipts_bn,
    at_national_ages_factor: main[end].plan.production("N", "G") }])),
  row8_bn: ROW8,
  // Receipts by group at the group's profile over the national profile, at the group's ages (GG / GN) and at
  // national ages (NG / NN).
  receipt_ratios: Object.fromEntries(ENDS.map(([end]) => [end, Object.fromEntries(["income_taxes", "payroll_taxes", "consumption_taxes"].map((g) => {
    const rows = main[end].plan.rows.filter((r) => r.side === "receipt" && GROUP_OF[r.id] === g);
    const tot = (st) => sum(rows.map((r) => r.amount(st[0], st[1])));
    return [g, { at_group_ages: tot("GG") / tot("GN"), at_national_ages: tot("NG") / tot("NN"), GG: tot("GG"), GN: tot("GN"), NG: tot("NG"), NN: tot("NN") }];
  }))])),
  part1_composition: Object.fromEntries(ENDS.map(([end]) => [end, Object.assign({}, main[end].states.NNN.parts,
    { amounts_at_zero_response_bn: main[end].states.NNN.zeroResponse })])),
  // Lines the case holds at zero response, at average residents' shares (receipts N/Nciv, spending hf x N/Nciv on the
  // row-4 frame): what the response conventions keep out of part 1.
  zero_response_at_average_residents: Object.fromEntries(ENDS.map(([end]) => [end, (() => {
    const f = FRAME.row4, sr = f.NG / f.NC, ss = HF * f.NG / f.NC;
    const pick = (side) => main[end].plan.rows.filter((r) => r.side === side && r.response === 0 && r.cls !== "zero")
      .map((r) => [r.id, unionLine(side, r.id).national_bn * (side === "receipt" ? sr : ss)]);
    const rec = Object.fromEntries(pick("receipt")), spe = Object.fromEntries(pick("spending"));
    return { receipts: rec, receipts_total_bn: sum(Object.values(rec)), spending: spe, spending_total_bn: sum(Object.values(spe)) };
  })()])),
  by_component: Object.fromEntries(ENDS.map(([end]) => [end, (() => {
    const comp = decompose(Object.fromEntries(STATES.map((st) => [st, main[end].states[st].parts])));
    return { shared: comp.shared, shapley: Object.fromEntries(FACTORS.map((f) => [PART_OF[f], comp.shapley[f]])) };
  })()])),
  linearity,
  sensitivities: sens,
  lines: lineTable,
};
if (IS_V4) {
  const rowsOf = (end, cls) => main[end].plan.rows.filter((r) => r.cls === cls);
  summary.v4 = {
    rules: {
      pension_accrual: ACCRUAL ? "social_security = ratio_net x OASDI receipts at (A, R); medicare = (1 - part_a_share) x the medicare key at (A, U), "
        + "corrected by its September 27 kappa, + the Part A accrual x covered workers at (A, R) / at GG; federal_income_tax = its key at (A, R) "
        + "with kappa on the cash amount (case + benefit tax) - the benefit tax on the Social Security benefit key at (A, R): the payload's "
        + "dollars at R = G, current_rate_nation x the national Social Security line at R = N" : null,
      property_taxes: "modeled_owner_property on the account's CPS key (profiles_sept29.py; published-share gate); tenant_occupied_property on ACS "
        + "contract rent and personal_property_tax on ACS household vehicles (per-person rates by age x the frame's headcount; kappa = the "
        + "measured share over the standardized one); factor R",
      housing_enterprise_surplus: "its national over housing_subsidies' national x housing_subsidies' amount at (A, U); factor U",
      state_price: "the parent's amount at (A, G) x the line's amount over the parent's at GG; 0 at U = N",
      roads_vmt: "the case's amount x the group's persons 5+ at national ages over its own at A = N; 0 at U = N",
      national_scale: "a scaled line's uncorrected cell is model.json's x (payload national / model.json national)",
    },
    accrual: ACCRUAL ? Object.fromEntries(ENDS.map(([end]) => [end, main[end].plan.accrual])) : null,
    accrual_national_ratio: RATIO_NATIONAL,
    kappas: Object.fromEntries(ENDS.map(([end]) => [end, Object.fromEntries(main[end].plan.rows
      .filter((r) => ["profile_acs", "medicare_accrual", "income_tax_less_benefit_tax"].includes(r.cls) || r.id === "modeled_owner_property")
      .map((r) => [r.id, r.kappa]))])),
    // Each named line's own cost contribution (-effect) over the eight states, split the same way (Shapley means).
    line_parts: Object.fromEntries(ENDS.map(([end]) => [end, Object.fromEntries(["social_security", "medicare", "federal_income_tax",
      "modeled_owner_property", "tenant_occupied_property", "personal_property_tax", HOUSING_ENTERPRISE, RENTAL_LINE, ...ROAD_LINES,
      ...Object.keys(STATE_PRICE_PARENT)].map((id) => {
      const at = (st) => { const ev = main[end].states[st].full.evaluation;
        const x = ev.receipts.find((r) => r.id === id) || ev.spending.find((r) => r.id === id); return -x.effect_bn; };
      const d = decompose(Object.fromEntries(STATES.map((st) => [st, at(st)])));
      return [id, { shared: d.shared, age_structure: d.shapley.A, taxes_at_given_ages: d.shapley.R, service_use_at_given_ages: d.shapley.U, total: at("GGG") }];
    }))])),
    state_price_parents: STATE_PRICE_PARENT,
    road_lines: [...ROAD_LINES],
    classes: Object.fromEntries(ENDS.map(([end]) => [end, Object.fromEntries(["state_price", "roads_vmt", "follows_rental", "profile_acs", "accrual",
      "medicare_accrual", "income_tax_less_benefit_tax"].map((c) => [c, rowsOf(end, c).map((r) => r.id)]))])),
  };
}
if (LINEAGE) {
  const E = LINEAGE.L.edits, row8v4 = P.CONSTANTS.row8.c * P0.SEPT29.RESPONSES.row8_factor;
  gate("v5: row 8 is v4's plus the lineage's row-8 edit (c x row8_factor at each share)", Math.abs(row8v4 + E.row8_edit_bn - ROW8) < 1e-12,
    `${row8v4} + ${E.row8_edit_bn} vs ${ROW8}`);
  // The lineage's lane-constants edit prices G3+ members at G3+'s share of the September 29 cell, row 8 included (whites
  // carry none): the part of it that is row 8.
  const row8InLineage = Object.fromEntries(ENDS.map(([end]) => {
    const a = main[end].plan.a, all = lineageAmount(CASE_DEF.cash ? "cash" : "set", "spending", P.SYN.constants, "k", a);
    const cell29 = UNION.spending.lines.find((l) => l.id === P.SYN.constants).keys.k[a].target_bn - all, people = all - E.row8_edit_bn;
    return [end, { allocation: a, lineage_edit_bn: people, september_29_cell_bn: cell29, row8_part_bn: people * row8v4 / cell29 }];
  }));
  summary.v5 = {
    rules: {
      added_people: "meta.lineage.counts.added placed at the identified G3+'s ages (profiles_oct05.py: convention a, the ASEC person weights, "
        + "this lane's bins); every row-4 union key vector is scaled by (union + added) / union in each bin, so the added people carry the "
        + "union's per-person key at their ages; the lineage's own amounts (its edits) enter through each line's kappa, as the corrections "
        + "do; the published frame stays model.json's",
      justice: "the added people's keyed parts at the union's relative risk theta on the row-4 frame (theta held)",
      pension_accrual: "social_security = the group's ratio (the case's amount over its OASDI receipts) x the OASDI receipts at (A, R); "
        + "medicare's Part A accrual = part_a_accrual_bn + the lineage's set Medicare less (1 - part_a_share) x its cash Medicare; the tax on "
        + "current benefits = benefit_tax_receipt_bn + the lineage's cash less its set federal income tax",
      lane_constants: "the lineage's edit is the added people's own (0 at U = N), as the line's amount beyond row 8; at U = N row 8 is c x "
        + "v5's row8_factor (row8_in_lineage gives the part of the edit that is G3+'s share of row 8)",
      finite_removal_note: "the linearity note's 2s is twice v5's group share (meta.lineage.s.v5)",
      part1_at_published_count: "not computed: the lineage's added people are counted on the account's frame only",
    },
    added: { persons: LINEAGE.M, members: PER_MEMBER, identified_g3plus: LINEAGE.G3,
      by_bin: Object.fromEntries(EDGES.map((e, b) => [e, LINEAGE.added[b]])), scale_by_bin: Object.fromEntries(EDGES.map((e, b) => [e, LINEAGE.scale[b]])) },
    accrual: ACCRUAL ? Object.fromEntries(ENDS.map(([end]) => [end, main[end].plan.accrual.lineage])) : null,
    justice_theta: Object.fromEntries(ENDS.map(([end]) => [end, main[end].plan.rows.find((r) => r.cls === "justice").theta])),
    row8: { v4_bn: row8v4, v5_bn: ROW8, lineage_edit_bn: E.row8_edit_bn },
    row8_in_lineage: row8InLineage,
  };
}
fs.writeFileSync(path.join(OUT, `summary${SUFFIX}.json`), JSON.stringify(deep(summary), null, 1) + "\n");

console.log("\nParts ($bn, Shapley mean; low / high):");
console.log(`  shared ${D.low.shared.toFixed(2)} / ${D.high.shared.toFixed(2)}`);
for (const f of FACTORS) console.log(`  ${PART_OF[f]} ${D.low.shapley[f].toFixed(2)} / ${D.high.shapley[f].toFixed(2)}`);
console.log(`  total ${costs.low.GGG.toFixed(4)} / ${costs.high.GGG.toFixed(4)}`);
if (fails.length) { console.log(`FAIL: ${fails.length} gate(s)`); process.exit(1); }
console.log("all gates passed");
