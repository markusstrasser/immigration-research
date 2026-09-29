// Prices each published-weight input of the v4 case on audit row 4, alone and together, through the adopted lane's
// package.cjs (evaluateFull at MAIN_SPECS[48] / [11]) for the set and, through forPayload(corrections_v4_cash.json),
// the cash set. The owner line follows the decomposition lane's probe (the reference cell's target over its kappa,
// summary_sept29.json v4.kappas); the others move their v4 amount by the row-4 reruns' change (derived/row4_*.json),
// with receipt changes expanded to every incidence rule as the v4 builder expands them (package expand()).
// Class A: group dollars summed at the published weights. Class B: ratios summed at the published weights and applied to
// row-4 amounts. Recorded, not applied: the adopted case is unchanged.
// Gates: the four reruns passed and match the payload's inputs; the oracle (the lane's summary.json, 1e-9, and v4 as
// adopted, 1e-4); the cash set's Medicare is September 27's; the positive control (owner +$0.34bn at both ends,
// $371.75 / 435.18bn: main_case_decomposition_2026_09_29/RESULT.md, "item 5's owner-occupied property tax").
// Writes derived/price_rekeys.json and derived/price_rekeys.csv. Run from the repository root after the row4_*.py scripts:
//   node infra/immigration-fiscal/row4_class_2026_09_29/price_rekeys.cjs
"use strict";
const fs = require("fs");
const path = require("path");
const F = path.resolve(__dirname, "..");
const OUT = path.join(__dirname, "derived");
const P = require(path.join(F, "main_case_2026_09_29/package.cjs"));
const K = require(path.join(F, "main_case_long_run_2026_09_27/package.cjs"));
const S = require(path.join(F, "main_case_decomposition_2026_09_29/derived/summary_sept29.json"));
const SUMMARY = JSON.parse(fs.readFileSync(path.join(F, "main_case_2026_09_29/derived/summary.json"), "utf8"));
const J = (f) => JSON.parse(fs.readFileSync(path.join(OUT, f), "utf8"));
const A = J("row4_parta.json"), BT = J("row4_benefit_tax.json"), SI = J("row4_state_index.json"), OA = J("row4_oasdi_ratio.json");
const CASH = JSON.parse(fs.readFileSync(path.join(F, "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json"), "utf8"));
const PC = P.forPayload(CASH);
const { Engine, MODEL } = P;
const REF = MODEL.receipts.reference;
const ENDS = [48, 11];
const ALLOCS = ["personal", "shared"];
const U = Engine.applyCorrections(MODEL, P.correctionsPayload());
const UC = Engine.applyCorrections(MODEL, CASH);
const U27 = Engine.applyCorrections(K.MODEL, K.correctionsPayload());
const V4 = P.V4PKG;
const pp = V4.pensionNet();
const lineOf = (m, side, id) => m[side].lines.find((l) => l.id === id);
let fails = 0;
const gate = (name, ok, detail) => { console.log(`GATE ${ok ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`); if (!ok) fails++; };

