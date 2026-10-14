/* Item child_credits of the v7 registry (package.cjs): the term the personal allocation still misses
 * (mixed_unit_credits_2026_10_14; research/immigration-v6-assumption-review-2026-10-14.md, "For the operator" item 1).
 * A non-member filer's child-related credits for member children sit on the non-member's record, and a removal would
 * end them; the reverse (member filers, non-member children whose claim continues) also exists. The lane measures both
 * on the identified union (39.71M, audit row 4), on its recommended reading (R3 with head-of-household status), and
 * states them as fixed cell shifts at the personal allocation (shared 0), in both sets, since credits are paid when
 * claimed.
 *
 *   edits    every one at shared 0: the receipt edit on federal_income_tax at each of the model's receipt scenarios, in
 *            its order, and the lane's spending edit on refundable_tax_credits. A receipt scenario's edit is the lane's
 *            reference edit (cbo_collective) times that scenario's union target on federal_income_tax over the
 *            reference's (model.json, the case's expand rule): the lane's own edits at its seven scenarios follow the
 *            rule (gated, 1e-12), and federal_gap_high_agi, where the lane computes no key, takes it [APPROX];
 *   parts    the lane's parts {name: {bn, cost_bn, line, side, generation}}, bn the change to the group's target on the
 *            line (a receipt part's bn is minus its cost): part p on edit j is union_<G>:<p>[:<scenario>] (the scenario
 *            where a line has more than one edit), {edit: j, by: {personal: bn x scale_j, shared: 0}}, scale_j the
 *            scenario's ratio (1 on the spending edit); lineage_g3plus:<line>[:<scenario>] the added people's. Each
 *            edit's by is its parts' sum (the union's gated against the lane's by, 1e-9), so consumers that split the case
 *            by generation route each part by its prefix;
 *   lineage  LINEAGE (the switch, on): the lane's G3+ term per member ($213.97: its G3+ net over the identified G3+) on
 *            the lineage's G3+-priced added people (later losses plus (1 - C3) of the G3-rate attriters,
 *            meta.lineage.members.g3plus), split across the two lines in G3+'s own receipt and spending proportions
 *            (item.json's G3plus parts); the white-priced added people take 0 [ASSUMPTION: not measured];
 *   arms     the lane's other readings (R1 and R2 with status, R3 without), each as the two side totals on the same
 *            edits, the added people's term in the central's G3+ proportions, without generation parts (whole-case
 *            variant rows);
 *   check    the spending edits less the reference scenario's receipt edits are the lane's net_bn plus the added
 *            people's term, each generation's parts its by_generation, each part's cost its sign rule (1e-9).
 *
 * build(ctx, arm, which) -> the edit set (package.cjs's contract). Run nothing: a module.
 */
"use strict";
const path = require("path");
const { sourceOf, tag } = require("./sources.cjs");
const V6 = require(path.join(__dirname, "..", "main_case_2026_10_07", "package.cjs"));

const ITEM = "child_credits";
// The switch for the added people: true prices the lane's G3+ term on the lineage's G3+-priced added people.
const LINEAGE = true;
const GENS = ["G1", "G2", "G3plus"];
const REF = "cbo_collective";
const clone = (x) => JSON.parse(JSON.stringify(x));
const blocked = (why) => { throw new Error(`[BLOCKED] item ${ITEM}: ${why}`); };
const isNum = (x) => typeof x === "number" && Number.isFinite(x);
// The lane writes personal-allocation amounts as {personal: x} (shared 0 by the contract).
const personalOf = (x, where) => {
  if (isNum(x)) return x;
  if (x && isNum(x.personal) && (x.shared === undefined || x.shared === 0)) return x.personal;
  return blocked(`${where} is not a personal amount ({personal}, shared absent or 0)`);
};
const lineKey = (e) => `${e.side}|${e.line}`;
const costOf = (p) => (p.side === "spending" ? p.bn : -p.bn);

