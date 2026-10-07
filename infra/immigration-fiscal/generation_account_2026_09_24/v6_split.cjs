/* v6 case (oct07): main case v6 (main_case_2026_10_07, key oct07: main case v5 plus an item registry) split by
 * generation, for any set of models whose September 29 payloads add to the union's: this lane's three generations
 * (run_generations_v6.cjs) and the late-arrival lane's nine cells (its run_cells.cjs). A module: it runs nothing and
 * writes nothing.
 *
 * The v6 payload is v5's in layout (v5_split.cjs) with two changes (main_case_2026_10_07 RESULT "The payloads"):
 *   - the lineage block (meta.lineage.edits: first, count, row 8 last within it) holds the lineage item's values (the
 *     package's LINEAGE_EDITS) in v5's cells and order, with v5's row 8 edit; its production grid is the item's;
 *   - the edit sets' edits follow the lineage block, in registry order; meta.items gives each applied edit set's place
 *     ({first, count}) and the parts its cell shifts add up from.
 * Each model's v6 part, beside its September 29 payload:
 *   the added people and row 8  v5_split.cjs layer(), unchanged, on the lineage item's cell edits and grid: G3+ takes
 *                               the lineage's cell edits and the grid's change; every model takes row 8's edit times its
 *                               share of the September 29 union's lane_constants k cell;
 *   the edit sets               in the payload's order, each edit by RULES:
 *     national-scale edit       ({side, line, national_bn}, engine.js scaleLine) as it is, on every model: each model
 *                               carries the union's national totals, so its cells scale by the case's factor and the
 *                               models still add to the union;
 *     a cell shift              its parts (meta.items), each spread by its rule's shares, which add to 1:
 *       lineage                 all on the G3+ model (TOP G3plus; exactly one): the added people's part;
 *       pension_oasdi           the September 29 split's own pension rule (v4_split.cjs split(): each model's accrual
 *       pension_part_a          is its generation's accrual per tax dollar times its own OASDI receipts, normalized to
 *                               the union's accrual; Part A likewise per HI tax dollar on its HI receipts), with each
 *                               generation's ratio moved by the pension lane's per-generation rows (arms.csv at the
 *                               payload's pinned commit: the item's arm over the control). Each model takes its own
 *                               change from the old split to the new, as a share of the union's change;
 *       parent_line             pro rata to each model's share of the parent line's union amount on the September 29
 *                               payloads: the line the item's meta names for the part (splits.split_basis), else the
 *                               edited line (the parent line's, for a payload line declared with a parent);
 *     an item's carriers        (its capital: receipt lines of one dollar whose share keys the item's offset components)
 *                               each model's carrier is the union's at the model's share by RULES[item].carriers
 *                               (parent_line: the line the item's split_basis names for the carrier), after its
 *                               September 29 receipt lines (payloadOf), so the models' offsets add to the union's.
 * ALTERNATIVES holds the rule beside each designed one; pension_receipt_shares is main_case_2026_10_07 api_check.cjs
 * pattern 3's rule (the union parts by each model's share of the union's OASDI receipts and Part A accrual).
 * evaluator() is v4_split.cjs's (candidate v4's package-free consumer.cjs) on the v6 payload, with the items' carriers
 * at zero on a model that lacks them (the package's withSyntheticLines); adoptedPackage() is the v6 package itself (its
 * CASH for the cash set), which the runners gate it against on every model they cost.
 */
"use strict";
const path = require("path");
const { execFileSync } = require("child_process");
const V5 = require(path.join(__dirname, "v5_split.cjs"));
const { X } = V5;
const { Engine, MODEL, ALLOCS, byAlloc, lineOf, readJson, sum } = X;

const FISCAL = path.resolve(__dirname, "..");
const ROOT = path.resolve(FISCAL, "..", "..");
const V6_LANE = "main_case_2026_10_07";
const P6 = require(path.join(FISCAL, V6_LANE, "package.cjs"));
const V6_FILES = { set: `${V6_LANE}/derived/corrections.json`, cash: `${V6_LANE}/derived/corrections_cash.json` };
const PENSION_ARMS = "derived/arms.csv";
const blocked = (why) => { throw new Error("[BLOCKED] " + why); };
const clone = (x) => JSON.parse(JSON.stringify(x));
if (P6.Engine !== Engine || P6.MODEL !== MODEL) blocked(`${V6_LANE}/package.cjs does not run on v4_split.cjs's engine and model`);

// The rule for each applied edit set's cell shifts, by part name (its meta.items parts) or a name prefix ("union_*"),
// or "*" for an item whose cell shifts carry no parts, and under "carriers" the rule for its carrier receipt lines (an
// item's capital). A national-scale edit needs no rule. An applied edit set that is not here stops the split.
const RULES = {
  pension_tr2026: { union_oasdi: "pension_oasdi", union_part_a: "pension_part_a", lineage_oasdi: "lineage", lineage_part_a: "lineage" },
  retiree_health: {},
  // The item's split_rule (meta.items): every part (each is union_<term>, its parts_rule) and each carrier pro rata to
  // the parent line's union amount, the line its meta names (meta.user_fees.splits.split_basis); the added people take none.
  user_fees: { "union_*": "parent_line", carriers: "parent_line" },
};
// A part's rule: its own name's, else the first prefix pattern ("<prefix>*") its name starts with.
const ruleOf = (R, name) => R[name] || Object.entries(R).filter(([k]) => k.length > 1 && k.endsWith("*") && name.startsWith(k.slice(0, -1)))
  .map(([, v]) => v)[0];
