/* G4, the API: consumers' call patterns, as they are written, run against this package in a harness inside the lane (so
 * the lane's reruns repeat it). Each pattern cites its consumer and repeats its calls and gates on this lane's package
 * and derived files, as a path swap would run them:
 *   1. distribution_weights_2026_09_23/case_ends.cjs:63-94, the package's own models (modelFor, withCentral, MAIN_SPECS,
 *      evaluateFull), plus the production block a peer's uncommitted edit adds (stateFor's production cell,
 *      Engine.productionIndex, the payload grid's P and F, cost = -(P + F) - A);
 *   2. uncertainty_propagation_2026_09_22/sept24_specs.cjs:94-150, capitalCase: its own models, model.json uncorrected
 *      and the payload applied by the consumer, at MAIN_SPECS; the specification-field gate; componentsFor(null) and
 *      the capital-return derivatives;
 *   3. world_ledger_2026_09_27/generation_lines.cjs:57-66 (run_generations.cjs partsAt()): its own models, the
 *      generation lane's per-generation models at the September 27 generation pin (8654a0c, pins.json), read with git
 *      show. Oracle: the generations add to the whole group, first under the September 27 package, then under this one;
 *      and forPayload() of the September 27 payload on that pin's corrected generation models is the September 27
 *      package, exactly;
 *   4. winners_losers_2026_09_24/specs.cjs:130-160: two cases, each payload applied by the consumer, the previous case
 *      through the package's SEPT27 (as the sept27 entry uses PSCHOOLS); RESPONSES; evaluateFull(m, spec) with no profile;
 *   5. main_case_decomposition_2026_09_29/decompose.cjs:74-82, 177-178, 356-373: correctionsPayload(), the union with no
 *      profile, componentsFor(spec.capital_variant), SYN, SYN_LINES, CONSTANTS and RESPONSES.row8_factor;
 *   6. within_group_distribution_2026_09_29/export_lines.cjs:37-73: dump(): evaluateFull and stateFor(withSyntheticLines(m),
 *      spec), the rows adding to the cost, on the union and on the generation models;
 *   7. sept24_propagation_2026_09_24/band_variants.cjs:96-212: specifications rebuilt from meta.responses, specsFor()
 *      at the reported rate and at option A, their bands against main_case_bands.csv; the lane's variant runs on the
 *      uncorrected and the corrected model through cost(m, s), which on the September 27 payload must print as that
 *      lane's published band_variants.csv rows.
 * And the package's own guard (8): an item variant built with the package's API is evaluated by candidate v4's package;
 * a copy of its specification, or the case's specification on its model, stops.
 *
 * A check fails G4 when the package does not serve the call. A consumer gate that fails as written because the case
 * changed (13 line responses, part_rekeyed keys, national-scale edits), not the API, is recorded under consumer_code
 * with the consumer's line, what it does today and the change it needs; those do not fail G4.
 *
 * Run from anywhere (after main_case.cjs): node api_check.cjs -> derived/api_check.json (exit 1 if a check fails)
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const P = require("./package.cjs");
const { Engine, MODEL, METHODS, readJson, csvRows } = P;

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const REPO = path.join(FISCAL, "..", "..");
const LANE = "main_case_2026_09_29";
const SEPT27 = "main_case_long_run_2026_09_27";
const GEN_PIN = "8654a0c";
const GEN_DIR = "infra/immigration-fiscal/generation_account_2026_09_24/derived";
const GENS = ["G1", "G2", "G3plus"];

const summary = readJson(`${LANE}/derived/summary.json`);
const payload = readJson(`${LANE}/derived/corrections.json`);
const payload27 = readJson(`${SEPT27}/derived/corrections.json`);
const bandRows = csvRows(`${LANE}/derived/main_case_bands.csv`).filter((r) => r.profile === P.MAIN_PROFILE);
const published = Object.fromEntries(bandRows.map((r) => [r.variant, [Number(r.cost_low_bn), Number(r.cost_high_bn)]]));
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(...xs.map(Math.abs));
const spanOf = (xs) => [Math.min(...xs), Math.max(...xs)];
const f4 = (b) => b.map((x) => x.toFixed(4)).join(" / ");
const e1 = (x) => x.toExponential(1);

const patterns = [];
const consumerCode = [];
let failures = 0;
let current = null;
function pattern(consumer, lines, calls) {
  current = { consumer, lines, calls, checks: [] };
  patterns.push(current);
  console.log(`[${consumer}:${lines}] ${calls}`);
}
function check(label, ok, detail) {
  current.checks.push({ check: label, pass: !!ok, detail: detail || "" });
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
function needsCode(line, today, change) {
  consumerCode.push({ consumer: current.consumer, line, today, change });
  console.log(`  CODE ${current.consumer} at ${line}: ${today} -> ${change}`);
}
const throws = (f) => { try { f(); return null; } catch (e) { return String(e.message).split("\n")[0]; } };

// ---------------------------------------------------------------------------------------------------
pattern("distribution_weights_2026_09_23/case_ends.cjs", "63-94, 98-122 (working tree)",
  "modelFor(\"central\", m, withCentral({})), evaluateFull(m, s, MAIN_PROFILE) over MAIN_SPECS, stateFor(m, s, MAIN_PROFILE).production");
{
  const CAPPED = ["housing_subsidies", "energy_assistance"];
  const models = METHODS.map((m) => P.modelFor("central", m, P.withCentral({})));
  const runs = models.map((m) => P.MAIN_SPECS.map((s) => P.evaluateFull(m, s, P.MAIN_PROFILE)));
  const costs = runs.map((xs) => xs.map((r) => r.cost_bn));
  const ends = costs.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
  const at = (e, f) => mean(ends.map((ij, m) => f(runs[m][ij[e]])));
  const row = (r, id) => r.evaluation.spending.find((l) => l.id === id);
  const level = (r, lv) => r.capital.components.filter((c) => c.level === lv).reduce((a, c) => a + c.return_bn, 0);
  const band = [0, 1].map((e) => at(e, (r) => r.cost_bn));
  check("the band equals summary.json main_case (1e-9)", worst(band.map((x, j) => x - summary.main_case[j])) < 1e-9,
    `${f4(band)}, ends ${JSON.stringify(ends)}`);
  check("the band equals main_case_bands.csv's adopted row (1e-4)", worst(band.map((x, j) => x - published.adopted[j])) < 1e-4);
  const cap = summary.capital_at_end_specifications;
  const capGap = worst([0, 1].flatMap((e) => [at(e, (r) => r.capital.total_bn) - cap.total_bn[e],
    at(e, (r) => level(r, "state_local")) - cap.by_level_bn.state_local[e], at(e, (r) => level(r, "federal")) - cap.by_level_bn.federal[e]]));
  check("the capital return equals capital_at_end_specifications, in total and by level (1e-9)", capGap < 1e-9, `max |diff| ${e1(capGap)}`);
  const rent = [0, 1].map((e) => at(e, (r) => row(r, "housing_subsidies").response * row(r, "housing_subsidies").amount_bn));
  check("rental assistance equals lines_at_end_specifications.housing_subsidies.added_bn (1e-9)",
    worst(rent.map((x, j) => x - summary.lines_at_end_specifications.housing_subsidies.added_bn[j])) < 1e-9, f4(rent));
  const responses = ends.flatMap((ij, m) => ij.flatMap((i) => CAPPED.map((id) => row(runs[m][i], id).response)));
  check("both capped lines respond at 1 at every end specification", responses.every((r) => r === 1), `${responses.length} rows`);
  // The production block: every method's end reads one production cell; P and F there are the payload grid's.
  for (const [e, name] of [[0, "low"], [1, "high"]]) {
    const cells = ends.map((ij, m) => P.stateFor(models[m], P.MAIN_SPECS[ij[e]], P.MAIN_PROFILE).production);
    const index = Engine.productionIndex(MODEL, cells[0]);
    const caseP = at(e, (r) => r.evaluation.private_wtp_bn), caseF = at(e, (r) => r.evaluation.induced_receipts_bn);
    const A = at(e, (r) => r.evaluation.direct_fiscal_response_bn - r.capital.total_bn);
    check(`${name} end: one production cell; P and F are the payload grid's there (exact); cost = -(P + F) - A (1e-9)`,
      cells.every((c) => JSON.stringify(c) === JSON.stringify(cells[0]))
      && caseP === payload.production.private_wtp_bn[index] && caseF === payload.production.induced_receipts_bn[index]
      && Math.abs(band[e] + caseP + caseF + A) < 1e-9,
      `cell ${index}, normalization ${cells[0].normalization}: P ${caseP.toFixed(4)} (model.json ${MODEL.production.private_wtp_bn[index].toFixed(4)}), F ${caseF.toFixed(4)}`);
  }
}

// ---------------------------------------------------------------------------------------------------
pattern("uncertainty_propagation_2026_09_22/sept24_specs.cjs", "94-150, 205-209",
  "its own models (MODEL; Engine.applyCorrections(MODEL, payload)), evaluateFull(m, spec, MAIN_PROFILE), componentsFor(null)");
{
  const P24 = P.P24;
  const { GG24, SCHOOL24 } = P.P26;
  const R = payload.meta.responses;
  const EXTRA = ["reading", "rate", "long_run", "enterprises", "line_responses"];
  const KLINES = ["education_services", "school_reprice", "college_rekey", "public_order_safety", "health_services",
    "general_public_services", "economic_affairs_services", "recreation_culture"];
  const RLINES = ["economic_affairs_services", "recreation_culture", "housing_subsidies"];
  const TRANSFER_LINES = ["snap", "other_state_welfare", "family_and_general_assistance", "unemployment"];
  const swap = (v, old, now) => (v === old[0] ? now[0] : v === old[1] ? now[1] : NaN);
  check("payload responses equal summary.json responses (:207)", JSON.stringify(R) === JSON.stringify(summary.responses));
  const models = { uncorrected: MODEL, case: Engine.applyCorrections(MODEL, payload) };
  const rows = P24.MAIN_SPECS.map((s, i) => ({ ...s,
    gg: swap(s.gg, GG24, [R.general_government.low, R.general_government.high]),
    school: swap(s.school, SCHOOL24, [R.school.growth, R.school.decline]),
    reading: P.MAIN_SPECS[i].reading, rate: P.MAIN_SPECS[i].rate, enterprises: P.MAIN_SPECS[i].enterprises }));
  check("adopted responses replace the September 24 ones one for one; no specification field beyond EXTRA (:102-104)",
    rows.length === P.MAIN_SPECS.length && rows.every((s, i) => Object.keys(P24.MAIN_SPECS[0]).every((k) => s[k] === P.MAIN_SPECS[i][k])
      && Object.keys(P.MAIN_SPECS[i]).every((k) => k in P24.MAIN_SPECS[0] || EXTRA.includes(k))),
    `${rows.length} specifications`);
  const defs = Object.fromEntries(P.componentsFor(null).map((c) => [c.id, c]));
  check("componentsFor(null) is meta.capital_return.components (:107)",
    JSON.stringify(P.componentsFor(null)) === JSON.stringify(payload.meta.capital_return.components), `${Object.keys(defs).length} components`);
  // The consumer's derivative loop, as written, on the first specification: it stops at a key it does not know.
  const asWritten = throws(() => {
    const spec = P.MAIN_SPECS[0], r = P.evaluateFull(models.case, spec, P.MAIN_PROFILE);
    const k = Object.fromEntries(KLINES.map((id) => [id, 0]).concat([["enterprise_share", 0]]));
    for (const comp of r.capital.components) {
      const rule = defs[comp.id].key, unit = comp.stock_charged_bn * spec.rate * comp.response;
      if (rule.kind === "receipt_amount_over_national" && rule.line === P.ENTERPRISE_LINE) k.enterprise_share += unit;
      else if (rule.kind === "lines_amount_over_national") {
        for (const id of rule.numerator_lines) if (!(id in k)) throw new Error(`[BLOCKED] capital key line ${id} is not in KLINES`);
      } else throw new Error(`[BLOCKED] capital key kind ${rule.kind} has no derivative here`);
    }
  });
  // The same loop with every key kind (part_rekeyed: the parent line over its national plus the correction line over the
  // part's total) and any line: it must rebuild the capital return on both models.
  let rebuildGap = 0, responseGap = 0, transferGap = 0;
  const coefGap = {};
  const spans = { uncorrected: [], case: [] };
  for (const [i, spec] of P.MAIN_SPECS.entries()) {
    const coefs = {};
    for (const [c, m] of Object.entries(models)) {
      const r = P.evaluateFull(m, spec, P.MAIN_PROFILE);
      const line = (id) => r.evaluation.spending.find((l) => l.id === id);
      const receipt = (id) => r.evaluation.receipts.find((l) => l.id === id);
      const k = {};
      const add = (id, v) => { k[id] = (k[id] || 0) + v; };
      for (const comp of r.capital.components) {
        const rule = defs[comp.id].key, unit = comp.stock_charged_bn * spec.rate * comp.response;
        if (rule.kind === "receipt_amount_over_national") add(`receipt:${rule.line}`, unit / receipt(rule.line).national_bn);
        else if (rule.kind === "lines_amount_over_national") for (const id of rule.numerator_lines) add(id, unit / line(rule.denominator_line).national_bn);
        else if (rule.kind === "part_rekeyed") { add(rule.parent_line, unit / line(rule.parent_line).national_bn); add(rule.correction_line, unit / rule.part_national_bn); }
        else if (rule.kind === "constant") add("constant", unit * rule.value);
      }
      const amount = (id) => (id === "constant" ? 1 : id.startsWith("receipt:") ? receipt(id.slice(8)).amount_bn : line(id).amount_bn);
      rebuildGap = Math.max(rebuildGap, Math.abs(Object.keys(k).reduce((a, id) => a + k[id] * amount(id), 0) - r.capital.total_bn));
      if (c === "uncorrected") Object.assign(coefs, k);
      else for (const id of Object.keys(k)) coefGap[id] = Math.max(coefGap[id] || 0, Math.abs(k[id] - (coefs[id] || 0)) / Math.abs(k[id]));
      spans[c].push(r.cost_bn);
      for (const id of RLINES) responseGap = Math.max(responseGap, Math.abs(line(id).response - spec.line_responses[id]));
      responseGap = Math.max(responseGap, Math.abs(receipt(P.ENTERPRISE_LINE).response - spec.line_responses[P.ENTERPRISE_RECEIPT]));
      for (const id of TRANSFER_LINES) transferGap = Math.max(transferGap, Math.abs(line(id).response - 1));
    }
  }
  check("each line takes its specification's response (engine rows, :133-137)", responseGap === 0, `${P.MAIN_SPECS.length} specifications, both models`);
  check("the benefit keys' transfer lines respond fully (:138)", transferGap === 0, TRANSFER_LINES.join(", "));
  check("derivatives with every key kind rebuild the capital return on both models (1e-9)", rebuildGap < 1e-9, `max |diff| ${e1(rebuildGap)}`);
  for (const [c, want] of [["uncorrected", summary.uncorrected_at_adopted_responses], ["case", summary.main_case]]) {
    const b = spanOf(spans[c]);
    check(`${c === "case" ? "the payload model" : "the uncorrected model"} spans the published band (${c === "case" ? "main_case" : "uncorrected_at_adopted_responses"}, 1e-9)`,
      worst(b.map((x, j) => x - want[j])) < 1e-9, f4(b));
  }
  const moved = Object.entries(coefGap).filter(([, g]) => g > 1e-12).map(([id, g]) => `${id} ${g.toExponential(2)}`);
  needsCode(":86, :122, :125", `stops: ${asWritten}`,
    "a part_rekeyed branch (parent line over its national, correction line over part_national_bn) and housing_subsidies, roads_vmt_sl, roads_vmt_fed in KLINES");
  if (moved.length) {
    const nat = (m, id) => (id.startsWith("receipt:") ? m.receipts.lines.find((l) => l.id === id.slice(8)) : m.spending.lines.find((l) => l.id === id)).national_bn;
    const moves = Object.keys(coefGap).filter((id) => coefGap[id] > 1e-12).map((id) => `${id} ${nat(MODEL, id)} -> ${nat(models.case, id).toFixed(3)}`);
    needsCode(":144-146", `the model-independence gate (1e-12) fails: relative coefficient change between the models, ${moved.join("; ")}`,
      `the payload's national-scale edits move these keys' national totals (${moves.join("; ")}), so a coefficient per unit of amount differs between the uncorrected and the corrected model; compare the coefficients within a model, or per unit of national share`);
  }
}

// ---------------------------------------------------------------------------------------------------
pattern("world_ledger_2026_09_27/generation_lines.cjs", "57-66, 109 (run_generations.cjs partsAt)",
  `its own models: the generation lane's model_G*.json at ${GEN_PIN}; evaluateFull(m, spec, MAIN_PROFILE), stateFor(m, spec, MAIN_PROFILE).receipt_scenario`);
const show = (f) => execFileSync("git", ["-C", REPO, "show", `${GEN_PIN}:${GEN_DIR}/${f}`], { maxBuffer: 1 << 30 }).toString("utf8");
const rawGen = Object.fromEntries(GENS.map((g) => [g, show(`model_${g}.json`)]));
const genModels = Object.fromEntries(GENS.map((g) => [g, JSON.parse(rawGen[g])]));
{
  // The oracle: model.json is the sum of the generation models, and the engine and every capital key are linear in the
  // group's amounts, so the generations add to the whole at every specification. It must hold under the September 27
  // package before it tests this one.
  const additivity = (pkg) => {
    let cost = 0, capital = 0;
    for (const s of pkg.MAIN_SPECS) {
      const whole = pkg.evaluateFull(MODEL, s, pkg.MAIN_PROFILE);
      const parts = GENS.map((g) => pkg.evaluateFull(genModels[g], s, pkg.MAIN_PROFILE));
      cost = Math.max(cost, Math.abs(parts.reduce((a, r) => a + r.cost_bn, 0) - whole.cost_bn));
      capital = Math.max(capital, Math.abs(parts.reduce((a, r) => a + r.capital.total_bn, 0) - whole.capital.total_bn));
    }
    return [cost, capital];
  };
  const a27 = additivity(P.SEPT27), a29 = additivity(P);
  check("the oracle holds under the September 27 package: the generations add to model.json at every specification (1e-9)",
    a27[0] < 1e-9 && a27[1] < 1e-9, `cost ${e1(a27[0])}, capital ${e1(a27[1])}`);
  check("under this package the generations add to model.json at every specification (1e-9)", a29[0] < 1e-9 && a29[1] < 1e-9,
    `cost ${e1(a29[0])}, capital ${e1(a29[1])}`);
  let capWorst = 0, zeroLines = true, scenarios = new Set();
  for (const s of P.MAIN_SPECS) for (const g of GENS) {
    const r = P.evaluateFull(genModels[g], s, P.MAIN_PROFILE);
    for (const c of r.capital.components) capWorst = Math.max(capWorst, Math.abs(c.stock_charged_bn * s.rate * c.key * c.response - c.return_bn));
    for (const l of P.PAYLOAD_LINES) { const x = r.evaluation.spending.find((y) => y.id === l.id); if (!x || x.amount_bn !== 0) zeroLines = false; }
    scenarios.add(P.stateFor(genModels[g], s, P.MAIN_PROFILE).receipt_scenario);
  }
  check("each capital component's stock x rate x key x response is its return (1e-9)", capWorst < 1e-9, `max |diff| ${e1(capWorst)}`);
  check("the payload's correction lines enter the generation models at zero (withSyntheticLines)", zeroLines, `${P.PAYLOAD_LINES.length} lines`);
  check("stateFor(m, spec, MAIN_PROFILE).receipt_scenario is set", [...scenarios].every((x) => typeof x === "string" && x.length), [...scenarios].join(", "));
  // forPayload() of the September 27 payload on that pin's corrected generation models is the September 27 package.
  const corr = JSON.parse(show("generation_corrections.json"));
  const F27 = P.forPayload(payload27);
  let gap = 0;
  for (const g of GENS) {
    const m = Engine.applyCorrections(JSON.parse(rawGen[g]), corr.payloads.a[g]);
    F27.MAIN_SPECS.forEach((s, i) => { gap = Math.max(gap, Math.abs(F27.evaluateFull(m, s, F27.MAIN_PROFILE).cost_bn - P.SEPT27.evaluateFull(m, P.SEPT27.MAIN_SPECS[i], P.MAIN_PROFILE).cost_bn)); });
  }
  check(`forPayload(${SEPT27} corrections.json) on the corrected generation models at ${GEN_PIN} is the September 27 package (exact)`,
    corr.meta.union.startsWith(SEPT27 + "/") && gap === 0, `${corr.meta.union}; max |diff| ${gap}`);
}

// ---------------------------------------------------------------------------------------------------
pattern("winners_losers_2026_09_24/specs.cjs", "100-108, 130-160",
  "each case's payload applied by the consumer; pkg.RESPONSES; pkg.evaluateFull(m, spec) (no profile); the previous case through SEPT27");
{
  const CASES = [["adopted_2026_09_27", SEPT27, "sept27_case", P.SEPT27], ["adopted_2026_09_29", LANE, "adopted", P]];
  for (const [caseName, payloadLane, variant, pkg] of CASES) {
    const pl = readJson(`${payloadLane}/derived/corrections.json`);
    const m = Engine.applyCorrections(MODEL, pl);
    const specs = pkg.MAIN_SPECS, r = pl.meta.responses, cap = pl.meta.capital_return;
    check(`${caseName}: the package's responses are the payload's meta.responses (:142)`, JSON.stringify(pkg.RESPONSES) === JSON.stringify(r));
    check(`${caseName}: every specification carries the payload's responses (:144-146)`, specs.every((s) =>
      [r.general_government.low, r.general_government.high].includes(s.gg) && [r.school.growth, r.school.decline].includes(s.school)));
    const want = (s, id) => (id.startsWith("receipt:") ? r[id.slice(8)].low : r[id][s.reading]);
    const asWritten = specs.every((s) => Object.keys(s.line_responses).length === 4 && Object.entries(s.line_responses).every(([id, v]) => v === want(s, id))
      && s.rate === cap.rates[s.reading] && s.enterprises === cap.enterprises);
    const general = specs.every((s) => Object.entries(s.line_responses).every(([id, v]) => v === want(s, id))
      && s.rate === cap.rates[s.reading] && s.enterprises === cap.enterprises);
    check(`${caseName}: every line response, the rate and the enterprise option are the payload's meta (:149-152 without the count)`, general,
      `${Object.keys(specs[0].line_responses).length} line responses`);
    if (!asWritten) needsCode(":151", `the gate requires exactly 4 line_responses; ${caseName} has ${Object.keys(specs[0].line_responses).length}`,
      "require one entry per meta.responses line or receipt override (P.LINE_RESPONSES); every receipt override has low = high, so :149's .low stays right");
    const results = specs.map((spec) => { const full = pkg.evaluateFull(m, spec); return { r: full.evaluation, capital: full.capital }; });
    const costs = results.map((x) => -x.r.welfare_bn + x.capital.total_bn);
    const b = spanOf(costs);
    check(`${caseName}: band reproduces main_case_bands.csv (${variant}, 1e-4)`, !!published[variant] && worst(b.map((x, j) => x - published[variant][j])) < 1e-4, f4(b));
    let colGap = 0;
    for (const x of results) {
      const lv = x.capital.components.reduce((a, c) => a + (c.level === "federal" || c.level === "state_local" ? c.return_bn : NaN), 0);
      const gp = x.capital.components.reduce((a, c) => a + (["core", "block", "enterprise"].includes(c.group) ? c.return_bn : NaN), 0);
      colGap = Math.max(colGap, Math.abs(lv - x.capital.total_bn), Math.abs(gp - x.capital.total_bn));
    }
    check(`${caseName}: capitalColumns() finds every component's level and part (:112-120)`, colGap < 1e-9, `max |diff| ${e1(colGap)}`);
  }
}

// ---------------------------------------------------------------------------------------------------
pattern("main_case_decomposition_2026_09_29/decompose.cjs", "74-82, 177-178, 356-373",
  "correctionsPayload(), evaluateFull(UNION, s) (no profile), componentsFor(spec.capital_variant), SYN, SYN_LINES, CONSTANTS, RESPONSES.row8_factor");
{
  check("correctionsPayload() is derived/corrections.json (:77)", JSON.stringify(P.correctionsPayload()) === JSON.stringify(payload),
    `${payload.lines.length} lines, ${payload.receipt_lines.length} receipt lines, ${payload.edits.length} edits`);
  const UNION = Engine.applyCorrections(MODEL, payload);
  const full = P.MAIN_SPECS.map((s) => P.evaluateFull(UNION, s));
  const b = spanOf(full.map((x) => x.cost_bn));
  check("the union with no profile spans summary.json main_case (1e-9)", worst(b.map((x, j) => x - summary.main_case[j])) < 1e-9, f4(b));
  const missing = full.flatMap((x, i) => x.capital.components.filter((c) => !P.componentsFor(P.MAIN_SPECS[i].capital_variant).find((y) => y.id === c.id)));
  check("componentsFor(spec.capital_variant) names every component the evaluation returns (:372-373)", missing.length === 0, `${full[0].capital.components.length} components`);
  const row8 = P.CONSTANTS.row8.c * P.RESPONSES.row8_factor;
  check("SYN, SYN_LINES, REKEY_LINE, ENTERPRISE_LINE, LR, LR_LINES and CONSTANTS.row8.c x RESPONSES.row8_factor are defined (:177-178, :227-228, :465-478)",
    P.SYN_LINES.length === 3 && [P.SYN.school, P.SYN.college, P.SYN.constants, P.REKEY_LINE, P.ENTERPRISE_LINE].every((x) => typeof x === "string")
    && !!P.LR && P.LR_LINES.length === 2 && Number.isFinite(row8), `row 8 ${row8.toFixed(4)}; SYN_LINES ${P.SYN_LINES.map((l) => l.id).join(", ")}`);
  needsCode(":177, :216-218", "SYN_LINES holds the September 24 package's three lines; the payload's five new lines (PAYLOAD_LINES) fall to the generic per-line treatment",
    "give roads_vmt_sl, roads_vmt_fed and the three state_price_* lines their age treatment (read P.PAYLOAD_LINES), and the receipt lines tenant_occupied_property and housing_enterprise_surplus theirs");
}

// ---------------------------------------------------------------------------------------------------
pattern("within_group_distribution_2026_09_29/export_lines.cjs", "37-73",
  "dump(): evaluateFull(m, spec), stateFor(withSyntheticLines(m), spec): fiscal_weight, receipt_scenario, production, count_production");
{
  function dump(m, spec) {
    const full = P.evaluateFull(m, spec);
    const state = P.stateFor(P.withSyntheticLines ? P.withSyntheticLines(m) : m, spec);
    const ev = full.evaluation, fw = state.fiscal_weight;
    const rows = ev.receipts.map((r) => -fw * r.effect_bn).concat(ev.spending.map((r) => -fw * r.effect_bn));
    const capital = full.capital.components.map((c) => c.return_bn);
    const production = -(ev.private_wtp_bn + fw * ev.induced_receipts_bn);
    return { cost_bn: full.cost_bn, sum_bn: rows.concat(capital).reduce((a, x) => a + x, 0) + production, state };
  }
  const unionModel = Engine.applyCorrections(MODEL, payload);
  const uCost = P.MAIN_SPECS.map((s) => P.evaluateFull(unionModel, s).cost_bn);
  const lo = uCost.indexOf(Math.min(...uCost)), hi = uCost.indexOf(Math.max(...uCost));
  check("the corrected union reproduces the adopted case (:40-41, 1e-4 against the adopted row)",
    Math.abs(uCost[lo] - published.adopted[0]) < 1e-4 && Math.abs(uCost[hi] - published.adopted[1]) < 1e-4, `${f4([uCost[lo], uCost[hi]])} at ${lo} / ${hi}`);
  let gap = 0, n = 0;
  for (const m of [unionModel].concat(GENS.map((g) => genModels[g]))) for (const i of [lo, hi]) {
    const d = dump(m, P.MAIN_SPECS[i]);
    gap = Math.max(gap, Math.abs(d.sum_bn - d.cost_bn));
    n += 1;
    if (!(d.state.production && typeof d.state.receipt_scenario === "string" && Number.isFinite(d.state.fiscal_weight))) gap = Infinity;
  }
  check("rows, capital and production sum to evaluateFull()'s cost, on the union and the generation models (:71, :80, :92; 1e-9)", gap < 1e-9, `${n} dumps, max |diff| ${e1(gap)}`);
  const capFile = readJson("capital_return_services_2026_09_27/derived/engine_components.json");
  const differ = capFile.components.filter((c) => JSON.stringify(c.key) !== JSON.stringify(P.componentsFor(null).find((x) => x.id === c.id).key)).map((c) => c.id);
  if (differ.length) needsCode(":29-30", `capRule reads the capital lane's engine_components.json; its key rule differs from the case's for ${differ.join(", ")} (silent: the rows carry the wrong rule text)`,
    "read the rules from P.componentsFor(spec.capital_variant) (meta.capital_return.components)");
}

// ---------------------------------------------------------------------------------------------------
pattern("sept24_propagation_2026_09_24/band_variants.cjs", "96-212",
  "specifications rebuilt from P24.MAIN_SPECS and meta.responses, P.specsFor({rates}), P.specsFor({enterprises: \"A\"}), Engine.applyCorrections(MODEL, payload)");
{
  const canon = (x) => JSON.stringify(x, (k, v) => (v && typeof v === "object" && !Array.isArray(v)
    ? Object.fromEntries(Object.keys(v).sort().map((kk) => [kk, v[kk]])) : v));
  const r = payload.meta.responses, cap = payload.meta.capital_return;
  check("the payload's meta.responses equal the case's summary.json responses (:145)", JSON.stringify(r) === JSON.stringify(summary.responses));
  const rebuild = (lineResponses) => P.P24.MAIN_SPECS.map((s) => {
    const low = s.gg === P.GG24[0], reading = low ? "low" : "high";
    return { ...s, gg: low ? r.general_government.low : r.general_government.high, school: s.school === P.SCHOOL24[0] ? r.school.growth : r.school.decline,
      reading, rate: cap.rates[reading], long_run: r[P.LR_LINES[0]].variant, enterprises: cap.enterprises, line_responses: lineResponses(reading) };
  });
  const asWritten = rebuild((reading) => ({ ...Object.fromEntries(P.LR_LINES.map((id) => [id, r[id][reading]])),
    [P.RENTAL]: r[P.RENTAL][reading], [r[P.ENTERPRISE_LINE].override]: r[P.ENTERPRISE_LINE][reading] }));
  const specs = rebuild((reading) => Object.fromEntries(Object.entries(P.LINE_RESPONSES).map(([k, e]) => [k, e[reading]])));
  check("specifications rebuilt from every meta.responses entry (P.LINE_RESPONSES) at the reading equal MAIN_SPECS", canon(specs) === canon(P.MAIN_SPECS));
  if (canon(asWritten) !== canon(P.MAIN_SPECS)) needsCode(":152-156", "the rebuild sets the long-run lines, rental assistance and the enterprise receipt only (4 of 13 line responses), so the MAIN_SPECS gate fails",
    "build line_responses from every meta.responses entry: a spending line under its id, a receipt override (receipt: true) under its override key, at the reading");
  const rate = cap.rates.reported;
  const specs7 = P.specsFor({ rates: { low: rate, high: rate } });
  check(`the ${rate} specifications differ from the case's in the rate alone (:169-170)`, canon(specs7) === canon(specs.map((s) => ({ ...s, rate }))));
  const corrected = Engine.applyCorrections(MODEL, payload);
  for (const [variant, sp] of [["capital_return_at_7pct", specs7], ["enterprises_out_option_a", P.specsFor({ enterprises: "A" })], ["adopted", specs]]) {
    const b = spanOf(sp.map((s) => P.evaluateFull(corrected, s, P.MAIN_PROFILE).cost_bn));
    check(`the payload model at ${variant === "adopted" ? "the rebuilt specifications" : `${variant}'s specifications`} gives main_case_bands.csv's ${variant} row (1e-4)`,
      worst(b.map((x, j) => x - published[variant][j])) < 1e-4, f4(b));
  }
  // The lane's variant runs (:96-124, :135-137, :176-190, :197-212): justice coding and grids, uncompensated use at 0.7,
  // each on the uncorrected model and the corrected one, through the package's cost(m, s). On the September 27 payload
  // (forPayload) they must print as sept27_propagation_2026_09_27/derived/band_variants.csv's sept27_uncorrected and
  // sept27 rows (toPrecision(15)); on this case the lane's own gates must hold.
  const cj = readJson("cj_use_allocation_2026_09_23/derived/summary.json");
  const JUSTICE = { central: cj.central.change_bn, grid_low: cj.range_change_bn[0], grid_high: cj.range_change_bn[1], cbp_fixed: cj.one_at_a_time_change_bn.cbp_zero };
  function shiftKey(m, lineId, key, delta) {
    const out = JSON.parse(JSON.stringify(m));
    const line = out.spending.lines.find((l) => l.id === lineId);
    for (const a of ["personal", "shared"]) { line.keys[key][a].target_bn += delta; line.keys[key][a].other_bn -= delta; }
    return out;
  }
  const UC07 = { uc: { uninsured_use_low: "uninsured_use_07_low", uninsured_use_high: "uninsured_use_07_high" } };
  const specsWith = (sp, change) => sp.map((s) => ({ ...s, ...(change.justice ? { justice: change.justice } : {}), ...(change.uc ? { uc: change.uc[s.uc] } : {}) }));
  const grid = (end) => (m) => shiftKey(m, "public_order_safety", "use", JUSTICE[end] - JUSTICE.central);
  const BV = [["adopted", {}, null], ["justice_raw_coding", { justice: "use_raw_coding" }, null], ["justice_grid_low", {}, grid("grid_low")],
    ["justice_grid_high", {}, grid("grid_high")], ["justice_cbp_fixed", {}, grid("cbp_fixed")], ["uncompensated_use_0.7", UC07, null],
    ["justice_grid_low_and_uncompensated_use_0.7", UC07, grid("grid_low")]];
  const runVariants = (pkg, base, sp) => Object.fromEntries(BV.map(([name, change, mc]) => {
    const m = mc ? mc(base) : base;
    return [name, specsWith(sp, change).map((s) => pkg.cost(m, s))];
  }));
  const F27 = P.forPayload(payload27);
  const r27 = payload27.meta.responses, cap27 = payload27.meta.capital_return;
  const specs27 = P.P24.MAIN_SPECS.map((s) => {
    const low = s.gg === P.GG24[0], reading = low ? "low" : "high";
    return { ...s, gg: low ? r27.general_government.low : r27.general_government.high, school: s.school === P.SCHOOL24[0] ? r27.school.growth : r27.school.decline,
      reading, rate: cap27.rates[reading], long_run: r27[P.LR_LINES[0]].variant, enterprises: cap27.enterprises,
      line_responses: { ...Object.fromEntries(P.LR_LINES.map((id) => [id, r27[id][reading]])), [P.RENTAL]: r27[P.RENTAL][reading],
        [r27[P.ENTERPRISE_LINE].override]: r27[P.ENTERPRISE_LINE][reading] } };
  });
  check("on the September 27 payload the rebuild as written equals forPayload()'s MAIN_SPECS (:156)", canon(specs27) === canon(F27.MAIN_SPECS));
  const pub = csvRows("sept27_propagation_2026_09_27/derived/band_variants.csv");
  let printedSame = 0, printedAll = 0;
  for (const [run, base] of [["sept27_uncorrected", MODEL], ["sept27", Engine.applyCorrections(MODEL, payload27)]]) {
    const v = runVariants(F27, base, specs27);
    for (const [name] of BV) {
      const b = spanOf(v[name]), row = pub.find((x) => x.case === run && x.variant === name);
      printedAll += 1;
      if (row && b[0].toPrecision(15) === row.cost_low_bn && b[1].toPrecision(15) === row.cost_high_bn) printedSame += 1;
    }
  }
  check("forPayload(September 27 payload): the variant runs on the uncorrected and the corrected model print as the published band_variants.csv rows (toPrecision(15))",
    printedSame === printedAll && printedAll === 2 * BV.length, `${printedSame} of ${printedAll} rows`);
  const vu = runVariants(P, MODEL, specs), vc = runVariants(P, corrected, specs);
  const bu = spanOf(vu.adopted), bc = spanOf(vc.adopted);
  check("this case: the uncorrected run reproduces uncorrected_at_adopted_responses and the corrected run main_case (summary.json 1e-9, main_case_bands.csv 1e-4) (:192-199)",
    worst(bu.map((x, j) => x - summary.uncorrected_at_adopted_responses[j])) < 1e-9 && worst(bc.map((x, j) => x - summary.main_case[j])) < 1e-9
    && worst(bu.map((x, j) => x - published.uncorrected_at_adopted_responses[j])) < 1e-4 && worst(bc.map((x, j) => x - published.adopted[j])) < 1e-4,
    `${f4(bu)}; ${f4(bc)}`);
  const moveGap = Math.max(...BV.slice(1).map(([name]) => worst(vu[name].map((x, i) => (x - vu.adopted[i]) - (vc[name][i] - vc.adopted[i])))));
  check("this case: every variant moves every specification by the same amount on the uncorrected and the corrected model (:200-206, 1e-9)",
    moveGap < 1e-9, `${BV.length - 1} variants, max gap ${e1(moveGap)}`);
}

// ---------------------------------------------------------------------------------------------------
pattern("main_case_2026_09_29/package.cjs", "225-245 (the guard)",
  "an item variant through the package's API: withCentral(o), modelFor, specsFor(o), evaluateFull");
{
  const o = { roads: P.V4PKG.OFF.roads };
  const oo = P.withCentral(o);
  const mv = P.modelFor("central", METHODS[0], oo);
  const sv = P.specsFor(o);
  const V4 = P.V4PKG;
  const sv4 = V4.specsFor(V4.withCentral(Object.assign({}, P.ITEMS, o)));
  const gap = worst(sv.map((s, i) => P.evaluateFull(mv, s).cost_bn - V4.evaluateFull(mv, sv4[i]).cost_bn));
  check(`the roads item off (${JSON.stringify(o)}): evaluateFull on its model and specsFor(o)'s specifications is candidate v4's (exact)`, gap === 0,
    `${sv.length} specifications; specification fields ${Object.keys(sv[0]).length}, as MAIN_SPECS' ${Object.keys(P.MAIN_SPECS[0]).length}`);
  const copied = throws(() => P.evaluateFull(mv, Object.assign({}, sv[0])));
  const crossed = throws(() => P.evaluateFull(mv, P.MAIN_SPECS[0]));
  check("a copy of the variant's specification stops ([BLOCKED])", !!copied && copied.includes("[BLOCKED]"), copied);
  check("the case's specification on the variant's model stops ([BLOCKED])", !!crossed && crossed.includes("[BLOCKED]"), crossed);
}

// ---------------------------------------------------------------------------------------------------
const record = {
  gate: "G4: consumers' call patterns, as written, run against this package; a failing check is a package defect",
  pass: failures === 0,
  generation_pin: { commit: GEN_PIN, files: `${GEN_DIR}/model_{G1,G2,G3plus}.json, generation_corrections.json`, source: "world_ledger_2026_09_27/pins.json sept27.generation" },
  patterns,
  consumer_code: consumerCode,
};
fs.writeFileSync(path.join(HERE, "derived", "api_check.json"), JSON.stringify(record, null, 1) + "\n");
const n = patterns.reduce((a, p) => a + p.checks.length, 0);
console.log(failures ? `G4 FAIL: ${failures} of ${n} checks` : `G4 PASS: ${patterns.length} patterns, ${n} checks; ${consumerCode.length} consumer gates need code (listed)`);
if (failures) process.exitCode = 1;
