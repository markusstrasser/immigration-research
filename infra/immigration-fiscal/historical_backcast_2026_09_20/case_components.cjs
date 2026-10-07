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
 * October 7 (OCT07_LANE, main case v6) is October 5 plus an item registry (meta.items). Every October 5 part comes from
 * October 5's package (P6.OCT05) at the same specification, as --case oct05 computes it. The items' change from October 5
 * is then added item by item, each item with its own parts (v6_<item>_<path>_<line>), never booked as an October 5 part.
 * The items are taken in the payload's order: the lineage item first (it re-values the added people's edits in place),
 * then the edit sets in registry order. Step k is the package's caseOf(v5, the first k items), so an item's change is
 * step k less step k - 1 at the same specification, and the last step is the case. Each step carries a union twin:
 * September 29's model plus audit row 8's change plus the union's part of every edit set so far. A cell shift takes its
 * union_ parts (meta.items); a national-scale edit takes the line's national total in the case after the step, so it
 * scales the twin's cells as it scales the case's. An item's change on a line then splits into the union's part (path
 * union: the twin's change) and the added people's (path lineage: the rest); the lineage item's change is the added
 * people's only. Social security and Medicare split per path as the lineage's do (accrual, benefits, cash). The cash
 * set's step is the cash package's (P6.CASH); an item that does not enter the cash set (the pension accrual) leaves it
 * unchanged. The capital return's change splits by component and path (v6_capital_bn). October 7's gates: the case's
 * specifications are October 5's; the last step is the case (set and cash set payloads, and the cost at every end
 * specification, 1e-9); the twin at October 5 less September 29 is change_at_fixed_specifications.oct05_case
 * .union_response_move; the edit sets move neither P nor F; at each step the set and the cash set differ only on federal
 * income tax, Medicare and social security; where the case's end specifications are October 5's, the case less the
 * items is October 5's band; on the main profile the items' parts and capital change equal
 * change_at_fixed_specifications.total, each item's equal its change alone plus its interactions with the items before it
 * (.items, .interactions), each edit set's union parts its .union (a union-only item's with its capital change), and
 * the capital return equals
 * capital_at_end_specifications (1e-9).
 *
 * Run from anywhere: node case_components.cjs [--case sept27|sept29|oct05|oct07] [--out-dir DIR]
 * -> derived/case_components_<case>.json (the default case is sept27, whose file backcast.py's default run reads).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.resolve(__dirname, "..");
const SEPT29_LANE = "main_case_2026_09_29";
const OCT05_LANE = "main_case_2026_10_05";
const OCT07_LANE = "main_case_2026_10_07";
const CASES = { sept27: "main_case_long_run_2026_09_27", sept29: SEPT29_LANE, oct05: OCT05_LANE, oct07: OCT07_LANE };
const DEFAULT_CASE = "sept27";
const argv = process.argv.slice(2);
const opt = (name, dflt) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : dflt);
const CASE = opt("--case", DEFAULT_CASE);
if (!CASES[CASE]) throw new Error(`[BLOCKED] unknown case ${CASE}`);
const LANE = CASES[CASE];
const OUT = path.resolve(opt("--out-dir", path.join(__dirname, "derived")));

// October 7: the case's package (P6) is October 5's with an item registry; P is October 5's package, so every October 5
// part below is computed as --case oct05 computes it, and PC is the case.
const V6 = CASE === "oct07";
const P6 = V6 ? require(path.join(FISCAL, LANE, "package.cjs")) : null;
if (V6 && P6.OCT05 !== require(path.join(FISCAL, OCT05_LANE, "package.cjs"))) {
  throw new Error("[BLOCKED] the case's package does not build on October 5's package");
}
const P = V6 ? P6.OCT05 : require(path.join(FISCAL, LANE, "package.cjs"));
const PC = V6 ? P6 : P;
// September 29 takes the schools case and September 27's additions from September 27's package; October 5 takes every
// September 29 part from September 29's package (P29, its SEPT29) and adds the lineage's change.
const V5 = CASE === "oct05" || V6;
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
// October 5's change from September 29 (October 7 keeps it under change_at_fixed_specifications.oct05_case).
const CH5 = V6 ? summary.change_at_fixed_specifications.oct05_case : summary.change_at_fixed_specifications;
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
const MODELS = METHODS.map((m) => PC.modelFor("central", m, PC.withCentral({})));
const SCHOOL_MODELS = METHODS.map((m) => P27.modelFor("central", m, P27.withCentral({ enterprise_rekey: false })));
const MODELS27 = V4 ? METHODS.map((m) => P27.modelFor("central", m, P27.withCentral({}))) : MODELS;
const SPECS = PC.MAIN_SPECS;
if (SPECS.length !== S.MAIN_SPECS.length) throw new Error("[BLOCKED] the case and the schools case differ in specifications");
// October 7 also needs October 5's models (P's).
const MODELS5 = V6 ? METHODS.map((m) => P.modelFor("central", m, P.withCentral({}))) : MODELS;
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
// The lines on which a case's set and cash set may differ (the pension switch).
const SET_CASH_LINES = ["receipts:federal_income_tax", "spending:medicare", "spending:social_security"];

