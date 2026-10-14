/* The case's own keys for the job-capital taxes lane: the wage key the receipt lane priced its ceiling with, the
 * floor it named, and the adopted case's lines, read from the packages unchanged.
 *
 *   sept27   main_case_long_run_2026_09_27/package.cjs, the case the receipt-side lane (receipt_side_long_run_2026_09_28)
 *            probed: the employer_hi share at specifications 48 and 11 (both fill-in methods averaged, as probe.cjs's
 *            lineAt), the three lines' national totals (business property net of the tenant split, which the
 *            receipt lane takes from housing.json's BEA split) and corporate_labor's group amount (the CBO 25% labor
 *            share at the wage key: the floor).
 *   v6       main_case_2026_10_07/package.cjs, the adopted case: the same lines' nationals, keys and responses at
 *            specifications 48, 11 and 16.
 *   case_wage_key  the union's and each generation's share of the case's wage key (corporate_labor at the reference
 *            incidence rule on the September 29 payload model, set and cash), the base main_case_2026_10_14 scales
 *            this lane's item by (item_job_capital.cjs); stored unrounded.
 *   case_housing_key  the same shares of the case's owner and tenant property lines (modeled_owner_property,
 *            tenant_occupied_property) and v6's responses for them: job_capital.py prices the residential parts of
 *            documentary taxes and special assessments, which the item leaves out, beside at these keys.
 *
 * Gates (exit 1, nothing written): the ceiling is the receipt lane's probe.json item 4 (-share x the three lines'
 * total, 1e-6 bn) and its wage shares (rounded to 6 places); corporate_labor at 48 / 11 is trace.csv's (4 places);
 * the three lines' nationals are model.json's (1e-9 bn) in both packages; in v6 each line has one key and response
 * 0 at every specification read (the zero this lane prices); corporate_labor is keyed by wage at the reference rule,
 * the generations' wage-key shares add to the union's (1e-12) and the set and cash set give the same shares (1e-12).
 *
 *   node infra/immigration-fiscal/job_capital_taxes_2026_10_14/case_keys.cjs [--out-dir DIR] -> derived/case_keys.json
 */
"use strict";
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const HERE = __dirname;
const FISCAL = path.resolve(HERE, "..");
const RECEIPT = path.join(FISCAL, "receipt_side_long_run_2026_09_28");
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));

const gates = [];
function gate(name, ok, detail = "") {
  gates.push({ gate: name, passed: Boolean(ok), detail: String(detail) });
  console.log(`  ${ok ? "✓" : "✗"} ${name}${detail ? ` (${detail})` : ""}`);
}
const near = (a, b, tol) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= tol;
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const r9 = (x) => Math.round(x * 1e9) / 1e9;

const K = require(path.join(FISCAL, "main_case_long_run_2026_09_27", "package.cjs"));
const P = require(path.join(FISCAL, "main_case_2026_10_07", "package.cjs"));
const MODEL = JSON.parse(fs.readFileSync(path.join(FISCAL, "assumption_explorer_2026_09_21", "derived", "model.json"), "utf8"));
const H = JSON.parse(fs.readFileSync(path.join(RECEIPT, "derived", "housing.json"), "utf8"));
const PROBE = JSON.parse(fs.readFileSync(path.join(RECEIPT, "derived", "probe.json"), "utf8"));
const TRACE = fs.readFileSync(path.join(RECEIPT, "derived", "trace.csv"), "utf8").trim().split("\n");

const nat = (id) => MODEL.receipts.lines.find((l) => l.id === id).national_bn;
const TENANT = H.bea_housing.tenant_taxes_bn;
const NATIONAL = {
  c_and_i_property: nat("remaining_production_property") - TENANT,
  other_production_taxes: nat("other_production_taxes"),
  corporate: nat("corporate_capital") + nat("corporate_labor"),
};
const TOTAL = Object.values(NATIONAL).reduce((a, b) => a + b, 0);
const LINE_IDS = ["employer_hi", "corporate_labor", "corporate_capital", "remaining_production_property",
  "tenant_occupied_property", "other_production_taxes"];

