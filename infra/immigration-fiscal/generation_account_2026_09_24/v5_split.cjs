/* v5 case (oct05): the main case adopted on 2026-10-05 (main_case_2026_10_05, decisions/2026-10-05-main-case-v5.md) split
 * by generation, for any set of models whose September 29 payloads add to the union's: this lane's three generations
 * (run_generations_v5.cjs) and the late-arrival lane's nine cells (its run_cells.cjs). A module: it runs nothing and
 * writes nothing.
 *
 * The case is the September 29 case plus the lineage (main_case_lineage_2026_10_05, arm b, counted whole): its payload
 * is the September 29 payload of the same set (the set's, or candidate v4's cash payload for the cash set) with the
 * lineage's 336 edits appended, the lineage's production grid and the lineage's meta (the group-size responses at the
 * larger group, the long-run capital values at them, meta.lineage). The edits are the added people's amounts in every
 * engine cell, then audit row 8's change at the larger group on lane_constants (meta.lineage.edits.row8_edit_index).
 * Each model's v5 part, beside its September 29 payload:
 *   the added people  the G3+ model (TOP G3plus; exactly one) takes the lineage's cell edits and the change in the
 *                     production grid, as the case's package.cjs withLineage() adds them: the 3.04M descendants who no
 *                     longer report Mexican origin, priced as identified G3+ members and as third-plus non-Hispanic whites
 *                     at G3+ ages, are third-plus by construction;
 *   row 8             the union's response move: every model takes the edit times its share of the September 29 union's
 *                     lane_constants k cell, per allocation (the lineage lane's generationCosts() rule; its shares add
 *                     to 1). The package's withLineage() puts all of it on the model it is given (ROW8_ALTERNATIVE);
 *   the responses     nothing to place: every model is evaluated at the case's responses (the payload's meta).
 * evaluator() is v4_split.cjs's (candidate v4's package-free consumer.cjs) on the v5 payload; adoptedPackage() is the
 * v5 package itself (its CASH for the cash set), which the runners gate it against on every model they cost.
 */
"use strict";
const path = require("path");
const X = require(path.join(__dirname, "v4_split.cjs"));
const { Engine, MODEL, ALLOCS, byAlloc, lineOf, readJson, sum } = X;

const FISCAL = path.resolve(__dirname, "..");
const V5_LANE = "main_case_2026_10_05";
const LINEAGE_LANE = "main_case_lineage_2026_10_05";
const P5 = require(path.join(FISCAL, V5_LANE, "package.cjs"));
const V5_FILES = { set: `${V5_LANE}/derived/corrections.json`, cash: `${V5_LANE}/derived/corrections_cash.json` };
const ROW8 = { side: "spending", line: "lane_constants", key: "k" };
const ROW8_ALTERNATIVE = "row 8: the whole edit on the G3+ model (the package's withLineage() on that model alone; "
  + "main_case_2026_10_05 api_check.cjs pattern 3 prints the split this way)";
const clone = (x) => JSON.parse(JSON.stringify(x));
const blocked = (why) => { throw new Error("[BLOCKED] " + why); };
if (P5.Engine !== Engine || P5.MODEL !== MODEL) blocked(`${V5_LANE}/package.cjs does not run on v4_split.cjs's engine and model`);