const S = sourceOf(ITEM);
function read() {
  const I = S.data;
  const net = personalOf(I.net_bn, "net_bn");
  if (!I.by_generation) blocked("item.json has no by_generation");
  const byGen = Object.fromEntries(GENS.map((G) => [G, personalOf(I.by_generation[G], `by_generation.${G}`)]));
  const genSum = GENS.reduce((t, G) => t + byGen[G], 0);
  if (Math.abs(genSum - net) > 1e-9) blocked(`by_generation adds to ${genSum}, not net_bn ${net}`);
  if (!Array.isArray(I.edits) || !I.edits.length) blocked("item.json has no edits");
  const parts = Object.entries(I.parts || {});
  if (!parts.length) blocked("item.json has no parts");
  for (const [n, p] of parts) {
    if (!p || !isNum(p.bn) || typeof p.line !== "string" || !["receipt", "spending"].includes(p.side) || !GENS.includes(p.generation)) {
      blocked(`part ${n} is not {bn, line, side, generation (${GENS.join(", ")})}`);
    }
    if (p.cost_bn !== undefined && Math.abs(p.cost_bn - costOf(p)) > 1e-12) blocked(`part ${n}: cost_bn ${p.cost_bn} is not ${p.side === "receipt" ? "minus " : ""}its bn`);
  }
  for (const G of GENS) {
    const s = parts.filter(([, p]) => p.generation === G).reduce((t, [, p]) => t + costOf(p), 0);
    if (Math.abs(s - byGen[G]) > 1e-9) blocked(`${G}'s parts cost ${s}, not by_generation ${byGen[G]}`);
  }
  for (const e of I.edits) {
    const where = `edit ${JSON.stringify(e)}`;
    if (!["receipt", "spending"].includes(e.side) || typeof e.line !== "string" || !e.by || !isNum(e.by.personal) || e.by.shared !== 0) blocked(`${where}: not {side, line, scenario | key, by: {personal, shared: 0}}`);
    if (e.side === "receipt" ? typeof e.scenario !== "string" || "key" in e : typeof e.key !== "string" || "scenario" in e) blocked(`${where}: a ${e.side} edit names ${e.side === "receipt" ? "a scenario" : "a key"}`);
    if (!parts.some(([, p]) => lineKey(p) === lineKey(e))) blocked(`${where} has no parts on its line`);
  }
  for (const [n, p] of parts) if (!I.edits.some((e) => lineKey(e) === lineKey(p))) blocked(`part ${n} (${p.side} ${p.line}) has no edit`);
  // Per line: the reference edit (the receipt edit at the reference scenario, or the line's one spending edit), which
  // its parts must make.
  const lines = {};
  for (const k of [...new Set(I.edits.map(lineKey))]) {
    const es = I.edits.filter((e) => lineKey(e) === k), side = es[0].side;
    const ref = side === "receipt" ? es.find((e) => e.scenario === REF) : es.length === 1 ? es[0] : null;
    if (!ref) blocked(`${k}: no reference edit (${side === "receipt" ? `the receipt edit at ${REF}` : "one spending edit"})`);
    const total = parts.filter(([, p]) => lineKey(p) === k).reduce((t, [, p]) => t + p.bn, 0);
    if (Math.abs(total - ref.by.personal) > 1e-9) blocked(`${k}: the reference edit ${ref.by.personal} is not its parts' sum ${total}`);
    // G3+'s own amount on the line (its parts' bn): the added people's split across the lines.
    const g3 = parts.filter(([, p]) => lineKey(p) === k && p.generation === "G3plus").reduce((t, [, p]) => t + p.bn, 0);
    lines[k] = { side, line: es[0].line, total, ref, edits: es, g3 };
  }
  if (Object.values(lines).filter((x) => x.side === "receipt").length !== 1 || Object.values(lines).filter((x) => x.side === "spending").length !== 1) {
    blocked("the lane's edits are not one receipt line and one spending line (the arms give one total per side)");
  }
  // The arms: the lane's other readings, the side totals on the same edits.
  const arms = Object.fromEntries(Object.entries(I.arms || {}).map(([k, a]) => {
    const anet = personalOf(a.net_bn, `arms.${k}.net_bn`), ag = Object.fromEntries(GENS.map((G) => [G, personalOf(a.by_generation[G], `arms.${k}.by_generation.${G}`)]));
    const sides = a.edits_personal || {};
    if (!isNum(sides.receipt) || !isNum(sides.spending)) blocked(`arms.${k}: edits_personal lacks receipt or spending`);
    if (Math.abs(sides.spending - sides.receipt - anet) > 1e-9) blocked(`arms.${k}: its side totals net to ${sides.spending - sides.receipt}, not net_bn ${anet}`);
    if (Math.abs(GENS.reduce((t, G) => t + ag[G], 0) - anet) > 1e-9) blocked(`arms.${k}: by_generation does not add to net_bn`);
    return [k, { net_bn: anet, by_generation: ag, se_bn: a.se_bn ? personalOf(a.se_bn, `arms.${k}.se_bn`) : null, sides }];
  }));
  const g3net = Object.values(lines).reduce((t, x) => t + (x.side === "spending" ? x.g3 : -x.g3), 0);
  if (Math.abs(g3net - byGen.G3plus) > 1e-9) blocked(`G3+'s parts by line net to ${g3net}, not by_generation.G3plus ${byGen.G3plus}`);
  const lin = I.lineage || {};
  if (!isNum(lin.g3plus_per_member_usd) || !isNum(lin.identified_g3plus) || Math.abs(lin.g3plus_per_member_usd * lin.identified_g3plus / 1e9 - byGen.G3plus) > 1e-9) {
    blocked("item.json's lineage block is not G3+'s net per identified G3+ member");
  }
  return { I, net, byGen, parts, lines, arms };
}
const R = read();
const ARMS = Object.fromEntries(Object.keys(R.arms).map((k) => [k, { label: `the lane's reading ${k} (${R.arms[k].net_bn.toFixed(3)}bn on the union)`, source_arm: k }]));