// Each re-key: (model) -> model, applied to a clone. `set_only` re-keys touch the pension switch, absent in the cash set.
const KAPPA_OWNER = S.v4.kappas.low.modeled_owner_property;
const partA = { A0: A.central.union.published_bn, A4: A.central.union.row4_bn };
const btBy = { shared: BT.shared.receipt_published_bn - BT.shared.receipt_row4_bn, personal: BT.personal.receipt_published_bn - BT.personal.receipt_row4_bn };
const SP_SYN = { public_order_safety: "state_price_public_order_safety", health_services: "state_price_health_services", recreation_culture: "state_price_recreation_culture" };
for (const [f, x] of [["row4_parta", A], ["row4_benefit_tax", BT], ["row4_state_index", SI], ["row4_oasdi_ratio", OA]]) gate(`${f}.json written with every gate passed`, Array.isArray(x.gates_failed) && x.gates_failed.length === 0);
gate("kappa for owner property is the same at both ends", S.v4.kappas.low.modeled_owner_property === S.v4.kappas.high.modeled_owner_property);
gate("relative rate in the rerun is the lane's", Math.abs(BT.relative_rate_published - OA.relative_rate_union) < 1e-9);
gate("benefit-tax receipts in the rerun are the payload's", ALLOCS.every((a) => Math.abs(BT[a].receipt_published_bn - pp.receipt_bn[a]) < 1e-9));
gate("Part A accrual in the rerun is the payload's", Math.abs(partA.A0 - pp.part_a_accrual_bn) < 1e-6, `${partA.A0} vs ${pp.part_a_accrual_bn}`);
gate("OASDI ratio_net in the rerun is the payload's", Math.abs(OA.published.ratio_net - pp.ratio_net) < 1e-9, `${OA.published.ratio_net} vs ${pp.ratio_net}`);
for (const [line, syn] of Object.entries(SP_SYN)) gate(`SP_PRE ${line} in the rerun is v4's`, Math.abs(SI.lines[line].sp_pre_published_bn - V4.SP_PRE[line]) < 1e-6, `${SI.lines[line].sp_pre_published_bn} vs ${V4.SP_PRE[line]}`);
for (const r of ["general_sales_tax", "personal_motor_vehicle"]) gate(`receipt factor ${r} in the rerun is v4's`, Math.abs(SI.receipts[r].factor_published - V4.SP_RECEIPT[r].factor) < 1e-9);

const REKEYS = {
  owner: { cls: "A", set_only: false, apply(m) {
    const x = Engine.clone(m), l = lineOf(x, "receipts", "modeled_owner_property");
    for (const a of ALLOCS) l.cells[REF][a].target_bn /= KAPPA_OWNER;
    return x;
  } },
  part_a: { cls: "A", set_only: true, apply(m) {
    const med = lineOf(m, "spending", "medicare");
    return Engine.applyCorrections(m, { lines: [], edits: [{ side: "spending", line: "medicare", key: med.preferred_key, by: { personal: partA.A4 - partA.A0, shared: partA.A4 - partA.A0 } }] });
  } },
  benefit_tax: { cls: "A", set_only: true, apply(m) {
    return Engine.applyCorrections(m, { lines: [], edits: P.expand([{ side: "receipt", line: "federal_income_tax", by: btBy }]) });
  } },
  state_index: { cls: "B", set_only: false, apply(m) {
    const edits = Object.entries(SP_SYN).map(([line, syn]) => {
      const k = lineOf(m, "spending", syn).keys.k, r = SI.lines[line].ratio;
      return { side: "spending", line: syn, key: "k", by: Object.fromEntries(ALLOCS.map((a) => [a, k[a].target_bn * (r - 1)])) };
    });
    const shifts = ["general_sales_tax", "personal_motor_vehicle"].map((id) => {
      const x = SI.receipts[id], c = lineOf(m, "receipts", id).cells[REF];
      return { side: "receipt", line: id, by: Object.fromEntries(ALLOCS.map((a) => [a, (x.factor_row4 - x.factor_published) * c[a].target_bn / (1 + x.factor_published)])) };
    });
    return Engine.applyCorrections(m, { lines: [], edits: edits.concat(P.expand(shifts)) });
  } },
  oasdi_ratio: { cls: "B", set_only: true, apply(m) {
    const ss = lineOf(m, "spending", "social_security"), k = ss.keys[ss.preferred_key];
    // ratio_net on row 4: the rerun's gross ratio and timing, and the relative rate at row-4 weights (row4_benefit_tax.json).
    const r = OA.row4.ratio_gross * (1 - BT.relative_rate_row4 * OA.row4.timing) / OA.published.ratio_net;
    return Engine.applyCorrections(m, { lines: [], edits: [{ side: "spending", line: "social_security", key: ss.preferred_key, by: Object.fromEntries(ALLOCS.map((a) => [a, k[a].target_bn * (r - 1)])) }] });
  } },
};

