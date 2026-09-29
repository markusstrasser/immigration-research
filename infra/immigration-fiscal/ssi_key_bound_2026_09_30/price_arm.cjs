/* Prices ssi_key.py's SSI keys through the adopted case (main_case_2026_09_29/package.cjs), the set and the cash set,
 * at specifications 48 (low end, shared allocation) and 11 (high end, personal).
 *
 * A key gives the group the line's household pool at the key's share: amount = national x household fraction x share,
 * the account's rule for a CPS key (cps_imputation_keys_2026_09_23/translate.py line_deltas). That amount replaces the
 * case's on the SSI line's `ssi` key. The case's amount carries the row-4 stack, the fill-in step (union-matched hot
 * deck) and CBO's income-group shift; the last two correct CPS reports, which an administrative key does not use, so
 * the swap replaces the amount whole. The row `admin_state_age_additive` keeps them instead: it adds national x fraction
 * x (the administrative share - the row-4 share), the back-test's sizing rule. The row `case_row4_share` replaces the
 * case's amount with its own row-4 share, which isolates the fill-in and the shift.
 *
 * The swap is an edit to the payload model's SSI cell. Engine.applyCorrections moves the same dollars out of other
 * residents, so the national total holds; the package's evaluateFull evaluates the edited model.
 *
 * Gates ([BLOCKED] on failure):
 *   - the oracle: the payload models give the case, 371.4146 / 434.8410, and the cash set, 294.7011 / 361.8175
 *     (summary.json to 1e-9 and the printed four decimals);
 *   - the SSI line is keyed `ssi` with response 1 and national 65.134 at both ends of both sets;
 *   - a zero edit returns the oracle exactly;
 *   - every move equals the edit at the specification's allocation (fiscal weight and response 1; 1e-9): the SSI
 *     amount enters the cost through its own line only.
 * Writes derived/arm.csv and derived/arm.json. Run from the repository root after ssi_key.py:
 *   node infra/immigration-fiscal/ssi_key_bound_2026_09_30/price_arm.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const FISCAL = path.join(__dirname, "..");
const P = require(path.join(FISCAL, "main_case_2026_09_29", "package.cjs"));
const readJson = (p) => JSON.parse(fs.readFileSync(path.join(FISCAL, p), "utf8"));
const CASH = readJson("main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json");
const SUMMARY = readJson("main_case_2026_09_29/derived/summary.json");
const AUDIT = readJson("ssi_key_bound_2026_09_30/derived/audit.json");
const LINE = "ssi", KEY = "ssi", NATIONAL = 65.134;
const ENDS = [["low", 48], ["high", 11]];
const PRINTED = { set: ["371.4146", "434.8410"], cash: ["294.7011", "361.8175"] };
const ORACLE = { set: SUMMARY.main_case, cash: SUMMARY.cash_set.band_bn };
const ALLOCS = ["personal", "shared"];
const fail = (msg) => { throw new Error("[BLOCKED] " + msg); };

// derived/shares.csv: variant, allocation, share, se, diff_vs_case, diff_se
const lines = fs.readFileSync(path.join(__dirname, "derived", "shares.csv"), "utf8").trim().split("\n");
const head = lines[0].split(",");
const SHARES = {};
for (const l of lines.slice(1)) {
  const r = Object.fromEntries(l.split(",").map((v, i) => [head[i], ["variant", "allocation"].includes(head[i]) ? v : Number(v)]));
  (SHARES[r.variant] = SHARES[r.variant] || {})[r.allocation] = r;
}
const HF = AUDIT.household_fraction;
const pool = NATIONAL * HF;
const VARIANTS = ["admin_state_age", "admin_state_age_additive", "admin_state_only", "admin_with_supplement",
  "admin_unauthorized_barred", "admin_citizens_only", "hybrid_cps_within_cell", "case_row4_share"];

const out = { lane: "ssi_key_bound_2026_09_30", package: "main_case_2026_09_29/package.cjs",
  cash_payload: "main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json", national_bn: NATIONAL,
  household_fraction: HF, ends: Object.fromEntries(ENDS), oracle: {}, case_amount_bn: {}, variants: {}, gates: [] };
const rows = [];
for (const [name, X] of [["set", P], ["cash", P.forPayload(CASH)]]) {
  const base = X.payloadModel();
  const at = (m) => ENDS.map(([, i]) => X.evaluateFull(m, X.MAIN_SPECS[i]));
  const r0 = at(base);
  const costs = r0.map((r) => r.cost_bn);
  costs.forEach((c, e) => {
    if (Math.abs(c - ORACLE[name][e]) > 1e-9 || c.toFixed(4) !== PRINTED[name][e]) fail(`${name} end ${e}: ${c} is not the oracle ${PRINTED[name][e]}`);
  });
  const allocOf = ENDS.map(([, i]) => X.MAIN_SPECS[i].allocation);
  r0.forEach((r, e) => {
    const row = r.evaluation.spending.find((l) => l.id === LINE);
    if (!row || row.key !== KEY || row.response !== 1 || row.national_bn !== NATIONAL) fail(`${name} end ${e}: the SSI line is not keyed ${KEY} at response 1 and national ${NATIONAL}`);
  });
  const cell = base.spending.lines.find((l) => l.id === LINE).keys[KEY];
  const caseAmount = Object.fromEntries(ALLOCS.map((a) => [a, cell[a].target_bn]));
  const edited = (by) => P.Engine.applyCorrections(base, { lines: [], edits: [{ side: "spending", line: LINE, key: KEY, by }], meta: base.corrections });
  const zero = at(edited({ personal: 0, shared: 0 })).map((r) => r.cost_bn);
  if (zero.some((c, e) => c !== costs[e])) fail(`${name}: a zero edit does not return the oracle exactly`);
  out.oracle[name] = { low_bn: costs[0], high_bn: costs[1] };
  out.case_amount_bn[name] = caseAmount;
  out.gates.push(`${name}: oracle ${costs.map((c) => c.toFixed(4)).join(" / ")}; SSI keyed ${KEY}, response 1, national ${NATIONAL}; zero edit exact`);

  for (const v of VARIANTS) {
    const amount = {}, by = {}, se = {};
    for (const a of ALLOCS) {
      const s = v === "admin_state_age_additive" ? SHARES.admin_state_age[a] : v === "case_row4_share" ? SHARES.case_cps[a] : SHARES[v][a];
      if (!s) fail(`shares.csv has no ${v} / ${a}`);
      if (v === "admin_state_age_additive") {
        by[a] = pool * s.diff_vs_case;
        amount[a] = caseAmount[a] + by[a];
      } else {
        amount[a] = pool * s.share;
        by[a] = amount[a] - caseAmount[a];
      }
      se[a] = pool * s.diff_se;  // sampling SE of the share's difference from the row-4 share; the fill-in's own error is not in it
    }
    const costsV = at(edited(by)).map((r) => r.cost_bn);
    const move = costsV.map((c, e) => c - costs[e]);
    move.forEach((m, e) => { if (Math.abs(m - by[allocOf[e]]) > 1e-9) fail(`${name} ${v} end ${e}: the move ${m} is not the edit ${by[allocOf[e]]}`); });
    const rec = (out.variants[v] = out.variants[v] || { share: {}, amount_bn: {}, edit_bn: {}, move_se_bn: {} });
    rec.share = Object.fromEntries(ALLOCS.map((a) => [a, v === "case_row4_share" ? SHARES.case_cps[a].share : SHARES[v === "admin_state_age_additive" ? "admin_state_age" : v][a].share]));
    rec.amount_bn[name] = amount; rec.edit_bn[name] = by; rec.move_se_bn = se;
    rec[name] = { low_bn: costsV[0], high_bn: costsV[1], move_low_bn: move[0], move_high_bn: move[1] };
    rows.push({ set: name, variant: v, share_shared: rec.share.shared, share_personal: rec.share.personal,
      amount_low_bn: amount[allocOf[0]], amount_high_bn: amount[allocOf[1]], cost_low_bn: costsV[0], cost_high_bn: costsV[1],
      move_low_bn: move[0], move_high_bn: move[1], move_se_low_bn: se[allocOf[0]], move_se_high_bn: se[allocOf[1]] });
  }
  rows.unshift({ set: name, variant: "oracle", share_shared: "", share_personal: "", amount_low_bn: caseAmount[allocOf[0]],
    amount_high_bn: caseAmount[allocOf[1]], cost_low_bn: costs[0], cost_high_bn: costs[1], move_low_bn: 0, move_high_bn: 0,
    move_se_low_bn: "", move_se_high_bn: "" });
}
out.gates.push("every move equals its edit at the specification's allocation (1e-9)");
const cols = Object.keys(rows[rows.length - 1]);
const fmt = (x) => (typeof x === "number" ? String(Number(x.toPrecision(12))) : x);
const order = (r) => (r.set === "set" ? 0 : 1);
const sorted = rows.slice().sort((a, b) => order(a) - order(b));
fs.writeFileSync(path.join(__dirname, "derived", "arm.csv"), [cols.join(",")].concat(sorted.map((r) => cols.map((c) => fmt(r[c])).join(","))).join("\n") + "\n");
fs.writeFileSync(path.join(__dirname, "derived", "arm.json"), JSON.stringify(out, null, 1) + "\n");
for (const g of out.gates) console.log("  ✓ " + g);
for (const r of sorted) console.log(`  ${r.set.padEnd(4)} ${r.variant.padEnd(26)} ${fmt(r.cost_low_bn).padEnd(14)} ${fmt(r.cost_high_bn).padEnd(14)} move ${Number(r.move_low_bn).toFixed(4)} / ${Number(r.move_high_bn).toFixed(4)}`);
