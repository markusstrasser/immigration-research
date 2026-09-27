/* Attack on item 1 (transfer consolidation) of main_case_candidate_2026_09_28. Read-only: requires the candidate's
 * package and writes nothing. Run from the repository root:
 *   node infra/immigration-fiscal/candidate_attack_2026_09_28/probe_item1_transfer.cjs
 *
 *   A. Is the "after" gate an identity? consolidate(withSyntheticTransfer(m, 1), T + 1) against consolidate(m, T),
 *      cell by cell. The two scale factors multiply to (n - T) / n whatever the engine does.
 *   B. The control on a transfer the fix does not consolidate: consolidate(withSyntheticTransfer(m, 1), T).
 *   C. Mutation test: which broken consolidate() would the gate catch?
 *   D. Item 1 moves nothing else: every line, P, F and every capital component, OFF against item 1 alone.
 *   E. Item 1 is a re-key: +0.2207 = (r_e ke - r_h kh) T. With the housing enterprise keyed like rental assistance
 *      (its tenants), consolidation moves nothing, and the September 27 case moves by (ke - kh) S_housing.
 */
"use strict";
const path = require("path");
const fs = require("fs");
const C = require(path.join(__dirname, "..", "main_case_candidate_2026_09_28", "package.cjs"));
const { Engine, METHODS, RENTAL, ENTERPRISE_LINE, ALLOCS, TRANSFERS, OFF, withCentral, specsFor, modelFor, evaluateFull,
  consolidate, withSyntheticTransfer, withProduction } = C;
const S = C.SEPT27;
const T = TRANSFERS.public_housing_operating.bn;
const ENDS = [48, 11];
const row = (r, side, id) => r.evaluation[side].find((l) => l.id === id);
const keyOf = (r, side, id) => row(r, side, id).amount_bn / row(r, side, id).national_bn;
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const withOff = (x) => Object.assign({}, OFF, x);
const cellsOf = (m) => {
  const h = m.spending.lines.find((l) => l.id === RENTAL), e = m.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
  const hc = Object.values(h.keys).flatMap((k) => ALLOCS.map((a) => k[a]));
  const ec = Object.values(e.cells).flatMap((k) => ALLOCS.map((a) => k[a]));
  return { national: [h.national_bn, e.national_bn], vals: hc.concat(ec).flatMap((c) => [c.target_bn, c.other_bn]) };
};

const oo = withCentral(OFF);
const specs = specsFor(oo);
const noCap = specsFor(withOff({ capital: false }));
const bases = METHODS.map((meth) => withProduction(S.modelFor("central", meth, oo), oo.production));
const costAt = (m, spec) => evaluateFull(m, spec).cost_bn;

console.log(`T = ${T} bn (HUD FY2024 PH operating obligations)`);
console.log("\n[A] the after-gate's two models, cell by cell");
METHODS.forEach((meth, k) => {
  const a = cellsOf(consolidate(bases[k], T)), b = cellsOf(consolidate(withSyntheticTransfer(bases[k], 1), T + 1));
  const dn = worst(a.national.map((x, i) => x - b.national[i]));
  const dv = worst(a.vals.map((x, i) => x - b.vals[i]));
  const rel = worst(a.vals.map((x, i) => (x === 0 ? b.vals[i] : (x - b.vals[i]) / x)));
  console.log(`  ${meth}: ${a.vals.length} cell values; max |diff| national ${dn.toExponential(2)}, cells ${dv.toExponential(2)} bn (relative ${rel.toExponential(2)})`);
});
// The same identity at any T: the gate cannot tell a right T from a wrong one.
for (const t of [0.001, T, 30, 60]) {
  const gap = worst(METHODS.flatMap((_, k) => ENDS.map((i) => costAt(consolidate(withSyntheticTransfer(bases[k], 1), t + 1), specs[i])
    - costAt(consolidate(bases[k], t), specs[i]))));
  console.log(`  gate formula at T = ${t}: max |cost diff| ${gap.toExponential(2)} bn`);
}

