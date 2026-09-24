/* The adopted 2026-09-24 package as importable definitions: the September 23 frame, the model edits
 * each lane contributes, and packageShifts(), which assembles them with the combining rules that
 * RESULT.md documents. main_case.cjs runs the gates and writes the bands; sign_reversal.cjs and page
 * builders import the same definitions, so there is one package.
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

const gateState = { failures: 0 };
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) gateState.failures += 1;
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
// The engine responds to these lines by class (engine.js spendingResponse); cost() below also sets
// their responses explicitly.
const SYN_LINES = [
  { id: SYN.school, family: "consumption", response_class: "education_school_part",
    label: "Schools priced where the group enrolls (correction)" },
  { id: SYN.college, family: "consumption", response_class: "education_other_part",
    label: "Colleges and other education, re-keyed (correction)" },
  { id: SYN.constants, family: "consumption", response_class: "correction_constant",
    label: "Care work, shelter and audit rows 8–10 (corrections counted in full)" },
];
// Service profiles of main_case_2026_09_23 (main_case_translate.js PROFILES): the main case, its
// variant with non-school education fixed, and the proportional reference.
const PROFILES = {
  cbo_category_lag_non_school_full: { other: 1, delayed: 0, school: null },
  cbo_category_lag_non_school_fixed: { other: 0, delayed: 0, school: null },
  proportional_reference: { other: 1, delayed: 1, school: 1 },
};
const MAIN_PROFILE = "cbo_category_lag_non_school_full";
function cost(m, spec, profile) {
  const pr = PROFILES[profile || MAIN_PROFILE];
  if (!pr) throw new Error("unknown profile " + profile);
  const school = pr.school === null ? spec.school : pr.school;
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = m.receipts.reference;
  s.production.normalization = spec.normalization;
  s.count_production = true;
  s.general_government_response = spec.gg;
  s.key_override = { public_order_safety: spec.justice, medicaid_and_chip_other_medical: spec.uc };
  s.response_override = {
    education_services: spec.share * school + (1 - spec.share) * pr.other,
    public_order_safety: 1, health_services: 1, income_security_services: 1,
    housing_community_services: 1, economic_affairs_services: pr.delayed, recreation_culture: pr.delayed,
    [SYN.school]: spec.share * school, [SYN.college]: (1 - spec.share) * pr.other, [SYN.constants]: 1,
  };
  return -Engine.evaluate(m, s).welfare_bn;
}
const band = (m, profile) => span(MAIN_SPECS.map((spec) => cost(m, spec, profile)));

// A change is a list of shifts {side: "receipt" | "spending", line, key, by: {personal, shared}}.
const MEDICAID = "medicaid_and_chip_other_medical";
// Keys built on the key a change was measured on take the same dollar change: the uninsured-use keys
// add uncompensated care to the Medicaid key, and raw ethnicity coding is a variant of the use key.
// The main case evaluates only uninsured_use_low/high and use; the 0.7x-use and raw-coding variants
// matter to consumers that range over every executed key (the figures page's outer envelope).
const KEY_FAMILIES = {
  [MEDICAID]: { medicaid: ["medicaid", "uninsured_use_low", "uninsured_use_high", "uninsured_use_07_low", "uninsured_use_07_high"] },
  public_order_safety: { use: ["use", "use_raw_coding"] },
};
// A list of shifts as the engine's cell edits (Engine.applyCorrections), in order.
function expand(shifts) {
  const edits = [];
  for (const s of shifts) {
    if (s.side === "receipt") {
      // Receipt changes are measured on the reference incidence rule. Every other executed rule takes
      // the same proportional change to the group's share of the line, so the rules keep their ratio;
      // on the lines where the rules agree that is the same dollar change.
      const line = MODEL.receipts.lines.find((l) => l.id === s.line);
      if (!line) throw new Error("no receipt line " + s.line);
      for (const sc of MODEL.receipts.scenarios) {
        const by = {};
        for (const a of ALLOCS) {
          const t0 = line.cells[MODEL.receipts.reference][a].target_bn;
          by[a] = s.by[a] * (t0 === 0 ? 1 : line.cells[sc][a].target_bn / t0);
        }
        edits.push({ side: "receipt", line: s.line, scenario: sc, by });
      }
      continue;
    }
    const line = MODEL.spending.lines.find((l) => l.id === s.line) || SYN_LINES.find((l) => l.id === s.line);
    if (!line) throw new Error("no spending line " + s.line);
    const key = s.key || line.preferred_key || "k";
    for (const k of (KEY_FAMILIES[s.line] && KEY_FAMILIES[s.line][key]) || [key]) {
      edits.push({ side: "spending", line: s.line, key: k, by: { personal: s.by.personal, shared: s.by.shared } });
    }
  }
  return edits;
}
const build = (shifts) => Engine.applyCorrections(MODEL, { lines: SYN_LINES, edits: expand(shifts) });
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
  band(build(packageShifts(STACKS[`row4+status_state_aware|${caseName}|${method}`], caseName, method, o)), o.profile);
const mean2 = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, Object.assign({}, CENTRAL, o))));

// The adopted package as the engine's corrections payload (derived/corrections.json): the central case
// with the two fill-in methods' shift lists averaged (the engine is linear), one net edit per cell.
function correctionsPayload() {
  const shifts = METHODS.flatMap((meth) => packageShifts(STACKS[`row4+status_state_aware|central|${meth}`], "central", meth, CENTRAL)
    .map((x) => ({ ...x, by: scale(x.by, both(0.5)) })));
  const net = new Map();
  for (const e of expand(shifts)) {
    const id = [e.side, e.line, e.side === "receipt" ? e.scenario : e.key].join("|");
    if (net.has(id)) net.get(id).by = plus(net.get(id).by, e.by); else net.set(id, e);
  }
  return {
    meta: { source: "main_case_2026_09_24/package.cjs", adopted: "2026-09-24",
      decision: "decisions/2026-09-24-main-case-audit-and-outside-checks.md",
      case: `central; fill-in methods ${METHODS.join(" and ")} averaged` },
    lines: SYN_LINES, edits: [...net.values()],
  };
}

module.exports = {
  Engine, MODEL, FISCAL, HERE, ALLOCS, SYN, SYN_LINES, MEDICAID, MAIN_SPECS, PROFILES, MAIN_PROFILE, CASES, METHODS, STACKS, CENTRAL, CONSTANTS,
  BOOKING, LTSS_CENTRAL, LTSS_RANGE, gateState, gate, near, span, f2, csvRows, read, readJson, both, scale, plus,
  cost, band, build, expand, correctionsPayload, stackShifts, stackFactor, cboShifts, row3Shifts, otaShifts, row1Shifts, medicalShifts,
  educationShifts, minusT0, benefitShifts, justiceShifts, constantShifts, bookingRow, packageShifts,
  evalPackage, mean2, central, mts, schoolV, schoolLines, ltssMain, benefitSe,
};
