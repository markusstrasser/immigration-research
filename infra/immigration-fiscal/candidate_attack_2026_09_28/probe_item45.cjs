/* Attack on item 4 (public pay) and item 5 (anything else) of main_case_candidate_2026_09_28. Read-only: requires
 * the candidate's package, reads its derived csv files, writes nothing. Run from the repository root:
 *   node infra/immigration-fiscal/candidate_attack_2026_09_28/probe_item45.cjs
 *
 *   4. The public-pay variant charges public employers the wage change "on an unchanged public workforce". The account's
 *      own spending responses shrink government consumption in the counterfactual. The overlap is (removed share) x
 *      charge: the account already prices the removed workers at today's wage.
 *   5a. Items 1 and 2 add exactly; nothing but the named lines, P and F moves (every spec, both methods).
 *   5b. The ends: which specifications are the band's ends under every case, and how close the runner-up is.
 *   5c. The outer range from components.csv, and with the long-run component read jointly with congestion.
 */
"use strict";
const path = require("path");
const fs = require("fs");
const C = require(path.join(__dirname, "..", "main_case_candidate_2026_09_28", "package.cjs"));
const { METHODS, MODEL, OFF, CANDIDATE, withCentral, specsFor, modelFor, evaluateFull } = C;
const DER = path.join(__dirname, "..", "main_case_candidate_2026_09_28", "derived");
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const runs = (o) => { const oo = withCentral(o), specs = specsFor(oo);
  return METHODS.map((meth) => { const m = modelFor("central", meth, oo); return specs.map((s) => evaluateFull(m, s)); }); };
const withOff = (x) => Object.assign({}, OFF, x), withCand = (x) => Object.assign({}, CANDIDATE, x);
const SETS = { sept27: OFF, item1: withOff({ internal_transfer: "public_housing_operating" }), item2: withOff({ production: "row4" }),
  candidate: CANDIDATE, cand_replacement: withCand({ road: "replacement" }), cand_fixed_stock: withCand({ road: "fixed_stock" }),
  cand_public_pay: withCand({ public_pay: true }), sept27_public_pay: withOff({ public_pay: true }) };
const R = Object.fromEntries(Object.entries(SETS).map(([k, o]) => [k, runs(o)]));
const K = Object.fromEntries(Object.entries(R).map(([k, rs]) => [k, rs.map((xs) => xs.map((r) => r.cost_bn))]));
const family = Object.fromEntries(MODEL.spending.lines.map((l) => [l.id, l.family]));

console.log("[4] public pay against the account's own shrinking of government consumption (candidate, both methods averaged)");
const pay = C.PROD.public_pay.row4;
for (const i of [48, 11]) {
  const shares = METHODS.map((_, m) => {
    const sp = R.candidate[m][i].evaluation.spending;
    const cons = sp.filter((l) => family[l.id] === "consumption");
    const nat = cons.reduce((a, l) => a + l.national_bn, 0), natNoDef = cons.filter((l) => l.id !== "defense").reduce((a, l) => a + l.national_bn, 0);
    const removed = -cons.reduce((a, l) => a + l.effect_bn, 0);
    const syn = -sp.filter((l) => ["school_reprice", "college_rekey"].includes(l.id)).reduce((a, l) => a + l.effect_bn, 0);
    return { all: removed / nat, noDef: removed / natNoDef, noDefSyn: (removed + syn) / natNoDef, removed, nat, natNoDef };
  });
  const norm = specsFor(withCentral(CANDIDATE))[i].normalization;
  const charge = pay[norm].charge_bn;
  const lo = mean(shares.map((s) => s.all)), hi = mean(shares.map((s) => s.noDefSyn));
  console.log(`  spec ${i} (${norm}): consumption removed $${mean(shares.map((s) => s.removed)).toFixed(2)}bn of $${shares[0].nat.toFixed(1)}bn `
    + `(${(100 * lo).toFixed(2)}%); without defense ${(100 * mean(shares.map((s) => s.noDef))).toFixed(2)}%, with the school rows ${(100 * hi).toFixed(2)}%`);
  console.log(`    charge ${charge.toFixed(4)}; overlap with the account's response ${(charge * lo).toFixed(2)}–${(charge * hi).toFixed(2)}; `
    + `charge on the counterfactual workforce ${(charge * (1 - hi)).toFixed(2)}–${(charge * (1 - lo)).toFixed(2)}`);
}
const payEnds = METHODS.map((_, m) => { const xs = K.cand_public_pay[m]; return [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]; });
console.log(`  public-pay band ${mean(K.cand_public_pay.map((xs) => Math.min(...xs))).toFixed(4)}–${mean(K.cand_public_pay.map((xs) => Math.max(...xs))).toFixed(4)}; ends by method ${payEnds.map((e) => e.join("/")).join(", ")}`);