const RULE_TEXT = {
  as_is: "a national-scale edit as it is on every model (each carries the union's national totals; engine.js scaleLine)",
  lineage: "on the G3+ model: the added people's part",
  pension_oasdi: "the September 29 split's pension rule (v4_split.cjs: each generation's accrual per tax dollar net of the benefit tax on "
    + "its own OASDI receipts, normalized to the union's accrual) with each generation's ratio times the pension lane's arm over its "
    + "control (arms.csv); each model takes its change from the old split to the new",
  pension_part_a: "the same for Part A: each generation's Part A accrual per HI tax dollar on its own HI receipts, normalized to the "
    + "union's Part A accrual, with the ratio times the arm over the control",
  parent_line: "pro rata to each model's share of the parent line's union amount on the September 29 payloads: the line its item's "
    + "meta names for the part or carrier (meta.<key>.splits.split_basis) at the line's preferred key, else the edited line at the "
    + "edit's key (its parent's, for a payload line with a parent)",
};
const ALTERNATIVES = Object.assign({}, V5.ALTERNATIVES, {
  pension_receipt_shares: "pension_tr2026's union parts by each model's share of the union's OASDI receipts and of its Part A "
    + "accrual on the September 29 payloads (main_case_2026_10_07 api_check.cjs pattern 3's rule), the same change per dollar in "
    + "every generation",
});
ALTERNATIVES.split_basis_edited_line = "each item part on a model line split by that line at its edit's key instead of the line its "
  + "meta's split_basis names (union_key_pell by other_federal_benefits' all_cash shares, where the case puts it on "
  + "education_services); parts on a payload line without a parent (the K-12 weight's, on school_reprice and college_rekey) and "
  + "the carriers keep their split_basis";
const PENSION_ALTERNATIVES = ["pension_receipt_shares"];

