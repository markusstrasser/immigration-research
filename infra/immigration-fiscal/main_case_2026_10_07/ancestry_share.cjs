/* Companion reading: a case of this package (package.cjs caseOf) counted by each member's share of Mexican-immigrant
 * ancestry instead of whole, the lineage lane's fractional count (main_case_lineage_2026_10_05/lineage_case.cjs lines
 * 578-627, committed d3b7e6e6; beside the case, never the headline). At each specification
 *   f = G1 + s_G2 x G2 + s_G3+ x G3+ + s_added x added,
 * and the band is f's minimum and maximum over the 64. The scenarios are the lineage lane's stated bound: g4_at_nothing
 * (s_G2 central, s_G3+ bound_low) and g4_at_bound (s_G2 central, s_G3+ bound_high), the added people at their central
 * share (fractional_shares.json).
 *
 * The parts. Each generation of the union is its corrected model (generation_account_2026_09_24 model_G*.json with
 * generation_corrections_sept29*.json payloads.a, convention a) with its part of row 8's edit, by its share of the
 * union's lane-constants cell (lineage_case.cjs generationCosts()), and its part of the edit sets' edits; the added
 * people are the case less the three generations. The edit sets' edits split by generation by the rule api_check.cjs
 * pattern 3 states and gates for consumers:
 *   - national-scale edits (item retiree_health) as they are on each generation model, so each generation's cells
 *     scale by the case's factor;
 *   - item pension_tr2026's union parts by each generation's share of the union's OASDI receipts and Part A accrual on
 *     the September 29 payloads [ASSUMPTION; the sensitivity splits them by the pension lane's own per-generation
 *     changes, pension_tr2026_2026_10_06/derived/arms.csv], its lineage parts on the added people;
 *   - item user_fees's parts and carriers by each generation's share of the split-basis line's union amount
 *     (meta.user_fees.splits.split_basis, the item's consumer rule) [ASSUMPTION], none on the added people.
 * Item added_age_mix changes the added people's addition, so it enters the added part whole.
 *
 * Gates (thrown as [BLOCKED]): each generation's corrected payload splits the case's September 29 payload; the rule's
 * bases and the lane-constants cells add over the generations to the union's; the generations with their parts add to the
 * union's model with the same edits (row 8's and the edit sets' union parts, unsplit) at every specification (1e-9).
 * main_case.cjs gates the count on v5 (no item) against the lineage lane's rows (v5_summary.json fractional.rows).
 *
 * rowsFor(Q, which, tools) -> the scenarios' rows for the set or the cash set. Run nothing: a module.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const FISCAL = path.join(__dirname, "..");
const LINEAGE_LANE = "main_case_lineage_2026_10_05";
const ROUTE = { file: `${LINEAGE_LANE}/lineage_case.cjs`, commit: "d3b7e6e6" };
const GEN = "generation_account_2026_09_24/derived";
const GENS = ["G1", "G2", "G3plus"];
const GEN_FILES = { set: "generation_corrections_sept29.json", cash: "generation_corrections_sept29_cash.json" };
const SHARES_FILE = `${LINEAGE_LANE}/derived/fractional_shares.json`;
const PENSION_ARMS = "pension_tr2026_2026_10_06/derived/arms.csv";
const ALLOCS = ["personal", "shared"];
const SCENARIOS = [
  ["g4_at_nothing", "bound_low", "the stated bound's low end: third generation at a quarter per Mexico-born grandparent, G4+ at nothing"],
  ["g4_at_bound", "bound_high", "the stated bound's high end: third generation at a quarter per Mexico-born grandparent, G4+ at its measured high bound"],
];
const RULES = {
  count: "f = G1 + s_G2 G2 + s_G3+ G3+ + s_added added at each specification, the band its minimum and maximum over the 64 (lineage_case.cjs's fractional count)",
  parts: "each union generation: its corrected model (convention a), its part of row 8's edit by its share of the union's lane-constants cell, and its part of the edit sets' edits; the added people: the case less the three generations",
  national_scale: "national-scale edits (item retiree_health) as they are on each generation model: each generation's cells scale by the case's factor",
  pension: "[ASSUMPTION] item pension_tr2026's union parts by each generation's share of the union's OASDI receipts (union_oasdi) and Part A accrual (union_part_a) on the September 29 payloads; its lineage parts on the added people",
  user_fees: "[ASSUMPTION] item user_fees's parts and carriers by each generation's share of the split-basis line's union amount at the line's preferred key (meta.user_fees.splits.split_basis); none on the added people",
  age_mix: "item added_age_mix changes the added people's addition: it enters the added part whole, at s_added",
};
const clone = (x) => JSON.parse(JSON.stringify(x));
const readJson = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const blocked = (why) => { throw new Error("[BLOCKED] ancestry_share: " + why); };

// The pension lane's per-generation change of the union parts' bases, arm over control (arms.csv): the sensitivity's
// shares for union_oasdi (the net accrual per tax dollar times the tax) and union_part_a.
function pensionShares(csvRows, arm) {
  const rows = csvRows(PENSION_ARMS);
  const at = (a, g) => { const r = rows.find((x) => x.arm === a && x.group === g); if (!r) blocked(`${PENSION_ARMS} has no row ${a} ${g}`); return r; };
  const d = (g) => ({ union_oasdi: (Number(at(arm, g).net_per_tax_dollar) - Number(at("control", g).net_per_tax_dollar)) * Number(at(arm, g).oasdi_tax_bn),
    union_part_a: Number(at(arm, g).part_a_bn) - Number(at("control", g).part_a_bn) });
  const ds = Object.fromEntries(GENS.map((g) => [g, d(g)]));
  return Object.fromEntries(["union_oasdi", "union_part_a"].map((k) => {
    const t = GENS.reduce((s, g) => s + ds[g][k], 0);
    return [k, Object.fromEntries(GENS.map((g) => [g, ds[g][k] / t]))];
  }));
}

// One set of case Q: the generation models with their parts, and the count at every specification.
function rowsFor(Q, which, tools) {
  const { Engine } = tools;
  const api = which === "set" ? Q : Q.CASH, sept = which === "set" ? Q.SEPT29 : Q.SEPT29_CASH;
  const specs = api.MAIN_SPECS, PROFILE = Q.MAIN_PROFILE;
  const pl = api.correctionsPayload(), L = pl.meta.lineage;
  const gp = readJson(`${GEN}/${GEN_FILES[which]}`);
  if (gp.meta.union !== Q.BASE_FILES[which]) blocked(`${GEN_FILES[which]} splits ${gp.meta.union}, not ${Q.BASE_FILES[which]}`);
  const GM = Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(readJson(`${GEN}/model_${g}.json`), gp.payloads.a[g])]));
  const U = sept.payloadModel();
  // Row 8's edit by each generation's share of the union's lane-constants cell (lineage_case.cjs setUp(), generationCosts()).
  const kCell = (m) => m.spending.lines.find((l) => l.id === "lane_constants").keys.k;
  const kShare = Object.fromEntries(GENS.map((g) => [g, Object.fromEntries(ALLOCS.map((a) => [a, kCell(GM[g])[a].target_bn / kCell(U)[a].target_bn]))]));
  const kSum = Math.max(...ALLOCS.map((a) => Math.abs(GENS.reduce((s, g) => s + kShare[g][a], 0) - 1)));
  if (!(kSum < 1e-12)) blocked(`${which}: the generation models' lane-constants cells do not add to the union's (${kSum})`);
  const d8 = L.edits.row8_edit_bn;
  const row8 = (f) => ({ side: "spending", line: "lane_constants", key: "k", by: { personal: d8 * f.personal, shared: d8 * f.shared } });
  // The rule's bases, read as package.cjs pensionBasis() reads the union's, and user_fees's split-basis lines. Q is a case's
  // set API (or v5's module): the cash set's items are its CASH's, on its item base's CASH.
  const recs = (api.CASE_ITEMS || []).filter((r) => r.applied && r.edits);
  const N_BASE = recs.length ? (which === "set" ? Q.ITEM_BASE : Q.ITEM_BASE.CASH).correctionsPayload().edits.length : 0;
  const needsPension = recs.some((r) => Object.keys(r.parts || {}).some((k) => k === "union_oasdi" || k === "union_part_a"));
  const PA = pl.meta.pension_accrual, REF = Q.MODEL.receipts.reference;
  if (needsPension && !PA) blocked(`${which}: item pension_tr2026's parts without a pension block`);
  const GMc = needsPension ? (() => { const gpc = readJson(`${GEN}/${GEN_FILES.cash}`);
    return Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(readJson(`${GEN}/model_${g}.json`), gpc.payloads.a[g])])); })() : null;
  const rcp = (m, id, a) => m.receipts.lines.find((l) => l.id === id).cells[REF][a].target_bn;
  const grp = (m, id, a) => { const l = m.spending.lines.find((x) => x.id === id); return l.keys[l.preferred_key][a].target_bn; };
  const oasdiOf = (m, a) => PA.oasdi_lines.reduce((s, id) => s + rcp(m, id, a), 0) + PA.se_oasdi_share * rcp(m, PA.se_line, a);
  const partAOf = (ms, mc, a) => grp(ms, "medicare", a) - (1 - PA.part_a_share) * grp(mc, "medicare", a);
  const SPLIT = pl.meta.user_fees ? pl.meta.user_fees.splits.split_basis : {};
  const BASIS = needsPension ? { union_oasdi: (g, a) => oasdiOf(GM[g], a), union_part_a: (g, a) => partAOf(GM[g], GMc[g], a) } : {};
  const lineShare = (id, g, a) => grp(GM[g], id, a) / GENS.reduce((t, x) => t + grp(GM[x], id, a), 0);
  const unionLineGap = Math.max(0, ...[...new Set(Object.values(SPLIT))].flatMap((id) => ALLOCS.map((a) => Math.abs(GENS.reduce((t, g) => t + grp(GM[g], id, a), 0) - grp(U, id, a)))));
  if (!(unionLineGap < 1e-9)) blocked(`${which}: user_fees's split-basis lines do not add over the generations to the union's (${unionLineGap})`);
  // A share function for the rule, or for the sensitivity's pension shares (measured: {part: {gen: share}}).
  const shareFn = (measured) => (name, g, a) => {
    if (name.startsWith("lineage_")) return 0;
    if (BASIS[name]) return measured ? measured[name][g] : BASIS[name](g, a) / GENS.reduce((t, x) => t + BASIS[name](x, a), 0);
    if (SPLIT[name]) return lineShare(SPLIT[name], g, a);
    return blocked(`${which}: part ${name} has no generation rule`);
  };
  // The edit sets' edits on generation g (or, with g null, on the union: every union part, no lineage part).
  const itemEditsFor = (g, share) => recs.flatMap((r) => api.ITEM_EDITS.slice(r.edits.first - N_BASE, r.edits.first - N_BASE + r.edits.count).map((e, j) => {
    if (e.national_bn !== undefined) return clone(e);
    const parts = Object.entries(r.parts || {}).filter(([, p]) => p.edit === j);
    if (!parts.length) blocked(`${which}: item ${r.id}'s cell shift ${j} has no parts to split by generation`);
    return Object.assign(clone(e), { by: Object.fromEntries(ALLOCS.map((a) => [a, parts.reduce((t, [name, p]) => t + p.by[a] * (g === null ? (name.startsWith("lineage_") ? 0 : 1) : share(name, g, a)), 0)])) });
  }));
  const carriersFor = (g, share) => (api.ITEM_RECEIPT_LINES || []).map((l) => {
    if (!SPLIT[l.id]) blocked(`${which}: carrier ${l.id} has no split basis`);
    if (g === null) return clone(l);
    return Object.assign(clone(l), { cells: Object.fromEntries(Object.entries(l.cells).map(([sc, c]) => [sc, Object.fromEntries(ALLOCS.map((a) => {
      const f = share(l.id, g, a);
      return [a, Object.assign({}, c[a], { target_bn: c[a].target_bn * f, other_bn: l.national_bn - c[a].target_bn * f, share: c[a].share * f })];
    }))])) });
  });
  const withParts = (m, edits, carriers) => Engine.applyCorrections(m, { receipt_lines: carriers, edits, meta: m.corrections });
  const genModels = (share) => Object.fromEntries(GENS.map((g) => [g, withParts(GM[g], [row8(kShare[g])].concat(itemEditsFor(g, share)), carriersFor(g, share))]));
  const cost = (m, s) => api.evaluateFull(m, s, PROFILE).cost_bn;
  const rule = shareFn(null);
  const gens = genModels(rule);
  const U6 = withParts(U, [row8({ personal: 1, shared: 1 })].concat(itemEditsFor(null)), carriersFor(null));
  const caseM = api.payloadModel();
  const gc = Object.fromEntries(GENS.map((g) => [g, specs.map((s) => cost(gens[g], s))]));
  const uc = specs.map((s) => cost(U6, s)), cc = specs.map((s) => cost(caseM, s));
  const addGap = Math.max(...specs.map((_, i) => Math.abs(GENS.reduce((t, g) => t + gc[g][i], 0) - uc[i])));
  if (!(addGap < 1e-9)) blocked(`${which}: the generations with their parts do not add to the union's model with the same edits (${addGap})`);
  const added = cc.map((c, i) => c - uc[i]);
  const SH = readJson(SHARES_FILE).shares;
  const nAdded = L.counts.added;
  const count = (sh, g3, ad, gcost) => specs.map((_, i) => gcost.G1[i] + sh.G2 * gcost.G2[i] + g3 * gcost.G3plus[i] + SH.added.central * ad[i]);
  const rowOf = ([scenario, bound, label], gcost, ad) => {
    const sh = { G2: SH.G2.central, G3plus: SH.G3plus[bound] };
    const f = count(sh, sh.G3plus, ad, gcost);
    const lo = f.indexOf(Math.min(...f)), hi = f.indexOf(Math.max(...f));
    const pop = SH.G1.population + sh.G2 * SH.G2.population + sh.G3plus * SH.G3plus.population + SH.added.central * nAdded;
    return { scenario, label: `[FRAMING-SENSITIVE] ${label}`, s_g2: sh.G2, s_g3plus: sh.G3plus, s_added: SH.added.central, fractional_population: pop,
      band_bn: [f[lo], f[hi]], ends: [lo, hi], per_member_usd: [f[lo] * 1e9 / pop, f[hi] * 1e9 / pop], whole_person_band_bn: [Math.min(...cc), Math.max(...cc)],
      parts_at_ends_bn: { G1: [gcost.G1[lo], gcost.G1[hi]], G2: [gcost.G2[lo], gcost.G2[hi]], G3plus: [gcost.G3plus[lo], gcost.G3plus[hi]], added: [ad[lo], ad[hi]] },
      costs: f };
  };
  const rows = SCENARIOS.map((sc) => rowOf(sc, gc, added));
  // The sensitivity: item pension_tr2026's union parts by the pension lane's per-generation changes.
  let pension = null;
  if (needsPension) {
    const arm = pl.meta.pension_accrual.source.arm, ms = pensionShares(Q.csvRows, arm);
    const gm = genModels(shareFn(ms));
    const gcm = Object.fromEntries(GENS.map((g) => [g, specs.map((s) => cost(gm[g], s))]));
    const gap = Math.max(...specs.map((_, i) => Math.abs(GENS.reduce((t, g) => t + gcm[g][i], 0) - uc[i])));
    if (!(gap < 1e-9)) blocked(`${which}: with the measured pension shares the generations do not add to the union's model (${gap})`);
    pension = { rule: `item pension_tr2026's union parts by the pension lane's per-generation changes, arm ${arm} over control (${PENSION_ARMS}: the net accrual per tax dollar times the tax, and Part A)`,
      shares: ms, rule_shares: Object.fromEntries(["union_oasdi", "union_part_a"].map((k) => [k, Object.fromEntries(GENS.map((g) => [g, ALLOCS.map((a) => rule(k, g, a))]))])),
      rows: SCENARIOS.map((sc) => { const r = rowOf(sc, gcm, added), r0 = rows.find((x) => x.scenario === sc[0]);
        return { scenario: sc[0], band_bn: r.band_bn, ends: r.ends, change_bn: [r.band_bn[0] - r0.band_bn[0], r.band_bn[1] - r0.band_bn[1]] }; }) };
  }
  return { which, rows, added_people: nAdded, row8_edit_bn: d8, k_share: kShare, union_band_bn: [Math.min(...uc), Math.max(...uc)], case_costs: cc, added_costs: added,
    generation_costs: gc, pension_sensitivity: pension };
}

module.exports = { rowsFor, SCENARIOS, RULES, ROUTE, SHARES_FILE, PENSION_ARMS };