// October 7: the items' cumulative cases and their union twins (see the header).
const ALLOCS = ["personal", "shared"];
const lineKey = (side, id) => `${side === "receipt" || side === "receipts" ? "receipt" : "spending"}:${id}`;
const nationalsOf = (m) => new Map(m.spending.lines.map((l) => [lineKey("spending", l.id), l.national_bn])
  .concat(m.receipts.lines.map((l) => [lineKey("receipt", l.id), l.national_bn])));
const ROW8 = V6 ? P.LINEAGE_EDITS[P.LINEAGE_EDITS.length - 1] : null;
// The capital components an item adds beside the payload's (its offsets) and the component whose stock each takes.
const OF_COMPONENT = V6 ? Object.fromEntries((PC.ITEM_COMPONENTS || []).map((c) => [c.id, c.of_component])) : {};
if (Object.values(OF_COMPONENT).some((x) => !x)) throw new Error("[BLOCKED] an item's capital component names no component whose stock it takes (of_component)");
// One edit set on the union twins (one per method): a cell shift takes the sum of its union_ parts (an edit with no
// parts cannot be split, so the run stops); a national-scale edit takes the line's national total in the case after the
// step, gated to start from the case's.
function twinStep(rec, edits, twins, before, after) {
  const union = edits.map(() => null);
  for (const [name, p] of Object.entries(rec.parts || {})) {
    if (!/^(union|lineage)_/.test(name)) throw new Error(`[BLOCKED] item ${rec.id}: part ${name} is neither the union's (union_) nor the added people's (lineage_)`);
    if (!edits[p.edit] || !edits[p.edit].by) throw new Error(`[BLOCKED] item ${rec.id}: part ${name} names no cell shift`);
    if (name.startsWith("union_")) union[p.edit] = Object.fromEntries(ALLOCS.map((a) => [a, (union[p.edit] ? union[p.edit][a] : 0) + p.by[a]]));
  }
  const parted = new Set(Object.values(rec.parts || {}).map((p) => p.edit));
  return twins.map((t, m) => {
    const N0 = nationalsOf(before[m]), N1 = nationalsOf(after[m]), NT = nationalsOf(t);
    const out = [];
    edits.forEach((e, j) => {
      if (e.national_bn !== undefined) {
        const k = lineKey(e.side, e.line);
        if (NT.get(k) !== N0.get(k)) throw new Error(`[BLOCKED] item ${rec.id}: the twin's national total of ${k} is not the case's before the item`);
        out.push({ side: e.side, line: e.line, national_bn: N1.get(k) });
      } else if (!parted.has(j)) {
        throw new Error(`[BLOCKED] item ${rec.id}: a cell shift on ${e.line} with no union_ or lineage_ parts; this lane cannot split it between the union and the added people`);
      } else if (union[j]) out.push(Object.assign({}, e, { by: union[j] }));
    });
    return Engine.applyCorrections(t, { edits: out, meta: t.corrections });
  });
}
const STEPS = [];
if (V6) {
  gate("the case's specifications are October 5's, every field, and its cash package's are its set's",
    P.MAIN_SPECS.length === SPECS.length && SPECS.every((s, i) => JSON.stringify(s) === JSON.stringify(P.MAIN_SPECS[i]))
    && PC.CASH.MAIN_SPECS.length === SPECS.length && SPECS.every((s, i) => JSON.stringify(s) === JSON.stringify(PC.CASH.MAIN_SPECS[i])),
    `${SPECS.length} specifications`);
  gate("the case's profiles are October 5's", JSON.stringify(PC.ALL_PROFILES) === JSON.stringify(P.ALL_PROFILES) && PC.MAIN_PROFILE === P.MAIN_PROFILE);
  gate("October 5's last lineage edit is audit row 8's change on lane_constants (meta.lineage.edits.row8_edit_bn)",
    ROW8.line === "lane_constants" && ROW8.key === "k" && ALLOCS.every((a) => ROW8.by[a] === P.LINEAGE_META.edits.row8_edit_bn), String(ROW8.by.shared));
  const lin = PC.LINEAGE_ITEM;
  const order = [...(lin ? [lin] : []), ...PC.ITEM_IDS.filter((id) => id !== lin)];
  const twinOf = (Q) => METHODS.map((m) => {
    const x = Q.modelFor("central", m, Q.withCentral({}));
    return Engine.applyCorrections(x, { edits: [ROW8], meta: x.corrections });
  });
  let prev = { id: null, kind: "base", Q: P, models: MODELS5, cashModels: CASH_MODELS, twins: twinOf(P29), cashTwins: twinOf(C29) };
  STEPS.push(prev);
  order.forEach((id, k) => {
    const ids = PC.ITEM_IDS.filter((x) => order.slice(0, k + 1).includes(x));
    const arms = Object.fromEntries(Object.entries(PC.ITEM_ARMS).filter(([x]) => ids.includes(x)));
    const Q = P6.caseOf(P6.OCT05, ids, arms);
    const rec = Q.CASE_ITEMS.find((x) => x.id === id), recCash = Q.CASH.CASE_ITEMS.find((x) => x.id === id);
    const of = (p, r) => p.edits.slice(r.edits.first, r.edits.first + r.edits.count);
    // How the step's change splits: the lineage item's is the added people's; an edit set that prices the union only
    // (its record's union_only) is the union's; any other edit set splits by the twin.
    const mode = rec.kind === "lineage" ? "lineage" : rec.kind !== "edit_set" ? null : rec.union_only ? "union" : "twin";
    if (!mode) throw new Error(`[BLOCKED] item ${id}: no rule for an item of kind ${rec.kind}`);
    const step = { id, kind: rec.kind, mode, Q, rec, recCash, cash_applied: recCash.applied,
      models: METHODS.map((m) => Q.modelFor("central", m, Q.withCentral({}))),
      cashModels: METHODS.map((m) => Q.CASH.modelFor("central", m, Q.CASH.withCentral({}))), twins: prev.twins, cashTwins: prev.cashTwins };
    if (mode === "twin") {
      if (!prev.twins || (recCash.applied && !prev.cashTwins)) throw new Error(`[BLOCKED] item ${id} splits by the twin, which an earlier union-only item left without its capital`);
      step.twins = twinStep(rec, of(Q.correctionsPayload(), rec), prev.twins, prev.models, step.models);
      if (recCash.applied) step.cashTwins = twinStep(recCash, of(Q.CASH.correctionsPayload(), recCash), prev.cashTwins, prev.cashModels, step.cashModels);
    } else if (mode === "union") {
      // The twin would need the item's carriers and capital components, which only the case's package evaluates; no
      // later step may split by it.
      step.twins = null;
      step.cashTwins = null;
    }
    STEPS.push(step);
    prev = step;
  });
  const last = STEPS[STEPS.length - 1].Q;
  gate("the last step is the case: its set and cash set payloads are the case's",
    JSON.stringify(last.correctionsPayload()) === JSON.stringify(PC.correctionsPayload())
    && JSON.stringify(last.CASH.correctionsPayload()) === JSON.stringify(PC.CASH.correctionsPayload()), `steps: ${order.join(", ")}`);
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

// October 7: one item's change at one specification, step k less step k - 1 (see the header), into acc. r1/r0 are the
// set's evaluations, c1/c0 the cash set's, t1/t0 and tc1/tc0 the union twins'. On each line the union's part is the
// twin's change and the added people's the rest; the lineage item's change is theirs only, a union-only edit set's the
// union's only. Social security and Medicare split per path as change29 splits the lineage's; the production grid's
// change is the added people's (an edit set's must be zero, recorded in acc.production); the capital return's change by
// component and path, a component the item adds (its offsets) counting from zero. An item's carrier receipt lines carry
// no amount that matters (gated below 1e-12 bn) and give no part. acc.items[item] keeps the step's change in cost, its
// parts' and capital change's sum and its union parts' sum, for the gates.
const changeItem = (acc, st, r1, r0, c1, c0, t1, t0, tc1, tc0) => {
  const row = (ev, side, id) => ev[side].find((x) => x.id === id);
  const eff = (run, side, id) => { const x = row(run.evaluation, side, id); return x ? x.effect_bn : 0; };
  const lineage = st.mode === "lineage", unionOnly = st.mode === "union";
  const carriers = new Set([...((st.rec.capital || {}).receipt_lines || []), ...(((st.recCash || {}).capital || {}).receipt_lines || [])]);
  const own = { sum: 0, union: 0 };
  const add = (part, value, info) => {
    if (part in acc.change) throw new Error(`[BLOCKED] two lines give the part ${part}`);
    acc.change[part] = value;
    acc.meta[part] = Object.assign({ item: st.id }, info);
    own.sum += value;
    if (info.path === "union") own.union += value;
  };
  for (const side of ["receipts", "spending"]) {
    const ids = [...new Set([...r0.evaluation[side].map((x) => x.id), ...r1.evaluation[side].map((x) => x.id)])];
    for (const id of ids) {
      const d = -(eff(r1, side, id) - eff(r0, side, id)), cash = -(eff(c1, side, id) - eff(c0, side, id));
      if (side === "receipts" && carriers.has(id)) {
        if (Math.abs(d) > 1e-12 || Math.abs(cash) > 1e-12) throw new Error(`[BLOCKED] item ${st.id}: its carrier ${id} moves the cost by ${d}`);
        continue;
      }
      const du = lineage ? 0 : unionOnly ? d : -(eff(t1, side, id) - eff(t0, side, id));
      const cu = lineage ? 0 : unionOnly ? cash : -(eff(tc1, side, id) - eff(tc0, side, id));
      const x = row(r1.evaluation, side, id) || row(r0.evaluation, side, id);
      const info = { side: side === "receipts" ? "receipt" : "spending", line: id, national_bn: x.national_bn, parent: PARENT5[id] || null };
      for (const [pathName, dp, cp] of [["union", du, cu], ["lineage", d - du, cash - cu]]) {
        const name = `v6_${st.id}_${pathName}_${id}`, pinfo = Object.assign({ path: pathName }, info);
        if (side === "spending" && (id === "social_security" || id === "medicare")) {
          if (dp === 0 && cp === 0) continue;
          // As change29: the set charges the accrual and, for Medicare, keeps 1 - part_a_share of the benefits the cash
          // set charges.
          const ss = id === "social_security", kept = ss ? 0 : 1 - PA.part_a_share;
          add(ss ? `v6_${st.id}_${pathName}_social_security_accrual` : `v6_${st.id}_${pathName}_medicare_part_a_accrual`, dp - kept * cp,
            { ...pinfo, rule: "accrual", contributions: ss ? "oasdi" : "hi" });
          if (cp !== 0) {
            add(`${name}_benefits`, cp, { ...pinfo, rule: "benefits" });
            add(`${name}_cash`, -(1 - kept) * cp, { ...pinfo, rule: "benefits" });
          }
        } else if (dp !== 0) add(name, dp, { ...pinfo, rule: PER_PERSON.includes(id) ? "per_person" : "line" });
      }
    }
  }
  const dP = -(r1.evaluation.private_wtp_bn - r0.evaluation.private_wtp_bn), dF = -(r1.evaluation.induced_receipts_bn - r0.evaluation.induced_receipts_bn);
  if (lineage) {
    add(`v6_${st.id}_lineage_production_private`, dP, { side: "production", line: "private_wtp_bn", national_bn: null, parent: null, path: "lineage", rule: "production" });
    add(`v6_${st.id}_lineage_production_receipts`, dF, { side: "production", line: "induced_receipts_bn", national_bn: null, parent: null, path: "lineage", rule: "production" });
  } else acc.production.push(Math.abs(dP) + Math.abs(dF));
  const cap = (run) => Object.fromEntries(run.capital.components.map((x) => [x.id, x.return_bn]));
  const k1 = cap(r1), k0 = cap(r0);
  const added = Object.keys(k1).filter((id) => !(id in k0));
  const allowed = new Set(((st.rec.capital || {}).components) || []);
  if (Object.keys(k0).some((id) => !(id in k1)) || added.some((id) => !allowed.has(id)) || (added.length && st.mode === "twin")) {
    throw new Error(`[BLOCKED] item ${st.id} changes the capital components beyond the ones it adds (${added.join(", ")})`);
  }
  const kt1 = st.mode === "twin" ? cap(t1) : null, kt0 = st.mode === "twin" ? cap(t0) : null;
  let capital = 0;
  for (const id of Object.keys(k1)) {
    const move = k1[id] - (k0[id] ?? 0);
    const du = lineage ? 0 : unionOnly ? move : kt1[id] - kt0[id];
    acc.capital.union[id] = (acc.capital.union[id] || 0) + du;
    acc.capital.lineage[id] = (acc.capital.lineage[id] || 0) + (move - du);
    capital += move;
  }
  const differ = (a, b) => ["receipts", "spending"].flatMap((s) => a.evaluation[s].filter((x) => x.effect_bn !== eff(b, s, x.id)).map((x) => `${s}:${x.id}`));
  acc.lines.push(...differ(r1, c1));
  // A union-only item's union is its whole change, its capital change included, as the case's summary counts it; a twin-split
  // item's union excludes its capital change, which the summary reports apart (capital_return).
  acc.items[st.id] = { total: r1.cost_bn - r0.cost_bn, parts: own.sum + capital, union: own.union + (unionOnly ? capital : 0),
    step_gap: Math.abs(own.sum + capital - (r1.cost_bn - r0.cost_bn)) };
};

const out = { case: CASE, lane: LANE, rule: "each fill-in method's end specifications of the case, averaged; base = the schools case's cost at those specifications",
  inputs: Object.fromEntries([`${LANE}/derived/summary.json`, `${LANE}/derived/main_case_bands.csv`, `${LANE}/derived/corrections.json`,
    `${LANE}/package.cjs`, ...(V4 ? [`${CASES.sept27}/package.cjs`, `${CASES.sept27}/derived/corrections.json`] : []),
    ...(V5 ? [`${LANE}/derived/corrections_cash.json`, `${SEPT29_LANE}/package.cjs`, `${SEPT29_LANE}/derived/corrections.json`,
      `${SEPT29_LANE}/derived/main_case_bands.csv`, P.BASE_FILES.cash, ...Object.values(P.LINEAGE_FILES)] : []),
    ...(V6 ? [`${OCT05_LANE}/package.cjs`, `${OCT05_LANE}/derived/corrections.json`, `${OCT05_LANE}/derived/corrections_cash.json`,
      `${OCT05_LANE}/derived/main_case_bands.csv`, `${LANE}/item_age_mix.cjs`, ...Object.values(PC.LINEAGE_FILES)] : [])]
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
if (V6) {
  out.v6_change_rule = "every October 5 part from October 5's package at the same specifications (as --case oct05); the items' change "
    + "from October 5 item by item, in the payload's order (the lineage item first, then the edit sets in registry order), each "
    + "step the package's caseOf(v5, the items so far) less the step before at the same specification; on each line the union's "
    + "part (path union) is the change of the union twin (September 29's model plus audit row 8's change plus the edit sets' "
    + "union_ parts and national totals) and the added people's (path lineage) the rest, v6_<item>_<path>_<line>, social "
    + "security and Medicare split per path into the accrual the set charges, the benefits the cash set charges and minus the "
    + "benefits the set does not charge; the production grid's change (the lineage item's only); the capital return's change "
    + "by component and path (v6_capital_bn)";
  out.v6_items = STEPS.slice(1).map((st) => ({ id: st.id, kind: st.kind, label: st.rec.label, source: st.rec.source, arm: st.rec.arm,
    cash_applied: st.cash_applied }));
}
for (const [concept, profile] of Object.entries(CONCEPTS)) {
  const base = P.ALL_PROFILES[profile].base;
  const runs = MODELS.map((m) => SPECS.map((s) => PC.evaluateFull(m, s, profile)));
  const costs = runs.map((xs) => xs.map((r) => r.cost_bn));
  const ends = costs.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
  const band = [mean(costs.map((xs) => Math.min(...xs))), mean(costs.map((xs) => Math.max(...xs)))];
  const adopted = bandRow(profile, "adopted");
  gate(`${concept} (${profile}): the band is main_case_bands.csv's adopted row (1e-4)`,
    near(band[0], adopted[0], 1e-4) && near(band[1], adopted[1], 1e-4), `${band.map((x) => x.toFixed(4)).join("/")}; ends ${JSON.stringify(ends)}`);
  // The parts at one method's end specification.
  const partsAt = (m, i) => {
    const r = runs[m][i];
    // October 5 at the same specification (for the earlier cases, the case itself), September 29 (for the earlier cases,
    // the case itself) and September 27 (for September 27, the case itself).
    const r5 = V6 ? P.evaluateFull(MODELS5[m], SPECS[i], profile) : r;
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
    let c5 = null;
    if (V5) {
      const c = C5.evaluateFull(CASH_MODELS[m], SPECS[i], profile), c29 = C29.evaluateFull(CASH_MODELS29[m], SPECS29[i], profile);
      c5 = c;
      const v5 = change29(r5, r29, c, c29);
      const same = JSON.stringify(r5.capital.components.map((x) => x.id)) === JSON.stringify(r29.capital.components.map((x) => x.id));
      Object.assign(extra, { check29: baseCost + Object.values(parts).reduce((a, b) => a + b, 0) + r29.capital.total_bn - r29.cost_bn,
        v5_capital: same ? Object.fromEntries(r5.capital.components.map((x) => [x.id, x.return_bn - capital[x.id]])) : null,
        v5_meta: v5.meta, set_cash_lines: v5.set_cash_lines });
      Object.assign(parts, v5.change);
    }
    if (V6) {
      // The items, step by step from October 5; the twins are evaluated as October 5's package evaluates any model.
      const acc = { change: {}, meta: {}, capital: { union: {}, lineage: {} }, items: {}, production: [], lines: [] };
      let r0 = r5, c0 = c5;
      let t0 = P.evaluateFull(STEPS[0].twins[m], SPECS[i], profile), tc0 = C5.evaluateFull(STEPS[0].cashTwins[m], SPECS[i], profile);
      const twinMove = t0.cost_bn - r29.cost_bn;
      for (const st of STEPS.slice(1)) {
        const r1 = st.Q.evaluateFull(st.models[m], SPECS[i], profile), c1 = st.Q.CASH.evaluateFull(st.cashModels[m], SPECS[i], profile);
        const t1 = st.mode === "twin" ? P.evaluateFull(st.twins[m], SPECS[i], profile) : t0;
        const tc1 = st.mode === "twin" ? C5.evaluateFull(st.cashTwins[m], SPECS[i], profile) : tc0;
        changeItem(acc, st, r1, r0, c1, c0, t1, t0, tc1, tc0);
        [r0, c0, t0, tc0] = [r1, c1, t1, tc1];
      }
      Object.assign(extra, { v6_last: r0.cost_bn - r.cost_bn, v6_cash: c0.cost_bn, v6_twin_move: twinMove, v6_capital: acc.capital,
        v6_meta: acc.meta, v6_items: acc.items, v6_production: acc.production, v6_set_cash_lines: [...new Set(acc.lines)].sort() });
      Object.assign(parts, acc.change);
    }
    const total = baseCost + Object.values(parts).reduce((a, b) => a + b, 0) + r.capital.total_bn;
    return { base: baseCost, cost: r.cost_bn, parts, capital, check: total - r.cost_bn,
      moved: [...moved("spending"), ...moved("receipts")],
      components: r.capital.components.map((c) => Object.assign({ id: c.id, part: c.group, level: c.level },
        OF_COMPONENT[c.id] ? { of_component: OF_COMPONENT[c.id] } : {})), ...extra };
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
  if (V6) {
    const worstLast = Math.max(...at.flat().map((x) => Math.abs(x.v6_last)));
    gate(`${concept}: at every end specification the last step is the case (1e-9)`, worstLast < 1e-9, `max |diff| ${worstLast.toExponential(1)}`);
    const worstStep = Math.max(...at.flat().flatMap((x) => Object.values(x.v6_items).map((v) => v.step_gap)));
    gate(`${concept}: at every end specification each item's parts and capital change add to its step's change (1e-9)`, worstStep < 1e-9,
      `max |diff| ${worstStep.toExponential(1)}`);
    gate(`${concept}: the edit sets move neither P nor F`, at.flat().every((x) => x.v6_production.every((v) => v === 0)));
    const lines6 = [...new Set(at.flat().flatMap((x) => x.v6_set_cash_lines))].sort();
    gate(`${concept}: at every step the set and the cash set differ only on federal income tax, Medicare and social security`,
      lines6.every((x) => SET_CASH_LINES.includes(x)), lines6.join(" "));
    // The base row: where the case's end specifications are October 5's, the case less the items is October 5's band.
    const costs5 = MODELS5.map((m) => SPECS.map((s) => P.evaluateFull(m, s, profile).cost_bn));
    const ends5 = costs5.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
    if (JSON.stringify(ends5) === JSON.stringify(ends)) {
      const main = profile === P.MAIN_PROFILE;
      const want = main ? bandRow(profile, "oct05_case") : (() => {
        const r = csv(`${OCT05_LANE}/derived/main_case_bands.csv`).find((x) => x.profile === profile && x.variant === "adopted");
        if (!r) throw new Error(`[BLOCKED] ${OCT05_LANE} main_case_bands.csv has no ${profile}/adopted row`);
        return [Number(r.cost_low_bn), Number(r.cost_high_bn)];
      })();
      const got = [0, 1].map((e) => mean(costs5.map((xs, m) => xs[ends[m][e]])));
      gate(`${concept}: the case less the items is October 5's band, ${main ? "main_case_bands.csv oct05_case" : `${OCT05_LANE} adopted`} (1e-4)`,
        near(got[0], want[0], 1e-4) && near(got[1], want[1], 1e-4), got.map((x) => x.toFixed(4)).join("/"));
    } else console.log(`  note ${concept}: October 5's end specifications ${JSON.stringify(ends5)} are not the case's; no band check`);
    if (profile === P.MAIN_PROFILE) {
      // The twin at October 5 is the union at the case's responses: less September 29, the lineage line's union move.
      const got = [0, 1].map((e) => mean(at.map((pair) => pair[e].v6_twin_move)));
      gate(`${concept}: the union twin at October 5 less September 29 is change_at_fixed_specifications.oct05_case.union_response_move (1e-9)`,
        [0, 1].every((e) => near(got[e], CH5.union_response_move[e], 1e-9)), got.map((x) => x.toFixed(4)).join("/"));
      // The set at the end specifications is the case's band unrounded (main_case_bands.csv prints 4 decimals).
      const set = [0, 1].map((e) => mean(at.map((pair) => pair[e].cost)));
      gate(`${concept}: the set at the case's end specifications is summary.json main_case (1e-9)`,
        [0, 1].every((e) => near(set[e], summary.main_case[e], 1e-9)), set.map((x) => x.toFixed(6)).join("/"));
      // The cash set's last step is the case's cash set, where its end specifications are the set's.
      const cs = summary.cash_set;
      if (cs.end_specifications.every((x, m) => JSON.stringify(x) === JSON.stringify(ends[m]))) {
        const cash = [0, 1].map((e) => mean(at.map((pair) => pair[e].v6_cash)));
        gate(`${concept}: the cash set's last step at the case's end specifications is summary.json cash_set.band_bn (1e-9)`,
          [0, 1].every((e) => near(cash[e], cs.band_bn[e], 1e-9)), cash.map((x) => x.toFixed(4)).join("/"));
      } else console.log(`  note ${concept}: the cash set's end specifications are not the set's; no cash band check`);
    }
  }
  const avg = (e, f) => mean(at.map((pair) => f(pair[e])));
  const ids = at[0][0].components.map((c) => c.id);
  // Every part at any end specification, in the order first met (a part missing at one specification is 0 there).
  const partIds = [...new Set(at.flat().flatMap((x) => Object.keys(x.parts)))];
  out.concepts[concept] = { profile, base_profile: base, end_specifications: ends.map((ij, m) => ({ method: METHODS[m], low: ij[0], high: ij[1] })),
    ends: Object.fromEntries(["low", "high"].map((end, e) => [end, {
      cost_bn: avg(e, (x) => x.cost), base_bn: avg(e, (x) => x.base),
      additions_bn: Object.fromEntries(partIds.map((k) => [k, avg(e, (x) => x.parts[k] || 0)])),
      // (October 7: a component an item adds is 0 in the September 29 and October 5 values.)
      capital_bn: Object.fromEntries(ids.map((k) => [k, avg(e, (x) => x.capital[k] ?? 0)])),
      ...(V5 ? { v5_capital_bn: Object.fromEntries(ids.map((k) => [k, avg(e, (x) => x.v5_capital[k] ?? 0)])) } : {}),
      ...(V6 ? { v6_capital_bn: Object.fromEntries(["union", "lineage"].map((p) => [p, Object.fromEntries(ids.map((k) => [k, avg(e, (x) => x.v6_capital[p][k])]))])) } : {}),
    }])),
    components: at[0][0].components };
  if (V4) out.concepts[concept].v4_parts = Object.assign({}, ...at.flat().map((x) => x.meta));
  if (V5) out.concepts[concept].v5_parts = Object.assign({}, ...at.flat().map((x) => x.v5_meta));
  if (V6) out.concepts[concept].v6_parts = Object.assign({}, ...at.flat().map((x) => x.v6_meta));
  if (profile === P.MAIN_PROFILE) {
    // The September 27 case's parts: the case's change for September 27, under sept27_case from September 29 on (and
    // under sept29_case.sept27_case from October 5; October 7 keeps October 5's under oct05_case).
    const change = V5 ? CH5.sept29_case : CH5;
    const c = V4 ? change.sept27_case : change;
    const cap = summary.capital_at_end_specifications.by_component;
    const E = out.concepts[concept].ends;
    // September 27's capital return by component: the case's own for September 27, September 27's run for September 29.
    // (October 7: a component an item adds is 0 in September 27's run.)
    const cap27 = (e, id) => (V4 ? avg(e === "low" ? 0 : 1, (x) => x.capital27[id] ?? 0) : E[e].capital_bn[id]);
    const sumOf = (e, part) => ids.filter((id) => at[0][0].components.find((x) => x.id === id).part === part)
      .reduce((a, id) => a + cap27(e, id), 0);
    const pairs = [["long_run_responses", (e) => E[e].additions_bn.long_run_economic_affairs_services + E[e].additions_bn.long_run_recreation_culture],
      ["rental_assistance", (e) => E[e].additions_bn.rental_assistance], ["enterprise_surplus_receipt", (e) => E[e].additions_bn.enterprise_surplus],
      ["capital_core", (e) => sumOf(e, "core")], ["capital_block", (e) => sumOf(e, "block")], ["capital_enterprise", (e) => sumOf(e, "enterprise")]];
    const worst = Math.max(...pairs.flatMap(([k, f]) => ["low", "high"].map((e, j) => Math.abs(f(e) - c[k][j]))));
    gate(`${concept}: the ${V4 ? "September 27 " : ""}parts equal summary.json change_at_fixed_specifications${V5 ? ".sept29_case" : ""}${V4 ? ".sept27_case" : ""} (1e-9)`,
      worst < 1e-9, `max |diff| ${worst.toExponential(1)}`);
    // The case's capital return by component (October 5: September 29's and the lineage's change).
    // (October 7: and the items' change on both paths.)
    const capOf = (e, id) => (V5 ? E[e].capital_bn[id] + E[e].v5_capital_bn[id] : E[e].capital_bn[id])
      + (V6 ? E[e].v6_capital_bn.union[id] + E[e].v6_capital_bn.lineage[id] : 0);
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
      const total = CH5.total;
      const worstT = Math.max(...["low", "high"].map((e, j) => Math.abs(changeAt(e) - total[j])));
      gate(`${concept}: the lineage's parts and its capital change equal change_at_fixed_specifications${V6 ? ".oct05_case" : ""}.total (1e-9)`, worstT < 1e-9,
        `${["low", "high"].map((e) => changeAt(e).toFixed(4)).join("/")}, max |diff| ${worstT.toExponential(1)}`);
    }
    if (V6) {
      const ch = summary.change_at_fixed_specifications;
      const changeAt = (e) => partIds.filter((k) => k.startsWith("v6_")).reduce((a, k) => a + E[e].additions_bn[k], 0)
        + ids.reduce((a, id) => a + E[e].v6_capital_bn.union[id] + E[e].v6_capital_bn.lineage[id], 0);
      const worstT = Math.max(...["low", "high"].map((e, j) => Math.abs(changeAt(e) - ch.total[j])));
      gate(`${concept}: the items' parts and capital change equal change_at_fixed_specifications.total (1e-9)`, worstT < 1e-9,
        `${["low", "high"].map((e) => changeAt(e).toFixed(4)).join("/")}, max |diff| ${worstT.toExponential(1)}`);
      // Each item, taken after the ones before it, is its change alone plus its interactions with them (pairs; a
      // higher-order remainder is allowed for).
      const pair = (a, b) => ch.interactions[`${a}_x_${b}`] || ch.interactions[`${b}_x_${a}`];
      const rest = ch.interactions.remainder || [0, 0];
      const done = [];
      for (const st of STEPS.slice(1)) {
        const alone = ch.items[st.id];
        const pairs = done.map((j) => pair(j, st.id));
        if (!alone || pairs.some((x) => !x)) throw new Error(`[BLOCKED] summary.json lacks item ${st.id}'s change alone or a pair with it`);
        const want = [0, 1].map((e) => alone.total[e] + pairs.reduce((a, x) => a + x[e], 0));
        const got = [0, 1].map((e) => avg(e, (x) => x.v6_items[st.id].parts));
        gate(`${concept}: item ${st.id}'s parts and capital change are its change alone plus its pairs with ${done.join(", ") || "no item"} (1e-9 + the remainder)`,
          [0, 1].every((e) => near(got[e], want[e], 1e-9 + Math.abs(rest[e]))), got.map((x) => x.toFixed(4)).join("/"));
        if (st.kind === "edit_set" && alone.union) {
          const u = [0, 1].map((e) => avg(e, (x) => x.v6_items[st.id].union));
          gate(`${concept}: item ${st.id}'s union parts are its .union (1e-9)`, [0, 1].every((e) => near(u[e], alone.union[e], 1e-9)),
            u.map((x) => x.toFixed(4)).join("/"));
        }
        done.push(st.id);
      }
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