// ---------------------------------------------------------------------------------------------------
// The case for a set: its payload, the September 29 payload it builds on, the lineage block (cell edits, row 8's edit,
// the grid's change) and the edit sets (meta.items, in the payload's order); api is the v6 package for the set.
function loadCase(set) {
  const rel = V6_FILES[set], baseRel = P6.BASE_FILES[set];
  if (!rel || !baseRel) blocked(`no ${set} payload in ${V6_LANE}`);
  const payload = readJson(rel), base = readJson(baseRel);
  const api = set === "set" ? P6 : P6.CASH;
  if (JSON.stringify(api.correctionsPayload()) !== JSON.stringify(payload)) blocked(`${rel} is not ${V6_LANE}/package.cjs's ${set} payload`);
  if (JSON.stringify(payload.lines) !== JSON.stringify(base.lines)) blocked(`${rel}: its lines are not ${baseRel}'s`);
  // An item's capital adds carrier receipt lines after the base's and components after the item base's (package.cjs
  // forItems), in registry order.
  const carriers = api.ITEM_RECEIPT_LINES || [], comps = api.ITEM_COMPONENTS || [];
  if (JSON.stringify(payload.receipt_lines) !== JSON.stringify((base.receipt_lines || []).concat(carriers))) {
    blocked(`${rel}: its receipt lines are not ${baseRel}'s and the items' carriers`);
  }
  const itemBase = (set === "set" ? P6.ITEM_BASE : P6.ITEM_BASE.CASH).correctionsPayload();
  if (JSON.stringify(payload.meta.capital_return.components) !== JSON.stringify(itemBase.meta.capital_return.components.concat(comps))) {
    blocked(`${rel}: its capital components are not the item base's and the items'`);
  }
  const n = base.edits.length;
  if (JSON.stringify(payload.edits.slice(0, n)) !== JSON.stringify(base.edits)) blocked(`${rel} does not start with ${baseRel}'s edits`);
  const lin = payload.meta.lineage;
  if (!lin || lin.edits.first !== n || lin.edits.row8_edit_index !== n + lin.edits.count - 1) blocked(`${rel}: meta.lineage.edits does not follow ${baseRel}'s edits with row 8 last`);
  const add = payload.edits.slice(n, n + lin.edits.count);
  if (JSON.stringify(add) !== JSON.stringify(api.LINEAGE_EDITS)) blocked(`${rel}: meta.lineage.edits does not locate the package's lineage edits`);
  const row8 = add[add.length - 1], R8 = V5.ROW8;
  if (!(row8.side === R8.side && row8.line === R8.line && row8.key === R8.key && ALLOCS.every((a) => row8.by[a] === lin.edits.row8_edit_bn))) {
    blocked(`${rel}: the lineage block's last edit is not audit row 8's change on ${R8.line}`);
  }
  if (lin.generation !== "G3plus") blocked(`${rel}: the lineage is priced as ${lin.generation}, not G3plus`);
  const cells = add.slice(0, -1);
  if (cells.some((e) => e.line === R8.line && e.key === R8.key && e.side === R8.side && e.by.personal === lin.edits.row8_edit_bn)) {
    blocked(`${rel}: a second row-8 edit among the lineage's cell edits`);
  }
  const pb = base.production, pp = payload.production;
  if (JSON.stringify(pp.dims) !== JSON.stringify(pb.dims) || JSON.stringify(pp.sampling_se_bn) !== JSON.stringify(pb.sampling_se_bn)
    || ["private_wtp_bn", "induced_receipts_bn"].some((k) => pp[k].length !== pb[k].length)) blocked(`${rel}: its production grid is not ${baseRel}'s with new P and F`);
  const dp = Object.fromEntries(["private_wtp_bn", "induced_receipts_bn"].map((k) => [k, pp[k].map((v, i) => v - pb[k][i])]));
  // meta.items: one lineage item (the block above) and the edit sets, whose edits tile the rest of the payload in order.
  const records = payload.meta.items;
  if (!Array.isArray(records) || !records.length) blocked(`${rel}: no meta.items`);
  if (records.some((r) => !["lineage", "edit_set"].includes(r.kind))) blocked(`${rel}: an item of a kind this split has no rule for`);
  const lineageItems = records.filter((r) => r.kind === "lineage");
  if (lineageItems.length !== 1 || !lineageItems[0].applied || JSON.stringify(lineageItems[0].lineage_edits) !== JSON.stringify(lin.edits)) {
    blocked(`${rel}: meta.items does not hold one applied lineage item at meta.lineage.edits`);
  }
  const tail = payload.edits.slice(n + lin.edits.count);
  if (JSON.stringify(tail) !== JSON.stringify(api.ITEM_EDITS)) blocked(`${rel}: the edits after the lineage block are not the package's ITEM_EDITS`);
  let at = n + lin.edits.count;
  const items = records.filter((r) => r.kind === "edit_set" && r.applied).map((r) => {
    if (!r.edits || r.edits.first !== at || !(r.edits.count > 0)) blocked(`${rel}: item ${r.id}'s edits do not follow the previous item's`);
    const edits = payload.edits.slice(at, at + r.edits.count);
    at += r.edits.count;
    // Its carriers: the payload's lines it names, whose shares are the values its record gives.
    const cap = r.capital;
    const lines = cap ? cap.receipt_lines.map((id) => payload.receipt_lines.find((l) => l.id === id)) : [];
    if (cap && lines.some((l, j) => !l || ALLOCS.some((a) => l.cells[MODEL.receipts.reference][a].share !== cap.carrier_values[cap.receipt_lines[j]][a]))) {
      blocked(`${rel}: item ${r.id}'s carriers are not in the payload at its record's values`);
    }
    return { id: r.id, record: r, first: r.edits.first, edits, receipt_lines: lines };
  });
  if (at !== payload.edits.length) blocked(`${rel}: ${payload.edits.length - at} edits after the last item's`);
  for (const r of records.filter((x) => x.kind === "edit_set" && !x.applied)) if (r.edits) blocked(`${rel}: item ${r.id} is not applied but has edits`);
  if (JSON.stringify(items.flatMap((it) => it.receipt_lines.map((l) => l.id))) !== JSON.stringify(carriers.map((l) => l.id))
    || JSON.stringify(items.flatMap((it) => (it.record.capital ? it.record.capital.components : []))) !== JSON.stringify(comps.map((c) => c.id))) {
    blocked(`${rel}: the items' records do not name the package's carriers and components, in order`);
  }
  return { set, rel, baseRel, payload, base, n, lineage: lin, cells, row8, dp, api, records, items, lineageItem: lineageItems[0].id };
}