// The lineage's G3+-priced added people and their ratio to the identified G3+ (on the case the item builds on).
function lineageScale(ctx) {
  const D = ctx.DETAIL && ctx.DETAIL.added_age_mix, B = ctx.B;
  if (!D || !D.counts) blocked("the added people's G3+ count comes from the lineage item added_age_mix's counts; a case without it has no rule here");
  const L = B.correctionsPayload().meta.lineage, I = R.I;
  const idG3 = I.lineage.identified_g3plus;
  if (Math.abs(idG3 - L.counts.identified_g3plus) > 1e-6) blocked(`the lane's identified G3+ (${idG3}) is not the case's (${L.counts.identified_g3plus})`);
  const n = D.counts.later + (1 - D.counts.c3) * D.counts.g3_rate;
  if (!(Math.abs(n - L.members.g3plus) <= 1e-6)) blocked(`the G3+-priced added people ${n} are not the case's meta.lineage.members.g3plus ${L.members.g3plus}`);
  return { added_g3plus_priced: n, identified_g3plus: idG3, scale: n / idG3, per_member_usd: I.lineage.g3plus_per_member_usd, counts: clone(D.counts) };
}

function build(ctx, arm, which) {
  const { B, MODEL } = ctx;
  if (MODEL.receipts.reference !== REF) blocked(`the model's reference scenario is ${MODEL.receipts.reference}, not ${REF}`);
  if (arm && !R.arms[arm]) blocked(`no arm ${arm} (${Object.keys(R.arms).join(", ")})`);
  const api = which === "set" ? B : B.CASH;
  const m = api.payloadModel();
  const { I, net, byGen, parts, lines } = R;
  const lin = LINEAGE ? lineageScale(ctx) : null;
  // The edits: each receipt line at every scenario of the model, by the case's rule (the reference edit times the
  // scenario's union target over the reference's on model.json, as V6.expand scales receipt shifts), then the spending line.
  const plan = [];
  let ruleGap = 0;
  const synthesized = [];
  for (const L of Object.values(lines)) {
    if (L.side === "spending") {
      for (const e of L.edits) plan.push({ L, e: { side: "spending", line: e.line, key: e.key }, scale: e.by.personal / L.ref.by.personal, suffix: L.edits.length > 1 ? `:${e.key}` : "" });
      continue;
    }
    const ml = MODEL.receipts.lines.find((l) => l.id === L.line);
    if (!ml) blocked(`model.json has no receipt line ${L.line}`);
    const ex = V6.expand([{ side: "receipt", line: L.line, by: { personal: L.ref.by.personal, shared: 0 } }]);
    for (const sc of MODEL.receipts.scenarios) {
      const t0 = ml.cells[REF].personal.target_bn, scale = t0 === 0 ? 1 : ml.cells[sc].personal.target_bn / t0;
      const given = L.edits.find((e) => e.scenario === sc), want = ex.find((e) => e.scenario === sc).by.personal;
      if (given) ruleGap = Math.max(ruleGap, Math.abs(given.by.personal - want));
      else synthesized.push({ line: L.line, scenario: sc, ratio: scale, by_personal: want });
      plan.push({ L, e: { side: "receipt", line: L.line, scenario: sc }, scale, suffix: `:${sc}`, given: given || null });
    }
  }
  if (!(ruleGap <= 1e-12)) blocked(`the lane's receipt edits do not follow the case's rule (the reference edit times each scenario's union target over the reference's): ${ruleGap}`);
  const outParts = {}, edits = [], scales = {};
  let byGap = 0;
  for (const { L, e, scale, suffix, given } of plan) {
    const has = e.side === "receipt" ? (m.receipts.lines.find((l) => l.id === e.line) || { cells: {} }).cells[e.scenario]
      : (m.spending.lines.find((l) => l.id === e.line) || { keys: {} }).keys[e.key];
    if (!has) blocked(`${which}: the model has no ${e.side} cell ${e.line}/${e.scenario || e.key}`);
    const at = e.scenario || e.key;
    scales[`${e.line}|${at}`] = scale;
    const by = { personal: 0, shared: 0 }, j = edits.length;
    if (arm) {
      // An arm: the side's total, scaled as the central's edit is, and the added people's term in the central's G3+ split.
      const A = R.arms[arm];
      by.personal = A.sides[e.side] * scale + (lin ? L.g3 * lin.scale * (A.by_generation.G3plus / byGen.G3plus) * scale : 0);
    } else {
      let union = 0;
      for (const [n, p] of parts) {
        if (lineKey(p) !== lineKey(L.ref)) continue;
        const name = `union_${p.generation}:${n}${suffix}`;
        if (name in outParts) blocked(`two parts named ${name}`);
        const v = p.bn * scale;
        outParts[name] = { edit: j, by: { personal: v, shared: 0 } };
        by.personal += v;
        union += v;
      }
      if (given) byGap = Math.max(byGap, Math.abs(union - given.by.personal));
      if (lin) {
        const v = L.g3 * lin.scale * scale;
        outParts[`lineage_g3plus:${e.line}${suffix}`] = { edit: j, by: { personal: v, shared: 0 } };
        by.personal += v;
      }
    }
    edits.push(Object.assign(clone(e), { by }));
  }
  if (!arm && !(byGap < 1e-9)) blocked(`the parts do not add to the lane's edits (${byGap})`);
  // The case's change at a personal specification with both lines at response 1: the spending edits less the
  // reference scenario's receipt edits.
  const change = edits.reduce((t, e) => t + (e.side === "spending" ? e.by.personal : e.scenario === REF ? -e.by.personal : 0), 0);
  const unionNet = arm ? R.arms[arm].net_bn : net, unionG3 = arm ? R.arms[arm].by_generation.G3plus : byGen.G3plus;
  const term = lin ? unionG3 * lin.scale : 0;
  const want = unionNet + term;
  if (Math.abs(change - want) > 1e-9) blocked(`the edits net to ${change} at ${REF}, not ${want} (the lane's net${lin ? " plus the added people's G3+ term" : ""})`);
  if (lin && !arm && Math.abs(term - lin.per_member_usd * lin.added_g3plus_priced / 1e9) > 1e-9) blocked(`the added people's term ${term} is not $${lin.per_member_usd} x ${lin.added_g3plus_priced}`);
  const block = {
    rule: "the child-related credits and head-of-household status that cross the group's boundary in mixed tax units, which the personal allocation misses: credits non-member filers claim for member children (a removal ends them) less credits member filers claim for non-member children whose claim continues; fixed cell shifts on the group's personal cells (shared 0), in both sets (credits are paid when claimed), each line responding at its case response (1); the receipt edit at every incidence rule is the reference edit times the rule's union target on federal_income_tax over the reference's",
    stub: S.stub,
    reading: arm || I.reading || null,
    reading_rule: I.reading_rule || null,
    sign: I.sign || null,
    scope: I.scope || null,
    net_bn: unionNet,
    se_bn: arm ? R.arms[arm].se_bn : I.se_bn ? personalOf(I.se_bn, "se_bn") : null,
    by_generation: clone(arm ? R.arms[arm].by_generation : byGen),
    edits: clone(I.edits),
    edits_note: I.edits_note || null,
    receipt_rule: { rule: "the lane's reference edit times each scenario's union target on federal_income_tax over the reference's (model.json), the case's expand rule; the lane's own edits at its scenarios follow it (1e-12)",
      synthesized: synthesized.map((x) => Object.assign({ tag: "[APPROX]", why: "the lane computes no key for this scenario" }, x)) },
    parts: arm ? null : clone(I.parts),
    scales: clone(scales),
    added_people: lin ? Object.assign({ applied: true, term_bn: term, rule: "the lane's G3+ term per member on the lineage's G3+-priced added people (later losses plus (1 - C3) of the G3-rate attriters, meta.lineage.members.g3plus), split across the two lines in G3+'s own receipt and spending proportions (item.json's G3plus parts); the white-priced added people take 0 [ASSUMPTION: not measured]",
      g3plus_by_line: Object.fromEntries(Object.values(lines).map((x) => [x.line, x.g3])) }, lin)
      : { applied: false, rule: "union only: the lane's lineage block would add its G3+ per-member term on the lineage's G3+-priced added people", lane: clone(I.lineage || null) },
    arms: Object.fromEntries(Object.entries(R.arms).map(([k, a]) => [k, { net_bn: a.net_bn, by_generation: clone(a.by_generation), se_bn: a.se_bn, edits_personal: clone(a.sides) }])),
    beside: clone(I.beside || null),
    source: { lane: S.lane, file: S.file, sha256: S.sha256, stub: S.stub, verdict: S.verdict },
  };
  const lineGates = Array.isArray(I.gates) ? I.gates : I.gates && typeof I.gates === "object" ? Object.values(I.gates) : [];
  return {
    edits, parts: outParts,
    meta: { child_credits: block },
    record: {
      stub: S.stub, source_net_bn: unionNet, source_by_generation_bn: clone(block.by_generation), reading: block.reading, added_people: !!lin, added_people_bn: term,
      rule: arm ? `item_child_credits.cjs: the lane's arm ${arm}, its side totals on the central's edits (no generation parts)`
        : "item_child_credits.cjs: the lane's edits on the group's personal cells, the receipt edit at every incidence rule by the case's rule, each edit's by the sum of its parts",
      parts_rule: arm ? "an arm carries no generation parts (a variant row)"
        : `every union part is the identified union's (39.71M): union_<G>:<lane part>[:<scenario>], routed to generation G${lin ? "; lineage_g3plus:<line>[:<scenario>] the added people's G3+-priced members (G3+'s amount on the line times their count over the identified G3+)" : "; the 3.04M added people take none (LINEAGE off)"}`,
      synthesized_scenarios: synthesized.map((x) => x.scenario),
      source_gates: { count: lineGates.length, all_passed: lineGates.length > 0 && lineGates.every((g) => g === true || (g && (g.passed === true || g.pass === true || g.ok === true))) },
      source: { file: S.file, sha256: S.sha256, verdict: S.verdict },
    },
    detail: { by_gap_bn: byGap, rule_gap_bn: ruleGap, scales, lineage: lin, synthesized },
  };
}

module.exports = { build, S, tag: () => tag(S), GENS, R, ARMS, LINEAGE };
