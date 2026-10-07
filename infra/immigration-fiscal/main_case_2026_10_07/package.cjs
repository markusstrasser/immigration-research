/* Main case v6, adopted 2026-10-07 (decisions/2026-10-07-main-case-v6.md): main case v5 (main_case_2026_10_05,
 * adopted 2026-10-05) plus a registry of items, each with its own provenance. Consumers key it oct07. The adopted case
 * is caseOf(v5, CANDIDATE) with no arm; its payloads carry adopted "2026-10-07" and v5's status form. Every other
 * combination (an arm, fewer items) is a variant, stamped adopted null. The package has v5's API: the same export names,
 * functions and signatures (../main_case_2026_10_05/package.cjs), so a consumer moves from oct05 to oct07 by changing
 * the lane it reads, and then routes the items (meta.items).
 *
 *   - An item (REGISTRY) is {id, kind, label, source, cash: {applies, why}, arms, build}. Two kinds:
 *       edit_set  build(ctx, arm, which) returns, for one set ("set" or "cash"),
 *                   edits    the engine's edit kinds (engine.js applyCorrections): cell shifts {side, line, key |
 *                            scenario, by: {personal, shared}} and national-scale edits {side, line, national_bn}, as
 *                            they enter the payload, after the lineage's edits;
 *                   editsAt  optional: the edits as a function of the model they apply to (item retiree_health's
 *                            national totals are the model's plus its change), so an option that moves a line's
 *                            total keeps the item's rule; without it the edits are fixed amounts and withItems stops
 *                            on an option that moves a line they edit;
 *                   parts    named parts of its cell shifts, {name: {edit, by}}, adding to them exactly (for consumers
 *                            that split the case by generation, person or household);
 *                   meta     the payload meta keys it sets; nothing else in the payload may change (gated);
 *                   record   what meta.items carries about it (factors, the source lane's own figures);
 *                   capital  optional: capital components the item adds beside the payload's, each keyed by a carrier
 *                            receipt line the item adds (item user_fees's re-keys and offsets): {carriers,
 *                            receiptLinesAt(m), the carrier lines on the model the item applies to; zeroLines(m), the
 *                            same at zero, for models without the item; componentsFor(comps, caseComps), the item's
 *                            components for a component list (an option's); checkEvaluation(ev)}. The package appends
 *                            the carriers to payload.receipt_lines and the components to meta.capital_return.components
 *                            and evaluates them with the payload's (evaluateFull, capitalReturn, componentsFor);
 *                 cash.applies says whether build() is also called for the cash set (the pension switch off).
 *       lineage   build(ctx, arm) returns the lineage's payload additions {set, cash} in the lineage lane's format, at
 *                 v5's cells in v5's order with v5's row 8 edit, counts, responses and capital values (gated), and
 *                 lineage_meta, keys added to meta.lineage. caseOf rebuilds the base from them with v5's own merge(),
 *                 adoptLineage() and forCase() on the September 29 payloads (rebase()), so the added people's edits
 *                 and production grid replace v5's in place (meta.lineage.edits keeps first 416, count 336, row 8 at
 *                 751) and every edit set builds on that base. One lineage item at a time.
 *     A change that varies with a specification field no key or scenario selects (the reading, the school response,
 *     the rate) is neither kind: it needs a meta.responses entry or a post-engine term that consumer.cjs reads, as the
 *     capital return is.
 *   - Arms are item options: caseOf(base, ids, {id: arm}) builds the case with that item at the arm (build's arm), the
 *     other items as they are, so an arm row is the whole case at the arm.
 *   - Lineage options: caseOf(base, ids, arms, name) builds the case with the lineage at another arm of the count or
 *     another C3 (lineage_count.cjs OPTIONS: arm_a, arm_c, c3_minus_se, c3_plus_se). The option's addition is v5's route
 *     at its counts, C3 and group-size responses (lineage_count.cjs, which rebuilds v5's addition exactly at v5's arm and
 *     C3); a lineage item builds on it (item added_age_mix's deltas at the option's counts, its mixes arm b's
 *     [ASSUMPTION]) and is checked against it; without one the option's addition is the base's lineage. The edit sets
 *     rebuild on that base as on item added_age_mix's. Every option is a variant.
 *   - caseOf(base, ids, arms) is the case: base a v5-style module (the set's API with CASH, SEPT29, SEPT29_CASH,
 *     ADDITION, POP and v5's exported functions), ids the items in registry order. The edit sets' edits follow the
 *     base payload's, in registry order; meta.items gives each item's place and parts. The payloads are stamped
 *     (source, adopted, decision, case, status, items): the adopted case with ADOPTED and v5's status sentence, a
 *     variant with adopted null and a status naming it a variant. With no item the case is the base's: its
 *     payloads unstamped, its API's names (LANE, HERE, DECISION, ...) the base's; generality.cjs and zero_items.cjs run
 *     v5's scripts and this lane's on it.
 *   - forItems(base, built, which) is the API of one set on a v5-style API. modelFor builds the base's model and
 *     applies the edit sets after it (withItems); evalPackage, central, payloadModel and correctionsPayload follow.
 *     With an item's capital, withSyntheticLines, componentsFor, capitalReturn, capitalMeta, evaluateFull, cost,
 *     bandFor and band carry its carriers and components too. Every other export is the base's: the specifications,
 *     the responses, the capital rules, the candidate route and the lineage (withLineage and LINEAGE_EDITS are the
 *     base's 336 lineage edits, the lineage item's when one applies; BASE stays the September 29 package).
 *     [ASSUMPTION for variants: an option leaves the fixed-amount items' edits at the case's, as it leaves the added
 *     people's amounts; withItems stops on an option that changes the national total of a line such an item edits,
 *     against the case's totals at that item's step.]
 *
 * Slots, described in SLOTS and not implemented: a lineage count population.json does not hold (its arms and other C3
 * values are lineage options), and an item that splits a line into a responding part and a part at zero response.
 *
 * Run nothing: this is a module. main_case.cjs gates it.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P5 = require(path.join(__dirname, "..", "main_case_2026_10_05", "package.cjs"));
const AGE_MIX = require(path.join(__dirname, "item_age_mix.cjs"));
const FEES = require(path.join(__dirname, "item_user_fees.cjs"));
const COUNT = require(path.join(__dirname, "lineage_count.cjs"));
const { Engine, MODEL, METHODS, mean2, span, readJson, sha256, FISCAL } = P5;

const HERE = __dirname;
const LANE = "main_case_2026_10_07";
const CASE_KEY = "oct07";
const DECISION = "decisions/2026-10-07-main-case-v6.md";
const ADOPTED = "2026-10-07";
// The adopted case's status; a variant's is "variant".
const STATUS = "adopted";
const STAMPED = ["source", "adopted", "decision", "case", "status", "items"];
const OCT05_LANE = "main_case_2026_10_05";
const OCT05_FILES = { set: `${OCT05_LANE}/derived/corrections.json`, cash: `${OCT05_LANE}/derived/corrections_cash.json`,
  summary: `${OCT05_LANE}/derived/summary.json` };
// Where main_case.cjs writes a lineage item's additions (meta.lineage.payload names them).
const LINEAGE_PAYLOADS = { set: `${LANE}/derived/lineage_payload.json`, cash: `${LANE}/derived/lineage_payload_cash.json` };
// Meta keys an edit set may not change: the package stamps the first six; the rest are the base's structure.
const RESERVED_META = ["source", "adopted", "decision", "case", "status", "items", "responses", "capital_return", "lineage",
  "builds_on", "previous", "production"];
// v5's module-level exports, beside forCase's API (main_case_2026_10_05/package.cjs, module.exports): a rebuilt base
// carries them.
const MODULE_KEYS = ["HERE", "LANE", "ADOPTED", "DECISION", "STAMPED", "LINEAGE_LANE", "COUNTING", "COUNTINGS", "LINEAGE_FILES",
  "POPULATION_FILE", "BASE_FILES", "GROUP_PATHS", "SEPT29", "SEPT29_CASH", "CASH", "CASH_PAYLOAD", "ADDITION", "POP", "forCase", "merge",
  "adoptLineage", "longRunAt", "moveLeaf", "responseDiffs", "tableOf", "sha256"];
const ALLOCS = ["personal", "shared"];
const clone = (x) => JSON.parse(JSON.stringify(x));
const blocked = (why) => { throw new Error("[BLOCKED] " + why); };
const byAlloc = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
const isNum = (x) => typeof x === "number" && Number.isFinite(x);
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const lineKey = (e) => `${e.side === "receipt" ? "receipt" : "spending"}:${e.line}`;
const nationalsOf = (m) => new Map(m.spending.lines.map((l) => [`spending:${l.id}`, l.national_bn])
  .concat(m.receipts.lines.map((l) => [`receipt:${l.id}`, l.national_bn])));
const armsOf = (d) => Object.fromEntries(Object.entries(d).map(([k, v]) => [k, { label: v.label, source_arm: v.source_arm }]));
if (MODULE_KEYS.some((k) => !(k in P5))) blocked(`v5's package lacks ${MODULE_KEYS.filter((k) => !(k in P5)).join(", ")}`);

// ---------------------------------------------------------------------------------------------------
// Item pension_tr2026: the pension accrual on the 2026 Trustees inputs, all six, on current law's separate OASI and DI
// trust funds (pension_tr2026_2026_10_06, arm all_2026_inputs_separate_funds). Its two edits are that lane's
// (case_tr2026.cjs editsFor), rebuilt on v5 and required to equal the arm's stored edits exactly, then rebuilt on the
// base the edit sets build on (the lineage item's, when one applies):
//   social_security  (ratio_net_arm - ratio_net) x the union's OASDI receipts, read on the September 29 payload's model,
//                    plus (f_ss - 1) x the added people's Social Security, f_ss being G3+'s net accrual per tax dollar at
//                    its own benefit-tax rate, arm over control;
//   medicare         part_a_arm - part_a, plus (f_pa - 1) x the added people's Part A accrual (their medicare amount in
//                    the case less (1 - part_a_share) x it in the cash set), f_pa being G3+'s Part A per HI tax dollar.
// The cash set has the pension switch off (no pension block), so no Trustees path enters it.
const PENSION = {
  lane: "pension_tr2026_2026_10_06",
  commit: "8cefec37",
  files: { summary: "pension_tr2026_2026_10_06/derived/summary.json", case: "pension_tr2026_2026_10_06/derived/case_oct05.json" },
  arm: "all_2026_inputs_separate_funds",
  base_commit: "9ea1beb",
  arms: { combined_funds: { source_arm: "all_2026_inputs",
    label: "the same 2026 inputs on the Trustees' combined OASDI funds, the convention of SSA's money's-worth notes and the Trustees' headline, which assumes a law moving funds between OASI and DI" } },
  paths: {
    reports: "the 2026 Trustees Reports: OASDI (tr2026) and HI (mtr2026), with SSA Actuarial Note 2026.3's average wage index",
    inputs: ["the payable paths, year by year from the reports' tables (OASDI: payroll tax over cost less the taxation of benefits, Tables IV.B1 and IV.B2, the depletion year with Tables IV.B4 and IV.B5; HI: non-interest income over cost, Tables III.B6 and III.B7)",
      "the tax-on-benefits path (TR 2026 Tables IV.B1 and IV.B2)", "new-issue interest rates (TR 2026 Table V.B2)",
      "the average wage index (Note 2026.3 Table 7)", "COLAs and contribution bases (TR 2026 Table V.C1)",
      "the mortality decline, 2025-2100 (TR 2026 sec. V.A)", "the HI cost per beneficiary (MTR 2026 Table V.D1)"],
    funds: "separate OASI and DI trust funds, as current law keeps them: OASI's payable share on OASI's scheduled cost and full payment on DI's, weighted by each fund's cost in the year (TR 2026 Tables IV.B1 and IV.B2) [APPROX: national cost weights stand in for each worker's mix of OASI and DI benefits]",
    level: "Note 2025.7 Table 3's money's-worth level, moved by the lifetime model's ratio of the 2026 path to the 2025 path (SSA has published no 2026 money's-worth note)",
  },
};
function pensionBasis(B, PP) {
  const REF = MODEL.receipts.reference;
  const line = (m, side, id) => { const l = m[side].lines.find((x) => x.id === id); if (!l) blocked(`no ${side} line ${id}`); return l; };
  const groupAmount = (m, id) => { const l = line(m, "spending", id); return byAlloc((a) => l.keys[l.preferred_key][a].target_bn); };
  const receiptAmount = (m, id) => byAlloc((a) => line(m, "receipts", id).cells[REF][a].target_bn);
  const oasdiOf = (m) => byAlloc((a) => PP.oasdi_lines.reduce((s, id) => s + receiptAmount(m, id)[a], 0) + PP.se_oasdi_share * receiptAmount(m, PP.se_line)[a]);
  const m4 = B.SEPT29.payloadModel(), m5 = B.payloadModel(), m4c = B.SEPT29_CASH.payloadModel(), m5c = B.CASH.payloadModel();
  for (const id of ["social_security", "medicare"]) if (line(m5, "spending", id).preferred_key !== id) blocked(`${id}'s preferred key is not ${id}`);
  const oasdi = oasdiOf(m4);
  const ss4 = groupAmount(m4, "social_security"), ss5 = groupAmount(m5, "social_security");
  const mc4 = groupAmount(m4, "medicare"), mc4c = groupAmount(m4c, "medicare"), mc5 = groupAmount(m5, "medicare"), mc5c = groupAmount(m5c, "medicare");
  const partAUnion = byAlloc((a) => mc4[a] - (1 - PP.part_a_share) * mc4c[a]);
  if (!ALLOCS.every((a) => Math.abs(ss4[a] - PP.ratio_net * oasdi[a]) <= 1e-9 && Math.abs(partAUnion[a] - PP.part_a_accrual_bn) <= 1e-9)) {
    blocked("the base's union is not priced by its pension block (social_security = ratio_net x OASDI receipts, Part A = part_a_accrual_bn)");
  }
  return { oasdi, ssLin: byAlloc((a) => ss5[a] - ss4[a]), partALin: byAlloc((a) => (mc5[a] - mc4[a]) - (1 - PP.part_a_share) * (mc5c[a] - mc4c[a])) };
}
function pensionArm(basis, S, name) {
  const ctl = S.arms.control, a = S.arms[name] || S.beside[name];
  if (!a) blocked(`the pension lane has no arm ${name}`);
  const fSS = a.g3plus_net_own_rate / ctl.g3plus_net_own_rate, fPA = a.g3plus_part_a_per_hi_tax_dollar / ctl.g3plus_part_a_per_hi_tax_dollar;
  const parts = {
    union_oasdi: byAlloc((x) => (a.ratio_net - ctl.ratio_net) * basis.oasdi[x]),
    union_part_a: byAlloc(() => a.part_a_bn - ctl.part_a_bn),
    lineage_oasdi: byAlloc((x) => (fSS - 1) * basis.ssLin[x]),
    lineage_part_a: byAlloc((x) => (fPA - 1) * basis.partALin[x]),
  };
  const edits = [
    { side: "spending", line: "social_security", key: "social_security", by: byAlloc((x) => parts.union_oasdi[x] + parts.lineage_oasdi[x]) },
    { side: "spending", line: "medicare", key: "medicare", by: byAlloc((x) => parts.union_part_a[x] + parts.lineage_part_a[x]) },
  ];
  return { a, fSS, fPA, parts, edits };
}
function buildPension(ctx, arm, which) {
  if (which !== "set") blocked("item pension_tr2026 has no cash-set edits");
  const { B, OCT05 } = ctx;
  if (arm && !PENSION.arms[arm]) blocked(`item pension_tr2026 has no arm ${arm}`);
  const name = arm ? PENSION.arms[arm].source_arm : PENSION.arm;
  const S = readJson(PENSION.files.summary), K = readJson(PENSION.files.case), S5 = readJson(OCT05_FILES.summary);
  const PP = B.correctionsPayload().meta.pension_accrual;
  if (!PP || JSON.stringify(PP) !== JSON.stringify(OCT05.correctionsPayload().meta.pension_accrual)) blocked("the base payload's pension block is not v5's");
  const ctl = S.arms.control;
  if (!(ctl.ratio_net === PP.ratio_net && ctl.part_a_bn === PP.part_a_accrual_bn && PP.source.commit === PENSION.base_commit)) {
    blocked(`the pension lane's control is not the base payload's pension block (${PENSION.base_commit})`);
  }
  if (!(Math.abs(K.case_band_bn[0] - S5.main_case[0]) <= 1e-9 && Math.abs(K.case_band_bn[1] - S5.main_case[1]) <= 1e-9
    && K.payload_pension_block.ratio_net === PP.ratio_net && K.payload_pension_block.part_a_accrual_bn === PP.part_a_accrual_bn)) {
    blocked(`${PENSION.files.case} was not run on v5 (its band or pension block differs from ${OCT05_FILES.summary}'s)`);
  }
  // On v5 the rebuilt edits are the lane's, exactly; on another lineage base only the added people's parts move.
  const basis5 = pensionBasis(OCT05, PP);
  const on5 = (n) => {
    const y = pensionArm(basis5, S, n);
    if (!K.arms[n] || JSON.stringify(y.edits) !== JSON.stringify(K.arms[n].edits)) blocked(`the rebuilt edits of arm ${n} are not ${PENSION.files.case}'s`);
    return y;
  };
  const x5 = on5(name);
  const x = B === OCT05 ? x5 : pensionArm(pensionBasis(B, PP), S, name);
  if (["union_oasdi", "union_part_a"].some((k) => JSON.stringify(x.parts[k]) !== JSON.stringify(x5.parts[k]))) blocked("the union's pension parts move with the lineage base");
  const factors = (y) => ({ f_ss: y.fSS, f_pa: y.fPA });
  const others = [[null, PENSION.arm, "the 2026 inputs on separate trust funds (the case)"]]
    .concat(Object.entries(PENSION.arms).map(([k, d]) => [k, d.source_arm, d.label])).filter(([, n]) => n !== name);
  const block = Object.assign(clone(PP), {
    ratio_net: x.a.ratio_net,
    part_a_accrual_bn: x.a.part_a_bn,
    scheduled_benefits_arm: Object.assign(clone(PP.scheduled_benefits_arm),
      { note: `${PP.scheduled_benefits_arm.note}; on the 2025 Trustees Reports (the pension lane at ${PP.source.commit}), not recomputed on the 2026 inputs` }),
    source: { file: PENSION.files.summary, commit: PENSION.commit, sha256: sha256(PENSION.files.summary), lane: PENSION.lane, arm: name,
      case_file: PENSION.files.case, case_sha256: sha256(PENSION.files.case), builds_on: clone(PP.source) },
    paths: Object.assign(clone(PENSION.paths), { construction: S.construction, depletion: S.depletion, documents: S.documents }),
    lineage_factors: Object.assign(factors(x), { rule: "the added people's Social Security accrual times f_ss and their Part A accrual times f_pa: G3+'s net accrual per tax dollar and its Part A per HI tax dollar, the arm over the 2025 control [APPROX: G3+'s ratio for both parts of their blend]" }),
    previous: { oct05: { ratio_net: PP.ratio_net, part_a_accrual_bn: PP.part_a_accrual_bn, source: clone(PP.source) } },
    arms: Object.fromEntries(others.map(([k, n, label]) => {
      const y = on5(n);
      return [k || "separate_funds", { label, source_arm: n, ratio_net: y.a.ratio_net, part_a_accrual_bn: y.a.part_a_bn, lineage_factors: factors(y) }];
    })),
  });
  const src = K.arms[name];
  return {
    edits: x.edits,
    parts: { union_oasdi: { edit: 0, by: x.parts.union_oasdi }, lineage_oasdi: { edit: 0, by: x.parts.lineage_oasdi },
      union_part_a: { edit: 1, by: x.parts.union_part_a }, lineage_part_a: { edit: 1, by: x.parts.lineage_part_a } },
    meta: { pension_accrual: block },
    record: {
      source_arm: name,
      rule: "case_tr2026.cjs editsFor(), rebuilt by package.cjs on v5 (equal to the arm's stored edits, exactly) and on the base the edit sets build on",
      parts_rule: "union_oasdi and union_part_a are the union's (the identified 39.71M); lineage_oasdi and lineage_part_a the 3.04M added people's, priced at G3+'s factors on the base's added people; each edit's by is its union part plus its lineage part",
      factors: factors(x),
      ratio_net: { oct05: PP.ratio_net, oct07: x.a.ratio_net }, part_a_accrual_bn: { oct05: PP.part_a_accrual_bn, oct07: x.a.part_a_bn },
      source_band_bn: src.band_bn, source_band_specs: src.band_specs, source_change_bn: src.band_change_bn,
      on_v5: B === OCT05 ? null : { edits: x5.edits, lineage_oasdi: x5.parts.lineage_oasdi, lineage_part_a: x5.parts.lineage_part_a,
        note: "the item's edits on v5's added people (the source lane's): the lineage parts move with the lineage item, the union parts do not" },
    },
    detail: { on_v5_edits: x5.edits },
  };
}

// ---------------------------------------------------------------------------------------------------
// Item retiree_health: retiree health on accrual, legacy at response 0 (public_pension_legacy_2026_10_07, arm central):
// state-local retiree-health pay-go swapped for the GASB 75 normal cost, federal civilian annuitants' premiums for
// OPM's normal cost, and military retirees' civilian-provider care in other_federal_benefits set to zero. Each engine
// line's national change (national.csv, from opeb_national.py) enters as a national-scale edit (engine.js scaleLine):
// the line's national total moves and every cell scales with it, so the group's share holds; the engine applies each
// line's response. Its edits are the model's national totals plus the change (case_opeb.cjs editsFor), equal to the
// lane's stored edits on v5's payload models exactly (the lineage's cell edits leave the totals alone). Both sets.
const OPEB = {
  lane: "public_pension_legacy_2026_10_07",
  commit: "96a8799b",
  files: { case: "public_pension_legacy_2026_10_07/derived/case_oct05.json", inputs: "public_pension_legacy_2026_10_07/derived/inputs.json",
    national: "public_pension_legacy_2026_10_07/derived/national.csv", by_line: "public_pension_legacy_2026_10_07/derived/by_line_oct05.csv" },
  arm: "central",
  arms: {
    mu_low: { source_arm: "mu_low", label: "mu low: all state-local OPEB over state plans 1.326 (CRR SLP 48 over Pew's 2016 gap)" },
    mu_high: { source_arm: "mu_high", label: "mu high: 2.300, symmetric about the central 1.813 [ASSUMPTION]" },
    rho_one: { source_arm: "rho_one", label: "rho = 1: state-local GASB 75 normal cost equal to employer contributions (accrual equals pay-go)" },
    rho_high: { source_arm: "rho_high", label: "rho high: 1.506, the federal military plan's normal cost over benefits paid" },
    military_low: { source_arm: "military_low", label: "military retirees' civilian-provider care at MERHCF's purchased care only, $9.7bn" },
    military_high: { source_arm: "military_high", label: "military retirees' civilian-provider care with all pre-65 care, $22.4bn" },
    no_federal: { source_arm: "no_federal", label: "state and local only: the federal civilian swap and the military care left in place" },
  },
  documents: [
    "Pew Charitable Trusts (2023), state retiree health (OPEB) liabilities, Appendix B: FY2019 GASB 75 service cost, employer contributions and interest, 48 states",
    "Reason Foundation (2021), OPEB survey: all state and local net OPEB liability, FY2019",
    "Center for Retirement Research, SLP 48 (2016): unfunded state and local OPEB, FY2013-14",
    "Financial Report of the U.S. Government FY2025, Note 13 (FY2024 column): federal civilian and military OPEB normal cost and benefits paid",
    "DoD Medicare-Eligible Retiree Health Care Fund, Audited Financial Report FY2024: purchased and total care",
    "BEA NIPA Tables 3.12 (line 26, footnote 7), 3.19, 7.8 (lines 16-17), 7.23 and 7.24",
    "pension_legacy_2026_09_30 derived/oct05/function_mix.csv: the 2024 payroll mix by function (ASPEP 2024)",
  ],
  beside: "not wired: the school key's state per-pupil prices stripped of legacy (+$0.27-0.87bn, the lane's school_beside_oct05.csv); the legacy share of benefits by state is not measured",
};
function readNational() {
  const NAT = fs.readFileSync(path.join(FISCAL, OPEB.files.national), "utf8").trim().split("\n").map((l) => l.split(","));
  const H = NAT[0];
  return NAT.slice(1).map((r) => Object.fromEntries(H.map((h, i) => [h, r[i]])));
}
function buildOpeb(ctx, arm, which) {
  const { B } = ctx;
  if (arm && !OPEB.arms[arm]) blocked(`item retiree_health has no arm ${arm}`);
  const name = arm ? OPEB.arms[arm].source_arm : OPEB.arm;
  const K = readJson(OPEB.files.case), I = readJson(OPEB.files.inputs), S5 = readJson(OCT05_FILES.summary);
  if (!(K.case_band_bn.every((x, e) => near(x, S5.main_case[e], 1e-9)) && K.cash_set_band_bn.every((x, e) => near(x, S5.cash_set.band_bn[e], 1e-9)))) {
    blocked(`${OPEB.files.case} was not run on v5 (its bands differ from ${OCT05_FILES.summary}'s)`);
  }
  if (!K.arms[name] || !I.arms[name] || I.arms[name].role !== "arm") blocked(`the retiree-health lane has no arm ${name}`);
  // case_opeb.cjs: the engine lines in national.csv's order, and each arm's change on a line summed over its plans.
  const NROWS = readNational();
  const LINES = [...new Set(NROWS.filter((r) => r.on_engine_line === "True").map((r) => r.line))];
  const delta = (id) => NROWS.filter((r) => r.arm === name && r.line === id).reduce((t, r) => t + Number(r.delta_bn), 0);
  const nat = (m, id) => { const l = m.spending.lines.find((x) => x.id === id); if (!l) blocked(`no spending line ${id}`); return l.national_bn; };
  const editsAt = (m) => LINES.map((id) => ({ side: "spending", line: id, national_bn: nat(m, id) + delta(id) }));
  const api = which === "set" ? B : B.CASH;
  const edits = editsAt(api.payloadModel());
  const stored = K.arms[name][which === "set" ? "case" : "cash"];
  if (JSON.stringify(edits) !== JSON.stringify(stored.edits)) blocked(`item retiree_health (${which}): the rebuilt edits of arm ${name} are not ${OPEB.files.case}'s`);
  const a = I.arms[name];
  const MU = { central: "central", low: "low", high: "high" }, RHO = { pew_2019: "pew_2019", one: "one", high: "high" };
  const block = {
    rule: "retiree health on accrual, legacy at response 0: state-local retiree-health pay-go replaced by the GASB 75 normal cost, federal civilian annuitants' premiums by OPM's normal cost, military retirees' civilian-provider care (other_federal_benefits, NIPA T3.12 line 26) set to zero; each line's national change spread by the 2024 payroll mix and entered as a national-scale edit (engine.js scaleLine), so the group's share of every line holds and the line's response applies",
    arm: name,
    inputs: {
      mu: I.mu[MU[a.mu]], rho: I.rho[RHO[a.rho]], military_retiree_purchased_care_bn: I.military_retiree_purchased_care_bn[a.mil],
      state_local: a.sl, federal: a.fed, swap: a.swap,
      sl_paygo_states_2024_bn: I.sl_paygo_states_2024_bn, group_health_growth_2019_2024: I.group_health_growth_2019_2024,
      pew_states_fy2019_bn: { normal_cost: I.pew_states_fy2019_bn.normal, employer_contributions: I.pew_states_fy2019_bn.employer, interest: I.pew_states_fy2019_bn.interest },
      federal_fy2024_bn: { civilian_normal_cost: I.fr_fy2024_bn.opeb_normal.civilian, civilian_paid: I.fr_fy2024_bn.opeb_paid.civilian,
        military_normal_cost: I.fr_fy2024_bn.opeb_normal.military, military_paid: I.fr_fy2024_bn.opeb_paid.military },
      merhcf_fy2024_bn: clone(I.merhcf_fy2024_bn),
    },
    national_change_bn: { total: I.national_by_arm_bn[name].delta_bn, by_line: Object.fromEntries(LINES.map((id) => [id, delta(id)])),
      normal_cost: I.national_by_arm_bn[name].normal_bn, paygo: I.national_by_arm_bn[name].paygo_bn,
      enterprises_left_off: I.national_by_arm_bn[name].enterprises_delta_bn },
    documents: OPEB.documents.slice(),
    source_hashes: clone(I.sources),
    source: { lane: OPEB.lane, commit: OPEB.commit, arm: name, files: Object.fromEntries(Object.entries(OPEB.files).map(([k, f]) => [k, { file: f, sha256: sha256(f) }])) },
    beside: OPEB.beside,
    arms: Object.fromEntries([["central", OPEB.arm, "the case"]].concat(Object.entries(OPEB.arms).map(([k, d]) => [k, d.source_arm, d.label]))
      .filter(([, n]) => n !== name).map(([k, n, label]) => [k, { label, national_change_bn: I.national_by_arm_bn[n].delta_bn }])),
  };
  return {
    edits, editsAt, parts: {}, meta: { retiree_health: block },
    record: {
      source_arm: name,
      rule: "case_opeb.cjs editsFor(): each line's national total in the model plus the arm's change (engine.js scaleLine), rebuilt by package.cjs and equal to the arm's stored edits, exactly",
      lines: LINES, national_change_bn: I.national_by_arm_bn[name].delta_bn,
      source_band_bn: stored.band_bn, source_band_specs: stored.band_specs, source_change_bn: stored.band_change_bn,
    },
    detail: { lines: LINES, delta: Object.fromEntries(LINES.map((id) => [id, delta(id)])) },
  };
}

// ---------------------------------------------------------------------------------------------------
// The registry, in edit order.
const REGISTRY = [
  { id: "pension_tr2026", kind: "edit_set",
    label: "the pension accrual on the 2026 Trustees inputs, all six, on current law's separate OASI and DI trust funds",
    source: { lane: PENSION.lane, commit: PENSION.commit, arm: PENSION.arm, files: PENSION.files },
    cash: { applies: false, why: "the cash set has the pension switch off: its payload has no pension block, so no Trustees path enters it" },
    arms: armsOf(PENSION.arms), build: buildPension },
  { id: "retiree_health", kind: "edit_set",
    label: "retiree health on accrual, legacy at response 0",
    source: { lane: OPEB.lane, commit: OPEB.commit, arm: OPEB.arm, files: OPEB.files },
    cash: { applies: true, why: "the swap moves service lines, which both sets price the same way" },
    arms: armsOf(OPEB.arms), build: buildOpeb },
  { id: "added_age_mix", kind: "lineage",
    label: "the 3.04M added people priced at their measured age mix",
    source: { lane: AGE_MIX.LANE, commit: AGE_MIX.COMMIT, reading: AGE_MIX.CENTRAL.reading, route: AGE_MIX.CENTRAL.route, files: AGE_MIX.FILES },
    cash: { applies: true, why: "the added people are in both sets" },
    arms: armsOf(AGE_MIX.ARMS), build: (ctx, arm) => AGE_MIX.build(ctx, arm) },
  { id: "user_fees", kind: "edit_set",
    label: "user fees and the education keys on the union, every part of the user-fee lane but transit",
    source: { lane: FEES.LANE, commit: FEES.COMMIT, arm: "all_but_transit", files: FEES.FILES },
    cash: { applies: true, why: "the terms move service and transfer lines and the capital keys, which both sets price the same way" },
    arms: {}, build: (ctx, arm, which) => FEES.build(ctx, arm, which) },
];
const CANDIDATE = ["pension_tr2026", "retiree_health", "added_age_mix", "user_fees"];
const SLOTS = {
  lineage_count: {
    what: "a lineage count that population.json does not hold, such as the VHB fourth-plus arm (ladder 287); population.json's arms (floor, a, b, c) and other C3 values are lineage options (lineage_count.cjs, caseOf's fourth argument, since 2026-10-07)",
    why_not_an_edit_set: "with the count move the group's share s and with it the 19 group-size responses (general government and its s, row 8's factor and edit, the long-run lines, roads, recreation's state price, the long-run property receipts) and the long-run capital values; forCase gates those as part of one addition on the September 29 payload",
    needs: [
      "the count as a population.json arm (added, g3_rate, later, population, s, k_metro), from which lineage_count.cjs builds the addition at its responses by the lineage lane's route",
      "the age mix of its parts where it is not arm b's (the age-mix lane priced arm b only; the options take arm b's mixes)",
      "the per-member divisor, meta.lineage.counts and the consumers' lineage splits from the new base, as for the options",
    ],
  },
  split_line: {
    what: "an item that splits a line into a part that responds and a part held at zero response, such as a legacy part of service costs paid for past service",
    why_not_an_edit_set: "the engine responds by line, so the zero part must be its own line; edits move amounts between cells of existing lines only",
    needs: [
      "a payload line for the zero part (payload.lines), its cells moved from the parent's key by paired shifts (-x on the parent, +x on the new line) so national totals hold",
      "its response: a meta.responses entry at 0 for the new line at both readings, which consumer.cjs and the specifications' line_responses read (no response class maps a service line to 0 by rule)",
      "the base package to accept lines and responses beyond v4's: forCase stops on both today; withSyntheticLines, PAYLOAD_LINES and PARENT carry the new line so other models evaluate and each profile holds it",
      "the lineage's edits on the parent split by the same share (followNationals splits receipt lines only), and the capital keys that read the parent's amount re-keyed or stated",
    ],
  },
};

// ---------------------------------------------------------------------------------------------------
function checkBuilt(item, x, api, which) {
  const where = `item ${item.id} (${which})`;
  if (!x || !Array.isArray(x.edits) || !x.meta || typeof x.meta !== "object") blocked(`${where}: build() returns no edits and meta`);
  for (const e of x.edits) {
    const shift = e.by !== undefined, scale = e.national_bn !== undefined;
    const fields = Object.keys(e).sort().join(",");
    if (shift === scale || !["receipt", "spending"].includes(e.side) || typeof e.line !== "string") blocked(`${where}: an edit that is not a cell shift or a national-scale edit`);
    if (shift && !(fields === (e.side === "receipt" ? "by,line,scenario,side" : "by,key,line,side") && ALLOCS.every((a) => isNum(e.by[a])) && Object.keys(e.by).length === 2)) {
      blocked(`${where}: a cell shift needs {side, line, ${e.side === "receipt" ? "scenario" : "key"}, by: {personal, shared}}`);
    }
    if (scale && !(fields === "line,national_bn,side" && isNum(e.national_bn))) blocked(`${where}: a national-scale edit needs {side, line, national_bn}`);
  }
  const m = api.payloadModel();
  if (x.capital) {
    const C = x.capital;
    if (!Array.isArray(C.carriers) || !C.carriers.length || ["receiptLinesAt", "zeroLines", "componentsFor", "checkEvaluation"].some((f) => typeof C[f] !== "function")) {
      blocked(`${where}: its capital needs carriers, receiptLinesAt, zeroLines, componentsFor and checkEvaluation`);
    }
    const rl = C.receiptLinesAt(m), zl = C.zeroLines(m), caseComps = api.componentsFor(null), comps = C.componentsFor(caseComps, caseComps);
    const ids = (ls) => JSON.stringify(ls.map((l) => l.id));
    if (ids(rl) !== JSON.stringify(C.carriers) || ids(zl) !== JSON.stringify(C.carriers) || C.carriers.some((id) => m.receipts.lines.some((l) => l.id === id))) {
      blocked(`${where}: its carriers are not new receipt lines named as it names them`);
    }
    if (zl.some((l) => Object.values(l.cells).some((c) => ALLOCS.some((a) => c[a].target_bn !== 0)))) blocked(`${where}: its zero carriers are not at zero`);
    if (!comps.length || comps.some((c) => c.key.kind !== "receipt_amount_over_national" || !C.carriers.includes(c.key.line) || !caseComps.some((t) => t.id === c.of_component)
      || caseComps.some((t) => t.id === c.id))) blocked(`${where}: its capital components are not new components keyed by its carriers beside the payload's`);
    Engine.applyCorrections(m, { receipt_lines: rl, edits: x.edits });
  } else Engine.applyCorrections(m, { edits: x.edits });
  if (x.editsAt && JSON.stringify(x.editsAt(m)) !== JSON.stringify(x.edits)) blocked(`${where}: editsAt() on the base payload's model is not its edits`);
  for (const k of Object.keys(x.meta)) if (RESERVED_META.includes(k)) blocked(`${where} changes meta.${k}, which the package stamps or the base's structure holds (see SLOTS)`);
  const sums = x.edits.map(() => byAlloc(() => 0));
  for (const [name, part] of Object.entries(x.parts || {})) {
    const e = x.edits[part.edit];
    if (!e || !e.by || !ALLOCS.every((a) => isNum(part.by[a]))) blocked(`${where}: part ${name} names no cell shift`);
    for (const a of ALLOCS) sums[part.edit][a] += part.by[a];
  }
  if (x.parts && Object.keys(x.parts).length && !x.edits.every((e, k) => !e.by || ALLOCS.every((a) => sums[k][a] === e.by[a]))) {
    blocked(`${where}: its parts do not add to its edits exactly`);
  }
  return Object.assign({ parts: {}, record: {}, detail: {} }, x);
}
// A lineage item's additions: v5's cells in v5's order, v5's row 8 edit, grid, counts, responses and capital values;
// at a lineage option (ref: the option's additions, lineage_count.cjs) the option's row 8 edit, counts, responses and
// capital values.
function checkLineage(item, x, B, ref) {
  const where = `item ${item.id}`;
  if (!x || !x.additions || !x.additions.set || !x.additions.cash || !x.lineage_meta) blocked(`${where}: build() returns no additions and lineage_meta`);
  const frame = (q) => q.edits.map((e) => [e.side, e.line, e.key, e.scenario].join("|"));
  for (const w of ["set", "cash"]) {
    const a = x.additions[w], b = (ref || B.ADDITION)[w];
    if (JSON.stringify(frame(a)) !== JSON.stringify(frame(b)) || JSON.stringify(a.edits[a.edits.length - 1]) !== JSON.stringify(b.edits[b.edits.length - 1])) {
      blocked(`${where} (${w}): the addition's cells are not v5's in v5's order with v5's row 8 edit last`);
    }
    if (!a.edits.every((e) => ALLOCS.every((al) => isNum(e.by[al])))) blocked(`${where} (${w}): an edit amount that is not a number`);
    if (JSON.stringify(a.production.dims) !== JSON.stringify(b.production.dims) || JSON.stringify(a.production.sampling_se_bn) !== JSON.stringify(b.production.sampling_se_bn)
      || ["private_wtp_bn", "induced_receipts_bn"].some((k) => a.production[k].length !== b.production[k].length || !a.production[k].every(isNum))) {
      blocked(`${where} (${w}): the addition's production grid is not v5's grid with new P and F`);
    }
    if (["builds_on", "apply", "lineage", "responses", "capital_return"].some((k) => JSON.stringify(a.meta[k]) !== JSON.stringify(b.meta[k]))) {
      blocked(`${where} (${w}): the addition moves ${ref ? "the option's" : "v5's"} counts, responses or capital values (a count or C3 change is a lineage option, lineage_count.cjs: caseOf's fourth argument)`);
    }
  }
  const clash = Object.keys(x.lineage_meta).filter((k) => k in B.LINEAGE_META || k === "payload" || k === "count_option");
  if (clash.length) blocked(`${where}: lineage_meta would overwrite meta.lineage.${clash.join(", ")}`);
  return Object.assign({ record: {}, detail: {} }, x);
}
// The base with a lineage item's additions in place of v5's: v5's merge(), adoptLineage() and forCase() on the
// September 29 payloads, as v5's module builds itself; meta.lineage names this lane's payload files and carries the
// item's keys. At a lineage option (x.option) no file holds the additions (payload null) and meta.lineage carries the
// option (count_option).
function rebase(B, x) {
  const p = B.adoptLineage(B.merge(B.SEPT29.correctionsPayload(), x.additions.set, "set"), "set");
  const pc = B.adoptLineage(B.merge(B.SEPT29_CASH.correctionsPayload(), x.additions.cash, "cash"), "cash");
  for (const [q, w] of [[p, "set"], [pc, "cash"]]) {
    q.meta.lineage = Object.assign(q.meta.lineage, { payload: x.option ? null : LINEAGE_PAYLOADS[w] }, clone(x.lineage_meta),
      x.option ? { count_option: clone(x.option.meta) } : {});
  }
  const cash = Object.assign(B.forCase(B.SEPT29_CASH, pc), { HERE: B.HERE, LANE: B.LANE });
  const mod = Object.fromEntries(MODULE_KEYS.map((k) => [k, B[k]]));
  return Object.assign(B.forCase(B.SEPT29, p), mod, { CASH: cash, CASH_PAYLOAD: clone(pc), ADDITION: clone(x.additions),
    LINEAGE_FILES: x.option ? null : clone(LINEAGE_PAYLOADS) });
}
// A lineage item's build reads only its files and the base, so each (base, item, arm, option) is built and rebased
// once; with no lineage item, a lineage option's base is its additions alone (v5's route at the option).
const LINEAGE_BASES = new WeakMap();
function lineageBase(item, B, arm, tools, opt) {
  if (!LINEAGE_BASES.has(B)) LINEAGE_BASES.set(B, new Map());
  const memo = LINEAGE_BASES.get(B), key = `${item ? item.id : ""}|${arm || ""}|${opt ? opt.name : ""}`;
  if (!memo.has(key)) {
    const built = item ? checkLineage(item, item.build(Object.assign({ B, LINEAGE_OPTION: opt }, tools), arm), B, opt ? opt.additions : null)
      : { additions: clone(opt.additions), lineage_meta: {}, record: {}, detail: {} };
    if (opt) built.option = opt;
    memo.set(key, { built, base: rebase(B, built) });
  }
  return memo.get(key);
}
const headerOf = (item) => ({ id: item.id, label: item.label, kind: item.kind, source: clone(item.source) });

// ---------------------------------------------------------------------------------------------------
// One set's API: the base's, with the edit sets applied after it, in registry order.
function forItems(base, built, which, adopted, option) {
  if (!["set", "cash"].includes(which)) blocked(`no set ${which}`);
  const p0 = base.correctionsPayload();
  const n0 = p0.edits.length;
  const steps = built.filter((b) => b.item.kind === "edit_set" && b[which]).map((b) => ({ id: b.item.id, x: b[which] }));
  const capSteps = steps.filter((s) => s.x.capital);
  const caseComps = base.componentsFor(null);
  const EDITS = [], RLINES = [], META = {}, RECORDS = [], NAT_AT = [];
  let mAt = base.payloadModel();
  for (const b of built) {
    const head = Object.assign(headerOf(b.item), { arm: b.arm || null, arms: clone(b.item.arms) });
    if (b.item.kind === "lineage") {
      RECORDS.push(Object.assign(head, { applied: true, lineage_edits: clone(base.LINEAGE_META.edits),
        production: "the added people's P and F, rebuilt with their edits", meta_changed: ["lineage"] }, clone(b.lineage.record)));
      continue;
    }
    const x = b[which];
    if (!x) { RECORDS.push(Object.assign(head, { applied: false, why: b.item.cash.why })); continue; }
    for (const [k, v] of Object.entries(x.meta)) {
      if (k in META) blocked(`items ${META[k].by} and ${b.item.id} both change meta.${k}`);
      META[k] = { by: b.item.id, value: clone(v) };
    }
    // The case's national totals where this item applies: the guard for fixed amounts under an option.
    NAT_AT.push(nationalsOf(mAt));
    const e = x.editsAt ? x.editsAt(mAt) : x.edits;
    if (JSON.stringify(e) !== JSON.stringify(x.edits)) blocked(`item ${b.item.id} (${which}): its edits move with an earlier item's`);
    const rl = x.capital ? x.capital.receiptLinesAt(mAt) : [];
    const capital = x.capital ? { receipt_lines: rl.map((l) => l.id), components: x.capital.componentsFor(caseComps, caseComps).map((c) => c.id),
      carrier_values: Object.fromEntries(rl.map((l) => [l.id, Object.fromEntries(ALLOCS.map((a) => [a, l.cells[MODEL.receipts.reference][a].share]))])),
      rule: "the carriers' amounts over their national totals, on the model at this item's step (after the earlier items), are the offsets' keys" } : null;
    RECORDS.push(Object.assign(head, { applied: true, edits: { first: n0 + EDITS.length, count: e.length },
      parts: clone(x.parts), meta_changed: Object.keys(x.meta) }, capital ? { capital } : {}, clone(x.record)));
    EDITS.push(...clone(e));
    RLINES.push(...clone(rl));
    if (e.length || rl.length) mAt = Engine.applyCorrections(mAt, { receipt_lines: rl, edits: e, meta: mAt.corrections });
  }
  const itemComps = (comps) => capSteps.flatMap((s) => s.x.capital.componentsFor(comps, caseComps));
  const COMPS = itemComps(caseComps);
  const caseText = (recs) => (recs.some((r) => r.applied)
    ? recs.filter((r) => r.applied).map((r) => `plus item ${r.id}${r.arm ? ` at arm ${r.arm}` : ""} (${r.label})`).join("; ")
    : recs.length ? `no item enters the ${which === "cash" ? "cash set" : "set"} (${recs.map((r) => `${r.id}: ${r.why}`).join("; ")})` : "no item")
    + (option ? `; the lineage at option ${option.name} (${option.label})` : "");
  // The adopted case takes v5's stamp form (adopted date, status sentence); a variant is stamped as one.
  const applied = (recs) => recs.filter((r) => r.applied).map((r) => r.id);
  const statusOf = (recs) => (!adopted
    ? `variant: not adopted; a variant of main case v6 (adopted ${ADOPTED}, ${DECISION}): ${caseText(recs)}`
    : which === "set"
      ? `adopted ${ADOPTED} (${DECISION}): v5 plus items ${applied(recs).join(", ")}, built by ${LANE}/package.cjs on ${OCT05_FILES.set}`
      : `the cash set of the case adopted ${ADOPTED} (the pension switch off): ${OCT05_FILES.cash} plus items ${applied(recs).join(", ")}, built by ${LANE}/package.cjs`);
  function stamped(p, recs, edits, rlines, comps) {
    p.edits = p.edits.concat(clone(edits));
    if (rlines.length) p.receipt_lines = (p.receipt_lines || []).concat(clone(rlines));
    if (comps.length) p.meta.capital_return.components = p.meta.capital_return.components.concat(clone(comps));
    for (const [k, v] of Object.entries(META)) p.meta[k] = clone(v.value);
    p.meta.source = `${LANE}/package.cjs`;
    p.meta.adopted = adopted ? ADOPTED : null;
    p.meta.decision = DECISION;
    p.meta.case = `${p.meta.case}; ${adopted ? `v6, adopted ${ADOPTED}` : `a variant of v6 (adopted ${ADOPTED}), not the adopted case`}: ${caseText(recs)}`;
    p.meta.status = statusOf(recs);
    p.meta.items = recs;
    return p;
  }
  const payload = built.length || option ? stamped(clone(p0), clone(RECORDS), EDITS, RLINES, COMPS) : clone(p0);
  function pensionGuard(oo) {
    if (steps.length && oo && oo.pension4 !== undefined && oo.pension4 !== base.ITEMS.pension4) {
      blocked(`the items here are priced with the pension switch ${base.ITEMS.pension4}; with ${oo.pension4} use that set's case (P.CASH)`);
    }
  }
  // A model that carries an item's carriers at zero (withSyntheticLines) takes them out before the item applies; one
  // that carries them with amounts has the item already.
  function withoutZeroCarriers(m, C) {
    const have = m.receipts.lines.filter((l) => C.carriers.includes(l.id));
    if (!have.length) return m;
    if (have.some((l) => Object.values(l.cells).some((c) => ALLOCS.some((a) => c[a].target_bn !== 0)))) blocked(`the model carries ${have.map((l) => l.id).join(", ")} already: the item is applied`);
    return Object.assign({}, m, { receipts: Object.assign({}, m.receipts, { lines: m.receipts.lines.filter((l) => !C.carriers.includes(l.id)) }) });
  }
  // Fixed-amount edits have no rule for an option that moves a line's national total (against the case's totals where
  // the item applies); editsAt items and the carriers follow the model.
  function applySteps(m, what) {
    let out = m;
    const all = [], rls = [];
    steps.forEach((s, k) => {
      if (!s.x.editsAt) {
        const N = nationalsOf(out), moved = [...new Set(s.x.edits.map(lineKey))].filter((key) => N.get(key) !== NAT_AT[k].get(key));
        if (moved.length) blocked(`${what} changes the national total of ${moved.join(", ")}, which item ${s.id} edits by fixed amounts; the item has no rule for it`);
      }
      const e = s.x.editsAt ? s.x.editsAt(out) : s.x.edits;
      let rl = [];
      if (s.x.capital) { out = withoutZeroCarriers(out, s.x.capital); rl = s.x.capital.receiptLinesAt(out); }
      all.push(...clone(e));
      rls.push(...clone(rl));
      if (e.length || rl.length) out = Engine.applyCorrections(out, { receipt_lines: rl, edits: e, meta: out.corrections });
    });
    return { out, all, rls };
  }
  function withItems(m, oo) {
    if (!steps.length) return m;
    pensionGuard(oo);
    const { out } = applySteps(m, "the model");
    if (!("corrections" in m)) delete out.corrections;
    return out;
  }
  const modelFor = (caseName, method, oo) => withItems(base.modelFor(caseName, method, oo), oo);
  const payloadModel = () => Engine.applyCorrections(MODEL, payload);
  // The payload itself, or, with options, the base's payload of that variant with the edit sets after it.
  function correctionsPayload(o) {
    if (!o || !Object.keys(o).length) return clone(payload);
    const p = base.correctionsPayload(o);
    if (!built.length) return p;
    pensionGuard(base.withCentral(o));
    const { all, rls } = applySteps(Engine.applyCorrections(MODEL, p), "the option");
    const recs = clone(RECORDS).map((r) => Object.assign(r, r.edits ? { edits: { first: r.edits.first - n0 + p.edits.length, count: r.edits.count } } : {},
      { note: "the item at the case's options (package.cjs withItems)" }));
    return stamped(p, recs, all, rls, itemComps(p.meta.capital_return.components));
  }
  const api = { modelFor, payloadModel, correctionsPayload, withItems, ITEM_EDITS: clone(EDITS), CASE_ITEMS: clone(RECORDS) };
  if (!capSteps.length) {
    function evalPackage(caseName, method, o) {
      const oo = base.withCentral(o);
      return base.bandFor(modelFor(caseName, method, oo), oo.profile, base.specsFor(oo));
    }
    const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
    return Object.assign({}, base, api, { evalPackage, central, ITEM_RECEIPT_LINES: [], ITEM_COMPONENTS: [] });
  }

  // The items' capital: their carriers on every model (at zero where the item is not applied), their components
  // evaluated after the payload's, in the payload's order.
  const ZERO = capSteps.flatMap((s) => s.x.capital.zeroLines(MODEL));
  const synth = new WeakMap();
  function withSyntheticLines(m0) {
    const m = base.withSyntheticLines(m0);
    const missing = ZERO.filter((l) => !m.receipts.lines.some((x) => x.id === l.id));
    if (!missing.length) return m;
    if (!synth.has(m)) synth.set(m, Engine.applyCorrections(m, { receipt_lines: missing, edits: [], meta: m.corrections }));
    return synth.get(m);
  }
  const compsMemo = new Map();
  const itemCompsFor = (variant) => {
    const k = variant || "";
    if (!compsMemo.has(k)) compsMemo.set(k, itemComps(base.componentsFor(variant)));
    return compsMemo.get(k);
  };
  const componentsFor = (variant) => base.componentsFor(variant).concat(itemCompsFor(variant));
  function withItemCapital(evaluation, spec, cap) {
    if (!spec.rate) return cap;
    for (const s of capSteps) s.x.capital.checkEvaluation(evaluation);
    const extra = itemCompsFor(spec.capital_variant).map((c) => {
      const key = base.keyOf(evaluation, c.key), response = base.responseOfRule(evaluation, spec, c.response);
      return { id: c.id, group: c.part, level: c.level, stock_charged_bn: c.stock_charged_bn, key, response, return_bn: c.stock_charged_bn * spec.rate * key * response };
    });
    return { components: cap.components.concat(extra), total_bn: extra.reduce((a, c) => a + c.return_bn, cap.total_bn) };
  }
  const capitalReturn = (evaluation, spec) => withItemCapital(evaluation, spec, base.capitalReturn(evaluation, spec));
  function capitalMeta(oo) {
    const K = base.capitalMeta(oo);
    return Object.assign(K, { components: K.components.concat(clone(itemCompsFor(oo.capital_variant))) });
  }
  function evaluateFull(m0, spec, profile) {
    const r = base.evaluateFull(withSyntheticLines(m0), spec, profile);
    const capital = withItemCapital(r.evaluation, spec, r.capital);
    if (capital === r.capital) return r;
    const direct = r.cost_bn === -r.evaluation.welfare_bn + r.capital.total_bn;
    return { evaluation: r.evaluation, capital, cost_bn: direct ? -r.evaluation.welfare_bn + capital.total_bn : r.cost_bn + (capital.total_bn - r.capital.total_bn) };
  }
  // The item variants' route (candidate v4's evaluateFull) with the items' capital after it, as evaluateFull adds it.
  function viaCandidate(m0, spec, profile) {
    const r = base.viaCandidate(withSyntheticLines(m0), spec, profile);
    const capital = withItemCapital(r.evaluation, spec, r.capital);
    return capital === r.capital ? r : { evaluation: r.evaluation, capital, cost_bn: r.cost_bn + (capital.total_bn - r.capital.total_bn) };
  }
  const cost = (m, spec, profile) => evaluateFull(m, spec, profile).cost_bn;
  const bandFor = (m, profile, specs) => span(specs.map((spec) => cost(m, spec, profile)));
  function evalPackage(caseName, method, o) {
    const oo = base.withCentral(o);
    return bandFor(modelFor(caseName, method, oo), oo.profile, base.specsFor(oo));
  }
  const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
  const band = (m, profile) => bandFor(m, profile, base.MAIN_SPECS);
  return Object.assign({}, base, api, { evalPackage, central, withSyntheticLines, componentsFor, capitalReturn, capitalMeta, evaluateFull, viaCandidate, cost,
    bandFor, band, ITEM_RECEIPT_LINES: clone(RLINES), ITEM_COMPONENTS: clone(COMPS) });
}

// The case: the set's API with its cash set's, on a v5-style base module; lineage, optional, names a lineage option
// (lineage_count.cjs OPTIONS: another arm of the count or another C3), with or without the lineage item.
function caseOf(B, ids, sel, lineage) {
  const arms = Object.assign({}, sel || {});
  const order = ids.map((id) => REGISTRY.findIndex((x) => x.id === id));
  if (order.some((k) => k < 0)) blocked(`no item ${ids[order.indexOf(-1)]} in the registry (${REGISTRY.map((x) => x.id).join(", ")})`);
  if (order.some((k, i) => i > 0 && k <= order[i - 1])) blocked("items must be named once each, in registry order");
  for (const [id, arm] of Object.entries(arms)) {
    const it = REGISTRY.find((x) => x.id === id);
    if (!ids.includes(id) || !it || !it.arms[arm]) blocked(`no arm ${arm} of an item ${id} in this case`);
  }
  const items = order.map((k) => REGISTRY[k]);
  const lin = items.filter((it) => it.kind === "lineage");
  if (lin.length > 1) blocked("one lineage item at a time: two would need one addition built for both");
  const tools = { OCT05: B, Engine, MODEL, METHODS, readJson, sha256 };
  const opt = lineage ? COUNT.optionOf(B, lineage, tools) : null;
  let L = B, linBuilt = null;
  if (lin.length) ({ built: linBuilt, base: L } = lineageBase(lin[0], B, arms[lin[0].id] || null, tools, opt));
  else if (opt) ({ base: L } = lineageBase(null, B, null, tools, opt));
  const ctx = Object.assign({ B: L, LINEAGE_ITEM: lin.length ? lin[0].id : null }, tools);
  const built = items.map((item) => {
    const arm = arms[item.id] || null;
    if (item.kind === "lineage") return { item, arm, lineage: linBuilt };
    return { item, arm, set: checkBuilt(item, item.build(ctx, arm, "set"), L, "set"),
      cash: item.cash.applies ? checkBuilt(item, item.build(ctx, arm, "cash"), L.CASH, "cash") : null };
  });
  // The adopted case: v5's module with every registry item of CANDIDATE, in order, no arm and no lineage option. A
  // lineage option is a variant with or without items.
  const adopted = B === P5 && JSON.stringify(ids) === JSON.stringify(CANDIDATE) && !Object.keys(arms).length && !opt;
  const stampIt = built.length > 0 || !!opt;
  const ident = stampIt ? { HERE, LANE, ADOPTED: adopted ? ADOPTED : null, DECISION, STATUS: adopted ? STATUS : "variant", STAMPED, CASE_KEY } : {};
  const set = Object.assign(forItems(L, built, "set", adopted, opt), ident);
  const cash = Object.assign(forItems(L.CASH, built, "cash", adopted, opt), stampIt ? { HERE, LANE } : {});
  const detail = Object.fromEntries(built.map((b) => [b.item.id, b.item.kind === "lineage" ? b.lineage.detail
    : { set: b.set.detail, cash: b.cash ? b.cash.detail : null }]));
  return Object.assign(set, { CASH: cash, CASH_PAYLOAD: cash.correctionsPayload(), OCT05: B, OCT05_CASH: B.CASH, OCT05_FILES, ITEM_BASE: L,
    ITEM_IDS: built.map((b) => b.item.id), ITEM_ARMS: arms, LINEAGE_ITEM: lin.length ? lin[0].id : null, ITEM_DETAIL: detail,
    LINEAGE_OPTION: opt ? opt.name : null, LINEAGE_OPTION_META: opt ? clone(opt.meta) : null });
}

const CASE = caseOf(P5, CANDIDATE);
module.exports = Object.assign(CASE, {
  V6: { LANE, CASE_KEY, DECISION, ADOPTED, STATUS, STAMPED, HERE }, REGISTRY, CANDIDATE, SLOTS, PENSION, OPEB, AGE_MIX, FEES, RESERVED_META, LINEAGE_PAYLOADS,
  COUNT, LINEAGE_OPTIONS: COUNT.OPTIONS,
  forItems, caseOf, rebase, checkBuilt, checkLineage,
});