// ---------------------------------------------------------------------------------------------------
// The pension rule's inputs: the September 29 split's (v4_split.cjs pensionInputs(), the 2025 lane at 9ea1beb, and the
// candidate v4 package's pension block) and the 2026 arm's per-generation rows (arms.csv at the payload's pinned
// commit), each generation's ratio moved by the arm over the control.
const armsCache = new Map();
function pensionArms(commit) {
  if (armsCache.has(commit)) return armsCache.get(commit);
  const rel = `infra/immigration-fiscal/pension_tr2026_2026_10_06/${PENSION_ARMS}`;
  let text;
  try { text = execFileSync("git", ["-C", ROOT, "show", `${commit}:${rel}`], { maxBuffer: 1 << 26, stdio: ["ignore", "pipe", "ignore"] }).toString("utf8"); }
  catch (e) { blocked(`${rel} is not in commit ${commit}`); }
  const [h, ...rows] = text.trim().split("\n");
  const k = h.split(",");
  const out = rows.map((r) => Object.fromEntries(r.split(",").map((v, i) => [k[i], v])));
  armsCache.set(commit, out);
  return out;
}
function pensionInputs(L, rec) {
  const PA = L.payload.meta.pension_accrual;
  if (!PA || !PA.previous || !PA.previous.oct05 || !PA.source) blocked(`${L.rel}: no 2026 pension block with its previous (oct05) values`);
  const pi = X.pensionInputs(), pp = X.V4.pensionNet();
  const prev = PA.previous.oct05;
  if (!(prev.ratio_net === pp.ratio_net && prev.part_a_accrual_bn === pp.part_a_accrual_bn && prev.source.commit === pp.commit
    && PA.part_a_share === pp.part_a_share && PA.se_oasdi_share === pp.se_oasdi_share && pi.commit === pp.commit)) {
    blocked(`${L.rel}: the pension block's previous values are not the September 29 split's (${pp.commit})`);
  }
  if (rec.source_arm !== PA.source.arm || rec.ratio_net.oct07 !== PA.ratio_net || rec.part_a_accrual_bn.oct07 !== PA.part_a_accrual_bn) {
    blocked(`item ${rec.id}: its record is not the payload's pension block`);
  }
  const rows = pensionArms(PA.source.commit);
  const row = (arm, g) => { const r = rows.filter((x) => x.arm === arm && x.group === g); if (r.length !== 1) blocked(`arms.csv: not one ${arm} row for ${g}`); return r[0]; };
  const gens = pi.gens;
  const num = (arm, g, c) => Number(row(arm, g)[c]);
  const half = 5.0001e-10;
  const checks = {
    control_net_is_the_split_s: Math.max(...gens.map((g) => Math.abs(num("control", g, "net_per_tax_dollar") - pi.net_ratio[g]))),
    control_union_net: Math.abs(num("control", "union", "net_per_tax_dollar") - pp.ratio_net),
    control_union_part_a: Math.abs(num("control", "union", "part_a_bn") - pp.part_a_accrual_bn),
    arm_union_net: Math.abs(num(PA.source.arm, "union", "net_per_tax_dollar") - PA.ratio_net),
    arm_union_part_a: Math.abs(num(PA.source.arm, "union", "part_a_bn") - PA.part_a_accrual_bn),
  };
  const bad = Object.entries(checks).filter(([, v]) => !(v <= half));
  if (bad.length) blocked(`arms.csv at ${PA.source.commit} is not the pension blocks to its nine decimals: ${bad.map(([k, v]) => `${k} ${v}`).join(", ")}`);
  const f_net = Object.fromEntries(gens.map((g) => [g, num(PA.source.arm, g, "net_per_tax_dollar") / num("control", g, "net_per_tax_dollar")]));
  const f_part_a = Object.fromEntries(gens.map((g) => [g, num(PA.source.arm, g, "part_a_per_hi_tax_dollar") / num("control", g, "part_a_per_hi_tax_dollar")]));
  // G3+'s factors are the item's lineage factors (summary.json at full precision) to arms.csv's rounding.
  if (!(Math.abs(f_net.G3plus - rec.factors.f_ss) < 2e-9 && Math.abs(f_part_a.G3plus - rec.factors.f_pa) < 2e-9)) {
    blocked(`arms.csv's G3+ factors are not item ${rec.id}'s lineage factors`);
  }
  return { commit: PA.source.commit, arm: PA.source.arm, file: `pension_tr2026_2026_10_06/${PENSION_ARMS} @ ${PA.source.commit}`, gens,
    ratio_old: pp.ratio_net, ratio_new: PA.ratio_net, part_a_old: pp.part_a_accrual_bn, part_a_new: PA.part_a_accrual_bn,
    part_a_share: pp.part_a_share, net_old: pi.net_ratio, part_a_per_hi_old: pi.part_a_per_hi_tax, f_net, f_part_a, checks };
}

// The two pension rules on a set of models: per model and allocation, the old and new accrual (the September 29
// split's rule, then with the 2026 ratios) and the receipts it keys on. models: {g: its September 29 model}.
function pensionSplit(PI, gens, top, models) {
  const oasdi = Object.fromEntries(gens.map((g) => [g, X.V4.oasdiOf(models[g])]));
  const hi = Object.fromEntries(gens.map((g) => [g, X.V4.hiOf(models[g])]));
  for (const g of gens) if (!PI.gens.includes(top[g])) blocked(`model ${g}: its generation ${top[g]} has no pension ratio`);
  const total = (f) => byAlloc((a) => sum(gens.map((g) => f(g, a))));
  const oasdiU = total((g, a) => oasdi[g][a]), hiU = total((g, a) => hi[g][a]);
  // amount(a) spread over the models in proportion to w(g, a) (v4_split.cjs split(): refs.oasdi and partAScale).
  const spread = (amount, w) => { const W = total(w); return Object.fromEntries(gens.map((g) => [g, byAlloc((a) => amount(a) * w(g, a) / W[a])])); };
  const ssOld = spread((a) => PI.ratio_old * oasdiU[a], (g, a) => PI.net_old[top[g]] * oasdi[g][a]);
  const ssNew = spread((a) => PI.ratio_new * oasdiU[a], (g, a) => PI.net_old[top[g]] * PI.f_net[top[g]] * oasdi[g][a]);
  const paOld = spread(() => PI.part_a_old, (g, a) => PI.part_a_per_hi_old[top[g]] * hi[g][a]);
  const paNew = spread(() => PI.part_a_new, (g, a) => PI.part_a_per_hi_old[top[g]] * PI.f_part_a[top[g]] * hi[g][a]);
  return { oasdi, hi, oasdi_union: oasdiU, hi_union: hiU, ss_old: ssOld, ss_new: ssNew, part_a_old: paOld, part_a_new: paNew };
}