console.log("\n[5a] additivity and unnamed moves (64 specs x 2 methods)");
const add = worst(METHODS.flatMap((_, m) => K.candidate[m].map((x, i) => (x - K.sept27[m][i]) - (K.item1[m][i] - K.sept27[m][i]) - (K.item2[m][i] - K.sept27[m][i]))));
console.log(`  candidate - sept27 - (item1 + item2 changes): max |diff| ${add.toExponential(2)} bn`);
const moved = new Map();
METHODS.forEach((_, m) => R.candidate[m].forEach((a, i) => {
  const b = R.sept27[m][i];
  for (const side of ["spending", "receipts"]) a.evaluation[side].forEach((x, j) => {
    const y = b.evaluation[side][j];
    if (x.id !== y.id) moved.set(`order ${side}`, 1);
    const d = Math.max(Math.abs(x.amount_bn - y.amount_bn), Math.abs(x.response - y.response), Math.abs((x.effect_bn || 0) - (y.effect_bn || 0)));
    if (d > 0) moved.set(`${side}:${x.id}`, Math.max(moved.get(`${side}:${x.id}`) || 0, d));
  });
  for (const k of ["private_wtp_bn", "induced_receipts_bn"]) { const d = Math.abs(a.evaluation[k] - b.evaluation[k]); if (d > 0) moved.set(k, Math.max(moved.get(k) || 0, d)); }
  a.capital.components.forEach((x, j) => { const d = Math.abs(x.return_bn - b.capital.components[j].return_bn); if (d > 0) moved.set(`capital:${x.id}`, Math.max(moved.get(`capital:${x.id}`) || 0, d)); });
}));
console.log(`  what moves, candidate vs sept27 (max |change|): ${[...moved].map(([k, v]) => `${k} ${v.toFixed(4)}`).join("; ")}`);

console.log("\n[5b] band ends and the runner-up specification (per method: spec, cost; margin to the next spec)");
const specs = specsFor(withCentral(CANDIDATE));
const lab = (i) => { const s = specs[i]; return `${i}(${s.allocation},${s.normalization},gg ${Number(s.gg).toFixed(4)},${s.reading})`; };
for (const [k, cm] of Object.entries(K)) {
  const parts = cm.map((xs, m) => {
    const order = xs.map((x, i) => [x, i]).sort((a, b) => a[0] - b[0]);
    const [lo1, lo2] = order, [hi1, hi2] = [order[order.length - 1], order[order.length - 2]];
    return `${METHODS[m].replace("b_", "")}: low ${lab(lo1[1])} ${lo1[0].toFixed(2)} (next ${lo2[1]} +${(lo2[0] - lo1[0]).toFixed(2)}), `
      + `high ${hi1[1]} ${hi1[0].toFixed(2)} (next ${hi2[1]} -${(hi1[0] - hi2[0]).toFixed(2)})`;
  });
  console.log(`  ${k}:\n    ${parts.join("\n    ")}`);
}