// One package at a set of specifications: each line's amount, national, key and response per method, then the
// methods' mean (the case's ends average the two fill-in methods).
function read(pkg, specs) {
  const models = pkg.METHODS.map((meth) => pkg.modelFor("central", meth, pkg.withCentral({})));
  const out = {};
  for (const i of specs) {
    const runs = models.map((m) => pkg.evaluateFull(m, pkg.MAIN_SPECS[i], pkg.MAIN_PROFILE));
    const lines = {};
    for (const id of LINE_IDS) {
      const rows = runs.map((r) => r.evaluation.receipts.find((l) => l.id === id));
      if (rows.some((x) => !x)) continue;
      lines[id] = {
        national_bn: rows[0].national_bn, key: rows[0].key,
        response_by_method: rows.map((x) => x.response),
        amount_bn_by_method: rows.map((x) => x.amount_bn),
        share_by_method: rows.map((x) => x.amount_bn / x.national_bn),
        amount_bn: mean(rows.map((x) => x.amount_bn)), share: mean(rows.map((x) => x.amount_bn / x.national_bn)),
      };
    }
    out[i] = { allocation: pkg.MAIN_SPECS[i].allocation, methods: pkg.METHODS, lines };
  }
  return out;
}

console.log("[sept27: the receipt lane's ceiling and floor]");
const s27 = read(K, [48, 11]);
const share27 = [48, 11].map((i) => s27[i].lines.employer_hi.share);
const ceiling = share27.map((w) => -w * TOTAL);
const item4 = PROBE.item4;
gate("the three lines' national total is probe.json's business taxes (1e-6 bn)",
  near(TOTAL, Object.values(item4.business_taxes_bn).reduce((a, b) => a + b, 0), 1e-6), TOTAL.toFixed(6));
gate("employer_hi shares at 48 / 11 round to probe.json's wage_share", share27.every((w, e) => near(w, item4.wage_share[e], 5e-7)),
  share27.map((w) => w.toFixed(9)).join(" / "));
gate("the plain-wage-share ceiling reproduces probe.json's use_key_at_1_bn (1e-6 bn)",
  ceiling.every((c, e) => near(c, item4.use_key_at_1_bn[e], 1e-6)), ceiling.map((c) => c.toFixed(6)).join(" / "));
const head = TRACE[0].split(",");
const traceRow = TRACE.find((l) => l.startsWith("corporate_labor,")).split(",");
const traceAt = (col) => +traceRow[head.indexOf(col)];
const floor = [48, 11].map((i) => s27[i].lines.corporate_labor.amount_bn);
gate("corporate_labor at 48 / 11 is trace.csv's floor (4 places)", near(floor[0], traceAt("group_48_bn"), 5e-5)
  && near(floor[1], traceAt("group_11_bn"), 5e-5), floor.map((x) => x.toFixed(4)).join(" / "));
gate("Sept 27 nationals are model.json's (1e-9 bn)", LINE_IDS.filter((id) => s27[48].lines[id]).every((id) =>
  near(s27[48].lines[id].national_bn, nat(id), 1e-9)));

console.log("\n[v6: the adopted case's lines]");
const v6 = read(P, [48, 11, 16]);
const v6l = v6[48].lines;
gate("v6 carries the tenant split: business property's national is model.json's less the BEA tenant tax (1e-9 bn)",
  near(v6l.remaining_production_property.national_bn, NATIONAL.c_and_i_property, 1e-9)
  && near(v6l.tenant_occupied_property.national_bn, TENANT, 1e-9), v6l.remaining_production_property.national_bn.toFixed(6));
gate("v6 other production and corporate nationals are model.json's (1e-9 bn)",
  near(v6l.other_production_taxes.national_bn, NATIONAL.other_production_taxes, 1e-9)
  && near(v6l.corporate_capital.national_bn + v6l.corporate_labor.national_bn, NATIONAL.corporate, 1e-9));
const zeroLines = ["remaining_production_property", "other_production_taxes", "corporate_capital", "corporate_labor"];
gate("v6: the three lines respond 0 at 48, 11 and 16, both methods (the zero this lane prices)",
  [48, 11, 16].every((i) => zeroLines.every((id) => v6[i].lines[id].response_by_method.every((r) => r === 0))));
