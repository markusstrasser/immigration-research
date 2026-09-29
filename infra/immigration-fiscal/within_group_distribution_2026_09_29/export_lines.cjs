/* Step 1: an adopted main case, line by line, for each generation at the case's two band ends.
 *
 * --case sept27 (the default): the September 27 case. Reads read-only: the case's package
 * (main_case_long_run_2026_09_27/package.cjs), the generation account's uncorrected models
 * (generation_account_2026_09_24/derived/model_{G1,G2,G3plus}.json, convention (a): everyone in their own generation)
 * and its corrections payloads (derived/generation_corrections.json, which already end with each generation's
 * enterprise re-key edits). Each generation's corrected model is evaluated with the package's evaluateFull() at the
 * union's low and high ends (specifications found as run_generations.cjs finds them: the minimum and maximum of the
 * corrected union's cost over MAIN_SPECS).
 *
 * --case sept29: the main case adopted on 2026-09-29 (SEPT29_LANE, candidate v4's set), on the generation account's
 * v4 split (derived/generation_corrections_sept29.json, run_generations_v4.cjs), evaluated with the adopted package at
 * its main profile. The cash set beside it (the pension switch off: candidate v4's cash payload and the generation
 * account's generation_corrections_sept29_cash.json) is evaluated at the same specifications, so that the switch's
 * lines split into their parts: social_security is the accrual; medicare is its benefits less the Part A share plus
 * the Part A accrual; federal_income_tax is the cash set's less the tax on benefits. Two more splits for households.py:
 * each road line (roads_vmt_*) into its driver-mile, freight and old-key pieces (candidate v4's withRoads: the line is
 * the highway national x (FP s_vmt + (1 - FP) k_cons - k_old)); and each part-rekeyed capital component into its parent
 * line's part and its correction line's part (the adopted package's keyOf). Writes _cache/sept29/lines.json.
 *
 * Both cases read capRule, each capital component's key rule, from the case's payload (meta.capital_return
 * components); on September 27 it must equal the capital lane's engine_components.json, whose rules the committed
 * outputs used.
 *
 * For every generation and end it writes each receipt and spending line (key, allocation, amount, response and
 * its cost to other residents), the production term (P, F and the specification's production dimensions) and
 * the 24 capital-return components with their key rules. households.py distributes these within each
 * generation over persons.
 * Gates (exit 1): the corrected union reproduces the case's band (September 27: $321.8194 / $387.3701bn; September 29:
 * $371.4146 / $434.8410bn and its cash set $294.7011 / $361.8175bn); each generation's rows sum to its evaluateFull()
 * cost and to the generation account's results file (1e-6 bn); the three generations sum to the union (1e-9 bn).
 * September 29 adds: the set and the cash set differ only in the three pension lines; the parts add to the payload's
 * union amounts (the accrual ratio_net x OASDI receipts, the Part A accrual, the tax on benefits; 1e-9 bn); the road
 * pieces' implied freight key is the generation's excise share before the gasoline shift (1e-9); the part-rekeyed
 * shares add to the component's key (1e-12).
 * Writes _cache/lines.json (September 27) or _cache/sept29/lines.json. Run from the repository root:
 *   node infra/immigration-fiscal/within_group_distribution_2026_09_29/export_lines.cjs [--case sept27|sept29]
 */