console.log("\n[5c] the outer range from components.csv");
const rows = fs.readFileSync(path.join(DER, "components.csv"), "utf8").trim().split("\n");
const hdr = rows[0].split(",");
const parse = (line) => { const out = []; let cur = "", q = false; for (const ch of line) { if (ch === '"') q = !q; else if (ch === "," && !q) { out.push(cur); cur = ""; } else cur += ch; } out.push(cur); return out; };
const comps = rows.slice(1).map((l) => Object.fromEntries(parse(l).map((v, j) => [hdr[j], v])));
const col = (c, k) => Number(c[k]);
const lowSum = comps.reduce((a, c) => a + Math.min(0, col(c, "candidate_low_end_lo")), 0);
const highSum = comps.reduce((a, c) => a + Math.max(0, col(c, "candidate_high_end_hi")), 0);
const band = [mean(K.candidate.map((xs) => Math.min(...xs))), mean(K.candidate.map((xs) => Math.max(...xs)))];
console.log(`  ${comps.length} components; band ${band.map((x) => x.toFixed(4)).join("–")}; band + sum of negative low-end extremes ${(band[0] + lowSum).toFixed(4)}; `
  + `+ sum of positive high-end extremes ${(band[1] + highSum).toFixed(4)}`);
const lr = comps.find((c) => c.component === "long_run_response");
const ra = fs.readFileSync(path.join(DER, "road_arm.csv"), "utf8").trim().split("\n");
const rh = ra[0].split(",");
const arm = ra.slice(1).map((l) => Object.fromEntries(parse(l).map((v, j) => [rh[j], v]))).filter((r) => r.road_case === "stationary_network" && r.long_run_variant !== "adopted");
console.log(`  long_run_response (account only): low end ${lr.candidate_low_end_lo} / ${lr.candidate_low_end_hi}, high end ${lr.candidate_high_end_lo} / ${lr.candidate_high_end_hi}`);
const joint = { low: [], high: [], lowAcc: [], highAcc: [] };
for (const r of arm) {
  const a48 = Number(r.account_change_spec48_bn), a11 = Number(r.account_change_spec11_bn);
  const j48 = a48 + Number(r.congestion_change_low_end_bn), j11 = a11 + Number(r.congestion_change_high_end_bn);
  joint.low.push(j48); joint.high.push(j11); joint.lowAcc.push(a48); joint.highAcc.push(a11);
  console.log(`    ${r.long_run_variant.padEnd(28)} account ${a48.toFixed(4)} / ${a11.toFixed(4)}; with congestion ${j48.toFixed(4)} / ${j11.toFixed(4)}`);
}
const ext = (xs) => [Math.min(0, ...xs), Math.max(0, ...xs)];
console.log(`  account-only extremes (48 / 11): ${ext(joint.lowAcc).map((x) => x.toFixed(4)).join(",")} / ${ext(joint.highAcc).map((x) => x.toFixed(4)).join(",")}`);
console.log(`  joint extremes (48 / 11): ${ext(joint.low).map((x) => x.toFixed(4)).join(",")} / ${ext(joint.high).map((x) => x.toFixed(4)).join(",")}`);
const dLow = ext(joint.low)[0] - Math.min(0, Number(lr.candidate_low_end_lo)), dHigh = ext(joint.high)[1] - Math.max(0, Number(lr.candidate_high_end_hi));
console.log(`  outer range with the component read jointly: ${(band[0] + lowSum + dLow).toFixed(4)}–${(band[1] + highSum + dHigh).toFixed(4)} (moves ${dLow.toFixed(4)} / ${dHigh.toFixed(4)})`);
const cs = JSON.parse(fs.readFileSync(path.join(DER, "summary.json"), "utf8"));
console.log(`  summary.json range: ${JSON.stringify(cs.range && (cs.range.candidate || cs.range)).slice(0, 300)}`);