console.log("\n[B] a $1bn internal transfer that the fix does not consolidate (spec 48, capital off; then 48 / 11 with capital)");
METHODS.forEach((meth, k) => {
  const cm = consolidate(bases[k], T), sm = consolidate(withSyntheticTransfer(bases[k], 1), T);
  const today = costAt(withSyntheticTransfer(bases[k], 1), noCap[48]) - costAt(bases[k], noCap[48]);
  const after = costAt(sm, noCap[48]) - costAt(cm, noCap[48]);
  const ends = ENDS.map((i) => costAt(sm, specs[i]) - costAt(cm, specs[i]));
  console.log(`  ${meth}: today ${(1000 * today).toFixed(4)}m; after consolidation ${(1000 * after).toFixed(4)}m; with capital at 48 / 11 ${ends.map((x) => (1000 * x).toFixed(4) + "m").join(" / ")}`);
});

console.log("\n[C] mutation test: the gate's formula on broken consolidate() variants (max |cost diff| over both methods, specs 48 and 11)");
const scale = (cells, f) => { for (const c of cells) { c.target_bn *= f; c.other_bn *= f; } };
const legs = (m) => {
  const h = m.spending.lines.find((l) => l.id === RENTAL), e = m.receipts.lines.find((l) => l.id === ENTERPRISE_LINE);
  return { h, e, hc: Object.values(h.keys).flatMap((x) => ALLOCS.map((a) => x[a])), ec: Object.values(e.cells).flatMap((x) => ALLOCS.map((a) => x[a])) };
};
const MUTANTS = {
  "correct (the candidate's)": consolidate,
  "rental leg only": (m0, bn) => { const m = Engine.clone(m0), L = legs(m); scale(L.hc, (L.h.national_bn - bn) / L.h.national_bn); L.h.national_bn -= bn; return m; },
  "enterprise leg only": (m0, bn) => { const m = Engine.clone(m0), L = legs(m); scale(L.ec, (L.e.national_bn - bn) / L.e.national_bn); L.e.national_bn -= bn; return m; },
  "rental factor on both legs": (m0, bn) => { const m = Engine.clone(m0), L = legs(m), f = (L.h.national_bn - bn) / L.h.national_bn; scale(L.hc, f); scale(L.ec, f); L.h.national_bn -= bn; L.e.national_bn -= bn; return m; },
  "national totals only, cells untouched": (m0, bn) => { const m = Engine.clone(m0), L = legs(m); L.h.national_bn -= bn; L.e.national_bn -= bn; return m; },
  "twice the amount": (m0, bn) => consolidate(m0, 2 * bn),
  "no-op": (m0) => m0,
};
for (const [name, f] of Object.entries(MUTANTS)) {
  const gap = worst(METHODS.flatMap((_, k) => ENDS.map((i) => costAt(f(withSyntheticTransfer(bases[k], 1), T + 1), specs[i]) - costAt(f(bases[k], T), specs[i]))));
  console.log(`  ${name.padEnd(40)} ${gap.toExponential(2)} bn  ${gap < 1e-9 ? "PASSES the gate" : "fails the gate"}`);
}
// A mutant pair: withSyntheticTransfer and consolidate broken the same way (both rental-leg only).
const synthRentalOnly = (m0, bn) => { const m = Engine.clone(m0), L = legs(m); scale(L.hc, (L.h.national_bn + bn) / L.h.national_bn); L.h.national_bn += bn; return m; };
const pairGap = worst(METHODS.flatMap((_, k) => ENDS.map((i) => costAt(MUTANTS["rental leg only"](synthRentalOnly(bases[k], 1), T + 1), specs[i]) - costAt(MUTANTS["rental leg only"](bases[k], T), specs[i]))));
console.log(`  pair broken alike (both helpers rental-leg only)   ${pairGap.toExponential(2)} bn  ${pairGap < 1e-9 ? "PASSES the after-gate" : "fails"}`);

