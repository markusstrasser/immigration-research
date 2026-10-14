/* G4, the API: consumers' call patterns, as they are written, run against this package (main case v7, the candidate) in a
 * harness inside the lane (so the lane's reruns repeat it). The patterns are v6's (main_case_2026_10_07/api_check.cjs),
 * each citing its consumer and repeating its calls and gates on this lane's package and derived files, as a path swap
 * would run them, with these changes for v7:
 *   - the case's specifications are the 32 personal ones (item personal_allocation): a consumer that iterates MAIN_SPECS
 *     gets the case's band; one that rebuilds the 64 from the September 24 package (patterns 2 and 7) is recorded, and
 *     its gate runs here on ALL_SPECS and on the personal slice;
 *   - pattern 3's generation split takes the v7 items' parts by their names (union_<G>: to generation G, lineage_ to G3+
 *     with the lineage), and prints at the case's ends (16 / 11);
 *   - pattern 4 adds v6 through OCT07 (the oct07_case row), and checks the line responses at each specification's
 *     reading; the consumer's own gate reads receipt overrides at their low response (:176), which it records when a
 *     receipt response differs by reading;
 *   - pattern 8 sets item job_capital_taxes's four receipt responses after candidate v4's evaluation (fixReceipts), as
 *     the package's variant route does;
 *   - pattern 9 is the item API on v7: v6's checks on its items, then the v7 layer (caseOn, the stamps, the registry,
 *     meta.items, the arms, the guards, lineage options with consumer.cjs reading meta.allocation);
 *   - new, pattern 10: the shared reading (SHARED_SPECS, ALL_SPECS, {allocation} on specsFor, evalPackage and central,
 *     the row shared_allocation) and the hard-coded end specifications, spans and pins the consumer sweep found (R5,
 *     recorded from reading the cited lines, basis "read").
 *
 * A check fails G4 when the package does not serve the call. A consumer gate that fails as written because the case
 * changed (the allocation rule, the v7 items' edits, parts and responses), not the API, is recorded under consumer_code
 * with the consumer's line, what it does today and the change it needs; those do not fail G4.
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
const LANE = "main_case_2026_10_14";
const OCT07 = "main_case_2026_10_07";
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
const payload6 = readJson(`${OCT07}/derived/corrections.json`);
const cashPayload6 = readJson(`${OCT07}/derived/corrections_cash.json`);
const ENDS7 = summary.v7.end_specifications.set;
const STUB = P.CREDITS.S.stub || P.JOBCAP.S.stub;
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
// basis: "run" when this check ran the consumer's call pattern and the gate as written failed or misattributed; "read"
// when the finding comes from reading the cited lines (R5), not from running them.
function needsCode(line, today, change, consumer, basis = "run") {
  consumerCode.push({ consumer: consumer || current.consumer, line, today, change, basis });
  console.log(`  CODE${basis === "read" ? " [read]" : ""} ${consumer || current.consumer} at ${line}: ${today} -> ${change}`);
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
  // As written (:94-104) the rebuild runs over the September 24 package's 64 and compares them with MAIN_SPECS one for
  // one; on v7 MAIN_SPECS holds the 32 personal ones, so the rebuild matches ALL_SPECS and, filtered by
  // meta.allocation.group_total, MAIN_SPECS.
  const rows64 = P24.MAIN_SPECS.map((s, i) => ({ ...s,
    gg: swap(s.gg, GG24, [R.general_government.low, R.general_government.high]),
    school: swap(s.school, SCHOOL24, [R.school.growth, R.school.decline]),
    reading: P.ALL_SPECS[i].reading, rate: P.ALL_SPECS[i].rate, enterprises: P.ALL_SPECS[i].enterprises }));
  const sameAs = (rs, sp) => rs.length === sp.length && rs.every((s, i) => Object.keys(P24.MAIN_SPECS[0]).every((k) => s[k] === sp[i][k])
      && Object.keys(sp[i]).every((k) => k in P24.MAIN_SPECS[0] || EXTRA.includes(k)));
  const rows = rows64.filter((s) => s.allocation === payload.meta.allocation.group_total);
  check("adopted responses replace the September 24 ones one for one over the 64 (ALL_SPECS), and the personal ones (meta.allocation.group_total) are MAIN_SPECS; no specification field beyond EXTRA (:102-104)",
    sameAs(rows64, P.ALL_SPECS) && sameAs(rows, P.MAIN_SPECS), `${rows64.length} specifications, ${rows.length} at the personal allocation`);
  if (!sameAs(rows64, P.MAIN_SPECS)) needsCode(":94-104 (the specification rebuild), :152-159 and :284-286", `the rebuild compares the September 24 package's ${rows64.length} with MAIN_SPECS one for one; MAIN_SPECS now holds the ${P.MAIN_SPECS.length} personal ones (item personal_allocation)`,
    "compare the rebuilt 64 with P.ALL_SPECS, and take the case's band over those at meta.allocation.group_total (P.MAIN_SPECS); PINNED (:72) moves to the oct14 ends");
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
  // Every basis a spending line of model.json, as the generation lane's v6_split.cjs splitBasis() requires; Pell on the
  // education line (meta.user_fees.splits.basis_rule, [ASSUMPTION]).
  if (payload.meta.user_fees) check(`user_fees's split bases are model.json spending lines (${lineBases.join(", ")}), and union_key_pell's is education_services`,
    Object.keys(SPLIT).length > 0 && Object.values(SPLIT).every((id) => MODEL.spending.lines.some((l) => l.id === id)) && SPLIT.union_key_pell === "education_services",
    Object.entries(SPLIT).map(([k, v]) => `${k} ${v}`).join("; "));
  const lineGap = Math.max(0, ...lineBases.flatMap((id) => P.ALLOCS.map((a) => Math.abs(GENS.reduce((t, g) => t + grp(gen29[g], id, a), 0) - grp(union29, id, a)))));
  const lineShare = (id, g, a) => grp(gen29[g], id, a) / GENS.reduce((t, x) => t + grp(gen29[x], id, a), 0);
  const basisGap = Math.max(lineGap, ...Object.keys(BASIS).flatMap((k) => P.ALLOCS.map((a) => Math.abs(GENS.reduce((t, g) => t + BASIS[k](g, a), 0) - UNION_BASIS[k](a)))));
  // v7's items name each union part's generation (union_G1:, union_G2:, union_G3plus:); their lineage_ parts go with the
  // lineage, on G3+.
  const GEN_PART = /^union_(G1|G2|G3plus):/;
  const share = (name, g, a) => (name.startsWith("lineage_") ? (g === "G3plus" ? 1 : 0)
    : GEN_PART.test(name) ? (name.match(GEN_PART)[1] === g ? 1 : 0)
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
  const ends6 = ENDS7;
  check(`${STUB ? "[STUB] " : ""}with the edit sets' edits by the rule (national-scale edits as they are; pension_tr2026's lineage parts on G3+, its union parts by those shares; user_fees's parts and carriers by their split-basis lines' union shares, meta.user_fees.splits.split_basis; the v7 edit sets' union_<G> parts on generation G and their lineage_ parts on G3+ with the lineage) they add to this case at every specification (1e-9)`,
    gap6 < 1e-9, `max |diff| ${e1(gap6)}; at specifications ${ends6.join(" / ")}: ${GENS.map((g) => `${g} ${f4(ends6.map((i) => byGen[g][i]))}`).join("; ")}`);
  const off = spanOf(asWritten);
  needsCode("v5_split.cjs:43-55 (loadCase), run_generations_v5.cjs:127-136",
    `loadCase stops (the lineage's edits no longer close the payload: ${payload.edits.length - E.first - E.count} edit-set edits follow them); with withLineage() alone on G3+ the generations add to the item base, ${off[0].toFixed(3)} to ${off[1].toFixed(3)}bn from this case across the ${P.MAIN_SPECS.length} specifications`,
    "slice the lineage by meta.lineage.edits (first, count) and add meta.items' edit sets per generation: v6's rules (national-scale edits as they are; pension_tr2026's lineage parts on G3+, its union parts by the OASDI and Part A shares; user_fees's parts and carriers by meta.user_fees.splits.split_basis); then v7's: R6, child_credits's parts union_<G>:* on generation G and lineage_g3plus:* with the lineage on G3+; R7, job_capital_taxes's parts union_<G>:<line>:<scenario> on generation G and lineage_g3plus / lineage_whites with the lineage on G3+, and its four meta.responses entries in every specification; R8, white_end_tax_keys's parts lineage_whites:* with the lineage on G3+; R9, row4_frame's parts union_<G>:<component>:<line>:<cell> on generation G and lineage_g3plus / lineage_whites with the lineage on G3+; v6_split.cjs RULES (:60-66) names items by id and stops on an unknown one (:305); then rebuild generation_corrections_oct14*.json and generation_results_oct14.csv at the case's ends (16 / 11)",
    "generation_account_2026_09_24");
  needsCode("run_generations_v6.cjs:472-477", "parses v6's api_check.json pattern 3 print \"at specifications 48 / 11: ...\" and gates lo === 48 && hi === 11",
    `read the ends from ${LANE}/derived/summary.json v7.end_specifications (${ENDS7.join(" / ")} at the personal allocation) and this file's print \"at specifications ${ENDS7.join(" / ")}: ...\"`, "generation_account_2026_09_24");
}

// ---------------------------------------------------------------------------------------------------
pattern("winners_losers_2026_09_24/specs.cjs", "160-189 (HEAD 52e2ccfb)",
  "each case's payload applied by the consumer; pkg.RESPONSES; pkg.evaluateFull(m, spec) (no profile); the previous cases through SEPT29 and OCT05");
{
  const CASES = [["adopted_2026_09_29", SEPT29, "sept29_case", P.SEPT29], ["adopted_2026_10_05", OCT05, "oct05_case", P.OCT05],
    ["adopted_2026_10_07", OCT07, "oct07_case", P.OCT07], ["candidate_2026_10_14", LANE, "adopted", P]];
  for (const [caseName, payloadLane, variant, pkg] of CASES) {
    const pl = readJson(`${payloadLane}/derived/corrections.json`);
    const m = Engine.applyCorrections(MODEL, pl);
    const specs = pkg.MAIN_SPECS, r = pl.meta.responses, cap = pl.meta.capital_return;
    check(`${caseName}: the package's responses are the payload's meta.responses (:164-165)`, JSON.stringify(pkg.RESPONSES) === JSON.stringify(r));
    check(`${caseName}: every specification carries the payload's responses (:166-168)`, specs.every((s) =>
      [r.general_government.low, r.general_government.high].includes(s.gg) && [r.school.growth, r.school.decline].includes(s.school)));
    // The gate as HEAD writes it, :170-179: the line responses are exactly the meta.responses entries with a low and a
    // high other than general government (a receipt's under its override key), a receipt's at its low response (:176).
    // An earlier version of this pattern reconstructed the pre-v4 gate (exactly four line responses) and recorded it as
    // failing on every case; HEAD has no such gate (prop-c's run, 2026-10-07: specs.cjs passes on oct05).
    const asWrittenWant = (s, id) => (id.startsWith("receipt:") ? r[id.slice(8)].low : r[id][s.reading]);
    const atReadingWant = (s, id) => (id.startsWith("receipt:") ? r[id.slice(8)][s.reading] : r[id][s.reading]);
    const ids = JSON.stringify(Object.entries(r).filter(([k, v]) => v && typeof v === "object" && "low" in v && "high" in v && k !== "general_government")
      .map(([k, v]) => v.override || k).sort());
    const gateWith = (want) => specs.every((s) => JSON.stringify(Object.keys(s.line_responses).sort()) === ids && Object.entries(s.line_responses).every(([id, v]) => v === want(s, id))
      && s.rate === cap.rates[s.reading] && s.enterprises === cap.enterprises);
    const byReading = Object.entries(r).filter(([, e]) => e && e.receipt === true && e.low !== e.high).map(([k]) => k);
    check(`${caseName}: every line response, the rate and the enterprise option are the payload's meta at the specification's reading`, gateWith(atReadingWant),
      `${Object.keys(specs[0].line_responses).length} line responses${byReading.length ? `; receipts that differ by reading: ${byReading.join(", ")}` : ""}`);
    const asWritten = gateWith(asWrittenWant);
    if (byReading.length && !asWritten) {
      needsCode(":176-179", `the gate reads every receipt override at its low response; on ${caseName} ${byReading.join(", ")} differ by reading, so it stops`,
        "read a receipt override at the specification's reading, r[id.slice(8)][s.reading], as band_variants.cjs lineResponsesAt does");
    } else {
      check(`${caseName}: as :170-179 gates them (HEAD)`, asWritten, `${Object.keys(specs[0].line_responses).length} line responses`);
    }
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
  check("the October 7 case is the package's OCT07, v6's case (its lane and adopted stamp, its payloads v6's derived files)", P.OCT07.LANE === OCT07 && P.OCT07.ADOPTED === "2026-10-07"
    && JSON.stringify(P.OCT07.correctionsPayload()) === JSON.stringify(payload6) && JSON.stringify(P.OCT07.CASH_PAYLOAD) === JSON.stringify(cashPayload6), `${P.OCT07.LANE}, adopted ${P.OCT07.ADOPTED}`);
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
  needsCode(":174", "gates the ends as specifications 48 (low) and 11 (high)", `the ends are ${ENDS7.join(" / ")} (personal, item personal_allocation): gate them against summary.json v7.end_specifications, or take the min and max over MAIN_SPECS`);
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
  // lineage's own, and by item row4_frame's parts on social_security and medicare: its union parts move the union's
  // OASDI ratio and Part A to row 4, its lineage parts the added people's, while meta.pension_accrual keeps v6's values.
  const PA = payload.meta.pension_accrual, cashModel = P.CASH.payloadModel(), m29 = P.SEPT29.payloadModel(), REF = MODEL.receipts.reference;
  const LS = P.LINEAGE_EDITS, LC = P.CASH.LINEAGE_EDITS;
  const it1 = P.CASE_ITEMS.find((r) => r.id === "pension_tr2026"), it8 = P.CASE_ITEMS.find((r) => r.id === "row4_frame");
  const r8 = (line, a) => Object.entries(it8.parts).filter(([n]) => n.split(":")[2] === line).reduce((t, [, p]) => t + p.by[a], 0);
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
    const fix = { accrual: it1.parts.lineage_oasdi.by[a] + r8("social_security", a), part_a: it1.parts.lineage_part_a.by[a] + r8("medicare", a) };
    fixGap = Math.max(fixGap, Math.abs(miss.accrual - fix.accrual), Math.abs(miss.part_a - fix.part_a));
    misses.push(`${end} (${a}): accrual ${miss.accrual.toFixed(6)}, Part A ${miss.part_a.toFixed(6)}`);
  }
  check("as written, the gate misses by exactly item pension_tr2026's lineage parts (meta.items parts lineage_oasdi, lineage_part_a) and item row4_frame's parts on social_security and medicare (its oasdi_ratio, part_a, part_a_split, ss_split and ss_factor; 1e-9)", fixGap < 1e-9,
    `${misses.join("; ")}; max |miss - parts| ${e1(fixGap)}`);
  needsCode(":280-304 (the gate at :302)", `the gate "the union's accrual less the lineage's own is the September 29 payload's" misses on this case (${misses.join("; ")}bn)`,
    "count item pension_tr2026's lineage parts (meta.items, pension_tr2026 parts lineage_oasdi and lineage_part_a, at the end's allocation) in own, and take item row4_frame's parts on social_security and medicare (R9: union_<G>:oasdi_ratio and :part_a, which move the union to row 4, and the lineage_ parts) out of the union's accrual and Part A; the payload's ratio_net and part_a_accrual_bn are the 2026 inputs' at published weights");
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
  // HEAD's rebuild (:344-353, lineResponsesAt :318-330, since 911afa6f) takes every meta.responses entry, as this does; an
  // earlier version of this pattern reconstructed the pre-v4 rebuild (4 of 13 line responses) and recorded it as
  // failing, which HEAD's code does not do.
  const specs64 = rebuild((reading) => Object.fromEntries(Object.entries(P.LINE_RESPONSES).map(([k, e]) => [k, e[reading]])));
  const specs = specs64.filter((s) => s.allocation === payload.meta.allocation.group_total);
  check("specifications rebuilt from every meta.responses entry (P.LINE_RESPONSES, item job_capital_taxes's four among them) at the reading equal ALL_SPECS, and at meta.allocation.group_total MAIN_SPECS",
    canon(specs64) === canon(P.ALL_SPECS) && canon(specs) === canon(P.MAIN_SPECS), `${specs64.length} / ${specs.length}`);
  if (canon(specs64) !== canon(P.MAIN_SPECS)) needsCode(":344-353 (the rebuild and its gate), :577, :593", `the rebuild from the September 24 package's 64 is gated equal to MAIN_SPECS (stops), and the variants' bands span the 64; MAIN_SPECS now holds the ${P.MAIN_SPECS.length} personal ones`,
    "gate the rebuild against P.ALL_SPECS and span the case's band over meta.allocation.group_total's (P.MAIN_SPECS); item job_capital_taxes's four receipt:<line> entries come with P.LINE_RESPONSES");
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
    const a = P.evaluateFull(mv, s), b = P.fixReceipts(V4.evaluateFull(mv, P.moveSpec(sv4[i], oo)), s, mv);
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
  check(`the roads item off (${JSON.stringify(o)}): evaluateFull on its model (the edit sets applied) and specsFor(o)'s specifications is candidate v4's at the moved specification with item job_capital_taxes's four receipt responses set after it (fixReceipts), the long-run capital at v5's subfunction responses (exact)`,
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
    stops.every((x) => x.why.includes("[BLOCKED]") && /item (pension_tr2026|user_fees|child_credits|white_end_tax_keys|row4_frame) edits by fixed amounts/.test(x.why)),
    `${onCase.length - stops.length} of ${onCase.length} build${stops.length ? `; stop: ${stops.map((x) => `${x.item} (${x.why})`).join("; ")}` : ""}`);
  const pension = throws(() => P.modelFor("central", METHODS[0], P.withCentral(V4.offOf({ pension4: P.ITEMS.pension4 }))));
  check("the pension switch off stops ([BLOCKED]): the lineage there is the cash payload's, through P.CASH", !!pension && pension.includes("[BLOCKED]") && pension.includes("P.CASH"), pension);
  const copied = throws(() => P.evaluateFull(mv, Object.assign({}, sv[0])));
  const crossed = throws(() => P.evaluateFull(mv, P.MAIN_SPECS[0]));
  check("a copy of the variant's specification stops ([BLOCKED])", !!copied && copied.includes("[BLOCKED]"), copied);
  check("the case's specification on the variant's model stops ([BLOCKED])", !!crossed && crossed.includes("[BLOCKED]"), crossed);
}

// ---------------------------------------------------------------------------------------------------
pattern("main_case_2026_10_14/package.cjs", "caseOf, caseOn, forItems7, REGISTRY (the item API)",
  "caseOf(OCT05, ids, arms, lineage), caseOn, meta.items, CASE_ITEMS, ITEM_EDITS, ITEM_BASE, LINEAGE_PAYLOADS, withItems(m), CASH, checkBuilt, checkBuilt7, checkLineage");
{
  const cost = (m, s) => P.evaluateFull(m, s, P.MAIN_PROFILE).cost_bn;
  // With no item the case is v5's; with v6's items it is v6's.
  const Z = P.caseOf(P.OCT05, []);
  check("caseOf(OCT05, []) is v5: its payloads are v5's derived files, its names v5's, no item (exact)",
    JSON.stringify(Z.correctionsPayload()) === JSON.stringify(payload5) && JSON.stringify(Z.CASH_PAYLOAD) === JSON.stringify(cashPayload5)
    && Z.LANE === OCT05 && Z.ADOPTED === P.OCT05.ADOPTED && Z.CASE_ITEMS.length === 0 && Z.ITEM_EDITS.length === 0, `${Z.LANE}, adopted ${Z.ADOPTED}`);
  const V6C = P.caseOf(P.OCT05, P.V6_PACKAGE.CANDIDATE);
  check("caseOf(OCT05, v6's CANDIDATE) is v6: its payloads are v6's derived files, its names and stamps v6's, no v7 item (exact)",
    JSON.stringify(V6C.correctionsPayload()) === JSON.stringify(payload6) && JSON.stringify(V6C.CASH_PAYLOAD) === JSON.stringify(cashPayload6)
    && V6C.LANE === OCT07 && V6C.ADOPTED === "2026-10-07" && !V6C.V7_ITEMS && V6C.MAIN_SPECS.length === 64, `${V6C.LANE}, adopted ${V6C.ADOPTED}`);
  // The stamps: the candidate, or the adopted case once STATUS is "adopted" (the decision file must exist).
  const ADOPTED7 = P.V7.STATUS === "adopted", DEC = path.join(FISCAL, "..", "..", P.V7.DECISION);
  const V = P.caseOf(P.OCT05, P.CANDIDATE, { child_credits: Object.keys(P.CREDITS.ARMS)[0] });
  check(ADOPTED7 ? "the payloads are stamped as adopted: source package.cjs, adopted 2026-10-14, the decision (its file exists), the case key oct14; a variant (an arm) is stamped adopted null"
    : "the payloads are stamped as the candidate: source package.cjs, adopted null, the decision named (written by the parent), status \"candidate: main case v7, not adopted ...\", the case key oct14; a variant (an arm) is stamped \"variant: ...\"",
    [payload, cashPayload].every((pl) => pl.meta.source === `${LANE}/package.cjs` && pl.meta.decision === P.V7.DECISION
      && (ADOPTED7 ? pl.meta.adopted === "2026-10-14" : pl.meta.adopted === null && pl.meta.status.startsWith("candidate: main case v7, not adopted")))
    && (!ADOPTED7 || fs.existsSync(DEC)) && P.CASE_KEY === "oct14" && P.STATUS === P.V7.STATUS
    && V.ADOPTED === null && V.correctionsPayload().meta.adopted === null && V.correctionsPayload().meta.status.startsWith("variant: "),
    `${P.V7.DECISION} ${fs.existsSync(DEC) ? "exists" : "not written yet"}; STATUS ${P.V7.STATUS}`);
  check("REGISTRY lists v6's items then v7's in edit order; CANDIDATE is all of them; NEW_IDS are v7's; SLOTS describe lineage_count and split_line",
    JSON.stringify(P.REGISTRY.map((x) => x.id)) === JSON.stringify(["pension_tr2026", "retiree_health", "added_age_mix", "user_fees", "personal_allocation", "child_credits", "job_capital_taxes", "white_end_tax_keys", "row4_frame"])
    && JSON.stringify(P.CANDIDATE) === JSON.stringify(P.ITEM_IDS) && JSON.stringify(P.NEW_IDS) === JSON.stringify(["personal_allocation", "child_credits", "job_capital_taxes", "white_end_tax_keys", "row4_frame"])
    && JSON.stringify(Object.keys(P.SLOTS)) === JSON.stringify(["lineage_count", "split_line"]), P.REGISTRY.map((x) => `${x.id} (${x.kind})`).join(", "));
  // meta.items locates every edit set's edits; the parts add to their edits.
  for (const [w, pl, api, base] of [["set", payload, P, P.ITEM_BASE], ["cash", cashPayload, P.CASH, P.ITEM_BASE.CASH]]) {
    const n = base.correctionsPayload().edits.length;
    const recs = pl.meta.items.filter((r) => r.applied && r.edits);
    const seg = recs.flatMap((r) => pl.edits.slice(r.edits.first, r.edits.first + r.edits.count));
    check(`${w}: meta.items is CASE_ITEMS; each edit set's first and count locate its edits, which follow the item base's ${n} in registry order and are ITEM_EDITS (exact); personal_allocation edits nothing`,
      JSON.stringify(pl.meta.items) === JSON.stringify(api.CASE_ITEMS) && recs.every((r, k) => r.edits.first === (k ? recs[k - 1].edits.first + recs[k - 1].edits.count : n))
      && JSON.stringify(seg) === JSON.stringify(pl.edits.slice(n)) && JSON.stringify(seg) === JSON.stringify(api.ITEM_EDITS)
      && JSON.stringify(pl.edits.slice(0, n)) === JSON.stringify(base.correctionsPayload().edits) && recs.find((r) => r.id === "personal_allocation").edits.count === 0,
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
    // v7's parts name their generation or the lineage, for consumers that split the case by generation.
    const names = recs.filter((r) => P.NEW_IDS.includes(r.id)).flatMap((r) => Object.keys(r.parts || {}));
    check(`${w}: every part of the v7 edit sets (${P.NEW_IDS.filter((id) => id !== "personal_allocation").join(", ")}) starts union_G1:, union_G2:, union_G3plus: or lineage_ (R6-R9)`,
      names.length > 0 && names.every((nm) => /^(union_(G1|G2|G3plus):|lineage_)/.test(nm)), `${names.length} parts`);
  }
  const pen = cashPayload.meta.items.find((r) => r.id === "pension_tr2026");
  check("the cash set: item pension_tr2026 does not apply (applied false, with its reason); the other eight do; CASH_PAYLOAD is corrections_cash.json",
    pen.applied === false && typeof pen.why === "string"
    && JSON.stringify(cashPayload.meta.items.filter((r) => r.applied).map((r) => r.id)) === JSON.stringify(["retiree_health", "added_age_mix", "user_fees", "personal_allocation", "child_credits", "job_capital_taxes", "white_end_tax_keys", "row4_frame"])
    && JSON.stringify(P.CASH_PAYLOAD) === JSON.stringify(cashPayload) && !("pension_accrual" in cashPayload.meta), pen.why);
  // Item child_credits by generation: its parts' net cost at the reference scenario is the lane's by_generation.
  {
    const r = payload.meta.items.find((x) => x.id === "child_credits"), REF = MODEL.receipts.reference;
    const es = payload.edits.slice(r.edits.first, r.edits.first + r.edits.count);
    const byG = Object.fromEntries(GENS.map((g) => [g, Object.entries(r.parts).filter(([nm]) => nm.startsWith(`union_${g}:`)).reduce((t, [, p]) => {
      const e = es[p.edit];
      return t + (e.side === "spending" ? p.by.personal : e.scenario === REF ? -p.by.personal : 0);
    }, 0)]));
    const want = payload.meta.child_credits.by_generation;
    check(`${STUB ? "" : ""}item child_credits: its parts by generation, spending less receipts at ${REF}, are the lane's by_generation (1e-9), the shared cells 0`,
      GENS.every((g) => Math.abs(byG[g] - want[g]) < 1e-9) && Object.values(r.parts).every((p) => p.by.shared === 0), GENS.map((g) => `${g} ${byG[g].toFixed(4)}`).join(", "));
    // Its added people: lineage_g3plus:<line>[:<scenario>], the lane's G3+ per-member term on the G3+-priced members.
    const ap = payload.meta.child_credits.added_people;
    const lin = Object.entries(r.parts).filter(([nm]) => nm.startsWith("lineage_g3plus:")).reduce((t, [, p]) => { const e = es[p.edit]; return t + (e.side === "spending" ? p.by.personal : e.scenario === REF ? -p.by.personal : 0); }, 0);
    check("item child_credits: its lineage_g3plus parts at the reference scenario net to meta.child_credits.added_people.term_bn, the per-member term times meta.lineage.members.g3plus (1e-9)",
      ap && ap.applied === true && Math.abs(lin - ap.term_bn) < 1e-9 && Math.abs(ap.term_bn - ap.per_member_usd * payload.meta.lineage.members.g3plus / 1e9) < 1e-9,
      `${lin.toFixed(6)} = $${ap ? ap.per_member_usd.toFixed(2) : "?"} x ${payload.meta.lineage.members.g3plus.toFixed(2)}`);
  }
  // Items white_end_tax_keys and row4_frame: their parts by group at the reference scenario, with the sources a consumer reads.
  for (const [id, groups] of [["white_end_tax_keys", ["lineage_whites"]], ["row4_frame", ["union_G1", "union_G2", "union_G3plus", "lineage_g3plus", "lineage_whites"]]]) {
    for (const [w, pl] of [["set", payload], ["cash", cashPayload]]) {
      const r = pl.meta.items.find((x) => x.id === id), REF = MODEL.receipts.reference, es = pl.edits.slice(r.edits.first, r.edits.first + r.edits.count);
      const names = Object.keys(r.parts);
      const ok = names.every((nm) => groups.some((g) => nm.startsWith(`${g}:`))) && es.every((e, j) => names.some((nm) => r.parts[nm].edit === j)) && pl.meta[id] && pl.meta[id].source;
      check(`${w}: item ${id}'s parts are named ${groups.map((g) => `${g}:`).join(", ")}..., every edit has parts, and meta.${id} carries its rule and sources`, ok,
        `${es.length} edits, ${names.length} parts`);
    }
  }
  // The four receipt responses: in meta.responses, in every specification, and read by consumer.cjs's lineResponses().
  const Consumer = require(path.join(FISCAL, "main_case_candidate_v4_2026_09_29", "consumer.cjs"));
  const JC = P.JOBCAP.LINES;
  const lr = (reading) => Consumer.lineResponses(Engine.applyCorrections(MODEL, payload), payload, reading);
  check(`${P.JOBCAP.S.stub ? "[STUB] " : ""}item job_capital_taxes's four responses: meta.responses entries with receipt true and override receipt:<line>, in every specification's line_responses, and consumer.cjs lineResponses() returns them at both readings`,
    JC.every((id) => payload.meta.responses[id] && payload.meta.responses[id].receipt === true && payload.meta.responses[id].override === `receipt:${id}`
      && P.ALL_SPECS.every((s) => s.line_responses[`receipt:${id}`] === payload.meta.responses[id][s.reading]) && ["low", "high"].every((rd) => lr(rd)[`receipt:${id}`] === payload.meta.responses[id][rd])),
    JC.map((id) => `${id} ${payload.meta.responses[id].low}`).join(", "));
  // The lineage base and its additions (v6's).
  const LP = { set: readJson(P.LINEAGE_PAYLOADS.set), cash: readJson(P.LINEAGE_PAYLOADS.cash) };
  check("ITEM_BASE.ADDITION is v6's lineage_payload.json and lineage_payload_cash.json, which meta.lineage.payload names, and this lane's copies (exact)",
    JSON.stringify(P.ITEM_BASE.ADDITION.set) === JSON.stringify(LP.set) && JSON.stringify(P.ITEM_BASE.ADDITION.cash) === JSON.stringify(LP.cash)
    && payload.meta.lineage.payload === P.LINEAGE_PAYLOADS.set && cashPayload.meta.lineage.payload === P.LINEAGE_PAYLOADS.cash
    && JSON.stringify(readJson(`${LANE}/derived/lineage_payload.json`)) === JSON.stringify(LP.set) && JSON.stringify(readJson(`${LANE}/derived/lineage_payload_cash.json`)) === JSON.stringify(LP.cash),
    `${P.LINEAGE_PAYLOADS.set}, ${P.LINEAGE_PAYLOADS.cash}`);
  // withItems() on a consumer's model of the item base gives the case.
  for (const [w, api, base] of [["set", P, P.ITEM_BASE], ["cash", P.CASH, P.ITEM_BASE.CASH]]) {
    const mB = Engine.applyCorrections(MODEL, base.correctionsPayload());
    const mI = api.withItems(mB), mP = api.payloadModel();
    const g = worst(api.MAIN_SPECS.map((s) => api.evaluateFull(mI, s, P.MAIN_PROFILE).cost_bn - api.evaluateFull(mP, s, P.MAIN_PROFILE).cost_bn));
    check(`${w}: withItems() on a consumer's model of the item base (model.json + ITEM_BASE's payload) is this case at every specification (1e-9)`, g < 1e-9, `max |diff| ${e1(g)}`);
  }
  // The fixed-amount guards: v6's (pension_tr2026 on social_security), then v7's (child_credits on refundable_tax_credits).
  const mB = Engine.applyCorrections(MODEL, P.ITEM_BASE.correctionsPayload());
  const nat = (m, id) => m.spending.lines.find((l) => l.id === id).national_bn;
  const moveLine = (m, id, f) => Engine.applyCorrections(m, { edits: [{ side: "spending", line: id, national_bn: nat(m, id) * f }], meta: m.corrections });
  const stop = throws(() => P.withItems(moveLine(mB, "social_security", 1.01)));
  check("withItems() on a model that moves social_security's national total stops ([BLOCKED]): item pension_tr2026 edits it by fixed amounts",
    !!stop && stop.includes("[BLOCKED]") && stop.includes("pension_tr2026"), stop);
  const QC = P.caseOf(P.OCT05, ["added_age_mix", "child_credits"]), mC = Engine.applyCorrections(MODEL, QC.ITEM_BASE.correctionsPayload());
  const stopC = throws(() => QC.withItems(moveLine(mC, "refundable_tax_credits", 1.01)));
  check("withItems() on a model that moves refundable_tax_credits's national total stops ([BLOCKED]): item child_credits edits it by fixed amounts",
    !!stopC && stopC.includes("[BLOCKED]") && stopC.includes("child_credits"), stopC);
  const QR = P.caseOf(P.OCT05, ["pension_tr2026", "added_age_mix", "row4_frame"]), mR = Engine.applyCorrections(MODEL, QR.ITEM_BASE.correctionsPayload());
  const rnat = (m, id) => m.receipts.lines.find((l) => l.id === id).national_bn;
  const stopR = throws(() => QR.withItems(Engine.applyCorrections(mR, { edits: [{ side: "receipt", line: "modeled_owner_property", national_bn: rnat(mR, "modeled_owner_property") * 1.01 }], meta: mR.corrections })));
  check("withItems() on a model that moves modeled_owner_property's national total stops ([BLOCKED]): item row4_frame edits it by fixed amounts",
    !!stopR && stopR.includes("[BLOCKED]") && stopR.includes("row4_frame"), stopR);
  // Arms are options: the whole case at the arm, v6's and v7's.
  for (const [id, arm] of [["retiree_health", "mu_low"], ["child_credits", Object.keys(P.CREDITS.ARMS)[0]], ["job_capital_taxes", Object.keys(P.JOBCAP.ARMS)[0]]]) {
    // An arm of item job_capital_taxes may set other responses than the case's, so the arm's payload is evaluated at the
    // specifications its own meta.responses give (A.MAIN_SPECS, gated to carry them), as consumer.cjs builds them.
    const A = P.caseOf(P.OCT05, P.ITEM_IDS, { [id]: arm }), pA = A.correctionsPayload();
    const ownSpecs = A.MAIN_SPECS.every((s) => P.JOBCAP.LINES.every((l) => s.line_responses[`receipt:${l}`] === pA.meta.responses[l][s.reading]));
    const bandA = spanOf(A.MAIN_SPECS.map((s) => cost(Engine.applyCorrections(MODEL, pA), s)));
    const rA = A.CASE_ITEMS.find((r) => r.id === id), row = `${id}_${arm}`;
    check(`${id === "job_capital_taxes" && P.JOBCAP.S.stub ? "[STUB] " : ""}caseOf(OCT05, ITEM_IDS, {${id}: "${arm}"}): its payload, applied by a consumer at its own specifications (its meta.responses at each reading), gives main_case_bands.csv's ${row} row (1e-4); meta.items names the arm`,
      ownSpecs && !!published[row] && worst(bandA.map((x, j) => x - published[row][j])) < 1e-4 && rA.arm === arm, f4(bandA));
  }
  const badArm = throws(() => P.caseOf(P.OCT05, P.ITEM_IDS, { child_credits: "no_such_arm" }));
  const badOrder = throws(() => P.caseOf(P.OCT05, ["child_credits", "retiree_health"]));
  const badItem = throws(() => P.caseOf(P.OCT05, ["no_such_item"]));
  check("an unknown arm, an unknown item and items out of registry order (a v7 item before a v6 one) stop ([BLOCKED])",
    [badArm, badOrder, badItem].every((x) => !!x && x.includes("[BLOCKED]")), [badArm, badOrder, badItem].join(" | "));
  // The guards: v6's on reserved meta, and v7's: an edit set may not set a meta key the payload has, nor a response the
  // payload has.
  const reserved = throws(() => P.checkBuilt({ id: "probe" }, { edits: [], meta: { lineage: {} } }, P.ITEM_BASE, "set"));
  const reserved7 = throws(() => P.checkBuilt7({ id: "probe" }, { edits: [], meta: { pension_accrual: {} } }, P.OCT07, "set"));
  const resp7 = throws(() => P.checkBuilt7({ id: "probe" }, { edits: [], meta: {}, responses: { housing_subsidies: { receipt: true, override: "receipt:housing_subsidies", low: 1, high: 1 } } }, P.OCT07, "set"));
  check("an edit set that changes meta.lineage stops (v6's guard); a v7 edit set that sets a meta key the payload has, or a response meta.responses has, stops ([BLOCKED])",
    [reserved, reserved7, resp7].every((x) => !!x && x.includes("[BLOCKED]")), [reserved, reserved7, resp7].join(" | "));
  // Lineage options: the whole case at another arm of the count, a variant. A consumer evaluates an option's payload with
  // its own meta.responses (consumer.cjs) and takes the band at meta.allocation.group_total.
  const consumerBand = (pl) => spanOf(Consumer.evaluateAll(JSON.parse(JSON.stringify(pl)), { engine: Engine, model: MODEL })
    .filter((x) => !pl.meta.allocation || x.spec.allocation === pl.meta.allocation.group_total).map((x) => x.cost_bn));
  const opt = "arm_a", O = P.caseOf(P.OCT05, P.ITEM_IDS, P.ITEM_ARMS, opt), O0 = P.caseOf(P.OCT05, [], {}, opt);
  const bandO = consumerBand(O.correctionsPayload());
  const lin5 = readJson("main_case_lineage_2026_10_05/derived/v5_summary.json").sets.set.arms.a.band_bn;
  const band0 = consumerBand(O0.correctionsPayload());
  const badOpt = throws(() => P.caseOf(P.OCT05, P.ITEM_IDS, {}, "no_such_option"));
  check(`caseOf(OCT05, ITEM_IDS, {}, "${opt}"): a variant (adopted null, meta.lineage.count_option) whose payload, applied by a consumer with its meta.responses and meta.allocation (consumer.cjs), gives main_case_bands.csv's lineage_${opt} row (1e-4); with no item (no meta.allocation: all 64) its payload gives the lineage lane's arm a band (1e-9); an unknown option stops ([BLOCKED])`,
    O.ADOPTED === null && O.correctionsPayload().meta.adopted === null && O.correctionsPayload().meta.lineage.count_option.name === opt
      && O.LINEAGE_OPTION === opt && worst(bandO.map((x, j) => x - published[`lineage_${opt}`][j])) < 1e-4
      && worst(band0.map((x, j) => x - lin5[j])) < 1e-9 && !!badOpt && badOpt.includes("[BLOCKED]"),
    `${f4(bandO)}; alone ${f4(band0)} against ${f4(lin5)}; ${badOpt}`);
  const all64 = spanOf(Consumer.evaluateAll(JSON.parse(JSON.stringify(payload)), { engine: Engine, model: MODEL }).map((x) => x.cost_bn));
  if (worst(all64.map((x, j) => x - summary.main_case[j])) >= 1e-9) needsCode("consumer.cjs specifications() (:29-36) and every caller's span over evaluateAll()",
    `evaluateAll() returns all 64 specifications; their span on v7's payload is ${f4(all64)}, not the case's ${f4(summary.main_case)}`,
    "take the band over the specifications at payload.meta.allocation.group_total (personal on v7); a payload without meta.allocation keeps v6's rule (all 64)", "main_case_candidate_v4_2026_09_29");
}

// ---------------------------------------------------------------------------------------------------
pattern("the shared reading and the allocation rule (summary.json v7.companions.shared_allocation; main_case_bands.csv shared_allocation)",
  "package.cjs MAIN_SPECS, SHARED_SPECS, ALL_SPECS, specsFor / evalPackage / central with {allocation}, meta.allocation",
  "specsFor({allocation: \"personal\" | \"shared\" | \"all\"}), central(o), evalPackage(caseName, method, o), the bands' rows, per_spec.csv in_band");
{
  const idx = (sp) => sp.map((s) => P.ALL_SPECS.indexOf(s));
  check("MAIN_SPECS are ALL_SPECS 0-31 (personal) and SHARED_SPECS 32-63 (shared), in v6's numbering; specsFor({}), specsFor({allocation: \"shared\"}) and specsFor({allocation: \"all\"}) give them (deep-equal)",
    P.ALL_SPECS.length === 64 && JSON.stringify(P.MAIN_SPECS) === JSON.stringify(P.ALL_SPECS.slice(0, 32)) && JSON.stringify(P.SHARED_SPECS) === JSON.stringify(P.ALL_SPECS.slice(32))
    && P.MAIN_SPECS.every((s) => s.allocation === "personal") && P.SHARED_SPECS.every((s) => s.allocation === "shared")
    && JSON.stringify(P.specsFor({})) === JSON.stringify(P.MAIN_SPECS) && JSON.stringify(P.specsFor({ allocation: "shared" })) === JSON.stringify(P.SHARED_SPECS)
    && JSON.stringify(P.specsFor({ allocation: "all" })) === JSON.stringify(P.ALL_SPECS), `${P.MAIN_SPECS.length} + ${P.SHARED_SPECS.length}`);
  const sh = P.central({ allocation: "shared" }), shc = P.CASH.central({ allocation: "shared" }), all = P.central({ allocation: "all" });
  const S7 = summary.v7.companions.shared_allocation;
  check("central({allocation: \"shared\"}) is summary.json's shared reading (1e-9) and main_case_bands.csv's shared_allocation rows (1e-4), set and cash",
    worst(sh.map((x, j) => x - S7.band_bn[j])) < 1e-9 && worst(shc.map((x, j) => x - S7.cash.band_bn[j])) < 1e-9
    && worst(sh.map((x, j) => x - published.shared_allocation[j])) < 1e-4 && worst(shc.map((x, j) => x - published.shared_allocation_cash_set[j])) < 1e-4,
    `${f4(sh)}; cash ${f4(shc)}`);
  const ps = csvRows(`${LANE}/derived/per_spec.csv`);
  const perMethod = (pred) => METHODS.map((m) => spanOf(ps.filter((r) => r.method === m && pred(r)).map((r) => Number(r.cost_bn))));
  const mean2 = (bs) => [mean(bs.map((b) => b[0])), mean(bs.map((b) => b[1]))];
  check("per_spec.csv: in_band marks the 32 personal specifications per method; the methods' bands over them are the case, over the shared ones the shared reading, over all 64 central({allocation: \"all\"}) (1e-9)",
    ps.length === 128 && ps.every((r) => (r.in_band === "true") === (r.allocation === "personal"))
    && worst(mean2(perMethod((r) => r.in_band === "true")).map((x, j) => x - summary.main_case[j])) < 1e-9
    && worst(mean2(perMethod((r) => r.allocation === "shared")).map((x, j) => x - sh[j])) < 1e-9
    && worst(mean2(perMethod(() => true)).map((x, j) => x - all[j])) < 1e-9, `all 64: ${f4(all)}`);
  const ev = P.evalPackage("central", METHODS[0], { allocation: "shared" }), want = perMethod((r) => r.allocation === "shared")[0];
  const bad = throws(() => P.central({ allocation: "both" }));
  check("evalPackage(\"central\", method, {allocation: \"shared\"}) is that method's band over its shared rows (1e-9); an unknown allocation stops ([BLOCKED])",
    worst(ev.map((x, j) => x - want[j])) < 1e-9 && !!bad && bad.includes("[BLOCKED]"), `${f4(ev)}; ${bad}`);
  check("meta.allocation in both payloads: group_total personal, the rule, the reason, what the shared allocation is kept for, the source record and the decision",
    [payload, cashPayload].every((pl) => pl.meta.allocation && pl.meta.allocation.group_total === "personal" && pl.meta.allocation.source.decision === P.V7.DECISION)
    && JSON.stringify(payload.meta.allocation) === JSON.stringify(cashPayload.meta.allocation), payload.meta.allocation.rule.slice(0, 100));
  // The consumers' hard-coded ends, 64-specification spans and pins (R5), from an rg sweep at HEAD 52e2ccfb with every
  // cited line re-read on 2026-10-14: recorded from reading, not run here. Patterns 3, 4, 5 and 7 record their own.
  const R5 = [
    ["generation_account_2026_09_24", "run_generations_v6.cjs:240-248, :537", "gates 64 specifications and takes the ends over them (stops); own_span over the 64 (silent: v6's rule)"],
    ["late_arrival_account_line_2026_09_27", "run_cells.cjs:684-697, :871", "the corrected union at the case's full-precision band at 48 / 11 (stops); own_span over the 64 (silent)"],
    ["debt_legacy_2026_09_23", "debt_legacy.py:404, :847-848, :2248-2251", "the oct07 oracle at ends (48, 11), checked at :2756-2761 (stops); the frame's corners over both allocations; any meta.responses change from v5 stops it, and R7 adds four"],
    ["sept24_propagation_2026_09_24", "band_variants.cjs:612-617, :655-658, :668, :688", "the band and its ends over every specification it rebuilds: gated against the case's summary at :612-617 and :655-658 (stops); the lineage and item moves at those ends (:668, :688; silent)"],
    ["uncertainty_propagation_2026_09_22", "sept24_specs.cjs:72; propagate.py:605-608; test_uncertainty.py:127", "PINNED holds v6's bands only; the specifications must span the published band (stops); the test asserts 64 specifications"],
    ["historical_backcast_2026_09_20", "case_components.cjs:99, :110-115, :165-166, :188-191, :236-238", "CASES and the oct07 route know no oct14; the case's MAIN_SPECS (32) must match the schools case's (64) in number (stops at :166) and the previous cases' in every field"],
    ["distribution_weights_2026_09_23", "case_ends.cjs:54-62; distribute.py:36, :441-443", "CASES and PREVIOUS_GRID know no oct14 (stops); the ends follow MAIN_SPECS (:91-93); distribute.py chains each case's change at a band end as a move of A alone, on the premise that the low end stays shared, and v7's low-end move is item personal_allocation's change of allocation (silent)"],
    ["world_ledger_2026_09_27", "generation_lines.cjs:9, :117-124; beside_extra.py:125", "the ends follow MAIN_SPECS and the oracle is the case's adopted row (its docstring says 48 and 11); CASE_SET pins v6's band"],
    ["within_group_distribution_2026_09_29", "export_lines.cjs:87-92, :124-133, :376-382", "the per-case config pins v6's band (oct14 needs an entry); the ends follow MAIN_SPECS against it; the lineage-part gate admits only social security and Medicare parts, and R7's lineage parts are receipts (stops)"],
    ["white_replacement_2026_09_28", "engine_lines.cjs:39, :112-118; rekey_sept29.py:527-529, :1143", "ENDS {low: 48, high: 11} over P.specsFor(oo) (:39), which on v7 gives the 32 personal specifications, so specs[48] is undefined and evaluateFull throws (stops; with {allocation: \"all\"} it would take the shared low end, silent); the benefit-tax rule (rule 3b, :1143) ties the low end to the shared allocation (silent); itemUnionEdits (:40-85) takes union_ and lineage_ parts, which v7's names keep"],
    ["black_comparator_rough_2026_09_28", "engine_lines.cjs:39, :112-118", "ENDS {low: 48, high: 11} over P.specsFor(oo): specs[48] is undefined on v7's 32 (stops)"],
    ["break_conditions_2026_09_29", "engine_breaks_sept29.cjs:120, :681; tables_oct07.py:44", "ENDS 48 / 11; :681 evaluates MAIN_SPECS[48], undefined on v7's 32 (stops); tables_oct07.py's ENDS"],
    ["closed_budget_2026_10_06", "closed_budget.py:94-103, :196-197", "the oct07 config pins v6's bands and its excess (stops at the gate)"],
    ["nonresponse_bias_2026_10_07", "reweight.py:231-232, :259", "personal allocation only (as v7); reads oct05's payload at :259"],
    ["number_drift_audit_2026_09_29", "memo_sweep.py:125-176", "the pairing and case records name v6's and v5's lanes"],
    ["overview_2026_09_28", "groups.py:58; quantity_registry.csv row 143", "\"The range covers 64 of them\"; the late-arrival cost keyed spec=low & allocation=shared"],
    ["row4_class_2026_09_29", "row4_oct07.cjs:52, :73-79, :175", "ENDS [48, 11], gated as shared / personal; W_ITEM keyed by 48 and 11 (outside the consumer table)"],
    ["figures_2026_09_22", "account.cjs:27-31; build_data.cjs:82, :85, :116", "pins v6's hashes; gates ENDS 48,11 and reads the C2 tally's low_end_48 rows (outside)"],
    ["assumption_explorer_2026_09_21", "case.js:191; test_engine.js:230", "loops both allocations for the band (silent: v6's rule); tests against v6's lane (outside)"],
    ["tax_key_heldout_2026_09_28", "ends.cjs:20-21; test_keys.py:61", "ENDS {low: 48, high: 11} with ALLOC {low: shared, high: personal}; a v6 path (outside)"],
  ];
  for (const [lane, line, today] of R5) needsCode(line, `${today}`, `read the case's ends from ${LANE}/derived/summary.json v7.end_specifications (${ENDS7.join(" / ")}), the band over MAIN_SPECS or meta.allocation.group_total's specifications, and the oct14 pins`, lane, "read");
  // R7 in the uncertainty lane, read at HEAD 52e2ccfb: its receipt overrides take their spread from the account's key.
  needsCode("propagate.py:814-841, :879-890 (sept24_specs.cjs:142-143 writes the columns)",
    "R7's four lines arrive as response_receipt_<line> columns; propagate.py gives each its account key's sampling spread (receipt_reps, :830) and routes item job_capital_taxes's reference-scenario edits by the line's ratio (route_of), while the item's amounts sit on the job-capital lane's industry wage key (silent)",
    "give the four lines the spread of the job-capital amounts (the lane's item.json se_bn, from its 160 replicate weights), or state that the account key's spread stands in for it", "uncertainty_propagation_2026_09_22", "read");
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
const byBasis = (b) => consumerCode.filter((x) => x.basis === b).length;
console.log(failures ? `G4 FAIL: ${failures} of ${n} checks` : `G4 PASS: ${patterns.length} patterns, ${n} checks; ${consumerCode.length} consumer gates need code (${byBasis("run")} found running their call patterns, ${byBasis("read")} reading the code; listed)`);
if (failures) process.exitCode = 1;
