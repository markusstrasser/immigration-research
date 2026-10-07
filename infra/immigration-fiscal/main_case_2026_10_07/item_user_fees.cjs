/* Item user_fees of the v6 registry (package.cjs), an edit set: user fees and the education keys
 * (user_fee_allocation_2026_10_07, committed 81bd22da), every part of that lane but transit, on the union (the
 * identified 39.71M).
 *
 * The lane prices on v5, at its 64 specifications and both sets: five synthetic engine lines at response 1 (fee_tuition,
 * key_higher_ed, fee_health, key_health, key_pell; each parent line responds at 1 at every specification, gated there)
 * and three post-engine terms: the K-12 weight, A + B s at the education line's response (s the school fraction), and
 * the college and K-12 capital keyed by use, stock x rate x response x (key_target - key_union). Transit (key_transit
 * and capital_transit) is left out: v3's item 8 tested the same object at the same ACS ratio, and weighted by where the
 * deficit falls the riders' key is 1.019 times the population key, held beside in v4
 * (decisions/2026-09-29-main-case-v4.md, rejected 4).
 *
 * Here the engine lines fold into their parent lines' cells, and the K-12 weight into row 6's re-blend lines, so a
 * consumer that reads lines by id finds them on education, health and other federal benefits:
 *   0  education_services / education_mix   fee_tuition + key_higher_ed
 *   1  school_reprice / k                    the K-12 weight's school part, A + B
 *   2  college_rekey / k                     the K-12 weight's other part, A
 *   3  health_services / health_other        fee_health + key_health
 *   4  other_federal_benefits / all_cash     key_pell
 * Edits 1 and 2 are row 6's re-blend at BEA's K-12 weight w_K (0.7748) in place of W (0.795). Row 6's school and
 * college edits are linear in W, f (n hf (W k K + (1 - W) P) - T0) and f (n hf (W K + (1 - W) P) - T0), so moving W
 * moves them by n (w_K - W)(k K_eff - P_eff) = A + B and n (w_K - W)(K_eff - P_eff) = A (gated against the lane's A
 * and B). At the case's school response (1 at every specification) they cost s (A + B) + (1 - s) A = A + B s, the
 * lane's term; under another school response r they respond as row 6's lines do, s r (A + B) + (1 - s) A, where the
 * lane writes (A + B s)(s r + 1 - s). Edit 0 responds at the education line's response, s r + 1 - s, 1 in the case.
 *
 * The capital. Four capital components read lines these edits move: k12 and college the education line's amount
 * (with school_reprice and college_rekey), health_sl and health_fed the health line's. In the lane the engine lines are
 * lines of their own, so no capital key moves with them, and the college and K-12 keys move by the lane's key change.
 * Here each of the four gets an offset component beside it (its stock, part, level, BEA source and response), keyed by
 * a carrier receipt line whose amount over its national total is
 *   v = (key_target - key_union) [college and k12; 0 for health] - (the item's edits on the component's key lines) / N,
 * N the national total of the key's denominator line in the model the item applies to. The component and its offset
 * then give stock x rate x response x (the component's key without the item + key_target - key_union) on any model:
 * the K-12 and college stocks keyed by use and the health stocks unmoved, as the lane prices them. A carrier is a
 * receipt line of national total 1e-9 bn (one dollar) at the engine's indirect response (0): its amounts are below
 * every tolerance of any sum, and it adds nothing to the cost. An option that re-keys a target component (the
 * k12_capital_at_pupil_share variant) drops that component's offset.
 *
 * Union only: the edits are the lane's amounts for the identified 39.71M, and the 3.04M added people keep their v5
 * (or lineage item's) pricing, their part of each capital key the line's. At the union's per-member terms they would
 * add (lineage / union - 1) x the change, about -0.02 / -0.06bn at the ends (meta.user_fees.union_only).
 *
 * build(ctx, arm, which) returns the edit set package.cjs checks (checkBuilt): edits, parts, meta.user_fees, record,
 * detail, and capital {carriers, receiptLinesAt(m), zeroLines(m), componentsFor(comps, caseComps), checkEvaluation(ev)}.
 * Run nothing: a module.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.join(__dirname, "..");
const LANE = "user_fee_allocation_2026_10_07";
const COMMIT = "81bd22da";
const FILES = {
  fee_lines: `${LANE}/derived/fee_lines.json`, case: `${LANE}/derived/case_oct05.json`, per_spec: `${LANE}/derived/case_oct05.csv`,
  case_script: `${LANE}/case.cjs`, builder: `${LANE}/fee_lines.py`,
};
const V5_SUMMARY = "main_case_2026_10_05/derived/summary.json";
const ALLOCS = ["personal", "shared"];
const ENDS = { low: 48, high: 11 };
const TAKEN = { lines: ["fee_tuition", "key_higher_ed", "fee_health", "key_health", "key_pell"], post_engine: ["k12_weight_bn", "capital_college_bn", "capital_k12_bn"] };
const LEFT_OUT = {
  lines: ["key_transit"], post_engine: ["capital_transit_bn"],
  why: "the transit terms repeat v3's item 8, which tested the same object at the same ACS ratio: weighted by where the deficit falls, the riders' key is 1.019 times the population key (SE 0.017), held beside in v4 (decisions/2026-09-29-main-case-v4.md, rejected 4)",
};
// The edits, in order, with the parts each adds.
const EDITS = [
  { line: "education_services", key: "education_mix", parts: ["fee_tuition", "key_higher_ed"] },
  { line: "school_reprice", key: "k", parts: ["k12_weight_school"] },
  { line: "college_rekey", key: "k", parts: ["k12_weight_other"] },
  { line: "health_services", key: "health_other", parts: ["fee_health", "key_health"] },
  { line: "other_federal_benefits", key: "all_cash", parts: ["key_pell"] },
];
const PARENT = { fee_tuition: "education_services", key_higher_ed: "education_services", fee_health: "health_services", key_health: "health_services",
  key_pell: "other_federal_benefits" };
// The line that splits a part across generations and households where it is not the part's parent line: the K-12
// weight's parts, because the consumers carry no generation amounts for row 6's re-blend lines, and Pell, which goes to
// students: its parent line, other_federal_benefits, is keyed by cash assistance and would put it on cash-assistance
// recipients, and no consumer has a college-enrollment key by person (decisions/2026-10-07-main-case-v6.md).
const SPLIT_OVER = { k12_weight_school: "education_services", k12_weight_other: "education_services", key_pell: "education_services" };
// The capital: the lane's re-keyed components, and the carrier of each component whose key reads an edited line.
const REKEY = { college: "college_capital", k12: "k12_capital" };
const CARRIERS = { user_fees_key_k12: ["k12"], user_fees_key_college: ["college"], user_fees_key_health: ["health_sl", "health_fed"] };
const CARRIER_NATIONAL_BN = 1e-9;
const OFFSET_SUFFIX = "_user_fees";
// A part's name in meta.items: the lane's term with the union_ prefix.
const PART = (term) => `union_${term}`;

const clone = (x) => JSON.parse(JSON.stringify(x));
const readRel = (rel) => fs.readFileSync(path.join(FISCAL, rel), "utf8");
const readJson = (rel) => JSON.parse(readRel(rel));
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const blocked = (why) => { throw new Error("[BLOCKED] item user_fees: " + why); };
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const byAlloc = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));

function csvRows(rel) {
  const [h, ...rows] = readRel(rel).trim().split("\n").map((l) => l.split(","));
  return rows.map((r) => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}
// The lane's change at its ends with every part but transit, from case_oct05.json (sets.{case,cash}.ends).
function changeAtEnds(K, set) {
  return ["low", "high"].map((end) => {
    const E = K.sets[set].ends[end];
    if (E.spec !== ENDS[end]) blocked(`case_oct05.json's ${set} ${end} end is specification ${E.spec}, not ${ENDS[end]}`);
    const lines = Object.entries(E.lines_bn).filter(([k]) => !LEFT_OUT.lines.includes(k));
    if (JSON.stringify(lines.map(([k]) => k).sort()) !== JSON.stringify(TAKEN.lines.slice().sort())) blocked("case_oct05.json's engine lines are not the five taken and key_transit");
    return lines.reduce((t, [, v]) => t + v, 0) + TAKEN.post_engine.reduce((t, k) => t + E.post_engine_bn[k], 0);
  });
}

function build(ctx, arm, which) {
  if (arm) blocked(`no arm ${arm}`);
  if (!["set", "cash"].includes(which)) blocked(`no set ${which}`);
  const { B, OCT05, Engine, MODEL } = ctx;
  const F = readJson(FILES.fee_lines), K = readJson(FILES.case), S5 = readJson(V5_SUMMARY);
  const lset = which === "set" ? "case" : "cash";
  const band5 = which === "set" ? S5.main_case : S5.cash_set.band_bn;
  // The lane ran on v5.
  if (!(K.sets.case.band_bn.every((x, e) => near(x, S5.main_case[e], 1e-9)) && K.sets.cash.band_bn.every((x, e) => near(x, S5.cash_set.band_bn[e], 1e-9)))) {
    blocked(`${FILES.case} was not run on v5 (its bands differ from ${V5_SUMMARY}'s)`);
  }
  for (const [id, parent] of Object.entries(PARENT)) if (!F.engine_lines[id] || F.engine_lines[id].parent !== parent) blocked(`fee_lines.json's ${id} has no parent ${parent}`);
  const api = which === "set" ? B : B.CASH, api5 = which === "set" ? OCT05 : OCT05.CASH;

  // The union reads, on the base payload's first edits (the September 29 payload's, before the lineage's): v5's, and the
  // base's (a lineage item replaces the lineage block only).
  const unionModel = (q) => {
    const p = q.correctionsPayload(), first = p.meta.lineage.edits.first;
    return { p, first, m: Engine.applyCorrections(MODEL, Object.assign({}, p, { edits: p.edits.slice(0, first) })) };
  };
  const u5 = unionModel(api5), u = unionModel(api);
  if (u.first !== u5.first || JSON.stringify(u.p.edits.slice(0, u.first)) !== JSON.stringify(u5.p.edits.slice(0, u5.first))) blocked("the base's first edits are not v5's");
  const cellOf = (m, key, a) => {
    const [side, rest] = key.split(":");
    if (side === "receipt") return m.receipts.lines.find((l) => l.id === rest).cells[m.receipts.reference][a].target_bn;
    const [line, k] = rest.split("/");
    return m.spending.lines.find((l) => l.id === line).keys[k][a].target_bn;
  };
  for (const [key, want] of Object.entries(F.union_reads)) for (const a of ALLOCS) {
    if (!near(cellOf(u.m, key, a), want[a], 1e-9)) blocked(`fee_lines.json's union read ${key} (${a}) is not the base's: ${cellOf(u.m, key, a)} against ${want[a]}`);
  }

  // The K-12 weight is row 6's re-blend at BEA's K-12 weight.
  const EK = F.education_key, n = F.nipa.education_line_bn, hf = F.frames.household_fraction, kw = F.post_engine.key_k12_weight;
  const wK = F.nipa.weights[kw.central].k12, W = EK.W, AB = kw.by_weights[kw.central];
  const N_EDU = u.m.spending.lines.find((l) => l.id === "education_services").national_bn;
  if (!near(N_EDU, n, 1e-9)) blocked("the education line's national total is not the lane's");
  for (const a of ALLOCS) {
    const x = EK.by_allocation[a];
    const school = (w) => x.f * (n * hf * (w * x.k * x.K_cps + (1 - w) * x.P_cps) - x.T0), college = (w) => x.f * (n * hf * (w * x.K_cps + (1 - w) * x.P_cps) - x.T0);
    if (!(near(school(W), x.school_edit_bn, 1e-9) && near(college(W), x.college_edit_bn, 1e-9)
      && near(x.school_edit_bn, F.union_reads["spending:school_reprice/k"][a], 1e-12) && near(x.college_edit_bn, F.union_reads["spending:college_rekey/k"][a], 1e-12))) {
      blocked(`row 6's edits (${a}) are not f (n hf (W k K + (1 - W) P) - T0) and f (n hf (W K + (1 - W) P) - T0) at the lane's inputs`);
    }
    if (!(near(school(wK) - school(W), AB[a].A + AB[a].B, 1e-9) && near(college(wK) - college(W), AB[a].A, 1e-9))) {
      blocked(`the K-12 weight's A and B (${a}) are not row 6's re-blend moved from W ${W} to w_K ${wK}`);
    }
  }

  // The edits and their parts.
  const line = (id) => F.engine_lines[id].by;
  const partBy = {
    fee_tuition: line("fee_tuition"), key_higher_ed: line("key_higher_ed"),
    k12_weight_school: byAlloc((a) => AB[a].A + AB[a].B), k12_weight_other: byAlloc((a) => AB[a].A),
    fee_health: line("fee_health"), key_health: line("key_health"), key_pell: line("key_pell"),
  };
  const m0 = api.payloadModel();
  for (const d of EDITS) {
    const l = m0.spending.lines.find((x) => x.id === d.line);
    if (!l || !l.keys[d.key] || l.preferred_key !== d.key) blocked(`the base model does not key ${d.line} by ${d.key}`);
  }
  const edits = EDITS.map((d) => ({ side: "spending", line: d.line, key: d.key, by: byAlloc((a) => d.parts.reduce((t, p) => t + partBy[p][a], 0)) }));
  // meta.items names each part union_<term>, the convention of item pension_tr2026's union_ and lineage_ parts (every
  // part here is the union's), with the lane's term, the line and the key of the edit it is in.
  const parts = Object.fromEntries(EDITS.flatMap((d, k) => d.parts.map((p) => [PART(p), { edit: k, by: clone(partBy[p]), term: p, line: d.line, key: d.key }])));

  // The capital: the components whose keys read an edited line are the carriers' four, each keyed by its lines' amount.
  const caseComps = api.componentsFor(null);
  const edited = new Set(edits.map((e) => e.line));
  const reads = (c) => (c.key.kind === "lines_amount_over_national" ? c.key.numerator_lines.concat([c.key.denominator_line]).some((x) => edited.has(x))
    : c.key.kind === "part_rekeyed" ? [c.key.parent_line, c.key.correction_line].some((x) => edited.has(x)) : false);
  const hit = caseComps.filter(reads).map((c) => c.id);
  const grouped = Object.values(CARRIERS).flat();
  if (JSON.stringify(hit.slice().sort()) !== JSON.stringify(grouped.slice().sort())) blocked(`the capital components that read the edited lines are ${hit.join(", ")}, not ${grouped.join(", ")}`);
  for (const [id, ids] of Object.entries(CARRIERS)) {
    const keys = ids.map((c) => JSON.stringify(caseComps.find((x) => x.id === c).key));
    if (keys.some((k) => k !== keys[0]) || caseComps.find((x) => x.id === ids[0]).key.kind !== "lines_amount_over_national") blocked(`carrier ${id}'s components do not share one lines key`);
    if (ids.some((c) => c in REKEY) && ids.length !== 1) blocked(`carrier ${id} carries a re-keyed component with others`);
  }
  // The lane's union keys are the case's union keys, (the union's education amount + row 6's edit) / N.
  const eduU = F.union_reads["spending:education_services/education_mix"];
  const unionKey = { college: byAlloc((a) => (eduU[a] + F.union_reads["spending:college_rekey/k"][a]) / N_EDU),
    k12: byAlloc((a) => (eduU[a] + F.union_reads["spending:school_reprice/k"][a]) / N_EDU) };
  for (const [c, blockName] of Object.entries(REKEY)) for (const a of ALLOCS) {
    if (!near(F.post_engine[blockName].key_union[a], unionKey[c][a], 1e-12) || F.post_engine[blockName].component !== c) blocked(`the lane's ${c} key_union (${a}) is not the case's union key`);
  }
  const delta = Object.fromEntries(Object.entries(REKEY).map(([c, blockName]) => [c, byAlloc((a) => F.post_engine[blockName].key_target[a] - F.post_engine[blockName].key_union[a])]));
  const keyOfCarrier = (id) => caseComps.find((x) => x.id === CARRIERS[id][0]).key;
  // The item's own move of a lines key on model m: its edits on the key's lines (at their preferred keys) over N.
  function induced(m, key) {
    const N = m.spending.lines.find((l) => l.id === key.denominator_line).national_bn;
    return byAlloc((a) => edits.filter((e) => key.numerator_lines.includes(e.line)).reduce((t, e) => {
      const l = m.spending.lines.find((x) => x.id === e.line);
      if (!l || l.preferred_key !== e.key) blocked(`the model does not key ${e.line} by ${e.key}`);
      return t + e.by[a];
    }, 0) / N);
  }
  const valuesAt = (m) => Object.fromEntries(Object.keys(CARRIERS).map((id) => {
    const c = CARRIERS[id][0], d = delta[c] || byAlloc(() => 0), ind = induced(m, keyOfCarrier(id));
    return [id, byAlloc((a) => d[a] - ind[a])];
  }));
  // At zero (zeroLines, for models without the item) every amount and share is 0 and the national total stays, so the
  // offsets' keys read 0, not 0 / 0.
  const carrierLine = (m, id, v, zero) => ({ id, national_bn: CARRIER_NATIONAL_BN, cells: Object.fromEntries(m.receipts.scenarios.map((sc) => [sc, byAlloc((a) => ({
    direct: false, key: "capital_key_offset", response_class: "capital_key_carrier",
    target_bn: zero ? 0 : v[a] * CARRIER_NATIONAL_BN, other_bn: zero ? 0 : CARRIER_NATIONAL_BN - v[a] * CARRIER_NATIONAL_BN, share: zero ? 0 : v[a] }))])) });
  const receiptLinesAt = (m) => { const v = valuesAt(m); return Object.keys(CARRIERS).map((id) => carrierLine(m, id, v[id], false)); };
  const zeroLines = (m) => Object.keys(CARRIERS).map((id) => carrierLine(m, id, null, true));
  const carrierOf = Object.fromEntries(Object.entries(CARRIERS).flatMap(([id, ids]) => ids.map((c) => [c, id])));
  const LABEL = {
    k12: "item user_fees: the K-12 stock keyed by its use key (the K-12 key at the school price), less the move the item's education edits give the line's key",
    college: "item user_fees: the college stock keyed by its use key (kappa U + (1 - kappa) P), less the move the item's education edits give the line's key",
    health_sl: "item user_fees: the move the item's health edits give the health key, taken back (the lane keeps the health stocks at their key)",
    health_fed: "item user_fees: the move the item's health edits give the health key, taken back (the lane keeps the health stocks at their key)",
  };
  // The offsets for a list of components (an option's): each component the case's own key still keys, in its order.
  function componentsFor(comps, caseC) {
    return comps.filter((t) => t.id in carrierOf).filter((t) => {
      const t0 = caseC.find((x) => x.id === t.id);
      return t0 && JSON.stringify(t.key) === JSON.stringify(t0.key);
    }).map((t) => ({ id: t.id + OFFSET_SUFFIX, label: LABEL[t.id], part: t.part, level: t.level, bea_source: t.bea_source, stock_charged_bn: t.stock_charged_bn,
      key: { kind: "receipt_amount_over_national", line: carrierOf[t.id],
        note: `carrier ${carrierOf[t.id]}: ${t.id in REKEY ? "key_target - key_union" : "0"} less the item's edits on ${t.key.numerator_lines.join(" and ")} over ${t.key.denominator_line}'s national total` },
      response: clone(t.response), of_component: t.id }));
  }
  // The evaluation keys the edited lines by the item's keys (an option that keys them otherwise has no rule here).
  function checkEvaluation(ev) {
    for (const e of edits) {
      const r = ev.spending.find((x) => x.id === e.line);
      if (!r || r.key !== e.key) blocked(`the evaluation keys ${e.line} by ${r ? r.key : "nothing"}, not ${e.key}, which the item edits`);
    }
  }

  // What the lane gives, every part but transit.
  const change = changeAtEnds(K, lset);
  const transit = ["low", "high"].map((end) => ({ key_transit_bn: K.sets[lset].ends[end].lines_bn.key_transit, capital_transit_bn: K.sets[lset].ends[end].post_engine_bn.capital_transit_bn }));
  const scale = F.frames.lineage_scale;
  const cases = csvRows(FILES.per_spec).filter((r) => r.set === lset);
  if (cases.length !== 64 || cases.some((r, i) => Number(r.spec) !== i)) blocked(`${FILES.per_spec} lacks the 64 specifications of set ${lset}`);
  const perSpec = cases.map((r) => Number(r.total_change_bn) - Number(r.key_transit_bn) - Number(r.capital_transit_bn));
  const block = {
    rule: "user fees and the education keys on the union, every part of the user-fee lane but transit: its five engine lines folded into their parent lines' cells (education_services, health_services, other_federal_benefits) at the lines' preferred keys, the K-12 weight as row 6's re-blend at BEA's weight (school_reprice and college_rekey), and the college and K-12 capital keyed by use through offset components keyed by carrier receipt lines",
    edits: EDITS.map((d, k) => ({ edit: k, line: d.line, key: d.key, parts: d.parts.map(PART), terms: d.parts.slice() })),
    engine_lines: Object.fromEntries(TAKEN.lines.map((id) => [id, { label: F.engine_lines[id].label, parent: F.engine_lines[id].parent, by: clone(F.engine_lines[id].by) }])),
    k12_weight: {
      rule: "row 6's re-blend at BEA's K-12 weight: its school and college edits move by n (w_K - W)(k K_eff - P_eff) = A + B and n (w_K - W)(K_eff - P_eff) = A; at the case's school response they cost A + B s, the lane's term",
      weight: kw.central, w_K: wK, W, A_B: clone(AB),
      arms_not_wired: Object.fromEntries(Object.keys(kw.by_weights).filter((k) => k !== kw.central).map((k) => [k, { w_K: F.nipa.weights[k].k12, A_B: clone(kw.by_weights[k]) }])),
    },
    capital: {
      rule: "each capital component whose key reads an edited line gets an offset component beside it (its stock, part, level, BEA source and response), keyed by a carrier receipt line whose amount over its national total is key_target - key_union (college, k12; 0 for the health components) less the item's edits on the component's key lines over the denominator line's national total in the model the item applies to: the college and K-12 stocks keyed by use, the health stocks unmoved",
      rekeyed: Object.fromEntries(Object.entries(REKEY).map(([c, blockName]) => [c, { key_target: clone(F.post_engine[blockName].key_target), key_union: clone(F.post_engine[blockName].key_union),
        change: clone(delta[c]), rule: F.post_engine[blockName].rule }])),
      carriers: Object.fromEntries(Object.entries(CARRIERS).map(([id, ids]) => [id, { components: ids.slice(), offsets: ids.map((c) => c + OFFSET_SUFFIX), national_bn: CARRIER_NATIONAL_BN,
        parent_line: keyOfCarrier(id).denominator_line }])),
      carrier_rule: "a receipt line of national total 1e-9 bn at the engine's indirect response (0): its amounts are below every tolerance of any sum, and it adds nothing to the cost; its amount over its national total is the offset's key",
      options: "an option that re-keys a target component (k12_capital_at_pupil_share) drops that component's offset; the offsets take the option's stock and response",
    },
    excluded: { engine_lines: LEFT_OUT.lines.slice(), post_engine: LEFT_OUT.post_engine.slice(), why: LEFT_OUT.why, lane_at_ends_bn: transit },
    union_only: {
      rule: "the edits and carriers are the lane's amounts for the union, the identified 39.71M; the 3.04M added people keep their v5 or lineage item's pricing, and their part of each capital key stays the line's",
      lineage_scale: scale,
      added_people_at_union_terms_bn: change.map((x) => (scale - 1) * x),
      limit: "at the union's per-member terms the added people would add (lineage / union - 1) x the change at each end; not counted",
    },
    splits: {
      generation: "union-only: split each edit's parts, and each carrier's offset (its cells' target and share), across the union's generations pro rata to each generation's share of its split-basis line's union amount at the line's preferred key (split_basis: education_services for union_fee_tuition, union_key_higher_ed, union_key_pell, the K-12 weight parts and the k12 and college carriers; health_services for union_fee_health, union_key_health and the health carrier); G3+'s added people take none",
      household_person: "pro rata to the split-basis line's amount in the household or person, within the union (split_basis)",
      basis_rule: "a part's split-basis line is its parent line except for the K-12 weight's parts, because the consumers carry no generation amounts for row 6's re-blend lines, and union_key_pell, because Pell goes to students: its parent line, other_federal_benefits, is keyed by cash assistance and would put it on cash-assistance recipients, and no consumer has a college-enrollment key by person (decisions/2026-10-07-main-case-v6.md)",
      split_basis: Object.assign(Object.fromEntries(TAKEN.lines.map((id) => [PART(id), PARENT[id]])),
        Object.fromEntries(Object.entries(SPLIT_OVER).map(([term, line]) => [PART(term), line])),
        Object.fromEntries(Object.keys(CARRIERS).map((id) => [id, keyOfCarrier(id).denominator_line]))),
    },
    school_response: "the folded terms respond at their lines' responses: edit 0 at the education line's s r + 1 - s, the K-12 weight parts at row 6's s r and 1 - s; at the case's school response 1 that is the lane's response 1 and A + B s; the lane's own form under another r is (A + B s)(s r + 1 - s) and response 1 for the engine lines",
    lane_change_at_ends_bn: change,
    source: { lane: LANE, commit: COMMIT, arm: "all_but_transit", files: Object.fromEntries(Object.entries(FILES).map(([k, f]) => [k, { file: f, sha256: sha256(f) }])) },
  };
  return {
    edits, parts, meta: { user_fees: block },
    record: {
      source_arm: "all_but_transit",
      rule: "the lane's five engine lines and K-12 weight as cell shifts on their parent lines (meta.user_fees.edits), its college and K-12 capital re-keys and the health keys' return as offset components keyed by carrier receipt lines (meta.user_fees.capital)",
      parts_rule: "each part is union_<term> for one of the lane's terms: union_fee_tuition, union_key_higher_ed, union_fee_health, union_key_health and union_key_pell (its engine lines), union_k12_weight_school and union_k12_weight_other (its K-12 weight, A + B and A); each names its edit, line and key and the lane's term; each edit's by is its parts' sum, in order; the capital terms are the offset components (capital_components)",
      split_rule: block.splits.generation,
      union_only: true,
      union_only_rule: block.union_only.rule,
      parent_lines: Object.fromEntries(EDITS.map((d) => [d.line, { key: d.key, parts: d.parts.map(PART) }])),
      capital_components: Object.fromEntries(grouped.map((c) => [c, { offset: c + OFFSET_SUFFIX, carrier: carrierOf[c], parent_line: keyOfCarrier(carrierOf[c]).denominator_line,
        rekeyed: c in REKEY, part: PART(`capital_${c}`) }])),
      carriers: Object.keys(CARRIERS), offsets: grouped.map((c) => c + OFFSET_SUFFIX),
      source_band_bn: band5.map((x, e) => x + change[e]), source_band_specs: [ENDS.low, ENDS.high], source_change_bn: change,
      source_rule: "the lane's v5 band plus every part but transit at its ends (case_oct05.json: the engine lines without key_transit, k12_weight_bn, capital_college_bn and capital_k12_bn)",
    },
    detail: { per_spec_change_bn: perSpec, partBy: clone(partBy), delta, A_B: clone(AB), carriers: clone(CARRIERS), offset_suffix: OFFSET_SUFFIX, change_at_ends_bn: change },
    capital: { carriers: Object.keys(CARRIERS), receiptLinesAt, zeroLines, componentsFor, checkEvaluation, offsets: grouped.map((c) => c + OFFSET_SUFFIX) },
  };
}

module.exports = { build, LANE, COMMIT, FILES, EDITS, CARRIERS, REKEY, TAKEN, LEFT_OUT, CARRIER_NATIONAL_BN, OFFSET_SUFFIX, changeAtEnds };
