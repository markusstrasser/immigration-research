/* Added-person unit age prices on v7, at fixed specifications 16 / 11.
 * Runs no upstream writer. Private age functions are loaded from unmodified source.
 * Child credits and white income-key residual inherit the case's fixed per-member
 * rule; no new age profile is invented for those residuals.
 * CLI: node added_band_prices.cjs --out <this lane>/derived/added_band_prices.json
 */
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto"), Module = require("module");
const FISCAL = path.resolve(__dirname, "..");
const clone = (x) => JSON.parse(JSON.stringify(x));
const block = (s) => { throw Error(`[BLOCKED] added_band_prices: ${s}`); };
const used = new Set();
function read(rel) {
  used.add(rel);
  return JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
}
function ageInternals() {
  const rel = "main_case_2026_10_07/item_age_mix.cjs", file = path.join(FISCAL, rel);
  used.add(rel);
  const m = new Module(file, module);
  m.filename = file; m.paths = Module._nodeModulePaths(path.dirname(file));
  m._compile(fs.readFileSync(file, "utf8") + "\nmodule.exports.unitInternals = { g3ModelKeys, wModel, cellMap };\n", file);
  return m.exports.unitInternals;
}
const line = (m, side, id) => {
  const l = m[side === "receipt" ? "receipts" : "spending"].lines.find((x) => x.id === id);
  if (!l) block(`no ${side} line ${id}`);
  return l;
};
function cell(m, side, id, at) {
  const l = line(m, side, id);
  return side === "receipt" ? l.cells[at || m.receipts.reference] : l.keys[at || l.preferred_key];
}
function shift(m, side, id, at, by) {
  const c = cell(m, side, id, at);
  for (const a of ["personal", "shared"]) c[a].target_bn += by[a];
}
function receiptShift(P, m, id, by) {
  for (const e of P.V6_PACKAGE.expand([{ side: "receipt", line: id, by }])) shift(m, "receipt", id, e.scenario, e.by);
}
function buildPrices() {
  const P = require(path.join(FISCAL, "main_case_2026_10_14/package.cjs"));
  const AI = ageInternals(), E = P.Engine;
  const MIX = read("added_age_mix_2026_10_07/derived/age_mix.json");
  const BL = read("added_age_mix_2026_10_07/derived/band_lines.json");
  const AK = read("added_age_mix_2026_10_07/derived/g3_age_keys.json");
  const SI = read(P.ROW4.FILES.state_index), R4 = P.ROW4.INPUTS;
  const gen = "generation_account_2026_09_24/derived/";
  const G0 = read(gen + "model_G3plus.json");
  const G = Object.fromEntries(["set", "cash"].map((w) => [w, E.applyCorrections(G0,
    read(gen + `generation_corrections_sept29${w === "cash" ? "_cash" : ""}.json`).payloads.a.G3plus)]));
  const I = { AK, BL, PI0: MIX.meta.identified, PENSION: P.SEPT29.correctionsPayload().meta.pension_accrual,
    gcashCells: AI.cellMap(G.cash), ZERO_PROFILE: [] };
  const base = { set: P.SEPT29.payloadModel(), cash: P.SEPT29_CASH.payloadModel() };
  const X = Object.fromEntries(["set", "cash"].map((w) => [w, { name: w, U: base[w], G: G[w], gCells: AI.cellMap(G[w]), NG: P.POP.meta.g3_account }]));
  const payload = { set: P.correctionsPayload(), cash: P.CASH.correctionsPayload() };
  const ape = P.OCT07.correctionsPayload().meta.pension_accrual;
  const full6 = { set: P.OCT07.payloadModel(), cash: P.OCT07.CASH.payloadModel() };
  const byA = (f) => Object.fromEntries(["personal", "shared"].map((a) => [a, f(a)]));
  const sumTotal = (c, a) => c[a].target_bn + c[a].other_bn;
  // The white library multiplies state indices by line-use keys. Pricing each
  // age band separately and summing those products need not recover pricing the
  // whole mix. Attribute the four products proportionately across the original
  // unit-band profiles, conserving the case's original per-line amounts exactly.
  // Applying this attribution at a new mix freezes the reference calibration;
  // that is an explicit assumption, not a new nonlinear white-library run.
  const productLines = ["receipts|personal_motor_vehicle", "receipts|general_sales_tax",
    "spending|state_price_public_order_safety", "spending|state_price_health_services"];
  const whiteCalibration = {};
  for (const basis of ["accrual", "cash"]) {
    const refMix = BL.mixes["cross_section_2007_2026|g3_rate"];
    whiteCalibration[basis] = {};
    for (const id of Object.keys(refMix.white[basis].lines)) {
      const sum = BL.meta.bands.reduce((s, _, b) => s + refMix.pi[b] * BL.mixes[`band|${b}`].white[basis].lines[id], 0);
      const want = refMix.white[basis].lines[id];
      if (!productLines.includes(id) && Math.abs(sum - want) > 1e-12) block(`unaccounted nonadditive white line ${id}`);
      if (productLines.includes(id)) whiteCalibration[basis][id] = { original_bn_per_person: want,
        raw_bands_bn_per_person: sum, factor: sum === 0 ? 1 : want / sum };
    }
  }
  // Keep raw unit models for row4's set/cash contrasts. Transformations act only
  // on their target amounts; nationals and denominators come from the full case.
  function transform(raw, kind, w) {
    const m = clone(raw[w]), u = raw[w];
    if (w === "set") {
      shift(m, "spending", "social_security", null, byA((a) => cell(u, "spending", "social_security")[a].target_bn * (ape.lineage_factors.f_ss - 1)));
      shift(m, "spending", "medicare", null, byA((a) => (cell(raw.set, "spending", "medicare")[a].target_bn
        - (1 - ape.part_a_share) * cell(raw.cash, "spending", "medicare")[a].target_bn) * (ape.lineage_factors.f_pa - 1)));
    }
    for (const e of payload[w].edits.filter((e) => e.national_bn !== undefined)) {
      const l = line(m, e.side, e.line), f = e.national_bn / l.national_bn;
      for (const c of Object.values(e.side === "receipt" ? l.cells : l.keys)) for (const a of ["personal", "shared"]) c[a].target_bn *= f;
      l.national_bn = e.national_bn;
    }
    if (kind === "g3") {
      const rec = payload[w].meta.items.find((r) => r.id === "child_credits");
      const n = P.ITEM_DETAIL.added_age_mix.counts.later + (1 - MIX.meta.c3) * P.ITEM_DETAIL.added_age_mix.counts.g3_rate;
      for (const [name, part] of Object.entries(rec.parts)) if (name.startsWith("lineage_g3plus:")) {
        const e = payload[w].edits[rec.edits.first + part.edit];
        shift(m, e.side, e.line, e.scenario || e.key, byA((a) => part.by[a] / n));
      }
    }
    const jb = P.JOBCAP.CENTRAL, wage = cell(u, "receipt", "corporate_labor");
    const wageTotal = cell(full6[w], "receipt", "corporate_labor");
    for (const id of P.JOBCAP.LINES) {
      const group = P.JOBCAP.GROUP_OF[id], l = line(full6[w], "receipt", id);
      const nat = P.JOBCAP.GROUPS[group].reduce((s, k) => s + line(full6[w], "receipt", k).national_bn, 0);
      for (const sc of Object.keys(l.cells)) for (const a of ["personal", "shared"]) {
        cell(m, "receipt", id, sc)[a].target_bn = wage[a].target_bn / sumTotal(wageTotal, a)
          * jb.factor[kind === "g3" ? "G3plus" : "white_nh"][group][a] * jb.lines[group].national_bn * sumTotal(l.cells[sc], a) / nat;
      }
    }
    if (kind === "white") receiptShift(P, m, "federal_income_tax", byA((a) => -P.ROW4.W_ROWS[w][a].bn / P.ROW4.W_CASE));
    if (w === "set") {
      if (kind === "g3") {
        const ss = cell(raw.set, "spending", "social_security"), med = cell(raw.set, "spending", "medicare"), cashmed = cell(raw.cash, "spending", "medicare");
        shift(m, "spending", "medicare", null, byA((a) => (med[a].target_bn - (1 - ape.part_a_share) * cashmed[a].target_bn) * R4.fPA0 * R4.delta_part_a[a]));
        shift(m, "spending", "social_security", null, byA((a) => ss[a].target_bn * (R4.fSS4 * R4.delta_ss[a] + R4.fSS4 - R4.fSS0)));
      } else shift(m, "spending", "social_security", null, byA((a) => cell(raw.set, "spending", "social_security")[a].target_bn * (R4.fSS4 - R4.fSS0)));
      receiptShift(P, m, "federal_income_tax", byA((a) => (cell(raw.set, "receipt", "federal_income_tax")[a].target_bn
        - cell(raw.cash, "receipt", "federal_income_tax")[a].target_bn) * (kind === "g3" ? R4.national_key_ratio[a] - 1 : R4.white_rule3_ratio - 1)));
    }
    if (kind === "g3") {
      for (const id of Object.keys(SI.lines)) {
        const syn = `state_price_${id}`;
        shift(m, "spending", syn, "k", byA((a) => cell(u, "spending", syn, "k")[a].target_bn * (SI.lines[id].ratio - 1)));
      }
      for (const id of ["general_sales_tax", "personal_motor_vehicle"]) receiptShift(P, m, id, byA((a) => {
        const x = SI.receipts[id]; return (x.factor_row4 - x.factor_published) * cell(u, "receipt", id)[a].target_bn / (1 + x.factor_published);
      }));
      shift(m, "receipt", "modeled_owner_property", m.receipts.reference,
        byA((a) => cell(u, "receipt", "modeled_owner_property")[a].target_bn * (R4.owner_national_ratio - 1)));
    }
    return m;
  }
  const ends = [16, 11], bases = {}, baseCosts = {};
  for (const w of ["set", "cash"]) {
    const q = w === "set" ? P : P.CASH;
    bases[w] = P.METHODS.map((method) => q.modelFor("central", method, q.withCentral({})));
    baseCosts[w] = bases[w].map((m) => ends.map((i) => q.evaluateFull(m, P.MAIN_SPECS[i], P.MAIN_PROFILE).cost_bn));
  }
  function costs(m, w) {
    const q = w === "set" ? P : P.CASH;
    const edits = P.AGE_MIX.cellsOf(m).map((c) => ({ side: c.side, line: c.line,
      [c.side === "receipt" ? "scenario" : "key"]: c.scenario || c.key,
      by: byA((a) => c.cell[a].target_bn * 1e6) }));
    return ends.map((i, j) => P.METHODS.reduce((s, _, k) => {
      const b = bases[w][k], bumped = E.applyCorrections(b, { edits, meta: b.corrections });
      for (const f of ["private_wtp_bn", "induced_receipts_bn"]) bumped.production[f] = b.production[f].map((x, z) => x + 1e6 * m.production[f][z]);
      return s + (q.evaluateFull(bumped, P.MAIN_SPECS[i], P.MAIN_PROFILE).cost_bn - baseCosts[w][k][j]) / P.METHODS.length / 1e6;
    }, 0));
  }
  const bands = BL.meta.bands;
  const rates = bands.map((band, b) => {
    const unit = (kind, calibrated = true) => {
      const raw = Object.fromEntries(["set", "cash"].map((w) => [w, kind === "g3" ? AI.g3ModelKeys(I, X[w], `band|${b}`) : AI.wModel(I, X[w], `band|${b}`)]));
      if (kind === "white" && calibrated) for (const w of ["set", "cash"]) for (const [id, cal] of Object.entries(whiteCalibration[w === "set" ? "accrual" : "cash"])) {
        const [side, name] = id.split("|"), l = line(raw[w], side === "receipts" ? "receipt" : side, name);
        for (const c of Object.values(side === "receipts" ? l.cells : l.keys)) for (const a of ["personal", "shared"]) c[a].target_bn *= cal.factor;
      }
      const models = Object.fromEntries(["set", "cash"].map((w) => [w, transform(raw, kind, w)]));
      return { rates: Object.fromEntries(["set", "cash"].map((w) => [w, costs(models[w], w)])), models };
    };
    const g3Unit = unit("g3"), g3 = g3Unit.rates, white = unit("white").rates, whiteRaw = unit("white", false).rates;
    const credit = P.CREDITS.LINEAGE ? P.CREDITS.R.I.lineage.g3plus_per_member_usd / 1e9 : 0;
    const g3NoCredit = Object.fromEntries(["set", "cash"].map((w) => [w, g3[w].map((x) => x - credit)]));
    const blend = Object.fromEntries(["set", "cash"].map((w) => [w, g3[w].map((x, e) => (1 - MIX.meta.c3) * x + MIX.meta.c3 * white[w][e])]));
    const rawBlend = Object.fromEntries(["set", "cash"].map((w) => [w, g3[w].map((x, e) => (1 - MIX.meta.c3) * x + MIX.meta.c3 * whiteRaw[w][e])]));
    const fallback = Object.fromEntries(["tenant_occupied_property", "lane_constants"].map((id) => [id,
      Object.fromEntries(["set", "cash"].map((w) => {
        const m = clone(g3Unit.models[w]);
        for (const c of P.AGE_MIX.cellsOf(m)) if (c.line !== id) for (const a of ["personal", "shared"]) c.cell[a].target_bn = 0;
        for (const f of ["private_wtp_bn", "induced_receipts_bn"]) m.production[f].fill(0);
        return [w, costs(m, w)];
      }))]));
    return { band, lower_age: b * 5, g3_bn_per_person: g3, g3_without_child_credits_bn_per_person: g3NoCredit,
      white_bn_per_person: white, white_raw_bn_per_person: whiteRaw, c3_blend_bn_per_person: blend,
      c3_blend_raw_bn_per_person: rawBlend, g3_fallback_line_bn_per_person: fallback };
  });
  const oracle = read("main_case_2026_10_14/derived/lineage_addition.json"), gates = [];
  for (const w of ["set", "cash"]) for (const part of ["later", "g3_rate"]) {
    const mix = MIX.readings.cross_section_2007_2026[part], n = MIX.meta[part];
    const key = part === "later" ? "g3_bn_per_person" : "c3_blend_bn_per_person";
    const got = ends.map((_, e) => rates.reduce((s, r, b) => s + n * mix[b] * r[key][w][e], 0));
    const want = oracle[w].parts[part].cost_bn;
    const gap = Math.max(...got.map((x, e) => Math.abs(x - want[e])));
    gates.push({ name: `original ${w} ${part} at fixed responses`, got_bn: got, want_bn: want, max_gap_bn: gap, pass: gap < 1e-6 });
  }
  const rawControl = Object.fromEntries(["set", "cash"].map((w) => {
    const pi = MIX.readings.cross_section_2007_2026.g3_rate, n = MIX.meta.g3_rate;
    const got = ends.map((_, e) => rates.reduce((s, r, b) => s + n * pi[b] * r.c3_blend_raw_bn_per_person[w][e], 0));
    return [w, { got_bn: got, want_bn: oracle[w].parts.g3_rate.cost_bn,
      gap_bn: got.map((x, e) => x - oracle[w].parts.g3_rate.cost_bn[e]) }];
  }));
  if (gates.some((g) => !g.pass)) block(JSON.stringify(gates));
  for (const rel of ["union_completion_2026_10_14/added_band_prices.cjs", "main_case_2026_10_07/package.cjs", "main_case_2026_10_14/package.cjs", "main_case_2026_10_14/item_job_capital.cjs",
    "main_case_2026_10_14/item_child_credits.cjs", "main_case_2026_10_14/item_row4.cjs", "main_case_2026_10_14/derived/corrections.json", "main_case_2026_10_14/derived/corrections_cash.json"]) used.add(rel);
  for (const rel of [P.CREDITS.S.file, P.JOBCAP.S.file, P.ROW4.FILES.limits, ...Object.keys(P.ROW4.SOURCES_8.files)]) used.add(rel);
  const hashes = Object.fromEntries([...used].sort().map((rel) => [rel, crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex")]));
  return { meta: { source: "union_completion_2026_10_14/added_band_prices.cjs", ends, c3: MIX.meta.c3,
    rule: "unit-band added-person cells on v7, increment evaluated on the full case at fixed responses; pure G3, pure white, and the case C3 blend",
    approximations: ["The case child-credit residual is fixed per G3-priced person, without an age profile.",
      "The case white income-key residual is fixed per white-priced person at its original age mix (item_row4 buildWhite).",
      "[ASSUMPTION] Four nonadditive white state-index products are attributed proportionately across unit-band profiles, calibrated to conserve the original case mix per-line amount; new ages retain that calibration."],
    white_state_product_calibration: whiteCalibration, child_credit_bn_per_g3_person: P.CREDITS.LINEAGE ? P.CREDITS.R.I.lineage.g3plus_per_member_usd / 1e9 : 0,
    raw_white_positive_control_before_calibration: rawControl, hashes }, rates, gates };
}
module.exports = { buildPrices };
if (require.main === module) {
  const ix = process.argv.indexOf("--out");
  if (ix < 0 || !process.argv[ix + 1]) block("explicit --out is required");
  const out = path.resolve(process.argv[ix + 1]);
  if (!out.startsWith(path.resolve(__dirname, "derived") + path.sep) && !out.startsWith(path.resolve(__dirname, "_cache") + path.sep)) block("output must be in this lane's derived/ or _cache/");
  const result = buildPrices(); fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify(result, null, 2) + "\n");
  console.log(`${result.gates.length} gates passed; wrote ${out}`);
}
