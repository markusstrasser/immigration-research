/* Step 5: the adopted main case run once per generation through the explorer engine.
 *
 * Reads the adopted package read-only (main_case_2026_09_24/package.cjs: its shift lists, stack factors,
 * specifications and cost function; requiring it rewrites that lane's vendored stack file byte for byte
 * when the CPS cache is unchanged) and this lane's derived inputs:
 *   model_{G1,G2,G3plus}.json and model_b_*.json  the uncorrected model split by generation (build_models.py,
 *                                                production.py), convention (a) own generation, (b) minors
 *                                                in the parents' generation;
 *   stack_by_generation.json                     the tax-records stack by generation (stack_split.py);
 *   external_by_generation.json                  CBO, Treasury OTA and premium-credit re-keys (external_split.py);
 *   correction_rules.json                        every other lane's split (correction_rules.py).
 * Each lane's union shift list is rebuilt exactly as packageShifts() builds it (gate), then split:
 *   - the stack by the generation payloads (exact);
 *   - ratio-type changes the package multiplies by the union's stack factor (CBO, medical ratios, schools,
 *     benefits) take each generation's own change times its own stack factor, the generation's cell after
 *     the stack over before; the small remainder from that non-additivity (reported) is spread by the
 *     generations' cells after the stack, so the three add to the package's figure exactly;
 *   - the long-term-care carve-out, premium credits, OTA, justice and the lane constants by their rules.
 * The generation edits are netted per cell as correctionsPayload() nets the union's (the two fill-in
 * methods averaged), applied with Engine.applyCorrections to each generation's model, and every
 * specification of MAIN_SPECS is evaluated with the package's cost().
 * Gates (exit 1): the lanes rebuild packageShifts for both methods; every split adds to its union shift
 * (1e-9 bn); the netted generation edits add to corrections.json cell by cell (1e-9 bn); the corrected
 * union reproduces the adopted main case ($200.8752-246.3184bn, 1e-4); for every specification and both
 * conventions the three generations' costs add to the union's (linearity, 1e-9 bn; the brief's gate is
 * $0.01bn), corrected and uncorrected. For step 6 (compare_ledger.py) it also splits each generation's cost at
 * the band ends into direct fiscal lines, production term and corrections, plus the direct lines at the
 * package's proportional reference (summary.ledger_bridge_a).
 * Writes derived/generation_results.csv, derived/generation_summary.json, derived/generation_corrections.json.
 * Run from the repository root: node infra/immigration-fiscal/generation_account_2026_09_24/run_generations.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const P = require(path.join(HERE, "..", "main_case_2026_09_24", "package.cjs"));
const { Engine, MODEL, ALLOCS, SYN, SYN_LINES, MEDICAID, MAIN_SPECS, METHODS, STACKS, CENTRAL, LTSS_CENTRAL,
  both, scale, cost, expand, stackShifts, stackFactor, cboShifts, otaShifts, row1Shifts, medicalShifts,
  educationShifts, benefitShifts, justiceShifts, constantShifts, packageShifts, csvRows, readJson } = P;

const GENS = ["G1", "G2", "G3plus"];
const CONVS = ["a", "b"];
const OUT = path.join(HERE, "derived");
const load = (f) => JSON.parse(fs.readFileSync(path.join(OUT, f), "utf8"));
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
const corrections = readJson("main_case_2026_09_24/derived/corrections.json");
const adopted = readJson("main_case_2026_09_24/derived/summary.json").main_case;

// ---------------------------------------------------------------------------------------------------
// The package's union shifts, lane by lane (packageShifts at CENTRAL).
function lanes(p) {
  const O = CENTRAL;
  const edu = ["0.77", "0.82"].flatMap((w) => educationShifts(p, w, O.k).map((s) => ({ ...s, by: scale(s.by, both(0.5)) })));
  return {
    stack: stackShifts(p), cbo: cboShifts(O.year, p, { scaled: O.scaled }), ota: otaShifts("vs_audit_package_ssn_rule"),
    row1: row1Shifts(), medical: medicalShifts(p, O.medSpec, { mcbs: O.mcbs, ltss: O.ltss }), education: edu,
    benefits: benefitShifts(p, O.benefits), justice: justiceShifts(O.row7, O.booking), constants: constantShifts(O.constants),
  };
}
const LANES = ["stack", "cbo", "ota", "row1", "medical", "education", "benefits", "justice", "constants"];
const unionLanes = {};
for (const m of METHODS) {
  const p = STACKS[`row4+status_state_aware|central|${m}`];
  unionLanes[m] = lanes(p);
  const flat = LANES.flatMap((l) => unionLanes[m][l]);
  gate(`lanes rebuild packageShifts (${m})`, JSON.stringify(flat) === JSON.stringify(packageShifts(p, "central", m, CENTRAL)));
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

// options: {stackPayloads: {g: payload}, benefits: "central" | "alt_g1" | "alt_usborn", justice, row10}
function genLanes(conv, m, opts) {
  const o = Object.assign({ benefits: "central", justice: "arrest_like_custody", row10: "central", scaling: "own" }, opts || {});
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
  return G;
}

// Netted edits per generation, as correctionsPayload() nets the union's.
function netEdits(shifts) {
  const net = new Map();
  for (const x of expand(shifts)) {
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
gate("the corrected union reproduces the adopted main case", near(uCost[lo], adopted[0], 1e-4) && near(uCost[hi], adopted[1], 1e-4),
  `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)}`);
const lo0 = u0Cost.indexOf(Math.min(...u0Cost)), hi0 = u0Cost.indexOf(Math.max(...u0Cost));
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
const summary = { adopted_main_case_bn: adopted, low_spec: MAIN_SPECS[lo], high_spec: MAIN_SPECS[hi], conventions: {} };
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
      sept23_cost_bn: [r.uncorrected[lo0], r.uncorrected[hi0]],
      correction_bn: [r.corrected[lo] - r.uncorrected[lo], r.corrected[hi] - r.uncorrected[hi]],
    };
    cs[g] = out;
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      rows.push({ convention: conv, generation: g, band_end: end, allocation: MAIN_SPECS[i].allocation,
        cost_bn: r.corrected[i], sept23_same_spec_bn: r.uncorrected[i], correction_bn: r.corrected[i] - r.uncorrected[i],
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
      sept23_bn: -main0.welfare_bn,
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

// ---------------------------------------------------------------------------------------------------
const header = Object.keys(rows[0]);
fs.writeFileSync(path.join(OUT, "generation_results.csv"),
  [header.join(","), ...rows.map((r) => header.map((k) => (typeof r[k] === "number" ? r[k].toFixed(6) : r[k])).join(","))].join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "generation_summary.json"), JSON.stringify(summary, null, 1) + "\n");
fs.writeFileSync(path.join(OUT, "generation_corrections.json"), JSON.stringify({
  meta: { source: "generation_account_2026_09_24/run_generations.cjs", union: "main_case_2026_09_24/derived/corrections.json",
    layout: "convention -> generation -> engine corrections payload (lines, edits); the three add to the union's edits" },
  payloads }) + "\n");

console.log("[results] net cost to other residents at the adopted band ends ($bn a year; low = shared, high = personal)");
for (const conv of CONVS) {
  console.log(`  convention (${conv})`);
  for (const g of GENS) {
    const c = summary.conventions[conv][g];
    console.log(`    ${g.padEnd(7)} ${c.cost_bn.map((x) => x.toFixed(2)).join(" – ")}  (Sept 23 case ${c.sept23_cost_bn.map((x) => x.toFixed(2)).join(" – ")}); `
      + `per member $${c.per_member_usd.map((x) => Math.round(x)).join("–$")}, per adult $${c.per_adult_usd.map((x) => Math.round(x)).join("–$")}`);
  }
}
if (fails.length) {
  console.log(`✗ ${fails.length} gate(s) failed: ${fails.join("; ")}`);
  process.exit(1);
}
console.log("  ✓ all generation-run gates passed");