gate("v6: specification 48 is the shared allocation, 11 and 16 personal",
  v6[48].allocation === "shared" && v6[11].allocation === "personal" && v6[16].allocation === "personal");

console.log("\n[the case's wage key on the September 29 payload: the base the v7 item scales]");
// main_case_2026_10_14 (item_job_capital.cjs) reads the lane's plain wage share as the union's share of the case's wage
// key: corporate_labor at the reference incidence rule on the September 29 payload model, set and cash, and the
// generations' shares from generation_account_2026_09_24's September 29 models (convention a). The case's key carries
// the September 24 stack (row 4, a fill-in method, the status rules at the on-books lane's shares), which this lane's
// own plain share (all CPS wages) does not.
const REF = P.MODEL.receipts.reference;
const GEN = path.join(FISCAL, "generation_account_2026_09_24", "derived");
const GENS = ["G1", "G2", "G3plus"];
const cellOf = (m, id) => m.receipts.lines.find((l) => l.id === id).cells[REF];
const totalOf = (c, a) => c[a].target_bn + c[a].other_bn;
const caseWage = {};
const HOUSING_LINES = ["modeled_owner_property", "tenant_occupied_property"];
const caseHousing = {};
for (const [which, api, file] of [["set", P.SEPT29, "generation_corrections_sept29.json"], ["cash", P.SEPT29_CASH, "generation_corrections_sept29_cash.json"]]) {
  const U = api.payloadModel();
  const GP = JSON.parse(fs.readFileSync(path.join(GEN, file), "utf8"));
  const GM = Object.fromEntries(GENS.map((g) => [g, P.Engine.applyCorrections(JSON.parse(fs.readFileSync(path.join(GEN, `model_${g}.json`), "utf8")), GP.payloads.a[g])]));
  const u = cellOf(U, "corporate_labor");
  const share = (m) => Object.fromEntries(["personal", "shared"].map((a) => [a, cellOf(m, "corporate_labor")[a].target_bn / totalOf(u, a)]));
  caseWage[which] = { union: share(U), ...Object.fromEntries(GENS.map((g) => [g, share(GM[g])])),
    key: { personal: u.personal.key, shared: u.shared.key }, national_bn: totalOf(u, "personal") };
  const add = Math.max(...["personal", "shared"].map((a) => Math.abs(GENS.reduce((t, g) => t + caseWage[which][g][a], 0) - caseWage[which].union[a])));
  gate(`${which}: corporate_labor at ${REF} is keyed by wage, and the generations' shares add to the union's (1e-12)`,
    u.personal.key === "wage" && u.shared.key === "wage" && add < 1e-12, `union ${caseWage[which].union.personal.toFixed(9)} / ${caseWage[which].union.shared.toFixed(9)}`);
  caseHousing[which] = Object.fromEntries(HOUSING_LINES.map((id) => {
    const uc = cellOf(U, id);
    const sh = (m) => Object.fromEntries(["personal", "shared"].map((a) => [a, cellOf(m, id)[a].target_bn / totalOf(uc, a)]));
    return [id, { union: sh(U), ...Object.fromEntries(GENS.map((g) => [g, sh(GM[g])])), key: { personal: uc.personal.key, shared: uc.shared.key },
      national_bn: totalOf(uc, "personal") }];
  }));
  const addH = Math.max(...HOUSING_LINES.flatMap((id) => ["personal", "shared"].map((a) =>
    Math.abs(GENS.reduce((t, g) => t + caseHousing[which][id][g][a], 0) - caseHousing[which][id].union[a]))));
  gate(`${which}: the owner and tenant property lines' generation shares add to the union's (1e-12)`, addH < 1e-12,
    HOUSING_LINES.map((id) => `${id} ${caseHousing[which][id].union.personal.toFixed(6)}`).join(", "));
}
gate("the case's wage-key shares are the same in the set and the cash set (1e-12)", ["union", ...GENS].every((g) =>
  ["personal", "shared"].every((a) => Math.abs(caseWage.set[g][a] - caseWage.cash[g][a]) < 1e-12)));
gate("the case's owner and tenant property shares are the same in the set and the cash set (1e-12)", HOUSING_LINES.every((id) =>
  ["union", ...GENS].every((g) => ["personal", "shared"].every((a) => Math.abs(caseHousing.set[id][g][a] - caseHousing.cash[id][g][a]) < 1e-12))));
