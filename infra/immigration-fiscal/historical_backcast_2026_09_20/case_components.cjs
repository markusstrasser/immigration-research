/* A main case's additions at each profile's band ends, for backcast.py, which carries each addition back with
 * its own national series.
 *
 * September 27 (main_case_long_run_2026_09_27) is the schools case plus long-run road and park responses, rental
 * assistance at 1, the enterprise surplus at 1 and the return on public capital. At every specification the case
 * is the schools case's cost there plus those additions exactly, so at each fill-in method's end specifications
 * this script writes the schools case's cost (the base) and each addition:
 *   - long_run_<line>: the added responsive spending of economic_affairs_services and recreation_culture;
 *   - rental_assistance: housing_subsidies;
 *   - enterprise_surplus: the receipt's cost at its response (the group's share of the enterprises' operating result);
 *   - capital_<component>: the return on each capital component, with its part (core, block, enterprise) and level.
 * Methods are averaged at their own end specifications, as the case lane does.
 *
 * Gates (exit 1, nothing written): the schools-case evaluation reproduces the schools lane's band; the case's band
 * per profile equals its main_case_bands.csv adopted row (1e-4); at each end specification base + additions equal
 * the case's cost (1e-9) and no other line moves; on the main profile the parts equal summary.json's
 * change_at_fixed_specifications and the components its capital_at_end_specifications (1e-9).
 *
 * Run from anywhere: node case_components.cjs [--case sept27] [--out-dir DIR] -> derived/case_components_<case>.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.resolve(__dirname, "..");
const CASES = { sept27: "main_case_long_run_2026_09_27" };
const argv = process.argv.slice(2);
const opt = (name, dflt) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : dflt);
const CASE = opt("--case", Object.keys(CASES).slice(-1)[0]);
if (!CASES[CASE]) throw new Error(`[BLOCKED] unknown case ${CASE}`);
const LANE = CASES[CASE];
const OUT = path.resolve(opt("--out-dir", path.join(__dirname, "derived")));

const P = require(path.join(FISCAL, LANE, "package.cjs"));
const S = P.PSCHOOLS;
const { Engine, METHODS } = P;
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const csv = (rel) => {
  const [head, ...rows] = fs.readFileSync(path.join(FISCAL, rel), "utf8").trim().split("\n").map((l) => l.split(","));
  return rows.map((r) => Object.fromEntries(head.map((h, i) => [h, r[i]])));
};
let failed = 0;
const gate = (name, ok, detail) => {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
  if (!ok) failed += 1;
};
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;

const summary = readJson(`${LANE}/derived/summary.json`);
const bands = csv(`${LANE}/derived/main_case_bands.csv`);
const schools = readJson("main_case_schools_full_2026_09_26/derived/summary.json");
const bandRow = (profile, variant) => {
  const r = bands.find((x) => x.profile === profile && x.variant === variant);
  if (!r) throw new Error(`[BLOCKED] ${LANE} main_case_bands.csv has no ${profile}/${variant} row`);
  return [Number(r.cost_low_bn), Number(r.cost_high_bn)];
};
// The back-cast's concepts and the case's profile for each; the base is that profile's schools-case profile.
const CONCEPTS = { net_cost_cbo_informed: P.MAIN_PROFILE, net_cost_full_proportional: "proportional_reference" };
const LINES = [...P.LR_LINES, P.RENTAL];
const RECEIPT = P.ENTERPRISE_LINE;

// The case's models (the enterprise receipt re-keyed) and the schools case's (model.json's receipt share).
const MODELS = METHODS.map((m) => P.modelFor("central", m, P.withCentral({})));
const SCHOOL_MODELS = METHODS.map((m) => P.modelFor("central", m, P.withCentral({ enterprise_rekey: false })));
const SPECS = P.MAIN_SPECS;
if (SPECS.length !== S.MAIN_SPECS.length) throw new Error("[BLOCKED] the case and the schools case differ in specifications");

console.log(`[${CASE}: ${LANE}]`);
{
  const costs = SCHOOL_MODELS.map((m) => S.MAIN_SPECS.map((s) => -Engine.evaluate(m, S.stateFor(m, s, S.MAIN_PROFILE)).welfare_bn));
  const band = [mean(costs.map((xs) => Math.min(...xs))), mean(costs.map((xs) => Math.max(...xs)))];
  gate("the schools-case evaluation reproduces the schools lane's band (1e-6)",
    near(band[0], schools.main_case[0], 1e-6) && near(band[1], schools.main_case[1], 1e-6), band.map((x) => x.toFixed(4)).join("/"));
}

const out = { case: CASE, lane: LANE, rule: "each fill-in method's end specifications of the case, averaged; base = the schools case's cost at those specifications",
  inputs: Object.fromEntries([`${LANE}/derived/summary.json`, `${LANE}/derived/main_case_bands.csv`, `${LANE}/derived/corrections.json`,
    `${LANE}/package.cjs`].map((rel) => [rel, sha256(rel)])),
  concepts: {} };
for (const [concept, profile] of Object.entries(CONCEPTS)) {
  const base = P.ALL_PROFILES[profile].base;
  const runs = MODELS.map((m) => SPECS.map((s) => P.evaluateFull(m, s, profile)));
  const costs = runs.map((xs) => xs.map((r) => r.cost_bn));
  const ends = costs.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
  const band = [mean(costs.map((xs) => Math.min(...xs))), mean(costs.map((xs) => Math.max(...xs)))];
  const adopted = bandRow(profile, "adopted");
  gate(`${concept} (${profile}): the band is main_case_bands.csv's adopted row (1e-4)`,
    near(band[0], adopted[0], 1e-4) && near(band[1], adopted[1], 1e-4), `${band.map((x) => x.toFixed(4)).join("/")}; ends ${JSON.stringify(ends)}`);
  // The parts at one method's end specification.
  const partsAt = (m, i) => {
    const r = runs[m][i];
    const e0 = Engine.evaluate(SCHOOL_MODELS[m], S.stateFor(SCHOOL_MODELS[m], S.MAIN_SPECS[i], base));
    const row = (ev, side, id) => ev[side].find((x) => x.id === id);
    const moved = (side) => r.evaluation[side].filter((x) => {
      const y = row(e0, side, x.id);
      return !y || x.effect_bn !== y.effect_bn;
    }).map((x) => x.id).filter((id) => (side === "spending" ? !LINES.includes(id) : id !== RECEIPT));
    const parts = {};
    for (const id of LINES) {
      const a = row(r.evaluation, "spending", id), b = row(e0, "spending", id);
      parts[id === P.RENTAL ? "rental_assistance" : `long_run_${id}`] = a.response * a.amount_bn - b.response * b.amount_bn;
    }
    parts.enterprise_surplus = -(row(r.evaluation, "receipts", RECEIPT).effect_bn - row(e0, "receipts", RECEIPT).effect_bn);
    const capital = Object.fromEntries(r.capital.components.map((c) => [c.id, c.return_bn]));
    const baseCost = -e0.welfare_bn;
    const total = baseCost + Object.values(parts).reduce((a, b) => a + b, 0) + r.capital.total_bn;
    return { base: baseCost, cost: r.cost_bn, parts, capital, check: total - r.cost_bn,
      moved: [...moved("spending"), ...moved("receipts")],
      components: r.capital.components.map((c) => ({ id: c.id, part: c.group, level: c.level })) };
  };
  const at = ends.map((ij, m) => ij.map((i) => partsAt(m, i)));
  gate(`${concept}: at every end specification base + additions = the case's cost (1e-9) and no other line moves`,
    at.flat().every((x) => Math.abs(x.check) < 1e-9 && x.moved.length === 0),
    `max |diff| ${Math.max(...at.flat().map((x) => Math.abs(x.check))).toExponential(1)}; other lines moved: ${[...new Set(at.flat().flatMap((x) => x.moved))].join(" ") || "none"}`);
  const avg = (e, f) => mean(at.map((pair) => f(pair[e])));
  const ids = at[0][0].components.map((c) => c.id);
  const partIds = Object.keys(at[0][0].parts);
  out.concepts[concept] = { profile, base_profile: base, end_specifications: ends.map((ij, m) => ({ method: METHODS[m], low: ij[0], high: ij[1] })),
    ends: Object.fromEntries(["low", "high"].map((end, e) => [end, {
      cost_bn: avg(e, (x) => x.cost), base_bn: avg(e, (x) => x.base),
      additions_bn: Object.fromEntries(partIds.map((k) => [k, avg(e, (x) => x.parts[k])])),
      capital_bn: Object.fromEntries(ids.map((k) => [k, avg(e, (x) => x.capital[k])])),
    }])),
    components: at[0][0].components };
  if (profile === P.MAIN_PROFILE) {
    const c = summary.change_at_fixed_specifications, cap = summary.capital_at_end_specifications.by_component;
    const E = out.concepts[concept].ends;
    const sumOf = (e, part) => Object.entries(E[e].capital_bn)
      .filter(([id]) => at[0][0].components.find((x) => x.id === id).part === part).reduce((a, [, v]) => a + v, 0);
    const pairs = [["long_run_responses", (e) => E[e].additions_bn.long_run_economic_affairs_services + E[e].additions_bn.long_run_recreation_culture],
      ["rental_assistance", (e) => E[e].additions_bn.rental_assistance], ["enterprise_surplus_receipt", (e) => E[e].additions_bn.enterprise_surplus],
      ["capital_core", (e) => sumOf(e, "core")], ["capital_block", (e) => sumOf(e, "block")], ["capital_enterprise", (e) => sumOf(e, "enterprise")]];
    const worst = Math.max(...pairs.flatMap(([k, f]) => ["low", "high"].map((e, j) => Math.abs(f(e) - c[k][j]))));
    gate(`${concept}: the parts equal summary.json change_at_fixed_specifications (1e-9)`, worst < 1e-9, `max |diff| ${worst.toExponential(1)}`);
    const worstC = Math.max(...ids.flatMap((id) => ["low", "high"].map((e, j) => Math.abs(E[e].capital_bn[id] - cap[id].return_bn[j]))));
    gate(`${concept}: each capital component equals summary.json capital_at_end_specifications (1e-9)`, worstC < 1e-9,
      `${ids.length} components, max |diff| ${worstC.toExponential(1)}`);
  }
  const E = out.concepts[concept].ends;
  const baseGap = Math.max(...["low", "high"].map((e, j) => Math.abs(E[e].base_bn - bandRow(profile, "schools_case")[j])));
  gate(`${concept}: the base is the profile's schools_case band, so the ends do not move (1e-4, the file's rounding)`, baseGap < 1e-4,
    `max |diff| ${baseGap.toExponential(1)}`);
}
if (failed) {
  console.error(`${failed} gate(s) failed; nothing written`);
  process.exit(1);
}
fs.mkdirSync(OUT, { recursive: true });
const file = path.join(OUT, `case_components_${CASE}.json`);
fs.writeFileSync(file, JSON.stringify(out, null, 1) + "\n");
console.log(`-> ${path.relative(process.cwd(), file)}`);
