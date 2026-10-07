/* Retiree health on the account's service lines, swapped from pay-as-you-go to accrual, on main case v5
 * (main_case_2026_10_05: $390.29-461.24bn, cash set $307.38-383.41bn) by an engine run: the case's payload plus one
 * edit per service line, evaluated at the case's 64 specifications by candidate v4's package-free consumer
 * (main_case_candidate_v4_2026_09_29/consumer.cjs), as pension_tr2026_2026_10_06/case_tr2026.cjs does.
 *
 * Each arm's national change on a line (derived/national.csv, from opeb_national.py: the GASB 75 or FR normal cost less
 * the pay-go, spread by the pension legacy lane's payroll mix) enters as a national-scale edit (engine.js scaleLine):
 * the line's national total moves by the change and every cell scales with it, so the group's share of the line holds
 * (the retiree-health swap moves the line's cost, not who uses it). The group's amount on the key the case evaluates
 * (public_order_safety: use; the rest: preferred; the lineage's added people included) moves by change x share; the
 * engine applies each line's response at each specification (education 1, public order 1, health 1, general
 * government 0.60-0.85, economic affairs its subfunction blend, defense 0). Shares holding, the capital return and
 * the state-price and school correction lines do not move. The cash set takes the same edits on its own model.
 *
 * Gates (each stops with [BLOCKED], nothing written):
 *   - the consumer reproduces the case and the cash set from their payloads (summary.json, 1e-9), ends at 48 / 11;
 *   - the per-member divisor is the payload's lineage population;
 *   - national.csv's engine lines add to inputs.json's per-arm totals (1e-6);
 *   - every share is in (0, 1) and the payloads' keys exist;
 *   - a zero edit on every line reproduces the case and the cash set at all 64 specifications (exact);
 *   - every arm's engine change, less its move in the capital return, equals the sum over lines of change x share x
 *     the line's response at that specification, read from the engine's evaluation (1e-9), at all 64 specifications
 *     of both sets. The capital return moves only through the k12 component's part_rekeyed key (the fixed
 *     school_reprice amount over the school part's national total, which scales with the line): recorded, gated
 *     below $0.01bn.
 * Recorded: per-line changes (one-line runs); beside, not an edit: the school key's price factor from
 * school_price_beside.csv times the group's school cost at each end (education_services' school part plus the
 * school_reprice line, each at its response).
 *
 * Writes derived/case_oct05.csv (arm x set x end), derived/by_line_oct05.csv and derived/case_oct05.json. Run from the
 * repository root after opeb_national.py:
 *   node infra/immigration-fiscal/public_pension_legacy_2026_10_07/case_opeb.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.resolve(HERE, "..");
const OUT = path.join(HERE, "derived");
const C = require(path.join(FISCAL, "main_case_candidate_v4_2026_09_29", "consumer.cjs"));
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const clone = (x) => JSON.parse(JSON.stringify(x));
const ALLOCS = ["personal", "shared"];
const byAlloc = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
const ENDS = { low: 48, high: 11 };
const KEY_OVERRIDE = { public_order_safety: "use" };   // consumer.cjs stateOf; the Medicaid key is not touched here

const fail = (msg) => { console.log(`✗ [BLOCKED] ${msg}`); process.exit(1); };
const gates = [];
function gate(name, ok, detail) {
  gates.push({ gate: name, passed: !!ok, detail: detail || "" });
  console.log(`  ${ok ? "✓" : "✗"} ${name}${detail ? " — " + detail : ""}`);
  if (!ok) fail(name);
}

// ---------------------------------------------------------------------------------------------------
// Inputs.
const V5 = "main_case_2026_10_05/derived";
const SETS = { case: readJson(`${V5}/corrections.json`), cash: readJson(`${V5}/corrections_cash.json`) };
const SUM5 = readJson(`${V5}/summary.json`);
const INPUTS = JSON.parse(fs.readFileSync(path.join(OUT, "inputs.json"), "utf8"));
const NAT = fs.readFileSync(path.join(OUT, "national.csv"), "utf8").trim().split("\n").map((l) => l.split(","));
const H = NAT[0], NROWS = NAT.slice(1).map((r) => Object.fromEntries(H.map((h, i) => [h, r[i]])));
const Eng = C.loadEngine(), MODEL = C.loadModel();
const POP = SETS.case.meta.lineage.counts.lineage_population;
if (!Number.isFinite(POP) || POP <= 0) fail(`the payload's lineage population is ${POP}`);

const runOf = (payload) => C.evaluateAll(payload, { engine: Eng, model: MODEL });
const costsOf = (payload) => runOf(payload).map((r) => r.cost_bn);
const band = (xs) => [Math.min(...xs), Math.max(...xs)];
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const ARMS = Object.keys(INPUTS.arms);
const LINES = [...new Set(NROWS.filter((r) => r.on_engine_line === "True").map((r) => r.line))];

// ---------------------------------------------------------------------------------------------------
console.log("[gates]");
const baseRun = { case: runOf(SETS.case), cash: runOf(SETS.cash) };
const base = { case: baseRun.case.map((r) => r.cost_bn), cash: baseRun.cash.map((r) => r.cost_bn) };
const want = { case: SUM5.main_case, cash: SUM5.cash_set.band_bn };
for (const s of ["case", "cash"]) {
  const [lo, hi] = band(base[s]);
  gate(`the consumer reproduces the ${s} band (summary.json, 1e-9)`, near(lo, want[s][0], 1e-9) && near(hi, want[s][1], 1e-9),
    `${lo.toFixed(4)} / ${hi.toFixed(4)}bn`);
  gate(`the ${s} ends are specifications 48 / 11`, base[s].indexOf(lo) === ENDS.low && base[s].indexOf(hi) === ENDS.high);
}
gate("the per-member divisor is summary.json's lineage population", POP === SUM5.v5.per_member_usd.population, `${(POP / 1e6).toFixed(3)}M`);
for (const arm of ARMS) {
  const sum = NROWS.filter((r) => r.arm === arm && r.on_engine_line === "True").reduce((t, r) => t + Number(r.delta_bn), 0);
  if (!near(sum, INPUTS.national_by_arm_bn[arm].delta_bn, 1e-6)) fail(`national.csv ${arm} adds to ${sum}, inputs.json ${INPUTS.national_by_arm_bn[arm].delta_bn}`);
}
gate("national.csv's engine lines add to inputs.json's per-arm totals (1e-6)", true, `${ARMS.length} arms, ${LINES.length} lines`);

// The group's share of each line on the key the case evaluates, per set and allocation.
const shares = {};
for (const s of ["case", "cash"]) {
  const m = Eng.applyCorrections(MODEL, SETS[s]);
  shares[s] = {};
  for (const id of LINES) {
    const l = m.spending.lines.find((x) => x.id === id);
    if (!l) fail(`no spending line ${id}`);
    const key = KEY_OVERRIDE[id] || l.preferred_key;
    if (!l.keys[key]) fail(`line ${id} has no key ${key}`);
    shares[s][id] = { key, national_bn: l.national_bn, ...byAlloc((a) => l.keys[key][a].target_bn / l.national_bn) };
  }
}
const allShares = Object.values(shares).flatMap((x) => Object.values(x)).flatMap((x) => ALLOCS.map((a) => x[a]));
gate("every share is in (0, 1)", allShares.every((v) => v > 0 && v < 1),
  LINES.map((id) => `${id} ${shares.case[id].personal.toFixed(4)}`).join("; "));

const nationalDelta = (arm, id) => NROWS.filter((r) => r.arm === arm && r.line === id).reduce((t, r) => t + Number(r.delta_bn), 0);
const editsFor = (arm, s, only) => LINES.filter((id) => !only || id === only).map((id) => ({
  side: "spending", line: id, national_bn: shares[s][id].national_bn + (arm ? nationalDelta(arm, id) : 0) }));
const groupMove = (arm, s, id) => byAlloc((a) => nationalDelta(arm, id) * shares[s][id][a]);
const withEdits = (s, edits) => { const p = clone(SETS[s]); p.edits = p.edits.concat(edits); return p; };
for (const s of ["case", "cash"]) {
  const zero = costsOf(withEdits(s, editsFor(null, s)));
  gate(`a zero edit on every line reproduces the ${s} at all 64 specifications (exact)`, zero.every((v, i) => v === base[s][i]));
}
// Each line's response at each specification, from the engine's own evaluation of the set.
const responses = {};
for (const s of ["case", "cash"]) {
  responses[s] = baseRun[s].map((r) =>
    Object.fromEntries(LINES.map((id) => [id, r.evaluation.spending.find((x) => x.id === id).response])));
}
const expected = (arm, s, specs, only) => specs.map((sp, i) => LINES.filter((id) => !only || id === only)
  .reduce((t, id) => t + groupMove(arm, s, id)[sp.allocation] * responses[s][i][id], 0));

// ---------------------------------------------------------------------------------------------------
// The arms, then each line alone (central arm).
const specs = C.specifications(Eng, MODEL, SETS.case);
const rows = [], arms = {};
let worst = 0, worstCap = 0;
for (const arm of ARMS) {
  arms[arm] = { role: INPUTS.arms[arm].role, national_delta_bn: INPUTS.national_by_arm_bn[arm].delta_bn };
  for (const s of ["case", "cash"]) {
    const edits = editsFor(arm, s);
    const run = runOf(withEdits(s, edits)), costs = run.map((r) => r.cost_bn);
    const exp = expected(arm, s, specs);
    const dcap = run.map((r, i) => r.capital.total_bn - baseRun[s][i].capital.total_bn);
    worst = Math.max(worst, ...costs.map((v, i) => Math.abs(v - base[s][i] - dcap[i] - exp[i])));
    worstCap = Math.max(worstCap, ...dcap.map(Math.abs));
    const [lo, hi] = band(base[s]), [blo, bhi] = band(costs);
    arms[arm][s] = { band_bn: [blo, bhi], band_specs: [costs.indexOf(blo), costs.indexOf(bhi)], band_change_bn: [blo - lo, bhi - hi],
      per_member_usd: [blo / POP * 1e9, bhi / POP * 1e9], edits };
    for (const [end, idx] of Object.entries(ENDS)) {
      const al = specs[idx].allocation;
      rows.push({ arm, role: INPUTS.arms[arm].role, set: s, end, spec: idx, allocation: al, national_delta_bn: arms[arm].national_delta_bn,
        group_move_bn: LINES.reduce((t, id) => t + groupMove(arm, s, id)[al], 0), expected_change_bn: exp[idx],
        capital_return_move_bn: dcap[idx], base_bn: base[s][idx], arm_bn: costs[idx], change_bn: costs[idx] - base[s][idx],
        arm_band_end_bn: end === "low" ? blo : bhi, arm_band_end_spec: costs.indexOf(end === "low" ? blo : bhi),
        per_member_usd: costs[idx] / POP * 1e9 });
    }
  }
}
gate("every arm's engine change less its capital-return move is the sum of change x share x response (1e-9, 64 specifications, both sets)",
  worst <= 1e-9, `worst ${worst.toExponential(1)}bn`);
gate("the capital return moves by less than $0.01bn in every arm (k12 part_rekeyed key)", worstCap < 0.01, `worst ${worstCap.toExponential(2)}bn`);
const lineRows = [];
for (const s of ["case", "cash"]) {
  for (const id of LINES) {
    const e = editsFor("central", s, id);
    const costs = costsOf(withEdits(s, e));
    for (const [end, idx] of Object.entries(ENDS)) {
      const al = specs[idx].allocation, edit = groupMove("central", s, id)[al], change = costs[idx] - base[s][idx];
      lineRows.push({ set: s, end, spec: idx, allocation: al, line: id, key: shares[s][id].key, group_share: shares[s][id][al],
        national_delta_bn: nationalDelta("central", id), group_move_bn: edit, response: responses[s][idx][id], change_bn: change });
    }
  }
}

// Beside: stripping legacy from the per-pupil state prices the school key uses (a bound; opeb_national.py).
const SB = fs.readFileSync(path.join(OUT, "school_price_beside.csv"), "utf8").trim().split("\n").map((l) => l.split(","));
const schoolBeside = [];
for (const s of ["case", "cash"]) {
  for (const [end, idx] of Object.entries(ENDS)) {
    const sp = specs[idx], ev = baseRun[s][idx].evaluation.spending;
    const edu = ev.find((x) => x.id === "education_services"), rep = ev.find((x) => x.id === "school_reprice");
    if (!edu || !rep) fail("no education_services or school_reprice row in the evaluation");
    const school = edu.amount_bn * sp.share * sp.school + rep.amount_bn * rep.response;
    for (const r of SB.slice(1).filter((r) => r[0] === sp.allocation)) {
      schoolBeside.push({ set: s, end, spec: idx, allocation: sp.allocation, legacy_fraction_of_benefits: Number(r[1]),
        key_factor: Number(r[5]), group_school_cost_bn: school, change_bn: (Number(r[5]) - 1) * school });
    }
  }
}

// ---------------------------------------------------------------------------------------------------
fs.mkdirSync(OUT, { recursive: true });
const fmt = (v) => (typeof v === "number" ? (Number.isInteger(v) ? String(v) : v.toFixed(6)) : String(v));
const writeCsv = (name, rs) => {
  const cols = Object.keys(rs[0]);
  fs.writeFileSync(path.join(OUT, name), [cols.join(","), ...rs.map((r) => cols.map((c) => fmt(r[c])).join(","))].join("\n") + "\n");
};
writeCsv("case_oct05.csv", rows);
writeCsv("by_line_oct05.csv", lineRows);
writeCsv("school_beside_oct05.csv", schoolBeside);
fs.writeFileSync(path.join(OUT, "case_oct05.json"), JSON.stringify({
  case: "oct05 (main case v5, main_case_2026_10_05)", case_band_bn: band(base.case), cash_set_band_bn: band(base.cash),
  lineage_population: POP, shares, method: "engine run: the v5 payloads plus one edit per service line, consumer.cjs at 64 specifications",
  capital_return_move_worst_bn: worstCap, arms, gates,
}, null, 1) + "\n");
console.log(`\n[arms] case ${band(base.case).map((x) => x.toFixed(2)).join(" / ")}bn; cash set ${band(base.cash).map((x) => x.toFixed(2)).join(" / ")}bn`);
for (const [k, v] of Object.entries(arms)) {
  const f = (x) => (x >= 0 ? "+" : "") + x.toFixed(2);
  console.log(`  ${v.role.padEnd(6)} ${k.padEnd(20)} national ${f(v.national_delta_bn).padStart(7)}  case ${v.case.band_bn.map((x) => x.toFixed(2)).join(" / ")} (${v.case.band_change_bn.map(f).join(" / ")})  cash (${v.cash.band_change_bn.map(f).join(" / ")})`);
}
for (const r of schoolBeside.filter((r) => r.set === "case")) console.log(`  beside school key, ${r.end} end, legacy ${r.legacy_fraction_of_benefits} of benefits: factor ${r.key_factor.toFixed(5)} x $${r.group_school_cost_bn.toFixed(2)}bn = ${r.change_bn >= 0 ? "+" : ""}${r.change_bn.toFixed(3)}bn`);
console.log(`[written] derived/case_oct05.csv, by_line_oct05.csv, school_beside_oct05.csv, case_oct05.json`);