// ---------------------------------------------------------------------------------------------------
// The shares a rule gives each model, by allocation (they add to 1), for one edit of an item.
function amountAt(m, side, id, key) {
  if (side === "receipt") {
    const l = lineOf(m, "receipts", id);
    return byAlloc((a) => l.cells[key || MODEL.receipts.reference][a].target_bn);
  }
  const l = lineOf(m, "spending", id);
  const k = l.keys[key] ? key : l.preferred_key;
  return byAlloc((a) => l.keys[k][a].target_bn);
}
function parentOf(L, e) {
  if (e.side !== "spending") return { side: "receipt", line: e.line, key: e.scenario };
  const def = (L.payload.lines || []).find((l) => l.id === e.line);
  if (def && def.parent) return { side: "spending", line: def.parent, key: null };
  if (def) blocked(`payload line ${e.line} has no parent to share it by`);
  return { side: "spending", line: e.line, key: e.key };
}
// The parent line an item's meta names for one of its parts or carriers (meta.<key>.splits.split_basis[name], for the
// meta keys the item changes), at the line's preferred key. An item that declares a split_basis must name every part
// and carrier in it; one that declares none gets null (the edited line).
function splitBasis(L, it, name) {
  const bases = (it.record.meta_changed || []).map((k) => [k, L.payload.meta[k] && L.payload.meta[k].splits && L.payload.meta[k].splits.split_basis])
    .filter(([, S]) => S);
  if (!bases.length) return null;
  const hit = bases.filter(([, S]) => S[name]);
  if (hit.length !== 1) blocked(`item ${it.id}: its split_basis names ${hit.length ? "more than one parent" : "no parent"} for ${name}`);
  const [k, S] = hit[0];
  if (!MODEL.spending.lines.some((l) => l.id === S[name])) blocked(`item ${it.id}: split_basis ${name} names ${S[name]}, no spending line`);
  return { side: "spending", line: S[name], key: null, from: `meta.${k}.splits.split_basis` };
}
// A carrier line at a model's shares of the union's: each cell's amount and share times the model's share, the rest of
// the nation in other_bn, as the generation models carry their receipt cells.
const scaledCarrier = (line, s) => Object.assign(clone(line), { cells: Object.fromEntries(Object.entries(line.cells).map(([sc, c]) => [sc, byAlloc((a) => {
  const t = s[a] * c[a].target_bn;
  return Object.assign({}, c[a], { target_bn: t, other_bn: line.national_bn - t, share: s[a] * c[a].share });
})])) });
function sharesFor(rule, ctx, e) {
  const { gens, top, models29, union29, pension, g3plus, alt } = ctx;
  const flat = (f) => Object.fromEntries(gens.map((g) => [g, byAlloc((a) => f(g, a))]));
  if (rule === "lineage") return flat((g) => (g === g3plus ? 1 : 0));
  if (rule === "pension_oasdi" || rule === "pension_part_a") {
    const S = pension;
    if (alt.has("pension_receipt_shares")) {
      return rule === "pension_oasdi" ? flat((g, a) => S.oasdi[g][a] / S.oasdi_union[a])
        : flat((g, a) => S.part_a_old[g][a] / sum(gens.map((h) => S.part_a_old[h][a])));
    }
    const [n, o] = rule === "pension_oasdi" ? [S.ss_new, S.ss_old] : [S.part_a_new, S.part_a_old];
    const d = (g, a) => n[g][a] - o[g][a];
    return flat((g, a) => d(g, a) / sum(gens.map((h) => d(h, a))));
  }
  if (rule === "parent_line") {
    const p = ctx.parent || parentOf(ctx.L, e);
    const u = amountAt(union29, p.side, p.line, p.key);
    return flat((g, a) => amountAt(models29[g], p.side, p.line, p.key)[a] / u[a]);
  }
  blocked(`no rule ${rule}`);
}

