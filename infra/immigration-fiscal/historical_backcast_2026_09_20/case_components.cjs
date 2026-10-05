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
 * September 29 (SEPT29_LANE, candidate v4 adopted) is September 27 plus its own change. At the case's end
 * specifications the file keeps the schools-case base and September 27's four additions (from September 27's
 * package at the same specifications), takes the capital return at the case's values, and adds the change from
 * September 27 line by line: v4_<line> = -(the line's effect less September 27's), for every receipt and spending line
 * that moves. Three lines are split so that each part has one national series in backcast.py:
 *   - social_security: v4_social_security_accrual (the accrual the pension switch charges, ratio_net x the group's
 *     OASDI receipts) and v4_social_security_cash (the rest: the benefits it no longer charges);
 *   - medicare: v4_medicare_part_a_accrual (part_a_accrual_bn at the line's response) and v4_medicare_cash (the rest:
 *     the Part A benefits it no longer charges);
 *   - the production grid: v4_production_private (-dP) and v4_production_receipts (-dF).
 * v4_parts records each part's side, line, national total and parent line (synthetic lines), which backcast.py maps
 * to a series.
 *
 * Gates (exit 1, nothing written): the schools-case evaluation reproduces the schools lane's band; the case's band
 * per profile equals its main_case_bands.csv adopted row (1e-4); at each end specification base + additions equal
 * the case's cost (1e-9) and no other line moves; on the main profile the parts equal summary.json's
 * change_at_fixed_specifications and the components its capital_at_end_specifications (1e-9). September 29 adds:
 * September 27's specifications are the case's (every field but line_responses); at each end specification the
 * schools-case base and September 27's additions and capital equal September 27's cost (1e-9); social security's
 * amount is ratio_net x the group's OASDI receipts and Medicare's the Part A swap (1e-9); the enterprise surplus moves
 * only by its national total (the public-housing deficit moved to its own line); on the main profile September 27's
 * parts equal change_at_fixed_specifications.sept27_case and the change from September 27 its total (1e-9).
 *
 * October 5 (OCT05_LANE, main case v5 adopted) is September 29 plus the lineage: the descendants of Mexican immigrants who
 * no longer report Mexican origin (3.04M added people, counted whole). At the case's end specifications the file keeps
 * every September 29 part (the schools-case base, September 27's four additions and the v4 change from September 27,
 * from September 29's package at the same specifications, as --case sept29 computes them), takes the capital return at
 * September 29's values (capital_bn) and records the lineage's change in it apart (v5_capital_bn), and adds the lineage
 * line line by line: v5_<line> = -(the line's effect less September 29's). The lineage's pension lines are split so that
 * each part has one national series and the set less the cash set stays separable, as debt_legacy.py needs it:
 *   - social_security: v5_social_security_accrual (the line's change in the set, the added people's accrual),
 *     v5_social_security_benefits (their benefits, the cash set's change) and v5_social_security_cash (minus those
 *     benefits, which the set does not charge);
 *   - medicare: v5_medicare_part_a_accrual (the set's change less the share of the cash set's change the set still
 *     charges, 1 - part_a_share), v5_medicare_benefits (the cash set's change) and v5_medicare_cash (minus part_a_share
 *     of it);
 *   - the production grid: v5_production_private (-dP) and v5_production_receipts (-dF).
 * The cash set's change comes from the case's cash package (CASH) less September 29's (SEPT29_CASH) at the same
 * specification. v5_parts records each part's side, line, national total, parent line and rule; school_reprice and
 * college_rekey carry with education services and lane_constants per person (rule per_person). backcast.py carries the
 * lineage's parts and capital change at the identified third-plus generation's path (inputs/cps_g3plus_path.csv).
 * October 5's gates: September 29's specifications are the case's but for the group-size responses (gg, line_responses);
 * the cash package's specifications are the set's; the pension accrual's parameters are September 29's; at each end
 * specification the September 29 parts and capital equal September 29's cost (1e-9); where the case's end
 * specifications are September 29's, they average to September 29's band (main_case_bands.csv sept29_case for the main
 * profile, the September 29 lane's adopted row otherwise; 1e-4); on the main profile the September 27 parts equal
 * change_at_fixed_specifications.sept29_case.sept27_case, the v4 parts and September 29's capital change equal its
 * total, the lineage's parts and capital change equal change_at_fixed_specifications.total, and the capital return
 * with the lineage's change equals capital_at_end_specifications (1e-9).
 *
 * Run from anywhere: node case_components.cjs [--case sept27|sept29|oct05] [--out-dir DIR]
 * -> derived/case_components_<case>.json (the default case is sept27, whose file backcast.py's default run reads).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.resolve(__dirname, "..");
const SEPT29_LANE = "main_case_2026_09_29";
const OCT05_LANE = "main_case_2026_10_05";
const CASES = { sept27: "main_case_long_run_2026_09_27", sept29: SEPT29_LANE, oct05: OCT05_LANE };
const DEFAULT_CASE = "sept27";
const argv = process.argv.slice(2);
const opt = (name, dflt) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : dflt);
const CASE = opt("--case", DEFAULT_CASE);
if (!CASES[CASE]) throw new Error(`[BLOCKED] unknown case ${CASE}`);
const LANE = CASES[CASE];
const OUT = path.resolve(opt("--out-dir", path.join(__dirname, "derived")));

const P = require(path.join(FISCAL, LANE, "package.cjs"));
// September 29 takes the schools case and September 27's additions from September 27's package; October 5 takes every
// September 29 part from September 29's package (P29, its SEPT29) and adds the lineage's change.
const V5 = CASE === "oct05";
const V4 = CASE === "sept29" || V5;
const P29 = V5 ? P.SEPT29 : P;
const P27 = V4 ? require(path.join(FISCAL, CASES.sept27, "package.cjs")) : P;
if (V4 && (P29.SEPT27 !== P27 || JSON.stringify(P29.METHODS) !== JSON.stringify(P27.METHODS))) {
  throw new Error("[BLOCKED] the case's package does not build on September 27's package and methods");
}
if (V5 && (P29 !== require(path.join(FISCAL, SEPT29_LANE, "package.cjs")) || JSON.stringify(P.METHODS) !== JSON.stringify(P29.METHODS))) {
  throw new Error("[BLOCKED] the case's package does not build on September 29's package and methods");
}
const S = P27.PSCHOOLS;
const { Engine, METHODS } = P27;
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
const LINES = [...P27.LR_LINES, P27.RENTAL];
const RECEIPT = P27.ENTERPRISE_LINE;

// The case's models (the enterprise receipt re-keyed) and the schools case's (model.json's receipt share); September
// 29 also needs September 27's.
const MODELS = METHODS.map((m) => P.modelFor("central", m, P.withCentral({})));
const SCHOOL_MODELS = METHODS.map((m) => P27.modelFor("central", m, P27.withCentral({ enterprise_rekey: false })));
const MODELS27 = V4 ? METHODS.map((m) => P27.modelFor("central", m, P27.withCentral({}))) : MODELS;
const SPECS = P.MAIN_SPECS;
if (SPECS.length !== S.MAIN_SPECS.length) throw new Error("[BLOCKED] the case and the schools case differ in specifications");
const SPECS27 = P27.MAIN_SPECS;
// October 5 also needs September 29's models, and both cases' cash packages for the lineage's pension lines.
const MODELS29 = V5 ? METHODS.map((m) => P29.modelFor("central", m, P29.withCentral({}))) : MODELS;
const SPECS29 = P29.MAIN_SPECS;
const C5 = V5 ? P.CASH : null, C29 = V5 ? P.SEPT29_CASH : null;
const CASH_MODELS = V5 ? METHODS.map((m) => C5.modelFor("central", m, C5.withCentral({}))) : null;
const CASH_MODELS29 = V5 ? METHODS.map((m) => C29.modelFor("central", m, C29.withCentral({}))) : null;
const PA = V4 ? P29.correctionsPayload().meta.pension_accrual : null;

console.log(`[${CASE}: ${LANE}]`);
const without = (s, keys) => JSON.stringify(Object.fromEntries(Object.entries(s).filter(([k]) => !keys.includes(k))));
if (V4) {
  const stripped = (s) => without(s, ["line_responses"]);
  gate("September 27's specifications are the case's, every field but line_responses",
    SPECS27.length === SPECS29.length && SPECS29.every((s, i) => stripped(s) === stripped(SPECS27[i])), `${SPECS29.length} specifications`);
}
if (V5) {
  gate("September 29's specifications are the case's, every field but the group-size responses (gg, line_responses)",
    SPECS29.length === SPECS.length && SPECS.every((s, i) => without(s, ["gg", "line_responses"]) === without(SPECS29[i], ["gg", "line_responses"])),
    `${SPECS.length} specifications`);
  gate("each cash package's specifications are its set's, every field",
    C5.MAIN_SPECS.length === SPECS.length && SPECS.every((s, i) => JSON.stringify(s) === JSON.stringify(C5.MAIN_SPECS[i]))
    && C29.MAIN_SPECS.length === SPECS29.length && SPECS29.every((s, i) => JSON.stringify(s) === JSON.stringify(C29.MAIN_SPECS[i])),
    `${SPECS.length} specifications`);
  gate("the pension accrual's parameters are September 29's",
    JSON.stringify(P.correctionsPayload().meta.pension_accrual) === JSON.stringify(PA), `part_a_share ${PA.part_a_share}`);
}
{
  const costs = SCHOOL_MODELS.map((m) => S.MAIN_SPECS.map((s) => -Engine.evaluate(m, S.stateFor(m, s, S.MAIN_PROFILE)).welfare_bn));
  const band = [mean(costs.map((xs) => Math.min(...xs))), mean(costs.map((xs) => Math.max(...xs)))];
  gate("the schools-case evaluation reproduces the schools lane's band (1e-6)",
    near(band[0], schools.main_case[0], 1e-6) && near(band[1], schools.main_case[1], 1e-6), band.map((x) => x.toFixed(4)).join("/"));
}

// September 29's change from September 27 at one specification, line by line (see the header), and what its gates
// read: the pension amounts' distance from their rules and the enterprise surplus's move.
const change27 = (r, r27) => {
  const change = {}, meta = {};
  const row = (ev, side, id) => ev[side].find((x) => x.id === id);
  const add = (part, value, info) => {
    if (part in change) throw new Error(`[BLOCKED] two lines give the part ${part}`);
    change[part] = value;
    meta[part] = info;
  };
  for (const side of ["receipts", "spending"]) {
    const ids = [...new Set([...r27.evaluation[side].map((x) => x.id), ...r.evaluation[side].map((x) => x.id)])];
    for (const id of ids) {
      const a = row(r.evaluation, side, id), b = row(r27.evaluation, side, id);
      const d = -((a ? a.effect_bn : 0) - (b ? b.effect_bn : 0));
      if (d === 0) continue;
      const info = { side: side === "receipts" ? "receipt" : "spending", line: id, national_bn: (a || b).national_bn, parent: P29.PARENT[id] || null };
      if (side === "spending" && id === "social_security") {
        const accrual = a.response * a.amount_bn;
        add("v4_social_security_accrual", accrual, { ...info, rule: "accrual", contributions: "oasdi" });
        add("v4_social_security_cash", d - accrual, { ...info, rule: "benefits" });
      } else if (side === "spending" && id === "medicare") {
        const accrual = a.response * PA.part_a_accrual_bn;
        add("v4_medicare_part_a_accrual", accrual, { ...info, rule: "accrual", contributions: "hi" });
        add("v4_medicare_cash", d - accrual, { ...info, rule: "benefits" });
      } else add(`v4_${id}`, d, { ...info, rule: "line" });
    }
  }
  add("v4_production_private", -(r.evaluation.private_wtp_bn - r27.evaluation.private_wtp_bn),
    { side: "production", line: "private_wtp_bn", national_bn: null, parent: null, rule: "production" });
  add("v4_production_receipts", -(r.evaluation.induced_receipts_bn - r27.evaluation.induced_receipts_bn),
    { side: "production", line: "induced_receipts_bn", national_bn: null, parent: null, rule: "production" });
  const rec = (id) => row(r.evaluation, "receipts", id).amount_bn;
  const ss = row(r.evaluation, "spending", "social_security");
  const md = row(r.evaluation, "spending", "medicare"), md27 = row(r27.evaluation, "spending", "medicare");
  const es = row(r.evaluation, "receipts", RECEIPT), es27 = row(r27.evaluation, "receipts", RECEIPT);
  return { change, meta,
    pension_gap: Math.max(
      Math.abs(ss.amount_bn - PA.ratio_net * (rec(PA.oasdi_lines[0]) + rec(PA.oasdi_lines[1]) + PA.se_oasdi_share * rec(PA.se_line))),
      Math.abs(md.amount_bn - (md27.amount_bn * (1 - PA.part_a_share) + PA.part_a_accrual_bn))),
    // The group's amount moves in proportion to the national total (one key share; the row's share is rounded).
    enterprise_gap: es.key === es27.key && es.response === es27.response
      ? Math.abs(es.amount_bn - es27.amount_bn * es.national_bn / es27.national_bn) : Infinity,
    enterprise_move_bn: es.national_bn - es27.national_bn };
};

// October 5's change from September 29 at one specification, line by line (see the header): r and r29 are the set's
// evaluations, c and c29 the cash set's. The lineage's synthetic education lines carry with education services, as
// debt_legacy.py's SYNTHETIC_CARRY does; the constant line, whose parts the back-cast does not see, per person.
const PARENT5 = V5 ? Object.assign({}, P.PARENT, { school_reprice: "education_services", college_rekey: "education_services" }) : null;
const PER_PERSON = ["lane_constants"];
const change29 = (r, r29, c, c29) => {
  const change = {}, meta = {};
  const row = (ev, side, id) => ev[side].find((x) => x.id === id);
  const eff = (run, side, id) => { const x = row(run.evaluation, side, id); return x ? x.effect_bn : 0; };
  const add = (part, value, info) => {
    if (part in change) throw new Error(`[BLOCKED] two lines give the part ${part}`);
    change[part] = value;
    meta[part] = info;
  };
  for (const side of ["receipts", "spending"]) {
    const ids = [...new Set([...r29.evaluation[side].map((x) => x.id), ...r.evaluation[side].map((x) => x.id)])];
    for (const id of ids) {
      const d = -(eff(r, side, id) - eff(r29, side, id));
      if (d === 0) continue;
      const x = row(r.evaluation, side, id) || row(r29.evaluation, side, id);
      const info = { side: side === "receipts" ? "receipt" : "spending", line: id, national_bn: x.national_bn, parent: PARENT5[id] || null };
      if (side === "spending" && (id === "social_security" || id === "medicare")) {
        // The cash set charges the added people's benefits; the set charges their accrual and, for Medicare, keeps
        // 1 - part_a_share of the benefits.
        const ss = id === "social_security", name = `v5_${id}`;
        const cash = -(eff(c, side, id) - eff(c29, side, id));
        const kept = ss ? 0 : 1 - PA.part_a_share;
        add(`${name}_benefits`, cash, { ...info, rule: "benefits" });
        add(ss ? "v5_social_security_accrual" : "v5_medicare_part_a_accrual", d - kept * cash,
          { ...info, rule: "accrual", contributions: ss ? "oasdi" : "hi" });
        add(`${name}_cash`, -(1 - kept) * cash, { ...info, rule: "benefits" });
      } else add(`v5_${id}`, d, { ...info, rule: PER_PERSON.includes(id) ? "per_person" : "line" });
    }
  }
  add("v5_production_private", -(r.evaluation.private_wtp_bn - r29.evaluation.private_wtp_bn),
    { side: "production", line: "private_wtp_bn", national_bn: null, parent: null, rule: "production" });
  add("v5_production_receipts", -(r.evaluation.induced_receipts_bn - r29.evaluation.induced_receipts_bn),
    { side: "production", line: "induced_receipts_bn", national_bn: null, parent: null, rule: "production" });
  // Lines on which the set and the cash set differ, for each case (debt_legacy.py's accrual_rows needs only these).
  const differ = (a, b) => ["receipts", "spending"].flatMap((s) => a.evaluation[s].filter((x) => x.effect_bn !== eff(b, s, x.id)).map((x) => `${s}:${x.id}`));
  return { change, meta, set_cash_lines: [...new Set([...differ(r, c), ...differ(r29, c29)])].sort() };
};

const out = { case: CASE, lane: LANE, rule: "each fill-in method's end specifications of the case, averaged; base = the schools case's cost at those specifications",
  inputs: Object.fromEntries([`${LANE}/derived/summary.json`, `${LANE}/derived/main_case_bands.csv`, `${LANE}/derived/corrections.json`,
    `${LANE}/package.cjs`, ...(V4 ? [`${CASES.sept27}/package.cjs`, `${CASES.sept27}/derived/corrections.json`] : []),
    ...(V5 ? [`${LANE}/derived/corrections_cash.json`, `${SEPT29_LANE}/package.cjs`, `${SEPT29_LANE}/derived/corrections.json`,
      `${SEPT29_LANE}/derived/main_case_bands.csv`, P.BASE_FILES.cash, ...Object.values(P.LINEAGE_FILES)] : [])]
    .map((rel) => [rel, sha256(rel)])),
  concepts: {} };
if (V4) {
  out.change_rule = "September 27's four additions from its package at the same specifications; the capital return at the case's "
    + "values; the change from September 27 line by line, v4_<line> = -(effect - September 27's effect), social security and "
    + "Medicare split into the accrual the pension switch charges and the benefits it no longer charges, and the production grid's "
    + "change in P and F";
  out.pension_accrual = Object.fromEntries(["ratio_net", "part_a_accrual_bn", "part_a_share", "se_oasdi_share", "oasdi_lines", "se_line"]
    .map((k) => [k, PA[k]]));
}
if (V5) {
  out.v5_change_rule = "every September 29 part from September 29's package at the same specifications, and the capital return at "
    + "September 29's values (capital_bn); the lineage's change from September 29 line by line, v5_<line> = -(effect - September 29's "
    + "effect), social security and Medicare split into the accrual the set charges, the benefits the cash set charges and minus the "
    + "benefits the set does not charge, the production grid's change in P and F, and the capital return's change by component "
    + "(v5_capital_bn)";
  const L = P.correctionsPayload().meta.lineage;
  out.lineage = Object.assign({ arm: L.arm, generation: L.generation, counting: L.counting.rule }, L.counts);
}
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
    // September 29 at the same specification (for the earlier cases, the case itself), and September 27 (for September
    // 27, the case itself).
    const r29 = V5 ? P29.evaluateFull(MODELS29[m], SPECS29[i], profile) : r;
    const r27 = V4 ? P27.evaluateFull(MODELS27[m], SPECS27[i], profile) : r;
    const e0 = Engine.evaluate(SCHOOL_MODELS[m], S.stateFor(SCHOOL_MODELS[m], S.MAIN_SPECS[i], base));
    const row = (ev, side, id) => ev[side].find((x) => x.id === id);
    const moved = (side) => r27.evaluation[side].filter((x) => {
      const y = row(e0, side, x.id);
      return !y || x.effect_bn !== y.effect_bn;
    }).map((x) => x.id).filter((id) => (side === "spending" ? !LINES.includes(id) : id !== RECEIPT));
    const parts = {};
    for (const id of LINES) {
      const a = row(r27.evaluation, "spending", id), b = row(e0, "spending", id);
      parts[id === P27.RENTAL ? "rental_assistance" : `long_run_${id}`] = a.response * a.amount_bn - b.response * b.amount_bn;
    }
    parts.enterprise_surplus = -(row(r27.evaluation, "receipts", RECEIPT).effect_bn - row(e0, "receipts", RECEIPT).effect_bn);
    const capital = Object.fromEntries(r29.capital.components.map((c) => [c.id, c.return_bn]));
    const baseCost = -e0.welfare_bn;
    const extra = {};
    if (V4) {
      Object.assign(extra, { check27: baseCost + Object.values(parts).reduce((a, b) => a + b, 0) + r27.capital.total_bn - r27.cost_bn,
        capital27: Object.fromEntries(r27.capital.components.map((c) => [c.id, c.return_bn])) }, change27(r29, r27));
      Object.assign(parts, extra.change);
    }
    if (V5) {
      const c = C5.evaluateFull(CASH_MODELS[m], SPECS[i], profile), c29 = C29.evaluateFull(CASH_MODELS29[m], SPECS29[i], profile);
      const v5 = change29(r, r29, c, c29);
      const same = JSON.stringify(r.capital.components.map((x) => x.id)) === JSON.stringify(r29.capital.components.map((x) => x.id));
      Object.assign(extra, { check29: baseCost + Object.values(parts).reduce((a, b) => a + b, 0) + r29.capital.total_bn - r29.cost_bn,
        v5_capital: same ? Object.fromEntries(r.capital.components.map((x) => [x.id, x.return_bn - capital[x.id]])) : null,
        v5_meta: v5.meta, set_cash_lines: v5.set_cash_lines });
      Object.assign(parts, v5.change);
    }
    const total = baseCost + Object.values(parts).reduce((a, b) => a + b, 0) + r.capital.total_bn;
    return { base: baseCost, cost: r.cost_bn, parts, capital, check: total - r.cost_bn,
      moved: [...moved("spending"), ...moved("receipts")],
      components: r.capital.components.map((c) => ({ id: c.id, part: c.group, level: c.level })), ...extra };
  };
  const at = ends.map((ij, m) => ij.map((i) => partsAt(m, i)));
  gate(`${concept}: at every end specification base + additions = the case's cost (1e-9) and no other line moves`,
    at.flat().every((x) => Math.abs(x.check) < 1e-9 && x.moved.length === 0),
    `max |diff| ${Math.max(...at.flat().map((x) => Math.abs(x.check))).toExponential(1)}; other lines moved: ${[...new Set(at.flat().flatMap((x) => x.moved))].join(" ") || "none"}`);
  if (V4) {
    const worst27 = Math.max(...at.flat().map((x) => Math.abs(x.check27)));
    gate(`${concept}: at every end specification the base, September 27's additions and its capital return = September 27's cost (1e-9)`,
      worst27 < 1e-9, `max |diff| ${worst27.toExponential(1)}`);
    const worstP = Math.max(...at.flat().map((x) => x.pension_gap));
    gate(`${concept}: social security's amount is ratio_net x the group's OASDI receipts and Medicare's the Part A swap (1e-9)`,
      worstP < 1e-9, `max |diff| ${worstP.toExponential(1)}`);
    const worstE = Math.max(...at.flat().map((x) => x.enterprise_gap));
    const moves = [...new Set(at.flat().map((x) => x.enterprise_move_bn))];
    gate(`${concept}: ${RECEIPT}'s group amount moves in proportion to its national total, at one key and response (1e-9)`,
      worstE < 1e-9 && moves.length === 1, `national total moves by ${moves.map((x) => x.toFixed(6)).join(", ")}`);
    out.v4_enterprise_surplus_national_move_bn = moves[0];
  }
  if (V5) {
    const worst29 = Math.max(...at.flat().map((x) => Math.abs(x.check29)));
    gate(`${concept}: at every end specification the September 29 parts and capital return = September 29's cost (1e-9)`,
      worst29 < 1e-9, `max |diff| ${worst29.toExponential(1)}`);
    gate(`${concept}: the case's capital components are September 29's`, at.flat().every((x) => x.v5_capital !== null));
    const lines = [...new Set(at.flat().flatMap((x) => x.set_cash_lines))].sort();
    const allowed = ["receipts:federal_income_tax", "spending:medicare", "spending:social_security"];
    gate(`${concept}: the set and the cash set differ only on federal income tax, Medicare and social security`,
      lines.every((x) => allowed.includes(x)), lines.join(" "));
    // The base row: where the case's end specifications are September 29's, September 29's band.
    const costs29 = MODELS29.map((m) => SPECS29.map((s) => P29.evaluateFull(m, s, profile).cost_bn));
    const ends29 = costs29.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
    if (JSON.stringify(ends29) === JSON.stringify(ends)) {
      const main = profile === P.MAIN_PROFILE;
      const want = main ? bandRow(profile, "sept29_case") : (() => {
        const r = csv(`${SEPT29_LANE}/derived/main_case_bands.csv`).find((x) => x.profile === profile && x.variant === "adopted");
        if (!r) throw new Error(`[BLOCKED] ${SEPT29_LANE} main_case_bands.csv has no ${profile}/adopted row`);
        return [Number(r.cost_low_bn), Number(r.cost_high_bn)];
      })();
      // base + September 29's parts and capital at each end = check29 + September 29's cost there
      const got = [0, 1].map((e) => mean(at.map((pair, m) => pair[e].check29 + costs29[m][ends[m][e]])));
      gate(`${concept}: the case less the lineage is September 29's band, ${main ? "main_case_bands.csv sept29_case" : `${SEPT29_LANE} adopted`} (1e-4)`,
        near(got[0], want[0], 1e-4) && near(got[1], want[1], 1e-4), got.map((x) => x.toFixed(4)).join("/"));
    } else console.log(`  note ${concept}: September 29's end specifications ${JSON.stringify(ends29)} are not the case's; no band check`);
  }
  const avg = (e, f) => mean(at.map((pair) => f(pair[e])));
  const ids = at[0][0].components.map((c) => c.id);
  // Every part at any end specification, in the order first met (a part missing at one specification is 0 there).
  const partIds = [...new Set(at.flat().flatMap((x) => Object.keys(x.parts)))];
  out.concepts[concept] = { profile, base_profile: base, end_specifications: ends.map((ij, m) => ({ method: METHODS[m], low: ij[0], high: ij[1] })),
    ends: Object.fromEntries(["low", "high"].map((end, e) => [end, {
      cost_bn: avg(e, (x) => x.cost), base_bn: avg(e, (x) => x.base),
      additions_bn: Object.fromEntries(partIds.map((k) => [k, avg(e, (x) => x.parts[k] || 0)])),
      capital_bn: Object.fromEntries(ids.map((k) => [k, avg(e, (x) => x.capital[k])])),
      ...(V5 ? { v5_capital_bn: Object.fromEntries(ids.map((k) => [k, avg(e, (x) => x.v5_capital[k])])) } : {}),
    }])),
    components: at[0][0].components };
  if (V4) out.concepts[concept].v4_parts = Object.assign({}, ...at.flat().map((x) => x.meta));
  if (V5) out.concepts[concept].v5_parts = Object.assign({}, ...at.flat().map((x) => x.v5_meta));
  if (profile === P.MAIN_PROFILE) {
    // The September 27 case's parts: the case's change for September 27, under sept27_case from September 29 on (and
    // under sept29_case.sept27_case from October 5).
    const change = V5 ? summary.change_at_fixed_specifications.sept29_case : summary.change_at_fixed_specifications;
    const c = V4 ? change.sept27_case : change;
    const cap = summary.capital_at_end_specifications.by_component;
    const E = out.concepts[concept].ends;
    // September 27's capital return by component: the case's own for September 27, September 27's run for September 29.
    const cap27 = (e, id) => (V4 ? avg(e === "low" ? 0 : 1, (x) => x.capital27[id]) : E[e].capital_bn[id]);
    const sumOf = (e, part) => ids.filter((id) => at[0][0].components.find((x) => x.id === id).part === part)
      .reduce((a, id) => a + cap27(e, id), 0);
    const pairs = [["long_run_responses", (e) => E[e].additions_bn.long_run_economic_affairs_services + E[e].additions_bn.long_run_recreation_culture],
      ["rental_assistance", (e) => E[e].additions_bn.rental_assistance], ["enterprise_surplus_receipt", (e) => E[e].additions_bn.enterprise_surplus],
      ["capital_core", (e) => sumOf(e, "core")], ["capital_block", (e) => sumOf(e, "block")], ["capital_enterprise", (e) => sumOf(e, "enterprise")]];
    const worst = Math.max(...pairs.flatMap(([k, f]) => ["low", "high"].map((e, j) => Math.abs(f(e) - c[k][j]))));
    gate(`${concept}: the ${V4 ? "September 27 " : ""}parts equal summary.json change_at_fixed_specifications${V5 ? ".sept29_case" : ""}${V4 ? ".sept27_case" : ""} (1e-9)`,
      worst < 1e-9, `max |diff| ${worst.toExponential(1)}`);
    // The case's capital return by component (October 5: September 29's and the lineage's change).
    const capOf = (e, id) => (V5 ? E[e].capital_bn[id] + E[e].v5_capital_bn[id] : E[e].capital_bn[id]);
    const worstC = Math.max(...ids.flatMap((id) => ["low", "high"].map((e, j) => Math.abs(capOf(e, id) - cap[id].return_bn[j]))));
    gate(`${concept}: each capital component equals summary.json capital_at_end_specifications (1e-9)`, worstC < 1e-9,
      `${ids.length} components, max |diff| ${worstC.toExponential(1)}`);
    if (V4) {
      const changeAt = (e) => partIds.filter((k) => k.startsWith("v4_")).reduce((a, k) => a + E[e].additions_bn[k], 0)
        + ids.reduce((a, id) => a + E[e].capital_bn[id] - cap27(e, id), 0);
      const total = change.total;
      const worstT = Math.max(...["low", "high"].map((e, j) => Math.abs(changeAt(e) - total[j])));
      gate(`${concept}: the v4 parts and the capital return's change equal change_at_fixed_specifications${V5 ? ".sept29_case" : ""}.total (1e-9)`, worstT < 1e-9,
        `${["low", "high"].map((e) => changeAt(e).toFixed(4)).join("/")}, max |diff| ${worstT.toExponential(1)}`);
    }
    if (V5) {
      const changeAt = (e) => partIds.filter((k) => k.startsWith("v5_")).reduce((a, k) => a + E[e].additions_bn[k], 0)
        + ids.reduce((a, id) => a + E[e].v5_capital_bn[id], 0);
      const total = summary.change_at_fixed_specifications.total;
      const worstT = Math.max(...["low", "high"].map((e, j) => Math.abs(changeAt(e) - total[j])));
      gate(`${concept}: the lineage's parts and its capital change equal change_at_fixed_specifications.total (1e-9)`, worstT < 1e-9,
        `${["low", "high"].map((e) => changeAt(e).toFixed(4)).join("/")}, max |diff| ${worstT.toExponential(1)}`);
    }
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
