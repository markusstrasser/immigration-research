// Gate 1 (oracle) and the line inventory: every receipt and spending line and capital component whose amount, key or
// response differs between the September 27 case and v4 at specifications 48 / 11.
// Gates: the adopted payload through main_case_2026_09_29/package.cjs reproduces the lane's summary.json (main_case and
// cash_set.band_bn, 1e-9) and v4 as adopted ($371.4146 / 434.8410bn, cash $294.7011 / 361.8175bn, 1e-4); the
// September 27 package reproduces summary.json's adopted_2026_09_27 (1e-9).
// Writes derived/lines_diff.json. Run from the repository root: node infra/immigration-fiscal/row4_class_2026_09_29/lines_diff.cjs
"use strict";
const fs = require("fs");
const path = require("path");
const F = path.resolve(__dirname, "..");
const OUT = path.join(__dirname, "derived");
const P = require(path.join(F, "main_case_2026_09_29/package.cjs"));
const K = require(path.join(F, "main_case_long_run_2026_09_27/package.cjs"));
const SUMMARY = JSON.parse(fs.readFileSync(path.join(F, "main_case_2026_09_29/derived/summary.json"), "utf8"));
const CASH = JSON.parse(fs.readFileSync(path.join(F, "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json"), "utf8"));
const PC = P.forPayload(CASH);
const { Engine, MODEL } = P;
const ENDS = [48, 11];

const U = Engine.applyCorrections(MODEL, P.correctionsPayload());
const UC = Engine.applyCorrections(MODEL, CASH);
const U27 = Engine.applyCorrections(K.MODEL, K.correctionsPayload());
const published = { set: SUMMARY.main_case, cash: SUMMARY.cash_set.band_bn };
const adopted = { set: [371.4146, 434.8410], cash: [294.7011, 361.8175] };
const out = { gate1: {} };
let ok = true;
const near = (got, want, tol) => got.every((g, j) => Math.abs(g - want[j]) < tol);
for (const [name, pk, m] of [["set", P, U], ["cash", PC, UC]]) {
  const got = ENDS.map((i) => pk.evaluateFull(m, pk.MAIN_SPECS[i]).cost_bn);
  const pass = near(got, published[name], 1e-9) && near(got, adopted[name], 1e-4 + 5e-5);
  ok = ok && pass;
  out.gate1[name] = got;
  console.log(`GATE 1 oracle ${name}: ${got.map((g) => g.toFixed(4)).join(" / ")} want ${adopted[name].join(" / ")} (summary.json 1e-9) ${pass ? "PASS" : "FAIL"}`);
}
const got27 = ENDS.map((i) => K.evaluateFull(U27, K.MAIN_SPECS[i]).cost_bn);
const pass27 = near(got27, SUMMARY.adopted_2026_09_27, 1e-9);
ok = ok && pass27;
console.log(`GATE sept27 reference: ${got27.map((g) => g.toFixed(4)).join(" / ")} (summary.json adopted_2026_09_27 1e-9) ${pass27 ? "PASS" : "FAIL"}`);

// Per-line inventory at each end.
const rows = [];
for (const [j, i] of ENDS.entries()) {
  const e4 = P.evaluateFull(U, P.MAIN_SPECS[i]);
  const e27 = K.evaluateFull(U27, K.MAIN_SPECS[i]);
  const s4 = P.MAIN_SPECS[i], s27 = K.MAIN_SPECS[i];
  const idx = (ev, side) => Object.fromEntries(ev.evaluation[side].map((r) => [r.id, r]));
  for (const side of ["receipts", "spending"]) {
    const a = idx(e4, side), b = idx(e27, side);
    for (const id of Object.keys(a)) {
      const x = a[id], y = b[id];
      const moved = !y || Math.abs(x.amount_bn - y.amount_bn) > 1e-9 || Math.abs(x.response - y.response) > 1e-12 || x.key !== y.key;
      rows.push({ end: i, side, id, key: x.key, amount_v4: x.amount_bn, response_v4: x.response, effect_v4: x.effect_bn,
        amount_27: y ? y.amount_bn : null, response_27: y ? y.response : null, key_27: y ? y.key : null, moved });
    }
  }
  const ca = Object.fromEntries(e4.capital.components.map((c) => [c.id, c]));
  const cb = Object.fromEntries(e27.capital.components.map((c) => [c.id, c]));
  for (const id of Object.keys(ca)) {
    const x = ca[id], y = cb[id];
    const moved = !y || Math.abs(x.key - y.key) > 1e-12 || Math.abs(x.response - y.response) > 1e-12;
    rows.push({ end: i, side: "capital", id, key: x.key, amount_v4: x.return_bn, response_v4: x.response, key_27: y ? y.key : null,
      amount_27: y ? y.return_bn : null, response_27: y ? y.response : null, moved });
  }
  console.log(`spec ${i}: allocation ${s4.allocation}, receipt_scenario ${s4.receipt_scenario || "(default)"}, justice ${s4.justice}; sept27 allocation ${s27.allocation}`);
}
for (const r of rows.filter((r) => r.moved)) {
  const f = (v) => (v === null || v === undefined ? "-" : typeof v === "number" ? v.toFixed(4) : v);
  console.log(`${r.end} ${r.side.padEnd(9)} ${r.id.padEnd(34)} key ${String(r.key).padEnd(22)} amt27 ${f(r.amount_27)} -> v4 ${f(r.amount_v4)}; resp ${f(r.response_27)} -> ${f(r.response_v4)}`);
}
if (!ok) {
  console.error("[BLOCKED] a gate failed; nothing written");
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "lines_diff.json"), JSON.stringify({ gate1: out.gate1, sept27: got27, rows }, null, 1));