// The edit sets on each model: {edits: {g: [its edits, in the payload's order]}, record: per item, edit and part, the
// rule and each model's share and amount}. models29 add to union29 (the September 29 union's model).
function itemSplit(L, gens, top, models29, union29, alt) {
  const g3 = gens.filter((g) => top[g] === "G3plus");
  if (g3.length !== 1) blocked(`the added people's parts go on exactly one G3+ model; ${g3.length} found`);
  const edits = Object.fromEntries(gens.map((g) => [g, []]));
  const receiptLines = Object.fromEntries(gens.map((g) => [g, []])), byItem = Object.fromEntries(gens.map((g) => [g, {}]));
  const record = [];
  let pension = null;
  for (const it of L.items) {
    const R = RULES[it.id];
    if (!R) blocked(`item ${it.id} (${L.rel} meta.items) has no rule in v6_split.cjs RULES`);
    const parts = it.record.parts || {};
    const rec = { id: it.id, first: it.first, count: it.edits.length, edits: [] };
    // Its carriers first, as the package applies them with the item's edits.
    for (const g of gens) byItem[g][it.id] = [];
    if (it.receipt_lines.length) {
      if (R.carriers !== "parent_line") blocked(`item ${it.id}: its carriers have no rule (RULES.${it.id}.carriers parent_line)`);
      rec.carriers = it.receipt_lines.map((line) => {
        const parent = splitBasis(L, it, line.id) || blocked(`item ${it.id}: carrier ${line.id} has no split_basis in its meta`);
        const share = sharesFor("parent_line", { L, gens, top, models29, union29, alt, parent }, null);
        for (const g of gens) byItem[g][it.id].push(scaledCarrier(line, share[g]));
        return { id: line.id, rule: "parent_line", parent: parent.line, parent_from: parent.from,
          union_value: byAlloc((a) => line.cells[MODEL.receipts.reference][a].share), share,
          value: Object.fromEntries(gens.map((g) => [g, byAlloc((a) => share[g][a] * line.cells[MODEL.receipts.reference][a].share)])) };
      });
      for (const g of gens) receiptLines[g].push(...byItem[g][it.id]);
    }
    it.edits.forEach((e, j) => {
      if (e.national_bn !== undefined) {
        for (const g of gens) edits[g].push(clone(e));
        rec.edits.push({ edit: j, side: e.side, line: e.line, national_bn: e.national_bn, rule: "as_is" });
        return;
      }
      const mine = Object.entries(parts).filter(([, p]) => p.edit === j);
      const pieces = mine.length ? mine.map(([name, p]) => ({ name, by: p.by, rule: ruleOf(R, name) })) : [{ name: "*", by: e.by, rule: R["*"] }];
      for (const p of pieces) if (!p.rule) blocked(`item ${it.id}: no rule for part ${p.name} of edit ${j} (${e.line})`);
      if (mine.length && ALLOCS.some((a) => Math.abs(sum(pieces.map((p) => p.by[a])) - e.by[a]) > 1e-12)) blocked(`item ${it.id}: the parts of edit ${j} do not add to it`);
      if (pieces.some((p) => p.rule.startsWith("pension_")) && !pension) {
        const PI = pensionInputs(L, it.record);
        pension = Object.assign({ inputs: PI }, pensionSplit(PI, gens, top, models29));
      }
      const onModelLine = e.side !== "spending" || !(L.payload.lines || []).some((l) => l.id === e.line);
      for (const p of pieces) {
        if (p.rule !== "parent_line") continue;
        p.parent = (alt.has("split_basis_edited_line") && onModelLine ? null : splitBasis(L, it, p.name)) || parentOf(L, e);
      }
      const ctx = { L, gens, top, models29, union29, pension, g3plus: g3[0], alt };
      const shares = Object.fromEntries(pieces.map((p) => [p.name, sharesFor(p.rule, Object.assign({}, ctx, { parent: p.parent }), e)]));
      for (const g of gens) {
        edits[g].push(Object.assign(clone(e), { by: byAlloc((a) => sum(pieces.map((p) => p.by[a] * shares[p.name][g][a]))) }));
      }
      rec.edits.push({ edit: j, side: e.side, line: e.line, key: e.key, scenario: e.scenario,
        parts: pieces.map((p) => ({ name: p.name, rule: p.rule, parent: p.parent ? p.parent.line : undefined, union_bn: p.by, share: shares[p.name],
          bn: Object.fromEntries(gens.map((g) => [g, byAlloc((a) => p.by[a] * shares[p.name][g][a])])) })) });
    });
    record.push(rec);
  }
  return { edits, receipt_lines: receiptLines, item_receipt_lines: byItem, record, pension, g3plus: g3[0] };
}

// ---------------------------------------------------------------------------------------------------
// The v6 part of each model: v5_split.cjs layer() on the lineage block (the added people on G3+, row 8 by share), then
// the edit sets by RULES. Returns layer()'s fields, with parts[g] = {edits (the lineage block's part, then the items'),
// lineage_edits, item_edits, row8, production}, and items (the split's record) and pension (the rule's amounts).
function layer(L, gens, top, models29, union29, opts) {
  const alt = new Set((opts && opts.alt) || []);
  for (const x of alt) if (!ALTERNATIVES[x]) blocked(`unknown alternative ${x}`);
  const lay = V5.layer(L, gens, top, models29, union29, { alt: [...alt].filter((x) => V5.ALTERNATIVES[x]) });
  const split = itemSplit(L, gens, top, models29, union29, alt);
  if (split.g3plus !== lay.g3plus) blocked("the lineage and the items' added-people parts are on different models");
  const parts = Object.fromEntries(gens.map((g) => [g, Object.assign({}, lay.parts[g], { lineage_edits: lay.parts[g].edits,
    item_edits: split.edits[g], edits: lay.parts[g].edits.concat(split.edits[g]),
    receipt_lines: split.receipt_lines[g], item_receipt_lines: split.item_receipt_lines[g] })]));
  return Object.assign({}, lay, { parts, items: split.record, pension: split.pension });
}

