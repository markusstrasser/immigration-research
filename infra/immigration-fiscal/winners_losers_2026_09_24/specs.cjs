/* The adopted main case, specification by specification, split into the engine's three terms.
 *
 * For each of the 64 main-case specifications (main_case_2026_09_24/package.cjs MAIN_SPECS) this
 * evaluates the explorer engine once on the September 23 model and once on the September 24 model
 * (the September 23 model plus derived/corrections.json, the adopted package as cell edits), and
 * writes the direct fiscal response A, the private production term P and the induced receipts F.
 * welfare = P + A + F, and the cost to other residents is -welfare. winners_losers.py puts A + F in
 * the fiscal channel and P in the wage channel.
 *
 * package.cjs is not imported: loading it rewrites main_case_2026_09_24/derived/stack_line_deltas.json
 * whenever the CPS lane's cache is present, and this lane writes only inside its own directory. The
 * spec grid and cost() below copy package.cjs (MAIN_SPECS, PROFILES, cost) for the main profile;
 * the band gates prove the copy against main_case_bands.csv.
 *
 * At the two band ends (the lowest- and highest-cost specifications) it also writes each account
 * line's responsive effect, for the federal/state-local split in winners_losers.py.
 *
 * Gates (exit 1 on failure): both bands reproduce main_case_bands.csv to 1e-4; welfare = P + A + F
 * in every specification; P + F depends on the normalization only.
 * Run: node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const MODEL = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const scaling = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "scaling_check.json"), "utf8"));
const PAYLOAD = JSON.parse(fs.readFileSync(path.join(FISCAL, "main_case_2026_09_24", "derived", "corrections.json"), "utf8"));

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
function product(dims) {
  return Object.entries(dims).reduce(
    (acc, [name, levels]) => acc.flatMap((spec) => levels.map((v) => ({ ...spec, [name]: v }))), [{}]);
}
function csvRows(file) {
  const [head, ...rows] = fs.readFileSync(file, "utf8").trim().split("\n");
  const keys = head.split(",");
  return rows.map((r) => Object.fromEntries(r.split(",").map((c, i) => [keys[i], c])));
}

// ---- copied from main_case_2026_09_24/package.cjs (main profile only)
const SHARES = Engine.schoolShareBounds(MODEL);
const GG = [scaling.composite_low, scaling.composite_high];
const MAIN_SPECS = product({
  allocation: ["personal", "shared"], normalization: ["cash", "gdp"], share: SHARES,
  school: [0.63, 0.66], gg: GG, uc: ["uninsured_use_low", "uninsured_use_high"], justice: ["use"],
});
const SYN = { school: "school_reprice", college: "college_rekey", constants: "lane_constants" };
const PROFILE = { other: 1, delayed: 0 };   // cbo_category_lag_non_school_full
function evaluate(m, spec) {
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = m.receipts.reference;
  s.production.normalization = spec.normalization;
  s.count_production = true;
  s.general_government_response = spec.gg;
  s.key_override = { public_order_safety: spec.justice, medicaid_and_chip_other_medical: spec.uc };
  s.response_override = {
    education_services: spec.share * spec.school + (1 - spec.share) * PROFILE.other,
    public_order_safety: 1, health_services: 1, income_security_services: 1,
    housing_community_services: 1, economic_affairs_services: PROFILE.delayed, recreation_culture: PROFILE.delayed,
    [SYN.school]: spec.share * spec.school, [SYN.college]: (1 - spec.share) * PROFILE.other, [SYN.constants]: 1,
  };
  return Engine.evaluate(m, s);
}

// ---- the two models: September 23 (no corrections) and September 24 (the adopted payload)
const MODELS = {
  adopted_2026_09_23: MODEL,
  adopted_2026_09_24: Engine.applyCorrections(MODEL, PAYLOAD),
};
const published = {};
for (const r of csvRows(path.join(FISCAL, "main_case_2026_09_24", "derived", "main_case_bands.csv"))) {
  if (r.profile === "cbo_category_lag_non_school_full") published[r.variant] = [Number(r.cost_low_bn), Number(r.cost_high_bn)];
}
const WANT = { adopted_2026_09_23: published.adopted_2026_09_23, adopted_2026_09_24: published.adopted };

const rows = [];
const lineRows = [];
console.log("[specifications]");
for (const [caseName, m] of Object.entries(MODELS)) {
  const results = MAIN_SPECS.map((spec) => ({ spec, r: evaluate(m, spec) }));
  const costs = results.map((x) => -x.r.welfare_bn);
  const lo = Math.min(...costs), hi = Math.max(...costs);
  gate(`${caseName}: band reproduces main_case_bands.csv`,
    Math.abs(lo - WANT[caseName][0]) < 1e-4 && Math.abs(hi - WANT[caseName][1]) < 1e-4,
    `${lo.toFixed(4)}–${hi.toFixed(4)} vs ${WANT[caseName][0]}–${WANT[caseName][1]}`);
  let maxId = 0;
  const pf = {};
  results.forEach(({ spec, r }, i) => {
    maxId = Math.max(maxId, Math.abs(r.welfare_bn - (r.private_wtp_bn + r.direct_fiscal_response_bn + r.induced_receipts_bn)));
    const key = spec.normalization;
    pf[key] = pf[key] || new Set();
    pf[key].add((r.private_wtp_bn + r.induced_receipts_bn).toFixed(9));
    rows.push({
      case: caseName, spec_id: i, ...spec, cost_bn: -r.welfare_bn, welfare_bn: r.welfare_bn,
      A_bn: r.direct_fiscal_response_bn, P_bn: r.private_wtp_bn, F_bn: r.induced_receipts_bn,
      band_end: costs[i] === lo ? "low" : costs[i] === hi ? "high" : "",
    });
  });
  gate(`${caseName}: welfare = P + A + F in all 64 specifications`, maxId < 1e-9, `max |gap| ${maxId.toExponential(2)}`);
  gate(`${caseName}: P + F depends on the normalization only`, Object.values(pf).every((s) => s.size === 1),
    Object.entries(pf).map(([k, s]) => `${k} ${[...s].join("/")}`).join("; "));
  // Line effects at the two band ends.
  for (const [end, target] of [["low", lo], ["high", hi]]) {
    const hit = results.find((x) => -x.r.welfare_bn === target);
    for (const l of hit.r.receipts) {
      lineRows.push({ case: caseName, end, side: "receipt", line: l.id, amount_bn: l.amount_bn, response: l.response, effect_bn: l.effect_bn });
    }
    for (const l of hit.r.spending) {
      lineRows.push({ case: caseName, end, side: "spending", line: l.id, amount_bn: l.amount_bn, response: l.response, effect_bn: l.effect_bn });
    }
    const sum = lineRows.filter((x) => x.case === caseName && x.end === end).reduce((s, x) => s + x.effect_bn, 0);
    gate(`${caseName} ${end}: line effects add to A`, Math.abs(sum - hit.r.direct_fiscal_response_bn) < 1e-8,
      `${sum.toFixed(6)} vs ${hit.r.direct_fiscal_response_bn.toFixed(6)}`);
  }
}

function writeCsv(file, list) {
  const keys = Object.keys(list[0]);
  const fmt = (v) => (typeof v === "number" ? (Number.isInteger(v) ? String(v) : v.toPrecision(15)) : String(v));
  fs.writeFileSync(file, [keys.join(",")].concat(list.map((r) => keys.map((k) => fmt(r[k])).join(","))).join("\n") + "\n");
}
if (failures) {
  console.log(`[BLOCKED] ${failures} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
writeCsv(path.join(HERE, "derived", "fiscal_specs.csv"), rows);
writeCsv(path.join(HERE, "derived", "fiscal_lines_band_ends.csv"), lineRows);
console.log(`wrote derived/fiscal_specs.csv (${rows.length} rows) and derived/fiscal_lines_band_ends.csv (${lineRows.length} rows)`);
