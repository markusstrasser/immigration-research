/* G4, the API: consumers' call patterns, as they are written, run against this package (main case v6, adopted 2026-10-07) in a
 * harness inside the lane (so the lane's reruns repeat it). The patterns are v5's (main_case_2026_10_05/api_check.cjs),
 * each citing its consumer and repeating its calls and gates on this lane's package and derived files, as a path swap
 * would run them, with these changes for v6:
 *   1. distribution_weights_2026_09_23/case_ends.cjs:63-94: unchanged; the case's band row keeps v5's name (adopted).
 *   2. uncertainty_propagation_2026_09_22/sept24_specs.cjs:94-150: unchanged.
 *   3. world_ledger_2026_09_27/generation_lines.cjs:57-66 (run_generations.cjs partsAt()): the September 29 generation
 *      payloads (aa1f53b2) with withLineage() on G3+ add to the item base (ITEM_BASE: v5 with the lineage item's
 *      edits); with the edit sets' edits by a stated rule they add to this case at every specification. The rule: each
 *      national-scale edit as it is on every generation model (their national totals are the case's, so each
 *      generation's cells scale by the case's factor); item pension_tr2026's lineage parts on G3+, its union parts by
 *      each generation's share of the union's OASDI receipts and Part A accrual on the September 29 payloads;
 *   4. winners_losers_2026_09_24/specs.cjs:144-175 (HEAD b7c453a9): three cases, September 29 through SEPT29, v5
 *      through OCT05 (the oct05_case row) and this one;
 *   5. main_case_decomposition_2026_09_29/decompose.cjs (line numbers at HEAD b7c453a9): v5's calls, then its v4 line
 *      gates (:281-284), its lineage-last gate (:308-311) and its pension-source gate (:286-290) as written;
 *   6. within_group_distribution_2026_09_29/export_lines.cjs (HEAD b7c453a9): v5's dump() (:126-155), its capRule
 *      (:94-103), then its pension gate (:280-304) as written, on the model cells at each end;
 *   7. sept24_propagation_2026_09_24/band_variants.cjs (line numbers at HEAD b7c453a9): its specification rebuild
 *      (:260-269), runs and move gates (:431-454), its cash-meta gate (:303-309) and its edit-layout gate (:312-320);
 *   8. the package's own guard (v5's viaCandidate, followNationals) on this package; the added people's keys under each
 *      v4 item off on ITEM_BASE (the lineage's edits, no edit set), and on this case whether the edit sets build there;
 *   9. new, the item API (package.cjs caseOf, forItems): with no item the case is v5; meta.items locates every edit
 *      set's edits and its parts add to them; the lineage base and its additions; withItems() on a consumer's model;
 *      the fixed-amount guard and editsAt(); arms as options; lineage options (caseOf's fourth argument, consumer.cjs on
 *      the option's payload); the cash set; the guards on reserved meta and the slots.
 *
 * A check fails G4 when the package does not serve the call. A consumer gate that fails as written because the case
 * changed (the edit sets after the lineage's edits, the 2026 pension block, the added people's amounts), not the API, is
 * recorded under consumer_code with the consumer's line, what it does today and the change it needs; those do not fail
 * G4. A recorded gate is one this file re-runs as the consumer writes it; where it reconstructs older code instead of
 * HEAD's, the record says so (2026-10-07: the winners and band_variants specification gates, decompose.cjs's
 * SYN_LINES treatment and export_lines.cjs's capRule were reconstructions of older code; they are now HEAD's, which
 * pass, and decompose.cjs's receipt-line gate, which stops on item user_fees's carriers, is recorded).
 *
 * Run from anywhere (after main_case.cjs): node api_check.cjs -> derived/api_check.json (exit 1 if a check fails)
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");
const P = require("./package.cjs");
const { Engine, MODEL, METHODS, readJson, csvRows } = P;

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const REPO = path.join(FISCAL, "..", "..");
const LANE = "main_case_2026_10_07";
const OCT05 = "main_case_2026_10_05";
const SEPT27 = "main_case_long_run_2026_09_27";
const SEPT29 = "main_case_2026_09_29";
const GEN_PIN = "8654a0c";
const GEN29_PIN = "aa1f53b2";
const GEN_DIR = "infra/immigration-fiscal/generation_account_2026_09_24/derived";
const GENS = ["G1", "G2", "G3plus"];

const summary = readJson(`${LANE}/derived/summary.json`);
const payload = readJson(`${LANE}/derived/corrections.json`);
const cashPayload = readJson(`${LANE}/derived/corrections_cash.json`);
const payload5 = readJson(`${OCT05}/derived/corrections.json`);
const cashPayload5 = readJson(`${OCT05}/derived/corrections_cash.json`);
const payload27 = readJson(`${SEPT27}/derived/corrections.json`);
const bandRows = csvRows(`${LANE}/derived/main_case_bands.csv`).filter((r) => r.profile === P.MAIN_PROFILE);
const published = Object.fromEntries(bandRows.map((r) => [r.variant, [Number(r.cost_low_bn), Number(r.cost_high_bn)]]));
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(...xs.map(Math.abs));
const spanOf = (xs) => [Math.min(...xs), Math.max(...xs)];
const f4 = (b) => b.map((x) => x.toFixed(4)).join(" / ");
const e1 = (x) => x.toExponential(1);
const sha = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const E = payload.meta.lineage.edits;
const N_BASE = P.ITEM_BASE.correctionsPayload().edits.length;

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
// consumer: the lane that holds the code, when it is not the pattern's (a producer the pattern's consumer reads).
function needsCode(line, today, change, consumer) {
  consumerCode.push({ consumer: consumer || current.consumer, line, today, change });
  console.log(`  CODE ${consumer || current.consumer} at ${line}: ${today} -> ${change}`);
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
  // The consumer's key-line pass as HEAD (b7c453a9) writes it, keyLines() at :104-115 (its derivatives at :160-170 take
  // the same kinds): line keys and part_rekeyed keys name their lines; a receipt key must be the enterprise receipt's.
  // An earlier version of this pattern reconstructed the pre-v4 loop (no part_rekeyed branch, a fixed KLINES list, a
  // model-independence gate) and recorded those as failing; HEAD has all three handled since the v4 propagation.
  const asWritten = throws(() => {
    for (const c of P.componentsFor(null)) {
      const k = c.key;
      if (k.kind === "lines_amount_over_national" || k.kind === "part_rekeyed") continue;
      if (!(k.kind === "receipt_amount_over_national" && k.line === P.ENTERPRISE_LINE)) {
        throw new Error(`[BLOCKED] capital key kind ${k.kind} (component ${c.id}) has no derivative here`);
      }
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
  if (asWritten) needsCode(":104-115 (keyLines), :160-170 (derivatives)", `stops: ${asWritten}: item user_fees's offset components are keyed by carrier receipt lines (meta.items capital)`,
    "a branch for any receipt_amount_over_national key: the return over the receipt line's national total per unit of its amount, so the rebuild holds; a carrier's amount is set from national totals, so an offset adds no derivative per unit of a group's amount");
  // HEAD's scaled gate (:197-200): the derivatives differ between the models only through the national totals the
  // payload rescales. Here: each model's coefficients per unit of amount, with every key kind; their change is the
  // national totals' (a coefficient per unit of amount is unit / national).
  const moved = Object.entries(coefGap).filter(([, g]) => g > 1e-12).map(([id]) => id);
  // The national totals each coefficient divides by, from the components' key rules.
  const over = {};
  const by = (id, nat) => { (over[id] = over[id] || new Set()).add(nat); };
  for (const c of P.componentsFor(null)) {
    const k = c.key;
    if (k.kind === "lines_amount_over_national") for (const id of k.numerator_lines) by(id, `spending:${k.denominator_line}`);
    else if (k.kind === "part_rekeyed") { by(k.parent_line, `spending:${k.parent_line}`); by(k.correction_line, "constant"); }
    else if (k.kind === "receipt_amount_over_national") by(`receipt:${k.line}`, `receipt:${k.line}`);
  }
  const natOf = (m, key) => { const [side, id] = key.split(":"); const l = side === "receipt" ? m.receipts.lines.find((x) => x.id === id) : m.spending.lines.find((x) => x.id === id); return l ? l.national_bn : null; };
  const mU = P.withSyntheticLines(MODEL), mC = P.withSyntheticLines(models.case);
  check("the coefficients differ between the uncorrected and the corrected model only where a national total they divide by moves (HEAD's scaled gate, :197-200)",
    moved.every((id) => [...(over[id] || [])].some((key) => key !== "constant" && natOf(mU, key) !== natOf(mC, key))), `moved: ${moved.join(", ") || "none"}`);
}

// ---------------------------------------------------------------------------------------------------
pattern("world_ledger_2026_09_27/generation_lines.cjs", "57-66, 109 (run_generations.cjs partsAt)",
  `its own models: the generation lane's model_G*.json at ${GEN_PIN}; evaluateFull(m, spec, MAIN_PROFILE), stateFor(m, spec, MAIN_PROFILE).receipt_scenario; the September 29 generation payloads at ${GEN29_PIN} with withLineage() on G3+; v6: the edit sets' edits by meta.items`);
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
  const a27 = additivity(P.SEPT27), aHere = additivity(P);
  check("the oracle holds under the September 27 package: the generations add to model.json at every specification (1e-9)",
    a27[0] < 1e-9 && a27[1] < 1e-9, `cost ${e1(a27[0])}, capital ${e1(a27[1])}`);
  check("under this package the generations add to model.json at every specification (1e-9)", aHere[0] < 1e-9 && aHere[1] < 1e-9,
    `cost ${e1(aHere[0])}, capital ${e1(aHere[1])}`);
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
  // The September 29 generation payloads (convention a) add to the September 29 union at this case's specifications;
  // with the lineage's edits and production on G3+ (withLineage: the lineage item's) they add to the item base; with the
  // edit sets' edits by the rule they add to this case.
  const show29 = (f) => execFileSync("git", ["-C", REPO, "show", `${GEN29_PIN}:${GEN_DIR}/${f}`], { maxBuffer: 1 << 30 }).toString("utf8");
  const corr29 = JSON.parse(show29("generation_corrections_sept29.json"));
  const corr29c = JSON.parse(show29("generation_corrections_sept29_cash.json"));
  const raw29 = Object.fromEntries(GENS.map((g) => [g, show29(`model_${g}.json`)]));
  const gen29 = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(JSON.parse(raw29[g]), corr29.payloads.a[g])]));
  const gen29c = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(JSON.parse(raw29[g]), corr29c.payloads.a[g])]));
  const genL = { G1: gen29.G1, G2: gen29.G2, G3plus: P.withLineage(gen29.G3plus) };
  const union29 = P.SEPT29.payloadModel(), unionL = P.ITEM_BASE.payloadModel(), union6 = P.payloadModel();
  // The rule's bases, read as the pension lane reads the union's (package.cjs pensionBasis): OASDI receipts at the
  // reference incidence, and the Part A accrual (medicare less (1 - part_a_share) x the cash set's medicare).
  const PA = payload.meta.pension_accrual, REF = MODEL.receipts.reference;
  const rcp = (m, id, a) => m.receipts.lines.find((l) => l.id === id).cells[REF][a].target_bn;
  const grp = (m, id, a) => { const l = m.spending.lines.find((x) => x.id === id); return l.keys[l.preferred_key][a].target_bn; };
  const oasdiOf = (m, a) => PA.oasdi_lines.reduce((s, id) => s + rcp(m, id, a), 0) + PA.se_oasdi_share * rcp(m, PA.se_line, a);
  const partAOf = (ms, mc, a) => grp(ms, "medicare", a) - (1 - PA.part_a_share) * grp(mc, "medicare", a);
  const BASIS = { union_oasdi: (g, a) => oasdiOf(gen29[g], a), union_part_a: (g, a) => partAOf(gen29[g], gen29c[g], a) };
  const UNION_BASIS = { union_oasdi: (a) => oasdiOf(union29, a), union_part_a: (a) => partAOf(union29, P.SEPT29_CASH.payloadModel(), a) };
  // Item user_fees's rule (meta.user_fees.splits.split_basis): each part and carrier by each generation's share of its
  // split-basis line's union amount at the line's preferred key.
  const SPLIT = payload.meta.user_fees ? payload.meta.user_fees.splits.split_basis : {};
  const lineBases = [...new Set(Object.values(SPLIT))];
  const lineGap = Math.max(0, ...lineBases.flatMap((id) => P.ALLOCS.map((a) => Math.abs(GENS.reduce((t, g) => t + grp(gen29[g], id, a), 0) - grp(union29, id, a)))));
  const lineShare = (id, g, a) => grp(gen29[g], id, a) / GENS.reduce((t, x) => t + grp(gen29[x], id, a), 0);
  const basisGap = Math.max(lineGap, ...Object.keys(BASIS).flatMap((k) => P.ALLOCS.map((a) => Math.abs(GENS.reduce((t, g) => t + BASIS[k](g, a), 0) - UNION_BASIS[k](a)))));
  const share = (name, g, a) => (name.startsWith("lineage_") ? (g === "G3plus" ? 1 : 0)
    : BASIS[name] ? BASIS[name](g, a) / GENS.reduce((t, x) => t + BASIS[name](x, a), 0) : SPLIT[name] ? lineShare(SPLIT[name], g, a) : NaN);
  const carriersFor = (g) => P.ITEM_RECEIPT_LINES.map((l) => {
    if (!SPLIT[l.id]) throw new Error(`[BLOCKED] carrier ${l.id} has no split basis`);
    return Object.assign({}, l, { cells: Object.fromEntries(Object.entries(l.cells).map(([sc, c]) => [sc, Object.fromEntries(P.ALLOCS.map((a) => {
      const f = share(l.id, g, a);
      return [a, Object.assign({}, c[a], { target_bn: c[a].target_bn * f, other_bn: l.national_bn - c[a].target_bn * f, share: c[a].share * f })];
    }))])) });
  });
  const recs = P.CASE_ITEMS.filter((r) => r.applied && r.edits);
  const itemEditsFor = (g) => recs.flatMap((r) => P.ITEM_EDITS.slice(r.edits.first - N_BASE, r.edits.first - N_BASE + r.edits.count).map((e, j) => {
    if (e.national_bn !== undefined) return e;
    const parts = Object.entries(r.parts).filter(([, p]) => p.edit === j);
    if (!parts.length) throw new Error(`[BLOCKED] item ${r.id}'s cell shift ${j} has no parts to split by generation`);
    return Object.assign({}, e, { by: Object.fromEntries(P.ALLOCS.map((a) => [a, parts.reduce((t, [name, p]) => t + p.by[a] * share(name, g, a), 0)])) });
  }));
  const scaleLines = [...new Set(P.ITEM_EDITS.filter((e) => e.national_bn !== undefined).map((e) => `${e.side}:${e.line}`))];
  const natOf = (m, k) => { const [side, id] = k.split(":"); return (side === "receipt" ? m.receipts : m.spending).lines.find((l) => l.id === id).national_bn; };
  const natGap = Math.max(...GENS.flatMap((g) => scaleLines.map((k) => Math.abs(natOf(genL[g], k) - natOf(unionL, k)))));
  const gen6 = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(genL[g], { receipt_lines: carriersFor(g), edits: itemEditsFor(g), meta: genL[g].corrections })]));
  let gap29 = 0, gapL = 0, gap6 = 0;
  const byGen = Object.fromEntries(GENS.map((g) => [g, []]));
  const asWritten = [];
  for (const s of P.MAIN_SPECS) {
    const cost = (m) => P.evaluateFull(m, s, P.MAIN_PROFILE).cost_bn;
    const parts29 = GENS.map((g) => cost(gen29[g])), partsL = GENS.map((g) => cost(genL[g])), parts6 = GENS.map((g) => cost(gen6[g]));
    const sum = (xs) => xs.reduce((a, x) => a + x, 0);
    gap29 = Math.max(gap29, Math.abs(sum(parts29) - cost(union29)));
    gapL = Math.max(gapL, Math.abs(sum(partsL) - cost(unionL)));
    const whole6 = cost(union6);
    gap6 = Math.max(gap6, Math.abs(sum(parts6) - whole6));
    asWritten.push(sum(partsL) - whole6);
    GENS.forEach((g, k) => byGen[g].push(parts6[k]));
  }
  check(`the September 29 generation payloads at ${GEN29_PIN} (convention a, the models unchanged since ${GEN_PIN}) add to the September 29 union at this case's specifications (1e-9)`,
    corr29.meta.union === `${SEPT29}/derived/corrections.json` && corr29c.meta.union === P.BASE_FILES.cash && GENS.every((g) => raw29[g] === rawGen[g]) && gap29 < 1e-9, `max |diff| ${e1(gap29)}`);
  check("with the lineage item's edits and production on G3+ (withLineage) they add to the item base (ITEM_BASE: v5 with item added_age_mix) at every specification (1e-9)",
    gapL < 1e-9, `max |diff| ${e1(gapL)}`);
  check("the edit sets' national-scale lines have the item base's national totals on every generation model, so each edit scales each generation's cells by the case's factor (exact)",
    natGap === 0, `${scaleLines.length} lines`);
  check(`the rule's bases add over the generations to the union's: OASDI receipts and Part A accrual, and user_fees's split-basis lines (${lineBases.join(", ")}), on the September 29 payloads (1e-9)`, basisGap < 1e-9, `max |diff| ${e1(basisGap)}`);
  const ends6 = [48, 11];
  check("with the edit sets' edits by the rule (national-scale edits as they are; pension_tr2026's lineage parts on G3+, its union parts by those shares; user_fees's parts and carriers by their split-basis lines' union shares, meta.user_fees.splits.split_basis) they add to this case at every specification (1e-9)",
    gap6 < 1e-9, `max |diff| ${e1(gap6)}; at specifications 48 / 11: ${GENS.map((g) => `${g} ${f4(ends6.map((i) => byGen[g][i]))}`).join("; ")}`);
  const off = spanOf(asWritten);
  needsCode("v5_split.cjs:43-55 (loadCase), run_generations_v5.cjs:127-136",
    `loadCase stops (the lineage's edits no longer close the payload: ${payload.edits.length - E.first - E.count} edit-set edits follow them); with withLineage() alone on G3+ the generations add to the item base, ${off[0].toFixed(3)} to ${off[1].toFixed(3)}bn from this case across the 64 specifications`,
    "slice the lineage by meta.lineage.edits (first, count) and add meta.items' edit sets per generation: each national-scale edit as it is on every generation model; item pension_tr2026's lineage parts (lineage_oasdi, lineage_part_a) on G3+ and its union parts by a stated generation split (here each generation's share of the union's OASDI receipts and Part A accrual; the pension lane's per-generation rows, arms.csv, are the measured alternative); item user_fees's parts and its carrier lines (payload.receipt_lines after the payload's own) by each generation's share of the parent line's union amount (meta.user_fees.splits.split_basis), none on the added people; then rebuild generation_corrections_oct07*.json for generation_lines.cjs's pins",
    "generation_account_2026_09_24");
}

// ---------------------------------------------------------------------------------------------------
pattern("winners_losers_2026_09_24/specs.cjs", "144-175 (HEAD b7c453a9)",
  "each case's payload applied by the consumer; pkg.RESPONSES; pkg.evaluateFull(m, spec) (no profile); the previous cases through SEPT29 and OCT05");
{
  const CASES = [["adopted_2026_09_29", SEPT29, "sept29_case", P.SEPT29], ["adopted_2026_10_05", OCT05, "oct05_case", P.OCT05],
    ["adopted_2026_10_07", LANE, "adopted", P]];
  for (const [caseName, payloadLane, variant, pkg] of CASES) {
    const pl = readJson(`${payloadLane}/derived/corrections.json`);
    const m = Engine.applyCorrections(MODEL, pl);
    const specs = pkg.MAIN_SPECS, r = pl.meta.responses, cap = pl.meta.capital_return;
    check(`${caseName}: the package's responses are the payload's meta.responses (:157-158)`, JSON.stringify(pkg.RESPONSES) === JSON.stringify(r));
    check(`${caseName}: every specification carries the payload's responses (:159-161)`, specs.every((s) =>
      [r.general_government.low, r.general_government.high].includes(s.gg) && [r.school.growth, r.school.decline].includes(s.school)));
    const want = (s, id) => (id.startsWith("receipt:") ? r[id.slice(8)].low : r[id][s.reading]);
    // The gate as HEAD (b7c453a9) writes it, :162-172: the line responses are exactly the meta.responses entries with a
    // low and a high other than general government (a receipt's under its override key). An earlier version of this
    // pattern reconstructed the pre-v4 gate (exactly four line responses) and recorded it as failing on every case; HEAD
    // has no such gate (prop-c's run, 2026-10-07: specs.cjs passes on oct05).
    const ids = JSON.stringify(Object.entries(r).filter(([k, v]) => v && typeof v === "object" && "low" in v && "high" in v && k !== "general_government")
      .map(([k, v]) => v.override || k).sort());
    const asWritten = specs.every((s) => JSON.stringify(Object.keys(s.line_responses).sort()) === ids && Object.entries(s.line_responses).every(([id, v]) => v === want(s, id))
      && s.rate === cap.rates[s.reading] && s.enterprises === cap.enterprises);
    check(`${caseName}: every line response, the rate and the enterprise option are the payload's meta, as :162-172 gates them (HEAD)`, asWritten,
      `${Object.keys(specs[0].line_responses).length} line responses`);
    if (!asWritten) needsCode(":162-172", `the gate fails on ${caseName}: its line responses are not the payload's meta.responses entries`,
      "build line_responses from every meta.responses entry (P.LINE_RESPONSES)");
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
  check("the October 5 case is the package's OCT05, v5's own module (its lane and adopted stamp)", P.OCT05.LANE === OCT05 && typeof P.OCT05.ADOPTED === "string"
    && JSON.stringify(P.OCT05.correctionsPayload()) === JSON.stringify(payload5), `${P.OCT05.LANE}, adopted ${P.OCT05.ADOPTED}`);
}

// ---------------------------------------------------------------------------------------------------
pattern("main_case_decomposition_2026_09_29/decompose.cjs", "126-129, 256-257, 271-311, 355-373 (HEAD b7c453a9)",
  "correctionsPayload(), evaluateFull(UNION, s) (no profile), componentsFor(spec.capital_variant), SYN, SYN_LINES, CONSTANTS, RESPONSES.row8_factor, LINEAGE_EDITS, meta.pension_accrual.source");
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
  check("SYN, SYN_LINES, REKEY_LINE, ENTERPRISE_LINE, LR, LR_LINES and CONSTANTS.row8.c x RESPONSES.row8_factor are defined (:256-257, :359-371, :711-739)",
    P.SYN_LINES.length === 3 && [P.SYN.school, P.SYN.college, P.SYN.constants, P.REKEY_LINE, P.ENTERPRISE_LINE].every((x) => typeof x === "string")
    && !!P.LR && P.LR_LINES.length === 2 && Number.isFinite(row8), `row 8 ${row8.toFixed(4)}; SYN_LINES ${P.SYN_LINES.map((l) => l.id).join(", ")}`);
  // :271-284, v4's line gates as written (2026-10-07: this record had reconstructed pre-v4 code, a SYN_LINES-only
  // treatment; HEAD classes the state-price and road lines itself, :423-427).
  const SYN_IDS = new Set(P.SYN_LINES.map((l) => l.id));
  const STATE_PRICE_PARENT = Object.fromEntries(((payload.meta.state_pricing || {}).lines || []).map((x) => [x.line, x.parent]));
  const ROAD_LINES = new Set(P.componentsFor(null).filter((c) => c.key.kind === "part_rekeyed").map((c) => c.key.correction_line));
  check("v4's correction lines are the state-price and road lines (:281-282, as written): the payload's lines beyond SYN_LINES are meta.state_pricing's and the part_rekeyed components' correction lines",
    payload.lines.filter((l) => !SYN_IDS.has(l.id)).every((l) => STATE_PRICE_PARENT[l.id] || ROAD_LINES.has(l.id)), payload.lines.map((l) => l.id).join(", "));
  const v4Receipts = ["housing_enterprise_surplus", "tenant_occupied_property"];
  if (payload.receipt_lines.map((l) => l.id).sort().join() !== v4Receipts.slice().sort().join()) {
    needsCode(":283-284", `stops: the gate requires the receipt lines to be v4's two (${v4Receipts.join(", ")}); the payload carries item user_fees's ${P.ITEM_RECEIPT_LINES.length} carriers after them (${P.ITEM_RECEIPT_LINES.map((l) => l.id).join(", ")})`,
      "take v4's two receipt lines and meta.items' capital.receipt_lines (the carriers), each carrier with the offsets it keys under their targets (of_component)");
  }
  // :308-311, the lineage block: as written it must close the payload; on this case the edit sets follow it.
  const items = P.CASE_ITEMS.filter((r) => r.applied && r.edits);
  const lastAsWritten = E.first + E.count === payload.edits.length && JSON.stringify(payload.edits.slice(E.first)) === JSON.stringify(P.LINEAGE_EDITS)
    && E.row8_edit_index === payload.edits.length - 1;
  const located = JSON.stringify(payload.edits.slice(E.first, E.first + E.count)) === JSON.stringify(P.LINEAGE_EDITS)
    && E.row8_edit_index === E.first + E.count - 1 && payload.edits[E.row8_edit_index].line === P.SYN.constants
    && items.every((r, k) => r.edits.first === (k ? items[k - 1].edits.first + items[k - 1].edits.count : E.first + E.count))
    && JSON.stringify(payload.edits.slice(E.first + E.count)) === JSON.stringify(P.ITEM_EDITS);
  check("the lineage's edits are where meta.lineage.edits puts them (first, count, row 8 the last of them) and the edit sets' follow at meta.items' positions to the payload's end (exact)",
    located, `lineage ${E.first} + ${E.count}, row 8 at ${E.row8_edit_index}; ${items.map((r) => `${r.id} ${r.edits.first} + ${r.edits.count}`).join(", ")}`);
  if (!lastAsWritten) needsCode(":308-311", `the gate requires the lineage's ${E.count} edits to close the payload with row 8 last; ${payload.edits.length - E.first - E.count} edit-set edits follow them (meta.items)`,
    "compare CORR.edits.slice(E.first, E.first + E.count) with P.LINEAGE_EDITS, row 8 at E.row8_edit_index, and decompose the tail by meta.items (each edit set's first and count; item pension_tr2026's parts put its lineage parts with lin)");
  // :286-290, the pension source: as written it hashes the 2025 lane's file against meta.pension_accrual.source.
  const ACC = payload.meta.pension_accrual, OLD = "pension_accrual_2026_09_28/derived/summary.json";
  check("meta.pension_accrual.source names its file, and the file's sha256 is the one stamped (the pin a consumer re-sources from)",
    sha(ACC.source.file) === ACC.source.sha256 && sha(ACC.source.case_file) === ACC.source.case_sha256 && ACC.source.builds_on.sha256 === sha(OLD),
    `${ACC.source.file} at ${ACC.source.commit}, arm ${ACC.source.arm}; builds_on ${ACC.source.builds_on.commit}`);
  if (sha(OLD) !== ACC.source.sha256) needsCode(":286-290", `the gate hashes ${OLD} against meta.pension_accrual.source.sha256, which is now ${ACC.source.file}'s; the ratio_net identity (gross x (1 - future share)) and RATIO_NATIONAL (:291-299) are the 2025 lane's`,
    "read the pension inputs from meta.pension_accrual.source and .paths (the 2025 lane's pin is .source.builds_on) and the ratio's construction from the pension_tr2026 lane's summary.json; the lineage's own accrual takes item pension_tr2026's lineage parts");
}

// ---------------------------------------------------------------------------------------------------
pattern("within_group_distribution_2026_09_29/export_lines.cjs", "94-112, 126-155, 280-304 (HEAD b7c453a9)",
  "dump(): evaluateFull(m, spec), stateFor(withSyntheticLines(m), spec): fiscal_weight, receipt_scenario, production, count_production; the pension gate on LINEAGE_EDITS and meta.pension_accrual");
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
  check("the corrected union reproduces the case (:40-41, 1e-4 against the adopted row)",
    Math.abs(uCost[lo] - published.adopted[0]) < 1e-4 && Math.abs(uCost[hi] - published.adopted[1]) < 1e-4, `${f4([uCost[lo], uCost[hi]])} at ${lo} / ${hi}`);
  let gap = 0, n = 0;
  for (const m of [unionModel].concat(GENS.map((g) => genModels[g]))) for (const i of [lo, hi]) {
    const d = dump(m, P.MAIN_SPECS[i]);
    gap = Math.max(gap, Math.abs(d.sum_bn - d.cost_bn));
    n += 1;
    if (!(d.state.production && typeof d.state.receipt_scenario === "string" && Number.isFinite(d.state.fiscal_weight))) gap = Infinity;
  }
  check("rows, capital and production sum to evaluateFull()'s cost, on the union and the generation models (:71, :80, :92; 1e-9)", gap < 1e-9, `${n} dumps, max |diff| ${e1(gap)}`);
  // :94-103, capRule as written: each component's key rule from the case's payload (meta.capital_return.components),
  // compared with the capital lane's engine_components.json only on September 27 (2026-10-07: this record had
  // reconstructed older code that read engine_components.json on every case).
  const capRule = Object.fromEntries(payload.meta.capital_return.components.map((c) => [c.id, c.key]));
  const evIds = [...new Set([lo, hi].flatMap((i) => P.evaluateFull(unionModel, P.MAIN_SPECS[i]).capital.components.map((c) => c.id)))];
  check("capRule (:97) keys every component the evaluation returns, item user_fees's offsets included, by the case's own key rule (componentsFor(null))",
    evIds.every((id) => capRule[id]) && P.componentsFor(null).every((c) => JSON.stringify(capRule[c.id]) === JSON.stringify(c.key)), `${evIds.length} components`);
  // :280-304 (the gate at :302) as written, on the model cells at each end's allocation: the union's accrual less the lineage's own (from
  // LINEAGE_EDITS) is the payload's ratio_net x the identified union's OASDI receipts, and its Part A accrual
  // part_a_accrual_bn. On this case it misses by item pension_tr2026's lineage parts, which the gate must count as the
  // lineage's own.
  const PA = payload.meta.pension_accrual, cashModel = P.CASH.payloadModel(), m29 = P.SEPT29.payloadModel(), REF = MODEL.receipts.reference;
  const LS = P.LINEAGE_EDITS, LC = P.CASH.LINEAGE_EDITS;
  const it1 = P.CASE_ITEMS.find((r) => r.id === "pension_tr2026");
  const grp = (m, id, a) => { const l = m.spending.lines.find((x) => x.id === id); return l.keys[l.preferred_key][a].target_bn; };
  const rcp = (m, id, a) => m.receipts.lines.find((l) => l.id === id).cells[REF][a].target_bn;
  const lin = (edits, id, key, a) => edits.filter((e) => e.side === "spending" && e.line === id && e.key === key).reduce((s, e) => s + e.by[a], 0);
  const key = (id) => unionModel.spending.lines.find((l) => l.id === id).preferred_key;
  let fixGap = 0;
  const misses = [];
  for (const [end, i] of [["low", lo], ["high", hi]]) {
    const a = P.MAIN_SPECS[i].allocation;
    const O = PA.oasdi_lines.reduce((s, id) => s + rcp(m29, id, a), 0) + PA.se_oasdi_share * rcp(m29, PA.se_line, a);
    const union = { accrual: grp(unionModel, "social_security", a), part_a: grp(unionModel, "medicare", a) - (1 - PA.part_a_share) * grp(cashModel, "medicare", a) };
    const own = { accrual: lin(LS, "social_security", key("social_security"), a),
      part_a: lin(LS, "medicare", key("medicare"), a) - (1 - PA.part_a_share) * lin(LC, "medicare", key("medicare"), a) };
    const want = { accrual: PA.ratio_net * O, part_a: PA.part_a_accrual_bn };
    const miss = { accrual: union.accrual - own.accrual - want.accrual, part_a: union.part_a - own.part_a - want.part_a };
    const fix = { accrual: it1.parts.lineage_oasdi.by[a], part_a: it1.parts.lineage_part_a.by[a] };
    fixGap = Math.max(fixGap, Math.abs(miss.accrual - fix.accrual), Math.abs(miss.part_a - fix.part_a));
    misses.push(`${end} (${a}): accrual ${miss.accrual.toFixed(6)}, Part A ${miss.part_a.toFixed(6)}`);
  }
  check("as written, the gate misses by exactly item pension_tr2026's lineage parts (meta.items parts lineage_oasdi, lineage_part_a; 1e-9)", fixGap < 1e-9,
    `${misses.join("; ")}; max |miss - parts| ${e1(fixGap)}`);
  needsCode(":280-304 (the gate at :302)", `the gate "the union's accrual less the lineage's own is the September 29 payload's" misses on this case (${misses.join("; ")}bn)`,
    "count item pension_tr2026's lineage parts (meta.items, pension_tr2026 parts lineage_oasdi and lineage_part_a, at the end's allocation) in own; the payload's ratio_net and part_a_accrual_bn are the 2026 inputs'");
}

// ---------------------------------------------------------------------------------------------------
pattern("sept24_propagation_2026_09_24/band_variants.cjs", "250-320, 436-460 (HEAD b7c453a9)",
  "specifications rebuilt from P24.MAIN_SPECS and meta.responses, P.specsFor({rates}), P.specsFor({enterprises: \"A\"}), Engine.applyCorrections(MODEL, payload); the cash set's meta and the edit layout");
{
  const canon = (x) => JSON.stringify(x, (k, v) => (v && typeof v === "object" && !Array.isArray(v)
    ? Object.fromEntries(Object.keys(v).sort().map((kk) => [kk, v[kk]])) : v));
  const r = payload.meta.responses, cap = payload.meta.capital_return;
  check("the payload's meta.responses equal the case's summary.json responses (:258)", JSON.stringify(r) === JSON.stringify(summary.responses));
  const rebuild = (lineResponses) => P.P24.MAIN_SPECS.map((s) => {
    const low = s.gg === P.GG24[0], reading = low ? "low" : "high";
    return { ...s, gg: low ? r.general_government.low : r.general_government.high, school: s.school === P.SCHOOL24[0] ? r.school.growth : r.school.decline,
      reading, rate: cap.rates[reading], long_run: r[P.LR_LINES[0]].variant, enterprises: cap.enterprises, line_responses: lineResponses(reading) };
  });
  // HEAD's rebuild (:260-269, since 911afa6f) takes every meta.responses entry (lineResponsesAt), as this does; an
  // earlier version of this pattern reconstructed the pre-v4 rebuild (4 of 13 line responses) and recorded it as
  // failing, which HEAD's code does not do.
  const specs = rebuild((reading) => Object.fromEntries(Object.entries(P.LINE_RESPONSES).map(([k, e]) => [k, e[reading]])));
  check("specifications rebuilt from every meta.responses entry (P.LINE_RESPONSES) at the reading equal MAIN_SPECS, as :260-269 gates them (HEAD)", canon(specs) === canon(P.MAIN_SPECS));
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
  check("on the September 27 payload the rebuild as written equals forPayload()'s MAIN_SPECS (:269)", canon(specs27) === canon(F27.MAIN_SPECS));
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
  check("this case: the uncorrected run reproduces uncorrected_at_adopted_responses and the corrected run main_case (summary.json 1e-9, main_case_bands.csv 1e-4) (:431-432)",
    worst(bu.map((x, j) => x - summary.uncorrected_at_adopted_responses[j])) < 1e-9 && worst(bc.map((x, j) => x - summary.main_case[j])) < 1e-9
    && worst(bu.map((x, j) => x - published.uncorrected_at_adopted_responses[j])) < 1e-4 && worst(bc.map((x, j) => x - published.adopted[j])) < 1e-4,
    `${f4(bu)}; ${f4(bc)}`);
  // The consumer's gates (:444-454): every variant moves the corrected model as the uncorrected one. It holds on the
  // September 29 payload. On the item base the added people are priced on every key of a line (the lineage lane's
  // cells), so a variant that picks another key (the justice coding, uninsured use at 0.7) moves their part too (v5's
  // statement). On this case item retiree_health also moves the national totals of public_order_safety and
  // health_services, the lines every variant here edits, which the capital keys and the state prices divide by; item
  // pension_tr2026's cell shifts on social_security and medicare move no variant.
  const movesOf = (va, vb) => BV.slice(1).map(([name]) => [name, worst(va[name].map((x, i) => (x - va.adopted[i]) - (vb[name][i] - vb.adopted[i])))]);
  const moveGapOf = (va, vb) => Math.max(...movesOf(va, vb).map(([, g]) => g));
  const v29 = runVariants(P, P.SEPT29.payloadModel(), specs);
  const gap29 = moveGapOf(vu, v29), gap6 = moveGapOf(vu, vc);
  check("the September 29 payload model, at this case's specifications: every variant moves every specification as on the uncorrected model (:450, 1e-9)",
    gap29 < 1e-9, `${BV.length - 1} variants, max gap ${e1(gap29)}`);
  const vB = runVariants(P, P.ITEM_BASE.payloadModel(), specs);
  const ownB = movesOf(vB, v29).filter(([, g]) => g >= 1e-9);
  check("the item base moves as the September 29 payload but for the variants that pick another key, where the added people's own cells move (v5's statement, 1e-9)",
    ownB.length > 0 && ownB.every(([name]) => /raw_coding|uncompensated_use/.test(name)), ownB.map(([n, g]) => `${n} up to ${g.toFixed(4)}`).join("; "));
  const Q1 = P.caseOf(P.OCT05, ["pension_tr2026", "added_age_mix"]);
  const v1 = runVariants(P, Q1.payloadModel(), specs);
  const g1 = moveGapOf(v1, vB), byItems = movesOf(vc, vB);
  const touched = [...new Set(P.ITEM_EDITS.filter((e) => e.national_bn !== undefined).map((e) => e.line))];
  check("item pension_tr2026 leaves every variant's move as the item base's (1e-9); the rest of this case's extra move is item retiree_health's, on lines it scales (public_order_safety, health_services)",
    g1 < 1e-9 && ["public_order_safety", "health_services"].every((id) => touched.includes(id)),
    `pension_tr2026 ${e1(g1)}; with retiree_health: ${byItems.map(([n, g]) => `${n} ${g.toFixed(4)}`).join("; ")}`);
  // HEAD's gate (b7c453a9, header :68-73) is split: the September 29 payload moves as the uncorrected model, and the
  // case by that plus the lineage's own move (its edits on the variant's key less those on the case's key). That split
  // passes on oct05 (prop-c's run, 2026-10-07: band_variants.cjs --case oct05, 67 gates). On this case it misses by the
  // edit sets' move of the variants: the case's move less the item base's. The unsplit gap (gap6, up to 0.0583bn) is
  // mostly the lineage's own move, which HEAD already splits off; an earlier version of this record reported that
  // unsplit gap as the failure.
  const gI = moveGapOf(vc, vB);
  if (gI >= 1e-9) needsCode(":450-454 (the split move gate, header :68-73)", `the split gate misses on this case by the edit sets' move of the variants, up to ${gI.toFixed(4)}bn (${byItems.filter(([, g]) => g >= 1e-9).map(([n, g]) => `${n} ${g.toFixed(4)}`).join(", ")}): item retiree_health's scaling of public_order_safety's and health_services's national totals, which the capital keys and state prices divide by (the lineage's own move is v5's rule; unsplit, the gap is ${gap6.toFixed(4)}bn)`,
    "add the edit sets' move to the split: the case's move less the item base's (P.ITEM_BASE.payloadModel() at the same variant), or run the September 29 control with P.ITEM_EDITS applied");
  // :303-305 as written: the cash set's payload has the set's responses, capital return and state pricing.
  check("the cash set's payload has the case payload's meta.responses, capital_return and state_pricing, as the gate is written (:303-305)",
    ["responses", "capital_return", "state_pricing"].every((k) => JSON.stringify(cashPayload.meta[k]) === JSON.stringify(payload.meta[k])));
  check("the package's cash set (CASH) has the cash set's payload, exactly (:308)", canon(P.CASH.correctionsPayload()) === canon(cashPayload));
  // :312-320 as written: the payload is the September 29 payload with the lineage's edits appended, and nothing after.
  const p29 = P.SEPT29.correctionsPayload(), n29 = p29.edits.length, nL = P.LINEAGE_EDITS.length;
  const layoutAsWritten = canon(payload.edits.slice(0, n29)) === canon(p29.edits) && payload.edits.length === n29 + nL
    && canon(payload.edits.slice(n29)) === canon(P.LINEAGE_EDITS) && payload.meta.lineage.edits.first === n29;
  const layout = canon(payload.edits.slice(0, n29)) === canon(p29.edits) && canon(payload.edits.slice(n29, n29 + nL)) === canon(P.LINEAGE_EDITS)
    && canon(payload.edits.slice(n29 + nL)) === canon(P.ITEM_EDITS) && payload.meta.lineage.edits.first === n29;
  check("the case's payload is the September 29 payload, then the lineage's edits (meta.lineage.edits), then the edit sets' (meta.items, ITEM_EDITS) (exact)",
    layout, `${n29} + ${nL} + ${P.ITEM_EDITS.length} edits`);
  if (!layoutAsWritten) needsCode(":312-320", `the gate requires the payload's edits to be the September 29 payload's ${n29} and the lineage's ${nL} only; ${P.ITEM_EDITS.length} edit-set edits follow (meta.items)`,
    "compare payload.edits.slice(n29, n29 + P.LINEAGE_EDITS.length) with P.LINEAGE_EDITS and the tail with P.ITEM_EDITS; lineageBy (:339) stays on P.LINEAGE_EDITS, and the variant decomposition counts item retiree_health's scaling of the variant's key as the case's own move");
}

// ---------------------------------------------------------------------------------------------------
pattern("main_case_2026_10_05/package.cjs", "viaCandidate, followNationals (the guard)",
  "an item variant through the package's API: withCentral(o), modelFor, specsFor(o), evaluateFull; v6: withItems after the lineage");
{
  const V4 = P.V4PKG;
  const o = { roads: V4.OFF.roads };
  const oo = P.withCentral(o);
  const mv = P.modelFor("central", METHODS[0], oo);
  const sv = P.specsFor(o);
  const sv4 = V4.specsFor(V4.withCentral(Object.assign({}, P.ITEMS, o)));
  // The route: candidate v4's evaluation at the moved specification, every capital component candidate v4's but the
  // long-run ones, which take v5's subfunction responses.
  const rules = new Map(P.componentsFor(null).map((c) => [c.id, c.response]));
  let evalGap = 0, capOther = 0, capLong = 0, nLong = 0, unknown = 0, nItem = 0;
  const ITEM_COMPS = new Set(P.ITEM_COMPONENTS.map((c) => c.id));
  sv.forEach((s, i) => {
    const a = P.evaluateFull(mv, s), b = V4.evaluateFull(mv, P.moveSpec(sv4[i], oo));
    evalGap = Math.max(evalGap, Math.abs(a.evaluation.welfare_bn - b.evaluation.welfare_bn));
    for (const c of a.capital.components) {
      const x = b.capital.components.find((y) => y.id === c.id), rule = rules.get(c.id);
      // An edit set's own capital components (item user_fees's offsets) come after candidate v4's.
      if (!x) { if (ITEM_COMPS.has(c.id)) nItem += 1; else unknown += 1; continue; }
      if (rule && rule.kind === "long_run_subfunction") {
        nLong += 1;
        capLong = Math.max(capLong, Math.abs(c.response - P.subfunctionResponses(s.long_run, s.reading)[rule.subfunction]), Math.abs(c.key - x.key));
      } else capOther = Math.max(capOther, Math.abs(c.return_bn - x.return_bn), Math.abs(c.key - x.key), Math.abs(c.response - x.response));
    }
  });
  check(`the roads item off (${JSON.stringify(o)}): evaluateFull on its model (the edit sets applied) and specsFor(o)'s specifications is candidate v4's at the moved specification, the long-run capital at v5's subfunction responses (exact)`,
    evalGap === 0 && capOther === 0 && capLong === 0 && nLong > 0 && unknown === 0, `${sv.length} specifications; ${nLong} long-run components; ${nItem} edit-set components beside candidate v4's; specification fields ${Object.keys(sv[0]).length}, as MAIN_SPECS' ${Object.keys(P.MAIN_SPECS[0]).length}`);
  // With an item off, the lineage's edits on the lines it removes go, and the added people keep their key (amount over
  // national) on every other line, the merged receipts included: on ITEM_BASE, the lineage's edits with no edit set.
  const IB = P.ITEM_BASE;
  const natOf = (m) => new Map(m.spending.lines.map((l) => ["spending:" + l.id, l.national_bn]).concat(m.receipts.lines.map((l) => ["receipt:" + l.id, l.national_bn])));
  const cellsOf = (m) => {
    const out = new Map();
    for (const l of m.receipts.lines) for (const [sc, c] of Object.entries(l.cells)) for (const a of P.ALLOCS) out.set(`receipt:${l.id}|${sc}|${a}`, c[a].target_bn);
    for (const l of m.spending.lines) for (const [k, c] of Object.entries(l.keys)) for (const a of P.ALLOCS) out.set(`spending:${l.id}|${k}|${a}`, c[a].target_bn);
    return out;
  };
  const addedKeys = (m5, m4) => { const n = natOf(m5), c5 = cellsOf(m5), c4 = cellsOf(m4);
    return new Map([...c5].filter(([k]) => c4.has(k) && n.get(k.split("|")[0]) !== 0).map(([k, v]) => [k, (v - c4.get(k)) / n.get(k.split("|")[0])])); };
  const caseKeys = addedKeys(IB.modelFor("central", METHODS[0], IB.withCentral({})), P.BASE.modelFor("central", METHODS[0], P.BASE.withCentral({})));
  const offRows = [], onCase = [];
  let keyGap = 0;
  for (const it of V4.SET_ITEMS.filter((x) => x.id !== "pension")) {
    const io = V4.offOf(it.o), ioo = P.withCentral(io);
    const m4 = P.BASE.modelFor("central", METHODS[0], ioo), m5 = IB.modelFor("central", METHODS[0], ioo);
    const gone = [...natOf(P.BASE.modelFor("central", METHODS[0], P.BASE.withCentral({}))).keys()].filter((k) => !natOf(m4).has(k));
    const keys = addedKeys(m5, m4);
    let g = 0;
    for (const [cell, x] of keys) { const want = caseKeys.get(cell); if (want !== undefined) g = Math.max(g, Math.abs(x - want)); }
    keyGap = Math.max(keyGap, g);
    offRows.push(`${it.id} off${gone.length ? ` (removes ${gone.map((k) => k.split(":")[1]).join(", ")})` : ""}`);
    const why = throws(() => P.modelFor("central", METHODS[0], ioo));
    onCase.push({ item: it.id, builds: !why, why });
  }
  check("on ITEM_BASE, each v4 item off (the pension switch apart: the cash set, P.CASH): the model builds, and the added people's key is the case's in every cell it keeps (1e-12)",
    keyGap < 1e-12, `${offRows.join("; ")}; max |diff| ${e1(keyGap)}`);
  const stops = onCase.filter((x) => !x.builds);
  check("on this case, each v4 item off builds with the edit sets after the lineage, or stops ([BLOCKED]) naming the fixed-amount item whose line it moves",
    stops.every((x) => x.why.includes("[BLOCKED]") && /item (pension_tr2026|user_fees) edits by fixed amounts/.test(x.why)),
    `${onCase.length - stops.length} of ${onCase.length} build${stops.length ? `; stop: ${stops.map((x) => `${x.item} (${x.why})`).join("; ")}` : ""}`);
  const pension = throws(() => P.modelFor("central", METHODS[0], P.withCentral(V4.offOf({ pension4: P.ITEMS.pension4 }))));
  check("the pension switch off stops ([BLOCKED]): the lineage there is the cash payload's, through P.CASH", !!pension && pension.includes("[BLOCKED]") && pension.includes("P.CASH"), pension);
  const copied = throws(() => P.evaluateFull(mv, Object.assign({}, sv[0])));
  const crossed = throws(() => P.evaluateFull(mv, P.MAIN_SPECS[0]));
  check("a copy of the variant's specification stops ([BLOCKED])", !!copied && copied.includes("[BLOCKED]"), copied);
  check("the case's specification on the variant's model stops ([BLOCKED])", !!crossed && crossed.includes("[BLOCKED]"), crossed);
}

// ---------------------------------------------------------------------------------------------------
pattern("main_case_2026_10_07/package.cjs", "caseOf, forItems, REGISTRY (the item API)",
  "caseOf(OCT05, ids, arms), meta.items, CASE_ITEMS, ITEM_EDITS, ITEM_BASE, LINEAGE_PAYLOADS, withItems(m), CASH, checkBuilt, checkLineage");
{
  const cost = (m, s) => P.evaluateFull(m, s, P.MAIN_PROFILE).cost_bn;
  // With no item the case is v5's.
  const Z = P.caseOf(P.OCT05, []);
  check("caseOf(OCT05, []) is v5: its payloads are v5's derived files, its names v5's, no item (exact)",
    JSON.stringify(Z.correctionsPayload()) === JSON.stringify(payload5) && JSON.stringify(Z.CASH_PAYLOAD) === JSON.stringify(cashPayload5)
    && Z.LANE === OCT05 && Z.ADOPTED === P.OCT05.ADOPTED && Z.CASE_ITEMS.length === 0 && Z.ITEM_EDITS.length === 0, `${Z.LANE}, adopted ${Z.ADOPTED}`);
  // The stamps and the registry.
  check("the payloads are stamped as adopted: source package.cjs, adopted 2026-10-07, the decision (its file exists), v5's status form, the case key oct07; a variant (an arm) is stamped adopted null",
    [payload, cashPayload].every((p) => p.meta.source === `${LANE}/package.cjs` && p.meta.adopted === "2026-10-07" && p.meta.decision === P.V6.DECISION)
      && payload.meta.status.startsWith(`adopted 2026-10-07 (${P.V6.DECISION}): `) && cashPayload.meta.status.startsWith("the cash set of the case adopted 2026-10-07 (")
      && fs.existsSync(path.join(FISCAL, "..", "..", P.V6.DECISION)) && P.CASE_KEY === "oct07" && P.STATUS === "adopted" && P.ADOPTED === "2026-10-07"
      && (() => { const V = P.caseOf(P.OCT05, P.CANDIDATE, { retiree_health: "mu_low" }); return V.ADOPTED === null && V.correctionsPayload().meta.adopted === null
        && V.correctionsPayload().meta.status.startsWith("variant: "); })(), P.V6.DECISION);
  check("REGISTRY lists the items in edit order; CANDIDATE is all of them; SLOTS describe lineage_count and split_line",
    JSON.stringify(P.REGISTRY.map((x) => x.id)) === JSON.stringify(["pension_tr2026", "retiree_health", "added_age_mix", "user_fees"])
    && JSON.stringify(P.CANDIDATE) === JSON.stringify(P.ITEM_IDS) && JSON.stringify(Object.keys(P.SLOTS)) === JSON.stringify(["lineage_count", "split_line"])
    && Object.values(P.SLOTS).every((s) => s.what && s.why_not_an_edit_set && s.needs.length), P.REGISTRY.map((x) => `${x.id} (${x.kind})`).join(", "));
  // meta.items locates every edit set's edits; the parts add to their edits.
  for (const [w, pl, api, base] of [["set", payload, P, P.ITEM_BASE], ["cash", cashPayload, P.CASH, P.ITEM_BASE.CASH]]) {
    const n = base.correctionsPayload().edits.length;
    const recs = pl.meta.items.filter((r) => r.applied && r.edits);
    const seg = recs.flatMap((r) => pl.edits.slice(r.edits.first, r.edits.first + r.edits.count));
    check(`${w}: meta.items is CASE_ITEMS; each edit set's first and count locate its edits, which follow the item base's ${n} in registry order and are ITEM_EDITS (exact)`,
      JSON.stringify(pl.meta.items) === JSON.stringify(api.CASE_ITEMS) && recs.every((r, k) => r.edits.first === (k ? recs[k - 1].edits.first + recs[k - 1].edits.count : n))
      && JSON.stringify(seg) === JSON.stringify(pl.edits.slice(n)) && JSON.stringify(seg) === JSON.stringify(api.ITEM_EDITS)
      && JSON.stringify(pl.edits.slice(0, n)) === JSON.stringify(base.correctionsPayload().edits),
      recs.map((r) => `${r.id} ${r.edits.first} + ${r.edits.count}`).join(", "));
    let partGap = 0, nParts = 0;
    for (const r of recs) {
      const sums = {};
      for (const p of Object.values(r.parts || {})) { nParts += 1; for (const a of P.ALLOCS) sums[`${p.edit}|${a}`] = (sums[`${p.edit}|${a}`] || 0) + p.by[a]; }
      pl.edits.slice(r.edits.first, r.edits.first + r.edits.count).forEach((e, j) => {
        if (e.by && Object.keys(r.parts || {}).length) for (const a of P.ALLOCS) partGap = Math.max(partGap, Math.abs(sums[`${j}|${a}`] - e.by[a]));
      });
    }
    check(`${w}: each edit set's parts add to its cell shifts exactly (the union and lineage parts, per allocation)`, partGap === 0, `${nParts} parts`);
  }
  const pen = cashPayload.meta.items.find((r) => r.id === "pension_tr2026");
  check("the cash set: item pension_tr2026 does not apply (applied false, with its reason); retiree_health, added_age_mix and user_fees do; CASH_PAYLOAD is corrections_cash.json",
    pen.applied === false && typeof pen.why === "string" && JSON.stringify(cashPayload.meta.items.filter((r) => r.applied).map((r) => r.id)) === JSON.stringify(["retiree_health", "added_age_mix", "user_fees"])
    && JSON.stringify(P.CASH_PAYLOAD) === JSON.stringify(cashPayload) && !("pension_accrual" in cashPayload.meta), pen.why);
  // The lineage base and its additions.
  const LP = { set: readJson(P.LINEAGE_PAYLOADS.set), cash: readJson(P.LINEAGE_PAYLOADS.cash) };
  check("ITEM_BASE.ADDITION is derived/lineage_payload.json and lineage_payload_cash.json, which meta.lineage.payload names (exact)",
    JSON.stringify(P.ITEM_BASE.ADDITION.set) === JSON.stringify(LP.set) && JSON.stringify(P.ITEM_BASE.ADDITION.cash) === JSON.stringify(LP.cash)
    && payload.meta.lineage.payload === P.LINEAGE_PAYLOADS.set && cashPayload.meta.lineage.payload === P.LINEAGE_PAYLOADS.cash,
    `${P.LINEAGE_PAYLOADS.set}, ${P.LINEAGE_PAYLOADS.cash}`);
  const EC = cashPayload.meta.lineage.edits;
  check("LINEAGE_EDITS (set and cash) are the payloads' meta.lineage.edits blocks and the additions' edits (exact)",
    JSON.stringify(P.LINEAGE_EDITS) === JSON.stringify(payload.edits.slice(E.first, E.first + E.count)) && JSON.stringify(P.LINEAGE_EDITS) === JSON.stringify(LP.set.edits)
    && JSON.stringify(P.CASH.LINEAGE_EDITS) === JSON.stringify(cashPayload.edits.slice(EC.first, EC.first + EC.count)) && JSON.stringify(P.CASH.LINEAGE_EDITS) === JSON.stringify(LP.cash.edits),
    `${P.LINEAGE_EDITS.length} edits each; meta.lineage.age_mix: ${payload.meta.lineage.age_mix.reading}, ${payload.meta.lineage.age_mix.route}`);
  // withItems() on a consumer's model of the item base gives the case.
  for (const [w, api, base] of [["set", P, P.ITEM_BASE], ["cash", P.CASH, P.ITEM_BASE.CASH]]) {
    const mB = Engine.applyCorrections(MODEL, base.correctionsPayload());
    const mI = api.withItems(mB), mP = api.payloadModel();
    const g = worst(P.MAIN_SPECS.map((s) => cost(mI, s) - cost(mP, s)));
    check(`${w}: withItems() on a consumer's model of the item base (model.json + ITEM_BASE's payload) is this case at every specification (1e-9)`, g < 1e-9, `max |diff| ${e1(g)}`);
  }
  // The fixed-amount guard and editsAt().
  const mB = Engine.applyCorrections(MODEL, P.ITEM_BASE.correctionsPayload());
  const nat = (m, id) => m.spending.lines.find((l) => l.id === id).national_bn;
  const moveLine = (m, id, f) => Engine.applyCorrections(m, { edits: [{ side: "spending", line: id, national_bn: nat(m, id) * f }], meta: m.corrections });
  const stop = throws(() => P.withItems(moveLine(mB, "social_security", 1.01)));
  check("withItems() on a model that moves social_security's national total stops ([BLOCKED]): item pension_tr2026 edits it by fixed amounts",
    !!stop && stop.includes("[BLOCKED]") && stop.includes("pension_tr2026"), stop);
  const RH = P.ITEM_DETAIL.retiree_health.set, L0 = "education_services";
  // On the case, user_fees edits education_services by fixed amounts after retiree_health, against the case's totals at
  // its step, so a moved total stops there; retiree_health without it follows the model.
  const stopFees = throws(() => P.withItems(moveLine(mB, L0, 1.01)));
  const QR = P.caseOf(P.OCT05, ["retiree_health"]), mBR = Engine.applyCorrections(MODEL, QR.ITEM_BASE.correctionsPayload());
  const m2 = moveLine(mBR, L0, 1.01), out = QR.withItems(m2);
  check(`item retiree_health follows a moved national total (editsAt): ${L0} ends at the model's total plus the item's change (exact); on the case the move stops at user_fees ([BLOCKED]), which edits ${L0} by fixed amounts against the case's totals at its step`,
    RH.lines.includes(L0) && nat(out, L0) === nat(m2, L0) + RH.delta[L0] && !!stopFees && stopFees.includes("[BLOCKED]") && stopFees.includes("user_fees"),
    `${nat(m2, L0).toFixed(3)} + ${RH.delta[L0].toFixed(3)} = ${nat(out, L0).toFixed(3)}; ${stopFees}`);
  // Item user_fees's capital: carriers after the receipt lines, offsets after the components, zero where the item is not
  // applied, dropped where an option re-keys the component; a second application stops.
  const UF = P.CASE_ITEMS.find((r) => r.id === "user_fees");
  if (UF) {
    const nR = payload5.receipt_lines.length, nK = payload5.meta.capital_return.components.length;
    check("item user_fees: both payloads carry its carrier lines after v5's receipt lines and its offset components after v5's components (ITEM_RECEIPT_LINES, ITEM_COMPONENTS; meta.items names them); componentsFor(null) is meta.capital_return.components (exact)",
      [[payload, P], [cashPayload, P.CASH]].every(([pl, api]) => JSON.stringify(pl.receipt_lines.slice(nR)) === JSON.stringify(api.ITEM_RECEIPT_LINES)
        && JSON.stringify(pl.meta.capital_return.components.slice(nK)) === JSON.stringify(api.ITEM_COMPONENTS)
        && JSON.stringify(api.componentsFor(null)) === JSON.stringify(pl.meta.capital_return.components)
        && JSON.stringify(pl.meta.items.find((r) => r.id === "user_fees").capital.receipt_lines) === JSON.stringify(api.ITEM_RECEIPT_LINES.map((l) => l.id))
        && JSON.stringify(pl.meta.items.find((r) => r.id === "user_fees").capital.components) === JSON.stringify(api.ITEM_COMPONENTS.map((c) => c.id))),
      `${P.ITEM_RECEIPT_LINES.map((l) => l.id).join(", ")}; ${P.ITEM_COMPONENTS.map((c) => c.id).join(", ")}`);
    const ucR = P.MAIN_SPECS.map((s) => P.evaluateFull(MODEL, s, P.MAIN_PROFILE));
    const zeroOk = ucR.every((r) => P.ITEM_COMPONENTS.every((c) => { const x = r.capital.components.find((y) => y.id === c.id); return x && x.key === 0 && x.return_bn === 0; }));
    // Item user_fees alone, so the stop is the carriers' (on the case, retiree_health's second scaling stops it first).
    const QF = P.caseOf(P.OCT05, ["user_fees"]), twice = throws(() => QF.withItems(QF.payloadModel()));
    const mS = P.withSyntheticLines(Engine.applyCorrections(MODEL, P.ITEM_BASE.correctionsPayload()));
    const gS = worst(P.MAIN_SPECS.map((s) => cost(P.withItems(mS), s) - cost(P.payloadModel(), s)));
    check("on a model without the item (model.json) its carriers enter at zero and its offsets return 0; withItems() on a withSyntheticLines() model of the item base replaces the zero carriers and is this case (1e-9); withItems() of the item alone on its own payload model stops ([BLOCKED]: the carriers are there with amounts)",
      zeroOk && gS < 1e-9 && !!twice && twice.includes("[BLOCKED]") && twice.includes("already"), `max |diff| ${e1(gS)}; ${twice}`);
    const pupil = P.componentsFor("k12_at_pupil_share").map((c) => c.id);
    check("under the pupil-share variant (k12 keyed by a constant) the k12 offset drops and the college and health offsets stay",
      !pupil.includes("k12_user_fees") && ["college_user_fees", "health_sl_user_fees", "health_fed_user_fees"].every((id) => pupil.includes(id)), pupil.filter((id) => id.endsWith("_user_fees")).join(", "));
    const stopH = throws(() => P.withItems(moveLine(mB, "other_federal_benefits", 1.01)));
    check("withItems() on a model that moves other_federal_benefits's national total stops at user_fees ([BLOCKED]): retiree_health follows it, user_fees's Pell edit is a fixed amount",
      !!stopH && stopH.includes("[BLOCKED]") && stopH.includes("user_fees"), stopH);
  }
  // Arms are options: the whole case at the arm.
  const arm = ["retiree_health", "mu_low"];
  const A = P.caseOf(P.OCT05, P.ITEM_IDS, { [arm[0]]: arm[1] });
  const bandA = spanOf(P.MAIN_SPECS.map((s) => cost(Engine.applyCorrections(MODEL, A.correctionsPayload()), s)));
  const rA = A.CASE_ITEMS.find((r) => r.id === arm[0]);
  check(`caseOf(OCT05, ITEM_IDS, {${arm[0]}: "${arm[1]}"}): its payload, applied by a consumer, gives main_case_bands.csv's ${arm.join("_")} row (1e-4); meta.items and meta.retiree_health name the arm`,
    worst(bandA.map((x, j) => x - published[arm.join("_")][j])) < 1e-4 && rA.arm === arm[1] && A.correctionsPayload().meta.retiree_health.arm === arm[1], f4(bandA));
  const badArm = throws(() => P.caseOf(P.OCT05, P.ITEM_IDS, { retiree_health: "no_such_arm" }));
  const badOrder = throws(() => P.caseOf(P.OCT05, ["retiree_health", "pension_tr2026"]));
  const badItem = throws(() => P.caseOf(P.OCT05, ["no_such_item"]));
  check("an unknown arm, an unknown item and items out of registry order stop ([BLOCKED])",
    [badArm, badOrder, badItem].every((x) => !!x && x.includes("[BLOCKED]")), [badArm, badOrder, badItem].join(" | "));
  // The guards: an edit set may not change reserved meta; a lineage addition may not move counts, responses or capital.
  const reserved = throws(() => P.checkBuilt({ id: "probe" }, { edits: [], meta: { lineage: {} } }, P.ITEM_BASE, "set"));
  check("an edit set that changes meta.lineage (reserved: the base's structure) stops ([BLOCKED])", !!reserved && reserved.includes("[BLOCKED]") && reserved.includes("meta.lineage"), reserved);
  const add = JSON.parse(JSON.stringify(P.ITEM_BASE.ADDITION));
  add.set.meta.lineage = Object.assign({}, add.set.meta.lineage, { probe_count: 1 });
  const slot = throws(() => P.checkLineage({ id: "probe" }, { additions: add, lineage_meta: {} }, P.OCT05));
  const same = throws(() => P.checkLineage({ id: "probe" }, { additions: JSON.parse(JSON.stringify(P.ITEM_BASE.ADDITION)), lineage_meta: {} }, P.OCT05));
  check("a lineage addition that moves meta.lineage (a count change) stops ([BLOCKED]: a count or C3 change is a lineage option, lineage_count.cjs); the age-mix addition passes",
    !!slot && slot.includes("[BLOCKED]") && slot.includes("lineage_count") && same === null, slot);
  // Lineage options: the whole case at another arm of the count or C3, a variant; with no item, v5's route at the option.
  // A consumer evaluates an option's payload with its own meta.responses (consumer.cjs), not at the case's.
  const Consumer = require(path.join(FISCAL, "main_case_candidate_v4_2026_09_29", "consumer.cjs"));
  const consumerBand = (pl) => spanOf(Consumer.evaluateAll(JSON.parse(JSON.stringify(pl)), { engine: Engine, model: MODEL }).map((x) => x.cost_bn));
  const opt = "arm_a", O = P.caseOf(P.OCT05, P.ITEM_IDS, P.ITEM_ARMS, opt), O0 = P.caseOf(P.OCT05, [], {}, opt);
  const bandO = consumerBand(O.correctionsPayload());
  const lin5 = readJson("main_case_lineage_2026_10_05/derived/v5_summary.json").sets.set.arms.a.band_bn;
  const band0 = consumerBand(O0.correctionsPayload());
  const badOpt = throws(() => P.caseOf(P.OCT05, P.ITEM_IDS, {}, "no_such_option"));
  check(`caseOf(OCT05, ITEM_IDS, {}, "${opt}"): a variant (adopted null, meta.lineage.count_option, no payload file) whose payload, applied by a consumer with its meta.responses (consumer.cjs), gives main_case_bands.csv's lineage_${opt} row (1e-4); with no item its payload gives the lineage lane's arm a band (1e-9); an unknown option stops ([BLOCKED])`,
    O.ADOPTED === null && O.correctionsPayload().meta.adopted === null && O.correctionsPayload().meta.lineage.count_option.name === opt
      && O.correctionsPayload().meta.lineage.payload === null && O.LINEAGE_OPTION === opt && worst(bandO.map((x, j) => x - published[`lineage_${opt}`][j])) < 1e-4
      && worst(band0.map((x, j) => x - lin5[j])) < 1e-9 && !!badOpt && badOpt.includes("[BLOCKED]"),
    `${f4(bandO)}; alone ${f4(band0)} against ${f4(lin5)}; ${badOpt}`);
}

// ---------------------------------------------------------------------------------------------------
const record = {
  gate: "G4: consumers' call patterns, as written, run against this package; a failing check is a package defect",
  pass: failures === 0,
  generation_pin: { commit: GEN_PIN, files: `${GEN_DIR}/model_{G1,G2,G3plus}.json, generation_corrections.json`, source: "world_ledger_2026_09_27/pins.json sept27.generation" },
  generation_pin_sept29: { commit: GEN29_PIN, files: `${GEN_DIR}/model_{G1,G2,G3plus}.json, generation_corrections_sept29.json, generation_corrections_sept29_cash.json`,
    source: "the last commit of generation_corrections_sept29*.json (run_generations_v4.cjs --case sept29)" },
  patterns,
  consumer_code: consumerCode,
};
fs.writeFileSync(path.join(HERE, "derived", "api_check.json"), JSON.stringify(record, null, 1) + "\n");
const n = patterns.reduce((a, p) => a + p.checks.length, 0);
console.log(failures ? `G4 FAIL: ${failures} of ${n} checks` : `G4 PASS: ${patterns.length} patterns, ${n} checks; ${consumerCode.length} consumer gates need code (listed)`);
if (failures) process.exitCode = 1;