// A generation payload: v5_split.cjs payloadOf() (the September 29 payload, the part's edits and grid), with the part's
// carrier receipt lines after the September 29 receipt lines, as the case's payload carries the union's.
function payloadOf(p29, part) {
  const p = V5.payloadOf(p29, part);
  if (part.receipt_lines && part.receipt_lines.length) p.receipt_lines = p.receipt_lines.concat(clone(part.receipt_lines));
  return p;
}
// A model with an item's step on it: its carrier receipt lines and its edits (package.cjs forItems applies them together).
const withStep = (m, edits, receiptLines) => (edits.length || (receiptLines && receiptLines.length)
  ? Engine.applyCorrections(m, { lines: [], receipt_lines: receiptLines || [], edits, meta: m.corrections }) : m);

// The consumer on the v6 payload (v4_split.cjs evaluator(): candidate v4's consumer.cjs) for any model: a model without
// the items' carriers takes them at zero, as the package's withSyntheticLines() adds them (gated equal), so the items'
// capital components key to 0 on it.
function evaluator(payload, api) {
  const ev = X.evaluator(payload);
  const ids = (api.ITEM_RECEIPT_LINES || []).map((l) => l.id);
  if (!ids.length) return ev;
  const zero = payload.receipt_lines.filter((l) => ids.includes(l.id)).map((l) => Object.assign(clone(l), {
    cells: Object.fromEntries(Object.entries(l.cells).map(([sc, c]) => [sc, byAlloc((a) => Object.assign({}, c[a], { target_bn: 0, other_bn: 0, share: 0 }))])) }));
  const pick = (m) => JSON.stringify(m.receipts.lines.filter((l) => ids.includes(l.id)));
  if (pick(api.withSyntheticLines(MODEL)) !== pick(Engine.applyCorrections(MODEL, { lines: [], receipt_lines: zero, edits: [] }))) {
    blocked(`the zero carriers are not ${V6_LANE}/package.cjs withSyntheticLines()'s`);
  }
  const memo = new WeakMap();
  function prepared(m0) {
    if (memo.has(m0)) return memo.get(m0);
    const have = ids.filter((id) => m0.receipts.lines.some((l) => l.id === id));
    if (have.length && have.length !== ids.length) blocked(`a model with ${have.length} of the ${ids.length} carriers`);
    const m = have.length ? m0 : Engine.applyCorrections(m0, { lines: [], receipt_lines: zero, edits: [], meta: m0.corrections });
    memo.set(m0, m);
    return m;
  }
  return { specs: ev.specs, evaluateFull: (m0, spec) => ev.evaluateFull(prepared(m0), spec), cost: (m0, spec) => ev.cost(prepared(m0), spec) };
}

// ---------------------------------------------------------------------------------------------------
// The added people's adults at the case's measured age mix (meta.lineage.age_mix): each count part (G3-rate persons,
// later losses) at its own mix, with every band from 20 adult, none under 15, and the 15-19 band's adults at the
// identified G3+'s share of it, theta, solved from the identified G3+'s adult share (row-4 weights) and its mix
// [APPROX: ages 18-19 split from the 15-19 band as the identified G3+'s]. v5 put them all at the identified adult share.
function addedAdults(lin, idAdultShare) {
  const M = lin.age_mix;
  if (!M || !M.mixes || !Array.isArray(M.bands)) blocked("meta.lineage.age_mix: no mixes");
  const i15 = M.bands.indexOf("15-19"), i20 = M.bands.indexOf("20-24");
  if (i15 < 0 || i20 !== i15 + 1 || M.bands.slice(0, i15).some((b) => Number(b.split("-")[1]) >= 15)) blocked("meta.lineage.age_mix: bands not in five-year order");
  const over20 = (mix) => sum(mix.slice(i20));
  for (const k of ["identified", "g3_rate", "later"]) if (!M.mixes[k] || Math.abs(sum(M.mixes[k]) - 1) > 1e-12) blocked(`meta.lineage.age_mix: mix ${k} does not sum to 1`);
  const theta = (idAdultShare - over20(M.mixes.identified)) / M.mixes.identified[i15];
  if (!(theta > 0 && theta < 1)) blocked(`theta ${theta}: the identified adult share is not inside the 15-19 band`);
  const share = (mix) => over20(mix) + theta * mix[i15];
  const c = lin.counts;
  const parts = { g3_rate: c.at_g3_rate * share(M.mixes.g3_rate), later: c.later_losses * share(M.mixes.later) };
  if (Math.abs(c.at_g3_rate + c.later_losses - c.added) > 1e-6) blocked("meta.lineage.counts: the parts do not add to the added people");
  const adults = parts.g3_rate + parts.later;
  return { adults, adult_share: adults / c.added, theta, by_part: parts, part_shares: { g3_rate: share(M.mixes.g3_rate), later: share(M.mixes.later) },
    identified_adult_share: idAdultShare, v5_rule_adults: c.added * idAdultShare };
}