// ---------------------------------------------------------------------------------------------------
// The case for a set: its payload, the September 29 payload it builds on, the lineage's cell edits, row 8's edit and
// the production grid's change; api is the v5 package for the set (P5, or P5.CASH).
function loadCase(set) {
  const rel = V5_FILES[set], baseRel = P5.BASE_FILES[set];
  if (!rel || !baseRel) blocked(`no ${set} payload in ${V5_LANE}`);
  const payload = readJson(rel), base = readJson(baseRel);
  const api = set === "set" ? P5 : P5.CASH;
  if (JSON.stringify(api.correctionsPayload()) !== JSON.stringify(payload)) blocked(`${rel} is not ${V5_LANE}/package.cjs's ${set} payload`);
  for (const k of ["lines", "receipt_lines"]) if (JSON.stringify(payload[k]) !== JSON.stringify(base[k])) blocked(`${rel}: its ${k} are not ${baseRel}'s`);
  const n = base.edits.length;
  if (JSON.stringify(payload.edits.slice(0, n)) !== JSON.stringify(base.edits)) blocked(`${rel} does not start with ${baseRel}'s edits`);
  const lin = payload.meta.lineage;
  const add = payload.edits.slice(n);
  if (!lin || lin.edits.first !== n || lin.edits.count !== add.length || lin.edits.row8_edit_index !== payload.edits.length - 1
    || JSON.stringify(add) !== JSON.stringify(api.LINEAGE_EDITS)) blocked(`${rel}: meta.lineage.edits does not locate the package's lineage edits`);
  const row8 = add[add.length - 1];
  if (!(row8.side === ROW8.side && row8.line === ROW8.line && row8.key === ROW8.key && ALLOCS.every((a) => row8.by[a] === lin.edits.row8_edit_bn))) {
    blocked(`${rel}: the lineage's last edit is not audit row 8's change on ${ROW8.line}`);
  }
  if (lin.generation !== "G3plus") blocked(`${rel}: the lineage is priced as ${lin.generation}, not G3plus`);
  const cells = add.slice(0, -1);
  if (cells.some((e) => e.line === ROW8.line && e.key === ROW8.key && e.side === ROW8.side && e.by.personal === lin.edits.row8_edit_bn)) {
    blocked(`${rel}: a second row-8 edit among the lineage's cell edits`);
  }
  const pb = base.production, pp = payload.production;
  if (JSON.stringify(pp.dims) !== JSON.stringify(pb.dims) || JSON.stringify(pp.sampling_se_bn) !== JSON.stringify(pb.sampling_se_bn)
    || ["private_wtp_bn", "induced_receipts_bn"].some((k) => pp[k].length !== pb[k].length)) blocked(`${rel}: its production grid is not ${baseRel}'s with new P and F`);
  const dp = Object.fromEntries(["private_wtp_bn", "induced_receipts_bn"].map((k) => [k, pp[k].map((v, i) => v - pb[k][i])]));
  return { set, rel, baseRel, payload, base, n, lineage: lin, cells, row8, dp, api };
}

// ---------------------------------------------------------------------------------------------------
// The v5 part of each model. models29 ({g: the model with its September 29 payload}) add to union29 (the September 29
// union's corrected model) cell by cell; top maps each model to its generation. Returns each model's share of the
// lane_constants k cell and its part: {edits (the lineage's cell edits on the G3+ model, then its row-8 edit), row8 (that
// edit), production (the grid's change on the G3+ model, else null)}. alt ["row8_on_g3plus"]: ROW8_ALTERNATIVE.
const ALTERNATIVES = { row8_on_g3plus: ROW8_ALTERNATIVE };
const kCell = (m) => lineOf(m, "spending", ROW8.line).keys[ROW8.key];
function layer(L, gens, top, models29, union29, opts) {
  const alt = new Set((opts && opts.alt) || []);
  for (const x of alt) if (!ALTERNATIVES[x]) blocked(`unknown alternative ${x}`);
  const g3 = gens.filter((g) => top[g] === "G3plus");
  if (g3.length !== 1) blocked(`the lineage goes on exactly one G3+ model; ${g3.length} found`);
  const kU = kCell(union29);
  const share = Object.fromEntries(gens.map((g) => [g, alt.has("row8_on_g3plus") ? byAlloc(() => (g === g3[0] ? 1 : 0))
    : byAlloc((a) => kCell(models29[g])[a].target_bn / kU[a].target_bn)]));
  const parts = Object.fromEntries(gens.map((g) => {
    const row8 = Object.assign(clone(ROW8), { by: byAlloc((a) => L.row8.by[a] * share[g][a]) });
    return [g, { edits: (g === g3[0] ? clone(L.cells) : []).concat([row8]), row8, production: g === g3[0] ? L.dp : null }];
  }));
  const shareSum = Math.max(...ALLOCS.map((a) => Math.abs(sum(gens.map((g) => share[g][a])) - 1)));
  return { g3plus: g3[0], share, share_sum_error: shareSum, parts };
}

