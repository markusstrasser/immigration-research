/* The main case adopted on 2026-09-24, run once through the explorer engine.
 *
 * Base: main_case_2026_09_23 (profile cbo_category_lag_non_school_full, 64 specifications; the low end
 * is the shared allocation, the high end the personal one), reproduced to 1e-4 before any change.
 *
 * Adopted by the operator on 2026-09-24 (decisions/2026-09-24-main-case-audit-and-outside-checks.md):
 *   1  the dataset audit as one package (dataset_integrity_2026_09_23), its row 6 run through the engine
 *      and its row 3 replaced by CBO's income-tax gradient;
 *   2  the pooled-MEPS medical figure jointly with the long-term-care carve-out, in place of audit row 5;
 *   3  care and household services (care_household_services_2026_09_23);
 *   5  migrant-shelter keying (migrant_shelter_costs_2026_09_23);
 *   6  the outside checks of 2026-09-24: schools priced where the group enrolls, CBO's income gradients,
 *      Treasury's EITC shares, benefit keys from administrative records and the booking correction.
 * Beside the account and not in these figures: the debt legacy (decision 4), victims' harm, audit
 * rows 11 and 12.
 *
 * How each change enters. Every model edit conserves national totals (other_bn moves the other way).
 * - Tax block: the CPS imputation lane's stack of audit rows 2, 13 and 4 and the state-aware status
 *   flag, as line deltas (derived/stack_line_deltas.json, a vendored subset of that lane's
 *   _cache/onbooks_lane_line_deltas.json; drift-checked whenever the cache is present). Central: the
 *   mean of the two fill-in methods at the on-books lane's central share. Range: the six case x method
 *   stacks. Audit row 3 is not in the stack; CBO's income-tax gradient replaces it.
 * - Frame: this script uses combine.cjs's overrides (justice "use", Medicaid uninsured_use_low/high).
 *   The CPS and long-term-care lanes translated on preferred keys plus the adopted justice and
 *   uncompensated-care shifts, so a shift on medicaid/medicaid also moves both uninsured-use keys, and
 *   the stack's public_order_safety/population shift (the use key's per-head part, scaled by the CPS
 *   lane) moves the use key. Gate: each stack alone reproduces the CPS lane's published change.
 * - Ratio-type changes rescale the group's key dollars on a line: CBO's gradients, the benefit keys,
 *   the medical-ethnicity ratios, the school price and re-blend. On top of the stack each is multiplied
 *   by its key's stack factor (the group's target after the stack over the target before).
 * - Replacement-type changes set the group's charge on named dollars: the long-term-care carve-out (the
 *   stack's change on those dollars is removed), premium tax credits (the stack already leaves them
 *   alone) and Treasury's EITC share (measured against the audit's SSN rule).
 * - Overlaps: CBO's income-tax gradient replaces audit row 3; the benefit keys replace CBO on SNAP, WIC
 *   and cash assistance; the medical-ethnicity ratios replace CBO's Medicare gradient; the booking
 *   factor multiplies audit row 7's 2024 arrest ratio.
 * - Lane figures with no line in common with any other change enter as one synthetic line at
 *   response 1: audit rows 8, 9 and 10 and its small items, shelter, care.
 * - Ranges: the tax block's six stacks and each other component's variants, summed as independent
 *   bounds at each band end, as dataset_integrity_2026_09_23/synthesis.py sums the audit's rows.
 *
 * Gates (exit 1 on failure): the adopted case reproduces; every component alone reproduces its lane.
 * Run from anywhere: node main_case.cjs  ->  derived/main_case_bands.csv, components.csv, summary.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const MODEL = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const scaling = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "scaling_check.json"), "utf8"));
const read = (rel) => fs.readFileSync(path.join(FISCAL, rel), "utf8");
const readJson = (rel) => JSON.parse(read(rel));
const ALLOCS = ["personal", "shared"];

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
const near = (a, b, tol) => Math.abs(a - b) < tol;
const span = (xs) => [Math.min(...xs), Math.max(...xs)];
const f2 = (b) => `${b[0].toFixed(3)} / ${b[1].toFixed(3)}`;
function product(dims) {
  return Object.entries(dims).reduce(
    (acc, [name, levels]) => acc.flatMap((spec) => levels.map((v) => ({ ...spec, [name]: v }))), [{}]);
}
function csvRows(rel) {
  const [head, ...rows] = read(rel).trim().split("\n");
  const keys = head.split(",");
  return rows.map((r) => {
    const cells = r.match(/("([^"]|"")*"|[^,]*)(,|$)/g).map((c) => c.replace(/,$/, "").replace(/^"|"$/g, ""));
    return Object.fromEntries(keys.map((k, i) => [k, cells[i]]));
  });
}
const both = (v) => ({ personal: v, shared: v });

// ---------------------------------------------------------------------------------------------------
// The adopted frame (outside_checks_combined_2026_09_24/combine.cjs), plus two synthetic lines for the
// school lane's re-keyed steps and one for lane constants.
const SHARES = Engine.schoolShareBounds(MODEL);
const GG = [scaling.composite_low, scaling.composite_high];
const MAIN_SPECS = product({
  allocation: ["personal", "shared"], normalization: ["cash", "gdp"], share: SHARES,
  school: [0.63, 0.66], gg: GG, uc: ["uninsured_use_low", "uninsured_use_high"], justice: ["use"],
});
const SYN = { school: "school_reprice", college: "college_rekey", constants: "lane_constants" };
function cost(m, spec) {
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = m.receipts.reference;
  s.production.normalization = spec.normalization;
  s.count_production = true;
  s.general_government_response = spec.gg;
  s.key_override = { public_order_safety: spec.justice, medicaid_and_chip_other_medical: spec.uc };
  s.response_override = {
    education_services: spec.share * spec.school + (1 - spec.share) * 1,
    public_order_safety: 1, health_services: 1, income_security_services: 1,
    housing_community_services: 1, economic_affairs_services: 0, recreation_culture: 0,
    [SYN.school]: spec.share * spec.school, [SYN.college]: (1 - spec.share) * 1, [SYN.constants]: 1,
  };
  return -Engine.evaluate(m, s).welfare_bn;
}
const band = (m) => span(MAIN_SPECS.map((spec) => cost(m, spec)));

// A change is a list of shifts {side: "receipt" | "spending", line, key, by: {personal, shared}}.
const MEDICAID = "medicaid_and_chip_other_medical";
const MEDICAID_KEYS = ["medicaid", "uninsured_use_low", "uninsured_use_high"];
function build(shifts) {
  const m = JSON.parse(JSON.stringify(MODEL));
  const cell = () => ({ target_bn: 0, other_bn: 0, share: 0 });
  for (const id of Object.values(SYN)) {
    m.spending.lines.push({ id, family: "consumption", national_bn: 0, response_class: id,
      preferred_key: "k", alternative_key: "k", keys: { k: { personal: cell(), shared: cell() } } });
  }
  for (const s of shifts) {
    let cells;
    if (s.side === "receipt") {
      const line = m.receipts.lines.find((l) => l.id === s.line);
      if (!line) throw new Error("no receipt line " + s.line);
      cells = [line.cells[m.receipts.reference]];
    } else {
      const line = m.spending.lines.find((l) => l.id === s.line);
      if (!line) throw new Error("no spending line " + s.line);
      const keys = s.line === MEDICAID && s.key === "medicaid" ? MEDICAID_KEYS : [s.key || line.preferred_key];
      cells = keys.map((k) => { if (!line.keys[k]) throw new Error(`no key ${s.line}/${k}`); return line.keys[k]; });
    }
    for (const c of cells) for (const a of ALLOCS) { c[a].target_bn += s.by[a]; c[a].other_bn -= s.by[a]; }
  }
  return m;
}
const scale = (by, f) => ({ personal: by.personal * f.personal, shared: by.shared * f.shared });
const plus = (a, b) => ({ personal: a.personal + b.personal, shared: a.shared + b.shared });

// ---------------------------------------------------------------------------------------------------
// Tax block: the CPS lane's stacks, vendored with a drift check.
const CPS_CACHE = path.join(FISCAL, "cps_imputation_keys_2026_09_23", "_cache", "onbooks_lane_line_deltas.json");
const STACK_FILE = path.join(HERE, "derived", "stack_line_deltas.json");
const CASES = ["low", "central", "high"];
const METHODS = ["b_hotdeck_union_matched", "b_matched_over_pooled"];
const STACK_KEYS = CASES.flatMap((c) => METHODS.flatMap((m) =>
  ["row4+status_state_aware", "row3", "medicare_key_fix"].map((arm) => `${arm}|${c}|${m}`))
  .concat([`row4+status_state_aware|${c}|audit_rules_alone`]));  // the audit's rules without a fill-in method
if (fs.existsSync(CPS_CACHE)) {
  const raw = fs.readFileSync(CPS_CACHE);
  const src = JSON.parse(raw);
  const subset = { source: path.relative(FISCAL, CPS_CACHE), source_sha256: crypto.createHash("sha256").update(raw).digest("hex"),
    payloads: Object.fromEntries(STACK_KEYS.map((k) => { if (!src[k]) throw new Error("[BLOCKED] missing stack " + k); return [k, src[k]]; })) };
  if (fs.existsSync(STACK_FILE)) {
    const old = JSON.parse(fs.readFileSync(STACK_FILE, "utf8"));
    const drift = JSON.stringify(old.payloads) !== JSON.stringify(subset.payloads);
    if (drift) console.log("[stack] the CPS lane's cache changed since the vendored copy; rewriting it");
  }
  fs.mkdirSync(path.dirname(STACK_FILE), { recursive: true });
  fs.writeFileSync(STACK_FILE, JSON.stringify(subset, null, 1) + "\n");
} else if (!fs.existsSync(STACK_FILE)) {
  throw new Error("[BLOCKED] no stack line deltas: run cps_imputation_keys_2026_09_23/combine_onbooks_lane.py");
} else {
  console.log("[stack] CPS lane cache absent; using the vendored copy " + path.relative(FISCAL, STACK_FILE));
}
const STACKS = JSON.parse(fs.readFileSync(STACK_FILE, "utf8")).payloads;

function stackShifts(p) {
  const out = [];
  for (const [line, by] of Object.entries(p.receipts || {})) out.push({ side: "receipt", line, by });
  for (const [line, byKey] of Object.entries(p.spending || {})) {
    for (const [key, by] of Object.entries(byKey)) {
      out.push({ side: "spending", line, key, by });
      // The CPS lane scaled this shift to the per-head part of the justice use key.
      if (line === "public_order_safety" && key === "population") out.push({ side: "spending", line, key: "use", by });
    }
  }
  return out;
}
// The group's target on a key after the stack over before (1 where the stack does not touch it).
function stackFactor(p, side, line, key) {
  const f = {};
  for (const a of ALLOCS) {
    let t0, d = 0;
    if (side === "receipt") {
      t0 = MODEL.receipts.lines.find((l) => l.id === line).cells[MODEL.receipts.reference][a].target_bn;
      if (p && p.receipts && p.receipts[line]) d = p.receipts[line][a];
    } else {
      const l = MODEL.spending.lines.find((x) => x.id === line);
      t0 = l.keys[key || l.preferred_key][a].target_bn;
      if (p && p.spending && p.spending[line] && p.spending[line][key || l.preferred_key]) d = p.spending[line][key || l.preferred_key][a];
    }
    f[a] = t0 === 0 ? 1 : (t0 + d) / t0;
  }
  return f;
}

// ---------------------------------------------------------------------------------------------------
// Lane inputs.
const cboAll = readJson("external_benchmarks_2026_09_24/derived/cbo_deltas.json");
const ota = readJson("external_benchmarks_2026_09_24/derived/ota_deltas.json");
const benefitsAll = readJson("admin_benefit_keys_2026_09_24/derived/line_deltas.json").deltas;
const benefitSe = csvRows("admin_benefit_keys_2026_09_24/derived/package_se.csv").filter((r) => r.package === "central");
const mts = readJson("dataset_integrity_2026_09_23/derived/spending_mts_credits.json");
const schoolV = readJson("school_cost_where_enrolled_2026_09_24/derived/school_key_variants.json");
const schoolLines = csvRows("school_cost_where_enrolled_2026_09_24/derived/engine_school_lines.csv");
const medTrans = csvRows("medical_ethnicity_pooled_2026_09_23/derived/translation_account.csv");
const ltssComb = csvRows("ltss_share_2026_09_23/derived/combined.csv");
const ltssEffects = csvRows("ltss_share_2026_09_23/derived/effects.csv");
const ltssMain = csvRows("ltss_share_2026_09_23/derived/main_case_effect.csv");
const mcbs = JSON.parse(fs.readFileSync(path.join(HERE, "derived", "mcbs_bound.json"), "utf8"));
const crimeRows = csvRows("crime_ratio_direction_2026_09_24/derived/dollar_effects.csv");
const shelterRows = csvRows("migrant_shelter_costs_2026_09_23/derived/account_keying.csv");

// CBO's bundle, all concepts but Medicaid. Skipped lines are re-keyed by a more direct measurement.
const CBO_SKIP = ["snap", "other_state_welfare", "family_and_general_assistance", "medicare"];
function cboShifts(year, p, opts) {
  const o = Object.assign({ skip: CBO_SKIP, scaled: true, incomeTax: true }, opts || {});
  const b = cboAll[`all_but_medicaid|${year}`];
  if (!b) throw new Error("no CBO bundle for " + year);
  const out = [];
  for (const [line, by] of Object.entries(b.receipts)) {
    if (!o.incomeTax && line === "federal_income_tax") continue;
    out.push({ side: "receipt", line, by: o.scaled ? scale(by, stackFactor(p, "receipt", line)) : by });
  }
  for (const [line, byKey] of Object.entries(b.spending)) {
    if (o.skip.includes(line)) continue;
    for (const [key, by] of Object.entries(byKey)) {
      out.push({ side: "spending", line, key, by: o.scaled ? scale(by, stackFactor(p, "spending", line, key)) : by });
    }
  }
  return out;
}
// Audit row 3 as that audit measured it on top of the stack (for comparison only).
function row3Shifts(caseName, method) {
  const a = STACKS[`row3|${caseName}|${method}`].receipts.federal_income_tax;
  const b = STACKS[`medicare_key_fix|${caseName}|${method}`].receipts.federal_income_tax;
  return [{ side: "receipt", line: "federal_income_tax", by: { personal: a.personal - b.personal, shared: a.shared - b.shared } }];
}

// Treasury's EITC shares.
const otaShifts = (variant) => Object.entries(ota[variant].spending).flatMap(([line, byKey]) =>
  Object.entries(byKey).map(([key, by]) => ({ side: "spending", line, key, by })));

// Audit row 1: premium tax credits re-keyed by marketplace persons (Treasury MTS).
const row1Shifts = () => [{ side: "spending", line: "refundable_tax_credits", key: "refundable_credits", by: both(mts.ptc_effect_on_main_case_bn) }];

// Decision 2: the medical-ethnicity ratios on the community remainder, the long-term-care carve-out.
const MED_LINES = ["medicare", "health_services", "military_medical", "veterans_other"];
const LTSS_CENTRAL = Number(ltssEffects.find((r) => r.variant === "central").total);
const LTSS_RANGE = [-12.5, -8.1];  // extremes of the lane's 960 combinations (ltss_share_2026_09_23 RESULT)
function medicalShifts(p, spec, opts) {
  const o = Object.assign({ mcbs: null, ltss: LTSS_CENTRAL }, opts || {});
  const rows = medTrans.filter((r) => r.spec === spec);
  const comb = ltssComb.find((r) => r.spec === spec);
  if (!rows.length || !comb) throw new Error("no medical spec " + spec);
  const d = Object.fromEntries(rows.map((r) => [r.line, Number(r.delta_bn)]));
  let medicaidEth = d[MEDICAID];
  const ltssFrac = -Number(comb.remainder_ratio_adjustment_bn) / medicaidEth;  // LTSS share of the group's keyed Medicaid
  if (o.mcbs) {
    if (spec !== mcbs.spec) throw new Error("the MCBS bound is computed at " + mcbs.spec);
    d.medicare = mcbs.cases[o.mcbs].medicare;
    medicaidEth = mcbs.cases[o.mcbs][MEDICAID];
  }
  const fMed = stackFactor(p, "spending", MEDICAID, "medicaid");
  const stackMed = p && p.spending && p.spending[MEDICAID] && p.spending[MEDICAID].medicaid ? p.spending[MEDICAID].medicaid : both(0);
  const ratioPart = medicaidEth * (1 - ltssFrac);
  const medicaid = {};
  for (const a of ALLOCS) medicaid[a] = ratioPart * fMed[a] + o.ltss - stackMed[a] * ltssFrac;
  const out = [{ side: "spending", line: MEDICAID, key: "medicaid", by: medicaid }];
  for (const line of MED_LINES) {
    const key = MODEL.spending.lines.find((l) => l.id === line).preferred_key;
    out.push({ side: "spending", line, key, by: scale(both(d[line]), stackFactor(p, "spending", line, key)) });
  }
  return out;
}

// Education: audit row 6's re-blend on the whole line with the school lane's price k on the school step.
const EDU = MODEL.spending.lines.find((l) => l.id === "education_services");
const eduT0 = { personal: EDU.keys.education_mix.personal.target_bn, shared: EDU.keys.education_mix.shared.target_bn };
const minusT0 = (t) => ({ personal: t.personal - eduT0.personal, shared: t.shared - eduT0.shared });
function educationShifts(p, w, k) {
  const f = stackFactor(p, "spending", "education_services", "education_mix");
  const school = minusT0(schoolV[`row6_w${w}|${k}`].school_target_bn);
  const college = minusT0(schoolV[`row6_w${w}_whole_line`].college_target_bn);
  return [{ side: "spending", line: SYN.school, key: "k", by: scale(school, f) },
    { side: "spending", line: SYN.college, key: "k", by: scale(college, f) }];
}

// Benefit keys from administrative records (ratio-type: a factor on the key's union share).
function benefitShifts(p, pkg) {
  return Object.entries(benefitsAll[pkg || "package_central"]).map(([line, by]) =>
    ({ side: "spending", line, key: null, by: scale(by, stackFactor(p, "spending", line, null)) }));
}

// Justice: audit row 7 (2024 arrests) and the booking factor on the updated ratio.
const RR_2019 = 1.145, SLOPE = 2.75 / 0.145;  // crime.md #1: -$2.75bn per -0.145 of RR, linear
const ROW7 = { "2024": 1.12, "2023": 1.34 };
const bookingRow = (label) => {
  const r = crimeRows.find((x) => x.method === label);
  if (!r) throw new Error("no booking row " + label);
  return Number(r.delta_main_case_bn);
};
const BOOKING = { central: "RR x 1.0401 (all ages, all five offences, TX+AZ NIBRS)",
  texas: "RR x 1.0439 (Texas only, TX+AZ NIBRS)", arizona: "RR x 1.0003 (Arizona only, TX+AZ NIBRS)" };
function justiceShifts(row7Year, booking) {
  const row7 = row7Year ? ROW7[row7Year] : 0;
  const rr = RR_2019 + row7 / SLOPE;
  const b = booking ? bookingRow(BOOKING[booking]) * rr / RR_2019 : 0;
  return [{ side: "spending", line: "public_order_safety", key: "use", by: both(row7 + b) }];
}

// Lane figures with no line in common with any other change (one synthetic line at response 1).
const shelterCentral = (gg) => shelterRows.filter((r) => r.outlays_case === "central" && r.mapping === "A_nyc_codes_consumption"
  && r.served_case === "nyc_jun2025" && Math.abs(Number(r.general_govt_response) - gg) < 1e-9)
  .map((r) => -Number(r.overcharge_musd) / 1000);
const CONSTANTS = {
  row8: { label: "audit row 8: unallocable S&L spending at the all-spending elasticity", c: 2.0, lo: 2.0, hi: 2.0 },
  row9: { label: "audit row 9: MEPS donor filter (non-LTSS remainder)", c: -0.8, lo: -1.6, hi: 0.0 },
  row10: { label: "audit row 10: foster care keyed by WIC", c: -1.5, lo: -2.0, hi: -1.0 },
  small: { label: "audit small items (origin allocation, grants, top-codes, flags)", c: -0.1, lo: -0.5, hi: 0.4 },
  shelter: { label: "shelter keying (mapping A, central outlays, NYC June 2025 share)", c: null, lo: -0.839, hi: -0.445 },
  care: { label: "care and household services (hours taxes, elder-care Medicaid, output)", c: -4.15, lo: -13.35, hi: -2.60 },
};
const [shelterLow] = shelterCentral(0.59), [shelterHigh] = shelterCentral(0.84);
if (!(shelterLow < -0.4 && shelterHigh < -0.4)) throw new Error("shelter rows not found");
function constantShifts(overrides) {
  const v = {};
  for (const [id, c] of Object.entries(CONSTANTS)) {
    const pick = (overrides && overrides[id]) || "c";
    v[id] = id === "shelter" && pick === "c" ? { shared: shelterLow, personal: shelterHigh } : both(c[pick]);
  }
  const by = Object.values(v).reduce(plus, both(0));
  return [{ side: "spending", line: SYN.constants, key: "k", by }];
}

// ---------------------------------------------------------------------------------------------------
// The package.
const CENTRAL = { year: 2022, scaled: true, medSpec: "winsor_p995", mcbs: null, ltss: LTSS_CENTRAL, w: "avg", k: "preferred",
  benefits: "package_central", benefitsDev: 0, row7: "2024", booking: "central", constants: null, incomeTax: "cbo" };
function packageShifts(p, caseName, method, o) {
  const edu = o.w === "avg"
    ? ["0.77", "0.82"].flatMap((w) => educationShifts(p, w, o.k).map((s) => ({ ...s, by: scale(s.by, both(0.5)) })))
    : educationShifts(p, o.w, o.k);
  const tax = o.incomeTax === "cbo" ? cboShifts(o.year, p, { scaled: o.scaled })
    : cboShifts(o.year, p, { scaled: o.scaled, incomeTax: false }).concat(row3Shifts(caseName, method));
  const extra = o.benefitsDev ? [{ side: "spending", line: SYN.constants, key: "k", by: o.benefitsDev }] : [];
  return [].concat(stackShifts(p), tax, otaShifts("vs_audit_package_ssn_rule"), row1Shifts(),
    medicalShifts(p, o.medSpec, { mcbs: o.mcbs, ltss: o.ltss }), edu, benefitShifts(p, o.benefits),
    justiceShifts(o.row7, o.booking), constantShifts(o.constants), extra);
}
const evalPackage = (caseName, method, o) =>
  band(build(packageShifts(STACKS[`row4+status_state_aware|${caseName}|${method}`], caseName, method, o)));
const mean2 = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, Object.assign({}, CENTRAL, o))));

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the adopted case and each change alone]");
const published = {};
csvRows("main_case_2026_09_23/derived/main_case_bands.csv").forEach((r) => {
  if (r.variant === "adopted") published[r.profile] = [Number(r.cost_low_bn), Number(r.cost_high_bn)];
});
const adopted = published.cbo_category_lag_non_school_full;
const base = band(build([]));
gate("no change reproduces the adopted main case", near(base[0], adopted[0], 1e-4) && near(base[1], adopted[1], 1e-4),
  `${base[0].toFixed(4)}–${base[1].toFixed(4)} vs ${adopted[0]}–${adopted[1]}`);
const change = (shifts) => { const b = band(build(shifts)); return [b[0] - base[0], b[1] - base[1]]; };
const alone = {};
function check(name, shifts, want, tol, detail) {
  const got = change(shifts);
  alone[name] = got;
  gate(`${name} alone reproduces ${detail}`, near(got[0], want[0], tol) && near(got[1], want[1], tol), `${f2(got)} vs ${f2(want)}`);
  return got;
}
const cpsLane = csvRows("cps_imputation_keys_2026_09_23/derived/status_combination_onbooks_lane.csv")
  .filter((r) => r.share_type === "origin" && r.arm === "row4+status_state_aware");
for (const c of CASES) for (const m of METHODS) {
  const want = ["shared", "personal"].map((a) => Number(cpsLane.find((r) => r.case === c && r.method === m && r.allocation === a).change_bn));
  check(`stack ${c}/${m}`, stackShifts(STACKS[`row4+status_state_aware|${c}|${m}`]), want, 2e-3, "the CPS lane's change");
}
const cboSpec = csvRows("external_benchmarks_2026_09_24/derived/cbo_spec_totals.csv").filter((r) => r.spec === "all_but_medicaid|2022");
check("CBO bundle 2022 (no skips)", cboShifts(2022, null, { skip: [], scaled: false }),
  ["low", "high"].map((e) => Number(cboSpec.find((r) => r.band_end === e).main_case_change_bn)), 1e-3, "the benchmarks lane");
const otaPub = csvRows("external_benchmarks_2026_09_24/derived/ota_main_case.csv")
  .find((r) => r.method === "vs_adopted_raw_keys" && r.profile === "cbo_category_lag_non_school_full");
check("Treasury EITC shares vs raw keys", otaShifts("vs_adopted_raw_keys"), [Number(otaPub.change_low_bn), Number(otaPub.change_high_bn)], 1e-3, "the benchmarks lane");
check("audit row 1", row1Shifts(), [mts.ptc_effect_on_main_case_bn, mts.ptc_effect_on_main_case_bn], 1e-6, "the audit's -14.23");
for (const spec of ["winsor_p995", "plain", "two_part_lognormal", "pooled_excl_2020_2021"]) {
  const r = ltssMain.find((x) => x.variant === "joint with medical-ethnicity lane: " + spec);
  check(`decision 2 joint ${spec}`, medicalShifts(null, spec), [Number(r.shift_low_bn), Number(r.shift_high_bn)], 1e-3, "the LTSS lane's engine run");
}
const schoolRow = (v) => { const r = schoolLines.find((x) => x.variant === v); return [Number(r.main_change_low_bn), Number(r.main_change_high_bn)]; };
check("row 6 whole line (w 0.77)", [
  { side: "spending", line: SYN.school, key: "k", by: minusT0(schoolV["row6_w0.77_whole_line"].school_target_bn) },
  { side: "spending", line: SYN.college, key: "k", by: minusT0(schoolV["row6_w0.77_whole_line"].college_target_bn) }],
  schoolRow("row6_w0.77_whole_line"), 1e-3, "the school lane");
check("row 6 school step with k (w 0.82)", [
  { side: "spending", line: SYN.school, key: "k", by: minusT0(schoolV["row6_w0.82|preferred"].school_target_bn) }],
  schoolRow("row6_w0.82|preferred"), 1e-3, "the school lane");
check("schools k on the adopted key", [
  { side: "spending", line: SYN.school, key: "k", by: minusT0(schoolV["preferred_district_and_school_level|blend"].school_target_bn) }],
  schoolRow("preferred_district_and_school_level|blend"), 1e-3, "the school lane");
const benPub = csvRows("admin_benefit_keys_2026_09_24/derived/main_case_translation.csv")
  .find((r) => r.spec === "package_central" && r.profile === "cbo_category_lag_non_school_full");
check("benefit keys (central)", benefitShifts(null), [Number(benPub.change_low_bn), Number(benPub.change_high_bn)], 1e-3, "the benefits lane");
const bk = bookingRow(BOOKING.central);
check("booking factor", justiceShifts(null, "central"), [bk, bk], 1e-6, "the crime lane");
check("audit row 7", justiceShifts("2024", null), [1.12, 1.12], 1e-6, "the audit's +1.12");
check("unit constant line", [{ side: "spending", line: SYN.constants, key: "k", by: both(1) }], [1, 1], 1e-9, "a response of 1");

// ---------------------------------------------------------------------------------------------------
console.log("\n[package]");
const C = central({});
console.log(`  central: ${C[0].toFixed(2)}–${C[1].toFixed(2)} (change ${(C[0] - base[0]).toFixed(2)} / ${(C[1] - base[1]).toFixed(2)})`);
const dev = (b) => [b[0] - C[0], b[1] - C[1]];
const components = [];
function component(name, label, variants) {
  const devs = variants.map(([v, b]) => ({ v, d: dev(b) }));
  const lo = [Math.min(0, ...devs.map((x) => x.d[0])), Math.min(0, ...devs.map((x) => x.d[1]))];
  const hi = [Math.max(0, ...devs.map((x) => x.d[0])), Math.max(0, ...devs.map((x) => x.d[1]))];
  components.push({ name, label, lo, hi, devs });
}
component("tax_block", "tax block: on-books share (low/central/high) x fill-in method",
  CASES.flatMap((c) => METHODS.map((m) => [`${c}/${m}`, evalPackage(c, m, CENTRAL)])));
component("income_tax", "CBO income gradients: 2018/2019/2022 data, scaled or not by the stack's factor",
  [2018, 2019, 2022].flatMap((y) => [true, false].map((s) => [`${y}${s ? "" : " unscaled"}`, central({ year: y, scaled: s })])));
component("medical", "decision 2: medical-ethnicity specifications and the MCBS 65+ bound",
  ["plain", "winsor_p999", "two_part_lognormal", "pooled_excl_2020_2021", "pooled_cpi_all_items", "pooled_year_normalized"]
    .map((s) => [s, central({ medSpec: s })]).concat([["MCBS as truth", central({ mcbs: "mcbs_as_truth" })],
      ["MCBS precision-weighted", central({ mcbs: "precision_weighted" })]]));
component("ltss", "long-term-care carve-out: extremes of the lane's 960 combinations",
  LTSS_RANGE.map((v) => [String(v), central({ ltss: v })]));
component("education", "audit row 6 weight w (0.77/0.82) x school price k (low/high)",
  ["0.77", "0.82"].flatMap((w) => ["low", "preferred", "high"].map((k) => [`w ${w} k ${k}`, central({ w, k })])));
const benSe = Object.fromEntries(benefitSe.map((r) => [r.allocation, 1.96 * Number(r.se_bn)]));
component("benefits", "benefit keys: central +/- 1.96 SE (package_se.csv)",
  [-1, 1].map((s) => [`${s > 0 ? "+" : "-"}1.96 SE`, central({ benefitsDev: { personal: s * benSe.personal, shared: s * benSe.shared } })]));
component("justice", "row 7 on 2023 arrests; booking factor Texas only or Arizona only",
  [["row 7 2023", central({ row7: "2023" })], ["booking Texas", central({ booking: "texas" })], ["booking Arizona", central({ booking: "arizona" })]]);
for (const id of Object.keys(CONSTANTS)) {
  component(id, CONSTANTS[id].label, ["lo", "hi"].map((p) => [p, central({ constants: { [id]: p } })]));
}
const sumLo = components.reduce((s, x) => [s[0] + x.lo[0], s[1] + x.lo[1]], [0, 0]);
const sumHi = components.reduce((s, x) => [s[0] + x.hi[0], s[1] + x.hi[1]], [0, 0]);
const rangeLowEnd = [C[0] + sumLo[0], C[0] + sumHi[0]], rangeHighEnd = [C[1] + sumLo[1], C[1] + sumHi[1]];
// The same spreads combined as independent (root of the sum of squares), for context only.
const rss = (xs) => Math.sqrt(xs.reduce((s, x) => s + x * x, 0));
const quadrature = [C[0] - rss(components.map((x) => x.lo[0])), C[1] + rss(components.map((x) => x.hi[1]))];

// Comparisons: the audit's own row 3 in place of CBO's income tax; lane figures simply added.
const withRow3 = central({ incomeTax: "row3" });
// Sensitivity: no fill-in correction (audit row 13 at zero), the audit's rules alone in the stack.
const noFillIn = evalPackage("central", "audit_rules_alone", CENTRAL);
const stackCentral = mean2(...METHODS.map((m) => { const s = check(`stack central/${m} (again)`, stackShifts(STACKS[`row4+status_state_aware|central|${m}`]),
  alone[`stack central/${m}`], 1e-9, "itself"); return s; }));
const aloneParts = {
  stack: stackCentral,
  cbo: change(cboShifts(2022, null, { scaled: false })),
  ota_over_audit: change(otaShifts("vs_audit_package_ssn_rule")),
  row1: alone["audit row 1"],
  medical: alone["decision 2 joint winsor_p995"],
  education: mean2(change(educationShifts(null, "0.77", "preferred")), change(educationShifts(null, "0.82", "preferred"))),
  benefits: alone["benefit keys (central)"],
  justice: change(justiceShifts("2024", "central")),
  constants: change(constantShifts(null)),
};
const added = Object.values(aloneParts).reduce((s, x) => [s[0] + x[0], s[1] + x[1]], [base[0], base[1]]);
// The package split by side: taxes (receipt shifts) against keyed spending (spending and synthetic lines).
const bySide = (keep) => mean2(...METHODS.map((m) => {
  const p = STACKS[`row4+status_state_aware|central|${m}`];
  const b = band(build(packageShifts(p, "central", m, CENTRAL).filter(keep)));
  return [b[0] - base[0], b[1] - base[1]];
}));
const sides = { receipts: bySide((x) => x.side === "receipt"), spending: bySide((x) => x.side !== "receipt") };
gate("the two sides add to the package", near(sides.receipts[0] + sides.spending[0], C[0] - base[0], 1e-6)
  && near(sides.receipts[1] + sides.spending[1], C[1] - base[1], 1e-6), `${f2(sides.receipts)} + ${f2(sides.spending)}`);

// ---------------------------------------------------------------------------------------------------
fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
const bandsCsv = ["profile,variant,cost_low_bn,cost_high_bn,range_low_bn,range_high_bn",
  `cbo_category_lag_non_school_full,adopted_2026_09_23,${base[0].toFixed(4)},${base[1].toFixed(4)},,`,
  `cbo_category_lag_non_school_full,adopted,${C[0].toFixed(4)},${C[1].toFixed(4)},${rangeLowEnd[0].toFixed(4)},${rangeHighEnd[1].toFixed(4)}`,
  `cbo_category_lag_non_school_full,audit_row3_instead_of_cbo_income_tax,${withRow3[0].toFixed(4)},${withRow3[1].toFixed(4)},,`,
  `cbo_category_lag_non_school_full,no_fill_in_correction,${noFillIn[0].toFixed(4)},${noFillIn[1].toFixed(4)},,`,
  `cbo_category_lag_non_school_full,lane_figures_added,${added[0].toFixed(4)},${added[1].toFixed(4)},,`];
fs.writeFileSync(path.join(HERE, "derived", "main_case_bands.csv"), bandsCsv.join("\n") + "\n");
const compCsv = ["component,label,range_dev_low_end_lo,range_dev_low_end_hi,range_dev_high_end_lo,range_dev_high_end_hi"]
  .concat(components.map((x) => [x.name, `"${x.label}"`, x.lo[0].toFixed(4), x.hi[0].toFixed(4), x.lo[1].toFixed(4), x.hi[1].toFixed(4)].join(",")));
fs.writeFileSync(path.join(HERE, "derived", "components.csv"), compCsv.join("\n") + "\n");
const aloneCsv = ["change,alone_on_adopted_low_bn,alone_on_adopted_high_bn"]
  .concat(Object.entries(aloneParts).map(([k, v]) => `${k},${v[0].toFixed(4)},${v[1].toFixed(4)}`));
fs.writeFileSync(path.join(HERE, "derived", "alone_on_adopted.csv"), aloneCsv.join("\n") + "\n");
const summary = {
  adopted_2026_09_23: base, main_case: C, change: [C[0] - base[0], C[1] - base[1]],
  range: { low_end: rangeLowEnd, high_end: rangeHighEnd, overall: [rangeLowEnd[0], rangeHighEnd[1]], quadrature },
  audit_row3_instead_of_cbo_income_tax: withRow3, no_fill_in_correction: noFillIn, lane_figures_added: added,
  interaction_total: [C[0] - added[0], C[1] - added[1]],
  by_side: sides,
  components: components.map((x) => ({ name: x.name, label: x.label, lo: x.lo, hi: x.hi,
    variants: Object.fromEntries(x.devs.map((d) => [d.v, d.d])) })),
  alone_on_adopted: aloneParts,
};
fs.writeFileSync(path.join(HERE, "derived", "summary.json"), JSON.stringify(summary, null, 1) + "\n");

console.log("\n[result]");
console.log(`  adopted 2026-09-23          ${base[0].toFixed(2)}–${base[1].toFixed(2)}`);
console.log(`  adopted 2026-09-24          ${C[0].toFixed(2)}–${C[1].toFixed(2)}  (change ${(C[0] - base[0]).toFixed(2)} / ${(C[1] - base[1]).toFixed(2)})`);
console.log(`  range, low end              ${rangeLowEnd[0].toFixed(1)}–${rangeLowEnd[1].toFixed(1)}`);
console.log(`  range, high end             ${rangeHighEnd[0].toFixed(1)}–${rangeHighEnd[1].toFixed(1)}`);
console.log(`  spreads in quadrature       ${quadrature[0].toFixed(1)}–${quadrature[1].toFixed(1)}`);
console.log(`  no fill-in correction       ${noFillIn[0].toFixed(2)}–${noFillIn[1].toFixed(2)}`);
console.log(`  with audit row 3 instead    ${withRow3[0].toFixed(2)}–${withRow3[1].toFixed(2)}`);
console.log(`  taxes ${f2(sides.receipts)}   keyed spending ${f2(sides.spending)}`);
console.log(`  lane figures added          ${added[0].toFixed(2)}–${added[1].toFixed(2)}  (interactions ${(C[0] - added[0]).toFixed(2)} / ${(C[1] - added[1]).toFixed(2)})`);
for (const [k, v] of Object.entries(aloneParts)) console.log(`    alone: ${k.padEnd(16)} ${v[0].toFixed(2)} / ${v[1].toFixed(2)}`);
for (const x of components) console.log(`    range: ${x.name.padEnd(12)} low end ${x.lo[0].toFixed(2)}..+${x.hi[0].toFixed(2)}  high end ${x.lo[1].toFixed(2)}..+${x.hi[1].toFixed(2)}`);
if (failures) { console.error(`FAIL: ${failures} gate(s)`); process.exit(1); }
console.log("all gates passed");