// ---------------------------------------------------------------------------------------------------
// The v6 package on the case's payload (its evaluateFull at its MAIN_SPECS), to cross-check evaluator() on every model.
function adoptedPackage(L) {
  return { source: `${V6_LANE}/package.cjs${L.set === "set" ? "" : " CASH"}`, specs: L.api.MAIN_SPECS,
    cost: (m, i) => L.api.evaluateFull(m, L.api.MAIN_SPECS[i], L.api.MAIN_PROFILE).cost_bn };
}
// The oracle: the case lane's published band (main_case_bands.csv, four decimals) and its full-precision band
// (summary.json), its end specifications, and the uncorrected model's band at the case's responses.
function oracle(set) {
  const variant = set === "set" ? "adopted" : "cash_set";
  const rows = X.P.csvRows(`${V6_LANE}/derived/main_case_bands.csv`).filter((x) => x.profile === X.P.MAIN_PROFILE);
  const r = rows.find((x) => x.variant === variant), u = rows.find((x) => x.variant === "uncorrected_at_adopted_responses");
  const S = readJson(`${V6_LANE}/derived/summary.json`);
  const ends = set === "set" ? S.end_specifications.map((x) => [x.low_end.index, x.high_end.index]) : S.cash_set.end_specifications;
  if (!r || !u || !ends.length || !ends.every((x) => x[0] === ends[0][0] && x[1] === ends[0][1])) {
    blocked(`${V6_LANE}: no ${variant} and uncorrected rows in main_case_bands.csv, or the methods' ends differ`);
  }
  return { source: `${V6_LANE}/derived/main_case_bands.csv (${variant})`, specs: ends[0].map(Number),
    band: [Number(r.cost_low_bn), Number(r.cost_high_bn)], uncorrected: [Number(u.cost_low_bn), Number(u.cost_high_bn)],
    full: { source: `${V6_LANE}/derived/summary.json ${set === "set" ? "main_case" : "cash_set.band_bn"}`, band: set === "set" ? S.main_case : S.cash_set.band_bn } };
}
// The lane's cost at every specification, the mean of the two fill-in methods (the set only).
function perSpec(set) {
  if (set !== "set") return null;
  const rows = X.P.csvRows(`${V6_LANE}/derived/per_spec.csv`);
  const out = new Map();
  for (const i of [...new Set(rows.map((r) => Number(r.spec)))]) {
    const rs = rows.filter((r) => Number(r.spec) === i);
    if (rs.length !== X.METHODS.length || !X.METHODS.every((m) => rs.some((r) => r.method === m))) blocked(`spec ${i}: not one row per method`);
    out.set(i, sum(rs.map((r) => Number(r.cost_bn))) / rs.length);
  }
  return { source: `${V6_LANE}/derived/per_spec.csv cost_bn`, cost: out };
}
// The case lane's change from v5 at the end specifications by item (summary.json change_at_fixed_specifications.items,
// each item alone on v5, and v6.interactions), for the set or the cash set.
function caseParts(set) {
  const S = readJson(`${V6_LANE}/derived/summary.json`);
  const CF = S.change_at_fixed_specifications, I = S.v6.interactions;
  const alone = Object.fromEntries(Object.entries(CF.items).map(([id, v]) => [id, set === "set" ? v.total : (v.cash ? v.cash.total : null)]));
  const pair = (a, b) => {
    const x = I[`${a}_x_${b}`] || I[`${b}_x_${a}`];
    return x ? (set === "set" ? x.at_end_specifications_bn : x.cash_at_end_specifications_bn) : null;
  };
  const remainder = I.remainder ? (set === "set" ? I.remainder.at_end_specifications_bn : I.remainder.cash_at_end_specifications_bn) : null;
  return { source: `${V6_LANE}/derived/summary.json change_at_fixed_specifications.items and v6.interactions`, alone, pair, remainder,
    change: set === "set" ? S.v6.change_from_the_october_5_case_bn : S.v6.change_from_the_october_5_cash_set_bn,
    lineage_item_parts: S.v6.lineage_item_parts[set === "set" ? "set" : "cash"], v5: set === "set" ? S.adopted_2026_10_05 : S.v6.base.cash_set_bn };
}

module.exports = { V6_LANE, V6_FILES, P6, V5, X, RULES, RULE_TEXT, ALTERNATIVES, PENSION_ALTERNATIVES, loadCase, layer,
  itemSplit, pensionInputs, pensionSplit, addedAdults, payloadOf, withStep, withEdits: V5.withEdits, evaluator, adoptedPackage, oracle,
  perSpec, caseParts };
