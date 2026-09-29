/* Candidate v4.1 (2026-09-30), not adopted: the adopted v4 case (main_case_2026_09_29) with the five inputs that
 * row4_class_2026_09_29 found on the survey's published weights (the CPS ASEC 2025 union of 40,896,574) moved to audit
 * row 4, the frame the rest of the account uses (39,712,493):
 *   owner        modeled_owner_property's group amount, every incidence rule, over kappa (item 5's line kept model.json's
 *                published cell, share 0.063237; row 4 gives 0.062121);
 *   part_a       the pension switch's Part A accrual, $41.137bn summed over the published frame -> the rerun on row 4;
 *   benefit_tax  the pension switch's benefit-tax receipt (removed from federal income tax) -> the rerun on row 4;
 *   state_index  state pricing's gaps sum_f S&L_f x (index_f - 1) and the sales and licence factors, the indexes taken on
 *                the group's state mix -> on row 4's state mix (v4's value x the rerun's row-4 / published ratio; the
 *                receipt factors v4's plus the rerun's change);
 *   oasdi_ratio  the pension switch's ratio_net (accrual per OASDI tax dollar, net of the future benefit tax) -> the rerun's
 *                gross ratio x (1 - the row-4 relative rate x timing).
 * The values are read from row4_class_2026_09_29/derived/*.json. They enter at their inputs: this lane's modelFor is
 * candidate v4's package.cjs modelFor (main_case_candidate_v4_2026_09_29/package.cjs:289-321) step for step, with the
 * pension switch's and state pricing's inputs passed in and the owner line's key corrected where item 5 enters (v3's
 * model); candidate v4's builder (payload.cjs build(), given those models) turns the two fill-in methods' models into the
 * payload. Everything else is v4's: the items, responses, capital components, production grid and specifications.
 * Every package is imported read-only; nothing outside this lane is written.
 *
 * Gates (each prints; any failure exits 1 and writes nothing):
 *   off     with every re-key off, this modelFor is candidate v4's for both methods, set and cash (JSON); the builder's
 *           set payload, stamped by the adopted package's adopt(), is main_case_2026_09_29/derived/corrections.json byte
 *           for byte, and its cash payload is main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json byte for
 *           byte; the adopted band $371.4146 / 434.8410bn and cash $294.7011 / 361.8175bn (summary.json, 1e-9);
 *   on      $371.2146 / 434.6300bn and cash $295.4036 / 362.5193bn (1e-4), the row4_class lane's joint rows;
 *   alone   each re-key alone, and the class-A joint row, gives its price_rekeys.csv row (1e-6; price_rekeys.json 1e-9);
 *   payload the payload model gives the two methods' mean at all 64 specifications (1e-9), and so does candidate v4's
 *           consumer.cjs (engine.js, model.json and the payload, no package);
 *   inputs  the rerun's published values are the builder's inputs (the pension summary's, 1e-9; state pricing's CSV
 *           values, 1e-7).
 * Run from the repository root: node infra/immigration-fiscal/main_case_candidate_v41_2026_09_30/build.cjs
 *   -> derived/corrections_v41.json, corrections_v41_cash.json, bands.csv, per_spec.csv, rekeys_at_inputs.csv,
 *      build_gates.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.resolve(__dirname, "..");
const OUT = path.join(__dirname, "derived");
const LANE = "main_case_candidate_v41_2026_09_30";
const ADOPTED_LANE = "main_case_2026_09_29";
const CAND_LANE = "main_case_candidate_v4_2026_09_29";
const ROW4 = "row4_class_2026_09_29/derived";
const P = require(path.join(FISCAL, ADOPTED_LANE, "package.cjs"));
const Consumer = require(path.join(FISCAL, CAND_LANE, "consumer.cjs"));
const V4 = P.V4PKG, B = P.BUILDER, V3 = V4.V3PKG, S27 = V4.SEPT27;
const { Engine, MODEL, METHODS, ALLOCS } = P;
const { lineOf, byAlloc, refAmount } = V4;

const read = (rel) => fs.readFileSync(path.join(FISCAL, rel), "utf8");
const readJson = (rel) => JSON.parse(read(rel));
const sha256 = (s) => crypto.createHash("sha256").update(s).digest("hex");
const fileSha = (rel) => sha256(fs.readFileSync(path.join(FISCAL, rel)));
const clone = (x) => JSON.parse(JSON.stringify(x));
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
const worst = (xs) => Math.max(0, ...xs.map(Math.abs));
const ex = (x) => x.toExponential(1);
const fx = (x) => x.toFixed(4);
// A CSV line's fields; a double-quoted field may hold commas (bands.csv labels).
const fieldsOf = (line) => (line.match(/("[^"]*"|[^,]*)(,|$)/g) || []).slice(0, -1).map((f) => f.replace(/,$/, "").replace(/^"(.*)"$/, "$1"));
const csvRows = (rel) => {
  const [head, ...lines] = read(rel).trim().split("\n");
  const keys = fieldsOf(head);
  return lines.map((l) => {
    const v = fieldsOf(l);
    if (v.length !== keys.length) throw new Error(`[BLOCKED] ${rel}: a row with ${v.length} fields, not ${keys.length}`);
    return Object.fromEntries(keys.map((k, i) => [k, v[i]]));
  });
};

const GATES = [];
function gate(name, pass, detail) {
  GATES.push({ name, pass: !!pass, detail: detail === undefined ? null : detail });
  console.log(`  ${pass ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
}

// ---------------------------------------------------------------------------------------------------
// The inputs: v4's (published weights) and row 4's (the row4_class lane's reruns).
const FILES = { parta: `${ROW4}/row4_parta.json`, bt: `${ROW4}/row4_benefit_tax.json`, si: `${ROW4}/row4_state_index.json`,
  oa: `${ROW4}/row4_oasdi_ratio.json`, price: `${ROW4}/price_rekeys.json`, price_csv: `${ROW4}/price_rekeys.csv` };
const R4 = Object.fromEntries(Object.entries(FILES).filter(([k]) => k !== "price_csv").map(([k, f]) => [k, readJson(f)]));
const PRICE_CSV = Object.fromEntries(csvRows(FILES.price_csv).map((r) => [r.rekey, r]));
const pp = V4.pensionNet();
const SP_IDS = Object.keys(V4.SP_RECEIPT);
const PUBLISHED = {
  kappa_owner: 1,
  part_a_accrual_bn: pp.part_a_accrual_bn,
  receipt_bn: Object.assign({}, pp.receipt_bn),
  ratio_net: pp.ratio_net,
  sp_pre: Object.assign({}, V4.SP_PRE),
  sp_factor: Object.fromEntries(SP_IDS.map((id) => [id, V4.SP_RECEIPT[id].factor])),
};
const ROW4_INPUTS = {
  kappa_owner: R4.price.kappa_owner,
  part_a_accrual_bn: R4.parta.central.union.row4_bn,
  receipt_bn: { shared: R4.bt.shared.receipt_row4_bn, personal: R4.bt.personal.receipt_row4_bn },
  ratio_net: R4.oa.row4.ratio_gross * (1 - R4.bt.relative_rate_row4 * R4.oa.row4.timing),
  sp_pre: Object.fromEntries(V4.SP_LINES.map((id) => [id, V4.SP_PRE[id] * (R4.si.lines[id].sp_pre_row4_bn / R4.si.lines[id].sp_pre_published_bn)])),
  sp_factor: Object.fromEntries(SP_IDS.map((id) => [id, V4.SP_RECEIPT[id].factor + (R4.si.receipts[id].factor_row4 - R4.si.receipts[id].factor_published)])),
};
const REKEYS = {
  owner: { cls: "A", fields: ["kappa_owner"], set_only: false, label: "owner-occupied property's key (item 5)" },
  part_a: { cls: "A", fields: ["part_a_accrual_bn"], set_only: true, label: "the Part A accrual (pension switch)" },
  benefit_tax: { cls: "A", fields: ["receipt_bn"], set_only: true, label: "the benefit-tax receipt (pension switch)" },
  state_index: { cls: "B", fields: ["sp_pre", "sp_factor"], set_only: false, label: "the state price indexes (state item)" },
  oasdi_ratio: { cls: "B", fields: ["ratio_net"], set_only: true, label: "OASDI ratio_net (pension switch)" },
};
const ALL = Object.keys(REKEYS);
const CLASS_A = ALL.filter((n) => REKEYS[n].cls === "A");
const inputsFor = (names) => Object.assign({}, PUBLISHED, ...names.map((n) => Object.fromEntries(REKEYS[n].fields.map((f) => [f, ROW4_INPUTS[f]]))));

// ---------------------------------------------------------------------------------------------------
// The models: candidate v4's modelFor with the five inputs passed in.
const OWNER = "modeled_owner_property";
const withEdits = (m, edits, lines) => Engine.applyCorrections(m, { lines: lines || [], edits, meta: m.corrections });
// Owner-occupied property's key on row 4: the group's amount over kappa, the same proportional change in every incidence
// rule (the September 24 expand()).
function withOwnerKey(m, inp) {
  const t = refAmount(m, OWNER);
  return withEdits(m, S27.expand([{ side: "receipt", line: OWNER, by: byAlloc((a) => t[a] * (1 / inp.kappa_owner - 1)) }]));
}
// candidate v4's withStatePrice (package.cjs:148-157) with the gaps and factors passed in.
function withStatePrice(m, amounts, inp) {
  const lines = V4.SP_LINES.map((id) => ({ id: V4.SP_SYN[id], family: "consumption", response_class: "service",
    label: `${id} priced where the group lives (state-pricing lane, central package; candidate)` }));
  const edits = V4.SP_LINES.map((id) => {
    const l = lineOf(m, "spending", id), k = l.keys[V4.parentKey(l)];
    return { side: "spending", line: V4.SP_SYN[id], key: "k", by: byAlloc((a) => inp.sp_pre[id] * k[a].target_bn / l.national_bn) };
  });
  const shifts = SP_IDS.filter((id) => amounts[id]).map((id) => ({ side: "receipt", line: id, by: byAlloc((a) => inp.sp_factor[id] * amounts[id][a]) }));
  return withEdits(m, edits.concat(S27.expand(shifts)), lines);
}
// candidate v4's withPensionNet (package.cjs:110-118) with ratio_net, the Part A accrual and the benefit-tax receipt passed in.
function withPensionNet(m, refs, inp) {
  const ss = lineOf(m, "spending", V4.SS_LINE), med = lineOf(m, "spending", V4.MEDICARE_LINE);
  const ks = ss.keys[ss.preferred_key], km = med.keys[med.preferred_key];
  return withEdits(m, [
    { side: "spending", line: V4.SS_LINE, key: ss.preferred_key, by: byAlloc((a) => inp.ratio_net * refs.oasdi[a] - ks[a].target_bn) },
    { side: "spending", line: V4.MEDICARE_LINE, key: med.preferred_key, by: byAlloc((a) => inp.part_a_accrual_bn * refs.partAScale[a] - pp.part_a_share * km[a].target_bn) },
  ].concat(S27.expand([{ side: "receipt", line: V4.FIT_LINE, by: byAlloc((a) => -inp.receipt_bn[a] * refs.fitScale[a]) }])));
}
// candidate v4's modelFor (package.cjs:289-321), step for step.
function modelFor(caseName, method, oo, inp) {
  const v3o = V4.v3Opts(oo);
  const m3v3 = V3.modelFor(caseName, method, v3o);
  const m3 = inp.kappa_owner === 1 ? m3v3 : withOwnerKey(m3v3, inp);
  const no6 = oo.payroll_items === "none" ? m3 : V3.modelFor(caseName, method, Object.assign({}, v3o, { payroll_items: "none" }));
  let m = oo.wc === "pooled_workers_compensation" ? V4.withWorkersCompOnly(m3) : m3;
  const facts = {};
  const both = oo.roads === "miles" && oo.state_price === "central";
  if (oo.roads === "miles") {
    const r = V4.withRoads(m, V4.roadKeysOf(m), V4.roadKeysOf(no6), oo, !(both && oo.licence_rule === "index_only"));
    facts.k_road = r.k_road; facts.k_cons_freight = r.k_cons_freight;
    m = r.m;
  }
  if (oo.state_price === "central") {
    const amounts = {
      [V4.SALES_LINE]: oo.sales_rule === "multiplicative" ? refAmount(m, V4.SALES_LINE) : refAmount(no6, V4.SALES_LINE),
      [V4.LICENCES]: both && oo.licence_rule === "miles_only" ? null
        : both && oo.licence_rule === "additive" ? refAmount(m3, V4.LICENCES) : refAmount(m, V4.LICENCES),
    };
    m = withStatePrice(m, amounts, inp);
  }
  if (oo.pension4 === "payable_net") {
    const base = oo.tax_key === "cbo_2022" && oo.payroll_items === "none" ? m3
      : V3.modelFor(caseName, method, Object.assign({}, v3o, { payroll_items: "none", tax_key: "cbo_2022" }));
    const fit = refAmount(m, V4.FIT_LINE), fit27 = refAmount(base, V4.FIT_LINE);
    const hi = V4.hiOf(m), hi27 = V4.hiOf(no6);
    m = withPensionNet(m, {
      oasdi: oo.accrual_receipts === "set" ? V4.oasdiOf(m) : V4.oasdiOf(no6),
      fitScale: byAlloc((a) => (oo.benefit_tax_rule === "fixed" ? 1 : fit[a] / fit27[a])),
      partAScale: byAlloc((a) => (oo.part_a_rule === "fixed" ? 1 : hi[a] / hi27[a])),
    }, inp);
  }
  return Object.assign({}, m, { candidate: Object.assign({}, m.candidate, { v4: Object.assign(V4.v4Part(oo), facts) }) });
}

// ---------------------------------------------------------------------------------------------------
// The payloads. A build is candidate v4's builder on this lane's models; the v4.1 stamps follow.
const SETS = { set: V4.SET, cash: V4.CASH };
const PKG = { set: P, cash: P.forPayload(readJson(`${CAND_LANE}/derived/corrections_v4_cash.json`)) };
const cache = new Map();
function buildOf(setName, names) {
  const applies = names.filter((n) => !(REKEYS[n].set_only && setName === "cash"));
  const k = `${setName}|${applies.join("+")}`;
  if (cache.has(k)) return cache.get(k);
  const oo = V4.withCentral(SETS[setName]);
  const inp = inputsFor(applies);
  const models4 = METHODS.map((x) => modelFor("central", x, oo, inp));
  const b = B.build(SETS[setName], { models4 });
  const r = { setName, applies, inp, models4, payload: b.payload };
  cache.set(k, r);
  return r;
}
const costAt = (setName, payload, i) => PKG[setName].evaluateFull(Engine.applyCorrections(MODEL, payload), PKG[setName].MAIN_SPECS[i]).cost_bn;
const ends = (setName, payload) => [48, 11].map((i) => costAt(setName, payload, i));

const FROM_TEXT = "; candidate v4, not adopted: ";
const REKEY_TEXT = { owner: "owner-occupied property's key", part_a: "the Part A accrual", benefit_tax: "the benefit-tax receipt",
  state_index: "the state price indexes", oasdi_ratio: "the OASDI accrual ratio" };
const listOf = (xs) => (xs.length > 1 ? `${xs.slice(0, -1).join(", ")} and ${xs[xs.length - 1]}` : xs.join(""));
function stampV41(r) {
  const p = clone(r.payload), m = p.meta;
  const parts = m.case.split(FROM_TEXT);
  if (parts.length !== 2) throw new Error("[BLOCKED] the builder's case text does not name candidate v4 once");
  const REVISES = r.setName === "set" ? `${ADOPTED_LANE}/derived/corrections.json` : `${CAND_LANE}/derived/corrections_v4_cash.json`;
  m.source = `${LANE}/build.cjs`;
  m.case = `${parts[0]}; candidate v4.1, not adopted: v4's items (${parts[1]}) with ${listOf(r.applies.map((n) => REKEY_TEXT[n]))} on audit row 4, the account's frame`;
  m.status = `candidate v4.1, not adopted (2026-09-30): the operator decides; until then the adopted case is ${ADOPTED_LANE}. An adoption sets adopted and decision`;
  const source = (f, field) => ({ file: f, field, sha256: fileSha(f) });
  if (m.pension_accrual) {
    const pa = m.pension_accrual;
    const moved = { ratio_net: "oasdi_ratio", part_a_accrual_bn: "part_a", benefit_tax_receipt_bn: "benefit_tax" };
    const was = {};
    for (const [field, n] of Object.entries(moved)) {
      if (!r.applies.includes(n)) continue;
      was[field] = pa[field];
      pa[field] = field === "benefit_tax_receipt_bn" ? Object.assign({}, r.inp.receipt_bn) : r.inp[field];
    }
    pa.rekeyed_on_row4 = { fields: Object.keys(was), published_weights: was, rule: "each field is the row4_class lane's rerun of the pension lane's own computation at audit row 4's weights; see candidate_v41.rekeys" };
  }
  if (m.state_pricing && r.applies.includes("state_index")) {
    const sp = m.state_pricing, was = { lines: {}, receipts: {} };
    for (const x of sp.lines) { was.lines[x.line] = x.national_gap_bn; x.national_gap_bn = r.inp.sp_pre[x.parent]; }
    for (const [id, v] of Object.entries(sp.receipts)) {
      was.receipts[id] = { factor: v.factor, index: v.index };
      v.factor = r.inp.sp_factor[id];
      v.index = 1 + v.factor * v.national_bn / v.sl_bn;
    }
    sp.rekeyed_on_row4 = { published_weights: was, rule: "the price indexes weight the states by the group's row-4 shares: each gap is v4's x the rerun's row-4 / published ratio, each receipt factor v4's plus the rerun's change; see candidate_v41.rekeys" };
  }
  const D = {
    owner: { input: `${OWNER}'s group amount in every incidence rule, divided by kappa (model.json's published cell, share 0.063237, to the row-4 frame's 0.062121)`,
      published: PUBLISHED.kappa_owner, row4: ROW4_INPUTS.kappa_owner, source: source(FILES.price, "kappa_owner (main_case_decomposition_2026_09_29/derived/summary_sept29.json v4.kappas)") },
    part_a: { input: "meta.pension_accrual.part_a_accrual_bn", published: PUBLISHED.part_a_accrual_bn, row4: ROW4_INPUTS.part_a_accrual_bn,
      source: source(FILES.parta, "central.union.row4_bn") },
    benefit_tax: { input: "meta.pension_accrual.benefit_tax_receipt_bn", published: PUBLISHED.receipt_bn, row4: ROW4_INPUTS.receipt_bn,
      source: source(FILES.bt, "shared.receipt_row4_bn, personal.receipt_row4_bn") },
    state_index: { input: "meta.state_pricing: each line's national_gap_bn and each receipt's factor", published: { national_gap_bn: PUBLISHED.sp_pre, factor: PUBLISHED.sp_factor },
      row4: { national_gap_bn: ROW4_INPUTS.sp_pre, factor: ROW4_INPUTS.sp_factor },
      rule: "v4's gap x the rerun's sp_pre_row4_bn / sp_pre_published_bn; v4's factor + the rerun's factor_row4 - factor_published (the rerun reproduces v4's CSV-based values to 1e-7)",
      source: source(FILES.si, "lines.*.sp_pre_row4_bn / sp_pre_published_bn, receipts.*.factor_row4 - factor_published") },
    oasdi_ratio: { input: "meta.pension_accrual.ratio_net", published: PUBLISHED.ratio_net, row4: ROW4_INPUTS.ratio_net,
      rule: "row4.ratio_gross x (1 - relative_rate_row4 x row4.timing)",
      source: [source(FILES.oa, "row4.ratio_gross, row4.timing"), source(FILES.bt, "relative_rate_row4")] },
  };
  m.candidate_v41 = {
    lane: LANE, builder: `${LANE}/build.cjs`,
    revises: { file: REVISES, sha256: fileSha(REVISES), case: r.setName === "set" ? "the adopted v4 case (adopted 2026-09-29, decisions/2026-09-29-main-case-v4.md)" : "the adopted v4 case's cash set" },
    found_by: "row4_class_2026_09_29 (75d1ae05): lines of v4 keyed on the survey's published weights (the CPS ASEC 2025 union of 40,896,574) instead of audit row 4's (39,712,493)",
    rule: "each input below replaces v4's published-weight value where candidate v4's package reads it (this lane's modelFor is main_case_candidate_v4_2026_09_29/package.cjs modelFor with the inputs passed in); candidate v4's builder (payload.cjs build()) turns the two fill-in methods' models into this payload. Items, responses, capital components, production grid and specifications are v4's",
    rekeys: r.applies.map((n) => Object.assign({ id: n, label: REKEYS[n].label, class: REKEYS[n].cls }, D[n])),
    not_in_this_set: ALL.filter((n) => !r.applies.includes(n)).map((n) => `${n}: the pension switch is off in the cash set`),
    not_rekeyed: [
      "se_oasdi_share, the OASDI part of self-employment tax: 0.803496 on the published weights, 0.803466 on row 4 (row4_oasdi_ratio.json); negligible, kept",
      "the scheduled-benefits arm's ratio_net (meta.pension_accrual.scheduled_benefits_arm), beside the case, stays on the published weights",
      "item 7's pooled 2019-2024 workers'-compensation ratio: each year at pwwgt0; row 4 exists only for income year 2024",
      "item 5's tenant and personal-property keys: ACS 2024 shares, neither frame",
      "meta.responses.modeled_owner_property's rule says the line keeps its key: that is item 5's rule; here the key is row 4's",
    ],
  };
  return p;
}
const serialize = B.serialize;

// ---------------------------------------------------------------------------------------------------
if (require.main === module) {
  console.log("[inputs: the reruns' published values are the builder's]");
  gate("Part A accrual: the rerun's published total is the pension summary's (v4's input; 1e-9)", Math.abs(R4.parta.central.union.published_bn - pp.part_a_accrual_bn) < 1e-9,
    `${pp.part_a_accrual_bn} -> row 4 ${ROW4_INPUTS.part_a_accrual_bn}`);
  gate("benefit-tax receipt: the rerun's published receipts are v4's (1e-9)", ALLOCS.every((a) => Math.abs(R4.bt[a].receipt_published_bn - pp.receipt_bn[a]) < 1e-9),
    ALLOCS.map((a) => `${a} ${pp.receipt_bn[a].toFixed(6)} -> ${ROW4_INPUTS.receipt_bn[a].toFixed(6)}`).join("; "));
  gate("ratio_net: the rerun's published ratio is v4's (1e-9)", Math.abs(R4.oa.published.ratio_net - pp.ratio_net) < 1e-9, `${pp.ratio_net} -> row 4 ${ROW4_INPUTS.ratio_net}`);
  gate("ratio_net on row 4 is price_rekeys.json's oasdi_ratio.row4", ROW4_INPUTS.ratio_net === R4.price.oasdi_ratio.row4);
  gate("state pricing: the rerun's published gaps are v4's CSV-based SP_PRE (1e-7)", V4.SP_LINES.every((id) => Math.abs(R4.si.lines[id].sp_pre_published_bn - V4.SP_PRE[id]) < 1e-7),
    V4.SP_LINES.map((id) => `${id} ${V4.SP_PRE[id].toFixed(6)} -> ${ROW4_INPUTS.sp_pre[id].toFixed(6)}`).join("; "));
  gate("state pricing: the rerun's published receipt factors are v4's (1e-9)", SP_IDS.every((id) => Math.abs(R4.si.receipts[id].factor_published - V4.SP_RECEIPT[id].factor) < 1e-9),
    SP_IDS.map((id) => `${id} ${V4.SP_RECEIPT[id].factor.toFixed(6)} -> ${ROW4_INPUTS.sp_factor[id].toFixed(6)}`).join("; "));
  const kappas = readJson("main_case_decomposition_2026_09_29/derived/summary_sept29.json").v4.kappas;
  gate("owner kappa is the decomposition lane's (summary_sept29.json v4.kappas), the same at both ends",
    ROW4_INPUTS.kappa_owner === kappas.low[OWNER] && ROW4_INPUTS.kappa_owner === kappas.high[OWNER] && ROW4_INPUTS.kappa_owner > 1, `${ROW4_INPUTS.kappa_owner}`);
  gate("every row4_class output was written with its gates passed", ["parta", "bt", "si", "oa"].every((k) => Array.isArray(R4[k].gates_failed) && !R4[k].gates_failed.length)
    && R4.price.gates_failed === 0);

  // ---------------------------------------------------------------------------------------------------
  console.log("\n[off: every re-key off is the adopted case]");
  const ADOPTED_FILE = `${ADOPTED_LANE}/derived/corrections.json`, CASH_FILE = `${CAND_LANE}/derived/corrections_v4_cash.json`;
  const SUMMARY = readJson(`${ADOPTED_LANE}/derived/summary.json`);
  const off = { set: buildOf("set", []), cash: buildOf("cash", []) };
  for (const s of ["set", "cash"]) {
    const ref = METHODS.map((x) => V4.modelFor("central", x, V4.withCentral(SETS[s])));
    gate(`${s}: this lane's modelFor with v4's inputs is candidate v4's modelFor, both methods (JSON)`,
      ref.every((m, i) => JSON.stringify(m) === JSON.stringify(off[s].models4[i])));
  }
  const offSetText = serialize(P.adopt(off.set.payload)), offCashText = serialize(off.cash.payload);
  gate(`set: the builder's payload, stamped by the adopted package's adopt(), is ${ADOPTED_FILE} byte for byte`, offSetText === read(ADOPTED_FILE),
    `${Buffer.byteLength(offSetText)} bytes, sha256 ${sha256(offSetText).slice(0, 12)}`);
  gate(`cash: the builder's payload is ${CASH_FILE} byte for byte`, offCashText === read(CASH_FILE), `sha256 ${sha256(offCashText).slice(0, 12)}`);
  const base = { set: ends("set", off.set.payload), cash: ends("cash", off.cash.payload) };
  gate("set: $371.4146 / 434.8410bn, the adopted summary.json's main_case (1e-9)", base.set.every((x, j) => Math.abs(x - SUMMARY.main_case[j]) < 1e-9)
    && base.set.every((x, j) => Math.abs(x - [371.4146, 434.8410][j]) < 1e-4), base.set.map(fx).join(" / "));
  gate("cash: $294.7011 / 361.8175bn, the adopted summary.json's cash_set (1e-9)", base.cash.every((x, j) => Math.abs(x - SUMMARY.cash_set.band_bn[j]) < 1e-9)
    && base.cash.every((x, j) => Math.abs(x - [294.7011, 361.8175][j]) < 1e-4), base.cash.map(fx).join(" / "));

  // ---------------------------------------------------------------------------------------------------
  console.log("\n[alone: each re-key at its inputs against the row4_class lane's pricing]");
  const CONFIGS = Object.fromEntries(ALL.map((n) => [n, [n]]).concat([["joint_published_frame", CLASS_A], ["joint_with_ratios", ALL]]));
  const alone = {};
  for (const [row, names] of Object.entries(CONFIGS)) {
    const got = {};
    for (const s of ["set", "cash"]) {
      const cost = ends(s, buildOf(s, names).payload);
      got[s] = { cost, move: cost.map((x, j) => x - base[s][j]) };
    }
    alone[row] = got;
    const pj = R4.price.rows[row], pc = PRICE_CSV[row];
    const csvGap = worst([pc.set_move_48 - got.set.move[0], pc.set_move_11 - got.set.move[1], pc.set_cost_48 - got.set.cost[0], pc.set_cost_11 - got.set.cost[1],
      pc.cash_move_48 - got.cash.move[0], pc.cash_move_11 - got.cash.move[1]].map(Number));
    const jsonGap = worst(["set", "cash"].flatMap((s) => [0, 1].flatMap((j) => [pj[s].cost[j] - got[s].cost[j], pj[s].move[j] - got[s].move[j]])));
    gate(`${row}: price_rekeys.csv's row (1e-6) and price_rekeys.json's (1e-9)`, csvGap < 1e-6 && jsonGap < 1e-9,
      `set ${got.set.move.map(fx).join(" / ")}, cash ${got.cash.move.map(fx).join(" / ")}; max |diff| csv ${ex(csvGap)}, json ${ex(jsonGap)}`);
  }

  // ---------------------------------------------------------------------------------------------------
  console.log("\n[on: candidate v4.1]");
  const v41 = { set: buildOf("set", ALL), cash: buildOf("cash", ALL) };
  const stamped = { set: stampV41(v41.set), cash: stampV41(v41.cash) };
  const texts = { set: serialize(stamped.set), cash: serialize(stamped.cash) };
  const on = { set: ends("set", JSON.parse(texts.set)), cash: ends("cash", JSON.parse(texts.cash)) };
  gate("set: $371.2146 / 434.6300bn (1e-4)", on.set.every((x, j) => Math.abs(x - [371.2146, 434.6300][j]) < 1e-4), on.set.map(fx).join(" / "));
  gate("cash: $295.4036 / 362.5193bn (1e-4)", on.cash.every((x, j) => Math.abs(x - [295.4036, 362.5193][j]) < 1e-4), on.cash.map(fx).join(" / "));
  for (const s of ["set", "cash"]) {
    const a = off[s].payload, b = JSON.parse(texts[s]);
    const key = (e) => `${e.side}|${e.line}|${e.scenario || e.key || ""}|${e.national_bn === undefined ? "" : "scale"}`;
    const added = b.edits.filter((e) => e.line === OWNER);
    gate(`${s}: lines, receipt lines, production grid, meta.responses and meta.capital_return are v4's; v4's edits keep their order, and the owner line adds one edit per incidence rule`,
      ["lines", "receipt_lines", "production"].every((k) => JSON.stringify(a[k]) === JSON.stringify(b[k]))
      && JSON.stringify(a.meta.responses) === JSON.stringify(b.meta.responses) && JSON.stringify(a.meta.capital_return) === JSON.stringify(b.meta.capital_return)
      && !a.edits.some((e) => e.line === OWNER) && added.length === MODEL.receipts.scenarios.length
      && JSON.stringify(b.edits.filter((e) => e.line !== OWNER).map(key)) === JSON.stringify(a.edits.map(key)),
      `${a.edits.length} -> ${b.edits.length} edits`);
    const ma = new Map(a.edits.map((e) => [key(e), e])), mb = new Map(b.edits.map((e) => [key(e), e]));
    const moved = [...new Set([...ma.keys(), ...mb.keys()].filter((k) => JSON.stringify(ma.get(k)) !== JSON.stringify(mb.get(k))).map((k) => k.split("|")[1]))].sort();
    const want = s === "set"
      ? [OWNER, V4.FIT_LINE, V4.LICENCES, V4.SALES_LINE, V4.MEDICARE_LINE, V4.SS_LINE, ...V4.SP_LINES.map((id) => V4.SP_SYN[id])].sort()
      : [OWNER, V4.LICENCES, V4.SALES_LINE, ...V4.SP_LINES.map((id) => V4.SP_SYN[id])].sort();
    gate(`${s}: the edits that move are exactly the re-keyed lines'`, moved.join() === want.join(), moved.join(", "));
    gate(`${s}: not adopted (adopted and decision null), candidate v4.1 in case and status`, b.meta.adopted === null && b.meta.decision === null
      && /candidate v4\.1, not adopted/.test(b.meta.case) && /candidate v4\.1, not adopted/.test(b.meta.status));
  }
  gate("set: meta.pension_accrual carries the row-4 ratio_net, Part A accrual and benefit-tax receipt", (() => {
    const pa = stamped.set.meta.pension_accrual;
    return pa.ratio_net === ROW4_INPUTS.ratio_net && pa.part_a_accrual_bn === ROW4_INPUTS.part_a_accrual_bn
      && ALLOCS.every((a) => pa.benefit_tax_receipt_bn[a] === ROW4_INPUTS.receipt_bn[a]) && pa.rekeyed_on_row4.fields.length === 3;
  })());
  gate("cash: no pension accrual block (the switch is off)", !stamped.cash.meta.pension_accrual);

  // ---------------------------------------------------------------------------------------------------
  console.log("\n[payload: the two methods' mean at all 64 specifications]");
  const CASES = [
    ["sept29", "the adopted v4 case (main_case_2026_09_29)", "set", off.set, JSON.parse(offSetText)],
    ["v41", "candidate v4.1: v4 with the five published-weight inputs on audit row 4", "set", v41.set, JSON.parse(texts.set)],
    ["sept29_cash", "the adopted case's cash set (pension switch off)", "cash", off.cash, JSON.parse(offCashText)],
    ["v41_cash", "candidate v4.1's cash set: owner property and state pricing on row 4", "cash", v41.cash, JSON.parse(texts.cash)],
  ];
  const X = {};
  for (const [k, label, s, built, payload] of CASES) {
    const pk = PKG[s], specs = pk.MAIN_SPECS;
    const costs = built.models4.map((m) => specs.map((spec) => pk.evaluateFull(m, spec).cost_bn));
    const pm = Engine.applyCorrections(MODEL, payload);
    const pay = specs.map((spec) => pk.evaluateFull(pm, spec).cost_bn);
    const meanCosts = specs.map((_, i) => mean(costs.map((c) => c[i])));
    const gap = worst(pay.map((x, i) => x - meanCosts[i]));
    gate(`${k}: the payload model gives the two methods' mean at every specification (1e-9)`, specs.length === 64 && gap < 1e-9, `max |diff| ${ex(gap)}`);
    const ind = Consumer.evaluateAll(clone(payload), { engine: Engine, model: MODEL });
    const indGap = worst(ind.map((x, i) => x.cost_bn - pay[i]));
    gate(`${k}: consumer.cjs (engine.js, model.json and the payload, no package) gives the same at every specification (1e-9)`,
      ind.length === 64 && ind.every((x, i) => ["allocation", "normalization", "share", "school", "gg", "uc", "reading"].every((f) => x.spec[f] === specs[i][f])) && indGap < 1e-9,
      `max |diff| ${ex(indGap)}`);
    const idx = costs.map((c) => [c.indexOf(Math.min(...c)), c.indexOf(Math.max(...c))]);
    gate(`${k}: both methods' ends are specifications 48 / 11`, idx.every((e) => e[0] === 48 && e[1] === 11), idx.map((e) => e.join("/")).join(", "));
    X[k] = { label, s, specs, costs, pay, idx };
  }
  gate("the adopted case's per-method ends are candidate v4's bands.csv (1e-4)", (() => {
    const rows = csvRows(`${CAND_LANE}/derived/bands.csv`);
    return [["sept29", "set"], ["sept29_cash", "cash"]].every(([k, c]) => METHODS.every((meth, mi) => {
      const r = rows.find((x) => x.case === c && x.method === meth);
      return Math.abs(X[k].costs[mi][48] - Number(r.spec48_bn)) < 1e-4 && Math.abs(X[k].costs[mi][11] - Number(r.spec11_bn)) < 1e-4;
    }));
  })());

  // ---------------------------------------------------------------------------------------------------
  const failures = GATES.filter((g) => !g.pass).length;
  if (failures) {
    console.error(`[BLOCKED] ${failures} gate(s) failed; nothing written`);
    process.exit(1);
  }
  const perMember = (bn) => bn * 1e9 / V4.COUNT;
  const bands = ["case,label,method,spec48_bn,spec11_bn,per_member_spec48_usd,per_member_spec11_usd,own_low_spec,own_high_spec,own_low_bn,own_high_bn"];
  for (const [k, x] of Object.entries(X)) {
    METHODS.forEach((meth, mi) => {
      const c = x.costs[mi];
      bands.push([k, `"${x.label}"`, meth, fx(c[48]), fx(c[11]), perMember(c[48]).toFixed(0), perMember(c[11]).toFixed(0), x.idx[mi][0], x.idx[mi][1],
        fx(c[x.idx[mi][0]]), fx(c[x.idx[mi][1]])].join(","));
    });
    const own = [0, 1].map((e) => mean(x.idx.map((ij, mi) => x.costs[mi][ij[e]])));
    bands.push([k, `"${x.label}"`, "mean", fx(x.pay[48]), fx(x.pay[11]), perMember(x.pay[48]).toFixed(0), perMember(x.pay[11]).toFixed(0), 48, 11, fx(own[0]), fx(own[1])].join(","));
  }
  const perSpec = ["method,spec,allocation,normalization,share,school,gg,uc,justice,reading,rate,enterprises,sept29_cost_bn,v41_cost_bn,sept29_cash_cost_bn,v41_cash_cost_bn"];
  const specCols = (s) => [s.allocation, s.normalization, s.share, s.school, s.gg, s.uc, s.justice, s.reading, s.rate, s.enterprises];
  for (const [mi, meth] of METHODS.concat(["mean"]).entries()) {
    X.sept29.specs.forEach((spec, i) => {
      const at = (k) => (meth === "mean" ? X[k].pay[i] : X[k].costs[mi][i]);
      perSpec.push([meth, i, ...specCols(spec), at("sept29"), at("v41"), at("sept29_cash"), at("v41_cash")].join(","));
    });
  }
  const rekeys = ["rekey,class,set_move_48,set_move_11,set_cost_48,set_cost_11,cash_move_48,cash_move_11"];
  const CLS = Object.assign(Object.fromEntries(ALL.map((n) => [n, REKEYS[n].cls])), { joint_published_frame: "A", joint_with_ratios: "A+B" });
  for (const [row, g] of Object.entries(alone)) {
    rekeys.push([row, CLS[row], ...g.set.move, ...g.set.cost, ...g.cash.move].map((v) => (typeof v === "number" ? v.toFixed(6) : v)).join(","));
  }
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, "corrections_v41.json"), texts.set);
  fs.writeFileSync(path.join(OUT, "corrections_v41_cash.json"), texts.cash);
  fs.writeFileSync(path.join(OUT, "bands.csv"), bands.join("\n") + "\n");
  fs.writeFileSync(path.join(OUT, "per_spec.csv"), perSpec.join("\n") + "\n");
  fs.writeFileSync(path.join(OUT, "rekeys_at_inputs.csv"), rekeys.join("\n") + "\n");
  const inputs = [ADOPTED_FILE, CASH_FILE, `${ADOPTED_LANE}/derived/summary.json`, `${CAND_LANE}/derived/bands.csv`, ...Object.values(FILES),
    "assumption_explorer_2026_09_21/derived/model.json", "assumption_explorer_2026_09_21/engine.js"];
  const record = {
    lane: LANE, status: "candidate v4.1, not adopted (2026-09-30): the operator decides",
    payloads: Object.fromEntries(["set", "cash"].map((s) => [s === "set" ? "corrections_v41.json" : "corrections_v41_cash.json", {
      bytes: Buffer.byteLength(texts[s]), sha256: sha256(texts[s]), lines: stamped[s].lines.length, edits: stamped[s].edits.length,
      rekeys: v41[s].applies, at_48_11_bn: on[s], adopted_at_48_11_bn: base[s] }])),
    inputs_published: PUBLISHED, inputs_row4: ROW4_INPUTS,
    gates: GATES,
    inputs: Object.fromEntries(inputs.map((f) => [f, fileSha(f)])),
  };
  fs.writeFileSync(path.join(OUT, "build_gates.json"), JSON.stringify(record, null, 1) + "\n");
  console.log(`\n[written] derived/corrections_v41.json, corrections_v41_cash.json, bands.csv, per_spec.csv, rekeys_at_inputs.csv, build_gates.json; ${GATES.length} gates passed`);
  console.log(bands.join("\n"));
  console.log(rekeys.join("\n"));
}

module.exports = { PUBLISHED, ROW4_INPUTS, REKEYS, inputsFor, modelFor, buildOf, stampV41 };