// A model's v5 payload: its September 29 payload, then its part; the G3+ model's grid moves by the lineage's change.
function payloadOf(p29, part) {
  const p = { receipt_lines: p29.receipt_lines || [], lines: p29.lines, edits: p29.edits.concat(part.edits) };
  const g = p29.production;
  if (part.production) {
    if (!g) blocked("a September 29 generation payload without a production grid");
    p.production = { dims: g.dims, private_wtp_bn: g.private_wtp_bn.map((v, i) => v + part.production.private_wtp_bn[i]),
      induced_receipts_bn: g.induced_receipts_bn.map((v, i) => v + part.production.induced_receipts_bn[i]), sampling_se_bn: g.sampling_se_bn };
  } else if (g) p.production = g;
  return p;
}
// A corrected model with edits applied on top (v4_split.cjs chainA's apply): the row-8 term of the response move.
const withEdits = (m, edits) => Engine.applyCorrections(m, { lines: [], edits, meta: m.corrections });

// ---------------------------------------------------------------------------------------------------
// The v5 package on the case's payload (its evaluateFull at its MAIN_SPECS), to cross-check evaluator() on every model.
function adoptedPackage(L) {
  return { source: `${V5_LANE}/package.cjs${L.set === "set" ? "" : " CASH"}`, specs: L.api.MAIN_SPECS,
    cost: (m, i) => L.api.evaluateFull(m, L.api.MAIN_SPECS[i], L.api.MAIN_PROFILE).cost_bn };
}
// The oracle: the lane's published band for the set or the cash set (four decimals), its end specifications, and the
// uncorrected model's band at the case's responses (the same row for both sets).
function oracle(set) {
  const variant = set === "set" ? "adopted" : "cash_set";
  const rows = X.P.csvRows(`${V5_LANE}/derived/main_case_bands.csv`).filter((x) => x.profile === X.P.MAIN_PROFILE);
  const r = rows.find((x) => x.variant === variant), u = rows.find((x) => x.variant === "uncorrected_at_adopted_responses");
  const S = readJson(`${V5_LANE}/derived/summary.json`);
  const ends = set === "set" ? S.end_specifications.map((x) => [x.low_end.index, x.high_end.index]) : S.cash_set.end_specifications;
  if (!r || !u || !ends.length || !ends.every((x) => x[0] === ends[0][0] && x[1] === ends[0][1])) {
    blocked(`${V5_LANE}: no ${variant} and uncorrected rows in main_case_bands.csv, or the methods' ends differ`);
  }
  return { source: `${V5_LANE}/derived/main_case_bands.csv (${variant})`, specs: ends[0].map(Number),
    band: [Number(r.cost_low_bn), Number(r.cost_high_bn)], uncorrected: [Number(u.cost_low_bn), Number(u.cost_high_bn)] };
}
// The lane's cost at every specification, the mean of the two fill-in methods (the set only).
function perSpec(set) {
  if (set !== "set") return null;
  const rows = X.P.csvRows(`${V5_LANE}/derived/per_spec.csv`);
  const out = new Map();
  for (const i of [...new Set(rows.map((r) => Number(r.spec)))]) {
    const rs = rows.filter((r) => Number(r.spec) === i);
    if (rs.length !== X.METHODS.length || !X.METHODS.every((m) => rs.some((r) => r.method === m))) blocked(`spec ${i}: not one row per method`);
    out.set(i, sum(rs.map((r) => Number(r.cost_bn))) / rs.length);
  }
  return { source: `${V5_LANE}/derived/per_spec.csv cost_bn`, cost: out };
}
// The lineage lane's parts of the change from the September 29 case (arm b, at the end specifications).
function lineageParts(set) {
  const S = readJson(`${LINEAGE_LANE}/derived/v5_summary.json`);
  const b = S.sets[set] && S.sets[set].arms && S.sets[set].arms.b;
  if (!b) blocked(`${LINEAGE_LANE}/derived/v5_summary.json: no ${set} arm b`);
  return { source: `${LINEAGE_LANE}/derived/v5_summary.json sets.${set}.arms.b`, ends: b.ends, band_bn: b.band_bn,
    change_bn: b.change_from_v4_bn, union_response_move_bn: b.of_which_union_response_move_bn,
    g3plus_part_bn: b.of_which_g3plus_part_bn, white_part_bn: b.of_which_white_part_bn };
}

module.exports = { V5_LANE, LINEAGE_LANE, V5_FILES, ROW8, ALTERNATIVES, P5, X, loadCase, layer, payloadOf, withEdits, kCell,
  adoptedPackage, oracle, perSpec, lineageParts };