"use strict";
const fs = require("fs");
const path = require("path");
const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const SEPT29_LANE = "main_case_2026_09_29";
const CASES = {
  sept27: { lane: "main_case_long_run_2026_09_27", genCorrections: "generation_corrections.json",
    genResults: "generation_results.csv", band: [321.8194, 387.3701], out: "lines.json" },
  sept29: { lane: SEPT29_LANE, genCorrections: "generation_corrections_sept29.json",
    genResults: "generation_results_sept29.csv", band: [371.4146, 434.8410], out: "sept29/lines.json",
    cash: { payload: "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json",
      genCorrections: "generation_corrections_sept29_cash.json", genResults: "generation_results_sept29_cash.csv",
      band: [294.7011, 361.8175] },
    summary: "generation_summary_sept29.json" },
};
const argv = process.argv.slice(2);
const CASE = argv.includes("--case") ? argv[argv.indexOf("--case") + 1] : "sept27";
if (!CASES[CASE]) throw new Error(`--case must be one of ${Object.keys(CASES).join(", ")}`);
const C = CASES[CASE];
const V4 = CASE === "sept29";
const P = require(path.join(FISCAL, C.lane, "package.cjs"));
const { Engine, MODEL, MAIN_SPECS } = P;
const PROFILE = V4 ? P.MAIN_PROFILE : undefined;
const GEN = path.join(FISCAL, "generation_account_2026_09_24", "derived");
const GENS = ["G1", "G2", "G3plus"];
const read = (f) => JSON.parse(fs.readFileSync(f, "utf8"));
let fails = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) fails += 1;
}

const corrections = read(path.join(FISCAL, C.lane, "derived/corrections.json"));
// Each capital component's key rule, from the case's payload. The committed September 27 outputs used the capital
// lane's rules, which that payload carries unchanged.
const capRule = Object.fromEntries(corrections.meta.capital_return.components.map((c) => [c.id, c.key]));
if (!V4) {
  const CAP = read(path.join(FISCAL, "capital_return_services_2026_09_27/derived/engine_components.json"));
  gate("the payload's capital key rules are the capital lane's (engine_components.json)",
    JSON.stringify(capRule) === JSON.stringify(Object.fromEntries(CAP.components.map((c) => [c.id, c.key]))),
    `${Object.keys(capRule).length} components`);
} else {
  gate("the adopted package's payload is its derived/corrections.json", JSON.stringify(P.correctionsPayload()) === JSON.stringify(corrections));
}
const unionModel = V4 ? P.payloadModel() : Engine.applyCorrections(MODEL, corrections);
const uCost = MAIN_SPECS.map((s) => P.evaluateFull(unionModel, s, PROFILE).cost_bn);
const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
gate("the corrected union reproduces the adopted case", Math.abs(uCost[lo] - C.band[0]) < 1e-4 && Math.abs(uCost[hi] - C.band[1]) < 1e-4,
  `${uCost[lo].toFixed(4)}–${uCost[hi].toFixed(4)} at specifications ${lo} / ${hi} (0-based)`);

function resultsOf(file) {
  const results = fs.readFileSync(path.join(GEN, file), "utf8").trim().split("\n");
  const head = results[0].split(",");
  const out = {};
  for (const row of results.slice(1)) {
    const r = Object.fromEntries(row.split(",").map((v, i) => [head[i], v]));
    if (r.convention === "a") out[`${r.generation}|${r.band_end}`] = Number(r.cost_bn);
  }
  return out;
}
const pay = read(path.join(GEN, C.genCorrections)).payloads.a;
const published = resultsOf(C.genResults);

function dump(m, spec) {
  const full = P.evaluateFull(m, spec, PROFILE);
  const state = V4 ? P.stateFor(m, spec, PROFILE) : P.stateFor(P.withSyntheticLines ? P.withSyntheticLines(m) : m, spec);
  const ev = full.evaluation, fw = state.fiscal_weight;
  const rows = [];
  for (const r of ev.receipts) {
    rows.push({ side: "receipt", id: r.id, key: r.key, scenario: state.receipt_scenario, group: r.group,
      response_class: r.response_class, amount_bn: r.amount_bn, response: r.response, cost_bn: -fw * r.effect_bn });
  }
  for (const r of ev.spending) {
    rows.push({ side: "spending", id: r.id, key: r.key, group: r.group, response_class: r.response_class,
      amount_bn: r.amount_bn, response: r.response, cost_bn: -fw * r.effect_bn });
  }
  const capital = full.capital.components.map((c) => ({ id: c.id, part: c.group, level: c.level, rule: capRule[c.id],
    key: c.key, response: c.response, cost_bn: c.return_bn }));
  if (V4) {
    // A part-rekeyed component's key is its parent line's share plus its correction line's amount over the part's
    // national total (the adopted package's keyOf); households.py spreads the return in those two parts.
    for (const c of capital) {
      if (c.rule.kind !== "part_rekeyed") continue;
      const parent = ev.spending.find((l) => l.id === c.rule.parent_line), part = ev.spending.find((l) => l.id === c.rule.correction_line);
      c.shares = { parent: parent.amount_bn / parent.national_bn, part: part.amount_bn / c.rule.part_national_bn };
      if (Math.abs(c.shares.parent + c.shares.part - c.key) > 1e-12) throw new Error(`[BLOCKED] ${c.id}: its two parts do not add to its key`);
    }
  }
  const production = { dims: state.production, count: state.count_production, fiscal_weight: fw,
    private_wtp_bn: ev.private_wtp_bn, induced_receipts_bn: ev.induced_receipts_bn,
    cost_bn: -(ev.private_wtp_bn + fw * ev.induced_receipts_bn) };
  const sum = rows.reduce((a, r) => a + r.cost_bn, 0) + capital.reduce((a, c) => a + c.cost_bn, 0) + production.cost_bn;
  return { cost_bn: full.cost_bn, sum_bn: sum, allocation: state.allocation, receipt_scenario: state.receipt_scenario,
    rows, capital, production };
}

