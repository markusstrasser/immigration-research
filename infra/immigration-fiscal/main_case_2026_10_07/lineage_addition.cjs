/* The lineage's addition on main case v6, by part, for the record's figures on the added people (FAQ 19, the INDEX):
 * at the case's end specifications (48 low, 11 high, in both methods, each figure the two methods' mean), set and cash:
 *
 *   1. each count part, the G3-rate attriters (1.94M) and the later losses (1.09M): persons, their cost to others and
 *      the cost per person, at the case's responses, with items 1-3's lineage parts (item 4 is union-only);
 *   2. all the added people;
 *   3. the union's own response to the larger group: the union priced at the case's responses (the 19 group-size
 *      responses, row 8's edit and the long-run capital values at the lineage's share s) less at its own;
 *   4. the lineage's addition: v6 less v6 without the lineage, the union-only case with items 1, 2 and 4 at the union's
 *      size (item 1's lineage parts gone);
 *   5. that union-only case per member of the 39.71M, beside v6 per member of the 42.75M.
 *
 * Route. Each case below is the package's case at a lineage option (package.cjs caseOf with lineage_count.cjs's
 * additions; its lineageBase() and caseOf() are repeated in caseAt() because the options here are not named in
 * lineage_count.cjs OPTIONS): the added people at given counts with the group-size responses at a given share s and
 * metro factor. v5's package refuses a lineage of nobody, so the cases with nobody added are the intercepts of the cost,
 * which is affine in the counts at fixed responses (gated): U = C(l, 0) + C(0, g) - C(l, g).
 *   at the case's responses (arm b's s and metro factor): C(l, g) is the case itself; the later part is
 *     C(l, g) - C(0, g) and the G3-rate part C(l, g) - C(l, 0); U6 is the union there;
 *   at the union's own (v4's share s_v4 and metro factor 1, where every group-size response, row 8's factor and the
 *     long-run capital values are v4's exactly, lineage_count.cjs responsesAt()): the intercept is the union-only case.
 * The parts then add: (later + G3-rate) + (U6 - U_own) = C - U_own.
 *
 * Gates: the cost is affine in the counts (a fourth case at twice the later losses, at both responses); with no item the
 * route gives v5's stored figures (main_case_lineage_2026_10_05/derived/v5_summary.json, 1e-9) and its intercept at
 * the union's responses is the September 29 case; with every item the case is v6's adopted band; item 4 leaves the
 * added people's parts unchanged; the persons add to 3,039,719.59.
 *
 * Run: node lineage_addition.cjs [--lane <main_case_2026_10_07 dir>] [--out <file>]. It reads the lane's package
 * (read only) and writes one file, by default <lane>/derived/lineage_addition.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const argv = process.argv.slice(2);
const arg = (k) => (argv.includes(k) ? argv[argv.indexOf(k) + 1] : null);
const LANE_DIR = path.resolve(arg("--lane") || __dirname);
const OUT = path.resolve(arg("--out") || path.join(LANE_DIR, "derived", "lineage_addition.json"));
const FISCAL = path.join(LANE_DIR, "..");
const P = require(path.join(LANE_DIR, "package.cjs"));
const B = P.OCT05, POP = B.POP, { Engine, MODEL, METHODS } = P;
const TOOLS = { OCT05: B, Engine, MODEL, METHODS, readJson: B.readJson, sha256: B.sha256 };
const REG = new Map(P.REGISTRY.map((it) => [it.id, it]));
const ALL = P.CANDIDATE.slice(), NO_FEES = ALL.filter((id) => id !== "user_fees");
const V5_SUMMARY = "main_case_lineage_2026_10_05/derived/v5_summary.json";
const ENDS = [48, 11];
const SETS = ["set", "cash"];

const clone = (x) => JSON.parse(JSON.stringify(x));
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const pair = (f) => [0, 1].map(f);
const sub = (a, b) => pair((e) => a[e] - b[e]);
const f3 = (xs) => xs.map((x) => x.toFixed(3)).join(" / ");
const usd = (xs) => xs.map((x) => `$${Math.round(x).toLocaleString("en-US")}`).join(" / ");
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const sha = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const blocked = (why) => { throw new Error("[BLOCKED] lineage_addition: " + why); };
const GATES = [];
function gate(name, ok, detail) {
  GATES.push({ name, pass: !!ok, detail });
  console.log(`  ${ok ? "PASS" : "FAIL"} ${name}${detail ? ` — ${detail}` : ""}`);
}

// ---------------------------------------------------------------------------------------------------
// The options: the added people at counts (later, g3_rate), with the responses at the case's share or the union's own.
const AB = POP.arms[POP.meta.central_arm];
const AT = {
  case: { s: AB.s, k_metro: AB.k_metro, label: "the case's responses (arm b's share s and metro factor)" },
  union: { s: POP.meta.s_v4, k_metro: 1, label: "the union's own responses (v4's share s_v4, metro factor 1: v4's responses exactly)" },
};
const COUNTS = { later: [AB.later, 0], g3_rate: [0, AB.g3_rate], both: [AB.later, AB.g3_rate], later_twice: [2 * AB.later, 0] };
function optionsAt(where, names) {
  // A base whose population.json arms include these counts; lineage_count.cjs builds each addition by v5's route.
  const Bx = Object.create(B), arms = {};
  for (const name of names) {
    const [later, g3] = COUNTS[name];
    arms[`${where}_${name}`] = Object.assign(clone(AB), { source_arm: `${AB.source_arm}, counts ${name}`, later, g3_rate: g3, added: later + g3,
      population: POP.meta.account_union + later + g3, added_cps: null, s: AT[where].s, k_metro: AT[where].k_metro });
  }
  Bx.POP = Object.assign({}, POP, { arms: Object.assign({}, POP.arms, arms) });
  return Object.fromEntries(names.map((name) => {
    const id = `${where}_${name}`, A = Bx.POP.arms[id], c3 = clone(POP.c3);
    const additions = P.COUNT.additionsAt(Bx, id, c3, TOOLS);
    for (const w of SETS) {
      const a = additions[w], n5 = B.ADDITION[w].edits.length;
      // At v4's share row 8's change is 0 and the route leaves it out; v5's frame keeps it last.
      if (a.edits.length === n5 - 1 && a.meta.lineage.row8_edit_bn === 0) a.edits.push({ side: "spending", line: "lane_constants", key: "k", by: { personal: 0, shared: 0 } });
      if (a.edits.length !== n5) blocked(`${id} (${w}): ${a.edits.length} edits, not v5's ${n5}`);
      a.meta.source = `${P.V6.LANE}/lineage_addition.cjs (lineage_count.cjs additionsAt)`;
      a.meta.status = `a decomposition case, not adopted: ${name} counts at ${AT[where].label}`;
    }
    const L = additions.set.meta.lineage;
    const meta = { name: id, label: `${name} counts at ${AT[where].label}`, arm: id, source_arm: A.source_arm, added: A.added, g3_rate: A.g3_rate,
      later: A.later, population: A.population, c3: c3.value, s: L.s, k_metro: L.k_metro, row8_edit_bn: L.row8_edit_bn, m_g3plus: L.m_g3plus,
      m_white: L.m_white, module: `${P.V6.LANE}/lineage_addition.cjs` };
    return [name, { name: id, label: meta.label, arm: id, A, C3: c3.value, c3, m_g3plus: L.m_g3plus, m_white: L.m_white, additions, meta }];
  }));
}

// package.cjs lineageBase() and caseOf() for an option object: the lineage item (if named) built on the option's
// addition, the base rebased on it, the edit sets built on that base; every such case is a variant.
function caseAt(ids, opt) {
  const items = ids.map((id) => REG.get(id));
  const lin = items.find((it) => it.kind === "lineage") || null;
  const linBuilt = lin ? P.checkLineage(lin, lin.build(Object.assign({ B, LINEAGE_OPTION: opt }, TOOLS), null), B, opt.additions)
    : { additions: clone(opt.additions), lineage_meta: {}, record: {}, detail: {} };
  linBuilt.option = opt;
  const L = P.rebase(B, linBuilt);
  const ctx = Object.assign({ B: L, LINEAGE_ITEM: lin ? lin.id : null }, TOOLS);
  const built = items.map((item) => (item.kind === "lineage" ? { item, arm: null, lineage: linBuilt }
    : { item, arm: null, set: P.checkBuilt(item, item.build(ctx, null, "set"), L, "set"),
      cash: item.cash.applies ? P.checkBuilt(item, item.build(ctx, null, "cash"), L.CASH, "cash") : null }));
  const set = P.forItems(L, built, "set", false, opt), cash = P.forItems(L.CASH, built, "cash", false, opt);
  if (set.correctionsPayload().meta.adopted !== null) blocked(`${opt.name}: the case is stamped adopted`);
  return { set, cash };
}
// A set's cost at the end specifications, each the two methods' mean.
function endCosts(X) {
  const models = METHODS.map((m) => X.modelFor("central", m, X.withCentral({})));
  return ENDS.map((i) => mean(models.map((m) => X.evaluateFull(m, X.MAIN_SPECS[i], P.MAIN_PROFILE).cost_bn)));
}
const costsOf = (pkg) => ({ set: endCosts(pkg.set), cash: endCosts(pkg.cash) });

// ---------------------------------------------------------------------------------------------------
// The decomposition for one item list: the case itself, then the options at both responses.
const OPTS = { case: optionsAt("case", ["later", "g3_rate", "later_twice"]), union: optionsAt("union", ["later", "g3_rate", "both", "later_twice"]) };
function decompose(tag, ids, whole) {
  console.log(`\n[${tag}: items ${ids.length ? ids.join(", ") : "none"}]`);
  const C = costsOf(whole);
  const at = (where, name) => costsOf(caseAt(ids, OPTS[where][name]));
  const K = { later: at("case", "later"), g3_rate: at("case", "g3_rate"), later_twice: at("case", "later_twice") };
  const N = { later: at("union", "later"), g3_rate: at("union", "g3_rate"), both: at("union", "both"), later_twice: at("union", "later_twice") };
  const out = {};
  for (const w of SETS) {
    const u6 = pair((e) => K.later[w][e] + K.g3_rate[w][e] - C[w][e]), u6b = pair((e) => 2 * K.later[w][e] - K.later_twice[w][e]);
    const uo = pair((e) => N.later[w][e] + N.g3_rate[w][e] - N.both[w][e]), uob = pair((e) => 2 * N.later[w][e] - N.later_twice[w][e]);
    gate(`${tag} (${w}): the cost is affine in the counts at the case's responses: the union from the later and G3-rate cases equals it from the later cases at 1x and 2x (1e-9)`,
      worst(sub(u6, u6b)) < 1e-9, `${f3(u6)}; max |diff| ${worst(sub(u6, u6b)).toExponential(1)}`);
    gate(`${tag} (${w}): the same at the union's own responses (1e-9)`, worst(sub(uo, uob)) < 1e-9, `${f3(uo)}; max |diff| ${worst(sub(uo, uob)).toExponential(1)}`);
    const later = sub(C[w], K.g3_rate[w]), g3 = sub(C[w], K.later[w]), added = pair((e) => later[e] + g3[e]);
    const response = sub(u6, uo), addition = sub(C[w], uo);
    gate(`${tag} (${w}): parts 1 and 3 add to part 4, the lineage's addition (1e-9)`, worst(pair((e) => added[e] + response[e] - addition[e])) < 1e-9,
      `${f3(added)} + ${f3(response)} = ${f3(addition)}`);
    out[w] = { case_bn: C[w], union_at_case_responses_bn: u6, union_only_bn: uo, later_bn: later, g3_rate_bn: g3, added_bn: added,
      union_response_bn: response, lineage_addition_bn: addition };
  }
  return out;
}

const counts = { later: AB.later, g3_rate: AB.g3_rate, added: AB.added, account_union: POP.meta.account_union, lineage_population: AB.population };
console.log("[persons]");
gate("the count parts add to the added people, 3,039,719.59 (1e-6), and the lineage population is the union plus them",
  Math.abs(counts.later + counts.g3_rate - counts.added) < 1e-6 && Math.abs(counts.added - 3039719.59) < 0.005
  && Math.abs(counts.account_union + counts.added - counts.lineage_population) < 1e-6,
  `${counts.later.toFixed(2)} + ${counts.g3_rate.toFixed(2)} = ${counts.added.toFixed(2)}`);
const L6 = P.correctionsPayload().meta.lineage.counts;
gate("the counts are v6's meta.lineage.counts", L6.later_losses === counts.later && L6.at_g3_rate === counts.g3_rate && L6.added === counts.added
  && L6.account_union === counts.account_union && L6.lineage_population === counts.lineage_population, JSON.stringify(L6));

const V6 = decompose("v6", ALL, { set: P, cash: P.CASH });
const V5 = decompose("v5", [], { set: B, cash: B.CASH });
const NF = decompose("v6 without item 4", NO_FEES, (() => { const x = P.caseOf(B, NO_FEES); return { set: x, cash: x.CASH }; })());

// ---------------------------------------------------------------------------------------------------
console.log("\n[gates: v6, v5 and item 4]");
const S5 = JSON.parse(fs.readFileSync(path.join(FISCAL, V5_SUMMARY), "utf8"));
const band6 = { set: P.central({}), cash: P.CASH.central({}) };
const PINNED = { set: [389.082553, 461.479709], cash: [307.399411, 385.364123] };
for (const w of SETS) {
  gate(`v6 (${w}): the end costs are the adopted band (1e-9), the one the consumers pinned (6 decimals)`,
    worst(sub(V6[w].case_bn, band6[w])) < 1e-9 && worst(sub(V6[w].case_bn, PINNED[w])) < 5e-7, f3(V6[w].case_bn));
  const s5 = S5.sets[w].arms[POP.meta.central_arm], v4 = (w === "set" ? P.SEPT29 : P.SEPT29_CASH).central({});
  const pp = (bn, n) => bn.map((x) => x * 1e9 / n);
  const checks = [
    ["the later losses per person are the identified G3+ member's (g3plus_member_usd)", pp(V5[w].later_bn, counts.later), s5.g3plus_member_usd, 1e-9 * 1e9 / counts.later],
    ["the G3-rate attriters per person are (1 - C3) G3+ + C3 W (g3_rate_attriter_usd)", pp(V5[w].g3_rate_bn, counts.g3_rate), s5.g3_rate_attriter_usd, 1e-9 * 1e9 / counts.g3_rate],
    ["the added people per person (added_per_person_usd)", pp(V5[w].added_bn, counts.added), s5.added_per_person_usd, 1e-9 * 1e9 / counts.added],
    ["the added people are the G3+ and white parts (of_which_g3plus_part_bn + of_which_white_part_bn)", V5[w].added_bn, pair((e) => s5.of_which_g3plus_part_bn[e] + s5.of_which_white_part_bn[e]), 1e-9],
    ["the union's response (of_which_union_response_move_bn)", V5[w].union_response_bn, s5.of_which_union_response_move_bn, 1e-9],
    ["the lineage's addition is v5 less v4 (change_from_v4_bn)", V5[w].lineage_addition_bn, s5.change_from_v4_bn, 1e-9],
    ["the union-only case is the September 29 case", V5[w].union_only_bn, v4, 1e-9],
  ];
  for (const [name, got, want, tol] of checks) gate(`v5 (${w}), no item: ${name}`, worst(sub(got, want)) < tol, `${got.map((x) => x.toFixed(4)).join(" / ")} against ${want.map((x) => x.toFixed(4)).join(" / ")}`);
  for (const k of ["later_bn", "g3_rate_bn"]) {
    gate(`item 4 leaves the added people's ${k.replace("_bn", "")} part unchanged (${w}, 1e-9)`, worst(sub(V6[w][k], NF[w][k])) < 1e-9,
      `max |diff| ${worst(sub(V6[w][k], NF[w][k])).toExponential(1)}`);
  }
}
const pub = { later: [8541, 11731], g3_rate: [5052, 7133], added: [6309, 8790], union_member: [9353, 10950] };
const r = (bn, n) => bn.map((x) => Math.round(x * 1e9 / n));
gate("v5's published figures (set): later $8,541 / 11,731, G3-rate $5,052 / 7,133, +$18.9 / +26.4bn, $6,309-8,790 per added person, $9,353-10,950 per union member",
  JSON.stringify(r(V5.set.later_bn, counts.later)) === JSON.stringify(pub.later) && JSON.stringify(r(V5.set.g3_rate_bn, counts.g3_rate)) === JSON.stringify(pub.g3_rate)
  && JSON.stringify(V5.set.lineage_addition_bn.map((x) => x.toFixed(1))) === JSON.stringify(["18.9", "26.4"])
  && JSON.stringify(r(V5.set.added_bn, counts.added)) === JSON.stringify(pub.added)
  && JSON.stringify(r(V5.set.union_only_bn, counts.account_union)) === JSON.stringify(pub.union_member),
  `${usd(r(V5.set.later_bn, counts.later))}; ${usd(r(V5.set.g3_rate_bn, counts.g3_rate))}; ${V5.set.lineage_addition_bn.map((x) => x.toFixed(1)).join(" / ")}; ${usd(r(V5.set.added_bn, counts.added))}; ${usd(r(V5.set.union_only_bn, counts.account_union))}`);

const failed = GATES.filter((g) => !g.pass).length;
if (failed) { console.error(`[BLOCKED] ${failed} gate(s) failed; nothing written`); process.exit(1); }

// ---------------------------------------------------------------------------------------------------
const per = (bn, n) => bn.map((x) => x * 1e9 / n);
function setOut(w) {
  const x = V6[w], y = V5[w];
  const part = (k, n) => ({ persons: n, cost_bn: x[k], per_person_usd: per(x[k], n), on_v5_cost_bn: y[k], on_v5_per_person_usd: per(y[k], n), items_change_bn: sub(x[k], y[k]) });
  return {
    case_bn: x.case_bn, per_member_usd: per(x.case_bn, counts.lineage_population),
    parts: { later: part("later_bn", counts.later), g3_rate: part("g3_rate_bn", counts.g3_rate), added: part("added_bn", counts.added) },
    union_response_bn: x.union_response_bn, union_response_on_v5_bn: y.union_response_bn,
    union_at_case_responses_bn: x.union_at_case_responses_bn,
    lineage_addition_bn: x.lineage_addition_bn, lineage_addition_on_v5_bn: y.lineage_addition_bn,
    union_only: { cost_bn: x.union_only_bn, per_member_usd: per(x.union_only_bn, counts.account_union), members: counts.account_union,
      on_v5_cost_bn: y.union_only_bn, on_v5_per_member_usd: per(y.union_only_bn, counts.account_union),
      rule: "v6 without the lineage: the September 29 union with items pension_tr2026 (its union parts), retiree_health and user_fees at the union's own responses" },
  };
}
const OUT_JSON = {
  meta: {
    lane: P.V6.LANE, script: "lineage_addition.cjs", case: P.correctionsPayload().meta.status, ends: ENDS, ends_rule: "each figure is the two methods' mean at specifications 48 (low) and 11 (high), the case's ends in both methods",
    counts,
    parts_rule: "at the case's responses: later = C(l, g) - C(0, g), G3-rate = C(l, g) - C(l, 0), each with items 1-3's parts on those people (item 3's age mix, item 1's lineage_oasdi and lineage_part_a, item 2's scaling of their cells); item 4 is union-only and leaves them unchanged (gated)",
    union_rule: "U = C(l, 0) + C(0, g) - C(l, g), the cost with nobody added (the cost is affine in the counts at fixed responses, gated); at the case's responses the union there, at the union's own the union-only case; the union's response is the first less the second",
    addition_rule: "the lineage's addition = v6 less the union-only case = the added people + the union's response",
    responses: { case: { s: AT.case.s, k_metro: AT.case.k_metro }, union: { s: AT.union.s, k_metro: AT.union.k_metro } },
    route: "package.cjs caseOf at lineage options built by lineage_count.cjs additionsAt (its lineageBase() and caseOf() repeated here for options it does not name)",
    inputs: Object.fromEntries([`${P.V6.LANE}/package.cjs`, `${P.V6.LANE}/lineage_count.cjs`, `${P.V6.LANE}/item_age_mix.cjs`, `${P.V6.LANE}/item_user_fees.cjs`,
      `${P.V6.LANE}/derived/corrections.json`, `${P.V6.LANE}/derived/corrections_cash.json`, `${P.V6.LANE}/derived/summary.json`, V5_SUMMARY].map((f) => [f, sha(f)])),
  },
  set: setOut("set"),
  cash: setOut("cash"),
  gates: GATES,
};
fs.writeFileSync(OUT, JSON.stringify(OUT_JSON, null, 1) + "\n");

console.log(`\n[figures at specifications 48 / 11; ${GATES.length} gates pass]`);
for (const w of SETS) {
  const o = OUT_JSON[w];
  console.log(`  ${w}: v6 ${f3(o.case_bn)} (${usd(o.per_member_usd)} per member of ${(counts.lineage_population / 1e6).toFixed(2)}M)`);
  for (const k of ["later", "g3_rate", "added"]) {
    const p = o.parts[k];
    console.log(`    ${k.padEnd(8)} ${(p.persons / 1e6).toFixed(4)}M  ${f3(p.cost_bn)}bn  ${usd(p.per_person_usd)} per person (v5 ${usd(p.on_v5_per_person_usd)}; items ${f3(p.items_change_bn)})`);
  }
  console.log(`    union's response ${f3(o.union_response_bn)} (v5 ${f3(o.union_response_on_v5_bn)})`);
  console.log(`    lineage's addition ${f3(o.lineage_addition_bn)} (v5 ${f3(o.lineage_addition_on_v5_bn)})`);
  console.log(`    union-only case ${f3(o.union_only.cost_bn)}: ${usd(o.union_only.per_member_usd)} per member of ${(counts.account_union / 1e6).toFixed(2)}M (v5's ${usd(o.union_only.on_v5_per_member_usd)})`);
}
console.log(`  wrote ${OUT}`);
