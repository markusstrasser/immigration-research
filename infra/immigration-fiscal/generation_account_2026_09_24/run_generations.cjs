/* Step 5: the adopted main case run once per generation through the explorer engine.
 *
 * --case picks the package lane (CASES below):
 *   sept26_schools  the default since 2026-09-26: main_case_schools_full_2026_09_26 ($258.4885-291.9548bn),
 *                   schools at their full average cost (response 1/1);
 *   sept26          main_case_2026_09_26 ($200.9180-245.6949bn), schools at 0.6522/0.6813, the one-year
 *                   scenario; reproduces its run of 2026-09-26 byte for byte;
 *   sept24          main_case_2026_09_24, reproducing the September 24 run byte for byte.
 * Both later cases are the September 24 package with the finite-removal responses (engine state, carried by
 * the package's MAIN_SPECS and gated against corrections.json meta.responses), audit row 8 at its finite
 * factor (lane row8_finite, split as the lane splits row 8, by population) and the consumption key (lane
 * consumption_key, from consumption_split.py); they share one payload and differ only in the school
 * response. --out-dir DIR writes the outputs to DIR instead of derived/ (the inputs always come from derived/).
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
 * `uncorrected_at_adopted_responses`: sept26_schools $265.5903-298.6797bn, sept26 $207.4046-253.1859bn;
 * sept24 the September 23 case); for every specification and both conventions the three generations' costs
 * add to the union's (linearity, 1e-9 bn; the brief's gate is $0.01bn), corrected and uncorrected. Cases after
 * sept24 also gate that corrections.json is the package's payload and that the specifications carry
 * meta.responses. The move from the September 24 case is a chain at matched specifications whose parts add
 * exactly (1e-9) for every generation and the union: the general-government and school responses, row 8 and
 * the consumption key reach the September 26 case at the September 24 ends (specifications 56 and 7); under
 * sept26_schools, school_full_cost then sets schools to 1 at the same specifications, and band_end_specs
 * moves to the case's own ends (48 and 11), whose union parts must add to that lane's summary `change`
 * (change_from_sept24, change_from_sept26).
 * For step 6 (compare_ledger.py) it also splits each generation's cost at
 * the band ends into direct fiscal lines, production term and corrections, plus the direct lines at the
 * package's proportional reference (summary.ledger_bridge_a).
 * Writes generation_results.csv, generation_summary.json, generation_corrections.json. After sept24 the
 * uncorrected model at the same specification is named `uncorrected_*` (under sept24 it was the
 * September 23 case, `sept23_*`). Run from the repository root:
 *   node infra/immigration-fiscal/generation_account_2026_09_24/run_generations.cjs [--case sept26_schools|sept26|sept24] [--out-dir DIR]
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const argv = process.argv.slice(2);
const arg = (name, dflt) => { const i = argv.indexOf(name); return i < 0 ? dflt : argv[i + 1]; };
// The case switch: each case's package lane. Repointing the lane is the default below. Every case after
// sept24 is built on main_case_2026_09_26/package.cjs (row 8's finite factor, the consumption key) and
// they differ only in their responses, which come from the package's MAIN_SPECS and meta.responses.
const CASES = { sept26_schools: "main_case_schools_full_2026_09_26", sept26: "main_case_2026_09_26", sept24: "main_case_2026_09_24" };
const CASE = arg("--case", "sept26_schools");
if (!CASES[CASE]) throw new Error(`--case must be one of ${Object.keys(CASES).join(", ")}`);
const ON26 = CASE !== "sept24";
const MAIN = CASES[CASE];
const P = require(path.join(HERE, "..", MAIN, "package.cjs"));
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
for (const conv of CONVS) {
  payloads[conv] = {};
  for (const g of GENS) payloads[conv][g] = payloadFor(GL[conv], g);
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
const uCost = MAIN_SPECS.map((s) => cost(unionModel, s));
const u0Cost = MAIN_SPECS.map((s) => cost(MODEL, s));
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
gate(`the corrected union reproduces the adopted main case${ON26 ? " (main_case_bands.csv adopted)" : ""}`,
  near(uCost[lo], gateAdopted[0], 1e-4) && near(uCost[hi], gateAdopted[1], 1e-4), `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)}`);
const lo0 = u0Cost.indexOf(Math.min(...u0Cost)), hi0 = u0Cost.indexOf(Math.max(...u0Cost));
gate(`the uncorrected union reproduces ${ON26 ? "the uncorrected model at the adopted responses (main_case_bands.csv)" : "the September 23 case"}`,
  near(u0Cost[lo0], gateUncorrected[0], 1e-4) && near(u0Cost[hi0], gateUncorrected[1], 1e-4),
  `${u0Cost[lo0].toFixed(4)}–${u0Cost[hi0].toFixed(4)}`);
const res = {};
for (const conv of CONVS) {
  res[conv] = {};
  for (const g of GENS) {
    const m0 = models[conv][g];
    const m1 = Engine.applyCorrections(m0, payloads[conv][g]);
    res[conv][g] = { corrected: MAIN_SPECS.map((s) => cost(m1, s)), uncorrected: MAIN_SPECS.map((s) => cost(m0, s)), model: m1 };
  }
  for (const kind of ["corrected", "uncorrected"]) {
    const ref = kind === "corrected" ? uCost : u0Cost;
    const worst = Math.max(...MAIN_SPECS.map((_, i) => Math.abs(GENS.reduce((t, g) => t + res[conv][g][kind][i], 0) - ref[i])));
    gate(`(${conv}) ${kind}: the three generations add to the union in all ${MAIN_SPECS.length} specifications`, worst < 1e-9,
      `max |diff| ${e(worst)} bn (brief's gate $0.01bn)`);
  }
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
      rows.push({ convention: conv, generation: g, band_end: end, allocation: MAIN_SPECS[i].allocation,
        cost_bn: r.corrected[i], [`${U}_same_spec_bn`]: r.uncorrected[i], correction_bn: r.corrected[i] - r.uncorrected[i],
        population: pop[conv][j], adults: adults[conv][j], per_member_usd: perHead(r.corrected[i], pop[conv][j]),
        per_adult_usd: perHead(r.corrected[i], adults[conv][j]) });
    }
  });
  summary.conventions[conv] = cs;
}

// Lane contributions per generation at the band ends (the engine is linear, so they add to the correction).
const laneRows = [];
for (const conv of CONVS) {
  for (const g of GENS) {
    const m0 = models[conv][g];
    const base0 = [cost(m0, MAIN_SPECS[lo]), cost(m0, MAIN_SPECS[hi])];
    for (const lane of LANES) {
      const ml = Engine.applyCorrections(m0, payloadFor(GL[conv], g, [lane]));
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
      const m1 = Engine.applyCorrections(models[conv][g], payloadFor(G, g));
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
// their average cost; general government stays at the specification's response). The state mirrors
// package.cjs cost() so evaluate() can report the parts; it must return cost() exactly (gate).
function stateOf(m, spec, profile) {
  const pr = P.PROFILES[profile];
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
  return s;
}
console.log("[ledger bridge]");
const bridge = {};
let mirrorWorst = 0, prodWorst = 0;
for (const g of GENS) {
  bridge[g] = {};
  for (const [end, i] of [["low", lo], ["high", hi]]) {
    const spec = MAIN_SPECS[i];
    const m0 = models.a[g], m1 = res.a[g].model;
    const main0 = Engine.evaluate(m0, stateOf(m0, spec, P.MAIN_PROFILE));
    const main1 = Engine.evaluate(m1, stateOf(m1, spec, P.MAIN_PROFILE));
    const prop0 = Engine.evaluate(m0, stateOf(m0, spec, "proportional_reference"));
    mirrorWorst = Math.max(mirrorWorst, Math.abs(-main0.welfare_bn - cost(m0, spec)), Math.abs(-main1.welfare_bn - cost(m1, spec)),
      Math.abs(-prop0.welfare_bn - cost(m0, spec, "proportional_reference")));
    const production = main0.private_wtp_bn + main0.induced_receipts_bn;
    prodWorst = Math.max(prodWorst, Math.abs(production - summary.production_alternatives[end].attribution_a[g]));
    bridge[g][end] = {
      proportional_fiscal_bn: -prop0.direct_fiscal_response_bn,
      adopted_responses_fiscal_bn: -main0.direct_fiscal_response_bn,
      production_bn: -production,
      [`${U}_bn`]: -main0.welfare_bn,
      corrections_bn: main0.welfare_bn - main1.welfare_bn,
      adopted_bn: -main1.welfare_bn,
    };
  }
}
gate("the mirrored state returns cost() exactly (main and proportional profiles)", mirrorWorst < 1e-12, `max |diff| ${e(mirrorWorst)} bn`);
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
// Under sept26 the summary keeps that run's format (parts 1-4 in change_from_sept24). Under sept26_schools,
// change_from_sept24 carries all six and change_from_sept26 the last two.
if (ON26) {
  console.log("[change from the September 24 case]");
  const s24 = P.P24.MAIN_SPECS;  // the September 24 specifications; later cases replace their responses value for value
  const s26 = CASE === "sept26" ? MAIN_SPECS : P.P26.MAIN_SPECS;
  const u24 = Engine.applyCorrections(MODEL, P.SEPT24);
  const c24 = s24.map((s) => cost(u24, s));
  const lo24 = c24.indexOf(Math.min(...c24)), hi24 = c24.indexOf(Math.max(...c24));
  const band24 = readJson("main_case_2026_09_24/derived/summary.json").main_case;
  gate("the September 24 corrections reproduce the September 24 case", near(c24[lo24], band24[0], 1e-4) && near(c24[hi24], band24[1], 1e-4),
    `${c24[lo24].toFixed(4)}–${c24[hi24].toFixed(4)}`);
  if (CASE !== "sept26") {
    gate("the case's payload edits are the September 26 payload's", JSON.stringify(P.P26.correctionsPayload().edits) === JSON.stringify(corrections.edits),
      "deep-equal");
  }
  const c26 = s26.map((s) => cost(unionModel, s));
  const band26 = readJson("main_case_2026_09_26/derived/summary.json").main_case;
  gate("the September 26 case has the September 24 ends and reproduces its band", c26.indexOf(Math.min(...c26)) === lo24
    && c26.indexOf(Math.max(...c26)) === hi24 && near(c26[lo24], band26[0], 1e-4) && near(c26[hi24], band26[1], 1e-4),
    `specifications ${lo24} and ${hi24}, ${c26[lo24].toFixed(4)}–${c26[hi24].toFixed(4)}`);
  const ENDS = [["low", lo24, lo], ["high", hi24, hi]];
  console.log(`  · band ends: specifications ${lo24} and ${hi24} on September 24 and 26, ${lo} and ${hi} in this case`);
  const edits24 = new Map(P.SEPT24.edits.map((x) => [cid(x), x]));
  const laneModel = {};
  const laneAt = (conv, g, lane, spec) => {
    const k = `${conv}|${g}|${lane}`;
    if (!laneModel[k]) laneModel[k] = Engine.applyCorrections(models[conv][g], payloadFor(GL[conv], g, [lane]));
    return cost(laneModel[k], spec) - cost(models[conv][g], spec);
  };
  // Parts 1-4 on a September 24 model m (lanes given for a generation, summed for the union).
  const toSept26 = (m, i24, lanesOf) => {
    const sept24 = cost(m, s24[i24]);
    const x = { sept24_bn: sept24, general_government_response_bn: cost(m, { ...s24[i24], gg: s26[i24].gg }) - sept24,
      school_response_bn: cost(m, { ...s24[i24], school: s26[i24].school }) - sept24, responses_bn: cost(m, s26[i24]) - sept24 };
    return Object.assign(x, lanesOf(s26[i24]));
  };
  // Parts 5-6 on the case model m.
  const fromSept26 = (m, i24, i) => {
    const sept26 = cost(m, s26[i24]), atOldEnd = cost(m, MAIN_SPECS[i24]), atEnd = cost(m, MAIN_SPECS[i]);
    return { sept26_bn: sept26, school_full_cost_bn: atOldEnd - sept26, band_end_specs_bn: atEnd - atOldEnd, sept26_schools_bn: atEnd,
      change_bn: atEnd - sept26, school_line_bn: atEnd - cost(m, { ...MAIN_SPECS[i], school: 0 }) };
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
    worstAdd = Math.max(worstAdd, ...s24.map((s, k) => Math.abs(GENS.reduce((t, g) => t + cost(m24[g], s), 0) - c24[k])));
    for (const g of GENS) {
      chain[conv][g] = {};
      chain26[conv][g] = {};
      for (const [end, i24, i] of ENDS) {
        const x = toSept26(m24[g], i24, (spec) => ({ row8_bn: laneAt(conv, g, "row8_finite", spec),
          consumption_key_bn: laneAt(conv, g, "consumption_key", spec) }));
        const y = fromSept26(res[conv][g].model, i24, i);
        worstParts = Math.max(worstParts, Math.abs(x.responses_bn - x.general_government_response_bn - x.school_response_bn),
          Math.abs(PARTS24.reduce((t, k) => t + x[k], x.sept24_bn) - y.sept26_bn),
          Math.abs(PARTS26.reduce((t, k) => t + y[k], y.sept26_bn) - y.sept26_schools_bn));
        worstCase = Math.max(worstCase, Math.abs(y.sept26_schools_bn - res[conv][g].corrected[i]));
        chain[conv][g][end] = { x, y };
      }
    }
  }
  for (const [end, i24, i] of ENDS) {
    const sumOf = (conv, k) => GENS.reduce((t, g) => t + chain[conv][g][end].x[k], 0);
    const x = toSept26(u24, i24, () => ({ row8_bn: sumOf("a", "row8_bn"), consumption_key_bn: sumOf("a", "consumption_key_bn") }));
    const y = fromSept26(unionModel, i24, i);
    worstParts = Math.max(worstParts, Math.abs(x.responses_bn - x.general_government_response_bn - x.school_response_bn),
      Math.abs(PARTS24.reduce((t, k) => t + x[k], x.sept24_bn) - y.sept26_bn),
      Math.abs(PARTS26.reduce((t, k) => t + y[k], y.sept26_bn) - y.sept26_schools_bn));
    worstCase = Math.max(worstCase, Math.abs(y.sept26_schools_bn - uCost[i]));
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
  gate(`the chain's parts add to each move (September 24 -> 26${CASE === "sept26" ? "" : " -> this case"}), every generation and the union, `
    + "and end at the case's own cost", worstParts < 1e-9 && worstCase < 1e-9, `max |diff| ${e(Math.max(worstParts, worstCase))} bn`);
  gate("the generations' parts add to the union's, part by part, both conventions", worstUnion < 1e-9, `max |diff| ${e(worstUnion)} bn`);
  const ends = { low: { sept24: lo24, sept26: lo24, case: lo }, high: { sept24: hi24, sept26: hi24, case: hi } };
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
    const lane = readJson(`${MAIN}/derived/summary.json`).change;  // that lane's own change from September 26
    const worstLane = Math.max(...ENDS.map(([end], k) => Math.abs(chain.union[end].y.change_bn - lane[k])));
    gate(`the union's school_full_cost + band_end_specs equal ${MAIN}'s change from September 26`, worstLane < 1e-9,
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

// ---------------------------------------------------------------------------------------------------
const header = Object.keys(rows[0]);
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "generation_results.csv"),
  [header.join(","), ...rows.map((r) => header.map((k) => (typeof r[k] === "number" ? r[k].toFixed(6) : r[k])).join(","))].join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "generation_summary.json"), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "generation_corrections.json"), JSON.stringify({
  meta: { source: "generation_account_2026_09_24/run_generations.cjs", union: `${MAIN}/derived/corrections.json`,
    layout: "convention -> generation -> engine corrections payload (lines, edits); the three add to the union's edits" },
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
if (fails.length) {
  console.log(`✗ ${fails.length} gate(s) failed: ${fails.join("; ")}`);
  process.exit(1);
}
console.log("  ✓ all generation-run gates passed");
