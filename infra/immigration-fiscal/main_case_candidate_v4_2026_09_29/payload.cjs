/* Candidate v4's adoption payload, built so that an operator's "go" can land at once. Nothing is adopted: meta.adopted
 * and meta.decision stay null until the operator decides.
 *
 * derived/corrections_v4.json is the set (pension accrual at payable benefits, net of the tax on benefits) and
 * derived/corrections_v4_cash.json the cash set, in the schema of the adopted
 * main_case_long_run_2026_09_27/derived/corrections.json. Each is that payload, rebuilt by its package's
 * correctionsPayload() and gated byte for byte against the file, followed by v4's parts. Those parts are read off the
 * two fill-in methods' models (package.cjs modelFor) against the September 27 case's models:
 *   receipt_lines  the receipt lines the set adds (public housing's deficit, item 1; the tenant-occupied property tax,
 *                  item 5), each cell the two methods' mean;
 *   edits          after the September 27 edits, a national-scale edit {side, line, national_bn} for each line whose
 *                  national total the set changes (items 1 and 5), then one ordinary edit per cell the set moves, by the
 *                  two methods' mean change beyond the scale (package.cjs composes the items on a shared cell);
 *   lines          the synthetic lines of roads by miles and state pricing;
 *   production     the row-4 grid (item 2);
 *   meta           the September 27 meta with v4's line and receipt responses, its capital keys (item 4, and roads'
 *                  part_rekeyed kind), the pension accrual block (the set only) and provenance.
 * engine.js applies receipt_lines, national-scale edits and production (optional fields since this lane). The cost is
 * linear in every cell amount and in the production grid, so the methods' mean payload gives the methods' mean cost at
 * each specification, and a payload built on one method's model gives that method's.
 *
 * Gates (each prints; any failure exits 1 and writes nothing):
 *   G1      with every item off the builder emits no v4 part, and its payload equals the adopted corrections.json, as
 *           JSON and byte for byte;
 *   G2      consumer.cjs (engine.js, model.json and the payload, no package) gives per_spec.csv's set and cash costs at
 *           all 64 specifications: each method's from a payload built on that method's models, the methods' mean from
 *           the written payloads (1e-6). Its engine state equals the package's at every specification, its capital
 *           components equal the package's, and the payload model equals the methods' mean model cell by cell;
 *   engine  the optional fields work and fail loudly on bad input, and every earlier payload applies and evaluates as
 *           with the engine at ENGINE_PIN.
 * Run: node payload.cjs (after main_case.cjs, whose derived/ it reads) -> derived/corrections_v4.json,
 * derived/corrections_v4_cash.json, derived/payload_gates.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const Module = require("module");
const { execFileSync } = require("child_process");
const V4 = require(path.join(__dirname, "package.cjs"));
const Consumer = require(path.join(__dirname, "consumer.cjs"));
const P = V4.SEPT27;
const { Engine, MODEL, FISCAL, METHODS, ALLOCS, HERE, LANE, ROOT, readJson, csvRows, lineOf } = V4;

const OUT = path.join(HERE, "derived");
const ADOPTED_FILE = "main_case_long_run_2026_09_27/derived/corrections.json";
const ADOPTED_TEXT = fs.readFileSync(path.join(FISCAL, ADOPTED_FILE), "utf8");
const ADOPTED = JSON.parse(ADOPTED_TEXT);
const RUN_COMMIT = "f40e47e";
const ENGINE_PIN = "d710a74";
const ENGINE_PATH = "infra/immigration-fiscal/assumption_explorer_2026_09_21/engine.js";
const serialize = (x) => JSON.stringify(x, null, 1) + "\n";
const sha256 = (s) => crypto.createHash("sha256").update(s).digest("hex");
const fileSha = (rel) => sha256(fs.readFileSync(path.join(FISCAL, rel)));
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const ex = (x) => x.toExponential(1);
const canon = (x) => JSON.stringify(x, (k, v) => (v && typeof v === "object" && !Array.isArray(v)
  ? Object.fromEntries(Object.keys(v).sort().map((kk) => [kk, v[kk]])) : v));

const GATES = [];
function gate(name, pass, detail) {
  GATES.push({ name, pass: !!pass, detail: detail === undefined ? null : detail });
  console.log(`  ${pass ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
}

// ---------------------------------------------------------------------------------------------------
// The September 27 payload and models.
const BASE = P.correctionsPayload();
const M27 = METHODS.map((x) => P.modelFor("central", x, P.withCentral({})));
const PM27 = Engine.applyCorrections(MODEL, BASE);
const SIDES = { receipts: "receipt", spending: "spending" };
const groupsOf = (side, l) => (side === "receipts" ? l.cells : l.keys);
const without = (x, keys) => { const y = Object.assign({}, x); for (const k of keys) delete y[k]; return y; };
const AMOUNTS = ["target_bn", "other_bn", "share"];
const GRID = ["private_wtp_bn", "induced_receipts_bn", "sampling_se_bn"];
// Everything in a model but its lines, its production arrays and the packages' tags; a payload cannot carry a change there.
function frame(m) {
  const x = without(m, ["corrections", "candidate", "corrected"]);
  x.receipts = without(m.receipts, ["lines"]); x.spending = without(m.spending, ["lines"]);
  x.production = without(m.production, GRID);
  return canon(x);
}
const sameArray = (a, b) => a.length === b.length && a.every((v, i) => v === b[i]);

// v4's parts from pairs {m4, base}: new lines and cells at the pairs' mean, national-scale edits where the national total
// moves (the same in every pair), and an edit per cell by the mean of m4 - s x base (s the line's scale, 1 if none).
function partsOf(pairs) {
  const out = { receipt_lines: [], scales: [], edits: [], lines: [], production: null };
  for (const { m4, base } of pairs) {
    if (frame(m4) !== frame(base)) throw new Error("[BLOCKED] v4 changes a part of the model that the payload cannot carry");
  }
  for (const side of Object.keys(SIDES)) {
    const ids = pairs[0].m4[side].lines.map((l) => l.id);
    for (const { m4, base } of pairs) {
      if (m4[side].lines.map((l) => l.id).join() !== ids.join()) throw new Error(`[BLOCKED] the methods' ${side} lines differ`);
      const baseIds = base[side].lines.map((l) => l.id);
      if (baseIds.join() !== ids.slice(0, baseIds.length).join()) throw new Error(`[BLOCKED] v4 drops or reorders a ${side} line`);
    }
    for (const id of ids) {
      const ls = pairs.map(({ m4, base }) => ({ l4: m4[side].lines.find((l) => l.id === id), lb: base[side].lines.find((l) => l.id === id) }));
      const g4 = (x) => groupsOf(side, x.l4), gb = (x) => groupsOf(side, x.lb);
      const groups = Object.keys(g4(ls[0]));
      for (const x of ls) {
        if (Object.keys(g4(x)).join() !== groups.join()) throw new Error(`[BLOCKED] ${id}: the methods' cells differ`);
        for (const g of groups) for (const a of ALLOCS) {
          if (canon(without(g4(x)[g][a], AMOUNTS)) !== canon(without(g4(ls[0])[g][a], AMOUNTS))) throw new Error(`[BLOCKED] ${id}/${g}: the methods' cell attributes differ`);
        }
      }
      if (!ls[0].lb) {
        if (ls.some((x) => x.lb) || ls.some((x) => x.l4.national_bn !== ls[0].l4.national_bn)) throw new Error(`[BLOCKED] ${id}: a new line differs between the methods`);
        const l0 = ls[0].l4;
        if (side === "receipts") {
          const cells = Object.fromEntries(groups.map((g) => [g, Object.fromEntries(ALLOCS.map((a) => [a, Object.assign({},
            without(l0.cells[g][a], AMOUNTS), Object.fromEntries(AMOUNTS.map((k) => [k, mean(ls.map((x) => x.l4.cells[g][a][k]))])))]))]));
          out.receipt_lines.push(Object.assign(without(l0, ["cells", "national_bn"]), { national_bn: l0.national_bn, cells }));
        } else {
          if (l0.national_bn !== 0 || groups.join() !== "k" || l0.preferred_key !== "k" || l0.alternative_key !== "k") {
            throw new Error(`[BLOCKED] ${id}: a new spending line other than a synthetic line at national 0 with key k`);
          }
          out.lines.push({ id, family: l0.family, response_class: l0.response_class, label: l0.label });
          out.edits.push({ side: "spending", line: id, key: "k", by: Object.fromEntries(ALLOCS.map((a) => [a, mean(ls.map((x) => x.l4.keys.k[a].target_bn))])) });
        }
        continue;
      }
      for (const x of ls) {
        if (canon(without(x.l4, ["national_bn", "cells", "keys"])) !== canon(without(x.lb, ["national_bn", "cells", "keys"]))) throw new Error(`[BLOCKED] ${id}: v4 changes the line's attributes`);
        if (Object.keys(gb(x)).join() !== groups.join()) throw new Error(`[BLOCKED] ${id}: v4 changes the line's cells`);
      }
      const scaled = ls.some((x) => x.l4.national_bn !== x.lb.national_bn);
      if (scaled) {
        if (ls.some((x) => x.l4.national_bn !== ls[0].l4.national_bn || x.lb.national_bn !== ls[0].lb.national_bn)) throw new Error(`[BLOCKED] ${id}: the methods scale it differently`);
        out.scales.push({ side: SIDES[side], line: id, national_bn: ls[0].l4.national_bn });
      }
      const s = ls.map((x) => (scaled ? x.l4.national_bn / x.lb.national_bn : 1));
      for (const g of groups) {
        const r = Object.fromEntries(ALLOCS.map((a) => [a, ls.map((x, i) => g4(x)[g][a].target_bn - (scaled ? gb(x)[g][a].target_bn * s[i] : gb(x)[g][a].target_bn))]));
        if (!ALLOCS.some((a) => r[a].some((v) => v !== 0))) continue;
        const by = Object.fromEntries(ALLOCS.map((a) => [a, mean(r[a])]));
        out.edits.push(side === "receipts" ? { side: "receipt", line: id, scenario: g, by } : { side: "spending", line: id, key: g, by });
      }
    }
  }
  const grids = pairs.map(({ m4 }) => m4.production);
  if (pairs.some(({ m4, base }) => GRID.some((k) => !sameArray(m4.production[k], base.production[k])))) {
    if (grids.some((g) => GRID.some((k) => !sameArray(g[k], grids[0][k])))) throw new Error("[BLOCKED] the methods' production grids differ");
    out.production = Object.assign({ dims: Object.fromEntries(Engine.PRODUCTION_DIMS.map((d) => [d, grids[0].dims[d]])) },
      Object.fromEntries(GRID.map((k) => [k, grids[0][k].slice()])));
  }
  return out;
}

// ---------------------------------------------------------------------------------------------------
// Responses: every line response the v4 specifications set beyond the September 27 case's, by reading.
const RESPONSE_NOTES = {
  "receipt:housing_enterprise_surplus": {
    rule: "public housing's enterprise deficit (NIPA 3.8 line 13, housing and urban renewal, -$40.298bn in 2024, less public housing's $5.258bn operating subsidy, consolidated with the rental line) as its own receipt line at the rental line's key; it responds as the enterprise receipt does, in every profile",
    source: "item 1: main_case_candidate_v2_2026_09_28/package.cjs splitHousing" },
  "receipt:modeled_owner_property": {
    rule: "owner-occupied property tax at the long-run owner response (the metro land-price fall), in every profile; the line keeps its key",
    source: "item 5: receipt_side_long_run_2026_09_28/items.cjs RESPONSES.owner.central (derived/housing.json)" },
  "receipt:tenant_occupied_property": {
    rule: "the tax on tenant-occupied housing, split out of remaining_production_property (BEA Table 7.4.5 housing taxes on production x the tenant share of housing output), keyed by the group's share of contract rent, at the long-run renter response in every profile",
    source: "item 5: receipt_side_long_run_2026_09_28/items.cjs splitTenant, RESPONSES.renter.central" },
  "receipt:personal_property_tax": {
    rule: "household personal property tax (NIPA 3.4 line 11), re-keyed to the group's share of household vehicles, at response 1 like the motor-vehicle line, in every profile",
    source: "item 5: receipt_side_long_run_2026_09_28/items.cjs rekey, CENTRAL_ITEMS.personal" },
  roads_vmt_sl: {
    rule: `re-keys the S&L highways part of economic_affairs_services (national $${V4.HWY_N.sl}bn) to the road key; it responds as that subfunction does at the specification's reading (responses.economic_affairs_services.subfunctions sl_highways)`,
    source: "roads: package.cjs withRoads (roads_mileage_key_2026_09_29)" },
  roads_vmt_fed: {
    rule: `re-keys the federal highways part of economic_affairs_services (national $${V4.HWY_N.fed}bn) to the road key; it responds as that subfunction does at the specification's reading (responses.economic_affairs_services.subfunctions fed_highways)`,
    source: "roads: package.cjs withRoads (roads_mileage_key_2026_09_29)" },
  state_price_public_order_safety: {
    rule: "public order and safety's state-price gap (the sum over its S&L functions of amount x (price index - 1)) at the line's use key; it responds as its parent, which the case holds at 1 in every profile",
    source: "state: package.cjs withStatePrice (state_priced_services_2026_09_29, central package)" },
  state_price_health_services: {
    rule: "health's state-price gap at the line's preferred key; it responds as its parent, which the case holds at 1 in every profile",
    source: "state: package.cjs withStatePrice (state_priced_services_2026_09_29, central package)" },
  state_price_recreation_culture: {
    rule: "recreation and culture's state-price gap at the line's preferred key; it responds as its parent, recreation_culture, at the specification's reading",
    source: "state: package.cjs withStatePrice (state_priced_services_2026_09_29, central package)" },
};
const SPEC_FIELDS = ["allocation", "normalization", "share", "school", "gg", "uc", "justice", "reading", "rate", "long_run", "enterprises"];
function responsesOf(oo) {
  const s4 = V4.specsFor(oo), s27 = P.specsFor({}), found = {};
  if (s4.length !== s27.length) throw new Error("[BLOCKED] v4 has another number of specifications");
  s4.forEach((s, i) => {
    const b = s27[i].line_responses;
    for (const f of SPEC_FIELDS) if (s[f] !== s27[i][f]) throw new Error(`[BLOCKED] v4 moves the specification field ${f} at ${i}`);
    for (const id of Object.keys(b)) {
      if (!(id in s.line_responses)) throw new Error(`[BLOCKED] v4 drops the response of ${id}`);
      if (s.line_responses[id] !== b[id]) throw new Error(`[BLOCKED] v4 changes the September 27 response of ${id}`);
    }
    for (const [id, v] of Object.entries(s.line_responses)) {
      if (id in b) continue;
      const e = found[id] || (found[id] = {});
      if (e[s.reading] !== undefined && e[s.reading] !== v) throw new Error(`[BLOCKED] ${id} takes two responses at the ${s.reading} reading`);
      e[s.reading] = v;
    }
  });
  const out = {};
  for (const [id, v] of Object.entries(found)) {
    const note = RESPONSE_NOTES[id];
    if (!note) throw new Error(`[BLOCKED] no note for the new response ${id}`);
    if (!Number.isFinite(v.low) || !Number.isFinite(v.high)) throw new Error(`[BLOCKED] ${id}: no response at one reading`);
    if (id.startsWith("receipt:")) out[id.slice("receipt:".length)] = Object.assign({ receipt: true, override: id, low: v.low, high: v.high }, note);
    else out[id] = Object.assign({ low: v.low, high: v.high }, note);
  }
  return out;
}

// ---------------------------------------------------------------------------------------------------
// The capital return: item 4's key (v3 rekeyCapital) and roads' road key (package.cjs evaluateFull) as rules on the
// evaluation. The road key is the economic-affairs line's key plus the synthetic line's amount over its part's national
// total: roads_vmt_<part> carries HWY_N[part] x (k_road - k_EA), so the sum is k_road for each method and allocation.
const PART_REKEYED = "the parent spending line's amount_bn over its national_bn, plus the correction line's amount_bn over part_national_bn: the key of a part of the parent line (national part_national_bn) that the correction line re-keys";
function capitalOf(oo) {
  const K = BASE.meta.capital_return;
  if (oo.transit !== "population") throw new Error("[BLOCKED] item 8 sits beside the set; its payload is not built");
  if (oo.capital_variant) throw new Error("[BLOCKED] a capital definition variant is not the case");
  const rekeys = {}, departures = [];
  if (oo.housing_capital === "tenants") {
    rekeys[V4.HOUSING_CAPITAL] = Object.assign({}, V4.HOUSING_CAPITAL_KEY, { note: `the rental line's evaluated key, the capital lane's variant ${V4.HOUSING_CAPITAL_VARIANT} (candidate v4 item 4)` });
    departures.push(`${V4.HOUSING_CAPITAL} (public housing's capital) is keyed like public housing's deficit, by the rental line's evaluated key: the capital lane's variant ${V4.HOUSING_CAPITAL_VARIANT} (candidate v4 item 4)`);
  }
  if (oo.roads === "miles") {
    for (const part of ["sl", "fed"]) {
      rekeys[V4.HWY[part].capital] = { kind: "part_rekeyed", parent_line: V4.EA, correction_line: V4.RD_SYN[part], part_national_bn: V4.HWY_N[part],
        note: `the road key k_road, read on the evaluation: ${V4.EA}'s key plus ${V4.RD_SYN[part]}'s amount over the ${V4.HWY[part].subfunction} national total (candidate v4, roads keyed by miles)` };
    }
    departures.push(`${V4.HWY.sl.capital} and ${V4.HWY.fed.capital} take the road key (vehicle miles and freight) through the part_rekeyed rule, not ${V4.EA}'s key (candidate v4, roads keyed by miles)`);
  }
  if (!Object.keys(rekeys).length) return { changed: false, meta: K, rekeys };
  for (const id of Object.keys(rekeys)) if (!K.components.some((c) => c.id === id)) throw new Error(`[BLOCKED] no capital component ${id}`);
  const kinds = Object.assign({}, K.rule_kinds);
  if (Object.values(rekeys).some((k) => k.kind === "part_rekeyed")) kinds.part_rekeyed = PART_REKEYED;
  return { changed: true, rekeys, meta: Object.assign({}, K, {
    rule_kinds: Object.fromEntries(Object.keys(kinds).sort().map((k) => [k, kinds[k]])),
    departures_from_the_capital_lane: K.departures_from_the_capital_lane.concat(departures),
    components: K.components.map((c) => (rekeys[c.id] ? Object.assign({}, c, { key: rekeys[c.id] }) : c)),
  }) };
}

// ---------------------------------------------------------------------------------------------------
// Provenance blocks.
const SUMMARY = readJson(`${LANE}/derived/summary.json`);
const TOUCH = SUMMARY.touch;
const itemOn = (oo, it) => Object.entries(it.o).every(([k, v]) => oo[k] === v);
function pensionBlock(oo) {
  const pp = V4.pensionNet();
  return {
    rule: `social_security's group amount (its preferred key) is ratio_net x the group's OASDI receipts on the reference incidence rule (${V4.OASDI_LINES.join(" + ")} + se_oasdi_share x ${V4.SE_LINE}); medicare's preferred-key amount swaps its Part A share (part_a_share of the amount) for part_a_accrual_bn; federal_income_tax falls by the tax on the group's benefits (benefit_tax_receipt_bn), expanded to every incidence rule. The payload's edits carry these amounts at its own receipts; a consumer that re-keys the OASDI receipts (a generation split) re-applies the rule`,
    ratio_net: pp.ratio_net, part_a_accrual_bn: pp.part_a_accrual_bn, part_a_share: pp.part_a_share, se_oasdi_share: pp.se_oasdi_share,
    oasdi_lines: V4.OASDI_LINES, se_line: V4.SE_LINE, benefit_tax_receipt_bn: pp.receipt_bn,
    rules: { benefit_tax_rule: oo.benefit_tax_rule, accrual_receipts: oo.accrual_receipts, part_a_rule: oo.part_a_rule },
    central: pp.central, scheduled_benefits_arm: { ratio_net: pp.scheduled_ratio_net, note: "the scheduled-benefits arm, beside the case (current law pays the payable benefits)" },
    source: { file: pp.file, commit: pp.commit, sha256: pp.sha256 },
  };
}
function statePricingBlock(oo) {
  const files = ["net_state_correction.csv", "corrections.csv", "receipts_corrections.csv"].map((f) => `${V4.SP_DIR}/${f}`);
  return {
    package: V4.SP_PACKAGE,
    rule: "each synthetic line's group amount is national_gap_bn (the sum over the parent's S&L functions of amount x (price index - 1)) x the parent line's key share (group amount over national total, on its evaluated key); it responds as its parent. Each receipt line's group amount moves by factor x its amount, expanded to every incidence rule",
    lines: V4.SP_LINES.map((id) => ({ line: V4.SP_SYN[id], parent: id, parent_key: V4.SP_KEY[id] || lineOf(MODEL, "spending", id).preferred_key, national_gap_bn: V4.SP_PRE[id] })),
    receipts: Object.fromEntries(Object.entries(V4.SP_RECEIPT).map(([id, v]) => [id, Object.assign({}, v)])),
    rules: { sales_rule: oo.sales_rule, licence_rule: oo.licence_rule },
    source: Object.fromEntries(files.map((f) => [f, fileSha(f)])),
  };
}
function roadsBlock(oo, models4) {
  const files = ["inputs.json", "summary.json"].map((f) => `${V4.RD_DIR}/${f}`);
  const k = models4.map((m) => m.candidate.v4.k_road);
  return {
    rule: "s_vmt(p) = p(1 - u5_group) rho / [p(1 - u5_group) rho + (1 - p)(1 - u5_others)], p the corrected population share; k_road = passenger_share x s_vmt + (1 - passenger_share) x k_freight, k_freight the excise line's key; roads_vmt_<part> = highway_national_bn[part] x (k_road - economic_affairs_services' key); gasoline taxes move by gasoline_bn x (s_vmt - k_excise) on excise_selective_sales and licences by licences_bn x (s_vmt - k_licences) on personal_motor_vehicle, expanded to every incidence rule",
    ratio: V4.RD_RATIO, passenger_share: V4.FP, under5_share: V4.U5, rho: V4.RHO, gasoline_bn: V4.GAS, licences_bn: V4.LIC, highway_national_bn: V4.HWY_N,
    k_road: { methods_mean: Object.fromEntries(ALLOCS.map((a) => [a, mean(k.map((x) => x[a]))])), by_method: Object.fromEntries(METHODS.map((x, i) => [x, k[i]])) },
    rules: { excise_rule: oo.excise_rule, freight_key: oo.freight_key, licence_rule: oo.licence_rule },
    source: Object.fromEntries(files.map((f) => [f, fileSha(f)])),
  };
}

// ---------------------------------------------------------------------------------------------------
// The builder. opts.method: a payload on that method's models alone (the G2 per-method check), built on the September 27
// payload's model rather than on the September 27 method models.
function build(o, opts) {
  const method = opts && opts.method;
  const oo = V4.withCentral(o);
  const models4 = (opts && opts.models4) || METHODS.map((x) => V4.modelFor("central", x, oo));
  const pairs = method ? [{ m4: models4[METHODS.indexOf(method)], base: PM27 }] : models4.map((m4, i) => ({ m4, base: M27[i] }));
  const parts = partsOf(pairs);
  const responses = responsesOf(oo);
  const capital = capitalOf(oo);
  const changed = parts.receipt_lines.length + parts.scales.length + parts.edits.length + parts.lines.length > 0 || parts.production
    || Object.keys(responses).length > 0 || capital.changed;
  if (!changed) return { payload: BASE, parts, responses, capital, models4 };
  const on = V4.SET_ITEMS.filter((it) => itemOn(oo, it));
  const pension = oo.pension4 === "payable_net";
  const tail = [...parts.receipt_lines.map((l) => `receipts:${l.id}`), ...parts.scales.map((e) => `${e.side === "receipt" ? "receipts" : "spending"}:${e.line}`),
    ...parts.edits.map((e) => `${e.side === "receipt" ? "receipts" : "spending"}:${e.line}`)];
  const lineItems = {};
  for (const it of on) for (const t of TOUCH[it.id] || []) (lineItems[t] || (lineItems[t] = [])).push(it.id);
  const meta = Object.assign({}, BASE.meta, {
    source: `${LANE}/payload.cjs`,
    adopted: null,
    decision: null,
    case: `${BASE.meta.case}; candidate v4, not adopted: ${on.map((it) => it.name.replace(/ \(switch\)$/, "")).join("; ")}${pension ? "" : "; pensions in cash"}`,
    builds_on: { source: BASE.meta.source, adopted: BASE.meta.adopted, decision: BASE.meta.decision, case: BASE.meta.case,
      file: ADOPTED_FILE, sha256: sha256(ADOPTED_TEXT) },
    responses: Object.assign({}, BASE.meta.responses, responses),
    previous: `${ADOPTED_FILE} (its lines and edits come first here, unchanged)`,
    capital_return: capital.meta,
    status: "candidate v4, not adopted (2026-09-29): the operator has not decided; an adoption sets adopted and decision",
    candidate_v4: {
      lane: LANE, package: `${LANE}/package.cjs`, run: `${RUN_COMMIT} (derived/bands.csv, per_spec.csv)`,
      set: pension ? "the set: pension accrual at payable benefits, net of the tax on benefits" : "the cash set: the set with the pension switch off",
      items: on.map((it) => ({ id: it.id, name: it.name, options: it.o })),
      rules: Object.fromEntries(Object.keys(V4.RULES).map((k) => [k, oo[k]])),
      beside: V4.BESIDE_ITEMS.map((it) => ({ id: it.id, name: it.name, note: "beside the set; not in this payload" })),
      payload: {
        rule: "the September 27 payload's lines and edits unchanged, then the receipt lines the set adds, a national-scale edit for each line whose national total it changes, and one edit per cell it moves: the two fill-in methods' mean change from the September 27 case's model to v4's (package.cjs modelFor) beyond the scale. The engine's cost is linear in every amount and in the production grid, so the payload's cost at a specification is the two methods' mean",
        september27: { lines: BASE.lines.length, edits: BASE.edits.length },
        receipt_lines: parts.receipt_lines.map((l) => l.id),
        national_scale_edits: parts.scales.map((e) => ({ side: e.side, line: e.line, from_bn: lineOf(MODEL, e.side === "receipt" ? "receipts" : "spending", e.line).national_bn, to_bn: e.national_bn })),
        edits_added: parts.edits.length,
        lines_added: parts.lines.map((l) => l.id),
        production: parts.production ? "row4" : null,
      },
      items_by_line: Object.fromEntries(Object.keys(lineItems).sort().map((t) => [t, lineItems[t]])),
      not_recomputed: ["beside_the_account.congestion is the September 27 figure, with roads on economic_affairs_services' key"],
    },
  });
  if (parts.production) meta.production = { grid: "row4", file: V4.PRODUCTION_FILE, sha256: fileSha(V4.PRODUCTION_FILE),
    rule: "the production model on the account's row-4 weights replaces model.json's grid (private_wtp_bn, induced_receipts_bn, sampling_se_bn), scenario by scenario (item 2)" };
  if (pension) meta.pension_accrual = pensionBlock(oo);
  if (oo.state_price === "central") meta.state_pricing = statePricingBlock(oo);
  if (oo.roads === "miles") meta.roads_mileage_key = roadsBlock(oo, models4);
  const payload = { meta };
  if (parts.receipt_lines.length) payload.receipt_lines = parts.receipt_lines;
  payload.lines = BASE.lines.concat(parts.lines);
  payload.edits = BASE.edits.concat(parts.scales, parts.edits);
  if (parts.production) payload.production = parts.production;
  return { payload, parts, responses, capital, models4, tail, lineItems };
}

// ---------------------------------------------------------------------------------------------------
// The engine as it stood before this lane's optional fields, for the regression gate.
function pinnedEngine() {
  const src = execFileSync("git", ["-C", ROOT, "show", `${ENGINE_PIN}:${ENGINE_PATH}`], { maxBuffer: 1 << 26, stdio: ["ignore", "pipe", "ignore"] }).toString("utf8");
  const mod = new Module(`engine_${ENGINE_PIN}`);
  mod._compile(src, `engine_${ENGINE_PIN}.js`);
  return { api: mod.exports, sha256: sha256(src) };
}

if (require.main === module) {
  console.log("[G1: every item off is the adopted payload]");
  gate("the September 27 package's correctionsPayload() is the adopted corrections.json, byte for byte", serialize(BASE) === ADOPTED_TEXT,
    `${ADOPTED_FILE} ${sha256(ADOPTED_TEXT).slice(0, 12)}`);
  const off = build(V4.OFF);
  gate("every item off: the builder finds no receipt line, national scale, edit, line, production grid, response or capital key",
    !off.parts.receipt_lines.length && !off.parts.scales.length && !off.parts.edits.length && !off.parts.lines.length && !off.parts.production
    && !Object.keys(off.responses).length && !off.capital.changed);
  gate("every item off: the payload equals the adopted corrections.json as JSON (key order included)", JSON.stringify(off.payload) === JSON.stringify(ADOPTED));
  gate("every item off: the payload equals the adopted corrections.json byte for byte", serialize(off.payload) === ADOPTED_TEXT);
  gate("every item off: both methods' models equal the September 27 models in every cell and grid", off.models4.every((m, i) =>
    frame(m) === frame(M27[i]) && ["receipts", "spending"].every((side) => JSON.stringify(m[side].lines) === JSON.stringify(M27[i][side].lines))
    && GRID.every((k) => sameArray(m.production[k], M27[i].production[k]))));

  // ---------------------------------------------------------------------------------------------------
  console.log("\n[the payloads]");
  const SETS = { set: V4.SET, cash: V4.CASH };
  const FILES = { set: "corrections_v4.json", cash: "corrections_v4_cash.json" };
  const built = {}, texts = {};
  for (const [name, o] of Object.entries(SETS)) {
    const b = build(o);
    built[name] = b;
    texts[name] = serialize(b.payload);
    const p = b.payload;
    gate(`${name}: the September 27 lines and edits come first, unchanged`, JSON.stringify(p.lines.slice(0, ADOPTED.lines.length)) === JSON.stringify(ADOPTED.lines)
      && JSON.stringify(p.edits.slice(0, ADOPTED.edits.length)) === JSON.stringify(ADOPTED.edits),
      `${ADOPTED.lines.length} lines, ${ADOPTED.edits.length} edits; then ${b.parts.lines.length} lines, ${b.parts.scales.length} national-scale and ${b.parts.edits.length} cell edits, ${b.parts.receipt_lines.length} receipt lines`);
    const keep = Object.keys(ADOPTED.meta).filter((k) => !["source", "adopted", "decision", "case", "builds_on", "responses", "previous", "capital_return"].includes(k));
    gate(`${name}: meta keeps every September 27 entry: the unchanged ones equal, every September 27 response and capital component but the re-keyed ones`,
      keep.every((k) => JSON.stringify(p.meta[k]) === JSON.stringify(ADOPTED.meta[k]))
      && Object.keys(ADOPTED.meta.responses).every((k) => JSON.stringify(p.meta.responses[k]) === JSON.stringify(ADOPTED.meta.responses[k]))
      && ADOPTED.meta.capital_return.components.every((c, i) => b.capital.rekeys[c.id]
        ? JSON.stringify(without(p.meta.capital_return.components[i], ["key"])) === JSON.stringify(without(c, ["key"]))
        : JSON.stringify(p.meta.capital_return.components[i]) === JSON.stringify(c)),
      `kept ${keep.join(", ")}; re-keyed ${Object.keys(b.capital.rekeys).join(", ")}`);
    gate(`${name}: not adopted (adopted and decision null)`, p.meta.adopted === null && p.meta.decision === null && /not adopted/.test(p.meta.status));
    // Completeness against the task-1 scan (summary.json touch): every line the payload moves belongs to an item that
    // touches it, and every line, capital component and production term an item touches is in the payload.
    const inPayload = new Set([...b.tail, ...b.parts.lines.map((l) => `spending:${l.id}`), ...Object.keys(b.responses).map((id) => (b.responses[id].receipt ? `receipts:${id}` : `spending:${id}`)),
      ...Object.keys(b.capital.rekeys).map((id) => `capital:${id}`), ...(b.parts.production ? ["production:P", "production:F"] : [])]);
    const touched = new Set(Object.keys(b.lineItems));
    const stray = [...inPayload].filter((t) => !touched.has(t)), missing = [...touched].filter((t) => !inPayload.has(t));
    gate(`${name}: the payload moves exactly the lines, capital components and production terms its items touch (summary.json touch)`,
      !stray.length && !missing.length, `${inPayload.size} entries${stray.length ? "; stray " + stray.join(" ") : ""}${missing.length ? "; missing " + missing.join(" ") : ""}`);
    gate(`${name}: the pension accrual block is present exactly when the switch is on`, name === "set" ? !!p.meta.pension_accrual : !p.meta.pension_accrual);
  }
  gate("the set and the cash set differ only in the pension switch's lines, edits and meta", (() => {
    const a = built.set.payload, c = built.cash.payload;
    const key = (e) => `${e.side}|${e.line}|${e.scenario || e.key || ""}|${e.national_bn === undefined ? "" : "scale"}`;
    const ma = new Map(a.edits.map((e) => [key(e), e])), mc = new Map(c.edits.map((e) => [key(e), e]));
    const moved = [...new Set([...ma.keys(), ...mc.keys()])].filter((k) => JSON.stringify(ma.get(k)) !== JSON.stringify(mc.get(k))).map((k) => k.split("|")[1]);
    return [...new Set(moved)].sort().join() === ["federal_income_tax", "medicare", "social_security"].join()
      && canon(a.receipt_lines) === canon(c.receipt_lines) && canon(a.lines) === canon(c.lines) && canon(a.production) === canon(c.production);
  })());

  // ---------------------------------------------------------------------------------------------------
  console.log("\n[G2: a consumer with no package reproduces per_spec.csv]");
  const PER_SPEC = csvRows(`${LANE}/derived/per_spec.csv`);
  const rowOf = (method, i) => {
    const rs = PER_SPEC.filter((r) => r.method === method && (Number(r.spec) === i || Number(r.twin) === i));
    if (rs.length !== 1) throw new Error(`[BLOCKED] per_spec.csv: ${rs.length} rows for ${method} spec ${i}`);
    return rs[0];
  };
  const COL = { set: "set_cost_bn", cash: "cash_cost_bn" };
  const g2 = {};
  for (const name of Object.keys(SETS)) {
    const oo = V4.withCentral(SETS[name]);
    const specs4 = V4.specsFor(oo);
    const b = built[name];
    const res = { per_method: {}, mean: null };
    // Each method's payload, through JSON and the consumer.
    for (const [mi, method] of METHODS.entries()) {
      const pm = JSON.parse(serialize(build(SETS[name], { method, models4: b.models4 }).payload));
      const got = Consumer.evaluateAll(pm, { engine: Engine, model: MODEL });
      const pkg = specs4.map((s) => V4.evaluateFull(b.models4[mi], s));
      const csvGap = Math.max(...got.map((x, i) => Math.abs(x.cost_bn - Number(rowOf(method, i)[COL[name]]))));
      const pkgGap = Math.max(...got.map((x, i) => Math.abs(x.cost_bn - pkg[i].cost_bn)));
      const order = got.every((x, i) => ["allocation", "normalization", "share", "school", "gg", "uc", "reading"].every((f) => x.spec[f] === specs4[i][f]));
      const states = got.every((x, i) => canon(x.state) === canon(V4.stateFor(b.models4[mi], specs4[i])));
      const capGap = Math.max(...got.map((x, i) => {
        const pc = pkg[i].capital.components;
        if (pc.length !== x.capital.components.length) return Infinity;
        return Math.max(...x.capital.components.map((c, j) => (c.id !== pc[j].id ? Infinity
          : Math.max(Math.abs(c.key - pc[j].key), Math.abs(c.response - pc[j].response), Math.abs(c.return_bn - pc[j].return_bn)))));
      }));
      res.per_method[method] = { csv_gap_bn: csvGap, package_gap_bn: pkgGap, capital_gap: capGap };
      gate(`${name}, ${method}: the consumer's specifications are the package's, in order`, order && got.length === 64);
      gate(`${name}, ${method}: the consumer's engine state equals the package's at all 64 specifications`, states);
      gate(`${name}, ${method}: capital components (key, response, return) equal the package's (1e-9)`, capGap < 1e-9, ex(capGap));
      gate(`${name}, ${method}: the method's payload gives per_spec.csv ${COL[name]} at all 64 specifications (1e-6)`, csvGap < 1e-6,
        `max |diff| ${ex(csvGap)}; against a fresh package run ${ex(pkgGap)}`);
    }
    // The written payload, the methods' mean.
    const pay = JSON.parse(texts[name]);
    const got = Consumer.evaluateAll(pay, { engine: Engine, model: MODEL });
    const meanGap = Math.max(...got.map((x, i) => Math.abs(x.cost_bn - mean(METHODS.map((mt) => Number(rowOf(mt, i)[COL[name]]))))));
    res.mean = { csv_gap_bn: meanGap };
    gate(`${name}: derived/${FILES[name]} gives the two methods' mean of per_spec.csv ${COL[name]} at all 64 specifications (1e-6)`, meanGap < 1e-6, `max |diff| ${ex(meanGap)}`);
    // The payload model against the methods' mean model, cell by cell, and the national totals.
    const pmod = Engine.applyCorrections(MODEL, pay);
    let cellGap = 0, natOk = true, lineSet = true, gapGap = 0;
    for (const side of ["receipts", "spending"]) {
      const ids = b.models4[0][side].lines.map((l) => l.id);
      if (pmod[side].lines.map((l) => l.id).join() !== ids.join()) lineSet = false;
      for (const id of ids) {
        const lp = lineOf(pmod, side, id), l4 = b.models4.map((m) => lineOf(m, side, id)), l27 = lineOf(PM27, side, id);
        if (!lp || lp.national_bn !== l4[0].national_bn) { natOk = false; continue; }
        for (const g of Object.keys(groupsOf(side, lp))) for (const a of ALLOCS) {
          const c = groupsOf(side, lp)[g][a];
          for (const k of ["target_bn", "other_bn"]) cellGap = Math.max(cellGap, Math.abs(c[k] - mean(l4.map((l) => groupsOf(side, l)[g][a][k]))));
          // group + other - national: the September 27 payload's gap scaled with the line, 0 on a new line.
          const gap = c.target_bn + c.other_bn - lp.national_bn;
          const want = l27 ? (groupsOf(side, l27)[g][a].target_bn + groupsOf(side, l27)[g][a].other_bn - l27.national_bn) * (lp.national_bn / l27.national_bn || 1) : 0;
          gapGap = Math.max(gapGap, Math.abs(gap - want));
        }
      }
    }
    const gridOk = GRID.every((k) => sameArray(pmod.production[k], b.models4[0].production[k]));
    gate(`${name}: the payload model has v4's lines and national totals, and v4's production grid exactly`, lineSet && natOk && gridOk);
    gate(`${name}: every cell of the payload model is the two methods' mean model (group and other, 1e-9)`, cellGap < 1e-9, ex(cellGap));
    gate(`${name}: national totals hold: each cell's group + other - national is the September 27 payload's, scaled with its line (0 on a new line; 1e-9)`, gapGap < 1e-9, ex(gapGap));
    g2[name] = Object.assign(res, { cell_gap_bn: cellGap, national_gap_bn: gapGap });
  }

  // ---------------------------------------------------------------------------------------------------
  console.log("\n[engine: the optional fields]");
  const PIN = pinnedEngine();
  const OLD_PAYLOADS = ["main_case_2026_09_24", "main_case_2026_09_26", "main_case_schools_full_2026_09_26", "main_case_long_run_2026_09_27"]
    .map((l) => `${l}/derived/corrections.json`).filter((f) => fs.existsSync(path.join(FISCAL, f)));
  const oldSame = OLD_PAYLOADS.map((f) => {
    const pay = readJson(f);
    const a = Engine.applyCorrections(MODEL, pay), b = PIN.api.applyCorrections(MODEL, pay);
    let same = JSON.stringify(a) === JSON.stringify(b);
    // The case's 64 states where the payload carries the meta to build them (September 26 on), else the default state.
    const R = pay.meta && pay.meta.responses;
    const states = R && R.school && R.general_government && Consumer.SYN_CLASSES.every((c) => pay.lines.filter((l) => l.response_class === c).length === 1)
      ? Consumer.evaluateAll(pay, { engine: Engine, model: MODEL }).map((x) => x.state) : [Engine.defaultState(a)];
    for (const s of states) same = same && JSON.stringify(Engine.evaluate(a, s)) === JSON.stringify(PIN.api.evaluate(b, s));
    return { file: f, same, states: states.length };
  });
  gate(`every earlier payload applies and evaluates exactly as with the engine at ${ENGINE_PIN}`, oldSame.length === 4 && oldSame.every((x) => x.same),
    oldSame.map((x) => `${x.file.split("/")[0]} ${x.same ? "same" : "DIFFERS"} (${x.states} states)`).join("; "));
  const throws = (f, re) => { try { f(); return false; } catch (e) { return re.test(e.message); } };
  const ref = MODEL.receipts.reference;
  const cellOf = (t) => ({ target_bn: t, other_bn: 10 - t, share: t / 10, key: "control", direct: true, response_class: "control" });
  const control = { id: "control_receipt", national_bn: 10, cells: Object.fromEntries(MODEL.receipts.scenarios.map((sc) => [sc, { personal: cellOf(1), shared: cellOf(2) }])) };
  const withLine = Engine.applyCorrections(MODEL, { edits: [], receipt_lines: [control] });
  const s0 = Engine.defaultState(MODEL);
  const dDirect = Engine.evaluate(withLine, s0).direct_fiscal_response_bn - Engine.evaluate(MODEL, s0).direct_fiscal_response_bn;
  gate("receipt_lines: a control line enters with its cells and moves the direct account by its group amount at its response",
    lineOf(withLine, "receipts", "control_receipt").cells[ref].shared.target_bn === 2 && Math.abs(dDirect - 1 * s0.direct_receipt_response) < 1e-12, `direct +${dDirect}`);
  const H = lineOf(MODEL, "spending", "housing_subsidies"), hScaled = Engine.applyCorrections(MODEL, { edits: [{ side: "spending", line: "housing_subsidies", national_bn: H.national_bn / 2 }] });
  const h2 = lineOf(hScaled, "spending", "housing_subsidies");
  gate("a national-scale edit halves the line's national total and every cell's group and other amounts; shares hold",
    h2.national_bn === H.national_bn / 2 && Object.keys(H.keys).every((k) => ALLOCS.every((a) => h2.keys[k][a].target_bn === H.keys[k][a].target_bn * 0.5
      && h2.keys[k][a].other_bn === H.keys[k][a].other_bn * 0.5 && h2.keys[k][a].share === H.keys[k][a].share)));
  const ordered = Engine.applyCorrections(MODEL, { edits: [{ side: "spending", line: "housing_subsidies", key: H.preferred_key, by: { personal: 1, shared: 1 } },
    { side: "spending", line: "housing_subsidies", national_bn: H.national_bn * 2 }] });
  gate("a national-scale edit applies in order with the other edits (an edit before it is scaled too)",
    Math.abs(lineOf(ordered, "spending", "housing_subsidies").keys[H.preferred_key].personal.target_bn - 2 * (H.keys[H.preferred_key].personal.target_bn + 1)) < 1e-12);
  const row4 = V4.PROD.grid.row4, dims = Object.fromEntries(Engine.PRODUCTION_DIMS.map((d) => [d, MODEL.production.dims[d]]));
  const withGrid = Engine.applyCorrections(MODEL, { edits: [], production: Object.assign({ dims }, Object.fromEntries(GRID.map((k) => [k, row4[k]]))) });
  const idx = Engine.productionIndex(MODEL, s0.production);
  gate("production: the row-4 grid replaces model.json's arrays and the engine reads P and F from it",
    Engine.evaluate(withGrid, s0).private_wtp_bn === row4.private_wtp_bn[idx] && Engine.evaluate(withGrid, s0).induced_receipts_bn === row4.induced_receipts_bn[idx]
    && MODEL.production.private_wtp_bn[idx] !== row4.private_wtp_bn[idx]);
  const bad = [
    ["a receipt line that exists", () => Engine.applyCorrections(MODEL, { edits: [], receipt_lines: [Object.assign({}, control, { id: "federal_income_tax" })] }), /exists already/],
    ["a receipt line without a cell", () => Engine.applyCorrections(MODEL, { edits: [], receipt_lines: [Object.assign({}, control, { cells: { [ref]: control.cells[ref] } })] }), /lacks an executed cell/],
    ["a receipt line without a national total", () => Engine.applyCorrections(MODEL, { edits: [], receipt_lines: [without(control, ["national_bn"])] }), /lacks a national total/],
    ["a scale edit on an unknown line", () => Engine.applyCorrections(MODEL, { edits: [{ side: "receipt", line: "no_such_line", national_bn: 1 }] }), /Not an executed line to scale/],
    ["a scale edit on a line at national 0", () => Engine.applyCorrections(MODEL, { lines: [{ id: "zero_line", family: "consumption", response_class: "service", label: "control" }], edits: [{ side: "spending", line: "zero_line", national_bn: 1 }] }), /Not a national total/],
    ["a scale edit to a non-number", () => Engine.applyCorrections(MODEL, { edits: [{ side: "spending", line: "housing_subsidies", national_bn: "1" }] }), /Not a national total/],
    ["a production grid of other dimensions", () => Engine.applyCorrections(MODEL, { edits: [], production: Object.assign({ dims: Object.assign({}, dims, { sigma: [1] }) }, Object.fromEntries(GRID.map((k) => [k, row4[k]]))) }), /dimension sigma/],
    ["a production grid of another length", () => Engine.applyCorrections(MODEL, { edits: [], production: Object.assign({ dims }, Object.fromEntries(GRID.map((k) => [k, row4[k].slice(1)]))) }), /Not this model's production grid: private_wtp_bn/],
  ];
  const badOut = bad.map(([label, f, re]) => [label, throws(f, re)]);
  gate("bad input fails loudly", badOut.every(([, ok]) => ok), badOut.map(([l, ok]) => `${l} ${ok ? "throws" : "DOES NOT THROW"}`).join("; "));

  // ---------------------------------------------------------------------------------------------------
  const failures = GATES.filter((g) => !g.pass).length;
  if (failures) {
    console.error(`[BLOCKED] ${failures} gate(s) failed; nothing written`);
    process.exit(1);
  }
  fs.mkdirSync(OUT, { recursive: true });
  for (const name of Object.keys(SETS)) fs.writeFileSync(path.join(OUT, FILES[name]), texts[name]);
  const inputs = [ADOPTED_FILE, `${LANE}/derived/per_spec.csv`, `${LANE}/derived/summary.json`, V4.PRODUCTION_FILE,
    "assumption_explorer_2026_09_21/derived/model.json", "assumption_explorer_2026_09_21/engine.js"];
  const record = {
    lane: LANE, status: "candidate v4's adoption payload, not adopted (2026-09-29)",
    payloads: Object.fromEntries(Object.keys(SETS).map((name) => {
      const b = built[name], p = b.payload;
      return [FILES[name], { bytes: Buffer.byteLength(texts[name]), sha256: sha256(texts[name]), lines: p.lines.length, edits: p.edits.length,
        receipt_lines: (p.receipt_lines || []).map((l) => l.id), national_scale_edits: b.parts.scales.map((e) => `${e.side}:${e.line}`),
        edits_added: b.parts.edits.length, lines_added: b.parts.lines.map((l) => l.id), production: p.production ? "row4" : null,
        responses_added: Object.keys(b.responses), capital_rekeyed: Object.keys(b.capital.rekeys) }];
    })),
    g2,
    engine: { pinned: ENGINE_PIN, pinned_sha256: PIN.sha256, earlier_payloads: oldSame,
      added: ["receipt_lines", "national-scale edits {side, line, national_bn}", "production {dims, private_wtp_bn, induced_receipts_bn, sampling_se_bn}"] },
    gates: GATES,
    inputs: Object.fromEntries(inputs.map((f) => [f, fileSha(f)])),
  };
  fs.writeFileSync(path.join(OUT, "payload_gates.json"), JSON.stringify(record, null, 1) + "\n");
  console.log(`\n[written] ${Object.values(FILES).map((f) => `derived/${f}`).join(", ")}, derived/payload_gates.json; ${GATES.length} gates passed`);
}

module.exports = { build, partsOf, responsesOf, capitalOf, BASE, M27, PM27, RESPONSE_NOTES, PART_REKEYED, serialize, frame };