const V6C_FILE = path.join(FISCAL, "main_case_2026_10_07", "derived", "corrections.json");
const V6C = JSON.parse(fs.readFileSync(V6C_FILE, "utf8"));
const housingResp = Object.fromEntries(HOUSING_LINES.map((id) => [id, { low: V6C.meta.responses[id].low, high: V6C.meta.responses[id].high }]));
gate("v6 sets a response for the owner and tenant property lines at both ends", HOUSING_LINES.every((id) =>
  Number.isFinite(housingResp[id].low) && Number.isFinite(housingResp[id].high)), JSON.stringify(housingResp));
const baseWage = Object.fromEntries(["personal", "shared"].map((a) => [a, cellOf(P.MODEL, "corporate_labor")[a].target_bn / totalOf(cellOf(P.MODEL, "corporate_labor"), a)]));

const failed = gates.filter((g) => !g.passed);
if (failed.length) {
  console.log(`\n[BLOCKED] ${failed.length} gate(s) failed; nothing written`);
  process.exit(1);
}
const round = (o) => JSON.parse(JSON.stringify(o, (k, v) => (typeof v === "number" ? r9(v) : v)));
const out = {
  meta: {
    sept27_package: "infra/immigration-fiscal/main_case_long_run_2026_09_27/package.cjs",
    v6_package: "infra/immigration-fiscal/main_case_2026_10_07/package.cjs",
    model: "infra/immigration-fiscal/assumption_explorer_2026_09_21/derived/model.json",
    model_sha256: crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, "assumption_explorer_2026_09_21", "derived", "model.json"))).digest("hex"),
    rule: "each end averages the two fill-in methods (probe.cjs lineAt); share = amount_bn / national_bn",
    tenant_split: "business property = remaining_production_property less the BEA tenant tax (receipt lane housing.json bea_housing.tenant_taxes_bn)",
  },
  national_bn: { ...NATIONAL, tenant_occupied_property: TENANT, total: TOTAL },
  sept27: {
    specs: s27,
    ceiling_bn: { spec48: ceiling[0], spec11: ceiling[1] },
    floor_corporate_labor_bn: { spec48: -floor[0], spec11: -floor[1] },
    employer_hi_share: { spec48: share27[0], spec11: share27[1] },
  },
  v6: { specs: v6 },
  case_wage_key: {
    rule: `the union's and each generation's share of corporate_labor's wage key at ${REF} on the September 29 payload model `
      + "(main_case_2026_10_07/package.cjs SEPT29; generations from generation_account_2026_09_24 model_<G>.json with "
      + "generation_corrections_sept29.json payloads.a): target over the line's national",
    reference: REF, line: "corporate_labor", key: caseWage.set.key, national_bn: caseWage.set.national_bn,
    shares: Object.fromEntries(["union", ...GENS].map((g) => [g, caseWage.set[g]])),
    base_model_union: baseWage,
  },
  case_housing_key: {
    rule: `the union's and each generation's share of the case's owner and tenant property lines at ${REF} on the September 29 payload model `
      + "(as case_wage_key), and v6's responses for them (main_case_2026_10_07/derived/corrections.json meta.responses)",
    reference: REF,
    corrections_sha256: crypto.createHash("sha256").update(fs.readFileSync(V6C_FILE)).digest("hex"),
    responses: housingResp,
    lines: Object.fromEntries(HOUSING_LINES.map((id) => [id, { key: caseHousing.set[id].key, national_bn: caseHousing.set[id].national_bn,
      shares: Object.fromEntries(["union", ...GENS].map((g) => [g, caseHousing.set[id][g]])) }])),
  },
  gates,
};
fs.mkdirSync(OUT, { recursive: true });
// Every number at 9 places, the case's wage-key shares aside: the v7 item compares them with the case at 1e-9.
const rounded = round(out);
rounded.case_wage_key = JSON.parse(JSON.stringify(out.case_wage_key));
fs.writeFileSync(path.join(OUT, "case_keys.json"), JSON.stringify(rounded, null, 1) + "\n");
console.log(`\nwrote ${path.join(OUT, "case_keys.json")}`);
