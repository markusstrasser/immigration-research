/* The late-arrival lane's engine step: generation_account_2026_09_24/run_generations.cjs (copied at 0f22f0c),
 * lines 62-445 (setup, lane splits, netted payloads, engine gates), run on the G1 cells of frame.py, then this
 * lane's own results: every cell's cost at the union's two band ends and its parts by programme.
 *
 * Changes from the copy, and nothing else:
 *   - GENS are frame.py's nine cells (seven G1 cells, G2, G3plus); inputs come from _cache/split_<def>/
 *     (run_split.sh), --def central | lower | upper;
 *   - the two non-additive splits (a ratio-type change times each generation's own stack factor with the
 *     remainder spread by cells, and the consumption key's own-factor part) run in two levels: first over
 *     G1 (the cells summed), G2 and G3plus exactly as the generation lane does, then inside G1 by the same
 *     rule on G1's amount, so G1 is the generation lane's to rounding (verify.py);
 *   - --case sept27 (main_case_long_run_2026_09_27, the adopted case since 2026-09-27): its package exports
 *     the schools package's shift lists unchanged; its payload adds the enterprise receipt's re-key, which
 *     each cell's model gets as rekeyEdits(corrected cell model) (the package's rule for per-generation
 *     models, RESULT "For consumers" 2), and its cost() adds the capital return, keyed by each cell's own
 *     evaluation (evaluateFull);
 *   - --case sept29 | sept29_cash (the main case adopted on 2026-09-29, candidate v4's set, and the cash set beside
 *     it): the sept27 steps above, unchanged, give each cell's September 27 payload; the v4 part then goes on each
 *     cell's September 27 model by the generation lane's rules (generation_account_2026_09_24/v4_split.cjs, whose
 *     V4_LANE constant names the adopted lane). Item 3 is split in two levels by scaledSplit, as a ratio-type change:
 *     each cell's own change in the raked cells (tax_key_by_generation.json) times its own stack factor. The other
 *     inputs are this lane's own (v4_inputs.json: row-4 production, tenant shares, row-4 headcounts); run_split.sh
 *     step 7 writes both. Costs and parts come from v4_split.cjs's evaluator, and the union is gated on the case's
 *     published band (1e-4).
 * Outputs: _cache/cells_<case>_<def>.json (per cell, convention, band end: cost and programme parts).
 * Run from the repository root:
 *   node infra/immigration-fiscal/late_arrival_account_line_2026_09_27/run_cells.cjs --case sept27 --def central
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
// sept29 and sept29_cash build their September 27 part on the September 27 package; their v4 part is v4Part()'s.
const CASES = { sept27: "main_case_long_run_2026_09_27", sept26_schools: "main_case_schools_full_2026_09_26",
  sept29: "main_case_long_run_2026_09_27", sept29_cash: "main_case_long_run_2026_09_27" };
const CASE = arg("--case", "sept26_schools");
if (!CASES[CASE]) throw new Error(`--case must be one of ${Object.keys(CASES).join(", ")}`);
const ON26 = CASE !== "sept24";
const V4SET = { sept29: "set", sept29_cash: "cash" }[CASE];
const ON29 = V4SET !== undefined;
const MAIN = CASES[CASE];
const P = require(path.join(HERE, "..", MAIN, "package.cjs"));
const { Engine, MODEL, ALLOCS, SYN, SYN_LINES, MEDICAID, MAIN_SPECS, METHODS, STACKS, CENTRAL, LTSS_CENTRAL,
  both, scale, cost, expand, stackShifts, stackFactor, cboShifts, otaShifts, row1Shifts, medicalShifts,
  educationShifts, benefitShifts, justiceShifts, constantShifts, packageShifts, csvRows, readJson } = P;

const G1_CELLS = ["G1_Y_u50", "G1_Y_50_64", "G1_Y_65p", "G1_L50_50_64", "G1_L50_65p", "G1_L55_55_64", "G1_L55_65p"];
const GENS = G1_CELLS.concat(["G2", "G3plus"]);
const TOPS = ["G1", "G2", "G3plus"];
const TOP = Object.fromEntries(GENS.map((g) => [g, G1_CELLS.includes(g) ? "G1" : g]));
const DEF = arg("--def", "central");
if (!["central", "lower", "upper"].includes(DEF)) throw new Error("--def must be central, lower or upper");
const CONVS = ["a", "b"];
const IN = path.join(HERE, "_cache", `split_${DEF}`);
const OUT = path.join(HERE, "_cache");
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
    const t0 = {}, t1 = {}, d = {};
    for (const g of GENS) {
      t0[g] = cellTarget(gm[g], side, line, key, a);
      t1[g] = t0[g] + payloadDelta(gp[g], gm[g], side, line, key, a);
      d[g] = deltas[g][a];
    }
    d.G1 = G1_CELLS.reduce((s, g) => s + d[g], 0);
    const r = twoLevel(t0, t1, (g, T0, T1) => d[g] * (T0 === 0 ? 1 : T1 / T0), unionBy[a]);
    worstResidual = Math.max(worstResidual, Math.abs(r.resid));
    for (const g of GENS) out[g][a] = r.out[g];
  }
  return out;
}
// The generation lane's rule in two levels. partOf(name, t0, t1) is a group's part before the remainder, for a
// cell or (with G1's summed t0 and t1) for G1, where it must equal the rule on the summed inputs; the
// remainder is spread by t1. Level 1 over G1, G2, G3plus reproduces the generation lane; level 2 splits G1's
// amount over its cells by the same rule.
function twoLevel(t0, t1, partOf, total) {
  const T0 = { G1: 0 }, T1 = { G1: 0 };
  for (const g of G1_CELLS) { T0.G1 += t0[g]; T1.G1 += t1[g]; }
  for (const k of ["G2", "G3plus"]) { T0[k] = t0[k]; T1[k] = t1[k]; }
  const part = {};
  let sum = 0, T = 0;
  for (const k of TOPS) {
    part[k] = k === "G1" ? partOf("G1", T0.G1, T1.G1) : partOf(k, T0[k], T1[k]);
    sum += part[k];
    T += T1[k];
  }
  const resid = total - sum;
  const out = {};
  for (const k of ["G2", "G3plus"]) out[k] = part[k] + resid * T1[k] / T;
  const g1Total = part.G1 + resid * T1.G1 / T;
  let s1 = 0;
  const p1 = {};
  for (const g of G1_CELLS) { p1[g] = partOf(g, t0[g], t1[g]); s1 += p1[g]; }
  for (const g of G1_CELLS) out[g] = p1[g] + (g1Total - s1) * t1[g] / T1.G1;
  return { out, resid };
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
      const t0 = {}, t1 = {};
      for (const g of GENS) {
        t0[g] = cellTarget(gm[g], "receipt", line, null, a);
        t1[g] = t0[g] + payloadDelta(gp[g], gm[g], "receipt", line, null, a);
      }
      const R = (g) => (g === "G1" ? G1_CELLS.reduce((s, x) => s + cg[x].R_bn[line], 0) : cg[g].R_bn[line]);
      const A = (g) => (g === "G1" ? G1_CELLS.reduce((s, x) => s + cg[x].A_bn[line], 0) : cg[g].A_bn[line]);
      const r = twoLevel(t0, t1, (g, T0, T1) => (o.scaling === "union" ? ckGen.meta.phi : T1 / T0) * R(g) - A(g), ckByLine[line][a]);
      residTotal[a] += r.resid;
      for (const g of GENS) out[g][a] = r.out[g];
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
  for (const g of GENS) {
    payloads[conv][g] = payloadFor(GL[conv], g);
    if (P.rekeyEdits) {
      const m1 = Engine.applyCorrections(models[conv][g], payloads[conv][g]);
      payloads[conv][g] = { lines: payloads[conv][g].lines, edits: payloads[conv][g].edits.concat(P.rekeyEdits(m1)) };
    }
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
// sept29 / sept29_cash: the v4 part on each cell's September 27 model (v4_split.cjs), gated as the generation lane's
// run_generations_v4.cjs gates its three generations. Each cell's payload is its September 27 payload above, the
// case's national-scale edits and its own v4 tail; its production grid is its row-4 attribution.
const V = ON29 ? v4Part() : null;
function v4Part() {
  console.log("[v4 part]");
  const X = require(path.join(HERE, "..", "generation_account_2026_09_24", "v4_split.cjs"));
  const C = X.loadCase(V4SET);
  console.log(`  · ${C.rel} (adopted-case lane constant: ${X.V4_LANE})`);
  gate("v4_split.cjs runs on this package's engine and model, and the case's payload starts with its corrections.json",
    X.P === P && X.Engine === Engine && X.MODEL === MODEL && JSON.stringify(C.base) === JSON.stringify(corrections));
  const U = X.unionRun(C);
  gate("the union's items on the methods' mean model reproduce the payload's v4 part: every cell edit, receipt line and synthetic line",
    U.worst < 1e-9 && U.worstRl < 1e-12 && U.sameLines, `${U.cellsCompared} cells; max |diff| ${e(U.worst)} bn, receipt lines ${e(U.worstRl)}`);
  const models27 = Object.fromEntries(CONVS.map((c) => [c, Object.fromEntries(GENS.map((g) =>
    [g, Engine.applyCorrections(models[c][g], payloads[c][g])]))]));
  // Item 3, per fill-in method: the union's shift split by scaledSplit in two levels, each cell's own change in the
  // raked cells (national line x its share change) times its own stack factor on the line, the remainder by the cells
  // after the stack; then the methods' mean, as the payload averages them.
  const TK = load("tax_key_by_generation.json");
  const FITN = X.lineOf(MODEL, "receipts", X.FIT).national_bn;
  gate("tax_key_by_generation.json is the payload's key change on model.json's line, over this lane's nine cells",
    TK.meta.line === X.FIT && TK.meta.national_bn === FITN && JSON.stringify(TK.meta.generations) === JSON.stringify(GENS)
    && C.options.tax_key === "irs_2023_raked" && TK.meta.variant === X.V4.TAX_KEYS[C.options.tax_key]
    && ALLOCS.every((a) => TK.union[a] === X.V4.TAX.share_change[TK.meta.variant][a]), `${TK.meta.variant}, national ${FITN}`);
  SCALING = "own";
  worstResidual = 0;
  const fitBy = {};
  let worstFit = 0;
  for (const conv of CONVS) {
    const deltas = Object.fromEntries(GENS.map((g) => [g, X.byAlloc((a) => FITN * TK[conv][g][a])]));
    const per = METHODS.map((m) => {
      const ub = X.V4.taxEditOf("central", m, C.options.tax_key);
      const s = scaledSplit(ub, deltas, models[conv], stackGen.payloads[m][conv], "receipt", X.FIT, null);
      worstFit = Math.max(worstFit, ...ALLOCS.map((a) => Math.abs(GENS.reduce((t, g) => t + s[g][a], 0) - ub[a])));
      return s;
    });
    fitBy[conv] = Object.fromEntries(GENS.map((g) => [g, X.byAlloc((a) => X.sum(per.map((s) => s[g][a])) / per.length)]));
    worstFit = Math.max(worstFit, ...ALLOCS.map((a) => Math.abs(GENS.reduce((t, g) => t + fitBy[conv][g][a], 0) - U.fitBy[a])));
  }
  const fitResidual = worstResidual;
  gate("item 3: the cells' shifts add to the union's in each fill-in method and in the methods' mean", worstFit < 1e-12,
    `max |diff| ${e(worstFit)} bn; non-additive remainder spread by cells, max ${fitResidual.toFixed(4)} bn`);
  const VI = load("v4_inputs.json");
  gate("v4_inputs.json is this lane's nine cells", JSON.stringify(VI.meta.generations) === JSON.stringify(GENS));
  const grids = {};
  let worstGrid = 0;
  for (const conv of CONVS) {
    grids[conv] = Object.fromEntries(GENS.map((g) => [g, X.gridOf(C, VI.production.series[conv][g])]));
    for (const k of ["private_wtp_bn", "induced_receipts_bn"]) {
      C.production[k].forEach((v, i) => { worstGrid = Math.max(worstGrid, Math.abs(GENS.reduce((t, g) => t + grids[conv][g][k][i], 0) - v)); });
    }
  }
  gate("the cells' row-4 production grids add to the payload's in every scenario, both conventions", worstGrid < 1e-12, `max |diff| ${e(worstGrid)} bn`);
  const cellsOf = (m) => {
    const out = new Map();
    for (const l of m.receipts.lines) for (const sc of Object.keys(l.cells)) out.set(`r|${l.id}|${sc}`, l.cells[sc]);
    for (const l of m.spending.lines) for (const k of Object.keys(l.keys)) out.set(`s|${l.id}|${k}`, l.keys[k]);
    return out;
  };
  const S = {}, v4Payloads = {};
  for (const conv of CONVS) {
    S[conv] = X.split(C, { gens: GENS, top: TOP, models27: models27[conv], union: U, fitBy: fitBy[conv],
      tenant: VI.tenant_share.rule[conv], persons5: Object.fromEntries(GENS.map((g) => [g, VI.headcount[conv][g].persons_5plus])) });
    const add = X.additivity(C, GENS, S[conv].tails, U);
    gate(`(${conv}) the cells' v4 tails add to the union's: cell edits, receipt-line cells, the same lines`,
      add.edits < 1e-9 && add.receipt_lines < 1e-12 && add.sameLines, `${add.cells} cells; max |diff| ${e(add.edits)} bn, receipt lines ${e(add.receipt_lines)}`);
    v4Payloads[conv] = Object.fromEntries(GENS.map((g) => [g, X.payloadOf(C, payloads[conv][g], S[conv].tails[g], grids[conv][g])]));
    let worst = 0;
    for (const g of GENS) {
      const a1 = cellsOf(Engine.applyCorrections(models[conv][g], v4Payloads[conv][g])), b1 = cellsOf(S[conv].final[g]);
      if (a1.size !== b1.size) worst = Infinity;
      for (const [k, c] of b1) for (const a of ALLOCS) worst = Math.max(worst, Math.abs(a1.get(k)[a].target_bn - c[a].target_bn));
    }
    gate(`(${conv}) each cell's payload gives the model its item chain built`, worst < 1e-9, `max |diff| ${e(worst)} bn`);
  }
  const ev = X.evaluator(C.payload);
  const FIELDS = ["allocation", "normalization", "share", "school", "reading", "gg", "uc"];
  gate("the consumer's specifications are this package's MAIN_SPECS, in order", ev.specs.length === MAIN_SPECS.length
    && ev.specs.every((s, i) => FIELDS.every((k) => s[k] === MAIN_SPECS[i][k])));
  return { X, C, U, ev, S, fitBy, fitResidual, VI, models27, payloads: v4Payloads, O: X.oracle(C.set) };
}

// ---------------------------------------------------------------------------------------------------
console.log("[engine]");
// The case's specifications and evaluator: the package's, or under sept29 the v4 consumer's (v4Part).
const SPECS = ON29 ? V.ev.specs : MAIN_SPECS;
const CE = ON29 ? { cost: V.ev.cost, full: V.ev.evaluateFull, fw: (full) => full.state.fiscal_weight }
  : { cost, full: evaluateCase, fw: (full, m, spec) => P.stateFor(m, spec).fiscal_weight };
const unionModel = Engine.applyCorrections(MODEL, ON29 ? V.C.payload : corrections);
const uCost = SPECS.map((s) => CE.cost(unionModel, s));
const u0Cost = SPECS.map((s) => CE.cost(MODEL, s));
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
const lo0 = u0Cost.indexOf(Math.min(...u0Cost)), hi0 = u0Cost.indexOf(Math.max(...u0Cost));
if (ON29) {
  gate(`the corrected union reproduces the case's band at its end specifications (${V.O.source}, four decimals)`,
    lo === V.O.specs[0] && hi === V.O.specs[1] && near(uCost[lo], V.O.band[0], 1e-4) && near(uCost[hi], V.O.band[1], 1e-4),
    `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)} at ${lo} / ${hi}`);
  const PS = V.X.perSpec(V.C.set);
  if (PS) {
    let worst = 0;
    for (const [i, c] of PS.cost) worst = Math.max(worst, Math.abs(uCost[i] - c));
    gate(`the corrected union reproduces ${PS.source} at each of its specifications (mean of the two methods)`,
      PS.cost.size > 0 && worst < 1e-9, `${PS.cost.size} specifications; max |diff| ${e(worst)} bn`);
  }
  if (V.O.uncorrected) {
    gate(`the uncorrected union reproduces the uncorrected model at the case's responses (${V.O.source.replace(/ \(.*\)$/, "")} uncorrected_at_adopted_responses, 1e-4)`,
      near(u0Cost[lo0], V.O.uncorrected[0], 1e-4) && near(u0Cost[hi0], V.O.uncorrected[1], 1e-4), `${u0Cost[lo0].toFixed(4)}–${u0Cost[hi0].toFixed(4)}`);
  } else console.log(`  · the uncorrected model at the case's responses: ${u0Cost[lo0].toFixed(4)}–${u0Cost[hi0].toFixed(4)} (no published row)`);
} else {
  gate(`the corrected union reproduces the adopted main case${ON26 ? " (main_case_bands.csv adopted)" : ""}`,
    near(uCost[lo], gateAdopted[0], 1e-4) && near(uCost[hi], gateAdopted[1], 1e-4), `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)}`);
  gate(`the uncorrected union reproduces ${ON26 ? "the uncorrected model at the adopted responses (main_case_bands.csv)" : "the September 23 case"}`,
    near(u0Cost[lo0], gateUncorrected[0], 1e-4) && near(u0Cost[hi0], gateUncorrected[1], 1e-4),
    `${u0Cost[lo0].toFixed(4)}–${u0Cost[hi0].toFixed(4)}`);
}
const res = {};
for (const conv of CONVS) {
  res[conv] = {};
  for (const g of GENS) {
    const m0 = models[conv][g];
    const m1 = Engine.applyCorrections(m0, (ON29 ? V.payloads : payloads)[conv][g]);
    res[conv][g] = { corrected: SPECS.map((s) => CE.cost(m1, s)), uncorrected: SPECS.map((s) => CE.cost(m0, s)), model: m1 };
  }
  for (const kind of ["corrected", "uncorrected"]) {
    const ref = kind === "corrected" ? uCost : u0Cost;
    const worst = Math.max(...SPECS.map((_, i) => Math.abs(GENS.reduce((t, g) => t + res[conv][g][kind][i], 0) - ref[i])));
    gate(`(${conv}) ${kind}: the nine cells add to the union in all ${SPECS.length} specifications`, worst < 1e-9,
      `max |diff| ${e(worst)} bn (brief's gate $0.01bn)`);
  }
}
// sept29: the adopted lane's own package on every model costed here, as its other consumers call it (only once
// v4_split.cjs names the adopted lane).
const AP = ON29 ? V.X.adoptedPackage(V.C) : null;
if (AP) {
  const FIELDS = ["allocation", "normalization", "share", "school", "reading", "gg", "uc"];
  gate(`${AP.source}: its specifications are the consumer's`, AP.specs.length === SPECS.length
    && AP.specs.every((s, i) => FIELDS.every((k) => s[k] === SPECS[i][k])));
  let worst = 0;
  SPECS.forEach((_, i) => {
    worst = Math.max(worst, Math.abs(AP.cost(unionModel, i) - uCost[i]), Math.abs(AP.cost(MODEL, i) - u0Cost[i]));
    for (const conv of CONVS) for (const g of GENS) {
      worst = Math.max(worst, Math.abs(AP.cost(res[conv][g].model, i) - res[conv][g].corrected[i]),
        Math.abs(AP.cost(models[conv][g], i) - res[conv][g].uncorrected[i]));
    }
  });
  gate(`${AP.source} evaluateFull gives every model's cost here (union and cells, corrected and uncorrected, all specifications)`,
    worst < 1e-9, `max |diff| ${e(worst)} bn`);
} else if (ON29) console.log(`  · cross-check against the adopted lane's package skipped: v4_split.cjs V4_LANE is ${V.X.V4_LANE}`);
// sept29: each cell's September 27 cost at the same specifications (the September 27 package on its September 27
// model), the union's gated on the September 27 band; the change is the v4 part's.
const sept27At = ON29 ? Object.fromEntries(CONVS.map((conv) => [conv, Object.fromEntries(GENS.map((g) =>
  [g, [cost(V.models27[conv][g], MAIN_SPECS[lo]), cost(V.models27[conv][g], MAIN_SPECS[hi])]]))])) : null;
if (ON29) {
  const u27 = [cost(Engine.applyCorrections(MODEL, corrections), MAIN_SPECS[lo]), cost(Engine.applyCorrections(MODEL, corrections), MAIN_SPECS[hi])];
  let worst = 0;
  for (const conv of CONVS) for (const k of [0, 1]) worst = Math.max(worst, Math.abs(GENS.reduce((t, g) => t + sept27At[conv][g][k], 0) - u27[k]));
  gate("the cells' September 27 costs at the case's ends add to the September 27 union, which is main_case_bands.csv adopted (1e-4)",
    worst < 1e-9 && near(u27[0], gateAdopted[0], 1e-4) && near(u27[1], gateAdopted[1], 1e-4),
    `${u27.map((x) => x.toFixed(4)).join("–")}; cells max |diff| ${e(worst)} bn`);
}

// ---------------------------------------------------------------------------------------------------
// This lane's results: every cell's cost at the union's band ends, in programme parts that add to the cost.
// cost = -P - fw (receipts' effects + spending effects + F) + capital return (engine.js evaluate; evaluateFull).
// A receipt line's part is -fw x its effect (taxes paid lower the cost), a spending line's +fw x response x
// amount. Parts are grouped below; every line of the model falls in exactly one group (gate).
// sept29 adds two receipt lines: tenant_occupied_property (the property tax on rented homes, split out of
// remaining_production_property) is a property tax; housing_enterprise_surplus (public housing's operating deficit)
// falls with the other enterprise receipts in taxes_other_receipts. Its five synthetic spending lines are services.
const RECEIPT_GROUPS = {
  taxes_income: ["federal_income_tax", "state_local_income_tax"],
  taxes_payroll: ["employee_oasdi", "employee_hi", "self_employment_oasdi_hi", "employer_oasdi", "employer_hi",
    "medicare_supplementary_premiums", "other_domestic_social_contributions"],
  taxes_consumption: ["general_sales_tax", "excise_selective_sales", "customs_duties"],
  taxes_property: ["personal_property_tax", "modeled_owner_property", "remaining_production_property", "personal_motor_vehicle",
    "tenant_occupied_property"],
};
const SPENDING_GROUPS = {
  medicaid: ["medicaid_and_chip_other_medical"], medicare: ["medicare"], social_security: ["social_security"], ssi: ["ssi"],
  snap: ["snap"], refundable_tax_credits: ["refundable_tax_credits"],
  education: ["education_services", "education_benefits", SYN.school, SYN.college],
};
function groupOfReceipt(id) {
  for (const [k, ids] of Object.entries(RECEIPT_GROUPS)) if (ids.includes(id)) return k;
  return "taxes_other_receipts";
}
function groupOfSpending(row) {
  for (const [k, ids] of Object.entries(SPENDING_GROUPS)) if (ids.includes(row.id)) return k;
  if (row.response_class === "household_transfer") return "other_transfers";
  if (["public_goods", "service", "correction_constant"].includes(row.response_class) || row.id === SYN.constants) return "services_other";
  return "subsidies_interest_foreign";
}
const PROGRAMS = [...Object.keys(RECEIPT_GROUPS), "taxes_other_receipts", ...Object.keys(SPENDING_GROUPS), "other_transfers",
  "services_other", "subsidies_interest_foreign", "capital_return", "production"];
function evaluateCase(m, spec) {
  if (P.evaluateFull) return P.evaluateFull(m, spec);
  const evaluation = Engine.evaluate(m, P.stateFor(m, spec));
  return { evaluation, capital: { components: [], total_bn: 0 }, cost_bn: -evaluation.welfare_bn };
}
let partsWorst = 0;
function partsOf(m, spec) {
  const full = CE.full(m, spec);
  const ev = full.evaluation;
  const fw = CE.fw(full, m, spec);
  const out = Object.fromEntries(PROGRAMS.map((k) => [k, 0]));
  for (const r of ev.receipts) out[groupOfReceipt(r.id)] -= fw * r.effect_bn;
  for (const r of ev.spending) out[groupOfSpending(r)] -= fw * r.effect_bn;
  out.capital_return = full.capital.total_bn;
  out.production = -ev.private_wtp_bn - fw * ev.induced_receipts_bn;
  const total = PROGRAMS.reduce((s, k) => s + out[k], 0);
  partsWorst = Math.max(partsWorst, Math.abs(total - full.cost_bn), Math.abs(full.cost_bn - CE.cost(m, spec)));
  // Programme inputs beside the parts: the Medicaid line's amount and response (for the pricing check).
  const mcd = ev.spending.find((r) => r.id === MEDICAID);
  return { cost_bn: full.cost_bn, parts: out, medicaid_amount_bn: mcd.amount_bn, medicaid_response: mcd.response,
    medicaid_key: mcd.key };
}
console.log("[programme parts]");
// sept29: the lane of the adopted case and per-member figures on the row-4 headcounts (v4_inputs.json), the case's basis.
const cells = { case: CASE, main: ON29 ? V.X.V4_LANE : MAIN, def: DEF, low_spec: SPECS[lo], high_spec: SPECS[hi], lo, hi,
  union_band_bn: [uCost[lo], uCost[hi]], programs: PROGRAMS, conventions: {} };
for (const conv of CONVS) {
  cells.conventions[conv] = {};
  GENS.forEach((g, j) => {
    const m1 = res[conv][g].model;
    cells.conventions[conv][g] = {
      population: ON29 ? V.VI.headcount[conv][g].population : keyMeta.population[conv][j],
      adults: ON29 ? V.VI.headcount[conv][g].adults : keyMeta.adults_18plus[conv][j],
      own_span_bn: [Math.min(...res[conv][g].corrected), Math.max(...res[conv][g].corrected)],
      low: partsOf(m1, SPECS[lo]), high: partsOf(m1, SPECS[hi]),
    };
    if (ON29) {
      Object.assign(cells.conventions[conv][g], { sept27_cost_bn: sept27At[conv][g],
        change_from_sept27_bn: [res[conv][g].corrected[lo] - sept27At[conv][g][0], res[conv][g].corrected[hi] - sept27At[conv][g][1]] });
    }
  });
  // The union's parts from the corrected union model, against which the cells' parts must add.
  cells.conventions[conv].union = { low: partsOf(unionModel, SPECS[lo]), high: partsOf(unionModel, SPECS[hi]) };
  let worst = 0;
  for (const end of ["low", "high"]) {
    for (const k of PROGRAMS) {
      const s = GENS.reduce((t, g) => t + cells.conventions[conv][g][end].parts[k], 0);
      worst = Math.max(worst, Math.abs(s - cells.conventions[conv].union[end].parts[k]));
    }
  }
  gate(`(${conv}) every programme part: the nine cells add to the union's at both band ends`, worst < 1e-9, `max |diff| ${e(worst)} bn`);
}
gate("programme parts add to evaluateFull's cost, which is the package's cost()", partsWorst < 1e-9, `max |diff| ${e(partsWorst)} bn`);
cells.stack_scaling_remainder_max_bn = mainResidual;
cells.consumption_key_scaling_remainder_max_bn = ckMainResidual;
if (ON29) {
  const S = V.S;
  cells.v4 = { set: V.C.set, payload: V.C.rel, oracle: V.O, uncorrected_own_ends_bn: [u0Cost[lo0], u0Cost[hi0]],
    uncorrected_own_ends: [lo0, hi0], item3_scaling_remainder_max_bn: V.fitResidual,
    rules: "generation_account_2026_09_24/v4_split.cjs (the generation lane's rules, its RESULT \"v4 case (sept29)\"); item 3 in two "
      + "levels by scaledSplit; this lane's row-4 inputs (v4_inputs.json, tax_key_by_generation.json)",
    parameters: Object.fromEntries(CONVS.map((conv) => [conv, Object.fromEntries(GENS.map((g) => [g, {
      fit_by_bn: V.fitBy[conv][g], tenant_share: V.VI.tenant_share.rule[conv][g], vehicle_share: S[conv].vehicle[g],
      s_vmt: S[conv].s_vmt[g], persons_5plus: V.VI.headcount[conv][g].persons_5plus,
      pension_refs: S[conv].pension ? S[conv].pension.refs[g] : null }]))])),
    union: { fit_by_bn: V.U.fitBy, s_vmt: V.U.sbar, oasdi_bn: V.U.oasdi } };
}
const outFile = path.join(OUT, `cells_${CASE}_${DEF}.json`);
fs.writeFileSync(outFile, JSON.stringify(cells, null, 1) + "\n");
console.log(`  wrote ${path.relative(process.cwd(), outFile)}`);
if (fails.length) {
  console.log(`✗ ${fails.length} gate(s) failed: ${fails.join("; ")}`);
  process.exit(1);
}
console.log("  ✓ all gates passed");
