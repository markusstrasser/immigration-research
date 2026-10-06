/* The adopted main case (v5, main_case_2026_10_05: $390.29-461.24bn, cash set $307.38-383.41bn) with its pension
 * accrual on each arm of pension_tr2026.py, by an engine run: the case's payload plus two edits, evaluated at the case's
 * 64 specifications by candidate v4's package-free consumer (main_case_candidate_v4_2026_09_29/consumer.cjs: engine.js,
 * model.json and the payload), which the v5 lane gates against its package at every specification.
 *
 * The case's pension items (corrections.json meta.pension_accrual, from the pension lane at 9ea1beb):
 *   - social_security's group amount (its preferred key) is ratio_net x the union's OASDI receipts on the reference
 *     incidence rule (employee + employer OASDI + se_oasdi_share x self-employment tax);
 *   - medicare's swaps its Part A share (part_a_share of the amount) for the union's Part A accrual, a fixed amount;
 *   - the lineage's 3.04M added people (meta.lineage, arm b) carry their own accrual: the identified G3+ members' per
 *     member, and the white part of the blend at whites' own ratios, at G3+ ages.
 * An arm moves them by two edits, per allocation:
 *   social_security  (ratio_net_arm - ratio_net) x the union's OASDI receipts, read on the September 29 payload's model
 *                    (the v5 payload is it plus the lineage's edits; gate), plus (f_ss - 1) x the added people's Social
 *                    Security, f_ss being G3+'s net accrual per tax dollar at its own benefit-tax rate, arm over control;
 *   medicare         part_a_arm - part_a, plus (f_pa - 1) x the added people's Part A accrual (their medicare amount in
 *                    the case less (1 - part_a_share) x it in the cash set), f_pa being G3+'s Part A per HI tax dollar,
 *                    arm over control.
 * [APPROX] the added people's factors: G3+'s ratio for both parts of the blend, since the pension lane has no white run
 * on another path and the white part is priced at G3+ ages; and G3+'s own ratio in place of the generation split's
 * normalized share (second order). They carry about 8% of the change.
 * The cash set has the pension switch off (its payload has no pension_accrual block): no path enters it.
 *
 * Gates (each stops with [BLOCKED], nothing written):
 *   - the consumer reproduces the case and the cash set from their payloads (summary.json, 1e-9), ends at 48 / 11;
 *   - the per-member divisor is the payload's lineage population, summary.json's, and the case per member reproduces;
 *   - the v5 payload's edits begin with the September 29 payload's; the cash payloads have no pension block;
 *   - the union's social_security amount is ratio_net x its OASDI receipts, and its Part A is part_a_accrual_bn, at both
 *     allocations (1e-9): the payload's rule, read back;
 *   - the added people's social_security amounts are the lineage lane's (lineage_lines.csv arm b, 5e-6);
 *   - pension_tr2026.py's control is the payload's ratio_net and Part A exactly, and its summary.json is current;
 *   - an arm with no change reproduces the case at every specification (exact).
 * Recorded, not gated: the engine's change against the edits' sum (social_security and medicare respond at 1).
 *
 * Writes derived/case_oct05.csv (arm x end) and derived/case_oct05.json. Run from the repository root after
 * pension_tr2026.py:
 *   node infra/immigration-fiscal/pension_tr2026_2026_10_06/case_tr2026.cjs
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
const P5 = readJson(`${V5}/corrections.json`), P5C = readJson(`${V5}/corrections_cash.json`);
const P4 = readJson("main_case_2026_09_29/derived/corrections.json");
const P4C = readJson("main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json");
const SUM5 = readJson(`${V5}/summary.json`);
const MINE = JSON.parse(fs.readFileSync(path.join(OUT, "summary.json"), "utf8"));
const LIN = fs.readFileSync(path.join(FISCAL, "main_case_lineage_2026_10_05/derived/lineage_lines.csv"), "utf8").trim().split("\n")
  .map((l) => l.split(","));
const PP = P5.meta.pension_accrual;
const Eng = C.loadEngine(), MODEL = C.loadModel();
const REF = MODEL.receipts.reference;
const POP = P5.meta.lineage.counts.lineage_population;
if (!Number.isFinite(POP) || POP <= 0) fail(`the payload's lineage population is ${POP}`);

const costsOf = (payload) => C.evaluateAll(payload, { engine: Eng, model: MODEL }).map((r) => r.cost_bn);
const band = (xs) => [Math.min(...xs), Math.max(...xs)];
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const line = (m, side, id) => {
  const l = m[side].lines.find((x) => x.id === id);
  if (!l) fail(`no ${side} line ${id}`);
  return l;
};
const groupAmount = (m, id) => { const l = line(m, "spending", id); return byAlloc((a) => l.keys[l.preferred_key][a].target_bn); };
const receiptAmount = (m, id) => byAlloc((a) => line(m, "receipts", id).cells[REF][a].target_bn);
const oasdiOf = (m) => byAlloc((a) => PP.oasdi_lines.reduce((s, id) => s + receiptAmount(m, id)[a], 0) + PP.se_oasdi_share * receiptAmount(m, PP.se_line)[a]);

// ---------------------------------------------------------------------------------------------------
console.log("[gates: the case and its pension items]");
const base = costsOf(P5), baseCash = costsOf(P5C);
const [lo, hi] = band(base), [clo, chi] = band(baseCash);
gate("the consumer reproduces the case's band (summary.json main_case, 1e-9)",
  near(lo, SUM5.main_case[0], 1e-9) && near(hi, SUM5.main_case[1], 1e-9), `${lo.toFixed(4)} / ${hi.toFixed(4)}bn`);
gate("the case's ends are specifications 48 / 11", base.indexOf(lo) === ENDS.low && base.indexOf(hi) === ENDS.high);
gate("the consumer reproduces the cash set (summary.json cash_set, 1e-9)",
  near(clo, SUM5.cash_set.band_bn[0], 1e-9) && near(chi, SUM5.cash_set.band_bn[1], 1e-9), `${clo.toFixed(4)} / ${chi.toFixed(4)}bn`);
gate("the cash set's ends are specifications 48 / 11", baseCash.indexOf(clo) === ENDS.low && baseCash.indexOf(chi) === ENDS.high);
const PM = SUM5.v5.per_member_usd;
gate("the per-member divisor is summary.json's lineage, and the case per member reproduces (1e-6)",
  POP === PM.population && near(lo / POP * 1e9, PM.set[0], 1e-6) && near(hi / POP * 1e9, PM.set[1], 1e-6),
  `$${(lo / POP * 1e9).toFixed(0)}-${(hi / POP * 1e9).toFixed(0)} over ${(POP / 1e6).toFixed(2)}M`);
gate("the cash payloads have no pension block (the switch is off; no path enters them)", !P5C.meta.pension_accrual && !P4C.meta.pension_accrual);
gate("the v5 payload's edits begin with the September 29 payload's", JSON.stringify(P5.edits.slice(0, P4.edits.length)) === JSON.stringify(P4.edits),
  `${P4.edits.length} of ${P5.edits.length}`);
gate("the payload's pension block is the pension lane's at 9ea1beb", PP.source.commit === "9ea1beb" && PP.rules.part_a_rule === "fixed" && PP.rules.accrual_receipts === "set");

const m4 = Eng.applyCorrections(MODEL, P4), m4c = Eng.applyCorrections(MODEL, P4C);
const m5 = Eng.applyCorrections(MODEL, P5), m5c = Eng.applyCorrections(MODEL, P5C);
const oasdi = oasdiOf(m4);
const ss4 = groupAmount(m4, "social_security"), ss5 = groupAmount(m5, "social_security");
const mc4 = groupAmount(m4, "medicare"), mc4c = groupAmount(m4c, "medicare"), mc5 = groupAmount(m5, "medicare"), mc5c = groupAmount(m5c, "medicare");
const partAUnion = byAlloc((a) => mc4[a] - (1 - PP.part_a_share) * mc4c[a]);
gate("the union's social_security is ratio_net x its OASDI receipts, both allocations (1e-9)",
  ALLOCS.every((a) => near(ss4[a], PP.ratio_net * oasdi[a], 1e-9)), ALLOCS.map((a) => `${a} ${ss4[a].toFixed(4)} = ${PP.ratio_net.toFixed(6)} x ${oasdi[a].toFixed(4)}`).join("; "));
gate("the union's Part A accrual is part_a_accrual_bn, both allocations (1e-9)",
  ALLOCS.every((a) => near(partAUnion[a], PP.part_a_accrual_bn, 1e-9)), ALLOCS.map((a) => partAUnion[a].toFixed(6)).join(" / "));
const ssLin = byAlloc((a) => ss5[a] - ss4[a]);
const partALin = byAlloc((a) => (mc5[a] - mc4[a]) - (1 - PP.part_a_share) * (mc5c[a] - mc4c[a]));
const linRow = (end) => LIN.find((r) => r[0] === "set" && r[1] === "b" && r[2] === end && r[4] === "spending|social_security");
const hdr = LIN[0];
const linSS = (end) => Number(linRow(end)[hdr.indexOf("lineage_bn")]);
gate("the added people's social_security is the lineage lane's (lineage_lines.csv arm b; 48 shared, 11 personal; 5e-6)",
  near(ssLin.shared, linSS("low"), 5e-6) && near(ssLin.personal, linSS("high"), 5e-6), `${ssLin.shared.toFixed(4)} / ${ssLin.personal.toFixed(4)}bn`);
const ctl = MINE.arms.control;
gate("pension_tr2026.py's control is the payload's ratio_net and Part A (exact)", ctl.ratio_net === PP.ratio_net && ctl.part_a_bn === PP.part_a_accrual_bn,
  `${ctl.ratio_net} / ${ctl.part_a_bn}`);

// ---------------------------------------------------------------------------------------------------
// The arms.
function editsFor(a) {
  const fSS = a.g3plus_net_own_rate / ctl.g3plus_net_own_rate, fPA = a.g3plus_part_a_per_hi_tax_dollar / ctl.g3plus_part_a_per_hi_tax_dollar;
  const parts = {
    union_oasdi: byAlloc((x) => (a.ratio_net - ctl.ratio_net) * oasdi[x]),
    union_part_a: byAlloc(() => a.part_a_bn - ctl.part_a_bn),
    lineage_oasdi: byAlloc((x) => (fSS - 1) * ssLin[x]),
    lineage_part_a: byAlloc((x) => (fPA - 1) * partALin[x]),
  };
  const edits = [
    { side: "spending", line: "social_security", key: "social_security", by: byAlloc((x) => parts.union_oasdi[x] + parts.lineage_oasdi[x]) },
    { side: "spending", line: "medicare", key: "medicare", by: byAlloc((x) => parts.union_part_a[x] + parts.lineage_part_a[x]) },
  ];
  return { edits, parts, f_ss: fSS, f_pa: fPA };
}
const withEdits = (edits) => { const p = clone(P5); p.edits = p.edits.concat(edits); return p; };
const zero = costsOf(withEdits(editsFor(ctl).edits));
gate("the control arm (no change) reproduces the case at all 64 specifications (exact)", zero.every((v, i) => v === base[i]));

const specs = C.specifications(Eng, MODEL, P5);
const rows = [], arms = {};
let worstLinear = 0;
for (const [role, set] of [["arm", MINE.arms], ["beside", MINE.beside]]) {
  for (const [name, a] of Object.entries(set)) {
    const e = editsFor(a);
    const costs = costsOf(withEdits(e.edits));
    const [blo, bhi] = band(costs);
    const sum = specs.map((s) => e.edits[0].by[s.allocation] + e.edits[1].by[s.allocation]);
    worstLinear = Math.max(worstLinear, ...costs.map((v, i) => Math.abs(v - base[i] - sum[i])));
    arms[name] = { role, ratio_net: a.ratio_net, part_a_bn: a.part_a_bn, f_ss: e.f_ss, f_pa: e.f_pa, band_bn: [blo, bhi],
      band_specs: [costs.indexOf(blo), costs.indexOf(bhi)], band_change_bn: [blo - lo, bhi - hi],
      pension_accrual_bn: [blo - clo, bhi - chi], per_member_usd: [blo / POP * 1e9, bhi / POP * 1e9], edits: e.edits };
    for (const [end, idx] of Object.entries(ENDS)) {
      const al = specs[idx].allocation;
      rows.push({ arm: name, role, end, spec: idx, allocation: al, ratio_net: a.ratio_net, part_a_bn: a.part_a_bn,
        case_bn: base[idx], arm_bn: costs[idx], change_bn: costs[idx] - base[idx],
        change_union_oasdi_bn: e.parts.union_oasdi[al], change_union_part_a_bn: e.parts.union_part_a[al],
        change_lineage_oasdi_bn: e.parts.lineage_oasdi[al], change_lineage_part_a_bn: e.parts.lineage_part_a[al],
        pension_accrual_case_bn: base[idx] - baseCash[idx], pension_accrual_arm_bn: costs[idx] - baseCash[idx],
        cash_set_bn: baseCash[idx], arm_band_end_bn: end === "low" ? blo : bhi, arm_band_end_spec: costs.indexOf(end === "low" ? blo : bhi),
        per_member_usd: costs[idx] / POP * 1e9 });
    }
  }
}

// ---------------------------------------------------------------------------------------------------
fs.mkdirSync(OUT, { recursive: true });
const cols = Object.keys(rows[0]);
const fmt = (v) => (typeof v === "number" ? (Number.isInteger(v) ? String(v) : v.toFixed(6)) : String(v));
fs.writeFileSync(path.join(OUT, "case_oct05.csv"), [cols.join(","), ...rows.map((r) => cols.map((c) => fmt(r[c])).join(","))].join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "case_oct05.json"), JSON.stringify({
  case: "oct05 (main case v5, main_case_2026_10_05)", case_band_bn: [lo, hi], cash_set_band_bn: [clo, chi],
  pension_accrual_case_bn: [lo - clo, hi - chi], lineage_population: POP,
  union_oasdi_receipts_bn: oasdi, union_part_a_bn: partAUnion, lineage_social_security_bn: ssLin, lineage_part_a_bn: partALin,
  payload_pension_block: { ratio_net: PP.ratio_net, part_a_accrual_bn: PP.part_a_accrual_bn, part_a_share: PP.part_a_share,
    se_oasdi_share: PP.se_oasdi_share, source: PP.source },
  method: "engine run: the v5 payload plus two edits per arm, evaluated by consumer.cjs at the case's 64 specifications",
  engine_change_minus_edit_sum_worst_bn: worstLinear, arms, gates,
}, null, 1) + "\n");
console.log(`\n[arms] case ${lo.toFixed(2)} / ${hi.toFixed(2)}bn; pension accrual ${(lo - clo).toFixed(2)} / ${(hi - chi).toFixed(2)}bn`);
for (const [k, v] of Object.entries(arms)) {
  console.log(`  ${v.role.padEnd(6)} ${k.padEnd(24)} ${v.band_bn.map((x) => x.toFixed(2)).join(" / ")}bn (${v.band_change_bn.map((x) => (x >= 0 ? "+" : "") + x.toFixed(2)).join(" / ")}; specs ${v.band_specs.join("/")}); pension ${v.pension_accrual_bn.map((x) => x.toFixed(2)).join(" / ")}`);
}
console.log(`[check] engine change less the edits' sum, worst ${worstLinear.toExponential(1)}bn (both lines respond at 1)`);
console.log(`[written] ${path.relative(path.resolve(FISCAL, "..", ".."), OUT)}/case_oct05.csv, case_oct05.json`);