const out = { meta: { case: C.lane, convention: "a", spec_index: { low: lo, high: hi },
  specs: { low: MAIN_SPECS[lo], high: MAIN_SPECS[hi] } }, union: {}, generations: {} };
for (const [end, i] of [["low", lo], ["high", hi]]) {
  out.union[end] = dump(unionModel, MAIN_SPECS[i]);
  gate(`union ${end}: rows sum to the cost`, Math.abs(out.union[end].sum_bn - out.union[end].cost_bn) < 1e-9,
    `${out.union[end].sum_bn.toFixed(6)} vs ${out.union[end].cost_bn.toFixed(6)}`);
}
const models = {};
for (const g of GENS) {
  const m0 = read(path.join(GEN, `model_${g}.json`));
  const m1 = Engine.applyCorrections(m0, pay[g]);
  models[g] = { m0, m1 };
  out.generations[g] = {};
  for (const [end, i] of [["low", lo], ["high", hi]]) {
    const d = dump(m1, MAIN_SPECS[i]);
    out.generations[g][end] = d;
    gate(`${g} ${end}: rows sum to evaluateFull() and to ${C.genResults}`,
      Math.abs(d.sum_bn - d.cost_bn) < 1e-9 && Math.abs(d.cost_bn - published[`${g}|${end}`]) < 1e-6,
      `${d.cost_bn.toFixed(6)} vs ${published[`${g}|${end}`]}`);
  }
}
for (const end of ["low", "high"]) {
  const s = GENS.reduce((a, g) => a + out.generations[g][end].cost_bn, 0);
  gate(`${end}: the three generations add to the union`, Math.abs(s - out.union[end].cost_bn) < 1e-9, `${s.toFixed(6)}`);
}