console.log("\n[D] item 1 alone against the September 27 case: what moves (all 64 specs, both methods)");
const item1 = withOff({ internal_transfer: "public_housing_operating" });
const oo1 = withCentral(item1), specs1 = specsFor(oo1);
const moved = new Map();
let pfGap = 0, capGap = 0;
METHODS.forEach((meth, k) => {
  const m0 = modelFor("central", meth, oo), m1 = modelFor("central", meth, oo1);
  specs.forEach((s, i) => {
    const a = evaluateFull(m0, s), b = evaluateFull(m1, specs1[i]);
    for (const side of ["spending", "receipts"]) a.evaluation[side].forEach((x, j) => {
      const y = b.evaluation[side][j];
      const d = Math.max(Math.abs(x.amount_bn - y.amount_bn), Math.abs((x.effect_bn || 0) - (y.effect_bn || 0)), Math.abs(x.response - y.response));
      if (d > 0) moved.set(`${side}:${x.id}`, Math.max(moved.get(`${side}:${x.id}`) || 0, d));
    });
    pfGap = Math.max(pfGap, Math.abs(a.evaluation.private_wtp_bn - b.evaluation.private_wtp_bn), Math.abs(a.evaluation.induced_receipts_bn - b.evaluation.induced_receipts_bn));
    a.capital.components.forEach((x, j) => { capGap = Math.max(capGap, Math.abs(x.return_bn - b.capital.components[j].return_bn), Math.abs(x.key - b.capital.components[j].key)); });
  });
});
console.log(`  lines that move: ${[...moved].map(([id, d]) => `${id} (max ${d.toFixed(6)})`).join(", ") || "none"}`);
console.log(`  P and F: max |diff| ${pfGap.toExponential(2)}; capital components (return and key): max |diff| ${capGap.toExponential(2)}`);

console.log("\n[E] item 1 as a re-key of public housing's operating subsidy");
const esv = fs.readFileSync(path.join(__dirname, "..", "capital_return_services_2026_09_27", "derived", "enterprise_surplus_vs_return.csv"), "utf8").split("\n");
const hdr = esv[0].split(",");
const hrow = esv.find((l) => l.startsWith("housing and urban renewal")).split(",");
const S_h = Number(hrow[hdr.indexOf("current_surplus_2024_bn")]);
console.log(`  NIPA 3.8 l13 housing and urban renewal current surplus 2024: ${S_h} bn (capital lane enterprise_surplus_vs_return.csv)`);
ENDS.forEach((i) => {
  const vals = METHODS.map((meth, k) => {
    const r = evaluateFull(modelFor("central", meth, oo), specs[i]);
    const kh = keyOf(r, "spending", RENTAL), ke = keyOf(r, "receipts", ENTERPRISE_LINE);
    const rh = row(r, "spending", RENTAL).response, re = row(r, "receipts", ENTERPRISE_LINE).response;
    return { kh, ke, rh, re, item1: (re * ke - rh * kh) * T, rekey27: re * (ke - kh) * S_h, rekeyCand: re * (ke - kh) * (S_h - T) };
  });
  const mean = (f) => vals.reduce((a, v) => a + f(v), 0) / vals.length;
  console.log(`  spec ${i}: kh ${vals.map((v) => v.kh.toFixed(4)).join("/")} ke ${vals.map((v) => v.ke.toFixed(4)).join("/")} r_h ${vals[0].rh} r_e ${vals[0].re}`);
  console.log(`    item 1 as (r_e ke - r_h kh) T: ${mean((v) => v.item1).toFixed(4)} bn`);
  console.log(`    housing enterprise keyed like its tenants (kh) instead of ke: Sept 27 ${mean((v) => v.rekey27).toFixed(4)} bn; candidate ${mean((v) => v.rekeyCand).toFixed(4)} bn`);
  console.log(`    => with that key, item 1 moves the case by ${mean((v) => v.item1 + v.rekeyCand - v.rekey27).toExponential(2)} bn`);
});
