/* Item job_capital_taxes of the v7 registry (package.cjs): the taxes on the business capital that serves the group's
 * jobs (job_capital_taxes_2026_10_14; research/immigration-v6-assumption-review-2026-10-14.md, "For the operator" item
 * 2). Under the case's full-adjustment premise the capital that works with the group is not in the US without it, so the
 * taxes collected where that capital sits are lost on removal, while its owners keep the same after-tax return (P and F
 * do not move). Today the four lines respond at 0, the engine's default for indirect receipts, and the production
 * module's capital-tax term is 0 at retention 1.
 *
 * The item follows v4's precedent for personal_property_tax and tenant_occupied_property
 * (main_case_candidate_v4_2026_09_29/payload.cjs RESPONSE_NOTES): it re-keys the four lines at every receipt scenario and
 * adds four meta.responses entries (receipt: true, override "receipt:<line>", low and high the lane's two readings),
 * which every case specification's line_responses carries (package.cjs).
 *
 *   amounts   on each line L of the lane's line g (corporate: corporate_capital and corporate_labor; business_property:
 *             remaining_production_property; other_production_taxes), at each scenario sc and allocation a, the group's
 *             amount becomes J = sum of five parts, each times T / N_g (T the cell's total, target plus other; N_g the
 *             national of g's model lines, so the corporate lines share the lane's corporate amount by their cells and
 *             every scenario's corporate total is the same key times 663.685):
 *               union_G1, union_G2, union_G3plus  the lane's by_generation[G][g][a] (the identified 39.71M);
 *               lineage_g3plus, lineage_whites    the 3.04M added people: their share of the case's wage key
 *                                                 (corporate_labor at cbo_collective; the lineage item's part models
 *                                                 split it into the G3+ members and the whites as the lineage prices
 *                                                 them) times the lane's G3plus or white_nh factor for g times g's
 *                                                 national_bn;
 *   edits     one cell shift per line and scenario (32), by = new less old amounts part by part (the union's old
 *             amounts by generation from generation_account_2026_09_24's September 29 models, convention a; the added
 *             people's from the part models), summed in that order so the parts add to the edit exactly; the target is
 *             then J (gated, 1e-9) and national totals hold;
 *   editsAt   on another model (a fill-in method's, an option's): by = J - target on that model's cells, so the target
 *             is J on every model; on the model the item was built on it returns the built edits;
 *   responses corporate lines at the lane's corporate response, remaining_production_property at its business-property
 *             response r_b = 1 - lambda_b (1 - delta_L), other_production_taxes at 1 (gated). A line's response in the
 *             lane's file is a number (low = high) or {low, high}: low is the low end's reading (general government
 *             0.60), high the high end's.
 * Arms are the lane's arms (whole-case variant rows): the same blocks with another key, national or response. One more
 * block, CEILING, is no arm: the receipt lane's ceiling (receipt_side_long_run_2026_09_28 probe.json item 4) on the case's
 * frame, every group at the union's plain wage share (each generation at its share of the case's wage key, every factor
 * 1) and every line at response 1, for main_case.cjs's gate on the machinery.
 *
 * build(ctx, arm, which) -> the edit set (package.cjs's contract, with `responses`). Run nothing: a module.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { sourceOf, tag } = require("./sources.cjs");

const FISCAL = path.join(__dirname, "..");
const ITEM = "job_capital_taxes";
const GEN = "generation_account_2026_09_24/derived";
const GEN_FILES = { set: `${GEN}/generation_corrections_sept29.json`, cash: `${GEN}/generation_corrections_sept29_cash.json` };
const GENS = ["G1", "G2", "G3plus"];
const FACTORS = ["G1", "G2", "G3plus", "white_nh", "black_nh", "union"];
const GROUPS = { corporate: ["corporate_capital", "corporate_labor"], other_production_taxes: ["other_production_taxes"],
  business_property: ["remaining_production_property"] };
const LINE_GROUPS = Object.keys(GROUPS);
const MODEL_LINES = ["corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes"];
const GROUP_OF = Object.fromEntries(Object.entries(GROUPS).flatMap(([g, ls]) => ls.map((l) => [l, g])));
const WAGE = { line: "corporate_labor", key: "wage" };
const PARTS = ["union_G1", "union_G2", "union_G3plus", "lineage_g3plus", "lineage_whites"];
const ALLOCS = ["personal", "shared"];
const clone = (x) => JSON.parse(JSON.stringify(x));
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const blocked = (why) => { throw new Error(`[BLOCKED] item ${ITEM}: ${why}`); };
const isNum = (x) => typeof x === "number" && Number.isFinite(x);
const byAlloc = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(a)]));
const READINGS = ["low", "high"];
const readingsOf = (r, where) => {
  if (isNum(r)) return { low: r, high: r };
  if (r && isNum(r.low) && isNum(r.high)) return { low: r.low, high: r.high };
  return blocked(`${where} is neither a number nor {low, high}`);
};
const showReadings = (r) => (r.low === r.high ? `${r.low}` : `${r.low} low / ${r.high} high`);
const pair = (x, where) => {
  if (isNum(x)) return { personal: x, shared: x };
  if (!x || !ALLOCS.every((a) => isNum(x[a]))) blocked(`${where} is not {personal, shared}`);
  return { personal: x.personal, shared: x.shared };
};
// A figure that may differ by reading: {personal, shared} (the same at both) or {low: {personal, shared}, high: {...}}.
const pairByReading = (x, where) => {
  if (x && typeof x === "object" && "low" in x && "high" in x) return { low: pair(x.low, `${where}.low`), high: pair(x.high, `${where}.high`) };
  const p = pair(x, where);
  return { low: p, high: clone(p) };
};

// ---------------------------------------------------------------------------------------------------
// The lane's file: the contract (the v7 brief), read once.
const S = sourceOf(ITEM);
function readBlock(b, where, central) {
  if (!b || typeof b !== "object" || !b.lines || !b.by_generation || !b.factor) blocked(`${where} lacks lines, by_generation or factor`);
  const lines = Object.fromEntries(LINE_GROUPS.map((g) => {
    const x = b.lines[g];
    if (!x || !isNum(x.national_bn)) blocked(`${where}.lines.${g} lacks national_bn`);
    const out = { national_bn: x.national_bn, response: readingsOf(x.response, `${where}.lines.${g}.response`), key_share: pair(x.key_share, `${where}.lines.${g}.key_share`),
      group_bn: pair(x.group_bn, `${where}.lines.${g}.group_bn`), plain_wage_share: pair(x.plain_wage_share, `${where}.lines.${g}.plain_wage_share`) };
    for (const a of ALLOCS) {
      if (Math.abs(out.group_bn[a] - out.key_share[a] * out.national_bn) > 1e-9) blocked(`${where}.lines.${g}: group_bn is not key_share x national_bn (${a})`);
    }
    return [g, out];
  }));
  const byGen = Object.fromEntries(GENS.map((G) => [G, Object.fromEntries(LINE_GROUPS.map((g) => [g, pair((b.by_generation[G] || {})[g], `${where}.by_generation.${G}.${g}`)]))]));
  for (const g of LINE_GROUPS) for (const a of ALLOCS) {
    const s = GENS.reduce((t, G) => t + byGen[G][g][a], 0);
    if (Math.abs(s - lines[g].group_bn[a]) > 1e-9) blocked(`${where}: by_generation does not add to group_bn on ${g} (${a}: ${s} against ${lines[g].group_bn[a]})`);
  }
  const factor = Object.fromEntries(FACTORS.map((F) => [F, Object.fromEntries(LINE_GROUPS.map((g) => [g, pair((b.factor[F] || {})[g], `${where}.factor.${F}.${g}`)]))]));
  for (const g of LINE_GROUPS) for (const a of ALLOCS) {
    const want = lines[g].key_share[a] / lines[g].plain_wage_share[a];
    if (Math.abs(factor.union[g][a] - want) > 1e-9) blocked(`${where}: factor.union.${g} is not key_share / plain_wage_share (${a})`);
  }
  const op = lines.other_production_taxes.response;
  if (central && (op.low !== 1 || op.high !== 1)) blocked(`${where}: other_production_taxes responds at ${showReadings(op)}, not 1 (the brief)`);
  const central_bn = b.central_bn ? pairByReading(b.central_bn, `${where}.central_bn`) : null;
  // The lane's central is the sum over lines of the response at each reading times group_bn (its conventions).
  if (central) {
    if (!central_bn) blocked(`${where} lacks central_bn`);
    for (const r of READINGS) for (const a of ALLOCS) {
      const want = LINE_GROUPS.reduce((t, g) => t + lines[g].response[r] * lines[g].group_bn[a], 0);
      if (Math.abs(central_bn[r][a] - want) > 1e-9) blocked(`${where}: central_bn.${r}.${a} ${central_bn[r][a]} is not the sum of response x group_bn (${want})`);
    }
  }
  return { label: typeof b.label === "string" ? b.label : null, lines, by_generation: byGen, factor, central_bn, raw: b };
}
const I = S.data;
const CENTRAL = readBlock(I, "item.json", true);
const ARMS_IN = I.arms && typeof I.arms === "object" ? I.arms : {};
const ARMS = Object.fromEntries(Object.entries(ARMS_IN).map(([k, b]) => [k, { label: (b && b.label) || k, source_arm: k }]));
const CEILING = "__ceiling";
// The ceiling's block on the September 29 generation models: each generation's share of the case's wage key times each
// line's national, factors 1, responses 1.
function ceilingBlock(GM, U, REF) {
  const wc = lineOf(U, WAGE.line).cells[REF];
  const shareOf = (m) => byAlloc((a) => lineOf(m, WAGE.line).cells[REF][a].target_bn / totalOf(wc, a));
  const sG = Object.fromEntries(GENS.map((G) => [G, shareOf(GM[G])])), su = shareOf(U);
  const lines = Object.fromEntries(LINE_GROUPS.map((g) => {
    const N = CENTRAL.lines[g].national_bn;
    return [g, { national_bn: N, response: { low: 1, high: 1 }, key_share: clone(su), group_bn: byAlloc((a) => su[a] * N), plain_wage_share: clone(su) }];
  }));
  const one = Object.fromEntries(LINE_GROUPS.map((g) => [g, byAlloc(() => 1)]));
  return { label: "the receipt lane's ceiling on the case's frame: every group at its share of the case's wage key, every line at response 1 (no arm)", lines,
    by_generation: Object.fromEntries(GENS.map((G) => [G, Object.fromEntries(LINE_GROUPS.map((g) => [g, byAlloc((a) => sG[G][a] * lines[g].national_bn)]))])),
    factor: Object.fromEntries(FACTORS.map((F) => [F, clone(one)])), central_bn: null, raw: null, ceiling: { union_share: su, generation_shares: sG } };
}
const blockOf = (arm) => {
  if (!arm) return CENTRAL;
  if (!ARMS_IN[arm]) blocked(`no arm ${arm} (${Object.keys(ARMS_IN).join(", ")})`);
  return readBlock(ARMS_IN[arm], `item.json arms.${arm}`, false);
};

// ---------------------------------------------------------------------------------------------------
const lineOf = (m, id) => { const l = m.receipts.lines.find((x) => x.id === id); if (!l) blocked(`the model has no receipt line ${id}`); return l; };
const totalOf = (c, a) => c[a].target_bn + c[a].other_bn;
const nationalOf = (m, g) => GROUPS[g].reduce((t, id) => t + lineOf(m, id).national_bn, 0);
// The four lines' cells, nationals and scenarios, for the "same model" test of editsAt.
const fingerprint = (m) => JSON.stringify(MODEL_LINES.map((id) => { const l = lineOf(m, id); return [l.national_bn, l.cells]; }).concat([m.receipts.scenarios]));

// The added people's share of the case's wage key, split into the G3+ members and the whites as the lineage item prices
// them: later x G_L + (1 - C3) g3 x G_3 and C3 g3 x W_3 in each cell (item_age_mix.cjs; v6 main_case.cjs gates the
// lineage block as v5's plus these deltas). Here per cell of the four lines, and the wage key's shares.
function lineageParts(D, which, m, U, REF) {
  if (!D || !D.part_models || !D.part_models[which] || !D.counts) {
    blocked("the added people's G3+ and white parts come from the lineage item added_age_mix's part models; a case without it has no rule here");
  }
  const pm = D.part_models[which], { later, g3_rate, c3 } = D.counts;
  const cellAt = (mm, id, sc) => lineOf(mm, id).cells[sc];
  const parts = {};
  let worst = 0;
  for (const id of MODEL_LINES) for (const sc of m.receipts.scenarios) {
    const gl = cellAt(pm.later, id, sc), g3 = cellAt(pm.g3_rate, id, sc), w3 = cellAt(pm.white_g3_rate, id, sc);
    const p = { g3plus: byAlloc((a) => later * gl[a].target_bn + (1 - c3) * g3_rate * g3[a].target_bn), whites: byAlloc((a) => c3 * g3_rate * w3[a].target_bn) };
    for (const a of ALLOCS) {
      const lin = cellAt(m, id, sc)[a].target_bn - cellAt(U, id, sc)[a].target_bn;
      worst = Math.max(worst, Math.abs(p.g3plus[a] + p.whites[a] - lin));
    }
    parts[`${id}|${sc}`] = p;
  }
  if (!(worst < 1e-9)) blocked(`the lineage's G3+ and white parts do not add to the added people's cells on the four lines (${worst})`);
  const wc = cellAt(m, WAGE.line, REF);
  if (wc.personal.key !== WAGE.key || wc.shared.key !== WAGE.key) blocked(`${WAGE.line} at ${REF} is not keyed by ${WAGE.key}`);
  const w = parts[`${WAGE.line}|${REF}`];
  const wage = { g3plus: byAlloc((a) => w.g3plus[a] / totalOf(wc, a)), whites: byAlloc((a) => w.whites[a] / totalOf(wc, a)) };
  return { parts, wage, worst_split_gap_bn: worst, counts: { later, g3_rate, c3 } };
}

// The new amounts' five parts on a model, per line, scenario and allocation.
function newParts(blk, wage, m) {
  const out = {};
  for (const id of MODEL_LINES) {
    const g = GROUP_OF[id], N = nationalOf(m, g), L = blk.lines[g], l = lineOf(m, id);
    for (const sc of m.receipts.scenarios) {
      const c = l.cells[sc];
      out[`${id}|${sc}`] = Object.fromEntries(PARTS.map((p) => [p, byAlloc((a) => {
        const f = totalOf(c, a) / N;
        if (p.startsWith("union_")) return blk.by_generation[p.slice("union_".length)][g][a] * f;
        const share = p === "lineage_g3plus" ? wage.g3plus[a] : wage.whites[a], F = p === "lineage_g3plus" ? blk.factor.G3plus : blk.factor.white_nh;
        return share * F[g][a] * L.national_bn * f;
      })]));
    }
  }
  return out;
}
const sumParts = (ps, a) => PARTS.reduce((t, p) => t + ps[p][a], 0);

function responsesOf(blk) {
  const SRC = S.stub ? `${S.file} [STUB]` : `${S.lane}/derived/item.json`;
  const rules = {
    corporate: "corporate tax (corporate_capital and corporate_labor), re-keyed to the group's job-capital amount, at the lane's corporate response at each reading in every profile: the capital that serves the group's jobs is not in the US without it",
    business_property: "business property tax (remaining_production_property: commercial and industrial after v4 split out tenant housing), re-keyed to the job-capital amount, at r_b = 1 - lambda_b (1 - delta_L) in every profile: the structures leave, the land stays at a lower price",
    other_production_taxes: "other taxes on production, re-keyed to the job-capital amount, at response 1 in every profile",
  };
  return Object.fromEntries(MODEL_LINES.map((id) => {
    const g = GROUP_OF[id], r = blk.lines[g].response;
    return [id, { receipt: true, override: `receipt:${id}`, low: r.low, high: r.high, rule: rules[g], source: `item job_capital_taxes: ${SRC}, lines.${g}.response` }];
  }));
}

// ---------------------------------------------------------------------------------------------------
function build(ctx, arm, which) {
  const { B, Engine, MODEL, DETAIL } = ctx;
  const api = which === "set" ? B : B.CASH;
  const REF = MODEL.receipts.reference;
  const m = api.payloadModel(), U = (which === "set" ? B.SEPT29 : B.SEPT29_CASH).payloadModel();
  // The union's old amounts by generation: the September 29 generation models (convention a), adding to the union's.
  const GP = readJson(GEN_FILES[which]);
  if (GP.meta.union !== B.BASE_FILES[which]) blocked(`${GEN_FILES[which]} splits ${GP.meta.union}, not ${B.BASE_FILES[which]}`);
  const GM = Object.fromEntries(GENS.map((G) => [G, Engine.applyCorrections(readJson(`${GEN}/model_${G}.json`), GP.payloads.a[G])]));
  const blk = arm === CEILING ? ceilingBlock(GM, U, REF) : blockOf(arm);
  let genGap = 0;
  for (const id of MODEL_LINES) for (const sc of m.receipts.scenarios) for (const a of ALLOCS) {
    genGap = Math.max(genGap, Math.abs(GENS.reduce((t, G) => t + lineOf(GM[G], id).cells[sc][a].target_bn, 0) - lineOf(U, id).cells[sc][a].target_bn));
  }
  if (!(genGap < 1e-9)) blocked(`${which}: the generation models' cells on the four lines do not add to the union's (${genGap})`);
  // The lane's plain wage share is the union's share of the case's wage key on the September 29 payload model.
  const wageCell = lineOf(U, WAGE.line).cells[REF];
  const pwsGap = Math.max(...LINE_GROUPS.flatMap((g) => ALLOCS.map((a) => Math.abs(blk.lines[g].plain_wage_share[a] - wageCell[a].target_bn / totalOf(wageCell, a)))));
  if (!(pwsGap < 1e-9)) blocked(`${which}: the lane's plain_wage_share is not the union's share of ${WAGE.line} at ${REF} on the September 29 payload (${pwsGap})`);
  if (!arm || arm === CEILING) for (const g of LINE_GROUPS) {
    if (Math.abs(blk.lines[g].national_bn - nationalOf(m, g)) > 1e-6) blocked(`lines.${g}.national_bn ${blk.lines[g].national_bn} is not the case's ${nationalOf(m, g)}`);
  }
  const lin = lineageParts(DETAIL && DETAIL.added_age_mix, which, m, U, REF);
  const np = newParts(blk, lin.wage, m);
  const edits = [], parts = {};
  let jGap = 0;
  for (const id of MODEL_LINES) for (const sc of m.receipts.scenarios) {
    const k = `${id}|${sc}`, n = np[k], cells = lineOf(m, id).cells[sc];
    const old = Object.fromEntries(PARTS.map((p) => [p, byAlloc((a) => (p.startsWith("union_") ? lineOf(GM[p.slice("union_".length)], id).cells[sc][a].target_bn
      : p === "lineage_g3plus" ? lin.parts[k].g3plus[a] : lin.parts[k].whites[a]))]));
    const j = edits.length, by = { personal: 0, shared: 0 };
    for (const p of PARTS) {
      const d = byAlloc((a) => n[p][a] - old[p][a]);
      parts[`${p}:${id}:${sc}`] = { edit: j, by: d };
      for (const a of ALLOCS) by[a] += d[a];
    }
    for (const a of ALLOCS) jGap = Math.max(jGap, Math.abs(cells[a].target_bn + by[a] - sumParts(n, a)));
    edits.push({ side: "receipt", line: id, scenario: sc, by });
  }
  if (!(jGap < 1e-9)) blocked(`${which}: the edits do not set the four lines' targets to the job-capital amounts (${jGap})`);
  const FP = fingerprint(m), wage = lin.wage;
  function editsAt(mm) {
    if (fingerprint(mm) === FP) return clone(edits);
    const q = newParts(blk, wage, mm);
    return MODEL_LINES.flatMap((id) => mm.receipts.scenarios.map((sc) => {
      const c = lineOf(mm, id).cells[sc];
      return { side: "receipt", line: id, scenario: sc, by: byAlloc((a) => sumParts(q[`${id}|${sc}`], a) - c[a].target_bn) };
    }));
  }
  const responses = responsesOf(blk);
  const J = (id, sc) => byAlloc((a) => sumParts(np[`${id}|${sc}`], a));
  const groupAt = (fn) => Object.fromEntries(LINE_GROUPS.map((g) => [g, byAlloc((a) => GROUPS[g].reduce((t, id) => t + fn(id)[a], 0))]));
  const before = groupAt((id) => byAlloc((a) => lineOf(m, id).cells[REF][a].target_bn)), after = groupAt((id) => J(id, REF));
  const effect = Object.fromEntries(READINGS.map((rd) => [rd, byAlloc((a) => LINE_GROUPS.reduce((t, g) => t + blk.lines[g].response[rd] * after[g][a], 0))]));
  const others = [["central", null, "the lane's central reading (the case)"]].concat(Object.entries(ARMS).map(([k, d]) => [k, k, d.label])).filter(([, k]) => k !== (arm || null) && arm !== CEILING);
  const block = {
    rule: "the taxes on the business capital that serves the group's jobs: corporate tax (corporate_capital, corporate_labor), business property tax (remaining_production_property) and other taxes on production, re-keyed at every receipt scenario to the group's job-capital amount by cell shifts (national totals hold) and responding as meta.responses sets; the owners keep the same after-tax return, so P and F do not move, and the production module's capital-tax term stays 0 at every case specification (capital_tax_retention 1), so nothing counts twice",
    stub: S.stub,
    arm: arm || "central",
    amounts: "on each model line L of the lane's line g, at each scenario and allocation: J = (union_G1 + union_G2 + union_G3plus + lineage_g3plus + lineage_whites) x T / N_g, T the cell's total (target plus other) and N_g the national of g's model lines; union_G = the lane's by_generation[G][g]; lineage_x = the added people's share of the case's wage key (corporate_labor at cbo_collective) for part x times the lane's factor (G3plus for the G3+ members, white_nh for the whites) for g times g's national_bn",
    lines: Object.fromEntries(LINE_GROUPS.map((g) => [g, Object.assign({ model_lines: GROUPS[g], model_national_bn: nationalOf(m, g) }, clone(blk.lines[g]),
      { factor_union: clone(blk.factor.union[g]), group_before_bn: before[g], group_after_bn: after[g] })])),
    by_generation: clone(blk.by_generation),
    factors: { G3plus: Object.fromEntries(LINE_GROUPS.map((g) => [g, clone(blk.factor.G3plus[g])])), white_nh: Object.fromEntries(LINE_GROUPS.map((g) => [g, clone(blk.factor.white_nh[g])])) },
    lineage: { rule: "the added people's share of the case's wage key from their own cells on corporate_labor at cbo_collective, split into the G3+ members (later x G_L + (1 - C3) g3 x G_3) and the whites (C3 g3 x W_3) by the lineage item's part models, times the lane's G3plus and white_nh factors",
      wage_share: clone(wage), counts: clone(lin.counts) },
    effect_at_reference_bn: effect,
    production: { capital_tax_term_bn: 0, rule: "the production module's capital-tax term is 0.246 x (domestic capital gain - capital_tax_retention x opportunity income); at every case specification the state's production cell has capital_adjustment 1, capital_tax_retention 1 and no excluded owners, where the term is 0 (full_account_benefits_2026_09_20 upstream_replay scenarios.csv; main_case.cjs gates it)" },
    arms: Object.fromEntries(others.map(([k, a, label]) => { const b = blockOf(a); return [k, { label, lines: Object.fromEntries(LINE_GROUPS.map((g) => [g, { national_bn: b.lines[g].national_bn, response: b.lines[g].response, key_share: clone(b.lines[g].key_share) }])) }]; })),
    source: { lane: S.lane, file: S.file, sha256: S.sha256, stub: S.stub, verdict: S.verdict },
  };
  return {
    edits, editsAt, parts, responses,
    meta: { job_capital_taxes: block },
    record: {
      source_arm: arm || "central", stub: S.stub,
      rule: "item_job_capital.cjs: the four lines re-keyed at every scenario to the job-capital amount, by = new less old amounts part by part; editsAt re-keys any other model to the same amounts",
      parts_rule: "union_G1, union_G2 and union_G3plus are the identified 39.71M's generations (the lane's by_generation less the September 29 generation models' cells, convention a); lineage_g3plus and lineage_whites the 3.04M added people's (the G3plus and white_nh factors at their share of the wage key, less their cells); each edit's by is its five parts' sum, in that order",
      responses: Object.fromEntries(MODEL_LINES.map((id) => [id, { low: responses[id].low, high: responses[id].high }])),
      group_before_bn: before, group_after_bn: after, effect_at_reference_bn: effect,
      source_central_bn: blk.central_bn, source: { file: S.file, sha256: S.sha256, verdict: S.verdict },
    },
    detail: { generation_gap_bn: genGap, plain_wage_share_gap: pwsGap, lineage_split_gap_bn: lin.worst_split_gap_bn, target_gap_bn: jGap, wage_share: wage, new_parts: np },
  };
}

module.exports = { build, ARMS, CENTRAL, CEILING, S, LINES: MODEL_LINES, GROUPS, GROUP_OF, PARTS, WAGE, READINGS, tag: () => tag(S), blockOf, responsesOf, showReadings };
