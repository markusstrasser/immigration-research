/* Step 5: the adopted main case run once per generation through the explorer engine.
 *
 * --case picks the package lane (CASES below):
 *   sept27          the default since 2026-09-27: main_case_long_run_2026_09_27 ($321.8194-387.3701bn), the
 *                   schools case with long-run road and park responses, rental assistance at 1, the return on
 *                   public capital (2% / 3%) and the government enterprises (option D);
 *   sept26_schools  main_case_schools_full_2026_09_26 ($258.4885-291.9548bn), schools at their full average
 *                   cost (response 1/1); reproduces its run of 2026-09-26 byte for byte;
 *   sept26          main_case_2026_09_26 ($200.9180-245.6949bn), schools at 0.6522/0.6813, the one-year
 *                   scenario; reproduces its run of 2026-09-26 byte for byte;
 *   sept24          main_case_2026_09_24, reproducing the September 24 run byte for byte.
 * The cases after sept24 are the September 24 package with the finite-removal responses (engine state, carried
 * by the package's MAIN_SPECS and gated against corrections.json meta.responses), audit row 8 at its finite
 * factor (lane row8_finite, split as the lane splits row 8, by population) and the consumption key (lane
 * consumption_key, from consumption_split.py); they share one payload and differ only in the school
 * response, until sept27. sept27 evaluates every model through the package's evaluateFull(): the engine at the
 * specification's line responses (the two long-run lines, housing_subsidies and the enterprise_surplus receipt)
 * plus the capital return, whose 24 components take their keys from that evaluation, so each generation's own
 * key shares split them (the 11 enterprise components by its enterprise_surplus receipt). Its payload is the
 * schools case's plus one receipt shift, the enterprise re-key; each generation's corrected model takes
 * rekeyEdits() on its own schools-case model, as modelFor() does for the union (lane enterprise_rekey).
 * --out-dir DIR writes the outputs to DIR instead of derived/ (the inputs always come from derived/).
 *
 * Reads the case's package read-only (<lane>/package.cjs: its shift lists, stack factors,
 * specifications and cost function; requiring it rewrites main_case_2026_09_24's vendored stack file byte
 * for byte when the CPS cache is unchanged) and this lane's derived inputs:
 *   model_{G1,G2,G3plus}.json and model_b_*.json  the uncorrected model split by generation (build_models.py,
 *                                                production.py), convention (a) own generation, (b) minors
 *                                                in the parents' generation;
 *   stack_by_generation.json                     the tax-records stack by generation (stack_split.py);
 *   external_by_generation.json                  CBO, Treasury OTA and premium-credit re-keys (external_split.py);
 *   correction_rules.json                        every other lane's split (correction_rules.py);
 *   consumption_key_by_generation.json           the consumption key's saving and corridor parts by
 *                                                generation (consumption_split.py; cases after sept24).
 * Each lane's union shift list is rebuilt exactly as packageShifts() builds it (gate), then split:
 *   - the stack by the generation payloads (exact);
 *   - ratio-type changes the package multiplies by the union's stack factor (CBO, medical ratios, schools,
 *     benefits) take each generation's own change times its own stack factor, the generation's cell after
 *     the stack over before; the small remainder from that non-additivity (reported) is spread by the
 *     generations' cells after the stack, so the three add to the package's figure exactly;
 *   - the long-term-care carve-out, premium credits, OTA, justice and the lane constants by their rules;
 *   - the consumption key's four receipt lines as the saving part times the generation's own stack factor
 *     on the consumption key (or the union's phi) less the corridor's dollars, the remainder spread by the
 *     cells after the stack as above; its cells with no main-case weight by each generation's share of the
 *     change in the key share.
 * The generation edits are netted per cell as correctionsPayload() nets the union's (the two fill-in
 * methods averaged), applied with Engine.applyCorrections to each generation's model, and every
 * specification of MAIN_SPECS is evaluated with the package's cost().
 * Gates (exit 1): the lanes rebuild packageShifts for both methods; every split adds to its union shift
 * (1e-9 bn); the netted generation edits add to corrections.json cell by cell (1e-9 bn); the corrected
 * union reproduces the case's main case (1e-4; after sept24 its main_case_bands.csv row `adopted`) and the
 * uncorrected union the uncorrected model at the case's responses (after sept24 the row
 * `uncorrected_at_adopted_responses`: sept27 $332.7493-398.3079bn, sept26_schools $265.5903-298.6797bn, sept26
 * $207.4046-253.1859bn; sept24 the September 23 case); for every specification and both conventions the three
 * generations' costs add to the union's (linearity, 1e-9 bn; the brief's gate is $0.01bn), corrected and
 * uncorrected. Cases after sept24 also gate that corrections.json is the package's payload and that the
 * specifications carry meta.responses. The move from the September 24 case is a chain at matched specifications
 * whose parts add exactly (1e-9) for every generation and the union: the general-government and school
 * responses, row 8 and the consumption key reach the September 26 case at the September 24 ends
 * (specifications 56 and 7); from sept26_schools on, school_full_cost then sets schools to 1 at the same
 * specifications, and band_end_specs moves to the schools case's own ends (48 and 11), whose union parts must
 * add to that lane's summary `change` (change_from_sept24, change_from_sept26). Under sept27 that chain runs on
 * the schools package and models, and a second chain leads from the schools case to this one at the same ends
 * (change_from_sept26_schools), in main_case.cjs's order: long-run responses, rental assistance, capital core,
 * capital block, then the enterprises (the receipt's re-key, the surplus at 1, the enterprise returns). Its
 * union parts must equal the case's change_at_fixed_specifications part by part and add to its `change` (1e-9);
 * the union must also reproduce the case's per_spec.csv (cost, capital by part and level, the enterprise receipt)
 * at every specification against the mean of the two fill-in methods (1e-9), and each generation's capital
 * return and enterprise receipt must add to the union's at every specification.
 * For step 6 (compare_ledger.py) it also splits each generation's cost at
 * the band ends into direct fiscal lines, production term and corrections, plus the direct lines at the
 * package's proportional reference (summary.ledger_bridge_a). The engine state is the package's stateFor();
 * under sept27 the capital return is part of the direct fiscal lines (the propagation brief's item 3) and is
 * also reported on its own.
 * Writes generation_results.csv, generation_summary.json, generation_corrections.json. After sept24 the
 * uncorrected model at the same specification is named `uncorrected_*` (under sept24 it was the
 * September 23 case, `sept23_*`). Run from the repository root:
 *   node infra/immigration-fiscal/generation_account_2026_09_24/run_generations.cjs [--case sept27|sept26_schools|sept26|sept24] [--out-dir DIR]
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const argv = process.argv.slice(2);
const arg = (name, dflt) => { const i = argv.indexOf(name); return i < 0 ? dflt : argv[i + 1]; };
// The case switch: each case's package lane. Repointing the lane is the default below. Every case after
// sept24 is built on main_case_2026_09_26/package.cjs (row 8's finite factor, the consumption key) and
// they differ only in their responses, which come from the package's MAIN_SPECS and meta.responses; sept27
// adds the capital return and the enterprise receipt's re-key on top of the schools case.
const CASES = { sept27: "main_case_long_run_2026_09_27", sept26_schools: "main_case_schools_full_2026_09_26",
  sept26: "main_case_2026_09_26", sept24: "main_case_2026_09_24" };
const CASE = arg("--case", "sept27");
if (!CASES[CASE]) throw new Error(`--case must be one of ${Object.keys(CASES).join(", ")}`);
const ON26 = CASE !== "sept24";
const ON27 = CASE === "sept27";
const MAIN = CASES[CASE];
const P = require(path.join(HERE, "..", MAIN, "package.cjs"));
// The schools case: under sept27 the package it builds on (PSCHOOLS), otherwise the case itself.
const SCH = ON27 ? P.PSCHOOLS : P;
const SCH_LANE = ON27 ? CASES.sept26_schools : MAIN;
const { Engine, MODEL, ALLOCS, SYN, SYN_LINES, MEDICAID, MAIN_SPECS, METHODS, STACKS, CENTRAL, LTSS_CENTRAL,
  both, scale, cost, expand, stackShifts, stackFactor, cboShifts, otaShifts, row1Shifts, medicalShifts,
  educationShifts, benefitShifts, justiceShifts, constantShifts, packageShifts, csvRows, readJson } = P;

const GENS = ["G1", "G2", "G3plus"];
const CONVS = ["a", "b"];
const IN = path.join(HERE, "derived");
const OUT = path.resolve(arg("--out-dir", IN));
const load = (f) => JSON.parse(fs.readFileSync(path.join(IN, f), "utf8"));
const fails = [];
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) fails.push(label);
}
const e = (x) => x.toExponential(1);

const stackGen = load("stack_by_generation.json");
const ext = load("external_by_generation.json");
const rules = load("correction_rules.json").rules;
const keyMeta = load("generation_key_shares.json").meta;
const models = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) =>
  [g, load(`${c === "a" ? "model_" : "model_b_"}${g}.json`)]))]));
const corrections = readJson(`${MAIN}/derived/corrections.json`);
// The schools case's payload: under sept27 the case's payload is it plus the enterprise re-key (gate), and the
// chain up to the schools case runs on it.
const schoolsPayload = ON27 ? readJson(`${SCH_LANE}/derived/corrections.json`) : corrections;
const mainSummary = readJson(`${MAIN}/derived/summary.json`);
const adopted = mainSummary.main_case;
// The uncorrected model at the case's responses: under the September 24 responses, the September 23 case.
const uncorrectedBand = ON26 ? mainSummary.uncorrected_at_adopted_responses : mainSummary.adopted_2026_09_23;
const U = ON26 ? "uncorrected" : "sept23";  // name of the uncorrected model at the same specification
console.log(`[case ${CASE}] ${MAIN}; outputs to ${path.relative(process.cwd(), OUT) || "."}`);
// After sept24 the gates take the case's published bands (main_case_bands.csv, main profile, four decimals);
// the summary keeps summary.json's full-precision figures, which must round to them.
const bandRow = (variant) => {
  const r = csvRows(`${MAIN}/derived/main_case_bands.csv`).find((x) => x.profile === P.MAIN_PROFILE && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] ${MAIN}/derived/main_case_bands.csv lacks ${P.MAIN_PROFILE} ${variant}`);
  return [Number(r.cost_low_bn), Number(r.cost_high_bn)];
};
const gateAdopted = ON26 ? bandRow("adopted") : adopted;
const gateUncorrected = ON26 ? bandRow("uncorrected_at_adopted_responses") : uncorrectedBand;
if (ON26) {
  gate("summary.json's main case and uncorrected band round to main_case_bands.csv (adopted, uncorrected_at_adopted_responses)",
    [0, 1].every((k) => Math.abs(adopted[k] - gateAdopted[k]) < 5.01e-5 && Math.abs(uncorrectedBand[k] - gateUncorrected[k]) < 5.01e-5),
    `${gateAdopted.map((x) => x.toFixed(4)).join("–")}; ${gateUncorrected.map((x) => x.toFixed(4)).join("–")}`);
  gate(`corrections.json is the ${MAIN} package's payload`, JSON.stringify(P.correctionsPayload()) === JSON.stringify(corrections),
    "deep-equal");
  const r = corrections.meta.responses;
  gate("the specifications carry the payload's responses (meta.responses)", MAIN_SPECS.every((s) =>
    [r.general_government.low, r.general_government.high].includes(s.gg) && [r.school.growth, r.school.decline].includes(s.school)),
    `general government ${r.general_government.low.toFixed(4)}/${r.general_government.high.toFixed(4)}, `
    + `schools ${r.school.growth.toFixed(4)}/${r.school.decline.toFixed(4)}`);
  if (ON27) {
    const cr = corrections.meta.capital_return;
    const at = (id, s) => r[id][s.reading];
    gate("the specifications carry the payload's long-run, rental-assistance and enterprise-receipt responses and its rates at their reading "
      + "(meta.responses, meta.capital_return)", MAIN_SPECS.every((s) => P.LR_LINES.every((id) => s.line_responses[id] === at(id, s))
      && s.line_responses[P.RENTAL] === at(P.RENTAL, s) && s.line_responses[P.ENTERPRISE_RECEIPT] === at(P.ENTERPRISE_LINE, s)
      && s.rate === cr.rates[s.reading] && s.enterprises === cr.enterprises),
    P.LR_LINES.map((id) => `${id} ${r[id].low.toFixed(4)}/${r[id].high.toFixed(4)}`).join(", ")
      + `, ${P.RENTAL} ${r[P.RENTAL].low}/${r[P.RENTAL].high}, ${P.ENTERPRISE_LINE} ${r[P.ENTERPRISE_LINE].low}/${r[P.ENTERPRISE_LINE].high}, `
      + `rates ${cr.rates.low}/${cr.rates.high}, option ${cr.enterprises}`);
    const tail = corrections.edits.slice(schoolsPayload.edits.length);
    gate(`corrections.json is ${SCH_LANE}'s payload (its lines and edits, in order) plus the enterprise receipt's re-key: one receipt `
      + "shift expanded to the eight incidence rules, equal to rekeyEdits() on the schools-case model",
    JSON.stringify(corrections.lines) === JSON.stringify(schoolsPayload.lines)
      && JSON.stringify(corrections.edits.slice(0, schoolsPayload.edits.length)) === JSON.stringify(schoolsPayload.edits)
      && tail.length === MODEL.receipts.scenarios.length && tail.every((x) => x.side === "receipt" && x.line === P.ENTERPRISE_LINE)
      && JSON.stringify(tail) === JSON.stringify(P.rekeyEdits(Engine.applyCorrections(MODEL, schoolsPayload))),
    `${schoolsPayload.lines.length} lines, ${schoolsPayload.edits.length} + ${tail.length} edits`);
  }
}

// ---------------------------------------------------------------------------------------------------
// The package's union shifts, lane by lane (packageShifts at CENTRAL).
function lanes(p) {
  const O = CENTRAL;
  const edu = ["0.77", "0.82"].flatMap((w) => educationShifts(p, w, O.k).map((s) => ({ ...s, by: scale(s.by, both(0.5)) })));
  const out = {
    stack: stackShifts(p), cbo: cboShifts(O.year, p, { scaled: O.scaled }), ota: otaShifts("vs_audit_package_ssn_rule"),
    row1: row1Shifts(), medical: medicalShifts(p, O.medSpec, { mcbs: O.mcbs, ltss: O.ltss }), education: edu,
    benefits: benefitShifts(p, O.benefits), justice: justiceShifts(O.row7, O.booking), constants: constantShifts(O.constants),
  };
  if (ON26) out.row8_finite = P.row8Shifts(O);
  return out;
}
const LANES24 = ["stack", "cbo", "ota", "row1", "medical", "education", "benefits", "justice", "constants"];
const SHIFT_LANES = LANES24.concat(ON26 ? ["row8_finite"] : []);
// The consumption key enters as cell edits after the shifts (main_case_2026_09_26/package.cjs build).
const LANES = SHIFT_LANES.concat(ON26 ? ["consumption_key"] : []);
const unionLanes = {};
for (const m of METHODS) {
  const p = STACKS[`row4+status_state_aware|central|${m}`];
  unionLanes[m] = lanes(p);
  const flat = SHIFT_LANES.flatMap((l) => unionLanes[m][l]);
  gate(`lanes rebuild packageShifts (${m})`, JSON.stringify(flat) === JSON.stringify(packageShifts(p, "central", m, CENTRAL)));
}
// The consumption key's union edits (the same dollars in all eight receipt scenarios on its four lines)
// and this lane's generation parts of them.
const CK_LINES = ["general_sales_tax", "excise_selective_sales", "customs_duties", "personal_current_transfers"];
const ckGen = ON26 ? load("consumption_key_by_generation.json") : null;
const ckUnion = ON26 ? P.ckEdits(CENTRAL) : [];
const ckByLine = {};
if (ON26) {
  let same = ckGen.meta.spec === CENTRAL.ck && Math.abs(ckGen.meta.phi - P.CK.meta.phi) < 1e-12;
  for (const x of ckUnion.filter((y) => y.side === "receipt" && CK_LINES.includes(y.line))) {
    const first = ckByLine[x.line] || (ckByLine[x.line] = x.by);
    same = same && ALLOCS.every((a) => x.by[a] === first[a] && Math.abs(x.by[a] - ckGen.union.edit_bn[x.line]) < 1e-9);
  }
  gate(`the consumption key's split is of the package's spec ${CENTRAL.ck}: one edit per line in every scenario and allocation, `
    + "equal to consumption_split.py's union edits", same && Object.keys(ckByLine).length === CK_LINES.length);
}

// ---------------------------------------------------------------------------------------------------
// Helpers.
const lineOf = (m, side, line) => (side === "receipt" ? m.receipts.lines : m.spending.lines).find((l) => l.id === line);
function cellTarget(m, side, line, key, a) {
  const l = lineOf(m, side, line);
  return side === "receipt" ? l.cells[m.receipts.reference][a].target_bn : l.keys[key || l.preferred_key][a].target_bn;
}
function payloadDelta(p, m, side, line, key, a) {
  if (side === "receipt") return (p.receipts && p.receipts[line] && p.receipts[line][a]) || 0;
  const k = key || lineOf(m, side, line).preferred_key;
  return (p.spending && p.spending[line] && p.spending[line][k] && p.spending[line][k][a]) || 0;
}
const zero = () => Object.fromEntries(GENS.map((g) => [g, both(0)]));
let worstResidual = 0;
let SCALING = "own";  // "union": every generation's change times the union's factor (a sensitivity)
// A ratio-type union shift (the union's change times the union's stack factor) split as each generation's
// own change times its own factor; the non-additive remainder goes by the generations' cells after the stack.
function scaledSplit(unionBy, deltas, gm, gp, side, line, key) {
  const out = zero();
  if (SCALING === "union") {
    for (const a of ALLOCS) {
      const sum = GENS.reduce((s, g) => s + deltas[g][a], 0);
      if (Math.abs(sum) < 1e-12) throw new Error("union scaling: no change to scale on " + line);
      for (const g of GENS) out[g][a] = deltas[g][a] * unionBy[a] / sum;
    }
    return out;
  }
  for (const a of ALLOCS) {
    const t0 = {}, t1 = {};
    let sum = 0, T = 0;
    const part = {};
    for (const g of GENS) {
      t0[g] = cellTarget(gm[g], side, line, key, a);
      t1[g] = t0[g] + payloadDelta(gp[g], gm[g], side, line, key, a);
      T += t1[g];
      part[g] = deltas[g][a] * (t0[g] === 0 ? 1 : t1[g] / t0[g]);
      sum += part[g];
    }
    const resid = unionBy[a] - sum;
    worstResidual = Math.max(worstResidual, Math.abs(resid));
    for (const g of GENS) out[g][a] = part[g] + resid * t1[g] / T;
  }
  return out;
}
let worstSplit = 0;
function checkSplit(unionBy, split) {
  for (const a of ALLOCS) worstSplit = Math.max(worstSplit, Math.abs(GENS.reduce((s, g) => s + split[g][a], 0) - unionBy[a]));
}
const fromRule = (item, conv) => Object.fromEntries(GENS.map((g) => [g, { personal: item[conv][g].personal, shared: item[conv][g].shared }]));
const byWeights = (by, w) => Object.fromEntries(GENS.map((g, j) => [g, { personal: by.personal * w[j], shared: by.shared * w[j] }]));
const near = (a, b, tol) => Math.abs(a - b) < tol;

// Medical inputs exactly as package.cjs medicalShifts reads them.
const medTrans = csvRows("medical_ethnicity_pooled_2026_09_23/derived/translation_account.csv").filter((r) => r.spec === CENTRAL.medSpec);
const medComb = csvRows("ltss_share_2026_09_23/derived/combined.csv").find((r) => r.spec === CENTRAL.medSpec);
const dMed = Object.fromEntries(medTrans.map((r) => [r.line, Number(r.delta_bn)]));
const ltssFrac = -Number(medComb.remainder_ratio_adjustment_bn) / dMed[MEDICAID];
const ratioPart = dMed[MEDICAID] * (1 - ltssFrac);
const LTSS_PARTS = ["NF", "ICF", "MHF", "HCBS", "remainder_key"];
const CONST_IDS = ["row8", "row9", "row10", "small", "shelter", "care"];

let ckResidual = 0;
// options: {stackPayloads: {g: payload}, benefits: "central" | "alt_g1" | "alt_usborn", justice, row10,
//   scaling: "own" | "union", ck: "exact" | "old_key_shares"}
function genLanes(conv, m, opts) {
  const o = Object.assign({ benefits: "central", justice: "arrest_like_custody", row10: "central", scaling: "own", ck: "exact" }, opts || {});
  SCALING = o.scaling;
  const p = STACKS[`row4+status_state_aware|central|${m}`];
  const L = unionLanes[m];
  const gm = models[conv];
  const gp = o.stackPayloads ? o.stackPayloads[conv][m] : Object.fromEntries(GENS.map((g) => [g, stackGen.payloads[m][conv][g]]));
  const G = Object.fromEntries(GENS.map((g) => [g, Object.fromEntries(LANES.map((l) => [l, []]))]));
  const push = (lane, s, split) => { checkSplit(s.by, split); for (const g of GENS) G[g][lane].push({ ...s, by: split[g] }); };
  // Stack: the generation payloads, matched shift by shift to the union's.
  const gs = Object.fromEntries(GENS.map((g) => [g, stackShifts(gp[g])]));
  for (const s of L.stack) {
    const split = {};
    for (const g of GENS) {
      const hits = gs[g].filter((x) => x.side === s.side && x.line === s.line && (x.key || null) === (s.key || null));
      if (hits.length !== 1) throw new Error(`stack shift not unique for ${g}: ${s.side}/${s.line}/${s.key}`);
      split[g] = hits[0].by;
    }
    push("stack", s, split);
  }
  // CBO (scaled).
  for (const s of L.cbo) {
    const c = ext.cbo[s.line];
    const f = stackFactor(p, s.side, s.line, s.key);
    for (const a of ALLOCS) if (!near(c.union[a] * f[a], s.by[a], 1e-9)) throw new Error("CBO union change differs on " + s.line);
    push("cbo", s, scaledSplit(s.by, fromRule(c, conv), gm, gp, s.side, s.line, s.key));
  }
  // OTA and premium credits.
  for (const s of L.ota) push("ota", s, fromRule(ext.ota, conv));
  for (const s of L.row1) push("row1", s, fromRule(ext.row1, conv));
  // Medical: the ratio parts scaled, the long-term-care carve-out by its rule, the stack's LTSS part removed.
  {
    const [mcd, ...rest] = L.medical;
    const fMed = stackFactor(p, "spending", MEDICAID, "medicaid");
    const stackMed = p.spending[MEDICAID].medicaid;
    for (const a of ALLOCS) {
      if (!near(ratioPart * fMed[a] + LTSS_CENTRAL - stackMed[a] * ltssFrac, mcd.by[a], 1e-9)) throw new Error("medicaid shift not rebuilt");
    }
    const w = rules.medical.ratio_part_weights[conv];
    const rp = scaledSplit({ personal: ratioPart * fMed.personal, shared: ratioPart * fMed.shared },
      byWeights(both(ratioPart), w), gm, gp, "spending", MEDICAID, "medicaid");
    const split = zero();
    for (const g of GENS) {
      for (const a of ALLOCS) {
        const ltss = LTSS_PARTS.reduce((s, c) => s + rules.ltss[c][conv][g][a], 0);
        split[g][a] = rp[g][a] + ltss - payloadDelta(gp[g], gm[g], "spending", MEDICAID, "medicaid", a) * ltssFrac;
      }
    }
    push("medical", mcd, split);
    for (const s of rest) {
      const f = stackFactor(p, "spending", s.line, s.key);
      for (const a of ALLOCS) if (!near(dMed[s.line] * f[a], s.by[a], 1e-9)) throw new Error("medical line not rebuilt " + s.line);
      push("medical", s, scaledSplit(s.by, fromRule(rules.medical[s.line], conv), gm, gp, "spending", s.line, s.key));
    }
  }
  // Education: school and college steps at w 0.77 and 0.82, half each, scaled by the education_mix factor.
  {
    const order = [["school", "0.77"], ["college", "0.77"], ["school", "0.82"], ["college", "0.82"]];
    const f = stackFactor(p, "spending", "education_services", "education_mix");
    L.education.forEach((s, i) => {
      const r = rules.education[`${order[i][0]}|${order[i][1]}`];
      for (const a of ALLOCS) if (!near(r.union[a] * 0.5 * f[a], s.by[a], 1e-9)) throw new Error("education shift not rebuilt " + i);
      const half = Object.fromEntries(GENS.map((g) => [g, scale(r[conv][g], both(0.5))]));
      push("education", s, scaledSplit(s.by, half, gm, gp, "spending", "education_services", "education_mix"));
    });
  }
  // Benefits (scaled by the key's stack factor).
  for (const s of L.benefits) {
    const r = rules.benefits[s.line];
    const f = stackFactor(p, "spending", s.line, null);
    for (const a of ALLOCS) if (!near(r.union[a] * f[a], s.by[a], 1e-9)) throw new Error("benefit shift not rebuilt " + s.line);
    const d = o.benefits === "central" ? fromRule(r, conv) : Object.fromEntries(GENS.map((g) => [g, r[`${o.benefits}_${conv}`][g]]));
    push("benefits", s, scaledSplit(s.by, d, gm, gp, "spending", s.line, null));
  }
  // Justice: the arrest-keyed parts of the use key.
  for (const s of L.justice) push("justice", s, byWeights(s.by, rules.justice[conv][o.justice]));
  // Lane constants.
  for (const s of L.constants) {
    const split = zero();
    const total = both(0);
    for (const id of CONST_IDS) {
      const r = rules.constants[id];
      for (const a of ALLOCS) total[a] += r.union[a];
      for (const g of GENS) {
        for (const a of ALLOCS) {
          split[g][a] += id === "row10" && o.row10 !== "central" ? r[`alt_children_${conv}`][g][a] : r[conv][g][a];
        }
      }
    }
    for (const a of ALLOCS) if (!near(total[a], s.by[a], 1e-9)) throw new Error("constants not rebuilt");
    push("constants", s, split);
  }
  if (!ON26) return G;
  // Audit row 8 at its finite-removal factor: as the lane splits row 8 (population).
  for (const s of L.row8_finite) {
    const r = rules.constants.row8;
    push("row8_finite", s, Object.fromEntries(GENS.map((g) => [g, Object.fromEntries(ALLOCS.map((a) =>
      [a, s.by[a] * r[conv][g][a] / r.union[a]]))])));
  }
  // The consumption key. On its four lines the saving part R_g takes the generation's own stack factor on
  // the line (the cell after the stack over before, as scaledSplit) or the union's phi, the corridor part
  // A_g stays in dollars, and the remainder goes by the cells after the stack. Its other cells (no
  // main-case weight) go by the generation's share of the change in the adopted-basis key share. The
  // brief's fallback, every cell by the generations' shares of the old key, is the sensitivity ck.
  const cg = ckGen[conv];
  const onLine = {};
  const residTotal = both(0);
  for (const line of CK_LINES) {
    const out = zero();
    for (const a of ALLOCS) {
      if (o.ck === "old_key_shares") {
        for (const g of GENS) out[g][a] = ckByLine[line][a] * cg[g].old_key_share;
        continue;
      }
      const t1 = {}, part = {};
      let T = 0, sum = 0;
      for (const g of GENS) {
        const t0 = cellTarget(gm[g], "receipt", line, null, a);
        t1[g] = t0 + payloadDelta(gp[g], gm[g], "receipt", line, null, a);
        T += t1[g];
        const f = o.scaling === "union" ? ckGen.meta.phi : t1[g] / t0;
        part[g] = f * cg[g].R_bn[line] - cg[g].A_bn[line];
        sum += part[g];
      }
      const resid = ckByLine[line][a] - sum;
      residTotal[a] += resid;
      for (const g of GENS) out[g][a] = part[g] + resid * t1[g] / T;
    }
    onLine[line] = out;
  }
  for (const a of ALLOCS) ckResidual = Math.max(ckResidual, Math.abs(residTotal[a]));
  for (const x of ckUnion) {
    const w = (g) => (o.ck === "old_key_shares" ? cg[g].old_key_share : cg[g].change_fraction);
    const split = x.side === "receipt" && CK_LINES.includes(x.line) ? onLine[x.line]
      : Object.fromEntries(GENS.map((g) => [g, scale(x.by, both(w(g)))]));
    checkSplit(x.by, split);
    for (const g of GENS) G[g].consumption_key.push({ ...x, by: split[g], cell: true });
  }
  return G;
}

// Netted edits per generation, as correctionsPayload() nets the union's; cell edits (the consumption key)
// are already expanded and follow the shifts, as in main_case_2026_09_26/package.cjs.
function netEdits(shifts) {
  const net = new Map();
  const cells = shifts.filter((s) => s.cell).map(({ cell, ...x }) => x);
  for (const x of expand(shifts.filter((s) => !s.cell)).concat(cells)) {
    const id = [x.side, x.line, x.side === "receipt" ? x.scenario : x.key].join("|");
    if (net.has(id)) {
      const n = net.get(id);
      n.by = { personal: n.by.personal + x.by.personal, shared: n.by.shared + x.by.shared };
    } else net.set(id, { ...x, by: { ...x.by } });
  }
  return net;
}
function payloadFor(G, g, laneSet) {
  const shifts = METHODS.flatMap((m) => (laneSet || LANES).flatMap((l) => G[m][g][l]).map((x) => ({ ...x, by: scale(x.by, both(0.5)) })));
  return { lines: SYN_LINES, edits: [...netEdits(shifts).values()] };
}

// ---------------------------------------------------------------------------------------------------
console.log("[splits]");
const GL = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(METHODS.map((m) => [m, genLanes(c, m)]))]));
gate("every lane split adds to its union shift", worstSplit < 1e-9, `max |diff| ${e(worstSplit)} bn`);
const mainResidual = worstResidual;
console.log(`  · non-additive remainder of the stack-factor scaling, spread by cells: max ${mainResidual.toFixed(4)} bn`);
const ckMainResidual = ckResidual;
if (ON26) console.log(`  · consumption key: remainder of its own-factor scaling over its four lines, spread by cells: max ${ckMainResidual.toFixed(4)} bn`);
const payloads = {};
const cid = (x) => [x.side, x.line, x.side === "receipt" ? x.scenario : x.key].join("|");
const unionEdits = new Map(corrections.edits.map((x) => [cid(x), x]));
// Under sept27 each generation's payload is its schools-case payload (the lanes above) plus its enterprise re-key:
// rekeyEdits() on the generation's schools-case model moves its enterprise_surplus receipt to its own corrected
// population share (general_public_services' population cell over the national amount), as modelFor() does for
// the union. The re-key alone is the lane enterprise_rekey.
const schoolsPayloads = {}, rekeys = {};
// A corrected model from a schools-case payload, re-keyed under sept27 (the sensitivities' variant payloads).
function correctedModel(m0, p) {
  const m = Engine.applyCorrections(m0, p);
  return ON27 ? Engine.applyCorrections(m, { lines: [], edits: P.rekeyEdits(m) }) : m;
}
for (const conv of CONVS) {
  payloads[conv] = {};
  schoolsPayloads[conv] = {};
  rekeys[conv] = {};
  for (const g of GENS) {
    const p = payloadFor(GL[conv], g);
    schoolsPayloads[conv][g] = p;
    if (!ON27) { payloads[conv][g] = p; continue; }
    rekeys[conv][g] = P.rekeyEdits(Engine.applyCorrections(models[conv][g], p));
    payloads[conv][g] = { lines: p.lines, edits: p.edits.concat(rekeys[conv][g]) };
  }
  if (ON27) {
    gate(`(${conv}) no generation's schools-case payload edits the ${P.ENTERPRISE_LINE} receipt, so the re-key's cells are its own`,
      GENS.every((g) => !schoolsPayloads[conv][g].edits.some((x) => x.side === "receipt" && x.line === P.ENTERPRISE_LINE)));
    const tail = corrections.edits.slice(schoolsPayload.edits.length);
    const worstRekey = Math.max(...tail.flatMap((x) => ALLOCS.map((a) => Math.abs(GENS.reduce((t, g) =>
      t + rekeys[conv][g].find((y) => cid(y) === cid(x)).by[a], 0) - x.by[a]))));
    gate(`(${conv}) the generations' re-key edits (${GENS.map((g) => rekeys[conv][g].length).join("/")}) add to the case's ${tail.length}`,
      GENS.every((g) => rekeys[conv][g].length === tail.length) && worstRekey < 1e-12, `max |diff| ${e(worstRekey)} bn; on the reference rule `
      + GENS.map((g) => `${g} ${rekeys[conv][g].find((y) => y.scenario === MODEL.receipts.reference).by.personal.toFixed(6)}`).join(", "));
    // The uncorrected generation models take no re-key: their receipt share already equals their population share
    // (to model.json's stored precision, as the union's).
    const shareGap = (m) => {
      const l = m.receipts.lines.find((x) => x.id === P.ENTERPRISE_LINE), s = P.populationShare(m);
      return Math.max(...ALLOCS.map((a) => Math.abs(l.cells[m.receipts.reference][a].target_bn / l.national_bn - s[a])));
    };
    const off = Math.max(...GENS.map((g) => shareGap(models[conv][g])));
    gate(`(${conv}) the uncorrected generation models' ${P.ENTERPRISE_LINE} share equals their ${P.REKEY_LINE} population share, `
      + "so they take no re-key, as the uncorrected union", off < 1e-11, `max |diff| ${e(off)} (union ${e(shareGap(MODEL))})`);
  }
  let worst = 0;
  const ids = new Set([...unionEdits.keys(), ...GENS.flatMap((g) => payloads[conv][g].edits.map(cid))]);
  for (const id of ids) {
    for (const a of ALLOCS) {
      const u = unionEdits.has(id) ? unionEdits.get(id).by[a] : 0;
      const s = GENS.reduce((t, g) => { const x = payloads[conv][g].edits.find((y) => cid(y) === id); return t + (x ? x.by[a] : 0); }, 0);
      worst = Math.max(worst, Math.abs(s - u));
    }
  }
  gate(`(${conv}) the generations' netted edits add to corrections.json in all ${unionEdits.size} cells`, worst < 1e-9, `max |diff| ${e(worst)} bn`);
}

// ---------------------------------------------------------------------------------------------------
console.log("[engine]");
const unionModel = Engine.applyCorrections(MODEL, corrections);
// Under sept27 each corrected model's evaluations are kept whole (evaluateFull(): the engine's evaluation, the
// capital return's components and the cost), so the return and the enterprise receipt can be split and gated.
const fullAt = (m) => MAIN_SPECS.map((s) => P.evaluateFull(m, s));
const uFull = ON27 ? fullAt(unionModel) : null;
const uCost = ON27 ? uFull.map((r) => r.cost_bn) : MAIN_SPECS.map((s) => cost(unionModel, s));
const u0Cost = MAIN_SPECS.map((s) => cost(MODEL, s));
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
gate(`the corrected union reproduces the adopted main case${ON26 ? " (main_case_bands.csv adopted)" : ""}`,
  near(uCost[lo], gateAdopted[0], 1e-4) && near(uCost[hi], gateAdopted[1], 1e-4), `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)}`);
const lo0 = u0Cost.indexOf(Math.min(...u0Cost)), hi0 = u0Cost.indexOf(Math.max(...u0Cost));
gate(`the uncorrected union reproduces ${ON26 ? "the uncorrected model at the adopted responses (main_case_bands.csv)" : "the September 23 case"}`,
  near(u0Cost[lo0], gateUncorrected[0], 1e-4) && near(u0Cost[hi0], gateUncorrected[1], 1e-4),
  `${u0Cost[lo0].toFixed(4)}–${u0Cost[hi0].toFixed(4)}`);
// The capital return and the enterprise receipt of one evaluateFull() result, as per_spec.csv carries them.
const capWhere = (r, pred) => r.capital.components.filter(pred).reduce((a, c) => a + c.return_bn, 0);
const esOf = (evaluation) => evaluation.receipts.find((x) => x.id === P.ENTERPRISE_LINE);
const capRow = (r) => ({ cost_bn: r.cost_bn, capital_total_bn: r.capital.total_bn,
  capital_state_local_bn: capWhere(r, (c) => c.level === "state_local"), capital_federal_bn: capWhere(r, (c) => c.level === "federal"),
  capital_core_bn: capWhere(r, (c) => c.group === "core"), capital_block_bn: capWhere(r, (c) => c.group === "block"),
  capital_enterprise_bn: capWhere(r, (c) => c.group === "enterprise"),
  group_enterprise_surplus_bn: esOf(r.evaluation).amount_bn, enterprise_surplus_receipt_cost_bn: -esOf(r.evaluation).effect_bn });
let schoolsUnion = null, uSchools = null;
if (ON27) {
  const perSpec = csvRows(`${MAIN}/derived/per_spec.csv`);
  const cols = Object.keys(capRow(uFull[0]));
  let worst = 0, n = 0;
  MAIN_SPECS.forEach((_, i) => {
    const rs = perSpec.filter((x) => Number(x.spec) === i);
    if (rs.length !== METHODS.length || !METHODS.every((m) => rs.some((x) => x.method === m))) { worst = Infinity; return; }
    const ours = capRow(uFull[i]);
    for (const k of cols) { worst = Math.max(worst, Math.abs(ours[k] - rs.reduce((t, x) => t + Number(x[k]), 0) / rs.length)); n++; }
  });
  gate(`the corrected union reproduces per_spec.csv at every specification, against the mean of the two fill-in methods: ${cols.join(", ")}`,
    perSpec.length === METHODS.length * MAIN_SPECS.length && worst < 1e-9, `${n} values; max |diff| ${e(worst)} bn`);
  // The schools case on its own package, where the chains meet: its payload on the union, and its band.
  schoolsUnion = Engine.applyCorrections(MODEL, schoolsPayload);
  uSchools = SCH.MAIN_SPECS.map((s) => SCH.cost(schoolsUnion, s));
  const b = csvRows(`${SCH_LANE}/derived/main_case_bands.csv`).find((x) => x.profile === SCH.MAIN_PROFILE && x.variant === "adopted");
  gate(`the schools payload on its own package reproduces ${SCH_LANE}'s band (its main_case_bands.csv adopted)`,
    near(Math.min(...uSchools), Number(b.cost_low_bn), 1e-4) && near(Math.max(...uSchools), Number(b.cost_high_bn), 1e-4),
    `${Math.min(...uSchools).toFixed(4)}–${Math.max(...uSchools).toFixed(4)}`);
}
const res = {};
for (const conv of CONVS) {
  res[conv] = {};
  for (const g of GENS) {
    const m0 = models[conv][g];
    const m1 = Engine.applyCorrections(m0, payloads[conv][g]);
    if (!ON27) {
      res[conv][g] = { corrected: MAIN_SPECS.map((s) => cost(m1, s)), uncorrected: MAIN_SPECS.map((s) => cost(m0, s)), model: m1 };
      continue;
    }
    const full = fullAt(m1);
    const schoolsModel = Engine.applyCorrections(m0, schoolsPayloads[conv][g]);
    res[conv][g] = { corrected: full.map((r) => r.cost_bn), uncorrected: MAIN_SPECS.map((s) => cost(m0, s)), model: m1, full,
      schoolsModel, schools: SCH.MAIN_SPECS.map((s) => SCH.cost(schoolsModel, s)) };
  }
  for (const kind of ["corrected", "uncorrected"].concat(ON27 ? ["schools"] : [])) {
    const ref = { corrected: uCost, uncorrected: u0Cost, schools: uSchools }[kind];
    const worst = Math.max(...MAIN_SPECS.map((_, i) => Math.abs(GENS.reduce((t, g) => t + res[conv][g][kind][i], 0) - ref[i])));
    gate(`(${conv}) ${kind === "schools" ? "the schools case on its package" : kind}: the three generations add to the union in all `
      + `${MAIN_SPECS.length} specifications`, worst < 1e-9, `max |diff| ${e(worst)} bn (brief's gate $0.01bn)`);
  }
  if (!ON27) continue;
  gate(`(${conv}) each generation's payload gives the model modelFor() builds: its schools-case model, then rekeyEdits() on it `
    + "(spending and receipt lines deep-equal)", GENS.every((g) => {
    const two = correctedModel(models[conv][g], schoolsPayloads[conv][g]), m = res[conv][g].model;
    return JSON.stringify(two.spending) === JSON.stringify(m.spending) && JSON.stringify(two.receipts) === JSON.stringify(m.receipts);
  }));
  const shareOf = (m) => {
    const l = m.receipts.lines.find((x) => x.id === P.ENTERPRISE_LINE);
    return l.cells[m.receipts.reference].personal.target_bn / l.national_bn;
  };
  const offShare = Math.max(...GENS.flatMap((g) => { const m = res[conv][g].model, l = m.receipts.lines.find((x) => x.id === P.ENTERPRISE_LINE);
    return ALLOCS.map((a) => Math.abs(l.cells[m.receipts.reference][a].target_bn / l.national_bn - P.populationShare(m)[a])); }));
  gate(`(${conv}) each generation's ${P.ENTERPRISE_LINE} receipt sits at its own corrected population share on the reference rule`,
    offShare < 1e-14, GENS.map((g) => `${g} ${shareOf(res[conv][g].model).toFixed(6)}`).join(", ") + ` (union ${shareOf(unionModel).toFixed(6)}); `
    + `max |diff| ${e(offShare)}`);
  let worstCap = 0;
  MAIN_SPECS.forEach((_, i) => {
    const u = capRow(uFull[i]), parts = GENS.map((g) => capRow(res[conv][g].full[i]));
    for (const k of Object.keys(u)) worstCap = Math.max(worstCap, Math.abs(parts.reduce((t, x) => t + x[k], 0) - u[k]));
  });
  gate(`(${conv}) the generations' capital return (total, by level, by part) and enterprise receipt (group amount, cost) add to the union's `
    + `in all ${MAIN_SPECS.length} specifications`, worstCap < 1e-9, `max |diff| ${e(worstCap)} bn`);
}

// ---------------------------------------------------------------------------------------------------
// Results.
const pop = keyMeta.population, adults = keyMeta.adults_18plus;
const rows = [];
const summary = Object.assign(ON26 ? { case: CASE, responses: corrections.meta.responses,
  uncorrected_at_adopted_responses_bn: uncorrectedBand } : {},
{ adopted_main_case_bn: adopted, low_spec: MAIN_SPECS[lo], high_spec: MAIN_SPECS[hi], conventions: {} });
const perHead = (bn, n) => bn * 1e9 / n;
for (const conv of CONVS) {
  const cs = {};
  GENS.forEach((g, j) => {
    const r = res[conv][g];
    const own = [Math.min(...r.corrected), Math.max(...r.corrected)];
    const out = {
      population: pop[conv][j], adults: adults[conv][j],
      cost_bn: [r.corrected[lo], r.corrected[hi]], own_span_bn: own,
      per_member_usd: [perHead(r.corrected[lo], pop[conv][j]), perHead(r.corrected[hi], pop[conv][j])],
      per_adult_usd: [perHead(r.corrected[lo], adults[conv][j]), perHead(r.corrected[hi], adults[conv][j])],
      [`${U}_cost_bn`]: [r.uncorrected[lo0], r.uncorrected[hi0]],
      correction_bn: [r.corrected[lo] - r.uncorrected[lo], r.corrected[hi] - r.uncorrected[hi]],
    };
    cs[g] = out;
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      // Under sept27 two parts of cost_bn get their own columns: the capital return (an imputed resource cost at
      // 2% / 3%, not a payment) and the enterprise surplus receipt's cost (the group's share of the enterprises'
      // operating loss at response 1).
      rows.push(Object.assign({ convention: conv, generation: g, band_end: end, allocation: MAIN_SPECS[i].allocation,
        cost_bn: r.corrected[i], [`${U}_same_spec_bn`]: r.uncorrected[i], correction_bn: r.corrected[i] - r.uncorrected[i],
        population: pop[conv][j], adults: adults[conv][j], per_member_usd: perHead(r.corrected[i], pop[conv][j]),
        per_adult_usd: perHead(r.corrected[i], adults[conv][j]) }, ON27 ? { capital_return_bn: r.full[i].capital.total_bn,
        enterprise_surplus_receipt_bn: -esOf(r.full[i].evaluation).effect_bn } : {}));
    }
  });
  summary.conventions[conv] = cs;
}

// Lane contributions per generation at the band ends (the engine and the capital return are linear in the cells, so
// they add to the correction). Under sept27 the re-key is a lane of its own, enterprise_rekey.
const laneRows = [];
for (const conv of CONVS) {
  for (const g of GENS) {
    const m0 = models[conv][g];
    const base0 = [cost(m0, MAIN_SPECS[lo]), cost(m0, MAIN_SPECS[hi])];
    for (const lane of LANES.concat(ON27 ? ["enterprise_rekey"] : [])) {
      const ml = Engine.applyCorrections(m0, lane === "enterprise_rekey" ? { lines: SYN_LINES, edits: rekeys[conv][g] }
        : payloadFor(GL[conv], g, [lane]));
      laneRows.push({ convention: conv, generation: g, lane,
        low_bn: cost(ml, MAIN_SPECS[lo]) - base0[0], high_bn: cost(ml, MAIN_SPECS[hi]) - base0[1] });
    }
  }
}
for (const conv of CONVS) {
  for (const g of GENS) {
    const s = laneRows.filter((r) => r.convention === conv && r.generation === g);
    const tot = [s.reduce((t, r) => t + r.low_bn, 0), s.reduce((t, r) => t + r.high_bn, 0)];
    const c = summary.conventions[conv][g].correction_bn;
    gate(`(${conv}) ${g}: lane contributions add to the generation's correction`, near(tot[0], c[0], 1e-9) && near(tot[1], c[1], 1e-9));
  }
}
summary.lanes = laneRows;

// Sensitivities of the flagged or inferred splits: each alternative re-run through the same pipeline.
function variantCosts(opts) {
  const out = {};
  for (const conv of CONVS) {
    const G = Object.fromEntries(METHODS.map((m) => [m, genLanes(conv, m, opts)]));
    out[conv] = Object.fromEntries(GENS.map((g) => {
      const m1 = correctedModel(models[conv][g], payloadFor(G, g));
      return [g, [cost(m1, MAIN_SPECS[lo]), cost(m1, MAIN_SPECS[hi])]];
    }));
  }
  return out;
}
// The brief's literal status rule: the status components (A, B) to the first generation alone.
const literal = {};
for (const conv of CONVS) {
  literal[conv] = {};
  for (const m of METHODS) {
    const comp = stackGen.components;
    literal[conv][m] = {};
    for (const g of GENS) {
      const base = JSON.parse(JSON.stringify(stackGen.payloads[m][conv][g]));
      for (const name of ["A_status_rules", "B_state_aware_flag"]) {
        const mine = comp[name][conv][g], all = comp[name].union.union;
        for (const [side, lines] of Object.entries(all)) {
          for (const [line, v] of Object.entries(lines)) {
            const cells = side === "receipts" ? { _: v } : v;
            for (const [key, by] of Object.entries(cells)) {
              for (const a of ALLOCS) {
                const own = side === "receipts" ? ((mine.receipts[line] || {})[a] || 0) : (((mine.spending[line] || {})[key] || {})[a] || 0);
                const add = (g === "G1" ? (by[a] || 0) : 0) - own;
                if (side === "receipts") { base.receipts[line] = base.receipts[line] || {}; base.receipts[line][a] = (base.receipts[line][a] || 0) + add; }
                else { base.spending[line] = base.spending[line] || {}; base.spending[line][key] = base.spending[line][key] || {}; base.spending[line][key][a] = (base.spending[line][key][a] || 0) + add; }
              }
            }
          }
        }
      }
      literal[conv][m][g] = base;
    }
  }
}
// The brief's literal fill-in rule: the exact fill-in component replaced by the imputed-dollar split.
const fillLiteral = {};
for (const conv of CONVS) {
  fillLiteral[conv] = {};
  for (const m of METHODS) {
    const exact = stackGen.components[`D_${m}`][conv];
    const alt = rules.fill_in_literal[`D_${m}`][conv];
    fillLiteral[conv][m] = {};
    for (const g of GENS) {
      const base = JSON.parse(JSON.stringify(stackGen.payloads[m][conv][g]));
      for (const [line, by] of Object.entries(alt[g].receipts)) {
        for (const a of ALLOCS) base.receipts[line][a] += (by[a] || 0) - ((exact[g].receipts[line] || {})[a] || 0);
      }
      for (const [line, keys] of Object.entries(alt[g].spending)) {
        for (const [key, by] of Object.entries(keys)) {
          for (const a of ALLOCS) base.spending[line][key][a] += (by[a] || 0) - (((exact[g].spending[line] || {})[key] || {})[a] || 0);
        }
      }
      fillLiteral[conv][m][g] = base;
    }
  }
}
const central = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) => [g, summary.conventions[c][g].cost_bn]))]));
const sens = {
  central,
  benefits_to_g1: variantCosts({ benefits: "alt_g1" }),
  benefits_to_usborn: variantCosts({ benefits: "alt_usborn" }),
  justice_per_adult: variantCosts({ justice: "arrest_per_adult" }),
  foster_care_by_children: variantCosts({ row10: "children" }),
  status_rules_all_to_g1: variantCosts({ stackPayloads: literal }),
  fill_ins_by_imputed_dollars: variantCosts({ stackPayloads: fillLiteral }),
  stack_scaling_by_union_factor: variantCosts({ scaling: "union" }),
};
// The brief's fallback for the consumption key: each line's edit by the generations' shares of the old key.
if (ON26) sens.consumption_key_by_old_key_shares = variantCosts({ ck: "old_key_shares" });
// Production attribution alternatives at the two normalizations (the band ends use cash or gdp at the reference).
const prod = load("production_by_generation.json").reference;
summary.production_alternatives = {};
for (const [end, i] of [["low", lo], ["high", hi]]) {
  const norm = MAIN_SPECS[i].normalization;
  const r = prod[norm];
  const pf = (x) => x.P + x.F;
  summary.production_alternatives[end] = {
    normalization: norm,
    attribution_a: Object.fromEntries(GENS.map((g) => [g, pf(r.attribution_a[g])])),
    standalone_a: Object.fromEntries(GENS.map((g) => [g, pf(r.standalone_a[g])])),
    labor_income_share_a: Object.fromEntries(GENS.map((g) => [g, pf(r.labor_income_share_a[g])])),
  };
}
summary.sensitivities = sens;
summary.stack_scaling_remainder_max_bn = mainResidual;
if (ON26) summary.consumption_key_scaling_remainder_max_bn = ckMainResidual;

// Bridge to the September 19 ledger (step 6), convention (a) as the ledger's groups: at each band end the
// generation's cost split into the direct fiscal lines and the production term, and the direct lines once
// more under the package's proportional reference (schools, other education and the delayed services at
// their average cost; general government stays at the specification's response). The engine state is the
// package's stateFor(), the one definition its cost() uses (the propagation brief of 2026-09-27: a consumer that
// builds engine state itself misses line responses); the evaluation must return cost() exactly (gate). Under
// sept27 it is evaluateFull()'s, and the capital return, part of the direct fiscal response (that brief's item 3),
// sits in each fiscal part and is also reported alone (the *_capital_return_bn fields).
const partsAt = (m, spec, profile) => (ON27 ? P.evaluateFull(m, spec, profile)
  : { evaluation: Engine.evaluate(m, P.stateFor(m, spec, profile)), capital: { total_bn: 0 } });
console.log("[ledger bridge]");
const bridge = {};
let mirrorWorst = 0, prodWorst = 0;
for (const g of GENS) {
  bridge[g] = {};
  for (const [end, i] of [["low", lo], ["high", hi]]) {
    const spec = MAIN_SPECS[i];
    const m0 = models.a[g], m1 = res.a[g].model;
    const f0 = partsAt(m0, spec, P.MAIN_PROFILE), f1 = partsAt(m1, spec, P.MAIN_PROFILE);
    const fp = partsAt(m0, spec, "proportional_reference");
    const [main0, main1, prop0] = [f0.evaluation, f1.evaluation, fp.evaluation];
    const [k0, k1, kp] = [f0.capital.total_bn, f1.capital.total_bn, fp.capital.total_bn];
    mirrorWorst = Math.max(mirrorWorst, Math.abs(-main0.welfare_bn + k0 - cost(m0, spec)), Math.abs(-main1.welfare_bn + k1 - cost(m1, spec)),
      Math.abs(-prop0.welfare_bn + kp - cost(m0, spec, "proportional_reference")));
    const production = main0.private_wtp_bn + main0.induced_receipts_bn;
    prodWorst = Math.max(prodWorst, Math.abs(production - summary.production_alternatives[end].attribution_a[g]));
    bridge[g][end] = Object.assign({
      proportional_fiscal_bn: -prop0.direct_fiscal_response_bn + kp,
      adopted_responses_fiscal_bn: -main0.direct_fiscal_response_bn + k0,
      production_bn: -production,
      [`${U}_bn`]: -main0.welfare_bn + k0,
      corrections_bn: (-main1.welfare_bn + k1) - (-main0.welfare_bn + k0),
      adopted_bn: -main1.welfare_bn + k1,
    }, ON27 ? { proportional_capital_return_bn: kp, adopted_responses_capital_return_bn: k0, adopted_capital_return_bn: k1 } : {});
  }
}
gate(`the evaluation on the package's stateFor()${ON27 ? " (evaluateFull())" : ""} returns cost() exactly (main and proportional profiles)`,
  mirrorWorst < 1e-12, `max |diff| ${e(mirrorWorst)} bn`);
gate("the engine's production parts equal the attribution at the band ends", prodWorst < 1e-9, `max |diff| ${e(prodWorst)} bn`);
summary.ledger_bridge_a = bridge;

// The allocation rule alone: each band end with the other allocation and everything else held. The shared
// rule splits every key equally over the SPM unit, so parents carry part of their children's costs even
// in convention (a), and mixed units pass costs and taxes across the union's boundary (mixed_units.py).
summary.allocation_swap = {};
for (const conv of CONVS) {
  summary.allocation_swap[conv] = Object.fromEntries(GENS.map((g) => {
    const m1 = res[conv][g].model;
    return [g, { low_spec_personal_bn: cost(m1, { ...MAIN_SPECS[lo], allocation: "personal" }),
      high_spec_shared_bn: cost(m1, { ...MAIN_SPECS[hi], allocation: "shared" }) }];
  }));
}

// The move from the September 24 case, a chain at matched specifications whose parts add exactly (the engine
// is linear in cells and responses). The September 24 ends (specifications 56 and 7) are also the September
// 26 ends (gate).
//   1-2  general_government_response, school_response: the finite-removal responses on the September 24
//        corrected model at the September 24 end, each with the specification otherwise held (they act on
//        different lines, so they add);
//   3-4  row8, consumption_key: those lanes' cell edits at the September 26 specification. Parts 1-4 reach the
//        September 26 case (sept26_bn).
//   5    school_full_cost (sept26_schools): schools from 0.6522/0.6813 to 1 at the same specification;
//   6    band_end_specs (sept26_schools): the case at its own end less the case at the September 24 end. The
//        ends move because at a school response of 1 the school-share bound flips.
// Under sept26 the summary keeps that run's format (parts 1-4 in change_from_sept24). From sept26_schools on,
// change_from_sept24 carries all six and change_from_sept26 the last two. Under sept27 this chain runs on the
// schools package (its cost() and specifications) and the schools-case models, and ends at the schools case; the
// chain from there to sept27 follows (change_from_sept26_schools).
if (ON26) {
  console.log("[change from the September 24 case]");
  const costS = SCH.cost, specsS = SCH.MAIN_SPECS;  // the schools case's (the case's own before sept27)
  const s24 = P.P24.MAIN_SPECS;  // the September 24 specifications; later cases replace their responses value for value
  const s26 = CASE === "sept26" ? MAIN_SPECS : P.P26.MAIN_SPECS;
  const u24 = Engine.applyCorrections(MODEL, P.SEPT24);
  const c24 = s24.map((s) => costS(u24, s));
  const lo24 = c24.indexOf(Math.min(...c24)), hi24 = c24.indexOf(Math.max(...c24));
  const band24 = readJson("main_case_2026_09_24/derived/summary.json").main_case;
  gate("the September 24 corrections reproduce the September 24 case", near(c24[lo24], band24[0], 1e-4) && near(c24[hi24], band24[1], 1e-4),
    `${c24[lo24].toFixed(4)}–${c24[hi24].toFixed(4)}`);
  if (CASE !== "sept26") {
    gate(`the ${ON27 ? "schools case's" : "case's"} payload edits are the September 26 payload's`,
      JSON.stringify(P.P26.correctionsPayload().edits) === JSON.stringify(schoolsPayload.edits), "deep-equal");
  }
  // The schools case's union model and per-specification costs, and its ends (the case's own before sept27).
  const unionS = ON27 ? schoolsUnion : unionModel, uS = ON27 ? uSchools : uCost;
  const loS = uS.indexOf(Math.min(...uS)), hiS = uS.indexOf(Math.max(...uS));
  const c26 = s26.map((s) => costS(unionS, s));
  const band26 = readJson("main_case_2026_09_26/derived/summary.json").main_case;
  gate("the September 26 case has the September 24 ends and reproduces its band", c26.indexOf(Math.min(...c26)) === lo24
    && c26.indexOf(Math.max(...c26)) === hi24 && near(c26[lo24], band26[0], 1e-4) && near(c26[hi24], band26[1], 1e-4),
    `specifications ${lo24} and ${hi24}, ${c26[lo24].toFixed(4)}–${c26[hi24].toFixed(4)}`);
  const ENDS = [["low", lo24, loS], ["high", hi24, hiS]];
  console.log(`  · band ends: specifications ${lo24} and ${hi24} on September 24 and 26, ${loS} and ${hiS} in `
    + `${ON27 ? "the schools case" : "this case"}`);
  const edits24 = new Map(P.SEPT24.edits.map((x) => [cid(x), x]));
  const laneModel = {};
  const laneAt = (conv, g, lane, spec) => {
    const k = `${conv}|${g}|${lane}`;
    if (!laneModel[k]) laneModel[k] = Engine.applyCorrections(models[conv][g], payloadFor(GL[conv], g, [lane]));
    return costS(laneModel[k], spec) - costS(models[conv][g], spec);
  };
  // Parts 1-4 on a September 24 model m (lanes given for a generation, summed for the union).
  const toSept26 = (m, i24, lanesOf) => {
    const sept24 = costS(m, s24[i24]);
    const x = { sept24_bn: sept24, general_government_response_bn: costS(m, { ...s24[i24], gg: s26[i24].gg }) - sept24,
      school_response_bn: costS(m, { ...s24[i24], school: s26[i24].school }) - sept24, responses_bn: costS(m, s26[i24]) - sept24 };
    return Object.assign(x, lanesOf(s26[i24]));
  };
  // Parts 5-6 on the schools-case model m.
  const fromSept26 = (m, i24, i) => {
    const sept26 = costS(m, s26[i24]), atOldEnd = costS(m, specsS[i24]), atEnd = costS(m, specsS[i]);
    return { sept26_bn: sept26, school_full_cost_bn: atOldEnd - sept26, band_end_specs_bn: atEnd - atOldEnd, sept26_schools_bn: atEnd,
      change_bn: atEnd - sept26, school_line_bn: atEnd - costS(m, { ...specsS[i], school: 0 }) };
  };
  const PARTS24 = ["general_government_response_bn", "school_response_bn", "row8_bn", "consumption_key_bn"];
  const PARTS26 = ["school_full_cost_bn", "band_end_specs_bn"];
  const chain = { union: {} }, chain26 = { union: {} };
  let worstCells = 0, worstAdd = 0, worstParts = 0, worstUnion = 0, worstCase = 0;
  for (const conv of CONVS) {
    chain[conv] = {};
    chain26[conv] = {};
    const m24 = {};
    for (const g of GENS) m24[g] = Engine.applyCorrections(models[conv][g], payloadFor(GL[conv], g, LANES24));
    const p24 = Object.fromEntries(GENS.map((g) => [g, new Map(payloadFor(GL[conv], g, LANES24).edits.map((x) => [cid(x), x]))]));
    for (const id of new Set([...edits24.keys(), ...GENS.flatMap((g) => [...p24[g].keys()])])) {
      for (const a of ALLOCS) {
        const s = GENS.reduce((t, g) => t + (p24[g].has(id) ? p24[g].get(id).by[a] : 0), 0);
        worstCells = Math.max(worstCells, Math.abs(s - (edits24.has(id) ? edits24.get(id).by[a] : 0)));
      }
    }
    worstAdd = Math.max(worstAdd, ...s24.map((s, k) => Math.abs(GENS.reduce((t, g) => t + costS(m24[g], s), 0) - c24[k])));
    for (const g of GENS) {
      chain[conv][g] = {};
      chain26[conv][g] = {};
      for (const [end, i24, i] of ENDS) {
        const x = toSept26(m24[g], i24, (spec) => ({ row8_bn: laneAt(conv, g, "row8_finite", spec),
          consumption_key_bn: laneAt(conv, g, "consumption_key", spec) }));
        const r = res[conv][g];
        const y = fromSept26(ON27 ? r.schoolsModel : r.model, i24, i);
        worstParts = Math.max(worstParts, Math.abs(x.responses_bn - x.general_government_response_bn - x.school_response_bn),
          Math.abs(PARTS24.reduce((t, k) => t + x[k], x.sept24_bn) - y.sept26_bn),
          Math.abs(PARTS26.reduce((t, k) => t + y[k], y.sept26_bn) - y.sept26_schools_bn));
        worstCase = Math.max(worstCase, Math.abs(y.sept26_schools_bn - (ON27 ? r.schools : r.corrected)[i]));
        chain[conv][g][end] = { x, y };
      }
    }
  }
  for (const [end, i24, i] of ENDS) {
    const sumOf = (conv, k) => GENS.reduce((t, g) => t + chain[conv][g][end].x[k], 0);
    const x = toSept26(u24, i24, () => ({ row8_bn: sumOf("a", "row8_bn"), consumption_key_bn: sumOf("a", "consumption_key_bn") }));
    const y = fromSept26(unionS, i24, i);
    worstParts = Math.max(worstParts, Math.abs(x.responses_bn - x.general_government_response_bn - x.school_response_bn),
      Math.abs(PARTS24.reduce((t, k) => t + x[k], x.sept24_bn) - y.sept26_bn),
      Math.abs(PARTS26.reduce((t, k) => t + y[k], y.sept26_bn) - y.sept26_schools_bn));
    worstCase = Math.max(worstCase, Math.abs(y.sept26_schools_bn - uS[i]));
    for (const conv of CONVS) {
      for (const k of ["sept24_bn", ...PARTS24]) worstUnion = Math.max(worstUnion, Math.abs(sumOf(conv, k) - x[k]));
      for (const k of ["sept26_bn", ...PARTS26, "sept26_schools_bn", "school_line_bn"]) {
        worstUnion = Math.max(worstUnion, Math.abs(GENS.reduce((t, g) => t + chain[conv][g][end].y[k], 0) - y[k]));
      }
    }
    chain.union[end] = { x, y };
  }
  gate("the generations' September 24 payloads (nine lanes) add to the September 24 corrections.json cell by cell", worstCells < 1e-9,
    `max |diff| ${e(worstCells)} bn`);
  gate("their September 24 costs add to the September 24 case in all 64 specifications", worstAdd < 1e-9, `max |diff| ${e(worstAdd)} bn`);
  gate(`the chain's parts add to each move (September 24 -> 26${CASE === "sept26" ? "" : ON27 ? " -> the schools case" : " -> this case"}), `
    + `every generation and the union, and end at the ${ON27 ? "schools case's" : "case's own"} cost`, worstParts < 1e-9 && worstCase < 1e-9,
  `max |diff| ${e(Math.max(worstParts, worstCase))} bn`);
  gate("the generations' parts add to the union's, part by part, both conventions", worstUnion < 1e-9, `max |diff| ${e(worstUnion)} bn`);
  const endKey = ON27 ? "sept26_schools" : "case";
  const ends = { low: { sept24: lo24, sept26: lo24, [endKey]: loS }, high: { sept24: hi24, sept26: hi24, [endKey]: hiS } };
  const pick = (fn) => Object.assign({ union: fn(chain.union) },
    ...CONVS.map((conv) => ({ [conv]: Object.fromEntries(GENS.map((g) => [g, fn(chain[conv][g])])) })));
  if (CASE === "sept26") {
    // The September 26 run's format, field for field.
    summary.change_from_sept24 = pick((c) => Object.fromEntries(ENDS.map(([end]) => {
      const { x, y } = c[end];
      return [end, { sept24_bn: x.sept24_bn, general_government_response_bn: x.general_government_response_bn,
        school_response_bn: x.school_response_bn, responses_bn: x.responses_bn, row8_bn: x.row8_bn,
        consumption_key_bn: x.consumption_key_bn, sept26_bn: y.sept26_bn, change_bn: y.sept26_bn - x.sept24_bn }];
    })));
  } else {
    const lane = readJson(`${SCH_LANE}/derived/summary.json`).change;  // that lane's own change from September 26
    const worstLane = Math.max(...ENDS.map(([end], k) => Math.abs(chain.union[end].y.change_bn - lane[k])));
    gate(`the union's school_full_cost + band_end_specs equal ${SCH_LANE}'s change from September 26`, worstLane < 1e-9,
      `${ENDS.map(([end]) => "+" + chain.union[end].y.change_bn.toFixed(4)).join(" / ")}; max |diff| ${e(worstLane)} bn`);
    summary.change_from_sept24 = Object.assign({ specifications: ends }, pick((c) => Object.fromEntries(ENDS.map(([end]) => {
      const { x, y } = c[end];
      return [end, { sept24_bn: x.sept24_bn, general_government_response_bn: x.general_government_response_bn,
        school_response_bn: x.school_response_bn, row8_bn: x.row8_bn, consumption_key_bn: x.consumption_key_bn, sept26_bn: y.sept26_bn,
        school_full_cost_bn: y.school_full_cost_bn, band_end_specs_bn: y.band_end_specs_bn, sept26_schools_bn: y.sept26_schools_bn,
        change_bn: y.sept26_schools_bn - x.sept24_bn }];
    }))));
    summary.change_from_sept26 = Object.assign({ specifications: ends }, pick((c) => Object.fromEntries(ENDS.map(([end]) => {
      const { y } = c[end];
      return [end, { sept26_bn: y.sept26_bn, school_full_cost_bn: y.school_full_cost_bn, band_end_specs_bn: y.band_end_specs_bn,
        sept26_schools_bn: y.sept26_schools_bn, change_bn: y.change_bn, school_line_bn: y.school_line_bn }];
    }))));
    // At a school response of 1 the growth and decline specifications coincide, so each end is attained twice.
    const rs = corrections.meta.responses.school;
    if (rs.growth === rs.decline) {
      const ties = (v) => uCost.map((x, k) => (x === v ? k : -1)).filter((k) => k >= 0);
      const tLo = ties(uCost[lo]), tHi = ties(uCost[hi]);
      const same = (t) => t.length === 2 && JSON.stringify(MAIN_SPECS[t[0]]) === JSON.stringify(MAIN_SPECS[t[1]])
        && CONVS.every((conv) => GENS.every((g) => res[conv][g].corrected[t[0]] === res[conv][g].corrected[t[1]]));
      gate(`the band ends tie exactly at one school response: low at specifications ${tLo.join(" and ")}, high at ${tHi.join(" and ")} `
        + `(identical specifications; costs equal (===) for the union and every generation); indexOf takes the first, ${lo} and ${hi}`,
      same(tLo) && same(tHi) && tLo[0] === lo && tHi[0] === hi);
      summary.band_end_ties = { low: tLo, high: tHi, picked: { low: lo, high: hi },
        rule: "at one school response the growth and decline specifications are identical; indexOf takes the first (growth)" };
    }
  }
}

// The move from the schools case to the September 27 case at the case's end specifications (48 and 11, the schools
// case's too: gate), in main_case.cjs's order and definitions, for every generation and the union:
//   long_run_responses, rental_assistance  each addition alone less the old settings (roads and parks at 0, rental
//                                          assistance and the receipt at 0, no capital return) on the re-keyed model;
//   capital_core, capital_block            the capital return's parts on the case;
//   enterprise_rekey                       the old settings on the re-keyed model less the schools case: 0, since the
//                                          receipt is still at 0 when the re-key applies;
//   enterprise_surplus_receipt             the receipt's cost at response 1 (minus its effect): the group's share of
//                                          the enterprises' operating loss, a receipt;
//   capital_enterprise                     the 11 enterprise components, keyed by the evaluation's receipt share.
// They add to change_bn exactly. Outside the sum: the long-run lines' own parts (group amount x response), the
// receipt's group amount and share, the re-key's move of that amount, the return by level, public housing's return
// and the re-key's effect (the case less the same case on the schools-case model, the receipt at model.json's
// share). The union's parts must equal the case's change_at_fixed_specifications and add to its change.
if (ON27) {
  console.log("[change from the schools case]");
  const OLD = { long_run: false, rental: 0, capital: false, enterprise_receipt: 0 };
  const sOld = P.specsFor(OLD), sLr = P.specsFor({ rental: 0, capital: false, enterprise_receipt: 0 });
  const sRental = P.specsFor({ long_run: false, capital: false, enterprise_receipt: 0 });
  const loS = uSchools.indexOf(Math.min(...uSchools)), hiS = uSchools.indexOf(Math.max(...uSchools));
  gate("the case keeps the schools case's end specifications, in both fill-in methods (summary.json end_specifications)",
    lo === loS && hi === hiS && mainSummary.end_specifications.every((x) => x.low_end.index === lo && x.high_end.index === hi), `${lo} / ${hi}`);
  const PARTS27 = ["long_run_responses_bn", "rental_assistance_bn", "capital_core_bn", "capital_block_bn", "enterprise_rekey_bn",
    "enterprise_surplus_receipt_bn", "capital_enterprise_bn"];
  const lineOfEval = (ev, id) => ev.spending.find((l) => l.id === id);
  // One entity at end specification i: its schools-case model mS, its case model m1 and m1's evaluateFull() there.
  const move = (mS, m1, full, i) => {
    const evS = Engine.evaluate(mS, SCH.stateFor(mS, SCH.MAIN_SPECS[i], SCH.MAIN_PROFILE)), ev = full.evaluation;
    const schools = -evS.welfare_bn, old = cost(m1, sOld[i]);
    return { sept26_schools_bn: schools,
      long_run_responses_bn: cost(m1, sLr[i]) - old, rental_assistance_bn: cost(m1, sRental[i]) - old,
      capital_core_bn: capWhere(full, (c) => c.group === "core"), capital_block_bn: capWhere(full, (c) => c.group === "block"),
      enterprise_rekey_bn: old - schools, enterprise_surplus_receipt_bn: -esOf(ev).effect_bn,
      capital_enterprise_bn: capWhere(full, (c) => c.group === "enterprise"),
      sept27_bn: full.cost_bn, change_bn: full.cost_bn - schools,
      long_run_by_line_bn: Object.fromEntries(P.LR_LINES.map((id) => [id, lineOfEval(ev, id).amount_bn * lineOfEval(ev, id).response])),
      enterprise_surplus_amount_bn: esOf(ev).amount_bn, enterprise_surplus_share: esOf(ev).amount_bn / esOf(ev).national_bn,
      enterprise_rekey_receipt_move_bn: esOf(ev).amount_bn - esOf(evS).amount_bn,
      capital_return_bn: full.capital.total_bn,
      capital_by_level_bn: { state_local: capWhere(full, (c) => c.level === "state_local"), federal: capWhere(full, (c) => c.level === "federal") },
      of_which_public_housing_bn: capWhere(full, (c) => c.id === "ent_housing_sl"),
      enterprise_rekey_against_model_json_share_bn: full.cost_bn - cost(mS, MAIN_SPECS[i]) };
  };
  const ENDS27 = [["low", lo], ["high", hi]];
  const flat = (x) => Object.assign({}, ...Object.entries(x).map(([k, v]) => (typeof v === "object"
    ? Object.fromEntries(Object.entries(v).map(([kk, vv]) => [`${k}.${kk}`, vv])) : { [k]: v })));
  let worstParts27 = 0, worstCase27 = 0, worstLines = 0, worstUnion27 = 0, rekeyNonzero = 0;
  const check = (x, caseCost, schoolsCost) => {
    worstParts27 = Math.max(worstParts27, Math.abs(PARTS27.reduce((t, k) => t + x[k], 0) - x.change_bn));
    worstCase27 = Math.max(worstCase27, Math.abs(x.sept27_bn - caseCost), Math.abs(x.sept26_schools_bn - schoolsCost));
    worstLines = Math.max(worstLines, Math.abs(P.LR_LINES.reduce((t, id) => t + x.long_run_by_line_bn[id], 0) - x.long_run_responses_bn));
    if (x.enterprise_rekey_bn !== 0) rekeyNonzero++;
  };
  const chain27 = { union: {} };
  for (const [end, i] of ENDS27) {
    chain27.union[end] = move(schoolsUnion, unionModel, uFull[i], i);
    check(chain27.union[end], uCost[i], uSchools[i]);
  }
  for (const conv of CONVS) {
    chain27[conv] = {};
    for (const g of GENS) {
      const r = res[conv][g];
      chain27[conv][g] = {};
      for (const [end, i] of ENDS27) {
        chain27[conv][g][end] = move(r.schoolsModel, r.model, r.full[i], i);
        check(chain27[conv][g][end], r.corrected[i], r.schools[i]);
      }
    }
    for (const [end] of ENDS27) {
      const u = flat(chain27.union[end]), parts = GENS.map((g) => flat(chain27[conv][g][end]));
      for (const k of Object.keys(u)) worstUnion27 = Math.max(worstUnion27, Math.abs(parts.reduce((t, x) => t + x[k], 0) - u[k]));
    }
  }
  gate("the chain's parts add to the move from the schools case, every generation and the union, both ends, from the schools case's "
    + "cost to this case's", worstParts27 < 1e-9 && worstCase27 < 1e-9, `max |diff| ${e(Math.max(worstParts27, worstCase27))} bn`);
  gate("enterprise_rekey is exactly 0 for every generation and the union: the receipt is still at 0 when the re-key applies", rekeyNonzero === 0);
  gate("the two long-run lines' own parts (group amount x response) add to long_run_responses", worstLines < 1e-9, `max |diff| ${e(worstLines)} bn`);
  gate("the generations' parts, and every item outside the sum, add to the union's, both conventions", worstUnion27 < 1e-9,
    `max |diff| ${e(worstUnion27)} bn`);
  const fx = mainSummary.change_at_fixed_specifications;
  const FX = { long_run_responses_bn: "long_run_responses", rental_assistance_bn: "rental_assistance", capital_core_bn: "capital_core",
    capital_block_bn: "capital_block", enterprise_rekey_bn: "enterprise_rekey", enterprise_surplus_receipt_bn: "enterprise_surplus_receipt",
    capital_enterprise_bn: "capital_enterprise", change_bn: "total", enterprise_rekey_receipt_move_bn: "enterprise_rekey_receipt_move",
    of_which_public_housing_bn: "of_which_public_housing",
    enterprise_rekey_against_model_json_share_bn: "enterprise_rekey_against_model_json_share" };
  const worstFx = Math.max(...ENDS27.flatMap(([end], j) => Object.entries(FX).map(([k, c]) => Math.abs(chain27.union[end][k] - fx[c][j]))
    .concat([Math.abs(chain27.union[end].change_bn - mainSummary.change[j])])));
  gate("the union's parts equal the case's change_at_fixed_specifications part by part (the seven parts, the total and the three items outside "
    + "its sum), and its change equals the case's change", worstFx < 1e-9,
  `${ENDS27.map(([end]) => "+" + chain27.union[end].change_bn.toFixed(4)).join(" / ")}; max |diff| ${e(worstFx)} bn`);
  const cap = mainSummary.capital_at_end_specifications, ent = mainSummary.enterprises.receipt_at_end_specifications;
  const worstCapEnds = Math.max(...ENDS27.flatMap(([end], j) => {
    const x = chain27.union[end];
    return [x.capital_return_bn - cap.total_bn[j], x.capital_by_level_bn.state_local - cap.by_level_bn.state_local[j],
      x.capital_by_level_bn.federal - cap.by_level_bn.federal[j], x.capital_core_bn - cap.by_part_bn.core[j],
      x.capital_block_bn - cap.by_part_bn.block[j], x.capital_enterprise_bn - cap.by_part_bn.enterprise[j],
      x.enterprise_surplus_amount_bn - ent.group_amount_bn[j], x.enterprise_surplus_share - mainSummary.enterprises.receipt_rekey.share.personal,
      x.enterprise_surplus_receipt_bn - ent.cost_bn[j], x.enterprise_rekey_receipt_move_bn - ent.move_from_the_schools_case_bn[j],
      ...P.LR_LINES.map((id) => x.long_run_by_line_bn[id] - mainSummary.lines_at_end_specifications[id].added_bn[j])].map(Math.abs);
  }));
  gate("the union's capital return (total, by level, by part), enterprise receipt (group amount, share, cost, move) and long-run lines "
    + "equal the case's summary.json at the ends", worstCapEnds < 1e-9, `max |diff| ${e(worstCapEnds)} bn`);
  const pick27 = (fn) => Object.assign({ union: fn(chain27.union) },
    ...CONVS.map((conv) => ({ [conv]: Object.fromEntries(GENS.map((g) => [g, fn(chain27[conv][g])])) })));
  summary.change_from_sept26_schools = Object.assign({ specifications: { low: lo, high: hi }, parts: PARTS27,
    rule: "main_case.cjs change_at_fixed_specifications, per generation: the parts add to change_bn; the items after change_bn are outside "
      + "the sum. The capital return is an imputed resource cost (the opportunity cost of the capital at 2% / 3%), not a payment; rental "
      + "assistance is a capped program, whose slots the group takes from other eligible households; the enterprise surplus is a receipt, "
      + "the group's share of the enterprises' operating loss (national -$47.46bn), at response 1" }, pick27((c) => c));
  // Beside the account, by generation (main_case_bands.csv rows), each at the union's own ends of that variant.
  const BESIDE = { without_capital_return: { capital: false }, enterprises_out_option_a: { enterprises: "A" },
    capital_return_at_7pct: { rates: { low: P.RATES.reported, high: P.RATES.reported } } };
  summary.beside_the_account = {};
  let worstBeside = 0, worstBesideAdd = 0;
  for (const [name, o] of Object.entries(BESIDE)) {
    const specs = P.specsFor(o);
    const u = specs.map((s) => cost(unionModel, s));
    const vlo = u.indexOf(Math.min(...u)), vhi = u.indexOf(Math.max(...u)), band = bandRow(name);
    worstBeside = Math.max(worstBeside, Math.abs(u[vlo] - band[0]), Math.abs(u[vhi] - band[1]));
    const out = { options: o, specifications: { low: vlo, high: vhi }, union_bn: [u[vlo], u[vhi]] };
    for (const conv of CONVS) {
      out[conv] = Object.fromEntries(GENS.map((g) => [g, [cost(res[conv][g].model, specs[vlo]), cost(res[conv][g].model, specs[vhi])]]));
      for (const j of [0, 1]) worstBesideAdd = Math.max(worstBesideAdd, Math.abs(GENS.reduce((t, g) => t + out[conv][g][j], 0) - out.union_bn[j]));
    }
    summary.beside_the_account[name] = out;
  }
  gate(`beside the account: the union reproduces main_case_bands.csv ${Object.keys(BESIDE).join(", ")} (1e-4), and the generations add to it`,
    worstBeside < 1e-4 && worstBesideAdd < 1e-9, Object.entries(summary.beside_the_account).map(([k, v]) =>
      `${k} ${v.union_bn.map((x) => x.toFixed(4)).join("–")} at ${v.specifications.low}/${v.specifications.high}`).join("; "));
}

// ---------------------------------------------------------------------------------------------------
// A failed gate writes nothing: the outputs in derived/ stay those of the last passing run.
if (fails.length) {
  console.log(`✗ ${fails.length} gate(s) failed, nothing written: ${fails.join("; ")}`);
  process.exit(1);
}
const header = Object.keys(rows[0]);
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "generation_results.csv"),
  [header.join(","), ...rows.map((r) => header.map((k) => (typeof r[k] === "number" ? r[k].toFixed(6) : r[k])).join(","))].join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "generation_summary.json"), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "generation_corrections.json"), JSON.stringify({
  meta: Object.assign({ source: "generation_account_2026_09_24/run_generations.cjs", union: `${MAIN}/derived/corrections.json`,
    layout: "convention -> generation -> engine corrections payload (lines, edits); the three add to the union's edits" },
  ON27 ? { enterprise_rekey: `each payload ends with its ${MODEL.receipts.scenarios.length} ${P.ENTERPRISE_LINE} re-key edits: rekeyEdits() on `
    + "the generation's schools-case model (the edits before them), as modelFor() re-keys the union" } : {}),
  payloads }) + "\n");

console.log("[results] net cost to other residents at the adopted band ends ($bn a year; low = shared, high = personal)");
for (const conv of CONVS) {
  console.log(`  convention (${conv})`);
  for (const g of GENS) {
    const c = summary.conventions[conv][g];
    console.log(`    ${g.padEnd(7)} ${c.cost_bn.map((x) => x.toFixed(2)).join(" – ")}  (${ON26 ? "uncorrected at the adopted responses" : "Sept 23 case"} `
      + `${c[`${U}_cost_bn`].map((x) => x.toFixed(2)).join(" – ")}); `
      + `per member $${c.per_member_usd.map((x) => Math.round(x)).join("–$")}, per adult $${c.per_adult_usd.map((x) => Math.round(x)).join("–$")}`);
  }
}
if (ON26) {
  const f = (x, k) => ["low", "high"].map((end) => (x[end][k] >= 0 ? "+" : "") + x[end][k].toFixed(2)).join(" / ");
  const c = summary.change_from_sept24;
  const rowsOf = [["union", c.union], ...CONVS.flatMap((conv) => GENS.map((g) => [`(${conv}) ${g}`, c[conv][g]]))];
  if (CASE === "sept26") {
    console.log("[change from the September 24 case] $bn, low / high");
    for (const [label, x] of rowsOf) {
      console.log(`    ${label.padEnd(12)} ${f(x, "sept24_bn")} -> ${f(x, "sept26_bn")}: general government ${f(x, "general_government_response_bn")}, `
        + `schools ${f(x, "school_response_bn")}, row 8 ${f(x, "row8_bn")}, consumption key ${f(x, "consumption_key_bn")}`);
    }
  } else {
    console.log("[change from the September 24 case: -> September 26 -> schools at 1 -> the case's ends] $bn, low / high");
    for (const [label, x] of rowsOf) {
      console.log(`    ${label.padEnd(12)} ${f(x, "sept24_bn")} -> ${f(x, "sept26_bn")} -> ${f(x, "sept26_schools_bn")}: general government `
        + `${f(x, "general_government_response_bn")}, schools ${f(x, "school_response_bn")}, row 8 ${f(x, "row8_bn")}, consumption key `
        + `${f(x, "consumption_key_bn")}, school full cost ${f(x, "school_full_cost_bn")}, band end ${f(x, "band_end_specs_bn")}`);
    }
  }
}
if (ON27) {
  const f = (x, k) => ["low", "high"].map((end) => (x[end][k] >= 0 ? "+" : "") + x[end][k].toFixed(2)).join(" / ");
  const c = summary.change_from_sept26_schools;
  console.log("[change from the schools case: long-run responses, rental assistance, capital core, capital block, re-key, enterprise surplus, "
    + "enterprise returns] $bn, low / high");
  for (const [label, x] of [["union", c.union], ...CONVS.flatMap((conv) => GENS.map((g) => [`(${conv}) ${g}`, c[conv][g]]))]) {
    console.log(`    ${label.padEnd(12)} ${f(x, "sept26_schools_bn")} -> ${f(x, "sept27_bn")}: ${c.parts.map((k) => f(x, k)).join(", ")}; `
      + `capital return ${f(x, "capital_return_bn")}, receipt ${f(x, "enterprise_surplus_amount_bn")}`);
  }
}
console.log("  ✓ all generation-run gates passed");