const base = { set: ENDS.map((i) => P.evaluateFull(U, P.MAIN_SPECS[i]).cost_bn), cash: ENDS.map((i) => PC.evaluateFull(UC, PC.MAIN_SPECS[i]).cost_bn) };
const near = (got, want, tol) => got.every((g, j) => Math.abs(g - want[j]) < tol);
gate("oracle set", near(base.set, SUMMARY.main_case, 1e-9) && near(base.set, [371.4146, 434.8410], 1e-4), base.set.map((x) => x.toFixed(4)).join(" / "));
gate("oracle cash", near(base.cash, SUMMARY.cash_set.band_bn, 1e-9) && near(base.cash, [294.7011, 361.8175], 1e-4), base.cash.map((x) => x.toFixed(4)).join(" / "));
const med27 = lineOf(U27, "spending", "medicare").keys.medicare;
gate("the cash set has no Part A accrual (Medicare is the September 27 amount)",
  ALLOCS.every((a) => Math.abs(lineOf(UC, "spending", "medicare").keys.medicare[a].target_bn - med27[a].target_bn) < 1e-9), med27.shared.target_bn.toFixed(6));
const run = (names) => {
  const out = {};
  for (const [set, pk, m0] of [["set", P, U], ["cash", PC, UC]]) {
    let m = m0;
    for (const n of names) if (!(REKEYS[n].set_only && set === "cash")) m = REKEYS[n].apply(m);
    const c = ENDS.map((i) => pk.evaluateFull(m, pk.MAIN_SPECS[i]).cost_bn);
    out[set] = { cost: c, move: c.map((x, j) => x - base[set][j]) };
  }
  return out;
};
const rows = {};
for (const n of Object.keys(REKEYS)) rows[n] = run([n]);
const clsA = Object.keys(REKEYS).filter((n) => REKEYS[n].cls === "A");
rows.joint_published_frame = run(clsA);
rows.joint_with_ratios = run(Object.keys(REKEYS));
gate("positive control: owner on row 4 moves the set +$0.34bn at both ends (decomposition lane: 371.75 / 435.18)",
  rows.owner.set.move.every((x) => Math.abs(x - 0.34) < 0.005) && Math.abs(rows.owner.set.cost[0] - 371.75) < 0.005 && Math.abs(rows.owner.set.cost[1] - 435.18) < 0.005,
  rows.owner.set.move.map((x) => x.toFixed(4)).join(" / "));
const f4 = (x) => (x >= 0 ? "+" : "") + x.toFixed(4);
for (const [n, r] of Object.entries(rows)) {
  console.log(`${n.padEnd(22)} set ${r.set.cost.map((x) => x.toFixed(4)).join(" / ")} (${r.set.move.map(f4).join(" / ")}); cash ${r.cash.cost.map((x) => x.toFixed(4)).join(" / ")} (${r.cash.move.map(f4).join(" / ")})`);
}
if (fails) {
  console.error(`[BLOCKED] ${fails} gate(s) failed; nothing written`);
  process.exit(1);
}
const CLASS = { ...Object.fromEntries(Object.entries(REKEYS).map(([n, r]) => [n, r.cls])), joint_published_frame: "A", joint_with_ratios: "A+B" };
const csv = [["rekey", "class", "set_move_48", "set_move_11", "set_cost_48", "set_cost_11", "cash_move_48", "cash_move_11"].join(",")];
for (const [n, r] of Object.entries(rows)) csv.push([n, CLASS[n], ...r.set.move, ...r.set.cost, ...r.cash.move].map((v) => (typeof v === "number" ? v.toFixed(6) : v)).join(","));
fs.writeFileSync(path.join(OUT, "price_rekeys.csv"), csv.join("\n") + "\n");
fs.writeFileSync(path.join(OUT, "price_rekeys.json"), JSON.stringify({ base, rows, kappa_owner: KAPPA_OWNER, part_a: partA, benefit_tax_by: btBy,
  oasdi_ratio: { published: OA.published.ratio_net, row4_rate_held: OA.row4.ratio_net, row4: OA.row4.ratio_gross * (1 - BT.relative_rate_row4 * OA.row4.timing) }, gates_failed: fails }, null, 1));
