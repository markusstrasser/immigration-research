/* The sign-reversal figures of the complete account on the main case adopted 2026-09-24.
 *
 * Definition (main_case_2026_09_23/sign_reversal.py, from the September 20 account): ordinary
 * service budgets respond at a common share s; defense and existing interest stay fixed; general
 * government responds at its adopted g whatever s is; transfers and direct receipts respond fully;
 * fiscal weight 1, no excluded capital owners. Welfare is linear in s, so the break-even share is
 * w(0) / (w(0) - w(1)). The break-even rows hold private capital fully adjusted; the frozen-services
 * row holds it fixed. The least adverse end pairs g 0.59 with uncompensated care at its low key, the
 * most adverse end g 0.84 with the high key.
 *
 * Frame: CBO incidence rules (cbo_collective) and preferred keys, the frame the package's receipt
 * changes are measured on. The September 23 lane's break-even rows are on this frame and are
 * reproduced first (gate). Its frozen-services row ranges over every incidence rule and key set,
 * so on this frame the script reports that row for both cases side by side instead.
 * The package enters as the engine's corrections payload (package.cjs correctionsPayload(): the two
 * fill-in methods' shift lists averaged, the engine being linear).
 * Run from anywhere: node sign_reversal.cjs  ->  derived/sign_reversal.csv
 * Imported (main_case_2026_09_26/sign_reversal.cjs), it exports the definition and runs nothing.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require("./package.cjs");
const { Engine, MODEL, SYN, HERE, gate, near, gateState, readJson, csvRows, build, correctionsPayload } = P;

const inputs = readJson("main_case_2026_09_23/derived/inputs.json");
const published = csvRows("main_case_2026_09_23/derived/sign_reversal.csv");
const PAIRS = [
  { end: "least", g: inputs.general_government_response.low, uc: "uninsured_use_low" },
  { end: "most", g: inputs.general_government_response.high, uc: "uninsured_use_high" },
];
const SHARES = Engine.schoolShareBounds(MODEL);
const DIMS = Engine.PRODUCTION_DIMS;
function productions(capital) {
  let out = [{}];
  for (const d of DIMS) {
    const levels = d === "capital_adjustment" ? [capital] : d === "excluded_capital_owner_share" ? [0] : MODEL.production.dims[d];
    out = out.flatMap((p) => levels.map((v) => ({ ...p, [d]: v })));
  }
  return out;
}
function welfare(m, allocation, s, pair, production, share) {
  const st = Engine.defaultState(m);
  st.allocation = allocation;
  st.receipt_scenario = m.receipts.reference;
  st.production = production;
  st.service_response = s;
  st.general_government_response = pair.g;
  st.school_share = share;
  st.key_override = { public_order_safety: "use", medicaid_and_chip_other_medical: pair.uc };
  st.response_override = { [SYN.school]: s * share, [SYN.college]: s * (1 - share), [SYN.constants]: 1 };
  return Engine.evaluate(m, st).welfare_bn;
}


function breakEven(m, allocation, pairs = PAIRS) {
  const roots = { least: [], most: [] };
  for (const pair of pairs) for (const prod of productions(1)) for (const share of SHARES) {
    const w0 = welfare(m, allocation, 0, pair, prod, share), w1 = welfare(m, allocation, 1, pair, prod, share);
    roots[pair.end].push(w0 / (w0 - w1));
  }
  return [Math.min(...roots.most), Math.max(...roots.least)];
}
function frozen(m, pairs = PAIRS) {
  const w = { least: [], most: [] };
  for (const allocation of ["personal", "shared"]) for (const pair of pairs) for (const prod of productions(0)) for (const share of SHARES) {
    w[pair.end].push(welfare(m, allocation, 0, pair, prod, share));
  }
  return [Math.min(...w.most), Math.max(...w.least)];
}

module.exports = { PAIRS, SHARES, productions, welfare, breakEven, frozen };
if (require.main === module) {
  const baseModel = build([]);
  const pkgModel = Engine.applyCorrections(MODEL, correctionsPayload());
  console.log("[gates]");
  const mainCheck = P.band(pkgModel);
  const want = csvRows("main_case_2026_09_24/derived/main_case_bands.csv").find((r) => r.variant === "adopted");
  gate("the averaged package reproduces the adopted main case", near(mainCheck[0], +want.cost_low_bn, 1e-4)
    && near(mainCheck[1], +want.cost_high_bn, 1e-4), `${mainCheck[0].toFixed(4)}–${mainCheck[1].toFixed(4)}`);
  const rows = [["measure", "sept23_low", "sept23_high", "sept24_low", "sept24_high"]];
  for (const allocation of ["personal", "shared"]) {
    const b = breakEven(baseModel, allocation);
    const pub = published.find((r) => r.measure === `service_break_even_${allocation}`);
    gate(`break-even, ${allocation}: September 23 reproduces`, near(b[0], +pub.adopted_low, 1e-4) && near(b[1], +pub.adopted_high, 1e-4),
      `${(100 * b[0]).toFixed(2)}–${(100 * b[1]).toFixed(2)}% vs ${(100 * pub.adopted_low).toFixed(2)}–${(100 * pub.adopted_high).toFixed(2)}%`);
    const k = breakEven(pkgModel, allocation);
    rows.push([`service_break_even_${allocation}`, b[0], b[1], k[0], k[1]]);
  }
  const f0 = frozen(baseModel), f1 = frozen(pkgModel);
  rows.push(["frozen_services_capital_fixed_welfare_bn_cbo_preferred", f0[0], f0[1], f1[0], f1[1]]);
  fs.writeFileSync(path.join(HERE, "derived", "sign_reversal.csv"),
    rows.map((r) => r.map((x) => (typeof x === "number" ? x.toFixed(4) : x)).join(",")).join("\n") + "\n");

  console.log("\n[result]");
  for (const r of rows.slice(1)) {
    const pct = r[0].startsWith("service");
    const fmt = (x) => (pct ? `${(100 * x).toFixed(1)}%` : x.toFixed(1));
    console.log(`  ${r[0].padEnd(56)} Sept 23 ${fmt(r[1])} to ${fmt(r[2])}   Sept 24 ${fmt(r[3])} to ${fmt(r[4])}`);
  }
  if (gateState.failures) { console.error(`FAIL: ${gateState.failures} gate(s)`); process.exit(1); }
  console.log("all gates passed");
}