if (V4) {
  const V = P.V4PKG;
  const PA = corrections.meta.pension_accrual;
  const SUM = read(path.join(GEN, C.summary));
  const ALLOC = { low: MAIN_SPECS[lo].allocation, high: MAIN_SPECS[hi].allocation };
  gate("the payload's OASDI lines are candidate v4's", JSON.stringify(PA.oasdi_lines) === JSON.stringify(V.OASDI_LINES), PA.oasdi_lines.join(", "));
  out.meta.pension_accrual = { ratio_net: PA.ratio_net, part_a_share: PA.part_a_share, se_oasdi_share: PA.se_oasdi_share,
    part_a_accrual_bn: PA.part_a_accrual_bn, benefit_tax_receipt_bn: PA.benefit_tax_receipt_bn, oasdi_lines: PA.oasdi_lines,
    hi_lines: V.HI_LINES, se_line: PA.se_line };
  out.meta.roads = { highway_national_bn: V.HWY_N, passenger_share: V.FP, gasoline_bn: V.GAS, reference_scenario: V.REF };

  // The cash set at the same specifications: the pension switch's parts.
  console.log("[cash set: the pension switch's parts]");
  const PC = P.forPayload(read(path.join(FISCAL, C.cash.payload)));
  const uCash = [lo, hi].map((i) => PC.evaluateFull(PC.payloadModel(), MAIN_SPECS[i], PROFILE).cost_bn);
  gate("the cash set's union reproduces its band at the same specifications (1e-4)",
    Math.abs(uCash[0] - C.cash.band[0]) < 1e-4 && Math.abs(uCash[1] - C.cash.band[1]) < 1e-4, `${uCash[0].toFixed(7)} / ${uCash[1].toFixed(7)}`);
  out.meta.cash_set = { payload: C.cash.payload, cost_bn: { low: uCash[0], high: uCash[1] } };
  const payCash = read(path.join(GEN, C.cash.genCorrections)).payloads.a;
  const cashResults = resultsOf(C.cash.genResults);
  const PENSION = new Set(["receipt|federal_income_tax", "spending|social_security", "spending|medicare"]);
  const tot = { accrual: [0, 0], part_a: [0, 0], benefit_tax: [0, 0] };
  const cashSum = [0, 0];
  for (const g of GENS) {
    const mc = Engine.applyCorrections(models[g].m0, payCash[g]);
    for (const [j, [end, i]] of [["low", lo], ["high", hi]].entries()) {
      const fc = PC.evaluateFull(mc, MAIN_SPECS[i], PROFILE);
      cashSum[j] += fc.cost_bn;
      const setRows = out.generations[g][end].rows;
      const cashRows = fc.evaluation.receipts.map((r) => ["receipt", r]).concat(fc.evaluation.spending.map((r) => ["spending", r]));
      const byId = new Map(cashRows.map(([side, r]) => [`${side}|${r.id}`, r]));
      const moved = setRows.filter((r) => { const c = byId.get(`${r.side}|${r.id}`); return !c || c.key !== r.key || Math.abs(c.amount_bn - r.amount_bn) > 1e-12; })
        .map((r) => `${r.side}|${r.id}`);
      const capSame = fc.capital.components.every((c, q) => Math.abs(c.return_bn - out.generations[g][end].capital[q].cost_bn) < 1e-12);
      const prodSame = fc.evaluation.private_wtp_bn === out.generations[g][end].production.private_wtp_bn
        && fc.evaluation.induced_receipts_bn === out.generations[g][end].production.induced_receipts_bn;
      gate(`${g} ${end}: the set and the cash set differ only in the three pension lines`,
        moved.length === 3 && moved.every((k) => PENSION.has(k)) && capSame && prodSame && byId.size === setRows.length,
        moved.join(", "));
      gate(`${g} ${end}: the cash set's cost is ${C.cash.genResults}'s (1e-6 bn)`, Math.abs(fc.cost_bn - cashResults[`${g}|${end}`]) < 1e-6,
        `${fc.cost_bn.toFixed(6)} vs ${cashResults[`${g}|${end}`]}`);
      const setOf = (side, id) => setRows.find((r) => r.side === side && r.id === id);
      const ss = setOf("spending", "social_security"), med = setOf("spending", "medicare"), fit = setOf("receipt", "federal_income_tax");
      const medCash = byId.get("spending|medicare").amount_bn, fitCash = byId.get("receipt|federal_income_tax").amount_bn;
      const pension = { accrual_bn: ss.amount_bn, medicare_benefits_bn: (1 - PA.part_a_share) * medCash,
        part_a_accrual_bn: med.amount_bn - (1 - PA.part_a_share) * medCash, fit_cash_bn: fitCash, benefit_tax_bn: fitCash - fit.amount_bn,
        keys: { social_security: ss.key, medicare: med.key, federal_income_tax: fit.key } };
      out.generations[g][end].pension = pension;
      tot.accrual[j] += pension.accrual_bn;
      tot.part_a[j] += pension.part_a_accrual_bn;
      tot.benefit_tax[j] += pension.benefit_tax_bn;
    }
  }
  for (const [j, end] of ["low", "high"].entries()) {
    const a = ALLOC[end];
    const rows = out.union[end].rows;
    const amt = (id) => rows.find((r) => r.side === "receipt" && r.id === id).amount_bn;
    const oasdi = PA.oasdi_lines.reduce((s, id) => s + amt(id), 0) + PA.se_oasdi_share * amt(PA.se_line);
    gate(`${end}: the three generations' cash sets add to the union's (1e-9 bn)`, Math.abs(cashSum[j] - uCash[j]) < 1e-9, `${cashSum[j].toFixed(6)}`);
    gate(`${end}: the generations' accruals add to ratio_net x the union's OASDI receipts (1e-9 bn)`,
      Math.abs(tot.accrual[j] - PA.ratio_net * oasdi) < 1e-9, `${tot.accrual[j].toFixed(6)} vs ${(PA.ratio_net * oasdi).toFixed(6)}`);
    gate(`${end}: the generations' Part A accruals add to part_a_accrual_bn (1e-9 bn)`, Math.abs(tot.part_a[j] - PA.part_a_accrual_bn) < 1e-9,
      `${tot.part_a[j].toFixed(6)}`);
    gate(`${end}: the generations' tax on benefits adds to benefit_tax_receipt_bn.${a} (1e-9 bn)`,
      Math.abs(tot.benefit_tax[j] - PA.benefit_tax_receipt_bn[a]) < 1e-9, `${tot.benefit_tax[j].toFixed(6)}`);
  }

  // Roads: each generation's road line in its three pieces, with the driver-mile share from the generation account.
  console.log("[road lines: driver-mile, freight and old-key pieces]");
  const EXCISE = "excise_selective_sales", EA = "economic_affairs_services";
  for (const g of GENS) {
    const m1 = models[g].m1;
    const ea = m1.spending.lines.find((l) => l.id === EA), ex = m1.receipts.lines.find((l) => l.id === EXCISE);
    for (const [end, i] of [["low", lo], ["high", hi]]) {
      const a = MAIN_SPECS[i].allocation;
      const svmt = SUM.rules.parameters.a[g].s_vmt[a];
      const kOld = ea.keys[ea.preferred_key][a].target_bn / ea.national_bn;
      // The final excise cell carries the gasoline shift GAS (s_vmt - k_cons) on the pre-roads cell k_cons x national.
      const kCons = (ex.cells[V.REF][a].target_bn - V.GAS * svmt) / (ex.national_bn - V.GAS);
      const rows = out.generations[g][end].rows;
      const eaRow = rows.find((r) => r.side === "spending" && r.id === EA);
      const roads = {};
      for (const [lvl, id] of [["sl", "roads_vmt_sl"], ["fed", "roads_vmt_fed"]]) {
        const r = rows.find((x) => x.side === "spending" && x.id === id);
        const N = V.HWY_N[lvl];
        const pieces = { driver_miles_bn: N * V.FP * svmt, old_key_bn: -N * kOld };
        pieces.freight_bn = r.amount_bn - pieces.driver_miles_bn - pieces.old_key_bn;
        const implied = pieces.freight_bn / (N * (1 - V.FP));
        gate(`${g} ${end} ${id}: the freight piece's key is the generation's excise share before the gasoline shift (1e-9)`,
          Math.abs(implied - kCons) < 1e-9, `${implied.toFixed(12)} vs ${kCons.toFixed(12)}`);
        roads[id] = Object.assign(pieces, { freight_key: ex.cells[V.REF][a].key || null, old_key: ea.preferred_key, s_vmt: svmt });
      }
      gate(`${g} ${end}: economic_affairs_services is evaluated at its preferred key`, eaRow.key === ea.preferred_key, `${eaRow.key}`);
      out.generations[g][end].roads = roads;
    }
  }
}
fs.mkdirSync(path.dirname(path.join(HERE, "_cache", C.out)), { recursive: true });
fs.writeFileSync(path.join(HERE, "_cache", C.out), JSON.stringify(out, null, 1) + "\n");
if (fails) { console.log(`✗ ${fails} gate(s) failed`); process.exit(1); }
console.log("  ✓ all export gates passed");
